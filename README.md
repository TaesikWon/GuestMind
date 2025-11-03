# 🏨 SoulStay

**AI로 고객의 감정을 읽다 — 감정 분석 기반 호텔 경험 관리 플랫폼**

---

## 💭 프로젝트 개발 동기

호텔 식음료 및 객실 업무를 경험하며 다양한 고객과 수많은 컴플레인 상황을 마주했습니다.

현장에서 느낀 점은:
- **고객 감정의 정확한 파악**이 효과적인 대응의 시작이다
- 고객이 감정적 표현 없이도 원하는 바를 명확히 전달할 수 있어야 한다
- 직원은 불필요한 스트레스 없이 본질적인 문제 해결에 집중할 수 있어야 한다

**SoulStay는 이러한 현장 경험에서 출발했습니다.**

AI를 통해 고객 피드백의 감정을 자동 분석하고, 유사 사례를 빠르게 검색하여 호텔 운영자와 직원이 고객을 더 깊이 이해하고 효과적으로 대응할 수 있도록 돕습니다.

---

## 📖 개요

SoulStay는 고객 피드백을 AI로 분석하여 호텔 운영자가 고객 감정을 직관적으로 파악하고 서비스를 개선할 수 있도록 지원하는 플랫폼입니다.

**Hugging Face 기반 한국어 감정 분석 모델**과 **LangChain RAG 시스템**을 결합하여 감정을 분류하고, 유사한 과거 피드백을 참고하여 맥락 있는 답변을 생성합니다. ChromaDB 벡터 스토어를 활용한 의미 기반 검색으로 트렌드 분석과 감정 통계 시각화를 제공합니다.

---

## 💡 핵심 기능

| 기능 | 설명 |
|------|------|
| 💬 **감정 분석** | Hugging Face BERT 모델로 긍정/부정/중립 자동 분류 |
| 🤖 **AI 챗봇** | LangChain 기반 RAG로 유사 사례를 참고한 맥락 있는 답변 생성 |
| 🧠 **벡터 검색** | ChromaDB + OpenAI Embeddings 기반 의미론적 유사 피드백 검색 |
| 👤 **회원 시스템** | JWT 기반 로그인/회원가입 (쿠키 저장) |
| 📚 **데이터 관리** | PostgreSQL + SQLAlchemy로 감정 로그 및 사용자 데이터 영구 저장 |
| 📊 **자동 요약** | APScheduler 기반 일일 감정 통계 자동 생성 |
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

## 🏗️ 시스템 아키텍처
```
┌─────────────┐
│   사용자     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│          FastAPI Server             │
│  ┌──────────────────────────────┐  │
│  │      Chat API                │  │
│  └────┬──────────────┬──────────┘  │
│       │              │              │
│       ▼              ▼              │
│  ┌─────────┐   ┌──────────────┐   │
│  │ Emotion │   │ LangChain    │   │
│  │ Service │   │ RAG Service  │   │
│  │ (BERT)  │   └──────┬───────┘   │
│  └─────────┘          │            │
│                       ▼            │
│              ┌─────────────────┐  │
│              │   ChromaDB      │  │
│              │  (Vector Store) │  │
│              └─────────────────┘  │
│                                    │
│              ┌─────────────────┐  │
│              │   PostgreSQL    │  │
│              │   (User Data)   │  │
│              └─────────────────┘  │
└────────────────────────────────────┘
```

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
SECRET_KEY=your-secret-key-here
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

👉 브라우저에서: http://127.0.0.1:8000

---

## 🗂️ 프로젝트 구조
```
SoulStay/
├── app/
│   ├── api/
│   │   └── chat_api.py          # 챗봇 통합 API
│   ├── routes/
│   │   ├── auth.py              # 회원가입/로그인/로그아웃
│   │   ├── chat.py              # 채팅 UI 및 API
│   │   ├── emotion.py           # 감정 분석 API
│   │   ├── rag.py               # RAG 검색
│   │   └── user.py              # 사용자 정보
│   ├── services/
│   │   ├── emotion_service.py   # Hugging Face 감정 분석
│   │   ├── langchain_rag_service.py  # LangChain RAG 시스템
│   │   ├── summary_service.py   # 일일 요약
│   │   ├── user_service.py      # 사용자 관리
│   │   └── token_service.py     # JWT 토큰
│   ├── models/
│   │   ├── user.py
│   │   ├── emotion_log.py
│   │   └── daily_summary.py
│   ├── core/
│   │   └── auth_utils.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── chat.html            # 챗봇 UI
│   │   ├── emotion.html
│   │   ├── login.html
│   │   └── register.html
│   ├── static/
│   │   └── style.css            # 앤티크 호텔 디자인
│   ├── config.py
│   ├── database.py
│   └── vectorstore.py
├── data/
│   └── feedback_samples.csv     # 50개 샘플 피드백
├── tests/
│   └── test_rag.py              # RAG 시스템 테스트
├── main.py
├── train_emotion_model.py       # 감정 분석 모델 학습 스크립트
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── logs/
```

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

## 🤖 AI 시스템 상세

### 감정 분석 (Emotion Analysis)
- **모델**: `WhitePeak/bert-base-cased-Korean-sentiment`
- **출력**: positive / negative / neutral
- **처리**: Hugging Face Transformers pipeline

### RAG 시스템 (Retrieval-Augmented Generation)
- **Framework**: LangChain (LCEL 방식)
- **Vector Store**: ChromaDB
- **Embedding**: OpenAI text-embedding-3-small (1536 차원)
- **LLM**: OpenAI GPT-4o-mini
- **프로세스**:
  1. 사용자 입력 → 감정 분석
  2. 벡터 검색 → 유사 피드백 3개 추출
  3. 프롬프트 템플릿 → 맥락 제공
  4. LLM → 개인화된 답변 생성

---

## 🧾 로그 확인

로그 파일은 `logs/` 디렉터리에 자동 생성됩니다.

FastAPI 라우트 호출 시 분석 결과와 DB 저장 상태가 기록됩니다.

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

- **Hugging Face**: 한국어 감정 분석 모델 제공
- **LangChain**: RAG 프레임워크
- **OpenAI**: GPT-4o-mini & Embeddings API
- **ChromaDB**: 벡터 데이터베이스