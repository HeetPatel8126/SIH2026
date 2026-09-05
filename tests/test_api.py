"""
BIS AI Assistant — API Endpoint Tests (Tech 3)

Comprehensive pytest test suite for all Tech 3 components:
    - Query router (with multilingual support)
    - Language detection
    - Citation extraction & parsing
    - Prompt template assembly
    - API endpoints: /health, /chat, /search-standards, /certification-guide
"""

from __future__ import annotations

import os
import pytest
from unittest.mock import AsyncMock, patch

# Set mock retriever before any backend imports
os.environ["USE_MOCK_RETRIEVER"] = "true"
os.environ["LLM_PROVIDER"] = "ollama"
os.environ["DEBUG"] = "false"

from fastapi.testclient import TestClient

from backend.api import app
from backend.models.schemas import QueryCategory, Citation
from backend.services.query_router import classify_query
from backend.services.language_detect import detect_language
from backend.services.citation import (
    extract_from_chunks,
    parse_inline_citations,
    merge_citations,
)
from backend.prompts.templates import (
    build_full_prompt,
    format_context_block,
    BASE_SYSTEM_PROMPT,
    CATEGORY_INSTRUCTIONS,
)

client = TestClient(app)

# A mock LLM answer for tests
_MOCK_LLM_ANSWER = (
    "IS 10500:2012 specifies requirements for drinking water. "
    "The acceptable limit for TDS is 500 mg/l. "
    "[Source: IS 10500:2012 | Clause: Table 1]"
)


# ==========================================================================
# Query Router Tests
# ==========================================================================


class TestQueryRouter:
    """Tests for the weighted keyword query classifier."""

    def test_standards_lookup(self):
        result = classify_query("What is the Indian Standard for packaged drinking water?")
        assert result == QueryCategory.STANDARDS

    def test_standards_is_code(self):
        result = classify_query("What does IS 10500 cover?")
        assert result == QueryCategory.STANDARDS

    def test_certification_isi(self):
        result = classify_query("How do I apply for a BIS license?")
        assert result == QueryCategory.CERTIFICATION

    def test_certification_crs_vs_isi(self):
        result = classify_query("What's the difference between ISI Mark and CRS?")
        assert result == QueryCategory.CERTIFICATION

    def test_hallmarking_mandatory(self):
        result = classify_query("Is hallmarking mandatory for silver jewellery?")
        assert result == QueryCategory.HALLMARKING

    def test_hallmarking_huid(self):
        result = classify_query("How do I check if my gold jewellery is genuinely hallmarked?")
        assert result == QueryCategory.HALLMARKING

    def test_consumer_complaint(self):
        result = classify_query("How do I file a complaint about a fake ISI product?")
        assert result == QueryCategory.CONSUMER

    def test_lab_suggestion(self):
        result = classify_query("Where can I get my product tested near Ahmedabad?")
        assert result == QueryCategory.LAB_SUGGESTION

    def test_general_fallback(self):
        result = classify_query("What is BIS?")
        assert result == QueryCategory.GENERAL

    def test_product_recommendation(self):
        result = classify_query("I manufacture pressure cookers, which standards apply to me?")
        assert result == QueryCategory.STANDARDS

    # --- Multilingual (Hindi) routing ---

    def test_hindi_standards(self):
        """Hindi query about drinking water standard should route to STANDARDS."""
        result = classify_query("पीने के पानी के लिए भारतीय मानक क्या है?")
        assert result == QueryCategory.STANDARDS

    def test_hindi_hallmarking(self):
        """Hindi query about gold hallmarking should route to HALLMARKING."""
        result = classify_query("सोने के आभूषणों पर हॉलमार्किंग अनिवार्य है क्या?")
        assert result == QueryCategory.HALLMARKING

    def test_hindi_certification(self):
        """Hindi query about ISI mark should route to CERTIFICATION."""
        result = classify_query("आईएसआई मार्क के लिए आवेदन कैसे करें?")
        assert result == QueryCategory.CERTIFICATION

    def test_hindi_consumer(self):
        """Hindi query about consumer complaint should route to CONSUMER."""
        result = classify_query("नकली उत्पाद के बारे में उपभोक्ता शिकायत कैसे दर्ज करें?")
        assert result == QueryCategory.CONSUMER

    def test_hindi_lab(self):
        """Hindi query about testing lab should route to LAB_SUGGESTION."""
        result = classify_query("मेरे उत्पाद की परीक्षण प्रयोगशाला कहाँ है?")
        assert result == QueryCategory.LAB_SUGGESTION


# ==========================================================================
# Language Detection Tests
# ==========================================================================


