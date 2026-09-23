"""
Validation for P011-P020 × 4 languages.
Tests: (A) correct -> all 10 PASS, (B) wrong -> at least 1 FAIL, (C) error -> ERROR status
"""
import sys, os, sqlite3
sys.path.insert(0, os.path.dirname(__file__))
from backend.engine.executor import execute

PASS = "✓"; FAIL = "✗"
results = {}

def load_tcs(pid):
    db = sqlite3.connect("database/research.db")
    rows = db.execute("SELECT input, expected_output FROM test_cases WHERE problem_id=? ORDER BY test_case_id", (pid,)).fetchall()
    db.close()
    return [{"input": r[0], "expected": r[1]} for r in rows]

def run(pid, lang, label, code, expect_all_pass):
    tcs = load_tcs(pid)
    r = execute(lang, code, tcs, "solve", harness_type="typed", problem_id=pid)
    cases = r.get("cases", [])
    st = r.get("status")
    passed  = sum(1 for c in cases if c["status"] == "PASS")
    failed  = sum(1 for c in cases if c["status"] == "FAIL")
    errored = sum(1 for c in cases if c["status"] == "ERROR")
    total   = len(cases)
    if expect_all_pass:
        ok = (passed == total and total > 0)
    else:
        ok = (failed > 0 or errored > 0 or st == "ERROR")
    mark = PASS if ok else FAIL
    print(f"  {mark}  [{lang:10}] {label}  status={st}  {passed}/{total}p {failed}f {errored}e")
    if not ok:
        for c in cases[:2]:
            print(f"       case[{c['index']}] {c['status']} actual={str(c.get('actual',''))[:50]} exp={str(c.get('expected',''))[:40]}")
        if r.get("error"): print(f"       err: {str(r['error'])[:200]}")
    results[(pid, lang, label)] = ok

# ── P011 ──────────────────────────────────────────────────────────────────
print("="*65); print("P011 — Email Validator"); print("="*65)
PY_C = """
import re
def is_valid_email(email):
    if not email or '..' in email: return False
    if email.count('@') != 1: return False
    local, domain = email.split('@')
    if not local or local.startswith('.') or local.endswith('.'): return False
    if not re.match(r'^[a-zA-Z0-9._%+\\-]+$', local): return False
    if not domain or domain.startswith('.') or domain.endswith('.'): return False
    labels = domain.split('.')
    if len(labels) < 2: return False
    if not re.match(r'^[a-zA-Z]{2,6}$', labels[-1]): return False
    for lb in labels:
        if not lb or lb.startswith('-') or lb.endswith('-'): return False
        if not re.match(r'^[a-zA-Z0-9\\-]+$', lb): return False
    return True
"""
PY_W = "def is_valid_email(email): return True\n"
PY_E = "def is_valid_email(email): return email[9999]\n"

JAVA_C = """
public class Solution {
    public static boolean isValidEmail(String email) {
        if (email == null || email.isEmpty() || email.contains("..")) return false;
        String[] at = email.split("@", -1);
        if (at.length != 2) return false;
        String local = at[0], domain = at[1];
        if (local.isEmpty() || local.startsWith(".") || local.endsWith(".")) return false;
        if (!local.matches("[a-zA-Z0-9._%+\\\\-]+")) return false;
        if (domain.isEmpty() || domain.startsWith(".") || domain.endsWith(".")) return false;
        String[] labels = domain.split("\\\\.", -1);
        if (labels.length < 2) return false;
        if (!labels[labels.length-1].matches("[a-zA-Z]{2,6}")) return false;
        for (String lb : labels) {
            if (lb.isEmpty() || lb.startsWith("-") || lb.endsWith("-")) return false;
            if (!lb.matches("[a-zA-Z0-9\\\\-]+")) return false;
        }
        return true;
    }
}"""
JAVA_W = "public class Solution { public static boolean isValidEmail(String e) { return true; } }"

