// Insertion Sort Algorithm Implementation in Go
//
// Time Complexity:
// - Best Case: O(n) - when array is already sorted
// - Average Case: O(n²)
// - Worst Case: O(n²) - when array is reverse sorted
// Space Complexity: O(1) for in-place, O(n) for functional approach
//
// Insertion Sort builds the final sorted array one item at a time.
//
// Go features:
// - Generic functions using type parameters (Go 1.18+)
// - Idiomatic Go patterns
// - Interface-based polymorphism
// - Benchmarking support

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

// InsertionSort performs standard insertion sort.
//
// Time Complexity: O(n²) average and worst case, O(n) best case
// Space Complexity: O(n) for the new slice
//
// Example visualization:
//   Initial: [5, 2, 8, 6, 1]
//   Step 1:  [2, 5, 8, 6, 1]  // Insert 2
//   Step 2:  [2, 5, 8, 6, 1]  // 8 already in place
//   Step 3:  [2, 5, 6, 8, 1]  // Insert 6
//   Step 4:  [1, 2, 5, 6, 8]  // Insert 1
func InsertionSort[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	InsertionSortInPlace(result)
	return result
}

// InsertionSortInPlace sorts the slice in-place.
//
// Time Complexity: O(n²) average and worst case, O(n) best case
// Space Complexity: O(1)
func InsertionSortInPlace[T Ordered](arr []T) {
	for i := 1; i < len(arr); i++ {
		key := arr[i]
		j := i - 1

		// Move elements greater than key one position ahead
		for j >= 0 && arr[j] > key {
			arr[j+1] = arr[j]
			j--
		}

		arr[j+1] = key
	}
}

// InsertionSortRecursive performs recursive insertion sort.
//
// Time Complexity: O(n²)
// Space Complexity: O(n) for recursion stack
func InsertionSortRecursive[T Ordered](arr []T) []T {
	result := make([]T, len(arr))
	copy(result, arr)
	insertionSortRecursiveHelper(result, len(result))
	return result
}

func insertionSortRecursiveHelper[T Ordered](arr []T, n int) {
	// Base case
	if n <= 1 {
		return
	}

	// Sort first n-1 elements
	insertionSortRecursiveHelper(arr, n-1)

	// Insert last element at its correct position
	key := arr[n-1]
	j := n - 2

	for j >= 0 && arr[j] > key {
		arr[j+1] = arr[j]
		j--
	}

	arr[j+1] = key
}

// BinaryInsertionSort uses binary search to find insertion position.
//
// Time Complexity: O(n²) for moves, O(n log n) for comparisons
// Space Complexity: O(n)
func BinaryInsertionSort[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)

	for i := 1; i < len(result); i++ {
		key := result[i]

		// Find position using binary search
		pos := binarySearchPosition(result, 0, i-1, key)

		// Shift elements to make space
		for j := i - 1; j >= pos; j-- {
			result[j+1] = result[j]
		}

		result[pos] = key
	}

	return result
}

func binarySearchPosition[T Ordered](arr []T, left, right int, key T) int {
	if right <= left {
		if key > arr[left] {
			return left + 1
		}
		return left
	}

	mid := (left + right) / 2

	if key == arr[mid] {
		return mid + 1
	}

	if key > arr[mid] {
		return binarySearchPosition(arr, mid+1, right, key)
	}

	return binarySearchPosition(arr, left, mid-1, key)
}

// ShellSort performs shell sort (generalization of insertion sort).
//
// Time Complexity: Depends on gap sequence (O(n log²n) for good sequences)
func ShellSort[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	n := len(result)

	// Start with a large gap, then reduce (Knuth's sequence)
	gap := 1
	for gap < n/3 {
		gap = 3*gap + 1
	}

	// Perform gapped insertion sort
	for gap > 0 {
		for i := gap; i < n; i++ {
			key := result[i]
			j := i

			// Insertion sort with gap
			for j >= gap && result[j-gap] > key {
				result[j] = result[j-gap]
				j -= gap
			}

			result[j] = key
		}

		gap /= 3
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
}

// Reset resets all statistics to zero
func (s *SortStatistics) Reset() {
	s.Comparisons = 0
	s.Swaps = 0
}

// String returns a string representation of the statistics
func (s *SortStatistics) String() string {
	return fmt.Sprintf("Comparisons: %d, Swaps: %d", s.Comparisons, s.Swaps)
}

// InsertionSortWithStats sorts and tracks statistics
func InsertionSortWithStats[T Ordered](arr []T, stats *SortStatistics) []T {
	stats.Reset()

	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)

	for i := 1; i < len(result); i++ {
		key := result[i]
		j := i - 1

		for j >= 0 {
			stats.Comparisons++
			if result[j] > key {
				result[j+1] = result[j]
				stats.Swaps++
				j--
			} else {
				break
			}
		}

		result[j+1] = key
	}

	return result
}

