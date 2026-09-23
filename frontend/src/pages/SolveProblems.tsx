import { useEffect, useState } from 'react';
import { api } from '../api';
import { Problem, Report } from '../types';
import CodeEditor from '../components/CodeEditor';
import ProgressSteps from '../components/ProgressSteps';

const LANG_LABELS: Record<string, string> = {
  python: 'Python',
  java: 'Java',
  cpp: 'C++',
  javascript: 'JavaScript',
};

/** Return the per-language starter template for the selected problem+language. */
function getStarter(p: Problem, lang: string): string {
  if (lang === 'java' && p.starter_template_java) return p.starter_template_java;
  if (lang === 'cpp' && p.starter_template_cpp) return p.starter_template_cpp;
  if (lang === 'javascript' && p.starter_template_javascript) return p.starter_template_javascript;
  if (lang === 'python' && p.starter_template_python) return p.starter_template_python;
  return p.starter_template ?? '';
}

/** Return the function signature string for display. */
function getSignature(p: Problem, lang: string): string {
  if (lang === 'java') return p.signature_java ?? '';
  if (lang === 'cpp') return p.signature_cpp ?? '';
  if (lang === 'javascript') return p.signature_javascript ?? '';
  return p.signature_python ?? '';
}

/** Typed-model contract hint per language. */
function TypedHint({ lang, p }: { lang: string; p: Problem }) {
  const sig = getSignature(p, lang);
  return (
    <div className="card" style={{ marginTop: 10, padding: '10px 14px', background: '#f0fdf4', border: '1px solid #86efac', borderRadius: 6 }}>
      <div style={{ fontWeight: 600, color: '#166534', marginBottom: 4 }}>
        ✏ Write Only The Solution Function
      </div>
      <div style={{ fontSize: 13, color: '#14532d', lineHeight: 1.6 }}>
        {lang === 'python' && <>
          Implement <strong>only</strong> the function: <code style={{ background: '#dcfce7', padding: '1px 4px', borderRadius: 3 }}>{sig}</code><br />
          The harness handles input parsing, function calling, and output comparison.<br />
          <strong>Do NOT add</strong> <code>input()</code>, <code>print()</code>, or a <code>main()</code> block.
        </>}
        {lang === 'java' && <>
          Implement <strong>only</strong> the method inside <code>public class Solution</code>: <code style={{ background: '#dcfce7', padding: '1px 4px', borderRadius: 3 }}>{sig}</code><br />
          The harness compiles and invokes your method via reflection.<br />
          <strong>Do NOT add</strong> <code>main()</code>, <code>Scanner</code>, or <code>System.in</code> reading.
        </>}
        {lang === 'cpp' && <>
          Implement <strong>only</strong> the function: <code style={{ background: '#dcfce7', padding: '1px 4px', borderRadius: 3 }}>{sig}</code><br />
          The harness provides <code>main()</code> and all I/O. Include any standard headers you need.<br />
          <strong>Do NOT add</strong> a <code>main()</code> function — it will cause a compilation error.
        </>}
        {lang === 'javascript' && <>
          Implement <strong>only</strong> the function and export it: <code style={{ background: '#dcfce7', padding: '1px 4px', borderRadius: 3 }}>{sig}</code><br />
          Export via <code>module.exports = {'{ functionName }'}</code>.<br />
          <strong>Do NOT use</strong> <code>process.stdin</code>, <code>readline</code>, or interactive I/O.
        </>}
        <br />
        <span style={{ color: '#166534', fontStyle: 'italic' }}>
          Both AI and Human code run through the identical harness and test cases.
        </span>
      </div>
    </div>
  );
}

