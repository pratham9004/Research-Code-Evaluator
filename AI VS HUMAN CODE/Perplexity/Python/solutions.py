# P001: Two Sum
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return sorted([seen[complement], i])
        seen[num] = i
    return []

# P002: Maximum Subarray Sum
def max_subarray(nums: list[int]) -> int:
    max_sum = nums[0]
    current_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum

# P003: Binary Search
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
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in '({[':
            stack.append(char)
        elif char in ')}]':
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
    return len(stack) == 0

# P006: CSV Record Field Count
def csv_field_count(line: str) -> int:
    if not line:
        return 0
    count = 0
    in_quotes = False
    i = 0
    while i < len(line):
        char = line[i]
        if char == '"':
            if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                i += 1
            else:
                in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            count += 1
        i += 1
    return count + 1

# P007: Log Level Counter
def count_log_levels(log: str) -> dict:
    result = {"ERROR": 0, "WARNING": 0, "INFO": 0, "DEBUG": 0}
    for line in log.split('\n'):
        line = line.strip()
        for level in ["ERROR", "WARNING", "INFO", "DEBUG"]:
            if line.startswith(level + ' ') or line.startswith(level + ':'):
                result[level] += 1
                break
    return result

# P008: Key-Value Parser
def parse_key_value(s: str) -> dict:
    if not s:
        return {}
    result = {}
    pairs = s.split(',')
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            result[key.strip()] = value.strip()
    return dict(sorted(result.items()))

# P009: Date Format Normalizer
def normalize_date(date: str) -> str:
    if '/' in date:
        parts = date.split('/')
        mm, dd, yyyy = parts[0], parts[1], parts[2]
        return f"{yyyy}-{mm}-{dd}"
    elif '-' in date:
        parts = date.split('-')
        dd, mm, yyyy = parts[0], parts[1], parts[2]
        return f"{yyyy}-{mm}-{dd}"
    elif '.' in date:
        parts = date.split('.')
        yyyy, mm, dd = parts[0], parts[1], parts[2]
        return f"{yyyy}-{mm}-{dd}"
    return date

# P010: Word Frequency
def word_frequency(text: str) -> dict:
    import re
    words = re.findall(r'[a-zA-Z]+', text.lower())
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

# P011: Email Validator
def is_valid_email(email: str) -> bool:
    if email.count('@') != 1:
        return False
    local, domain = email.split('@')
    if not local or local.startswith('.') or local.endswith('.') or '..' in local:
        return False
    for char in local:
        if char not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._%+-':
            return False
    if not domain or domain.startswith('.') or domain.endswith('.'):
        return False
    labels = domain.split('.')
    if len(labels) < 2:
        return False
    tld = labels[-1]
    if not tld.isalpha() or len(tld) < 2 or len(tld) > 6:
        return False
    for label in labels:
        if not label or label.startswith('-') or label.endswith('-'):
            return False
    return True

# P012: Password Policy Validator
def is_valid_password(password: str) -> bool:
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*' for c in password)
    return has_upper and has_lower and has_digit and has_special

# P013: Integer Range Validator
def is_valid_range(s: str) -> str:
    try:
        parts = s.split('|')
        if len(parts) != 3:
            return "INVALID"
        value, min_val, max_val = int(parts[0]), int(parts[1]), int(parts[2])
        if min_val <= value <= max_val:
            return "VALID"
        return "INVALID"
    except (ValueError, IndexError):
        return "INVALID"

# P014: IPv4 Validator
def is_valid_ipv4(ip: str) -> bool:
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part or not part.isdigit():
            return False
        if len(part) > 1 and part[0] == '0':
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
    return True

# P015: Username Validator
def is_valid_username(username: str) -> bool:
    if len(username) < 3 or len(username) > 20:
        return False
    if not username[0].isalpha():
        return False
    for char in username:
        if char not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-':
            return False
    return True

# P016: HTML Text Escaper
def escape_html(s: str) -> str:
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('"', '&quot;')
    s = s.replace("'", '&#39;')
    return s