// VisualizeInsertionSort creates a step-by-step visualization
func VisualizeInsertionSort(arr []int) []string {
	steps := []string{}
	result := make([]int, len(arr))
	copy(result, arr)

	steps = append(steps, fmt.Sprintf("Initial: %v", result))

	for i := 1; i < len(result); i++ {
		key := result[i]
		j := i - 1

		steps = append(steps, fmt.Sprintf("\nStep %d: Inserting %d", i, key))
		steps = append(steps, fmt.Sprintf("  Before: %v", result))

		for j >= 0 && result[j] > key {
			result[j+1] = result[j]
			j--
		}

		result[j+1] = key
		steps = append(steps, fmt.Sprintf("  After:  %v", result))
	}

	steps = append(steps, fmt.Sprintf("\nFinal: %v", result))
	return steps
}

// DemonstrateStability shows that insertion sort is stable
func DemonstrateStability() {
	type Pair struct {
		Value         int
		OriginalIndex int
	}

	data := []Pair{
		{3, 0}, {1, 1}, {3, 2}, {2, 3}, {3, 4},
	}

	// Custom sort function that only compares values
	sortFunc := func(arr []Pair) []Pair {
		result := make([]Pair, len(arr))
		copy(result, arr)

		for i := 1; i < len(result); i++ {
			key := result[i]
			j := i - 1

			for j >= 0 && result[j].Value > key.Value {
				result[j+1] = result[j]
				j--
			}

			result[j+1] = key
		}

		return result
	}

	fmt.Println("Stability Demonstration:")
	fmt.Print("Original: ")
	for _, p := range data {
		fmt.Printf("(%d,%d) ", p.Value, p.OriginalIndex)
	}
	fmt.Println()

	sorted := sortFunc(data)
	fmt.Print("Sorted:   ")
	for _, p := range sorted {
		fmt.Printf("(%d,%d) ", p.Value, p.OriginalIndex)
	}
	fmt.Println()

	// Check stability
	var threeIndices []int
	for _, p := range sorted {
		if p.Value == 3 {
			threeIndices = append(threeIndices, p.OriginalIndex)
		}
	}

	isStable := len(threeIndices) == 3 && threeIndices[0] == 0 && threeIndices[1] == 2 && threeIndices[2] == 4
	fmt.Printf("Stable: %v (indices of 3's: %v)\n", isStable, threeIndices)
}

// Helper function to print a slice
func printSlice[T any](arr []T, label string) {
	fmt.Printf("%s: %v\n", label, arr)
}

