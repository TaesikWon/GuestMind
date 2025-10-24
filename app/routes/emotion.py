from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.emotion_service import analyze_emotion

router = APIRouter(prefix="/emotion", tags=["Emotion Analysis"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def render_emotion_page(request: Request):
    return templates.TemplateResponse("emotion.html", {"request": request, "result": None, "text": ""})


@router.post("/analyze", response_class=HTMLResponse)
def handle_emotion_analysis(request: Request, text: str = Form(...), db: Session = Depends(get_db)):
    if not text.strip():
        return templates.TemplateResponse(
            "emotion.html",
            {"request": request, "result": {"emotion": "⚠️ 텍스트를 입력하세요.", "reason": ""}, "text": text}
        )

    result = analyze_emotion(db=db, user_id=1, text=text)  # 임시 user_id
    return templates.TemplateResponse("emotion.html", {"request": request, "result": result, "text": text})
