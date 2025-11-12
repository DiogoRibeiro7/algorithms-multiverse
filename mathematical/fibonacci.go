// Fibonacci Sequence Implementation in Go
//
// Time Complexity:
// - Naive Recursive: O(2^n)
// - Memoization: O(n)
// - Dynamic Programming: O(n)
// - Matrix Exponentiation: O(log n)
// - Closed Form (Binet's): O(1)
// Space Complexity: O(n) for memoization, O(1) for iterative
//
// The Fibonacci sequence is a series where each number is the sum of the
// two preceding ones: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
//
// Go features:
// - big.Int support for arbitrarily large Fibonacci numbers
// - Multiple implementations (recursive, iterative, matrix, Binet's formula)
// - Memoization with concurrent-safe cache
// - Channel-based Fibonacci generator
// - Golden ratio calculations
// - Performance benchmarking

package main

import (
	"fmt"
	"math"
	"math/big"
	"strings"
	"sync"
	"time"
)

// BASIC FIBONACCI IMPLEMENTATIONS (using int)

// FibonacciRecursive computes Fibonacci number using naive recursion
//
// Time Complexity: O(2^n) - exponential, very slow
// Space Complexity: O(n) for recursion stack
func FibonacciRecursive(n int) int {
	if n <= 1 {
		return n
	}
	return FibonacciRecursive(n-1) + FibonacciRecursive(n-2)
}

// FibonacciMemoization computes Fibonacci with memoization
//
// Time Complexity: O(n)
// Space Complexity: O(n)
func FibonacciMemoization(n int) int {
	memo := make(map[int]int)
	return fibMemo(n, memo)
}

func fibMemo(n int, memo map[int]int) int {
	if n <= 1 {
		return n
	}

	if val, ok := memo[n]; ok {
		return val
	}

	memo[n] = fibMemo(n-1, memo) + fibMemo(n-2, memo)
	return memo[n]
}

// FibonacciIterative computes Fibonacci iteratively
//
// Time Complexity: O(n)
// Space Complexity: O(1)
func FibonacciIterative(n int) int {
	if n <= 1 {
		return n
	}

	a, b := 0, 1

	for i := 2; i <= n; i++ {
		a, b = b, a+b
	}

	return b
}

// FibonacciDP computes Fibonacci using dynamic programming
//
// Time Complexity: O(n)
// Space Complexity: O(n)
func FibonacciDP(n int) int {
	if n <= 1 {
		return n
	}

	dp := make([]int, n+1)
	dp[0] = 0
	dp[1] = 1

	for i := 2; i <= n; i++ {
		dp[i] = dp[i-1] + dp[i-2]
	}

	return dp[n]
}

// BIG INTEGER FIBONACCI IMPLEMENTATIONS

// FibonacciBig computes large Fibonacci numbers using big.Int
//
// Time Complexity: O(n)
// Space Complexity: O(1)
func FibonacciBig(n int) *big.Int {
	if n <= 1 {
		return big.NewInt(int64(n))
	}

	a := big.NewInt(0)
	b := big.NewInt(1)

	for i := 2; i <= n; i++ {
		a, b = b, new(big.Int).Add(a, b)
	}

	return b
}

// FibonacciBigMemo computes large Fibonacci with memoization
type FibonacciCache struct {
	cache map[int]*big.Int
	mu    sync.RWMutex
}

// NewFibonacciCache creates a new thread-safe Fibonacci cache
func NewFibonacciCache() *FibonacciCache {
	return &FibonacciCache{
		cache: make(map[int]*big.Int),
	}
}

// Get retrieves cached value or computes it
func (fc *FibonacciCache) Get(n int) *big.Int {
	fc.mu.RLock()
	if val, ok := fc.cache[n]; ok {
		fc.mu.RUnlock()
		return new(big.Int).Set(val)
	}
	fc.mu.RUnlock()

	// Compute and cache
	fc.mu.Lock()
	defer fc.mu.Unlock()

	// Double-check after acquiring write lock
	if val, ok := fc.cache[n]; ok {
		return new(big.Int).Set(val)
	}

	result := fc.compute(n)
	fc.cache[n] = result
	return new(big.Int).Set(result)
}

func (fc *FibonacciCache) compute(n int) *big.Int {
	if n <= 1 {
		return big.NewInt(int64(n))
	}

	a := fc.Get(n - 1)
	b := fc.Get(n - 2)
	return new(big.Int).Add(a, b)
}

