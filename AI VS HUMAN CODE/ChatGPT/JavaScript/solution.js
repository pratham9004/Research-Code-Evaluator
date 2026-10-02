// Research Code Evaluator - AI Generated Benchmark Solutions

// P001
function twoSum(nums, target) {
    const seen = new Map();
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (seen.has(complement)) {
            return [seen.get(complement), i].sort((a, b) => a - b);
        }
        seen.set(nums[i], i);
    }
    return [];
}

// P002
function maxSubarray(nums) {
    let current = nums[0];
    let best = nums[0];
    for (let i = 1; i < nums.length; i++) {
        current = Math.max(nums[i], current + nums[i]);
        best = Math.max(best, current);
    }
    return best;
}

// P003
function binarySearch(nums, target) {
    let left = 0;
    let right = nums.length - 1;
    while (left <= right) {
        const mid = left + Math.floor((right - left) / 2);
        if (nums[mid] === target) return mid;
        if (nums[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

// P004
function mergeSortedArrays(nums1, nums2) {
    const result = [];
    let i = 0;
    let j = 0;
    while (i < nums1.length && j < nums2.length) {
        if (nums1[i] <= nums2[j]) result.push(nums1[i++]);
        else result.push(nums2[j++]);
    }
    while (i < nums1.length) result.push(nums1[i++]);
    while (j < nums2.length) result.push(nums2[j++]);
    return result;
}

// P005
function isBalanced(s) {
    const stack = [];
    const pairs = { ')': '(', ']': '[', '}': '{' };
    for (const ch of s) {
        if (ch === '(' || ch === '[' || ch === '{') {
            stack.push(ch);
        } else {
            if (stack.length === 0 || stack.pop() !== pairs[ch]) return false;
        }
    }
    return stack.length === 0;
}

// P006
function csvFieldCount(line) {
    if (line.length === 0) return 1;
    let count = 1;
    let inQuotes = false;
    for (let i = 0; i < line.length; i++) {
        if (line[i] === '"') {
            if (inQuotes && i + 1 < line.length && line[i + 1] === '"') {
                i++;
            } else {
                inQuotes = !inQuotes;
            }
        } else if (line[i] === ',' && !inQuotes) {
            count++;
        }
    }
    return count;
}

// P007
function countLogLevels(log) {
    const counts = { ERROR: 0, WARNING: 0, INFO: 0, DEBUG: 0 };
    for (const line of log.split(/\r?\n/)) {
        for (const level of Object.keys(counts)) {
            if (line.startsWith(level) && line.length > level.length &&
                (line[level.length] === ' ' || line[level.length] === ':')) {
                counts[level]++;
                break;
            }
        }
    }
    return counts;
}

// P008
function parseKeyValue(s) {
    const result = {};
    if (s.length === 0) return result;
    for (const pair of s.split(',')) {
        const index = pair.indexOf('=');
        const key = pair.slice(0, index).trim();
        const value = pair.slice(index + 1).trim();
        result[key] = value;
    }
    return Object.fromEntries(Object.entries(result).sort(([a], [b]) => a.localeCompare(b)));
}

// P009
function normalizeDate(date) {
    let year;
    let month;
    let day;
    if (date.includes('/')) {
        const [m, d, y] = date.split('/');
        month = Number(m);
        day = Number(d);
        year = Number(y);
    } else if (date.includes('-')) {
        const [d, m, y] = date.split('-');
        day = Number(d);
        month = Number(m);
        year = Number(y);
    } else {
        const [y, m, d] = date.split('.');
        year = Number(y);
        month = Number(m);
        day = Number(d);
    }
    return `${String(year).padStart(4, '0')}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
}

// P010
function wordFrequency(text) {
    const counts = {};
    const matches = text.match(/[A-Za-z]+/g) || [];
    for (const raw of matches) {
        const word = raw.toLowerCase();
        counts[word] = (counts[word] || 0) + 1;
    }
    return counts;
}

// P011
function isValidEmail(email) {
    const at = email.indexOf('@');
    if (at === -1 || at !== email.lastIndexOf('@')) return false;
    const local = email.slice(0, at);
    const domain = email.slice(at + 1);
    if (!local || !domain || local.startsWith('.') || local.endsWith('.') || local.includes('..')) return false;
    if (!/^[a-zA-Z0-9._%+-]+$/.test(local)) return false;
    const labels = domain.split('.');
    for (const label of labels) {
        if (!label || label.startsWith('-') || label.endsWith('-') || !/^[A-Za-z0-9-]+$/.test(label)) return false;
    }
    const tld = labels[labels.length - 1];
    return /^[A-Za-z]{2,6}$/.test(tld);
}

// P012
function isValidPassword(password) {
    if (password.length < 8) return false;
    return /[A-Z]/.test(password) &&
           /[a-z]/.test(password) &&
           /[0-9]/.test(password) &&
           /[!@#$%^&*]/.test(password);
}

// P013
function isValidRange(s) {
    const parts = s.split('|');
    if (parts.length !== 3) return 'INVALID';
    if (!/^-?\d+$/.test(parts[0]) || !/^-?\d+$/.test(parts[1]) || !/^-?\d+$/.test(parts[2])) {
        return 'INVALID';
    }
    const value = Number(parts[0]);
    const min = Number(parts[1]);
    const max = Number(parts[2]);
    return min <= value && value <= max ? 'VALID' : 'INVALID';
}

// P014
function isValidIPv4(ip) {
    const parts = ip.split('.');
    if (parts.length !== 4) return false;
    for (const part of parts) {
        if (!/^\d+$/.test(part) || (part.length > 1 && part[0] === '0') || Number(part) > 255) return false;
    }
    return true;
}

// P015
function isValidUsername(username) {
    return username.length >= 3 && username.length <= 20 &&
           /^[a-zA-Z][a-zA-Z0-9_-]*$/.test(username);
}

// P016
function escapeHtml(s) {
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
}

// P017
function escapeCsvCell(s) {
    if (/[,"\n\r]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
    return s;
}

// P018
function escapeJsonString(s) {
    let result = '';
    for (const ch of s) {
        const code = ch.charCodeAt(0);
        if (ch === '"') result += '\\"';
        else if (ch === '\\') result += '\\\\';
        else if (ch === '/') result += '\\/';
        else if (ch === '\b') result += '\\b';
        else if (ch === '\f') result += '\\f';
        else if (ch === '\n') result += '\\n';
        else if (ch === '\r') result += '\\r';
        else if (ch === '\t') result += '\\t';
        else if (code < 0x20) result += `\\u${code.toString(16).padStart(4, '0')}`;
        else result += ch;
    }
    return result;
}

// P019
function encodeUrlComponent(s) {
    const bytes = new TextEncoder().encode(s);
    const hex = '0123456789ABCDEF';
    let result = '';
    for (const byte of bytes) {
        const unreserved =
            (byte >= 65 && byte <= 90) ||
            (byte >= 97 && byte <= 122) ||
            (byte >= 48 && byte <= 57) ||
            byte === 45 || byte === 95 || byte === 46 || byte === 126;
        if (unreserved) result += String.fromCharCode(byte);
        else result += `%${hex[byte >> 4]}${hex[byte & 15]}`;
    }
    return result;
}

// P020
function sanitizeTemplate(s) {
    return s.replace(/\{\{([^{}]*)\}\}/g, (match, key) => /^[a-zA-Z0-9_]+$/.test(key) ? match : '');
}

// P021
function safePathNormalize(path) {
    if (path.length === 0 || path.trim().length === 0 || path.includes('\\')) return '';
    const parts = [];
    for (const segment of path.split('/')) {
        if (segment === '' || segment === '.') continue;
        if (segment === '..') {
            if (parts.length === 0) return '';
            parts.pop();
        } else {
            parts.push(segment);
        }
    }
    return parts.join('/');
}

// P022
function isAllowedExtension(path) {
    const filename = path.split(/[\\/]/).pop();
    const dot = filename.lastIndexOf('.');
    if (dot <= 0) return false;
    return new Set(['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt', '.csv']).has(filename.slice(dot).toLowerCase());
}

// P023
function sanitizeFilename(name) {
    let value = name.slice(0, 200).replace(/[^a-zA-Z0-9._-]/g, '_');
    value = value.replace(/_+/g, '_').replace(/^_+|_+$/g, '');
    return value || '_';
}

// P024
function checkArchiveEntry(path) {
    if (path === '') return 'safe';
    if (path.startsWith('/') || path.includes('\\')) return 'unsafe';
    let depth = 0;
    for (const segment of path.split('/')) {
        if (segment === '' || segment === '.') continue;
        if (segment === '..') {
            depth--;
            if (depth < 0) return 'unsafe';
        } else {
            depth++;
        }
    }
    return 'safe';
}

// P025
function isAllowedFiletype(ext) {
    const value = ext.startsWith('.') ? ext.slice(1) : ext;
    return value.length > 0 &&
           new Set(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'pdf', 'txt', 'csv', 'json', 'xml']).has(value.toLowerCase());
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
    if ((s.match(/\|/g) || []).length !== 1) return 'INVALID';
    const [table, conditions] = s.split('|');
    if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(table) || conditions.length === 0) return 'INVALID';
    const columns = [];
    for (const part of conditions.split(',')) {
        const eq = part.indexOf('=');
        if (eq < 0) return 'INVALID';
        const column = part.slice(0, eq);
        if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(column)) return 'INVALID';
        columns.push(column);
    }
    if (columns.length === 0) return 'INVALID';
    return `SELECT * FROM ${table} WHERE ${columns.map(c => `${c}=?`).join(' AND ')}`;
}

// P029
function validateSortDirection(s) {
    const value = s.trim().toUpperCase();
    return value === 'ASC' || value === 'DESC' ? value : 'INVALID';
}

// P030
function isAllowedColumn(col) {
    return new Set(['id', 'name', 'email', 'created_at', 'status', 'age', 'role', 'score']).has(col.trim());
}

// P031
function quoteShellArg(s) {
    return `'${s.replace(/'/g, "'\\''")}'`;
}

// P032
function isAllowedCommand(s) {
    return new Set(['ls', 'cat', 'echo', 'grep', 'find', 'sort', 'uniq', 'wc', 'head', 'tail']).has(s.trim());
}

// P033
function detectShellMeta(s) {
    return /[;|&$`><(){}\\"'\n\r]/.test(s) ? 'unsafe' : 'safe';
}

// P034
function isValidEnvVar(name) {
    return name.length >= 1 && name.length <= 64 && /^[A-Z_][A-Z0-9_]*$/.test(name);
}

// P035
function splitArgs(s) {
    if (s.length === 0) return [];
    const tokens = [];
    let current = '';
    let inQuotes = false;
    let tokenStarted = false;
    for (const ch of s) {
        if (ch === '"') {
            inQuotes = !inQuotes;
            tokenStarted = true;
        } else if (ch === ' ' && !inQuotes) {
            if (tokenStarted) {
                tokens.push(current);
                current = '';
                tokenStarted = false;
            }
        } else {
            current += ch;
            tokenStarted = true;
        }
    }
    if (tokenStarted) tokens.push(current);
    return tokens;
}

// P036
function parseSafeLiteral(s) {
    if (/^-?(0|[1-9][0-9]*)$/.test(s)) return s;
    if (s === 'true' || s === 'false' || s === 'null') return s;
    if (s.length >= 2 && s[0] === '"' && s[s.length - 1] === '"') {
        const content = s.slice(1, -1);
        let result = '';
        for (let i = 0; i < content.length; i++) {
            if (content[i] === '\\') {
                if (i + 1 >= content.length || content[i + 1] !== '"') return 'INVALID';
                result += '"';
                i++;
            } else if (content[i] === '"') {
                return 'INVALID';
            } else {
                result += content[i];
            }
        }
        return result;
    }
    return 'INVALID';
}

// P037
function parseConfigBool(s) {
    const value = s.trim().toLowerCase();
    if (new Set(['true', 'yes', '1', 'on', 'enabled']).has(value)) return 'true';
    if (new Set(['false', 'no', '0', 'off', 'disabled']).has(value)) return 'false';
    return 'INVALID';
}

// P038
function isAllowedConfigKey(key) {
    return new Set(['host', 'port', 'database', 'username', 'password', 'timeout',
                    'max_connections', 'ssl_enabled', 'log_level', 'retry_count']).has(key.trim());
}

// P039
function validateToken(s) {
    return /^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[0-9a-f]{8}$/.test(s) ? 'valid' : 'invalid';
}

// P040
function validateNumericExpr(s) {
    const number = '-?(?:0|[1-9][0-9]*)';
    const pattern = new RegExp(`^${number}(?:\\s*[+\\-*/]\\s*${number})*$`);
    return pattern.test(s) ? 'valid' : 'invalid';
}

// P041
function frequencyCounter(nums) {
    const counts = new Map();
    for (const value of nums) counts.set(value, (counts.get(value) || 0) + 1);
    const result = {};
    [...counts.keys()].sort((a, b) => a - b).forEach(key => {
        result[String(key)] = counts.get(key);
    });
    return result;
}

// P042
function hasDuplicate(nums) {
    return new Set(nums).size !== nums.length;
}

// P043
function streamingSum(nums) {
    return nums.reduce((sum, value) => sum + value, 0);
}

// P044
function boundedLogProcessor(log, maxLines) {
    let kept = 0;
    let totalWords = 0;
    if (maxLines > 0 && log.length > 0) {
        for (const line of log.split(/\r?\n/)) {
            if (line.trim().length === 0) continue;
            if (kept >= maxLines) break;
            kept++;
            totalWords += line.trim().split(/\s+/).length;
        }
    }
    return { kept, total_words: totalWords };
}

// P045
function topKFrequent(nums, k) {
    if (nums.length === 0 || k === 0) return [];
    const counts = new Map();
    for (const value of nums) counts.set(value, (counts.get(value) || 0) + 1);
    const values = [...counts.keys()].sort((a, b) => {
        const frequencyDifference = counts.get(b) - counts.get(a);
        return frequencyDifference !== 0 ? frequencyDifference : a - b;
    });
    return values.slice(0, k).sort((a, b) => a - b);
}

// P046
function validateTokenFormat(token) {
    return /^[a-zA-Z][a-zA-Z0-9-]{7,31}$/.test(token) ? 'valid' : 'invalid';
}

// P047
function evaluatePermission(role, action) {
    const permissions = {
        admin: new Set(['read', 'write', 'delete', 'execute']),
        editor: new Set(['read', 'write']),
        viewer: new Set(['read']),
        guest: new Set()
    };
    return permissions[role]?.has(action) ? 'allowed' : 'denied';
}

// P048
function roleHasPermission(role, permission) {
    const permissions = {
        admin: new Set(['read', 'write', 'delete', 'execute']),
        editor: new Set(['read', 'write']),
        viewer: new Set(['read']),
        guest: new Set()
    };
    return permissions[role]?.has(permission) || false;
}

// P049
function checkSession(lastActive, currentTime, timeout) {
    if (currentTime < lastActive) return 'invalid';
    return currentTime - lastActive > timeout ? 'expired' : 'active';
}

// P050
function validateScope(requested, allowed) {
    const parts = requested.split(':');
    for (let i = parts.length; i >= 1; i--) {
        const prefix = parts.slice(0, i).join(':');
        if (allowed.includes(prefix)) return 'granted';
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
    validateScope
};
