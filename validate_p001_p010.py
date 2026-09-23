"""
Validation script for P001-P010 across all 4 languages.
Tests:  (A) correct implementation  -> all PASS
        (B) wrong implementation     -> at least one FAIL
        (C) syntax/compile error     -> ERROR status

Run from repo root:
    python validate_p001_p010.py
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(__file__))

from backend.engine.executor import execute

PASS_MARK = "✓"
FAIL_MARK = "✗"
WARN_MARK = "⚠"

results = {}   # (pid, lang, variant) -> ok:bool

def run(pid, lang, label, code, expect_all_pass):
    db_pid_map = {
        "P001":"P001","P002":"P002","P003":"P003","P004":"P004","P005":"P005",
        "P006":"P006","P007":"P007","P008":"P008","P009":"P009","P010":"P010",
    }
    # Load test cases from the live database
    import sqlite3, json
    db = sqlite3.connect("database/research.db")
    rows = db.execute(
        "SELECT input, expected_output FROM test_cases WHERE problem_id=? ORDER BY test_case_id",
        (pid,)
    ).fetchall()
    db.close()
    tcs = [{"input": r[0], "expected": r[1]} for r in rows]

    result = execute(lang, code, tcs, "solve",
                     harness_type="typed", problem_id=pid)
    cases  = result.get("cases", [])
    status = result.get("status")
    passed = sum(1 for c in cases if c["status"] == "PASS")
    failed = sum(1 for c in cases if c["status"] == "FAIL")
    errored= sum(1 for c in cases if c["status"] == "ERROR")
    total  = len(cases)

    if expect_all_pass:
        ok = passed == total and total > 0
    else:
        # wrong or error code: at least one non-PASS
        ok = (failed > 0 or errored > 0 or status == "ERROR")

    mark = PASS_MARK if ok else FAIL_MARK
    print(f"  {mark}  [{lang.upper():10}] {label}")
    print(f"       status={status}  {passed}/{total} pass  {failed} fail  {errored} err")
    if not ok:
        for c in cases[:3]:
            print(f"       case[{c['index']}] {c['status']}  actual={str(c.get('actual',''))[:60]}  expected={str(c.get('expected',''))[:40]}")
        if result.get("error"):
            print(f"       error: {str(result['error'])[:200]}")
    results[(pid, lang, label)] = ok
    if lang == "cpp":
        time.sleep(0.5)   # brief pause between C++ runs to avoid AppControl timing issues
    return ok


# =============================================================================
# P001 — Two Sum
# =============================================================================
print("="*65); print("P001 — Two Sum"); print("="*65)

PY_CORRECT = """
def two_sum(nums, target):
    seen = {}
    for i, v in enumerate(nums):
        if target - v in seen:
            return [seen[target-v], i]
        seen[v] = i
    return []
"""
PY_WRONG = """
def two_sum(nums, target):
    return [0, 0]
"""
PY_ERROR = """
def two_sum(nums, target):
    return nums[999]
"""

run("P001","python","Correct",PY_CORRECT,True)
run("P001","python","Wrong",  PY_WRONG,  False)
run("P001","python","Error",  PY_ERROR,  False)

JAVA_CORRECT = """
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
}
"""
JAVA_WRONG = """
public class Solution {
    public static int[] twoSum(int[] nums, int target) {
        return new int[]{0, 0};
    }
}
"""
JAVA_ERROR = """
public class Solution {
    public static int[] twoSum(int[] nums, int target) {
        return new int[]{nums[999]};
    }
}
"""
run("P001","java","Correct",JAVA_CORRECT,True)
run("P001","java","Wrong",  JAVA_WRONG,  False)
run("P001","java","Error",  JAVA_ERROR,  False)

CPP_CORRECT = """
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
}
"""
CPP_WRONG = """
#include <vector>
using namespace std;
vector<int> twoSum(vector<int>& nums, int target) { return {0,0}; }
"""
run("P001","cpp","Correct",CPP_CORRECT,True)
run("P001","cpp","Wrong",  CPP_WRONG,  False)

JS_CORRECT = """
function twoSum(nums, target) {
    const map = {};
    for (let i = 0; i < nums.length; i++) {
        const c = target - nums[i];
        if (c in map) return [map[c], i];
        map[nums[i]] = i;
    }
    return [];
}
module.exports = { twoSum };
"""
JS_WRONG = """
function twoSum(nums, target) { return [0, 0]; }
module.exports = { twoSum };
"""
run("P001","javascript","Correct",JS_CORRECT,True)
run("P001","javascript","Wrong",  JS_WRONG,  False)


# =============================================================================
# P002 — Maximum Subarray Sum
# =============================================================================
print("\n"+"="*65); print("P002 — Maximum Subarray Sum"); print("="*65)

PY_CORRECT = """
def max_subarray(nums):
    best = cur = nums[0]
    for n in nums[1:]:
        cur = max(n, cur + n)
        best = max(best, cur)
    return best
