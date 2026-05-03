"""Query API endpoint for RAG operations."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

try:
    from ..core.rag import rag_service
except ImportError:
    from core.rag import rag_service

router = APIRouter()


class QueryRequest(BaseModel):
    """Request model for query endpoint."""

    question: str = Field(..., description="Câu hỏi để truy vấn tài liệu")
    k: int = Field(default=4, ge=1, le=10, description="Số lượng nguồn để truy xuất (mặc định là 4, tối đa là 10)")


class QueryResponse(BaseModel):
    """Response model for query endpoint."""

    status: str
    answer: str
    sources: list


@router.post("/query-document", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    """
    Query the document collection with a question.

    Args:
        request: QueryRequest containing question and optional k parameter

    Returns:
        QueryResponse with answer and sources
    """
    if not request.question or not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Câu hỏi không thể để trống"
        )

    try:
        result = rag_service.query(request.question, k=request.k)

        return QueryResponse(
            status="success",
            answer=result["answer"],
            sources=result["sources"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi trong khi xử lý truy vấn: {str(e)}"
        )


@router.post("/clear-documents")
async def clear_documents():
    """
    Clear all documents from the vector store.

    Returns:
        Status message
    """
    try:
        rag_service.clear_store()
        return {
            "status": "success",
            "message": "Tất cả tài liệu đã được xóa khỏi vector store"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi trong khi xóa tài liệu: {str(e)}"
        )
