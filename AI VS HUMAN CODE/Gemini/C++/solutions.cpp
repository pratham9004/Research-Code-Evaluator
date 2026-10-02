#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <unordered_map>
#include <set>
#include <unordered_set>
#include <algorithm>
#include <cctype>
#include <sstream>
#include <regex>

using namespace std;

// ==============================
// P001 — Two Sum
// ==============================
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> mp;
    for (int i = 0; i < (int)nums.size(); i++) {
        int comp = target - nums[i];
        if (mp.count(comp)) return {mp[comp], i};
        mp[nums[i]] = i;
    }
    return {};
}

// ==============================
// P002 — Maximum Subarray Sum
// ==============================
int maxSubarray(vector<int>& nums) {
    int maxSoFar = nums[0], currMax = nums[0];
    for (size_t i = 1; i < nums.size(); i++) {
        currMax = max(nums[i], currMax + nums[i]);
        maxSoFar = max(maxSoFar, currMax);
    }
    return maxSoFar;
}

// ==============================
// P003 — Binary Search
// ==============================
int binarySearch(vector<int>& nums, int target) {
    int left = 0, right = (int)nums.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

// ==============================
// P004 — Merge Sorted Arrays
// ==============================
vector<int> mergeSortedArrays(vector<int>& nums1, vector<int>& nums2) {
    vector<int> res;
    size_t i = 0, j = 0;
    while (i < nums1.size() && j < nums2.size()) {
        if (nums1[i] <= nums2[j]) res.push_back(nums1[i++]);
        else res.push_back(nums2[j++]);
    }
    while (i < nums1.size()) res.push_back(nums1[i++]);
    while (j < nums2.size()) res.push_back(nums2[j++]);
    return res;
}

// ==============================
// P005 — Balanced Brackets
// ==============================
bool isBalanced(const string& s) {
    vector<char> st;
    for (char c : s) {
        if (c == '(' || c == '{' || c == '[') st.push_back(c);
        else {
            if (st.empty()) return false;
            char top = st.back(); st.pop_back();
            if ((c == ')' && top != '(') || (c == '}' && top != '{') || (c == ']' && top != '[')) return false;
        }
    }
    return st.empty();
}

// ==============================
// P006 — CSV Record Field Count
// ==============================
int csvFieldCount(const string& line) {
    if (line.empty()) return 0;
    int count = 1;
    bool inQuotes = false;
    for (char c : line) {
        if (c == '"') inQuotes = !inQuotes;
        else if (c == ',' && !inQuotes) count++;
    }
    return count;
}

// ==============================
// P007 — Log Level Counter
// ==============================
map<string, int> countLogLevels(const string& log) {
    map<string, int> res = {{"ERROR", 0}, {"WARNING", 0}, {"INFO", 0}, {"DEBUG", 0}};
    stringstream ss(log);
    string line;
    while (getline(ss, line)) {
        size_t first = line.find_first_not_of(" \t\r\n");
        if (first == string::npos) continue;
        string trimmed = line.substr(first);
        for (auto& pair : res) {
            string k = pair.first;
            if (trimmed.compare(0, k.length() + 1, k + " ") == 0 || trimmed.compare(0, k.length() + 1, k + ":") == 0) {
                res[k]++;
                break;
            }
        }
    }
    return res;
}

// ==============================
// P008 — Key-Value Parser
// ==============================
map<string, string> parseKeyValue(const string& s) {
    map<string, string> res;
    stringstream ss(s);
    string pair;
    while (getline(ss, pair, ',')) {
        size_t eq = pair.find('=');
        if (eq != string::npos) {
            string k = pair.substr(0, eq), v = pair.substr(eq + 1);
            auto trim = [](string str) {
                size_t start = str.find_first_not_of(" \t\r\n");
                size_t end = str.find_last_not_of(" \t\r\n");
                return (start == string::npos) ? "" : str.substr(start, end - start + 1);
            };
            res[trim(k)] = trim(v);
        }
    }
    return res;
}

// ==============================
// P009 — Date Format Normalizer
// ==============================
string normalizeDate(const string& date) {
    string d = date;
    d.erase(0, d.find_first_not_of(" \t\r\n"));
    d.erase(d.find_last_not_of(" \t\r\n") + 1);
    char buf[16];
    if (d.find('/') != string::npos) {
        int m, day, y;
        sscanf(d.c_str(), "%d/%d/%d", &m, &day, &y);
        snprintf(buf, sizeof(buf), "%04d-%02d-%02d", y, m, day);
        return string(buf);
    } else if (d.find('-') != string::npos) {
        int day, m, y;
        sscanf(d.c_str(), "%d-%d-%d", &day, &m, &y);
        snprintf(buf, sizeof(buf), "%04d-%02d-%02d", y, m, day);
        return string(buf);
    } else if (d.find('.') != string::npos) {
        int y, m, day;
        sscanf(d.c_str(), "%d.%d.%d", &y, &m, &day);
        snprintf(buf, sizeof(buf), "%04d-%02d-%02d", y, m, day);
        return string(buf);
    }
    return d;
}

// ==============================
// P010 — Word Frequency
// ==============================
vector<pair<string, int>> wordFrequency(const string& text) {
    map<string, int> counts;
    string w = "";
    for (char c : text) {
        if (isalpha(c)) w += tolower(c);
        else if (!w.empty()) { counts[w]++; w = ""; }
    }
    if (!w.empty()) counts[w]++;
    vector<pair<string, int>> vec(counts.begin(), counts.end());
    sort(vec.begin(), vec.end(), [](const pair<string, int>& a, const pair<string, int>& b) {
        if (a.second != b.second) return a.second > b.second;
        return a.first < b.first;
    });
    return vec;
}

// ==============================
// P011 — Email Validator
// ==============================
bool isValidEmail(const string& email) {
    size_t at = email.find('@');
    if (at == string::npos || at != email.rfind('@')) return false;
    string local = email.substr(0, at), domain = email.substr(at + 1);
    if (local.empty() || local.front() == '.' || local.back() == '.' || local.find("..") != string::npos) return false;
    for (char c : local) if (!isalnum(c) && c!='.' && c!='_' && c!='%' && c!='+' && c!='-') return false;
    if (domain.empty()) return false;
    vector<string> dParts;
    stringstream ss(domain);
    string part;
    while (getline(ss, part, '.')) dParts.push_back(part);
    if (dParts.size() < 2) return false;
    string tld = dParts.back();
    if (tld.length() < 2 || tld.length() > 6) return false;
    for (char c : tld) if (!isalpha(c)) return false;
    for (const string& p : dParts) {
        if (p.empty() || p.front() == '-' || p.back() == '-') return false;
        for (char c : p) if (!isalnum(c) && c != '-') return false;
    }
    return true;
}

// ==============================
// P012 — Password Policy Validator
// ==============================
bool isValidPassword(const string& pw) {
    if (pw.length() < 8) return false;
    bool u = false, l = false, d = false, s = false;
    string spec = "!@#$%^&*";
    for (char c : pw) {
        if (isupper(c)) u = true;
        else if (islower(c)) l = true;
        else if (isdigit(c)) d = true;
        else if (spec.find(c) != string::npos) s = true;
    }
    return u && l && d && s;
}

// ==============================
// P013 — Integer Range Validator
// ==============================
string isValidRange(const string& s) {
    int v, mn, mx;
    if (sscanf(s.c_str(), "%d|%d|%d", &v, &mn, &mx) == 3) {
        return (v >= mn && v <= mx) ? "VALID" : "INVALID";
    }
    return "INVALID";
}

// ==============================
// P014 — IPv4 Validator
// ==============================
bool isValidIPv4(const string& ip) {
    stringstream ss(ip);
    string part;
    int count = 0;
    while (getline(ss, part, '.')) {
        count++;
        if (part.empty() || (part.length() > 1 && part[0] == '0')) return false;
        for (char c : part) if (!isdigit(c)) return false;
        try {
            int val = stoi(part);
            if (val < 0 || val > 255) return false;
        } catch (...) { return false; }
    }
    return count == 4 && ip.back() != '.';
}

// ==============================
// P015 — Username Validator
// ==============================
bool isValidUsername(const string& s) {
    if (s.length() < 3 || s.length() > 20 || !isalpha(s[0])) return false;
    for (char c : s) if (!isalnum(c) && c != '_' && c != '-') return false;
    return true;
}

// ==============================
// P016 — HTML Text Escaper
// ==============================
string escapeHtml(const string& s) {
    string res = "";
    for (char c : s) {
        if (c == '&') res += "&amp;";
        else if (c == '<') res += "&lt;";
        else if (c == '>') res += "&gt;";
        else if (c == '"') res += "&quot;";
        else if (c == '\'') res += "&#39;";
        else res += c;
    }
    return res;
}

// ==============================
// P017 — CSV Cell Escaper
// ==============================
string escapeCsvCell(const string& s) {
    bool needQuote = false;
    for (char c : s) if (c == ',' || c == '"' || c == '\n' || c == '\r') { needQuote = true; break; }
    if (!needQuote) return s;
    string res = "\"";
    for (char c : s) {
        if (c == '"') res += "\"\"";
        else res += c;
    }
    res += "\"";
    return res;
}

// ==============================
// P018 — JSON String Escaper
// ==============================
string escapeJsonString(const string& s) {
    string res = "";
    for (char c : s) {
        unsigned char uc = (unsigned char)c;
        if (c == '"') res += "\\\"";
        else if (c == '\\') res += "\\\\";
        else if (c == '/') res += "\\/";
        else if (c == '\b') res += "\\b";
        else if (c == '\f') res += "\\f";
        else if (c == '\n') res += "\\n";
        else if (c == '\r') res += "\\r";
        else if (c == '\t') res += "\\t";
        else if (uc < 32) {
            char buf[8];
            snprintf(buf, sizeof(buf), "\\u%04x", uc);
            res += buf;
        } else res += c;
    }
    return res;
}

// ==============================
// P019 — URL Query Component Encoder
// ==============================
string encodeUrlComponent(const string& s) {
    string unreserved = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~";
    string res = "";
    for (char c : s) {
        if (unreserved.find(c) != string::npos) res += c;
        else {
            char buf[4];
            snprintf(buf, sizeof(buf), "%%%02X", (unsigned char)c);
            res += buf;
        }
    }
    return res;
}

// ==============================
// P020 — Template Placeholder Sanitizer
// ==============================
string sanitizeTemplate(const string& s) {
    string res = "";
    size_t i = 0;
    while (i < s.length()) {
        if (i + 1 < s.length() && s[i] == '{' && s[i+1] == '{') {
            size_t close = s.find("}}", i + 2);
            if (close != string::npos) {
                string key = s.substr(i + 2, close - (i + 2));
                bool valid = !key.empty();
                for (char c : key) if (!isalnum(c) && c != '_') { valid = false; break; }
                if (valid) res += s.substr(i, close + 2 - i);
                i = close + 2;
                continue;
            }
        }
        res += s[i++];
    }
    return res;
}

// ==============================
// P021 — Safe Path Normalizer
// ==============================
string safePathNormalize(const string& path) {
    if (path.empty() || path.find('\\') != string::npos) return "";
    stringstream ss(path);
    string part;
    vector<string> st;
    while (getline(ss, part, '/')) {
        if (part.empty() || part == ".") continue;
        if (part == "..") {
            if (st.empty()) return "";
            st.pop_back();
        } else st.push_back(part);
    }
    string res = "";
    for (size_t i = 0; i < st.size(); i++) {
        if (i > 0) res += "/";
        res += st[i];
    }
    return res;
}

// ==============================
// P022 — Path Extension Validator
// ==============================
bool isAllowedExtension(const string& path) {
    set<string> allowed = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".csv"};
    string fn = path;
    size_t slash = fn.find_last_of("/\\");
    if (slash != string::npos) fn = fn.substr(slash + 1);
    if (fn.empty()) return false;
    size_t dot = fn.find_last_of('.');
    if (dot == string::npos || dot == 0) return false;
    string ext = fn.substr(dot);
    for (char& c : ext) c = tolower(c);
    return allowed.count(ext) > 0;
}

