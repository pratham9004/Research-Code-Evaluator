# Research Problem Taxonomy

## Purpose

This document defines the research problem taxonomy for the Research Code Evaluator.

The taxonomy serves two purposes:

1. **Experiment design** — helps the researcher select problems that cover the intended research dimensions.
2. **Reporting context** — provides metadata tags that appear in reports and exports so that results can be interpreted correctly.

**Important:** The taxonomy tags are contextual metadata only. They do NOT act as hidden scoring multipliers. The approved scoring methodology (reliability 20%, performance 15%, maintainability 20%, security 15%, complexity 15%, code quality 15%) is applied identically to every problem regardless of its taxonomy tags.

---

## Supported Languages

The research instrument supports four programming languages:

| Language | Runtime | Entry Contract |
|----------|---------|----------------|
| Python | Python 3.x | `def solve(data: str) -> str:` |
| Java | Java 17+ | `public static String solve(String data)` inside `public class Solution` |
| C++ | g++ (C++17+) | `std::string solve(const std::string& data)` inside `solution.cpp` |
| JavaScript | Node.js 18+ | `function solve(data)` returning a string, exported or declared in `solution.js` |

---

## Research Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Reliability | 20% | Percentage of predefined test cases passed |
| Performance | 15% | Subprocess runtime execution time (lower is better; compilation excluded) |
| Maintainability | 20% | Composite of cyclomatic complexity, function length, nesting, coupling |
| Security | 15% | Static security findings (tool-specific per language) |
| Complexity | 15% | Average cyclomatic complexity |
| Code Quality | 15% | Static code-quality findings (tool-specific per language) |

---

## Static Analysis Tools by Language

| Language | Security Tool | Code Quality Tool | Availability |
|----------|--------------|-------------------|-------------|
| Python | Bandit | Ruff | pip-installable |
| Java | SpotBugs | PMD | Binary (.bat on Windows) |
| C++ | cppcheck | cppcheck | System binary |
| JavaScript | eslint + eslint-plugin-security | eslint | npm-installable |

When a tool is not available, a `TOOL_UNAVAILABLE` note is recorded. Tool unavailability is never equated with zero findings.

---

## Taxonomy Fields

Each problem in the benchmark carries:

| Field | Type | Values | Purpose |
|-------|------|--------|---------|
| `problem_id` | string | B001–B050 | Unique identifier for benchmark v1.1 |
| `supported_languages` | list | python, java, cpp, javascript | Languages the problem supports |
| `research_focus` | string | comma-separated dimension names | Primary dimensions this problem is designed to reveal |
| `security_relevance` | string | `low` / `medium` / `high` | Whether security analysis is expected to yield meaningful findings |

Each test case carries:

| Field | Type | Values | Purpose |
|-------|------|--------|---------|
| `case_type` | string | `normal` / `boundary` / `edge` / `adversarial` / `stress` | Deliberate test case design classification |

---

## Current Problem Bank (6 original problems — P001–P006)

These are the original 6 problems in the existing database. They are **not replaced** by the new benchmark.

| ID | Title | Languages | Research Focus | Security Relevance |
|----|-------|-----------|----------------|--------------------|
| P001 | Two Sum | Python, Java | reliability, complexity, performance | low |
| P002 | Factorial | Python, Java | reliability, performance, code_quality | low |
| P003 | Palindrome Check | Python, Java | reliability, maintainability, code_quality | low |
| P004 | Fibonacci | Python, Java | reliability, performance, complexity | low |
| P005 | Reverse String | Python | reliability, maintainability, code_quality | low |
| P006 | Prime Check | Java | reliability, complexity, performance | low |

---

## New Benchmark — B001–B050 (50 problems, 4 languages)

The benchmark document `RESEARCH_CODE_EVALUATOR_FINAL_50_PROBLEM_BENCHMARK_v1.1.md` defines 50 problems across 10 categories. All 50 support Python, Java, C++, and JavaScript.

