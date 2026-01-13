# AI Code Analysis Service - POC

GitHub 리포지토리 분석 기반 포트폴리오 생성 서비스의 FastAPI 워커 POC 구현

## 아키텍처 개요

- **FastAPI**: 비동기 AI 분석 워커 (이 프로젝트)
- **Spring Boot**: 메인 서버 (향후 통합 예정)
- **Resource Update Pattern**: RESTful 방식의 데이터 정합성 보장
- **Map-Reduce AI 분석**: 메모리 최적화된 병렬 코드 분석

자세한 설계는 [AI_archi.md](./docs/architecture/AI_archi.md) 참조

## 주요 기능

1. **Git Clone & Filtering**: 리포지토리 클론 및 git blame 기반 사용자 파일 필터링
2. **Smart Grouping**: Name-based & Folder-based 파일 클러스터링
3. **AI Map Analysis**: 개별 파일 그룹 병렬 분석 (Semaphore 10)
4. **AI Reduce Analysis**: 종합 리포트 JSON 생성
5. **Callback to Spring**: 분석 결과를 Spring PATCH 엔드포인트로 전송
6. **Memory Optimization**: AWS Free Tier (1GB RAM) 환경 최적화

## 빠른 시작 (Quick Start)

### 1. Ollama Docker 실행

```bash
# Ollama 컨테이너 시작
docker-compose up -d

# 모델 다운로드 (최초 1회만)
docker exec -it ollama ollama pull llama3.2

# 모델 확인
docker exec -it ollama ollama list
```

### 2. Python 가상환경 설정

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 3. 환경 변수 확인

`.env` 파일이 이미 생성되어 있으며, Ollama 기본 설정이 되어 있습니다:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

OpenAI를 사용하려면 `.env` 수정:
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview
```

## 실행 방법

### 1. Mock Spring 서버 실행 (터미널 1)

```bash
python tests/mock_spring.py
```

Mock Spring 서버가 `http://localhost:9000`에서 실행됩니다.

### 2. FastAPI 서버 실행 (터미널 2)

```bash
python -m app.main
```

FastAPI 서버가 `http://localhost:8000`에서 실행됩니다.

**실행 중 확인:**
```
==================================================
AI Code Analysis Service Starting...
LLM Provider: ollama
Ollama URL: http://localhost:11434
Ollama Model: llama3.2
Global Semaphore Limit: 2
Internal Semaphore Limit: 10
==================================================
```

### 3. API 문서 확인

브라우저에서 열기:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 4. 분석 요청 테스트

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/myongji-univ/shuttle-bus.git",
    "branch": "main",
    "target_user": "HandsomeGuy",
    "report_id": 100,
    "callback_url": "http://localhost:9000/api/reports/100"
  }'
```

**응답 (즉시):**
```json
{
  "status": "ACCEPTED",
  "message": "Analysis queued for Report #100"
}
```

### 5. 결과 확인

**Mock Spring 서버 터미널 (터미널 1)**에서 분석 결과 로그를 실시간으로 확인할 수 있습니다:

```
======================================================================
Received callback for Report #100
Status: COMPLETED
======================================================================
ANALYSIS RESULT
======================================================================

Summary:
이 개발자는 전체 프로젝트의 35%를 기여했으며...

Tech Stack:
Java, Spring Boot, Redis, WebSocket

Key Contributions:
  1. Redis Geo 자료구조를 활용한 실시간 위치 트래킹
  2. Global Exception Handler 도입
  3. CompletableFuture 비동기 처리 최적화
