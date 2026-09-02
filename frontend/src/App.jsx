import { useState, useEffect, useCallback } from 'react';
import { Routes, Route } from 'react-router-dom';
import { Menu, Sun, Moon } from 'lucide-react';
import Sidebar from './components/Sidebar';
import ChatPage from './pages/ChatPage';
import SearchStandardsPage from './pages/SearchStandardsPage';
import CertificationGuidePage from './pages/CertificationGuidePage';
import LabsPage from './pages/LabsPage';
import ConsumerHubPage from './pages/ConsumerHubPage';
import AboutPage from './pages/AboutPage';
import { fetchHealth } from './services/api';

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [health, setHealth] = useState(null);
  const [healthStatus, setHealthStatus] = useState('checking'); // checking | online | offline
  const [theme, setTheme] = useState(() => localStorage.getItem('bis_theme') || 'dark');

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('bis_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  const checkHealth = useCallback(async () => {
    setHealthStatus('checking');
    try {
      const data = await fetchHealth();
      setHealth(data);
      setHealthStatus('online');
    } catch {
      setHealth(null);
      setHealthStatus('offline');
    }
  }, []);

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, [checkHealth]);

  return (
    <div className="h-screen h-[100dvh] w-full bg-[var(--bg-primary)] text-[var(--text-primary)] flex flex-col font-sans transition-colors duration-200 overflow-hidden">
      {/* Mobile Top Header */}
      <header className="md:hidden flex items-center justify-between px-4 py-3 bg-[var(--bg-sidebar)] border-b border-[var(--border-color)] z-40 shrink-0">
        <button
          onClick={() => setSidebarOpen(true)}
          className="p-2 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-card)] transition"
          aria-label="Open menu"
        >
          <Menu size={20} />
        </button>

        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-md bg-[var(--accent-terracotta)] text-white flex items-center justify-center font-bold text-xs">
            B
          </div>
          <span className="font-bold text-sm tracking-tight text-[var(--text-primary)]">BIS Assistant</span>
        </div>

        <button
          onClick={toggleTheme}
          className="p-2 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-card)] transition"
          aria-label="Toggle theme"
        >
          {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
        </button>
      </header>

      {/* Main Responsive Layout */}
      <div className="flex-1 flex overflow-hidden relative min-h-0">
        {/* Mobile backdrop overlay */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 bg-black/50 z-40 md:hidden backdrop-blur-xs transition-opacity"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        <Sidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          healthStatus={healthStatus}
          health={health}
          theme={theme}
          toggleTheme={toggleTheme}
        />

        <main className="flex-1 flex flex-col overflow-hidden relative bg-[var(--bg-primary)] min-h-0">
          <Routes>
            <Route path="/" element={<ChatPage />} />
            <Route path="/search" element={<SearchStandardsPage />} />
            <Route path="/certification" element={<CertificationGuidePage />} />
            <Route path="/labs" element={<LabsPage />} />
            <Route path="/consumer" element={<ConsumerHubPage />} />
            <Route path="/about" element={<AboutPage health={health} healthStatus={healthStatus} />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}
