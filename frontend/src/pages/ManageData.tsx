import { useEffect, useState } from 'react';
import { api } from '../api';
import { ComparisonSummary } from '../types';

interface Preview {
  comparison_ids: number[];
  count: number;
  earliest: string | null;
  latest: string | null;
  problems_affected: string[];
  protected_note: string;
}

interface Summary {
  deletable: { total_comparisons: number; research_comparisons: number; pilot_comparisons: number };
  protected: { problems: number; predefined_test_cases: number; note: string };
}

function ProtectedNote() {
  return (
    <div style={{
      background: '#f0fdf4', border: '1px solid #86efac', borderRadius: 6,
      padding: '8px 12px', fontSize: 13, color: '#166534', marginTop: 8,
    }}>
      🔒 <strong>Problems and predefined test cases are NEVER deleted.</strong> Only comparison experiment data is removed.
    </div>
  );
}

function PreviewBox({ preview, onConfirm, onCancel, loading, mode }: {
  preview: Preview;
  onConfirm: () => void;
  onCancel: () => void;
  loading: boolean;
  mode: 'standard' | 'strong';
}) {
  const [typed, setTyped] = useState('');
  const confirmWord = 'DELETE RESEARCH DATA';
  const canConfirm = mode === 'standard' || typed === confirmWord;

  return (
    <div style={{
      background: '#fef2f2', border: '1px solid #fca5a5', borderRadius: 8,
      padding: 20, marginTop: 16,
    }}>
      <div style={{ fontWeight: 700, fontSize: 15, color: '#991b1b', marginBottom: 12 }}>
        ⚠ Confirm Deletion
      </div>
      <p style={{ margin: '0 0 8px' }}>
        You are about to delete <strong>{preview.count} comparison{preview.count !== 1 ? 's' : ''}</strong> and all their associated experiment results.
      </p>
      {preview.earliest && (
        <p style={{ margin: '0 0 4px', fontSize: 13, color: '#64748b' }}>
          Date range: {preview.earliest?.slice(0, 10)} → {preview.latest?.slice(0, 10)}
        </p>
      )}
      <p style={{ margin: '0 0 8px', fontSize: 13, color: '#64748b' }}>
        Problems involved: {preview.problems_affected.join(', ') || 'none'}
      </p>
      <p style={{ margin: '0 0 12px', fontWeight: 600, color: '#166534', fontSize: 13 }}>
        🔒 {preview.protected_note}
      </p>

      {mode === 'strong' && (
        <div style={{ marginBottom: 12 }}>
          <label style={{ display: 'block', marginBottom: 4, fontSize: 13, fontWeight: 600 }}>
            Type <code style={{ background: '#fee2e2', padding: '1px 4px', borderRadius: 3 }}>{confirmWord}</code> to confirm:
          </label>
          <input
            type="text"
            value={typed}
            onChange={e => setTyped(e.target.value)}
            style={{
              width: '100%', padding: '8px 10px', border: '1px solid #fca5a5',
              borderRadius: 4, fontSize: 13, fontFamily: 'monospace',
              background: typed === confirmWord ? '#f0fdf4' : 'white',
            }}
            placeholder={confirmWord}
            disabled={loading}
          />
        </div>
      )}

      <div style={{ display: 'flex', gap: 8 }}>
        <button
          className="btn"
          style={{ background: canConfirm ? '#dc2626' : '#9ca3af', cursor: canConfirm ? 'pointer' : 'not-allowed' }}
          onClick={onConfirm}
          disabled={!canConfirm || loading}
        >
          {loading ? 'Deleting…' : `Delete ${preview.count} Comparison${preview.count !== 1 ? 's' : ''}`}
        </button>
        <button className="btn btn-secondary" onClick={onCancel} disabled={loading}>
          Cancel
        </button>
      </div>
    </div>
  );
}