// ==============================
// P023 — Filename Sanitizer
// ==============================
string sanitizeFilename(const string& name) {
    string s = name.substr(0, min((size_t)200, name.length()));
    for (char& c : s) if (!isalnum(c) && c != '.' && c != '_' && c != '-') c = '_';
    string collapsed = "";
    for (char c : s) {
        if (c == '_' && !collapsed.empty() && collapsed.back() == '_') continue;
        collapsed += c;
    }
    while (!collapsed.empty() && collapsed.front() == '_') collapsed.erase(0, 1);
    while (!collapsed.empty() && collapsed.back() == '_') collapsed.pop_back();
    return collapsed.empty() ? "_" : collapsed;
}

// ==============================
// P024 — Archive Entry Path Checker
// ==============================
string checkArchiveEntry(const string& path) {
    if (path.empty()) return "safe";
    if (path.front() == '/' || path.find('\\') != string::npos) return "unsafe";
    stringstream ss(path);
    string part;
    int depth = 0;
    while (getline(ss, part, '/')) {
        if (part.empty() || part == ".") continue;
        if (part == "..") {
            depth--;
            if (depth < 0) return "unsafe";
        } else depth++;
    }
    return "safe";
}

// ==============================
// P025 — File Type Allowlist
// ==============================
bool isAllowedFiletype(const string& ext) {
    set<string> allowed = {"jpg", "jpeg", "png", "gif", "bmp", "pdf", "txt", "csv", "json", "xml"};
    string clean = ext;
    clean.erase(0, clean.find_first_not_of(" \t\r\n"));
    clean.erase(clean.find_last_not_of(" \t\r\n") + 1);
    if (!clean.empty() && clean.front() == '.') clean.erase(0, 1);
    for (char& c : clean) c = tolower(c);
    return !clean.empty() && allowed.count(clean) > 0;
}

