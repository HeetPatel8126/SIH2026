"""
BIS AI Assistant — Prompt Builder Service

Assembles the final prompt from templates, retrieved context, and user query.
Thin wrapper around prompts.templates for use by routers.
"""

from __future__ import annotations

import logging

from backend.config import settings
from backend.models.schemas import QueryCategory
from backend.prompts.templates import build_full_prompt

logger = logging.getLogger("bis_assistant.prompt_builder")


def build_prompt(
    query: str,
    chunks: list[dict],
    category: QueryCategory,
    language: str = "en",
) -> str:
    """
    Build the complete LLM prompt for a given query.

    Args:
        query: User's question.
        chunks: Retrieved context chunks from the vector DB.
        category: Classified query category.
        language: ISO 639-1 language code.

    Returns:
        Fully assembled prompt string.
    """
    prompt = build_full_prompt(
        query=query,
        chunks=chunks,
        category=category.value,
        language=language,
        max_context_chars=settings.max_context_chars,
    )

    logger.debug(
        "Built prompt — category=%s, chunks=%d, language=%s, length=%d chars",
        category.value,
        len(chunks),
        language,
        len(prompt),
    )

    return prompt
