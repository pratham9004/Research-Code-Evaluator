import java.math.BigInteger;
import java.util.*;

public class ProjectEuler001To050 {

    // =========================================================================
    // Problems 001 - 010
    // =========================================================================

    public static long p001() {
        return sumDivisibleBy(3, 999) + sumDivisibleBy(5, 999) - sumDivisibleBy(15, 999);
    }

    private static long sumDivisibleBy(long n, long limit) {
        long p = limit / n;
        return n * (p * (p + 1)) / 2;
    }

    public static long p002() {
        long a = 1, b = 2;
        long total = 0;
        while (a <= 4_000_000) {
            if (a % 2 == 0) total += a;
            long next = a + b;
            a = b;
            b = next;
        }
        return total;
    }

    public static long p003() {
        long n = 600851475143L;
        long factor = 2;
        while (factor * factor <= n) {
            if (n % factor == 0) {
                n /= factor;
            } else {
                factor += (factor == 2) ? 1 : 2;
            }
        }
        return n;
    }

    public static long p004() {
        long maxPal = 0;
        for (long i = 999; i >= 100; i--) {
            if (i * 999 <= maxPal) break;
            for (long j = i; j >= 100; j--) {
                long prod = i * j;
                if (prod <= maxPal) break;
                String s = String.valueOf(prod);
                if (s.equals(new StringBuilder(s).reverse().toString())) {
                    maxPal = prod;
                }
            }
        }
        return maxPal;
    }

    public static long p005() {
        long lcm = 1;
        for (long i = 1; i <= 20; i++) {
            lcm = (lcm * i) / gcd(lcm, i);
        }
        return lcm;
    }

    private static long gcd(long a, long b) {
        return b == 0 ? a : gcd(b, a % b);
    }

    public static long p006() {
        long n = 100;
        long sumOfSq = (n * (n + 1) * (2 * n + 1)) / 6;
        long sqOfSum = (n * (n + 1)) / 2;
        sqOfSum *= sqOfSum;
        return sqOfSum - sumOfSq;
    }

    public static long p007() {
        List<Long> primes = new ArrayList<>();
        primes.add(2L);
        long candidate = 3;
        while (primes.size() < 10001) {
            boolean isPrime = true;
            for (long p : primes) {
                if (p * p > candidate) break;
                if (candidate % p == 0) {
                    isPrime = false;
                    break;
                }
            }
            if (isPrime) primes.add(candidate);
            candidate += 2;
        }
        return primes.get(primes.size() - 1);
    }

    public static long p008() {
        String s = "73167176531330624919225119674426574742355349194934" +
                   "96983520312774506326239578318016984801869478451846" +
                   "43710764249037563878829138613009739521729962893441" +
                   "56037998316847121655389409001157677894120067405526" +
                   "39657535284510965700873026895316970038101458518638" +
                   "83099410177540378318400022618580885163650048297421" +
                   "58486561581175762917618622418684311263102383857001" +
                   "11361524334138398413729756015525032152643210386701" +
                   "53075475109659908180646399431682338520846062033773" +
                   "49001164205626505820982564803622262847370938131825" +
                   "67816479288610490526980220831659976372178960917363" +
                   "71787214684409012249534301465495853710507922796892" +
                   "58923542019956112129021960864034418159813629774771" +
                   "30996051870721134999999837297804995105973173281609" +
                   "63185950244594553469083026425223082533446850352619" +
                   "31188171010003137838752886587533208381420617177669" +
                   "14730359825349042875546873115956286388235378759375" +
                   "19577818577805321712268066130019278766111959092164" +
                   "20198938095257201065485863278865936153381827968230" +
                   "30195203530185296899577362259941389124972177528347";

        long maxProd = 0;
        for (int i = 0; i <= s.length() - 13; i++) {
            long prod = 1;
            for (int j = i; j < i + 13; j++) {
                prod *= Character.getNumericValue(s.charAt(j));
            }
            maxProd = Math.max(maxProd, prod);
        }
        return maxProd;
    }

