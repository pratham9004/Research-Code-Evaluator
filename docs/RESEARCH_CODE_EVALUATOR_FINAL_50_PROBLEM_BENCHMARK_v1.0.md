# Research Code Evaluator --- Final 50-Problem Benchmark

**Benchmark version:** 1.0\
**Status:** Draft for researcher approval --- do not implement until
approved\
**Project:** An Empirical Study on the Reliability, Security, and
Maintainability of AI-Generated Code in Software Development

## 1. Purpose

This document defines the proposed replacement benchmark for the current
6-problem bank. It is designed to fit the existing Research Code
Evaluator rather than change the research methodology.

**Target:** 50 predefined problems × 10 deterministic test cases = **500
frozen test cases**.

The same problem statement, language, tests, execution limits, and
analysis configuration must be used for AI-generated and human-written
submissions. AI code continues to be generated externally and pasted
into the evaluator; the application does not generate AI code.

## 2. Compatibility with the existing project

This benchmark preserves the existing project contract:

-   Six dimensions remain: Reliability, Performance, Maintainability,
    Security, Complexity, Code Quality.
-   Existing scoring weights remain unchanged: Reliability 20%,
    Performance 15%, Maintainability 20%, Security 15%, Complexity 15%,
    Code Quality 15%.
-   Taxonomy fields remain contextual metadata; they are not hidden
    scoring multipliers.
-   Problems are deterministic and offline.
-   No real credentials, external network, production database,
    destructive action, or arbitrary OS command is required.
-   The evaluator remains responsible for execution, timeouts,
    isolation, static analysis, scoring, persistence, and reporting.
-   Security-focused functional tests provide behavioral evidence but do
    **not** silently replace the existing static-analysis-based security
    score.

## 3. Controlled code contract

### Python

``` python
def solve(data: str) -> str:
    # Implement only the required solution logic.
    # Return the required result as a string.
    pass
```

### Java

``` java
public class Solution {
    public static String solve(String data) {
        return "";
    }
}
```

Do not add `input()`, protocol `print()`, `Scanner`, `main()`,
interactive I/O, or a custom test runner. The evaluator owns execution.

## 4. Test-case standard

Each problem has exactly 10 deterministic test cases. Test types are
`normal`, `boundary`, `edge`, `adversarial`, and `stress`.

Rules: - At least one boundary and one edge case per problem. -
Adversarial cases are used only where validation/security behavior is
part of the research purpose. - The exact inputs and expected outputs
below are benchmark data; the evaluator must not generate replacements
dynamically. - Expected outputs must never be changed because a
submitted solution fails. - If a benchmark defect is discovered after
freezing, create a new benchmark version and re-run affected
observations.

**Input notation:** In the tables, `\|` means a literal pipe character,
`\n` newline, `\r` carriage return, `\t` tab, and `(empty)` means an
empty string. The implementation must store the corresponding actual
characters.

## 5. Category distribution

  Category      Problems Main research purpose
  ----------- ---------- -----------------------------------------------
  A                    5 Classic algorithmic correctness
  B                    5 Data processing and parsing
  C                    5 Input validation
  D                    5 String sanitization/output safety
  E                    5 Path/file safety
  F                    5 SQL/query safety
  G                    5 Command/shell safety
  H                    5 Safe parsing/configuration
  I                    5 Resource/performance safety
  J                    5 Authentication/token/authorization validation
  **Total**       **50** 

## 6. Final problem catalogue

### Category A --- Classic Algorithmic Correctness

Baseline algorithmic correctness, boundary handling, performance, and
structural complexity.

#### P001 --- Two Sum

-   **Difficulty:** Easy
-   **Research focus:** reliability,performance,complexity
-   **Security relevance:** low
-   **Task:** Find two indices whose values sum to target. Return
    indices in ascending order; return -1 -1 if absent.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input             Expected output   case_type
  ---- ----------------- ----------------- ------------
     1 `2 7 11 15\|9`    `0 1`             `normal`
     2 `3 2 4\|6`        `1 2`             `normal`
     3 `3 3\|6`          `0 1`             `edge`
     4 `1 2\|3`          `0 1`             `boundary`
     5 `1 2 3\|7`        `-1 -1`           `normal`
     6 `-3 4 5 9\|-8`    `0 2`             `edge`
     7 `0 0 0\|0`        `0 1`             `edge`
     8 `5 -2 8 1\|-1`    `1 3`             `normal`
     9 `10\|10`          `-1 -1`           `boundary`
    10 `-5 -3 -1 2\|1`   `2 3`             `normal`

#### P002 --- Maximum Subarray Sum

-   **Difficulty:** Easy
-   **Research focus:** reliability,performance,complexity
-   **Security relevance:** low
-   **Task:** Return the maximum sum of a contiguous non-empty subarray.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input                     Expected output   case_type
  ---- ------------------------- ----------------- ------------
     1 `1 2 3 4`                 `10`              `normal`
     2 `-2 1 -3 4 -1 2 1 -5 4`   `6`               `normal`
     3 `-5 -2 -8`                `-2`              `edge`
     4 `0`                       `0`               `boundary`
     5 `5 -1 2 -1 3`             `8`               `normal`
     6 `-1 0 -2 0`               `0`               `edge`
     7 `10 -20 5 6 -2 8`         `17`              `normal`
     8 `-3 4 -1 2 -1`            `5`               `normal`
     9 `2 -1 2 -1 2`             `4`               `edge`
    10 `-10 -1 -5`               `-1`              `boundary`

#### P003 --- Binary Search

-   **Difficulty:** Easy
-   **Research focus:** reliability,performance,complexity
-   **Security relevance:** low
-   **Task:** Return the first index of target in a sorted integer
    array, or -1.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input              Expected output   case_type
  ---- ------------------ ----------------- ------------
     1 `1 3 5 7 9\|1`     `0`               `normal`
     2 `1 3 5 7 9\|9`     `4`               `normal`
     3 `1 3 5 7 9\|5`     `2`               `normal`
     4 `1 3 5 7 9\|4`     `-1`              `normal`
     5 `1\|1`             `0`               `boundary`
     6 `1\|-1`            `-1`              `boundary`
     7 `2 2 2 3\|2`       `0`               `edge`
     8 `-5 -2 0 4 9\|0`   `2`               `edge`
     9 `-3 -1 2 8\|8`     `3`               `normal`
    10 `-3 -1 2 8\|-3`    `0`               `normal`

#### P004 --- Merge Sorted Arrays

-   **Difficulty:** Easy
-   **Research focus:**
    reliability,performance,complexity,maintainability
-   **Security relevance:** low
-   **Task:** Merge two sorted integer arrays into one sorted array.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input               Expected output    case_type
  ---- ------------------- ------------------ ------------
     1 `1 3 5\|2 4 6`      `1 2 3 4 5 6`      `normal`
     2 `1 2\|`             `1 2`              `boundary`
     3 `\|3 4`             `3 4`              `boundary`
     4 `-2 0 3\|-1 1 4`    `-2 -1 0 1 3 4`    `normal`
     5 `1 1 2\|1 2 2`      `1 1 1 2 2 2`      `edge`
     6 `0\|0`              `0 0`              `edge`
     7 `-5 -3\|-4 -2 -1`   `-5 -4 -3 -2 -1`   `normal`
     8 `5 7\|1 2 9`        `1 2 5 7 9`        `normal`
     9 `2 4 6\|1 3 5`      `1 2 3 4 5 6`      `normal`
    10 `9 10\|11`          `9 10 11`          `boundary`

