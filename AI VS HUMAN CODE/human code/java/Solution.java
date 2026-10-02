import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Solution {

    private static final Map<String, Set<String>> PERMISSION_TABLE = Map.of(
            "admin", Set.of("read", "write", "delete", "execute"),
            "editor", Set.of("read", "write"),
            "viewer", Set.of("read"),
            "guest", Set.of()
    );

    // P001: Two Sum
    public static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (seen.containsKey(complement)) {
                int a = seen.get(complement);
                int b = i;
                return a < b ? new int[]{a, b} : new int[]{b, a};
            }
            seen.put(nums[i], i);
        }
        return new int[0];
    }

    // P002: Maximum Subarray Sum
    public static int maxSubarray(int[] nums) {
        int best = nums[0];
        int current = nums[0];
        for (int i = 1; i < nums.length; i++) {
            current = Math.max(nums[i], current + nums[i]);
            best = Math.max(best, current);
        }
        return best;
    }

    // P003: Binary Search
    public static int binarySearch(int[] nums, int target) {
        int lo = 0, hi = nums.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] == target) return mid;
            if (nums[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }

    // P004: Merge Sorted Arrays
    public static int[] mergeSortedArrays(int[] nums1, int[] nums2) {
        int[] result = new int[nums1.length + nums2.length];
        int i = 0, j = 0, k = 0;
        while (i < nums1.length && j < nums2.length) {
            if (nums1[i] <= nums2[j]) result[k++] = nums1[i++];
            else result[k++] = nums2[j++];
        }
        while (i < nums1.length) result[k++] = nums1[i++];
        while (j < nums2.length) result[k++] = nums2[j++];
        return result;
    }

    // P005: Balanced Brackets
    public static boolean isBalanced(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        Map<Character, Character> pairs = Map.of(')', '(', ']', '[', '}', '{');
        for (char ch : s.toCharArray()) {
            if (ch == '(' || ch == '[' || ch == '{') {
                stack.push(ch);
            } else if (ch == ')' || ch == ']' || ch == '}') {
                if (stack.isEmpty() || stack.pop() != pairs.get(ch)) return false;
            }
        }
        return stack.isEmpty();
    }

    // P006: CSV Record Field Count
    public static int csvFieldCount(String line) {
        if (line.isEmpty()) return 0;
        int count = 1;
        boolean inQuotes = false;
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (c == '"') {
                if (inQuotes && i + 1 < line.length() && line.charAt(i + 1) == '"') {
                    i++;
                } else {
                    inQuotes = !inQuotes;
                }
            } else if (c == ',' && !inQuotes) {
                count++;
            }
        }
        return count;
    }

    // P007: Log Level Counter
    public static Map<String, Integer> countLogLevels(String log) {
        Map<String, Integer> levels = new LinkedHashMap<>();
        levels.put("ERROR", 0);
        levels.put("WARNING", 0);
        levels.put("INFO", 0);
        levels.put("DEBUG", 0);
        for (String line : log.split("\n", -1)) {
            for (String level : levels.keySet()) {
                if (line.startsWith(level + " ") || line.startsWith(level + ":")) {
                    levels.put(level, levels.get(level) + 1);
                    break;
                }
            }
        }
        return levels;
    }

    // P008: Key-Value Parser
    public static Map<String, String> parseKeyValue(String s) {
        Map<String, String> result = new TreeMap<>();
        if (s.isEmpty()) return result;
        for (String pair : s.split(",", -1)) {
            int idx = pair.indexOf('=');
            String key = pair.substring(0, idx).trim();
            String value = pair.substring(idx + 1).trim();
            result.put(key, value);
        }
        return result;
    }

    // P009: Date Format Normalizer
    public static String normalizeDate(String date) {
        if (date.contains("/")) {
            String[] parts = date.split("/");
            return parts[2] + "-" + parts[0] + "-" + parts[1];
        }
        if (date.contains("-")) {
            String[] parts = date.split("-");
            return parts[2] + "-" + parts[1] + "-" + parts[0];
        }
        String[] parts = date.split("\\.");
        return parts[0] + "-" + parts[1] + "-" + parts[2];
    }

    // P010: Word Frequency
    public static Map<String, Integer> wordFrequency(String text) {
        Map<String, Integer> counts = new HashMap<>();
        Matcher m = Pattern.compile("[A-Za-z]+").matcher(text.toLowerCase());
        while (m.find()) {
            String w = m.group();
            counts.put(w, counts.getOrDefault(w, 0) + 1);
        }
        List<Map.Entry<String, Integer>> entries = new ArrayList<>(counts.entrySet());
        entries.sort((a, b) -> {
            int cmp = b.getValue().compareTo(a.getValue());
            if (cmp != 0) return cmp;
            return a.getKey().compareTo(b.getKey());
        });
        Map<String, Integer> result = new LinkedHashMap<>();
        for (Map.Entry<String, Integer> e : entries) result.put(e.getKey(), e.getValue());
        return result;
    }

    // P011: Email Validator
    public static boolean isValidEmail(String email) {
        if (email.length() - email.replace("@", "").length() != 1) return false;
        String[] parts = email.split("@", -1);
        String local = parts[0];
        String domain = parts[1];
        if (!local.matches("[a-zA-Z0-9._%+-]+")) return false;
        if (local.startsWith(".") || local.endsWith(".") || local.contains("..")) return false;
        String[] labels = domain.split("\\.", -1);
        if (labels.length < 2) return false;
        for (String label : labels) {
            if (label.isEmpty() || label.startsWith("-") || label.endsWith("-")) return false;
            if (!label.matches("[a-zA-Z0-9-]+")) return false;
        }
        String tld = labels[labels.length - 1];
        return tld.matches("[a-zA-Z]{2,6}");
    }

    // P012: Password Policy Validator
    public static boolean isValidPassword(String password) {
        if (password.length() < 8) return false;
        if (!password.matches(".*[A-Z].*")) return false;
        if (!password.matches(".*[a-z].*")) return false;
        if (!password.matches(".*[0-9].*")) return false;
        if (!password.matches(".*[!@#$%^&*].*")) return false;
        return true;
    }

    // P013: Integer Range Validator
    public static String isValidRange(String s) {
        String[] parts = s.split("\\|", -1);
        if (parts.length != 3) return "INVALID";
        try {
            long value = Long.parseLong(parts[0]);
            long lo = Long.parseLong(parts[1]);
            long hi = Long.parseLong(parts[2]);
            return (lo <= value && value <= hi) ? "VALID" : "INVALID";
        } catch (NumberFormatException e) {
            return "INVALID";
        }
    }

    // P014: IPv4 Validator
    public static boolean isValidIPv4(String ip) {
        String[] parts = ip.split("\\.", -1);
        if (parts.length != 4) return false;
        for (String p : parts) {
            if (p.isEmpty() || !p.chars().allMatch(Character::isDigit)) return false;
            if (p.length() > 1 && p.charAt(0) == '0') return false;
            if (Integer.parseInt(p) > 255) return false;
        }
        return true;
    }

    // P015: Username Validator
    public static boolean isValidUsername(String username) {
        if (username.length() < 3 || username.length() > 20) return false;
        return username.matches("[A-Za-z][A-Za-z0-9_-]*");
    }

    // P016: HTML Text Escaper
    public static String escapeHtml(String s) {
        s = s.replace("&", "&amp;");
        s = s.replace("<", "&lt;");
        s = s.replace(">", "&gt;");
        s = s.replace("\"", "&quot;");
        s = s.replace("'", "&#39;");
        return s;
    }

    // P017: CSV Cell Escaper
    public static String escapeCsvCell(String s) {
        if (s.contains(",") || s.contains("\"") || s.contains("\n") || s.contains("\r")) {
            return "\"" + s.replace("\"", "\"\"") + "\"";
        }
        return s;
    }

    // P018: JSON String Escaper
    public static String escapeJsonString(String s) {
        StringBuilder sb = new StringBuilder();
        for (char ch : s.toCharArray()) {
            switch (ch) {
                case '"': sb.append("\\\""); break;
                case '\\': sb.append("\\\\"); break;
                case '/': sb.append("\\/"); break;
                case '\b': sb.append("\\b"); break;
                case '\f': sb.append("\\f"); break;
                case '\n': sb.append("\\n"); break;
                case '\r': sb.append("\\r"); break;
                case '\t': sb.append("\\t"); break;
                default:
                    if (ch < 0x20) sb.append(String.format("\\u%04x", (int) ch));
                    else sb.append(ch);
            }
        }
        return sb.toString();
    }

    // P019: URL Query Component Encoder
    public static String encodeUrlComponent(String s) {
        StringBuilder sb = new StringBuilder();
        byte[] bytes = s.getBytes(StandardCharsets.UTF_8);
        String unreserved = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~";
        for (byte b : bytes) {
            int v = b & 0xFF;
            char c = (char) v;
            if (v < 128 && unreserved.indexOf(c) >= 0) {
                sb.append(c);
            } else {
                sb.append(String.format("%%%02X", v));
            }
        }
        return sb.toString();
    }

    // P020: Template Placeholder Sanitizer
    public static String sanitizeTemplate(String s) {
        Pattern p = Pattern.compile("\\{\\{(.*?)\\}\\}");
        Matcher m = p.matcher(s);
        StringBuilder sb = new StringBuilder();
        while (m.find()) {
            String key = m.group(1);
            String replacement = key.matches("[a-zA-Z0-9_]+") ? "{{" + key + "}}" : "";
            m.appendReplacement(sb, Matcher.quoteReplacement(replacement));
        }
        m.appendTail(sb);
        return sb.toString();
    }

    // P021: Safe Path Normalizer
    public static String safePathNormalize(String path) {
        if (path.trim().isEmpty()) return "";
        Deque<String> stack = new ArrayDeque<>();
        for (String part : path.split("/", -1)) {
            if (part.isEmpty() || part.equals(".")) continue;
            if (part.equals("..")) {
                if (stack.isEmpty()) return "";
                stack.removeLast();
            } else {
                stack.addLast(part);
            }
        }
        return String.join("/", stack);
    }

    // P022: Path Extension Validator
    public static boolean isAllowedExtension(String path) {
        Set<String> allowed = Set.of(".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".csv");
        String normalized = path.replace("\\", "/");
        String filename = normalized.substring(normalized.lastIndexOf('/') + 1);
        int idx = filename.lastIndexOf('.');
        if (idx <= 0) return false;
        String ext = filename.substring(idx).toLowerCase();
        return allowed.contains(ext);
    }

    // P023: Filename Sanitizer
    public static String sanitizeFilename(String name) {
        String truncated = name.length() > 200 ? name.substring(0, 200) : name;
        String replaced = truncated.replaceAll("[^a-zA-Z0-9._-]", "_");
        String collapsed = replaced.replaceAll("_+", "_");
        String stripped = collapsed.replaceAll("^_+|_+$", "");
        return stripped.isEmpty() ? "_" : stripped;
    }

    // P024: Archive Entry Path Checker
    public static String checkArchiveEntry(String path) {
        if (path.isEmpty()) return "safe";
        if (path.startsWith("/")) return "unsafe";
        if (path.contains("\\")) return "unsafe";
        int depth = 0;
        for (String part : path.split("/", -1)) {
            if (part.isEmpty() || part.equals(".")) continue;
            if (part.equals("..")) {
                depth--;
                if (depth < 0) return "unsafe";
            } else {
                depth++;
            }
        }
        return "safe";
    }

    // P025: File Type Allowlist
    public static boolean isAllowedFiletype(String ext) {
        Set<String> allowed = Set.of("jpg", "jpeg", "png", "gif", "bmp", "pdf", "txt", "csv", "json", "xml");
        if (ext.isEmpty()) return false;
        String e = ext.startsWith(".") ? ext.substring(1) : ext;
        return allowed.contains(e.toLowerCase());
    }

    // P026: SQL Identifier Validator
    public static boolean isValidSqlIdentifier(String name) {
        if (name.length() < 1 || name.length() > 64) return false;
        return name.matches("[a-zA-Z_][a-zA-Z0-9_]*");
    }

    // P027: SQL String Literal Escaper
    public static String escapeSqlString(String s) {
        s = s.replace("\\", "\\\\");
        s = s.replace("'", "''");
        return s;
    }

    // P028: Parameterized Query Builder
    public static String buildParamQuery(String s) {
        long pipeCount = s.chars().filter(c -> c == '|').count();
        if (pipeCount != 1) return "INVALID";
        int idx = s.indexOf('|');
        String table = s.substring(0, idx);
        String cols = s.substring(idx + 1);
        if (!isValidSqlIdentifier(table)) return "INVALID";
        if (cols.isEmpty()) return "INVALID";
        List<String> conditions = new ArrayList<>();
        for (String pair : cols.split(",", -1)) {
            int eq = pair.indexOf('=');
            if (eq < 0) return "INVALID";
            String col = pair.substring(0, eq);
            if (!isValidSqlIdentifier(col)) return "INVALID";
            conditions.add(col + "=?");
        }
        return "SELECT * FROM " + table + " WHERE " + String.join(" AND ", conditions);
    }

    // P029: Sort Direction Validator
    public static String validateSortDirection(String s) {
        String t = s.trim().toUpperCase();
        return (t.equals("ASC") || t.equals("DESC")) ? t : "INVALID";
    }

    // P030: Column Allowlist Checker
    public static boolean isAllowedColumn(String col) {
        Set<String> allowed = Set.of("id", "name", "email", "created_at", "status", "age", "role", "score");
        return allowed.contains(col.trim());
    }

    // P031: Shell Argument Quoter
    public static String quoteShellArg(String s) {
        return "'" + s.replace("'", "'\\''") + "'";
    }

    // P032: Command Name Allowlist
    public static boolean isAllowedCommand(String s) {
        Set<String> allowed = Set.of("ls", "cat", "echo", "grep", "find", "sort", "uniq", "wc", "head", "tail");
        String t = s.trim();
        if (t.contains(" ")) return false;
        return allowed.contains(t);
    }

    // P033: Shell Metacharacter Detector
    public static String detectShellMeta(String s) {
        String dangerous = ";|&$`><(){}\\\"'\n\r";
        for (char c : s.toCharArray()) {
            if (dangerous.indexOf(c) >= 0) return "unsafe";
        }
        return "safe";
    }

    // P034: Environment Variable Name Validator
    public static boolean isValidEnvVar(String name) {
        if (name.length() < 1 || name.length() > 64) return false;
        return name.matches("[A-Z_][A-Z0-9_]*");
    }

    // P035: Command Argument Splitter
    public static List<String> splitArgs(String s) {
        List<String> tokens = new ArrayList<>();
        int i = 0, n = s.length();
        while (i < n) {
            while (i < n && s.charAt(i) == ' ') i++;
            if (i >= n) break;
            if (s.charAt(i) == '"') {
                int j = i + 1;
                int start = j;
                while (j < n && s.charAt(j) != '"') j++;
                tokens.add(s.substring(start, j));
                i = j + 1;
            } else {
                int start = i;
                while (i < n && s.charAt(i) != ' ') i++;
                tokens.add(s.substring(start, i));
            }
        }
        return tokens;
    }

    // P036: Safe Literal Parser
    public static String parseSafeLiteral(String s) {
        if (s.equals("true") || s.equals("false")) return s;
        if (s.equals("null")) return "null";
        if (s.matches("-?(0|[1-9][0-9]*)")) return s;
        if (s.length() >= 2 && s.charAt(0) == '"' && s.charAt(s.length() - 1) == '"') {
            String inner = s.substring(1, s.length() - 1);
            StringBuilder sb = new StringBuilder();
            int i = 0;
            while (i < inner.length()) {
                if (inner.charAt(i) == '\\' && i + 1 < inner.length() && inner.charAt(i + 1) == '"') {
                    sb.append('"');
                    i += 2;
                } else if (inner.charAt(i) == '"') {
                    return "INVALID";
                } else {
                    sb.append(inner.charAt(i));
                    i++;
                }
            }
            return sb.toString();
        }
        return "INVALID";
    }

    // P037: Configuration Boolean Parser
    public static String parseConfigBool(String s) {
        String t = s.trim().toLowerCase();
        Set<String> trueVals = Set.of("true", "yes", "1", "on", "enabled");
        Set<String> falseVals = Set.of("false", "no", "0", "off", "disabled");
        if (trueVals.contains(t)) return "true";
        if (falseVals.contains(t)) return "false";
        return "INVALID";
    }

    // P038: Configuration Key Allowlist
    public static boolean isAllowedConfigKey(String key) {
        Set<String> allowed = Set.of("host", "port", "database", "username", "password", "timeout",
                "max_connections", "ssl_enabled", "log_level", "retry_count");
        return allowed.contains(key.trim());
    }

    // P039: Structured Token Decoder
    public static String validateToken(String s) {
        String[] parts = s.split("\\.", -1);
        if (parts.length != 3) return "invalid";
        if (!parts[0].matches("[A-Za-z0-9_-]+")) return "invalid";
        if (!parts[1].matches("[A-Za-z0-9_-]+")) return "invalid";
        if (!parts[2].matches("[0-9a-f]{8}")) return "invalid";
        return "valid";
    }

    // P040: Safe Numeric Expression Validator
    public static String validateNumericExpr(String s) {
        String number = "-?(0|[1-9][0-9]*)";
        String pattern = "^\\s*" + number + "\\s*([+\\-*/]\\s*" + number + "\\s*)*$";
        return s.matches(pattern) ? "valid" : "invalid";
    }

    // P041: Frequency Counter Large Input
    public static Map<Integer, Integer> frequencyCounter(int[] nums) {
        Map<Integer, Integer> counts = new TreeMap<>();
        for (int n : nums) counts.put(n, counts.getOrDefault(n, 0) + 1);
        return counts;
    }

    // P042: Duplicate Detector
    public static boolean hasDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int n : nums) {
            if (!seen.add(n)) return true;
        }
        return false;
    }

    // P043: Streaming Sum
    public static long streamingSum(int[] nums) {
        long sum = 0;
        for (int n : nums) sum += n;
        return sum;
    }

    // P044: Bounded Log Processor
    public static Map<String, Integer> boundedLogProcessor(String log, int maxLines) {
        Map<String, Integer> result = new LinkedHashMap<>();
        if (maxLines <= 0 || log.isEmpty()) {
            result.put("kept", 0);
            result.put("total_words", 0);
            return result;
        }
        int kept = 0, totalWords = 0;
        for (String line : log.split("\n", -1)) {
            if (line.trim().isEmpty()) continue;
            if (kept >= maxLines) break;
            kept++;
            totalWords += line.trim().split("\\s+").length;
        }
        result.put("kept", kept);
        result.put("total_words", totalWords);
        return result;
    }

    // P045: Top-K Frequent Values
    public static int[] topKFrequent(int[] nums, int k) {
        if (k <= 0 || nums.length == 0) return new int[0];
        Map<Integer, Integer> counts = new HashMap<>();
        for (int n : nums) counts.put(n, counts.getOrDefault(n, 0) + 1);
        List<Integer> keys = new ArrayList<>(counts.keySet());
        keys.sort((a, b) -> {
            int cmp = counts.get(b) - counts.get(a);
            if (cmp != 0) return cmp;
            return a - b;
        });
        List<Integer> top = new ArrayList<>(keys.subList(0, Math.min(k, keys.size())));
        Collections.sort(top);
        int[] result = new int[top.size()];
        for (int i = 0; i < result.length; i++) result[i] = top.get(i);
        return result;
    }

    // P046: Token Format Validator
    public static String validateTokenFormat(String token) {
        return token.matches("[a-zA-Z][a-zA-Z0-9-]{7,31}") ? "valid" : "invalid";
    }

    // P047: Permission Rule Evaluator
    public static String evaluatePermission(String role, String action) {
        Set<String> perms = PERMISSION_TABLE.getOrDefault(role, Set.of());
        return perms.contains(action) ? "allowed" : "denied";
    }

    // P048: Role Permission Checker
    public static boolean roleHasPermission(String role, String permission) {
        Set<String> perms = PERMISSION_TABLE.getOrDefault(role, Set.of());
        return perms.contains(permission);
    }

    // P049: Session Timeout Checker
    public static String checkSession(int lastActive, int currentTime, int timeout) {
        if (currentTime < lastActive) return "invalid";
        int elapsed = currentTime - lastActive;
        return elapsed > timeout ? "expired" : "active";
    }

    // P050: Access Scope Validator
    public static String validateScope(String requested, List<String> allowed) {
        if (allowed == null || allowed.isEmpty()) return "denied";
        String[] parts = requested.split(":", -1);
        StringBuilder prefix = new StringBuilder();
        for (int i = 0; i < parts.length; i++) {
            if (i > 0) prefix.append(":");
            prefix.append(parts[i]);
            if (allowed.contains(prefix.toString())) return "granted";
        }
        return "denied";
    }
}
