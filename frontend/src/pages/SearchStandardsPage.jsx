import { useState } from 'react';
import { searchStandards } from '../services/api';

export default function SearchStandardsPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim() || loading) return;
    setLoading(true);
    setError(null);

    try {
      const data = await searchStandards({ query: query.trim(), top_k: 10 });
      setResults(data);
    } catch (err) {
      setError(err.message || 'Search failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="page-header">
        <h2>Search Indian Standards</h2>
        <p>Find standards by product name, keyword, or IS code</p>
      </div>

      <div className="page-content">
        <form className="search-form" onSubmit={handleSearch}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. packaged drinking water, IS 10500, pressure cooker…"
            id="standards-search-input"
          />
          <button className="btn-primary" type="submit" disabled={loading || !query.trim()} id="standards-search-btn">
            {loading ? <span className="spinner" /> : 'Search'}
          </button>
        </form>

        {error && <div className="error-banner">⚠ {error}</div>}

        {results && results.results.length === 0 && (
          <div className="empty-state">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <p>No standards found for &ldquo;{results.query}&rdquo;.</p>
            <p style={{ marginTop: 4 }}>The knowledge base may not be loaded yet. Try again once documents are ingested.</p>
          </div>
        )}

        {results && results.results.length > 0 && (
          <>
            <p style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)', marginBottom: 'var(--space-md)' }}>
              {results.total_found} result{results.total_found !== 1 ? 's' : ''} found
            </p>
            <div className="results-grid">
              {results.results.map((r, i) => (
                <div key={i} className="result-card">
                  <span className="is-code">{r.is_code}</span>
                  <div className="result-title">{r.title}</div>
                  {r.summary && <div className="result-summary">{r.summary}</div>}
                  {r.relevance_score != null && (
                    <div className="result-score">Relevance: {Math.round(r.relevance_score * 100)}%</div>
                  )}
                </div>
              ))}
            </div>
          </>
        )}

        {!results && !error && (
          <div className="empty-state">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <p>Enter a product, keyword, or IS code to search.</p>
          </div>
        )}
      </div>
    </>
  );
}
