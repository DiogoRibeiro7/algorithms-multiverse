// Merge Sort Algorithm Implementation in Go
//
// Time Complexity: O(n log n) - consistently across all cases
// Space Complexity: O(n) for auxiliary arrays
//
// Merge Sort is a divide-and-conquer algorithm that divides the input array
// into two halves, recursively sorts them, and then merges the two sorted
// halves. It is stable and guarantees O(n log n) time complexity.
//
// Go features:
// - Generic functions using type parameters (Go 1.18+)
// - Parallel sorting with goroutines for large datasets
// - Channel-based synchronization for concurrent operations
// - Benchmarking and performance analysis
// - Memory-efficient in-place merge variants
// - Iterative (bottom-up) implementation

package main

import (
	"fmt"
	"math/rand"
	"sort"
	"strings"
	"sync"
	"time"
)

// Ordered is a constraint that permits any ordered type
type Ordered interface {
	~int | ~int8 | ~int16 | ~int32 | ~int64 |
		~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~uintptr |
		~float32 | ~float64 |
		~string
}

// MergeSort performs standard recursive merge sort
//
// Time Complexity: O(n log n)
// Space Complexity: O(n)
func MergeSort[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	mergeSortHelper(result, 0, len(result)-1)
	return result
}

// mergeSortHelper is the recursive helper for merge sort
func mergeSortHelper[T Ordered](arr []T, left, right int) {
	if left >= right {
		return
	}

	mid := left + (right-left)/2

	// Recursively sort left and right halves
	mergeSortHelper(arr, left, mid)
	mergeSortHelper(arr, mid+1, right)

	// Merge the sorted halves
	merge(arr, left, mid, right)
}

// merge merges two sorted subarrays arr[left..mid] and arr[mid+1..right]
func merge[T Ordered](arr []T, left, mid, right int) {
	// Create temporary arrays
	leftSize := mid - left + 1
	rightSize := right - mid

	leftArr := make([]T, leftSize)
	rightArr := make([]T, rightSize)

	// Copy data to temporary arrays
	copy(leftArr, arr[left:mid+1])
	copy(rightArr, arr[mid+1:right+1])

	// Merge the temporary arrays back
	i, j, k := 0, 0, left

	for i < leftSize && j < rightSize {
		if leftArr[i] <= rightArr[j] {
			arr[k] = leftArr[i]
			i++
		} else {
			arr[k] = rightArr[j]
			j++
		}
		k++
	}

	// Copy remaining elements
	for i < leftSize {
		arr[k] = leftArr[i]
		i++
		k++
	}

	for j < rightSize {
		arr[k] = rightArr[j]
		j++
		k++
	}
}

// MergeSortParallel performs parallel merge sort using goroutines
//
// Uses goroutines to sort subarrays concurrently when array size
// exceeds the threshold. This can significantly improve performance
// on multi-core systems for large datasets.
//
// Time Complexity: O(n log n)
// Space Complexity: O(n)
// Concurrency: Utilizes multiple CPU cores
func MergeSortParallel[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)

	// Threshold for switching to parallel execution
	const threshold = 1000

	mergeSortParallelHelper(result, 0, len(result)-1, threshold)
	return result
}

// mergeSortParallelHelper implements parallel merge sort with threshold
func mergeSortParallelHelper[T Ordered](arr []T, left, right, threshold int) {
	if left >= right {
		return
	}

	// Use sequential sort for small arrays
	if right-left+1 < threshold {
		mergeSortHelper(arr, left, right)
		return
	}

	mid := left + (right-left)/2

	// Sort halves in parallel using goroutines
	var wg sync.WaitGroup
	wg.Add(2)

	go func() {
		defer wg.Done()
		mergeSortParallelHelper(arr, left, mid, threshold)
	}()

	go func() {
		defer wg.Done()
		mergeSortParallelHelper(arr, mid+1, right, threshold)
	}()

	wg.Wait()

	// Merge the sorted halves
	merge(arr, left, mid, right)
}

