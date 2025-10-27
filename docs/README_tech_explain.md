# 🧠 기술 구현 설명서 (README_tech_explain.md)

## 📘 프로젝트 개요

**프로젝트명:** SoulStay  
**목적:** 호텔 고객 피드백을 AI로 감정 분석하고, 사용자별 감정 트렌드와 통찰을 제공하는 서비스

---

## ⚙️ 시스템 아키텍처

**구성요소:**
* **FastAPI** — 백엔드 API 서버
* **SQLite → PostgreSQL** — 데이터베이스 (ORM: SQLAlchemy)
* **ChromaDB** — 피드백 벡터 저장소 (RAG 검색용)
* **OpenAI GPT-4o-mini** — 감정 분석 및 근거 생성
* **Jinja2 + Bootstrap** — 웹 프론트엔드
* **APScheduler** — 자동 데이터 파이프라인
* **Docker** — 배포 환경 컨테이너화

---

## 🧩 기술별 구현 상세

### 🔐 JWT 인증 (`app/utils/token_service.py`)

**기능:** 로그인 시 JWT 발급 및 유효성 검증  
**이유:** FastAPI의 `Depends(get_current_user)` 구조와 자연스럽게 통합  
**핵심 포인트:**
```python
payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
user = db.query(User).filter(User.id == payload.get("sub")).first()
```

→ DB 세션으로 실제 사용자 조회 → 쿠키/헤더 둘 다 인증 지원

---

### 🧠 감정 분석 (`app/services/emotion_service.py`)

**기능:** OpenAI GPT-4o-mini로 감정 분류 및 근거 생성  
**입력:** 고객 피드백 텍스트  
**출력:** JSON 구조 → `{ "emotion": "positive", "reason": "..." }`  
**이유:** GPT 모델의 자연어 이해력을 활용한 다중 감정 분석

---

### 🧬 RAG 검색 (`app/services/rag_service.py`)

**구조:**
1️⃣ 피드백 텍스트를 문장 단위로 청킹(chunking)  
2️⃣ 각 청크를 embedding → ChromaDB 저장  
3️⃣ 검색 시 유사 피드백 Top-k 불러와 GPT에 컨텍스트 제공

**핵심 함수:**
```python
def split_text_into_chunks(text: str, max_len=300):
    return re.split(r'(?<=[.!?]) +', text)
```

**이유:** 긴 텍스트를 문장 단위로 쪼개면 RAG 정확도가 향상됨

---

### 🕒 APScheduler 파이프라인 (`app/pipelines/daily_pipeline.py`)

**기능:** EmotionLog 데이터를 매일 자정 자동 요약

**수행 과정:**
1️⃣ EmotionLog → 감정별 비율 계산  
2️⃣ DailySummary 테이블에 저장  
3️⃣ 실패 시 logging.error 기록

**이유:** 자동화된 데이터 집계로 실시간 대시보드 업데이트 가능

---

## 🧱 데이터베이스 모델 구조

| 모델 | 설명 |
|------|------|
| User | 사용자 정보, JWT 인증용 |
| EmotionLog | 피드백 감정 결과 저장 |
| DailySummary | 하루 단위 감정 요약 |
| FeedbackEmbedding | 벡터 임베딩 메타데이터 (RAG) |

---

## 🐳 Docker 구성

* `Dockerfile` → FastAPI 앱 컨테이너
* `docker-compose.yml` → app + db (PostgreSQL) 통합 실행
* `.env` 파일로 환경 변수 분리

---

## 🧭 시스템 흐름 요약
```mermaid
flowchart LR
A[사용자 피드백 입력] --> B[Emotion API 호출]
B --> C[GPT 감정 분석 + 근거 생성]
C --> D[EmotionLog 저장 + ChromaDB 임베딩]
D --> E[RAG 검색 시 근거 데이터 제공]
E --> F[결과 대시보드 시각화]
F --> G[APScheduler 자동 요약]
```

---

## 🧩 기술적 선택 이유

| 기술 | 선택 이유 |
|------|-----------|
| FastAPI | 비동기 + 간결한 라우팅 구조 |
| SQLAlchemy | ORM + 확장성 |
| OpenAI GPT | 고품질 감정 분류 |
| ChromaDB | 가볍고 빠른 벡터 DB |
| APScheduler | 간단한 스케줄 기반 ETL |
| Docker | 재현 가능한 환경 구성 |