// ==============================
// P026 — SQL Identifier Validator
// ==============================
bool isValidSqlIdentifier(const string& name) {
    if (name.empty() || name.length() > 64) return false;
    if (!isalpha(name[0]) && name[0] != '_') return false;
    for (char c : name) if (!isalnum(c) && c != '_') return false;
    return true;
}

// ==============================
// P027 — SQL String Literal Escaper
// ==============================
string escapeSqlString(const string& s) {
    string res = "";
    for (char c : s) {
        if (c == '\\') res += "\\\\";
        else if (c == '\'') res += "''";
        else res += c;
    }
    return res;
}

// ==============================
// P028 — Parameterized Query Builder
// ==============================
string buildParamQuery(const string& s) {
    size_t bar = s.find('|');
    if (bar == string::npos || bar != s.rfind('|')) return "INVALID";
    string table = s.substr(0, bar), conds = s.substr(bar + 1);
    auto checkIdent = [](const string& id) {
        if (id.empty()) return false;
        if (!isalpha(id[0]) && id[0] != '_') return false;
        for (char c : id) if (!isalnum(c) && c != '_') return false;
        return true;
    };
    if (!checkIdent(table) || conds.empty()) return "INVALID";
    stringstream ss(conds);
    string pair;
    vector<string> cols;
    while (getline(ss, pair, ',')) {
        size_t eq = pair.find('=');
        if (eq == string::npos) return "INVALID";
        string col = pair.substr(0, eq);
        if (!checkIdent(col)) return "INVALID";
        cols.push_back(col + "=\\?");
    }
    string res = "SELECT * FROM " + table + " WHERE ";
    for (size_t i = 0; i < cols.size(); i++) {
        if (i > 0) res += " AND ";
        res += cols[i].substr(0, cols[i].length() - 1); // remove escape
    }
    return res;
}

