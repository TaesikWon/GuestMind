# app/api/chat_api.py
import logging
from app.services.emotion_service import EmotionService
from app.services.rag_service import RAGService
from app.services.response_generator import ResponseGenerator

logger = logging.getLogger("soulstay.chat_api")


class ChatAPI:
    """감정 분석 + RAG + GPT 응답을 통합 처리하는 챗봇 API"""

    def __init__(self):
        self.emotion = EmotionService()
        self.rag = RAGService()
        self.response = ResponseGenerator()

    def process_message(self, text: str) -> dict:
        """사용자 입력을 분석하고 응답 생성"""
        if not text or not text.strip():
            return {
                "emotion": "none",
                "similar_cases": [],
                "response": "메시지를 입력해주세요 😊"
            }

        try:
            # 1️⃣ 감정 분석
            emotion_result = self.emotion.analyze(text)
            
            # ✅ 결과가 dict인지 str인지 확인
            if isinstance(emotion_result, dict):
                emotion = emotion_result.get("emotion", "중립")
            else:
                emotion = emotion_result  # 문자열인 경우

            # 2️⃣ 유사 피드백 검색 (RAG)
            similar_cases = self.rag.search_similar_feedback(text, top_k=3)

            # 3️⃣ 응답 생성 (GPT or 기본 규칙)
            reply = self.response.compose(text, emotion, similar_cases)

            logger.info(f"CHAT: 응답 생성 완료 — 감정={emotion}, 유사사례={len(similar_cases)}")
            return {
                "emotion": emotion,
                "similar_cases": similar_cases,
                "response": reply,
            }

        except Exception as e:
            logger.exception(f"❌ ChatAPI 처리 중 오류: {e}")
            return {
                "emotion": "error",
                "similar_cases": [],
                "response": "⚠️ 대화를 처리하는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
            }