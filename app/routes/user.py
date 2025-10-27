# app/routes/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.routes.auth import get_current_user
from fastapi.templating import Jinja2Templates
from fastapi import Request

router = APIRouter(prefix="/user", tags=["User"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def user_list(
    request: Request, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ← 인증 추가
):
    """
    사용자 목록 조회 (로그인 필요)
    """
    users = db.query(User).all()
    return templates.TemplateResponse("user_list.html", {
        "request": request, 
        "users": users,
        "current_user": current_user  # ← 템플릿에 전달
    })

@router.get("/{user_id}")
def user_detail(
    user_id: int, 
    request: Request, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ← 인증 추가
):
    """
    사용자 상세 정보 조회 (로그인 필요)
    본인 또는 관리자만 조회 가능하도록 제한 가능
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # ✅ 선택: 본인만 조회 가능하도록 제한
    # if current_user.id != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="You can only view your own profile"
    #     )
    
    return templates.TemplateResponse("user_detail.html", {
        "request": request, 
        "user": user,
        "current_user": current_user  # ← 템플릿에 전달
    })