# 🏨 SoulStay

**AI로 고객의 감정을 읽다 — 감정 분석 기반 호텔 경험 관리 플랫폼**

---

## 💭 프로젝트 개발 목적

호텔 식음료 및 객실 업무를 경험하며 다양한 고객과 수많은 컴플레인 상황을 마주했습니다.

현장에서 느낀 점은:
- **고객 감정의 정확한 파악**이 효과적인 대응의 시작이다
- 고객이 감정적 표현 없이도 원하는 바를 명확히 전달할 수 있어야 한다
- 직원은 불필요한 스트레스 없이 본질적인 문제 해결에 집중할 수 있어야 한다

**SoulStay는 이러한 현장 경험에서 출발했습니다.**

AI를 통해 고객 피드백의 감정을 자동 분석하고, 유사 사례를 빠르게 검색하여 호텔 운영자와 직원이 고객을 더 깊이 이해하고 효과적으로 대응할 수 있도록 돕습니다.

---

## 📖 프로젝트 개요

SoulStay는 고객 피드백을 AI로 분석하여 호텔 운영자가 고객 감정을 직관적으로 파악하고 서비스를 개선할 수 있도록 지원하는 플랫폼입니다.

**Hugging Face 기반 한국어 감정 분석 모델**과 **LangChain RAG 시스템**을 결합하여 감정을 분류하고, 유사한 과거 피드백을 참고하여 맥락 있는 답변을 생성합니다.

또한, 근무 교대 시 자동 생성되는 **인수인계 요약 기능**을 통해 이전 근무자의 응대 내용과 감정 상태를 자연스럽게 이어받을 수 있습니다.

---

## 💡 핵심 기능

| 기능 | 설명 |
|------|------|
| 💬 **감정 분석** | Hugging Face BERT 모델로 긍정/부정/중립 자동 분류 |
| 🤖 **AI 챗봇** | LangChain 기반 RAG로 유사 사례를 참고한 맥락 있는 답변 생성 |
| 🧠 **벡터 검색** | ChromaDB + OpenAI Embeddings 기반 의미론적 유사 피드백 검색 |
| 👥 **인수인계 자동 요약** | GPT 모델이 감정 요약 + 업무 전달문 자동 생성 |
| 👤 **회원 시스템** | JWT 기반 로그인/회원가입 (쿠키 저장) |
| 📚 **데이터 관리** | PostgreSQL + SQLAlchemy로 감정 로그 및 사용자 데이터 저장 |
| 📊 **감정 통계 시각화** | APScheduler 기반 일일 감정 통계 및 트렌드 리포트 자동 생성 |
| 🧾 **로깅 시스템** | Python logging 모듈 기반 상세 로그 기록 |

---

## ⚙️ 기술 스택

| 분야 | 사용 기술 |
|------|----------|
| **Backend** | FastAPI, SQLAlchemy, PostgreSQL, Alembic |
| **감정 분석** | Hugging Face Transformers (WhitePeak/bert-base-cased-Korean-sentiment) |
| **LLM** | OpenAI GPT-4o-mini |
| **RAG Framework** | LangChain (LCEL), LangChain-OpenAI, LangChain-Chroma |
| **Vector DB** | ChromaDB |
| **Embedding** | OpenAI text-embedding-3-small |
| **Auth** | JWT (Access + Refresh Token), python-jose, bcrypt |
| **Scheduler** | APScheduler |
| **Frontend** | Jinja2, Bootstrap 5, Custom CSS |
| **Config** | python-dotenv, pydantic-settings |
| **Logging** | Python logging 모듈 |

---

## 🧭 사용자 시나리오 예시

### 🏨 호텔 객실팀 근무자

1. **출근 시:** 전날 자동 생성된 인수인계 요약 확인
2. **근무 중:** 신규 고객 피드백 감정 분석 결과 실시간 확인
3. **퇴근 전:** 자동 생성된 인수인계 문서 검토 후 코멘트 추가

➡ SoulStay는 현장 직원이 고객 감정 데이터를 자연스럽게 공유하고 효율적으로 인수인계할 수 있는 **AI 기반 도우미**입니다.

---