class TestLanguageDetection:
    """Tests for Unicode script-based language detection."""

    def test_english(self):
        assert detect_language("What is the Indian Standard for drinking water?") == "en"

    def test_hindi(self):
        assert detect_language("पीने के पानी के लिए भारतीय मानक क्या है?") == "hi"

    def test_bengali(self):
        assert detect_language("পানীয় জলের জন্য ভারতীয় মান কী?") == "bn"

    def test_tamil(self):
        assert detect_language("குடிநீருக்கான இந்திய தரநிலை என்ன?") == "ta"

    def test_gujarati(self):
        assert detect_language("પીવાના પાણી માટે ભારતીય ધોરણ શું છે?") == "gu"

    def test_empty_string(self):
        assert detect_language("") == "en"

    def test_mixed_script_mostly_english(self):
        assert detect_language("What is IS 10500 for water testing?") == "en"


# ==========================================================================
# Citation Tests
# ==========================================================================


class TestCitations:
    """Tests for citation extraction, parsing, and merging."""

    def test_extract_from_chunks(self):
        chunks = [
            {"text": "Sample", "metadata": {"document": "IS 10500:2012", "clause": "Table 1"}, "score": 0.92},
            {"text": "Sample2", "metadata": {"document": "BIS Overview", "clause": "1.1"}, "score": 0.85},
        ]
        citations = extract_from_chunks(chunks)
        assert len(citations) == 2
        assert citations[0].document_name == "IS 10500:2012"
        assert citations[0].clause == "Table 1"
        assert citations[0].relevance_score == 0.92

    def test_extract_deduplicates(self):
        chunks = [
            {"text": "A", "metadata": {"document": "IS 10500:2012", "clause": "Table 1"}, "score": 0.92},
            {"text": "B", "metadata": {"document": "IS 10500:2012", "clause": "Table 1"}, "score": 0.88},
        ]
        citations = extract_from_chunks(chunks)
        assert len(citations) == 1

    def test_parse_inline_citations(self):
        text = (
            "The limit is 500 mg/l. [Source: IS 10500:2012 | Clause: Table 1] "
            "Also see [Source: BIS Overview | Clause: 1.1]."
        )
        citations = parse_inline_citations(text)
        assert len(citations) == 2
        assert citations[0].document_name == "IS 10500:2012"
        assert citations[0].clause == "Table 1"

    def test_parse_inline_no_clause(self):
        text = "[Source: BIS Guidelines]"
        citations = parse_inline_citations(text)
        assert len(citations) == 1
        assert citations[0].clause is None

    def test_merge_deduplicates(self):
        chunk_cites = [Citation(document_name="IS 10500:2012", clause="Table 1", relevance_score=0.92)]
        inline_cites = [
            Citation(document_name="IS 10500:2012", clause="Table 1"),
            Citation(document_name="New Source", clause="2.0"),
        ]
        merged = merge_citations(chunk_cites, inline_cites)
        assert len(merged) == 2
        # Chunk citation (with score) takes priority
        assert merged[0].relevance_score == 0.92

    def test_empty_citations(self):
        assert extract_from_chunks([]) == []
        assert parse_inline_citations("No citations here.") == []


# ==========================================================================
# Prompt Template Tests
# ==========================================================================


class TestPromptTemplates:
    """Tests for prompt assembly and context formatting."""

    _sample_chunks = [
        {"text": "IS 10500 covers drinking water.", "metadata": {"document": "IS 10500:2012", "clause": "1"}, "score": 0.9},
    ]

    @pytest.mark.parametrize("category", ["standards", "certification", "hallmarking", "consumer", "lab_suggestion", "general"])
    def test_all_categories_produce_valid_prompts(self, category):
        prompt = build_full_prompt("Test query", self._sample_chunks, category)
        assert "BIS AI Assistant" in prompt
        assert "Retrieved Context" in prompt
        assert "User Question" in prompt
        assert "Test query" in prompt

    def test_category_instructions_injected(self):
        prompt = build_full_prompt("test", self._sample_chunks, "standards")
        assert "Indian Standards Lookup" in prompt

    def test_multilingual_instruction_injected(self):
        prompt = build_full_prompt("test", self._sample_chunks, "general", language="hi")
        assert "Language Requirement" in prompt
        assert "hi" in prompt

    def test_multilingual_instruction_not_injected_for_english(self):
        prompt = build_full_prompt("test", self._sample_chunks, "general", language="en")
        assert "Language Requirement" not in prompt

    def test_empty_context_message(self):
        result = format_context_block([])
        assert "No relevant context" in result

    def test_context_truncation(self):
        big_chunk = {"text": "x" * 15000, "metadata": {"document": "Big Doc"}, "score": 0.9}
        result = format_context_block([big_chunk], max_chars=100)
        assert len(result) <= 15100  # should truncate

    def test_chain_of_thought_instructions(self):
        prompt = build_full_prompt("test", self._sample_chunks, "general")
        assert "<think>" in prompt
        assert "</think>" in prompt


# ==========================================================================
# API Endpoint Tests
# ==========================================================================


