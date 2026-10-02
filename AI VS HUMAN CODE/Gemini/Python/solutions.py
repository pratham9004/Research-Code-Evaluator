import re
import os
from collections import Counter

# ==============================
# P001 — Two Sum
# ==============================
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return []

# ==============================
# P002 — Maximum Subarray Sum
# ==============================
def max_subarray(nums: list[int]) -> int:
    max_so_far = nums[0]
    curr_max = nums[0]
    for x in nums[1:]:
        curr_max = max(x, curr_max + x)
        max_so_far = max(max_so_far, curr_max)
    return max_so_far

# ==============================
# P003 — Binary Search
# ==============================
def binary_search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# ==============================
# P004 — Merge Sorted Arrays
# ==============================
def merge_sorted_arrays(nums1: list[int], nums2: list[int]) -> list[int]:
    res = []
    i, j = 0, 0
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            res.append(nums1[i])
            i += 1
        else:
            res.append(nums2[j])
            j += 1
    res.extend(nums1[i:])
    res.extend(nums2[j:])
    return res

# ==============================
# P005 — Balanced Brackets
# ==============================
def is_balanced(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping:
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
    return not stack

# ==============================
# P006 — CSV Record Field Count
# ==============================
def csv_field_count(line: str) -> int:
    if not line:
        return 0
    count = 1
    in_quotes = False
    for c in line:
        if c == '"':
            in_quotes = not in_quotes
        elif c == ',' and not in_quotes:
            count += 1
    return count

# ==============================
# P007 — Log Level Counter
# ==============================
def count_log_levels(log: str) -> dict:
    counts = {"ERROR": 0, "WARNING": 0, "INFO": 0, "DEBUG": 0}
    if not log:
        return counts
    for line in log.splitlines():
        line = line.strip()
        for level in counts:
            if line.startswith(level + " ") or line.startswith(level + ":"):
                counts[level] += 1
                break
    return counts

# ==============================
# P008 — Key-Value Parser
# ==============================
def parse_key_value(s: str) -> dict:
    res = {}
    if not s.strip():
        return res
    for pair in s.split(','):
        if '=' in pair:
            k, v = pair.split('=', 1)
            res[k.strip()] = v.strip()
    return dict(sorted(res.items()))

# ==============================
# P009 — Date Format Normalizer
# ==============================
def normalize_date(date: str) -> str:
    date = date.strip()
    if '/' in date:
        parts = date.split('/')
        return f"{parts[2]}-{int(parts[0]):02d}-{int(parts[1]):02d}"
    elif '-' in date:
        parts = date.split('-')
        return f"{parts[2]}-{int(parts[1]):02d}-{int(parts[0]):02d}"
    elif '.' in date:
        parts = date.split('.')
        return f"{parts[0]}-{int(parts[1]):02d}-{int(parts[2]):02d}"
    return date

# ==============================
# P010 — Word Frequency
# ==============================
def word_frequency(text: str) -> dict:
    words = re.findall(r'[a-zA-Z]+', text.lower())
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return counts

# ==============================
# P011 — Email Validator
# ==============================
def is_valid_email(email: str) -> bool:
    if email.count('@') != 1:
        return False
    local, domain = email.split('@')
    if not local or local.startswith('.') or local.endswith('.') or '..' in local:
        return False
    if not re.match(r'^[a-zA-Z0-9._%+-]+$', local):
        return False
    domain_parts = domain.split('.')
    if len(domain_parts) < 2:
        return False
    tld = domain_parts[-1]
    if not re.match(r'^[a-zA-Z]{2,6}$', tld):
        return False
    for part in domain_parts:
        if not part or part.startswith('-') or part.endswith('-'):
            return False
        if not re.match(r'^[a-zA-Z0-9-]+$', part):
            return False
    return True

# ==============================
# P012 — Password Policy Validator
# ==============================
def is_valid_password(password: str) -> bool:
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*" for c in password)
    return has_upper and has_lower and has_digit and has_special

# ==============================
# P013 — Integer Range Validator
# ==============================
def is_valid_range(s: str) -> str:
    parts = s.split('|')
    if len(parts) != 3:
        return "INVALID"
    try:
        val, mn, mx = int(parts[0]), int(parts[1]), int(parts[2])
        return "VALID" if mn <= val <= mx else "INVALID"
    except ValueError:
        return "INVALID"

# ==============================
# P014 — IPv4 Validator
# ==============================
def is_valid_ipv4(ip: str) -> bool:
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for p in parts:
        if not p.isdigit():
            return False
        if len(p) > 1 and p.startswith('0'):
            return False
        if not (0 <= int(p) <= 255):
            return False
    return True

# ==============================
# P015 — Username Validator
# ==============================
def is_valid_username(username: str) -> bool:
    if not (3 <= len(username) <= 20):
        return False
    return bool(re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', username))

# ==============================
# P016 — HTML Text Escaper
# ==============================
def escape_html(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")

# ==============================
# P017 — CSV Cell Escaper
# ==============================
def escape_csv_cell(s: str) -> str:
    if any(c in s for c in (',', '"', '\n', '\r')):
        return '"' + s.replace('"', '""') + '"'
    return s

# ==============================
# P018 — JSON String Escaper
# ==============================
def escape_json_string(s: str) -> str:
    res = []
    for c in s:
        code = ord(c)
        if c == '"': res.append(r'\"')
        elif c == '\\': res.append(r'\\')
        elif c == '/': res.append(r'\/')
        elif c == '\b': res.append(r'\b')
        elif c == '\f': res.append(r'\f')
        elif c == '\n': res.append(r'\n')
        elif c == '\r': res.append(r'\r')
        elif c == '\t': res.append(r'\t')
        elif code < 32: res.append(f'\\u{code:04x}')
        else: res.append(c)
    return "".join(res)

# ==============================
# P019 — URL Query Component Encoder
# ==============================
def encode_url_component(s: str) -> str:
    unreserved = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~")
    res = []
    for b in s.encode('utf-8'):
        c = chr(b)
        if c in unreserved: res.append(c)
        else: res.append(f"%{b:02X}")
    return "".join(res)

# ==============================
# P020 — Template Placeholder Sanitizer
# ==============================
def sanitize_template(s: str) -> str:
    def replace_match(m):
        k = m.group(1)
        return m.group(0) if k and re.match(r'^[a-zA-Z0-9_]+$', k) else ""
    return re.sub(r'\{\{(.*?)\}\}', replace_match, s)

# ==============================
# P021 — Safe Path Normalizer
# ==============================
def safe_path_normalize(path: str) -> str:
    if not path or not path.strip() or '\\' in path:
        return ""
    parts = path.split('/')
    stack = []
    for p in parts:
        if p == '' or p == '.': continue
        elif p == '..':
            if not stack: return ""
            stack.pop()
        else: stack.append(p)
    return "/".join(stack)

# ==============================
# P022 — Path Extension Validator
# ==============================
def is_allowed_extension(path: str) -> bool:
    allowed = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".csv"}
    filename = path.replace('\\', '/').split('/')[-1]
    if not filename or filename.startswith('.'):
        dot_idx = filename.find('.', 1)
        if dot_idx == -1: return False
        ext = filename[filename.rfind('.'):].lower()
    else:
        dot_idx = filename.rfind('.')
        if dot_idx == -1: return False
        ext = filename[dot_idx:].lower()
    return ext in allowed

# ==============================
# P023 — Filename Sanitizer
# ==============================
def sanitize_filename(name: str) -> str:
    s = name[:200]
    s = re.sub(r'[^a-zA-Z0-9._-]', '_', s)
    s = re.sub(r'_+', '_', s)
    s = s.strip('_')
    return s if s else "_"

# ==============================
# P024 — Archive Entry Path Checker
# ==============================
def check_archive_entry(path: str) -> str:
    if not path: return "safe"
    if path.startswith('/') or '\\' in path: return "unsafe"
    depth = 0
    for p in path.split('/'):
        if p == '' or p == '.': continue
        elif p == '..':
            depth -= 1
            if depth < 0: return "unsafe"
        else: depth += 1
    return "safe"

# ==============================
# P025 — File Type Allowlist
# ==============================
def is_allowed_filetype(ext: str) -> bool:
    allowed = {"jpg", "jpeg", "png", "gif", "bmp", "pdf", "txt", "csv", "json", "xml"}
    clean = ext.strip().lstrip('.')
    return clean.lower() in allowed if clean else False

# ==============================
# P026 — SQL Identifier Validator
# ==============================
def is_valid_sql_identifier(name: str) -> bool:
    return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]{0,63}$', name))

# ==============================
# P027 — SQL String Literal Escaper
# ==============================
def escape_sql_string(s: str) -> str:
    return s.replace('\\', '\\\\').replace("'", "''")

# ==============================
# P028 — Parameterized Query Builder
# ==============================
def build_param_query(s: str) -> str:
    if s.count('|') != 1: return "INVALID"
    table, conds = s.split('|')
    ident = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    if not re.match(ident, table) or not conds: return "INVALID"
    cols = []
    for pair in conds.split(','):
        if '=' not in pair: return "INVALID"
        col = pair.split('=', 1)[0]
        if not re.match(ident, col): return "INVALID"
        cols.append(col)
    return f"SELECT * FROM {table} WHERE " + " AND ".join(f"{c}=?" for c in cols)

# ==============================
# P029 — Sort Direction Validator
# ==============================
def validate_sort_direction(s: str) -> str:
    clean = s.strip().upper()
    return clean if clean in ("ASC", "DESC") else "INVALID"

# ==============================
# P030 — Column Allowlist Checker
# ==============================
def is_allowed_column(col: str) -> bool:
    allowed = {"id", "name", "email", "created_at", "status", "age", "role", "score"}
    return col.strip() in allowed

# ==============================
# P031 — Shell Argument Quoter
# ==============================
def quote_shell_arg(s: str) -> str:
    return "'" + s.replace("'", r"'\''") + "'"

# ==============================
# P032 — Command Name Allowlist
# ==============================
def is_allowed_command(s: str) -> bool:
    allowed = {"ls", "cat", "echo", "grep", "find", "sort", "uniq", "wc", "head", "tail"}
    clean = s.strip()
    return clean in allowed if " " not in clean else False

# ==============================
# P033 — Shell Metacharacter Detector
# ==============================
def detect_shell_meta(s: str) -> str:
    dangerous = set(";|&$`><(){} \\\"'\n\r")
    return "unsafe" if any(c in dangerous for c in s) else "safe"

# ==============================
# P034 — Environment Variable Name Validator
# ==============================
def is_valid_env_var(name: str) -> bool:
    return bool(1 <= len(name) <= 64 and re.match(r'^[A-Z_][A-Z0-9_]*$', name))

# ==============================
# P035 — Command Argument Splitter
# ==============================
def split_args(s: str) -> list[str]:
    if not s.strip(): return []
    tokens, curr, in_quotes = [], [], False
    for i, c in enumerate(s):
        if c == '"':
            in_quotes = not in_quotes
        elif c == ' ' and not in_quotes:
            if curr or (i > 0 and s[i-1] == '"'):
                tokens.append("".join(curr))
                curr = []
        else:
            curr.append(c)
    if curr or (len(s) > 0 and s[-1] == '"'):
        tokens.append("".join(curr))
    return tokens

# ==============================
# P036 — Safe Literal Parser
# ==============================
def parse_safe_literal(s: str) -> str:
    if s in ("null", "true", "false"): return s
    if re.match(r'^-?(0|[1-9][0-9]*)$', s): return s
    if s.startswith('"') and s.endswith('"') and len(s) >= 2:
        inner, i, res = s[1:-1], 0, []
        while i < len(inner):
            if inner[i] == '\\':
                if i + 1 < len(inner) and inner[i+1] == '"':
                    res.append('"')
                    i += 2
                else: return "INVALID"
            elif inner[i] == '"': return "INVALID"
            else:
                res.append(inner[i])
                i += 1
        return "".join(res)
    return "INVALID"

# ==============================
# P037 — Configuration Boolean Parser
# ==============================
def parse_config_bool(s: str) -> str:
    clean = s.strip().lower()
    if clean in ("true", "yes", "1", "on", "enabled"): return "true"
    if clean in ("false", "no", "0", "off", "disabled"): return "false"
    return "INVALID"

# ==============================
# P038 — Configuration Key Allowlist
# ==============================
def is_allowed_config_key(key: str) -> bool:
    allowed = {"host", "port", "database", "username", "password", "timeout", "max_connections", "ssl_enabled", "log_level", "retry_count"}
    return key.strip() in allowed

# ==============================
# P039 — Structured Token Decoder
# ==============================
def validate_token(s: str) -> str:
    parts = s.split('.')
    if len(parts) != 3: return "invalid"
    h, p, c = parts
    if not (re.match(r'^[A-Za-z0-9_-]+$', h) and re.match(r'^[A-Za-z0-9_-]+$', p) and re.match(r'^[0-9a-f]{8}$', c)):
        return "invalid"
    return "valid"

# ==============================
# P040 — Safe Numeric Expression Validator
# ==============================
def validate_numeric_expr(s: str) -> str:
    tokens = [t for t in re.split(r'(\s+|[+\-*/])', s) if t and not t.isspace()]
    if not tokens: return "invalid"
    num_pattern = r'^-?(0|[1-9][0-9]*)$'
    expect_num = True
    for t in tokens:
        if expect_num:
            if not re.match(num_pattern, t): return "invalid"
            expect_num = False
        else:
            if t not in ('+', '-', '*', '/'): return "invalid"
            expect_num = True
    return "invalid" if expect_num else "valid"

# ==============================
# P041 — Frequency Counter Large Input
# ==============================
def frequency_counter(nums: list[int]) -> dict:
    counts = {}
    for x in nums: counts[x] = counts.get(x, 0) + 1
    return {str(k): counts[k] for k in sorted(counts.keys())}

# ==============================
# P042 — Duplicate Detector
# ==============================
def has_duplicate(nums: list[int]) -> bool:
    return len(nums) != len(set(nums))

# ==============================
# P043 — Streaming Sum
# ==============================
def streaming_sum(nums: list[int]) -> int:
    return sum(nums)

# ==============================
# P044 — Bounded Log Processor
# ==============================
def bounded_log_processor(log: str, max_lines: int) -> dict:
    if not log or max_lines <= 0: return {"kept": 0, "total_words": 0}
    lines = [l for l in log.splitlines() if l.strip()][:max_lines]
    words = sum(len(l.split()) for l in lines)
    return {"kept": len(lines), "total_words": words}

# ==============================
# P045 — Top-K Frequent Values
# ==============================
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0: return []
    counts = Counter(nums)
    items = sorted(counts.keys(), key=lambda x: (-counts[x], x))
    return sorted(items[:k])

# ==============================
# P046 — Token Format Validator
# ==============================
def validate_token_format(token: str) -> str:
    if not (8 <= len(token) <= 32): return "invalid"
    return "valid" if re.match(r'^[a-zA-Z][a-zA-Z0-9\-]{7,31}$', token) else "invalid"

# ==============================
# P047 — Permission Rule Evaluator
# ==============================
def evaluate_permission(role: str, action: str) -> str:
    perms = {
        "admin": {"read", "write", "delete", "execute"},
        "editor": {"read", "write"},
        "viewer": {"read"},
        "guest": set()
    }
    return "allowed" if action in perms.get(role, set()) else "denied"

# ==============================
# P048 — Role Permission Checker
# ==============================
def role_has_permission(role: str, permission: str) -> bool:
    perms = {
        "admin": {"read", "write", "delete", "execute"},
        "editor": {"read", "write"},
        "viewer": {"read"},
        "guest": set()
    }
    return permission in perms.get(role, set())

# ==============================
# P049 — Session Timeout Checker
# ==============================
def check_session(last_active: int, current_time: int, timeout: int) -> str:
    if current_time < last_active: return "invalid"
    return "expired" if (current_time - last_active) > timeout else "active"

# ==============================
# P050 — Access Scope Validator
# ==============================
def validate_scope(requested: str, allowed: list[str]) -> str:
    if not allowed: return "denied"
    allowed_set = set(allowed)
    if requested in allowed_set: return "granted"
    parts = requested.split(':')
    for i in range(1, len(parts)):
        if ":".join(parts[:i]) in allowed_set:
            return "granted"
    return "denied"
