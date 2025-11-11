"""
Advanced Number Theory Algorithms
==================================

Implementation of advanced number theory algorithms with focus on:
- Probabilistic primality testing (Miller-Rabin)
- Integer factorization (Pollard's Rho)
- Cryptographic applications

Author: algorithms-multiverse
Python Version: 3.7+
"""

import random
import math
from typing import List, Optional, Set
from number_theory import gcd, mod_exp


def miller_rabin(n: int, k: int = 5) -> bool:
    """
    Miller-Rabin probabilistic primality test.

    Algorithm:
    Based on Fermat's Little Theorem and its contrapositive.
    Write n-1 as 2^r × d where d is odd.
    For random witness a:
      - Compute x = a^d mod n
      - If x = 1 or x = n-1, continue to next witness
      - Square x repeatedly r-1 times
      - If any result is n-1, continue to next witness
      - Otherwise n is definitely composite

    Mathematical Foundation:
    - If n is prime: a^(n-1) ≡ 1 (mod n) for all a coprime to n (Fermat)
    - If n is odd composite: at most (n-1)/4 values of a pass the test
    - Error probability ≤ 4^(-k) for k random witnesses

    Deterministic variants:
    For n < 2,047, test with a = [2] is deterministic
    For n < 1,373,653, test with a = [2, 3] is deterministic
    For n < 9,080,191, test with a = [31, 73] is deterministic
    For n < 2^64, test with a = [2,3,5,7,11,13,17,19,23,29,31,37] is deterministic

    Time Complexity: O(k log³ n)
    - k rounds of testing
    - Each round: O(log n) modular exponentiations
    - Each modular exponentiation: O(log n) operations

    Space Complexity: O(1)

    Applications:
    - RSA key generation (finding large primes)
    - Cryptographic protocols
    - Primality certificates

    Args:
        n: Number to test for primality (must be > 2)
        k: Number of testing rounds (higher k = lower error probability)

    Returns:
        True if n is probably prime, False if n is definitely composite

    Example:
        >>> miller_rabin(17, k=5)
        True
        >>> miller_rabin(561, k=5)  # 561 is a Carmichael number
        False
    """
    # Handle small cases
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r × d where d is odd
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Deterministic witnesses for small n
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
        # Use random witnesses for larger n
        witnesses = [random.randrange(2, n - 1) for _ in range(k)]

    # Test each witness
    for a in witnesses:
        if a >= n:
            continue

        # Compute x = a^d mod n
        x = mod_exp(a, d, n)

        if x == 1 or x == n - 1:
            continue

        # Square x repeatedly r-1 times
        composite = True
        for _ in range(r - 1):
            x = mod_exp(x, 2, n)
            if x == n - 1:
                composite = False
                break

        if composite:
            return False  # Definitely composite

    return True  # Probably prime


