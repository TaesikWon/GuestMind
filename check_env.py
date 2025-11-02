# check_env.py
import os
from dotenv import load_dotenv

print("🔍 .env 파일 로드 테스트 시작...")

# 1️⃣ .env 파일 로드
load_dotenv()

# 2️⃣ 주요 환경 변수 확인
openai_key = os.getenv("OPENAI_API_KEY")

if openai_key:
    print("✅ OPENAI_API_KEY 로드 성공!")
    print(f"🔑 키 앞부분: {openai_key[:10]}... (총 {len(openai_key)}자)")
else:
    print("❌ OPENAI_API_KEY 로드 실패 — .env 파일 위치 또는 load_dotenv() 확인 필요")

# 3️⃣ 기타 환경 변수도 필요하면 추가 확인 가능
# db_url = os.getenv("DATABASE_URL")
# print("DATABASE_URL:", db_url)

print("🔎 테스트 완료")
