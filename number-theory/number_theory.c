/*
 * Number Theory Algorithms - C Implementation
 * ============================================
 *
 * High-performance implementation of fundamental number theory algorithms.
 * Uses native 64-bit integers for maximum performance.
 *
 * Compilation:
 *   gcc -O3 -o number_theory number_theory.c -lm
 *
 * Usage:
 *   ./number_theory
 *
 * Author: algorithms-multiverse
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <time.h>

/* Type definitions for clarity */
typedef uint64_t u64;
typedef int64_t i64;

/* Maximum value for sieves and arrays */
#define MAX_SIEVE 10000000

/* ============================================================================
 * PRIME NUMBER GENERATION
 * ============================================================================ */

/**
 * Sieve of Eratosthenes - Generate all primes up to limit
 *
 * Time Complexity: O(n log log n)
 * Space Complexity: O(n)
 *
 * @param limit: Upper bound for prime generation
 * @param count: Output parameter for number of primes found
 * @return: Dynamically allocated array of primes (caller must free)
 */
u64* sieve_of_eratosthenes(u64 limit, u64* count) {
    if (limit < 2) {
        *count = 0;
        return NULL;
    }

    /* Allocate and initialize sieve */
    bool* is_prime = (bool*)malloc((limit + 1) * sizeof(bool));
    if (!is_prime) {
        fprintf(stderr, "Memory allocation failed\n");
        *count = 0;
        return NULL;
    }

    memset(is_prime, true, (limit + 1) * sizeof(bool));
    is_prime[0] = is_prime[1] = false;

    /* Sieve algorithm */
    u64 sqrt_limit = (u64)sqrt((double)limit);
    for (u64 i = 2; i <= sqrt_limit; i++) {
        if (is_prime[i]) {
            /* Mark multiples of i as composite */
            for (u64 j = i * i; j <= limit; j += i) {
                is_prime[j] = false;
            }
        }
    }

    /* Count primes */
    *count = 0;
    for (u64 i = 2; i <= limit; i++) {
        if (is_prime[i]) (*count)++;
    }

    /* Collect primes */
    u64* primes = (u64*)malloc(*count * sizeof(u64));
    if (!primes) {
        fprintf(stderr, "Memory allocation failed\n");
        free(is_prime);
        *count = 0;
        return NULL;
    }

    u64 index = 0;
    for (u64 i = 2; i <= limit; i++) {
        if (is_prime[i]) {
            primes[index++] = i;
        }
    }

    free(is_prime);
    return primes;
}

/* ============================================================================
 * GREATEST COMMON DIVISOR
 * ============================================================================ */

/**
 * Euclidean algorithm for GCD
 *
 * Time Complexity: O(log min(a, b))
 * Space Complexity: O(1)
 *
 * Mathematical proof:
 *   gcd(a, b) = gcd(b, a mod b)
 *   Base case: gcd(a, 0) = a
 */
