# Research Code Evaluator - AI Generated Benchmark Solutions
# P001
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            result = [seen[complement], i]
            result.sort()
            return result
        seen[value] = i
    return []

# P002
def max_subarray(nums: list[int]) -> int:
    current = best = nums[0]
    for value in nums[1:]:
        current = max(value, current + value)
        best = max(best, current)
    return best

# P003
def binary_search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# P004
def merge_sorted_arrays(nums1: list[int], nums2: list[int]) -> list[int]:
    result = []
    i = j = 0
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

# P005
def is_balanced(s: str) -> bool:
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif not stack or stack.pop() != pairs[ch]:
            return False
    return not stack

# P006
def csv_field_count(line: str) -> int:
    if not line:
        return 1
    count = 1
    in_quotes = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '"':
            if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                i += 1
            else:
                in_quotes = not in_quotes
        elif ch == ',' and not in_quotes:
            count += 1
        i += 1
    return count

# P007
def count_log_levels(log: str) -> dict:
    counts = {"ERROR": 0, "WARNING": 0, "INFO": 0, "DEBUG": 0}
    for line in log.splitlines():
        for level in counts:
            if line.startswith(level) and len(line) > len(level) and line[len(level)] in ' :':
                counts[level] += 1
                break
    return counts

# P008
def parse_key_value(s: str) -> dict:
    result = {}
    if not s:
        return result
    for pair in s.split(','):
        key, value = pair.split('=', 1)
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
    return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"

# P010
def word_frequency(text: str) -> dict:
    import re
    counts = {}
    for word in re.findall(r'[A-Za-z]+', text):
        word = word.lower()
        counts[word] = counts.get(word, 0) + 1
    return counts

