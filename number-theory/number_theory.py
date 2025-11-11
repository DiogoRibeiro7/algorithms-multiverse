"""
Number Theory Algorithms - Basic and Intermediate
==================================================

A comprehensive collection of fundamental number theory algorithms with
mathematical proofs, performance optimizations, and cryptographic applications.

Author: algorithms-multiverse
Python Version: 3.7+
"""

import math
import random
from typing import List, Tuple, Optional, Set
from functools import reduce


def sieve_of_eratosthenes(limit: int) -> List[int]:
    """
    Generate all prime numbers up to limit using Sieve of Eratosthenes.

    Algorithm:
    1. Create a boolean array of size limit+1, initially all True
    2. Mark 0 and 1 as not prime
    3. For each number i from 2 to √limit:
       - If i is still marked prime, mark all multiples of i as composite
    4. Collect all numbers still marked as prime

    Mathematical Proof:
    - Any composite number n has a prime factor p ≤ √n
    - By marking multiples of all primes ≤ √limit, we identify all composites
    - Remaining unmarked numbers must be prime (by contradiction)

    Time Complexity: O(n log log n)
    Space Complexity: O(n)

    Optimization: We only check odd numbers after 2, reducing work by 50%.

    Args:
        limit: Upper bound for prime generation (inclusive)

    Returns:
        List of all prime numbers ≤ limit

    Example:
        >>> sieve_of_eratosthenes(30)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    """
    if limit < 2:
        return []

    # Initialize sieve: True means "potentially prime"
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    # Only need to check up to √limit
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            # Mark all multiples of i as composite
            # Start from i², as smaller multiples already marked
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    # Collect all prime numbers
    return [num for num in range(limit + 1) if is_prime[num]]


def sieve_of_sundaram(limit: int) -> List[int]:
    """
    Generate all prime numbers up to limit using Sieve of Sundaram.

    Algorithm:
    The Sieve of Sundaram generates odd primes by marking numbers of the form
    i + j + 2ij where 1 ≤ i ≤ j. The remaining unmarked numbers k yield primes 2k+1.

    Mathematical Foundation:
    - Every odd composite number can be written as (2i+1)(2j+1) = 2(i+j+2ij)+1
    - By marking all i+j+2ij values, we identify positions of odd composites
    - 2k+1 is prime if and only if k is unmarked

    Time Complexity: O(n log n)
    Space Complexity: O(n)

    Args:
        limit: Upper bound for prime generation (inclusive)

    Returns:
        List of all prime numbers ≤ limit

    Example:
        >>> sieve_of_sundaram(30)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    """
    if limit < 2:
        return []
    if limit == 2:
        return [2]

    # Calculate the limit for the sundaram sieve
    # We need n such that 2n+1 ≥ limit, so n = (limit-1)//2
    n = (limit - 1) // 2

    # Initialize array: True means "unmarked" (potentially prime)
    unmarked = [True] * (n + 1)

    # Mark positions i+j+2ij
    for i in range(1, n + 1):
        j = i
        while i + j + 2 * i * j <= n:
            unmarked[i + j + 2 * i * j] = False
            j += 1

    # Generate primes: 2k+1 for unmarked k
    primes = [2]  # 2 is the only even prime
    for k in range(1, n + 1):
        if unmarked[k]:
            prime = 2 * k + 1
            if prime <= limit:
                primes.append(prime)

    return primes


def prime_factorization(n: int) -> List[Tuple[int, int]]:
    """
    Find the prime factorization of n.

    Algorithm:
    1. Handle factor 2 separately (only even prime)
    2. Check odd divisors from 3 to √n
    3. If n > 1 after loop, n itself is a prime factor

    Returns factors as (prime, exponent) pairs.

    Mathematical Foundation:
    - Every integer n > 1 has a unique prime factorization (Fundamental Theorem)
    - Any factor p of n where p > √n must be paired with a factor q < √n
    - By checking up to √n, we find all factors

    Time Complexity: O(√n)
    Space Complexity: O(log n) for storing factors

    Args:
        n: Integer to factorize (n ≥ 2)

    Returns:
        List of (prime, exponent) tuples

    Example:
        >>> prime_factorization(60)
        [(2, 2), (3, 1), (5, 1)]  # 60 = 2² × 3¹ × 5¹
    """
    if n < 2:
        return []

    factors = []

    # Handle factor 2
    exponent = 0
    while n % 2 == 0:
        exponent += 1
        n //= 2
    if exponent > 0:
        factors.append((2, exponent))

    # Check odd divisors from 3 onwards
    divisor = 3
    while divisor * divisor <= n:
        exponent = 0
        while n % divisor == 0:
            exponent += 1
            n //= divisor
        if exponent > 0:
            factors.append((divisor, exponent))
        divisor += 2

    # If n > 1, then it's a prime factor
    if n > 1:
        factors.append((n, 1))

    return factors


