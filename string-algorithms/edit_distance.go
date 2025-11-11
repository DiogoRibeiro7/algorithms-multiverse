/**
 * Edit Distance Algorithms - Go Implementation
 * =============================================
 *
 * String similarity and edit distance metrics.
 *
 * Run: go run edit_distance.go
 */

package main

import (
	"fmt"
	"math"
	"strings"
)

// ============================================================================
// Edit Distance Algorithms
// ============================================================================

// HammingDistance computes the Hamming distance between two strings
// Time: O(n), Space: O(1)
func HammingDistance(str1, str2 string) (int, error) {
	if len(str1) != len(str2) {
		return 0, fmt.Errorf("hamming distance requires equal length strings")
	}

	distance := 0
	for i := 0; i < len(str1); i++ {
		if str1[i] != str2[i] {
			distance++
		}
	}

	return distance, nil
}

// LevenshteinDistance computes the Levenshtein distance
// Time: O(nm), Space: O(nm)
func LevenshteinDistance(str1, str2 string, visualize bool) int {
	m, n := len(str1), len(str2)

	// Create DP table
	dp := make([][]int, m+1)
	for i := range dp {
		dp[i] = make([]int, n+1)
	}

	// Initialize base cases
	for i := 0; i <= m; i++ {
		dp[i][0] = i
	}
	for j := 0; j <= n; j++ {
		dp[0][j] = j
	}

	// Fill DP table
	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			cost := 0
			if str1[i-1] != str2[j-1] {
				cost = 1
			}

			dp[i][j] = min3(
				dp[i-1][j]+1,      // deletion
				dp[i][j-1]+1,      // insertion
				dp[i-1][j-1]+cost, // substitution
			)
		}
	}

	if visualize {
		visualizeDPTable(str1, str2, dp)
	}

	return dp[m][n]
}

// LevenshteinOptimized computes Levenshtein distance with O(min(n,m)) space
func LevenshteinOptimized(str1, str2 string) int {
	// Ensure str1 is shorter
	if len(str1) > len(str2) {
		str1, str2 = str2, str1
	}

	m, n := len(str1), len(str2)

	// Use two rows
	prevRow := make([]int, n+1)
	currRow := make([]int, n+1)

	for j := 0; j <= n; j++ {
		prevRow[j] = j
	}

	for i := 1; i <= m; i++ {
		currRow[0] = i

		for j := 1; j <= n; j++ {
			cost := 0
			if str1[i-1] != str2[j-1] {
				cost = 1
			}

			currRow[j] = min3(
				prevRow[j]+1,      // deletion
				currRow[j-1]+1,    // insertion
				prevRow[j-1]+cost, // substitution
			)
		}

		prevRow, currRow = currRow, prevRow
	}

	return prevRow[n]
}

// DamerauLevenshteinDistance computes Damerau-Levenshtein distance
// Time: O(nm), Space: O(nm)
func DamerauLevenshteinDistance(str1, str2 string) int {
	m, n := len(str1), len(str2)
	maxDist := m + n

	// Use map for sparse matrix
	H := make(map[[2]int]int)

	// Initialize
	H[[2]int{-1, -1}] = maxDist
	for i := 0; i <= m; i++ {
		H[[2]int{i, -1}] = maxDist
		H[[2]int{i, 0}] = i
	}
	for j := 0; j <= n; j++ {
		H[[2]int{-1, j}] = maxDist
		H[[2]int{0, j}] = j
	}

	for i := 1; i <= m; i++ {
		DB := 0

		for j := 1; j <= n; j++ {
			k := DB
			l := 0
			if str1[i-1] != str2[j-1] {
				l = 1
			} else {
				DB = j
			}

			H[[2]int{i, j}] = min4(
				H[[2]int{i-1, j}]+1,                                    // deletion
				H[[2]int{i, j-1}]+1,                                    // insertion
				H[[2]int{i-1, j-1}]+l,                                  // substitution
				H[[2]int{k-1, DB-1}]+(i-k-1)+1+(j-DB-1), // transposition
			)
		}
	}

	return H[[2]int{m, n}]
}

// LCSLength computes the length of Longest Common Subsequence
// Time: O(nm), Space: O(nm)
func LCSLength(str1, str2 string) int {
	m, n := len(str1), len(str2)

	dp := make([][]int, m+1)
	for i := range dp {
		dp[i] = make([]int, n+1)
	}

	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if str1[i-1] == str2[j-1] {
				dp[i][j] = dp[i-1][j-1] + 1
			} else {
				dp[i][j] = max(dp[i-1][j], dp[i][j-1])
			}
		}
	}

	return dp[m][n]
}

