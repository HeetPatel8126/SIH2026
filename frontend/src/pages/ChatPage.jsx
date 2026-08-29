import { useState, useRef, useEffect, useCallback } from 'react';
import ChatMessage from '../components/ChatMessage';
import ChatInput from '../components/ChatInput';
import WelcomeScreen from '../components/WelcomeScreen';
import { sendChat } from '../services/api';

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => { scrollToBottom(); }, [messages, loading, scrollToBottom]);

  const handleSend = async (query) => {
    if (loading) return;

    const userMsg = {
      role: 'user',
      content: query,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    setError(null);

    try {
      const data = await sendChat({ query, session_id: sessionId });

      if (data.session_id) setSessionId(data.session_id);

      const assistantMsg = {
        role: 'assistant',
        content: data.answer,
        citations: data.citations,
        query_category: data.query_category,
        timestamp: data.timestamp,
        processing_time_ms: data.processing_time_ms,
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setError(err.message || 'Failed to get a response. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setSessionId(null);
    setError(null);
  };

  return (
    <div className="chat-container">
      {messages.length === 0 && !loading ? (
        <WelcomeScreen onQuestionClick={handleSend} />
      ) : (
        <div className="chat-messages">
          {messages.map((msg, i) => (
            <ChatMessage key={i} message={msg} />
          ))}

          {loading && (
            <div className="chat-message assistant">
              <div className="message-avatar assistant">B</div>
              <div className="message-body">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span /><span /><span />
                  </div>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div style={{ maxWidth: 820, margin: '0 auto' }}>
              <div className="error-banner">⚠ {error}</div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      )}

      {messages.length > 0 && (
        <div style={{ textAlign: 'center', padding: '4px 0' }}>
          <button
            onClick={handleNewChat}
            style={{
              background: 'none', border: 'none',
              color: 'var(--color-text-muted)', fontSize: '0.75rem',
              cursor: 'pointer', padding: '4px 12px',
            }}
          >
            ↻ New conversation
          </button>
        </div>
      )}

      <ChatInput onSend={handleSend} disabled={loading} />
    </div>
  );
}
