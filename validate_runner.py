"""Run validation for a single problem+language combination.
Called by the master validation script as a subprocess to isolate C++ AppControl issues.
Usage: python validate_runner.py <problem_id> <language> <variant>
variant: correct | wrong | error
"""
import sys, os, sqlite3, json
sys.path.insert(0, os.path.dirname(__file__))
from backend.engine.executor import execute

SOLUTIONS = {
# ── P001 ──
("P001","python","correct"): '''
def two_sum(nums, target):
    seen = {}
    for i, v in enumerate(nums):
        if target - v in seen:
            return [seen[target-v], i]
        seen[v] = i
    return []
''',
("P001","python","wrong"): "def two_sum(nums, target):\n    return [0, 0]\n",
("P001","python","error"):  "def two_sum(nums, target):\n    return nums[999]\n",
("P001","java","correct"): """
import java.util.*;
public class Solution {
    public static int[] twoSum(int[] nums, int target) {
        Map<Integer,Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int comp = target - nums[i];
            if (map.containsKey(comp)) return new int[]{map.get(comp), i};
            map.put(nums[i], i);
        }
        return new int[]{};
    }
}""",
("P001","java","wrong"): "public class Solution { public static int[] twoSum(int[] n, int t) { return new int[]{0,0}; } }",
("P001","java","error"): "public class Solution { public static int[] twoSum(int[] n, int t) { return new int[]{n[999]}; } }",
("P001","cpp","correct"): r"""
#include <vector>
#include <unordered_map>
using namespace std;
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int,int> m;
    for (int i = 0; i < (int)nums.size(); i++) {
        int c = target - nums[i];
        if (m.count(c)) return {m[c], i};
        m[nums[i]] = i;
    }
    return {};
}""",
("P001","cpp","wrong"): "#include <vector>\nusing namespace std;\nvector<int> twoSum(vector<int>& n, int t) { return {0,0}; }",
("P001","javascript","correct"): """function twoSum(nums, target) {
    const map = {};
    for (let i = 0; i < nums.length; i++) {
        const c = target - nums[i];
        if (c in map) return [map[c], i];
        map[nums[i]] = i;
    }
    return [];
}
module.exports = { twoSum };""",
("P001","javascript","wrong"): "function twoSum(n, t) { return [0, 0]; }\nmodule.exports = { twoSum };",

# ── P002 ──
("P002","python","correct"): """
def max_subarray(nums):
    best = cur = nums[0]
    for n in nums[1:]:
        cur = max(n, cur + n)
        best = max(best, cur)
    return best
""",
("P002","python","wrong"): "def max_subarray(nums): return 0\n",
("P002","java","correct"): """
public class Solution {
    public static int maxSubarray(int[] nums) {
        int best = nums[0], cur = nums[0];
        for (int i=1;i<nums.length;i++){cur=Math.max(nums[i],cur+nums[i]);best=Math.max(best,cur);}
        return best;
    }
}""",
("P002","cpp","correct"): r"""
#include <vector>
#include <algorithm>
using namespace std;
int maxSubarray(vector<int>& nums) {
    int best=nums[0],cur=nums[0];
    for(int i=1;i<(int)nums.size();i++){cur=max(nums[i],cur+nums[i]);best=max(best,cur);}
    return best;
}""",
("P002","javascript","correct"): """function maxSubarray(nums) {
    let best=nums[0],cur=nums[0];
    for(let i=1;i<nums.length;i++){cur=Math.max(nums[i],cur+nums[i]);best=Math.max(best,cur);}
    return best;
}
module.exports = { maxSubarray };""",
("P002","javascript","wrong"): "function maxSubarray(n){return 0;}\nmodule.exports={maxSubarray};",

# ── P003 ──
("P003","python","correct"): """
def binary_search(nums, target):
    lo, hi = 0, len(nums)-1
    while lo <= hi:
        mid = (lo+hi)//2
        if nums[mid]==target: return mid
        elif nums[mid]<target: lo=mid+1
        else: hi=mid-1
    return -1
""",
("P003","python","wrong"): "def binary_search(n,t): return -1\n",
("P003","java","correct"): """
public class Solution {
    public static int binarySearch(int[] nums, int target) {
        int lo=0,hi=nums.length-1;
        while(lo<=hi){int mid=(lo+hi)/2;if(nums[mid]==target)return mid;else if(nums[mid]<target)lo=mid+1;else hi=mid-1;}
        return -1;
    }
}""",
("P003","cpp","correct"): r"""
#include <vector>
using namespace std;
int binarySearch(vector<int>& nums, int target) {
    int lo=0,hi=(int)nums.size()-1;
    while(lo<=hi){int mid=(lo+hi)/2;if(nums[mid]==target)return mid;else if(nums[mid]<target)lo=mid+1;else hi=mid-1;}
    return -1;
}""",
("P003","javascript","correct"): """function binarySearch(nums, target) {
    let lo=0,hi=nums.length-1;
    while(lo<=hi){const mid=(lo+hi)>>1;if(nums[mid]===target)return mid;else if(nums[mid]<target)lo=mid+1;else hi=mid-1;}
    return -1;
}
module.exports = { binarySearch };""",

# ── P004 ──
("P004","python","correct"): """
def merge_sorted_arrays(nums1, nums2):
    res=[]
    i=j=0
    while i<len(nums1) and j<len(nums2):
        if nums1[i]<=nums2[j]: res.append(nums1[i]); i+=1
        else: res.append(nums2[j]); j+=1
    return res+nums1[i:]+nums2[j:]
""",
("P004","python","wrong"): "def merge_sorted_arrays(a,b): return []\n",
("P004","java","correct"): """
public class Solution {
    public static int[] mergeSortedArrays(int[] a, int[] b) {
        int[] res=new int[a.length+b.length]; int i=0,j=0,k=0;
        while(i<a.length&&j<b.length) res[k++]=(a[i]<=b[j])?a[i++]:b[j++];
        while(i<a.length) res[k++]=a[i++];
        while(j<b.length) res[k++]=b[j++];
        return res;
    }
}""",
("P004","cpp","correct"): r"""
#include <vector>
using namespace std;
vector<int> mergeSortedArrays(vector<int>& a, vector<int>& b) {
    vector<int> res; int i=0,j=0;
    while(i<(int)a.size()&&j<(int)b.size()){if(a[i]<=b[j])res.push_back(a[i++]);else res.push_back(b[j++]);}
    while(i<(int)a.size()) res.push_back(a[i++]);
    while(j<(int)b.size()) res.push_back(b[j++]);
    return res;
}""",
("P004","javascript","correct"): """function mergeSortedArrays(a, b) {
    const res=[]; let i=0,j=0;
    while(i<a.length&&j<b.length) res.push(a[i]<=b[j]?a[i++]:b[j++]);
    while(i<a.length) res.push(a[i++]);
    while(j<b.length) res.push(b[j++]);
    return res;
}
module.exports = { mergeSortedArrays };""",

# ── P005 ──
("P005","python","correct"): """
def is_balanced(s):
    stack=[]
    m={'(':')','[':']','{':'}'}
    for c in s:
        if c in m: stack.append(m[c])
        elif c in ')]}':
            if not stack or stack[-1]!=c: return False
            stack.pop()
    return not stack
""",
("P005","python","wrong"): "def is_balanced(s): return True\n",
("P005","java","correct"): """
import java.util.*;
public class Solution {
    public static boolean isBalanced(String s) {
        Deque<Character> stack=new ArrayDeque<>();
        for(char c:s.toCharArray()){
            if(c=='('||c=='['||c=='{') stack.push(c=='('?')':c=='['?']':'}');
            else if(c==')'||c==']'||c=='}'){if(stack.isEmpty()||stack.pop()!=c)return false;}
        }
        return stack.isEmpty();
    }
}""",
("P005","cpp","correct"): r"""
#include <string>
#include <stack>
using namespace std;
bool isBalanced(const string& s) {
    stack<char> st;
    for(char c:s){
        if(c=='('||c=='['||c=='{') st.push(c=='('?')':c=='['?']':'}');
        else if(c==')'||c==']'||c=='}'){if(st.empty()||st.top()!=c)return false;st.pop();}
    }
    return st.empty();
}""",
("P005","javascript","correct"): """function isBalanced(s) {
    const stack=[], m={'(':')','{':'}','[':']'};
    for(const c of s){
        if(m[c]) stack.push(m[c]);
        else if(')}]'.includes(c)){if(stack.pop()!==c)return false;}
    }
    return stack.length===0;
}
module.exports = { isBalanced };""",
("P005","javascript","wrong"): "function isBalanced(s){return false;}\nmodule.exports={isBalanced};",

# ── P006 ──
("P006","python","correct"): """
def csv_field_count(line):
    count=1; in_q=False
    for c in line:
        if c=='"': in_q=not in_q
        elif c==',' and not in_q: count+=1
    return count
""",
("P006","python","wrong"): "def csv_field_count(line): return 0\n",
("P006","java","correct"): """
public class Solution {
    public static int csvFieldCount(String line) {
        int count=1; boolean inQ=false;
        for(char c:line.toCharArray()){
            if(c=='"') inQ=!inQ;
            else if(c==','&&!inQ) count++;
        }
        return count;
    }
}""",
("P006","cpp","correct"): r"""
#include <string>
using namespace std;
int csvFieldCount(const string& line) {
    int count=1; bool inQ=false;
    for(char c:line){if(c=='"')inQ=!inQ;else if(c==','&&!inQ)count++;}
    return count;
}""",
("P006","javascript","correct"): """function csvFieldCount(line) {
    let count=1, inQ=false;
    for(const c of line){if(c==='"')inQ=!inQ;else if(c===','&&!inQ)count++;}
    return count;
}
module.exports = { csvFieldCount };""",

# ── P007 ──
("P007","python","correct"): """
def count_log_levels(log):
    counts={"ERROR":0,"WARNING":0,"INFO":0,"DEBUG":0}
    for line in log.splitlines():
        for lvl in counts:
            if line.startswith(lvl): counts[lvl]+=1; break
    return counts
""",
("P007","python","wrong"): "def count_log_levels(log): return {}\n",
("P007","java","correct"): """
import java.util.*;
public class Solution {
    public static Map<String,Integer> countLogLevels(String log) {
        Map<String,Integer> m=new LinkedHashMap<>();
        m.put("ERROR",0);m.put("WARNING",0);m.put("INFO",0);m.put("DEBUG",0);
        for(String line:log.split("\\\\n",-1)){
            for(String lvl:m.keySet()){if(line.startsWith(lvl)){m.put(lvl,m.get(lvl)+1);break;}}
        }
        return m;
    }
}""",
("P007","cpp","correct"): r"""
#include <map>
#include <string>
#include <sstream>
using namespace std;
map<string,int> countLogLevels(const string& log) {
    map<string,int> m={{"ERROR",0},{"WARNING",0},{"INFO",0},{"DEBUG",0}};
    istringstream ss(log); string line;
    while(getline(ss,line)){
        for(auto& kv:m) if(line.substr(0,kv.first.size())==kv.first){kv.second++;break;}
    }
    return m;
}""",
("P007","javascript","correct"): """function countLogLevels(log) {
    const counts={ERROR:0,WARNING:0,INFO:0,DEBUG:0};
    for(const line of log.split('\\n')){
        for(const lvl of Object.keys(counts)){if(line.startsWith(lvl)){counts[lvl]++;break;}}
    }
    return counts;
}
module.exports = { countLogLevels };""",

# ── P008 ──
("P008","python","correct"): """
def parse_key_value(s):
    if not s.strip(): return {}
    result={}
    for pair in s.split(','):
        if '=' in pair:
            k,v=pair.split('=',1)
            result[k.strip()]=v.strip()
    return result
""",
("P008","python","wrong"): "def parse_key_value(s): return {}\n",
("P008","java","correct"): """
import java.util.*;
public class Solution {
    public static Map<String,String> parseKeyValue(String s) {
        Map<String,String> m=new LinkedHashMap<>();
        if(s.trim().isEmpty()) return m;
        for(String pair:s.split(",")){
            int eq=pair.indexOf('=');
            if(eq>=0) m.put(pair.substring(0,eq).trim(),pair.substring(eq+1).trim());
        }
        return m;
    }
}""",
("P008","cpp","correct"): r"""
#include <map>
#include <string>
#include <sstream>
using namespace std;
map<string,string> parseKeyValue(const string& s) {
    map<string,string> m;
    if(s.empty()) return m;
    istringstream ss(s); string tok;
    while(getline(ss,tok,',')){
        auto eq=tok.find('=');
        if(eq!=string::npos){
            string k=tok.substr(0,eq),v=tok.substr(eq+1);
            while(!k.empty()&&k.front()==' ')k.erase(k.begin());
            while(!k.empty()&&k.back()==' ')k.pop_back();
            while(!v.empty()&&v.front()==' ')v.erase(v.begin());
            while(!v.empty()&&v.back()==' ')v.pop_back();
            m[k]=v;
        }
    }
    return m;
}""",
("P008","javascript","correct"): """function parseKeyValue(s) {
    const res={};
    if(!s.trim()) return res;
    for(const pair of s.split(',')){
        const eq=pair.indexOf('=');
        if(eq>=0) res[pair.slice(0,eq).trim()]=pair.slice(eq+1).trim();
    }
    return res;
}
module.exports = { parseKeyValue };""",

# ── P009 ──
("P009","python","correct"): r"""
import re
def normalize_date(date):
    date=date.strip()
    if re.match(r'\d{2}/\d{2}/\d{4}',date):
        m,d,y=date.split('/')
        return f'{y}-{m}-{d}'
    elif re.match(r'\d{2}-\d{2}-\d{4}',date):
        d,m,y=date.split('-')
        return f'{y}-{m}-{d}'
    elif re.match(r'\d{4}\.\d{2}\.\d{2}',date):
        y,m,d=date.split('.')
        return f'{y}-{m}-{d}'
    return date
""",
("P009","python","wrong"): "def normalize_date(d): return d\n",
("P009","java","correct"): r"""
public class Solution {
    public static String normalizeDate(String date) {
        date=date.trim();
        if(date.matches("\\d{2}/\\d{2}/\\d{4}")){
            String[]p=date.split("/"); return p[2]+"-"+p[0]+"-"+p[1];
        } else if(date.matches("\\d{2}-\\d{2}-\\d{4}")){
            String[]p=date.split("-"); return p[2]+"-"+p[1]+"-"+p[0];
        } else if(date.matches("\\d{4}\\.\\d{2}\\.\\d{2}")){
            String[]p=date.split("\\."); return p[0]+"-"+p[1]+"-"+p[2];
        }
        return date;
    }
}""",
("P009","cpp","correct"): r"""
#include <string>
using namespace std;
string normalizeDate(const string& date) {
    if(date.size()==10 && date[2]=='/') return date.substr(6,4)+"-"+date.substr(0,2)+"-"+date.substr(3,2);
    if(date.size()==10 && date[2]=='-') return date.substr(6,4)+"-"+date.substr(3,2)+"-"+date.substr(0,2);
    if(date.size()==10 && date[4]=='.') return date.substr(0,4)+"-"+date.substr(5,2)+"-"+date.substr(8,2);
    return date;
}""",
("P009","javascript","correct"): r"""function normalizeDate(date) {
    date=date.trim();
    if(/^\d{2}\/\d{2}\/\d{4}$/.test(date)){const[m,d,y]=date.split('/');return `${y}-${m}-${d}`;}
    if(/^\d{2}-\d{2}-\d{4}$/.test(date)){const[d,m,y]=date.split('-');return `${y}-${m}-${d}`;}
    if(/^\d{4}\.\d{2}\.\d{2}$/.test(date)){const[y,m,d]=date.split('.');return `${y}-${m}-${d}`;}
    return date;
}
module.exports = { normalizeDate };""",

# ── P010 ──
("P010","python","correct"): r"""
import re
def word_frequency(text):
    words=re.findall(r'[a-zA-Z]+',text.lower())
    freq={}
    for w in words: freq[w]=freq.get(w,0)+1
    return freq
""",
("P010","python","wrong"): "def word_frequency(text): return {}\n",
("P010","java","correct"): """
import java.util.*;
import java.util.regex.*;
public class Solution {
    public static Map<String,Integer> wordFrequency(String text) {
        Map<String,Integer> m=new LinkedHashMap<>();
        Matcher mat=Pattern.compile("[a-zA-Z]+").matcher(text.toLowerCase());
        while(mat.find()){String w=mat.group();m.put(w,m.getOrDefault(w,0)+1);}
        return m;
    }
}""",
("P010","cpp","correct"): r"""
#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include <cctype>
using namespace std;
vector<pair<string,int>> wordFrequency(const string& text) {
    map<string,int> freq;
    string word;
    for(char c:text){
        if(isalpha(c)) word+=tolower(c);
        else if(!word.empty()){freq[word]++;word="";}
    }
    if(!word.empty()) freq[word]++;
    vector<pair<string,int>> res(freq.begin(),freq.end());
    sort(res.begin(),res.end(),[](auto&a,auto&b){return a.second!=b.second?a.second>b.second:a.first<b.first;});
    return res;
}""",
("P010","javascript","correct"): """function wordFrequency(text) {
    const words=text.toLowerCase().match(/[a-zA-Z]+/g)||[];
    const freq={};
    for(const w of words) freq[w]=(freq[w]||0)+1;
    return freq;
}
module.exports = { wordFrequency };""",
("P010","javascript","wrong"): "function wordFrequency(t){return {};}\nmodule.exports={wordFrequency};",
}

