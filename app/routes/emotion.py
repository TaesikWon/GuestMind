from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app.services.emotion_service import analyze_emotion
from app.models.user import User
from app.core.auth_utils import get_current_user_optional
from app.services.rag_service import RAGService   # ✅ 수정
from app.models.emotion_log import EmotionLog

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/emotion", tags=["Emotion Analysis"])
templates = Jinja2Templates(directory="app/templates")

rag_service = RAGService()   # ✅ 수정


@router.get("/", response_class=HTMLResponse)
def render_emotion_page(request: Request):
    """감정 분석 페이지"""
    return templates.TemplateResponse("emotion.html", {
        "request": request,
        "result": None,
        "text": ""
    })


@router.post("/analyze", response_class=HTMLResponse)
def handle_emotion_analysis(
    request: Request,
    text: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    """감정 분석 (회원 전용 + DB + RAG 트랜잭션)"""

    # ✅ 로그인 여부 확인
    if not current_user:
        return templates.TemplateResponse("emotion.html", {
            "request": request,
            "result": {
                "emotion": "⚠️ 로그인 필요",
                "reason": "감정 분석을 이용하려면 로그인해주세요."
            },
            "text": text
        })

    # ✅ 입력값 검증
    if not text.strip():
        return templates.TemplateResponse("emotion.html", {
            "request": request,
            "result": {"emotion": "⚠️ 텍스트를 입력하세요.", "reason": ""},
            "text": text
        })

    if len(text) > 1000:
        return templates.TemplateResponse("emotion.html", {
            "request": request,
            "result": {"emotion": "⚠️ 최대 1000자까지 입력 가능", "reason": ""},
            "text": text[:1000]
        })

    user_id = current_user.id
    db.begin()

    try:
        # 1️⃣ 감정 분석 (OpenAI)
        result = analyze_emotion(db=db, user_id=user_id, text=text)
        emotion = result.get("emotion")
        reason = result.get("reason")
        logger.info(f"감정 분석 완료 ✅ (user_id={user_id}, emotion={emotion})")

        # 2️⃣ 감정 로그 DB 저장
        log_entry = EmotionLog(user_id=user_id, text=text, emotion=emotion, reason=reason)
        db.add(log_entry)

        # 3️⃣ RAG 저장 (수정됨)
        rag_service.add_feedback_to_rag(user_id=user_id, feedback_text=text)
        logger.info(f"🟢 RAG 저장 완료 (user_id={user_id})")

        # ✅ 커밋
        db.commit()
        logger.info(f"🟢 DB + RAG 트랜잭션 커밋 완료 (user_id={user_id})")

        return templates.TemplateResponse("emotion.html", {
            "request": request,
            "result": result,
            "text": text
        })

    except Exception as e:
        db.rollback()
        logger.exception(f"❌ 트랜잭션 실패: {e}")
        return templates.TemplateResponse("emotion.html", {
            "request": request,
            "result": {"emotion": "❌ 처리 실패", "reason": "서버 내부 오류"},
            "text": text
        }, status_code=500)

    finally:
        db.close()