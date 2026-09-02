"""
BIS AI Assistant — FastAPI Backend (api.py)
Tech 3 (Heet) — Backend / LLM Orchestration Engineer

This is the main application entry point. All endpoint logic lives in
dedicated routers under backend/routers/. This file only handles:
    - App creation & metadata
    - CORS middleware
    - Request logging middleware
    - Health endpoint
    - Router registration
    - Startup / shutdown hooks

Endpoints (via routers):
    POST /chat                  — Main conversational Q&A (RAG pipeline)
    POST /search-standards      — Search for Indian Standards by product/keyword
    POST /certification-guide   — Explain BIS certification schemes & processes
    GET  /health                — Health check
"""

from __future__ import annotations

import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.models.schemas import HealthResponse
from backend.routers import chat_router, standards_router, certification_router
from backend.services.llm_wrapper import shutdown_client

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("bis_assistant")

# ---------------------------------------------------------------------------
# App initialisation
# ---------------------------------------------------------------------------
_start_time = time.time()

app = FastAPI(
    title="BIS AI Assistant",
    description=(
        "AI-powered conversational assistant for Indian Standards & BIS services. "
        "Retrieval-Augmented Generation (RAG) backed, with source citations."
    ),
    version="0.1.0",
)

# CORS — allow the frontend (React / Streamlit) to talk to us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # tighten for production
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
# Lifecycle hooks
# ---------------------------------------------------------------------------
@app.on_event("startup")
async def on_startup():
    logger.info(
        "BIS AI Assistant starting — provider=%s model=%s mock_retriever=%s",
        settings.llm_provider,
        settings.llm_model,
        settings.use_mock_retriever,
    )


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutting down — closing HTTP client")
    await shutdown_client()


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
