"""
test_queries.py — Evaluation query set for the BIS AI Assistant (Tech 5)

Each query maps to one of the 8 expected-solution capabilities from the
problem statement. Used to test retrieval accuracy + citation correctness
once the /chat endpoint (Tech 3) and retriever (Tech 1) are working.
"""

from __future__ import annotations
import pytest

TEST_QUERIES = [
    # --- Capability 1: Answer questions about Indian Standards (P0) ---
    {
        "id": "std_01",
        "capability": "standards_qa",
        "query": "What is the Indian Standard for packaged drinking water?",
        "expected_keywords": ["14543", "drinking water", "packaged"],
        "expected_source": "IS 14543",
    },
    {
        "id": "std_02",
        "capability": "standards_qa",
        "query": "What does IS 302 cover?",
        "expected_keywords": ["electrical", "appliances", "safety"],
        "expected_source": "IS 302",
    },
    {
        "id": "std_03",
        "capability": "standards_qa",
        "query": "Is there an Indian Standard for LED bulbs?",
        "expected_keywords": ["16102", "LED"],
        "expected_source": "IS 16102",
    },
    {
        "id": "std_04",
        "capability": "standards_qa",
        "query": "What is the Indian Standard for cement?",
        "expected_keywords": ["cement", "Portland", "OPC"],
        "expected_source": "IS 12269",
    },

    # --- Capability 2: Recommend standards from a product description (P0) ---
    {
        "id": "reco_01",
        "capability": "standard_recommendation",
        "query": "I manufacture pressure cookers, which standards apply to me?",
        "expected_keywords": ["2347", "pressure cooker"],
        "expected_source": "IS 2347",
    },
    {
        "id": "reco_02",
        "capability": "standard_recommendation",
        "query": "I make LED bulbs, what BIS certificate do I need?",
        "expected_keywords": ["16102", "CRS", "registration"],
        "expected_source": "IS 16102",
    },
    {
        "id": "reco_03",
        "capability": "standard_recommendation",
        "query": "I want to sell bottled mineral water, what do I need?",
        "expected_keywords": ["13428", "mineral water", "ISI"],
        "expected_source": "IS 13428",
    },
    {
        "id": "reco_04",
        "capability": "standard_recommendation",
        "query": "I manufacture electric kettles, which standard covers this?",
        "expected_keywords": ["302", "safety"],
        "expected_source": "IS 302",
    },

    # --- Capability 3: Explain certification schemes (P0) ---
    {
        "id": "scheme_01",
        "capability": "certification_schemes",
        "query": "What's the difference between ISI Mark and CRS?",
        "expected_keywords": ["ISI", "CRS", "electronics"],
        "expected_source": "Scheme I",
    },
    {
        "id": "scheme_02",
        "capability": "certification_schemes",
        "query": "What is FMCS and who needs it?",
        "expected_keywords": ["Foreign Manufacturers", "Authorized Indian Representative"],
        "expected_source": "FMCS",
    },
    {
        "id": "scheme_03",
        "capability": "certification_schemes",
        "query": "What is Scheme X under BIS certification?",
        "expected_keywords": ["Scheme X", "capital goods"],
        "expected_source": "Scheme X",
    },
    {
        "id": "scheme_04",
        "capability": "certification_schemes",
        "query": "What is ECO Mark and which products qualify?",
        "expected_keywords": ["ECO Mark", "environment"],
        "expected_source": "ECO Mark",
    },

    # --- Capability 4: Explain certification processes step-by-step (P0) ---
    {
        "id": "process_01",
        "capability": "process_explainer",
        "query": "How do I apply for a BIS license?",
        "expected_keywords": ["application", "manakonline", "inspection", "license"],
        "expected_source": "Product Certification",
    },
    {
        "id": "process_02",
        "capability": "process_explainer",
        "query": "What documents are needed to apply for ISI certification?",
        "expected_keywords": ["documents", "machinery", "testing", "factory"],
        "expected_source": "Product Certification",
    },
    {
        "id": "process_03",
        "capability": "process_explainer",
        "query": "How long does BIS certification usually take?",
        "expected_keywords": ["days", "months", "time"],
        "expected_source": "Product Certification",
    },
    {
        "id": "process_04",
        "capability": "process_explainer",
        "query": "What happens during a BIS factory inspection?",
        "expected_keywords": ["inspection", "officer", "sample", "verification"],
        "expected_source": "Product Certification",
    },

    # --- Capability 5: Consumer queries (P1) ---
    {
        "id": "consumer_01",
        "capability": "consumer_queries",
        "query": "How do I check if my gold jewellery is genuinely hallmarked?",
        "expected_keywords": ["HUID", "BIS Care"],
        "expected_source": "Hallmarking",
    },
    {
        "id": "consumer_02",
        "capability": "consumer_queries",
        "query": "How do I file a complaint against a fake ISI mark product?",
        "expected_keywords": ["BIS Care", "complaint", "portal"],
        "expected_source": "Consumer",
    },
    {
        "id": "consumer_03",
        "capability": "consumer_queries",
        "query": "How can I verify a BIS certificate number?",
        "expected_keywords": ["verify", "BIS Care", "portal"],
        "expected_source": "Consumer",
    },
    {
        "id": "consumer_04",
        "capability": "consumer_queries",
        "query": "What should I do if a product doesn't meet its claimed standard?",
        "expected_keywords": ["complaint", "BIS Care", "officer"],
        "expected_source": "Consumer",
    },

    # --- Capability 6: Hallmarking guidance (P1) ---
    {
        "id": "hallmark_01",
        "capability": "hallmarking",
        "query": "Is hallmarking mandatory for silver jewellery?",
        "expected_keywords": ["silver", "voluntary", "mandatory"],
        "expected_source": "Hallmarking",
    },
    {
        "id": "hallmark_02",
        "capability": "hallmarking",
        "query": "What is HUID and why does it matter?",
        "expected_keywords": ["Hallmark Unique", "6-digit"],
        "expected_source": "Hallmarking",
    },
    {
        "id": "hallmark_03",
        "capability": "hallmarking",
        "query": "Which gold purities are covered under mandatory hallmarking?",
        "expected_keywords": ["22K", "18K", "14K"],
        "expected_source": "Hallmarking",
    },
    {
        "id": "hallmark_04",
        "capability": "hallmarking",
        "query": "How do I become a BIS-recognized Assaying and Hallmarking Centre?",
        "expected_keywords": ["AHC", "Assaying", "recognition"],
        "expected_source": "Hallmarking",
    },

    # --- Capability 7: Suggest testing laboratories (P1) ---
    {
        "id": "lab_01",
        "capability": "lab_suggestion",
        "query": "Where can I get my product tested near Ahmedabad?",
        "expected_keywords": ["Ahmedabad", "Gujarat"],
        "expected_source": "Lab Directory",
    },
    {
        "id": "lab_02",
        "capability": "lab_suggestion",
        "query": "Which labs are recognized for testing electronics products?",
        "expected_keywords": ["lab", "electronics", "testing"],
        "expected_source": "Lab Directory",
    },
    {
        "id": "lab_03",
        "capability": "lab_suggestion",
        "query": "How do I find a BIS-recognized lab in my state?",
        "expected_keywords": ["LIMS", "portal", "laboratory"],
        "expected_source": "Lab Directory",
    },

    # --- Capability 8: Multilingual interaction (P1 — Day 2+) ---
    {
        "id": "multi_01",
        "capability": "multilingual",
        "query": "मैं प्रेशर कुकर बनाता हूँ, मुझे कौन सा मानक लागू होता है?",
        "expected_keywords": ["2347", "कुकर"],
        "expected_source": "IS 2347",
        "note": "Same question as reco_01, in Hindi.",
    },
    {
        "id": "multi_02",
        "capability": "multilingual",
        "query": "सोने के आभूषणों पर हॉलमार्किंग अनिवार्य है क्या?",
        "expected_keywords": ["हॉलमार्किंग", "अनिवार्य"],
        "expected_source": "Hallmarking",
        "note": "Same question as hallmark_01, in Hindi.",
    },

    # --- Edge cases: things the assistant should NOT confidently answer ---
    {
        "id": "edge_01",
        "capability": "hallucination_guard",
        "query": "What is the Indian Standard for flying cars?",
        "expected_keywords": ["not found", "no relevant", "unable to find", "does not exist"],
        "expected_source": None,
        "note": "No real standard exists — checks the assistant says 'not found' instead of inventing an IS code.",
    },
    {
        "id": "edge_02",
        "capability": "hallucination_guard",
        "query": "What is the exact fee for ISI certification in 2026?",
        "expected_keywords": ["portal", "manakonline", "fee"],
        "expected_source": None,
        "note": "Fees change and may not be in the corpus — checks it points to portal rather than inventing fees.",
    },
]


