P001
import java.util.*;
public class Solution {
    public static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int need = target - nums[i];
            if (seen.containsKey(need)) {
                int a = seen.get(need);
                int b = i;
                return a < b ? new int[]{a, b} : new int[]{b, a};
            }
            seen.put(nums[i], i);
        }
        return new int[0];
    }
}

P002
public class Solution {
    public static int maxSubarray(int[] nums) {
        int best = nums[0];
        int cur = nums[0];
        for (int i = 1; i < nums.length; i++) {
            cur = Math.max(nums[i], cur + nums[i]);
            best = Math.max(best, cur);
        }
        return best;
    }
}

P003
public class Solution {
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
}

P004
public class Solution {
    public static int[] mergeSortedArrays(int[] nums1, int[] nums2) {
        int[] out = new int[nums1.length + nums2.length];
        int i = 0, j = 0, k = 0;
        while (i < nums1.length && j < nums2.length) {
            if (nums1[i] <= nums2[j]) out[k++] = nums1[i++];
            else out[k++] = nums2[j++];
        }
        while (i < nums1.length) out[k++] = nums1[i++];
        while (j < nums2.length) out[k++] = nums2[j++];
        return out;
    }
}

P005
import java.util.*;
public class Solution {
    public static boolean isBalanced(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (c == '(' || c == '[' || c == '{') stack.push(c);
            else if (c == ')' || c == ']' || c == '}') {
                if (stack.isEmpty()) return false;
                char top = stack.pop();
                if ((c == ')' && top != '(') || (c == ']' && top != '[') || (c == '}' && top != '{')) return false;
            }
        }
        return stack.isEmpty();
    }
}

P006
public class Solution {
    public static int csvFieldCount(String line) {
        if (line == null || line.isEmpty()) return 0;
        int count = 1;
        int i = 0;
        int n = line.length();
        while (i < n) {
            if (line.charAt(i) == '"') {
                i++;
                while (i < n) {
                    if (line.charAt(i) == '"') {
                        if (i + 1 < n && line.charAt(i + 1) == '"') i += 2;
                        else { i++; break; }
                    } else i++;
                }
            } else if (line.charAt(i) == ',') {
                count++;
                i++;
            } else i++;
        }
        return count;
    }
}

P007
import java.util.*;
public class Solution {
    public static Map<String, Integer> countLogLevels(String log) {
        Map<String, Integer> counts = new LinkedHashMap<>();
        counts.put("ERROR", 0);
        counts.put("WARNING", 0);
        counts.put("INFO", 0);
        counts.put("DEBUG", 0);
        if (log == null || log.isEmpty()) return counts;
        String[] lines = log.split("\\r?\\n", -1);
        for (String line : lines) {
            line = line.replaceFirst("^\\s+", "");
            for (String level : new String[]{"ERROR", "WARNING", "INFO", "DEBUG"}) {
                if (line.startsWith(level) && (line.length() == level.length() || line.charAt(level.length()) == ' ' || line.charAt(level.length()) == ':')) {
                    counts.put(level, counts.get(level) + 1);
                    break;
                }
            }
        }
        return counts;
    }
}

P008
import java.util.*;
public class Solution {
    public static Map<String, String> parseKeyValue(String s) {
        Map<String, String> result = new TreeMap<>();
        if (s == null || s.trim().isEmpty()) return result;
        String[] parts = s.split(",");
        for (String part : parts) {
            part = part.trim();
            if (part.isEmpty() || !part.contains("=")) continue;
            int eq = part.indexOf('=');
            String k = part.substring(0, eq).trim();
            String v = part.substring(eq + 1).trim();
            result.put(k, v);
        }
        return result;
    }
}

P009
public class Solution {
    public static String normalizeDate(String date) {
        if (date.contains("/")) {
            String[] p = date.split("/");
            return String.format("%s-%02d-%02d", p[2], Integer.parseInt(p[0]), Integer.parseInt(p[1]));
        }
        if (date.contains("-")) {
            String[] p = date.split("-");
            return String.format("%s-%02d-%02d", p[2], Integer.parseInt(p[1]), Integer.parseInt(p[0]));
        }
        String[] p = date.split("\\.");
        return String.format("%s-%02d-%02d", p[0], Integer.parseInt(p[1]), Integer.parseInt(p[2]));
    }
}

