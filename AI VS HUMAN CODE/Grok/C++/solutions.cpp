P001
#include <vector>
#include <unordered_map>
using namespace std;
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> seen;
    for (int i = 0; i < (int)nums.size(); i++) {
        int need = target - nums[i];
        if (seen.count(need)) {
            int a = seen[need], b = i;
            return a < b ? vector<int>{a, b} : vector<int>{b, a};
        }
        seen[nums[i]] = i;
    }
    return {};
}

P002
#include <vector>
#include <algorithm>
using namespace std;
int maxSubarray(vector<int>& nums) {
    int best = nums[0], cur = nums[0];
    for (size_t i = 1; i < nums.size(); i++) {
        cur = max(nums[i], cur + nums[i]);
        best = max(best, cur);
    }
    return best;
}

P003
#include <vector>
using namespace std;
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

P004
#include <vector>
using namespace std;
vector<int> mergeSortedArrays(vector<int>& nums1, vector<int>& nums2) {
    vector<int> out;
    size_t i = 0, j = 0;
    while (i < nums1.size() && j < nums2.size()) {
        if (nums1[i] <= nums2[j]) out.push_back(nums1[i++]);
        else out.push_back(nums2[j++]);
    }
    while (i < nums1.size()) out.push_back(nums1[i++]);
    while (j < nums2.size()) out.push_back(nums2[j++]);
    return out;
}

P005
#include <string>
#include <stack>
using namespace std;
bool isBalanced(const string& s) {
    stack<char> st;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') st.push(c);
        else if (c == ')' || c == ']' || c == '}') {
            if (st.empty()) return false;
            char t = st.top(); st.pop();
            if ((c == ')' && t != '(') || (c == ']' && t != '[') || (c == '}' && t != '{')) return false;
        }
    }
    return st.empty();
}

P006
#include <string>
using namespace std;
int csvFieldCount(const string& line) {
    if (line.empty()) return 0;
    int count = 1;
    size_t i = 0, n = line.size();
    while (i < n) {
        if (line[i] == '"') {
            i++;
            while (i < n) {
                if (line[i] == '"') {
                    if (i + 1 < n && line[i + 1] == '"') i += 2;
                    else { i++; break; }
                } else i++;
            }
        } else if (line[i] == ',') {
            count++;
            i++;
        } else i++;
    }
    return count;
}

P007
#include <string>
#include <map>
#include <sstream>
using namespace std;
map<string, int> countLogLevels(const string& log) {
    map<string, int> counts{{"ERROR", 0}, {"WARNING", 0}, {"INFO", 0}, {"DEBUG", 0}};
    istringstream iss(log);
    string line;
    while (getline(iss, line)) {
        size_t start = line.find_first_not_of(" \t");
        if (start == string::npos) continue;
        line = line.substr(start);
        for (const string& level : {"ERROR", "WARNING", "INFO", "DEBUG"}) {
            if (line.compare(0, level.size(), level) == 0 &&
                (line.size() == level.size() || line[level.size()] == ' ' || line[level.size()] == ':')) {
                counts[level]++;
                break;
            }
        }
    }
    return counts;
}

P008
#include <string>
#include <map>
#include <sstream>
using namespace std;
map<string, string> parseKeyValue(const string& s) {
    map<string, string> result;
    if (s.empty()) return result;
    istringstream iss(s);
    string part;
    while (getline(iss, part, ',')) {
        size_t eq = part.find('=');
        if (eq == string::npos) continue;
        string k = part.substr(0, eq);
        string v = part.substr(eq + 1);
        auto trim = [](string& x) {
            size_t a = x.find_first_not_of(" \t");
            size_t b = x.find_last_not_of(" \t");
            if (a == string::npos) x.clear();
            else x = x.substr(a, b - a + 1);
        };
        trim(k); trim(v);
        if (!k.empty()) result[k] = v;
    }
    return result;
}

P009
#include <string>
#include <sstream>
#include <iomanip>
using namespace std;
string normalizeDate(const string& date) {
    int y, m, d;
    char sep;
    if (date.find('/') != string::npos) {
        sscanf(date.c_str(), "%d/%d/%d", &m, &d, &y);
    } else if (date.find('-') != string::npos) {
        sscanf(date.c_str(), "%d-%d-%d", &d, &m, &y);
    } else {
        sscanf(date.c_str(), "%d.%d.%d", &y, &m, &d);
    }
    ostringstream oss;
    oss << y << '-' << setfill('0') << setw(2) << m << '-' << setw(2) << d;
    return oss.str();
}

