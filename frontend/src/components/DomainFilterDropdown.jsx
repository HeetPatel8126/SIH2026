import { useState, useRef, useEffect } from 'react';
import { Filter, Check, ChevronDown, Layers, Droplets, ShieldCheck, Cpu, Utensils, FlaskConical } from 'lucide-react';

export const DOMAINS = [
  { id: 'all', label: 'All Regulatory Domains', icon: Layers, standard: 'Complete Corpus', desc: 'Queries across all indexed BIS standards & gazettes' },
  { id: 'water', label: 'Drinking Water & Quality', icon: Droplets, standard: 'IS 10500:2012', desc: 'TDS, microbial parameters, organoleptic limits & testing' },
  { id: 'hallmarking', label: 'Gold Hallmarking & HUID', icon: ShieldCheck, standard: 'IS 1417:2016', desc: '22K/18K/14K purity, 6-digit HUID verification & assays' },
  { id: 'electronics', label: 'Electronics CRS Safety', icon: Cpu, standard: 'IS 16102 (1 & 2)', desc: 'Smart lighting, LED luminaires, IT devices compulsory registration' },
  { id: 'appliances', label: 'Cookware & Domestic Goods', icon: Utensils, standard: 'IS 2347:2017', desc: 'Stainless steel pressure cookers, burst pressure, thermal tests' },
  { id: 'labs', label: 'Testing Laboratories & Schemes', icon: FlaskConical, standard: 'Lab Manual 2024', desc: 'NABL accredited test houses, regional labs & certification schemes' },
];

export default function DomainFilterDropdown({
  selectedDomain = 'all',
  onSelectDomain = () => {},
}) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  const active = DOMAINS.find((d) => d.id === selectedDomain) || DOMAINS[0];
  const ActiveIcon = active.icon;

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

  return (
    <div className="relative inline-block text-left" ref={dropdownRef}>
      {/* Trigger Button */}
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        className={`
          flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl border text-xs transition-all duration-150 shadow-2xs cursor-pointer select-none
          ${isOpen
            ? 'bg-[var(--bg-card-elevated)] border-[var(--accent-terracotta)] text-[var(--accent-terracotta)] ring-2 ring-[var(--accent-terracotta)]/20'
            : 'bg-[var(--bg-card)] border-[var(--border-color)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:border-[var(--border-hover)]'
          }
        `}
        title="Filter RAG Search Scope"
      >
        <Filter size={12} className={isOpen ? 'text-[var(--accent-terracotta)]' : 'text-[var(--text-muted)]'} />
        <span className="font-semibold text-xs text-[var(--text-primary)] hidden md:inline">
          {active.label}
        </span>
        <span className="font-semibold text-xs text-[var(--text-primary)] md:hidden">
          {active.standard}
        </span>
        <ChevronDown size={12} className={`text-[var(--text-muted)] transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {/* Popover Card */}
      {isOpen && (
        <div className="absolute top-full right-0 sm:left-0 mt-2 w-72 sm:w-80 bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl shadow-elevated z-50 overflow-hidden animate-in fade-in zoom-in-95 duration-100 backdrop-blur-md">
          {/* Header */}
          <div className="px-3.5 py-2.5 border-b border-[var(--border-color)] bg-[var(--bg-card-elevated)]/60 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Filter size={13} className="text-[var(--accent-terracotta)]" />
              <span className="font-semibold text-xs text-[var(--text-primary)]">
                Regulatory Retrieval Scope
              </span>
            </div>
            <span className="text-[10px] text-[var(--text-muted)] font-mono">ChromaDB Filter</span>
          </div>

          {/* Options */}
          <div className="p-1.5 space-y-0.5 max-h-64 overflow-y-auto">
            {DOMAINS.map((domain) => {
              const Icon = domain.icon;
              const isSelected = domain.id === selectedDomain;
              return (
                <button
                  key={domain.id}
                  type="button"
                  onClick={() => {
                    onSelectDomain(domain.id);
                    setIsOpen(false);
                  }}
                  className={`
                    w-full p-2 rounded-xl text-left transition flex items-center justify-between gap-2.5
                    ${isSelected
                      ? 'bg-[var(--accent-terracotta)]/10 text-[var(--accent-terracotta)] font-medium'
                      : 'hover:bg-[var(--bg-card-elevated)] text-[var(--text-primary)]'
                    }
                  `}
                >
                  <div className="flex items-center gap-2.5 min-w-0">
                    <div className={`p-1.5 rounded-lg shrink-0 ${isSelected ? 'bg-[var(--accent-terracotta)] text-white' : 'bg-[var(--bg-sidebar)] text-[var(--text-muted)]'}`}>
                      <Icon size={13} />
                    </div>
                    <div className="truncate">
                      <div className="flex items-center gap-1.5">
                        <span className="font-semibold text-xs">{domain.label}</span>
                        <span className="text-[9px] font-mono px-1 py-0.2 rounded bg-[var(--bg-sidebar)] border border-[var(--border-color)] text-[var(--text-muted)] shrink-0">
                          {domain.standard}
                        </span>
                      </div>
                      <div className="text-[10px] text-[var(--text-muted)] truncate">{domain.desc}</div>
                    </div>
                  </div>

                  {isSelected && (
                    <Check size={14} className="text-[var(--accent-terracotta)] shrink-0 ml-1" />
                  )}
                </button>
              );
            })}
          </div>

          {/* Footer */}
          <div className="px-3 py-1.5 border-t border-[var(--border-color)] bg-[var(--bg-card-elevated)]/30 text-[10px] text-[var(--text-muted)] flex items-center justify-between font-mono">
            <span>Filters ChromaDB vector collections</span>
            <span>Zero Hallucination</span>
          </div>
        </div>
      )}
    </div>
  );
}
