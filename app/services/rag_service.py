# app/services/rag_service.py
import os
import logging
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.schema import Document

logger = logging.getLogger("soulstay.langchain_rag")


class LangChainRAGService:
    def __init__(self, collection_name="soulstay_feedback", use_gpt: bool = False):
        """
        LangChain 기반 RAG 서비스
        - use_gpt=False : 자체 모델만 사용 (기본값)
        - use_gpt=True : OpenAI를 문장 자연화에 보조적으로 사용
        """
        try:
            self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
            self.vectorstore = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory="./chroma_langchain"
            )

            self.llm = None
            if use_gpt:
                self.llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.3,
                    openai_api_key=os.getenv("OPENAI_API_KEY")
                )

            logger.info(f"✅ LangChain RAG 초기화 완료 (GPT 사용: {use_gpt})")

        except Exception as e:
            logger.exception(f"❌ LangChain RAG 초기화 실패: {e}")
            raise

    def add_document(self, text: str, metadata: dict = None):
        """문서를 LangChain VectorStore에 추가"""
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_text(text)
            docs = [Document(page_content=c, metadata=metadata or {}) for c in chunks]
            self.vectorstore.add_documents(docs)
            logger.info(f"📚 문서 추가 완료 ({len(chunks)}개 청크)")
            return True
        except Exception as e:
            logger.exception(f"❌ 문서 추가 실패: {e}")
            return False

    def search(self, query: str, top_k: int = 3):
        """RAG 벡터 검색"""
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": top_k})
        return retriever.get_relevant_documents(query)

    def ask_with_context(self, query: str, top_k: int = 3):
        """검색 + GPT로 문맥 정리 (보조용)"""
        if not self.llm:
            logger.warning("⚠️ GPT 비활성화 상태, 검색 결과만 반환")
            return self.search(query, top_k=top_k)

        retriever = self.vectorstore.as_retriever(search_kwargs={"k": top_k})
        qa_chain = RetrievalQA.from_chain_type(llm=self.llm, retriever=retriever, chain_type="stuff")
        answer = qa_chain.invoke({"query": query})
        return answer["result"]

RAGService = LangChainRAGService
