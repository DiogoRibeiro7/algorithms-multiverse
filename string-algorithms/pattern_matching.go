/**
 * Comprehensive String Pattern Matching Algorithms
 * =================================================
 *
 * This module implements six major pattern matching algorithms with detailed
 * explanations, preprocessing steps, performance analysis, and benchmarking.
 *
 * Algorithms:
 * 1. Knuth-Morris-Pratt (KMP)
 * 2. Boyer-Moore
 * 3. Rabin-Karp
 * 4. Aho-Corasick (multiple pattern matching)
 * 5. Z-algorithm
 * 6. Manacher's algorithm (palindrome detection)
 *
 * Run: go run pattern_matching.go
 */

package main

import (
	"fmt"
	"strings"
	"time"
)

// ============================================================================
// 1. KNUTH-MORRIS-PRATT (KMP) ALGORITHM
// ============================================================================

// KMP implements the Knuth-Morris-Pratt pattern matching algorithm
// Time: O(n + m), Space: O(m)
type KMP struct{}

// ComputeLPS computes the Longest Proper Prefix which is also Suffix array
// Time: O(m)
func (k *KMP) ComputeLPS(pattern string) []int {
	m := len(pattern)
	lps := make([]int, m)
	length := 0
	i := 1

	for i < m {
		if pattern[i] == pattern[length] {
			length++
			lps[i] = length
			i++
		} else {
			if length != 0 {
				length = lps[length-1]
			} else {
				lps[i] = 0
				i++
			}
		}
	}

	return lps
}

// Search finds all occurrences of pattern in text
// Time: O(n + m)
func (k *KMP) Search(text, pattern string, visualize bool) []int {
	if len(pattern) == 0 || len(text) == 0 {
		return []int{}
	}

	n := len(text)
	m := len(pattern)

	if m > n {
		return []int{}
	}

	lps := k.ComputeLPS(pattern)
	matches := []int{}

	i := 0 // Index for text
	j := 0 // Index for pattern

	if visualize {
		fmt.Println("\nKMP Algorithm Visualization:")
		fmt.Printf("Text:    %s\n", text)
		fmt.Printf("Pattern: %s\n", pattern)
		fmt.Printf("LPS:     %v\n\n", lps)
	}

	for i < n {
		if visualize && j == 0 {
			endIdx := i + m
			if endIdx > n {
				endIdx = n
			}
			fmt.Printf("Comparing at position %d: '%s'\n", i, text[i:endIdx])
		}

		if pattern[j] == text[i] {
			i++
			j++
		}

		if j == m {
			matches = append(matches, i-j)
			if visualize {
				fmt.Printf("✓ Match found at index %d\n", i-j)
			}
			j = lps[j-1]
		} else if i < n && pattern[j] != text[i] {
			if j != 0 {
				if visualize {
					fmt.Printf("  Mismatch at position %d, using LPS to skip to j=%d\n", i, lps[j-1])
				}
				j = lps[j-1]
			} else {
				i++
			}
		}
	}

	return matches
}

// ============================================================================
// 2. BOYER-MOORE ALGORITHM
// ============================================================================

// BoyerMoore implements the Boyer-Moore pattern matching algorithm
// Time: Best O(n/m), Average O(n), Worst O(n*m)
type BoyerMoore struct{}

// BadCharacterTable builds the bad character table
// Time: O(m + |Σ|)
func (bm *BoyerMoore) BadCharacterTable(pattern string) map[byte]int {
	table := make(map[byte]int)
	m := len(pattern)

	for i := 0; i < m; i++ {
		table[pattern[i]] = i
	}

	return table
}

// GoodSuffixTable builds the good suffix table
// Time: O(m)
func (bm *BoyerMoore) GoodSuffixTable(pattern string) []int {
	m := len(pattern)
	shift := make([]int, m+1)
	border := make([]int, m+1)

	i := m
	j := m + 1
	border[i] = j

	for i > 0 {
		for j <= m && pattern[i-1] != pattern[j-1] {
			if shift[j] == 0 {
				shift[j] = j - i
			}
			j = border[j]
		}

		i--
		j--
		border[i] = j
	}

	j = border[0]
	for i := 0; i <= m; i++ {
		if shift[i] == 0 {
			shift[i] = j
		}
		if i == j {
			j = border[j]
		}
	}

	return shift
}

