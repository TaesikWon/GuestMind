from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# DB 엔진 생성
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 세션 (DB 연결 세션)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델들이 상속받을 Base 클래스
Base = declarative_base()

# ✅ FastAPI 의존성 주입용 DB 세션 함수
def get_db():
    db = SessionLocal()
    try:
        yield db   # 요청 중에 DB 세션 제공
    finally:
        db.close()  # 요청 끝나면 자동 닫기
