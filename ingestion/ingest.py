"""
ingest.py — Parse, chunk, embed BIS source docs into vector DB (owned by Tech 2)

Takes the chunks from data/processed/chunks.jsonl (built by chunker.py) and:
    1. Converts each chunk's text into an embedding (a vector of numbers
       representing its meaning) using sentence-transformers
    2. Stores each chunk + its embedding + its metadata into ChromaDB

Once this runs, backend/services/retriever.py can search this vector DB
to find relevant chunks for any user question.

USAGE:
    pip install sentence-transformers chromadb
    python ingestion/ingest.py

Output:
    A ChromaDB collection saved to data/chroma_db/ (persisted on disk)
"""

import json
import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = "data/processed/chunks.jsonl"
CHROMA_DB_PATH = "./data/vectordb"  # must match backend/config.py's CHROMA_PERSIST_DIR default
COLLECTION_NAME = "bis_documents"

# A small, fast, well-regarded embedding model — good default for a hackathon
# (runs on CPU fine, no GPU needed, ~80MB download)
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


def load_chunks() -> list[dict]:
    chunks = []
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    return chunks


def main():
    print("Loading chunks...")
    chunks = load_chunks()
    print(f"  Loaded {len(chunks)} chunks.")

    print(f"Loading embedding model ({EMBEDDING_MODEL_NAME})... this downloads ~80MB the first time.")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    print("Setting up ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    # If a collection with this name already exists (e.g. from a previous
    # run), delete it first so we don't end up with duplicate/stale data.
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"  Removed existing '{COLLECTION_NAME}' collection to rebuild fresh.")
    except Exception:
        pass  # collection didn't exist yet, that's fine

    collection = client.create_collection(name=COLLECTION_NAME)

    print("Embedding and storing chunks (this may take a minute)...")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    ids = [chunk["chunk_id"] for chunk in chunks]
    metadatas = [
        {
            "source_document": chunk["source_document"],
            "document_title": chunk["document_title"],
            "source_url": chunk["source_url"],
            "capability": chunk["capability"],
            "chunk_index_in_doc": chunk["chunk_index_in_doc"],
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
    )

    print(f"\nDone. {len(chunks)} chunks embedded and stored in ChromaDB at {CHROMA_DB_PATH}/")
    print(f"Collection name: {COLLECTION_NAME}")

    # Quick sanity check: run one test query
    print("\n--- Sanity check: test query ---")
    test_query = "What is the ISI mark?"
    test_embedding = model.encode([test_query]).tolist()
    results = collection.query(query_embeddings=test_embedding, n_results=3)
    print(f"Query: '{test_query}'")
    for i, doc in enumerate(results["documents"][0]):
        title = results["metadatas"][0][i]["document_title"]
        print(f"  [{i+1}] From: {title}")
        print(f"      {doc[:150]}...")


if __name__ == "__main__":
    main()
