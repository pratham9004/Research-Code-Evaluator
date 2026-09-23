# Experiment Workflow

## 1. Application Entry

The researcher opens the application and arrives at the Dashboard.

The Dashboard provides access to:

- Solve Problems
- Reports
- Research Progress

## 2. Select Problem

The researcher opens Solve Problems and selects one predefined research problem.

The selected problem provides:

- Problem description
- Supported language(s)
- Predefined test cases

## 3. Enter Code

The application displays two code sections side by side.

### AI-Written Code

The researcher enters:

- AI system name
- AI-generated source code

### Human-Written Code

The researcher enters:

- Human-written source code

No human name or participant ID is required.

## 4. Select Language

If the problem supports multiple languages, the researcher selects one language.

The selected language applies to both code variants.

AI and human code must use the same language for a comparison.

Supported languages are: Python, Java, C++, JavaScript.

## 5. Submit

The researcher clicks one common button:

**Submit & Compare**

The system validates:

- Problem selected
- Language selected
- AI name provided
- AI code provided
- Human code provided

## 6. Execute Both Codes

After submission, the system evaluates both code variants.

Both use:

- Same problem
- Same language
- Same predefined test cases
- Same execution environment
- Same execution limits

Each test case produces an execution result.

Possible results include:

- PASS
- FAIL
- ERROR
- TIMEOUT

### Language-Specific Execution

**Python:** The submitted function `solve(data: str) -> str` is imported by the harness and called once per test case. Interactive `input()` is not permitted.

**Java:** The submitted `public class Solution` containing `public static String solve(String data)` is compiled and called by the Runner harness. No `main()` method or `Scanner` is permitted in the submission.

**C++:** The submitted `solution.cpp` must define `std::string solve(const std::string& data)`. The harness compiles it together with a runner that calls `solve` for each test case. No `main()`, `cin`, `cout` for protocol I/O, or interactive I/O is permitted in the submission.

**JavaScript:** The submitted `solution.js` must define `function solve(data)` that returns a string. The harness requires the module and calls `solve` for each test case. No `readline`, `process.stdin`, or interactive I/O is permitted in the submission.

## 7. Measure Performance

The system records execution performance for both code variants.

At minimum:

- Execution time
- Execution status

Performance is measured as total subprocess wall-clock time across all test cases for that variant. For compiled languages (Java, C++), compilation time is excluded from the performance metric; only execution time is measured.

## 8. Static Analysis

The system analyses both source codes using the applicable analysis tools for the selected language.

The same analysis methodology is applied to both variants.

| Language | Security Tool | Code Quality Tool | Complexity Tool |
|----------|--------------|-------------------|-----------------|
| Python | Bandit | Ruff | radon (AST) |
| Java | SpotBugs | PMD | Lightweight parser |
| C++ | cppcheck | cppcheck | Lightweight regex parser |
| JavaScript | eslint (security plugins) | eslint | escomplex / lightweight parser |

If a tool is unavailable, a `TOOL_UNAVAILABLE` note is recorded. Tool unavailability is never treated as zero findings.

## 9. Calculate Metrics

The system calculates:

- Reliability
- Performance
- Maintainability
- Security
- Complexity
- Code Quality

The same six-dimension formula and weights are applied regardless of language.

## 10. Compare Results

The system compares the AI and human measurements.

Example:

| Metric | AI | Human |
|---|---:|---:|
| Test Cases Passed | 8/10 | 7/10 |
| Reliability | 80% | 70% |
| Execution Time | 12 ms | 15 ms |
| Maintainability | 82 | 76 |
| Security Findings | 0 | 1 |
| Complexity | 2.1 | 3.0 |

## 11. Generate Report

After evaluation, the system automatically generates a comparison report.

The report contains:

- Problem
- Language
- AI name
- Test results
- Performance
- Reliability
- Maintainability
- Security
- Complexity
- Code Quality
- AI-human differences
- Neutral observations

## 12. Store Results

After successful evaluation, the system automatically stores the complete comparison in the database.

The researcher does not manually enter calculated results.

## 13. Update Dashboard

After database storage, the dashboard automatically updates:

- Completed problems
- Remaining problems
- Completion percentage
- Total comparisons
- AI systems used
- AI versus human outcomes
- Metric summaries

## 14. Reports

The Reports section displays completed comparisons.

Each completed comparison can be opened to view its detailed report.

## 15. Research Completion

After all research problems have been evaluated, the system provides an overall research summary based on the collected comparisons.

The summary includes:

- Total problems evaluated
- AI systems used
- Languages used
- Reliability comparison
- Performance comparison
- Maintainability comparison
- Security comparison
- Complexity comparison
- Code Quality comparison
- Statistical results
