from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# ✅ 한국어 감정분류 공개모델
MODEL_PATH = "WhitePeak/bert-base-cased-Korean-sentiment"
LABELS = ["부정", "중립", "긍정"]

# ✅ 토크나이저 / 모델 불러오기
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

def analyze_emotion_local(text: str):
    """허깅페이스 모델을 이용한 감정 분석"""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        pred = torch.argmax(outputs.logits, dim=1).item()
    emotion = LABELS[pred]
    return {"emotion": emotion, "reason": f"Hugging Face 모델({MODEL_PATH}) 예측 결과"}
