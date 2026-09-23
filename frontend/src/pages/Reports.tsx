import { useEffect, useState } from 'react';
import { api } from '../api';
import { ComparisonSummary } from '../types';

export default function Reports({ onOpen, onOpenDetailed }: { onOpen: (id: number) => void; onOpenDetailed: (id: number) => void }) {
  const [items, setItems] = useState<ComparisonSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);
  const [exportingPdfId, setExportingPdfId] = useState<number | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [filterPilot, setFilterPilot] = useState<string>('all');
  const [filterAi, setFilterAi] = useState<string>('all');
  const [filterLanguage, setFilterLanguage] = useState<string>('all');
  const [filterProblem, setFilterProblem] = useState<string>('all');
  const [successMsg, setSuccessMsg] = useState('');

  function refresh() {
    setLoading(true);
    api.listComparisons().then(setItems).finally(() => setLoading(false));
  }

  useEffect(() => { refresh(); }, []);

  async function handleExport() {
    setExporting(true);
    try { await api.exportResearchReport(); }
    catch (e) { alert((e as Error).message); }
    finally { setExporting(false); }
  }

  async function handleExportPdf(id: number) {
    setExportingPdfId(id);
    try { await api.exportResearchReportPdf(id); }
    catch (e) { alert((e as Error).message); }
    finally { setExportingPdfId(null); }
  }

  async function handleDelete(it: ComparisonSummary) {
    const confirmed = window.confirm(
      `Delete comparison #${it.comparison_id} (${it.problem_title} · ${it.language} · ${it.ai_name})?\n\n` +
      `This will permanently remove the comparison and all its experiment results.\n` +
      `Problems and predefined test cases will NOT be deleted.`
    );
    if (!confirmed) return;
    setDeletingId(it.comparison_id);
    try {
      await api.deleteOneComparison(it.comparison_id);
      setSuccessMsg(`Comparison #${it.comparison_id} deleted. Problems and test cases are intact.`);
      setTimeout(() => setSuccessMsg(''), 5000);
      refresh();
    } catch (e) {
      alert(`Delete failed: ${(e as Error).message}`);
    } finally {
      setDeletingId(null);
    }
  }

  const filtered = items.filter(it => {
    if (filterPilot === 'research' && it.is_pilot) return false;
    if (filterPilot === 'pilot' && !it.is_pilot) return false;
    if (filterAi !== 'all' && it.ai_name !== filterAi) return false;
    if (filterLanguage !== 'all' && it.language !== filterLanguage) return false;
    if (filterProblem !== 'all' && it.problem_id !== filterProblem) return false;
    return true;
  });

  const aiSystems = Array.from(new Set(items.map(i => i.ai_name))).sort();
  const problems = Array.from(new Set(items.map(i => i.problem_id))).sort();

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2 className="page-title">Evaluations</h2>
          <p className="page-sub">Completed AI vs Human comparisons</p>
        </div>
        {items.length > 0 && (
          <button className="btn btn-secondary" onClick={handleExport} disabled={exporting}>
            {exporting ? 'Generating…' : 'Generate Research Report (Excel)'}
          </button>
        )}
      </div>

      {successMsg && <div className="alert alert--success">✓ {successMsg}</div>}

      <div className="filter-panel">
        <div className="filter-controls">
          <div className="filter-field">
            <label>AI System</label>
            <select value={filterAi} onChange={(e) => setFilterAi(e.target.value)}>
              <option value="all">All AI Systems</option>
              {aiSystems.map(name => <option key={name} value={name}>{name}</option>)}
            </select>
          </div>
          <div className="filter-field">
            <label>Language</label>
            <select value={filterLanguage} onChange={(e) => setFilterLanguage(e.target.value)}>
              <option value="all">All Languages</option>
              <option value="python">Python</option>
              <option value="java">Java</option>
            </select>
          </div>
          <div className="filter-field">
            <label>Problem</label>
            <select value={filterProblem} onChange={(e) => setFilterProblem(e.target.value)}>
              <option value="all">All Problems</option>
              {problems.map(id => <option key={id} value={id}>{id}</option>)}
            </select>
          </div>
          <div className="filter-field">
            <label>Data Type</label>
            <select value={filterPilot} onChange={(e) => setFilterPilot(e.target.value)}>
              <option value="all">All Data</option>
              <option value="research">Research Data Only</option>
              <option value="pilot">Pilot Data Only</option>
            </select>
          </div>
        </div>
      </div>

      {loading && <p>Loading…</p>}
      {!loading && items.length === 0 && (
        <div className="empty-state">
          <h3>No comparisons yet.</h3>
          <p>Run a comparison from <strong>Solve Problems</strong> to generate a report.</p>
        </div>
      )}

      {items.length > 0 && (
        <div className="evaluation-record-list">
          {filtered.map((it) => {
            const isDeleting = deletingId === it.comparison_id;
            const winnerClass =
              it.overall_winner === 'AI' ? 'status-badge--ai' :
              it.overall_winner === 'HUMAN' ? 'status-badge--human' :
              'status-badge--neutral';
            const typeClass = it.is_pilot ? 'status-badge--pilot' : 'status-badge--research';
            const statusClass =
              it.status === 'COMPLETED' ? 'status-badge--completed' :
              it.status === 'COMPARABLE' ? 'status-badge--comparable' :
              'status-badge--neutral';
            return (
              <div key={it.comparison_id} className={`evaluation-record ${isDeleting ? 'is-deleting' : ''}`}>
                <div className="evaluation-record__top">
                  <div className="evaluation-record__cell">
                    <span className="evaluation-record__label">ID</span>
                    <span className="evaluation-record__value nowrap">#{it.comparison_id}</span>
                  </div>
                  <div className="evaluation-record__cell">
                    <span className="evaluation-record__label">Problem</span>
                    <span className="evaluation-record__value wrap-text">{it.problem_title}</span>
                  </div>
                  <div className="evaluation-record__cell">
                    <span className="evaluation-record__label">Language</span>
                    <span className="evaluation-record__value nowrap">{it.language}</span>
                  </div>
                  <div className="evaluation-record__cell">
                    <span className="evaluation-record__label">AI System</span>
                    <span className="evaluation-record__value wrap-text">{it.ai_name}</span>
                  </div>
                  <div className="evaluation-record__cell">
                    <span className="evaluation-record__label">Type</span>
                    <span className="evaluation-record__value"><span className={`status-badge ${typeClass}`}>{it.experiment_type}</span></span>
                  </div>
                </div>

                <div className="evaluation-record__middle">
                  <div className="evaluation-record__cell">
                    <span className="evaluation-record__label">AI Score</span>
                    <span className="evaluation-record__value nowrap" style={{ textAlign: 'center' }}>{it.ai_overall != null ? it.ai_overall.toFixed(2) : '—'}</span>
                  </div>
                  <div className="evaluation-record__cell">
                    <span className="evaluation-record__label">Human Score</span>
                    <span className="evaluation-record__value nowrap" style={{ textAlign: 'center' }}>{it.human_overall != null ? it.human_overall.toFixed(2) : '—'}</span>
                  </div>
                  <div className="evaluation-record__cell">
                    <span className="evaluation-record__label">Winner</span>
                    <span className="evaluation-record__value"><span className={`status-badge ${winnerClass}`}>{it.overall_winner ?? '—'}</span></span>
                  </div>
                  <div className="evaluation-record__cell">
                    <span className="evaluation-record__label">Status</span>
                    <span className="evaluation-record__value"><span className={`status-badge ${statusClass}`}>{it.status}</span></span>
                  </div>
                </div>

                <div className="evaluation-record__actions">
                  <button className="btn btn-secondary" onClick={() => onOpenDetailed(it.comparison_id)} disabled={isDeleting}>View Detailed Report</button>
                  <button className="btn btn-secondary" onClick={() => handleExportPdf(it.comparison_id)} disabled={exportingPdfId === it.comparison_id || isDeleting}>{exportingPdfId === it.comparison_id ? 'Exporting…' : 'Export PDF'}</button>
                  <button className="btn btn-secondary btn-delete" onClick={() => handleDelete(it)} disabled={isDeleting}>{isDeleting ? 'Deleting…' : 'Delete'}</button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
