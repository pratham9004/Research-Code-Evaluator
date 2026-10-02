import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

public class Solution {

    // P001
    public static int[] twoSum(int[] nums, int target) {
        Map<Long, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            long complement = (long) target - nums[i];
            Integer index = seen.get(complement);
            if (index != null) {
                return new int[] {index, i};
            }
            seen.putIfAbsent((long) nums[i], i);
        }
        return new int[0];
    }

    // P002
    public static int maxSubarray(int[] nums) {
        if (nums.length == 0) {
            return 0;
        }
        long best = nums[0];
        long current = nums[0];
        for (int i = 1; i < nums.length; i++) {
            current = Math.max(nums[i], current + nums[i]);
            best = Math.max(best, current);
        }
        return (int) best;
    }

    // P003
    public static int binarySearch(int[] nums, int target) {
        int low = 0;
        int high = nums.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] == target) {
                return mid;
            }
            if (nums[mid] < target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return -1;
    }

    // P004
    public static int[] mergeSortedArrays(int[] nums1, int[] nums2) {
        int[] merged = new int[nums1.length + nums2.length];
        int i = 0;
        int j = 0;
        int k = 0;
        while (i < nums1.length && j < nums2.length) {
            if (nums1[i] <= nums2[j]) {
                merged[k++] = nums1[i++];
            } else {
                merged[k++] = nums2[j++];
            }
        }
        while (i < nums1.length) {
            merged[k++] = nums1[i++];
        }
        while (j < nums2.length) {
            merged[k++] = nums2[j++];
        }
        return merged;
    }

    // P005
    public static boolean isBalanced(String s) {
        char[] stack = new char[s.length()];
        int top = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(' || ch == '[' || ch == '{') {
                stack[top++] = ch;
            } else if (ch == ')' || ch == ']' || ch == '}') {
                char expected = ch == ')' ? '(' : (ch == ']' ? '[' : '{');
                if (top == 0 || stack[top - 1] != expected) {
                    return false;
                }
                top--;
            } else {
                return false;
            }
        }
        return top == 0;
    }

    // P006
    public static int csvFieldCount(String line) {
        int count = 1;
        boolean inQuotes = false;
        for (int i = 0; i < line.length(); i++) {
            char ch = line.charAt(i);
            if (ch == '"') {
                inQuotes = !inQuotes;
            } else if (ch == ',' && !inQuotes) {
                count++;
            }
        }
        return count;
    }

    // P007
    public static Map<String, Integer> countLogLevels(String log) {
        String[] levels = {"ERROR", "WARNING", "INFO", "DEBUG"};
        Map<String, Integer> counts = new LinkedHashMap<>();
        for (String level : levels) {
            counts.put(level, 0);
        }
        for (String line : log.split("\r\n|\r|\n", -1)) {
            for (String level : levels) {
                if (line.startsWith(level)
                        && (line.length() == level.length()
                                || line.charAt(level.length()) == ' '
                                || line.charAt(level.length()) == ':')) {
                    counts.put(level, counts.get(level) + 1);
                    break;
                }
            }
        }
        return counts;
    }

    // P008
    public static Map<String, String> parseKeyValue(String s) {
        Map<String, String> result = new TreeMap<>();
        for (String pair : s.split(",", -1)) {
            int eq = pair.indexOf('=');
            if (eq < 0) {
                continue;
            }
            result.put(pair.substring(0, eq).trim(), pair.substring(eq + 1).trim());
        }
        return result;
    }

    // P009
    public static String normalizeDate(String date) {
        String year;
        String month;
        String day;
        String[] parts;
        if (date.indexOf('/') >= 0) {
            parts = date.split("/", -1);
            if (parts.length != 3) {
                return date;
            }
            month = parts[0];
            day = parts[1];
            year = parts[2];
        } else if (date.indexOf('-') >= 0) {
            parts = date.split("-", -1);
            if (parts.length != 3) {
                return date;
            }
            day = parts[0];
            month = parts[1];
            year = parts[2];
        } else {
            parts = date.split("\\.", -1);
            if (parts.length != 3) {
                return date;
            }
            year = parts[0];
            month = parts[1];
            day = parts[2];
        }
        StringBuilder result = new StringBuilder();
        for (int i = year.length(); i < 4; i++) {
            result.append('0');
        }
        result.append(year).append('-');
        for (int i = month.length(); i < 2; i++) {
            result.append('0');
        }
        result.append(month).append('-');
        for (int i = day.length(); i < 2; i++) {
            result.append('0');
        }
        result.append(day);
        return result.toString();
    }

    // P010
    public static Map<String, Integer> wordFrequency(String text) {
        Map<String, Integer> counts = new HashMap<>();
        StringBuilder word = new StringBuilder();
        for (int i = 0; i <= text.length(); i++) {
            char ch = i < text.length() ? text.charAt(i) : ' ';
            if (ch >= 'A' && ch <= 'Z') {
                word.append((char) (ch - 'A' + 'a'));
            } else if (ch >= 'a' && ch <= 'z') {
                word.append(ch);
            } else if (word.length() > 0) {
                counts.merge(word.toString(), 1, Integer::sum);
                word.setLength(0);
            }
        }
        List<Map.Entry<String, Integer>> entries = new ArrayList<>(counts.entrySet());
        entries.sort((a, b) -> {
            int byCount = Integer.compare(b.getValue(), a.getValue());
            return byCount != 0 ? byCount : a.getKey().compareTo(b.getKey());
        });
        Map<String, Integer> ordered = new LinkedHashMap<>();
        for (Map.Entry<String, Integer> entry : entries) {
            ordered.put(entry.getKey(), entry.getValue());
        }
        return ordered;
    }

    // P011
    public static boolean isValidEmail(String email) {
        int at = email.indexOf('@');
        if (at < 0 || email.indexOf('@', at + 1) >= 0) {
            return false;
        }
        String local = email.substring(0, at);
        String domain = email.substring(at + 1);
        if (local.isEmpty()) {
            return false;
        }
        for (int i = 0; i < local.length(); i++) {
            char c = local.charAt(i);
            boolean allowed = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')
                    || (c >= '0' && c <= '9') || "._%+-".indexOf(c) >= 0;
            if (!allowed) {
                return false;
            }
        }
        if (local.charAt(0) == '.' || local.charAt(local.length() - 1) == '.' || local.contains("..")) {
            return false;
        }
        String[] labels = domain.split("\\.", -1);
        if (labels.length < 2) {
            return false;
        }
        for (String label : labels) {
            if (label.isEmpty() || label.charAt(0) == '-' || label.charAt(label.length() - 1) == '-') {
                return false;
            }
            for (int i = 0; i < label.length(); i++) {
                char c = label.charAt(i);
                boolean allowed = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')
                        || (c >= '0' && c <= '9') || c == '-';
                if (!allowed) {
                    return false;
                }
            }
        }
        String tld = labels[labels.length - 1];
        if (tld.length() < 2 || tld.length() > 6) {
            return false;
        }
        for (int i = 0; i < tld.length(); i++) {
            char c = tld.charAt(i);
            if (!((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'))) {
                return false;
            }
        }
        return true;
    }

    // P012
    public static boolean isValidPassword(String password) {
        if (password.length() < 8) {
            return false;
        }
        boolean hasUpper = false;
        boolean hasLower = false;
        boolean hasDigit = false;
        boolean hasSpecial = false;
        for (int i = 0; i < password.length(); i++) {
            char c = password.charAt(i);
            if (c >= 'A' && c <= 'Z') {
                hasUpper = true;
            } else if (c >= 'a' && c <= 'z') {
                hasLower = true;
            } else if (c >= '0' && c <= '9') {
                hasDigit = true;
            } else if ("!@#$%^&*".indexOf(c) >= 0) {
                hasSpecial = true;
            }
        }
        return hasUpper && hasLower && hasDigit && hasSpecial;
    }

    // P013
    public static String isValidRange(String s) {
        String[] parts = s.split("\\|", -1);
        if (parts.length != 3) {
            return "INVALID";
        }
        for (String part : parts) {
            int i = (!part.isEmpty() && (part.charAt(0) == '-' || part.charAt(0) == '+')) ? 1 : 0;
            if (i >= part.length()) {
                return "INVALID";
            }
            for (; i < part.length(); i++) {
                char c = part.charAt(i);
                if (c < '0' || c > '9') {
                    return "INVALID";
                }
            }
        }
        BigInteger value = new BigInteger(parts[0]);
        BigInteger min = new BigInteger(parts[1]);
        BigInteger max = new BigInteger(parts[2]);
        return value.compareTo(min) >= 0 && value.compareTo(max) <= 0 ? "VALID" : "INVALID";
    }

    // P014
    public static boolean isValidIPv4(String ip) {
        String[] octets = ip.split("\\.", -1);
        if (octets.length != 4) {
            return false;
        }
        for (String octet : octets) {
            if (octet.isEmpty() || octet.length() > 3) {
                return false;
            }
            int value = 0;
            for (int i = 0; i < octet.length(); i++) {
                char c = octet.charAt(i);
                if (c < '0' || c > '9') {
                    return false;
                }
                value = value * 10 + (c - '0');
            }
            if (octet.length() > 1 && octet.charAt(0) == '0') {
                return false;
            }
            if (value > 255) {
                return false;
            }
        }
        return true;
    }

    // P015
    public static boolean isValidUsername(String username) {
        if (username.length() < 3 || username.length() > 20) {
            return false;
        }
        char first = username.charAt(0);
        if (!((first >= 'a' && first <= 'z') || (first >= 'A' && first <= 'Z'))) {
            return false;
        }
        for (int i = 0; i < username.length(); i++) {
            char c = username.charAt(i);
            boolean allowed = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')
                    || (c >= '0' && c <= '9') || c == '_' || c == '-';
            if (!allowed) {
                return false;
            }
        }
        return true;
    }

    // P016
    public static String escapeHtml(String s) {
        StringBuilder result = new StringBuilder(s.length());
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            switch (ch) {
                case '&':
                    result.append("&amp;");
                    break;
                case '<':
                    result.append("&lt;");
                    break;
                case '>':
                    result.append("&gt;");
                    break;
                case '"':
                    result.append("&quot;");
                    break;
                case '\'':
                    result.append("&#39;");
                    break;
                default:
                    result.append(ch);
            }
        }
        return result.toString();
    }

    // P017
    public static String escapeCsvCell(String s) {
        boolean needsQuoting = s.indexOf(',') >= 0 || s.indexOf('"') >= 0
                || s.indexOf('\n') >= 0 || s.indexOf('\r') >= 0;
        if (!needsQuoting) {
            return s;
        }
        return "\"" + s.replace("\"", "\"\"") + "\"";
    }

    // P018
    public static String escapeJsonString(String s) {
        StringBuilder result = new StringBuilder(s.length());
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            switch (ch) {
                case '"':
                    result.append("\\\"");
                    break;
                case '\\':
                    result.append("\\\\");
                    break;
                case '/':
                    result.append("\\/");
                    break;
                case '\b':
                    result.append("\\b");
                    break;
                case '\f':
                    result.append("\\f");
                    break;
                case '\n':
                    result.append("\\n");
                    break;
                case '\r':
                    result.append("\\r");
                    break;
                case '\t':
                    result.append("\\t");
                    break;
                default:
                    if (ch < 0x20) {
                        result.append(String.format("\\u%04x", (int) ch));
                    } else {
                        result.append(ch);
                    }
            }
        }
        return result.toString();
    }

    // P019
    public static String encodeUrlComponent(String s) {
        final String hex = "0123456789ABCDEF";
        byte[] bytes = s.getBytes(StandardCharsets.UTF_8);
        StringBuilder result = new StringBuilder(bytes.length * 3);
        for (byte b : bytes) {
            int value = b & 0xFF;
            boolean unreserved = (value >= 'A' && value <= 'Z') || (value >= 'a' && value <= 'z')
                    || (value >= '0' && value <= '9') || value == '-' || value == '_'
                    || value == '.' || value == '~';
            if (unreserved) {
                result.append((char) value);
            } else {
                result.append('%').append(hex.charAt(value >> 4)).append(hex.charAt(value & 0x0F));
            }
        }
        return result.toString();
    }

    // P020
    public static String sanitizeTemplate(String s) {
        StringBuilder result = new StringBuilder();
        int pos = 0;
        while (pos < s.length()) {
            int open = s.indexOf("{{", pos);
            if (open < 0) {
                result.append(s, pos, s.length());
                break;
            }
            int close = s.indexOf("}}", open + 2);
            if (close < 0) {
                result.append(s, pos, s.length());
                break;
            }
            result.append(s, pos, open);
            String key = s.substring(open + 2, close);
            boolean safe = !key.isEmpty();
            for (int i = 0; i < key.length() && safe; i++) {
                char c = key.charAt(i);
                boolean allowed = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')
                        || (c >= '0' && c <= '9') || c == '_';
                if (!allowed) {
                    safe = false;
                }
            }
            if (safe) {
                result.append(s, open, close + 2);
            }
            pos = close + 2;
        }
        return result.toString();
    }

    // P021
    public static String safePathNormalize(String path) {
        if (path.trim().isEmpty() || path.indexOf('\\') >= 0) {
            return "";
        }
        List<String> resolved = new ArrayList<>();
        for (String segment : path.split("/", -1)) {
            if (segment.isEmpty() || segment.equals(".")) {
                continue;
            }
            if (segment.equals("..")) {
                if (resolved.isEmpty()) {
                    return "";
                }
                resolved.remove(resolved.size() - 1);
            } else {
                resolved.add(segment);
            }
        }
        return String.join("/", resolved);
    }

    // P022
    public static boolean isAllowedExtension(String path) {
        List<String> allowed = Arrays.asList(".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".csv");
        int separator = Math.max(path.lastIndexOf('/'), path.lastIndexOf('\\'));
        String filename = path.substring(separator + 1);
        int dot = filename.lastIndexOf('.');
        if (dot <= 0) {
            return false;
        }
        return allowed.contains(filename.substring(dot).toLowerCase(Locale.ROOT));
    }

    // P023
    public static String sanitizeFilename(String name) {
        StringBuilder result = new StringBuilder();
        boolean lastUnderscore = false;
        int count = 0;
        int index = 0;
        while (index < name.length() && count < 200) {
            int codePoint = name.codePointAt(index);
            index += Character.charCount(codePoint);
            count++;
            boolean allowed = (codePoint >= 'a' && codePoint <= 'z') || (codePoint >= 'A' && codePoint <= 'Z')
                    || (codePoint >= '0' && codePoint <= '9') || codePoint == '.'
                    || codePoint == '_' || codePoint == '-';
            char out = allowed ? (char) codePoint : '_';
            if (out == '_') {
                if (lastUnderscore) {
                    continue;
                }
                lastUnderscore = true;
            } else {
                lastUnderscore = false;
            }
            result.append(out);
        }
        int start = 0;
        int end = result.length();
        while (start < end && result.charAt(start) == '_') {
            start++;
        }
        while (end > start && result.charAt(end - 1) == '_') {
            end--;
        }
        return start == end ? "_" : result.substring(start, end);
    }

    // P024
    public static String checkArchiveEntry(String path) {
        if (path.isEmpty()) {
            return "safe";
        }
        if (path.charAt(0) == '/' || path.indexOf('\\') >= 0) {
            return "unsafe";
        }
        int depth = 0;
        for (String segment : path.split("/", -1)) {
            if (segment.isEmpty() || segment.equals(".")) {
                continue;
            }
            if (segment.equals("..")) {
                depth--;
                if (depth < 0) {
                    return "unsafe";
                }
            } else {
                depth++;
            }
        }
        return "safe";
    }

    // P025
    public static boolean isAllowedFiletype(String ext) {
        List<String> allowed = Arrays.asList("jpg", "jpeg", "png", "gif", "bmp", "pdf", "txt", "csv", "json", "xml");
        String value = ext.startsWith(".") ? ext.substring(1) : ext;
        if (value.isEmpty()) {
            return false;
        }
        return allowed.contains(value.toLowerCase(Locale.ROOT));
    }

    // P026
    public static boolean isValidSqlIdentifier(String name) {
        if (name.isEmpty() || name.length() > 64) {
            return false;
        }
        for (int i = 0; i < name.length(); i++) {
            char c = name.charAt(i);
            boolean letterOrUnderscore = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
            boolean digit = c >= '0' && c <= '9';
            if (i == 0 ? !letterOrUnderscore : !(letterOrUnderscore || digit)) {
                return false;
            }
        }
        return true;
    }

    // P027
    public static String escapeSqlString(String s) {
        return s.replace("\\", "\\\\").replace("'", "''");
    }

    // P028
    public static String buildParamQuery(String s) {
        int bar = s.indexOf('|');
        if (bar < 0 || s.indexOf('|', bar + 1) >= 0) {
            return "INVALID";
        }
        String table = s.substring(0, bar);
        String conditions = s.substring(bar + 1);
        if (conditions.isEmpty()) {
            return "INVALID";
        }
        List<String> identifiers = new ArrayList<>();
        identifiers.add(table);
        List<String> clauses = new ArrayList<>();
        for (String condition : conditions.split(",", -1)) {
            int eq = condition.indexOf('=');
            if (eq < 0) {
                return "INVALID";
            }
            String column = condition.substring(0, eq);
            identifiers.add(column);
            clauses.add(column + "=?");
        }
        for (String identifier : identifiers) {
            if (identifier.isEmpty()) {
                return "INVALID";
            }
            for (int i = 0; i < identifier.length(); i++) {
                char c = identifier.charAt(i);
                boolean letterOrUnderscore = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
                boolean digit = c >= '0' && c <= '9';
                if (i == 0 ? !letterOrUnderscore : !(letterOrUnderscore || digit)) {
                    return "INVALID";
                }
            }
        }
        return "SELECT * FROM " + table + " WHERE " + String.join(" AND ", clauses);
    }

    // P029
    public static String validateSortDirection(String s) {
        String direction = s.trim().toUpperCase(Locale.ROOT);
        return direction.equals("ASC") || direction.equals("DESC") ? direction : "INVALID";
    }

    // P030
    public static boolean isAllowedColumn(String col) {
        List<String> allowed = Arrays.asList("id", "name", "email", "created_at", "status", "age", "role", "score");
        return allowed.contains(col.trim());
    }

    // P031
    public static String quoteShellArg(String s) {
        return "'" + s.replace("'", "'\\''") + "'";
    }

    // P032
    public static boolean isAllowedCommand(String s) {
        List<String> allowed = Arrays.asList("ls", "cat", "echo", "grep", "find", "sort", "uniq", "wc", "head", "tail");
        String command = s.trim();
        if (command.indexOf(' ') >= 0) {
            return false;
        }
        return allowed.contains(command);
    }

    // P033
    public static String detectShellMeta(String s) {
        final String dangerous = ";|&$`><(){}\\\"'\n\r";
        for (int i = 0; i < s.length(); i++) {
            if (dangerous.indexOf(s.charAt(i)) >= 0) {
                return "unsafe";
            }
        }
        return "safe";
    }

    // P034
    public static boolean isValidEnvVar(String name) {
        if (name.isEmpty() || name.length() > 64) {
            return false;
        }
        for (int i = 0; i < name.length(); i++) {
            char c = name.charAt(i);
            boolean upperOrUnderscore = (c >= 'A' && c <= 'Z') || c == '_';
            boolean digit = c >= '0' && c <= '9';
            if (i == 0 ? !upperOrUnderscore : !(upperOrUnderscore || digit)) {
                return false;
            }
        }
        return true;
    }

    // P035
    public static java.util.List<String> splitArgs(String s) {
        List<String> tokens = new ArrayList<>();
        StringBuilder current = new StringBuilder();
        boolean inQuotes = false;
        boolean hasToken = false;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '"') {
                inQuotes = !inQuotes;
                hasToken = true;
            } else if (ch == ' ' && !inQuotes) {
                if (hasToken) {
                    tokens.add(current.toString());
                    current.setLength(0);
                    hasToken = false;
                }
            } else {
                current.append(ch);
                hasToken = true;
            }
        }
        if (hasToken) {
            tokens.add(current.toString());
        }
        return tokens;
    }

    // P036
    public static String parseSafeLiteral(String s) {
        int digitsStart = (!s.isEmpty() && s.charAt(0) == '-') ? 1 : 0;
        boolean allDigits = digitsStart < s.length();
        for (int i = digitsStart; i < s.length() && allDigits; i++) {
            char c = s.charAt(i);
            if (c < '0' || c > '9') {
                allDigits = false;
            }
        }
        if (allDigits && (s.charAt(digitsStart) != '0' || s.length() - digitsStart == 1)) {
            return s.equals("-0") ? "0" : s;
        }
        if (s.equals("true") || s.equals("false") || s.equals("null")) {
            return s;
        }
        if (s.length() >= 2 && s.charAt(0) == '"' && s.charAt(s.length() - 1) == '"') {
            String inner = s.substring(1, s.length() - 1);
            StringBuilder result = new StringBuilder();
            int i = 0;
            while (i < inner.length()) {
                char ch = inner.charAt(i);
                if (ch == '\\') {
                    if (i + 1 < inner.length() && inner.charAt(i + 1) == '"') {
                        result.append('"');
                        i += 2;
                        continue;
                    }
                    return "INVALID";
                }
                if (ch == '"') {
                    return "INVALID";
                }
                result.append(ch);
                i++;
            }
            return result.toString();
        }
        return "INVALID";
    }

    // P037
    public static String parseConfigBool(String s) {
        String value = s.trim().toLowerCase(Locale.ROOT);
        if (value.equals("true") || value.equals("yes") || value.equals("1")
                || value.equals("on") || value.equals("enabled")) {
            return "true";
        }
        if (value.equals("false") || value.equals("no") || value.equals("0")
                || value.equals("off") || value.equals("disabled")) {
            return "false";
        }
        return "INVALID";
    }

    // P038
    public static boolean isAllowedConfigKey(String key) {
        List<String> allowed = Arrays.asList(
                "host", "port", "database", "username", "password",
                "timeout", "max_connections", "ssl_enabled", "log_level", "retry_count");
        return allowed.contains(key.trim());
    }

    // P039
    public static String validateToken(String s) {
        String[] parts = s.split("\\.", -1);
        if (parts.length != 3) {
            return "invalid";
        }
        for (int part = 0; part < 2; part++) {
            if (parts[part].isEmpty()) {
                return "invalid";
            }
            for (int i = 0; i < parts[part].length(); i++) {
                char c = parts[part].charAt(i);
                boolean allowed = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')
                        || (c >= '0' && c <= '9') || c == '_' || c == '-';
                if (!allowed) {
                    return "invalid";
                }
            }
        }
        if (parts[2].length() != 8) {
            return "invalid";
        }
        for (int i = 0; i < parts[2].length(); i++) {
            char c = parts[2].charAt(i);
            if (!((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f'))) {
                return "invalid";
            }
        }
        return "valid";
    }

    // P040
    public static String validateNumericExpr(String s) {
        int n = s.length();
        int i = 0;
        while (true) {
            if (i < n && s.charAt(i) == '-') {
                i++;
            }
            if (i >= n || s.charAt(i) < '0' || s.charAt(i) > '9') {
                return "invalid";
            }
            if (s.charAt(i) == '0') {
                i++;
                if (i < n && s.charAt(i) >= '0' && s.charAt(i) <= '9') {
                    return "invalid";
                }
            } else {
                while (i < n && s.charAt(i) >= '0' && s.charAt(i) <= '9') {
                    i++;
                }
            }
            int afterNumber = i;
            while (i < n && s.charAt(i) == ' ') {
                i++;
            }
            if (i == n) {
                return afterNumber == n ? "valid" : "invalid";
            }
            char op = s.charAt(i);
            if (op != '+' && op != '-' && op != '*' && op != '/') {
                return "invalid";
            }
            i++;
            while (i < n && s.charAt(i) == ' ') {
                i++;
            }
        }
    }

    // P041
    public static Map<Integer, Integer> frequencyCounter(int[] nums) {
        Map<Integer, Integer> counts = new TreeMap<>();
        for (int value : nums) {
            counts.merge(value, 1, Integer::sum);
        }
        return counts;
    }

    // P042
    public static boolean hasDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int value : nums) {
            if (!seen.add(value)) {
                return true;
            }
        }
        return false;
    }

    // P043
    public static long streamingSum(int[] nums) {
        long total = 0;
        for (int value : nums) {
            total += value;
        }
        return total;
    }

    // P044
    public static Map<String, Integer> boundedLogProcessor(String log, int maxLines) {
        int kept = 0;
        int totalWords = 0;
        if (maxLines > 0) {
            for (String line : log.split("\r\n|\r|\n", -1)) {
                if (kept >= maxLines) {
                    break;
                }
                int words = 0;
                boolean inWord = false;
                for (int i = 0; i < line.length(); i++) {
                    boolean space = " \t\n\r\f\u000B".indexOf(line.charAt(i)) >= 0;
                    if (!space && !inWord) {
                        words++;
                    }
                    inWord = !space;
                }
                if (words == 0) {
                    continue;
                }
                kept++;
                totalWords += words;
            }
        }
        Map<String, Integer> result = new LinkedHashMap<>();
        result.put("kept", kept);
        result.put("total_words", totalWords);
        return result;
    }

    // P045
    public static int[] topKFrequent(int[] nums, int k) {
        if (k <= 0 || nums.length == 0) {
            return new int[0];
        }
        Map<Integer, Integer> counts = new HashMap<>();
        for (int value : nums) {
            counts.merge(value, 1, Integer::sum);
        }
        List<Map.Entry<Integer, Integer>> entries = new ArrayList<>(counts.entrySet());
        entries.sort((a, b) -> {
            int byCount = Integer.compare(b.getValue(), a.getValue());
            return byCount != 0 ? byCount : Integer.compare(a.getKey(), b.getKey());
        });
        int take = Math.min(k, entries.size());
        int[] result = new int[take];
        for (int i = 0; i < take; i++) {
            result[i] = entries.get(i).getKey();
        }
        Arrays.sort(result);
        return result;
    }

    // P046
    public static String validateTokenFormat(String token) {
        if (token.length() < 8 || token.length() > 32) {
            return "invalid";
        }
        char first = token.charAt(0);
        if (!((first >= 'a' && first <= 'z') || (first >= 'A' && first <= 'Z'))) {
            return "invalid";
        }
        for (int i = 0; i < token.length(); i++) {
            char c = token.charAt(i);
            boolean allowed = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')
                    || (c >= '0' && c <= '9') || c == '-';
            if (!allowed) {
                return "invalid";
            }
        }
        return "valid";
    }

    // P047
    public static String evaluatePermission(String role, String action) {
        Map<String, List<String>> permissions = new HashMap<>();
        permissions.put("admin", Arrays.asList("read", "write", "delete", "execute"));
        permissions.put("editor", Arrays.asList("read", "write"));
        permissions.put("viewer", Arrays.asList("read"));
        permissions.put("guest", new ArrayList<String>());
        List<String> granted = permissions.get(role);
        return granted != null && granted.contains(action) ? "allowed" : "denied";
    }

    // P048
    public static boolean roleHasPermission(String role, String permission) {
        Map<String, List<String>> permissions = new HashMap<>();
        permissions.put("admin", Arrays.asList("read", "write", "delete", "execute"));
        permissions.put("editor", Arrays.asList("read", "write"));
        permissions.put("viewer", Arrays.asList("read"));
        permissions.put("guest", new ArrayList<String>());
        List<String> granted = permissions.get(role);
        return granted != null && granted.contains(permission);
    }

    // P049
    public static String checkSession(int lastActive, int currentTime, int timeout) {
        if (currentTime < lastActive) {
            return "invalid";
        }
        long elapsed = (long) currentTime - lastActive;
        return elapsed > timeout ? "expired" : "active";
    }

    // P050
    public static String validateScope(String requested, java.util.List<String> allowed) {
        Set<String> allowedScopes = new HashSet<>(allowed);
        int pos = 0;
        while (true) {
            int colon = requested.indexOf(':', pos);
            if (colon < 0) {
                break;
            }
            if (allowedScopes.contains(requested.substring(0, colon))) {
                return "granted";
            }
            pos = colon + 1;
        }
        return allowedScopes.contains(requested) ? "granted" : "denied";
    }
}
