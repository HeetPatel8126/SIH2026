import { useState, useMemo } from 'react';
import { FlaskConical, MapPin, ShieldCheck, Phone, Mail, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const SAMPLE_LABS = [
  {
    id: 1,
    name: 'BIS Central Laboratory (CL)',
    type: 'BIS Owned & Operated',
    location: 'Sahibabad, Ghaziabad, Uttar Pradesh',
    state: 'Uttar Pradesh',
    discipline: 'Chemical, Mechanical, Electrical, Microbiology',
    testingScope: ['Packaged Drinking Water (IS 10500)', 'LPG Cylinders & Valves', 'Transformers & Cables', 'Paints & Chemicals'],
    accreditation: 'NABL Accredited ISO/IEC 17025',
    contact: { phone: '+91-120-2774044', email: 'cl@bis.gov.in' },
    status: 'Operational'
  },
  {
    id: 2,
    name: 'BIS Western Regional Office Laboratory (WROL)',
    type: 'BIS Regional Lab',
    location: 'Andheri (East), Mumbai, Maharashtra',
    state: 'Maharashtra',
    discipline: 'Electrical, Electronics, Chemical',
    testingScope: ['LED Bulbs & Luminaires (IS 16102)', 'Electric Irons & Appliances', 'Plastic Piping Systems', 'Jewelry Gold Assay'],
    accreditation: 'NABL Accredited ISO/IEC 17025',
    contact: { phone: '+91-22-28329295', email: 'wrol@bis.gov.in' },
    status: 'Operational'
  },
  {
    id: 3,
    name: 'BIS Southern Regional Office Laboratory (SROL)',
    type: 'BIS Regional Lab',
    location: 'Taramani, Chennai, Tamil Nadu',
    state: 'Tamil Nadu',
    discipline: 'Mechanical, Metallurgy, Textiles',
    testingScope: ['Steel & TMT Bars (IS 1786)', 'Textiles & PPE Kits', 'Cement & Concrete', 'Automotive Components'],
    accreditation: 'NABL Accredited ISO/IEC 17025',
    contact: { phone: '+91-44-22541442', email: 'srol@bis.gov.in' },
    status: 'Operational'
  },
  {
    id: 4,
    name: 'BIS Eastern Regional Office Laboratory (EROL)',
    type: 'BIS Regional Lab',
    location: 'Salt Lake City, Kolkata, West Bengal',
    state: 'West Bengal',
    discipline: 'Chemical, Food & Agri, Mechanical',
    testingScope: ['Tea & Agricultural Products', 'Jute & Packaging Goods', 'Domestic Gas Stoves', 'Pesticides & Fertilizers'],
    accreditation: 'NABL Accredited ISO/IEC 17025',
    contact: { phone: '+91-33-23207080', email: 'erol@bis.gov.in' },
    status: 'Operational'
  },
  {
    id: 5,
    name: 'BIS Northern Regional Office Laboratory (NROL)',
    type: 'BIS Regional Lab',
    location: 'Phase-VII, SAS Nagar, Mohali, Punjab',
    state: 'Punjab',
    discipline: 'Mechanical, Electronics, Chemical',
    testingScope: ['Solar Photovoltaic Modules', 'Agricultural Pumpsets', 'Wood & Plywood Products', 'Sanitary Appliances'],
    accreditation: 'NABL Accredited ISO/IEC 17025',
    contact: { phone: '+91-172-2270132', email: 'nrol@bis.gov.in' },
    status: 'Operational'
  },
  {
    id: 6,
    name: 'National Test House (NTH - Western Region)',
    type: 'BIS Recognized / Govt Lab',
    location: 'Marol, Andheri East, Mumbai, Maharashtra',
    state: 'Maharashtra',
    discipline: 'Electronics, IT Products, High Voltage Testing',
    testingScope: ['Smartphones & Tablets (CRS)', 'Power Adapters & Inverters', 'Batteries (IS 16046)', 'Server & Networking Gear'],
    accreditation: 'NABL & BIS Recognized Lab Scheme (LRS)',
    contact: { phone: '+91-22-28267230', email: 'nth-wr@gov.in' },
    status: 'Operational'
  },
  {
    id: 7,
    name: 'CPRI (Central Power Research Institute)',
    type: 'BIS Recognized Autonomous Lab',
    location: 'Sir C.V. Raman Road, Bengaluru, Karnataka',
    state: 'Karnataka',
    discipline: 'High Voltage Electrical & Power Electronics',
    testingScope: ['Distribution Transformers (IS 1180)', 'Electric Vehicle EV Chargers', 'Switchgear & Circuit Breakers'],
    accreditation: 'NABL & BIS Recognized',
    contact: { phone: '+91-80-22072210', email: 'cpri@nic.in' },
    status: 'Operational'
  }
];

const DISCIPLINES = ['All Disciplines', 'Electrical', 'Electronics', 'Chemical', 'Mechanical', 'Food & Agri', 'Textiles'];

export default function LabsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDiscipline, setSelectedDiscipline] = useState('All Disciplines');
  const [selectedState, setSelectedState] = useState('All');
  const navigate = useNavigate();

  const statesList = useMemo(() => {
    const set = new Set(SAMPLE_LABS.map((l) => l.state));
    return ['All', ...Array.from(set)];
  }, []);

  const filteredLabs = useMemo(() => {
    return SAMPLE_LABS.filter((lab) => {
      const matchesSearch =
        lab.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        lab.location.toLowerCase().includes(searchQuery.toLowerCase()) ||
        lab.testingScope.some((s) => s.toLowerCase().includes(searchQuery.toLowerCase()));

      const matchesDiscipline =
        selectedDiscipline === 'All Disciplines' ||
        lab.discipline.toLowerCase().includes(selectedDiscipline.toLowerCase());

      const matchesState = selectedState === 'All' || lab.state === selectedState;

      return matchesSearch && matchesDiscipline && matchesState;
    });
  }, [searchQuery, selectedDiscipline, selectedState]);

  const handleAskLabTesting = (lab, item) => {
    navigate('/', { state: { initialPrompt: `What is the testing procedure and required standard for ${item} at ${lab.name}?` } });
  };

  return (
    <div className="flex-1 overflow-y-auto min-h-0 p-4 sm:p-8 max-w-6xl w-full mx-auto space-y-6">
      
      {/* Page Header */}
      <div className="space-y-1">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-[var(--bg-card)] border border-[var(--border-color)] flex items-center justify-center text-[var(--accent-terracotta)]">
            <FlaskConical size={16} />
          </div>
          <h1 className="text-xl sm:text-2xl font-bold text-[var(--text-primary)] tracking-tight">
            BIS Recognized Testing Laboratories
          </h1>
        </div>
        <p className="text-xs sm:text-sm text-[var(--text-muted)] leading-relaxed">
          Locate accredited laboratories across India for product sample testing and compliance certification.
        </p>
      </div>

      {/* Search & Filter Controls */}
      <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-4 sm:p-5 shadow-2xs space-y-4">
        <div>
          <input
            type="text"
            className="w-full bg-[var(--bg-sidebar)] border border-[var(--border-color)] focus:border-[var(--accent-terracotta)] rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-[var(--text-primary)] outline-none placeholder:text-[var(--text-muted)] transition"
            placeholder="Search by lab name, city, or product (e.g. LED bulbs, drinking water, steel bars)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <div className="flex flex-wrap items-center justify-between gap-3 pt-1">
          <div className="flex flex-wrap items-center gap-1.5">
            {DISCIPLINES.map((d) => (
              <button
                key={d}
                type="button"
                className={`text-xs px-3 py-1.5 rounded-lg border transition font-medium cursor-pointer ${
                  selectedDiscipline === d
                    ? 'bg-[var(--bg-card-elevated)] border-[var(--accent-terracotta)] text-[var(--accent-terracotta)] font-semibold shadow-2xs'
                    : 'bg-[var(--bg-sidebar)] border-[var(--border-color)] text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
                }`}
                onClick={() => setSelectedDiscipline(d)}
              >
                {d}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-2 text-xs">
            <span className="text-[var(--text-muted)]">State:</span>
            <select
              value={selectedState}
              onChange={(e) => setSelectedState(e.target.value)}
              className="bg-[var(--bg-sidebar)] border border-[var(--border-color)] rounded-lg px-2.5 py-1 text-xs text-[var(--text-primary)] font-medium outline-none"
            >
              {statesList.map((st) => (
                <option key={st} value={st} className="bg-[var(--bg-card)] text-[var(--text-primary)]">
                  {st === 'All' ? 'All States' : st}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Lab Results Count */}
      <div className="text-xs text-[var(--text-muted)] font-mono">
        Showing {filteredLabs.length} testing laboratory facilities
      </div>

      {/* Labs Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredLabs.map((lab) => (
          <div
            key={lab.id}
            className="bg-[var(--bg-card)] border border-[var(--border-color)] hover:border-[var(--border-hover)] rounded-2xl p-5 flex flex-col justify-between shadow-2xs space-y-4 transition group"
          >
            <div className="space-y-2.5">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-mono font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800/60 px-2.5 py-0.5 rounded">
                  {lab.type}
                </span>
                <span className="text-[11px] text-emerald-600 dark:text-emerald-400 font-semibold flex items-center gap-1">
                  <ShieldCheck size={13} /> {lab.status}
                </span>
              </div>

              <h3 className="font-bold text-base text-[var(--text-primary)] leading-snug group-hover:text-[var(--accent-terracotta)] transition">
                {lab.name}
              </h3>

              <div className="flex items-start gap-2 text-xs text-[var(--text-secondary)]">
                <MapPin size={14} className="shrink-0 text-[var(--accent-terracotta)] mt-0.5" />
                <span>{lab.location}</span>
              </div>

              <div className="text-xs text-[var(--text-muted)]">
                <strong className="text-[var(--text-primary)]">Disciplines:</strong> {lab.discipline}
              </div>

              <div className="space-y-1.5 pt-1">
                <div className="text-[10px] font-mono uppercase text-[var(--text-muted)] font-bold">
                  Primary Testing Scope
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {lab.testingScope.map((scope, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleAskLabTesting(lab, scope)}
                      className="text-[11px] px-2.5 py-1 rounded-md bg-[var(--bg-sidebar)] hover:bg-[var(--bg-card-elevated)] border border-[var(--border-color)] hover:border-[var(--accent-terracotta)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition cursor-pointer flex items-center gap-1"
                      title="Click to ask AI assistant"
                    >
                      <span>{scope}</span>
                      <span className="text-[var(--accent-terracotta)]">↗</span>
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-[var(--border-color)]/60 flex items-center justify-between text-xs">
              <div className="flex items-center gap-3 text-[11px] text-[var(--text-muted)]">
                <span className="flex items-center gap-1"><Phone size={12} /> {lab.contact.phone}</span>
                <span className="flex items-center gap-1"><Mail size={12} /> Email</span>
              </div>

              <button
                type="button"
                onClick={() => navigate('/', { state: { initialPrompt: `How can I submit product test samples to ${lab.name}?` } })}
                className="text-[var(--accent-terracotta)] hover:brightness-110 font-semibold flex items-center gap-1 transition cursor-pointer"
              >
                <span>Inquire AI</span>
                <ArrowRight size={13} />
              </button>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
