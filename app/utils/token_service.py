# app/utils/token_service.py
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional, Dict, Any
from app.config import settings
import logging

# 🔹 로거 초기화
logger = logging.getLogger("soulstay.token_service")


# ✅ Access Token 생성
def create_access_token(data: dict) -> str:
    """사용자 정보 기반 Access Token 생성"""
    try:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "access"})
        token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        logger.info(f"Access token created for user={data.get('sub')}")
        return token
    except Exception as e:
        logger.error(f"Access token generation failed: {e}")
        raise


# ✅ Refresh Token 생성
def create_refresh_token(data: dict) -> str:
    """Refresh Token 생성 (유효기간: 기본 7일)"""
    try:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        logger.info(f"Refresh token created for user={data.get('sub')}")
        return token
    except Exception as e:
        logger.error(f"Refresh token generation failed: {e}")
        raise


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
            logger.warning(f"Token type mismatch: expected={expected_type}, got={token_type}")
            return None

        username = payload.get("sub")
        if not username:
            logger.warning("Token missing 'sub' field")
            return None

        return payload
    except JWTError as e:
        logger.warning(f"Token verification failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in verify_token: {e}")
        return None


# ✅ 토큰 생성 단축 함수 (로그인 시 사용)
def generate_token_pair(user: Dict[str, Any]) -> Dict[str, str]:
    """
    로그인 시 Access + Refresh Token 세트 생성
    """
    username = user.get("username") or user.get("sub")
    if not username:
        logger.error("Token generation failed: missing username/sub")
        raise ValueError("User data must include 'username' or 'sub'")

    access_token = create_access_token({"sub": username})
    refresh_token = create_refresh_token({"sub": username})
    logger.info(f"Token pair generated for {username}")
    return {"access_token": access_token, "refresh_token": refresh_token}
