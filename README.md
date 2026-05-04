# RAG App - Ứng Dụng Nghiên Cứu Tài Liệu Thông Minh

Ưng dụng full-stack hoàn chỉnh cho phép người dùng tải lên tài liệu (PDF, Text) và đặt câu hỏi dựa trên nội dung tài liệu sử dụng công nghệ RAG (Retrieval-Augmented Generation).

**Tính năng chính:**
- Tải lên và xử lý tài liệu PDF, Text
- Trả lời câu hỏi dựa trên nội dung tài liệu
- Trích dẫn nguồn cho mỗi câu trả lời
- Giao diện trò chuyện hiện đại
- Thiết kế tương thích với mọi thiết bị

## Hướng Dẫn Cài Đặt

### 1. Thiết Lập Môi Trường

```bash
# Tạo môi trường ảo
cd rag-app
python -m venv venv

# Kích hoạt môi trường ảo
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cài đặt các gói phụ thuộc
pip install -r requirements.txt
```

### 2. Cấu Hình Biến Môi Trường

```bash
# Sao chép tệp cấu hình mẫu
cp .env.example .env

# Chỉnh sửa .env và thêm Google Gemini API key của bạn
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-1.5-flash
```

### 3. Chạy Các Máy Chủ

```bash
# Khởi động máy chủ backend
cd backend
uvicorn main:app --reload

# Trong cửa sổ terminal khác, khởi động frontend
cd ..
npm install
npm run dev
```

Máy chủ backend: http://localhost:8001  
Ung dụng frontend: http://localhost:5173

### 4. Kiểm Tra Ứng Dụng

- **Tài liệu API:** http://localhost:8001/docs (Swagger UI)
- **Ứng dụng Web:** http://localhost:5173 (React frontend)

Tải lên tài liệu và đặt câu hỏi thông qua giao diện web!

## Các Điểm Cuối API

### Tải Lên Tài Liệu
```bash
POST /api/upload-document
Content-Type: multipart/form-data

Body: file (PDF hoặc TXT)
```

### Truy Vấn Tài Liệu
```bash
POST /api/query-document
Content-Type: application/json

{
  "question": "Câu hỏi của bạn?",
  "k": 4
}
```

### Liệt Kê Tài Liệu
```bash
GET /api/documents
```

### Xóa Tài Liệu
```bash
DELETE /api/documents/{filename}
```

### Xóa Tất Cả Tài Liệu
```bash
POST /api/clear-documents
```

## Cấu Trúc Dự Án

```
rag-app/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── api/
│   │   ├── upload.py       # Upload endpoints
│   │   └── query.py        # Query endpoints
│   ├── core/
│   │   ├── config.py       # Configuration
│   │   ├── rag.py          # RAG logic
│   │   └── __init__.py     # RAG service instance
│   ├── models/
│   ├── tests/
│   │   └── test_api.py     # Unit tests
│   └── requirements.txt    # Backend dependencies
├── src/
│   ├── App.jsx             # Main React app
│   ├── main.jsx            # React entry point
│   ├── index.css           # Global styles
│   └── components/
│       ├── FileUpload.jsx  # File upload component
│       ├── ChatArea.jsx    # Chat interface
│       └── DocumentList.jsx # Document list
├── data/
│   ├── uploads/            # Uploaded files
│   └── chroma/             # Vector database
├── CLAUDE.md               # Claude Code project documentation
├── README.md               # This file
├── package.json            # Frontend dependencies
├── vite.config.js          # Vite configuration
├── tailwind.config.js      # Tailwind configuration
├── index.html              # HTML entry point
├── requirements.txt        # Root dependencies (if any)
└── .env.example           # Environment variables template
```

## Phát Triển

### Backend
```bash
cd backend
pytest                    # Chạy kiểm tra
pytest -v                # Kết quả chi tiết
ruff check .             # Kiểm tra cách viết code
ruff check . --fix       # Sửa tự động
```

### Frontend
```bash
npm run dev              # Khởi động máy chủ phát triển
npm run build            # Xây dựng cho sản xuất
npm run preview          # Xem trước bản xây dựng
```

## Công Nghệ Sử Dụng

- **Backend:** Python, FastAPI
- **AI Framework:** LangChain
- **Vector Database:** ChromaDB (local)
- **Embeddings:** HuggingFace (sentence-transformers/all-MiniLM-L6-v2)
- **LLM:** Google Gemini 1.5 Flash
- **Frontend:** React (Vite) + Tailwind CSS

## Đóng Góp

Đây là một dự án cá nhân. Hãy tự do fork và thử nghiệm!

## Giấy Phép

MIT
