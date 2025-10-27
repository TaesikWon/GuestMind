# app/routes/rag.py
from fastapi import APIRouter, HTTPException
from app.services import rag_service

router = APIRouter(prefix="/rag", tags=["RAG"])

@router.post("/add")
def add_feedback(feedback_id: int, feedback_text: str):
    """피드백을 벡터DB에 추가"""
    success = rag_service.add_feedback_to_rag(feedback_id, feedback_text)
    if not success:
        raise HTTPException(status_code=500, detail="피드백 추가 실패")
    return {"message": "피드백이 RAG에 저장되었습니다."}

@router.get("/search")
def search_feedback(query: str, top_k: int = 3):
    """유사 피드백 검색"""
    results = rag_service.search_similar_feedback(query, top_k)
    return {"results": results}
