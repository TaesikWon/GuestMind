from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Response,
    Request,
    status
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import logging

from app.services.user_service import authenticate_user, create_user
from app.utils.token_service import generate_token_pair, verify_token, create_access_token
from app.config import settings
from app.database import get_db
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])
logger = logging.getLogger("soulstay.auth")

# ✅ 회원가입
@router.post("/signup")
def signup(username: str, password: str, db: Session = Depends(get_db)):
    """
    새 사용자 생성 (이미 존재하면 400)
    """
    user = create_user(db, username, password)
    if not user:
        logger.warning(f"Signup failed: username '{username}' already exists.")
        raise HTTPException(status_code=400, detail="Username already exists")
    logger.info(f"New user created: {username}")
    return {"message": "User created successfully"}

# ✅ 로그인 → Access + Refresh Token 쿠키에 저장
@router.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    사용자 인증 후 Access / Refresh Token 발급
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Login failed for user: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    tokens = generate_token_pair({"sub": user.username})

    # Access Token 쿠키 저장
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=False,  # HTTPS 환경에서는 True
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )

    # Refresh Token 쿠키 저장
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=False,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        samesite="lax"
    )

    logger.info(f"User '{user.username}' logged in successfully.")
    return {"message": "Login successful"}

# ✅ 토큰 재발급
@router.post("/refresh")
def refresh_token(request: Request, response: Response):
    """
    Refresh Token으로 새 Access Token 발급
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    payload = verify_token(refresh_token, "refresh")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid payload")

    new_access_token = create_access_token({"sub": username})

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=False,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )

    logger.info(f"Access token refreshed for user: {username}")
    return {"access_token": new_access_token, "message": "Access token refreshed"}

# ✅ 현재 로그인한 사용자 확인용
def get_current_user(request: Request, db: Session = Depends(get_db)):
    """
    쿠키에 저장된 Access Token을 해독해 현재 사용자 반환
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user

# ✅ 로그아웃
@router.post("/logout")
def logout(response: Response):
    """
    저장된 쿠키 삭제 → 완전 로그아웃
    """
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    logger.info("User logged out successfully.")
    return {"message": "Logged out successfully"}
