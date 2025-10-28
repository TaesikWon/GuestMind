# app/vectorstore.py
from chromadb import PersistentClient
from openai import OpenAI
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# ✅ OpenAI 클라이언트
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

def embedding_function(texts: list[str]) -> list[list[float]]:
    """
    OpenAI text-embedding-3-small 모델로 임베딩 벡터 생성
    
    Args:
        texts: 임베딩할 텍스트 리스트
        
    Returns:
        임베딩 벡터 리스트
        
    Raises:
        Exception: OpenAI API 호출 실패 시
    """
    try:
        response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        logger.error(f"임베딩 생성 실패: {e}")
        raise

# ✅ Chroma 클라이언트 초기화
try:
    chroma_client = PersistentClient(path=settings.CHROMA_DB_PATH)
    logger.info(f"ChromaDB 연결 성공: {settings.CHROMA_DB_PATH}")
except Exception as e:
    logger.error(f"ChromaDB 연결 실패: {e}")
    raise

# ✅ 컬렉션 가져오기 또는 생성
collection_name = "feedback_embeddings"

def get_collection():
    """컬렉션 가져오기 (없으면 생성)"""
    try:
        collection = chroma_client.get_collection(name=collection_name)
        logger.info(f"기존 컬렉션 로드: {collection_name}")
    except Exception:
        collection = chroma_client.create_collection(name=collection_name)
        logger.info(f"새 컬렉션 생성: {collection_name}")
    
    return collection

# 전역 컬렉션 객체
collection = get_collection()