// Search finds all occurrences using Boyer-Moore
// Time: O(n) average
func (bm *BoyerMoore) Search(text, pattern string, visualize bool) []int {
	if len(pattern) == 0 || len(text) == 0 {
		return []int{}
	}

	n := len(text)
	m := len(pattern)

	if m > n {
		return []int{}
	}

	badChar := bm.BadCharacterTable(pattern)
	goodSuffix := bm.GoodSuffixTable(pattern)

	matches := []int{}
	s := 0

	if visualize {
		fmt.Println("\nBoyer-Moore Algorithm Visualization:")
		fmt.Printf("Text:    %s\n", text)
		fmt.Printf("Pattern: %s\n\n", pattern)
	}

	for s <= n-m {
		j := m - 1

		if visualize {
			fmt.Printf("Checking at position %d: '%s'\n", s, text[s:s+m])
		}

		for j >= 0 && pattern[j] == text[s+j] {
			j--
		}

		if j < 0 {
			matches = append(matches, s)
			if visualize {
				fmt.Printf("✓ Match found at index %d\n", s)
			}
			s += goodSuffix[0]
		} else {
			badCharShift := j
			if val, ok := badChar[text[s+j]]; ok {
				badCharShift = j - val
			} else {
				badCharShift = j + 1
			}
			goodSuffixShift := goodSuffix[j+1]

			shift := badCharShift
			if goodSuffixShift > badCharShift {
				shift = goodSuffixShift
			}

			if visualize {
				fmt.Printf("  Mismatch at j=%d, shifting by %d\n", j, shift)
			}

			s += shift
		}
	}

	return matches
}

// ============================================================================
// 3. RABIN-KARP ALGORITHM
// ============================================================================

// RabinKarp implements the Rabin-Karp rolling hash algorithm
// Time: Average O(n + m), Worst O(n*m)
type RabinKarp struct {
	base  int64
	prime int64
}

// NewRabinKarp creates a new RabinKarp instance
func NewRabinKarp() *RabinKarp {
	return &RabinKarp{base: 256, prime: 101}
}

// Hash computes the hash value
func (rk *RabinKarp) Hash(s string, length int) int64 {
	var h int64 = 0
	for i := 0; i < length; i++ {
		h = (h*rk.base + int64(s[i])) % rk.prime
	}
	return h
}

// Search finds all occurrences using Rabin-Karp
// Time: O(n + m) average
func (rk *RabinKarp) Search(text, pattern string, visualize bool) []int {
	if len(pattern) == 0 || len(text) == 0 {
		return []int{}
	}

	n := len(text)
	m := len(pattern)

	if m > n {
		return []int{}
	}

	patternHash := rk.Hash(pattern, m)
	textHash := rk.Hash(text, m)

	var h int64 = 1
	for i := 0; i < m-1; i++ {
		h = (h * rk.base) % rk.prime
	}

	matches := []int{}

	if visualize {
		fmt.Println("\nRabin-Karp Algorithm Visualization:")
		fmt.Printf("Text:    %s\n", text)
		fmt.Printf("Pattern: %s\n", pattern)
		fmt.Printf("Pattern hash: %d\n\n", patternHash)
	}

	for i := 0; i <= n-m; i++ {
		if visualize {
			fmt.Printf("Position %d: hash=%d, substring='%s'\n", i, textHash, text[i:i+m])
		}

		if patternHash == textHash {
			if text[i:i+m] == pattern {
				matches = append(matches, i)
				if visualize {
					fmt.Printf("  ✓ Match found at index %d\n", i)
				}
			} else if visualize {
				fmt.Println("  ✗ Hash collision, not a real match")
			}
		}

		if i < n-m {
			textHash = (rk.base*(textHash-int64(text[i])*h) + int64(text[i+m])) % rk.prime

			if textHash < 0 {
				textHash += rk.prime
			}
		}
	}

	return matches
}

// ============================================================================
// 4. AHO-CORASICK ALGORITHM (MULTIPLE PATTERN MATCHING)
// ============================================================================

// TrieNode represents a node in the Aho-Corasick trie
type TrieNode struct {
	children map[byte]*TrieNode
	output   []int
	fail     *TrieNode
}

// AhoCorasick implements the Aho-Corasick multiple pattern matching algorithm
// Time: O(n + k) where k = number of matches
type AhoCorasick struct {
	root     *TrieNode
	patterns []string
}

