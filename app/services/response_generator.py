import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

# ✅ .env 파일 강제 로드 (경로 명시)
env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path=env_path)

logger = logging.getLogger("soulstay.response")

try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing")

    # ✅ 새로운 OpenAI 클라이언트 초기화 방식
    client = OpenAI(api_key=api_key)
    logger.info("✅ OpenAI 클라이언트 초기화 성공")

except Exception as e:
    client = None
    logger.warning(f"⚠️ OpenAI 클라이언트 초기화 실패. GPT 응답 기능 비활성화됨. ({e})")


class ResponseGenerator:
    """응답 생성기 (GPT 활용)"""

    def __init__(self):
        self.client = client

    def compose(self, text, emotion, cases):
        """감정 + 유사 사례 기반 응답 생성"""
        if self.client:
            try:
                return self._generate_with_gpt(text, emotion, cases)
            except Exception as e:
                logger.warning(f"⚠️ GPT 응답 생성 실패, 기본 응답 사용: {e}")
        
        return self._base_response(emotion)

    def _generate_with_gpt(self, text, emotion, cases):
        """GPT로 유사 사례를 참고하여 맥락 있는 답변 생성"""
        
        # 유사 사례 컨텍스트 구성
        context = ""
        if cases and len(cases) > 0:
            context = "\n\n참고할 유사한 고객 피드백:\n"
            for i, case in enumerate(cases[:3], 1):
                context += f"{i}. {case['text']}\n"
        
        # 감정에 따른 시스템 프롬프트
        system_prompt = """당신은 SoulStay 호텔의 친절하고 전문적인 고객 상담 담당자입니다.
고객의 감정에 공감하며 진정성 있게 답변하세요.

답변 가이드:
- 긍정적 피드백: 감사 표현과 함께 앞으로도 최선을 다하겠다는 다짐
- 부정적 피드백: 진심 어린 사과와 구체적인 개선 의지 표현
- 중립적 피드백: 의견에 대한 감사와 경청하는 태도

유사한 과거 피드백이 제공되면, 해당 내용을 참고하여 더 구체적이고 맥락 있는 답변을 작성하세요.
답변은 2-3문장으로 간결하고 따뜻하게 작성해주세요."""

        user_prompt = f"""고객 피드백: "{text}"
감정 분석 결과: {emotion}
{context}

위 고객의 피드백에 대해 공감적이고 전문적인 답변을 작성해주세요."""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()

    def _base_response(self, emotion):
        """GPT 사용 불가 시 기본 응답"""
        responses = {
            "positive": "소중한 의견 감사드립니다. 앞으로도 더 나은 서비스로 보답하겠습니다.",
            "negative": "불편을 드려 정말 죄송합니다. 고객님의 의견을 바탕으로 개선하도록 노력하겠습니다.",
            "neutral": "의견 주셔서 감사합니다. 서비스 향상에 참고하겠습니다.",
        }
        return responses.get(emotion, "피드백 감사드립니다.")