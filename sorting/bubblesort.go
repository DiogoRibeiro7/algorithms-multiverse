// Bubble Sort Algorithm Implementation in Go
//
// Time Complexity:
// - Best Case: O(n) - when array is already sorted (optimized version)
// - Average Case: O(n²)
// - Worst Case: O(n²) - when array is reverse sorted
// Space Complexity: O(1) for in-place, O(n) for functional approach
//
// Bubble Sort works by repeatedly stepping through the list, comparing adjacent
// elements and swapping them if they are in the wrong order. The pass through
// the list is repeated until the list is sorted.
//
// Go features:
// - Generic functions using type parameters (Go 1.18+)
// - Interface-based polymorphism
// - Idiomatic Go patterns
// - Benchmarking support
// - Custom comparison functions

package main

import (
	"fmt"
	"math/rand"
	"sort"
	"strings"
	"time"
)

// Ordered is a constraint that permits any ordered type
type Ordered interface {
	~int | ~int8 | ~int16 | ~int32 | ~int64 |
		~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~uintptr |
		~float32 | ~float64 |
		~string
}

// BubbleSortIterative is the basic iterative bubble sort implementation.
//
// This is the standard bubble sort algorithm that compares and swaps
// adjacent elements until the entire slice is sorted.
//
// Time Complexity: O(n²) in all cases (no optimization)
// Space Complexity: O(n) for the new slice
func BubbleSortIterative[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	n := len(result)

	// Outer loop for number of passes
	for i := 0; i < n; i++ {
		// Inner loop for comparisons
		// After each pass, the largest element "bubbles up" to its position
		for j := 0; j < n-i-1; j++ {
			if result[j] > result[j+1] {
				// Swap adjacent elements
				result[j], result[j+1] = result[j+1], result[j]
			}
		}
	}

	return result
}

// BubbleSortOptimized is an optimized bubble sort with early termination.
//
// This version includes a flag to detect if any swaps were made during a pass.
// If no swaps occur, the array is already sorted and we can terminate early.
//
// Time Complexity:
//   - Best Case: O(n) when already sorted
//   - Average/Worst: O(n²)
// Space Complexity: O(n) for the new slice
func BubbleSortOptimized[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	n := len(result)

	for i := 0; i < n; i++ {
		// Flag to optimize for already sorted arrays
		swapped := false

		for j := 0; j < n-i-1; j++ {
			if result[j] > result[j+1] {
				result[j], result[j+1] = result[j+1], result[j]
				swapped = true
			}
		}

		// If no swaps occurred, array is sorted
		if !swapped {
			break
		}
	}

	return result
}

// BubbleSortInPlace sorts the slice in-place (optimized).
//
// Sorts the slice in-place without creating a new slice,
// minimizing space complexity.
//
// Time Complexity: O(n) best case, O(n²) average/worst
// Space Complexity: O(1)
func BubbleSortInPlace[T Ordered](arr []T) {
	n := len(arr)

	for i := 0; i < n; i++ {
		swapped := false

		for j := 0; j < n-i-1; j++ {
			if arr[j] > arr[j+1] {
				arr[j], arr[j+1] = arr[j+1], arr[j]
				swapped = true
			}
		}

		if !swapped {
			break
		}
	}
}

// BubbleSortRecursive is a recursive bubble sort implementation.
//
// Each recursive call performs one pass through the array,
// bubbling the largest element to the end.
//
// Time Complexity: O(n²)
// Space Complexity: O(n) for recursion stack
func BubbleSortRecursive[T Ordered](arr []T) []T {
	result := make([]T, len(arr))
	copy(result, arr)
	bubbleSortRecursiveHelper(result, len(result))
	return result
}

func bubbleSortRecursiveHelper[T Ordered](arr []T, n int) {
	// Base case: single element or empty
	if n <= 1 {
		return
	}

	// One pass of bubble sort
	// After this pass, the largest element will be at the end
	for i := 0; i < n-1; i++ {
		if arr[i] > arr[i+1] {
			arr[i], arr[i+1] = arr[i+1], arr[i]
		}
	}

	// Recursively sort the first n-1 elements
	bubbleSortRecursiveHelper(arr, n-1)
}

