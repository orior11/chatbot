"""Pydantic models for chat API request/response."""
from typing import List, Optional

from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Single message: role (user/assistant/system) and content."""

    role: str
    content: str


class ChatRequest(BaseModel):
    """Incoming chat request from the frontend."""

    messages: List[ChatMessage]
    model_name: str = "gemini-1.5-flash"
    user_name: Optional[str] = None
    user_phone: Optional[str] = None


class ChatResponse(BaseModel):
    """Response containing the assistant message."""

    message: ChatMessage
