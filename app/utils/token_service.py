# app/utils/token_service.py
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional, Dict, Any
from app.config import settings


# ✅ Access Token 생성
def create_access_token(data: dict) -> str:
    """사용자 정보 기반 Access Token 생성"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# ✅ Refresh Token 생성
def create_refresh_token(data: dict) -> str:
    """Refresh Token 생성 (유효기간: 기본 7일)"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# ✅ 토큰 검증 (Access / Refresh 공용)
def verify_token(token: str, expected_type: str = "access") -> Optional[Dict[str, Any]]:
    """
    JWT 토큰 검증 후 payload 반환
    - expected_type: 'access' 또는 'refresh'
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_type = payload.get("type")

        if token_type != expected_type:
            return None  # 타입 불일치 → 거부

        username: str = payload.get("sub")
        if username is None:
            return None

        return payload  # payload 전체 반환
    except JWTError:
        return None


# ✅ (선택) 토큰 생성 단축 함수 (로그인 시 사용)
def generate_token_pair(user: Dict[str, Any]) -> Dict[str, str]:
    """
    로그인 시 Access + Refresh Token 세트 생성
    """
    access_token = create_access_token({"sub": user["username"]})
    refresh_token = create_refresh_token({"sub": user["username"]})
    return {"access_token": access_token, "refresh_token": refresh_token}
