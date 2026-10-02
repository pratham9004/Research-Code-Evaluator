# Testing Infrastructure Cleanup Report

> **Update:** This file now records both cleanup steps. The original Step 1 inventory below is historical. The **Step 2 addendum at the end is authoritative for the current tree** and supersedes earlier KEEP/UNKNOWN actions.

**Step performed:** Step 1 only — inventory and cleanup of obsolete testing artifacts.  
**Date:** 2026-09-30  
**Database, source solutions, benchmark definitions, application code, and current research records were not modified.**

## Backup and starting state

Backups were created and verified before cleanup:

- Complete project snapshot: [complete_project_backup.zip](backup_snapshots/pre_testing_cleanup_20260930_192711/complete_project_backup.zip) — 14,419 archived file entries; ZIP integrity check passed. It includes the project tree, including `.git`, installed dependencies, and the database as it existed before cleanup.
- SQLite snapshot: [research.db](backup_snapshots/pre_testing_cleanup_20260930_192711/research.db) — `PRAGMA integrity_check` returned `ok`.
- Repository/worktree state: [git_and_worktree_state.txt](backup_snapshots/pre_testing_cleanup_20260930_192711/git_and_worktree_state.txt) — records HEAD, initial `git status --short`, diff summary, and tracked diff. The starting state was already substantially modified: it included numerous existing edits/untracked files and six already-deleted legacy scripts. This cleanup preserved those changes.

## Cleanup performed

- Removed 40 generated temporary/cache files: 37 files in project-owned Python `__pycache__` / `.pytest_cache` folders and 3 files in the abandoned `database/tmp/rce_ud_xev8t` executor directory (`runner.cpp`, `solution.cpp`, `testcases.json`). The executor creates temporary working directories at runtime; no code refers to that specific old directory. Runtime source and harness files were preserved.
- Removed no source scripts during this step: the six previously identified legacy scripts were already absent from the main working tree at the start and appeared as deletions in its initial Git status. Their absence and lack of active application/runner references were checked.
- Moved: **0**.
- Database rows changed: **0**. The active raw dataset remains available; no source solutions, benchmark cases, or research outputs were removed.

## Candidate inventory

The filesystem contained 14,423 files at the post-backup, pre-cleanup inventory point. The targeted project-owned filename/path scan found 52 candidates (including the registered nested worktree); a separate artifact scan found the current summary CSV, for 53 initial candidates/artifacts. It found five benchmark JSON outputs and one CSV; no standalone generated XLSX/PDF files. Dependency test files under `backend/.venv` and `frontend/node_modules` were treated as installed third-party packages, not project test suites. The separate `.kilo/worktrees/carnation-error` checkout is registered with Git and was left untouched because it is an independent worktree.