| Category | Problems | Main Research Purpose | Security Relevance Range |
|----------|----------|-----------------------|--------------------------|
| A (B001–B005) | 5 | Classic algorithmic correctness | low |
| B (B006–B010) | 5 | Data processing and parsing | low–medium |
| C (B011–B015) | 5 | Input validation | medium |
| D (B016–B020) | 5 | String sanitization / output safety | medium–high |
| E (B021–B025) | 5 | Path / file safety | medium–high |
| F (B026–B030) | 5 | SQL / query safety | medium–high |
| G (B031–B035) | 5 | Command / shell safety | medium–high |
| H (B036–B040) | 5 | Safe parsing / configuration | medium–high |
| I (B041–B045) | 5 | Resource / performance safety | low–medium |
| J (B046–B050) | 5 | Authentication / token / authorization | medium–high |

### Security Coverage

The benchmark provides meaningful security coverage through categories C–J. All problems in these categories involve patterns detectable by Bandit (Python), SpotBugs (Java), cppcheck (C++), and eslint-plugin-security (JavaScript).

---

## Language Compatibility for B001–B050

All 50 benchmark problems are pure string-in/string-out functions using standard library only. They are compatible with all four languages:

- **Python**: Uses string methods, standard parsing, regex where needed.
- **Java**: Uses `String`, `StringBuilder`, standard collections from `java.util`.
- **C++**: Uses `std::string`, `std::vector`, `std::map`, `<regex>`, standard headers.
- **JavaScript**: Uses string methods, `Array`, `Map`, `RegExp`, built-in `JSON`.

No problem requires:

- File I/O
- Network access
- Database connections
- External services
- Operating system commands
- Real credentials

All 50 are therefore fully implementable in all four languages under the existing execution contract.

---

## Execution Contract per Language

### Python

```python
def solve(data: str) -> str:
    # Implement only the required solution logic.
    # Return the required result as a string.
    pass
```

Restrictions: No `input()`, no `exec()`, no `eval()`, no interactive I/O.

### Java

```java
public class Solution {
    public static String solve(String data) {
        return "";
    }
}
```

Restrictions: No `main()`, no `Scanner`, no `System.in`, no interactive I/O.

### C++

```cpp
#include <string>
using namespace std;

string solve(const string& data) {
    return "";
}
```

Restrictions: No `main()`, no `cin`, no `cout` for protocol output, no interactive I/O. Additional standard headers (`<vector>`, `<map>`, `<sstream>`, `<regex>`, etc.) are permitted.

### JavaScript

```javascript
function solve(data) {
    // Implement only the required solution logic.
    // Return the required result as a string.
    return "";
}

module.exports = { solve };
```

Restrictions: No `readline`, no `process.stdin`, no interactive I/O. Built-in modules (`String`, `Array`, `Map`, `RegExp`, `JSON`, `Math`) are permitted. No `require('fs')`, no `require('http')`, no external npm packages.

---

## Test Case Design Rules

For each problem, test cases should be deliberately designed:

| Type | Purpose |
|------|---------|
| `normal` | Standard expected input |
| `boundary` | Minimum or maximum allowed values |
| `edge` | Unusual but valid input |
| `adversarial` | Input designed to expose unsafe behaviour |
| `stress` | Large input to reveal performance differences |

Use `adversarial` cases only for problems in categories C–J where the research question explicitly evaluates security or validation behaviour.

---

## Security Problem Design Rules

Security problems must follow these rules to remain scientifically valid:

1. Deterministic — same input always produces same output.
2. Offline — no network access, no external services.
3. Predefined inputs — same test cases for AI and Human.
4. No real credentials, no destructive actions.
5. No arbitrary command execution.
6. Static analysis tools can detect relevant insecure patterns for each supported language.
7. Functional test cases can expose unsafe behaviour where appropriate.
8. Do NOT require a real database, filesystem, or shell.

---

## Balanced Dataset Target

The benchmark aims for balance across:

- 10 categories (A–J) with 5 problems each
- 10 test cases per problem (at least 1 boundary and 1 edge per problem)
- All 50 problems support all 4 languages
- Security-focused problems in categories C–J provide meaningful Bandit/SpotBugs/cppcheck/eslint findings

This document must be updated when any problem is added or modified.
