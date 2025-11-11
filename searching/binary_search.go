/**
 * Binary Search Algorithm Collection in Go
 *
 * Comprehensive implementation of binary search variants including:
 * 1. Classic binary search (iterative & recursive)
 * 2. First/last occurrence finding
 * 3. Rotated array search
 * 4. Exponential search
 * 5. Interpolation search
 * 6. Ternary search
 * 7. Binary search on answer (optimization)
 * 8. Advanced utilities
 *
 * Time Complexity: O(log n) for most variants
 * Space Complexity: O(1) iterative, O(log n) recursive
 *
 * Go Features:
 * - Generic implementations using interfaces
 * - First-class functions
 * - Slices and efficient memory management
 * - Comprehensive error handling
 */

package main

import (
	"fmt"
	"math"
	"math/rand"
	"time"
)

// ==============================================================================
// TYPE DEFINITIONS AND INTERFACES
// ==============================================================================

// Comparable interface for elements that can be compared
type Comparable[T any] interface {
	Compare(other T) int
}

// Predicate is a function that tests a condition
type Predicate func(int) bool

// UnaryFunction is a function taking one argument
type UnaryFunction func(float64) float64

// ==============================================================================
// 1. CLASSIC BINARY SEARCH
// ==============================================================================

// BinarySearchIterative performs classic binary search iteratively
//
// Time Complexity: O(log n)
// Space Complexity: O(1)
func BinarySearchIterative(arr []int, target int) int {
	if len(arr) == 0 {
		return -1
	}

	left, right := 0, len(arr)-1

	for left <= right {
		mid := left + (right-left)/2 // Avoid overflow

		if arr[mid] == target {
			return mid
		} else if arr[mid] < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}

	return -1
}

// BinarySearchRecursive performs classic binary search recursively
//
// Time Complexity: O(log n)
// Space Complexity: O(log n) - recursion stack
func BinarySearchRecursive(arr []int, target int) int {
	if len(arr) == 0 {
		return -1
	}
	return binarySearchRecursiveHelper(arr, target, 0, len(arr)-1)
}

func binarySearchRecursiveHelper(arr []int, target, left, right int) int {
	if left > right {
		return -1
	}

	mid := left + (right-left)/2

	if arr[mid] == target {
		return mid
	} else if arr[mid] < target {
		return binarySearchRecursiveHelper(arr, target, mid+1, right)
	} else {
		return binarySearchRecursiveHelper(arr, target, left, mid-1)
	}
}

// BinarySearchFloat64 performs binary search on float64 slices
func BinarySearchFloat64(arr []float64, target float64) int {
	if len(arr) == 0 {
		return -1
	}

	left, right := 0, len(arr)-1

	for left <= right {
		mid := left + (right-left)/2

		if math.Abs(arr[mid]-target) < 1e-9 {
			return mid
		} else if arr[mid] < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}

	return -1
}

// ==============================================================================
// 2. FIRST/LAST OCCURRENCE
// ==============================================================================

// FindFirstOccurrence finds the first (leftmost) occurrence of target
func FindFirstOccurrence(arr []int, target int) int {
	if len(arr) == 0 {
		return -1
	}

	left, right := 0, len(arr)-1
	result := -1

	for left <= right {
		mid := left + (right-left)/2

		if arr[mid] == target {
			result = mid
			right = mid - 1 // Continue searching left
		} else if arr[mid] < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}

	return result
}

// FindLastOccurrence finds the last (rightmost) occurrence of target
func FindLastOccurrence(arr []int, target int) int {
	if len(arr) == 0 {
		return -1
	}

	left, right := 0, len(arr)-1
	result := -1

	for left <= right {
		mid := left + (right-left)/2

		if arr[mid] == target {
			result = mid
			left = mid + 1 // Continue searching right
		} else if arr[mid] < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}

	return result
}

// CountOccurrences counts total occurrences of target
func CountOccurrences(arr []int, target int) int {
	first := FindFirstOccurrence(arr, target)
	if first == -1 {
		return 0
	}

	last := FindLastOccurrence(arr, target)
	return last - first + 1
}

// SearchRange finds the range [start, end] of target
func SearchRange(arr []int, target int) [2]int {
	first := FindFirstOccurrence(arr, target)
	if first == -1 {
		return [2]int{-1, -1}
	}

	last := FindLastOccurrence(arr, target)
	return [2]int{first, last}
}

// ==============================================================================
// 3. ROTATED SORTED ARRAY SEARCH
// ==============================================================================