def gcd(a: int, b: int) -> int:
    """
    Calculate the Greatest Common Divisor using Euclidean algorithm.

    Algorithm (Recursive formulation):
        gcd(a, b) = gcd(b, a mod b) if b ≠ 0
        gcd(a, 0) = a

    Mathematical Proof:
    - Let d = gcd(a, b)
    - Then d | a and d | b (d divides both)
    - Since a = bq + r where r = a mod b
    - Any divisor of b and r also divides a
    - Therefore gcd(a, b) = gcd(b, r)

    Time Complexity: O(log min(a, b))
    - Based on Lamé's theorem: number of steps ≤ 5 times the number of digits
    Space Complexity: O(1)

    Args:
        a, b: Non-negative integers

    Returns:
        Greatest common divisor of a and b

    Example:
        >>> gcd(48, 18)
        6
        >>> gcd(17, 19)
        1
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean Algorithm: Find gcd(a,b) and coefficients x, y such that:
        ax + by = gcd(a, b)

    These coefficients (x, y) are called Bézout coefficients.

    Algorithm:
    - Maintain invariant: a = old_r × old_s + old_t
    - Update coefficients along with remainders

    Applications:
    - Computing modular multiplicative inverse
    - Solving linear Diophantine equations
    - Chinese Remainder Theorem

    Time Complexity: O(log min(a, b))
    Space Complexity: O(1)

    Args:
        a, b: Integers

    Returns:
        Tuple (gcd, x, y) where gcd = ax + by

    Example:
        >>> extended_gcd(35, 15)
        (5, 1, -2)  # Because 35×1 + 15×(-2) = 5
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def lcm(a: int, b: int) -> int:
    """
    Calculate the Least Common Multiple.

    Mathematical Foundation:
        lcm(a, b) × gcd(a, b) = a × b

    Therefore:
        lcm(a, b) = (a × b) / gcd(a, b)

    Time Complexity: O(log min(a, b))
    Space Complexity: O(1)

    Args:
        a, b: Positive integers

    Returns:
        Least common multiple of a and b

    Example:
        >>> lcm(12, 18)
        36
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def mod_inverse(a: int, m: int) -> Optional[int]:
    """
    Calculate the modular multiplicative inverse of a modulo m.

    Find x such that: (a × x) ≡ 1 (mod m)

    Mathematical Foundation:
    - Inverse exists if and only if gcd(a, m) = 1 (a and m are coprime)
    - Using Extended Euclidean Algorithm: ax + my = 1
    - Therefore: ax ≡ 1 (mod m), so x is the inverse

    Applications:
    - RSA decryption
    - Solving modular equations
    - Finite field arithmetic

    Time Complexity: O(log m)
    Space Complexity: O(1)

    Args:
        a: Integer to find inverse of
        m: Modulus (must be > 1)

    Returns:
        Modular inverse of a mod m, or None if it doesn't exist

    Example:
        >>> mod_inverse(3, 11)
        4  # Because 3 × 4 = 12 ≡ 1 (mod 11)
    """
    g, x, _ = extended_gcd(a, m)

    if g != 1:
        # Inverse doesn't exist
        return None

    # Make sure result is positive
    return x % m


