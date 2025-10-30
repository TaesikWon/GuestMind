import logging
from transformers import pipeline
from app.services.local_emotion_model import analyze_emotion_local

logger = logging.getLogger("soulstay.emotion")

# 한 번만 모델 로드
_model = pipeline(
    "sentiment-analysis",
    model="WhitePeak/bert-base-cased-Korean-sentiment",
    device=-1
)

class EmotionService:
    def analyze(self, text: str):
        try:
            result = _model(text)[0]
            label = result["label"].lower()
            if "pos" in label:
                return "positive"
            elif "neg" in label:
                return "negative"
            return "neutral"
        except Exception as e:
            logger.exception("❌ 감정 분석 오류")
            return "error"

def analyze_emotion(db, user_id, text: str):
    """로컬 학습 모델 기반 감정 분석"""
    try:
        result = analyze_emotion_local(text)
        logger.info(f"🧠 로컬 모델 감정 분석 완료: {result}")
        return result
    except Exception as e:
        logger.exception("❌ 로컬 감정 분석 오류")
        return {"emotion": "오류", "reason": str(e)}
