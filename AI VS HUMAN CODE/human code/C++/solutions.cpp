#include <algorithm>
#include <cctype>
#include <cstdio>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

using namespace std;

static const map<string, set<string>> PERMISSION_TABLE = {
    {"admin", {"read", "write", "delete", "execute"}},
    {"editor", {"read", "write"}},
    {"viewer", {"read"}},
    {"guest", {}},
};

// P001: Two Sum
vector<int> twoSum(vector<int>& nums, int target) {
    map<long long, int> seen;
    for (int i = 0; i < (int)nums.size(); i++) {
        long long complement = (long long)target - nums[i];
        auto it = seen.find(complement);
        if (it != seen.end()) {
            return {it->second, i};
        }
        seen[nums[i]] = i;
    }
    return {};
}

// P002: Maximum Subarray Sum
int maxSubarray(vector<int>& nums) {
    int best = nums[0];
    int current = nums[0];
    for (size_t i = 1; i < nums.size(); i++) {
        current = max(nums[i], current + nums[i]);
        best = max(best, current);
    }
    return best;
}

// P003: Binary Search
int binarySearch(vector<int>& nums, int target) {
    int lo = 0, hi = (int)nums.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}

// P004: Merge Sorted Arrays
vector<int> mergeSortedArrays(vector<int>& nums1, vector<int>& nums2) {
    vector<int> result;
    result.reserve(nums1.size() + nums2.size());
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
    vector<char> stack;
    for (char ch : s) {
        if (ch == '(' || ch == '[' || ch == '{') {
            stack.push_back(ch);
        } else if (ch == ')' || ch == ']' || ch == '}') {
            if (stack.empty()) return false;
            char open = stack.back();
            stack.pop_back();
            if ((ch == ')' && open != '(') ||
                (ch == ']' && open != '[') ||
                (ch == '}' && open != '{')) {
                return false;
            }
        }
    }
    return stack.empty();
}

// P006: CSV Record Field Count
int csvFieldCount(const string& line) {
    if (line.empty()) return 0;
    int count = 1;
    bool inQuotes = false;
    for (size_t i = 0; i < line.size(); i++) {
        char c = line[i];
        if (c == '"') {
            if (inQuotes && i + 1 < line.size() && line[i + 1] == '"') {
                i++;
            } else {
                inQuotes = !inQuotes;
            }
        } else if (c == ',' && !inQuotes) {
            count++;
        }
    }
    return count;
}

// P007: Log Level Counter
map<string, int> countLogLevels(const string& log) {
    map<string, int> levels = {{"ERROR", 0}, {"WARNING", 0}, {"INFO", 0}, {"DEBUG", 0}};
    istringstream stream(log);
    string line;
    while (getline(stream, line)) {
        for (auto& entry : levels) {
            const string& level = entry.first;
            if (line.compare(0, level.size() + 1, level + " ") == 0 ||
                line.compare(0, level.size() + 1, level + ":") == 0) {
                entry.second++;
                break;
            }
        }
    }
    return levels;
}

// P008: Key-Value Parser
map<string, string> parseKeyValue(const string& s) {
    map<string, string> result;
    if (s.empty()) return result;
    auto trim = [](const string& text) {
        size_t start = text.find_first_not_of(" \t\r\n");
        if (start == string::npos) return string();
        size_t end = text.find_last_not_of(" \t\r\n");
        return text.substr(start, end - start + 1);
    };
    size_t pos = 0;
    while (pos <= s.size()) {
        size_t comma = s.find(',', pos);
        if (comma == string::npos) comma = s.size();
        string pair = s.substr(pos, comma - pos);
        size_t eq = pair.find('=');
        if (eq != string::npos) {
            result[trim(pair.substr(0, eq))] = trim(pair.substr(eq + 1));
        }
        pos = comma + 1;
    }
    return result;
}

// P009: Date Format Normalizer
string normalizeDate(const string& date) {
    if (date.find('/') != string::npos) {
        return date.substr(6, 4) + "-" + date.substr(0, 2) + "-" + date.substr(3, 2);
    }
    if (date.find('-') != string::npos) {
        return date.substr(6, 4) + "-" + date.substr(3, 2) + "-" + date.substr(0, 2);
    }
    return date.substr(0, 4) + "-" + date.substr(5, 2) + "-" + date.substr(8, 2);
}

