# Metrics and Scoring

## 1. Evaluation Dimensions

The application evaluates six primary dimensions:

1. Reliability
2. Performance
3. Maintainability
4. Security
5. Complexity
6. Code Quality

The same methodology is applied to AI and human code across all supported languages (Python, Java, C++, JavaScript).

## 2. Reliability

Reliability measures how successfully the code handles the predefined test cases.

### Pass Rate

Pass Rate is calculated as:

Pass Rate = Passed Test Cases / Total Test Cases × 100

The system stores:

- Total test cases
- Passed test cases
- Failed test cases
- Error cases
- Timeout cases
- Pass rate

A higher pass rate represents better observed reliability.

## 3. Performance

Performance measures execution behaviour under the same environment.

The system records:

- Execution time (wall-clock time of the test-case execution phase only; compilation is excluded)
- Timeout status
- Execution errors

For equivalent workloads, lower execution time represents better observed performance.

**Note on compiled languages:** For Java and C++, only the runtime execution time is included in the performance metric. Compilation time is recorded separately but does not affect the performance score.

## 4. Maintainability

Maintainability is measured using structural code characteristics.

The maintainability evaluation uses:

- Cyclomatic complexity
- Function length
- Nesting depth
- Coupling

The maintainability composite is:

Maintainability =
0.30 × Cyclomatic Component
+
0.20 × Function Length Component
+
0.20 × Nesting Component
+
0.30 × Coupling Component

Metrics where lower values indicate better maintainability are inverted during normalization.

Raw measurements must always be preserved.

### Maintainability Measurement by Language

| Language | Cyclomatic Complexity | Function Length | Nesting Depth | Coupling |
|----------|----------------------|-----------------|---------------|---------|
| Python | radon (AST) | AST node analysis | AST walk | Import + attribute analysis |
| Java | Lightweight regex parser | Line counting | Brace counting | Import + attribute analysis |
| C++ | Lightweight regex parser | Line counting | Brace counting | Include + identifier analysis |
| JavaScript | Lightweight AST / regex | Line counting | Brace/block counting | require/import + call analysis |

## 5. Complexity

Complexity measures the structural difficulty of the source code.

The system may record:

- Cyclomatic complexity
- Nesting depth
- Function-level complexity
- Other approved complexity measurements

Raw complexity values must be stored separately from calculated scores.

## 6. Security

Security analysis identifies potential security weaknesses.

| Language | Security Tool | Notes |
|----------|--------------|-------|
| Python | Bandit | Available via pip; scans for common Python security weaknesses |
| Java | SpotBugs | Available as .bat/binary; XML output parsed by harness |
| C++ | cppcheck | Available as binary; scans for common C++ issues including buffer issues and unsafe functions |
| JavaScript | eslint with eslint-plugin-security | Available via npm; detects unsafe patterns in JS code |

Security findings should retain:

- Severity
- Rule
- Category
- Description
- Source location
- Tool name
- Tool version

Raw security findings must not be discarded.

Tool unavailability must never be treated as zero findings. When a tool is unavailable, a `TOOL_UNAVAILABLE` status is recorded.

## 7. Code Quality

Code quality is evaluated using static-analysis findings.

| Language | Code Quality Tool | Notes |
|----------|------------------|-------|
| Python | Ruff | Available via pip; fast linter covering style, errors, and best practices |
| Java | PMD | Available as .bat; covers code style and best practices |
| C++ | cppcheck | Same binary as security; code-quality rules (style, performance, portability) |
| JavaScript | eslint | Available via npm; covers style, best practices, and potential errors |

The system should retain:

- Finding count
- Severity
- Rule/category
- Message
- Tool
- Tool version

## 8. Normalization

Metrics with different units may be normalized before being combined.

For higher-is-better metrics:

Normalized = (x - min) / (max - min)

For lower-is-better metrics:

Normalized = (max - x) / (max - min)

Division by zero must be handled safely when all values are identical.

Raw values must always remain available.

Normalization uses the accumulated research dataset population. Population min, max, and n are persisted per score row for traceability.

## 9. Overall Score

An overall configured score may be calculated from the approved research dimensions and their configured weights.

Weights must be maintained in configuration rather than hard-coded into the frontend.

The system must preserve:

- Raw metric
- Normalized metric
- Weighted metric
- Dimension score
- Overall score

### Scoring Weights

| Dimension | Weight | Direction |
|-----------|--------|-----------|
| Reliability | 20% | higher is better |
| Performance | 15% | lower is better |
| Maintainability | 20% | higher is better |
| Security | 15% | lower is better |
| Complexity | 15% | lower is better |
| Code Quality | 15% | lower is better |

These weights apply identically to all four supported languages.

## 10. Comparison

For every metric, the system calculates the difference between AI and human results.

Example:

AI Reliability = 90%

Human Reliability = 80%

Difference = 10 percentage points

The system must not make universal claims from a single comparison.

## 11. Statistical Analysis

Statistical analysis is performed on the accumulated research dataset.

Where meaningful paired problem-level observations exist, the primary significance test is:

Wilcoxon Signed-Rank Test

The significance level is:

α = 0.05

The statistical analysis should report:

- Number of paired observations
- Test statistic
- P-value
- Significance status
- Effect size

Statistical analysis operates only on Research Data (is_pilot = 0). Language may be used as a grouping variable for sub-group analysis.

## 12. Research-Only Metrics

Additional measurements that are not part of the primary scoring model may be stored for research analysis.

Such measurements must not silently affect the primary overall score.

## 13. Reproducibility

Where applicable, automated measurements should retain:

- Tool name
- Tool version
- Language
- Problem
- Execution configuration
- Timestamp
- Raw result

## 14. Neutral Reporting

Reports should use objective language such as:

- AI code recorded a higher reliability value.
- Human code recorded lower execution time.
- AI code produced fewer security findings.
- Human code showed lower complexity.
- No statistically significant difference was detected.

The system must not present unsupported universal conclusions.
