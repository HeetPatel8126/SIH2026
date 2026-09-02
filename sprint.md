# AI-Powered Intelligent Assistant for Indian Standards & BIS Services — Sprint Plan

> **PS ID:** SIH26107 · **Category:** Software · **Theme:** Smart Automation
> **Organization:** Ministry of Consumer Affairs, Food & Public Distribution
> **Goal:** A conversational, source-cited RAG assistant that helps MSMEs, startups, students, and consumers find the right Indian Standard, certification scheme, and BIS process — in plain language.

---

## Team (6 Members)

| Member                        | Role                                 | Owns                                                                                                             | First Task                                                             |
| ----------------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Tech 1 (Rudra/Heet)** | RAG Pipeline + Retrieval Engineer    | Vector DB, embedding pipeline,`retriever.py`, chunking strategy                                                | Stand up vector store, embed 50 sample IS documents                    |
| **Tech 2 (Namish/Om)**  | Data / Knowledge Base Engineer       | Scraping & structuring BIS knowledge (standards catalog, scheme docs, FAQs),`ingest.py`                        | Collect and clean source documents into a corpus folder                |
| **Tech 3 (Heet)**       | Backend / LLM Orchestration Engineer | `api.py`, prompt templates, citation logic, query routing (standards / certification / hallmarking / consumer) | Build FastAPI skeleton + LLM call wrapper                              |
| **Tech 4 (Krrish/Om)**  | Frontend Engineer                    | Chat UI, source-citation display, multilingual toggle                                                            | Build chat interface shell (input box, message thread, citation cards) |
| **Tech 5 (Rudra)**      | QA + Evaluation + Deployment         | Test query set, accuracy/citation-correctness scoring, deployment, README                                        | Build a 30-query test set covering all 8 expected-solution points      |
| **Member 6**            | Presentation + Demo Prep             | Deck, demo script, FAQ cheat sheet, narration                                                                    | Draft the problem framing + elevator pitch slide                       |

---

## 1. Problem Statement (As Given)

**Background.** BIS publishes thousands of Indian Standards and runs services spanning product certification, hallmarking, laboratory recognition, Standards Clubs, training, consumer affairs, and conformity assessment. Today, people struggle to figure out which standard applies to their product, what certification they need, which BIS scheme fits, how licensing works, what testing is required, and where to get answers — especially MSMEs, startups, students, and everyday consumers who don't have time to dig through scattered PDFs and portals.

**Ask.** Build an AI conversational assistant that understands natural-language questions and returns accurate, source-backed answers about Indian Standards and BIS services, citing the specific document or clause behind each answer.

### Expected Solution — 8 Capabilities

| # | Capability                                                                       | Priority                      |
| - | -------------------------------------------------------------------------------- | ----------------------------- |
| 1 | Answer questions about Indian Standards                                          | P0                            |
| 2 | Recommend applicable standards from a product description                        | P0                            |
| 3 | Explain BIS certification schemes (ISI, CRS, FMCS, Hallmark, Scheme X, ECO Mark) | P0                            |
| 4 | Explain certification processes step-by-step                                     | P0                            |
| 5 | Answer consumer-related queries (complaints, verifying a mark, grievances)       | P1                            |
| 6 | Guide users on hallmarking                                                       | P1                            |
| 7 | Suggest relevant testing laboratories                                            | P1                            |
| 8 | Support multilingual interaction                                                 | P1 — build after P0 is solid |

---

## 2. Simple Explanation (ELI5)

Think of it as **"ChatGPT, but it only knows BIS and never makes things up."**

A user types something like *"I make LED bulbs, what BIS certificate do I need?"* Instead of guessing, the assistant:

1. Searches a library of real BIS documents (standards, scheme guides, FAQs) for the relevant passages,
2. Hands those passages to an LLM along with the question,
3. The LLM writes an answer **using only what it found**, and
4. The answer comes back with a clickable/visible reference to the exact document or clause it used.

This pattern — retrieve real documents first, then generate an answer grounded in them — is called **RAG (Retrieval-Augmented Generation)**. It's what stops the bot from hallucinating a fake IS code or a made-up fee.

---

## 3. Tech Stack

