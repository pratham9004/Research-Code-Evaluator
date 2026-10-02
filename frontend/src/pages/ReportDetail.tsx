import { useEffect, useState } from 'react';
import { api } from '../api';
import { Report } from '../types';

const METRIC_LABELS: Record<string, string> = {
  reliability: 'reliability',
  performance: 'execution time',
  maintainability: 'maintainability',
  security: 'security findings',
  complexity: 'complexity',
  code_quality: 'code quality',
  overall: 'overall score',
};

function observation(metric: string, direction: string): string {
  const label = METRIC_LABELS[metric] || metric;
  if (direction === 'AI') return `AI implementation recorded a higher ${label} value.`;
  if (direction === 'HUMAN') return `Human implementation recorded a higher ${label} value.`;
  return `No marked difference was observed in ${label}.`;
}

export default function ReportDetail({ reportId, onBack }: { reportId: number; onBack: () => void }) {
  const [report, setReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setLoadError(null);
    api.getComparison(reportId)
      .then(setReport)
      .catch((e: Error) => setLoadError(e.message))
      .finally(() => setLoading(false));
  }, [reportId]);

  if (loading) return <div className="page"><p>Loading report…</p></div>;
  if (!report) return <div className="page"><p>{loadError || 'Report not found.'}</p></div>;

  const cmp = (m: string) => report.comparison.find((c) => c.metric === m);

  return (
    <div className="page report-page">
      <button className="btn btn-secondary" onClick={onBack} style={{ marginBottom: 16 }}>← Back to Reports</button>
      <h2 className="page-title">Comparison Report #{report.comparison_id}</h2>
      <p className="page-sub">
        {report.problem_title} · {report.language} · AI: {report.ai_name}
      </p>

      <div className="card" style={{ marginBottom: 18 }}>
        <table className="report-field-table">
          <tbody>
            <tr><td>Experiment Type</td><td className="wrap-text">{report.experiment_type}</td></tr>
            <tr><td>Problem Version</td><td className="wrap-text">{report.problem_version ?? 'N/A'}</td></tr>
            <tr><td>Test Case Version</td><td className="wrap-text">{report.test_case_version ?? 'N/A'}</td></tr>
            <tr><td>Data Classification</td><td className="wrap-text">{report.data_classification}</td></tr>
            <tr><td>Status</td><td className="wrap-text"><span className={`pill ${report.is_pilot ? 'pilot' : 'research'}`}>{report.experiment_type}</span></td></tr>
          </tbody>
        </table>
      </div>

      {report.preflight?.ai?.length > 0 && (
        <div className="card" style={{ marginBottom: 18 }}>
          <div className="section-title" style={{ marginTop: 0 }}>Preflight Validation — AI</div>
          <table>
            <thead><tr><th>Status</th><th>Message</th></tr></thead>
            <tbody>
              {report.preflight.ai.map((p, i) => (
                <tr key={i}><td><span className={`pill ${p.status === 'PASS' ? 'pass' : 'fail'}`}>{p.status}</span></td><td>{p.message}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {report.preflight?.human?.length > 0 && (
        <div className="card" style={{ marginBottom: 18 }}>
          <div className="section-title" style={{ marginTop: 0 }}>Preflight Validation — Human</div>
          <table>
            <thead><tr><th>Status</th><th>Message</th></tr></thead>
            <tbody>
              {report.preflight.human.map((p, i) => (
                <tr key={i}><td><span className={`pill ${p.status === 'PASS' ? 'pass' : 'fail'}`}>{p.status}</span></td><td>{p.message}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="card" style={{ marginBottom: 18 }}>
        <table>
          <thead>
            <tr><th>Metric</th><th className="ai-col">AI</th><th className="human-col">Human</th><th>Difference</th><th>Direction</th></tr>
          </thead>
          <tbody>
            {report.comparison.map((c) => (
              <tr key={c.metric}>
                <td>{METRIC_LABELS[c.metric] || c.metric}</td>
                <td className="ai-col">{c.ai_value}</td>
                <td className="human-col">{c.human_value}</td>
                <td>{c.difference}</td>
                <td>
                  <span className={`pill ${c.direction === 'AI' ? 'ai' : c.direction === 'HUMAN' ? 'human' : 'comp'}`}>
                    {c.direction}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card" style={{ marginBottom: 18 }}>
        <div className="section-title" style={{ marginTop: 0 }}>Test Case Results</div>
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th className="ai-col">AI</th>
              <th className="human-col">Human</th>
              <th>AI Time</th>
              <th>Human Time</th>
            </tr>
          </thead>
          <tbody>
            {report.execution.ai.cases.map((c: any, i: number) => {
              const h = report.execution.human.cases[i] || { status: 'N/A', execution_time_ms: null };
              const pillColor = (s: string) =>
                s === 'PASS' ? 'pass' : s === 'ERROR' ? 'err' : s === 'TIMEOUT' ? 'fail' : 'fail';
              return (
                <tr key={i}>
                  <td>{i + 1}</td>
                  <td className="ai-col"><span className={`pill ${pillColor(c.status)}`}>{c.status}</span></td>
                  <td className="human-col"><span className={`pill ${pillColor(h.status)}`}>{h.status}</span></td>
                  <td>{c.execution_time_ms ?? 'N/A'} ms</td>
                  <td>{h.execution_time_ms ?? 'N/A'} ms</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="card">
        <div className="section-title" style={{ marginTop: 0 }}>Neutral Observations</div>
        <ul className="neutral-observations">
          {report.comparison.map((c) => (
            <li key={c.metric} className="obs">{observation(c.metric, c.direction)}</li>
          ))}
          <li className="obs muted">Objective findings above are based on a single comparison and do not imply a universal conclusion.</li>
        </ul>
      </div>
    </div>
  );
}
