# P001
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for index, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return [seen[complement], index]
        seen[value] = index
    return []


# P002
def max_subarray(nums: list[int]) -> int:
    best = current = nums[0]
    for value in nums[1:]:
        current = max(value, current + value)
        best = max(best, current)
    return best


# P003
def binary_search(nums: list[int], target: int) -> int:
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


# P004
def merge_sorted_arrays(nums1: list[int], nums2: list[int]) -> list[int]:
    merged = []
    i = j = 0
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            merged.append(nums1[i])
            i += 1
        else:
            merged.append(nums2[j])
            j += 1
    merged.extend(nums1[i:])
    merged.extend(nums2[j:])
    return merged


# P005
def is_balanced(s: str) -> bool:
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            return False
    return not stack


# P006
def csv_field_count(line: str) -> int:
    count = 1
    in_quotes = False
    for ch in line:
        if ch == '"':
            in_quotes = not in_quotes
        elif ch == ',' and not in_quotes:
            count += 1
    return count


# P007
import re


def count_log_levels(log: str) -> dict:
    counts = {"ERROR": 0, "WARNING": 0, "INFO": 0, "DEBUG": 0}
    pattern = re.compile(r'(ERROR|WARNING|INFO|DEBUG)(?:[ :]|$)')
    for line in log.splitlines():
        match = pattern.match(line)
        if match:
            counts[match.group(1)] += 1
    return counts


# P008
def parse_key_value(s: str) -> dict:
    result = {}
    for pair in s.split(','):
        key, separator, value = pair.partition('=')
        if not separator:
            continue
        result[key.strip()] = value.strip()
    return dict(sorted(result.items()))


# P009
def normalize_date(date: str) -> str:
    if '/' in date:
        month, day, year = date.split('/')
    elif '-' in date:
        day, month, year = date.split('-')
    else:
        year, month, day = date.split('.')
    return f"{year.zfill(4)}-{month.zfill(2)}-{day.zfill(2)}"


# P010
import re


def word_frequency(text: str) -> dict:
    counts = {}
    for word in re.findall(r'[A-Za-z]+', text):
        word = word.lower()
        counts[word] = counts.get(word, 0) + 1
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return dict(ordered)


# P011
import re


def is_valid_email(email: str) -> bool:
    if email.count('@') != 1:
        return False
    local, domain = email.split('@')
    if not re.fullmatch(r'[A-Za-z0-9._%+-]+', local):
        return False
    if local.startswith('.') or local.endswith('.') or '..' in local:
        return False
    labels = domain.split('.')
    if len(labels) < 2:
        return False
    for label in labels:
        if not re.fullmatch(r'[A-Za-z0-9-]+', label):
            return False
        if label.startswith('-') or label.endswith('-'):
            return False
    return re.fullmatch(r'[A-Za-z]{2,6}', labels[-1]) is not None


# P012
def is_valid_password(password: str) -> bool:
    specials = "!@#$%^&*"
    return (
        len(password) >= 8
        and any('A' <= c <= 'Z' for c in password)
        and any('a' <= c <= 'z' for c in password)
        and any('0' <= c <= '9' for c in password)
        and any(c in specials for c in password)
    )


# P013
import re


def is_valid_range(s: str) -> str:
    parts = s.split('|')
    if len(parts) != 3:
        return "INVALID"
    if not all(re.fullmatch(r'[+-]?[0-9]+', part) for part in parts):
        return "INVALID"
    value, low, high = (int(part) for part in parts)
    return "VALID" if low <= value <= high else "INVALID"


# P014
def is_valid_ipv4(ip: str) -> bool:
    octets = ip.split('.')
    if len(octets) != 4:
        return False
    for octet in octets:
        if not (octet.isascii() and octet.isdigit()):
            return False
        if len(octet) > 1 and octet[0] == '0':
            return False
        if int(octet) > 255:
            return False
    return True


# P015
def is_valid_username(username: str) -> bool:
    if not 3 <= len(username) <= 20:
        return False
    first = username[0]
    if not (first.isascii() and first.isalpha()):
        return False
    return all(
        (c.isascii() and c.isalnum()) or c in '_-'
        for c in username
    )


# P016
def escape_html(s: str) -> str:
    return (
        s.replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&#39;')
    )


# P017
def escape_csv_cell(s: str) -> str:
    if any(ch in s for ch in ',"\n\r'):
        return '"' + s.replace('"', '""') + '"'
    return s


