# Research Code Evaluator

Research Code Evaluator is a local web application for comparing AI-generated
and human-written implementations of a fixed programming benchmark. It runs
both submissions against the same stored test cases, records execution and
static-analysis measurements, calculates configured comparison scores, and
stores the result in SQLite.

The application does not generate AI or human solutions and does not call AI
services. Researchers supply the code they want to compare.

## Application workflow

1. Open **Dashboard** to review stored comparison summaries.
2. Open **Solve Problems**.
3. Select one problem (`P001`–`P050`) and a language (Python, JavaScript, Java,
   or C++).
4. Enter the AI system name and its code, then enter the matching human code.
   Follow the problem and function signature shown by the page; the backend
   supplies the benchmark execution harness.
5. Click **Submit & Compare**. The backend validates the submissions, executes
   both against the problem's stored test cases, analyzes the code, calculates
   the configured measurements, saves the comparison, and returns its report.
6. Review the comparison report or open **Evaluations** to browse saved
   comparisons, open detailed reports, export an individual PDF, or download
   the full Excel research report.

Other application pages are **Research Guide**, **Methodology**, and **Manage
Data**. Manage Data can permanently delete stored comparisons; review its
confirmation carefully.

The frontend uses these page paths:

| Page | Path |
| --- | --- |
| Dashboard | `/dashboard` |
| Solve Problems | `/solve-problems` |
| Evaluations | `/reports` |
| Comparison report | `/reports/{comparison_id}` |
| Detailed report | `/reports/{comparison_id}/detailed` |
| Research Guide | `/research-guide` |
| Methodology | `/about-methodology` |
| Manage Data | `/manage-data` |

## Technology and prerequisites

- Windows PowerShell is used in the commands below.
- Python 3.11 or newer for the API and Python solution execution.
- Node.js 18 or newer and npm for the React/Vite frontend and Playwright.
- A JDK providing `java` and `javac` to execute Java submissions.
- MSYS2 UCRT64 `g++` for C++ submissions. The executor currently expects
  `C:\msys64\ucrt64\bin\g++.exe`.
- Chromium for Playwright browser tests (`npx playwright install chromium`).

The backend's Python dependencies are listed in `backend/requirements.txt`.
Java quality/security analysis additionally uses PMD and SpotBugs if their
commands are available on `PATH`; the analyzer records when these optional
tools are unavailable. No AI API keys, Redis, Celery, or queue service are
required.

## First-time installation

Run commands from the repository root unless a command changes directory.

### 1. Create the Python environment

```powershell
py -3.11 -m venv backend/.venv
.\backend\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

If PowerShell blocks activation, use the virtual environment's Python directly
in subsequent commands:

```powershell
.\backend\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
```

### 2. Install frontend packages

```powershell
cd frontend
npm ci
cd ..
```

### 3. Install Playwright and Chromium (for browser automation)

The root `package.json` contains Playwright Test. Install its pinned dependency
tree and browser once:

```powershell
npm ci
npx playwright install chromium
```

Backend and frontend installation are independent; Playwright is only needed
when running `e2e` browser automation.

## Run the application in development

Start the backend and frontend in two separate PowerShell terminals. Keep both
terminals open while using the application.

### Terminal 1: backend API

From the repository root:

```powershell
.\backend\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

The API is at `http://127.0.0.1:8000`; interactive API documentation is at
`http://127.0.0.1:8000/docs`.

Do not add `--reload` for normal comparison runs. The executor creates and
removes temporary files under `database/tmp`; a reload watcher can mistake that
activity for source changes and interrupt an evaluation.

### Terminal 2: frontend

From the repository root:

```powershell
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

Open `http://127.0.0.1:5173`. Vite forwards `/api` requests to the backend on
port 8000 as configured in `frontend/vite.config.ts`.

### Production-style local preview

The FastAPI application serves `frontend/dist` when that directory exists. To
build the frontend and serve it from the API port:

```powershell
cd frontend
npm ci
npm run build
cd ..
.\backend\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Then open `http://127.0.0.1:8000`. The frontend development server on port
5173 is not needed in this mode.

## Database and benchmark configuration

- `database/research.db` is the active local SQLite database by default. It
  stores benchmark problems, test cases, comparisons, per-case executions,
  static-analysis findings, complexity/security measurements, scores, and
  statistical results.
- At startup, the backend creates missing schema objects and seeds or
  synchronizes the problem bank from `config/problems.yaml`; it does not clear
  comparison records as routine startup behavior.
- `config/scoring.yaml` is the configured source for score weights,
  normalization directions, and scoring references.
- `database/migrate.py` contains manual schema migrations. It is **not** run
  automatically at startup. Before migrating an existing database, stop the
  backend and make a separate backup. A fresh database is initialized by the
  application and does not need a migration first.
- For a confirmed migration of an existing default database, stop the backend
  and run:

  ```powershell
  Copy-Item database/research.db database/research-before-migration.db
  .\backend\.venv\Scripts\python.exe -m database.migrate
  ```

  Do not overwrite an earlier backup; choose a new backup name if needed.
- Set `RESEARCH_DB_PATH` before starting the backend only when you intend to
  use a different SQLite file. The same path must be used consistently for
  the application session.