// MergeSortIterative performs bottom-up iterative merge sort
//
// Avoids recursion overhead by using an iterative approach.
// Sorts subarrays of increasing size (1, 2, 4, 8, ...).
//
// Time Complexity: O(n log n)
// Space Complexity: O(n)
func MergeSortIterative[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	n := len(result)

	// Start with merge subarrays of size 1, then 2, 4, 8, ...
	for size := 1; size < n; size *= 2 {
		// Pick starting index of left sub array
		for left := 0; left < n-1; left += 2 * size {
			// Find ending point of left subarray
			// The starting point of right subarray is mid + 1
			mid := min(left+size-1, n-1)
			right := min(left+2*size-1, n-1)

			// Merge subarrays arr[left...mid] and arr[mid+1...right]
			merge(result, left, mid, right)
		}
	}

	return result
}

// MergeSortInPlace sorts the slice in-place
//
// Time Complexity: O(n log n)
// Space Complexity: O(n) - still needs temporary arrays for merging
func MergeSortInPlace[T Ordered](arr []T) {
	if len(arr) <= 1 {
		return
	}
	mergeSortHelper(arr, 0, len(arr)-1)
}

// MergeSortStable ensures stable sorting (preserves relative order of equal elements)
//
// Standard merge sort is already stable, but this explicitly documents it.
//
// Time Complexity: O(n log n)
// Space Complexity: O(n)
func MergeSortStable[T Ordered](arr []T) []T {
	return MergeSort(arr)
}

// MergeSortWithChannel demonstrates using channels for concurrent merge sort
//
// This is an educational implementation showing Go's channel-based
// concurrency model applied to merge sort.
//
// Time Complexity: O(n log n)
// Space Complexity: O(n)
func MergeSortWithChannel[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)

	const threshold = 500
	sortWithChannel(result, threshold)
	return result
}

// sortWithChannel sorts array using channel-based communication
func sortWithChannel[T Ordered](arr []T, threshold int) {
	if len(arr) <= 1 {
		return
	}

	if len(arr) < threshold {
		mergeSortHelper(arr, 0, len(arr)-1)
		return
	}

	mid := len(arr) / 2
	left := make([]T, mid)
	right := make([]T, len(arr)-mid)
	copy(left, arr[:mid])
	copy(right, arr[mid:])

	// Create channels for results
	leftDone := make(chan bool)
	rightDone := make(chan bool)

	// Sort both halves concurrently
	go func() {
		sortWithChannel(left, threshold)
		leftDone <- true
	}()

	go func() {
		sortWithChannel(right, threshold)
		rightDone <- true
	}()

	// Wait for both goroutines to complete
	<-leftDone
	<-rightDone

	// Merge results
	i, j, k := 0, 0, 0
	for i < len(left) && j < len(right) {
		if left[i] <= right[j] {
			arr[k] = left[i]
			i++
		} else {
			arr[k] = right[j]
			j++
		}
		k++
	}

	for i < len(left) {
		arr[k] = left[i]
		i++
		k++
	}

	for j < len(right) {
		arr[k] = right[j]
		j++
		k++
	}
}

// CompareFunc is a function type for custom comparisons
type CompareFunc[T any] func(a, b T) bool

// MergeSortWithComparator sorts using a custom comparison function
//
// The compare function should return true if a <= b
func MergeSortWithComparator[T any](arr []T, compare CompareFunc[T]) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	mergeSortComparatorHelper(result, 0, len(result)-1, compare)
	return result
}

func mergeSortComparatorHelper[T any](arr []T, left, right int, compare CompareFunc[T]) {
	if left >= right {
		return
	}

	mid := left + (right-left)/2
	mergeSortComparatorHelper(arr, left, mid, compare)
	mergeSortComparatorHelper(arr, mid+1, right, compare)
	mergeWithComparator(arr, left, mid, right, compare)
}

func mergeWithComparator[T any](arr []T, left, mid, right int, compare CompareFunc[T]) {
	leftSize := mid - left + 1
	rightSize := right - mid

	leftArr := make([]T, leftSize)
	rightArr := make([]T, rightSize)

	copy(leftArr, arr[left:mid+1])
	copy(rightArr, arr[mid+1:right+1])

	i, j, k := 0, 0, left

	for i < leftSize && j < rightSize {
		if compare(leftArr[i], rightArr[j]) {
			arr[k] = leftArr[i]
			i++
		} else {
			arr[k] = rightArr[j]
			j++
		}
		k++
	}

	for i < leftSize {
		arr[k] = leftArr[i]
		i++
		k++
	}

	for j < rightSize {
		arr[k] = rightArr[j]
		j++
		k++
	}
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
	Merges      int
	Recursions  int
	Duration    time.Duration
}

