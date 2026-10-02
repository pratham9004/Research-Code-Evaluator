# Research Code Evaluator: Root Cause, Cleanup, and Verification Report

**Audit date:** 2026-09-30  
**Scope:** Python ChatGPT vs Human P001–P050 collection, persistence, dashboard, report detail, export, and root-level helper files.

## 1. Root causes found

1. **The earlier Python collector did not reliably execute the submitted modules.** Its function extraction discarded module-level imports/helpers, and the Human source directory mapping was incorrect. It could therefore create misleading/incomplete output instead of representing execution of the original files.
2. **The importer dropped Human per-test-case results.** It retained partial aggregate fields while losing case detail, so the report could not show both sides consistently.
3. **Raw execution data was labeled as a completed comparison.** Import logic treated the presence of executions as comparative completion and wrote directional metric rows and score rows even when no overall comparison score existed. The pre-cleanup backup showed 50 such rows, 100 `ComparisonResult` rows without an overall metric, and 200 score rows whose `overall_score` was null. These records had no defensible overall winner.
4. **The dashboard expects valid overall research results.** It calculates research counts and outcomes from completed comparisons having an `overall` result with non-null values. Metric-level reliability/performance observations without an overall result correctly do not qualify, but were previously marked completed and were confusing to inspect.
5. **Detailed report rendering crashed on missing scores.** The API can return `null` for `final_score`; `DetailedReport.tsx` called `.toFixed()` on that null value. The detailed API returned HTTP 200, but the React render could fail and leave the page blank.
6. **Seed data did not refresh existing test-case mappings.** Existing test-case rows were left unchanged when benchmark YAML changed. P018/P019 therefore had stale stored inputs/expected outputs.
7. **Startup import swept historical result files.** On an empty database, startup could import every matching language/model JSON file in the output directory, including stale datasets. That made automatic database state depend on archived files.

## 2. Database backup and cleanup

- Created a pre-cleanup SQLite snapshot: [research_backup_before_raw_execution_cleanup_20260930.db](database/research_backup_before_raw_execution_cleanup_20260930.db). Its SQLite integrity check passed. It preserves the pre-cleanup state, including the derived rows described above.
- A separate earlier snapshot is [research_backup_before_python_chatgpt_human_20260930.db](database/research_backup_before_python_chatgpt_human_20260930.db).
- Removed only the invalid derived `ComparisonResult` and `Score` rows for the 50 imported raw-execution comparisons (100 and 200 rows respectively). The original comparison containers were retained and correctly marked `execution_only`.
- Preserved all 50 problems, official test cases, original AI/Human source modules, 100 execution records, and 1,000 case-result records. No source code or benchmark dataset was regenerated or modified.
- Seed synchronization now updates the existing test-case input/expected output values by ordinal while preserving their database IDs; it inserts missing cases and does not delete extra rows. A verification found zero mismatches against the official Python YAML cases.
- Re-importing the current dataset is idempotent: it matched the existing 50 comparison identities and reported no duplicate comparisons.

## 3. Collection outcome and current valid counts

The new runner executed the existing Python source modules against the official P001–P050 benchmark cases. It did not fabricate or fill missing results.

| Measure | Current result |
| --- | ---: |
| Problems / paired datasets | 50 |
| AI executions / Human executions | 50 / 50 |
| Stored case executions | 1,000 |
| AI case outcomes | 375 pass, 123 fail, 2 error, 0 timeout |
| Human case outcomes | 498 pass, 2 fail, 0 error, 0 timeout |
| AI evaluation outcomes | 27 pass, 22 fail, 1 error |
| Human evaluation outcomes | 48 pass, 2 fail |
| Official test-case mapping mismatches | 0 |
| Duplicate comparison identities | 0 |
| Valid scored research comparisons | 0 |

The 50 datasets are valid **raw execution datasets**, not scored comparative research records. They have actual pass rates, statuses, outputs, and observed execution times; however, no overall scoring methodology was applied to establish an AI/Human winner. Therefore they remain `execution_only`, have no `Score` or `ComparisonResult` rows, and the dashboard correctly reports 0 scored research comparisons and 0 winners. Missing/error outcomes remain explicit rather than being converted to zero-valued scores.

P050 was inspected through the detailed API: ChatGPT recorded 0/10 passes and Human recorded 10/10 passes, with actual outputs, expected outputs, inputs, and per-case times present. Its comparison status is `execution_only` and its scoring fields are null.

## 4. Files changed and fixes implemented

