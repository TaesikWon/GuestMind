from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class EmotionLog(Base):
    __tablename__ = "emotion_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(String, nullable=False)         # 사용자가 입력한 문장
    emotion = Column(String, nullable=False)      # 감정 (긍정, 부정, 중립)
    reason = Column(String, nullable=True)        # 감정 분석 이유
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정 (User 테이블과 연결)
    user = relationship("User", back_populates="logs")
