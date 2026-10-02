import csv
import re


# P001: Two Sum
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return sorted([seen[complement], i])
        seen[n] = i
    return []


# P002: Maximum Subarray Sum
def max_subarray(nums: list[int]) -> int:
    best = nums[0]
    current = nums[0]
    for n in nums[1:]:
        current = max(n, current + n)
        best = max(best, current)
    return best


# P003: Binary Search
def binary_search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# P004: Merge Sorted Arrays
def merge_sorted_arrays(nums1: list[int], nums2: list[int]) -> list[int]:
    result = []
    i, j = 0, 0
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            result.append(nums1[i])
            i += 1
        else:
            result.append(nums2[j])
            j += 1
    result.extend(nums1[i:])
    result.extend(nums2[j:])
    return result


# P005: Balanced Brackets
def is_balanced(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


# P006: CSV Record Field Count
def csv_field_count(line: str) -> int:
    if line == "":
        return 0
    row = next(csv.reader([line]))
    return len(row)


# P007: Log Level Counter
def count_log_levels(log: str) -> dict:
    levels = {"ERROR": 0, "WARNING": 0, "INFO": 0, "DEBUG": 0}
    for line in log.splitlines():
        for level in levels:
            if line.startswith(level + " ") or line.startswith(level + ":"):
                levels[level] += 1
                break
    return levels


# P008: Key-Value Parser
def parse_key_value(s: str) -> dict:
    result = {}
    if s == "":
        return result
    for pair in s.split(","):
        key, value = pair.split("=", 1)
        result[key.strip()] = value.strip()
    return dict(sorted(result.items()))


# P009: Date Format Normalizer
def normalize_date(date: str) -> str:
    if "/" in date:
        mm, dd, yyyy = date.split("/")
        return f"{yyyy}-{mm}-{dd}"
    if "-" in date:
        dd, mm, yyyy = date.split("-")
        return f"{yyyy}-{mm}-{dd}"
    yyyy, mm, dd = date.split(".")
    return f"{yyyy}-{mm}-{dd}"


# P010: Word Frequency
def word_frequency(text: str) -> dict:
    words = re.findall(r"[A-Za-z]+", text.lower())
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return dict(ordered)


# P011: Email Validator
def is_valid_email(email: str) -> bool:
    if email.count("@") != 1:
        return False
    local, domain = email.split("@")
    if not re.fullmatch(r"[a-zA-Z0-9._%+-]+", local):
        return False
    if local.startswith(".") or local.endswith(".") or ".." in local:
        return False
    labels = domain.split(".")
    if len(labels) < 2:
        return False
    for label in labels:
        if not label or label.startswith("-") or label.endswith("-"):
            return False
        if not re.fullmatch(r"[a-zA-Z0-9-]+", label):
            return False
    tld = labels[-1]
    return bool(re.fullmatch(r"[a-zA-Z]{2,6}", tld))


# P012: Password Policy Validator
def is_valid_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*]", password):
        return False
    return True


# P013: Integer Range Validator
def is_valid_range(s: str) -> str:
    parts = s.split("|")
    if len(parts) != 3:
        return "INVALID"
    try:
        value, lo, hi = (int(p) for p in parts)
    except ValueError:
        return "INVALID"
    return "VALID" if lo <= value <= hi else "INVALID"


# P014: IPv4 Validator
def is_valid_ipv4(ip: str) -> bool:
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for p in parts:
        if not p.isdigit():
            return False
        if len(p) > 1 and p[0] == "0":
            return False
        if int(p) > 255:
            return False
    return True


# P015: Username Validator
def is_valid_username(username: str) -> bool:
    if not (3 <= len(username) <= 20):
        return False
    return bool(re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", username))


# P016: HTML Text Escaper
def escape_html(s: str) -> str:
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    s = s.replace("'", "&#39;")
    return s


# P017: CSV Cell Escaper
def escape_csv_cell(s: str) -> str:
    if any(c in s for c in [",", '"', "\n", "\r"]):
        return '"' + s.replace('"', '""') + '"'
    return s


# P018: JSON String Escaper
def escape_json_string(s: str) -> str:
    out = []
    for ch in s:
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ch == "/":
            out.append("\\/")
        elif ch == "\b":
            out.append("\\b")
        elif ch == "\f":
            out.append("\\f")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif ord(ch) < 0x20:
            out.append(f"\\u{ord(ch):04x}")
        else:
            out.append(ch)
    return "".join(out)


# P019: URL Query Component Encoder
def encode_url_component(s: str) -> str:
    unreserved = set(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~"
    )
    out = []
    for byte in s.encode("utf-8"):
        ch = chr(byte)
        if byte < 128 and ch in unreserved:
            out.append(ch)
        else:
            out.append(f"%{byte:02X}")
    return "".join(out)


# P020: Template Placeholder Sanitizer
def sanitize_template(s: str) -> str:
    def repl(m):
        key = m.group(1)
        if re.fullmatch(r"[a-zA-Z0-9_]+", key):
            return "{{" + key + "}}"
        return ""

    return re.sub(r"\{\{(.*?)\}\}", repl, s)


# P021: Safe Path Normalizer
def safe_path_normalize(path: str) -> str:
    if path.strip() == "":
        return ""
    stack = []
    for part in path.split("/"):
        if part == "" or part == ".":
            continue
        if part == "..":
            if not stack:
                return ""
            stack.pop()
        else:
            stack.append(part)
    return "/".join(stack)


# P022: Path Extension Validator
def is_allowed_extension(path: str) -> bool:
    allowed = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".csv"}
    filename = path.replace("\\", "/").split("/")[-1]
    idx = filename.rfind(".")
    if idx <= 0:
        return False
    ext = filename[idx:].lower()
    return ext in allowed