// ==============================
// P029 — Sort Direction Validator
// ==============================
string validateSortDirection(const string& s) {
    string clean = s;
    clean.erase(0, clean.find_first_not_of(" \t\r\n"));
    clean.erase(clean.find_last_not_of(" \t\r\n") + 1);
    for (char& c : clean) c = toupper(c);
    return (clean == "ASC" || clean == "DESC") ? clean : "INVALID";
}

// ==============================
// P030 — Column Allowlist Checker
// ==============================
bool isAllowedColumn(const string& col) {
    set<string> allowed = {"id", "name", "email", "created_at", "status", "age", "role", "score"};
    string clean = col;
    clean.erase(0, clean.find_first_not_of(" \t\r\n"));
    clean.erase(clean.find_last_not_of(" \t\r\n") + 1);
    return allowed.count(clean) > 0;
}

// ==============================
// P031 — Shell Argument Quoter
// ==============================
string quoteShellArg(const string& s) {
    string res = "'";
    for (char c : s) {
        if (c == '\'') res += "'\\''";
        else res += c;
    }
    res += "'";
    return res;
}

// ==============================
// P032 — Command Name Allowlist
// ==============================
bool isAllowedCommand(const string& s) {
    set<string> allowed = {"ls", "cat", "echo", "grep", "find", "sort", "uniq", "wc", "head", "tail"};
    string clean = s;
    clean.erase(0, clean.find_first_not_of(" \t\r\n"));
    clean.erase(clean.find_last_not_of(" \t\r\n") + 1);
    if (clean.find(' ') != string::npos) return false;
    return allowed.count(clean) > 0;
}

// ==============================
// P033 — Shell Metacharacter Detector
// ==============================
string detectShellMeta(const string& s) {
    string dangerous = ";|&$`><(){} \\\"'\n\r";
    for (char c : s) if (dangerous.find(c) != string::npos) return "unsafe";
    return "safe";
}