def mod_exp(base: int, exponent: int, modulus: int) -> int:
    """
    Fast modular exponentiation using binary exponentiation (exponentiation by squaring).

    Calculate: base^exponent mod modulus

    Algorithm (Right-to-left binary method):
    1. Express exponent in binary
    2. For each bit, square the current result
    3. If bit is 1, multiply by base

    Mathematical Foundation:
    - base^(2k) = (base^k)² - squaring reduces problem size by half
    - base^(2k+1) = base × (base^k)²
    - Taking mod at each step prevents integer overflow

    Example binary exponentiation:
        3^13 = 3^(1101₂) = 3^8 × 3^4 × 3^1

    Time Complexity: O(log exponent)
    Space Complexity: O(1)

    Applications:
    - RSA encryption/decryption: c = m^e mod n
    - Diffie-Hellman key exchange
    - Primality testing
    - Discrete logarithm problems

    Args:
        base: Base number
        exponent: Power to raise base to (non-negative)
        modulus: Modulus (must be > 0)

    Returns:
        base^exponent mod modulus

    Example:
        >>> mod_exp(2, 10, 1000)
        24  # 2^10 = 1024 ≡ 24 (mod 1000)
        >>> mod_exp(3, 1000, 13)
        3  # 3^1000 mod 13
    """
    if modulus == 1:
        return 0

    result = 1
    base = base % modulus

    while exponent > 0:
        # If exponent is odd, multiply base with result
        if exponent % 2 == 1:
            result = (result * base) % modulus

        # exponent must be even now
        exponent = exponent >> 1  # Divide by 2
        base = (base * base) % modulus

    return result


def chinese_remainder_theorem(remainders: List[int], moduli: List[int]) -> Optional[int]:
    """
    Solve system of congruences using Chinese Remainder Theorem.

    Given:
        x ≡ a₁ (mod m₁)
        x ≡ a₂ (mod m₂)
        ...
        x ≡ aₙ (mod mₙ)

    Find x that satisfies all congruences simultaneously.

    Mathematical Foundation:
    - Requires moduli to be pairwise coprime (gcd(mᵢ, mⱼ) = 1 for i ≠ j)
    - Solution exists and is unique modulo M = m₁ × m₂ × ... × mₙ
    - Construction: x = Σ(aᵢ × Mᵢ × yᵢ) mod M
      where Mᵢ = M/mᵢ and yᵢ = Mᵢ⁻¹ mod mᵢ

    Applications:
    - RSA with CRT speedup (4x faster decryption)
    - Calendar calculations
    - Solving systems of modular equations
    - Secret sharing schemes

    Time Complexity: O(n log M) where M is product of moduli
    Space Complexity: O(n)

    Args:
        remainders: List of remainders [a₁, a₂, ..., aₙ]
        moduli: List of moduli [m₁, m₂, ..., mₙ] (must be pairwise coprime)

    Returns:
        Solution x, or None if moduli are not coprime

    Example:
        >>> chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
        23  # x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7)
    """
    if len(remainders) != len(moduli):
        return None

    # Check if moduli are pairwise coprime
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            if gcd(moduli[i], moduli[j]) != 1:
                return None  # Not pairwise coprime

    # Calculate M = product of all moduli
    M = reduce(lambda x, y: x * y, moduli)

    # Calculate solution
    x = 0
    for i in range(len(moduli)):
        Mi = M // moduli[i]
        yi = mod_inverse(Mi, moduli[i])
        if yi is None:
            return None
        x += remainders[i] * Mi * yi

    return x % M


