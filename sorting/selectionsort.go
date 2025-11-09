// Selection Sort Algorithm - Educational Implementation (Go)
//
// ALGORITHM OVERVIEW:
// ==================
// Selection Sort works by repeatedly finding the minimum element from the unsorted
// portion of the array and placing it at the beginning. It divides the array into
// two parts: a sorted portion (left) and an unsorted portion (right).
//
// Time Complexity:
// - Best Case: O(n²) - Even if array is already sorted, still searches for minimum
// - Average Case: O(n²)
// - Worst Case: O(n²)
// - IMPORTANT: Unlike bubble sort and insertion sort, selection sort ALWAYS performs
//   O(n²) comparisons, regardless of input
//
// Space Complexity: O(1) - Sorts in-place with only constant extra space
//
// Stability: NOT stable by default (can be made stable with modifications)
// In-place: YES
//
// KEY ADVANTAGE: Makes MINIMUM number of swaps - only O(n) swaps!

package main

import (
	"fmt"
	"math/rand"
	"strings"
	"time"
)

// ============================================================================
// ORDERED CONSTRAINT
// ============================================================================

// Ordered is a constraint that permits any ordered type
type Ordered interface {
	~int | ~int8 | ~int16 | ~int32 | ~int64 |
		~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~uintptr |
		~float32 | ~float64 |
		~string
}

// ============================================================================
// STANDARD SELECTION SORT
// ============================================================================

// SelectionSort performs standard selection sort on a generic slice.
//
// ALGORITHM STEPS:
// ===============
// 1. Find the minimum element in the unsorted portion
// 2. Swap it with the first element of the unsorted portion
// 3. Move the boundary of sorted/unsorted portions one element to the right
// 4. Repeat until the entire array is sorted
//
// Visual Example:
// ==============
// Initial: [64, 25, 12, 22, 11]
//
// Pass 1: Find min in [64, 25, 12, 22, 11] → 11
//         Swap 64 ↔ 11
//         Result: [11, 25, 12, 22, 64]
//                  ^^^ sorted portion
//
// Pass 2: Find min in [25, 12, 22, 64] → 12
//         Swap 25 ↔ 12
//         Result: [11, 12, 25, 22, 64]
//                  ^^^^^^^ sorted portion
//
// Time: O(n²), Space: O(n) for new slice
func SelectionSort[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	SelectionSortInPlace(result)
	return result
}

// SelectionSortInPlace sorts the slice in-place using selection sort.
//
// DETAILED STEP-BY-STEP:
// ======================
// For each position i from 0 to n-1:
//     - Assume arr[i] is the minimum
//     - Scan all elements from i+1 to n-1
//     - Track the index of the actual minimum element
//     - After scanning, swap arr[i] with the minimum element found
//
// Time: O(n²), Space: O(1)
func SelectionSortInPlace[T Ordered](arr []T) {
	n := len(arr)

	// Outer loop: Move boundary of unsorted subarray one by one
	for i := 0; i < n-1; i++ {
		// Find the minimum element in the remaining unsorted array
		// Start by assuming the first unsorted element is the minimum
		minIdx := i

		// Inner loop: Search for the minimum in arr[i+1...n-1]
		for j := i + 1; j < n; j++ {
			// If we find a smaller element, update minIdx
			if arr[j] < arr[minIdx] {
				minIdx = j
			}
		}

		// Swap the found minimum element with the first element
		// of the unsorted portion
		if minIdx != i {
			arr[i], arr[minIdx] = arr[minIdx], arr[i]
		}
	}
}

// ============================================================================
// BIDIRECTIONAL SELECTION SORT
// ============================================================================