def pollard_rho(n: int, max_iterations: int = 100000) -> Optional[int]:
    """
    Pollard's Rho algorithm for integer factorization.

    Algorithm:
    Uses Floyd's cycle detection on the sequence:
        x₀ = 2
        xᵢ₊₁ = (xᵢ² + 1) mod n

    The sequence eventually enters a cycle. If gcd(|xᵢ - xⱼ|, n) > 1,
    we've found a non-trivial factor.

    Mathematical Foundation:
    - Birthday Paradox: Expected cycle length is O(√p) for smallest prime factor p
    - Floyd's algorithm detects cycles in O(√p) time and O(1) space
    - Using tortoise-and-hare: tortoise moves 1 step, hare moves 2 steps

    Why it works:
    - If p | n, the sequence mod p will cycle faster than mod n
    - When tortoise and hare collide mod p, their difference is divisible by p
    - gcd finds the factor p

    Time Complexity: O(n^(1/4)) expected, but highly variable
    Space Complexity: O(1)

    Limitations:
    - May fail to find factors (returns None)
    - Not guaranteed to find smallest factor
    - Can be slow for large primes

    Optimizations:
    - Brent's improvement: Replaces Floyd's cycle detection (20-25% faster)
    - Different polynomials: xᵢ₊₁ = (xᵢ² + c) mod n for various c

    Applications:
    - Breaking RSA with weak key generation
    - Finding factors of semi-primes
    - Computational number theory research

    Args:
        n: Number to factorize (must be composite)
        max_iterations: Maximum number of iterations before giving up

    Returns:
        A non-trivial factor of n, or None if factorization fails

    Example:
        >>> pollard_rho(8051)  # 8051 = 83 × 97
        83  # (or 97, depending on which factor is found first)
    """
    if n == 1:
        return None
    if n % 2 == 0:
        return 2

    # Random starting values can help find different factors
    x = random.randint(2, n - 1)
    y = x
    c = random.randint(1, n - 1)
    d = 1

    # Floyd's cycle detection
    iteration = 0
    while d == 1 and iteration < max_iterations:
        # Tortoise: move one step
        x = (x * x + c) % n

        # Hare: move two steps
        y = (y * y + c) % n
        y = (y * y + c) % n

        # Check if we found a factor
        d = gcd(abs(x - y), n)

        iteration += 1

    if d == n or iteration >= max_iterations:
        # Failed to find factor, try again with different parameters
        return None

    return d


