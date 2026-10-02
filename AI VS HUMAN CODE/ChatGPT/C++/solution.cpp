#include <algorithm>
#include <cctype>
#include <iomanip>
#include <map>
#include <regex>
#include <set>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using namespace std;

// P001
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> seen;
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
        int complement = target - nums[i];
        auto it = seen.find(complement);
        if (it != seen.end()) {
            vector<int> result{it->second, i};
            sort(result.begin(), result.end());
            return result;
        }
        seen[nums[i]] = i;
    }
    return {};
}

// P002
int maxSubarray(vector<int>& nums) {
    int current = nums[0];
    int best = nums[0];
    for (size_t i = 1; i < nums.size(); ++i) {
        current = max(nums[i], current + nums[i]);
        best = max(best, current);
    }
    return best;
}

// P003
int binarySearch(vector<int>& nums, int target) {
    int left = 0, right = static_cast<int>(nums.size()) - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

// P004
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

// P005
bool isBalanced(const string& s) {
    vector<char> stack;
    for (char ch : s) {
        if (ch == '(' || ch == '[' || ch == '{') {
            stack.push_back(ch);
        } else {
            if (stack.empty()) return false;
            char open = stack.back();
            stack.pop_back();
            if ((ch == ')' && open != '(') ||
                (ch == ']' && open != '[') ||
                (ch == '}' && open != '{')) return false;
        }
    }
    return stack.empty();
}

// P006
int csvFieldCount(const string& line) {
    if (line.empty()) return 1;
    int count = 1;
    bool inQuotes = false;
    for (size_t i = 0; i < line.size(); ++i) {
        if (line[i] == '"') {
            if (inQuotes && i + 1 < line.size() && line[i + 1] == '"') {
                ++i;
            } else {
                inQuotes = !inQuotes;
            }
        } else if (line[i] == ',' && !inQuotes) {
            ++count;
        }
    }
    return count;
}

// P007
map<string, int> countLogLevels(const string& log) {
    map<string, int> counts{{"DEBUG", 0}, {"ERROR", 0}, {"INFO", 0}, {"WARNING", 0}};
    istringstream stream(log);
    string line;
    while (getline(stream, line)) {
        for (const string& level : {"ERROR", "WARNING", "INFO", "DEBUG"}) {
            if (line.rfind(level, 0) == 0 && line.size() > level.size() &&
                (line[level.size()] == ' ' || line[level.size()] == ':')) {
                ++counts[level];
                break;
            }
        }
    }
    return counts;
}

// P008
map<string, string> parseKeyValue(const string& s) {
    map<string, string> result;
    if (s.empty()) return result;
    size_t start = 0;
    while (start <= s.size()) {
        size_t comma = s.find(',', start);
        string pair = s.substr(start, comma == string::npos ? string::npos : comma - start);
        size_t eq = pair.find('=');
        string key = pair.substr(0, eq);
        string value = pair.substr(eq + 1);
        auto trim = [](string value) {
            size_t first = value.find_first_not_of(" \t\r\n");
            if (first == string::npos) return string();
            size_t last = value.find_last_not_of(" \t\r\n");
            return value.substr(first, last - first + 1);
        };
        result[trim(key)] = trim(value);
        if (comma == string::npos) break;
        start = comma + 1;
    }
    return result;
}

// P009
string normalizeDate(const string& date) {
    char delimiter = date.find('/') != string::npos ? '/' :
                     (date.find('-') != string::npos ? '-' : '.');
    vector<string> parts;
    size_t start = 0;
    while (true) {
        size_t pos = date.find(delimiter, start);
        if (pos == string::npos) {
            parts.push_back(date.substr(start));
            break;
        }
        parts.push_back(date.substr(start, pos - start));
        start = pos + 1;
    }
    int year, month, day;
    if (delimiter == '/') {
        month = stoi(parts[0]); day = stoi(parts[1]); year = stoi(parts[2]);
    } else if (delimiter == '-') {
        day = stoi(parts[0]); month = stoi(parts[1]); year = stoi(parts[2]);
    } else {
        year = stoi(parts[0]); month = stoi(parts[1]); day = stoi(parts[2]);
    }
    ostringstream out;
    out << setfill('0') << setw(4) << year << '-' << setw(2) << month << '-' << setw(2) << day;
    return out.str();
}

// P010
vector<pair<string, int>> wordFrequency(const string& text) {
    map<string, int> counts;
    string current;
    for (char ch : text) {
        if ((ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z')) {
            current += static_cast<char>(tolower(static_cast<unsigned char>(ch)));
        } else if (!current.empty()) {
            ++counts[current];
            current.clear();
        }
    }
    if (!current.empty()) ++counts[current];
    vector<pair<string, int>> result(counts.begin(), counts.end());
    sort(result.begin(), result.end(), [](const auto& a, const auto& b) {
        if (a.second != b.second) return a.second > b.second;
        return a.first < b.first;
    });
    return result;
}

// P011
bool isValidEmail(const string& email) {
    size_t at = email.find('@');
    if (at == string::npos || at != email.rfind('@')) return false;
    string local = email.substr(0, at);
    string domain = email.substr(at + 1);
    if (local.empty() || domain.empty() || local.front() == '.' || local.back() == '.' ||
        local.find("..") != string::npos) return false;
    for (char ch : local) {
        bool ok = (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z') ||
                  (ch >= '0' && ch <= '9') || string("._%+-").find(ch) != string::npos;
        if (!ok) return false;
    }
    vector<string> labels;
    size_t start = 0;
    while (true) {
        size_t pos = domain.find('.', start);
        labels.push_back(domain.substr(start, pos == string::npos ? string::npos : pos - start));
        if (pos == string::npos) break;
        start = pos + 1;
    }
    for (const string& label : labels) {
        if (label.empty() || label.front() == '-' || label.back() == '-') return false;
        for (char ch : label) {
            if (!((ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z') ||
                  (ch >= '0' && ch <= '9') || ch == '-')) return false;
        }
    }
    const string& tld = labels.back();
    if (tld.size() < 2 || tld.size() > 6) return false;
    return all_of(tld.begin(), tld.end(), [](char ch) {
        return (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z');
    });
}

// P012
bool isValidPassword(const string& pw) {
    if (pw.size() < 8) return false;
    bool upper = false, lower = false, digit = false, special = false;
    for (char ch : pw) {
        if (ch >= 'A' && ch <= 'Z') upper = true;
        else if (ch >= 'a' && ch <= 'z') lower = true;
        else if (ch >= '0' && ch <= '9') digit = true;
        else if (string("!@#$%^&*").find(ch) != string::npos) special = true;
    }
    return upper && lower && digit && special;
}

// P013
string isValidRange(const string& s) {
    vector<string> parts;
    size_t start = 0;
    while (true) {
        size_t pos = s.find('|', start);
        parts.push_back(s.substr(start, pos == string::npos ? string::npos : pos - start));
        if (pos == string::npos) break;
        start = pos + 1;
    }
    if (parts.size() != 3) return "INVALID";
    try {
        long long value = stoll(parts[0]);
        long long minValue = stoll(parts[1]);
        long long maxValue = stoll(parts[2]);
        return minValue <= value && value <= maxValue ? "VALID" : "INVALID";
    } catch (...) {
        return "INVALID";
    }
}

// P014
bool isValidIPv4(const string& ip) {
    vector<string> parts;
    size_t start = 0;
    while (true) {
        size_t pos = ip.find('.', start);
        parts.push_back(ip.substr(start, pos == string::npos ? string::npos : pos - start));
        if (pos == string::npos) break;
        start = pos + 1;
    }
    if (parts.size() != 4) return false;
    for (const string& part : parts) {
        if (part.empty() || (part.size() > 1 && part[0] == '0')) return false;
        for (char ch : part) if (ch < '0' || ch > '9') return false;
        try {
            if (stoi(part) > 255) return false;
        } catch (...) {
            return false;
        }
    }
    return true;
}

// P015
bool isValidUsername(const string& username) {
    if (username.size() < 3 || username.size() > 20) return false;
    if (!((username[0] >= 'A' && username[0] <= 'Z') || (username[0] >= 'a' && username[0] <= 'z'))) return false;
    for (char ch : username) {
        if (!((ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z') ||
              (ch >= '0' && ch <= '9') || ch == '_' || ch == '-')) return false;
    }
    return true;
}

// P016
string escapeHtml(const string& s) {
    string result;
    for (char ch : s) {
        switch (ch) {
            case '&': result += "&amp;"; break;
            case '<': result += "&lt;"; break;
            case '>': result += "&gt;"; break;
            case '"': result += "&quot;"; break;
            case '\'': result += "&#39;"; break;
            default: result += ch;
        }
    }
    return result;
}

// P017
string escapeCsvCell(const string& s) {
    if (s.find(',') != string::npos || s.find('"') != string::npos ||
        s.find('\n') != string::npos || s.find('\r') != string::npos) {
        string result = "\"";
        for (char ch : s) {
            if (ch == '"') result += "\"\"";
            else result += ch;
        }
        result += "\"";
        return result;
    }
    return s;
}

// P018
string escapeJsonString(const string& s) {
    ostringstream result;
    result << nouppercase << hex;
    for (unsigned char ch : s) {
        switch (ch) {
            case '"': result << "\\\""; break;
            case '\\': result << "\\\\"; break;
            case '/': result << "\\/"; break;
            case '\b': result << "\\b"; break;
            case '\f': result << "\\f"; break;
            case '\n': result << "\\n"; break;
            case '\r': result << "\\r"; break;
            case '\t': result << "\\t"; break;
            default:
                if (ch < 0x20) {
                    result << "\\u" << setw(4) << setfill('0') << static_cast<int>(ch);
                    result << setfill(' ');
                } else {
                    result << static_cast<char>(ch);
                }
        }
    }
    return result.str();
}

// P019
string encodeUrlComponent(const string& s) {
    const string hex = "0123456789ABCDEF";
    string result;
    for (unsigned char byte : s) {
        bool unreserved = (byte >= 'A' && byte <= 'Z') || (byte >= 'a' && byte <= 'z') ||
                          (byte >= '0' && byte <= '9') || byte == '-' || byte == '_' ||
                          byte == '.' || byte == '~';
        if (unreserved) result += static_cast<char>(byte);
        else {
            result += '%';
            result += hex[byte >> 4];
            result += hex[byte & 0x0F];
        }
    }
    return result;
}

// P020
string sanitizeTemplate(const string& s) {
    regex pattern(R"(\{\{([^{}]*)\}\})");
    string result;
    size_t last = 0;
    for (sregex_iterator it(s.begin(), s.end(), pattern), end; it != end; ++it) {
        smatch match = *it;
        result += s.substr(last, match.position() - last);
        string key = match.str(1);
        if (regex_match(key, regex(R"([a-zA-Z0-9_]+)"))) result += match.str(0);
        last = match.position() + match.length();
    }
    result += s.substr(last);
    return result;
}

// P021
string safePathNormalize(const string& path) {
    if (path.empty() || all_of(path.begin(), path.end(), [](unsigned char c) { return isspace(c); }) ||
        path.find('\\') != string::npos) return "";
    vector<string> parts;
    size_t start = 0;
    while (true) {
        size_t pos = path.find('/', start);
        string segment = path.substr(start, pos == string::npos ? string::npos : pos - start);
        if (!segment.empty() && segment != ".") {
            if (segment == "..") {
                if (parts.empty()) return "";
                parts.pop_back();
            } else {
                parts.push_back(segment);
            }
        }
        if (pos == string::npos) break;
        start = pos + 1;
    }
    string result;
    for (size_t i = 0; i < parts.size(); ++i) {
        if (i) result += '/';
        result += parts[i];
    }
    return result;
}

// P022
bool isAllowedExtension(const string& path) {
    size_t slash = path.find_last_of("/\\");
    string filename = path.substr(slash == string::npos ? 0 : slash + 1);
    size_t dot = filename.find_last_of('.');
    if (dot == string::npos || dot == 0) return false;
    string ext = filename.substr(dot);
    transform(ext.begin(), ext.end(), ext.begin(), [](unsigned char c) { return static_cast<char>(tolower(c)); });
    static const set<string> allowed{".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".csv"};
    return allowed.count(ext) > 0;
}

// P023
string sanitizeFilename(const string& name) {
    string value = name.substr(0, min<size_t>(200, name.size()));
    string replaced;
    for (char ch : value) {
        bool allowed = (ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z') ||
                       (ch >= '0' && ch <= '9') || ch == '.' || ch == '_' || ch == '-';
        replaced += allowed ? ch : '_';
    }
    string collapsed;
    for (char ch : replaced) {
        if (ch == '_' && !collapsed.empty() && collapsed.back() == '_') continue;
        collapsed += ch;
    }
    size_t first = collapsed.find_first_not_of('_');
    if (first == string::npos) return "_";
    size_t last = collapsed.find_last_not_of('_');
    return collapsed.substr(first, last - first + 1);
}

// P024
string checkArchiveEntry(const string& path) {
    if (path.empty()) return "safe";
    if (path.front() == '/' || path.find('\\') != string::npos) return "unsafe";
    int depth = 0;
    size_t start = 0;
    while (true) {
        size_t pos = path.find('/', start);
        string segment = path.substr(start, pos == string::npos ? string::npos : pos - start);
        if (!segment.empty() && segment != ".") {
            if (segment == "..") {
                if (--depth < 0) return "unsafe";
            } else {
                ++depth;
            }
        }
        if (pos == string::npos) break;
        start = pos + 1;
    }
    return "safe";
}

// P025
bool isAllowedFiletype(const string& ext) {
    string value = ext;
    if (!value.empty() && value.front() == '.') value.erase(value.begin());
    if (value.empty()) return false;
    transform(value.begin(), value.end(), value.begin(), [](unsigned char c) { return static_cast<char>(tolower(c)); });
    static const set<string> allowed{"jpg", "jpeg", "png", "gif", "bmp", "pdf", "txt", "csv", "json", "xml"};
    return allowed.count(value) > 0;
}

// P026
bool isValidSqlIdentifier(const string& name) {
    return regex_match(name, regex(R"([a-zA-Z_][a-zA-Z0-9_]{0,63})"));
}

// P027
string escapeSqlString(const string& s) {
    string result;
    for (char ch : s) {
        if (ch == '\\') result += "\\\\";
        else if (ch == '\'') result += "''";
        else result += ch;
    }
    return result;
}

// P028
string buildParamQuery(const string& s) {
    if (count(s.begin(), s.end(), '|') != 1) return "INVALID";
    size_t pipe = s.find('|');
    string table = s.substr(0, pipe);
    string conditions = s.substr(pipe + 1);
    if (!regex_match(table, regex(R"([a-zA-Z_][a-zA-Z0-9_]*)")) || conditions.empty()) return "INVALID";
    vector<string> columns;
    size_t start = 0;
    while (true) {
        size_t comma = conditions.find(',', start);
        string part = conditions.substr(start, comma == string::npos ? string::npos : comma - start);
        size_t eq = part.find('=');
        if (eq == string::npos) return "INVALID";
        string column = part.substr(0, eq);
        if (!regex_match(column, regex(R"([a-zA-Z_][a-zA-Z0-9_]*)"))) return "INVALID";
        columns.push_back(column);
        if (comma == string::npos) break;
        start = comma + 1;
    }
    if (columns.empty()) return "INVALID";
    string result = "SELECT * FROM " + table + " WHERE ";
    for (size_t i = 0; i < columns.size(); ++i) {
        if (i) result += " AND ";
        result += columns[i] + "=?";
    }
    return result;
}

// P029
string validateSortDirection(const string& s) {
    string value = s;
    size_t first = value.find_first_not_of(" \t\r\n");
    if (first == string::npos) return "INVALID";
    size_t last = value.find_last_not_of(" \t\r\n");
    value = value.substr(first, last - first + 1);
    transform(value.begin(), value.end(), value.begin(), [](unsigned char c) { return static_cast<char>(toupper(c)); });
    return value == "ASC" || value == "DESC" ? value : "INVALID";
}

// P030
bool isAllowedColumn(const string& col) {
    string value = col;
    size_t first = value.find_first_not_of(" \t\r\n");
    if (first == string::npos) value.clear();
    else {
        size_t last = value.find_last_not_of(" \t\r\n");
        value = value.substr(first, last - first + 1);
    }
    static const set<string> allowed{"id", "name", "email", "created_at", "status", "age", "role", "score"};
    return allowed.count(value) > 0;
}

// P031
string quoteShellArg(const string& s) {
    string result = "'";
    for (char ch : s) {
        if (ch == '\'') result += "'\\''";
        else result += ch;
    }
    result += "'";
    return result;
}

// P032
bool isAllowedCommand(const string& s) {
    string value = s;
    size_t first = value.find_first_not_of(" \t\r\n");
    if (first == string::npos) value.clear();
    else {
        size_t last = value.find_last_not_of(" \t\r\n");
        value = value.substr(first, last - first + 1);
    }
    static const set<string> allowed{"ls", "cat", "echo", "grep", "find", "sort", "uniq", "wc", "head", "tail"};
    return allowed.count(value) > 0;
}

// P033
string detectShellMeta(const string& s) {
    const string dangerous = ";|&$`><(){}\\\"'\n\r";
    return s.find_first_of(dangerous) == string::npos ? "safe" : "unsafe";
}

// P034
bool isValidEnvVar(const string& name) {
    if (name.empty() || name.size() > 64) return false;
    if (!((name[0] >= 'A' && name[0] <= 'Z') || name[0] == '_')) return false;
    for (char ch : name) {
        if (!((ch >= 'A' && ch <= 'Z') || (ch >= '0' && ch <= '9') || ch == '_')) return false;
    }
    return true;
}

// P035
vector<string> splitArgs(const string& s) {
    vector<string> tokens;
    string current;
    bool inQuotes = false;
    bool tokenStarted = false;
    for (char ch : s) {
        if (ch == '"') {
            inQuotes = !inQuotes;
            tokenStarted = true;
        } else if (ch == ' ' && !inQuotes) {
            if (tokenStarted) {
                tokens.push_back(current);
                current.clear();
                tokenStarted = false;
            }
        } else {
            current += ch;
            tokenStarted = true;
        }
    }
    if (tokenStarted) tokens.push_back(current);
    return tokens;
}

// P036
string parseSafeLiteral(const string& s) {
    if (regex_match(s, regex(R"(-?(0|[1-9][0-9]*))"))) return s;
    if (s == "true" || s == "false" || s == "null") return s;
    if (s.size() >= 2 && s.front() == '"' && s.back() == '"') {
        string content = s.substr(1, s.size() - 2);
        string result;
        for (size_t i = 0; i < content.size(); ++i) {
            if (content[i] == '\\') {
                if (i + 1 >= content.size() || content[i + 1] != '"') return "INVALID";
                result += '"';
                ++i;
            } else if (content[i] == '"') {
                return "INVALID";
            } else {
                result += content[i];
            }
        }
        return result;
    }
    return "INVALID";
}

// P037
string parseConfigBool(const string& s) {
    string value = s;
    size_t first = value.find_first_not_of(" \t\r\n");
    if (first == string::npos) return "INVALID";
    size_t last = value.find_last_not_of(" \t\r\n");
    value = value.substr(first, last - first + 1);
    transform(value.begin(), value.end(), value.begin(), [](unsigned char c) { return static_cast<char>(tolower(c)); });
    static const set<string> trueValues{"true", "yes", "1", "on", "enabled"};
    static const set<string> falseValues{"false", "no", "0", "off", "disabled"};
    if (trueValues.count(value)) return "true";
    if (falseValues.count(value)) return "false";
    return "INVALID";
}

// P038
bool isAllowedConfigKey(const string& key) {
    string value = key;
    size_t first = value.find_first_not_of(" \t\r\n");
    if (first == string::npos) value.clear();
    else {
        size_t last = value.find_last_not_of(" \t\r\n");
        value = value.substr(first, last - first + 1);
    }
    static const set<string> allowed{"host", "port", "database", "username", "password",
                                     "timeout", "max_connections", "ssl_enabled", "log_level", "retry_count"};
    return allowed.count(value) > 0;
}

// P039
string validateToken(const string& s) {
    return regex_match(s, regex(R"([A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[0-9a-f]{8})")) ? "valid" : "invalid";
}

// P040
string validateNumericExpr(const string& s) {
    const string number = R"(-?(0|[1-9][0-9]*))";
    regex pattern(number + "(\\s*[+\\-*/]\\s*" + number + ")*");
    return regex_match(s, pattern) ? "valid" : "invalid";
}

// P041
map<int, int> frequencyCounter(vector<int>& nums) {
    map<int, int> counts;
    for (int value : nums) ++counts[value];
    return counts;
}

// P042
bool hasDuplicate(vector<int>& nums) {
    unordered_set<int> seen;
    for (int value : nums) {
        if (!seen.insert(value).second) return true;
    }
    return false;
}

// P043
long long streamingSum(vector<int>& nums) {
    long long sum = 0;
    for (int value : nums) sum += value;
    return sum;
}

// P044
map<string, int> boundedLogProcessor(const string& log, int maxLines) {
    int kept = 0;
    int totalWords = 0;
    if (maxLines > 0 && !log.empty()) {
        istringstream stream(log);
        string line;
        while (getline(stream, line)) {
            bool nonEmpty = any_of(line.begin(), line.end(), [](unsigned char c) { return !isspace(c); });
            if (!nonEmpty) continue;
            if (kept >= maxLines) break;
            ++kept;
            istringstream words(line);
            string word;
            while (words >> word) ++totalWords;
        }
    }
    return {{"kept", kept}, {"total_words", totalWords}};
}

// P045
vector<int> topKFrequent(vector<int>& nums, int k) {
    if (nums.empty() || k == 0) return {};
    map<int, int> counts;
    for (int value : nums) ++counts[value];
    vector<int> values;
    for (const auto& [value, count] : counts) values.push_back(value);
    sort(values.begin(), values.end(), [&](int a, int b) {
        if (counts[a] != counts[b]) return counts[a] > counts[b];
        return a < b;
    });
    if (k < static_cast<int>(values.size())) values.resize(k);
    sort(values.begin(), values.end());
    return values;
}

// P046
string validateTokenFormat(const string& token) {
    return regex_match(token, regex(R"([a-zA-Z][a-zA-Z0-9-]{7,31})")) ? "valid" : "invalid";
}

// P047
string evaluatePermission(const string& role, const string& action) {
    static const map<string, set<string>> permissions{
        {"admin", {"read", "write", "delete", "execute"}},
        {"editor", {"read", "write"}},
        {"viewer", {"read"}},
        {"guest", {}}
    };
    auto it = permissions.find(role);
    return it != permissions.end() && it->second.count(action) ? "allowed" : "denied";
}

// P048
bool roleHasPermission(const string& role, const string& permission) {
    static const map<string, set<string>> permissions{
        {"admin", {"read", "write", "delete", "execute"}},
        {"editor", {"read", "write"}},
        {"viewer", {"read"}},
        {"guest", {}}
    };
    auto it = permissions.find(role);
    return it != permissions.end() && it->second.count(permission) > 0;
}

// P049
string checkSession(int lastActive, int currentTime, int timeout) {
    if (currentTime < lastActive) return "invalid";
    return currentTime - lastActive > timeout ? "expired" : "active";
}

// P050
string validateScope(const string& requested, vector<string>& allowed) {
    vector<string> parts;
    size_t start = 0;
    while (true) {
        size_t pos = requested.find(':', start);
        parts.push_back(requested.substr(start, pos == string::npos ? string::npos : pos - start));
        if (pos == string::npos) break;
        start = pos + 1;
    }
    for (int i = static_cast<int>(parts.size()); i >= 1; --i) {
        string prefix;
        for (int j = 0; j < i; ++j) {
            if (j) prefix += ':';
            prefix += parts[j];
        }
        if (find(allowed.begin(), allowed.end(), prefix) != allowed.end()) return "granted";
    }
    return "denied";
}
