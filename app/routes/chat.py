from fastapi import APIRouter
from pydantic import BaseModel
from app.api.chat_api import ChatAPI

router = APIRouter(prefix="/chat", tags=["Chatbot"])

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def chat(request: ChatRequest):
    service = ChatAPI()
    result = service.process_message(request.message)
    return result