// NewAhoCorasick creates a new Aho-Corasick instance
func NewAhoCorasick() *AhoCorasick {
	return &AhoCorasick{
		root:     &TrieNode{children: make(map[byte]*TrieNode), output: []int{}, fail: nil},
		patterns: []string{},
	}
}

// AddPattern adds a pattern to the trie
// Time: O(m)
func (ac *AhoCorasick) AddPattern(pattern string) {
	patternID := len(ac.patterns)
	ac.patterns = append(ac.patterns, pattern)

	node := ac.root
	for i := 0; i < len(pattern); i++ {
		c := pattern[i]
		if _, ok := node.children[c]; !ok {
			node.children[c] = &TrieNode{children: make(map[byte]*TrieNode), output: []int{}, fail: nil}
		}
		node = node.children[c]
	}

	node.output = append(node.output, patternID)
}

// BuildFailureLinks builds failure links using BFS
// Time: O(total pattern length)
func (ac *AhoCorasick) BuildFailureLinks() {
	queue := []*TrieNode{}

	for _, child := range ac.root.children {
		child.fail = ac.root
		queue = append(queue, child)
	}

	for len(queue) > 0 {
		current := queue[0]
		queue = queue[1:]

		for c, child := range current.children {
			queue = append(queue, child)

			failNode := current.fail
			for failNode != nil {
				if _, ok := failNode.children[c]; ok {
					break
				}
				failNode = failNode.fail
			}

			if failNode != nil {
				child.fail = failNode.children[c]
			} else {
				child.fail = ac.root
			}

			child.output = append(child.output, child.fail.output...)
		}
	}
}

// Search finds all occurrences of all patterns
// Time: O(n + k)
func (ac *AhoCorasick) Search(text string, visualize bool) map[int][]int {
	if len(text) == 0 {
		return map[int][]int{}
	}

	if len(ac.root.children) > 0 {
		// Check if failure links need to be built
		for _, child := range ac.root.children {
			if child.fail == nil {
				ac.BuildFailureLinks()
			}
			break
		}
	}

	results := make(map[int][]int)
	current := ac.root

	if visualize {
		fmt.Println("\nAho-Corasick Algorithm Visualization:")
		fmt.Printf("Text: %s\n", text)
		fmt.Printf("Patterns: %v\n\n", ac.patterns)
	}

	for i := 0; i < len(text); i++ {
		c := text[i]

		for current != nil {
			if _, ok := current.children[c]; ok {
				break
			}
			current = current.fail
		}

		if current == nil {
			current = ac.root
			continue
		}

		current = current.children[c]

		if len(current.output) > 0 {
			for _, patternID := range current.output {
				patternLen := len(ac.patterns[patternID])
				startIdx := i - patternLen + 1

				results[patternID] = append(results[patternID], startIdx)

				if visualize {
					fmt.Printf("✓ Found pattern '%s' at index %d\n", ac.patterns[patternID], startIdx)
				}
			}
		}
	}

	return results
}

// ============================================================================
// 5. Z-ALGORITHM
// ============================================================================

// ZAlgorithm implements the Z-algorithm for pattern matching
// Time: O(n + m), Space: O(n + m)
type ZAlgorithm struct{}

// ComputeZArray computes the Z-array
// Time: O(n)
func (z *ZAlgorithm) ComputeZArray(s string) []int {
	n := len(s)
	zArr := make([]int, n)
	zArr[0] = n

	l, r := 0, 0

	for i := 1; i < n; i++ {
		if i > r {
			l, r = i, i
			for r < n && s[r-l] == s[r] {
				r++
			}
			zArr[i] = r - l
			r--
		} else {
			k := i - l
			if zArr[k] < r-i+1 {
				zArr[i] = zArr[k]
			} else {
				l = i
				for r < n && s[r-l] == s[r] {
					r++
				}
				zArr[i] = r - l
				r--
			}
		}
	}

	return zArr
}