# P011
def is_valid_email(email: str) -> bool:
    if email.count('@') != 1:
        return False
    local, domain = email.split('@')
    if not local or not domain:
        return False
    if local[0] == '.' or local[-1] == '.' or '..' in local:
        return False
    if any(ch not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._%+-' for ch in local):
        return False
    labels = domain.split('.')
    if any(not label for label in labels):
        return False
    for label in labels:
        if label[0] == '-' or label[-1] == '-':
            return False
        if any(not (ch.isalnum() and ord(ch) < 128 or ch == '-') for ch in label):
            return False
    tld = labels[-1]
    return 2 <= len(tld) <= 6 and all('A' <= ch <= 'Z' or 'a' <= ch <= 'z' for ch in tld)

# P012
def is_valid_password(password: str) -> bool:
    if len(password) < 8:
        return False
    return (
        any('A' <= c <= 'Z' for c in password)
        and any('a' <= c <= 'z' for c in password)
        and any('0' <= c <= '9' for c in password)
        and any(c in '!@#$%^&*' for c in password)
    )

# P013
def is_valid_range(s: str) -> str:
    parts = s.split('|')
    if len(parts) != 3:
        return "INVALID"
    try:
        value, minimum, maximum = (int(part) for part in parts)
    except ValueError:
        return "INVALID"
    return "VALID" if minimum <= value <= maximum else "INVALID"

# P014
def is_valid_ipv4(ip: str) -> bool:
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part or not part.isdigit() or (len(part) > 1 and part[0] == '0'):
            return False
        if int(part) > 255:
            return False
    return True

# P015
def is_valid_username(username: str) -> bool:
    if not 3 <= len(username) <= 20:
        return False
    if not ('A' <= username[0] <= 'Z' or 'a' <= username[0] <= 'z'):
        return False
    return all(
        'A' <= c <= 'Z' or 'a' <= c <= 'z' or '0' <= c <= '9' or c in '_-'
        for c in username
    )

# P016
def escape_html(s: str) -> str:
    return (s.replace('&', '&amp;')
             .replace('<', '&lt;')
             .replace('>', '&gt;')
             .replace('"', '&quot;')
             .replace("'", '&#39;'))

# P017
def escape_csv_cell(s: str) -> str:
    if any(ch in s for ch in ',\"\n\r'):
        return '"' + s.replace('"', '""') + '"'
    return s

# P018
def escape_json_string(s: str) -> str:
    result = []
    for ch in s:
        code = ord(ch)
        if ch == '"':
            result.append('\\"')
        elif ch == '\\':
            result.append('\\\\')
        elif ch == '/':
            result.append('\\/')
        elif ch == '\b':
            result.append('\\b')
        elif ch == '\f':
            result.append('\\f')
        elif ch == '\n':
            result.append('\\n')
        elif ch == '\r':
            result.append('\\r')
        elif ch == '\t':
            result.append('\\t')
        elif code < 0x20:
            result.append(f'\\u{code:04x}')
        else:
            result.append(ch)
    return ''.join(result)

# P019
def encode_url_component(s: str) -> str:
    import urllib.parse
    safe = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~'
    return urllib.parse.quote(s, safe=safe, encoding='utf-8', errors='strict')

# P020
def sanitize_template(s: str) -> str:
    import re
    pattern = re.compile(r'\{\{([^{}]*)\}\}')
    def replace(match):
        key = match.group(1)
        return match.group(0) if re.fullmatch(r'[a-zA-Z0-9_]+', key) else ''
    return pattern.sub(replace, s)

# P021
def safe_path_normalize(path: str) -> str:
    if not path or not path.strip() or '\\' in path:
        return ''
    parts = []
    for segment in path.split('/'):
        if not segment or segment == '.':
            continue
        if segment == '..':
            if not parts:
                return ''
            parts.pop()
        else:
            parts.append(segment)
    return '/'.join(parts)

# P022
def is_allowed_extension(path: str) -> bool:
    filename = path.replace('\\', '/').rsplit('/', 1)[-1]
    dot = filename.rfind('.')
    if dot <= 0:
        return False
    return filename[dot:].lower() in {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt', '.csv'}

# P023
def sanitize_filename(name: str) -> str:
    import re
    value = name[:200]
    value = re.sub(r'[^a-zA-Z0-9._-]', '_', value)
    value = re.sub(r'_+', '_', value).strip('_')
    return value or '_'

# P024
def check_archive_entry(path: str) -> str:
    if path == '':
        return 'safe'
    if path.startswith('/') or '\\' in path:
        return 'unsafe'
    depth = 0
    for segment in path.split('/'):
        if segment in ('', '.'):
            continue
        if segment == '..':
            depth -= 1
            if depth < 0:
                return 'unsafe'
        else:
            depth += 1
    return 'safe'

# P025
def is_allowed_filetype(ext: str) -> bool:
    value = ext[1:] if ext.startswith('.') else ext
    return bool(value) and value.lower() in {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'pdf', 'txt', 'csv', 'json', 'xml'}

# P026
def is_valid_sql_identifier(name: str) -> bool:
    import re
    return re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]{0,63}', name) is not None

# P027
def escape_sql_string(s: str) -> str:
    return s.replace('\\', '\\\\').replace("'", "''")

# P028
def build_param_query(s: str) -> str:
    if s.count('|') != 1:
        return 'INVALID'
    table, conditions = s.split('|')
    import re
    if re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', table) is None or not conditions:
        return 'INVALID'
    parts = conditions.split(',')
    columns = []
    for part in parts:
        if '=' not in part:
            return 'INVALID'
        column, _ = part.split('=', 1)
        if re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', column) is None:
            return 'INVALID'
        columns.append(column)
    if not columns:
        return 'INVALID'
    return 'SELECT * FROM ' + table + ' WHERE ' + ' AND '.join(c + '=?' for c in columns)

# P029
def validate_sort_direction(s: str) -> str:
    value = s.strip().upper()
    return value if value in ('ASC', 'DESC') else 'INVALID'

# P030
def is_allowed_column(col: str) -> bool:
    return col.strip() in {'id', 'name', 'email', 'created_at', 'status', 'age', 'role', 'score'}

# P031
def quote_shell_arg(s: str) -> str:
    return "'" + s.replace("'", "'\\''") + "'"

# P032
def is_allowed_command(s: str) -> bool:
    return s.strip() in {'ls', 'cat', 'echo', 'grep', 'find', 'sort', 'uniq', 'wc', 'head', 'tail'}

# P033
def detect_shell_meta(s: str) -> str:
    dangerous = set(";|&$`><(){}\\\"'\n\r")
    return 'unsafe' if any(ch in dangerous for ch in s) else 'safe'

# P034
def is_valid_env_var(name: str) -> bool:
    if not 1 <= len(name) <= 64:
        return False
    if not ('A' <= name[0] <= 'Z' or name[0] == '_'):
        return False
    return all('A' <= c <= 'Z' or '0' <= c <= '9' or c == '_' for c in name)

# P035
def split_args(s: str) -> list[str]:
    if not s:
        return []
    tokens = []
    current = []
    in_quotes = False
    token_started = False
    for ch in s:
        if ch == '"':
            in_quotes = not in_quotes
            token_started = True
        elif ch == ' ' and not in_quotes:
            if token_started:
                tokens.append(''.join(current))
                current = []
                token_started = False
        else:
            current.append(ch)
            token_started = True
    if token_started:
        tokens.append(''.join(current))
    return tokens

# P036
def parse_safe_literal(s: str) -> str:
    import re
    if re.fullmatch(r'-?(0|[1-9][0-9]*)', s):
        return s
    if s in ('true', 'false', 'null'):
        return s
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        content = s[1:-1]
        result = []
        i = 0
        while i < len(content):
            if content[i] == '\\':
                if i + 1 >= len(content) or content[i + 1] != '"':
                    return 'INVALID'
                result.append('"')
                i += 2
            elif content[i] == '"':
                return 'INVALID'
            else:
                result.append(content[i])
                i += 1
        return ''.join(result)
    return 'INVALID'

# P037
def parse_config_bool(s: str) -> str:
    value = s.strip().lower()
    if value in {'true', 'yes', '1', 'on', 'enabled'}:
        return 'true'
    if value in {'false', 'no', '0', 'off', 'disabled'}:
        return 'false'
    return 'INVALID'

# P038
def is_allowed_config_key(key: str) -> bool:
    return key.strip() in {
        'host', 'port', 'database', 'username', 'password',
        'timeout', 'max_connections', 'ssl_enabled', 'log_level', 'retry_count'
    }

# P039
def validate_token(s: str) -> str:
    import re
    return 'valid' if re.fullmatch(r'[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[0-9a-f]{8}', s) else 'invalid'

# P040
def validate_numeric_expr(s: str) -> str:
    import re
    number = r'-?(?:0|[1-9][0-9]*)'
    pattern = rf'{number}(?:\s*[+\-*/]\s*{number})*'
    return 'valid' if re.fullmatch(pattern, s) else 'invalid'

# P041
def frequency_counter(nums: list[int]) -> dict:
    counts = {}
    for value in nums:
        counts[value] = counts.get(value, 0) + 1
    return {str(k): counts[k] for k in sorted(counts)}

# P042
def has_duplicate(nums: list[int]) -> bool:
    return len(nums) != len(set(nums))

# P043
def streaming_sum(nums: list[int]) -> int:
    return sum(nums)

# P044
def bounded_log_processor(log: str, max_lines: int) -> dict:
    if max_lines <= 0 or not log:
        return {'kept': 0, 'total_words': 0}
    kept = 0
    total_words = 0
    for line in log.splitlines():
        if not line.strip():
            continue
        if kept >= max_lines:
            break
        kept += 1
        total_words += len(line.split())
    return {'kept': kept, 'total_words': total_words}

# P045
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    if not nums or k == 0:
        return []
    counts = {}
    for value in nums:
        counts[value] = counts.get(value, 0) + 1
    selected = sorted(counts, key=lambda value: (-counts[value], value))[:k]
    return sorted(selected)

# P046
def validate_token_format(token: str) -> str:
    import re
    return 'valid' if re.fullmatch(r'[a-zA-Z][a-zA-Z0-9-]{7,31}', token) else 'invalid'

# P047
def evaluate_permission(role: str, action: str) -> str:
    permissions = {
        'admin': {'read', 'write', 'delete', 'execute'},
        'editor': {'read', 'write'},
        'viewer': {'read'},
        'guest': set()
    }
    return 'allowed' if action in permissions.get(role, set()) else 'denied'

# P048
def role_has_permission(role: str, permission: str) -> bool:
    permissions = {
        'admin': {'read', 'write', 'delete', 'execute'},
        'editor': {'read', 'write'},
        'viewer': {'read'},
        'guest': set()
    }
    return permission in permissions.get(role, set())

# P049
def check_session(last_active: int, current_time: int, timeout: int) -> str:
    if current_time < last_active:
        return 'invalid'
    return 'expired' if current_time - last_active > timeout else 'active'

# P050
def validate_scope(requested: str, allowed: list[str]) -> str:
    parts = requested.split(':')
    for i in range(len(parts), 0, -1):
        if ':'.join(parts[:i]) in allowed:
            return 'granted'
    return 'denied'
