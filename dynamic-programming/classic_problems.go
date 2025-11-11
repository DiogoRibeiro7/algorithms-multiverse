package main

import (
	"fmt"
	"math"
	"sort"
	"strings"
)

/**
 * Dynamic Programming Classic Problems
 * =====================================
 *
 * Comprehensive implementations of classic DP problems with multiple
 * solution approaches: naive recursive, memoized (top-down),
 * tabulated (bottom-up), and space-optimized versions.
 *
 * Run: go run classic_problems.go
 */

// ============================================================================
// 1. LONGEST COMMON SUBSEQUENCE (LCS)
// ============================================================================

/*
Problem: Find the length of the longest subsequence common to two sequences.

Real-world applications:
- Version control systems (diff algorithms)
- DNA sequence analysis
- Plagiarism detection
*/

// LcsNaive - Naive recursive solution
// Time: O(2^(m+n)), Space: O(m+n)
func LcsNaive(s1, s2 string) int {
	return lcsNaiveHelper(s1, s2, 0, 0)
}

func lcsNaiveHelper(s1, s2 string, i, j int) int {
	if i == len(s1) || j == len(s2) {
		return 0
	}

	if s1[i] == s2[j] {
		return 1 + lcsNaiveHelper(s1, s2, i+1, j+1)
	}
	return max(lcsNaiveHelper(s1, s2, i+1, j), lcsNaiveHelper(s1, s2, i, j+1))
}

// LcsMemoized - Memoized solution
// Time: O(m*n), Space: O(m*n)
func LcsMemoized(s1, s2 string) int {
	memo := make(map[string]int)
	return lcsMemoizedHelper(s1, s2, 0, 0, memo)
}

func lcsMemoizedHelper(s1, s2 string, i, j int, memo map[string]int) int {
	if i == len(s1) || j == len(s2) {
		return 0
	}

	key := fmt.Sprintf("%d,%d", i, j)
	if val, ok := memo[key]; ok {
		return val
	}

	var result int
	if s1[i] == s2[j] {
		result = 1 + lcsMemoizedHelper(s1, s2, i+1, j+1, memo)
	} else {
		result = max(lcsMemoizedHelper(s1, s2, i+1, j, memo),
			lcsMemoizedHelper(s1, s2, i, j+1, memo))
	}

	memo[key] = result
	return result
}

// LcsTabulated - Tabulated solution
// Time: O(m*n), Space: O(m*n)
func LcsTabulated(s1, s2 string) int {
	m, n := len(s1), len(s2)
	dp := make([][]int, m+1)
	for i := range dp {
		dp[i] = make([]int, n+1)
	}

	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if s1[i-1] == s2[j-1] {
				dp[i][j] = 1 + dp[i-1][j-1]
			} else {
				dp[i][j] = max(dp[i-1][j], dp[i][j-1])
			}
		}
	}

	return dp[m][n]
}

// LcsSpaceOptimized - Space-optimized solution
// Time: O(m*n), Space: O(min(m, n))
func LcsSpaceOptimized(s1, s2 string) int {
	if len(s1) < len(s2) {
		s1, s2 = s2, s1
	}

	m, n := len(s1), len(s2)
	prev := make([]int, n+1)
	curr := make([]int, n+1)

	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if s1[i-1] == s2[j-1] {
				curr[j] = 1 + prev[j-1]
			} else {
				curr[j] = max(prev[j], curr[j-1])
			}
		}
		prev, curr = curr, prev
	}

	return prev[n]
}

// ============================================================================
// 2. LONGEST INCREASING SUBSEQUENCE (LIS)
// ============================================================================

/*
Problem: Find the length of the longest strictly increasing subsequence.

Real-world applications:
- Stock market trend analysis
- Task scheduling
*/

// LisNaive - Naive recursive solution
// Time: O(2^n), Space: O(n)
func LisNaive(arr []int) int {
	return lisNaiveHelper(arr, 0, math.MinInt32)
}

