"""
BIS AI Assistant — Clause-Aware Chunker (Tech 2: Data Ingestion)

Implements clause-aware semantic chunking for Indian Standards and BIS documents.
Ensures:
  - Regulatory clauses, requirement tables, and statutory limits are kept intact.
  - No blind character slicing across clauses or critical parameters.
  - Rich metadata (document ID, clause, page, category, source URL) attached to each chunk.
"""

from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import asdict, dataclass
from typing import Any, Optional

from ingestion.parser import ParsedDocument, ParsedSection

logger = logging.getLogger("bis_assistant.chunker")


@dataclass
class DocumentChunk:
    """A semantic chunk ready for vector embedding and retrieval."""
    chunk_id: str
    text: str
    document_id: str
    clause: str
    title: str
    category: str
    page: Optional[int]
    url: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert chunk to standard dictionary representation."""
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "document_id": self.document_id,
            "clause": self.clause,
            "title": self.title,
            "category": self.category,
            "page": self.page,
            "url": self.url,
            "metadata": {
                **self.metadata,
                "document": self.document_id,
                "clause": self.clause,
                "title": self.title,
                "category": self.category,
                "page": str(self.page) if self.page else "1",
                "url": self.url,
            },
        }


class ClauseAwareChunker:
    """
    Splits ParsedDocuments into clause-bounded chunks with semantic overlap.
    """

    def __init__(
        self,
        target_chunk_size: int = 1200,
        max_chunk_size: int = 1800,
        overlap_size: int = 200,
    ):
        self.target_chunk_size = target_chunk_size
        self.max_chunk_size = max_chunk_size
        self.overlap_size = overlap_size

    def chunk_document(self, doc: ParsedDocument) -> list[DocumentChunk]:
        """
        Process a ParsedDocument into a list of DocumentChunk instances.
        """
        chunks: list[DocumentChunk] = []

        for sec_idx, section in enumerate(doc.sections):
            section_chunks = self._chunk_section(doc, section, sec_idx)
            chunks.extend(section_chunks)

        logger.info(
            "Chunked document '%s' (%s) into %d chunks",
            doc.document_id,
            doc.category,
            len(chunks),
        )
        return chunks

    def _chunk_section(
        self,
        doc: ParsedDocument,
        section: ParsedSection,
        sec_idx: int,
    ) -> list[DocumentChunk]:
        """Process an individual section into one or more chunks."""
        text = section.content.strip()
        if not text:
            return []

        # If section has structured table data, format into markdown
        if section.table_data:
            table_text = self._format_table_to_markdown(section.table_data)
            if table_text:
                text = f"{text}\n\n{table_text}"

        clause_label = section.clause_id or section.title or f"Clause {sec_idx + 1}"
        doc_url = doc.metadata.get("url", "https://www.bis.gov.in")

        # 1. Section fits cleanly in max_chunk_size -> Keep whole!
        if len(text) <= self.max_chunk_size:
            chunk_text = f"[{doc.document_id}] {doc.title}\n{clause_label}:\n{text}"
            chunk_id = self._generate_chunk_id(doc.document_id, clause_label, 0)
            return [
                DocumentChunk(
                    chunk_id=chunk_id,
                    text=chunk_text,
                    document_id=doc.document_id,
                    clause=clause_label,
                    title=doc.title,
                    category=doc.category,
                    page=section.page_number,
                    url=doc_url,
                    metadata={"section_index": sec_idx},
                )
            ]

        # 2. Section is large -> Split on paragraph/sentence boundaries with overlap
        chunks: list[DocumentChunk] = []
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        
        current_chunk_parts: list[str] = []
        current_len = 0
        sub_idx = 0

        for p in paragraphs:
            p_len = len(p)
            if current_len + p_len > self.target_chunk_size and current_chunk_parts:
                # Flush current chunk
                body = "\n\n".join(current_chunk_parts)
                chunk_text = f"[{doc.document_id}] {doc.title}\n{clause_label} (Part {sub_idx + 1}):\n{body}"
                chunk_id = self._generate_chunk_id(doc.document_id, clause_label, sub_idx)
                
                chunks.append(
                    DocumentChunk(
                        chunk_id=chunk_id,
                        text=chunk_text,
                        document_id=doc.document_id,
                        clause=f"{clause_label} (Part {sub_idx + 1})",
                        title=doc.title,
                        category=doc.category,
                        page=section.page_number,
                        url=doc_url,
                        metadata={"section_index": sec_idx, "sub_index": sub_idx},
                    )
                )
                sub_idx += 1

                # Retain overlap from end of previous chunk if possible
                overlap_text = body[-self.overlap_size:] if len(body) > self.overlap_size else ""
                current_chunk_parts = [overlap_text, p] if overlap_text else [p]
                current_len = len(current_chunk_parts[0]) + p_len
            else:
                current_chunk_parts.append(p)
                current_len += p_len

        # Flush final remaining chunk
        if current_chunk_parts:
            body = "\n\n".join(current_chunk_parts)
            part_suffix = f" (Part {sub_idx + 1})" if sub_idx > 0 else ""
            chunk_text = f"[{doc.document_id}] {doc.title}\n{clause_label}{part_suffix}:\n{body}"
            chunk_id = self._generate_chunk_id(doc.document_id, clause_label, sub_idx)

            chunks.append(
                DocumentChunk(
                    chunk_id=chunk_id,
                    text=chunk_text,
                    document_id=doc.document_id,
                    clause=f"{clause_label}{part_suffix}",
                    title=doc.title,
                    category=doc.category,
                    page=section.page_number,
                    url=doc_url,
                    metadata={"section_index": sec_idx, "sub_index": sub_idx},
                )
            )

        return chunks

    def _format_table_to_markdown(self, table: list[dict[str, Any]]) -> str:
        """Render list-of-dicts table data into a clean Markdown table."""
        if not table or not isinstance(table, list):
            return ""

        headers = list(table[0].keys())
        if not headers:
            return ""

        header_line = "| " + " | ".join(headers) + " |"
        sep_line = "| " + " | ".join(["---"] * len(headers)) + " |"
        rows = []

        for row in table:
            row_str = "| " + " | ".join(str(row.get(h, "")) for h in headers) + " |"
            rows.append(row_str)

        return "\n".join([header_line, sep_line] + rows)

    def _generate_chunk_id(self, doc_id: str, clause: str, part: int) -> str:
        """Create a reproducible deterministic chunk ID."""
        clean_doc = re.sub(r"[^a-zA-Z0-9]+", "_", doc_id).lower()
        clean_clause = re.sub(r"[^a-zA-Z0-9]+", "_", clause).lower()[:30]
        raw_sig = f"{clean_doc}_{clean_clause}_{part}"
        digest = hashlib.md5(raw_sig.encode()).hexdigest()[:6]
        return f"{clean_doc[:15]}_{clean_clause[:20]}_{digest}"
