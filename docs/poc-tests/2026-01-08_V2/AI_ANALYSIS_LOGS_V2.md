### Spring Server log

```
 sunmin@iseonmin-ui-MacBookPro AI_report_Poc % venv/bin/activate
zsh: permission denied: venv/bin/activate
sunmin@iseonmin-ui-MacBookPro AI_report_Poc % python3 tests/mock_spring.py
Traceback (most recent call last):
  File "/Users/sunmin/project/AI_report_Poc/tests/mock_spring.py", line 10, in <module>
    from fastapi import FastAPI, Request
ModuleNotFoundError: No module named 'fastapi'
sunmin@iseonmin-ui-MacBookPro AI_report_Poc % venv/bin/activate           
zsh: permission denied: venv/bin/activate
sunmin@iseonmin-ui-MacBookPro AI_report_Poc % venv/bin/activate
zsh: permission denied: venv/bin/activate
sunmin@iseonmin-ui-MacBookPro AI_report_Poc % source venv/bin/activate
(venv) sunmin@iseonmin-ui-MacBookPro AI_report_Poc % python3 tests/mock_spring.py
2026-01-08 16:57:52,560 - __main__ - INFO - ======================================================================
2026-01-08 16:57:52,560 - __main__ - INFO - Starting Mock Spring Server on http://localhost:9000
2026-01-08 16:57:52,560 - __main__ - INFO - Waiting for callbacks from FastAPI...
2026-01-08 16:57:52,560 - __main__ - INFO - ======================================================================
INFO:     Started server process [48435]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9000 (Press CTRL+C to quit)
2026-01-08 17:04:57,398 - __main__ - INFO - ======================================================================
2026-01-08 17:04:57,398 - __main__ - INFO - Received callback for Report #102
2026-01-08 17:04:57,398 - __main__ - INFO - Status: COMPLETED
2026-01-08 17:04:57,398 - __main__ - INFO - 
======================================================================
2026-01-08 17:04:57,398 - __main__ - INFO - ANALYSIS RESULT
2026-01-08 17:04:57,398 - __main__ - INFO - ======================================================================
2026-01-08 17:04:57,398 - __main__ - INFO - 
Summary:
분석 결과를 파싱하는 중 오류가 발생했습니다.
2026-01-08 17:04:57,398 - __main__ - INFO - 
Tech Stack:

2026-01-08 17:04:57,398 - __main__ - INFO - 
Key Contributions:
2026-01-08 17:04:57,398 - __main__ - INFO - 
Code Quality:
평가 불가
2026-01-08 17:04:57,398 - __main__ - INFO - 
Project Tree:
...
2026-01-08 17:04:57,398 - __main__ - INFO - ======================================================================
INFO:     127.0.0.1:57981 - "PATCH /api/reports/102 HTTP/1.1" 200 OK
```
<br/>

### python server log