# P018
def escape_json_string(s: str) -> str:
    table = {
        '"': '\\"',
        '\\': '\\\\',
        '/': '\\/',
        '\b': '\\b',
        '\f': '\\f',
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
    }
    parts = []
    for ch in s:
        if ch in table:
            parts.append(table[ch])
        elif ord(ch) < 0x20:
            parts.append('\\u%04x' % ord(ch))
        else:
            parts.append(ch)
    return ''.join(parts)


# P019
def encode_url_component(s: str) -> str:
    unreserved = frozenset(
        b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~"
    )
    parts = []
    for byte in s.encode('utf-8'):
        if byte in unreserved:
            parts.append(chr(byte))
        else:
            parts.append('%%%02X' % byte)
    return ''.join(parts)


# P020
import re


def sanitize_template(s: str) -> str:
    def replace(match):
        key = match.group(1)
        if re.fullmatch(r'[a-zA-Z0-9_]+', key):
            return match.group(0)
        return ''

    return re.sub(r'\{\{(.*?)\}\}', replace, s, flags=re.DOTALL)


# P021
def safe_path_normalize(path: str) -> str:
    if not path.strip() or '\\' in path:
        return ""
    resolved = []
    for segment in path.split('/'):
        if segment == '' or segment == '.':
            continue
        if segment == '..':
            if not resolved:
                return ""
            resolved.pop()
        else:
            resolved.append(segment)
    return '/'.join(resolved)


# P022
def is_allowed_extension(path: str) -> bool:
    allowed = {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt', '.csv'}
    separator_index = max(path.rfind('/'), path.rfind('\\'))
    filename = path[separator_index + 1:]
    dot_index = filename.rfind('.')
    if dot_index <= 0:
        return False
    return filename[dot_index:].lower() in allowed


# P023
import re


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r'[^a-zA-Z0-9._-]', '_', name[:200])
    cleaned = re.sub(r'_+', '_', cleaned).strip('_')
    return cleaned if cleaned else "_"


# P024
def check_archive_entry(path: str) -> str:
    if path == "":
        return "safe"
    if path.startswith('/') or '\\' in path:
        return "unsafe"
    depth = 0
    for segment in path.split('/'):
        if segment == '' or segment == '.':
            continue
        if segment == '..':
            depth -= 1
            if depth < 0:
                return "unsafe"
        else:
            depth += 1
    return "safe"


# P025
def is_allowed_filetype(ext: str) -> bool:
    allowed = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'pdf', 'txt', 'csv', 'json', 'xml'}
    if ext.startswith('.'):
        ext = ext[1:]
    if ext == "":
        return False
    return ext.lower() in allowed


# P026
import re


def is_valid_sql_identifier(name: str) -> bool:
    return re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]{0,63}', name) is not None


# P027
def escape_sql_string(s: str) -> str:
    return s.replace('\\', '\\\\').replace("'", "''")


# P028
import re


def build_param_query(s: str) -> str:
    if s.count('|') != 1:
        return "INVALID"
    table, conditions = s.split('|')
    identifier = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
    if not identifier.fullmatch(table) or not conditions:
        return "INVALID"
    clauses = []
    for condition in conditions.split(','):
        column, separator, _ = condition.partition('=')
        if not separator or not identifier.fullmatch(column):
            return "INVALID"
        clauses.append(f"{column}=?")
    return f"SELECT * FROM {table} WHERE " + " AND ".join(clauses)


# P029
def validate_sort_direction(s: str) -> str:
    direction = s.strip().upper()
    return direction if direction in ("ASC", "DESC") else "INVALID"


# P030
def is_allowed_column(col: str) -> bool:
    allowed = {"id", "name", "email", "created_at", "status", "age", "role", "score"}
    return col.strip() in allowed


# P031
def quote_shell_arg(s: str) -> str:
    return "'" + s.replace("'", "'\\''") + "'"


# P032
def is_allowed_command(s: str) -> bool:
    allowed = {"ls", "cat", "echo", "grep", "find", "sort", "uniq", "wc", "head", "tail"}
    command = s.strip()
    if ' ' in command:
        return False
    return command in allowed


# P033
def detect_shell_meta(s: str) -> str:
    dangerous = set(';|&$`><(){}\\"\'\n\r')
    return "unsafe" if any(ch in dangerous for ch in s) else "safe"


# P034
import re


def is_valid_env_var(name: str) -> bool:
    return re.fullmatch(r'[A-Z_][A-Z0-9_]{0,63}', name) is not None


