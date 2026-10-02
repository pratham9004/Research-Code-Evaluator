import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Solution {
    // P001
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

    // P002
    public static int maxSubarray(int[] nums) {
        int current = nums[0];
        int best = nums[0];
        for (int i = 1; i < nums.length; i++) {
            current = Math.max(nums[i], current + nums[i]);
            best = Math.max(best, current);
        }
        return best;
    }

    // P003
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

    // P004
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

    // P005
    public static boolean isBalanced(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        for (char ch : s.toCharArray()) {
            if (ch == '(' || ch == '[' || ch == '{') {
                stack.push(ch);
            } else {
                if (stack.isEmpty()) return false;
                char open = stack.pop();
                if ((ch == ')' && open != '(') ||
                    (ch == ']' && open != '[') ||
                    (ch == '}' && open != '{')) return false;
            }
        }
        return stack.isEmpty();
    }

    // P006
    public static int csvFieldCount(String line) {
        if (line.isEmpty()) return 1;
        int count = 1;
        boolean inQuotes = false;
        for (int i = 0; i < line.length(); i++) {
            char ch = line.charAt(i);
            if (ch == '"') {
                if (inQuotes && i + 1 < line.length() && line.charAt(i + 1) == '"') {
                    i++;
                } else {
                    inQuotes = !inQuotes;
                }
            } else if (ch == ',' && !inQuotes) {
                count++;
            }
        }
        return count;
    }

    // P007
    public static Map<String, Integer> countLogLevels(String log) {
        Map<String, Integer> counts = new LinkedHashMap<>();
        counts.put("ERROR", 0);
        counts.put("WARNING", 0);
        counts.put("INFO", 0);
        counts.put("DEBUG", 0);
        String[] lines = log.split("\\R", -1);
        for (String line : lines) {
            for (String level : counts.keySet()) {
                if (line.startsWith(level) && line.length() > level.length()) {
                    char next = line.charAt(level.length());
                    if (next == ' ' || next == ':') {
                        counts.put(level, counts.get(level) + 1);
                        break;
                    }
                }
            }
        }
        return counts;
    }

    // P008
    public static Map<String, String> parseKeyValue(String s) {
        Map<String, String> result = new TreeMap<>();
        if (s.isEmpty()) return result;
        for (String pair : s.split(",", -1)) {
            String[] parts = pair.split("=", 2);
            result.put(parts[0].trim(), parts[1].trim());
        }
        return result;
    }

    // P009
    public static String normalizeDate(String date) {
        String[] parts;
        int year, month, day;
        if (date.contains("/")) {
            parts = date.split("/");
            month = Integer.parseInt(parts[0]);
            day = Integer.parseInt(parts[1]);
            year = Integer.parseInt(parts[2]);
        } else if (date.contains("-")) {
            parts = date.split("-");
            day = Integer.parseInt(parts[0]);
            month = Integer.parseInt(parts[1]);
            year = Integer.parseInt(parts[2]);
        } else {
            parts = date.split("\\.");
            year = Integer.parseInt(parts[0]);
            month = Integer.parseInt(parts[1]);
            day = Integer.parseInt(parts[2]);
        }
        return String.format("%04d-%02d-%02d", year, month, day);
    }

    // P010
    public static Map<String, Integer> wordFrequency(String text) {
        Map<String, Integer> counts = new HashMap<>();
        Matcher matcher = Pattern.compile("[A-Za-z]+").matcher(text);
        while (matcher.find()) {
            String word = matcher.group().toLowerCase(Locale.ROOT);
            counts.put(word, counts.getOrDefault(word, 0) + 1);
        }
        return counts;
    }

    // P011
    public static boolean isValidEmail(String email) {
        if (email.chars().filter(c -> c == '@').count() != 1) return false;
        int at = email.indexOf('@');
        String local = email.substring(0, at);
        String domain = email.substring(at + 1);
        if (local.isEmpty() || domain.isEmpty()) return false;
        if (local.startsWith(".") || local.endsWith(".") || local.contains("..")) return false;
        if (!local.matches("[a-zA-Z0-9._%+\\-]+")) return false;
        String[] labels = domain.split("\\.", -1);
        for (String label : labels) {
            if (label.isEmpty() || label.startsWith("-") || label.endsWith("-")) return false;
            if (!label.matches("[A-Za-z0-9\\-]+")) return false;
        }
        String tld = labels[labels.length - 1];
        return tld.length() >= 2 && tld.length() <= 6 && tld.matches("[A-Za-z]+");
    }

    // P012
    public static boolean isValidPassword(String password) {
        if (password.length() < 8) return false;
        boolean upper = false, lower = false, digit = false, special = false;
        for (char ch : password.toCharArray()) {
            if (ch >= 'A' && ch <= 'Z') upper = true;
            else if (ch >= 'a' && ch <= 'z') lower = true;
            else if (ch >= '0' && ch <= '9') digit = true;
            else if ("!@#$%^&*".indexOf(ch) >= 0) special = true;
        }
        return upper && lower && digit && special;
    }

    // P013
    public static String isValidRange(String s) {
        String[] parts = s.split("\\|", -1);
        if (parts.length != 3) return "INVALID";
        try {
            long value = Long.parseLong(parts[0]);
            long min = Long.parseLong(parts[1]);
            long max = Long.parseLong(parts[2]);
            return min <= value && value <= max ? "VALID" : "INVALID";
        } catch (NumberFormatException e) {
            return "INVALID";
        }
    }

    // P014
    public static boolean isValidIPv4(String ip) {
        String[] parts = ip.split("\\.", -1);
        if (parts.length != 4) return false;
        for (String part : parts) {
            if (part.isEmpty() || !part.matches("\\d+")) return false;
            if (part.length() > 1 && part.charAt(0) == '0') return false;
            try {
                if (Integer.parseInt(part) > 255) return false;
            } catch (NumberFormatException e) {
                return false;
            }
        }
        return true;
    }

    // P015
    public static boolean isValidUsername(String username) {
        return username.length() >= 3 && username.length() <= 20
            && username.matches("[a-zA-Z][a-zA-Z0-9_-]*");
    }

    // P016
    public static String escapeHtml(String s) {
        return s.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\"", "&quot;")
                .replace("'", "&#39;");
    }

    // P017
    public static String escapeCsvCell(String s) {
        if (s.indexOf(',') >= 0 || s.indexOf('"') >= 0 || s.indexOf('\n') >= 0 || s.indexOf('\r') >= 0) {
            return "\"" + s.replace("\"", "\"\"") + "\"";
        }
        return s;
    }

    // P018
    public static String escapeJsonString(String s) {
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            switch (ch) {
                case '"': result.append("\\\""); break;
                case '\\': result.append("\\\\"); break;
                case '/': result.append("\\/"); break;
                case '\b': result.append("\\b"); break;
                case '\f': result.append("\\f"); break;
                case '\n': result.append("\\n"); break;
                case '\r': result.append("\\r"); break;
                case '\t': result.append("\\t"); break;
                default:
                    if (ch < 0x20) result.append(String.format("\\u%04x", (int) ch));
                    else result.append(ch);
            }
        }
        return result.toString();
    }

    // P019
    public static String encodeUrlComponent(String s) {
        byte[] bytes = s.getBytes(StandardCharsets.UTF_8);
        String hex = "0123456789ABCDEF";
        StringBuilder result = new StringBuilder();
        for (byte b : bytes) {
            int value = b & 0xFF;
            char ch = (char) value;
            if ((ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z') ||
                (ch >= '0' && ch <= '9') || ch == '-' || ch == '_' || ch == '.' || ch == '~') {
                result.append(ch);
            } else {
                result.append('%').append(hex.charAt(value >>> 4)).append(hex.charAt(value & 15));
            }
        }
        return result.toString();
    }

    // P020
    public static String sanitizeTemplate(String s) {
        Pattern pattern = Pattern.compile("\\{\\{([^{}]*)\\}\\}");
        Matcher matcher = pattern.matcher(s);
        StringBuffer result = new StringBuffer();
        while (matcher.find()) {
            String key = matcher.group(1);
            if (key.matches("[a-zA-Z0-9_]+")) matcher.appendReplacement(result, Matcher.quoteReplacement(matcher.group(0)));
            else matcher.appendReplacement(result, "");
        }
        matcher.appendTail(result);
        return result.toString();
    }

    // P021
    public static String safePathNormalize(String path) {
        if (path.isEmpty() || path.trim().isEmpty() || path.indexOf('\\') >= 0) return "";
        Deque<String> parts = new ArrayDeque<>();
        for (String segment : path.split("/", -1)) {
            if (segment.isEmpty() || segment.equals(".")) continue;
            if (segment.equals("..")) {
                if (parts.isEmpty()) return "";
                parts.removeLast();
            } else {
                parts.addLast(segment);
            }
        }
        return String.join("/", parts);
    }

    // P022
    public static boolean isAllowedExtension(String path) {
        int slash = Math.max(path.lastIndexOf('/'), path.lastIndexOf('\\'));
        String filename = path.substring(slash + 1);
        int dot = filename.lastIndexOf('.');
        if (dot <= 0) return false;
        String ext = filename.substring(dot).toLowerCase(Locale.ROOT);
        return Set.of(".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".csv").contains(ext);
    }

    // P023
    public static String sanitizeFilename(String name) {
        String value = name.substring(0, Math.min(200, name.length()));
        value = value.replaceAll("[^a-zA-Z0-9._-]", "_");
        value = value.replaceAll("_+", "_");
        value = value.replaceAll("^_+|_+$", "");
        return value.isEmpty() ? "_" : value;
    }

    // P024
    public static String checkArchiveEntry(String path) {
        if (path.isEmpty()) return "safe";
        if (path.startsWith("/") || path.indexOf('\\') >= 0) return "unsafe";
        int depth = 0;
        for (String segment : path.split("/", -1)) {
            if (segment.isEmpty() || segment.equals(".")) continue;
            if (segment.equals("..")) {
                depth--;
                if (depth < 0) return "unsafe";
            } else {
                depth++;
            }
        }
        return "safe";
    }

    // P025
    public static boolean isAllowedFiletype(String ext) {
        String value = ext.startsWith(".") ? ext.substring(1) : ext;
        if (value.isEmpty()) return false;
        return Set.of("jpg", "jpeg", "png", "gif", "bmp", "pdf", "txt", "csv", "json", "xml")
                .contains(value.toLowerCase(Locale.ROOT));
    }

    // P026
    public static boolean isValidSqlIdentifier(String name) {
        return name.matches("[a-zA-Z_][a-zA-Z0-9_]{0,63}");
    }

    // P027
    public static String escapeSqlString(String s) {
        return s.replace("\\", "\\\\").replace("'", "''");
    }

    // P028
    public static String buildParamQuery(String s) {
        if (s.chars().filter(c -> c == '|').count() != 1) return "INVALID";
        String[] outer = s.split("\\|", -1);
        String table = outer[0];
        String conditions = outer[1];
        if (!table.matches("[a-zA-Z_][a-zA-Z0-9_]*") || conditions.isEmpty()) return "INVALID";
        String[] parts = conditions.split(",", -1);
        List<String> columns = new ArrayList<>();
        for (String part : parts) {
            int eq = part.indexOf('=');
            if (eq < 0) return "INVALID";
            String column = part.substring(0, eq);
            if (!column.matches("[a-zA-Z_][a-zA-Z0-9_]*")) return "INVALID";
            columns.add(column);
        }
        if (columns.isEmpty()) return "INVALID";
        return "SELECT * FROM " + table + " WHERE " +
                String.join(" AND ", columns.stream().map(c -> c + "=?").toList());
    }

    // P029
    public static String validateSortDirection(String s) {
        String value = s.trim().toUpperCase(Locale.ROOT);
        return value.equals("ASC") || value.equals("DESC") ? value : "INVALID";
    }

    // P030
    public static boolean isAllowedColumn(String col) {
        return Set.of("id", "name", "email", "created_at", "status", "age", "role", "score").contains(col.trim());
    }

    // P031
    public static String quoteShellArg(String s) {
        return "'" + s.replace("'", "'\\''") + "'";
    }

    // P032
    public static boolean isAllowedCommand(String s) {
        return Set.of("ls", "cat", "echo", "grep", "find", "sort", "uniq", "wc", "head", "tail").contains(s.trim());
    }

    // P033
    public static String detectShellMeta(String s) {
        String dangerous = ";|&$`><(){}\\\"'\n\r";
        for (int i = 0; i < s.length(); i++) {
            if (dangerous.indexOf(s.charAt(i)) >= 0) return "unsafe";
        }
        return "safe";
    }

    // P034
    public static boolean isValidEnvVar(String name) {
        return name.length() >= 1 && name.length() <= 64 && name.matches("[A-Z_][A-Z0-9_]*");
    }

    // P035
    public static List<String> splitArgs(String s) {
        if (s.isEmpty()) return new ArrayList<>();
        List<String> tokens = new ArrayList<>();
        StringBuilder current = new StringBuilder();
        boolean inQuotes = false;
        boolean tokenStarted = false;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '"') {
                inQuotes = !inQuotes;
                tokenStarted = true;
            } else if (ch == ' ' && !inQuotes) {
                if (tokenStarted) {
                    tokens.add(current.toString());
                    current.setLength(0);
                    tokenStarted = false;
                }
            } else {
                current.append(ch);
                tokenStarted = true;
            }
        }
        if (tokenStarted) tokens.add(current.toString());
        return tokens;
    }

    // P036
    public static String parseSafeLiteral(String s) {
        if (s.matches("-?(0|[1-9][0-9]*)")) return s;
        if (s.equals("true") || s.equals("false") || s.equals("null")) return s;
        if (s.length() >= 2 && s.charAt(0) == '"' && s.charAt(s.length() - 1) == '"') {
            String content = s.substring(1, s.length() - 1);
            StringBuilder result = new StringBuilder();
            for (int i = 0; i < content.length(); i++) {
                char ch = content.charAt(i);
                if (ch == '\\') {
                    if (i + 1 >= content.length() || content.charAt(i + 1) != '"') return "INVALID";
                    result.append('"');
                    i++;
                } else if (ch == '"') {
                    return "INVALID";
                } else {
                    result.append(ch);
                }
            }
            return result.toString();
        }
        return "INVALID";
    }

    // P037
    public static String parseConfigBool(String s) {
        String value = s.trim().toLowerCase(Locale.ROOT);
        if (Set.of("true", "yes", "1", "on", "enabled").contains(value)) return "true";
        if (Set.of("false", "no", "0", "off", "disabled").contains(value)) return "false";
        return "INVALID";
    }

    // P038
    public static boolean isAllowedConfigKey(String key) {
        return Set.of("host", "port", "database", "username", "password", "timeout",
                "max_connections", "ssl_enabled", "log_level", "retry_count").contains(key.trim());
    }

    // P039
    public static String validateToken(String s) {
        return s.matches("[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+\\.[0-9a-f]{8}") ? "valid" : "invalid";
    }

    // P040
    public static String validateNumericExpr(String s) {
        String number = "-?(?:0|[1-9][0-9]*)";
        return s.matches(number + "(?:\\s*[+\\-*/]\\s*" + number + ")*") ? "valid" : "invalid";
    }

    // P041
    public static Map<Integer, Integer> frequencyCounter(int[] nums) {
        Map<Integer, Integer> counts = new TreeMap<>();
        for (int value : nums) counts.put(value, counts.getOrDefault(value, 0) + 1);
        return counts;
    }

    // P042
    public static boolean hasDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int value : nums) if (!seen.add(value)) return true;
        return false;
    }

    // P043
    public static long streamingSum(int[] nums) {
        long sum = 0;
        for (int value : nums) sum += value;
        return sum;
    }

    // P044
    public static Map<String, Integer> boundedLogProcessor(String log, int maxLines) {
        Map<String, Integer> result = new LinkedHashMap<>();
        int kept = 0;
        int totalWords = 0;
        if (maxLines > 0 && !log.isEmpty()) {
            for (String line : log.split("\\R", -1)) {
                if (line.trim().isEmpty()) continue;
                if (kept >= maxLines) break;
                kept++;
                totalWords += line.trim().isEmpty() ? 0 : line.trim().split("\\s+").length;
            }
        }
        result.put("kept", kept);
        result.put("total_words", totalWords);
        return result;
    }

    // P045
    public static int[] topKFrequent(int[] nums, int k) {
        if (nums.length == 0 || k == 0) return new int[0];
        Map<Integer, Integer> counts = new HashMap<>();
        for (int value : nums) counts.put(value, counts.getOrDefault(value, 0) + 1);
        List<Integer> values = new ArrayList<>(counts.keySet());
        values.sort((a, b) -> {
            int byFreq = Integer.compare(counts.get(b), counts.get(a));
            return byFreq != 0 ? byFreq : Integer.compare(a, b);
        });
        int limit = Math.min(k, values.size());
        int[] result = new int[limit];
        for (int i = 0; i < limit; i++) result[i] = values.get(i);
        Arrays.sort(result);
        return result;
    }

    // P046
    public static String validateTokenFormat(String token) {
        return token.matches("[a-zA-Z][a-zA-Z0-9-]{7,31}") ? "valid" : "invalid";
    }

    // P047
    public static String evaluatePermission(String role, String action) {
        Set<String> permissions;
        switch (role) {
            case "admin": permissions = Set.of("read", "write", "delete", "execute"); break;
            case "editor": permissions = Set.of("read", "write"); break;
            case "viewer": permissions = Set.of("read"); break;
            case "guest": permissions = Collections.emptySet(); break;
            default: return "denied";
        }
        return permissions.contains(action) ? "allowed" : "denied";
    }

    // P048
    public static boolean roleHasPermission(String role, String permission) {
        Set<String> permissions;
        switch (role) {
            case "admin": permissions = Set.of("read", "write", "delete", "execute"); break;
            case "editor": permissions = Set.of("read", "write"); break;
            case "viewer": permissions = Set.of("read"); break;
            case "guest": permissions = Collections.emptySet(); break;
            default: return false;
        }
        return permissions.contains(permission);
    }

    // P049
    public static String checkSession(int lastActive, int currentTime, int timeout) {
        if (currentTime < lastActive) return "invalid";
        return currentTime - lastActive > timeout ? "expired" : "active";
    }

    // P050
    public static String validateScope(String requested, List<String> allowed) {
        String[] parts = requested.split(":", -1);
        for (int i = parts.length; i >= 1; i--) {
            String prefix = String.join(":", Arrays.copyOfRange(parts, 0, i));
            if (allowed.contains(prefix)) return "granted";
        }
        return "denied";
    }
}
