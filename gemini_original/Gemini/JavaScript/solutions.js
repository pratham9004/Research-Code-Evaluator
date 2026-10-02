// =========================================================================
// Big Integer & Math Helpers
// =========================================================================

function isPrime(n) {
    if (n < 2) return false;
    if (n === 2 || n === 3) return true;
    if (n % 2 === 0 || n % 3 === 0) return false;
    for (let i = 5; i * i <= n; i += 6) {
        if (n % i === 0 || n % (i + 2) === 0) return false;
    }
    return true;
}

function sumProperDivisors(n) {
    if (n <= 1) return 0;
    let total = 1;
    for (let i = 2; i * i <= n; i++) {
        if (n % i === 0) {
            total += i;
            if (i * i !== n) total += n / i;
        }
    }
    return total;
}

function isPandigital1To9(str) {
    if (str.length !== 9) return false;
    return str.split('').sort().join('') === '123456789';
}

function gcd(a, b) {
    while (b) {
        let t = b;
        b = a % b;
        a = t;
    }
    return a;
}

// =========================================================================
// Problems 001 - 010
// =========================================================================

function p001() {
    const sumDiv = (n, limit) => {
        const p = Math.floor(limit / n);
        return n * Math.floor((p * (p + 1)) / 2);
    };
    return sumDiv(3, 999) + sumDiv(5, 999) - sumDiv(15, 999);
}

function p002() {
    let a = 1, b = 2, total = 0;
    while (a <= 4000000) {
        if (a % 2 === 0) total += a;
        [a, b] = [b, a + b];
    }
    return total;
}

function p003() {
    let n = 600851475143;
    let factor = 2;
    while (factor * factor <= n) {
        if (n % factor === 0) n /= factor;
        else factor += factor === 2 ? 1 : 2;
    }
    return n;
}

function p004() {
    let maxPal = 0;
    for (let i = 999; i >= 100; i--) {
        if (i * 999 <= maxPal) break;
        for (let j = i; j >= 100; j--) {
            let prod = i * j;
            if (prod <= maxPal) break;
            let s = String(prod);
            if (s === s.split('').reverse().join('')) maxPal = prod;
        }
    }
    return maxPal;
}

function p005() {
    let lcmVal = 1;
    for (let i = 1; i <= 20; i++) {
        lcmVal = (lcmVal * i) / gcd(lcmVal, i);
    }
    return lcmVal;
}

function p006() {
    const n = 100;
    const sumSq = Math.floor((n * (n + 1) * (2 * n + 1)) / 6);
    const sqSum = Math.floor((n * (n + 1)) / 2);
    return sqSum * sqSum - sumSq;
}

function p007() {
    const primes = [2];
    let candidate = 3;
    while (primes.length < 10001) {
        let isP = true;
        for (let p of primes) {
            if (p * p > candidate) break;
            if (candidate % p === 0) { isP = false; break; }
        }
        if (isP) primes.push(candidate);
        candidate += 2;
    }
    return primes[primes.length - 1];
}

function p008() {
    const s = "73167176531330624919225119674426574742355349194934" +
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
    let maxP = 0;
    for (let i = 0; i <= s.length - 13; i++) {
        let prod = 1;
        for (let j = i; j < i + 13; j++) prod *= Number(s[j]);
        if (prod > maxP) maxP = prod;
    }
    return maxP;
}

function p009() {
    for (let a = 1; a < 333; a++) {
        for (let b = a + 1; b < Math.floor((1000 - a) / 2); b++) {
            let c = 1000 - a - b;
            if (a * a + b * b === c * c) return a * b * c;
        }
    }
    return -1;
}

function p010() {
    const limit = 2000000;
    const isP = new Uint8Array(limit).fill(1);
    isP[0] = isP[1] = 0;
    for (let i = 2; i * i < limit; i++) {
        if (isP[i]) {
            for (let j = i * i; j < limit; j += i) isP[j] = 0;
        }
    }
    let sum = 0;
    for (let i = 0; i < limit; i++) if (isP[i]) sum += i;
    return sum;
}

// =========================================================================
// Problems 011 - 020
// =========================================================================

