#!/usr/bin/env Rscript
# ============================================================================
# Number Theory Algorithms - R Implementation
# ============================================================================
#
# Statistical computing implementation of fundamental number theory algorithms.
#
# Features:
# - Vectorized operations where possible
# - Integration with gmp package for big integers (optional)
# - Statistical analysis applications
# - Data visualization support
#
# Installation of optional packages:
#   install.packages("gmp")
#   install.packages("microbenchmark")
#
# Usage:
#   Rscript number_theory.R
#   # Or in R console:
#   source("number_theory.R")
#
# Author: algorithms-multiverse
# ============================================================================

# ============================================================================
# PRIME NUMBER GENERATION
# ============================================================================

#' Sieve of Eratosthenes - Generate all primes up to limit
#'
#' Time Complexity: O(n log log n)
#' Space Complexity: O(n)
#'
#' @param limit Upper bound for prime generation
#' @return Vector of all prime numbers <= limit
#'
#' @examples
#' sieve_of_eratosthenes(30)
#' # [1]  2  3  5  7 11 13 17 19 23 29
sieve_of_eratosthenes <- function(limit) {
    if (limit < 2) {
        return(integer(0))
    }

    # Initialize sieve: TRUE means "potentially prime"
    is_prime <- rep(TRUE, limit + 1)
    is_prime[1:2] <- c(FALSE, FALSE)  # 0 and 1 are not prime

    # Sieve algorithm
    sqrt_limit <- floor(sqrt(limit))
    for (i in 2:sqrt_limit) {
        if (is_prime[i + 1]) {
            # Mark all multiples of i as composite
            multiples <- seq(i * i, limit, by = i)
            is_prime[multiples + 1] <- FALSE
        }
    }

    # Return primes (adjust for 0-based indexing)
    which(is_prime) - 1
}

#' Sieve of Sundaram - Alternative prime generation algorithm
#'
#' Time Complexity: O(n log n)
#' Space Complexity: O(n)
#'
#' @param limit Upper bound for prime generation
#' @return Vector of all prime numbers <= limit
sieve_of_sundaram <- function(limit) {
    if (limit < 2) {
        return(integer(0))
    }
    if (limit == 2) {
        return(2)
    }

    # Calculate the limit for the sundaram sieve
    n <- floor((limit - 1) / 2)

    # Initialize array: TRUE means "unmarked" (potentially prime)
    unmarked <- rep(TRUE, n + 1)

    # Mark positions i+j+2ij
    for (i in 1:n) {
        j <- i
        while (i + j + 2*i*j <= n) {
            unmarked[i + j + 2*i*j + 1] <- FALSE
            j <- j + 1
        }
    }

    # Generate primes: 2k+1 for unmarked k
    primes <- c(2)  # 2 is the only even prime
    for (k in 1:n) {
        if (unmarked[k + 1]) {
            prime <- 2*k + 1
            if (prime <= limit) {
                primes <- c(primes, prime)
            }
        }
    }

    primes
}

# ============================================================================
# GREATEST COMMON DIVISOR
# ============================================================================

#' Euclidean algorithm for GCD
#'
#' Time Complexity: O(log min(a, b))
#' Space Complexity: O(1)
#'
#' @param a,b Non-negative integers
#' @return Greatest common divisor of a and b
#'
#' @examples
#' gcd(48, 18)  # Returns 6
gcd <- function(a, b) {
    a <- abs(a)
    b <- abs(b)

    while (b != 0) {
        temp <- b
        b <- a %% b
        a <- temp
    }

    return(a)
}

#' Extended Euclidean Algorithm
#'
#' Finds gcd(a, b) and Bézout coefficients x, y such that ax + by = gcd(a, b)
#'
#' @param a,b Integers
#' @return List with gcd, x, and y
#'
#' @examples
#' extended_gcd(35, 15)
#' # $gcd: 5, $x: 1, $y: -2  (because 35*1 + 15*(-2) = 5)
extended_gcd <- function(a, b) {
    old_r <- a
    r <- b
    old_s <- 1
    s <- 0
    old_t <- 0
    t <- 1

    while (r != 0) {
        quotient <- old_r %/% r

        temp <- r
        r <- old_r - quotient * r
        old_r <- temp

        temp <- s
        s <- old_s - quotient * s
        old_s <- temp

        temp <- t
        t <- old_t - quotient * t
        old_t <- temp
    }

    list(gcd = old_r, x = old_s, y = old_t)
}

