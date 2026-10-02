# AI Code Generation Specification

## Purpose

This document standardizes AI-generated code for the Research Code Evaluator benchmark. It is aligned to the project source of truth: the predefined benchmark in `config/problems.yaml`, the execution contract in `backend/api/comparisons.py`, and the language execution harness in `backend/engine/executor.py`.

The application compares AI-generated and human-written code across 50 predefined problems and four supported languages: Python, Java, C++, and JavaScript.

## Source of Truth

- Benchmark file: `config/problems.yaml`
- Database seed and benchmark loader: `backend/db/seed.py`
- Execution system: `backend/engine/executor.py`
- Typed harness contract: `backend/api/comparisons.py`
- Scoring and evaluation: `config/scoring.yaml`, `backend/scoring/scoring.py`, `backend/analysis/analyzer.py`
- Research methodology: `docs/01_RESEARCH_METHODOLOGY.md`, `docs/02_EXPERIMENT_WORKFLOW.md`, `docs/03_METRICS_AND_SCORING.md`

## Scope

- Exactly 50 benchmark problems.
- Exactly four supported languages: Python, Java, C++, JavaScript.
- Five AI models will generate one submission per problem per language, for a total of 1,000 planned AI-generated submissions.
- No benchmark data, test cases, problem requirements, or execution rules may be changed.

## Supported Languages and Execution Conventions

The project executes each submission through the typed harness used by the application. The generation target must therefore follow the exact function names and signatures declared in the benchmark, even when the solution is otherwise a conventional algorithmic implementation.

### Python
- Required function name comes from the benchmark signature and must be preserved exactly.
- No `input()`, `print()`, or `main()` block.
- The harness calls the function directly with the provided input object or scalar.
- Return the value required by the problem specification.

### Java
- Provide a complete Java source file with `public class Solution` and the required static method.
- Preserve the exact required method name and parameter types.
- Do not add `main()`, `Scanner`, or `System.in` reads.
- Return the required Java type from the method.
- Do not submit only a bare method fragment without the class wrapper.

### C++
- Preserve the exact function name and parameter types.
- Do not add a `main()` function.
- Use standard library types where required by the benchmark signature.
- Return the required primitive, vector, map, or string result.

### JavaScript
- Preserve the exact function name and parameter list.
- Do not use `process.stdin`, `readline`, or interactive I/O.
- Export the function in the supported `module.exports` form required by the harness.

## Global Generation Rules

1. Implement only the required solution for the specified problem.
2. Use exactly the function or method name provided by the benchmark for that language.
3. Preserve the exact signature, parameter types, and return type as defined in the benchmark.
4. Do not include analysis, comments, markdown, code fences, sample inputs, unit tests, or explanations.
5. Do not add helper programs, wrappers, custom drivers, or extra classes unrelated to the required solution.
6. Do not use interactive input or output mechanisms.
7. Do not modify the benchmark, problem IDs, expected outputs, or constraints.
8. Do not optimize for model-specific behavior or for a research metric. Produce the correct solution for the problem itself.
9. Do not include any text before or after the generated code.
10. Return code that is directly executable by the existing Research Code Evaluator harness.

## Standardized Prompt for Any AI Model

> You are generating code for an empirical software engineering research study.
>
> Implement the specified programming problem using the exact function signature and requirements provided.
>
> Return only the required implementation for the selected language. Do not include explanations, markdown, comments, test cases, sample I/O, or extra code.
>
> Do not change the function signature, problem requirements, constraints, or expected behavior.
>
> Use the same problem specification and constraints as every other model in this study.
>
> Produce a correct, executable implementation that follows the language-specific execution system requirements.
>
> Do not intentionally introduce bugs, security vulnerabilities, inefficient algorithms, or artificial limitations.
>
> Do not optimize for a particular research metric. Write the solution you would normally provide for the stated problem.

## Dataset Organization

Use a model-first, problem-second, language-third directory structure to keep the generated dataset auditable and consistent.

```text
AI_GENERATED_CODE/
  MODEL_1/
    P001/
      python.py
      java.java
      cpp.cpp
      javascript.js
    P002/
      python.py
      java.java
      cpp.cpp
      javascript.js
    ...
  MODEL_2/
    P001/
      python.py
      java.java
      cpp.cpp
      javascript.js
  MODEL_3/
  MODEL_4/
  MODEL_5/
```

Naming convention:
- `MODEL_X` is a placeholder for one of the five AI models used in the study.
- `P###` matches the benchmark ID in `config/problems.yaml`.
- File names use the language key: `python.py`, `java.java`, `cpp.cpp`, `javascript.js`.
- The mapping is one submission per model, per problem, per language, resulting in 1,000 planned AI submissions.

## Quality and Consistency Checklist

- [ ] Correct problem ID and title.
- [ ] Correct programming language file.
- [ ] Correct function name and signature.
- [ ] Correct parameter types and return type.
- [ ] No `main()` or interactive I/O unless explicitly required by the project contract.
- [ ] No unnecessary helper functions or comments.
- [ ] No markdown, code fences, or explanations outside the raw code.
- [ ] Compatible with the existing execution harness.
- [ ] Valid syntax for the target language.
- [ ] Matches the benchmark behavior and expected output format.
- [ ] No accidental benchmark modification or requirement drift.

## Problem-by-Problem Generation Specification

--------------------------------------------------
Problem ID: P001
Problem Title: Two Sum
--------------------------------------------------

**Problem Description:**
Given an array of integers `nums` and an integer `target`, return the
indices of the two numbers that add up to `target`.
You may assume that each input has exactly one solution, and you may
not use the same element twice.
Return the two indices in any order.

**Required Behavior:**
- Output contract: JSON array of two indices, e.g. [0,1] (sorted ascending)
- Constraints: 2 <= nums.length <= 10^4 | -10^9 <= nums[i] <= 10^9 | Exactly one solution exists
- Input contract: JSON object {"nums": [...], "target": N}

**Input Parameters:**
JSON object {"nums": [...], "target": N}

**Expected Return Type:**
JSON array of two indices, e.g. [0,1] (sorted ascending)

**Constraints and Edge Cases:**
2 <= nums.length <= 10^4 | -10^9 <= nums[i] <= 10^9 | Exactly one solution exists

### Python
**Required signature:**
def two_sum(nums: list[int], target: int) -> list[int]:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static int[] twoSum(int[] nums, int target)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
vector<int> twoSum(vector<int>& nums, int target)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function twoSum(nums, target)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P002
Problem Title: Maximum Subarray Sum
--------------------------------------------------

