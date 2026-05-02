"""Upload API endpoint for document processing."""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
from pathlib import Path
import shutil

from ..core.rag import rag_service
from ..core.config import settings

router = APIRouter()


@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document.

    Args:
        file: The file to upload (PDF or TXT)

    Returns:
        Status message and number of chunks created
    """
    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="Không có tệp nào được tải lên")

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in [".pdf", ".txt"]:
        raise HTTPException(
            status_code=400,
            detail="Chỉ hỗ trợ tệp PDF và TXT"
        )

    # Create upload directory if it doesn't exist
    upload_dir = Path("./data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Save file
    file_path = upload_dir / file.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi trong khi lưu file: {str(e)}"
        )

    # Process document based on type
    try:
        from langchain.schema import Document

        if file_ext == ".pdf":
            # Process PDF
            from pypdf import PdfReader

            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            document = Document(page_content=text, metadata={"source": file.filename})

        else:  # TXT
            # Process text file
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            document = Document(page_content=text, metadata={"source": file.filename})

        # Add to vector store
        chunks_added = rag_service.add_documents([document])

        return {
            "status": "success",
            "message": f"Tài liệu '{file.filename}' đã được xử lý thành công và thêm vào vector store",
            "chunks_added": chunks_added
        }

    except Exception as e:
        # Clean up file if processing failed
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Lỗi trong khi xử lý tài liệu: {str(e)}"
        )


@router.get("/documents")
async def list_documents():
    """
    List all uploaded documents.

    Returns:
        List of document filenames
    """
    upload_dir = Path("./data/uploads")
    if not upload_dir.exists():
        return {"documents": []}

    documents = [
        f.name for f in upload_dir.iterdir()
        if f.is_file() and not f.name.startswith(".")
    ]

    return {"documents": documents}


@router.delete("/documents/{filename}")
async def delete_document(filename: str):
    """
    Delete a document.

    Args:
        filename: Name of the file to delete

    Returns:
        Status message
    """
    file_path = Path("./data/uploads") / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Tài liệu không tồn tại")

    try:
        file_path.unlink()
        return {
            "status": "success",
            "message": f"Tài liệu '{filename}' đã được xóa thành công"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi trong khi xóa tài liệu: {str(e)}"
        )
