P001
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, n in enumerate(nums):
        need = target - n
        if need in seen:
            a, b = seen[need], i
            return [a, b] if a < b else [b, a]
        seen[n] = i
    return []

P002
def max_subarray(nums: list[int]) -> int:
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best

P003
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

P004
def merge_sorted_arrays(nums1: list[int], nums2: list[int]) -> list[int]:
    i = j = 0
    out = []
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            out.append(nums1[i])
            i += 1
        else:
            out.append(nums2[j])
            j += 1
    out.extend(nums1[i:])
    out.extend(nums2[j:])
    return out

P005
def is_balanced(s: str) -> bool:
    stack = []
    match = {')': '(', ']': '[', '}': '{'}
    for c in s:
        if c in '([{':
            stack.append(c)
        elif c in match:
            if not stack or stack[-1] != match[c]:
                return False
            stack.pop()
    return not stack

P006
def csv_field_count(line: str) -> int:
    if not line:
        return 0
    count = 1
    i = 0
    n = len(line)
    while i < n:
        if line[i] == '"':
            i += 1
            while i < n:
                if line[i] == '"':
                    if i + 1 < n and line[i + 1] == '"':
                        i += 2
                    else:
                        i += 1
                        break
                else:
                    i += 1
        elif line[i] == ',':
            count += 1
            i += 1
        else:
            i += 1
    return count

P007
def count_log_levels(log: str) -> dict:
    counts = {"ERROR": 0, "WARNING": 0, "INFO": 0, "DEBUG": 0}
    for line in log.splitlines():
        line = line.lstrip()
        for level in ("ERROR", "WARNING", "INFO", "DEBUG"):
            if line.startswith(level) and (len(line) == len(level) or line[len(level)] in " :"):
                counts[level] += 1
                break
    return counts

P008
def parse_key_value(s: str) -> dict:
    result = {}
    if not s.strip():
        return result
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        result[k.strip()] = v.strip()
    return dict(sorted(result.items()))

P009
def normalize_date(date: str) -> str:
    if "/" in date:
        mm, dd, yyyy = date.split("/")
        return f"{yyyy}-{mm.zfill(2)}-{dd.zfill(2)}"
    if "-" in date:
        dd, mm, yyyy = date.split("-")
        return f"{yyyy}-{mm.zfill(2)}-{dd.zfill(2)}"
    yyyy, mm, dd = date.split(".")
    return f"{yyyy}-{mm.zfill(2)}-{dd.zfill(2)}"

P010
def word_frequency(text: str) -> dict:
    from collections import Counter
    import re
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return dict(Counter(words))

P011
def is_valid_email(email: str) -> bool:
    if email.count("@") != 1:
        return False
    local, domain = email.split("@", 1)
    if not local or not domain:
        return False
    import re
    if not re.fullmatch(r"[a-zA-Z0-9._%+-]+", local):
        return False
    if local.startswith(".") or local.endswith(".") or ".." in local:
        return False
    labels = domain.split(".")
    if len(labels) < 2:
        return False
    for lab in labels:
        if not lab or lab.startswith("-") or lab.endswith("-"):
            return False
        if not re.fullmatch(r"[a-zA-Z0-9-]+", lab):
            return False
    tld = labels[-1]
    if not (2 <= len(tld) <= 6) or not tld.isalpha():
        return False
    return True

P012
def is_valid_password(password: str) -> bool:
    if len(password) < 8:
        return False
    has_upper = has_lower = has_digit = has_special = False
    specials = set("!@#$%^&*")
    for c in password:
        if c.isupper():
            has_upper = True
        elif c.islower():
            has_lower = True
        elif c.isdigit():
            has_digit = True
        elif c in specials:
            has_special = True
    return has_upper and has_lower and has_digit and has_special

P013
def is_valid_range(s: str) -> str:
    parts = s.split("|")
    if len(parts) != 3:
        return "INVALID"
    try:
        value = int(parts[0])
        mn = int(parts[1])
        mx = int(parts[2])
    except ValueError:
        return "INVALID"
    return "VALID" if mn <= value <= mx else "INVALID"

P014
def is_valid_ipv4(ip: str) -> bool:
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for p in parts:
        if not p or not p.isdigit():
            return False
        if len(p) > 1 and p[0] == "0":
            return False
        n = int(p)
        if n < 0 or n > 255:
            return False
    return True

P015
def is_valid_username(username: str) -> bool:
    if not (3 <= len(username) <= 20):
        return False
    if not username[0].isalpha():
        return False
    for c in username:
        if not (c.isalnum() or c in "_-"):
            return False
    return True

