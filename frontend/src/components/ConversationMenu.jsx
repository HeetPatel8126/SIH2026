import { useState, useRef, useEffect } from 'react';
import { MoreVertical, Download, FileJson, Copy, Check, Trash2, Eye, EyeOff, Sparkles } from 'lucide-react';

export default function ConversationMenu({
  messages = [],
  onExportMarkdown,
  onExportJson,
  onClearChat,
  autoExpandThinking,
  onToggleAutoExpandThinking,
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [copied, setCopied] = useState(false);
  const [showClearConfirm, setShowClearConfirm] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(e) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
        setShowClearConfirm(false);
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
        setShowClearConfirm(false);
      }
    }
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  const handleCopyTranscript = () => {
    if (messages.length === 0) return;
    const text = messages
      .map((m) => `[${m.role === 'user' ? 'USER' : 'BIS AI ASSISTANT'}]:\n${m.content}\n`)
      .join('\n---\n\n');
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => {
      setCopied(false);
      setIsOpen(false);
    }, 1500);
  };

  return (
    <div className="relative inline-block text-left" ref={dropdownRef}>
      {/* Trigger Button */}
      <button
        type="button"
        onClick={() => {
          setIsOpen((prev) => !prev);
          setShowClearConfirm(false);
        }}
        className={`
          p-1.5 rounded-xl border text-xs transition-all duration-150 shadow-2xs cursor-pointer select-none
          ${isOpen
            ? 'bg-[var(--bg-card-elevated)] border-[var(--accent-terracotta)] text-[var(--accent-terracotta)] ring-2 ring-[var(--accent-terracotta)]/20'
            : 'bg-[var(--bg-card)] border-[var(--border-color)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:border-[var(--border-hover)]'
          }
        `}
        title="Conversation Actions & Export"
      >
        <MoreVertical size={15} />
      </button>

      {/* Popover Dropdown */}
      {isOpen && (
        <div className="absolute top-full right-0 mt-2 w-64 bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl shadow-elevated z-50 overflow-hidden animate-in fade-in zoom-in-95 duration-100 backdrop-blur-md">
          <div className="p-2.5 border-b border-[var(--border-color)] bg-[var(--bg-card-elevated)]/60 flex items-center justify-between">
            <span className="font-semibold text-xs text-[var(--text-primary)]">Chat Actions</span>
            <span className="text-[10px] text-[var(--text-muted)] font-mono">{messages.length} messages</span>
          </div>

          <div className="p-1.5 space-y-0.5 text-xs">
            {/* Export Markdown */}
            <button
              type="button"
              onClick={() => {
                onExportMarkdown();
                setIsOpen(false);
              }}
              disabled={messages.length === 0}
              className="w-full px-2.5 py-2 rounded-xl text-left hover:bg-[var(--bg-card-elevated)] text-[var(--text-primary)] flex items-center gap-2.5 transition disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <Download size={14} className="text-[var(--accent-terracotta)] shrink-0" />
              <div>
                <div className="font-semibold text-[11px]">Export as Markdown</div>
                <div className="text-[10px] text-[var(--text-muted)]">Download formatted `.md` notes</div>
              </div>
            </button>

            {/* Export JSON */}
            <button
              type="button"
              onClick={() => {
                onExportJson();
                setIsOpen(false);
              }}
              disabled={messages.length === 0}
              className="w-full px-2.5 py-2 rounded-xl text-left hover:bg-[var(--bg-card-elevated)] text-[var(--text-primary)] flex items-center gap-2.5 transition disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <FileJson size={14} className="text-blue-500 shrink-0" />
              <div>
                <div className="font-semibold text-[11px]">Export Session JSON</div>
                <div className="text-[10px] text-[var(--text-muted)]">Includes citations & tokens metadata</div>
              </div>
            </button>

            {/* Copy Full Transcript */}
            <button
              type="button"
              onClick={handleCopyTranscript}
              disabled={messages.length === 0}
              className="w-full px-2.5 py-2 rounded-xl text-left hover:bg-[var(--bg-card-elevated)] text-[var(--text-primary)] flex items-center gap-2.5 transition disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {copied ? <Check size={14} className="text-emerald-500 shrink-0" /> : <Copy size={14} className="text-[var(--text-muted)] shrink-0" />}
              <div>
                <div className="font-semibold text-[11px]">{copied ? 'Transcript Copied!' : 'Copy Transcript'}</div>
                <div className="text-[10px] text-[var(--text-muted)]">Copy raw dialogue to clipboard</div>
              </div>
            </button>

            {/* Divider */}
            <div className="border-t border-[var(--border-color)]/60 my-1"></div>

            {/* Toggle Thinking Visibility Default */}
            {onToggleAutoExpandThinking && (
              <button
                type="button"
                onClick={onToggleAutoExpandThinking}
                className="w-full px-2.5 py-2 rounded-xl text-left hover:bg-[var(--bg-card-elevated)] text-[var(--text-primary)] flex items-center justify-between transition"
              >
                <div className="flex items-center gap-2.5">
                  <Sparkles size={14} className="text-[var(--accent-terracotta)] shrink-0" />
                  <div>
                    <div className="font-semibold text-[11px]">Auto-Expand Thinking</div>
                    <div className="text-[10px] text-[var(--text-muted)]">Show internal reasoning by default</div>
                  </div>
                </div>
                <div className={`w-8 h-4.5 rounded-full transition-colors flex items-center p-0.5 ${autoExpandThinking ? 'bg-[var(--accent-terracotta)]' : 'bg-[var(--border-color)]'}`}>
                  <div className={`w-3.5 h-3.5 rounded-full bg-white transition-transform ${autoExpandThinking ? 'translate-x-3.5' : 'translate-x-0'}`} />
                </div>
              </button>
            )}

            {/* Divider */}
            <div className="border-t border-[var(--border-color)]/60 my-1"></div>

            {/* Clear Chat with inline confirm */}
            {!showClearConfirm ? (
              <button
                type="button"
                onClick={() => setShowClearConfirm(true)}
                disabled={messages.length === 0}
                className="w-full px-2.5 py-2 rounded-xl text-left hover:bg-rose-500/10 text-rose-500 hover:text-rose-600 flex items-center gap-2.5 transition disabled:opacity-40 disabled:cursor-not-allowed"
              >
                <Trash2 size={14} className="shrink-0" />
                <div>
                  <div className="font-semibold text-[11px]">Clear Conversation</div>
                  <div className="text-[10px] text-[var(--text-muted)]">Reset all messages & memory</div>
                </div>
              </button>
            ) : (
              <div className="p-2.5 rounded-xl bg-rose-500/10 border border-rose-500/30 space-y-2">
                <div className="text-xs text-rose-500 font-semibold">Are you sure?</div>
                <div className="text-[10px] text-[var(--text-muted)] leading-tight">This will permanently delete this conversation history.</div>
                <div className="flex items-center gap-2 pt-1">
                  <button
                    type="button"
                    onClick={() => {
                      onClearChat();
                      setIsOpen(false);
                      setShowClearConfirm(false);
                    }}
                    className="flex-1 py-1 rounded-lg bg-rose-500 text-white font-semibold text-xs hover:bg-rose-600 transition"
                  >
                    Yes, Clear
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowClearConfirm(false)}
                    className="flex-1 py-1 rounded-lg bg-[var(--bg-card)] border border-[var(--border-color)] text-xs text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
