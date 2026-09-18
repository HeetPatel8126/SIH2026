"""
BIS AI Assistant — Language Detection

Unicode script-based language detection for common Indian languages,
with secondary Hinglish (Romanized Hindi) detection for mixed-script queries.
No external dependency required — uses Python's built-in unicodedata.

Falls back to 'en' if no strong signal is detected.
"""

from __future__ import annotations

import logging
import re
import unicodedata

logger = logging.getLogger("bis_assistant.language_detect")

# ---------------------------------------------------------------------------
# Unicode script → ISO 639-1 mapping for Indian languages
# ---------------------------------------------------------------------------

_SCRIPT_TO_LANG: dict[str, str] = {
    "DEVANAGARI": "hi",     # Hindi, Marathi, Sanskrit, Nepali
    "BENGALI": "bn",        # Bengali, Assamese
    "GURMUKHI": "pa",       # Punjabi
    "GUJARATI": "gu",       # Gujarati
    "ORIYA": "or",          # Odia
    "TAMIL": "ta",          # Tamil
    "TELUGU": "te",         # Telugu
    "KANNADA": "kn",        # Kannada
    "MALAYALAM": "ml",      # Malayalam
    "ARABIC": "ur",         # Urdu (Nastaliq script variant of Arabic)
}

# ---------------------------------------------------------------------------
# Hinglish (Romanized Hindi) detection
# ---------------------------------------------------------------------------
# Common Hindi function words / particles written in Roman script.
# If ≥2 of these appear in a query that has no Devanagari, it's likely Hinglish.

_HINGLISH_MARKERS: set[str] = {
    # Question words
    "kya", "kaise", "kahan", "kahaan", "kaun", "kitna", "kitne", "kitni", "kyun", "kyu",
    # Verbs / auxiliaries
    "hai", "hain", "tha", "thi", "the", "hota", "hoti", "hote", "karna", "karo",
    "kare", "karein", "karenge", "karega", "karegi", "chahiye", "chahte", "milega",
    "milta", "milti", "dena", "dedo", "dijiye", "batao", "bataye", "bataiye",
    # Postpositions / particles
    "ka", "ke", "ki", "ko", "mein", "me", "se", "par", "pe", "tak",
    "wala", "wali", "wale", "aur", "ya", "bhi",
    # Negation
    "nahi", "nahin", "nah", "mat",
    # Common nouns (BIS-relevant)
    "paani", "pani", "sona", "chandi", "doodh", "cement", "steel",
    "bijli", "bulb", "ghar", "product", "company",
    # Common BIS terms in Hinglish
    "manak", "praman", "patra", "pramanikaran", "hallmark",
    "license", "testing", "lab", "complaint", "shikayat",
    "nakli", "asli", "sahi", "galat",
    # Verbs related to BIS queries
    "liye", "lena", "leni", "milna", "apply",
    "registration", "certificate", "renewal",
}

# Compile a pattern that matches whole words from the marker set
_HINGLISH_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in sorted(_HINGLISH_MARKERS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)

# Minimum number of Hinglish marker matches to classify as Hinglish
_HINGLISH_MIN_MATCHES = 2


def detect_language(text: str) -> str:
    """
    Detect the language of input text based on Unicode script analysis,
    with secondary Hinglish detection for Romanized Hindi queries.

    Args:
        text: User input text.

    Returns:
        ISO 639-1 language code (e.g. 'hi', 'bn', 'en') or 'hi-Latn'
        for Romanized Hindi (Hinglish).
    """
    if not text or not text.strip():
        return "en"

    # --- Phase 1: Unicode script-based detection ---
    script_counts: dict[str, int] = {}

    for char in text:
        if char.isspace() or char.isdigit():
            continue

        try:
            name = unicodedata.name(char, "")
        except ValueError:
            continue

        # Extract script name from Unicode character name
        # e.g., "DEVANAGARI LETTER KA" → "DEVANAGARI"
        for script in _SCRIPT_TO_LANG:
            if name.startswith(script):
                script_counts[script] = script_counts.get(script, 0) + 1
                break

    if script_counts:
        # Find the dominant script
        dominant_script = max(script_counts, key=script_counts.get)  # type: ignore[arg-type]
        dominant_count = script_counts[dominant_script]
        total_alpha = sum(1 for c in text if c.isalpha())

        # Require at least 20% of alphabetic characters to be in the detected script
        if total_alpha > 0 and (dominant_count / total_alpha) >= 0.2:
            detected = _SCRIPT_TO_LANG.get(dominant_script, "en")
            logger.debug(
                "Language detected (script): %s (script=%s, count=%d/%d)",
                detected, dominant_script, dominant_count, total_alpha,
            )
            return detected

    # --- Phase 2: Hinglish (Romanized Hindi) detection ---
    # Only triggered when no non-Latin script is dominant (would be 'en' otherwise)
    matches = _HINGLISH_PATTERN.findall(text)
    if len(matches) >= _HINGLISH_MIN_MATCHES:
        logger.debug(
            "Language detected (Hinglish): hi-Latn (markers found: %s)",
            matches[:5],
        )
        return "hi-Latn"

    return "en"