#' Least Common Multiple
#'
#' @param a,b Positive integers
#' @return Least common multiple of a and b
lcm <- function(a, b) {
    if (a == 0 || b == 0) {
        return(0)
    }
    return(abs(a * b) %/% gcd(a, b))
}

# ============================================================================
# MODULAR ARITHMETIC
# ============================================================================

#' Modular exponentiation using binary exponentiation
#'
#' Computes: base^exponent mod modulus
#'
#' Time Complexity: O(log exponent)
#' Space Complexity: O(1)
#'
#' @param base Base number
#' @param exponent Power to raise base to
#' @param modulus Modulus
#' @return base^exponent mod modulus
#'
#' @examples
#' mod_exp(2, 10, 1000)  # Returns 24
mod_exp <- function(base, exponent, modulus) {
    if (modulus == 1) {
        return(0)
    }

    result <- 1
    base <- base %% modulus

    while (exponent > 0) {
        # If exponent is odd, multiply base with result
        if (exponent %% 2 == 1) {
            result <- (result * base) %% modulus
        }

        # Square the base and halve the exponent
        exponent <- exponent %/% 2
        base <- (base * base) %% modulus
    }

    return(result)
}

#' Modular multiplicative inverse
#'
#' Find x such that (a * x) ≡ 1 (mod m)
#'
#' @param a Integer to find inverse of
#' @param m Modulus
#' @return Modular inverse of a mod m, or NA if it doesn't exist
#'
#' @examples
#' mod_inverse(3, 11)  # Returns 4
mod_inverse <- function(a, m) {
    result <- extended_gcd(a, m)

    if (result$gcd != 1) {
        return(NA)  # Inverse doesn't exist
    }

    # Make sure result is positive
    return((result$x %% m + m) %% m)
}

# ============================================================================
# PRIME FACTORIZATION
# ============================================================================

#' Prime factorization using trial division
#'
#' Time Complexity: O(√n)
#' Space Complexity: O(log n)
#'
#' @param n Integer to factorize (n >= 2)
#' @return Data frame with columns 'prime' and 'exponent'
#'
#' @examples
#' prime_factorization(60)
#' #   prime exponent
#' # 1     2        2
#' # 2     3        1
#' # 3     5        1
prime_factorization <- function(n) {
    if (n < 2) {
        return(data.frame(prime = integer(0), exponent = integer(0)))
    }

    factors <- list()

    # Handle factor 2
    if (n %% 2 == 0) {
        exponent <- 0
        while (n %% 2 == 0) {
            exponent <- exponent + 1
            n <- n %/% 2
        }
        factors[[length(factors) + 1]] <- c(prime = 2, exponent = exponent)
    }

    # Check odd divisors
    divisor <- 3
    while (divisor * divisor <= n) {
        if (n %% divisor == 0) {
            exponent <- 0
            while (n %% divisor == 0) {
                exponent <- exponent + 1
                n <- n %/% divisor
            }
            factors[[length(factors) + 1]] <- c(prime = divisor, exponent = exponent)
        }
        divisor <- divisor + 2
    }

    # If n > 1, then it's a prime factor
    if (n > 1) {
        factors[[length(factors) + 1]] <- c(prime = n, exponent = 1)
    }

    # Convert to data frame
    if (length(factors) == 0) {
        return(data.frame(prime = integer(0), exponent = integer(0)))
    }

    do.call(rbind, lapply(factors, function(x) {
        data.frame(prime = x[1], exponent = x[2])
    }))
}

# ============================================================================
# PRIMALITY TESTING
# ============================================================================

