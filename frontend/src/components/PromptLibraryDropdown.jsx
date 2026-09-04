import { useState, useRef, useEffect } from 'react';
import { Sparkles, ChevronUp, ChevronDown, Droplet, ShieldCheck, Cpu, Utensils, FlaskConical, AlertTriangle, ArrowRight } from 'lucide-react';

const PRESET_CATEGORIES = [
  {
    id: 'standards',
    name: 'Standards & Limits',
    icon: Droplet,
    color: 'text-blue-500',
    prompts: [
      {
        title: 'Drinking Water Limits (IS 10500)',
        query: 'What is the permissible limit for TDS, Arsenic, and Lead in drinking water according to IS 10500:2012?',
        standard: 'IS 10500:2012'
      },
      {
        title: 'Stainless Steel Cookware (IS 2347)',
        query: 'What are the mandatory thermal shock and burst pressure testing requirements for pressure cookers under IS 2347:2017?',
        standard: 'IS 2347:2017'
      }
    ]
  },
  {
    id: 'gold',
    name: 'Hallmarking & HUID',
    icon: ShieldCheck,
    color: 'text-amber-500',
    prompts: [
      {
        title: 'Verify 6-digit Gold HUID',
        query: 'How do I verify a 6-digit alphanumeric HUID on 22-karat gold jewellery using the BIS Care mobile app?',
        standard: 'IS 1417:2016'
      },
      {
        title: 'Hallmarking Grades & Purity',
        query: 'What are the official gold purity grades (24K, 22K, 18K, 14K) recognized by BIS under IS 1417?',
        standard: 'IS 1417:2016'
      }
    ]
  },
  {
    id: 'crs',
    name: 'Electronics & CRS',
    icon: Cpu,
    color: 'text-indigo-500',
    prompts: [
      {
        title: 'LED Luminaire CRS Safety',
        query: 'What safety parameters and insulation tests are required for LED high-bay luminaires under IS 16102 (Part 1 & 2)?',
        standard: 'IS 16102:2012'
      },
      {
        title: 'Compulsory Registration Scheme (CRS)',
        query: 'What electronic and IT products fall under the BIS Compulsory Registration Scheme (CRS)?',
        standard: 'CRS Order 2021'
      }
    ]
  },
  {
    id: 'grievance',
    name: 'Labs & Consumer Rights',
    icon: AlertTriangle,
    color: 'text-rose-500',
    prompts: [
      {
        title: 'Lodge Substandard Product Complaint',
        query: 'How can a consumer file a grievance against a manufacturer selling counterfeit ISI mark goods?',
        standard: 'BIS Act 2016'
      },
      {
        title: 'Find Accredited Testing Labs',
        query: 'Where can I find BIS-recognized testing laboratories for chemical and mechanical testing in Mumbai and Pune?',
        standard: 'Lab Directory'
      }
    ]
  }
];

export default function PromptLibraryDropdown({ onSelectPrompt, disabled }) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeCategory, setActiveCategory] = useState(PRESET_CATEGORIES[0].id);
  const dropdownRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(e) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    }
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen]);

  useEffect(() => {
    function handleKeyDown(e) {
      if (e.key === 'Escape' && isOpen) {
        setIsOpen(false);
      }
    }
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  const currentCategory = PRESET_CATEGORIES.find((c) => c.id === activeCategory) || PRESET_CATEGORIES[0];

  return (
    <div className="relative inline-block text-left" ref={dropdownRef}>
      {/* Trigger Button */}
      <button
        type="button"
        onClick={() => !disabled && setIsOpen((prev) => !prev)}
        disabled={disabled}
        className={`
          flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-lg
          border transition-all duration-150 select-none shadow-2xs
          ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:border-[var(--accent-terracotta)]'}
          ${isOpen
            ? 'bg-[var(--bg-card-elevated)] border-[var(--accent-terracotta)] text-[var(--accent-terracotta)] ring-2 ring-[var(--accent-terracotta)]/20'
            : 'bg-[var(--bg-sidebar)] border border-[var(--border-color)] text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
          }
        `}
        title="Prompt Library & Presets"
      >
        <Sparkles size={12} className="text-[var(--accent-terracotta)]" />
        <span className="font-medium text-[11px] hidden sm:inline">Prompts</span>
        {isOpen ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
      </button>

      {/* Popover Card */}
      {isOpen && (
        <div className="absolute bottom-full left-0 mb-2 w-80 sm:w-96 bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl shadow-elevated z-50 overflow-hidden animate-in fade-in zoom-in-95 duration-100 backdrop-blur-md">
          {/* Header */}
          <div className="px-3.5 py-2.5 border-b border-[var(--border-color)] bg-[var(--bg-card-elevated)]/60 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles size={13} className="text-[var(--accent-terracotta)]" />
              <span className="font-semibold text-xs text-[var(--text-primary)]">
                BIS Regulatory Prompts
              </span>
            </div>
            <span className="text-[10px] text-[var(--text-muted)] font-mono">1-Click Run</span>
          </div>

          {/* Category Tabs */}
          <div className="flex items-center gap-1 p-1.5 border-b border-[var(--border-color)] bg-[var(--bg-sidebar)]/50 overflow-x-auto">
            {PRESET_CATEGORIES.map((cat) => {
              const Icon = cat.icon;
              const isActive = cat.id === activeCategory;
              return (
                <button
                  key={cat.id}
                  type="button"
                  onClick={() => setActiveCategory(cat.id)}
                  className={`
                    px-2.5 py-1 rounded-lg text-[11px] font-medium flex items-center gap-1.5 shrink-0 transition
                    ${isActive
                      ? 'bg-[var(--bg-card)] text-[var(--accent-terracotta)] shadow-2xs font-semibold'
                      : 'text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-card)]/50'
                    }
                  `}
                >
                  <Icon size={12} className={cat.color} />
                  <span>{cat.name}</span>
                </button>
              );
            })}
          </div>

          {/* Prompt List */}
          <div className="p-2 space-y-1.5 max-h-60 overflow-y-auto">
            {currentCategory.prompts.map((p, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => {
                  onSelectPrompt(p.query);
                  setIsOpen(false);
                }}
                className="w-full text-left p-2.5 rounded-xl border border-[var(--border-color)]/70 hover:border-[var(--accent-terracotta)] bg-[var(--bg-card)] hover:bg-[var(--bg-card-elevated)] transition group flex items-start justify-between gap-2 shadow-2xs"
              >
                <div className="space-y-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-xs text-[var(--text-primary)] group-hover:text-[var(--accent-terracotta)] transition">
                      {p.title}
                    </span>
                    <span className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-[var(--bg-sidebar)] border border-[var(--border-color)] text-[var(--text-muted)]">
                      {p.standard}
                    </span>
                  </div>
                  <p className="text-[11px] text-[var(--text-secondary)] line-clamp-2 leading-relaxed">
                    {p.query}
                  </p>
                </div>
                <ArrowRight size={13} className="text-[var(--text-muted)] group-hover:text-[var(--accent-terracotta)] group-hover:translate-x-0.5 transition shrink-0 mt-1" />
              </button>
            ))}
          </div>

          {/* Footer Info */}
          <div className="px-3.5 py-1.5 border-t border-[var(--border-color)]/70 bg-[var(--bg-card-elevated)]/30 text-[10px] text-[var(--text-muted)] flex items-center justify-between font-mono">
            <span>Select to fill & ask dynamically</span>
            <span>SIH 2026 Core</span>
          </div>
        </div>
      )}
    </div>
  );
}
