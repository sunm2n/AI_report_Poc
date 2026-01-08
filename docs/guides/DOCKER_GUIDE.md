# Docker 사용 가이드 (Ollama Only)

이 가이드는 Ollama를 Docker로 실행하는 방법을 설명합니다.

## 왜 Ollama만 Docker로?

**POC 단계에서는 리소스 효율성을 위해 Ollama만 Docker로 실행합니다:**

- ✅ **Ollama (Docker)**: GPU 가속, 모델 관리 편의성
- ✅ **FastAPI (로컬)**: 빠른 개발, hot reload, 낮은 오버헤드
- ✅ **Mock Spring (로컬)**: 간단한 테스트 서버

## 사전 요구사항

- Docker Desktop 설치
- M4 Pro의 경우 Metal GPU 가속 자동 활성화

## 빠른 시작

### 1. Ollama 컨테이너 시작

```bash
# Docker Compose로 Ollama 시작
docker-compose up -d

# 컨테이너 상태 확인
docker ps | grep ollama
```

### 2. Ollama 모델 다운로드

```bash
# llama3.2 모델 다운로드 (최초 1회)
docker exec -it ollama ollama pull llama3.2

# 모델 목록 확인
docker exec -it ollama ollama list
```

**예상 출력:**
```
NAME            ID              SIZE    MODIFIED
llama3.2:latest a80c4f17acd5    2.0 GB  2 minutes ago
```

### 3. Ollama 테스트

```bash
# 간단한 테스트
docker exec -it ollama ollama run llama3.2 "Hello, who are you?"

# HTTP API 테스트
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

## Ollama 관리 명령어

### 컨테이너 관리

```bash
# 로그 확인
docker logs ollama

# 실시간 로그 확인
docker logs -f ollama

# 컨테이너 재시작
docker-compose restart ollama

# 컨테이너 중지
docker-compose stop ollama

# 컨테이너 시작
docker-compose start ollama

# 컨테이너 및 볼륨 삭제 (주의: 모델 데이터 삭제됨)
docker-compose down -v
```

### 모델 관리

```bash
# 사용 가능한 모델 목록 (Ollama 라이브러리)
docker exec -it ollama ollama list

# 다른 모델 다운로드
docker exec -it ollama ollama pull llama3.1:13b
docker exec -it ollama ollama pull codellama:7b
docker exec -it ollama ollama pull mistral:7b

# 모델 삭제
docker exec -it ollama ollama rm llama3.2

# 모델 정보 확인
docker exec -it ollama ollama show llama3.2
```

## M4 Pro GPU 가속

M4 Pro의 Metal GPU는 자동으로 활성화됩니다. 확인:

```bash
# Metal 사용 확인
docker logs ollama 2>&1 | grep -i metal

# 추론 성능 확인 (토큰/초)
time docker exec -it ollama ollama run llama3.2 "Write a short poem"
```

**예상 성능 (M4 Pro):**
- llama3.2 (3B): ~40-60 tokens/sec
- llama3.1 (13B): ~15-25 tokens/sec

## 데이터 지속성

Ollama 모델은 Docker 볼륨에 저장됩니다:

```bash
# 볼륨 확인
docker volume ls | grep ollama

# 볼륨 상세 정보
docker volume inspect ai_report_poc_ollama_data

# 볼륨 백업
docker run --rm \
  -v ai_report_poc_ollama_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/ollama_backup.tar.gz -C /data .

# 볼륨 복원
docker run --rm \
  -v ai_report_poc_ollama_data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/ollama_backup.tar.gz -C /data
```

## 포트 변경

기본 포트 11434가 충돌하는 경우:

```yaml
# docker-compose.yml 수정
services:
  ollama:
    ports:
      - "11435:11434"  # 호스트:컨테이너
```

`.env` 파일도 수정:
```env
OLLAMA_BASE_URL=http://localhost:11435
```

## 트러블슈팅

### Ollama 컨테이너가 시작 안됨

```bash
# 로그 확인
docker logs ollama

# 포트 충돌 확인
lsof -i :11434

# 완전 재시작
docker-compose down
docker-compose up -d
```

### 모델 다운로드 실패

```bash
# 디스크 공간 확인
df -h

# Docker Desktop 재시작
# Docker Desktop > Quit > 재시작

# 수동으로 재시도
docker exec -it ollama ollama pull llama3.2
```

### Metal GPU 가속 안됨

M4 Pro에서 Metal은 자동 활성화됩니다. 확인:

```bash
# Metal 관련 로그 확인
docker logs ollama 2>&1 | grep -i metal

# 시스템 정보
docker exec -it ollama uname -m  # arm64 확인
```

### 메모리 부족

```bash
# Docker Desktop 설정 확인
# Settings > Resources > Memory

# 권장 설정:
# - llama3.2 (3B): 최소 4GB
# - llama3.1 (13B): 최소 8GB
```

## 유용한 명령어 모음

```bash
# Ollama 컨테이너 셸 접속
docker exec -it ollama bash

# 모델 파일 위치 확인
docker exec -it ollama ls -lh /root/.ollama/models

# 리소스 사용량 실시간 모니터링
docker stats ollama

# Ollama API 엔드포인트 목록
curl http://localhost:11434/api/tags
```

## FastAPI 연동

FastAPI는 로컬에서 실행되며, Docker의 Ollama와 통신합니다:

```python
# .env 설정
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

FastAPI에서 Ollama 접근:
```python
import ollama

client = ollama.AsyncClient(host="http://localhost:11434")
response = await client.chat(model="llama3.2", ...)
```

## 다음 단계

Ollama POC 테스트 완료 후:
- [ ] 프로덕션용 모델 선택 (성능 vs 정확도)
- [ ] 모델 파인튜닝 고려
- [ ] AWS EC2에 Ollama 배포
- [ ] OpenAI API 병행 사용 (속도/품질 비교)