    public static long p009() {
        for (long a = 1; a < 333; a++) {
            for (long b = a + 1; b < (1000 - a) / 2; b++) {
                long c = 1000 - a - b;
                if (a * a + b * b == c * c) {
                    return a * b * c;
                }
            }
        }
        return -1;
    }

    public static long p010() {
        int limit = 2_000_000;
        boolean[] isPrime = new boolean[limit];
        Arrays.fill(isPrime, true);
        isPrime[0] = isPrime[1] = false;
        for (int i = 2; i * i < limit; i++) {
            if (isPrime[i]) {
                for (int j = i * i; j < limit; j += i) {
                    isPrime[j] = false;
                }
            }
        }
        long sum = 0;
        for (int i = 0; i < limit; i++) {
            if (isPrime[i]) sum += i;
        }
        return sum;
    }

    // =========================================================================
    // Problems 011 - 020
    // =========================================================================

    public static long p011() {
        int[][] grid = {
            {8, 2, 22, 97, 38, 15, 0, 40, 0, 75, 4, 5, 7, 78, 52, 12, 50, 77, 91, 8},
            {49, 49, 99, 40, 17, 81, 18, 57, 60, 87, 17, 40, 98, 43, 69, 48, 4, 56, 62, 0},
            {81, 49, 31, 73, 55, 79, 14, 29, 93, 71, 40, 67, 53, 88, 30, 3, 49, 13, 36, 65},
            {52, 70, 95, 23, 4, 60, 11, 42, 69, 24, 68, 56, 1, 32, 56, 71, 37, 2, 36, 91},
            {22, 31, 16, 71, 51, 67, 63, 89, 41, 92, 36, 54, 22, 40, 40, 28, 66, 33, 13, 80},
            {24, 47, 32, 60, 99, 3, 45, 2, 44, 75, 30, 53, 45, 29, 2, 96, 2, 27, 2, 65},
            {1, 52, 86, 43, 84, 68, 52, 82, 86, 70, 77, 91, 85, 78, 50, 85, 31, 30, 46, 39},
            {11, 70, 69, 7, 36, 21, 41, 15, 81, 56, 0, 5, 35, 6, 62, 0, 80, 44, 5, 40},
            {22, 31, 16, 23, 19, 72, 63, 23, 4, 21, 33, 18, 57, 42, 16, 7, 0, 38, 45, 7},
            {66, 28, 80, 70, 93, 28, 0, 58, 22, 7, 37, 71, 65, 9, 53, 54, 89, 29, 44, 47},
            {43, 31, 33, 21, 30, 81, 51, 54, 38, 97, 66, 24, 25, 33, 35, 24, 27, 72, 88, 34},
            {8, 24, 71, 29, 51, 61, 42, 37, 21, 35, 85, 1, 54, 22, 12, 41, 41, 31, 18, 46},
            {38, 32, 39, 15, 24, 15, 72, 40, 14, 67, 48, 28, 51, 45, 85, 8, 4, 8, 12, 70},
            {71, 43, 6, 8, 20, 72, 0, 23, 33, 7, 53, 69, 28, 8, 85, 97, 51, 17, 33, 81},
            {17, 6, 24, 82, 36, 11, 54, 1, 44, 15, 45, 68, 23, 4, 27, 2, 0, 98, 30, 69},
            {4, 4, 52, 8, 2, 52, 64, 93, 12, 82, 17, 85, 42, 62, 45, 19, 56, 65, 9, 39},
            {50, 41, 92, 69, 39, 76, 96, 62, 84, 6, 83, 31, 3, 83, 19, 24, 23, 66, 62, 18},
            {0, 86, 2, 0, 31, 8, 56, 2, 7, 12, 37, 25, 72, 8, 49, 17, 4, 18, 14, 7},
            {4, 14, 84, 7, 29, 78, 11, 84, 30, 73, 31, 82, 83, 24, 19, 37, 84, 2, 40, 29},
            {10, 2, 33, 15, 65, 6, 24, 40, 86, 92, 14, 52, 27, 69, 23, 0, 39, 40, 42, 12}
        };

        long maxProd = 0;
        for (int r = 0; r < 20; r++) {
            for (int c = 0; c < 20; c++) {
                if (c + 3 < 20) {
                    long p = (long) grid[r][c] * grid[r][c+1] * grid[r][c+2] * grid[r][c+3];
                    maxProd = Math.max(maxProd, p);
                }
                if (r + 3 < 20) {
                    long p = (long) grid[r][c] * grid[r+1][c] * grid[r+2][c] * grid[r+3][c];
                    maxProd = Math.max(maxProd, p);
                }
                if (r + 3 < 20 && c + 3 < 20) {
                    long p = (long) grid[r][c] * grid[r+1][c+1] * grid[r+2][c+2] * grid[r+3][c+3];
                    maxProd = Math.max(maxProd, p);
                }
                if (r + 3 < 20 && c - 3 >= 0) {
                    long p = (long) grid[r][c] * grid[r+1][c-1] * grid[r+2][c-2] * grid[r+3][c-3];
                    maxProd = Math.max(maxProd, p);
                }
            }
        }
        return maxProd;
    }

