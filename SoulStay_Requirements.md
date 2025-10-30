# 📘 SoulStay 요구사항 정의서

---

## 1️⃣ 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **프로젝트명** | SoulStay |
| **한줄 소개** | AI 기반 감정 분석을 활용한 호텔 고객 경험 관리 플랫폼 |
| **개발 목적** | 고객 피드백의 감정 상태를 자동 분석하고, 유사 사례 검색 및 통계 요약을 통해 고객 만족도 개선에 기여 |
| **기술 스택** | FastAPI, PostgreSQL, SQLAlchemy, OpenAI GPT-4o-mini, LangChain, ChromaDB, APScheduler, Jinja2 |

---

## 2️⃣ 시스템 개요

SoulStay는 호텔 고객 피드백(리뷰, 설문 등)을 입력받아  
**AI 모델(OpenAI GPT)**을 통해 감정 분석을 수행하고,  
분석 결과를 **데이터베이스와 벡터스토어**에 저장하여  
**RAG 기반 유사 피드백 검색** 및 **일일 요약 자동화** 기능을 제공합니다.

---

## 3️⃣ 주요 기능 요약

| 구분 | 기능명 | 설명 |
|------|--------|------|
| **회원 관리** | 회원가입 / 로그인 | 사용자 계정 생성 및 인증 처리 (JWT 예정) |
|  | 비밀번호 암호화 | bcrypt 기반 해시 저장 |
| **감정 분석** | 피드백 감정 분석 | OpenAI API를 통해 긍정/부정/중립 감정 분류 |
|  | 감정 근거 추출 | LLM이 감정 근거(reason) 필드를 함께 반환 |
| **데이터 저장** | 감정 로그 저장 | emotion_logs 테이블에 감정 결과 저장 |
|  | 사용자별 로그 연동 | user_id 외래키로 연결 |
| **RAG 검색** | 유사 피드백 검색 | ChromaDB + LangChain 기반 벡터 검색 |
| **일일 요약** | 자동 감정 통계 | APScheduler가 매일 자정에 실행, daily_summaries 테이블에 저장 |
| **UI/UX** | 반응형 웹 | Jinja2 + Bootstrap5로 간단한 웹 인터페이스 제공 |
| **로깅 시스템** | 로그 파일 저장 | 모든 분석 결과 및 오류를 /logs 폴더에 저장 |

---

## 4️⃣ 비기능 요구사항

| 항목 | 요구사항 |
|------|----------|
| **성능** | 1초 이내 감정 분석 응답 (LLM 호출 제외 시) |
| **보안** | 사용자 비밀번호 해시 저장 (bcrypt) |
| **데이터 무결성** | FK 제약조건(user_id)으로 유효한 사용자만 로그 등록 가능 |
| **신뢰성** | Scheduler 실패 시 자동 예외 처리 및 로그 기록 |
| **확장성** | LangChain RAG 구조로 LLM/Embedding 교체 용이 |
| **유지보수성** | 모듈 단위 구조 (routes, services, models) 유지 |

---

## 5️⃣ 데이터베이스 설계 요약

### 🧩 users 테이블

| 필드명 | 타입 | 설명 |
|--------|------|------|
| **id** | SERIAL (PK) | 사용자 고유 ID |
| **username** | VARCHAR | 로그인 ID |
| **password_hash** | VARCHAR | 암호화된 비밀번호 |
| **created_at** | TIMESTAMP | 생성 시각 |
| **last_login** | TIMESTAMP | 마지막 로그인 시각 |

### 🧩 emotion_logs 테이블

| 필드명 | 타입 | 설명 |
|--------|------|------|
| **id** | SERIAL (PK) | 로그 ID |
| **user_id** | INTEGER (FK) | 작성자 ID |
| **text** | VARCHAR | 피드백 내용 |
| **emotion** | VARCHAR | 감정 결과 |
| **reason** | VARCHAR | 감정 근거 |
| **created_at** | TIMESTAMP | 분석 시각 |

### 🧩 daily_summaries 테이블

| 필드명 | 타입 | 설명 |
|--------|------|------|
| **id** | SERIAL (PK) | 요약 ID |
| **user_id** | INTEGER (FK) | 사용자 ID |
| **date** | DATE | 요약 날짜 |
| **total_feedback** | INTEGER | 피드백 수 |
| **positive_ratio** | FLOAT | 긍정 비율 |
| **negative_ratio** | FLOAT | 부정 비율 |
| **neutral_ratio** | FLOAT | 중립 비율 |
| **created_at** | TIMESTAMP | 요약 시각 |

---

## 6️⃣ 시스템 아키텍처
```
사용자 → FastAPI → EmotionService → OpenAI GPT-4o-mini
                              ↓
                      EmotionLog (PostgreSQL)
                              ↓
                     ChromaDB (Vector Store)
                              ↓
                     APScheduler (일일 요약)
```

---

## 7️⃣ 향후 개선 계획

| 단계 | 개선 내용 |
|------|-----------|
| **Phase 1** | JWT 인증 완성 및 Refresh Token 추가 |
| **Phase 2** | 감정 통계 대시보드 시각화 (Chart.js / Plotly) |
| **Phase 3** | Docker 컨테이너화 및 AWS 배포 |
| **Phase 4** | 챗봇 기능 확장 (고객 응대 AI 시나리오) |

---

## 8️⃣ 문서 메타정보

| 항목 | 내용 |
|------|------|
| **작성자** | Taesik Won |
| **버전** | 1.0 |
| **작성일** | 2025-10-30 |
| **문서 목적** | SoulStay 프로젝트의 기능 및 시스템 요구사항 명세 |

---

## ✅ 프로젝트 정의

**SoulStay**는 호텔 산업의 고객 경험 관리를 혁신하기 위한 AI 기반 플랫폼으로,  
감정 분석과 RAG 기술을 활용하여 **고객 피드백을 자동으로 분석하고 인사이트를 제공**하는  
**차세대 호텔 고객 경험 관리 시스템**입니다.