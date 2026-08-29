export default function AboutPage({ health, healthStatus }) {
  return (
    <>
      <div className="page-header">
        <h2>About BIS AI Assistant</h2>
        <p>AI-powered conversational assistant for Indian Standards &amp; BIS Services</p>
      </div>

      <div className="page-content">
        {/* System Status */}
        <div className="result-card" style={{ maxWidth: 600, marginBottom: 'var(--space-lg)' }}>
          <h3 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: 12, color: 'var(--color-primary)' }}>
            System Status
          </h3>
          <table style={{ width: '100%', fontSize: '0.85rem', borderCollapse: 'collapse' }}>
            <tbody>
              {[
                ['Backend', healthStatus === 'online' ? '● Online' : healthStatus === 'offline' ? '● Offline' : '● Checking…'],
                ['Version', health?.version || '—'],
                ['LLM Provider', health?.llm_provider || '—'],
                ['LLM Model', health?.llm_model || '—'],
                ['Uptime', health?.uptime_seconds != null ? `${Math.round(health.uptime_seconds)}s` : '—'],
              ].map(([label, value]) => (
                <tr key={label}>
                  <td style={{ padding: '6px 0', color: 'var(--color-text-secondary)', width: 140 }}>{label}</td>
                  <td style={{ padding: '6px 0', fontWeight: 500 }}>{value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* About */}
        <div className="result-card" style={{ maxWidth: 600, marginBottom: 'var(--space-lg)' }}>
          <h3 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: 12, color: 'var(--color-primary)' }}>
            What is this?
          </h3>
          <p style={{ fontSize: '0.85rem', lineHeight: 1.65, color: 'var(--color-text-secondary)', marginBottom: 12 }}>
            The BIS AI Assistant is an AI-powered conversational interface that helps MSMEs, startups, students, and consumers
            navigate Indian Standards and Bureau of Indian Standards (BIS) services. Every answer is grounded in real BIS
            documents with source citations — the assistant never fabricates IS codes, fees, or process steps.
          </p>
          <p style={{ fontSize: '0.85rem', lineHeight: 1.65, color: 'var(--color-text-secondary)' }}>
            Built using Retrieval-Augmented Generation (RAG): the system retrieves relevant passages from official BIS documents,
            then generates a clear, cited answer using a large language model.
          </p>
        </div>

        {/* Capabilities */}
        <div className="result-card" style={{ maxWidth: 600 }}>
          <h3 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: 12, color: 'var(--color-primary)' }}>
            Capabilities
          </h3>
          <ul style={{ fontSize: '0.85rem', lineHeight: 1.8, color: 'var(--color-text-secondary)', paddingLeft: 20 }}>
            <li>Answer questions about Indian Standards</li>
            <li>Recommend applicable standards from a product description</li>
            <li>Explain BIS certification schemes (ISI, CRS, FMCS, Hallmark, Scheme X, ECO Mark)</li>
            <li>Walk through certification processes step-by-step</li>
            <li>Answer consumer-related queries (complaints, verifying marks)</li>
            <li>Guide users on hallmarking</li>
            <li>Suggest relevant testing laboratories</li>
            <li>Support multilingual interaction</li>
          </ul>
        </div>

        <p style={{ marginTop: 'var(--space-xl)', fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
          Built for Smart India Hackathon 2026 · PS ID: SIH26107 · Ministry of Consumer Affairs, Food &amp; Public Distribution
        </p>
      </div>
    </>
  );
}
