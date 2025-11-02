# main.py
from fastapi import FastAPI
from app.routes import chat, health   # ✅ health.py 포함
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from dotenv import load_dotenv
from app.services import rag_service

# --- 환경 변수 로드 ---
load_dotenv()

# --- 로거 설정 ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("soulstay.main")

# ✅ FastAPI 앱 정의 (가장 먼저 선언해야 함)
app = FastAPI(
    title="SoulStay Chatbot API",
    description="AI 기반 감정 분석 + RAG 응답 생성 백엔드 시스템",
    version="1.0.0",
)

# ✅ 라우터 등록 (app 정의 이후에!)
app.include_router(chat.router)
app.include_router(health.router)

# --- 스케줄러 초기화 ---
scheduler = BackgroundScheduler()

def run_daily_pipeline():
    logger.info("🧩 매일 실행되는 통계 파이프라인")

scheduler.add_job(run_daily_pipeline, "interval", hours=24)
scheduler.start()
logger.info("🕒 Scheduler started")

# ✅ 서버 시작 시 RAG 초기화
@app.on_event("startup")
def startup_event():
    try:
        rag_service.load_feedback_csv("data/feedback_samples.csv")
        logger.info("✅ RAG 초기화 완료 (feedback_samples.csv 불러옴)")
    except Exception as e:
        logger.error(f"❌ RAG 초기화 실패: {e}")

# ✅ 서버 종료 시 스케줄러 정리
@app.on_event("shutdown")
def shutdown_event():
    try:
        scheduler.shutdown(wait=False)
        logger.info("🛑 Scheduler stopped.")
    except Exception as e:
        logger.error(f"❌ Scheduler 종료 중 오류: {e}")