#### P005 --- Balanced Brackets

-   **Difficulty:** Easy
-   **Research focus:** reliability,maintainability,code_quality
-   **Security relevance:** low
-   **Task:** Return VALID if (), \[\], {} are properly balanced;
    otherwise INVALID.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input       Expected output   case_type
  ---- ----------- ----------------- ------------
     1 `()`        `VALID`           `normal`
     2 `([])`      `VALID`           `normal`
     3 `([{}])`    `VALID`           `normal`
     4 `(]`        `INVALID`         `edge`
     5 `([)]`      `INVALID`         `edge`
     6 `(empty)`   `VALID`           `boundary`
     7 `{[()]}`    `VALID`           `normal`
     8 `(((`       `INVALID`         `boundary`
     9 `}{`        `INVALID`         `edge`
    10 `()[]{}`    `VALID`           `normal`

### Category B --- Data Processing / Parsing

Parsing ambiguity, malformed data handling, and maintainability.

#### P006 --- CSV Record Field Count

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,maintainability,code_quality
-   **Security relevance:** medium
-   **Task:** Count comma-separated fields while treating commas inside
    double quotes as data; return field count.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input         Expected output   case_type
  ---- ------------- ----------------- ------------
     1 `a,b,c`       `3`               `normal`
     2 `"a,b",c`     `2`               `edge`
     3 `"a,b,c"`     `1`               `edge`
     4 `a,,c`        `3`               `normal`
     5 `(empty)`     `1`               `boundary`
     6 `"a","b",c`   `3`               `normal`
     7 `"a""b",c`    `2`               `edge`
     8 `a,b,`        `3`               `boundary`
     9 `"",x`        `2`               `edge`
    10 `a,b,c,d`     `4`               `normal`

#### P007 --- Log Level Counter

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,performance,maintainability
-   **Security relevance:** low
-   **Task:** Given one log level per line, return counts
    ERROR,WARN,INFO in that order.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input                        Expected output   case_type
  ---- ---------------------------- ----------------- ------------
     1 `ERROR\nWARN\nINFO`          `1 1 1`           `normal`
     2 `INFO\nINFO\nINFO`           `0 0 3`           `normal`
     3 `ERROR\nERROR`               `2 0 0`           `edge`
     4 `WARN`                       `0 1 0`           `boundary`
     5 `(empty)`                    `0 0 0`           `boundary`
     6 `DEBUG\nTRACE`               `0 0 0`           `edge`
     7 `ERROR\nINFO\nWARN\nERROR`   `2 1 1`           `normal`
     8 `warn\nERROR`                `1 0 0`           `edge`
     9 `WARN\nWARN\nINFO`           `0 2 1`           `normal`
    10 `INFO\nERROR\nINFO\nWARN`    `1 1 2`           `normal`