// CompareFunc is a function type for custom comparisons
type CompareFunc[T any] func(a, b T) bool

// BubbleSortWithComparator sorts using a custom comparison function.
//
// The compare function should return true if a > b (for ascending order)
func BubbleSortWithComparator[T any](arr []T, compare CompareFunc[T]) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	n := len(result)

	for i := 0; i < n; i++ {
		swapped := false

		for j := 0; j < n-i-1; j++ {
			if compare(result[j], result[j+1]) {
				result[j], result[j+1] = result[j+1], result[j]
				swapped = true
			}
		}

		if !swapped {
			break
		}
	}

	return result
}

// CocktailSort is a bidirectional bubble sort.
//
// An optimized version of bubble sort that sorts in both directions
// alternately, which can be more efficient for certain data patterns.
//
// Time Complexity: O(n²) worst case, but often faster than standard bubble sort
// Space Complexity: O(n)
func CocktailSort[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	start := 0
	end := len(result) - 1
	swapped := true

	for swapped {
		swapped = false

		// Forward pass (like bubble sort)
		for i := start; i < end; i++ {
			if result[i] > result[i+1] {
				result[i], result[i+1] = result[i+1], result[i]
				swapped = true
			}
		}

		if !swapped {
			break
		}

		swapped = false
		end--

		// Backward pass
		for i := end - 1; i >= start; i-- {
			if result[i] > result[i+1] {
				result[i], result[i+1] = result[i+1], result[i]
				swapped = true
			}
		}

		start++
	}

	return result
}

// IsSorted checks if a slice is sorted in ascending order
func IsSorted[T Ordered](arr []T) bool {
	for i := 0; i < len(arr)-1; i++ {
		if arr[i] > arr[i+1] {
			return false
		}
	}
	return true
}

// SortStatistics tracks sorting operations
type SortStatistics struct {
	Comparisons int
	Swaps       int
	Iterations  int
}

// Reset resets all statistics to zero
func (s *SortStatistics) Reset() {
	s.Comparisons = 0
	s.Swaps = 0
	s.Iterations = 0
}

// String returns a string representation of the statistics
func (s *SortStatistics) String() string {
	return fmt.Sprintf("Comparisons: %d, Swaps: %d, Iterations: %d",
		s.Comparisons, s.Swaps, s.Iterations)
}

// BubbleSortWithStats sorts and tracks statistics
func BubbleSortWithStats[T Ordered](arr []T, stats *SortStatistics) []T {
	stats.Reset()

	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	n := len(result)

	for i := 0; i < n; i++ {
		stats.Iterations++
		swapped := false

		for j := 0; j < n-i-1; j++ {
			stats.Comparisons++
			if result[j] > result[j+1] {
				result[j], result[j+1] = result[j+1], result[j]
				stats.Swaps++
				swapped = true
			}
		}

		if !swapped {
			break
		}
	}

	return result
}

// BubbleSorter is a class-like structure with state
type BubbleSorter[T Ordered] struct {
	stats SortStatistics
}

// NewBubbleSorter creates a new BubbleSorter instance
func NewBubbleSorter[T Ordered]() *BubbleSorter[T] {
	return &BubbleSorter[T]{}
}

// Sort sorts the array and tracks statistics
func (bs *BubbleSorter[T]) Sort(arr []T) []T {
	return BubbleSortWithStats(arr, &bs.stats)
}

// GetStats returns the current statistics
func (bs *BubbleSorter[T]) GetStats() SortStatistics {
	return bs.stats
}

// ResetStats resets the statistics
func (bs *BubbleSorter[T]) ResetStats() {
	bs.stats.Reset()
}

// Helper function to print a slice
func printSlice[T any](arr []T, label string) {
	fmt.Printf("%s: %v\n", label, arr)
}

