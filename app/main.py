from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import settings
from app.api import routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Code Analysis Service",
    description="GitHub repository analysis worker for portfolio generation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router)


@app.on_event("startup")
async def startup_event():
    logger.info("=" * 50)
    logger.info("AI Code Analysis Service Starting...")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    if settings.llm_provider == "ollama":
        logger.info(f"Ollama URL: {settings.ollama_base_url}")
        logger.info(f"Ollama Model: {settings.ollama_model}")
    else:
        logger.info(f"OpenAI Model: {settings.openai_model}")
    logger.info(f"Global Semaphore Limit: {settings.global_semaphore_limit}")
    logger.info(f"Internal Semaphore Limit: {settings.internal_semaphore_limit}")
    logger.info("=" * 50)


@app.get("/")
async def root():
    return {
        "service": "AI Code Analysis Service",
        "status": "running",
        "llm_provider": settings.llm_provider
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
