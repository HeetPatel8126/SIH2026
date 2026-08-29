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

# Run the server
uvicorn backend.api:app --reload --port 8000
```

API docs available at **http://localhost:8000/docs**

## API Endpoints

| Endpoint                 | Method | Description                       |
| ------------------------ | ------ | --------------------------------- |
| `/health`              | GET    | Health check                      |
| `/chat`                | POST   | Conversational Q&A with citations |
| `/search-standards`    | POST   | Search Indian Standards           |
| `/certification-guide` | POST   | BIS certification guidance        |

## Tech Stack

- **Backend:** FastAPI + Uvicorn
- **LLM:** Ollama (Llama 3.x) / hosted API
- **Vector DB:** ChromaDB
- **Embeddings:** sentence-transformers
- **Frontend:** React / Streamlit

## Project Structure

```
├── backend/          # FastAPI backend, services, prompt templates
├── ingestion/        # Document parsing & embedding pipeline
├── data/             # Raw docs, processed chunks, vector DB
├── frontend/         # Chat UI
└── tests/            # API tests & evaluation queries
```

## License

Built for Smart India Hackathon 2026.