// DemonstrateInsertionSort demonstrates various implementations
func DemonstrateInsertionSort() {
	fmt.Println("📝 Insertion Sort Implementation in Go")
	fmt.Println(strings.Repeat("=", 60))

	// Test data
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
		{[]int{1, 3, 2, 4, 5}, "Nearly sorted"},
	}

	fmt.Println("\n📋 Basic Sorting Tests:")
	fmt.Println(strings.Repeat("-", 60))

	for _, tc := range testCases {
		original := make([]int, len(tc.arr))
		copy(original, tc.arr)

		standardResult := InsertionSort(tc.arr)
		binaryResult := BinaryInsertionSort(tc.arr)
		shellResult := ShellSort(tc.arr)
		recursiveResult := InsertionSortRecursive(tc.arr)

		fmt.Printf("\nTest: %s\n", tc.desc)
		printSlice(original, "Original")
		printSlice(standardResult, "Sorted  ")

		allCorrect := IsSorted(standardResult) && IsSorted(binaryResult) &&
			IsSorted(shellResult) && IsSorted(recursiveResult)
		allEqual := slicesEqual(standardResult, binaryResult) &&
			slicesEqual(standardResult, shellResult) &&
			slicesEqual(standardResult, recursiveResult)

		status := "✓"
		if !allCorrect || !allEqual {
			status = "✗"
		}
		fmt.Printf("All implementations match: %s\n", status)
	}

	// Visualization demo
	fmt.Println("\n\n🎬 Step-by-Step Visualization:")
	fmt.Println(strings.Repeat("-", 60))

	demoArr := []int{5, 2, 8, 6, 1}
	steps := VisualizeInsertionSort(demoArr)
	for _, step := range steps {
		fmt.Println(step)
	}

	// Stability demonstration
	fmt.Println("\n\n🔒 Stability Demonstration:")
	fmt.Println(strings.Repeat("-", 60))
	DemonstrateStability()

	// Performance analysis
	fmt.Println("\n\n📊 Operation Counting:")
	fmt.Println(strings.Repeat("-", 60))

	statTestCases := []TestCase{
		{[]int{5, 2, 8, 6, 1}, "Random"},
		{[]int{1, 2, 3, 4, 5}, "Already sorted"},
		{[]int{5, 4, 3, 2, 1}, "Reverse sorted"},
	}

	for _, tc := range statTestCases {
		stats := &SortStatistics{}
		InsertionSortWithStats(tc.arr, stats)

		n := len(tc.arr)
		fmt.Printf("\n%s: %v\n", tc.desc, tc.arr)
		fmt.Printf("Array size (n): %d\n", n)
		fmt.Printf("Comparisons: %d\n", stats.Comparisons)
		fmt.Printf("Swaps: %d\n", stats.Swaps)
		fmt.Printf("Best case comparisons: %d\n", n-1)
		fmt.Printf("Worst case comparisons: %d\n", n*(n-1)/2)
	}
}

// PerformanceBenchmark benchmarks insertion sort
func PerformanceBenchmark() {
	fmt.Println("\n\n⚡ Performance Benchmark")
	fmt.Println(strings.Repeat("=", 80))
	fmt.Println("\nInsertion sort is preferred for:")
	fmt.Println("  • Small arrays (typically n < 10-20)")
	fmt.Println("  • Nearly sorted arrays")
	fmt.Println("  • As part of hybrid sorting algorithms")
	fmt.Println()

	sizes := []int{5, 10, 20, 50, 100, 500, 1000}

	patterns := map[string]func(int) []int{
		"Random": func(n int) []int {
			rand.Seed(42)
			arr := make([]int, n)
			for i := range arr {
				arr[i] = rand.Intn(1000) + 1
			}
			return arr
		},
		"Nearly Sorted": func(n int) []int {
			arr := make([]int, n)
			for i := range arr {
				arr[i] = i
			}
			for i := 0; i < min(5, n/10); i++ {
				idx1 := rand.Intn(n)
				idx2 := rand.Intn(n)
				arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
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
	}

	for patternName, patternGen := range patterns {
		fmt.Printf("\n%s Data:\n", patternName)
		fmt.Printf("%-8s%15s%15s%15s%15s\n", "Size", "Insertion", "Binary", "Shell", "sort.Ints")
		fmt.Println(strings.Repeat("-", 68))

		for _, size := range sizes {
			testData := patternGen(size)
			fmt.Printf("%-8d", size)

			// Insertion Sort
			start := time.Now()
			InsertionSort(testData)
			elapsed := time.Since(start)
			fmt.Printf("%14.3fms", float64(elapsed.Microseconds())/1000.0)

			// Binary Insertion Sort
			start = time.Now()
			BinaryInsertionSort(testData)
			elapsed = time.Since(start)
			fmt.Printf("%14.3fms", float64(elapsed.Microseconds())/1000.0)

			// Shell Sort
			start = time.Now()
			ShellSort(testData)
			elapsed = time.Since(start)
			fmt.Printf("%14.3fms", float64(elapsed.Microseconds())/1000.0)

			// sort.Ints
			testData2 := make([]int, len(testData))
			copy(testData2, testData)
			start = time.Now()
			sort.Ints(testData2)
			elapsed = time.Since(start)
			fmt.Printf("%14.3fms\n", float64(elapsed.Microseconds())/1000.0)
		}
	}
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

// Helper function for min of two ints
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func main() {
	DemonstrateInsertionSort()
	PerformanceBenchmark()

	fmt.Println("\n✨ Insertion Sort demonstration complete!")
}
