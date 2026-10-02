"use strict";

const PERMISSION_TABLE = new Map([
    ["admin", new Set(["read", "write", "delete", "execute"])],
    ["editor", new Set(["read", "write"])],
    ["viewer", new Set(["read"])],
    ["guest", new Set()],
]);

// P001: Two Sum
function twoSum(nums, target) {
    const seen = new Map();
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (seen.has(complement)) {
            return [seen.get(complement), i];
        }
        seen.set(nums[i], i);
    }
    return [];
}

// P002: Maximum Subarray Sum
function maxSubarray(nums) {
    let best = nums[0];
    let current = nums[0];
    for (let i = 1; i < nums.length; i++) {
        current = Math.max(nums[i], current + nums[i]);
        best = Math.max(best, current);
    }
    return best;
}

// P003: Binary Search
function binarySearch(nums, target) {
    let lo = 0;
    let hi = nums.length - 1;
    while (lo <= hi) {
        const mid = Math.floor((lo + hi) / 2);
        if (nums[mid] === target) return mid;
        if (nums[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}

// P004: Merge Sorted Arrays
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

// P005: Balanced Brackets
function isBalanced(s) {
    const pairs = { ")": "(", "]": "[", "}": "{" };
    const stack = [];
    for (const ch of s) {
        if (ch === "(" || ch === "[" || ch === "{") {
            stack.push(ch);
        } else if (ch === ")" || ch === "]" || ch === "}") {
            if (stack.length === 0 || stack.pop() !== pairs[ch]) return false;
        }
    }
    return stack.length === 0;
}

// P006: CSV Record Field Count
function csvFieldCount(line) {
    if (line === "") return 0;
    let count = 1;
    let inQuotes = false;
    for (let i = 0; i < line.length; i++) {
        const c = line[i];
        if (c === '"') {
            if (inQuotes && line[i + 1] === '"') {
                i++;
            } else {
                inQuotes = !inQuotes;
            }
        } else if (c === "," && !inQuotes) {
            count++;
        }
    }
    return count;
}

// P007: Log Level Counter
function countLogLevels(log) {
    const levels = { ERROR: 0, WARNING: 0, INFO: 0, DEBUG: 0 };
    for (const line of log.split("\n")) {
        for (const level of Object.keys(levels)) {
            if (line.startsWith(level + " ") || line.startsWith(level + ":")) {
                levels[level]++;
                break;
            }
        }
    }
    return levels;
}

// P008: Key-Value Parser
function parseKeyValue(s) {
    if (s === "") return {};
    const entries = [];
    for (const pair of s.split(",")) {
        const idx = pair.indexOf("=");
        if (idx === -1) continue;
        entries.push([pair.slice(0, idx).trim(), pair.slice(idx + 1).trim()]);
    }
    entries.sort((a, b) => (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0));
    return Object.fromEntries(entries);
}

// P009: Date Format Normalizer
function normalizeDate(date) {
    if (date.includes("/")) {
        const [mm, dd, yyyy] = date.split("/");
        return `${yyyy}-${mm}-${dd}`;
    }
    if (date.includes("-")) {
        const [dd, mm, yyyy] = date.split("-");
        return `${yyyy}-${mm}-${dd}`;
    }
    const [yyyy, mm, dd] = date.split(".");
    return `${yyyy}-${mm}-${dd}`;
}

// P010: Word Frequency
function wordFrequency(text) {
    const counts = new Map();
    const words = text.toLowerCase().match(/[a-z]+/g) || [];
    for (const word of words) {
        counts.set(word, (counts.get(word) || 0) + 1);
    }
    return [...counts.entries()].sort((a, b) => {
        if (a[1] !== b[1]) return b[1] - a[1];
        return a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0;
    });
}

// P011: Email Validator
function isValidEmail(email) {
    if (email.split("@").length !== 2) return false;
    const [local, domain] = email.split("@");
    if (!/^[a-zA-Z0-9._%+-]+$/.test(local)) return false;
    if (local.startsWith(".") || local.endsWith(".") || local.includes("..")) return false;
    const labels = domain.split(".");
    if (labels.length < 2) return false;
    for (const label of labels) {
        if (label === "" || label.startsWith("-") || label.endsWith("-")) return false;
        if (!/^[a-zA-Z0-9-]+$/.test(label)) return false;
    }
    return /^[a-zA-Z]{2,6}$/.test(labels[labels.length - 1]);
}

// P012: Password Policy Validator
function isValidPassword(password) {
    if (password.length < 8) return false;
    if (!/[A-Z]/.test(password)) return false;
    if (!/[a-z]/.test(password)) return false;
    if (!/[0-9]/.test(password)) return false;
    if (!/[!@#$%^&*]/.test(password)) return false;
    return true;
}

// P013: Integer Range Validator
function isValidRange(s) {
    const parts = s.split("|");
    if (parts.length !== 3) return "INVALID";
    if (!parts.every((p) => /^[+-]?[0-9]+$/.test(p))) return "INVALID";
    const [value, lo, hi] = parts.map((p) => BigInt(p));
    return lo <= value && value <= hi ? "VALID" : "INVALID";
}

// P014: IPv4 Validator
function isValidIPv4(ip) {
    const parts = ip.split(".");
    if (parts.length !== 4) return false;
    for (const p of parts) {
        if (!/^[0-9]+$/.test(p)) return false;
        if (p.length > 1 && p[0] === "0") return false;
        if (Number(p) > 255) return false;
    }
    return true;
}

// P015: Username Validator
function isValidUsername(username) {
    if (username.length < 3 || username.length > 20) return false;
    return /^[A-Za-z][A-Za-z0-9_-]*$/.test(username);
}

// P016: HTML Text Escaper
function escapeHtml(s) {
    return s
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
}

// P017: CSV Cell Escaper
function escapeCsvCell(s) {
    if (/[,"\n\r]/.test(s)) {
        return '"' + s.replace(/"/g, '""') + '"';
    }
    return s;
}

// P018: JSON String Escaper
function escapeJsonString(s) {
    let result = "";
    for (const ch of s) {
        switch (ch) {
            case '"': result += '\\"'; break;
            case "\\": result += "\\\\"; break;
            case "/": result += "\\/"; break;
            case "\b": result += "\\b"; break;
            case "\f": result += "\\f"; break;
            case "\n": result += "\\n"; break;
            case "\r": result += "\\r"; break;
            case "\t": result += "\\t"; break;
            default:
                if (ch.charCodeAt(0) < 0x20) {
                    result += "\\u" + ch.charCodeAt(0).toString(16).padStart(4, "0");
                } else {
                    result += ch;
                }
        }
    }
    return result;
}

// P019: URL Query Component Encoder
function encodeUrlComponent(s) {
    const unreserved = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~";
    let result = "";
    for (const byte of new TextEncoder().encode(s)) {
        const ch = String.fromCharCode(byte);
        if (byte < 128 && unreserved.includes(ch)) {
            result += ch;
        } else {
            result += "%" + byte.toString(16).toUpperCase().padStart(2, "0");
        }
    }
    return result;
}

// P020: Template Placeholder Sanitizer
function sanitizeTemplate(s) {
    return s.replace(/\{\{(.*?)\}\}/g, (match, key) => {
        return /^[a-zA-Z0-9_]+$/.test(key) ? "{{" + key + "}}" : "";
    });
}

// P021: Safe Path Normalizer
function safePathNormalize(path) {
    if (path.trim() === "") return "";
    const stack = [];
    for (const part of path.split("/")) {
        if (part === "" || part === ".") continue;
        if (part === "..") {
            if (stack.length === 0) return "";
            stack.pop();
        } else {
            stack.push(part);
        }
    }
    return stack.join("/");
}

// P022: Path Extension Validator
function isAllowedExtension(path) {
    const allowed = new Set([".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".csv"]);
    const parts = path.replace(/\\/g, "/").split("/");
    const filename = parts[parts.length - 1];
    const idx = filename.lastIndexOf(".");
    if (idx <= 0) return false;
    return allowed.has(filename.slice(idx).toLowerCase());
}

// P023: Filename Sanitizer
function sanitizeFilename(name) {
    const cleaned = name
        .slice(0, 200)
        .replace(/[^a-zA-Z0-9._-]/g, "_")
        .replace(/_+/g, "_")
        .replace(/^_+|_+$/g, "");
    return cleaned === "" ? "_" : cleaned;
}

// P024: Archive Entry Path Checker
function checkArchiveEntry(path) {
    if (path === "") return "safe";
    if (path.startsWith("/")) return "unsafe";
    if (path.includes("\\")) return "unsafe";
    let depth = 0;
    for (const part of path.split("/")) {
        if (part === "" || part === ".") continue;
        if (part === "..") {
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
    const allowed = new Set(["jpg", "jpeg", "png", "gif", "bmp", "pdf", "txt", "csv", "json", "xml"]);
    if (ext === "") return false;
    const normalized = ext.startsWith(".") ? ext.slice(1) : ext;
    return allowed.has(normalized.toLowerCase());
}

// P026: SQL Identifier Validator
function isValidSqlIdentifier(name) {
    if (name.length < 1 || name.length > 64) return false;
    return /^[a-zA-Z_][a-zA-Z0-9_]*$/.test(name);
}

// P027: SQL String Literal Escaper
function escapeSqlString(s) {
    return s.replace(/\\/g, "\\\\").replace(/'/g, "''");
}

// P028: Parameterized Query Builder
function buildParamQuery(s) {
    const halves = s.split("|");
    if (halves.length !== 2) return "INVALID";
    const [table, cols] = halves;
    if (!isValidSqlIdentifier(table)) return "INVALID";
    if (cols === "") return "INVALID";
    const conditions = [];
    for (const pair of cols.split(",")) {
        const idx = pair.indexOf("=");
        if (idx === -1) return "INVALID";
        const col = pair.slice(0, idx);
        if (!isValidSqlIdentifier(col)) return "INVALID";
        conditions.push(col + "=?");
    }
    return "SELECT * FROM " + table + " WHERE " + conditions.join(" AND ");
}

// P029: Sort Direction Validator
function validateSortDirection(s) {
    const direction = s.trim().toUpperCase();
    return direction === "ASC" || direction === "DESC" ? direction : "INVALID";
}

// P030: Column Allowlist Checker
function isAllowedColumn(col) {
    const allowed = new Set(["id", "name", "email", "created_at", "status", "age", "role", "score"]);
    return allowed.has(col.trim());
}

// P031: Shell Argument Quoter
function quoteShellArg(s) {
    return "'" + s.replace(/'/g, "'\\''") + "'";
}

// P032: Command Name Allowlist
function isAllowedCommand(s) {
    const allowed = new Set(["ls", "cat", "echo", "grep", "find", "sort", "uniq", "wc", "head", "tail"]);
    const command = s.trim();
    if (command.includes(" ")) return false;
    return allowed.has(command);
}

// P033: Shell Metacharacter Detector
function detectShellMeta(s) {
    const dangerous = ";|&$`><(){}\\\"'\n\r";
    for (const ch of s) {
        if (dangerous.includes(ch)) return "unsafe";
    }
    return "safe";
}

// P034: Environment Variable Name Validator
function isValidEnvVar(name) {
    if (name.length < 1 || name.length > 64) return false;
    return /^[A-Z_][A-Z0-9_]*$/.test(name);
}

// P035: Command Argument Splitter
function splitArgs(s) {
    const tokens = [];
    let i = 0;
    while (i < s.length) {
        while (i < s.length && s[i] === " ") i++;
        if (i >= s.length) break;
        if (s[i] === '"') {
            let j = i + 1;
            while (j < s.length && s[j] !== '"') j++;
            tokens.push(s.slice(i + 1, j));
            i = j + 1;
        } else {
            const start = i;
            while (i < s.length && s[i] !== " ") i++;
            tokens.push(s.slice(start, i));
        }
    }
    return tokens;
}

// P036: Safe Literal Parser
function parseSafeLiteral(s) {
    if (s === "true" || s === "false") return s;
    if (s === "null") return "null";
    if (/^-?(0|[1-9][0-9]*)$/.test(s)) return s;
    if (s.length >= 2 && s[0] === '"' && s[s.length - 1] === '"') {
        const inner = s.slice(1, -1);
        let result = "";
        let i = 0;
        while (i < inner.length) {
            if (inner[i] === "\\" && inner[i + 1] === '"') {
                result += '"';
                i += 2;
            } else if (inner[i] === '"') {
                return "INVALID";
            } else {
                result += inner[i];
                i++;
            }
        }
        return result;
    }
    return "INVALID";
}

// P037: Configuration Boolean Parser
function parseConfigBool(s) {
    const value = s.trim().toLowerCase();
    if (["true", "yes", "1", "on", "enabled"].includes(value)) return "true";
    if (["false", "no", "0", "off", "disabled"].includes(value)) return "false";
    return "INVALID";
}

// P038: Configuration Key Allowlist
function isAllowedConfigKey(key) {
    const allowed = new Set([
        "host", "port", "database", "username", "password", "timeout",
        "max_connections", "ssl_enabled", "log_level", "retry_count",
    ]);
    return allowed.has(key.trim());
}

// P039: Structured Token Decoder
function validateToken(s) {
    const parts = s.split(".");
    if (parts.length !== 3) return "invalid";
    if (!/^[A-Za-z0-9_-]+$/.test(parts[0])) return "invalid";
    if (!/^[A-Za-z0-9_-]+$/.test(parts[1])) return "invalid";
    if (!/^[0-9a-f]{8}$/.test(parts[2])) return "invalid";
    return "valid";
}

// P040: Safe Numeric Expression Validator
function validateNumericExpr(s) {
    const number = "-?(?:0|[1-9][0-9]*)";
    const pattern = new RegExp("^\\s*" + number + "\\s*(?:[+\\-*/]\\s*" + number + "\\s*)*$");
    return pattern.test(s) ? "valid" : "invalid";
}

// P041: Frequency Counter Large Input
function frequencyCounter(nums) {
    const counts = new Map();
    for (const n of nums) {
        counts.set(n, (counts.get(n) || 0) + 1);
    }
    const keys = [...counts.keys()].sort((a, b) => a - b);
    return Object.fromEntries(keys.map((k) => [String(k), counts.get(k)]));
}

// P042: Duplicate Detector
function hasDuplicate(nums) {
    return new Set(nums).size !== nums.length;
}

// P043: Streaming Sum
function streamingSum(nums) {
    let sum = 0;
    for (const n of nums) sum += n;
    return sum;
}

// P044: Bounded Log Processor
function boundedLogProcessor(log, maxLines) {
    let kept = 0;
    let totalWords = 0;
    if (maxLines > 0 && log !== "") {
        for (const line of log.split("\n")) {
            const trimmed = line.trim();
            if (trimmed === "") continue;
            if (kept >= maxLines) break;
            kept++;
            totalWords += trimmed.split(/\s+/).length;
        }
    }
    return { kept: kept, total_words: totalWords };
}

// P045: Top-K Frequent Values
function topKFrequent(nums, k) {
    if (k <= 0 || nums.length === 0) return [];
    const counts = new Map();
    for (const n of nums) {
        counts.set(n, (counts.get(n) || 0) + 1);
    }
    const ordered = [...counts.entries()].sort((a, b) => {
        if (a[1] !== b[1]) return b[1] - a[1];
        return a[0] - b[0];
    });
    return ordered.slice(0, k).map((entry) => entry[0]).sort((a, b) => a - b);
}

// P046: Token Format Validator
function validateTokenFormat(token) {
    return /^[a-zA-Z][a-zA-Z0-9-]{7,31}$/.test(token) ? "valid" : "invalid";
}

// P047: Permission Rule Evaluator
function evaluatePermission(role, action) {
    const permissions = PERMISSION_TABLE.get(role);
    return permissions && permissions.has(action) ? "allowed" : "denied";
}

// P048: Role Permission Checker
function roleHasPermission(role, permission) {
    const permissions = PERMISSION_TABLE.get(role);
    return permissions ? permissions.has(permission) : false;
}

// P049: Session Timeout Checker
function checkSession(lastActive, currentTime, timeout) {
    if (currentTime < lastActive) return "invalid";
    return currentTime - lastActive > timeout ? "expired" : "active";
}

// P050: Access Scope Validator
function validateScope(requested, allowed) {
    if (!allowed || allowed.length === 0) return "denied";
    const parts = requested.split(":");
    for (let i = 1; i <= parts.length; i++) {
        if (allowed.includes(parts.slice(0, i).join(":"))) return "granted";
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
    validateTokenFormat, evaluatePermission, roleHasPermission, checkSession, validateScope,
};