// Reset resets all statistics to zero
func (s *SortStatistics) Reset() {
	s.Comparisons = 0
	s.Merges = 0
	s.Recursions = 0
	s.Duration = 0
}

// String returns a string representation of the statistics
func (s *SortStatistics) String() string {
	return fmt.Sprintf("Comparisons: %d, Merges: %d, Recursions: %d, Duration: %v",
		s.Comparisons, s.Merges, s.Recursions, s.Duration)
}

// MergeSorter is a class-like structure with state
type MergeSorter[T Ordered] struct {
	stats     SortStatistics
	parallel  bool
	threshold int
}

// NewMergeSorter creates a new MergeSorter instance
func NewMergeSorter[T Ordered](parallel bool, threshold int) *MergeSorter[T] {
	return &MergeSorter[T]{
		parallel:  parallel,
		threshold: threshold,
	}
}

// Sort sorts the array using configured settings
func (ms *MergeSorter[T]) Sort(arr []T) []T {
	ms.stats.Reset()
	start := time.Now()

	var result []T
	if ms.parallel {
		result = MergeSortParallel(arr)
	} else {
		result = MergeSort(arr)
	}

	ms.stats.Duration = time.Since(start)
	return result
}

// GetStats returns the current statistics
func (ms *MergeSorter[T]) GetStats() SortStatistics {
	return ms.stats
}

