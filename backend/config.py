"""
BIS AI Assistant — Centralized Configuration

All environment-based settings loaded via pydantic-settings.
Import `settings` from this module anywhere in the backend.
"""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # --- LLM ---
    llm_provider: str = os.getenv("LLM_PROVIDER", "ollama")
    llm_model: str = os.getenv("LLM_MODEL", "llama3.1:8b")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "http://localhost:11434")
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    llm_max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "1024"))

    # --- Embedding ---
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # --- Vector DB ---
    chroma_persist_dir: str = os.getenv("CHROMA_PERSIST_DIR", "./data/vectordb")
    chroma_collection: str = os.getenv("CHROMA_COLLECTION", "bis_documents")

    # --- Retriever ---
    retriever_top_k: int = int(os.getenv("RETRIEVER_TOP_K", "5"))
    use_mock_retriever: bool = os.getenv("USE_MOCK_RETRIEVER", "true").lower() == "true"

    # --- Server ---
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"

    # --- Prompt ---
    max_context_chars: int = int(os.getenv("MAX_CONTEXT_CHARS", "12000"))


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()


settings = get_settings()
