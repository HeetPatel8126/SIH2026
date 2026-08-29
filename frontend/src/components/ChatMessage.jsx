import ReactMarkdown from 'react-markdown';
import Citations from './Citations';

export default function ChatMessage({ message }) {
  const { role, content, citations, query_category, timestamp, processing_time_ms } = message;
  const isUser = role === 'user';

  return (
    <div className={`chat-message ${role}`}>
      <div className={`message-avatar ${role}`}>
        {isUser ? 'U' : 'B'}
      </div>

      <div className="message-body">
        <div className="message-content">
          {isUser ? (
            <p>{content}</p>
          ) : (
            <ReactMarkdown>{content}</ReactMarkdown>
          )}
        </div>

        {!isUser && (
          <>
            <div className="message-meta">
              {query_category && (
                <span className="message-category">{query_category}</span>
              )}
              {processing_time_ms != null && (
                <span>{processing_time_ms.toFixed(0)}ms</span>
              )}
              {timestamp && (
                <span>{new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
              )}
            </div>
            <Citations citations={citations} />
          </>
        )}

        {isUser && timestamp && (
          <div className="message-meta">
            <span>{new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
          </div>
        )}
      </div>
    </div>
  );
}
