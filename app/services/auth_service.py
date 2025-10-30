import logging
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app.models.user import User

logger = logging.getLogger("soulstay.auth")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =============================
# 🔐 OAuth2 스킴 설정
# =============================
# 로그인 시 토큰을 발급받을 URL 지정 (/auth/login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# =============================
# 🔐 비밀번호 관련
# =============================
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# =============================
# 🔑 JWT 토큰 생성
# =============================
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        logger.debug(f"Access token created for {data.get('sub')}")
        return encoded_jwt
    except Exception as e:
        logger.exception(f"토큰 생성 중 오류: {e}")
        raise

def create_refresh_token(data: dict):
    try:
        expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        logger.debug(f"Refresh token created for {data.get('sub')}")
        return encoded_jwt
    except Exception as e:
        logger.exception(f"리프레시 토큰 생성 오류: {e}")
        raise

# =============================
# 👤 유저 인증 로직
# =============================
def authenticate_user(email: str, password: str, db):
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            logger.warning(f"❌ 로그인 실패 - 존재하지 않는 사용자: {email}")
            return None
        if not verify_password(password, user.password):
            logger.warning(f"❌ 로그인 실패 - 비밀번호 불일치: {email}")
            return None
        logger.info(f"✅ 로그인 성공: {email}")
        return user
    except Exception as e:
        logger.exception(f"사용자 인증 중 오류: {e}")
        return None