def is_prime_trial_division(n: int) -> bool:
    """
    Simple primality test using trial division.

    Check if n is divisible by any number from 2 to √n.

    Time Complexity: O(√n)
    Space Complexity: O(1)

    Args:
        n: Number to test

    Returns:
        True if n is prime, False otherwise

    Example:
        >>> is_prime_trial_division(17)
        True
        >>> is_prime_trial_division(15)
        False
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Check odd divisors from 3 to √n
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False

    return True


def totient(n: int) -> int:
    """
    Calculate Euler's totient function φ(n).

    φ(n) = count of integers k in range 1 ≤ k ≤ n where gcd(k, n) = 1

    Mathematical Formula:
    If n = p₁^a₁ × p₂^a₂ × ... × pₖ^aₖ, then:
        φ(n) = n × (1 - 1/p₁) × (1 - 1/p₂) × ... × (1 - 1/pₖ)

    Applications:
    - RSA: φ(n) used to calculate private key
    - Euler's theorem: a^φ(n) ≡ 1 (mod n) if gcd(a,n) = 1
    - Cyclic group theory

    Time Complexity: O(√n)
    Space Complexity: O(log n)

    Args:
        n: Positive integer

    Returns:
        Euler's totient of n

    Example:
        >>> totient(9)
        6  # 1,2,4,5,7,8 are coprime with 9
        >>> totient(36)
        12
    """
    if n == 1:
        return 1

    result = n
    factors = prime_factorization(n)

    for prime, _ in factors:
        # Multiply by (1 - 1/prime) = (prime - 1)/prime
        result = result * (prime - 1) // prime

    return result


def main():
    """Demonstration and testing of number theory algorithms."""
    print("=" * 60)
    print("NUMBER THEORY ALGORITHMS - DEMONSTRATION")
    print("=" * 60)

    # 1. Prime Generation
    print("\n1. PRIME NUMBER GENERATION")
    print("-" * 40)
    limit = 50
    primes_eratosthenes = sieve_of_eratosthenes(limit)
    primes_sundaram = sieve_of_sundaram(limit)
    print(f"Primes up to {limit} (Eratosthenes): {primes_eratosthenes}")
    print(f"Primes up to {limit} (Sundaram):     {primes_sundaram}")
    print(f"Verification: Both methods agree: {primes_eratosthenes == primes_sundaram}")

    # 2. Prime Factorization
    print("\n2. PRIME FACTORIZATION")
    print("-" * 40)
    numbers = [60, 128, 1001, 2024]
    for n in numbers:
        factors = prime_factorization(n)
        factors_str = " * ".join([f"{p}^{e}" if e > 1 else str(p) for p, e in factors])
        print(f"{n} = {factors_str}")

    # 3. GCD and LCM
    print("\n3. GCD AND LCM")
    print("-" * 40)
    pairs = [(48, 18), (100, 35), (17, 19)]
    for a, b in pairs:
        g = gcd(a, b)
        l = lcm(a, b)
        print(f"gcd({a}, {b}) = {g}, lcm({a}, {b}) = {l}")

    # 4. Extended GCD
    print("\n4. EXTENDED GCD (Bezout's Identity)")
    print("-" * 40)
    pairs = [(35, 15), (240, 46)]
    for a, b in pairs:
        g, x, y = extended_gcd(a, b)
        print(f"{a}*{x} + {b}*{y} = {g}")
        print(f"Verification: {a*x + b*y} = {g}")

    # 5. Modular Inverse
    print("\n5. MODULAR MULTIPLICATIVE INVERSE")
    print("-" * 40)
    test_cases = [(3, 11), (7, 26), (4, 6)]
    for a, m in test_cases:
        inv = mod_inverse(a, m)
        if inv:
            print(f"Inverse of {a} mod {m} = {inv}")
            print(f"Verification: ({a} * {inv}) mod {m} = {(a * inv) % m}")
        else:
            print(f"Inverse of {a} mod {m} does not exist (not coprime)")

    # 6. Modular Exponentiation
    print("\n6. MODULAR EXPONENTIATION")
    print("-" * 40)
    test_cases = [(2, 10, 1000), (3, 100, 13), (7, 256, 100)]
    for base, exp, mod in test_cases:
        result = mod_exp(base, exp, mod)
        print(f"{base}^{exp} mod {mod} = {result}")

    # 7. Chinese Remainder Theorem
    print("\n7. CHINESE REMAINDER THEOREM")
    print("-" * 40)
    remainders = [2, 3, 2]
    moduli = [3, 5, 7]
    solution = chinese_remainder_theorem(remainders, moduli)
    print(f"System of congruences:")
    for a, m in zip(remainders, moduli):
        print(f"  x == {a} (mod {m})")
    print(f"Solution: x = {solution}")
    print(f"Verification:")
    for a, m in zip(remainders, moduli):
        print(f"  {solution} mod {m} = {solution % m} (expected {a})")

    # 8. Euler's Totient
    print("\n8. EULER'S TOTIENT FUNCTION")
    print("-" * 40)
    test_values = [1, 9, 10, 36, 100]
    for n in test_values:
        phi = totient(n)
        print(f"phi({n}) = {phi}")

    # 9. Performance Comparison
    print("\n9. PERFORMANCE NOTES")
    print("-" * 40)
    print("Algorithm complexities:")
    print("  - Sieve of Eratosthenes: O(n log log n)")
    print("  - Prime Factorization:   O(sqrt(n))")
    print("  - GCD (Euclidean):       O(log min(a,b))")
    print("  - Modular Exponentiation: O(log exponent)")
    print("  - Chinese Remainder:     O(n log M)")
    print("  - Euler's Totient:       O(sqrt(n))")

    print("\n" + "=" * 60)
    print("All basic algorithms demonstrated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
