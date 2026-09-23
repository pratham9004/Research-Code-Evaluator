import { useEffect, useState } from 'react';
import logo from '../../drawable/logo.png';
import Dashboard from './pages/Dashboard';
import SolveProblems from './pages/SolveProblems';
import Reports from './pages/Reports';
import ReportDetail from './pages/ReportDetail';
import DetailedReport from './pages/DetailedReport';
import ResearchGuide from './pages/ResearchGuide';
import AboutMethodology from './pages/AboutMethodology';
import ManageData from './pages/ManageData';
import { Report } from './types';

type Page = 'dashboard' | 'solve' | 'reports' | 'report' | 'detailed_report' | 'research_guide' | 'about_methodology' | 'manage_data';

type RouteState = {
  page: Page;
  reportId?: number | null;
};

const NAV_ITEMS: Array<{ key: Page; label: string; path: string; section: string }> = [
  { key: 'dashboard', label: 'Dashboard', path: '/dashboard', section: 'Workspace' },
  { key: 'solve', label: 'Solve Problems', path: '/solve-problems', section: 'Workspace' },
  { key: 'reports', label: 'Evaluations', path: '/reports', section: 'Workspace' },
  { key: 'research_guide', label: 'Research Guide', path: '/research-guide', section: 'Analysis' },
  { key: 'about_methodology', label: 'Methodology', path: '/about-methodology', section: 'Analysis' },
  { key: 'manage_data', label: 'Manage Data', path: '/manage-data', section: 'System' },
];

function getRouteFromLocation(): RouteState {
  const pathname = window.location.pathname || '/';
  const canonical = pathname === '/' ? '/dashboard' : pathname;

  if (canonical.startsWith('/reports/')) {
    const segments = canonical.split('/').filter(Boolean);
    const id = Number(segments[1]);

    if (segments[2] === 'detailed' && Number.isFinite(id)) {
      return { page: 'detailed_report', reportId: id };
    }
    if (Number.isFinite(id)) {
      return { page: 'report', reportId: id };
    }
    return { page: 'reports' };
  }

  const match = NAV_ITEMS.find((item) => item.path === canonical);
  return { page: match?.key ?? 'dashboard' };
}

export default function App() {
  const [route, setRoute] = useState<RouteState>(() => getRouteFromLocation());

  function navigate(path: string) {
    const next = path === '/' ? '/dashboard' : path;
    if (window.location.pathname !== next) {
      window.history.pushState({}, '', next);
    }
    setRoute(getRouteFromLocation());
  }

  useEffect(() => {
    if (window.location.pathname === '/' || window.location.pathname === '') {
      window.history.replaceState({}, '', '/dashboard');
      setRoute({ page: 'dashboard' });
    }

    const onPopState = () => setRoute(getRouteFromLocation());
    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, []);

  function handleReport(r: Report) {
    navigate(`/reports/${r.comparison_id}`);
  }

  function openReport(id: number) {
    navigate(`/reports/${id}`);
  }

  function openDetailedReport(id: number) {
    navigate(`/reports/${id}/detailed`);
  }

  function back() {
    navigate('/reports');
  }

  const currentReportId = route.reportId ?? null;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <img src={logo} alt="Research Code Evaluator logo" className="brand-mark" />
          <div>
            <div className="brand-name">Research Code Evaluator</div>
            <div className="brand-tag">Archive</div>
          </div>
        </div>

        <div className="nav-groups">
          {['Workspace', 'Analysis', 'System'].map((groupName) => {
            const items = NAV_ITEMS.filter((item) => item.section === groupName);
            return (
              <div key={groupName} className="nav-group">
                <div className="nav-group__title">{groupName}</div>
                {items.map((item) => (
                  <button
                    key={item.key}
                    type="button"
                    className={`nav-button ${route.page === item.key ? 'nav-button--active' : ''}`}
                    onClick={() => navigate(item.path)}
                    aria-current={route.page === item.key ? 'page' : undefined}
                  >
                    <span>{item.label}</span>
                  </button>
                ))}
              </div>
            );
          })}
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <p className="eyebrow">Empirical study</p>
            <h1>Research workspace</h1>
          </div>
          <div className="topbar__meta">
            <span className="meta-pill">AI vs Human</span>
            <span className="meta-pill meta-pill--muted">P001–P050</span>
          </div>
        </header>

        <div className="content-shell">
          {route.page === 'dashboard' && <Dashboard />}
          {route.page === 'solve' && <SolveProblems onReport={handleReport} />}
          {route.page === 'reports' && <Reports onOpen={openReport} onOpenDetailed={openDetailedReport} />}
          {route.page === 'report' && currentReportId !== null && (
            <ReportDetail reportId={currentReportId} onBack={back} />
          )}
          {route.page === 'detailed_report' && currentReportId !== null && (
            <DetailedReport reportId={currentReportId} onBack={back} />
          )}
          {route.page === 'research_guide' && <ResearchGuide />}
          {route.page === 'about_methodology' && <AboutMethodology />}
          {route.page === 'manage_data' && <ManageData />}
        </div>
      </main>
    </div>
  );
}
