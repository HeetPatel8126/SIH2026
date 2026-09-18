"""
BIS AI Assistant — In-Memory Session Store

Provides multi-turn conversation memory keyed by session_id.
Stores the last N turns (user question + assistant answer summary)
with automatic TTL-based expiration.

No external dependencies — uses a plain dict. For production,
swap with Redis or SQLite.
"""

from __future__ import annotations

import logging
import time
from typing import Optional

logger = logging.getLogger("bis_assistant.session_store")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MAX_HISTORY_TURNS: int = 5          # Keep last N exchanges per session
SESSION_TTL_SECONDS: float = 1800   # 30 minutes

# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------
# Structure: { session_id: { "turns": [...], "last_access": float } }
_sessions: dict[str, dict] = {}


def _evict_expired() -> None:
    """Remove sessions that haven't been accessed within TTL."""
    now = time.time()
    expired = [
        sid for sid, data in _sessions.items()
        if now - data["last_access"] > SESSION_TTL_SECONDS
    ]
    for sid in expired:
        del _sessions[sid]
    if expired:
        logger.debug("Evicted %d expired session(s)", len(expired))


def get_history(session_id: str) -> list[dict]:
    """
    Retrieve conversation history for a session.

    Returns:
        List of dicts with 'role' ('user'|'assistant') and 'content' keys.
        Empty list if session doesn't exist or has expired.
    """
    _evict_expired()

    session = _sessions.get(session_id)
    if session is None:
        return []

    session["last_access"] = time.time()
    return list(session["turns"])


def add_turn(session_id: str, user_query: str, assistant_answer: str) -> None:
    """
    Record a conversation turn (user question + assistant answer).

    The assistant answer is truncated to a summary (~500 chars) to keep
    prompt sizes manageable across many turns.

    Args:
        session_id: The session identifier.
        user_query: The user's question.
        assistant_answer: The full LLM response (will be summarized).
    """
    _evict_expired()

    # Summarize assistant answer to keep history compact
    answer_summary = assistant_answer[:500]
    if len(assistant_answer) > 500:
        answer_summary += "..."

    if session_id not in _sessions:
        _sessions[session_id] = {"turns": [], "last_access": time.time()}

    session = _sessions[session_id]
    session["last_access"] = time.time()
    session["turns"].append({"role": "user", "content": user_query})
    session["turns"].append({"role": "assistant", "content": answer_summary})

    # Trim to last MAX_HISTORY_TURNS exchanges (each exchange = 2 entries)
    max_entries = MAX_HISTORY_TURNS * 2
    if len(session["turns"]) > max_entries:
        session["turns"] = session["turns"][-max_entries:]

    logger.debug(
        "Session %s: recorded turn (%d turns stored)",
        session_id[:8], len(session["turns"]) // 2,
    )


def clear_session(session_id: str) -> None:
    """Remove a session and all its history."""
    _sessions.pop(session_id, None)
    logger.debug("Cleared session %s", session_id[:8])


def get_active_session_count() -> int:
    """Return the number of active (non-expired) sessions."""
    _evict_expired()
    return len(_sessions)