CPP_C = r"""
#include <string>
#include <regex>
using namespace std;
bool isValidEmail(const string& email) {
    if (email.empty() || email.find("..") != string::npos) return false;
    size_t at = email.find('@');
    if (at == string::npos || email.find('@', at+1) != string::npos) return false;
    string local = email.substr(0, at), domain = email.substr(at+1);
    if (local.empty() || local.front()=='.' || local.back()=='.') return false;
    if (!regex_match(local, regex("[a-zA-Z0-9._%+\\-]+"))) return false;
    if (domain.empty() || domain.front()=='.' || domain.back()=='.') return false;
    // simple TLD check
    size_t lastDot = domain.rfind('.');
    if (lastDot == string::npos) return false;
    string tld = domain.substr(lastDot+1);
    if (!regex_match(tld, regex("[a-zA-Z]{2,6}"))) return false;
    // label check
    string dom = domain;
    size_t pos = 0;
    while ((pos = dom.find('.')) != string::npos) {
        string lb = dom.substr(0, pos);
        if (lb.empty() || lb.front()=='-' || lb.back()=='-') return false;
        if (!regex_match(lb, regex("[a-zA-Z0-9\\-]+"))) return false;
        dom = dom.substr(pos+1);
    }
    if (dom.empty() || dom.front()=='-' || dom.back()=='-') return false;
    return true;
}"""
CPP_W = "#include <string>\nusing namespace std;\nbool isValidEmail(const string& e) { return true; }"

JS_C = """
function isValidEmail(email) {
    if (!email || email.includes('..')) return false;
    const parts = email.split('@');
    if (parts.length !== 2) return false;
    const [local, domain] = parts;
    if (!local || local.startsWith('.') || local.endsWith('.')) return false;
    if (!/^[a-zA-Z0-9._%+\\-]+$/.test(local)) return false;
    if (!domain || domain.startsWith('.') || domain.endsWith('.')) return false;
    const labels = domain.split('.');
    if (labels.length < 2) return false;
    if (!/^[a-zA-Z]{2,6}$/.test(labels[labels.length-1])) return false;
    for (const lb of labels) {
        if (!lb || lb.startsWith('-') || lb.endsWith('-')) return false;
        if (!/^[a-zA-Z0-9\\-]+$/.test(lb)) return false;
    }
    return true;
}
module.exports = { isValidEmail };"""
JS_W = "function isValidEmail(e){return true;}\nmodule.exports={isValidEmail};"

run("P011","python","correct",PY_C,True); run("P011","python","wrong",PY_W,False); run("P011","python","error",PY_E,False)
run("P011","java","correct",JAVA_C,True); run("P011","java","wrong",JAVA_W,False)
run("P011","cpp","correct",CPP_C,True);   run("P011","cpp","wrong",CPP_W,False)
run("P011","javascript","correct",JS_C,True); run("P011","javascript","wrong",JS_W,False)

# ── P012 ──────────────────────────────────────────────────────────────────
print("\n"+"="*65); print("P012 — Password Policy Validator"); print("="*65)
PY_C = """
import re
def is_valid_password(password):
    if len(password) < 8: return False
    if not re.search(r'[A-Z]', password): return False
    if not re.search(r'[a-z]', password): return False
    if not re.search(r'[0-9]', password): return False
    if not re.search(r'[!@#$%^&*]', password): return False
    return True
"""
JAVA_C = """
public class Solution {
    public static boolean isValidPassword(String pw) {
        if (pw.length() < 8) return false;
        boolean upper=false,lower=false,digit=false,special=false;
        String sp="!@#$%^&*";
        for(char c:pw.toCharArray()){
            if(Character.isUpperCase(c)) upper=true;
            else if(Character.isLowerCase(c)) lower=true;
            else if(Character.isDigit(c)) digit=true;
            else if(sp.indexOf(c)>=0) special=true;
        }
        return upper&&lower&&digit&&special;
    }
}"""
CPP_C = r"""
#include <string>
#include <cctype>
using namespace std;
bool isValidPassword(const string& pw) {
    if (pw.size() < 8) return false;
    bool upper=false,lower=false,digit=false,special=false;
    string sp="!@#$%^&*";
    for(char c:pw){
        if(isupper(c)) upper=true;
        else if(islower(c)) lower=true;
        else if(isdigit(c)) digit=true;
        else if(sp.find(c)!=string::npos) special=true;
    }
    return upper&&lower&&digit&&special;
}"""
JS_C = """
function isValidPassword(pw) {
    if (pw.length < 8) return false;
    if (!/[A-Z]/.test(pw)) return false;
    if (!/[a-z]/.test(pw)) return false;
    if (!/[0-9]/.test(pw)) return false;
    if (!/[!@#$%^&*]/.test(pw)) return false;
    return true;
}
module.exports = { isValidPassword };"""

run("P012","python","correct",PY_C,True); run("P012","python","wrong","def is_valid_password(p): return True\n",False)
run("P012","java","correct",JAVA_C,True)
run("P012","cpp","correct",CPP_C,True)
run("P012","javascript","correct",JS_C,True); run("P012","javascript","wrong","function isValidPassword(p){return true;}\nmodule.exports={isValidPassword};",False)

