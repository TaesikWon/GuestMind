from app.services.emotion_service import EmotionService
from app.services.rag_service import RAGService
from app.services.response_generator import ResponseGenerator

class ChatAPI:
    def __init__(self):
        self.emotion = EmotionService()
        self.rag = RAGService()
        self.response = ResponseGenerator()

    def process_message(self, text: str):
        emotion = self.emotion.analyze(text)
        similar = self.rag.search(text, emotion)
        reply = self.response.compose(text, emotion, similar)
        return {
            "emotion": emotion,
            "similar_cases": similar,
            "response": reply
        }
