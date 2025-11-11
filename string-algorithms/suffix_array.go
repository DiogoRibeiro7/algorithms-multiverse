/*
 * Suffix Array and LCP Array Construction in Go
 * =============================================
 *
 * Algorithms implemented:
 * 1. Prefix doubling O(n log² n) for suffix array construction
 * 2. Kasai's algorithm O(n) for LCP array computation
 *
 * Applications:
 * - Pattern matching in O(m log n) time
 * - Finding longest repeated substring
 * - Counting distinct substrings
 * - Longest common substring between two strings
 *
 * Usage: go run suffix_array.go
 */

package main

import (
	"fmt"
	"sort"
	"strings"
	"time"
)

// Suffix represents a suffix with its index and rank pair
type Suffix struct {
	Index int
	Rank  [2]int
}

// SuffixArray provides methods for suffix array construction and operations
type SuffixArray struct {
	text string
	sa   []int
	lcp  []int
}

// NewSuffixArray creates a new suffix array from text
func NewSuffixArray(text string) *SuffixArray {
	sa := &SuffixArray{
		text: text,
	}
	sa.Build()
	sa.BuildLCP()
	return sa
}

// Build constructs the suffix array using prefix doubling algorithm
// Time: O(n log² n)
// Space: O(n)
func (sa *SuffixArray) Build() {
	n := len(sa.text)
	sa.sa = make([]int, n)

	if n == 0 {
		return
	}

	// Create suffix structures
	suffixes := make([]Suffix, n)
	rank := make([]int, n)

	// Initialize ranks with character values
	for i := 0; i < n; i++ {
		suffixes[i].Index = i
		suffixes[i].Rank[0] = int(sa.text[i])
		if i+1 < n {
			suffixes[i].Rank[1] = int(sa.text[i+1])
		} else {
			suffixes[i].Rank[1] = -1
		}
	}

	// Sort by first two characters
	sort.Slice(suffixes, func(i, j int) bool {
		if suffixes[i].Rank[0] != suffixes[j].Rank[0] {
			return suffixes[i].Rank[0] < suffixes[j].Rank[0]
		}
		return suffixes[i].Rank[1] < suffixes[j].Rank[1]
	})

	// Build initial rank array
	for i := 0; i < n; i++ {
		rank[suffixes[i].Index] = i
	}

	// Prefix doubling
	for k := 4; k < 2*n; k *= 2 {
		// Update ranks for sorting
		for i := 0; i < n; i++ {
			curr := suffixes[i].Index
			suffixes[i].Rank[0] = rank[curr]
			if curr+k/2 < n {
				suffixes[i].Rank[1] = rank[curr+k/2]
			} else {
				suffixes[i].Rank[1] = -1
			}
		}

		// Sort suffixes
		sort.Slice(suffixes, func(i, j int) bool {
			if suffixes[i].Rank[0] != suffixes[j].Rank[0] {
				return suffixes[i].Rank[0] < suffixes[j].Rank[0]
			}
			return suffixes[i].Rank[1] < suffixes[j].Rank[1]
		})

		// Update ranks
		tempRank := make([]int, n)
		tempRank[suffixes[0].Index] = 0

		for i := 1; i < n; i++ {
			prev := suffixes[i-1]
			curr := suffixes[i]

			// Same rank if both pairs are equal
			if curr.Rank[0] == prev.Rank[0] && curr.Rank[1] == prev.Rank[1] {
				tempRank[curr.Index] = tempRank[prev.Index]
			} else {
				tempRank[curr.Index] = tempRank[prev.Index] + 1
			}
		}

		rank = tempRank
	}

	// Build suffix array from sorted suffixes
	for i := 0; i < n; i++ {
		sa.sa[i] = suffixes[i].Index
	}
}

