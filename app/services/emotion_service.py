import logging
from transformers import pipeline
from app.services.local_emotion_model import analyze_emotion_local

logger = logging.getLogger("soulstay.emotion")

# 모델 1회만 로드
_model = pipeline(
    "sentiment-analysis",
    model="WhitePeak/bert-base-cased-Korean-sentiment",
    device=-1
)

class EmotionService:
    """Hugging Face BERT 기반 감정 분석 서비스"""

    def analyze(self, text: str) -> str:
        try:
            result = _model(text)[0]
            label = result["label"].lower()
            if "pos" in label:
                return "positive"
            elif "neg" in label:
                return "negative"
            return "neutral"
        except Exception:
            logger.exception("❌ 감정 분석 오류")
            return "error"


def analyze_emotion(db, user_id, text: str):
    """로컬 모델 기반 감정 분석 (백업용)"""
    try:
        result = analyze_emotion_local(text)
        logger.info(f"🧠 로컬 모델 감정 분석 완료: {result}")
        return result
    except Exception as e:
        logger.exception("❌ 로컬 감정 분석 오류")
        return {"emotion": "error", "reason": str(e)}
