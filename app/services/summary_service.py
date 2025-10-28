from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.emotion_log import EmotionLog
from app.models.daily_summary import DailySummary
from app.utils.logger import logger

def update_daily_summary(db: Session) -> int:
    """
    하루 동안의 감정 로그 비율 요약 생성
    - 정상 처리 시: 총 처리된 감정 로그 수 반환
    - 오류 발생 시: 0 반환
    """
    today = datetime.utcnow().date()
    try:
        logger.info(f"SUMMARY: Starting daily summary update for {today}")

        logs = db.query(EmotionLog).filter(
            EmotionLog.created_at >= today - timedelta(days=1)
        ).all()

        if not logs:
            logger.info("SUMMARY: No emotion logs found for the day — skipping summary.")
            return 0

        total = len(logs)
        positives = sum(1 for l in logs if l.emotion == "positive")
        negatives = sum(1 for l in logs if l.emotion == "negative")
        neutrals = sum(1 for l in logs if l.emotion == "neutral")

        summary = DailySummary(
            date=today,
            total_feedback=total,
            positive_ratio=positives / total,
            negative_ratio=negatives / total,
            neutral_ratio=neutrals / total
        )

        db.add(summary)
        db.commit()

        logger.info(
            f"SUMMARY: ✅ Daily summary created — total={total}, "
            f"pos={positives}, neg={negatives}, neu={neutrals}"
        )
        logger.debug(f"SUMMARY: Ratios — +{positives/total:.2f}, -{negatives/total:.2f}, ={neutrals/total:.2f}")

        return total

    except Exception as e:
        db.rollback()
        logger.exception(f"SUMMARY: ❌ Error updating daily summary — {e}")
        return 0
