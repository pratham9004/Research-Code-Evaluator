P001
function twoSum(nums, target) {
    const seen = new Map();
    for (let i = 0; i < nums.length; i++) {
        const need = target - nums[i];
        if (seen.has(need)) {
            const a = seen.get(need);
            const b = i;
            return a < b ? [a, b] : [b, a];
        }
        seen.set(nums[i], i);
    }
    return [];
}
module.exports = twoSum;

P002
function maxSubarray(nums) {
    let best = nums[0];
    let cur = nums[0];
    for (let i = 1; i < nums.length; i++) {
        cur = Math.max(nums[i], cur + nums[i]);
        best = Math.max(best, cur);
    }
    return best;
}
module.exports = maxSubarray;

P003
function binarySearch(nums, target) {
    let lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        const mid = (lo + hi) >> 1;
        if (nums[mid] === target) return mid;
        if (nums[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
module.exports = binarySearch;

P004
function mergeSortedArrays(nums1, nums2) {
    const out = [];
    let i = 0, j = 0;
    while (i < nums1.length && j < nums2.length) {
        if (nums1[i] <= nums2[j]) out.push(nums1[i++]);
        else out.push(nums2[j++]);
    }
    while (i < nums1.length) out.push(nums1[i++]);
    while (j < nums2.length) out.push(nums2[j++]);
    return out;
}
module.exports = mergeSortedArrays;

P005
function isBalanced(s) {
    const stack = [];
    const match = { ')': '(', ']': '[', '}': '{' };
    for (const c of s) {
        if (c === '(' || c === '[' || c === '{') stack.push(c);
        else if (c in match) {
            if (!stack.length || stack.pop() !== match[c]) return false;
        }
    }
    return stack.length === 0;
}
module.exports = isBalanced;

P006
function csvFieldCount(line) {
    if (!line) return 0;
    let count = 1;
    let i = 0;
    const n = line.length;
    while (i < n) {
        if (line[i] === '"') {
            i++;
            while (i < n) {
                if (line[i] === '"') {
                    if (i + 1 < n && line[i + 1] === '"') i += 2;
                    else { i++; break; }
                } else i++;
            }
        } else if (line[i] === ',') {
            count++;
            i++;
        } else i++;
    }
    return count;
}
module.exports = csvFieldCount;

P007
function countLogLevels(log) {
    const counts = { ERROR: 0, WARNING: 0, INFO: 0, DEBUG: 0 };
    if (!log) return counts;
    const lines = log.split(/\r?\n/);
    for (let line of lines) {
        line = line.replace(/^\s+/, '');
        for (const level of ['ERROR', 'WARNING', 'INFO', 'DEBUG']) {
            if (line.startsWith(level) && (line.length === level.length || line[level.length] === ' ' || line[level.length] === ':')) {
                counts[level]++;
                break;
            }
        }
    }
    return counts;
}
module.exports = countLogLevels;

P008
function parseKeyValue(s) {
    const result = {};
    if (!s || !s.trim()) return result;
    for (const part of s.split(',')) {
        const p = part.trim();
        if (!p || !p.includes('=')) continue;
        const eq = p.indexOf('=');
        const k = p.slice(0, eq).trim();
        const v = p.slice(eq + 1).trim();
        result[k] = v;
    }
    return Object.fromEntries(Object.entries(result).sort(([a], [b]) => a.localeCompare(b)));
}
module.exports = parseKeyValue;

P009
function normalizeDate(date) {
    if (date.includes('/')) {
        const [mm, dd, yyyy] = date.split('/');
        return `${yyyy}-${mm.padStart(2, '0')}-${dd.padStart(2, '0')}`;
    }
    if (date.includes('-')) {
        const [dd, mm, yyyy] = date.split('-');
        return `${yyyy}-${mm.padStart(2, '0')}-${dd.padStart(2, '0')}`;
    }
    const [yyyy, mm, dd] = date.split('.');
    return `${yyyy}-${mm.padStart(2, '0')}-${dd.padStart(2, '0')}`;
}
module.exports = normalizeDate;

P010
function wordFrequency(text) {
    const freq = {};
    let word = '';
    for (const c of text) {
        if (/[a-zA-Z]/.test(c)) word += c.toLowerCase();
        else {
            if (word) {
                freq[word] = (freq[word] || 0) + 1;
                word = '';
            }
        }
    }
    if (word) freq[word] = (freq[word] || 0) + 1;
    return freq;
}
module.exports = wordFrequency;

P011
function isValidEmail(email) {
    if (!email || email.split('@').length !== 2) return false;
    const [local, domain] = email.split('@');
    if (!local || !domain) return false;
    if (!/^[a-zA-Z0-9._%+-]+$/.test(local)) return false;
    if (local.startsWith('.') || local.endsWith('.') || local.includes('..')) return false;
    const labels = domain.split('.');
    if (labels.length < 2) return false;
    for (const lab of labels) {
        if (!lab || lab.startsWith('-') || lab.endsWith('-') || !/^[a-zA-Z0-9-]+$/.test(lab)) return false;
    }
    const tld = labels[labels.length - 1];
    return tld.length >= 2 && tld.length <= 6 && /^[a-zA-Z]+$/.test(tld);
}
module.exports = isValidEmail;

P012
function isValidPassword(password) {
    if (!password || password.length < 8) return false;
    let up = false, lo = false, dig = false, spe = false;
    const specials = new Set('!@#$%^&*');
    for (const c of password) {
        if (c >= 'A' && c <= 'Z') up = true;
        else if (c >= 'a' && c <= 'z') lo = true;
        else if (c >= '0' && c <= '9') dig = true;
        else if (specials.has(c)) spe = true;
    }
    return up && lo && dig && spe;
}
module.exports = isValidPassword;

P013
function isValidRange(s) {
    if (!s) return 'INVALID';
    const parts = s.split('|');
    if (parts.length !== 3) return 'INVALID';
    const value = Number(parts[0]);
    const mn = Number(parts[1]);
    const mx = Number(parts[2]);
    if (!Number.isInteger(value) || !Number.isInteger(mn) || !Number.isInteger(mx)) return 'INVALID';
    return (mn <= value && value <= mx) ? 'VALID' : 'INVALID';
}
module.exports = isValidRange;

P014
function isValidIPv4(ip) {
    if (!ip) return false;
    const parts = ip.split('.');
    if (parts.length !== 4) return false;
    for (const p of parts) {
        if (!p || !/^\d+$/.test(p)) return false;
        if (p.length > 1 && p[0] === '0') return false;
        const n = Number(p);
        if (n < 0 || n > 255) return false;
    }
    return true;
}
module.exports = isValidIPv4;

P015
function isValidUsername(username) {
    if (!username || username.length < 3 || username.length > 20) return false;
    if (!/^[a-zA-Z]/.test(username)) return false;
    return /^[a-zA-Z0-9_-]+$/.test(username);
}
module.exports = isValidUsername;

P016
function escapeHtml(s) {
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
}
module.exports = escapeHtml;

P017
function escapeCsvCell(s) {
    if (s.includes(',') || s.includes('"') || s.includes('\n') || s.includes('\r')) {
        return '"' + s.replace(/"/g, '""') + '"';
    }
    return s;
}
module.exports = escapeCsvCell;

P018
function escapeJsonString(s) {
    let out = '';
    for (let i = 0; i < s.length; i++) {
        const c = s[i];
        const o = s.charCodeAt(i);
        if (c === '"') out += '\\"';
        else if (c === '\\') out += '\\\\';
        else if (c === '/') out += '\\/';
        else if (o === 8) out += '\\b';
        else if (o === 12) out += '\\f';
        else if (o === 10) out += '\\n';
        else if (o === 13) out += '\\r';
        else if (o === 9) out += '\\t';
        else if (o >= 0 && o <= 31) out += '\\u' + o.toString(16).padStart(4, '0');
        else out += c;
    }
    return out;
}
module.exports = escapeJsonString;

P019
function encodeUrlComponent(s) {
    const unreserved = new Set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~');
    let out = '';
    for (const c of s) {
        if (unreserved.has(c)) out += c;
        else {
            const bytes = new TextEncoder().encode(c);
            for (const b of bytes) out += '%' + b.toString(16).toUpperCase().padStart(2, '0');
        }
    }
    return out;
}
module.exports = encodeUrlComponent;

P020
function sanitizeTemplate(s) {
    return s.replace(/\{\{([^}]*)\}\}/g, (match, key) => {
        if (key && /^[a-zA-Z0-9_]+$/.test(key)) return match;
        return '';
    });
}
module.exports = sanitizeTemplate;

P021
function safePathNormalize(path) {
    if (!path || !path.trim()) return '';
    if (path.includes('\\')) return '';
    const stack = [];
    for (const p of path.split('/')) {
        if (p === '' || p === '.') continue;
        if (p === '..') {
            if (!stack.length) return '';
            stack.pop();
        } else {
            stack.push(p);
        }
    }
    return stack.join('/');
}
module.exports = safePathNormalize;

P022
function isAllowedExtension(path) {
    const name = path.replace(/\\/g, '/').split('/').pop();
    const dot = name.lastIndexOf('.');
    if (dot <= 0) return false;
    const ext = name.slice(dot).toLowerCase();
    return ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt', '.csv'].includes(ext);
}
module.exports = isAllowedExtension;

P023
function sanitizeFilename(name) {
    name = name.slice(0, 200);
    let out = '';
    for (const c of name) {
        if (/[a-zA-Z0-9._-]/.test(c)) out += c;
        else out += '_';
    }
    while (out.includes('__')) out = out.replace(/__/g, '_');
    out = out.replace(/^_+|_+$/g, '');
    return out || '_';
}
module.exports = sanitizeFilename;

P024
function checkArchiveEntry(path) {
    if (path === '') return 'safe';
    if (path.startsWith('/') || path.includes('\\')) return 'unsafe';
    let depth = 0;
    for (const part of path.split('/')) {
        if (part === '' || part === '.') continue;
        if (part === '..') {
            depth--;
            if (depth < 0) return 'unsafe';
        } else {
            depth++;
        }
    }
    return 'safe';
}
module.exports = checkArchiveEntry;

P025
function isAllowedFiletype(ext) {
    let e = ext.startsWith('.') ? ext.slice(1).toLowerCase() : ext.toLowerCase();
    if (!e) return false;
    return ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'pdf', 'txt', 'csv', 'json', 'xml'].includes(e);
}
module.exports = isAllowedFiletype;

P026
function isValidSqlIdentifier(name) {
    return /^[a-zA-Z_][a-zA-Z0-9_]{0,63}$/.test(name);
}
module.exports = isValidSqlIdentifier;

P027
function escapeSqlString(s) {
    return s.replace(/\\/g, '\\\\').replace(/'/g, "''");
}
module.exports = escapeSqlString;

P028
function buildParamQuery(s) {
    if ((s.match(/\|/g) || []).length !== 1) return 'INVALID';
    const [table, conds] = s.split('|');
    if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(table)) return 'INVALID';
    if (!conds.trim()) return 'INVALID';
    const parts = [];
    for (const pair of conds.split(',')) {
        const p = pair.trim();
        if (!p || !p.includes('=')) return 'INVALID';
        const col = p.slice(0, p.indexOf('=')).trim();
        if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(col)) return 'INVALID';
        parts.push(col + '=?');
    }
    return 'SELECT * FROM ' + table + ' WHERE ' + parts.join(' AND ');
}
module.exports = buildParamQuery;

P029
function validateSortDirection(s) {
    const t = s.trim().toUpperCase();
    if (t === 'ASC' || t === 'DESC') return t;
    return 'INVALID';
}
module.exports = validateSortDirection;

P030
function isAllowedColumn(col) {
    const allowed = new Set(['id', 'name', 'email', 'created_at', 'status', 'age', 'role', 'score']);
    return allowed.has(col.trim());
}
module.exports = isAllowedColumn;

P031
function quoteShellArg(s) {
    return "'" + s.replace(/'/g, "'\\''") + "'";
}
module.exports = quoteShellArg;

P032
function isAllowedCommand(s) {
    const t = s.trim();
    if (t.includes(' ')) return false;
    return ['ls', 'cat', 'echo', 'grep', 'find', 'sort', 'uniq', 'wc', 'head', 'tail'].includes(t);
}
module.exports = isAllowedCommand;

P033
function detectShellMeta(s) {
    const dangerous = new Set(';|&$`><(){}\\"\'\n\r');
    for (const c of s) {
        if (dangerous.has(c)) return 'unsafe';
    }
    return 'safe';
}
module.exports = detectShellMeta;

P034
function isValidEnvVar(name) {
    return /^[A-Z_][A-Z0-9_]{0,63}$/.test(name);
}
module.exports = isValidEnvVar;

P035
function splitArgs(s) {
    if (!s) return [];
    const tokens = [];
    let i = 0;
    const n = s.length;
    while (i < n) {
        while (i < n && s[i] === ' ') i++;
        if (i >= n) break;
        if (s[i] === '"') {
            i++;
            let buf = '';
            while (i < n && s[i] !== '"') {
                buf += s[i];
                i++;
            }
            if (i < n && s[i] === '"') i++;
            tokens.push(buf);
        } else {
            let buf = '';
            while (i < n && s[i] !== ' ') {
                buf += s[i];
                i++;
            }
            tokens.push(buf);
        }
    }
    return tokens;
}
module.exports = splitArgs;

P036
function parseSafeLiteral(s) {
    if (s === 'true' || s === 'false' || s === 'null') return s;
    if (s.length >= 2 && s[0] === '"' && s[s.length - 1] === '"') {
        let out = '';
        for (let i = 1; i < s.length - 1; i++) {
            if (s[i] === '\\' && i + 1 < s.length - 1 && s[i + 1] === '"') {
                out += '"';
                i++;
            } else if (s[i] === '"') {
                return 'INVALID';
            } else {
                out += s[i];
            }
        }
        return out;
    }
    if (s === '0') return '0';
    if (s.startsWith('-')) {
        if (s.length === 1 || !/^\d+$/.test(s.slice(1)) || (s.length > 2 && s[1] === '0')) return 'INVALID';
        return s;
    }
    if (/^\d+$/.test(s)) {
        if (s.length > 1 && s[0] === '0') return 'INVALID';
        return s;
    }
    return 'INVALID';
}
module.exports = parseSafeLiteral;

P037
function parseConfigBool(s) {
    const t = s.trim().toLowerCase();
    if (['true', 'yes', '1', 'on', 'enabled'].includes(t)) return 'true';
    if (['false', 'no', '0', 'off', 'disabled'].includes(t)) return 'false';
    return 'INVALID';
}
module.exports = parseConfigBool;

P038
function isAllowedConfigKey(key) {
    const allowed = new Set(['host', 'port', 'database', 'username', 'password', 'timeout',
        'max_connections', 'ssl_enabled', 'log_level', 'retry_count']);
    return allowed.has(key.trim());
}
module.exports = isAllowedConfigKey;

P039
function validateToken(s) {
    const parts = s.split('.');
    if (parts.length !== 3) return 'invalid';
    if (!/^[A-Za-z0-9_-]+$/.test(parts[0])) return 'invalid';
    if (!/^[A-Za-z0-9_-]+$/.test(parts[1])) return 'invalid';
    if (!/^[0-9a-f]{8}$/.test(parts[2])) return 'invalid';
    return 'valid';
}
module.exports = validateToken;

P040
function validateNumericExpr(s) {
    s = s.trim();
    if (!s) return 'invalid';
    const num = '(?:-?(?:0|[1-9]\\d*))';
    const op = '[+\\-*/]';
    const pattern = new RegExp('^' + num + '(?:\\s*' + op + '\\s*' + num + ')*$');
    return pattern.test(s) ? 'valid' : 'invalid';
}
module.exports = validateNumericExpr;

P041
function frequencyCounter(nums) {
    const freq = {};
    for (const n of nums) {
        const k = String(n);
        freq[k] = (freq[k] || 0) + 1;
    }
    return Object.fromEntries(Object.entries(freq).sort(([a], [b]) => Number(a) - Number(b)));
}
module.exports = frequencyCounter;

P042
function hasDuplicate(nums) {
    return new Set(nums).size !== nums.length;
}
module.exports = hasDuplicate;

P043
function streamingSum(nums) {
    return nums.reduce((a, b) => a + b, 0);
}
module.exports = streamingSum;

P044
function boundedLogProcessor(log, maxLines) {
    let kept = 0, totalWords = 0;
    if (maxLines <= 0) return { kept: 0, total_words: 0 };
    for (const line of log.split(/\r?\n/)) {
        if (!line.trim()) continue;
        if (kept >= maxLines) break;
        kept++;
        totalWords += line.trim().split(/\s+/).filter(Boolean).length;
    }
    return { kept, total_words: totalWords };
}
module.exports = boundedLogProcessor;

P045
function topKFrequent(nums, k) {
    if (k <= 0 || !nums.length) return [];
    const freq = new Map();
    for (const n of nums) freq.set(n, (freq.get(n) || 0) + 1);
    const items = [...freq.entries()].sort((a, b) => {
        if (b[1] !== a[1]) return b[1] - a[1];
        return a[0] - b[0];
    });
    const selected = items.slice(0, k).map(x => x[0]);
    return selected.sort((a, b) => a - b);
}
module.exports = topKFrequent;

P046
function validateTokenFormat(token) {
    return /^[a-zA-Z][a-zA-Z0-9\-]{7,31}$/.test(token) ? 'valid' : 'invalid';
}
module.exports = validateTokenFormat;

P047
function evaluatePermission(role, action) {
    const perms = {
        admin: new Set(['read', 'write', 'delete', 'execute']),
        editor: new Set(['read', 'write']),
        viewer: new Set(['read']),
        guest: new Set()
    };
    if (perms[role] && perms[role].has(action)) return 'allowed';
    return 'denied';
}
module.exports = evaluatePermission;

P048
function roleHasPermission(role, permission) {
    const perms = {
        admin: new Set(['read', 'write', 'delete', 'execute']),
        editor: new Set(['read', 'write']),
        viewer: new Set(['read']),
        guest: new Set()
    };
    return !!(perms[role] && perms[role].has(permission));
}
module.exports = roleHasPermission;

P049
function checkSession(lastActive, currentTime, timeout) {
    if (currentTime < lastActive) return 'invalid';
    const elapsed = currentTime - lastActive;
    if (elapsed > timeout) return 'expired';
    return 'active';
}
module.exports = checkSession;

P050
function validateScope(requested, allowed) {
    if (!allowed || !allowed.length) return 'denied';
    if (allowed.includes(requested)) return 'granted';
    const parts = requested.split(':');
    for (let i = 1; i < parts.length; i++) {
        const parent = parts.slice(0, i).join(':');
        if (allowed.includes(parent)) return 'granted';
    }
    return 'denied';
}
module.exports = validateScope;