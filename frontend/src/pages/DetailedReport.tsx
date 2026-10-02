import { useEffect, useState } from 'react';
import { api } from '../api';
import { DetailedReport as DetailedReportData, MaintainabilityComponent } from '../types';

function SectionTitle({ children, style }: { children: React.ReactNode; style?: React.CSSProperties }) {
  return <div className="section-title" style={style}>{children}</div>;
}

function Pill({ children, color }: { children: React.ReactNode; color?: string }) {
  const bg = color === 'ai' ? 'rgba(37,99,235,0.12)' : color === 'human' ? 'rgba(13,148,136,0.12)' : 'rgba(100,116,139,0.12)';
  const textColor = color === 'ai' ? 'var(--ai)' : color === 'human' ? 'var(--human)' : 'var(--muted)';
  return <span className="pill" style={{ background: bg, color: textColor }}>{children}</span>;
}

function displayDirection(direction: string | null | undefined): string {
  return direction || 'UNAVAILABLE';
}

export default function DetailedReport({ reportId, onBack }: { reportId: number; onBack: () => void }) {
  const [report, setReport] = useState<DetailedReportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [exportingPdf, setExportingPdf] = useState(false);

  useEffect(() => {
    setLoading(true);
    setLoadError(null);
    api.getDetailedComparison(reportId)
      .then(setReport)
      .catch((e: Error) => setLoadError(e.message))
      .finally(() => setLoading(false));
  }, [reportId]);

  async function handleExportPdf() {
    setExportingPdf(true);
    try {
      await api.exportResearchReportPdf(reportId);
    } catch (e) {
      alert((e as Error).message);
    } finally {
      setExportingPdf(false);
    }
  }

  if (loading) return <div className="page"><p>Loading detailed report…</p></div>;
  if (!report) return <div className="page"><p>{loadError || 'Report not found.'}</p></div>;

  const e = report.experiment;
  const exec_ = report.executive_result;
  const rawExecution = e.status.toLowerCase() === 'execution_only';

  return (
    <div className="page report-page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <button className="btn btn-secondary" onClick={onBack}>← Back to Reports</button>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn btn-secondary" onClick={handleExportPdf} disabled={exportingPdf}>
            {exportingPdf ? 'Exporting PDF…' : 'Export PDF'}
          </button>
        </div>
      </div>

      <h2 className="page-title">{rawExecution ? 'Detailed Raw Execution Report' : 'Detailed Research Report'} #{e.comparison_id}</h2>
      <p className="page-sub">
        {e.problem_id} — {e.problem_title} · {e.language} · AI: {e.ai_name} · reference: Human
      </p>

      {/* SECTION 1 — EXPERIMENT INFORMATION */}
      <div className="card" style={{ marginBottom: 18 }}>
        <SectionTitle>1. Experiment Information</SectionTitle>
        <table className="report-field-table">
          <tbody>
            <tr><td>Comparison ID</td><td className="wrap-text nowrap">{e.comparison_id}</td></tr>
            <tr><td>Problem ID</td><td className="wrap-text nowrap">{e.problem_id}</td></tr>
            <tr><td>Problem Title</td><td className="wrap-text">{e.problem_title}</td></tr>
            <tr><td>Category</td><td className="wrap-text">{e.category}</td></tr>
            <tr><td>Difficulty</td><td className="wrap-text">{e.difficulty}</td></tr>
            <tr><td>Language</td><td className="wrap-text nowrap">{e.language}</td></tr>
            <tr><td>AI System</td><td className="wrap-text">{e.ai_name}</td></tr>
            <tr><td>Experiment Type</td><td className="wrap-text"><Pill color={e.is_pilot ? 'human' : 'ai'}>{e.experiment_type}</Pill></td></tr>
            <tr><td>Status</td><td className="wrap-text"><Pill>{rawExecution ? 'RAW EXECUTION DATA' : e.status}</Pill></td></tr>
            <tr><td>Problem Version</td><td className="wrap-text">{e.problem_version ?? 'N/A'}</td></tr>
            <tr><td>Test Case Version</td><td className="wrap-text">{e.test_case_version ?? 'N/A'}</td></tr>
            <tr><td>Created At</td><td className="wrap-text">{e.created_at}</td></tr>
            <tr><td>Completed At</td><td className="wrap-text">{e.completed_at}</td></tr>
            <tr><td>Execution Timeout</td><td className="wrap-text">{e.execution_timeout_seconds} seconds</td></tr>
            <tr><td>Test Cases</td><td className="wrap-text nowrap">{e.test_case_count}</td></tr>
            <tr><td>AI Code Available</td><td className="wrap-text">{e.ai_code_available ? 'Yes' : 'No'}</td></tr>
            <tr><td>Human Code Available</td><td className="wrap-text">{e.human_code_available ? 'Yes' : 'No'}</td></tr>
            <tr><td>Data Classification</td><td className="wrap-text"><strong>{e.data_classification}</strong></td></tr>
          </tbody>
        </table>
      </div>

      {/* SECTION 2 — EXECUTIVE RESULT */}
      <div className="card" style={{ marginBottom: 18 }}>
        <SectionTitle>2. Executive Result</SectionTitle>
        {rawExecution ? <p className="obs">This record contains raw execution data only. Comparative scores and an AI/Human winner have not been calculated.</p> : <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 14 }}>
          <div className="kpi"><div className="value">{exec_.ai_overall?.toFixed(2) ?? 'N/A'}</div><div className="label">AI Overall Score /100</div></div>
          <div className="kpi"><div className="value">{exec_.human_overall?.toFixed(2) ?? 'N/A'}</div><div className="label">Human Overall Score /100</div></div>
          <div className="kpi"><div className="value">{(exec_.difference)?.toFixed(2) ?? 'N/A'}</div><div className="label">Difference</div></div>
          <div className="kpi"><div className="value">{exec_.percentage_difference?.toFixed(2) ?? 'N/A'}%</div><div className="label">Percentage Difference</div></div>
        </div>}
        {!rawExecution && <>
          <p style={{ marginTop: 12 }}>
            Overall comparison: <Pill color={exec_.direction?.toLowerCase()}>{displayDirection(exec_.direction)}</Pill>
          </p>
          <p className="obs muted">{exec_.neutral_statement}</p>
        </>}
      </div>

      {/* SECTION 3 — PREFLIGHT VALIDATION */}
      <div className="card" style={{ marginBottom: 18 }}>
        <SectionTitle>3. Preflight Validation</SectionTitle>
        <table className="report-status-table">
          <thead><tr><th>Variant</th><th>Status</th><th>Message</th></tr></thead>
          <tbody>
            {report.preflight.ai.map((p, i) => <tr key={`ai-${i}`}><td>AI</td><td className="nowrap"><Pill color="ai">{p.status}</Pill></td><td className="wrap-text">{p.message}</td></tr>)}
            {report.preflight.human.map((p, i) => <tr key={`human-${i}`}><td>Human</td><td className="nowrap"><Pill color="human">{p.status}</Pill></td><td className="wrap-text">{p.message}</td></tr>)}
          </tbody>
        </table>
      </div>

      {/* SECTION 4 — SIX-DIMENSION COMPARISON */}
      {!rawExecution && <div className="card" style={{ marginBottom: 18 }}>
        <SectionTitle>3. Six-Dimension Comparison</SectionTitle>
        <table>
          <thead><tr><th>Dimension</th><th className="ai-col">AI</th><th className="human-col">Human</th><th>Difference</th><th>Direction</th></tr></thead>
          <tbody>
            {report.six_dimensions.map((d) => (
              <tr key={d.dimension}>
                <td>{d.dimension}</td>
                <td className="ai-col">{d.ai_value?.toFixed(3) ?? 'N/A'}</td>
                <td className="human-col">{d.human_value?.toFixed(3) ?? 'N/A'}</td>
                <td>{d.difference?.toFixed(3) ?? 'N/A'}</td>
                <td><Pill color={d.direction?.toLowerCase()}>{displayDirection(d.direction)}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>}

      {/* SECTION 4 — RELIABILITY */}
      <div className="card" style={{ marginBottom: 18 }}>
        <SectionTitle>4. Reliability</SectionTitle>
        <p className="obs"><strong>Formula:</strong> {report.reliability.formula}</p>
        {(['ai', 'human'] as const).map((variant) => (
          <div key={variant} style={{ marginBottom: 12 }}>
            <div className="section-title" style={{ marginTop: 0 }}>{variant === 'ai' ? 'AI' : 'Human'} Execution</div>
            <table>
              <thead><tr><th>Total</th><th>Passed</th><th>Failed</th><th>Errors</th><th>Timeouts</th><th>Pass Rate</th></tr></thead>
              <tbody>
                <tr>
                  <td>{report.reliability[variant].total_test_cases}</td>
                  <td>{report.reliability[variant].passed_count}</td>
                  <td>{report.reliability[variant].failed_count}</td>
                  <td>{report.reliability[variant].error_count}</td>
                  <td>{report.reliability[variant].timeout_count}</td>
                  <td>{report.reliability[variant].pass_rate?.toFixed(2) ?? 'N/A'}%</td>
                </tr>
              </tbody>
            </table>
            <div style={{ marginTop: 8 }}>
              <strong>Test Case Results:</strong>
              <table>
                <thead><tr><th>Test Case ID</th><th>Input</th><th>Status</th><th>Time (ms)</th><th>Actual</th><th>Expected</th><th>Error</th></tr></thead>
                <tbody>
                  {report.reliability[variant].cases.map((c, i) => (
                    <tr key={i}>
                      <td>{c.test_case_id}</td>
                      <td className="wrap-text">{c.input ?? 'N/A'}</td>
                      <td><Pill color={c.status === 'PASS' ? 'pass' : c.status === 'ERROR' ? 'err' : c.status === 'TIMEOUT' ? 'fail' : 'fail'}>{c.status}</Pill></td>
                      <td>{c.execution_time_ms ?? 'N/A'}</td>
                      <td>{c.actual_output}</td>
                      <td>{c.expected_output}</td>
                      <td>{c.error}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}
      </div>

      {/* SECTION 5 — PERFORMANCE */}
      <div className="card" style={{ marginBottom: 18 }}>
        <SectionTitle>5. Performance</SectionTitle>
        <p className="obs">{report.performance.note}</p>
        <table>
          <thead><tr><th></th><th className="ai-col">AI</th><th className="human-col">Human</th></tr></thead>
          <tbody>
            <tr><td>Execution Time (ms)</td><td className="ai-col">{report.performance.ai.execution_time_ms}</td><td className="human-col">{report.performance.human.execution_time_ms}</td></tr>
            <tr><td>Status</td><td className="ai-col">{report.performance.ai.execution_status}</td><td className="human-col">{report.performance.human.execution_status}</td></tr>
            <tr><td>Normalized Score</td><td className="ai-col">{report.performance.ai.normalized_value?.toFixed(3) ?? 'N/A'}</td><td className="human-col">{report.performance.human.normalized_value?.toFixed(3) ?? 'N/A'}</td></tr>
          </tbody>
        </table>
      </div>

      {!rawExecution && <>
      {/* SECTION 6 — MAINTAINABILITY */}
      <div className="card" style={{ marginBottom: 18 }}>
        <SectionTitle>6. Maintainability</SectionTitle>
        <p className="obs"><strong>Formula:</strong> {report.maintainability.formula}</p>
        {(['ai', 'human'] as const).map((variant) => (
          <div key={variant} style={{ marginBottom: 12 }}>
            <div className="section-title" style={{ marginTop: 0 }}>{variant === 'ai' ? 'AI' : 'Human'} Maintainability</div>
            <p><strong>Final Score: {report.maintainability[variant].final_score?.toFixed(3) ?? 'N/A'} /100</strong></p>
            <table>
              <thead><tr><th>Component</th><th>Raw Value</th><th>Ref Min</th><th>Ref Max</th><th>Normalized</th><th>Weight</th><th>Contribution</th></tr></thead>
              <tbody>
                {Object.entries(report.maintainability[variant].components).map(([name, comp]) => (
                  <tr key={name}>
                    <td>{name}</td>
                    <td>{(comp as MaintainabilityComponent).raw_value}</td>
                    <td>{(comp as MaintainabilityComponent).reference_min}</td>
                    <td>{(comp as MaintainabilityComponent).reference_max}</td>
                    <td>{(comp as MaintainabilityComponent).normalized_score.toFixed(3)}</td>
                    <td>{(comp as MaintainabilityComponent).weight}</td>
                    <td>{(comp as MaintainabilityComponent).weighted_contribution.toFixed(3)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </div>

      {/* SECTION 7 — SECURITY */}
      <div className="card" style={{ marginBottom: 18 }}>
        <SectionTitle>7. Security</SectionTitle>
        <p className="obs">{report.security.note}</p>
        {(['ai', 'human'] as const).map((variant) => (
          <div key={variant} style={{ marginBottom: 12 }}>
            <div className="section-title" style={{ marginTop: 0 }}>{variant === 'ai' ? 'AI' : 'Human'} Security</div>
            <p><strong>Findings Count:</strong> {report.security[variant].count}</p>
            {report.security[variant].tool_status && <p className="obs"><strong>Tool Status:</strong> {report.security[variant].tool_status}</p>}
            {report.security[variant].findings.length > 0 && (
              <table>
                <thead><tr><th>Tool</th><th>Severity</th><th>Rule</th><th>Message</th><th>Location</th></tr></thead>
                <tbody>
                  {report.security[variant].findings.map((f, i) => (
                    <tr key={i}>
                      <td>{f.tool}</td>
                      <td><Pill color={f.severity === 'high' || f.severity === 'medium' ? 'err' : 'pass'}>{f.severity}</Pill></td>
                      <td>{f.rule}</td>
                      <td>{f.message}</td>
                      <td>{f.location}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        ))}
      </div>

      {/* SECTION 8 — COMPLEXITY */}
      <div className="card" style={{ marginBottom: 18 }}>
        <SectionTitle>8. Complexity</SectionTitle>
        <p className="obs">{report.complexity.note}</p>
        <table>
          <thead><tr><th>Metric</th><th className="ai-col">AI Raw</th><th className="human-col">Human Raw</th><th>AI Normalized</th><th>Human Normalized</th></tr></thead>
          <tbody>
            {Object.keys(report.complexity.ai).map((metric) => (
              <tr key={metric}>
                <td>{metric}</td>
                <td className="ai-col">{report.complexity.ai[metric]}</td>
                <td className="human-col">{report.complexity.human[metric]}</td>
                <td>{report.complexity.normalized_ai?.toFixed(3) ?? 'N/A'}</td>
                <td>{report.complexity.normalized_human?.toFixed(3) ?? 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* SECTION 9 — CODE QUALITY */}
      <div className="card" style={{ marginBottom: 18 }}>
        <SectionTitle>9. Code Quality</SectionTitle>
        <p className="obs">{report.code_quality.note}</p>
        {(['ai', 'human'] as const).map((variant) => (
          <div key={variant} style={{ marginBottom: 12 }}>
            <div className="section-title" style={{ marginTop: 0 }}>{variant === 'ai' ? 'AI' : 'Human'} Code Quality</div>
            <p><strong>Findings Count:</strong> {report.code_quality[variant].count}</p>
            {report.code_quality[variant].tool_status && <p className="obs"><strong>Tool Status:</strong> {report.code_quality[variant].tool_status}</p>}
            {report.code_quality[variant].findings.length > 0 && (
              <table>
                <thead><tr><th>Tool</th><th>Rule</th><th>Severity</th><th>Message</th><th>Location</th></tr></thead>
                <tbody>
                  {report.code_quality[variant].findings.map((f, i) => (
                    <tr key={i}>
                      <td>{f.tool_name}</td>
                      <td>{f.rule}</td>
                      <td><Pill color={f.severity === 'high' || f.severity === 'medium' ? 'err' : 'pass'}>{f.severity}</Pill></td>
                      <td>{f.message}</td>
                      <td>{f.source_location}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        ))}
      </div>

      {/* SECTION 10 — SCORING CALCULATION */}
      <div className="card" style={{ marginBottom: 18 }}>
        <SectionTitle>10. Scoring Calculation</SectionTitle>
        <p className="obs"><strong>Formula:</strong> {report.scoring_calculation.formula}</p>
        {(['ai', 'human'] as const).map((variant) => (
          <div key={variant} style={{ marginBottom: 12 }}>
            <div className="section-title" style={{ marginTop: 0 }}>{variant === 'ai' ? 'AI' : 'Human'} Dimension Scores</div>
            <table>
              <thead><tr><th>Dimension</th><th>Raw Value</th><th>Normalized</th><th>Pop Min</th><th>Pop Max</th><th>Pop N</th><th>Weight</th><th>Weighted Contribution</th></tr></thead>
              <tbody>
                {report.scoring_calculation[variant].dimensions.map((d) => (
                  <tr key={d.dimension}>
                    <td>{d.dimension}</td>
                    <td>{d.raw_value?.toFixed(3) ?? 'N/A'}</td>
                    <td>{d.normalized_value?.toFixed(3) ?? 'N/A'}</td>
                    <td>{d.normalization_population_min?.toFixed(3) ?? 'N/A'}</td>
                    <td>{d.normalization_population_max?.toFixed(3) ?? 'N/A'}</td>
                    <td>{d.normalization_population_n ?? 'N/A'}</td>
                    <td>{d.weight?.toFixed(2) ?? 'N/A'}</td>
                    <td>{d.weighted_contribution?.toFixed(3) ?? 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p style={{ marginTop: 8 }}><strong>Overall Score: {report.scoring_calculation[variant].overall_score?.toFixed(3) ?? 'N/A'} /100</strong></p>
          </div>
        ))}
      </div>

      {/* SECTION 11 — NORMALIZATION */}
      <div className="card" style={{ marginBottom: 18 }}>
        <SectionTitle>11. Normalization Explanation</SectionTitle>
        <p><strong>Methodology:</strong> {report.normalization.methodology}</p>
        <p><strong>Neutral Value:</strong> {report.normalization.neutral_value}</p>
        <p><strong>Higher-is-Better:</strong> {report.normalization.higher_is_better_formula}</p>
        <p><strong>Lower-is-Better:</strong> {report.normalization.lower_is_better_formula}</p>
        <p className="obs muted">{report.normalization.note}</p>
      </div>

      {/* SECTION 12 — AI VS HUMAN */}
      <div className="card" style={{ marginBottom: 18 }}>
        <SectionTitle>12. AI vs Human Analysis</SectionTitle>
        <table>
          <thead><tr><th>Metric</th><th className="ai-col">AI</th><th className="human-col">Human</th><th>Difference</th><th>% Diff</th><th>Direction</th></tr></thead>
          <tbody>
            {report.ai_vs_human.map((r) => (
              <tr key={r.metric}>
                <td>{r.metric}</td>
                <td className="ai-col">{r.ai_value?.toFixed(3) ?? 'N/A'}</td>
                <td className="human-col">{r.human_value?.toFixed(3) ?? 'N/A'}</td>
                <td>{r.difference?.toFixed(3) ?? 'N/A'}</td>
                <td>{r.percentage_difference?.toFixed(2) ?? 'N/A'}%</td>
                <td><Pill color={r.direction?.toLowerCase()}>{displayDirection(r.direction)}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* SECTION 13 — STATISTICAL ANALYSIS */}
      <div className="card" style={{ marginBottom: 18 }}>
        <SectionTitle>13. Statistical Analysis</SectionTitle>
        <p><strong>Alpha:</strong> {report.statistical_analysis.alpha}</p>
        {!report.statistical_analysis.has_sufficient_data && (
          <p className="obs">Insufficient data for statistical analysis. Statistical analysis requires multiple paired comparisons.</p>
        )}
        {report.statistical_analysis.has_sufficient_data && (
          <table>
            <thead><tr><th>Metric</th><th>N Paired</th><th>Statistic</th><th>P-Value</th><th>Significant</th><th>Effect Size</th><th>Status</th></tr></thead>
            <tbody>
              {Object.entries(report.statistical_analysis.per_metric).map(([metric, data]: [string, any]) => (
                <tr key={metric}>
                  <td>{metric}</td>
                  <td>{data.n_paired}</td>
                  <td>{data.statistic ?? 'N/A'}</td>
                  <td>{data.p_value ?? 'N/A'}</td>
                  <td>{data.significant ? 'Yes' : 'No'}</td>
                  <td>{data.effect_size ?? 'N/A'}</td>
                  <td>{data.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
      </>}

      {/* SECTION 14 — TEST CASE RESULTS */}
      <div className="card" style={{ marginBottom: 18 }}>
        <SectionTitle>14. Test Case Results</SectionTitle>
        <table>
          <thead><tr><th>#</th><th className="ai-col">AI Status</th><th className="human-col">Human Status</th></tr></thead>
          <tbody>
            {report.test_cases.ai.map((tc, i) => {
              const h = report.test_cases.human[i];
              return (
                <tr key={tc.test_case_id}>
                  <td>{tc.test_case_id}</td>
                  <td className="ai-col"><Pill color={tc.status === 'PASS' ? 'pass' : tc.status === 'ERROR' ? 'err' : 'fail'}>{tc.status}</Pill></td>
                  <td className="human-col"><Pill color={h.status === 'PASS' ? 'pass' : h.status === 'ERROR' ? 'err' : 'fail'}>{h.status}</Pill></td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* SECTION 15 — INTERPRETATION */}
      <div className="card" style={{ marginBottom: 18 }}>
        <SectionTitle>15. Research Interpretation</SectionTitle>
        <p>{rawExecution ? 'Raw execution data only; no aggregate scores or winner are available for this record.' : report.interpretation.statement}</p>
        <p className="obs muted">{report.interpretation.disclaimer}</p>
      </div>
    </div>
  );
}
