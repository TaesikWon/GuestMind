import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.schema import Document

class RAGService:
    """LangChain + Chroma 기반 RAG 검색 서비스"""

    def __init__(self):
        # ✅ 임베딩 모델 설정 (한국어 대응 SentenceTransformer)
        embedding_model = "jhgan/ko-sroberta-multitask"
        self.embedding = SentenceTransformerEmbeddings(model_name=embedding_model)

        # ✅ Chroma 벡터 DB 초기화
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
        """
        try:
            results = self.vector_db.similarity_search(text, k=top_k)
            if not results:
                return [{"text": "유사한 사례가 없습니다.", "emotion": "neutral"}]

            # LangChain Document 객체 → dict로 변환
            response = [{"text": r.page_content, "emotion": emotion} for r in results]
            return response
        except Exception as e:
            print(f"[RAG ERROR] {e}")
            return [{"text": f"⚠️ 검색 오류: {str(e)}", "emotion": "error"}]


# ✅ 호환용 (기존 코드 유지)
LangChainRAGService = RAGService
