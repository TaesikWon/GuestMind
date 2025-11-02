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
    """응답 생성기 (GPT 후처리 포함)"""

    def __init__(self):
        self.client = client

    def compose(self, text, emotion, cases):
        """감정 + 유사 사례 기반 응답 생성"""
        base_text = self._base_response(text, emotion, cases)
        
        # GPT로 문체만 다듬기
        if self.client:
            try:
                refined = self._refine_with_gpt(base_text)
                return refined
            except Exception as e:
                logger.warning(f"⚠️ GPT 후처리 실패, 기본 응답 사용: {e}")
        
        return base_text

    def _base_response(self, text, emotion, cases):
        """규칙 기반 기본 응답 생성"""
        # 감정에 따른 기본 톤
        if emotion == "positive":
            tone = "소중한 의견 감사드립니다. 고객님께서 만족하셨다니 저희에게 큰 기쁨입니다."
        elif emotion == "negative":
            tone = "불편을 드려 정말 죄송합니다. 고객님의 의견을 진지하게 받아들이고 개선하도록 노력하겠습니다."
        else:
            tone = "의견 주셔서 감사합니다. 고객님의 피드백은 저희에게 소중한 자산입니다."
        
        # 유사 사례가 있으면 참고만 (절대 그대로 붙이지 않음)
        if cases:
            tone += " 유사한 고객 사례를 참고하여 더 나은 서비스를 제공하도록 하겠습니다."
        
        return tone

    def _refine_with_gpt(self, text: str):
        """GPT로 문체만 자연스럽게 다듬기"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 문체 교정 전문가입니다. 주어진 답변의 의미는 그대로 유지하되, 더 자연스럽고 따뜻한 문체로 다듬어주세요. 내용을 추가하거나 변경하지 말고 문체만 개선하세요."
                },
                {"role": "user", "content": text},
            ],
            temperature=0.3,  # 낮게 설정 (창의성보다 정확성)
            max_tokens=150
        )
        return response.choices[0].message.content.strip()