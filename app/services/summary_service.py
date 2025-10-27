from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.emotion_log import EmotionLog
from app.models.daily_summary import DailySummary

def update_daily_summary(db: Session):
    """하루 동안의 감정 비율 요약"""
    today = datetime.utcnow().date()
    logs = db.query(EmotionLog).filter(EmotionLog.created_at >= today - timedelta(days=1)).all()

    if not logs:
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
    return total
