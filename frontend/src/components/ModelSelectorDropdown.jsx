import { useState, useRef, useEffect } from 'react';
import { Cpu, ChevronDown, Check, Zap, Brain, Cloud, ShieldCheck, Settings2 } from 'lucide-react';

export const ENGINE_OPTIONS = [
  {
    id: 'ollama-qwen',
    name: 'Qwen 2.5 7B (Local Core)',
    badge: 'NVIDIA RTX 4060',
    icon: Cpu,
    tag: 'LOCAL GPU',
    speed: '~42 tok/s',
    desc: 'Local private execution via Ollama with authentic Chain of Thought',
    isLocal: true,
  },
  {
    id: 'cot-deep',
    name: 'Deep Standards Reasoning',
    badge: 'CoT High-Precision',
    icon: Brain,
    tag: 'REASONING',
    speed: '~35 tok/s',
    desc: 'Multi-step deduction cross-referencing tables, clauses, and gazettes',
    isLocal: true,
  },
  {
    id: 'groq-llama',
    name: 'Groq Llama 3.3 70B',
    badge: 'Cloud LPU',
    icon: Zap,
    tag: 'CLOUD FAST',
    speed: '~280 tok/s',
    desc: 'Sub-second ultra-fast cloud inference with zero latency',
    isLocal: false,
  },
  {
    id: 'gemini-flash',
    name: 'Google Gemini 1.5 Flash',
    badge: 'Cloud AI',
    icon: Cloud,
    tag: 'MULTIMODAL',
    speed: '~120 tok/s',
    desc: 'Deep document comprehension with broad context window',
    isLocal: false,
  },
];

export default function ModelSelectorDropdown({
  selectedEngine = 'ollama-qwen',
  onSelectEngine = () => {},
}) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  const active = ENGINE_OPTIONS.find((e) => e.id === selectedEngine) || ENGINE_OPTIONS[0];
  const ActiveIcon = active.icon;

  useEffect(() => {
    function handleClickOutside(e) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    }
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen]);

  useEffect(() => {
    function handleKeyDown(e) {
      if (e.key === 'Escape' && isOpen) {
        setIsOpen(false);
      }
    }
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  return (
    <div className="relative inline-block text-left" ref={dropdownRef}>
      {/* Trigger Pill */}
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        className={`
          flex items-center gap-2 px-2.5 py-1.5 rounded-xl border text-xs transition-all duration-150 shadow-2xs cursor-pointer select-none
          ${isOpen
            ? 'bg-[var(--bg-card-elevated)] border-[var(--accent-terracotta)] text-[var(--accent-terracotta)] ring-2 ring-[var(--accent-terracotta)]/20'
            : 'bg-[var(--bg-card)] border-[var(--border-color)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:border-[var(--border-hover)]'
          }
        `}
      >
        <div className="relative flex items-center justify-center">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
        </div>

        <ActiveIcon size={13} className="text-[var(--accent-terracotta)] shrink-0" />

        <div className="flex items-center gap-1.5">
          <span className="font-semibold text-xs text-[var(--text-primary)]">{active.name}</span>
          <span className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-[var(--bg-sidebar)] border border-[var(--border-color)] text-[var(--text-muted)] hidden sm:inline">
            {active.badge}
          </span>
        </div>

        <ChevronDown size={13} className={`text-[var(--text-muted)] transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {/* Popover Card */}
      {isOpen && (
        <div className="absolute top-full left-0 mt-2 w-80 bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl shadow-elevated z-50 overflow-hidden animate-in fade-in zoom-in-95 duration-100 backdrop-blur-md">
          {/* Header */}
          <div className="p-3 border-b border-[var(--border-color)] bg-[var(--bg-card-elevated)]/60 flex items-center justify-between">
            <div className="flex items-center gap-1.5">
              <Settings2 size={13} className="text-[var(--accent-terracotta)]" />
              <span className="font-semibold text-xs text-[var(--text-primary)]">Inference Engine Selector</span>
            </div>
            <span className="text-[10px] font-mono text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded border border-emerald-500/20">
              Active: RTX 4060
            </span>
          </div>

          {/* List of Models */}
          <div className="p-2 space-y-1">
            {ENGINE_OPTIONS.map((opt) => {
              const Icon = opt.icon;
              const isSelected = opt.id === selectedEngine;
              return (
                <button
                  key={opt.id}
                  type="button"
                  onClick={() => {
                    onSelectEngine(opt.id);
                    setIsOpen(false);
                  }}
                  className={`
                    w-full p-2.5 rounded-xl border text-left transition flex items-start justify-between gap-2.5
                    ${isSelected
                      ? 'bg-[var(--accent-terracotta)]/10 border-[var(--accent-terracotta)]/50'
                      : 'border-transparent hover:border-[var(--border-color)] hover:bg-[var(--bg-card-elevated)]'
                    }
                  `}
                >
                  <div className="flex items-start gap-2.5 min-w-0">
                    <div className={`p-1.5 rounded-lg shrink-0 mt-0.5 ${isSelected ? 'bg-[var(--accent-terracotta)] text-white' : 'bg-[var(--bg-sidebar)] text-[var(--text-muted)]'}`}>
                      <Icon size={14} />
                    </div>
                    <div className="min-w-0">
                      <div className="flex items-center gap-1.5">
                        <span className="font-semibold text-xs text-[var(--text-primary)] truncate">
                          {opt.name}
                        </span>
                        <span className="text-[9px] font-mono px-1 py-0.2 rounded bg-[var(--bg-sidebar)] border border-[var(--border-color)] text-[var(--text-muted)] shrink-0">
                          {opt.tag}
                        </span>
                      </div>
                      <p className="text-[11px] text-[var(--text-secondary)] mt-0.5 leading-snug">
                        {opt.desc}
                      </p>
                      <div className="text-[10px] font-mono text-[var(--text-muted)] mt-1 flex items-center gap-2">
                        <span>Speed: {opt.speed}</span>
                        <span>•</span>
                        <span>{opt.isLocal ? '100% Offline' : 'Web Fallback'}</span>
                      </div>
                    </div>
                  </div>

                  {isSelected && (
                    <Check size={15} className="text-[var(--accent-terracotta)] shrink-0 mt-1" />
                  )}
                </button>
              );
            })}
          </div>

          {/* Footer */}
          <div className="px-3 py-2 border-t border-[var(--border-color)] bg-[var(--bg-card-elevated)]/30 text-[10px] text-[var(--text-muted)] flex items-center justify-between font-mono">
            <span>RAG Grounding: ChromaDB Active</span>
            <span>Zero Hallucination Mode</span>
          </div>
        </div>
      )}
    </div>
  );
}
