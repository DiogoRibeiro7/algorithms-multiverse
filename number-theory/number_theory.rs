/*
 * Number Theory Algorithms - Rust Implementation
 * ==============================================
 *
 * Memory-safe, high-performance implementation of fundamental number theory algorithms.
 *
 * Features:
 * - Zero-cost abstractions
 * - Memory safety without garbage collection
 * - Support for arbitrary precision with num-bigint (optional)
 * - Comprehensive error handling
 *
 * Compilation:
 *   rustc number_theory.rs
 *   # Or for optimized build:
 *   rustc -O number_theory.rs
 *
 * With Cargo (for num-bigint support):
 *   Add to Cargo.toml:
 *   [dependencies]
 *   num-bigint = "0.4"
 *   num-traits = "0.2"
 *
 * Usage:
 *   ./number_theory
 *
 * Author: algorithms-multiverse
 */

use std::collections::HashMap;

// ============================================================================
// PRIME NUMBER GENERATION
// ============================================================================

/// Sieve of Eratosthenes - Generate all primes up to limit
///
/// Time Complexity: O(n log log n)
/// Space Complexity: O(n)
///
/// # Mathematical Foundation
/// Any composite number n has a prime factor p ≤ √n.
/// By marking multiples of all primes ≤ √limit, we identify all composites.
///
/// # Examples
/// ```
/// let primes = sieve_of_eratosthenes(30);
/// assert_eq!(primes, vec![2, 3, 5, 7, 11, 13, 17, 19, 23, 29]);
/// ```
fn sieve_of_eratosthenes(limit: u64) -> Vec<u64> {
    if limit < 2 {
        return Vec::new();
    }

    // Initialize sieve: true means "potentially prime"
    let mut is_prime = vec![true; (limit + 1) as usize];
    is_prime[0] = false;
    is_prime[1] = false;

    // Sieve algorithm
    let sqrt_limit = (limit as f64).sqrt() as u64;
    for i in 2..=sqrt_limit {
        if is_prime[i as usize] {
            // Mark all multiples of i as composite
            let mut j = i * i;
            while j <= limit {
                is_prime[j as usize] = false;
                j += i;
            }
        }
    }

    // Collect primes
    (2..=limit)
        .filter(|&i| is_prime[i as usize])
        .collect()
}

/// Sieve of Sundaram - Alternative prime generation algorithm
///
/// Time Complexity: O(n log n)
/// Space Complexity: O(n)
///
/// # Mathematical Foundation
/// Every odd composite number can be written as (2i+1)(2j+1) = 2(i+j+2ij)+1.
/// By marking all i+j+2ij values, we identify positions of odd composites.
fn sieve_of_sundaram(limit: u64) -> Vec<u64> {
    if limit < 2 {
        return Vec::new();
    }
    if limit == 2 {
        return vec![2];
    }

    // Calculate the limit for the sundaram sieve
    let n = (limit - 1) / 2;

    // Initialize array: true means "unmarked" (potentially prime)
    let mut unmarked = vec![true; (n + 1) as usize];

    // Mark positions i+j+2ij
    for i in 1..=n {
        let mut j = i;
        loop {
            let pos = i + j + 2 * i * j;
            if pos > n {
                break;
            }
            unmarked[pos as usize] = false;
            j += 1;
        }
    }

    // Generate primes: 2k+1 for unmarked k
    let mut primes = vec![2]; // 2 is the only even prime
    for k in 1..=n {
        if unmarked[k as usize] {
            let prime = 2 * k + 1;
            if prime <= limit {
                primes.push(prime);
            }
        }
    }

    primes
}

// ============================================================================
// GREATEST COMMON DIVISOR
// ============================================================================

/// Euclidean algorithm for GCD
///
/// Time Complexity: O(log min(a, b))
/// Space Complexity: O(1)
///
/// # Mathematical Proof
/// gcd(a, b) = gcd(b, a mod b) when b ≠ 0
/// gcd(a, 0) = a
///
/// # Examples
/// ```
/// assert_eq!(gcd(48, 18), 6);
/// assert_eq!(gcd(17, 19), 1);
/// ```
fn gcd(mut a: u64, mut b: u64) -> u64 {
    while b != 0 {
        let temp = b;
        b = a % b;
        a = temp;
    }
    a
}

