from app.services.rag_service import RAGService
from app.services.emotion_service import analyze_emotion_local

rag = RAGService()

def chatbot_response(user_text: str):
    emotion = analyze_emotion_local(user_text)["emotion"]
    related_docs = rag.search_similar_feedback(user_text, top_k=3)
    
    context = " ".join([doc["text"] for doc in related_docs])
    response = f"감정: {emotion}\n\n"
    
    if emotion == "긍정":
        response += "감사합니다 😊 고객님의 좋은 의견을 반영하겠습니다."
    elif emotion == "부정":
        response += "죄송합니다 🙏 불편하셨던 점을 개선하겠습니다."
    else:
        response += "소중한 의견 감사합니다. 더 나은 서비스를 준비하겠습니다."
    
    if context:
        response += f"\n\n📎 관련 의견 요약: {context[:200]}..."
    
    return response