func lisNaiveHelper(arr []int, idx, prev int) int {
	if idx == len(arr) {
		return 0
	}

	exclude := lisNaiveHelper(arr, idx+1, prev)
	include := 0
	if arr[idx] > prev {
		include = 1 + lisNaiveHelper(arr, idx+1, arr[idx])
	}

	return max(exclude, include)
}

// LisTabulated - Tabulated O(n^2) solution
// Time: O(n^2), Space: O(n)
func LisTabulated(arr []int) int {
	if len(arr) == 0 {
		return 0
	}

	n := len(arr)
	dp := make([]int, n)
	for i := range dp {
		dp[i] = 1
	}

	for i := 1; i < n; i++ {
		for j := 0; j < i; j++ {
			if arr[j] < arr[i] {
				dp[i] = max(dp[i], dp[j]+1)
			}
		}
	}

	maxLen := 0
	for _, val := range dp {
		maxLen = max(maxLen, val)
	}
	return maxLen
}

// LisOptimized - Optimized solution using binary search
// Time: O(n log n), Space: O(n)
func LisOptimized(arr []int) int {
	if len(arr) == 0 {
		return 0
	}

	tails := []int{}

	for _, num := range arr {
		pos := sort.SearchInts(tails, num)
		if pos == len(tails) {
			tails = append(tails, num)
		} else {
			tails[pos] = num
		}
	}

	return len(tails)
}

// ============================================================================
// 3. EDIT DISTANCE (LEVENSHTEIN DISTANCE)
// ============================================================================

/*
Problem: Minimum operations (insert, delete, replace) to convert s1 to s2.

Real-world applications:
- Spell checkers
- DNA sequence alignment
- Autocorrect systems
*/

// EditDistanceNaive - Naive recursive solution
// Time: O(3^max(m,n)), Space: O(max(m, n))
func EditDistanceNaive(s1, s2 string) int {
	return editDistanceNaiveHelper(s1, s2, len(s1), len(s2))
}

func editDistanceNaiveHelper(s1, s2 string, i, j int) int {
	if i == 0 {
		return j
	}
	if j == 0 {
		return i
	}

	if s1[i-1] == s2[j-1] {
		return editDistanceNaiveHelper(s1, s2, i-1, j-1)
	}

	return 1 + min3(
		editDistanceNaiveHelper(s1, s2, i, j-1),   // insert
		editDistanceNaiveHelper(s1, s2, i-1, j),   // delete
		editDistanceNaiveHelper(s1, s2, i-1, j-1), // replace
	)
}

// EditDistanceMemoized - Memoized solution
// Time: O(m*n), Space: O(m*n)
func EditDistanceMemoized(s1, s2 string) int {
	memo := make(map[string]int)
	return editDistanceMemoizedHelper(s1, s2, len(s1), len(s2), memo)
}

func editDistanceMemoizedHelper(s1, s2 string, i, j int, memo map[string]int) int {
	if i == 0 {
		return j
	}
	if j == 0 {
		return i
	}

	key := fmt.Sprintf("%d,%d", i, j)
	if val, ok := memo[key]; ok {
		return val
	}

	var result int
	if s1[i-1] == s2[j-1] {
		result = editDistanceMemoizedHelper(s1, s2, i-1, j-1, memo)
	} else {
		result = 1 + min3(
			editDistanceMemoizedHelper(s1, s2, i, j-1, memo),
			editDistanceMemoizedHelper(s1, s2, i-1, j, memo),
			editDistanceMemoizedHelper(s1, s2, i-1, j-1, memo),
		)
	}

	memo[key] = result
	return result
}

// EditDistanceTabulated - Tabulated solution
// Time: O(m*n), Space: O(m*n)
func EditDistanceTabulated(s1, s2 string) int {
	m, n := len(s1), len(s2)
	dp := make([][]int, m+1)
	for i := range dp {
		dp[i] = make([]int, n+1)
	}

	for i := 0; i <= m; i++ {
		dp[i][0] = i
	}
	for j := 0; j <= n; j++ {
		dp[0][j] = j
	}

	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if s1[i-1] == s2[j-1] {
				dp[i][j] = dp[i-1][j-1]
			} else {
				dp[i][j] = 1 + min3(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])
			}
		}
	}

	return dp[m][n]
}