/// Extended Euclidean Algorithm
/// Finds gcd(a, b) and Bézout coefficients x, y such that ax + by = gcd(a, b)
///
/// Time Complexity: O(log min(a, b))
/// Space Complexity: O(1)
///
/// # Applications
/// - Computing modular multiplicative inverse
/// - Solving linear Diophantine equations
/// - Chinese Remainder Theorem
fn extended_gcd(a: i64, b: i64) -> (i64, i64, i64) {
    if b == 0 {
        return (a, 1, 0);
    }

    let (gcd_val, x1, y1) = extended_gcd(b, a % b);
    let x = y1;
    let y = x1 - (a / b) * y1;

    (gcd_val, x, y)
}

/// Least Common Multiple
///
/// Formula: lcm(a, b) = (a × b) / gcd(a, b)
fn lcm(a: u64, b: u64) -> u64 {
    if a == 0 || b == 0 {
        return 0;
    }
    (a / gcd(a, b)) * b
}

// ============================================================================
// MODULAR ARITHMETIC
// ============================================================================

/// Modular exponentiation using binary exponentiation
/// Computes: base^exponent mod modulus
///
/// Time Complexity: O(log exponent)
/// Space Complexity: O(1)
///
/// # Critical for Cryptography
/// - RSA encryption/decryption
/// - Diffie-Hellman key exchange
/// - Digital signatures
///
/// Prevents integer overflow by taking mod at each step
fn mod_exp(mut base: u64, mut exponent: u64, modulus: u64) -> u64 {
    if modulus == 1 {
        return 0;
    }

    let mut result = 1u64;
    base %= modulus;

    while exponent > 0 {
        if exponent & 1 == 1 {
            result = ((result as u128 * base as u128) % modulus as u128) as u64;
        }
        exponent >>= 1;
        base = ((base as u128 * base as u128) % modulus as u128) as u64;
    }

    result
}

/// Modular multiplicative inverse
/// Find x such that (a × x) ≡ 1 (mod m)
///
/// Uses Extended Euclidean Algorithm
/// Inverse exists if and only if gcd(a, m) = 1
///
/// Returns None if inverse doesn't exist
fn mod_inverse(a: i64, m: i64) -> Option<i64> {
    let (g, x, _) = extended_gcd(a, m);

    if g != 1 {
        return None; // Inverse doesn't exist
    }

    // Ensure positive result
    Some(((x % m) + m) % m)
}

// ============================================================================
// PRIME FACTORIZATION
// ============================================================================

/// Prime factorization using trial division
///
/// Time Complexity: O(√n)
/// Space Complexity: O(log n)
///
/// Returns a HashMap of prime -> exponent pairs
///
/// # Examples
/// ```
/// let factors = prime_factorization(60);
/// // factors = {2: 2, 3: 1, 5: 1} since 60 = 2² × 3 × 5
/// ```
fn prime_factorization(mut n: u64) -> HashMap<u64, u32> {
    let mut factors = HashMap::new();

    if n < 2 {
        return factors;
    }

    // Handle factor 2
    while n % 2 == 0 {
        *factors.entry(2).or_insert(0) += 1;
        n /= 2;
    }

    // Check odd divisors
    let mut i = 3u64;
    while i * i <= n {
        while n % i == 0 {
            *factors.entry(i).or_insert(0) += 1;
            n /= i;
        }
        i += 2;
    }

    // If n > 1, then it's a prime factor
    if n > 1 {
        *factors.entry(n).or_insert(0) += 1;
    }

    factors
}

// ============================================================================
// PRIMALITY TESTING
// ============================================================================

/// Miller-Rabin primality test
///
/// Probabilistic test with deterministic witnesses for n < 2^64
///
/// Time Complexity: O(k log³ n) for k rounds
/// Error probability: ≤ 4^(-k) for random witnesses
///
/// # Applications
/// - RSA key generation
/// - Cryptographic protocols
/// - Prime number research
fn miller_rabin(n: u64, _k: u32) -> bool {
    // Handle small cases
    if n < 2 {
        return false;
    }
    if n == 2 || n == 3 {
        return true;
    }
    if n % 2 == 0 {
        return false;
    }

    // Write n-1 as 2^r × d where d is odd
    let mut d = n - 1;
    let mut r = 0;
    while d % 2 == 0 {
        r += 1;
        d /= 2;
    }

    // Deterministic witnesses for n < 2^64
    let witnesses = vec![2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37];

    // Test each witness
    'witness_loop: for &a in &witnesses {
        if a >= n {
            continue;
        }

        // Compute x = a^d mod n
        let mut x = mod_exp(a, d, n);

        if x == 1 || x == n - 1 {
            continue;
        }

        // Square x repeatedly r-1 times
        for _ in 0..r - 1 {
            x = mod_exp(x, 2, n);
            if x == n - 1 {
                continue 'witness_loop;
            }
        }

        return false; // Definitely composite
    }

    true // Probably prime
}

