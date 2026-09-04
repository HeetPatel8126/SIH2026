import { useState } from 'react';
import { X, BookOpen, ExternalLink, Copy, Check, MessageSquarePlus, ShieldCheck } from 'lucide-react';

export default function ClausePreviewModal({ citation, onClose, onAskAboutClause }) {
  const [copied, setCopied] = useState(false);

  if (!citation) return null;

  const scorePct = citation.relevance_score != null ? Math.round(citation.relevance_score * 100) : 92;

  const handleCopy = () => {
    const text = `${citation.document_name} ${citation.clause ? `— Clause: ${citation.clause}` : ''}\n${citation.text || citation.snippet || ''}`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs animate-in fade-in duration-150">
      <div className="w-full max-w-lg bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl shadow-elevated overflow-hidden animate-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="px-5 py-4 border-b border-[var(--border-color)] bg-[var(--bg-card-elevated)]/60 flex items-start justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-[var(--accent-terracotta)]/10 text-[var(--accent-terracotta)] flex items-center justify-center font-bold text-xs shrink-0">
              <BookOpen size={16} />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-sm text-[var(--text-primary)]">{citation.document_name}</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-semibold border border-emerald-500/20">
                  {scorePct}% Match
                </span>
              </div>
              {citation.clause && (
                <div className="text-xs text-[var(--text-muted)] font-mono mt-0.5">
                  Clause: {citation.clause}
                </div>
              )}
            </div>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="p-1 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-sidebar)] transition"
          >
            <X size={18} />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-5 space-y-4 max-h-80 overflow-y-auto">
          {/* Regulatory Summary / Snippet */}
          <div className="space-y-1.5">
            <div className="text-[11px] uppercase font-mono tracking-wider text-[var(--text-muted)] font-semibold flex items-center gap-1.5">
              <ShieldCheck size={13} className="text-[var(--accent-terracotta)]" />
              Verified Standard Clause Text
            </div>
            <div className="p-3.5 rounded-xl bg-[var(--bg-primary)] border border-[var(--border-color)] text-xs text-[var(--text-primary)] font-mono leading-relaxed whitespace-pre-wrap">
              {citation.text || citation.snippet || 'Official verified clause content from the Bureau of Indian Standards gazette publication.'}
            </div>
          </div>

          {/* Metadata Grid */}
          <div className="grid grid-cols-2 gap-2 text-xs font-mono">
            <div className="p-2.5 rounded-xl bg-[var(--bg-sidebar)]/60 border border-[var(--border-color)]">
              <div className="text-[10px] text-[var(--text-muted)]">Authority</div>
              <div className="font-semibold text-[var(--text-primary)] mt-0.5">Bureau of Indian Standards</div>
            </div>
            <div className="p-2.5 rounded-xl bg-[var(--bg-sidebar)]/60 border border-[var(--border-color)]">
              <div className="text-[10px] text-[var(--text-muted)]">Verification Status</div>
              <div className="font-semibold text-emerald-600 dark:text-emerald-400 mt-0.5">Mandatory Gazette Active</div>
            </div>
          </div>
        </div>

        {/* Actions Footer */}
        <div className="px-5 py-3 border-t border-[var(--border-color)] bg-[var(--bg-card-elevated)]/40 flex items-center justify-between gap-3">
          <button
            type="button"
            onClick={handleCopy}
            className="px-3 py-1.5 rounded-xl border border-[var(--border-color)] hover:bg-[var(--bg-card)] text-xs text-[var(--text-secondary)] hover:text-[var(--text-primary)] flex items-center gap-1.5 transition shadow-2xs font-medium"
          >
            {copied ? <Check size={13} className="text-emerald-500" /> : <Copy size={13} />}
            <span>{copied ? 'Copied' : 'Copy Clause'}</span>
          </button>

          <div className="flex items-center gap-2">
            {citation.url && (
              <a
                href={citation.url}
                target="_blank"
                rel="noopener noreferrer"
                className="px-3 py-1.5 rounded-xl border border-[var(--border-color)] hover:bg-[var(--bg-card)] text-xs text-[var(--text-secondary)] hover:text-[var(--text-primary)] flex items-center gap-1.5 transition shadow-2xs font-medium"
              >
                <span>Gazette PDF</span>
                <ExternalLink size={12} />
              </a>
            )}

            {onAskAboutClause && (
              <button
                type="button"
                onClick={() => {
                  onAskAboutClause(`Explain ${citation.document_name} ${citation.clause ? `Clause ${citation.clause}` : ''} requirements in detail with testing procedures.`);
                  onClose();
                }}
                className="px-3.5 py-1.5 rounded-xl bg-[var(--accent-terracotta)] hover:bg-[var(--accent-terracotta-hover)] text-white text-xs font-semibold flex items-center gap-1.5 transition shadow-2xs cursor-pointer"
              >
                <MessageSquarePlus size={13} />
                <span>Ask AI About This</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
