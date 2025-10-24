from openai import OpenAI
from app.config import settings
from app.models.emotion_log import EmotionLog

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def analyze_emotion(db, user_id: int, text: str):
    """
    감정 분석 + DB 저장
    """
    prompt = f"""
    문장: "{text}"
    위 문장의 감정을 분석하세요.
    가능한 감정: 긍정, 부정, 중립.
    JSON 형식으로 출력:
    {{
        "emotion": "<감정>",
        "reason": "<간단한 이유>"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        import json
        content = response.choices[0].message.content.strip()
        result = json.loads(content)

        log = EmotionLog(
            user_id=user_id,
            text=text,
            emotion=result.get("emotion", "중립"),
            reason=result.get("reason", "")
        )
        db.add(log)
        db.commit()

    except Exception as e:
        result = {"emotion": "분석 실패", "reason": str(e)}

    return result
