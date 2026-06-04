#!/usr/bin/env python3
"""Quick test script to verify Groq API configuration."""

import os
import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_groq_connection():
    """Test if Groq API connection works."""
    from dotenv import load_dotenv
    
    # Load environment variables
    env_path = project_root / "backend" / ".env"
    load_dotenv(env_path)
    
    # Import settings
    from backend.core.config import settings
    
    print("=" * 60)
    print("🔧 RAG App - Groq Configuration Test")
    print("=" * 60)
    
    # Check if API key is set
    if not settings.groq_api_key:
        print("❌ GROQ_API_KEY is not set in .env file")
        return False
    
    print(f"✅ GROQ_API_KEY: {settings.groq_api_key[:20]}...***")
    print(f"✅ GROQ_MODEL: {settings.groq_model}")
    print(f"✅ ChromaDB Directory: {settings.chroma_persist_directory}")
    print(f"✅ Server: {settings.host}:{settings.port}")
    print()
    
    # Test Groq import
    try:
        from langchain_groq import ChatGroq
        print("✅ langchain_groq imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langchain_groq: {e}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    # Test API connection
    try:
        print("\n⏳ Testing Groq API connection...")
        llm = ChatGroq(
            model=settings.groq_model,
            groq_api_key=settings.groq_api_key,
            temperature=0
        )
        
        response = llm.invoke("Hello, are you Groq?")
        print(f"✅ Groq API Response: {response.content[:100]}...")
        
    except Exception as e:
        print(f"❌ Groq API Error: {e}")
        return False
    
    # Test RAG Service
    try:
        print("\n⏳ Initializing RAG Service...")
        from backend.core.rag import rag_service
        print("✅ RAG Service initialized successfully")
        
        # Check vector store
        collection_count = rag_service.collection.count()
        print(f"✅ Vector Store Status: {collection_count} documents")
        
    except Exception as e:
        print(f"❌ RAG Service Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All checks passed! Ready to run RAG App with Groq")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("   1. Run: python -m uvicorn backend.main:app --reload")
    print("   2. Visit: http://localhost:8001")
    print("   3. Upload documents and query them!")
    
    return True


if __name__ == "__main__":
    success = test_groq_connection()
    sys.exit(0 if success else 1)
