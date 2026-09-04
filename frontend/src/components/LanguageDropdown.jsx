import { useState, useRef, useEffect } from 'react';
import { Globe, Check, Search, ChevronUp, ChevronDown } from 'lucide-react';

export const LANGUAGES = [
  { code: 'en', label: 'English', native: 'English', script: 'EN', flag: '🇬🇧', desc: 'Standard BIS technical English' },
  { code: 'hi', label: 'Hindi', native: 'हिन्दी', script: 'HI', flag: '🇮🇳', desc: 'मानक एवं विनियम हिंदी' },
  { code: 'ta', label: 'Tamil', native: 'தமிழ்', script: 'TA', flag: '🇮🇳', desc: 'இந்திய தரநிலைகள் தமிழ்' },
  { code: 'te', label: 'Telugu', native: 'తెలుగు', script: 'TE', flag: '🇮🇳', desc: 'భారతీయ ప్రమాణాలు తెలుగు' },
  { code: 'mr', label: 'Marathi', native: 'मराठी', script: 'MR', flag: '🇮🇳', desc: 'भारतीय मानके मराठी' },
  { code: 'bn', label: 'Bengali', native: 'বাংলা', script: 'BN', flag: '🇮🇳', desc: 'ভারতীয় মানক বাংলা' },
  { code: 'gu', label: 'Gujarati', native: 'ગુજરાતી', script: 'GU', flag: '🇮🇳', desc: 'ભારતીય ધોરણો ગુજરાતી' },
  { code: 'kn', label: 'Kannada', native: 'ಕನ್ನಡ', script: 'KN', flag: '🇮🇳', desc: 'ಭಾರತೀಯ ಗುಣಮಟ್ಟ ಕನ್ನಡ' },
  { code: 'pa', label: 'Punjabi', native: 'ਪੰਜਾਬੀ', script: 'PA', flag: '🇮🇳', desc: 'ਭਾਰਤੀ ਮਿਆਰ ਪੰਜਾਬੀ' },
  { code: 'ml', label: 'Malayalam', native: 'മലയാളം', script: 'ML', flag: '🇮🇳', desc: 'ഭാരതീയ മാനദണ്ഡങ്ങൾ മലയാളം' },
];

export default function LanguageDropdown({ selectedLanguage, onSelect, disabled }) {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState('');
  const dropdownRef = useRef(null);
  const searchInputRef = useRef(null);

  const activeLang = LANGUAGES.find((l) => l.code === selectedLanguage) || LANGUAGES[0];

  const filtered = LANGUAGES.filter((l) =>
    l.label.toLowerCase().includes(search.toLowerCase()) ||
    l.native.toLowerCase().includes(search.toLowerCase()) ||
    l.code.toLowerCase().includes(search.toLowerCase())
  );

  // Close when clicking outside
  useEffect(() => {
    function handleClickOutside(e) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    }
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      // Focus search input when opening
      setTimeout(() => searchInputRef.current?.focus(), 50);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen]);

  // Handle ESC key
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
        onClick={() => !disabled && setIsOpen((prev) => !prev)}
        disabled={disabled}
        className={`
          flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-lg
          border transition-all duration-150 select-none shadow-2xs
          ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:border-[var(--accent-terracotta)]'}
          ${isOpen
            ? 'bg-[var(--bg-card-elevated)] border-[var(--accent-terracotta)] text-[var(--accent-terracotta)] ring-2 ring-[var(--accent-terracotta)]/20'
            : 'bg-[var(--bg-sidebar)] border-[var(--border-color)] text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
          }
        `}
        title="Change Assistant Language"
      >
        <Globe size={13} className={isOpen ? 'text-[var(--accent-terracotta)]' : 'text-[var(--text-muted)]'} />
        <span className="font-medium text-[11px] flex items-center gap-1">
          <span>{activeLang.flag}</span>
          <span>{activeLang.native}</span>
        </span>
        {isOpen ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
      </button>

      {/* Popover Dropdown (Opens upward above input) */}
      {isOpen && (
        <div className="absolute bottom-full left-0 mb-2 w-72 bg-[var(--bg-card)] border border-[var(--border-color)] rounded-xl shadow-elevated z-50 overflow-hidden animate-in fade-in zoom-in-95 duration-100 backdrop-blur-md">
          {/* Header & Search */}
          <div className="p-2 border-b border-[var(--border-color)] bg-[var(--bg-card-elevated)]/50">
            <div className="relative flex items-center">
              <Search size={13} className="text-[var(--text-muted)] absolute left-2.5 pointer-events-none" />
              <input
                ref={searchInputRef}
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search languages..."
                className="w-full pl-8 pr-2.5 py-1 text-xs rounded-lg bg-[var(--bg-primary)] border border-[var(--border-color)] text-[var(--text-primary)] placeholder-[var(--text-muted)] focus:outline-none focus:border-[var(--accent-terracotta)]"
              />
            </div>
          </div>

          {/* Languages List */}
          <div className="max-h-56 overflow-y-auto p-1 space-y-0.5">
            {filtered.length === 0 ? (
              <div className="p-3 text-center text-xs text-[var(--text-muted)]">
                No matching languages found
              </div>
            ) : (
              filtered.map((lang) => {
                const isSelected = lang.code === selectedLanguage;
                return (
                  <button
                    key={lang.code}
                    type="button"
                    onClick={() => {
                      onSelect(lang.code);
                      setIsOpen(false);
                      setSearch('');
                    }}
                    className={`
                      w-full px-2.5 py-1.5 rounded-lg flex items-center justify-between text-left text-xs transition
                      ${isSelected
                        ? 'bg-[var(--accent-terracotta)]/10 text-[var(--accent-terracotta)] font-medium'
                        : 'hover:bg-[var(--bg-card-elevated)] text-[var(--text-primary)]'
                      }
                    `}
                  >
                    <div className="flex items-center gap-2 min-w-0">
                      <span className="text-sm shrink-0">{lang.flag}</span>
                      <div className="truncate">
                        <div className="flex items-center gap-1.5">
                          <span className="font-semibold text-[11px]">{lang.native}</span>
                          <span className="text-[10px] text-[var(--text-muted)] font-mono">({lang.label})</span>
                        </div>
                        <div className="text-[10px] text-[var(--text-muted)] truncate">{lang.desc}</div>
                      </div>
                    </div>

                    {isSelected && (
                      <Check size={14} className="text-[var(--accent-terracotta)] shrink-0 ml-1.5" />
                    )}
                  </button>
                );
              })
            )}
          </div>

          {/* Footer note */}
          <div className="px-3 py-1.5 border-t border-[var(--border-color)]/70 bg-[var(--bg-card-elevated)]/30 text-[10px] text-[var(--text-muted)] flex items-center justify-between font-mono">
            <span>Powered by Indic NLLB Core</span>
            <span>{LANGUAGES.length} Languages</span>
          </div>
        </div>
      )}
    </div>
  );
}
