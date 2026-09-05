"""
BIS AI Assistant — Multi-Provider LLM Client with Streaming & Hybrid Fallback

Supports:
  - Ollama (Local offline inference with qwen2.5:7b / llama3.2:3b)
  - Groq (Ultra-fast cloud inference with llama-3.3-70b-versatile)
  - OpenAI / Together / OpenRouter (OpenAI-compatible APIs)
  - Google Gemini (via OpenAI-compatible endpoint or native)
  - Anthropic (Claude API)

Features:
  - Both one-shot `call_llm()` and real-time token generator `stream_llm()`
  - Hybrid Fallback Architecture: if primary cloud API fails, automatically falls back to local Ollama.
"""

from __future__ import annotations

import json
import logging
from typing import AsyncGenerator, Optional

import httpx

from backend.config import settings

logger = logging.getLogger("bis_assistant.llm_wrapper")

# Shared async client — reused across calls (connection pooling)
_client: Optional[httpx.AsyncClient] = None


def _get_client() -> httpx.AsyncClient:
    """Lazy-initialize the shared httpx async client."""
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=httpx.Timeout(90.0, connect=10.0))
    return _client


# ---------------------------------------------------------------------------
# One-shot Provider implementations
# ---------------------------------------------------------------------------

async def _call_ollama(prompt: str, is_fallback: bool = False) -> str:
    """Call a local Ollama instance (one-shot)."""
    client = _get_client()
    base_url = settings.fallback_llm_base_url if is_fallback else settings.llm_base_url
    model = settings.fallback_llm_model if is_fallback else settings.llm_model
    url = f"{base_url.rstrip('/')}/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": settings.llm_temperature,
            "num_predict": settings.llm_max_tokens,
        },
    }

    logger.debug("Ollama request — model=%s, url=%s (fallback=%s)", model, url, is_fallback)
    response = await client.post(url, json=payload)
    response.raise_for_status()

    data = response.json()
    return data.get("response", "").strip()


async def _call_openai_compatible(
    prompt: str,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    is_fallback: bool = False,
) -> str:
    """Call any OpenAI-compatible chat completion endpoint."""
    client = _get_client()
    raw_base = base_url or (settings.fallback_llm_base_url if is_fallback else settings.llm_base_url)
    key = api_key or (settings.fallback_llm_api_key if is_fallback else settings.llm_api_key)
    target_model = model or (settings.fallback_llm_model if is_fallback else settings.llm_model)

    clean_base = raw_base.rstrip("/")
    if clean_base.endswith("/chat/completions"):
        url = clean_base
    elif clean_base.endswith("/v1"):
        url = f"{clean_base}/chat/completions"
    else:
        url = f"{clean_base}/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": target_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": settings.llm_temperature,
        "max_tokens": settings.llm_max_tokens,
    }

    logger.debug("OpenAI-compatible request — model=%s, url=%s", target_model, url)
    response = await client.post(url, json=payload, headers=headers)
    response.raise_for_status()

    data = response.json()
    choices = data.get("choices", [])
    if not choices:
        raise ValueError("No choices returned from OpenAI-compatible API")

    msg = choices[0].get("message", {})
    content = msg.get("content", "").strip()
    reasoning = msg.get("reasoning", "").strip()
    if reasoning and not content.startswith("<think>"):
        content = f"<think>\n{reasoning}\n</think>\n\n{content}"

    return content


async def _call_groq(prompt: str, is_fallback: bool = False) -> str:
    base_url = settings.fallback_llm_base_url if is_fallback else settings.llm_base_url
    if "localhost" in base_url or "127.0.0.1" in base_url:
        base_url = "https://api.groq.com/openai"
    raw_model = settings.fallback_llm_model if is_fallback else settings.llm_model
    api_key = settings.fallback_llm_api_key if is_fallback else settings.llm_api_key
    if not raw_model or "llama" in raw_model.lower() or ":" in raw_model:
        # Groq flagship open source reasoning model (120B)
        model = "openai/gpt-oss-120b"
    else:
        model = raw_model

    return await _call_openai_compatible(
        prompt=prompt,
        base_url=base_url,
        api_key=api_key,
        model=model,
        is_fallback=is_fallback,
    )


async def _call_gemini(prompt: str, is_fallback: bool = False) -> str:
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai"
    model = settings.llm_model
    if not model or "llama" in model.lower() or "qwen" in model.lower():
        model = "gemini-2.0-flash"

    return await _call_openai_compatible(
        prompt=prompt,
        base_url=base_url,
        api_key=settings.llm_api_key,
        model=model,
        is_fallback=is_fallback,
    )


async def _call_anthropic(prompt: str, is_fallback: bool = False) -> str:
    client = _get_client()
    url = "https://api.anthropic.com/v1/messages"
    key = settings.fallback_llm_api_key if is_fallback else settings.llm_api_key
    model = settings.fallback_llm_model if is_fallback else settings.llm_model

    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model or "claude-3-5-sonnet-20241022",
        "max_tokens": settings.llm_max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = await client.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    content_blocks = data.get("content", [])
    return "".join(b.get("text", "") for b in content_blocks if b.get("type") == "text").strip()


