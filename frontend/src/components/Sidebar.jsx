import { NavLink, useNavigate } from 'react-router-dom';
import {
  MessageSquarePlus,
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

  const navItems = [
    { to: '/', label: 'AI Standards Advisor', icon: MessageSquarePlus, exact: true },
    { to: '/search', label: 'Standards Catalog', icon: BookOpen },
    { to: '/certification', label: 'Certification & Schemes', icon: Award },
    { to: '/labs', label: 'Testing Laboratories', icon: FlaskConical },
    { to: '/consumer', label: 'HUID & Consumer Hub', icon: ShieldCheck },
    { to: '/about', label: 'System & Architecture', icon: Info },
  ];

  const recentPresets = [
    { text: 'Drinking water permissible limits under IS 10500' },
    { text: 'LED high-bay luminaire CRS registration process' },
    { text: 'How to verify 6-digit Gold Hallmark HUID' },
  ];

  const handleStartNewChat = () => {
    navigate('/');
    if (onClose) onClose();
  };

  const handlePresetClick = (preset) => {
    navigate('/', { state: { initialPrompt: preset } });
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
      <div className="space-y-4">
        
        {/* Brand Header */}
        <div className="flex items-center justify-between px-2 py-1">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-md bg-[var(--accent-terracotta)] text-white flex items-center justify-center font-bold text-xs shadow-xs">
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
          className="w-full bg-[var(--bg-card)] hover:bg-[var(--bg-card-elevated)] border border-[var(--border-color)] hover:border-[var(--border-hover)] text-[var(--text-primary)] font-medium px-3.5 py-2.5 rounded-xl text-xs flex items-center justify-between shadow-2xs transition"
        >
          <span className="flex items-center gap-2">
            <MessageSquarePlus size={15} className="text-[var(--accent-terracotta)]" />
            <span>Start new chat</span>
          </span>
          <kbd className="text-[10px] text-[var(--text-muted)] bg-[var(--bg-sidebar)] border border-[var(--border-color)] px-1.5 py-0.5 rounded font-mono">
            ⌘K
          </kbd>
        </button>

        {/* Primary Navigation List */}
        <div className="space-y-0.5">
          <div className="text-[10px] font-semibold text-[var(--text-muted)] px-2 py-1 font-mono uppercase tracking-wider">
            Knowledge Base
          </div>

          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.exact}
                onClick={onClose}
                className={({ isActive }) => `
                  flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-xs font-medium transition
                  ${
                    isActive
                      ? 'bg-[var(--bg-card)] text-[var(--text-primary)] font-semibold shadow-2xs border border-[var(--border-color)]'
                      : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-card)]/50'
                  }
                `}
              >
                <Icon size={15} className="shrink-0 text-[var(--accent-terracotta)]" />
                <span className="truncate">{item.label}</span>
              </NavLink>
            );
          })}
        </div>

        {/* Recent Presets / Starters */}
        <div className="space-y-1 pt-1">
          <div className="text-[10px] font-semibold text-[var(--text-muted)] px-2 py-1 font-mono uppercase tracking-wider flex items-center justify-between">
            <span>Recent Queries</span>
            <span className="text-[9px] font-normal text-[var(--text-muted)]">Quick Launch</span>
          </div>

          {recentPresets.map((preset, idx) => (
            <button
              key={idx}
              onClick={() => handlePresetClick(preset.text)}
              className="w-full text-left px-2.5 py-1.5 rounded-lg text-xs text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-card)]/60 cursor-pointer truncate transition flex items-center justify-between group"
            >
              <span className="truncate pr-1">{preset.text}</span>
              <ChevronRight size={12} className="text-[var(--text-muted)] opacity-0 group-hover:opacity-100 transition shrink-0" />
            </button>
          ))}
        </div>

      </div>

      {/* Footer Section: Health Status, Theme Toggle & Official Portal Link */}
      <div className="pt-3 border-t border-[var(--border-color)] space-y-2 text-xs">
        
        {/* Backend Live Telemetry Badge */}
        <div className="flex items-center justify-between px-2 py-1 text-[11px] text-[var(--text-muted)]">
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
            className="flex items-center gap-2 p-1.5 px-2.5 rounded-lg text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-card)] border border-transparent hover:border-[var(--border-color)] transition text-xs font-medium"
          >
            {theme === 'dark' ? <Sun size={14} className="text-amber-400" /> : <Moon size={14} className="text-slate-600" />}
            <span>{theme === 'dark' ? 'Light mode' : 'Dark mode'}</span>
          </button>

          <a
            href="https://www.services.bis.gov.in"
            target="_blank"
            rel="noreferrer"
            className="text-[var(--text-muted)] hover:text-[var(--text-primary)] p-1.5 rounded-lg transition"
            title="Official BIS Portal"
          >
            <ExternalLink size={14} />
          </a>
        </div>

      </div>
    </aside>
  );
}
