const SUGGESTED_QUESTIONS = [
  'What is the Indian Standard for packaged drinking water?',
  'I manufacture pressure cookers, which standards apply?',
  "What's the difference between ISI Mark and CRS?",
  'How do I apply for a BIS license?',
];

export default function WelcomeScreen({ onQuestionClick }) {
  return (
    <div className="welcome-container">
      <div className="welcome-icon">B</div>
      <h2>BIS AI Assistant</h2>
      <p className="welcome-sub">
        Your AI-powered guide to Indian Standards and Bureau of Indian Standards services.
        Ask questions and get source-cited answers.
      </p>

      <div className="welcome-topics">
        {['Indian Standards', 'Certification', 'Hallmarking', 'Consumer Affairs', 'Lab Testing'].map((t) => (
          <span key={t} className="welcome-topic">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="20 6 9 17 4 12"/></svg>
            {t}
          </span>
        ))}
      </div>

      <div className="suggested-questions">
        {SUGGESTED_QUESTIONS.map((q) => (
          <button key={q} className="suggested-q-btn" onClick={() => onQuestionClick(q)}>
            <svg className="sq-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
            {q}
          </button>
        ))}
      </div>
    </div>
  );
}
