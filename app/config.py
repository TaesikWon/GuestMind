from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # ✅ 주요 API / 보안 관련
    openai_api_key: str
    secret_key: str
    algorithm: str

    # ✅ Database / Storage
    database_url: str
    chroma_db_path: str

    # ✅ Token 설정
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    # ✅ 환경 구분
    app_env: str = "development"

    # ✅ AWS 관련
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_s3_bucket_name: str
    aws_region: str

    # ✅ 로깅 (선택적)
    log_level: str | None = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # ✅ 대소문자 구분 안 함
        extra="ignore",        # ✅ 정의 안 된 .env 변수 무시
    )

    # ✅ 대문자 접근도 자동 변환
    def __getattr__(self, name: str):
        return getattr(self, name.lower())

settings = Settings()
