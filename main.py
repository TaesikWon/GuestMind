# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import logging

logger = logging.getLogger("soulstay.main")

# ✅ 스케줄러 전역 변수
scheduler = BackgroundScheduler()

def run_daily_pipeline():
    """매일 자정 실행되는 요약 작업"""
    logger.info("🌙 일일 요약 파이프라인 시작...")
    # 여기에 실제 요약 로직 추가

# ✅ Lifespan 이벤트 핸들러 (startup/shutdown 통합)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler.add_job(
        run_daily_pipeline,
        trigger="cron",
        hour=0,
        minute=0,
        id="daily_summary"
    )
    scheduler.start()
    logger.info("🕒 Scheduler started")
    
    yield  # 서버 실행 중
    
    # Shutdown
    scheduler.shutdown()
    logger.info("🛑 Scheduler stopped")

# ✅ FastAPI 앱 생성 (lifespan 적용)
app = FastAPI(
    title="SoulStay API",
    version="1.0.0",
    lifespan=lifespan  # 여기에 lifespan 추가
)

# 라우터 등록
from app.routes import health, auth, chat, emotion, user
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(emotion.router)
app.include_router(user.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)