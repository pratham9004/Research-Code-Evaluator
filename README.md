# Research Code Evaluator

A research instrument for the MCA study:
**"An Empirical Study on the Reliability, Security, and Maintainability of AI-Generated Code in Software Development."**

The application is **not** an AI generator. Researchers paste AI-generated code
(obtained externally from ChatGPT, Claude, Gemini, etc.) and human-written code,
then the system executes both against the **same predefined test cases**, measures
research metrics, compares AI vs Human, stores results, and updates the dashboard.

## Workflow

Dashboard → Solve Problems → Select problem → Paste AI + Human code →
**Submit & Compare** → same test cases → execute → analyse → compare →
report → stored → dashboard updated → Reports.

## Tech stack

- **Backend:** Python 3.11, FastAPI, SQLAlchemy, SQLite, SciPy
- **Frontend:** React 18, TypeScript, Vite, Chart.js, CodeMirror
- **Analysis (Python):** radon (complexity), Ruff (code quality), Bandit (security)
- **Analysis (Java):** lightweight parser (metrics) + PMD 7.x (code quality) + SpotBugs 4.x (security)
- No Redis, Celery, queues, auth, or AI APIs.

## Project structure

```
config/        scoring.yaml (weights/directions), problems.yaml (problem bank)
backend/       db/ engine/ analysis/ scoring/ statistics/ api/ main.py
frontend/      src/ (pages, components, api)
database/      research.db (created at runtime, gitignored)
tests/         pytest backend tests
docs/          FIVE source-of-truth research documents (do not edit)
```

## Local development

### 1. Backend

```powershell
python -m venv backend/.venv
.\backend\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
python -m database.migrate       # apply any schema migrations
python -m uvicorn backend.main:app --port 8000
```

> **Note:** Do **not** use `--reload` in production. The file watcher triggers
> on `database/tmp` harness writes and restarts the server mid-comparison.

The API is available at http://localhost:8000 (Swagger docs at /docs).
The problem bank is seeded automatically on startup.

### 2. Frontend

```powershell
cd frontend
npm install
npm run dev          # dev server with proxy to :8000
# or build and let the FastAPI server serve it:
npm run build        # outputs frontend/dist, served at http://localhost:8000/
```

Open http://localhost:8000. The dashboard shows "No comparison data available
yet." until the first real comparison is completed.

## Database

SQLite file at `database/research.db`, auto-created and seeded on first run.
Stores: problems, test cases, comparisons, execution results, test-case results,
static-analysis results, complexity data, security findings, scores, and
comparison results — raw measurements and calculated values are kept separately
per `docs/04_DATABASE_DESIGN.md`. The production database ships empty (no fake
research data).

## Export

`GET /api/export/dataset?format=csv` or `?format=json` exports the full research
dataset for Python/R/Excel/SPSS analysis.

## Tests

```powershell
# Backend (uses an isolated temp database)
python -m pytest tests/ -q

# Frontend
cd frontend
npm test
npm run build
```

## Required external tools for analysis

- **Python execution & analysis:** Python 3.11+ on PATH; `radon`, `ruff`,
  `bandit` (all pip-installable). Already satisfied in this environment.
- **Java execution & analysis:** a JDK (`java`, `javac`) on PATH plus PMD
  (`pmd.bat`) and SpotBugs (`spotbugs.bat`) on PATH for full Java analysis.
  If Java is not installed, Java comparisons fail gracefully (stored as ERROR)
  and Java static-analysis tools are skipped with a clear "tool unavailable"
  note — never fabricated results.

## Notes / design decisions

- **Execution contract (internal only):** pasted code must expose a function
  `solve(data: str) -> str` (Python) / `public static String solve(String data)`
  (Java). The UI shows the required signature per problem; the researcher never
  configures a harness.
- **Scoring** follows `docs/03_METRICS_AND_SCORING.md`: the maintainability
  composite uses the documented four-component weighted formula; per-dimension
  normalization uses the research dataset min/max with safe divide-by-zero
  handling; overall score weights live in `config/scoring.yaml`.
- **Statistics:** Wilcoxon Signed-Rank (SciPy) across accumulated comparisons,
  α = 0.05, reported only when sufficient paired observations exist.
