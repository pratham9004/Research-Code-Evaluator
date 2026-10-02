// P001: Two Sum
public class Solution {
    public static int[] twoSum(int[] nums, int target) {
        java.util.Map<Integer, Integer> seen = new java.util.HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (seen.containsKey(complement)) {
                int[] result = {seen.get(complement), i};
                java.util.Arrays.sort(result);
                return result;
            }
            seen.put(nums[i], i);
        }
        return new int[]{};
    }

    // P002: Maximum Subarray Sum
    public static int maxSubarray(int[] nums) {
        int maxSum = nums[0];
        int currentSum = nums[0];
        for (int i = 1; i < nums.length; i++) {
            currentSum = Math.max(nums[i], currentSum + nums[i]);
            maxSum = Math.max(maxSum, currentSum);
        }
        return maxSum;
    }

    // P003: Binary Search
    public static int binarySearch(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) return mid;
            else if (nums[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }

    // P004: Merge Sorted Arrays
    public static int[] mergeSortedArrays(int[] nums1, int[] nums2) {
        java.util.List<Integer> result = new java.util.ArrayList<>();
        int i = 0, j = 0;
        while (i < nums1.length && j < nums2.length) {
            if (nums1[i] <= nums2[j]) result.add(nums1[i++]);
            else result.add(nums2[j++]);
        }
        while (i < nums1.length) result.add(nums1[i++]);
        while (j < nums2.length) result.add(nums2[j++]);
        return result.stream().mapToInt(Integer::intValue).toArray();
    }

    // P005: Balanced Brackets
    public static boolean isBalanced(String s) {
        java.util.Stack<Character> stack = new java.util.Stack<>();
        java.util.Map<Character, Character> pairs = new java.util.HashMap<>();
        pairs.put(')', '(');
        pairs.put('}', '{');
        pairs.put(']', '[');
        for (char c : s.toCharArray()) {
            if (c == '(' || c == '{' || c == '[') stack.push(c);
            else if (c == ')' || c == '}' || c == ']') {
                if (stack.isEmpty() || stack.peek() != pairs.get(c)) return false;
                stack.pop();
            }
        }
        return stack.isEmpty();
    }

    // P006: CSV Record Field Count
    public static int csvFieldCount(String line) {
        if (line == null || line.isEmpty()) return 0;
        int count = 0;
        boolean inQuotes = false;
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (c == '"') {
                if (inQuotes && i + 1 < line.length() && line.charAt(i + 1) == '"') i++;
                else inQuotes = !inQuotes;
            } else if (c == ',' && !inQuotes) count++;
        }
        return count + 1;
    }

    // P007: Log Level Counter
    public static java.util.Map<String, Integer> countLogLevels(String log) {
        java.util.Map<String, Integer> result = new java.util.HashMap<>();
        result.put("ERROR", 0);
        result.put("WARNING", 0);
        result.put("INFO", 0);
        result.put("DEBUG", 0);
        if (log == null || log.isEmpty()) return result;
        String[] lines = log.split("\n");
        for (String line : lines) {
            line = line.trim();
            if (line.startsWith("ERROR ") || line.startsWith("ERROR:")) result.put("ERROR", result.get("ERROR") + 1);
            else if (line.startsWith("WARNING ") || line.startsWith("WARNING:")) result.put("WARNING", result.get("WARNING") + 1);
            else if (line.startsWith("INFO ") || line.startsWith("INFO:")) result.put("INFO", result.get("INFO") + 1);
            else if (line.startsWith("DEBUG ") || line.startsWith("DEBUG:")) result.put("DEBUG", result.get("DEBUG") + 1);
        }
        return result;
    }

    // P008: Key-Value Parser
    public static java.util.Map<String, String> parseKeyValue(String s) {
        java.util.Map<String, String> result = new java.util.TreeMap<>();
        if (s == null || s.isEmpty()) return result;
        String[] pairs = s.split(",");
        for (String pair : pairs) {
            int eq = pair.indexOf('=');
            if (eq != -1) {
                String key = pair.substring(0, eq).trim();
                String value = pair.substring(eq + 1).trim();
                result.put(key, value);
            }
        }
        return result;
    }

    // P009: Date Format Normalizer
    public static String normalizeDate(String date) {
        if (date.contains("/")) {
            String[] parts = date.split("/");
            return parts[2] + "-" + parts[0] + "-" + parts[1];
        } else if (date.contains("-")) {
            String[] parts = date.split("-");
            return parts[2] + "-" + parts[1] + "-" + parts[0];
        } else if (date.contains(".")) {
            String[] parts = date.split("\\.");
            return parts[0] + "-" + parts[1] + "-" + parts[2];
        }
        return date;
    }

    // P010: Word Frequency
    public static java.util.Map<String, Integer> wordFrequency(String text) {
        java.util.Map<String, Integer> freq = new java.util.HashMap<>();
        if (text == null || text.isEmpty()) return freq;
        StringBuilder word = new StringBuilder();
        for (char c : text.toCharArray()) {
            if (Character.isLetter(c)) word.append(Character.toLowerCase(c));
            else if (word.length() > 0) {
                String w = word.toString();
                freq.put(w, freq.getOrDefault(w, 0) + 1);
                word.setLength(0);
            }
        }
        if (word.length() > 0) {
            String w = word.toString();
            freq.put(w, freq.getOrDefault(w, 0) + 1);
        }
        return freq;
    }

    // P011: Email Validator
    public static boolean isValidEmail(String email) {
        if (email == null) return false;
        int atCount = 0;
        for (char c : email.toCharArray()) if (c == '@') atCount++;
        if (atCount != 1) return false;
        int atPos = email.indexOf('@');
        String local = email.substring(0, atPos);
        String domain = email.substring(atPos + 1);
        if (local.isEmpty() || local.startsWith(".") || local.endsWith(".") || local.contains("..")) return false;
        for (char c : local.toCharArray()) {
            if (!("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._%+-".indexOf(c) >= 0)) return false;
        }
        if (domain.isEmpty() || domain.startsWith(".") || domain.endsWith(".")) return false;
        int lastDot = domain.lastIndexOf('.');
        if (lastDot <= 0) return false;
        String tld = domain.substring(lastDot + 1);
        if (tld.length() < 2 || tld.length() > 6) return false;
        for (char c : tld.toCharArray()) if (!Character.isLetter(c)) return false;
        String[] labels = domain.split("\\.");
        for (String label : labels) {
            if (label.isEmpty() || label.startsWith("-") || label.endsWith("-")) return false;
        }
        return true;
    }

    // P012: Password Policy Validator
    public static boolean isValidPassword(String password) {
        if (password == null || password.length() < 8) return false;
        boolean upper = false, lower = false, digit = false, special = false;
        for (char c : password.toCharArray()) {
            if (Character.isUpperCase(c)) upper = true;
            if (Character.isLowerCase(c)) lower = true;
            if (Character.isDigit(c)) digit = true;
            if ("!@#$%^&*".indexOf(c) >= 0) special = true;
        }
        return upper && lower && digit && special;
    }

    // P013: Integer Range Validator
    public static String isValidRange(String s) {
        if (s == null) return "INVALID";
        String[] parts = s.split("\\|");
        if (parts.length != 3) return "INVALID";
        try {
            int value = Integer.parseInt(parts[0]);
            int minVal = Integer.parseInt(parts[1]);
            int maxVal = Integer.parseInt(parts[2]);
            return (minVal <= value && value <= maxVal) ? "VALID" : "INVALID";
        } catch (NumberFormatException e) {
            return "INVALID";
        }
    }

    // P014: IPv4 Validator
    public static boolean isValidIPv4(String ip) {
        if (ip == null) return false;
        String[] parts = ip.split("\\.");
        if (parts.length != 4) return false;
        for (String part : parts) {
            if (part.isEmpty() || part.length() > 3) return false;
            for (char c : part.toCharArray()) if (!Character.isDigit(c)) return false;
            if (part.length() > 1 && part.charAt(0) == '0') return false;
            int num = Integer.parseInt(part);
            if (num < 0 || num > 255) return false;
        }
        return true;
    }

    // P015: Username Validator
    public static boolean isValidUsername(String username) {
        if (username == null || username.length() < 3 || username.length() > 20) return false;
        if (!Character.isLetter(username.charAt(0))) return false;
        for (char c : username.toCharArray()) {
            if (!Character.isLetterOrDigit(c) && c != '_' && c != '-') return false;
        }
        return true;
    }

    // P016: HTML Text Escaper
    public static String escapeHtml(String s) {
        if (s == null) return "";
        StringBuilder result = new StringBuilder();
        for (char c : s.toCharArray()) {
            if (c == '&') result.append("&amp;");
            else if (c == '<') result.append("&lt;");
            else if (c == '>') result.append("&gt;");
            else if (c == '"') result.append("&quot;");
            else if (c == '\'') result.append("&#39;");
            else result.append(c);
        }
        return result.toString();
    }

    // P017: CSV Cell Escaper
    public static String escapeCsvCell(String s) {
        if (s == null) return "";
        boolean needsQuoting = s.contains(",") || s.contains("\"") || s.contains("\n") || s.contains("\r");
        if (!needsQuoting) return s;
        StringBuilder escaped = new StringBuilder();
        for (char c : s.toCharArray()) {
            if (c == '"') escaped.append("\"\"");
            else escaped.append(c);
        }
        return "\"" + escaped.toString() + "\"";
    }

    // P018: JSON String Escaper
    public static String escapeJsonString(String s) {
        if (s == null) return "";
        StringBuilder result = new StringBuilder();
        for (char c : s.toCharArray()) {
            if (c == '"') result.append("\\\"");
            else if (c == '\\') result.append("\\\\");
            else if (c == '/') result.append("\\/");
            else if (c == '\b') result.append("\\b");
            else if (c == '\f') result.append("\\f");
            else if (c == '\n') result.append("\\n");
            else if (c == '\r') result.append("\\r");
            else if (c == '\t') result.append("\\t");
            else if (c < 0x20) result.append(String.format("\\u%04x", (int) c));
            else result.append(c);
        }
        return result.toString();
    }

    // P019: URL Query Component Encoder
    public static String encodeUrlComponent(String s) {
        if (s == null) return "";
        String unreserved = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~";
        StringBuilder result = new StringBuilder();
        for (char c : s.toCharArray()) {
            if (unreserved.indexOf(c) >= 0) result.append(c);
            else {
                byte[] bytes = String.valueOf(c).getBytes(java.nio.charset.StandardCharsets.UTF_8);
                for (byte b : bytes) result.append(String.format("%%%02X", b & 0xFF));
            }
        }
        return result.toString();
    }

    // P020: Template Placeholder Sanitizer
    public static String sanitizeTemplate(String s) {
        if (s == null) return "";
        StringBuilder result = new StringBuilder();
        int i = 0;
        while (i < s.length()) {
            if (i + 1 < s.length() && s.charAt(i) == '{' && s.charAt(i + 1) == '{') {
                int end = s.indexOf("}}", i + 2);
                if (end != -1) {
                    String key = s.substring(i + 2, end);
                    boolean safe = !key.isEmpty();
                    for (char c : key.toCharArray()) {
                        if (!Character.isLetterOrDigit(c) && c != '_') { safe = false; break; }
                    }
                    if (safe) result.append(s, i, end + 2);
                    i = end + 2;
                    continue;
                }
            }
            result.append(s.charAt(i++));
        }
        return result.toString();
    }

    // P021: Safe Path Normalizer
    public static String safePathNormalize(String path) {
        if (path == null || path.trim().isEmpty()) return "";
        if (path.contains("\\")) return "";
        String[] segments = path.split("/");
        java.util.List<String> result = new java.util.ArrayList<>();
        for (String seg : segments) {
            if (seg.isEmpty() || seg.equals(".")) continue;
            if (seg.equals("..")) {
                if (result.isEmpty()) return "";
                result.remove(result.size() - 1);
            } else {
                result.add(seg);
            }
        }
        return String.join("/", result);
    }

    // P022: Path Extension Validator
    public static boolean isAllowedExtension(String path) {
        if (path == null) return false;
        java.util.Set<String> allowed = new java.util.HashSet<>();
        allowed.add(".jpg"); allowed.add(".jpeg"); allowed.add(".png");
        allowed.add(".gif"); allowed.add(".pdf"); allowed.add(".txt"); allowed.add(".csv");
        String filename = path.replace('\\', '/');
        int lastSlash = filename.lastIndexOf('/');
        if (lastSlash != -1) filename = filename.substring(lastSlash + 1);
        int dot = filename.lastIndexOf('.');
        if (dot <= 0) return false;
        String ext = "." + filename.substring(dot + 1).toLowerCase();
        return allowed.contains(ext);
    }

    // P023: Filename Sanitizer
    public static String sanitizeFilename(String name) {
        if (name == null) return "_";
        if (name.length() > 200) name = name.substring(0, 200);
        StringBuilder sb = new StringBuilder();
        for (char c : name.toCharArray()) {
            if (Character.isLetterOrDigit(c) || c == '.' || c == '_' || c == '-') sb.append(c);
            else sb.append('_');
        }
        String s = sb.toString().replaceAll("_+", "_").replaceAll("^_|_$", "");
        return s.isEmpty() ? "_" : s;
    }

    // P024: Archive Entry Path Checker
    public static String checkArchiveEntry(String path) {
        if (path == null || path.isEmpty()) return "safe";
        if (path.startsWith("/")) return "unsafe";
        if (path.contains("\\")) return "unsafe";
        int depth = 0;
        String[] segments = path.split("/");
        for (String seg : segments) {
            if (seg.isEmpty() || seg.equals(".")) continue;
            if (seg.equals("..")) {
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
        if (ext == null) return false;
        java.util.Set<String> allowed = new java.util.HashSet<>();
        allowed.add("jpg"); allowed.add("jpeg"); allowed.add("png");
        allowed.add("gif"); allowed.add("bmp"); allowed.add("pdf");
        allowed.add("txt"); allowed.add("csv"); allowed.add("json"); allowed.add("xml");
        ext = ext.toLowerCase();
        if (ext.startsWith(".")) ext = ext.substring(1);
        return !ext.isEmpty() && allowed.contains(ext);
    }

    // P026: SQL Identifier Validator
    public static boolean isValidSqlIdentifier(String name) {
        if (name == null || name.isEmpty() || name.length() > 64) return false;
        char first = name.charAt(0);
        if (!Character.isLetter(first) && first != '_') return false;
        for (char c : name.toCharArray()) {
            if (!Character.isLetterOrDigit(c) && c != '_') return false;
        }
        return true;
    }

    // P027: SQL String Literal Escaper
    public static String escapeSqlString(String s) {
        if (s == null) return "";
        return s.replace("\\", "\\\\").replace("'", "''");
    }

    // P028: Parameterized Query Builder
    public static String buildParamQuery(String s) {
        if (s == null) return "INVALID";
        int pipe = s.indexOf('|');
        if (pipe == -1) return "INVALID";
        String table = s.substring(0, pipe);
        String conditions = s.substring(pipe + 1);
        if (!isValidSqlIdentifier(table)) return "INVALID";
        if (conditions.isEmpty()) return "INVALID";
        String[] condPairs = conditions.split(",");
        if (condPairs.length == 0) return "INVALID";
        java.util.List<String> cols = new java.util.ArrayList<>();
        for (String pair : condPairs) {
            int eq = pair.indexOf('=');
            if (eq == -1) return "INVALID";
            String col = pair.substring(0, eq);
            if (!isValidSqlIdentifier(col)) return "INVALID";
            cols.add(col);
        }
        if (cols.isEmpty()) return "INVALID";
        StringBuilder where = new StringBuilder();
        for (int i = 0; i < cols.size(); i++) {
            if (i > 0) where.append(" AND ");
            where.append(cols.get(i)).append("=?");
        }
        return "SELECT * FROM " + table + " WHERE " + where.toString();
    }

    // P029: Sort Direction Validator
    public static String validateSortDirection(String s) {
        if (s == null) return "INVALID";
        String trimmed = s.trim().toUpperCase();
        if (trimmed.equals("ASC") || trimmed.equals("DESC")) return trimmed;
        return "INVALID";
    }

    // P030: Column Allowlist Checker
    public static boolean isAllowedColumn(String col) {
        if (col == null) return false;
        java.util.Set<String> allowed = new java.util.HashSet<>();
        allowed.add("id"); allowed.add("name"); allowed.add("email");
        allowed.add("created_at"); allowed.add("status"); allowed.add("age");
        allowed.add("role"); allowed.add("score");
        return allowed.contains(col.trim());
    }

    // P031: Shell Argument Quoter
    public static String quoteShellArg(String s) {
        if (s == null) s = "";
        StringBuilder escaped = new StringBuilder();
        for (char c : s.toCharArray()) {
            if (c == '\'') escaped.append("'\\''");
            else escaped.append(c);
        }
        return "'" + escaped.toString() + "'";
    }

    // P032: Command Name Allowlist
    public static boolean isAllowedCommand(String s) {
        if (s == null) return false;
        java.util.Set<String> allowed = new java.util.HashSet<>();
        allowed.add("ls"); allowed.add("cat"); allowed.add("echo");
        allowed.add("grep"); allowed.add("find"); allowed.add("sort");
        allowed.add("uniq"); allowed.add("wc"); allowed.add("head"); allowed.add("tail");
        String trimmed = s.trim();
        if (!trimmed.equals(s.replaceAll("\\s+", ""))) return false;
        return allowed.contains(trimmed);
    }

    // P033: Shell Metacharacter Detector
    public static String detectShellMeta(String s) {
        if (s == null) return "safe";
        String dangerous = ";|&$`><(){}\\\"'";
        for (char c : s.toCharArray()) {
            if (dangerous.indexOf(c) >= 0 || c == '\n' || c == '\r') return "unsafe";
        }
        return "safe";
    }

    // P034: Environment Variable Name Validator
    public static boolean isValidEnvVar(String name) {
        if (name == null || name.isEmpty() || name.length() > 64) return false;
        char first = name.charAt(0);
        if (!Character.isUpperCase(first) && first != '_') return false;
        for (char c : name.toCharArray()) {
            if (!Character.isUpperCase(c) && !Character.isDigit(c) && c != '_') return false;
        }
        return true;
    }

    // P035: Command Argument Splitter
    public static java.util.List<String> splitArgs(String s) {
        java.util.List<String> result = new java.util.ArrayList<>();
        if (s == null || s.isEmpty()) return result;
        StringBuilder current = new StringBuilder();
        boolean inQuotes = false;
        for (char c : s.toCharArray()) {
            if (c == '"') {
                if (inQuotes) {
                    result.add(current.toString());
                    current.setLength(0);
                    inQuotes = false;
                } else {
                    if (current.length() > 0) {
                        result.add(current.toString());
                        current.setLength(0);
                    }
                    inQuotes = true;
                }
            } else if (c == ' ' && !inQuotes) {
                if (current.length() > 0) {
                    result.add(current.toString());
                    current.setLength(0);
                }
            } else {
                current.append(c);
            }
        }
        if (current.length() > 0) result.add(current.toString());
        return result;
    }

    // P036: Safe Literal Parser
    public static String parseSafeLiteral(String s) {
        if (s == null) return "INVALID";
        if (s.equals("true") || s.equals("false") || s.equals("null")) return s;
        boolean neg = false;
        int i = 0;
        if (s.startsWith("-")) {
            neg = true;
            i = 1;
        }
        if (i >= s.length()) return "INVALID";
        StringBuilder digits = new StringBuilder();
        for (; i < s.length(); i++) {
            char c = s.charAt(i);
            if (!Character.isDigit(c)) return "INVALID";
            digits.append(c);
        }
        if (digits.length() == 0) return "INVALID";
        if ((digits.length() > 1 && digits.charAt(0) == '0') || (neg && digits.length() > 1 && digits.charAt(0) == '0')) return "INVALID";
        return (neg ? "-" : "") + digits.toString();
    }

    // P037: Configuration Boolean Parser
    public static String parseConfigBool(String s) {
        if (s == null) return "INVALID";
        String trimmed = s.trim().toLowerCase();
        if (trimmed.equals("true") || trimmed.equals("yes") || trimmed.equals("1") || trimmed.equals("on") || trimmed.equals("enabled")) return "true";
        if (trimmed.equals("false") || trimmed.equals("no") || trimmed.equals("0") || trimmed.equals("off") || trimmed.equals("disabled")) return "false";
        return "INVALID";
    }

    // P038: Configuration Key Allowlist
    public static boolean isAllowedConfigKey(String key) {
        if (key == null) return false;
        java.util.Set<String> allowed = new java.util.HashSet<>();
        allowed.add("host"); allowed.add("port"); allowed.add("database");
        allowed.add("username"); allowed.add("password"); allowed.add("timeout");
        allowed.add("max_connections"); allowed.add("ssl_enabled");
        allowed.add("log_level"); allowed.add("retry_count");
        return allowed.contains(key.trim());
    }

    // P039: Structured Token Decoder
    public static String validateToken(String s) {
        if (s == null) return "invalid";
        String[] parts = s.split("\\.", -1);
        if (parts.length != 3) return "invalid";
        String header = parts[0], payload = parts[1], checksum = parts[2];
        String base64url = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
        for (char c : header.toCharArray()) if (base64url.indexOf(c) == -1) return "invalid";
        for (char c : payload.toCharArray()) if (base64url.indexOf(c) == -1) return "invalid";
        String hex = "0123456789abcdef";
        if (checksum.length() != 8) return "invalid";
        for (char c : checksum.toCharArray()) if (hex.indexOf(c) == -1) return "invalid";
        return "valid";
    }

    // P040: Safe Numeric Expression Validator
    public static String validateNumericExpr(String s) {
        if (s == null || s.trim().isEmpty()) return "invalid";
        String trimmed = s.replaceAll("\\s+", "");
        if (trimmed.isEmpty()) return "invalid";
        String ops = "+-*/";
        int i = 0;
        java.util.function.BooleanSupplier parseNum = () -> {
            if (i >= trimmed.length()) return false;
            if (trimmed.charAt(i) == '-') i++;
            if (i >= trimmed.length() || !Character.isDigit(trimmed.charAt(i))) return false;
            if (trimmed.charAt(i) == '0') {
                i++;
                if (i < trimmed.length() && Character.isDigit(trimmed.charAt(i))) return false;
            } else {
                while (i < trimmed.length() && Character.isDigit(trimmed.charAt(i))) i++;
            }
            return true;
        };
        if (!parseNum.getAsBoolean()) return "invalid";
        while (i < trimmed.length()) {
            if (ops.indexOf(trimmed.charAt(i)) == -1) return "invalid";
            i++;
            if (!parseNum.getAsBoolean()) return "invalid";
        }
        return "valid";
    }

    // P041: Frequency Counter Large Input
    public static java.util.Map<Integer, Integer> frequencyCounter(int[] nums) {
        java.util.Map<Integer, Integer> freq = new java.util.TreeMap<>();
        if (nums == null) return freq;
        for (int n : nums) freq.put(n, freq.getOrDefault(n, 0) + 1);
        return freq;
    }

    // P042: Duplicate Detector
    public static boolean hasDuplicate(int[] nums) {
        if (nums == null || nums.length == 0) return false;
        java.util.Set<Integer> seen = new java.util.HashSet<>();
        for (int n : nums) {
            if (!seen.add(n)) return true;
        }
        return false;
    }

    // P043: Streaming Sum
    public static long streamingSum(int[] nums) {
        if (nums == null) return 0;
        long sum = 0;
        for (int n : nums) sum += n;
        return sum;
    }

    // P044: Bounded Log Processor
    public static java.util.Map<String, Integer> boundedLogProcessor(String log, int maxLines) {
        java.util.Map<String, Integer> result = new java.util.HashMap<>();
        result.put("kept", 0);
        result.put("total_words", 0);
        if (log == null || maxLines <= 0) return result;
        String[] lines = log.split("\n");
        int kept = 0;
        for (String line : lines) {
            if (kept >= maxLines) break;
            String trimmed = line.trim();
            if (trimmed.isEmpty()) continue;
            kept++;
            String[] words = trimmed.split("\\s+");
            result.put("total_words", result.get("total_words") + words.length);
        }
        result.put("kept", kept);
        return result;
    }

    // P045: Top-K Frequent Values
    public static int[] topKFrequent(int[] nums, int k) {
        if (nums == null || nums.length == 0 || k <= 0) return new int[]{};
        java.util.Map<Integer, Integer> freq = new java.util.HashMap<>();
        for (int n : nums) freq.put(n, freq.getOrDefault(n, 0) + 1);
        java.util.List<java.util.Map.Entry<Integer, Integer>> items = new java.util.ArrayList<>(freq.entrySet());
        items.sort((a, b) -> {
            int cmp = b.getValue().compareTo(a.getValue());
            if (cmp != 0) return cmp;
            return a.getKey().compareTo(b.getKey());
        });
        java.util.List<Integer> result = new java.util.ArrayList<>();
        for (int i = 0; i < Math.min(k, items.size()); i++) result.add(items.get(i).getKey());
        java.util.Collections.sort(result);
        return result.stream().mapToInt(Integer::intValue).toArray();
    }

    // P046: Token Format Validator
    public static String validateTokenFormat(String token) {
        if (token == null || token.isEmpty() || token.length() < 8 || token.length() > 32) return "invalid";
        if (!Character.isLetter(token.charAt(0))) return "invalid";
        for (char c : token.toCharArray()) {
            if (!Character.isLetterOrDigit(c) && c != '-') return "invalid";
        }
        return "valid";
    }

    // P047: Permission Rule Evaluator
    public static String evaluatePermission(String role, String action) {
        if (role == null || action == null) return "denied";
        java.util.Map<String, java.util.Set<String>> perms = new java.util.HashMap<>();
        perms.put("admin", new java.util.HashSet<>(java.util.Arrays.asList("read", "write", "delete", "execute")));
        perms.put("editor", new java.util.HashSet<>(java.util.Arrays.asList("read", "write")));
        perms.put("viewer", new java.util.HashSet<>(java.util.Arrays.asList("read")));
        perms.put("guest", new java.util.HashSet<>());
        if (perms.containsKey(role) && perms.get(role).contains(action)) return "allowed";
        return "denied";
    }

    // P048: Role Permission Checker
    public static boolean roleHasPermission(String role, String permission) {
        if (role == null || permission == null) return false;
        java.util.Map<String, java.util.Set<String>> perms = new java.util.HashMap<>();
        perms.put("admin", new java.util.HashSet<>(java.util.Arrays.asList("read", "write", "delete", "execute")));
        perms.put("editor", new java.util.HashSet<>(java.util.Arrays.asList("read", "write")));
        perms.put("viewer", new java.util.HashSet<>(java.util.Arrays.asList("read")));
        perms.put("guest", new java.util.HashSet<>());
        return perms.containsKey(role) && perms.get(role).contains(permission);
    }

    // P049: Session Timeout Checker
    public static String checkSession(int lastActive, int currentTime, int timeout) {
        if (currentTime < lastActive) return "invalid";
        int elapsed = currentTime - lastActive;
        return (elapsed <= timeout) ? "active" : "expired";
    }

    // P050: Access Scope Validator
    public static String validateScope(String requested, java.util.List<String> allowed) {
        if (requested == null || allowed == null || allowed.isEmpty()) return "denied";
        java.util.Set<String> allowedSet = new java.util.HashSet<>(allowed);
        if (allowedSet.contains(requested)) return "granted";
        int pos = 0;
        while ((pos = requested.indexOf(':', pos)) != -1) {
            String parent = requested.substring(0, pos);
            if (allowedSet.contains(parent)) return "granted";
            // Reconstructed from the P050 benchmark contract; not present in the truncated source.
            pos++;
        }
        return "denied";
    }
}