// EditDistanceSpaceOptimized - Space-optimized solution
// Time: O(m*n), Space: O(min(m, n))
func EditDistanceSpaceOptimized(s1, s2 string) int {
	if len(s1) < len(s2) {
		s1, s2 = s2, s1
	}

	n := len(s2)
	prev := make([]int, n+1)
	curr := make([]int, n+1)

	for j := 0; j <= n; j++ {
		prev[j] = j
	}

	for i := 1; i <= len(s1); i++ {
		curr[0] = i
		for j := 1; j <= n; j++ {
			if s1[i-1] == s2[j-1] {
				curr[j] = prev[j-1]
			} else {
				curr[j] = 1 + min3(curr[j-1], prev[j], prev[j-1])
			}
		}
		prev, curr = curr, prev
	}

	return prev[n]
}

// ============================================================================
// 4. COIN CHANGE PROBLEM
// ============================================================================

/*
Problem: Find minimum coins needed or count ways to make change.

Real-world applications:
- Vending machines
- Currency exchange
*/

// CoinChangeMinNaive - Naive recursive for minimum coins
// Time: O(amount^len(coins)), Space: O(amount)
func CoinChangeMinNaive(coins []int, amount int) int {
	result := coinChangeMinNaiveHelper(coins, amount)
	if result == math.MaxInt32 {
		return -1
	}
	return result
}

func coinChangeMinNaiveHelper(coins []int, remaining int) int {
	if remaining == 0 {
		return 0
	}
	if remaining < 0 {
		return math.MaxInt32
	}

	minCoins := math.MaxInt32
	for _, coin := range coins {
		result := coinChangeMinNaiveHelper(coins, remaining-coin)
		if result != math.MaxInt32 {
			minCoins = min(minCoins, result+1)
		}
	}

	return minCoins
}

// CoinChangeMinMemoized - Memoized for minimum coins
// Time: O(amount * len(coins)), Space: O(amount)
func CoinChangeMinMemoized(coins []int, amount int) int {
	memo := make(map[int]int)
	result := coinChangeMinMemoizedHelper(coins, amount, memo)
	if result == math.MaxInt32 {
		return -1
	}
	return result
}

func coinChangeMinMemoizedHelper(coins []int, remaining int, memo map[int]int) int {
	if remaining == 0 {
		return 0
	}
	if remaining < 0 {
		return math.MaxInt32
	}

	if val, ok := memo[remaining]; ok {
		return val
	}

	minCoins := math.MaxInt32
	for _, coin := range coins {
		result := coinChangeMinMemoizedHelper(coins, remaining-coin, memo)
		if result != math.MaxInt32 {
			minCoins = min(minCoins, result+1)
		}
	}

	memo[remaining] = minCoins
	return minCoins
}

// CoinChangeMinTabulated - Tabulated for minimum coins
// Time: O(amount * len(coins)), Space: O(amount)
func CoinChangeMinTabulated(coins []int, amount int) int {
	dp := make([]int, amount+1)
	for i := range dp {
		dp[i] = math.MaxInt32
	}
	dp[0] = 0

	for i := 1; i <= amount; i++ {
		for _, coin := range coins {
			if coin <= i && dp[i-coin] != math.MaxInt32 {
				dp[i] = min(dp[i], dp[i-coin]+1)
			}
		}
	}

	if dp[amount] == math.MaxInt32 {
		return -1
	}
	return dp[amount]
}

// CoinChangeWaysTabulated - Count ways to make change
// Time: O(amount * len(coins)), Space: O(amount)
func CoinChangeWaysTabulated(coins []int, amount int) int {
	dp := make([]int, amount+1)
	dp[0] = 1

	for _, coin := range coins {
		for i := coin; i <= amount; i++ {
			dp[i] += dp[i-coin]
		}
	}

	return dp[amount]
}

// ============================================================================
// 5. KNAPSACK PROBLEMS
// ============================================================================

