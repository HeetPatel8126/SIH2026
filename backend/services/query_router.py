"""
BIS AI Assistant — Query Router

Classifies user queries into intent categories using weighted keyword matching.
Designed to be swappable with an LLM-based classifier later.
"""

from __future__ import annotations

import logging
import re

from backend.models.schemas import QueryCategory

logger = logging.getLogger("bis_assistant.query_router")

# ---------------------------------------------------------------------------
# Keyword → Category mappings with weights
# ---------------------------------------------------------------------------
# Higher weight = stronger signal. Multi-word phrases score higher because
# they're more specific.

_KEYWORD_RULES: list[tuple[QueryCategory, list[tuple[str, float]]]] = [
    (QueryCategory.HALLMARKING, [
        ("hallmark", 3.0),
        ("hallmarking", 3.0),
        ("huid", 4.0),
        ("hallmark unique id", 5.0),
        ("gold jewellery", 3.0),
        ("gold jewelry", 3.0),
        ("silver jewellery", 3.0),
        ("silver jewelry", 3.0),
        ("assaying centre", 4.0),
        ("assaying center", 4.0),
        ("purity of gold", 3.0),
        ("purity of silver", 3.0),
        ("caratage", 3.0),
        ("bis care app", 4.0),
        ("gold", 1.0),
        ("silver", 1.0),
        ("jewellery", 2.0),
        ("jewelry", 2.0),
    ]),
    (QueryCategory.CERTIFICATION, [
        ("isi mark", 5.0),
        ("isi certification", 5.0),
        ("crs", 3.0),
        ("compulsory registration", 5.0),
        ("fmcs", 4.0),
        ("foreign manufacturer", 4.0),
        ("eco mark", 4.0),
        ("scheme x", 4.0),
        ("bis license", 4.0),
        ("bis licence", 4.0),
        ("certification scheme", 4.0),
        ("certification process", 4.0),
        ("how to get certified", 4.0),
        ("how to apply for", 3.0),
        ("license", 2.0),
        ("licence", 2.0),
        ("certification", 2.5),
        ("certified", 2.0),
        ("scheme", 1.5),
        ("apply", 1.0),
        ("application process", 3.0),
        ("factory inspection", 3.0),
        ("sample testing", 2.0),
        ("renewal", 2.0),
    ]),
    (QueryCategory.CONSUMER, [
        ("consumer complaint", 5.0),
        ("file a complaint", 5.0),
        ("grievance", 4.0),
        ("fake product", 4.0),
        ("counterfeit", 4.0),
        ("verify mark", 4.0),
        ("check if genuine", 4.0),
        ("consumer rights", 3.0),
        ("consumer helpline", 4.0),
        ("complaint", 3.0),
        ("consumer", 2.0),
        ("verify", 1.5),
        ("fake", 2.0),
        ("genuine", 1.5),
    ]),
    (QueryCategory.LAB_SUGGESTION, [
        ("testing laboratory", 5.0),
        ("testing lab", 5.0),
        ("lab near", 5.0),
        ("laboratory near", 5.0),
        ("bis recognized lab", 5.0),
        ("bis recognised lab", 5.0),
        ("where can i get tested", 4.0),
        ("where can i get my product tested", 5.0),
        ("tested near", 4.0),
        ("get tested", 3.0),
        ("where to test", 3.0),
        ("product testing", 3.0),
        ("test facility", 3.0),
        ("test near", 4.0),
        ("lab", 2.0),
        ("laboratory", 2.5),
        ("testing", 1.0),
    ]),
    (QueryCategory.STANDARDS, [
        ("indian standard", 5.0),
        ("is code", 5.0),
        ("is number", 4.0),
        ("which standard", 4.0),
        ("what standard", 4.0),
        ("applicable standard", 4.0),
        ("bis standard", 4.0),
        ("standard for", 3.0),
        ("standards for", 3.0),
        ("is ", 1.0),  # loose — "IS 10500"
        ("standard", 2.0),
        ("specification", 2.0),
        ("code of practice", 3.0),
    ]),
]

# Pre-compile: "is " as a standalone IS code reference (e.g. "IS 10500")
_IS_CODE_PATTERN = re.compile(r"\bIS\s+\d+", re.IGNORECASE)


def classify_query(query: str) -> QueryCategory:
    """
    Classify a user query into a QueryCategory using weighted keyword matching.

    Args:
        query: The user's natural language question.

    Returns:
        The best-matching QueryCategory, defaults to GENERAL.
    """
    q_lower = query.lower()

    # Bonus for explicit IS code references (e.g., "IS 10500")
    has_is_code = bool(_IS_CODE_PATTERN.search(query))

    scores: dict[QueryCategory, float] = {cat: 0.0 for cat in QueryCategory}

    for category, keywords in _KEYWORD_RULES:
        for keyword, weight in keywords:
            if keyword in q_lower:
                scores[category] += weight

    # Bonus for IS code reference
    if has_is_code:
        scores[QueryCategory.STANDARDS] += 5.0

    # Find the best match
    best_category = max(scores, key=scores.get)  # type: ignore[arg-type]
    best_score = scores[best_category]

    # Require a minimum confidence to avoid false positives
    if best_score < 2.0:
        best_category = QueryCategory.GENERAL

    logger.debug(
        "Query classification — scores=%s → %s (%.1f)",
        {k.value: round(v, 1) for k, v in scores.items() if v > 0},
        best_category.value,
        best_score,
    )

    return best_category
