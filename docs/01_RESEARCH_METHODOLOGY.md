# Research Methodology

## Research Title

An Empirical Study on the Reliability, Security, and Maintainability of AI-Generated Code in Software Development

## Research Objective

This research empirically compares AI-generated code with human-written code using the same predefined programming problems, identical test cases, and the same execution and analysis environment.

The comparison focuses on:

- Reliability
- Performance
- Maintainability
- Security
- Complexity
- Code Quality

## Research Instrument

The software is a research instrument used to:

1. Select a predefined programming problem.
2. Accept AI-generated code.
3. Accept human-written code.
4. Execute both codes using the same test cases.
5. Measure execution and code-quality characteristics.
6. Compare the results.
7. Store the results automatically.
8. Present research progress and reports.

The software does not generate AI code.

## Supported Programming Languages

The research instrument supports four programming languages:

- **Python** (3.x)
- **Java** (17 or later)
- **C++** (C++17 or later, compiled with g++)
- **JavaScript** (Node.js 18 or later)

All four languages use the same controlled code contract: a single deterministic function that receives the test-case input as a string and returns the result as a string. The evaluator owns execution; submitted code must not use interactive I/O.

## AI-Generated Code

AI code is generated externally using systems such as:

- ChatGPT
- Claude
- Gemini
- Other AI coding systems

The researcher copies the generated code into the AI-Written Code section of the application.

The application only records the AI system name and the submitted AI source code.

The application does not:

- generate AI code
- call AI APIs
- require AI API keys
- manage AI accounts
- generate prompts

## Human-Written Code

Human-written code is entered into the Human-Written Code section.

No human name or participant ID is required.

## Controlled Comparison

For every selected problem:

- AI and human code solve the same problem.
- Both use the same programming language.
- Both use the same predefined test cases.
- Both execute under the same conditions.
- Both use the same execution limits.
- Both are analysed using the same applicable tools for that language.
- Both use the same evaluation methodology.

## Research Problem Bank

The application uses a predefined research problem bank.

Each problem contains:

- Problem ID
- Title
- Description
- Category
- Difficulty
- Supported language(s)
- Predefined test cases

The researcher selects problems from this predefined bank.

## Research Data

Each completed comparison produces structured research data containing:

- Problem
- Programming language
- AI system name
- AI source code
- Human source code
- Test-case results
- Execution time
- Reliability measurements
- Maintainability measurements
- Security findings
- Complexity measurements
- Code-quality measurements
- Comparison results
- Timestamp

The collected records form the research dataset.

## Objectivity

The application must report measured results objectively.

A single comparison must not be used to claim that AI is universally better than humans or that humans are universally better than AI.

The final research conclusions must be based on the complete collected dataset and appropriate statistical analysis.

## Research Progress

The application tracks:

- Total problems
- Completed problems
- Remaining problems
- Completion percentage
- Total comparisons
- AI systems used
- AI versus human outcomes

The dashboard provides visual representations of this information.

## Scope

The project focuses on empirical evaluation and comparison of source code.

It does not include:

- AI model training
- AI model development
- AI API integration
- Chatbot functionality
- User authentication
- Participant account management
- AI prompt generation
- AI code generation inside the application

## Research Goal

The final dataset should provide empirical evidence for comparing AI-generated and human-written code across the selected software-quality dimensions.

The evaluation process must be consistent, repeatable, measurable, and suitable for academic research.
