import { useState } from 'react';

export default function Citations({ citations }) {
  const [expanded, setExpanded] = useState(false);

  if (!citations || citations.length === 0) return null;

  return (
    <div className="citations-section">
      <button className="citations-toggle" onClick={() => setExpanded(!expanded)}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" /><polyline points="14 2 14 8 20 8" />
        </svg>
        {citations.length} Source{citations.length > 1 ? 's' : ''} Referenced
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
          style={{ transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 150ms ease' }}>
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </button>

      {expanded && (
        <div className="citations-list">
          {citations.map((c, i) => (
            <div key={i} className="citation-card">
              <svg className="citation-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
              <div>
                <div className="citation-name">{c.document_name}</div>
                {c.clause && <div className="citation-clause">Clause: {c.clause}</div>}
                {c.url && (
                  <a href={c.url} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.75rem', color: 'var(--color-primary-light)' }}>
                    View Source ↗
                  </a>
                )}
              </div>
              {c.relevance_score != null && (
                <span className="citation-score">{Math.round(c.relevance_score * 100)}% match</span>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
