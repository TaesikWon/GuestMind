from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base   # ✅ 여기 수정!

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # User ↔ EmotionLog 관계
    logs = relationship("EmotionLog", back_populates="user")