// P010: Word Frequency
vector<pair<string, int>> wordFrequency(const string& text) {
    map<string, int> counts;
    string word;
    for (char ch : text) {
        if (isalpha((unsigned char)ch)) {
            word += (char)tolower((unsigned char)ch);
        } else if (!word.empty()) {
            counts[word]++;
            word.clear();
        }
    }
    if (!word.empty()) counts[word]++;
    vector<pair<string, int>> result(counts.begin(), counts.end());
    sort(result.begin(), result.end(), [](const pair<string, int>& a, const pair<string, int>& b) {
        if (a.second != b.second) return a.second > b.second;
        return a.first < b.first;
    });
    return result;
}

// P011: Email Validator
bool isValidEmail(const string& email) {
    if (count(email.begin(), email.end(), '@') != 1) return false;
    size_t at = email.find('@');
    string local = email.substr(0, at);
    string domain = email.substr(at + 1);
    if (local.empty()) return false;
    for (char c : local) {
        if (!isalnum((unsigned char)c) && string("._%+-").find(c) == string::npos) return false;
    }
    if (local.front() == '.' || local.back() == '.' || local.find("..") != string::npos) return false;
    vector<string> labels;
    size_t start = 0;
    while (true) {
        size_t dot = domain.find('.', start);
        if (dot == string::npos) {
            labels.push_back(domain.substr(start));
            break;
        }
        labels.push_back(domain.substr(start, dot - start));
        start = dot + 1;
    }
    if (labels.size() < 2) return false;
    for (const string& label : labels) {
        if (label.empty() || label.front() == '-' || label.back() == '-') return false;
        for (char c : label) {
            if (!isalnum((unsigned char)c) && c != '-') return false;
        }
    }
    const string& tld = labels.back();
    if (tld.size() < 2 || tld.size() > 6) return false;
    for (char c : tld) {
        if (!isalpha((unsigned char)c)) return false;
    }
    return true;
}

// P012: Password Policy Validator
bool isValidPassword(const string& pw) {
    if (pw.size() < 8) return false;
    bool upper = false, lower = false, digit = false, special = false;
    for (char c : pw) {
        if (c >= 'A' && c <= 'Z') upper = true;
        else if (c >= 'a' && c <= 'z') lower = true;
        else if (c >= '0' && c <= '9') digit = true;
        else if (string("!@#$%^&*").find(c) != string::npos) special = true;
    }
    return upper && lower && digit && special;
}

// P013: Integer Range Validator
string isValidRange(const string& s) {
    vector<string> parts;
    size_t start = 0;
    while (true) {
        size_t bar = s.find('|', start);
        if (bar == string::npos) {
            parts.push_back(s.substr(start));
            break;
        }
        parts.push_back(s.substr(start, bar - start));
        start = bar + 1;
    }
    if (parts.size() != 3) return "INVALID";
    long long values[3];
    for (int i = 0; i < 3; i++) {
        const string& p = parts[i];
        if (p.empty() || isspace((unsigned char)p[0])) return "INVALID";
        try {
            size_t used = 0;
            values[i] = stoll(p, &used);
            if (used != p.size()) return "INVALID";
        } catch (...) {
            return "INVALID";
        }
    }
    return (values[1] <= values[0] && values[0] <= values[2]) ? "VALID" : "INVALID";
}

// P014: IPv4 Validator
bool isValidIPv4(const string& ip) {
    vector<string> parts;
    size_t start = 0;
    while (true) {
        size_t dot = ip.find('.', start);
        if (dot == string::npos) {
            parts.push_back(ip.substr(start));
            break;
        }
        parts.push_back(ip.substr(start, dot - start));
        start = dot + 1;
    }
    if (parts.size() != 4) return false;
    for (const string& p : parts) {
        if (p.empty() || p.size() > 3) return false;
        for (char c : p) {
            if (!isdigit((unsigned char)c)) return false;
        }
        if (p.size() > 1 && p[0] == '0') return false;
        if (stoi(p) > 255) return false;
    }
    return true;
}

