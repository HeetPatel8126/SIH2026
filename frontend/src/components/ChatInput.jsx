import { useState, useRef, useEffect } from 'react';
import { ArrowUp, Square, Mic, MicOff } from 'lucide-react';
import LanguageDropdown from './LanguageDropdown';
import PromptLibraryDropdown from './PromptLibraryDropdown';

const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'हिंदी (Hindi)' },
  { code: 'ta', label: 'தமிழ் (Tamil)' },
  { code: 'te', label: 'తెలుగు (Telugu)' },
  { code: 'mr', label: 'मराठी (Marathi)' },
  { code: 'bn', label: 'বাংলা (Bengali)' },
  { code: 'gu', label: 'ગુજરાતી (Gujarati)' }
];

export default function ChatInput({
  onSend,
  disabled,
  selectedLanguage,
  onLanguageChange,
  isGenerating = false,
  onStop = () => {},
}) {
  const [text, setText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const textareaRef = useRef(null);
  const recognitionRef = useRef(null);

  /* Auto-resize textarea */
  useEffect(() => {
    const ta = textareaRef.current;
    if (ta) {
      ta.style.height = 'auto';
      ta.style.height = Math.min(ta.scrollHeight, 160) + 'px';
    }
  }, [text]);

  /* Web Speech API initialization */
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = selectedLanguage === 'hi' ? 'hi-IN' : 'en-IN';

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setText((prev) => (prev ? `${prev} ${transcript}` : transcript));
        setIsListening(false);
      };

      recognition.onerror = () => {
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }
  }, [selectedLanguage]);

  const toggleSpeechRecognition = () => {
    if (!recognitionRef.current) {
      alert('Speech recognition is not supported by your browser. Please use Chrome, Edge, or Safari.');
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch {
        setIsListening(false);
      }
    }
  };

  const handleSubmit = () => {
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed, selectedLanguage);
    setText('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto px-4 sm:px-6 pb-5 pt-2">
      <div className="bg-[var(--bg-input)] border border-[var(--border-color)] focus-within:border-[var(--accent-terracotta)] focus-within:ring-2 focus-within:ring-[var(--accent-terracotta)]/20 rounded-2xl p-3 shadow-card transition-all duration-200 space-y-2">
        
        {/* Text Input Area */}
        <textarea
          ref={textareaRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything about Indian Standards, ISI Mark, Gold HUID, Lab Testing, or Grievances..."
          disabled={disabled && !isGenerating}
          rows={1}
          className="w-full bg-transparent resize-none border-none outline-none text-xs sm:text-sm text-[var(--text-primary)] placeholder-[var(--text-muted)] max-h-40 overflow-y-auto leading-relaxed"
        />

        {/* Action Controls Bar */}
        <div className="flex items-center justify-between pt-1 border-t border-[var(--border-color)]/50">
          
          <div className="flex items-center gap-2">
            {/* Dynamic Searchable Language Popover */}
            <LanguageDropdown
              selectedLanguage={selectedLanguage}
              onSelect={onLanguageChange}
              disabled={disabled}
            />

            {/* Dynamic BIS Regulatory Prompts Library */}
            <PromptLibraryDropdown
              onSelectPrompt={(query) => {
                setText(query);
                if (textareaRef.current) {
                  textareaRef.current.focus();
                }
              }}
              disabled={disabled}
            />

            {/* Voice Input Mic */}
            <button
              type="button"
              onClick={toggleSpeechRecognition}
              disabled={disabled}
              className={`p-1.5 rounded-lg border transition ${
                isListening
                  ? 'bg-rose-500 text-white border-rose-600 animate-pulse'
                  : 'bg-[var(--bg-sidebar)] border-[var(--border-color)] text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
              }`}
              title={isListening ? 'Listening… click to stop' : 'Voice Input (Speech-to-Text)'}
            >
              {isListening ? <MicOff size={13} /> : <Mic size={13} />}
            </button>
          </div>

          <div className="flex items-center gap-3">
            {/* Real-time Character Counter */}
            {text.length > 0 && (
              <span className="text-[10px] font-mono text-[var(--text-muted)] hidden sm:inline">
                {text.length} chars
              </span>
            )}

            {/* Submit / Stop Action */}
            {isGenerating ? (
              <button
                type="button"
                onClick={onStop}
                className="p-2 rounded-xl bg-rose-500 hover:bg-rose-600 text-white transition shadow-xs flex items-center justify-center transform hover:scale-105"
                title="Stop generating"
              >
                <Square size={14} fill="currentColor" />
              </button>
            ) : (
              <button
                type="button"
                onClick={handleSubmit}
                disabled={disabled || !text.trim()}
                id="send-button"
                className={`p-2 rounded-xl transition shadow-xs flex items-center justify-center ${
                  !text.trim() || disabled
                    ? 'bg-[var(--bg-sidebar)] text-[var(--text-muted)] cursor-not-allowed'
                    : 'bg-[var(--accent-terracotta)] hover:bg-[var(--accent-terracotta-hover)] text-white transform hover:scale-105'
                }`}
                title="Send query (Enter)"
              >
                <ArrowUp size={15} />
              </button>
            )}
          </div>

        </div>

      </div>

      <p className="text-[11px] text-center text-[var(--text-muted)] mt-2">
        BIS AI answers are grounded in official Bureau of Indian Standards gazette notifications.
      </p>
    </div>
  );
}