def main():
    if len(sys.argv) < 4:
        print("Usage: python validate_runner.py <pid> <lang> <variant>")
        sys.exit(2)
    pid, lang, variant = sys.argv[1], sys.argv[2], sys.argv[3]
    key = (pid, lang, variant)
    if key not in SOLUTIONS:
        print(f"SKIP: no solution defined for {key}")
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
    passed = sum(1 for c in cases if c["status"] == "PASS")
    failed = sum(1 for c in cases if c["status"] == "FAIL")
    errored= sum(1 for c in cases if c["status"] == "ERROR")
    total  = len(cases)
    expect_all_pass = (variant == "correct")
    if expect_all_pass:
        ok = passed == total and total > 0
    else:
        ok = (failed > 0 or errored > 0 or status == "ERROR")
    mark = "PASS" if ok else "FAIL"
    print(f"{mark} {pid} [{lang}] {variant}: status={status} {passed}/{total}p {failed}f {errored}e")
    if not ok:
        for c in cases[:3]:
            print(f"  case[{c['index']}] {c['status']} actual={str(c.get('actual',''))[:60]} exp={str(c.get('expected',''))[:40]}")
        if result.get("error"):
            print(f"  error: {str(result['error'])[:300]}")
    sys.exit(0 if ok else 1)

