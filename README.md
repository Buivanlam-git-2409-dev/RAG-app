# RAG App - AI-Powered Smart Document Research

Ứng dụng cho phép upload tài liệu (PDF, Text) và đặt câu hỏi dựa trên nội dung tài liệu bằng công nghệ RAG (Retrieval-Augmented Generation).

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Tạo virtual environment
cd rag-app
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env và thêm OpenAI API key của bạn
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run Server

```bash
# Start development server
cd backend
uvicorn main:app --reload
```

Server sẽ chạy tại: http://localhost:8001

### 4. Test API

Mở browser và truy cập: http://localhost:8001/docs

Đây là Swagger UI - bạn có thể test tất cả API endpoints trực tiếp.

## 📚 API Endpoints

### Upload Document
```bash
POST /api/upload-document
Content-Type: multipart/form-data

Body: file (PDF or TXT)
```

### Query Document
```bash
POST /api/query-document
Content-Type: application/json

{
  "question": "Câu hỏi của bạn?",
  "k": 4
}
```

### List Documents
```bash
GET /api/documents
```

### Delete Document
```bash
DELETE /api/documents/{filename}
```

### Clear All Documents
```bash
POST /api/clear-documents
```

## 🏗️ Project Structure

```
rag-app/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── api/
│   │   ├── upload.py       # Upload endpoints
│   │   └── query.py        # Query endpoints
│   ├── core/
│   │   ├── config.py       # Configuration
│   │   └── rag.py          # RAG logic
│   └── models/
├── data/
│   ├── uploads/            # Uploaded files
│   └── chroma/             # Vector database
├── CLAUDE.md               # Claude Code project documentation
├── requirements.txt        # Python dependencies
└── .env.example           # Environment variables template
```

## 🔧 Development

### Run Tests
```bash
pytest
```

### Lint Code
```bash
ruff check .
ruff check . --fix
```

## 📖 Tech Stack

- **Backend:** Python, FastAPI
- **AI Framework:** LangChain
- **Vector Database:** ChromaDB (local)
- **LLM:** OpenAI GPT-4o/mini
- **Frontend:** React (Vite) + Tailwind CSS (coming soon)

## 🤝 Contributing

This is a learning project. Feel free to fork and experiment!

## 📝 License

MIT