## 🧩 시스템 아키텍처
```
┌──────────────┐
│   사용자      │
└──────┬───────┘
       │
       ▼
┌────────────────────────────────────┐
│          FastAPI Server            │
│  ┌─────────────────────────────┐  │
│  │         Chat API            │  │
│  └──────────┬────────────┬─────┘  │
│             │            │         │
│             ▼            ▼         │
│  ┌────────────┐   ┌────────────┐  │
│  │  Emotion   │   │    RAG     │  │
│  │  Service   │   │  Service   │  │
│  │  (BERT)    │   │ (ChromaDB) │  │
│  └──────┬─────┘   └──────┬────┘  │
│         │                │         │
│         ▼                ▼         │
│     감정분석 결과     유사문서검색 │
│         │                │         │
│         └──────┬─────────┘         │
│                ▼                   │
│       ┌────────────────────┐       │
│       │ Response Generator │       │
│       │  (OpenAI GPT API)  │       │
│       └────────────────────┘       │
│                                    │
│ ┌────────────────┐ ┌────────────┐ │
│ │PostgreSQL(User)│ │ChromaDB    │ │
│ └────────────────┘ └────────────┘ │
└────────────────────────────────────┘
```

---

## 📊 인텔리전트 호텔 운영 고도화 (향후 확장 계획)

SoulStay는 단순한 감정 분석을 넘어 **호텔 운영 효율화와 협업 강화**를 목표로 발전할 수 있습니다.

### 1️⃣ KPI 기반 운영 대시보드
- 감정 로그 데이터를 KPI 지표로 시각화
- **주요 지표:** 긍정/부정 피드백 비율, 피드백 수, 인수인계 완료율 등
- 관리자용 `/dashboard` 페이지에서 실시간 운영 현황 모니터링

### 2️⃣ 감정 트렌드 분석 리포트
- APScheduler를 확장해 주간/월간 단위 리포트 자동 생성
- GPT 요약 기반으로 긍정/부정 키워드 트렌드 자동 파악
- 관리자에게 이메일 또는 화면 리포트로 전달

### 3️⃣ 인수인계 확인 로그 + 협업 기록
- 다음 근무자의 인수인계 문서 열람 및 확인 로그
- 코멘트 기능으로 추가 지시나 피드백 공유
- GPT 자동 요약과 사람의 수정 이력을 통합 관리

---

## 🔄 확장 로드맵 요약

| 단계 | 목표 | 주요 기능 |
|------|------|-----------|
| **MVP (현재)** | 감정 분석 + 인수인계 자동화 | 감정 분석, GPT 요약, 유사 피드백 검색 |
| **1차 확장** | 데이터 활용 강화 | KPI 대시보드, 감정 트렌드 리포트 |
| **2차 확장** | 협업 및 운영 고도화 | 인수인계 확인 로그, 협업 코멘트 기능 |

✅ 확장 기능들은 기존 **FastAPI + PostgreSQL + ChromaDB** 구조를 유지하면서 프론트엔드(Jinja2) 및 DB 스키마 확장으로 구현 가능합니다.

---

## 🚀 실행 방법

### 1️⃣ 환경 구성
```bash
git clone https://github.com/TaesikWon/SoulStay.git
cd SoulStay
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2️⃣ 환경 변수 설정

프로젝트 루트에 `.env` 파일 생성:
```env
# OpenAI API
OPENAI_API_KEY=sk-your-api-key

# Database
DATABASE_URL=postgresql+psycopg2://postgres:yourpassword@localhost/soulstay

# Vector Store
CHROMA_DB_PATH=./app/services/embeddings

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# Environment
ENVIRONMENT=development
```

### 3️⃣ 데이터베이스 초기화
```bash
# PostgreSQL 데이터베이스 생성
createdb soulstay

# 서버 첫 실행 시 테이블 자동 생성
python main.py
```

### 4️⃣ RAG 벡터 스토어 초기화
```bash
# 피드백 샘플 데이터를 ChromaDB에 로드
python tests/test_rag.py
```

### 5️⃣ 서버 실행
```bash
python main.py
# 또는
uvicorn main:app --reload
```

📍 브라우저 접속 → http://127.0.0.1:8000

---

## 👤 개발자

**Taesik Won**

- Backend & AI Developer
- Focus: Generative AI, NLP, RAG Systems
- GitHub: [@TaesikWon](https://github.com/TaesikWon)

---

## 📜 라이선스

본 프로젝트는 학습 및 연구 목적의 오픈소스 예시이며, 무단 상업적 이용 및 재배포를 금합니다.

---

## 🙏 Acknowledgments

- 🤗 **Hugging Face** — 한국어 감정 분석 모델 제공
- 🧩 **LangChain** — RAG 프레임워크
- 💬 **OpenAI** — GPT-4o-mini & Embeddings API
- 🧱 **ChromaDB** — 벡터 데이터베이스