/*
Problem: Maximize value within weight capacity.

Real-world applications:
- Resource allocation
- Portfolio optimization
*/

// Knapsack01Naive - 0/1 Knapsack naive recursive
// Time: O(2^n), Space: O(n)
func Knapsack01Naive(weights, values []int, capacity int) int {
	return knapsack01NaiveHelper(weights, values, capacity, 0)
}

func knapsack01NaiveHelper(weights, values []int, capacity, idx int) int {
	if idx == len(weights) || capacity == 0 {
		return 0
	}

	skip := knapsack01NaiveHelper(weights, values, capacity, idx+1)
	take := 0
	if weights[idx] <= capacity {
		take = values[idx] + knapsack01NaiveHelper(weights, values, capacity-weights[idx], idx+1)
	}

	return max(skip, take)
}

// Knapsack01Tabulated - 0/1 Knapsack tabulated
// Time: O(n * capacity), Space: O(n * capacity)
func Knapsack01Tabulated(weights, values []int, capacity int) int {
	n := len(weights)
	dp := make([][]int, n+1)
	for i := range dp {
		dp[i] = make([]int, capacity+1)
	}

	for i := 1; i <= n; i++ {
		for w := 0; w <= capacity; w++ {
			dp[i][w] = dp[i-1][w]
			if weights[i-1] <= w {
				dp[i][w] = max(dp[i][w], dp[i-1][w-weights[i-1]]+values[i-1])
			}
		}
	}

	return dp[n][capacity]
}

// Knapsack01SpaceOptimized - 0/1 Knapsack space optimized
// Time: O(n * capacity), Space: O(capacity)
func Knapsack01SpaceOptimized(weights, values []int, capacity int) int {
	dp := make([]int, capacity+1)

	for i := 0; i < len(weights); i++ {
		for w := capacity; w >= weights[i]; w-- {
			dp[w] = max(dp[w], dp[w-weights[i]]+values[i])
		}
	}

	return dp[capacity]
}

// KnapsackUnboundedTabulated - Unbounded Knapsack
// Time: O(n * capacity), Space: O(capacity)
func KnapsackUnboundedTabulated(weights, values []int, capacity int) int {
	dp := make([]int, capacity+1)

	for w := 1; w <= capacity; w++ {
		for i := 0; i < len(weights); i++ {
			if weights[i] <= w {
				dp[w] = max(dp[w], dp[w-weights[i]]+values[i])
			}
		}
	}

	return dp[capacity]
}

// ============================================================================
// 6. MATRIX CHAIN MULTIPLICATION
// ============================================================================

/*
Problem: Find optimal parenthesization to minimize multiplications.

Real-world applications:
- Compiler optimization
- Database query optimization
*/

// MatrixChainNaive - Naive recursive solution
// Time: O(2^n), Space: O(n)
func MatrixChainNaive(dims []int) int {
	return matrixChainNaiveHelper(dims, 1, len(dims)-1)
}

func matrixChainNaiveHelper(dims []int, i, j int) int {
	if i == j {
		return 0
	}

	minCost := math.MaxInt32
	for k := i; k < j; k++ {
		cost := matrixChainNaiveHelper(dims, i, k) +
			matrixChainNaiveHelper(dims, k+1, j) +
			dims[i-1]*dims[k]*dims[j]
		minCost = min(minCost, cost)
	}

	return minCost
}

// MatrixChainMemoized - Memoized solution
// Time: O(n^3), Space: O(n^2)
func MatrixChainMemoized(dims []int) int {
	memo := make(map[string]int)
	return matrixChainMemoizedHelper(dims, 1, len(dims)-1, memo)
}

func matrixChainMemoizedHelper(dims []int, i, j int, memo map[string]int) int {
	if i == j {
		return 0
	}

	key := fmt.Sprintf("%d,%d", i, j)
	if val, ok := memo[key]; ok {
		return val
	}

	minCost := math.MaxInt32
	for k := i; k < j; k++ {
		cost := matrixChainMemoizedHelper(dims, i, k, memo) +
			matrixChainMemoizedHelper(dims, k+1, j, memo) +
			dims[i-1]*dims[k]*dims[j]
		minCost = min(minCost, cost)
	}

	memo[key] = minCost
	return minCost
}

