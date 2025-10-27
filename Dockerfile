# ===============================
# SoulStay Dockerfile
# ===============================

# 1️⃣ Python 베이스 이미지 선택
FROM python:3.11-slim

# 2️⃣ 작업 디렉토리 생성
WORKDIR /app

# 3️⃣ 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ 앱 코드 복사
COPY . .

# 5️⃣ FastAPI 실행 (Uvicorn)
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
