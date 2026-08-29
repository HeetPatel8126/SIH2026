import { useState, useEffect, useCallback } from 'react';
import { Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import ChatPage from './pages/ChatPage';
import SearchStandardsPage from './pages/SearchStandardsPage';
import CertificationGuidePage from './pages/CertificationGuidePage';
import AboutPage from './pages/AboutPage';
import { fetchHealth } from './services/api';

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [health, setHealth] = useState(null);
  const [healthStatus, setHealthStatus] = useState('checking'); // checking | online | offline

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
    <>
      {/* Mobile header */}
      <div className="mobile-header">
        <button className="hamburger-btn" onClick={() => setSidebarOpen(true)} aria-label="Open menu">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
        <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>BIS AI Assistant</span>
      </div>

      <div className="app-layout">
        {/* Overlay for mobile */}
        <div className={`sidebar-overlay ${sidebarOpen ? 'open' : ''}`} onClick={() => setSidebarOpen(false)} />

        <Sidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          healthStatus={healthStatus}
          health={health}
        />

        <main className="app-main">
          <Routes>
            <Route path="/" element={<ChatPage />} />
            <Route path="/search" element={<SearchStandardsPage />} />
            <Route path="/certification" element={<CertificationGuidePage />} />
            <Route path="/about" element={<AboutPage health={health} healthStatus={healthStatus} />} />
          </Routes>
        </main>
      </div>
    </>
  );
}