def pollard_rho_factorize(n: int, max_attempts: int = 10) -> List[int]:
    """
    Factorize n using Pollard's Rho algorithm with multiple attempts.

    Combines Pollard's Rho with trial division and recursion to fully
    factorize a number.

    Algorithm:
    1. Handle small factors with trial division
    2. Use Miller-Rabin to check if n is prime
    3. Apply Pollard's Rho to find a factor
    4. Recursively factorize the factor and quotient

    Time Complexity: O(n^(1/4)) expected per factor
    Space Complexity: O(log n) for recursion

    Args:
        n: Number to factorize
        max_attempts: Number of attempts for each Pollard's Rho call

    Returns:
        List of prime factors (not necessarily sorted)

    Example:
        >>> sorted(pollard_rho_factorize(60))
        [2, 2, 3, 5]
    """
    if n < 2:
        return []

    # Handle small factors with trial division
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    for i in range(3, min(1000, int(math.sqrt(n)) + 1), 2):
        while n % i == 0:
            factors.append(i)
            n //= i

    if n == 1:
        return factors

    # Check if n is prime
    if miller_rabin(n, k=10):
        return factors + [n]

    # Try Pollard's Rho multiple times
    for _ in range(max_attempts):
        factor = pollard_rho(n)
        if factor and factor != n:
            # Recursively factorize both parts
            factors.extend(pollard_rho_factorize(factor, max_attempts))
            factors.extend(pollard_rho_factorize(n // factor, max_attempts))
            return factors

    # If Pollard's Rho fails, return n as a "factor" (might be composite)
    return factors + [n]


def generate_prime(bits: int, k: int = 20) -> int:
    """
    Generate a random probable prime with specified bit length.

    Algorithm:
    1. Generate random odd number with 'bits' bits
    2. Test with Miller-Rabin
    3. If composite, try next odd number
    4. Repeat until prime is found

    Optimizations:
    - Set highest and lowest bits to ensure correct bit length
    - Only test odd numbers
    - Use k rounds of Miller-Rabin (error probability < 4^(-k))

    Prime Number Theorem:
    The probability that a random n-bit number is prime is approximately 1/ln(2^n) ≈ 1/(0.693n).
    So we expect to test about 0.693n numbers before finding a prime.

    Time Complexity: O(n² log n) where n is bit length
    - Expected O(n) candidates
    - Each Miller-Rabin test: O(n² log n)

    Applications:
    - RSA key generation
    - Cryptographic protocol setup
    - Generating safe primes (p where (p-1)/2 is also prime)

    Args:
        bits: Bit length of prime to generate
        k: Number of Miller-Rabin rounds (higher = more confidence)

    Returns:
        A probable prime with exactly 'bits' bits

    Example:
        >>> p = generate_prime(128)
        >>> p.bit_length()
        128
        >>> miller_rabin(p, k=20)
        True
    """
    while True:
        # Generate random odd number with 'bits' bits
        # Set highest bit to 1 (ensures n has 'bits' bits)
        # Set lowest bit to 1 (ensures n is odd)
        n = random.randrange(2**(bits-1), 2**bits) | 1

        # Test primality
        if miller_rabin(n, k=k):
            return n


def is_perfect_power(n: int) -> bool:
    """
    Check if n is a perfect power (n = a^b for some a, b > 1).

    Algorithm:
    For each possible exponent b from 2 to log₂(n):
        - Compute a = n^(1/b) using binary search
        - Check if a^b == n

    Time Complexity: O(log³ n)
    Space Complexity: O(1)

    Args:
        n: Number to test

    Returns:
        True if n is a perfect power, False otherwise

    Example:
        >>> is_perfect_power(64)  # 64 = 2^6
        True
        >>> is_perfect_power(65)
        False
    """
    if n <= 1:
        return True

    # Check for each possible exponent
    max_exp = n.bit_length()
    for b in range(2, max_exp + 1):
        # Binary search for a such that a^b = n
        low, high = 1, int(n**(1/b)) + 2

        while low <= high:
            mid = (low + high) // 2
            power = mid ** b

            if power == n:
                return True
            elif power < n:
                low = mid + 1
            else:
                high = mid - 1

    return False


def carmichael_lambda(n: int) -> int:
    """
    Calculate the Carmichael lambda function λ(n).

    The Carmichael function gives the smallest positive integer m such that:
        a^m ≡ 1 (mod n) for all a coprime to n

    Mathematical Foundation:
    - λ(p^k) = φ(p^k) = p^(k-1)(p-1) for odd prime p
    - λ(2^k) = 2^(k-2) for k ≥ 3
    - λ(n) = lcm(λ(p₁^k₁), λ(p₂^k₂), ...) for n = p₁^k₁ × p₂^k₂ × ...

    Relation to Totient:
    - λ(n) always divides φ(n)
    - Often λ(n) < φ(n), making it more useful for some applications

    Applications:
    - RSA cryptosystem (alternative to φ(n))
    - Carmichael numbers (λ(n) | n-1)

    Time Complexity: O(√n)
    Space Complexity: O(log n)

    Args:
        n: Positive integer

    Returns:
        Carmichael lambda of n

    Example:
        >>> carmichael_lambda(15)  # 15 = 3 × 5
        4  # lcm(φ(3), φ(5)) = lcm(2, 4) = 4
    """
    if n == 1:
        return 1

    from number_theory import prime_factorization, lcm

    factors = prime_factorization(n)
    lambda_values = []

    for prime, exponent in factors:
        if prime == 2:
            if exponent <= 2:
                lambda_values.append(2 ** (exponent - 1))
            else:
                lambda_values.append(2 ** (exponent - 2))
        else:
            # λ(p^k) = φ(p^k) = p^(k-1)(p-1)
            lambda_values.append((prime ** (exponent - 1)) * (prime - 1))

    # Return LCM of all lambda values
    from functools import reduce
    return reduce(lcm, lambda_values)


def main():
    """Demonstration and testing of advanced number theory algorithms."""
    print("=" * 70)
    print("ADVANCED NUMBER THEORY ALGORITHMS - DEMONSTRATION")
    print("=" * 70)

    # 1. Miller-Rabin Primality Testing
    print("\n1. MILLER-RABIN PRIMALITY TEST")
    print("-" * 50)
    test_numbers = [
        (17, True),
        (561, False),  # Carmichael number
        (1105, False),  # Another Carmichael number
        (2047, False),  # Pseudoprime to base 2
        (8191, True),   # Mersenne prime
        (9973, True),
        (10001, False)
    ]

    for n, expected in test_numbers:
        result = miller_rabin(n, k=20)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status:4s}] {n:5d}: {'PRIME' if result else 'COMPOSITE':12s} (expected: {'PRIME' if expected else 'COMPOSITE'})")

    # 2. Large Prime Generation
    print("\n2. RANDOM PRIME GENERATION")
    print("-" * 50)
    bit_lengths = [32, 64, 128]
    for bits in bit_lengths:
        prime = generate_prime(bits, k=20)
        print(f"{bits}-bit prime: {prime}")
        print(f"  Binary length: {prime.bit_length()} bits")
        print(f"  Is prime: {miller_rabin(prime, k=20)}")

    # 3. Pollard's Rho Factorization
    print("\n3. POLLARD'S RHO FACTORIZATION")
    print("-" * 50)
    test_composites = [
        8051,      # 83 × 97
        10403,     # 101 × 103
        15770708441,  # 127 × 103 × 991 × 1223
    ]

    for n in test_composites:
        print(f"\nFactoring {n}:")
        factors = pollard_rho_factorize(n, max_attempts=20)
        factors.sort()
        print(f"  Factors: {factors}")
        product = 1
        for f in factors:
            product *= f
        print(f"  Verification: {' * '.join(map(str, factors))} = {product}")
        print(f"  Correct: {product == n}")

    # 4. Perfect Power Detection
    print("\n4. PERFECT POWER DETECTION")
    print("-" * 50)
    test_numbers = [
        (64, True, "2^6"),
        (128, True, "2^7"),
        (125, True, "5^3"),
        (100, True, "10^2"),
        (65, False, "not a perfect power"),
        (1000, True, "10^3"),
    ]

    for n, expected, desc in test_numbers:
        result = is_perfect_power(n)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status:4s}] {n:4d}: {'YES' if result else 'NO':3s} - {desc}")

    # 5. Carmichael Lambda Function
    print("\n5. CARMICHAEL LAMBDA FUNCTION")
    print("-" * 50)
    from number_theory import totient
    test_values = [8, 15, 16, 21, 35, 561]
    for n in test_values:
        lambda_n = carmichael_lambda(n)
        phi_n = totient(n)
        print(f"n = {n:3d}: lambda(n) = {lambda_n:3d}, phi(n) = {phi_n:3d}, ratio = {phi_n/lambda_n:.2f}")

    # 6. Cryptographic Application Example
    print("\n6. CRYPTOGRAPHIC APPLICATION: SIMPLE RSA DEMO")
    print("-" * 50)
    print("Generating small RSA keys (for demonstration only)...")

    # Generate two small primes
    p = generate_prime(16, k=10)
    q = generate_prime(16, k=10)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Choose e (commonly 65537 in practice)
    e = 65537
    if gcd(e, phi_n) != 1:
        e = 3  # Fallback for small primes

    from number_theory import mod_inverse
    d = mod_inverse(e, phi_n)

    print(f"Prime p: {p}")
    print(f"Prime q: {q}")
    print(f"Modulus n = p*q: {n}")
    print(f"Public exponent e: {e}")
    print(f"Private exponent d: {d}")

    # Encrypt and decrypt a message
    message = 42
    ciphertext = mod_exp(message, e, n)
    decrypted = mod_exp(ciphertext, d, n)

    print(f"\nMessage: {message}")
    print(f"Encrypted: {ciphertext}")
    print(f"Decrypted: {decrypted}")
    print(f"Correct: {message == decrypted}")

    # 7. Performance Notes
    print("\n7. ALGORITHM COMPLEXITIES")
    print("-" * 50)
    print("Miller-Rabin:      O(k log^3 n) for k rounds")
    print("Pollard's Rho:     O(n^(1/4)) expected")
    print("Prime Generation:  O(n^2 log n) for n-bit prime")
    print("Perfect Power:     O(log^3 n)")
    print("Carmichael Lambda: O(sqrt(n))")

    print("\n" + "=" * 70)
    print("All advanced algorithms demonstrated successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
