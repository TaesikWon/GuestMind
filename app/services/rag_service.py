import csv
import logging
from app.vectorstore import collection, embedding_function

logger = logging.getLogger("soulstay.rag_service")

# ✅ CSV 기반 초기 데이터 로드
def load_feedback_csv(csv_path: str):
    """feedback_samples.csv 파일을 읽어서 ChromaDB에 임베딩 추가"""
    try:
        # 기존 데이터 완전 삭제 (새로 로드하기 위해)
        try:
            existing_ids = collection.get()['ids']
            if existing_ids:
                collection.delete(ids=existing_ids)
                logger.info(f"🗑️ 기존 {len(existing_ids)}개 데이터 삭제")
        except:
            pass

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            texts = [row["text"].strip() for row in reader if row.get("text")]

        if not texts:
            logger.warning("⚠️ CSV 파일이 비어있거나 'text' 컬럼이 없습니다.")
            return

        embeddings = embedding_function(texts)
        ids = [f"fb_{i}" for i in range(len(texts))]
        collection.add(documents=texts, embeddings=embeddings, ids=ids)

        logger.info(f"✅ {len(texts)}개의 피드백을 RAG 벡터DB에 추가 완료")

    except FileNotFoundError:
        logger.error(f"❌ CSV 파일을 찾을 수 없습니다: {csv_path}")
    except Exception as e:
        logger.exception(f"❌ CSV 로드 중 오류 발생: {e}")


# ✅ 새 피드백 추가 (중복 체크 포함)
def add_feedback_to_rag(user_id: int, feedback_text: str):
    """새로운 사용자 피드백을 RAG 벡터DB에 추가"""
    try:
        feedback_text = feedback_text.strip()
        if not feedback_text:
            logger.warning("⚠️ 빈 피드백은 추가하지 않습니다.")
            return

        # 중복 피드백 확인
        existing = collection.query(query_texts=[feedback_text], n_results=1)
        if existing and existing.get("documents") and existing["documents"][0]:
            existing_text = existing["documents"][0][0]
            if existing_text == feedback_text:
                logger.info("⚠️ 동일한 피드백이 이미 존재합니다. 추가하지 않습니다.")
                return

        embedding = embedding_function([feedback_text])[0]
        doc_id = f"fb_user_{user_id}_{collection.count() + 1}"

        collection.add(
            documents=[feedback_text],
            embeddings=[embedding],
            ids=[doc_id],
        )

        logger.info(f"🆕 새로운 피드백 추가 완료 (user_id={user_id})")

    except Exception as e:
        logger.exception(f"❌ 새 피드백 추가 실패: {e}")


# ✅ 유사 피드백 검색 (RAG Retrieval)
def search_similar_feedback(query: str, top_k: int = 3, min_score: float = 0.1):
    """입력 텍스트와 유사한 피드백 검색"""
    try:
        if not query.strip():
            logger.warning("⚠️ 빈 쿼리로 검색 요청됨.")
            return []

        query_embedding = embedding_function([query])[0]
        results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

        if not results or "documents" not in results:
            return []

        matches = [
            {"text": t, "score": float(s)}
            for t, s in zip(results["documents"][0], results["distances"][0])
            if float(s) > min_score
        ]

        logger.info(f"🔍 유사 피드백 {len(matches)}개 검색 완료")
        return matches

    except Exception as e:
        logger.exception(f"❌ 유사 피드백 검색 실패: {e}")
        return []


# ✅ RAG 상태 확인용 함수
def get_rag_status():
    """현재 RAG 데이터 상태 반환"""
    try:
        count = collection.count()
        return {"total_documents": count}
    except Exception as e:
        logger.exception(f"RAG 상태 확인 실패: {e}")
        return {"error": str(e)}


# ✅ 클래스 인터페이스 (기존 코드 호환용)
class RAGService:
    """RAG 관련 기능을 묶은 서비스 클래스"""

    @staticmethod
    def load_feedback_csv(csv_path: str):
        return load_feedback_csv(csv_path)

    @staticmethod
    def add_feedback_to_rag(user_id: int, feedback_text: str):
        return add_feedback_to_rag(user_id, feedback_text)

    @staticmethod
    def search_similar_feedback(query: str, top_k: int = 3):
        return search_similar_feedback(query, top_k)