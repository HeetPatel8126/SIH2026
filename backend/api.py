"""
BIS AI Assistant — FastAPI Backend (api.py)
Tech 3 (Heet) — Backend / LLM Orchestration Engineer

Endpoints:
    POST /chat                  — Main conversational Q&A (RAG pipeline)
    POST /search-standards      — Search for Indian Standards by product/keyword
    POST /certification-guide   — Explain BIS certification schemes & processes
    GET  /health                — Health check
"""

from __future__ import annotations

import logging
import os
import time
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1:8b")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("bis_assistant")

# ---------------------------------------------------------------------------
# Pydantic models — request / response schemas
# ---------------------------------------------------------------------------

class QueryCategory(str, Enum):
    """Intent categories for the query router."""
    STANDARDS = "standards"
    CERTIFICATION = "certification"
    HALLMARKING = "hallmarking"
    CONSUMER = "consumer"
    LAB_SUGGESTION = "lab_suggestion"
    GENERAL = "general"


class Citation(BaseModel):
    """A single source citation attached to an answer."""
    document_name: str = Field(..., description="Name or title of the source document")
    clause: Optional[str] = Field(None, description="Specific clause, section, or page number")
    url: Optional[str] = Field(None, description="Link to the original source if available")
    relevance_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Retrieval similarity score")


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


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "0.1.0"
    llm_provider: str
    llm_model: str
    uptime_seconds: float


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
# Health endpoint
# ---------------------------------------------------------------------------
@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Returns service health, uptime, and configured LLM info."""
    return HealthResponse(
        llm_provider=LLM_PROVIDER,
        llm_model=LLM_MODEL,
        uptime_seconds=round(time.time() - _start_time, 2),
    )


# ---------------------------------------------------------------------------
# POST /chat — Main RAG conversational endpoint
# ---------------------------------------------------------------------------
@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Main conversational endpoint.

    Pipeline:
        1. Detect language (if not provided)
        2. Route query to an intent category
        3. Embed query → retrieve top-k chunks from vector DB
        4. Build prompt (system instructions + context + question)
        5. Call LLM
        6. Extract citations from LLM output
        7. Return answer + citations
    """
    start = time.time()
    session_id = request.session_id or str(uuid.uuid4())

    logger.info("Chat request — session=%s query=%r", session_id, request.query[:80])

    # ------ Step 1: Language detection (placeholder) ------
    detected_lang = request.language or "en"

    # ------ Step 2: Query routing (placeholder — keyword-based stub) ------
    query_category = _classify_query(request.query)
    logger.debug("Query classified as: %s", query_category.value)

    # ------ Step 3: Retrieve relevant chunks (placeholder) ------
    # TODO: Wire to retriever.py once Tech 1 (Rudra) has the vector DB ready
    retrieved_chunks: list[dict] = []
    # Example shape of a chunk:
    # {
    #     "text": "IS 10500 specifies requirements for drinking water...",
    #     "metadata": {"document": "IS 10500:2012", "clause": "4.1", "page": 3},
    #     "score": 0.87
    # }

    # ------ Step 4: Build prompt ------
    prompt = _build_prompt(request.query, retrieved_chunks, query_category, detected_lang)

    # ------ Step 5: Call LLM ------
    # TODO: Replace with actual LLM call via llm_wrapper.py
    llm_answer = _placeholder_llm_call(prompt)

    # ------ Step 6: Extract citations ------
    citations = _extract_citations(retrieved_chunks)

    processing_time = (time.time() - start) * 1000
    return ChatResponse(
        answer=llm_answer,
        citations=citations,
        query_category=query_category,
        session_id=session_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        processing_time_ms=round(processing_time, 2),
    )


