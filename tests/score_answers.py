"""
score_answers.py — Tech 5 evaluation harness for the BIS AI Assistant.

Runs the full 30-query test set against the live /chat endpoint,
checks each answer, and prints + saves a pass/fail report.

USAGE:
    1. Make sure the backend is running: uvicorn backend.api:app --reload --port 8000
    2. Run this file: python tests/score_answers.py
    3. Check the printed summary + tests/evaluation_results.csv
"""

import csv
import requests
from test_queries import TEST_QUERIES

API_URL = "http://localhost:8000/chat"


def ask_bot(question: str, language: str = "en") -> dict:
    response = requests.post(API_URL, json={"query": question, "language": language})
    response.raise_for_status()
    return response.json()


def check_answer(query_info: dict, bot_response: dict) -> dict:
    answer_text = bot_response.get("answer", "")
    citations = bot_response.get("citations", [])
    processing_time_ms = bot_response.get("processing_time_ms", None)

    has_answer = len(answer_text.strip()) > 0
    citation_names = [c.get("document_name", "") for c in citations if c.get("document_name")]
    has_real_citation = len(citation_names) > 0

    expected = query_info.get("expected_keywords", [])
    if expected:
        answer_lower = answer_text.lower()
        found_keywords = [kw for kw in expected if kw.lower() in answer_lower]
        keyword_hit_rate = len(found_keywords) / len(expected)
    else:
        found_keywords = []
        keyword_hit_rate = None

    is_guard_query = query_info["capability"] == "hallucination_guard"
    if is_guard_query:
        passed = any(kw.lower() in answer_text.lower() for kw in expected) if expected else has_answer
    else:
        passed = has_answer and has_real_citation

    return {
        "id": query_info["id"],
        "capability": query_info["capability"],
        "query": query_info["query"],
        "has_answer": has_answer,
        "has_citation": has_real_citation,
        "citation_names": "; ".join(citation_names),
        "keyword_hit_rate": keyword_hit_rate,
        "processing_time_ms": processing_time_ms,
        "passed": passed,
    }


def run_all():
    results = []
    for i, query_info in enumerate(TEST_QUERIES, 1):
        print(f"[{i}/{len(TEST_QUERIES)}] Testing: {query_info['id']} — {query_info['query'][:60]}")
        try:
            bot_response = ask_bot(query_info["query"])
            result = check_answer(query_info, bot_response)
        except Exception as e:
            result = {
                "id": query_info["id"],
                "capability": query_info["capability"],
                "query": query_info["query"],
                "has_answer": False,
                "has_citation": False,
                "citation_names": "",
                "keyword_hit_rate": None,
                "processing_time_ms": None,
                "passed": False,
                "error": str(e),
            }
            print(f"    FAILED with error: {e}")
        results.append(result)
        status = "PASS" if result["passed"] else "FAIL"
        print(f"    -> {status}")

    # --- Summary ---
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    print(f"\n{'='*50}")
    print(f"TOTAL: {passed}/{total} passed ({passed/total*100:.1f}%)")
    print(f"{'='*50}")

    # Per-capability breakdown
    from collections import defaultdict
    by_cap = defaultdict(lambda: [0, 0])  # [passed, total]
    for r in results:
        by_cap[r["capability"]][1] += 1
        if r["passed"]:
            by_cap[r["capability"]][0] += 1

    print("\nBy capability:")
    for cap, (p, t) in by_cap.items():
        print(f"  {cap}: {p}/{t}")

    # --- Save CSV ---
    fieldnames = ["id", "capability", "query", "has_answer", "has_citation",
                  "citation_names", "keyword_hit_rate", "processing_time_ms", "passed"]
    with open("evaluation_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)
    print("\nSaved: evaluation_results.csv")

    return results


if __name__ == "__main__":
    run_all()
