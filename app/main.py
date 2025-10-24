from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.database import Base, engine
from app.models import user, emotion_log
from app.routes import auth, emotion, user as user_routes
import json

# FastAPI 앱 생성 (중복 제거)
app = FastAPI(title="SoulStay")

# 템플릿 설정
templates = Jinja2Templates(directory="app/templates")

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

# 라우터 등록
app.include_router(auth.router)
app.include_router(emotion.router)
app.include_router(user_routes.router)

# 루트 엔드포인트
@app.get("/")
def root():
    return RedirectResponse(url="/emotion")