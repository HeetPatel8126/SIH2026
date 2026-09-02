import { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Copy, Check, Star, ArrowRight, BookOpen, X } from 'lucide-react';
import { searchStandards } from '../services/api';

const POPULAR_STANDARDS = [
  {
    is_code: 'IS 10500:2012',
    title: 'Drinking Water — Specification (Second Revision)',
    summary: 'Specifies acceptable and permissible quality limits for physical, chemical, and microbiological parameters in drinking water.',
    sector: 'Food & Water'
  },
  {
    is_code: 'IS 16102 (Part 1):2012',
    title: 'Self-Ballasted LED Lamps for General Lighting Services',
    summary: 'Safety and performance requirements for LED bulbs, covers mandatory CRS registration requirements under MeitY QCO.',
    sector: 'Electronics & IT'
  },
  {
    is_code: 'IS 2347:2017',
    title: 'Domestic Pressure Cookers — Specification',
    summary: 'Safety requirements, material composition, bursting pressure, and thermal efficiency for domestic pressure cookers (Mandatory ISI Mark).',
    sector: 'Mechanical'
  },
  {
    is_code: 'IS 1786:2008',
    title: 'High Strength Deformed Steel Bars & Wires for Concrete Reinforcement',
    summary: 'Covers physical and chemical properties of TMT steel bars (Fe 415, Fe 500, Fe 550) used in building construction.',
    sector: 'Civil & Construction'
  },
  {
    is_code: 'IS 1417:2016',
    title: 'Gold and Gold Alloys, Plat & Silver — Grades & Hallmarking',
    summary: 'Prescribes standards of fineness, karat grades (24K, 22K, 18K, 14K), and hallmark assaying specifications.',
    sector: 'Metallurgy & Jewelry'
  },
  {
    is_code: 'IS 694:2010',
    title: 'PVC Insulated Cables for Working Voltages up to 1100V',
    summary: 'Electrical wiring cables, insulation thickness, spark testing, and conductor resistance specifications.',
    sector: 'Electrical'
  }
];

const SECTORS = ['All Sectors', 'Electronics & IT', 'Food & Water', 'Civil & Construction', 'Mechanical', 'Electrical', 'Metallurgy & Jewelry'];

