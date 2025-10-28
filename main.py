# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
import logging
import atexit

# -------------------------------
# 🔹 내부 모듈 Import
# -------------------------------
from app.routes import auth, emotion, rag, user as user_routes
from app.api import health  # ✅ 새 헬스체크 라우터
from app.database import Base, engine, SessionLocal
from app.services import summary_service

# ==========================
# 🧱 로깅 설정
# ==========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("soulstay.main")

# ==========================
# 🧠 스케줄러 설정
# ==========================
scheduler = BackgroundScheduler(timezone="Asia/Seoul")

def run_daily_pipeline():
    """매일 자정 감정 로그 요약"""
    db = SessionLocal()
    try:
        count = summary_service.update_daily_summary(db)
        db.commit()
        logger.info(f"✅ Daily pipeline 완료 — {count}건 처리")
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Daily pipeline 오류: {e}")
        raise
    finally:
        db.close()

# ==========================
# 🔄 Lifespan 이벤트 (startup/shutdown)
# ==========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    
    if not scheduler.get_jobs():
        scheduler.add_job(
            run_daily_pipeline,
            CronTrigger(hour=0, minute=0),
            id="daily_summary_job",
            replace_existing=True
        )
        scheduler.start()
        logger.info("🕒 Scheduler started")
    
    yield  # 앱 실행
    
    # Shutdown
    if scheduler.running:
        scheduler.shutdown()
        logger.info("🛑 Scheduler stopped")

# 프로세스 종료 시 자동 정리
atexit.register(lambda: scheduler.shutdown() if scheduler.running else None)

# ==========================
# 🌐 FastAPI 앱 생성
# ==========================
app = FastAPI(
    title="SoulStay API",
    version="1.2",
    lifespan=lifespan
)

# ==========================
# 📁 정적 파일
# ==========================
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ==========================
# 🧩 라우터 등록
# ==========================
app.include_router(auth.router)
app.include_router(emotion.router)
app.include_router(user_routes.router)
app.include_router(rag.router)
app.include_router(health.router)  # ✅ 헬스 라우터 추가

# ==========================
# 🧬 루트 엔드포인트
# ==========================
@app.get("/")
def root():
    return {
        "message": "SoulStay API running",
        "version": "1.2",
        "scheduler": "active" if scheduler.running else "stopped"
    }
