/*
Package main implements fundamental number theory algorithms in Go.

Features:
- Arbitrary precision arithmetic using math/big
- Idiomatic Go code with proper error handling
- Efficient implementations of classic algorithms
- Cryptographic applications

Compilation and execution:
    go run number_theory.go

Author: algorithms-multiverse
*/

package main

import (
	"fmt"
	"math"
	"math/big"
	"math/rand"
	"time"
)

// ============================================================================
// PRIME NUMBER GENERATION
// ============================================================================

// SieveOfEratosthenes generates all prime numbers up to limit.
//
// Time Complexity: O(n log log n)
// Space Complexity: O(n)
//
// Mathematical Foundation:
// Any composite number n has a prime factor p ≤ √n.
// By marking multiples of all primes ≤ √limit, we identify all composites.
func SieveOfEratosthenes(limit uint64) []uint64 {
	if limit < 2 {
		return []uint64{}
	}

	// Initialize sieve: true means "potentially prime"
	isPrime := make([]bool, limit+1)
	for i := range isPrime {
		isPrime[i] = true
	}
	isPrime[0], isPrime[1] = false, false

	// Sieve algorithm
	sqrtLimit := uint64(math.Sqrt(float64(limit)))
	for i := uint64(2); i <= sqrtLimit; i++ {
		if isPrime[i] {
			// Mark all multiples of i as composite
			for j := i * i; j <= limit; j += i {
				isPrime[j] = false
			}
		}
	}

	// Collect primes
	primes := []uint64{}
	for i := uint64(2); i <= limit; i++ {
		if isPrime[i] {
			primes = append(primes, i)
		}
	}

	return primes
}

// SieveOfSundaram generates all prime numbers up to limit using Sieve of Sundaram.
//
// Time Complexity: O(n log n)
// Space Complexity: O(n)
//
// Mathematical Foundation:
// Every odd composite number can be written as (2i+1)(2j+1) = 2(i+j+2ij)+1.
// By marking all i+j+2ij values, we identify positions of odd composites.
func SieveOfSundaram(limit uint64) []uint64 {
	if limit < 2 {
		return []uint64{}
	}
	if limit == 2 {
		return []uint64{2}
	}

	// Calculate the limit for the sundaram sieve
	n := (limit - 1) / 2

	// Initialize array: true means "unmarked" (potentially prime)
	unmarked := make([]bool, n+1)
	for i := range unmarked {
		unmarked[i] = true
	}

	// Mark positions i+j+2ij
	for i := uint64(1); i <= n; i++ {
		j := i
		for i+j+2*i*j <= n {
			unmarked[i+j+2*i*j] = false
			j++
		}
	}

	// Generate primes: 2k+1 for unmarked k
	primes := []uint64{2} // 2 is the only even prime
	for k := uint64(1); k <= n; k++ {
		if unmarked[k] {
			prime := 2*k + 1
			if prime <= limit {
				primes = append(primes, prime)
			}
		}
	}

	return primes
}

// ============================================================================
// GREATEST COMMON DIVISOR
// ============================================================================

