package main

import (
	"fmt"
	"math"
	"sort"
	"strings"
	"sync"
	"time"
)

/**
 * Advanced Search Algorithms Implementation in Go
 *
 * This implementation focuses on:
 * - Idiomatic Go patterns (interfaces, goroutines, channels)
 * - Concurrent implementations using goroutines
 * - Efficient memory usage with slices
 * - Generic implementations using interfaces
 *
 * Algorithms Included:
 * 1. Jump Search - O(√n) time, O(1) space
 * 2. Fibonacci Search - O(log n) time, division-free
 * 3. Interpolation Search - O(log log n) average for uniform data
 * 4. Exponential Search - O(log n) for unbounded arrays
 * 5. Parallel/Concurrent Search - Goroutine-based implementations
 * 6. Fuzzy Search - Approximate string matching
 * 7. KD-Tree - Geometric search in k-dimensions
 * 8. Channel-based Search Patterns
 */

// ============================================================================
// INTERFACES AND TYPES
// ============================================================================

// Comparable interface for types that can be compared
type Comparable interface {
	CompareTo(other Comparable) int // Returns: -1 if less, 0 if equal, 1 if greater
}

// Point represents a k-dimensional point
type Point []float64

func (p Point) CompareTo(other Comparable) int {
	otherPoint := other.(Point)
	for i := range p {
		if p[i] < otherPoint[i] {
			return -1
		} else if p[i] > otherPoint[i] {
			return 1
		}
	}
	return 0
}

// ============================================================================
// 1. JUMP SEARCH
// ============================================================================

/**
 * JumpSearch - Block-based search algorithm
 *
 * Time Complexity: O(√n)
 * Space Complexity: O(1)
 *
 * Best for: Sorted arrays where binary search is too complex
 * Advantages:
 * - Better cache performance than binary search for large arrays
 * - Only jumps forward (better for tape/sequential storage)
 * - Simpler implementation than binary search
 */
func JumpSearch(arr []int, target int) int {
	n := len(arr)
	if n == 0 {
		return -1
	}

	// Optimal jump size is √n
	jump := int(math.Sqrt(float64(n)))
	prev := 0

	// Find the block where element may be present
	for prev < n && arr[min(jump, n)-1] < target {
		prev = jump
		jump += int(math.Sqrt(float64(n)))

		if prev >= n {
			return -1
		}
	}

	// Linear search within the block
	for i := prev; i < min(jump, n); i++ {
		if arr[i] == target {
			return i
		}
		if arr[i] > target {
			return -1
		}
	}

	return -1
}

// JumpSearchGeneric - Generic version using comparison function
func JumpSearchGeneric[T any](arr []T, target T, less func(T, T) bool, equal func(T, T) bool) int {
	n := len(arr)
	if n == 0 {
		return -1
	}

	jump := int(math.Sqrt(float64(n)))
	prev := 0

	for prev < n && less(arr[min(jump, n)-1], target) {
		prev = jump
		jump += int(math.Sqrt(float64(n)))

		if prev >= n {
			return -1
		}
	}

	for i := prev; i < min(jump, n); i++ {
		if equal(arr[i], target) {
			return i
		}
		if !less(arr[i], target) && !equal(arr[i], target) {
			return -1
		}
	}

	return -1
}

// ============================================================================
// 2. FIBONACCI SEARCH
// ============================================================================

/**
 * FibonacciSearch - Division-free search algorithm
 *
 * Time Complexity: O(log n)
 * Space Complexity: O(1)
 *
 * Best for: Systems where division is expensive
 * Advantages:
 * - No division operations (uses addition/subtraction only)
 * - Good cache performance with sequential access
 */
func FibonacciSearch(arr []int, target int) int {
	n := len(arr)
	if n == 0 {
		return -1
	}

	// Initialize Fibonacci numbers
	fibM2 := 0 // (m-2)'th Fibonacci number
	fibM1 := 1 // (m-1)'th Fibonacci number
	fibM := fibM2 + fibM1

	// Find the smallest Fibonacci number >= n
	for fibM < n {
		fibM2 = fibM1
		fibM1 = fibM
		fibM = fibM2 + fibM1
	}

	// Marks the eliminated range from front
	offset := -1

	// While there are elements to be inspected
	for fibM > 1 {
		// Check if fibM2 is a valid index
		i := min(offset+fibM2, n-1)

		if arr[i] < target {
			fibM = fibM1
			fibM1 = fibM2
			fibM2 = fibM - fibM1
			offset = i
		} else if arr[i] > target {
			fibM = fibM2
			fibM1 = fibM1 - fibM2
			fibM2 = fibM - fibM1
		} else {
			return i
		}
	}

	// Check the last element
	if fibM1 == 1 && offset+1 < n && arr[offset+1] == target {
		return offset + 1
	}

	return -1
}

