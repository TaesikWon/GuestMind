from sqlalchemy import Column, Integer, Float, Date, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class DailySummary(Base):
    __tablename__ = "daily_summaries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    date = Column(Date, nullable=False, index=True)

    # ✅ 하루 감정 통계
    total_feedback = Column(Integer, nullable=False, default=0)
    positive_ratio = Column(Float, nullable=False, default=0.0)
    negative_ratio = Column(Float, nullable=False, default=0.0)
    neutral_ratio = Column(Float, nullable=False, default=0.0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ✅ 관계 설정
    user = relationship("User", back_populates="daily_summaries")

    # ✅ 날짜별 중복 방지 (사용자별 1일 1요약)
    __table_args__ = (
        UniqueConstraint("user_id", "date", name="uq_user_date_summary"),
    )

    def __repr__(self):
        return (
            f"<DailySummary(date={self.date}, total={self.total_feedback}, "
            f"pos={self.positive_ratio:.2f}, neg={self.negative_ratio:.2f}, neu={self.neutral_ratio:.2f})>"
        )
