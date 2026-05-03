"""Configuration management for RAG App."""
import os
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""

    # Google Gemini Configuration
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    gemini_embedding_model: str = os.getenv("GEMINI_EMBEDDING_MODEL", "models/text-embedding-004")

    # ChromaDB Configuration
    chroma_persist_directory: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")

    # Server Configuration
    host: str = os.getenv("HOST", "localhost")
    port: int = int(os.getenv("PORT", "8001"))

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Bỏ qua fields không cần thiết


# Global settings instance
settings = Settings()