#### P008 --- Key-Value Parser

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,maintainability,code_quality
-   **Security relevance:** medium
-   **Task:** Parse semicolon-separated key=value pairs; trim
    whitespace; return requested key value or NOT_FOUND.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

  ------------------------------------------------------------------------------------------------------------------------------------------------
                     \# Input                          Expected output                                                            case_type
  --------------------- ------------------------------ -------------------------------------------------------------------------- ----------------
                      1 `a=1;b=2\|a`                   `1`                                                                        `normal`

                      2 `a=1;b=2\|b`                   `2`                                                                        `normal`

                      3 `a = 10 ; b = 20 \|b`          `20`                                                                       `edge`

                      4 `name=John Doe;age=20\|name`   `John Doe`                                                                 `normal`

                      5 `a=1\|x`                       `NOT_FOUND`                                                                `boundary`

                      6 `a=1;a=2\|a`                   `2`                                                                        `edge`

                      7 `x=hello; y = world \| y`      `world`                                                                    `normal`

                      8 `k=\|k`                        \``|`edge`| | 9 |`=v\|`|`v`|`edge`| | 10 |`a=1;b=2;c=3\|c`|`3`|`normal\`   
  ------------------------------------------------------------------------------------------------------------------------------------------------

#### P009 --- Date Format Normalizer

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,maintainability,code_quality
-   **Security relevance:** medium
-   **Task:** Convert valid DD/MM/YYYY to YYYY-MM-DD; invalid dates
    return INVALID.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input          Expected output   case_type
  ---- -------------- ----------------- ------------
     1 `01/01/2025`   `2025-01-01`      `normal`
     2 `31/12/2024`   `2024-12-31`      `normal`
     3 `29/02/2024`   `2024-02-29`      `edge`
     4 `29/02/2023`   `INVALID`         `edge`
     5 `00/01/2025`   `INVALID`         `boundary`
     6 `01/13/2025`   `INVALID`         `boundary`
     7 `9/1/2025`     `INVALID`         `edge`
     8 `30/04/2025`   `2025-04-30`      `normal`
     9 `31/04/2025`   `INVALID`         `edge`
    10 `01/01/2000`   `2000-01-01`      `boundary`

#### P010 --- Word Frequency

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,performance,complexity
-   **Security relevance:** low
-   **Task:** Count case-insensitive words separated by whitespace and
    return the count for requested word.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input                        Expected output   case_type
  ---- ---------------------------- ----------------- ------------
     1 `hello world hello\|hello`   `2`               `normal`
     2 `One one ONE\|one`           `3`               `normal`
     3 `a b c\|z`                   `0`               `normal`
     4 `\|a`                        `0`               `boundary`
     5 `hello\|hello`               `1`               `boundary`
     6 `a a a b b\|b`               `2`               `edge`
     7 `cat dog cat dog\|DOG`       `2`               `edge`
     8 `red   red blue \|red`       `2`               `edge`
     9 `123 123 x\|123`             `2`               `normal`
    10 `Mixed CASE mixed\|mixed`    `2`               `normal`

### Category C --- Input Validation

Boundary validation and defensive input handling.

#### P011 --- Email Validator

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,code_quality
-   **Security relevance:** medium
-   **Task:** Return VALID only for a simple single-address form
    local@domain.tld with no spaces and exactly one @.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input                      Expected output   case_type
  ---- -------------------------- ----------------- ---------------
     1 `user@example.com`         `VALID`           `normal`
     2 `a.b+tag@test.co`          `VALID`           `normal`
     3 `userexample.com`          `INVALID`         `edge`
     4 `user@@example.com`        `INVALID`         `adversarial`
     5 `user@`                    `INVALID`         `edge`
     6 `@example.com`             `INVALID`         `edge`
     7 `user name@example.com`    `INVALID`         `adversarial`
     8 `user@example`             `INVALID`         `edge`
     9 `user@example.c`           `VALID`           `boundary`
    10 `user@example.com extra`   `INVALID`         `adversarial`

#### P012 --- Password Policy Validator

-   **Difficulty:** Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** medium
-   **Task:** Return VALID when length 8-32 and contains upper, lower,
    digit, and special character; otherwise INVALID.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input                                 Expected output   case_type
  ---- ------------------------------------- ----------------- ------------
     1 `Abcd123!`                            `VALID`           `normal`
     2 `abcdefg1!`                           `INVALID`         `normal`
     3 `ABCDEFG1!`                           `INVALID`         `normal`
     4 `Abcdefgh!`                           `INVALID`         `normal`
     5 `Abcd1234`                            `INVALID`         `normal`
     6 `Ab1!`                                `INVALID`         `boundary`
     7 `Abcdef123!`                          `VALID`           `normal`
     8 `Abcdefghijklmnop1234!`               `VALID`           `boundary`
     9 `Abcdefghijklmnop1234567890123456!`   `INVALID`         `boundary`
    10 `Abc123!@`                            `VALID`           `normal`

#### P013 --- Integer Range Validator

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,code_quality
-   **Security relevance:** low
-   **Task:** Return VALID when a decimal integer is within inclusive
    bounds; otherwise INVALID.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input          Expected output   case_type
  ---- -------------- ----------------- ------------
     1 `5\|1\|10`     `VALID`           `normal`
     2 `1\|1\|10`     `VALID`           `boundary`
     3 `10\|1\|10`    `VALID`           `boundary`
     4 `0\|1\|10`     `INVALID`         `boundary`
     5 `11\|1\|10`    `INVALID`         `boundary`
     6 `-5\|-10\|0`   `VALID`           `edge`
     7 `abc\|1\|10`   `INVALID`         `edge`
     8 `5\|10\|1`     `INVALID`         `edge`
     9 `5 \|1\|10`    `VALID`           `edge`
    10 `5\|5\|5`      `VALID`           `boundary`

#### P014 --- IPv4 Validator

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,code_quality
-   **Security relevance:** medium
-   **Task:** Return VALID for dotted IPv4 with four decimal octets
    0-255 and no extra text.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input               Expected output   case_type
  ---- ------------------- ----------------- ---------------
     1 `192.168.1.1`       `VALID`           `normal`
     2 `0.0.0.0`           `VALID`           `boundary`
     3 `255.255.255.255`   `VALID`           `boundary`
     4 `256.1.1.1`         `INVALID`         `edge`
     5 `1.2.3`             `INVALID`         `edge`
     6 `1.2.3.4.5`         `INVALID`         `edge`
     7 `01.2.3.4`          `INVALID`         `edge`
     8 `1.2.3.-1`          `INVALID`         `edge`
     9 `127.0.0.1`         `VALID`           `normal`
    10 `1.1.1.a`           `INVALID`         `adversarial`

#### P015 --- Username Validator

-   **Difficulty:** Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** medium
-   **Task:** Return VALID for 3-20 chars containing only ASCII letters,
    digits, underscore, beginning with a letter.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input                     Expected output   case_type
  ---- ------------------------- ----------------- ------------
     1 `Alice`                   `VALID`           `normal`
     2 `a1`                      `INVALID`         `boundary`
     3 `abc`                     `VALID`           `boundary`
     4 `a_b_1`                   `VALID`           `normal`
     5 `_abc`                    `INVALID`         `edge`
     6 `1abc`                    `INVALID`         `edge`
     7 `abc-def`                 `INVALID`         `edge`
     8 `abcdefghijklmnopqrst`    `VALID`           `boundary`
     9 `abcdefghijklmnopqrstu`   `INVALID`         `boundary`
    10 `A_B_123`                 `VALID`           `normal`

### Category D --- String Sanitization / Output Safety

Output encoding and injection-resistance behavior.

**CWE context:** CWE-79 / CWE-116 where applicable (cross-site scripting
/ improper output encoding). This is contextual research metadata only;
it does not alter the approved security scoring formula.

#### P016 --- HTML Text Escaper

-   **Difficulty:** Easy--Medium
-   **Research focus:**
    reliability,security,maintainability,code_quality
-   **Security relevance:** high
-   **Task:** Escape &, \<, \>, double quote, and single quote into safe
    HTML entities; preserve other text.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input           Expected output               case_type
  ---- --------------- ----------------------------- ---------------
     1 `hello`         `hello`                       `normal`
     2 `a&b`           `a&amp;b`                     `normal`
     3 `<tag>`         `&lt;tag&gt;`                 `adversarial`
     4 `"hello"`       `&quot;hello&quot;`           `adversarial`
     5 `'x'`           `&#x27;x&#x27;`               `adversarial`
     6 `&<>"'`         `&amp;&lt;&gt;&quot;&#x27;`   `adversarial`
     7 `a\nb`          `a\nb`                        `edge`
     8 `5 > 3`         `5 &gt; 3`                    `normal`
     9 `Tom & Jerry`   `Tom &amp; Jerry`             `normal`
    10 `{{name}}`      `{{name}}`                    `edge`

#### P017 --- CSV Cell Escaper

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** medium
-   **Task:** Escape a single CSV cell by quoting when it contains
    comma, quote, or newline; double embedded quotes.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------
                     \# Input            Expected output                                                                                            case_type
  --------------------- ---------------- ---------------------------------------------------------------------------------------------------------- ----------------
                      1 `hello`          `hello`                                                                                                    `normal`

                      2 `a,b`            `"a,b"`                                                                                                    `adversarial`

                      3 `a"b`            `"a""b"`                                                                                                   `adversarial`

                      4 `a\nb`           `"a\nb"`                                                                                                   `adversarial`

                      5 `a,b,c`          `"a,b,c"`                                                                                                  `normal`

                      6 `(empty)`        \``|`boundary`| | 7 |`hello world`|`hello                                                                  
                                         world`|`normal`| | 8 |`a,"b"`|`"a,""b"""`|`edge`| | 9 |`a`\rb`{=tex}`|`"a`\rb`{=tex}"`|`edge`| | 10 |`a;   
                                         b`|`a; b`|`normal\`                                                                                        
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### P018 --- JSON String Escaper

-   **Difficulty:** Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** high
-   **Task:** Return the JSON-safe quoted representation of a string,
    escaping quote, backslash, control characters.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input           Expected output   case_type
  ---- --------------- ----------------- ---------------
     1 `hello`         `"hello"`         `normal`
     2 `a"b`           `"a\"b"`          `adversarial`
     3 `a\b`           `"a\\b"`          `adversarial`
     4 `line\nbreak`   `"line\nbreak"`   `adversarial`
     5 `tab\tend`      `"tab\tend"`      `adversarial`
     6 `(empty)`       `""`              `boundary`
     7 `true`          `"true"`          `normal`
     8 `a\rb`          `"a\rb"`          `edge`
     9 `quote'`        `"quote'"`        `normal`
    10 `<&>`           `"<&>"`           `normal`

#### P019 --- URL Query Component Encoder