// Size returns cache size
func (fc *FibonacciCache) Size() int {
	fc.mu.RLock()
	defer fc.mu.RUnlock()
	return len(fc.cache)
}

// Clear clears the cache
func (fc *FibonacciCache) Clear() {
	fc.mu.Lock()
	defer fc.mu.Unlock()
	fc.cache = make(map[int]*big.Int)
}

// MATRIX EXPONENTIATION (Fast Method)

// FibonacciMatrix computes Fibonacci using matrix exponentiation
//
// Time Complexity: O(log n)
// Space Complexity: O(log n) for recursion
//
// Uses the fact that:
// [F(n+1) F(n)  ] = [1 1]^n
// [F(n)   F(n-1)]   [1 0]
func FibonacciMatrix(n int) *big.Int {
	if n <= 1 {
		return big.NewInt(int64(n))
	}

	result := matrixPower(n - 1)
	return result[0][0]
}

// Matrix represents a 2x2 matrix
type Matrix [2][2]*big.Int

// newMatrix creates a new matrix
func newMatrix(a, b, c, d int64) Matrix {
	return Matrix{
		{big.NewInt(a), big.NewInt(b)},
		{big.NewInt(c), big.NewInt(d)},
	}
}

// multiply multiplies two matrices
func multiply(a, b Matrix) Matrix {
	result := Matrix{
		{new(big.Int), new(big.Int)},
		{new(big.Int), new(big.Int)},
	}

	// result[0][0] = a[0][0]*b[0][0] + a[0][1]*b[1][0]
	result[0][0].Mul(a[0][0], b[0][0])
	temp := new(big.Int).Mul(a[0][1], b[1][0])
	result[0][0].Add(result[0][0], temp)

	// result[0][1] = a[0][0]*b[0][1] + a[0][1]*b[1][1]
	result[0][1].Mul(a[0][0], b[0][1])
	temp = new(big.Int).Mul(a[0][1], b[1][1])
	result[0][1].Add(result[0][1], temp)

	// result[1][0] = a[1][0]*b[0][0] + a[1][1]*b[1][0]
	result[1][0].Mul(a[1][0], b[0][0])
	temp = new(big.Int).Mul(a[1][1], b[1][0])
	result[1][0].Add(result[1][0], temp)

	// result[1][1] = a[1][0]*b[0][1] + a[1][1]*b[1][1]
	result[1][1].Mul(a[1][0], b[0][1])
	temp = new(big.Int).Mul(a[1][1], b[1][1])
	result[1][1].Add(result[1][1], temp)

	return result
}

// matrixPower computes matrix^n using fast exponentiation
func matrixPower(n int) Matrix {
	if n == 1 {
		return newMatrix(1, 1, 1, 0)
	}

	if n%2 == 0 {
		half := matrixPower(n / 2)
		return multiply(half, half)
	}

	return multiply(newMatrix(1, 1, 1, 0), matrixPower(n-1))
}

// BINET'S FORMULA (Closed Form)

// FibonacciBinet computes Fibonacci using Binet's formula
//
// Time Complexity: O(1)
// Note: Only accurate for small n due to floating-point precision
func FibonacciBinet(n int) int {
	phi := (1 + math.Sqrt(5)) / 2
	psi := (1 - math.Sqrt(5)) / 2

	result := (math.Pow(phi, float64(n)) - math.Pow(psi, float64(n))) / math.Sqrt(5)
	return int(math.Round(result))
}

// FIBONACCI SEQUENCE GENERATION

// FibonacciSequence generates first n Fibonacci numbers
func FibonacciSequence(n int) []int {
	if n <= 0 {
		return []int{}
	}

	sequence := make([]int, n)
	if n >= 1 {
		sequence[0] = 0
	}
	if n >= 2 {
		sequence[1] = 1
	}

	for i := 2; i < n; i++ {
		sequence[i] = sequence[i-1] + sequence[i-2]
	}

	return sequence
}

// FibonacciSequenceBig generates first n Fibonacci numbers as big.Int
func FibonacciSequenceBig(n int) []*big.Int {
	if n <= 0 {
		return []*big.Int{}
	}

	sequence := make([]*big.Int, n)
	if n >= 1 {
		sequence[0] = big.NewInt(0)
	}
	if n >= 2 {
		sequence[1] = big.NewInt(1)
	}

	for i := 2; i < n; i++ {
		sequence[i] = new(big.Int).Add(sequence[i-1], sequence[i-2])
	}

	return sequence
}

