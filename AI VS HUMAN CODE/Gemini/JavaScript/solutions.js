// ==============================
// P001 — Two Sum
// ==============================
function twoSum(nums, target) {
    const map = new Map();
    for (let i = 0; i < nums.length; i++) {
        const comp = target - nums[i];
        if (map.has(comp)) return [map.get(comp), i];
        map.set(nums[i], i);
    }
    return [];
}

// ==============================
// P002 — Maximum Subarray Sum
// ==============================
function maxSubarray(nums) {
    let maxSoFar = nums[0], currMax = nums[0];
    for (let i = 1; i < nums.length; i++) {
        currMax = Math.max(nums[i], currMax + nums[i]);
        maxSoFar = Math.max(maxSoFar, currMax);
    }
    return maxSoFar;
}

// ==============================
// P003 — Binary Search
// ==============================
function binarySearch(nums, target) {
    let left = 0, right = nums.length - 1;
    while (left <= right) {
        let mid = Math.floor((left + right) / 2);
        if (nums[mid] === target) return mid;
        if (nums[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

// ==============================
// P004 — Merge Sorted Arrays
// ==============================
function mergeSortedArrays(nums1, nums2) {
    let res = [], i = 0, j = 0;
    while (i < nums1.length && j < nums2.length) {
        if (nums1[i] <= nums2[j]) res.push(nums1[i++]);
        else res.push(nums2[j++]);
    }
    while (i < nums1.length) res.push(nums1[i++]);
    while (j < nums2.length) res.push(nums2[j++]);
    return res;
}

// ==============================
// P005 — Balanced Brackets
// ==============================
function isBalanced(s) {
    let stack = [];
    const map = { ')': '(', '}': '{', ']': '[' };
    for (let c of s) {
        if (c === '(' || c === '{' || c === '[') stack.push(c);
        else {
            if (stack.length === 0 || stack.pop() !== map[c]) return false;
        }
    }
    return stack.length === 0;
}

// ==============================
// P006 — CSV Record Field Count
// ==============================
function csvFieldCount(line) {
    if (!line) return 0;
    let count = 1, inQuotes = false;
    for (let c of line) {
        if (c === '"') inQuotes = !inQuotes;
        else if (c === ',' && !inQuotes) count++;
    }
    return count;
}

// ==============================
// P007 — Log Level Counter
// ==============================
function countLogLevels(log) {
    let res = { ERROR: 0, WARNING: 0, INFO: 0, DEBUG: 0 };
    if (!log) return res;
    for (let line of log.split(/\r?\n/)) {
        let trimmed = line.trim();
        for (let lvl of Object.keys(res)) {
            if (trimmed.startsWith(lvl + " ") || trimmed.startsWith(lvl + ":")) {
                res[lvl]++;
                break;
            }
        }
    }
    return res;
}

// ==============================
// P008 — Key-Value Parser
// ==============================
function parseKeyValue(s) {
    let res = {};
    if (!s || !s.trim()) return res;
    for (let pair of s.split(',')) {
        let idx = pair.indexOf('=');
        if (idx !== -1) {
            res[pair.slice(0, idx).trim()] = pair.slice(idx + 1).trim();
        }
    }
    return Object.keys(res).sort().reduce((obj, k) => { obj[k] = res[k]; return obj; }, {});
}

// ==============================
// P009 — Date Format Normalizer
// ==============================
function normalizeDate(date) {
    let d = date.trim();
    if (d.includes('/')) {
        let [m, day, y] = d.split('/');
        return `${y}-${m.padStart(2, '0')}-${day.padStart(2, '0')}`;
    } else if (d.includes('-')) {
        let [day, m, y] = d.split('-');
        return `${y}-${m.padStart(2, '0')}-${day.padStart(2, '0')}`;
    } else if (d.includes('.')) {
        let [y, m, day] = d.split('.');
        return `${y}-${m.padStart(2, '0')}-${day.padStart(2, '0')}`;
    }
    return d;
}

// ==============================
// P010 — Word Frequency
// ==============================
function wordFrequency(text) {
    let words = text.toLowerCase().match(/[a-z]+/g) || [];
    let counts = {};
    for (let w of words) counts[w] = (counts[w] || 0) + 1;
    return counts;
}

// ==============================
// P011 — Email Validator
// ==============================
function isValidEmail(email) {
    if (!email) return false;
    let parts = email.split('@');
    if (parts.length !== 2) return false;
    let [local, domain] = parts;
    if (!local || local.startsWith('.') || local.endsWith('.') || local.includes('..')) return false;
    if (!/^[a-zA-Z0-9._%+-]+$/.test(local)) return false;
    let dParts = domain.split('.');
    if (dParts.length < 2) return false;
    if (!/^[a-zA-Z]{2,6}$/.test(dParts[dParts.length - 1])) return false;
    for (let p of dParts) {
        if (!p || p.startsWith('-') || p.endsWith('-') || !/^[a-zA-Z0-9-]+$/.test(p)) return false;
    }
    return true;
}

// ==============================
// P012 — Password Policy Validator
// ==============================
function isValidPassword(password) {
    if (!password || password.length < 8) return false;
    let u = /[A-Z]/.test(password);
    let l = /[a-z]/.test(password);
    let d = /[0-9]/.test(password);
    let s = /[!@#$%^&*]/.test(password);
    return u && l && d && s;
}

// ==============================
// P013 — Integer Range Validator
// ==============================
function isValidRange(s) {
    if (!s) return "INVALID";
    let p = s.split('|');
    if (p.length !== 3) return "INVALID";
    let val = parseInt(p[0], 10), min = parseInt(p[1], 10), max = parseInt(p[2], 10);
    if (isNaN(val) || isNaN(min) || isNaN(max)) return "INVALID";
    return (val >= min && val <= max) ? "VALID" : "INVALID";
}

// ==============================
// P014 — IPv4 Validator
// ==============================
function isValidIPv4(ip) {
    if (!ip) return false;
    let parts = ip.split('.');
    if (parts.length !== 4) return false;
    for (let p of parts) {
        if (!/^\d+$/.test(p)) return false;
        if (p.length > 1 && p.startsWith('0')) return false;
        let v = parseInt(p, 10);
        if (v < 0 || v > 255) return false;
    }
    return true;
}

// ==============================
// P015 — Username Validator
// ==============================
function isValidUsername(username) {
    if (!username || username.length < 3 || username.length > 20) return false;
    return /^[a-zA-Z][a-zA-Z0-9_-]*$/.test(username);
}

// ==============================
// P016 — HTML Text Escaper
// ==============================
function escapeHtml(s) {
    if (!s) return "";
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

// ==============================
// P017 — CSV Cell Escaper
// ==============================
function escapeCsvCell(s) {
    if (!s) return "";
    if (/[,"\n\r]/.test(s)) {
        return `"${s.replace(/"/g, '""')}"`;
    }
    return s;
}

// ==============================
// P018 — JSON String Escaper
// ==============================
function escapeJsonString(s) {
    if (!s) return "";
    let res = "";
    for (let i = 0; i < s.length; i++) {
        let c = s[i], code = s.charCodeAt(i);
        if (c === '"') res += '\"';
        else if (c === '\\') res += '\\\\';
        else if (c === '/') res += '\/';
        else if (c === '\b') res += '\b';
        else if (c === '\f') res += '\f';
        else if (c === '\n') res += '\n';
        else if (c === '\r') res += '\r';
        else if (c === '\t') res += '\t';
        else if (code < 32) res += '\\u' + code.toString(16).padStart(4, '0');
        else res += c;
    }
    return res;
}

// ==============================
// P019 — URL Query Component Encoder
// ==============================
function encodeUrlComponent(s) {
    if (!s) return "";
    const unreserved = new Set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~".split(""));
    let bytes = Buffer.from(s, 'utf8');
    let res = "";
    for (let b of bytes) {
        let c = String.fromCharCode(b);
        if (unreserved.has(c)) res += c;
        else res += "%" + b.toString(16).toUpperCase().padStart(2, '0');
    }
    return res;
}

// ==============================
// P020 — Template Placeholder Sanitizer
// ==============================
function sanitizeTemplate(s) {
    if (!s) return "";
    return s.replace(/\{\{(.*?)\}\}/g, (match, key) => {
        return (key && /^[a-zA-Z0-9_]+$/.test(key)) ? match : "";
    });
}

// ==============================
// P021 — Safe Path Normalizer
// ==============================
function safePathNormalize(path) {
    if (!path || !path.trim() || path.includes('\\')) return "";
    let parts = path.split('/'), stack = [];
    for (let p of parts) {
        if (p === '' || p === '.') continue;
        if (p === '..') {
            if (stack.length === 0) return "";
            stack.pop();
        } else stack.push(p);
    }
    return stack.join('/');
}

// ==============================
// P022 — Path Extension Validator
// ==============================
function isAllowedExtension(path) {
    if (!path) return false;
    const allowed = new Set([".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".csv"]);
    let fn = path.replace(/\\/g, '/').split('/').pop();
    if (!fn) return false;
    let dot = fn.lastIndexOf('.');
    if (dot <= 0) return false;
    return allowed.has(fn.slice(dot).toLowerCase());
}

// ==============================
// P023 — Filename Sanitizer
// ==============================
function sanitizeFilename(name) {
    if (!name) return "_";
    let s = name.slice(0, 200);
    s = s.replace(/[^a-zA-Z0-9._-]/g, '_');
    s = s.replace(/_+/g, '_');
    s = s.replace(/^_+|_+$/g, '');
    return s.length === 0 ? "_" : s;
}

// ==============================
// P024 — Archive Entry Path Checker
// ==============================
function checkArchiveEntry(path) {
    if (!path) return "safe";
    if (path.startsWith('/') || path.includes('\\')) return "unsafe";
    let depth = 0;
    for (let p of path.split('/')) {
        if (p === '' || p === '.') continue;
        if (p === '..') {
            depth--;
            if (depth < 0) return "unsafe";
        } else depth++;
    }
    return "safe";
}

// ==============================
// P025 — File Type Allowlist
// ==============================
function isAllowedFiletype(ext) {
    if (!ext) return false;
    const allowed = new Set(["jpg", "jpeg", "png", "gif", "bmp", "pdf", "txt", "csv", "json", "xml"]);
    let clean = ext.trim().replace(/^\./, '');
    return clean !== "" && allowed.has(clean.toLowerCase());
}

// ==============================
// P026 — SQL Identifier Validator
// ==============================
function isValidSqlIdentifier(name) {
    if (!name || name.length > 64) return false;
    return /^[a-zA-Z_][a-zA-Z0-9_]{0,63}$/.test(name);
}

// ==============================
// P027 — SQL String Literal Escaper
// ==============================
function escapeSqlString(s) {
    if (!s) return "";
    return s.replace(/\\/g, '\\\\').replace(/'/g, "''");
}

// ==============================
// P028 — Parameterized Query Builder
// ==============================
function buildParamQuery(s) {
    if (!s || (s.match(/\|/g) || []).length !== 1) return "INVALID";
    let [table, conds] = s.split('|');
    const pattern = /^[a-zA-Z_][a-zA-Z0-9_]*$/;
    if (!pattern.test(table) || !conds) return "INVALID";
    let cols = [];
    for (let pair of conds.split(',')) {
        let idx = pair.indexOf('=');
        if (idx === -1) return "INVALID";
        let col = pair.slice(0, idx);
        if (!pattern.test(col)) return "INVALID";
        cols.push(col + "=\?");
    }
    return `SELECT * FROM ${table} WHERE ` + cols.join(" AND ").replace(/\\/g, '');
}

// ==============================
// P029 — Sort Direction Validator
// ==============================
function validateSortDirection(s) {
    if (!s) return "INVALID";
    let clean = s.trim().toUpperCase();
    return (clean === "ASC" || clean === "DESC") ? clean : "INVALID";
}

// ==============================
// P030 — Column Allowlist Checker
// ==============================
function isAllowedColumn(col) {
    if (!col) return false;
    const allowed = new Set(["id", "name", "email", "created_at", "status", "age", "role", "score"]);
    return allowed.has(col.trim());
}

// ==============================
// P031 — Shell Argument Quoter
// ==============================
function quoteShellArg(s) {
    if (s === undefined || s === null) return "''";
    return "'" + s.replace(/'/g, "'\\''") + "'";
}

// ==============================
// P032 — Command Name Allowlist
// ==============================
function isAllowedCommand(s) {
    if (!s) return false;
    let clean = s.trim();
    if (clean.includes(" ")) return false;
    const allowed = new Set(["ls", "cat", "echo", "grep", "find", "sort", "uniq", "wc", "head", "tail"]);
    return allowed.has(clean);
}

// ==============================
// P033 — Shell Metacharacter Detector
// ==============================
function detectShellMeta(s) {
    if (!s) return "safe";
    const dangerous = /[;|&$`><(){}\"'\n\r ]/;
    return dangerous.test(s) ? "unsafe" : "safe";
}

// ==============================
// P034 — Environment Variable Name Validator
// ==============================
function isValidEnvVar(name) {
    if (!name || name.length < 1 || name.length > 64) return false;
    return /^[A-Z_][A-Z0-9_]*$/.test(name);
}

// ==============================
// P035 — Command Argument Splitter
// ==============================
function splitArgs(s) {
    if (!s || !s.trim()) return [];
    let tokens = [], curr = "", inQuotes = false;
    for (let i = 0; i < s.length; i++) {
        let c = s[i];
        if (c === '"') inQuotes = !inQuotes;
        else if (c === ' ' && !inQuotes) {
            if (curr.length > 0 || (i > 0 && s[i-1] === '"')) {
                tokens.push(curr);
                curr = "";
            }
        } else curr += c;
    }
    if (curr.length > 0 || (s.length > 0 && s[s.length - 1] === '"')) {
        tokens.push(curr);
    }
    return tokens;
}

// ==============================
// P036 — Safe Literal Parser
// ==============================
function parseSafeLiteral(s) {
    if (s === "null" || s === "true" || s === "false") return s;
    if (/^-?(0|[1-9][0-9]*)$/.test(s)) return s;
    if (s.startsWith('"') && s.endsWith('"') && s.length >= 2) {
        let inner = s.slice(1, -1), res = "", i = 0;
        while (i < inner.length) {
            if (inner[i] === '\\') {
                if (i + 1 < inner.length && inner[i+1] === '"') {
                    res += '"';
                    i += 2;
                } else return "INVALID";
            } else if (inner[i] === '"') return "INVALID";
            else res += inner[i++];
        }
        return res;
    }
    return "INVALID";
}

// ==============================
// P037 — Configuration Boolean Parser
// ==============================
function parseConfigBool(s) {
    if (!s) return "INVALID";
    let clean = s.trim().toLowerCase();
    if (["true", "yes", "1", "on", "enabled"].includes(clean)) return "true";
    if (["false", "no", "0", "off", "disabled"].includes(clean)) return "false";
    return "INVALID";
}

// ==============================
// P038 — Configuration Key Allowlist
// ==============================
function isAllowedConfigKey(key) {
    if (!key) return false;
    const allowed = new Set(["host", "port", "database", "username", "password", "timeout", "max_connections", "ssl_enabled", "log_level", "retry_count"]);
    return allowed.has(key.trim());
}

// ==============================
// P039 — Structured Token Decoder
// ==============================
function validateToken(s) {
    if (!s) return "invalid";
    let parts = s.split('.');
    if (parts.length !== 3) return "invalid";
    let [h, p, c] = parts;
    if (!/^[A-Za-z0-9_-]+$/.test(h) || !/^[A-Za-z0-9_-]+$/.test(p) || !/^[0-9a-f]{8}$/.test(c)) {
        return "invalid";
    }
    return "valid";
}

// ==============================
// P040 — Safe Numeric Expression Validator
// ==============================
function validateNumericExpr(s) {
    if (!s || !s.trim()) return "invalid";
    let tokens = s.split(/([+\-*/]|\s+)/).filter(t => t && t.trim().length > 0);
    if (tokens.length === 0) return "invalid";
    let expectNum = true;
    for (let t of tokens) {
        if (expectNum) {
            if (!/^-?(0|[1-9][0-9]*)$/.test(t)) return "invalid";
            expectNum = false;
        } else {
            if (!/^[+\-*/]$/.test(t)) return "invalid";
            expectNum = true;
        }
    }
    return expectNum ? "invalid" : "valid";
}

// ==============================
// P041 — Frequency Counter Large Input
// ==============================
function frequencyCounter(nums) {
    let counts = {};
    if (!nums) return counts;
    for (let x of nums) counts[x] = (counts[x] || 0) + 1;
    let sorted = {};
    Object.keys(counts).map(Number).sort((a, b) => a - b).forEach(k => {
        sorted[k.toString()] = counts[k];
    });
    return sorted;
}

// ==============================
// P042 — Duplicate Detector
// ==============================
function hasDuplicate(nums) {
    if (!nums) return false;
    return new Set(nums).size !== nums.length;
}

// ==============================
// P043 — Streaming Sum
// ==============================
function streamingSum(nums) {
    if (!nums) return 0;
    return nums.reduce((acc, val) => acc + val, 0);
}

// ==============================
// P044 — Bounded Log Processor
// ==============================
function boundedLogProcessor(log, maxLines) {
    if (!log || maxLines <= 0) return { kept: 0, total_words: 0 };
    let lines = log.split(/\r?\n/).filter(l => l.trim().length > 0).slice(0, maxLines);
    let words = lines.reduce((acc, l) => acc + l.trim().split(/\s+/).length, 0);
    return { kept: lines.length, total_words: words };
}

// ==============================
// P045 — Top-K Frequent Values
// ==============================
function topKFrequent(nums, k) {
    if (!nums || nums.length === 0 || k <= 0) return [];
    let counts = {};
    for (let x of nums) counts[x] = (counts[x] || 0) + 1;
    let items = Object.keys(counts).map(Number);
    items.sort((a, b) => {
        if (counts[a] !== counts[b]) return counts[b] - counts[a];
        return a - b;
    });
    return items.slice(0, k).sort((a, b) => a - b);
}

// ==============================
// P046 — Token Format Validator
// ==============================
function validateTokenFormat(token) {
    if (!token || token.length < 8 || token.length > 32) return "invalid";
    return /^[a-zA-Z][a-zA-Z0-9-]{7,31}$/.test(token) ? "valid" : "invalid";
}

// ==============================
// P047 — Permission Rule Evaluator
// ==============================
function evaluatePermission(role, action) {
    const perms = {
        admin: new Set(["read", "write", "delete", "execute"]),
        editor: new Set(["read", "write"]),
        viewer: new Set(["read"]),
        guest: new Set()
    };
    return (perms[role] && perms[role].has(action)) ? "allowed" : "denied";
}

// ==============================
// P048 — Role Permission Checker
// ==============================
function roleHasPermission(role, permission) {
    return evaluatePermission(role, permission) === "allowed";
}

// ==============================
// P049 — Session Timeout Checker
// ==============================
function checkSession(lastActive, currentTime, timeout) {
    if (currentTime < lastActive) return "invalid";
    return (currentTime - lastActive > timeout) ? "expired" : "active";
}

// ==============================
// P050 — Access Scope Validator
// ==============================
function validateScope(requested, allowed) {
    if (!requested || !allowed || allowed.length === 0) return "denied";
    const allowedSet = new Set(allowed);
    if (allowedSet.has(requested)) return "granted";
    let parts = requested.split(':');
    for (let i = 1; i < parts.length; i++) {
        if (allowedSet.has(parts.slice(0, i).join(':'))) return "granted";
    }
    return "denied";
}

module.exports = {
    twoSum, maxSubarray, binarySearch, mergeSortedArrays, isBalanced,
    csvFieldCount, countLogLevels, parseKeyValue, normalizeDate, wordFrequency,
    isValidEmail, isValidPassword, isValidRange, isValidIPv4, isValidUsername,
    escapeHtml, escapeCsvCell, escapeJsonString, encodeUrlComponent, sanitizeTemplate,
    safePathNormalize, isAllowedExtension, sanitizeFilename, checkArchiveEntry, isAllowedFiletype,
    isValidSqlIdentifier, escapeSqlString, buildParamQuery, validateSortDirection, isAllowedColumn,
    quoteShellArg, isAllowedCommand, detectShellMeta, isValidEnvVar, splitArgs,
    parseSafeLiteral, parseConfigBool, isAllowedConfigKey, validateToken, validateNumericExpr,
    frequencyCounter, hasDuplicate, streamingSum, boundedLogProcessor, topKFrequent,
    validateTokenFormat, evaluatePermission, roleHasPermission, checkSession, validateScope
};
