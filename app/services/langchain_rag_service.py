import logging
from typing import List, Dict
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.config import settings
import csv

logger = logging.getLogger("soulstay.langchain_rag")


class LangChainRAGService:
    """LangChain 기반 RAG 서비스"""

    def __init__(self):
        # OpenAI LLM 초기화
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.5,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # OpenAI Embeddings 초기화
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # ChromaDB vectorstore 초기화
        self.vectorstore = Chroma(
            collection_name="feedback_embeddings",
            embedding_function=self.embeddings,
            persist_directory=settings.CHROMA_DB_PATH
        )
        
        # 프롬프트 템플릿 정의
        self.prompt_template = PromptTemplate(
            input_variables=["customer_feedback", "emotion", "similar_cases"],
            template="""당신은 SoulStay 호텔의 친절하고 전문적인 고객 상담 담당자입니다.
고객의 감정에 공감하며 진정성 있게 답변하세요.

답변 가이드:
- 긍정적 피드백: 감사 표현과 함께 앞으로도 최선을 다하겠다는 다짐
- 부정적 피드백: 진심 어린 사과와 구체적인 개선 의지 표현
- 중립적 피드백: 의견에 대한 감사와 경청하는 태도

고객 피드백: "{customer_feedback}"
감정 분석 결과: {emotion}

참고할 유사한 고객 피드백:
{similar_cases}

위 고객의 피드백에 대해 공감적이고 전문적인 답변을 2-3문장으로 간결하고 따뜻하게 작성해주세요."""
        )
        
        # ✅ LCEL 방식으로 체인 생성 (최신 방식)
        self.chain = self.prompt_template | self.llm | StrOutputParser()
        
        logger.info("✅ LangChain RAG 서비스 초기화 완료")

    def load_feedback_csv(self, csv_path: str):
        """CSV에서 피드백 데이터를 읽어 vectorstore에 추가"""
        try:
            # 기존 데이터 삭제
            try:
                self.vectorstore.delete_collection()
                self.vectorstore = Chroma(
                    collection_name="feedback_embeddings",
                    embedding_function=self.embeddings,
                    persist_directory=settings.CHROMA_DB_PATH
                )
                logger.info("🗑️ 기존 vectorstore 초기화")
            except:
                pass

            # CSV 읽기
            documents = []
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if row.get("text"):
                        doc = Document(
                            page_content=row["text"].strip(),
                            metadata={"id": f"fb_{i}", "emotion": row.get("emotion", "neutral")}
                        )
                        documents.append(doc)

            if not documents:
                logger.warning("⚠️ CSV 파일이 비어있습니다.")
                return

            # Vectorstore에 추가
            self.vectorstore.add_documents(documents)
            logger.info(f"✅ {len(documents)}개의 피드백을 vectorstore에 추가 완료")

        except FileNotFoundError:
            logger.error(f"❌ CSV 파일을 찾을 수 없습니다: {csv_path}")
        except Exception as e:
            logger.exception(f"❌ CSV 로드 중 오류 발생: {e}")

    def add_feedback_to_rag(self, user_id: int, feedback_text: str):
        """새로운 피드백 추가"""
        try:
            if not feedback_text.strip():
                logger.warning("⚠️ 빈 피드백은 추가하지 않습니다.")
                return

            doc = Document(
                page_content=feedback_text.strip(),
                metadata={"id": f"fb_user_{user_id}", "user_id": user_id}
            )
            
            self.vectorstore.add_documents([doc])
            logger.info(f"🆕 새로운 피드백 추가 완료 (user_id={user_id})")

        except Exception as e:
            logger.exception(f"❌ 새 피드백 추가 실패: {e}")

    def search_similar_feedback(self, query: str, top_k: int = 3) -> List[Dict]:
        """유사한 피드백 검색"""
        try:
            if not query.strip():
                logger.warning("⚠️ 빈 쿼리로 검색 요청됨.")
                return []

            # Vectorstore에서 유사 문서 검색
            results = self.vectorstore.similarity_search_with_score(query, k=top_k)
            
            matches = [
                {"text": doc.page_content, "score": float(score)}
                for doc, score in results
            ]

            logger.info(f"🔍 유사 피드백 {len(matches)}개 검색 완료")
            return matches

        except Exception as e:
            logger.exception(f"❌ 유사 피드백 검색 실패: {e}")
            return []

    def generate_response(self, customer_feedback: str, emotion: str, similar_cases: List[Dict]) -> str:
        """LangChain LCEL을 사용하여 응답 생성"""
        try:
            # 유사 사례 포맷팅
            cases_text = ""
            if similar_cases:
                cases_text = "\n".join([f"{i+1}. {case['text']}" for i, case in enumerate(similar_cases[:3])])
            else:
                cases_text = "유사한 사례 없음"

            # ✅ LCEL invoke 사용 (최신 방식)
            response = self.chain.invoke({
                "customer_feedback": customer_feedback,
                "emotion": emotion,
                "similar_cases": cases_text
            })

            return response.strip()

        except Exception as e:
            logger.exception(f"❌ 응답 생성 실패: {e}")
            # 기본 응답
            responses = {
                "positive": "소중한 의견 감사드립니다. 앞으로도 더 나은 서비스로 보답하겠습니다.",
                "negative": "불편을 드려 정말 죄송합니다. 고객님의 의견을 바탕으로 개선하도록 노력하겠습니다.",
                "neutral": "의견 주셔서 감사합니다. 서비스 향상에 참고하겠습니다.",
            }
            return responses.get(emotion, "피드백 감사드립니다.")

    def get_rag_status(self) -> Dict:
        """RAG 상태 확인"""
        try:
            # Collection의 문서 개수 확인
            count = len(self.vectorstore.get()['ids']) if self.vectorstore.get()['ids'] else 0
            return {"total_documents": count}
        except Exception as e:
            logger.exception(f"RAG 상태 확인 실패: {e}")
            return {"error": str(e)}