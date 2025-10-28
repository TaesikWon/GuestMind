from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# ----------------------------
# ✅ 프로젝트 경로 설정
# ----------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import Base
from app.models import user, emotion_log, daily_summary  # 모델 등록

# ----------------------------
# ✅ Alembic 설정 불러오기
# ----------------------------
config = context.config

# ----------------------------
# ✅ 로깅 설정
# ----------------------------
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ----------------------------
# ✅ Metadata 등록 (자동 인식용)
# ----------------------------
target_metadata = Base.metadata


# ----------------------------
# 🧩 환경 변수에서 DB URL 불러오기
# ----------------------------
def get_url():
    """환경변수(.env) 또는 alembic.ini에서 DB URL 불러오기"""
    return os.getenv("DB_URL", config.get_main_option("sqlalchemy.url"))


# ----------------------------
# 🧱 오프라인 모드 (스크립트 생성만)
# ----------------------------
def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ----------------------------
# 🧱 온라인 모드 (DB 직접 적용)
# ----------------------------
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=get_url(),
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