    public static long p012() {
        long n = 1;
        while (true) {
            long tri = n * (n + 1) / 2;
            if (countDivisors(tri) > 500) return tri;
            n++;
        }
    }

    private static int countDivisors(long n) {
        int divs = 1;
        long d = 2;
        while (d * d <= n) {
            int count = 0;
            while (n % d == 0) {
                count++;
                n /= d;
            }
            divs *= (count + 1);
            d++;
        }
        if (n > 1) divs *= 2;
        return divs;
    }

    public static String p013() {
        String[] numbers = {
            "37107287533902102798797998220837590246510135740250",
            "46376937677490009712648124896970078050417018260538",
            "74324986199524741059474233309513058123726617309629",
            "91942213363574161572522430563301811072406154908250",
            "23067588207539346171171980310421047513778063246676",
            "89261670696623633820136378418383684178734361726757",
            "28112879812849979408065481931592621691275889832738",
            "44274228917432858478500288209259130643547389920107",
            "79171741700698913501006508210821544996293278472180",
            "92938183015305548141201261340200853701658061268073"
        };
        BigInteger sum = BigInteger.ZERO;
        for (String num : numbers) {
            sum = sum.add(new BigInteger(num));
        }
        return sum.toString().substring(0, 10);
    }

    public static long p014() {
        Map<Long, Long> memo = new HashMap<>();
        memo.put(1L, 1L);

        long maxLen = 0;
        long maxStart = 0;

        for (long i = 1; i < 1_000_000; i++) {
            long len = getCollatz(i, memo);
            if (len > maxLen) {
                maxLen = len;
                maxStart = i;
            }
        }
        return maxStart;
    }

    private static long getCollatz(long n, Map<Long, Long> memo) {
        if (memo.containsKey(n)) return memo.get(n);
        long next = (n % 2 == 0) ? n / 2 : 3 * n + 1;
        long len = 1 + getCollatz(next, memo);
        if (n < 2_000_000) memo.put(n, len);
        return len;
    }

    public static BigInteger p015() {
        return combinations(40, 20);
    }

    private static BigInteger combinations(int n, int k) {
        BigInteger res = BigInteger.ONE;
        for (int i = 1; i <= k; i++) {
            res = res.multiply(BigInteger.valueOf(n - i + 1)).divide(BigInteger.valueOf(i));
        }
        return res;
    }

    public static long p016() {
        BigInteger val = BigInteger.valueOf(2).pow(1000);
        String s = val.toString();
        long sum = 0;
        for (char c : s.toCharArray()) {
            sum += Character.getNumericValue(c);
        }
        return sum;
    }