// MatrixChainTabulated - Tabulated solution
// Time: O(n^3), Space: O(n^2)
func MatrixChainTabulated(dims []int) int {
	n := len(dims)
	dp := make([][]int, n)
	for i := range dp {
		dp[i] = make([]int, n)
	}

	for length := 2; length < n; length++ {
		for i := 1; i < n-length+1; i++ {
			j := i + length - 1
			dp[i][j] = math.MaxInt32

			for k := i; k < j; k++ {
				cost := dp[i][k] + dp[k+1][j] + dims[i-1]*dims[k]*dims[j]
				dp[i][j] = min(dp[i][j], cost)
			}
		}
	}

	return dp[1][n-1]
}

// ============================================================================
// 7. PALINDROME PROBLEMS
// ============================================================================

/*
Real-world applications:
- DNA sequence analysis
- Text processing
*/

// LongestPalindromeSubsequenceTabulated - Longest palindromic subsequence
// Time: O(n^2), Space: O(n^2)
func LongestPalindromeSubsequenceTabulated(s string) int {
	n := len(s)
	dp := make([][]int, n)
	for i := range dp {
		dp[i] = make([]int, n)
		dp[i][i] = 1
	}

	for length := 2; length <= n; length++ {
		for i := 0; i < n-length+1; i++ {
			j := i + length - 1

			if s[i] == s[j] {
				if i+1 <= j-1 {
					dp[i][j] = 2 + dp[i+1][j-1]
				} else {
					dp[i][j] = 2
				}
			} else {
				dp[i][j] = max(dp[i+1][j], dp[i][j-1])
			}
		}
	}

	return dp[0][n-1]
}

// CountPalindromicSubstrings - Count palindromic substrings
// Time: O(n^2), Space: O(1)
func CountPalindromicSubstrings(s string) int {
	total := 0
	for i := 0; i < len(s); i++ {
		total += expandAroundCenter(s, i, i)     // odd length
		total += expandAroundCenter(s, i, i+1)   // even length
	}
	return total
}

func expandAroundCenter(s string, left, right int) int {
	count := 0
	for left >= 0 && right < len(s) && s[left] == s[right] {
		count++
		left--
		right++
	}
	return count
}

// MinInsertionsPalindrome - Minimum insertions to make palindrome
// Time: O(n^2), Space: O(n^2)
func MinInsertionsPalindrome(s string) int {
	return len(s) - LongestPalindromeSubsequenceTabulated(s)
}

// PalindromePartitioningMinCuts - Minimum cuts for palindrome partitioning
// Time: O(n^2), Space: O(n^2)
func PalindromePartitioningMinCuts(s string) int {
	n := len(s)

	isPalindrome := make([][]bool, n)
	for i := range isPalindrome {
		isPalindrome[i] = make([]bool, n)
		isPalindrome[i][i] = true
	}

	for length := 2; length <= n; length++ {
		for i := 0; i < n-length+1; i++ {
			j := i + length - 1
			if s[i] == s[j] {
				isPalindrome[i][j] = (length == 2) || isPalindrome[i+1][j-1]
			}
		}
	}

	dp := make([]int, n)
	for i := range dp {
		dp[i] = math.MaxInt32
	}

	for i := 0; i < n; i++ {
		if isPalindrome[0][i] {
			dp[i] = 0
		} else {
			for j := 0; j < i; j++ {
				if isPalindrome[j+1][i] {
					dp[i] = min(dp[i], dp[j]+1)
				}
			}
		}
	}

	return dp[n-1]
}

// ============================================================================
// 8. MAXIMUM SUBARRAY SUM (KADANE'S ALGORITHM)
// ============================================================================

/*
Problem: Find contiguous subarray with maximum sum.

Real-world applications:
- Stock market analysis
- Signal processing
*/

