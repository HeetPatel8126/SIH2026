import { useState, useRef, useEffect, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import { Trash2, Download, AlertCircle } from 'lucide-react';
import ChatMessage from '../components/ChatMessage';
import ChatInput from '../components/ChatInput';
import WelcomeScreen from '../components/WelcomeScreen';
import { sendChat } from '../services/api';

const STORAGE_KEY = 'bis_assistant_chat_history';

export default function ChatPage() {
  const [messages, setMessages] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const scrollContainerRef = useRef(null);
  const location = useLocation();

  // Save messages to localStorage
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
    } catch {
      // ignore storage errors
    }
  }, [messages]);

  const scrollToBottom = useCallback(() => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTo({
        top: scrollContainerRef.current.scrollHeight,
        behavior: 'smooth'
      });
    }
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading, scrollToBottom]);

  const handleSend = useCallback(async (query, lang = selectedLanguage) => {
    if (!query.trim()) return;

    const userMsg = {
      role: 'user',
      content: query.trim(),
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    setError(null);

    try {
      const data = await sendChat({
        query: query.trim(),
        language: lang,
        session_id: sessionId
      });

      if (data.session_id) setSessionId(data.session_id);

      const assistantMsg = {
        role: 'assistant',
        content: data.answer,
        citations: data.citations || [],
        query_category: data.query_category,
        timestamp: data.timestamp || new Date().toISOString(),
        processing_time_ms: data.processing_time_ms,
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setError(err.message || 'Failed to get a response. Please check if the backend server is running.');
    } finally {
      setLoading(false);
    }
  }, [selectedLanguage, sessionId]);

  // Handle incoming prompts from router state
  useEffect(() => {
    if (location.state?.initialPrompt) {
      handleSend(location.state.initialPrompt, selectedLanguage);
      window.history.replaceState({}, document.title);
    }
  }, [location.state, handleSend, selectedLanguage]);

  const handleClearChat = () => {
    if (messages.length === 0) return;
    if (window.confirm('Clear this conversation?')) {
      setMessages([]);
      setSessionId(null);
      setError(null);
      localStorage.removeItem(STORAGE_KEY);
    }
  };

  const handleExportChat = () => {
    if (messages.length === 0) return;
    const exportText = messages
      .map((m) => `### ${m.role === 'user' ? 'User' : 'BIS AI Assistant'} (${new Date(m.timestamp).toLocaleString()})\n\n${m.content}\n\n---\n`)
      .join('\n');

    const blob = new Blob([exportText], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `bis-ai-conversation-${new Date().toISOString().slice(0, 10)}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex-1 flex flex-col justify-between overflow-hidden relative h-full min-h-0">
      
      {/* Claude Minimal Top Bar */}
      <header className="px-6 py-3 border-b border-[var(--border-color)] bg-[var(--bg-primary)]/90 backdrop-blur-md flex items-center justify-between z-10 shrink-0">
        <div className="flex items-center gap-2">
          <span className="font-semibold text-xs sm:text-sm text-[var(--text-primary)]">
            BIS Standards Advisory
          </span>
          <span className="text-[11px] font-mono text-[var(--text-muted)] bg-[var(--bg-sidebar)] px-2 py-0.5 rounded border border-[var(--border-color)] hidden sm:inline">
            v2.6 Core
          </span>
        </div>

        {messages.length > 0 && (
          <div className="flex items-center gap-2 text-xs">
            <button
              onClick={handleExportChat}
              className="p-1.5 px-2.5 rounded-lg border border-[var(--border-color)] hover:bg-[var(--bg-card)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition flex items-center gap-1.5 shadow-2xs"
              title="Export Conversation as Markdown"
            >
              <Download size={13} />
              <span className="hidden sm:inline">Export</span>
            </button>
            <button
              onClick={handleClearChat}
              className="p-1.5 px-2.5 rounded-lg border border-[var(--border-color)] hover:bg-rose-500/10 text-rose-500 hover:text-rose-600 transition flex items-center gap-1.5 shadow-2xs"
              title="Clear Conversation"
            >
              <Trash2 size={13} />
              <span className="hidden sm:inline">Clear</span>
            </button>
          </div>
        )}
      </header>

      {/* Messages Stream / Welcome Hero */}
      <div 
        ref={scrollContainerRef}
        className="flex-1 overflow-y-auto px-4 sm:px-8 py-6 space-y-6 min-h-0"
      >
        {messages.length === 0 && !loading ? (
          <WelcomeScreen onQuestionClick={(q) => handleSend(q, selectedLanguage)} />
        ) : (
          <div className="space-y-6">
            {messages.map((msg, i) => (
              <ChatMessage key={i} message={msg} />
            ))}

            {/* Typing indicator */}
            {loading && (
              <div className="w-full max-w-3xl mx-auto flex items-start gap-3.5 py-3">
                <div className="w-7 h-7 rounded-full bg-[var(--accent-terracotta)] text-white font-bold flex items-center justify-center text-xs shrink-0 mt-0.5 shadow-xs">
                  B
                </div>
                <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl rounded-tl-none p-4 flex items-center gap-1.5 shadow-2xs">
                  <span className="w-2 h-2 rounded-full bg-[var(--accent-terracotta)] animate-bounce [animation-delay:-0.3s]"></span>
                  <span className="w-2 h-2 rounded-full bg-[var(--accent-terracotta)] animate-bounce [animation-delay:-0.15s]"></span>
                  <span className="w-2 h-2 rounded-full bg-[var(--accent-terracotta)] animate-bounce"></span>
                </div>
              </div>
            )}

            {/* Error Notification */}
            {error && (
              <div className="max-w-3xl w-full mx-auto p-4 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-300 text-xs flex items-center gap-2.5 shadow-2xs">
                <AlertCircle size={16} className="shrink-0" />
                <div>
                  <strong>Error:</strong> {error}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Claude Bottom Input Container */}
      <div className="shrink-0">
        <ChatInput
          onSend={handleSend}
          disabled={loading}
          selectedLanguage={selectedLanguage}
          onLanguageChange={setSelectedLanguage}
        />
      </div>

    </div>
  );
}
