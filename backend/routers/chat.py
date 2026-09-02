"""
BIS AI Assistant — Chat Router

POST /chat — Main conversational Q&A endpoint (RAG pipeline).

Pipeline:
    1. Detect language (if not provided)
    2. Route query to an intent category
    3. Retrieve top-k chunks from vector DB
    4. Build prompt (system instructions + context + question)
    5. Call LLM
    6. Extract and merge citations
    7. Return answer + citations
"""

from __future__ import annotations

import logging
import time
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter

from backend.models.schemas import ChatRequest, ChatResponse
from backend.services.query_router import classify_query
from backend.services.prompt_builder import build_prompt
from backend.services.llm_wrapper import call_llm
from backend.services.retriever import retrieve
from backend.services.citation import extract_from_chunks, parse_inline_citations, merge_citations
from backend.services.language_detect import detect_language

logger = logging.getLogger("bis_assistant.router.chat")

router = APIRouter(tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main conversational endpoint — full RAG pipeline.
    """
    start = time.time()
    session_id = request.session_id or str(uuid.uuid4())

    logger.info("Chat request — session=%s query=%r", session_id, request.query[:80])

    # Step 1: Language detection
    detected_lang = request.language or "en"
    if detected_lang == "en":
        # Auto-detect if the user didn't explicitly specify or left default
        auto_lang = detect_language(request.query)
        if auto_lang != "en":
            detected_lang = auto_lang
            logger.info("Auto-detected language: %s", detected_lang)

    # Step 2: Query routing
    query_category = classify_query(request.query)
    logger.debug("Query classified as: %s", query_category.value)

    # Step 3: Retrieve relevant chunks
    retrieved_chunks = await retrieve(
        query=request.query,
        category=query_category,
    )
    logger.debug("Retrieved %d chunks", len(retrieved_chunks))

    # Step 4: Build prompt
    prompt = build_prompt(
        query=request.query,
        chunks=retrieved_chunks,
        category=query_category,
        language=detected_lang,
    )

    # Step 5: Call LLM
    llm_answer = await call_llm(prompt)

    # Step 6: Extract and merge citations
    chunk_citations = extract_from_chunks(retrieved_chunks)
    inline_citations = parse_inline_citations(llm_answer)
    citations = merge_citations(chunk_citations, inline_citations)

    processing_time = (time.time() - start) * 1000

    return ChatResponse(
        answer=llm_answer,
        citations=citations,
        query_category=query_category,
        session_id=session_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        processing_time_ms=round(processing_time, 2),
    )