"""
run("P002","python","Correct",PY_CORRECT,True)
run("P002","python","Wrong",  "def max_subarray(nums): return 0",False)

JAVA_CORRECT = """
public class Solution {
    public static int maxSubarray(int[] nums) {
        int best = nums[0], cur = nums[0];
        for (int i=1;i<nums.length;i++){cur=Math.max(nums[i],cur+nums[i]);best=Math.max(best,cur);}
        return best;
    }
}
"""
run("P002","java","Correct",JAVA_CORRECT,True)

CPP_CORRECT = """
#include <vector>
#include <algorithm>
using namespace std;
int maxSubarray(vector<int>& nums) {
    int best=nums[0],cur=nums[0];
    for(int i=1;i<(int)nums.size();i++){cur=max(nums[i],cur+nums[i]);best=max(best,cur);}
    return best;
}
"""
run("P002","cpp","Correct",CPP_CORRECT,True)

JS_CORRECT = """
function maxSubarray(nums) {
    let best=nums[0],cur=nums[0];
    for(let i=1;i<nums.length;i++){cur=Math.max(nums[i],cur+nums[i]);best=Math.max(best,cur);}
    return best;
}
module.exports = { maxSubarray };
"""
run("P002","javascript","Correct",JS_CORRECT,True)
run("P002","javascript","Wrong","function maxSubarray(n){return 0;}\nmodule.exports={maxSubarray};",False)


# =============================================================================
# P003 — Binary Search
# =============================================================================
print("\n"+"="*65); print("P003 — Binary Search"); print("="*65)

PY_CORRECT = """
def binary_search(nums, target):
    lo, hi = 0, len(nums)-1
    while lo <= hi:
        mid = (lo+hi)//2
        if nums[mid]==target: return mid
        elif nums[mid]<target: lo=mid+1
        else: hi=mid-1
    return -1
"""
run("P003","python","Correct",PY_CORRECT,True)
run("P003","python","Wrong","def binary_search(n,t): return -1",False)

JAVA_CORRECT = """
public class Solution {
    public static int binarySearch(int[] nums, int target) {
        int lo=0,hi=nums.length-1;
        while(lo<=hi){int mid=(lo+hi)/2;if(nums[mid]==target)return mid;else if(nums[mid]<target)lo=mid+1;else hi=mid-1;}
        return -1;
    }
}
"""
run("P003","java","Correct",JAVA_CORRECT,True)

CPP_CORRECT = """
#include <vector>
using namespace std;
int binarySearch(vector<int>& nums, int target) {
    int lo=0,hi=(int)nums.size()-1;
    while(lo<=hi){int mid=(lo+hi)/2;if(nums[mid]==target)return mid;else if(nums[mid]<target)lo=mid+1;else hi=mid-1;}
    return -1;
}
"""
run("P003","cpp","Correct",CPP_CORRECT,True)

JS_CORRECT = """
function binarySearch(nums, target) {
    let lo=0,hi=nums.length-1;
    while(lo<=hi){const mid=(lo+hi)>>1;if(nums[mid]===target)return mid;else if(nums[mid]<target)lo=mid+1;else hi=mid-1;}
    return -1;
}
module.exports = { binarySearch };
"""
run("P003","javascript","Correct",JS_CORRECT,True)


# =============================================================================
# P004 — Merge Sorted Arrays
# =============================================================================
print("\n"+"="*65); print("P004 — Merge Sorted Arrays"); print("="*65)

PY_CORRECT = """
def merge_sorted_arrays(nums1, nums2):
    res=[]
    i=j=0
    while i<len(nums1) and j<len(nums2):
        if nums1[i]<=nums2[j]: res.append(nums1[i]); i+=1
        else: res.append(nums2[j]); j+=1
    return res+nums1[i:]+nums2[j:]
