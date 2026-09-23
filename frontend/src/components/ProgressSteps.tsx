const STEPS = [
  'Running AI code',
  'Running Human code',
  'Running test cases',
  'Analysing code',
  'Comparing results',
  'Generating report',
  'Saving research data',
];

export default function ProgressSteps({ active }: { active: number }) {
  return (
    <div className="progress-overlay">
      <div className="spinner" />
      <h3>Evaluating comparison…</h3>
      {STEPS.map((s, i) => (
        <div key={s} className={`step ${i < active ? 'done' : i === active ? 'active' : ''}`}>
          <span className="dot" />
          <span>{s} {i < active ? '✓' : ''}</span>
        </div>
      ))}
    </div>
  );
}
