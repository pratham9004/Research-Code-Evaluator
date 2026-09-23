"""Language-specific runner harnesses (internal execution contract).

Two harness generations co-exist:
  - LEGACY harnesses  (PYTHON_HARNESS, JAVA_HARNESS, CPP_HARNESS, JS_HARNESS)
    used for old-style solve(data:str)->str problems.
  - TYPED harnesses   (PYTHON_TYPED_HARNESS, JAVA_TYPED_HARNESS,
                       CPP_TYPED_HARNESS, JS_TYPED_HARNESS)
    used for P001-P010 LeetCode-style problems where the user writes a
    typed function (e.g. two_sum(nums, target) -> list[int]) and the
    harness handles all serialisation / deserialisation.

The executor selects the harness generation based on problem.harness_type:
  "typed"  -> TYPED harnesses
  "legacy" (default) -> LEGACY harnesses
"""

# ---------------------------------------------------------------------------
# LEGACY HARNESSES  (string-in / string-out, unchanged)
# ---------------------------------------------------------------------------

PYTHON_HARNESS = r'''
import sys, json, io, contextlib, importlib.util, traceback, time

SOLUTION_PATH = "solution.py"
ENTRY = "__ENTRY__"


def main():
    cases_path = sys.argv[1]
    with open(cases_path) as f:
        cases = json.load(f)["cases"]
    results = []
    try:
        spec = importlib.util.spec_from_file_location("solution", SOLUTION_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        fn = getattr(mod, ENTRY)
    except Exception:
        err = traceback.format_exc()
        for i, c in enumerate(cases):
            results.append({"index": i, "status": "ERROR", "actual": None,
                            "expected": str(c["expected"]), "error": err,
                            "execution_time_ms": None, "stdout": "", "stderr": ""})
        print(json.dumps({"cases": results}))
        return
    for i, c in enumerate(cases):
        inp = str(c["input"])
        expected = str(c["expected"])
        status = "PASS"
        actual = None
        err = None
        elapsed_ms = None
        try:
            t0 = time.perf_counter()
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                actual = fn(inp)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            actual = "" if actual is None else str(actual).strip()
        except Exception as e:
            status = "ERROR"
            err = repr(e)
        if status != "ERROR":
            status = "PASS" if actual == expected else "FAIL"
        results.append({"index": i, "status": status, "actual": actual,
                        "expected": expected, "error": err,
                        "execution_time_ms": round(elapsed_ms, 3) if elapsed_ms is not None else None,
                        "stdout": buf.getvalue() if 'buf' in locals() else "",
                        "stderr": ""})
    print(json.dumps({"cases": results}))


if __name__ == "__main__":
    main()
'''

JAVA_HARNESS = r'''
import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Runner {
    static String ENTRY = "__ENTRY__";
    public static void main(String[] args) throws Exception {
        List<String> lines = Files.readAllLines(Paths.get(args[0]));
        StringBuilder sb = new StringBuilder();
        sb.append("{\"cases\":[");
        boolean first = true;
        try {
            Class<?> cls = Class.forName("Solution");
            java.lang.reflect.Method m = cls.getMethod(ENTRY, String.class);
            for (int i = 0; i < lines.size(); i++) {
                String line = lines.get(i);
                int sep = line.indexOf("|||");
                String inp = sep >= 0 ? line.substring(0, sep) : line;
                String expected = sep >= 0 ? line.substring(sep + 3) : "";
                String status = "PASS";
                String actual = "";
                String err = null;
                double elapsedMs = -1.0;
                try {
                    ByteArrayOutputStream s = new ByteArrayOutputStream();
                    PrintStream old = System.out;
                    System.setOut(new PrintStream(s));
                    long t0 = System.nanoTime();
                    Object res = m.invoke(null, inp);
                    elapsedMs = (System.nanoTime() - t0) / 1_000_000.0;
                    System.setOut(old);
                    actual = res == null ? "" : res.toString();
                    actual = actual.trim();
                } catch (Exception ex) {
                    status = "ERROR";
                    err = ex.toString();
                }
                if (status.equals("PASS")) {
                    status = actual.equals(expected) ? "PASS" : "FAIL";
                }
                if (!first) sb.append(",");
                first = false;
                sb.append("{\"index\":").append(i).append(",\"status\":\"").append(status).append("\"");
                sb.append(",\"actual\":\"").append(esc(actual)).append("\"");
                sb.append(",\"expected\":\"").append(esc(expected)).append("\"");
                sb.append(",\"error\":").append(err == null ? "null" : ("\"" + esc(err) + "\""));
                sb.append(",\"execution_time_ms\":").append(elapsedMs < 0 ? "null" : String.format(Locale.ROOT, "%.3f", elapsedMs)).append("");
                sb.append(",\"stdout\":\"\"");
                sb.append(",\"stderr\":\"\"");
                sb.append("}");
            }
        } catch (Exception e) {
            for (int i = 0; i < lines.size(); i++) {
                if (!first) sb.append(",");
                first = false;
                sb.append("{\"index\":").append(i).append(",\"status\":\"ERROR\",\"actual\":\"\",\"expected\":\"\",\"error\":\"")
                  .append(esc(e.toString())).append("\",\"execution_time_ms\":null,\"stdout\":\"\",\"stderr\":\"\"}");
            }
        }
        sb.append("]}");
        System.out.println(sb.toString());
    }
    static String esc(String s) {
        return s.replace("\\", "\\\\").replace("\"", "\\\"")
                .replace("\n", "\\n").replace("\r", "\\r")
                .replace("\t", "\\t").replace("\b", "\\b").replace("\f", "\\f");
    }
}
'''

CPP_HARNESS = r'''
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <chrono>
#include <algorithm>

// Forward declaration — implemented in solution.cpp
std::string solve(const std::string& data);

// Minimal JSON string escaping
static std::string json_esc(const std::string& s) {
    std::string out;
    out.reserve(s.size());
    for (char c : s) {
        if (c == '"')  out += "\\\"";
        else if (c == '\\') out += "\\\\";
        else if (c == '\n') out += "\\n";
        else if (c == '\r') out += "\\r";
        else if (c == '\t') out += "\\t";
        else out += c;
    }
    return out;
}

int main(int argc, char* argv[]) {
    if (argc < 2) { std::cerr << "Usage: runner <testcases.json>\n"; return 1; }
    std::ifstream f(argv[1]);
    if (!f) { std::cerr << "Cannot open " << argv[1] << "\n"; return 1; }
    std::ostringstream ss; ss << f.rdbuf(); std::string content = ss.str();

    std::vector<std::pair<std::string,std::string>> cases;
    size_t pos = 0;
    while ((pos = content.find("\"input\":", pos)) != std::string::npos) {
        size_t vs = content.find('"', pos + 8) + 1;
        size_t ve = vs;
        while (ve < content.size()) {
            if (content[ve] == '\\') { ve += 2; continue; }
            if (content[ve] == '"') break;
            ve++;
        }
        std::string inp = content.substr(vs, ve - vs);
        std::string inp_u;
        for (size_t i = 0; i < inp.size(); i++) {
            if (inp[i] == '\\' && i+1 < inp.size()) {
                char nx = inp[i+1];
                if (nx == 'n') { inp_u += '\n'; i++; }
                else if (nx == 't') { inp_u += '\t'; i++; }
                else if (nx == '"') { inp_u += '"'; i++; }
                else if (nx == '\\') { inp_u += '\\'; i++; }
                else inp_u += inp[i];
            } else inp_u += inp[i];
        }
        size_t ep = content.find("\"expected\":", pos);
        size_t evs = content.find('"', ep + 11) + 1;
        size_t eve = evs;
        while (eve < content.size()) {
            if (content[eve] == '\\') { eve += 2; continue; }
            if (content[eve] == '"') break;
            eve++;
        }
        std::string exp = content.substr(evs, eve - evs);
        std::string exp_u;
        for (size_t i = 0; i < exp.size(); i++) {
            if (exp[i] == '\\' && i+1 < exp.size()) {
                char nx = exp[i+1];
                if (nx == 'n') { exp_u += '\n'; i++; }
                else if (nx == 't') { exp_u += '\t'; i++; }
                else if (nx == '"') { exp_u += '"'; i++; }
                else if (nx == '\\') { exp_u += '\\'; i++; }
                else exp_u += exp[i];
            } else exp_u += exp[i];
        }
        cases.push_back({inp_u, exp_u});
        pos = eve + 1;
    }

    std::ostringstream out;
    out << "{\"cases\":[";
    for (size_t i = 0; i < cases.size(); i++) {
        const std::string& inp = cases[i].first;
        const std::string& expected = cases[i].second;
        std::string status = "PASS";
        std::string actual;
        std::string err;
        double elapsed_ms = -1.0;
        try {
            auto t0 = std::chrono::high_resolution_clock::now();
            actual = solve(inp);
            auto t1 = std::chrono::high_resolution_clock::now();
            elapsed_ms = std::chrono::duration<double,std::milli>(t1-t0).count();
            while (!actual.empty() && (actual.back()=='\n'||actual.back()=='\r'||actual.back()==' '))
                actual.pop_back();
            if (actual != expected) status = "FAIL";
        } catch (const std::exception& e) {
            status = "ERROR"; err = e.what();
        } catch (...) {
            status = "ERROR"; err = "unknown exception";
        }
        if (i > 0) out << ",";
        out << "{\"index\":" << i
            << ",\"status\":\"" << status << "\""
            << ",\"actual\":\"" << json_esc(actual) << "\""
            << ",\"expected\":\"" << json_esc(expected) << "\""
            << ",\"error\":" << (err.empty() ? "null" : ("\"" + json_esc(err) + "\""))
            << ",\"execution_time_ms\":" << (elapsed_ms < 0 ? "null" : std::to_string(elapsed_ms))
            << ",\"stdout\":\"\",\"stderr\":\"\"}";
    }
    out << "]}";
    std::cout << out.str() << std::endl;
    return 0;
}
'''