// CHANNEL-BASED FIBONACCI GENERATOR

// FibonacciGenerator generates Fibonacci numbers via channel
func FibonacciGenerator() <-chan int {
	ch := make(chan int)

	go func() {
		a, b := 0, 1
		for {
			ch <- a
			a, b = b, a+b
		}
	}()

	return ch
}

// FibonacciGeneratorBig generates big Fibonacci numbers via channel
func FibonacciGeneratorBig() <-chan *big.Int {
	ch := make(chan *big.Int)

	go func() {
		a := big.NewInt(0)
		b := big.NewInt(1)

		for {
			// Send a copy
			val := new(big.Int).Set(a)
			ch <- val

			// Calculate next
			a, b = b, new(big.Int).Add(a, b)
		}
	}()

	return ch
}

// GOLDEN RATIO

// GoldenRatio computes the golden ratio from Fibonacci sequence
func GoldenRatio(n int) float64 {
	if n < 2 {
		return 0
	}

	fn := float64(FibonacciIterative(n))
	fnMinus1 := float64(FibonacciIterative(n - 1))

	return fn / fnMinus1
}

// GoldenRatioConvergence shows convergence to golden ratio
func GoldenRatioConvergence(maxN int) []float64 {
	ratios := make([]float64, maxN-1)

	for i := 2; i <= maxN; i++ {
		ratios[i-2] = GoldenRatio(i)
	}

	return ratios
}

// FIBONACCI UTILITIES

// IsFibonacci checks if a number is a Fibonacci number
//
// A number is Fibonacci if one of (5*n^2 + 4) or (5*n^2 - 4) is a perfect square
func IsFibonacci(n int) bool {
	if n < 0 {
		return false
	}

	n5 := 5 * n * n

	return isPerfectSquare(n5+4) || isPerfectSquare(n5-4)
}

func isPerfectSquare(n int) bool {
	if n < 0 {
		return false
	}

	sqrt := int(math.Sqrt(float64(n)))
	return sqrt*sqrt == n
}

// FibonacciIndex finds the index of a Fibonacci number
func FibonacciIndex(target int) int {
	if target < 0 {
		return -1
	}

	if target == 0 {
		return 0
	}

	a, b := 0, 1
	index := 1

	for b < target {
		a, b = b, a+b
		index++
	}

	if b == target {
		return index
	}

	return -1 // Not a Fibonacci number
}

