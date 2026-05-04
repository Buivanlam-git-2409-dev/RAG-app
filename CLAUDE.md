# CLAUDE.md

## Project
AI-Powered Smart Document Research (RAG App) - Ứng dụng cho phép upload tài liệu PDF/Text và đặt câu hỏi dựa trên nội dung tài liệu bằng công nghệ RAG.

## Stack
- **Backend:** Python, FastAPI
- **AI Framework:** LangChain
- **Vector Database:** ChromaDB (local)
- **Embeddings:** HuggingFace (sentence-transformers/all-MiniLM-L6-v2)
- **LLM:** Google Gemini 1.5 Flash
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
- **Last session:** 2026-05-04 — Project completion and testing
- **Backend Completed:**
  - Created project structure (backend, data directories)
  - Implemented FastAPI application with CORS support
  - Created RAG service with ChromaDB integration and HuggingFace embeddings
  - Implemented upload API endpoint (PDF/TXT support)
  - Implemented query API endpoint with source retrieval
  - Added document management endpoints (list, delete, clear)
  - Added configuration management with environment variables
  - Added comprehensive error handling and validation
  - Setup virtual environment and installed dependencies
  - Fixed import issues and RAG service instantiation
  - **Backend server running successfully on port 8001** ✅
- **Frontend Completed:**
  - Created React components with modern UI design
  - Implemented file upload with drag & drop functionality
  - Created chat interface for document queries
  - Added document list display
  - Configured Tailwind CSS with custom theme
  - Set up Vite build system with proxy to backend
  - Created index.css with Tailwind directives and custom styles
  - Installed all dependencies
  - **Frontend dev server running successfully on port 5173** ✅
- **Full Integration Tested:**
  - Backend and frontend servers running
  - API proxy configured correctly
  - Ready for end-to-end testing

## Key Decisions
- Sử dụng ChromaDB local vì dễ setup và không cần external service
- HuggingFace embeddings (local, free) thay vì OpenAI embeddings
- Google Gemini cho LLM vì free tier và good performance
- LangChain cho RAG implementation vì có good documentation và community support
- FastAPI cho backend vì async support và automatic API docs
