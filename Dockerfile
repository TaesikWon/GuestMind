# ===============================
# SoulStay Dockerfile
# ===============================

# 1️⃣ Python 베이스 이미지 선택
FROM python:3.11-slim AS base

# 2️⃣ 환경 변수 설정 (버퍼링 끄기 & UTF-8 강제)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ 작업 디렉토리 생성
WORKDIR /app

# 4️⃣ 시스템 패키지 업데이트 + psycopg2 의존성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5️⃣ requirements.txt 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6️⃣ 앱 코드 복사
COPY . .

# 7️⃣ 포트 노출
EXPOSE 8000

# 8️⃣ 실행 명령 (uvicorn)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
