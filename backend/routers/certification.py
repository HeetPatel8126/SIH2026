"""
BIS AI Assistant — Certification Guide Router

POST /certification-guide — Explain BIS certification schemes & processes.

Uses the retriever with CERTIFICATION category filter, then the LLM
to generate a structured answer with steps and citations.
"""

from __future__ import annotations

import logging
import re
import time
from datetime import datetime, timezone

from fastapi import APIRouter

from backend.models.schemas import (
    CertificationGuideRequest,
    CertificationGuideResponse,
    QueryCategory,
)
from backend.services.query_router import classify_query
from backend.services.prompt_builder import build_prompt
from backend.services.llm_wrapper import call_llm
from backend.services.retriever import retrieve
from backend.services.citation import extract_from_chunks, parse_inline_citations, merge_citations

logger = logging.getLogger("bis_assistant.router.certification")

router = APIRouter(tags=["Certification"])

# Known scheme keywords for identification
_SCHEME_KEYWORDS: dict[str, list[str]] = {
    "ISI": ["isi mark", "isi certification", "scheme i", "scheme 1", "product certification"],
    "CRS": ["crs", "compulsory registration", "scheme ii", "scheme 2"],
    "FMCS": ["fmcs", "foreign manufacturer"],
    "Hallmark": ["hallmark", "hallmarking", "huid", "gold", "silver", "jewellery", "jewelry"],
    "Scheme X": ["scheme x"],
    "ECO Mark": ["eco mark", "ecomark", "eco-mark"],
}


def _identify_scheme(query: str, explicit_scheme: str | None) -> str | None:
    """Identify the BIS scheme being asked about."""
    if explicit_scheme:
        return explicit_scheme

    q_lower = query.lower()
    for scheme, keywords in _SCHEME_KEYWORDS.items():
        if any(kw in q_lower for kw in keywords):
            return scheme

    return None


def _extract_steps(text: str) -> list[str]:
    """
    Extract numbered steps from LLM output.

    Looks for patterns like:
        1. Step one
        2. Step two
    or
        (1) Step one
        (2) Step two
    """
    # Try numbered list pattern: "1. ...", "2. ..." etc.
    steps = re.findall(r"(?:^|\n)\s*\d+[\.\)]\s*(.+?)(?=\n\s*\d+[\.\)]|\n\n|$)", text, re.DOTALL)

    if steps:
        return [step.strip() for step in steps if step.strip()]

    # Try bullet points: "- ..." or "• ..."
    bullets = re.findall(r"(?:^|\n)\s*[-•]\s*(.+?)(?=\n\s*[-•]|\n\n|$)", text, re.DOTALL)
    if bullets:
        return [b.strip() for b in bullets if b.strip()]

    return []


@router.post("/certification-guide", response_model=CertificationGuideResponse)
async def certification_guide(request: CertificationGuideRequest):
    """
    Explain BIS certification schemes (ISI, CRS, FMCS, Hallmark, etc.)
    and walk through the application process step-by-step.
    """
    start = time.time()
    logger.info("Certification guide — query=%r scheme=%s", request.query, request.scheme)

    # Identify the scheme
    scheme = _identify_scheme(request.query, request.scheme)

    # Determine retrieval category — hallmarking has its own
    retrieval_category = QueryCategory.CERTIFICATION
    if scheme == "Hallmark":
        retrieval_category = QueryCategory.HALLMARKING

    # Retrieve relevant chunks
    chunks = await retrieve(
        query=request.query,
        category=retrieval_category,
    )

    # Build prompt
    prompt = build_prompt(
        query=request.query,
        chunks=chunks,
        category=retrieval_category,
    )

    # Call LLM
    llm_answer = await call_llm(prompt)

    # Extract steps from the answer
    steps = _extract_steps(llm_answer)

    # Extract citations
    chunk_citations = extract_from_chunks(chunks)
    inline_citations = parse_inline_citations(llm_answer)
    citations = merge_citations(chunk_citations, inline_citations)

    processing_time = (time.time() - start) * 1000
    logger.info(
        "Certification guide complete — scheme=%s, steps=%d, citations=%d in %.1f ms",
        scheme, len(steps), len(citations), processing_time,
    )

    return CertificationGuideResponse(
        answer=llm_answer,
        scheme_identified=scheme,
        steps=steps,
        citations=citations,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