"""
run("P004","python","Correct",PY_CORRECT,True)
run("P004","python","Wrong","def merge_sorted_arrays(a,b): return []",False)

JAVA_CORRECT = """
public class Solution {
    public static int[] mergeSortedArrays(int[] a, int[] b) {
        int[] res=new int[a.length+b.length]; int i=0,j=0,k=0;
        while(i<a.length&&j<b.length) res[k++]=(a[i]<=b[j])?a[i++]:b[j++];
        while(i<a.length) res[k++]=a[i++];
        while(j<b.length) res[k++]=b[j++];
        return res;
    }
}
"""
run("P004","java","Correct",JAVA_CORRECT,True)

CPP_CORRECT = """
#include <vector>
using namespace std;
vector<int> mergeSortedArrays(vector<int>& a, vector<int>& b) {
    vector<int> res; int i=0,j=0;
    while(i<(int)a.size()&&j<(int)b.size()){if(a[i]<=b[j])res.push_back(a[i++]);else res.push_back(b[j++]);}
    while(i<(int)a.size()) res.push_back(a[i++]);
    while(j<(int)b.size()) res.push_back(b[j++]);
    return res;
}
"""
run("P004","cpp","Correct",CPP_CORRECT,True)

JS_CORRECT = """
function mergeSortedArrays(a, b) {
    const res=[]; let i=0,j=0;
    while(i<a.length&&j<b.length) res.push(a[i]<=b[j]?a[i++]:b[j++]);
    while(i<a.length) res.push(a[i++]);
    while(j<b.length) res.push(b[j++]);
    return res;
}
module.exports = { mergeSortedArrays };
"""
run("P004","javascript","Correct",JS_CORRECT,True)


# =============================================================================
# P005 — Balanced Brackets
# =============================================================================
print("\n"+"="*65); print("P005 — Balanced Brackets"); print("="*65)

PY_CORRECT = """
def is_balanced(s):
    stack=[]
    m={'(':')','[':']','{':'}'}
    for c in s:
        if c in m: stack.append(m[c])
        elif c in ')]}':
            if not stack or stack[-1]!=c: return False
            stack.pop()
    return not stack
"""
run("P005","python","Correct",PY_CORRECT,True)
run("P005","python","Wrong","def is_balanced(s): return True",False)

JAVA_CORRECT = """
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
}
"""
run("P005","java","Correct",JAVA_CORRECT,True)

CPP_CORRECT = """
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
}
"""
run("P005","cpp","Correct",CPP_CORRECT,True)

JS_CORRECT = """
function isBalanced(s) {
    const stack=[], m={'(':')','{':'}','[':']'};
    for(const c of s){
        if(m[c]) stack.push(m[c]);
        else if(')}]'.includes(c)){if(stack.pop()!==c)return false;}
    }
    return stack.length===0;
}
module.exports = { isBalanced };
"""
run("P005","javascript","Correct",JS_CORRECT,True)
run("P005","javascript","Wrong","function isBalanced(s){return false;}\nmodule.exports={isBalanced};",False)


# =============================================================================
# P006 — CSV Field Count
# =============================================================================
print("\n"+"="*65); print("P006 — CSV Field Count"); print("="*65)

PY_CORRECT = """
def csv_field_count(line):
    count=1; in_q=False
    for c in line:
        if c=='"': in_q=not in_q
        elif c==',' and not in_q: count+=1
    return count
"""
run("P006","python","Correct",PY_CORRECT,True)
run("P006","python","Wrong","def csv_field_count(line): return 0",False)

JAVA_CORRECT = """
public class Solution {
    public static int csvFieldCount(String line) {
        int count=1; boolean inQ=false;
        for(char c:line.toCharArray()){
            if(c=='"') inQ=!inQ;
            else if(c==','&&!inQ) count++;
        }
        return count;
    }
}
"""
run("P006","java","Correct",JAVA_CORRECT,True)

CPP_CORRECT = """
#include <string>
using namespace std;
int csvFieldCount(const string& line) {
    int count=1; bool inQ=false;
    for(char c:line){if(c=='"')inQ=!inQ;else if(c==','&&!inQ)count++;}
    return count;
}
"""
run("P006","cpp","Correct",CPP_CORRECT,True)

JS_CORRECT = """
function csvFieldCount(line) {
    let count=1, inQ=false;
    for(const c of line){if(c==='"')inQ=!inQ;else if(c===','&&!inQ)count++;}
    return count;
}
module.exports = { csvFieldCount };
"""
run("P006","javascript","Correct",JS_CORRECT,True)


# =============================================================================
# P007 — Log Level Counter
# =============================================================================
print("\n"+"="*65); print("P007 — Log Level Counter"); print("="*65)

PY_CORRECT = """
def count_log_levels(log):
    counts={"ERROR":0,"WARNING":0,"INFO":0,"DEBUG":0}
    for line in log.splitlines():
        for lvl in counts:
            if line.startswith(lvl): counts[lvl]+=1; break
    return counts
