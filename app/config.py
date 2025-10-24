from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    OPENAI_API_KEY: str
    DATABASE_URL: str = "sqlite:///./soulstay.db"

    class Config:
        env_file = ".env"

# 인스턴스 생성
settings = Settings()
