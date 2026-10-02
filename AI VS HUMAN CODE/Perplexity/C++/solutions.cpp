// P001: Two Sum
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> seen;
    for (int i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];
        if (seen.find(complement) != seen.end()) {
            vector<int> result = {seen[complement], i};
            sort(result.begin(), result.end());
            return result;
        }
        seen[nums[i]] = i;
    }
    return {};
}

// P002: Maximum Subarray Sum
int maxSubarray(vector<int>& nums) {
    int max_sum = nums[0];
    int current_sum = nums[0];
    for (size_t i = 1; i < nums.size(); i++) {
        current_sum = max(nums[i], current_sum + nums[i]);
        max_sum = max(max_sum, current_sum);
    }
    return max_sum;
}

// P003: Binary Search
int binarySearch(vector<int>& nums, int target) {
    int left = 0, right = nums.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        else if (nums[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

// P004: Merge Sorted Arrays
vector<int> mergeSortedArrays(vector<int>& nums1, vector<int>& nums2) {
    vector<int> result;
    size_t i = 0, j = 0;
    while (i < nums1.size() && j < nums2.size()) {
        if (nums1[i] <= nums2[j]) result.push_back(nums1[i++]);
        else result.push_back(nums2[j++]);
    }
    while (i < nums1.size()) result.push_back(nums1[i++]);
    while (j < nums2.size()) result.push_back(nums2[j++]);
    return result;
}

// P005: Balanced Brackets
bool isBalanced(const string& s) {
    stack<char> st;
    unordered_map<char, char> pairs = {{')', '('}, {'}', '{'}, {']', '['}};
    for (char c : s) {
        if (c == '(' || c == '{' || c == '[') st.push(c);
        else if (c == ')' || c == '}' || c == ']') {
            if (st.empty() || st.top() != pairs[c]) return false;
            st.pop();
        }
    }
    return st.empty();
}

// P006: CSV Record Field Count
int csvFieldCount(const string& line) {
    if (line.empty()) return 0;
    int count = 0;
    bool in_quotes = false;
    for (size_t i = 0; i < line.size(); i++) {
        char c = line[i];
        if (c == '"') {
            if (in_quotes && i + 1 < line.size() && line[i + 1] == '"') i++;
            else in_quotes = !in_quotes;
        } else if (c == ',' && !in_quotes) count++;
    }
    return count + 1;
}

// P007: Log Level Counter
map<string, int> countLogLevels(const string& log) {
    map<string, int> result = {{"ERROR", 0}, {"WARNING", 0}, {"INFO", 0}, {"DEBUG", 0}};
    stringstream ss(log);
    string line;
    while (getline(ss, line)) {
        size_t pos = line.find_first_not_of(" \t");
        if (pos == string::npos) continue;
        line = line.substr(pos);
        if (line.find("ERROR ") == 0 || line.find("ERROR:") == 0) result["ERROR"]++;
        else if (line.find("WARNING ") == 0 || line.find("WARNING:") == 0) result["WARNING"]++;
        else if (line.find("INFO ") == 0 || line.find("INFO:") == 0) result["INFO"]++;
        else if (line.find("DEBUG ") == 0 || line.find("DEBUG:") == 0) result["DEBUG"]++;
    }
    return result;
}

// P008: Key-Value Parser
map<string, string> parseKeyValue(const string& s) {
    map<string, string> result;
    if (s.empty()) return result;
    stringstream ss(s);
    string pair;
    while (getline(ss, pair, ',')) {
        size_t eq = pair.find('=');
        if (eq != string::npos) {
            string key = pair.substr(0, eq);
            string value = pair.substr(eq + 1);
            size_t ks = key.find_first_not_of(" "), ke = key.find_last_not_of(" ");
            size_t vs = value.find_first_not_of(" "), ve = value.find_last_not_of(" ");
            if (ks != string::npos) key = key.substr(ks, ke - ks + 1);
            if (vs != string::npos) value = value.substr(vs, ve - vs + 1);
            result[key] = value;
        }
    }
    return result;
}

// P009: Date Format Normalizer
string normalizeDate(const string& date) {
    if (date.find('/') != string::npos) {
        size_t p1 = date.find('/'), p2 = date.find('/', p1 + 1);
        string mm = date.substr(0, p1), dd = date.substr(p1 + 1, p2 - p1 - 1), yyyy = date.substr(p2 + 1);
        return yyyy + "-" + mm + "-" + dd;
    } else if (date.find('-') != string::npos) {
        size_t p1 = date.find('-'), p2 = date.find('-', p1 + 1);
        string dd = date.substr(0, p1), mm = date.substr(p1 + 1, p2 - p1 - 1), yyyy = date.substr(p2 + 1);
        return yyyy + "-" + mm + "-" + dd;
    } else if (date.find('.') != string::npos) {
        size_t p1 = date.find('.'), p2 = date.find('.', p1 + 1);
        string yyyy = date.substr(0, p1), mm = date.substr(p1 + 1, p2 - p1 - 1), dd = date.substr(p2 + 1);
        return yyyy + "-" + mm + "-" + dd;
    }
    return date;
}

// P010: Word Frequency
vector<pair<string, int>> wordFrequency(const string& text) {
    map<string, int> freq;
    string word;
    for (char c : text) {
        if (isalpha(c)) word += tolower(c);
        else if (!word.empty()) { freq[word]++; word = ""; }
    }
    if (!word.empty()) freq[word]++;
    vector<pair<string, int>> result(freq.begin(), freq.end());
    sort(result.begin(), result.end(), [](const pair<string,int>& a, const pair<string,int>& b) {
        if (a.second != b.second) return a.second > b.second;
        return a.first < b.first;
    });
    return result;
}

// P011: Email Validator
bool isValidEmail(const string& email) {
    int at = 0;
    for (char c : email) if (c == '@') at++;
    if (at != 1) return false;
    size_t atpos = email.find('@');
    string local = email.substr(0, atpos), domain = email.substr(atpos + 1);
    if (local.empty() || local.front() == '.' || local.back() == '.' || local.find("..") != string::npos) return false;
    for (char c : local) if (string("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._%+-").find(c) == string::npos) return false;
    if (domain.empty() || domain.front() == '.' || domain.back() == '.') return false;
    size_t lastdot = domain.rfind('.');
    if (lastdot == string::npos || lastdot == 0) return false;
    string tld = domain.substr(lastdot + 1);
    if (tld.length() < 2 || tld.length() > 6) return false;
    for (char c : tld) if (!isalpha(c)) return false;
    stringstream ss(domain);
    string label;
    while (getline(ss, label, '.')) {
        if (label.empty() || label.front() == '-' || label.back() == '-') return false;
    }
    return true;
}

// P012: Password Policy Validator
bool isValidPassword(const string& pw) {
    if (pw.length() < 8) return false;
    bool upper = false, lower = false, digit = false, special = false;
    for (char c : pw) {
        if (isupper(c)) upper = true;
        if (islower(c)) lower = true;
        if (isdigit(c)) digit = true;
        if (string("!@#$%^&*").find(c) != string::npos) special = true;
    }
    return upper && lower && digit && special;
}

// P013: Integer Range Validator
string isValidRange(const string& s) {
    stringstream ss(s);
    string part;
    vector<string> parts;
    while (getline(ss, part, '|')) parts.push_back(part);
    if (parts.size() != 3) return "INVALID";
    try {
        int value = stoi(parts[0]), min_val = stoi(parts[1]), max_val = stoi(parts[2]);
        return (min_val <= value && value <= max_val) ? "VALID" : "INVALID";
    } catch (...) { return "INVALID"; }
}

// P014: IPv4 Validator
bool isValidIPv4(const string& ip) {
    stringstream ss(ip);
    string part;
    vector<string> parts;
    while (getline(ss, part, '.')) parts.push_back(part);
    if (parts.size() != 4) return false;
    for (const string& p : parts) {
        if (p.empty() || p.length() > 3) return false;
        for (char c : p) if (!isdigit(c)) return false;
        if (p.length() > 1 && p[0] == '0') return false;
        int num = stoi(p);
        if (num < 0 || num > 255) return false;
    }
    return true;
}

// P015: Username Validator
bool isValidUsername(const string& s) {
    if (s.length() < 3 || s.length() > 20) return false;
    if (!isalpha(s[0])) return false;
    for (char c : s) if (!isalnum(c) && c != '_' && c != '-') return false;
    return true;
}

// P016: HTML Text Escaper
string escapeHtml(const string& s) {
    string result;
    for (char c : s) {
        if (c == '&') result += "&amp;";
        else if (c == '<') result += "&lt;";
        else if (c == '>') result += "&gt;";
        else if (c == '"') result += "&quot;";
        else if (c == '\'') result += "&#39;";
        else result += c;
    }
    return result;
}

// P017: CSV Cell Escaper
string escapeCsvCell(const string& s) {
    bool needs = false;
    for (char c : s) if (c == ',' || c == '"' || c == '\n' || c == '\r') { needs = true; break; }
    if (!needs) return s;
    string escaped;
    for (char c : s) {
        if (c == '"') escaped += "\"\"";
        else escaped += c;
    }
    return "\"" + escaped + "\"";
}

// P018: JSON String Escaper
string escapeJsonString(const string& s) {
    string result;
    for (char c : s) {
        if (c == '"') result += "\\\"";
        else if (c == '\\') result += "\\\\";
        else if (c == '/') result += "\\/";
        else if (c == '\b') result += "\\b";
        else if (c == '\f') result += "\\f";
        else if (c == '\n') result += "\\n";
        else if (c == '\r') result += "\\r";
        else if (c == '\t') result += "\\t";
        else if ((unsigned char)c < 0x20) {
            char buf[8]; snprintf(buf, sizeof(buf), "\\u%04x", (unsigned char)c);
            result += buf;
        } else result += c;
    }
    return result;
}

// P019: URL Query Component Encoder
string encodeUrlComponent(const string& s) {
    const string unreserved = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~";
    string result;
    for (unsigned char c : s) {
        if (unreserved.find(c) != string::npos) result += c;
        else {
            char buf[4]; snprintf(buf, sizeof(buf), "%%%02X", c);
            result += buf;
        }
    }
    return result;
}

// P020: Template Placeholder Sanitizer
string sanitizeTemplate(const string& s) {
    string result;
    size_t i = 0;
    while (i < s.size()) {
        if (i + 1 < s.size() && s[i] == '{' && s[i+1] == '{') {
            size_t end = s.find("}}", i + 2);
            if (end != string::npos) {
                string key = s.substr(i + 2, end - i - 2);
                bool safe = !key.empty();
                for (char c : key) if (!isalnum(c) && c != '_') { safe = false; break; }
                if (safe) result += s.substr(i, end + 2 - i);
                i = end + 2;
                continue;
            }
        }
        result += s[i++];
    }
    return result;
}

// P021: Safe Path Normalizer
string safePathNormalize(const string& path) {
    if (path.empty() || path.find_first_not_of(" \t") == string::npos) return "";
    if (path.find('\\') != string::npos) return "";
    vector<string> segs;
    stringstream ss(path);
    string seg;
    while (getline(ss, seg, '/')) {
        if (seg.empty() || seg == ".") continue;
        if (seg == "..") { if (segs.empty()) return ""; segs.pop_back(); }
        else segs.push_back(seg);
    }
    string result;
    for (size_t i = 0; i < segs.size(); i++) {
        if (i > 0) result += "/";
        result += segs[i];
    }
    return result;
}

// P022: Path Extension Validator
bool isAllowedExtension(const string& path) {
    set<string> allowed = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".csv"};
    string fname = path;
    size_t pos = fname.find_last_of("/\\");
    if (pos != string::npos) fname = fname.substr(pos + 1);
    size_t dot = fname.rfind('.');
    if (dot == string::npos || dot == 0) return false;
    string ext = ".";
    for (char c : fname.substr(dot + 1)) ext += tolower(c);
    return allowed.count(ext) > 0;
}

// P023: Filename Sanitizer
string sanitizeFilename(const string& name) {
    string s = name.substr(0, min((size_t)200, name.size()));
    string result;
    for (char c : s) result += (isalnum(c) || c == '.' || c == '_' || c == '-') ? c : '_';
    string collapsed;
    bool last_underscore = false;
    for (char c : result) {
        if (c == '_') { if (!last_underscore) { collapsed += c; last_underscore = true; } }
        else { collapsed += c; last_underscore = false; }
    }
    size_t start = collapsed.find_first_not_of('_'), end = collapsed.find_last_not_of('_');
    if (start == string::npos) return "_";
    string trimmed = collapsed.substr(start, end - start + 1);
    return trimmed.empty() ? "_" : trimmed;
}

// P024: Archive Entry Path Checker
string checkArchiveEntry(const string& path) {
    if (path.empty()) return "safe";
    if (path[0] == '/') return "unsafe";
    if (path.find('\\') != string::npos) return "unsafe";
    int depth = 0;
    stringstream ss(path);
    string seg;
    while (getline(ss, seg, '/')) {
        if (seg.empty() || seg == ".") continue;
        if (seg == "..") { depth--; if (depth < 0) return "unsafe"; }
        else depth++;
    }
    return "safe";
}

// P025: File Type Allowlist
bool isAllowedFiletype(const string& ext) {
    set<string> allowed = {"jpg", "jpeg", "png", "gif", "bmp", "pdf", "txt", "csv", "json", "xml"};
    string e = ext;
    if (!e.empty() && e[0] == '.') e = e.substr(1);
    for (char& c : e) c = tolower(c);
    return !e.empty() && allowed.count(e) > 0;
}

// P026: SQL Identifier Validator
bool isValidSqlIdentifier(const string& name) {
    if (name.empty() || name.size() > 64) return false;
    if (!isalpha(name[0]) && name[0] != '_') return false;
    for (char c : name) if (!isalnum(c) && c != '_') return false;
    return true;
}

// P027: SQL String Literal Escaper
string escapeSqlString(const string& s) {
    string result;
    for (char c : s) {
        if (c == '\\') result += "\\\\";
        else if (c == '\'') result += "''";
        else result += c;
    }
    return result;
}

// P028: Parameterized Query Builder
string buildParamQuery(const string& s) {
    size_t pipe = s.find('|');
    if (pipe == string::npos) return "INVALID";
    string table = s.substr(0, pipe), conditions = s.substr(pipe + 1);
    if (!isValidSqlIdentifier(table)) return "INVALID";
    if (conditions.empty()) return "INVALID";
    stringstream ss(conditions);
    string pair;
    vector<string> cols;
    while (getline(ss, pair, ',')) {
        size_t eq = pair.find('=');
        if (eq == string::npos) return "INVALID";
        string col = pair.substr(0, eq);
        if (!isValidSqlIdentifier(col)) return "INVALID";
        cols.push_back(col);
    }
    if (cols.empty()) return "INVALID";
    string result = "SELECT * FROM " + table + " WHERE ";
    for (size_t i = 0; i < cols.size(); i++) {
        if (i > 0) result += " AND ";
        result += cols[i] + "=?";
    }
    return result;
}

// P029: Sort Direction Validator
string validateSortDirection(const string& s) {
    string trimmed;
    for (char c : s) if (!isspace(c)) trimmed += toupper(c);
    if (trimmed == "ASC" || trimmed == "DESC") return trimmed;
    return "INVALID";
}

// P030: Column Allowlist Checker
bool isAllowedColumn(const string& col) {
    set<string> allowed = {"id", "name", "email", "created_at", "status", "age", "role", "score"};
    string trimmed;
    for (char c : col) if (!isspace(c)) trimmed += c;
    return allowed.count(trimmed) > 0;
}

// P031: Shell Argument Quoter
string quoteShellArg(const string& s) {
    string escaped;
    for (char c : s) {
        if (c == '\'') escaped += "'\\''";
        else escaped += c;
    }
    return "'" + escaped + "'";
}

// P032: Command Name Allowlist
bool isAllowedCommand(const string& s) {
    set<string> allowed = {"ls", "cat", "echo", "grep", "find", "sort", "uniq", "wc", "head", "tail"};
    string trimmed;
    for (char c : s) if (!isspace(c)) trimmed += c;
    if (trimmed != s) {
        bool has_space = false;
        for (size_t i = 0; i < s.size(); i++) if (!isspace(s[i])) { size_t j = i; while (j < s.size() && !isspace(s[j])) j++; if (j < s.size() && s.find_first_not_of(" \t", j) != string::npos) has_space = true; break; }
        if (has_space) return false;
    }
    return allowed.count(trimmed) > 0;
}

// P033: Shell Metacharacter Detector
string detectShellMeta(const string& s) {
    const string dangerous = ";|&$`><(){}\\\"'";
    for (char c : s) if (dangerous.find(c) != string::npos || c == '\n' || c == '\r') return "unsafe";
    return "safe";
}

// P034: Environment Variable Name Validator
bool isValidEnvVar(const string& name) {
    if (name.empty() || name.size() > 64) return false;
    if (!isupper(name[0]) && name[0] != '_') return false;
    for (char c : name) if (!isupper(c) && !isdigit(c) && c != '_') return false;
    return true;
}

// P035: Command Argument Splitter
vector<string> splitArgs(const string& s) {
    vector<string> result;
    if (s.empty()) return result;
    string current;
    bool in_quotes = false;
    for (char c : s) {
        if (c == '"') {
            if (in_quotes) { result.push_back(current); current = ""; in_quotes = false; }
            else { if (!current.empty()) { result.push_back(current); current = ""; } in_quotes = true; }
        } else if (c == ' ' && !in_quotes) {
            if (!current.empty()) { result.push_back(current); current = ""; }
        } else current += c;
    }
    if (!current.empty()) result.push_back(current);
    return result;
}

// P036: Safe Literal Parser
string parseSafeLiteral(const string& s) {
    if (s == "true" || s == "false" || s == "null") return s;
    bool neg = false;
    string digits;
    size_t i = 0;
    if (!s.empty() && s[0] == '-') { neg = true; i = 1; }
    if (i >= s.size()) return "INVALID";
    for (; i < s.size(); i++) {
        if (!isdigit(s[i])) return "INVALID";
        digits += s[i];
    }
    if (digits.empty()) return "INVALID";
    if ((digits.size() > 1 && digits[0] == '0') || (neg && digits.size() > 1 && digits[0] == '0')) return "INVALID";
    return (neg ? "-" : "") + digits;
}

// P037: Configuration Boolean Parser
string parseConfigBool(const string& s) {
    string trimmed;
    for (char c : s) if (!isspace(c)) trimmed += tolower(c);
    if (trimmed == "true" || trimmed == "yes" || trimmed == "1" || trimmed == "on" || trimmed == "enabled") return "true";
    if (trimmed == "false" || trimmed == "no" || trimmed == "0" || trimmed == "off" || trimmed == "disabled") return "false";
    return "INVALID";
}

// P038: Configuration Key Allowlist
bool isAllowedConfigKey(const string& key) {
    set<string> allowed = {"host", "port", "database", "username", "password", "timeout", "max_connections", "ssl_enabled", "log_level", "retry_count"};
    string trimmed;
    for (char c : key) if (!isspace(c)) trimmed += c;
    return allowed.count(trimmed) > 0;
}

// P039: Structured Token Decoder
string validateToken(const string& s) {
    size_t p1 = s.find('.'), p2 = s.find('.', p1 + 1);
    if (p1 == string::npos || p2 == string::npos) return "invalid";
    string header = s.substr(0, p1), payload = s.substr(p1 + 1, p2 - p1 - 1), checksum = s.substr(p2 + 1);
    const string base64url = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
    for (char c : header) if (base64url.find(c) == string::npos) return "invalid";
    for (char c : payload) if (base64url.find(c) == string::npos) return "invalid";
    const string hex = "0123456789abcdef";
    if (checksum.size() != 8) return "invalid";
    for (char c : checksum) if (hex.find(c) == string::npos) return "invalid";
    return "valid";
}

// P040: Safe Numeric Expression Validator
string validateNumericExpr(const string& s) {
    if (s.empty()) return "invalid";
    string trimmed;
    for (char c : s) if (!isspace(c)) trimmed += c;
    if (trimmed.empty()) return "invalid";
    const string ops = "+-*/";
    size_t i = 0;
    auto parseNum = [&]() -> bool {
        if (i >= trimmed.size()) return false;
        bool neg = false;
        if (trimmed[i] == '-') { neg = true; i++; }
        if (i >= trimmed.size() || !isdigit(trimmed[i])) return false;
        if (trimmed[i] == '0') {
            i++;
            if (i < trimmed.size() && isdigit(trimmed[i])) return false;
        } else {
            while (i < trimmed.size() && isdigit(trimmed[i])) i++;
        }
        return true;
    };
    if (!parseNum()) return "invalid";
    while (i < trimmed.size()) {
        if (ops.find(trimmed[i]) == string::npos) return "invalid";
        i++;
        if (!parseNum()) return "invalid";
    }
    return "valid";
}

// P041: Frequency Counter Large Input
map<int, int> frequencyCounter(vector<int>& nums) {
    map<int, int> freq;
    for (int n : nums) freq[n]++;
    return freq;
}

// P042: Duplicate Detector
bool hasDuplicate(vector<int>& nums) {
    unordered_set<int> seen;
    for (int n : nums) {
        if (seen.count(n)) return true;
        seen.insert(n);
    }
    return false;
}

// P043: Streaming Sum
long long streamingSum(vector<int>& nums) {
    long long sum = 0;
    for (int n : nums) sum += n;
    return sum;
}

// P044: Bounded Log Processor
map<string, int> boundedLogProcessor(const string& log, int maxLines) {
    map<string, int> result = {{"kept", 0}, {"total_words", 0}};
    if (maxLines <= 0) return result;
    stringstream ss(log);
    string line;
    int kept = 0;
    while (getline(ss, line) && kept < maxLines) {
        string trimmed;
        for (char c : line) if (!isspace(c)) trimmed += c;
        if (trimmed.empty()) continue;
        kept++;
        stringstream ws(line);
        string word;
        while (ws >> word) result["total_words"]++;
    }
    result["kept"] = kept;
    return result;
}

// P045: Top-K Frequent Values
vector<int> topKFrequent(vector<int>& nums, int k) {
    if (k <= 0 || nums.empty()) return {};
    map<int, int> freq;
    for (int n : nums) freq[n]++;
    vector<pair<int, int>> items(freq.begin(), freq.end());
    sort(items.begin(), items.end(), [](const pair<int,int>& a, const pair<int,int>& b) {
        if (a.second != b.second) return a.second > b.second;
        return a.first < b.first;
    });
    vector<int> result;
    for (int i = 0; i < min(k, (int)items.size()); i++) result.push_back(items[i].first);
    sort(result.begin(), result.end());
    return result;
}

// P046: Token Format Validator
string validateTokenFormat(const string& token) {
    if (token.empty() || token.size() < 8 || token.size() > 32) return "invalid";
    if (!isalpha(token[0])) return "invalid";
    for (char c : token) if (!isalnum(c) && c != '-') return "invalid";
    return "valid";
}

// P047: Permission Rule Evaluator
string evaluatePermission(const string& role, const string& action) {
    unordered_map<string, unordered_set<string>> perms = {
        {"admin", {"read", "write", "delete", "execute"}},
        {"editor", {"read", "write"}},
        {"viewer", {"read"}},
        {"guest", {}}
    };
    if (perms.count(role) && perms[role].count(action)) return "allowed";
    return "denied";
}

// P048: Role Permission Checker
bool roleHasPermission(const string& role, const string& permission) {
    unordered_map<string, unordered_set<string>> perms = {
        {"admin", {"read", "write", "delete", "execute"}},
        {"editor", {"read", "write"}},
        {"viewer", {"read"}},
        {"guest", {}}
    };
    return perms.count(role) && perms[role].count(permission);
}

// P049: Session Timeout Checker
string checkSession(int lastActive, int currentTime, int timeout) {
    if (currentTime < lastActive) return "invalid";
    int elapsed = currentTime - lastActive;
    return (elapsed <= timeout) ? "active" : "expired";
}

// P050: Access Scope Validator
string validateScope(const string& requested, vector<string> allowed) {
    if (allowed.empty()) return "denied";
    unordered_set<string> allowedSet(allowed.begin(), allowed.end());
    if (allowedSet.count(requested)) return "granted";
    size_t pos = 0;
    while ((pos = requested.find(':', pos)) != string::npos) {
        string parent = requested.substr(0, pos);
        if (allowedSet.count(parent)) return "granted";
        pos++;
    }
    return "denied";
}