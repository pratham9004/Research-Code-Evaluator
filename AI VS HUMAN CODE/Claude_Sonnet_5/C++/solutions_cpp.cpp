#include <algorithm>
#include <cstdio>
#include <map>
#include <set>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

using namespace std;

// P001
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<long long, int> seen;
    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
        long long complement = static_cast<long long>(target) - nums[i];
        auto it = seen.find(complement);
        if (it != seen.end()) {
            return {it->second, i};
        }
        seen.emplace(nums[i], i);
    }
    return {};
}


// P002
int maxSubarray(vector<int>& nums) {
    if (nums.empty()) {
        return 0;
    }
    long long best = nums[0];
    long long current = nums[0];
    for (size_t i = 1; i < nums.size(); ++i) {
        current = max(static_cast<long long>(nums[i]), current + nums[i]);
        best = max(best, current);
    }
    return static_cast<int>(best);
}


// P003
int binarySearch(vector<int>& nums, int target) {
    int low = 0;
    int high = static_cast<int>(nums.size()) - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (nums[mid] == target) {
            return mid;
        }
        if (nums[mid] < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return -1;
}


// P004
vector<int> mergeSortedArrays(vector<int>& nums1, vector<int>& nums2) {
    vector<int> merged;
    merged.reserve(nums1.size() + nums2.size());
    size_t i = 0;
    size_t j = 0;
    while (i < nums1.size() && j < nums2.size()) {
        if (nums1[i] <= nums2[j]) {
            merged.push_back(nums1[i++]);
        } else {
            merged.push_back(nums2[j++]);
        }
    }
    while (i < nums1.size()) {
        merged.push_back(nums1[i++]);
    }
    while (j < nums2.size()) {
        merged.push_back(nums2[j++]);
    }
    return merged;
}


// P005
bool isBalanced(const string& s) {
    string stack;
    for (char ch : s) {
        if (ch == '(' || ch == '[' || ch == '{') {
            stack.push_back(ch);
        } else if (ch == ')' || ch == ']' || ch == '}') {
            char expected = ch == ')' ? '(' : (ch == ']' ? '[' : '{');
            if (stack.empty() || stack.back() != expected) {
                return false;
            }
            stack.pop_back();
        } else {
            return false;
        }
    }
    return stack.empty();
}


// P006
int csvFieldCount(const string& line) {
    int count = 1;
    bool inQuotes = false;
    for (char ch : line) {
        if (ch == '"') {
            inQuotes = !inQuotes;
        } else if (ch == ',' && !inQuotes) {
            ++count;
        }
    }
    return count;
}


// P007
map<string, int> countLogLevels(const string& log) {
    map<string, int> counts = {{"DEBUG", 0}, {"ERROR", 0}, {"INFO", 0}, {"WARNING", 0}};
    const vector<string> levels = {"ERROR", "WARNING", "INFO", "DEBUG"};
    size_t pos = 0;
    while (pos <= log.size()) {
        size_t end = log.find_first_of("\r\n", pos);
        if (end == string::npos) {
            end = log.size();
        }
        string line = log.substr(pos, end - pos);
        for (const string& level : levels) {
            if (line.compare(0, level.size(), level) == 0 &&
                (line.size() == level.size() || line[level.size()] == ' ' || line[level.size()] == ':')) {
                ++counts[level];
                break;
            }
        }
        pos = end + 1;
    }
    return counts;
}


// P008
map<string, string> parseKeyValue(const string& s) {
    const string whitespace = " \t\n\r\f\v";
    auto trim = [&whitespace](const string& text) -> string {
        size_t begin = text.find_first_not_of(whitespace);
        if (begin == string::npos) {
            return string();
        }
        size_t last = text.find_last_not_of(whitespace);
        return text.substr(begin, last - begin + 1);
    };
    map<string, string> result;
    size_t start = 0;
    while (start <= s.size()) {
        size_t comma = s.find(',', start);
        if (comma == string::npos) {
            comma = s.size();
        }
        string pair = s.substr(start, comma - start);
        size_t eq = pair.find('=');
        if (eq != string::npos) {
            result[trim(pair.substr(0, eq))] = trim(pair.substr(eq + 1));
        }
        start = comma + 1;
    }
    return result;
}


// P009
string normalizeDate(const string& date) {
    char separator = date.find('/') != string::npos ? '/' : (date.find('-') != string::npos ? '-' : '.');
    vector<string> parts;
    size_t start = 0;
    while (true) {
        size_t p = date.find(separator, start);
        if (p == string::npos) {
            parts.push_back(date.substr(start));
            break;
        }
        parts.push_back(date.substr(start, p - start));
        start = p + 1;
    }
    if (parts.size() != 3) {
        return date;
    }
    string year, month, day;
    if (separator == '/') {
        month = parts[0];
        day = parts[1];
        year = parts[2];
    } else if (separator == '-') {
        day = parts[0];
        month = parts[1];
        year = parts[2];
    } else {
        year = parts[0];
        month = parts[1];
        day = parts[2];
    }
    auto pad = [](string value, size_t width) -> string {
        while (value.size() < width) {
            value.insert(value.begin(), '0');
        }
        return value;
    };
    return pad(year, 4) + "-" + pad(month, 2) + "-" + pad(day, 2);
}


// P010
vector<pair<string, int>> wordFrequency(const string& text) {
    map<string, int> counts;
    string word;
    auto flush = [&]() {
        if (!word.empty()) {
            ++counts[word];
            word.clear();
        }
    };
    for (char ch : text) {
        if (ch >= 'A' && ch <= 'Z') {
            word.push_back(static_cast<char>(ch - 'A' + 'a'));
        } else if (ch >= 'a' && ch <= 'z') {
            word.push_back(ch);
        } else {
            flush();
        }
    }
    flush();
    vector<pair<string, int>> result(counts.begin(), counts.end());
    sort(result.begin(), result.end(),
         [](const pair<string, int>& a, const pair<string, int>& b) {
             if (a.second != b.second) {
                 return a.second > b.second;
             }
             return a.first < b.first;
         });
    return result;
}


// P011
bool isValidEmail(const string& email) {
    auto isAlpha = [](char c) { return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'); };
    auto isDigit = [](char c) { return c >= '0' && c <= '9'; };
    if (count(email.begin(), email.end(), '@') != 1) {
        return false;
    }
    size_t at = email.find('@');
    string local = email.substr(0, at);
    string domain = email.substr(at + 1);
    if (local.empty()) {
        return false;
    }
    const string localSpecials = "._%+-";
    for (char c : local) {
        if (!isAlpha(c) && !isDigit(c) && localSpecials.find(c) == string::npos) {
            return false;
        }
    }
    if (local.front() == '.' || local.back() == '.' || local.find("..") != string::npos) {
        return false;
    }
    vector<string> labels;
    size_t start = 0;
    while (true) {
        size_t p = domain.find('.', start);
        if (p == string::npos) {
            labels.push_back(domain.substr(start));
            break;
        }
        labels.push_back(domain.substr(start, p - start));
        start = p + 1;
    }
    if (labels.size() < 2) {
        return false;
    }
    for (const string& label : labels) {
        if (label.empty() || label.front() == '-' || label.back() == '-') {
            return false;
        }
        for (char c : label) {
            if (!isAlpha(c) && !isDigit(c) && c != '-') {
                return false;
            }
        }
    }
    const string& tld = labels.back();
    if (tld.size() < 2 || tld.size() > 6) {
        return false;
    }
    for (char c : tld) {
        if (!isAlpha(c)) {
            return false;
        }
    }
    return true;
}


// P012
bool isValidPassword(const string& pw) {
    if (pw.size() < 8) {
        return false;
    }
    const string specials = "!@#$%^&*";
    bool hasUpper = false;
    bool hasLower = false;
    bool hasDigit = false;
    bool hasSpecial = false;
    for (char c : pw) {
        if (c >= 'A' && c <= 'Z') {
            hasUpper = true;
        } else if (c >= 'a' && c <= 'z') {
            hasLower = true;
        } else if (c >= '0' && c <= '9') {
            hasDigit = true;
        } else if (specials.find(c) != string::npos) {
            hasSpecial = true;
        }
    }
    return hasUpper && hasLower && hasDigit && hasSpecial;
}


// P013
string isValidRange(const string& s) {
    vector<string> parts;
    size_t start = 0;
    while (true) {
        size_t p = s.find('|', start);
        if (p == string::npos) {
            parts.push_back(s.substr(start));
            break;
        }
        parts.push_back(s.substr(start, p - start));
        start = p + 1;
    }
    if (parts.size() != 3) {
        return "INVALID";
    }
    for (const string& part : parts) {
        size_t i = (!part.empty() && (part[0] == '-' || part[0] == '+')) ? 1 : 0;
        if (i >= part.size()) {
            return "INVALID";
        }
        for (; i < part.size(); ++i) {
            if (part[i] < '0' || part[i] > '9') {
                return "INVALID";
            }
        }
    }
    auto normalize = [](const string& text, bool& negative, string& digits) {
        negative = text[0] == '-';
        size_t i = (text[0] == '-' || text[0] == '+') ? 1 : 0;
        while (i + 1 < text.size() && text[i] == '0') {
            ++i;
        }
        digits = text.substr(i);
        if (digits == "0") {
            negative = false;
        }
    };
    auto compareNumbers = [&normalize](const string& a, const string& b) -> int {
        bool negA, negB;
        string digitsA, digitsB;
        normalize(a, negA, digitsA);
        normalize(b, negB, digitsB);
        if (negA != negB) {
            return negA ? -1 : 1;
        }
        int magnitude;
        if (digitsA.size() != digitsB.size()) {
            magnitude = digitsA.size() < digitsB.size() ? -1 : 1;
        } else {
            int c = digitsA.compare(digitsB);
            magnitude = c < 0 ? -1 : (c > 0 ? 1 : 0);
        }
        return negA ? -magnitude : magnitude;
    };
    bool aboveMin = compareNumbers(parts[0], parts[1]) >= 0;
    bool belowMax = compareNumbers(parts[0], parts[2]) <= 0;
    return (aboveMin && belowMax) ? "VALID" : "INVALID";
}


// P014
bool isValidIPv4(const string& ip) {
    vector<string> octets;
    size_t start = 0;
    while (true) {
        size_t p = ip.find('.', start);
        if (p == string::npos) {
            octets.push_back(ip.substr(start));
            break;
        }
        octets.push_back(ip.substr(start, p - start));
        start = p + 1;
    }
    if (octets.size() != 4) {
        return false;
    }
    for (const string& octet : octets) {
        if (octet.empty() || octet.size() > 3) {
            return false;
        }
        int value = 0;
        for (char c : octet) {
            if (c < '0' || c > '9') {
                return false;
            }
            value = value * 10 + (c - '0');
        }
        if (octet.size() > 1 && octet[0] == '0') {
            return false;
        }
        if (value > 255) {
            return false;
        }
    }
    return true;
}


// P015
bool isValidUsername(const string& s) {
    if (s.size() < 3 || s.size() > 20) {
        return false;
    }
    auto isAlpha = [](char c) { return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'); };
    if (!isAlpha(s[0])) {
        return false;
    }
    for (char c : s) {
        if (!isAlpha(c) && !(c >= '0' && c <= '9') && c != '_' && c != '-') {
            return false;
        }
    }
    return true;
}


// P016
string escapeHtml(const string& s) {
    string result;
    result.reserve(s.size());
    for (char ch : s) {
        switch (ch) {
            case '&': result += "&amp;"; break;
            case '<': result += "&lt;"; break;
            case '>': result += "&gt;"; break;
            case '"': result += "&quot;"; break;
            case '\'': result += "&#39;"; break;
            default: result.push_back(ch);
        }
    }
    return result;
}


// P017
string escapeCsvCell(const string& s) {
    if (s.find_first_of(",\"\n\r") == string::npos) {
        return s;
    }
    string result = "\"";
    for (char ch : s) {
        if (ch == '"') {
            result += "\"\"";
        } else {
            result.push_back(ch);
        }
    }
    result.push_back('"');
    return result;
}


// P018
string escapeJsonString(const string& s) {
    string result;
    result.reserve(s.size());
    for (char ch : s) {
        switch (ch) {
            case '"': result += "\\\""; break;
            case '\\': result += "\\\\"; break;
            case '/': result += "\\/"; break;
            case '\b': result += "\\b"; break;
            case '\f': result += "\\f"; break;
            case '\n': result += "\\n"; break;
            case '\r': result += "\\r"; break;
            case '\t': result += "\\t"; break;
            default:
                if (static_cast<unsigned char>(ch) < 0x20) {
                    char buffer[8];
                    snprintf(buffer, sizeof(buffer), "\\u%04x", static_cast<unsigned char>(ch));
                    result += buffer;
                } else {
                    result.push_back(ch);
                }
        }
    }
    return result;
}


// P019
string encodeUrlComponent(const string& s) {
    const char* hex = "0123456789ABCDEF";
    string result;
    result.reserve(s.size() * 3);
    for (unsigned char ch : s) {
        bool unreserved = (ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z') ||
                          (ch >= '0' && ch <= '9') || ch == '-' || ch == '_' || ch == '.' || ch == '~';
        if (unreserved) {
            result.push_back(static_cast<char>(ch));
        } else {
            result.push_back('%');
            result.push_back(hex[ch >> 4]);
            result.push_back(hex[ch & 0x0F]);
        }
    }
    return result;
}


// P020
string sanitizeTemplate(const string& s) {
    string result;
    size_t pos = 0;
    while (pos < s.size()) {
        size_t open = s.find("{{", pos);
        if (open == string::npos) {
            result.append(s, pos, string::npos);
            break;
        }
        size_t close = s.find("}}", open + 2);
        if (close == string::npos) {
            result.append(s, pos, string::npos);
            break;
        }
        result.append(s, pos, open - pos);
        string key = s.substr(open + 2, close - open - 2);
        bool safe = !key.empty();
        for (char c : key) {
            bool allowed = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
                           (c >= '0' && c <= '9') || c == '_';
            if (!allowed) {
                safe = false;
                break;
            }
        }
        if (safe) {
            result.append(s, open, close + 2 - open);
        }
        pos = close + 2;
    }
    return result;
}


// P021
string safePathNormalize(const string& path) {
    const string whitespace = " \t\n\r\f\v";
    if (path.find_first_not_of(whitespace) == string::npos) {
        return "";
    }
    if (path.find('\\') != string::npos) {
        return "";
    }
    vector<string> resolved;
    size_t start = 0;
    while (start <= path.size()) {
        size_t slash = path.find('/', start);
        if (slash == string::npos) {
            slash = path.size();
        }
        string segment = path.substr(start, slash - start);
        start = slash + 1;
        if (segment.empty() || segment == ".") {
            continue;
        }
        if (segment == "..") {
            if (resolved.empty()) {
                return "";
            }
            resolved.pop_back();
        } else {
            resolved.push_back(segment);
        }
    }
    string result;
    for (size_t i = 0; i < resolved.size(); ++i) {
        if (i > 0) {
            result.push_back('/');
        }
        result += resolved[i];
    }
    return result;
}


// P022
bool isAllowedExtension(const string& path) {
    static const set<string> allowed = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".csv"};
    size_t separator = path.find_last_of("/\\");
    string filename = separator == string::npos ? path : path.substr(separator + 1);
    size_t dot = filename.rfind('.');
    if (dot == string::npos || dot == 0) {
        return false;
    }
    string extension = filename.substr(dot);
    for (char& c : extension) {
        if (c >= 'A' && c <= 'Z') {
            c = static_cast<char>(c - 'A' + 'a');
        }
    }
    return allowed.count(extension) > 0;
}


// P023
string sanitizeFilename(const string& name) {
    string result;
    size_t codePoints = 0;
    bool lastUnderscore = false;
    for (unsigned char ch : name) {
        if ((ch & 0xC0) != 0x80) {
            if (codePoints == 200) {
                break;
            }
            ++codePoints;
        }
        bool allowed = (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z') ||
                       (ch >= '0' && ch <= '9') || ch == '.' || ch == '_' || ch == '-';
        char out = allowed ? static_cast<char>(ch) : '_';
        if (out == '_') {
            if (lastUnderscore) {
                continue;
            }
            lastUnderscore = true;
        } else {
            lastUnderscore = false;
        }
        result.push_back(out);
    }
    size_t first = result.find_first_not_of('_');
    if (first == string::npos) {
        return "_";
    }
    size_t last = result.find_last_not_of('_');
    return result.substr(first, last - first + 1);
}


// P024
string checkArchiveEntry(const string& path) {
    if (path.empty()) {
        return "safe";
    }
    if (path[0] == '/' || path.find('\\') != string::npos) {
        return "unsafe";
    }
    int depth = 0;
    size_t start = 0;
    while (start <= path.size()) {
        size_t slash = path.find('/', start);
        if (slash == string::npos) {
            slash = path.size();
        }
        string segment = path.substr(start, slash - start);
        start = slash + 1;
        if (segment.empty() || segment == ".") {
            continue;
        }
        if (segment == "..") {
            if (--depth < 0) {
                return "unsafe";
            }
        } else {
            ++depth;
        }
    }
    return "safe";
}


// P025
bool isAllowedFiletype(const string& ext) {
    static const set<string> allowed = {"jpg", "jpeg", "png", "gif", "bmp", "pdf", "txt", "csv", "json", "xml"};
    string value = ext;
    if (!value.empty() && value[0] == '.') {
        value.erase(0, 1);
    }
    if (value.empty()) {
        return false;
    }
    for (char& c : value) {
        if (c >= 'A' && c <= 'Z') {
            c = static_cast<char>(c - 'A' + 'a');
        }
    }
    return allowed.count(value) > 0;
}


// P026
bool isValidSqlIdentifier(const string& name) {
    if (name.empty() || name.size() > 64) {
        return false;
    }
    for (size_t i = 0; i < name.size(); ++i) {
        char c = name[i];
        bool letterOrUnderscore = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
        bool digit = c >= '0' && c <= '9';
        if (i == 0 ? !letterOrUnderscore : !(letterOrUnderscore || digit)) {
            return false;
        }
    }
    return true;
}


// P027
string escapeSqlString(const string& s) {
    string result;
    result.reserve(s.size());
    for (char ch : s) {
        if (ch == '\\') {
            result += "\\\\";
        } else if (ch == '\'') {
            result += "''";
        } else {
            result.push_back(ch);
        }
    }
    return result;
}


// P028
string buildParamQuery(const string& s) {
    if (count(s.begin(), s.end(), '|') != 1) {
        return "INVALID";
    }
    size_t bar = s.find('|');
    string table = s.substr(0, bar);
    string conditions = s.substr(bar + 1);
    auto isIdentifier = [](const string& text) {
        if (text.empty()) {
            return false;
        }
        for (size_t i = 0; i < text.size(); ++i) {
            char c = text[i];
            bool letterOrUnderscore = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
            bool digit = c >= '0' && c <= '9';
            if (i == 0 ? !letterOrUnderscore : !(letterOrUnderscore || digit)) {
                return false;
            }
        }
        return true;
    };
    if (!isIdentifier(table) || conditions.empty()) {
        return "INVALID";
    }
    string query = "SELECT * FROM " + table + " WHERE ";
    size_t start = 0;
    bool first = true;
    while (true) {
        size_t comma = conditions.find(',', start);
        string condition = conditions.substr(start, comma == string::npos ? string::npos : comma - start);
        size_t eq = condition.find('=');
        if (eq == string::npos) {
            return "INVALID";
        }
        string column = condition.substr(0, eq);
        if (!isIdentifier(column)) {
            return "INVALID";
        }
        if (!first) {
            query += " AND ";
        }
        query += column + "=?";
        first = false;
        if (comma == string::npos) {
            break;
        }
        start = comma + 1;
    }
    return query;
}


// P029
string validateSortDirection(const string& s) {
    const string whitespace = " \t\n\r\f\v";
    size_t begin = s.find_first_not_of(whitespace);
    if (begin == string::npos) {
        return "INVALID";
    }
    size_t last = s.find_last_not_of(whitespace);
    string direction = s.substr(begin, last - begin + 1);
    for (char& c : direction) {
        if (c >= 'a' && c <= 'z') {
            c = static_cast<char>(c - 'a' + 'A');
        }
    }
    return (direction == "ASC" || direction == "DESC") ? direction : "INVALID";
}


// P030
bool isAllowedColumn(const string& col) {
    static const set<string> allowed = {"id", "name", "email", "created_at", "status", "age", "role", "score"};
    const string whitespace = " \t\n\r\f\v";
    size_t begin = col.find_first_not_of(whitespace);
    if (begin == string::npos) {
        return false;
    }
    size_t last = col.find_last_not_of(whitespace);
    return allowed.count(col.substr(begin, last - begin + 1)) > 0;
}


// P031
string quoteShellArg(const string& s) {
    string result = "'";
    for (char ch : s) {
        if (ch == '\'') {
            result += "'\\''";
        } else {
            result.push_back(ch);
        }
    }
    result.push_back('\'');
    return result;
}


// P032
bool isAllowedCommand(const string& s) {
    static const set<string> allowed = {"ls", "cat", "echo", "grep", "find", "sort", "uniq", "wc", "head", "tail"};
    const string whitespace = " \t\n\r\f\v";
    size_t begin = s.find_first_not_of(whitespace);
    if (begin == string::npos) {
        return false;
    }
    size_t last = s.find_last_not_of(whitespace);
    string command = s.substr(begin, last - begin + 1);
    if (command.find(' ') != string::npos) {
        return false;
    }
    return allowed.count(command) > 0;
}


// P033
string detectShellMeta(const string& s) {
    return s.find_first_of(";|&$`><(){}\\\"'\n\r") == string::npos ? "safe" : "unsafe";
}


// P034
bool isValidEnvVar(const string& name) {
    if (name.empty() || name.size() > 64) {
        return false;
    }
    for (size_t i = 0; i < name.size(); ++i) {
        char c = name[i];
        bool upperOrUnderscore = (c >= 'A' && c <= 'Z') || c == '_';
        bool digit = c >= '0' && c <= '9';
        if (i == 0 ? !upperOrUnderscore : !(upperOrUnderscore || digit)) {
            return false;
        }
    }
    return true;
}


// P035
vector<string> splitArgs(const string& s) {
    vector<string> tokens;
    string current;
    bool inQuotes = false;
    bool hasToken = false;
    for (char ch : s) {
        if (ch == '"') {
            inQuotes = !inQuotes;
            hasToken = true;
        } else if (ch == ' ' && !inQuotes) {
            if (hasToken) {
                tokens.push_back(current);
                current.clear();
                hasToken = false;
            }
        } else {
            current.push_back(ch);
            hasToken = true;
        }
    }
    if (hasToken) {
        tokens.push_back(current);
    }
    return tokens;
}


// P036
string parseSafeLiteral(const string& s) {
    {
        size_t digitsStart = (!s.empty() && s[0] == '-') ? 1 : 0;
        bool allDigits = digitsStart < s.size();
        for (size_t i = digitsStart; i < s.size() && allDigits; ++i) {
            if (s[i] < '0' || s[i] > '9') {
                allDigits = false;
            }
        }
        if (allDigits && (s[digitsStart] != '0' || s.size() - digitsStart == 1)) {
            return s == "-0" ? string("0") : s;
        }
    }
    if (s == "true" || s == "false" || s == "null") {
        return s;
    }
    if (s.size() >= 2 && s.front() == '"' && s.back() == '"') {
        string inner = s.substr(1, s.size() - 2);
        string result;
        size_t i = 0;
        while (i < inner.size()) {
            char ch = inner[i];
            if (ch == '\\') {
                if (i + 1 < inner.size() && inner[i + 1] == '"') {
                    result.push_back('"');
                    i += 2;
                    continue;
                }
                return "INVALID";
            }
            if (ch == '"') {
                return "INVALID";
            }
            result.push_back(ch);
            ++i;
        }
        return result;
    }
    return "INVALID";
}


// P037
string parseConfigBool(const string& s) {
    const string whitespace = " \t\n\r\f\v";
    size_t begin = s.find_first_not_of(whitespace);
    if (begin == string::npos) {
        return "INVALID";
    }
    size_t last = s.find_last_not_of(whitespace);
    string value = s.substr(begin, last - begin + 1);
    for (char& c : value) {
        if (c >= 'A' && c <= 'Z') {
            c = static_cast<char>(c - 'A' + 'a');
        }
    }
    if (value == "true" || value == "yes" || value == "1" || value == "on" || value == "enabled") {
        return "true";
    }
    if (value == "false" || value == "no" || value == "0" || value == "off" || value == "disabled") {
        return "false";
    }
    return "INVALID";
}


// P038
bool isAllowedConfigKey(const string& key) {
    static const set<string> allowed = {
        "host", "port", "database", "username", "password",
        "timeout", "max_connections", "ssl_enabled", "log_level", "retry_count"};
    const string whitespace = " \t\n\r\f\v";
    size_t begin = key.find_first_not_of(whitespace);
    if (begin == string::npos) {
        return false;
    }
    size_t last = key.find_last_not_of(whitespace);
    return allowed.count(key.substr(begin, last - begin + 1)) > 0;
}


// P039
string validateToken(const string& s) {
    vector<string> parts;
    size_t start = 0;
    while (true) {
        size_t p = s.find('.', start);
        if (p == string::npos) {
            parts.push_back(s.substr(start));
            break;
        }
        parts.push_back(s.substr(start, p - start));
        start = p + 1;
    }
    if (parts.size() != 3) {
        return "invalid";
    }
    for (int index = 0; index < 2; ++index) {
        if (parts[index].empty()) {
            return "invalid";
        }
        for (char c : parts[index]) {
            bool allowed = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
                           (c >= '0' && c <= '9') || c == '_' || c == '-';
            if (!allowed) {
                return "invalid";
            }
        }
    }
    if (parts[2].size() != 8) {
        return "invalid";
    }
    for (char c : parts[2]) {
        if (!((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f'))) {
            return "invalid";
        }
    }
    return "valid";
}


// P040
string validateNumericExpr(const string& s) {
    size_t i = 0;
    const size_t n = s.size();
    auto parseNumber = [&]() -> bool {
        if (i < n && s[i] == '-') {
            ++i;
        }
        if (i >= n || s[i] < '0' || s[i] > '9') {
            return false;
        }
        if (s[i] == '0') {
            ++i;
            return !(i < n && s[i] >= '0' && s[i] <= '9');
        }
        while (i < n && s[i] >= '0' && s[i] <= '9') {
            ++i;
        }
        return true;
    };
    auto skipSpaces = [&]() {
        while (i < n && s[i] == ' ') {
            ++i;
        }
    };
    if (!parseNumber()) {
        return "invalid";
    }
    while (true) {
        size_t afterNumber = i;
        skipSpaces();
        if (i == n) {
            return afterNumber == n ? "valid" : "invalid";
        }
        if (s[i] != '+' && s[i] != '-' && s[i] != '*' && s[i] != '/') {
            return "invalid";
        }
        ++i;
        skipSpaces();
        if (!parseNumber()) {
            return "invalid";
        }
    }
}


// P041
map<int, int> frequencyCounter(vector<int>& nums) {
    map<int, int> counts;
    for (int value : nums) {
        ++counts[value];
    }
    return counts;
}


// P042
bool hasDuplicate(vector<int>& nums) {
    unordered_set<int> seen;
    for (int value : nums) {
        if (!seen.insert(value).second) {
            return true;
        }
    }
    return false;
}


// P043
long long streamingSum(vector<int>& nums) {
    long long total = 0;
    for (int value : nums) {
        total += value;
    }
    return total;
}


// P044
map<string, int> boundedLogProcessor(const string& log, int maxLines) {
    int kept = 0;
    int totalWords = 0;
    if (maxLines > 0) {
        const string whitespace = " \t\n\r\f\v";
        size_t pos = 0;
        while (pos <= log.size() && kept < maxLines) {
            size_t end = log.find_first_of("\r\n", pos);
            if (end == string::npos) {
                end = log.size();
            }
            string line = log.substr(pos, end - pos);
            pos = end + 1;
            if (line.find_first_not_of(whitespace) == string::npos) {
                continue;
            }
            ++kept;
            bool inWord = false;
            for (char c : line) {
                bool space = whitespace.find(c) != string::npos;
                if (!space && !inWord) {
                    ++totalWords;
                }
                inWord = !space;
            }
        }
    }
    return {{"kept", kept}, {"total_words", totalWords}};
}


// P045
vector<int> topKFrequent(vector<int>& nums, int k) {
    if (k <= 0 || nums.empty()) {
        return {};
    }
    map<int, int> counts;
    for (int value : nums) {
        ++counts[value];
    }
    vector<pair<int, int>> items(counts.begin(), counts.end());
    sort(items.begin(), items.end(),
         [](const pair<int, int>& a, const pair<int, int>& b) {
             if (a.second != b.second) {
                 return a.second > b.second;
             }
             return a.first < b.first;
         });
    size_t take = min(items.size(), static_cast<size_t>(k));
    vector<int> result;
    result.reserve(take);
    for (size_t i = 0; i < take; ++i) {
        result.push_back(items[i].first);
    }
    sort(result.begin(), result.end());
    return result;
}


// P046
string validateTokenFormat(const string& token) {
    if (token.size() < 8 || token.size() > 32) {
        return "invalid";
    }
    char first = token[0];
    if (!((first >= 'a' && first <= 'z') || (first >= 'A' && first <= 'Z'))) {
        return "invalid";
    }
    for (char c : token) {
        bool allowed = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
                       (c >= '0' && c <= '9') || c == '-';
        if (!allowed) {
            return "invalid";
        }
    }
    return "valid";
}


// P047
string evaluatePermission(const string& role, const string& action) {
    static const map<string, set<string>> permissions = {
        {"admin", {"read", "write", "delete", "execute"}},
        {"editor", {"read", "write"}},
        {"viewer", {"read"}},
        {"guest", {}},
    };
    auto it = permissions.find(role);
    if (it == permissions.end()) {
        return "denied";
    }
    return it->second.count(action) > 0 ? "allowed" : "denied";
}


// P048
bool roleHasPermission(const string& role, const string& permission) {
    static const map<string, set<string>> permissions = {
        {"admin", {"read", "write", "delete", "execute"}},
        {"editor", {"read", "write"}},
        {"viewer", {"read"}},
        {"guest", {}},
    };
    auto it = permissions.find(role);
    if (it == permissions.end()) {
        return false;
    }
    return it->second.count(permission) > 0;
}


// P049
string checkSession(int lastActive, int currentTime, int timeout) {
    if (currentTime < lastActive) {
        return "invalid";
    }
    long long elapsed = static_cast<long long>(currentTime) - lastActive;
    return elapsed > timeout ? "expired" : "active";
}


// P050
string validateScope(const string& requested, vector<string>& allowed) {
    set<string> allowedScopes(allowed.begin(), allowed.end());
    size_t pos = 0;
    while (true) {
        size_t colon = requested.find(':', pos);
        if (colon == string::npos) {
            break;
        }
        if (allowedScopes.count(requested.substr(0, colon)) > 0) {
            return "granted";
        }
        pos = colon + 1;
    }
    return allowedScopes.count(requested) > 0 ? "granted" : "denied";
}