// LCSString returns the actual Longest Common Subsequence
func LCSString(str1, str2 string) string {
	m, n := len(str1), len(str2)

	dp := make([][]int, m+1)
	for i := range dp {
		dp[i] = make([]int, n+1)
	}

	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if str1[i-1] == str2[j-1] {
				dp[i][j] = dp[i-1][j-1] + 1
			} else {
				dp[i][j] = max(dp[i-1][j], dp[i][j-1])
			}
		}
	}

	// Backtrack to find LCS
	var lcs strings.Builder
	i, j := m, n

	for i > 0 && j > 0 {
		if str1[i-1] == str2[j-1] {
			lcs.WriteByte(str1[i-1])
			i--
			j--
		} else if dp[i-1][j] > dp[i][j-1] {
			i--
		} else {
			j--
		}
	}

	// Reverse the string
	result := lcs.String()
	return reverse(result)
}

// EditOperation represents an edit operation
type EditOperation struct {
	Op   string
	Pos  int
	Char byte
}

// EditSequence returns the sequence of edit operations
func EditSequence(str1, str2 string) []EditOperation {
	m, n := len(str1), len(str2)

	dp := make([][]int, m+1)
	ops := make([][]*EditOperation, m+1)
	for i := range dp {
		dp[i] = make([]int, n+1)
		ops[i] = make([]*EditOperation, n+1)
	}

	// Initialize
	for i := 0; i <= m; i++ {
		dp[i][0] = i
		if i > 0 {
			ops[i][0] = &EditOperation{"delete", i - 1, str1[i-1]}
		}
	}

	for j := 0; j <= n; j++ {
		dp[0][j] = j
		if j > 0 {
			ops[0][j] = &EditOperation{"insert", j - 1, str2[j-1]}
		}
	}

	// Fill tables
	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if str1[i-1] == str2[j-1] {
				dp[i][j] = dp[i-1][j-1]
				ops[i][j] = &EditOperation{"match", i - 1, str1[i-1]}
			} else {
				costs := []struct {
					cost int
					op   EditOperation
				}{
					{dp[i-1][j] + 1, EditOperation{"delete", i - 1, str1[i-1]}},
					{dp[i][j-1] + 1, EditOperation{"insert", j - 1, str2[j-1]}},
					{dp[i-1][j-1] + 1, EditOperation{"substitute", i - 1, str2[j-1]}},
				}

				minCost := costs[0]
				for _, c := range costs[1:] {
					if c.cost < minCost.cost {
						minCost = c
					}
				}

				dp[i][j] = minCost.cost
				ops[i][j] = &minCost.op
			}
		}
	}

	// Backtrack
	sequence := []EditOperation{}
	i, j := m, n

	for i > 0 || j > 0 {
		if ops[i][j] != nil {
			sequence = append([]EditOperation{*ops[i][j]}, sequence...)

			switch ops[i][j].Op {
			case "match", "substitute":
				i--
				j--
			case "delete":
				i--
			case "insert":
				j--
			}
		} else {
			break
		}
	}

	return sequence
}

// ============================================================================
// Similarity Metrics
// ============================================================================

// NormalizedLevenshtein computes normalized Levenshtein distance (0 to 1)
func NormalizedLevenshtein(str1, str2 string) float64 {
	if len(str1) == 0 && len(str2) == 0 {
		return 1.0
	}

	distance := LevenshteinDistance(str1, str2, false)
	maxLen := max(len(str1), len(str2))

	return 1.0 - float64(distance)/float64(maxLen)
}

// SimilarityRatio computes similarity ratio based on LCS
func SimilarityRatio(str1, str2 string) float64 {
	if len(str1) == 0 && len(str2) == 0 {
		return 1.0
	}

	lcsLen := LCSLength(str1, str2)
	totalLen := len(str1) + len(str2)

	if totalLen == 0 {
		return 1.0
	}

	return 2.0 * float64(lcsLen) / float64(totalLen)
}

// JaroDistance computes Jaro distance
func JaroDistance(str1, str2 string) float64 {
	if str1 == str2 {
		return 1.0
	}

	len1, len2 := len(str1), len(str2)

	if len1 == 0 || len2 == 0 {
		return 0.0
	}

	// Maximum allowed distance
	matchDistance := max(len1, len2)/2 - 1
	if matchDistance < 1 {
		matchDistance = 1
	}

	str1Matches := make([]bool, len1)
	str2Matches := make([]bool, len2)

	matches := 0
	transpositions := 0

	// Find matches
	for i := 0; i < len1; i++ {
		start := max(0, i-matchDistance)
		end := min(i+matchDistance+1, len2)

		for j := start; j < end; j++ {
			if str2Matches[j] || str1[i] != str2[j] {
				continue
			}
			str1Matches[i] = true
			str2Matches[j] = true
			matches++
			break
		}
	}

	if matches == 0 {
		return 0.0
	}

	// Find transpositions
	k := 0
	for i := 0; i < len1; i++ {
		if !str1Matches[i] {
			continue
		}
		for !str2Matches[k] {
			k++
		}
		if str1[i] != str2[k] {
			transpositions++
		}
		k++
	}

	return (float64(matches)/float64(len1) +
		float64(matches)/float64(len2) +
		float64(matches-transpositions/2)/float64(matches)) / 3.0
}

