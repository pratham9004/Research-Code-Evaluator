import java.util.*;
import java.util.regex.*;

public class Solution {

    // ==============================
    // P001 — Two Sum
    // ==============================
    public static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int comp = target - nums[i];
            if (map.containsKey(comp)) return new int[] { map.get(comp), i };
            map.put(nums[i], i);
        }
        return new int[0];
    }

    // ==============================
    // P002 — Maximum Subarray Sum
    // ==============================
    public static int maxSubarray(int[] nums) {
        int maxSoFar = nums[0], currMax = nums[0];
        for (int i = 1; i < nums.length; i++) {
            currMax = Math.max(nums[i], currMax + nums[i]);
            maxSoFar = Math.max(maxSoFar, currMax);
        }
        return maxSoFar;
    }

    // ==============================
    // P003 — Binary Search
    // ==============================
    public static int binarySearch(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) return mid;
            if (nums[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }

    // ==============================
    // P004 — Merge Sorted Arrays
    // ==============================
    public static int[] mergeSortedArrays(int[] nums1, int[] nums2) {
        int[] res = new int[nums1.length + nums2.length];
        int i = 0, j = 0, k = 0;
        while (i < nums1.length && j < nums2.length) {
            if (nums1[i] <= nums2[j]) res[k++] = nums1[i++];
            else res[k++] = nums2[j++];
        }
        while (i < nums1.length) res[k++] = nums1[i++];
        while (j < nums2.length) res[k++] = nums2[j++];
        return res;
    }

    // ==============================
    // P005 — Balanced Brackets
    // ==============================
    public static boolean isBalanced(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (c == '(' || c == '{' || c == '[') stack.push(c);
            else {
                if (stack.isEmpty()) return false;
                char top = stack.pop();
                if ((c == ')' && top != '(') || (c == '}' && top != '{') || (c == ']' && top != '[')) return false;
            }
        }
        return stack.isEmpty();
    }

    // ==============================
    // P006 — CSV Record Field Count
    // ==============================
    public static int csvFieldCount(String line) {
        if (line == null || line.isEmpty()) return 0;
        int count = 1;
        boolean inQuotes = false;
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (c == '"') inQuotes = !inQuotes;
            else if (c == ',' && !inQuotes) count++;
        }
        return count;
    }

    // ==============================
    // P007 — Log Level Counter
    // ==============================
    public static Map<String, Integer> countLogLevels(String log) {
        Map<String, Integer> res = new HashMap<>();
        res.put("ERROR", 0); res.put("WARNING", 0); res.put("INFO", 0); res.put("DEBUG", 0);
        if (log == null || log.isEmpty()) return res;
        for (String line : log.split("\\r?\\n")) {
            String trimmed = line.trim();
            for (String level : res.keySet()) {
                if (trimmed.startsWith(level + " ") || trimmed.startsWith(level + ":")) {
                    res.put(level, res.get(level) + 1);
                    break;
                }
            }
        }
        return res;
    }

    // ==============================
    // P008 — Key-Value Parser
    // ==============================
    public static Map<String, String> parseKeyValue(String s) {
        Map<String, String> map = new TreeMap<>();
        if (s == null || s.trim().isEmpty()) return map;
        for (String pair : s.split(",")) {
            int idx = pair.indexOf('=');
            if (idx != -1) {
                map.put(pair.substring(0, idx).trim(), pair.substring(idx + 1).trim());
            }
        }
        return map;
    }

    // ==============================
    // P009 — Date Format Normalizer
    // ==============================
    public static String normalizeDate(String date) {
        String d = date.trim();
        if (d.contains("/")) {
            String[] p = d.split("/");
            return String.format("%s-%02d-%02d", p[2], Integer.parseInt(p[0]), Integer.parseInt(p[1]));
        } else if (d.contains("-")) {
            String[] p = d.split("-");
            return String.format("%s-%02d-%02d", p[2], Integer.parseInt(p[1]), Integer.parseInt(p[0]));
        } else if (d.contains(".")) {
            String[] p = d.split("\\.");
            return String.format("%s-%02d-%02d", p[0], Integer.parseInt(p[1]), Integer.parseInt(p[2]));
        }
        return d;
    }

    // ==============================
    // P010 — Word Frequency
    // ==============================
    public static Map<String, Integer> wordFrequency(String text) {
        Map<String, Integer> counts = new HashMap<>();
        Matcher m = Pattern.compile("[a-zA-Z]+").matcher(text.toLowerCase());
        while (m.find()) {
            String w = m.group();
            counts.put(w, counts.getOrDefault(w, 0) + 1);
        }
        return counts;
    }

    // ==============================
    // P011 — Email Validator
    // ==============================
    public static boolean isValidEmail(String email) {
        if (email == null) return false;
        String[] parts = email.split("@", -1);
        if (parts.length != 2) return false;
        String local = parts[0], domain = parts[1];
        if (local.isEmpty() || local.startsWith(".") || local.endsWith(".") || local.contains("..")) return false;
        if (!local.matches("^[a-zA-Z0-9._%+-]+$")) return false;
        String[] dParts = domain.split("\\.", -1);
        if (dParts.length < 2) return false;
        if (!dParts[dParts.length - 1].matches("^[a-zA-Z]{2,6}$")) return false;
        for (String p : dParts) {
            if (p.isEmpty() || p.startsWith("-") || p.endsWith("-") || !p.matches("^[a-zA-Z0-9-]+$")) return false;
        }
        return true;
    }

    // ==============================
    // P012 — Password Policy Validator
    // ==============================
    public static boolean isValidPassword(String password) {
        if (password == null || password.length() < 8) return false;
        boolean u = false, l = false, d = false, s = false;
        for (char c : password.toCharArray()) {
            if (Character.isUpperCase(c)) u = true;
            else if (Character.isLowerCase(c)) l = true;
            else if (Character.isDigit(c)) d = true;
            else if ("!@#$%^&*".indexOf(c) != -1) s = true;
        }
        return u && l && d && s;
    }

    // ==============================
    // P013 — Integer Range Validator
    // ==============================
    public static String isValidRange(String s) {
        if (s == null) return "INVALID";
        String[] p = s.split("\\|", -1);
        if (p.length != 3) return "INVALID";
        try {
            int val = Integer.parseInt(p[0]), min = Integer.parseInt(p[1]), max = Integer.parseInt(p[2]);
            return (val >= min && val <= max) ? "VALID" : "INVALID";
        } catch (NumberFormatException e) {
            return "INVALID";
        }
    }

    // ==============================
    // P014 — IPv4 Validator
    // ==============================
    public static boolean isValidIPv4(String ip) {
        if (ip == null) return false;
        String[] parts = ip.split("\\.", -1);
        if (parts.length != 4) return false;
        for (String p : parts) {
            if (!p.matches("\\d+")) return false;
            if (p.length() > 1 && p.startsWith("0")) return false;
            try {
                int val = Integer.parseInt(p);
                if (val < 0 || val > 255) return false;
            } catch (NumberFormatException e) {
                return false;
            }
        }
        return true;
    }

    // ==============================
    // P015 — Username Validator
    // ==============================
    public static boolean isValidUsername(String username) {
        if (username == null || username.length() < 3 || username.length() > 20) return false;
        return username.matches("^[a-zA-Z][a-zA-Z0-9_-]*$");
    }

    // ==============================
    // P016 — HTML Text Escaper
    // ==============================
    public static String escapeHtml(String s) {
        if (s == null) return "";
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&#39;");
    }

    // ==============================
    // P017 — CSV Cell Escaper
    // ==============================
    public static String escapeCsvCell(String s) {
        if (s == null) return "";
        if (s.contains(",") || s.contains("\"") || s.contains("\n") || s.contains("\r")) {
            return "\"" + s.replace("\"", "\"\"") + "\"";
        }
        return s;
    }

    // ==============================
    // P018 — JSON String Escaper
    // ==============================
    public static String escapeJsonString(String s) {
        if (s == null) return "";
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '"') sb.append("\\\"");
            else if (c == '\\') sb.append("\\\\");
            else if (c == '/') sb.append("\\/");
            else if (c == '\b') sb.append("\\b");
            else if (c == '\f') sb.append("\\f");
            else if (c == '\n') sb.append("\\n");
            else if (c == '\r') sb.append("\\r");
            else if (c == '\t') sb.append("\\t");
            else if (c < 32) sb.append(String.format("\\u%04x", (int) c));
            else sb.append(c);
        }
        return sb.toString();
    }

    // ==============================
    // P019 — URL Query Component Encoder
    // ==============================
    public static String encodeUrlComponent(String s) {
        if (s == null) return "";
        StringBuilder sb = new StringBuilder();
        byte[] bytes = s.getBytes(java.nio.charset.StandardCharsets.UTF_8);
        String unreserved = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~";
        for (byte b : bytes) {
            char c = (char) (b & 0xFF);
            if (unreserved.indexOf(c) != -1) sb.append(c);
            else sb.append(String.format("%%%02X", b & 0xFF));
        }
        return sb.toString();
    }

    // ==============================
    // P020 — Template Placeholder Sanitizer
    // ==============================
    public static String sanitizeTemplate(String s) {
        if (s == null) return "";
        Matcher m = Pattern.compile("\\{\\{(.*?)\\}\\}").matcher(s);
        StringBuffer sb = new StringBuffer();
        while (m.find()) {
            String key = m.group(1);
            if (key != null && key.matches("^[a-zA-Z0-9_]+$")) {
                m.appendReplacement(sb, Matcher.quoteReplacement(m.group(0)));
            } else {
                m.appendReplacement(sb, "");
            }
        }
        m.appendTail(sb);
        return sb.toString();
    }

    // ==============================
    // P021 — Safe Path Normalizer
    // ==============================
    public static String safePathNormalize(String path) {
        if (path == null || path.trim().isEmpty() || path.contains("\\")) return "";
        String[] parts = path.split("/");
        List<String> stack = new ArrayList<>();
        for (String p : parts) {
            if (p.isEmpty() || p.equals(".")) continue;
            if (p.equals("..")) {
                if (stack.isEmpty()) return "";
                stack.remove(stack.size() - 1);
            } else {
                stack.add(p);
            }
        }
        return String.join("/", stack);
    }

    // ==============================
    // P022 — Path Extension Validator
    // ==============================
    public static boolean isAllowedExtension(String path) {
        if (path == null) return false;
        Set<String> allowed = new HashSet<>(Arrays.asList(".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".csv"));
        String fn = path.replace('\\', '/');
        int slash = fn.lastIndexOf('/');
        if (slash != -1) fn = fn.substring(slash + 1);
        if (fn.isEmpty()) return false;
        int dot = fn.lastIndexOf('.');
        if (dot == -1 || dot == 0) return false;
        return allowed.contains(fn.substring(dot).toLowerCase());
    }

    // ==============================
    // P023 — Filename Sanitizer
    // ==============================
    public static String sanitizeFilename(String name) {
        if (name == null || name.isEmpty()) return "_";
        String s = name.substring(0, Math.min(name.length(), 200));
        s = s.replaceAll("[^a-zA-Z0-9._-]", "_");
        s = s.replaceAll("_+", "_");
        while (s.startsWith("_")) s = s.substring(1);
        while (s.endsWith("_")) s = s.substring(0, s.length() - 1);
        return s.isEmpty() ? "_" : s;
    }

    // ==============================
    // P024 — Archive Entry Path Checker
    // ==============================
    public static String checkArchiveEntry(String path) {
        if (path == null || path.isEmpty()) return "safe";
        if (path.startsWith("/") || path.contains("\\")) return "unsafe";
        int depth = 0;
        for (String p : path.split("/")) {
            if (p.isEmpty() || p.equals(".")) continue;
            if (p.equals("..")) {
                depth--;
                if (depth < 0) return "unsafe";
            } else depth++;
        }
        return "safe";
    }

    // ==============================
    // P025 — File Type Allowlist
    // ==============================
    public static boolean isAllowedFiletype(String ext) {
        if (ext == null) return false;
        Set<String> allowed = new HashSet<>(Arrays.asList("jpg", "jpeg", "png", "gif", "bmp", "pdf", "txt", "csv", "json", "xml"));
        String clean = ext.trim();
        if (clean.startsWith(".")) clean = clean.substring(1);
        return !clean.isEmpty() && allowed.contains(clean.toLowerCase());
    }

    // ==============================
    // P026 — SQL Identifier Validator
    // ==============================
    public static boolean isValidSqlIdentifier(String name) {
        return name != null && name.matches("^[a-zA-Z_][a-zA-Z0-9_]{0,63}$");
    }

    // ==============================
    // P027 — SQL String Literal Escaper
    // ==============================
    public static String escapeSqlString(String s) {
        if (s == null) return "";
        return s.replace("\\", "\\\\").replace("'", "''");
    }

    // ==============================
    // P028 — Parameterized Query Builder
    // ==============================
    public static String buildParamQuery(String s) {
        if (s == null) return "INVALID";
        int idx = s.indexOf('|');
        if (idx == -1 || idx != s.lastIndexOf('|')) return "INVALID";
        String table = s.substring(0, idx), conds = s.substring(idx + 1);
        String pattern = "^[a-zA-Z_][a-zA-Z0-9_]*$";
        if (!table.matches(pattern) || conds.isEmpty()) return "INVALID";
        List<String> cols = new ArrayList<>();
        for (String pair : conds.split(",")) {
            int eq = pair.indexOf('=');
            if (eq == -1) return "INVALID";
            String col = pair.substring(0, eq);
            if (!col.matches(pattern)) return "INVALID";
            cols.add(col + "=?");
        }
        return "SELECT * FROM " + table + " WHERE " + String.join(" AND ", cols);
    }

    // ==============================
    // P029 — Sort Direction Validator
    // ==============================
    public static String validateSortDirection(String s) {
        if (s == null) return "INVALID";
        String clean = s.trim().toUpperCase();
        return (clean.equals("ASC") || clean.equals("DESC")) ? clean : "INVALID";
    }

    // ==============================
    // P030 — Column Allowlist Checker
    // ==============================
    public static boolean isAllowedColumn(String col) {
        if (col == null) return false;
        Set<String> allowed = new HashSet<>(Arrays.asList("id", "name", "email", "created_at", "status", "age", "role", "score"));
        return allowed.contains(col.trim());
    }

    // ==============================
    // P031 — Shell Argument Quoter
    // ==============================
    public static String quoteShellArg(String s) {
        if (s == null) return "''";
        return "'" + s.replace("'", "'\\''") + "'";
    }

    // ==============================
    // P032 — Command Name Allowlist
    // ==============================
    public static boolean isAllowedCommand(String s) {
        if (s == null) return false;
        String clean = s.trim();
        if (clean.contains(" ")) return false;
        Set<String> allowed = new HashSet<>(Arrays.asList("ls", "cat", "echo", "grep", "find", "sort", "uniq", "wc", "head", "tail"));
        return allowed.contains(clean);
    }

    // ==============================
    // P033 — Shell Metacharacter Detector
    // ==============================
    public static String detectShellMeta(String s) {
        if (s == null) return "safe";
        String dangerous = ";|&$`><(){} \\\"'\n\r";
        for (char c : s.toCharArray()) {
            if (dangerous.indexOf(c) != -1) return "unsafe";
        }
        return "safe";
    }

    // ==============================
    // P034 — Environment Variable Name Validator
    // ==============================
    public static boolean isValidEnvVar(String name) {
        return name != null && name.length() >= 1 && name.length() <= 64 && name.matches("^[A-Z_][A-Z0-9_]*$");
    }

    // ==============================
    // P035 — Command Argument Splitter
    // ==============================
    public static List<String> splitArgs(String s) {
        List<String> res = new ArrayList<>();
        if (s == null || s.trim().isEmpty()) return res;
        StringBuilder curr = new StringBuilder();
        boolean inQuotes = false;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '"') {
                inQuotes = !inQuotes;
            } else if (c == ' ' && !inQuotes) {
                if (curr.length() > 0 || (i > 0 && s.charAt(i - 1) == '"')) {
                    res.add(curr.toString());
                    curr.setLength(0);
                }
            } else {
                curr.append(c);
            }
        }
        if (curr.length() > 0 || (s.length() > 0 && s.charAt(s.length() - 1) == '"')) {
            res.add(curr.toString());
        }
        return res;
    }

    // ==============================
    // P036 — Safe Literal Parser
    // ==============================
    public static String parseSafeLiteral(String s) {
        if (s == null) return "INVALID";
        if (s.equals("null") || s.equals("true") || s.equals("false")) return s;
        if (s.matches("^-?(0|[1-9][0-9]*)$")) return s;
        if (s.startsWith("\"") && s.endsWith("\"") && s.length() >= 2) {
            String inner = s.substring(1, s.length() - 1);
            StringBuilder sb = new StringBuilder();
            int i = 0;
            while (i < inner.length()) {
                char c = inner.charAt(i);
                if (c == '\\') {
                    if (i + 1 < inner.length() && inner.charAt(i + 1) == '"') {
                        sb.append('"');
                        i += 2;
                    } else return "INVALID";
                } else if (c == '"') return "INVALID";
                else {
                    sb.append(c);
                    i++;
                }
            }
            return sb.toString();
        }
        return "INVALID";
    }

    // ==============================
    // P037 — Configuration Boolean Parser
    // ==============================
    public static String parseConfigBool(String s) {
        if (s == null) return "INVALID";
        String clean = s.trim().toLowerCase();
        if (Arrays.asList("true", "yes", "1", "on", "enabled").contains(clean)) return "true";
        if (Arrays.asList("false", "no", "0", "off", "disabled").contains(clean)) return "false";
        return "INVALID";
    }

    // ==============================
    // P038 — Configuration Key Allowlist
    // ==============================
    public static boolean isAllowedConfigKey(String key) {
        if (key == null) return false;
        Set<String> allowed = new HashSet<>(Arrays.asList("host", "port", "database", "username", "password", "timeout", "max_connections", "ssl_enabled", "log_level", "retry_count"));
        return allowed.contains(key.trim());
    }

    // ==============================
    // P039 — Structured Token Decoder
    // ==============================
    public static String validateToken(String s) {
        if (s == null) return "invalid";
        String[] parts = s.split("\\.", -1);
        if (parts.length != 3) return "invalid";
        if (parts[0].matches("^[A-Za-z0-9_-]+$") && parts[1].matches("^[A-Za-z0-9_-]+$") && parts[2].matches("^[0-9a-f]{8}$")) {
            return "valid";
        }
        return "invalid";
    }

    // ==============================
    // P040 — Safe Numeric Expression Validator
    // ==============================
    public static String validateNumericExpr(String s) {
        if (s == null || s.trim().isEmpty()) return "invalid";
        String[] tokens = s.split("(?<=[+\\-*/])|(?=[+\\-*/])|\\s+");
        List<String> clean = new ArrayList<>();
        for (String t : tokens) if (!t.trim().isEmpty()) clean.add(t.trim());
        if (clean.isEmpty()) return "invalid";
        boolean expectNum = true;
        for (String t : clean) {
            if (expectNum) {
                if (!t.matches("^-?(0|[1-9][0-9]*)$")) return "invalid";
                expectNum = false;
            } else {
                if (!t.matches("^[+\\-*/]$")) return "invalid";
                expectNum = true;
            }
        }
        return expectNum ? "invalid" : "valid";
    }

    // ==============================
    // P041 — Frequency Counter Large Input
    // ==============================
    public static Map<Integer, Integer> frequencyCounter(int[] nums) {
        Map<Integer, Integer> map = new TreeMap<>();
        if (nums == null) return map;
        for (int x : nums) map.put(x, map.getOrDefault(x, 0) + 1);
        return map;
    }

    // ==============================
    // P042 — Duplicate Detector
    // ==============================
    public static boolean hasDuplicate(int[] nums) {
        if (nums == null) return false;
        Set<Integer> set = new HashSet<>();
        for (int x : nums) {
            if (!set.add(x)) return true;
        }
        return false;
    }

    // ==============================
    // P043 — Streaming Sum
    // ==============================
    public static long streamingSum(int[] nums) {
        if (nums == null) return 0;
        long sum = 0;
        for (int x : nums) sum += x;
        return sum;
    }

    // ==============================
    // P044 — Bounded Log Processor
    // ==============================
    public static Map<String, Integer> boundedLogProcessor(String log, int maxLines) {
        Map<String, Integer> res = new HashMap<>();
        if (log == null || maxLines <= 0) {
            res.put("kept", 0); res.put("total_words", 0);
            return res;
        }
        int kept = 0, words = 0;
        for (String line : log.split("\\r?\\n")) {
            if (!line.trim().isEmpty()) {
                kept++;
                words += line.trim().split("\\s+").length;
                if (kept == maxLines) break;
            }
        }
        res.put("kept", kept);
        res.put("total_words", words);
        return res;
    }

    // ==============================
    // P045 — Top-K Frequent Values
    // ==============================
    public static int[] topKFrequent(int[] nums, int k) {
        if (nums == null || nums.length == 0 || k <= 0) return new int[0];
        Map<Integer, Integer> counts = new HashMap<>();
        for (int x : nums) counts.put(x, counts.getOrDefault(x, 0) + 1);
        List<Integer> list = new ArrayList<>(counts.keySet());
        list.sort((a, b) -> {
            int fa = counts.get(a), fb = counts.get(b);
            if (fa != fb) return Integer.compare(fb, fa);
            return Integer.compare(a, b);
        });
        int size = Math.min(k, list.size());
        int[] res = new int[size];
        for (int i = 0; i < size; i++) res[i] = list.get(i);
        Arrays.sort(res);
        return res;
    }

    // ==============================
    // P046 — Token Format Validator
    // ==============================
    public static String validateTokenFormat(String token) {
        if (token == null || token.length() < 8 || token.length() > 32) return "invalid";
        return token.matches("^[a-zA-Z][a-zA-Z0-9\\-]{7,31}$") ? "valid" : "invalid";
    }

    // ==============================
    // P047 — Permission Rule Evaluator
    // ==============================
    public static String evaluatePermission(String role, String action) {
        if (role == null || action == null) return "denied";
        Map<String, Set<String>> perms = new HashMap<>();
        perms.put("admin", new HashSet<>(Arrays.asList("read", "write", "delete", "execute")));
        perms.put("editor", new HashSet<>(Arrays.asList("read", "write")));
        perms.put("viewer", new HashSet<>(Arrays.asList("read")));
        perms.put("guest", new HashSet<>());
        return (perms.containsKey(role) && perms.get(role).contains(action)) ? "allowed" : "denied";
    }

    // ==============================
    // P048 — Role Permission Checker
    // ==============================
    public static boolean roleHasPermission(String role, String permission) {
        return "allowed".equals(evaluatePermission(role, permission));
    }

    // ==============================
    // P049 — Session Timeout Checker
    // ==============================
    public static String checkSession(int lastActive, int currentTime, int timeout) {
        if (currentTime < lastActive) return "invalid";
        return (currentTime - lastActive > timeout) ? "expired" : "active";
    }

    // ==============================
    // P050 — Access Scope Validator
    // ==============================
    public static String validateScope(String requested, List<String> allowed) {
        if (requested == null || allowed == null || allowed.isEmpty()) return "denied";
        Set<String> set = new HashSet<>(allowed);
        if (set.contains(requested)) return "granted";
        String[] parts = requested.split(":");
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < parts.length - 1; i++) {
            if (i > 0) sb.append(":");
            sb.append(parts[i]);
            if (set.contains(sb.toString())) return "granted";
        }
        return "denied";
    }
}
