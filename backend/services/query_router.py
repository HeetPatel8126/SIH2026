"""
BIS AI Assistant — Query Router

Classifies user queries into intent categories using weighted keyword matching.
Supports multilingual queries (Hindi and other Indian languages) by normalizing
known terms to English before classification.

Supports both single-category (classify_query) and multi-category
(classify_query_multi) classification for cross-domain queries.

Designed to be swappable with an LLM-based classifier later.
"""

from __future__ import annotations

import logging
import re

from backend.models.schemas import QueryCategory

logger = logging.getLogger("bis_assistant.query_router")

# ---------------------------------------------------------------------------
# Multilingual → English normalization map
# ---------------------------------------------------------------------------
# Maps Hindi / transliterated terms to their English equivalents so the
# keyword classifier works on non-English queries too. Add more languages
# by extending this dict.

_MULTILINGUAL_TERMS: dict[str, str] = {
    # Hindi — Standards
    "भारतीय मानक": "indian standard",
    "मानक": "standard",
    "विनिर्देश": "specification",
    "आईएस कोड": "is code",
    "आचार संहिता": "code of practice",
    # Hindi — Certification
    "प्रमाणन": "certification",
    "प्रमाणित": "certified",
    "लाइसेंस": "license",
    "आईएसआई मार्क": "isi mark",
    "आईएसआई": "isi mark",
    "अनिवार्य पंजीकरण": "compulsory registration",
    "विदेशी निर्माता": "foreign manufacturer",
    "आवेदन": "apply",
    "आवेदन प्रक्रिया": "application process",
    "कारखाना निरीक्षण": "factory inspection",
    "नवीनीकरण": "renewal",
    "योजना": "scheme",
    # Hindi — Hallmarking
    "हॉलमार्क": "hallmark",
    "हॉलमार्किंग": "hallmarking",
    "सोना": "gold",
    "चांदी": "silver",
    "आभूषण": "jewellery",
    "गहना": "jewellery",
    "गहने": "jewellery",
    "शुद्धता": "purity of gold",
    "कैरेट": "caratage",
    # Hindi — Consumer
    "उपभोक्ता": "consumer",
    "शिकायत": "complaint",
    "उपभोक्ता शिकायत": "consumer complaint",
    "नकली": "fake",
    "नकली उत्पाद": "fake product",
    "असली": "genuine",
    "सत्यापन": "verify",
    "सत्यापित": "verify",
    # Hindi — Lab
    "प्रयोगशाला": "laboratory",
    "परीक्षण": "testing",
    "परीक्षण प्रयोगशाला": "testing laboratory",
    "कहाँ परीक्षण": "where to test",
    "लैब": "lab",
    # Hindi — General
    "बीआईएस": "bis",
    "क्या है": "what is",
    "कैसे": "how to",
    "कहाँ": "where",
    "कौन सा": "which",
    "लागू": "applicable",
    "अनिवार्य": "mandatory",
    # -----------------------------------------------------------------------
    # Hinglish (Romanized Hindi) — expanded coverage
    # -----------------------------------------------------------------------
    # Standards-related
    "manak": "standard",
    "manak kya hai": "what is standard",
    "standard kya hai": "what is standard",
    "bis standard": "bis standard",
    "is code kya hai": "is code what is",
    "paani ka manak": "standard for water",
    "pani ka standard": "standard for water",
    "cement ka manak": "standard for cement",
    "cement ka standard": "standard for cement",
    "steel ka standard": "standard for steel",
    "steel ka manak": "standard for steel",
    "bulb ka standard": "standard for led bulb",
    "led ka standard": "standard for led",
    "pressure cooker standard": "standard pressure cooker",
    "pressure cooker ka manak": "standard pressure cooker",
    "toy safety": "toy safety standard",
    "khilone ka manak": "toy safety standard",
    "kapde ka manak": "fabric standard",
    "organic food standard": "organic food standard",
    # Certification-related
    "praman patra": "certification",
    "pramanikaran": "certification",
    "isi mark kya hai": "what is isi mark",
    "isi mark kaise milega": "how to get isi mark",
    "isi mark kaise le": "how to get isi mark",
    "crs registration": "compulsory registration",
    "crs kya hai": "what is crs",
    "bis license kaise le": "how to get bis license",
    "license kaise milega": "how to get license",
    "license renewal kaise kare": "license renewal how to",
    "kaise apply kare": "how to apply",
    "apply kaise kare": "how to apply",
    "certificate kaise le": "how to get certificate",
    "certificate kaise milega": "how to get certificate",
    # Hallmarking-related
    "hallmark kya hai": "what is hallmark",
    "hallmark kaise check kare": "how to verify hallmark",
    "sone ka hallmark": "gold hallmark",
    "chandi ka hallmark": "silver hallmark",
    "huid kya hai": "what is huid",
    "huid kaise check kare": "how to verify huid",
    "jewellery ka hallmark": "jewellery hallmark",
    "sona asli hai ya nahi": "gold genuine verify",
    # Consumer-related
    "complaint kaise kare": "how to file complaint",
    "shikayat kaise kare": "how to file complaint",
    "nakli product": "fake product",
    "asli ya nakli": "genuine or fake",
    "consumer helpline": "consumer helpline",
    # Lab-related
    "lab kahan hai": "where is lab",
    "testing lab kahan hai": "where is testing lab",
    "product test karna hai": "product testing",
    "product kahan test karein": "where to test product",
    "test kaise karaye": "how to get tested",
    # General
    "bis kya hai": "what is bis",
    "bis ka full form": "full form of bis",
    "bureau of indian standards": "bis",
}

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
        ("how to get", 2.0),
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
        ("genuine or fake", 4.0),
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
        ("sample submission", 5.0),
        ("submit test samples", 5.0),
        ("submit samples", 5.0),
        ("test samples", 4.0),
        ("samples to", 3.5),
        ("cpri", 5.0),
        ("central power research institute", 5.0),
        ("nth", 4.0),
        ("national test house", 4.0),
        ("referral lab", 4.5),
        ("lrs", 4.0),
        ("where can i get tested", 4.0),
        ("where can i get my product tested", 5.0),
        ("where is lab", 4.0),
        ("where is testing lab", 5.0),
        ("product testing", 3.5),
        ("where to test", 3.0),
        ("how to get tested", 3.0),
        ("tested near", 4.0),
        ("get tested", 3.0),
        ("test facility", 3.5),
        ("test near", 4.0),
        ("lab", 2.0),
        ("laboratory", 2.5),
        ("testing", 1.5),
    ]),
    (QueryCategory.STANDARDS, [
        ("indian standard", 5.0),
        ("is code", 5.0),
        ("is number", 4.0),
        ("which standard", 4.0),
        ("what standard", 4.0),
        ("what is standard", 4.0),
        ("applicable standard", 4.0),
        ("bis standard", 4.0),
        ("standard for", 3.0),
        ("standards for", 3.0),
        ("standard for water", 5.0),
        ("standard for cement", 5.0),
        ("standard for steel", 5.0),
        ("standard for led", 5.0),
        ("standard pressure cooker", 5.0),
        ("toy safety standard", 5.0),
        ("fabric standard", 4.0),
        ("organic food standard", 4.0),
        ("specification", 2.0),
        ("code of practice", 3.0),
        ("is ", 1.0),  # loose — "IS 10500"
        ("standard", 2.0),
    ]),
]

