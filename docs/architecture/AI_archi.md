# 📄 AI Code Analysis Service: Workflow & Design Specification

## 1. 시스템 개요 (System Overview)

본 시스템은 사용자의 GitHub 리포지토리를 분석하여 **개발 기여도, 기술 스택, 코드 품질**을 평가하는 포트폴리오 생성 서비스이다.
**Spring Boot**가 메인 서버(DB, PDF 생성, 사용자 요청) 역할을 하며, **FastAPI**는 비동기 AI 분석 워커(Worker) 역할을 수행한다.

### 1.1 아키텍처 패턴: 리소스 업데이트 (Resource Update Pattern)

이벤트 알림(Webhook)이 아닌, **RESTful 리소스 수정 방식**을 채택하여 데이터의 정합성을 보장한다.

1. **Creation:** Spring이 사용자 요청을 받아 DB에 `AnalysisReport` 데이터를 생성한다. (Status: `PENDING`)
2. **Delegation:** Spring이 FastAPI에게 "이 리포트(ID)의 내용을 분석해서 채워달라"고 요청한다.
3. **Processing:** FastAPI는 백그라운드에서 분석을 수행한다. (AWS Free Tier 메모리 최적화 필수)
4. **Update:** 분석이 완료되면 FastAPI가 Spring의 리소스 수정 API(`PATCH`)를 호출하여 결과를 업데이트한다.
5. **Rendering:** Spring은 업데이트된 데이터를 바탕으로 최종 **PDF 리포트**를 생성한다.

---

## 2. API 인터페이스 명세 (Interface Spec)

Spring과 FastAPI 간의 통신 규약이다. 작업의 식별자는 Spring DB의 Primary Key(`report_id`)를 사용한다.

### 2.1 분석 요청 API (Spring → FastAPI)

* **Endpoint:** `POST /analyze`
* **Description:** 분석 작업을 큐에 등록한다.
* **Request Body:**
```json
{
  "repo_url": "https://github.com/myongji-univ/shuttle-bus.git",
  "branch": "main",
  "target_user": "HandsomeGuy",
  "report_id": 100,  // Spring DB의 PK
  "callback_url": "http://spring-server/api/reports/100" // 결과를 업데이트할 Spring Endpoint
}

```


* **Response (Immediate):**
* `202 Accepted`: `{"status": "ACCEPTED", "message": "Analysis queued for Report #100"}`
* `429 Too Many Requests`: 글로벌 작업 큐가 가득 참.



### 2.2 결과 반영 API (FastAPI → Spring)

FastAPI가 분석 완료 후 Spring의 리소스를 수정(Update)한다. **PDF 템플릿에 매핑될 구조화된 JSON**을 전송해야 한다.

* **Endpoint:** `PATCH {callback_url}` (예: `/api/reports/100`)
* **Request Body (Success):**
```json
{
  "status": "COMPLETED",
  "result": {
    "report": {
      "summary": "이 개발자는 전체 프로젝트의 35%를 기여했으며, 주로 Redis 캐싱 레이어와...",
      "tech_stack": ["Java", "Spring Boot", "Redis", "WebSocket"],
      "key_contributions": [
        "Redis Geo 자료구조를 활용한 실시간 위치 트래킹",
        "Global Exception Handler 도입",
        "CompletableFuture 비동기 처리 최적화"
      ],
      "code_quality": "객체지향 원칙(SOLID)을 준수하며, 전략 패턴을 적절히 활용함.",
      "project_tree": "src/\n├── main/\n│   ├── java/com/..." 
    }
  }
}

```


* **Request Body (Failure):**
```json
{
  "status": "FAILED",
  "error_message": "Private Repository 접근 권한이 없거나 URL이 잘못되었습니다."
}

```



---

## 3. 데이터베이스 스키마 가이드 (Spring Side)

FastAPI가 보낸 데이터를 담기 위해 Spring 엔티티는 다음과 같이 구성되어야 한다.

### 3.1 DDL (Table Definition)

```sql
CREATE TABLE analysis_report (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    repo_url VARCHAR(255) NOT NULL,
    target_user VARCHAR(100) NOT NULL,
    
    -- [AI 분석 결과 저장 필드: JSON 매핑 권장]
    summary_content TEXT,       -- 상세 분석 리포트 (Markdown)
    tech_stack JSON,            -- 기술 스택 배열 (["Java", "Spring"])
    contribution_score INT,     -- 기여도 점수 (0~100)
    
    -- [상태 및 메타데이터]
    status VARCHAR(20) DEFAULT 'PENDING', -- PENDING -> COMPLETED or FAILED
    created_at DATETIME DEFAULT NOW()
);

```