/** Legacy-model contract hint. */
function LegacyHint({ lang, entry }: { lang: string; entry: string }) {
  return (
    <div className="card" style={{ marginTop: 10, padding: '10px 14px', background: '#fefce8', border: '1px solid #fbbf24', borderRadius: 6 }}>
      <div style={{ fontWeight: 600, color: '#92400e', marginBottom: 4 }}>
        ⚠ Execution Contract
      </div>
      <div style={{ fontSize: 13, color: '#78350f', lineHeight: 1.6 }}>
        {lang === 'java' ? (
          <>Implement <strong>only</strong> <code>Solution.{entry}(String data)</code> inside <code>public class Solution</code>.<br />
          <strong>Do NOT add</strong> <code>main()</code>, <code>Scanner</code>, or interactive I/O.</>
        ) : lang === 'cpp' ? (
          <>Implement <strong>only</strong> <code>{'string ' + entry + '(const string& data)'}</code>.<br />
          <strong>Do NOT add</strong> a <code>main()</code> function.</>
        ) : lang === 'javascript' ? (
          <>Implement <strong>only</strong> <code>function {entry}(data)</code> and export via <code>module.exports = {'{ ' + entry + ' }'}</code>.</>
        ) : (
          <>Implement <strong>only</strong> <code>def {entry}(data: str) → str</code>.<br />
          <strong>Do NOT use</strong> <code>input()</code> or interactive I/O.</>
        )}
        <br />
        <span style={{ color: '#92400e' }}>AI and Human code are evaluated under identical conditions.</span>
      </div>
    </div>
  );
}