P010
import java.util.*;
public class Solution {
    public static Map<String, Integer> wordFrequency(String text) {
        Map<String, Integer> freq = new HashMap<>();
        if (text == null) return freq;
        StringBuilder word = new StringBuilder();
        for (char c : text.toCharArray()) {
            if (Character.isLetter(c)) word.append(Character.toLowerCase(c));
            else {
                if (word.length() > 0) {
                    String w = word.toString();
                    freq.put(w, freq.getOrDefault(w, 0) + 1);
                    word.setLength(0);
                }
            }
        }
        if (word.length() > 0) {
            String w = word.toString();
            freq.put(w, freq.getOrDefault(w, 0) + 1);
        }
        return freq;
    }
}

P011
import java.util.regex.*;
public class Solution {
    public static boolean isValidEmail(String email) {
        if (email == null) return false;
        int at = email.indexOf('@');
        if (at <= 0 || at != email.lastIndexOf('@')) return false;
        String local = email.substring(0, at);
        String domain = email.substring(at + 1);
        if (local.isEmpty() || domain.isEmpty()) return false;
        if (!local.matches("[a-zA-Z0-9._%+-]+")) return false;
        if (local.startsWith(".") || local.endsWith(".") || local.contains("..")) return false;
        String[] labels = domain.split("\\.");
        if (labels.length < 2) return false;
        for (String lab : labels) {
            if (lab.isEmpty() || lab.startsWith("-") || lab.endsWith("-")) return false;
            if (!lab.matches("[a-zA-Z0-9-]+")) return false;
        }
        String tld = labels[labels.length - 1];
        return tld.length() >= 2 && tld.length() <= 6 && tld.matches("[a-zA-Z]+");
    }
}

P012
public class Solution {
    public static boolean isValidPassword(String password) {
        if (password == null || password.length() < 8) return false;
        boolean up = false, lo = false, dig = false, spe = false;
        String specials = "!@#$%^&*";
        for (char c : password.toCharArray()) {
            if (Character.isUpperCase(c)) up = true;
            else if (Character.isLowerCase(c)) lo = true;
            else if (Character.isDigit(c)) dig = true;
            else if (specials.indexOf(c) >= 0) spe = true;
        }
        return up && lo && dig && spe;
    }
}

P013
public class Solution {
    public static String isValidRange(String s) {
        if (s == null) return "INVALID";
        String[] parts = s.split("\\|", -1);
        if (parts.length != 3) return "INVALID";
        try {
            int value = Integer.parseInt(parts[0].trim());
            int mn = Integer.parseInt(parts[1].trim());
            int mx = Integer.parseInt(parts[2].trim());
            return (mn <= value && value <= mx) ? "VALID" : "INVALID";
        } catch (NumberFormatException e) {
            return "INVALID";
        }
    }
}

P014
public class Solution {
    public static boolean isValidIPv4(String ip) {
        if (ip == null) return false;
        String[] parts = ip.split("\\.", -1);
        if (parts.length != 4) return false;
        for (String p : parts) {
            if (p.isEmpty() || !p.matches("\\d+")) return false;
            if (p.length() > 1 && p.charAt(0) == '0') return false;
            try {
                int n = Integer.parseInt(p);
                if (n < 0 || n > 255) return false;
            } catch (NumberFormatException e) {
                return false;
            }
        }
        return true;
    }
}

P015
public class Solution {
    public static boolean isValidUsername(String username) {
        if (username == null || username.length() < 3 || username.length() > 20) return false;
        if (!Character.isLetter(username.charAt(0))) return false;
        for (char c : username.toCharArray()) {
            if (!Character.isLetterOrDigit(c) && c != '_' && c != '-') return false;
        }
        return true;
    }
}

P016
public class Solution {
    public static String escapeHtml(String s) {
        if (s == null) return null;
        return s.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\"", "&quot;")
                .replace("'", "&#39;");
    }
}

