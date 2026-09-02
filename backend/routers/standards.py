"""
BIS AI Assistant — Standards Search Router

POST /search-standards — Search Indian Standards by product/keyword/IS code.

Uses the retriever with STANDARDS category filter to find matching standards.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone

from fastapi import APIRouter

from backend.models.schemas import (
    StandardSearchRequest,
    StandardSearchResponse,
    StandardResult,
    QueryCategory,
)
from backend.services.retriever import retrieve

logger = logging.getLogger("bis_assistant.router.standards")

router = APIRouter(tags=["Standards"])


@router.post("/search-standards", response_model=StandardSearchResponse)
async def search_standards(request: StandardSearchRequest):
    """
    Search for Indian Standards by product name, keyword, or IS code.

    Retrieves matching chunks from the standards knowledge base and
    extracts IS codes, titles, and summaries.
    """
    start = time.time()
    logger.info("Standards search — query=%r top_k=%d", request.query, request.top_k)

    # Retrieve chunks scoped to standards
    chunks = await retrieve(
        query=request.query,
        top_k=request.top_k,
        category=QueryCategory.STANDARDS,
    )

    # Convert chunks to StandardResult objects
    results: list[StandardResult] = []
    seen_codes: set[str] = set()

    for chunk in chunks:
        meta = chunk.get("metadata", {})
        doc_name = meta.get("document", "Unknown")

        # Extract IS code from document name (e.g., "IS 10500:2012" → "IS 10500")
        is_code = doc_name.split("—")[0].strip() if "—" in doc_name else doc_name

        if is_code in seen_codes:
            continue
        seen_codes.add(is_code)

        # Extract title from the text (first sentence or the full doc name)
        text = chunk.get("text", "")
        title = doc_name
        if "—" in text:
            # Try to extract title from text like "IS 10500:2012 — Drinking Water — Specification"
            parts = text.split("—", 2)
            if len(parts) >= 2:
                title = parts[1].strip().rstrip(".")
                if len(parts) >= 3:
                    subtitle = parts[2].strip().split(".")[0]
                    title = f"{title} — {subtitle}"

        results.append(
            StandardResult(
                is_code=is_code,
                title=title,
                summary=text[:300] + ("..." if len(text) > 300 else ""),
                relevance_score=chunk.get("score"),
            )
        )

    processing_time = (time.time() - start) * 1000
    logger.info(
        "Standards search complete — %d results in %.1f ms",
        len(results), processing_time,
    )

    return StandardSearchResponse(
        results=results,
        total_found=len(results),
        query=request.query,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