# ── P013 ──────────────────────────────────────────────────────────────────
print("\n"+"="*65); print("P013 — Integer Range Validator"); print("="*65)
PY_C = """
def is_valid_range(s):
    parts = s.split('|')
    if len(parts) != 3: return "INVALID"
    try:
        val,lo,hi = int(parts[0]),int(parts[1]),int(parts[2])
    except ValueError: return "INVALID"
    return "VALID" if lo <= val <= hi else "INVALID"
"""
JAVA_C = """
public class Solution {
    public static String isValidRange(String s) {
        String[] p = s.split("\\\\|", -1);
        if (p.length != 3) return "INVALID";
        try {
            int val=Integer.parseInt(p[0].trim()),lo=Integer.parseInt(p[1].trim()),hi=Integer.parseInt(p[2].trim());
            return (lo <= val && val <= hi) ? "VALID" : "INVALID";
        } catch (NumberFormatException e) { return "INVALID"; }
    }
}"""
CPP_C = r"""
#include <string>
#include <sstream>
#include <vector>
using namespace std;
string isValidRange(const string& s) {
    vector<string> parts;
    stringstream ss(s); string tok;
    while(getline(ss,tok,'|')) parts.push_back(tok);
    if(parts.size()!=3) return "INVALID";
    try {
        int val=stoi(parts[0]),lo=stoi(parts[1]),hi=stoi(parts[2]);
        return (lo<=val && val<=hi) ? "VALID" : "INVALID";
    } catch(...){ return "INVALID"; }
}"""
JS_C = """
function isValidRange(s) {
    const p = s.split('|');
    if (p.length !== 3) return 'INVALID';
    const [val,lo,hi] = p.map(x => parseInt(x.trim(),10));
    if (isNaN(val)||isNaN(lo)||isNaN(hi)) return 'INVALID';
    return (lo<=val&&val<=hi) ? 'VALID' : 'INVALID';
}
module.exports = { isValidRange };"""

run("P013","python","correct",PY_C,True); run("P013","python","wrong","def is_valid_range(s): return 'VALID'\n",False)
run("P013","java","correct",JAVA_C,True)
run("P013","cpp","correct",CPP_C,True)
run("P013","javascript","correct",JS_C,True)

# ── P014 ──────────────────────────────────────────────────────────────────
print("\n"+"="*65); print("P014 — IPv4 Validator"); print("="*65)
PY_C = """
def is_valid_ipv4(ip):
    parts = ip.split('.')
    if len(parts) != 4: return False
    for p in parts:
        if not p: return False
        if len(p) > 1 and p[0] == '0': return False
        try:
            n = int(p)
        except ValueError: return False
        if n < 0 or n > 255: return False
    return True
"""
JAVA_C = """
public class Solution {
    public static boolean isValidIPv4(String ip) {
        if(ip==null||ip.isEmpty()) return false;
        String[] p=ip.split("\\\\.",-1);
        if(p.length!=4) return false;
        for(String s:p){
            if(s.isEmpty()) return false;
            if(s.length()>1&&s.charAt(0)=='0') return false;
            try{ int n=Integer.parseInt(s); if(n<0||n>255) return false; }
            catch(NumberFormatException e){ return false; }
        }
        return true;
    }
}"""
CPP_C = r"""
#include <string>
#include <vector>
#include <sstream>
using namespace std;
bool isValidIPv4(const string& ip) {
    if(ip.empty()) return false;
    vector<string> parts;
    stringstream ss(ip); string tok;
    while(getline(ss,tok,'.')) parts.push_back(tok);
    if(parts.size()!=4) return false;
    for(auto& p:parts){
        if(p.empty()) return false;
        if(p.size()>1&&p[0]=='0') return false;
        for(char c:p) if(!isdigit(c)) return false;
        int n=stoi(p);
        if(n<0||n>255) return false;
    }
    return true;
}"""
JS_C = """
function isValidIPv4(ip) {
    if(!ip) return false;
    const p = ip.split('.');
    if(p.length!==4) return false;
    for(const s of p){
        if(!s) return false;
        if(s.length>1&&s[0]==='0') return false;
        if(!/^[0-9]+$/.test(s)) return false;
        const n=parseInt(s,10);
        if(n<0||n>255) return false;
    }
    return true;
}
module.exports = { isValidIPv4 };"""

