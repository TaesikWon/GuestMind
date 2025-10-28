# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # -------------------------------
    # 🧠 기본 설정
    # -------------------------------
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    db_url: str = Field(..., env="DB_URL")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")

    access_token_expire_minutes: int = Field(default=60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")

    chroma_db_path: str = Field(default="./data/chroma", env="CHROMA_DB_PATH")
    app_env: str = Field(default="development", env="APP_ENV")

    # -------------------------------
    # ☁️ AWS 선택 설정 (S3 / 배포용)
    # -------------------------------
    aws_access_key_id: str | None = Field(default=None, env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str | None = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    aws_s3_bucket: str | None = Field(default=None, env="AWS_S3_BUCKET")
    aws_region: str | None = Field(default=None, env="AWS_REGION")

    # -------------------------------
    # ⚙️ 설정
    # -------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,  # 🔑 대소문자 구분 안함!
        extra="ignore"         # ✅ .env에 추가 키 있어도 무시 (에러 X)
    )

    # -------------------------------
    # 🔄 대문자 alias (기존 코드 호환용)
    # -------------------------------
    @property
    def OPENAI_API_KEY(self): return self.openai_api_key
    @property
    def DB_URL(self): return self.db_url
    @property
    def SECRET_KEY(self): return self.secret_key
    @property
    def ALGORITHM(self): return self.algorithm
    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self): return self.access_token_expire_minutes
    @property
    def REFRESH_TOKEN_EXPIRE_DAYS(self): return self.refresh_token_expire_days
    @property
    def CHROMA_DB_PATH(self): return self.chroma_db_path
    @property
    def APP_ENV(self): return self.app_env
    @property
    def AWS_ACCESS_KEY_ID(self): return self.aws_access_key_id
    @property
    def AWS_SECRET_ACCESS_KEY(self): return self.aws_secret_access_key
    @property
    def AWS_S3_BUCKET(self): return self.aws_s3_bucket
    @property
    def AWS_REGION(self): return self.aws_region


settings = Settings()