P010
#include <string>
#include <vector>
#include <map>
#include <cctype>
#include <algorithm>
using namespace std;
vector<pair<string, int>> wordFrequency(const string& text) {
    map<string, int> freq;
    string word;
    for (char c : text) {
        if (isalpha(static_cast<unsigned char>(c))) {
            word += tolower(static_cast<unsigned char>(c));
        } else {
            if (!word.empty()) {
                freq[word]++;
                word.clear();
            }
        }
    }
    if (!word.empty()) freq[word]++;
    vector<pair<string, int>> res(freq.begin(), freq.end());
    sort(res.begin(), res.end(), [](const auto& a, const auto& b) {
        if (a.second != b.second) return a.second > b.second;
        return a.first < b.first;
    });
    return res;
}

P011
#include <string>
#include <regex>
using namespace std;
bool isValidEmail(const string& email) {
    size_t at = email.find('@');
    if (at == string::npos || at == 0 || email.find('@', at + 1) != string::npos) return false;
    string local = email.substr(0, at);
    string domain = email.substr(at + 1);
    if (local.empty() || domain.empty()) return false;
    if (!regex_match(local, regex("[a-zA-Z0-9._%+-]+"))) return false;
    if (local.front() == '.' || local.back() == '.' || local.find("..") != string::npos) return false;
    size_t pos = 0;
    vector<string> labels;
    while (pos < domain.size()) {
        size_t next = domain.find('.', pos);
        if (next == string::npos) next = domain.size();
        labels.push_back(domain.substr(pos, next - pos));
        pos = next + 1;
    }
    if (labels.size() < 2) return false;
    for (const string& lab : labels) {
        if (lab.empty() || lab.front() == '-' || lab.back() == '-') return false;
        if (!regex_match(lab, regex("[a-zA-Z0-9-]+"))) return false;
    }
    const string& tld = labels.back();
    return tld.size() >= 2 && tld.size() <= 6 && regex_match(tld, regex("[a-zA-Z]+"));
}

P012
#include <string>
#include <cctype>
using namespace std;
bool isValidPassword(const string& pw) {
    if (pw.size() < 8) return false;
    bool up = false, lo = false, dig = false, spe = false;
    string specials = "!@#$%^&*";
    for (char c : pw) {
        if (isupper(static_cast<unsigned char>(c))) up = true;
        else if (islower(static_cast<unsigned char>(c))) lo = true;
        else if (isdigit(static_cast<unsigned char>(c))) dig = true;
        else if (specials.find(c) != string::npos) spe = true;
    }
    return up && lo && dig && spe;
}

P013
#include <string>
#include <sstream>
using namespace std;
string isValidRange(const string& s) {
    istringstream iss(s);
    string p1, p2, p3;
    if (!getline(iss, p1, '|') || !getline(iss, p2, '|') || !getline(iss, p3, '|')) return "INVALID";
    string extra;
    if (getline(iss, extra, '|')) return "INVALID";
    try {
        int value = stoi(p1);
        int mn = stoi(p2);
        int mx = stoi(p3);
        return (mn <= value && value <= mx) ? "VALID" : "INVALID";
    } catch (...) {
        return "INVALID";
    }
}

P014
#include <string>
#include <sstream>
using namespace std;
bool isValidIPv4(const string& ip) {
    istringstream iss(ip);
    string part;
    int count = 0;
    while (getline(iss, part, '.')) {
        count++;
        if (part.empty() || part.find_first_not_of("0123456789") != string::npos) return false;
        if (part.size() > 1 && part[0] == '0') return false;
        try {
            int n = stoi(part);
            if (n < 0 || n > 255) return false;
        } catch (...) {
            return false;
        }
    }
    return count == 4;
}

P015
#include <string>
#include <cctype>
using namespace std;
bool isValidUsername(const string& s) {
    if (s.size() < 3 || s.size() > 20) return false;
    if (!isalpha(static_cast<unsigned char>(s[0]))) return false;
    for (char c : s) {
        if (!isalnum(static_cast<unsigned char>(c)) && c != '_' && c != '-') return false;
    }
    return true;
}

