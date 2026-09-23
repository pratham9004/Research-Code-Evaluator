"""Validation runner for P041-P050."""
import sys, os, sqlite3, json, re
sys.path.insert(0, os.path.dirname(__file__))
from backend.engine.executor import execute
from collections import Counter

SOLUTIONS = {

# ── P041 ──────────────────────────────────────────────────────────────
("P041","python","correct"): r"""
from collections import Counter
def frequency_counter(nums):
    c = Counter(nums)
    return dict(c)
""",
("P041","python","wrong"): "def frequency_counter(nums): return {}\n",
("P041","java","correct"): r"""
import java.util.*;
public class Solution {
    public static Map<Integer,Integer> frequencyCounter(int[] nums) {
        Map<Integer,Integer> m = new LinkedHashMap<>();
        for (int n : nums) m.put(n, m.getOrDefault(n,0)+1);
        return m;
    }
}""",
("P041","cpp","correct"): r"""
#include <map>
#include <vector>
using namespace std;
map<int,int> frequencyCounter(vector<int>& nums) {
    map<int,int> m;
    for(int n:nums) m[n]++;
    return m;
}""",
("P041","javascript","correct"): r"""
function frequencyCounter(nums) {
    const m={};
    for(const n of nums) m[n]=(m[n]||0)+1;
    return m;
}
module.exports = { frequencyCounter };""",
("P041","javascript","wrong"): "function frequencyCounter(n){return {};}\nmodule.exports={frequencyCounter};",

# ── P042 ──────────────────────────────────────────────────────────────
("P042","python","correct"): r"""
def has_duplicate(nums):
    return len(nums) != len(set(nums))
""",
("P042","python","wrong"): "def has_duplicate(nums): return False\n",
("P042","java","correct"): r"""
import java.util.*;
public class Solution {
    public static boolean hasDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for(int n:nums) if(!seen.add(n)) return true;
        return false;
    }
}""",
("P042","cpp","correct"): r"""
#include <vector>
#include <set>
using namespace std;
bool hasDuplicate(vector<int>& nums) {
    set<int> seen;
    for(int n:nums) if(!seen.insert(n).second) return true;
    return false;
}""",
("P042","javascript","correct"): r"""
function hasDuplicate(nums) {
    return new Set(nums).size !== nums.length;
}
module.exports = { hasDuplicate };""",

# ── P043 ──────────────────────────────────────────────────────────────
("P043","python","correct"): r"""
def streaming_sum(nums):
    return sum(nums)
""",
("P043","python","wrong"): "def streaming_sum(nums): return 0\n",
("P043","java","correct"): r"""
public class Solution {
    public static long streamingSum(int[] nums) {
        long s=0; for(int n:nums) s+=n; return s;
    }
}""",
("P043","cpp","correct"): r"""
#include <vector>
using namespace std;
long long streamingSum(vector<int>& nums) {
    long long s=0; for(int n:nums) s+=n; return s;
}""",
("P043","javascript","correct"): r"""
function streamingSum(nums) {
    return nums.reduce((s,n)=>s+n,0);
}
module.exports = { streamingSum };""",

# ── P044 ──────────────────────────────────────────────────────────────
("P044","python","correct"): r"""
def bounded_log_processor(log, max_lines):
    lines = [l for l in log.split('\n') if l.strip()]
    kept = lines[:max_lines]
    return {"kept": len(kept), "total_words": sum(len(l.split()) for l in kept)}
""",
("P044","python","wrong"): "def bounded_log_processor(log, max_lines): return {'kept':0,'total_words':0}\n",
("P044","java","correct"): r"""
import java.util.*;
public class Solution {
    public static Map<String,Integer> boundedLogProcessor(String log, int maxLines) {
        String[] lines = log.split("\n", -1);
        int kept=0, words=0;
        for(String l : lines) {
            if(l.trim().isEmpty()) continue;
            if(kept >= maxLines) break;
            kept++;
            words += l.trim().split("\\s+").length;
        }
        Map<String,Integer> m=new LinkedHashMap<>();
        m.put("kept",kept); m.put("total_words",words);
        return m;
    }
}""",
("P044","cpp","correct"): r"""
#include <map>
#include <string>
#include <sstream>
using namespace std;
map<string,int> boundedLogProcessor(const string& log, int maxLines) {
    istringstream ss(log); string line;
    int kept=0, words=0;
    while(getline(ss,line)){
        if(line.find_first_not_of(" \t\r")==string::npos) continue;
        if(kept>=maxLines) break;
        kept++;
        istringstream ws(line); string w;
        while(ws>>w) words++;
    }
    map<string,int> m; m["kept"]=kept; m["total_words"]=words;
    return m;
}""",
("P044","javascript","correct"): r"""
function boundedLogProcessor(log, maxLines) {
    const lines = log.split('\n').filter(l=>l.trim());
    const kept = lines.slice(0,maxLines);
    const words = kept.reduce((s,l)=>s+l.trim().split(/\s+/).length,0);
    return {kept:kept.length,total_words:words};
}
module.exports = { boundedLogProcessor };""",

# ── P045 ──────────────────────────────────────────────────────────────
("P045","python","correct"): r"""
from collections import Counter
def top_k_frequent(nums, k):
    if not nums or k <= 0: return []
    c = Counter(nums)
    sorted_keys = sorted(c.keys(), key=lambda x: (-c[x], x))
    return sorted(sorted_keys[:k])
""",
("P045","python","wrong"): "def top_k_frequent(nums, k): return []\n",
("P045","java","correct"): r"""
import java.util.*;
public class Solution {
    public static int[] topKFrequent(int[] nums, int k) {
        if(nums.length==0||k<=0) return new int[]{};
        Map<Integer,Integer> c=new HashMap<>();
        for(int n:nums) c.put(n,c.getOrDefault(n,0)+1);
        List<Integer> keys=new ArrayList<>(c.keySet());
        keys.sort((a,b)->c.get(b).equals(c.get(a))?a-b:c.get(b)-c.get(a));
        int sz=Math.min(k,keys.size());
        int[] res=new int[sz];
        for(int i=0;i<sz;i++) res[i]=keys.get(i);
        Arrays.sort(res);
        return res;
    }
}""",
("P045","cpp","correct"): r"""
#include <vector>
#include <map>
#include <algorithm>
using namespace std;
vector<int> topKFrequent(vector<int>& nums, int k) {
    if(nums.empty()||k<=0) return {};
    map<int,int> c;
    for(int n:nums) c[n]++;
    vector<pair<int,int>> v(c.begin(),c.end());
    sort(v.begin(),v.end(),[](auto&a,auto&b){return a.second!=b.second?a.second>b.second:a.first<b.first;});
    int sz=min(k,(int)v.size());
    vector<int> res;
    for(int i=0;i<sz;i++) res.push_back(v[i].first);
    sort(res.begin(),res.end());
    return res;
}""",
("P045","javascript","correct"): r"""
function topKFrequent(nums, k) {
    if(!nums.length||k<=0) return [];
    const c={};
    for(const n of nums) c[n]=(c[n]||0)+1;
    const keys=Object.keys(c).map(Number);
    keys.sort((a,b)=>c[b]!==c[a]?c[b]-c[a]:a-b);
    return keys.slice(0,k).sort((a,b)=>a-b);
}
module.exports = { topKFrequent };""",

# ── P046 ──────────────────────────────────────────────────────────────
("P046","python","correct"): r"""
import re
def validate_token_format(token):
    if not token: return 'invalid'
    return 'valid' if re.match(r'^[a-zA-Z][a-zA-Z0-9\-]{7,31}$', token) else 'invalid'
""",
("P046","python","wrong"): "def validate_token_format(t): return 'valid'\n",
("P046","java","correct"): r"""
public class Solution {
    public static String validateTokenFormat(String token) {
        if(token==null||token.isEmpty()) return "invalid";
        return token.matches("[a-zA-Z][a-zA-Z0-9\\-]{7,31}") ? "valid" : "invalid";
    }
}""",
("P046","cpp","correct"): r"""
#include <string>
#include <regex>
using namespace std;
string validateTokenFormat(const string& token) {
    if(token.empty()) return "invalid";
    return regex_match(token,regex("[a-zA-Z][a-zA-Z0-9\\-]{7,31}")) ? "valid" : "invalid";
}""",
("P046","javascript","correct"): r"""
function validateTokenFormat(token) {
    if(!token) return 'invalid';
    return /^[a-zA-Z][a-zA-Z0-9\-]{7,31}$/.test(token) ? 'valid' : 'invalid';
}
module.exports = { validateTokenFormat };""",

# ── P047 ──────────────────────────────────────────────────────────────
("P047","python","correct"): r"""
def evaluate_permission(role, action):
    perms={'admin':{'read','write','delete','execute'},'editor':{'read','write'},'viewer':{'read'},'guest':set()}
    return 'allowed' if action in perms.get(role,set()) else 'denied'
""",
("P047","python","wrong"): "def evaluate_permission(r,a): return 'denied'\n",
("P047","java","correct"): r"""
import java.util.*;
public class Solution {
    private static final Map<String,Set<String>> PERMS=new HashMap<>();
    static{
        PERMS.put("admin",new HashSet<>(Arrays.asList("read","write","delete","execute")));
        PERMS.put("editor",new HashSet<>(Arrays.asList("read","write")));
        PERMS.put("viewer",new HashSet<>(Arrays.asList("read")));
        PERMS.put("guest",new HashSet<>());
    }
    public static String evaluatePermission(String role,String action){
        Set<String> p=PERMS.getOrDefault(role,new HashSet<>());
        return p.contains(action)?"allowed":"denied";
    }
}""",
("P047","cpp","correct"): r"""
#include <string>
#include <map>
#include <set>
using namespace std;
string evaluatePermission(const string& role,const string& action){
    static map<string,set<string>> perms={
        {"admin",{"read","write","delete","execute"}},
        {"editor",{"read","write"}},
        {"viewer",{"read"}},
        {"guest",{}}
    };
    auto it=perms.find(role);
    if(it==perms.end()) return "denied";
    return it->second.count(action)?"allowed":"denied";
}""",
("P047","javascript","correct"): r"""
function evaluatePermission(role,action){
    const p={admin:['read','write','delete','execute'],editor:['read','write'],viewer:['read'],guest:[]};
    return (p[role]||[]).includes(action)?'allowed':'denied';
}
module.exports = { evaluatePermission };""",

# ── P048 ──────────────────────────────────────────────────────────────
("P048","python","correct"): r"""
def role_has_permission(role,permission):
    perms={'admin':{'read','write','delete','execute'},'editor':{'read','write'},'viewer':{'read'},'guest':set()}
    return permission in perms.get(role,set())
""",
("P048","python","wrong"): "def role_has_permission(r,p): return False\n",
("P048","java","correct"): r"""
import java.util.*;
public class Solution {
    private static final Map<String,Set<String>> PERMS=new HashMap<>();
    static{
        PERMS.put("admin",new HashSet<>(Arrays.asList("read","write","delete","execute")));
        PERMS.put("editor",new HashSet<>(Arrays.asList("read","write")));
        PERMS.put("viewer",new HashSet<>(Arrays.asList("read")));
        PERMS.put("guest",new HashSet<>());
    }
    public static boolean roleHasPermission(String role,String permission){
        return PERMS.getOrDefault(role,new HashSet<>()).contains(permission);
    }
}""",
("P048","cpp","correct"): r"""
#include <string>
#include <map>
#include <set>
using namespace std;
bool roleHasPermission(const string& role,const string& permission){
    static map<string,set<string>> perms={
        {"admin",{"read","write","delete","execute"}},
        {"editor",{"read","write"}},
        {"viewer",{"read"}},
        {"guest",{}}
    };
    auto it=perms.find(role);
    if(it==perms.end()) return false;
    return it->second.count(permission)>0;
}""",
("P048","javascript","correct"): r"""
function roleHasPermission(role,permission){
    const p={admin:['read','write','delete','execute'],editor:['read','write'],viewer:['read'],guest:[]};
    return (p[role]||[]).includes(permission);
}
module.exports = { roleHasPermission };""",

# ── P049 ──────────────────────────────────────────────────────────────
("P049","python","correct"): r"""
def check_session(last_active,current_time,timeout):
    if current_time < last_active: return 'invalid'
    return 'expired' if (current_time-last_active) > timeout else 'active'
""",
("P049","python","wrong"): "def check_session(a,b,c): return 'active'\n",
("P049","java","correct"): r"""
public class Solution {
    public static String checkSession(int lastActive,int currentTime,int timeout){
        if(currentTime<lastActive) return "invalid";
        return (currentTime-lastActive)>timeout?"expired":"active";
    }
}""",
("P049","cpp","correct"): r"""
#include <string>
using namespace std;
string checkSession(int lastActive,int currentTime,int timeout){
    if(currentTime<lastActive) return "invalid";
    return (currentTime-lastActive)>timeout?"expired":"active";
}""",
("P049","javascript","correct"): r"""
function checkSession(lastActive,currentTime,timeout){
    if(currentTime<lastActive) return 'invalid';
    return (currentTime-lastActive)>timeout?'expired':'active';
}
module.exports = { checkSession };""",

# ── P050 ──────────────────────────────────────────────────────────────
("P050","python","correct"): r"""
def validate_scope(requested,allowed):
    if requested in allowed: return 'granted'
    parts=requested.split(':')
    for i in range(1,len(parts)):
        if ':'.join(parts[:i]) in allowed: return 'granted'
    return 'denied'
""",
("P050","python","wrong"): "def validate_scope(r,a): return 'denied'\n",
("P050","java","correct"): r"""
import java.util.*;
public class Solution {
    public static String validateScope(String requested,List<String> allowed){
        if(allowed.contains(requested)) return "granted";
        String[] parts=requested.split(":",-1);
        for(int i=1;i<parts.length;i++){
            String parent=String.join(":",Arrays.copyOf(parts,i));
            if(allowed.contains(parent)) return "granted";
        }
        return "denied";
    }
}""",
("P050","cpp","correct"): r"""
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>
using namespace std;
string validateScope(const string& requested,vector<string>& allowed){
    if(find(allowed.begin(),allowed.end(),requested)!=allowed.end()) return "granted";
    vector<string> parts; stringstream ss(requested); string tok;
    while(getline(ss,tok,':')) parts.push_back(tok);
    for(size_t i=1;i<parts.size();i++){
        string parent=parts[0];
        for(size_t j=1;j<i;j++) parent+=":"+parts[j];
        if(find(allowed.begin(),allowed.end(),parent)!=allowed.end()) return "granted";
    }
    return "denied";
}""",
("P050","javascript","correct"): r"""
function validateScope(requested,allowed){
    if(allowed.includes(requested)) return 'granted';
    const parts=requested.split(':');
    for(let i=1;i<parts.length;i++){
        const parent=parts.slice(0,i).join(':');
        if(allowed.includes(parent)) return 'granted';
    }
    return 'denied';
}
module.exports = { validateScope };""",
}

def main():
    if len(sys.argv) < 4:
        print("Usage: python validate_runner_p041_p050.py <pid> <lang> <variant>"); sys.exit(2)
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
    st = result.get("status", "ERROR")
    passed  = sum(1 for c in cases if c["status"] == "PASS")
    failed  = sum(1 for c in cases if c["status"] == "FAIL")
    errored = sum(1 for c in cases if c["status"] == "ERROR")
    total   = len(cases)
    expect_pass = (variant == "correct")
    ok = (passed == total and total > 0) if expect_pass else (failed > 0 or errored > 0 or st == "ERROR")
    mark = "PASS" if ok else "FAIL"
    print(f"{mark} {pid} [{lang}] {variant}: {st} {passed}/{total}p {failed}f {errored}e")
    if not ok:
        for c in cases[:3]:
            print(f"  [{c['index']}] {c['status']} actual={repr(str(c.get('actual',''))[:60])} exp={repr(str(c.get('expected',''))[:50])}")
        if result.get("error"): print(f"  error: {str(result['error'])[:200]}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
