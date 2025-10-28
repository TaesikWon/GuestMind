from sqlalchemy import Column, Integer, Float, Date, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class DailySummary(Base):
    __tablename__ = "daily_summaries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    date = Column(Date, nullable=False, index=True)

    # 하루 동안의 감정 통계
    total_feedback = Column(Integer, nullable=False)
    positive_ratio = Column(Float, nullable=False)
    negative_ratio = Column(Float, nullable=False)
    neutral_ratio = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    user = relationship("User", back_populates="daily_summaries")

    def __repr__(self):
        return (
            f"<DailySummary date={self.date} total={self.total_feedback} "
            f"pos={self.positive_ratio:.2f} neg={self.negative_ratio:.2f} neu={self.neutral_ratio:.2f}>"
        )
