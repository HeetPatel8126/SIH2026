import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Award, ChevronRight, Shield, Layers, FileCheck, Factory, Beaker, BadgeCheck, CheckCircle2 } from 'lucide-react';
import Citations from '../components/Citations';
import { getCertificationGuide } from '../services/api';

const SCHEMES = [
  {
    id: 'ISI',
    name: 'ISI Mark (Scheme I)',
    badge: 'Product Certification',
    icon: Award,
    desc: 'Mandatory and voluntary conformity for domestic manufacturers ensuring consistent quality & safety.',
    sampleQuery: 'How do I apply for ISI Mark certification for domestic electrical appliances?'
  },
  {
    id: 'CRS',
    name: 'CRS Scheme',
    badge: 'Electronics & IT (MeitY)',
    icon: Shield,
    desc: 'Self-declaration of conformity based on testing in BIS-recognized labs for IT, telecom, and solar products.',
    sampleQuery: 'What is the CRS registration procedure for IT products and power adapters?'
  },
  {
    id: 'FMCS',
    name: 'FMCS (Foreign Mfrs)',
    badge: 'Foreign Manufacturers',
    icon: Factory,
    desc: 'Scheme enabling overseas manufacturers to use the standard ISI Mark on products exported to India.',
    sampleQuery: 'What are the requirements for foreign manufacturers under the FMCS scheme?'
  },
  {
    id: 'Hallmark',
    name: 'Gold & Silver Hallmark',
    badge: 'Precious Metals',
    icon: Award,
    desc: 'Mandatory purity certification for gold jewelry with 6-digit alphanumeric HUID stamped at AHCs.',
    sampleQuery: 'What is the mandatory gold hallmarking process and how does an Assaying Centre issue HUID?'
  },
  {
    id: 'SchemeX',
    name: 'Scheme X',
    badge: 'Heavy Machinery & Pressure',
    icon: Layers,
    desc: 'Simplified conformity assessment for heavy machinery, boilers, transformers, and industrial gear.',
    sampleQuery: 'Explain the BIS Scheme X certification process for heavy capital goods.'
  },
  {
    id: 'ECOMark',
    name: 'ECO Mark',
    badge: 'Eco-Friendly Goods',
    icon: CheckCircle2,
    desc: 'Ecolabeling scheme for consumer products meeting environmental criteria alongside quality standards.',
    sampleQuery: 'What are the prerequisites for obtaining an ECO Mark certification on consumer products?'
  }
];

const DEFAULT_STEPS = [
  {
    step: 1,
    title: 'Standard Identification & Product Readiness',
    desc: 'Identify the applicable Indian Standard (IS Code) and ensure manufacturing setup meets in-house test capabilities prescribed in the Scheme of Inspection and Testing (SIT).'
  },
  {
    step: 2,
    title: 'Online Application on Manakonline Portal',
    desc: 'Submit application form along with manufacturing details, test equipment list, calibration certificates, and initial application fees on the BIS Manakonline portal.'
  },
  {
    step: 3,
    title: 'Independent Sample Testing',
    desc: 'Product test samples are tested either in a BIS laboratory or NABL accredited BIS-recognized laboratory to verify complete compliance with the standard.'
  },
  {
    step: 4,
    title: 'Factory Inspection & Audit',
    desc: 'A designated BIS Inspecting Officer conducts a physical or hybrid audit of the manufacturing premises, testing facilities, and quality control systems.'
  },
  {
    step: 5,
    title: 'Grant of Certification License (CM/L Number)',
    desc: 'Upon successful inspection and compliant test reports, BIS grants the Certificate of Conformity and CM/L license number with authorization to affix the ISI mark.'
  }
];

