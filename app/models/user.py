# app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, func, event, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)

    # ✅ 추가: 권한/활성 상태 필드
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ✅ 관계 (예: 일일 요약 / 감정 로그)
    daily_summaries = relationship("DailySummary", back_populates="user", cascade="all, delete")
    # emotion_logs = relationship("EmotionLog", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}', active={self.is_active})>"


# ✅ 이메일 자동 소문자 변환 (회원가입 시 대소문자 문제 방지)
@event.listens_for(User, "before_insert")
def normalize_email_before_insert(mapper, connection, target):
    if target.email:
        target.email = target.email.strip().lower()


@event.listens_for(User, "before_update")
def normalize_email_before_update(mapper, connection, target):
    if target.email:
        target.email = target.email.strip().lower()