# ── P011-P020 solutions appended ─────────────────────────────────────────
SOLUTIONS.update({

# ── P011 ──
("P011","python","correct"): r"""
import re
def is_valid_email(email):
    if not email or '..' in email: return False
    if email.count('@') != 1: return False
    local, domain = email.split('@')
    if not local or local.startswith('.') or local.endswith('.'): return False
    if not re.match(r'^[a-zA-Z0-9._%+\-]+$', local): return False
    if not domain or domain.startswith('.') or domain.endswith('.'): return False
    labels = domain.split('.')
    if len(labels) < 2: return False
    if not re.match(r'^[a-zA-Z]{2,6}$', labels[-1]): return False
    for lb in labels:
        if not lb or lb.startswith('-') or lb.endswith('-'): return False
        if not re.match(r'^[a-zA-Z0-9\-]+$', lb): return False
    return True
""",
("P011","python","wrong"): "def is_valid_email(email): return True\n",
("P011","python","error"):  "def is_valid_email(email): return email[9999]\n",
("P011","java","correct"): r"""
public class Solution {
    public static boolean isValidEmail(String email) {
        if (email == null || email.isEmpty() || email.contains("..")) return false;
        String[] at = email.split("@", -1);
        if (at.length != 2) return false;
        String local = at[0], domain = at[1];
        if (local.isEmpty() || local.startsWith(".") || local.endsWith(".")) return false;
        if (!local.matches("[a-zA-Z0-9._%+\\-]+")) return false;
        if (domain.isEmpty() || domain.startsWith(".") || domain.endsWith(".")) return false;
        String[] labels = domain.split("\\.", -1);
        if (labels.length < 2) return false;
        if (!labels[labels.length-1].matches("[a-zA-Z]{2,6}")) return false;
        for (String lb : labels) {
            if (lb.isEmpty() || lb.startsWith("-") || lb.endsWith("-")) return false;
            if (!lb.matches("[a-zA-Z0-9\\-]+")) return false;
        }
        return true;
    }
}""",
("P011","java","wrong"): "public class Solution { public static boolean isValidEmail(String e) { return true; } }",
("P011","cpp","correct"): r"""
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
    size_t lastDot = domain.rfind('.');
    if (lastDot == string::npos) return false;
    string tld = domain.substr(lastDot+1);
    if (!regex_match(tld, regex("[a-zA-Z]{2,6}"))) return false;
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
}""",
("P011","cpp","wrong"): "#include <string>\nusing namespace std;\nbool isValidEmail(const string& e) { return true; }",
("P011","javascript","correct"): r"""
function isValidEmail(email) {
    if (!email || email.includes('..')) return false;
    const parts = email.split('@');
    if (parts.length !== 2) return false;
    const [local, domain] = parts;
    if (!local || local.startsWith('.') || local.endsWith('.')) return false;
    if (!/^[a-zA-Z0-9._%+\-]+$/.test(local)) return false;
    if (!domain || domain.startsWith('.') || domain.endsWith('.')) return false;
    const labels = domain.split('.');
    if (labels.length < 2) return false;
    if (!/^[a-zA-Z]{2,6}$/.test(labels[labels.length-1])) return false;
    for (const lb of labels) {
        if (!lb || lb.startsWith('-') || lb.endsWith('-')) return false;
        if (!/^[a-zA-Z0-9\-]+$/.test(lb)) return false;
    }
    return true;
}
module.exports = { isValidEmail };""",
("P011","javascript","wrong"): "function isValidEmail(e){return true;}\nmodule.exports={isValidEmail};",

# ── P012 ──
("P012","python","correct"): r"""
import re
def is_valid_password(password):
    if len(password) < 8: return False
    if not re.search(r'[A-Z]', password): return False
    if not re.search(r'[a-z]', password): return False
    if not re.search(r'[0-9]', password): return False
    if not re.search(r'[!@#$%^&*]', password): return False
    return True
""",
("P012","python","wrong"): "def is_valid_password(p): return True\n",
("P012","java","correct"): r"""
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
}""",
("P012","cpp","correct"): r"""
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
}""",
("P012","javascript","correct"): r"""
function isValidPassword(pw) {
    if (pw.length < 8) return false;
    if (!/[A-Z]/.test(pw)) return false;
    if (!/[a-z]/.test(pw)) return false;
    if (!/[0-9]/.test(pw)) return false;
    if (!/[!@#$%^&*]/.test(pw)) return false;
    return true;
}
module.exports = { isValidPassword };""",
("P012","javascript","wrong"): "function isValidPassword(p){return true;}\nmodule.exports={isValidPassword};",

# ── P013 ──
("P013","python","correct"): r"""
def is_valid_range(s):
    parts = s.split('|')
    if len(parts) != 3: return "INVALID"
    try:
        val,lo,hi = int(parts[0]),int(parts[1]),int(parts[2])
    except ValueError: return "INVALID"
    return "VALID" if lo <= val <= hi else "INVALID"
""",
("P013","python","wrong"): "def is_valid_range(s): return 'VALID'\n",
("P013","java","correct"): r"""
public class Solution {
    public static String isValidRange(String s) {
        String[] p = s.split("\\|", -1);
        if (p.length != 3) return "INVALID";
        try {
            int val=Integer.parseInt(p[0].trim()),lo=Integer.parseInt(p[1].trim()),hi=Integer.parseInt(p[2].trim());
            return (lo <= val && val <= hi) ? "VALID" : "INVALID";
        } catch (NumberFormatException e) { return "INVALID"; }
    }
}""",
("P013","cpp","correct"): r"""
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
}""",
("P013","javascript","correct"): r"""
function isValidRange(s) {
    const p = s.split('|');
    if (p.length !== 3) return 'INVALID';
    const [val,lo,hi] = p.map(x => parseInt(x.trim(),10));
    if (isNaN(val)||isNaN(lo)||isNaN(hi)) return 'INVALID';
    return (lo<=val&&val<=hi) ? 'VALID' : 'INVALID';
}
module.exports = { isValidRange };""",

# ── P014 ──
("P014","python","correct"): r"""
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
""",
("P014","python","wrong"): "def is_valid_ipv4(ip): return True\n",
("P014","java","correct"): r"""
public class Solution {
    public static boolean isValidIPv4(String ip) {
        if(ip==null||ip.isEmpty()) return false;
        String[] p=ip.split("\\.",-1);
        if(p.length!=4) return false;
        for(String s:p){
            if(s.isEmpty()) return false;
            if(s.length()>1&&s.charAt(0)=='0') return false;
            try{ int n=Integer.parseInt(s); if(n<0||n>255) return false; }
            catch(NumberFormatException e){ return false; }
        }
        return true;
    }
}""",
("P014","cpp","correct"): r"""
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
}""",
("P014","javascript","correct"): r"""
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
module.exports = { isValidIPv4 };""",

# ── P015 ──
("P015","python","correct"): r"""
import re
def is_valid_username(username):
    if not username or len(username)<3 or len(username)>20: return False
    if not re.match(r'^[a-zA-Z]', username): return False
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_\-]*$', username): return False
    return True
""",
("P015","python","wrong"): "def is_valid_username(u): return True\n",
("P015","java","correct"): r"""
public class Solution {
    public static boolean isValidUsername(String u) {
        if(u==null||u.length()<3||u.length()>20) return false;
        if(!Character.isLetter(u.charAt(0))) return false;
        for(char c:u.toCharArray())
            if(!Character.isLetterOrDigit(c)&&c!='_'&&c!='-') return false;
        return true;
    }
}""",
("P015","cpp","correct"): r"""
#include <string>
#include <cctype>
using namespace std;
bool isValidUsername(const string& s) {
    if(s.size()<3||s.size()>20) return false;
    if(!isalpha(s[0])) return false;
    for(char c:s) if(!isalnum(c)&&c!='_'&&c!='-') return false;
    return true;
}""",
("P015","javascript","correct"): r"""
function isValidUsername(u) {
    if(!u||u.length<3||u.length>20) return false;
    if(!/^[a-zA-Z]/.test(u)) return false;
    if(!/^[a-zA-Z][a-zA-Z0-9_\-]*$/.test(u)) return false;
    return true;
}
module.exports = { isValidUsername };""",

# ── P016 ──
("P016","python","correct"): r"""
def escape_html(s):
    s=s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    s=s.replace('"','&quot;').replace("'",'&#39;')
    return s
""",
("P016","python","wrong"): "def escape_html(s): return s\n",
("P016","java","correct"): r"""
public class Solution {
    public static String escapeHtml(String s) {
        return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                .replace("\"","&quot;").replace("'","&#39;");
    }
}""",
("P016","cpp","correct"): r"""
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
}""",
("P016","javascript","correct"): r"""
function escapeHtml(s) {
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
             .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}
module.exports = { escapeHtml };""",
("P016","javascript","wrong"): "function escapeHtml(s){return s;}\nmodule.exports={escapeHtml};",

# ── P017 ──
("P017","python","correct"): r"""
def escape_csv_cell(s):
    if ',' in s or '"' in s or '\n' in s or '\r' in s:
        return '"' + s.replace('"', '""') + '"'
    return s
""",
("P017","python","wrong"): "def escape_csv_cell(s): return s\n",
("P017","java","correct"): r"""
public class Solution {
    public static String escapeCsvCell(String s) {
        if (s.contains(",") || s.contains("\"") || s.contains("\n") || s.contains("\r")) {
            return "\"" + s.replace("\"", "\"\"") + "\"";
        }
        return s;
    }
}""",
("P017","cpp","correct"): r"""
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
}""",
("P017","javascript","correct"): r"""
function escapeCsvCell(s) {
    if (s.includes(',') || s.includes('"') || s.includes('\n') || s.includes('\r')) {
        return '"' + s.replace(/"/g, '""') + '"';
    }
    return s;
}
module.exports = { escapeCsvCell };""",

# ── P018 ──
("P018","python","correct"): r"""
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
""",
("P018","python","wrong"): "def escape_json_string(s): return s\n",
("P018","java","correct"): r"""
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
}""",
("P018","cpp","correct"): r"""
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
}""",
("P018","javascript","correct"): r"""
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
module.exports = { escapeJsonString };""",

# ── P019 ──
("P019","python","correct"): r"""
UNRESERVED = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~')
def encode_url_component(s):
    result=[]
    for ch in s:
        if ch in UNRESERVED: result.append(ch)
        else:
            for byte in ch.encode('utf-8'):
                result.append(f'%{byte:02X}')
    return ''.join(result)
""",
("P019","python","wrong"): "def encode_url_component(s): return s\n",
("P019","java","correct"): r"""
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
}""",
("P019","cpp","correct"): r"""
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
}""",
("P019","javascript","correct"): r"""
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
module.exports = { encodeUrlComponent };""",

# ── P020 ──
("P020","python","correct"): r"""
import re
def sanitize_template(s):
    def replace(m):
        key = m.group(1)
        return m.group(0) if re.match(r'^[a-zA-Z0-9_]+$', key) else ''
    return re.sub(r'\{\{([^}]*)\}\}', replace, s)
""",
("P020","python","wrong"): "def sanitize_template(s): return ''\n",
("P020","java","correct"): r"""
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
}""",
("P020","cpp","correct"): r"""
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
}""",
("P020","javascript","correct"): r"""
function sanitizeTemplate(s) {
    return s.replace(/\{\{([^}]*)\}\}/g, (match, key) => /^[a-zA-Z0-9_]+$/.test(key) ? match : '');
}
module.exports = { sanitizeTemplate };""",
("P020","javascript","wrong"): "function sanitizeTemplate(s){return '';}\nmodule.exports={sanitizeTemplate};",
})

if __name__ == "__main__":
    main()