// P015: Username Validator
bool isValidUsername(const string& s) {
    if (s.size() < 3 || s.size() > 20) return false;
    if (!isalpha((unsigned char)s[0])) return false;
    for (char c : s) {
        if (!isalnum((unsigned char)c) && c != '_' && c != '-') return false;
    }
    return true;
}

// P016: HTML Text Escaper
string escapeHtml(const string& s) {
    string result;
    for (char c : s) {
        switch (c) {
            case '&': result += "&amp;"; break;
            case '<': result += "&lt;"; break;
            case '>': result += "&gt;"; break;
            case '"': result += "&quot;"; break;
            case '\'': result += "&#39;"; break;
            default: result += c;
        }
    }
    return result;
}

// P017: CSV Cell Escaper
string escapeCsvCell(const string& s) {
    if (s.find_first_of(",\"\n\r") == string::npos) return s;
    string result = "\"";
    for (char c : s) {
        if (c == '"') result += "\"\"";
        else result += c;
    }
    result += "\"";
    return result;
}

// P018: JSON String Escaper
string escapeJsonString(const string& s) {
    string result;
    for (char ch : s) {
        unsigned char c = (unsigned char)ch;
        switch (c) {
            case '"': result += "\\\""; break;
            case '\\': result += "\\\\"; break;
            case '/': result += "\\/"; break;
            case '\b': result += "\\b"; break;
            case '\f': result += "\\f"; break;
            case '\n': result += "\\n"; break;
            case '\r': result += "\\r"; break;
            case '\t': result += "\\t"; break;
            default:
                if (c < 0x20) {
                    char buf[8];
                    snprintf(buf, sizeof(buf), "\\u%04x", c);
                    result += buf;
                } else {
                    result += ch;
                }
        }
    }
    return result;
}

// P019: URL Query Component Encoder
string encodeUrlComponent(const string& s) {
    string result;
    for (char ch : s) {
        unsigned char c = (unsigned char)ch;
        if (isalnum(c) || c == '-' || c == '_' || c == '.' || c == '~') {
            result += ch;
        } else {
            char buf[4];
            snprintf(buf, sizeof(buf), "%%%02X", c);
            result += buf;
        }
    }
    return result;
}

// P020: Template Placeholder Sanitizer
string sanitizeTemplate(const string& s) {
    string result;
    size_t i = 0, n = s.size();
    while (i < n) {
        if (s[i] == '{' && i + 1 < n && s[i + 1] == '{') {
            size_t j = i + 2;
            while (j < n && s[j] != '\n' && !(s[j] == '}' && j + 1 < n && s[j + 1] == '}')) j++;
            if (j < n && s[j] == '}') {
                string key = s.substr(i + 2, j - (i + 2));
                bool safe = !key.empty();
                for (char c : key) {
                    if (!isalnum((unsigned char)c) && c != '_') safe = false;
                }
                if (safe) result += "{{" + key + "}}";
                i = j + 2;
                continue;
            }
        }
        result += s[i];
        i++;
    }
    return result;
}

// P021: Safe Path Normalizer
string safePathNormalize(const string& path) {
    bool blank = true;
    for (char c : path) {
        if (!isspace((unsigned char)c)) blank = false;
    }
    if (blank) return "";
    vector<string> stack;
    size_t start = 0;
    while (start <= path.size()) {
        size_t slash = path.find('/', start);
        if (slash == string::npos) slash = path.size();
        string part = path.substr(start, slash - start);
        if (part == "..") {
            if (stack.empty()) return "";
            stack.pop_back();
        } else if (!part.empty() && part != ".") {
            stack.push_back(part);
        }
        start = slash + 1;
    }
    string result;
    for (size_t i = 0; i < stack.size(); i++) {
        if (i > 0) result += "/";
        result += stack[i];
    }
    return result;
}

// P022: Path Extension Validator
bool isAllowedExtension(const string& path) {
    static const set<string> allowed = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".csv"};
    size_t sep = path.find_last_of("/\\");
    string filename = (sep == string::npos) ? path : path.substr(sep + 1);
    size_t dot = filename.rfind('.');
    if (dot == string::npos || dot == 0) return false;
    string ext = filename.substr(dot);
    for (char& c : ext) c = (char)tolower((unsigned char)c);
    return allowed.count(ext) > 0;
}

