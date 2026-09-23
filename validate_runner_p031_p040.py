"""
Validation runner for P031-P040.
Usage: python validate_runner_p031_p040.py <pid> <lang> <variant>
variant: correct | wrong | error
"""
import sys, os, sqlite3, re, json
sys.path.insert(0, os.path.dirname(__file__))
from backend.engine.executor import execute

SOLUTIONS = {

# ── P031 ──────────────────────────────────────────────────────────────
("P031","python","correct"): r"""
def quote_shell_arg(s):
    return "'" + s.replace("'", "'\\''") + "'"
""",
("P031","python","wrong"): "def quote_shell_arg(s): return s\n",
("P031","java","correct"): r"""
public class Solution {
    public static String quoteShellArg(String s) {
        return "'" + s.replace("'", "'\\''") + "'";
    }
}""",
("P031","cpp","correct"): r"""
#include <string>
using namespace std;
string quoteShellArg(const string& s) {
    string r = "'";
    for (char c : s) {
        if (c == '\'') r += "'\\''";
        else r += c;
    }
    r += "'";
    return r;
}""",
("P031","javascript","correct"): r"""
function quoteShellArg(s) {
    return "'" + s.replace(/'/g, "'\\''") + "'";
}
module.exports = { quoteShellArg };""",
("P031","javascript","wrong"): "function quoteShellArg(s){return s;}\nmodule.exports={quoteShellArg};",

# ── P032 ──────────────────────────────────────────────────────────────
("P032","python","correct"): r"""
def is_allowed_command(s):
    allowed = {'ls','cat','echo','grep','find','sort','uniq','wc','head','tail'}
    return s.strip() in allowed
""",
("P032","python","wrong"): "def is_allowed_command(s): return True\n",
("P032","java","correct"): r"""
import java.util.*;
public class Solution {
    private static final Set<String> ALLOWED = new HashSet<>(Arrays.asList(
        "ls","cat","echo","grep","find","sort","uniq","wc","head","tail"));
    public static boolean isAllowedCommand(String s) {
        return ALLOWED.contains(s.strip());
    }
}""",
("P032","cpp","correct"): r"""
#include <string>
#include <set>
using namespace std;
bool isAllowedCommand(const string& s) {
    static set<string> a={"ls","cat","echo","grep","find","sort","uniq","wc","head","tail"};
    string t=s;
    while(!t.empty()&&t.front()==' ')t.erase(t.begin());
    while(!t.empty()&&t.back()==' ')t.pop_back();
    return a.count(t)>0;
}""",
("P032","javascript","correct"): r"""
function isAllowedCommand(s) {
    const a=new Set(['ls','cat','echo','grep','find','sort','uniq','wc','head','tail']);
    return a.has(s.trim());
}
module.exports = { isAllowedCommand };""",

# ── P033 ──────────────────────────────────────────────────────────────
("P033","python","correct"): r"""
def detect_shell_meta(s):
    dangerous = set(';|&$`><(){}"\'\\' + '\n\r')
    for ch in s:
        if ch in dangerous:
            return "unsafe"
    return "safe"
""",
("P033","python","wrong"): "def detect_shell_meta(s): return 'safe'\n",
("P033","java","correct"): r"""
public class Solution {
    private static final String DANGEROUS = ";|&$`><(){}\"\'\\\n\r";
    public static String detectShellMeta(String s) {
        for (char c : s.toCharArray())
            if (DANGEROUS.indexOf(c) >= 0) return "unsafe";
        return "safe";
    }
}""",
("P033","cpp","correct"): r"""
#include <string>
using namespace std;
string detectShellMeta(const string& s) {
    string d = ";|&$`><(){}\"'\\\n\r";
    for(char c:s) if(d.find(c)!=string::npos) return "unsafe";
    return "safe";
}""",
("P033","javascript","correct"): r"""
function detectShellMeta(s) {
    const dangerous = new Set([';','|','&','$','`','>','<','(',')','{'  ,'}','"',"'",'\\','\n','\r']);
    for (const ch of s) if (dangerous.has(ch)) return 'unsafe';
    return 'safe';
}
module.exports = { detectShellMeta };""",

# ── P034 ──────────────────────────────────────────────────────────────
("P034","python","correct"): r"""
import re
def is_valid_env_var(name):
    if not name or len(name) > 64: return False
    return bool(re.match(r'^[A-Z_][A-Z0-9_]*$', name))
""",
("P034","python","wrong"): "def is_valid_env_var(name): return True\n",
("P034","java","correct"): r"""
public class Solution {
    public static boolean isValidEnvVar(String name) {
        if (name == null || name.isEmpty() || name.length() > 64) return false;
        return name.matches("[A-Z_][A-Z0-9_]*");
    }
}""",
("P034","cpp","correct"): r"""
#include <string>
#include <cctype>
using namespace std;
bool isValidEnvVar(const string& name) {
    if (name.empty() || name.size()>64) return false;
    if (!isupper(name[0]) && name[0]!='_') return false;
    for (char c:name) if (!isupper(c) && !isdigit(c) && c!='_') return false;
    return true;
}""",
("P034","javascript","correct"): r"""
function isValidEnvVar(name) {
    if (!name || name.length > 64) return false;
    return /^[A-Z_][A-Z0-9_]*$/.test(name);
}
module.exports = { isValidEnvVar };""",

# ── P035 ──────────────────────────────────────────────────────────────
("P035","python","correct"): r"""
def split_args(s):
    tokens = []
    current = []
    in_quote = False
    started = False
    for ch in s:
        if ch == '"' and not in_quote:
            in_quote = True; started = True
        elif ch == '"' and in_quote:
            in_quote = False
        elif ch == ' ' and not in_quote:
            if started:
                tokens.append(''.join(current)); current = []; started = False
        else:
            current.append(ch); started = True
    if started:
        tokens.append(''.join(current))
    return tokens
""",
("P035","python","wrong"): "def split_args(s): return []\n",
("P035","java","correct"): r"""
import java.util.*;
public class Solution {
    public static List<String> splitArgs(String s) {
        List<String> tokens = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        boolean inQ = false, started = false;
        for (char c : s.toCharArray()) {
            if (c == '"' && !inQ) { inQ = true; started = true; }
            else if (c == '"' && inQ) { inQ = false; }
            else if (c == ' ' && !inQ) {
                if (started) { tokens.add(cur.toString()); cur = new StringBuilder(); started = false; }
            } else { cur.append(c); started = true; }
        }
        if (started) tokens.add(cur.toString());
        return tokens;
    }
}""",
("P035","cpp","correct"): r"""
#include <vector>
#include <string>
using namespace std;
vector<string> splitArgs(const string& s) {
    vector<string> tokens;
    string cur;
    bool inQ=false, started=false;
    for (char c:s) {
        if(c=='"'&&!inQ){inQ=true;started=true;}
        else if(c=='"'&&inQ){inQ=false;}
        else if(c==' '&&!inQ){if(started){tokens.push_back(cur);cur="";started=false;}}
        else{cur+=c;started=true;}
    }
    if(started) tokens.push_back(cur);
    return tokens;
}""",
("P035","javascript","correct"): r"""
function splitArgs(s) {
    const tokens=[];
    let cur='', inQ=false, started=false;
    for(const ch of s){
        if(ch==='"'&&!inQ){inQ=true;started=true;}
        else if(ch==='"'&&inQ){inQ=false;}
        else if(ch===' '&&!inQ){if(started){tokens.push(cur);cur='';started=false;}}
        else{cur+=ch;started=true;}
    }
    if(started) tokens.push(cur);
    return tokens;
}
module.exports = { splitArgs };""",

# ── P036 ──────────────────────────────────────────────────────────────
("P036","python","correct"): r"""
import re
def parse_safe_literal(s):
    s = s.strip()
    if not s: return "INVALID"
    if s == "null": return "null"
    if s == "true": return "true"
    if s == "false": return "false"
    if re.match(r'^-?[0-9]+$', s): return str(int(s))
    if s.startswith('"') and s.endswith('"') and len(s)>=2:
        inner=s[1:-1]; i=0; result=[]
        while i<len(inner):
            if inner[i]=='\\'  and i+1<len(inner) and inner[i+1]=='"':
                result.append('"'); i+=2
            elif inner[i]=='"': return "INVALID"
            else: result.append(inner[i]); i+=1
        return ''.join(result)
    return "INVALID"
""",
("P036","python","wrong"): "def parse_safe_literal(s): return 'INVALID'\n",
("P036","java","correct"): r"""
public class Solution {
    public static String parseSafeLiteral(String s) {
        s = s.trim();
        if (s.isEmpty()) return "INVALID";
        if (s.equals("null")) return "null";
        if (s.equals("true")) return "true";
        if (s.equals("false")) return "false";
        if (s.matches("-?[0-9]+")) return String.valueOf(Integer.parseInt(s));
        if (s.startsWith("\"") && s.endsWith("\"") && s.length()>=2) {
            String inner = s.substring(1,s.length()-1);
            StringBuilder sb = new StringBuilder();
            int i=0;
            while(i<inner.length()){
                if(inner.charAt(i)=='\\' && i+1<inner.length() && inner.charAt(i+1)=='"'){
                    sb.append('"'); i+=2;
                } else if(inner.charAt(i)=='"') return "INVALID";
                else sb.append(inner.charAt(i++));
            }
            return sb.toString();
        }
        return "INVALID";
    }
}""",
("P036","cpp","correct"): r"""
#include <string>
#include <regex>
using namespace std;
string parseSafeLiteral(const string& raw) {
    string s=raw;
    while(!s.empty()&&s.front()==' ')s.erase(s.begin());
    while(!s.empty()&&s.back()==' ')s.pop_back();
    if(s.empty()) return "INVALID";
    if(s=="null") return "null";
    if(s=="true") return "true";
    if(s=="false") return "false";
    if(regex_match(s,regex("-?[0-9]+"))) return to_string(stol(s));
    if(s.front()=='"'&&s.back()=='"'&&s.size()>=2){
        string inner=s.substr(1,s.size()-2); string res; size_t i=0;
        while(i<inner.size()){
            if(inner[i]=='\\'&&i+1<inner.size()&&inner[i+1]=='"'){res+='"';i+=2;}
            else if(inner[i]=='"') return "INVALID";
            else res+=inner[i++];
        }
        return res;
    }
    return "INVALID";
}""",
("P036","javascript","correct"): r"""
function parseSafeLiteral(s) {
    s = s.trim();
    if (!s) return 'INVALID';
    if (s === 'null') return 'null';
    if (s === 'true') return 'true';
    if (s === 'false') return 'false';
    if (/^-?[0-9]+$/.test(s)) return String(parseInt(s, 10));
    if (s.startsWith('"') && s.endsWith('"') && s.length >= 2) {
        const inner = s.slice(1, -1);
        let res = '', i = 0;
        while (i < inner.length) {
            if (inner[i] === '\\' && i+1 < inner.length && inner[i+1] === '"') {
                res += '"'; i += 2;
            } else if (inner[i] === '"') return 'INVALID';
            else res += inner[i++];
        }
        return res;
    }
    return 'INVALID';
}
module.exports = { parseSafeLiteral };""",

# ── P037 ──────────────────────────────────────────────────────────────
("P037","python","correct"): r"""
def parse_config_bool(s):
    n = s.strip().lower()
    if n in {'true','yes','1','on','enabled'}: return 'true'
    if n in {'false','no','0','off','disabled'}: return 'false'
    return 'INVALID'
""",
("P037","python","wrong"): "def parse_config_bool(s): return 'true'\n",
("P037","java","correct"): r"""
import java.util.*;
public class Solution {
    private static final Set<String> T=new HashSet<>(Arrays.asList("true","yes","1","on","enabled"));
    private static final Set<String> F=new HashSet<>(Arrays.asList("false","no","0","off","disabled"));
    public static String parseConfigBool(String s) {
        String n=s.strip().toLowerCase();
        if(T.contains(n)) return "true";
        if(F.contains(n)) return "false";
        return "INVALID";
    }
}""",
("P037","cpp","correct"): r"""
#include <string>
#include <set>
#include <algorithm>
using namespace std;
string parseConfigBool(const string& s) {
    string n=s;
    while(!n.empty()&&n.front()==' ')n.erase(n.begin());
    while(!n.empty()&&n.back()==' ')n.pop_back();
    transform(n.begin(),n.end(),n.begin(),::tolower);
    static set<string> T={"true","yes","1","on","enabled"};
    static set<string> F={"false","no","0","off","disabled"};
    if(T.count(n)) return "true";
    if(F.count(n)) return "false";
    return "INVALID";
}""",
("P037","javascript","correct"): r"""
function parseConfigBool(s) {
    const n=s.trim().toLowerCase();
    if(['true','yes','1','on','enabled'].includes(n)) return 'true';
    if(['false','no','0','off','disabled'].includes(n)) return 'false';
    return 'INVALID';
}
module.exports = { parseConfigBool };""",

# ── P038 ──────────────────────────────────────────────────────────────
("P038","python","correct"): r"""
def is_allowed_config_key(key):
    allowed={'host','port','database','username','password','timeout',
             'max_connections','ssl_enabled','log_level','retry_count'}
    return key.strip() in allowed
""",
("P038","python","wrong"): "def is_allowed_config_key(key): return True\n",
("P038","java","correct"): r"""
import java.util.*;
public class Solution {
    private static final Set<String> ALLOWED=new HashSet<>(Arrays.asList(
        "host","port","database","username","password","timeout",
        "max_connections","ssl_enabled","log_level","retry_count"));
    public static boolean isAllowedConfigKey(String key) {
        return ALLOWED.contains(key.strip());
    }
}""",
("P038","cpp","correct"): r"""
#include <string>
#include <set>
using namespace std;
bool isAllowedConfigKey(const string& key) {
    static set<string> a={"host","port","database","username","password","timeout",
        "max_connections","ssl_enabled","log_level","retry_count"};
    string s=key;
    while(!s.empty()&&s.front()==' ')s.erase(s.begin());
    while(!s.empty()&&s.back()==' ')s.pop_back();
    return a.count(s)>0;
}""",
("P038","javascript","correct"): r"""
function isAllowedConfigKey(key) {
    const a=new Set(['host','port','database','username','password','timeout',
        'max_connections','ssl_enabled','log_level','retry_count']);
    return a.has(key.trim());
}
module.exports = { isAllowedConfigKey };""",

# ── P039 ──────────────────────────────────────────────────────────────
("P039","python","correct"): r"""
import re
def validate_token(s):
    parts = s.split('.')
    if len(parts) != 3: return 'invalid'
    h,p,c = parts
    if not h or not re.match(r'^[A-Za-z0-9_\-]+$', h): return 'invalid'
    if not p or not re.match(r'^[A-Za-z0-9_\-]+$', p): return 'invalid'
    if not re.match(r'^[0-9a-f]{8}$', c): return 'invalid'
    return 'valid'
""",
("P039","python","wrong"): "def validate_token(s): return 'valid'\n",
("P039","java","correct"): r"""
public class Solution {
    public static String validateToken(String s) {
        String[] p=s.split("\\.",-1);
        if(p.length!=3) return "invalid";
        if(p[0].isEmpty()||!p[0].matches("[A-Za-z0-9_\\-]+")) return "invalid";
        if(p[1].isEmpty()||!p[1].matches("[A-Za-z0-9_\\-]+")) return "invalid";
        if(!p[2].matches("[0-9a-f]{8}")) return "invalid";
        return "valid";
    }
}""",
("P039","cpp","correct"): r"""
#include <string>
#include <regex>
using namespace std;
string validateToken(const string& s) {
    vector<string> parts; string tok; istringstream ss(s);
    // split on dot
    #include <sstream>
    return ""; // placeholder — use proper split below
}""",
# C++ clean version without nested include:
("P039","cpp","correct"): r"""
#include <string>
#include <vector>
#include <sstream>
#include <regex>
using namespace std;
string validateToken(const string& s) {
    vector<string> parts;
    stringstream ss(s); string tok;
    while(getline(ss,tok,'.')) parts.push_back(tok);
    if(parts.size()!=3) return "invalid";
    if(parts[0].empty()||!regex_match(parts[0],regex("[A-Za-z0-9_\\-]+"))) return "invalid";
    if(parts[1].empty()||!regex_match(parts[1],regex("[A-Za-z0-9_\\-]+"))) return "invalid";
    if(!regex_match(parts[2],regex("[0-9a-f]{8}"))) return "invalid";
    return "valid";
}""",
("P039","javascript","correct"): r"""
function validateToken(s) {
    const p=s.split('.');
    if(p.length!==3) return 'invalid';
    if(!p[0]||!/^[A-Za-z0-9_\-]+$/.test(p[0])) return 'invalid';
    if(!p[1]||!/^[A-Za-z0-9_\-]+$/.test(p[1])) return 'invalid';
    if(!/^[0-9a-f]{8}$/.test(p[2])) return 'invalid';
    return 'valid';
}
module.exports = { validateToken };""",

# ── P040 ──────────────────────────────────────────────────────────────
("P040","python","correct"): r"""
import re
def validate_numeric_expr(s):
    s=s.strip()
    if not s: return 'invalid'
    pattern = r'^-?(?:0|[1-9][0-9]*)(?:\s*[+\-*/]\s*-?(?:0|[1-9][0-9]*))*$'
    return 'valid' if re.match(pattern,s) else 'invalid'
""",
("P040","python","wrong"): "def validate_numeric_expr(s): return 'valid'\n",
("P040","java","correct"): r"""
public class Solution {
    public static String validateNumericExpr(String s) {
        s=s.trim();
        if(s.isEmpty()) return "invalid";
        if(!s.matches("-?(?:0|[1-9][0-9]*)(?:\\s*[+\\-*/]\\s*-?(?:0|[1-9][0-9]*))*"))
            return "invalid";
        return "valid";
    }
}""",
("P040","cpp","correct"): r"""
#include <string>
#include <regex>
using namespace std;
string validateNumericExpr(const string& raw) {
    string s=raw;
    while(!s.empty()&&s.front()==' ')s.erase(s.begin());
    while(!s.empty()&&s.back()==' ')s.pop_back();
    if(s.empty()) return "invalid";
    regex pat("-?(?:0|[1-9][0-9]*)(?:\\s*[+\\-*/]\\s*-?(?:0|[1-9][0-9]*))*");
    return regex_match(s,pat) ? "valid" : "invalid";
}""",
("P040","javascript","correct"): r"""
function validateNumericExpr(s) {
    s=s.trim();
    if(!s) return 'invalid';
    const p=/^-?(?:0|[1-9][0-9]*)(?:\s*[+\-*/]\s*-?(?:0|[1-9][0-9]*))*$/;
    return p.test(s) ? 'valid' : 'invalid';
}
module.exports = { validateNumericExpr };""",
}

