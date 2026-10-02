# Validation Report — All 4 Languages (200 Solutions)

## Scope
200 / 200 solutions generated: 50 problems (P001–P050) × 4 languages
(Python, Java, C++, JavaScript).

## Method
No official/hidden test suite was included in the uploaded project files, so every
check below is a self-authored sanity test written directly from
`FINAL_AI_CODE_GENERATION_SPECIFICATION.md` — typically a normal case and an edge
case per problem. These were actually executed with each language's real
toolchain, not just asserted:

| Language   | How it was run                          | Checks run | Checks passed |
|------------|------------------------------------------|-----------:|---------------:|
| Python     | `python3 test_solutions.py`               | 71         | 71             |
| Java       | `javac Solution.java && java TestSolution`| 87         | 87             |
| C++        | `g++ -std=c++17 -Wall -Wextra` + run       | 87         | 87             |
| JavaScript | `node --check` + `node test_solutions.js` | 88         | 88             |

Function presence and exact signature names were also checked programmatically
against the spec for all 200 functions (50 per language) — 200/200 matched.

## Known limitation
These are hand-written sanity checks, not the project's official/hidden benchmark
test cases (none were provided). Before this set is used as ground truth in the
evaluation platform, it should also be run through the platform's real execution
harness and its actual benchmark test data, since some exact edge-case rules
(tie-breaking, rounding, whitespace handling in ambiguous spots) can only be
fully confirmed against the authoritative test data.

## Reference-link verification (real HTTP checks, not assumed)
All 200 reference URLs in the Excel source index were fetched directly:

| Language   | Accessible (HTTP 200) | Genuinely used (fetched + read + relevant) |
|------------|-----------------------:|--------------------------------------------:|
| Python     | 3 / 50                 | 3 / 50                                      |
| Java       | 47 / 50                | 5 / 50                                      |
| C++        | 47 / 50                | 5 / 50                                      |
| JavaScript | 47 / 50                | 5 / 50                                      |

Two different failure patterns showed up, and both are recorded honestly rather
than papered over:
- **Python column**: most links (47/50) are simply dead — 404 at check time.
- **Java/C++/JS columns**: most links (42/50 each) are alive but not
  topically relevant — the same one or two generic library files (e.g.
  `openjdk/String.java`, `libstdc++/basic_string.h`, `node/internal/errors.js`)
  are reused across dozens of unrelated problem rows in the source index.

Only 18 of 200 references were both reachable and topically specific to their
problem — e.g. `TheAlgorithms/Java/.../KadaneAlgorithm.java` for the max-subarray
problem, or `mysqljs/sqlstring/.../SqlString.js` for the SQL-escaping problem.
Those 18 were actually opened and read (not just filename-matched) before being
marked "Used." Full row-by-row detail, including the exact HTTP status and the
reasoning for every accessibility/relevance/used decision, is in
`References/reference_report.xlsx` (or the .csv).

No reference is marked "Used" unless it was actually fetched and its content
inspected — consistent with the project's Requirement 1, which explicitly
prohibits marking a reference used without checking it.
