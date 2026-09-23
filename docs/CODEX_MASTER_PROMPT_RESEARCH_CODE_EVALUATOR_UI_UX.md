# CODEX MASTER PROMPT — RESEARCH CODE EVALUATOR
## UI/UX REDESIGN + NAVIGATION ARCHITECTURE ONLY

You are working on my MCA research project:

**Research Title:** “An Empirical Study on the Reliability, Security, and Maintainability of AI-Generated Code in Software Development.”

**Software Instrument:** **Research Code Evaluator**

Your task is to perform a **professional UI/UX redesign and navigation architecture improvement ONLY**.

---

## 1. ABSOLUTE PRIORITY — DO NOT CHANGE RESEARCH FUNCTIONALITY

This is the most important instruction.

### DO NOT MODIFY:
- Research methodology
- Research workflow logic
- Evaluation methodology
- Scoring formulas
- Reliability, performance, security, maintainability, complexity, or code-quality calculations
- Statistical calculations
- AI-vs-Human comparison logic
- Execution engine
- Sandbox/compiler/runtime behavior
- Timeout rules
- Test-case execution
- Expected outputs
- Programming problem definitions
- Problem IDs, statements, categories, difficulty, or language definitions
- AI model data
- Human submission data
- Database research meaning
- Existing API contracts
- Existing backend behavior
- Existing analysis tools
- Existing report calculations
- Existing research records

**Do not rewrite, refactor, optimize, “clean up,” or improve the research engine.**

### Frozen benchmark

The project is designed for:

- **50 research problems: P001–P050**
- **500 total test cases**
- **10 test cases per problem**
- Python
- Java
- C++
- JavaScript

Protect **P001–P050 and all associated test cases**.

Do not rename, delete, regenerate, reorder, simplify, replace, or modify any problem or test case.

Do not create fake research data.

---

## 2. YOUR ROLE

Act as a:

- Senior UI/UX engineer
- Senior frontend engineer
- Design-system engineer
- Navigation/routing engineer

You are NOT being asked to redesign the research methodology, backend, evaluation algorithm, or database research model.

Your job is:

> Make the existing Research Code Evaluator look and behave like a polished professional research/software-engineering platform while keeping all existing functionality and research behavior unchanged.

---

## 3. FIRST STEP — INSPECT BEFORE MODIFYING

Before making changes:

1. Inspect the repository.
2. Identify the frontend framework and routing implementation.
3. Identify all existing pages/routes.
4. Identify reusable components.
5. Identify existing API calls.
6. Identify state management.
7. Identify the evaluation workflow.
8. Identify the problem/test-case data flow.
9. Identify current navigation behavior.
10. Identify where browser history currently works or fails.
11. Identify the safest UI files/components to modify.
12. Create/use a safe rollback point before major changes.

Do not assume the architecture. Preserve the existing working architecture wherever possible.

---

## 4. DESIGN REFERENCE — CLAUDE “ARCHIVE”

Use the provided Claude UI/UX mockups as the primary visual reference.

The direction is called **Archive**.

Desired character:

- Professional
- Academic
- Research-oriented
- Technical
- Premium
- Calm
- Human-designed
- Distinctive
- Clean
- Classy

It must NOT look like a generic AI-generated SaaS dashboard.

Avoid:

- Neon gradients
- Purple/blue AI clichés
- Excessive glassmorphism
- Excessive shadows
- Excessive rounded cards
- Huge decorative elements
- Excessive animations
- Futuristic “AI” effects
- Unnecessary gradients
- Overly colorful dashboards
- Childish colors
- Visual clutter

The application should look like a serious research and software-engineering platform.

---

## 5. VISUAL DESIGN SYSTEM

Use the Archive concept as the design foundation.

Suggested starting tokens:

- Primary / Ink Blue: `#1F3347`
- Secondary / Slate: `#56677A`
- Accent / Muted Brass: `#B8862B`
- Background / Paper: `#F6F4EE`
- Surface / Card: `#FFFFFF`
- AI chart color: approximately `#2A6F97`
- Human chart color: approximately `#C2732A`

Implement these through reusable design tokens/theme variables. Do not scatter raw colors throughout components.

Do not use brass for large primary buttons or large fills. Use it as restrained emphasis.

### Typography

Preferred direction:

- **IBM Plex Sans** — UI/body
- **IBM Plex Mono** — code, IDs, technical values, metrics
- **Source Serif 4** — major page/research headings

Use serif selectively; do not make the entire application serif.

Suggested hierarchy:

