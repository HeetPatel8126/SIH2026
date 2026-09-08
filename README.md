# 🏛️ BIS AI Assistant

AI-powered conversational assistant for **Indian Standards & BIS Services** — built for SIH 2026.

Ask questions about Indian Standards, certification schemes, hallmarking, and more. Every answer is grounded in real BIS documents with source citations.

## Quick Start

```bash
# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows
# source venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env

# Run the ingestion pipeline (first time only)
python -m ingestion.ingest --reseed

# Run the server
uvicorn backend.api:app --reload --port 8000
```

API docs available at **http://localhost:8000/docs**

## Docker Deployment

```bash
# One-command deployment (backend + frontend)
docker compose up --build

# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API docs: http://localhost:8000/docs
```

## API Endpoints

| Endpoint                 | Method | Description                       |
| ------------------------ | ------ | --------------------------------- |
| `/health`              | GET    | Health check                      |
| `/chat`                | POST   | Conversational Q&A with citations |
| `/chat/stream`         | POST   | SSE streaming Q&A with thinking   |
| `/search-standards`    | POST   | Search Indian Standards           |
| `/certification-guide` | POST   | BIS certification guidance        |

## Key Features

- **RAG Pipeline** — retrieves real BIS documents, never hallucinates
- **Citation Faithfulness** — every inline citation is verified against retrieved chunks
- **Multi-Turn Memory** — follow-up questions work via session-based conversation history
- **Multi-Category Routing** — cross-domain questions retrieve from multiple categories
- **Multilingual** — supports Hindi (Devanagari), Hinglish (Romanized Hindi), and 9 other Indian languages
- **Hybrid Fallback** — automatic offline LLM fallback (Ollama) when cloud providers fail
- **Rate Limiting** — built-in slowapi rate limiter for production readiness

## Tech Stack

- **Backend:** FastAPI + Uvicorn
- **LLM:** Ollama (Llama 3.x / Qwen 2.5) / Groq / Gemini / OpenAI / Anthropic
- **Vector DB:** ChromaDB
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **Frontend:** React (Vite)
- **Deployment:** Docker Compose

## Project Structure

```
├── backend/          # FastAPI backend, services, prompt templates
│   ├── routers/      # chat, standards, certification endpoints
│   ├── services/     # retriever, query router, LLM wrapper, citations, session store
│   ├── prompts/      # Category-specific prompt templates
│   └── models/       # Pydantic schemas
├── ingestion/        # Document parsing & embedding pipeline
├── data/             # Raw docs, processed chunks, vector DB
├── frontend/         # React chat UI
├── tests/            # API tests & evaluation queries
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
└── requirements.txt
```

## Future Roadmap

- **Automated Re-Ingestion Pipeline** — cron-based periodic re-ingestion to keep the knowledge base current with new BIS standards and revisions
- **Document Freshness Tracking** — each chunk carries a source-date; stale content is flagged or deprioritized in retrieval
- **Admin Dashboard** — web interface for corpus management (add/remove documents, view ingestion status, monitor retrieval quality)
- **Production Deployment** — Kubernetes orchestration, managed vector DB (Pinecone/Weaviate), CI/CD pipeline
- **Feedback Loop** — thumbs up/down on answers to identify retrieval gaps and improve the knowledge base
- **Extended Language Support** — full translation pipeline using IndicTrans2 for all 22 scheduled Indian languages

## License

Built for Smart India Hackathon 2026.
