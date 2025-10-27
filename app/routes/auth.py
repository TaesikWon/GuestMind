# app/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends, Response, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_service import authenticate_user, create_user
from app.utils.token_service import generate_token_pair, verify_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])


# ✅ 회원가입
@router.post("/signup")
def signup(username: str, password: str):
    user = create_user(username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User created successfully"}


# ✅ 로그인 → Access + Refresh Token 쿠키에 저장
@router.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    사용자 인증 후 Access / Refresh Token 발급
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    tokens = generate_token_pair({"username": user.username})

    # 쿠키 저장 (HttpOnly → 클라이언트 JS 접근 불가)
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=False,  # HTTPS 환경이면 True로 설정
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=False,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        samesite="lax"
    )

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

    from app.utils.token_service import create_access_token
    new_access_token = create_access_token({"sub": username})

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=False,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )

    return {"access_token": new_access_token, "message": "Access token refreshed"}


# ✅ 로그아웃
@router.post("/logout")
def logout(response: Response):
    """
    저장된 쿠키 삭제 → 완전 로그아웃
    """
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}