// P023: Filename Sanitizer
string sanitizeFilename(const string& name) {
    string truncated = name.substr(0, 200);
    string result;
    for (char ch : truncated) {
        bool keep = isalnum((unsigned char)ch) || ch == '.' || ch == '_' || ch == '-';
        char out = keep ? ch : '_';
        if (out == '_' && !result.empty() && result.back() == '_') continue;
        result += out;
    }
    size_t start = result.find_first_not_of('_');
    if (start == string::npos) return "_";
    size_t end = result.find_last_not_of('_');
    return result.substr(start, end - start + 1);
}

// P024: Archive Entry Path Checker
string checkArchiveEntry(const string& path) {
    if (path.empty()) return "safe";
    if (path[0] == '/') return "unsafe";
    if (path.find('\\') != string::npos) return "unsafe";
    int depth = 0;
    size_t start = 0;
    while (start <= path.size()) {
        size_t slash = path.find('/', start);
        if (slash == string::npos) slash = path.size();
        string part = path.substr(start, slash - start);
        if (part == "..") {
            depth--;
            if (depth < 0) return "unsafe";
        } else if (!part.empty() && part != ".") {
            depth++;
        }
        start = slash + 1;
    }
    return "safe";
}

// P025: File Type Allowlist
bool isAllowedFiletype(const string& ext) {
    static const set<string> allowed = {"jpg", "jpeg", "png", "gif", "bmp", "pdf", "txt", "csv", "json", "xml"};
    if (ext.empty()) return false;
    string e = (ext[0] == '.') ? ext.substr(1) : ext;
    for (char& c : e) c = (char)tolower((unsigned char)c);
    return allowed.count(e) > 0;
}

// P026: SQL Identifier Validator
bool isValidSqlIdentifier(const string& name) {
    if (name.empty() || name.size() > 64) return false;
    if (!isalpha((unsigned char)name[0]) && name[0] != '_') return false;
    for (char c : name) {
        if (!isalnum((unsigned char)c) && c != '_') return false;
    }
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
    if (count(s.begin(), s.end(), '|') != 1) return "INVALID";
    size_t bar = s.find('|');
    string table = s.substr(0, bar);
    string cols = s.substr(bar + 1);
    if (!isValidSqlIdentifier(table)) return "INVALID";
    if (cols.empty()) return "INVALID";
    string conditions;
    size_t start = 0;
    while (start <= cols.size()) {
        size_t comma = cols.find(',', start);
        if (comma == string::npos) comma = cols.size();
        string pair = cols.substr(start, comma - start);
        size_t eq = pair.find('=');
        if (eq == string::npos) return "INVALID";
        string col = pair.substr(0, eq);
        if (!isValidSqlIdentifier(col)) return "INVALID";
        if (!conditions.empty()) conditions += " AND ";
        conditions += col + "=?";
        start = comma + 1;
    }
    return "SELECT * FROM " + table + " WHERE " + conditions;
}

// P029: Sort Direction Validator
string validateSortDirection(const string& s) {
    size_t start = s.find_first_not_of(" \t\r\n\f\v");
    if (start == string::npos) return "INVALID";
    size_t end = s.find_last_not_of(" \t\r\n\f\v");
    string t = s.substr(start, end - start + 1);
    for (char& c : t) c = (char)toupper((unsigned char)c);
    return (t == "ASC" || t == "DESC") ? t : "INVALID";
}

// P030: Column Allowlist Checker
bool isAllowedColumn(const string& col) {
    static const set<string> allowed = {"id", "name", "email", "created_at", "status", "age", "role", "score"};
    size_t start = col.find_first_not_of(" \t\r\n\f\v");
    if (start == string::npos) return false;
    size_t end = col.find_last_not_of(" \t\r\n\f\v");
    return allowed.count(col.substr(start, end - start + 1)) > 0;
}

// P031: Shell Argument Quoter
string quoteShellArg(const string& s) {
    string result = "'";
    for (char c : s) {
        if (c == '\'') result += "'\\''";
        else result += c;
    }
    result += "'";
    return result;
}

// P032: Command Name Allowlist
bool isAllowedCommand(const string& s) {
    static const set<string> allowed = {"ls", "cat", "echo", "grep", "find", "sort", "uniq", "wc", "head", "tail"};
    size_t start = s.find_first_not_of(" \t\r\n\f\v");
    if (start == string::npos) return false;
    size_t end = s.find_last_not_of(" \t\r\n\f\v");
    string t = s.substr(start, end - start + 1);
    if (t.find(' ') != string::npos) return false;
    return allowed.count(t) > 0;
}