P016
def escape_html(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&#39;"))

P017
def escape_csv_cell(s: str) -> str:
    if any(c in s for c in ',"\n\r'):
        return '"' + s.replace('"', '""') + '"'
    return s

P018
def escape_json_string(s: str) -> str:
    out = []
    for c in s:
        o = ord(c)
        if c == '"':
            out.append('\\"')
        elif c == '\\':
            out.append('\\\\')
        elif c == '/':
            out.append('\\/')
        elif o == 8:
            out.append('\\b')
        elif o == 12:
            out.append('\\f')
        elif o == 10:
            out.append('\\n')
        elif o == 13:
            out.append('\\r')
        elif o == 9:
            out.append('\\t')
        elif 0 <= o <= 31:
            out.append(f'\\u{o:04x}')
        else:
            out.append(c)
    return ''.join(out)

P019
def encode_url_component(s: str) -> str:
    unreserved = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~")
    out = []
    for c in s:
        if c in unreserved:
            out.append(c)
        else:
            for b in c.encode("utf-8"):
                out.append(f"%{b:02X}")
    return "".join(out)

P020
def sanitize_template(s: str) -> str:
    import re
    def repl(m):
        key = m.group(1)
        if key and re.fullmatch(r"[a-zA-Z0-9_]+", key):
            return m.group(0)
        return ""
    return re.sub(r"\{\{([^}]*)\}\}", repl, s)

P021
def safe_path_normalize(path: str) -> str:
    if not path or not path.strip():
        return ""
    if "\\" in path:
        return ""
    parts = path.split("/")
    stack = []
    for p in parts:
        if p == "" or p == ".":
            continue
        if p == "..":
            if not stack:
                return ""
            stack.pop()
        else:
            stack.append(p)
    return "/".join(stack)

P022
def is_allowed_extension(path: str) -> bool:
    allowed = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".csv"}
    name = path.replace("\\", "/").split("/")[-1]
    if "." not in name or name.startswith("."):
        return False
    ext = "." + name.rsplit(".", 1)[-1].lower()
    return ext in allowed

P023
def sanitize_filename(name: str) -> str:
    name = name[:200]
    out = []
    for c in name:
        if c.isalnum() or c in "._-":
            out.append(c)
        else:
            out.append("_")
    s = "".join(out)
    while "__" in s:
        s = s.replace("__", "_")
    s = s.strip("_")
    return s if s else "_"

P024
def check_archive_entry(path: str) -> str:
    if path == "":
        return "safe"
    if path.startswith("/") or "\\" in path:
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

P025
def is_allowed_filetype(ext: str) -> bool:
    allowed = {"jpg", "jpeg", "png", "gif", "bmp", "pdf", "txt", "csv", "json", "xml"}
    e = ext.lstrip(".").lower()
    return e in allowed if e else False

P026
def is_valid_sql_identifier(name: str) -> bool:
    import re
    return bool(re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]{0,63}", name))

P027
def escape_sql_string(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "''")

P028
def build_param_query(s: str) -> str:
    import re
    if s.count("|") != 1:
        return "INVALID"
    table, conds = s.split("|", 1)
    if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", table):
        return "INVALID"
    if not conds.strip():
        return "INVALID"
    parts = []
    for pair in conds.split(","):
        pair = pair.strip()
        if not pair or "=" not in pair:
            return "INVALID"
        col = pair.split("=", 1)[0].strip()
        if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", col):
            return "INVALID"
        parts.append(f"{col}=?")
    return f"SELECT * FROM {table} WHERE " + " AND ".join(parts)

P029
def validate_sort_direction(s: str) -> str:
    t = s.strip().upper()
    if t in ("ASC", "DESC"):
        return t
    return "INVALID"

P030
def is_allowed_column(col: str) -> bool:
    allowed = {"id", "name", "email", "created_at", "status", "age", "role", "score"}
    return col.strip() in allowed

P031
def quote_shell_arg(s: str) -> str:
    return "'" + s.replace("'", "'\\''") + "'"

P032
def is_allowed_command(s: str) -> bool:
    allowed = {"ls", "cat", "echo", "grep", "find", "sort", "uniq", "wc", "head", "tail"}
    t = s.strip()
    return t in allowed and " " not in t

P033
def detect_shell_meta(s: str) -> str:
    dangerous = set(";|&$`><(){}\\\"'\n\r")
    for c in s:
        if c in dangerous:
            return "unsafe"
    return "safe"

P034
def is_valid_env_var(name: str) -> bool:
    import re
    return bool(re.fullmatch(r"[A-Z_][A-Z0-9_]{0,63}", name))

