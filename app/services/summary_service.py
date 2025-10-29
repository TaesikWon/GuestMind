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
        logger.info(f"SUMMARY: 시작 — {today} 기준 감정 로그 요약 생성")

        logs = db.query(EmotionLog).filter(
            EmotionLog.created_at >= today - timedelta(days=1)
        ).all()

        if not logs:
            logger.info("SUMMARY: 감정 로그 없음 — 요약 건너뜀.")
            return 0

        total = len(logs)
        positives = sum(1 for l in logs if l.emotion == "긍정")
        negatives = sum(1 for l in logs if l.emotion == "부정")
        neutrals = sum(1 for l in logs if l.emotion == "중립")

        summary = DailySummary(
            date=today,
            total_feedback=total,
            positive_ratio=positives / total,
            negative_ratio=negatives / total,
            neutral_ratio=neutrals / total,
        )

        db.add(summary)
        db.commit()

        logger.info(
            f"SUMMARY: ✅ 요약 완료 — 총 {total}건 | 긍정:{positives} 부정:{negatives} 중립:{neutrals}"
        )
        return total

    except Exception as e:
        db.rollback()
        logger.exception(f"SUMMARY: ❌ 요약 생성 오류: {e}")
        return 0