function p011() {
    const grid = [
        [8, 2, 22, 97, 38, 15, 0, 40, 0, 75, 4, 5, 7, 78, 52, 12, 50, 77, 91, 8],
        [49, 49, 99, 40, 17, 81, 18, 57, 60, 87, 17, 40, 98, 43, 69, 48, 4, 56, 62, 0],
        [81, 49, 31, 73, 55, 79, 14, 29, 93, 71, 40, 67, 53, 88, 30, 3, 49, 13, 36, 65],
        [52, 70, 95, 23, 4, 60, 11, 42, 69, 24, 68, 56, 1, 32, 56, 71, 37, 2, 36, 91],
        [22, 31, 16, 71, 51, 67, 63, 89, 41, 92, 36, 54, 22, 40, 40, 28, 66, 33, 13, 80],
        [24, 47, 32, 60, 99, 3, 45, 2, 44, 75, 30, 53, 45, 29, 2, 96, 2, 27, 2, 65],
        [1, 52, 86, 43, 84, 68, 52, 82, 86, 70, 77, 91, 85, 78, 50, 85, 31, 30, 46, 39],
        [11, 70, 69, 7, 36, 21, 41, 15, 81, 56, 0, 5, 35, 6, 62, 0, 80, 44, 5, 40],
        [22, 31, 16, 23, 19, 72, 63, 23, 4, 21, 33, 18, 57, 42, 16, 7, 0, 38, 45, 7],
        [66, 28, 80, 70, 93, 28, 0, 58, 22, 7, 37, 71, 65, 9, 53, 54, 89, 29, 44, 47],
        [43, 31, 33, 21, 30, 81, 51, 54, 38, 97, 66, 24, 25, 33, 35, 24, 27, 72, 88, 34],
        [8, 24, 71, 29, 51, 61, 42, 37, 21, 35, 85, 1, 54, 22, 12, 41, 41, 31, 18, 46],
        [38, 32, 39, 15, 24, 15, 72, 40, 14, 67, 48, 28, 51, 45, 85, 8, 4, 8, 12, 70],
        [71, 43, 6, 8, 20, 72, 0, 23, 33, 7, 53, 69, 28, 8, 85, 97, 51, 17, 33, 81],
        [17, 6, 24, 82, 36, 11, 54, 1, 44, 15, 45, 68, 23, 4, 27, 2, 0, 98, 30, 69],
        [4, 4, 52, 8, 2, 52, 64, 93, 12, 82, 17, 85, 42, 62, 45, 19, 56, 65, 9, 39],
        [50, 41, 92, 69, 39, 76, 96, 62, 84, 6, 83, 31, 3, 83, 19, 24, 23, 66, 62, 18],
        [0, 86, 2, 0, 31, 8, 56, 2, 7, 12, 37, 25, 72, 8, 49, 17, 4, 18, 14, 7],
        [4, 14, 84, 7, 29, 78, 11, 84, 30, 73, 31, 82, 83, 24, 19, 37, 84, 2, 40, 29],
        [10, 2, 33, 15, 65, 6, 24, 40, 86, 92, 14, 52, 27, 69, 23, 0, 39, 40, 42, 12]
    ];

    let maxP = 0;
    for (let r = 0; r < 20; r++) {
        for (let c = 0; c < 20; c++) {
            if (c + 3 < 20) {
                let p = grid[r][c] * grid[r][c+1] * grid[r][c+2] * grid[r][c+3];
                if (p > maxP) maxP = p;
            }
            if (r + 3 < 20) {
                let p = grid[r][c] * grid[r+1][c] * grid[r+2][c] * grid[r+3][c];
                if (p > maxP) maxP = p;
            }
            if (r + 3 < 20 && c + 3 < 20) {
                let p = grid[r][c] * grid[r+1][c+1] * grid[r+2][c+2] * grid[r+3][c+3];
                if (p > maxP) maxP = p;
            }
            if (r + 3 < 20 && c - 3 >= 0) {
                let p = grid[r][c] * grid[r+1][c-1] * grid[r+2][c-2] * grid[r+3][c-3];
                if (p > maxP) maxP = p;
            }
        }
    }
    return maxP;
}

function p012() {
    const countDivs = (n) => {
        let divs = 1, d = 2;
        while (d * d <= n) {
            let count = 0;
            while (n % d === 0) { count++; n /= d; }
            divs *= (count + 1);
            d++;
        }
        if (n > 1) divs *= 2;
        return divs;
    };

    let n = 1;
    while (true) {
        let tri = (n * (n + 1)) / 2;
        if (countDivs(tri) > 500) return tri;
        n++;
    }
}

function p013() {
    const numbers = [
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
    ];
    let sum = numbers.reduce((acc, x) => acc + BigInt(x), 0n);
    return sum.toString().slice(0, 10);
}