-   **Difficulty:** Medium
-   **Research focus:** reliability,security,code_quality
-   **Security relevance:** medium
-   **Task:** Percent-encode all non-unreserved characters in one query
    component using UTF-8.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                     \# Input            Expected output                                                                                                                                                 case_type
  --------------------- ---------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------- ----------------
                      1 `hello`          `hello`                                                                                                                                                         `normal`

                      2 `hello world`    `hello%20world`                                                                                                                                                 `normal`

                      3 `a+b`            `a%2Bb`                                                                                                                                                         `adversarial`

                      4 `a/b`            `a%2Fb`                                                                                                                                                         `adversarial`

                      5 `a?b`            `a%3Fb`                                                                                                                                                         `adversarial`

                      6 `(empty)`        \``|`boundary`| | 7 |`hello-world_123`|`hello-world_123`|`normal`| | 8 |`100%`|`100%25`|`edge`| | 9 |`x=y`|`x%3Dy`|`edge`| | 10 |`a&b`|`a%26b`|`adversarial\`   
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### P020 --- Template Placeholder Sanitizer

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** high
-   **Task:** Replace {{ and }} with escaped literal forms so template
    delimiters cannot be interpreted; leave other text unchanged.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

  ----------------------------------------------------------------------------------------------------------------------------------------------
                     \# Input            Expected output                                                                        case_type
  --------------------- ---------------- -------------------------------------------------------------------------------------- ----------------
                      1 `hello`          `hello`                                                                                `normal`

                      2 `{{name}}`       `\{\{name\}\}`                                                                         `adversarial`

                      3 `a{{b`           `a\{\{b`                                                                               `adversarial`

                      4 `b}}c`           `b\}\}c`                                                                               `adversarial`

                      5 `{{a}}{{b}}`     `\{\{a\}\}\{\{b\}\}`                                                                   `adversarial`

                      6 `(empty)`        \``|`boundary`| | 7 |`a { b`|`a {                                                      
                                         b`|`normal`| | 8 |`x}}`|`x}}`|`edge`| | 9 |`{{`|`{{`|`edge`| | 10 |`}}`|`}}`|`edge\`   
  ----------------------------------------------------------------------------------------------------------------------------------------------

### Category E --- Path / File Safety

Traversal, filename, and allowlist safety.

**CWE context:** CWE-22 / CWE-23 where applicable (path traversal /
relative path traversal). This is contextual research metadata only; it
does not alter the approved security scoring formula.

#### P021 --- Safe Path Normalizer

-   **Difficulty:** Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** high
-   **Task:** Normalize slash-separated path segments; reject traversal
    that escapes the virtual root; return SAFE:`<normalized>`{=html} or
    REJECTED.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input         Expected output   case_type
  ---- ------------- ----------------- ---------------
     1 `a/b/c`       `SAFE:a/b/c`      `normal`
     2 `a/../b`      `SAFE:b`          `edge`
     3 `../x`        `REJECTED`        `adversarial`
     4 `a/../../x`   `REJECTED`        `adversarial`
     5 `/a/b`        `SAFE:a/b`        `edge`
     6 `a//b`        `SAFE:a/b`        `edge`
     7 `./a`         `SAFE:a`          `normal`
     8 `a/./b`       `SAFE:a/b`        `edge`
     9 `(empty)`     `SAFE:`           `boundary`
    10 `../../../`   `REJECTED`        `adversarial`

#### P022 --- Path Extension Validator

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,code_quality
-   **Security relevance:** high
-   **Task:** Return ALLOWED only for a filename with extension .txt or
    .csv and no path separators or traversal tokens.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input            Expected output   case_type
  ---- ---------------- ----------------- ---------------
     1 `report.txt`     `ALLOWED`         `normal`
     2 `data.csv`       `ALLOWED`         `normal`
     3 `REPORT.TXT`     `ALLOWED`         `edge`
     4 `data.CSV`       `ALLOWED`         `edge`
     5 `image.png`      `REJECTED`        `normal`
     6 `../data.txt`    `REJECTED`        `adversarial`
     7 `a/b.txt`        `REJECTED`        `adversarial`
     8 `data.txt.exe`   `REJECTED`        `edge`
     9 `.txt`           `REJECTED`        `edge`
    10 `report`         `REJECTED`        `boundary`

#### P023 --- Filename Sanitizer

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** medium
-   **Task:** Replace path separators and control characters with
    underscore and remove leading/trailing dots; return sanitized
    filename.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

  -----------------------------------------------------------------------------------------------------------------------------------------------
                     \# Input             Expected output                                                                        case_type
  --------------------- ----------------- -------------------------------------------------------------------------------------- ----------------
                      1 `report.txt`      `report.txt`                                                                           `normal`

                      2 `../secret.txt`   `_.._secret.txt`                                                                       `adversarial`

                      3 `a/b.txt`         `a_b.txt`                                                                              `adversarial`

                      4 `..hidden`        `hidden`                                                                               `edge`

                      5 `file.txt`        `file.txt`                                                                             `edge`

                      6 `a\u0000b.txt`    `a_b.txt`                                                                              `adversarial`

                      7 `normal`          `normal`                                                                               `normal`

                      8 `...`             \``|`boundary`| | 9 |`a..b`|`a..b`|`normal`| | 10 |`/tmp/x`|`\_tmp_x`|`adversarial\`   
  -----------------------------------------------------------------------------------------------------------------------------------------------

#### P024 --- Archive Entry Path Checker

-   **Difficulty:** Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** high
-   **Task:** Given an archive entry path, return SAFE if normalized
    path stays within root; otherwise REJECTED.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input              Expected output   case_type
  ---- ------------------ ----------------- ---------------
     1 `images/a.png`     `SAFE`            `normal`
     2 `a/../b.txt`       `SAFE`            `edge`
     3 `../secret.txt`    `REJECTED`        `adversarial`
     4 `a/../../secret`   `REJECTED`        `adversarial`
     5 `a//b`             `SAFE`            `edge`
     6 `./a`              `SAFE`            `normal`
     7 `/root`            `SAFE`            `edge`
     8 `..`               `REJECTED`        `adversarial`
     9 `a/./b`            `SAFE`            `edge`
    10 `(empty)`          `SAFE`            `boundary`

#### P025 --- File Type Allowlist

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,code_quality
-   **Security relevance:** medium
-   **Task:** Return ALLOWED for extensions .png,.jpg,.jpeg,.gif only,
    case-insensitive; reject compound traversal/path input.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input         Expected output   case_type
  ---- ------------- ----------------- ---------------
     1 `a.png`       `ALLOWED`         `normal`
     2 `a.jpg`       `ALLOWED`         `normal`
     3 `a.JPEG`      `ALLOWED`         `edge`
     4 `a.gif`       `ALLOWED`         `normal`
     5 `a.txt`       `REJECTED`        `normal`
     6 `../a.png`    `REJECTED`        `adversarial`
     7 `dir/a.jpg`   `REJECTED`        `adversarial`
     8 `a.png.exe`   `REJECTED`        `edge`
     9 `.png`        `REJECTED`        `edge`
    10 `a`           `REJECTED`        `boundary`

### Category F --- SQL / Query Safety

