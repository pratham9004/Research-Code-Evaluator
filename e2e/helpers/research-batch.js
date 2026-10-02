const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '../..');
const MODEL_FILES = {
  ChatGPT: {
    python: 'ChatGPT/Python/solution.py',
    javascript: 'ChatGPT/JavaScript/solution.js',
    java: 'ChatGPT/Java/Solution.java',
    cpp: 'ChatGPT/C++/solution.cpp',
  },
  Perplexity: {
    python: 'Perplexity/Python/solutions.py',
    javascript: 'Perplexity/JavaScript/solutions.js',
    java: 'Perplexity/Java/Solutions.java',
    cpp: 'Perplexity/C++/solutions.cpp',
  },
  Grok: {
    python: 'Grok/Python/solutions.py',
    javascript: 'Grok/JavaScript/solutions.js',
    java: 'Grok/Java/Solutions.java',
    cpp: 'Grok/C++/solutions.cpp',
  },
  Gemini: {
    python: 'Gemini/Python/solutions.py',
    javascript: 'Gemini/JavaScript/solutions.js',
    java: 'Gemini/Java/Solutions.java',
    cpp: 'Gemini/C++/solutions.cpp',
  },
  Claude_Sonnet_5: {
    python: 'Claude_Sonnet_5/Python/solutions_python.py',
    javascript: 'Claude_Sonnet_5/JavaScript/solutions_javascript.js',
    java: 'Claude_Sonnet_5/Java/Solution.java',
    cpp: 'Claude_Sonnet_5/C++/solutions_cpp.cpp',
  },
};

const HUMAN_FILES = {
  python: 'human code/python/solutions.py',
  javascript: 'human code/javascript/solutions.js',
  java: 'human code/java/Solution.java',
  cpp: 'human code/C++/solutions.cpp',
};

const ENTRIES = [
  ['two_sum', 'twoSum'], ['max_subarray', 'maxSubarray'], ['binary_search', 'binarySearch'],
  ['merge_sorted_arrays', 'mergeSortedArrays'], ['is_balanced', 'isBalanced'],
  ['csv_field_count', 'csvFieldCount'], ['count_log_levels', 'countLogLevels'],
  ['parse_key_value', 'parseKeyValue'], ['normalize_date', 'normalizeDate'],
  ['word_frequency', 'wordFrequency'], ['is_valid_email', 'isValidEmail'],
  ['is_valid_password', 'isValidPassword'], ['is_valid_range', 'isValidRange'],
  ['is_valid_ipv4', 'isValidIPv4'], ['is_valid_username', 'isValidUsername'],
  ['escape_html', 'escapeHtml'], ['escape_csv_cell', 'escapeCsvCell'],
  ['escape_json_string', 'escapeJsonString'], ['encode_url_component', 'encodeUrlComponent'],
  ['sanitize_template', 'sanitizeTemplate'], ['safe_path_normalize', 'safePathNormalize'],
  ['is_allowed_extension', 'isAllowedExtension'], ['sanitize_filename', 'sanitizeFilename'],
  ['check_archive_entry', 'checkArchiveEntry'], ['is_allowed_filetype', 'isAllowedFiletype'],
  ['is_valid_sql_identifier', 'isValidSqlIdentifier'], ['escape_sql_string', 'escapeSqlString'],
  ['build_param_query', 'buildParamQuery'], ['validate_sort_direction', 'validateSortDirection'],
  ['is_allowed_column', 'isAllowedColumn'], ['quote_shell_arg', 'quoteShellArg'],
  ['is_allowed_command', 'isAllowedCommand'], ['detect_shell_meta', 'detectShellMeta'],
  ['is_valid_env_var', 'isValidEnvVar'], ['split_args', 'splitArgs'],
  ['parse_safe_literal', 'parseSafeLiteral'], ['parse_config_bool', 'parseConfigBool'],
  ['is_allowed_config_key', 'isAllowedConfigKey'], ['validate_token', 'validateToken'],
  ['validate_numeric_expr', 'validateNumericExpr'], ['frequency_counter', 'frequencyCounter'],
  ['has_duplicate', 'hasDuplicate'], ['streaming_sum', 'streamingSum'],
  ['bounded_log_processor', 'boundedLogProcessor'], ['top_k_frequent', 'topKFrequent'],
  ['validate_token_format', 'validateTokenFormat'], ['evaluate_permission', 'evaluatePermission'],
  ['role_has_permission', 'roleHasPermission'], ['check_session', 'checkSession'],
  ['validate_scope', 'validateScope'],
];

