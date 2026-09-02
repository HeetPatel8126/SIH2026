import { Factory, Gem, ShieldAlert, FlaskConical, ArrowRight, Sparkles } from 'lucide-react';

const PERSONAS = [
  {
    icon: Factory,
    title: 'MSMEs & Manufacturers',
    description: 'Find required Indian Standards, mandatory QCOs, and licensing steps for your products.',
    prompt: 'I manufacture LED bulbs and luminaires. Which Indian Standards and BIS certification schemes apply to my product?'
  },
  {
    icon: Gem,
    title: 'Gold & Jewelry Buyers',
    description: 'Verify 6-digit HUID Hallmarking, gold karat purities, and how to spot counterfeit marks.',
    prompt: 'How do I verify a 6-digit HUID hallmark on gold jewelry, and what are the 3 mandatory marks?'
  },
  {
    icon: ShieldAlert,
    title: 'Consumer Complaints & Safety',
    description: 'Report fake ISI marks, substandard goods, and understand your rights under BIS Act 2016.',
    prompt: 'How can I report a manufacturer using a counterfeit ISI mark on domestic gas stoves?'
  },
  {
    icon: FlaskConical,
    title: 'Standards & Lab Testing',
    description: 'Search permissible chemical limits, sample testing parameters, and NABL accredited labs.',
    prompt: 'What are the key chemical and microbiological testing parameters for packaged drinking water under IS 10500?'
  }
];

export default function WelcomeScreen({ onQuestionClick }) {
  return (
    <div className="max-w-3xl w-full mx-auto px-4 sm:px-6 py-8 sm:py-12 flex flex-col items-center text-center space-y-6">
      
      {/* Top National Emblem Avatar */}
      <div className="w-12 h-12 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-color)] flex items-center justify-center text-2xl shadow-sm">
        🏛️
      </div>

      {/* Greeting Title */}
      <div className="space-y-2">
        <h1 className="text-2xl sm:text-3xl font-bold text-[var(--text-primary)] tracking-tight">
          BIS Standards &amp; Certification Advisor
        </h1>
        <p className="text-xs sm:text-sm text-[var(--text-muted)] max-w-xl mx-auto leading-relaxed">
          Your intelligent guide to <strong>Indian Standards (IS Codes), BIS Certification Schemes, &amp; Consumer Protection</strong>. Grounded in official Government of India gazette notifications.
        </p>
      </div>

      {/* Topic Chips */}
      <div className="flex flex-wrap gap-2 justify-center max-w-2xl pt-1">
        {['ISI Mark (Scheme I)', 'CRS Registration', 'Gold Hallmarking (HUID)', 'IS 10500 Drinking Water', 'Foreign Mfrs (FMCS)', 'BIS CARE Redressal'].map((topic) => (
          <button
            key={topic}
            onClick={() => onQuestionClick(`Tell me about ${topic}`)}
            className="text-xs font-medium px-3 py-1.5 rounded-full bg-[var(--bg-card)] hover:bg-[var(--bg-card-elevated)] border border-[var(--border-color)] hover:border-[var(--accent-terracotta)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition shadow-2xs flex items-center gap-1.5 cursor-pointer"
          >
            <Sparkles size={12} className="text-[var(--accent-terracotta)]" />
            <span>{topic}</span>
          </button>
        ))}
      </div>

      {/* Persona Starter Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 w-full text-left pt-3">
        {PERSONAS.map((p, idx) => {
          const Icon = p.icon;
          return (
            <div
              key={idx}
              onClick={() => onQuestionClick(p.prompt)}
              className="bg-[var(--bg-card)] hover:bg-[var(--bg-card-elevated)] border border-[var(--border-color)] hover:border-[var(--accent-terracotta)] rounded-2xl p-4 sm:p-5 flex flex-col justify-between cursor-pointer transition shadow-2xs group space-y-3"
            >
              <div className="space-y-2">
                <div className="flex items-center gap-2.5">
                  <div className="w-7 h-7 rounded-lg bg-[var(--bg-sidebar)] border border-[var(--border-color)] flex items-center justify-center text-[var(--accent-terracotta)] shrink-0">
                    <Icon size={15} />
                  </div>
                  <h3 className="font-semibold text-xs sm:text-sm text-[var(--text-primary)] group-hover:text-[var(--accent-terracotta)] transition">
                    {p.title}
                  </h3>
                </div>

                <p className="text-xs text-[var(--text-muted)] leading-relaxed">
                  {p.description}
                </p>
              </div>

              <div className="pt-2 border-t border-[var(--border-color)]/60 flex items-center justify-between text-xs text-[var(--accent-terracotta)] font-medium">
                <span>Ask sample query</span>
                <ArrowRight size={13} className="group-hover:translate-x-1 transition" />
              </div>
            </div>
          );
        })}
      </div>

    </div>
  );
}