- H1: Source Serif 4, ~30px
- H2: Source Serif 4, ~22px
- H3/card title: IBM Plex Sans, ~16px
- Body: IBM Plex Sans, ~14px
- Long-form/report text: ~16px
- Code: IBM Plex Mono, ~13px
- Important metric numbers: IBM Plex Mono with tabular numerals

---

## 6. GENERAL UI PRINCIPLES

Implement:

- Clear visual hierarchy
- Consistent spacing
- Strong readability
- Subtle borders
- Restrained shadows
- Consistent card radius
- Consistent buttons/inputs
- Consistent tables and badges
- Clear hover/active/disabled states
- Loading, empty and error states
- Reusable components/tokens

Avoid random styling, excessive card variants, excessive decoration, or duplicated CSS.

---

## 7. SIDEBAR / INFORMATION ARCHITECTURE

Use a professional left-sidebar structure similar to the reference:

### WORKSPACE
- Dashboard
- Problem Library
- Evaluations

### ANALYSIS
- Research Analytics
- Model Comparison
- Problem Analysis

### OUTPUT
- Reports

### SYSTEM
- Settings

Adapt this to the existing application. Do not remove functional pages merely because they are not in the mockup.

---

## 8. DASHBOARD

Redesign the Dashboard as a professional research overview.

Use **real application data only**.

Show, where already supported:

- Research progress
- Problems evaluated out of 50
- Six primary metrics:
  - Reliability
  - Performance
  - Security
  - Maintainability
  - Complexity
  - Code Quality
- Recent evaluations
- Draft/incomplete/error states
- Useful next action

Never hardcode mock research values.

---

## 9. PROBLEM LIBRARY

Create a polished benchmark browser.

Support the existing functionality for:

- Search
- Category
- Difficulty
- Language
- Status
- Sorting if already available

Use a clean table/list with fields such as:

- Problem ID
- Title
- Category
- Difficulty
- Languages
- Status
- Last evaluated

All **P001–P050** must remain accessible.

Do not change benchmark content.

---

## 10. PROBLEM DETAILS

If present, redesign it professionally while preserving its real content:

- Problem ID
- Title
- Description
- Constraints
- Function/method signature
- Supported languages
- Evaluation status
- Existing submission state

Do not rewrite problem definitions.

---

## 11. CODE SUBMISSION / EVALUATION

This is one of the most important screens.

Use a clear workflow:

**01 Select Problem → 02 Submit Code → 03 Evaluate → 04 Results → 05 Detailed Metrics**

Clearly distinguish:

### AI-generated
from
### Human-written

Preserve all existing editor behavior, language selection, AI-model selection, submission, validation and evaluation actions.

Only improve:

- Layout
- Typography
- Labels
- Spacing
- Toolbar styling
- Error presentation
- Responsive behavior

Do NOT change how code is processed.

---

## 12. EVALUATION RESULT

Make this one of the strongest screens.

Show real existing information:

- Evaluation ID
- Problem
- Language
- Date/time
- Scoring/test version if already present
- AI result
- Human result
- Tests passed
- Tests failed/errors/timeouts
- Six metric comparisons

Use professional comparison charts/tables.

Do not generate values.

---

## 13. TEST CASE RESULTS

Use a clean table such as:

| Test | Input | Expected | AI | Human |
|------|-------|----------|----|-------|

Preserve actual statuses:

- PASS
- FAIL
- ERROR
- TIMEOUT

Do not change their meaning.

---

## 14. ANALYTICS / REPORTS

Redesign existing pages without changing calculations.

Possible existing areas:

- Research Analytics
- Model Comparison
- Problem Analysis
- Reports

Use actual database/API data.

Do not change formulas, statistical methodology, or research interpretation.

---

# 15. AI VS HUMAN VISUAL RULE

AI and Human must be distinguishable, but **never by color alone**.

Use combinations of:

- Color
- Icon
- Text label
- Chart marker/shape

For example, charts may use different marker shapes.

AI/Human colors are categorical identifiers, NOT quality judgments.

The application's main interaction color should remain separate from the AI/Human series colors.

---

# 16. NAVIGATION — CRITICAL REQUIREMENT

The current application requires too much menu clicking.

Fix this.

The application must behave like a normal professional web application.

Example:

**Dashboard → Problem Library → Problem Details → Submit → Result**

The user must be able to move backward naturally.

### Browser Back
Must work correctly.

### Browser Forward
Must work correctly.

### Mouse Back/Forward
Must work through normal browser history.

### Laptop Trackpad
Two-finger back/forward gestures must work through browser history.

### Keyboard
Do not block normal browser shortcuts such as:
- Alt + Left = Back
- Alt + Right = Forward

