# Project audit and database cleanup — 2026-09-27

## Findings

The project is a FastAPI/SQLAlchemy/SQLite backend with a React/TypeScript/Vite frontend. Benchmark results are read from `AI VS HUMAN CODE/benchmark_execution_results/*_execution_results.json`, imported into `comparisons`, `execution_results`, `test_case_results`, `scores`, and `comparison_results`, then consumed by the dashboard, comparison report endpoints, and Excel/PDF exporters.

The four execution JSON files contain 1,000 AI/model/problem/language result entries (five model identities × 50 problems × four languages). They do not contain source code for those results. Their `human_reference` entries are marked `MISSING` and contain no human execution cases or source code. The importer nevertheless created completed comparisons, synthetic source-code placeholders, zero-valued Human execution metrics, and zero-valued scores for unmeasured dimensions. It also treated absent `pass_rate` as zero instead of deriving it from the recorded test cases. The importer stored each zero-based case index as a database test-case ID, which mislinked case results.

The detailed-report code turned absent complexity data into perfect maintainability components, used zero as the difference when overall scores were absent, and assumed a comparison direction was always present. The frontend called `.toLowerCase()` on that direction; once missing scores are represented accurately, that assumption would crash report rendering. Report load errors were also discarded. Excel overview counts treated every research-labeled row as a valid research comparison and generated maintainability components from missing values.

## Backup and cleanup

Before changing the database, a byte-for-byte copy was created at `database/research_backup_pre_audit_20260927.db`. Its SHA-256 at backup time was `b8507dc2d733cb9c11c275d093b9d733923885b4a8f8fb1d5e5d4649cf77bb40`.

The live database passed SQLite `integrity_check` before and after cleanup. No comparison records, problems, test cases, or source datasets were deleted. The 1,000 benchmark comparison rows were retained and reclassified as `incomplete`. Their recorded AI executions and case results remain stored. Missing measurements are now SQL `NULL`; fabricated source-code placeholders and derived scores were removed.

| Table | Before | After | Cleanup |
| --- | ---: | ---: | --- |
| problems | 50 | 50 | preserved |
| test_cases | 500 | 500 | preserved |
| comparisons | 1,000 | 1,000 | retained; all are incomplete pending Human executions |
| execution_results | 2,000 | 2,000 | retained; missing pass rates/timings are NULL |
| test_case_results | 6,830 | 6,830 | retained; case IDs now map to the right problem test cases |
| comparison_results | 7,000 | 2,000 | removed 5,000 synthetic/missing-dimension and overall result rows |
| scores | 14,000 | 4,000 | removed 10,000 fabricated zero-score rows; retained observed raw reliability/performance values |

AI execution statuses recorded in the import are PASS 478, FAIL 138, ERROR 67, and MISSING 317. Human result entries include 790 MISSING, 205 ERROR, and five PASS status labels, but none has cases or source code; all remain incomplete. There are no complete paired comparisons, so the current valid comparison count is **0**. The dashboard correctly reports 0 wins, 0 human wins, and 0 comparable outcomes; the 1,000 incomplete records are shown separately.

There are no orphaned test-case result references or SQLite foreign-key violations after the correction.

## Code changes

- `backend/db/benchmark_import.py`: keeps absent measurements absent, derives AI pass rate from stored cases when needed, maps case ordinals to the problem’s actual test-case IDs, marks comparisons incomplete unless both variants have source and complete execution evidence, and stops inventing placeholder source or score values.
- `backend/db/models.py` and `database/migrate.py`: allow nullable pass rates and timings and migrate existing databases without dropping execution records.
- `backend/api/dashboard.py`: counts only completed research pairs with non-null overall scores; reports incomplete rows separately and does not count missing directions as comparable.
- `backend/api/comparisons.py`: preserves missing scores/directions in detailed reports and avoids defaulting unavailable maintainability, difference, or interpretation values to zero/perfect scores.
- `backend/export/report.py` and `backend/export/pdf_report.py`: show only scored pairs in research overview aggregates and keep unavailable metrics blank/N/A.
- `frontend/src/pages/Dashboard.tsx`, `DetailedReport.tsx`, `ReportDetail.tsx`, and `frontend/src/types.ts`: communicate incomplete data and display unavailable measurements without crashing; report fetch errors are visible.
- `frontend/src/components/ChartPanel.tsx` and `frontend/src/vite-env.d.ts`: fix existing Chart.js option typing and PNG module typing errors uncovered while running TypeScript checks.

## File removal review

Removed `Microsoft/Windows/PowerShell/ModuleAnalysisCache`, an untracked PowerShell runtime cache unrelated to the application. Repository search found no project references to it. Temporary audit scripts created during this review were also removed. No benchmark, AI/Human source, validation, test, configuration, report, or documentation files were deleted. The remaining validation scripts cover different problem ranges or purposes; no additional duplicates were confirmed safe to remove.

## Verification and remaining work

- `python -m pytest tests/ -q`: 15 passed after the import/dashboard/report assertions were added. (The suite emits upstream deprecation and small-sample SciPy warnings.)
- `npm test`: 1 passed.
- `npm run typecheck`: passed.
- `npm run build`: passed; Vite reports the existing large JavaScript chunk warning.
- Excel export tests load the workbook and verify that the overview excludes incomplete records from valid-pair totals.
- Detailed-report tests verify that unavailable Human metrics and overall scores remain null and that imported test-case IDs point to P001’s actual cases.

The source data does not currently provide paired Human execution results for these imports. The system does not regenerate or infer them. To obtain nonzero valid comparison counts, import the missing Human source/execution artifacts through the corrected mapping after their provenance and complete test-case outputs are available.
