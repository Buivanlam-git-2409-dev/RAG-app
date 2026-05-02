# CLAUDE.md

## Project
AI-Powered Smart Document Research (RAG App) - Ứng dụng cho phép upload tài liệu PDF/Text và đặt câu hỏi dựa trên nội dung tài liệu bằng công nghệ RAG.

## Stack
- **Backend:** Python, FastAPI
- **AI Framework:** LangChain
- **Vector Database:** ChromaDB (local)
- **LLM:** OpenAI GPT-4o/mini
- **Frontend:** React (Vite) + Tailwind CSS

## Commands
```bash
# Backend
cd backend
python -m venv venv              # Tạo virtual environment
source venv/bin/activate         # Activate (Linux/Mac)
venv\Scripts\activate            # Activate (Windows)
pip install -r requirements.txt  # Install dependencies
uvicorn main:app --reload        # Start dev server

# Testing
pytest                           # Run tests
pytest -v                        # Verbose output

# Linting
ruff check .                     # Check code style
ruff check . --fix              # Auto-fix issues
```

## Conventions
- Python code follows PEP 8
- API endpoints use kebab-case: `/upload-document`, `/query-document`
- JSON fields use camelCase
- All API responses include `status` field

## YOU MUST
- Luôn chạy tests sau khi thay đổi logic
- Sử dụng environment variables cho API keys (không hardcode)
- Validate input data ở API layer
- Log errors với context đầy đủ
- Không commit file `.env` hoặc API keys

## Current State
- **Last session:** 2026-05-01 — Completed backend foundation setup
- **Completed:**
  - Created project structure (backend, data directories)
  - Implemented FastAPI application with CORS support
  - Created RAG service with ChromaDB integration
  - Implemented upload API endpoint (PDF/TXT support)
  - Implemented query API endpoint with source retrieval
  - Added document management endpoints (list, delete, clear)
  - Created configuration management with environment variables
  - Added comprehensive error handling and validation
- **In progress:** Testing and validation
- **Next:** Setup virtual environment, install dependencies, test API endpoints

## Key Decisions
- Sử dụng ChromaDB local vì dễ setup và không cần external service
- LangChain cho RAG implementation vì có good documentation và community support
- FastAPI cho backend vì async support và automatic API docs
