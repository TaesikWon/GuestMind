from openai import OpenAI
from sqlalchemy.orm import Session
from app.models.emotion_log import EmotionLog
from app.config import settings
import datetime

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def analyze_emotion(db: Session, user_id: int, text: str):
    """
    고객 피드백 텍스트를 OpenAI 감정 분석 API로 분석하고 DB에 저장.
    """
    try:
        # ✅ 감정 분석 요청
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 고객 피드백의 감정을 분석하는 AI입니다."},
                {"role": "user", "content": f"문장 '{text}'의 감정을 긍정, 부정, 중립 중 하나로 분류하고 이유를 간단히 설명해 주세요."},
            ],
        )

        analysis = response.choices[0].message.content.strip()

        # ✅ DB 저장 (emotion / reason 필드 사용)
        log = EmotionLog(
            user_id=user_id,
            text=text,
            emotion=analysis,       # 감정 결과 (텍스트로)
            reason="자동 분석 결과",
        )
        db.add(log)
        db.commit()

        return {"emotion": analysis, "reason": "성공"}

    except Exception as e:
        print(f"[Emotion] ❌ 분석 실패: {e}")
        return {"emotion": "분석 실패", "reason": str(e)}
