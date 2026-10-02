// P001
function twoSum(nums, target) {
  const seen = new Map();
  for (let i = 0; i < nums.length; i++) {
    const complement = target - nums[i];
    if (seen.has(complement)) {
      return [seen.get(complement), i];
    }
    if (!seen.has(nums[i])) {
      seen.set(nums[i], i);
    }
  }
  return [];
}

// P002
function maxSubarray(nums) {
  if (nums.length === 0) {
    return 0;
  }
  let best = nums[0];
  let current = nums[0];
  for (let i = 1; i < nums.length; i++) {
    current = Math.max(nums[i], current + nums[i]);
    best = Math.max(best, current);
  }
  return best;
}

// P003
function binarySearch(nums, target) {
  let low = 0;
  let high = nums.length - 1;
  while (low <= high) {
    const mid = low + Math.floor((high - low) / 2);
    if (nums[mid] === target) {
      return mid;
    }
    if (nums[mid] < target) {
      low = mid + 1;
    } else {
      high = mid - 1;
    }
  }
  return -1;
}

// P004
function mergeSortedArrays(nums1, nums2) {
  const merged = [];
  let i = 0;
  let j = 0;
  while (i < nums1.length && j < nums2.length) {
    if (nums1[i] <= nums2[j]) {
      merged.push(nums1[i++]);
    } else {
      merged.push(nums2[j++]);
    }
  }
  while (i < nums1.length) {
    merged.push(nums1[i++]);
  }
  while (j < nums2.length) {
    merged.push(nums2[j++]);
  }
  return merged;
}

// P005
function isBalanced(s) {
  const closing = { ')': '(', ']': '[', '}': '{' };
  const stack = [];
  for (const ch of s) {
    if (ch === '(' || ch === '[' || ch === '{') {
      stack.push(ch);
    } else if (ch === ')' || ch === ']' || ch === '}') {
      if (stack.length === 0 || stack.pop() !== closing[ch]) {
        return false;
      }
    } else {
      return false;
    }
  }
  return stack.length === 0;
}

// P006
function csvFieldCount(line) {
  let count = 1;
  let inQuotes = false;
  for (const ch of line) {
    if (ch === '"') {
      inQuotes = !inQuotes;
    } else if (ch === ',' && !inQuotes) {
      count++;
    }
  }
  return count;
}

// P007
function countLogLevels(log) {
  const counts = { ERROR: 0, WARNING: 0, INFO: 0, DEBUG: 0 };
  for (const line of log.split(/\r\n|\r|\n/)) {
    for (const level of ['ERROR', 'WARNING', 'INFO', 'DEBUG']) {
      if (
        line.startsWith(level) &&
        (line.length === level.length || line[level.length] === ' ' || line[level.length] === ':')
      ) {
        counts[level]++;
        break;
      }
    }
  }
  return counts;
}

// P008
function parseKeyValue(s) {
  const entries = new Map();
  for (const pair of s.split(',')) {
    const eq = pair.indexOf('=');
    if (eq < 0) {
      continue;
    }
    entries.set(pair.slice(0, eq).trim(), pair.slice(eq + 1).trim());
  }
  const sortedKeys = Array.from(entries.keys()).sort();
  const result = {};
  for (const key of sortedKeys) {
    Object.defineProperty(result, key, {
      value: entries.get(key),
      enumerable: true,
      writable: true,
      configurable: true,
    });
  }
  return result;
}

