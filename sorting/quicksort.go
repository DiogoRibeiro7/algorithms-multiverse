// Quick Sort Algorithm Implementation in Go
//
// Time Complexity:
// - Best Case: O(n log n) - balanced partitions
// - Average Case: O(n log n)
// - Worst Case: O(n²) - poor pivot selection
// Space Complexity: O(log n) for recursion stack, O(1) auxiliary space
//
// Quick Sort is a divide-and-conquer algorithm that picks a pivot element
// and partitions the array around it, recursively sorting the subarrays.
// It's one of the fastest sorting algorithms in practice.
//
// Go features:
// - Generic functions using type parameters
// - Multiple pivot selection strategies (first, last, median, random)
// - Parallel quicksort with goroutines for large datasets
// - Three-way partitioning for arrays with many duplicates
// - Tail call optimization
// - Hybrid approach with insertion sort for small subarrays

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

// PivotStrategy defines the pivot selection strategy
type PivotStrategy int

const (
	PivotFirst PivotStrategy = iota
	PivotLast
	PivotMiddle
	PivotRandom
	PivotMedianOfThree
)

// QuickSort performs standard quicksort with last element as pivot
//
// Time Complexity: O(n log n) average, O(n²) worst case
// Space Complexity: O(log n) for recursion
func QuickSort[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	quickSortHelper(result, 0, len(result)-1, PivotLast)
	return result
}

// quickSortHelper is the recursive helper for quicksort
func quickSortHelper[T Ordered](arr []T, low, high int, strategy PivotStrategy) {
	if low < high {
		pivotIdx := partition(arr, low, high, strategy)
		quickSortHelper(arr, low, pivotIdx-1, strategy)
		quickSortHelper(arr, pivotIdx+1, high, strategy)
	}
}

// partition partitions the array and returns the pivot index
func partition[T Ordered](arr []T, low, high int, strategy PivotStrategy) int {
	// Choose pivot based on strategy
	pivotIdx := choosePivot(arr, low, high, strategy)

	// Move pivot to end
	arr[pivotIdx], arr[high] = arr[high], arr[pivotIdx]
	pivot := arr[high]

	// Partition around pivot
	i := low - 1

	for j := low; j < high; j++ {
		if arr[j] <= pivot {
			i++
			arr[i], arr[j] = arr[j], arr[i]
		}
	}

	// Place pivot in correct position
	arr[i+1], arr[high] = arr[high], arr[i+1]
	return i + 1
}

// choosePivot selects pivot index based on strategy
func choosePivot[T Ordered](arr []T, low, high int, strategy PivotStrategy) int {
	switch strategy {
	case PivotFirst:
		return low
	case PivotLast:
		return high
	case PivotMiddle:
		return low + (high-low)/2
	case PivotRandom:
		return low + rand.Intn(high-low+1)
	case PivotMedianOfThree:
		return medianOfThree(arr, low, high)
	default:
		return high
	}
}

// medianOfThree returns the index of the median of first, middle, and last elements
func medianOfThree[T Ordered](arr []T, low, high int) int {
	mid := low + (high-low)/2

	// Sort the three elements
	if arr[low] > arr[mid] {
		if arr[mid] > arr[high] {
			return mid
		} else if arr[low] > arr[high] {
			return high
		}
		return low
	}

	if arr[low] > arr[high] {
		return low
	} else if arr[mid] > arr[high] {
		return high
	}
	return mid
}

// QuickSortMedian performs quicksort with median-of-three pivot
//
// Better performance than simple pivot selection by avoiding worst case more often
func QuickSortMedian[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	quickSortHelper(result, 0, len(result)-1, PivotMedianOfThree)
	return result
}

// QuickSortRandom performs quicksort with randomized pivot selection
//
// Randomized pivot helps avoid worst-case performance on sorted/reverse-sorted inputs
func QuickSortRandom[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	rand.Seed(time.Now().UnixNano())
	quickSortHelper(result, 0, len(result)-1, PivotRandom)
	return result
}

// QuickSort3Way performs three-way partitioning quicksort
//
// Excellent for arrays with many duplicate values.
// Partitions into: [< pivot | = pivot | > pivot]
//
// Time Complexity: O(n log n), much better for duplicates
func QuickSort3Way[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	quickSort3WayHelper(result, 0, len(result)-1)
	return result
}

// quickSort3WayHelper implements three-way partitioning
func quickSort3WayHelper[T Ordered](arr []T, low, high int) {
	if low >= high {
		return
	}

	// Three-way partition
	lt, gt := low, high
	pivot := arr[low]
	i := low + 1

	for i <= gt {
		if arr[i] < pivot {
			arr[lt], arr[i] = arr[i], arr[lt]
			lt++
			i++
		} else if arr[i] > pivot {
			arr[i], arr[gt] = arr[gt], arr[i]
			gt--
		} else {
			i++
		}
	}

	// Recursively sort partitions
	quickSort3WayHelper(arr, low, lt-1)
	quickSort3WayHelper(arr, gt+1, high)
}