// ============================================================================
// 3. INTERPOLATION SEARCH
// ============================================================================

/**
 * InterpolationSearch - Improved binary search for uniformly distributed data
 *
 * Time Complexity:
 * - Average: O(log log n) for uniformly distributed data
 * - Worst: O(n) for non-uniform data
 * Space Complexity: O(1)
 *
 * Best for: Uniformly distributed sorted data
 */
func InterpolationSearch(arr []int, target int) int {
	n := len(arr)
	if n == 0 {
		return -1
	}

	low := 0
	high := n - 1

	for low <= high && target >= arr[low] && target <= arr[high] {
		if low == high {
			if arr[low] == target {
				return low
			}
			return -1
		}

		// Estimate position using interpolation formula
		pos := low + int(float64(target-arr[low])/float64(arr[high]-arr[low])*float64(high-low))

		// Ensure pos is within bounds
		if pos < low {
			pos = low
		}
		if pos > high {
			pos = high
		}

		if arr[pos] == target {
			return pos
		}

		if arr[pos] < target {
			low = pos + 1
		} else {
			high = pos - 1
		}
	}

	return -1
}

// ============================================================================
// 4. EXPONENTIAL SEARCH
// ============================================================================

/**
 * ExponentialSearch - Combination of unbounded search and binary search
 *
 * Time Complexity: O(log n)
 * Space Complexity: O(1)
 *
 * Best for: Unbounded/infinite arrays, or when target is close to beginning
 */
func ExponentialSearch(arr []int, target int) int {
	n := len(arr)
	if n == 0 {
		return -1
	}

	if arr[0] == target {
		return 0
	}

	// Find range for binary search by repeated doubling
	i := 1
	for i < n && arr[i] <= target {
		i *= 2
	}

	// Perform binary search in found range
	left := i / 2
	right := min(i, n-1)

	for left <= right {
		mid := left + (right-left)/2

		if arr[mid] == target {
			return mid
		}

		if arr[mid] < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}

	return -1
}

// ============================================================================
// 5. PARALLEL/CONCURRENT SEARCH ALGORITHMS
// ============================================================================

/**
 * ParallelLinearSearch - Multi-goroutine search
 *
 * Time Complexity: O(n/g) where g is number of goroutines
 * Space Complexity: O(g)
 *
 * Best for: Unsorted large arrays on multi-core systems
 */
func ParallelLinearSearch(arr []int, target int, numWorkers int) int {
	n := len(arr)
	if n == 0 {
		return -1
	}

	// For small arrays, use sequential search
	if n < 1000 {
		for i, v := range arr {
			if v == target {
				return i
			}
		}
		return -1
	}

	// If numWorkers not specified, use number of CPUs
	if numWorkers <= 0 {
		numWorkers = 4 // Default
	}

	// Channel to receive results
	resultChan := make(chan int, numWorkers)
	var wg sync.WaitGroup

	// Divide work among goroutines
	chunkSize := (n + numWorkers - 1) / numWorkers

	for i := 0; i < numWorkers; i++ {
		start := i * chunkSize
		end := min(start+chunkSize, n)

		if start >= n {
			break
		}

		wg.Add(1)
		go func(start, end int) {
			defer wg.Done()
			for j := start; j < end; j++ {
				if arr[j] == target {
					resultChan <- j
					return
				}
			}
		}(start, end)
	}

	// Close channel when all goroutines finish
	go func() {
		wg.Wait()
		close(resultChan)
	}()

	// Get the first result (lowest index)
	minIndex := -1
	for idx := range resultChan {
		if minIndex == -1 || idx < minIndex {
			minIndex = idx
		}
	}

	return minIndex
}

/**
 * ConcurrentBinarySearch - Parallel binary search using goroutines
 *
 * Note: This is primarily educational. Sequential binary search is usually
 * faster due to O(log n) complexity and low overhead.
 */
