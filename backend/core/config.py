"""Configuration management for RAG App."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"

    # ChromaDB Configuration
    chroma_persist_directory: str = "./data/chroma"

    # Server Configuration
    host: str = "http://localhost"
    port: int = 8001

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
