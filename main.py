from fastapi import FastAPI
from app.routes import chat
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from dotenv import load_dotenv  # ✅ 추가
load_dotenv()  # ✅ .env 파일 로드

logger = logging.getLogger("soulstay.main")

app = FastAPI(title="SoulStay Chatbot")

app.include_router(chat.router)

# --- 스케줄러 초기화 ---
scheduler = BackgroundScheduler()

def run_daily_pipeline():
    logger.info("🧩 매일 실행되는 통계 파이프라인")

scheduler.add_job(run_daily_pipeline, "interval", hours=24)
scheduler.start()
logger.info("🕒 Scheduler started")