# ---------------------------------------------------------------------------
# Real-Time Streaming Provider implementations
# ---------------------------------------------------------------------------

async def _stream_ollama(prompt: str, is_fallback: bool = False) -> AsyncGenerator[str, None]:
    """Stream real-time tokens from Ollama."""
    client = _get_client()
    base_url = settings.fallback_llm_base_url if is_fallback else settings.llm_base_url
    model = settings.fallback_llm_model if is_fallback else settings.llm_model
    url = f"{base_url.rstrip('/')}/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": settings.llm_temperature,
            "num_predict": settings.llm_max_tokens,
        },
    }

    logger.debug("Streaming Ollama — model=%s, url=%s", model, url)
    async with client.stream("POST", url, json=payload) as response:
        response.raise_for_status()
        async for line in response.aiter_lines():
            line = line.strip()
            if not line:
                continue
            try:
                chunk = json.loads(line)
                token = chunk.get("response", "")
                if token:
                    yield token
            except Exception:
                continue


async def _stream_openai_compatible(
    prompt: str,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    is_fallback: bool = False,
) -> AsyncGenerator[str, None]:
    """Stream real-time tokens from an OpenAI-compatible API."""
    client = _get_client()
    raw_base = base_url or (settings.fallback_llm_base_url if is_fallback else settings.llm_base_url)
    key = api_key or (settings.fallback_llm_api_key if is_fallback else settings.llm_api_key)
    target_model = model or (settings.fallback_llm_model if is_fallback else settings.llm_model)

    clean_base = raw_base.rstrip("/")
    if clean_base.endswith("/chat/completions"):
        url = clean_base
    elif clean_base.endswith("/v1"):
        url = f"{clean_base}/chat/completions"
    else:
        url = f"{clean_base}/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": target_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": settings.llm_temperature,
        "max_tokens": settings.llm_max_tokens,
        "stream": True,
    }

    logger.debug("Streaming OpenAI-compatible — model=%s, url=%s", target_model, url)
    in_reasoning = False
    async with client.stream("POST", url, json=payload, headers=headers) as response:
        response.raise_for_status()
        async for line in response.aiter_lines():
            line = line.strip()
            if not line or line.startswith(":"):
                continue
            if line.startswith("data: "):
                data_str = line[6:].strip()
                if data_str == "[DONE]":
                    break
                try:
                    data = json.loads(data_str)
                    delta = data.get("choices", [{}])[0].get("delta", {})
                    reasoning_token = delta.get("reasoning", "")
                    content_token = delta.get("content", "")

                    if reasoning_token:
                        if not in_reasoning:
                            in_reasoning = True
                            yield "<think>\n"
                        yield reasoning_token
                    elif content_token:
                        if in_reasoning:
                            in_reasoning = False
                            yield "\n</think>\n\n"
                        yield content_token
                except Exception:
                    continue
        if in_reasoning:
            yield "\n</think>\n\n"


async def _stream_groq(prompt: str, is_fallback: bool = False) -> AsyncGenerator[str, None]:
    base_url = settings.fallback_llm_base_url if is_fallback else settings.llm_base_url
    if "localhost" in base_url or "127.0.0.1" in base_url:
        base_url = "https://api.groq.com/openai"
    raw_model = settings.fallback_llm_model if is_fallback else settings.llm_model
    api_key = settings.fallback_llm_api_key if is_fallback else settings.llm_api_key
    if not raw_model or "llama" in raw_model.lower() or ":" in raw_model:
        # Groq flagship open source reasoning model (120B)
        model = "openai/gpt-oss-120b"
    else:
        model = raw_model

    async for token in _stream_openai_compatible(
        prompt=prompt,
        base_url=base_url,
        api_key=api_key,
        model=model,
        is_fallback=is_fallback,
    ):
        yield token


async def _stream_gemini(prompt: str, is_fallback: bool = False) -> AsyncGenerator[str, None]:
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai"
    model = settings.llm_model
    if not model or "llama" in model.lower() or "qwen" in model.lower():
        model = "gemini-2.0-flash"

    async for token in _stream_openai_compatible(
        prompt=prompt,
        base_url=base_url,
        api_key=settings.llm_api_key,
        model=model,
        is_fallback=is_fallback,
    ):
        yield token