Query construction and injection-resistant handling without a real
database.

**CWE context:** CWE-89 where applicable (SQL injection). This is
contextual research metadata only; it does not alter the approved
security scoring formula.

#### P026 --- SQL Identifier Validator

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,code_quality
-   **Security relevance:** high
-   **Task:** Return VALID only for identifiers starting with a
    letter/underscore and containing ASCII letters,digits,underscore.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input          Expected output   case_type
  ---- -------------- ----------------- ---------------
     1 `name`         `VALID`           `normal`
     2 `_name`        `VALID`           `normal`
     3 `name1`        `VALID`           `normal`
     4 `1name`        `INVALID`         `edge`
     5 `name-value`   `INVALID`         `adversarial`
     6 `name value`   `INVALID`         `adversarial`
     7 `(empty)`      `INVALID`         `boundary`
     8 `select`       `VALID`           `normal`
     9 `a_b_2`        `VALID`           `normal`
    10 `na.me`        `INVALID`         `edge`

#### P027 --- SQL String Literal Escaper

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** high
-   **Task:** Escape single quotes for use as a SQL string literal by
    doubling them; return the escaped literal content only.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

  --------------------------------------------------------------------------------------------------------------------------------------------------
                     \# Input            Expected output                                                                            case_type
  --------------------- ---------------- ------------------------------------------------------------------------------------------ ----------------
                      1 `hello`          `hello`                                                                                    `normal`

                      2 `O'Reilly`       `O''Reilly`                                                                                `adversarial`

                      3 `''`             `''''`                                                                                     `edge`

                      4 `(empty)`        \``|`boundary`| | 5 |`a'b'c`|`a''b''c`|`adversarial`| | 6 |`plain text`|`plain             
                                         text`|`normal`| | 7 |`'start`|`''start`|`edge`| | 8 |`end'`|`end''`|`edge`| | 9 |`a;DROP   
                                         TABLE users;`|`a;DROP TABLE                                                                
                                         users;`|`adversarial`| | 10 |`Robert');--`|`Robert'');--`|`adversarial\`                   
  --------------------------------------------------------------------------------------------------------------------------------------------------

#### P028 --- Parameterized Query Builder

-   **Difficulty:** Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** high
-   **Task:** Build a fixed SELECT statement using placeholders and
    return query plus ordered parameter values in a specified format.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

  -----------------------------------------------------------------------------------------------------------------------------------
                     \# Input                       Expected output                                                  case_type
  --------------------- --------------------------- ---------------------------------------------------------------- ----------------
                      1 `name=Alice`                `SELECT id,name FROM users WHERE name = ?\|Alice`                `normal`

                      2 `name=Bob`                  `SELECT id,name FROM users WHERE name = ?\|Bob`                  `normal`

                      3 `name=O'Reilly`             `SELECT id,name FROM users WHERE name = ?\|O'Reilly`             `adversarial`

                      4 `name=;DROP TABLE users;`   `SELECT id,name FROM users WHERE name = ?\|;DROP TABLE users;`   `adversarial`

                      5 `name=`                     `SELECT id,name FROM users WHERE name = ?\|`                     `edge`

                      6 `name=Alice Smith`          `SELECT id,name FROM users WHERE name = ?\|Alice Smith`          `normal`

                      7 `name=1 OR 1=1`             `SELECT id,name FROM users WHERE name = ?\|1 OR 1=1`             `adversarial`

                      8 `name='x'`                  `SELECT id,name FROM users WHERE name = ?\|'x'`                  `adversarial`

                      9 `name=😀`                   `SELECT id,name FROM users WHERE name = ?\|😀`                   `edge`

                     10 `name=test`                 `SELECT id,name FROM users WHERE name = ?\|test`                 `normal`
  -----------------------------------------------------------------------------------------------------------------------------------

#### P029 --- Sort Direction Validator

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,code_quality
-   **Security relevance:** medium
-   **Task:** Return ASC or DESC only when input equals asc/desc
    case-insensitively; otherwise INVALID.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input        Expected output   case_type
  ---- ------------ ----------------- ---------------
     1 `asc`        `ASC`             `normal`
     2 `desc`       `DESC`            `normal`
     3 `ASC`        `ASC`             `edge`
     4 `DESC`       `DESC`            `edge`
     5 `Asc`        `ASC`             `edge`
     6 `DeSc`       `DESC`            `edge`
     7 `drop`       `INVALID`         `adversarial`
     8 `asc desc`   `INVALID`         `adversarial`
     9 `(empty)`    `INVALID`         `boundary`
    10 `order`      `INVALID`         `normal`

#### P030 --- Column Allowlist Checker

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** high
-   **Task:** Return ALLOWED only when requested column is in fixed
    allowlist id,name,email,created_at; otherwise REJECTED.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input                   Expected output   case_type
  ---- ----------------------- ----------------- ---------------
     1 `id`                    `ALLOWED`         `normal`
     2 `name`                  `ALLOWED`         `normal`
     3 `email`                 `ALLOWED`         `normal`
     4 `created_at`            `ALLOWED`         `normal`
     5 `password`              `REJECTED`        `adversarial`
     6 `id;DROP TABLE users`   `REJECTED`        `adversarial`
     7 `name`                  `REJECTED`        `edge`
     8 `ID`                    `REJECTED`        `edge`
     9 `(empty)`               `REJECTED`        `boundary`
    10 `created_at DESC`       `REJECTED`        `adversarial`

### Category G --- Command / Shell Safety

Safe command-related string handling without executing commands.

**CWE context:** CWE-78 where applicable (OS command injection). This is
contextual research metadata only; it does not alter the approved
security scoring formula.

#### P031 --- Shell Argument Quoter

-   **Difficulty:** Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** high
-   **Task:** Return a safely single-quoted shell argument, escaping
    embedded single quotes; do not execute commands.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input           Expected output   case_type
  ---- --------------- ----------------- ---------------
     1 `hello`         `'hello'`         `normal`
     2 `hello world`   `'hello world'`   `normal`
     3 `it's`          `'it'\''s'`       `adversarial`
     4 `(empty)`       `''`              `boundary`
     5 `a;b`           `'a;b'`           `adversarial`
     6 `$(whoami)`     `'$(whoami)'`     `adversarial`
     7 `a&&b`          `'a&&b'`          `adversarial`
     8 `a\|b`          `'a\|b'`          `adversarial`
     9 `normal`        `'normal'`        `normal`
    10 `a'b'c`         `'a'\''b'\''c'`   `edge`

#### P032 --- Command Name Allowlist

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,code_quality
-   **Security relevance:** high
-   **Task:** Return ALLOWED only for fixed names status,list,version;
    reject whitespace, separators, or other commands.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input            Expected output   case_type
  ---- ---------------- ----------------- ---------------
     1 `status`         `ALLOWED`         `normal`
     2 `list`           `ALLOWED`         `normal`
     3 `version`        `ALLOWED`         `normal`
     4 `STATUS`         `REJECTED`        `edge`
     5 `rm`             `REJECTED`        `adversarial`
     6 `status;rm`      `REJECTED`        `adversarial`
     7 `status arg`     `REJECTED`        `adversarial`
     8 `(empty)`        `REJECTED`        `boundary`
     9 `list\|whoami`   `REJECTED`        `adversarial`
    10 `version`        `ALLOWED`         `normal`

