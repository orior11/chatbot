"""Chat API: POST /chat."""
import logging

from fastapi import APIRouter, HTTPException

from models import ChatMessage, ChatRequest, ChatResponse
from services import UnsupportedModelError, chat, log_conversation

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Process chat messages with Gemini and return assistant reply.
    Optionally logs the interaction to Excel when user_name and user_phone are set.
    """
    messages_dicts = [{"role": m.role, "content": m.content} for m in request.messages]

    try:
        ai_content = chat(messages=messages_dicts, model_name=request.model_name)
    except UnsupportedModelError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.exception("AI error")
        raise HTTPException(status_code=500, detail=f"AI Service Error: {str(e)}") from e

    if not ai_content:
        ai_content = "The AI returned an empty response."

    if request.user_name and request.user_phone:
        try:
            last_user_msg = (
                request.messages[-1].content if request.messages else "No Content"
            )
            interaction_log = f"User: {last_user_msg} | AI: {ai_content}"
            log_conversation(
                request.user_name, request.user_phone, interaction_log
            )
        except Exception as e:
            logger.warning("Excel log error: %s", e)

    return ChatResponse(
        message=ChatMessage(role="assistant", content=ai_content)
    )
