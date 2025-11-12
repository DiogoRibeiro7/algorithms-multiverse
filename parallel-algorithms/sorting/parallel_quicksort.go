/*
Parallel Quicksort Implementation in Go

This implementation leverages Go's goroutines for efficient parallel sorting with:
- Three-way partitioning for duplicate handling
- Work-stealing strategy via channels
- Depth limiting to prevent goroutine explosion
- Adaptive switching to sequential sort

Features:
- Goroutine-based parallelism
- Channel-based work distribution
- Load balancing
- Performance comparison with sequential version

Time Complexity: O(n log n) average, O(n²) worst case
Space Complexity: O(log n) with in-place partitioning

Author: Algorithms Multiverse
*/

package main

import (
	"fmt"
	"math/rand"
	"runtime"
	"sync"
	"time"
)

// SortResult contains metrics from a sorting operation
type SortResult struct {
	SortedArray   []int
	TimeTaken     time.Duration
	Comparisons   int64
	Swaps         int64
	Method        string
	NumGoroutines int
}

// ParallelQuicksort handles parallel quicksort operations
type ParallelQuicksort struct {
	sequentialThreshold int
	maxParallelDepth    int
	comparisons         int64
	swaps               int64
	mu                  sync.Mutex
}

// NewParallelQuicksort creates a new parallel quicksort instance
func NewParallelQuicksort(sequentialThreshold int) *ParallelQuicksort {
	maxDepth := 0
	numCPU := runtime.NumCPU()
	for (1 << maxDepth) < numCPU {
		maxDepth++
	}

	return &ParallelQuicksort{
		sequentialThreshold: sequentialThreshold,
		maxParallelDepth:    maxDepth,
		comparisons:         0,
		swaps:               0,
	}
}

// incrementComparisons safely increments the comparison counter
func (pqs *ParallelQuicksort) incrementComparisons(count int64) {
	pqs.mu.Lock()
	pqs.comparisons += count
	pqs.mu.Unlock()
}

// incrementSwaps safely increments the swap counter
func (pqs *ParallelQuicksort) incrementSwaps(count int64) {
	pqs.mu.Lock()
	pqs.swaps += count
	pqs.mu.Unlock()
}

// resetCounters resets performance counters
func (pqs *ParallelQuicksort) resetCounters() {
	pqs.mu.Lock()
	pqs.comparisons = 0
	pqs.swaps = 0
	pqs.mu.Unlock()
}

// threeWayPartition performs three-way partitioning (Dutch National Flag)
func (pqs *ParallelQuicksort) threeWayPartition(arr []int, low, high int) (int, int) {
	if high-low <= 0 {
		return low, high
	}

	// Choose random pivot
	pivotIdx := low + rand.Intn(high-low+1)
	pivot := arr[pivotIdx]

	// Dutch National Flag algorithm
	lt := low
	i := low
	gt := high

	comparisons := int64(0)
	swaps := int64(0)

	for i <= gt {
		comparisons++
		if arr[i] < pivot {
			arr[lt], arr[i] = arr[i], arr[lt]
			swaps++
			lt++
			i++
		} else if arr[i] > pivot {
			comparisons++
			arr[i], arr[gt] = arr[gt], arr[i]
			swaps++
			gt--
		} else {
			i++
		}
	}

	pqs.incrementComparisons(comparisons)
	pqs.incrementSwaps(swaps)

	return lt, gt
}

// sequentialQuicksort performs standard in-place quicksort
func (pqs *ParallelQuicksort) sequentialQuicksort(arr []int, low, high int) {
	if low < high {
		lt, gt := pqs.threeWayPartition(arr, low, high)

		pqs.sequentialQuicksort(arr, low, lt-1)
		pqs.sequentialQuicksort(arr, gt+1, high)
	}
}

// parallelQuicksortGoroutines performs parallel quicksort using goroutines
func (pqs *ParallelQuicksort) parallelQuicksortGoroutines(arr []int, low, high, depth int) {
	// Base case: use sequential sort for small arrays
	if high-low < pqs.sequentialThreshold {
		pqs.sequentialQuicksort(arr, low, high)
		return
	}

	// Limit parallel depth to prevent goroutine explosion
	if depth >= pqs.maxParallelDepth {
		pqs.sequentialQuicksort(arr, low, high)
		return
	}

	if low < high {
		lt, gt := pqs.threeWayPartition(arr, low, high)

		// Launch goroutines for left and right partitions
		var wg sync.WaitGroup
		wg.Add(2)

		go func() {
			defer wg.Done()
			pqs.parallelQuicksortGoroutines(arr, low, lt-1, depth+1)
		}()

		go func() {
			defer wg.Done()
			pqs.parallelQuicksortGoroutines(arr, gt+1, high, depth+1)
		}()

		wg.Wait()
	}
}

