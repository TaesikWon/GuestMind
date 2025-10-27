# 🧾 SoulStay API 명세서

## 📘 Base URL
http://localhost:8000

yaml
코드 복사

---

## 🔐 Auth API

### ▶ `/auth/signup` (POST)

**설명:** 회원가입

**입력:**
```json
{
  "username": "test",
  "password": "1234"
}
출력:

json
코드 복사
{
  "message": "User created successfully"
}
▶ /auth/login (POST)
설명: 로그인 후 JWT 토큰 발급

입력:

json
코드 복사
{
  "username": "test",
  "password": "1234"
}
출력:

json
코드 복사
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5...",
  "token_type": "bearer"
}
🧠 Emotion API
▶ /emotion/analyze (POST)
설명: 텍스트 감정 분석

입력:

json
코드 복사
{
  "feedback": "호텔 직원이 너무 친절했어요!"
}
출력:

json
코드 복사
{
  "emotion": "positive",
  "reason": "친절한 경험에 대한 긍정적인 피드백"
}
🧩 RAG API
▶ /rag/search (POST)
설명: 유사 피드백 검색

입력:

json
코드 복사
{
  "query": "청결 관련 불만",
  "top_k": 3
}
출력:

json
코드 복사
[
  {
    "feedback": "방 청소가 덜 되어 있었어요.",
    "similarity": 0.82
  }
]
👤 User API
▶ /user/detail/{id} (GET)
설명: 사용자 감정 로그 상세 조회

출력 예시:

json
코드 복사
{
  "user": "test",
  "emotion_logs": [
    {"text": "직원 친절", "emotion": "positive"},
    {"text": "식사가 별로", "emotion": "negative"}
  ]
}
📊 Summary API
▶ /summary/daily (GET)
설명: 일별 감정 요약 데이터 반환

출력:

json
코드 복사
{
  "date": "2025-10-27",
  "positive_ratio": 0.68,
  "negative_ratio": 0.21,
  "neutral_ratio": 0.11
}
🔁 Health Check
▶ / (GET)
출력:

json
코드 복사
{
  "message": "SoulStay API running with APScheduler & RAG chunking"
}
✅ 응답 코드 표
상태코드	의미
200	성공
201	생성됨
400	잘못된 요청
401	인증 실패
404	데이터 없음
500	서버 오류

🧩 예시 실행 흐름
1️⃣ /auth/signup → /auth/login
2️⃣ 토큰을 Authorization 헤더로 전달
3️⃣ /emotion/analyze → /rag/search
4️⃣ /summary/daily 로 통계 조회