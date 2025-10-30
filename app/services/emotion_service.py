from app.services.local_emotion_model import analyze_emotion_local
import logging

logger = logging.getLogger("soulstay.emotion")

def analyze_emotion(db, user_id, text: str):
    """로컬 학습 모델을 사용한 감정 분석"""
    try:
        result = analyze_emotion_local(text)
        logger.info(f"🧠 로컬 모델 감정 분석 완료: {result}")
        return result
    except Exception as e:
        logger.exception("❌ 로컬 감정 분석 오류")
        return {"emotion": "오류", "reason": str(e)}
