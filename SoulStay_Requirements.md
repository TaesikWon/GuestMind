# 📋 SoulStay 기능 요구사항 명세서

| 요구사항 ID | 요구사항명 | 기능 ID | 기능명 | 상세 설명 | 비고 |
|------------|-----------|---------|--------|-----------|------|
| **ACC01** | 계정 관리 | FBF-01 | 회원가입 및 로그인 | JWT 기반 사용자 인증 및 토큰 발급 기능 구현 | FastAPI, PostgreSQL |
|  |  | FBF-02 | 비밀번호 암호화 | bcrypt 해시 기반 암호 저장 | 보안 강화 |
|  |  | FBF-03 | 로그인 상태 유지 | Access/Refresh Token 구조를 통해 지속 로그인 유지 | Refresh Token 기능 예정 |
|  |  | FBF-04 | 회원 탈퇴 | 사용자 정보 및 연관 로그 삭제 |  |
| **EMO01** | 감정 분석 | FBF-05 | 감정 분석 API | OpenAI GPT-4o-mini를 이용해 고객 피드백의 감정(긍정/부정/중립) 분류 | OpenAI API |
|  |  | FBF-06 | 감정 근거 추출 | LLM이 감정 결과와 함께 근거(reason) 반환 | RAG와 연동 |
|  |  | FBF-07 | 감정 로그 저장 | emotion_logs 테이블에 감정 결과 저장 | user_id FK 연결 |
| **RAG01** | 유사 피드백 검색 | FBF-08 | 벡터 임베딩 저장 | 고객 피드백 데이터를 ChromaDB에 벡터 형태로 저장 | LangChain, ChromaDB |
|  |  | FBF-09 | 유사 피드백 검색 | 입력 피드백과 유사한 감정 로그 검색 및 반환 | Semantic Search |
| **SCH01** | 자동 요약 | FBF-10 | 일일 감정 요약 | APScheduler를 이용해 매일 자정 감정 통계 자동 요약 | daily_summaries 테이블 |
|  |  | FBF-11 | 예외 처리 및 로깅 | 스케줄 실행 오류 발생 시 예외 처리 및 로그 기록 | Log 파일 관리 |
| **DAS01** | 감정 통계 대시보드 | FFH-01 | 대시보드 UI 구성 | Jinja2 + Chart.js 기반 감정 통계 시각화 페이지 구현 | 관리자용 |
|  |  | FBF-12 | 통계 데이터 API | `/dashboard/data` 엔드포인트에서 기간별 감정 통계 제공 | JSON 반환 |
|  |  | FBF-13 | 통계 자동 갱신 | APScheduler로 일정 주기마다 요약 데이터 최신화 |  |
| **USR01** | 사용자 로그 관리 | FBF-14 | 사용자별 로그 조회 | 사용자 ID 기준으로 감정 분석 및 검색 로그 조회 | 관리자 접근 제한 |
|  |  | FBF-15 | 로그 백업 | 로그 파일 자동 백업 및 보관 | /logs 디렉토리 |
| **DBS01** | 데이터베이스 | FBF-16 | 사용자 DB | users, emotion_logs, daily_summaries 테이블 설계 및 구축 | PostgreSQL |
|  |  | FBF-17 | 외래키 제약조건 | user_id FK를 통한 데이터 무결성 보장 |  |
| **NET01** | 네트워크 및 서버 | FBN-01 | HTTPS 통신 | SSL 인증서를 통한 통신 암호화 | 보안 강화 |
|  |  | FBN-02 | 요청 대기 처리 | 서버 과부하 방지를 위한 비동기 처리 및 timeout 설정 | Gunicorn + uvicorn |
|  |  | FBN-03 | 로드 밸런싱 | 다중 워커 기반 부하 분산 처리 |  |
| **SYS01** | 시스템 구조 | FAS-01 | 모듈 단위 구조화 | routes / services / models 폴더 구조로 유지보수성 향상 |  |
|  |  | FAS-02 | 로깅 시스템 | 시스템 로그를 /logs 디렉토리에 파일 단위로 기록 |  |
| **EXT01** | UI 및 프론트엔드 | FFH-02 | 반응형 웹 UI | Bootstrap5 기반 반응형 인터페이스 구현 |  |
|  |  | FFH-03 | 감정 결과 시각 표시 | 분석 결과에 따라 긍정/부정/중립 색상 구분 표시 | UX 강화 |
| **DEV01** | 개발 환경 및 배포 | FAD-01 | Docker 컨테이너화 | FastAPI, DB, Scheduler 통합 Docker 구성 |  |
|  |  | FAD-02 | AWS 배포 | EC2 + RDS + S3 기반 인프라 구축 | 향후 계획 |
| **BOT01** | 챗봇 기능(예정) | FAC-01 | 고객 응대 챗봇 | 감정 기반 대화 모델로 고객 피드백 대응 | Phase 4 예정 |