"""RAG (Retrieval-Augmented Generation) implementation."""
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from typing import List, Optional
import os
from pathlib import Path

from .config import settings


class RAGService:
    """Service for RAG operations."""

    def __init__(self):
        """Initialize RAG service with embeddings and vector store."""
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.openai_api_key
        )
        self.vector_store = None
        self.qa_chain = None
        self._initialize_vector_store()

    def _initialize_vector_store(self):
        """Initialize or load existing vector store."""
        persist_dir = settings.chroma_persist_directory

        # Create directory if it doesn't exist
        Path(persist_dir).mkdir(parents=True, exist_ok=True)

        # Try to load existing vector store
        if os.path.exists(persist_dir) and os.listdir(persist_dir):
            self.vector_store = Chroma(
                persist_directory=persist_dir,
                embedding_function=self.embeddings
            )
        else:
            # Create new vector store
            self.vector_store = Chroma(
                persist_directory=persist_dir,
                embedding_function=self.embeddings
            )

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

        # Add to vector store
        self.vector_store.add_documents(splits)

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
        if not self.vector_store:
            return {
                "answer": "Không có tài liệu nào trong vector store để truy vấn",
                "sources": []
            }

        # Create retriever
        retriever = self.vector_store.as_retriever(search_kwargs={"k": k})

        # Create LLM
        llm = ChatOpenAI(
            model=settings.openai_model,
            openai_api_key=settings.openai_api_key,
            temperature=0
        )

        # Create prompt template
        from langchain_core.prompts import ChatPromptTemplate

        template = """Answer the question based only on the following context:

{context}

Question: {question}

Answer the question in Vietnamese. If you don't know the answer based on the context, say "Tôi không tìm thấy thông tin này trong tài liệu." """

        prompt = ChatPromptTemplate.from_template(template)

        # Create RAG chain using LCEL
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | prompt
            | llm
            | StrOutputParser()
        )

        # Query and get sources
        retrieved_docs = retriever.invoke(question)
        answer = rag_chain.invoke(question)

        # Extract sources
        sources = []
        for doc in retrieved_docs:
            sources.append({
                "content": doc.page_content[:200] + "...",
                "metadata": doc.metadata
            })

        return {
            "answer": answer,
            "sources": sources
        }

    def clear_store(self):
        """Clear all documents from the vector store."""
        if self.vector_store:
            # Delete all documents
            self.vector_store.delete_collection()
            self._initialize_vector_store()


# Global RAG service instance
rag_service = RAGService()