| Layer                      | Choice                                                                                                                | Why                                                                        |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **LLM**              | Open-source (Llama 3.x / Qwen2.5) via Ollama, or a hosted API (Claude/GPT) if internet access is allowed at the venue | Generates the final natural-language answer from retrieved context         |
| **Embeddings**       | `bge-base-en` or `all-MiniLM-L6-v2` (sentence-transformers)                                                       | Turns document chunks + queries into vectors for similarity search         |
| **Vector DB**        | ChromaDB (local, zero-setup) or FAISS                                                                                 | Stores embedded chunks, does fast nearest-neighbor retrieval               |
| **Orchestration**    | LangChain or a hand-rolled retriever + prompt pipeline                                                                | Wires retrieval → prompt → LLM → citation together                      |
| **Backend**          | FastAPI (Python)                                                                                                      | Serves`/chat`, `/search-standards`, `/certification-guide` endpoints |
| **Frontend**         | React (or Streamlit for a faster build)                                                                               | Chat interface with source-citation cards                                  |
| **Document parsing** | PyMuPDF / pdfplumber + BeautifulSoup                                                                                  | Extracts and chunks BIS PDFs and portal pages, keeps page/clause numbers   |
| **Multilingual**     | IndicTrans2 or the LLM's native multilingual ability + language-detect on input                                       | Lets users ask in Hindi/regional languages                                 |
| **Deployment**       | Docker Compose (API + vector DB + frontend)                                                                           | One-command spin-up for demo and judges                                    |

---

## 4. Architecture

```
                          ┌─────────────────────┐
                          │   User (Chat UI)     │
                          │  "What standard for  │
                          │   LED bulbs?"        │
                          └──────────┬───────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │   FastAPI Backend    │
                          │  - Query router       │
                          │  - Language detect    │
                          └──────────┬───────────┘
                                     │
                     ┌───────────────┼───────────────┐
                     ▼               ▼               ▼
             ┌───────────┐   ┌───────────────┐  ┌─────────────┐
             │ Embedding  │   │ Vector DB      │  │ Query Router │
             │ Model      │──▶│ (ChromaDB)     │  │ (standards /│
             │ (query →   │   │ top-k chunks   │  │ certify /   │
             │  vector)   │   │ + metadata     │  │ hallmark /  │
             └───────────┘   └───────┬────────┘  │ consumer)   │
                                     │            └─────────────┘
                                     ▼
                          ┌─────────────────────┐
                          │  Prompt Builder       │
                          │  context + question   │
                          │  + citation template  │
                          └──────────┬───────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │      LLM              │
                          │  generates grounded    │
                          │  answer + cites source │
                          └──────────┬───────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │  Response + Citations │
                          │  → back to Chat UI    │
                          └─────────────────────┘

        ── offline / setup-time pipeline ──
   BIS Sources (Standards catalog, scheme PDFs,
   hallmarking guides, FAQs, lab directory)
              │
              ▼
   ┌─────────────────┐     ┌──────────────┐
   │ Extractor/Chunker │──▶│ Embedding Model│──▶ Vector DB (above)
   │ (keeps clause/    │   │                │
   │  page metadata)   │   └──────────────┘
   └─────────────────┘
```

---

## 5. Workflow (End-to-End)

1. **Ingestion (one-time / periodic):** Pull BIS knowledge sources — standards catalog, certification scheme documents, hallmarking guides, lab directory, consumer FAQs — chunk them while preserving clause/page numbers, embed, and store in the vector DB.
2. **User asks a question** in the chat UI, in any supported language.
3. **Query router** classifies intent: standard lookup, certification guidance, hallmarking, lab suggestion, or general consumer query.
4. **Retriever** embeds the query and pulls the top-k most relevant chunks from the vector DB.
5. **Prompt builder** assembles a prompt: system instructions ("answer only from the given context, always cite"), the retrieved chunks, and the user's question.
6. **LLM generates the answer**, grounded in the retrieved text, with inline references to the source document/clause.
7. **Response renders** in the UI with the answer plus expandable citation cards (document name, clause, link).
8. **Feedback loop (stretch):** thumbs up/down on answers to flag retrieval gaps for the knowledge base team.

---

## 6. Divided Work — Build Order (3-Day Style Sprint)

| Day             | Focus                 | Key Deliverable                                                                                                                                                                                      |
| --------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Day 1** | Vertical slice        | Ingest ~50 sample docs → embed → retrieve → one working`/chat` call → plain-text answer with a citation, end to end                                                                            |
| **Day 2** | Breadth               | All 8 expected-solution capabilities wired (standards Q&A, recommendation, certification schemes, process explainer, consumer queries, hallmarking, lab suggestion, multilingual toggle) + UI polish |
| **Day 3** | Hardening + demo prep | Run the 30-query test set, fix retrieval misses, rehearse the 5-minute demo, freeze features                                                                                                         |

---

## 7. Examples to Use When Presenting

Use these as live demo queries — they map directly to the 8 expected-solution points:

