"""
BIS AI Assistant — Pydantic Schemas

Centralized request/response models used across the API.
Extracted from api.py for clean separation.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class QueryCategory(str, Enum):
    """Intent categories for the query router."""
    STANDARDS = "standards"
    CERTIFICATION = "certification"
    HALLMARKING = "hallmarking"
    CONSUMER = "consumer"
    LAB_SUGGESTION = "lab_suggestion"
    GENERAL = "general"


# ---------------------------------------------------------------------------
# Shared sub-models
# ---------------------------------------------------------------------------

class Citation(BaseModel):
    """A single source citation attached to an answer."""
    document_name: str = Field(..., description="Name or title of the source document")
    clause: Optional[str] = Field(None, description="Specific clause, section, or page number")
    url: Optional[str] = Field(None, description="Link to the original source if available")
    relevance_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Retrieval similarity score")


# ---------------------------------------------------------------------------
# /chat
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    """Payload for the /chat endpoint."""
    query: str = Field(..., min_length=1, max_length=2000, description="User's question in natural language")
    language: Optional[str] = Field("en", description="ISO 639-1 language code (e.g. 'en', 'hi')")
    session_id: Optional[str] = Field(None, description="Optional session ID for conversation continuity")


class ChatResponse(BaseModel):
    """Response from the /chat endpoint."""
    answer: str
    citations: list[Citation] = []
    query_category: QueryCategory
    session_id: str
    timestamp: str
    processing_time_ms: float


# ---------------------------------------------------------------------------
# /search-standards
# ---------------------------------------------------------------------------

class StandardSearchRequest(BaseModel):
    """Payload for the /search-standards endpoint."""
    query: str = Field(..., min_length=1, max_length=1000, description="Product name, keyword, or IS code")
    top_k: int = Field(5, ge=1, le=20, description="Number of results to return")


class StandardResult(BaseModel):
    """A single Indian Standard result."""
    is_code: str = Field(..., description="Indian Standard code, e.g. IS 10500")
    title: str
    summary: Optional[str] = None
    relevance_score: Optional[float] = None


class StandardSearchResponse(BaseModel):
    """Response from the /search-standards endpoint."""
    results: list[StandardResult] = []
    total_found: int = 0
    query: str
    timestamp: str


# ---------------------------------------------------------------------------
# /certification-guide
# ---------------------------------------------------------------------------

class CertificationGuideRequest(BaseModel):
    """Payload for the /certification-guide endpoint."""
    query: str = Field(..., min_length=1, max_length=1000, description="Question about BIS certification")
    scheme: Optional[str] = Field(
        None,
        description="Specific scheme filter: ISI, CRS, FMCS, Hallmark, SchemeX, ECOMark"
    )


class CertificationGuideResponse(BaseModel):
    """Response from the /certification-guide endpoint."""
    answer: str
    scheme_identified: Optional[str] = None
    steps: list[str] = []
    citations: list[Citation] = []
    timestamp: str


# ---------------------------------------------------------------------------
# /health
# ---------------------------------------------------------------------------

class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "0.1.0"
    llm_provider: str
    llm_model: str
    uptime_seconds: float
