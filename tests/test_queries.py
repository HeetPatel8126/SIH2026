"""
test_queries.py — Evaluation query set for the BIS AI Assistant (Tech 5)

Each query maps to one of the 8 expected-solution capabilities from the
problem statement. Used to test retrieval accuracy + citation correctness
once the /chat endpoint (Tech 3) and retriever (Tech 1) are working.

Fill in `expected_keywords` and `expected_source` once real BIS documents
are ingested — for now these are placeholders to be confirmed against
whatever Tech 2 actually loads into the corpus.
"""

TEST_QUERIES = [
    # --- Capability 1: Answer questions about Indian Standards (P0) ---
    {
        "id": "std_01",
        "capability": "standards_qa",
        "query": "What is the Indian Standard for packaged drinking water?",
        "expected_keywords": [],   # e.g. IS code number, once known
        "expected_source": None,  # e.g. document name/clause, once known
    },
    {
        "id": "std_02",
        "capability": "standards_qa",
        "query": "What does IS 302 cover?",
        "expected_keywords": [],
        "expected_source": None,
    },
    {
        "id": "std_03",
        "capability": "standards_qa",
        "query": "Is there an Indian Standard for LED bulbs?",
        "expected_keywords": [],
        "expected_source": None,
    },
    {
        "id": "std_04",
        "capability": "standards_qa",
        "query": "What is the Indian Standard for cement?",
        "expected_keywords": [],
        "expected_source": None,
    },

    # --- Capability 2: Recommend standards from a product description (P0) ---
    {
        "id": "reco_01",
        "capability": "standard_recommendation",
        "query": "I manufacture pressure cookers, which standards apply to me?",
        "expected_keywords": [],
        "expected_source": None,
    },
    {
        "id": "reco_02",
        "capability": "standard_recommendation",
        "query": "I make LED bulbs, what BIS certificate do I need?",
        "expected_keywords": [],
        "expected_source": None,
    },
    {
        "id": "reco_03",
        "capability": "standard_recommendation",
        "query": "I want to sell bottled mineral water, what do I need?",
        "expected_keywords": [],
        "expected_source": None,
    },
    {
        "id": "reco_04",
        "capability": "standard_recommendation",
        "query": "I manufacture electric kettles, which standard covers this?",
        "expected_keywords": [],
        "expected_source": None,
    },

    # --- Capability 3: Explain certification schemes (P0) ---
    {
        "id": "scheme_01",
        "capability": "certification_schemes",
        "query": "What's the difference between ISI Mark and CRS?",
        "expected_keywords": ["ISI", "CRS", "electronics", "license"],
        "expected_source": None,
    },
    {
        "id": "scheme_02",
        "capability": "certification_schemes",
        "query": "What is FMCS and who needs it?",
        "expected_keywords": ["Foreign Manufacturers", "Authorized Indian Representative"],
        "expected_source": None,
    },
    {
        "id": "scheme_03",
        "capability": "certification_schemes",
        "query": "What is Scheme X under BIS certification?",
        "expected_keywords": [],
        "expected_source": None,
    },
    {
        "id": "scheme_04",
        "capability": "certification_schemes",
        "query": "What is ECO Mark and which products qualify?",
        "expected_keywords": [],
        "expected_source": None,
    },

    # --- Capability 4: Explain certification processes step-by-step (P0) ---
    {
        "id": "process_01",
        "capability": "process_explainer",
        "query": "How do I apply for a BIS license?",
        "expected_keywords": ["application", "factory inspection", "sample testing", "license"],
        "expected_source": None,
    },
    {
        "id": "process_02",
        "capability": "process_explainer",
        "query": "What documents are needed to apply for ISI certification?",
        "expected_keywords": [],
        "expected_source": None,
    },
    {
        "id": "process_03",
        "capability": "process_explainer",
        "query": "How long does BIS certification usually take?",
        "expected_keywords": [],
        "expected_source": None,
    },
    {
        "id": "process_04",
        "capability": "process_explainer",
        "query": "What happens during a BIS factory inspection?",
        "expected_keywords": [],
        "expected_source": None,
    },

    # --- Capability 5: Consumer queries (P1) ---
    {
        "id": "consumer_01",
        "capability": "consumer_queries",
        "query": "How do I check if my gold jewellery is genuinely hallmarked?",
        "expected_keywords": ["HUID", "BIS Care"],
        "expected_source": None,
    },
    {
        "id": "consumer_02",
        "capability": "consumer_queries",
        "query": "How do I file a complaint against a fake ISI mark product?",
        "expected_keywords": [],
        "expected_source": None,
    },
    {
        "id": "consumer_03",
        "capability": "consumer_queries",
        "query": "How can I verify a BIS certificate number?",
        "expected_keywords": [],
        "expected_source": None,
    },
    {
        "id": "consumer_04",
        "capability": "consumer_queries",
        "query": "What should I do if a product doesn't meet its claimed standard?",
        "expected_keywords": [],
        "expected_source": None,
    },

    # --- Capability 6: Hallmarking guidance (P1) ---
    {
        "id": "hallmark_01",
        "capability": "hallmarking",
        "query": "Is hallmarking mandatory for silver jewellery?",
        "expected_keywords": [],
        "expected_source": None,
    },
    {
        "id": "hallmark_02",
        "capability": "hallmarking",
        "query": "What is HUID and why does it matter?",
        "expected_keywords": ["Hallmark Unique ID"],
        "expected_source": None,
    },
    {
        "id": "hallmark_03",
        "capability": "hallmarking",
        "query": "Which gold purities are covered under mandatory hallmarking?",
        "expected_keywords": [],
        "expected_source": None,
    },
    {
        "id": "hallmark_04",
        "capability": "hallmarking",
        "query": "How do I become a BIS-recognized Assaying and Hallmarking Centre?",
        "expected_keywords": [],
        "expected_source": None,
    },

    # --- Capability 7: Suggest testing laboratories (P1) ---
    {
        "id": "lab_01",
        "capability": "lab_suggestion",
        "query": "Where can I get my product tested near Ahmedabad?",
        "expected_keywords": [],
        "expected_source": None,
    },
    {
        "id": "lab_02",
        "capability": "lab_suggestion",
        "query": "Which labs are recognized for testing electronics products?",
        "expected_keywords": [],
        "expected_source": None,
    },
    {
        "id": "lab_03",
        "capability": "lab_suggestion",
        "query": "How do I find a BIS-recognized lab in my state?",
        "expected_keywords": [],
        "expected_source": None,
    },

    # --- Capability 8: Multilingual interaction (P1 — Day 2+) ---
    {
        "id": "multi_01",
        "capability": "multilingual",
        "query": "मैं प्रेशर कुकर बनाता हूँ, मुझे कौन सा मानक लागू होता है?",  # Hindi version of reco_01
        "expected_keywords": [],
        "expected_source": None,
        "note": "Same question as reco_01, in Hindi — checks answer is equally accurate and returned in Hindi.",
    },
    {
        "id": "multi_02",
        "capability": "multilingual",
        "query": "सोने के आभूषणों पर हॉलमार्किंग अनिवार्य है क्या?",  # Hindi version of hallmark_01
        "expected_keywords": [],
        "expected_source": None,
        "note": "Same question as hallmark_01, in Hindi.",
    },

    # --- Edge cases: things the assistant should NOT confidently answer ---
    {
        "id": "edge_01",
        "capability": "hallucination_guard",
        "query": "What is the Indian Standard for flying cars?",
        "expected_keywords": ["not found", "no relevant", "unable to find"],
        "expected_source": None,
        "note": "No real standard exists — checks the assistant says 'not found' instead of inventing an IS code.",
    },
    {
        "id": "edge_02",
        "capability": "hallucination_guard",
        "query": "What is the exact fee for ISI certification in 2026?",
        "expected_keywords": [],
        "expected_source": None,
        "note": "Fees change and may not be in the corpus — checks it doesn't guess a specific number without a source.",
    },
]

if __name__ == "__main__":
    print(f"Total queries: {len(TEST_QUERIES)}")
    from collections import Counter
    counts = Counter(q["capability"] for q in TEST_QUERIES)
    for cap, count in counts.items():
        print(f"  {cap}: {count}")