# P017: CSV Cell Escaper
def escape_csv_cell(s: str) -> str:
    needs_quoting = ',' in s or '"' in s or '\n' in s or '\r' in s
    if needs_quoting:
        s = s.replace('"', '""')
        return '"' + s + '"'
    return s

# P018: JSON String Escaper
def escape_json_string(s: str) -> str:
    result = []
    for char in s:
        if char == '"':
            result.append('\\"')
        elif char == '\\':
            result.append('\\\\')
        elif char == '/':
            result.append('\\/')
        elif char == '\b':
            result.append('\\b')
        elif char == '\f':
            result.append('\\f')
        elif char == '\n':
            result.append('\\n')
        elif char == '\r':
            result.append('\\r')
        elif char == '\t':
            result.append('\\t')
        elif ord(char) < 0x20:
            result.append(f'\\u{ord(char):04x}')
        else:
            result.append(char)
    return ''.join(result)

# P019: URL Query Component Encoder
def encode_url_component(s: str) -> str:
    unreserved = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~')
    result = []
    for char in s:
        if char in unreserved:
            result.append(char)
        else:
            for byte in char.encode('utf-8'):
                result.append(f'%{byte:02X}')
    return ''.join(result)

# P020: Template Placeholder Sanitizer
def sanitize_template(s: str) -> str:
    import re
    def replace_placeholder(match):
        key = match.group(1)
        if key and re.match(r'^[a-zA-Z0-9_]+$', key):
            return match.group(0)
        return ''
    return re.sub(r'\{\{([^}]*)\}\}', replace_placeholder, s)

# P021: Safe Path Normalizer
def safe_path_normalize(path: str) -> str:
    if not path or path.isspace():
        return ''
    if '\\' in path:
        return ''
    segments = path.split('/')
    result = []
    for seg in segments:
        if seg == '' or seg == '.':
            continue
        if seg == '..':
            if not result:
                return ''
            result.pop()
        else:
            result.append(seg)
    return '/'.join(result)

# P022: Path Extension Validator
def is_allowed_extension(path: str) -> bool:
    allowed = {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt', '.csv'}
    filename = path.replace('\\', '/').split('/')[-1]
    if '.' not in filename or filename.startswith('.'):
        dot_pos = filename.rfind('.')
        if dot_pos <= 0:
            return False
    ext = '.' + filename.rsplit('.', 1)[-1].lower()
    return ext in allowed

# P023: Filename Sanitizer
def sanitize_filename(name: str) -> str:
    name = name[:200]
    result = []
    for char in name:
        if char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-':
            result.append(char)
        else:
            result.append('_')
    s = ''.join(result)
    import re
    s = re.sub(r'_+', '_', s)
    s = s.strip('_')
    return s if s else '_'

# P024: Archive Entry Path Checker
def check_archive_entry(path: str) -> str:
    if not path:
        return "safe"
    if path.startswith('/'):
        return "unsafe"
    if '\\' in path:
        return "unsafe"
    depth = 0
    segments = path.split('/')
    for seg in segments:
        if seg == '.' or seg == '':
            continue
        if seg == '..':
            depth -= 1
            if depth < 0:
                return "unsafe"
        else:
            depth += 1
    return "safe"

# P025: File Type Allowlist
def is_allowed_filetype(ext: str) -> bool:
    allowed = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'pdf', 'txt', 'csv', 'json', 'xml'}
    ext = ext.lstrip('.').lower()
    return ext in allowed if ext else False

# P026: SQL Identifier Validator
def is_valid_sql_identifier(name: str) -> bool:
    if len(name) < 1 or len(name) > 64:
        return False
    if not (name[0].isalpha() or name[0] == '_'):
        return False
    for char in name:
        if not (char.isalpha() or char.isdigit() or char == '_'):
            return False
    return True

# P027: SQL String Literal Escaper
def escape_sql_string(s: str) -> str:
    s = s.replace('\\', '\\\\')
    s = s.replace("'", "''")
    return s

