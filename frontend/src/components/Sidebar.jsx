import { useState, useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  MessageSquarePlus,
  MessageSquare,
  BookOpen,
  Award,
  FlaskConical,
  ShieldCheck,
  Info,
  Sun,
  Moon,
  X,
  ExternalLink,
  ChevronRight,
  ChevronDown,
  Compass,
} from 'lucide-react';

export default function Sidebar({
  isOpen,
  onClose,
  healthStatus,
  health,
  theme,
  toggleTheme,
}) {
  const navigate = useNavigate();

  const [portalsOpen, setPortalsOpen] = useState(() => {
    try {
      return localStorage.getItem('bis_portals_open') !== 'false';
    } catch {
      return true;
    }
  });

  const [recentQueries, setRecentQueries] = useState([
    'Drinking water permissible limits under IS 10500',
    'LED high-bay luminaire CRS registration process',
    'How to verify 6-digit Gold Hallmark HUID',
  ]);

  // Read actual recent user queries from conversation history if available
  useEffect(() => {
    try {
      const saved = localStorage.getItem('bis_ai_conversation_history');
      if (saved) {
        const parsed = JSON.parse(saved);
        const userMsgs = parsed
          .filter((m) => m.role === 'user' && m.content && m.content.trim().length > 0)
          .map((m) => m.content.trim());
        
        const uniqueQueries = Array.from(new Set(userMsgs));
        if (uniqueQueries.length > 0) {
          setRecentQueries(uniqueQueries.slice(-4).reverse());
        }
      }
    } catch {
      // fallback to presets
    }
  }, [isOpen]);

  const togglePortals = () => {
    setPortalsOpen((prev) => {
      const next = !prev;
      try {
        localStorage.setItem('bis_portals_open', String(next));
      } catch {
        // ignore
      }
      return next;
    });
  };

  const referencePortals = [
    { to: '/search', label: 'Standards Catalog', icon: BookOpen },
    { to: '/certification', label: 'Certification Schemes', icon: Award },
    { to: '/labs', label: 'Testing Laboratories', icon: FlaskConical },
    { to: '/consumer', label: 'HUID & Consumer Hub', icon: ShieldCheck },
    { to: '/about', label: 'Architecture & Specs', icon: Info },
  ];

  const handleStartNewChat = () => {
    navigate('/');
    if (onClose) onClose();
  };

  const handleQueryClick = (queryText) => {
    navigate('/', { state: { initialPrompt: queryText } });
    if (onClose) onClose();
  };

  return (
    <aside
      className={`
        fixed md:static inset-y-0 left-0 z-50
        w-64 bg-[var(--bg-sidebar)] border-r border-[var(--border-color)]
        flex flex-col justify-between p-3.5
        transition-transform duration-200 ease-in-out
        ${isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
      `}
    >
      {/* Top Section & Scrollable Area */}
      <div className="flex-1 flex flex-col min-h-0 space-y-3">
        
        {/* Brand Header */}
        <div className="flex items-center justify-between px-1.5 py-0.5 shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-[var(--accent-terracotta)] text-white flex items-center justify-center font-bold text-xs shadow-xs">
              B
            </div>
            <div>
              <span className="font-bold text-sm tracking-tight text-[var(--text-primary)]">BIS Assistant</span>
              <div className="text-[10px] text-[var(--text-muted)] font-mono">Manak AI · SIH 2026</div>
            </div>
          </div>

          <button
            onClick={onClose}
            className="md:hidden p-1.5 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-card)] transition"
            aria-label="Close sidebar"
          >
            <X size={18} />
          </button>
        </div>

        {/* Start New Chat Action */}
        <button
          onClick={handleStartNewChat}
          className="w-full bg-[var(--bg-card)] hover:bg-[var(--bg-card-elevated)] border border-[var(--border-color)] hover:border-[var(--border-hover)] text-[var(--text-primary)] font-medium px-3 py-2 rounded-xl text-xs flex items-center justify-between shadow-2xs transition shrink-0 cursor-pointer"
        >
          <span className="flex items-center gap-2">
            <MessageSquarePlus size={14} className="text-[var(--accent-terracotta)]" />
            <span>Start new chat</span>
          </span>
          <kbd className="text-[10px] text-[var(--text-muted)] bg-[var(--bg-sidebar)] border border-[var(--border-color)] px-1.5 py-0.5 rounded font-mono">
            ⌘K
          </kbd>
        </button>

        {/* Scrollable Middle Navigation Content */}
        <div className="flex-1 overflow-y-auto pr-1 -mr-1 space-y-3.5 min-h-0 scrollbar-none">
          
          {/* Main AI Chat Nav Item */}
          <div>
            <NavLink
              to="/"
              end
              onClick={onClose}
              className={({ isActive }) => `
                flex items-center gap-2 px-2.5 py-1.5 rounded-lg text-xs font-medium transition
                ${
                  isActive
                    ? 'bg-[var(--bg-card)] text-[var(--text-primary)] font-semibold shadow-2xs border border-[var(--border-color)]'
                    : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-card)]/50'
                }
              `}
            >
              <MessageSquare size={13} className="shrink-0 text-[var(--accent-terracotta)]" />
              <span className="truncate">AI Standards Advisor</span>
            </NavLink>
          </div>

          {/* Recent Queries / Quick Starters */}
          <div className="space-y-1">
            <div className="text-[10px] font-semibold text-[var(--text-muted)] px-2 py-0.5 font-mono uppercase tracking-wider flex items-center justify-between">
              <span>Recent Queries</span>
              <span className="text-[9px] font-normal text-[var(--text-muted)]">Quick Launch</span>
            </div>

            <div className="space-y-0.5">
              {recentQueries.map((text, idx) => (
                <button
                  key={idx}
                  onClick={() => handleQueryClick(text)}
                  className="w-full text-left px-2 py-1.5 rounded-lg text-xs text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-card)]/60 cursor-pointer truncate transition flex items-center justify-between group"
                  title={text}
                >
                  <span className="truncate pr-1 text-[11.5px] leading-tight">{text}</span>
                  <ChevronRight size={11} className="text-[var(--text-muted)] opacity-0 group-hover:opacity-100 transition shrink-0" />
                </button>
              ))}
            </div>
          </div>

          {/* Collapsible Reference Portals Hub */}
          <div className="space-y-1 pt-1 border-t border-[var(--border-color)]/60">
            <button
              type="button"
              onClick={togglePortals}
              className="w-full flex items-center justify-between px-2 py-1 text-[10px] font-semibold text-[var(--text-muted)] hover:text-[var(--text-primary)] font-mono uppercase tracking-wider transition group cursor-pointer select-none"
            >
              <span className="flex items-center gap-1.5">
                <Compass size={11} className="text-[var(--text-muted)] group-hover:text-[var(--accent-terracotta)] transition" />
                <span>Reference Portals</span>
              </span>
              <div className="flex items-center gap-1">
                <span className="text-[9px] font-mono text-[var(--text-muted)]">{referencePortals.length}</span>
                <ChevronDown
                  size={11}
                  className={`text-[var(--text-muted)] transition-transform duration-200 ${portalsOpen ? 'rotate-180' : ''}`}
                />
              </div>
            </button>

            {portalsOpen && (
              <div className="space-y-0.5 pt-0.5">
                {referencePortals.map((item) => {
                  const Icon = item.icon;
                  return (
                    <NavLink
                      key={item.to}
                      to={item.to}
                      onClick={onClose}
                      className={({ isActive }) => `
                        group flex items-center gap-2 px-2.5 py-1.5 rounded-lg text-xs transition
                        ${
                          isActive
                            ? 'bg-[var(--bg-card)] text-[var(--text-primary)] font-medium border border-[var(--border-color)]/80 shadow-2xs'
                            : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-card)]/40'
                        }
                      `}
                    >
                      <Icon
                        size={13}
                        className="shrink-0 text-[var(--text-muted)] group-hover:text-[var(--accent-terracotta)] transition"
                      />
                      <span className="truncate">{item.label}</span>
                    </NavLink>
                  );
                })}
              </div>
            )}
          </div>

        </div>

      </div>

      {/* Footer Section: Health Status, Theme Toggle & Official Portal Link */}
      <div className="pt-2.5 border-t border-[var(--border-color)] space-y-1.5 text-xs shrink-0">
        
        {/* Backend Live Telemetry Badge */}
        <div className="flex items-center justify-between px-2 py-0.5 text-[11px] text-[var(--text-muted)]">
          <span className="flex items-center gap-1.5">
            <span
              className={`w-2 h-2 rounded-full ${
                healthStatus === 'online'
                  ? 'bg-emerald-500 animate-pulse'
                  : healthStatus === 'checking'
                  ? 'bg-amber-400'
                  : 'bg-rose-500'
              }`}
            />
            <span className="font-mono capitalize">{healthStatus}</span>
          </span>
          <span className="text-[10px] font-mono text-[var(--text-muted)]">
            {health?.uptime_seconds ? `${Math.floor(health.uptime_seconds / 60)}m up` : 'RAG v2.6'}
          </span>
        </div>

        {/* Theme & User Profile Bar */}
        <div className="flex items-center justify-between px-1">
          <button
            onClick={toggleTheme}
            className="flex items-center gap-2 p-1.5 px-2 rounded-lg text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-card)] border border-transparent hover:border-[var(--border-color)] transition text-xs font-medium cursor-pointer"
          >
            {theme === 'dark' ? <Sun size={13} className="text-amber-400" /> : <Moon size={13} className="text-slate-600" />}
            <span>{theme === 'dark' ? 'Light mode' : 'Dark mode'}</span>
          </button>

          <a
            href="https://www.services.bis.gov.in"
            target="_blank"
            rel="noreferrer"
            className="text-[var(--text-muted)] hover:text-[var(--text-primary)] p-1.5 rounded-lg transition"
            title="Official BIS Portal"
          >
            <ExternalLink size={13} />
          </a>
        </div>

      </div>
    </aside>
  );
}