# ==========================================================================
# Automated Evaluation Tests (Pytest)
# ==========================================================================

def test_eval_suite_coverage():
    """Verify test query suite covers all 8 problem statement capabilities."""
    capabilities = {q["capability"] for q in TEST_QUERIES}
    expected_caps = {
        "standards_qa",
        "standard_recommendation",
        "certification_schemes",
        "process_explainer",
        "consumer_queries",
        "hallmarking",
        "lab_suggestion",
        "multilingual",
        "hallucination_guard",
    }
    assert expected_caps.issubset(capabilities), f"Missing capabilities: {expected_caps - capabilities}"
    assert len(TEST_QUERIES) >= 30


def test_retrieval_across_eval_suite():
    """Test that retriever returns non-empty grounded chunks for core evaluation queries."""
    import asyncio
    from backend.services.retriever import retrieve
    from backend.services.query_router import classify_query

    async def _test():
        sample_queries = [q for q in TEST_QUERIES if q["capability"] != "hallucination_guard"][:5]
        for item in sample_queries:
            cat = classify_query(item["query"])
            chunks = await retrieve(query=item["query"], category=cat, top_k=3)
            assert len(chunks) > 0, f"Retriever returned no chunks for query: {item['query']}"
            assert all("text" in c and "metadata" in c for c in chunks)

    asyncio.run(_test())


if __name__ == "__main__":
    print(f"Total queries: {len(TEST_QUERIES)}")
    from collections import Counter
    counts = Counter(q["capability"] for q in TEST_QUERIES)
    for cap, count in counts.items():
        print(f"  {cap}: {count}")