// P009
function normalizeDate(date) {
  let year;
  let month;
  let day;
  if (date.includes('/')) {
    [month, day, year] = date.split('/');
  } else if (date.includes('-')) {
    [day, month, year] = date.split('-');
  } else {
    [year, month, day] = date.split('.');
  }
  return `${year.padStart(4, '0')}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
}

// P010
function wordFrequency(text) {
  const counts = new Map();
  const words = text.match(/[A-Za-z]+/g) || [];
  for (const rawWord of words) {
    const word = rawWord.toLowerCase();
    counts.set(word, (counts.get(word) || 0) + 1);
  }
  const ordered = Array.from(counts.entries()).sort((a, b) => {
    if (a[1] !== b[1]) {
      return b[1] - a[1];
    }
    return a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0;
  });
  const result = {};
  for (const [word, count] of ordered) {
    result[word] = count;
  }
  return result;
}

// P011
function isValidEmail(email) {
  const atIndex = email.indexOf('@');
  if (atIndex < 0 || email.indexOf('@', atIndex + 1) >= 0) {
    return false;
  }
  const local = email.slice(0, atIndex);
  const domain = email.slice(atIndex + 1);
  if (!/^[A-Za-z0-9._%+-]+$/.test(local)) {
    return false;
  }
  if (local.startsWith('.') || local.endsWith('.') || local.includes('..')) {
    return false;
  }
  const labels = domain.split('.');
  if (labels.length < 2) {
    return false;
  }
  for (const label of labels) {
    if (!/^[A-Za-z0-9-]+$/.test(label)) {
      return false;
    }
    if (label.startsWith('-') || label.endsWith('-')) {
      return false;
    }
  }
  return /^[A-Za-z]{2,6}$/.test(labels[labels.length - 1]);
}

// P012
function isValidPassword(password) {
  return (
    password.length >= 8 &&
    /[A-Z]/.test(password) &&
    /[a-z]/.test(password) &&
    /[0-9]/.test(password) &&
    /[!@#$%^&*]/.test(password)
  );
}

// P013
function isValidRange(s) {
  const parts = s.split('|');
  if (parts.length !== 3) {
    return 'INVALID';
  }
  for (const part of parts) {
    if (!/^[+-]?[0-9]+$/.test(part)) {
      return 'INVALID';
    }
  }
  const [value, min, max] = parts.map((part) => BigInt(part));
  return value >= min && value <= max ? 'VALID' : 'INVALID';
}

// P014
function isValidIPv4(ip) {
  const octets = ip.split('.');
  if (octets.length !== 4) {
    return false;
  }
  for (const octet of octets) {
    if (!/^(0|[1-9][0-9]{0,2})$/.test(octet)) {
      return false;
    }
    if (Number(octet) > 255) {
      return false;
    }
  }
  return true;
}

// P015
function isValidUsername(username) {
  return /^[A-Za-z][A-Za-z0-9_-]{2,19}$/.test(username);
}

// P016
function escapeHtml(s) {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// P017
function escapeCsvCell(s) {
  if (/[,"\n\r]/.test(s)) {
    return '"' + s.replace(/"/g, '""') + '"';
  }
  return s;
}

// P018
function escapeJsonString(s) {
  const table = {
    '"': '\\"',
    '\\': '\\\\',
    '/': '\\/',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
  };
  let result = '';
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    if (Object.prototype.hasOwnProperty.call(table, ch)) {
      result += table[ch];
    } else if (s.charCodeAt(i) < 0x20) {
      result += '\\u' + s.charCodeAt(i).toString(16).padStart(4, '0');
    } else {
      result += ch;
    }
  }
  return result;
}

// P019
function encodeUrlComponent(s) {
  const bytes = new TextEncoder().encode(s);
  let result = '';
  for (const byte of bytes) {
    const isUnreserved =
      (byte >= 0x41 && byte <= 0x5a) ||
      (byte >= 0x61 && byte <= 0x7a) ||
      (byte >= 0x30 && byte <= 0x39) ||
      byte === 0x2d ||
      byte === 0x5f ||
      byte === 0x2e ||
      byte === 0x7e;
    if (isUnreserved) {
      result += String.fromCharCode(byte);
    } else {
      result += '%' + byte.toString(16).toUpperCase().padStart(2, '0');
    }
  }
  return result;
}

// P020
function sanitizeTemplate(s) {
  let result = '';
  let pos = 0;
  while (pos < s.length) {
    const open = s.indexOf('{{', pos);
    if (open < 0) {
      result += s.slice(pos);
      break;
    }
    const close = s.indexOf('}}', open + 2);
    if (close < 0) {
      result += s.slice(pos);
      break;
    }
    result += s.slice(pos, open);
    const key = s.slice(open + 2, close);
    if (/^[a-zA-Z0-9_]+$/.test(key)) {
      result += s.slice(open, close + 2);
    }
    pos = close + 2;
  }
  return result;
}

// P021
function safePathNormalize(path) {
  if (path.trim() === '' || path.includes('\\')) {
    return '';
  }
  const resolved = [];
  for (const segment of path.split('/')) {
    if (segment === '' || segment === '.') {
      continue;
    }
    if (segment === '..') {
      if (resolved.length === 0) {
        return '';
      }
      resolved.pop();
    } else {
      resolved.push(segment);
    }
  }
  return resolved.join('/');
}

// P022
function isAllowedExtension(path) {
  const allowed = new Set(['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt', '.csv']);
  const separatorIndex = Math.max(path.lastIndexOf('/'), path.lastIndexOf('\\'));
  const filename = path.slice(separatorIndex + 1);
  const dotIndex = filename.lastIndexOf('.');
  if (dotIndex <= 0) {
    return false;
  }
  return allowed.has(filename.slice(dotIndex).toLowerCase());
}

// P023
function sanitizeFilename(name) {
  const truncated = Array.from(name).slice(0, 200).join('');
  let cleaned = truncated.replace(/[^a-zA-Z0-9._-]/gu, '_');
  cleaned = cleaned.replace(/_+/g, '_').replace(/^_+|_+$/g, '');
  return cleaned === '' ? '_' : cleaned;
}

// P024
function checkArchiveEntry(path) {
  if (path === '') {
    return 'safe';
  }
  if (path.startsWith('/') || path.includes('\\')) {
    return 'unsafe';
  }
  let depth = 0;
  for (const segment of path.split('/')) {
    if (segment === '' || segment === '.') {
      continue;
    }
    if (segment === '..') {
      depth--;
      if (depth < 0) {
        return 'unsafe';
      }
    } else {
      depth++;
    }
  }
  return 'safe';
}

// P025
function isAllowedFiletype(ext) {
  const allowed = new Set(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'pdf', 'txt', 'csv', 'json', 'xml']);
  const value = ext.startsWith('.') ? ext.slice(1) : ext;
  if (value === '') {
    return false;
  }
  return allowed.has(value.toLowerCase());
}

// P026
function isValidSqlIdentifier(name) {
  return /^[a-zA-Z_][a-zA-Z0-9_]{0,63}$/.test(name);
}

// P027
function escapeSqlString(s) {
  return s.replace(/\\/g, '\\\\').replace(/'/g, "''");
}

// P028
function buildParamQuery(s) {
  const bar = s.indexOf('|');
  if (bar < 0 || s.indexOf('|', bar + 1) >= 0) {
    return 'INVALID';
  }
  const table = s.slice(0, bar);
  const conditions = s.slice(bar + 1);
  const identifier = /^[a-zA-Z_][a-zA-Z0-9_]*$/;
  if (!identifier.test(table) || conditions === '') {
    return 'INVALID';
  }
  const clauses = [];
  for (const condition of conditions.split(',')) {
    const eq = condition.indexOf('=');
    if (eq < 0) {
      return 'INVALID';
    }
    const column = condition.slice(0, eq);
    if (!identifier.test(column)) {
      return 'INVALID';
    }
    clauses.push(`${column}=?`);
  }
  return `SELECT * FROM ${table} WHERE ${clauses.join(' AND ')}`;
}

// P029
function validateSortDirection(s) {
  const direction = s.trim().toUpperCase();
  return direction === 'ASC' || direction === 'DESC' ? direction : 'INVALID';
}

// P030
function isAllowedColumn(col) {
  const allowed = new Set(['id', 'name', 'email', 'created_at', 'status', 'age', 'role', 'score']);
  return allowed.has(col.trim());
}

// P031
function quoteShellArg(s) {
  return "'" + s.split("'").join("'\\''") + "'";
}

// P032
function isAllowedCommand(s) {
  const allowed = new Set(['ls', 'cat', 'echo', 'grep', 'find', 'sort', 'uniq', 'wc', 'head', 'tail']);
  const command = s.trim();
  if (command.includes(' ')) {
    return false;
  }
  return allowed.has(command);
}

// P033
function detectShellMeta(s) {
  return /[;|&$`><(){}\\"'\n\r]/.test(s) ? 'unsafe' : 'safe';
}

