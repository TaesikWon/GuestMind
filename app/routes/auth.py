#app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.services.user_service import create_user, authenticate_user
from app.utils.token_service import create_access_token, verify_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# 현재 로그인된 사용자 확인용
@router.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"username": username}