func ConcurrentBinarySearch(arr []int, target int, depth int) int {
	n := len(arr)
	if n == 0 {
		return -1
	}

	// Base case: use sequential for small ranges or deep recursion
	if n < 10000 || depth > 3 {
		left, right := 0, n-1
		for left <= right {
			mid := left + (right-left)/2
			if arr[mid] == target {
				return mid
			}
			if arr[mid] < target {
				left = mid + 1
			} else {
				right = mid - 1
			}
		}
		return -1
	}

	mid := n / 2

	if arr[mid] == target {
		return mid
	}

	if arr[mid] < target {
		// Search right half
		result := ConcurrentBinarySearch(arr[mid+1:], target, depth+1)
		if result != -1 {
			return mid + 1 + result
		}
	} else {
		// Search left half
		return ConcurrentBinarySearch(arr[:mid], target, depth+1)
	}

	return -1
}

/**
 * ChannelBasedSearch - Uses channels for streaming search results
 *
 * Useful pattern for searching while results are being processed
 */
func ChannelBasedSearch(arr []int, target int) <-chan int {
	resultChan := make(chan int)

	go func() {
		defer close(resultChan)
		for i, v := range arr {
			if v == target {
				resultChan <- i
			}
		}
	}()

	return resultChan
}

// ============================================================================
// 6. FUZZY SEARCH - APPROXIMATE STRING MATCHING
// ============================================================================

/**
 * LevenshteinDistance - Edit distance between two strings
 *
 * Time Complexity: O(m * n)
 * Space Complexity: O(min(m, n))
 */
func LevenshteinDistance(s1, s2 string) int {
	m, n := len(s1), len(s2)

	// Optimize space by using only two rows
	prev := make([]int, n+1)
	curr := make([]int, n+1)

	// Initialize first row
	for j := 0; j <= n; j++ {
		prev[j] = j
	}

	// Fill the matrix row by row
	for i := 1; i <= m; i++ {
		curr[0] = i

		for j := 1; j <= n; j++ {
			if s1[i-1] == s2[j-1] {
				curr[j] = prev[j-1]
			} else {
				curr[j] = 1 + min3(
					prev[j],    // deletion
					curr[j-1],  // insertion
					prev[j-1],  // substitution
				)
			}
		}

		prev, curr = curr, prev
	}

	return prev[n]
}

/**
 * FuzzyStringSearch - Find all strings within edit distance threshold
 */
type FuzzyMatch struct {
	Index    int
	Distance int
	Value    string
}

func FuzzyStringSearch(arr []string, pattern string, maxDistance int) []FuzzyMatch {
	results := make([]FuzzyMatch, 0)

	for i, str := range arr {
		dist := LevenshteinDistance(str, pattern)
		if dist <= maxDistance {
			results = append(results, FuzzyMatch{
				Index:    i,
				Distance: dist,
				Value:    str,
			})
		}
	}

	// Sort by distance (closest matches first)
	sort.Slice(results, func(i, j int) bool {
		return results[i].Distance < results[j].Distance
	})

	return results
}

/**
 * HammingDistance - Distance for fixed-length strings
 */
func HammingDistance(s1, s2 string) int {
	if len(s1) != len(s2) {
		return -1
	}

	distance := 0
	for i := 0; i < len(s1); i++ {
		if s1[i] != s2[i] {
			distance++
		}
	}

	return distance
}

/**
 * ParallelFuzzySearch - Concurrent fuzzy string search
 */
func ParallelFuzzySearch(arr []string, pattern string, maxDistance int, numWorkers int) []FuzzyMatch {
	n := len(arr)
	if n == 0 {
		return nil
	}

	if numWorkers <= 0 {
		numWorkers = 4
	}

	resultChan := make(chan []FuzzyMatch, numWorkers)
	var wg sync.WaitGroup

	chunkSize := (n + numWorkers - 1) / numWorkers

	for i := 0; i < numWorkers; i++ {
		start := i * chunkSize
		end := min(start+chunkSize, n)

		if start >= n {
			break
		}

		wg.Add(1)
		go func(start, end int) {
			defer wg.Done()
			localResults := make([]FuzzyMatch, 0)

			for j := start; j < end; j++ {
				dist := LevenshteinDistance(arr[j], pattern)
				if dist <= maxDistance {
					localResults = append(localResults, FuzzyMatch{
						Index:    j,
						Distance: dist,
						Value:    arr[j],
					})
				}
			}

			resultChan <- localResults
		}(start, end)
	}

	go func() {
		wg.Wait()
		close(resultChan)
	}()

	// Combine results
	allResults := make([]FuzzyMatch, 0)
	for localResults := range resultChan {
		allResults = append(allResults, localResults...)
	}

	// Sort by distance
	sort.Slice(allResults, func(i, j int) bool {
		return allResults[i].Distance < allResults[j].Distance
	})

	return allResults
}

