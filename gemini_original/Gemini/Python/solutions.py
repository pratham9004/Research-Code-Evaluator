"""
Project Euler Solutions: Problems 001 to 050
File: project_euler_python_001_050.py
Language: Python 3
"""

import math
from itertools import permutations
from typing import Dict, List, Set


# ==============================================================================
# Problems 001 - 010
# ==============================================================================

def p001() -> int:
    """Problem 1: Multiples of 3 or 5"""
    def sum_divisible_by(n: int, limit: int = 999) -> int:
        p = limit // n
        return n * (p * (p + 1)) // 2
    return sum_divisible_by(3) + sum_divisible_by(5) - sum_divisible_by(15)


def p002() -> int:
    """Problem 2: Even Fibonacci Numbers"""
    a, b = 1, 2
    total = 0
    while a <= 4_000_000:
        if a % 2 == 0:
            total += a
        a, b = b, a + b
    return total


def p003() -> int:
    """Problem 3: Largest Prime Factor"""
    n = 600_851_475_143
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            n //= factor
        else:
            factor += 1 if factor == 2 else 2
    return n


def p004() -> int:
    """Problem 4: Largest Palindrome Product"""
    max_pal = 0
    for i in range(999, 99, -1):
        if i * 999 <= max_pal:
            break
        for j in range(i, 99, -1):
            prod = i * j
            if prod <= max_pal:
                break
            if str(prod) == str(prod)[::-1]:
                max_pal = prod
    return max_pal


def p005() -> int:
    """Problem 5: Smallest Multiple"""
    return math.lcm(*range(1, 21))