function p014() {
    const memo = new Map();
    memo.set(1, 1);

    const getCollatz = (n) => {
        if (memo.has(n)) return memo.get(n);
        let next = n % 2 === 0 ? n / 2 : 3 * n + 1;
        let len = 1 + getCollatz(next);
        if (n < 2000000) memo.set(n, len);
        return len;
    };

    let maxLen = 0, maxStart = 0;
    for (let i = 1; i < 1000000; i++) {
        let len = getCollatz(i);
        if (len > maxLen) {
            maxLen = len;
            maxStart = i;
        }
    }
    return maxStart;
}

function p015() {
    let res = 1n;
    for (let i = 1n; i <= 20n; i++) {
        res = (res * (40n - i + 1n)) / i;
    }
    return res.toString();
}

function p016() {
    let val = 2n ** 1000n;
    return val.toString().split('').reduce((a, b) => a + Number(b), 0);
}

function p017() {
    const ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
                  "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
                  "seventeen", "eighteen", "nineteen"];
    const tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"];

    let totalLetters = 0;
    for (let i = 1; i <= 1000; i++) {
        let word = "";
        if (i === 1000) {
            word = "onethousand";
        } else {
            if (i >= 100) {
                word += ones[Math.floor(i / 100)] + "hundred";
                if (i % 100 !== 0) word += "and";
            }
            let rem = i % 100;
            if (rem > 0) {
                if (rem < 20) word += ones[rem];
                else {
                    word += tens[Math.floor(rem / 10)];
                    if (rem % 10 !== 0) word += ones[rem % 10];
                }
            }
        }
        totalLetters += word.length;
    }
    return totalLetters;
}