- [Python_ChatGPT_Human_P001_P050_Tests.py](Python_ChatGPT_Human_P001_P050_Tests.py): new active collector. Loads and syntax-checks the original full modules, executes both variants independently for all official cases, records errors/timeouts, emits JSON/CSV, and imports the raw execution data.
- [backend/db/benchmark_import.py](backend/db/benchmark_import.py): preserves Human case details; supports explicit import paths; defaults to only the active Python raw dataset; persists raw executions as `execution_only`; removes invalid derived scoring rows on raw re-import without deleting source/execution evidence.
- [backend/main.py](backend/main.py): automatic first-run import is restricted to the active raw Python collection file instead of globbing archived datasets.
- [backend/db/seed.py](backend/db/seed.py): synchronizes current official test values without changing existing test-case IDs or deleting cases.
- [backend/api/dashboard.py](backend/api/dashboard.py), [backend/api/comparisons.py](backend/api/comparisons.py): exposes raw execution summaries and stored case input/details; distinguishes raw datasets from scored research counts.
- [backend/export/report.py](backend/export/report.py): reports raw execution dataset counts separately from incomplete/scored research rows.
- [frontend/src/pages/Dashboard.tsx](frontend/src/pages/Dashboard.tsx), [frontend/src/pages/Reports.tsx](frontend/src/pages/Reports.tsx), [frontend/src/pages/DetailedReport.tsx](frontend/src/pages/DetailedReport.tsx), [frontend/src/types.ts](frontend/src/types.ts): show raw statuses, pass/fail/error/timeout counts, times, and actual case details; label unavailable scores/winners as not calculated; guard nullable scores to prevent the blank detail route.
- [tests/test_api.py](tests/test_api.py) and frontend tests under [frontend/src/tests](frontend/src/tests): cover import, dashboard, raw report detail, Excel overview, and null-safe detail rendering. The maintainability API test now selects its own created scored record instead of relying on whichever record happens to be newest.

## 5. Root-level file audit

### Removed

- `final_audit_p050.py` — no active references were found; it posted hard-coded synthetic examples into the live database, so retaining it was unsafe and misleading.
- `Python_1_to_50_Tests.py` — the previous, superseded Python collection script; replaced by the full-module, ChatGPT/Human runner above.
- `test_live_comparison.py`, `test_p021_p030_live.py`, `test_p031_p040_live.py` — stale live-database scripts from earlier validation workflows; their expected sample/range behavior was obsolete.
- `validate_languages.py` — obsolete language validation helper with stale benchmark assumptions.

The last four files were removed in the earlier root-file cleanup; they are included here so the full cleanup history is clear.

### Retained

- `Cpp_1_to_50_Tests.py`, `Java_1_to_50_Tests.py`, `JavaScript_1_to_50_Tests.py` — separate language collection/generation workflows, not duplicates of the Python-specific runner.
- `run_validation.ps1` and `validate_runner.py` — paired generic validation entry point and runner.
- `run_validation_p021_p030.ps1` and `validate_runner_p021_p030.py` — paired range-specific workflow.
- `run_validation.py` — isolated validation runner with its own test database; distinct from raw research collection.
- `validate_p001_p010.py`, `validate_p011_p020.py`, `validate_runner_p031_p040.py`, `validate_runner_p041_p050.py` — distinct range/function checks; usage or scope is specialized enough to retain.
- `test_delete_feature.py` — unique deletion/data-management test using a temporary database.
- Existing application, backend tests, frontend tests, documentation, benchmark files, and source modules — required or preserved as requested.

Several validators have overlapping broad goals, but they use distinct ranges, fixtures, or workflows and the references do not establish a safe consolidation. They were retained. The new Python runner is the single active P001–P050 Python data collector.

## 6. Verification performed

- Full collection run: 50 problems, 100 variant executions, 1,000 case executions; database import verified 50 pairs.
- Backend suite: `pytest tests/ -q` — **15 passed**, 6 warnings (one dependency deprecation and small-sample Wilcoxon warnings).
- Frontend suite: `npm test` — **4 tests passed** across 4 files.
- Frontend typecheck: `npm run typecheck` — passed.
- Frontend production build: `npm run build` — passed. Vite reports that the generated JavaScript chunk is about 951 kB and exceeds its 500 kB advisory threshold.
- `test_delete_feature.py` — **61 passed** against its temporary test database.
- Live database inspection: 50 `execution_only` comparisons, 100 executions, 1,000 case results, 0 score rows, 0 comparison-result rows, and 0 statistical-result rows for these pairs.
- Live API: `/api/dashboard` returned 200 with 50 raw rows and 0 incomplete research records; `/api/comparisons` returned 200 with 50 rows; `/api/comparisons/50/detailed` returned 200 and actual P050 detail; `/api/export/research-report` returned a valid 22-sheet XLSX. The Research Overview sheet showed 50 raw datasets, 0 incomplete research records, and 0 scored research comparisons.
- Frontend component tests verify the raw detail rendering path and null-safe report display. The route, component, and API were checked; no browser automation or screenshot check was run.

## 7. Remaining issues / next steps

1. **Overall AI-vs-Human scores and winners remain unavailable by design.** Define and approve the research scoring methodology (including how reliability, performance, and other dimensions are weighted and how failures are handled) before creating comparative scores. The current raw execution records must not be counted as winners or comparable results.
2. The observed benchmark failures/errors are genuine recorded outcomes: ChatGPT had 123 failing and 2 error case results, while Human had 2 failing case results. Investigate those source solutions or benchmark expectations separately; original source files were deliberately left unchanged.
3. The production build’s large-chunk advisory remains. It did not fail the build and is unrelated to the report rendering fix.

No claim is made that AI/Human comparative scoring is fixed or complete: collection, status representation, database mapping, dashboard/raw report visibility, and export have been corrected and verified; a defensible score/winner still requires an explicit scoring methodology.