// BuildLCP builds the LCP array using Kasai's algorithm
// Time: O(n)
// Space: O(n)
//
// LCP[i] = length of longest common prefix between
//          suffix[SA[i]] and suffix[SA[i-1]]
func (sa *SuffixArray) BuildLCP() {
	n := len(sa.text)
	sa.lcp = make([]int, n)

	if n == 0 {
		return
	}

	// Compute inverse suffix array (rank)
	rank := make([]int, n)
	for i := 0; i < n; i++ {
		rank[sa.sa[i]] = i
	}

	h := 0 // Height of LCP

	for i := 0; i < n; i++ {
		if rank[i] > 0 {
			j := sa.sa[rank[i]-1]

			// Compute LCP
			for i+h < n && j+h < n && sa.text[i+h] == sa.text[j+h] {
				h++
			}

			sa.lcp[rank[i]] = h

			// Decrease h for next iteration
			if h > 0 {
				h--
			}
		}
	}
}

// PatternSearch searches for pattern using binary search on suffix array
// Time: O(m log n)
// Returns: Slice of starting positions
func (sa *SuffixArray) PatternSearch(pattern string) []int {
	n := len(sa.text)
	m := len(pattern)
	matches := []int{}

	if m == 0 || n == 0 {
		return matches
	}

	// Binary search for lower bound
	lower := sort.Search(n, func(i int) bool {
		suffix := sa.text[sa.sa[i]:]
		return suffix >= pattern
	})

	// Binary search for upper bound
	upper := sort.Search(n, func(i int) bool {
		suffix := sa.text[sa.sa[i]:]
		if len(suffix) < m {
			return suffix > pattern[:len(suffix)]
		}
		return suffix[:m] > pattern
	})

	// Collect all matches
	for i := lower; i < upper; i++ {
		if strings.HasPrefix(sa.text[sa.sa[i]:], pattern) {
			matches = append(matches, sa.sa[i])
		}
	}

	return matches
}

// LongestRepeatedSubstring finds the longest repeated substring
// Time: O(n)
func (sa *SuffixArray) LongestRepeatedSubstring() string {
	if len(sa.lcp) == 0 {
		return ""
	}

	maxLCP := 0
	maxIdx := 0

	// Find maximum LCP value
	for i := 1; i < len(sa.lcp); i++ {
		if sa.lcp[i] > maxLCP {
			maxLCP = sa.lcp[i]
			maxIdx = i
		}
	}

	if maxLCP == 0 {
		return ""
	}

	return sa.text[sa.sa[maxIdx] : sa.sa[maxIdx]+maxLCP]
}

// CountDistinctSubstrings counts the number of distinct substrings
// Time: O(n)
// Formula: n*(n+1)/2 - sum(LCP)
func (sa *SuffixArray) CountDistinctSubstrings() int64 {
	n := int64(len(sa.text))
	total := n * (n + 1) / 2

	var duplicates int64
	for i := 1; i < len(sa.lcp); i++ {
		duplicates += int64(sa.lcp[i])
	}

	return total - duplicates
}

// Visualize prints the suffix array and LCP array
func (sa *SuffixArray) Visualize() {
	fmt.Printf("\nSuffix Array Visualization:\n")
	fmt.Printf("Text: '%s'\n", sa.text)
	fmt.Printf("Length: %d\n\n", len(sa.text))

	fmt.Printf("%-4s | %-6s | %-6s | Suffix\n", "i", "SA[i]", "LCP[i]")
	fmt.Println(strings.Repeat("-", 70))

	for i := 0; i < len(sa.sa); i++ {
		suffix := sa.text[sa.sa[i]:]
		if len(suffix) > 40 {
			suffix = suffix[:37] + "..."
		}
		fmt.Printf("%-4d | %-6d | %-6d | %s\n", i, sa.sa[i], sa.lcp[i], suffix)
	}
	fmt.Println()
}

