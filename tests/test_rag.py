# tests/test_rag_workflow.py
from app.services import rag_service

def test_rag_add_and_search():
    text = "호텔 서비스가 친절했어요."
    rag_service.add_feedback_to_rag(999, text)
    results = rag_service.search_similar_feedback("친절한 직원", top_k=1)
    assert len(results) > 0
    assert "친절" in results[0]["text"]
