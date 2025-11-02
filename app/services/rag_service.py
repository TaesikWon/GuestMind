import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.schema import Document
from sentence_transformers import SentenceTransformer, util


class RAGService:
    """LangChain + Chroma 기반 RAG 검색 서비스 (Re-ranking 포함)"""

    def __init__(self):
        # ✅ 임베딩 모델 (한국어 SBERT)
        self.embedding_model = "jhgan/ko-sroberta-multitask"
        self.embedding = SentenceTransformerEmbeddings(model_name=self.embedding_model)

        # ✅ SentenceTransformer 로드 (re-ranking용)
        self.reranker = SentenceTransformer(self.embedding_model)

        # ✅ Chroma DB 설정
        self.persist_dir = os.path.join("app", "services", "embeddings", "soulstay_index")
        os.makedirs(self.persist_dir, exist_ok=True)

        self.vector_db = Chroma(
            collection_name="soulstay_reviews",
            embedding_function=self.embedding,
            persist_directory=self.persist_dir
        )

    def add_documents(self, docs: list):
        """
        텍스트 리스트를 받아 Chroma에 추가
        docs: ["문장1", "문장2", ...]
        """
        documents = [Document(page_content=text) for text in docs]
        self.vector_db.add_documents(documents)
        self.vector_db.persist()
        return f"✅ {len(docs)}개 문서가 추가되었습니다."

    def search(self, text: str, emotion: str, top_k: int = 3):
        """
        text: 사용자가 입력한 문장
        emotion: 감정 분석 결과 (positive/negative/neutral)
        top_k: 반환할 결과 개수
        """
        try:
            # 1️⃣ 1차 검색 (벡터 유사도 기반 Top-10)
            initial_results = self.vector_db.similarity_search(text, k=10)
            if not initial_results:
                return [{"text": "유사한 사례가 없습니다.", "emotion": "neutral"}]

            # 2️⃣ Re-ranking (SentenceTransformer cosine similarity)
            query_emb = self.reranker.encode(text, convert_to_tensor=True)
            doc_texts = [r.page_content for r in initial_results]
            doc_embs = self.reranker.encode(doc_texts, convert_to_tensor=True)

            scores = util.cos_sim(query_emb, doc_embs)[0]
            ranked_indices = scores.argsort(descending=True)

            # 3️⃣ 상위 top_k 결과만 정렬 반환
            reranked_results = [initial_results[i] for i in ranked_indices[:top_k]]

            # 4️⃣ 감정 태그 부착 (검색 결과 자체에 감정 정보 없음 → 요청 감정 반영)
            response = [{"text": r.page_content, "emotion": emotion} for r in reranked_results]

            return response

        except Exception as e:
            print(f"[RAG ERROR] {e}")
            return [{"text": f"⚠️ 검색 오류: {str(e)}", "emotion": "error"}]


# ✅ 기존 코드 호환성 유지
LangChainRAGService = RAGService