// QuickSortHybrid uses quicksort for large subarrays and insertion sort for small ones
//
// Hybrid approach combines speed of quicksort with efficiency of insertion sort
// on small arrays
//
// Time Complexity: O(n log n) average
func QuickSortHybrid[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	quickSortHybridHelper(result, 0, len(result)-1)
	return result
}

// Threshold for switching to insertion sort
const hybridThreshold = 10

func quickSortHybridHelper[T Ordered](arr []T, low, high int) {
	// Use insertion sort for small subarrays
	if high-low+1 <= hybridThreshold {
		insertionSort(arr, low, high)
		return
	}

	if low < high {
		pivotIdx := partition(arr, low, high, PivotMedianOfThree)
		quickSortHybridHelper(arr, low, pivotIdx-1)
		quickSortHybridHelper(arr, pivotIdx+1, high)
	}
}

// insertionSort sorts arr[low..high] using insertion sort
func insertionSort[T Ordered](arr []T, low, high int) {
	for i := low + 1; i <= high; i++ {
		key := arr[i]
		j := i - 1

		for j >= low && arr[j] > key {
			arr[j+1] = arr[j]
			j--
		}
		arr[j+1] = key
	}
}

// QuickSortParallel performs parallel quicksort using goroutines
//
// Uses goroutines to sort partitions concurrently when array size
// exceeds the threshold. Significantly improves performance on multi-core systems.
//
// Time Complexity: O(n log n) average
// Concurrency: Utilizes multiple CPU cores
func QuickSortParallel[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)

	const threshold = 10000
	quickSortParallelHelper(result, 0, len(result)-1, threshold)
	return result
}

func quickSortParallelHelper[T Ordered](arr []T, low, high, threshold int) {
	// Use sequential sort for small arrays
	if high-low+1 < threshold {
		quickSortHelper(arr, low, high, PivotMedianOfThree)
		return
	}

	if low < high {
		pivotIdx := partition(arr, low, high, PivotMedianOfThree)

		// Sort partitions in parallel
		var wg sync.WaitGroup
		wg.Add(2)

		go func() {
			defer wg.Done()
			quickSortParallelHelper(arr, low, pivotIdx-1, threshold)
		}()

		go func() {
			defer wg.Done()
			quickSortParallelHelper(arr, pivotIdx+1, high, threshold)
		}()

		wg.Wait()
	}
}

// QuickSortInPlace sorts the slice in-place
//
// Time Complexity: O(n log n) average
// Space Complexity: O(log n) for recursion
func QuickSortInPlace[T Ordered](arr []T) {
	if len(arr) <= 1 {
		return
	}
	quickSortHelper(arr, 0, len(arr)-1, PivotMedianOfThree)
}

// QuickSortTailOptimized uses tail call optimization to reduce stack depth
//
// Optimizes to always recurse on the smaller partition first
//
// Time Complexity: O(n log n) average
// Space Complexity: O(log n) worst case stack depth
func QuickSortTailOptimized[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	quickSortTailHelper(result, 0, len(result)-1)
	return result
}

func quickSortTailHelper[T Ordered](arr []T, low, high int) {
	for low < high {
		pivotIdx := partition(arr, low, high, PivotMedianOfThree)

		// Recurse on smaller partition, iterate on larger
		if pivotIdx-low < high-pivotIdx {
			quickSortTailHelper(arr, low, pivotIdx-1)
			low = pivotIdx + 1
		} else {
			quickSortTailHelper(arr, pivotIdx+1, high)
			high = pivotIdx - 1
		}
	}
}

// CompareFunc is a function type for custom comparisons
type CompareFunc[T any] func(a, b T) bool

// QuickSortWithComparator sorts using a custom comparison function
func QuickSortWithComparator[T any](arr []T, compare CompareFunc[T]) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	quickSortComparatorHelper(result, 0, len(result)-1, compare)
	return result
}

func quickSortComparatorHelper[T any](arr []T, low, high int, compare CompareFunc[T]) {
	if low < high {
		pivotIdx := partitionComparator(arr, low, high, compare)
		quickSortComparatorHelper(arr, low, pivotIdx-1, compare)
		quickSortComparatorHelper(arr, pivotIdx+1, high, compare)
	}
}