Do not intercept these unnecessarily.

---

# 17. ROUTING ARCHITECTURE

Use the existing routing framework if one already exists.

Do NOT replace the entire routing architecture unnecessarily.

The goal is:

> Correct route-based navigation + browser history + shareable URLs + sensible state restoration.

Conceptually, routes may resemble:

- `/dashboard`
- `/problems`
- `/problems/:id`
- `/evaluations`
- `/evaluations/:id`
- `/analytics`
- `/model-comparison`
- `/problem-analysis`
- `/reports`
- `/settings`

Use the project's existing route conventions if different.

Do not create duplicate routing systems.

---

# 18. URL STATE

Where appropriate, keep search/filter/sort state in the URL.

Example:

`/problems?category=security&language=python`

Browser Back should restore relevant previous filters/search state.

Do not put sensitive submitted code into URLs.

---

# 19. CONTEXTUAL BACK BUTTONS

Add clear Back buttons where useful:

- Problem Details → `← Back to Problem Library`
- Evaluation Result → `← Back`
- Detailed Analysis → `← Back to Evaluation Result`

But do NOT make the sidebar or custom Back buttons a replacement for real browser history.

---

# 20. BREADCRUMBS

Use breadcrumbs where they improve orientation.

Example:

`Problem Library / P003 Binary Search / Evaluation / Result`

Do not add them unnecessarily to every page.

---

# 21. ACCESSIBILITY

Target WCAG 2.2 AA principles.

Implement:

- Good text contrast
- Visible keyboard focus
- Keyboard-accessible controls
- Semantic HTML
- Proper input labels
- Accessible tables
- Accessible navigation
- Meaningful ARIA where required
- Screen-reader-friendly status changes
- No color-only meaning
- Practical hit targets
- Reduced-motion support

For statuses use:

**icon + color + text**

For AI/Human charts use:

**color + label + marker shape** where practical.

---

# 22. RESPONSIVE DESIGN

Primary target:

- Laptop
- Desktop

Also support tablet.

Keep the main research workflow comfortable on laptop screens.

Do not sacrifice desktop usability for unnecessary mobile-first complexity.

---

# 23. MOTION

Keep motion minimal.

Use only subtle transitions/fades where useful.

Avoid:

- Animated gradients
- Bouncing cards
- Excessive effects
- Marketing-style animation

Respect:

`prefers-reduced-motion`

---

# 24. DATA INTEGRITY — CRITICAL

All UI values must come from the existing application.

Never hardcode:

- Scores
- Problem counts
- Test counts
- Evaluation dates
- AI model results
- Reliability
- Security
- Maintainability
- Performance
- Complexity
- Code quality

The Claude screenshots contain illustrative values only.

They are NOT research data.

---

# 25. DO NOT MODIFY THE BENCHMARK

Frozen:

- P001–P050
- All test cases
- Expected outputs
- Problem statements
- Function/method contracts
- Language definitions
- Execution rules

If you discover a benchmark issue while implementing the UI:

**STOP and report it.**

Do not silently change the benchmark.

---

# 26. DO NOT MODIFY BACKEND/DATABASE FOR COSMETIC REASONS

Do not rewrite backend APIs just to make the UI easier.

Prefer frontend-only changes.

If a backend change is absolutely required for UI/navigation compatibility, it must:

1. Not alter research behavior.
2. Not alter stored research meaning.
3. Be backward compatible.
4. Be clearly reported.

Do not delete/reset/recalculate research records.

---

# 27. ERROR / LOADING / EMPTY STATES

Implement professional states for major pages.

### Loading
Use appropriate skeleton/spinner.

### Error
Explain the problem and provide Retry where appropriate.

### Empty
Explain what is missing and give the next useful action.

Never fill empty screens with fake research data.

---

# 28. DESIGN SYSTEM IMPLEMENTATION

Create reusable tokens/components for:

- Colors
- Typography
- Spacing
- Radius
- Shadows
- Borders
- Buttons
- Inputs
- Cards
- Tables
- Badges
- Tabs
- Breadcrumbs
- Sidebar
- Navigation
- Alerts
- Metric cards
- Chart containers

Keep the implementation maintainable.

---

# 29. FUNCTIONAL REGRESSION REQUIREMENT

After the redesign, these existing workflows must still work:

1. Dashboard
2. Problem Library
3. Search/filter
4. Open problem
5. Select language
6. Submit AI code
7. Submit human code
8. Select AI model where applicable
9. Run evaluation
10. Execute test cases
11. Generate metrics
12. Save results
13. View evaluation result
14. View detailed metrics
15. View analytics
16. View model comparison
17. View problem analysis
18. View reports
19. Navigate backward/forward

