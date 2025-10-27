from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import auth, emotion, rag, user as user_routes
from app.database import Base, engine
from app.models import user as user_model, emotion_log

app = FastAPI()

# ✅ 정적 파일 경로 등록
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ✅ 템플릿 폴더 지정
templates = Jinja2Templates(directory="app/templates")

# ✅ 라우터 등록
app.include_router(auth.router)
app.include_router(emotion.router)
app.include_router(user_routes.router)
app.include_router(rag.router)

@app.get("/")
def root():
    return {"message": "SoulStay API running"}

# ✅ 테이블 자동 생성
Base.metadata.create_all(bind=engine)