function p018() {
    const triangle = [
        [75],
        [95, 64],
        [17, 47, 82],
        [18, 35, 87, 10],
        [20, 4, 82, 47, 65],
        [19, 1, 23, 75, 3, 34],
        [88, 2, 77, 73, 7, 63, 67],
        [99, 65, 4, 28, 6, 16, 70, 92],
        [41, 41, 26, 56, 83, 40, 80, 70, 33],
        [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
        [53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14],
        [70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57],
        [91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48],
        [63, 66, 4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31],
        [4, 62, 98, 27, 23, 9, 70, 98, 73, 93, 38, 53, 60, 4, 23]
    ];

    for (let r = triangle.length - 2; r >= 0; r--) {
        for (let c = 0; c < triangle[r].length; c++) {
            triangle[r][c] += Math.max(triangle[r+1][c], triangle[r+1][c+1]);
        }
    }
    return triangle[0][0];
}

function p019() {
    let sundayCount = 0;
    for (let year = 1901; year <= 2000; year++) {
        for (let month = 0; month < 12; month++) {
            if (new Date(year, month, 1).getDay() === 0) sundayCount++;
        }
    }
    return sundayCount;
}

function p020() {
    let fact = 1n;
    for (let i = 1n; i <= 100n; i++) fact *= i;
    return fact.toString().split('').reduce((a, b) => a + Number(b), 0);
}

// =========================================================================
// Problems 021 - 030
// =========================================================================

function p021() {
    let amicableSum = 0;
    for (let a = 2; a < 10000; a++) {
        let b = sumProperDivisors(a);
        if (a !== b && sumProperDivisors(b) === a) amicableSum += a;
    }
    return amicableSum;
}

function p022() {
    const names = ["MARY", "PATRICIA", "LINDA", "BARBARA", "ELIZABETH", "JENNIFER", "MARIA", "SUSAN", "MARGARET", "DOROTHY", "COLIN"].sort();
    let totalScore = 0;
    for (let i = 0; i < names.length; i++) {
        let wordVal = 0;
        for (let c of names[i]) wordVal += c.charCodeAt(0) - 64;
        totalScore += (i + 1) * wordVal;
    }
    return totalScore;
}

function p023() {
    const limit = 28123;
    const abundants = [];
    for (let i = 12; i <= limit; i++) {
        if (sumProperDivisors(i) > i) abundants.push(i);
    }

    const isAbundantSum = new Uint8Array(limit + 1);
    for (let i = 0; i < abundants.length; i++) {
        for (let j = i; j < abundants.length; j++) {
            let s = abundants[i] + abundants[j];
            if (s <= limit) isAbundantSum[s] = 1;
            else break;
        }
    }

    let nonAbundantSum = 0;
    for (let i = 1; i <= limit; i++) {
        if (!isAbundantSum[i]) nonAbundantSum += i;
    }
    return nonAbundantSum;
}

function p024() {
    let digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
    let k = 999999;
    let facts = [362880, 40320, 5040, 720, 120, 24, 6, 2, 1, 1];
    let result = "";

    for (let f of facts) {
        let idx = Math.floor(k / f);
        result += digits[idx];
        digits.splice(idx, 1);
        k %= f;
    }
    return result;
}

function p025() {
    let a = 1n, b = 1n;
    let index = 2;
    while (b.toString().length < 1000) {
        [a, b] = [b, a + b];
        index++;
    }
    return index;
}

function p026() {
    let maxLen = 0, bestD = 0;
    for (let d = 2; d < 1000; d++) {
        const seen = new Map();
        let val = 1, pos = 0;
        while (val !== 0 && !seen.has(val)) {
            seen.set(val, pos++);
            val = (val * 10) % d;
        }
        if (val !== 0) {
            let cycleLen = pos - seen.get(val);
            if (cycleLen > maxLen) {
                maxLen = cycleLen;
                bestD = d;
            }
        }
    }
    return bestD;
}

function p027() {
    let maxN = 0, bestProd = 0;
    for (let a = -999; a < 1000; a++) {
        for (let b = -1000; b <= 1000; b++) {
            if (!isPrime(Math.abs(b))) continue;
            let n = 0;
            while (isPrime(n * n + a * n + b)) n++;
            if (n > maxN) {
                maxN = n;
                bestProd = a * b;
            }
        }
    }
    return bestProd;
}

function p028() {
    let total = 1, current = 1;
    for (let step = 2; step <= 1000; step += 2) {
        for (let i = 0; i < 4; i++) {
            current += step;
            total += current;
        }
    }
    return total;
}

function p029() {
    const powers = new Set();
    for (let a = 2n; a <= 100n; a++) {
        for (let b = 2n; b <= 100n; b++) {
            powers.add(a ** b);
        }
    }
    return powers.size;
}

function p030() {
    let total = 0;
    const fifthPowers = Array.from({ length: 10 }, (_, i) => Math.pow(i, 5));

    for (let i = 10; i <= 354294; i++) {
        let sum = 0, temp = i;
        while (temp > 0) {
            sum += fifthPowers[temp % 10];
            temp = Math.floor(temp / 10);
        }
        if (sum === i) total += i;
    }
    return total;
}

// =========================================================================
// Problems 031 - 040
// =========================================================================

function p031() {
    const coins = [1, 2, 5, 10, 20, 50, 100, 200];
    const ways = new Array(201).fill(0);
    ways[0] = 1;

    for (let coin of coins) {
        for (let i = coin; i <= 200; i++) {
            ways[i] += ways[i - coin];
        }
    }
    return ways[200];
}

function p032() {
    const products = new Set();
    for (let a = 1; a < 100; a++) {
        for (let b = 100; b < 10000; b++) {
            let p = a * b;
            let s = `${a}${b}${p}`;
            if (s.length === 9 && isPandigital1To9(s)) products.add(p);
            else if (s.length > 9) break;
        }
    }
    let sum = 0;
    for (let p of products) sum += p;
    return sum;
}

function p033() {
    let numProd = 1, denProd = 1;
    for (let d = 10; d < 100; d++) {
        for (let n = 10; n < d; n++) {
            let n0 = Math.floor(n / 10), n1 = n % 10;
            let d0 = Math.floor(d / 10), d1 = d % 10;
            if (n1 === 0 && d1 === 0) continue;

            if (n1 === d0 && d1 !== 0 && n / d === n0 / d1) {
                numProd *= n0; denProd *= d1;
            } else if (n0 === d1 && d0 !== 0 && n / d === n1 / d0) {
                numProd *= n1; denProd *= d0;
            }
        }
    }
    return denProd / gcd(numProd, denProd);
}

function p034() {
    const facts = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880];
    let total = 0;
    for (let i = 10; i < 50000; i++) {
        let sum = 0, temp = i;
        while (temp > 0) {
            sum += facts[temp % 10];
            temp = Math.floor(temp / 10);
        }
        if (sum === i) total += i;
    }
    return total;
}

