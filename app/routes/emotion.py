from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.emotion_service import analyze_emotion
from app.routes.auth import get_current_user  # ← 맨 위로
from app.models.user import User  # ← 맨 위로

router = APIRouter(prefix="/emotion", tags=["Emotion Analysis"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def render_emotion_page(request: Request):
    return templates.TemplateResponse("emotion.html", {"request": request, "result": None, "text": ""})


@router.post("/analyze", response_class=HTMLResponse)
def handle_emotion_analysis(
    request: Request, 
    text: str = Form(...), 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not text.strip():
        return templates.TemplateResponse(
            "emotion.html",
            {"request": request, "result": {"emotion": "⚠️ 텍스트를 입력하세요.", "reason": ""}, "text": text, "current_user": current_user}
        )
    
    result = analyze_emotion(db=db, user_id=current_user.id, text=text)
    return templates.TemplateResponse("emotion.html", {
        "request": request, 
        "result": result, 
        "text": text,
        "current_user": current_user
    })