// ==============================
// P034 — Environment Variable Name Validator
// ==============================
bool isValidEnvVar(const string& name) {
    if (name.length() < 1 || name.length() > 64) return false;
    if (!isupper(name[0]) && name[0] != '_') return false;
    for (char c : name) if (!isupper(c) && !isdigit(c) && c != '_') return false;
    return true;
}

// ==============================
// P035 — Command Argument Splitter
// ==============================
vector<string> splitArgs(const string& s) {
    vector<string> res;
    string curr = "";
    bool inQuotes = false;
    for (size_t i = 0; i < s.length(); i++) {
        char c = s[i];
        if (c == '"') inQuotes = !inQuotes;
        else if (c == ' ' && !inQuotes) {
            if (!curr.empty() || (i > 0 && s[i-1] == '"')) {
                res.push_back(curr);
                curr = "";
            }
        } else curr += c;
    }
    if (!curr.empty() || (!s.empty() && s.back() == '"')) res.push_back(curr);
    return res;
}

// ==============================
// P036 — Safe Literal Parser
// ==============================
string parseSafeLiteral(const string& s) {
    if (s == "null" || s == "true" || s == "false") return s;
    bool isInt = true;
    size_t start = (s.length() > 0 && s[0] == '-') ? 1 : 0;
    if (start >= s.length()) isInt = false;
    else if (s[start] == '0' && s.length() > start + 1) isInt = false;
    else {
        for (size_t i = start; i < s.length(); i++) if (!isdigit(s[i])) { isInt = false; break; }
    }
    if (isInt) return s;
    if (s.length() >= 2 && s.front() == '"' && s.back() == '"') {
        string inner = s.substr(1, s.length() - 2);
        string res = "";
        size_t i = 0;
        while (i < inner.length()) {
            if (inner[i] == '\\') {
                if (i + 1 < inner.length() && inner[i+1] == '"') {
                    res += '"';
                    i += 2;
                } else return "INVALID";
            } else if (inner[i] == '"') return "INVALID";
            else res += inner[i++];
        }
        return res;
    }
    return "INVALID";
}

// ==============================
// P037 — Configuration Boolean Parser
// ==============================
string parseConfigBool(const string& s) {
    string clean = s;
    clean.erase(0, clean.find_first_not_of(" \t\r\n"));
    clean.erase(clean.find_last_not_of(" \t\r\n") + 1);
    for (char& c : clean) c = tolower(c);
    set<string> t = {"true", "yes", "1", "on", "enabled"};
    set<string> f = {"false", "no", "0", "off", "disabled"};
    if (t.count(clean)) return "true";
    if (f.count(clean)) return "false";
    return "INVALID";
}

// ==============================
// P038 — Configuration Key Allowlist
// ==============================
bool isAllowedConfigKey(const string& key) {
    set<string> allowed = {"host", "port", "database", "username", "password", "timeout", "max_connections", "ssl_enabled", "log_level", "retry_count"};
    string clean = key;
    clean.erase(0, clean.find_first_not_of(" \t\r\n"));
    clean.erase(clean.find_last_not_of(" \t\r\n") + 1);
    return allowed.count(clean) > 0;
}

// ==============================
// P039 — Structured Token Decoder
// ==============================
string validateToken(const string& s) {
    vector<string> p;
    stringstream ss(s);
    string part;
    while (getline(ss, part, '.')) p.push_back(part);
    if (p.size() != 3) return "invalid";
    auto b64 = [](const string& str) {
        if (str.empty()) return false;
        for (char c : str) if (!isalnum(c) && c != '_' && c != '-') return false;
        return true;
    };
    if (!b64(p[0]) || !b64(p[1]) || p[2].length() != 8) return "invalid";
    for (char c : p[2]) if (!isdigit(c) && (c < 'a' || c > 'f')) return "invalid";
    return "valid";
}

// ==============================
// P040 — Safe Numeric Expression Validator
// ==============================
string validateNumericExpr(const string& s) {
    vector<string> tokens;
    string curr = "";
    for (char c : s) {
        if (c == '+' || c == '-' || c == '*' || c == '/') {
            if (!curr.empty()) { tokens.push_back(curr); curr = ""; }
            tokens.push_back(string(1, c));
        } else if (isspace(c)) {
            if (!curr.empty()) { tokens.push_back(curr); curr = ""; }
        } else curr += c;
    }
    if (!curr.empty()) tokens.push_back(curr);
    if (tokens.empty()) return "invalid";
    bool expectNum = true;
    for (const string& t : tokens) {
        if (expectNum) {
            size_t st = (t[0] == '-') ? 1 : 0;
            if (st >= t.length()) return "invalid";
            if (t[st] == '0' && t.length() > st + 1) return "invalid";
            for (size_t i = st; i < t.length(); i++) if (!isdigit(t[i])) return "invalid";
            expectNum = false;
        } else {
            if (t != "+" && t != "-" && t != "*" && t != "/") return "invalid";
            expectNum = true;
        }
    }
    return expectNum ? "invalid" : "valid";
}