P016
#include <string>
using namespace std;
string escapeHtml(const string& s) {
    string out;
    for (char c : s) {
        if (c == '&') out += "&amp;";
        else if (c == '<') out += "&lt;";
        else if (c == '>') out += "&gt;";
        else if (c == '"') out += "&quot;";
        else if (c == '\'') out += "&#39;";
        else out += c;
    }
    return out;
}

P017
#include <string>
using namespace std;
string escapeCsvCell(const string& s) {
    if (s.find(',') != string::npos || s.find('"') != string::npos ||
        s.find('\n') != string::npos || s.find('\r') != string::npos) {
        string out = "\"";
        for (char c : s) {
            if (c == '"') out += "\"\"";
            else out += c;
        }
        out += "\"";
        return out;
    }
    return s;
}

P018
#include <string>
#include <cstdio>
using namespace std;
string escapeJsonString(const string& s) {
    string out;
    for (unsigned char c : s) {
        if (c == '"') out += "\\\"";
        else if (c == '\\') out += "\\\\";
        else if (c == '/') out += "\\/";
        else if (c == 8) out += "\\b";
        else if (c == 12) out += "\\f";
        else if (c == 10) out += "\\n";
        else if (c == 13) out += "\\r";
        else if (c == 9) out += "\\t";
        else if (c <= 31) {
            char buf[8];
            snprintf(buf, sizeof(buf), "\\u%04x", c);
            out += buf;
        } else out += c;
    }
    return out;
}

P019
#include <string>
using namespace std;
string encodeUrlComponent(const string& s) {
    string out;
    const string unreserved = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~";
    for (unsigned char c : s) {
        if (unreserved.find(c) != string::npos) out += c;
        else {
            char buf[4];
            snprintf(buf, sizeof(buf), "%%%02X", c);
            out += buf;
        }
    }
    return out;
}

P020
#include <string>
#include <regex>
using namespace std;
string sanitizeTemplate(const string& s) {
    regex re(R"(\{\{([^}]*)\}\})");
    string result;
    sregex_iterator it(s.begin(), s.end(), re), end;
    size_t last = 0;
    for (; it != end; ++it) {
        result += s.substr(last, it->position() - last);
        string key = (*it)[1].str();
        if (!key.empty() && regex_match(key, regex("[a-zA-Z0-9_]+"))) {
            result += it->str();
        }
        last = it->position() + it->length();
    }
    result += s.substr(last);
    return result;
}

P021
#include <string>
#include <vector>
#include <sstream>
using namespace std;
string safePathNormalize(const string& path) {
    if (path.empty() || path.find_first_not_of(" \t") == string::npos) return "";
    if (path.find('\\') != string::npos) return "";
    vector<string> stack;
    istringstream iss(path);
    string part;
    while (getline(iss, part, '/')) {
        if (part.empty() || part == ".") continue;
        if (part == "..") {
            if (stack.empty()) return "";
            stack.pop_back();
        } else {
            stack.push_back(part);
        }
    }
    string out;
    for (size_t i = 0; i < stack.size(); i++) {
        if (i) out += '/';
        out += stack[i];
    }
    return out;
}

P022
#include <string>
#include <algorithm>
#include <cctype>
using namespace std;
bool isAllowedExtension(const string& path) {
    string name = path;
    size_t slash = name.find_last_of("/\\");
    if (slash != string::npos) name = name.substr(slash + 1);
    size_t dot = name.find_last_of('.');
    if (dot == string::npos || dot == 0) return false;
    string ext = name.substr(dot);
    transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
    return ext == ".jpg" || ext == ".jpeg" || ext == ".png" || ext == ".gif" ||
           ext == ".pdf" || ext == ".txt" || ext == ".csv";
}

P023
#include <string>
#include <cctype>
using namespace std;
string sanitizeFilename(const string& name) {
    string s = name.substr(0, 200);
    string out;
    for (char c : s) {
        if (isalnum(static_cast<unsigned char>(c)) || c == '.' || c == '_' || c == '-') out += c;
        else out += '_';
    }
    string collapsed;
    for (char c : out) {
        if (c == '_' && !collapsed.empty() && collapsed.back() == '_') continue;
        collapsed += c;
    }
    size_t start = collapsed.find_first_not_of('_');
    size_t end = collapsed.find_last_not_of('_');
    if (start == string::npos) return "_";
    return collapsed.substr(start, end - start + 1);
}