| File | Action | Reason | Dependency check |
|---|---|---|---|
| `final_audit_p050.py` (main tree) | REMOVED (already absent) | Prior cleanup removed a script that posted hard-coded synthetic P049/P045 comparisons. | No current app, script, or package invocation; verified no active references. The Git deletion existed before this step. |
| `Python_1_to_50_Tests.py` (main tree) | REMOVED (already absent) | Superseded Python collection script; the current raw Python dataset and its execution evidence are preserved. | No current invocation/reference; Git deletion existed before this step. |
| `test_live_comparison.py` (main tree) | REMOVED (already absent) | Obsolete live-database comparison helper. | No current invocation/reference; Git deletion existed before this step. |
| `test_p021_p030_live.py` (main tree) | REMOVED (already absent) | Obsolete live comparison helper for one range. | No current invocation/reference; Git deletion existed before this step. |
| `test_p031_p040_live.py` (main tree) | REMOVED (already absent) | Obsolete live comparison helper for one range. | No current invocation/reference; Git deletion existed before this step. |
| `validate_languages.py` (main tree) | REMOVED (already absent) | Obsolete language validation script with stale benchmark assumptions. | No current invocation/reference; Git deletion existed before this step. |
| `database/tmp/rce_ud_xev8t/runner.cpp` | REMOVED | Generated temporary executor source left in an old work directory. | No hard-coded reference to this directory; runtime harness remains in `backend/engine/`. |
| `database/tmp/rce_ud_xev8t/solution.cpp` | REMOVED | Generated temporary solution copy, not an authoritative solution source. | No hard-coded reference to this directory; original benchmark sources remain untouched. |
| `database/tmp/rce_ud_xev8t/testcases.json` | REMOVED | Generated temporary case payload, not the official benchmark definition. | No hard-coded reference to this directory; official test cases remain in config/database. |
| Project-owned Python `__pycache__` and `.pytest_cache` files (37 files) | REMOVED | Regenerable interpreter/test-run cache artifacts. | No application dependency; Python/pytest recreate them when needed. Excluded virtualenv, node_modules, and nested worktree caches. |
| `Python_ChatGPT_Human_P001_P050_Tests.py` | KEPT | Current raw collection runner; needed to reproduce the 50 preserved raw datasets. | Referenced by its report and benchmark-import/API test; its JSON is the active dataset. |
| `PYTHON_CHATGPT_HUMAN_TEST_REPORT.md` | KEPT | Documents the current actual collection and observed outcomes. | Evidence for the active dataset; not a duplicate temporary log. |
| `AI VS HUMAN CODE/benchmark_execution_results/python_chatgpt_human_p001_p050_execution_results.json` | KEPT | Current source result file for the 50 raw Python datasets. | Imported by backend startup/importer and exercised by the backend import test. |
| `python_chatgpt_human_p001_p050_summary.csv` | KEPT | Current human-readable collection summary. | Companion evidence generated by the active Python runner. |
| `AI VS HUMAN CODE/benchmark_execution_results/python_p001_p050_execution_results.json` | KEPT | Earlier Python execution dataset. | Historical evidence; not imported by default. No proof it is disposable, so preserved. |
| `AI VS HUMAN CODE/benchmark_execution_results/cpp_p001_p050_execution_results.json` | KEPT | C++ execution result artifact. | Historical/reproducibility evidence; preserved. |
| `AI VS HUMAN CODE/benchmark_execution_results/java_p001_p050_execution_results.json` | KEPT | Java execution result artifact. | Historical/reproducibility evidence; preserved. |
| `AI VS HUMAN CODE/benchmark_execution_results/javascript_p001_p050_execution_results.json` | KEPT | JavaScript execution result artifact. | Historical/reproducibility evidence; preserved. |
| `Cpp_1_to_50_Tests.py` | KEPT | Language-specific C++ collector. | Distinct language workflow; no evidence it is an accidental duplicate of the Python collector. |
| `Java_1_to_50_Tests.py` | KEPT | Language-specific Java collector. | Distinct language workflow; no evidence it is an accidental duplicate of the Python collector. |
| `JavaScript_1_to_50_Tests.py` | KEPT | Language-specific JavaScript collector. | Distinct language workflow; no evidence it is an accidental duplicate of the Python collector. |
| `backend/db/benchmark_import.py` | KEPT | Application database import path for benchmark execution results. | Imported by backend startup and backend tests; essential database integration code. |
| `database/research_BACKUP_before_benchmark_removal_20260920_155725.db` | KEPT | Historical database backup. | Preserved as a recovery/research record; not used by the active app. |
| `database/research_backup_before_raw_execution_cleanup_20260930.db` | KEPT | Earlier pre-cleanup database snapshot. | Preserved as a recovery/research record; not used by the active app. |
| `database/research_backup_pre_audit_20260927.db` | KEPT | Historical pre-audit database backup. | Preserved as a recovery/research record; not used by the active app. |
| `database/validation_test.db` | KEPT | Isolated state database used by `run_validation.py`. | The validation script explicitly selects this database; kept to preserve its existing isolated workflow. |
| `database/research.db` | KEPT | Active application/research database. | Backed up before cleanup and queried read-only afterward; contains the preserved raw execution records. |
| `tests/test_api.py` | KEPT | Backend API, execution, database, report, and export tests. | Discovered by pytest; verifies application endpoints and import behavior. |
| `frontend/src/tests/Dashboard.test.tsx` | KEPT | Dashboard rendering regression test. | Discovered by Vitest; verifies raw execution dashboard display. |
| `frontend/src/tests/DetailedReport.test.tsx` | KEPT | Detailed report rendering regression test. | Discovered by Vitest; verifies nullable/raw score handling. |
| `frontend/src/tests/Reports.test.tsx` | KEPT | Reports list regression test. | Discovered by Vitest; verifies raw dataset labeling. |
| `frontend/src/tests/SolveProblems.test.tsx` | KEPT | Frontend solve flow regression test. | Existing Vitest test; verifies application behavior. |
| `test_delete_feature.py` | KEPT | Database/data-management feature test. | Uses an isolated temporary SQLite database; verifies app deletion behavior while preserving benchmark records. |
| `run_validation.py` | KEPT | Controlled backend integration/functional validation suite. | Explicitly sets `RESEARCH_DB_PATH` to `database/validation_test.db`; not a research collector. |
| `run_validation.ps1` | KEPT | PowerShell harness for a broad set of direct runner fixtures over P001–P020. | Calls `validate_runner.py`; distinct from database import/collection and kept as a manual validation workflow. |
| `run_validation_p021_p030.ps1` | KEPT | PowerShell harness for direct runner fixtures over P021–P030. | Calls `validate_runner_p021_p030.py`; no database population path found. |
| `validate_p001_p010.py` | UNKNOWN (kept) | Standalone correct/wrong/error execution checks for P001–P010 across languages. | Reads official cases from `database/research.db` and calls the executor, but does not write research rows; no active caller found. Retained because standalone validation use is plausible. |
| `validate_p011_p020.py` | UNKNOWN (kept) | Standalone correct/wrong/error execution checks for P011–P020 across languages. | Reads official cases from `database/research.db` and calls the executor, but does not write research rows; no active caller found. Retained because standalone validation use is plausible. |
| `validate_runner.py` | KEPT | Reusable fixture runner for the first range, invoked by the broad PowerShell validation harness. | Called by `run_validation.ps1`; direct executor use, not DB population. |
| `validate_runner_p021_p030.py` | KEPT | Reusable fixture runner for P021–P030. | Called by `run_validation_p021_p030.ps1`; direct executor use, not DB population. |
| `validate_runner_p031_p040.py` | UNKNOWN (kept) | Reusable fixture runner for P031–P040. | No current wrapper/reference found. It calls the executor and has distinct range fixtures; retained pending proof it is obsolete. |
| `validate_runner_p041_p050.py` | UNKNOWN (kept) | Reusable fixture runner for P041–P050. | No current wrapper/reference found. It calls the executor and has distinct range fixtures; retained pending proof it is obsolete. |
| `AUDIT_REPORT.txt` (main tree) | KEPT | Existing project audit record. | Documentation/evidence; no code dependency required, but not proven disposable. |
| `TESTING_INFRASTRUCTURE_CLEANUP_REPORT.md` | KEPT | This requested cleanup inventory and outcome. | Requested project documentation. |
| `docs/FINAL_SPECIFICATION_VALIDATION_REPORT.md` | KEPT | Specification validation documentation. | Preserved as requested documentation; no code dependency required. |
| `docs/FULL_PROJECT_AUDIT_2026-09-27.md` | KEPT | Historical full-project audit. | Preserved as an existing report; no code dependency required. |
| `docs/RESEARCH_CODE_EVALUATOR_FINAL_50_PROBLEM_BENCHMARK_v1.0.md` | KEPT | Benchmark specification. | Official/research documentation; explicitly preserved. |
| `docs/RESEARCH_CODE_EVALUATOR_FINAL_50_PROBLEM_BENCHMARK_v1.1.md` | KEPT | Updated benchmark specification. | Official/research documentation; explicitly preserved. |
| `.kilo/worktrees/carnation-error/final_audit_p050.py` | UNKNOWN (kept) | Duplicate exists inside a separate registered Git worktree, not the main working tree. | Git reports this as an independent detached worktree at the same HEAD; it is not the application’s active runner. Left untouched to avoid changing another worktree. |
| `.kilo/worktrees/carnation-error/test_live_comparison.py` | UNKNOWN (kept) | Duplicate old live test exists only inside the separate registered worktree. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/test_p021_p030_live.py` | UNKNOWN (kept) | Duplicate old live test exists only inside the separate registered worktree. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/test_p031_p040_live.py` | UNKNOWN (kept) | Duplicate old live test exists only inside the separate registered worktree. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/validate_languages.py` | UNKNOWN (kept) | Duplicate old validator exists only inside the separate registered worktree. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/test_delete_feature.py` | UNKNOWN (kept) | Separate worktree copy of the feature test. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/tests/test_api.py` | UNKNOWN (kept) | Separate worktree copy of backend tests. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/frontend/src/tests/SolveProblems.test.tsx` | UNKNOWN (kept) | Separate worktree copy of a frontend test. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/run_validation.py` | UNKNOWN (kept) | Separate worktree copy of controlled validation. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/run_validation.ps1` | UNKNOWN (kept) | Separate worktree copy of broad fixture harness. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/run_validation_p021_p030.ps1` | UNKNOWN (kept) | Separate worktree copy of range fixture harness. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/validate_p001_p010.py` | UNKNOWN (kept) | Separate worktree copy of range validation. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/validate_p011_p020.py` | UNKNOWN (kept) | Separate worktree copy of range validation. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/validate_runner.py` | UNKNOWN (kept) | Separate worktree copy of fixture runner. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/validate_runner_p021_p030.py` | UNKNOWN (kept) | Separate worktree copy of range runner. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/validate_runner_p031_p040.py` | UNKNOWN (kept) | Separate worktree copy of range runner. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/validate_runner_p041_p050.py` | UNKNOWN (kept) | Separate worktree copy of range runner. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/AUDIT_REPORT.txt` | UNKNOWN (kept) | Separate worktree audit record. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/docs/RESEARCH_CODE_EVALUATOR_FINAL_50_PROBLEM_BENCHMARK_v1.0.md` | UNKNOWN (kept) | Separate worktree copy of benchmark specification. | Independent Git worktree; left untouched. |
| `.kilo/worktrees/carnation-error/docs/RESEARCH_CODE_EVALUATOR_FINAL_50_PROBLEM_BENCHMARK_v1.1.md` | UNKNOWN (kept) | Separate worktree copy of benchmark specification. | Independent Git worktree; left untouched. |

The six main-tree legacy scripts are documented as already absent rather than counted among the found candidates. The registered nested worktree contains copies of those old live scripts; its contents remain unchanged. A second Git worktree pointer under `AI VS HUMAN CODE/Gemini/.kilo` is marked prunable by Git, but no accessible project files were found there; it was not altered.

## Remaining project-owned search matches

The post-cleanup filename/path search found 56 matches when including all file types (including this report and database backup filenames). The separate results-artifact scan also found the current summary CSV. The list below excludes `.git`, installed dependencies (`backend/.venv`, `frontend/node_modules`), the backup archive, build outputs, and Python/pytest caches:

```text
.kilo/worktrees/carnation-error/AUDIT_REPORT.txt
.kilo/worktrees/carnation-error/docs/RESEARCH_CODE_EVALUATOR_FINAL_50_PROBLEM_BENCHMARK_v1.0.md
.kilo/worktrees/carnation-error/docs/RESEARCH_CODE_EVALUATOR_FINAL_50_PROBLEM_BENCHMARK_v1.1.md
.kilo/worktrees/carnation-error/final_audit_p050.py
.kilo/worktrees/carnation-error/frontend/src/tests/SolveProblems.test.tsx
.kilo/worktrees/carnation-error/run_validation.ps1
.kilo/worktrees/carnation-error/run_validation.py
.kilo/worktrees/carnation-error/run_validation_p021_p030.ps1
.kilo/worktrees/carnation-error/test_delete_feature.py
.kilo/worktrees/carnation-error/test_live_comparison.py
.kilo/worktrees/carnation-error/test_p021_p030_live.py
.kilo/worktrees/carnation-error/test_p031_p040_live.py
.kilo/worktrees/carnation-error/tests/test_api.py
.kilo/worktrees/carnation-error/validate_languages.py
.kilo/worktrees/carnation-error/validate_p001_p010.py
.kilo/worktrees/carnation-error/validate_p011_p020.py
.kilo/worktrees/carnation-error/validate_runner.py
.kilo/worktrees/carnation-error/validate_runner_p021_p030.py
.kilo/worktrees/carnation-error/validate_runner_p031_p040.py
.kilo/worktrees/carnation-error/validate_runner_p041_p050.py
AI VS HUMAN CODE/benchmark_execution_results/cpp_p001_p050_execution_results.json
AI VS HUMAN CODE/benchmark_execution_results/java_p001_p050_execution_results.json
AI VS HUMAN CODE/benchmark_execution_results/javascript_p001_p050_execution_results.json
AI VS HUMAN CODE/benchmark_execution_results/python_chatgpt_human_p001_p050_execution_results.json
AI VS HUMAN CODE/benchmark_execution_results/python_p001_p050_execution_results.json
AUDIT_REPORT.txt
Cpp_1_to_50_Tests.py
Java_1_to_50_Tests.py
JavaScript_1_to_50_Tests.py
PYTHON_CHATGPT_HUMAN_TEST_REPORT.md
Python_ChatGPT_Human_P001_P050_Tests.py
TESTING_INFRASTRUCTURE_CLEANUP_REPORT.md
python_chatgpt_human_p001_p050_summary.csv
backend/db/benchmark_import.py
database/research_BACKUP_before_benchmark_removal_20260920_155725.db
database/research_backup_before_raw_execution_cleanup_20260930.db
database/research_backup_pre_audit_20260927.db
database/validation_test.db
docs/FINAL_SPECIFICATION_VALIDATION_REPORT.md
docs/FULL_PROJECT_AUDIT_2026-09-27.md
docs/RESEARCH_CODE_EVALUATOR_FINAL_50_PROBLEM_BENCHMARK_v1.0.md
docs/RESEARCH_CODE_EVALUATOR_FINAL_50_PROBLEM_BENCHMARK_v1.1.md
frontend/src/tests/Dashboard.test.tsx
frontend/src/tests/DetailedReport.test.tsx
frontend/src/tests/Reports.test.tsx
frontend/src/tests/SolveProblems.test.tsx
run_validation.ps1
run_validation.py
run_validation_p021_p030.ps1
test_delete_feature.py
tests/test_api.py
validate_p001_p010.py
validate_p011_p020.py
validate_runner.py
validate_runner_p021_p030.py
validate_runner_p031_p040.py
validate_runner_p041_p050.py
```

`database/tmp/rce_ud_xev8t` and project-owned Python/pytest caches no longer appear. Third-party package tests remain inside installed dependency directories. The matching scripts within the nested Git worktree are the main unresolved cleanup items: they are outside the active working tree and were kept to avoid dirtying a registered independent checkout. No application tests were deleted. No tests were run for this cleanup-only step.

## Final confirmations

1. Project files scanned: **14,423 physical files** at initial inventory. The focused inventory found 52 filename/path candidates plus the current summary CSV; the final broader search found 56 remaining filename/path matches plus that CSV. The temporary testcase payload was removed.
2. Files removed in this step: **40 generated temporary/cache files**. Six legacy scripts were already deleted from the main tree before this step; no additional source scripts were deleted.
3. Files retained: all valid application tests, current collectors and evidence, official specs, source code, app/backend code, and uncertain validation scripts. **No files moved.**
4. Database backup: `backup_snapshots/pre_testing_cleanup_20260930_192711/research.db` (integrity `ok`).
5. Project backup: `backup_snapshots/pre_testing_cleanup_20260930_192711/complete_project_backup.zip` (integrity passed).
6. ChatGPT and Human source modules were untouched.
7. Official benchmark cases were untouched.
8. The current 50 raw Python pairs, 100 executions, and 1,000 case results were preserved; no database writes or result deletions occurred.
9. No Step 2 system, new runner, dashboard/report changes, score calculations, or winner calculations were started.

---

## Step 2 addendum — remove old research execution infrastructure

**Date:** 2026-09-30. This step removed old tools and generated summaries only. It did not run the old execution system or change application/source/data files.

### Removed and archived

| File(s) | Action | Reason and reference check |
|---|---|---|
| `Cpp_1_to_50_Tests.py`, `Java_1_to_50_Tests.py`, `JavaScript_1_to_50_Tests.py`, `Python_ChatGPT_Human_P001_P050_Tests.py` | REMOVED | Standalone legacy collectors. No application import or package script invokes them. Backend startup/import tests consume the preserved Python JSON directly, not these generator scripts. |
| `validate_p001_p010.py`, `validate_p011_p020.py`, `validate_runner.py`, `validate_runner_p021_p030.py`, `validate_runner_p031_p040.py`, `validate_runner_p041_p050.py` | REMOVED | Legacy direct execution/fixture validators. No active application references; their only identified launcher references were in the old PowerShell validation scripts removed below. |
| `run_validation.py`, `run_validation.ps1`, `run_validation_p021_p030.ps1` | REMOVED | Superseded manual validation launchers. The PowerShell scripts called the removed fixture runners. `run_validation.py` was a standalone controlled API check, not imported by the application. |
| `python_chatgpt_human_p001_p050_summary.csv`, `PYTHON_CHATGPT_HUMAN_TEST_REPORT.md`, `AUDIT_REPORT.txt` | REMOVED | Generated collection summary/report and generated root audit output. No application dependency or package-script reference was found. The raw JSON research evidence remains. |
| `FULL_PROJECT_ROOT_CAUSE_AND_FIX_REPORT.md` | MOVED | Historical cleanup/debugging report moved to `archive/old-audits/FULL_PROJECT_ROOT_CAUSE_AND_FIX_REPORT.md`, as allowed by the request. |

**Step 2 totals:** 16 files removed from the active project tree; 1 file moved to the historical audit archive. Six other named legacy scripts (`final_audit_p050.py`, `Python_1_to_50_Tests.py`, three old live tests, and `validate_languages.py`) had already been deleted from the active tree before Step 1. No Step 2 application test or research-data file was deleted.

### Retained files and evidence

- `test_delete_feature.py` was retained. It is a standalone application data-management feature test, not a research collector. It has no caller in the formal backend/frontend suites, and `tests/test_api.py` does not cover deletion; it uniquely checks delete behavior and preservation of problems/test cases. Its isolated temporary database keeps it separate from research records.
- `tests/test_api.py` and all four files in `frontend/src/tests/` remain. They are the formal application API and UI tests.
- `TESTING_INFRASTRUCTURE_CLEANUP_REPORT.md` remains at the root because this task explicitly requires updating this report there.
- `AI VS HUMAN CODE/benchmark_execution_results/` retains all five JSON artifacts: `cpp_p001_p050_execution_results.json`, `java_p001_p050_execution_results.json`, `javascript_p001_p050_execution_results.json`, `python_p001_p050_execution_results.json`, and `python_chatgpt_human_p001_p050_execution_results.json`. The current Python AI/Human JSON is used by the backend importer/test. The other JSON files are historical benchmark evidence whose validity was not disproved; no result data was deleted.
- Official specification, methodology, metrics/scoring documents, benchmark cases, AI/Human source modules, active database, database schema/migrations, and application code remain unchanged.
- Other matching paths such as `backend/export/report.py`, `backend/export/pdf_report.py`, and the frontend report pages are active application code, not old generated reports.

### Search results and remaining files

The post-cleanup filename/path search (keywords: `test`, `Tests`, `validat`, `runner`, `execution`, `collection`, `summary`, `report`, `audit`) found **46 files**, excluding installed dependencies, Python/pytest caches, `.git`, and the Step 1 backup snapshot.

#### A. Active application tests

```text
test_delete_feature.py
tests/test_api.py
frontend/src/tests/Dashboard.test.tsx
frontend/src/tests/DetailedReport.test.tsx
frontend/src/tests/Reports.test.tsx
frontend/src/tests/SolveProblems.test.tsx
```

#### B. Research and cleanup documentation

```text
docs/FINAL_SPECIFICATION_VALIDATION_REPORT.md
docs/FULL_PROJECT_AUDIT_2026-09-27.md
TESTING_INFRASTRUCTURE_CLEANUP_REPORT.md
archive/old-audits/FULL_PROJECT_ROOT_CAUSE_AND_FIX_REPORT.md
```

#### C. Preserved execution evidence and validation databases

```text
AI VS HUMAN CODE/benchmark_execution_results/cpp_p001_p050_execution_results.json
AI VS HUMAN CODE/benchmark_execution_results/java_p001_p050_execution_results.json
AI VS HUMAN CODE/benchmark_execution_results/javascript_p001_p050_execution_results.json
AI VS HUMAN CODE/benchmark_execution_results/python_chatgpt_human_p001_p050_execution_results.json
AI VS HUMAN CODE/benchmark_execution_results/python_p001_p050_execution_results.json
database/research_backup_before_raw_execution_cleanup_20260930.db
database/research_backup_pre_audit_20260927.db
database/validation_test.db
```

`database/validation_test.db` is an isolated validation database, not the current research database. It was left untouched. The active `database/research.db` is also unchanged; it does not match the requested filename keywords.

#### D. Obsolete files removed from the active tree

```text
Cpp_1_to_50_Tests.py
Java_1_to_50_Tests.py
JavaScript_1_to_50_Tests.py
Python_ChatGPT_Human_P001_P050_Tests.py
validate_p001_p010.py
validate_p011_p020.py
validate_runner.py
validate_runner_p021_p030.py
validate_runner_p031_p040.py
validate_runner_p041_p050.py
run_validation.py
run_validation.ps1
run_validation_p021_p030.ps1
python_chatgpt_human_p001_p050_summary.csv
PYTHON_CHATGPT_HUMAN_TEST_REPORT.md
AUDIT_REPORT.txt
```

#### E. Active application code and supporting records

These matched the requested words but are application code, historical database files, or archival records, so they remain:

```text
backend/export/pdf_report.py
backend/export/report.py
frontend/src/pages/DetailedReport.tsx
frontend/src/pages/ReportDetail.tsx
frontend/src/pages/Reports.tsx
```

#### F. Remaining matches inside the separate registered Git worktree

These files are physically nested in the repository but belong to `.kilo/worktrees/carnation-error`, an independent detached Git worktree. The obsolete copies remain because the automatic approval review blocked modifying that checkout:

```text
.kilo/worktrees/carnation-error/AUDIT_REPORT.txt
.kilo/worktrees/carnation-error/backend/export/pdf_report.py
.kilo/worktrees/carnation-error/backend/export/report.py
.kilo/worktrees/carnation-error/final_audit_p050.py
.kilo/worktrees/carnation-error/frontend/src/pages/DetailedReport.tsx
.kilo/worktrees/carnation-error/frontend/src/pages/ReportDetail.tsx
.kilo/worktrees/carnation-error/frontend/src/pages/Reports.tsx
.kilo/worktrees/carnation-error/frontend/src/tests/SolveProblems.test.tsx
.kilo/worktrees/carnation-error/run_validation.ps1
.kilo/worktrees/carnation-error/run_validation.py
.kilo/worktrees/carnation-error/run_validation_p021_p030.ps1
.kilo/worktrees/carnation-error/test_delete_feature.py
.kilo/worktrees/carnation-error/test_live_comparison.py
.kilo/worktrees/carnation-error/test_p021_p030_live.py
.kilo/worktrees/carnation-error/test_p031_p040_live.py
.kilo/worktrees/carnation-error/tests/test_api.py
.kilo/worktrees/carnation-error/validate_languages.py
.kilo/worktrees/carnation-error/validate_p001_p010.py
.kilo/worktrees/carnation-error/validate_p011_p020.py
.kilo/worktrees/carnation-error/validate_runner.py
.kilo/worktrees/carnation-error/validate_runner_p021_p030.py
.kilo/worktrees/carnation-error/validate_runner_p031_p040.py
.kilo/worktrees/carnation-error/validate_runner_p041_p050.py
```

### Separate registered Git worktree limitation

The physical repository also contains `.kilo/worktrees/carnation-error`, which Git reports as a separate registered detached worktree. It still contains copies of obsolete scripts, including `final_audit_p050.py`, the old live-comparison scripts, `validate_languages.py`, the range validators, and the `run_validation*` launchers, plus a nested `AUDIT_REPORT.txt`. It also contains separate app/test files and benchmark sources.

An automatic approval review rejected a command that combined deletion from this separate worktree with the active-tree cleanup, stating that modifying another checkout could affect independent worktree content. That command did not complete. I proceeded with the requested active-tree cleanup and did not retry deletion from the nested worktree. These remaining copies are therefore **not claimed as removed**; approval is needed before modifying that registered checkout.

### Step 2 verification

- Read-only SQLite check after cleanup: **50** Python ChatGPT/Human comparison containers still have `execution_only` status; **100** execution rows and **1,000** test-case results remain; **0** Score rows and **0** ComparisonResult rows for those pairs.
- No database writes or row deletions occurred.
- No AI/Human source solutions or official benchmark cases were edited.
- No tests or old execution scripts were run, per the Step 2 stop instruction.
- No new execution system, runner, test file, dashboard, scoring, or comparison logic was created or changed.
