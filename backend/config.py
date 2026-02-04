"""
Centralized configuration: CORS, port, and environment loading.
Loads .env from project root (parent of backend).
"""
import os
from pathlib import Path

from dotenv import load_dotenv

_BACKEND_DIR = Path(__file__).resolve().parent
_ROOT_DIR = _BACKEND_DIR.parent
_ENV_PATH = _ROOT_DIR / ".env"

if _ENV_PATH.exists():
    load_dotenv(_ENV_PATH)

# Server
PORT = int(os.getenv("CHATBOT_PORT", "3002"))

# CORS: allow React dev server origins
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]


def get_gemini_api_key() -> str | None:
    """Return trimmed GEMINI_API_KEY or None if missing/empty."""
    key = os.getenv("GEMINI_API_KEY")
    if not key or not key.strip():
        return None
    return key.strip()


def get_chat_log_path() -> Path:
    """Path to the Excel chat log file (backend directory)."""
    return _BACKEND_DIR / "chat_logs.xlsx"
