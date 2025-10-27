# app/routes/user.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from fastapi.templating import Jinja2Templates
from fastapi import Request

router = APIRouter(prefix="/user", tags=["User"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def user_list(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("user_list.html", {"request": request, "users": users})

@router.get("/{user_id}")
def user_detail(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    return templates.TemplateResponse("user_detail.html", {"request": request, "user": user})