run("P014","python","correct",PY_C,True); run("P014","python","wrong","def is_valid_ipv4(ip): return True\n",False)
run("P014","java","correct",JAVA_C,True)
run("P014","cpp","correct",CPP_C,True)
run("P014","javascript","correct",JS_C,True)

# ── P015 ──────────────────────────────────────────────────────────────────
print("\n"+"="*65); print("P015 — Username Validator"); print("="*65)
PY_C = """
import re
def is_valid_username(username):
    if not username or len(username)<3 or len(username)>20: return False
    if not re.match(r'^[a-zA-Z]', username): return False
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_\\-]*$', username): return False
    return True
"""
JAVA_C = """
public class Solution {
    public static boolean isValidUsername(String u) {
        if(u==null||u.length()<3||u.length()>20) return false;
        if(!Character.isLetter(u.charAt(0))) return false;
        for(char c:u.toCharArray())
            if(!Character.isLetterOrDigit(c)&&c!='_'&&c!='-') return false;
        return true;
    }
}"""
CPP_C = r"""
#include <string>
#include <cctype>
using namespace std;
bool isValidUsername(const string& s) {
    if(s.size()<3||s.size()>20) return false;
    if(!isalpha(s[0])) return false;
    for(char c:s) if(!isalnum(c)&&c!='_'&&c!='-') return false;
    return true;
}"""
JS_C = """
function isValidUsername(u) {
    if(!u||u.length<3||u.length>20) return false;
    if(!/^[a-zA-Z]/.test(u)) return false;
    if(!/^[a-zA-Z][a-zA-Z0-9_\\-]*$/.test(u)) return false;
    return true;
}
module.exports = { isValidUsername };"""

run("P015","python","correct",PY_C,True); run("P015","python","wrong","def is_valid_username(u): return True\n",False)
run("P015","java","correct",JAVA_C,True)
run("P015","cpp","correct",CPP_C,True)
run("P015","javascript","correct",JS_C,True)

# ── P016 ──────────────────────────────────────────────────────────────────
print("\n"+"="*65); print("P016 — HTML Text Escaper"); print("="*65)
PY_C = """
def escape_html(s):
    s=s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    s=s.replace('"','&quot;').replace("'",'&#39;')
    return s
"""
JAVA_C = """
public class Solution {
    public static String escapeHtml(String s) {
        return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                .replace("\\"","&quot;").replace("'","&#39;");
    }
}"""
CPP_C = r"""
#include <string>
using namespace std;
string escapeHtml(const string& s) {
    string r;
    for(char c:s){
        if(c=='&') r+="&amp;";
        else if(c=='<') r+="&lt;";
        else if(c=='>') r+="&gt;";
        else if(c=='"') r+="&quot;";
        else if(c=='\'') r+="&#39;";
        else r+=c;
    }
    return r;
}"""
JS_C = """
function escapeHtml(s) {
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
             .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}
module.exports = { escapeHtml };"""

run("P016","python","correct",PY_C,True); run("P016","python","wrong","def escape_html(s): return s\n",False)
run("P016","java","correct",JAVA_C,True)
run("P016","cpp","correct",CPP_C,True)
run("P016","javascript","correct",JS_C,True); run("P016","javascript","wrong","function escapeHtml(s){return s;}\nmodule.exports={escapeHtml};",False)

# ── P017 ──────────────────────────────────────────────────────────────────
print("\n"+"="*65); print("P017 — CSV Cell Escaper"); print("="*65)
PY_C = """
def escape_csv_cell(s):
    if ',' in s or '"' in s or '\\n' in s or '\\r' in s:
        return '"' + s.replace('"', '""') + '"'
    return s
"""
JAVA_C = r"""
public class Solution {
    public static String escapeCsvCell(String s) {
        if (s.contains(",") || s.contains("\"") || s.contains("\n") || s.contains("\r")) {
            return "\"" + s.replace("\"", "\"\"") + "\"";
        }
        return s;
    }
}"""
CPP_C = r"""
#include <string>
using namespace std;
string escapeCsvCell(const string& s) {
    bool needsQuote = (s.find(',')!=string::npos || s.find('"')!=string::npos ||
                       s.find('\n')!=string::npos || s.find('\r')!=string::npos);
    if (!needsQuote) return s;
    string r = "\"";
    for(char c:s){ if(c=='"') r+="\"\""; else r+=c; }
    r+="\"";
    return r;
}"""
JS_C = r"""
function escapeCsvCell(s) {
    if (s.includes(',') || s.includes('"') || s.includes('\n') || s.includes('\r')) {
        return '"' + s.replace(/"/g, '""') + '"';
    }
    return s;
}
module.exports = { escapeCsvCell };"""