# Pre-compile: "is " as a standalone IS code reference (e.g. "IS 10500")
_IS_CODE_PATTERN = re.compile(r"\bIS\s+\d+", re.IGNORECASE)

# ---------------------------------------------------------------------------
# Multi-category threshold
# ---------------------------------------------------------------------------
# If the second-best category score is within this ratio of the best score
# (and above the minimum threshold), both categories are returned.
_MULTI_CATEGORY_RATIO = 0.60
_MIN_SCORE_THRESHOLD = 2.0


def _normalize_multilingual(query: str) -> str:
    """
    Normalize a potentially non-English query by appending English equivalents
    of recognized Hindi/multilingual terms.

    This lets the keyword classifier work on Hindi, Hinglish, and other
    Indian-language queries without needing a full translation service.

    Args:
        query: Original user query (any language).

    Returns:
        The original query with English keyword equivalents appended.
    """
    q_lower = query.lower()
    english_terms: list[str] = []

    # Sort by length descending so longer (more specific) phrases match first
    for term, english in sorted(_MULTILINGUAL_TERMS.items(), key=lambda x: len(x[0]), reverse=True):
        if term in q_lower:
            english_terms.append(english)

    if english_terms:
        # Append English equivalents so the keyword classifier can score them
        normalized = query + " " + " ".join(english_terms)
        logger.debug(
            "Multilingual normalization — injected terms: %s",
            english_terms,
        )
        return normalized

    return query


def _score_categories(query: str) -> dict[QueryCategory, float]:
    """
    Score all categories for a query using weighted keyword matching.

    Args:
        query: The user's natural language question (already normalized).

    Returns:
        Dict mapping each QueryCategory to its score.
    """
    # Normalize multilingual queries to include English keyword equivalents
    normalized = _normalize_multilingual(query)
    q_lower = normalized.lower()

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

    return scores


def classify_query(query: str) -> QueryCategory:
    """
    Classify a user query into a single QueryCategory using weighted keyword matching.

    Supports multilingual queries by normalizing Hindi/Indian language terms
    to English before classification.

    Args:
        query: The user's natural language question.

    Returns:
        The best-matching QueryCategory, defaults to GENERAL.
    """
    categories = classify_query_multi(query)
    return categories[0]


def classify_query_multi(query: str) -> list[QueryCategory]:
    """
    Classify a user query into one or more QueryCategories.

    Returns the best-matching category, plus the second-best if its score
    is within 60% of the best score. This allows cross-domain questions
    (e.g. "certification AND hallmarking") to retrieve from both categories.

    Args:
        query: The user's natural language question.

    Returns:
        List of 1-2 QueryCategory values, best match first.
    """
    scores = _score_categories(query)

    # Sort categories by score descending
    sorted_cats = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    best_category, best_score = sorted_cats[0]

    # Require a minimum confidence to avoid false positives
    if best_score < _MIN_SCORE_THRESHOLD:
        logger.debug(
            "Query classification — all scores below threshold, defaulting to GENERAL. scores=%s",
            {k.value: round(v, 1) for k, v in scores.items() if v > 0},
        )
        return [QueryCategory.GENERAL]

    result = [best_category]

    # Check if second-best category qualifies for multi-category retrieval
    if len(sorted_cats) > 1:
        second_category, second_score = sorted_cats[1]
        if (
            second_score >= _MIN_SCORE_THRESHOLD
            and second_score >= best_score * _MULTI_CATEGORY_RATIO
        ):
            result.append(second_category)
            logger.debug(
                "Multi-category classification — primary=%s (%.1f), secondary=%s (%.1f)",
                best_category.value, best_score,
                second_category.value, second_score,
            )

    logger.debug(
        "Query classification — scores=%s -> %s",
        {k.value: round(v, 1) for k, v in scores.items() if v > 0},
        [c.value for c in result],
    )

    return result
