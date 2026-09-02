"""
BIS AI Assistant — Citation Extraction Service

Builds citation objects from retrieved chunks and parses inline references
from LLM output text.
"""

from __future__ import annotations

import logging
import re
from typing import Optional

from backend.models.schemas import Citation

logger = logging.getLogger("bis_assistant.citation")

# Pattern to match [Source: <doc> | Clause: <clause>] in LLM output
_INLINE_CITATION_PATTERN = re.compile(
    r"\[Source:\s*(?P<document>[^|\]]+)"
    r"(?:\s*\|\s*Clause:\s*(?P<clause>[^\]]*))?"
    r"\]",
    re.IGNORECASE,
)


def extract_from_chunks(chunks: list[dict]) -> list[Citation]:
    """
    Build Citation objects from retrieved chunk metadata.

    Args:
        chunks: List of chunk dicts with 'metadata' and optional 'score'.

    Returns:
        List of Citation objects, deduplicated by document name.
    """
    citations: list[Citation] = []
    seen_docs: set[str] = set()

    for chunk in chunks:
        meta = chunk.get("metadata", {})
        doc_name = meta.get("document", "Unknown")

        # Deduplicate by document name + clause
        dedup_key = f"{doc_name}|{meta.get('clause', '')}"
        if dedup_key in seen_docs:
            continue
        seen_docs.add(dedup_key)

        citations.append(
            Citation(
                document_name=doc_name,
                clause=meta.get("clause"),
                url=meta.get("url"),
                relevance_score=chunk.get("score"),
            )
        )

    return citations


def parse_inline_citations(llm_text: str) -> list[Citation]:
    """
    Parse inline [Source: ... | Clause: ...] references from LLM-generated text.

    The LLM is instructed to cite sources in this format. This function
    extracts them as structured Citation objects.

    Args:
        llm_text: The raw text output from the LLM.

    Returns:
        List of unique Citation objects found in the text.
    """
    citations: list[Citation] = []
    seen: set[str] = set()

    for match in _INLINE_CITATION_PATTERN.finditer(llm_text):
        doc = match.group("document").strip()
        clause = match.group("clause")
        if clause:
            clause = clause.strip()

        dedup_key = f"{doc}|{clause or ''}"
        if dedup_key in seen:
            continue
        seen.add(dedup_key)

        citations.append(
            Citation(
                document_name=doc,
                clause=clause if clause else None,
                url=None,
                relevance_score=None,
            )
        )

    return citations


def merge_citations(
    chunk_citations: list[Citation],
    inline_citations: list[Citation],
) -> list[Citation]:
    """
    Merge citations from chunks and inline LLM references, deduplicating
    by document name. Chunk citations take priority (they have scores + URLs).

    Args:
        chunk_citations: Citations extracted from retrieved chunks.
        inline_citations: Citations parsed from LLM output.

    Returns:
        Merged, deduplicated list of Citation objects.
    """
    merged: list[Citation] = list(chunk_citations)
    seen = {f"{c.document_name}|{c.clause or ''}" for c in merged}

    for ic in inline_citations:
        key = f"{ic.document_name}|{ic.clause or ''}"
        if key not in seen:
            seen.add(key)
            merged.append(ic)

    logger.debug(
        "Merged citations: %d from chunks + %d inline → %d total",
        len(chunk_citations),
        len(inline_citations),
        len(merged),
    )

    return merged