    public static long p017() {
        String[] ones = {"", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
                         "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
                         "seventeen", "eighteen", "nineteen"};
        String[] tens = {"", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"};

        long totalLetters = 0;
        for (int i = 1; i <= 1000; i++) {
            String word = "";
            if (i == 1000) {
                word = "one thousand";
            } else {
                if (i >= 100) {
                    word += ones[i / 100] + " hundred";
                    if (i % 100 != 0) word += " and ";
                }
                int rem = i % 100;
                if (rem > 0) {
                    if (rem < 20) {
                        word += ones[rem];
                    } else {
                        word += tens[rem / 10];
                        if (rem % 10 != 0) word += "-" + ones[rem % 10];
                    }
                }
            }
            totalLetters += word.replace(" ", "").replace("-", "").length();
        }
        return totalLetters;
    }

    public static long p018() {
        int[][] triangle = {
            {75},
            {95, 64},
            {17, 47, 82},
            {18, 35, 87, 10},
            {20, 4, 82, 47, 65},
            {19, 1, 23, 75, 3, 34},
            {88, 2, 77, 73, 7, 63, 67},
            {99, 65, 4, 28, 6, 16, 70, 92},
            {41, 41, 26, 56, 83, 40, 80, 70, 33},
            {41, 48, 72, 33, 47, 32, 37, 16, 94, 29},
            {53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14},
            {70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57},
            {91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48},
            {63, 66, 4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31},
            {4, 62, 98, 27, 23, 9, 70, 98, 73, 93, 38, 53, 60, 4, 23}
        };

        for (int r = triangle.length - 2; r >= 0; r--) {
            for (int c = 0; c < triangle[r].length; c++) {
                triangle[r][c] += Math.max(triangle[r+1][c], triangle[r+1][c+1]);
            }
        }
        return triangle[0][0];
    }

    public static long p019() {
        int[] daysInMonths = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        int dayOfWeek = 2; // Jan 1 1901 was Tuesday (0=Sun, 1=Mon, 2=Tue)
        int sundayCount = 0;

        for (int year = 1901; year <= 2000; year++) {
            for (int month = 0; month < 12; month++) {
                if (dayOfWeek == 0) sundayCount++;
                int days = daysInMonths[month];
                if (month == 1 && (year % 4 == 0 && (year % 100 != 0 || year % 400 == 0))) {
                    days = 29;
                }
                dayOfWeek = (dayOfWeek + days) % 7;
            }
        }
        return sundayCount;
    }

    public static long p020() {
        BigInteger fact = BigInteger.ONE;
        for (int i = 1; i <= 100; i++) {
            fact = fact.multiply(BigInteger.valueOf(i));
        }
        long sum = 0;
        for (char c : fact.toString().toCharArray()) {
            sum += Character.getNumericValue(c);
        }
        return sum;
    }

    // =========================================================================
    // Problems 021 - 030
    // =========================================================================

    public static long p021() {
        long amicableSum = 0;
        for (int a = 2; a < 10000; a++) {
            long b = sumProperDivisors(a);
            if (a != b && sumProperDivisors(b) == a) {
                amicableSum += a;
            }
        }
        return amicableSum;
    }

    private static long sumProperDivisors(long n) {
        if (n <= 1) return 0;
        long total = 1;
        for (long i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                total += i;
                if (i * i != n) total += n / i;
            }
        }
        return total;
    }

    public static long p022() {
        String[] names = {"MARY", "PATRICIA", "LINDA", "BARBARA", "ELIZABETH", "JENNIFER", "MARIA", "SUSAN", "MARGARET", "DOROTHY", "COLIN"};
        Arrays.sort(names);
        long totalScore = 0;
        for (int i = 0; i < names.length; i++) {
            long wordValue = 0;
            for (char c : names[i].toCharArray()) {
                wordValue += (c - 'A' + 1);
            }
            totalScore += (i + 1) * wordValue;
        }
        return totalScore;
    }

    public static long p023() {
        int limit = 28123;
        List<Integer> abundants = new ArrayList<>();
        for (int i = 12; i <= limit; i++) {
            if (sumProperDivisors(i) > i) {
                abundants.add(i);
            }
        }

        boolean[] isAbundantSum = new boolean[limit + 1];
        for (int i = 0; i < abundants.size(); i++) {
            for (int j = i; j < abundants.size(); j++) {
                int s = abundants.get(i) + abundants.get(j);
                if (s <= limit) {
                    isAbundantSum[s] = true;
                } else {
                    break;
                }
            }
        }

        long nonAbundantSum = 0;
        for (int i = 1; i <= limit; i++) {
            if (!isAbundantSum[i]) nonAbundantSum += i;
        }
        return nonAbundantSum;
    }

