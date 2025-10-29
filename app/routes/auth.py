# app/routes/auth.py
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Response,
    Request,
    status,
    Form
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import re
import logging

from app.services.user_service import authenticate_user, create_user
from app.utils.token_service import generate_token_pair, verify_token, create_access_token
from app.config import settings
from app.database import get_db
from app.models.user import User

# -------------------------------
# 설정
# -------------------------------
router = APIRouter(prefix="/auth", tags=["Auth"])
logger = logging.getLogger("soulstay.auth")
templates = Jinja2Templates(directory="app/templates")

# -------------------------------
# ✅ 비밀번호 유효성 검사 함수
# -------------------------------
def validate_password(password: str):
    """
    비밀번호 유효성 검사
    - 8자 이상
    - 영문 + 숫자 조합
    """
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="비밀번호는 8자 이상이어야 합니다.")
    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="비밀번호는 영문과 숫자를 포함해야 합니다.")
    return True


# -------------------------------
# 🧩 HTML 렌더링 (로그인 / 회원가입 페이지)
# -------------------------------
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """로그인 페이지 HTML"""
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    """회원가입 페이지 HTML"""
    return templates.TemplateResponse("signup.html", {"request": request})


# -------------------------------
# ✅ 회원가입
# -------------------------------
@router.post("/signup")
def signup(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """
    새 사용자 생성 (유효성 검사 + 중복 방지)
    """
    validate_password(password)

    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        logger.warning(f"Signup failed: username '{username}' already exists.")
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자명입니다.")

    user = create_user(db, username, password)
    logger.info(f"✅ New user created: {username}")
    return {"message": "회원가입이 완료되었습니다."}


# -------------------------------
# ✅ 로그인 → Access + Refresh Token 쿠키 저장
# -------------------------------
@router.post("/login")
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    사용자 인증 후 Access / Refresh Token 발급
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Login failed for user: {form_data.username}")
        raise HTTPException(status_code=401, detail="잘못된 사용자명 또는 비밀번호입니다.")

    tokens = generate_token_pair({"sub": user.username})
    is_secure = settings.ENVIRONMENT == "production"

    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=is_secure,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=is_secure,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        samesite="lax"
    )

    logger.info(f"✅ User '{user.username}' logged in successfully.")
    return {"message": "로그인 성공"}


# -------------------------------
# ✅ 토큰 재발급
# -------------------------------
@router.post("/refresh")
def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token이 없습니다.")

    payload = verify_token(refresh_token, "refresh")
    if not payload:
        raise HTTPException(status_code=401, detail="Refresh token이 만료되었거나 유효하지 않습니다.")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    new_access_token = create_access_token({"sub": username})

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )

    logger.info(f"🔄 Access token refreshed for user: {username}")
    return {"access_token": new_access_token, "message": "Access token refreshed"}


# -------------------------------
# ✅ 현재 로그인한 사용자 확인
# -------------------------------
def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token이 없습니다.")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰 정보가 올바르지 않습니다.")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰이 만료되었거나 잘못되었습니다.")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="사용자를 찾을 수 없습니다.")

    return user


# -------------------------------
# ✅ 로그아웃
# -------------------------------
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    logger.info("🚪 User logged out successfully.")
    return {"message": "로그아웃 완료"}