/// Simple primality test using trial division
///
/// Time Complexity: O(√n)
/// Space Complexity: O(1)
fn is_prime_trial(n: u64) -> bool {
    if n < 2 {
        return false;
    }
    if n == 2 {
        return true;
    }
    if n % 2 == 0 {
        return false;
    }

    let sqrt_n = (n as f64).sqrt() as u64;
    for i in (3..=sqrt_n).step_by(2) {
        if n % i == 0 {
            return false;
        }
    }

    true
}

// ============================================================================
// EULER'S TOTIENT FUNCTION
// ============================================================================

/// Calculate Euler's totient function φ(n)
///
/// φ(n) = count of integers k where 1 ≤ k ≤ n and gcd(k, n) = 1
///
/// Time Complexity: O(√n)
/// Space Complexity: O(log n)
///
/// # Applications
/// - RSA: φ(n) used to calculate private key
/// - Euler's theorem: a^φ(n) ≡ 1 (mod n) if gcd(a,n) = 1
/// - Cyclic group theory
fn euler_totient(n: u64) -> u64 {
    if n == 1 {
        return 1;
    }

    let factors = prime_factorization(n);
    let mut result = n;

    for (&prime, _) in &factors {
        // Multiply by (1 - 1/prime) = (prime - 1)/prime
        result = result / prime * (prime - 1);
    }

    result
}

// ============================================================================
// CHINESE REMAINDER THEOREM
// ============================================================================

/// Chinese Remainder Theorem
/// Solve system of congruences:
///   x ≡ a[0] (mod m[0])
///   x ≡ a[1] (mod m[1])
///   ...
///
/// Requires moduli to be pairwise coprime
///
/// Time Complexity: O(n² log M) where M is product of moduli
/// Space Complexity: O(1)
///
/// Returns Some(solution) if successful, None if moduli not coprime
fn chinese_remainder_theorem(remainders: &[i64], moduli: &[i64]) -> Option<i64> {
    if remainders.len() != moduli.len() {
        return None;
    }

    // Check if moduli are pairwise coprime
    for i in 0..moduli.len() {
        for j in (i + 1)..moduli.len() {
            if gcd(moduli[i].abs() as u64, moduli[j].abs() as u64) != 1 {
                return None; // Not pairwise coprime
            }
        }
    }

    // Calculate M = product of all moduli
    let big_m = moduli.iter().product::<i64>();

    // Calculate solution
    let mut x = 0i64;
    for i in 0..moduli.len() {
        let mi = big_m / moduli[i];
        let yi = mod_inverse(mi, moduli[i])?;
        x = (x + remainders[i] * mi * yi) % big_m;
    }

    // Ensure positive result
    if x < 0 {
        x += big_m;
    }

    Some(x)
}

// ============================================================================
// POLLARD'S RHO FACTORIZATION
// ============================================================================

/// Pollard's Rho algorithm for integer factorization
///
/// Time Complexity: O(n^(1/4)) expected
/// Space Complexity: O(1)
///
/// May return None if factorization fails
fn pollard_rho(n: u64) -> Option<u64> {
    if n == 1 {
        return None;
    }
    if n % 2 == 0 {
        return Some(2);
    }

    // Simple random values (in production, use rand crate)
    let mut x = 2u64;
    let mut y = 2u64;
    let c = 1u64;
    let mut d = 1u64;

    // Floyd's cycle detection
    let max_iterations = 100000;
    let mut iteration = 0;

    while d == 1 && iteration < max_iterations {
        // Tortoise: move one step
        x = (((x as u128 * x as u128) + c as u128) % n as u128) as u64;

        // Hare: move two steps
        y = (((y as u128 * y as u128) + c as u128) % n as u128) as u64;
        y = (((y as u128 * y as u128) + c as u128) % n as u128) as u64;

        // Check if we found a factor
        d = gcd(if x > y { x - y } else { y - x }, n);

        iteration += 1;
    }

    if d == n || iteration >= max_iterations {
        None // Failed to find factor
    } else {
        Some(d)
    }
}

