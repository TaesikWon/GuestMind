from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app.services.emotion_service import analyze_emotion
from app.models.user import User
from app.core.auth_utils import get_current_user_optional


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/emotion", tags=["Emotion Analysis"])
templates = Jinja2Templates(directory="app/templates")


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
    current_user: User = Depends(get_current_user_optional)  # ← None 가능
):
    """감정 분석 실행 (로그인 선택사항)"""
    
    if not text.strip():
        return templates.TemplateResponse("emotion.html", {
            "request": request,
            "result": {"emotion": "⚠️ 텍스트를 입력하세요.", "reason": ""},
            "text": text
        })
    
    if len(text) > 1000:
        return templates.TemplateResponse("emotion.html", {
            "request": request,
            "result": {"emotion": "⚠️ 최대 1000자", "reason": ""},
            "text": text[:1000]
        })
    
    try:
        # 로그인했으면 user_id 저장, 아니면 None
        user_id = current_user.id if current_user else None
        result = analyze_emotion(db=db, user_id=user_id, text=text)
        
        logger.info(f"분석 완료 (user_id={user_id})")
        
        return templates.TemplateResponse("emotion.html", {
            "request": request,
            "result": result,
            "text": text
        })
        
    except Exception as e:
        logger.error(f"분석 실패: {e}")
        db.rollback()
        
        return templates.TemplateResponse("emotion.html", {
            "request": request,
            "result": {"emotion": "❌ 분석 실패", "reason": "서버 오류"},
            "text": text
        }, status_code=500)