| Query Type                    | Example Question                                                   | What the Demo Should Show                                                                                                                                     |
| ----------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Standard lookup               | *"What is the Indian Standard for packaged drinking water?"*     | Correct IS number + a one-line summary + citation                                                                                                             |
| Product → standard mapping   | *"I manufacture pressure cookers, which standards apply to me?"* | Recommends the relevant IS code and mentions it's a mandatory ISI item                                                                                        |
| Certification scheme guidance | *"What's the difference between ISI Mark and CRS?"*              | Clear side-by-side explanation, correctly scoped (ISI = broad product certification for domestic manufacturers; CRS = electronics/IT, self-declaration based) |
| Process explainer             | *"How do I apply for a BIS license?"*                            | Step-by-step: application → factory inspection → sample testing → license grant                                                                            |
| Consumer query                | *"How do I check if my gold jewellery is genuinely hallmarked?"* | Explains HUID verification via the BIS Care app/portal                                                                                                        |
| Hallmarking guidance          | *"Is hallmarking mandatory for silver jewellery?"*               | States current applicability clearly, cites source                                                                                                            |
| Lab suggestion                | *"Where can I get my product tested near Ahmedabad?"*            | Suggests BIS-recognized labs in the region                                                                                                                    |
| Multilingual                  | Ask the same pressure-cooker question in Hindi                     | Same accurate answer, returned in Hindi                                                                                                                       |

**Elevator pitch (30 sec):** MSMEs and consumers lose days digging through scattered BIS PDFs and portals just to find one applicable standard or certification step. This assistant answers in plain language, in the user's own language, and never invents an answer — every response is grounded in and cited to the actual BIS document behind it.

---

## 8. FAQs About BIS (Judge/Audience Q&A Prep)

**Q: What is BIS?**
BIS (Bureau of Indian Standards) is India's national standards body, functioning under the Ministry of Consumer Affairs, Food & Public Distribution. It sets Indian Standards (IS codes) and certifies that products and processes conform to them.

**Q: What's the difference between ISI Mark, CRS, FMCS, and Hallmark?**

- **ISI Mark (Scheme I / domestic licensing):** Product certification for Indian manufacturers — involves factory inspection, ongoing sample testing, and a license number displayed alongside the mark. Covers items like steel, cement, packaged water, and home appliances.
- **CRS (Compulsory Registration Scheme, Scheme II):** Mainly for electronics and IT products notified by MeitY; based on self-declaration after testing in a BIS-recognized lab, rather than a full license-and-inspection cycle.
- **FMCS (Foreign Manufacturers Certification Scheme):** The route for overseas manufacturers to get the ISI mark on goods exported to India; requires appointing an Authorized Indian Representative and undergoing factory inspection abroad.
- **Hallmarking:** Mandatory purity certification specifically for gold (and increasingly silver) jewellery, done through BIS-recognized Assaying & Hallmarking Centres.

**Q: What is an HUID?**
A unique Hallmark Unique ID assigned to each piece of hallmarked jewellery, verifiable through the BIS Care app or portal — this is the kind of consumer-facing question capability #5 targets.

**Q: Why does the assistant need to cite sources instead of just answering directly?**
Because getting a certification requirement or an IS code wrong has real regulatory/financial consequences for the user — citation lets them verify the answer against the actual BIS document rather than trusting the bot blindly.

**Q: How do you keep the assistant from hallucinating?**
RAG (retrieve-then-generate): the LLM is instructed to answer only from retrieved context and to say "not found in available sources" rather than guess when nothing relevant is retrieved.

**Q: How does this scale beyond the demo?**
The knowledge base is corpus-driven — adding a new standard or scheme document is a re-ingestion step, not a code change. The same pattern extends to any other BIS service area (training, Standards Clubs, laboratory recognition) by adding more source documents.

**Q: What about outdated standards or scheme changes?**
A periodic re-ingestion pipeline (Day-1 ingestion step, re-run on a schedule) keeps the vector DB in sync with the latest published documents; each chunk carries a source-date so the assistant can flag or deprioritize stale content.

---

## Risk Mitigation

| Risk                                              | Mitigation                                                                                                          |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| BIS source documents are hard to scrape/structure | Start with a curated subset (top 50–100 standards/schemes covering common categories) rather than the full catalog |
| LLM hallucinates despite RAG                      | Strict "answer only from context" system prompt + a "not found" fallback + always show citations so it's checkable  |
| No internet at venue for hosted LLM               | Have an offline path ready (Ollama + a 7B model) as backup, same pattern as the offline-tool build                  |
| Multilingual quality is weak                      | Treat multilingual as P1 — get English rock-solid on Day 2 before touching translation                             |
| Retrieval misses relevant chunks                  | Tune chunk size/overlap early on Day 1 against a handful of known-answer test queries                               |

---

## Single Message to Remember

> The judges want to see one thing: ask it any real BIS question — a standard, a certification scheme, a hallmarking rule, a lab near you — and get back a correct, plain-language answer **with a citation you could actually go check**. Everything else (multilingual, more schemes, more docs) is polish on top of that core loop.
