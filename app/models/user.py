from sqlalchemy import Column, Integer, String, DateTime, func, event
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    is_active = Column(Integer, default=1)  # 1=활성, 0=비활성
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"


# ✅ 이메일 자동 소문자 변환 (회원가입 시 대소문자 문제 방지)
@event.listens_for(User, "before_insert")
def normalize_email_before_insert(mapper, connection, target):
    if target.email:
        target.email = target.email.lower()


@event.listens_for(User, "before_update")
def normalize_email_before_update(mapper, connection, target):
    if target.email:
        target.email = target.email.lower()