### 3.2 데이터 상태 변화 (Lifecycle)

* **Step 1 (Insert):** 요청 시 `status='PENDING'`, 결과 필드는 `NULL`.
* **Step 2 (Update):** FastAPI의 `PATCH` 요청을 받아 `status='COMPLETED'`, 결과 필드 채움.
* **Step 3 (PDF Generation):** Spring 템플릿 엔진이 위 데이터를 조회하여 PDF 렌더링.

---

## 4. 상세 처리 파이프라인 (Detailed Pipeline)

**AWS Free Tier (RAM 1GB)** 환경을 고려하여 메모리 사용량을 엄격히 제어하되, 분석 속도를 위해 **이중 병렬 제어(Dual Semaphore)** 전략을 사용한다.

### Step 1: 리소스 제어 (Concurrency Control)

* **Global Semaphore (서비스 보호):**
* 동시에 처리 가능한 **사용자 요청(Repository)** 개수는 **최대 1~2개**로 제한한다.
* *목적:* `git clone` 및 파싱 과정에서의 메모리 스파이크(OOM) 방지.


* **Internal Semaphore (속도 향상):**
* 하나의 리포지토리 내부에서 AI에게 보내는 **청크(Chunk)** 요청은 **동시에 10개**까지 병렬 처리(`asyncio.gather`)한다.
* *목적:* LLM API 대기 시간(Network I/O)을 줄여 전체 분석 속도 극대화.



### Step 2: 코드 확보 및 구조화 (Preprocessing)

1. **Workspace:** `/tmp/{report_id}/` 디렉토리 생성.
2. **Git Clone (Lightweight):** `git clone --depth 1 {repo_url} .` (과거 이력 제외).
3. **Generate Project Tree:** 전체 프로젝트의 폴더 구조를 문자열로 생성하여 저장 (Reduce 단계에서 사용).
4. **Filtering:** `GitPython`으로 `git blame` 수행. `target_user`가 작성한 라인이 **1줄 이상**인 파일만 추출.

### Step 3: 스마트 그룹핑 (Smart Grouping)

AI에게 문맥(Context)을 제공하기 위해 연관된 파일을 논리적으로 묶는다.

1. **Name-based Clustering (1순위):** 파일명에서 접미사(`Controller`, `Service`, `Impl`, `Repository`, `Dto`)를 제거한 **핵심 키워드**가 같은 파일끼리 묶는다.
2. **Folder-based Clustering (2순위):** 이름으로 묶이지 않은 파일은 같은 디렉토리에 있는 파일끼리 묶는다.

### Step 4: AI 분석 (Map-Reduce with XML Strategy)

비용과 정확도를 위해 **XML 포맷**과 **한/영 혼용 프롬프트**를 사용한다.

#### 4.1 Phase 1: Map (개별 파일 분석)

* **Format:** XML Tag (`<document><path>...</path><content>...</content></document>`)
* **Prompt (System):** "You are a Senior Reviewer. Analyze the code in `<content>`. Focus on `<user_lines>`. Explain logic & tech stack in **Korean JSON**."
* **Concurrency:** Internal Semaphore(10) 적용.

#### 4.2 Phase 2: Reduce (종합 및 PDF 데이터 생성)

개별 분석 결과와 **전체 프로젝트 트리**를 함께 입력받아 최종 JSON을 생성한다.

* **Input:** 1. List of Map Results (JSON List), 2. **Project Directory Tree (String)**
* **System Prompt (English):**
> "You are a Tech Lead.


> 1. Use the 'Project Tree' to understand the architectural context.
> 2. Synthesize the 'Chunk Summaries' into a structured report.
> 3. **Output MUST be strictly in JSON format as defined.**"
> 
> 


* **Target JSON Schema:**
```json
{
  "summary": "String (Korean, 3-5 lines)",
  "tech_stack": "List[String]",
  "key_contributions": "List[String] (Top 3-5 features)",
  "code_quality": "String (Korean)",
  "project_tree": "String (The tree provided in input)"
}

```



### Step 5: 정리 (Cleanup)

* 작업 완료 또는 실패 시, 반드시 `shutil.rmtree('/tmp/{report_id}')`를 실행하여 임시 파일을 삭제한다.

---

## 5. 에러 처리 전략 (Error Handling)

1. **Git Clone 실패:** URL 오류/권한 문제 시 `FAILED` 상태와 에러 메시지를 Spring에 전송.
2. **AI API 오류:** `tenacity` 라이브러리로 최대 3회 재시도(Retry).
3. **예외 처리:** 최상위 `try-except` 블록에서 포착하여 서버 다운 방지 및 `FAILED` 콜백 전송.