u64 gcd(u64 a, u64 b) {
    while (b != 0) {
        u64 temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

/**
 * Extended Euclidean Algorithm
 * Finds gcd(a, b) and coefficients x, y such that ax + by = gcd(a, b)
 *
 * Time Complexity: O(log min(a, b))
 * Space Complexity: O(1)
 *
 * @param a, b: Input integers
 * @param x, y: Output Bézout coefficients
 * @return: gcd(a, b)
 */
i64 extended_gcd(i64 a, i64 b, i64* x, i64* y) {
    if (b == 0) {
        *x = 1;
        *y = 0;
        return a;
    }

    i64 x1, y1;
    i64 gcd_val = extended_gcd(b, a % b, &x1, &y1);

    *x = y1;
    *y = x1 - (a / b) * y1;

    return gcd_val;
}

/**
 * Least Common Multiple
 *
 * Formula: lcm(a, b) = (a * b) / gcd(a, b)
 */
u64 lcm(u64 a, u64 b) {
    if (a == 0 || b == 0) return 0;
    return (a / gcd(a, b)) * b;  /* Avoid overflow */
}

/* ============================================================================
 * MODULAR ARITHMETIC
 * ============================================================================ */

/**
 * Modular exponentiation using binary exponentiation
 * Computes: base^exponent mod modulus
 *
 * Time Complexity: O(log exponent)
 * Space Complexity: O(1)
 *
 * Critical for cryptographic applications (RSA, Diffie-Hellman)
 * Prevents integer overflow by taking mod at each step
 */
u64 mod_exp(u64 base, u64 exponent, u64 modulus) {
    if (modulus == 1) return 0;

    u64 result = 1;
    base = base % modulus;

    while (exponent > 0) {
        /* If exponent is odd, multiply base with result */
        if (exponent & 1) {
            result = ((__uint128_t)result * base) % modulus;
        }

        /* Square the base and halve the exponent */
        exponent >>= 1;
        base = ((__uint128_t)base * base) % modulus;
    }

    return result;
}

/**
 * Modular multiplicative inverse
 * Find x such that (a * x) ≡ 1 (mod m)
 *
 * Uses Extended Euclidean Algorithm
 * Inverse exists if and only if gcd(a, m) = 1
 *
 * @return: Inverse of a mod m, or 0 if it doesn't exist
 */
u64 mod_inverse(i64 a, i64 m) {
    i64 x, y;
    i64 g = extended_gcd(a, m, &x, &y);

    if (g != 1) {
        return 0;  /* Inverse doesn't exist */
    }

    /* Ensure positive result */
    return (x % m + m) % m;
}

/* ============================================================================
 * PRIME FACTORIZATION
 * ============================================================================ */

/**
 * Prime factorization using trial division
 *
 * Time Complexity: O(√n)
 * Space Complexity: O(log n)
 *
 * Returns array of prime factors (with repetition)
 *
 * @param n: Number to factorize
 * @param count: Output parameter for number of factors
 * @return: Array of prime factors (caller must free)
 */
u64* prime_factorization(u64 n, u64* count) {
    if (n < 2) {
        *count = 0;
        return NULL;
    }

    /* Allocate maximum possible space */
    u64* factors = (u64*)malloc(64 * sizeof(u64));
    *count = 0;

    /* Handle factor 2 */
    while (n % 2 == 0) {
        factors[(*count)++] = 2;
        n /= 2;
    }

    /* Check odd divisors */
    for (u64 i = 3; i * i <= n; i += 2) {
        while (n % i == 0) {
            factors[(*count)++] = i;
            n /= i;
        }
    }

    /* If n > 1, then it's a prime factor */
    if (n > 1) {
        factors[(*count)++] = n;
    }

    return factors;
}

/* ============================================================================
 * PRIMALITY TESTING
 * ============================================================================ */

/**
 * Miller-Rabin primality test
 *
 * Probabilistic test with deterministic witnesses for n < 2^64
 *
 * Time Complexity: O(k log³ n) for k rounds
 * Error probability: ≤ 4^(-k) for random witnesses
 *
 * @param n: Number to test for primality
 * @param k: Number of testing rounds (ignored if using deterministic witnesses)
 * @return: true if probably prime, false if definitely composite
 */
bool miller_rabin(u64 n, int k) {
    /* Handle small cases */
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0) return false;

    /* Write n-1 as 2^r * d */
    u64 d = n - 1;
    int r = 0;
    while (d % 2 == 0) {
        r++;
        d /= 2;
    }

    /* Deterministic witnesses for n < 2^64 */
    u64 witnesses[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
    int num_witnesses = 12;

    /* Test each witness */
    for (int i = 0; i < num_witnesses; i++) {
        u64 a = witnesses[i];
        if (a >= n) continue;

        /* Compute x = a^d mod n */
        u64 x = mod_exp(a, d, n);

        if (x == 1 || x == n - 1) continue;

        /* Square x repeatedly r-1 times */
        bool composite = true;
        for (int j = 0; j < r - 1; j++) {
            x = mod_exp(x, 2, n);
            if (x == n - 1) {
                composite = false;
                break;
            }
        }

        if (composite) return false;
    }

    return true;
}

/**
 * Simple primality test using trial division
 *
 * Time Complexity: O(√n)
 * Space Complexity: O(1)
 */
bool is_prime_trial(u64 n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;

    u64 sqrt_n = (u64)sqrt((double)n);
    for (u64 i = 3; i <= sqrt_n; i += 2) {
        if (n % i == 0) return false;
    }

    return true;
}

/* ============================================================================
 * EULER'S TOTIENT FUNCTION
 * ============================================================================ */

/**
 * Calculate Euler's totient function φ(n)
 *
 * φ(n) = count of integers k where 1 ≤ k ≤ n and gcd(k, n) = 1
 *
 * Formula: If n = p1^a1 * p2^a2 * ... * pk^ak, then
 *          φ(n) = n * (1 - 1/p1) * (1 - 1/p2) * ... * (1 - 1/pk)
 *
 * Time Complexity: O(√n)
 * Space Complexity: O(1)
 */
u64 euler_totient(u64 n) {
    if (n == 1) return 1;

    u64 result = n;
    u64 temp = n;

    /* Handle factor 2 */
    if (temp % 2 == 0) {
        result = result / 2;
        while (temp % 2 == 0) {
            temp /= 2;
        }
    }

    /* Check odd factors */
    for (u64 i = 3; i * i <= temp; i += 2) {
        if (temp % i == 0) {
            result = result / i * (i - 1);
            while (temp % i == 0) {
                temp /= i;
            }
        }
    }

    /* If temp > 1, it's a prime factor */
    if (temp > 1) {
        result = result / temp * (temp - 1);
    }

    return result;
}

/* ============================================================================
 * CHINESE REMAINDER THEOREM
 * ============================================================================ */

/**
 * Chinese Remainder Theorem
 * Solve system of congruences:
 *   x ≡ a[0] (mod m[0])
 *   x ≡ a[1] (mod m[1])
 *   ...
 *   x ≡ a[n-1] (mod m[n-1])
 *
 * Requires moduli to be pairwise coprime
 *
 * Time Complexity: O(n² log M) where M is product of moduli
 * Space Complexity: O(1)
 *
 * @param remainders: Array of remainders
 * @param moduli: Array of moduli (must be pairwise coprime)
 * @param n: Number of congruences
 * @param result: Output parameter for solution
 * @return: true if solution found, false if moduli not coprime
 */
bool chinese_remainder_theorem(u64* remainders, u64* moduli, int n, u64* result) {
    /* Check if moduli are pairwise coprime */
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (gcd(moduli[i], moduli[j]) != 1) {
                return false;  /* Not pairwise coprime */
            }
        }
    }

    /* Calculate M = product of all moduli */
    u64 M = 1;
    for (int i = 0; i < n; i++) {
        M *= moduli[i];
    }

    /* Calculate solution */
    u64 x = 0;
    for (int i = 0; i < n; i++) {
        u64 Mi = M / moduli[i];
        u64 yi = mod_inverse(Mi, moduli[i]);
        x = (x + remainders[i] * Mi * yi) % M;
    }

    *result = x;
    return true;
}