// Search finds all occurrences using Z-algorithm
// Time: O(n + m)
func (z *ZAlgorithm) Search(text, pattern string, visualize bool) []int {
	if len(pattern) == 0 || len(text) == 0 {
		return []int{}
	}

	n := len(text)
	m := len(pattern)

	if m > n {
		return []int{}
	}

	concat := pattern + "$" + text
	zArr := z.ComputeZArray(concat)

	matches := []int{}

	if visualize {
		fmt.Println("\nZ-Algorithm Visualization:")
		fmt.Printf("Text:    %s\n", text)
		fmt.Printf("Pattern: %s\n", pattern)
		fmt.Printf("Concatenation: %s\n", concat)
		fmt.Printf("Z-array: %v\n\n", zArr)
	}

	for i := m + 1; i < len(concat); i++ {
		if zArr[i] == m {
			matchPos := i - m - 1
			matches = append(matches, matchPos)
			if visualize {
				fmt.Printf("✓ Match found at index %d (Z[%d] = %d)\n", matchPos, i, m)
			}
		}
	}

	return matches
}

// ============================================================================
// 6. MANACHER'S ALGORITHM (PALINDROME DETECTION)
// ============================================================================

// Palindrome represents a palindrome substring
type Palindrome struct {
	Start int
	End   int
	Text  string
}

// Manacher implements Manacher's algorithm for finding palindromes
// Time: O(n), Space: O(n)
type Manacher struct{}

// Preprocess transforms string to handle even/odd palindromes uniformly
func (m *Manacher) Preprocess(s string) string {
	if len(s) == 0 {
		return "#"
	}

	var result strings.Builder
	result.WriteByte('#')
	for i := 0; i < len(s); i++ {
		result.WriteByte(s[i])
		result.WriteByte('#')
	}
	return result.String()
}

// FindAllPalindromes finds all palindromes in the string
// Time: O(n)
func (m *Manacher) FindAllPalindromes(s string, visualize bool) []Palindrome {
	if len(s) == 0 {
		return []Palindrome{}
	}

	t := m.Preprocess(s)
	n := len(t)
	p := make([]int, n)

	center := 0
	right := 0

	if visualize {
		fmt.Println("\nManacher's Algorithm Visualization:")
		fmt.Printf("Original: %s\n", s)
		fmt.Printf("Transformed: %s\n\n", t)
	}

	for i := 0; i < n; i++ {
		mirror := 2*center - i

		if i < right {
			p[i] = min(right-i, p[mirror])
		}

		for i+p[i]+1 < n && i-p[i]-1 >= 0 && t[i+p[i]+1] == t[i-p[i]-1] {
			p[i]++
		}

		if i+p[i] > right {
			center = i
			right = i + p[i]
		}
	}

	palindromes := []Palindrome{}
	for i := 0; i < n; i++ {
		if p[i] > 0 {
			start := (i - p[i]) / 2
			end := (i + p[i]) / 2
			if start < end {
				palindromes = append(palindromes, Palindrome{
					Start: start,
					End:   end,
					Text:  s[start:end],
				})
			}
		}
	}

	if visualize {
		fmt.Println("Palindromes found:")
		for _, pal := range palindromes {
			fmt.Printf("  [%d:%d] = '%s'\n", pal.Start, pal.End, pal.Text)
		}
	}

	return palindromes
}