"""
run("P007","python","Correct",PY_CORRECT,True)
run("P007","python","Wrong","def count_log_levels(log): return {}",False)

JAVA_CORRECT = """
import java.util.*;
public class Solution {
    public static Map<String,Integer> countLogLevels(String log) {
        Map<String,Integer> m=new LinkedHashMap<>();
        m.put("ERROR",0);m.put("WARNING",0);m.put("INFO",0);m.put("DEBUG",0);
        for(String line:log.split("\\n",-1)){
            for(String lvl:m.keySet()){if(line.startsWith(lvl)){m.put(lvl,m.get(lvl)+1);break;}}
        }
        return m;
    }
}
"""
run("P007","java","Correct",JAVA_CORRECT,True)

CPP_CORRECT = """
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
}
"""
run("P007","cpp","Correct",CPP_CORRECT,True)

JS_CORRECT = """
function countLogLevels(log) {
    const counts={ERROR:0,WARNING:0,INFO:0,DEBUG:0};
    for(const line of log.split('\\n')){
        for(const lvl of Object.keys(counts)){if(line.startsWith(lvl)){counts[lvl]++;break;}}
    }
    return counts;
}
module.exports = { countLogLevels };
"""
run("P007","javascript","Correct",JS_CORRECT,True)


# =============================================================================
# P008 — Key-Value Parser
# =============================================================================
print("\n"+"="*65); print("P008 — Key-Value Parser"); print("="*65)

PY_CORRECT = """
def parse_key_value(s):
    if not s.strip(): return {}
    result={}
    for pair in s.split(','):
        if '=' in pair:
            k,v=pair.split('=',1)
            result[k.strip()]=v.strip()
    return result
"""
run("P008","python","Correct",PY_CORRECT,True)
run("P008","python","Wrong","def parse_key_value(s): return {}",False)

JAVA_CORRECT = """
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
}
"""
run("P008","java","Correct",JAVA_CORRECT,True)

CPP_CORRECT = """
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
            // trim
            while(!k.empty()&&k.front()==' ')k.erase(k.begin());
            while(!k.empty()&&k.back()==' ')k.pop_back();
            while(!v.empty()&&v.front()==' ')v.erase(v.begin());
            while(!v.empty()&&v.back()==' ')v.pop_back();
            m[k]=v;
        }
    }
    return m;
}
"""
run("P008","cpp","Correct",CPP_CORRECT,True)

JS_CORRECT = """
function parseKeyValue(s) {
    const res={};
    if(!s.trim()) return res;
    for(const pair of s.split(',')){
        const eq=pair.indexOf('=');
        if(eq>=0) res[pair.slice(0,eq).trim()]=pair.slice(eq+1).trim();
    }
    return res;
}
module.exports = { parseKeyValue };
"""
run("P008","javascript","Correct",JS_CORRECT,True)


# =============================================================================
# P009 — Date Format Normalizer
# =============================================================================
print("\n"+"="*65); print("P009 — Date Format Normalizer"); print("="*65)

PY_CORRECT = """
import re
def normalize_date(date):
    date=date.strip()
    if re.match(r'\\d{2}/\\d{2}/\\d{4}',date):
        m,d,y=date.split('/')
        return f'{y}-{m}-{d}'
    elif re.match(r'\\d{2}-\\d{2}-\\d{4}',date):
        d,m,y=date.split('-')
        return f'{y}-{m}-{d}'
    elif re.match(r'\\d{4}\\.\\d{2}\\.\\d{2}',date):
        y,m,d=date.split('.')
        return f'{y}-{m}-{d}'
    return date