P024
#include <string>
#include <sstream>
using namespace std;
string checkArchiveEntry(const string& path) {
    if (path.empty()) return "safe";
    if (path[0] == '/' || path.find('\\') != string::npos) return "unsafe";
    int depth = 0;
    istringstream iss(path);
    string part;
    while (getline(iss, part, '/')) {
        if (part.empty() || part == ".") continue;
        if (part == "..") {
            depth--;
            if (depth < 0) return "unsafe";
        } else {
            depth++;
        }
    }
    return "safe";
}

P025
#include <string>
#include <algorithm>
#include <cctype>
using namespace std;
bool isAllowedFiletype(const string& ext) {
    string e = ext;
    if (!e.empty() && e[0] == '.') e = e.substr(1);
    transform(e.begin(), e.end(), e.begin(), ::tolower);
    if (e.empty()) return false;
    return e == "jpg" || e == "jpeg" || e == "png" || e == "gif" || e == "bmp" ||
           e == "pdf" || e == "txt" || e == "csv" || e == "json" || e == "xml";
}

P026
#include <string>
#include <regex>
using namespace std;
bool isValidSqlIdentifier(const string& name) {
    return regex_match(name, regex("[a-zA-Z_][a-zA-Z0-9_]{0,63}"));
}

P027
#include <string>
using namespace std;
string escapeSqlString(const string& s) {
    string out;
    for (char c : s) {
        if (c == '\\') out += "\\\\";
        else if (c == '\'') out += "''";
        else out += c;
    }
    return out;
}

P028
#include <string>
#include <sstream>
#include <regex>
using namespace std;
string buildParamQuery(const string& s) {
    size_t pipe = s.find('|');
    if (pipe == string::npos || s.find('|', pipe + 1) != string::npos) return "INVALID";
    string table = s.substr(0, pipe);
    string conds = s.substr(pipe + 1);
    if (!regex_match(table, regex("[a-zA-Z_][a-zA-Z0-9_]*"))) return "INVALID";
    if (conds.find_first_not_of(" \t") == string::npos) return "INVALID";
    string out = "SELECT * FROM " + table + " WHERE ";
    istringstream iss(conds);
    string pair;
    bool first = true;
    while (getline(iss, pair, ',')) {
        size_t eq = pair.find('=');
        if (eq == string::npos) return "INVALID";
        string col = pair.substr(0, eq);
        size_t a = col.find_first_not_of(" \t");
        size_t b = col.find_last_not_of(" \t");
        if (a == string::npos) return "INVALID";
        col = col.substr(a, b - a + 1);
        if (!regex_match(col, regex("[a-zA-Z_][a-zA-Z0-9_]*"))) return "INVALID";
        if (!first) out += " AND ";
        out += col + "=?";
        first = false;
    }
    return out;
}

P029
#include <string>
#include <algorithm>
#include <cctype>
using namespace std;
string validateSortDirection(const string& s) {
    string t = s;
    size_t a = t.find_first_not_of(" \t");
    size_t b = t.find_last_not_of(" \t");
    if (a == string::npos) return "INVALID";
    t = t.substr(a, b - a + 1);
    transform(t.begin(), t.end(), t.begin(), ::toupper);
    if (t == "ASC" || t == "DESC") return t;
    return "INVALID";
}

P030
#include <string>
using namespace std;
bool isAllowedColumn(const string& col) {
    string c = col;
    size_t a = c.find_first_not_of(" \t");
    size_t b = c.find_last_not_of(" \t");
    if (a == string::npos) return false;
    c = c.substr(a, b - a + 1);
    return c == "id" || c == "name" || c == "email" || c == "created_at" ||
           c == "status" || c == "age" || c == "role" || c == "score";
}

P031
#include <string>
using namespace std;
string quoteShellArg(const string& s) {
    string out = "'";
    for (char c : s) {
        if (c == '\'') out += "'\\''";
        else out += c;
    }
    out += "'";
    return out;
}

P032
#include <string>
using namespace std;
bool isAllowedCommand(const string& s) {
    string t = s;
    size_t a = t.find_first_not_of(" \t");
    size_t b = t.find_last_not_of(" \t");
    if (a == string::npos) return false;
    t = t.substr(a, b - a + 1);
    if (t.find(' ') != string::npos) return false;
    return t == "ls" || t == "cat" || t == "echo" || t == "grep" || t == "find" ||
           t == "sort" || t == "uniq" || t == "wc" || t == "head" || t == "tail";
}

