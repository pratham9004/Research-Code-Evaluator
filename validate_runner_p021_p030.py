"""
Validation runner for P021-P030 — one problem/language/variant per call.
Usage: python validate_runner_p021_p030.py <pid> <lang> <variant>
variant: correct | wrong | error
"""
import sys, os, sqlite3
sys.path.insert(0, os.path.dirname(__file__))
from backend.engine.executor import execute

SOLUTIONS = {

# ── P021 ──────────────────────────────────────────────────────────────
("P021","python","correct"): r"""
def safe_path_normalize(path):
    if not path or not path.strip(): return ""
    if "\\" in path: return ""
    parts = path.split("/")
    resolved = []
    for part in parts:
        if part == "" or part == ".": continue
        elif part == "..":
            if resolved: resolved.pop()
            else: return ""
        else: resolved.append(part)
    return "/".join(resolved)
""",
("P021","python","wrong"): "def safe_path_normalize(path): return path\n",
("P021","java","correct"): r"""
public class Solution {
    public static String safePathNormalize(String path) {
        if (path == null || path.trim().isEmpty()) return "";
        if (path.contains("\\")) return "";
        String[] parts = path.split("/", -1);
        java.util.Deque<String> stack = new java.util.ArrayDeque<>();
        for (String part : parts) {
            if (part.isEmpty() || part.equals(".")) continue;
            else if (part.equals("..")) {
                if (stack.isEmpty()) return "";
                stack.pollLast();
            } else stack.addLast(part);
        }
        return String.join("/", stack);
    }
}""",
("P021","java","wrong"): "public class Solution { public static String safePathNormalize(String p) { return p; } }",
("P021","cpp","correct"): r"""
#include <string>
#include <vector>
#include <sstream>
using namespace std;
string safePathNormalize(const string& path) {
    if (path.empty()) return "";
    if (path.find('\\') != string::npos) return "";
    // check all whitespace
    bool allWs = true;
    for (char c : path) if (c != ' ') { allWs = false; break; }
    if (allWs) return "";
    vector<string> stack;
    stringstream ss(path); string part;
    while (getline(ss, part, '/')) {
        if (part.empty() || part == ".") continue;
        else if (part == "..") {
            if (stack.empty()) return "";
            stack.pop_back();
        } else stack.push_back(part);
    }
    string res;
    for (size_t i = 0; i < stack.size(); i++) { if (i) res += '/'; res += stack[i]; }
    return res;
}""",
("P021","cpp","wrong"): "#include <string>\nusing namespace std;\nstring safePathNormalize(const string& p) { return p; }",
("P021","javascript","correct"): r"""
function safePathNormalize(path) {
    if (!path || !path.trim()) return '';
    if (path.includes('\\')) return '';
    const parts = path.split('/');
    const stack = [];
    for (const part of parts) {
        if (!part || part === '.') continue;
        else if (part === '..') {
            if (stack.length === 0) return '';
            stack.pop();
        } else stack.push(part);
    }
    return stack.join('/');
}
module.exports = { safePathNormalize };""",
("P021","javascript","wrong"): "function safePathNormalize(p){return p;}\nmodule.exports={safePathNormalize};",

# ── P022 ──────────────────────────────────────────────────────────────
("P022","python","correct"): r"""
def is_allowed_extension(path):
    allowed = {'.jpg','.jpeg','.png','.gif','.pdf','.txt','.csv'}
    filename = path.split('/')[-1].split('\\')[-1]
    if not filename or filename.startswith('.'): return False
    dot = filename.rfind('.')
    if dot <= 0: return False
    return filename[dot:].lower() in allowed
""",
("P022","python","wrong"): "def is_allowed_extension(path): return True\n",
("P022","java","correct"): r"""
import java.util.*;
public class Solution {
    private static final Set<String> ALLOWED = new HashSet<>(Arrays.asList(
        ".jpg",".jpeg",".png",".gif",".pdf",".txt",".csv"));
    public static boolean isAllowedExtension(String path) {
        String filename = path;
        int slash = Math.max(path.lastIndexOf('/'), path.lastIndexOf('\\'));
        if (slash >= 0) filename = path.substring(slash + 1);
        if (filename.isEmpty() || filename.startsWith(".")) return false;
        int dot = filename.lastIndexOf('.');
        if (dot <= 0) return false;
        return ALLOWED.contains(filename.substring(dot).toLowerCase());
    }
}""",
("P022","cpp","correct"): r"""
#include <string>
#include <set>
#include <algorithm>
using namespace std;
bool isAllowedExtension(const string& path) {
    static set<string> allowed = {".jpg",".jpeg",".png",".gif",".pdf",".txt",".csv"};
    string filename = path;
    size_t s = max(path.rfind('/'), path.rfind('\\'));
    if (s != string::npos) filename = path.substr(s+1);
    if (filename.empty() || filename[0] == '.') return false;
    size_t dot = filename.rfind('.');
    if (dot == string::npos || dot == 0) return false;
    string ext = filename.substr(dot);
    transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
    return allowed.count(ext) > 0;
}""",
("P022","javascript","correct"): r"""
function isAllowedExtension(path) {
    const allowed = new Set(['.jpg','.jpeg','.png','.gif','.pdf','.txt','.csv']);
    const parts = path.replace(/\\/g, '/').split('/');
    const filename = parts[parts.length-1];
    if (!filename || filename.startsWith('.')) return false;
    const dot = filename.lastIndexOf('.');
    if (dot <= 0) return false;
    return allowed.has(filename.slice(dot).toLowerCase());
}
module.exports = { isAllowedExtension };""",

# ── P023 ──────────────────────────────────────────────────────────────
("P023","python","correct"): r"""
import re
def sanitize_filename(name):
    name = name[:200]
    s = re.sub(r'[^a-zA-Z0-9._\-]', '_', name)
    s = re.sub(r'_+', '_', s)
    s = s.strip('_')
    return s if s else '_'
""",
("P023","python","wrong"): "def sanitize_filename(name): return name\n",
("P023","java","correct"): r"""
public class Solution {
    public static String sanitizeFilename(String name) {
        if (name.length() > 200) name = name.substring(0, 200);
        String s = name.replaceAll("[^a-zA-Z0-9._\\-]", "_");
        s = s.replaceAll("_+", "_");
        s = s.replaceAll("^_+|_+$", "");
        return s.isEmpty() ? "_" : s;
    }
}""",
("P023","cpp","correct"): r"""
#include <string>
#include <regex>
using namespace std;
string sanitizeFilename(const string& name) {
    string n = name.substr(0, min((int)name.size(), 200));
    string s;
    for (char c : n) {
        if (isalnum(c) || c == '.' || c == '_' || c == '-') s += c;
        else s += '_';
    }
    // collapse underscores
    string r;
    bool prevUs = false;
    for (char c : s) {
        if (c == '_') { if (!prevUs) r += c; prevUs = true; }
        else { r += c; prevUs = false; }
    }
    // strip leading/trailing underscores
    size_t start = r.find_first_not_of('_');
    if (start == string::npos) return "_";
    size_t end = r.find_last_not_of('_');
    return r.substr(start, end - start + 1);
}""",
("P023","javascript","correct"): r"""
function sanitizeFilename(name) {
    name = name.slice(0, 200);
    let s = name.replace(/[^a-zA-Z0-9._\-]/g, '_');
    s = s.replace(/_+/g, '_');
    s = s.replace(/^_+|_+$/g, '');
    return s || '_';
}
module.exports = { sanitizeFilename };""",

# ── P024 ──────────────────────────────────────────────────────────────
("P024","python","correct"): r"""
def check_archive_entry(path):
    if not path: return "safe"
    if '\\' in path: return "unsafe"
    if path.startswith('/'): return "unsafe"
    depth = 0
    for part in path.split('/'):
        if not part or part == '.': continue
        elif part == '..':
            depth -= 1
            if depth < 0: return "unsafe"
        else: depth += 1
    return "safe"
""",
("P024","python","wrong"): "def check_archive_entry(path): return 'safe'\n",
("P024","java","correct"): r"""
public class Solution {
    public static String checkArchiveEntry(String path) {
        if (path == null || path.isEmpty()) return "safe";
        if (path.contains("\\") || path.startsWith("/")) return "unsafe";
        int depth = 0;
        for (String part : path.split("/", -1)) {
            if (part.isEmpty() || part.equals(".")) continue;
            else if (part.equals("..")) { depth--; if (depth < 0) return "unsafe"; }
            else depth++;
        }
        return "safe";
    }
}""",
("P024","cpp","correct"): r"""
#include <string>
#include <vector>
#include <sstream>
using namespace std;
string checkArchiveEntry(const string& path) {
    if (path.empty()) return "safe";
    if (path.find('\\') != string::npos) return "unsafe";
    if (path[0] == '/') return "unsafe";
    int depth = 0;
    stringstream ss(path); string part;
    while (getline(ss, part, '/')) {
        if (part.empty() || part == ".") continue;
        else if (part == "..") { depth--; if (depth < 0) return "unsafe"; }
        else depth++;
    }
    return "safe";
}""",
("P024","javascript","correct"): r"""
function checkArchiveEntry(path) {
    if (!path) return 'safe';
    if (path.includes('\\') || path.startsWith('/')) return 'unsafe';
    let depth = 0;
    for (const part of path.split('/')) {
        if (!part || part === '.') continue;
        else if (part === '..') { depth--; if (depth < 0) return 'unsafe'; }
        else depth++;
    }
    return 'safe';
}
module.exports = { checkArchiveEntry };""",

# ── P025 ──────────────────────────────────────────────────────────────
("P025","python","correct"): r"""
def is_allowed_filetype(ext):
    allowed = {'jpg','jpeg','png','gif','bmp','pdf','txt','csv','json','xml'}
    return ext.strip().lstrip('.').lower() in allowed
""",
("P025","python","wrong"): "def is_allowed_filetype(ext): return True\n",
("P025","java","correct"): r"""
import java.util.*;
public class Solution {
    private static final Set<String> ALLOWED = new HashSet<>(Arrays.asList(
        "jpg","jpeg","png","gif","bmp","pdf","txt","csv","json","xml"));
    public static boolean isAllowedFiletype(String ext) {
        String s = ext.trim();
        if (s.startsWith(".")) s = s.substring(1);
        return ALLOWED.contains(s.toLowerCase());
    }
}""",
("P025","cpp","correct"): r"""
#include <string>
#include <set>
#include <algorithm>
using namespace std;
bool isAllowedFiletype(const string& ext) {
    static set<string> allowed = {"jpg","jpeg","png","gif","bmp","pdf","txt","csv","json","xml"};
    string s = ext;
    while (!s.empty() && s.front() == ' ') s.erase(s.begin());
    while (!s.empty() && s.back() == ' ') s.pop_back();
    if (!s.empty() && s.front() == '.') s.erase(s.begin());
    transform(s.begin(), s.end(), s.begin(), ::tolower);
    return allowed.count(s) > 0;
}""",
("P025","javascript","correct"): r"""
function isAllowedFiletype(ext) {
    const allowed = new Set(['jpg','jpeg','png','gif','bmp','pdf','txt','csv','json','xml']);
    let s = ext.trim();
    if (s.startsWith('.')) s = s.slice(1);
    return allowed.has(s.toLowerCase());
}
module.exports = { isAllowedFiletype };""",

# ── P026 ──────────────────────────────────────────────────────────────
("P026","python","correct"): r"""
import re
def is_valid_sql_identifier(name):
    if not name or len(name) > 64: return False
    return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name))
""",
("P026","python","wrong"): "def is_valid_sql_identifier(name): return True\n",
("P026","java","correct"): r"""
public class Solution {
    public static boolean isValidSqlIdentifier(String name) {
        if (name == null || name.isEmpty() || name.length() > 64) return false;
        return name.matches("[a-zA-Z_][a-zA-Z0-9_]*");
    }
}""",
("P026","cpp","correct"): r"""
#include <string>
#include <regex>
using namespace std;
bool isValidSqlIdentifier(const string& name) {
    if (name.empty() || name.size() > 64) return false;
    if (!isalpha(name[0]) && name[0] != '_') return false;
    for (char c : name) if (!isalnum(c) && c != '_') return false;
    return true;
}""",
("P026","javascript","correct"): r"""
function isValidSqlIdentifier(name) {
    if (!name || name.length > 64) return false;
    return /^[a-zA-Z_][a-zA-Z0-9_]*$/.test(name);
}
module.exports = { isValidSqlIdentifier };""",

# ── P027 ──────────────────────────────────────────────────────────────
("P027","python","correct"): r"""
def escape_sql_string(s):
    s = s.replace('\\', '\\\\')
    s = s.replace("'", "''")
    return s
""",
("P027","python","wrong"): "def escape_sql_string(s): return s\n",
("P027","java","correct"): r"""
public class Solution {
    public static String escapeSqlString(String s) {
        return s.replace("\\", "\\\\").replace("'", "''");
    }
}""",
("P027","cpp","correct"): r"""
#include <string>
using namespace std;
string escapeSqlString(const string& s) {
    string r;
    for (char c : s) {
        if (c == '\\') r += "\\\\";
        else if (c == '\'') r += "''";
        else r += c;
    }
    return r;
}""",
("P027","javascript","correct"): r"""
function escapeSqlString(s) {
    return s.replace(/\\/g, '\\\\').replace(/'/g, "''");
}
module.exports = { escapeSqlString };""",

# ── P028 ──────────────────────────────────────────────────────────────
("P028","python","correct"): r"""
import re
def build_param_query(s):
    parts = s.split('|', 1)
    if len(parts) != 2: return 'INVALID'
    table = parts[0].strip()
    cond_str = parts[1].strip()
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table): return 'INVALID'
    if not cond_str: return 'INVALID'
    pairs = cond_str.split(',')
    clauses = []
    for pair in pairs:
        if '=' not in pair: return 'INVALID'
        col = pair.split('=', 1)[0].strip()
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', col): return 'INVALID'
        clauses.append(f'{col}=?')
    return f"SELECT * FROM {table} WHERE {' AND '.join(clauses)}"
""",
("P028","python","wrong"): "def build_param_query(s): return 'INVALID'\n",
("P028","java","correct"): r"""
public class Solution {
    public static String buildParamQuery(String s) {
        String[] parts = s.split("\\|", 2);
        if (parts.length != 2) return "INVALID";
        String table = parts[0].trim();
        String condStr = parts[1].trim();
        if (!table.matches("[a-zA-Z_][a-zA-Z0-9_]*")) return "INVALID";
        if (condStr.isEmpty()) return "INVALID";
        String[] pairs = condStr.split(",");
        StringBuilder sb = new StringBuilder("SELECT * FROM " + table + " WHERE ");
        for (int i = 0; i < pairs.length; i++) {
            int eq = pairs[i].indexOf('=');
            if (eq < 0) return "INVALID";
            String col = pairs[i].substring(0, eq).trim();
            if (!col.matches("[a-zA-Z_][a-zA-Z0-9_]*")) return "INVALID";
            if (i > 0) sb.append(" AND ");
            sb.append(col).append("=?");
        }
        return sb.toString();
    }
}""",
("P028","cpp","correct"): r"""
#include <string>
#include <vector>
#include <sstream>
#include <regex>
using namespace std;
bool validId(const string& s) {
    if (s.empty()) return false;
    if (!isalpha(s[0]) && s[0] != '_') return false;
    for (char c : s) if (!isalnum(c) && c != '_') return false;
    return true;
}
string trim(const string& s) {
    size_t a = s.find_first_not_of(" \t");
    if (a == string::npos) return "";
    size_t b = s.find_last_not_of(" \t");
    return s.substr(a, b-a+1);
}
string buildParamQuery(const string& s) {
    size_t pipe = s.find('|');
    if (pipe == string::npos) return "INVALID";
    string table = trim(s.substr(0, pipe));
    string condStr = trim(s.substr(pipe+1));
    if (!validId(table) || condStr.empty()) return "INVALID";
    vector<string> clauses;
    stringstream ss(condStr); string tok;
    while (getline(ss, tok, ',')) {
        size_t eq = tok.find('=');
        if (eq == string::npos) return "INVALID";
        string col = trim(tok.substr(0, eq));
        if (!validId(col)) return "INVALID";
        clauses.push_back(col + "=?");
    }
    if (clauses.empty()) return "INVALID";
    string res = "SELECT * FROM " + table + " WHERE ";
    for (size_t i = 0; i < clauses.size(); i++) { if (i) res += " AND "; res += clauses[i]; }
    return res;
}""",
("P028","javascript","correct"): r"""
function buildParamQuery(s) {
    const pipe = s.indexOf('|');
    if (pipe < 0) return 'INVALID';
    const table = s.slice(0, pipe).trim();
    const condStr = s.slice(pipe+1).trim();
    if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(table)) return 'INVALID';
    if (!condStr) return 'INVALID';
    const pairs = condStr.split(',');
    const clauses = [];
    for (const pair of pairs) {
        const eq = pair.indexOf('=');
        if (eq < 0) return 'INVALID';
        const col = pair.slice(0, eq).trim();
        if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(col)) return 'INVALID';
        clauses.push(col + '=?');
    }
    return 'SELECT * FROM ' + table + ' WHERE ' + clauses.join(' AND ');
}
module.exports = { buildParamQuery };""",

# ── P029 ──────────────────────────────────────────────────────────────
("P029","python","correct"): r"""
def validate_sort_direction(s):
    n = s.strip().upper()
    return n if n in ('ASC','DESC') else 'INVALID'
""",
("P029","python","wrong"): "def validate_sort_direction(s): return s\n",
("P029","java","correct"): r"""
public class Solution {
    public static String validateSortDirection(String s) {
        String n = s.strip().toUpperCase();
        return (n.equals("ASC") || n.equals("DESC")) ? n : "INVALID";
    }
}""",
("P029","cpp","correct"): r"""
#include <string>
#include <algorithm>
using namespace std;
string validateSortDirection(const string& s) {
    string n = s;
    while (!n.empty() && n.front()==' ') n.erase(n.begin());
    while (!n.empty() && n.back()==' ') n.pop_back();
    transform(n.begin(), n.end(), n.begin(), ::toupper);
    return (n == "ASC" || n == "DESC") ? n : "INVALID";
}""",
("P029","javascript","correct"): r"""
function validateSortDirection(s) {
    const n = s.trim().toUpperCase();
    return (n === 'ASC' || n === 'DESC') ? n : 'INVALID';
}
module.exports = { validateSortDirection };""",

# ── P030 ──────────────────────────────────────────────────────────────
("P030","python","correct"): r"""
def is_allowed_column(col):
    allowed = {'id','name','email','created_at','status','age','role','score'}
    return col.strip() in allowed
""",
("P030","python","wrong"): "def is_allowed_column(col): return True\n",
("P030","java","correct"): r"""
import java.util.*;
public class Solution {
    private static final Set<String> ALLOWED = new HashSet<>(Arrays.asList(
        "id","name","email","created_at","status","age","role","score"));
    public static boolean isAllowedColumn(String col) {
        return ALLOWED.contains(col.strip());
    }
}""",
("P030","cpp","correct"): r"""
#include <string>
#include <set>
using namespace std;
bool isAllowedColumn(const string& col) {
    static set<string> allowed = {"id","name","email","created_at","status","age","role","score"};
    string s = col;
    while (!s.empty() && s.front()==' ') s.erase(s.begin());
    while (!s.empty() && s.back()==' ') s.pop_back();
    return allowed.count(s) > 0;
}""",
("P030","javascript","correct"): r"""
function isAllowedColumn(col) {
    const allowed = new Set(['id','name','email','created_at','status','age','role','score']);
    return allowed.has(col.trim());
}
module.exports = { isAllowedColumn };""",
}