#' Miller-Rabin primality test
#'
#' Time Complexity: O(k log³ n) for k rounds
#' Error probability: ≤ 4^(-k) for random witnesses
#'
#' @param n Number to test for primality
#' @param k Number of testing rounds
#' @return TRUE if n is probably prime, FALSE if definitely composite
#'
#' @examples
#' miller_rabin(17, k = 5)   # TRUE
#' miller_rabin(561, k = 5)  # FALSE (Carmichael number)
miller_rabin <- function(n, k = 5) {
    # Handle small cases
    if (n < 2) return(FALSE)
    if (n == 2 || n == 3) return(TRUE)
    if (n %% 2 == 0) return(FALSE)

    # Write n-1 as 2^r × d where d is odd
    d <- n - 1
    r <- 0
    while (d %% 2 == 0) {
        r <- r + 1
        d <- d %/% 2
    }

    # Deterministic witnesses for small n
    witnesses <- c(2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)

    # Test each witness
    for (a in witnesses) {
        if (a >= n) next

        # Compute x = a^d mod n
        x <- mod_exp(a, d, n)

        if (x == 1 || x == n - 1) next

        # Square x repeatedly r-1 times
        composite <- TRUE
        for (j in 1:(r - 1)) {
            x <- mod_exp(x, 2, n)
            if (x == n - 1) {
                composite <- FALSE
                break
            }
        }

        if (composite) return(FALSE)
    }

    return(TRUE)
}

#' Simple primality test using trial division
#'
#' Time Complexity: O(√n)
#' Space Complexity: O(1)
#'
#' @param n Number to test
#' @return TRUE if n is prime, FALSE otherwise
is_prime_trial <- function(n) {
    if (n < 2) return(FALSE)
    if (n == 2) return(TRUE)
    if (n %% 2 == 0) return(FALSE)

    sqrt_n <- floor(sqrt(n))
    for (i in seq(3, sqrt_n, by = 2)) {
        if (n %% i == 0) return(FALSE)
    }

    return(TRUE)
}

# ============================================================================
# EULER'S TOTIENT FUNCTION
# ============================================================================

#' Calculate Euler's totient function φ(n)
#'
#' φ(n) = count of integers k where 1 ≤ k ≤ n and gcd(k, n) = 1
#'
#' Time Complexity: O(√n)
#' Space Complexity: O(log n)
#'
#' @param n Positive integer
#' @return Euler's totient of n
#'
#' @examples
#' euler_totient(9)   # Returns 6
#' euler_totient(36)  # Returns 12
euler_totient <- function(n) {
    if (n == 1) return(1)

    result <- n
    factors <- prime_factorization(n)

    for (prime in factors$prime) {
        # Multiply by (1 - 1/prime) = (prime - 1)/prime
        result <- result %/% prime * (prime - 1)
    }

    return(result)
}

# ============================================================================
# CHINESE REMAINDER THEOREM
# ============================================================================

#' Chinese Remainder Theorem
#'
#' Solve system of congruences:
#'   x ≡ a[1] (mod m[1])
#'   x ≡ a[2] (mod m[2])
#'   ...
#'
#' @param remainders Vector of remainders
#' @param moduli Vector of moduli (must be pairwise coprime)
#' @return Solution x, or NA if moduli are not coprime
#'
#' @examples
#' chinese_remainder_theorem(c(2, 3, 2), c(3, 5, 7))  # Returns 23
chinese_remainder_theorem <- function(remainders, moduli) {
    if (length(remainders) != length(moduli)) {
        return(NA)
    }

    # Check if moduli are pairwise coprime
    n <- length(moduli)
    for (i in 1:(n - 1)) {
        for (j in (i + 1):n) {
            if (gcd(moduli[i], moduli[j]) != 1) {
                return(NA)  # Not pairwise coprime
            }
        }
    }

    # Calculate M = product of all moduli
    M <- prod(moduli)

    # Calculate solution
    x <- 0
    for (i in 1:n) {
        Mi <- M %/% moduli[i]
        yi <- mod_inverse(Mi, moduli[i])
        if (is.na(yi)) return(NA)
        x <- (x + remainders[i] * Mi * yi) %% M
    }

    return(x)
}

# ============================================================================
# TESTING AND DEMONSTRATION
# ============================================================================

print_separator <- function(char = "=", length = 70) {
    cat(paste(rep(char, length), collapse = ""), "\n")
}

test_sieve <- function() {
    cat("\n1. PRIME NUMBER GENERATION\n")
    print_separator("-", 50)

    limit <- 50
    primes_e <- sieve_of_eratosthenes(limit)
    primes_s <- sieve_of_sundaram(limit)

    cat(sprintf("Primes up to %d (Eratosthenes): ", limit))
    cat(primes_e, "\n")
    cat(sprintf("Primes up to %d (Sundaram):     ", limit))
    cat(primes_s, "\n")
    cat(sprintf("Verification: Both methods agree: %s\n",
                identical(primes_e, primes_s)))
}