// BidirectionalSelectionSort performs bidirectional selection sort.
//
// OPTIMIZATION:
// ============
// Instead of finding just the minimum in each pass, we find BOTH the minimum
// and maximum elements. We place the minimum at the beginning and the maximum
// at the end, reducing the number of passes by approximately half.
//
// Time: Still O(n²), but approximately 2x faster in practice
func BidirectionalSelectionSort[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	n := len(result)

	// Process from both ends toward the middle
	left := 0
	right := n - 1

	for left < right {
		// Find both minimum and maximum in the current range
		minIdx := left
		maxIdx := left

		for i := left; i <= right; i++ {
			if result[i] < result[minIdx] {
				minIdx = i
			}
			if result[i] > result[maxIdx] {
				maxIdx = i
			}
		}

		// Handle special case: if min is at right position
		if minIdx == right {
			result[left], result[right] = result[right], result[left]
			if maxIdx == left {
				maxIdx = right
			}
		} else {
			// Swap minimum to the left boundary
			if minIdx != left {
				result[left], result[minIdx] = result[minIdx], result[left]
			}

			// If maximum was at left position, it's now at minIdx
			if maxIdx == left {
				maxIdx = minIdx
			}

			// Swap maximum to the right boundary
			if maxIdx != right {
				result[right], result[maxIdx] = result[maxIdx], result[right]
			}
		}

		// Move boundaries inward
		left++
		right--
	}

	return result
}

// ============================================================================
// RECURSIVE SELECTION SORT
// ============================================================================

// SelectionSortRecursive performs recursive selection sort.
//
// RECURSIVE APPROACH:
// ==================
// Base case: Array of size 0 or 1 is already sorted
// Recursive case:
//     1. Find the minimum element in the array
//     2. Swap it with the first element
//     3. Recursively sort the rest of the array (excluding the first element)
//
// Time: O(n²), Space: O(n) for recursion stack
func SelectionSortRecursive[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	selectionSortRecursiveHelper(result, 0)
	return result
}

func selectionSortRecursiveHelper[T Ordered](arr []T, startIdx int) {
	// Base case: if we've reached the end, we're done
	if startIdx >= len(arr)-1 {
		return
	}

	// Find the minimum element in arr[startIdx...n-1]
	minIdx := startIdx
	for i := startIdx + 1; i < len(arr); i++ {
		if arr[i] < arr[minIdx] {
			minIdx = i
		}
	}

	// Swap the minimum with the element at startIdx
	if minIdx != startIdx {
		arr[startIdx], arr[minIdx] = arr[minIdx], arr[startIdx]
	}

	// Recursively sort the rest
	selectionSortRecursiveHelper(arr, startIdx+1)
}

// ============================================================================
// STABLE SELECTION SORT
// ============================================================================

// StableSelectionSort performs stable selection sort.
//
// WHY STANDARD SELECTION SORT IS UNSTABLE:
// ========================================
// When we swap the minimum element with the first element of the unsorted
// portion, we can change the relative order of equal elements.
//
// MAKING IT STABLE:
// ================
// Instead of swapping, we shift all elements and insert the minimum
// at the correct position. This preserves the relative order.
//
// Time: O(n²) comparisons + O(n²) shifts
func StableSelectionSort[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	n := len(result)

	for i := 0; i < n-1; i++ {
		// Find minimum in unsorted portion
		minIdx := i
		for j := i + 1; j < n; j++ {
			if result[j] < result[minIdx] {
				minIdx = j
			}
		}

		// Instead of swapping, shift elements and insert
		if minIdx != i {
			minValue := result[minIdx]
			// Shift all elements between i and minIdx one position right
			for k := minIdx; k > i; k-- {
				result[k] = result[k-1]
			}
			// Place minimum at position i
			result[i] = minValue
		}
	}

	return result
}

// ============================================================================
// VISUALIZATION AND STATISTICS
// ============================================================================

// SortStatistics tracks sorting operations
type SortStatistics struct {
	Comparisons   int
	Swaps         int
	ArrayAccesses int
}

// Reset resets all statistics to zero
func (s *SortStatistics) Reset() {
	s.Comparisons = 0
	s.Swaps = 0
	s.ArrayAccesses = 0
}

// String returns a string representation of the statistics
func (s *SortStatistics) String() string {
	return fmt.Sprintf("Comparisons: %d, Swaps: %d, Array Accesses: %d",
		s.Comparisons, s.Swaps, s.ArrayAccesses)
}