// SearchRotatedArray searches in a rotated sorted array
func SearchRotatedArray(arr []int, target int) int {
	if len(arr) == 0 {
		return -1
	}

	left, right := 0, len(arr)-1

	for left <= right {
		mid := left + (right-left)/2

		if arr[mid] == target {
			return mid
		}

		// Determine which half is sorted
		if arr[left] <= arr[mid] {
			// Left half is sorted
			if arr[left] <= target && target < arr[mid] {
				right = mid - 1
			} else {
				left = mid + 1
			}
		} else {
			// Right half is sorted
			if arr[mid] < target && target <= arr[right] {
				left = mid + 1
			} else {
				right = mid - 1
			}
		}
	}

	return -1
}

// FindRotationPoint finds the rotation point (minimum element)
func FindRotationPoint(arr []int) int {
	if len(arr) == 0 {
		return -1
	}

	left, right := 0, len(arr)-1

	for left < right {
		mid := left + (right-left)/2

		if arr[mid] > arr[right] {
			left = mid + 1
		} else {
			right = mid
		}
	}

	return left
}

// ==============================================================================
// 4. EXPONENTIAL SEARCH
// ==============================================================================

// ExponentialSearch performs exponential search
func ExponentialSearch(arr []int, target int) int {
	if len(arr) == 0 {
		return -1
	}

	if arr[0] == target {
		return 0
	}

	// Find range for binary search
	i := 1
	for i < len(arr) && arr[i] <= target {
		i *= 2
	}

	// Binary search in found range
	left := i / 2
	right := i
	if right >= len(arr) {
		right = len(arr) - 1
	}

	return binarySearchRecursiveHelper(arr, target, left, right)
}

// ==============================================================================
// 5. INTERPOLATION SEARCH
// ==============================================================================

// InterpolationSearch performs interpolation search
//
// Time Complexity: O(log log n) average, O(n) worst
func InterpolationSearch(arr []int, target int) int {
	if len(arr) == 0 {
		return -1
	}

	left, right := 0, len(arr)-1

	for left <= right && target >= arr[left] && target <= arr[right] {
		if left == right {
			if arr[left] == target {
				return left
			}
			return -1
		}

		// Interpolation formula
		pos := left + ((target-arr[left])*(right-left))/(arr[right]-arr[left])

		// Ensure pos is within bounds
		if pos < left {
			pos = left
		}
		if pos > right {
			pos = right
		}

		if arr[pos] == target {
			return pos
		} else if arr[pos] < target {
			left = pos + 1
		} else {
			right = pos - 1
		}
	}

	return -1
}

// ==============================================================================
// 6. TERNARY SEARCH
// ==============================================================================

// TernarySearch performs ternary search
func TernarySearch(arr []int, target int) int {
	if len(arr) == 0 {
		return -1
	}

	left, right := 0, len(arr)-1

	for left <= right {
		mid1 := left + (right-left)/3
		mid2 := right - (right-left)/3

		if arr[mid1] == target {
			return mid1
		}
		if arr[mid2] == target {
			return mid2
		}

		if target < arr[mid1] {
			right = mid1 - 1
		} else if target > arr[mid2] {
			left = mid2 + 1
		} else {
			left = mid1 + 1
			right = mid2 - 1
		}
	}

	return -1
}

// TernarySearchMaximum finds maximum of unimodal function
func TernarySearchMaximum(fn UnaryFunction, left, right, epsilon float64) float64 {
	for right-left > epsilon {
		mid1 := left + (right-left)/3.0
		mid2 := right - (right-left)/3.0

		if fn(mid1) < fn(mid2) {
			left = mid1
		} else {
			right = mid2
		}
	}

	return (left + right) / 2.0
}

// ==============================================================================
// 7. BINARY SEARCH ON ANSWER
// ==============================================================================

// BinarySearchOnAnswer performs binary search on answer space
func BinarySearchOnAnswer(predicate Predicate, low, high int) int {
	result := -1

	for low <= high {
		mid := low + (high-low)/2

		if predicate(mid) {
			result = mid
			high = mid - 1 // Try to find smaller answer
		} else {
			low = mid + 1
		}
	}

	return result
}

// IntegerSquareRoot finds integer square root using binary search
func IntegerSquareRoot(n int) int {
	if n < 0 {
		return -1
	}

	if n == 0 || n == 1 {
		return n
	}

	left, right := 0, n
	result := 0

	for left <= right {
		mid := left + (right-left)/2
		square := mid * mid

		if square == n {
			return mid
		} else if square < n {
			result = mid
			left = mid + 1
		} else {
			right = mid - 1
		}
	}

	return result
}

// SquareRoot finds square root with decimal precision
func SquareRoot(n float64, precision int) float64 {
	if n < 0 {
		return -1
	}

	if n == 0.0 || n == 1.0 {
		return n
	}

	left, right := 0.0, n
	epsilon := math.Pow(10, float64(-precision))

	for right-left > epsilon {
		mid := left + (right-left)/2.0
		square := mid * mid

		if math.Abs(square-n) < epsilon {
			return mid
		} else if square < n {
			left = mid
		} else {
			right = mid
		}
	}

	return (left + right) / 2.0
}