function p035() {
    const limit = 1000000;
    const isP = new Uint8Array(limit).fill(1);
    isP[0] = isP[1] = 0;
    for (let i = 2; i * i < limit; i++) {
        if (isP[i]) {
            for (let j = i * i; j < limit; j += i) isP[j] = 0;
        }
    }

    let count = 0;
    for (let i = 2; i < limit; i++) {
        if (isP[i]) {
            let s = String(i);
            let isCirc = true;
            for (let j = 0; j < s.length; j++) {
                let rot = s.slice(j) + s.slice(0, j);
                if (!isP[Number(rot)]) { isCirc = false; break; }
            }
            if (isCirc) count++;
        }
    }
    return count;
}

function p036() {
    let total = 0;
    for (let i = 1; i < 1000000; i++) {
        let s10 = i.toString(10);
        if (s10 === s10.split('').reverse().join('')) {
            let s2 = i.toString(2);
            if (s2 === s2.split('').reverse().join('')) total += i;
        }
    }
    return total;
}

function p037() {
    let count = 0, sum = 0, n = 11;
    while (count < 11) {
        if (isPrime(n)) {
            let s = String(n);
            let truncatable = true;
            for (let i = 1; i < s.length; i++) {
                let left = Number(s.slice(i));
                let right = Number(s.slice(0, s.length - i));
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

function p038() {
    let maxPandigital = 0;
    for (let i = 1; i < 10000; i++) {
        let concat = "";
        let n = 1;
        while (concat.length < 9) {
            concat += (i * n);
            n++;
        }
        if (concat.length === 9 && isPandigital1To9(concat)) {
            maxPandigital = Math.max(maxPandigital, Number(concat));
        }
    }
    return maxPandigital;
}

function p039() {
    let bestP = 0, maxSolutions = 0;
    for (let p = 12; p <= 1000; p += 2) {
        let count = 0;
        for (let a = 1; a < p / 3; a++) {
            if ((p * (p - 2 * a)) % (2 * (p - a)) === 0) count++;
        }
        if (count > maxSolutions) {
            maxSolutions = count;
            bestP = p;
        }
    }
    return bestP;
}

function p040() {
    let s = "";
    for (let i = 1; s.length < 1000005; i++) s += i;
    const indices = [1, 10, 100, 1000, 10000, 100000, 1000000];
    let prod = 1;
    for (let idx of indices) prod *= Number(s[idx - 1]);
    return prod;
}

// =========================================================================
// Problems 041 - 050
// =========================================================================

function p041() {
    function getPermutations(str) {
        if (str.length <= 1) return [str];
        let perms = [];
        for (let i = 0; i < str.length; i++) {
            let char = str[i];
            let remainingChars = str.slice(0, i) + str.slice(i + 1);
            for (let perm of getPermutations(remainingChars)) {
                perms.push(char + perm);
            }
        }
        return perms;
    }

    const perms = getPermutations("7654321").map(Number);
    for (let val of perms) {
        if (isPrime(val)) return val;
    }
    return -1;
}

function p042() {
    const triangles = new Set();
    for (let n = 1; n < 100; n++) triangles.add((n * (n + 1)) / 2);
    const words = ["SKY", "ABILITY", "ABLE", "ABOUT", "ABOVE", "ACCEPT", "ACCORDING", "ACCOUNT"];
    let count = 0;
    for (let w of words) {
        let score = 0;
        for (let c of w) score += c.charCodeAt(0) - 64;
        if (triangles.has(score)) count++;
    }
    return count;
}

function p043() {
    const primes = [2, 3, 5, 7, 11, 13, 17];
    let sum = 0;

    function search(s, used) {
        if (s.length === 10) {
            sum += Number(s);
            return;
        }
        let idx = s.length - 3;
        for (let d = 0; d <= 9; d++) {
            if (!used[d]) {
                if (s.length >= 3) {
                    let sub = Number(s.slice(idx) + d);
                    if (sub % primes[idx - 1] !== 0) continue;
                }
                used[d] = true;
                search(s + d, used);
                used[d] = false;
            }
        }
    }

    search("", new Array(10).fill(false));
    return sum;
}

function p044() {
    const isPentagonal = (n) => {
        let val = (1 + Math.sqrt(1 + 24 * n)) / 6;
        return Number.isInteger(val);
    };

    const pentagonals = [];
    let i = 1;
    while (true) {
        let pI = (i * (3 * i - 1)) / 2;
        for (let j = pentagonals.length - 1; j >= 0; j--) {
            let pJ = pentagonals[j];
            if (isPentagonal(pI - pJ) && isPentagonal(pI + pJ)) {
                return pI - pJ;
            }
        }
        pentagonals.push(pI);
        i++;
    }
}

function p045() {
    const isPentagonal = (n) => {
        let val = (1 + Math.sqrt(1 + 24 * n)) / 6;
        return Number.isInteger(val);
    };

    let h = 144;
    while (true) {
        let hexVal = h * (2 * h - 1);
        if (isPentagonal(hexVal)) return hexVal;
        h++;
    }
}

function p046() {
    let n = 3;
    while (true) {
        if (!isPrime(n)) {
            let found = false;
            for (let k = 1; 2 * k * k < n; k++) {
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

function p047() {
    const limit = 200000;
    const factors = new Uint8Array(limit);

    for (let i = 2; i < limit; i++) {
        if (factors[i] === 0) {
            for (let j = i; j < limit; j += i) factors[j]++;
        }
    }

    let consecutive = 0;
    for (let i = 2; i < limit; i++) {
        if (factors[i] === 4) {
            consecutive++;
            if (consecutive === 4) return i - 3;
        } else {
            consecutive = 0;
        }
    }
    return -1;
}

function p048() {
    let total = 0n;
    const mod = 10000000000n;
    for (let i = 1n; i <= 1000n; i++) {
        total = (total + (i ** i)) % mod;
    }
    return total.toString();
}

function p049() {
    const isPerm = (a, b) => {
        return String(a).split('').sort().join('') === String(b).split('').sort().join('');
    };

    for (let a = 1000; a < 10000; a++) {
        if (a === 1487 || !isPrime(a)) continue;
        let b = a + 3330;
        let c = a + 6660;
        if (isPrime(b) && isPrime(c)) {
            if (isPerm(a, b) && isPerm(a, c)) {
                return `${a}${b}${c}`;
            }
        }
    }
    return "";
}

function p050() {
    const limit = 1000000;
    const isP = new Uint8Array(limit).fill(1);
    isP[0] = isP[1] = 0;
    for (let i = 2; i * i < limit; i++) {
        if (isP[i]) {
            for (let j = i * i; j < limit; j += i) isP[j] = 0;
        }
    }

    const primes = [];
    const primeSet = new Set();
    for (let i = 0; i < limit; i++) {
        if (isP[i]) {
            primes.push(i);
            primeSet.add(i);
        }
    }

    const cumSum = new Array(primes.length + 1).fill(0);
    for (let i = 0; i < primes.length; i++) {
        cumSum[i + 1] = cumSum[i] + primes[i];
    }

    let maxTerms = 0;
    let maxPrime = 0;

    for (let i = 0; i < cumSum.length; i++) {
        for (let j = i + maxTerms + 1; j < cumSum.length; j++) {
            let sum = cumSum[j] - cumSum[i];
            if (sum >= limit) break;
            if (primeSet.has(sum)) {
                maxTerms = j - i;
                maxPrime = sum;
            }
        }
    }
    return maxPrime;
}

// =========================================================================
// Main Runner
// =========================================================================

function main() {
    console.log("P001:", p001());
    console.log("P002:", p002());
    console.log("P003:", p003());
    console.log("P004:", p004());
    console.log("P005:", p005());
    console.log("P006:", p006());
    console.log("P007:", p007());
    console.log("P008:", p008());
    console.log("P009:", p009());
    console.log("P010:", p010());
    console.log("P011:", p011());
    console.log("P012:", p012());
    console.log("P013:", p013());
    console.log("P014:", p014());
    console.log("P015:", p015());
    console.log("P016:", p016());
    console.log("P017:", p017());
    console.log("P018:", p018());
    console.log("P019:", p019());
    console.log("P020:", p020());
    console.log("P021:", p021());
    console.log("P022:", p022());
    console.log("P023:", p023());
    console.log("P024:", p024());
    console.log("P025:", p025());
    console.log("P026:", p026());
    console.log("P027:", p027());
    console.log("P028:", p028());
    console.log("P029:", p029());
    console.log("P030:", p030());
    console.log("P031:", p031());
    console.log("P032:", p032());
    console.log("P033:", p033());
    console.log("P034:", p034());
    console.log("P035:", p035());
    console.log("P036:", p036());
    console.log("P037:", p037());
    console.log("P038:", p038());
    console.log("P039:", p039());
    console.log("P040:", p040());
    console.log("P041:", p041());
    console.log("P042:", p042());
    console.log("P043:", p043());
    console.log("P044:", p044());
    console.log("P045:", p045());
    console.log("P046:", p046());
    console.log("P047:", p047());
    console.log("P048:", p048());
    console.log("P049:", p049());
    console.log("P050:", p050());
}

main();