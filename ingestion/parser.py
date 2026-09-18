"""
BIS AI Assistant — Document Parser (Tech 2: Data Ingestion)

Extracts clean text, structured tables, section headings, and metadata
from BIS knowledge sources:
  - PDF files (BIS Gazette notifications, IS standards, scheme guides via PyMuPDF)
  - JSON files (curated standards catalogs, scheme matrices, lab directories)
  - Text / Markdown files (.txt, .md)
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("bis_assistant.parser")


@dataclass
class ParsedSection:
    """A distinct structural section or clause extracted from a document."""
    title: str
    clause_id: Optional[str]
    content: str
    page_number: Optional[int] = None
    table_data: Optional[list[dict[str, Any]]] = None


@dataclass
class ParsedDocument:
    """Standardized representation of a parsed BIS source document."""
    document_id: str
    title: str
    category: str  # "standards", "certification", "hallmarking", "consumer", "lab_suggestion", "general"
    source_type: str  # "pdf", "json", "markdown", "text"
    source_path: str
    sections: list[ParsedSection] = field(default_factory=list)
    raw_text: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class DocumentParser:
    """Unified parser for BIS document formats."""

    # Regex patterns to detect Indian Standard codes (e.g., IS 10500:2012, IS 16102 (Part 1):2012)
    IS_CODE_PATTERN = re.compile(
        r"\b(IS(?:\s+|/)[0-9]{3,5}(?:\s*(?:\([^\)]+\)|Part\s+[0-9]+))?(?:\s*:\s*[0-9]{4})?)\b",
        re.IGNORECASE,
    )

    def __init__(self):
        self._fitz = None
        try:
            import fitz  # PyMuPDF
            self._fitz = fitz
        except ImportError:
            logger.warning("PyMuPDF (fitz) is not installed. PDF parsing will use text fallback.")

    def parse_file(self, file_path: str | Path) -> ParsedDocument:
        """Parse any supported file format based on extension."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        suffix = path.suffix.lower()
        if suffix == ".pdf":
            return self.parse_pdf(path)
        elif suffix == ".json":
            return self.parse_json(path)
        elif suffix in (".txt", ".md"):
            return self.parse_text(path)
        else:
            raise ValueError(f"Unsupported document format: {suffix}")

    def parse_pdf(self, path: Path) -> ParsedDocument:
        """
        Parse a PDF file using PyMuPDF.
        Preserves page numbers, clause headings, and structural markers.
        """
        if not self._fitz:
            raise RuntimeError("PyMuPDF is required to parse PDF files. Install via `pip install pymupdf`.")

        doc = self._fitz.open(str(path))
        sections: list[ParsedSection] = []
        full_text_parts: list[str] = []

        doc_title = path.stem.replace("_", " ").title()
        detected_is_code = self._extract_is_code(path.stem)

        for page_idx, page in enumerate(doc):
            page_num = page_idx + 1
            text = page.get_text("text")
            if not text.strip():
                continue

            clean_page_text = self._clean_text(text)
            full_text_parts.append(clean_page_text)

            # Check for standard IS code on first page
            if page_num == 1 and not detected_is_code:
                match = self.IS_CODE_PATTERN.search(clean_page_text)
                if match:
                    detected_is_code = match.group(1).strip()

            # Identify clause / section blocks on the page
            page_sections = self._split_page_into_sections(clean_page_text, page_num)
            sections.extend(page_sections)

        raw_full_text = "\n\n".join(full_text_parts)
        category = self._infer_category(raw_full_text, path.stem)

        metadata = {
            "is_code": detected_is_code or path.stem,
            "page_count": len(doc),
            "filename": path.name,
            "url": "https://www.bis.gov.in",
        }

        return ParsedDocument(
            document_id=detected_is_code or path.stem,
            title=doc_title,
            category=category,
            source_type="pdf",
            source_path=str(path),
            sections=sections,
            raw_text=raw_full_text,
            metadata=metadata,
        )

    def parse_json(self, path: Path) -> ParsedDocument:
        """
        Parse a structured JSON file containing BIS standards, schemes, or lab data.
        Expected JSON can either be a single document or a list of standard items.
        """
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        sections: list[ParsedSection] = []
        raw_parts: list[str] = []

        doc_id = data.get("is_code") or data.get("id") or path.stem
        doc_title = data.get("title") or path.stem.replace("_", " ").title()
        category = data.get("category") or self._infer_category(json.dumps(data), path.stem)

        # 1. If JSON specifies explicit clauses/sections
        if "clauses" in data and isinstance(data["clauses"], list):
            for item in data["clauses"]:
                clause_id = item.get("clause") or item.get("id") or ""
                clause_title = item.get("title") or clause_id
                content = item.get("text") or item.get("content") or ""
                page_num = item.get("page", 1)
                table_data = item.get("table")

                sec = ParsedSection(
                    title=f"{clause_id} — {clause_title}".strip(" —"),
                    clause_id=clause_id,
                    content=content,
                    page_number=page_num,
                    table_data=table_data,
                )
                sections.append(sec)
                raw_parts.append(f"{sec.title}\n{content}")

        # 2. If JSON contains an items/standards array
        elif "items" in data and isinstance(data["items"], list):
            for idx, item in enumerate(data["items"]):
                item_code = item.get("is_code") or f"Item {idx + 1}"
                item_title = item.get("title") or ""
                summary = item.get("summary") or item.get("description") or ""
                details = item.get("requirements") or item.get("testing_parameters") or ""

                combined_content = f"{item_title}\n{summary}\n{details}".strip()
                sec = ParsedSection(
                    title=f"{item_code}: {item_title}".strip(": "),
                    clause_id=item_code,
                    content=combined_content,
                    page_number=item.get("page", 1),
                )
                sections.append(sec)
                raw_parts.append(f"{sec.title}\n{combined_content}")

        # 3. Flat JSON dict
        else:
            for k, v in data.items():
                if isinstance(v, (str, int, float)):
                    content = f"{k}: {v}"
                    sections.append(ParsedSection(title=k, clause_id=k, content=content))
                    raw_parts.append(content)
                elif isinstance(v, dict):
                    content = "\n".join(f"{sk}: {sv}" for sk, sv in v.items())
                    sections.append(ParsedSection(title=k, clause_id=k, content=content))
                    raw_parts.append(content)

        raw_text = "\n\n".join(raw_parts)

        return ParsedDocument(
            document_id=doc_id,
            title=doc_title,
            category=category,
            source_type="json",
            source_path=str(path),
            sections=sections,
            raw_text=raw_text,
            metadata=data.get("metadata", {"filename": path.name, "url": "https://www.bis.gov.in"}),
        )

    def parse_text(self, path: Path) -> ParsedDocument:
        """Parse a plain text or Markdown file."""
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        clean = self._clean_text(content)
        detected_is_code = self._extract_is_code(clean) or self._extract_is_code(path.stem)
        doc_title = path.stem.replace("_", " ").title()
        category = self._infer_category(clean, path.stem)

        sections = self._split_text_into_sections(clean)

        return ParsedDocument(
            document_id=detected_is_code or path.stem,
            title=doc_title,
            category=category,
            source_type="markdown" if path.suffix == ".md" else "text",
            source_path=str(path),
            sections=sections,
            raw_text=clean,
            metadata={"filename": path.name, "is_code": detected_is_code},
        )

    # -----------------------------------------------------------------------
    # Helper & Cleaning Methods
    # -----------------------------------------------------------------------

    def _clean_text(self, text: str) -> str:
        """Normalize line breaks and clean whitespace artifacts."""
        # Replace multiple spaces with a single space, preserve intentional newlines
        text = re.sub(r"\r\n|\r", "\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _extract_is_code(self, text: str) -> Optional[str]:
        """Attempt to extract an official IS code from text."""
        match = self.IS_CODE_PATTERN.search(text)
        return match.group(1).strip() if match else None

    def _infer_category(self, text: str, hint: str = "") -> str:
        """Infer QueryCategory from document text keywords."""
        lower_combined = f"{hint} {text[:3000]}".lower()

        if any(w in lower_combined for w in ["hallmark", "huid", "carat", "gold purity", "silver purity", "ahc"]):
            return "hallmarking"
        elif any(w in lower_combined for w in ["laboratory", "testing facility", "nabl", "test charges", "testing lab"]):
            return "lab_suggestion"
        elif any(w in lower_combined for w in ["scheme i", "scheme ii", "crs", "fmcs", "eco mark", "scheme x", "licensing fee", "factory inspection"]):
            return "certification"
        elif any(w in lower_combined for w in ["consumer", "complaint", "grievance", "bis care", "misuse of isi", "penalty"]):
            return "consumer"
        else:
            return "standards"

    def _split_page_into_sections(self, page_text: str, page_num: int) -> list[ParsedSection]:
        """Split a page into structured sections based on clause / heading patterns."""
        # Split on patterns like: Clause 4.1, Section 2, Table 1, 4.1 Scope, etc.
        pattern = re.compile(
            r"(?:\n|^)(?=(?:(?:Clause|Section|Table|Annex|Part)\s+[0-9A-Za-z\.\-]+|[0-9]+\.[0-9]+(?:\.[0-9]+)?\s+[A-Z]))",
            re.MULTILINE,
        )
        splits = pattern.split(page_text)
        sections = []

        for idx, chunk in enumerate(splits):
            chunk = chunk.strip()
            if not chunk:
                continue

            first_line = chunk.split("\n", 1)[0].strip()
            sections.append(
                ParsedSection(
                    title=first_line[:80],
                    clause_id=first_line.split()[0] if first_line else f"P{page_num}-S{idx+1}",
                    content=chunk,
                    page_number=page_num,
                )
            )

        if not sections:
            sections.append(
                ParsedSection(
                    title=f"Page {page_num}",
                    clause_id=f"Page {page_num}",
                    content=page_text,
                    page_number=page_num,
                )
            )

        return sections

    def _split_text_into_sections(self, text: str) -> list[ParsedSection]:
        """Split markdown/plain text by headings or clause headers."""
        # Split on markdown headers (# or ##) or clause numbers
        pattern = re.compile(r"(?:\n|^)(?=#{1,4}\s+|Clause\s+[0-9\.\-]+|[0-9]+\.[0-9]+(?:\.[0-9]+)?\s+)", re.MULTILINE)
        parts = pattern.split(text)
        sections = []

        for idx, part in enumerate(parts):
            part = part.strip()
            if not part:
                continue

            first_line = part.split("\n", 1)[0].replace("#", "").strip()
            sections.append(
                ParsedSection(
                    title=first_line[:80],
                    clause_id=first_line.split()[0] if first_line else f"Sec-{idx+1}",
                    content=part,
                )
            )

        return sections or [ParsedSection(title="Full Document", clause_id="1.0", content=text)]