// LongestPalindrome finds the longest palindromic substring
// Time: O(n)
func (m *Manacher) LongestPalindrome(s string) string {
	if len(s) == 0 {
		return ""
	}

	t := m.Preprocess(s)
	n := len(t)
	p := make([]int, n)

	center := 0
	right := 0

	for i := 0; i < n; i++ {
		mirror := 2*center - i

		if i < right {
			p[i] = min(right-i, p[mirror])
		}

		for i+p[i]+1 < n && i-p[i]-1 >= 0 && t[i+p[i]+1] == t[i-p[i]-1] {
			p[i]++
		}

		if i+p[i] > right {
			center = i
			right = i + p[i]
		}
	}

	maxLen := 0
	centerIndex := 0
	for i := 0; i < n; i++ {
		if p[i] > maxLen {
			maxLen = p[i]
			centerIndex = i
		}
	}

	start := (centerIndex - maxLen) / 2
	return s[start : start+maxLen]
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

// ============================================================================
// PERFORMANCE BENCHMARKING
// ============================================================================

// BenchmarkSinglePattern benchmarks single-pattern algorithms
func BenchmarkSinglePattern(text, pattern string, iterations int) {
	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("PERFORMANCE BENCHMARK")
	fmt.Println(strings.Repeat("=", 70))
	fmt.Printf("Text length: %d\n", len(text))
	fmt.Printf("Pattern length: %d\n", len(pattern))
	fmt.Printf("Iterations: %d\n\n", iterations)

	algorithms := []struct {
		name string
		fn   func()
	}{
		{"KMP", func() { new(KMP).Search(text, pattern, false) }},
		{"Boyer-Moore", func() { new(BoyerMoore).Search(text, pattern, false) }},
		{"Rabin-Karp", func() { NewRabinKarp().Search(text, pattern, false) }},
		{"Z-Algorithm", func() { new(ZAlgorithm).Search(text, pattern, false) }},
	}

	type result struct {
		name    string
		avgTime float64
	}
	results := []result{}

	for _, algo := range algorithms {
		start := time.Now()
		for i := 0; i < iterations; i++ {
			algo.fn()
		}
		elapsed := time.Since(start)

		avgTime := elapsed.Seconds() * 1000.0 / float64(iterations)
		results = append(results, result{algo.name, avgTime})

		fmt.Printf("%-15s | %8.4f ms\n", algo.name, avgTime)
	}

	// Find fastest
	minTime := results[0].avgTime
	minName := results[0].name
	for _, r := range results {
		if r.avgTime < minTime {
			minTime = r.avgTime
			minName = r.name
		}
	}

	fmt.Printf("\n✓ Fastest: %s (%.4f ms)\n", minName, minTime)
}

// ============================================================================
// EXAMPLE USAGE AND TESTING
// ============================================================================

func main() {
	fmt.Println(strings.Repeat("=", 70))
	fmt.Println("STRING PATTERN MATCHING ALGORITHMS")
	fmt.Println(strings.Repeat("=", 70))

	text := "ABABCABABABCABAB"
	pattern := "ABAB"

	fmt.Printf("\nTest Text: %s\n", text)
	fmt.Printf("Pattern: %s\n\n", pattern)

	// 1. KMP Algorithm
	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("1. KMP ALGORITHM")
	fmt.Println(strings.Repeat("=", 70))
	kmp := &KMP{}
	matches := kmp.Search(text, pattern, true)
	fmt.Printf("\nMatches found: %v\n", matches)

	// 2. Boyer-Moore Algorithm
	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("2. BOYER-MOORE ALGORITHM")
	fmt.Println(strings.Repeat("=", 70))
	bm := &BoyerMoore{}
	matches = bm.Search(text, pattern, true)
	fmt.Printf("\nMatches found: %v\n", matches)

	// 3. Rabin-Karp Algorithm
	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("3. RABIN-KARP ALGORITHM")
	fmt.Println(strings.Repeat("=", 70))
	rk := NewRabinKarp()
	matches = rk.Search(text, pattern, true)
	fmt.Printf("\nMatches found: %v\n", matches)

	// 4. Aho-Corasick Algorithm
	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("4. AHO-CORASICK ALGORITHM (Multiple Patterns)")
	fmt.Println(strings.Repeat("=", 70))
	ac := NewAhoCorasick()
	patterns := []string{"ABAB", "ABC", "CAB"}
	for _, p := range patterns {
		ac.AddPattern(p)
	}
	ac.BuildFailureLinks()
	results := ac.Search(text, true)
	fmt.Printf("\nAll matches: %v\n", results)

	// 5. Z-Algorithm
	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("5. Z-ALGORITHM")
	fmt.Println(strings.Repeat("=", 70))
	zAlgo := &ZAlgorithm{}
	matches = zAlgo.Search(text, pattern, true)
	fmt.Printf("\nMatches found: %v\n", matches)

	// 6. Manacher's Algorithm
	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("6. MANACHER'S ALGORITHM")
	fmt.Println(strings.Repeat("=", 70))
	palindromeText := "babad"
	manacher := &Manacher{}
	longest := manacher.LongestPalindrome(palindromeText)
	fmt.Printf("Text: %s\n", palindromeText)
	fmt.Printf("Longest palindrome: '%s'\n", longest)

	palindromes := manacher.FindAllPalindromes(palindromeText, true)
	_ = palindromes

	// Performance Benchmarking
	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("PERFORMANCE BENCHMARKING")
	fmt.Println(strings.Repeat("=", 70))

	benchmarkText := strings.Repeat("ABC", 1000)
	benchmarkPattern := "ABCABC"

	BenchmarkSinglePattern(benchmarkText, benchmarkPattern, 100)

	fmt.Println("\n" + strings.Repeat("=", 70))
}
