# app/services/user_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from passlib.context import CryptContext
from app.utils.logger import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ 비밀번호 해싱
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ✅ 비밀번호 검증
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ✅ 회원가입
def create_user(db: Session, username: str, password: str):
    """새로운 사용자 생성"""
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    if len(username) < 3 or len(password) < 6:
        raise HTTPException(status_code=400, detail="Username ≥3, password ≥6 chars")

    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        logger.warning(f"USER: '{username}' already exists.")
        raise HTTPException(status_code=400, detail="Username already exists")

    try:
        new_user = User(username=username, password_hash=hash_password(password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"USER: Created new account — {username}")
        return new_user

    except Exception as e:
        db.rollback()
        logger.exception(f"USER: DB error while creating '{username}' — {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# ✅ 로그인 인증
def authenticate_user(db: Session, username: str, password: str):
    """사용자 로그인 인증"""
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    try:
        user = db.query(User).filter(User.username == username).first()

        # 🔒 보안상 구체적인 이유 노출 안 함
        if not user or not verify_password(password, user.password_hash):
            logger.warning(f"USER: Login failed for '{username}' (invalid credentials)")
            raise HTTPException(status_code=401, detail="Invalid username or password")

        logger.info(f"USER: Login success — {username}")
        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"USER: Unexpected error on login — {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
