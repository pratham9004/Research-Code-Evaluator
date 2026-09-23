import { api } from '../api';

export default function AboutMethodology() {
  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2 className="page-title">Methodology</h2>
          <p className="page-sub">Research instrument methodology and design decisions</p>
        </div>
        <span className="meta-pill">Research design</span>
      </div>

      <div className="section-card page-intro">
        <div className="doc-section">
          <h3>Research instrument</h3>
          <p>The Research Code Evaluator is a research instrument for the MCA study: <em>"An Empirical Study on the Reliability, Security, and Maintainability of AI-Generated Code in Software Development."</em></p>
          <p>The application does <strong>not</strong> generate AI code, call AI APIs, or require AI keys. Researchers paste externally generated AI code and human-written code into the interface.</p>
        </div>
      </div>

      <div className="section-card">
        <div className="doc-section">
          <h3>Controlled comparison design</h3>
          <p>Every comparison controls for:</p>
          <ul>
            <li>Same predefined problem</li>
            <li>Same programming language</li>
            <li>Same predefined test cases</li>
            <li>Same execution timeout (10 seconds)</li>
            <li>Same analysis tools and versions</li>
            <li>Same scoring methodology and weights</li>
          </ul>
          <p>This ensures observed differences are attributable to the code itself, not the measurement process.</p>
        </div>
        <div className="doc-section">
          <h3>Execution contract</h3>
          <p>Pasted code must expose the entry function/method shown in the problem definition:</p>
          <ul>
            <li><strong>Python:</strong> <code>def solve(data: str) -&gt; str:</code></li>
            <li><strong>Java:</strong> <code>public static String solve(String data)</code> inside <code>public class Solution</code></li>
          </ul>
          <p>The function receives the test-case input as a string and must return a string. Do not use <code>input()</code> or <code>print()</code>.</p>
        </div>
      </div>

      <div className="section-card">
        <div className="doc-section">
          <h3>Six evaluation dimensions</h3>
          <ol>
            <li><strong>Reliability</strong> — percentage of test cases passed</li>
            <li><strong>Performance</strong> — execution time under identical conditions</li>
            <li><strong>Maintainability</strong> — composite of cyclomatic complexity, function length, nesting, coupling</li>
            <li><strong>Security</strong> — static security findings (Bandit for Python, SpotBugs for Java)</li>
            <li><strong>Complexity</strong> — cyclomatic complexity and related structural metrics</li>
            <li><strong>Code Quality</strong> — static code-quality findings (Ruff for Python, PMD for Java)</li>
          </ol>
        </div>
        <div className="doc-section">
          <h3>Scoring methodology</h3>
          <p>Each dimension is normalized to 0–100 using dataset min/max normalization. Weights are defined in <code>config/scoring.yaml</code>. The overall score is the weighted sum of normalized dimension scores. Raw values are always preserved.</p>
          <p><strong>Maintainability composite formula:</strong> 0.30 × Cyclomatic Component + 0.20 × Function Length Component + 0.20 × Nesting Component + 0.30 × Coupling Component</p>
        </div>
      </div>

      <div className="section-card">
        <div className="doc-section">
          <h3>Statistical analysis</h3>
          <p>Statistical analysis uses the <strong>Wilcoxon Signed-Rank Test</strong> with &alpha; = 0.05. Results are reported only when sufficient paired observations exist (minimum 2).</p>
        </div>
        <div className="doc-section">
          <h3>Pilot vs research data</h3>
          <p><strong>Pilot data</strong> validates the system. <strong>Research data</strong> is collected for analysis. The database maintains a pilot/research classification at the database level. Dashboard and reports can filter by dataset type.</p>
        </div>
        <div className="doc-section">
          <h3>Reproducibility</h3>
          <p>Reports capture application version, timestamp, language versions, tool versions, scoring configuration, timeout, and dataset classification. Store the database file and exports together for full reproducibility.</p>
        </div>
      </div>

      <div className="section-card">
        <div className="doc-section">
          <h3>Data integrity</h3>
          <ul>
            <li>No fabricated data is ever generated</li>
            <li>Tool-unavailable states are recorded, not substituted with zeros</li>
            <li>Pilot data is clearly marked and separated from research data</li>
            <li>All scores are explainable with traceable normalization populations</li>
            <li>Statistical results are persisted, not recomputed live</li>
          </ul>
        </div>
        <div className="doc-section">
          <h3>Technology stack</h3>
          <ul>
            <li><strong>Backend:</strong> Python 3.11, FastAPI, SQLAlchemy, SQLite, SciPy</li>
            <li><strong>Frontend:</strong> React 18, TypeScript, Vite, Chart.js, CodeMirror</li>
            <li><strong>Analysis (Python):</strong> radon, Ruff, Bandit</li>
            <li><strong>Analysis (Java):</strong> lightweight parser, PMD, SpotBugs</li>
            <li><strong>Exports:</strong> openpyxl (Excel), reportlab (PDF)</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
