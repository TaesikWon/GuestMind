# app/core/auth_utils.py
from fastapi import Depends, HTTPException, status, Header
from jose import JWTError, jwt
from typing import Optional
from app.config import settings
from app.models.user import User
from app.database import SessionLocal
import logging

logger = logging.getLogger("soulstay.auth_utils")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def get_user_from_token(token: str) -> Optional[User]:
    """JWT 토큰에서 user_id 추출 후 DB 조회"""
    db = SessionLocal()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            logger.warning("❌ Invalid token: missing 'sub'")
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            logger.warning(f"❌ Token references non-existent user_id={user_id}")
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.exception(f"Token processing error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()


def get_current_user(
    authorization: Optional[str] = Header(default=None)
) -> User:
    """
    ✅ 일반 로그인 필요 엔드포인트용
    - Authorization 헤더에서 Bearer 토큰 추출 후 검증
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.split(" ")[1]
    return get_user_from_token(token)


def get_current_user_optional(
    authorization: Optional[str] = Header(default=None)
) -> Optional[User]:
    """
    ✅ 선택적 로그인 유틸
    - 토큰 없거나 잘못돼도 None 반환
    """
    if not authorization or not authorization.startswith("Bearer "):
        logger.debug("비로그인 요청 (토큰 없음)")
        return None

    token = authorization.split(" ")[1]
    try:
        return get_user_from_token(token)
    except HTTPException:
        logger.debug("비로그인 요청 (잘못된 토큰)")
        return None