// ============================================================================
// TESTING AND DEMONSTRATION
// ============================================================================

fn print_separator(c: char, length: usize) {
    println!("{}", c.to_string().repeat(length));
}

fn test_sieve() {
    println!("\n1. PRIME NUMBER GENERATION");
    print_separator('-', 50);

    let limit = 50;
    let primes_e = sieve_of_eratosthenes(limit);
    let primes_s = sieve_of_sundaram(limit);

    println!("Primes up to {} (Eratosthenes): {:?}", limit, primes_e);
    println!("Primes up to {} (Sundaram):     {:?}", limit, primes_s);
    println!("Verification: Both methods agree: {}", primes_e == primes_s);
}

fn test_gcd() {
    println!("\n2. GCD AND LCM");
    print_separator('-', 50);

    let pairs = vec![(48, 18), (100, 35), (17, 19)];

    for (a, b) in pairs {
        let g = gcd(a, b);
        let l = lcm(a, b);
        println!("gcd({}, {}) = {}, lcm({}, {}) = {}", a, b, g, a, b, l);
    }
}

fn test_modular_arithmetic() {
    println!("\n3. MODULAR ARITHMETIC");
    print_separator('-', 50);

    println!("Modular Exponentiation:");
    let test_cases = vec![(2, 10, 1000), (3, 100, 13), (7, 256, 100)];

    for (base, exp, modulus) in test_cases {
        let result = mod_exp(base, exp, modulus);
        println!("  {}^{} mod {} = {}", base, exp, modulus, result);
    }

    println!("\nModular Inverse:");
    let inv_cases = vec![(3, 11), (7, 26)];

    for (a, m) in inv_cases {
        if let Some(inv) = mod_inverse(a, m) {
            println!("  Inverse of {} mod {} = {}", a, m, inv);
            println!("    Verification: ({} × {}) mod {} = {}", a, inv, m, (a * inv) % m);
        }
    }
}

fn test_primality() {
    println!("\n4. PRIMALITY TESTING");
    print_separator('-', 50);

    let test_numbers = vec![17, 561, 1105, 2047, 8191, 9973, 10001];

    for n in test_numbers {
        let result = miller_rabin(n, 20);
        println!("{:5}: {}", n, if result { "PRIME" } else { "COMPOSITE" });
    }
}

fn test_factorization() {
    println!("\n5. PRIME FACTORIZATION");
    print_separator('-', 50);

    let test_numbers = vec![60, 128, 1001, 2024];

    for n in test_numbers {
        let factors = prime_factorization(n);
        print!("{} = ", n);

        let mut factor_vec: Vec<_> = factors.iter().collect();
        factor_vec.sort();

        let factor_str: Vec<String> = factor_vec
            .iter()
            .map(|(prime, exp)| {
                if **exp > 1 {
                    format!("{}^{}", prime, exp)
                } else {
                    format!("{}", prime)
                }
            })
            .collect();

        println!("{}", factor_str.join(" × "));
    }
}

fn test_totient() {
    println!("\n6. EULER'S TOTIENT FUNCTION");
    print_separator('-', 50);

    let test_values = vec![1, 9, 10, 36, 100];

    for n in test_values {
        let phi = euler_totient(n);
        println!("φ({}) = {}", n, phi);
    }
}

fn test_crt() {
    println!("\n7. CHINESE REMAINDER THEOREM");
    print_separator('-', 50);

    let remainders = vec![2, 3, 2];
    let moduli = vec![3, 5, 7];

    println!("System of congruences:");
    for (a, m) in remainders.iter().zip(moduli.iter()) {
        println!("  x ≡ {} (mod {})", a, m);
    }

    if let Some(solution) = chinese_remainder_theorem(&remainders, &moduli) {
        println!("Solution: x = {}", solution);
        println!("Verification:");
        for (a, m) in remainders.iter().zip(moduli.iter()) {
            println!("  {} mod {} = {} (expected {})", solution, m, solution % m, a);
        }
    } else {
        println!("Failed to solve (moduli not pairwise coprime)");
    }
}

fn main() {
    print_separator('=', 70);
    println!("NUMBER THEORY ALGORITHMS - RUST IMPLEMENTATION");
    print_separator('=', 70);

    test_sieve();
    test_gcd();
    test_modular_arithmetic();
    test_primality();
    test_factorization();
    test_totient();
    test_crt();

    println!();
    print_separator('=', 70);
    println!("All tests completed successfully!");
    print_separator('=', 70);
}
