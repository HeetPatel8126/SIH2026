import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import Citations from '../components/Citations';
import { getCertificationGuide } from '../services/api';

const SCHEMES = ['', 'ISI', 'CRS', 'FMCS', 'Hallmark', 'SchemeX', 'ECOMark'];

export default function CertificationGuidePage() {
  const [query, setQuery] = useState('');
  const [scheme, setScheme] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim() || loading) return;
    setLoading(true);
    setError(null);

    try {
      const data = await getCertificationGuide({
        query: query.trim(),
        scheme: scheme || null,
      });
      setResult(data);
    } catch (err) {
      setError(err.message || 'Request failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="page-header">
        <h2>BIS Certification Guide</h2>
        <p>Learn about certification schemes, licensing processes, and requirements</p>
      </div>

      <div className="page-content">
        <form className="cert-form" onSubmit={handleSubmit}>
          <div className="form-row">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. How do I apply for ISI Mark for my product?"
              style={{ flex: 1, padding: '8px 16px', border: '1.5px solid var(--color-border)', borderRadius: 'var(--radius-sm)', fontFamily: 'inherit', fontSize: 'var(--font-size-base)', color: 'var(--color-text)', outline: 'none' }}
              id="cert-query-input"
            />
            <select value={scheme} onChange={(e) => setScheme(e.target.value)} id="cert-scheme-select">
              <option value="">All Schemes</option>
              {SCHEMES.filter(Boolean).map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>
          <button className="btn-primary" type="submit" disabled={loading || !query.trim()} id="cert-submit-btn">
            {loading ? <span className="spinner" /> : 'Get Guidance'}
          </button>
        </form>

        {error && <div className="error-banner">⚠ {error}</div>}

        {result && (
          <div className="cert-answer">
            {result.scheme_identified && (
              <span className="cert-scheme-badge">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                {result.scheme_identified}
              </span>
            )}

            <div className="cert-text">
              <ReactMarkdown>{result.answer}</ReactMarkdown>
            </div>

            {result.steps && result.steps.length > 0 && (
              <>
                <h4 style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: 8, color: 'var(--color-primary)' }}>Process Steps</h4>
                <ol className="cert-steps">
                  {result.steps.map((step, i) => (
                    <li key={i}>{step}</li>
                  ))}
                </ol>
              </>
            )}

            <Citations citations={result.citations} />

            <div style={{ marginTop: 12, fontSize: '0.7rem', color: 'var(--color-text-muted)' }}>
              Response generated at {new Date(result.timestamp).toLocaleString()}
            </div>
          </div>
        )}

        {!result && !error && (
          <div className="empty-state">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            <p>Ask about BIS certification schemes, licensing steps, or requirements.</p>
          </div>
        )}
      </div>
    </>
  );
}