function problemIds() {
  return Array.from({ length: 50 }, (_, index) => `P${String(index + 1).padStart(3, '0')}`);
}

function problemEntry(problemId, language) {
  const index = Number(problemId.slice(1)) - 1;
  const entry = ENTRIES[index];
  if (!entry) throw new Error(`Unknown benchmark problem: ${problemId}`);
  return entry[language === 'python' ? 0 : 1];
}

function readSource(relativePath) {
  const fullPath = path.join(ROOT, 'AI VS HUMAN CODE', relativePath);
  if (!fs.existsSync(fullPath)) throw new Error(`Solution file does not exist: ${relativePath}`);
  return fs.readFileSync(fullPath, 'utf8').replace(/^\uFEFF/, '');
}

function extractFunction(source, entry, language, label) {
  const escaped = entry.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  let declaration;
  if (language === 'python') {
    declaration = new RegExp(`^(?:async\\s+)?def\\s+${escaped}\\s*\\(`, 'm');
  } else if (language === 'javascript') {
    declaration = new RegExp(`(?:function\\s+${escaped}\\s*\\(|(?:const|let|var)\\s+${escaped}\\s*=\\s*(?:async\\s*)?(?:function|\\())`);
  } else if (language === 'java') {
    declaration = new RegExp(`(?:public|protected|private)?\\s*(?:static\\s+)?[\\w<>?,\\[\\]. ]+\\s+${escaped}\\s*\\(`);
  } else {
    declaration = new RegExp(`(?:[\\w:<>&,* ]+\\s+)${escaped}\\s*\\(`);
  }

  const match = declaration.exec(source);
  if (!match) throw new Error(`${label} solution has no benchmark function '${entry}'. The selected source may belong to a different benchmark.`);

  const start = match.index;
  if (language === 'python') {
    const lineStart = source.lastIndexOf('\n', start - 1) + 1;
    const after = source.slice(start);
    const next = after.slice(1).search(/^(?:async\s+)?def\s+\w+\s*\(/m);
    const end = next < 0 ? source.length : start + 1 + next;
    const raw = source.slice(lineStart, end).trimEnd();
    const firstFunction = new RegExp(`^(?:async\\s+)?def\\s+${ENTRIES[0][0]}\\s*\\(`, 'm').exec(source);
    const prefix = firstFunction ? source.slice(0, firstFunction.index).trim() : '';
    const imports = [...source.matchAll(/^(?:from\s+[\w.]+\s+import\s+.+|import\s+[\w., ]+)$/gm)]
      .map((item) => item[0]);
    return [...new Set([prefix, ...imports, raw].filter(Boolean))].join('\n\n');
  }

  if (language === 'javascript') {
    const lineStart = source.lastIndexOf('\n', start - 1) + 1;
    const nextMarker = source.slice(start).search(/^\s*(?:\/\/\s*)?P\d{3}\b/m);
    let end = nextMarker < 0 ? source.length : start + nextMarker;
    const body = source.slice(lineStart, end).trimEnd();
    const firstMarker = source.search(/^\s*(?:\/\/\s*)?P001\b/m);
    const prefix = source.slice(0, firstMarker < 0 ? 0 : firstMarker).trim();
    const exportLine = `\n\nmodule.exports = { ${entry} };`;
    return `${[prefix, body].filter(Boolean).join('\n\n')}${exportLine}`;
  }

  const brace = source.indexOf('{', start);
  if (brace < 0) throw new Error(`Could not find function body for ${entry} in ${label} solution`);
  const end = matchingBrace(source, brace);
  const lineStart = source.lastIndexOf('\n', start - 1) + 1;
  const method = source.slice(lineStart, end).trim();

  if (language === 'java') {
    const classStart = source.search(/\bpublic\s+class\s+Solution\b/);
    if (classStart < 0) throw new Error(`${label} Java file does not declare public class Solution`);
    const header = source.slice(0, classStart);
    const classLineEnd = source.indexOf('\n', classStart);
    const classOpen = source.indexOf('{', classStart);
    const firstEntry = ENTRIES[0][1];
    const firstMethod = new RegExp(`(?:public|protected|private)?\\s*(?:static\\s+)?[\\w<>?,\\[\\]. ]+\\s+${firstEntry}\\s*\\(`).exec(source);
    const preambleEnd = firstMethod ? source.lastIndexOf('\n', firstMethod.index) + 1 : lineStart;
    const preamble = source.slice(classOpen + 1, preambleEnd)
      .replace(/^\s*(?:\/\/\s*)?P\d{3}\b[^\r\n]*\r?\n/gm, '').trim();
    return `${header}public class Solution {\n${preamble ? `${preamble}\n` : ''}${method}\n}`;
  }

  const firstEntry = ENTRIES[0][1];
  const firstFunction = new RegExp(`(?:[\\w:<>&,* ]+\\s+)${firstEntry}\\s*\\(`).exec(source);
  const prefix = source.slice(0, firstFunction ? source.lastIndexOf('\n', firstFunction.index) + 1 : lineStart)
    .replace(/^\s*P\d{3}\s*\r?\n/gm, '').trim();
  const cppPrefix = prefix || '#include <bits/stdc++.h>\nusing namespace std;';
  return `${cppPrefix}\n\n${method}`;
}

function matchingBrace(source, openIndex) {
  let depth = 0;
  let quote = null;
  let lineComment = false;
  let blockComment = false;
  let escape = false;
  for (let index = openIndex; index < source.length; index += 1) {
    const char = source[index];
    const next = source[index + 1];
    if (lineComment) { if (char === '\n') lineComment = false; continue; }
    if (blockComment) { if (char === '*' && next === '/') { blockComment = false; index += 1; } continue; }
    if (quote) {
      if (escape) escape = false;
      else if (char === '\\') escape = true;
      else if (char === quote) quote = null;
      continue;
    }
    if (char === '/' && next === '/') { lineComment = true; index += 1; continue; }
    if (char === '/' && next === '*') { blockComment = true; index += 1; continue; }
    if (char === '"' || char === "'" || char === '`') { quote = char; continue; }
    if (char === '{') depth += 1;
    if (char === '}' && --depth === 0) return index + 1;
  }
  throw new Error('Unbalanced braces in benchmark solution source');
}

function getSolutions(model, language, problemId) {
  const aiPath = MODEL_FILES[model]?.[language];
  const humanPath = HUMAN_FILES[language];
  if (!aiPath || !humanPath) throw new Error(`No solution mapping for ${model} + ${language}`);
  const entry = problemEntry(problemId, language);
  try {
    return {
      ai: extractFunction(readSource(aiPath), entry, language, `${model} source file AI VS HUMAN CODE/${aiPath}`),
      human: extractFunction(readSource(humanPath), entry, language, 'Human'),
    };
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    throw new Error(`${problemId} | ${model} | ${language} | load solution files | ${message}`);
  }
}

async function ensureNoDuplicateComparisons(request, baseURL, model, language, ids) {
  const response = await request.get(new URL('/api/comparisons', baseURL).toString());
  if (!response.ok()) throw new Error(`Duplicate preflight failed: /api/comparisons returned ${response.status()}`);
  const comparisons = await response.json();
  const existing = comparisons.filter((row) => ids.includes(row.problem_id)
    && row.ai_name === model && row.language === language);
  const byProblem = new Map();
  for (const row of existing) {
    const rows = byProblem.get(row.problem_id) ?? [];
    rows.push(row);
    byProblem.set(row.problem_id, rows);
  }
  const incomplete = existing.filter((row) => row.status !== 'completed');
  if (incomplete.length) {
    const found = incomplete.map((row) => `${row.problem_id} (${row.status})`).join(', ');
    throw new Error(`Refusing ${model} + ${language} batch because unfinished comparisons already exist: ${found}`);
  }
  return new Set(byProblem.keys());
}

async function runBatch({ page, request, baseURL, model, language, onlyProblemId, submissionModelName }) {
  const ids = onlyProblemId
    ? (Array.isArray(onlyProblemId) ? onlyProblemId : [onlyProblemId])
    : problemIds();
  const submittedAs = submissionModelName || model;
  const completed = await ensureNoDuplicateComparisons(request, baseURL, submittedAs, language, ids);
  await page.context().grantPermissions(['clipboard-read', 'clipboard-write'], {
    origin: new URL(baseURL).origin,
  });
  page.setDefaultTimeout(3 * 60 * 1000);
  page.setDefaultNavigationTimeout(60 * 1000);
  const browserErrors = [];
  const failures = [];
  page.on('pageerror', (error) => browserErrors.push(error.message));
  for (const problemId of ids) {
    if (completed.has(problemId)) {
      console.log(`${problemId} | ${submittedAs} | ${language} | already completed; skipped`);
      continue;
    }
    let step = 'load solution files';
    try {
      const pair = getSolutions(model, language, problemId);

      step = 'open Dashboard';
      browserErrors.length = 0;
      await page.goto('/');
      await page.getByRole('heading', { name: 'Dashboard' }).waitFor({ state: 'visible' });

      step = 'navigate to Solve Problems';
      await page.getByRole('button', { name: 'Solve Problems' }).click();
      await page.getByRole('heading', { name: 'Solve Problems' }).waitFor({ state: 'visible' });

      const selects = page.locator('.problem-meta').getByRole('combobox');
      step = 'select and verify problem';
      const problemSelect = selects.first();
      await problemSelect.selectOption(problemId);
      await expectValue(problemSelect, problemId);

      step = 'select and verify language';
      const languageSelect = selects.nth(1);
      await languageSelect.selectOption(language);
      await expectValue(languageSelect, language);

      const aiPanel = page.locator('.editor-panel').filter({ hasText: 'AI-Written Solution' });
      const humanPanel = page.locator('.editor-panel').filter({ hasText: 'Human-Written Solution' });
      step = 'select and verify AI model';
      const modelInput = aiPanel.locator('input[type="text"]');
      await modelInput.fill(submittedAs);
      if (await modelInput.inputValue() !== submittedAs) throw new Error(`AI System Name did not retain ${submittedAs}`);

      step = 'fill AI and human editors';
      const aiEditor = aiPanel.locator('[contenteditable="true"][role="textbox"]');
      const humanEditor = humanPanel.locator('[contenteditable="true"][role="textbox"]');
      await pasteCode(page, aiEditor, pair.ai);
      await pasteCode(page, humanEditor, pair.human);
      if (normalizeCode(await editorValue(aiEditor)) !== normalizeCode(pair.ai)) throw new Error('AI editor content does not match the mapped solution');
      if (normalizeCode(await editorValue(humanEditor)) !== normalizeCode(pair.human)) throw new Error('Human editor content does not match the mapped solution');

      step = 'submit comparison';
      const submitResponsePromise = page.waitForResponse((response) =>
        response.request().method() === 'POST'
          && new URL(response.url()).pathname === '/api/comparisons',
      );
      await page.getByRole('button', { name: 'Submit & Compare' }).click();
      const submitResponse = await submitResponsePromise;
      if (!submitResponse.ok()) {
        const responseBody = (await submitResponse.text()).slice(0, 1200);
        throw new Error(`Submit returned HTTP ${submitResponse.status()}: ${responseBody}`);
      }

      step = 'wait for completed evaluation';
      await page.getByRole('heading', { name: /^Comparison Report #\d+$/ }).waitFor({ state: 'visible' });
      await page.getByText(new RegExp(`AI: ${escapeRegExp(submittedAs)}`)).waitFor({ state: 'visible' });
      if (browserErrors.length) throw new Error(browserErrors.join('; '));
      console.log(`${problemId} | ${submittedAs} | ${language} | completed`);
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      const failure = `${problemId} | ${submittedAs} | ${language} | ${step} | ${message}`;
      failures.push(failure);
      console.error(`FAILED ${failure}`);
    }
  }

  if (failures.length) {
    throw new Error(`Batch finished with ${failures.length} failed problem(s):\n${failures.join('\n')}`);
  }
}

async function expectValue(locator, expected) {
  const actual = await locator.inputValue();
  if (actual !== expected) throw new Error(`Expected '${expected}', selected '${actual || '(empty)'}'`);
}

async function editorValue(locator) {
  return locator.evaluate((element) => {
    if (element instanceof HTMLElement && element.classList.contains('cm-content')) {
      return Array.from(element.querySelectorAll('.cm-line'), (line) => line.textContent ?? '').join('\n');
    }
    return element.value ?? element.innerText ?? element.textContent ?? '';
  });
}

async function pasteCode(page, editor, source) {
  await page.evaluate((value) => navigator.clipboard.writeText(value), source);
  await editor.click();
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Control+V');
}

function normalizeCode(source) {
  return source.replace(/\r\n?/g, '\n');
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

module.exports = { getSolutions, problemIds, runBatch };
