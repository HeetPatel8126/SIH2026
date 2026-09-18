"""
chunker.py — Document chunker: splits parsed documents into chunks with metadata.

Takes the raw .txt files from data/raw/ (produced by parser.py / scrape_bis.py)
and splits each into ~300-word chunks, keeping track of which source document
and capability each chunk came from. This is what gets embedded into the
vector DB (ChromaDB) in ingest.py.

USAGE:
    python ingestion/chunker.py

Output:
    data/processed/chunks.jsonl   (one JSON object per line, one per chunk)
"""

import os
import json
import csv

RAW_DIR = "data/raw"
OUTPUT_DIR = "data/processed"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "chunks.jsonl")

CHUNK_SIZE_WORDS = 300     # target words per chunk
CHUNK_OVERLAP_WORDS = 50   # words repeated between consecutive chunks, so we
                           # don't lose context right at a chunk boundary


def load_index() -> dict:
    """Loads data/raw/_index.csv into a lookup: filename -> {capability, title, url}"""
    index_path = os.path.join(RAW_DIR, "_index.csv")
    lookup = {}
    with open(index_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lookup[row["filename"]] = row
    return lookup


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Splits text into overlapping word-based chunks."""
    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        if end >= len(words):
            break
        start = end - overlap  # step back by the overlap amount
    return chunks


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    index = load_index()

    all_chunks = []
    chunk_id_counter = 0

    for filename, meta in index.items():
        filepath = os.path.join(RAW_DIR, filename)
        if not os.path.exists(filepath):
            print(f"  WARNING: {filename} in index but file not found, skipping.")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Skip the "SOURCE URL: ... / TITLE: ..." header lines we added when scraping
        body = content.split("\n\n", 1)[-1] if "\n\n" in content else content

        chunks = chunk_text(body, CHUNK_SIZE_WORDS, CHUNK_OVERLAP_WORDS)
        print(f"{filename}: {len(chunks)} chunks")

        for i, chunk_text_value in enumerate(chunks):
            chunk_id_counter += 1
            all_chunks.append({
                "chunk_id": f"chunk_{chunk_id_counter:04d}",
                "text": chunk_text_value,
                "source_document": filename,
                "document_title": meta["title"],
                "source_url": meta["url"],
                "capability": meta["capability"],
                "chunk_index_in_doc": i,
            })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"\nDone. {len(all_chunks)} total chunks saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()