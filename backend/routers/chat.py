"""
BIS AI Assistant — Chat Router with Streaming & Thinking Events

Endpoints:
    POST /chat        — One-shot conversational Q&A endpoint
    POST /chat/stream — Real-time Server-Sent Events (SSE) streaming endpoint
                        with "Thinking...", token-by-token generation, and live citations.
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
from backend.services.query_router import classify_query
from backend.services.retriever import retrieve

logger = logging.getLogger("bis_assistant.router.chat")

router = APIRouter(tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main conversational endpoint — one-shot full RAG pipeline.
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

    # Step 2: Query routing
    query_category = classify_query(request.query)

    # Step 3: Retrieve relevant chunks
    retrieved_chunks = await retrieve(
        query=request.query,
        category=query_category,
    )

    # Step 4: Build prompt
    prompt = build_prompt(
        query=request.query,
        chunks=retrieved_chunks,
        category=query_category,
        language=detected_lang,
    )

    # Step 5: Call LLM
    llm_answer = await call_llm(prompt)

    # Step 6: Extract and merge citations
    chunk_citations = extract_from_chunks(retrieved_chunks)
    inline_citations = parse_inline_citations(llm_answer)
    citations = merge_citations(chunk_citations, inline_citations)

    processing_time = (time.time() - start) * 1000

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

        # 2. Query classification & retrieval
        query_category = classify_query(request.query)
        retrieval_start = time.time()
        retrieved_chunks = await retrieve(
            query=request.query,
            category=query_category,
        )
        retrieval_ms = round((time.time() - retrieval_start) * 1000, 1)
        sources_found = list({c["metadata"].get("document", "IS Standard") for c in retrieved_chunks})

        # 3. Assemble prompt with Chain-of-Thought instructions
        prompt = build_prompt(
            query=request.query,
            chunks=retrieved_chunks,
            category=query_category,
            language=detected_lang,
        )

        # 4. Stream LLM tokens — parse authentic AI <think>...</think> in real time
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
                    before = parts[0]
                    buffer = parts[1]
                    if before:
                        yield sse("token", {"token": before})
                        full_answer_parts.append(before)
                    think_start_time = time.time()
                elif len(buffer) >= 15 or "\n" in buffer:
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

        full_answer = "".join(full_answer_parts)

        # 5. Extract citations
        chunk_citations = extract_from_chunks(retrieved_chunks)
        inline_citations = parse_inline_citations(full_answer)
        citations = merge_citations(chunk_citations, inline_citations)
        citations_data = [c.model_dump() for c in citations]

        yield sse("citations", {"citations": citations_data})

        # 6. Done event
        total_time_ms = round((time.time() - start) * 1000, 1)
        yield sse("done", {
            "session_id": session_id,
            "total_tokens": token_count,
            "processing_time_ms": total_time_ms,
            "query_category": query_category.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
