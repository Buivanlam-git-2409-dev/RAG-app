"""Configuration management for RAG App."""
import os
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""

    # Groq Configuration
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

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