export default function CertificationGuidePage() {
  const [selectedScheme, setSelectedScheme] = useState('ISI');
  const [query, setQuery] = useState('How do I apply for ISI Mark certification for domestic electrical appliances?');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSchemeClick = (scheme) => {
    setSelectedScheme(scheme.id);
    setQuery(scheme.sampleQuery);
  };

  const handleSubmit = async (e) => {
    e?.preventDefault();
    if (!query.trim() || loading) return;
    setLoading(true);
    setError(null);

    try {
      const data = await getCertificationGuide({
        query: query.trim(),
        scheme: selectedScheme || null,
      });
      setResult(data);
    } catch (err) {
      setError(err.message || 'Request failed. Displaying standard procedural guidelines.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 overflow-y-auto min-h-0 p-4 sm:p-8 max-w-6xl w-full mx-auto space-y-6">
      
      {/* Page Header */}
      <div className="space-y-1">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-[var(--bg-card)] border border-[var(--border-color)] flex items-center justify-center text-[var(--accent-terracotta)]">
            <Award size={16} />
          </div>
          <h1 className="text-xl sm:text-2xl font-bold text-[var(--text-primary)] tracking-tight">
            BIS Certification Schemes &amp; Process Navigator
          </h1>
        </div>
        <p className="text-xs sm:text-sm text-[var(--text-muted)] leading-relaxed">
          Explore official BIS conformity schemes (ISI Mark, CRS, FMCS, Hallmarking) and 5-stage licensing roadmaps.
        </p>
      </div>

      {/* Scheme Selector Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {SCHEMES.map((s) => {
          const Icon = s.icon;
          const isActive = selectedScheme === s.id;
          return (
            <div
              key={s.id}
              onClick={() => handleSchemeClick(s)}
              className={`p-3.5 rounded-xl border flex flex-col justify-between cursor-pointer transition shadow-2xs space-y-2 ${
                isActive
                  ? 'bg-[var(--bg-card)] border-[var(--accent-terracotta)] ring-2 ring-[var(--accent-terracotta)]/20'
                  : 'bg-[var(--bg-card)] border-[var(--border-color)] hover:border-[var(--border-hover)]'
              }`}
            >
              <div className="w-7 h-7 rounded-lg bg-[var(--bg-sidebar)] flex items-center justify-center text-[var(--accent-terracotta)]">
                <Icon size={15} />
              </div>
              <div>
                <div className="font-bold text-xs text-[var(--text-primary)]">{s.name}</div>
                <div className="text-[10px] text-[var(--text-muted)] font-mono truncate">{s.badge}</div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Guidance Search Box */}
      <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-4 sm:p-5 shadow-2xs">
        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            className="flex-1 bg-[var(--bg-sidebar)] border border-[var(--border-color)] focus:border-[var(--accent-terracotta)] rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-[var(--text-primary)] outline-none placeholder:text-[var(--text-muted)] transition"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about certification schemes, audit requirements, testing fees..."
            id="cert-query-input"
          />
          <button
            type="submit"
            className="bg-[var(--accent-terracotta)] hover:bg-[var(--accent-terracotta-hover)] text-white font-medium px-4 py-2.5 rounded-xl text-xs sm:text-sm transition flex items-center justify-center gap-1.5 shrink-0 shadow-xs cursor-pointer"
            disabled={loading || !query.trim()}
            id="cert-submit-btn"
          >
            {loading ? <span className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" /> : <ChevronRight size={15} />}
            <span>Get Scheme Guidance</span>
          </button>
        </form>
      </div>

      {error && (
        <div className="p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-300 text-xs">
          ⚠ {error}
        </div>
      )}

      {/* Dynamic Answer or Interactive Process Stepper */}
      {result ? (
        <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-5 sm:p-6 shadow-2xs space-y-4">
          {result.scheme_identified && (
            <span className="font-mono text-xs font-semibold px-2.5 py-1 rounded bg-[var(--bg-sidebar)] text-[var(--accent-terracotta)] border border-[var(--border-color)] inline-block">
              {result.scheme_identified}
            </span>
          )}

          <div className="claude-prose text-xs sm:text-sm text-[var(--text-primary)]">
            <ReactMarkdown>{result.answer}</ReactMarkdown>
          </div>

          {result.steps && result.steps.length > 0 && (
            <div className="pt-3 border-t border-[var(--border-color)] space-y-3">
              <h3 className="font-bold text-sm text-[var(--text-primary)]">
                Step-by-Step Procedure
              </h3>
              <div className="space-y-2.5">
                {result.steps.map((st, i) => (
                  <div key={i} className="flex items-start gap-3 p-3 rounded-xl bg-[var(--bg-sidebar)] border border-[var(--border-color)] text-xs">
                    <span className="w-5 h-5 rounded-full bg-[var(--accent-terracotta)] text-white font-bold text-[10px] flex items-center justify-center shrink-0 mt-0.5">
                      {i + 1}
                    </span>
                    <p className="text-[var(--text-primary)] leading-relaxed font-medium">{st}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          <Citations citations={result.citations} />
        </div>
      ) : (
        /* Visual Stepper Diagram */
        <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-5 sm:p-6 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-[var(--border-color)]">
            <h3 className="font-bold text-sm text-[var(--text-primary)]">
              Standard 5-Stage Licensing Flow ({selectedScheme})
            </h3>
            <span className="text-[10px] font-mono text-[var(--text-muted)]">BIS Manakonline Portal</span>
          </div>

          <div className="space-y-3">
            {DEFAULT_STEPS.map((st) => (
              <div key={st.step} className="flex items-start gap-3.5 p-3.5 rounded-xl bg-[var(--bg-sidebar)] border border-[var(--border-color)]">
                <span className="w-6 h-6 rounded-full bg-[var(--accent-terracotta)] text-white font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                  {st.step}
                </span>
                <div className="space-y-1">
                  <h4 className="font-bold text-xs sm:text-sm text-[var(--text-primary)]">{st.title}</h4>
                  <p className="text-xs text-[var(--text-muted)] leading-relaxed">{st.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Scheme Comparison Matrix */}
      <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-5 sm:p-6 shadow-2xs space-y-3">
        <h3 className="font-bold text-sm text-[var(--text-primary)]">
          Certification Schemes Comparison Matrix
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-[var(--bg-sidebar)] text-[var(--text-primary)] border-b border-[var(--border-color)]">
                <th className="p-3 font-semibold">Scheme</th>
                <th className="p-3 font-semibold">Target Products</th>
                <th className="p-3 font-semibold">Testing Mode</th>
                <th className="p-3 font-semibold">Factory Audit</th>
                <th className="p-3 font-semibold">Mark Issued</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--border-color)] text-[var(--text-secondary)]">
              <tr>
                <td className="p-3 font-semibold text-[var(--text-primary)]">ISI Mark (Scheme I)</td>
                <td className="p-3">Food, Steel, Appliances, Cement</td>
                <td className="p-3">In-house + BIS Lab</td>
                <td className="p-3">Mandatory Physical Audit</td>
                <td className="p-3 font-medium text-[var(--accent-terracotta)]">Standard ISI Mark</td>
              </tr>
              <tr>
                <td className="p-3 font-semibold text-[var(--text-primary)]">CRS (MeitY)</td>
                <td className="p-3">IT Goods, Laptops, Mobile, Solar</td>
                <td className="p-3">NABL / BIS Recognized Lab</td>
                <td className="p-3">Not Mandatory (Self-Dec)</td>
                <td className="p-3 font-medium text-blue-500">CRS R-Number Mark</td>
              </tr>
              <tr>
                <td className="p-3 font-semibold text-[var(--text-primary)]">FMCS</td>
                <td className="p-3">Foreign Manufactured Products</td>
                <td className="p-3">BIS Lab in India</td>
                <td className="p-3">Overseas Factory Audit</td>
                <td className="p-3 font-medium text-purple-500">ISI Mark with Foreign Tag</td>
              </tr>
              <tr>
                <td className="p-3 font-semibold text-[var(--text-primary)]">Hallmarking</td>
                <td className="p-3">Gold &amp; Silver Jewelry</td>
                <td className="p-3">AHC Fire Assay / XRF</td>
                <td className="p-3">Jeweler Registration Audit</td>
                <td className="p-3 font-medium text-amber-500">6-Digit HUID + BIS Triangle</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
