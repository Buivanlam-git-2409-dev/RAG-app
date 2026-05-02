"""Basic tests for RAG App."""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
import os

from backend.main import app


client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "RAG App" in data["message"]


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_list_documents_empty():
    """Test listing documents when none exist."""
    response = client.get("/api/documents")
    assert response.status_code == 200
    data = response.json()
    assert "documents" in data


def test_query_without_documents():
    """Test query when no documents are uploaded."""
    response = client.post(
        "/api/query-document",
        json={"question": "Test question", "k": 4}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    # Should return a message about no documents


def test_query_empty_question():
    """Test query with empty question."""
    response = client.post(
        "/api/query-document",
        json={"question": "", "k": 4}
    )
    assert response.status_code == 400


def test_upload_no_file():
    """Test upload without file."""
    response = client.post("/api/upload-document")
    assert response.status_code == 422  # Unprocessable Entity


def test_upload_unsupported_format():
    """Test upload with unsupported file format."""
    # Create a temporary .docx file
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
        f.write(b"test content")
        temp_path = f.name

    try:
        with open(temp_path, "rb") as f:
            response = client.post(
                "/api/upload-document",
                files={"file": ("test.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
            )
        assert response.status_code == 400
    finally:
        os.unlink(temp_path)


def test_clear_documents():
    """Test clearing all documents."""
    response = client.post("/api/clear-documents")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
