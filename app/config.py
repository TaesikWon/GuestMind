from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str = "sqlite:///./soulstay.db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # 🔹 새로 추가해야 하는 부분
    CHROMA_DB_PATH: str = "app/chroma_db"
    APP_ENV: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
