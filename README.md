# SoulStay 🏨

**AI로 고객의 감정을 읽다 — 호텔 경험 관리 서비스**

---

## 📖 소개

SoulStay는 호텔 고객의 피드백을 AI로 실시간 감정 분석하여 경영자가 고객 경험을 직관적으로 파악하고 개선할 수 있도록 돕는 웹 서비스입니다.

### 💡 핵심 가치

- 📊 **데이터 기반 의사결정**: 고객 피드백의 감정 트렌드를 한눈에 파악
- 🔍 **인사이트 발견**: 유사 피드백 검색으로 반복되는 이슈 식별
- ⚡ **실시간 분석**: 즉각적인 감정 분류 및 데이터베이스 저장

---

## ✨ 주요 기능

| 기능 | 설명 |
|------|------|
| 💬 감정 분석 | OpenAI GPT-4o-mini를 활용한 긍정/부정/중립 분류 및 근거 제공 |
| 🧠 RAG 검색 | ChromaDB 벡터 데이터베이스 기반의 유사 피드백 검색 |
| 👤 사용자 관리 | 회원가입/로그인 시스템 (JWT 인증 예정) |
| 📊 데이터 로깅 | SQLite + SQLAlchemy 기반 분석 결과 영구 저장 |
| 🎨 반응형 UI | Jinja2 + Bootstrap 5 기반 직관적 웹 인터페이스 |

---

## 🚀 빠른 시작

### ✅ 사전 요구사항

- Python 3.8+
- 유효한 OpenAI API Key

### ⚙️ 설치
```bash
# 저장소 클론
git clone https://github.com/TaesikWon/SoulStay.git
cd SoulStay

# 가상환경 생성 및 활성화
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 🧩 환경 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 입력하세요:
```env
OPENAI_API_KEY=sk-your-api-key-here
DATABASE_URL=sqlite:///./soulstay.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CHROMA_DB_PATH=app/chroma_db
APP_ENV=development
```

### ▶️ 실행
```bash
uvicorn main:app --reload
```

브라우저에서 http://127.0.0.1:8000/emotion 으로 접속하세요.

---

## 🏗️ 프로젝트 구조
```
SoulStay/
├── app/
│   ├── config.py              # 환경 설정
│   ├── database.py            # DB 연결 관리
│   ├── models/                # 데이터 모델
│   ├── routes/                # API 엔드포인트
│   ├── services/              # 비즈니스 로직
│   ├── static/                # CSS, JS 파일
│   ├── templates/             # HTML 템플릿
│   └── utils/                 # 유틸리티 함수
├── main.py                    # 애플리케이션 진입점
├── requirements.txt
├── .env
└── soulstay.db
```

---

## 🛠️ 기술 스택

| 영역 | 사용 기술 |
|------|-----------|
| **Backend** | FastAPI, SQLAlchemy, SQLite |
| **AI / NLP** | OpenAI GPT-4o-mini, text-embedding-3-small |
| **Vector DB** | ChromaDB |
| **Frontend** | Jinja2, Bootstrap 5, Custom CSS |
| **Security** | python-dotenv, JWT (예정) |

---

## 🗓️ 로드맵

### 📍 Phase 1 — 현재

- [x] 기본 감정 분석 API
- [x] ChromaDB 기반 RAG 검색
- [x] SQLite 데이터 로깅
- [x] 반응형 웹 UI 구축

### 🔜 Phase 2 — 진행 예정

- [ ] JWT 기반 인증 시스템
- [ ] 감정 분석 대시보드 (차트 시각화)
- [ ] 입력 검증 및 예외 처리 강화
- [ ] API 문서 자동화 (Swagger UI)

### 🚀 Phase 3 — 계획

- [ ] Docker 컨테이너화
- [ ] Render / Railway 배포
- [ ] 실시간 알림 기능
- [ ] 다국어 지원

---

## 👨‍💻 개발자

**Taesik Won**

- Backend & AI Developer
- Focus: Generative AI, NLP, Data Engineering
- GitHub: [@TaesikWon](https://github.com/TaesikWon)

---

## 📄 라이선스

Copyright © 2025 Taesik Won. All rights reserved.

이 프로젝트의 소스코드는 **학습 및 참고 목적으로 공개**되었습니다.  
무단 복제, 수정, 재배포 및 상업적 이용은 금지됩니다.