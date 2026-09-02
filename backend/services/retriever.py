"""
BIS AI Assistant — Retriever Service

When USE_MOCK_RETRIEVER=true (default), returns realistic hardcoded BIS data
for all 8 expected-solution capabilities. This allows end-to-end testing
before Tech 1's vector DB is ready.

When USE_MOCK_RETRIEVER=false, queries ChromaDB for real embedded chunks.
"""

from __future__ import annotations

import logging
from typing import Optional

from backend.config import settings
from backend.models.schemas import QueryCategory

logger = logging.getLogger("bis_assistant.retriever")

# ---------------------------------------------------------------------------
# Mock data — realistic BIS content for each category
# ---------------------------------------------------------------------------

_MOCK_CHUNKS: dict[str, list[dict]] = {
    "standards": [
        {
            "text": (
                "IS 10500:2012 — Drinking Water — Specification (Second Revision). "
                "This standard prescribes the requirements for drinking water. It covers "
                "the acceptable limits for various substances including turbidity (1 NTU acceptable, "
                "5 NTU permissible), total dissolved solids (500 mg/l acceptable, 2000 mg/l permissible), "
                "pH (6.5 to 8.5), iron (0.3 mg/l), and microbiological requirements. "
                "This standard is applicable to packaged drinking water and all piped water supplies."
            ),
            "metadata": {"document": "IS 10500:2012", "clause": "Table 1 — Requirements", "page": "3", "url": "https://www.bis.gov.in"},
            "score": 0.92,
        },
        {
            "text": (
                "IS 2062:2011 — Hot Rolled Medium and High Tensile Structural Steel. "
                "Specifies requirements for hot rolled medium and high tensile structural "
                "steel plates, strips, shapes and sections (angles, tees, beams, channels, "
                "and bulb angles) for use in structural purposes. Grade E250 (Fe 410 W) A "
                "is the most commonly used grade for general structural applications."
            ),
            "metadata": {"document": "IS 2062:2011", "clause": "4.1", "page": "5"},
            "score": 0.85,
        },
        {
            "text": (
                "IS 1239 (Part 1):2004 — Mild Steel Tubes, Tubulars and Other Wrought Steel "
                "Fittings — Specification. Covers steel tubes suitable for screwing to "
                "IS 554 threads. Used extensively in water supply, gas supply, and "
                "structural applications."
            ),
            "metadata": {"document": "IS 1239 (Part 1):2004", "clause": "1 — Scope", "page": "1"},
            "score": 0.78,
        },
        {
            "text": (
                "IS 16046:2018 — LED Luminaires for General Lighting — Specification. "
                "This standard specifies the safety and performance requirements for LED "
                "luminaires intended for general lighting purposes. LED luminaires must comply "
                "with this standard for BIS certification. Covers operating voltage up to 250V "
                "and various wattage ranges."
            ),
            "metadata": {"document": "IS 16046:2018", "clause": "1 — Scope", "page": "1"},
            "score": 0.88,
        },
        {
            "text": (
                "IS 302-2-6:2009 / IEC 60335-2-6 — Safety of Household and Similar "
                "Electrical Appliances — Particular Requirements for Stationary Cooking "
                "Ranges, Hobs, Ovens and Similar Appliances. This standard is mandatory "
                "for ISI certification of cooking appliances sold in India."
            ),
            "metadata": {"document": "IS 302-2-6:2009", "clause": "1 — Scope", "page": "1"},
            "score": 0.75,
        },
    ],
    "certification": [
        {
            "text": (
                "BIS Product Certification Scheme I (ISI Mark): Domestic manufacturers "
                "apply for a license to use the ISI mark on their products. The process involves: "
                "(1) Application submission on the BIS portal (manakonline.bis.gov.in), "
                "(2) Factory assessment/inspection by BIS officers, "
                "(3) Sample testing in BIS-recognized labs, "
                "(4) Grant of licence upon compliance. "
                "The license is valid for 1 year initially and can be renewed annually. "
                "Application fees start at ₹1,000 and annual marking fees depend on production volume."
            ),
            "metadata": {"document": "BIS Product Certification Scheme I — Guidelines", "clause": "3.2 — Process", "page": "4"},
            "score": 0.95,
        },
        {
            "text": (
                "BIS CRS (Compulsory Registration Scheme / Scheme II): Applicable to "
                "electronics and IT goods notified under the Electronics and Information "
                "Technology Goods (Requirements for Compulsory Registration) Order. "
                "Manufacturers or importers must get products tested in a BIS-recognized lab "
                "and register on the BIS portal. Unlike Scheme I, no factory inspection is required — "
                "it's a self-declaration-based scheme. Registration is valid for 2 years."
            ),
            "metadata": {"document": "CRS Scheme Guidelines", "clause": "2.1 — Scope", "page": "2"},
            "score": 0.91,
        },
        {
            "text": (
                "FMCS (Foreign Manufacturers Certification Scheme): Enables overseas "
                "manufacturers to obtain ISI certification for products exported to India. "
                "Requires: (1) appointment of an Authorized Indian Representative (AIR), "
                "(2) application through the AIR, (3) factory inspection by BIS officers abroad, "
                "(4) product testing. The manufacturer bears the travel and inspection costs. "
                "License validity and marking fee structure is the same as Scheme I."
            ),
            "metadata": {"document": "FMCS Guidelines", "clause": "4.1 — Requirements", "page": "5"},
            "score": 0.87,
        },
    ],
    "hallmarking": [
        {
            "text": (
                "BIS Hallmarking — Mandatory hallmarking of gold jewellery has been "
                "enforced since June 16, 2021 under the Bureau of Indian Standards "
                "(Hallmarking of Gold Jewellery) Order 2020. As of Phase 3 (April 2023), "
                "it is applicable in all districts across India. Gold jewellery in 14, 18, 20, "
                "22, and 24 carat must be hallmarked. Export jewellery, watches, fountain pens, "
                "and special-order jewellery above 10 grams are exempt."
            ),
            "metadata": {"document": "BIS Hallmarking Order 2020 (Amendment 2023)", "clause": "3 — Applicability", "page": "2"},
            "score": 0.96,
        },
        {
            "text": (
                "HUID (Hallmark Unique ID): Every hallmarked article receives a unique "
                "6-character alphanumeric HUID. Consumers can verify the authenticity of "
                "hallmarked jewellery by entering the HUID on the BIS Care app (available "
                "on Android and iOS) or the BIS website (www.bis.gov.in). The HUID record "
                "shows the purity, jeweller's details, and assaying centre information. "
                "Silver hallmarking is currently under the voluntary phase."
            ),
            "metadata": {"document": "BIS HUID System — Consumer Guide", "clause": "5 — Verification", "page": "8"},
            "score": 0.94,
        },
    ],
    "consumer": [
        {
            "text": (
                "Consumer Complaints against BIS licensees: Consumers can lodge complaints "
                "about substandard or counterfeit ISI-marked products through: "
                "(1) BIS Care App — scan the ISI mark or enter the license number, "
                "(2) BIS website — Online complaint form at www.bis.gov.in, "
                "(3) Email — ccd@bis.gov.in, "
                "(4) Toll-free helpline — 1800-11-4100 (open Mon–Fri, 9:30 AM to 5:30 PM). "
                "BIS investigates complaints and can suspend or cancel licenses."
            ),
            "metadata": {"document": "BIS Consumer Complaint Guide", "clause": "2 — How to Complain", "page": "1"},
            "score": 0.93,
        },
        {
            "text": (
                "Verifying ISI Mark Authenticity: A genuine ISI mark consists of: "
                "(1) The ISI logo (a triangular figure), "
                "(2) The IS number of the standard, "
                "(3) A CM/L (certification marks/license) number unique to the manufacturer. "
                "Consumers can verify the CM/L number on the BIS website or BIS Care app "
                "to confirm the product is genuinely ISI-certified."
            ),
            "metadata": {"document": "BIS ISI Mark Verification Guide", "clause": "1 — Components of ISI Mark", "page": "1"},
            "score": 0.89,
        },
    ],
    "lab_suggestion": [
        {
            "text": (
                "BIS-Recognized Testing Laboratories: BIS maintains a directory of "
                "recognized laboratories across India. Key labs include:\n"
                "- Gujarat region: BIS Regional Office Lab, Ahmedabad; "
                "National Accreditation Board for Testing and Calibration Laboratories (NABL)-accredited labs\n"
                "- Maharashtra: BIS Western Regional Office Lab, Mumbai; "
                "SGS India Pvt. Ltd., Mumbai\n"
                "- Delhi NCR: BIS Central Lab, New Delhi; ERTL (East), Kolkata\n"
                "- South India: ETDC, Bengaluru; ERTL (South), Bengaluru; "
                "BIS Branch Office Lab, Chennai\n\n"
                "The full directory is available at www.bis.gov.in under 'Recognized Labs'. "
                "Labs are categorized by product type — electrical, food, construction, etc."
            ),
            "metadata": {"document": "BIS Recognized Laboratory Directory 2024", "clause": "Annex A — Lab Listing", "page": "12"},
            "score": 0.90,
        },
    ],
    "general": [
        {
            "text": (
                "Bureau of Indian Standards (BIS) is the national standards body of India "
                "established under the Bureau of Indian Standards Act, 2016. It functions "
                "under the Ministry of Consumer Affairs, Food & Public Distribution. "
                "BIS is responsible for: (1) Formulating Indian Standards (IS codes), "
                "(2) Product certification (ISI mark, CRS, FMCS), "
                "(3) Hallmarking of precious metals, "
                "(4) Laboratory recognition, "
                "(5) Consumer protection related to standardized products. "
                "BIS has published over 22,000 Indian Standards covering various sectors "
                "including food, electronics, construction, chemicals, and textiles."
            ),
            "metadata": {"document": "BIS Overview — About Us", "clause": "1 — Introduction", "page": "1"},
            "score": 0.88,
        },
        {
            "text": (
                "Standards Clubs: BIS runs a Standards Club Scheme to promote quality "
                "awareness among students. Standards Clubs can be established in schools, "
                "colleges, and polytechnics. The scheme aims to create awareness about "
                "standardization, quality, and conformity assessment among the youth."
            ),
            "metadata": {"document": "BIS Standards Club Scheme", "clause": "2 — Objectives", "page": "1"},
            "score": 0.72,
        },
    ],
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def retrieve(
    query: str,
    top_k: int | None = None,
    category: QueryCategory | None = None,
) -> list[dict]:
    """
    Retrieve relevant document chunks for a query.

    When USE_MOCK_RETRIEVER is True, returns hardcoded sample data.
    When False, queries ChromaDB (requires Tech 1's vector DB to be set up).

    Args:
        query: The user's question (will be embedded for real retrieval).
        top_k: Number of chunks to return.
        category: Optional category filter to scope retrieval.

    Returns:
        List of chunk dicts with 'text', 'metadata', and 'score' keys.
    """
    if top_k is None:
        top_k = settings.retriever_top_k

    if settings.use_mock_retriever:
        return _mock_retrieve(query, top_k, category)

    return await _real_retrieve(query, top_k, category)


def _mock_retrieve(
    query: str,
    top_k: int,
    category: QueryCategory | None,
) -> list[dict]:
    """Return mock chunks matching the category."""
    cat_key = category.value if category else "general"

    chunks = _MOCK_CHUNKS.get(cat_key, _MOCK_CHUNKS["general"])

    # Simple query-word overlap scoring to make mock results seem responsive
    query_words = set(query.lower().split())
    scored = []
    for chunk in chunks:
        text_words = set(chunk["text"].lower().split())
        overlap = len(query_words & text_words)
        # Combine base score with overlap bonus
        dynamic_score = chunk.get("score", 0.5) + (overlap * 0.02)
        scored.append({**chunk, "score": min(dynamic_score, 1.0)})

    # Sort by score descending and take top_k
    scored.sort(key=lambda c: c.get("score", 0), reverse=True)

    logger.debug(
        "Mock retriever — category=%s, returning %d/%d chunks",
        cat_key, min(top_k, len(scored)), len(scored),
    )

    return scored[:top_k]


async def _real_retrieve(
    query: str,
    top_k: int,
    category: QueryCategory | None,
) -> list[dict]:
    """
    Real retriever — queries ChromaDB with embedded query.

    TODO: Wire this once Tech 1 delivers the vector DB.

    Expected flow:
        1. Embed query using sentence-transformers
        2. Query ChromaDB collection with optional category filter
        3. Return top_k chunks with metadata
    """
    logger.warning(
        "Real retriever called but not yet implemented. "
        "Set USE_MOCK_RETRIEVER=true in .env to use mock data."
    )

    # Placeholder — return the structure Tech 1 will implement
    # from chromadb import PersistentClient
    # from sentence_transformers import SentenceTransformer
    #
    # model = SentenceTransformer(settings.embedding_model)
    # query_embedding = model.encode(query).tolist()
    #
    # client = PersistentClient(path=settings.chroma_persist_dir)
    # collection = client.get_collection(settings.chroma_collection)
    #
    # where_filter = {"category": category.value} if category else None
    # results = collection.query(
    #     query_embeddings=[query_embedding],
    #     n_results=top_k,
    #     where=where_filter,
    # )
    #
    # chunks = []
    # for i, doc in enumerate(results["documents"][0]):
    #     chunks.append({
    #         "text": doc,
    #         "metadata": results["metadatas"][0][i],
    #         "score": 1 - results["distances"][0][i],  # ChromaDB returns distances
    #     })
    # return chunks

    return []
