import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Copy, Check, Volume2, VolumeX, ThumbsUp, ThumbsDown, Zap, Clock } from 'lucide-react';
import Citations from './Citations';

export default function ChatMessage({ message }) {
  const { role, content, citations, query_category, timestamp, processing_time_ms } = message;
  const isUser = role === 'user';
  const [copied, setCopied] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [feedback, setFeedback] = useState(null); // 'up' | 'down' | null

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleSpeak = () => {
    if (!('speechSynthesis' in window)) {
      alert('Text-to-speech is not supported by your browser.');
      return;
    }

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    } else {
      window.speechSynthesis.cancel();
      const plainText = content.replace(/[*#`_[\]()]/g, '');
      const utterance = new SpeechSynthesisUtterance(plainText);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;

      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);

      window.speechSynthesis.speak(utterance);
      setIsSpeaking(true);
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto py-3">
      {isUser ? (
        /* User Message */
        <div className="flex items-start justify-end gap-3">
          <div className="bg-[var(--bg-card)] border border-[var(--border-color)] text-[var(--text-primary)] rounded-2xl rounded-tr-none px-4 py-3 max-w-[85%] text-xs sm:text-sm leading-relaxed shadow-2xs">
            <p className="whitespace-pre-wrap">{content}</p>
            {timestamp && (
              <div className="text-[10px] text-[var(--text-muted)] text-right mt-1 font-mono">
                {new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            )}
          </div>
          <div className="w-7 h-7 rounded-full bg-slate-300 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-bold flex items-center justify-center text-xs shrink-0 font-mono mt-0.5 shadow-2xs">
            U
          </div>
        </div>
      ) : (
        /* Assistant Message (Claude Style) */
        <div className="flex items-start gap-3.5">
          <div className="w-7 h-7 rounded-full bg-[var(--accent-terracotta)] text-white font-bold flex items-center justify-center text-xs shrink-0 mt-0.5 shadow-xs">
            B
          </div>

          <div className="flex-1 space-y-3 min-w-0">
            
            {/* Category / Grounding Tag */}
            {query_category && (
              <div className="flex items-center gap-2 text-[11px] font-mono">
                <span className="bg-[var(--bg-card-elevated)] border border-[var(--border-color)] text-[var(--accent-terracotta)] font-semibold px-2 py-0.5 rounded">
                  {query_category}
                </span>
                {processing_time_ms != null && (
                  <span className="text-[var(--text-muted)] flex items-center gap-1 text-[10px]">
                    <Zap size={10} className="text-[var(--accent-terracotta)]" />
                    {processing_time_ms.toFixed(0)}ms
                  </span>
                )}
              </div>
            )}

            {/* Markdown Body */}
            <div className="claude-prose text-xs sm:text-sm text-[var(--text-primary)]">
              <ReactMarkdown>{content}</ReactMarkdown>
            </div>

            {/* Citations / Grounded Sources Artifacts */}
            {citations && citations.length > 0 && (
              <div className="pt-1">
                <Citations citations={citations} />
              </div>
            )}

            {/* Action Ribbon */}
            <div className="flex items-center justify-between pt-2 border-t border-[var(--border-color)]/60 text-xs text-[var(--text-muted)]">
              <div className="flex items-center gap-3">
                <button
                  onClick={handleCopy}
                  className="hover:text-[var(--text-primary)] flex items-center gap-1 transition p-1 rounded hover:bg-[var(--bg-card)]"
                  title="Copy response"
                >
                  {copied ? <Check size={13} className="text-emerald-500" /> : <Copy size={13} />}
                  <span>{copied ? 'Copied' : 'Copy'}</span>
                </button>

                <button
                  onClick={handleSpeak}
                  className="hover:text-[var(--text-primary)] flex items-center gap-1 transition p-1 rounded hover:bg-[var(--bg-card)]"
                  title={isSpeaking ? 'Stop speech' : 'Read aloud'}
                >
                  {isSpeaking ? <VolumeX size={13} className="text-rose-500" /> : <Volume2 size={13} />}
                  <span>{isSpeaking ? 'Stop' : 'Listen'}</span>
                </button>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => setFeedback(feedback === 'up' ? null : 'up')}
                  className={`p-1 rounded transition hover:bg-[var(--bg-card)] ${feedback === 'up' ? 'text-[var(--accent-terracotta)]' : 'hover:text-[var(--text-primary)]'}`}
                  title="Helpful"
                >
                  <ThumbsUp size={13} />
                </button>

                <button
                  onClick={() => setFeedback(feedback === 'down' ? null : 'down')}
                  className={`p-1 rounded transition hover:bg-[var(--bg-card)] ${feedback === 'down' ? 'text-rose-500' : 'hover:text-[var(--text-primary)]'}`}
                  title="Needs improvement"
                >
                  <ThumbsDown size={13} />
                </button>

                {timestamp && (
                  <span className="text-[10px] text-[var(--text-muted)] font-mono pl-2 flex items-center gap-1">
                    <Clock size={10} />
                    {new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                )}
              </div>
            </div>

          </div>
        </div>
      )}
    </div>
  );
}