// P034
function isValidEnvVar(name) {
  return /^[A-Z_][A-Z0-9_]{0,63}$/.test(name);
}

// P035
function splitArgs(s) {
  const tokens = [];
  let current = '';
  let inQuotes = false;
  let hasToken = false;
  for (const ch of s) {
    if (ch === '"') {
      inQuotes = !inQuotes;
      hasToken = true;
    } else if (ch === ' ' && !inQuotes) {
      if (hasToken) {
        tokens.push(current);
        current = '';
        hasToken = false;
      }
    } else {
      current += ch;
      hasToken = true;
    }
  }
  if (hasToken) {
    tokens.push(current);
  }
  return tokens;
}

// P036
function parseSafeLiteral(s) {
  if (/^-?(0|[1-9][0-9]*)$/.test(s)) {
    return s === '-0' ? '0' : s;
  }
  if (s === 'true' || s === 'false' || s === 'null') {
    return s;
  }
  if (s.length >= 2 && s[0] === '"' && s[s.length - 1] === '"') {
    const inner = s.slice(1, -1);
    let result = '';
    let i = 0;
    while (i < inner.length) {
      const ch = inner[i];
      if (ch === '\\') {
        if (i + 1 < inner.length && inner[i + 1] === '"') {
          result += '"';
          i += 2;
          continue;
        }
        return 'INVALID';
      }
      if (ch === '"') {
        return 'INVALID';
      }
      result += ch;
      i++;
    }
    return result;
  }
  return 'INVALID';
}

