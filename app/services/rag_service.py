# app/services/rag_service.py
import re
from app.vectorstore import chroma_client, embedding_function
from app.utils.logger import logger

# =====================================
# ✨ 텍스트 전처리 및 청킹
# =====================================
def split_text_into_chunks(text: str, max_len: int = 300):
    """문장을 청킹 단위로 나눠서 저장"""
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks, current = [], ""

    for sentence in sentences:
        if len(current) + len(sentence) < max_len:
            current += " " + sentence
        else:
            chunks.append(current.strip())
            current = sentence
    if current:
        chunks.append(current.strip())

    logger.debug(f"RAG: Split text into {len(chunks)} chunks")
    return chunks


# =====================================
# 💾 피드백 벡터 저장
# =====================================
def store_feedback_with_chunking(feedback_id: int, feedback_text: str, emotion: str):
    """피드백을 청킹 후 각 chunk를 임베딩 저장"""
    try:
        chunks = split_text_into_chunks(feedback_text)
        for idx, chunk in enumerate(chunks):
            chroma_client.add_texts(
                texts=[chunk],
                metadatas=[{
                    "feedback_id": feedback_id,
                    "chunk_id": idx,
                    "emotion": emotion
                }],
                ids=[f"{feedback_id}-{idx}"],
                embedding_function=embedding_function
            )
        logger.info(f"RAG: Stored feedback {feedback_id} with {len(chunks)} chunks")

    except Exception as e:
        logger.exception(f"RAG: Error while storing feedback {feedback_id} — {e}")
        raise RuntimeError("Failed to store feedback embeddings")


# =====================================
# 🔍 유사 피드백 검색 (선택)
# =====================================
def search_similar_feedback(query: str, top_k: int = 3):
    """입력 문장과 유사한 피드백 검색"""
    try:
        results = chroma_client.similarity_search(query, n_results=top_k)
        logger.debug(f"RAG: Search for '{query}' → {len(results)} results")
        return [
            {
                "text": r.page_content,
                "metadata": r.metadata
            }
            for r in results
        ]
    except Exception as e:
        logger.exception(f"RAG: Search error for query '{query}' — {e}")
        raise RuntimeError("Search failed in RAG service")