// MaxSubarrayNaive - Naive solution
// Time: O(n^2), Space: O(1)
func MaxSubarrayNaive(arr []int) int {
	if len(arr) == 0 {
		return 0
	}

	maxSum := math.MinInt32
	for i := 0; i < len(arr); i++ {
		currentSum := 0
		for j := i; j < len(arr); j++ {
			currentSum += arr[j]
			maxSum = max(maxSum, currentSum)
		}
	}

	return maxSum
}

// MaxSubarrayKadane - Kadane's Algorithm
// Time: O(n), Space: O(1)
func MaxSubarrayKadane(arr []int) int {
	if len(arr) == 0 {
		return 0
	}

	maxSum := arr[0]
	currentSum := arr[0]

	for i := 1; i < len(arr); i++ {
		currentSum = max(arr[i], currentSum+arr[i])
		maxSum = max(maxSum, currentSum)
	}

	return maxSum
}

// SubarrayResult holds the result with indices
type SubarrayResult struct {
	MaxSum int
	Start  int
	End    int
}

// MaxSubarrayWithIndices - Kadane's with indices
// Time: O(n), Space: O(1)
func MaxSubarrayWithIndices(arr []int) SubarrayResult {
	if len(arr) == 0 {
		return SubarrayResult{0, -1, -1}
	}

	maxSum := arr[0]
	currentSum := arr[0]
	start, end, tempStart := 0, 0, 0

	for i := 1; i < len(arr); i++ {
		if arr[i] > currentSum+arr[i] {
			currentSum = arr[i]
			tempStart = i
		} else {
			currentSum = currentSum + arr[i]
		}

		if currentSum > maxSum {
			maxSum = currentSum
			start = tempStart
			end = i
		}
	}

	return SubarrayResult{maxSum, start, end}
}

// MaxSubarrayCircular - Maximum subarray in circular array
// Time: O(n), Space: O(1)
func MaxSubarrayCircular(arr []int) int {
	if len(arr) == 0 {
		return 0
	}

	maxNormal := MaxSubarrayKadane(arr)
	if maxNormal < 0 {
		return maxNormal
	}

	totalSum := 0
	for _, num := range arr {
		totalSum += num
	}

	minSum := kadaneMin(arr)
	maxCircular := totalSum - minSum

	return max(maxNormal, maxCircular)
}

