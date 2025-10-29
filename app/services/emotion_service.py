# app/services/emotion_service.py
from openai import OpenAI, OpenAIError
from sqlalchemy.orm import Session
from app.models.emotion_log import EmotionLog
from app.services.rag_service import RAGService
from app.config import settings
import json, logging

client = OpenAI(api_key=settings.openai_api_key)
rag_service = RAGService()
logger = logging.getLogger("soulstay.emotion")


def analyze_emotion(db: Session, user_id: int, text: str):
    """
    고객 피드백 감정을 분석하고, DB 및 RAG에 저장.
    - 트랜잭션은 FastAPI 세션 범위 내에서 처리됨
    - 하나라도 실패하면 전체 롤백
    """
    try:
        # --- 1️⃣ OpenAI 감정 분석 ---
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "고객 피드백의 감정을 분석하고 JSON 형식으로만 답변하세요. (예: {\"emotion\": \"긍정\", \"reason\": \"서비스가 만족스러움\"})"},
                {"role": "user", "content": f'문장: "{text}"'}
            ],
            temperature=0.3,
        )

        analysis = response.choices[0].message.content.strip()
        logger.info(f"GPT 응답: {analysis}")

        # --- 2️⃣ JSON 파싱 ---
        try:
            parsed = json.loads(analysis)
            emotion = parsed.get("emotion") or parsed.get("감정") or "중립"
            reason = parsed.get("reason") or parsed.get("이유") or "분석 완료"
        except json.JSONDecodeError:
            emotion = "중립"
            reason = "GPT 응답 파싱 실패"

        # --- 3️⃣ 감정 로그 저장 ---
        log = EmotionLog(user_id=user_id, text=text, emotion=emotion, reason=reason)
        db.add(log)

        # --- 4️⃣ RAG 저장 ---
        rag_service.add_document(
            text=text,
            metadata={"user_id": user_id, "emotion": emotion, "reason": reason}
        )

        # --- 5️⃣ 커밋 ---
        db.commit()
        logger.info(f"✅ 감정 분석 + RAG 저장 완료 | user_id={user_id}")

        return {"emotion": emotion, "reason": reason}

    except OpenAIError as e:
        db.rollback()
        logger.error(f"❌ OpenAI 오류: {e}")
        return {"emotion": "오류", "reason": "OpenAI 호출 실패"}

    except Exception as e:
        db.rollback()
        logger.exception(f"❌ 감정 분석 중 오류 발생: {e}")
        return {"emotion": "오류", "reason": "서버 내부 오류"}

    finally:
        db.close()
