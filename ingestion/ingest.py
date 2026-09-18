"""
BIS AI Assistant — Ingestion Pipeline (Tech 2: Data & Ingestion)

Full end-to-end ingestion runner:
  1. Reads all raw BIS documents (.pdf, .json, .txt, .md) from data/raw/
  2. Parses them with DocumentParser
  3. Chunks them with ClauseAwareChunker
  4. Exports structured chunks to data/processed/chunks.json
  5. Generates dense embeddings and indexes them into ChromaDB (data/vectordb/)
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional

from backend.config import settings
from ingestion.chunker import ClauseAwareChunker
from ingestion.parser import DocumentParser
from ingestion.seed_data import generate_seed_corpus

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("bis_assistant.ingest")


def run_ingestion(
    raw_dir: str | Path = "data/raw",
    processed_dir: str | Path = "data/processed",
    force_reseed: bool = False,
    persist_chroma: bool = True,
) -> int:
    """
    Execute complete ingestion workflow.
    Returns total number of chunks ingested into the vector DB.
    """
    raw_path = Path(raw_dir)
    processed_path = Path(processed_dir)
    raw_path.mkdir(parents=True, exist_ok=True)
    processed_path.mkdir(parents=True, exist_ok=True)

    # 1. Check for raw files, or seed curated data
    existing_files = [f for f in raw_path.iterdir() if f.is_file() and f.name != ".gitkeep"]
    if not existing_files or force_reseed:
        logger.info("Raw data directory is empty or reseed requested. Generating seed BIS corpus...")
        generate_seed_corpus(raw_path)
        existing_files = [f for f in raw_path.iterdir() if f.is_file() and f.name != ".gitkeep"]

    logger.info("Discovered %d source file(s) in '%s'", len(existing_files), raw_path)

    # 2. Parse documents
    parser = DocumentParser()
    parsed_docs = []

    for file_path in existing_files:
        try:
            doc = parser.parse_file(file_path)
            parsed_docs.append(doc)
            logger.info(
                "Parsed '%s' -> %d sections (ID: %s, Category: %s)",
                file_path.name,
                len(doc.sections),
                doc.document_id,
                doc.category,
            )
        except Exception as e:
            logger.error("Failed to parse '%s': %s", file_path.name, e)

    if not parsed_docs:
        logger.warning("No documents were successfully parsed. Exiting ingestion.")
        return 0

    # 3. Chunk documents using ClauseAwareChunker
    chunker = ClauseAwareChunker()
    all_chunks = []

    for doc in parsed_docs:
        chunks = chunker.chunk_document(doc)
        all_chunks.extend(chunks)

    logger.info("Successfully produced %d clause-aware chunks in total.", len(all_chunks))

    # 4. Save processed chunks to JSON for auditing & inspection
    chunks_json_path = processed_path / "chunks.json"
    chunk_dicts = [c.to_dict() for c in all_chunks]
    with open(chunks_json_path, "w", encoding="utf-8") as f:
        json.dump(chunk_dicts, f, indent=2, ensure_ascii=False)
    logger.info("Saved %d chunks to '%s'", len(chunk_dicts), chunks_json_path)

    # 5. Embed & index into ChromaDB
    if persist_chroma:
        _index_into_chromadb(all_chunks)

    return len(all_chunks)


def _index_into_chromadb(chunks: list) -> None:
    """Index chunks into persistent ChromaDB collection."""
    logger.info(
        "Connecting to ChromaDB at '%s' (collection: '%s')...",
        settings.chroma_persist_dir,
        settings.chroma_collection,
    )

    try:
        import chromadb
        from chromadb.config import Settings as ChromaSettings

        chroma_dir = Path(settings.chroma_persist_dir)
        chroma_dir.mkdir(parents=True, exist_ok=True)

        client = chromadb.PersistentClient(
            path=str(chroma_dir),
            settings=ChromaSettings(anonymized_telemetry=False),
        )

        # Recreate or retrieve collection
        try:
            client.delete_collection(settings.chroma_collection)
            logger.info("Cleared existing collection '%s'", settings.chroma_collection)
        except Exception:
            pass

        # Try to use SentenceTransformerEmbeddingFunction if available
        embedding_fn = None
        try:
            from chromadb.utils import embedding_functions
            embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=settings.embedding_model
            )
            logger.info("Using SentenceTransformerEmbeddingFunction ('%s')", settings.embedding_model)
        except Exception as e:
            logger.info("SentenceTransformer function fallback: ChromaDB default embedding will be used (%s)", e)

        collection = client.get_or_create_collection(
            name=settings.chroma_collection,
            embedding_function=embedding_fn,
            metadata={"description": "BIS Indian Standards & Service Guidelines"},
        )

        # Batch insert chunks
        ids = [c.chunk_id for c in chunks]
        docs = [c.text for c in chunks]
        metadatas = [
            {
                "document": c.document_id,
                "clause": c.clause,
                "title": c.title,
                "category": c.category,
                "page": str(c.page) if c.page else "1",
                "url": c.url,
            }
            for c in chunks
        ]

        batch_size = 50
        for i in range(0, len(ids), batch_size):
            batch_end = min(i + batch_size, len(ids))
            collection.add(
                ids=ids[i:batch_end],
                documents=docs[i:batch_end],
                metadatas=metadatas[i:batch_end],
            )
            logger.debug("Indexed chunks %d to %d into ChromaDB", i + 1, batch_end)

        logger.info(
            "Successfully indexed %d chunks into ChromaDB collection '%s'!",
            collection.count(),
            settings.chroma_collection,
        )

    except ImportError as e:
        logger.error(
            "ChromaDB is not installed or import failed (%s). "
            "Chunks are saved in '%s/chunks.json' and ready for ingestion once ChromaDB is available.",
            e,
            settings.chroma_persist_dir,
        )
    except Exception as e:
        logger.error("Error during ChromaDB indexing: %s", e, exc_info=True)


if __name__ == "__main__":
    cli_parser = argparse.ArgumentParser(description="Ingest BIS documents into vector database")
    cli_parser.add_argument("--raw-dir", default="data/raw", help="Path to raw source files")
    cli_parser.add_argument("--processed-dir", default="data/processed", help="Path for processed output")
    cli_parser.add_argument("--reseed", action="store_true", help="Force recreate seed documents")
    cli_parser.add_argument("--no-chroma", action="store_true", help="Skip ChromaDB indexing")

    args = cli_parser.parse_args()
    count = run_ingestion(
        raw_dir=args.raw_dir,
        processed_dir=args.processed_dir,
        force_reseed=args.reseed,
        persist_chroma=not args.no_chroma,
    )
    print(f"\n[OK] Ingestion complete: {count} chunks processed.")