# P028: Parameterized Query Builder
def build_param_query(s: str) -> str:
    if '|' not in s:
        return "INVALID"
    parts = s.split('|', 1)
    if len(parts) != 2:
        return "INVALID"
    table, conditions = parts
    if not is_valid_sql_identifier(table):
        return "INVALID"
    if not conditions:
        return "INVALID"
    cond_pairs = conditions.split(',')
    if not cond_pairs:
        return "INVALID"
    cols = []
    for pair in cond_pairs:
        if '=' not in pair:
            return "INVALID"
        col, _ = pair.split('=', 1)
        if not is_valid_sql_identifier(col):
            return "INVALID"
        cols.append(col)
    where_parts = [f"{col}=?" for col in cols]
    return f"SELECT * FROM {table} WHERE " + " AND ".join(where_parts)

# P029: Sort Direction Validator
def validate_sort_direction(s: str) -> str:
    s = s.strip().upper()
    if s == 'ASC' or s == 'DESC':
        return s
    return "INVALID"

# P030: Column Allowlist Checker
def is_allowed_column(col: str) -> bool:
    allowed = {'id', 'name', 'email', 'created_at', 'status', 'age', 'role', 'score'}
    return col.strip() in allowed

# P031: Shell Argument Quoter
def quote_shell_arg(s: str) -> str:
    escaped = s.replace("'", "'\\''")
    return f"'{escaped}'"

# P032: Command Name Allowlist
def is_allowed_command(s: str) -> bool:
    allowed = {'ls', 'cat', 'echo', 'grep', 'find', 'sort', 'uniq', 'wc', 'head', 'tail'}
    s = s.strip()
    if ' ' in s:
        return False
    return s in allowed

# P033: Shell Metacharacter Detector
def detect_shell_meta(s: str) -> str:
    dangerous = set(';|&$`><(){}\\\"\'\n\r')
    for char in s:
        if char in dangerous:
            return "unsafe"
    return "safe"

# P034: Environment Variable Name Validator
def is_valid_env_var(name: str) -> bool:
    if len(name) < 1 or len(name) > 64:
        return False
    if not (name[0].isupper() or name[0] == '_'):
        return False
    for char in name:
        if not (char.isupper() or char.isdigit() or char == '_'):
            return False
    return True

# P035: Command Argument Splitter
def split_args(s: str) -> list[str]:
    if not s:
        return []
    result = []
    current = []
    in_quotes = False
    i = 0
    while i < len(s):
        char = s[i]
        if char == '"':
            if in_quotes:
                result.append(''.join(current))
                current = []
                in_quotes = False
            else:
                if current:
                    result.append(''.join(current))
                    current = []
                in_quotes = True
        elif char == ' ' and not in_quotes:
            if current:
                result.append(''.join(current))
                current = []
        else:
            current.append(char)
        i += 1
    if current:
        result.append(''.join(current))
    return result

# P036: Safe Literal Parser
def parse_safe_literal(s: str) -> str:
    if s == 'true' or s == 'false' or s == 'null':
        return s
    if s.isdigit() or (s.startswith('-') and s[1:].isdigit() and len(s) > 1):
        if s.startswith('-') and len(s) > 1 and s[1] == '0' and len(s) > 2:
            return "INVALID"
        if s == '0' or (not s.startswith('0')) or (s.startswith('-') and s[1] != '0'):
            if s.startswith('-'):
                num_part = s[1:]
                if len(num_part) > 1 and num_part[0] == '0':
                    return "INVALID"
            elif len(s) > 1 and s[0] == '0':
                return "INVALID"
            return s
        return "INVALID"
    if s.startswith('"') and s.endswith('"') and len(s) >= 2:
        content = s[1:-1]
        result = []
        i = 0
        while i < len(content):
            if content[i] == '\\' and i + 1 < len(content) and content[i + 1] == '"':
                result.append('"')
                i += 2
            elif content[i] == '\\':
                return "INVALID"
            elif content[i] == '"':
                return "INVALID"
            else:
                result.append(content[i])
                i += 1
        return ''.join(result)
    return "INVALID"

# P037: Configuration Boolean Parser
def parse_config_bool(s: str) -> str:
    s = s.strip().lower()
    if s in {'true', 'yes', '1', 'on', 'enabled'}:
        return "true"
    if s in {'false', 'no', '0', 'off', 'disabled'}:
        return "false"
    return "INVALID"

