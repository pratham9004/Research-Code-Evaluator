# Software Requirements

## 1. Application Name

Research Code Evaluator

## 2. Purpose

The application is a research-focused software system used to compare AI-generated and human-written source code.

The application must be simple, user-friendly, visually clear, and focused on research data collection.

## 3. Main Navigation

The application should contain three primary sections:

- Dashboard
- Solve Problems
- Reports

Avoid unnecessary navigation and unnecessary forms.

## 4. Dashboard

The Dashboard is the main landing page.

It must show:

- Total Problems
- Completed Problems
- Remaining Problems
- Completion Percentage
- Total Comparisons
- AI Systems Used

## 5. Dashboard Visualizations

The Dashboard must contain clear visual charts.

### Research Progress

Show completed versus remaining problems.

### AI Systems Used

Show how many comparisons were performed using each AI system.

Example:

- ChatGPT
- Claude
- Gemini

### Languages Used

Show how many comparisons were performed in each language:

- Python
- Java
- C++
- JavaScript

### AI vs Human Outcomes

Show:

- AI better
- Human better
- Comparable

The result must be calculated from the configured research comparison methodology.

### Metric Comparison

Provide visual comparisons for:

- Reliability
- Performance
- Maintainability
- Security
- Complexity
- Code Quality

Charts must be easy to understand.

## 6. Solve Problems

The Solve Problems page is the main data-entry page.

The researcher selects a predefined problem.

The selected problem displays its description and available language(s).

## 7. Code Comparison Interface

The page contains two clearly separated code editors.

### AI-Written Code

Fields:

- AI Name
- AI Source Code

### Human-Written Code

Fields:

- Human Source Code

No human name is required.

No participant ID is required.

## 8. Language

If the selected problem supports multiple languages, the researcher selects the language.

The same language must be used for both AI and human code.

Supported languages: Python, Java, C++, JavaScript.

## 9. Submit

There must be one common primary button:

**Submit & Compare**

The system validates both code inputs before starting evaluation.

## 10. Evaluation

After submission, the system automatically:

1. Validates the submitted code against the entry contract for the selected language.
2. Executes AI code.
3. Executes human code.
4. Runs the same predefined test cases.
5. Measures execution performance (runtime only; compilation excluded from metric).
6. Runs applicable static analysis for the selected language.
7. Calculates research metrics.
8. Compares AI and human results.
9. Generates a report.
10. Stores the results in the database.
11. Updates the Dashboard.

## 11. Execution Feedback

While evaluation is running, the interface should clearly show progress such as:

- Running AI code
- Running Human code
- Running test cases
- Analysing code
- Generating report
- Saving results

The interface must provide clear feedback instead of appearing frozen.

## 12. Comparison Report

The report must display:

- Problem
- Language
- AI name
- Test-case results
- Execution time
- Reliability
- Maintainability
- Security
- Complexity
- Code Quality
- AI-human differences
- Statistical information where applicable

## 13. Neutral Reporting

The system should use neutral research language.

For example:

"AI code recorded a higher reliability score."

Instead of:

"AI is better."

The application must not make unsupported universal claims.

## 14. Reports Section

The Reports section lists completed comparisons.

Each report should provide:

- Problem
- AI system
- Language
- Completion status
- View Report action

The researcher can open any completed report to see the detailed comparison.

## 15. Problem Bank

The application must use a predefined research problem bank.

Each problem should provide:

- Problem title
- Category
- Difficulty
- Supported language(s)
- Completion status

The normal application workflow must not require manual creation of test cases.

## 16. Progress Tracking

The application must automatically update research progress after each completed comparison.

The Dashboard must reflect:

- Completed problems
- Remaining problems
- Completion percentage
- Total comparisons
- AI systems used
- Languages used
- AI versus human outcomes

## 17. AI Integration

The application must NOT:

- call ChatGPT APIs
- call Claude APIs
- call Gemini APIs
- generate AI code
- manage AI accounts
- store AI API keys
- generate prompts

AI code is generated externally and pasted into the application.

## 18. Authentication

The initial research prototype does not require:

- Login
- Registration
- User accounts
- Participant accounts

## 19. Execution Safety

The execution engine must:

- enforce execution timeouts (10 seconds per variant)
- isolate code execution in a temporary directory via subprocess
- capture output
- capture errors
- handle timeouts
- clean temporary files
- prevent one submission from affecting another

### Language-Specific Safety Requirements

**Python:** No `input()`, no `exec()`, no `eval()` for research submissions. Harness imports and calls `solve`.

**Java:** Compiled via `javac`; run via `java Runner`. Submission must not contain a `main()` method or interactive I/O.

**C++:** Compiled via `g++ -std=c++17`. Submission must define only `solve`. No `main()`, no `cin`/`cout` for protocol I/O.

**JavaScript:** Run via `node`. Submission must define `function solve(data)` or `module.exports = { solve }`. No `readline` or interactive I/O.

## 20. Responsive UI

The application should be usable on:

- Desktop
- Laptop
- Tablet

The primary comparison interface should be optimized for larger screens because two code editors are displayed side by side.

## 21. UI/UX Principles

The interface must be:

- simple
- clean
- professional
- easy to navigate
- research-focused
- visually understandable

Use:

- clear navigation
- consistent spacing
- readable typography
- meaningful cards
- useful charts
- readable tables
- clear status indicators
- accessible colour usage

Avoid:

- unnecessary forms
- unnecessary pages
- unnecessary metadata
- complicated workflows
- excessive configuration

## 22. Testing

The application must include automated tests for:

- problem retrieval
- test-case execution (all four languages)
- Python execution (PASS/FAIL/ERROR/TIMEOUT)
- Java execution (PASS/FAIL/ERROR/TIMEOUT)
- C++ execution (PASS/FAIL/ERROR/TIMEOUT)
- JavaScript execution (PASS/FAIL/ERROR/TIMEOUT)
- static analysis (tool available and tool unavailable paths)
- metric calculation
- comparison calculation
- database storage
- report generation
- dashboard aggregation
- research export

Important frontend workflows should also be tested.

## 23. Final Workflow

```
Dashboard
    ↓
Solve Problems
    ↓
Select Problem
    ↓
Select Language (Python / Java / C++ / JavaScript)
    ↓
AI-Written Code + Human-Written Code
    ↓
Submit & Compare
    ↓
Same Test Cases
    ↓
Execute Both
    ↓
Analyse Both
    ↓
Calculate Metrics
    ↓
Compare Results
    ↓
Generate Report
    ↓
Save to Database
    ↓
Update Dashboard
    ↓
Reports
```

## 24. Definition of Done

The application is complete when:

- predefined problems work
- predefined test cases work
- AI and human code can be entered side by side
- AI name can be entered
- no human identity is required
- both codes use the same problem and language
- both codes use the same test cases
- both codes execute correctly for all four languages
- reliability is calculated
- performance is measured
- maintainability is calculated
- security is analysed (tool or TOOL_UNAVAILABLE noted)
- complexity is analysed
- code quality is analysed
- results are compared
- results are automatically stored
- dashboard progress updates automatically
- dashboard charts display research information
- languages used chart is visible
- AI usage is visible
- AI versus human outcomes are visible
- reports are accessible
- research data can be exported
- the interface is simple and user-friendly
- no AI API integration is required
- no unnecessary user metadata is required
- no fabricated research data is generated