func partitionComparator[T any](arr []T, low, high int, compare CompareFunc[T]) int {
	pivot := arr[high]
	i := low - 1

	for j := low; j < high; j++ {
		if compare(arr[j], pivot) {
			i++
			arr[i], arr[j] = arr[j], arr[i]
		}
	}

	arr[i+1], arr[high] = arr[high], arr[i+1]
	return i + 1
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

// DemonstrateQuickSort demonstrates various quicksort implementations
func DemonstrateQuickSort() {
	fmt.Println("⚡ Quick Sort Implementation in Go")
	fmt.Println(strings.Repeat("=", 70))

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
		{[]int{5, 1, 4, 2, 3}, "Nearly sorted"},
		{[]int{3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5}, "Many duplicates"},
	}

	fmt.Println("\n📋 Basic Sorting Tests:")
	fmt.Println(strings.Repeat("-", 70))

	for _, tc := range testCases {
		original := make([]int, len(tc.arr))
		copy(original, tc.arr)

		// Test different implementations
		basicResult := QuickSort(tc.arr)
		medianResult := QuickSortMedian(tc.arr)
		threeWayResult := QuickSort3Way(tc.arr)
		hybridResult := QuickSortHybrid(tc.arr)
		tailResult := QuickSortTailOptimized(tc.arr)

		// Test in-place
		inplaceResult := make([]int, len(tc.arr))
		copy(inplaceResult, tc.arr)
		QuickSortInPlace(inplaceResult)

		fmt.Printf("\nTest: %s\n", tc.desc)
		printSlice(original, "Original")
		printSlice(basicResult, "Sorted  ")

		// Verify all results
		allCorrect := IsSorted(basicResult) && IsSorted(medianResult) &&
			IsSorted(threeWayResult) && IsSorted(hybridResult) &&
			IsSorted(tailResult) && IsSorted(inplaceResult)

		allEqual := slicesEqual(basicResult, medianResult) &&
			slicesEqual(basicResult, threeWayResult) &&
			slicesEqual(basicResult, hybridResult) &&
			slicesEqual(basicResult, tailResult) &&
			slicesEqual(basicResult, inplaceResult)

		status := "✓"
		if !allCorrect || !allEqual {
			status = "✗"
		}
		fmt.Printf("All implementations match: %s\n", status)
	}

	// String sorting
	fmt.Println("\n🔤 Word sorting:")
	words := []string{"banana", "apple", "cherry", "date", "elderberry"}
	sortedWords := QuickSort(words)
	printSlice(words, "Original    ")
	printSlice(sortedWords, "Alphabetical")

	// Custom comparison
	fmt.Println("\n🔢 Custom comparison (descending):")
	numbers := []int{3, 1, 4, 1, 5, 9, 2, 6}
	descSorted := QuickSortWithComparator(numbers, func(a, b int) bool {
		return a >= b
	})
	printSlice(numbers, "Original  ")
	printSlice(descSorted, "Descending")
}

// PerformanceBenchmark benchmarks different quicksort implementations
func PerformanceBenchmark() {
	fmt.Println("\n\n⚡ Performance Benchmark")
	fmt.Println(strings.Repeat("=", 100))

	sizes := []int{1000, 5000, 10000, 50000}

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
		"Duplicates": func(n int) []int {
			rand.Seed(42)
			arr := make([]int, n)
			for i := range arr {
				arr[i] = rand.Intn(10) + 1 // Only 10 unique values
			}
			return arr
		},
	}

	type MethodFunc func([]int) []int

	methods := map[string]MethodFunc{
		"Basic":      QuickSort[int],
		"Median":     QuickSortMedian[int],
		"3-Way":      QuickSort3Way[int],
		"Hybrid":     QuickSortHybrid[int],
		"Tail":       QuickSortTailOptimized[int],
		"Parallel":   QuickSortParallel[int],
		"sort.Ints":  func(arr []int) []int {
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
		methodNames := []string{"Basic", "Median", "3-Way", "Hybrid", "Tail", "Parallel", "sort.Ints"}
		for _, name := range methodNames {
			fmt.Printf("%11s", name)
		}
		fmt.Println()
		fmt.Println(strings.Repeat("-", 8+11*len(methodNames)))

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
				fmt.Printf("%10.2fms", elapsedMs)

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
		_ = QuickSort(testData)
		seqTime := time.Since(start)

		// Parallel
		start = time.Now()
		_ = QuickSortParallel(testData)
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

// AnalyzePivotStrategies analyzes different pivot selection strategies
func AnalyzePivotStrategies() {
	fmt.Println("\n\n🎯 Pivot Strategy Analysis")
	fmt.Println(strings.Repeat("=", 70))

	size := 10000
	rand.Seed(42)

	patterns := map[string][]int{
		"Random":     make([]int, size),
		"Sorted":     make([]int, size),
		"Reversed":   make([]int, size),
	}

	for i := 0; i < size; i++ {
		patterns["Random"][i] = rand.Intn(10000)
		patterns["Sorted"][i] = i
		patterns["Reversed"][i] = size - i
	}

	strategies := []PivotStrategy{
		PivotFirst,
		PivotLast,
		PivotMiddle,
		PivotMedianOfThree,
	}

	strategyNames := []string{"First", "Last", "Middle", "Median-3"}

	fmt.Printf("%-12s", "Pattern")
	for _, name := range strategyNames {
		fmt.Printf("%12s", name)
	}
	fmt.Println()
	fmt.Println(strings.Repeat("-", 12+12*len(strategyNames)))

	for patternName, data := range patterns {
		fmt.Printf("%-12s", patternName)

		for _, strategy := range strategies {
			testData := make([]int, len(data))
			copy(testData, data)

			start := time.Now()
			quickSortHelper(testData, 0, len(testData)-1, strategy)
			elapsed := time.Since(start)

			fmt.Printf("%11.2fms", float64(elapsed.Microseconds())/1000.0)
		}

		fmt.Println()
	}
}

func main() {
	DemonstrateQuickSort()
	PerformanceBenchmark()
	CompareConcurrency()
	AnalyzePivotStrategies()

	fmt.Println("\n✨ Quick Sort demonstration complete!")
}