The UI redesign must not change any underlying behavior.

---

# 30. RESEARCH EXPERIMENT PROTECTION

The same experimental conditions must remain unchanged for AI and Human:

- Same problem
- Same language
- Same test cases
- Same execution environment
- Same limits
- Same timeout
- Same evaluation logic
- Same scoring methodology
- Same static-analysis methodology
- Same database meaning

The redesign is **presentation + navigation only**.

---

# 31. IMPLEMENTATION ORDER

Work incrementally:

### Phase 1
Inspect repository + safe rollback point.

### Phase 2
Design tokens/theme.

### Phase 3
Global typography/layout.

### Phase 4
Sidebar/navigation.

### Phase 5
Routing/history fixes.

### Phase 6
Dashboard.

### Phase 7
Problem Library.

### Phase 8
Problem Details.

### Phase 9
Submission/Evaluation.

### Phase 10
Evaluation Result.

### Phase 11
Analytics/Reports/remaining pages.

### Phase 12
Accessibility/responsive polish.

### Phase 13
Full regression testing.

Do not perform a giant unrelated refactor.

---

# 32. VALIDATION

### Navigation
Test:

- Sidebar navigation
- Browser Back
- Browser Forward
- Mouse Back
- Trackpad Back
- Keyboard Back
- Direct URL access
- Refresh
- Deep links
- Search/filter state restoration
- Breadcrumbs
- Contextual Back buttons

### UI
Test every major page.

### Functional regression
Verify:

- Code submission
- Evaluation
- Test execution
- Metrics
- Database storage
- Existing results
- Reports

### Benchmark integrity
Verify:

- P001–P050 still exist
- Test cases unchanged
- No problem deleted
- No test case modified
- No fake research data added

---

# 33. VISUAL QUALITY CHECK

Before completion, inspect every major page.

Confirm:

- Professional appearance
- Academic/research identity
- Human-designed appearance
- Clear hierarchy
- Good spacing
- Restrained colors
- Consistent typography
- Readable tables
- Understandable charts
- Clear AI/Human distinction
- Natural navigation
- Good laptop experience
- No generic AI-dashboard appearance

---

# 34. FINAL CHANGE REPORT

When finished, provide:

### UI
- Pages redesigned
- Design system implemented
- Major visual changes

### Navigation
- Routes changed
- Browser history behavior
- Back/Forward behavior
- URL-state behavior

### Accessibility
- Keyboard navigation
- Focus
- Contrast
- AI/Human non-color distinction

### Research safety
Explicitly confirm:

- P001–P050 preserved
- Test cases preserved
- Research calculations preserved
- Evaluation logic preserved
- Database research data preserved
- AI-vs-Human methodology preserved

### Testing
Report:

- Frontend build result
- Navigation test result
- Functional regression result
- Benchmark integrity result

### Files changed
List important files/components modified.

### Important files intentionally untouched
List backend/research files deliberately not modified.

---

# 35. FINAL SAFETY RULE

If there is ever a conflict between UI/UX improvement and research functionality:

**RESEARCH FUNCTIONALITY ALWAYS WINS.**

Do not solve the conflict by changing research behavior.

Stop, preserve the research system, and report the conflict.

---

# FINAL OBJECTIVE

Transform the existing Research Code Evaluator into a:

**professional, premium, academic-grade research + software-engineering platform**

using the Claude **Archive** mockups as the visual reference.

But preserve **100% of the existing research functionality and benchmark integrity**.

The highest-priority requirements are:

1. **DO NOT CHANGE RESEARCH FUNCTIONALITY**
2. **DO NOT CHANGE P001–P050**
3. **DO NOT CHANGE TEST CASES**
4. **DO NOT CHANGE SCORING/EVALUATION LOGIC**
5. **DO NOT CHANGE EXISTING RESEARCH DATA**
6. **IMPLEMENT PROFESSIONAL UI/UX**
7. **IMPLEMENT PROPER ROUTING AND BROWSER HISTORY**
8. **MAKE BROWSER/MOUSE/TRACKPAD BACK-FORWARD WORK NATURALLY**
9. **USE THE ARCHIVE DESIGN DIRECTION FROM THE CLAUDE REFERENCES**
10. **USE REAL APPLICATION DATA — NEVER MOCK RESEARCH RESULTS**
11. **TEST EVERYTHING AFTER THE REDESIGN**

If any visual request risks breaking research functionality, do not silently change the functionality. Preserve it and report the issue.