export default function ManageData() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [comparisons, setComparisons] = useState<ComparisonSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'single' | 'multiple' | 'daterange' | 'all'>('single');

  // Single delete
  const [singleId, setSingleId] = useState<string>('');
  const [singlePreview, setSinglePreview] = useState<Preview | null>(null);
  const [singleLoading, setSingleLoading] = useState(false);

  // Multiple select
  const [selected, setSelected] = useState<Set<number>>(new Set());
  const [multiPreview, setMultiPreview] = useState<Preview | null>(null);
  const [multiLoading, setMultiLoading] = useState(false);

  // Date range
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [datePreview, setDatePreview] = useState<Preview | null>(null);
  const [dateLoading, setDateLoading] = useState(false);

  // Delete all
  const [allPreview, setAllPreview] = useState<Preview | null>(null);
  const [allLoading, setAllLoading] = useState(false);

  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  function refresh() {
    setLoading(true);
    Promise.all([
      api.getDataSummary().then(setSummary),
      api.listComparisons().then(setComparisons),
    ]).finally(() => setLoading(false));
  }

  useEffect(() => { refresh(); }, []);

  function showSuccess(msg: string) {
    setSuccessMsg(msg);
    setErrorMsg('');
    setTimeout(() => setSuccessMsg(''), 5000);
  }
  function showError(msg: string) {
    setErrorMsg(msg);
    setSuccessMsg('');
  }

  // ── Single ────────────────────────────────────────────────────────────
  async function previewSingle() {
    const id = parseInt(singleId, 10);
    if (isNaN(id)) return showError('Please enter a valid comparison ID.');
    setSingleLoading(true);
    try {
      const p = await api.previewDeleteByIds([id]);
      if (p.count === 0) return showError(`Comparison ${id} not found.`);
      setSinglePreview(p);
      setErrorMsg('');
    } catch (e: any) { showError(e.message); }
    finally { setSingleLoading(false); }
  }

  async function confirmSingle() {
    if (!singlePreview) return;
    setSingleLoading(true);
    try {
      const r = await api.deleteOneComparison(singlePreview.comparison_ids[0]);
      showSuccess(`Deleted comparison #${singlePreview.comparison_ids[0]}. ${r.protected_note}`);
      setSinglePreview(null);
      setSingleId('');
      refresh();
    } catch (e: any) { showError(e.message); }
    finally { setSingleLoading(false); }
  }

  // ── Multiple ──────────────────────────────────────────────────────────
  function toggleSelect(id: number) {
    setSelected(prev => {
      const s = new Set(prev);
      s.has(id) ? s.delete(id) : s.add(id);
      return s;
    });
    setMultiPreview(null);
  }

  function selectAll() { setSelected(new Set(comparisons.map(c => c.comparison_id))); setMultiPreview(null); }
  function selectNone() { setSelected(new Set()); setMultiPreview(null); }

  async function previewMulti() {
    if (selected.size === 0) return showError('Select at least one comparison.');
    setMultiLoading(true);
    try {
      const p = await api.previewDeleteByIds([...selected]);
      setMultiPreview(p);
      setErrorMsg('');
    } catch (e: any) { showError(e.message); }
    finally { setMultiLoading(false); }
  }

  async function confirmMulti() {
    if (!multiPreview) return;
    setMultiLoading(true);
    try {
      const r = await api.deleteComparisonsByIds(multiPreview.comparison_ids);
      showSuccess(`Deleted ${r.deleted_comparisons} comparisons. ${r.protected_note}`);
      setMultiPreview(null);
      setSelected(new Set());
      refresh();
    } catch (e: any) { showError(e.message); }
    finally { setMultiLoading(false); }
  }

  // ── Date range ────────────────────────────────────────────────────────
  async function previewDate() {
    if (!dateFrom || !dateTo) return showError('Select both a start and end date.');
    if (dateFrom > dateTo) return showError('Start date must be before or equal to end date.');
    setDateLoading(true);
    try {
      const p = await api.previewDeleteByDateRange(dateFrom, dateTo);
      setDatePreview(p);
      setErrorMsg('');
    } catch (e: any) { showError(e.message); }
    finally { setDateLoading(false); }
  }

  async function confirmDate() {
    if (!datePreview) return;
    setDateLoading(true);
    try {
      const r = await api.deleteByDateRange(dateFrom, dateTo);
      showSuccess(`Deleted ${r.deleted_comparisons} comparisons in date range. ${r.protected_note}`);
      setDatePreview(null);
      refresh();
    } catch (e: any) { showError(e.message); }
    finally { setDateLoading(false); }
  }

  // ── Delete All ────────────────────────────────────────────────────────
  async function previewAll() {
    setAllLoading(true);
    try {
      const p = await api.previewDeleteAll();
      setAllPreview(p);
      setErrorMsg('');
    } catch (e: any) { showError(e.message); }
    finally { setAllLoading(false); }
  }

  async function confirmAll() {
    if (!allPreview) return;
    setAllLoading(true);
    try {
      const r = await api.deleteAllComparisons();
      showSuccess(`Deleted all ${r.deleted_comparisons} comparisons. ${r.protected_note}`);
      setAllPreview(null);
      refresh();
    } catch (e: any) { showError(e.message); }
    finally { setAllLoading(false); }
  }

  const tabStyle = (t: string): React.CSSProperties => ({
    padding: '8px 16px', cursor: 'pointer', border: 'none', borderRadius: '6px 6px 0 0',
    fontWeight: activeTab === t ? 700 : 400,
    background: activeTab === t ? 'white' : '#f1f5f9',
    color: activeTab === t ? '#1e3a8a' : '#64748b',
    borderBottom: activeTab === t ? '2px solid #1e3a8a' : '2px solid transparent',
  });

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2 className="page-title">Manage Research Data</h2>
          <p className="page-sub">Safely delete experiment/comparison data. Problems and predefined test cases are always preserved.</p>
        </div>
        <span className="meta-pill">Data controls</span>
      </div>

      {successMsg && <div className="alert alert--success">✓ {successMsg}</div>}
      {errorMsg && <div className="alert alert--error">✗ {errorMsg}</div>}

      {summary && (
        <div className="info-grid" style={{ marginBottom: 20 }}>
          <div className="kpi">
            <div className="value" style={{ color: '#a04040' }}>{summary.deletable.total_comparisons}</div>
            <div className="label">Total Comparisons</div>
          </div>
          <div className="kpi">
            <div className="value" style={{ color: 'var(--archive-success)' }}>{summary.deletable.research_comparisons}</div>
            <div className="label">Research Data</div>
          </div>
          <div className="kpi">
            <div className="value" style={{ color: 'var(--archive-slate)' }}>{summary.deletable.pilot_comparisons}</div>
            <div className="label">Pilot Data</div>
          </div>
          <div className="kpi" style={{ background: 'linear-gradient(180deg, rgba(42,100,77,0.08), rgba(42,100,77,0.04))' }}>
            <div className="value" style={{ fontSize: '1.35rem', color: '#1d5d4a' }}>🔒 {summary.protected.problems} problems</div>
            <div className="label" style={{ color: '#1d5d4a' }}>{summary.protected.predefined_test_cases} test cases protected</div>
          </div>
        </div>
      )}

      <div className="segmented-tabs">
        <button className={`tab-button ${activeTab === 'single' ? 'tab-button--active' : ''}`} onClick={() => { setActiveTab('single'); setSinglePreview(null); }}>Delete One</button>
        <button className={`tab-button ${activeTab === 'multiple' ? 'tab-button--active' : ''}`} onClick={() => { setActiveTab('multiple'); setMultiPreview(null); }}>Delete Selected</button>
        <button className={`tab-button ${activeTab === 'daterange' ? 'tab-button--active' : ''}`} onClick={() => { setActiveTab('daterange'); setDatePreview(null); }}>Delete by Date</button>
        <button className={`tab-button ${activeTab === 'all' ? 'tab-button--active' : ''}`} onClick={() => { setActiveTab('all'); setAllPreview(null); }}>Delete All</button>
      </div>

      <div className="section-card" style={{ marginTop: 0 }}>

        {/* ── Single ── */}
        {activeTab === 'single' && (
          <div>
            <p style={{ marginBottom: 12, fontWeight: 600 }}>Delete a single comparison by ID</p>
            <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
              <input
                type="number"
                value={singleId}
                onChange={e => { setSingleId(e.target.value); setSinglePreview(null); }}
                placeholder="Comparison ID (e.g. 5)"
                style={{ width: 180, padding: '8px 10px', border: '1px solid #e2e8f0', borderRadius: 4 }}
                disabled={singleLoading}
              />
              <button className="btn btn-secondary" onClick={previewSingle} disabled={singleLoading || !singleId}>
                {singleLoading ? 'Checking…' : 'Preview'}
              </button>
            </div>
            <ProtectedNote />
            {singlePreview && !singleLoading && (
              <PreviewBox preview={singlePreview} onConfirm={confirmSingle} onCancel={() => setSinglePreview(null)} loading={singleLoading} mode="standard" />
            )}
          </div>
        )}

        {/* ── Multiple ── */}
        {activeTab === 'multiple' && (
          <div>
            <p style={{ marginBottom: 8, fontWeight: 600 }}>Select comparisons to delete</p>
            <div style={{ display: 'flex', gap: 8, marginBottom: 10 }}>
              <button className="btn btn-secondary" onClick={selectAll} style={{ fontSize: 12 }}>Select All</button>
              <button className="btn btn-secondary" onClick={selectNone} style={{ fontSize: 12 }}>Select None</button>
              <span style={{ fontSize: 13, color: 'var(--muted)', alignSelf: 'center' }}>{selected.size} selected</span>
            </div>
            {loading ? <p>Loading…</p> : (
              <div style={{ maxHeight: 320, overflowY: 'auto', border: '1px solid #e2e8f0', borderRadius: 6 }}>
                <table style={{ width: '100%' }}>
                  <thead>
                    <tr style={{ background: '#f8fafc' }}>
                      <th style={{ width: 40, padding: '8px 10px' }}></th>
                      <th style={{ padding: '8px 10px', textAlign: 'left' }}>ID</th>
                      <th style={{ padding: '8px 10px', textAlign: 'left' }}>Problem</th>
                      <th style={{ padding: '8px 10px', textAlign: 'left' }}>Language</th>
                      <th style={{ padding: '8px 10px', textAlign: 'left' }}>AI System</th>
                      <th style={{ padding: '8px 10px', textAlign: 'left' }}>Type</th>
                      <th style={{ padding: '8px 10px', textAlign: 'left' }}>Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    {comparisons.map(c => (
                      <tr key={c.comparison_id} style={{ background: selected.has(c.comparison_id) ? '#eff6ff' : 'white', cursor: 'pointer' }} onClick={() => toggleSelect(c.comparison_id)}>
                        <td style={{ padding: '6px 10px', textAlign: 'center' }}>
                          <input type="checkbox" checked={selected.has(c.comparison_id)} onChange={() => toggleSelect(c.comparison_id)} onClick={e => e.stopPropagation()} />
                        </td>
                        <td style={{ padding: '6px 10px' }}>{c.comparison_id}</td>
                        <td style={{ padding: '6px 10px' }}>{c.problem_title}</td>
                        <td style={{ padding: '6px 10px' }}>{c.language}</td>
                        <td style={{ padding: '6px 10px' }}>{c.ai_name}</td>
                        <td style={{ padding: '6px 10px' }}><span className={`pill ${c.is_pilot ? 'pilot' : 'research'}`}>{c.experiment_type}</span></td>
                        <td style={{ padding: '6px 10px', fontSize: 12, color: 'var(--muted)' }}>{c.created_at?.slice(0, 10)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
            <ProtectedNote />
            <div style={{ marginTop: 12 }}>
              <button className="btn btn-secondary" onClick={previewMulti} disabled={selected.size === 0 || multiLoading}>
                {multiLoading ? 'Checking…' : `Preview Delete (${selected.size})`}
              </button>
            </div>
            {multiPreview && !multiLoading && (
              <PreviewBox preview={multiPreview} onConfirm={confirmMulti} onCancel={() => setMultiPreview(null)} loading={multiLoading} mode="standard" />
            )}
          </div>
        )}

        {/* ── Date range ── */}
        {activeTab === 'daterange' && (
          <div>
            <p style={{ marginBottom: 12, fontWeight: 600 }}>Delete all comparisons created within a date range</p>
            <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
              <div>
                <label style={{ display: 'block', fontSize: 12, marginBottom: 4 }}>From</label>
                <input type="date" value={dateFrom} onChange={e => { setDateFrom(e.target.value); setDatePreview(null); }}
                  style={{ padding: '8px 10px', border: '1px solid #e2e8f0', borderRadius: 4 }} disabled={dateLoading} />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: 12, marginBottom: 4 }}>To</label>
                <input type="date" value={dateTo} onChange={e => { setDateTo(e.target.value); setDatePreview(null); }}
                  style={{ padding: '8px 10px', border: '1px solid #e2e8f0', borderRadius: 4 }} disabled={dateLoading} />
              </div>
              <button className="btn btn-secondary" style={{ marginTop: 18 }} onClick={previewDate} disabled={!dateFrom || !dateTo || dateLoading}>
                {dateLoading ? 'Checking…' : 'Preview'}
              </button>
            </div>
            <ProtectedNote />
            {datePreview && !dateLoading && (
              datePreview.count === 0
                ? <p style={{ marginTop: 12, color: 'var(--muted)' }}>No comparisons found in that date range.</p>
                : <PreviewBox preview={datePreview} onConfirm={confirmDate} onCancel={() => setDatePreview(null)} loading={dateLoading} mode="standard" />
            )}
          </div>
        )}

        {/* ── Delete All ── */}
        {activeTab === 'all' && (
          <div>
            <div style={{ background: '#fef2f2', border: '1px solid #fca5a5', borderRadius: 6, padding: '12px 16px', marginBottom: 16 }}>
              <p style={{ margin: 0, fontWeight: 700, color: '#991b1b' }}>⚠ Delete ALL Comparison Data</p>
              <p style={{ margin: '6px 0 0', fontSize: 13, color: '#7f1d1d' }}>
                This will permanently remove every comparison and all associated experiment results.
                Use this to clear old test/pilot data before starting your real research collection.
              </p>
            </div>
            <ProtectedNote />
            <div style={{ marginTop: 12 }}>
              <button className="btn" style={{ background: '#dc2626' }} onClick={previewAll} disabled={allLoading}>
                {allLoading ? 'Checking…' : 'Preview Delete All'}
              </button>
            </div>
            {allPreview && !allLoading && (
              allPreview.count === 0
                ? <p style={{ marginTop: 12, color: 'var(--muted)' }}>No comparisons to delete.</p>
                : <PreviewBox preview={allPreview} onConfirm={confirmAll} onCancel={() => setAllPreview(null)} loading={allLoading} mode="strong" />
            )}
          </div>
        )}

      </div>
    </div>
  );
}