P033
#include <string>
using namespace std;
string detectShellMeta(const string& s) {
    string dangerous = ";|&$`><(){}\\\"'\n\r";
    for (char c : s) {
        if (dangerous.find(c) != string::npos) return "unsafe";
    }
    return "safe";
}

P034
#include <string>
#include <regex>
using namespace std;
bool isValidEnvVar(const string& name) {
    return regex_match(name, regex("[A-Z_][A-Z0-9_]{0,63}"));
}

P035
#include <string>
#include <vector>
using namespace std;
vector<string> splitArgs(const string& s) {
    vector<string> tokens;
    if (s.empty()) return tokens;
    size_t i = 0, n = s.size();
    while (i < n) {
        while (i < n && s[i] == ' ') i++;
        if (i >= n) break;
        if (s[i] == '"') {
            i++;
            string buf;
            while (i < n && s[i] != '"') {
                buf += s[i];
                i++;
            }
            if (i < n && s[i] == '"') i++;
            tokens.push_back(buf);
        } else {
            string buf;
            while (i < n && s[i] != ' ') {
                buf += s[i];
                i++;
            }
            tokens.push_back(buf);
        }
    }
    return tokens;
}

P036
#include <string>
#include <cctype>
using namespace std;
string parseSafeLiteral(const string& s) {
    if (s == "true" || s == "false" || s == "null") return s;
    if (s.size() >= 2 && s.front() == '"' && s.back() == '"') {
        string out;
        for (size_t i = 1; i + 1 < s.size(); i++) {
            if (s[i] == '\\' && i + 1 < s.size() - 1 && s[i + 1] == '"') {
                out += '"';
                i++;
            } else if (s[i] == '"') {
                return "INVALID";
            } else {
                out += s[i];
            }
        }
        return out;
    }
    if (s == "0") return "0";
    if (!s.empty() && s[0] == '-') {
        if (s.size() == 1) return "INVALID";
        string rest = s.substr(1);
        if (rest.find_first_not_of("0123456789") != string::npos) return "INVALID";
        if (rest.size() > 1 && rest[0] == '0') return "INVALID";
        return s;
    }
    if (!s.empty() && s.find_first_not_of("0123456789") == string::npos) {
        if (s.size() > 1 && s[0] == '0') return "INVALID";
        return s;
    }
    return "INVALID";
}

P037
#include <string>
#include <algorithm>
#include <cctype>
using namespace std;
string parseConfigBool(const string& s) {
    string t = s;
    size_t a = t.find_first_not_of(" \t");
    size_t b = t.find_last_not_of(" \t");
    if (a == string::npos) return "INVALID";
    t = t.substr(a, b - a + 1);
    transform(t.begin(), t.end(), t.begin(), ::tolower);
    if (t == "true" || t == "yes" || t == "1" || t == "on" || t == "enabled") return "true";
    if (t == "false" || t == "no" || t == "0" || t == "off" || t == "disabled") return "false";
    return "INVALID";
}

P038
#include <string>
using namespace std;
bool isAllowedConfigKey(const string& key) {
    string k = key;
    size_t a = k.find_first_not_of(" \t");
    size_t b = k.find_last_not_of(" \t");
    if (a == string::npos) return false;
    k = k.substr(a, b - a + 1);
    return k == "host" || k == "port" || k == "database" || k == "username" ||
           k == "password" || k == "timeout" || k == "max_connections" ||
           k == "ssl_enabled" || k == "log_level" || k == "retry_count";
}

P039
#include <string>
#include <regex>
using namespace std;
string validateToken(const string& s) {
    size_t p1 = s.find('.');
    if (p1 == string::npos) return "invalid";
    size_t p2 = s.find('.', p1 + 1);
    if (p2 == string::npos || s.find('.', p2 + 1) != string::npos) return "invalid";
    string header = s.substr(0, p1);
    string payload = s.substr(p1 + 1, p2 - p1 - 1);
    string checksum = s.substr(p2 + 1);
    if (!regex_match(header, regex("[A-Za-z0-9_-]+"))) return "invalid";
    if (!regex_match(payload, regex("[A-Za-z0-9_-]+"))) return "invalid";
    if (!regex_match(checksum, regex("[0-9a-f]{8}"))) return "invalid";
    return "valid";
}