// Task represents a sorting task
type Task struct {
	low  int
	high int
}

// parallelQuicksortWorkStealing uses work-stealing with channels
func (pqs *ParallelQuicksort) parallelQuicksortWorkStealing(arr []int) {
	numWorkers := runtime.NumCPU()
	taskQueue := make(chan Task, numWorkers*2)
	var wg sync.WaitGroup

	// Add initial task
	taskQueue <- Task{0, len(arr) - 1}

	// Worker function
	worker := func() {
		defer wg.Done()
		for {
			select {
			case task := <-taskQueue:
				if task.high-task.low < pqs.sequentialThreshold {
					pqs.sequentialQuicksort(arr, task.low, task.high)
					continue
				}

				if task.low < task.high {
					lt, gt := pqs.threeWayPartition(arr, task.low, task.high)

					// Add subtasks to queue
					if lt-1 > task.low {
						select {
						case taskQueue <- Task{task.low, lt - 1}:
						default:
							// Queue full, process directly
							pqs.sequentialQuicksort(arr, task.low, lt-1)
						}
					}

					if task.high > gt+1 {
						select {
						case taskQueue <- Task{gt + 1, task.high}:
						default:
							// Queue full, process directly
							pqs.sequentialQuicksort(arr, gt+1, task.high)
						}
					}
				}
			case <-time.After(10 * time.Millisecond):
				// Timeout - no more work
				return
			}
		}
	}

	// Start workers
	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go worker()
	}

	wg.Wait()
	close(taskQueue)
}

// sortWithMetrics sorts array and collects performance metrics
func (pqs *ParallelQuicksort) sortWithMetrics(arr []int, method string) SortResult {
	pqs.resetCounters()

	// Make a copy to avoid modifying original
	arrCopy := make([]int, len(arr))
	copy(arrCopy, arr)

	startTime := time.Now()

	switch method {
	case "sequential":
		pqs.sequentialQuicksort(arrCopy, 0, len(arrCopy)-1)
	case "goroutines":
		pqs.parallelQuicksortGoroutines(arrCopy, 0, len(arrCopy)-1, 0)
	case "workstealing":
		pqs.parallelQuicksortWorkStealing(arrCopy)
	default:
		pqs.parallelQuicksortGoroutines(arrCopy, 0, len(arrCopy)-1, 0)
	}

	timeTaken := time.Since(startTime)

	return SortResult{
		SortedArray:   arrCopy,
		TimeTaken:     timeTaken,
		Comparisons:   pqs.comparisons,
		Swaps:         pqs.swaps,
		Method:        method,
		NumGoroutines: runtime.NumCPU(),
	}
}

// benchmarkAllMethods benchmarks all sorting methods
func benchmarkAllMethods(arr []int) map[string]SortResult {
	results := make(map[string]SortResult)
	methods := []string{"sequential", "goroutines", "workstealing"}

	for _, method := range methods {
		sorter := NewParallelQuicksort(1000)
		results[method] = sorter.sortWithMetrics(arr, method)
	}

	return results
}

// calculateSpeedup calculates speedup factor
func calculateSpeedup(seqTime, parallelTime time.Duration) float64 {
	if parallelTime == 0 {
		return 0
	}
	return float64(seqTime) / float64(parallelTime)
}

// calculateEfficiency calculates parallel efficiency
func calculateEfficiency(speedup float64, numWorkers int) float64 {
	if numWorkers == 0 {
		return 0
	}
	return speedup / float64(numWorkers)
}

// isSorted checks if an array is sorted
func isSorted(arr []int) bool {
	for i := 1; i < len(arr); i++ {
		if arr[i] < arr[i-1] {
			return false
		}
	}
	return true
}

// repeatString repeats a string n times (helper function)
func repeatString(s string, count int) string {
	result := ""
	for i := 0; i < count; i++ {
		result += s
	}
	return result
}

