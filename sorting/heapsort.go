// Heap Sort Algorithm Implementation in Go
//
// Time Complexity: O(n log n) - consistently across all cases
// Space Complexity: O(1) for in-place sorting, O(n) for auxiliary heap
//
// Heap Sort is a comparison-based sorting algorithm that uses a binary heap data
// structure. It divides its input into a sorted and an unsorted region, and it
// iteratively shrinks the unsorted region by extracting the largest element and
// inserting it into the sorted region.
//
// Go features:
// - Generic functions using type parameters
// - Heap data structure implementation
// - Priority queue
// - Error handling
// - Visual representation

package main

import (
	"errors"
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

// HeapifyMax maintains the max-heap property for a subtree rooted at index i
//
// Time Complexity: O(log n)
func HeapifyMax[T Ordered](arr []T, n, i int) {
	largest := i
	left := 2*i + 1
	right := 2*i + 2

	// Check if left child exists and is greater than root
	if left < n && arr[left] > arr[largest] {
		largest = left
	}

	// Check if right child exists and is greater than largest so far
	if right < n && arr[right] > arr[largest] {
		largest = right
	}

	// If largest is not root, swap and recursively heapify
	if largest != i {
		arr[i], arr[largest] = arr[largest], arr[i]
		HeapifyMax(arr, n, largest)
	}
}

// HeapifyMin maintains the min-heap property for a subtree rooted at index i
//
// Time Complexity: O(log n)
func HeapifyMin[T Ordered](arr []T, n, i int) {
	smallest := i
	left := 2*i + 1
	right := 2*i + 2

	if left < n && arr[left] < arr[smallest] {
		smallest = left
	}

	if right < n && arr[right] < arr[smallest] {
		smallest = right
	}

	if smallest != i {
		arr[i], arr[smallest] = arr[smallest], arr[i]
		HeapifyMin(arr, n, smallest)
	}
}

// BuildMaxHeap builds a max-heap from an unordered array
//
// Time Complexity: O(n)
func BuildMaxHeap[T Ordered](arr []T) {
	n := len(arr)
	// Start from the last non-leaf node and heapify each node
	for i := n/2 - 1; i >= 0; i-- {
		HeapifyMax(arr, n, i)
	}
}

// BuildMinHeap builds a min-heap from an unordered array
//
// Time Complexity: O(n)
func BuildMinHeap[T Ordered](arr []T) {
	n := len(arr)
	for i := n/2 - 1; i >= 0; i-- {
		HeapifyMin(arr, n, i)
	}
}

// HeapSort sorts a slice using heap sort algorithm
//
// Time Complexity: O(n log n)
func HeapSort[T Ordered](arr []T) []T {
	if len(arr) <= 1 {
		result := make([]T, len(arr))
		copy(result, arr)
		return result
	}

	result := make([]T, len(arr))
	copy(result, arr)
	HeapSortInPlace(result)
	return result
}

// HeapSortInPlace sorts a slice in-place using heap sort
//
// Time Complexity: O(n log n)
// Space Complexity: O(1)
func HeapSortInPlace[T Ordered](arr []T) {
	n := len(arr)

	// Build a max heap
	BuildMaxHeap(arr)

	// Extract elements from heap one by one
	for i := n - 1; i > 0; i-- {
		// Move current root to end
		arr[0], arr[i] = arr[i], arr[0]
		// Call heapify on the reduced heap
		HeapifyMax(arr, i, 0)
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

// MaxHeap is a max-heap data structure implementation
type MaxHeap[T Ordered] struct {
	heap []T
}

// NewMaxHeap creates a new max-heap
func NewMaxHeap[T Ordered](initialData ...T) *MaxHeap[T] {
	h := &MaxHeap[T]{
		heap: make([]T, len(initialData)),
	}
	copy(h.heap, initialData)
	if len(h.heap) > 0 {
		h.buildHeap()
	}
	return h
}

func (h *MaxHeap[T]) parent(i int) int {
	return (i - 1) / 2
}

func (h *MaxHeap[T]) left(i int) int {
	return 2*i + 1
}

func (h *MaxHeap[T]) right(i int) int {
	return 2*i + 2
}

func (h *MaxHeap[T]) buildHeap() {
	for i := len(h.heap)/2 - 1; i >= 0; i-- {
		h.heapifyDown(i)
	}
}

func (h *MaxHeap[T]) bubbleUp(i int) {
	for i > 0 && h.heap[h.parent(i)] < h.heap[i] {
		parentIdx := h.parent(i)
		h.heap[i], h.heap[parentIdx] = h.heap[parentIdx], h.heap[i]
		i = parentIdx
	}
}

func (h *MaxHeap[T]) heapifyDown(i int) {
	largest := i
	left := h.left(i)
	right := h.right(i)

	if left < len(h.heap) && h.heap[left] > h.heap[largest] {
		largest = left
	}

	if right < len(h.heap) && h.heap[right] > h.heap[largest] {
		largest = right
	}

	if largest != i {
		h.heap[i], h.heap[largest] = h.heap[largest], h.heap[i]
		h.heapifyDown(largest)
	}
}

// Insert adds a new key into the heap
//
// Time Complexity: O(log n)
func (h *MaxHeap[T]) Insert(key T) {
	h.heap = append(h.heap, key)
	h.bubbleUp(len(h.heap) - 1)
}

// ExtractMax removes and returns the maximum element from the heap
//
// Time Complexity: O(log n)
func (h *MaxHeap[T]) ExtractMax() (T, error) {
	var zero T
	if len(h.heap) == 0 {
		return zero, errors.New("extractMax from empty heap")
	}

	if len(h.heap) == 1 {
		max := h.heap[0]
		h.heap = h.heap[:0]
		return max, nil
	}

	max := h.heap[0]
	h.heap[0] = h.heap[len(h.heap)-1]
	h.heap = h.heap[:len(h.heap)-1]
	h.heapifyDown(0)

	return max, nil
}

// GetMax returns the maximum element without removing it
func (h *MaxHeap[T]) GetMax() (T, error) {
	var zero T
	if len(h.heap) == 0 {
		return zero, errors.New("getMax from empty heap")
	}
	return h.heap[0], nil
}

// IncreaseKey increases the value of a key at index i
//
// Time Complexity: O(log n)
func (h *MaxHeap[T]) IncreaseKey(i int, newKey T) error {
	if i < 0 || i >= len(h.heap) {
		return fmt.Errorf("index %d out of bounds", i)
	}

	if newKey < h.heap[i] {
		return errors.New("new key is smaller than current key")
	}

	h.heap[i] = newKey
	h.bubbleUp(i)
	return nil
}

// DecreaseKey decreases the value of a key at index i
//
// Time Complexity: O(log n)
func (h *MaxHeap[T]) DecreaseKey(i int, newKey T) error {
	if i < 0 || i >= len(h.heap) {
		return fmt.Errorf("index %d out of bounds", i)
	}

	if newKey > h.heap[i] {
		return errors.New("new key is greater than current key")
	}

	h.heap[i] = newKey
	h.heapifyDown(i)
	return nil
}

// Size returns the size of the heap
func (h *MaxHeap[T]) Size() int {
	return len(h.heap)
}

// IsEmpty checks if the heap is empty
func (h *MaxHeap[T]) IsEmpty() bool {
	return len(h.heap) == 0
}

// ToSlice returns a copy of the heap as a slice
func (h *MaxHeap[T]) ToSlice() []T {
	result := make([]T, len(h.heap))
	copy(result, h.heap)
	return result
}

// Visualize creates ASCII art visualization of the heap
func (h *MaxHeap[T]) Visualize() string {
	if len(h.heap) == 0 {
		return "Empty heap"
	}

	var lines []string
	h.visualizeHelper(0, "", "", &lines)
	return strings.Join(lines, "\n")
}

func (h *MaxHeap[T]) visualizeHelper(i int, prefix, childPrefix string, lines *[]string) {
	if i >= len(h.heap) {
		return
	}

	*lines = append(*lines, fmt.Sprintf("%s%v", prefix, h.heap[i]))

	leftIdx := h.left(i)
	rightIdx := h.right(i)

	if leftIdx < len(h.heap) || rightIdx < len(h.heap) {
		if leftIdx < len(h.heap) {
			if rightIdx < len(h.heap) {
				h.visualizeHelper(leftIdx, childPrefix+"├── ", childPrefix+"│   ", lines)
			} else {
				h.visualizeHelper(leftIdx, childPrefix+"└── ", childPrefix+"    ", lines)
			}
		}

		if rightIdx < len(h.heap) {
			h.visualizeHelper(rightIdx, childPrefix+"└── ", childPrefix+"    ", lines)
		}
	}
}

// MinHeap is a min-heap data structure implementation
type MinHeap[T Ordered] struct {
	heap []T
}

// NewMinHeap creates a new min-heap
func NewMinHeap[T Ordered](initialData ...T) *MinHeap[T] {
	h := &MinHeap[T]{
		heap: make([]T, len(initialData)),
	}
	copy(h.heap, initialData)
	if len(h.heap) > 0 {
		h.buildHeap()
	}
	return h
}

func (h *MinHeap[T]) parent(i int) int {
	return (i - 1) / 2
}

func (h *MinHeap[T]) left(i int) int {
	return 2*i + 1
}

func (h *MinHeap[T]) right(i int) int {
	return 2*i + 2
}

func (h *MinHeap[T]) buildHeap() {
	for i := len(h.heap)/2 - 1; i >= 0; i-- {
		h.heapifyDown(i)
	}
}

func (h *MinHeap[T]) bubbleUp(i int) {
	for i > 0 && h.heap[h.parent(i)] > h.heap[i] {
		parentIdx := h.parent(i)
		h.heap[i], h.heap[parentIdx] = h.heap[parentIdx], h.heap[i]
		i = parentIdx
	}
}

func (h *MinHeap[T]) heapifyDown(i int) {
	smallest := i
	left := h.left(i)
	right := h.right(i)

	if left < len(h.heap) && h.heap[left] < h.heap[smallest] {
		smallest = left
	}

	if right < len(h.heap) && h.heap[right] < h.heap[smallest] {
		smallest = right
	}

	if smallest != i {
		h.heap[i], h.heap[smallest] = h.heap[smallest], h.heap[i]
		h.heapifyDown(smallest)
	}
}

// Insert adds a new key into the min-heap
func (h *MinHeap[T]) Insert(key T) {
	h.heap = append(h.heap, key)
	h.bubbleUp(len(h.heap) - 1)
}

// ExtractMin removes and returns the minimum element
func (h *MinHeap[T]) ExtractMin() (T, error) {
	var zero T
	if len(h.heap) == 0 {
		return zero, errors.New("extractMin from empty heap")
	}

	if len(h.heap) == 1 {
		min := h.heap[0]
		h.heap = h.heap[:0]
		return min, nil
	}

	min := h.heap[0]
	h.heap[0] = h.heap[len(h.heap)-1]
	h.heap = h.heap[:len(h.heap)-1]
	h.heapifyDown(0)

	return min, nil
}

// GetMin returns the minimum element without removing it
func (h *MinHeap[T]) GetMin() (T, error) {
	var zero T
	if len(h.heap) == 0 {
		return zero, errors.New("getMin from empty heap")
	}
	return h.heap[0], nil
}

// Size returns the size of the heap
func (h *MinHeap[T]) Size() int {
	return len(h.heap)
}

// IsEmpty checks if the heap is empty
func (h *MinHeap[T]) IsEmpty() bool {
	return len(h.heap) == 0
}

// Visualize creates ASCII art visualization of the min-heap
func (h *MinHeap[T]) Visualize() string {
	if len(h.heap) == 0 {
		return "Empty heap"
	}

	var lines []string
	h.visualizeHelper(0, "", "", &lines)
	return strings.Join(lines, "\n")
}

func (h *MinHeap[T]) visualizeHelper(i int, prefix, childPrefix string, lines *[]string) {
	if i >= len(h.heap) {
		return
	}

	*lines = append(*lines, fmt.Sprintf("%s%v", prefix, h.heap[i]))

	leftIdx := h.left(i)
	rightIdx := h.right(i)

	if leftIdx < len(h.heap) || rightIdx < len(h.heap) {
		if leftIdx < len(h.heap) {
			if rightIdx < len(h.heap) {
				h.visualizeHelper(leftIdx, childPrefix+"├── ", childPrefix+"│   ", lines)
			} else {
				h.visualizeHelper(leftIdx, childPrefix+"└── ", childPrefix+"    ", lines)
			}
		}

		if rightIdx < len(h.heap) {
			h.visualizeHelper(rightIdx, childPrefix+"└── ", childPrefix+"    ", lines)
		}
	}
}

// PriorityQueue is a priority queue implementation using a max-heap
type PriorityQueue[T Ordered] struct {
	heap *MaxHeap[T]
}

// NewPriorityQueue creates a new priority queue
func NewPriorityQueue[T Ordered]() *PriorityQueue[T] {
	return &PriorityQueue[T]{
		heap: NewMaxHeap[T](),
	}
}

// Enqueue adds an item to the priority queue
func (pq *PriorityQueue[T]) Enqueue(item T) {
	pq.heap.Insert(item)
}

// Dequeue removes and returns the highest priority item
func (pq *PriorityQueue[T]) Dequeue() (T, error) {
	return pq.heap.ExtractMax()
}

// Peek returns the highest priority item without removing it
func (pq *PriorityQueue[T]) Peek() (T, error) {
	return pq.heap.GetMax()
}

// IsEmpty checks if the priority queue is empty
func (pq *PriorityQueue[T]) IsEmpty() bool {
	return pq.heap.IsEmpty()
}

// Size returns the size of the priority queue
func (pq *PriorityQueue[T]) Size() int {
	return pq.heap.Size()
}

// Helper function to print a slice
func printSlice[T any](arr []T, label string) {
	fmt.Printf("%s: %v\n", label, arr)
}

// DemonstrateHeapSort demonstrates heap sort and heap data structure
func DemonstrateHeapSort() {
	fmt.Println("🏔️  Heap Sort Implementation in Go")
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
	}

	fmt.Println("\n📋 Basic Sorting Tests:")
	fmt.Println(strings.Repeat("-", 60))

	for _, tc := range testCases {
		original := make([]int, len(tc.arr))
		copy(original, tc.arr)

		sortedArr := HeapSort(tc.arr)

		fmt.Printf("\nTest: %s\n", tc.desc)
		printSlice(original, "Original")
		printSlice(sortedArr, "Sorted  ")
		fmt.Printf("Correct:  %s\n", map[bool]string{true: "✓", false: "✗"}[IsSorted(sortedArr)])
	}

	fmt.Println("\n" + strings.Repeat("-", 60))

	// Demonstrate heap visualization
	fmt.Println("\n🌲 Heap Visualization:")
	fmt.Println(strings.Repeat("-", 60))

	data := []int{64, 34, 25, 12, 22, 11, 90}
	maxHeap := NewMaxHeap(data...)

	fmt.Println("\nMax-Heap built from:", data)
	fmt.Println(maxHeap.Visualize())

	fmt.Println("\nMin-Heap built from:", data)
	minHeap := NewMinHeap(data...)
	fmt.Println(minHeap.Visualize())

	// Demonstrate heap operations
	fmt.Println("\n🔧 Heap Operations:")
	fmt.Println(strings.Repeat("-", 60))

	heap := NewMaxHeap[int]()
	operations := []int{50, 30, 70, 20, 40, 60, 80}

	fmt.Println("\nInserting elements:", operations)
	for _, val := range operations {
		heap.Insert(val)
		max, _ := heap.GetMax()
		fmt.Printf("Inserted %d, Max: %d\n", val, max)
	}

	fmt.Println("\nHeap structure:")
	fmt.Println(heap.Visualize())

	fmt.Println("\nExtracting elements:")
	var extracted []int
	for !heap.IsEmpty() {
		val, _ := heap.ExtractMax()
		extracted = append(extracted, val)
		fmt.Printf("Extracted: %d\n", val)
	}

	printSlice(extracted, "Extraction order")

	// Demonstrate priority queue
	fmt.Println("\n📬 Priority Queue Demo:")
	fmt.Println(strings.Repeat("-", 60))

	pq := NewPriorityQueue[int]()
	tasks := []int{5, 1, 9, 3, 7}

	fmt.Println("\nEnqueuing tasks with priorities:", tasks)
	for _, priority := range tasks {
		pq.Enqueue(priority)
		top, _ := pq.Peek()
		fmt.Printf("Enqueued priority %d, Top priority: %d\n", priority, top)
	}

	fmt.Println("\nProcessing tasks by priority:")
	for !pq.IsEmpty() {
		priority, _ := pq.Dequeue()
		fmt.Printf("Processing task with priority: %d\n", priority)
	}
}

// PerformanceBenchmark benchmarks heap sort
func PerformanceBenchmark() {
	fmt.Println("\n\n⚡ Performance Benchmark")
	fmt.Println(strings.Repeat("=", 80))

	sizes := []int{100, 500, 1000, 5000, 10000}

	patterns := map[string]func(int) []int{
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
	}

	for patternName, patternGen := range patterns {
		fmt.Printf("\n%s Data:\n", patternName)
		fmt.Printf("%-8s%15s%15s\n", "Size", "Heap Sort", "sort.Ints")
		fmt.Println(strings.Repeat("-", 38))

		for _, size := range sizes {
			testData := patternGen(size)
			fmt.Printf("%-8d", size)

			// Heap Sort
			start := time.Now()
			_ = HeapSort(testData)
			elapsed := time.Since(start)
			fmt.Printf("%14.2fms", float64(elapsed.Microseconds())/1000.0)

			// sort.Ints
			testData2 := make([]int, len(testData))
			copy(testData2, testData)
			start = time.Now()
			sort.Ints(testData2)
			elapsed = time.Since(start)
			fmt.Printf("%14.2fms\n", float64(elapsed.Microseconds())/1000.0)
		}
	}
}

// TestEdgeCases tests edge cases and error handling
func TestEdgeCases() {
	fmt.Println("\n\n🧪 Edge Cases and Error Handling")
	fmt.Println(strings.Repeat("=", 60))

	fmt.Println("\n1. Testing empty heap operations:")
	heap := NewMaxHeap[int]()
	_, err := heap.ExtractMax()
	if err != nil {
		fmt.Printf("   ✓ Correctly returned error: %v\n", err)
	} else {
		fmt.Println("   ✗ Should have returned error")
	}

	fmt.Println("\n2. Testing increaseKey with smaller value:")
	heap2 := NewMaxHeap(10, 20, 30)
	err = heap2.IncreaseKey(0, 5)
	if err != nil {
		fmt.Printf("   ✓ Correctly returned error: %v\n", err)
	} else {
		fmt.Println("   ✗ Should have returned error")
	}

	fmt.Println("\n3. Testing with duplicates:")
	arr := []int{5, 5, 5, 5, 5}
	sorted := HeapSort(arr)
	printSlice(arr, "   Original")
	printSlice(sorted, "   Sorted  ")
	correct := slicesEqual(sorted, arr)
	fmt.Printf("   Correct:  %s\n", map[bool]string{true: "✓", false: "✗"}[correct])
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

func main() {
	DemonstrateHeapSort()
	PerformanceBenchmark()
	TestEdgeCases()

	fmt.Println("\n✨ Heap Sort demonstration complete!")
}
