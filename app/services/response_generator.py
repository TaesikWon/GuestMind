# app/services/response_generator.py
import os
import openai
import logging

logger = logging.getLogger("soulstay.response")

openai.api_key = os.getenv("OPENAI_API_KEY")

class ResponseGenerator:
    def __init__(self, use_gpt: bool = True):
        """응답 생성기 (GPT 후처리 옵션 포함)"""
        self.use_gpt = use_gpt
        if not openai.api_key:
            logger.warning("⚠️ OPENAI_API_KEY가 없습니다. GPT 후처리를 비활성화합니다.")
            self.use_gpt = False

    def compose(self, text, emotion, cases):
        """감정 + 유사 사례 기반 응답 생성"""
        base_text = self._base_response(text, emotion, cases)

        if self.use_gpt:
            try:
                refined = self._refine_with_gpt(base_text)
                return refined
            except Exception as e:
                logger.warning(f"⚠️ GPT 후처리 실패, 기본 응답으로 대체: {e}")
                return base_text

        return base_text

    def _base_response(self, text, emotion, cases):
        """기본 응답 구성"""
        tone = {
            "positive": "진심으로 감사드립니다. 고객님의 소중한 의견은 큰 힘이 됩니다. ",
            "negative": "불편을 드려 정말 죄송합니다. 더 나은 서비스를 위해 개선하겠습니다. ",
            "neutral": "의견을 남겨주셔서 감사합니다. 참고하여 서비스 품질을 높이겠습니다. ",
        }.get(emotion, "의견을 남겨주셔서 감사합니다. ")

        if cases and isinstance(cases, list) and "text" in cases[0]:
            summary = f"유사한 사례로 '{cases[0]['text']}' 이(가) 있었습니다."
        else:
            summary = "유사한 고객 사례는 아직 없습니다."

        return tone + summary

    def _refine_with_gpt(self, text: str):
        """OpenAI GPT 모델로 문체 후처리"""
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "당신은 호텔 고객 경험 담당자입니다. "
                        "고객에게 공손하고 따뜻한 어조로 답변하세요. "
                        "감정에 공감하는 한 문장으로 마무리해주세요."
                    ),
                },
                {"role": "user", "content": text},
            ],
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