    public static String p024() {
        List<Integer> digits = new ArrayList<>(Arrays.asList(0, 1, 2, 3, 4, 5, 6, 7, 8, 9));
        int target = 999_999;
        StringBuilder result = new StringBuilder();

        for (int i = 9; i >= 0; i--) {
            long fact = factorial(i);
            int idx = (int) (target / fact);
            target %= fact;
            result.append(digits.remove(idx));
        }
        return result.toString();
    }

    private static long factorial(int n) {
        long f = 1;
        for (int i = 2; i <= n; i++) f *= i;
        return f;
    }

    public static long p025() {
        BigInteger a = BigInteger.ONE;
        BigInteger b = BigInteger.ONE;
        long index = 2;
        while (b.toString().length() < 1000) {
            BigInteger next = a.add(b);
            a = b;
            b = next;
            index++;
        }
        return index;
    }

    public static long p026() {
        int maxLen = 0;
        int bestD = 0;

        for (int d = 2; d < 1000; d++) {
            Map<Integer, Integer> seen = new HashMap<>();
            int val = 1;
            int pos = 0;
            while (val != 0 && !seen.containsKey(val)) {
                seen.put(val, pos);
                val = (val * 10) % d;
                pos++;
            }
            if (val != 0) {
                int cycleLen = pos - seen.get(val);
                if (cycleLen > maxLen) {
                    maxLen = cycleLen;
                    bestD = d;
                }
            }
        }
        return bestD;
    }

    public static long p027() {
        int maxN = 0;
        long bestProduct = 0;

        for (int a = -999; a < 1000; a++) {
            for (int b = -1000; b <= 1000; b++) {
                if (!isPrime(b)) continue;
                int n = 0;
                while (isPrime(n * n + a * n + b)) {
                    n++;
                }
                if (n > maxN) {
                    maxN = n;
                    bestProduct = a * b;
                }
            }
        }
        return bestProduct;
    }

    private static boolean isPrime(long n) {
        if (n < 2) return false;
        for (long i = 2; i * i <= n; i++) {
            if (n % i == 0) return false;
        }
        return true;
    }

    public static long p028() {
        long total = 1;
        long current = 1;
        for (long step = 2; step <= 1000; step += 2) {
            for (int i = 0; i < 4; i++) {
                current += step;
                total += current;
            }
        }
        return total;
    }

    public static long p029() {
        Set<BigInteger> powers = new HashSet<>();
        for (int a = 2; a <= 100; a++) {
            BigInteger base = BigInteger.valueOf(a);
            for (int b = 2; b <= 100; b++) {
                powers.add(base.pow(b));
            }
        }
        return powers.size();
    }

    public static long p030() {
        long total = 0;
        long[] fifthPowers = new long[10];
        for (int i = 0; i < 10; i++) fifthPowers[i] = (long) Math.pow(i, 5);

        for (long i = 10; i <= 354294; i++) {
            long sum = 0;
            long temp = i;
            while (temp > 0) {
                sum += fifthPowers[(int) (temp % 10)];
                temp /= 10;
            }
            if (sum == i) total += i;
        }
        return total;
    }

    // =========================================================================
    // Problems 031 - 040
    // =========================================================================

    public static long p031() {
        int[] coins = {1, 2, 5, 10, 20, 50, 100, 200};
        int[] ways = new int[201];
        ways[0] = 1;
        for (int coin : coins) {
            for (int i = coin; i <= 200; i++) {
                ways[i] += ways[i - coin];
            }
        }
        return ways[200];
    }

    public static long p032() {
        Set<Long> products = new HashSet<>();
        for (long a = 1; a < 100; a++) {
            for (long b = 100; b < 10000; b++) {
                long p = a * b;
                String s = "" + a + b + p;
                if (s.length() == 9 && isPandigital1To9(s)) {
                    products.add(p);
                } else if (s.length() > 9) {
                    break;
                }
            }
        }
        long sum = 0;
        for (long p : products) sum += p;
        return sum;
    }

    private static boolean isPandigital1To9(String s) {
        if (s.length() != 9) return false;
        char[] chars = s.toCharArray();
        Arrays.sort(chars);
        return new String(chars).equals("123456789");
    }

