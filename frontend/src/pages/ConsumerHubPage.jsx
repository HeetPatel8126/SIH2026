import { useState } from 'react';
import { ShieldAlert, CheckCircle2, AlertTriangle, Smartphone, PhoneCall, ArrowRight, Award, FileText } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function ConsumerHubPage() {
  const [huidInput, setHuidInput] = useState('');
  const [huidResult, setHuidResult] = useState(null);

  const [cmlInput, setCmlInput] = useState('');
  const [cmlResult, setCmlResult] = useState(null);

  const navigate = useNavigate();

  const handleVerifyHUID = (e) => {
    e.preventDefault();
    const clean = huidInput.trim().toUpperCase();
    if (!clean) return;

    // HUID is 6 alphanumeric characters
    const isAlphanumeric = /^[A-Z0-9]{6}$/.test(clean);

    if (isAlphanumeric) {
      setHuidResult({
        valid: true,
        code: clean,
        message: 'Valid HUID Format! A standard 6-digit alphanumeric Hallmark Unique ID consists of 6 alphanumeric characters stamped by an AHC (Assaying & Hallmarking Centre).',
        action: 'Verify official purity & jeweler registration in the BIS CARE App under "Verify HUID".'
      });
    } else {
      setHuidResult({
        valid: false,
        code: clean,
        message: 'Invalid HUID format. Authentic BIS HUID must be exactly 6 alphanumeric characters (e.g., A1B2C3, 7K9M2P).'
      });
    }
  };

  const handleVerifyCML = (e) => {
    e.preventDefault();
    const clean = cmlInput.trim();
    if (!clean) return;

    // CML is 7-8 digits
    const isDigits = /^\d{7,8}$/.test(clean);

    if (isDigits) {
      setCmlResult({
        valid: true,
        code: clean,
        message: `Valid CML Number Structure (${clean}). BIS License (CM/L) numbers are 7 or 8 digits printed directly under the standard ISI Mark.`
      });
    } else {
      setCmlResult({
        valid: false,
        code: clean,
        message: 'CM/L Number should consist of 7 or 8 digits. Check the number printed below the ISI mark.'
      });
    }
  };

  return (
    <div className="flex-1 overflow-y-auto min-h-0 p-4 sm:p-8 max-w-6xl w-full mx-auto space-y-8">
      
      {/* Page Header */}
      <div className="space-y-1">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-[var(--bg-card)] border border-[var(--border-color)] flex items-center justify-center text-[var(--accent-terracotta)]">
            <ShieldAlert size={16} />
          </div>
          <h1 className="text-xl sm:text-2xl font-bold text-[var(--text-primary)] tracking-tight">
            Consumer Rights &amp; Mark Verification Hub
          </h1>
        </div>
        <p className="text-xs sm:text-sm text-[var(--text-muted)] leading-relaxed">
          Verify BIS quality marks, check Gold Hallmark HUIDs, and understand consumer grievance procedures.
        </p>
      </div>

      {/* Verification Tool Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        
        {/* HUID Verifier */}
        <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-5 sm:p-6 shadow-2xs space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-[var(--bg-sidebar)] flex items-center justify-center text-[var(--accent-terracotta)]">
              <Award size={18} />
            </div>
            <div>
              <h3 className="font-bold text-sm text-[var(--text-primary)]">Gold Hallmark HUID Verifier</h3>
              <p className="text-[11px] text-[var(--text-muted)] font-mono">6-Digit Hallmark Unique ID</p>
            </div>
          </div>

          <form onSubmit={handleVerifyHUID} className="flex gap-2">
            <input
              type="text"
              placeholder="e.g. 8K2M9P"
              maxLength={6}
              value={huidInput}
              onChange={(e) => setHuidInput(e.target.value.toUpperCase())}
              className="flex-1 bg-[var(--bg-sidebar)] border border-[var(--border-color)] focus:border-[var(--accent-terracotta)] rounded-xl px-3.5 py-2 text-xs sm:text-sm text-[var(--text-primary)] font-mono uppercase outline-none"
            />
            <button
              type="submit"
              className="bg-[var(--accent-terracotta)] hover:bg-[var(--accent-terracotta-hover)] text-white font-medium px-4 py-2 rounded-xl text-xs sm:text-sm transition shadow-xs cursor-pointer"
            >
              Verify
            </button>
          </form>

          {huidResult && (
            <div className={`p-3.5 rounded-xl border text-xs flex items-start gap-2.5 ${
              huidResult.valid
                ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-300'
                : 'bg-rose-50 dark:bg-rose-950/40 border-rose-200 dark:border-rose-800 text-rose-800 dark:text-rose-300'
            }`}>
              {huidResult.valid ? <CheckCircle2 size={16} className="text-emerald-500 shrink-0 mt-0.5" /> : <AlertTriangle size={16} className="text-rose-500 shrink-0 mt-0.5" />}
              <div>
                <div className="font-semibold mb-0.5">{huidResult.message}</div>
                {huidResult.action && <div className="text-[11px] opacity-90">{huidResult.action}</div>}
              </div>
            </div>
          )}

          <div className="pt-2 border-t border-[var(--border-color)]/60 text-xs text-[var(--text-secondary)] space-y-1">
            <strong className="text-[var(--text-primary)]">Hallmark Composition:</strong>
            <ul className="list-disc pl-4 space-y-0.5 text-[11px] text-[var(--text-muted)]">
              <li>BIS Standard Logo (Triangle)</li>
              <li>Purity in Karat &amp; Fineness (e.g. 22K916, 18K750)</li>
              <li>6-digit alphanumeric HUID stamped by Assaying Center</li>
            </ul>
          </div>
        </div>

        {/* ISI CM/L Verifier */}
        <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-5 sm:p-6 shadow-2xs space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-[var(--bg-sidebar)] flex items-center justify-center text-blue-500">
              <FileText size={18} />
            </div>
            <div>
              <h3 className="font-bold text-sm text-[var(--text-primary)]">ISI Mark (CM/L) Verifier</h3>
              <p className="text-[11px] text-[var(--text-muted)] font-mono">Certification License 7-8 Digit Number</p>
            </div>
          </div>

          <form onSubmit={handleVerifyCML} className="flex gap-2">
            <input
              type="text"
              placeholder="e.g. 8400192384"
              maxLength={8}
              value={cmlInput}
              onChange={(e) => setCmlInput(e.target.value.replace(/\D/g, ''))}
              className="flex-1 bg-[var(--bg-sidebar)] border border-[var(--border-color)] focus:border-[var(--accent-terracotta)] rounded-xl px-3.5 py-2 text-xs sm:text-sm text-[var(--text-primary)] font-mono outline-none"
            />
            <button
              type="submit"
              className="bg-[var(--accent-terracotta)] hover:bg-[var(--accent-terracotta-hover)] text-white font-medium px-4 py-2 rounded-xl text-xs sm:text-sm transition shadow-xs cursor-pointer"
            >
              Check
            </button>
          </form>

          {cmlResult && (
            <div className={`p-3.5 rounded-xl border text-xs flex items-start gap-2.5 ${
              cmlResult.valid
                ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-300'
                : 'bg-rose-50 dark:bg-rose-950/40 border-rose-200 dark:border-rose-800 text-rose-800 dark:text-rose-300'
            }`}>
              {cmlResult.valid ? <CheckCircle2 size={16} className="text-emerald-500 shrink-0 mt-0.5" /> : <AlertTriangle size={16} className="text-rose-500 shrink-0 mt-0.5" />}
              <div className="font-semibold">{cmlResult.message}</div>
            </div>
          )}

          <div className="pt-2 border-t border-[var(--border-color)]/60 text-xs text-[var(--text-secondary)] space-y-1">
            <strong className="text-[var(--text-primary)]">Packaging Inspection Guide:</strong>
            <p className="text-[11px] text-[var(--text-muted)] leading-relaxed">
              Look for the ISI mark with the standard code on top (e.g. <code>IS 10500</code>) and the manufacturer license CM/L-XXXXXXXX directly below.
            </p>
          </div>
        </div>

      </div>

      {/* Consumer Grievance Actions */}
      <div className="space-y-4">
        <h2 className="font-bold text-base text-[var(--text-primary)]">
          How to Lodge a Consumer Grievance / Misuse of Mark
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-5 shadow-2xs space-y-2.5">
            <div className="flex items-center gap-2 text-[var(--accent-terracotta)] font-bold text-xs sm:text-sm">
              <Smartphone size={16} />
              <span>1. BIS CARE Mobile App</span>
            </div>
            <p className="text-xs text-[var(--text-muted)] leading-relaxed">
              Download the official <strong>BIS CARE App</strong> on Android &amp; iOS. Navigate to <em>"Complaints"</em> to upload photos of counterfeit ISI marks, substandard goods, or un-hallmarked gold.
            </p>
          </div>

          <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-5 shadow-2xs space-y-2.5">
            <div className="flex items-center gap-2 text-emerald-600 dark:text-emerald-400 font-bold text-xs sm:text-sm">
              <PhoneCall size={16} />
              <span>2. National Consumer Helpline</span>
            </div>
            <p className="text-xs text-[var(--text-muted)] leading-relaxed">
              Dial <strong>1915</strong> (Toll-Free) or send SMS to <strong>8800001915</strong> to file consumer grievances with the Ministry of Consumer Affairs.
            </p>
          </div>

          <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-5 shadow-2xs space-y-2.5 flex flex-col justify-between">
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-blue-500 font-bold text-xs sm:text-sm">
                <ShieldAlert size={16} />
                <span>3. Ask AI Legal &amp; Clause Guidance</span>
              </div>
              <p className="text-xs text-[var(--text-muted)] leading-relaxed">
                Unsure of the penalties for fake ISI mark usage under Section 14/15 of BIS Act 2016? Ask our AI advisor directly.
              </p>
            </div>

            <button
              onClick={() => navigate('/', { state: { initialPrompt: 'What are the legal penalties for manufacturing or selling products with a fake ISI mark under the BIS Act 2016?' } })}
              className="text-[var(--accent-terracotta)] hover:brightness-110 text-xs font-semibold flex items-center gap-1 cursor-pointer pt-2"
            >
              <span>Ask AI about BIS Penalties</span>
              <ArrowRight size={13} />
            </button>
          </div>
        </div>
      </div>

    </div>
  );
}