def main():
    if len(sys.argv) < 4:
        print("Usage: python validate_runner_p021_p030.py <pid> <lang> <variant>")
        sys.exit(2)
    pid, lang, variant = sys.argv[1], sys.argv[2], sys.argv[3]
    key = (pid, lang, variant)
    if key not in SOLUTIONS:
        print(f"SKIP: no solution for {key}")
        sys.exit(0)
    code = SOLUTIONS[key]
    db = sqlite3.connect("database/research.db")
    rows = db.execute(
        "SELECT input, expected_output FROM test_cases WHERE problem_id=? ORDER BY test_case_id",
        (pid,)
    ).fetchall()
    db.close()
    tcs = [{"input": r[0], "expected": r[1]} for r in rows]
    result = execute(lang, code, tcs, "solve", harness_type="typed", problem_id=pid)
    cases = result.get("cases", [])
    status = result.get("status", "ERROR")
    passed  = sum(1 for c in cases if c["status"] == "PASS")
    failed  = sum(1 for c in cases if c["status"] == "FAIL")
    errored = sum(1 for c in cases if c["status"] == "ERROR")
    total   = len(cases)
    expect_pass = (variant == "correct")
    if expect_pass:
        ok = (passed == total and total > 0)
    else:
        ok = (failed > 0 or errored > 0 or status == "ERROR")
    mark = "PASS" if ok else "FAIL"
    print(f"{mark} {pid} [{lang}] {variant}: status={status} {passed}/{total}p {failed}f {errored}e")
    if not ok:
        for c in cases[:3]:
            print(f"  [{c['index']}] {c['status']} actual={repr(c.get('actual','')[:50])} exp={repr(c.get('expected','')[:40])}")
        if result.get("error"):
            print(f"  error: {str(result['error'])[:200]}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
