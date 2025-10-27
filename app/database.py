# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()  # 트랜잭션 정상 완료 시 커밋
    except Exception:
        db.rollback()  # 예외 발생 시 되돌림
        raise           # 예외를 상위로 다시 전달
    finally:
        db.close()      # 세션 종료 (항상 실행)