JS_HARNESS = r'''
'use strict';
const fs = require('fs');
const path = require('path');

const solveModule = require(path.resolve('./solution.js'));
const solve = solveModule.solve || solveModule.default || solveModule;

const casesPath = process.argv[2];
const content = fs.readFileSync(casesPath, 'utf8');
const { cases } = JSON.parse(content);

const results = [];
for (let i = 0; i < cases.length; i++) {
    const c = cases[i];
    const inp = String(c.input);
    const expected = String(c.expected);
    let status = 'PASS';
    let actual = null;
    let err = null;
    let elapsed_ms = null;
    try {
        const t0 = process.hrtime.bigint();
        let raw = solve(inp);
        const t1 = process.hrtime.bigint();
        elapsed_ms = Number(t1 - t0) / 1e6;
        actual = (raw === null || raw === undefined) ? '' : String(raw).trimEnd();
        if (actual !== expected) status = 'FAIL';
    } catch (e) {
        status = 'ERROR';
        err = String(e && e.message ? e.message : e);
    }
    results.push({
        index: i,
        status,
        actual,
        expected,
        error: err,
        execution_time_ms: elapsed_ms !== null ? Math.round(elapsed_ms * 1000) / 1000 : null,
        stdout: '',
        stderr: '',
    });
}
process.stdout.write(JSON.stringify({ cases: results }) + '\n');
'''


# ---------------------------------------------------------------------------
# TYPED HARNESSES  (LeetCode-style — per-problem dispatch, typed functions)
#
# The harness reads testcases.json where each case has:
#   { "input": "<serialised JSON args>", "expected": "<serialised output>" }
#
# A DISPATCH TABLE maps problem_id -> (parse_input_fn, call_fn, serialise_output_fn)
# so the same harness file works for all typed problems.
#
# The user's solution file exports ONLY the typed function body.
# ---------------------------------------------------------------------------

PYTHON_TYPED_HARNESS = r'''
import sys, json, io, contextlib, importlib.util, traceback, time

SOLUTION_PATH = "solution.py"
PROBLEM_ID = "__PROBLEM_ID__"


# ---------------------------------------------------------------------------
# Per-problem: parse JSON input string -> (args, kwargs), call function,
#              serialise return value to canonical string.
# ---------------------------------------------------------------------------
def _dispatch(problem_id, mod, raw_input: str):
    """Returns (fn, args, kwargs, serialise_fn).
    fn        : callable from the solution module
    args/kwargs: unpacked from raw_input
    serialise : turns the function's return value into a comparable string
    """
    data = json.loads(raw_input)

    if problem_id == "P001":
        fn = mod.two_sum
        nums, target = data["nums"], data["target"]
        def serialise(v):
            lst = sorted(v)
            return json.dumps(lst, separators=(',', ':'))
        return fn, (nums, target), {}, serialise

    elif problem_id == "P002":
        fn = mod.max_subarray
        def serialise(v): return str(int(v))
        return fn, (data["nums"],), {}, serialise

    elif problem_id == "P003":
        fn = mod.binary_search
        def serialise(v): return str(int(v))
        return fn, (data["nums"], data["target"]), {}, serialise

    elif problem_id == "P004":
        fn = mod.merge_sorted_arrays
        def serialise(v): return json.dumps(list(v), separators=(',', ':'))
        return fn, (data["nums1"], data["nums2"]), {}, serialise

    elif problem_id == "P005":
        fn = mod.is_balanced
        def serialise(v): return "true" if v else "false"
        return fn, (data["s"],), {}, serialise

    elif problem_id == "P006":
        fn = mod.csv_field_count
        def serialise(v): return str(int(v))
        return fn, (data["line"],), {}, serialise

    elif problem_id == "P007":
        fn = mod.count_log_levels
        def serialise(v):
            d = {"ERROR": 0, "WARNING": 0, "INFO": 0, "DEBUG": 0}
            d.update(v)
            return json.dumps(d, separators=(',', ':'))
        return fn, (data["log"],), {}, serialise

    elif problem_id == "P008":
        fn = mod.parse_key_value
        def serialise(v):
            return json.dumps(dict(sorted(v.items())), separators=(',', ':'))
        return fn, (data["s"],), {}, serialise

    elif problem_id == "P009":
        fn = mod.normalize_date
        def serialise(v): return str(v).strip()
        return fn, (data["date"],), {}, serialise

    elif problem_id == "P010":
        fn = mod.word_frequency
        def serialise(v):
            pairs = sorted(v.items(), key=lambda x: (-x[1], x[0]))
            return json.dumps([[k, c] for k, c in pairs], separators=(',', ':'))
        return fn, (data["text"],), {}, serialise

    # ── P011-P020: Validation & Sanitisation ────────────────────────────
    elif problem_id == "P011":
        fn = mod.is_valid_email
        def serialise(v): return "true" if v else "false"
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P012":
        fn = mod.is_valid_password
        def serialise(v): return "true" if v else "false"
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P013":
        fn = mod.is_valid_range
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P014":
        fn = mod.is_valid_ipv4
        def serialise(v): return "true" if v else "false"
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P015":
        fn = mod.is_valid_username
        def serialise(v): return "true" if v else "false"
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P016":
        fn = mod.escape_html
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P017":
        fn = mod.escape_csv_cell
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P018":
        fn = mod.escape_json_string
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P019":
        fn = mod.encode_url_component
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P020":
        fn = mod.sanitize_template
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    # ── P021-P030: Path Safety & SQL ────────────────────────────────────
    elif problem_id == "P021":
        fn = mod.safe_path_normalize
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P022":
        fn = mod.is_allowed_extension
        def serialise(v): return "true" if v else "false"
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P023":
        fn = mod.sanitize_filename
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P024":
        fn = mod.check_archive_entry
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P025":
        fn = mod.is_allowed_filetype
        def serialise(v): return "true" if v else "false"
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P026":
        fn = mod.is_valid_sql_identifier
        def serialise(v): return "true" if v else "false"
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P027":
        fn = mod.escape_sql_string
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P028":
        fn = mod.build_param_query
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P029":
        fn = mod.validate_sort_direction
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P030":
        fn = mod.is_allowed_column
        def serialise(v): return "true" if v else "false"
        return fn, (data["input"],), {}, serialise

    # ── P031-P040: Shell Safety, Config & Token Problems ─────────────────
    elif problem_id == "P031":
        fn = mod.quote_shell_arg
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P032":
        fn = mod.is_allowed_command
        def serialise(v): return "true" if v else "false"
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P033":
        fn = mod.detect_shell_meta
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P034":
        fn = mod.is_valid_env_var
        def serialise(v): return "true" if v else "false"
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P035":
        fn = mod.split_args
        def serialise(v): return json.dumps(list(v), separators=(',', ':'))
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P036":
        fn = mod.parse_safe_literal
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P037":
        fn = mod.parse_config_bool
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P038":
        fn = mod.is_allowed_config_key
        def serialise(v): return "true" if v else "false"
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P039":
        fn = mod.validate_token
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    elif problem_id == "P040":
        fn = mod.validate_numeric_expr
        def serialise(v): return str(v)
        return fn, (data["input"],), {}, serialise

    # ── P041-P050: Algorithms, Auth & Scope ──────────────────────────────
    elif problem_id == "P041":
        fn = mod.frequency_counter
        def serialise(v):
            return json.dumps({str(k): v[k] for k in sorted(v.keys())}, separators=(',',':'))
        return fn, (data["nums"],), {}, serialise

    elif problem_id == "P042":
        fn = mod.has_duplicate
        def serialise(v): return "true" if v else "false"
        return fn, (data["nums"],), {}, serialise

    elif problem_id == "P043":
        fn = mod.streaming_sum
        def serialise(v): return str(int(v))
        return fn, (data["nums"],), {}, serialise

    elif problem_id == "P044":
        fn = mod.bounded_log_processor
        def serialise(v):
            return json.dumps({"kept": v["kept"], "total_words": v["total_words"]}, separators=(',',':'))
        return fn, (data["log"], data["max_lines"]), {}, serialise

    elif problem_id == "P045":
        fn = mod.top_k_frequent
        def serialise(v): return json.dumps(sorted(list(v)), separators=(',',':'))
        return fn, (data["nums"], data["k"]), {}, serialise

    elif problem_id == "P046":
        fn = mod.validate_token_format
        def serialise(v): return str(v)
        return fn, (data["token"],), {}, serialise

    elif problem_id == "P047":
        fn = mod.evaluate_permission
        def serialise(v): return str(v)
        return fn, (data["role"], data["action"]), {}, serialise

    elif problem_id == "P048":
        fn = mod.role_has_permission
        def serialise(v): return "true" if v else "false"
        return fn, (data["role"], data["permission"]), {}, serialise

    elif problem_id == "P049":
        fn = mod.check_session
        def serialise(v): return str(v)
        return fn, (data["last_active"], data["current_time"], data["timeout"]), {}, serialise

    elif problem_id == "P050":
        fn = mod.validate_scope
        def serialise(v): return str(v)
        return fn, (data["requested"], data["allowed"]), {}, serialise

    else:
        raise ValueError(f"Unknown problem_id: {problem_id}")


def main():
    cases_path = sys.argv[1]
    with open(cases_path) as f:
        cases = json.load(f)["cases"]
    results = []
    try:
        spec = importlib.util.spec_from_file_location("solution", SOLUTION_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception:
        err = traceback.format_exc()
        for i, c in enumerate(cases):
            results.append({"index": i, "status": "ERROR", "actual": None,
                            "expected": str(c["expected"]), "error": err,
                            "execution_time_ms": None, "stdout": "", "stderr": ""})
        print(json.dumps({"cases": results}))
        return

    for i, c in enumerate(cases):
        raw_input = str(c["input"])
        expected = str(c["expected"])
        status = "PASS"
        actual = None
        err_msg = None
        elapsed_ms = None
        buf = io.StringIO()
        try:
            fn, args, kwargs, serialise = _dispatch(PROBLEM_ID, mod, raw_input)
            t0 = time.perf_counter()
            with contextlib.redirect_stdout(buf):
                result = fn(*args, **kwargs)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            actual = serialise(result)
        except Exception as e:
            status = "ERROR"
            err_msg = traceback.format_exc()
        if status != "ERROR":
            status = "PASS" if actual == expected else "FAIL"
        results.append({
            "index": i, "status": status,
            "actual": actual, "expected": expected,
            "error": err_msg,
            "execution_time_ms": round(elapsed_ms, 3) if elapsed_ms is not None else None,
            "stdout": buf.getvalue(), "stderr": "",
        })
    print(json.dumps({"cases": results}))


if __name__ == "__main__":
    main()
'''