// JaroWinklerDistance computes Jaro-Winkler distance
func JaroWinklerDistance(str1, str2 string, prefixScale float64) float64 {
	jaro := JaroDistance(str1, str2)

	// Find common prefix length (max 4)
	prefix := 0
	minLen := min(len(str1), len(str2))
	if minLen > 4 {
		minLen = 4
	}

	for i := 0; i < minLen; i++ {
		if str1[i] == str2[i] {
			prefix++
		} else {
			break
		}
	}

	return jaro + float64(prefix)*prefixScale*(1-jaro)
}

// ============================================================================
// Helper Functions
// ============================================================================

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func min3(a, b, c int) int {
	return min(min(a, b), c)
}

func min4(a, b, c, d int) int {
	return min(min3(a, b, c), d)
}

func reverse(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func visualizeDPTable(str1, str2 string, dp [][]int) {
	fmt.Println("\nDP Table:")
	fmt.Println(strings.Repeat("=", 70))

	// Header
	fmt.Print("       ")
	for _, c := range str2 {
		fmt.Printf("%4c", c)
	}
	fmt.Println()

	// Rows
	for i, row := range dp {
		if i == 0 {
			fmt.Print("  ")
		} else {
			fmt.Printf("%2c", str1[i-1])
		}

		for _, val := range row {
			fmt.Printf("%4d", val)
		}
		fmt.Println()
	}
}

// ============================================================================
// Main Function - Examples
// ============================================================================

func main() {
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println("EDIT DISTANCE ALGORITHMS - GO")
	fmt.Println(strings.Repeat("=", 70))

	// Example 1: Hamming distance
	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("EXAMPLE 1: Hamming Distance")
	fmt.Println(strings.Repeat("=", 70))

	str1, str2 := "karolin", "kathrin"
	dist, err := HammingDistance(str1, str2)
	if err != nil {
		fmt.Println("Error:", err)
	} else {
		fmt.Printf("String 1: '%s'\n", str1)
		fmt.Printf("String 2: '%s'\n", str2)
		fmt.Printf("Hamming distance: %d\n", dist)
	}

	// Example 2: Levenshtein distance
	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("EXAMPLE 2: Levenshtein Distance")
	fmt.Println(strings.Repeat("=", 70))

	str3, str4 := "kitten", "sitting"
	dist2 := LevenshteinDistance(str3, str4, true)

	fmt.Printf("\nString 1: '%s'\n", str3)
	fmt.Printf("String 2: '%s'\n", str4)
	fmt.Printf("Levenshtein distance: %d\n", dist2)

	// Example 3: Damerau-Levenshtein
	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("EXAMPLE 3: Damerau-Levenshtein Distance")
	fmt.Println(strings.Repeat("=", 70))

	testCases := [][2]string{
		{"kitten", "sitting"},
		{"teh", "the"},
		{"abcd", "acbd"},
	}

	for _, tc := range testCases {
		s1, s2 := tc[0], tc[1]
		levDist := LevenshteinDistance(s1, s2, false)
		damLevDist := DamerauLevenshteinDistance(s1, s2)

		fmt.Printf("\nString 1: '%s'\n", s1)
		fmt.Printf("String 2: '%s'\n", s2)
		fmt.Printf("  Levenshtein:         %d\n", levDist)
		fmt.Printf("  Damerau-Levenshtein: %d\n", damLevDist)
	}

	// Example 4: LCS
	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("EXAMPLE 4: Longest Common Subsequence")
	fmt.Println(strings.Repeat("=", 70))

	str5, str6 := "ABCDGH", "AEDFHR"
	lcs := LCSString(str5, str6)

	fmt.Printf("String 1: '%s'\n", str5)
	fmt.Printf("String 2: '%s'\n", str6)
	fmt.Printf("LCS: '%s' (length: %d)\n", lcs, len(lcs))

	// Example 5: Similarity metrics
	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("EXAMPLE 5: Similarity Metrics")
	fmt.Println(strings.Repeat("=", 70))

	testPairs := [][2]string{
		{"kitten", "sitting"},
		{"saturday", "sunday"},
		{"martha", "marhta"},
		{"dixon", "dicksonx"},
	}

	for _, pair := range testPairs {
		s1, s2 := pair[0], pair[1]
		normLev := NormalizedLevenshtein(s1, s2)
		simRatio := SimilarityRatio(s1, s2)
		jaro := JaroDistance(s1, s2)
		jaroWinkler := JaroWinklerDistance(s1, s2, 0.1)

		fmt.Printf("\n'%s' vs '%s':\n", s1, s2)
		fmt.Printf("  Normalized Levenshtein: %.4f\n", normLev)
		fmt.Printf("  Similarity Ratio:       %.4f\n", simRatio)
		fmt.Printf("  Jaro:                   %.4f\n", jaro)
		fmt.Printf("  Jaro-Winkler:           %.4f\n", jaroWinkler)
	}

	fmt.Println("\n" + strings.Repeat("=", 70))
}