/* ============================================================================
 * TESTING AND DEMONSTRATION
 * ============================================================================ */

void print_separator(char c, int length) {
    for (int i = 0; i < length; i++) putchar(c);
    putchar('\n');
}

void test_sieve() {
    printf("\n1. SIEVE OF ERATOSTHENES\n");
    print_separator('-', 50);

    u64 limit = 100;
    u64 count;
    u64* primes = sieve_of_eratosthenes(limit, &count);

    printf("Primes up to %llu: ", (unsigned long long)limit);
    for (u64 i = 0; i < count && i < 25; i++) {
        printf("%llu ", (unsigned long long)primes[i]);
    }
    if (count > 25) printf("...");
    printf("\nTotal: %llu primes\n", (unsigned long long)count);

    free(primes);
}

void test_gcd_lcm() {
    printf("\n2. GCD AND LCM\n");
    print_separator('-', 50);

    u64 pairs[][2] = {{48, 18}, {100, 35}, {17, 19}};
    int num_pairs = sizeof(pairs) / sizeof(pairs[0]);

    for (int i = 0; i < num_pairs; i++) {
        u64 a = pairs[i][0];
        u64 b = pairs[i][1];
        u64 g = gcd(a, b);
        u64 l = lcm(a, b);
        printf("gcd(%llu, %llu) = %llu, lcm(%llu, %llu) = %llu\n",
               (unsigned long long)a, (unsigned long long)b, (unsigned long long)g,
               (unsigned long long)a, (unsigned long long)b, (unsigned long long)l);
    }
}

