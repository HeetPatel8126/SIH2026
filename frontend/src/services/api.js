/**
 * BIS AI Assistant — Centralized API Service Layer
 *
 * All backend communication goes through this module.
 * Supports both one-shot request() and real-time streaming streamChat().
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

/* ------------------------------------------------------------------ */
/*  Generic fetch wrapper                                              */
/* ------------------------------------------------------------------ */

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  };

  const response = await fetch(url, config);

  if (!response.ok) {
    let errorDetail = `HTTP ${response.status}`;
    try {
      const body = await response.json();
      errorDetail = body.detail || JSON.stringify(body);
    } catch {
      /* ignore parse errors */
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

/* ------------------------------------------------------------------ */
/*  GET /health                                                        */
/* ------------------------------------------------------------------ */

export function fetchHealth() {
  return request('/health');
}

/* ------------------------------------------------------------------ */
/*  POST /chat (one-shot fallback)                                     */
/* ------------------------------------------------------------------ */

export function sendChat({ query, language = 'en', session_id = null }) {
  const body = { query, language };
  if (session_id) body.session_id = session_id;

  return request('/chat', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

/* ------------------------------------------------------------------ */
/*  POST /chat/stream (SSE Real-time Streaming & Thinking)            */
/* ------------------------------------------------------------------ */

export async function streamChat({
  query,
  language = 'en',
  session_id = null,
  onThought = () => {},
  onThoughtToken = () => {},
  onThoughtEnd = () => {},
  onToken = () => {},
  onCitations = () => {},
  onDone = () => {},
  onError = () => {},
  signal = null,
}) {
  const url = `${API_BASE}/chat/stream`;
  const body = { query, language };
  if (session_id) body.session_id = session_id;

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal,
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`Stream request failed (${response.status}): ${errText}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n\n');
      buffer = lines.pop(); // Keep unfinished chunk in buffer

      for (const block of lines) {
        if (!block.trim()) continue;

        let eventType = 'message';
        let eventData = '';

        for (const line of block.split('\n')) {
          if (line.startsWith('event: ')) {
            eventType = line.slice(7).trim();
          } else if (line.startsWith('data: ')) {
            eventData = line.slice(6).trim();
          }
        }

        if (!eventData) continue;

        try {
          const parsed = JSON.parse(eventData);

          if (eventType === 'thought_token') {
            onThoughtToken(parsed.token);
          } else if (eventType === 'thought') {
            onThought(parsed);
          } else if (eventType === 'thought_end') {
            onThoughtEnd(parsed);
          } else if (eventType === 'token') {
            onToken(parsed.token);
          } else if (eventType === 'citations') {
            onCitations(parsed.citations);
          } else if (eventType === 'done') {
            onDone(parsed);
          }
        } catch {
          // Ignore JSON parse chunk errors
        }
      }
    }
  } catch (err) {
    if (err.name === 'AbortError') {
      console.debug('Stream aborted by user');
    } else {
      onError(err);
    }
  }
}

/* ------------------------------------------------------------------ */
/*  POST /search-standards                                             */
/* ------------------------------------------------------------------ */

export function searchStandards({ query, sector = null, top_k = 10 }) {
  const body = { query, top_k };
  if (sector) body.sector = sector;

  return request('/search-standards', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

/* ------------------------------------------------------------------ */
/*  POST /certification-guide                                          */
/* ------------------------------------------------------------------ */

export function getCertificationGuide({ scheme = null, product = null }) {
  const body = {};
  if (scheme) body.scheme = scheme;
  if (product) body.product = product;

  return request('/certification-guide', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}