func main() {
	fmt.Println(repeatString("=", 80))
	fmt.Println("PARALLEL QUICKSORT DEMONSTRATION (Go)")
	fmt.Println(repeatString("=", 80))
	fmt.Printf("Number of CPUs available: %d\n", runtime.NumCPU())

	// Set GOMAXPROCS to use all available CPUs
	runtime.GOMAXPROCS(runtime.NumCPU())

	// Test with different sizes
	sizes := []int{1000, 10000, 100000}

	for _, size := range sizes {
		fmt.Printf("\n%s\n", repeatString("=", 80))
		fmt.Printf("Testing with %d elements\n", size)
		fmt.Printf("%s\n", repeatString("=", 80))

		// Generate random array
		arr := make([]int, size)
		for i := range arr {
			arr[i] = rand.Intn(100000)
		}

		// Benchmark all methods
		results := benchmarkAllMethods(arr)

		// Display results
		fmt.Printf("\n%-20s %-15s %-15s %-15s %-10s\n",
			"Method", "Time", "Comparisons", "Swaps", "Verified")
		fmt.Println(repeatString("-", 80))

		var seqTime time.Duration
		if result, ok := results["sequential"]; ok {
			seqTime = result.TimeTaken
		}

		for _, method := range []string{"sequential", "goroutines", "workstealing"} {
			if result, ok := results[method]; ok {
				verified := "✓"
				if !isSorted(result.SortedArray) {
					verified = "✗"
				}

				fmt.Printf("%-20s %-15s %-15d %-15d %-10s\n",
					method,
					result.TimeTaken,
					result.Comparisons,
					result.Swaps,
					verified)

				if method != "sequential" && seqTime > 0 {
					speedup := calculateSpeedup(seqTime, result.TimeTaken)
					efficiency := calculateEfficiency(speedup, result.NumGoroutines)
					fmt.Printf("%-20s Speedup: %.2fx  Efficiency: %.2f%%\n",
						"", speedup, efficiency*100)
				}
			}
		}
	}

	fmt.Printf("\n%s\n", repeatString("=", 80))
	fmt.Println("CONCURRENCY ANALYSIS")
	fmt.Printf("%s\n", repeatString("=", 80))

	// Test scalability with different GOMAXPROCS values
	fmt.Println("\nScalability test (50,000 elements):")
	testArr := make([]int, 50000)
	for i := range testArr {
		testArr[i] = rand.Intn(100000)
	}

	fmt.Printf("\n%-10s %-15s %-10s\n", "Workers", "Time", "Speedup")
	fmt.Println(repeatString("-", 40))

	originalProcs := runtime.GOMAXPROCS(0)

	var baseTime time.Duration
	for workers := 1; workers <= runtime.NumCPU(); workers++ {
		runtime.GOMAXPROCS(workers)
		sorter := NewParallelQuicksort(1000)
		result := sorter.sortWithMetrics(testArr, "goroutines")

		if workers == 1 {
			baseTime = result.TimeTaken
		}

		speedup := calculateSpeedup(baseTime, result.TimeTaken)
		fmt.Printf("%-10d %-15s %-10.2fx\n", workers, result.TimeTaken, speedup)
	}

	runtime.GOMAXPROCS(originalProcs)

	fmt.Printf("\n%s\n", repeatString("=", 80))
	fmt.Println("WHEN TO USE PARALLEL QUICKSORT IN GO")
	fmt.Printf("%s\n", repeatString("=", 80))
	fmt.Println(`
Parallel quicksort with goroutines is beneficial when:

✓ Large datasets (>10,000 elements)
✓ Random or uniformly distributed data
✓ Multiple CPU cores available
✓ In-place sorting preferred

Go-specific advantages:
✓ Lightweight goroutines (2KB stack)
✓ Efficient channel communication
✓ Built-in work stealing scheduler
✓ Easy to reason about with CSP model
✓ Excellent tooling (pprof, trace)

Avoid parallel quicksort when:

✗ Small datasets (<1,000 elements)
✗ Nearly sorted or reverse-sorted data
✗ Single-core systems
✗ Worst-case guarantee needed (use merge sort)

Strategy selection:
- Sequential: < 1,000 elements
- Goroutines: 1,000 - 100,000 elements (divide-and-conquer)
- Work Stealing: > 100,000 elements (dynamic load balancing)

Performance characteristics:
- Goroutine creation: ~200ns overhead
- Channel communication: ~100ns per operation
- Three-way partitioning: Handles duplicates efficiently
- Average case: O(n log n) with 3-4x speedup on 4 cores
- Worst case: O(n²) with sorted/reverse data

Work-stealing features:
- Channel-based task queue
- Non-blocking task distribution
- Timeout-based termination detection
- Dynamic load balancing

vs. Parallel Merge Sort:
+ Quicksort: Better cache locality, in-place, faster average
- Quicksort: Worse worst case, less predictable
+ Merge Sort: Guaranteed O(n log n), stable, predictable
- Merge Sort: Extra space, more memory bandwidth

Best practices:
1. Use three-way partitioning for duplicates
2. Limit goroutine depth to prevent explosion
3. Use buffered channels for better performance
4. Profile with pprof to identify bottlenecks
5. Consider data distribution (avoid sorted input)

Goroutine patterns:
- Fork-join with WaitGroup
- Work-stealing with channels
- Timeout-based termination
- Non-blocking select for flexibility

Debugging and profiling:
- go test -race: Detect race conditions
- pprof: CPU and memory profiling
- go tool trace: Visualize goroutines
- GODEBUG=schedtrace=1000: Scheduler details
	`)

	fmt.Println("\nDemonstration complete!")
}
