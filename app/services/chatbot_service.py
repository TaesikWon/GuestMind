# app/services/chatbot_service.py
from app.services.rag_service import RAGService
from app.services.emotion_analyzer import analyze_emotion_local
import logging

logger = logging.getLogger("soulstay.chatbot")

rag = RAGService()

def chatbot_response(user_text: str) -> str:
    """감정 분석 + RAG 검색 기반 응답 생성"""
    if not user_text or not user_text.strip():
        return "메시지를 입력해주세요 😊"

    try:
        # 1️⃣ 감정 분석
        emotion_result = analyze_emotion_local(user_text)
        emotion = emotion_result.get("emotion", "중립")

        # 2️⃣ 유사 피드백 검색
        related_docs = rag.search_similar_feedback(user_text, top_k=3)
        context_texts = []
        if related_docs:
            seen = set()
            for doc in related_docs:
                text = doc.get("text", "")
                if text not in seen and text:
                    context_texts.append(text.strip())
                    seen.add(text)

        # 3️⃣ 기본 응답 생성
        tone_map = {
            "긍정": "감사합니다 😊 고객님의 좋은 의견이 큰 힘이 됩니다.",
            "부정": "불편을 드려 죄송합니다 🙏 개선을 위해 최선을 다하겠습니다.",
            "중립": "소중한 의견 감사합니다. 더 나은 서비스를 준비하겠습니다."
        }
        response = f"감정 분석 결과: **{emotion}**\n\n{tone_map.get(emotion, tone_map['중립'])}"

        # 4️⃣ 유사 의견 요약 첨부
        if context_texts:
            context_summary = " / ".join(context_texts[:3])
            response += f"\n\n📎 참고된 유사 피드백:\n{context_summary[:200]}..."

        logger.info(f"CHATBOT: 응답 생성 완료 ({emotion})")
        return response

    except Exception as e:
        logger.error(f"❌ 챗봇 응답 생성 오류: {e}")
        return "현재 응답을 생성할 수 없습니다. 잠시 후 다시 시도해주세요 🙏"