// SelectionSortWithStats sorts and tracks statistics
func SelectionSortWithStats[T Ordered](arr []T, stats *SortStatistics) []T {
	stats.Reset()

	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	n := len(result)

	for i := 0; i < n-1; i++ {
		minIdx := i
		stats.ArrayAccesses++

		for j := i + 1; j < n; j++ {
			stats.Comparisons++
			stats.ArrayAccesses += 2 // Read result[j] and result[minIdx]
			if result[j] < result[minIdx] {
				minIdx = j
			}
		}

		if minIdx != i {
			stats.Swaps++
			stats.ArrayAccesses += 4 // Two reads, two writes
			result[i], result[minIdx] = result[minIdx], result[i]
		}
	}

	return result
}

// VisualizeSelectionSort creates a step-by-step visualization
func VisualizeSelectionSort(arr []int) []string {
	steps := []string{}
	result := make([]int, len(arr))
	copy(result, arr)

	steps = append(steps, strings.Repeat("=", 70))
	steps = append(steps, "SELECTION SORT VISUALIZATION")
	steps = append(steps, strings.Repeat("=", 70))
	steps = append(steps, fmt.Sprintf("Initial array: %v", result))
	steps = append(steps, "")

	n := len(result)
	for i := 0; i < n-1; i++ {
		steps = append(steps, fmt.Sprintf("Pass %d:", i+1))
		steps = append(steps, fmt.Sprintf("  Looking for minimum in unsorted portion: %v", result[i:]))

		minIdx := i
		minValue := result[i]

		// Show the search process
		for j := i + 1; j < n; j++ {
			if result[j] < minValue {
				minIdx = j
				minValue = result[j]
				steps = append(steps, fmt.Sprintf("    Found new minimum: %d at index %d", minValue, minIdx))
			}
		}

		// Show the swap
		if minIdx != i {
			steps = append(steps, fmt.Sprintf("  Swapping %d ↔ %d", result[i], result[minIdx]))
			result[i], result[minIdx] = result[minIdx], result[i]
		} else {
			steps = append(steps, "  No swap needed (minimum already in place)")
		}

		// Show current state
		sorted := result[:i+1]
		unsorted := result[i+1:]
		steps = append(steps, fmt.Sprintf("  Sorted: %v | Unsorted: %v", sorted, unsorted))
		steps = append(steps, "")
	}

	steps = append(steps, fmt.Sprintf("Final sorted array: %v", result))
	steps = append(steps, strings.Repeat("=", 70))

	return steps
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

// ============================================================================
// DEMONSTRATION AND TESTING
// ============================================================================

func demonstrateSelectionSort() {
	fmt.Println("📚 SELECTION SORT - EDUCATIONAL DEMONSTRATION")
	fmt.Println(strings.Repeat("=", 80))

	// Test data
	type TestCase struct {
		arr  []int
		desc string
	}

	testCases := []TestCase{
		{[]int{64, 25, 12, 22, 11}, "Random array"},
		{[]int{5, 2, 8, 6, 1, 9, 4}, "Small random array"},
		{[]int{1}, "Single element"},
		{[]int{}, "Empty array"},
		{[]int{3, 3, 3, 3, 3}, "All duplicates"},
		{[]int{9, 8, 7, 6, 5, 4, 3, 2, 1}, "Reverse sorted"},
		{[]int{1, 2, 3, 4, 5}, "Already sorted"},
		{[]int{1, 3, 2, 4, 5}, "Nearly sorted"},
	}

	fmt.Println("\n📋 BASIC FUNCTIONALITY TESTS:")
	fmt.Println(strings.Repeat("-", 80))

	for _, tc := range testCases {
		original := make([]int, len(tc.arr))
		copy(original, tc.arr)

		standard := SelectionSort(tc.arr)
		bidirectional := BidirectionalSelectionSort(tc.arr)
		recursive := SelectionSortRecursive(tc.arr)
		stable := StableSelectionSort(tc.arr)

		fmt.Printf("\nTest: %s\n", tc.desc)
		fmt.Printf("Original:      %v\n", original)
		fmt.Printf("Standard:      %v\n", standard)
		fmt.Printf("Bidirectional: %v\n", bidirectional)
		fmt.Printf("Recursive:     %v\n", recursive)
		fmt.Printf("Stable:        %v\n", stable)

		allCorrect := IsSorted(standard) && IsSorted(bidirectional) &&
			IsSorted(recursive) && IsSorted(stable)

		status := "✓"
		if !allCorrect {
			status = "✗"
		}
		fmt.Printf("All correct: %s\n", status)
	}

	// Visualization
	fmt.Println("\n\n🎬 STEP-BY-STEP VISUALIZATION:")
	fmt.Println(strings.Repeat("-", 80))

	demoArr := []int{64, 25, 12, 22, 11}
	steps := VisualizeSelectionSort(demoArr)
	for _, step := range steps {
		fmt.Println(step)
	}

	// Memory analysis
	fmt.Println("\n\n💾 MEMORY USAGE ANALYSIS:")
	fmt.Println(strings.Repeat("-", 80))
	fmt.Println(`
Selection Sort Memory Characteristics:

1. In-Place Sorting:
   - Space Complexity: O(1) auxiliary space
   - Only uses constant extra memory (minIdx, loop variables)
   - Original array is modified in-place

2. Memory Writes:
   - Selection Sort: O(n) swaps (minimum writes)
   - Bubble Sort: O(n²) swaps in worst case
   - Insertion Sort: O(n²) shifts in worst case

   ⭐ This makes Selection Sort ideal when writing to memory is expensive!
      Examples: Flash memory, EEPROM, or distributed systems

3. Cache Performance:
   - Poor cache locality during the search for minimum
   - Each pass scans the entire unsorted portion
   - Comparison: Insertion sort has better cache performance
`)

	fmt.Println("\n📌 WHEN TO USE SELECTION SORT:")
	fmt.Println(strings.Repeat("-", 80))
	fmt.Println(`
✅ GOOD USE CASES:

1. Minimal Memory Writes:
   - Flash memory or EEPROM (limited write cycles)
   - Distributed systems where network writes are expensive

2. Small Datasets:
   - When simplicity matters more than efficiency
   - Educational purposes to understand sorting concepts

3. Known Small Data:
   - Embedded systems with small, fixed-size arrays
   - When n is guaranteed to be small (< 20 elements)

❌ POOR USE CASES:

1. Large Datasets:
   - Always O(n²) time, never adapts to input
   - Much slower than O(n log n) algorithms

2. Nearly Sorted Data:
   - Unlike insertion sort, doesn't benefit from sorted input
   - Still performs all O(n²) comparisons

3. Stable Sorting Required:
   - Standard selection sort is not stable
   - Making it stable adds overhead
`)
}

func performanceBenchmark() {
	fmt.Println("\n\n⚡ PERFORMANCE BENCHMARK")
	fmt.Println(strings.Repeat("=", 80))

	sizes := []int{10, 20, 50, 100, 200}

	patterns := map[string]func(int) []int{
		"Random": func(n int) []int {
			arr := make([]int, n)
			for i := range arr {
				arr[i] = rand.Intn(1000)
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
	}

	for patternName, patternGen := range patterns {
		fmt.Printf("\n%s Data:\n", patternName)
		fmt.Printf("%-10s%15s%15s%15s\n", "Size", "Standard", "Bidirectional", "Recursive")
		fmt.Println(strings.Repeat("-", 55))

		for _, size := range sizes {
			testData := patternGen(size)

			// Standard
			start := time.Now()
			SelectionSort(testData)
			timeStandard := time.Since(start).Seconds() * 1000

			// Bidirectional
			start = time.Now()
			BidirectionalSelectionSort(testData)
			timeBidirectional := time.Since(start).Seconds() * 1000

			// Recursive
			start = time.Now()
			SelectionSortRecursive(testData)
			timeRecursive := time.Since(start).Seconds() * 1000

			fmt.Printf("%-10d%14.3fms%14.3fms%14.3fms\n",
				size, timeStandard, timeBidirectional, timeRecursive)
		}
	}
}

func main() {
	demonstrateSelectionSort()
	performanceBenchmark()

	fmt.Println("\n✨ Selection Sort demonstration complete!")
}
