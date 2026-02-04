"""Health check endpoint."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    """Return service status."""
    return {"status": "ok", "service": "chatbot-backend"}
