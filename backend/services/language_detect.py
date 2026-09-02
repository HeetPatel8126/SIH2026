"""
BIS AI Assistant — Language Detection

Unicode script-based language detection for common Indian languages.
No external dependency required — uses Python's built-in unicodedata.

Falls back to 'en' if no strong signal is detected.
"""

from __future__ import annotations

import logging
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


def detect_language(text: str) -> str:
    """
    Detect the language of input text based on Unicode script analysis.

    Counts characters belonging to known scripts and returns the language
    with the most hits. If no non-Latin script is dominant, returns 'en'.

    Args:
        text: User input text.

    Returns:
        ISO 639-1 language code (e.g. 'hi', 'bn', 'en').
    """
    if not text or not text.strip():
        return "en"

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

    if not script_counts:
        return "en"

    # Find the dominant script
    dominant_script = max(script_counts, key=script_counts.get)  # type: ignore[arg-type]
    dominant_count = script_counts[dominant_script]
    total_alpha = sum(1 for c in text if c.isalpha())

    # Require at least 20% of alphabetic characters to be in the detected script
    if total_alpha > 0 and (dominant_count / total_alpha) < 0.2:
        return "en"

    detected = _SCRIPT_TO_LANG.get(dominant_script, "en")
    logger.debug(
        "Language detected: %s (script=%s, count=%d/%d)",
        detected, dominant_script, dominant_count, total_alpha,
    )

    return detected