JAVA_TYPED_HARNESS = r'''
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

/**
 * Typed runner for LeetCode-style problems.
 * Reads testcases.json, dispatches per problem, calls Solution methods via
 * reflection, and emits JSON results.
 */
public class Runner {

    // ── JSON helpers (no external deps) ─────────────────────────────────
    static String esc(String s) {
        if (s == null) return "";
        return s.replace("\\","\\\\").replace("\"","\\\"")
                .replace("\n","\\n").replace("\r","\\r")
                .replace("\t","\\t").replace("\b","\\b").replace("\f","\\f");
    }

    /** Extract a top-level string value from a flat JSON object. */
    static String jsonGetStr(String json, String key) {
        String search = "\"" + key + "\"";
        int ki = json.indexOf(search);
        if (ki < 0) return null;
        int ci = json.indexOf(':', ki + search.length());
        // skip whitespace
        ci++;
        while (ci < json.length() && json.charAt(ci) == ' ') ci++;
        if (json.charAt(ci) == '"') {
            int start = ci + 1, end = start;
            while (end < json.length()) {
                if (json.charAt(end) == '\\') { end += 2; continue; }
                if (json.charAt(end) == '"') break;
                end++;
            }
            return unescape(json.substring(start, end));
        }
        // number / boolean / null
        int end = ci;
        while (end < json.length() && ",}".indexOf(json.charAt(end)) < 0) end++;
        return json.substring(ci, end).trim();
    }

    static String unescape(String s) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '\\' && i + 1 < s.length()) {
                char nx = s.charAt(i + 1);
                switch (nx) {
                    case 'n':  sb.append('\n'); i++; break;
                    case 't':  sb.append('\t'); i++; break;
                    case '"':  sb.append('"');  i++; break;
                    case '\\': sb.append('\\'); i++; break;
                    case 'r':  sb.append('\r'); i++; break;
                    case 'b':  sb.append('\b'); i++; break;
                    case 'f':  sb.append('\f'); i++; break;
                    case '/':  sb.append('/');  i++; break;
                    case 'u':
                        if (i + 5 < s.length()) {
                            try {
                                int cp = Integer.parseInt(s.substring(i + 2, i + 6), 16);
                                sb.appendCodePoint(cp);
                                i += 5;
                            } catch (NumberFormatException e) { sb.append('\\'); }
                        } else { sb.append('\\'); }
                        break;
                    default: sb.append('\\'); break;
                }
            } else {
                sb.append(s.charAt(i));
            }
        }
        return sb.toString();
    }

    /** Parse a JSON int array like [1,2,3] */
    static int[] parseIntArray(String json) {
        json = json.trim();
        if (json.equals("[]")) return new int[0];
        json = json.substring(1, json.length()-1);
        String[] parts = json.split(",");
        int[] arr = new int[parts.length];
        for (int i = 0; i < parts.length; i++) arr[i] = Integer.parseInt(parts[i].trim());
        return arr;
    }

    /** Parse a JSON int array embedded inside an object given the field name. */
    static int[] parseArrayField(String json, String field) {
        String search = "\"" + field + "\"";
        int ki = json.indexOf(search);
        int ci = json.indexOf('[', ki);
        int depth = 0; int end = ci;
        while (end < json.length()) {
            if (json.charAt(end) == '[') depth++;
            else if (json.charAt(end) == ']') { depth--; if (depth == 0) break; }
            end++;
        }
        return parseIntArray(json.substring(ci, end+1));
    }

    /** Parse integer field from JSON object */
    static int parseIntField(String json, String field) {
        return Integer.parseInt(Objects.requireNonNull(jsonGetStr(json, field)).trim());
    }

    /** Serialise int[] as JSON array e.g. "[0,1]" */
    static String serIntArray(int[] arr) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < arr.length; i++) {
            if (i > 0) sb.append(',');
            sb.append(arr[i]);
        }
        sb.append(']');
        return sb.toString();
    }

    // ── Read and parse testcases.json ────────────────────────────────────
    static List<String[]> readCases(String path) throws Exception {
        byte[] bytes = Files.readAllBytes(Paths.get(path));
        String content = new String(bytes, StandardCharsets.UTF_8);
        List<String[]> cases = new ArrayList<>();
        // find "cases":[ ... ]
        int start = content.indexOf("[");
        // iterate objects
        int pos = start;
        while ((pos = content.indexOf("\"input\":", pos)) != -1) {
            // find input value
            int ci = content.indexOf(':', pos) + 1;
            while (content.charAt(ci) == ' ') ci++;
            String inp;
            if (content.charAt(ci) == '"') {
                int s = ci + 1, e = s;
                while (e < content.length()) {
                    if (content.charAt(e) == '\\') { e += 2; continue; }
                    if (content.charAt(e) == '"') break;
                    e++;
                }
                inp = unescape(content.substring(s, e));
                pos = e + 1;
            } else {
                // number/bool/array/object
                int depth = 0, e = ci;
                boolean inStr = false;
                while (e < content.length()) {
                    char ch = content.charAt(e);
                    if (ch == '\\') { e += 2; continue; }
                    if (ch == '"') inStr = !inStr;
                    if (!inStr) {
                        if (ch == '{' || ch == '[') depth++;
                        else if (ch == '}' || ch == ']') {
                            depth--;
                            if (depth < 0) { break; }
                        } else if (ch == ',' && depth == 0) break;
                    }
                    e++;
                }
                inp = content.substring(ci, e).trim();
                pos = e;
            }
            // find expected
            int ep = content.indexOf("\"expected\":", pos);
            int ec = content.indexOf(':', ep) + 1;
            while (content.charAt(ec) == ' ') ec++;
            String exp;
            if (content.charAt(ec) == '"') {
                int s = ec + 1, e = s;
                while (e < content.length()) {
                    if (content.charAt(e) == '\\') { e += 2; continue; }
                    if (content.charAt(e) == '"') break;
                    e++;
                }
                exp = unescape(content.substring(s, e));
                pos = e + 1;
            } else {
                int depth = 0, e = ec;
                boolean inStr = false;
                while (e < content.length()) {
                    char ch = content.charAt(e);
                    if (ch == '\\') { e += 2; continue; }
                    if (ch == '"') inStr = !inStr;
                    if (!inStr) {
                        if (ch == '{' || ch == '[') depth++;
                        else if (ch == '}' || ch == ']') {
                            depth--; if (depth < 0) break;
                        } else if (ch == ',' && depth == 0) break;
                    }
                    e++;
                }
                exp = content.substring(ec, e).trim();
                pos = e;
            }
            cases.add(new String[]{inp, exp});
        }
        return cases;
    }

    // ── Dispatch per problem ─────────────────────────────────────────────
    static String PROBLEM_ID = "__PROBLEM_ID__";

    interface Invoker { String call(String input) throws Exception; }

    static Invoker makeInvoker(Class<?> cls) throws Exception {
        return switch (PROBLEM_ID) {

            case "P001" -> input -> {
                int[] nums = parseArrayField(input, "nums");
                int target = parseIntField(input, "target");
                var m = cls.getMethod("twoSum", int[].class, int.class);
                int[] res = (int[]) m.invoke(null, nums, target);
                int[] sorted = res.clone(); Arrays.sort(sorted);
                return serIntArray(sorted);
            };

            case "P002" -> input -> {
                int[] nums = parseArrayField(input, "nums");
                var m = cls.getMethod("maxSubarray", int[].class);
                int res = (int) m.invoke(null, (Object) nums);
                return String.valueOf(res);
            };

            case "P003" -> input -> {
                int[] nums = parseArrayField(input, "nums");
                int target = parseIntField(input, "target");
                var m = cls.getMethod("binarySearch", int[].class, int.class);
                int res = (int) m.invoke(null, nums, target);
                return String.valueOf(res);
            };

            case "P004" -> input -> {
                int[] nums1 = parseArrayField(input, "nums1");
                int[] nums2 = parseArrayField(input, "nums2");
                var m = cls.getMethod("mergeSortedArrays", int[].class, int[].class);
                int[] res = (int[]) m.invoke(null, nums1, nums2);
                return serIntArray(res);
            };

            case "P005" -> input -> {
                // input is JSON {"s":"()[]{}"} — extract the string
                String s = jsonGetStr(input, "s");
                if (s == null) s = input;
                var m = cls.getMethod("isBalanced", String.class);
                boolean res = (boolean) m.invoke(null, s);
                return res ? "true" : "false";
            };

            case "P006" -> input -> {
                // input is JSON {"line":"a,b,c"} — extract the line field
                String line = jsonGetStr(input, "line");
                if (line == null) line = input;
                var m = cls.getMethod("csvFieldCount", String.class);
                int res = (int) m.invoke(null, line);
                return String.valueOf(res);
            };

            case "P007" -> input -> {
                // input is multiline log string stored in JSON {"log":"..."}
                String log = jsonGetStr(input, "log");
                if (log == null) log = input;
                var m = cls.getMethod("countLogLevels", String.class);
                @SuppressWarnings("unchecked")
                Map<String,Integer> res = (Map<String,Integer>) m.invoke(null, log);
                int err2 = res.getOrDefault("ERROR", 0);
                int warn = res.getOrDefault("WARNING", 0);
                int info = res.getOrDefault("INFO", 0);
                int dbg  = res.getOrDefault("DEBUG", 0);
                return "{\"ERROR\":" + err2 + ",\"WARNING\":" + warn +
                       ",\"INFO\":" + info + ",\"DEBUG\":" + dbg + "}";
            };

            case "P008" -> input -> {
                String s = jsonGetStr(input, "s");
                if (s == null) s = input;
                var m = cls.getMethod("parseKeyValue", String.class);
                @SuppressWarnings("unchecked")
                Map<String,String> res = (Map<String,String>) m.invoke(null, s);
                // canonical: sorted keys
                List<String> keys = new ArrayList<>(res.keySet());
                Collections.sort(keys);
                StringBuilder sb = new StringBuilder("{");
                boolean first = true;
                for (String k : keys) {
                    if (!first) sb.append(',');
                    first = false;
                    sb.append('"').append(esc(k)).append("\":\"").append(esc(res.get(k))).append('"');
                }
                sb.append('}');
                return sb.toString();
            };

            case "P009" -> input -> {
                String date = jsonGetStr(input, "date");
                if (date == null) date = input;
                var m = cls.getMethod("normalizeDate", String.class);
                return ((String) m.invoke(null, date)).trim();
            };

            case "P010" -> input -> {
                String text = jsonGetStr(input, "text");
                if (text == null) text = input;
                var m = cls.getMethod("wordFrequency", String.class);
                @SuppressWarnings("unchecked")
                Map<String,Integer> res = (Map<String,Integer>) m.invoke(null, text);
                // sort by count desc, then alpha asc
                List<Map.Entry<String,Integer>> entries = new ArrayList<>(res.entrySet());
                entries.sort((a, b) -> {
                    int c = b.getValue() - a.getValue();
                    return c != 0 ? c : a.getKey().compareTo(b.getKey());
                });
                StringBuilder sb = new StringBuilder("[");
                boolean first = true;
                for (var e : entries) {
                    if (!first) sb.append(',');
                    first = false;
                    sb.append("[\"").append(esc(e.getKey())).append("\",").append(e.getValue()).append("]");
                }
                sb.append(']');
                return sb.toString();
            };

            // ── P011-P020: Validation & Sanitisation ─────────────────────
            case "P011" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("isValidEmail", String.class);
                boolean res = (boolean) m.invoke(null, s);
                return res ? "true" : "false";
            };

            case "P012" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("isValidPassword", String.class);
                boolean res = (boolean) m.invoke(null, s);
                return res ? "true" : "false";
            };

            case "P013" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("isValidRange", String.class);
                return (String) m.invoke(null, s);
            };

            case "P014" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("isValidIPv4", String.class);
                boolean res = (boolean) m.invoke(null, s);
                return res ? "true" : "false";
            };

            case "P015" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("isValidUsername", String.class);
                boolean res = (boolean) m.invoke(null, s);
                return res ? "true" : "false";
            };

            case "P016" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("escapeHtml", String.class);
                return (String) m.invoke(null, s);
            };

            case "P017" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("escapeCsvCell", String.class);
                return (String) m.invoke(null, s);
            };

            case "P018" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("escapeJsonString", String.class);
                return (String) m.invoke(null, s);
            };

            case "P019" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("encodeUrlComponent", String.class);
                return (String) m.invoke(null, s);
            };

            case "P020" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("sanitizeTemplate", String.class);
                return (String) m.invoke(null, s);
            };

            // ── P021-P030: Path Safety & SQL ─────────────────────────────
            case "P021" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("safePathNormalize", String.class);
                return (String) m.invoke(null, s);
            };

            case "P022" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("isAllowedExtension", String.class);
                boolean res = (boolean) m.invoke(null, s);
                return res ? "true" : "false";
            };

            case "P023" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("sanitizeFilename", String.class);
                return (String) m.invoke(null, s);
            };

            case "P024" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("checkArchiveEntry", String.class);
                return (String) m.invoke(null, s);
            };

            case "P025" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("isAllowedFiletype", String.class);
                boolean res = (boolean) m.invoke(null, s);
                return res ? "true" : "false";
            };

            case "P026" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("isValidSqlIdentifier", String.class);
                boolean res = (boolean) m.invoke(null, s);
                return res ? "true" : "false";
            };

            case "P027" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("escapeSqlString", String.class);
                return (String) m.invoke(null, s);
            };

            case "P028" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("buildParamQuery", String.class);
                return (String) m.invoke(null, s);
            };

            case "P029" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("validateSortDirection", String.class);
                return (String) m.invoke(null, s);
            };

            case "P030" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("isAllowedColumn", String.class);
                boolean res = (boolean) m.invoke(null, s);
                return res ? "true" : "false";
            };

            // ── P031-P040: Shell Safety, Config & Token ─────────────────
            case "P031" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("quoteShellArg", String.class);
                return (String) m.invoke(null, s);
            };

            case "P032" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("isAllowedCommand", String.class);
                boolean res = (boolean) m.invoke(null, s);
                return res ? "true" : "false";
            };

            case "P033" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("detectShellMeta", String.class);
                return (String) m.invoke(null, s);
            };

            case "P034" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("isValidEnvVar", String.class);
                boolean res = (boolean) m.invoke(null, s);
                return res ? "true" : "false";
            };

            case "P035" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("splitArgs", String.class);
                @SuppressWarnings("unchecked")
                java.util.List<String> res = (java.util.List<String>) m.invoke(null, s);
                // serialise as JSON array
                StringBuilder sb2 = new StringBuilder("[");
                boolean first2 = true;
                for (String tok : res) {
                    if (!first2) sb2.append(',');
                    first2 = false;
                    sb2.append('"').append(esc(tok)).append('"');
                }
                sb2.append(']');
                return sb2.toString();
            };

            case "P036" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("parseSafeLiteral", String.class);
                return (String) m.invoke(null, s);
            };

            case "P037" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("parseConfigBool", String.class);
                return (String) m.invoke(null, s);
            };

            case "P038" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("isAllowedConfigKey", String.class);
                boolean res = (boolean) m.invoke(null, s);
                return res ? "true" : "false";
            };

            case "P039" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("validateToken", String.class);
                return (String) m.invoke(null, s);
            };

            case "P040" -> input -> {
                String s = jsonGetStr(input, "input");
                if (s == null) s = input;
                var m = cls.getMethod("validateNumericExpr", String.class);
                return (String) m.invoke(null, s);
            };

            // ── P041-P050: Algorithms, Auth & Scope ─────────────────────
            case "P041" -> input -> {
                int[] nums = parseArrayField(input, "nums");
                var m = cls.getMethod("frequencyCounter", int[].class);
                @SuppressWarnings("unchecked")
                java.util.Map<Integer,Integer> res = (java.util.Map<Integer,Integer>) m.invoke(null, (Object) nums);
                List<Integer> keys = new ArrayList<>(res.keySet()); Collections.sort(keys);
                StringBuilder sb2 = new StringBuilder("{");
                boolean f2=true;
                for(int k:keys){ if(!f2)sb2.append(','); f2=false; sb2.append('"').append(k).append("\":").append(res.get(k)); }
                sb2.append('}'); return sb2.toString();
            };

            case "P042" -> input -> {
                int[] nums = parseArrayField(input, "nums");
                var m = cls.getMethod("hasDuplicate", int[].class);
                boolean res = (boolean) m.invoke(null, (Object) nums);
                return res ? "true" : "false";
            };

            case "P043" -> input -> {
                int[] nums = parseArrayField(input, "nums");
                var m = cls.getMethod("streamingSum", int[].class);
                long res = (long) m.invoke(null, (Object) nums);
                return String.valueOf(res);
            };

            case "P044" -> input -> {
                String log2 = jsonGetStr(input, "log");
                if (log2 == null) log2 = "";
                String maxLinesStr = jsonGetStr(input, "max_lines");
                int maxLines = maxLinesStr != null ? Integer.parseInt(maxLinesStr) : 0;
                var m = cls.getMethod("boundedLogProcessor", String.class, int.class);
                @SuppressWarnings("unchecked")
                java.util.Map<String,Integer> res = (java.util.Map<String,Integer>) m.invoke(null, log2, maxLines);
                return "{\"kept\":" + res.get("kept") + ",\"total_words\":" + res.get("total_words") + "}";
            };

            case "P045" -> input -> {
                int[] nums = parseArrayField(input, "nums");
                int k2 = Integer.parseInt(jsonGetStr(input, "k"));
                var m = cls.getMethod("topKFrequent", int[].class, int.class);
                int[] res = (int[]) m.invoke(null, nums, k2);
                return serIntArray(res);
            };

            case "P046" -> input -> {
                String tok = jsonGetStr(input, "token");
                if (tok == null) tok = "";
                var m = cls.getMethod("validateTokenFormat", String.class);
                return (String) m.invoke(null, tok);
            };

            case "P047" -> input -> {
                String role = jsonGetStr(input, "role");
                String action = jsonGetStr(input, "action");
                if (role == null) role = ""; if (action == null) action = "";
                var m = cls.getMethod("evaluatePermission", String.class, String.class);
                return (String) m.invoke(null, role, action);
            };

            case "P048" -> input -> {
                String role = jsonGetStr(input, "role");
                String perm = jsonGetStr(input, "permission");
                if (role == null) role = ""; if (perm == null) perm = "";
                var m = cls.getMethod("roleHasPermission", String.class, String.class);
                boolean res = (boolean) m.invoke(null, role, perm);
                return res ? "true" : "false";
            };

            case "P049" -> input -> {
                int lastActive = Integer.parseInt(jsonGetStr(input, "last_active"));
                int currentTime = Integer.parseInt(jsonGetStr(input, "current_time"));
                int timeout2 = Integer.parseInt(jsonGetStr(input, "timeout"));
                var m = cls.getMethod("checkSession", int.class, int.class, int.class);
                return (String) m.invoke(null, lastActive, currentTime, timeout2);
            };

            case "P050" -> input -> {
                String requested = jsonGetStr(input, "requested");
                if (requested == null) requested = "";
                // parse allowed array
                int ai = input.indexOf("\"allowed\"");
                int ab = input.indexOf('[', ai);
                int ae = input.indexOf(']', ab);
                String arrStr = input.substring(ab+1, ae).trim();
                java.util.List<String> allowed = new ArrayList<>();
                if (!arrStr.isEmpty()) {
                    for (String part : arrStr.split(",")) {
                        String p = part.trim();
                        if (p.startsWith("\"") && p.endsWith("\"")) allowed.add(p.substring(1,p.length()-1));
                        else if (!p.isEmpty()) allowed.add(p);
                    }
                }
                var m = cls.getMethod("validateScope", String.class, java.util.List.class);
                return (String) m.invoke(null, requested, allowed);
            };

            default -> throw new IllegalArgumentException("Unknown problem: " + PROBLEM_ID);
        };
    }

    // ── main ─────────────────────────────────────────────────────────────
    public static void main(String[] args) throws Exception {
        List<String[]> cases = readCases(args[0]);
        StringBuilder sb = new StringBuilder("{\"cases\":[");
        boolean first = true;
        Class<?> cls;
        Invoker invoker;
        try {
            cls = Class.forName("Solution");
            invoker = makeInvoker(cls);
        } catch (Exception e) {
            for (int i = 0; i < cases.size(); i++) {
                if (!first) sb.append(',');
                first = false;
                sb.append("{\"index\":").append(i)
                  .append(",\"status\":\"ERROR\",\"actual\":\"\",\"expected\":\"")
                  .append(esc(cases.get(i)[1]))
                  .append("\",\"error\":\"").append(esc(e.toString()))
                  .append("\",\"execution_time_ms\":null,\"stdout\":\"\",\"stderr\":\"\"}");
            }
            sb.append("]}");
            System.out.println(sb);
            return;
        }

        for (int i = 0; i < cases.size(); i++) {
            String inp = cases.get(i)[0];
            String expected = cases.get(i)[1];
            String status = "PASS";
            String actual = "";
            String err = null;
            double elapsedMs = -1;
            try {
                long t0 = System.nanoTime();
                actual = invoker.call(inp);
                elapsedMs = (System.nanoTime() - t0) / 1_000_000.0;
                if (!actual.equals(expected)) status = "FAIL";
            } catch (Exception ex) {
                status = "ERROR";
                err = ex.getCause() != null ? ex.getCause().toString() : ex.toString();
            }
            if (!first) sb.append(',');
            first = false;
            sb.append("{\"index\":").append(i)
              .append(",\"status\":\"").append(status).append("\"")
              .append(",\"actual\":\"").append(esc(actual)).append("\"")
              .append(",\"expected\":\"").append(esc(expected)).append("\"")
              .append(",\"error\":").append(err == null ? "null" : "\"" + esc(err) + "\"")
              .append(",\"execution_time_ms\":").append(elapsedMs < 0 ? "null" :
                  String.format(Locale.ROOT, "%.3f", elapsedMs))
              .append(",\"stdout\":\"\",\"stderr\":\"\"}");
        }
        sb.append("]}");
        System.out.println(sb);
    }
}
'''