// ============================================================================
// 7. KD-TREE - GEOMETRIC SEARCH
// ============================================================================

/**
 * KDTree - k-dimensional tree for geometric search
 *
 * Time Complexity:
 * - Construction: O(n log n)
 * - Search: O(log n) average, O(n) worst case
 * - Nearest Neighbor: O(log n) average
 */
type KDNode struct {
	Point Point
	Left  *KDNode
	Right *KDNode
	Axis  int
}

type KDTree struct {
	Root *KDNode
	K    int
}

func NewKDTree(k int) *KDTree {
	return &KDTree{K: k}
}

func (t *KDTree) Build(points []Point) {
	if len(points) == 0 {
		return
	}
	t.Root = t.buildTree(points, 0)
}

func (t *KDTree) buildTree(points []Point, depth int) *KDNode {
	if len(points) == 0 {
		return nil
	}

	axis := depth % t.K
	mid := len(points) / 2

	// Sort by current axis
	sort.Slice(points, func(i, j int) bool {
		return points[i][axis] < points[j][axis]
	})

	node := &KDNode{
		Point: points[mid],
		Axis:  axis,
	}

	node.Left = t.buildTree(points[:mid], depth+1)
	node.Right = t.buildTree(points[mid+1:], depth+1)

	return node
}

func (t *KDTree) distanceSquared(a, b Point) float64 {
	dist := 0.0
	for i := 0; i < t.K; i++ {
		diff := a[i] - b[i]
		dist += diff * diff
	}
	return dist
}

func (t *KDTree) NearestNeighbor(query Point) (Point, float64) {
	if t.Root == nil {
		return nil, -1
	}

	bestPoint := t.Root.Point
	bestDist := t.distanceSquared(query, t.Root.Point)

	t.nearestNeighborSearch(t.Root, query, &bestPoint, &bestDist)

	return bestPoint, math.Sqrt(bestDist)
}

func (t *KDTree) nearestNeighborSearch(node *KDNode, query Point, bestPoint *Point, bestDist *float64) {
	if node == nil {
		return
	}

	// Calculate distance to current point
	dist := t.distanceSquared(node.Point, query)
	if dist < *bestDist {
		*bestDist = dist
		*bestPoint = node.Point
	}

	// Determine which side to search first
	axis := node.Axis
	diff := query[axis] - node.Point[axis]

	var first, second *KDNode
	if diff < 0 {
		first = node.Left
		second = node.Right
	} else {
		first = node.Right
		second = node.Left
	}

	// Search near side first
	t.nearestNeighborSearch(first, query, bestPoint, bestDist)

	// Check if we need to search the other side
	if diff*diff < *bestDist {
		t.nearestNeighborSearch(second, query, bestPoint, bestDist)
	}
}

func (t *KDTree) RangeQuery(lower, upper Point) []Point {
	results := make([]Point, 0)
	t.rangeSearch(t.Root, lower, upper, &results)
	return results
}