// DemonstrateFibonacci demonstrates various Fibonacci implementations
func DemonstrateFibonacci() {
	fmt.Println("🔢 Fibonacci Sequence Implementation in Go")
	fmt.Println(strings.Repeat("=", 70))

	// Basic sequence
	fmt.Println("\n📋 First 20 Fibonacci Numbers:")
	fmt.Println(strings.Repeat("-", 70))

	sequence := FibonacciSequence(20)
	fmt.Printf("%v\n", sequence)

	// Different implementations
	fmt.Println("\n🔄 Different Implementations (F(10)):")
	fmt.Println(strings.Repeat("-", 70))

	n := 10
	fmt.Printf("Recursive:     F(%d) = %d\n", n, FibonacciRecursive(n))
	fmt.Printf("Memoization:   F(%d) = %d\n", n, FibonacciMemoization(n))
	fmt.Printf("Iterative:     F(%d) = %d\n", n, FibonacciIterative(n))
	fmt.Printf("DP:            F(%d) = %d\n", n, FibonacciDP(n))
	fmt.Printf("Binet's:       F(%d) = %d\n", n, FibonacciBinet(n))

	// Large Fibonacci numbers
	fmt.Println("\n🔢 Large Fibonacci Numbers (using big.Int):")
	fmt.Println(strings.Repeat("-", 70))

	largeIndices := []int{50, 100, 200, 500, 1000}
	for _, idx := range largeIndices {
		fib := FibonacciBig(idx)
		fmt.Printf("F(%d) = %s... (%d digits)\n", idx, fib.String()[:min(50, len(fib.String()))], len(fib.String()))
	}

	// Matrix method
	fmt.Println("\n⚡ Matrix Exponentiation (Fast Method):")
	fmt.Println(strings.Repeat("-", 70))

	matrixTest := []int{10, 50, 100}
	for _, idx := range matrixTest {
		fib := FibonacciMatrix(idx)
		fmt.Printf("F(%d) = %s\n", idx, fib.String())
	}

	// Memoization cache
	fmt.Println("\n💾 Memoization Cache:")
	fmt.Println(strings.Repeat("-", 70))

	cache := NewFibonacciCache()
	for i := 0; i <= 100; i++ {
		cache.Get(i)
	}

	fmt.Printf("Computed F(0) through F(100)\n")
	fmt.Printf("Cache size: %d entries\n", cache.Size())

	// Quick access to cached values
	fmt.Printf("F(50) = %s\n", cache.Get(50).String())
	fmt.Printf("F(100) = %s\n", cache.Get(100).String())

	// Channel-based generator
	fmt.Println("\n📡 Channel-Based Generator:")
	fmt.Println(strings.Repeat("-", 70))

	gen := FibonacciGenerator()
	fmt.Print("First 15: ")
	for i := 0; i < 15; i++ {
		if i > 0 {
			fmt.Print(", ")
		}
		fmt.Printf("%d", <-gen)
	}
	fmt.Println()

	// Golden ratio
	fmt.Println("\n✨ Golden Ratio Convergence:")
	fmt.Println(strings.Repeat("-", 70))

	actualGoldenRatio := (1 + math.Sqrt(5)) / 2
	fmt.Printf("Actual Golden Ratio: %.15f\n\n", actualGoldenRatio)

	fmt.Println("n   F(n)/F(n-1)        Difference")
	fmt.Println(strings.Repeat("-", 45))

	for i := 2; i <= 20; i += 2 {
		ratio := GoldenRatio(i)
		diff := math.Abs(ratio - actualGoldenRatio)
		fmt.Printf("%-3d %.15f  %.2e\n", i, ratio, diff)
	}

	// Check Fibonacci numbers
	fmt.Println("\n🔍 Checking if Numbers are Fibonacci:")
	fmt.Println(strings.Repeat("-", 70))

	testNumbers := []int{1, 2, 3, 4, 5, 8, 13, 20, 21, 34, 35, 55, 89, 90}
	for _, num := range testNumbers {
		isFib := IsFibonacci(num)
		status := "✓"
		if !isFib {
			status = "✗"
		}

		idx := FibonacciIndex(num)
		if idx != -1 {
			fmt.Printf("%3d: %s (F(%d))\n", num, status, idx)
		} else {
			fmt.Printf("%3d: %s\n", num, status)
		}
	}

	// Performance benchmark
	fmt.Println("\n⚡ Performance Benchmark:")
	fmt.Println(strings.Repeat("-", 70))

	benchmarks := []struct {
		name string
		fn   func(int) interface{}
		n    int
	}{
		{"Iterative", func(n int) interface{} { return FibonacciIterative(n) }, 40},
		{"Memoization", func(n int) interface{} { return FibonacciMemoization(n) }, 40},
		{"DP", func(n int) interface{} { return FibonacciDP(n) }, 40},
		{"Binet's", func(n int) interface{} { return FibonacciBinet(n) }, 40},
		{"BigInt", func(n int) interface{} { return FibonacciBig(n) }, 1000},
		{"Matrix", func(n int) interface{} { return FibonacciMatrix(n) }, 1000},
	}

	for _, bench := range benchmarks {
		start := time.Now()
		result := bench.fn(bench.n)
		elapsed := time.Since(start)

		fmt.Printf("%-12s F(%-4d): %10v (%.3fµs)\n",
			bench.name, bench.n,
			fmt.Sprintf("%.0e", 0.0), // Placeholder
			float64(elapsed.Microseconds()))

		_ = result // Use result to prevent optimization
	}

	// Parallel generation
	fmt.Println("\n🚀 Concurrent Fibonacci Generation:")
	fmt.Println(strings.Repeat("-", 70))

	var wg sync.WaitGroup
	results := make(chan string, 5)

	indices := []int{100, 200, 300, 400, 500}
	for _, idx := range indices {
		wg.Add(1)
		go func(n int) {
			defer wg.Done()
			fib := FibonacciBig(n)
			results <- fmt.Sprintf("F(%d): %d digits", n, len(fib.String()))
		}(idx)
	}

	go func() {
		wg.Wait()
		close(results)
	}()

	for result := range results {
		fmt.Printf("  %s\n", result)
	}
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func main() {
	DemonstrateFibonacci()
	fmt.Println("\n✨ Fibonacci demonstration complete!")
}
