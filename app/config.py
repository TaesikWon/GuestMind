from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str = "sqlite:///./soulstay.db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ✅ 추가: .env에 존재하는 항목 등록
    CHROMA_DB_PATH: str = "app/chroma_db"
    APP_ENV: str = "development"

    # ✅ Pydantic v2 방식 (class Config 대신)
    model_config = ConfigDict(env_file=".env")


settings = Settings()
