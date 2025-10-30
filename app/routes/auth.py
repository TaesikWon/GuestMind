from fastapi import APIRouter, Form, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.database import get_db
from app.services import auth_service
from app.models.user import User
from app.utils.security import SECRET_KEY

router = APIRouter(prefix="/auth", tags=["Auth"])
templates = Jinja2Templates(directory="app/templates")

# ✅ 회원가입 폼 렌더링
@router.get("/register", response_class=HTMLResponse)
def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# ✅ 회원가입 처리
@router.post("/register", response_class=HTMLResponse)
def register_user(
    request: Request,
    email: str = Form(...),
    name: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.email == email.lower()).first()
    if existing_user:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "이미 등록된 이메일입니다. 다른 이메일을 사용해주세요.",
                "email": email,
                "name": name,
            },
        )

    auth_service.register_user(db, email, password, name)
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "success": f"🎉 {name}님, 회원가입이 완료되었습니다!"},
    )

# ✅ JWT 인증 헬퍼
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(auth_service.oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 토큰입니다.")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="사용자를 찾을 수 없습니다.")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰 인증 실패")