// DemonstrateBubbleSort demonstrates various bubble sort implementations
func DemonstrateBubbleSort() {
	fmt.Println("🫧 Bubble Sort Implementation in Go")
	fmt.Println(strings.Repeat("=", 50))

	// Test data - comprehensive edge cases
	type TestCase struct {
		arr  []int
		desc string
	}

	testCases := []TestCase{
		{[]int{64, 34, 25, 12, 22, 11, 90}, "Random array"},
		{[]int{5, 2, 8, 6, 1, 9, 4}, "Small random array"},
		{[]int{1}, "Single element"},
		{[]int{}, "Empty array"},
		{[]int{3, 3, 3, 3, 3}, "All duplicates"},
		{[]int{9, 8, 7, 6, 5, 4, 3, 2, 1}, "Reverse sorted"},
		{[]int{1, 2, 3, 4, 5}, "Already sorted"},
		{[]int{5, 1, 4, 2, 3}, "Nearly sorted"},
	}

	fmt.Println("\n📋 Basic Sorting Tests:")
	fmt.Println(strings.Repeat("-", 50))

	for _, tc := range testCases {
		// Make a copy to preserve original
		original := make([]int, len(tc.arr))
		copy(original, tc.arr)

		// Test different implementations
		iterativeResult := BubbleSortIterative(tc.arr)
		optimizedResult := BubbleSortOptimized(tc.arr)
		recursiveResult := BubbleSortRecursive(tc.arr)
		cocktailResult := CocktailSort(tc.arr)

		// Test in-place
		inplaceResult := make([]int, len(tc.arr))
		copy(inplaceResult, tc.arr)
		BubbleSortInPlace(inplaceResult)

		fmt.Printf("\nTest: %s\n", tc.desc)
		printSlice(original, "Original")
		printSlice(iterativeResult, "Sorted  ")

		// Verify all results are correct and equal
		allCorrect := IsSorted(iterativeResult) && IsSorted(optimizedResult) &&
			IsSorted(recursiveResult) && IsSorted(cocktailResult) &&
			IsSorted(inplaceResult)

		allEqual := slicesEqual(iterativeResult, optimizedResult) &&
			slicesEqual(iterativeResult, recursiveResult) &&
			slicesEqual(iterativeResult, cocktailResult) &&
			slicesEqual(iterativeResult, inplaceResult)

		status := "✓"
		if !allCorrect || !allEqual {
			status = "✗"
		}
		fmt.Printf("All implementations match: %s\n", status)
	}

	fmt.Println("\n" + strings.Repeat("-", 50))

	// String sorting
	words := []string{"banana", "apple", "cherry", "date", "elderberry"}
	sortedWords := BubbleSortOptimized(words)

	fmt.Println("\n🔤 Word sorting:")
	printSlice(words, "Original    ")
	printSlice(sortedWords, "Alphabetical")

	// Custom comparison (descending)
	numbers := []int{3, 1, 4, 1, 5, 9, 2, 6}
	descSorted := BubbleSortWithComparator(numbers, func(a, b int) bool {
		return a < b // Reverse comparison for descending order
	})

	fmt.Println("\n🔢 Custom comparison (descending):")
	printSlice(numbers, "Original  ")
	printSlice(descSorted, "Descending")
}

// Helper function to check if two slices are equal
func slicesEqual[T comparable](a, b []T) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