class TestHealthEndpoint:
    """Tests for GET /health."""

    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_response_shape(self):
        data = client.get("/health").json()
        assert data["status"] == "ok"
        assert data["version"] == "0.1.0"
        assert "llm_provider" in data
        assert "llm_model" in data
        assert "uptime_seconds" in data


class TestSearchStandardsEndpoint:
    """Tests for POST /search-standards (uses mock retriever)."""

    def test_search_returns_200(self):
        response = client.post("/search-standards", json={"query": "LED bulbs", "top_k": 3})
        assert response.status_code == 200

    def test_search_returns_results(self):
        data = client.post("/search-standards", json={"query": "drinking water"}).json()
        assert data["total_found"] > 0
        assert len(data["results"]) > 0

    def test_search_result_shape(self):
        data = client.post("/search-standards", json={"query": "LED", "top_k": 1}).json()
        result = data["results"][0]
        assert "is_code" in result
        assert "title" in result
        assert "relevance_score" in result

    def test_search_validation_empty_query(self):
        response = client.post("/search-standards", json={"query": ""})
        assert response.status_code == 422  # validation error


class TestChatEndpoint:
    """Tests for POST /chat (mocks the LLM call)."""

    @patch("backend.routers.chat.call_llm", new_callable=AsyncMock, return_value=_MOCK_LLM_ANSWER)
    def test_chat_returns_200(self, mock_llm):
        response = client.post("/chat", json={"query": "What is IS 10500?"})
        assert response.status_code == 200

    @patch("backend.routers.chat.call_llm", new_callable=AsyncMock, return_value=_MOCK_LLM_ANSWER)
    def test_chat_response_shape(self, mock_llm):
        data = client.post("/chat", json={"query": "What is IS 10500?"}).json()
        assert "answer" in data
        assert "citations" in data
        assert "query_category" in data
        assert "session_id" in data
        assert "timestamp" in data
        assert "processing_time_ms" in data

    @patch("backend.routers.chat.call_llm", new_callable=AsyncMock, return_value=_MOCK_LLM_ANSWER)
    def test_chat_routes_to_standards(self, mock_llm):
        data = client.post("/chat", json={"query": "What is IS 10500?"}).json()
        assert data["query_category"] == "standards"

    @patch("backend.routers.chat.call_llm", new_callable=AsyncMock, return_value=_MOCK_LLM_ANSWER)
    def test_chat_extracts_citations(self, mock_llm):
        data = client.post("/chat", json={"query": "What is IS 10500?"}).json()
        assert len(data["citations"]) > 0

    @patch("backend.routers.chat.call_llm", new_callable=AsyncMock, return_value=_MOCK_LLM_ANSWER)
    def test_chat_hindi_query_routes_correctly(self, mock_llm):
        """Hindi drinking water query should route to standards, not general."""
        data = client.post("/chat", json={
            "query": "पीने के पानी के लिए भारतीय मानक क्या है?"
        }).json()
        assert data["query_category"] == "standards"

    def test_chat_validation_empty_query(self):
        response = client.post("/chat", json={"query": ""})
        assert response.status_code == 422


class TestCertificationGuideEndpoint:
    """Tests for POST /certification-guide (mocks the LLM call)."""

    _MOCK_CERT_ANSWER = (
        "To apply for ISI certification:\n"
        "1. Submit application on BIS portal\n"
        "2. Factory assessment\n"
        "3. Sample testing\n"
        "4. License grant\n"
        "[Source: BIS Scheme I Guidelines | Clause: 3.2]"
    )

    @patch("backend.routers.certification.call_llm", new_callable=AsyncMock, return_value=_MOCK_CERT_ANSWER)
    def test_certification_returns_200(self, mock_llm):
        response = client.post("/certification-guide", json={"query": "How to get ISI mark?"})
        assert response.status_code == 200

    @patch("backend.routers.certification.call_llm", new_callable=AsyncMock, return_value=_MOCK_CERT_ANSWER)
    def test_certification_identifies_scheme(self, mock_llm):
        data = client.post("/certification-guide", json={"query": "How to get ISI mark?"}).json()
        assert data["scheme_identified"] == "ISI"

    @patch("backend.routers.certification.call_llm", new_callable=AsyncMock, return_value=_MOCK_CERT_ANSWER)
    def test_certification_extracts_steps(self, mock_llm):
        data = client.post("/certification-guide", json={"query": "How to get ISI mark?"}).json()
        assert len(data["steps"]) >= 3

    @patch("backend.routers.certification.call_llm", new_callable=AsyncMock, return_value=_MOCK_CERT_ANSWER)
    def test_certification_explicit_scheme(self, mock_llm):
        data = client.post("/certification-guide", json={
            "query": "How to apply?",
            "scheme": "CRS"
        }).json()
        assert data["scheme_identified"] == "CRS"

    def test_certification_validation_empty_query(self):
        response = client.post("/certification-guide", json={"query": ""})
        assert response.status_code == 422
