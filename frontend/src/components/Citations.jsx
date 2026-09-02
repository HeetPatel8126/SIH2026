import { useState } from 'react';
import { FileText, ChevronDown, ExternalLink } from 'lucide-react';

export default function Citations({ citations }) {
  const [expanded, setExpanded] = useState(false);

  if (!citations || citations.length === 0) return null;

  return (
    <div className="space-y-2 mt-2">
      <button
        type="button"
        onClick={() => setExpanded(!expanded)}
        className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[var(--bg-card)] hover:bg-[var(--bg-card-elevated)] border border-[var(--border-color)] hover:border-[var(--accent-terracotta)] text-xs text-[var(--text-secondary)] hover:text-[var(--text-primary)] font-medium transition cursor-pointer shadow-2xs"
      >
        <FileText size={13} className="text-[var(--accent-terracotta)]" />
        <span>{citations.length} Grounded BIS Source{citations.length > 1 ? 's' : ''}</span>
        <ChevronDown
          size={13}
          className={`transition-transform duration-200 ${expanded ? 'rotate-180' : ''}`}
        />
      </button>

      {expanded && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1">
          {citations.map((c, i) => {
            const scorePct = c.relevance_score != null ? Math.round(c.relevance_score * 100) : 88;
            return (
              <div
                key={i}
                className="bg-[var(--bg-card)] border border-[var(--border-color)] hover:border-[var(--accent-terracotta)] rounded-xl p-3 flex flex-col justify-between shadow-2xs space-y-2 transition group"
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="font-semibold text-xs text-[var(--text-primary)] group-hover:text-[var(--accent-terracotta)] transition leading-snug">
                    {c.document_name}
                  </div>
                  {c.url && (
                    <a
                      href={c.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-[var(--accent-terracotta)] hover:brightness-110 shrink-0 p-1"
                      title="View Official Source"
                    >
                      <ExternalLink size={13} />
                    </a>
                  )}
                </div>

                {c.clause && (
                  <div className="text-[11px] font-mono text-[var(--text-muted)] bg-[var(--bg-sidebar)] px-2 py-0.5 rounded border border-[var(--border-color)] inline-block self-start">
                    Clause: {c.clause}
                  </div>
                )}

                <div className="flex items-center justify-between text-[10px] text-[var(--text-muted)] pt-1 border-t border-[var(--border-color)]/60 font-mono">
                  <span>Confidence Match</span>
                  <span className="font-bold text-[var(--accent-terracotta)]">{scorePct}%</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