func kadaneMin(arr []int) int {
	minSum := arr[0]
	currentSum := arr[0]
	for i := 1; i < len(arr); i++ {
		currentSum = min(arr[i], currentSum+arr[i])
		minSum = min(minSum, currentSum)
	}
	return minSum
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func min3(a, b, c int) int {
	return min(min(a, b), c)
}

// ============================================================================
// MAIN - EXAMPLE USAGE AND TESTING
// ============================================================================

func main() {
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println("DYNAMIC PROGRAMMING CLASSIC PROBLEMS - EXAMPLES")
	fmt.Println(strings.Repeat("=", 70))

	// LCS Examples
	fmt.Println("\n1. Longest Common Subsequence:")
	s1, s2 := "ABCDGH", "AEDFHR"
	fmt.Printf("   Strings: '%s', '%s'\n", s1, s2)
	fmt.Printf("   Naive: %d\n", LcsNaive(s1, s2))
	fmt.Printf("   Memoized: %d\n", LcsMemoized(s1, s2))
	fmt.Printf("   Tabulated: %d\n", LcsTabulated(s1, s2))
	fmt.Printf("   Space-optimized: %d\n", LcsSpaceOptimized(s1, s2))

	// LIS Examples
	fmt.Println("\n2. Longest Increasing Subsequence:")
	arr1 := []int{10, 9, 2, 5, 3, 7, 101, 18}
	fmt.Printf("   Array: %v\n", arr1)
	fmt.Printf("   Naive: %d\n", LisNaive(arr1))
	fmt.Printf("   Tabulated O(n^2): %d\n", LisTabulated(arr1))
	fmt.Printf("   Optimized O(n log n): %d\n", LisOptimized(arr1))

	// Edit Distance
	fmt.Println("\n3. Edit Distance:")
	str1, str2 := "kitten", "sitting"
	fmt.Printf("   Strings: '%s', '%s'\n", str1, str2)
	fmt.Printf("   Naive: %d\n", EditDistanceNaive(str1, str2))
	fmt.Printf("   Memoized: %d\n", EditDistanceMemoized(str1, str2))
	fmt.Printf("   Tabulated: %d\n", EditDistanceTabulated(str1, str2))
	fmt.Printf("   Space-optimized: %d\n", EditDistanceSpaceOptimized(str1, str2))

	// Coin Change
	fmt.Println("\n4. Coin Change:")
	coins := []int{1, 2, 5}
	amount := 11
	fmt.Printf("   Coins: %v, Amount: %d\n", coins, amount)
	fmt.Printf("   Min coins (naive): %d\n", CoinChangeMinNaive(coins, amount))
	fmt.Printf("   Min coins (memoized): %d\n", CoinChangeMinMemoized(coins, amount))
	fmt.Printf("   Min coins (tabulated): %d\n", CoinChangeMinTabulated(coins, amount))
	fmt.Printf("   Ways to make change: %d\n", CoinChangeWaysTabulated(coins, amount))

	// Knapsack
	fmt.Println("\n5. Knapsack Problem:")
	weights := []int{1, 3, 4, 5}
	values := []int{1, 4, 5, 7}
	capacity := 7
	fmt.Printf("   Weights: %v, Values: %v, Capacity: %d\n", weights, values, capacity)
	fmt.Printf("   0/1 Naive: %d\n", Knapsack01Naive(weights, values, capacity))
	fmt.Printf("   0/1 Tabulated: %d\n", Knapsack01Tabulated(weights, values, capacity))
	fmt.Printf("   0/1 Space-optimized: %d\n", Knapsack01SpaceOptimized(weights, values, capacity))
	fmt.Printf("   Unbounded: %d\n", KnapsackUnboundedTabulated(weights, values, capacity))

	// Matrix Chain
	fmt.Println("\n6. Matrix Chain Multiplication:")
	dims := []int{10, 20, 30, 40, 30}
	fmt.Printf("   Dimensions: %v\n", dims)
	fmt.Printf("   Naive: %d\n", MatrixChainNaive(dims))
	fmt.Printf("   Memoized: %d\n", MatrixChainMemoized(dims))
	fmt.Printf("   Tabulated: %d\n", MatrixChainTabulated(dims))

	// Palindromes
	fmt.Println("\n7. Palindrome Problems:")
	pStr := "bbbab"
	fmt.Printf("   String: '%s'\n", pStr)
	fmt.Printf("   Longest palindromic subsequence: %d\n",
		LongestPalindromeSubsequenceTabulated(pStr))
	fmt.Printf("   Count palindromic substrings: %d\n",
		CountPalindromicSubstrings(pStr))
	fmt.Printf("   Min insertions for palindrome: %d\n",
		MinInsertionsPalindrome(pStr))
	fmt.Printf("   Min cuts for palindrome partition: %d\n",
		PalindromePartitioningMinCuts(pStr))

	// Maximum Subarray
	fmt.Println("\n8. Maximum Subarray Sum:")
	arr2 := []int{-2, 1, -3, 4, -1, 2, 1, -5, 4}
	fmt.Printf("   Array: %v\n", arr2)
	fmt.Printf("   Naive: %d\n", MaxSubarrayNaive(arr2))
	fmt.Printf("   Kadane's: %d\n", MaxSubarrayKadane(arr2))
	result := MaxSubarrayWithIndices(arr2)
	fmt.Printf("   With indices: sum=%d, range=[%d:%d]\n",
		result.MaxSum, result.Start, result.End+1)

	arrCircular := []int{5, -3, 5}
	fmt.Printf("   Circular array: %v\n", arrCircular)
	fmt.Printf("   Max circular sum: %d\n", MaxSubarrayCircular(arrCircular))

	fmt.Println("\n" + strings.Repeat("=", 70))
}
