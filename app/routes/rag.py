from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.services.rag_service import RAGService
from app.routes.auth import get_current_user
from app.models.user import User
from app.database import get_db
import logging

router = APIRouter(prefix="/rag", tags=["RAG"])
rag_service = RAGService()
logger = logging.getLogger("soulstay.rag_route")

# ✅ 요청 모델 정의
class FeedbackAdd(BaseModel):
    feedback_text: str = Field(..., min_length=1, max_length=1000, description="피드백 내용")


class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="검색 쿼리")
    top_k: int = Field(default=3, ge=1, le=10, description="결과 개수 (1~10)")


# ✅ 피드백 추가
@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_feedback(
    request: FeedbackAdd = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """새로운 피드백을 RAG 벡터DB에 추가"""
    try:
        rag_service.add_feedback_to_rag(user_id=current_user.id, feedback_text=request.feedback_text)
        logger.info(f"🆕 RAG 피드백 추가 — user_id={current_user.id}")
        return {"message": "✅ 피드백이 벡터DB에 저장되었습니다."}
    except Exception as e:
        logger.exception(f"❌ RAG 피드백 추가 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"RAG 저장 실패: {type(e).__name__} - {e}",
        )


# ✅ 피드백 검색
@router.post("/search")
def search_feedback(
    request: SearchQuery = Body(...),
    current_user: User = Depends(get_current_user),
):
    """유사 피드백 검색"""
    try:
        results = rag_service.search_similar_feedback(query=request.query, top_k=request.top_k)
        return {"count": len(results), "results": results}
    except Exception as e:
        logger.exception(f"❌ 유사 피드백 검색 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"검색 실패: {type(e).__name__} - {e}",
        )