P040
#include <string>
#include <regex>
using namespace std;
string validateNumericExpr(const string& s) {
    string t = s;
    size_t a = t.find_first_not_of(" \t");
    size_t b = t.find_last_not_of(" \t");
    if (a == string::npos) return "invalid";
    t = t.substr(a, b - a + 1);
    string num = R"((?:-?(?:0|[1-9]\d*)))";
    string op = R"([+\-*/])";
    string pattern = "^" + num + "(?:\\s*" + op + "\\s*" + num + ")*$";
    if (regex_match(t, regex(pattern))) return "valid";
    return "invalid";
}

P041
#include <vector>
#include <map>
using namespace std;
map<int, int> frequencyCounter(vector<int>& nums) {
    map<int, int> m;
    for (int n : nums) m[n]++;
    return m;
}

P042
#include <vector>
#include <unordered_set>
using namespace std;
bool hasDuplicate(vector<int>& nums) {
    unordered_set<int> seen;
    for (int n : nums) {
        if (!seen.insert(n).second) return true;
    }
    return false;
}

P043
#include <vector>
using namespace std;
long long streamingSum(vector<int>& nums) {
    long long sum = 0;
    for (int n : nums) sum += n;
    return sum;
}

P044
#include <string>
#include <map>
#include <sstream>
using namespace std;
map<string, int> boundedLogProcessor(const string& log, int maxLines) {
    map<string, int> res{{"kept", 0}, {"total_words", 0}};
    if (maxLines <= 0) return res;
    istringstream iss(log);
    string line;
    int kept = 0, totalWords = 0;
    while (getline(iss, line)) {
        if (line.find_first_not_of(" \t") == string::npos) continue;
        if (kept >= maxLines) break;
        kept++;
        istringstream wiss(line);
        string w;
        while (wiss >> w) totalWords++;
    }
    res["kept"] = kept;
    res["total_words"] = totalWords;
    return res;
}

P045
#include <vector>
#include <map>
#include <algorithm>
using namespace std;
vector<int> topKFrequent(vector<int>& nums, int k) {
    if (k <= 0 || nums.empty()) return {};
    map<int, int> freq;
    for (int n : nums) freq[n]++;
    vector<pair<int, int>> items(freq.begin(), freq.end());
    sort(items.begin(), items.end(), [](const auto& a, const auto& b) {
        if (a.second != b.second) return a.second > b.second;
        return a.first < b.first;
    });
    int take = min(k, (int)items.size());
    vector<int> selected;
    for (int i = 0; i < take; i++) selected.push_back(items[i].first);
    sort(selected.begin(), selected.end());
    return selected;
}

P046
#include <string>
#include <regex>
using namespace std;
string validateTokenFormat(const string& token) {
    if (regex_match(token, regex("[a-zA-Z][a-zA-Z0-9\\-]{7,31}"))) return "valid";
    return "invalid";
}

P047
#include <string>
#include <unordered_map>
#include <unordered_set>
using namespace std;
string evaluatePermission(const string& role, const string& action) {
    static unordered_map<string, unordered_set<string>> perms = {
        {"admin", {"read", "write", "delete", "execute"}},
        {"editor", {"read", "write"}},
        {"viewer", {"read"}},
        {"guest", {}}
    };
    auto it = perms.find(role);
    if (it != perms.end() && it->second.count(action)) return "allowed";
    return "denied";
}

P048
#include <string>
#include <unordered_map>
#include <unordered_set>
using namespace std;
bool roleHasPermission(const string& role, const string& permission) {
    static unordered_map<string, unordered_set<string>> perms = {
        {"admin", {"read", "write", "delete", "execute"}},
        {"editor", {"read", "write"}},
        {"viewer", {"read"}},
        {"guest", {}}
    };
    auto it = perms.find(role);
    return it != perms.end() && it->second.count(permission);
}

P049
#include <string>
using namespace std;
string checkSession(int lastActive, int currentTime, int timeout) {
    if (currentTime < lastActive) return "invalid";
    int elapsed = currentTime - lastActive;
    if (elapsed > timeout) return "expired";
    return "active";
}

P050
#include <string>
#include <vector>
using namespace std;
string validateScope(const string& requested, vector<string>& allowed) {
    if (allowed.empty()) return "denied";
    for (const string& a : allowed) {
        if (a == requested) return "granted";
    }
    string prefix;
    size_t pos = 0;
    while ((pos = requested.find(':', pos)) != string::npos) {
        prefix = requested.substr(0, pos);
        for (const string& a : allowed) {
            if (a == prefix) return "granted";
        }
        pos++;
    }
    return "denied";
}