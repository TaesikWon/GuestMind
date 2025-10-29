# app/services/langchain_rag_service.py
import os
import logging
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.schema import Document

logger = logging.getLogger("soulstay.langchain_rag")

class LangChainRAGService:
    def __init__(self, collection_name="soulstay_feedback"):
        """LangChain 기반 RAG 서비스 초기화"""
        try:
            self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
            self.vectorstore = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory="./chroma_langchain"
            )
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.3,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            logger.info(f"✅ LangChain RAG 초기화 완료 — collection='{collection_name}'")
        except Exception as e:
            logger.exception(f"❌ LangChain RAG 초기화 실패: {e}")
            raise

    def add_document(self, text: str, metadata: dict = None):
        """문서를 LangChain VectorStore에 추가"""
        try:
            # 긴 텍스트는 자동 분할
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_text(text)
            docs = [Document(page_content=c, metadata=metadata or {}) for c in chunks]
            self.vectorstore.add_documents(docs)
            logger.info(f"📚 LangChain RAG 문서 추가 완료 ({len(chunks)}개 청크)")
        except Exception as e:
            logger.exception(f"❌ 문서 추가 실패: {e}")

    def search(self, query: str, top_k: int = 3):
        """벡터 기반 문서 검색"""
        try:
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": top_k})
            results = retriever.get_relevant_documents(query)
            logger.info(f"🔍 검색 완료 — {len(results)}개 결과")
            return results
        except Exception as e:
            logger.exception(f"❌ 검색 실패: {e}")
            return []

    def ask_with_context(self, query: str, top_k: int = 3):
        """문서 검색 + LLM 답변 생성 (RAG 완성형)"""
        try:
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": top_k})
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                retriever=retriever,
                chain_type="stuff"
            )
            answer = qa_chain.invoke({"query": query})
            logger.info("💬 RAG 응답 생성 완료")
            return answer["result"]
        except Exception as e:
            logger.exception(f"❌ RAG 질의 실패: {e}")
            return "오류가 발생했습니다."