run("P017","python","correct",PY_C,True); run("P017","python","wrong","def escape_csv_cell(s): return s\n",False)
run("P017","java","correct",JAVA_C,True)
run("P017","cpp","correct",CPP_C,True)
run("P017","javascript","correct",JS_C,True)

# ── P018 ──────────────────────────────────────────────────────────────────
print("\n"+"="*65); print("P018 — JSON String Escaper"); print("="*65)
PY_C = r"""
def escape_json_string(s):
    result=[]
    for ch in s:
        if ch=='"':    result.append('\\"')
        elif ch=='\\': result.append('\\\\')
        elif ch=='/':  result.append('\\/')
        elif ch=='\b': result.append('\\b')
        elif ch=='\f': result.append('\\f')
        elif ch=='\n': result.append('\\n')
        elif ch=='\r': result.append('\\r')
        elif ch=='\t': result.append('\\t')
        elif ord(ch)<0x20: result.append(f'\\u{ord(ch):04x}')
        else: result.append(ch)
    return ''.join(result)
"""
JAVA_C = r"""
public class Solution {
    public static String escapeJsonString(String s) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch(c) {
                case '"':  sb.append("\\\""); break;
                case '\\': sb.append("\\\\"); break;
                case '/':  sb.append("\\/"); break;
                case '\b': sb.append("\\b"); break;
                case '\f': sb.append("\\f"); break;
                case '\n': sb.append("\\n"); break;
                case '\r': sb.append("\\r"); break;
                case '\t': sb.append("\\t"); break;
                default:
                    if (c < 0x20) sb.append(String.format("\\u%04x", (int)c));
                    else sb.append(c);
            }
        }
        return sb.toString();
    }
}"""
CPP_C = r"""
#include <string>
#include <sstream>
#include <iomanip>
using namespace std;
string escapeJsonString(const string& s) {
    string r;
    for(unsigned char c:s){
        if(c=='"')       r+="\\\"";
        else if(c=='\\') r+="\\\\";
        else if(c=='/')  r+="\\/";
        else if(c=='\b') r+="\\b";
        else if(c=='\f') r+="\\f";
        else if(c=='\n') r+="\\n";
        else if(c=='\r') r+="\\r";
        else if(c=='\t') r+="\\t";
        else if(c<0x20){ ostringstream os; os<<"\\u"<<setw(4)<<setfill('0')<<hex<<(int)c; r+=os.str(); }
        else r+=c;
    }
    return r;
}"""
JS_C = r"""
function escapeJsonString(s) {
    let r = '';
    for (const ch of s) {
        const code = ch.charCodeAt(0);
        if (ch==='"')       r += '\\"';
        else if (ch==='\\') r += '\\\\';
        else if (ch==='/')  r += '\\/';
        else if (ch==='\b') r += '\\b';
        else if (ch==='\f') r += '\\f';
        else if (ch==='\n') r += '\\n';
        else if (ch==='\r') r += '\\r';
        else if (ch==='\t') r += '\\t';
        else if (code < 0x20) r += '\\u' + code.toString(16).padStart(4,'0');
        else r += ch;
    }
    return r;
}
module.exports = { escapeJsonString };"""

run("P018","python","correct",PY_C,True); run("P018","python","wrong","def escape_json_string(s): return s\n",False)
run("P018","java","correct",JAVA_C,True)
run("P018","cpp","correct",CPP_C,True)
run("P018","javascript","correct",JS_C,True)