// P037
function parseConfigBool(s) {
  const value = s.trim().toLowerCase();
  if (['true', 'yes', '1', 'on', 'enabled'].includes(value)) {
    return 'true';
  }
  if (['false', 'no', '0', 'off', 'disabled'].includes(value)) {
    return 'false';
  }
  return 'INVALID';
}

// P038
function isAllowedConfigKey(key) {
  const allowed = new Set([
    'host', 'port', 'database', 'username', 'password',
    'timeout', 'max_connections', 'ssl_enabled', 'log_level', 'retry_count',
  ]);
  return allowed.has(key.trim());
}

// P039
function validateToken(s) {
  const parts = s.split('.');
  if (parts.length !== 3) {
    return 'invalid';
  }
  const valid =
    /^[A-Za-z0-9_-]+$/.test(parts[0]) &&
    /^[A-Za-z0-9_-]+$/.test(parts[1]) &&
    /^[0-9a-f]{8}$/.test(parts[2]);
  return valid ? 'valid' : 'invalid';
}

// P040
function validateNumericExpr(s) {
  const n = s.length;
  const isDigit = (ch) => ch >= '0' && ch <= '9';
  let i = 0;
  while (true) {
    if (i < n && s[i] === '-') {
      i++;
    }
    if (i >= n || !isDigit(s[i])) {
      return 'invalid';
    }
    if (s[i] === '0') {
      i++;
      if (i < n && isDigit(s[i])) {
        return 'invalid';
      }
    } else {
      while (i < n && isDigit(s[i])) {
        i++;
      }
    }
    const afterNumber = i;
    while (i < n && s[i] === ' ') {
      i++;
    }
    if (i === n) {
      return afterNumber === n ? 'valid' : 'invalid';
    }
    if (s[i] !== '+' && s[i] !== '-' && s[i] !== '*' && s[i] !== '/') {
      return 'invalid';
    }
    i++;
    while (i < n && s[i] === ' ') {
      i++;
    }
  }
}

// P041
function frequencyCounter(nums) {
  const counts = new Map();
  for (const value of nums) {
    counts.set(value, (counts.get(value) || 0) + 1);
  }
  const result = {};
  for (const key of Array.from(counts.keys()).sort((a, b) => a - b)) {
    result[key] = counts.get(key);
  }
  return result;
}

