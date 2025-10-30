from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/chatbot", tags=["Chatbot UI"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def chatbot_page(request: Request):
    """챗봇 UI 페이지 렌더링"""
    return templates.TemplateResponse("chat.html", {"request": request})