# P038: Configuration Key Allowlist
def is_allowed_config_key(key: str) -> bool:
    allowed = {'host', 'port', 'database', 'username', 'password', 'timeout', 'max_connections', 'ssl_enabled', 'log_level', 'retry_count'}
    return key.strip() in allowed

# P039: Structured Token Decoder
def validate_token(s: str) -> str:
    import re
    parts = s.split('.')
    if len(parts) != 3:
        return "invalid"
    header, payload, checksum = parts
    if not re.match(r'^[A-Za-z0-9_-]+$', header):
        return "invalid"
    if not re.match(r'^[A-Za-z0-9_-]+$', payload):
        return "invalid"
    if not re.match(r'^[0-9a-f]{8}$', checksum):
        return "invalid"
    return "valid"

# P040: Safe Numeric Expression Validator
def validate_numeric_expr(s: str) -> str:
    import re
    s = s.strip()
    if not s:
        return "invalid"
    number_pattern = r'(0|-?[1-9][0-9]*)'
    operator_pattern = r'[+\-*/]'
    full_pattern = f'^{number_pattern}(\\s*{operator_pattern}\\s*{number_pattern})*$'
    if re.match(full_pattern, s):
        return "valid"
    return "invalid"

# P041: Frequency Counter Large Input
def frequency_counter(nums: list[int]) -> dict:
    freq = {}
    for num in nums:
        freq[num] = freq.get(num, 0) + 1
    return dict(sorted(freq.items()))

# P042: Duplicate Detector
def has_duplicate(nums: list[int]) -> bool:
    return len(nums) != len(set(nums))

# P043: Streaming Sum
def streaming_sum(nums: list[int]) -> int:
    return sum(nums)

# P044: Bounded Log Processor
def bounded_log_processor(log: str, max_lines: int) -> dict:
    if max_lines <= 0:
        return {"kept": 0, "total_words": 0}
    lines = log.split('\n')
    kept = 0
    total_words = 0
    for line in lines:
        if kept >= max_lines:
            break
        stripped = line.strip()
        if stripped:
            kept += 1
            total_words += len(stripped.split())
    return {"kept": kept, "total_words": total_words}

# P045: Top-K Frequent Values
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    if k <= 0 or not nums:
        return []
    freq = {}
    for num in nums:
        freq[num] = freq.get(num, 0) + 1
    sorted_items = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    result = [item[0] for item in sorted_items[:k]]
    return sorted(result)

# P046: Token Format Validator
def validate_token_format(token: str) -> str:
    import re
    if not token:
        return "invalid"
    if len(token) < 8 or len(token) > 32:
        return "invalid"
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9\-]*$', token):
        return "invalid"
    return "valid"

# P047: Permission Rule Evaluator
def evaluate_permission(role: str, action: str) -> str:
    permissions = {
        'admin': {'read', 'write', 'delete', 'execute'},
        'editor': {'read', 'write'},
        'viewer': {'read'},
        'guest': set()
    }
    if role in permissions and action in permissions[role]:
        return "allowed"
    return "denied"

# P048: Role Permission Checker
def role_has_permission(role: str, permission: str) -> bool:
    permissions = {
        'admin': {'read', 'write', 'delete', 'execute'},
        'editor': {'read', 'write'},
        'viewer': {'read'},
        'guest': set()
    }
    return role in permissions and permission in permissions[role]

# P049: Session Timeout Checker
def check_session(last_active: int, current_time: int, timeout: int) -> str:
    if current_time < last_active:
        return "invalid"
    elapsed = current_time - last_active
    if elapsed <= timeout:
        return "active"
    return "expired"

# P050: Access Scope Validator
def validate_scope(requested: str, allowed: list[str]) -> str:
    if not allowed:
        return "denied"
    if requested in allowed:
        return "granted"
    parts = requested.split(':')
    for i in range(1, len(parts)):
        parent = ':'.join(parts[:i])
        if parent in allowed:
            return "granted"
    return "denied"