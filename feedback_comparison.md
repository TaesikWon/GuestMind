# 🏨 SoulStay

**AI로 고객의 감정을 읽다 — 감정 분석 기반 호텔 경험 관리 플랫폼**

---

## 💭 프로젝트 제작 동기

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

**Hugging Face 기반 한국어 감정 분석 모델**과 **LangChain RAG 시스템**을 결합하여 감정을 분류하고, 유사한 과거 피드백을 참고하여 맥락 있는 답변을 생성합니다. 또한 **인수인계 자동 요약 기능**을 통해 직원 간의 교대 시 정보를 효율적으로 전달할 수 있습니다.

---

## 💡 핵심 기능

| 기능 | 설명 |
|------|------|
| 💬 **감정 분석** | Hugging Face BERT 모델로 긍정/부정/중립 자동 분류 |
| 🤖 **AI 챗봇** | LangChain 기반 RAG로 유사 사례를 참고한 맥락 있는 답변 생성 |
| 🧠 **벡터 검색** | ChromaDB + OpenAI Embeddings 기반 의미론적 유사 피드백 검색 |
| 👤 **회원 시스템** | JWT 기반 로그인/회원가입 (쿠키 저장) |
| 📚 **데이터 관리** | PostgreSQL + SQLAlchemy로 감정 로그 및 사용자 데이터 영구 저장 |
| 📊 **자동 요약** | APScheduler 기반 일일 감정 통계 및 인수인계 요약 자동 생성 |
| 🎨 **프론트엔드** | Jinja2 + Bootstrap 기반 앤티크 호텔 디자인 UI |
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

## 🧩 기획 및 시스템 설계

### 🎯 1️⃣ 사용자 여정 (User Flow)

SoulStay의 주요 사용자는 **호텔 직원**입니다. 그들은 고객 피드백을 바탕으로 서비스 품질을 개선하고, 다음 근무자에게 효율적으로 인수인계하기 위해 이 시스템을 사용합니다.

**예시 시나리오: 🏨 호텔 식음료팀 근무자**

1. **출근 시:** 전날 고객 피드백의 자동 감정 요약 확인
2. **근무 중:** 실시간 신규 피드백의 감정 분석 결과 조회
3. **퇴근 전:** AI가 생성한 인수인계 요약 문서를 검토 및 저장

✅ 이렇게 SoulStay는 **"감정 기반 인수인계 자동화"**를 중심으로 호텔 현장의 일상적인 운영 흐름에 자연스럽게 녹아듭니다.

---

### 🧠 2️⃣ 인수인계 자동 요약 프로세스

SoulStay의 핵심 가치는 **AI가 인수인계 문서를 자동으로 정리**해주는 기능입니다. 다음은 인수인계 자동화의 전체 흐름입니다.
```
[고객 피드백 수집]
        ↓
[감정 분석 (BERT)]
        ↓
[유사 피드백 검색 (RAG)]
        ↓
[GPT 요약 및 응답 생성]
        ↓
[자동 인수인계 문서 생성]
        ↓
[다음 근무자 확인 및 검토]
```

💬 이 과정을 통해 **고객 감정의 변화, 주요 불만사항, 긍정 피드백**을 직원이 빠르게 이해하고 자연스럽게 업무를 이어갈 수 있습니다.

---

### 🔄 3️⃣ 데이터 흐름 설계 (Data Flow)

데이터는 다음의 경로로 시스템 내에서 처리됩니다.
```
고객 피드백 (Text)
   ↓
감정 분석 서비스 → 감정 결과 저장 (PostgreSQL)
   ↓
벡터화 (OpenAI Embedding)
   ↓
유사 문서 검색 (ChromaDB)
   ↓
GPT 요약 → 인수인계 자동 문서 생성
```

💾 **PostgreSQL**은 구조화된 감정 로그를 저장하고, **ChromaDB**는 의미론적 유사도 기반 검색을 담당합니다.

---

### ⚙️ 4️⃣ 운영 및 유지보수 설계

실무 환경에서도 안정적으로 작동하도록 자동화와 모니터링 로직을 포함하고 있습니다.

| 항목 | 설명 |
|------|------|
| 🕛 **APScheduler** | 매일 0시에 자동 감정 요약 생성 |
| 💽 **벡터DB 백업** | 주 1회 자동 백업 |
| 🧩 **Health Check** | `/health/db` 엔드포인트로 DB 연결 상태 점검 |
| 🧾 **로깅 시스템** | `logs/` 폴더에 자동 로그 기록 및 주기적 정리 |

📈 운영 효율성과 안정성을 고려해 **"예방적 유지보수" 구조**로 설계되었습니다.

---

### 🚀 5️⃣ 리스크 및 향후 확장 기획

| 구분 | 내용 |
|------|------|
| **MVP 범위** | 감정 분석 + 유사 사례 검색 + 인수인계 자동 요약 |
| **확장 가능성** | 실시간 음성 피드백 입력, 다국어 감정 분석, 관리자 대시보드 |

🧭 MVP는 **"직원 인수인계 자동화"**에 집중하고, 확장 버전은 **"운영 효율화 및 실시간 분석"**으로 발전시킬 수 있습니다.

---

## 🧠 데이터베이스 구조

### 📋 users 테이블

| 컬럼 | 타입 | 제약조건 |
|------|------|----------|
| id | SERIAL | PK |
| username | VARCHAR | NOT NULL, UNIQUE |
| password_hash | VARCHAR | NOT NULL |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| last_login | TIMESTAMP | NULL |

### 📋 emotion_logs 테이블

| 컬럼 | 타입 | 제약조건 |
|------|------|----------|
| id | SERIAL | PK |
| user_id | INTEGER | FK (users.id) |
| text | VARCHAR | NOT NULL |
| emotion | VARCHAR | NOT NULL |
| reason | VARCHAR | NULL |
| created_at | TIMESTAMP | DEFAULT now() |

### 📋 daily_summaries 테이블

| 컬럼 | 타입 | 제약조건 |
|------|------|----------|
| id | SERIAL | PK |
| user_id | INTEGER | FK (users.id) |
| date | DATE | NOT NULL |
| total_feedback | INTEGER | NOT NULL |
| positive_ratio | FLOAT | NOT NULL |
| negative_ratio | FLOAT | NOT NULL |
| neutral_ratio | FLOAT | NOT NULL |
| created_at | TIMESTAMP | DEFAULT now() |

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