# ── P019 ──────────────────────────────────────────────────────────────────
print("\n"+"="*65); print("P019 — URL Query Component Encoder"); print("="*65)
PY_C = r"""
UNRESERVED = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~')
def encode_url_component(s):
    result=[]
    for ch in s:
        if ch in UNRESERVED: result.append(ch)
        else:
            for byte in ch.encode('utf-8'):
                result.append(f'%{byte:02X}')
    return ''.join(result)
"""
JAVA_C = """
public class Solution {
    private static final String UNRESERVED = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~";
    public static String encodeUrlComponent(String s) {
        StringBuilder sb = new StringBuilder();
        try {
            byte[] bytes = s.getBytes("UTF-8");
            for (byte b : bytes) {
                int v = b & 0xFF;
                char c = (char) v;
                if (UNRESERVED.indexOf(c) >= 0) sb.append(c);
                else sb.append(String.format("%%%02X", v));
            }
        } catch (Exception e) {}
        return sb.toString();
    }
}"""
CPP_C = r"""
#include <string>
#include <sstream>
#include <iomanip>
using namespace std;
bool isUnreserved(unsigned char c) {
    return (c>='A'&&c<='Z')||(c>='a'&&c<='z')||(c>='0'&&c<='9')||c=='-'||c=='_'||c=='.'||c=='~';
}
string encodeUrlComponent(const string& s) {
    ostringstream r;
    for(unsigned char c:s){
        if(isUnreserved(c)) r<<c;
        else r<<'%'<<uppercase<<hex<<setw(2)<<setfill('0')<<(int)c;
    }
    return r.str();
}"""
JS_C = r"""
function encodeUrlComponent(s) {
    const unreserved = /^[A-Za-z0-9\-_.~]$/;
    let r = '';
    for (const ch of s) {
        if (unreserved.test(ch)) { r += ch; continue; }
        const bytes = Buffer.from(ch, 'utf8');
        for (const b of bytes) r += '%' + b.toString(16).toUpperCase().padStart(2,'0');
    }
    return r;
}
module.exports = { encodeUrlComponent };"""

run("P019","python","correct",PY_C,True); run("P019","python","wrong","def encode_url_component(s): return s\n",False)
run("P019","java","correct",JAVA_C,True)
run("P019","cpp","correct",CPP_C,True)
run("P019","javascript","correct",JS_C,True)

# ── P020 ──────────────────────────────────────────────────────────────────
print("\n"+"="*65); print("P020 — Template Placeholder Sanitizer"); print("="*65)
PY_C = r"""
import re
def sanitize_template(s):
    def replace(m):
        key = m.group(1)
        return m.group(0) if re.match(r'^[a-zA-Z0-9_]+$', key) else ''
    return re.sub(r'\{\{([^}]*)\}\}', replace, s)
"""
JAVA_C = r"""
import java.util.regex.*;
public class Solution {
    public static String sanitizeTemplate(String s) {
        Pattern p = Pattern.compile("\\{\\{([^}]*)\\}\\}");
        Matcher m = p.matcher(s);
        StringBuffer sb = new StringBuffer();
        while (m.find()) {
            String key = m.group(1);
            if (key.matches("[a-zA-Z0-9_]+")) m.appendReplacement(sb, Matcher.quoteReplacement(m.group(0)));
            else m.appendReplacement(sb, "");
        }
        m.appendTail(sb);
        return sb.toString();
    }
}"""
CPP_C = r"""
#include <string>
#include <regex>
using namespace std;
bool isSafeKey(const string& k) {
    if(k.empty()) return false;
    for(char c:k) if(!isalnum(c)&&c!='_') return false;
    return true;
}
string sanitizeTemplate(const string& s) {
    regex pat("\\{\\{([^}]*)\\}\\}");
    string result;
    auto it = sregex_iterator(s.begin(), s.end(), pat);
    auto end = sregex_iterator();
    size_t lastPos = 0;
    for(auto i=it; i!=end; ++i) {
        smatch m = *i;
        result += s.substr(lastPos, m.position()-lastPos);
        if(isSafeKey(m[1].str())) result += m[0].str();
        lastPos = m.position() + m.length();
    }
    result += s.substr(lastPos);
    return result;
}"""
JS_C = r"""
function sanitizeTemplate(s) {
    return s.replace(/\{\{([^}]*)\}\}/g, (match, key) => /^[a-zA-Z0-9_]+$/.test(key) ? match : '');
}
module.exports = { sanitizeTemplate };"""

run("P020","python","correct",PY_C,True); run("P020","python","wrong","def sanitize_template(s): return s\n",False)
run("P020","java","correct",JAVA_C,True)
run("P020","cpp","correct",CPP_C,True)
run("P020","javascript","correct",JS_C,True); run("P020","javascript","wrong","function sanitizeTemplate(s){return '';}\nmodule.exports={sanitizeTemplate};",False)

# ── SUMMARY ───────────────────────────────────────────────────────────────
total   = len(results)
passed  = sum(1 for v in results.values() if v)
failed  = total - passed
print("\n" + "="*65)
print(f"TOTAL: {total}  PASSED: {passed}  FAILED: {failed}")
if failed:
    print("FAILURES:")
    for (pid,lang,label),ok in results.items():
        if not ok: print(f"  {pid} [{lang}] {label}")
    sys.exit(1)
else:
    print("ALL CHECKS PASSED")
    sys.exit(0)
