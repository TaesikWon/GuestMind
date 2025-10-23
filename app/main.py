from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, emotion_log
from app.routes import auth

# ✅ FastAPI 인스턴스 생성
app = FastAPI(title="GuestMind")

# ✅ DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

# ✅ 라우터 등록
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello, GuestMind!"}