P017
public class Solution {
    public static String escapeCsvCell(String s) {
        if (s == null) return null;
        if (s.indexOf(',') >= 0 || s.indexOf('"') >= 0 || s.indexOf('\n') >= 0 || s.indexOf('\r') >= 0) {
            return "\"" + s.replace("\"", "\"\"") + "\"";
        }
        return s;
    }
}

P018
public class Solution {
    public static String escapeJsonString(String s) {
        if (s == null) return null;
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            int o = (int) c;
            if (c == '"') out.append("\\\"");
            else if (c == '\\') out.append("\\\\");
            else if (c == '/') out.append("\\/");
            else if (o == 8) out.append("\\b");
            else if (o == 12) out.append("\\f");
            else if (o == 10) out.append("\\n");
            else if (o == 13) out.append("\\r");
            else if (o == 9) out.append("\\t");
            else if (o >= 0 && o <= 31) out.append(String.format("\\u%04x", o));
            else out.append(c);
        }
        return out.toString();
    }
}

P019
public class Solution {
    public static String encodeUrlComponent(String s) {
        if (s == null) return null;
        StringBuilder out = new StringBuilder();
        String unreserved = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~";
        for (int i = 0; i < s.length(); ) {
            int cp = s.codePointAt(i);
            i += Character.charCount(cp);
            if (cp < 128 && unreserved.indexOf((char) cp) >= 0) {
                out.append((char) cp);
            } else {
                byte[] bytes = new String(Character.toChars(cp)).getBytes(java.nio.charset.StandardCharsets.UTF_8);
                for (byte b : bytes) {
                    out.append(String.format("%%%02X", b & 0xFF));
                }
            }
        }
        return out.toString();
    }
}

P020
import java.util.regex.*;
public class Solution {
    public static String sanitizeTemplate(String s) {
        if (s == null) return null;
        Pattern p = Pattern.compile("\\{\\{([^}]*)\\}\\}");
        Matcher m = p.matcher(s);
        StringBuffer sb = new StringBuffer();
        while (m.find()) {
            String key = m.group(1);
            if (key != null && key.matches("[a-zA-Z0-9_]+")) {
                m.appendReplacement(sb, Matcher.quoteReplacement(m.group(0)));
            } else {
                m.appendReplacement(sb, "");
            }
        }
        m.appendTail(sb);
        return sb.toString();
    }
}

