# AI Code Analysis Service - 문서 목록

## 📂 문서 구조

### 📊 POC 테스트 (poc-tests/)
날짜별 POC 테스트 결과 및 분석 로그

#### 2026-01-08
- **[POC_TEST_RESULT.md](./poc-tests/2026-01-08/POC_TEST_RESULT.md)** - POC 테스트 종합 보고서
  - 검증된 기능 (Git, 그룹핑, AI 분석, 비동기 처리)
  - 발견된 이슈 (LLM 모델 한계, 성능)
  - 개선 방안 및 다음 단계

- **[AI_ANALYSIS_LOGS.md](./poc-tests/2026-01-08/AI_ANALYSIS_LOGS.md)** - AI Map 분석 상세 로그
  - 11개 모듈 분석 결과
  - 기술 스택 및 코드 품질 평가
  - 분석 통계

- **[GEMINI_INTEGRATION_GUIDE.md](./poc-tests/2026-01-08/GEMINI_INTEGRATION_GUIDE.md)** - Gemini API 통합 가이드
  - Ollama vs Gemini 비교
  - JSON Mode 구현 방법
  - 비용 계산 및 성능 예측

---

### 🏗️ 아키텍처 (architecture/)
시스템 설계 및 아키텍처 문서

- **[AI_archi.md](./architecture/AI_archi.md)** - AI Code Analysis Service 전체 아키텍처
  - 시스템 개요 (Spring + FastAPI)
  - Resource Update Pattern
  - API 인터페이스 명세
  - Map-Reduce 파이프라인 상세 설계
  - 동시성 제어 전략

---

### 📖 가이드 (guides/)
설치, 배포, 사용법 가이드

- **[DOCKER_GUIDE.md](./guides/DOCKER_GUIDE.md)** - Docker 사용 가이드 (Ollama Only)
  - Ollama Docker 관리
  - 모델 다운로드 및 관리
  - M4 Pro GPU 가속
  - 트러블슈팅

---

### 🔧 개발 (development/)
개발 관련 문서 (향후 추가 예정)

- CHANGELOG.md (예정)
- CONTRIBUTING.md (예정)
- API_REFERENCE.md (예정)

---

## 📌 빠른 링크

### 처음 시작하는 경우
1. [아키텍처 문서](./architecture/AI_archi.md) - 전체 시스템 이해
2. [Docker 가이드](./guides/DOCKER_GUIDE.md) - Ollama 설정
3. [프로젝트 README](../README.md) - 설치 및 실행

### POC 결과 확인
1. [POC 테스트 결과](./poc-tests/2026-01-08/POC_TEST_RESULT.md) - 종합 보고서
2. [AI 분석 로그](./poc-tests/2026-01-08/AI_ANALYSIS_LOGS.md) - 상세 분석

### 프로덕션 준비
1. [Gemini 통합 가이드](./poc-tests/2026-01-08/GEMINI_INTEGRATION_GUIDE.md) - 성능/비용 최적화

---

## 📝 문서 작성 규칙

### 파일명 규칙
- 대문자 스네이크 케이스: `POC_TEST_RESULT.md`
- 날짜 형식: `YYYY-MM-DD`
- 공백 대신 언더스코어 사용

### 디렉토리 구조
```
docs/
├── poc-tests/
│   └── YYYY-MM-DD/
│       ├── POC_TEST_RESULT.md
│       └── ...
├── architecture/
│   └── 시스템_설계.md
├── guides/
│   └── 가이드명_GUIDE.md
└── development/
    └── 개발_문서.md
```

### 문서 메타데이터
각 문서 하단에 포함:
```markdown
---
**작성일**: YYYY-MM-DD
**작성자**: 작성자명
**버전**: x.x
```

---

## 🔄 최근 업데이트

- **2026-01-08**: 초기 문서 구조 생성
  - POC 테스트 결과 (Ollama llama3.2)
  - AI 분석 로그 (11개 모듈)
  - Gemini 통합 가이드

---

**Last Updated**: 2026-01-08