CPP_TYPED_HARNESS = r'''
/*
 * Typed runner for LeetCode-style C++ problems.
 * Compiles alongside solution.cpp and dispatches per PROBLEM_ID.
 */
#include <bits/stdc++.h>
using namespace std;

// ── Problem: __PROBLEM_ID__ ──────────────────────────────────────────────
// Forward declarations — implemented in solution.cpp
#if defined(P001)
vector<int> twoSum(vector<int>& nums, int target);
#elif defined(P002)
int maxSubarray(vector<int>& nums);
#elif defined(P003)
int binarySearch(vector<int>& nums, int target);
#elif defined(P004)
vector<int> mergeSortedArrays(vector<int>& nums1, vector<int>& nums2);
#elif defined(P005)
bool isBalanced(const string& s);
#elif defined(P006)
int csvFieldCount(const string& line);
#elif defined(P007)
map<string,int> countLogLevels(const string& log);
#elif defined(P008)
map<string,string> parseKeyValue(const string& s);
#elif defined(P009)
string normalizeDate(const string& date);
#elif defined(P010)
vector<pair<string,int>> wordFrequency(const string& text);
#elif defined(P011)
bool isValidEmail(const string& email);
#elif defined(P012)
bool isValidPassword(const string& pw);
#elif defined(P013)
string isValidRange(const string& s);
#elif defined(P014)
bool isValidIPv4(const string& ip);
#elif defined(P015)
bool isValidUsername(const string& s);
#elif defined(P016)
string escapeHtml(const string& s);
#elif defined(P017)
string escapeCsvCell(const string& s);
#elif defined(P018)
string escapeJsonString(const string& s);
#elif defined(P019)
string encodeUrlComponent(const string& s);
#elif defined(P020)
string sanitizeTemplate(const string& s);
#elif defined(P021)
string safePathNormalize(const string& path);
#elif defined(P022)
bool isAllowedExtension(const string& path);
#elif defined(P023)
string sanitizeFilename(const string& name);
#elif defined(P024)
string checkArchiveEntry(const string& path);
#elif defined(P025)
bool isAllowedFiletype(const string& ext);
#elif defined(P026)
bool isValidSqlIdentifier(const string& name);
#elif defined(P027)
string escapeSqlString(const string& s);
#elif defined(P028)
string buildParamQuery(const string& s);
#elif defined(P029)
string validateSortDirection(const string& s);
#elif defined(P030)
bool isAllowedColumn(const string& col);
#elif defined(P031)
string quoteShellArg(const string& s);
#elif defined(P032)
bool isAllowedCommand(const string& s);
#elif defined(P033)
string detectShellMeta(const string& s);
#elif defined(P034)
bool isValidEnvVar(const string& name);
#elif defined(P035)
vector<string> splitArgs(const string& s);
#elif defined(P036)
string parseSafeLiteral(const string& s);
#elif defined(P037)
string parseConfigBool(const string& s);
#elif defined(P038)
bool isAllowedConfigKey(const string& key);
#elif defined(P039)
string validateToken(const string& s);
#elif defined(P040)
string validateNumericExpr(const string& s);
#elif defined(P041)
map<int,int> frequencyCounter(vector<int>& nums);
#elif defined(P042)
bool hasDuplicate(vector<int>& nums);
#elif defined(P043)
long long streamingSum(vector<int>& nums);
#elif defined(P044)
map<string,int> boundedLogProcessor(const string& log, int maxLines);
#elif defined(P045)
vector<int> topKFrequent(vector<int>& nums, int k);
#elif defined(P046)
string validateTokenFormat(const string& token);
#elif defined(P047)
string evaluatePermission(const string& role, const string& action);
#elif defined(P048)
bool roleHasPermission(const string& role, const string& permission);
#elif defined(P049)
string checkSession(int lastActive, int currentTime, int timeout);
#elif defined(P050)
string validateScope(const string& requested, vector<string>& allowed);
#endif

// ── Utilities ────────────────────────────────────────────────────────────
static string jesc(const string& s) {
    string o; o.reserve(s.size());
    for (char c : s) {
        if (c=='"') o+="\\\"";
        else if (c=='\\') o+="\\\\";
        else if (c=='\n') o+="\\n";
        else if (c=='\r') o+="\\r";
        else if (c=='\t') o+="\\t";
        else if (c=='\b') o+="\\b";
        else if (c=='\f') o+="\\f";
        else o+=c;
    }
    return o;
}

// Parse JSON int array "[1,2,3]"
static vector<int> parseIntArr(const string& s) {
    vector<int> v;
    string t = s; t.erase(remove(t.begin(),t.end(),' '),t.end());
    if (t=="[]") return v;
    t = t.substr(1, t.size()-2);
    stringstream ss(t); string tok;
    while (getline(ss, tok, ',')) v.push_back(stoi(tok));
    return v;
}

// Get a JSON field value (string or number) from a flat JSON object string
static string getField(const string& json, const string& key) {
    string search = "\"" + key + "\"";
    size_t ki = json.find(search);
    if (ki == string::npos) return "";
    size_t ci = json.find(':', ki + search.size()) + 1;
    while (ci < json.size() && json[ci]==' ') ci++;
    if (json[ci]=='"') {
        size_t s = ci+1, e = s;
        while (e < json.size()) {
            if (json[e]=='\\') { e+=2; continue; }
            if (json[e]=='"') break; e++;
        }
        string r = json.substr(s, e-s);
        // unescape
        string out;
        for (size_t i=0;i<r.size();i++) {
            if (r[i]=='\\' && i+1<r.size()) {
                char nx=r[i+1];
                if(nx=='n'){out+='\n';i++;}
                else if(nx=='t'){out+='\t';i++;}
                else if(nx=='"'){out+='"';i++;}
                else if(nx=='\\'){out+='\\';i++;}
                else out+=r[i];
            } else out+=r[i];
        }
        return out;
    }
    size_t e = ci;
    while (e < json.size() && json[e]!=',' && json[e]!='}') e++;
    return json.substr(ci, e-ci);
}

// Get array field as string "[...]"
static string getArrayField(const string& json, const string& key) {
    string search = "\"" + key + "\"";
    size_t ki = json.find(search);
    if (ki==string::npos) return "[]";
    size_t ci = json.find('[', ki);
    int depth=0; size_t e=ci;
    while (e<json.size()) {
        if(json[e]=='[') depth++;
        else if(json[e]==']') { depth--; if(depth==0) break; }
        e++;
    }
    return json.substr(ci, e-ci+1);
}

// Serialise vector<int> as "[1,2,3]"
static string serIntVec(const vector<int>& v) {
    string s="[";
    for(size_t i=0;i<v.size();i++){if(i)s+=",";s+=to_string(v[i]);}
    s+="]"; return s;
}

// ── Parse test cases from JSON file ─────────────────────────────────────
struct Case { string input, expected; };

static vector<Case> parseCases(const string& path) {
    ifstream f(path); if(!f) throw runtime_error("Cannot open "+path);
    ostringstream ss; ss<<f.rdbuf(); string content=ss.str();
    vector<Case> cases;
    size_t pos=0;
    while ((pos=content.find("\"input\":",pos))!=string::npos) {
        size_t ci = content.find(':',pos)+1;
        while(content[ci]==' ') ci++;
        string inp;
        if(content[ci]=='"') {
            size_t s=ci+1,e=s;
            while(e<content.size()){if(content[e]=='\\'){e+=2;continue;}if(content[e]=='"')break;e++;}
            string raw=content.substr(s,e-s);
            string out; for(size_t i=0;i<raw.size();i++){
                if(raw[i]=='\\' && i+1<raw.size()){
                    char nx=raw[i+1];
                    if(nx=='n'){out+='\n';i++;}else if(nx=='t'){out+='\t';i++;}
                    else if(nx=='"'){out+='"';i++;}else if(nx=='\\'){out+='\\';i++;}
                    else out+=raw[i];
                }else out+=raw[i];
            }
            inp=out; pos=e+1;
        } else {
            // object/array
            int depth=0; size_t e=ci; bool inS=false;
            while(e<content.size()){
                char ch=content[e];
                if(ch=='\\'){e+=2;continue;}
                if(ch=='"') inS=!inS;
                if(!inS){
                    if(ch=='{'||ch=='[') depth++;
                    else if(ch=='}'||ch==']'){depth--;if(depth<0)break;}
                    else if(ch==','&&depth==0) break;
                }
                e++;
            }
            inp=content.substr(ci,e-ci); pos=e;
        }
        size_t ep=content.find("\"expected\":",pos);
        size_t ec=content.find(':',ep)+1;
        while(content[ec]==' ') ec++;
        string exp;
        if(content[ec]=='"'){
            size_t s=ec+1,e=s;
            while(e<content.size()){if(content[e]=='\\'){e+=2;continue;}if(content[e]=='"')break;e++;}
            string raw=content.substr(s,e-s);
            string out; for(size_t i=0;i<raw.size();i++){
                if(raw[i]=='\\' && i+1<raw.size()){
                    char nx=raw[i+1];
                    if(nx=='n'){out+='\n';i++;}else if(nx=='t'){out+='\t';i++;}
                    else if(nx=='"'){out+='"';i++;}else if(nx=='\\'){out+='\\';i++;}
                    else out+=raw[i];
                }else out+=raw[i];
            }
            exp=out; pos=e+1;
        } else {
            int depth=0; size_t e=ec; bool inS=false;
            while(e<content.size()){
                char ch=content[e];
                if(ch=='\\'){e+=2;continue;}
                if(ch=='"') inS=!inS;
                if(!inS){
                    if(ch=='{'||ch=='[') depth++;
                    else if(ch=='}'||ch==']'){depth--;if(depth<0)break;}
                    else if(ch==','&&depth==0)break;
                }
                e++;
            }
            exp=content.substr(ec,e-ec); pos=e;
        }
        cases.push_back({inp,exp});
    }
    return cases;
}

// ── Invoke and serialise ─────────────────────────────────────────────────
static string invoke(const string& problem, const string& inp) {
#if defined(P001)
    auto nums = parseIntArr(getArrayField(inp,"nums"));
    int target = stoi(getField(inp,"target"));
    auto res = twoSum(nums, target);
    vector<int> sorted_res = res; sort(sorted_res.begin(), sorted_res.end());
    return serIntVec(sorted_res);
#elif defined(P002)
    auto nums = parseIntArr(getArrayField(inp,"nums"));
    return to_string(maxSubarray(nums));
#elif defined(P003)
    auto nums = parseIntArr(getArrayField(inp,"nums"));
    int target = stoi(getField(inp,"target"));
    return to_string(binarySearch(nums, target));
#elif defined(P004)
    auto n1 = parseIntArr(getArrayField(inp,"nums1"));
    auto n2 = parseIntArr(getArrayField(inp,"nums2"));
    return serIntVec(mergeSortedArrays(n1, n2));
#elif defined(P005)
    {
    string s = getField(inp,"s");
    if(s.empty() && inp.find("\"s\"") == string::npos) s=inp;
    return isBalanced(s) ? "true" : "false";
    }
#elif defined(P006)
    {
    string line = getField(inp,"line");
    if(line.empty() && inp.find("\"line\"") == string::npos) line=inp;
    return to_string(csvFieldCount(line));
    }
#elif defined(P007)
    {
    string log = getField(inp,"log");
    if(log.empty() && inp.find("\"log\"") == string::npos) log=inp;
    auto m = countLogLevels(log);
    return "{\"ERROR\":" + to_string(m["ERROR"]) +
           ",\"WARNING\":" + to_string(m["WARNING"]) +
           ",\"INFO\":"    + to_string(m["INFO"]) +
           ",\"DEBUG\":"   + to_string(m["DEBUG"]) + "}";
    }
#elif defined(P008)
    {
    string s = getField(inp,"s");
    if(s.empty() && inp.find("\"s\"") == string::npos) s=inp;
    auto m = parseKeyValue(s);
    vector<string> keys;
    for(auto& kv:m) keys.push_back(kv.first);
    sort(keys.begin(),keys.end());
    string out="{"; bool first=true;
    for(auto& k:keys){
        if(!first) out+=","; first=false;
        out+="\""+jesc(k)+"\":\""+jesc(m[k])+"\"";
    }
    out+="}"; return out;
    }
#elif defined(P009)
    {
    string d = getField(inp,"date");
    // only fall back if key not present at all
    if(d.empty() && inp.find("\"date\"") == string::npos) d=inp;
    string r = normalizeDate(d);
    while(!r.empty()&&(r.back()=='\n'||r.back()=='\r'||r.back()==' ')) r.pop_back();
    return r;
    }
#elif defined(P010)
    {
    string t = getField(inp,"text");
    // only fall back if key not present at all (empty string is a valid value)
    if(t.empty() && inp.find("\"text\"") == string::npos) t=inp;
    auto pairs = wordFrequency(t);
    string out="["; bool first=true;
    for(auto& p:pairs){
        if(!first) out+=","; first=false;
        out+="[\""+jesc(p.first)+"\","+to_string(p.second)+"]";
    }
    out+="]"; return out;
    }
#elif defined(P011)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return isValidEmail(s) ? "true" : "false";
    }
#elif defined(P012)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return isValidPassword(s) ? "true" : "false";
    }
#elif defined(P013)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    string r = isValidRange(s);
    while(!r.empty()&&(r.back()=='\n'||r.back()=='\r'||r.back()==' ')) r.pop_back();
    return r;
    }
#elif defined(P014)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return isValidIPv4(s) ? "true" : "false";
    }
#elif defined(P015)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return isValidUsername(s) ? "true" : "false";
    }
#elif defined(P016)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    string r = escapeHtml(s);
    return r;
    }
#elif defined(P017)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return escapeCsvCell(s);
    }
#elif defined(P018)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return escapeJsonString(s);
    }
#elif defined(P019)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return encodeUrlComponent(s);
    }
#elif defined(P020)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return sanitizeTemplate(s);
    }
#elif defined(P021)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return safePathNormalize(s);
    }
#elif defined(P022)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return isAllowedExtension(s) ? "true" : "false";
    }
#elif defined(P023)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return sanitizeFilename(s);
    }
#elif defined(P024)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return checkArchiveEntry(s);
    }
#elif defined(P025)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return isAllowedFiletype(s) ? "true" : "false";
    }
#elif defined(P026)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return isValidSqlIdentifier(s) ? "true" : "false";
    }
#elif defined(P027)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return escapeSqlString(s);
    }
#elif defined(P028)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return buildParamQuery(s);
    }
#elif defined(P029)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return validateSortDirection(s);
    }
#elif defined(P030)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return isAllowedColumn(s) ? "true" : "false";
    }
#elif defined(P031)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return quoteShellArg(s);
    }
#elif defined(P032)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return isAllowedCommand(s) ? "true" : "false";
    }
#elif defined(P033)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return detectShellMeta(s);
    }
#elif defined(P034)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return isValidEnvVar(s) ? "true" : "false";
    }
#elif defined(P035)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    auto tokens = splitArgs(s);
    string out="["; bool first=true;
    for(auto& t:tokens){ if(!first) out+=","; first=false; out+="\""+jesc(t)+"\""; }
    out+="]"; return out;
    }
#elif defined(P036)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return parseSafeLiteral(s);
    }
#elif defined(P037)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return parseConfigBool(s);
    }
#elif defined(P038)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return isAllowedConfigKey(s) ? "true" : "false";
    }
#elif defined(P039)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return validateToken(s);
    }
#elif defined(P040)
    {
    string s = getField(inp,"input");
    if(s.empty() && inp.find("\"input\"") == string::npos) s=inp;
    return validateNumericExpr(s);
    }
#elif defined(P041)
    {
    auto nums = parseIntArr(getArrayField(inp,"nums"));
    auto res = frequencyCounter(nums);
    vector<int> keys; for(auto& kv:res) keys.push_back(kv.first);
    sort(keys.begin(),keys.end());
    string out="{"; bool first=true;
    for(int k:keys){if(!first)out+=",";first=false;out+="\""+to_string(k)+"\":"+to_string(res[k]);}
    out+="}"; return out;
    }
#elif defined(P042)
    {
    auto nums = parseIntArr(getArrayField(inp,"nums"));
    return hasDuplicate(nums) ? "true" : "false";
    }
#elif defined(P043)
    {
    auto nums = parseIntArr(getArrayField(inp,"nums"));
    return to_string(streamingSum(nums));
    }
#elif defined(P044)
    {
    string log2 = getField(inp,"log");
    if(log2.empty() && inp.find("\"log\"") == string::npos) log2="";
    string ml = getField(inp,"max_lines");
    int maxLines = ml.empty() ? 0 : stoi(ml);
    auto res = boundedLogProcessor(log2, maxLines);
    return "{\"kept\":"+to_string(res["kept"])+",\"total_words\":"+to_string(res["total_words"])+"}";
    }
#elif defined(P045)
    {
    auto nums = parseIntArr(getArrayField(inp,"nums"));
    string ks = getField(inp,"k");
    int k2 = ks.empty() ? 0 : stoi(ks);
    auto res = topKFrequent(nums, k2);
    sort(res.begin(),res.end());
    return serIntVec(res);
    }
#elif defined(P046)
    {
    string tok = getField(inp,"token");
    if(tok.empty() && inp.find("\"token\"") == string::npos) tok="";
    return validateTokenFormat(tok);
    }
#elif defined(P047)
    {
    string role = getField(inp,"role");
    string action = getField(inp,"action");
    return evaluatePermission(role, action);
    }
#elif defined(P048)
    {
    string role = getField(inp,"role");
    string perm = getField(inp,"permission");
    return roleHasPermission(role, perm) ? "true" : "false";
    }
#elif defined(P049)
    {
    string la=getField(inp,"last_active"), ct=getField(inp,"current_time"), to2=getField(inp,"timeout");
    int lastActive=la.empty()?0:stoi(la), currentTime=ct.empty()?0:stoi(ct), timeout2=to2.empty()?0:stoi(to2);
    return checkSession(lastActive, currentTime, timeout2);
    }
#elif defined(P050)
    {
    string requested = getField(inp,"requested");
    // parse allowed array
    size_t ai=inp.find("\"allowed\"");
    vector<string> allowed;
    if(ai!=string::npos){
        size_t ab=inp.find('[',ai), ae=inp.find(']',ab);
        string arrStr=inp.substr(ab+1,ae-ab-1);
        stringstream ss2(arrStr); string tok;
        while(getline(ss2,tok,',')){
            string p=tok; 
            while(!p.empty()&&(p.front()==' '||p.front()=='"'))p.erase(p.begin());
            while(!p.empty()&&(p.back()==' '||p.back()=='"'))p.pop_back();
            if(!p.empty()) allowed.push_back(p);
        }
    }
    return validateScope(requested, allowed);
    }
#else
    throw runtime_error("Unknown problem");
#endif
}

// ── main ──────────────────────────────────────────────────────────────────
int main(int argc, char* argv[]) {
    if (argc < 2) { cerr << "Usage: runner testcases.json\n"; return 1; }
    string problem_id = "__PROBLEM_ID__";
    vector<Case> cases;
    try { cases = parseCases(argv[1]); }
    catch (exception& e) { cerr << "Failed to read cases: " << e.what() << "\n"; return 1; }

    ostringstream out;
    out << "{\"cases\":[";
    for (size_t i=0; i<cases.size(); i++) {
        const string& inp = cases[i].input;
        const string& expected = cases[i].expected;
        string status="PASS", actual, err;
        double elapsed=-1;
        try {
            auto t0=chrono::high_resolution_clock::now();
            actual = invoke(problem_id, inp);
            auto t1=chrono::high_resolution_clock::now();
            elapsed=chrono::duration<double,milli>(t1-t0).count();
            while(!actual.empty()&&(actual.back()=='\n'||actual.back()=='\r'||actual.back()==' '))
                actual.pop_back();
            if(actual!=expected) status="FAIL";
        } catch(exception& e){ status="ERROR"; err=e.what(); }
        catch(...){ status="ERROR"; err="unknown"; }
        if(i>0) out<<",";
        out<<"{\"index\":"<<i
           <<",\"status\":\""<<status<<"\""
           <<",\"actual\":\""<<jesc(actual)<<"\""
           <<",\"expected\":\""<<jesc(expected)<<"\""
           <<",\"error\":"<<(err.empty()?"null":"\""+jesc(err)+"\"")
           <<",\"execution_time_ms\":"<<(elapsed<0?"null":to_string(elapsed))
           <<",\"stdout\":\"\",\"stderr\":\"\"}";
    }
    out<<"]}";
    cout<<out.str()<<endl;
    return 0;
}
'''


