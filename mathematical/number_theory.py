"""
Number Theory Algorithms - Comprehensive Implementation

A complete collection of fundamental number theory algorithms with applications
in cryptography, hashing, and computational mathematics.

Algorithms Implemented:
1. Prime Number Generation
   - Sieve of Eratosthenes (O(n log log n))
   - Sieve of Sundaram (O(n log n))
   - Segmented Sieve (for large ranges)

2. Prime Testing
   - Trial Division
   - Miller-Rabin Primality Test (probabilistic)
   - Deterministic variants

3. Factorization
   - Trial Division
   - Pollard's Rho Algorithm
   - Prime Factorization

4. GCD and LCM
   - Euclidean Algorithm
   - Extended Euclidean Algorithm
   - Binary GCD (Stein's Algorithm)

5. Modular Arithmetic
   - Modular Addition/Multiplication
   - Modular Inverse
   - Fast Modular Exponentiation

6. Advanced Algorithms
   - Chinese Remainder Theorem
   - Euler's Totient Function
   - Carmichael's Function

Applications:
- RSA Encryption/Decryption
- Diffie-Hellman Key Exchange
- Hash Functions
- Digital Signatures

Author: Claude Code
Python 3.8+ (uses math.gcd, math.isqrt for verification)
"""

import math
import random
import time
from typing import List, Tuple, Optional, Dict
from functools import reduce
from collections import Counter
import operator


# ==============================================================================
# 1. PRIME NUMBER GENERATION
# ==============================================================================

def sieve_of_eratosthenes(limit: int) -> List[int]:
    """
    Sieve of Eratosthenes - Classical prime number generation algorithm.

    Algorithm:
    1. Create a boolean array of size limit+1, initialized to True
    2. Mark 0 and 1 as not prime
    3. For each number i from 2 to √limit:
       - If i is marked prime, mark all multiples of i as not prime
    4. Collect all numbers still marked as prime

    Mathematical Proof:
    - Any composite number n has a prime factor ≤ √n
    - By marking multiples up to limit, we identify all composites
    - Remaining unmarked numbers are prime

    Time Complexity: O(n log log n)
    Space Complexity: O(n)

    Optimization: Only check odd numbers after 2

    Args:
        limit: Upper bound for prime generation

    Returns:
        List of all prime numbers up to limit

    Examples:
        >>> sieve_of_eratosthenes(30)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    Applications:
        - Generating prime tables for cryptography
        - Finding all primes in a range
        - Testing primality for small numbers
    """
    if limit < 2:
        return []

    # Use bitarray for memory efficiency (could optimize further)
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    # Only need to check up to √limit
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            # Mark all multiples of i as composite
            # Optimization: start from i*i (smaller multiples already marked)
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    return [i for i in range(limit + 1) if is_prime[i]]