The local database can contain real collected research data. It is ignored by
Git; do not delete, replace, or reset it as routine setup. Other `.db` files
may be dated backups or test databases; they are not used by default. Keep
backups outside Git and verify them before any database maintenance.

## Benchmark solutions and research data

`config/problems.yaml` defines the active P001–P050 tasks and test cases. The
benchmark code files are organized under `AI VS HUMAN CODE`:

```text
AI VS HUMAN CODE/
  ChatGPT/{Python,JavaScript,Java,C++}/
  Perplexity/{Python,JavaScript,Java,C++}/
  Grok/{Python,JavaScript,Java,C++}/
  Gemini/{Python,JavaScript,Java,C++}/
  Claude_Sonnet_5/{Python,JavaScript,Java,C++}/
  human code/{python,javascript,java,C++}/
```

These are source inputs for controlled comparisons and the Playwright data
mapping. Preserve the model, language, problem, and human-solution association;
do not use one model's code for another model or edit official human solutions
as part of normal setup. Historical Gemini originals and project audit
snapshots are kept separately in `gemini_original/`, `archive/`, and
`backup_snapshots/`; they are not needed to start the application.

## Playwright E2E automation

`playwright.config.ts` runs Chromium tests serially with one worker. It does
not start the application servers for you. Start the backend and frontend
first, then run commands from the repository root:

```powershell
$env:PLAYWRIGHT_BASE_URL = 'http://127.0.0.1:5173'
npx playwright test --list
npx playwright test e2e/Gemini_TEST --project=chromium
```

There are five model folders under `e2e/`—`ChatGPT_TEST`, `Perplexity_TEST`,
`Grok_TEST`, `Gemini_TEST`, and `Claude_Sonnet_5_TEST`—with one spec for each
of the four languages. Each spec represents that model/language's P001–P050
batch. `e2e/helpers/research-batch.js` maps the official solution files,
performs navigation/submission, waits for evaluation, and checks for existing
completed comparisons to avoid duplicate submissions. The runner reports
problem/model/language and failed step when a submission fails.

**Important:** E2E specs submit comparisons to the database; they are data
collection runs, not read-only UI checks. A full run can create up to 1,000
research comparisons and can take a long time. Back up the intended database
first and run only the model/language batches you mean to collect:

```powershell
# Example: one complete Gemini + Python batch (P001–P050)
npx playwright test e2e/Gemini_TEST/python.spec.js --project=chromium

# All configured batches (up to 1,000 submissions)
npx playwright test --project=chromium

# Open the last HTML report
npx playwright show-report
```

The configured base URL can be changed per session with
`$env:PLAYWRIGHT_BASE_URL = 'http://host:port'`.

## Tests and quality checks

Backend tests use pytest and an isolated temporary database. Pytest is not in
the runtime requirements file, so install it in the backend environment if
needed:

```powershell
.\backend\.venv\Scripts\python.exe -m pip install pytest
.\backend\.venv\Scripts\python.exe -m pytest tests/ -q
```

Frontend tests, type checking, and production build:

```powershell
cd frontend
npm test
npm run typecheck
npm run build
```

## Reports and exports

- The **Evaluations** page downloads the complete Excel workbook using
  `GET /api/export/research-report`.
- Individual comparison reports can be exported as PDF from the report UI;
  the endpoint is `GET /api/export/research-report/pdf/{comparison_id}`.
- The raw comparison dataset is available as CSV or JSON from
  `GET /api/export/dataset?format=csv` or
  `GET /api/export/dataset?format=json`.
- Excel downloads are generated from the current database. Root-level files
  named `research_report*.xlsx` are local export copies, not application input
  files; they can be regenerated from **Evaluations**.

## Important project files

| File or directory | Purpose |
| --- | --- |
| `backend/main.py` | FastAPI app and startup database initialization/seeding |
| `backend/api/` | Problem, comparison, dashboard, export, and data-management APIs |
| `backend/engine/` | Isolated execution and language-specific harnesses |
| `backend/analysis/` | Raw metrics, code-quality, and security analysis |
| `backend/scoring/` | Score normalization and comparison calculations |
| `backend/export/` | Excel and PDF report generation |
| `backend/requirements.txt` | Python runtime dependencies |
| `frontend/src/` | React pages, components, and API client |
| `frontend/package.json` | Frontend dependencies and test/build scripts |
| `frontend/vite.config.ts` | Development server and `/api` proxy configuration |
| `database/migrate.py` | Manual schema upgrades for an existing database |
| `config/problems.yaml` | Active benchmark problem/test-case definitions |
| `config/scoring.yaml` | Active scoring configuration |
| `AI VS HUMAN CODE/` | Model-generated and human benchmark solution inputs |
| `tests/` | Backend API tests |
| `e2e/` | Model/language Playwright submission batches and shared runner |
| `docs/` | Research, benchmark, workflow, and methodology documents |
| `drawable/` | Frontend image assets |

For study methodology and database design, see `docs/01_RESEARCH_METHODOLOGY.md`,
`docs/03_METRICS_AND_SCORING.md`, `docs/04_DATABASE_DESIGN.md`, and
`docs/05_SOFTWARE_REQUIREMENTS.md`. The active problem contracts are in
`config/problems.yaml`.