async def _stream_anthropic(prompt: str, is_fallback: bool = False) -> AsyncGenerator[str, None]:
    """Stream real-time tokens from the Anthropic Messages API."""
    client = _get_client()
    url = "https://api.anthropic.com/v1/messages"
    key = settings.fallback_llm_api_key if is_fallback else settings.llm_api_key
    model = settings.fallback_llm_model if is_fallback else settings.llm_model

    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model or "claude-3-5-sonnet-20241022",
        "max_tokens": settings.llm_max_tokens,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }

    logger.debug("Streaming Anthropic — model=%s", model)
    async with client.stream("POST", url, json=payload, headers=headers) as response:
        response.raise_for_status()
        async for line in response.aiter_lines():
            line = line.strip()
            if not line or line.startswith(":"):
                continue
            if line.startswith("data: "):
                data_str = line[6:].strip()
                if data_str == "[DONE]":
                    break
                try:
                    data = json.loads(data_str)
                    event_type = data.get("type", "")
                    if event_type == "content_block_delta":
                        delta = data.get("delta", {})
                        token = delta.get("text", "")
                        if token:
                            yield token
                except Exception:
                    continue


_PROVIDERS = {
    "ollama": _call_ollama,
    "openai": _call_openai_compatible,
    "groq": _call_groq,
    "gemini": _call_gemini,
    "together": _call_openai_compatible,
    "anthropic": _call_anthropic,
}

_STREAM_PROVIDERS = {
    "ollama": _stream_ollama,
    "openai": _stream_openai_compatible,
    "groq": _stream_groq,
    "gemini": _stream_gemini,
    "together": _stream_openai_compatible,
    "anthropic": _stream_anthropic,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_same_provider_config() -> bool:
    """Check if primary and fallback are effectively the same endpoint."""
    if settings.llm_provider.lower() != settings.fallback_llm_provider.lower():
        return False
    # Same provider type — also check if base URLs match
    primary_url = settings.llm_base_url.rstrip("/").lower()
    fallback_url = settings.fallback_llm_base_url.rstrip("/").lower()
    return primary_url == fallback_url


# ---------------------------------------------------------------------------
# Public APIs
# ---------------------------------------------------------------------------

async def call_llm(prompt: str, retries: int = 1) -> str:
    """Call configured LLM (one-shot) with automatic hybrid fallback."""
    provider = settings.llm_provider.lower()
    call_fn = _PROVIDERS.get(provider)

    if call_fn is None:
        supported = ", ".join(_PROVIDERS.keys())
        return f"\u26a0\ufe0f Unknown LLM provider: `{provider}`. Supported: {supported}."

    last_error = None
    for attempt in range(1 + retries):
        try:
            return await call_fn(prompt)
        except Exception as e:
            last_error = e
            logger.warning("Primary LLM call failed (attempt %d/%d): %s", attempt + 1, 1 + retries, e)

    # Hybrid Fallback — skip if primary and fallback point to same endpoint
    can_fallback = (
        settings.fallback_enabled
        and not _is_same_provider_config()
    )
    if can_fallback:
        logger.warning(
            "Primary provider '%s' failed. Executing fallback to '%s' (%s)...",
            provider, settings.fallback_llm_provider, settings.fallback_llm_model,
        )
        try:
            fallback_fn = _PROVIDERS.get(settings.fallback_llm_provider)
            if fallback_fn:
                return await fallback_fn(prompt, is_fallback=True)
        except Exception as fb_err:
            logger.error("Hybrid fallback also failed: %s", fb_err)
    elif settings.fallback_enabled and _is_same_provider_config():
        logger.warning(
            "Skipping fallback — primary and fallback are the same provider (%s @ %s)",
            provider, settings.llm_base_url,
        )

    return f"\u26a0\ufe0f **LLM Generation Error**: {last_error}"


async def stream_llm(prompt: str) -> AsyncGenerator[str, None]:
    """
    Stream real-time tokens from the configured LLM.
    If the primary cloud provider fails, seamlessly falls back to streaming
    from the fallback provider (skips if same provider/endpoint as primary).
    """
    provider = settings.llm_provider.lower()
    stream_fn = _STREAM_PROVIDERS.get(provider)

    tokens_yielded = 0
    try:
        if stream_fn:
            async for token in stream_fn(prompt):
                tokens_yielded += 1
                yield token
            return
    except Exception as e:
        logger.warning("Streaming with '%s' encountered error: %s", provider, e)

    # If primary failed to yield or raised an error, engage hybrid fallback
    can_fallback = (
        tokens_yielded == 0
        and settings.fallback_enabled
        and not _is_same_provider_config()
    )
    if can_fallback:
        logger.warning(
            "Engaging hybrid fallback stream with '%s' (%s)...",
            settings.fallback_llm_provider, settings.fallback_llm_model
        )
        fallback_fn = _STREAM_PROVIDERS.get(settings.fallback_llm_provider, _stream_ollama)
        try:
            async for token in fallback_fn(prompt, is_fallback=True):
                yield token
        except Exception as fb_err:
            logger.error("Hybrid fallback streaming also failed: %s", fb_err)
            yield f"\n\n\u26a0\ufe0f **Streaming error**: Could not reach fallback ({fb_err})"


async def shutdown_client():
    """Close the shared HTTP client."""
    global _client
    if _client and not _client.is_closed:
        await _client.aclose()
        _client = None