// ==============================
// P041 — Frequency Counter Large Input
// ==============================
map<int, int> frequencyCounter(vector<int>& nums) {
    map<int, int> counts;
    for (int x : nums) counts[x]++;
    return counts;
}

// ==============================
// P042 — Duplicate Detector
// ==============================
bool hasDuplicate(vector<int>& nums) {
    unordered_set<int> st;
    for (int x : nums) {
        if (st.count(x)) return true;
        st.insert(x);
    }
    return false;
}

// ==============================
// P043 — Streaming Sum
// ==============================
long long streamingSum(vector<int>& nums) {
    long long sum = 0;
    for (int x : nums) sum += x;
    return sum;
}

// ==============================
// P044 — Bounded Log Processor
// ==============================
map<string, int> boundedLogProcessor(const string& log, int maxLines) {
    map<string, int> res = {{"kept", 0}, {"total_words", 0}};
    if (log.empty() || maxLines <= 0) return res;
    stringstream ss(log);
    string line;
    int kept = 0, words = 0;
    while (getline(ss, line)) {
        size_t st = line.find_first_not_of(" \t\r\n");
        if (st != string::npos) {
            kept++;
            stringstream lss(line);
            string w;
            while (lss >> w) words++;
            if (kept == maxLines) break;
        }
    }
    res["kept"] = kept;
    res["total_words"] = words;
    return res;
}

// ==============================
// P045 — Top-K Frequent Values
// ==============================
vector<int> topKFrequent(vector<int>& nums, int k) {
    if (nums.empty() || k <= 0) return {};
    unordered_map<int, int> counts;
    for (int x : nums) counts[x]++;
    vector<pair<int, int>> vec;
    for (auto& p : counts) vec.push_back({p.first, p.second});
    sort(vec.begin(), vec.end(), [](const pair<int, int>& a, const pair<int, int>& b) {
        if (a.second != b.second) return a.second > b.second;
        return a.first < b.first;
    });
    vector<int> res;
    for (int i = 0; i < min((int)k, (int)vec.size()); i++) res.push_back(vec[i].first);
    sort(res.begin(), res.end());
    return res;
}

// ==============================
// P046 — Token Format Validator
// ==============================
string validateTokenFormat(const string& token) {
    if (token.length() < 8 || token.length() > 32 || !isalpha(token[0])) return "invalid";
    for (char c : token) if (!isalnum(c) && c != '-') return "invalid";
    return "valid";
}

// ==============================
// P047 — Permission Rule Evaluator
// ==============================
string evaluatePermission(const string& role, const string& action) {
    map<string, set<string>> perms = {
        {"admin", {"read", "write", "delete", "execute"}},
        {"editor", {"read", "write"}},
        {"viewer", {"read"}},
        {"guest", {}}
    };
    return (perms.count(role) && perms[role].count(action)) ? "allowed" : "denied";
}

// ==============================
// P048 — Role Permission Checker
// ==============================
bool roleHasPermission(const string& role, const string& permission) {
    return evaluatePermission(role, permission) == "allowed";
}

// ==============================
// P049 — Session Timeout Checker
// ==============================
string checkSession(int lastActive, int currentTime, int timeout) {
    if (currentTime < lastActive) return "invalid";
    return (currentTime - lastActive > timeout) ? "expired" : "active";
}

// ==============================
// P050 — Access Scope Validator
// ==============================
string validateScope(const string& requested, vector<string>& allowed) {
    set<string> st(allowed.begin(), allowed.end());
    if (st.count(requested)) return "granted";
    string curr = "";
    stringstream ss(requested);
    string part;
    vector<string> parts;
    while (getline(ss, part, ':')) parts.push_back(part);
    for (size_t i = 0; i < parts.size() - 1; i++) {
        if (i > 0) curr += ":";
        curr += parts[i];
        if (st.count(curr)) return "granted";
    }
    return "denied";
}
