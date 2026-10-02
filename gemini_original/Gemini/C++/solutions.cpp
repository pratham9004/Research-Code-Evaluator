#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <numeric>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <cmath>

using namespace std;

// =========================================================================
// Big Integer & Math Helpers
// =========================================================================

static string addBigInt(const string& a, const string& b) {
    string res = "";
    int i = (int)a.length() - 1, j = (int)b.length() - 1, carry = 0;
    while (i >= 0 || j >= 0 || carry) {
        int sum = carry;
        if (i >= 0) sum += a[i--] - '0';
        if (j >= 0) sum += b[j--] - '0';
        res += to_string(sum % 10);
        carry = sum / 10;
    }
    reverse(res.begin(), res.end());
    return res;
}

static string multiplyInt(const string& s, int n) {
    string res = "";
    int carry = 0;
    for (int i = (int)s.length() - 1; i >= 0; i--) {
        int prod = (s[i] - '0') * n + carry;
        res += to_string(prod % 10);
        carry = prod / 10;
    }
    while (carry) {
        res += to_string(carry % 10);
        carry /= 10;
    }
    reverse(res.begin(), res.end());
    return res;
}

static bool isPrime(long long n) {
    if (n < 2) return false;
    for (long long i = 2; i * i <= n; i++) {
        if (n % i == 0) return false;
    }
    return true;
}

static bool isPandigital1To9(const string& s) {
    if (s.length() != 9) return false;
    string temp = s;
    sort(temp.begin(), temp.end());
    return temp == "123456789";
}

static long long sumProperDivisors(long long n) {
    if (n <= 1) return 0;
    long long total = 1;
    for (long long i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            total += i;
            if (i * i != n) total += n / i;
        }
    }
    return total;
}

// =========================================================================
// Problems 001 - 010
// =========================================================================

long long p001() {
    auto sumDiv = [](long long n, long long limit) {
        long long p = limit / n;
        return n * (p * (p + 1)) / 2;
    };
    return sumDiv(3, 999) + sumDiv(5, 999) - sumDiv(15, 999);
}

long long p002() {
    long long a = 1, b = 2, total = 0;
    while (a <= 4000000) {
        if (a % 2 == 0) total += a;
        long long next = a + b;
        a = b; b = next;
    }
    return total;
}

long long p003() {
    long long n = 600851475143LL;
    long long factor = 2;
    while (factor * factor <= n) {
        if (n % factor == 0) n /= factor;
        else factor += (factor == 2) ? 1 : 2;
    }
    return n;
}

long long p004() {
    long long maxPal = 0;
    for (long long i = 999; i >= 100; i--) {
        if (i * 999 <= maxPal) break;
        for (long long j = i; j >= 100; j--) {
            long long prod = i * j;
            if (prod <= maxPal) break;
            string s = to_string(prod);
            string rev = s;
            reverse(rev.begin(), rev.end());
            if (s == rev) maxPal = prod;
        }
    }
    return maxPal;
}

long long p005() {
    long long lcm_val = 1;
    for (long long i = 1; i <= 20; i++) {
        lcm_val = std::lcm(lcm_val, i);
    }
    return lcm_val;
}

long long p006() {
    long long n = 100;
    long long sumSq = (n * (n + 1) * (2 * n + 1)) / 6;
    long long sqSum = (n * (n + 1)) / 2;
    return sqSum * sqSum - sumSq;
}

long long p007() {
    vector<long long> primes = {2};
    long long candidate = 3;
    while (primes.size() < 10001) {
        bool isP = true;
        for (long long p : primes) {
            if (p * p > candidate) break;
            if (candidate % p == 0) { isP = false; break; }
        }
        if (isP) primes.push_back(candidate);
        candidate += 2;
    }
    return primes.back();
}

long long p008() {
    string s = "73167176531330624919225119674426574742355349194934"
               "96983520312774506326239578318016984801869478451846"
               "43710764249037563878829138613009739521729962893441"
               "56037998316847121655389409001157677894120067405526"
               "39657535284510965700873026895316970038101458518638"
               "83099410177540378318400022618580885163650048297421"
               "58486561581175762917618622418684311263102383857001"
               "11361524334138398413729756015525032152643210386701"
               "53075475109659908180646399431682338520846062033773"
               "49001164205626505820982564803622262847370938131825"
               "67816479288610490526980220831659976372178960917363"
               "71787214684409012249534301465495853710507922796892"
               "58923542019956112129021960864034418159813629774771"
               "30996051870721134999999837297804995105973173281609"
               "63185950244594553469083026425223082533446850352619"
               "31188171010003137838752886587533208381420617177669"
               "14730359825349042875546873115956286388235378759375"
               "19577818577805321712268066130019278766111959092164"
               "20198938095257201065485863278865936153381827968230"
               "30195203530185296899577362259941389124972177528347";
    long long maxP = 0;
    for (size_t i = 0; i + 13 <= s.length(); i++) {
        long long prod = 1;
        for (size_t j = i; j < i + 13; j++) prod *= (s[j] - '0');
        maxP = max(maxP, prod);
    }
    return maxP;
}

