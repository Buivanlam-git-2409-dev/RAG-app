#!/usr/bin/env python3
"""
Quick start script to run RAG App with Groq.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main setup and run function."""
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("=" * 70)
    print("🚀 RAG App with Groq - Quick Start")
    print("=" * 70)
    
    # Step 1: Install dependencies
    print("\n📦 Step 1: Installing dependencies...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"],
            check=True
        )
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("   Try running manually: pip install -r requirements.txt")
        return False
    
    # Step 2: Test Groq connection
    print("\n🔧 Step 2: Testing Groq connection...")
    try:
        result = subprocess.run(
            [sys.executable, "test_groq_setup.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
            return False
    except Exception as e:
        print(f"⚠️  Groq test skipped: {e}")
    
    # Step 3: Run the app
    print("\n🎯 Step 3: Starting RAG App...")
    print("-" * 70)
    try:
        subprocess.run(
            [
                sys.executable, "-m", "uvicorn",
                "backend.main:app",
                "--reload",
                "--host", "0.0.0.0",
                "--port", "8001"
            ]
        )
    except KeyboardInterrupt:
        print("\n\n👋 App stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error running app: {e}")
        return False
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