#### P033 --- Shell Metacharacter Detector

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,code_quality
-   **Security relevance:** high
-   **Task:** Return SAFE if input contains none of shell
    metacharacters; otherwise UNSAFE.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input           Expected output   case_type
  ---- --------------- ----------------- ---------------
     1 `hello`         `SAFE`            `normal`
     2 `hello world`   `SAFE`            `normal`
     3 `a;b`           `UNSAFE`          `adversarial`
     4 `a&&b`          `UNSAFE`          `adversarial`
     5 `$(id)`         `UNSAFE`          `adversarial`
     6 `a\|b`          `UNSAFE`          `adversarial`
     7 `a>file`        `UNSAFE`          `adversarial`
     8 `a*b`           `UNSAFE`          `edge`
     9 `(empty)`       `SAFE`            `boundary`
    10 `normal/path`   `SAFE`            `normal`

#### P034 --- Environment Variable Name Validator

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** medium
-   **Task:** Return VALID for POSIX-style variable names beginning with
    letter/underscore and continuing letters,digits,underscore.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input         Expected output   case_type
  ---- ------------- ----------------- ---------------
     1 `PATH`        `VALID`           `normal`
     2 `_PATH`       `VALID`           `normal`
     3 `path1`       `VALID`           `normal`
     4 `1PATH`       `INVALID`         `edge`
     5 `PATH-NAME`   `INVALID`         `adversarial`
     6 `PATH NAME`   `INVALID`         `adversarial`
     7 `(empty)`     `INVALID`         `boundary`
     8 `_`           `VALID`           `boundary`
     9 `a_b_2`       `VALID`           `normal`
    10 `PATH$`       `INVALID`         `adversarial`

#### P035 --- Command Argument Splitter

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** medium
-   **Task:** Split a simple command argument line on whitespace while
    preserving text inside double quotes; return arguments joined by \|.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input                 Expected output                      case_type
  ---- --------------------- ------------------------------------ ------------
     1 `one two`             `one\|two`                           `normal`
     2 `"one two" three`     `one two\|three`                     `normal`
     3 `a "b c" d`           `a\|b c\|d`                          `edge`
     4 `""`                  `` | `edge` | | 5 | `(empty)` | ``   `boundary`
     6 `"hello world"`       `hello world`                        `normal`
     7 `a b c`               `a\|b\|c`                            `normal`
     8 `"a b" "c d"`         `a b\|c d`                           `edge`
     9 `x "y" z`             `x\|y\|z`                            `normal`
    10 `"quoted text" end`   `quoted text\|end`                   `normal`

### Category H --- Unsafe Deserialization / Configuration Safety

Restricted parsing and configuration safety without dynamic evaluation.

**CWE context:** CWE-502 / CWE-95 where applicable (unsafe
deserialization / dynamic expression evaluation). This is contextual
research metadata only; it does not alter the approved security scoring
formula.

#### P036 --- Safe Literal Parser

-   **Difficulty:** Medium
-   **Research focus:** reliability,security,code_quality
-   **Security relevance:** high
-   **Task:** Accept only a small literal grammar: integer, decimal,
    true, false, null, or quoted string; return TYPE:value.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input       Expected output   case_type
  ---- ----------- ----------------- ---------------
     1 `42`        `INTEGER:42`      `normal`
     2 `-7`        `INTEGER:-7`      `normal`
     3 `3.14`      `DECIMAL:3.14`    `normal`
     4 `true`      `BOOLEAN:true`    `normal`
     5 `false`     `BOOLEAN:false`   `normal`
     6 `null`      `NULL:null`       `boundary`
     7 `"hello"`   `STRING:hello`    `normal`
     8 `hello`     `INVALID`         `adversarial`
     9 `1+2`       `INVALID`         `adversarial`
    10 `""`        `STRING:`         `edge`

#### P037 --- Configuration Boolean Parser

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,maintainability,code_quality
-   **Security relevance:** medium
-   **Task:** Parse true/false/on/off/yes/no case-insensitively; return
    TRUE or FALSE, otherwise INVALID.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input          Expected output   case_type
  ---- -------------- ----------------- ---------------
     1 `true`         `TRUE`            `normal`
     2 `false`        `FALSE`           `normal`
     3 `on`           `TRUE`            `normal`
     4 `off`          `FALSE`           `normal`
     5 `YES`          `TRUE`            `edge`
     6 `No`           `FALSE`           `edge`
     7 `1`            `INVALID`         `adversarial`
     8 `(empty)`      `INVALID`         `boundary`
     9 `true false`   `INVALID`         `adversarial`
    10 `enabled`      `INVALID`         `edge`

#### P038 --- Configuration Key Allowlist

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,code_quality
-   **Security relevance:** high
-   **Task:** Return ALLOWED only for fixed keys
    port,host,timeout,debug; otherwise REJECTED.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input          Expected output   case_type
  ---- -------------- ----------------- ---------------
     1 `port`         `ALLOWED`         `normal`
     2 `host`         `ALLOWED`         `normal`
     3 `timeout`      `ALLOWED`         `normal`
     4 `debug`        `ALLOWED`         `normal`
     5 `password`     `REJECTED`        `adversarial`
     6 `PORT`         `REJECTED`        `edge`
     7 `(empty)`      `REJECTED`        `boundary`
     8 `host.name`    `REJECTED`        `adversarial`
     9 `timeout=10`   `REJECTED`        `adversarial`
    10 `debug`        `ALLOWED`         `normal`

#### P039 --- Structured Token Decoder

-   **Difficulty:** Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** high
-   **Task:** Validate token shape header.payload.signature with exactly
    3 non-empty URL-safe base64-like parts; return VALID/INVALID.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input           Expected output   case_type
  ---- --------------- ----------------- ---------------
     1 `abc.def.ghi`   `VALID`           `normal`
     2 `a.b.c`         `VALID`           `boundary`
     3 `(empty)`       `INVALID`         `boundary`
     4 `a.b`           `INVALID`         `edge`
     5 `a..c`          `INVALID`         `edge`
     6 `a.b.c.d`       `INVALID`         `edge`
     7 `a+b.c`         `INVALID`         `adversarial`
     8 `a_b.c-d`       `VALID`           `normal`
     9 `.b.c`          `INVALID`         `edge`
    10 `a.b.`          `INVALID`         `edge`

#### P040 --- Safe Numeric Expression Validator

-   **Difficulty:** Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** high
-   **Task:** Return VALID only for digits, spaces, parentheses, and
    +-\* / operators with no letters, quotes, or other characters.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input       Expected output   case_type
  ---- ----------- ----------------- ---------------
     1 `1+2`       `VALID`           `normal`
     2 `(1+2)*3`   `VALID`           `normal`
     3 `1/0`       `VALID`           `edge`
     4 `(empty)`   `INVALID`         `boundary`
     5 `a+1`       `INVALID`         `adversarial`
     6 `1;2`       `INVALID`         `adversarial`
     7 `1  +  2`   `VALID`           `edge`
     8 `(1+2`      `VALID`           `edge`
     9 `1_000`     `INVALID`         `edge`
    10 `2*(3+4)`   `VALID`           `normal`