"""
run("P009","python","Correct",PY_CORRECT,True)
run("P009","python","Wrong","def normalize_date(d): return d",False)

JAVA_CORRECT = """
public class Solution {
    public static String normalizeDate(String date) {
        date=date.trim();
        if(date.matches("\\\\d{2}/\\\\d{2}/\\\\d{4}")){
            String[]p=date.split("/"); return p[2]+"-"+p[0]+"-"+p[1];
        } else if(date.matches("\\\\d{2}-\\\\d{2}-\\\\d{4}")){
            String[]p=date.split("-"); return p[2]+"-"+p[1]+"-"+p[0];
        } else if(date.matches("\\\\d{4}\\\\.\\\\d{2}\\\\.\\\\d{2}")){
            String[]p=date.split("\\\\."); return p[0]+"-"+p[1]+"-"+p[2];
        }
        return date;
    }
}
"""
run("P009","java","Correct",JAVA_CORRECT,True)

CPP_CORRECT = """
#include <string>
#include <regex>
using namespace std;
string normalizeDate(const string& date) {
    if(date.size()==10 && date[2]=='/') return date.substr(6,4)+"-"+date.substr(0,2)+"-"+date.substr(3,2);
    if(date.size()==10 && date[2]=='-') return date.substr(6,4)+"-"+date.substr(3,2)+"-"+date.substr(0,2);
    if(date.size()==10 && date[4]=='.') return date.substr(0,4)+"-"+date.substr(5,2)+"-"+date.substr(8,2);
    return date;
}
"""
run("P009","cpp","Correct",CPP_CORRECT,True)

JS_CORRECT = """
function normalizeDate(date) {
    date=date.trim();
    if(/^\\d{2}\\/\\d{2}\\/\\d{4}$/.test(date)){const[m,d,y]=date.split('/');return `${y}-${m}-${d}`;}
    if(/^\\d{2}-\\d{2}-\\d{4}$/.test(date)){const[d,m,y]=date.split('-');return `${y}-${m}-${d}`;}
    if(/^\\d{4}\\.\\d{2}\\.\\d{2}$/.test(date)){const[y,m,d]=date.split('.');return `${y}-${m}-${d}`;}
    return date;
}
module.exports = { normalizeDate };
"""
run("P009","javascript","Correct",JS_CORRECT,True)


# =============================================================================
# P010 — Word Frequency
# =============================================================================
print("\n"+"="*65); print("P010 — Word Frequency"); print("="*65)

PY_CORRECT = """
import re
def word_frequency(text):
    words=re.findall(r'[a-zA-Z]+',text.lower())
    freq={}
    for w in words: freq[w]=freq.get(w,0)+1
    return freq
"""
run("P010","python","Correct",PY_CORRECT,True)
run("P010","python","Wrong","def word_frequency(text): return {}",False)

JAVA_CORRECT = """
import java.util.*;
import java.util.regex.*;
public class Solution {
    public static Map<String,Integer> wordFrequency(String text) {
        Map<String,Integer> m=new LinkedHashMap<>();
        Matcher mat=Pattern.compile("[a-zA-Z]+").matcher(text.toLowerCase());
        while(mat.find()){String w=mat.group();m.put(w,m.getOrDefault(w,0)+1);}
        return m;
    }
}
"""
run("P010","java","Correct",JAVA_CORRECT,True)

CPP_CORRECT = """
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
}
"""
run("P010","cpp","Correct",CPP_CORRECT,True)

JS_CORRECT = """
function wordFrequency(text) {
    const words=text.toLowerCase().match(/[a-zA-Z]+/g)||[];
    const freq={};
    for(const w of words) freq[w]=(freq[w]||0)+1;
    return freq;
}
module.exports = { wordFrequency };
"""
run("P010","javascript","Correct",JS_CORRECT,True)
run("P010","javascript","Wrong","function wordFrequency(t){return {};}\nmodule.exports={wordFrequency};",False)


# =============================================================================
# Summary
# =============================================================================
print("\n"+"="*65)
print("VALIDATION SUMMARY")
print("="*65)
total   = len(results)
passed  = sum(1 for v in results.values() if v)
failed  = total - passed
print(f"  Total checks : {total}")
print(f"  Passed       : {passed}")
print(f"  Failed       : {failed}")

if failed:
    print("\n  FAILURES:")
    for (pid,lang,label),ok in results.items():
        if not ok:
            print(f"    {pid} [{lang}] {label}")
    sys.exit(1)
else:
    print("\n  ALL CHECKS PASSED")
    sys.exit(0)