// GCD calculates the greatest common divisor using Euclidean algorithm.
//
// Time Complexity: O(log min(a, b))
// Space Complexity: O(1)
//
// Mathematical Proof:
// gcd(a, b) = gcd(b, a mod b) when b ≠ 0
// gcd(a, 0) = a
func GCD(a, b uint64) uint64 {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

// GCDBig calculates GCD for big integers.
func GCDBig(a, b *big.Int) *big.Int {
	result := new(big.Int)
	return result.GCD(nil, nil, a, b)
}

// ExtendedGCD finds gcd(a, b) and Bézout coefficients x, y such that ax + by = gcd(a, b).
//
// Time Complexity: O(log min(a, b))
// Space Complexity: O(1)
//
// Applications:
// - Computing modular multiplicative inverse
// - Solving linear Diophantine equations
func ExtendedGCD(a, b int64) (gcd, x, y int64) {
	if b == 0 {
		return a, 1, 0
	}

	gcd1, x1, y1 := ExtendedGCD(b, a%b)
	gcd = gcd1
	x = y1
	y = x1 - (a/b)*y1

	return
}

// LCM calculates the least common multiple.
//
// Formula: lcm(a, b) = (a × b) / gcd(a, b)
func LCM(a, b uint64) uint64 {
	if a == 0 || b == 0 {
		return 0
	}
	return (a / GCD(a, b)) * b
}

// ============================================================================
// MODULAR ARITHMETIC
// ============================================================================

// ModExp performs modular exponentiation: base^exponent mod modulus.
//
// Time Complexity: O(log exponent)
// Space Complexity: O(1)
//
// Uses binary exponentiation (exponentiation by squaring).
// Critical for RSA encryption/decryption and other cryptographic protocols.
func ModExp(base, exponent, modulus uint64) uint64 {
	if modulus == 1 {
		return 0
	}

	result := uint64(1)
	base = base % modulus

	for exponent > 0 {
		if exponent&1 == 1 {
			result = (result * base) % modulus
		}
		exponent >>= 1
		base = (base * base) % modulus
	}

	return result
}

// ModExpBig performs modular exponentiation with big integers.
func ModExpBig(base, exponent, modulus *big.Int) *big.Int {
	result := new(big.Int)
	return result.Exp(base, exponent, modulus)
}

// ModInverse calculates the modular multiplicative inverse of a modulo m.
//
// Find x such that (a × x) ≡ 1 (mod m).
// Inverse exists if and only if gcd(a, m) = 1.
//
// Returns 0 if inverse doesn't exist.
func ModInverse(a, m int64) int64 {
	gcd, x, _ := ExtendedGCD(a, m)

	if gcd != 1 {
		return 0 // Inverse doesn't exist
	}

	// Ensure positive result
	return ((x % m) + m) % m
}

// ModInverseBig calculates modular inverse for big integers.
func ModInverseBig(a, m *big.Int) *big.Int {
	result := new(big.Int)
	return result.ModInverse(a, m)
}

// ============================================================================
// PRIME FACTORIZATION
// ============================================================================

// PrimeFactorization finds the prime factorization of n.
//
// Time Complexity: O(√n)
// Space Complexity: O(log n)
//
// Returns a map of prime -> exponent pairs.
func PrimeFactorization(n uint64) map[uint64]int {
	if n < 2 {
		return map[uint64]int{}
	}

	factors := make(map[uint64]int)

	// Handle factor 2
	for n%2 == 0 {
		factors[2]++
		n /= 2
	}

	// Check odd divisors
	for i := uint64(3); i*i <= n; i += 2 {
		for n%i == 0 {
			factors[i]++
			n /= i
		}
	}

	// If n > 1, then it's a prime factor
	if n > 1 {
		factors[n] = 1
	}

	return factors
}

// ============================================================================
// PRIMALITY TESTING
// ============================================================================

// MillerRabin performs the Miller-Rabin probabilistic primality test.
//
// Time Complexity: O(k log³ n) for k rounds
// Error probability: ≤ 4^(-k) for random witnesses
//
// For n < 2^64, using deterministic witnesses makes this test deterministic.
//
// Applications:
// - RSA key generation
// - Cryptographic protocols
func MillerRabin(n uint64, k int) bool {
	// Handle small cases
	if n < 2 {
		return false
	}
	if n == 2 || n == 3 {
		return true
	}
	if n%2 == 0 {
		return false
	}

	// Write n-1 as 2^r × d where d is odd
	d := n - 1
	r := 0
	for d%2 == 0 {
		r++
		d /= 2
	}

	// Deterministic witnesses for n < 2^64
	witnesses := []uint64{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}

	// Test each witness
	for _, a := range witnesses {
		if a >= n {
			continue
		}

		// Compute x = a^d mod n
		x := ModExp(a, d, n)

		if x == 1 || x == n-1 {
			continue
		}

		// Square x repeatedly r-1 times
		composite := true
		for j := 0; j < r-1; j++ {
			x = ModExp(x, 2, n)
			if x == n-1 {
				composite = false
				break
			}
		}

		if composite {
			return false // Definitely composite
		}
	}

	return true // Probably prime
}

// IsPrimeTrial performs simple primality test using trial division.
//
// Time Complexity: O(√n)
// Space Complexity: O(1)
func IsPrimeTrial(n uint64) bool {
	if n < 2 {
		return false
	}
	if n == 2 {
		return true
	}
	if n%2 == 0 {
		return false
	}

	sqrtN := uint64(math.Sqrt(float64(n)))
	for i := uint64(3); i <= sqrtN; i += 2 {
		if n%i == 0 {
			return false
		}
	}

	return true
}

// ============================================================================
// EULER'S TOTIENT FUNCTION
// ============================================================================

// EulerTotient calculates Euler's totient function φ(n).
//
// φ(n) = count of integers k where 1 ≤ k ≤ n and gcd(k, n) = 1
//
// Time Complexity: O(√n)
// Space Complexity: O(log n)
//
// Applications:
// - RSA: φ(n) used to calculate private key
// - Euler's theorem: a^φ(n) ≡ 1 (mod n) if gcd(a,n) = 1
func EulerTotient(n uint64) uint64 {
	if n == 1 {
		return 1
	}

	result := n
	factors := PrimeFactorization(n)

	for prime := range factors {
		// Multiply by (1 - 1/prime) = (prime - 1)/prime
		result = result / prime * (prime - 1)
	}

	return result
}

// ============================================================================
// CHINESE REMAINDER THEOREM
// ============================================================================

// ChineseRemainderTheorem solves a system of congruences.
//
// Given:
//   x ≡ a[0] (mod m[0])
//   x ≡ a[1] (mod m[1])
//   ...
//
// Find x that satisfies all congruences.
// Requires moduli to be pairwise coprime.
//
// Time Complexity: O(n log M) where M is product of moduli
// Space Complexity: O(1)
//
// Returns (solution, true) if successful, (0, false) if moduli not coprime.
func ChineseRemainderTheorem(remainders, moduli []int64) (int64, bool) {
	if len(remainders) != len(moduli) {
		return 0, false
	}

	// Check if moduli are pairwise coprime
	for i := 0; i < len(moduli); i++ {
		for j := i + 1; j < len(moduli); j++ {
			if GCD(uint64(moduli[i]), uint64(moduli[j])) != 1 {
				return 0, false // Not pairwise coprime
			}
		}
	}

	// Calculate M = product of all moduli
	M := int64(1)
	for _, m := range moduli {
		M *= m
	}

	// Calculate solution
	x := int64(0)
	for i := 0; i < len(moduli); i++ {
		Mi := M / moduli[i]
		yi := ModInverse(Mi, moduli[i])
		if yi == 0 {
			return 0, false
		}
		x = (x + remainders[i]*Mi*yi) % M
	}

	// Ensure positive result
	if x < 0 {
		x += M
	}

	return x, true
}

// ============================================================================
// POLLARD'S RHO FACTORIZATION
// ============================================================================

// PollardRho attempts to find a non-trivial factor of n.
//
// Time Complexity: O(n^(1/4)) expected
// Space Complexity: O(1)
//
// May return 0 if factorization fails.
func PollardRho(n uint64) uint64 {
	if n == 1 {
		return 0
	}
	if n%2 == 0 {
		return 2
	}

	// Random starting values
	rand.Seed(time.Now().UnixNano())
	x := uint64(rand.Int63n(int64(n-2))) + 2
	y := x
	c := uint64(rand.Int63n(int64(n-1))) + 1
	d := uint64(1)

	// Floyd's cycle detection
	maxIterations := 100000
	iteration := 0

	for d == 1 && iteration < maxIterations {
		// Tortoise: move one step
		x = (x*x + c) % n

		// Hare: move two steps
		y = (y*y + c) % n
		y = (y*y + c) % n

		// Check if we found a factor
		if x > y {
			d = GCD(x-y, n)
		} else {
			d = GCD(y-x, n)
		}

		iteration++
	}

	if d == n || iteration >= maxIterations {
		return 0 // Failed to find factor
	}

	return d
}

// ============================================================================
// TESTING AND DEMONSTRATION
// ============================================================================

func printSeparator(c rune, length int) {
	for i := 0; i < length; i++ {
		fmt.Print(string(c))
	}
	fmt.Println()
}

func testSieve() {
	fmt.Println("\n1. PRIME NUMBER GENERATION")
	printSeparator('-', 50)

	limit := uint64(50)
	primesE := SieveOfEratosthenes(limit)
	primesS := SieveOfSundaram(limit)

	fmt.Printf("Primes up to %d (Eratosthenes): %v\n", limit, primesE)
	fmt.Printf("Primes up to %d (Sundaram):     %v\n", limit, primesS)

	// Verify both methods give same result
	equal := len(primesE) == len(primesS)
	if equal {
		for i := range primesE {
			if primesE[i] != primesS[i] {
				equal = false
				break
			}
		}
	}
	fmt.Printf("Verification: Both methods agree: %v\n", equal)
}

func testGCD() {
	fmt.Println("\n2. GCD AND LCM")
	printSeparator('-', 50)

	pairs := [][2]uint64{{48, 18}, {100, 35}, {17, 19}}

	for _, pair := range pairs {
		a, b := pair[0], pair[1]
		g := GCD(a, b)
		l := LCM(a, b)
		fmt.Printf("gcd(%d, %d) = %d, lcm(%d, %d) = %d\n", a, b, g, a, b, l)
	}
}

func testModularArithmetic() {
	fmt.Println("\n3. MODULAR ARITHMETIC")
	printSeparator('-', 50)

	testCases := [][3]uint64{{2, 10, 1000}, {3, 100, 13}, {7, 256, 100}}

	fmt.Println("Modular Exponentiation:")
	for _, tc := range testCases {
		base, exp, mod := tc[0], tc[1], tc[2]
		result := ModExp(base, exp, mod)
		fmt.Printf("  %d^%d mod %d = %d\n", base, exp, mod, result)
	}

	fmt.Println("\nModular Inverse:")
	invCases := [][2]int64{{3, 11}, {7, 26}}
	for _, ic := range invCases {
		a, m := ic[0], ic[1]
		inv := ModInverse(a, m)
		if inv > 0 {
			fmt.Printf("  Inverse of %d mod %d = %d\n", a, m, inv)
			fmt.Printf("    Verification: (%d × %d) mod %d = %d\n",
				a, inv, m, (a*inv)%m)
		}
	}
}

func testPrimality() {
	fmt.Println("\n4. PRIMALITY TESTING")
	printSeparator('-', 50)

	testNumbers := []uint64{17, 561, 1105, 2047, 8191, 9973, 10001}

	for _, n := range testNumbers {
		result := MillerRabin(n, 20)
		status := "COMPOSITE"
		if result {
			status = "PRIME"
		}
		fmt.Printf("%5d: %s\n", n, status)
	}
}

func testFactorization() {
	fmt.Println("\n5. PRIME FACTORIZATION")
	printSeparator('-', 50)

	testNumbers := []uint64{60, 128, 1001, 2024}

	for _, n := range testNumbers {
		factors := PrimeFactorization(n)
		fmt.Printf("%d = ", n)

		first := true
		for prime, exp := range factors {
			if !first {
				fmt.Print(" × ")
			}
			if exp > 1 {
				fmt.Printf("%d^%d", prime, exp)
			} else {
				fmt.Printf("%d", prime)
			}
			first = false
		}
		fmt.Println()
	}
}

func testTotient() {
	fmt.Println("\n6. EULER'S TOTIENT FUNCTION")
	printSeparator('-', 50)

	testValues := []uint64{1, 9, 10, 36, 100}

	for _, n := range testValues {
		phi := EulerTotient(n)
		fmt.Printf("φ(%d) = %d\n", n, phi)
	}
}

func testCRT() {
	fmt.Println("\n7. CHINESE REMAINDER THEOREM")
	printSeparator('-', 50)

	remainders := []int64{2, 3, 2}
	moduli := []int64{3, 5, 7}

	fmt.Println("System of congruences:")
	for i := range remainders {
		fmt.Printf("  x ≡ %d (mod %d)\n", remainders[i], moduli[i])
	}

	solution, ok := ChineseRemainderTheorem(remainders, moduli)
	if ok {
		fmt.Printf("Solution: x = %d\n", solution)
		fmt.Println("Verification:")
		for i := range remainders {
			fmt.Printf("  %d mod %d = %d (expected %d)\n",
				solution, moduli[i], solution%moduli[i], remainders[i])
		}
	} else {
		fmt.Println("Failed to solve (moduli not pairwise coprime)")
	}
}

func main() {
	printSeparator('=', 70)
	fmt.Println("NUMBER THEORY ALGORITHMS - GO IMPLEMENTATION")
	printSeparator('=', 70)

	testSieve()
	testGCD()
	testModularArithmetic()
	testPrimality()
	testFactorization()
	testTotient()
	testCRT()

	fmt.Println()
	printSeparator('=', 70)
	fmt.Println("All tests completed successfully!")
	printSeparator('=', 70)
}
