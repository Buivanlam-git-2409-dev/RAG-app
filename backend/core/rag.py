"""RAG (Retrieval-Augmented Generation) implementation."""

import os
os.environ["CHROMA_TELEMETRY_DISABLED"] = "true"

from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List, Optional
import os
from pathlib import Path
import chromadb
import uuid

from .config import settings


class RAGService:
    """Service for RAG operations."""

    def __init__(self):
        """Initialize RAG service with embeddings and vector store."""
        # Dùng HuggingFace embeddings (free, local, không cần API key)
        print("[RAG] Initializing HuggingFace embeddings...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        print("[RAG] ✅ Embeddings initialized")
        
        # ✅ Dùng ChromaDB client với cấu hình mới
        from pathlib import Path
        persist_dir = Path(settings.chroma_persist_directory)
        persist_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"[RAG] Initializing ChromaDB at: {persist_dir}")
        
        self.chroma_client = chromadb.PersistentClient(
            path=str(persist_dir)
        )
        
        # Tạo hoặc lấy collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="rag_documents"
        )
        print(f"[RAG] ✅ ChromaDB initialized (docs count: {self.collection.count()})")
        
        self.qa_chain = None

    def add_documents(self, documents: List[Document]) -> int:
        """
        Add documents to the vector store.

        Args:
            documents: List of Document objects to add

        Returns:
            Number of documents added
        """
        if not documents:
            return 0

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        splits = text_splitter.split_documents(documents)
        
        # Chuyển đổi sang format cho ChromaDB
        ids = [str(uuid.uuid4()) for _ in splits]
        texts = [split.page_content for split in splits]
        metadatas = [split.metadata for split in splits]
        
        # Tạo embeddings
        print(f"Đang tạo embeddings cho {len(splits)} chunks...")
        embeddings = []
        for text in texts:
            emb = self.embeddings.embed_query(text)
            embeddings.append(emb)
        
        # Thêm vào collection
        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings
        )
        
        print(f"✅ Đã thêm {len(splits)} chunks vào database")
        return len(splits)

    def query(self, question: str, k: int = 4) -> dict:
        """
        Query the vector store with a question.

        Args:
            question: The question to ask
            k: Number of relevant documents to retrieve

        Returns:
            Dictionary with answer and sources
        """
        # Kiểm tra xem có dữ liệu không
        try:
            collection_count = self.collection.count()
            if collection_count == 0:
                return {
                    "answer": "Không có tài liệu nào trong vector store để truy vấn",
                    "sources": []
                }
        except Exception as e:
            return {
                "answer": f"Lỗi khi kiểm tra database: {str(e)}",
                "sources": []
            }

        try:
            # Tạo embedding cho câu hỏi
            question_embedding = self.embeddings.embed_query(question)
            
            # Tìm kiếm bằng embedding
            results = self.collection.query(
                query_embeddings=[question_embedding],
                n_results=k
            )
            
            if not results.get('documents') or len(results['documents']) == 0 or len(results['documents'][0]) == 0:
                return {
                    "answer": "Không tìm thấy thông tin liên quan trong tài liệu.",
                    "sources": []
                }
            
            # Lấy kết quả
            contexts = results['documents'][0]
            sources = []
            
            for i, meta in enumerate(results.get('metadatas', [[]])[0] if results.get('metadatas') else []):
                sources.append({
                    "content": contexts[i][:200] + "..." if len(contexts[i]) > 200 else contexts[i],
                    "metadata": meta
                })
            
            # Tạo prompt
            context_text = "\n\n".join(contexts)
            
            prompt = f"""Answer the question based only on the following context:

{context_text}

Question: {question}

Answer the question in Vietnamese. If you don't know the answer based on the context, say "Tôi không tìm thấy thông tin này trong tài liệu." """

            # Create LLM
            llm = ChatGroq(
                model=settings.groq_model,
                groq_api_key=settings.groq_api_key,
                temperature=0
            )
            
            # Gọi LLM trực tiếp
            response = llm.invoke(prompt)

            return {
                "answer": response.content,
                "sources": sources
            }
        except Exception as e:
            return {
                "answer": f"Lỗi xử lý: {str(e)}",
                "sources": []
            }

    def clear_store(self):
        """Clear all documents from the vector store."""
        try:
            self.chroma_client.delete_collection("rag_documents")
        except:
            pass
        self.collection = self.chroma_client.create_collection("rag_documents")


# Global RAG service instance
rag_service = RAGService()