void test_modular_arithmetic() {
    printf("\n3. MODULAR ARITHMETIC\n");
    print_separator('-', 50);

    /* Modular exponentiation */
    printf("Modular Exponentiation:\n");
    u64 test_cases[][3] = {{2, 10, 1000}, {3, 100, 13}, {7, 256, 100}};
    int num_cases = sizeof(test_cases) / sizeof(test_cases[0]);

    for (int i = 0; i < num_cases; i++) {
        u64 base = test_cases[i][0];
        u64 exp = test_cases[i][1];
        u64 mod = test_cases[i][2];
        u64 result = mod_exp(base, exp, mod);
        printf("  %llu^%llu mod %llu = %llu\n",
               (unsigned long long)base, (unsigned long long)exp,
               (unsigned long long)mod, (unsigned long long)result);
    }

    /* Modular inverse */
    printf("\nModular Inverse:\n");
    i64 inv_cases[][2] = {{3, 11}, {7, 26}};
    int num_inv = sizeof(inv_cases) / sizeof(inv_cases[0]);

    for (int i = 0; i < num_inv; i++) {
        i64 a = inv_cases[i][0];
        i64 m = inv_cases[i][1];
        u64 inv = mod_inverse(a, m);
        if (inv > 0) {
            printf("  Inverse of %lld mod %lld = %llu\n",
                   (long long)a, (long long)m, (unsigned long long)inv);
            printf("    Verification: (%lld × %llu) mod %lld = %llu\n",
                   (long long)a, (unsigned long long)inv, (long long)m,
                   (unsigned long long)((a * inv) % m));
        }
    }
}

void test_primality() {
    printf("\n4. PRIMALITY TESTING\n");
    print_separator('-', 50);

    u64 test_numbers[] = {17, 561, 1105, 2047, 8191, 9973, 10001};
    int num_tests = sizeof(test_numbers) / sizeof(test_numbers[0]);

    for (int i = 0; i < num_tests; i++) {
        u64 n = test_numbers[i];
        bool result = miller_rabin(n, 20);
        printf("%llu: %s\n", (unsigned long long)n,
               result ? "PRIME" : "COMPOSITE");
    }
}

void test_factorization() {
    printf("\n5. PRIME FACTORIZATION\n");
    print_separator('-', 50);

    u64 test_numbers[] = {60, 128, 1001, 2024};
    int num_tests = sizeof(test_numbers) / sizeof(test_numbers[0]);

    for (int i = 0; i < num_tests; i++) {
        u64 n = test_numbers[i];
        u64 count;
        u64* factors = prime_factorization(n, &count);

        printf("%llu = ", (unsigned long long)n);
        for (u64 j = 0; j < count; j++) {
            printf("%llu", (unsigned long long)factors[j]);
            if (j < count - 1) printf(" × ");
        }
        printf("\n");

        free(factors);
    }
}

void test_totient() {
    printf("\n6. EULER'S TOTIENT FUNCTION\n");
    print_separator('-', 50);

    u64 test_values[] = {1, 9, 10, 36, 100};
    int num_tests = sizeof(test_values) / sizeof(test_values[0]);

    for (int i = 0; i < num_tests; i++) {
        u64 n = test_values[i];
        u64 phi = euler_totient(n);
        printf("φ(%llu) = %llu\n", (unsigned long long)n, (unsigned long long)phi);
    }
}

void test_crt() {
    printf("\n7. CHINESE REMAINDER THEOREM\n");
    print_separator('-', 50);

    u64 remainders[] = {2, 3, 2};
    u64 moduli[] = {3, 5, 7};
    int n = 3;
    u64 result;

    printf("System of congruences:\n");
    for (int i = 0; i < n; i++) {
        printf("  x ≡ %llu (mod %llu)\n",
               (unsigned long long)remainders[i],
               (unsigned long long)moduli[i]);
    }

    if (chinese_remainder_theorem(remainders, moduli, n, &result)) {
        printf("Solution: x = %llu\n", (unsigned long long)result);
        printf("Verification:\n");
        for (int i = 0; i < n; i++) {
            printf("  %llu mod %llu = %llu (expected %llu)\n",
                   (unsigned long long)result,
                   (unsigned long long)moduli[i],
                   (unsigned long long)(result % moduli[i]),
                   (unsigned long long)remainders[i]);
        }
    } else {
        printf("Failed to solve (moduli not pairwise coprime)\n");
    }
}

int main() {
    print_separator('=', 70);
    printf("NUMBER THEORY ALGORITHMS - C IMPLEMENTATION\n");
    print_separator('=', 70);

    test_sieve();
    test_gcd_lcm();
    test_modular_arithmetic();
    test_primality();
    test_factorization();
    test_totient();
    test_crt();

    printf("\n");
    print_separator('=', 70);
    printf("All tests completed successfully!\n");
    print_separator('=', 70);

    return 0;
}
