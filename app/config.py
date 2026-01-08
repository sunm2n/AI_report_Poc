from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # LLM Configuration
    llm_provider: Literal["openai", "ollama"] = "ollama"

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"

    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"

    # Concurrency Control
    global_semaphore_limit: int = 2
    internal_semaphore_limit: int = 10

    # Temporary Workspace
    temp_workspace: str = "/tmp"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