long long p009() {
    for (long long a = 1; a < 333; a++) {
        for (long long b = a + 1; b < (1000 - a) / 2; b++) {
            long long c = 1000 - a - b;
            if (a * a + b * b == c * c) return a * b * c;
        }
    }
    return -1;
}

long long p010() {
    int limit = 2000000;
    vector<bool> isP(limit, true);
    isP[0] = isP[1] = false;
    for (int i = 2; i * i < limit; i++) {
        if (isP[i]) {
            for (int j = i * i; j < limit; j += i) isP[j] = false;
        }
    }
    long long sum = 0;
    for (int i = 0; i < limit; i++) if (isP[i]) sum += i;
    return sum;
}

// =========================================================================
// Problems 011 - 020
// =========================================================================

long long p011() {
    int grid[20][20] = {
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

    long long maxP = 0;
    for (int r = 0; r < 20; r++) {
        for (int c = 0; c < 20; c++) {
            if (c + 3 < 20) {
                long long p = (long long)grid[r][c] * grid[r][c+1] * grid[r][c+2] * grid[r][c+3];
                maxP = max(maxP, p);
            }
            if (r + 3 < 20) {
                long long p = (long long)grid[r][c] * grid[r+1][c] * grid[r+2][c] * grid[r+3][c];
                maxP = max(maxP, p);
            }
            if (r + 3 < 20 && c + 3 < 20) {
                long long p = (long long)grid[r][c] * grid[r+1][c+1] * grid[r+2][c+2] * grid[r+3][c+3];
                maxP = max(maxP, p);
            }
            if (r + 3 < 20 && c - 3 >= 0) {
                long long p = (long long)grid[r][c] * grid[r+1][c-1] * grid[r+2][c-2] * grid[r+3][c-3];
                maxP = max(maxP, p);
            }
        }
    }
    return maxP;
}

long long p012() {
    auto countDivs = [](long long n) {
        int divs = 1;
        long long d = 2;
        while (d * d <= n) {
            int count = 0;
            while (n % d == 0) { count++; n /= d; }
            divs *= (count + 1);
            d++;
        }
        if (n > 1) divs *= 2;
        return divs;
    };

    long long n = 1;
    while (true) {
        long long tri = n * (n + 1) / 2;
        if (countDivs(tri) > 500) return tri;
        n++;
    }
}

string p013() {
    vector<string> numbers = {
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
    string sum = "0";
    for (const auto& num : numbers) {
        sum = addBigInt(sum, num);
    }
    return sum.substr(0, 10);
}

long long p014() {
    unordered_map<long long, long long> memo;
    memo[1] = 1;

    auto getCollatz = [&](auto& self, long long n) -> long long {
        if (memo.count(n)) return memo[n];
        long long next = (n % 2 == 0) ? n / 2 : 3 * n + 1;
        long long len = 1 + self(self, next);
        if (n < 2000000) memo[n] = len;
        return len;
    };

    long long maxLen = 0, maxStart = 0;
    for (long long i = 1; i < 1000000; i++) {
        long long len = getCollatz(getCollatz, i);
        if (len > maxLen) {
            maxLen = len;
            maxStart = i;
        }
    }
    return maxStart;
}

long long p015() {
    long long res = 1;
    for (int i = 1; i <= 20; i++) {
        res = res * (40 - i + 1) / i;
    }
    return res;
}

long long p016() {
    string s = "1";
    for (int i = 0; i < 1000; i++) {
        s = multiplyInt(s, 2);
    }
    long long sum = 0;
    for (char c : s) sum += c - '0';
    return sum;
}

long long p017() {
    vector<string> ones = {"", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
                           "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
                           "seventeen", "eighteen", "nineteen"};
    vector<string> tens = {"", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"};

    long long totalLetters = 0;
    for (int i = 1; i <= 1000; i++) {
        string word = "";
        if (i == 1000) {
            word = "onethousand";
        } else {
            if (i >= 100) {
                word += ones[i / 100] + "hundred";
                if (i % 100 != 0) word += "and";
            }
            int rem = i % 100;
            if (rem > 0) {
                if (rem < 20) word += ones[rem];
                else {
                    word += tens[rem / 10];
                    if (rem % 10 != 0) word += ones[rem % 10];
                }
            }
        }
        totalLetters += word.length();
    }
    return totalLetters;
}

long long p018() {
    vector<vector<int>> triangle = {
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

    for (int r = (int)triangle.size() - 2; r >= 0; r--) {
        for (size_t c = 0; c < triangle[r].size(); c++) {
            triangle[r][c] += max(triangle[r+1][c], triangle[r+1][c+1]);
        }
    }
    return triangle[0][0];
}

long long p019() {
    int daysInMonths[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    int dayOfWeek = 2; // Jan 1 1901 was Tuesday (0=Sun, 1=Mon, 2=Tue)
    int sundayCount = 0;

    for (int year = 1901; year <= 2000; year++) {
        for (int month = 0; month < 12; month++) {
            if (dayOfWeek == 0) sundayCount++;
            int days = daysInMonths[month];
            if (month == 1 && (year % 4 == 0 && (year % 100 != 0 || year % 400 == 0))) days = 29;
            dayOfWeek = (dayOfWeek + days) % 7;
        }
    }
    return sundayCount;
}

long long p020() {
    string fact = "1";
    for (int i = 1; i <= 100; i++) fact = multiplyInt(fact, i);
    long long sum = 0;
    for (char c : fact) sum += c - '0';
    return sum;
}

// =========================================================================
// Problems 021 - 030
// =========================================================================

long long p021() {
    long long amicableSum = 0;
    for (int a = 2; a < 10000; a++) {
        long long b = sumProperDivisors(a);
        if (a != b && sumProperDivisors(b) == a) amicableSum += a;
    }
    return amicableSum;
}

long long p022() {
    vector<string> names = {"MARY", "PATRICIA", "LINDA", "BARBARA", "ELIZABETH", "JENNIFER", "MARIA", "SUSAN", "MARGARET", "DOROTHY", "COLIN"};
    sort(names.begin(), names.end());
    long long totalScore = 0;
    for (size_t i = 0; i < names.size(); i++) {
        long long wordVal = 0;
        for (char c : names[i]) wordVal += (c - 'A' + 1);
        totalScore += (i + 1) * wordVal;
    }
    return totalScore;
}

long long p023() {
    int limit = 28123;
    vector<int> abundants;
    for (int i = 12; i <= limit; i++) {
        if (sumProperDivisors(i) > i) abundants.push_back(i);
    }

    vector<bool> isAbundantSum(limit + 1, false);
    for (size_t i = 0; i < abundants.size(); i++) {
        for (size_t j = i; j < abundants.size(); j++) {
            int s = abundants[i] + abundants[j];
            if (s <= limit) isAbundantSum[s] = true;
            else break;
        }
    }

    long long nonAbundantSum = 0;
    for (int i = 1; i <= limit; i++) {
        if (!isAbundantSum[i]) nonAbundantSum += i;
    }
    return nonAbundantSum;
}

string p024() {
    string s = "0123456789";
    for (int i = 1; i < 1000000; i++) {
        next_permutation(s.begin(), s.end());
    }
    return s;
}

long long p025() {
    string a = "1", b = "1";
    long long index = 2;
    while (b.length() < 1000) {
        string next = addBigInt(a, b);
        a = b;
        b = next;
        index++;
    }
    return index;
}

long long p026() {
    int maxLen = 0, bestD = 0;
    for (int d = 2; d < 1000; d++) {
        unordered_map<int, int> seen;
        int val = 1, pos = 0;
        while (val != 0 && !seen.count(val)) {
            seen[val] = pos++;
            val = (val * 10) % d;
        }
        if (val != 0) {
            int cycleLen = pos - seen[val];
            if (cycleLen > maxLen) {
                maxLen = cycleLen;
                bestD = d;
            }
        }
    }
    return bestD;
}

long long p027() {
    int maxN = 0;
    long long bestProd = 0;
    for (int a = -999; a < 1000; a++) {
        for (int b = -1000; b <= 1000; b++) {
            if (!isPrime(b)) continue;
            int n = 0;
            while (isPrime(n * n + a * n + b)) n++;
            if (n > maxN) {
                maxN = n;
                bestProd = a * b;
            }
        }
    }
    return bestProd;
}

long long p028() {
    long long total = 1, current = 1;
    for (long long step = 2; step <= 1000; step += 2) {
        for (int i = 0; i < 4; i++) {
            current += step;
            total += current;
        }
    }
    return total;
}

long long p029() {
    set<string> powers;
    for (int a = 2; a <= 100; a++) {
        string val = "1";
        for (int b = 1; b <= 100; b++) {
            val = multiplyInt(val, a);
            if (b >= 2) powers.insert(val);
        }
    }
    return powers.size();
}

long long p030() {
    long long total = 0;
    long long fifthPowers[10];
    for (int i = 0; i < 10; i++) fifthPowers[i] = (long long)pow(i, 5);

    for (long long i = 10; i <= 354294; i++) {
        long long sum = 0, temp = i;
        while (temp > 0) {
            sum += fifthPowers[temp % 10];
            temp /= 10;
        }
        if (sum == i) total += i;
    }
    return total;
}

// =========================================================================
// Problems 031 - 040
// =========================================================================

long long p031() {
    int coins[] = {1, 2, 5, 10, 20, 50, 100, 200};
    vector<int> ways(201, 0);
    ways[0] = 1;
    for (int coin : coins) {
        for (int i = coin; i <= 200; i++) {
            ways[i] += ways[i - coin];
        }
    }
    return ways[200];
}

long long p032() {
    set<long long> products;
    for (long long a = 1; a < 100; a++) {
        for (long long b = 100; b < 10000; b++) {
            long long p = a * b;
            string s = to_string(a) + to_string(b) + to_string(p);
            if (s.length() == 9 && isPandigital1To9(s)) products.insert(p);
            else if (s.length() > 9) break;
        }
    }
    long long sum = 0;
    for (long long p : products) sum += p;
    return sum;
}

long long p033() {
    long long numProd = 1, denProd = 1;
    for (int d = 10; d < 100; d++) {
        for (int n = 10; n < d; n++) {
            int n0 = n / 10, n1 = n % 10;
            int d0 = d / 10, d1 = d % 10;
            if (n1 == 0 && d1 == 0) continue;

            if (n1 == d0 && d1 != 0 && (double)n / d == (double)n0 / d1) {
                numProd *= n0; denProd *= d1;
            } else if (n0 == d1 && d0 != 0 && (double)n / d == (double)n1 / d0) {
                numProd *= n1; denProd *= d0;
            }
        }
    }
    return denProd / std::gcd(numProd, denProd);
}

long long p034() {
    auto fact = [](int n) {
        long long f = 1;
        for (int i = 2; i <= n; i++) f *= i;
        return f;
    };
    long long facts[10];
    for (int i = 0; i < 10; i++) facts[i] = fact(i);

    long long total = 0;
    for (long long i = 10; i < 50000; i++) {
        long long sum = 0, temp = i;
        while (temp > 0) {
            sum += facts[temp % 10];
            temp /= 10;
        }
        if (sum == i) total += i;
    }
    return total;
}

long long p035() {
    int limit = 1000000;
    vector<bool> isP(limit, true);
    isP[0] = isP[1] = false;
    for (int i = 2; i * i < limit; i++) {
        if (isP[i]) {
            for (int j = i * i; j < limit; j += i) isP[j] = false;
        }
    }

    long long count = 0;
    for (int i = 2; i < limit; i++) {
        if (isP[i]) {
            string s = to_string(i);
            bool isCirc = true;
            for (size_t j = 0; j < s.length(); j++) {
                string rot = s.substr(j) + s.substr(0, j);
                if (!isP[stoi(rot)]) { isCirc = false; break; }
            }
            if (isCirc) count++;
        }
    }
    return count;
}

long long p036() {
    auto toBinary = [](int n) {
        string r = "";
        while (n > 0) { r += (n % 2 ? '1' : '0'); n /= 2; }
        return r;
    };

    long long total = 0;
    for (int i = 1; i < 1000000; i++) {
        string s10 = to_string(i);
        string rev10 = s10; reverse(rev10.begin(), rev10.end());
        if (s10 == rev10) {
            string s2 = toBinary(i);
            string rev2 = s2; reverse(rev2.begin(), rev2.end());
            if (s2 == rev2) total += i;
        }
    }
    return total;
}

long long p037() {
    long long count = 0, sum = 0, n = 11;
    while (count < 11) {
        if (isPrime(n)) {
            string s = to_string(n);
            bool truncatable = true;
            for (size_t i = 1; i < s.length(); i++) {
                long long left = stoll(s.substr(i));
                long long right = stoll(s.substr(0, s.length() - i));
                if (!isPrime(left) || !isPrime(right)) {
                    truncatable = false;
                    break;
                }
            }
            if (truncatable) { sum += n; count++; }
        }
        n += 2;
    }
    return sum;
}

long long p038() {
    long long maxPandigital = 0;
    for (int i = 1; i < 10000; i++) {
        string concat = "";
        int n = 1;
        while (concat.length() < 9) {
            concat += to_string(i * n);
            n++;
        }
        if (concat.length() == 9 && isPandigital1To9(concat)) {
            maxPandigital = max(maxPandigital, stoll(concat));
        }
    }
    return maxPandigital;
}

long long p039() {
    int bestP = 0, maxSolutions = 0;
    for (int p = 12; p <= 1000; p += 2) {
        int count = 0;
        for (int a = 1; a < p / 3; a++) {
            if ((p * (p - 2 * a)) % (2 * (p - a)) == 0) count++;
        }
        if (count > maxSolutions) {
            maxSolutions = count;
            bestP = p;
        }
    }
    return bestP;
}

long long p040() {
    string s = "";
    for (int i = 1; s.length() < 1000005; i++) s += to_string(i);
    int indices[] = {1, 10, 100, 1000, 10000, 100000, 1000000};
    long long prod = 1;
    for (int idx : indices) prod *= (s[idx - 1] - '0');
    return prod;
}

// =========================================================================
// Problems 041 - 050
// =========================================================================

long long p041() {
    string s = "7654321";
    do {
        long long val = stoll(s);
        if (isPrime(val)) return val;
    } while (prev_permutation(s.begin(), s.end()));
    return -1;
}

long long p042() {
    unordered_set<int> triangles;
    for (int n = 1; n < 100; n++) triangles.insert(n * (n + 1) / 2);
    vector<string> words = {"SKY", "ABILITY", "ABLE", "ABOUT", "ABOVE", "ACCEPT", "ACCORDING", "ACCOUNT"};
    long long count = 0;
    for (const string& w : words) {
        int score = 0;
        for (char c : w) score += (c - 'A' + 1);
        if (triangles.count(score)) count++;
    }
    return count;
}

long long p043() {
    string s = "0123456789";
    int primes[] = {2, 3, 5, 7, 11, 13, 17};
    long long sum = 0;
    do {
        if (s[0] == '0') continue;
        bool valid = true;
        for (int i = 0; i < 7; i++) {
            int sub = stoi(s.substr(i + 1, 3));
            if (sub % primes[i] != 0) { valid = false; break; }
        }
        if (valid) sum += stoll(s);
    } while (next_permutation(s.begin(), s.end()));
    return sum;
}

long long p044() {
    auto isPentagonal = [](long long n) {
        double val = (1.0 + sqrt(1.0 + 24.0 * n)) / 6.0;
        return val == (long long)val;
    };

    vector<long long> pentagonals;
    int i = 1;
    while (true) {
        long long pI = (long long)i * (3 * i - 1) / 2;
        for (int j = (int)pentagonals.size() - 1; j >= 0; j--) {
            long long pJ = pentagonals[j];
            if (isPentagonal(pI - pJ) && isPentagonal(pI + pJ)) {
                return pI - pJ;
            }
        }
        pentagonals.push_back(pI);
        i++;
    }
}

long long p045() {
    auto isPentagonal = [](long long n) {
        double val = (1.0 + sqrt(1.0 + 24.0 * n)) / 6.0;
        return val == (long long)val;
    };

    long long h = 144;
    while (true) {
        long long hexVal = h * (2 * h - 1);
        if (isPentagonal(hexVal)) return hexVal;
        h++;
    }
}

long long p046() {
    long long n = 3;
    while (true) {
        if (!isPrime(n)) {
            bool found = false;
            for (long long k = 1; 2 * k * k < n; k++) {
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

long long p047() {
    int limit = 200000;
    vector<int> factors(limit, 0);

    for (int i = 2; i < limit; i++) {
        if (factors[i] == 0) {
            for (int j = i; j < limit; j += i) factors[j]++;
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

long long p048() {
    long long mod = 10000000000LL;
    long long total = 0;
    auto modPow = [&](long long base, long long exp) {
        long long res = 1;
        base %= mod;
        while (exp > 0) {
            if (exp % 2 == 1) res = (long long)((__int128)res * base % mod);
            base = (long long)((__int128)base * base % mod);
            exp /= 2;
        }
        return res;
    };
    for (int i = 1; i <= 1000; i++) {
        total = (total + modPow(i, i)) % mod;
    }
    return total;
}

string p049() {
    auto isPerm = [](int a, int b) {
        string sa = to_string(a), sb = to_string(b);
        sort(sa.begin(), sa.end());
        sort(sb.begin(), sb.end());
        return sa == sb;
    };

    for (int a = 1000; a < 10000; a++) {
        if (a == 1487 || !isPrime(a)) continue;
        int b = a + 3330;
        int c = a + 6660;
        if (isPrime(b) && isPrime(c)) {
            if (isPerm(a, b) && isPerm(a, c)) {
                return to_string(a) + to_string(b) + to_string(c);
            }
        }
    }
    return "";
}

long long p050() {
    int limit = 1000000;
    vector<bool> isP(limit, true);
    isP[0] = isP[1] = false;
    for (int i = 2; i * i < limit; i++) {
        if (isP[i]) {
            for (int j = i * i; j < limit; j += i) isP[j] = false;
        }
    }

    vector<int> primes;
    unordered_set<int> primeSet;
    for (int i = 0; i < limit; i++) {
        if (isP[i]) {
            primes.push_back(i);
            primeSet.insert(i);
        }
    }

    vector<long long> cumSum(primes.size() + 1, 0);
    for (size_t i = 0; i < primes.size(); i++) {
        cumSum[i + 1] = cumSum[i] + primes[i];
    }

    int maxTerms = 0;
    long long maxPrime = 0;

    for (size_t i = 0; i < cumSum.size(); i++) {
        for (size_t j = i + maxTerms + 1; j < cumSum.size(); j++) {
            long long s = cumSum[j] - cumSum[i];
            if (s >= limit) break;
            if (primeSet.count((int)s)) {
                maxTerms = (int)(j - i);
                maxPrime = s;
            }
        }
    }
    return maxPrime;
}

// =========================================================================
// Main Runner
// =========================================================================

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cout << "P001: " << p001() << "\n";
    cout << "P002: " << p002() << "\n";
    cout << "P003: " << p003() << "\n";
    cout << "P004: " << p004() << "\n";
    cout << "P005: " << p005() << "\n";
    cout << "P006: " << p006() << "\n";
    cout << "P007: " << p007() << "\n";
    cout << "P008: " << p008() << "\n";
    cout << "P009: " << p009() << "\n";
    cout << "P010: " << p010() << "\n";
    cout << "P011: " << p011() << "\n";
    cout << "P012: " << p012() << "\n";
    cout << "P013: " << p013() << "\n";
    cout << "P014: " << p014() << "\n";
    cout << "P015: " << p015() << "\n";
    cout << "P016: " << p016() << "\n";
    cout << "P017: " << p017() << "\n";
    cout << "P018: " << p018() << "\n";
    cout << "P019: " << p019() << "\n";
    cout << "P020: " << p020() << "\n";
    cout << "P021: " << p021() << "\n";
    cout << "P022: " << p022() << "\n";
    cout << "P023: " << p023() << "\n";
    cout << "P024: " << p024() << "\n";
    cout << "P025: " << p025() << "\n";
    cout << "P026: " << p026() << "\n";
    cout << "P027: " << p027() << "\n";
    cout << "P028: " << p028() << "\n";
    cout << "P029: " << p029() << "\n";
    cout << "P030: " << p030() << "\n";
    cout << "P031: " << p031() << "\n";
    cout << "P032: " << p032() << "\n";
    cout << "P033: " << p033() << "\n";
    cout << "P034: " << p034() << "\n";
    cout << "P035: " << p035() << "\n";
    cout << "P036: " << p036() << "\n";
    cout << "P037: " << p037() << "\n";
    cout << "P038: " << p038() << "\n";
    cout << "P039: " << p039() << "\n";
    cout << "P040: " << p040() << "\n";
    cout << "P041: " << p041() << "\n";
    cout << "P042: " << p042() << "\n";
    cout << "P043: " << p043() << "\n";
    cout << "P044: " << p044() << "\n";
    cout << "P045: " << p045() << "\n";
    cout << "P046: " << p046() << "\n";
    cout << "P047: " << p047() << "\n";
    cout << "P048: " << p048() << "\n";
    cout << "P049: " << p049() << "\n";
    cout << "P050: " << p050() << "\n";

    return 0;
}