from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.api.chat_api import ChatAPI

router = APIRouter(tags=["Chatbot"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/chat")
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    service = ChatAPI()
    result = service.process_message(request.message)
    return result
