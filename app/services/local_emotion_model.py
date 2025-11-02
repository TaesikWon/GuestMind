# app/services/emotion_analyzer.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import logging

logger = logging.getLogger("soulstay.emotion")

# ✅ 모델 경로 및 라벨 정의
MODEL_PATH = "WhitePeak/bert-base-cased-Korean-sentiment"
LABELS = ["부정", "중립", "긍정"]

# ✅ 모델 & 토크나이저 로드 (CPU 전용)
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()
    logger.info(f"✅ 감정 분석 모델 로드 완료 ({MODEL_PATH}, CPU 모드)")
except Exception as e:
    logger.error(f"❌ 감정 분석 모델 로드 실패: {e}")
    tokenizer, model = None, None


def analyze_emotion_local(text: str):
    """
    한국어 감정 분석 (CPU 전용)
    Args:
        text (str): 분석할 문장
    Returns:
        dict: {"emotion": 감정라벨, "reason": 분석결과설명}
    """
    if not text or not text.strip():
        logger.warning("⚠️ 감정 분석 실패 — 입력이 비어 있음")
        return {"emotion": "중립", "reason": "입력이 비어있습니다."}

    if model is None or tokenizer is None:
        return {"emotion": "중립", "reason": "모델이 로드되지 않았습니다."}

    try:
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )

        with torch.no_grad():
            outputs = model(**inputs)
            pred = torch.argmax(outputs.logits, dim=1).item()
            emotion = LABELS[pred]

        logger.info(f"🧠 감정 분석 결과: '{text[:30]}...' → {emotion}")
        return {"emotion": emotion, "reason": f"Hugging Face 모델({MODEL_PATH}) 예측 결과"}

    except Exception as e:
        logger.error(f"❌ 감정 분석 오류: {e}")
        return {"emotion": "중립", "reason": f"분석 중 오류 발생: {e}"}
