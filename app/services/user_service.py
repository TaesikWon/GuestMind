from sqlalchemy.orm import Session
from app.models.user import User
import bcrypt

def create_user(db: Session, username: str, password: str):
    # 이미 존재하는 유저 확인
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return None

    # 비밀번호 해싱
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, hashed_password=hashed_pw.decode('utf-8'))

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    if not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        return None

    return user
