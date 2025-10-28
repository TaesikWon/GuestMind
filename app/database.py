# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# --- DB 연결 URL ---
SQLALCHEMY_DATABASE_URL = settings.database_url

# --- SQLAlchemy 엔진 및 세션 ---
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- 모델 베이스 클래스 ---
Base = declarative_base()

# --- DB 세션 종속성 (FastAPI Depends에서 사용) ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