    public static long p033() {
        long numProd = 1;
        long denProd = 1;

        for (int d = 10; d < 100; d++) {
            for (int n = 10; n < d; n++) {
                int n0 = n / 10, n1 = n % 10;
                int d0 = d / 10, d1 = d % 10;

                if (n1 == 0 && d1 == 0) continue;

                if (n1 == d0 && d1 != 0 && (double) n / d == (double) n0 / d1) {
                    numProd *= n0;
                    denProd *= d1;
                } else if (n0 == d1 && d0 != 0 && (double) n / d == (double) n1 / d0) {
                    numProd *= n1;
                    denProd *= d0;
                }
            }
        }
        return denProd / gcd(numProd, denProd);
    }

    public static long p034() {
        long[] facts = new long[10];
        for (int i = 0; i < 10; i++) facts[i] = factorial(i);

        long total = 0;
        for (long i = 10; i < 50000; i++) {
            long sum = 0;
            long temp = i;
            while (temp > 0) {
                sum += facts[(int) (temp % 10)];
                temp /= 10;
            }
            if (sum == i) total += i;
        }
        return total;
    }

    public static long p035() {
        int limit = 1_000_000;
        boolean[] isPrime = new boolean[limit];
        Arrays.fill(isPrime, true);
        isPrime[0] = isPrime[1] = false;
        for (int i = 2; i * i < limit; i++) {
            if (isPrime[i]) {
                for (int j = i * i; j < limit; j += i) {
                    isPrime[j] = false;
                }
            }
        }

        long count = 0;
        for (int i = 2; i < limit; i++) {
            if (isPrime[i]) {
                String s = String.valueOf(i);
                boolean isCircular = true;
                for (int j = 0; j < s.length(); j++) {
                    String rot = s.substring(j) + s.substring(0, j);
                    if (!isPrime[Integer.parseInt(rot)]) {
                        isCircular = false;
                        break;
                    }
                }
                if (isCircular) count++;
            }
        }
        return count;
    }

    public static long p036() {
        long total = 0;
        for (int i = 1; i < 1_000_000; i++) {
            String s10 = String.valueOf(i);
            String s2 = Integer.toBinaryString(i);
            if (s10.equals(new StringBuilder(s10).reverse().toString()) &&
                s2.equals(new StringBuilder(s2).reverse().toString())) {
                total += i;
            }
        }
        return total;
    }

    public static long p037() {
        long count = 0;
        long sum = 0;
        long n = 11;

        while (count < 11) {
            if (isPrime(n)) {
                String s = String.valueOf(n);
                boolean truncatable = true;
                for (int i = 1; i < s.length(); i++) {
                    long left = Long.parseLong(s.substring(i));
                    long right = Long.parseLong(s.substring(0, s.length() - i));
                    if (!isPrime(left) || !isPrime(right)) {
                        truncatable = false;
                        break;
                    }
                }
                if (truncatable) {
                    sum += n;
                    count++;
                }
            }
            n += 2;
        }
        return sum;
    }

    public static long p038() {
        long maxPandigital = 0;
        for (int i = 1; i < 10000; i++) {
            StringBuilder concat = new StringBuilder();
            int n = 1;
            while (concat.length() < 9) {
                concat.append(i * n);
                n++;
            }
            if (concat.length() == 9 && isPandigital1To9(concat.toString())) {
                maxPandigital = Math.max(maxPandigital, Long.parseLong(concat.toString()));
            }
        }
        return maxPandigital;
    }

    public static long p039() {
        int bestP = 0;
        int maxSolutions = 0;

        for (int p = 12; p <= 1000; p += 2) {
            int count = 0;
            for (int a = 1; a < p / 3; a++) {
                if ((p * (p - 2 * a)) % (2 * (p - a)) == 0) {
                    count++;
                }
            }
            if (count > maxSolutions) {
                maxSolutions = count;
                bestP = p;
            }
        }
        return bestP;
    }

