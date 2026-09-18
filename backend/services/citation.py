"""
BIS AI Assistant — Citation Extraction & Faithfulness Verification

Builds citation objects from retrieved chunks, parses inline references
from LLM output text, and verifies that inline citations actually match
retrieved context (prevents hallucinated citations from being displayed).
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


# ---------------------------------------------------------------------------
# Citation Faithfulness Verification (Audit #2)
# ---------------------------------------------------------------------------

def _normalize_doc_name(name: str) -> str:
    """Normalize a document name for fuzzy matching.

    Strips whitespace, lowercases, and removes common noise like year
    suffixes and punctuation so 'IS 10500:2012' matches 'IS 10500'.
    """
    name = name.lower().strip()
    # Remove trailing year like ':2012' or '(2024)'
    name = re.sub(r"[:\s]*\d{4}\)?$", "", name)
    # Collapse whitespace
    name = re.sub(r"\s+", " ", name)
    # Remove trailing/leading punctuation
    name = name.strip(" -—–")
    return name


def verify_inline_citations(
    inline_citations: list[Citation],
    retrieved_chunks: list[dict],
) -> list[Citation]:
    """
    Cross-check inline LLM citations against actually-retrieved chunks.

    For each inline citation, checks if the document name fuzzy-matches
    any retrieved chunk's metadata. Citations that don't match any retrieved
    source are flagged with '⚠ unverified' in their clause field.

    Args:
        inline_citations: Citations parsed from LLM output text.
        retrieved_chunks: The chunks that were actually retrieved from the
                          vector DB and fed to the LLM as context.

    Returns:
        The same citations list, with unverified ones flagged.
    """
    if not inline_citations or not retrieved_chunks:
        return inline_citations

    # Build a set of normalized document names from retrieved chunks
    retrieved_doc_names: set[str] = set()
    for chunk in retrieved_chunks:
        meta = chunk.get("metadata", {})
        doc = meta.get("document", "")
        if doc:
            retrieved_doc_names.add(_normalize_doc_name(doc))
            # Also add partial matches — just the IS code part
            # e.g., from "IS 10500:2012 — Drinking Water" extract "is 10500"
            is_match = re.search(r"(is\s+\d+)", doc.lower())
            if is_match:
                retrieved_doc_names.add(is_match.group(1).strip())

    verified: list[Citation] = []
    for citation in inline_citations:
        norm_name = _normalize_doc_name(citation.document_name)

        # Check exact normalized match
        is_verified = norm_name in retrieved_doc_names

        # Check if the IS code portion matches any retrieved doc
        if not is_verified:
            is_match = re.search(r"(is\s+\d+)", norm_name)
            if is_match:
                is_verified = is_match.group(1).strip() in retrieved_doc_names

        # Check substring containment (e.g., "BIS Hallmarking Order" in retrieved docs)
        if not is_verified:
            for retrieved_name in retrieved_doc_names:
                if norm_name in retrieved_name or retrieved_name in norm_name:
                    is_verified = True
                    break

        if is_verified:
            verified.append(citation)
        else:
            # Flag the citation as unverified rather than silently dropping it
            logger.warning(
                "Citation faithfulness check: '%s' not found in retrieved chunks — flagging as unverified",
                citation.document_name,
            )
            flagged = Citation(
                document_name=citation.document_name,
                clause=f"{citation.clause} ⚠ unverified" if citation.clause else "⚠ unverified",
                url=citation.url,
                relevance_score=None,
            )
            verified.append(flagged)

    return verified


def merge_citations(
    chunk_citations: list[Citation],
    inline_citations: list[Citation],
    retrieved_chunks: list[dict] | None = None,
) -> list[Citation]:
    """
    Merge citations from chunks and inline LLM references, deduplicating
    by document name. Chunk citations take priority (they have scores + URLs).

    If retrieved_chunks is provided, inline citations are verified for
    faithfulness before merging.

    Args:
        chunk_citations: Citations extracted from retrieved chunks.
        inline_citations: Citations parsed from LLM output.
        retrieved_chunks: Optional — the raw retrieved chunks for
                          faithfulness verification.

    Returns:
        Merged, deduplicated list of Citation objects.
    """
    # Verify inline citations if we have the retrieved chunks
    if retrieved_chunks is not None:
        inline_citations = verify_inline_citations(inline_citations, retrieved_chunks)

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