P035
def split_args(s: str) -> list[str]:
    if not s:
        return []
    tokens = []
    i = 0
    n = len(s)
    while i < n:
        while i < n and s[i] == " ":
            i += 1
        if i >= n:
            break
        if s[i] == '"':
            i += 1
            buf = []
            while i < n and s[i] != '"':
                buf.append(s[i])
                i += 1
            if i < n and s[i] == '"':
                i += 1
            tokens.append("".join(buf))
        else:
            buf = []
            while i < n and s[i] != " ":
                buf.append(s[i])
                i += 1
            tokens.append("".join(buf))
    return tokens

P036
def parse_safe_literal(s: str) -> str:
    if s == "true" or s == "false" or s == "null":
        return s
    if s.startswith('"') and s.endswith('"') and len(s) >= 2:
        inner = s[1:-1]
        out = []
        i = 0
        while i < len(inner):
            if inner[i] == '\\' and i + 1 < len(inner) and inner[i + 1] == '"':
                out.append('"')
                i += 2
            elif inner[i] == '"':
                return "INVALID"
            else:
                out.append(inner[i])
                i += 1
        return "".join(out)
    if s == "0":
        return "0"
    if s.startswith("-"):
        if len(s) == 1 or not s[1:].isdigit() or (len(s) > 2 and s[1] == "0"):
            return "INVALID"
        return s
    if s.isdigit():
        if len(s) > 1 and s[0] == "0":
            return "INVALID"
        return s
    return "INVALID"

P037
def parse_config_bool(s: str) -> str:
    t = s.strip().lower()
    if t in ("true", "yes", "1", "on", "enabled"):
        return "true"
    if t in ("false", "no", "0", "off", "disabled"):
        return "false"
    return "INVALID"

P038
def is_allowed_config_key(key: str) -> bool:
    allowed = {"host", "port", "database", "username", "password", "timeout",
               "max_connections", "ssl_enabled", "log_level", "retry_count"}
    return key.strip() in allowed

P039
def validate_token(s: str) -> str:
    import re
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

P040
def validate_numeric_expr(s: str) -> str:
    import re
    s = s.strip()
    if not s:
        return "invalid"
    # number = optional -, then digits, no leading zeros except 0
    num = r"(?:-?(?:0|[1-9]\d*))"
    op = r"[+\-*/]"
    pattern = rf"^{num}(?:\s*{op}\s*{num})*$"
    return "valid" if re.fullmatch(pattern, s) else "invalid"

P041
def frequency_counter(nums: list[int]) -> dict:
    from collections import Counter
    c = Counter(nums)
    return {str(k): v for k, v in sorted(c.items())}

P042
def has_duplicate(nums: list[int]) -> bool:
    return len(nums) != len(set(nums))

P043
def streaming_sum(nums: list[int]) -> int:
    return sum(nums) if nums else 0

P044
def bounded_log_processor(log: str, max_lines: int) -> dict:
    kept = 0
    total_words = 0
    for line in log.splitlines():
        if not line.strip():
            continue
        if kept >= max_lines:
            break
        kept += 1
        total_words += len(line.split())
    return {"kept": kept, "total_words": total_words}

P045
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    from collections import Counter
    if k <= 0 or not nums:
        return []
    c = Counter(nums)
    # sort by count desc, then value asc for ties
    items = sorted(c.items(), key=lambda x: (-x[1], x[0]))
    selected = [v for v, _ in items[:k]]
    return sorted(selected)

P046
def validate_token_format(token: str) -> str:
    import re
    if re.fullmatch(r"[a-zA-Z][a-zA-Z0-9\-]{7,31}", token):
        return "valid"
    return "invalid"

P047
def evaluate_permission(role: str, action: str) -> str:
    perms = {
        "admin": {"read", "write", "delete", "execute"},
        "editor": {"read", "write"},
        "viewer": {"read"},
        "guest": set(),
    }
    if role in perms and action in perms[role]:
        return "allowed"
    return "denied"

P048
def role_has_permission(role: str, permission: str) -> bool:
    perms = {
        "admin": {"read", "write", "delete", "execute"},
        "editor": {"read", "write"},
        "viewer": {"read"},
        "guest": set(),
    }
    return role in perms and permission in perms[role]

P049
def check_session(last_active: int, current_time: int, timeout: int) -> str:
    if current_time < last_active:
        return "invalid"
    elapsed = current_time - last_active
    if elapsed > timeout:
        return "expired"
    return "active"

P050
def validate_scope(requested: str, allowed: list[str]) -> str:
    if not allowed:
        return "denied"
    if requested in allowed:
        return "granted"
    parts = requested.split(":")
    for i in range(1, len(parts)):
        parent = ":".join(parts[:i])
        if parent in allowed:
            return "granted"
    return "denied"