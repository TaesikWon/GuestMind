# app/services/response_service_kobart.py
import torch
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

class KoBARTResponseGenerator:
    """한국어 문맥형 답변 생성기 (KoBART 기반)"""

    def __init__(self, model_name="gogamza/kobart-base-v2"):
        print("🔄 KoBART 모델 로드 중...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name)
        self.model = BartForConditionalGeneration.from_pretrained(model_name).to(self.device)
        print(f"✅ KoBART 로드 완료 ({self.device})")

    def compose(self, text, emotion, cases=None):
        """감정 + 유사사례 기반 응답 생성"""
        context = ""
        if cases:
            context = " ".join([c["text"] for c in cases[:3]])
        prompt = self._build_prompt(text, emotion, context)
        return self._generate_response(prompt)

    def _build_prompt(self, text, emotion, context):
        tone = {
            "positive": "감사한 마음으로 답변하세요.",
            "negative": "사과와 공감이 담긴 답변을 하세요.",
            "neutral": "공손하고 객관적인 어조로 답변하세요."
        }.get(emotion, "공손하게 답변하세요.")

        prompt = (
            f"고객 피드백: {text}\n"
            f"유사 피드백 참고: {context}\n"
            f"답변 지침: {tone}\n"
            f"AI 응답:"
        )
        return prompt

    def _generate_response(self, prompt):
        """KoBART를 이용해 답변 문장 생성"""
        inputs = self.tokenizer([prompt], return_tensors="pt", truncation=True).to(self.device)
        output_ids = self.model.generate(
            **inputs,
            max_length=150,
            num_beams=4,
            repetition_penalty=2.0,
            no_repeat_ngram_size=3,
            early_stopping=True,
        )
        response = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return response.strip()