# P035
def split_args(s: str) -> list[str]:
    tokens = []
    current = []
    in_quotes = False
    has_token = False
    for ch in s:
        if ch == '"':
            in_quotes = not in_quotes
            has_token = True
        elif ch == ' ' and not in_quotes:
            if has_token:
                tokens.append(''.join(current))
                current = []
                has_token = False
        else:
            current.append(ch)
            has_token = True
    if has_token:
        tokens.append(''.join(current))
    return tokens


# P036
import re


def parse_safe_literal(s: str) -> str:
    if re.fullmatch(r'-?(0|[1-9][0-9]*)', s):
        return "0" if s == "-0" else s
    if s in ("true", "false", "null"):
        return s
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        inner = s[1:-1]
        result = []
        i = 0
        while i < len(inner):
            ch = inner[i]
            if ch == '\\':
                if i + 1 < len(inner) and inner[i + 1] == '"':
                    result.append('"')
                    i += 2
                    continue
                return "INVALID"
            if ch == '"':
                return "INVALID"
            result.append(ch)
            i += 1
        return ''.join(result)
    return "INVALID"


# P037
def parse_config_bool(s: str) -> str:
    value = s.strip().lower()
    if value in ("true", "yes", "1", "on", "enabled"):
        return "true"
    if value in ("false", "no", "0", "off", "disabled"):
        return "false"
    return "INVALID"


# P038
def is_allowed_config_key(key: str) -> bool:
    allowed = {
        "host", "port", "database", "username", "password",
        "timeout", "max_connections", "ssl_enabled", "log_level", "retry_count",
    }
    return key.strip() in allowed


# P039
import re


def validate_token(s: str) -> str:
    pattern = r'[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[0-9a-f]{8}'
    return "valid" if re.fullmatch(pattern, s) else "invalid"


# P040
import re


def validate_numeric_expr(s: str) -> str:
    number = r'-?(?:0|[1-9][0-9]*)'
    pattern = number + r'(?: *[+\-*/] *' + number + r')*'
    return "valid" if re.fullmatch(pattern, s) else "invalid"


# P041
def frequency_counter(nums: list[int]) -> dict:
    counts = {}
    for value in nums:
        counts[value] = counts.get(value, 0) + 1
    return {str(key): counts[key] for key in sorted(counts)}


# P042
def has_duplicate(nums: list[int]) -> bool:
    return len(set(nums)) != len(nums)


# P043
def streaming_sum(nums: list[int]) -> int:
    total = 0
    for value in nums:
        total += value
    return total


# P044
def bounded_log_processor(log: str, max_lines: int) -> dict:
    kept = 0
    total_words = 0
    if max_lines > 0:
        for line in log.splitlines():
            if not line.strip():
                continue
            if kept >= max_lines:
                break
            kept += 1
            total_words += len(line.split())
    return {"kept": kept, "total_words": total_words}


# P045
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    if k <= 0 or not nums:
        return []
    counts = {}
    for value in nums:
        counts[value] = counts.get(value, 0) + 1
    ranked = sorted(counts, key=lambda value: (-counts[value], value))
    return sorted(ranked[:k])


# P046
import re


def validate_token_format(token: str) -> str:
    return "valid" if re.fullmatch(r'[a-zA-Z][a-zA-Z0-9\-]{7,31}', token) else "invalid"


# P047
def evaluate_permission(role: str, action: str) -> str:
    permissions = {
        "admin": {"read", "write", "delete", "execute"},
        "editor": {"read", "write"},
        "viewer": {"read"},
        "guest": set(),
    }
    return "allowed" if action in permissions.get(role, set()) else "denied"


# P048
def role_has_permission(role: str, permission: str) -> bool:
    permissions = {
        "admin": {"read", "write", "delete", "execute"},
        "editor": {"read", "write"},
        "viewer": {"read"},
        "guest": set(),
    }
    return permission in permissions.get(role, set())


# P049
def check_session(last_active: int, current_time: int, timeout: int) -> str:
    if current_time < last_active:
        return "invalid"
    elapsed = current_time - last_active
    return "expired" if elapsed > timeout else "active"


# P050
def validate_scope(requested: str, allowed: list[str]) -> str:
    allowed_scopes = set(allowed)
    parts = requested.split(':')
    for end in range(1, len(parts) + 1):
        if ':'.join(parts[:end]) in allowed_scopes:
            return "granted"
    return "denied"