    public static long p040() {
        StringBuilder sb = new StringBuilder();
        for (int i = 1; sb.length() < 1_000_005; i++) {
            sb.append(i);
        }
        int[] indices = {1, 10, 100, 1000, 10000, 100000, 1000000};
        long prod = 1;
        for (int idx : indices) {
            prod *= Character.getNumericValue(sb.charAt(idx - 1));
        }
        return prod;
    }

    // =========================================================================
    // Problems 041 - 050
    // =========================================================================

    public static long p041() {
        List<String> perms = new ArrayList<>();
        generatePermutations("7654321", "", perms);
        for (String p : perms) {
            long val = Long.parseLong(p);
            if (isPrime(val)) return val;
        }
        return -1;
    }

    private static void generatePermutations(String str, String prefix, List<String> result) {
        if (str.isEmpty()) {
            result.add(prefix);
        } else {
            for (int i = 0; i < str.length(); i++) {
                generatePermutations(str.substring(0, i) + str.substring(i + 1), prefix + str.charAt(i), result);
            }
        }
    }

    public static long p042() {
        Set<Integer> triangles = new HashSet<>();
        for (int n = 1; n < 100; n++) {
            triangles.add(n * (n + 1) / 2);
        }
        String[] words = {"SKY", "ABILITY", "ABLE", "ABOUT", "ABOVE", "ACCEPT", "ACCORDING", "ACCOUNT"};
        long count = 0;
        for (String w : words) {
            int score = 0;
            for (char c : w.toCharArray()) score += (c - 'A' + 1);
            if (triangles.contains(score)) count++;
        }
        return count;
    }

    public static long p043() {
        int[] primes = {2, 3, 5, 7, 11, 13, 17};
        List<String> perms = new ArrayList<>();
        generatePermutations("0123456789", "", perms);

        long sum = 0;
        for (String p : perms) {
            if (p.charAt(0) == '0') continue;
            boolean valid = true;
            for (int i = 0; i < 7; i++) {
                int sub = Integer.parseInt(p.substring(i + 1, i + 4));
                if (sub % primes[i] != 0) {
                    valid = false;
                    break;
                }
            }
            if (valid) sum += Long.parseLong(p);
        }
        return sum;
    }

    public static long p044() {
        List<Long> pentagonals = new ArrayList<>();
        int i = 1;
        while (true) {
            long pI = (long) i * (3 * i - 1) / 2;
            for (int j = pentagonals.size() - 1; j >= 0; j--) {
                long pJ = pentagonals.get(j);
                if (isPentagonal(pI - pJ) && isPentagonal(pI + pJ)) {
                    return pI - pJ;
                }
            }
            pentagonals.add(pI);
            i++;
        }
    }

    private static boolean isPentagonal(long n) {
        double val = (1.0 + Math.sqrt(1.0 + 24.0 * n)) / 6.0;
        return val == (long) val;
    }

    public static long p045() {
        long h = 144;
        while (true) {
            long hexVal = h * (2 * h - 1);
            if (isPentagonal(hexVal)) return hexVal;
            h++;
        }
    }

    public static long p046() {
        long n = 3;
        while (true) {
            if (!isPrime(n)) {
                boolean found = false;
                for (long k = 1; 2 * k * k < n; k++) {
                    if (isPrime(n - 2 * k * k)) {
                        found = true;
                        break;
                    }
                }
                if (!found) return n;
            }
            n += 2;
        }
    }

    public static long p047() {
        int limit = 200_000;
        int[] factors = new int[limit];

        for (int i = 2; i < limit; i++) {
            if (factors[i] == 0) {
                for (int j = i; j < limit; j += i) {
                    factors[j]++;
                }
            }
        }

        int consecutive = 0;
        for (int i = 2; i < limit; i++) {
            if (factors[i] == 4) {
                consecutive++;
                if (consecutive == 4) return i - 3;
            } else {
                consecutive = 0;
            }
        }
        return -1;
    }

    public static long p048() {
        BigInteger mod = BigInteger.TEN.pow(10);
        BigInteger sum = BigInteger.ZERO;
        for (int i = 1; i <= 1000; i++) {
            BigInteger base = BigInteger.valueOf(i);
            sum = sum.add(base.modPow(base, mod)).mod(mod);
        }
        return sum.longValue();
    }