**Problem Description:**
Given an integer array `nums`, find the contiguous subarray (containing
at least one number) which has the largest sum and return its sum.
(Classic Kadane's algorithm problem.)

**Required Behavior:**
- Output contract: Integer: maximum subarray sum
- Constraints: 1 <= nums.length <= 10^5 | -10^4 <= nums[i] <= 10^4
- Input contract: JSON object {"nums": [...]}

**Input Parameters:**
JSON object {"nums": [...]}

**Expected Return Type:**
Integer: maximum subarray sum

**Constraints and Edge Cases:**
1 <= nums.length <= 10^5 | -10^4 <= nums[i] <= 10^4

### Python
**Required signature:**
def max_subarray(nums: list[int]) -> int:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static int maxSubarray(int[] nums)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
int maxSubarray(vector<int>& nums)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function maxSubarray(nums)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P003
Problem Title: Binary Search
--------------------------------------------------

**Problem Description:**
Given a sorted array of distinct integers `nums` and a `target` value,
return the index of `target` if it exists, or `-1` if it does not.
Your implementation must run in O(log n) time.

**Required Behavior:**
- Output contract: Integer index of target, or -1 if not found
- Constraints: 1 <= nums.length <= 10^4 | All nums[i] are distinct | Array is sorted ascending
- Input contract: JSON object {"nums": [...sorted...], "target": N}

**Input Parameters:**
JSON object {"nums": [...sorted...], "target": N}

**Expected Return Type:**
Integer index of target, or -1 if not found

**Constraints and Edge Cases:**
1 <= nums.length <= 10^4 | All nums[i] are distinct | Array is sorted ascending

### Python
**Required signature:**
def binary_search(nums: list[int], target: int) -> int:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static int binarySearch(int[] nums, int target)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
int binarySearch(vector<int>& nums, int target)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function binarySearch(nums, target)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P004
Problem Title: Merge Sorted Arrays
--------------------------------------------------

**Problem Description:**
Given two sorted integer arrays `nums1` and `nums2`, merge them into
a single sorted array and return it.
The returned array should contain all elements from both arrays in
non-decreasing order.

**Required Behavior:**
- Output contract: JSON array of merged sorted integers
- Constraints: 0 <= nums1.length, nums2.length <= 200 | -10^9 <= nums[i] <= 10^9 | Both arrays are sorted
- Input contract: JSON object {"nums1": [...], "nums2": [...]}

**Input Parameters:**
JSON object {"nums1": [...], "nums2": [...]}

**Expected Return Type:**
JSON array of merged sorted integers

**Constraints and Edge Cases:**
0 <= nums1.length, nums2.length <= 200 | -10^9 <= nums[i] <= 10^9 | Both arrays are sorted

### Python
**Required signature:**
def merge_sorted_arrays(nums1: list[int], nums2: list[int]) -> list[int]:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static int[] mergeSortedArrays(int[] nums1, int[] nums2)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
vector<int> mergeSortedArrays(vector<int>& nums1, vector<int>& nums2)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function mergeSortedArrays(nums1, nums2)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P005
Problem Title: Balanced Brackets
--------------------------------------------------

**Problem Description:**
Given a string `s` containing only the characters `(`, `)`, `{`, `}`,
`[`, and `]`, determine if the input string is valid.
A string is valid if:
  - Every open bracket is closed by the same type of bracket.
  - Open brackets are closed in the correct order.
  - Every close bracket has a corresponding open bracket.
Return `true` if valid, `false` otherwise.

**Required Behavior:**
- Output contract: "true" or "false"
- Constraints: 1 <= s.length <= 10^4 | s consists only of '()[]{}'
- Input contract: JSON object {"s": "<bracket string>"}

**Input Parameters:**
JSON object {"s": "<bracket string>"}

**Expected Return Type:**
"true" or "false"

**Constraints and Edge Cases:**
1 <= s.length <= 10^4 | s consists only of '()[]{}'

### Python
**Required signature:**
def is_balanced(s: str) -> bool:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static boolean isBalanced(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
bool isBalanced(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function isBalanced(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P006
Problem Title: CSV Record Field Count
--------------------------------------------------

**Problem Description:**
Given a single CSV line (a string), count the number of fields.
Fields are separated by commas. A field may be enclosed in double
quotes, in which case it may contain commas and escaped quotes (`""`).
Return the integer count of fields.

**Required Behavior:**
- Output contract: Integer: number of fields in the CSV line
- Constraints: 0 <= line.length <= 10^4 | Standard CSV quoting rules apply
- Input contract: JSON object {"line": "<csv line>"}

**Input Parameters:**
JSON object {"line": "<csv line>"}

**Expected Return Type:**
Integer: number of fields in the CSV line

**Constraints and Edge Cases:**
0 <= line.length <= 10^4 | Standard CSV quoting rules apply

### Python
**Required signature:**
def csv_field_count(line: str) -> int:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static int csvFieldCount(String line)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
int csvFieldCount(const string& line)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function csvFieldCount(line)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P007
Problem Title: Log Level Counter
--------------------------------------------------

**Problem Description:**
Given a multiline log string where each line begins with a log level
tag (ERROR, WARNING, INFO, or DEBUG), count the occurrences of each
level and return a dictionary/map with keys ERROR, WARNING, INFO, DEBUG.
Lines that do not match a known level are ignored.
Return a dict with all four keys present (use 0 for absent levels).

**Required Behavior:**
- Output contract: JSON object {"ERROR":N,"WARNING":N,"INFO":N,"DEBUG":N}
- Constraints: Each line starts with ERROR/WARNING/INFO/DEBUG followed by a space or colon | 0 <= lines <= 10^4
- Input contract: JSON object {"log": "<multiline log string>"}

**Input Parameters:**
JSON object {"log": "<multiline log string>"}

**Expected Return Type:**
JSON object {"ERROR":N,"WARNING":N,"INFO":N,"DEBUG":N}

**Constraints and Edge Cases:**
Each line starts with ERROR/WARNING/INFO/DEBUG followed by a space or colon | 0 <= lines <= 10^4

### Python
**Required signature:**
def count_log_levels(log: str) -> dict:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static Map<String,Integer> countLogLevels(String log)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
map<string,int> countLogLevels(const string& log)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function countLogLevels(log)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P008
Problem Title: Key-Value Parser
--------------------------------------------------

**Problem Description:**
Given a string `s` containing comma-separated key=value pairs, parse it
into a dictionary/map and return it.
Keys and values are separated by `=`. Pairs are separated by `,`.
Keys and values may contain spaces (stripped) but will not contain `=` or `,`.
Return the resulting mapping.

**Required Behavior:**
- Output contract: JSON object with string keys and string values, sorted by key
- Constraints: 0 <= pairs <= 100 | Keys are unique | No = or , in key/value text
- Input contract: JSON object {"s": "key1=val1,key2=val2,..."}

**Input Parameters:**
JSON object {"s": "key1=val1,key2=val2,..."}

**Expected Return Type:**
JSON object with string keys and string values, sorted by key

**Constraints and Edge Cases:**
0 <= pairs <= 100 | Keys are unique | No = or , in key/value text

### Python
**Required signature:**
def parse_key_value(s: str) -> dict:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static Map<String,String> parseKeyValue(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
map<string,string> parseKeyValue(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function parseKeyValue(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P009
Problem Title: Date Format Normalizer
--------------------------------------------------

**Problem Description:**
Given a date string in one of the following formats:
  - MM/DD/YYYY  (e.g. 01/15/2023)
  - DD-MM-YYYY  (e.g. 15-01-2023)
  - YYYY.MM.DD  (e.g. 2023.01.15)
Return the date in ISO 8601 format: YYYY-MM-DD.
You may assume the input is always a valid date in one of the three formats.

**Required Behavior:**
- Output contract: ISO date string YYYY-MM-DD
- Constraints: Input is always a valid date in one of the three listed formats
- Input contract: JSON object {"date": "<date string>"}

**Input Parameters:**
JSON object {"date": "<date string>"}

**Expected Return Type:**
ISO date string YYYY-MM-DD

**Constraints and Edge Cases:**
Input is always a valid date in one of the three listed formats

### Python
**Required signature:**
def normalize_date(date: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String normalizeDate(String date)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string normalizeDate(const string& date)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function normalizeDate(date)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P010
Problem Title: Word Frequency
--------------------------------------------------

**Problem Description:**
Given a string `text`, count the frequency of each word.
Words are sequences of alphabetic characters only (ignore punctuation).
Comparison is case-insensitive; return lowercase words.
Return the result as a list of [word, count] pairs sorted by count
descending, then alphabetically ascending for ties.

**Required Behavior:**
- Output contract: JSON array of [word, count] pairs, sorted by count desc then alpha asc
- Constraints: 0 <= text.length <= 10^4 | Only ASCII text
- Input contract: JSON object {"text": "<text string>"}
- Implementation contract: the function may return a dictionary/map/object keyed by word, but the evaluator serializes it to the canonical JSON array form shown above.

**Input Parameters:**
JSON object {"text": "<text string>"}

**Expected Return Type:**
JSON array of [word, count] pairs, sorted by count desc then alpha asc

**Constraints and Edge Cases:**
0 <= text.length <= 10^4 | Only ASCII text

### Python
**Required signature:**
def word_frequency(text: str) -> dict:

**Implementation note:** Return a dictionary-like mapping of word -> count; the harness converts it into the canonical ordered list-of-pairs output expected by the benchmark.

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static Map<String,Integer> wordFrequency(String text)

**Required output:** Provide the complete `public class Solution` with the required method; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation note:** Return a `Map<String,Integer>` keyed by lowercase words; the evaluator serializes it into the canonical ordered list-of-pairs output.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
vector<pair<string,int>> wordFrequency(const string& text)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation note:** Return a vector of pairs sorted by count descending and then word ascending; the benchmark's harness compares the canonical serialized output.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function wordFrequency(text)

**Required output:** Implement the function and export it in the harness-compatible `module.exports` form. Do not add interactive I/O, extra explanation, or non-essential code.

**Implementation note:** Return an object mapping lowercase word -> count; the evaluator serializes it into the canonical ordered list-of-pairs output.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P011
Problem Title: Email Validator
--------------------------------------------------

**Problem Description:**
Given an email address string, determine whether it is valid.
Validation rules:
  - Must contain exactly one @ symbol
  - Local part (before @): 1+ chars, only [a-zA-Z0-9._%+-], no leading/trailing dot, no consecutive dots
  - Domain part (after @): dot-separated labels, no leading/trailing dot or hyphen per label
  - TLD (last label): 2-6 alphabetic characters only
Return true if valid, false otherwise.

**Required Behavior:**
- Output contract: "true" or "false"
- Constraints: Defined validation rules apply — see description
- Input contract: JSON object {"input": "<email string>"}

**Input Parameters:**
JSON object {"input": "<email string>"}

**Expected Return Type:**
"true" or "false"

**Constraints and Edge Cases:**
Defined validation rules apply — see description

### Python
**Required signature:**
def is_valid_email(email: str) -> bool:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static boolean isValidEmail(String email)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
bool isValidEmail(const string& email)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function isValidEmail(email)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P012
Problem Title: Password Policy Validator
--------------------------------------------------

**Problem Description:**
Given a password string, determine whether it satisfies the following policy:
  - Minimum 8 characters
  - At least 1 uppercase letter (A-Z)
  - At least 1 lowercase letter (a-z)
  - At least 1 digit (0-9)
  - At least 1 special character from the set: !@#$%^&*
Return true if all rules pass, false otherwise.

**Required Behavior:**
- Output contract: "true" or "false"
- Constraints: All 5 rules must pass simultaneously
- Input contract: JSON object {"input": "<password string>"}

**Input Parameters:**
JSON object {"input": "<password string>"}

**Expected Return Type:**
"true" or "false"

**Constraints and Edge Cases:**
All 5 rules must pass simultaneously

### Python
**Required signature:**
def is_valid_password(password: str) -> bool:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static boolean isValidPassword(String password)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
bool isValidPassword(const string& pw)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function isValidPassword(password)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P013
Problem Title: Integer Range Validator
--------------------------------------------------

**Problem Description:**
Given a string in the format "value|min|max" (pipe-separated integers),
determine whether value is within the inclusive range [min, max].
Return "VALID" if min <= value <= max, otherwise "INVALID".
Return "INVALID" if the input is malformed (non-integer, wrong number of parts).

**Required Behavior:**
- Output contract: "VALID" or "INVALID"
- Constraints: All three parts must be parseable as integers
- Input contract: JSON object {"input": "value|min|max"}

**Input Parameters:**
JSON object {"input": "value|min|max"}

**Expected Return Type:**
"VALID" or "INVALID"

**Constraints and Edge Cases:**
All three parts must be parseable as integers

### Python
**Required signature:**
def is_valid_range(s: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String isValidRange(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string isValidRange(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function isValidRange(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P014
Problem Title: IPv4 Validator
--------------------------------------------------

**Problem Description:**
Given a string, determine whether it is a valid IPv4 address.
Rules:
  - Exactly 4 octets separated by dots
  - Each octet is an integer in [0, 255]
  - No leading zeros (e.g. "01" is invalid; "0" is valid)
  - No extra characters
Return true if valid, false otherwise.

**Required Behavior:**
- Output contract: "true" or "false"
- Constraints: No leading zeros; octets must be 0-255
- Input contract: JSON object {"input": "<ip string>"}

**Input Parameters:**
JSON object {"input": "<ip string>"}

**Expected Return Type:**
"true" or "false"

**Constraints and Edge Cases:**
No leading zeros; octets must be 0-255

### Python
**Required signature:**
def is_valid_ipv4(ip: str) -> bool:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static boolean isValidIPv4(String ip)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
bool isValidIPv4(const string& ip)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function isValidIPv4(ip)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P015
Problem Title: Username Validator
--------------------------------------------------

**Problem Description:**
Given a username string, determine whether it is valid.
Rules:
  - Length: 3 to 20 characters (inclusive)
  - Must start with a letter (a-z or A-Z)
  - Allowed characters: letters, digits, underscore (_), hyphen (-)
  - No spaces or other special characters
Return true if valid, false otherwise.

**Required Behavior:**
- Output contract: "true" or "false"
- Constraints: Must start with letter; 3-20 chars; only [a-zA-Z0-9_-]
- Input contract: JSON object {"input": "<username string>"}

**Input Parameters:**
JSON object {"input": "<username string>"}

**Expected Return Type:**
"true" or "false"

**Constraints and Edge Cases:**
Must start with letter; 3-20 chars; only [a-zA-Z0-9_-]

### Python
**Required signature:**
def is_valid_username(username: str) -> bool:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static boolean isValidUsername(String username)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
bool isValidUsername(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function isValidUsername(username)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P016
Problem Title: HTML Text Escaper
--------------------------------------------------

**Problem Description:**
Given a plain text string, escape it for safe inclusion in HTML.
Apply the following substitutions in this exact order:
  1. & -> &amp;
  2. < -> &lt;
  3. > -> &gt;
  4. " -> &quot;
  5. ' -> &#39;
Return the escaped string.

**Required Behavior:**
- Output contract: Escaped HTML-safe string
- Constraints: Process & first to avoid double-escaping
- Input contract: JSON object {"input": "<raw text>"}

**Input Parameters:**
JSON object {"input": "<raw text>"}

**Expected Return Type:**
Escaped HTML-safe string

**Constraints and Edge Cases:**
Process & first to avoid double-escaping

### Python
**Required signature:**
def escape_html(s: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String escapeHtml(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string escapeHtml(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function escapeHtml(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P017
Problem Title: CSV Cell Escaper
--------------------------------------------------

**Problem Description:**
Given a string representing a CSV cell value, escape it per RFC 4180.
Rules:
  - If the value contains a comma, double-quote, newline (LF), or carriage return (CR):
      Wrap the entire value in double-quotes.
      Escape any internal double-quote by doubling it ("" instead of ").
  - Otherwise: return the value unchanged.
Tab characters are NOT special in CSV and do NOT require escaping.

**Required Behavior:**
- Output contract: RFC 4180 escaped CSV cell string
- Constraints: RFC 4180 rules; tab is not special
- Input contract: JSON object {"input": "<cell value>"}

**Input Parameters:**
JSON object {"input": "<cell value>"}

**Expected Return Type:**
RFC 4180 escaped CSV cell string

**Constraints and Edge Cases:**
RFC 4180 rules; tab is not special

### Python
**Required signature:**
def escape_csv_cell(s: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String escapeCsvCell(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string escapeCsvCell(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function escapeCsvCell(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P018
Problem Title: JSON String Escaper
--------------------------------------------------

**Problem Description:**
Given a raw string, escape it so it can be safely embedded as the VALUE
inside a JSON string (without the surrounding quotes).
Apply these substitutions:
  " -> \"     \ -> \\     / -> \/
  backspace (U+0008) -> \b     form feed (U+000C) -> \f
  newline (U+000A) -> \n       carriage return (U+000D) -> \r
  tab (U+0009) -> \t
  other control chars (U+0000-U+001F) -> \uXXXX  (lowercase hex)
All other characters are returned as-is.
Return the escaped content WITHOUT surrounding quotes.

**Required Behavior:**
- Output contract: JSON-safe escaped string content (no surrounding quotes)
- Constraints: Exact substitution table as specified
- Input contract: JSON object {"input": "<raw string>"}

**Input Parameters:**
JSON object {"input": "<raw string>"}

**Expected Return Type:**
JSON-safe escaped string content (no surrounding quotes)

**Constraints and Edge Cases:**
Exact substitution table as specified

### Python
**Required signature:**
def escape_json_string(s: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String escapeJsonString(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string escapeJsonString(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function escapeJsonString(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P019
Problem Title: URL Query Component Encoder
--------------------------------------------------

**Problem Description:**
Given a string, percent-encode it for use as a URL query parameter value.
Encoding rules (RFC 3986 unreserved characters are NOT encoded):
  - Unreserved characters [A-Za-z0-9 - _ . ~] are kept as-is
  - All other characters are encoded as %XX where XX is the uppercase
    hexadecimal representation of each UTF-8 byte
  - Space is encoded as %20 (NOT as +)
Return the encoded string.

**Required Behavior:**
- Output contract: Percent-encoded string
- Constraints: RFC 3986 unreserved set; space -> %20; uppercase hex
- Input contract: JSON object {"input": "<raw string>"}

**Input Parameters:**
JSON object {"input": "<raw string>"}

**Expected Return Type:**
Percent-encoded string

**Constraints and Edge Cases:**
RFC 3986 unreserved set; space -> %20; uppercase hex

### Python
**Required signature:**
def encode_url_component(s: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String encodeUrlComponent(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string encodeUrlComponent(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function encodeUrlComponent(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P020
Problem Title: Template Placeholder Sanitizer
--------------------------------------------------

**Problem Description:**
Given a template string containing {{key}} placeholders, remove any
placeholder whose key contains characters other than [a-zA-Z0-9_].
Safe placeholders (keys matching ^[a-zA-Z0-9_]+$) are kept unchanged.
Unsafe placeholders are removed entirely (replaced with empty string).
An empty key {{}} is also considered unsafe and must be removed.
Return the sanitized string.

**Required Behavior:**
- Output contract: Template with unsafe placeholders removed
- Constraints: Safe key regex: ^[a-zA-Z0-9_]+$; empty key is unsafe
- Input contract: JSON object {"input": "<template string>"}

**Input Parameters:**
JSON object {"input": "<template string>"}

**Expected Return Type:**
Template with unsafe placeholders removed

**Constraints and Edge Cases:**
Safe key regex: ^[a-zA-Z0-9_]+$; empty key is unsafe

### Python
**Required signature:**
def sanitize_template(s: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String sanitizeTemplate(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string sanitizeTemplate(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function sanitizeTemplate(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P021
Problem Title: Safe Path Normalizer
--------------------------------------------------

**Problem Description:**
Normalize a relative file path by resolving "." and ".." segments.
Rules:
  - Split on "/" (forward slash only; backslash is NOT a separator and must return "")
  - Skip empty segments and "." segments
  - For ".." segments: pop the last resolved segment; if nothing to pop, return "" (traversal blocked)
  - If the input is empty or whitespace-only, return ""
  - Return the joined resolved segments separated by "/"
  - No leading or trailing slash in the result
Security: Any path that attempts to escape the logical root returns "".

**Required Behavior:**
- Output contract: Normalized path string, or empty string if traversal detected
- Constraints: Forward slash only; backslash input returns empty string
- Input contract: JSON object {"input": "<path string>"}

**Input Parameters:**
JSON object {"input": "<path string>"}

**Expected Return Type:**
Normalized path string, or empty string if traversal detected

**Constraints and Edge Cases:**
Forward slash only; backslash input returns empty string

### Python
**Required signature:**
def safe_path_normalize(path: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String safePathNormalize(String path)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string safePathNormalize(const string& path)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function safePathNormalize(path)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P022
Problem Title: Path Extension Validator
--------------------------------------------------

**Problem Description:**
Determine whether a filename or path has an allowed extension.
Allowed extensions (case-insensitive): .jpg .jpeg .png .gif .pdf .txt .csv
Rules:
  - Extract the filename as the last segment after "/" or "\"
  - Extension = everything from the LAST dot onwards (including the dot)
  - Files with no dot, or whose only dot is the leading dot (e.g. ".gitignore"), return false
  - Multiple extensions: only the last one counts (e.g. "file.tar.gz" → .gz → false)
  - Comparison is case-insensitive
Return true if allowed, false otherwise.

**Required Behavior:**
- Output contract: "true" or "false"
- Constraints: Allowed set: .jpg .jpeg .png .gif .pdf .txt .csv
- Input contract: JSON object {"input": "<filename or path>"}

**Input Parameters:**
JSON object {"input": "<filename or path>"}

**Expected Return Type:**
"true" or "false"

**Constraints and Edge Cases:**
Allowed set: .jpg .jpeg .png .gif .pdf .txt .csv

### Python
**Required signature:**
def is_allowed_extension(path: str) -> bool:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static boolean isAllowedExtension(String path)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
bool isAllowedExtension(const string& path)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function isAllowedExtension(path)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P023
Problem Title: Filename Sanitizer
--------------------------------------------------

**Problem Description:**
Convert an unsafe filename into a safe representation using these exact rules:
  1. Take only the first 200 characters of the input
  2. Replace every character NOT in [a-zA-Z0-9._-] with an underscore "_"
  3. Collapse consecutive underscores into a single underscore
  4. Strip leading and trailing underscores
  5. If the result is empty after all steps, return "_"
The dot "." and hyphen "-" characters are ALLOWED and preserved.

**Required Behavior:**
- Output contract: Sanitized filename string
- Constraints: Only [a-zA-Z0-9._-] allowed; others replaced with _
- Input contract: JSON object {"input": "<raw filename>"}

**Input Parameters:**
JSON object {"input": "<raw filename>"}

**Expected Return Type:**
Sanitized filename string

**Constraints and Edge Cases:**
Only [a-zA-Z0-9._-] allowed; others replaced with _

### Python
**Required signature:**
def sanitize_filename(name: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String sanitizeFilename(String name)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string sanitizeFilename(const string& name)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function sanitizeFilename(name)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P024
Problem Title: Archive Entry Path Checker
--------------------------------------------------

**Problem Description:**
Determine whether an archive entry path is safe (does not escape the extraction root).
Rules:
  - Empty path is "safe"
  - Paths starting with "/" are "unsafe" (absolute path)
  - Paths containing backslash "\" are "unsafe"
  - Resolve "." (skip) and ".." (go up one level) segments
  - If any ".." causes the depth to go below 0, return "unsafe"
  - Otherwise return "safe"
Forward slash "/" is the only path separator recognized.

**Required Behavior:**
- Output contract: "safe" or "unsafe"
- Constraints: Traversal check against logical root; backslash is unsafe
- Input contract: JSON object {"input": "<archive entry path>"}

**Input Parameters:**
JSON object {"input": "<archive entry path>"}

**Expected Return Type:**
"safe" or "unsafe"

**Constraints and Edge Cases:**
Traversal check against logical root; backslash is unsafe

### Python
**Required signature:**
def check_archive_entry(path: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String checkArchiveEntry(String path)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string checkArchiveEntry(const string& path)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function checkArchiveEntry(path)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P025
Problem Title: File Type Allowlist
--------------------------------------------------

**Problem Description:**
Given a file extension string (with or without a leading dot), determine
whether it belongs to the predefined safe allowlist.
Allowed types: jpg, jpeg, png, gif, bmp, pdf, txt, csv, json, xml
Rules:
  - Strip leading dot if present
  - Comparison is case-insensitive
  - Empty string returns false
Return true if in the allowlist, false otherwise.

**Required Behavior:**
- Output contract: "true" or "false"
- Constraints: Allowed: jpg jpeg png gif bmp pdf txt csv json xml
- Input contract: JSON object {"input": "<extension>"}

**Input Parameters:**
JSON object {"input": "<extension>"}

**Expected Return Type:**
"true" or "false"

**Constraints and Edge Cases:**
Allowed: jpg jpeg png gif bmp pdf txt csv json xml

### Python
**Required signature:**
def is_allowed_filetype(ext: str) -> bool:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static boolean isAllowedFiletype(String ext)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
bool isAllowedFiletype(const string& ext)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function isAllowedFiletype(ext)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P026
Problem Title: SQL Identifier Validator
--------------------------------------------------

**Problem Description:**
Validate a string as a SQL identifier using these exact rules:
  - Length must be 1 to 64 characters (inclusive)
  - Must match the pattern: starts with a letter [a-zA-Z] or underscore [_]
  - Remaining characters: only [a-zA-Z0-9_] allowed
  - No spaces, hyphens, quotes, or other special characters
Return true if valid, false otherwise.
Note: This is purely structural — no reserved word checking.

**Required Behavior:**
- Output contract: "true" or "false"
- Constraints: ^[a-zA-Z_][a-zA-Z0-9_]{0,63}$
- Input contract: JSON object {"input": "<identifier string>"}

**Input Parameters:**
JSON object {"input": "<identifier string>"}

**Expected Return Type:**
"true" or "false"

**Constraints and Edge Cases:**
^[a-zA-Z_][a-zA-Z0-9_]{0,63}$

### Python
**Required signature:**
def is_valid_sql_identifier(name: str) -> bool:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static boolean isValidSqlIdentifier(String name)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
bool isValidSqlIdentifier(const string& name)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function isValidSqlIdentifier(name)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P027
Problem Title: SQL String Literal Escaper
--------------------------------------------------

**Problem Description:**
Escape a string for safe embedding inside a SQL single-quoted string literal.
Exact substitution rules (in this order):
  1. Replace every backslash "\" with two backslashes "\\"
  2. Replace every single-quote "'" with two single-quotes "''"
No other substitutions are made.
Return the escaped content WITHOUT surrounding quotes.

**Required Behavior:**
- Output contract: Escaped string (no surrounding quotes)
- Constraints: Backslash doubled first, then single-quote doubled
- Input contract: JSON object {"input": "<raw string>"}

**Input Parameters:**
JSON object {"input": "<raw string>"}

**Expected Return Type:**
Escaped string (no surrounding quotes)

**Constraints and Edge Cases:**
Backslash doubled first, then single-quote doubled

### Python
**Required signature:**
def escape_sql_string(s: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String escapeSqlString(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string escapeSqlString(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function escapeSqlString(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P028
Problem Title: Parameterized Query Builder
--------------------------------------------------

**Problem Description:**
Build a parameterized SELECT query from a structured input string.
Input format: "table_name|col1=val1,col2=val2,..."
  - table_name and all column names must be valid SQL identifiers: ^[a-zA-Z_][a-zA-Z0-9_]*$
  - Values are NOT embedded — each becomes a "?" placeholder
  - Conditions appear in the order given
Output format: "SELECT * FROM <table> WHERE <col1>=? AND <col2>=?"
Return "INVALID" if:
  - Input does not contain exactly one "|"
  - Table name fails identifier validation
  - Any column name fails identifier validation
  - No conditions provided (empty conditions string)

**Required Behavior:**
- Output contract: "SELECT * FROM table WHERE col1=? AND col2=?" or "INVALID"
- Constraints: SQL identifier rules for table and column names
- Input contract: JSON object {"input": "table|col1=val1,col2=val2"}

**Input Parameters:**
JSON object {"input": "table|col1=val1,col2=val2"}

**Expected Return Type:**
"SELECT * FROM table WHERE col1=? AND col2=?" or "INVALID"

**Constraints and Edge Cases:**
SQL identifier rules for table and column names

### Python
**Required signature:**
def build_param_query(s: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String buildParamQuery(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string buildParamQuery(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function buildParamQuery(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P029
Problem Title: Sort Direction Validator
--------------------------------------------------

**Problem Description:**
Accept only the two valid SQL sort directions.
Rules:
  - Trim leading and trailing whitespace from the input
  - Convert to uppercase
  - If the result is "ASC" or "DESC", return it (canonical uppercase)
  - Otherwise return "INVALID"
This prevents SQL injection via ORDER BY direction parameters.

**Required Behavior:**
- Output contract: "ASC", "DESC", or "INVALID"
- Constraints: Only ASC and DESC (case-insensitive) are valid
- Input contract: JSON object {"input": "<sort direction>"}

**Input Parameters:**
JSON object {"input": "<sort direction>"}

**Expected Return Type:**
"ASC", "DESC", or "INVALID"

**Constraints and Edge Cases:**
Only ASC and DESC (case-insensitive) are valid

### Python
**Required signature:**
def validate_sort_direction(s: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String validateSortDirection(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string validateSortDirection(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function validateSortDirection(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P030
Problem Title: Column Allowlist Checker
--------------------------------------------------

**Problem Description:**
Determine whether a requested column name belongs to the predefined allowlist.
Allowed columns: id, name, email, created_at, status, age, role, score
Rules:
  - Trim whitespace before comparison
  - Comparison is case-SENSITIVE (exact match required)
  - Input must be a single column name — no commas, pipes, or SQL keywords
Return true if the column is in the allowlist, false otherwise.

**Required Behavior:**
- Output contract: "true" or "false"
- Constraints: Case-sensitive exact match against allowlist
- Input contract: JSON object {"input": "<column name>"}

**Input Parameters:**
JSON object {"input": "<column name>"}

**Expected Return Type:**
"true" or "false"

**Constraints and Edge Cases:**
Case-sensitive exact match against allowlist

### Python
**Required signature:**
def is_allowed_column(col: str) -> bool:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static boolean isAllowedColumn(String col)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
bool isAllowedColumn(const string& col)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function isAllowedColumn(col)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P031
Problem Title: Shell Argument Quoter
--------------------------------------------------

**Problem Description:**
Given a string representing a shell argument, return a safely single-quoted
version using the POSIX single-quote wrapping convention.
Rules:
  - Wrap the entire argument in single quotes: 'arg'
  - If the argument contains a single quote, escape it as: '\''
    (close quote, backslash-quote, reopen quote)
  - Backslash and all other characters are treated as literals inside
    single quotes — they do NOT need escaping
  - Empty string → ''
This is a deterministic string transformation. The evaluator does NOT
execute any shell command.

**Required Behavior:**
- Output contract: Single-quoted shell-safe string
- Constraints: POSIX single-quote wrapping; ' escaped as '\'''
- Input contract: JSON object {"input": "<argument string>"}

**Input Parameters:**
JSON object {"input": "<argument string>"}

**Expected Return Type:**
Single-quoted shell-safe string

**Constraints and Edge Cases:**
POSIX single-quote wrapping; ' escaped as '\'''

### Python
**Required signature:**
def quote_shell_arg(s: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String quoteShellArg(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string quoteShellArg(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function quoteShellArg(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P032
Problem Title: Command Name Allowlist
--------------------------------------------------

**Problem Description:**
Given a command name string, determine whether it is in the predefined
safe allowlist.
Allowed commands: ls, cat, echo, grep, find, sort, uniq, wc, head, tail
Rules:
  - Trim leading/trailing whitespace before comparison
  - Comparison is case-SENSITIVE
  - Input containing spaces after trimming (e.g. "find; rm") is rejected
Return true if in allowlist, false otherwise.
The evaluator does NOT execute any command.

**Required Behavior:**
- Output contract: "true" or "false"
- Constraints: Allowed: ls cat echo grep find sort uniq wc head tail (exact, case-sensitive)
- Input contract: JSON object {"input": "<command name>"}

**Input Parameters:**
JSON object {"input": "<command name>"}

**Expected Return Type:**
"true" or "false"

**Constraints and Edge Cases:**
Allowed: ls cat echo grep find sort uniq wc head tail (exact, case-sensitive)

### Python
**Required signature:**
def is_allowed_command(s: str) -> bool:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static boolean isAllowedCommand(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
bool isAllowedCommand(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function isAllowedCommand(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P033
Problem Title: Shell Metacharacter Detector
--------------------------------------------------

**Problem Description:**
Given a string, determine whether it contains any shell metacharacter.
Dangerous characters: ; | & $ ` > < ( ) { } \ " ' and newline (LF/CR)
Return "safe" if NONE of these characters are present.
Return "unsafe" if ANY of them appear.
Empty string is "safe".
The evaluator does NOT execute any detected command.

**Required Behavior:**
- Output contract: "safe" or "unsafe"
- Constraints: Dangerous set: ; | & $ ` > < ( ) { } \ " ' \n \r
- Input contract: JSON object {"input": "<string to check>"}

**Input Parameters:**
JSON object {"input": "<string to check>"}

**Expected Return Type:**
"safe" or "unsafe"

**Constraints and Edge Cases:**
Dangerous set: ; | & $ ` > < ( ) { } \ " ' \n \r

### Python
**Required signature:**
def detect_shell_meta(s: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String detectShellMeta(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string detectShellMeta(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function detectShellMeta(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P034
Problem Title: Environment Variable Name Validator
--------------------------------------------------

**Problem Description:**
Given a string, determine whether it is a valid POSIX environment
variable name.
Rules:
  - Must match ^[A-Z_][A-Z0-9_]*$ (uppercase only convention)
  - Length: 1 to 64 characters inclusive
  - Only uppercase letters A-Z, digits 0-9, and underscore _
  - Must start with an uppercase letter or underscore
Return true if valid, false otherwise.

**Required Behavior:**
- Output contract: "true" or "false"
- Constraints: ^[A-Z_][A-Z0-9_]*$, length 1-64
- Input contract: JSON object {"input": "<env var name>"}

**Input Parameters:**
JSON object {"input": "<env var name>"}

**Expected Return Type:**
"true" or "false"

**Constraints and Edge Cases:**
^[A-Z_][A-Z0-9_]*$, length 1-64

### Python
**Required signature:**
def is_valid_env_var(name: str) -> bool:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static boolean isValidEnvVar(String name)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
bool isValidEnvVar(const string& name)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function isValidEnvVar(name)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P035
Problem Title: Command Argument Splitter
--------------------------------------------------

**Problem Description:**
Split a command-line argument string into individual tokens.
Parsing rules:
  - Tokens are separated by one or more space characters outside quotes
  - Text inside double-quotes "..." is treated as a single token (quotes stripped)
  - An empty double-quoted group "" produces an empty string token
  - Single quotes are treated as ordinary characters (not special)
  - Backslash has no special meaning (treated as literal)
  - Empty input → empty list
Return the result as a JSON array of strings, e.g. ["a","b","c"]

**Required Behavior:**
- Output contract: JSON array of strings e.g. ["arg1","arg2"]
- Constraints: Double-quote grouping only; single-quote and backslash are literal
- Input contract: JSON object {"input": "<command argument string>"}

**Input Parameters:**
JSON object {"input": "<command argument string>"}

**Expected Return Type:**
JSON array of strings e.g. ["arg1","arg2"]

**Constraints and Edge Cases:**
Double-quote grouping only; single-quote and backslash are literal

### Python
**Required signature:**
def split_args(s: str) -> list[str]:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static java.util.List<String> splitArgs(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
vector<string> splitArgs(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function splitArgs(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P036
Problem Title: Safe Literal Parser
--------------------------------------------------

**Problem Description:**
Parse and validate that the input is exactly one of these safe literal types:
  - Integer: optional leading minus, digits only; no leading zeros except "0"
  - Boolean: exactly "true" or "false" (lowercase only)
  - Null: exactly "null"
  - Quoted string: starts and ends with double-quote; internal double-quotes
    must be escaped as \"; no other escape sequences are supported
If valid, return the canonical representation:
  integer → decimal string (e.g. "42", "-7")
  boolean → "true" or "false"
  null    → "null"
  string  → content without surrounding quotes (\" unescaped to ")
If invalid (lists, dicts, floats, expressions, function calls, etc.) → "INVALID"

**Required Behavior:**
- Output contract: Canonical value string, or "INVALID"
- Constraints: Only int/bool/null/double-quoted-string accepted
- Input contract: JSON object {"input": "<literal string>"}

**Input Parameters:**
JSON object {"input": "<literal string>"}

**Expected Return Type:**
Canonical value string, or "INVALID"

**Constraints and Edge Cases:**
Only int/bool/null/double-quoted-string accepted

### Python
**Required signature:**
def parse_safe_literal(s: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String parseSafeLiteral(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string parseSafeLiteral(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function parseSafeLiteral(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P037
Problem Title: Configuration Boolean Parser
--------------------------------------------------

**Problem Description:**
Parse a configuration value string as a boolean.
TRUE  values (case-insensitive after trim): true, yes, 1, on, enabled
FALSE values (case-insensitive after trim): false, no, 0, off, disabled
Anything else → "INVALID"
Return "true", "false", or "INVALID".

**Required Behavior:**
- Output contract: "true", "false", or "INVALID"
- Constraints: TRUE: true/yes/1/on/enabled | FALSE: false/no/0/off/disabled
- Input contract: JSON object {"input": "<config value>"}

**Input Parameters:**
JSON object {"input": "<config value>"}

**Expected Return Type:**
"true", "false", or "INVALID"

**Constraints and Edge Cases:**
TRUE: true/yes/1/on/enabled | FALSE: false/no/0/off/disabled

### Python
**Required signature:**
def parse_config_bool(s: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String parseConfigBool(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string parseConfigBool(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function parseConfigBool(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P038
Problem Title: Configuration Key Allowlist
--------------------------------------------------

**Problem Description:**
Given a configuration key string, determine whether it is in the
predefined allowlist.
Allowed keys: host, port, database, username, password, timeout,
              max_connections, ssl_enabled, log_level, retry_count
Rules:
  - Trim whitespace before comparison
  - Comparison is case-SENSITIVE
Return true if in allowlist, false otherwise.

**Required Behavior:**
- Output contract: "true" or "false"
- Constraints: 10 allowed keys; case-sensitive exact match after trim
- Input contract: JSON object {"input": "<config key>"}

**Input Parameters:**
JSON object {"input": "<config key>"}

**Expected Return Type:**
"true" or "false"

**Constraints and Edge Cases:**
10 allowed keys; case-sensitive exact match after trim

### Python
**Required signature:**
def is_allowed_config_key(key: str) -> bool:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static boolean isAllowedConfigKey(String key)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
bool isAllowedConfigKey(const string& key)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function isAllowedConfigKey(key)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P039
Problem Title: Structured Token Decoder
--------------------------------------------------

**Problem Description:**
Validate the structural format of a benchmark token string.
Token format: "<header>.<payload>.<checksum>"
Rules:
  - Exactly 3 dot-separated parts
  - header: one or more base64url characters [A-Za-z0-9_-]+
  - payload: one or more base64url characters [A-Za-z0-9_-]+
  - checksum: exactly 8 lowercase hexadecimal digits [0-9a-f]{8}
Return "valid" if the token matches all rules.
Return "invalid" otherwise.
This is purely structural validation — no decryption, no secrets, no network.

**Required Behavior:**
- Output contract: "valid" or "invalid"
- Constraints: 3 dot-separated parts; header+payload base64url; checksum 8 lowercase hex
- Input contract: JSON object {"input": "<token string>"}

**Input Parameters:**
JSON object {"input": "<token string>"}

**Expected Return Type:**
"valid" or "invalid"

**Constraints and Edge Cases:**
3 dot-separated parts; header+payload base64url; checksum 8 lowercase hex

### Python
**Required signature:**
def validate_token(s: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String validateToken(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string validateToken(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function validateToken(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P040
Problem Title: Safe Numeric Expression Validator
--------------------------------------------------

**Problem Description:**
Validate that an input string is a safe numeric expression matching
the restricted grammar:
  expr   = number ( operator number )*
  number = optional minus sign, then one or more digits; no leading zeros
           except the standalone zero "0"
  operator = + | - | * | /
  Spaces around operators are allowed
Return "valid" if the expression matches exactly.
Return "invalid" for anything else: empty input, letters, parentheses,
function calls, exponentiation, leading zeros, or malformed structure.
The evaluator does NOT evaluate the expression.

**Required Behavior:**
- Output contract: "valid" or "invalid"
- Constraints: number op number grammar; integers only; no parens; no leading zeros
- Input contract: JSON object {"input": "<expression string>"}

**Input Parameters:**
JSON object {"input": "<expression string>"}

**Expected Return Type:**
"valid" or "invalid"

**Constraints and Edge Cases:**
number op number grammar; integers only; no parens; no leading zeros

### Python
**Required signature:**
def validate_numeric_expr(s: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String validateNumericExpr(String s)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string validateNumericExpr(const string& s)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function validateNumericExpr(s)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P041
Problem Title: Frequency Counter Large Input
--------------------------------------------------

**Problem Description:**
Given a list of integers, count the frequency of each value.
Return a JSON object with integer keys (as strings) sorted ascending,
mapping each key to its count.
Empty list returns an empty object {}.

**Required Behavior:**
- Output contract: JSON object {"k1":n1,...} sorted by key ascending
- Constraints: Keys are integer strings; sorted ascending
- Input contract: JSON object {"nums": [...]}

**Input Parameters:**
JSON object {"nums": [...]}

**Expected Return Type:**
JSON object {"k1":n1,...} sorted by key ascending

**Constraints and Edge Cases:**
Keys are integer strings; sorted ascending

### Python
**Required signature:**
def frequency_counter(nums: list[int]) -> dict:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static Map<Integer,Integer> frequencyCounter(int[] nums)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
map<int,int> frequencyCounter(vector<int>& nums)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function frequencyCounter(nums)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P042
Problem Title: Duplicate Detector
--------------------------------------------------

**Problem Description:**
Given a list of integers, determine whether any value appears more
than once.
Return true if any duplicate exists, false otherwise.
Empty list has no duplicates → false.

**Required Behavior:**
- Output contract: "true" or "false"
- Constraints: Any repeated value → true
- Input contract: JSON object {"nums": [...]}

**Input Parameters:**
JSON object {"nums": [...]}

**Expected Return Type:**
"true" or "false"

**Constraints and Edge Cases:**
Any repeated value → true

### Python
**Required signature:**
def has_duplicate(nums: list[int]) -> bool:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static boolean hasDuplicate(int[] nums)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
bool hasDuplicate(vector<int>& nums)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function hasDuplicate(nums)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P043
Problem Title: Streaming Sum
--------------------------------------------------

**Problem Description:**
Given a list of integers, return their sum as a decimal integer string.
Empty list → "0".
Handles negative values and large sequences.

**Required Behavior:**
- Output contract: Integer sum as decimal string
- Constraints: Empty → 0; supports negative values
- Input contract: JSON object {"nums": [...]}

**Input Parameters:**
JSON object {"nums": [...]}

**Expected Return Type:**
Integer sum as decimal string

**Constraints and Edge Cases:**
Empty → 0; supports negative values

### Python
**Required signature:**
def streaming_sum(nums: list[int]) -> int:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static long streamingSum(int[] nums)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
long long streamingSum(vector<int>& nums)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function streamingSum(nums)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P044
Problem Title: Bounded Log Processor
--------------------------------------------------

**Problem Description:**
Given a multiline log string and a maximum line count, process at most
max_lines non-empty lines from the start.
Count the total number of words (whitespace-split) across kept lines.
Return JSON: {"kept": K, "total_words": W}
where K is the number of lines actually kept (≤ max_lines).
Empty log or max_lines=0 → {"kept":0,"total_words":0}

**Required Behavior:**
- Output contract: JSON {"kept":K,"total_words":W}
- Constraints: Skip empty lines; take first max_lines non-empty lines
- Input contract: JSON object {"log": "<multiline string>", "max_lines": N}

**Input Parameters:**
JSON object {"log": "<multiline string>", "max_lines": N}

**Expected Return Type:**
JSON {"kept":K,"total_words":W}

**Constraints and Edge Cases:**
Skip empty lines; take first max_lines non-empty lines

### Python
**Required signature:**
def bounded_log_processor(log: str, max_lines: int) -> dict:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static Map<String,Integer> boundedLogProcessor(String log, int maxLines)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
map<string,int> boundedLogProcessor(const string& log, int maxLines)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function boundedLogProcessor(log, maxLines)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P045
Problem Title: Top-K Frequent Values
--------------------------------------------------

**Problem Description:**
Given a list of integers and an integer k, return the k most frequent
values as a sorted JSON array (ascending order).
Tie-breaking: when frequencies are equal, lower value takes priority
(is considered "more frequent" for selection purposes).
If k >= number of unique values, return all unique values sorted ascending.
Empty list or k=0 → [].

**Required Behavior:**
- Output contract: JSON array of integers sorted ascending
- Constraints: Tie-break: lower value first; result sorted ascending
- Input contract: JSON object {"nums": [...], "k": N}

**Input Parameters:**
JSON object {"nums": [...], "k": N}

**Expected Return Type:**
JSON array of integers sorted ascending

**Constraints and Edge Cases:**
Tie-break: lower value first; result sorted ascending

### Python
**Required signature:**
def top_k_frequent(nums: list[int], k: int) -> list[int]:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static int[] topKFrequent(int[] nums, int k)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
vector<int> topKFrequent(vector<int>& nums, int k)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function topKFrequent(nums, k)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P046
Problem Title: Token Format Validator
--------------------------------------------------

**Problem Description:**
Given a token string, validate it against this exact format:
  - Length: 8 to 32 characters inclusive
  - Characters: letters [a-zA-Z], digits [0-9], and hyphens [-] only
  - Must start with a letter [a-zA-Z]
  - Pattern: ^[a-zA-Z][a-zA-Z0-9\-]{7,31}$
Return "valid" if the token matches, "invalid" otherwise.
Empty string → "invalid".

**Required Behavior:**
- Output contract: "valid" or "invalid"
- Constraints: ^[a-zA-Z][a-zA-Z0-9\-]{7,31}$ ; length 8-32
- Input contract: JSON object {"token": "<string>"}

**Input Parameters:**
JSON object {"token": "<string>"}

**Expected Return Type:**
"valid" or "invalid"

**Constraints and Edge Cases:**
^[a-zA-Z][a-zA-Z0-9\-]{7,31}$ ; length 8-32

### Python
**Required signature:**
def validate_token_format(token: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String validateTokenFormat(String token)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string validateTokenFormat(const string& token)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function validateTokenFormat(token)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P047
Problem Title: Permission Rule Evaluator
--------------------------------------------------

**Problem Description:**
Evaluate whether a role is allowed to perform an action using a
hardcoded permission table:
  admin   → read, write, delete, execute
  editor  → read, write
  viewer  → read
  guest   → (none)
Return "allowed" if the role has the action, "denied" otherwise.
Unknown role → "denied".
This is fully in-memory. No real systems are accessed.

**Required Behavior:**
- Output contract: "allowed" or "denied"
- Constraints: 4 hardcoded roles; unknown role → denied
- Input contract: JSON object {"role": "<string>", "action": "<string>"}

**Input Parameters:**
JSON object {"role": "<string>", "action": "<string>"}

**Expected Return Type:**
"allowed" or "denied"

**Constraints and Edge Cases:**
4 hardcoded roles; unknown role → denied

### Python
**Required signature:**
def evaluate_permission(role: str, action: str) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String evaluatePermission(String role, String action)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string evaluatePermission(const string& role, const string& action)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function evaluatePermission(role, action)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P048
Problem Title: Role Permission Checker
--------------------------------------------------

**Problem Description:**
Given a role and permission name, determine whether the role has that
permission using the same hardcoded table as P047:
  admin   → read, write, delete, execute
  editor  → read, write
  viewer  → read
  guest   → (none)
Return true if the role has the permission, false otherwise.
Unknown role → false.

**Required Behavior:**
- Output contract: "true" or "false"
- Constraints: Same 4-role table as P047; unknown role → false
- Input contract: JSON object {"role": "<string>", "permission": "<string>"}

**Input Parameters:**
JSON object {"role": "<string>", "permission": "<string>"}

**Expected Return Type:**
"true" or "false"

**Constraints and Edge Cases:**
Same 4-role table as P047; unknown role → false

### Python
**Required signature:**
def role_has_permission(role: str, permission: str) -> bool:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static boolean roleHasPermission(String role, String permission)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
bool roleHasPermission(const string& role, const string& permission)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function roleHasPermission(role, permission)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P049
Problem Title: Session Timeout Checker
--------------------------------------------------

**Problem Description:**
Given a last_active timestamp, current_time timestamp, and timeout
duration (all non-negative integers in seconds), determine whether
the session is still valid.
Rules:
  - If current_time < last_active → return "invalid" (impossible timestamp)
  - Elapsed = current_time - last_active
  - If elapsed > timeout → "expired"
  - If elapsed <= timeout → "active"  (boundary is ACTIVE, not expired)
No real clock is used. All inputs come from the test case.

**Required Behavior:**
- Output contract: "active", "expired", or "invalid"
- Constraints: Boundary elapsed==timeout → active; current<last → invalid
- Input contract: JSON object {"last_active": T1, "current_time": T2, "timeout": N}

**Input Parameters:**
JSON object {"last_active": T1, "current_time": T2, "timeout": N}

**Expected Return Type:**
"active", "expired", or "invalid"

**Constraints and Edge Cases:**
Boundary elapsed==timeout → active; current<last → invalid

### Python
**Required signature:**
def check_session(last_active: int, current_time: int, timeout: int) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String checkSession(int lastActive, int currentTime, int timeout)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string checkSession(int lastActive, int currentTime, int timeout)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function checkSession(lastActive, currentTime, timeout)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

--------------------------------------------------
Problem ID: P050
Problem Title: Access Scope Validator
--------------------------------------------------

**Problem Description:**
Determine whether a requested scope is covered by an allowed scopes list.
Scope hierarchy uses colon ":" as separator (e.g. "read:files:reports").
Granting rules:
  - "granted" if requested appears exactly in allowed list, OR
  - "granted" if a parent scope of requested appears in allowed
    (e.g. allowed=["read"] grants "read:files" and "read:files:reports")
  - "denied" otherwise
Parent scope check: split requested on ":", check all prefixes.
Empty allowed list → "denied".

**Required Behavior:**
- Output contract: "granted" or "denied"
- Constraints: Colon-separated hierarchy; parent grants children
- Input contract: JSON object {"requested": "<scope>", "allowed": ["<scope1>",...]}

**Input Parameters:**
JSON object {"requested": "<scope>", "allowed": ["<scope1>",...]}

**Expected Return Type:**
"granted" or "denied"

**Constraints and Edge Cases:**
Colon-separated hierarchy; parent grants children

### Python
**Required signature:**
def validate_scope(requested: str, allowed: list[str]) -> str:

**Required output:** Only the executable function body. Do not include `input()`, `print()`, `main()`, comments, markdown, or extra helper logic.

**Implementation placeholder:**

    # INSERT SOLUTION HERE

### Java
**Required signature:**
public static String validateScope(String requested, java.util.List<String> allowed)

**Required output:** Only the method body inside `public class Solution`; do not include a `main()` method, `Scanner`, or `System.in` reads.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### C++
**Required signature:**
string validateScope(const string& requested, vector<string>& allowed)

**Required output:** Only the executable function body. Do not include a `main()` function, extra I/O code, or unrelated helpers.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

### JavaScript
**Required signature:**
function validateScope(requested, allowed)

**Required output:** Only the executable function implementation. Do not add interactive I/O, extra explanation, or non-essential code. Export the function in the harness-compatible `module.exports` form.

**Implementation placeholder:**

    // INSERT SOLUTION HERE

**Language-specific compatibility requirement:** Use the exact function name and argument structure declared above. Do not change the benchmark semantics or expected return format.

## Final Validation Checklist

Before generating any AI code, verify the following:
- [ ] All 50 benchmark problems are included in the generation set.
- [ ] Every problem has four language-specific requirements.
- [ ] Each signature matches the benchmark file exactly.
- [ ] The generated output contains only code, no markdown or commentary.
- [ ] No `main()`, `input()`, `Scanner`, `cin`, or interactive I/O is included unless explicitly required by the benchmark contract.
- [ ] Each result is directly executable by the existing Research Code Evaluator harness.
- [ ] No benchmark problems, IDs, test cases, or expected outputs are modified.
- [ ] All five models receive the same specification and constraints.

## Unresolved Issues or Ambiguities

This specification intentionally follows the authoritative benchmark and execution system. No new problems were invented, and no benchmark data was altered.

No unresolved benchmark ambiguities were identified in the source-of-truth artifacts reviewed for this specification. The benchmark file and execution contract remain the governing authority for function names, signatures, and required behavior.

## Summary

The benchmark is fixed, the problem set is complete, and the generation instructions are standardized for five AI models across four programming languages. The generation task must remain a code-only, harness-compatible exercise with no benchmark drift.