JS_TYPED_HARNESS = r'''
'use strict';
const fs = require('fs');
const path = require('path');

const PROBLEM_ID = '__PROBLEM_ID__';
const sol = require(path.resolve('./solution.js'));

// ── Serialisation helpers ────────────────────────────────────────────────
function serIntArray(arr) {
    return '[' + arr.join(',') + ']';
}
function serSortedPairs(pairs) {
    return '[' + pairs.map(([k,v]) => `["${k}",${v}]`).join(',') + ']';
}

// ── Per-problem dispatcher ───────────────────────────────────────────────
function dispatch(inp, expected) {
    switch (PROBLEM_ID) {

    case 'P001': {
        const data = JSON.parse(inp);
        const res = sol.twoSum(data.nums, data.target);
        const sorted = [...res].sort((a,b)=>a-b);
        return serIntArray(sorted);
    }
    case 'P002': {
        const data = JSON.parse(inp);
        return String(sol.maxSubarray(data.nums));
    }
    case 'P003': {
        const data = JSON.parse(inp);
        return String(sol.binarySearch(data.nums, data.target));
    }
    case 'P004': {
        const data = JSON.parse(inp);
        return serIntArray(sol.mergeSortedArrays(data.nums1, data.nums2));
    }
    case 'P005': {
        const data = JSON.parse(inp);
        return sol.isBalanced(data.s) ? 'true' : 'false';
    }
    case 'P006': {
        const data = JSON.parse(inp);
        return String(sol.csvFieldCount(data.line));
    }
    case 'P007': {
        const data = JSON.parse(inp);
        const res = sol.countLogLevels(data.log);
        const d = {ERROR:0, WARNING:0, INFO:0, DEBUG:0, ...res};
        return JSON.stringify({ERROR:d.ERROR,WARNING:d.WARNING,INFO:d.INFO,DEBUG:d.DEBUG});
    }
    case 'P008': {
        const data = JSON.parse(inp);
        const res = sol.parseKeyValue(data.s);
        const sorted = Object.fromEntries(Object.entries(res).sort());
        return JSON.stringify(sorted);
    }
    case 'P009': {
        const data = JSON.parse(inp);
        return String(sol.normalizeDate(data.date)).trim();
    }
    case 'P010': {
        const data = JSON.parse(inp);
        const res = sol.wordFrequency(data.text);
        const pairs = Object.entries(res)
            .sort(([a,ca],[b,cb]) => cb-ca || a.localeCompare(b));
        return serSortedPairs(pairs);
    }
    // ── P011-P020: Validation & Sanitisation ────────────────────────────
    case 'P011': {
        const data = JSON.parse(inp);
        return sol.isValidEmail(data.input) ? 'true' : 'false';
    }
    case 'P012': {
        const data = JSON.parse(inp);
        return sol.isValidPassword(data.input) ? 'true' : 'false';
    }
    case 'P013': {
        const data = JSON.parse(inp);
        return String(sol.isValidRange(data.input));
    }
    case 'P014': {
        const data = JSON.parse(inp);
        return sol.isValidIPv4(data.input) ? 'true' : 'false';
    }
    case 'P015': {
        const data = JSON.parse(inp);
        return sol.isValidUsername(data.input) ? 'true' : 'false';
    }
    case 'P016': {
        const data = JSON.parse(inp);
        return String(sol.escapeHtml(data.input));
    }
    case 'P017': {
        const data = JSON.parse(inp);
        return String(sol.escapeCsvCell(data.input));
    }
    case 'P018': {
        const data = JSON.parse(inp);
        return String(sol.escapeJsonString(data.input));
    }
    case 'P019': {
        const data = JSON.parse(inp);
        return String(sol.encodeUrlComponent(data.input));
    }
    case 'P020': {
        const data = JSON.parse(inp);
        return String(sol.sanitizeTemplate(data.input));
    }
    // ── P021-P030: Path Safety & SQL ────────────────────────────────────
    case 'P021': {
        const data = JSON.parse(inp);
        return String(sol.safePathNormalize(data.input));
    }
    case 'P022': {
        const data = JSON.parse(inp);
        return sol.isAllowedExtension(data.input) ? 'true' : 'false';
    }
    case 'P023': {
        const data = JSON.parse(inp);
        return String(sol.sanitizeFilename(data.input));
    }
    case 'P024': {
        const data = JSON.parse(inp);
        return String(sol.checkArchiveEntry(data.input));
    }
    case 'P025': {
        const data = JSON.parse(inp);
        return sol.isAllowedFiletype(data.input) ? 'true' : 'false';
    }
    case 'P026': {
        const data = JSON.parse(inp);
        return sol.isValidSqlIdentifier(data.input) ? 'true' : 'false';
    }
    case 'P027': {
        const data = JSON.parse(inp);
        return String(sol.escapeSqlString(data.input));
    }
    case 'P028': {
        const data = JSON.parse(inp);
        return String(sol.buildParamQuery(data.input));
    }
    case 'P029': {
        const data = JSON.parse(inp);
        return String(sol.validateSortDirection(data.input));
    }
    case 'P030': {
        const data = JSON.parse(inp);
        return sol.isAllowedColumn(data.input) ? 'true' : 'false';
    }
    // ── P031-P040: Shell Safety, Config & Token ──────────────────────────
    case 'P031': {
        const data = JSON.parse(inp);
        return String(sol.quoteShellArg(data.input));
    }
    case 'P032': {
        const data = JSON.parse(inp);
        return sol.isAllowedCommand(data.input) ? 'true' : 'false';
    }
    case 'P033': {
        const data = JSON.parse(inp);
        return String(sol.detectShellMeta(data.input));
    }
    case 'P034': {
        const data = JSON.parse(inp);
        return sol.isValidEnvVar(data.input) ? 'true' : 'false';
    }
    case 'P035': {
        const data = JSON.parse(inp);
        const res = sol.splitArgs(data.input);
        return JSON.stringify(res);
    }
    case 'P036': {
        const data = JSON.parse(inp);
        return String(sol.parseSafeLiteral(data.input));
    }
    case 'P037': {
        const data = JSON.parse(inp);
        return String(sol.parseConfigBool(data.input));
    }
    case 'P038': {
        const data = JSON.parse(inp);
        return sol.isAllowedConfigKey(data.input) ? 'true' : 'false';
    }
    case 'P039': {
        const data = JSON.parse(inp);
        return String(sol.validateToken(data.input));
    }
    case 'P040': {
        const data = JSON.parse(inp);
        return String(sol.validateNumericExpr(data.input));
    }
    // ── P041-P050: Algorithms, Auth & Scope ─────────────────────────────
    case 'P041': {
        const data = JSON.parse(inp);
        const res = sol.frequencyCounter(data.nums);
        const sortedKeys = Object.keys(res).sort((a,b)=>parseInt(a)-parseInt(b));
        let out='{';
        sortedKeys.forEach((k,i)=>{if(i>0)out+=',';out+='"'+k+'":'+res[k];});
        out+='}';
        return out;
    }
    case 'P042': {
        const data = JSON.parse(inp);
        return sol.hasDuplicate(data.nums) ? 'true' : 'false';
    }
    case 'P043': {
        const data = JSON.parse(inp);
        return String(sol.streamingSum(data.nums));
    }
    case 'P044': {
        const data = JSON.parse(inp);
        const res = sol.boundedLogProcessor(data.log, data.max_lines);
        return JSON.stringify({kept:res.kept,total_words:res.total_words});
    }
    case 'P045': {
        const data = JSON.parse(inp);
        const res = sol.topKFrequent(data.nums, data.k);
        return JSON.stringify([...res].sort((a,b)=>a-b));
    }
    case 'P046': {
        const data = JSON.parse(inp);
        return String(sol.validateTokenFormat(data.token));
    }
    case 'P047': {
        const data = JSON.parse(inp);
        return String(sol.evaluatePermission(data.role, data.action));
    }
    case 'P048': {
        const data = JSON.parse(inp);
        return sol.roleHasPermission(data.role, data.permission) ? 'true' : 'false';
    }
    case 'P049': {
        const data = JSON.parse(inp);
        return String(sol.checkSession(data.last_active, data.current_time, data.timeout));
    }
    case 'P050': {
        const data = JSON.parse(inp);
        return String(sol.validateScope(data.requested, data.allowed));
    }
    default:
        throw new Error('Unknown problem: ' + PROBLEM_ID);
    }
}

// ── Run cases ────────────────────────────────────────────────────────────
const casesPath = process.argv[2];
const { cases } = JSON.parse(fs.readFileSync(casesPath, 'utf8'));
const results = [];

for (let i = 0; i < cases.length; i++) {
    const c = cases[i];
    const inp = String(c.input);
    const expected = String(c.expected);
    let status = 'PASS', actual = null, err = null, elapsed_ms = null;
    try {
        const t0 = process.hrtime.bigint();
        actual = dispatch(inp, expected);
        const t1 = process.hrtime.bigint();
        elapsed_ms = Number(t1 - t0) / 1e6;
        if (actual !== expected) status = 'FAIL';
    } catch(e) {
        status = 'ERROR';
        err = e && e.message ? e.message : String(e);
    }
    results.push({ index: i, status, actual, expected, error: err,
        execution_time_ms: elapsed_ms !== null ? Math.round(elapsed_ms*1000)/1000 : null,
        stdout: '', stderr: '' });
}
process.stdout.write(JSON.stringify({ cases: results }) + '\n');
'''