def main():
    if len(sys.argv) < 4:
        print("Usage: python validate_runner_p031_p040.py <pid> <lang> <variant>"); sys.exit(2)
    pid, lang, variant = sys.argv[1], sys.argv[2], sys.argv[3]
    key = (pid, lang, variant)
    if key not in SOLUTIONS:
        print(f"SKIP: no solution for {key}"); sys.exit(0)
    code = SOLUTIONS[key]
    db = sqlite3.connect("database/research.db")
    rows = db.execute("SELECT input, expected_output FROM test_cases WHERE problem_id=? ORDER BY test_case_id", (pid,)).fetchall()
    db.close()
    tcs = [{"input": r[0], "expected": r[1]} for r in rows]
    result = execute(lang, code, tcs, "solve", harness_type="typed", problem_id=pid)
    cases = result.get("cases", [])
    st = result.get("status","ERROR")
    passed = sum(1 for c in cases if c["status"]=="PASS")
    failed = sum(1 for c in cases if c["status"]=="FAIL")
    errored= sum(1 for c in cases if c["status"]=="ERROR")
    total  = len(cases)
    expect_pass = (variant == "correct")
    ok = (passed == total and total > 0) if expect_pass else (failed > 0 or errored > 0 or st == "ERROR")
    mark = "PASS" if ok else "FAIL"
    print(f"{mark} {pid} [{lang}] {variant}: {st} {passed}/{total}p {failed}f {errored}e")
    if not ok:
        for c in cases[:3]:
            print(f"  [{c['index']}] {c['status']} actual={repr(str(c.get('actual',''))[:50])} exp={repr(str(c.get('expected',''))[:40])}")
        if result.get("error"): print(f"  error: {str(result['error'])[:200]}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
