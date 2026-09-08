"""
BIS AI Assistant — FastAPI Backend (api.py)
Tech 3 (Heet) — Backend / LLM Orchestration Engineer

This is the main application entry point. All endpoint logic lives in
dedicated routers under backend/routers/. This file only handles:
    - App creation & metadata
    - CORS middleware
    - Rate limiting middleware (slowapi)
    - Request logging middleware
    - Health endpoint
    - Router registration
    - Startup / shutdown hooks (via lifespan)

Endpoints (via routers):
    POST /chat                  — Main conversational Q&A (RAG pipeline)
    POST /chat/stream           — Streaming SSE variant of /chat
    POST /search-standards      — Search for Indian Standards by product/keyword
    POST /certification-guide   — Explain BIS certification schemes & processes
    GET  /health                — Health check
"""

from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import settings
from backend.models.schemas import HealthResponse
from backend.routers import chat_router, standards_router, certification_router
from backend.services.llm_wrapper import shutdown_client

# ---------------------------------------------------------------------------
# Rate Limiting (slowapi)
# ---------------------------------------------------------------------------
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded

    limiter = Limiter(key_func=get_remote_address)
    _RATE_LIMITING_AVAILABLE = True
except ImportError:
    limiter = None
    _RATE_LIMITING_AVAILABLE = False

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("bis_assistant")

# ---------------------------------------------------------------------------
# Lifespan — replaces deprecated @app.on_event("startup") / ("shutdown")
# ---------------------------------------------------------------------------
_start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — runs setup before yield, teardown after."""
    logger.info(
        "BIS AI Assistant starting — provider=%s model=%s mock_retriever=%s",
        settings.llm_provider,
        settings.llm_model,
        settings.use_mock_retriever,
    )
    # Pre-warm embeddings and vector store so first request is instantaneous (<20ms)
    try:
        from backend.services.retriever import retrieve
        await retrieve("warmup", top_k=1)
        logger.info("Retriever embeddings and ChromaDB warmed up successfully.")
    except Exception as e:
        logger.warning("Startup retriever warmup: %s", e)

    yield
    logger.info("Shutting down — closing HTTP client")
    await shutdown_client()


# ---------------------------------------------------------------------------
# App initialisation
# ---------------------------------------------------------------------------
app = FastAPI(
    title="BIS AI Assistant",
    description=(
        "AI-powered conversational assistant for Indian Standards & BIS services. "
        "Retrieval-Augmented Generation (RAG) backed, with source citations."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# Attach rate limiter to app state
if _RATE_LIMITING_AVAILABLE and limiter is not None:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    logger.info("Rate limiting enabled (slowapi)")
else:
    logger.warning("slowapi not installed — rate limiting disabled. pip install slowapi to enable.")


# CORS — configurable origins from env (defaults to ["*"] for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Middleware — request logging
# ---------------------------------------------------------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000
    logger.info(
        "%s %s → %s (%.1f ms)",
        request.method, request.url.path, response.status_code, duration,
    )
    return response



# ---------------------------------------------------------------------------
# Health endpoint (kept here — it's simple and doesn't need a router)
# ---------------------------------------------------------------------------
@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Returns service health, uptime, and configured LLM info."""
    return HealthResponse(
        llm_provider=settings.llm_provider,
        llm_model=settings.llm_model,
        uptime_seconds=round(time.time() - _start_time, 2),
    )


# ---------------------------------------------------------------------------
# Register routers
# ---------------------------------------------------------------------------
app.include_router(chat_router)
app.include_router(standards_router)
app.include_router(certification_router)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import os
    import uvicorn
    uvicorn.run(
        "backend.api:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