    public static String p049() {
        for (int a = 1000; a < 10000; a++) {
            if (a == 1487 || !isPrime(a)) continue;
            int b = a + 3330;
            int c = a + 6660;
            if (isPrime(b) && isPrime(c)) {
                if (isPermutation(a, b) && isPermutation(a, c)) {
                    return "" + a + b + c;
                }
            }
        }
        return "";
    }

    private static boolean isPermutation(int a, int b) {
        char[] ca = String.valueOf(a).toCharArray();
        char[] cb = String.valueOf(b).toCharArray();
        Arrays.sort(ca);
        Arrays.sort(cb);
        return Arrays.equals(ca, cb);
    }

    public static long p050() {
        int limit = 1_000_000;
        boolean[] isPrime = new boolean[limit];
        Arrays.fill(isPrime, true);
        isPrime[0] = isPrime[1] = false;
        for (int i = 2; i * i < limit; i++) {
            if (isPrime[i]) {
                for (int j = i * i; j < limit; j += i) {
                    isPrime[j] = false;
                }
            }
        }

        List<Integer> primes = new ArrayList<>();
        Set<Integer> primeSet = new HashSet<>();
        for (int i = 0; i < limit; i++) {
            if (isPrime[i]) {
                primes.add(i);
                primeSet.add(i);
            }
        }

        long[] cumulativeSum = new long[primes.size() + 1];
        for (int i = 0; i < primes.size(); i++) {
            cumulativeSum[i + 1] = cumulativeSum[i] + primes.get(i);
        }

        int maxTerms = 0;
        long maxPrime = 0;

        for (int i = 0; i < cumulativeSum.length; i++) {
            for (int j = i + maxTerms + 1; j < cumulativeSum.length; j++) {
                long s = cumulativeSum[j] - cumulativeSum[i];
                if (s >= limit) break;
                if (primeSet.contains((int) s)) {
                    maxTerms = j - i;
                    maxPrime = s;
                }
            }
        }
        return maxPrime;
    }

    // =========================================================================
    // Main Method Runner
    // =========================================================================

    public static void main(String[] args) {
        System.out.println("P001: " + p001());
        System.out.println("P002: " + p002());
        System.out.println("P003: " + p003());
        System.out.println("P004: " + p004());
        System.out.println("P005: " + p005());
        System.out.println("P006: " + p006());
        System.out.println("P007: " + p007());
        System.out.println("P008: " + p008());
        System.out.println("P009: " + p009());
        System.out.println("P010: " + p010());
        System.out.println("P011: " + p011());
        System.out.println("P012: " + p012());
        System.out.println("P013: " + p013());
        System.out.println("P014: " + p014());
        System.out.println("P015: " + p015());
        System.out.println("P016: " + p016());
        System.out.println("P017: " + p017());
        System.out.println("P018: " + p018());
        System.out.println("P019: " + p019());
        System.out.println("P020: " + p020());
        System.out.println("P021: " + p021());
        System.out.println("P022: " + p022());
        System.out.println("P023: " + p023());
        System.out.println("P024: " + p024());
        System.out.println("P025: " + p025());
        System.out.println("P026: " + p026());
        System.out.println("P027: " + p027());
        System.out.println("P028: " + p028());
        System.out.println("P029: " + p029());
        System.out.println("P030: " + p030());
        System.out.println("P031: " + p031());
        System.out.println("P032: " + p032());
        System.out.println("P033: " + p033());
        System.out.println("P034: " + p034());
        System.out.println("P035: " + p035());
        System.out.println("P036: " + p036());
        System.out.println("P037: " + p037());
        System.out.println("P038: " + p038());
        System.out.println("P039: " + p039());
        System.out.println("P040: " + p040());
        System.out.println("P041: " + p041());
        System.out.println("P042: " + p042());
        System.out.println("P043: " + p043());
        System.out.println("P044: " + p044());
        System.out.println("P045: " + p045());
        System.out.println("P046: " + p046());
        System.out.println("P047: " + p047());
        System.out.println("P048: " + p048());
        System.out.println("P049: " + p049());
        System.out.println("P050: " + p050());
    }
}