import { Activity, Server, Cpu, Layers, ShieldCheck, Zap } from 'lucide-react';

export default function AboutPage({ health, healthStatus }) {
  return (
    <div className="flex-1 overflow-y-auto min-h-0 p-4 sm:p-8 max-w-6xl w-full mx-auto space-y-6">
      
      {/* Page Header */}
      <div className="space-y-1">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-[var(--bg-card)] border border-[var(--border-color)] flex items-center justify-center text-[var(--accent-terracotta)]">
            <Activity size={16} />
          </div>
          <h1 className="text-xl sm:text-2xl font-bold text-[var(--text-primary)] tracking-tight">
            About BIS AI Assistant &amp; Architecture
          </h1>
        </div>
        <p className="text-xs sm:text-sm text-[var(--text-muted)] leading-relaxed">
          Smart India Hackathon 2026 · Ministry of Consumer Affairs, Food &amp; Public Distribution
        </p>
      </div>

      {/* Live System Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        
        <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-4 sm:p-5 shadow-2xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono font-bold uppercase text-[var(--text-muted)]">Backend</span>
            <Server size={15} className="text-[var(--accent-terracotta)]" />
          </div>
          <div className="flex items-center gap-2">
            <span className={`w-2.5 h-2.5 rounded-full ${healthStatus === 'online' ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`} />
            <span className="font-bold text-base text-[var(--text-primary)] capitalize">
              {healthStatus === 'online' ? 'Operational' : healthStatus === 'offline' ? 'Offline' : 'Connecting'}
            </span>
          </div>
          <div className="text-[11px] font-mono text-[var(--text-muted)]">
            FastAPI v{health?.version || '0.1.0'}
          </div>
        </div>

        <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-4 sm:p-5 shadow-2xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono font-bold uppercase text-[var(--text-muted)]">LLM Core</span>
            <Cpu size={15} className="text-blue-500" />
          </div>
          <div className="font-bold text-base text-blue-500">
            {health?.llm_provider ? health.llm_provider.toUpperCase() : 'OLLAMA'}
          </div>
          <div className="text-[11px] font-mono text-[var(--text-muted)] truncate">
            {health?.llm_model || 'llama3.1:8b'}
          </div>
        </div>

        <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-4 sm:p-5 shadow-2xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono font-bold uppercase text-[var(--text-muted)]">Vector Store</span>
            <Layers size={15} className="text-emerald-500" />
          </div>
          <div className="font-bold text-base text-emerald-500">
            ChromaDB
          </div>
          <div className="text-[11px] font-mono text-[var(--text-muted)] truncate">
            sentence-transformers
          </div>
        </div>

        <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-4 sm:p-5 shadow-2xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono font-bold uppercase text-[var(--text-muted)]">Service Uptime</span>
            <Zap size={15} className="text-amber-500" />
          </div>
          <div className="font-bold text-base text-amber-500">
            {health?.uptime_seconds != null ? `${Math.round(health.uptime_seconds)}s` : 'Active'}
          </div>
          <div className="text-[11px] font-mono text-[var(--text-muted)]">
            Zero hallucination guardrails
          </div>
        </div>

      </div>

      {/* Project Background & RAG Architecture Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        
        <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-5 sm:p-6 shadow-2xs space-y-3">
          <div className="flex items-center gap-2 text-[var(--accent-terracotta)] font-bold text-sm">
            <ShieldCheck size={18} />
            <span>Problem Statement &amp; Solution</span>
          </div>
          <p className="text-xs sm:text-sm text-[var(--text-secondary)] leading-relaxed">
            BIS publishes thousands of Indian Standards and operates complex certification schemes (ISI, CRS, FMCS, Hallmarking, ECO Mark). MSMEs, startups, and everyday consumers often struggle with obscure terminology, scattered PDFs, and dense guidelines.
          </p>
          <p className="text-xs sm:text-sm text-[var(--text-secondary)] leading-relaxed">
            <strong>The BIS AI Assistant</strong> bridges this gap through a verified <em>Retrieval-Augmented Generation (RAG)</em> pipeline. It grounds every response in authenticated BIS standards, providing clause-level citations and actionable next steps.
          </p>
        </div>

        <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-5 sm:p-6 shadow-2xs space-y-3">
          <div className="flex items-center gap-2 text-blue-500 font-bold text-sm">
            <Layers size={18} />
            <span>5-Stage RAG Pipeline</span>
          </div>
          <ol className="list-decimal pl-4 text-xs text-[var(--text-secondary)] space-y-1.5 leading-relaxed">
            <li><strong>Query Routing &amp; Intent:</strong> Classifies user intent into Standards, Certification, Hallmarking, Consumer Grievances, or Lab Testing.</li>
            <li><strong>Dense Retrieval:</strong> Converts queries into dense vectors and queries ChromaDB for top-k document passages.</li>
            <li><strong>Strict Prompt Guardrails:</strong> Instructs the LLM to formulate answers strictly using retrieved BIS passages.</li>
            <li><strong>Citation Extraction:</strong> Automatically links document titles, clause numbers, and similarity metrics.</li>
            <li><strong>Multilingual Support:</strong> Real-time handling of Hindi and English natural language queries.</li>
          </ol>
        </div>

      </div>

      {/* SIH Team Attribution Footer */}
      <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-5 text-center shadow-2xs">
        <p className="text-xs text-[var(--text-secondary)]">
          🏛️ Built with pride for <strong>Smart India Hackathon 2026 (SIH)</strong> · Team BIS Innovators · Ministry of Consumer Affairs, Food &amp; Public Distribution
        </p>
      </div>

    </div>
  );
}