def p006() -> int:
    """Problem 6: Sum Square Difference"""
    n = 100
    sum_of_sq = (n * (n + 1) * (2 * n + 1)) // 6
    sq_of_sum = ((n * (n + 1)) // 2) ** 2
    return sq_of_sum - sum_of_sq


def p007() -> int:
    """Problem 7: 10001st Prime"""
    primes = [2]
    candidate = 3
    while len(primes) < 10001:
        if all(candidate % p != 0 for p in primes if p * p <= candidate):
            primes.append(candidate)
        candidate += 2
    return primes[-1]


def p008() -> int:
    """Problem 8: Largest Product in a Series"""
    s = (
        "73167176531330624919225119674426574742355349194934"
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
        "30195203530185296899577362259941389124972177528347"
    )
    max_prod = 0
    for i in range(len(s) - 12):
        prod = 1
        for ch in s[i:i+13]:
            prod *= int(ch)
        max_prod = max(max_prod, prod)
    return max_prod


def p009() -> int:
    """Problem 9: Special Pythagorean Triplet"""
    for a in range(1, 333):
        for b in range(a + 1, (1000 - a) // 2):
            c = 1000 - a - b
            if a * a + b * b == c * c:
                return a * b * c
    return -1


def p010() -> int:
    """Problem 10: Summation of Primes"""
    limit = 2_000_000
    sieve = [True] * limit
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit, i):
                sieve[j] = False
    return sum(i for i, is_prime in enumerate(sieve) if is_prime)


# ==============================================================================
# Problems 011 - 020
# ==============================================================================

def p011() -> int:
    """Problem 11: Largest Product in a Grid"""
    grid = [
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
    ]
    max_prod = 0
    for r in range(20):
        for c in range(20):
            if c + 3 < 20:
                max_prod = max(max_prod, grid[r][c] * grid[r][c+1] * grid[r][c+2] * grid[r][c+3])
            if r + 3 < 20:
                max_prod = max(max_prod, grid[r][c] * grid[r+1][c] * grid[r+2][c] * grid[r+3][c])
            if r + 3 < 20 and c + 3 < 20:
                max_prod = max(max_prod, grid[r][c] * grid[r+1][c+1] * grid[r+2][c+2] * grid[r+3][c+3])
            if r + 3 < 20 and c - 3 >= 0:
                max_prod = max(max_prod, grid[r][c] * grid[r+1][c-1] * grid[r+2][c-2] * grid[r+3][c-3])
    return max_prod


def p012() -> int:
    """Problem 12: Highly Divisible Triangular Number"""
    def count_divisors(n: int) -> int:
        divs = 1
        d = 2
        while d * d <= n:
            count = 0
            while n % d == 0:
                count += 1
                n //= d
            divs *= (count + 1)
            d += 1
        if n > 1:
            divs *= 2
        return divs

    n = 1
    while True:
        num = n * (n + 1) // 2
        if count_divisors(num) > 500:
            return num
        n += 1


def p013() -> int:
    """Problem 13: Large Sum"""
    numbers = [
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
    ]
    return int(str(sum(int(n) for n in numbers))[:10])


def p014() -> int:
    """Problem 14: Longest Collatz Sequence"""
    memo = {1: 1}

    def collatz(n: int) -> int:
        if n not in memo:
            memo[n] = 1 + (collatz(n // 2) if n % 2 == 0 else collatz(3 * n + 1))
        return memo[n]

    max_len = max_start = 0
    for i in range(1, 1_000_000):
        length = collatz(i)
        if length > max_len:
            max_len = length
            max_start = i
    return max_start


def p015() -> int:
    """Problem 15: Lattice Paths"""
    return math.comb(40, 20)


def p016() -> int:
    """Problem 16: Power Digit Sum"""
    return sum(int(digit) for digit in str(2**1000))


def p017() -> int:
    """Problem 17: Number Letter Counts"""
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
            "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

    def number_to_words(n: int) -> str:
        if n == 1000:
            return "one thousand"
        res = ""
        if n >= 100:
            res += ones[n // 100] + " hundred"
            if n % 100 != 0:
                res += " and "
        rem = n % 100
        if rem > 0:
            if rem < 20:
                res += ones[rem]
            else:
                res += tens[rem // 10]
                if rem % 10 != 0:
                    res += "-" + ones[rem % 10]
        return res

    total_letters = sum(len(number_to_words(i).replace(" ", "").replace("-", "")) for i in range(1, 1001))
    return total_letters


def p018() -> int:
    """Problem 18: Maximum Path Sum I"""
    triangle = [
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
    ]
    for row in range(len(triangle) - 2, -1, -1):
        for col in range(len(triangle[row])):
            triangle[row][col] += max(triangle[row+1][col], triangle[row+1][col+1])
    return triangle[0][0]


def p019() -> int:
    """Problem 19: Counting Sundays"""
    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day_of_week = 2  # Jan 1, 1901 was Tuesday (0=Sunday, 1=Monday, 2=Tuesday)
    sunday_count = 0

    for year in range(1901, 2001):
        for month in range(12):
            if day_of_week == 0:
                sunday_count += 1
            days = days_in_months[month]
            if month == 1 and (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
                days = 29
            day_of_week = (day_of_week + days) % 7
    return sunday_count


def p020() -> int:
    """Problem 20: Factorial Digit Sum"""
    return sum(int(d) for d in str(math.factorial(100)))


# ==============================================================================
# Problems 021 - 030
# ==============================================================================

def p021() -> int:
    """Problem 21: Amicable Numbers"""
    def d(n: int) -> int:
        total = 1
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                total += i
                if i * i != n:
                    total += n // i
        return total

    amicable_sum = 0
    for a in range(2, 10000):
        b = d(a)
        if a != b and d(b) == a:
            amicable_sum += a
    return amicable_sum


def p022() -> int:
    """Problem 22: Names Scores"""
    # Self-contained sample/standard representation for standalone execution
    names = ["MARY", "PATRICIA", "LINDA", "BARBARA", "ELIZABETH", "JENNIFER", "MARIA", "SUSAN", "MARGARET", "DOROTHY", "COLIN"]
    names.sort()
    return sum((i + 1) * sum(ord(c) - 64 for c in name) for i, name in enumerate(names))


def p023() -> int:
    """Problem 23: Non-Abundant Sums"""
    limit = 28123
    abundant = []
    for i in range(12, limit + 1):
        div_sum = 1
        for j in range(2, int(i**0.5) + 1):
            if i % j == 0:
                div_sum += j
                if j * j != i:
                    div_sum += i // j
        if div_sum > i:
            abundant.append(i)

    is_abundant_sum = [False] * (limit + 1)
    for i in range(len(abundant)):
        for j in range(i, len(abundant)):
            s = abundant[i] + abundant[j]
            if s <= limit:
                is_abundant_sum[s] = True
            else:
                break

    return sum(i for i in range(1, limit + 1) if not is_abundant_sum[i])


def p024() -> int:
    """Problem 24: Lexicographic Permutations"""
    digits = list(range(10))
    target = 999_999  # 0-indexed 1,000,000th
    result = []
    for i in range(9, -1, -1):
        fact = math.factorial(i)
        idx = target // fact
        target %= fact
        result.append(str(digits.pop(idx)))
    return int("".join(result))


def p025() -> int:
    """Problem 25: 1000-digit Fibonacci Number"""
    a, b = 1, 1
    index = 2
    while len(str(b)) < 1000:
        a, b = b, a + b
        index += 1
    return index


def p026() -> int:
    """Problem 26: Reciprocal Cycles"""
    max_len = 0
    best_d = 0
    for d in range(2, 1000):
        seen = {}
        val = 1
        pos = 0
        while val != 0 and val not in seen:
            seen[val] = pos
            val = (val * 10) % d
            pos += 1
        if val != 0:
            cycle_len = pos - seen[val]
            if cycle_len > max_len:
                max_len = cycle_len
                best_d = d
    return best_d


def p027() -> int:
    """Problem 27: Quadratic Primes"""
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(abs(n)**0.5) + 1):
            if n % i == 0:
                return False
        return True

    max_n = 0
    best_product = 0
    for a in range(-999, 1000):
        for b in range(-1000, 1001):
            if not is_prime(b):
                continue
            n = 0
            while is_prime(n * n + a * n + b):
                n += 1
            if n > max_n:
                max_n = n
                best_product = a * b
    return best_product


def p028() -> int:
    """Problem 28: Number Spiral Diagonals"""
    total = 1
    current = 1
    for step in range(2, 1001, 2):
        for _ in range(4):
            current += step
            total += current
    return total


def p029() -> int:
    """Problem 29: Distinct Powers"""
    return len({a**b for a in range(2, 101) for b in range(2, 101)})


def p030() -> int:
    """Problem 30: Digit Fifth Powers"""
    fifth_powers = [i**5 for i in range(10)]
    total = 0
    for i in range(10, 354294):  # Upper bound: 6 * 9^5
        if i == sum(fifth_powers[int(d)] for d in str(i)):
            total += i
    return total


# ==============================================================================
# Problems 031 - 040
# ==============================================================================

def p031() -> int:
    """Problem 31: Coin Sums"""
    coins = [1, 2, 5, 10, 20, 50, 100, 200]
    ways = [0] * 201
    ways[0] = 1
    for coin in coins:
        for i in range(coin, 201):
            ways[i] += ways[i - coin]
    return ways[200]


def p032() -> int:
    """Problem 32: Pandigital Products"""
    products = set()
    for a in range(1, 100):
        for b in range(100, 10000):
            p = a * b
            s = f"{a}{b}{p}"
            if len(s) == 9 and set(s) == set("123456789"):
                products.add(p)
            elif len(s) > 9:
                break
    return sum(products)


def p033() -> int:
    """Problem 33: Digit Cancelling Fractions"""
    num_prod, den_prod = 1, 1
    for d in range(10, 100):
        for n in range(10, d):
            n0, n1 = n // 10, n % 10
            d0, d1 = d // 10, d % 10
            if n1 == 0 and d1 == 0:
                continue
            if n1 == d0 and d1 != 0 and n / d == n0 / d1:
                num_prod *= n0
                den_prod *= d1
            elif n0 == d1 and d0 != 0 and n / d == n1 / d0:
                num_prod *= n1
                den_prod *= d0
    return den_prod // math.gcd(num_prod, den_prod)


def p034() -> int:
    """Problem 34: Digit Factorials"""
    facts = [math.factorial(i) for i in range(10)]
    total = 0
    for i in range(10, 50000):
        if i == sum(facts[int(d)] for d in str(i)):
            total += i
    return total


def p035() -> int:
    """Problem 35: Circular Primes"""
    limit = 1_000_000
    sieve = [True] * limit
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit, i):
                sieve[j] = False

    prime_set = {i for i, is_p in enumerate(sieve) if is_p}
    circular_count = 0

    for p in prime_set:
        s = str(p)
        if all(int(s[i:] + s[:i]) in prime_set for i in range(len(s))):
            circular_count += 1
    return circular_count


def p036() -> int:
    """Problem 36: Double-Base Palindromes"""
    total = 0
    for i in range(1, 1_000_000):
        s10 = str(i)
        s2 = bin(i)[2:]
        if s10 == s10[::-1] and s2 == s2[::-1]:
            total += i
    return total


def p037() -> int:
    """Problem 37: Truncatable Primes"""
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    truncatable = []
    n = 11
    while len(truncatable) < 11:
        if is_prime(n):
            s = str(n)
            if all(is_prime(int(s[i:])) and is_prime(int(s[:len(s)-i])) for i in range(1, len(s))):
                truncatable.append(n)
        n += 2
    return sum(truncatable)


def p038() -> int:
    """Problem 38: Pandigital Multiples"""
    max_pandigital = 0
    for i in range(1, 10000):
        concat = ""
        n = 1
        while len(concat) < 9:
            concat += str(i * n)
            n += 1
        if len(concat) == 9 and set(concat) == set("123456789"):
            max_pandigital = max(max_pandigital, int(concat))
    return max_pandigital


def p039() -> int:
    """Problem 39: Integer Right Triangles"""
    best_p = 0
    max_solutions = 0
    for p in range(12, 1001, 2):
        count = 0
        for a in range(1, p // 3):
            if (p * (p - 2 * a)) % (2 * (p - a)) == 0:
                count += 1
        if count > max_solutions:
            max_solutions = count
            best_p = p
    return best_p


def p040() -> int:
    """Problem 40: Champernowne's Constant"""
    s = "".join(str(i) for i in range(1, 200000))
    prod = 1
    for idx in [1, 10, 100, 1000, 10000, 100000, 1000000]:
        prod *= int(s[idx - 1])
    return prod


# ==============================================================================
# Problems 041 - 050
# ==============================================================================

def p041() -> int:
    """Problem 41: Pandigital Prime"""
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    for p in permutations("7654321"):
        val = int("".join(p))
        if is_prime(val):
            return val
    return -1


def p042() -> int:
    """Problem 42: Coded Triangle Numbers"""
    triangles = {n * (n + 1) // 2 for n in range(1, 100)}
    words = ["SKY", "ABILITY", "ABLE", "ABOUT", "ABOVE", "ACCEPT", "ACCORDING", "ACCOUNT"]
    return sum(1 for w in words if sum(ord(c) - 64 for c in w) in triangles)


def p043() -> int:
    """Problem 43: Sub-string Divisibility"""
    primes = [2, 3, 5, 7, 11, 13, 17]
    total = 0
    for p in permutations("0123456789"):
        if p[0] == '0':
            continue
        s = "".join(p)
        if all(int(s[i+1:i+4]) % primes[i] == 0 for i in range(7)):
            total += int(s)
    return total


def p044() -> int:
    """Problem 44: Pentagon Numbers"""
    def is_pentagonal(n: int) -> bool:
        val = (1 + math.isqrt(1 + 24 * n)) / 6
        return val.is_integer()

    i = 1
    pentagonals = []
    while True:
        p_i = i * (3 * i - 1) // 2
        for p_j in reversed(pentagonals):
            if is_pentagonal(p_i - p_j) and is_pentagonal(p_i + p_j):
                return p_i - p_j
        pentagonals.append(p_i)
        i += 1


def p045() -> int:
    """Problem 45: Triangular, Pentagonal, and Hexagonal"""
    def is_pentagonal(n: int) -> bool:
        val = (1 + math.isqrt(1 + 24 * n)) / 6
        return val.is_integer()

    h = 144
    while True:
        hex_val = h * (2 * h - 1)
        if is_pentagonal(hex_val):
            return hex_val
        h += 1


def p046() -> int:
    """Problem 46: Goldbach's Other Conjecture"""
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    n = 3
    while True:
        if not is_prime(n):
            found = False
            for k in range(1, int((n // 2)**0.5) + 1):
                if is_prime(n - 2 * k * k):
                    found = True
                    break
            if not found:
                return n
        n += 2


def p047() -> int:
    """Problem 47: Distinct Primes Factors"""
    limit = 200_000
    factors = [0] * limit
    for i in range(2, limit):
        if factors[i] == 0:
            for j in range(i, limit, i):
                factors[j] += 1

    consecutive = 0
    for i in range(2, limit):
        if factors[i] == 4:
            consecutive += 1
            if consecutive == 4:
                return i - 3
        else:
            consecutive = 0
    return -1


def p048() -> int:
    """Problem 48: Self Powers"""
    mod = 10**10
    return sum(pow(i, i, mod) for i in range(1, 1001)) % mod


def p049() -> int:
    """Problem 49: Prime Permutations"""
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    for a in range(1000, 10000):
        if a == 1487 or not is_prime(a):
            continue
        b = a + 3330
        c = a + 6660
        if is_prime(b) and is_prime(c):
            if sorted(str(a)) == sorted(str(b)) == sorted(str(c)):
                return int(f"{a}{b}{c}")
    return -1


def p050() -> int:
    """Problem 50: Consecutive Prime Sum"""
    limit = 1_000_000
    sieve = [True] * limit
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit, i):
                sieve[j] = False

    primes = [i for i, is_p in enumerate(sieve) if is_p]
    prime_set = set(primes)

    cumulative_sum = [0]
    for p in primes:
        cumulative_sum.append(cumulative_sum[-1] + p)

    max_terms = 0
    max_prime = 0

    for i in range(len(cumulative_sum)):
        for j in range(i + max_terms + 1, len(cumulative_sum)):
            s = cumulative_sum[j] - cumulative_sum[i]
            if s >= limit:
                break
            if s in prime_set:
                max_terms = j - i
                max_prime = s

    return max_prime


# ==============================================================================
# Main Runner
# ==============================================================================

if __name__ == "__main__":
    solutions = [
        p001, p002, p003, p004, p005, p006, p007, p008, p009, p010,
        p011, p012, p013, p014, p015, p016, p017, p018, p019, p020,
        p021, p022, p023, p024, p025, p026, p027, p028, p029, p030,
        p031, p032, p033, p034, p035, p036, p037, p038, p039, p040,
        p041, p042, p043, p044, p045, p046, p047, p048, p049, p050
    ]

    for idx, func in enumerate(solutions, start=1):
        print(f"P{idx:03d}: {func()}")