// ==============================================================================
// 8. ADVANCED UTILITIES
// ==============================================================================

// SearchInsertPosition finds insertion position to maintain sorted order
func SearchInsertPosition(arr []int, target int) int {
	if len(arr) == 0 {
		return 0
	}

	left, right := 0, len(arr)

	for left < right {
		mid := left + (right-left)/2

		if arr[mid] < target {
			left = mid + 1
		} else {
			right = mid
		}
	}

	return left
}

// FindClosest finds element closest to target
func FindClosest(arr []int, target int) int {
	if len(arr) == 0 {
		return -1
	}

	if len(arr) == 1 {
		return 0
	}

	if target <= arr[0] {
		return 0
	}
	if target >= arr[len(arr)-1] {
		return len(arr) - 1
	}

	left, right := 0, len(arr)-1

	for left < right {
		mid := left + (right-left)/2

		if arr[mid] == target {
			return mid
		} else if arr[mid] < target {
			left = mid + 1
		} else {
			right = mid
		}
	}

	if left > 0 && abs(arr[left-1]-target) < abs(arr[left]-target) {
		return left - 1
	}

	return left
}

// FindPeakElement finds a peak element
func FindPeakElement(arr []int) int {
	if len(arr) == 0 {
		return -1
	}

	if len(arr) == 1 {
		return 0
	}

	left, right := 0, len(arr)-1

	for left < right {
		mid := left + (right-left)/2

		if arr[mid] < arr[mid+1] {
			left = mid + 1
		} else {
			right = mid
		}
	}

	return left
}

// ==============================================================================
// UTILITY FUNCTIONS
// ==============================================================================

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

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

// ==============================================================================
// DEMONSTRATION AND TESTING
// ==============================================================================

func main() {
	fmt.Println("======================================================================")
	fmt.Println("BINARY SEARCH ALGORITHM COLLECTION - GO")
	fmt.Println("======================================================================")

	demonstrateClassicBinarySearch()
	demonstrateFirstLastOccurrence()
	demonstrateRotatedArraySearch()
	demonstrateExponentialSearch()
	demonstrateInterpolationSearch()
	demonstrateTernarySearch()
	demonstrateBinarySearchOnAnswer()
	demonstrateAdvancedUtilities()
	runPerformanceTests()

	fmt.Println("\n======================================================================")
	fmt.Println("DEMONSTRATION COMPLETE")
	fmt.Println("======================================================================")
}

func demonstrateClassicBinarySearch() {
	fmt.Println("\n1. CLASSIC BINARY SEARCH")
	fmt.Println("--------------------------------------------------")

	arr := []int{1, 3, 5, 7, 9, 11, 13, 15, 17, 19}
	targets := []int{7, 10, 1, 19}

	for _, target := range targets {
		idxIter := BinarySearchIterative(arr, target)
		idxRec := BinarySearchRecursive(arr, target)
		fmt.Printf("Search %2d: Iterative=%2d, Recursive=%2d\n",
			target, idxIter, idxRec)
	}
}

func demonstrateFirstLastOccurrence() {
	fmt.Println("\n2. FIRST/LAST OCCURRENCE")
	fmt.Println("--------------------------------------------------")

	arr := []int{1, 2, 2, 2, 3, 4, 4, 4, 4, 5}
	targets := []int{2, 4, 6}

	for _, target := range targets {
		first := FindFirstOccurrence(arr, target)
		last := FindLastOccurrence(arr, target)
		count := CountOccurrences(arr, target)
		fmt.Printf("Target %d: First=%2d, Last=%2d, Count=%d\n",
			target, first, last, count)
	}
}

func demonstrateRotatedArraySearch() {
	fmt.Println("\n3. ROTATED ARRAY SEARCH")
	fmt.Println("--------------------------------------------------")

	rotated := []int{4, 5, 6, 7, 0, 1, 2}
	rotationPoint := FindRotationPoint(rotated)

	fmt.Printf("Rotated array: %v\n", rotated)
	fmt.Printf("Rotation point: %d (value: %d)\n",
		rotationPoint, rotated[rotationPoint])

	targets := []int{0, 3, 6}
	for _, target := range targets {
		idx := SearchRotatedArray(rotated, target)
		fmt.Printf("Search %d: Index=%d\n", target, idx)
	}
}

func demonstrateExponentialSearch() {
	fmt.Println("\n4. EXPONENTIAL SEARCH")
	fmt.Println("--------------------------------------------------")

	largeArr := make([]int, 50)
	for i := 0; i < 50; i++ {
		largeArr[i] = i*2 + 1
	}

	targets := []int{15, 51, 99}
	for _, target := range targets {
		idx := ExponentialSearch(largeArr, target)
		fmt.Printf("Search %2d in array of size 50: Index=%d\n", target, idx)
	}
}

