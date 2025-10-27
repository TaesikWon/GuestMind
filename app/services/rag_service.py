# services/rag_service.py
import chromadb
from openai import OpenAI
from app.config import settings  # ✅ 환경 변수 불러오기

# ✅ OpenAI 클라이언트 (API 키 설정)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# ✅ ChromaDB 영속 경로 (.env에서 불러옴)
chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection("feedback_embeddings")

def add_feedback_to_rag(feedback_id, feedback_text):
    """피드백 텍스트를 임베딩 후 ChromaDB에 저장"""
    try:
        embedding = client.embeddings.create(
            model="text-embedding-3-small",
            input=feedback_text
        ).data[0].embedding

        collection.add(
            ids=[str(feedback_id)],
            embeddings=[embedding],
            documents=[feedback_text]
        )
        return True
    except Exception as e:
        print(f"[RAG] ❌ Add failed: {e}")
        return False


def search_similar_feedback(query_text, top_k=3):
    """입력 텍스트와 유사한 피드백 검색"""
    try:
        query_emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=query_text
        ).data[0].embedding

        results = collection.query(
            query_embeddings=[query_emb],
            n_results=top_k
        )

        hits = [
            {"text": doc, "distance": dist}
            for doc, dist in zip(results["documents"][0], results["distances"][0])
        ]
        return hits
    except Exception as e:
        print(f"[RAG] ❌ Search failed: {e}")
        return []