...
======================================================================
```

## 프로젝트 구조

```
AI_report_Poc/
├── app/
│   ├── main.py                  # FastAPI 진입점
│   ├── config.py                # 환경 변수 설정
│   ├── api/
│   │   └── routes.py            # POST /analyze 엔드포인트
│   ├── services/
│   │   ├── analyzer.py          # 메인 분석 오케스트레이터
│   │   ├── git_service.py       # Git clone & blame
│   │   ├── grouping_service.py  # 스마트 그룹핑
│   │   ├── ai_service.py        # AI Map/Reduce 분석
│   │   └── callback_service.py  # Spring 콜백
│   ├── models/
│   │   ├── request.py           # 요청 스키마
│   │   └── response.py          # 응답 스키마
│   ├── core/
│   │   ├── semaphore.py         # Global/Internal Semaphore
│   │   ├── tree_generator.py   # 프로젝트 트리 생성
│   │   └── exceptions.py        # 커스텀 예외
│   └── utils/
│       ├── cleanup.py           # 임시 파일 정리
│       └── retry.py             # Tenacity 재시도
├── tests/
│   └── mock_spring.py           # Mock Spring 서버
├── requirements.txt
├── .env.example
└── README.md
```

## API 명세

### POST /api/analyze

리포지토리 분석 작업을 큐에 등록합니다.

**Request Body:**
```json
{
  "repo_url": "https://github.com/user/repo.git",
  "branch": "main",
  "target_user": "username",
  "report_id": 100,
  "callback_url": "http://spring-server/api/reports/100"
}
```

**Response (202 Accepted):**
```json
{
  "status": "ACCEPTED",
  "message": "Analysis queued for Report #100"
}
```

**Response (429 Too Many Requests):**
```json
{
  "detail": "Analysis queue is full. Please try again later."
}
```

### 콜백 (FastAPI → Spring)

분석 완료 후 FastAPI가 Spring의 PATCH 엔드포인트를 호출합니다.

**Endpoint:** `PATCH {callback_url}`

**Request Body (성공):**
```json
{
  "status": "COMPLETED",
  "result": {
    "summary": "개발자 기여도 분석...",
    "tech_stack": ["Java", "Spring Boot", "Redis"],
    "key_contributions": [
      "Redis 캐싱 레이어 구현",
      "Global Exception Handler 도입"
    ],
    "code_quality": "객체지향 원칙 준수...",
    "project_tree": "src/\n├── main/\n..."
  }
}
```

**Request Body (실패):**
```json
{
  "status": "FAILED",
  "error_message": "Private Repository 접근 권한이 없습니다."
}
```

## 동시성 제어

- **Global Semaphore (2)**: 동시 리포지토리 처리 제한 (OOM 방지)
- **Internal Semaphore (10)**: AI 청크 요청 병렬 처리 (속도 최적화)

## 트러블슈팅

### Ollama 연결 실패

```bash
# Docker 컨테이너 상태 확인
docker ps | grep ollama

# Ollama 로그 확인
docker logs ollama

# Ollama 재시작
docker-compose restart ollama

# 모델 다운로드 확인
docker exec -it ollama ollama list
```

### Git Clone 실패
- Private 리포지토리는 접근 권한 필요
- URL이 `.git`으로 끝나는지 확인
- 브랜치 이름이 정확한지 확인

### AI 응답 파싱 오류
- Ollama 모델이 충분히 큰지 확인 (최소 7B 파라미터 권장)
- 더 큰 모델 사용: `docker exec -it ollama ollama pull llama3.1:13b`
- OpenAI API 키가 유효한지 확인

### M4 Pro 최적화

M4 Pro의 Metal GPU 가속은 자동으로 활성화됩니다. 성능 확인:

```bash
# Ollama 컨테이너 로그에서 Metal 사용 확인
docker logs ollama | grep -i metal

# 추론 속도 테스트
docker exec -it ollama ollama run llama3.2 "Hello"
```

## 📚 문서

자세한 문서는 [docs/](./docs/) 디렉토리를 참조하세요.

### 주요 문서
- **[POC 테스트 결과](./docs/poc-tests/2026-01-08/POC_TEST_RESULT.md)** - 2026-01-08 POC 종합 보고서
- **[AI 분석 로그](./docs/poc-tests/2026-01-08/AI_ANALYSIS_LOGS.md)** - 11개 모듈 상세 분석
- **[Gemini 통합 가이드](./docs/poc-tests/2026-01-08/GEMINI_INTEGRATION_GUIDE.md)** - 프로덕션 준비
- **[아키텍처 문서](./docs/architecture/AI_archi.md)** - 전체 시스템 설계
- **[Docker 가이드](./docs/guides/DOCKER_GUIDE.md)** - Ollama 관리

전체 문서 목록: [docs/README.md](./docs/README.md)

## 다음 단계

- [ ] Gemini API 통합 (파싱 문제 해결)
- [ ] Spring Boot 백엔드 통합
- [ ] PDF 생성 기능 추가 (Spring 측)
- [ ] 프로덕션 배포 (AWS EC2, Docker)
- [ ] 성능 최적화 및 메모리 프로파일링

