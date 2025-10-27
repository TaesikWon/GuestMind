from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging

# 내부 모듈
from app.routes import auth, emotion, rag, user as user_routes
from app.database import Base, engine, SessionLocal
from app.models import user as user_model, emotion_log, daily_summary
from app.services import summary_service, rag_service

# ==========================
# 🌐 기본 설정
# ==========================

app = FastAPI(title="SoulStay API", version="1.2")

# 정적 파일 & 템플릿 등록
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# ==========================
# 🧱 로깅 설정
# ==========================
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ==========================
# 📦 데이터베이스 초기화
# ==========================
Base.metadata.create_all(bind=engine)

# ==========================
# 🧩 라우터 등록
# ==========================
app.include_router(auth.router)
app.include_router(emotion.router)
app.include_router(user_routes.router)
app.include_router(rag.router)

# ==========================
# 🧠 APScheduler: 배치 파이프라인
# ==========================

# 전역 스케줄러 (중복 실행 방지)
scheduler = BackgroundScheduler(timezone="Asia/Seoul")

def run_daily_pipeline():
    """매일 자정마다 감정 로그를 요약해서 DailySummary에 저장"""
    db = SessionLocal()
    try:
        count = summary_service.update_daily_summary(db)
        logging.info(f"[{datetime.now()}] ✅ Daily pipeline 완료 — {count}건 처리됨")
    except Exception as e:
        logging.exception(f"[{datetime.now()}] ❌ Daily pipeline 오류: {e}")
    finally:
        db.close()

# 중복 등록 방지 — 서버 재시작 시 동일 job이 여러 번 추가되는 문제 예방
if not scheduler.get_jobs():
    scheduler.add_job(
        run_daily_pipeline,
        CronTrigger(hour=0, minute=0),
        id="daily_summary_job",
        replace_existing=True,
    )
    scheduler.start()
    logging.info("🕒 APScheduler started successfully")

# ==========================
# 🧬 루트 라우트
# ==========================
@app.get("/")
def root():
    return {"message": "SoulStay API running with APScheduler & RAG chunking"}

# ==========================
# 🧩 앱 종료 시 스케줄러 정리
# ==========================
@app.on_event("shutdown")
def shutdown_event():
    if scheduler.running:
        scheduler.shutdown()
        logging.info("🛑 Scheduler stopped cleanly.")
