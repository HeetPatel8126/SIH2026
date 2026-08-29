/**
 * BIS AI Assistant — Centralized API Service Layer
 *
 * All backend communication goes through this module.
 * Mirrors the exact schemas defined in backend/api.py.
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
/*  Response: { status, version, llm_provider, llm_model,             */
/*              uptime_seconds }                                       */
/* ------------------------------------------------------------------ */

export function fetchHealth() {
  return request('/health');
}

/* ------------------------------------------------------------------ */
/*  POST /chat                                                         */
/*  Request:  { query, language?, session_id? }                        */
/*  Response: { answer, citations[], query_category, session_id,       */
/*              timestamp, processing_time_ms }                        */
/*  Citation: { document_name, clause?, url?, relevance_score? }       */
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
/*  POST /search-standards                                             */
/*  Request:  { query, top_k? }                                        */
/*  Response: { results[], total_found, query, timestamp }             */
/*  StandardResult: { is_code, title, summary?, relevance_score? }     */
/* ------------------------------------------------------------------ */

export function searchStandards({ query, top_k = 5 }) {
  return request('/search-standards', {
    method: 'POST',
    body: JSON.stringify({ query, top_k }),
  });
}

/* ------------------------------------------------------------------ */
/*  POST /certification-guide                                          */
/*  Request:  { query, scheme? }                                       */
/*  Response: { answer, scheme_identified?, steps[], citations[],      */
/*              timestamp }                                            */
/* ------------------------------------------------------------------ */

export function getCertificationGuide({ query, scheme = null }) {
  const body = { query };
  if (scheme) body.scheme = scheme;

  return request('/certification-guide', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}