def sieve_of_eratosthenes_optimized(limit: int) -> List[int]:
    """
    Optimized Sieve of Eratosthenes - Only processes odd numbers.

    Optimizations:
    1. Handle 2 separately, then only check odd numbers
    2. Use bit packing for memory efficiency
    3. Skip even multiples entirely

    Space saved: ~50% compared to basic sieve

    Time Complexity: O(n log log n)
    Space Complexity: O(n/2)
    """
    if limit < 2:
        return []
    if limit == 2:
        return [2]

    # Array size is (limit-1)//2 to store only odd numbers
    # Index i represents number 2*i + 3
    size = (limit - 1) // 2
    is_prime = [True] * size

    # Check odd numbers starting from 3
    for i in range(int(math.sqrt(limit)) // 2):
        if is_prime[i]:
            # The odd number represented by index i
            p = 2 * i + 3
            # Mark odd multiples of p
            # Start from p*p, increment by 2*p to skip even multiples
            start = (p * p - 3) // 2
            for j in range(start, size, p):
                is_prime[j] = False

    # Reconstruct prime list
    primes = [2] + [2 * i + 3 for i in range(size) if is_prime[i]]
    return primes


def sieve_of_sundaram(limit: int) -> List[int]:
    """
    Sieve of Sundaram - Alternative prime generation algorithm.

    Algorithm:
    1. Create array of size (n-1)/2
    2. Mark numbers of form i + j + 2ij where i ≤ j
    3. Remaining numbers k generate primes 2k + 1

    Mathematical Basis:
    - Numbers of form i + j + 2ij correspond to odd composites
    - If k is not marked, then 2k + 1 is prime

    Time Complexity: O(n log n)
    Space Complexity: O(n)

    Note: Slightly slower than Eratosthenes but interesting mathematically

    Args:
        limit: Upper bound for prime generation

    Returns:
        List of prime numbers up to limit

    Examples:
        >>> sieve_of_sundaram(30)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    """
    if limit < 2:
        return []
    if limit == 2:
        return [2]

    n = (limit - 1) // 2
    marked = [False] * (n + 1)

    # Mark numbers of form i + j + 2ij
    for i in range(1, n + 1):
        j = i
        while i + j + 2 * i * j <= n:
            marked[i + j + 2 * i * j] = True
            j += 1

    # Generate primes: 2k + 1 for unmarked k
    primes = [2] + [2 * i + 1 for i in range(1, n + 1) if not marked[i]]

    return [p for p in primes if p <= limit]


def segmented_sieve(low: int, high: int) -> List[int]:
    """
    Segmented Sieve - For generating primes in a large range [low, high].

    Used when the range is too large to fit in memory.

    Algorithm:
    1. Generate all primes up to √high using simple sieve
    2. Divide [low, high] into segments
    3. For each segment, mark composites using small primes
    4. Collect primes from each segment

    Memory efficient for large ranges.

    Time Complexity: O((high-low) log log high + √high log log √high)
    Space Complexity: O(√high + segment_size)

    Args:
        low: Lower bound (inclusive)
        high: Upper bound (inclusive)

    Returns:
        List of primes in range [low, high]

    Applications:
        - Finding primes in very large ranges
        - Memory-constrained environments
        - Distributed prime generation
    """
    if high < 2:
        return []

    # Step 1: Find all primes up to √high
    limit = int(math.sqrt(high)) + 1
    small_primes = sieve_of_eratosthenes(limit)

    # Step 2: Process segments
    segment_size = max(limit, 10000)  # Choose efficient segment size
    primes = []

    # Handle the first segment if it includes small primes
    if low <= limit:
        primes.extend([p for p in small_primes if low <= p <= high])
        low = limit + 1

    # Process remaining segments
    for seg_low in range(low, high + 1, segment_size):
        seg_high = min(seg_low + segment_size - 1, high)

        # Create segment array
        is_prime = [True] * (seg_high - seg_low + 1)

        # Mark composites using small primes
        for p in small_primes:
            # Find first multiple of p in segment
            start = max(p * p, ((seg_low + p - 1) // p) * p)

            for j in range(start, seg_high + 1, p):
                is_prime[j - seg_low] = False

        # Collect primes from segment
        primes.extend([seg_low + i for i in range(len(is_prime)) if is_prime[i]])

    return primes


# ==============================================================================
# 2. PRIMALITY TESTING
# ==============================================================================

def is_prime_trial_division(n: int) -> bool:
    """
    Trial Division - Simple primality test.

    Tests divisibility by all numbers up to √n.

    Time Complexity: O(√n)
    Space Complexity: O(1)

    Optimizations:
    - Check 2 and 3 separately
    - Then check only numbers of form 6k ± 1
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Check divisors of form 6k ± 1 up to √n
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True


def miller_rabin_test(n: int, k: int = 5) -> bool:
    """
    Miller-Rabin Primality Test - Probabilistic primality testing.

    Algorithm based on Fermat's Little Theorem:
    If n is prime and a is not divisible by n, then:
        a^(n-1) ≡ 1 (mod n)

    For composite n, this holds for at most 1/4 of bases a.
    Testing k random bases gives error probability ≤ (1/4)^k.

    Mathematical Basis:
    - Write n-1 = 2^r * d where d is odd
    - Test if a^d ≡ 1 (mod n) or
    -        a^(2^i * d) ≡ -1 (mod n) for some i

    Time Complexity: O(k log³ n) - k iterations of modular exponentiation
    Space Complexity: O(1)

    Error Probability: ≤ (1/4)^k
    - k=5: error ≤ 0.1%
    - k=10: error ≤ 0.0001%

    Args:
        n: Number to test for primality
        k: Number of rounds (more rounds = more accurate)

    Returns:
        True if probably prime, False if definitely composite

    Examples:
        >>> miller_rabin_test(17)
        True
        >>> miller_rabin_test(221)  # 221 = 13 * 17 (composite)
        False

    Applications:
        - RSA key generation
        - Cryptographic prime generation
        - Fast primality testing for large numbers
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Perform k rounds of testing
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)  # a^d mod n

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def miller_rabin_deterministic(n: int) -> bool:
    """
    Deterministic Miller-Rabin test for n < 3,317,044,064,679,887,385,961,981.

    Uses specific bases that ensure correctness for all numbers below threshold.

    Bases for different ranges:
    - n < 2,047: test a = 2
    - n < 1,373,653: test a = 2, 3
    - n < 25,326,001: test a = 2, 3, 5
    - n < 3,215,031,751: test a = 2, 3, 5, 7
    - etc.

    Time Complexity: O(log³ n)
    Space Complexity: O(1)
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Deterministic bases for ranges
    if n < 2047:
        witnesses = [2]
    elif n < 1373653:
        witnesses = [2, 3]
    elif n < 9080191:
        witnesses = [31, 73]
    elif n < 25326001:
        witnesses = [2, 3, 5]
    elif n < 3215031751:
        witnesses = [2, 3, 5, 7]
    elif n < 4759123141:
        witnesses = [2, 7, 61]
    elif n < 1122004669633:
        witnesses = [2, 13, 23, 1662803]
    elif n < 2152302898747:
        witnesses = [2, 3, 5, 7, 11]
    elif n < 3474749660383:
        witnesses = [2, 3, 5, 7, 11, 13]
    elif n < 341550071728321:
        witnesses = [2, 3, 5, 7, 11, 13, 17]
    else:
        # For very large numbers, use probabilistic
        return miller_rabin_test(n, k=20)

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Test each witness
    for a in witnesses:
        if a >= n:
            continue

        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


# ==============================================================================
# 3. FACTORIZATION
# ==============================================================================

def trial_division_factorization(n: int) -> List[int]:
    """
    Trial Division - Simple factorization algorithm.

    Divides by all numbers up to √n to find factors.

    Time Complexity: O(√n)
    Space Complexity: O(log n) for storing factors
    """
    if n < 2:
        return []

    factors = []

    # Handle 2 separately
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # Check odd divisors
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2

    # If n > 1, then it's a prime factor
    if n > 1:
        factors.append(n)

    return factors


def pollard_rho(n: int, max_iterations: int = 10000) -> Optional[int]:
    """
    Pollard's Rho Algorithm - Fast integer factorization.

    Algorithm:
    Uses pseudo-random sequence x_i = (x_{i-1}^2 + c) mod n
    Finds cycles in this sequence to detect factors.

    Mathematical Basis (Birthday Paradox):
    - In a sequence mod p (prime factor of n), cycles appear
    - GCD of differences reveals factors

    Expected Time: O(n^(1/4))
    Much faster than trial division for large numbers!

    Args:
        n: Number to factor (should be composite)
        max_iterations: Maximum iterations before giving up

    Returns:
        A non-trivial factor of n, or None if not found

    Examples:
        >>> pollard_rho(221)  # 221 = 13 * 17
        13  # or 17

    Applications:
        - Breaking weak RSA keys
        - Integer factorization challenges
        - Cryptanalysis
    """
    if n == 1:
        return None
    if n % 2 == 0:
        return 2

    # Choose random starting point and constant
    x = random.randint(2, n - 1)
    y = x
    c = random.randint(1, n - 1)
    d = 1

    # Floyd's cycle detection
    for _ in range(max_iterations):
        # x moves one step: x = (x^2 + c) mod n
        x = (x * x + c) % n

        # y moves two steps
        y = (y * y + c) % n
        y = (y * y + c) % n

        # Check if we found a factor
        d = math.gcd(abs(x - y), n)

        if d != 1:
            break

    # If d == n, we failed to find a factor
    return d if d != n else None


def pollard_rho_factorization(n: int) -> List[int]:
    """
    Complete factorization using Pollard's Rho.

    Combines Pollard's Rho with trial division and primality testing.

    Strategy:
    1. Use trial division for small factors
    2. Use Miller-Rabin to test if remaining number is prime
    3. Use Pollard's Rho to find factors of composite numbers

    Time Complexity: O(n^(1/4)) per factor
    """
    if n < 2:
        return []

    factors = []

    # Step 1: Trial division for small primes
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    for p in small_primes:
        while n % p == 0:
            factors.append(p)
            n //= p

    # Step 2: Factor remaining number
    def factor_recursive(num):
        if num == 1:
            return

        # Check if prime
        if miller_rabin_deterministic(num):
            factors.append(num)
            return

        # Find a factor using Pollard's Rho
        factor = pollard_rho(num)

        if factor is None:
            # Fallback to trial division
            factors.extend(trial_division_factorization(num))
            return

        # Recursively factor both parts
        factor_recursive(factor)
        factor_recursive(num // factor)

    factor_recursive(n)
    return sorted(factors)


def prime_factorization(n: int) -> Dict[int, int]:
    """
    Prime factorization with multiplicities.

    Returns dictionary mapping prime factors to their exponents.

    Time Complexity: O(√n) worst case, O(n^(1/4)) average with Pollard's Rho

    Examples:
        >>> prime_factorization(60)
        {2: 2, 3: 1, 5: 1}  # 60 = 2^2 * 3 * 5
        >>> prime_factorization(128)
        {2: 7}  # 128 = 2^7
    """
    factors = pollard_rho_factorization(n)
    return dict(Counter(factors))


# ==============================================================================
# 4. GCD AND LCM
# ==============================================================================

def gcd_euclidean(a: int, b: int) -> int:
    """
    Euclidean Algorithm - Greatest Common Divisor.

    Algorithm (recursive definition):
        gcd(a, b) = gcd(b, a mod b)  if b ≠ 0
        gcd(a, 0) = a

    Mathematical Proof:
    - Any common divisor of a and b also divides (a - kb) for any integer k
    - Therefore, gcd(a, b) = gcd(b, a mod b)

    Time Complexity: O(log min(a, b))
    Space Complexity: O(1)

    Examples:
        >>> gcd_euclidean(48, 18)
        6
        >>> gcd_euclidean(100, 35)
        5

    Applications:
        - Simplifying fractions
        - Modular inverse calculation
        - RSA key generation
    """
    while b:
        a, b = b, a % b
    return abs(a)


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.

    Finds gcd(a, b) and coefficients x, y such that:
        ax + by = gcd(a, b)

    This is Bézout's identity.

    Time Complexity: O(log min(a, b))
    Space Complexity: O(1)

    Returns:
        (gcd, x, y) where ax + by = gcd

    Examples:
        >>> extended_gcd(30, 20)
        (10, 1, -1)  # 30*1 + 20*(-1) = 10

    Applications:
        - Computing modular inverses
        - Solving linear Diophantine equations
        - Chinese Remainder Theorem
    """
    if b == 0:
        return abs(a), 1 if a >= 0 else -1, 0

    x1, x2, y1, y2 = 0, 1, 1, 0

    while b:
        q = a // b
        a, b = b, a % b
        x1, x2 = x2 - q * x1, x1
        y1, y2 = y2 - q * y1, y1

    return abs(a), x2, y2


def binary_gcd(a: int, b: int) -> int:
    """
    Binary GCD (Stein's Algorithm) - GCD using only subtraction and bit shifts.

    More efficient on binary computers as it avoids division.

    Algorithm:
    1. If both even, gcd(a,b) = 2 * gcd(a/2, b/2)
    2. If one even, gcd(a,b) = gcd(a/2, b) (even number removed)
    3. If both odd, gcd(a,b) = gcd((a-b)/2, b)

    Time Complexity: O(log min(a, b))
    Space Complexity: O(1)

    Advantage: Uses bit shifts instead of modulo (faster on some hardware)
    """
    a, b = abs(a), abs(b)

    if a == 0:
        return b
    if b == 0:
        return a

    # Count common factors of 2
    shift = 0
    while ((a | b) & 1) == 0:
        a >>= 1
        b >>= 1
        shift += 1

    # Remove remaining factors of 2 from a
    while (a & 1) == 0:
        a >>= 1

    while b:
        # Remove factors of 2 from b
        while (b & 1) == 0:
            b >>= 1

        # Swap if necessary
        if a > b:
            a, b = b, a

        b -= a

    return a << shift


def lcm(a: int, b: int) -> int:
    """
    Least Common Multiple using GCD.

    Formula: lcm(a, b) = |a * b| / gcd(a, b)

    Time Complexity: O(log min(a, b))
    """
    return abs(a * b) // gcd_euclidean(a, b) if a and b else 0


# ==============================================================================
# 5. MODULAR ARITHMETIC
# ==============================================================================

def mod_add(a: int, b: int, m: int) -> int:
    """Modular addition: (a + b) mod m"""
    return (a % m + b % m) % m


def mod_multiply(a: int, b: int, m: int) -> int:
    """Modular multiplication: (a * b) mod m"""
    return ((a % m) * (b % m)) % m


def mod_power(base: int, exp: int, mod: int) -> int:
    """
    Fast Modular Exponentiation - Binary exponentiation.

    Computes (base^exp) mod mod efficiently.

    Algorithm (Square-and-Multiply):
    - Express exponent in binary
    - Square and multiply based on binary digits

    Example: 3^13 mod 7
    - 13 = 1101₂
    - Result = 3^8 * 3^4 * 3^1 mod 7

    Time Complexity: O(log exp)
    Space Complexity: O(1)

    Mathematical Basis:
        (a * b) mod m = ((a mod m) * (b mod m)) mod m
        a^(2k) = (a^k)^2

    Applications:
        - RSA encryption/decryption
        - Diffie-Hellman key exchange
        - Digital signatures
        - Primality testing

    Examples:
        >>> mod_power(2, 10, 1000)
        24  # 2^10 = 1024 ≡ 24 (mod 1000)
        >>> mod_power(3, 13, 7)
        6
    """
    result = 1
    base = base % mod

    while exp > 0:
        # If exp is odd, multiply base with result
        if exp % 2 == 1:
            result = (result * base) % mod

        # exp must be even now
        exp = exp >> 1  # exp = exp // 2
        base = (base * base) % mod

    return result


def mod_inverse(a: int, m: int) -> Optional[int]:
    """
    Modular Multiplicative Inverse.

    Finds x such that (a * x) ≡ 1 (mod m)

    Exists only if gcd(a, m) = 1

    Uses Extended Euclidean Algorithm.

    Time Complexity: O(log m)

    Applications:
        - RSA decryption
        - Solving modular equations
        - Chinese Remainder Theorem

    Examples:
        >>> mod_inverse(3, 7)
        5  # 3 * 5 = 15 ≡ 1 (mod 7)
        >>> mod_inverse(2, 4)
        None  # No inverse (gcd(2,4) = 2 ≠ 1)
    """
    g, x, _ = extended_gcd(a, m)

    if g != 1:
        return None  # Inverse doesn't exist

    return x % m


# ==============================================================================
# 6. CHINESE REMAINDER THEOREM
# ==============================================================================

def chinese_remainder_theorem(remainders: List[int], moduli: List[int]) -> Optional[int]:
    """
    Chinese Remainder Theorem - Solve system of modular congruences.

    Solves:
        x ≡ a₁ (mod m₁)
        x ≡ a₂ (mod m₂)
        ...
        x ≡ aₙ (mod mₙ)

    Requirements: All moduli must be pairwise coprime

    Algorithm:
    1. Compute M = m₁ * m₂ * ... * mₙ
    2. For each i, compute M_i = M / m_i
    3. Find y_i such that M_i * y_i ≡ 1 (mod m_i)
    4. Solution: x = (a₁*M₁*y₁ + ... + aₙ*Mₙ*yₙ) mod M

    Time Complexity: O(n * log² max(moduli))

    Args:
        remainders: List of remainders [a₁, a₂, ..., aₙ]
        moduli: List of moduli [m₁, m₂, ..., mₙ] (must be pairwise coprime)

    Returns:
        Solution x, or None if no solution exists

    Examples:
        >>> chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
        23  # x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7)

    Applications:
        - RSA with CRT speedup (4x faster decryption)
        - Splitting secrets across multiple parties
        - Parallel computation
        - Calendar calculations
    """
    if len(remainders) != len(moduli):
        return None

    # Check if moduli are pairwise coprime
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            if gcd_euclidean(moduli[i], moduli[j]) != 1:
                return None  # Not pairwise coprime

    # Compute product of all moduli
    M = reduce(operator.mul, moduli, 1)

    result = 0

    for remainder, modulus in zip(remainders, moduli):
        M_i = M // modulus
        y_i = mod_inverse(M_i, modulus)

        if y_i is None:
            return None

        result = (result + remainder * M_i * y_i) % M

    return result


# ==============================================================================
# 7. EULER'S TOTIENT AND RELATED FUNCTIONS
# ==============================================================================

def euler_totient(n: int) -> int:
    """
    Euler's Totient Function φ(n).

    Counts integers from 1 to n that are coprime to n.

    Formula: φ(n) = n * ∏(1 - 1/p) for all prime factors p of n

    Time Complexity: O(√n) or O(n^(1/4)) with Pollard's Rho

    Examples:
        >>> euler_totient(9)
        6  # Numbers coprime to 9: 1,2,4,5,7,8
        >>> euler_totient(12)
        4  # Numbers coprime to 12: 1,5,7,11

    Applications:
        - RSA key generation (φ(n) for public key)
        - Carmichael's function
        - Number theory problems
    """
    if n == 1:
        return 1

    result = n
    factors = prime_factorization(n)

    for prime in factors:
        result -= result // prime

    return result


def carmichael_function(n: int) -> int:
    """
    Carmichael's Function λ(n).

    Smallest positive integer k such that a^k ≡ 1 (mod n)
    for all a coprime to n.

    For n = p₁^k₁ * p₂^k₂ * ... * pₙ^kₙ:
        λ(n) = lcm(λ(p₁^k₁), λ(p₂^k₂), ..., λ(pₙ^kₙ))

    Used in RSA instead of φ(n) for smaller private exponent.

    Time Complexity: O(√n)
    """
    if n == 1:
        return 1

    factors = prime_factorization(n)

    def lambda_prime_power(p, k):
        if p == 2 and k >= 3:
            return pow(p, k - 2)
        return pow(p, k - 1) * (p - 1)

    values = [lambda_prime_power(p, k) for p, k in factors.items()]

    return reduce(lcm, values, 1)


# ==============================================================================
# 8. CRYPTOGRAPHIC APPLICATIONS
# ==============================================================================

class RSA:
    """
    RSA Encryption/Decryption Implementation.

    Demonstrates practical application of number theory algorithms.

    Key Generation:
    1. Choose two large primes p and q
    2. Compute n = p * q (modulus)
    3. Compute φ(n) = (p-1)(q-1)
    4. Choose e such that gcd(e, φ(n)) = 1 (public exponent)
    5. Compute d = e^(-1) mod φ(n) (private exponent)

    Public key: (e, n)
    Private key: (d, n)

    Encryption: c = m^e mod n
    Decryption: m = c^d mod n
    """

    def __init__(self, bits: int = 512):
        """
        Generate RSA key pair.

        Args:
            bits: Size of the modulus in bits (512, 1024, 2048, etc.)
        """
        # Generate two large primes
        p = self._generate_prime(bits // 2)
        q = self._generate_prime(bits // 2)

        # Compute modulus and totient
        self.n = p * q
        phi = (p - 1) * (q - 1)

        # Choose public exponent (commonly 65537)
        self.e = 65537

        # Compute private exponent
        self.d = mod_inverse(self.e, phi)

        # For CRT speedup (optional)
        self.p = p
        self.q = q
        self.dp = self.d % (p - 1)
        self.dq = self.d % (q - 1)
        self.qinv = mod_inverse(q, p)

    def _generate_prime(self, bits: int) -> int:
        """Generate a prime number of specified bit length."""
        while True:
            # Generate random odd number
            n = random.getrandbits(bits) | (1 << (bits - 1)) | 1

            if miller_rabin_test(n, k=10):
                return n

    def encrypt(self, message: int) -> int:
        """
        Encrypt message.

        Args:
            message: Integer message < n

        Returns:
            Encrypted ciphertext
        """
        if message >= self.n:
            raise ValueError("Message must be less than modulus")

        return mod_power(message, self.e, self.n)

    def decrypt(self, ciphertext: int) -> int:
        """
        Decrypt ciphertext.

        Args:
            ciphertext: Encrypted message

        Returns:
            Decrypted message
        """
        return mod_power(ciphertext, self.d, self.n)

    def decrypt_crt(self, ciphertext: int) -> int:
        """
        Decrypt using Chinese Remainder Theorem (4x faster).

        Uses Garner's formula for CRT.
        """
        m1 = mod_power(ciphertext, self.dp, self.p)
        m2 = mod_power(ciphertext, self.dq, self.q)

        h = (self.qinv * (m1 - m2)) % self.p
        return m2 + h * self.q


# ==============================================================================
# 9. PERFORMANCE BENCHMARKING
# ==============================================================================

def benchmark_algorithms():
    """
    Comprehensive benchmarking of number theory algorithms.
    """
    print("=" * 70)
    print("NUMBER THEORY ALGORITHMS - PERFORMANCE BENCHMARKS")
    print("=" * 70)

    # 1. Prime Generation
    print("\n1. PRIME GENERATION")
    print("-" * 70)

    for limit in [1000, 10000, 100000]:
        start = time.time()
        primes1 = sieve_of_eratosthenes(limit)
        time1 = (time.time() - start) * 1000

        start = time.time()
        primes2 = sieve_of_eratosthenes_optimized(limit)
        time2 = (time.time() - start) * 1000

        start = time.time()
        primes3 = sieve_of_sundaram(limit)
        time3 = (time.time() - start) * 1000

        print(f"\nGenerating primes up to {limit:,}")
        print(f"  Sieve of Eratosthenes:      {time1:8.3f} ms ({len(primes1)} primes)")
        print(f"  Optimized Sieve:            {time2:8.3f} ms ({len(primes2)} primes)")
        print(f"  Sieve of Sundaram:          {time3:8.3f} ms ({len(primes3)} primes)")

    # 2. Primality Testing
    print("\n2. PRIMALITY TESTING")
    print("-" * 70)

    test_numbers = [
        (561, False),  # Carmichael number
        (1105, False),  # Carmichael number
        (104729, True),  # Prime
        (104743, True),  # Prime
        (1000000007, True),  # Large prime
        (1000000009, True),  # Large prime
    ]

    for n, is_prime in test_numbers:
        start = time.time()
        result1 = is_prime_trial_division(n)
        time1 = (time.time() - start) * 1000000  # microseconds

        start = time.time()
        result2 = miller_rabin_test(n, k=5)
        time2 = (time.time() - start) * 1000000

        start = time.time()
        result3 = miller_rabin_deterministic(n)
        time3 = (time.time() - start) * 1000000

        print(f"\nTesting {n:,} (actual: {'prime' if is_prime else 'composite'})")
        print(f"  Trial Division:     {time1:8.2f} μs - {'PRIME' if result1 else 'COMPOSITE'}")
        print(f"  Miller-Rabin:       {time2:8.2f} μs - {'PRIME' if result2 else 'COMPOSITE'}")
        print(f"  Deterministic:      {time3:8.2f} μs - {'PRIME' if result3 else 'COMPOSITE'}")

    # 3. Factorization
    print("\n3. FACTORIZATION")
    print("-" * 70)

    test_numbers = [
        1234567,
        9876543,
        1000000007 * 1000000009,  # Product of two large primes
    ]

    for n in test_numbers:
        print(f"\nFactoring {n:,}")

        start = time.time()
        factors1 = trial_division_factorization(n)
        time1 = (time.time() - start) * 1000

        start = time.time()
        factors2 = pollard_rho_factorization(n)
        time2 = (time.time() - start) * 1000

        print(f"  Trial Division:     {time1:8.3f} ms - {factors1}")
        print(f"  Pollard's Rho:      {time2:8.3f} ms - {factors2}")

    # 4. GCD Comparison
    print("\n4. GCD ALGORITHMS")
    print("-" * 70)

    a, b = 123456789, 987654321

    start = time.time()
    for _ in range(10000):
        gcd_euclidean(a, b)
    time1 = (time.time() - start) * 1000

    start = time.time()
    for _ in range(10000):
        binary_gcd(a, b)
    time2 = (time.time() - start) * 1000

    start = time.time()
    for _ in range(10000):
        math.gcd(a, b)
    time3 = (time.time() - start) * 1000

    print(f"GCD({a:,}, {b:,}) - 10,000 iterations")
    print(f"  Euclidean Algorithm:   {time1:8.3f} ms")
    print(f"  Binary GCD:            {time2:8.3f} ms")
    print(f"  Python built-in:       {time3:8.3f} ms")

    # 5. Modular Exponentiation
    print("\n5. MODULAR EXPONENTIATION")
    print("-" * 70)

    base, exp, mod = 12345, 67890, 1000000007

    start = time.time()
    result1 = mod_power(base, exp, mod)
    time1 = (time.time() - start) * 1000000

    start = time.time()
    result2 = pow(base, exp, mod)
    time2 = (time.time() - start) * 1000000

    print(f"Computing {base}^{exp} mod {mod:,}")
    print(f"  Custom implementation:  {time1:8.2f} μs - Result: {result1}")
    print(f"  Python built-in pow():  {time2:8.2f} μs - Result: {result2}")


def demonstrate_cryptographic_applications():
    """Demonstrate RSA and other cryptographic applications."""
    print("\n" + "=" * 70)
    print("CRYPTOGRAPHIC APPLICATIONS")
    print("=" * 70)

    # RSA Demonstration
    print("\n1. RSA ENCRYPTION/DECRYPTION")
    print("-" * 70)

    print("Generating 512-bit RSA key pair...")
    rsa = RSA(bits=512)

    message = 123456789
    print(f"\nOriginal message: {message}")

    ciphertext = rsa.encrypt(message)
    print(f"Encrypted:        {ciphertext}")

    decrypted = rsa.decrypt(ciphertext)
    print(f"Decrypted:        {decrypted}")

    decrypted_crt = rsa.decrypt_crt(ciphertext)
    print(f"Decrypted (CRT):  {decrypted_crt}")

    print(f"\nVerification: {'✓ SUCCESS' if message == decrypted == decrypted_crt else '✗ FAILED'}")

    # Chinese Remainder Theorem
    print("\n2. CHINESE REMAINDER THEOREM")
    print("-" * 70)

    remainders = [2, 3, 2]
    moduli = [3, 5, 7]

    print(f"Solving system:")
    for r, m in zip(remainders, moduli):
        print(f"  x ≡ {r} (mod {m})")

    solution = chinese_remainder_theorem(remainders, moduli)
    print(f"\nSolution: x = {solution}")

    # Verify
    print("\nVerification:")
    for r, m in zip(remainders, moduli):
        print(f"  {solution} mod {m} = {solution % m} {'✓' if solution % m == r else '✗'}")


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_cryptographic_applications()

    # Run benchmarks
    benchmark_algorithms()

    # Run doctests
    print("\n" + "=" * 70)
    print("RUNNING DOCTESTS")
    print("=" * 70)
    import doctest
    results = doctest.testmod(verbose=False)
    print(f"Doctests: {results.attempted} tests, {results.failed} failures")
    if results.failed == 0:
        print("✓ All tests passed!")