func demonstrateInterpolationSearch() {
	fmt.Println("\n5. INTERPOLATION SEARCH")
	fmt.Println("--------------------------------------------------")

	uniformArr := []int{10, 20, 30, 40, 50, 60, 70, 80, 90, 100}
	targets := []int{30, 75, 100}

	for _, target := range targets {
		idx := InterpolationSearch(uniformArr, target)
		fmt.Printf("Search %3d: Index=%d\n", target, idx)
	}
}

func demonstrateTernarySearch() {
	fmt.Println("\n6. TERNARY SEARCH")
	fmt.Println("--------------------------------------------------")

	arr := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	targets := []int{5, 1, 10, 11}

	for _, target := range targets {
		idx := TernarySearch(arr, target)
		fmt.Printf("Search %2d: Index=%d\n", target, idx)
	}

	// Unimodal function
	fn := func(x float64) float64 {
		return -(x-5)*(x-5) + 25
	}
	maxX := TernarySearchMaximum(fn, 0, 10, 1e-9)
	fmt.Printf("Maximum of -(x-5)² + 25 at x ≈ %.6f\n", maxX)
}

func demonstrateBinarySearchOnAnswer() {
	fmt.Println("\n7. BINARY SEARCH ON ANSWER")
	fmt.Println("--------------------------------------------------")

	testNumbers := []int{16, 25, 50, 100}
	for _, n := range testNumbers {
		sqrtInt := IntegerSquareRoot(n)
		sqrtPrecise := SquareRoot(float64(n), 2)
		fmt.Printf("√%3d = %d (integer), %.2f (precise)\n",
			n, sqrtInt, sqrtPrecise)
	}
}

func demonstrateAdvancedUtilities() {
	fmt.Println("\n8. ADVANCED UTILITIES")
	fmt.Println("--------------------------------------------------")

	arr := []int{1, 3, 5, 6, 8, 10}
	targets := []int{2, 5, 11}

	for _, target := range targets {
		pos := SearchInsertPosition(arr, target)
		fmt.Printf("Insert position for %2d: %d\n", target, pos)
	}

	arrClosest := []int{1, 3, 5, 7, 9}
	targetsClosest := []int{4, 6, 8}

	for _, target := range targetsClosest {
		idx := FindClosest(arrClosest, target)
		fmt.Printf("Closest to %d: Index=%d, Value=%d\n",
			target, idx, arrClosest[idx])
	}

	peakArr := []int{1, 3, 20, 4, 1, 0}
	peak := FindPeakElement(peakArr)
	fmt.Printf("Peak element in %v: Index=%d, Value=%d\n",
		peakArr, peak, peakArr[peak])
}

func runPerformanceTests() {
	fmt.Println("\n======================================================================")
	fmt.Println("PERFORMANCE BENCHMARKS")
	fmt.Println("======================================================================")

	sizes := []int{1000, 10000, 100000}
	rand.Seed(42)

	for _, size := range sizes {
		fmt.Printf("\nArray size: %d\n", size)
		fmt.Println("--------------------------------------------------")

		// Generate sorted array
		arr := make([]int, size)
		for i := 0; i < size; i++ {
			arr[i] = i * 2
		}

		targets := make([]int, 100)
		for i := 0; i < 100; i++ {
			targets[i] = rand.Intn(size) * 2
		}

		// Binary Search (Iterative)
		start := time.Now()
		for _, target := range targets {
			BinarySearchIterative(arr, target)
		}
		timeBinaryIter := time.Since(start).Milliseconds()

		// Binary Search (Recursive)
		start = time.Now()
		for _, target := range targets {
			BinarySearchRecursive(arr, target)
		}
		timeBinaryRec := time.Since(start).Milliseconds()

		// Exponential Search
		start = time.Now()
		for _, target := range targets {
			ExponentialSearch(arr, target)
		}
		timeExponential := time.Since(start).Milliseconds()

		// Interpolation Search
		start = time.Now()
		for _, target := range targets {
			InterpolationSearch(arr, target)
		}
		timeInterpolation := time.Since(start).Milliseconds()

		// Ternary Search
		start = time.Now()
		for _, target := range targets {
			TernarySearch(arr, target)
		}
		timeTernary := time.Since(start).Milliseconds()

		fmt.Printf("Binary (Iterative):    %8d ms\n", timeBinaryIter)
		fmt.Printf("Binary (Recursive):    %8d ms\n", timeBinaryRec)
		fmt.Printf("Exponential Search:    %8d ms\n", timeExponential)
		fmt.Printf("Interpolation Search:  %8d ms\n", timeInterpolation)
		fmt.Printf("Ternary Search:        %8d ms\n", timeTernary)
	}
}