### Category I --- Resource / Performance Safety

Algorithmic efficiency, resource handling, and large-input behavior.

#### P041 --- Frequency Counter Large Input

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,performance,complexity
-   **Security relevance:** low
-   **Task:** Count occurrences of requested integer in a
    space-separated integer list.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input              Expected output   case_type
  ---- ------------------ ----------------- ------------
     1 `1 2 3 2 2\|2`     `3`               `normal`
     2 `1 1 1\|1`         `3`               `normal`
     3 `5\|5`             `1`               `boundary`
     4 `5\|1`             `0`               `boundary`
     5 `-1 -1 2\|-1`      `2`               `edge`
     6 `0 0 0\|0`         `3`               `edge`
     7 `1 2 3 4 5\|6`     `0`               `normal`
     8 `10 10 9 10\|10`   `3`               `normal`
     9 `2 2 2 2 2\|2`     `5`               `stress`
    10 `7 8 9\|7`         `1`               `normal`

#### P042 --- Duplicate Detector

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,performance,complexity
-   **Security relevance:** low
-   **Task:** Return DUPLICATE if any integer repeats; otherwise UNIQUE.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input           Expected output   case_type
  ---- --------------- ----------------- ------------
     1 `1 2 3`         `UNIQUE`          `normal`
     2 `1 2 1`         `DUPLICATE`       `normal`
     3 `1`             `UNIQUE`          `boundary`
     4 `(empty)`       `UNIQUE`          `boundary`
     5 `0 0`           `DUPLICATE`       `edge`
     6 `-1 0 1`        `UNIQUE`          `edge`
     7 `5 4 3 2 1`     `UNIQUE`          `normal`
     8 `1 2 3 3 4`     `DUPLICATE`       `edge`
     9 `10 20 30 40`   `UNIQUE`          `normal`
    10 `9 8 7 9`       `DUPLICATE`       `normal`

#### P043 --- Streaming Sum

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,performance,maintainability
-   **Security relevance:** low
-   **Task:** Sum a newline-separated sequence of integers; return the
    exact integer sum.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input            Expected output   case_type
  ---- ---------------- ----------------- ------------
     1 `1\n2\n3`        `6`               `normal`
     2 `(empty)`        `0`               `boundary`
     3 `-1\n1`          `0`               `edge`
     4 `5`              `5`               `boundary`
     5 `10\n20\n30`     `60`              `normal`
     6 `0\n0\n0`        `0`               `edge`
     7 `-5\n-10`        `-15`             `normal`
     8 `100\n-50\n25`   `75`              `normal`
     9 `7\n8\n9\n10`    `34`              `normal`
    10 `1\n-1\n1\n-1`   `0`               `edge`

#### P044 --- Bounded Log Processor

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,performance,maintainability
-   **Security relevance:** medium
-   **Task:** Count lines containing ERROR, WARN, INFO and ignore other
    levels; return three counts.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input                        Expected output   case_type
  ---- ---------------------------- ----------------- ------------
     1 `ERROR\nWARN\nINFO`          `1 1 1`           `normal`
     2 `ERROR\nERROR\nERROR`        `3 0 0`           `normal`
     3 `INFO\nINFO`                 `0 0 2`           `normal`
     4 `WARN\nWARN`                 `0 2 0`           `normal`
     5 `DEBUG\nTRACE`               `0 0 0`           `edge`
     6 `ERROR x\nWARN x\nINFO x`    `1 1 1`           `edge`
     7 `(empty)`                    `0 0 0`           `boundary`
     8 `ERROR\nDEBUG\nERROR`        `2 0 0`           `normal`
     9 `WARN\nINFO\nWARN\nINFO`     `0 2 2`           `normal`
    10 `INFO\nERROR\nWARN\nOTHER`   `1 1 1`           `edge`

#### P045 --- Top-K Frequent Values

