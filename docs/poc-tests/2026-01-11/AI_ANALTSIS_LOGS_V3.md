# FastApi server

/Users/sunmin/project/AI_test/AI_report_Poc/app/main.py:36: DeprecationWarning: 
        on_event is deprecated, use lifespan event handlers instead.

        Read more about it in the
        [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
        
  @app.on_event("startup")
INFO:     Will watch for changes in these directories: ['/Users/sunmin/project/AI_test/AI_report_Poc']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [96822] using WatchFiles
INFO:     Started server process [96826]
INFO:     Waiting for application startup.
2026-01-11 22:39:02,349 - app.main - INFO - ==================================================
2026-01-11 22:39:02,349 - app.main - INFO - AI Code Analysis Service Starting...
2026-01-11 22:39:02,349 - app.main - INFO - LLM Provider: openai
2026-01-11 22:39:02,349 - app.main - INFO - OpenAI Model: gpt-4o
2026-01-11 22:39:02,349 - app.main - INFO - Global Semaphore Limit: 2
2026-01-11 22:39:02,349 - app.main - INFO - Internal Semaphore Limit: 10
2026-01-11 22:39:02,349 - app.main - INFO - ==================================================
INFO:     Application startup complete.
2026-01-11 22:39:16,538 - app.api.routes - INFO - Received analysis request for Report #103
2026-01-11 22:39:16,538 - app.api.routes - INFO - Repository: https://github.com/Dangdaengdan/PETNER-backend.git, User: sunm2n
INFO:     127.0.0.1:53190 - "POST /api/analyze HTTP/1.1" 202 Accepted
2026-01-11 22:39:16,538 - app.services.analyzer - INFO - [Report #103] Starting analysis pipeline
2026-01-11 22:39:16,538 - app.services.analyzer - INFO - [Report #103] Acquired global semaphore
2026-01-11 22:39:16,538 - app.services.git_service - INFO - Cloning https://github.com/Dangdaengdan/PETNER-backend.git (branch: dev) to /tmp/103
2026-01-11 22:39:17,370 - app.services.git_service - INFO - Successfully cloned repository
2026-01-11 22:39:17,370 - app.services.git_service - INFO - Filtering files by user: sunm2n
2026-01-11 22:39:20,128 - app.services.git_service - INFO - Filtered 35 files with contributions from sunm2n
2026-01-11 22:39:20,129 - app.services.analyzer - INFO - [Report #103] Found 35 files by sunm2n
2026-01-11 22:39:20,129 - app.services.analyzer - INFO - [Report #103] Generated project tree
2026-01-11 22:39:20,129 - app.services.grouping_service - INFO - Starting smart grouping for 35 files
2026-01-11 22:39:20,130 - app.services.grouping_service - INFO - Name-based grouping created 2 groups
2026-01-11 22:39:20,130 - app.services.grouping_service - INFO - Folder-based grouping created 16 additional groups
2026-01-11 22:39:20,130 - app.services.grouping_service - INFO - Total groups created: 18
2026-01-11 22:39:20,130 - app.services.analyzer - INFO - [Report #103] Grouped into 18 clusters
2026-01-11 22:39:20,255 - app.services.ai_service - INFO - AIService initialized with provider: openai, model: gpt-4o
2026-01-11 22:39:20,255 - app.services.ai_service - INFO - Starting Map analysis for 18 file groups
2026-01-11 22:39:21,548 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:21,549 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:21,642 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:21,914 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:21,945 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:21,995 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:22,063 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:22,097 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:22,112 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:22,416 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:23,057 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:23,188 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:23,326 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:23,448 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:23,776 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:23,866 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:23,878 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:24,027 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:24,029 - app.services.ai_service - INFO - Map analysis completed: 18/18 succeeded
2026-01-11 22:39:24,029 - app.services.analyzer - INFO - [Report #103] Completed Map analysis
2026-01-11 22:39:24,029 - app.services.ai_service - INFO - Starting Reduce analysis with 18 map results
2026-01-11 22:39:32,083 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-01-11 22:39:32,099 - app.services.ai_service - INFO - Reduce analysis completed
2026-01-11 22:39:32,099 - app.services.analyzer - INFO - [Report #103] Completed Reduce analysis
2026-01-11 22:39:32,099 - app.services.callback_service - INFO - Sending callback to http://localhost:9000/api/reports/102
2026-01-11 22:39:32,118 - httpx - INFO - HTTP Request: PATCH http://localhost:9000/api/reports/102 "HTTP/1.1 200 OK"
2026-01-11 22:39:32,119 - app.services.callback_service - INFO - Callback successful: 200
2026-01-11 22:39:32,120 - app.services.analyzer - INFO - [Report #103] Sent results to Spring
2026-01-11 22:39:32,120 - app.services.analyzer - INFO - [Report #103] Released global semaphore
2026-01-11 22:39:32,148 - app.utils.cleanup - INFO - Cleaned up workspace: /tmp/103
2026-01-11 22:39:32,148 - app.services.analyzer - INFO - [Report #103] Analysis pipeline finished
2026-01-11 23:41:31,560 - watchfiles.main - INFO - 3 changes detected
2026-01-11 23:44:26,532 - watchfiles.main - INFO - 3 changes detected
WARNING:  WatchFiles detected changes in 'tests/mock_spring.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [96826]
INFO:     Started server process [98719]
INFO:     Waiting for application startup.
2026-01-11 23:44:27,056 - app.main - INFO - ==================================================
2026-01-11 23:44:27,056 - app.main - INFO - AI Code Analysis Service Starting...
2026-01-11 23:44:27,056 - app.main - INFO - LLM Provider: openai
2026-01-11 23:44:27,056 - app.main - INFO - OpenAI Model: gpt-4o
2026-01-11 23:44:27,056 - app.main - INFO - Global Semaphore Limit: 2
2026-01-11 23:44:27,056 - app.main - INFO - Internal Semaphore Limit: 10
2026-01-11 23:44:27,056 - app.main - INFO - ==================================================
INFO:     Application startup complete.
2026-01-11 23:48:24,127 - watchfiles.main - INFO - 3 changes detected
2026-01-11 23:49:44,630 - watchfiles.main - INFO - 1 change detected
2026-01-11 23:50:22,224 - watchfiles.main - INFO - 1 change detected
2026-01-11 23:52:59,609 - watchfiles.main - INFO - 3 changes detected
2026-01-11 23:53:45,795 - watchfiles.main - INFO - 3 changes detected
2026-01-11 23:54:11,091 - watchfiles.main - INFO - 1 change detected
2026-01-11 23:54:14,753 - watchfiles.main - INFO - 2 changes detected
2026-01-12 00:06:22,170 - watchfiles.main - INFO - 3 changes detected
2026-01-12 00:34:16,956 - watchfiles.main - INFO - 3 changes detected
2026-01-12 00:41:36,037 - watchfiles.main - INFO - 3 changes detected

# 보고서 생성 결과.json

{
  "payload": {
    "status": "COMPLETED",
    "result": {
      "summary": "이 개발자는 회원 관리 기능과 인증 기능을 포함한 다양한 기능을 구현하였으며, 데이터베이스 최적화 및 세션 관리에 중점을 두었습니다. Spring Boot 애플리케이션의 엔트리 포인트를 설정하고, 전반적인 오류 처리 시스템을 구축하였습니다. 또한, Swagger를 사용하여 API 문서화를 개선하였습니다.",
      "tech_stack": [
        "Java",
        "Spring Boot",
        "Redis",
        "WebSocket"
      ],
      "key_contributions": [
        "회원 관리 기능 구현 및 데이터베이스 최적화",
        "Kakao OAuth를 사용한 인증 기능 구현",
        "전반적인 오류 처리 시스템 구축"
      ],
      "code_quality": "코드는 Spring Data JPA와 트랜잭션 관리, 커스텀 예외 처리 등 다양한 설계 패턴을 잘 활용하고 있습니다. 또한, Lombok을 사용하여 보일러플레이트 코드를 줄이고, 인터페이스 분리 원칙을 준수하여 코드의 유지보수성을 높였습니다.",
      "project_tree": "├── .claude/\n│   └── settings.local.json\n├── .github/\n│   ├── ISSUE_TEMPLATE/\n│   │   ├── 기능-개발.md\n│   │   ├── 기타-업무.md\n│   │   ├── 리팩토링.md\n│   │   ├── 문서-작성-및-코드-수정.md\n│   │   ├── 배포-작업.md\n│   │   ├── 버그-수정.md\n│   │   ├── 성능-개선.md\n│   │   ├── 코드-형태-변경.md\n│   │   ├── 테스트-코드.md\n│   │   └── 환경-설정.md\n│   ├── workflows/\n│   │   └── auto-close-issues.yml\n│   └── pull_request_template.md\n├── gradle/\n│   └── wrapper/\n│       ├── gradle-wrapper.jar\n│       └── gradle-wrapper.properties\n├── src/\n│   ├── main/\n│   │   ├── java/\n│   │   │   └── com/\n│   │   │       └── example/\n│   │   │           └── petner/\n│   │   └── resources/\n│   │       ├── db/\n│   │       │   └── migration/\n│   │       │       ├── V10__create_messages_table.sql\n│   │       │       ├── V11__insert_initial_data.sql\n│   │       │       ├── V1__create_locations_table.sql\n│   │       │       ├── V20250922125701__Alter_chat_rooms_table.sql\n│   │       │       ├── V20250922125702__Add_index_to_messages_table.sql\n│   │       │       ├── V20250922125703__Create_chat_room_members_table.sql\n│   │       │       ├── V20250922161000__Add_joined_at_to_chat_room_members.sql\n│   │       │       ├── V20250922164102__Remove_member_table_not_null_constraints.sql\n│   │       │       ├── V20250925000000__Insert_shelter_initial_data.sql\n│   │       │       ├── V20250925171606__Add_deleted_at_to_comments.sql\n│   │       │       ├── V20250928073810__Add_like_functionality.sql\n│   │       │       ├── V20250928135604__Add_deleted_column_to_dogs_table.sql\n│   │       │       ├── V20250928162442__Create_dog_applies_table.sql\n│   │       │       ├── V2__create_breeds_table.sql\n│   │       │       ├── V3__create_shelters_table.sql\n│   │       │       ├── V4__create_members_table.sql\n│   │       │       ├── V5__create_dogs_table.sql\n│   │       │       ├── V6__create_posts_table.sql\n│   │       │       ├── V7__create_comments_table.sql\n│   │       │       ├── V8__create_favorites_table.sql\n│   │       │       └── V9__create_chatrooms_table.sql\n│   │       ├── static/\n│   │       │   ├── chat/\n│   │       │   │   └── chat-test.html\n│   │       │   └── upload/\n│   │       │       └── upload-test.html\n│   │       ├── application-dev.properties\n│   │       ├── application-prod.properties\n│   │       ├── application-test.properties\n│   │       └── application.properties\n│   └── test/\n│       └── java/\n│           └── com/\n│               └── example/\n│                   └── petner/\n├── .env.example\n├── .gitattributes\n├── README.md\n├── build.gradle\n├── gradlew\n├── gradlew.bat\n└── settings.gradle"
    },
    "error_message": null
  },
  "received_at": "2026-01-11T22:39:32.117232"
}