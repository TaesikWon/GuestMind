from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.emotion_log import EmotionLog
from app.models.daily_summary import DailySummary
from app.utils.logger import logger

def update_daily_summary(db: Session) -> int:
    """
    하루 동안의 감정 로그 비율 요약 생성
    - 중복 요약 방지
    - 로그 없을 때 0값으로 저장
    - 정상 처리 시: 총 처리된 감정 로그 수 반환
    - 오류 발생 시: 0 반환
    """
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)

    try:
        logger.info(f"📊 SUMMARY: {yesterday} 기준 감정 로그 요약 시작")

        # ✅ 이미 요약된 날짜면 건너뜀
        existing = db.query(DailySummary).filter(DailySummary.date == yesterday).first()
        if existing:
            logger.info(f"ℹ️ SUMMARY: {yesterday} 요약 이미 존재 — 건너뜀")
            return 0

        # ✅ 어제 날짜 기준 감정 로그 조회
        logs = db.query(EmotionLog).filter(
            EmotionLog.created_at >= yesterday,
            EmotionLog.created_at < today
        ).all()

        total = len(logs)
        positives = sum(1 for l in logs if l.emotion == "긍정")
        negatives = sum(1 for l in logs if l.emotion == "부정")
        neutrals = sum(1 for l in logs if l.emotion == "중립")

        # ✅ 로그 없을 때도 기록 (데이터 일관성 유지)
        summary = DailySummary(
            date=yesterday,
            total_feedback=total,
            positive_ratio=(positives / total) if total > 0 else 0,
            negative_ratio=(negatives / total) if total > 0 else 0,
            neutral_ratio=(neutrals / total) if total > 0 else 0,
        )

        db.add(summary)
        db.commit()

        logger.info(
            f"✅ SUMMARY 완료 — 날짜:{yesterday} | 총:{total} | 긍정:{positives}, 부정:{negatives}, 중립:{neutrals}"
        )
        return total

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"❌ SUMMARY: DB 오류 — {e}")
        return 0

    except Exception as e:
        db.rollback()
        logger.exception(f"❌ SUMMARY: 예외 발생 — {e}")
        return 0
