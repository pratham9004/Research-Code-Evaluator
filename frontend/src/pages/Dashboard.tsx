import { useEffect, useState } from 'react';
import { api } from '../api';
import { DashboardData } from '../types';
import MetricCard from '../components/MetricCard';
import { BarChart } from '../components/ChartPanel';

function WinnerPill({ winner }: { winner: string }) {
  const styles: Record<string, React.CSSProperties> = {
    AI:         { background: 'rgba(37,99,235,0.12)', color: 'var(--ai)',    padding: '2px 8px', borderRadius: 4, fontWeight: 600, fontSize: 12 },
    HUMAN:      { background: 'rgba(13,148,136,0.12)', color: 'var(--human)', padding: '2px 8px', borderRadius: 4, fontWeight: 600, fontSize: 12 },
    COMPARABLE: { background: 'rgba(100,116,139,0.10)', color: '#475569',     padding: '2px 8px', borderRadius: 4, fontWeight: 600, fontSize: 12 },
  };
  return <span style={styles[winner] ?? styles['COMPARABLE']}>{winner}</span>;
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getDashboard().then(setData).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="page"><p>Loading…</p></div>;
  if (!data) return <div className="page"><p>Failed to load dashboard.</p></div>;

  if (!data.has_data) {
    return (
      <div className="page">
        <h2 className="page-title">Dashboard</h2>
        <p className="page-sub">Research progress and analytics</p>
        <div className="empty-state">
          <h3>{data.python_benchmark_results?.some((row) => row.comparison_id != null)
            ? 'Python execution results are available; aggregate scores are not.'
            : 'No valid paired comparison data available.'}</h3>
          <p>{data.kpis.incomplete_comparisons} incomplete records are retained. Records without the complete score dimensions are excluded from aggregate outcome analytics.</p>
          <p>Complete a comparison from <strong>Solve Problems</strong> to populate research analytics.</p>
        </div>
      </div>
    );
  }

  const k = data.kpis;
  const o = data.outcomes;
  const metricKeys = Object.keys(data.metric_averages);
  const totalOutcomes = o.ai_better + o.human_better + o.comparable;

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2 className="page-title">Dashboard</h2>
          <p className="page-sub">Research progress and analytics — research data only (pilot excluded)</p>
        </div>
        <div className="page-header__meta">
          <span className="meta-pill">Research overview</span>
        </div>
      </div>

      <div className="grid-kpi">
        <MetricCard value={k.total_problems} label="Total Problems" />
        <MetricCard value={k.problems_compared} label="Problems Compared" />
        <MetricCard value={k.problems_remaining} label="Remaining" />
        <MetricCard value={`${k.completion_percentage}%`} label="Completion" />
        <MetricCard value={k.total_comparisons} label="Research Comparisons" />
        <MetricCard value={k.raw_execution_datasets} label="Raw Execution Datasets" />
        <MetricCard value={k.pilot_comparisons} label="Pilot Comparisons" />
        <MetricCard value={k.ai_systems_count} label="AI Systems Used" />
      </div>

      {totalOutcomes > 0 && (
        <div className="section-card" style={{ marginBottom: 18 }}>
          <div className="section-title" style={{ marginTop: 0, marginBottom: 12 }}>Overall Outcome Summary</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(0, 1fr))', gap: 12, textAlign: 'center' }}>
            <div style={{ padding: 14, borderRadius: 12, background: 'rgba(47,106,142,0.08)', border: '1px solid rgba(47,106,142,0.12)' }}>
              <div style={{ fontSize: 30, fontWeight: 700, color: 'var(--archive-ai)' }}>{o.ai_better}</div>
              <div style={{ fontSize: 12, color: 'var(--archive-muted)', marginTop: 4, letterSpacing: '0.08em', textTransform: 'uppercase' }}>AI Wins</div>
            </div>
            <div style={{ padding: 14, borderRadius: 12, background: 'rgba(184,108,42,0.08)', border: '1px solid rgba(184,108,42,0.12)' }}>
              <div style={{ fontSize: 30, fontWeight: 700, color: 'var(--archive-human)' }}>{o.human_better}</div>
              <div style={{ fontSize: 12, color: 'var(--archive-muted)', marginTop: 4, letterSpacing: '0.08em', textTransform: 'uppercase' }}>Human Wins</div>
            </div>
            <div style={{ padding: 14, borderRadius: 12, background: 'rgba(86,103,122,0.08)', border: '1px solid rgba(86,103,122,0.12)' }}>
              <div style={{ fontSize: 30, fontWeight: 700, color: '#475569' }}>{o.comparable}</div>
              <div style={{ fontSize: 12, color: 'var(--archive-muted)', marginTop: 4, letterSpacing: '0.08em', textTransform: 'uppercase' }}>Comparable</div>
            </div>
          </div>
          <p className="obs muted" style={{ marginBottom: 0, textAlign: 'center' }}>
            Single-comparison results do not establish universal superiority. Statistical conclusions require sufficient paired observations.
          </p>
        </div>
      )}

      <div className="section-title">Dimension Analysis</div>
      <div className="grid-charts">
        {metricKeys.map((key) => {
          const m = data.metric_averages[key];
          return (
            <div className="chart-card" key={key}>
              <div className="chart-card__header">
                <h3 className="chart-card__title">{m.label}</h3>
                <span className="chart-card__note">Mean values</span>
              </div>
              {m.ai !== null && m.human !== null
                ? <BarChart title="" labels={['AI', 'Human']} ai={[m.ai]} human={[m.human]} />
                : <p className="obs">No complete paired measurements available.</p>}
            </div>
          );
        })}
      </div>

      {data.recent_comparisons && data.recent_comparisons.length > 0 && (
        <>
          <div className="section-title" style={{ marginTop: 24 }}>Recent Research Comparisons</div>
          <div className="data-table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Problem</th>
                  <th>Language</th>
                  <th>AI System</th>
                  <th>AI Score</th>
                  <th>Human Score</th>
                  <th>Winner</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {data.recent_comparisons.map((r) => (
                  <tr key={r.comparison_id}>
                    <td>{r.comparison_id}</td>
                    <td>{r.problem_title}</td>
                    <td>{r.language}</td>
                    <td>{r.ai_name}</td>
                    <td>{r.ai_overall != null ? r.ai_overall.toFixed(2) : 'N/A'}</td>
                    <td>{r.human_overall != null ? r.human_overall.toFixed(2) : 'N/A'}</td>
                    <td><WinnerPill winner={r.overall_winner} /></td>
                    <td style={{ fontSize: 12, color: 'var(--archive-muted)', whiteSpace: 'nowrap' }}>
                      {r.created_at ? new Date(r.created_at).toLocaleDateString() : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      <div className="section-card" style={{ marginTop: 20 }}>
        <a className="report-link" href="/api/export/research-report">
          Download Full Research Report (Excel)
        </a>
      </div>
    </div>
  );
}