// LongestCommonSubstring finds the longest common substring between two strings
// Time: O(n + m)
func LongestCommonSubstring(text1, text2 string) string {
	// Concatenate with separator
	separator := "#"
	combined := text1 + separator + text2
	len1 := len(text1)

	// Build suffix array
	sa := NewSuffixArray(combined)

	// Find max LCP where adjacent suffixes are from different strings
	maxLCP := 0
	maxPos := 0

	for i := 1; i < len(sa.sa); i++ {
		pos1 := sa.sa[i-1]
		pos2 := sa.sa[i]

		// One before separator, one after
		if (pos1 < len1) != (pos2 < len1) {
			if sa.lcp[i] > maxLCP {
				maxLCP = sa.lcp[i]
				maxPos = sa.sa[i]
			}
		}
	}

	if maxLCP == 0 {
		return ""
	}

	return combined[maxPos : maxPos+maxLCP]
}

// Benchmark measures suffix array construction time
func BenchmarkConstruction(text string) time.Duration {
	start := time.Now()
	NewSuffixArray(text)
	return time.Since(start)
}

// =========================================================================
// EXAMPLES AND TESTING
// =========================================================================

func exampleBasicConstruction() {
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println("EXAMPLE 1: Basic Suffix Array Construction")
	fmt.Println(strings.Repeat("=", 70))

	text := "banana"
	sa := NewSuffixArray(text)
	sa.Visualize()
}

func examplePatternSearch() {
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println("EXAMPLE 2: Pattern Searching")
	fmt.Println(strings.Repeat("=", 70))

	text := "the quick brown fox jumps over the lazy dog"
	pattern := "the"

	sa := NewSuffixArray(text)
	matches := sa.PatternSearch(pattern)

	fmt.Printf("Text: '%s'\n", text)
	fmt.Printf("Pattern: '%s'\n", pattern)
	fmt.Printf("Matches at positions: %v\n\n", matches)

	for _, pos := range matches {
		fmt.Printf("  Position %d: '%s'\n", pos, text[pos:pos+len(pattern)])
	}
	fmt.Println()
}

func exampleLongestRepeatedSubstring() {
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println("EXAMPLE 3: Longest Repeated Substring")
	fmt.Println(strings.Repeat("=", 70))

	text := "abracadabra"
	sa := NewSuffixArray(text)
	lrs := sa.LongestRepeatedSubstring()

	fmt.Printf("Text: '%s'\n", text)
	fmt.Printf("Longest repeated substring: '%s'\n\n", lrs)
}

func exampleCountDistinct() {
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println("EXAMPLE 4: Count Distinct Substrings")
	fmt.Println(strings.Repeat("=", 70))

	text := "abab"
	sa := NewSuffixArray(text)
	count := sa.CountDistinctSubstrings()

	fmt.Printf("Text: '%s'\n", text)
	fmt.Printf("Number of distinct substrings: %d\n\n", count)
}

func exampleLongestCommonSubstring() {
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println("EXAMPLE 5: Longest Common Substring")
	fmt.Println(strings.Repeat("=", 70))

	text1 := "algorithms"
	text2 := "altruistic"
	lcs := LongestCommonSubstring(text1, text2)

	fmt.Printf("Text 1: '%s'\n", text1)
	fmt.Printf("Text 2: '%s'\n", text2)
	fmt.Printf("Longest common substring: '%s'\n\n", lcs)
}

func exampleBenchmark() {
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println("EXAMPLE 6: Performance Benchmarking")
	fmt.Println(strings.Repeat("=", 70))

	// Small text
	smallText := strings.Repeat("banana", 10)
	smallTime := BenchmarkConstruction(smallText)
	fmt.Printf("Small text (length %d): %v\n", len(smallText), smallTime)

	// Medium text
	mediumText := strings.Repeat("abracadabra", 100)
	mediumTime := BenchmarkConstruction(mediumText)
	fmt.Printf("Medium text (length %d): %v\n\n", len(mediumText), mediumTime)
}

func main() {
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println("SUFFIX ARRAY AND LCP ARRAY IN GO")
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println()

	exampleBasicConstruction()
	examplePatternSearch()
	exampleLongestRepeatedSubstring()
	exampleCountDistinct()
	exampleLongestCommonSubstring()
	exampleBenchmark()

	fmt.Println(strings.Repeat("=", 70))
	fmt.Println("All examples completed successfully!")
	fmt.Println(strings.Repeat("=", 70))
}
