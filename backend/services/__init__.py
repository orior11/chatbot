"""Business logic: AI and conversation logging."""

from services.ai import UnsupportedModelError, chat
from services.excel_logger import log_conversation

__all__ = ["chat", "UnsupportedModelError", "log_conversation"]
