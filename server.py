#!/usr/bin/env python3
"""
MediLink Enterprise — Full-Stack Hospital Management & Unified Medical Records System
Production FastAPI REST API & EMR Frontend Server.

Usage:
    python server.py
    python server.py 8080
"""

import sys
import os
import webbrowser
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import uvicorn
from backend.app.config import settings

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
HOST = "127.0.0.1"

def run():
    url = f"http://localhost:{PORT}"
    print("=" * 70)
    print("  🏥  MediLink: Aadhaar-Based Unified Medical Records System")
    print("  Enterprise Hospital Management & Interoperability Network v4.0")
    print("=" * 70)
    print(f"  > Server URL:       {url}")
    print(f"  > REST API Docs:    {url}/docs")
    print(f"  > Database Engine:  {settings.DB_ENGINE}")
    print(f"  > Base Directory:   {BASE_DIR}")
    print("=" * 70)
    print("  > Press Ctrl+C to terminate the server.\n")

    try:
        webbrowser.open(url)
    except Exception:
        pass

    uvicorn.run(
        "backend.app.main:app",
        host=HOST,
        port=PORT,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    run()