# P023: Filename Sanitizer
def sanitize_filename(name: str) -> str:
    name = name[:200]
    name = re.sub(r"[^a-zA-Z0-9._-]", "_", name)
    name = re.sub(r"_+", "_", name)
    name = name.strip("_")
    return name if name else "_"


# P024: Archive Entry Path Checker
def check_archive_entry(path: str) -> str:
    if path == "":
        return "safe"
    if path.startswith("/"):
        return "unsafe"
    if "\\" in path:
        return "unsafe"
    depth = 0
    for part in path.split("/"):
        if part == "" or part == ".":
            continue
        if part == "..":
            depth -= 1
            if depth < 0:
                return "unsafe"
        else:
            depth += 1
    return "safe"


# P025: File Type Allowlist
def is_allowed_filetype(ext: str) -> bool:
    allowed = {"jpg", "jpeg", "png", "gif", "bmp", "pdf", "txt", "csv", "json", "xml"}
    if ext == "":
        return False
    if ext.startswith("."):
        ext = ext[1:]
    return ext.lower() in allowed


# P026: SQL Identifier Validator
def is_valid_sql_identifier(name: str) -> bool:
    if not (1 <= len(name) <= 64):
        return False
    return bool(re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", name))


# P027: SQL String Literal Escaper
def escape_sql_string(s: str) -> str:
    s = s.replace("\\", "\\\\")
    s = s.replace("'", "''")
    return s


# P028: Parameterized Query Builder
def build_param_query(s: str) -> str:
    if s.count("|") != 1:
        return "INVALID"
    table, cols = s.split("|")
    if not is_valid_sql_identifier(table):
        return "INVALID"
    if cols == "":
        return "INVALID"
    conditions = []
    for pair in cols.split(","):
        if "=" not in pair:
            return "INVALID"
        col, _ = pair.split("=", 1)
        if not is_valid_sql_identifier(col):
            return "INVALID"
        conditions.append(f"{col}=?")
    return "SELECT * FROM " + table + " WHERE " + " AND ".join(conditions)


# P029: Sort Direction Validator
def validate_sort_direction(s: str) -> str:
    s = s.strip().upper()
    return s if s in ("ASC", "DESC") else "INVALID"


# P030: Column Allowlist Checker
def is_allowed_column(col: str) -> bool:
    allowed = {"id", "name", "email", "created_at", "status", "age", "role", "score"}
    return col.strip() in allowed


# P031: Shell Argument Quoter
def quote_shell_arg(s: str) -> str:
    return "'" + s.replace("'", "'\\''") + "'"


# P032: Command Name Allowlist
def is_allowed_command(s: str) -> bool:
    allowed = {"ls", "cat", "echo", "grep", "find", "sort", "uniq", "wc", "head", "tail"}
    s = s.strip()
    if " " in s:
        return False
    return s in allowed


# P033: Shell Metacharacter Detector
def detect_shell_meta(s: str) -> str:
    dangerous = set(';|&$`><(){}\\"\'\n\r')
    return "unsafe" if any(c in dangerous for c in s) else "safe"


# P034: Environment Variable Name Validator
def is_valid_env_var(name: str) -> bool:
    if not (1 <= len(name) <= 64):
        return False
    return bool(re.fullmatch(r"[A-Z_][A-Z0-9_]*", name))


# P035: Command Argument Splitter
def split_args(s: str) -> list[str]:
    tokens = []
    i, n = 0, len(s)
    while i < n:
        while i < n and s[i] == " ":
            i += 1
        if i >= n:
            break
        if s[i] == '"':
            j = i + 1
            start = j
            while j < n and s[j] != '"':
                j += 1
            tokens.append(s[start:j])
            i = j + 1
        else:
            start = i
            while i < n and s[i] != " ":
                i += 1
            tokens.append(s[start:i])
    return tokens


# P036: Safe Literal Parser
def parse_safe_literal(s: str) -> str:
    if s == "true" or s == "false":
        return s
    if s == "null":
        return "null"
    if re.fullmatch(r"-?(0|[1-9][0-9]*)", s):
        return s
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        inner = s[1:-1]
        out = []
        i = 0
        while i < len(inner):
            if inner[i] == "\\" and i + 1 < len(inner) and inner[i + 1] == '"':
                out.append('"')
                i += 2
            elif inner[i] == '"':
                return "INVALID"
            else:
                out.append(inner[i])
                i += 1
        return "".join(out)
    return "INVALID"


# P037: Configuration Boolean Parser
def parse_config_bool(s: str) -> str:
    s = s.strip().lower()
    if s in ("true", "yes", "1", "on", "enabled"):
        return "true"
    if s in ("false", "no", "0", "off", "disabled"):
        return "false"
    return "INVALID"


# P038: Configuration Key Allowlist
def is_allowed_config_key(key: str) -> bool:
    allowed = {
        "host", "port", "database", "username", "password", "timeout",
        "max_connections", "ssl_enabled", "log_level", "retry_count",
    }
    return key.strip() in allowed


# P039: Structured Token Decoder
def validate_token(s: str) -> str:
    parts = s.split(".")
    if len(parts) != 3:
        return "invalid"
    header, payload, checksum = parts
    if not re.fullmatch(r"[A-Za-z0-9_-]+", header):
        return "invalid"
    if not re.fullmatch(r"[A-Za-z0-9_-]+", payload):
        return "invalid"
    if not re.fullmatch(r"[0-9a-f]{8}", checksum):
        return "invalid"
    return "valid"


# P040: Safe Numeric Expression Validator
def validate_numeric_expr(s: str) -> str:
    number = r"-?(0|[1-9][0-9]*)"
    pattern = rf"^\s*{number}\s*([+\-*/]\s*{number}\s*)*$"
    return "valid" if re.fullmatch(pattern, s) else "invalid"


# P041: Frequency Counter Large Input
def frequency_counter(nums: list[int]) -> dict:
    counts = {}
    for n in nums:
        counts[n] = counts.get(n, 0) + 1
    return {str(k): counts[k] for k in sorted(counts)}


# P042: Duplicate Detector
def has_duplicate(nums: list[int]) -> bool:
    return len(set(nums)) != len(nums)


# P043: Streaming Sum
def streaming_sum(nums: list[int]) -> int:
    return sum(nums)


# P044: Bounded Log Processor
def bounded_log_processor(log: str, max_lines: int) -> dict:
    if max_lines <= 0 or log == "":
        return {"kept": 0, "total_words": 0}
    kept = 0
    total_words = 0
    for line in log.splitlines():
        if line.strip() == "":
            continue
        if kept >= max_lines:
            break
        kept += 1
        total_words += len(line.split())
    return {"kept": kept, "total_words": total_words}


# P045: Top-K Frequent Values
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    if k <= 0 or not nums:
        return []
    counts = {}
    for n in nums:
        counts[n] = counts.get(n, 0) + 1
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    top = [val for val, _ in ordered[:k]]
    return sorted(top)


# P046: Token Format Validator
def validate_token_format(token: str) -> str:
    if re.fullmatch(r"[a-zA-Z][a-zA-Z0-9-]{7,31}", token):
        return "valid"
    return "invalid"


_PERMISSION_TABLE = {
    "admin": {"read", "write", "delete", "execute"},
    "editor": {"read", "write"},
    "viewer": {"read"},
    "guest": set(),
}


# P047: Permission Rule Evaluator
def evaluate_permission(role: str, action: str) -> str:
    return "allowed" if action in _PERMISSION_TABLE.get(role, set()) else "denied"


# P048: Role Permission Checker
def role_has_permission(role: str, permission: str) -> bool:
    return permission in _PERMISSION_TABLE.get(role, set())


# P049: Session Timeout Checker
def check_session(last_active: int, current_time: int, timeout: int) -> str:
    if current_time < last_active:
        return "invalid"
    elapsed = current_time - last_active
    return "expired" if elapsed > timeout else "active"


# P050: Access Scope Validator
def validate_scope(requested: str, allowed: list[str]) -> str:
    if not allowed:
        return "denied"
    parts = requested.split(":")
    prefixes = [":".join(parts[: i + 1]) for i in range(len(parts))]
    return "granted" if any(p in allowed for p in prefixes) else "denied"
