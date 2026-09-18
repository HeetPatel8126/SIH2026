"""
BIS AI Assistant — Chat Router with Streaming, Multi-Turn Memory & Thinking Events

Endpoints:
    POST /chat        — One-shot conversational Q&A endpoint
    POST /chat/stream — Real-time Server-Sent Events (SSE) streaming endpoint
                        with "Thinking...", token-by-token generation, and live citations.

Features:
    - Multi-turn conversation memory via session store
    - Multi-category query routing for cross-domain questions
    - Citation faithfulness verification against retrieved chunks
    - Structured retrieval and LLM latency logging
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from datetime import datetime, timezone
from typing import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.models.schemas import ChatRequest, ChatResponse
from backend.services.citation import extract_from_chunks, merge_citations, parse_inline_citations
from backend.services.language_detect import detect_language
from backend.services.llm_wrapper import call_llm, stream_llm
from backend.services.prompt_builder import build_prompt
from backend.services.query_router import classify_query, classify_query_multi
from backend.services.retriever import retrieve
from backend.services.session_store import get_history, add_turn

logger = logging.getLogger("bis_assistant.router.chat")

router = APIRouter(tags=["Chat"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _retrieve_multi_category(query: str, categories, top_k: int = 5) -> list[dict]:
    """
    Retrieve chunks across multiple categories and merge, deduplicated by chunk text.
    """
    all_chunks: list[dict] = []
    seen_texts: set[str] = set()

    for cat in categories:
        chunks = await retrieve(query=query, category=cat, top_k=top_k)
        for chunk in chunks:
            text_key = chunk.get("text", "")[:100]
            if text_key not in seen_texts:
                seen_texts.add(text_key)
                all_chunks.append(chunk)

    # Re-sort by score descending and trim to top_k
    all_chunks.sort(key=lambda c: c.get("score", 0), reverse=True)
    return all_chunks[:top_k]


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main conversational endpoint — one-shot full RAG pipeline.
    Supports multi-turn memory and multi-category retrieval.
    """
    start = time.time()
    session_id = request.session_id or str(uuid.uuid4())

    logger.info("Chat request — session=%s query=%r", session_id, request.query[:80])

    # Step 1: Language detection
    detected_lang = request.language or "en"
    if detected_lang == "en":
        auto_lang = detect_language(request.query)
        if auto_lang != "en":
            detected_lang = auto_lang

    # Step 2: Query routing (multi-category)
    categories = classify_query_multi(request.query)
    query_category = categories[0]  # primary category for response

    # Step 3: Retrieve relevant chunks (across multiple categories if needed)
    retrieval_start = time.time()
    if len(categories) > 1:
        retrieved_chunks = await _retrieve_multi_category(request.query, categories)
    else:
        retrieved_chunks = await retrieve(query=request.query, category=query_category)
    retrieval_ms = round((time.time() - retrieval_start) * 1000, 1)

    # Step 4: Get conversation history
    history = get_history(session_id)

    # Step 5: Build prompt (with history)
    prompt = build_prompt(
        query=request.query,
        chunks=retrieved_chunks,
        category=query_category,
        language=detected_lang,
        history=history,
    )

    # Step 6: Call LLM
    llm_start = time.time()
    llm_answer = await call_llm(prompt)
    llm_ms = round((time.time() - llm_start) * 1000, 1)

    # Step 7: Extract and merge citations (with faithfulness check)
    chunk_citations = extract_from_chunks(retrieved_chunks)
    inline_citations = parse_inline_citations(llm_answer)
    citations = merge_citations(chunk_citations, inline_citations, retrieved_chunks=retrieved_chunks)

    # Step 8: Save turn to session store
    add_turn(session_id, request.query, llm_answer)

    processing_time = (time.time() - start) * 1000

    # Structured logging
    logger.info(
        "Chat complete — session=%s category=%s categories=%s "
        "chunks=%d top_score=%.3f retrieval_ms=%.1f llm_ms=%.1f total_ms=%.1f",
        session_id[:8], query_category.value, [c.value for c in categories],
        len(retrieved_chunks),
        retrieved_chunks[0]["score"] if retrieved_chunks else 0.0,
        retrieval_ms, llm_ms, processing_time,
    )

    return ChatResponse(
        answer=llm_answer,
        citations=citations,
        query_category=query_category,
        session_id=session_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        processing_time_ms=round(processing_time, 2),
    )


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Real-time Server-Sent Events (SSE) streaming endpoint.
    Emits thought steps, live tokens, citations, and completion stats.
    Supports multi-turn memory and multi-category retrieval.
    """
    async def event_generator() -> AsyncGenerator[str, None]:
        start = time.time()
        session_id = request.session_id or str(uuid.uuid4())

        def sse(event_type: str, data: dict) -> str:
            return f"event: {event_type}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"

        # 1. Start thinking & language check
        yield sse("thought", {
            "step": "language",
            "message": "Analyzing language & query parameters..."
        })

        detected_lang = request.language or "en"
        if detected_lang == "en":
            auto_lang = detect_language(request.query)
            if auto_lang != "en":
                detected_lang = auto_lang

        # 2. Query classification (multi-category) & retrieval
        categories = classify_query_multi(request.query)
        query_category = categories[0]

        retrieval_start = time.time()
        if len(categories) > 1:
            retrieved_chunks = await _retrieve_multi_category(request.query, categories)
        else:
            retrieved_chunks = await retrieve(
                query=request.query,
                category=query_category,
            )
        retrieval_ms = round((time.time() - retrieval_start) * 1000, 1)
        sources_found = list({c["metadata"].get("document", "IS Standard") for c in retrieved_chunks})

        # 3. Get conversation history & assemble prompt
        history = get_history(session_id)
        prompt = build_prompt(
            query=request.query,
            chunks=retrieved_chunks,
            category=query_category,
            language=detected_lang,
            history=history,
        )

        # 4. Stream LLM tokens — parse authentic AI <think>...</think> in real time
        llm_start = time.time()
        think_start_time = time.time()
        in_thinking = False
        has_thought_ended = False
        buffer = ""
        full_thought_parts = []
        full_answer_parts = []
        token_count = 0

        async for raw_token in stream_llm(prompt):
            token_count += 1
            buffer += raw_token

            # Check if thinking hasn't started yet
            if not in_thinking and not has_thought_ended:
                if "<think>" in buffer:
                    in_thinking = True
                    parts = buffer.split("<think>", 1)
                    before = parts[0].strip()
                    buffer = parts[1]
                    if before:
                        yield sse("token", {"token": before})
                        full_answer_parts.append(before)
                    think_start_time = time.time()
                else:
                    stripped = buffer.lstrip()
                    if "<think>".startswith(stripped):
                        # Potential start of <think> tag, wait for remaining tokens
                        continue
                    elif len(stripped) >= 15 or ("\n" in stripped and not stripped.startswith("<")):
                        # Model did not start with <think> tag — stream directly as answer
                        has_thought_ended = True
                        yield sse("thought_end", {
                            "thought_time_ms": round((time.time() - think_start_time) * 1000, 1),
                            "category": query_category.value,
                            "sources": sources_found,
                            "summary": f"Retrieved {len(retrieved_chunks)} relevant standard clauses ({', '.join(sources_found[:3])}).",
                            "chunks_count": len(retrieved_chunks),
                        })
                        yield sse("token", {"token": buffer})
                        full_answer_parts.append(buffer)
                        buffer = ""
                        continue

            # In thinking mode: stream AI thoughts in real-time
            if in_thinking:
                if "</think>" in buffer:
                    parts = buffer.split("</think>", 1)
                    thought_part = parts[0]
                    answer_part = parts[1]

                    if thought_part:
                        full_thought_parts.append(thought_part)
                        yield sse("thought_token", {"token": thought_part})

                    in_thinking = False
                    has_thought_ended = True
                    thought_time_ms = round((time.time() - think_start_time) * 1000, 1)

                    yield sse("thought_end", {
                        "thought_time_ms": thought_time_ms,
                        "category": query_category.value,
                        "sources": sources_found,
                        "summary": f"Retrieved {len(retrieved_chunks)} relevant standard clauses ({', '.join(sources_found[:3])}) in {retrieval_ms}ms. Formulated grounded response.",
                        "chunks_count": len(retrieved_chunks),
                    })

                    buffer = answer_part
                    if buffer:
                        yield sse("token", {"token": buffer})
                        full_answer_parts.append(buffer)
                        buffer = ""
                else:
                    # Protect against emitting partial </think> tag
                    closing_tag = "</think>"
                    keep_len = 0
                    for i in range(1, len(closing_tag)):
                        if buffer.endswith(closing_tag[:i]):
                            keep_len = i
                            break

                    if keep_len > 0:
                        to_emit = buffer[:-keep_len]
                        buffer = buffer[-keep_len:]
                    else:
                        to_emit = buffer
                        buffer = ""

                    if to_emit:
                        full_thought_parts.append(to_emit)
                        yield sse("thought_token", {"token": to_emit})

            elif has_thought_ended:
                if "<think>" in buffer and not in_thinking:
                    in_thinking = True
                    has_thought_ended = False
                    parts = buffer.split("<think>", 1)
                    before = parts[0]
                    buffer = parts[1]
                    if before:
                        yield sse("token", {"token": before})
                        full_answer_parts.append(before)
                    think_start_time = time.time()
                    continue
                if buffer:
                    yield sse("token", {"token": buffer})
                    full_answer_parts.append(buffer)
                    buffer = ""

        # Flush any remaining buffer
        if buffer:
            if in_thinking:
                full_thought_parts.append(buffer)
                yield sse("thought_token", {"token": buffer})
                thought_time_ms = round((time.time() - think_start_time) * 1000, 1)
                yield sse("thought_end", {
                    "thought_time_ms": thought_time_ms,
                    "category": query_category.value,
                    "sources": sources_found,
                    "summary": f"Analyzed {len(retrieved_chunks)} standard clauses.",
                    "chunks_count": len(retrieved_chunks),
                })
        # If LLM failed to stream any tokens, emit an error explanation
        if not full_answer_parts:
            if in_thinking or not has_thought_ended:
                yield sse("thought_end", {
                    "thought_time_ms": round((time.time() - think_start_time) * 1000, 1),
                    "category": query_category.value,
                    "sources": sources_found,
                    "summary": "LLM generation encountered an error.",
                    "chunks_count": len(retrieved_chunks),
                })
            err_msg = (
                "⚠️ **LLM Generation Error**: The model did not produce a response. "
                "Please verify that your configured LLM provider and model name in `.env` "
                "are valid and running."
            )
            yield sse("token", {"token": err_msg})
            full_answer_parts.append(err_msg)

        llm_ms = round((time.time() - llm_start) * 1000, 1)
        full_answer = "".join(full_answer_parts)

        # 5. Save turn to session store
        add_turn(session_id, request.query, full_answer)

        # 6. Extract citations (with faithfulness check)
        chunk_citations = extract_from_chunks(retrieved_chunks)
        inline_citations = parse_inline_citations(full_answer)
        citations = merge_citations(chunk_citations, inline_citations, retrieved_chunks=retrieved_chunks)
        citations_data = [c.model_dump() for c in citations]

        yield sse("citations", {"citations": citations_data})

        # 7. Done event
        total_time_ms = round((time.time() - start) * 1000, 1)
        yield sse("done", {
            "session_id": session_id,
            "total_tokens": token_count,
            "processing_time_ms": total_time_ms,
            "query_category": query_category.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        # Structured logging
        logger.info(
            "Chat stream complete — session=%s category=%s categories=%s "
            "chunks=%d retrieval_ms=%.1f llm_ms=%.1f total_ms=%.1f tokens=%d",
            session_id[:8], query_category.value, [c.value for c in categories],
            len(retrieved_chunks), retrieval_ms, llm_ms, total_time_ms, token_count,
        )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