```
Last login: Thu Jan  8 16:56:07 on ttys003
sunmin@iseonmin-ui-MacBookPro AI_report_Poc % source venv/bin/activate
(venv) sunmin@iseonmin-ui-MacBookPro AI_report_Poc % python3 -m app.main
/Users/sunmin/project/AI_report_Poc/app/main.py:36: DeprecationWarning: 
        on_event is deprecated, use lifespan event handlers instead.

        Read more about it in the
        [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
        
  @app.on_event("startup")
INFO:     Will watch for changes in these directories: ['/Users/sunmin/project/AI_report_Poc']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [48441] using WatchFiles
INFO:     Started server process [48445]
INFO:     Waiting for application startup.
2026-01-08 16:57:59,128 - app.main - INFO - ==================================================
2026-01-08 16:57:59,128 - app.main - INFO - AI Code Analysis Service Starting...
2026-01-08 16:57:59,128 - app.main - INFO - LLM Provider: ollama
2026-01-08 16:57:59,128 - app.main - INFO - Ollama URL: http://localhost:11434
2026-01-08 16:57:59,128 - app.main - INFO - Ollama Model: llama3.2
2026-01-08 16:57:59,128 - app.main - INFO - Global Semaphore Limit: 2
2026-01-08 16:57:59,128 - app.main - INFO - Internal Semaphore Limit: 10
2026-01-08 16:57:59,128 - app.main - INFO - ==================================================
INFO:     Application startup complete.
2026-01-08 16:58:43,234 - app.api.routes - INFO - Received analysis request for Report #102
2026-01-08 16:58:43,235 - app.api.routes - INFO - Repository: https://github.com/Dangdaengdan/PETNER-backend.git, User: sunm2n
INFO:     127.0.0.1:57956 - "POST /api/analyze HTTP/1.1" 202 Accepted
2026-01-08 16:58:43,235 - app.services.analyzer - INFO - [Report #102] Starting analysis pipeline
2026-01-08 16:58:43,235 - app.services.analyzer - INFO - [Report #102] Acquired global semaphore
2026-01-08 16:58:43,235 - app.services.git_service - INFO - Cloning https://github.com/Dangdaengdan/PETNER-backend.git (branch: dev) to /tmp/102
2026-01-08 16:58:44,088 - app.services.git_service - INFO - Successfully cloned repository
2026-01-08 16:58:44,088 - app.services.git_service - INFO - Filtering files by user: sunm2n
2026-01-08 16:58:46,425 - app.services.git_service - INFO - Filtered 35 files with contributions from sunm2n
2026-01-08 16:58:46,425 - app.services.analyzer - INFO - [Report #102] Found 35 files by sunm2n
2026-01-08 16:58:46,425 - app.services.analyzer - INFO - [Report #102] Generated project tree
2026-01-08 16:58:46,426 - app.services.grouping_service - INFO - Starting smart grouping for 35 files
2026-01-08 16:58:46,426 - app.services.grouping_service - INFO - Name-based grouping created 2 groups
2026-01-08 16:58:46,426 - app.services.grouping_service - INFO - Folder-based grouping created 16 additional groups
2026-01-08 16:58:46,426 - app.services.grouping_service - INFO - Total groups created: 18
2026-01-08 16:58:46,426 - app.services.analyzer - INFO - [Report #102] Grouped into 18 clusters
2026-01-08 16:58:46,437 - app.services.ai_service - INFO - AIService initialized with provider: ollama, model: llama3.2
2026-01-08 16:58:46,437 - app.services.ai_service - INFO - Starting Map analysis for 18 file groups
2026-01-08 16:58:59,543 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 16:58:59,544 - app.services.ai_service - ERROR - Failed to parse AI response as JSON: Expecting value: line 1 column 1 (char 0)
2026-01-08 16:58:59,544 - app.services.ai_service - ERROR - Response was: **JSON Analysis Summary**

{
  "files_analyzed": ["file1.java"],
  "main_features": "This user implemented a SessionUser class in Java, which is a data transfer object (DTO) for storing and transferring user information. The class uses Lombok annotations for builder and getter functionality.",
  "tech_stack": ["Java", "Spring", "Redis"],
  "notable_patterns": "The user employed the Builder pattern using Lombok to create a SessionUser instance from a Member entity, ensuring data consistency and reducing boilerplate code."
}
2026-01-08 16:59:03,527 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 16:59:27,917 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 16:59:27,918 - app.services.ai_service - ERROR - Failed to parse AI response as JSON: Expecting value: line 1 column 1 (char 0)
2026-01-08 16:59:27,918 - app.services.ai_service - ERROR - Response was: Here is a concise summary of the analyzed code in JSON format:

```
{
  "files_analyzed": ["AuthController.java", "AuthService.java"],
  "main_features": "This developer implemented an authentication controller using Spring Boot, Kakao login, and Redis-based session management. The controller handles user login, logout, and member information retrieval.",
  "tech_stack": ["Java", "Spring", "Redis"],
  "notable_patterns": "The developer used Lombok for annotation processing and logging with SLF4J. They also implemented a custom exception handling mechanism using ErrorCode and MemberException."
}
```

Note that I focused on the main features of the code, highlighting the key functionalities implemented by this user's contribution.
2026-01-08 16:59:32,339 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 16:59:34,027 - watchfiles.main - INFO - 1 change detected
2026-01-08 16:59:51,196 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 16:59:51,196 - app.services.ai_service - ERROR - Failed to parse AI response as JSON: Expecting value: line 1 column 1 (char 0)
2026-01-08 16:59:51,197 - app.services.ai_service - ERROR - Response was: **JSON Summary**

{
  "files_analyzed": ["file1.java", "file2.java"],
  "main_features": "This developer implemented Spring Security configuration with Redis session management, Swagger UI support, and Web MVC settings. They also registered an argument resolver for SessionUser injection.",
  "tech_stack": ["Java", "Spring", "Redis"],
  "notable_patterns": "Notable code patterns include the use of @Configuration annotation for bean definition, @Bean method for creating beans, and @RequiredArgsConstructor for constructor-based dependency injection."
}

**Analysis**

The provided Java files are configuration classes for a Spring-based web application. The main features implemented by this developer include:

* Spring Security configuration with Redis session management
* Support for Swagger UI
* Web MVC settings

Notable code patterns used in the code include:

* Use of @Configuration annotation for bean definition
* Use of @Bean method for creating beans
* Use of @RequiredArgsConstructor for constructor-based dependency injection
2026-01-08 16:59:58,318 - watchfiles.main - INFO - 1 change detected
2026-01-08 17:00:00,497 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 17:00:00,498 - app.services.ai_service - ERROR - Failed to parse AI response as JSON: Expecting value: line 1 column 1 (char 0)
2026-01-08 17:00:00,498 - app.services.ai_service - ERROR - Response was: **JSON Analysis Summary**

{
  "files_analyzed": ["file1.java"],
  "main_features": "This developer implemented a custom annotation `@SessionMember` to automatically inject the current logged-in user information into method parameters. The annotation also allows for optional parameter validation.",
  "tech_stack": ["Java", "Spring"],
  "notable_patterns": "The use of Java annotations and Spring framework is notable in this code, showcasing the developer's familiarity with these technologies."
}
2026-01-08 17:00:22,206 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 17:00:22,206 - app.services.ai_service - ERROR - Failed to parse AI response as JSON: Expecting value: line 1 column 1 (char 0)
2026-01-08 17:00:22,206 - app.services.ai_service - ERROR - Response was: Here is the analysis of the provided code in JSON format:

```
{
  "files_analyzed": ["file1.java"],
  "main_features": "This user implemented a custom ArgumentResolver for Spring that injects the current logged-in user's information into controller methods using the @SessionMember annotation.",
  "tech_stack": ["Java", "Spring", "Redis"],
  "notable_patterns": "The use of Lombok and Spring Framework features such as HandlerMethodArgumentResolver, ModelAndViewContainer, NativeWebRequest, and WebDataBinderFactory demonstrate a good understanding of Spring's architecture and design patterns."
}
```

Note that I've focused on what this user's code does, without making any assumptions about the surrounding code or other files.
2026-01-08 17:01:12,036 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 17:01:12,037 - app.services.ai_service - ERROR - Failed to parse AI response as JSON: Expecting value: line 1 column 1 (char 0)
2026-01-08 17:01:12,037 - app.services.ai_service - ERROR - Response was: Here is a concise summary of the analyzed code in JSON format:

```
{
  "files_analyzed": [
    "file1.java",
    "file2.java"
  ],
  "main_features": "This developer implemented a member management system with Spring Boot, using JPA for database operations and Redis (not shown in the provided files). The system provides methods for creating new members, completing profiles, updating profiles, checking nickname and email duplicates.",
  "tech_stack": [
    "Java",
    "Spring",
    "Redis"
  ],
  "notable_patterns": "The developer used Spring Data JPA with query hints to optimize N+1 problems. They also implemented custom exception handling for specific error cases."
}
```

Note that I did not include Redis in the `main_features` section since it was not shown in the provided files, but it is mentioned in the `tech_stack`.
2026-01-08 17:01:35,802 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 17:01:35,803 - app.services.ai_service - ERROR - Failed to parse AI response as JSON: Expecting value: line 1 column 1 (char 0)
2026-01-08 17:01:35,803 - app.services.ai_service - ERROR - Response was: Here is a concise summary of the analyzed code in JSON format:

```
{
  "files_analyzed": ["file1.java", "file2.java"],
  "main_features": "This class provides utility methods for managing user sessions, including authentication, session management, and logout. It also includes features for caching user information and handling exceptions.",
  "tech_stack": ["Java", "Spring", "Redis"],
  "notable_patterns": "The use of Optional to handle null or absent values in the getCurrentUser method is a notable pattern. The class also uses try-catch blocks to handle exceptions, such as ClassCastException and MemberException."
}
```
2026-01-08 17:02:28,429 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 17:02:28,430 - app.services.ai_service - ERROR - Failed to parse AI response as JSON: Expecting value: line 1 column 1 (char 0)
2026-01-08 17:02:28,430 - app.services.ai_service - ERROR - Response was: **JSON Summary**

```json
{
  "files_analyzed": ["file1.java", "file2.java"],
  "main_features": "This user implemented a custom exception handling system using Spring's @RestControllerAdvice annotation, allowing for centralized error handling and response generation. The system also includes support for various HTTP status codes and error messages.",
  "tech_stack": ["Java", "Spring", "Redis"],
  "notable_patterns": "The use of Lombok annotations (e.g., @Getter, @RequiredArgsConstructor) to simplify code generation and the implementation of a generic exception handling mechanism using Spring's @ExceptionHandler annotation."
}
```

**Code Review**

The provided code consists of two main files: `ErrorCode.java` and `GlobalExceptionHandler.java`. The `ErrorCode` enum defines various error codes with corresponding HTTP status codes and error messages. The `GlobalExceptionHandler` class is responsible for catching and handling exceptions that occur during request processing.

The exception handling mechanism in the `GlobalExceptionHandler` class is robust and covers a wide range of scenarios, including:

* Custom exceptions (e.g., `RuntimeException`, `MethodArgumentNotValidException`)
* HTTP-related exceptions (e.g., `HttpMessageNotReadableException`, `HttpRequestMethodNotSupportedException`)
* Security-related exceptions (e.g., `AuthenticationException`, `AccessDeniedException`)
* Database-related exceptions (e.g., `DataIntegrityViolationException`)

The class uses Spring's `@ExceptionHandler` annotation to define exception handlers, which allows for centralized error handling and response generation. The exception handlers also log warnings using the SLF4J logging framework.

Overall, the code is well-structured, readable, and maintainable. However, some minor suggestions can be made:

* Consider adding more specific error messages or logging details to help with debugging.
* Review the `ErrorCode` enum for potential duplication or inconsistencies.
* Consider using a more robust exception handling mechanism, such as Spring's built-in `ExceptionResolver` interface.

**Code Quality**

The code is well-organized and follows standard Java coding conventions. The use of Lombok annotations simplifies code generation and reduces boilerplate code. The exception handling mechanism is robust and covers a wide range of scenarios.

However, some minor suggestions can be made:

* Consider adding more comments or documentation to explain the purpose and behavior of the `GlobalExceptionHandler` class.
* Review the code for potential performance bottlenecks or optimization opportunities.
* Consider using a more consistent naming convention throughout the codebase.
2026-01-08 17:02:40,214 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 17:02:40,215 - app.services.ai_service - ERROR - Failed to parse AI response as JSON: Expecting value: line 1 column 1 (char 0)
2026-01-08 17:02:40,215 - app.services.ai_service - ERROR - Response was: **JSON Analysis Summary**

{
  "files_analyzed": ["file1.java", "file2.java"],
  "main_features": "This developer implemented a set of custom exception classes (MemberException, DogException, ShelterException, ChatException, PostException) that extend the RuntimeException class and include an ErrorCode field. These exceptions are likely used to handle specific error conditions in a pet-related application.",
  "tech_stack": ["Java", "Spring", "Redis"],
  "notable_patterns": "The use of Lombok annotations (Getter, RequiredArgsConstructor) simplifies code generation for these custom exception classes."
}
2026-01-08 17:02:53,531 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 17:02:53,531 - app.services.ai_service - ERROR - Failed to parse AI response as JSON: Expecting value: line 1 column 1 (char 0)
2026-01-08 17:02:53,532 - app.services.ai_service - ERROR - Response was: **JSON Summary**

{
  "files_analyzed": ["file1.java"],
  "main_features": "This developer implemented a Swagger configuration class for Spring Boot, including security settings and customizing OpenAPI parameters. The class uses annotations to filter out certain parameters from the API documentation.",
  "tech_stack": ["Java", "Spring", "Redis"],
  "notable_patterns": "The code demonstrates the use of Spring Boot's @Configuration annotation and Java Reflection to customize Swagger UI configuration, specifically filtering out parameters annotated with @SessionMember."
}
2026-01-08 17:03:08,271 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 17:03:08,271 - app.services.ai_service - ERROR - Failed to parse AI response as JSON: Expecting value: line 1 column 1 (char 0)
2026-01-08 17:03:08,271 - app.services.ai_service - ERROR - Response was: Here is the summary in JSON format:

{
  "files_analyzed": ["file1.java", "file2.java"],
  "main_features": "This developer implemented two data transfer object (DTO) classes, ProfileResponseDto and ValidationResponseDto, which are used to exchange data between layers of an application. The DTOs contain relevant member information and provide methods for validation.",
  "tech_stack": ["Java", "Spring", "Redis"],
  "notable_patterns": "The developer utilized Lombok annotations (e.g., @Getter, @Builder, @AllArgsConstructor) to simplify the implementation of the DTO classes."
}
2026-01-08 17:03:26,247 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 17:03:26,247 - app.services.ai_service - ERROR - Failed to parse AI response as JSON: Expecting value: line 1 column 1 (char 0)
2026-01-08 17:03:26,248 - app.services.ai_service - ERROR - Response was: **JSON Summary**

{
  "files_analyzed": ["file1.java", "file2.java"],
  "main_features": "This developer implemented two data transfer object (DTO) classes, ProfileCompleteRequestDto and ProfileUpdateRequestDto, for handling profile-related requests. Both classes use Java Validation API to validate user input data.",
  "tech_stack": ["Java", "Spring", "Redis"],
  "notable_patterns": "The developer used Lombok annotations for simplifying code generation, indicating a preference for concise and efficient coding practices."
}
2026-01-08 17:03:32,054 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 17:03:51,501 - watchfiles.main - INFO - 1 change detected
2026-01-08 17:03:58,132 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 17:03:58,133 - app.services.ai_service - ERROR - Failed to parse AI response as JSON: Expecting value: line 1 column 1 (char 0)
2026-01-08 17:03:58,133 - app.services.ai_service - ERROR - Response was: Here is a concise summary of the analyzed code in JSON format:

```
{
  "files_analyzed": ["file1.java", "file2.java"],
  "main_features": "This user implemented an OAuth API client interface (OAuthApiClient) and its implementation class (KakaoApiClient) using Spring and Redis. The KakaoApiClient class uses the RestTemplate to make HTTP requests to the Kakao API.",
  "tech_stack": ["Java", "Spring", "Redis"],
  "notable_patterns": "This user implemented ISP (Interface Segregation Principle) and DIP (Dependency Inversion Principle) in their code, and used Jackson for JSON parsing. They also handled exceptions and logging using Spring's built-in features."
}
```

Note that I did not include any specific design patterns or notable code smells, as the provided code does not exhibit any major issues. However, if you'd like me to provide a more detailed analysis, please let me know!
2026-01-08 17:04:11,612 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 17:04:15,532 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 17:04:15,532 - app.services.ai_service - ERROR - Failed to parse AI response as JSON: Expecting value: line 1 column 1 (char 0)
2026-01-08 17:04:15,533 - app.services.ai_service - ERROR - Response was: **JSON Summary**

{
  "files_analyzed": ["PetnerApplicationTests.java"],
  "main_features": "This user implemented a basic JUnit test class for the PetnerApplication, but it is incomplete and lacks any test methods.",
  "tech_stack": ["Java", "Spring"],
  "notable_patterns": ""
}
2026-01-08 17:04:15,533 - app.services.ai_service - INFO - Map analysis completed: 18/18 succeeded
2026-01-08 17:04:15,533 - app.services.analyzer - INFO - [Report #102] Completed Map analysis
2026-01-08 17:04:15,533 - app.services.ai_service - INFO - Starting Reduce analysis with 18 map results
2026-01-08 17:04:57,384 - httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
2026-01-08 17:04:57,385 - app.services.ai_service - ERROR - Failed to parse AI response as JSON: Expecting ':' delimiter: line 27 column 5 (char 747)
2026-01-08 17:04:57,385 - app.services.ai_service - ERROR - Response was: {
  "summary": "이 개발자는 Petner应用 프로그램을 구축하고, Spring Boot와 Redis를 사용하여 응답 DTO를 구현했습니다. Lombok을 사용하여 builder 및 getter 기능을 간단하게 구현했습니다.",
  "tech_stack": ["Java", "Spring", "Redis"],
  "key_contributions": [
    "PetnerApplication.java",
    "ErrorPayload.java",
    "KakaoUserInfo.java",
    "response DTOs"
  ],
  "code_quality": "Lombok을 사용하여 builder 및 getter 기능을 간단하게 구현하여 코드의 readability를 향상시켰습니다. 그러나 response DTOs에 대한 추가적인 테스트가 필요합니다.",
  "project_tree": {
    "root": [
      ".claude/",
      ".github/",
      "gradle/",
      "src/",
      ".env.example",
      ".gitattributes",
      "README.md",
      "build.gradle",
      "gradlew",
      "gradlew.bat",
      "settings.gradle"
    ],
    ".claude/": {
      "settings.local.json"
    },
    ".github/": {
      "ISSUE_TEMPLATE/",
      "workflows/",
      "pull_request_template.md"
    },
    "gradle/": {
      "wrapper/",
      "build.gradle"
    },
    "src/": {
      "main/",
      "test/"
    },
    "src/main/java/": {
      "com/",
      "example/",
      "petner/"
    },
    "src/test/java/": {
      "com/",
      "example/",
      "petner/"
    }
  }
}
2026-01-08 17:04:57,385 - app.services.ai_service - INFO - Reduce analysis completed
2026-01-08 17:04:57,385 - app.services.analyzer - INFO - [Report #102] Completed Reduce analysis
2026-01-08 17:04:57,386 - app.services.callback_service - INFO - Sending callback to http://localhost:9000/api/reports/102
2026-01-08 17:04:57,399 - httpx - INFO - HTTP Request: PATCH http://localhost:9000/api/reports/102 "HTTP/1.1 200 OK"
2026-01-08 17:04:57,399 - app.services.callback_service - INFO - Callback successful: 200
2026-01-08 17:04:57,399 - app.services.analyzer - INFO - [Report #102] Sent results to Spring
2026-01-08 17:04:57,399 - app.services.analyzer - INFO - [Report #102] Released global semaphore
2026-01-08 17:04:57,429 - app.utils.cleanup - INFO - Cleaned up workspace: /tmp/102
2026-01-08 17:04:57,429 - app.services.analyzer - INFO - [Report #102] Analysis pipeline finished
```