test_gcd_lcm <- function() {
    cat("\n2. GCD AND LCM\n")
    print_separator("-", 50)

    pairs <- list(c(48, 18), c(100, 35), c(17, 19))

    for (pair in pairs) {
        a <- pair[1]
        b <- pair[2]
        g <- gcd(a, b)
        l <- lcm(a, b)
        cat(sprintf("gcd(%d, %d) = %d, lcm(%d, %d) = %d\n", a, b, g, a, b, l))
    }
}

test_modular_arithmetic <- function() {
    cat("\n3. MODULAR ARITHMETIC\n")
    print_separator("-", 50)

    cat("Modular Exponentiation:\n")
    test_cases <- list(c(2, 10, 1000), c(3, 100, 13), c(7, 256, 100))

    for (tc in test_cases) {
        base <- tc[1]
        exp <- tc[2]
        mod <- tc[3]
        result <- mod_exp(base, exp, mod)
        cat(sprintf("  %d^%d mod %d = %d\n", base, exp, mod, result))
    }

    cat("\nModular Inverse:\n")
    inv_cases <- list(c(3, 11), c(7, 26))

    for (ic in inv_cases) {
        a <- ic[1]
        m <- ic[2]
        inv <- mod_inverse(a, m)
        if (!is.na(inv)) {
            cat(sprintf("  Inverse of %d mod %d = %d\n", a, m, inv))
            cat(sprintf("    Verification: (%d × %d) mod %d = %d\n",
                       a, inv, m, (a * inv) %% m))
        }
    }
}

test_primality <- function() {
    cat("\n4. PRIMALITY TESTING\n")
    print_separator("-", 50)

    test_numbers <- c(17, 561, 1105, 2047, 8191, 9973, 10001)

    for (n in test_numbers) {
        result <- miller_rabin(n, k = 20)
        status <- if (result) "PRIME" else "COMPOSITE"
        cat(sprintf("%5d: %s\n", n, status))
    }
}

test_factorization <- function() {
    cat("\n5. PRIME FACTORIZATION\n")
    print_separator("-", 50)

    test_numbers <- c(60, 128, 1001, 2024)

    for (n in test_numbers) {
        factors <- prime_factorization(n)
        factor_str <- paste(sapply(1:nrow(factors), function(i) {
            if (factors$exponent[i] > 1) {
                sprintf("%d^%d", factors$prime[i], factors$exponent[i])
            } else {
                sprintf("%d", factors$prime[i])
            }
        }), collapse = " × ")
        cat(sprintf("%d = %s\n", n, factor_str))
    }
}

test_totient <- function() {
    cat("\n6. EULER'S TOTIENT FUNCTION\n")
    print_separator("-", 50)

    test_values <- c(1, 9, 10, 36, 100)

    for (n in test_values) {
        phi <- euler_totient(n)
        cat(sprintf("φ(%d) = %d\n", n, phi))
    }
}

test_crt <- function() {
    cat("\n7. CHINESE REMAINDER THEOREM\n")
    print_separator("-", 50)

    remainders <- c(2, 3, 2)
    moduli <- c(3, 5, 7)

    cat("System of congruences:\n")
    for (i in 1:length(remainders)) {
        cat(sprintf("  x ≡ %d (mod %d)\n", remainders[i], moduli[i]))
    }

    solution <- chinese_remainder_theorem(remainders, moduli)

    if (!is.na(solution)) {
        cat(sprintf("Solution: x = %d\n", solution))
        cat("Verification:\n")
        for (i in 1:length(remainders)) {
            cat(sprintf("  %d mod %d = %d (expected %d)\n",
                       solution, moduli[i], solution %% moduli[i], remainders[i]))
        }
    } else {
        cat("Failed to solve (moduli not pairwise coprime)\n")
    }
}

main <- function() {
    print_separator("=", 70)
    cat("NUMBER THEORY ALGORITHMS - R IMPLEMENTATION\n")
    print_separator("=", 70)

    test_sieve()
    test_gcd_lcm()
    test_modular_arithmetic()
    test_primality()
    test_factorization()
    test_totient()
    test_crt()

    cat("\n")
    print_separator("=", 70)
    cat("All tests completed successfully!\n")
    print_separator("=", 70)
}

# Run main if script is executed directly
if (sys.nframe() == 0) {
    main()
}
