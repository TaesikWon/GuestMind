from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import create_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["Auth"])

# 입력 데이터 모델
class UserCreate(BaseModel):
    username: str
    password: str

# 회원가입
@router.post("/signup")
def signup(request: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, request.username, request.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User created successfully", "username": user.username}

# 로그인
@router.post("/login")
def login(request: UserCreate, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "username": user.username}