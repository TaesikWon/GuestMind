import os
import logging
from openai import OpenAI
from dotenv import load_dotenv  # ✅ 추가

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
    """응답 생성기 (GPT 후처리 포함)"""

    def __init__(self):
        self.client = client

    def compose(self, text, emotion, cases):
        """감정 + 유사 사례 기반 응답 생성"""
        base_text = self._base_response(text, emotion, cases)
        if self.client:
            try:
                refined = self._refine_with_gpt(base_text)
                return refined
            except Exception as e:
                logger.warning(f"⚠️ GPT 후처리 실패, 기본 응답 사용: {e}")
        return base_text

    def _base_response(self, text, emotion, cases):
        tone = {
            "positive": "진심으로 감사드립니다. 고객님의 소중한 의견은 큰 힘이 됩니다. ",
            "negative": "불편을 드려 정말 죄송합니다. 더 나은 서비스를 위해 개선하겠습니다. ",
            "neutral": "의견을 남겨주셔서 감사합니다. 참고하여 서비스 품질을 높이겠습니다. ",
        }.get(emotion, "의견을 남겨주셔서 감사합니다. ")

        case_text = cases[0]["text"] if cases else "유사한 고객 사례는 아직 없습니다."
        return tone + f"참고 사례: {case_text}"

    def _refine_with_gpt(self, text: str):
        """GPT로 문체 후처리"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 호텔 고객센터 담당자입니다. 고객의 감정에 공감하며 따뜻하게 답변하세요."
                },
                {"role": "user", "content": text},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
