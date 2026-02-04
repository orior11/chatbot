"""
FastAPI application entry point.
Wired with config, CORS, and routers; uvicorn runs main:app from backend/.
"""
import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import CORS_ORIGINS, PORT, get_gemini_api_key
from routers import chat_router, health_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: verify Gemini API key is loaded."""
    logger.info("System startup...")
    if get_gemini_api_key():
        logger.info("Gemini API key loaded.")
    else:
        logger.warning("GEMINI_API_KEY is missing!")
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(chat_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