func (t *KDTree) rangeSearch(node *KDNode, lower, upper Point, results *[]Point) {
	if node == nil {
		return
	}

	// Check if current point is in range
	inRange := true
	for i := 0; i < t.K; i++ {
		if node.Point[i] < lower[i] || node.Point[i] > upper[i] {
			inRange = false
			break
		}
	}

	if inRange {
		*results = append(*results, node.Point)
	}

	// Check which subtrees to search
	axis := node.Axis

	if lower[axis] <= node.Point[axis] {
		t.rangeSearch(node.Left, lower, upper, results)
	}
	if upper[axis] >= node.Point[axis] {
		t.rangeSearch(node.Right, lower, upper, results)
	}
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

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
// PERFORMANCE ANALYSIS
// ============================================================================

func measureTime(name string, fn func()) {
	start := time.Now()
	fn()
	elapsed := time.Since(start)
	fmt.Printf("%-25s: %v\n", name, elapsed)
}

func compareAlgorithms() {
	fmt.Println("\n=== Algorithm Performance Comparison ===\n")

	sizes := []int{1000, 10000, 100000, 1000000}

	for _, size := range sizes {
		arr := make([]int, size)
		for i := 0; i < size; i++ {
			arr[i] = i + 1
		}

		target := size * 3 / 4

		fmt.Printf("Array size: %d\n", size)
		fmt.Printf("Target position: ~75%%\n\n")

		measureTime("Jump Search", func() {
			JumpSearch(arr, target)
		})

		measureTime("Fibonacci Search", func() {
			FibonacciSearch(arr, target)
		})

		measureTime("Interpolation Search", func() {
			InterpolationSearch(arr, target)
		})

		measureTime("Exponential Search", func() {
			ExponentialSearch(arr, target)
		})

		fmt.Println()
	}
}

// ============================================================================
// MAIN - EXAMPLES AND TESTS
// ============================================================================

func main() {
	fmt.Println("Advanced Search Algorithms in Go - Concurrent Implementation")
	fmt.Println("=============================================================")

	// Example 1: Jump Search
	fmt.Println("\n1. JUMP SEARCH EXAMPLE")
	fmt.Println("----------------------")
	arr1 := []int{1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25}
	target1 := 15
	result1 := JumpSearch(arr1, target1)
	fmt.Printf("Array: %v\n", arr1)
	fmt.Printf("Search for: %d\n", target1)
	if result1 != -1 {
		fmt.Printf("Result: Found at index %d\n", result1)
	} else {
		fmt.Println("Result: Not found")
	}
	fmt.Printf("Optimal jump size: √%d ≈ %d\n", len(arr1), int(math.Sqrt(float64(len(arr1)))))

	// Example 2: Fibonacci Search
	fmt.Println("\n2. FIBONACCI SEARCH EXAMPLE")
	fmt.Println("---------------------------")
	arr2 := []int{10, 22, 35, 40, 45, 50, 80, 82, 85, 90, 100}
	target2 := 85
	result2 := FibonacciSearch(arr2, target2)
	fmt.Printf("Array: %v\n", arr2)
	fmt.Printf("Search for: %d\n", target2)
	if result2 != -1 {
		fmt.Printf("Result: Found at index %d\n", result2)
	} else {
		fmt.Println("Result: Not found")
	}
	fmt.Println("Division-free algorithm - uses only addition/subtraction")

	// Example 3: Interpolation Search
	fmt.Println("\n3. INTERPOLATION SEARCH EXAMPLE")
	fmt.Println("-------------------------------")
	arr3 := []int{10, 20, 30, 40, 50, 60, 70, 80, 90, 100}
	target3 := 70
	result3 := InterpolationSearch(arr3, target3)
	fmt.Printf("Array (uniform): %v\n", arr3)
	fmt.Printf("Search for: %d\n", target3)
	if result3 != -1 {
		fmt.Printf("Result: Found at index %d\n", result3)
	} else {
		fmt.Println("Result: Not found")
	}
	fmt.Println("Best for uniformly distributed data: O(log log n) average")

	// Example 4: Exponential Search
	fmt.Println("\n4. EXPONENTIAL SEARCH EXAMPLE")
	fmt.Println("-----------------------------")
	arr4 := []int{2, 3, 4, 10, 40, 50, 80, 100, 120, 150, 200}
	target4 := 10
	result4 := ExponentialSearch(arr4, target4)
	fmt.Printf("Array: %v\n", arr4)
	fmt.Printf("Search for: %d (near beginning)\n", target4)
	if result4 != -1 {
		fmt.Printf("Result: Found at index %d\n", result4)
	} else {
		fmt.Println("Result: Not found")
	}
	fmt.Println("Excellent for unbounded arrays and early elements")

	// Example 5: Parallel Search
	fmt.Println("\n5. PARALLEL SEARCH EXAMPLE")
	fmt.Println("--------------------------")
	arr5 := make([]int, 100000)
	for i := range arr5 {
		arr5[i] = i + 1
	}
	target5 := 75000

	start := time.Now()
	result5 := ParallelLinearSearch(arr5, target5, 4)
	elapsed := time.Since(start)

	fmt.Printf("Array size: %d elements\n", len(arr5))
	fmt.Println("Goroutines: 4")
	fmt.Printf("Search for: %d\n", target5)
	if result5 != -1 {
		fmt.Printf("Result: Found at index %d\n", result5)
	} else {
		fmt.Println("Result: Not found")
	}
	fmt.Printf("Time: %v\n", elapsed)

	// Example 6: Fuzzy Search
	fmt.Println("\n6. FUZZY STRING SEARCH EXAMPLE")
	fmt.Println("------------------------------")
	words := []string{"apple", "application", "apply", "banana", "band", "can"}
	pattern := "app"
	maxDist := 2
	fuzzyResults := FuzzyStringSearch(words, pattern, maxDist)

	fmt.Printf("Dictionary: %v\n", words)
	fmt.Printf("Pattern: \"%s\"\n", pattern)
	fmt.Printf("Max edit distance: %d\n", maxDist)
	fmt.Println("Results:")
	for _, match := range fuzzyResults {
		fmt.Printf("  \"%s\" (distance: %d)\n", match.Value, match.Distance)
	}

	// Example 7: Parallel Fuzzy Search
	fmt.Println("\n7. PARALLEL FUZZY SEARCH EXAMPLE")
	fmt.Println("--------------------------------")
	manyWords := make([]string, 10000)
	for i := range manyWords {
		manyWords[i] = fmt.Sprintf("word%d", i)
	}
	manyWords[500] = "apple"
	manyWords[1500] = "apply"
	manyWords[5000] = "application"

	start = time.Now()
	parallelResults := ParallelFuzzySearch(manyWords, "app", 3, 4)
	elapsed = time.Since(start)

	fmt.Printf("Dictionary size: %d words\n", len(manyWords))
	fmt.Printf("Pattern: \"app\"\n")
	fmt.Printf("Max distance: 3\n")
	fmt.Printf("Goroutines: 4\n")
	fmt.Printf("Found %d matches in %v\n", len(parallelResults), elapsed)
	fmt.Println("Top matches:")
	for i := 0; i < min(3, len(parallelResults)); i++ {
		fmt.Printf("  \"%s\" at index %d (distance: %d)\n",
			parallelResults[i].Value, parallelResults[i].Index, parallelResults[i].Distance)
	}

	// Example 8: KD-Tree Search
	fmt.Println("\n8. KD-TREE GEOMETRIC SEARCH EXAMPLE")
	fmt.Println("-----------------------------------")
	kdtree := NewKDTree(2)
	points := []Point{
		{2.0, 3.0}, {5.0, 4.0}, {9.0, 6.0}, {4.0, 7.0}, {8.0, 1.0}, {7.0, 2.0},
	}
	kdtree.Build(points)

	fmt.Print("Points: ")
	for _, p := range points {
		fmt.Printf("(%.0f,%.0f) ", p[0], p[1])
	}
	fmt.Println()

	query := Point{5.0, 5.0}
	nearest, dist := kdtree.NearestNeighbor(query)
	fmt.Printf("Query point: (%.0f, %.0f)\n", query[0], query[1])
	if nearest != nil {
		fmt.Printf("Nearest neighbor: (%.0f, %.0f)\n", nearest[0], nearest[1])
		fmt.Printf("Distance: %.2f\n", dist)
	}

	// Range query
	lower := Point{3.0, 2.0}
	upper := Point{8.0, 6.0}
	rangeResults := kdtree.RangeQuery(lower, upper)
	fmt.Printf("\nRange query: [(%.0f,%.0f) to (%.0f,%.0f)]\n",
		lower[0], lower[1], upper[0], upper[1])
	fmt.Print("Points in range: ")
	for _, p := range rangeResults {
		fmt.Printf("(%.0f,%.0f) ", p[0], p[1])
	}
	fmt.Println()

	// Example 9: Channel-Based Search
	fmt.Println("\n9. CHANNEL-BASED SEARCH PATTERN")
	fmt.Println("--------------------------------")
	arr9 := []int{1, 5, 3, 7, 5, 2, 5, 9, 5}
	target9 := 5
	fmt.Printf("Array: %v\n", arr9)
	fmt.Printf("Search for all occurrences of: %d\n", target9)

	resultChan := ChannelBasedSearch(arr9, target9)
	fmt.Print("Found at indices: ")
	indices := make([]int, 0)
	for idx := range resultChan {
		indices = append(indices, idx)
	}
	fmt.Println(indices)
	fmt.Println("Useful for streaming results as they're found")

	// Algorithm Selection Guide
	fmt.Println("\n10. ALGORITHM SELECTION GUIDE")
	fmt.Println("=============================\n")

	guide := []struct {
		name        string
		when        []string
		complexity  string
		concurrency bool
	}{
		{
			name: "JUMP SEARCH",
			when: []string{
				"Binary search is too complex for hardware",
				"Sequential access is faster (linked lists)",
				"Cache performance matters more than theory",
			},
			complexity:  "O(√n) time, O(1) space",
			concurrency: false,
		},
		{
			name: "FIBONACCI SEARCH",
			when: []string{
				"Division operations are expensive",
				"Working with embedded systems",
				"Data is not uniformly distributed",
			},
			complexity:  "O(log n) time, O(1) space, no division",
			concurrency: false,
		},
		{
			name: "INTERPOLATION SEARCH",
			when: []string{
				"Data is uniformly distributed",
				"Array elements are numerical",
				"Phone books, dictionaries, numerical datasets",
			},
			complexity:  "O(log log n) average, O(n) worst",
			concurrency: false,
		},
		{
			name: "EXPONENTIAL SEARCH",
			when: []string{
				"Array size is unknown (unbounded)",
				"Target is likely near the beginning",
				"Working with streams or infinite sequences",
			},
			complexity:  "O(log n), very fast for early elements",
			concurrency: false,
		},
		{
			name: "PARALLEL SEARCH",
			when: []string{
				"Array is very large (> 100k elements)",
				"Multiple cores available",
				"Array is unsorted",
				"Can leverage goroutines effectively",
			},
			complexity:  "O(n/g) where g = goroutines",
			concurrency: true,
		},
		{
			name: "FUZZY SEARCH",
			when: []string{
				"Exact matches are not required",
				"Dealing with user input (typos)",
				"Spell checkers, autocomplete, suggestions",
			},
			complexity:  "O(n*m*k) where k is string length",
			concurrency: true,
		},
		{
			name: "KD-TREE",
			when: []string{
				"Searching in multidimensional space",
				"Need nearest neighbor queries",
				"Need range queries in multiple dimensions",
				"GIS, computer graphics, machine learning",
			},
			complexity:  "O(log n) average for search",
			concurrency: false,
		},
	}

	for _, item := range guide {
		fmt.Printf("%s:\n", item.name)
		fmt.Println("  When to use:")
		for _, w := range item.when {
			fmt.Printf("    - %s\n", w)
		}
		fmt.Printf("  Complexity: %s\n", item.complexity)
		if item.concurrency {
			fmt.Println("  Concurrency: Supports parallel/concurrent implementation")
		}
		fmt.Println()
	}

	// Go-specific patterns
	fmt.Println("=== Go-Specific Concurrency Patterns ===\n")
	fmt.Println("1. GOROUTINES FOR PARALLEL SEARCH:")
	fmt.Println("   - Lightweight threads for concurrent operations")
	fmt.Println("   - Ideal for dividing search space")
	fmt.Println("   - Use WaitGroups for synchronization")
	fmt.Println()

	fmt.Println("2. CHANNELS FOR STREAMING RESULTS:")
	fmt.Println("   - Stream results as they're found")
	fmt.Println("   - Non-blocking result processing")
	fmt.Println("   - Fan-out/fan-in patterns for aggregation")
	fmt.Println()

	fmt.Println("3. SELECT FOR TIMEOUT/CANCELLATION:")
	fmt.Println("   - Implement search timeouts")
	fmt.Println("   - Cancel long-running searches")
	fmt.Println("   - Handle multiple result channels")
	fmt.Println()

	fmt.Println("4. CONTEXT FOR PROPAGATION:")
	fmt.Println("   - Propagate cancellation across goroutines")
	fmt.Println("   - Set deadlines for search operations")
	fmt.Println("   - Pass request-scoped values")

	// Performance comparison
	compareAlgorithms()

	fmt.Println("\n=== Concurrency Best Practices ===\n")
	fmt.Println("1. Use goroutines for large datasets (> 10k elements)")
	fmt.Println("2. Partition data for good cache locality")
	fmt.Println("3. Avoid goroutine overhead for small tasks")
	fmt.Println("4. Use buffered channels to prevent blocking")
	fmt.Println("5. Always use WaitGroups or contexts for coordination")
	fmt.Println("6. Consider memory overhead of parallel operations")

	fmt.Println("\n" + strings.Repeat("=", 65))
	fmt.Println("Implementation complete with idiomatic Go patterns!")
	fmt.Println(strings.Repeat("=", 65))
}