// P042
function hasDuplicate(nums) {
  return new Set(nums).size !== nums.length;
}

// P043
function streamingSum(nums) {
  let total = 0;
  for (const value of nums) {
    total += value;
  }
  return total;
}

// P044
function boundedLogProcessor(log, maxLines) {
  let kept = 0;
  let totalWords = 0;
  if (maxLines > 0) {
    for (const line of log.split(/\r\n|\r|\n/)) {
      if (kept >= maxLines) {
        break;
      }
      const words = line.split(/\s+/).filter((word) => word !== '');
      if (words.length === 0) {
        continue;
      }
      kept++;
      totalWords += words.length;
    }
  }
  return { kept, total_words: totalWords };
}

// P045
function topKFrequent(nums, k) {
  if (k <= 0 || nums.length === 0) {
    return [];
  }
  const counts = new Map();
  for (const value of nums) {
    counts.set(value, (counts.get(value) || 0) + 1);
  }
  const ranked = Array.from(counts.entries()).sort((a, b) => {
    if (a[1] !== b[1]) {
      return b[1] - a[1];
    }
    return a[0] - b[0];
  });
  return ranked
    .slice(0, k)
    .map((entry) => entry[0])
    .sort((a, b) => a - b);
}

// P046
function validateTokenFormat(token) {
  return /^[a-zA-Z][a-zA-Z0-9-]{7,31}$/.test(token) ? 'valid' : 'invalid';
}

// P047
function evaluatePermission(role, action) {
  const permissions = new Map([
    ['admin', ['read', 'write', 'delete', 'execute']],
    ['editor', ['read', 'write']],
    ['viewer', ['read']],
    ['guest', []],
  ]);
  const granted = permissions.get(role);
  return granted !== undefined && granted.includes(action) ? 'allowed' : 'denied';
}

// P048
function roleHasPermission(role, permission) {
  const permissions = new Map([
    ['admin', ['read', 'write', 'delete', 'execute']],
    ['editor', ['read', 'write']],
    ['viewer', ['read']],
    ['guest', []],
  ]);
  const granted = permissions.get(role);
  return granted !== undefined && granted.includes(permission);
}

// P049
function checkSession(lastActive, currentTime, timeout) {
  if (currentTime < lastActive) {
    return 'invalid';
  }
  const elapsed = currentTime - lastActive;
  return elapsed > timeout ? 'expired' : 'active';
}

// P050
function validateScope(requested, allowed) {
  const allowedScopes = new Set(allowed);
  const parts = requested.split(':');
  for (let end = 1; end <= parts.length; end++) {
    if (allowedScopes.has(parts.slice(0, end).join(':'))) {
      return 'granted';
    }
  }
  return 'denied';
}

module.exports = {
  twoSum,
  maxSubarray,
  binarySearch,
  mergeSortedArrays,
  isBalanced,
  csvFieldCount,
  countLogLevels,
  parseKeyValue,
  normalizeDate,
  wordFrequency,
  isValidEmail,
  isValidPassword,
  isValidRange,
  isValidIPv4,
  isValidUsername,
  escapeHtml,
  escapeCsvCell,
  escapeJsonString,
  encodeUrlComponent,
  sanitizeTemplate,
  safePathNormalize,
  isAllowedExtension,
  sanitizeFilename,
  checkArchiveEntry,
  isAllowedFiletype,
  isValidSqlIdentifier,
  escapeSqlString,
  buildParamQuery,
  validateSortDirection,
  isAllowedColumn,
  quoteShellArg,
  isAllowedCommand,
  detectShellMeta,
  isValidEnvVar,
  splitArgs,
  parseSafeLiteral,
  parseConfigBool,
  isAllowedConfigKey,
  validateToken,
  validateNumericExpr,
  frequencyCounter,
  hasDuplicate,
  streamingSum,
  boundedLogProcessor,
  topKFrequent,
  validateTokenFormat,
  evaluatePermission,
  roleHasPermission,
  checkSession,
  validateScope,
};
