# app/services/user_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from passlib.context import CryptContext
from app.utils.logger import logger  # ✅ 중앙 로거 사용

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ 비밀번호 해싱
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ✅ 비밀번호 검증
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ✅ 회원가입
def create_user(db: Session, username: str, password: str):
    if not username or not password:
        logger.warning("USER: Signup failed — Missing username or password")
        raise HTTPException(status_code=400, detail="Username and password required")

    if len(username) < 3 or len(password) < 6:
        logger.warning(f"USER: Signup failed — username/password too short ({username})")
        raise HTTPException(status_code=400, detail="Username ≥3, password ≥6 chars")

    try:
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            logger.warning(f"USER: Signup failed — username '{username}' already exists")
            raise HTTPException(status_code=400, detail="Username already exists")

        new_user = User(username=username, password_hash=hash_password(password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"USER: New user created — {username}")
        return new_user

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.exception(f"USER: Database error while creating '{username}' — {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# ✅ 로그인 시 사용자 인증
def authenticate_user(db: Session, username: str, password: str):
    if not username or not password:
        logger.warning("USER: Login failed — Missing username or password")
        raise HTTPException(status_code=400, detail="Username and password required")

    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            logger.warning(f"USER: Login failed — user '{username}' not found")
            raise HTTPException(status_code=401, detail="Invalid username or password")

        if not verify_password(password, user.password_hash):
            logger.warning(f"USER: Login failed — wrong password for '{username}'")
            raise HTTPException(status_code=401, detail="Invalid username or password")

        logger.info(f"USER: '{username}' authenticated successfully")
        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"USER: Unexpected login error for '{username}' — {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
