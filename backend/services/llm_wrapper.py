"""
BIS AI Assistant — LLM Call Wrapper

Multi-provider async LLM client supporting Ollama, OpenAI-compatible APIs,
and Anthropic. Provider is selected via the LLM_PROVIDER env variable.
"""

from __future__ import annotations

import json
import logging
from typing import Optional

import httpx

from backend.config import settings

logger = logging.getLogger("bis_assistant.llm_wrapper")

# Shared async client — reused across calls (connection pooling)
_client: Optional[httpx.AsyncClient] = None


def _get_client() -> httpx.AsyncClient:
    """Lazy-initialize the shared httpx async client."""
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=10.0))
    return _client


# ---------------------------------------------------------------------------
# Provider-specific call implementations
# ---------------------------------------------------------------------------

async def _call_ollama(prompt: str) -> str:
    """
    Call a local Ollama instance.

    Endpoint: POST {base_url}/api/generate
    Docs: https://github.com/ollama/ollama/blob/main/docs/api.md
    """
    client = _get_client()
    url = f"{settings.llm_base_url}/api/generate"

    payload = {
        "model": settings.llm_model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": settings.llm_temperature,
            "num_predict": settings.llm_max_tokens,
        },
    }

    logger.debug("Ollama request — model=%s, url=%s", settings.llm_model, url)
    response = await client.post(url, json=payload)
    response.raise_for_status()

    data = response.json()
    return data.get("response", "").strip()


async def _call_openai(prompt: str) -> str:
    """
    Call an OpenAI-compatible API (works for OpenAI, Groq, Together, etc.).

    Endpoint: POST {base_url}/v1/chat/completions
    """
    client = _get_client()

    # For standard OpenAI, base_url is "https://api.openai.com"
    # For Groq, it's "https://api.groq.com/openai"
    url = f"{settings.llm_base_url}/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.llm_model,
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "temperature": settings.llm_temperature,
        "max_tokens": settings.llm_max_tokens,
    }

    logger.debug("OpenAI-compatible request — model=%s, url=%s", settings.llm_model, url)
    response = await client.post(url, json=payload, headers=headers)
    response.raise_for_status()

    data = response.json()
    choices = data.get("choices", [])
    if not choices:
        raise ValueError("No choices returned from OpenAI-compatible API")

    return choices[0].get("message", {}).get("content", "").strip()


async def _call_anthropic(prompt: str) -> str:
    """
    Call the Anthropic Messages API.

    Endpoint: POST https://api.anthropic.com/v1/messages
    """
    client = _get_client()
    url = "https://api.anthropic.com/v1/messages"

    headers = {
        "x-api-key": settings.llm_api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.llm_model,
        "max_tokens": settings.llm_max_tokens,
        "messages": [
            {"role": "user", "content": prompt},
        ],
    }

    logger.debug("Anthropic request — model=%s", settings.llm_model)
    response = await client.post(url, json=payload, headers=headers)
    response.raise_for_status()

    data = response.json()
    content_blocks = data.get("content", [])
    if not content_blocks:
        raise ValueError("No content returned from Anthropic API")

    # Concatenate all text blocks
    return "".join(
        block.get("text", "") for block in content_blocks if block.get("type") == "text"
    ).strip()


# ---------------------------------------------------------------------------
# Provider dispatch map
# ---------------------------------------------------------------------------

_PROVIDERS = {
    "ollama": _call_ollama,
    "openai": _call_openai,
    "groq": _call_openai,       # Groq uses OpenAI-compatible API
    "together": _call_openai,   # Together uses OpenAI-compatible API
    "anthropic": _call_anthropic,
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def call_llm(prompt: str, retries: int = 1) -> str:
    """
    Call the configured LLM provider and return the generated text.

    Handles retries on failure. Falls back to a descriptive error message
    rather than crashing.

    Args:
        prompt: The fully assembled prompt string.
        retries: Number of retry attempts on failure (default 1).

    Returns:
        The LLM's generated text response.
    """
    provider = settings.llm_provider.lower()
    call_fn = _PROVIDERS.get(provider)

    if call_fn is None:
        supported = ", ".join(_PROVIDERS.keys())
        logger.error("Unknown LLM provider: %s (supported: %s)", provider, supported)
        return (
            f"⚠️ Unknown LLM provider: `{provider}`. "
            f"Supported providers: {supported}. "
            f"Set LLM_PROVIDER in your .env file."
        )

    last_error: Exception | None = None

    for attempt in range(1 + retries):
        try:
            result = await call_fn(prompt)
            if attempt > 0:
                logger.info("LLM call succeeded on retry %d", attempt)
            return result

        except httpx.HTTPStatusError as e:
            last_error = e
            logger.warning(
                "LLM HTTP error (attempt %d/%d): %s %s",
                attempt + 1, 1 + retries, e.response.status_code, e.response.text[:200],
            )
        except httpx.ConnectError as e:
            last_error = e
            logger.warning(
                "LLM connection error (attempt %d/%d): %s",
                attempt + 1, 1 + retries, str(e),
            )
        except Exception as e:
            last_error = e
            logger.warning(
                "LLM call failed (attempt %d/%d): %s",
                attempt + 1, 1 + retries, str(e),
            )

    # All attempts failed
    error_msg = str(last_error) if last_error else "Unknown error"
    logger.error("LLM call failed after %d attempts: %s", 1 + retries, error_msg)

    return (
        f"⚠️ **LLM call failed** — could not reach the {provider} API.\n\n"
        f"Error: {error_msg}\n\n"
        f"Please check:\n"
        f"- Is the LLM server running? (e.g., `ollama serve` for Ollama)\n"
        f"- Is `LLM_BASE_URL` correct in your `.env`? (current: `{settings.llm_base_url}`)\n"
        f"- Is `LLM_API_KEY` set? (required for OpenAI/Anthropic)\n"
    )


async def shutdown_client():
    """Close the shared HTTP client. Call on app shutdown."""
    global _client
    if _client and not _client.is_closed:
        await _client.aclose()
        _client = None
