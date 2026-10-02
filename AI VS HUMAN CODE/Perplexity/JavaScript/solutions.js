// P001: Two Sum
function twoSum(nums, target) {
    const seen = {};
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (seen.hasOwnProperty(complement)) {
            const result = [seen[complement], i];
            result.sort((a, b) => a - b);
            return result;
        }
        seen[nums[i]] = i;
    }
    return [];
}

// P002: Maximum Subarray Sum
function maxSubarray(nums) {
    let maxSum = nums[0];
    let currentSum = nums[0];
    for (let i = 1; i < nums.length; i++) {
        currentSum = Math.max(nums[i], currentSum + nums[i]);
        maxSum = Math.max(maxSum, currentSum);
    }
    return maxSum;
}

// P003: Binary Search
function binarySearch(nums, target) {
    let left = 0, right = nums.length - 1;
    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        if (nums[mid] === target) return mid;
        else if (nums[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

// P004: Merge Sorted Arrays
function mergeSortedArrays(nums1, nums2) {
    const result = [];
    let i = 0, j = 0;
    while (i < nums1.length && j < nums2.length) {
        if (nums1[i] <= nums2[j]) result.push(nums1[i++]);
        else result.push(nums2[j++]);
    }
    while (i < nums1.length) result.push(nums1[i++]);
    while (j < nums2.length) result.push(nums2[j++]);
    return result;
}

// P005: Balanced Brackets
function isBalanced(s) {
    const stack = [];
    const pairs = { ')': '(', '}': '{', ']': '[' };
    for (const c of s) {
        if (c === '(' || c === '{' || c === '[') stack.push(c);
        else if (c === ')' || c === '}' || c === ']') {
            if (stack.length === 0 || stack[stack.length - 1] !== pairs[c]) return false;
            stack.pop();
        }
    }
    return stack.length === 0;
}

// P006: CSV Record Field Count
function csvFieldCount(line) {
    if (!line) return 0;
    let count = 0;
    let inQuotes = false;
    for (let i = 0; i < line.length; i++) {
        const c = line[i];
        if (c === '"') {
            if (inQuotes && i + 1 < line.length && line[i + 1] === '"') i++;
            else inQuotes = !inQuotes;
        } else if (c === ',' && !inQuotes) count++;
    }
    return count + 1;
}

// P007: Log Level Counter
function countLogLevels(log) {
    const result = { ERROR: 0, WARNING: 0, INFO: 0, DEBUG: 0 };
    if (!log) return result;
    const lines = log.split('\n');
    for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('ERROR ') || trimmed.startsWith('ERROR:')) result.ERROR++;
        else if (trimmed.startsWith('WARNING ') || trimmed.startsWith('WARNING:')) result.WARNING++;
        else if (trimmed.startsWith('INFO ') || trimmed.startsWith('INFO:')) result.INFO++;
        else if (trimmed.startsWith('DEBUG ') || trimmed.startsWith('DEBUG:')) result.DEBUG++;
    }
    return result;
}

// P008: Key-Value Parser
function parseKeyValue(s) {
    const result = {};
    if (!s) return result;
    const pairs = s.split(',');
    for (const pair of pairs) {
        const eq = pair.indexOf('=');
        if (eq !== -1) {
            const key = pair.substring(0, eq).trim();
            const value = pair.substring(eq + 1).trim();
            result[key] = value;
        }
    }
    const sorted = {};
    Object.keys(result).sort().forEach(k => sorted[k] = result[k]);
    return sorted;
}

// P009: Date Format Normalizer
function normalizeDate(date) {
    if (date.includes('/')) {
        const [mm, dd, yyyy] = date.split('/');
        return `${yyyy}-${mm}-${dd}`;
    } else if (date.includes('-')) {
        const [dd, mm, yyyy] = date.split('-');
        return `${yyyy}-${mm}-${dd}`;
    } else if (date.includes('.')) {
        const [yyyy, mm, dd] = date.split('.');
        return `${yyyy}-${mm}-${dd}`;
    }
    return date;
}

// P010: Word Frequency
function wordFrequency(text) {
    const freq = {};
    if (!text) return freq;
    let word = '';
    for (const c of text) {
        if (/[a-zA-Z]/.test(c)) word += c.toLowerCase();
        else if (word) {
            freq[word] = (freq[word] || 0) + 1;
            word = '';
        }
    }
    if (word) freq[word] = (freq[word] || 0) + 1;
    return freq;
}

// P011: Email Validator
function isValidEmail(email) {
    if (!email) return false;
    const atCount = (email.match(/@/g) || []).length;
    if (atCount !== 1) return false;
    const [local, domain] = email.split('@');
    if (!local || local.startsWith('.') || local.endsWith('.') || local.includes('..')) return false;
    for (const c of local) {
        if (!/[a-zA-Z0-9._%+-]/.test(c)) return false;
    }
    if (!domain || domain.startsWith('.') || domain.endsWith('.')) return false;
    const labels = domain.split('.');
    if (labels.length < 2) return false;
    const tld = labels[labels.length - 1];
    if (!/^[a-zA-Z]{2,6}$/.test(tld)) return false;
    for (const label of labels) {
        if (!label || label.startsWith('-') || label.endsWith('-')) return false;
    }
    return true;
}

// P012: Password Policy Validator
function isValidPassword(password) {
    if (!password || password.length < 8) return false;
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasDigit = /[0-9]/.test(password);
    const hasSpecial = /[!@#$%^&*]/.test(password);
    return hasUpper && hasLower && hasDigit && hasSpecial;
}

// P013: Integer Range Validator
function isValidRange(s) {
    if (!s) return "INVALID";
    const parts = s.split('|');
    if (parts.length !== 3) return "INVALID";
    const value = parseInt(parts[0], 10);
    const minVal = parseInt(parts[1], 10);
    const maxVal = parseInt(parts[2], 10);
    if (isNaN(value) || isNaN(minVal) || isNaN(maxVal)) return "INVALID";
    return (minVal <= value && value <= maxVal) ? "VALID" : "INVALID";
}

// P014: IPv4 Validator
function isValidIPv4(ip) {
    if (!ip) return false;
    const parts = ip.split('.');
    if (parts.length !== 4) return false;
    for (const part of parts) {
        if (!part || part.length > 3) return false;
        if (!/^\d+$/.test(part)) return false;
        if (part.length > 1 && part[0] === '0') return false;
        const num = parseInt(part, 10);
        if (num < 0 || num > 255) return false;
    }
    return true;
}

// P015: Username Validator
function isValidUsername(username) {
    if (!username || username.length < 3 || username.length > 20) return false;
    if (!/^[a-zA-Z]/.test(username[0])) return false;
    return /^[a-zA-Z0-9_-]+$/.test(username);
}

// P016: HTML Text Escaper
function escapeHtml(s) {
    if (!s) return "";
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

// P017: CSV Cell Escaper
function escapeCsvCell(s) {
    if (!s) return "";
    const needsQuoting = /[,"\n\r]/.test(s);
    if (!needsQuoting) return s;
    const escaped = s.replace(/"/g, '""');
    return `"${escaped}"`;
}

// P018: JSON String Escaper
function escapeJsonString(s) {
    if (!s) return "";
    let result = '';
    for (const c of s) {
        if (c === '"') result += '\\"';
        else if (c === '\\') result += '\\\\';
        else if (c === '/') result += '\\/';
        else if (c === '\b') result += '\\b';
        else if (c === '\f') result += '\\f';
        else if (c === '\n') result += '\\n';
        else if (c === '\r') result += '\\r';
        else if (c === '\t') result += '\\t';
        else if (c.charCodeAt(0) < 0x20) result += '\\u' + c.charCodeAt(0).toString(16).padStart(4, '0');
        else result += c;
    }
    return result;
}

// P019: URL Query Component Encoder
function encodeUrlComponent(s) {
    if (!s) return "";
    const unreserved = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~';
    let result = '';
    for (const c of s) {
        if (unreserved.includes(c)) result += c;
        else {
            const bytes = new TextEncoder().encode(c);
            for (const b of bytes) result += '%' + b.toString(16).toUpperCase().padStart(2, '0');
        }
    }
    return result;
}

// P020: Template Placeholder Sanitizer
function sanitizeTemplate(s) {
    if (!s) return "";
    return s.replace(/\{\{([^}]*)\}\}/g, (match, key) => {
        if (key && /^[a-zA-Z0-9_]+$/.test(key)) return match;
        return '';
    });
}

// P021: Safe Path Normalizer
function safePathNormalize(path) {
    if (!path || path.trim() === '') return '';
    if (path.includes('\\')) return '';
    const segments = path.split('/');
    const result = [];
    for (const seg of segments) {
        if (seg === '' || seg === '.') continue;
        if (seg === '..') {
            if (result.length === 0) return '';
            result.pop();
        } else {
            result.push(seg);
        }
    }
    return result.join('/');
}

// P022: Path Extension Validator
function isAllowedExtension(path) {
    if (!path) return false;
    const allowed = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt', '.csv'];
    const filename = path.replace(/\\/g, '/').split('/').pop();
    const dot = filename.lastIndexOf('.');
    if (dot <= 0) return false;
    const ext = '.' + filename.substring(dot + 1).toLowerCase();
    return allowed.includes(ext);
}

// P023: Filename Sanitizer
function sanitizeFilename(name) {
    if (!name) return '_';
    name = name.substring(0, 200);
    let result = '';
    for (const c of name) {
        result += /[a-zA-Z0-9._-]/.test(c) ? c : '_';
    }
    result = result.replace(/_+/g, '_').replace(/^_|_$/g, '');
    return result || '_';
}

// P024: Archive Entry Path Checker
function checkArchiveEntry(path) {
    if (!path) return "safe";
    if (path.startsWith('/')) return "unsafe";
    if (path.includes('\\')) return "unsafe";
    let depth = 0;
    const segments = path.split('/');
    for (const seg of segments) {
        if (seg === '' || seg === '.') continue;
        if (seg === '..') {
            depth--;
            if (depth < 0) return "unsafe";
        } else {
            depth++;
        }
    }
    return "safe";
}

// P025: File Type Allowlist
function isAllowedFiletype(ext) {
    if (!ext) return false;
    const allowed = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'pdf', 'txt', 'csv', 'json', 'xml'];
    ext = ext.toLowerCase().replace(/^\./, '');
    return allowed.includes(ext);
}

// P026: SQL Identifier Validator
function isValidSqlIdentifier(name) {
    if (!name || name.length < 1 || name.length > 64) return false;
    if (!/^[a-zA-Z_]/.test(name[0])) return false;
    return /^[a-zA-Z0-9_]+$/.test(name);
}

// P027: SQL String Literal Escaper
function escapeSqlString(s) {
    if (!s) return "";
    return s.replace(/\\/g, '\\\\').replace(/'/g, "''");
}

// P028: Parameterized Query Builder
function buildParamQuery(s) {
    if (!s) return "INVALID";
    const pipe = s.indexOf('|');
    if (pipe === -1) return "INVALID";
    const table = s.substring(0, pipe);
    const conditions = s.substring(pipe + 1);
    if (!isValidSqlIdentifier(table)) return "INVALID";
    if (!conditions) return "INVALID";
    const condPairs = conditions.split(',');
    const cols = [];
    for (const pair of condPairs) {
        const eq = pair.indexOf('=');
        if (eq === -1) return "INVALID";
        const col = pair.substring(0, eq);
        if (!isValidSqlIdentifier(col)) return "INVALID";
        cols.push(col);
    }
    if (cols.length === 0) return "INVALID";
    const where = cols.map(c => `${c}=?`).join(' AND ');
    return `SELECT * FROM ${table} WHERE ${where}`;
}

// P029: Sort Direction Validator
function validateSortDirection(s) {
    if (!s) return "INVALID";
    const trimmed = s.trim().toUpperCase();
    if (trimmed === 'ASC' || trimmed === 'DESC') return trimmed;
    return "INVALID";
}

// P030: Column Allowlist Checker
function isAllowedColumn(col) {
    if (!col) return false;
    const allowed = ['id', 'name', 'email', 'created_at', 'status', 'age', 'role', 'score'];
    return allowed.includes(col.trim());
}

// P031: Shell Argument Quoter
function quoteShellArg(s) {
    if (!s) s = '';
    const escaped = s.replace(/'/g, "'\\''");
    return `'${escaped}'`;
}

// P032: Command Name Allowlist
function isAllowedCommand(s) {
    if (!s) return false;
    const allowed = ['ls', 'cat', 'echo', 'grep', 'find', 'sort', 'uniq', 'wc', 'head', 'tail'];
    const trimmed = s.trim();
    if (trimmed !== trimmed.replace(/\s+/g, '')) return false;
    return allowed.includes(trimmed);
}

// P033: Shell Metacharacter Detector
function detectShellMeta(s) {
    if (!s) return "safe";
    const dangerous = ';|&$`><(){}\\"\'\n\r';
    for (const c of s) {
        if (dangerous.includes(c)) return "unsafe";
    }
    return "safe";
}

// P034: Environment Variable Name Validator
function isValidEnvVar(name) {
    if (!name || name.length < 1 || name.length > 64) return false;
    if (!/^[A-Z_]/.test(name[0])) return false;
    return /^[A-Z0-9_]+$/.test(name);
}

// P035: Command Argument Splitter
function splitArgs(s) {
    if (!s) return [];
    const result = [];
    let current = '';
    let inQuotes = false;
    for (const c of s) {
        if (c === '"') {
            if (inQuotes) {
                result.push(current);
                current = '';
                inQuotes = false;
            } else {
                if (current) {
                    result.push(current);
                    current = '';
                }
                inQuotes = true;
            }
        } else if (c === ' ' && !inQuotes) {
            if (current) {
                result.push(current);
                current = '';
            }
        } else {
            current += c;
        }
    }
    if (current) result.push(current);
    return result;
}

// P036: Safe Literal Parser
function parseSafeLiteral(s) {
    if (!s) return "INVALID";
    if (s === 'true' || s === 'false' || s === 'null') return s;
    let neg = false;
    let i = 0;
    if (s.startsWith('-')) {
        neg = true;
        i = 1;
    }
    if (i >= s.length) return "INVALID";
    let digits = '';
    for (; i < s.length; i++) {
        if (!/[0-9]/.test(s[i])) return "INVALID";
        digits += s[i];
    }
    if (!digits) return "INVALID";
    if ((digits.length > 1 && digits[0] === '0') || (neg && digits.length > 1 && digits[0] === '0')) return "INVALID";
    return (neg ? '-' : '') + digits;
}

// P037: Configuration Boolean Parser
function parseConfigBool(s) {
    if (!s) return "INVALID";
    const trimmed = s.trim().toLowerCase();
    if (['true', 'yes', '1', 'on', 'enabled'].includes(trimmed)) return "true";
    if (['false', 'no', '0', 'off', 'disabled'].includes(trimmed)) return "false";
    return "INVALID";
}

// P038: Configuration Key Allowlist
function isAllowedConfigKey(key) {
    if (!key) return false;
    const allowed = ['host', 'port', 'database', 'username', 'password', 'timeout', 'max_connections', 'ssl_enabled', 'log_level', 'retry_count'];
    return allowed.includes(key.trim());
}

// P039: Structured Token Decoder
function validateToken(s) {
    if (!s) return "invalid";
    const parts = s.split('.');
    if (parts.length !== 3) return "invalid";
    const [header, payload, checksum] = parts;
    if (!/^[A-Za-z0-9_-]+$/.test(header)) return "invalid";
    if (!/^[A-Za-z0-9_-]+$/.test(payload)) return "invalid";
    if (!/^[0-9a-f]{8}$/.test(checksum)) return "invalid";
    return "valid";
}

// P040: Safe Numeric Expression Validator
function validateNumericExpr(s) {
    if (!s || !s.trim()) return "invalid";
    const trimmed = s.replace(/\s+/g, '');
    if (!trimmed) return "invalid";
    const numPattern = '(0|-?[1-9][0-9]*)';
    const opPattern = '[+\\-*/]';
    const fullPattern = new RegExp(`^${numPattern}(${opPattern}${numPattern})*$`);
    return fullPattern.test(trimmed) ? "valid" : "invalid";
}

// P041: Frequency Counter Large Input
function frequencyCounter(nums) {
    const freq = {};
    if (!nums) return freq;
    for (const n of nums) {
        freq[n] = (freq[n] || 0) + 1;
    }
    const sorted = {};
    Object.keys(freq).sort((a, b) => parseInt(a) - parseInt(b)).forEach(k => sorted[k] = freq[k]);
    return sorted;
}

// P042: Duplicate Detector
function hasDuplicate(nums) {
    if (!nums || nums.length === 0) return false;
    const seen = new Set();
    for (const n of nums) {
        if (seen.has(n)) return true;
        seen.add(n);
    }
    return false;
}

// P043: Streaming Sum
function streamingSum(nums) {
    if (!nums) return 0;
    return nums.reduce((sum, n) => sum + n, 0);
}

// P044: Bounded Log Processor
function boundedLogProcessor(log, maxLines) {
    const result = { kept: 0, total_words: 0 };
    if (!log || maxLines <= 0) return result;
    const lines = log.split('\n');
    let kept = 0;
    for (const line of lines) {
        if (kept >= maxLines) break;
        const trimmed = line.trim();
        if (!trimmed) continue;
        kept++;
        result.total_words += trimmed.split(/\s+/).length;
    }
    result.kept = kept;
    return result;
}

// P045: Top-K Frequent Values
function topKFrequent(nums, k) {
    if (!nums || nums.length === 0 || k <= 0) return [];
    const freq = {};
    for (const n of nums) {
        freq[n] = (freq[n] || 0) + 1;
    }
    const items = Object.entries(freq).map(([num, count]) => ({ num: parseInt(num), count }));
    items.sort((a, b) => {
        if (b.count !== a.count) return b.count - a.count;
        return a.num - b.num;
    });
    const result = items.slice(0, k).map(item => item.num);
    result.sort((a, b) => a - b);
    return result;
}

// P046: Token Format Validator
function validateTokenFormat(token) {
    if (!token || token.length < 8 || token.length > 32) return "invalid";
    if (!/^[a-zA-Z]/.test(token[0])) return "invalid";
    if (!/^[a-zA-Z0-9\-]+$/.test(token)) return "invalid";
    return "valid";
}

// P047: Permission Rule Evaluator
function evaluatePermission(role, action) {
    const perms = {
        admin: new Set(['read', 'write', 'delete', 'execute']),
        editor: new Set(['read', 'write']),
        viewer: new Set(['read']),
        guest: new Set()
    };
    if (perms[role] && perms[role].has(action)) return "allowed";
    return "denied";
}

// P048: Role Permission Checker
function roleHasPermission(role, permission) {
    const perms = {
        admin: new Set(['read', 'write', 'delete', 'execute']),
        editor: new Set(['read', 'write']),
        viewer: new Set(['read']),
        guest: new Set()
    };
    return !!(perms[role] && perms[role].has(permission));
}

// P049: Session Timeout Checker
function checkSession(lastActive, currentTime, timeout) {
    if (currentTime < lastActive) return "invalid";
    const elapsed = currentTime - lastActive;
    return elapsed <= timeout ? "active" : "expired";
}

// P050: Access Scope Validator
function validateScope(requested, allowed) {
    if (!allowed || allowed.length === 0) return "denied";
    const allowedSet = new Set(allowed);
    if (allowedSet.has(requested)) return "granted";
    let pos = 0;
    while ((pos = requested.indexOf(':', pos)) !== -1) {
        const parent = requested.substring(0, pos);
        if (allowedSet.has(parent)) return "granted";
        pos++;
    }
    return "denied";
}

module.exports = {
    twoSum, maxSubarray, binarySearch, mergeSortedArrays, isBalanced, csvFieldCount,
    countLogLevels, parseKeyValue, normalizeDate, wordFrequency, isValidEmail,
    isValidPassword, isValidRange, isValidIPv4, isValidUsername, escapeHtml,
    escapeCsvCell, escapeJsonString, encodeUrlComponent, sanitizeTemplate,
    safePathNormalize, isAllowedExtension, sanitizeFilename, checkArchiveEntry,
    isAllowedFiletype, isValidSqlIdentifier, escapeSqlString, buildParamQuery,
    validateSortDirection, isAllowedColumn, quoteShellArg, isAllowedCommand,
    detectShellMeta, isValidEnvVar, splitArgs, parseSafeLiteral, parseConfigBool,
    isAllowedConfigKey, validateToken, validateNumericExpr, frequencyCounter,
    hasDuplicate, streamingSum, boundedLogProcessor, topKFrequent, validateTokenFormat,
    evaluatePermission, roleHasPermission, checkSession, validateScope
};