// Helper function to print a slice
func printSlice[T any](arr []T, label string) {
	fmt.Printf("%s: %v\n", label, arr)
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

// DemonstrateMergeSort demonstrates various merge sort implementations
func DemonstrateMergeSort() {
	fmt.Println("🔀 Merge Sort Implementation in Go")
	fmt.Println(strings.Repeat("=", 70))

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
	fmt.Println(strings.Repeat("-", 70))

	for _, tc := range testCases {
		// Make a copy to preserve original
		original := make([]int, len(tc.arr))
		copy(original, tc.arr)

		// Test different implementations
		recursiveResult := MergeSort(tc.arr)
		iterativeResult := MergeSortIterative(tc.arr)
		parallelResult := MergeSortParallel(tc.arr)
		channelResult := MergeSortWithChannel(tc.arr)

		// Test in-place
		inplaceResult := make([]int, len(tc.arr))
		copy(inplaceResult, tc.arr)
		MergeSortInPlace(inplaceResult)

		fmt.Printf("\nTest: %s\n", tc.desc)
		printSlice(original, "Original")
		printSlice(recursiveResult, "Sorted  ")

		// Verify all results are correct and equal
		allCorrect := IsSorted(recursiveResult) && IsSorted(iterativeResult) &&
			IsSorted(parallelResult) && IsSorted(channelResult) &&
			IsSorted(inplaceResult)

		allEqual := slicesEqual(recursiveResult, iterativeResult) &&
			slicesEqual(recursiveResult, parallelResult) &&
			slicesEqual(recursiveResult, channelResult) &&
			slicesEqual(recursiveResult, inplaceResult)

		status := "✓"
		if !allCorrect || !allEqual {
			status = "✗"
		}
		fmt.Printf("All implementations match: %s\n", status)
	}

	fmt.Println("\n" + strings.Repeat("-", 70))

	// String sorting
	words := []string{"banana", "apple", "cherry", "date", "elderberry"}
	sortedWords := MergeSort(words)

	fmt.Println("\n🔤 Word sorting:")
	printSlice(words, "Original    ")
	printSlice(sortedWords, "Alphabetical")

	// Custom comparison (descending)
	numbers := []int{3, 1, 4, 1, 5, 9, 2, 6}
	descSorted := MergeSortWithComparator(numbers, func(a, b int) bool {
		return a >= b // Reverse comparison for descending order
	})

	fmt.Println("\n🔢 Custom comparison (descending):")
	printSlice(numbers, "Original  ")
	printSlice(descSorted, "Descending")

	// Demonstrate stability
	fmt.Println("\n🎯 Stability Test:")
	type Person struct {
		Name string
		Age  int
	}

	people := []Person{
		{"Alice", 30},
		{"Bob", 25},
		{"Charlie", 30},
		{"David", 25},
	}

	sortedByAge := MergeSortWithComparator(people, func(a, b Person) bool {
		return a.Age <= b.Age
	})

	fmt.Println("Original order:")
	for _, p := range people {
		fmt.Printf("  %s: %d\n", p.Name, p.Age)
	}

	fmt.Println("Sorted by age (stable):")
	for _, p := range sortedByAge {
		fmt.Printf("  %s: %d\n", p.Name, p.Age)
	}
}

// PerformanceBenchmark benchmarks different merge sort implementations
func PerformanceBenchmark() {
	fmt.Println("\n\n⚡ Performance Benchmark")
	fmt.Println(strings.Repeat("=", 90))

	sizes := []int{1000, 5000, 10000, 50000}

	// Test different data patterns
	type PatternFunc func(int) []int

	patterns := map[string]PatternFunc{
		"Random": func(n int) []int {
			rand.Seed(42)
			arr := make([]int, n)
			for i := range arr {
				arr[i] = rand.Intn(10000) + 1
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

	type MethodFunc func([]int) []int

	methods := map[string]MethodFunc{
		"Recursive": MergeSort[int],
		"Iterative": MergeSortIterative[int],
		"Parallel":  MergeSortParallel[int],
		"Channel":   MergeSortWithChannel[int],
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
		methodNames := []string{"Recursive", "Iterative", "Parallel", "Channel", "sort.Ints"}
		for _, name := range methodNames {
			fmt.Printf("%12s", name)
		}
		fmt.Println()
		fmt.Println(strings.Repeat("-", 8+12*len(methodNames)))

		for _, size := range sizes {
			testData := patternGen(size)
			fmt.Printf("%-8d", size)

			for _, methodName := range methodNames {
				methodFunc := methods[methodName]

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

// CompareConcurrency compares sequential vs parallel performance
func CompareConcurrency() {
	fmt.Println("\n\n🚀 Concurrency Performance Analysis")
	fmt.Println(strings.Repeat("=", 70))

	sizes := []int{10000, 50000, 100000, 500000}

	fmt.Printf("%-10s%15s%15s%15s\n", "Size", "Sequential", "Parallel", "Speedup")
	fmt.Println(strings.Repeat("-", 55))

	for _, size := range sizes {
		rand.Seed(42)
		testData := make([]int, size)
		for i := range testData {
			testData[i] = rand.Intn(100000) + 1
		}

		// Sequential
		start := time.Now()
		_ = MergeSort(testData)
		seqTime := time.Since(start)

		// Parallel
		start = time.Now()
		_ = MergeSortParallel(testData)
		parTime := time.Since(start)

		speedup := float64(seqTime) / float64(parTime)

		fmt.Printf("%-10d%14.2fms%14.2fms%14.2fx\n",
			size,
			float64(seqTime.Microseconds())/1000.0,
			float64(parTime.Microseconds())/1000.0,
			speedup)
	}

	fmt.Println("\nNote: Speedup varies based on CPU cores and system load")
}

func main() {
	DemonstrateMergeSort()
	PerformanceBenchmark()
	CompareConcurrency()

	// Demonstrate OOP approach
	fmt.Println("\n\n📊 Object-Oriented Approach")
	fmt.Println(strings.Repeat("=", 70))

	testArray := []int{64, 34, 25, 12, 22, 11, 90, 88, 45, 50, 32, 17, 99}

	// Sequential sorter
	seqSorter := NewMergeSorter[int](false, 1000)
	sortedSeq := seqSorter.Sort(testArray)
	statsSeq := seqSorter.GetStats()

	// Parallel sorter
	parSorter := NewMergeSorter[int](true, 1000)
	sortedPar := parSorter.Sort(testArray)
	statsPar := parSorter.GetStats()

	printSlice(testArray, "Original")
	printSlice(sortedSeq, "Sequential")
	fmt.Printf("  Duration: %v\n", statsSeq.Duration)
	printSlice(sortedPar, "Parallel  ")
	fmt.Printf("  Duration: %v\n", statsPar.Duration)

	fmt.Println("\n✨ Merge Sort demonstration complete!")
}
