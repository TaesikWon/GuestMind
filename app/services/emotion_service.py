from openai import OpenAI
from sqlalchemy.orm import Session
from app.models.emotion_log import EmotionLog
from app.config import settings
import json
import logging

client = OpenAI(api_key=settings.OPENAI_API_KEY)
logger = logging.getLogger(__name__)

def analyze_emotion(db: Session, user_id: int, text: str):
    """
    고객 피드백 텍스트를 OpenAI 감정 분석 API로 분석하고 DB에 저장.
    """
    try:
        # ✅ JSON 형식 강제 프롬프트
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "당신은 고객 피드백의 감정을 분석하는 AI입니다. 반드시 JSON 형식으로만 답변하세요."
                },
                {
                    "role": "user", 
                    "content": f"""다음 문장의 감정을 분석하고, 아래 JSON 형식으로만 답변하세요:
{{
  "emotion": "긍정" 또는 "부정" 또는 "중립",
  "reason": "감정 판단 이유를 한 문장으로"
}}

문장: "{text}"
"""
                },
            ],
            temperature=0.3,  # 일관성 있는 답변을 위해 낮게 설정
        )

        analysis = response.choices[0].message.content.strip()
        logger.info(f"GPT 원본 응답: {analysis}")

        # ✅ JSON 파싱
        try:
            parsed = json.loads(analysis)
            emotion = parsed.get("emotion", "중립")
            reason = parsed.get("reason", "분석 완료")
            
            # ✅ 감정 검증 (긍정/부정/중립만 허용)
            if emotion not in ["긍정", "부정", "중립"]:
                logger.warning(f"예상치 못한 감정값: {emotion}, 중립로 설정")
                emotion = "중립"
                
        except json.JSONDecodeError as e:
            # ✅ JSON 파싱 실패 시 폴백
            logger.error(f"JSON 파싱 실패: {e}, 원본: {analysis}")
            
            # 간단한 키워드 기반 폴백
            if "긍정" in analysis:
                emotion = "긍정"
            elif "부정" in analysis:
                emotion = "부정"
            else:
                emotion = "중립"
            reason = analysis[:100]  # 원본 응답 일부만 저장

        # ✅ DB 저장
        log = EmotionLog(
            user_id=user_id,
            text=text,
            emotion=emotion,
            reason=reason,
        )
        db.add(log)
        db.commit()
        db.refresh(log)

        logger.info(f"감정 분석 저장 완료: user_id={user_id}, emotion={emotion}")
        return {"emotion": emotion, "reason": reason}

    except Exception as e:
        logger.error(f"감정 분석 실패: {e}")
        db.rollback()
        return {"emotion": "❌ 오류 발생", "reason": str(e)}