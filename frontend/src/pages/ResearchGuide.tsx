import { api } from '../api';
import { Problem } from '../types';

export default function ResearchGuide() {
  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2 className="page-title">Research Guide</h2>
          <p className="page-sub">How to use the Research Code Evaluator for empirical data collection</p>
        </div>
        <span className="meta-pill">Research handbook</span>
      </div>

      <div className="section-card page-intro">
        <div className="doc-section">
          <h3>What this application measures</h3>
          <p>
            This application is a <strong>research instrument</strong> for comparing AI-generated code with human-written code. It does <strong>not</strong> generate AI code, call AI APIs, or require AI keys. The researcher pastes externally generated AI code and human code into the interface.
          </p>
        </div>
      </div>

      <div className="section-card">
        <div className="doc-section">
          <h3>AI vs Human comparison</h3>
          <p>For each comparison, both AI and human code solve the <strong>same problem</strong>, use the <strong>same language</strong>, and are executed against the <strong>same predefined test cases</strong> under identical conditions.</p>
        </div>
        <div className="doc-section">
          <h3>Controlled experiment</h3>
          <p>Every comparison controls for problem, language, test cases, execution timeout, analysis tools, and scoring methodology. This ensures observed differences are attributable to the code itself, not the measurement process.</p>
        </div>
        <div className="doc-section">
          <h3>How to prepare AI code</h3>
          <p>Generate AI code externally using systems such as ChatGPT, Claude, Gemini, or other AI coding assistants. Copy the generated source code into the <strong>AI-Written Code</strong> editor. Enter the AI system name (e.g., &quot;ChatGPT&quot;) in the provided field.</p>
        </div>
        <div className="doc-section">
          <h3>How to prepare human code</h3>
          <p>Write or collect human-written code that solves the same problem. Paste it into the <strong>Human-Written Code</strong> editor. No human name or participant ID is required.</p>
        </div>
      </div>

      <div className="section-card">
        <div className="doc-section">
          <h3>Required function / method contract</h3>
          <p>Pasted code must expose the entry function/method shown in the problem definition.</p>
          <ul>
            <li><strong>Python:</strong> <code>def solve(data: str) -&gt; str:</code></li>
            <li><strong>Java:</strong> <code>public static String solve(String data)</code> inside <code>public class Solution</code></li>
          </ul>
          <p>The function receives the test-case input as a <strong>string</strong> and must return a <strong>string</strong>. Do not use <code>input()</code> or <code>print()</code>.</p>
        </div>
        <div className="doc-section">
          <h3>Test cases</h3>
          <p>Each problem has predefined test cases. The same test cases run for both AI and human code. Test case results are displayed as:</p>
          <ul>
            <li><strong>PASS</strong> — output matches expected</li>
            <li><strong>FAIL</strong> — code ran but output is incorrect</li>
            <li><strong>ERROR</strong> — compile/runtime/parse error</li>
            <li><strong>TIMEOUT</strong> — execution exceeded 10 seconds</li>
          </ul>
        </div>
        <div className="doc-section">
          <h3>Six metrics</h3>
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
          <h3>Scoring and normalization</h3>
          <p>Each dimension is normalized to 0–100 using dataset min/max normalization. Weights are defined in <code>config/scoring.yaml</code>. The overall score is the weighted sum of normalized dimension scores. Raw values are always preserved.</p>
        </div>
        <div className="doc-section">
          <h3>Statistics</h3>
          <p>Statistical analysis uses the <strong>Wilcoxon Signed-Rank Test</strong> with &alpha; = 0.05. Results are reported only when sufficient paired observations exist.</p>
        </div>
        <div className="doc-section">
          <h3>Pilot vs Research Data</h3>
          <p><strong>Pilot data</strong> is used to validate the system. <strong>Research data</strong> is collected for analysis. The database maintains a pilot/research classification. Dashboard and reports can filter by dataset type.</p>
        </div>
        <div className="doc-section">
          <h3>Reports and exports</h3>
          <p>Each comparison generates a detailed report. Data can be exported as Excel (.xlsx), CSV, or JSON. The Excel workbook contains multiple sheets for analysis and dissertation use.</p>
        </div>
        <div className="doc-section">
          <h3>Reproducibility</h3>
          <p>Reports capture application version, timestamp, language versions, tool versions, scoring configuration, timeout, and dataset classification. Store the database file and exports together for full reproducibility.</p>
        </div>
        <div className="doc-section">
          <h3>Important notes</h3>
          <ul>
            <li>Do not use <code>input()</code> or <code>print()</code> in submitted code.</li>
            <li>Java code must declare <code>public class Solution</code>.</li>
            <li>The application runs code in an isolated subprocess with a 10-second timeout.</li>
            <li>No fabricated data is ever generated. Tool-unavailable states are recorded, not substituted with zeros.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
