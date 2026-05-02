"""Configuration management for RAG App."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    # Google Gemini Configuration
    google_api_key: str
    gemini_model: str = "gemini-1.5-flash"
    gemini_embedding_model: str = "models/embedding-001"

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
