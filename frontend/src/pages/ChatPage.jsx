import { useState, useRef, useEffect, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import { AlertCircle } from 'lucide-react';
import ChatMessage from '../components/ChatMessage';
import ChatInput from '../components/ChatInput';
import WelcomeScreen from '../components/WelcomeScreen';
import ModelSelectorDropdown from '../components/ModelSelectorDropdown';
import DomainFilterDropdown from '../components/DomainFilterDropdown';
import ConversationMenu from '../components/ConversationMenu';
import { streamChat, sendChat } from '../services/api';

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
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [selectedEngine, setSelectedEngine] = useState('ollama-qwen');
  const [selectedDomain, setSelectedDomain] = useState('all');
  const [autoExpandThinking, setAutoExpandThinking] = useState(false);
  
  const scrollContainerRef = useRef(null);
  const abortControllerRef = useRef(null);
  const location = useLocation();
  const lastConsumedPromptRef = useRef(null);
  const sessionIdRef = useRef(sessionId);
  const selectedLanguageRef = useRef(selectedLanguage);

  useEffect(() => {
    sessionIdRef.current = sessionId;
  }, [sessionId]);

  useEffect(() => {
    selectedLanguageRef.current = selectedLanguage;
  }, [selectedLanguage]);

  // Save messages to localStorage (excluding temporary streaming flags)
  useEffect(() => {
    try {
      const cleanMessages = messages.map((m) => {
        const copy = { ...m };
        delete copy.isStreaming;
        if (copy.thinking) {
          copy.thinking = { ...copy.thinking, isThinking: false };
        }
        return copy;
      });
      localStorage.setItem(STORAGE_KEY, JSON.stringify(cleanMessages));
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
  }, [messages, loading, isStreaming, scrollToBottom]);

  const handleStop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setIsStreaming(false);
    setLoading(false);
    setMessages((prev) =>
      prev.map((msg, idx) =>
        idx === prev.length - 1 && msg.role === 'assistant'
          ? { ...msg, isStreaming: false, thinking: msg.thinking ? { ...msg.thinking, isThinking: false } : null }
          : msg
      )
    );
  };

  const handleSend = useCallback(async (query, lang = selectedLanguage) => {
    if (!query.trim()) return;

    const userMsg = {
      role: 'user',
      content: query.trim(),
      timestamp: new Date().toISOString(),
    };

    const initialAssistantMsg = {
      role: 'assistant',
      content: '',
      isStreaming: true,
      citations: [],
      query_category: null,
      thinking: {
        isThinking: true,
        aiThoughtText: '',
        thoughtSteps: [],
        thoughtTimeMs: null,
        thoughtSummary: null,
        sources: [],
        category: null,
      },
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg, initialAssistantMsg]);
    setLoading(true);
    setIsStreaming(true);
    setError(null);

    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }

    const controller = new AbortController();
    abortControllerRef.current = controller;

    try {
      await streamChat({
        query: query.trim(),
        language: lang,
        session_id: sessionIdRef.current,
        signal: controller.signal,

        onThoughtToken: (token) => {
          setMessages((prev) => {
            const updated = [...prev];
            const last = { ...updated[updated.length - 1] };
            if (last.role === 'assistant' && last.thinking) {
              last.thinking = {
                ...last.thinking,
                aiThoughtText: (last.thinking.aiThoughtText || '') + token,
              };
              updated[updated.length - 1] = last;
            }
            return updated;
          });
        },

        onThought: (data) => {
          setMessages((prev) => {
            const updated = [...prev];
            const last = { ...updated[updated.length - 1] };
            if (last.role === 'assistant' && last.thinking) {
              const steps = [...(last.thinking.thoughtSteps || [])];
              if (!steps.some((s) => s.message === data.message)) {
                steps.push(data);
              }
              last.thinking = { ...last.thinking, thoughtSteps: steps };
              updated[updated.length - 1] = last;
            }
            return updated;
          });
        },

        onThoughtEnd: (data) => {
          setMessages((prev) => {
            const updated = [...prev];
            const last = { ...updated[updated.length - 1] };
            if (last.role === 'assistant' && last.thinking) {
              last.thinking = {
                ...last.thinking,
                isThinking: false,
                thoughtTimeMs: data.thought_time_ms,
                thoughtSummary: data.summary,
                sources: data.sources || [],
                category: data.category,
              };
              last.query_category = data.category;
              updated[updated.length - 1] = last;
            }
            return updated;
          });
        },

        onToken: (token) => {
          setMessages((prev) => {
            const updated = [...prev];
            const last = { ...updated[updated.length - 1] };
            if (last.role === 'assistant') {
              last.content = (last.content || '') + token;
              if (last.thinking && last.thinking.isThinking) {
                last.thinking.isThinking = false;
              }
              updated[updated.length - 1] = last;
            }
            return updated;
          });
        },

        onCitations: (citations) => {
          setMessages((prev) => {
            const updated = [...prev];
            const last = { ...updated[updated.length - 1] };
            if (last.role === 'assistant') {
              last.citations = citations;
              updated[updated.length - 1] = last;
            }
            return updated;
          });
        },

        onDone: (doneData) => {
          if (doneData.session_id) setSessionId(doneData.session_id);
          setMessages((prev) => {
            const updated = [...prev];
            const last = { ...updated[updated.length - 1] };
            if (last.role === 'assistant') {
              last.isStreaming = false;
              last.processing_time_ms = doneData.processing_time_ms;
              last.totalTokens = doneData.total_tokens;
              last.query_category = doneData.query_category || last.query_category;
              if (last.thinking) {
                last.thinking.isThinking = false;
              }
              updated[updated.length - 1] = last;
            }
            return updated;
          });
          setIsStreaming(false);
          setLoading(false);
        },

        onError: (err) => {
          if (err?.name === 'AbortError') return;
          console.warn('Stream failed:', err);

          setMessages((prev) => {
            const last = prev[prev.length - 1];
            // If tokens were already rendered, don't wipe and restart; just conclude gracefully
            if (last && last.role === 'assistant' && last.content && last.content.trim().length > 0) {
              const updated = [...prev];
              updated[updated.length - 1] = {
                ...last,
                isStreaming: false,
                thinking: last.thinking ? { ...last.thinking, isThinking: false } : null,
              };
              setIsStreaming(false);
              setLoading(false);
              return updated;
            }

            // Only if zero content was streamed, attempt fallback to one-shot
            sendChat({ query: query.trim(), language: lang, session_id: sessionIdRef.current })
              .then((data) => {
                if (data.session_id) setSessionId(data.session_id);
                setMessages((curr) => {
                  const updated = [...curr];
                  const lastMsg = {
                    role: 'assistant',
                    content: data.answer,
                    citations: data.citations || [],
                    query_category: data.query_category,
                    timestamp: data.timestamp || new Date().toISOString(),
                    processing_time_ms: data.processing_time_ms,
                    isStreaming: false,
                  };
                  updated[updated.length - 1] = lastMsg;
                  return updated;
                });
              })
              .catch((fallbackErr) => {
                setError(fallbackErr.message || 'Failed to get a response.');
              })
              .finally(() => {
                setIsStreaming(false);
                setLoading(false);
              });

            return prev;
          });
        },
      });
    } catch (err) {
      setError(err.message || 'Failed to connect to backend.');
      setIsStreaming(false);
      setLoading(false);
    }
  }, []);

  // Cleanup consumed prompt on unmount so navigating back to chat page can trigger again
  useEffect(() => {
    return () => {
      lastConsumedPromptRef.current = null;
    };
  }, []);

  // Handle incoming prompts from router state (guaranteed strictly once per prompt)
  useEffect(() => {
    const prompt = location.state?.initialPrompt;
    if (prompt && prompt !== lastConsumedPromptRef.current) {
      lastConsumedPromptRef.current = prompt;
      try {
        window.history.replaceState({}, document.title);
        if (location.state) {
          location.state.initialPrompt = null;
        }
      } catch {
        // ignore
      }
      handleSend(prompt, selectedLanguageRef.current);
    }
  }, [location.state, handleSend]);

  const handleClearChat = () => {
    handleStop();
    setMessages([]);
    setSessionId(null);
    setError(null);
    localStorage.removeItem(STORAGE_KEY);
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

  const handleExportJson = () => {
    if (messages.length === 0) return;
    const sessionData = {
      app: 'BIS AI Assistant',
      version: '2.6 Hybrid Core',
      exported_at: new Date().toISOString(),
      engine: selectedEngine,
      domain_filter: selectedDomain,
      session_id: sessionId,
      total_messages: messages.length,
      conversation: messages.map((m) => ({
        role: m.role,
        content: m.content,
        timestamp: m.timestamp,
        citations: m.citations || [],
        thinking_time_ms: m.thinking?.thoughtTimeMs || null,
        query_category: m.query_category || null,
      })),
    };
    const blob = new Blob([JSON.stringify(sessionData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `bis-ai-session-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex-1 flex flex-col justify-between overflow-hidden relative h-full min-h-0">
      
      {/* Dynamic Modern Top Bar */}
      <header className="px-4 sm:px-6 py-2.5 border-b border-[var(--border-color)] bg-[var(--bg-primary)]/90 backdrop-blur-md flex items-center justify-between z-10 shrink-0 gap-2">
        <div className="flex items-center gap-2 min-w-0">
          {/* Dynamic Model & Engine Selector */}
          <ModelSelectorDropdown
            selectedEngine={selectedEngine}
            onSelectEngine={setSelectedEngine}
          />

          {/* Dynamic RAG Regulatory Scope Filter */}
          <DomainFilterDropdown
            selectedDomain={selectedDomain}
            onSelectDomain={setSelectedDomain}
          />
        </div>

        {/* Dynamic Actions Menu */}
        <div className="flex items-center gap-2 shrink-0">
          <ConversationMenu
            messages={messages}
            onExportMarkdown={handleExportChat}
            onExportJson={handleExportJson}
            onClearChat={handleClearChat}
            autoExpandThinking={autoExpandThinking}
            onToggleAutoExpandThinking={() => setAutoExpandThinking((prev) => !prev)}
          />
        </div>
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
              <ChatMessage
                key={i}
                message={msg}
                onAskAboutClause={(q) => handleSend(q, selectedLanguage)}
                autoExpandThinking={autoExpandThinking}
              />
            ))}

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

      {/* Bottom Input Container */}
      <div className="shrink-0">
        <ChatInput
          onSend={handleSend}
          disabled={loading && !isStreaming}
          isGenerating={isStreaming}
          onStop={handleStop}
          selectedLanguage={selectedLanguage}
          onLanguageChange={setSelectedLanguage}
        />
      </div>

    </div>
  );
}