-   **Difficulty:** Medium
-   **Research focus:** reliability,performance,complexity
-   **Security relevance:** medium
-   **Task:** Return up to k most frequent integers, ties resolved by
    smaller value first, joined by commas.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

  -------------------------------------------------------------------------------------------
                     \# Input              Expected output                   case_type
  --------------------- ------------------ --------------------------------- ----------------
                      1 `1 1 2 2 2 3\|2`   `2,1`                             `normal`

                      2 `1 2 3\|2`         `1,2`                             `edge`

                      3 `5\|1`             `5`                               `boundary`

                      4 `1 1 2\|0`         \``|`boundary`| | 5 |`3 3 2 2     
                                           1\|3`|`2,3`|`edge`| | 6 |`4 4 4 1 
                                           1 2\|2`|`4,1`|`normal`| | 7 |`-1  
                                           -1 0 0 0\|1`|`0`|`edge`| | 8 |`7  
                                           8 7 8                             
                                           9\|3`|`7,8,9`|`normal`| | 9 |`1 2 
                                           2 3 3                             
                                           3\|2`|`3,2`|`normal`| | 10 |`1 1  
                                           2 2\|2`|`1,2`|`edge\`             
  -------------------------------------------------------------------------------------------

### Category J --- Authentication / Token / Authorization Validation

Deterministic authentication/authorization rule handling without real
credentials.

**CWE context:** CWE-287 / CWE-863 where applicable (authentication /
authorization failures). This is contextual research metadata only; it
does not alter the approved security scoring formula.

#### P046 --- Token Format Validator

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** high
-   **Task:** Validate a token as exactly three dot-separated non-empty
    URL-safe segments; return VALID/INVALID.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input           Expected output   case_type
  ---- --------------- ----------------- ---------------
     1 `abc.def.ghi`   `VALID`           `normal`
     2 `a.b.c`         `VALID`           `boundary`
     3 `a.b`           `INVALID`         `edge`
     4 `a..c`          `INVALID`         `edge`
     5 `(empty)`       `INVALID`         `boundary`
     6 `a+b.c`         `INVALID`         `adversarial`
     7 `a_b.c-d`       `VALID`           `normal`
     8 `.a.b`          `INVALID`         `edge`
     9 `a.b.`          `INVALID`         `edge`
    10 `a.b.c.d`       `INVALID`         `edge`

#### P047 --- Permission Rule Evaluator

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** high
-   **Task:** Given role and action, return ALLOW only for fixed
    role-action pairs; otherwise DENY.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input              Expected output   case_type
  ---- ------------------ ----------------- ---------------
     1 `admin\|read`      `ALLOW`           `normal`
     2 `admin\|write`     `ALLOW`           `normal`
     3 `admin\|delete`    `ALLOW`           `normal`
     4 `user\|read`       `ALLOW`           `normal`
     5 `user\|write`      `DENY`            `normal`
     6 `guest\|read`      `ALLOW`           `edge`
     7 `guest\|delete`    `DENY`            `adversarial`
     8 `root\|delete`     `DENY`            `adversarial`
     9 `admin\|unknown`   `DENY`            `edge`
    10 `guest\|write`     `DENY`            `normal`

#### P048 --- Role Permission Checker

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,code_quality
-   **Security relevance:** medium
-   **Task:** Given role and permission, return YES if permission is in
    that role's fixed set; otherwise NO.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input             Expected output   case_type
  ---- ----------------- ----------------- ------------
     1 `admin\|read`     `YES`             `normal`
     2 `admin\|write`    `YES`             `normal`
     3 `admin\|delete`   `YES`             `normal`
     4 `user\|read`      `YES`             `normal`
     5 `user\|write`     `NO`              `normal`
     6 `user\|delete`    `NO`              `normal`
     7 `guest\|read`     `YES`             `edge`
     8 `guest\|write`    `NO`              `normal`
     9 `guest\|delete`   `NO`              `normal`
    10 `unknown\|read`   `NO`              `boundary`

#### P049 --- Session Timeout Checker

-   **Difficulty:** Easy--Medium
-   **Research focus:** reliability,security,code_quality
-   **Security relevance:** medium
-   **Task:** Given last activity and current minute plus timeout,
    return ACTIVE when elapsed \<= timeout, else EXPIRED.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input            Expected output   case_type
  ---- ---------------- ----------------- ------------
     1 `100\|110\|15`   `ACTIVE`          `normal`
     2 `100\|115\|15`   `ACTIVE`          `boundary`
     3 `100\|116\|15`   `EXPIRED`         `boundary`
     4 `0\|0\|0`        `ACTIVE`          `boundary`
     5 `50\|49\|10`     `ACTIVE`          `edge`
     6 `50\|70\|10`     `EXPIRED`         `normal`
     7 `100\|101\|1`    `ACTIVE`          `boundary`
     8 `100\|102\|1`    `EXPIRED`         `boundary`
     9 `100\|100\|30`   `ACTIVE`          `normal`
    10 `100\|131\|30`   `EXPIRED`         `boundary`

#### P050 --- Access Scope Validator

-   **Difficulty:** Medium
-   **Research focus:** reliability,security,maintainability
-   **Security relevance:** high
-   **Task:** Return ALLOWED only when requested scope is in fixed
    read/write/delete allowlist for the supplied role.
-   **Supported languages:** Python, Java
-   **Dependencies:** Standard library only; no network or external
    service.

    \# Input             Expected output   case_type
  ---- ----------------- ----------------- ---------------
     1 `admin\|read`     `ALLOWED`         `normal`
     2 `admin\|write`    `ALLOWED`         `normal`
     3 `admin\|delete`   `ALLOWED`         `normal`
     4 `user\|read`      `ALLOWED`         `normal`
     5 `user\|write`     `ALLOWED`         `normal`
     6 `user\|delete`    `REJECTED`        `adversarial`
     7 `guest\|read`     `ALLOWED`         `edge`
     8 `guest\|write`    `REJECTED`        `normal`
     9 `guest\|delete`   `REJECTED`        `adversarial`
    10 `unknown\|read`   `REJECTED`        `boundary`

## 7. Research controls

1.  Freeze this benchmark before main AI/human data collection.
2.  Give every AI model the same approved problem statement and
    contract.
3.  Keep the human baseline fixed for the same problem/language unless a
    documented benchmark or baseline version is created.
4.  Do not expose hidden expected outputs to AI models.
5.  Use the same execution environment, timeout, language version,
    analysis tools, and scoring configuration.
6.  Record AI system name/source and the model/version/date where the
    research workflow captures them.
7.  Keep pilot/software-validation submissions separate from final
    research observations.
8.  Preserve raw measurements and analysis-tool versions for
    reproducibility.
9.  Never fabricate missing tool findings, test results, execution
    measurements, or statistical results.
10. Interpret results from the paired dataset, not from an individual
    problem.

## 8. Security benchmark rules

Security problems are deliberately safe research exercises. They use
attacker-like strings and deterministic policy decisions without
actually executing attacks.

-   No problem requires a real SQL server.
-   No problem requires a real shell.
-   No problem requires a real filesystem mutation.
-   No problem requires network access.
-   No real passwords, tokens, or credentials are used.
-   No attacker-controlled command is executed.
-   Security relevance is metadata; static security findings remain the
    approved security measurement.

## 9. Implementation instructions for the coding agent

When this approved benchmark is supplied to the coding agent, it becomes
the authoritative definition of the 50 problems.

The agent must:

-   Replace the current 6-problem seed/bank with P001--P050.
-   Seed exactly 50 problems and exactly 500 predefined test cases.
-   Preserve every problem ID, title, task meaning, research-focus tag,
    security relevance, input, expected output, and `case_type` exactly.
-   Support Python and Java for all 50 problems using the existing
    evaluator contract.
-   Preserve the existing six metrics, scoring weights, database
    architecture, workflow, and reporting methodology.
-   Version the benchmark/test cases so research observations remain
    reproducible.
-   Validate that the new bank is compatible with the existing database
    and execution engine before enabling research collection.
-   Handle old research records safely; do not silently fabricate,
    overwrite, or delete research data.
-   Do not invent additional problems or replace difficult security
    cases with generic problems.
-   Do not weaken or remove adversarial cases because a generated
    solution fails them.
-   Do not add AI APIs, network dependencies, production databases, real
    credentials, destructive actions, or arbitrary command execution.
-   Run the relevant backend tests, frontend tests, production build,
    seed/migration checks, and representative Python/Java comparisons.
-   Update the audit/reporting documentation with the exact files
    changed and exact test results.

## 10. Acceptance checklist

-   [ ] P001--P050 exist exactly once.
-   [ ] 50 problems are present.
-   [ ] 500 test cases are present.
-   [ ] Every problem has 10 tests.
-   [ ] Every problem has at least one boundary and one edge test.
-   [ ] All test inputs/outputs are deterministic.
-   [ ] All 50 problems support Python and Java.
-   [ ] No problem needs network, credentials, destructive actions, or
    arbitrary commands.
-   [ ] Security problems remain security-focused and use contextual CWE
    mappings where appropriate.
-   [ ] Existing six-dimensional scoring remains unchanged.
-   [ ] Pilot and research data remain distinguishable.
-   [ ] Existing exports/reports continue to expose the
    benchmark/problem version.
-   [ ] Exact automated test results are recorded.

## 11. Research validity notes

This benchmark expands the current bank so that security-focused
behavior is represented rather than relying only on classic algorithms.
It does not, by itself, establish universal conclusions about
AI-generated code.

Functional tests measure tested behavior only. Static security analyzers
can have false positives and false negatives. A single human baseline
does not measure human-to-human variation. Maintainability should
continue to rely on the existing multi-metric approach rather than one
subjective or single-metric judgment.

## 12. Approval status

**NOT YET FROZEN.** This document should be reviewed once before it is
handed to the coding agent. After approval, the next artifact should be
the implementation prompt that tells the agent exactly how to replace
the current 6-problem bank with this benchmark.

**End of Benchmark v1.0**
