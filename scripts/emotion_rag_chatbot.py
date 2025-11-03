# scripts/emotion_rag_chatbot.py

import torch

def detect_emotion(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = emotion_model(**inputs)
    pred = torch.argmax(outputs.logits, dim=1).item()
    labels = {0: "positive", 1: "negative", 2: "neutral"}
    return labels[pred]

def get_emotion_response(user_input: str):
    emotion = detect_emotion(user_input)

    if emotion == "positive":
        return f"😊 고객님, 좋은 말씀 감사합니다! 고객님의 만족이 저희의 가장 큰 보람입니다."
    elif emotion == "negative":
        return f"😔 불편을 드려 죄송합니다. 말씀해주신 부분은 즉시 개선하겠습니다."
    else:
        return f"🙂 소중한 의견 감사합니다. 고객님의 경험이 더욱 좋아질 수 있도록 노력하겠습니다."
