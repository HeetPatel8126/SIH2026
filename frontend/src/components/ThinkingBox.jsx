import { useState, useEffect } from 'react';
import { Sparkles, ChevronDown, ChevronRight, CheckCircle2, Search, BookOpen, Layers } from 'lucide-react';

export default function ThinkingBox({ thinkingState, autoExpand = false }) {
  const {
    isThinking,
    aiThoughtText = '',
    thoughtSteps = [],
    thoughtTimeMs,
    thoughtSummary,
    sources = [],
    category,
  } = thinkingState;

  // Auto-expand while actively thinking or when autoExpand is enabled
  const [expanded, setExpanded] = useState(isThinking || autoExpand);

  // Live timer while actively thinking
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    let timer;
    if (isThinking) {
      setExpanded(true);
      const start = Date.now();
      timer = setInterval(() => {
        setElapsed(((Date.now() - start) / 1000).toFixed(1));
      }, 100);
    } else {
      setExpanded(autoExpand);
    }
    return () => clearInterval(timer);
  }, [isThinking, autoExpand]);

  if (!isThinking && !thoughtSummary && !aiThoughtText && thoughtSteps.length === 0) {
    return null;
  }

  const durationText = thoughtTimeMs
    ? `${(thoughtTimeMs / 1000).toFixed(1)}s`
    : `${elapsed}s`;

  return (
    <div className="w-full my-2 border border-[var(--border-color)]/70 rounded-xl bg-[var(--bg-card)] overflow-hidden shadow-2xs transition-all duration-200">
      {/* Header Bar */}
      <button
        type="button"
        onClick={() => setExpanded((prev) => !prev)}
        className="w-full px-3.5 py-2 flex items-center justify-between text-xs text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-card-elevated)]/60 transition"
      >
        <div className="flex items-center gap-2">
          {isThinking ? (
            <div className="relative flex items-center justify-center">
              <span className="w-2.5 h-2.5 rounded-full bg-[var(--accent-terracotta)] animate-ping absolute opacity-75"></span>
              <Sparkles size={13} className="text-[var(--accent-terracotta)] animate-pulse relative" />
            </div>
          ) : (
            <CheckCircle2 size={13} className="text-emerald-500 shrink-0" />
          )}

          <span className="font-medium text-[11px] tracking-wide">
            {isThinking ? (
              <span className="flex items-center gap-1.5 font-semibold text-[var(--accent-terracotta)]">
                Thinking... <span className="font-mono text-[10px] text-[var(--text-muted)] font-normal">({durationText})</span>
              </span>
            ) : (
              <span>
                Thought for <span className="font-semibold text-[var(--text-primary)] font-mono">{durationText}</span>
              </span>
            )}
          </span>

          {category && (
            <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-[var(--bg-card-elevated)] border border-[var(--border-color)] text-[var(--text-muted)]">
              {category}
            </span>
          )}
        </div>

        <div className="flex items-center gap-1 text-[var(--text-muted)]">
          <span className="text-[10px] hidden sm:inline">{expanded ? 'Hide' : 'Show reasoning'}</span>
          {expanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
        </div>
      </button>

      {/* Expanded Reasoning & Retrieval Details */}
      {expanded && (
        <div className="px-3.5 py-2.5 border-t border-[var(--border-color)]/60 bg-[var(--bg-card-elevated)]/40 space-y-2 text-[11px] font-mono text-[var(--text-secondary)]">
          {/* Authentic AI Thought Stream */}
          {aiThoughtText ? (
            <div className="relative font-mono text-[11px] leading-relaxed text-[var(--text-secondary)] bg-[var(--bg-primary)]/60 p-2.5 rounded-lg border border-[var(--border-color)]/40 whitespace-pre-wrap max-h-60 overflow-y-auto">
              <div className="text-[10px] uppercase font-sans font-semibold tracking-wider text-[var(--text-muted)] mb-1.5 flex items-center gap-1.5">
                <Sparkles size={11} className="text-[var(--accent-terracotta)]" />
                AI Model Reasoning (Chain of Thought)
              </div>
              {aiThoughtText}
              {isThinking && (
                <span className="inline-block w-1.5 h-3 ml-1 bg-[var(--accent-terracotta)] animate-pulse align-middle" />
              )}
            </div>
          ) : isThinking ? (
            <div className="flex items-center gap-2 py-1 text-[11px] text-[var(--text-muted)] italic font-sans">
              <span className="w-1.5 h-1.5 rounded-full bg-[var(--accent-terracotta)] animate-pulse"></span>
              Generating internal Chain-of-Thought reasoning...
            </div>
          ) : null}

          {/* Active Steps Log (if present) */}
          {thoughtSteps.length > 0 && (
            <div className="space-y-1">
              {thoughtSteps.map((s, idx) => (
                <div key={idx} className="flex items-start gap-2 text-[var(--text-secondary)]">
                  <span className="text-[var(--accent-terracotta)] shrink-0">›</span>
                  <span className="leading-tight">{s.message || s}</span>
                </div>
              ))}
            </div>
          )}

          {/* Retrieved Standard Sources Pills */}
          {sources.length > 0 && (
            <div className="pt-1 flex items-center gap-1.5 flex-wrap">
              <span className="text-[10px] text-[var(--text-muted)] flex items-center gap-1">
                <BookOpen size={11} /> Grounded in:
              </span>
              {sources.map((src, i) => (
                <span
                  key={i}
                  className="px-2 py-0.5 rounded bg-[var(--bg-primary)] border border-[var(--border-color)] text-[var(--text-primary)] text-[10px] font-semibold"
                >
                  {src}
                </span>
              ))}
            </div>
          )}

          {/* Thought Summary */}
          {thoughtSummary && (
            <p className="text-[11px] font-sans text-[var(--text-muted)] border-t border-[var(--border-color)]/40 pt-1.5 leading-relaxed">
              {thoughtSummary}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
