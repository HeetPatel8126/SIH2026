"""
BIS AI Assistant — Services Package

Business logic services for the RAG pipeline.
"""

from backend.services.query_router import classify_query
from backend.services.prompt_builder import build_prompt
from backend.services.llm_wrapper import call_llm
from backend.services.retriever import retrieve
from backend.services.citation import extract_from_chunks, parse_inline_citations, merge_citations
from backend.services.language_detect import detect_language

__all__ = [
    "classify_query",
    "build_prompt",
    "call_llm",
    "retrieve",
    "extract_from_chunks",
    "parse_inline_citations",
    "merge_citations",
    "detect_language",
]
