# app/core/auth_utils.py

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from typing import Optional
from app.config import settings
from app.models.user import User
from app.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def get_user_from_token(token: str) -> Optional[User]:
    """JWT 토큰에서 user_id 추출 후 DB 조회"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token: missing user_id")

        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        db.close()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError as e:
        logger.warning(f"JWT 토큰 검증 실패: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(f"토큰 처리 중 오류: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def get_current_user_optional(token: Optional[str] = None) -> Optional[User]:
    """
    ✅ 선택적 로그인 유틸
    - 로그인 안 되어 있으면 None
    - 유효한 JWT 있으면 User 반환
    """
    if not token:
        logger.debug("비로그인 요청: 토큰 없음")
        return None

    try:
        return get_user_from_token(token)
    except HTTPException:
        logger.debug("비로그인 요청: 잘못된 토큰")
        return None
