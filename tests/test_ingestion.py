"""
Unit tests for BIS Ingestion Pipeline (DocumentParser & ClauseAwareChunker)
"""

from pathlib import Path
from ingestion.parser import DocumentParser, ParsedDocument, ParsedSection
from ingestion.chunker import ClauseAwareChunker


def test_parser_with_seed_json():
    parser = DocumentParser()
    sample_file = Path("data/raw/is_10500_2012.json")
    assert sample_file.exists(), "Seed file is_10500_2012.json should exist"

    doc = parser.parse_file(sample_file)
    assert doc.document_id == "IS 10500:2012"
    assert doc.category == "standards"
    assert len(doc.sections) >= 4
    assert any("Table 1" in s.title for s in doc.sections)


def test_chunker_preserves_clauses():
    chunker = ClauseAwareChunker(target_chunk_size=1000, max_chunk_size=1500)
    
    mock_doc = ParsedDocument(
        document_id="IS 2347:2017",
        title="Domestic Pressure Cookers",
        category="standards",
        source_type="json",
        source_path="test_cookers.json",
        sections=[
            ParsedSection(
                title="Clause 4.1 Materials",
                clause_id="Clause 4.1",
                content="Pressure cooker bodies must be made of food-grade stainless steel (AISI 304) or aluminium alloy with minimum thickness 3.25 mm.",
                page_number=3,
            ),
            ParsedSection(
                title="Clause 6.3 Safety Vent",
                clause_id="Clause 6.3",
                content="Every cooker must have a primary pressure regulating vent (1.0 kgf/cm²) and a fusible safety valve (fuses between 1.4 to 2.0 kgf/cm²).",
                page_number=5,
            ),
        ],
    )

    chunks = chunker.chunk_document(mock_doc)
    assert len(chunks) == 2
    assert chunks[0].document_id == "IS 2347:2017"
    assert chunks[0].clause == "Clause 4.1"
    assert chunks[0].category == "standards"
    assert "stainless steel" in chunks[0].text
    assert chunks[1].clause == "Clause 6.3"
    assert "fusible safety valve" in chunks[1].text


def test_table_formatting():
    chunker = ClauseAwareChunker()
    table_section = ParsedSection(
        title="Table 1 Physical Parameters",
        clause_id="Table 1",
        content="Limits for water characteristics:",
        table_data=[
            {"Parameter": "Turbidity", "Acceptable": "1 NTU", "Permissible": "5 NTU"},
            {"Parameter": "TDS", "Acceptable": "500 mg/L", "Permissible": "2000 mg/L"},
        ],
    )
    mock_doc = ParsedDocument(
        document_id="IS 10500:2012",
        title="Drinking Water",
        category="standards",
        source_type="json",
        source_path="mock.json",
        sections=[table_section],
    )
    chunks = chunker.chunk_document(mock_doc)
    assert len(chunks) == 1
    assert "| Parameter | Acceptable | Permissible |" in chunks[0].text
    assert "| Turbidity | 1 NTU | 5 NTU |" in chunks[0].text
    assert "| TDS | 500 mg/L | 2000 mg/L |" in chunks[0].text