export default function SearchStandardsPage() {
  const [query, setQuery] = useState('');
  const [selectedSector, setSelectedSector] = useState('All Sectors');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [copiedCode, setCopiedCode] = useState(null);
  const [bookmarks, setBookmarks] = useState(() => {
    try {
      const saved = localStorage.getItem('bis_bookmarked_standards');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });
  const [showBookmarksOnly, setShowBookmarksOnly] = useState(false);

  const navigate = useNavigate();

  // Persist bookmarks
  useEffect(() => {
    try {
      localStorage.setItem('bis_bookmarked_standards', JSON.stringify(bookmarks));
    } catch {
      // ignore
    }
  }, [bookmarks]);

  const toggleBookmark = (standard) => {
    setBookmarks((prev) => {
      const exists = prev.some((b) => b.is_code === standard.is_code);
      if (exists) {
        return prev.filter((b) => b.is_code !== standard.is_code);
      } else {
        return [...prev, standard];
      }
    });
  };

  const handleCopyCode = (code) => {
    navigator.clipboard.writeText(code);
    setCopiedCode(code);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  const handleSearch = async (e) => {
    e?.preventDefault();
    if (!query.trim() || loading) return;
    setLoading(true);
    setError(null);

    try {
      const data = await searchStandards({ query: query.trim(), top_k: 12 });
      setResults(data);
    } catch (err) {
      setError(err.message || 'Search failed. Falling back to curated catalog.');
    } finally {
      setLoading(false);
    }
  };

  const displayedList = useMemo(() => {
    if (showBookmarksOnly) {
      return bookmarks;
    }

    if (results && results.results && results.results.length > 0) {
      return results.results;
    }

    return POPULAR_STANDARDS.filter((s) => {
      const matchesSector = selectedSector === 'All Sectors' || s.sector === selectedSector;
      const matchesQuery =
        !query.trim() ||
        s.is_code.toLowerCase().includes(query.toLowerCase()) ||
        s.title.toLowerCase().includes(query.toLowerCase()) ||
        s.summary.toLowerCase().includes(query.toLowerCase());

      return matchesSector && matchesQuery;
    });
  }, [results, query, selectedSector, showBookmarksOnly, bookmarks]);

  const handleAskAIAboutStandard = (item) => {
    navigate('/', {
      state: {
        initialPrompt: `Can you explain the key requirements, testing parameters, and certification process for Indian Standard ${item.is_code} (${item.title})?`
      }
    });
  };

  return (
    <div className="flex-1 overflow-y-auto min-h-0 p-4 sm:p-8 max-w-6xl w-full mx-auto space-y-6">
      
      {/* Page Header */}
      <div className="space-y-1">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-[var(--bg-card)] border border-[var(--border-color)] flex items-center justify-center text-[var(--accent-terracotta)]">
            <Search size={16} />
          </div>
          <h1 className="text-xl sm:text-2xl font-bold text-[var(--text-primary)] tracking-tight">
            Indian Standards Catalog &amp; Finder
          </h1>
        </div>
        <p className="text-xs sm:text-sm text-[var(--text-muted)] leading-relaxed">
          Search over 21,000+ Bureau of Indian Standards (IS Codes), product safety requirements, and Quality Control Orders.
        </p>
      </div>

      {/* Hero Search Box */}
      <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-4 sm:p-5 shadow-2xs space-y-4">
        <form className="flex items-center gap-2" onSubmit={handleSearch}>
          <div className="relative flex-1">
            <input
              type="text"
              className="w-full bg-[var(--bg-sidebar)] border border-[var(--border-color)] focus:border-[var(--accent-terracotta)] rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-[var(--text-primary)] outline-none placeholder:text-[var(--text-muted)] transition"
              value={query}
              onChange={(e) => {
                setQuery(e.target.value);
                if (!e.target.value.trim()) setResults(null);
              }}
              placeholder="Search by product (e.g. drinking water, pressure cooker, LED bulbs) or IS code (IS 10500)..."
              id="standards-search-input"
            />
            {query && (
              <button
                type="button"
                className="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--text-muted)] hover:text-[var(--text-primary)]"
                onClick={() => { setQuery(''); setResults(null); }}
                title="Clear search"
              >
                <X size={15} />
              </button>
            )}
          </div>

          <button
            type="submit"
            className="bg-[var(--accent-terracotta)] hover:bg-[var(--accent-terracotta-hover)] text-white font-medium px-4 py-2.5 rounded-xl text-xs sm:text-sm transition flex items-center gap-2 shrink-0 shadow-xs cursor-pointer"
            disabled={loading || !query.trim()}
            id="standards-search-btn"
          >
            {loading ? <span className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" /> : <Search size={14} />}
            <span>Search</span>
          </button>
        </form>

        {/* Sector Filter Chips */}
        <div className="flex flex-wrap items-center justify-between gap-2 pt-1">
          <div className="flex flex-wrap items-center gap-1.5">
            {SECTORS.map((sec) => (
              <button
                key={sec}
                type="button"
                className={`text-xs px-3 py-1.5 rounded-lg border transition font-medium cursor-pointer ${
                  selectedSector === sec && !showBookmarksOnly
                    ? 'bg-[var(--bg-card-elevated)] border-[var(--accent-terracotta)] text-[var(--accent-terracotta)] font-semibold shadow-2xs'
                    : 'bg-[var(--bg-sidebar)] border-[var(--border-color)] text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
                }`}
                onClick={() => {
                  setSelectedSector(sec);
                  setShowBookmarksOnly(false);
                }}
              >
                {sec}
              </button>
            ))}
          </div>

          <button
            type="button"
            className={`text-xs px-3 py-1.5 rounded-lg border flex items-center gap-1.5 transition cursor-pointer font-medium ${
              showBookmarksOnly
                ? 'bg-[var(--bg-card-elevated)] border-[var(--accent-terracotta)] text-[var(--accent-terracotta)] font-semibold'
                : 'bg-[var(--bg-sidebar)] border-[var(--border-color)] text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
            }`}
            onClick={() => setShowBookmarksOnly(!showBookmarksOnly)}
          >
            <Star size={13} fill={showBookmarksOnly ? 'var(--accent-terracotta)' : 'none'} />
            <span>Saved ({bookmarks.length})</span>
          </button>
        </div>
      </div>

      {error && (
        <div className="p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-300 text-xs">
          ⚠ {error}
        </div>
      )}

      {/* Results Header */}
      <div className="flex items-center justify-between text-xs text-[var(--text-muted)] font-mono">
        <span>
          {showBookmarksOnly
            ? `Viewing ${bookmarks.length} saved standard${bookmarks.length !== 1 ? 's' : ''}`
            : `Showing ${displayedList.length} relevant standard${displayedList.length !== 1 ? 's' : ''}`}
        </span>
      </div>

      {/* Grid of Standard Cards */}
      {displayedList.length === 0 ? (
        <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-12 text-center space-y-3">
          <BookOpen size={36} className="mx-auto text-[var(--text-muted)]" />
          <h3 className="font-semibold text-sm text-[var(--text-primary)]">No matching Indian Standards found</h3>
          <p className="text-xs text-[var(--text-muted)] max-w-sm mx-auto">
            Try searching by alternative product names or click another sector filter above.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {displayedList.map((item, idx) => {
            const isBookmarked = bookmarks.some((b) => b.is_code === item.is_code);
            return (
              <div
                key={idx}
                className="bg-[var(--bg-card)] border border-[var(--border-color)] hover:border-[var(--border-hover)] rounded-2xl p-5 flex flex-col justify-between shadow-2xs space-y-4 transition group"
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs font-bold text-[var(--accent-terracotta)] bg-[var(--bg-sidebar)] px-2.5 py-1 rounded-md border border-[var(--border-color)]">
                      {item.is_code}
                    </span>
                    
                    <div className="flex items-center gap-1">
                      <button
                        type="button"
                        className="p-1.5 rounded-md hover:bg-[var(--bg-sidebar)] text-[var(--text-muted)] hover:text-[var(--text-primary)] transition"
                        onClick={() => handleCopyCode(item.is_code)}
                        title="Copy IS Code"
                      >
                        {copiedCode === item.is_code ? <Check size={14} className="text-emerald-500" /> : <Copy size={14} />}
                      </button>
                      <button
                        type="button"
                        className="p-1.5 rounded-md hover:bg-[var(--bg-sidebar)] text-[var(--text-muted)] hover:text-[var(--text-primary)] transition"
                        onClick={() => toggleBookmark(item)}
                        title={isBookmarked ? 'Remove bookmark' : 'Bookmark standard'}
                      >
                        <Star size={14} fill={isBookmarked ? 'var(--accent-terracotta)' : 'none'} className={isBookmarked ? 'text-[var(--accent-terracotta)]' : ''} />
                      </button>
                    </div>
                  </div>

                  <h3 className="font-bold text-sm text-[var(--text-primary)] leading-snug group-hover:text-[var(--accent-terracotta)] transition">
                    {item.title}
                  </h3>

                  {item.summary && (
                    <p className="text-xs text-[var(--text-secondary)] leading-relaxed line-clamp-3">
                      {item.summary}
                    </p>
                  )}
                </div>

                <div className="pt-3 border-t border-[var(--border-color)]/60 flex items-center justify-between text-xs">
                  <span className="text-[11px] font-mono text-[var(--text-muted)]">
                    {item.sector || 'Standard'}
                  </span>

                  <button
                    type="button"
                    onClick={() => handleAskAIAboutStandard(item)}
                    className="text-[var(--accent-terracotta)] hover:brightness-110 font-semibold flex items-center gap-1.5 transition cursor-pointer"
                  >
                    <span>Ask AI</span>
                    <ArrowRight size={13} />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

    </div>
  );
}
