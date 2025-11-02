from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
import logging
import datetime

router = APIRouter(prefix="/health", tags=["Health"])
logger = logging.getLogger("soulstay.health")

@router.get("/ping")
def ping():
    """서버 정상 응답 확인용"""
    return {
        "status": "ok",
        "message": "Server is running",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"  # ✅ 시간 표시
    }

@router.get("/db")
def check_database(db: Session = Depends(get_db)):
    """데이터베이스 연결 상태 확인"""
    try:
        db.execute("SELECT 1")
        logger.info("✅ Database connection check succeeded")
        return {
            "status": "ok",
            "message": "Database connected",
            "checked_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return {
            "status": "error",
            "message": str(e),
            "checked_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