P021
public class Solution {
    public static String safePathNormalize(String path) {
        if (path == null || path.trim().isEmpty()) return "";
        if (path.indexOf('\\') >= 0) return "";
        String[] parts = path.split("/");
        java.util.ArrayList<String> stack = new java.util.ArrayList<>();
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
}

P022
public class Solution {
    public static boolean isAllowedExtension(String path) {
        if (path == null) return false;
        String name = path.replace('\\', '/');
        int slash = name.lastIndexOf('/');
        if (slash >= 0) name = name.substring(slash + 1);
        int dot = name.lastIndexOf('.');
        if (dot <= 0) return false;
        String ext = name.substring(dot).toLowerCase();
        return ext.equals(".jpg") || ext.equals(".jpeg") || ext.equals(".png") ||
               ext.equals(".gif") || ext.equals(".pdf") || ext.equals(".txt") || ext.equals(".csv");
    }
}

P023
public class Solution {
    public static String sanitizeFilename(String name) {
        if (name == null) return "_";
        if (name.length() > 200) name = name.substring(0, 200);
        StringBuilder out = new StringBuilder();
        for (char c : name.toCharArray()) {
            if (Character.isLetterOrDigit(c) || c == '.' || c == '_' || c == '-') out.append(c);
            else out.append('_');
        }
        String s = out.toString();
        while (s.contains("__")) s = s.replace("__", "_");
        s = s.replaceAll("^_+|_+$", "");
        return s.isEmpty() ? "_" : s;
    }
}

P024
public class Solution {
    public static String checkArchiveEntry(String path) {
        if (path == null || path.isEmpty()) return "safe";
        if (path.startsWith("/") || path.indexOf('\\') >= 0) return "unsafe";
        int depth = 0;
        for (String part : path.split("/")) {
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
}

P025
public class Solution {
    public static boolean isAllowedFiletype(String ext) {
        if (ext == null) return false;
        String e = ext.startsWith(".") ? ext.substring(1).toLowerCase() : ext.toLowerCase();
        if (e.isEmpty()) return false;
        return e.equals("jpg") || e.equals("jpeg") || e.equals("png") || e.equals("gif") ||
               e.equals("bmp") || e.equals("pdf") || e.equals("txt") || e.equals("csv") ||
               e.equals("json") || e.equals("xml");
    }
}

P026
public class Solution {
    public static boolean isValidSqlIdentifier(String name) {
        if (name == null) return false;
        return name.matches("[a-zA-Z_][a-zA-Z0-9_]{0,63}");
    }
}

P027
public class Solution {
    public static String escapeSqlString(String s) {
        if (s == null) return null;
        return s.replace("\\", "\\\\").replace("'", "''");
    }
}

P028
public class Solution {
    public static String buildParamQuery(String s) {
        if (s == null || s.chars().filter(ch -> ch == '|').count() != 1) return "INVALID";
        String[] parts = s.split("\\|", 2);
        String table = parts[0];
        String conds = parts[1];
        if (!table.matches("[a-zA-Z_][a-zA-Z0-9_]*")) return "INVALID";
        if (conds.trim().isEmpty()) return "INVALID";
        StringBuilder sb = new StringBuilder();
        sb.append("SELECT * FROM ").append(table).append(" WHERE ");
        String[] pairs = conds.split(",");
        boolean first = true;
        for (String pair : pairs) {
            pair = pair.trim();
            if (pair.isEmpty() || !pair.contains("=")) return "INVALID";
            String col = pair.substring(0, pair.indexOf('=')).trim();
            if (!col.matches("[a-zA-Z_][a-zA-Z0-9_]*")) return "INVALID";
            if (!first) sb.append(" AND ");
            sb.append(col).append("=?");
            first = false;
        }
        return sb.toString();
    }
}

P029
public class Solution {
    public static String validateSortDirection(String s) {
        if (s == null) return "INVALID";
        String t = s.trim().toUpperCase();
        if (t.equals("ASC") || t.equals("DESC")) return t;
        return "INVALID";
    }
}

P030
public class Solution {
    public static boolean isAllowedColumn(String col) {
        if (col == null) return false;
        String c = col.trim();
        return c.equals("id") || c.equals("name") || c.equals("email") || c.equals("created_at") ||
               c.equals("status") || c.equals("age") || c.equals("role") || c.equals("score");
    }
}

P031
public class Solution {
    public static String quoteShellArg(String s) {
        if (s == null) return "''";
        return "'" + s.replace("'", "'\\''") + "'";
    }
}

P032
public class Solution {
    public static boolean isAllowedCommand(String s) {
        if (s == null) return false;
        String t = s.trim();
        if (t.indexOf(' ') >= 0) return false;
        return t.equals("ls") || t.equals("cat") || t.equals("echo") || t.equals("grep") ||
               t.equals("find") || t.equals("sort") || t.equals("uniq") || t.equals("wc") ||
               t.equals("head") || t.equals("tail");
    }
}

P033
public class Solution {
    public static String detectShellMeta(String s) {
        if (s == null) return "safe";
        String dangerous = ";|&$`><(){}\\\"'\n\r";
        for (int i = 0; i < s.length(); i++) {
            if (dangerous.indexOf(s.charAt(i)) >= 0) return "unsafe";
        }
        return "safe";
    }
}

P034
public class Solution {
    public static boolean isValidEnvVar(String name) {
        if (name == null) return false;
        return name.matches("[A-Z_][A-Z0-9_]{0,63}");
    }
}

P035
import java.util.*;
public class Solution {
    public static List<String> splitArgs(String s) {
        List<String> tokens = new ArrayList<>();
        if (s == null || s.isEmpty()) return tokens;
        int i = 0, n = s.length();
        while (i < n) {
            while (i < n && s.charAt(i) == ' ') i++;
            if (i >= n) break;
            if (s.charAt(i) == '"') {
                i++;
                StringBuilder buf = new StringBuilder();
                while (i < n && s.charAt(i) != '"') {
                    buf.append(s.charAt(i));
                    i++;
                }
                if (i < n && s.charAt(i) == '"') i++;
                tokens.add(buf.toString());
            } else {
                StringBuilder buf = new StringBuilder();
                while (i < n && s.charAt(i) != ' ') {
                    buf.append(s.charAt(i));
                    i++;
                }
                tokens.add(buf.toString());
            }
        }
        return tokens;
    }
}

P036
public class Solution {
    public static String parseSafeLiteral(String s) {
        if (s == null) return "INVALID";
        if (s.equals("true") || s.equals("false") || s.equals("null")) return s;
        if (s.length() >= 2 && s.charAt(0) == '"' && s.charAt(s.length() - 1) == '"') {
            StringBuilder out = new StringBuilder();
            for (int i = 1; i < s.length() - 1; i++) {
                if (s.charAt(i) == '\\' && i + 1 < s.length() - 1 && s.charAt(i + 1) == '"') {
                    out.append('"');
                    i++;
                } else if (s.charAt(i) == '"') {
                    return "INVALID";
                } else {
                    out.append(s.charAt(i));
                }
            }
            return out.toString();
        }
        if (s.equals("0")) return "0";
        if (s.startsWith("-")) {
            if (s.length() == 1) return "INVALID";
            String rest = s.substring(1);
            if (!rest.matches("\\d+") || (rest.length() > 1 && rest.charAt(0) == '0')) return "INVALID";
            return s;
        }
        if (s.matches("\\d+")) {
            if (s.length() > 1 && s.charAt(0) == '0') return "INVALID";
            return s;
        }
        return "INVALID";
    }
}

P037
public class Solution {
    public static String parseConfigBool(String s) {
        if (s == null) return "INVALID";
        String t = s.trim().toLowerCase();
        if (t.equals("true") || t.equals("yes") || t.equals("1") || t.equals("on") || t.equals("enabled")) return "true";
        if (t.equals("false") || t.equals("no") || t.equals("0") || t.equals("off") || t.equals("disabled")) return "false";
        return "INVALID";
    }
}

P038
public class Solution {
    public static boolean isAllowedConfigKey(String key) {
        if (key == null) return false;
        String k = key.trim();
        return k.equals("host") || k.equals("port") || k.equals("database") || k.equals("username") ||
               k.equals("password") || k.equals("timeout") || k.equals("max_connections") ||
               k.equals("ssl_enabled") || k.equals("log_level") || k.equals("retry_count");
    }
}

P039
public class Solution {
    public static String validateToken(String s) {
        if (s == null) return "invalid";
        String[] parts = s.split("\\.", -1);
        if (parts.length != 3) return "invalid";
        if (!parts[0].matches("[A-Za-z0-9_-]+")) return "invalid";
        if (!parts[1].matches("[A-Za-z0-9_-]+")) return "invalid";
        if (!parts[2].matches("[0-9a-f]{8}")) return "invalid";
        return "valid";
    }
}

P040
public class Solution {
    public static String validateNumericExpr(String s) {
        if (s == null) return "invalid";
        s = s.trim();
        if (s.isEmpty()) return "invalid";
        String num = "(?:-?(?:0|[1-9]\\d*))";
        String op = "[+\\-*/]";
        if (s.matches("^" + num + "(?:\\s*" + op + "\\s*" + num + ")*$")) return "valid";
        return "invalid";
    }
}

P041
import java.util.*;
public class Solution {
    public static Map<Integer, Integer> frequencyCounter(int[] nums) {
        Map<Integer, Integer> map = new TreeMap<>();
        if (nums == null) return map;
        for (int n : nums) map.put(n, map.getOrDefault(n, 0) + 1);
        return map;
    }
}

P042
import java.util.*;
public class Solution {
    public static boolean hasDuplicate(int[] nums) {
        if (nums == null || nums.length == 0) return false;
        Set<Integer> seen = new HashSet<>();
        for (int n : nums) {
            if (!seen.add(n)) return true;
        }
        return false;
    }
}

P043
public class Solution {
    public static long streamingSum(int[] nums) {
        if (nums == null || nums.length == 0) return 0L;
        long sum = 0;
        for (int n : nums) sum += n;
        return sum;
    }
}

P044
import java.util.*;
public class Solution {
    public static Map<String, Integer> boundedLogProcessor(String log, int maxLines) {
        Map<String, Integer> res = new LinkedHashMap<>();
        res.put("kept", 0);
        res.put("total_words", 0);
        if (log == null || maxLines <= 0) return res;
        int kept = 0, totalWords = 0;
        String[] lines = log.split("\\r?\\n", -1);
        for (String line : lines) {
            if (line.trim().isEmpty()) continue;
            if (kept >= maxLines) break;
            kept++;
            totalWords += line.trim().isEmpty() ? 0 : line.trim().split("\\s+").length;
        }
        res.put("kept", kept);
        res.put("total_words", totalWords);
        return res;
    }
}

P045
import java.util.*;
public class Solution {
    public static int[] topKFrequent(int[] nums, int k) {
        if (nums == null || nums.length == 0 || k <= 0) return new int[0];
        Map<Integer, Integer> freq = new HashMap<>();
        for (int n : nums) freq.put(n, freq.getOrDefault(n, 0) + 1);
        List<Map.Entry<Integer, Integer>> list = new ArrayList<>(freq.entrySet());
        list.sort((a, b) -> {
            int cmp = Integer.compare(b.getValue(), a.getValue());
            if (cmp != 0) return cmp;
            return Integer.compare(a.getKey(), b.getKey());
        });
        int take = Math.min(k, list.size());
        int[] selected = new int[take];
        for (int i = 0; i < take; i++) selected[i] = list.get(i).getKey();
        Arrays.sort(selected);
        return selected;
    }
}

P046
public class Solution {
    public static String validateTokenFormat(String token) {
        if (token == null) return "invalid";
        if (token.matches("[a-zA-Z][a-zA-Z0-9\\-]{7,31}")) return "valid";
        return "invalid";
    }
}

P047
import java.util.*;
public class Solution {
    public static String evaluatePermission(String role, String action) {
        Map<String, Set<String>> perms = new HashMap<>();
        perms.put("admin", new HashSet<>(Arrays.asList("read", "write", "delete", "execute")));
        perms.put("editor", new HashSet<>(Arrays.asList("read", "write")));
        perms.put("viewer", new HashSet<>(Arrays.asList("read")));
        perms.put("guest", new HashSet<>());
        if (perms.containsKey(role) && perms.get(role).contains(action)) return "allowed";
        return "denied";
    }
}

P048
import java.util.*;
public class Solution {
    public static boolean roleHasPermission(String role, String permission) {
        Map<String, Set<String>> perms = new HashMap<>();
        perms.put("admin", new HashSet<>(Arrays.asList("read", "write", "delete", "execute")));
        perms.put("editor", new HashSet<>(Arrays.asList("read", "write")));
        perms.put("viewer", new HashSet<>(Arrays.asList("read")));
        perms.put("guest", new HashSet<>());
        return perms.containsKey(role) && perms.get(role).contains(permission);
    }
}

P049
public class Solution {
    public static String checkSession(int lastActive, int currentTime, int timeout) {
        if (currentTime < lastActive) return "invalid";
        int elapsed = currentTime - lastActive;
        if (elapsed > timeout) return "expired";
        return "active";
    }
}

P050
import java.util.*;
public class Solution {
    public static String validateScope(String requested, List<String> allowed) {
        if (allowed == null || allowed.isEmpty()) return "denied";
        if (allowed.contains(requested)) return "granted";
        String[] parts = requested.split(":");
        for (int i = 1; i < parts.length; i++) {
            String parent = String.join(":", Arrays.copyOf(parts, i));
            if (allowed.contains(parent)) return "granted";
        }
        return "denied";
    }
}