# ---------------------------------------------------------------------------
# POST /search-standards — Search Indian Standards
# ---------------------------------------------------------------------------
@app.post("/search-standards", response_model=StandardSearchResponse, tags=["Standards"])
async def search_standards(request: StandardSearchRequest):
    """
    Search for Indian Standards by product name, keyword, or IS code.

    TODO: Wire to the vector DB retriever for semantic search over the
    standards catalog.
    """
    logger.info("Standards search — query=%r top_k=%d", request.query, request.top_k)

    # Placeholder — returns empty until retriever is wired
    # TODO: Implement semantic search over standards catalog
    results: list[StandardResult] = []

    return StandardSearchResponse(
        results=results,
        total_found=len(results),
        query=request.query,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# POST /certification-guide — BIS certification scheme guidance
# ---------------------------------------------------------------------------
@app.post("/certification-guide", response_model=CertificationGuideResponse, tags=["Certification"])
async def certification_guide(request: CertificationGuideRequest):
    """
    Explain BIS certification schemes (ISI, CRS, FMCS, Hallmark, etc.)
    and walk through the application process step-by-step.

    TODO: Wire retriever + LLM call for scheme-specific RAG answers.
    """
    logger.info("Certification guide — query=%r scheme=%s", request.query, request.scheme)

    # Placeholder response
    # TODO: Implement RAG pipeline scoped to certification/scheme documents
    return CertificationGuideResponse(
        answer=(
            "Certification guidance will be available once the knowledge base is "
            "ingested. Please check back after the document pipeline is set up."
        ),
        scheme_identified=request.scheme,
        steps=[],
        citations=[],
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# Internal helpers — stubs to be replaced with real service calls
# ---------------------------------------------------------------------------

def _classify_query(query: str) -> QueryCategory:
    """
    Simple keyword-based query router (placeholder).

    TODO: Replace with a proper classifier in services/query_router.py —
    could be a small fine-tuned model, an LLM-based classifier, or
    an intent detection pipeline.
    """
    q = query.lower()

    if any(kw in q for kw in ["hallmark", "huid", "gold", "silver", "jewellery", "jewelry"]):
        return QueryCategory.HALLMARKING
    if any(kw in q for kw in ["certif", "license", "isi mark", "crs", "fmcs", "scheme", "eco mark"]):
        return QueryCategory.CERTIFICATION
    if any(kw in q for kw in ["complaint", "consumer", "grievance", "verify", "fake"]):
        return QueryCategory.CONSUMER
    if any(kw in q for kw in ["lab", "laboratory", "testing", "test near"]):
        return QueryCategory.LAB_SUGGESTION
    if any(kw in q for kw in ["standard", "is code", "is ", "indian standard", "bis"]):
        return QueryCategory.STANDARDS

    return QueryCategory.GENERAL


def _build_prompt(
    query: str,
    chunks: list[dict],
    category: QueryCategory,
    language: str,
) -> str:
    """
    Assemble the prompt for the LLM.

    TODO: Move to services/prompt_builder.py with proper templates
    from prompts/templates.py.
    """
    context_block = "\n\n---\n\n".join(
        f"[Source: {c['metadata'].get('document', 'Unknown')} | "
        f"Clause: {c['metadata'].get('clause', 'N/A')}]\n{c['text']}"
        for c in chunks
    ) or "(No relevant context retrieved yet — knowledge base not loaded.)"

    system_prompt = (
        "You are the BIS AI Assistant — an expert on Indian Standards and "
        "Bureau of Indian Standards (BIS) services. You MUST:\n"
        "1. Answer ONLY based on the provided context below.\n"
        "2. If the context does not contain enough information, say: "
        "\"I could not find this information in the available BIS sources.\"\n"
        "3. ALWAYS cite the specific document and clause you are referencing.\n"
        "4. Keep answers clear, concise, and in plain language.\n"
        "5. Never fabricate IS codes, fee amounts, or process steps.\n"
    )

    if language != "en":
        system_prompt += f"\n6. Respond in the language with ISO code: {language}\n"

    return (
        f"{system_prompt}\n\n"
        f"### Query Category: {category.value}\n\n"
        f"### Retrieved Context:\n{context_block}\n\n"
        f"### User Question:\n{query}\n\n"
        f"### Your Answer (with citations):"
    )


def _placeholder_llm_call(prompt: str) -> str:
    """
    Placeholder LLM call — returns a canned response.

    TODO: Replace with actual call to Ollama / OpenAI / Anthropic
    in services/llm_wrapper.py.
    """
    logger.debug("LLM prompt length: %d chars", len(prompt))
    return (
        "🔧 **LLM not connected yet.** This is a placeholder response.\n\n"
        "The BIS AI Assistant backend is running successfully. "
        "Once the knowledge base is ingested (Tech 1 & 2) and the LLM wrapper "
        "is wired up, this endpoint will return grounded, cited answers about "
        "Indian Standards and BIS services.\n\n"
        "Try the `/health` endpoint to verify the server is running, "
        "or the `/docs` endpoint for interactive API documentation."
    )


def _extract_citations(chunks: list[dict]) -> list[Citation]:
    """
    Build citation objects from retrieved chunks.

    TODO: Enhance in services/citation.py to also parse inline
    references from the LLM's generated text.
    """
    citations = []
    for chunk in chunks:
        meta = chunk.get("metadata", {})
        citations.append(
            Citation(
                document_name=meta.get("document", "Unknown"),
                clause=meta.get("clause"),
                url=meta.get("url"),
                relevance_score=chunk.get("score"),
            )
        )
    return citations


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=DEBUG,
    )
