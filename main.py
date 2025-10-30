# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
import logging
from dotenv import load_dotenv
load_dotenv()

# -------------------------------
# 🔹 내부 모듈 Import
# -------------------------------
from app.routes import auth, emotion, rag, user as user_routes
from app.api import health
from app.database import Base, engine, SessionLocal
from app.services import summary_service
from app.config import settings

# ==========================
# 🧱 로깅 설정
# ==========================
logging.basicConfig(
    level=logging.DEBUG if settings.app_env == "development" else logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
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
        logger.exception(f"❌ Daily pipeline 오류: {e}")
    finally:
        db.close()

# ==========================
# 🔄 Lifespan 이벤트
# ==========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    if not scheduler.get_jobs():
        scheduler.add_job(
            run_daily_pipeline,
            CronTrigger(hour=0, minute=0),
            id="daily_summary_job",
            replace_existing=True,
        )
        scheduler.start()
        logger.info("🕒 Scheduler started")

    yield  # 앱 실행 중

    if scheduler.running:
        scheduler.shutdown()
        logger.info("🛑 Scheduler stopped")

# ==========================
# 🌐 FastAPI 앱 생성
# ==========================
app = FastAPI(
    title="SoulStay API",
    version="1.3",
    lifespan=lifespan,
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
app.include_router(health.router)

# ==========================
# ⚠️ 전역 예외 핸들러
# ==========================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"❌ Unhandled Exception at {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "서버 내부 오류가 발생했습니다. 잠시 후 다시 시도해주세요."},
    )

# ==========================
# 🧬 루트 엔드포인트
# ==========================
@app.get("/")
def root():
    return {
        "message": "SoulStay API running",
        "scheduler": "active" if scheduler.running else "stopped",
    }