// PerformanceBenchmark benchmarks different bubble sort implementations
func PerformanceBenchmark() {
	fmt.Println("\n\n⚡ Performance Benchmark")
	fmt.Println(strings.Repeat("=", 70))

	sizes := []int{100, 500, 1000, 2000}

	// Test different data patterns
	type PatternFunc func(int) []int

	patterns := map[string]PatternFunc{
		"Random": func(n int) []int {
			rand.Seed(42)
			arr := make([]int, n)
			for i := range arr {
				arr[i] = rand.Intn(1000) + 1
			}
			return arr
		},
		"Sorted": func(n int) []int {
			arr := make([]int, n)
			for i := range arr {
				arr[i] = i
			}
			return arr
		},
		"Reversed": func(n int) []int {
			arr := make([]int, n)
			for i := range arr {
				arr[i] = n - i
			}
			return arr
		},
		"Nearly Sorted": func(n int) []int {
			arr := make([]int, n)
			for i := range arr {
				arr[i] = i
			}
			// Swap a few elements
			rand.Seed(42)
			for i := 0; i < min(5, n/10); i++ {
				idx1 := rand.Intn(n)
				idx2 := rand.Intn(n)
				arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
			}
			return arr
		},
	}

	type MethodFunc func([]int) []int

	methods := map[string]MethodFunc{
		"Iterative": BubbleSortIterative[int],
		"Optimized": BubbleSortOptimized[int],
		"Recursive": BubbleSortRecursive[int],
		"Cocktail":  CocktailSort[int],
		"sort.Ints": func(arr []int) []int {
			result := make([]int, len(arr))
			copy(result, arr)
			sort.Ints(result)
			return result
		},
	}

	for patternName, patternGen := range patterns {
		fmt.Printf("\n%s Data:\n", patternName)

		// Header
		fmt.Printf("%-8s", "Size")
		for methodName := range methods {
			fmt.Printf("%12s", methodName)
		}
		fmt.Println()
		fmt.Println(strings.Repeat("-", 8+12*len(methods)))

		for _, size := range sizes {
			testData := patternGen(size)
			fmt.Printf("%-8d", size)

			for methodName, methodFunc := range methods {
				// Skip recursive for large sizes
				if methodName == "Recursive" && size > 1000 {
					fmt.Printf("%12s", "N/A")
					continue
				}

				// Warm-up
				methodFunc(testData)

				// Benchmark
				start := time.Now()
				result := methodFunc(testData)
				elapsed := time.Since(start)

				elapsedMs := float64(elapsed.Microseconds()) / 1000.0
				fmt.Printf("%11.2fms", elapsedMs)

				// Verify correctness
				if !IsSorted(result) {
					fmt.Print(" ✗")
				}
			}

			fmt.Println()
		}
	}
}

// AnalyzeAlgorithm analyzes bubble sort behavior with different inputs
func AnalyzeAlgorithm() {
	fmt.Println("\n\n🔍 Algorithm Analysis")
	fmt.Println(strings.Repeat("=", 50))

	type TestCase struct {
		arr  []int
		desc string
	}

	testCases := []TestCase{
		{[]int{5, 2, 8, 6, 1}, "Random"},
		{[]int{1, 2, 3, 4, 5}, "Already sorted"},
		{[]int{5, 4, 3, 2, 1}, "Reverse sorted"},
	}

	for _, tc := range testCases {
		stats := &SortStatistics{}
		BubbleSortWithStats(tc.arr, stats)

		n := len(tc.arr)
		theoreticalMax := n * (n - 1) / 2

		fmt.Printf("\n%s: %v\n", tc.desc, tc.arr)
		fmt.Printf("Array size (n): %d\n", n)
		fmt.Printf("Comparisons: %d (theoretical max: %d)\n",
			stats.Comparisons, theoreticalMax)
		fmt.Printf("Swaps: %d\n", stats.Swaps)

		efficiency := 0.0
		if stats.Comparisons > 0 {
			efficiency = (1.0 - float64(stats.Swaps)/float64(stats.Comparisons)) * 100.0
		}
		fmt.Printf("Efficiency: %.1f%% (fewer swaps is better)\n", efficiency)
	}
}

// Helper function for min of two ints
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func main() {
	DemonstrateBubbleSort()
	PerformanceBenchmark()
	AnalyzeAlgorithm()

	// Demonstrate OOP approach
	fmt.Println("\n\n📊 Object-Oriented Approach")
	fmt.Println(strings.Repeat("=", 50))

	sorter := NewBubbleSorter[int]()
	testArray := []int{64, 34, 25, 12, 22, 11, 90}

	sortedArray := sorter.Sort(testArray)
	stats := sorter.GetStats()

	printSlice(testArray, "Original")
	printSlice(sortedArray, "Sorted  ")
	fmt.Printf("Statistics: %s\n", stats.String())

	fmt.Println("\n✨ Bubble Sort demonstration complete!")
}
