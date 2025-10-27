# app/routes/rag.py
from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.services import rag_service
from app.routes.auth import get_current_user
from app.models.user import User
from app.database import get_db

router = APIRouter(prefix="/rag", tags=["RAG"])

# ✅ Pydantic 모델 추가
class FeedbackAdd(BaseModel):
    feedback_id: int = Field(..., gt=0, description="피드백 ID (양수)")
    feedback_text: str = Field(..., min_length=1, max_length=1000, description="피드백 내용")

class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="검색 쿼리")
    top_k: int = Field(default=3, ge=1, le=10, description="결과 개수 (1-10)")

@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_feedback(
    request: FeedbackAdd = Body(...),
    current_user: User = Depends(get_current_user),  # ← 인증 추가
    db: Session = Depends(get_db)
):
    """
    피드백을 벡터DB에 추가 (로그인 필요)
    """
    success = rag_service.add_feedback_to_rag(
        feedback_id=request.feedback_id, 
        feedback_text=request.feedback_text
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="피드백 추가 실패"
        )
    
    return {
        "message": "피드백이 RAG에 저장되었습니다.",
        "feedback_id": request.feedback_id,
        "user_id": current_user.id
    }

@router.post("/search")
def search_feedback(
    request: SearchQuery = Body(...),
    current_user: User = Depends(get_current_user)  # ← 인증 추가
):
    """
    유사 피드백 검색 (로그인 필요)
    """
    if request.query.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="검색어를 입력하세요"
        )
    
    results = rag_service.search_similar_feedback(
        query_text=request.query, 
        top_k=request.top_k
    )
    
    if not results:
        return {
            "message": "검색 결과가 없습니다.",
            "results": [],
            "count": 0
        }
    
    return {
        "results": results,
        "count": len(results),
        "query": request.query
    }