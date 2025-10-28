from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# ✅ .env 파일에서 불러온 PostgreSQL URL 사용
DATABASE_URL = settings.db_url

# ✅ PostgreSQL은 connect_args 필요 없음!
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 연결 확인
    echo=settings.APP_ENV == "development"  # 개발환경에서만 SQL 로그 출력
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """DB 세션 생성 (FastAPI Dependency)"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"❌ DB 세션 오류 발생: {e}")
        db.rollback()  # 에러 시 롤백
        raise
    finally:
        db.close()