export default function SolveProblems({ onReport }: { onReport: (r: Report) => void }) {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [selectedId, setSelectedId] = useState<string>('');
  const [language, setLanguage] = useState<string>('python');
  const [aiName, setAiName] = useState<string>('ChatGPT');
  const [aiCode, setAiCode] = useState<string>('');
  const [humanCode, setHumanCode] = useState<string>('');
  const [busy, setBusy] = useState(false);
  const [step, setStep] = useState(0);
  const [error, setError] = useState<string>('');

  useEffect(() => { api.getProblems().then(setProblems); }, []);

  const selected = problems.find((p) => p.problem_id === selectedId);
  const isTyped = selected?.harness_type === 'typed';

  function onSelectProblem(id: string) {
    const p = problems.find((x) => x.problem_id === id);
    setSelectedId(id);
    const lang = p?.supported_languages[0] ?? 'python';
    setLanguage(lang);
    if (p) {
      const skeleton = getStarter(p, lang);
      setAiCode(skeleton);
      setHumanCode(skeleton);
    } else {
      setAiCode('');
      setHumanCode('');
    }
    setError('');
  }

  function onSelectLanguage(lang: string) {
    setLanguage(lang);
    if (selected) {
      const skeleton = getStarter(selected, lang);
      setAiCode(skeleton);
      setHumanCode(skeleton);
    }
  }

  async function submit() {
    if (!selected) return setError('Please select a problem.');
    if (!language) return setError('Please select a language.');
    if (!aiName.trim()) return setError('Please enter the AI system name.');
    if (!aiCode.trim() || !humanCode.trim()) return setError('Both AI and Human code are required.');

    setBusy(true);
    setError('');
    let i = 0;
    const timer = setInterval(() => { i = Math.min(i + 1, 6); setStep(i); }, 450);

    try {
      const report: Report = await api.submitComparison({
        problem_id: selected.problem_id,
        language,
        ai_name: aiName,
        ai_code: aiCode,
        human_code: humanCode,
      });
      clearInterval(timer);
      setBusy(false);
      onReport(report);
    } catch (e: any) {
      clearInterval(timer);
      setBusy(false);
      setError(e.message || 'Submission failed.');
    }
  }

  return (
    <div className="page">
      <h2 className="page-title">Solve Problems</h2>
      <p className="page-sub">
        Select a problem, paste the AI-written solution and the Human-written solution,
        then compare both across 6 research dimensions.
      </p>

      <div className="problem-meta">
        <label>Problem</label>
        <select value={selectedId} onChange={(e) => onSelectProblem(e.target.value)}>
          <option value="">— Select a problem —</option>
          {problems.map((p) => (
            <option key={p.problem_id} value={p.problem_id}>
              {p.problem_id} · {p.title} ({p.difficulty})
            </option>
          ))}
        </select>

        {selected && (
          <>
            <div style={{ marginTop: 12 }}>
              <span className="badge">{selected.category}</span>
              <span className="badge">{selected.difficulty}</span>
              <span className="badge">{selected.supported_languages.map(l => LANG_LABELS[l] || l).join(', ')}</span>
              <span className="badge">{selected.test_case_count} test cases</span>
              <span className="badge">v{selected.version}</span>
              {isTyped && <span className="badge" style={{ background: '#dbeafe', color: '#1e40af' }}>Typed Functions</span>}
            </div>

            <p style={{ marginTop: 12 }}>{selected.description}</p>

            {selected.input_spec && (
              <div className="signature" style={{ marginTop: 8 }}>
                <strong>Input:</strong> {selected.input_spec}
              </div>
            )}
            {selected.output_spec && (
              <div className="signature" style={{ marginTop: 4 }}>
                <strong>Output:</strong> {selected.output_spec}
              </div>
            )}
            {selected.constraints && (
              <div className="signature" style={{ marginTop: 4 }}>
                <strong>Constraints:</strong> {selected.constraints}
              </div>
            )}

            {/* Language selector */}
            {selected.supported_languages.length > 1 && (
              <div style={{ marginTop: 12 }}>
                <label>Language</label>
                <select value={language} onChange={(e) => onSelectLanguage(e.target.value)}>
                  {selected.supported_languages.map((l) => (
                    <option key={l} value={l}>{LANG_LABELS[l] || l}</option>
                  ))}
                </select>
              </div>
            )}

            {/* Function signature */}
            <div className="signature" style={{ marginTop: 10 }}>
              <strong>Function signature ({LANG_LABELS[language] || language}):</strong><br />
              <code style={{ fontSize: 13 }}>{getSignature(selected, language)}</code>
            </div>

            {/* Contract hint */}
            {isTyped
              ? <TypedHint lang={language} p={selected} />
              : <LegacyHint lang={language} entry={selected.entry_function} />
            }

            {/* Test cases table */}
            {selected.test_cases && selected.test_cases.length > 0 && (
              <div style={{ marginTop: 12 }}>
                <div className="section-title" style={{ marginBottom: 6 }}>Controlled Test Cases</div>
                <table>
                  <thead><tr><th>#</th><th>Input</th><th>Expected Output</th><th>Type</th></tr></thead>
                  <tbody>
                    {selected.test_cases.map((tc, i) => (
                      <tr key={tc.test_case_id}>
                        <td>{i + 1}</td>
                        <td className="code-cell">{tc.input}</td>
                        <td className="code-cell">{tc.expected_output}</td>
                        <td>{tc.case_type}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </>
        )}
      </div>

      {selected && (
        <>
          <div className="grid-2">
            {/* AI Editor */}
            <div className="editor-panel">
              <div className="editor-header ai">AI-Written Solution</div>
              <div style={{ padding: 12 }}>
                <label>AI System Name</label>
                <input
                  type="text"
                  value={aiName}
                  onChange={(e) => setAiName(e.target.value)}
                  placeholder="e.g. ChatGPT-4o"
                />
                <label style={{ marginTop: 12 }}>
                  {isTyped
                    ? 'Solution function (replace the placeholder comment with your implementation)'
                    : 'Code'}
                </label>
                <CodeEditor value={aiCode} onChange={setAiCode} language={language} height="360px" />
              </div>
            </div>

            {/* Human Editor */}
            <div className="editor-panel">
              <div className="editor-header human">Human-Written Solution</div>
              <div style={{ padding: 12 }}>
                <label style={{ marginTop: 0 }}>
                  {isTyped
                    ? 'Solution function (replace the placeholder comment with your implementation)'
                    : 'Code'}
                </label>
                <CodeEditor value={humanCode} onChange={setHumanCode} language={language} height="360px" />
              </div>
            </div>
          </div>

          {error && <p className="pill err" style={{ display: 'inline-block', marginTop: 12 }}>{error}</p>}

          <div style={{ marginTop: 16 }}>
            <button className="btn" onClick={submit} disabled={busy}>
              {busy ? 'Processing…' : 'Submit & Compare'}
            </button>
          </div>
        </>
      )}

      {busy && <ProgressSteps active={step} />}
    </div>
  );
}