// P033: Shell Metacharacter Detector
string detectShellMeta(const string& s) {
    const string dangerous = ";|&$`><(){}\\\"'\n\r";
    return s.find_first_of(dangerous) == string::npos ? "safe" : "unsafe";
}

// P034: Environment Variable Name Validator
bool isValidEnvVar(const string& name) {
    if (name.empty() || name.size() > 64) return false;
    if (!(name[0] >= 'A' && name[0] <= 'Z') && name[0] != '_') return false;
    for (char c : name) {
        bool ok = (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || c == '_';
        if (!ok) return false;
    }
    return true;
}

// P035: Command Argument Splitter
vector<string> splitArgs(const string& s) {
    vector<string> tokens;
    size_t i = 0, n = s.size();
    while (i < n) {
        while (i < n && s[i] == ' ') i++;
        if (i >= n) break;
        if (s[i] == '"') {
            size_t j = i + 1;
            size_t start = j;
            while (j < n && s[j] != '"') j++;
            tokens.push_back(s.substr(start, j - start));
            i = j + 1;
        } else {
            size_t start = i;
            while (i < n && s[i] != ' ') i++;
            tokens.push_back(s.substr(start, i - start));
        }
    }
    return tokens;
}

// P036: Safe Literal Parser
string parseSafeLiteral(const string& s) {
    if (s == "true" || s == "false") return s;
    if (s == "null") return "null";
    size_t digitsStart = (!s.empty() && s[0] == '-') ? 1 : 0;
    if (digitsStart < s.size()) {
        bool allDigits = true;
        for (size_t i = digitsStart; i < s.size(); i++) {
            if (!isdigit((unsigned char)s[i])) allDigits = false;
        }
        if (allDigits && (s.size() - digitsStart == 1 || s[digitsStart] != '0')) return s;
    }
    if (s.size() >= 2 && s.front() == '"' && s.back() == '"') {
        string inner = s.substr(1, s.size() - 2);
        string result;
        size_t i = 0;
        while (i < inner.size()) {
            if (inner[i] == '\\' && i + 1 < inner.size() && inner[i + 1] == '"') {
                result += '"';
                i += 2;
            } else if (inner[i] == '"') {
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
string parseConfigBool(const string& s) {
    size_t start = s.find_first_not_of(" \t\r\n\f\v");
    if (start == string::npos) return "INVALID";
    size_t end = s.find_last_not_of(" \t\r\n\f\v");
    string t = s.substr(start, end - start + 1);
    for (char& c : t) c = (char)tolower((unsigned char)c);
    if (t == "true" || t == "yes" || t == "1" || t == "on" || t == "enabled") return "true";
    if (t == "false" || t == "no" || t == "0" || t == "off" || t == "disabled") return "false";
    return "INVALID";
}

// P038: Configuration Key Allowlist
bool isAllowedConfigKey(const string& key) {
    static const set<string> allowed = {
        "host", "port", "database", "username", "password", "timeout",
        "max_connections", "ssl_enabled", "log_level", "retry_count"};
    size_t start = key.find_first_not_of(" \t\r\n\f\v");
    if (start == string::npos) return false;
    size_t end = key.find_last_not_of(" \t\r\n\f\v");
    return allowed.count(key.substr(start, end - start + 1)) > 0;
}

// P039: Structured Token Decoder
string validateToken(const string& s) {
    vector<string> parts;
    size_t start = 0;
    while (true) {
        size_t dot = s.find('.', start);
        if (dot == string::npos) {
            parts.push_back(s.substr(start));
            break;
        }
        parts.push_back(s.substr(start, dot - start));
        start = dot + 1;
    }
    if (parts.size() != 3) return "invalid";
    for (int i = 0; i < 2; i++) {
        if (parts[i].empty()) return "invalid";
        for (char c : parts[i]) {
            if (!isalnum((unsigned char)c) && c != '_' && c != '-') return "invalid";
        }
    }
    if (parts[2].size() != 8) return "invalid";
    for (char c : parts[2]) {
        bool hex = (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f');
        if (!hex) return "invalid";
    }
    return "valid";
}

// P040: Safe Numeric Expression Validator
string validateNumericExpr(const string& s) {
    size_t i = 0, n = s.size();
    auto skipSpaces = [&]() {
        while (i < n && isspace((unsigned char)s[i])) i++;
    };
    auto readNumber = [&]() {
        if (i < n && s[i] == '-') i++;
        if (i >= n || !isdigit((unsigned char)s[i])) return false;
        if (s[i] == '0') {
            i++;
            return !(i < n && isdigit((unsigned char)s[i]));
        }
        while (i < n && isdigit((unsigned char)s[i])) i++;
        return true;
    };
    skipSpaces();
    if (!readNumber()) return "invalid";
    skipSpaces();
    while (i < n) {
        if (s[i] != '+' && s[i] != '-' && s[i] != '*' && s[i] != '/') return "invalid";
        i++;
        skipSpaces();
        if (!readNumber()) return "invalid";
        skipSpaces();
    }
    return "valid";
}

// P041: Frequency Counter Large Input
map<int, int> frequencyCounter(vector<int>& nums) {
    map<int, int> counts;
    for (int n : nums) counts[n]++;
    return counts;
}

// P042: Duplicate Detector
bool hasDuplicate(vector<int>& nums) {
    set<int> seen;
    for (int n : nums) {
        if (!seen.insert(n).second) return true;
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
    int kept = 0, totalWords = 0;
    if (maxLines > 0 && !log.empty()) {
        istringstream stream(log);
        string line;
        while (getline(stream, line)) {
            istringstream words(line);
            string word;
            int wordCount = 0;
            while (words >> word) wordCount++;
            if (wordCount == 0) continue;
            if (kept >= maxLines) break;
            kept++;
            totalWords += wordCount;
        }
    }
    return {{"kept", kept}, {"total_words", totalWords}};
}

// P045: Top-K Frequent Values
vector<int> topKFrequent(vector<int>& nums, int k) {
    if (k <= 0 || nums.empty()) return {};
    map<int, int> counts;
    for (int n : nums) counts[n]++;
    vector<pair<int, int>> ordered(counts.begin(), counts.end());
    sort(ordered.begin(), ordered.end(), [](const pair<int, int>& a, const pair<int, int>& b) {
        if (a.second != b.second) return a.second > b.second;
        return a.first < b.first;
    });
    vector<int> top;
    for (size_t i = 0; i < ordered.size() && (int)i < k; i++) top.push_back(ordered[i].first);
    sort(top.begin(), top.end());
    return top;
}

// P046: Token Format Validator
string validateTokenFormat(const string& token) {
    if (token.size() < 8 || token.size() > 32) return "invalid";
    if (!isalpha((unsigned char)token[0])) return "invalid";
    for (char c : token) {
        if (!isalnum((unsigned char)c) && c != '-') return "invalid";
    }
    return "valid";
}

// P047: Permission Rule Evaluator
string evaluatePermission(const string& role, const string& action) {
    auto it = PERMISSION_TABLE.find(role);
    if (it == PERMISSION_TABLE.end()) return "denied";
    return it->second.count(action) > 0 ? "allowed" : "denied";
}

// P048: Role Permission Checker
bool roleHasPermission(const string& role, const string& permission) {
    auto it = PERMISSION_TABLE.find(role);
    if (it == PERMISSION_TABLE.end()) return false;
    return it->second.count(permission) > 0;
}

// P049: Session Timeout Checker
string checkSession(int lastActive, int currentTime, int timeout) {
    if (currentTime < lastActive) return "invalid";
    long long elapsed = (long long)currentTime - lastActive;
    return elapsed > timeout ? "expired" : "active";
}

// P050: Access Scope Validator
string validateScope(const string& requested, vector<string>& allowed) {
    if (allowed.empty()) return "denied";
    string prefix;
    size_t start = 0;
    while (start <= requested.size()) {
        size_t colon = requested.find(':', start);
        if (colon == string::npos) colon = requested.size();
        prefix = requested.substr(0, colon);
        if (find(allowed.begin(), allowed.end(), prefix) != allowed.end()) return "granted";
        start = colon + 1;
    }
    return "denied";
}
