"""Main FastAPI application for RAG App."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .api import upload, query
from .core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    print("🚀 Starting RAG App...")
    print(f"📁 ChromaDB persist directory: {settings.chroma_persist_directory}")
    print(f"🤖 Using OpenAI model: {settings.openai_model}")
    yield
    # Shutdown
    print("👋 Shutting down RAG App...")


# Create FastAPI app
app = FastAPI(
    title="RAG App",
    description="AI-Powered Smart Document Research",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(query.router, prefix="/api", tags=["query"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "RAG App - AI-Powered Smart Document Research",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/api/upload-document",
            "query": "/api/query-document",
            "list_documents": "/api/documents",
            "delete_document": "/api/documents/{filename}",
            "clear_documents": "/api/clear-documents"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        reload_dirs=["backend"]
    )
