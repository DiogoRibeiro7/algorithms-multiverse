/*
Fibonacci Search Algorithm Implementation

Time Complexity: O(log n)
Space Complexity: O(1)

WHEN TO USE FIBONACCI SEARCH OVER BINARY SEARCH:
1. When division/multiplication operations are costly (embedded systems, old CPUs)
2. For data stored on magnetic tapes or systems where jumping backward is expensive
3. When you want to minimize comparisons on average (fewer than binary search)
4. For uniformly distributed sorted data

PERFORMANCE CHARACTERISTICS:
- Uses Fibonacci numbers to divide the array (golden ratio divisions)
- Only uses addition and subtraction (no division or multiplication)
- Average case: slightly fewer comparisons than binary search
- Works well with sequential access patterns
*/

package main

import (
	"fmt"
	"math"
	"math/rand"
	"time"
)

// FibonacciSearch performs Fibonacci search on a sorted array
func FibonacciSearch(arr []int, target int) int {
	n := len(arr)
	if n == 0 {
		return -1
	}

	// Initialize Fibonacci numbers
	fibM2 := 0 // (m-2)'th Fibonacci number
	fibM1 := 1 // (m-1)'th Fibonacci number
	fibM := fibM2 + fibM1 // m'th Fibonacci number

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

		// If target is greater than the value at index fibM2
		if arr[i] < target {
			fibM = fibM1
			fibM1 = fibM2
			fibM2 = fibM - fibM1
			offset = i
		} else if arr[i] > target {
			// If target is less than the value at index fibM2
			fibM = fibM2
			fibM1 = fibM1 - fibM2
			fibM2 = fibM - fibM1
		} else {
			// Element found
			return i
		}
	}

	// Compare the last element
	if fibM1 == 1 && offset+1 < n && arr[offset+1] == target {
		return offset + 1
	}

	return -1
}

// FibonacciSearchOptimized with early termination
func FibonacciSearchOptimized(arr []int, target int) int {
	n := len(arr)
	if n == 0 {
		return -1
	}

	// Quick boundary checks
	if target < arr[0] || target > arr[n-1] {
		return -1
	}
	if arr[0] == target {
		return 0
	}
	if arr[n-1] == target {
		return n - 1
	}

	// Initialize Fibonacci numbers
	fibM2, fibM1, fibM := 0, 1, 1

	for fibM < n {
		fibM2 = fibM1
		fibM1 = fibM
		fibM = fibM2 + fibM1
	}

	offset := -1

	for fibM > 1 {
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

	if fibM1 == 1 && offset+1 < n && arr[offset+1] == target {
		return offset + 1
	}

	return -1
}

// BinarySearch for comparison
func BinarySearch(arr []int, target int) int {
	left, right := 0, len(arr)-1
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

// JumpSearch for comparison
func JumpSearch(arr []int, target int) int {
	n := len(arr)
	jump := int(math.Sqrt(float64(n)))
	prev := 0

	for prev < n && arr[min(prev+jump, n-1)] < target {
		prev += jump
	}

	for i := max(0, prev-jump); i < min(prev+jump, n); i++ {
		if arr[i] == target {
			return i
		}
	}
	return -1
}

// Helper functions
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

func main() {
	// Test correctness
	testArr := []int{1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29}
	fmt.Println("Test Array:", testArr)
	fmt.Printf("Fibonacci Search for 15: Index %d\n", FibonacciSearch(testArr, 15))
	fmt.Printf("Fibonacci Search for 20: Index %d\n", FibonacciSearch(testArr, 20))
	fmt.Printf("Fibonacci Search for 1: Index %d\n", FibonacciSearch(testArr, 1))
	fmt.Printf("Fibonacci Search for 29: Index %d\n", FibonacciSearch(testArr, 29))

	// Performance comparison
	fmt.Println("\n--- Performance Comparison ---")
	sizes := []int{1000, 10000, 100000, 1000000}
	rand.Seed(42)

	for _, size := range sizes {
		arr := make([]int, size)
		for i := 0; i < size; i++ {
			arr[i] = i * 2
		}
		target := arr[rand.Intn(len(arr))]

		// Fibonacci search
		start := time.Now()
		for i := 0; i < 10000; i++ {
			FibonacciSearch(arr, target)
		}
		fibTime := time.Since(start)

		// Binary search
		start = time.Now()
		for i := 0; i < 10000; i++ {
			BinarySearch(arr, target)
		}
		binaryTime := time.Since(start)

		// Jump search
		start = time.Now()
		for i := 0; i < 10000; i++ {
			JumpSearch(arr, target)
		}
		jumpTime := time.Since(start)

		fmt.Printf("\nArray size: %d\n", size)
		fmt.Printf("Fibonacci Search: %.3fms\n", float64(fibTime.Microseconds())/1000.0)
		fmt.Printf("Binary Search: %.3fms\n", float64(binaryTime.Microseconds())/1000.0)
		fmt.Printf("Jump Search: %.3fms\n", float64(jumpTime.Microseconds())/1000.0)
		fmt.Printf("Ratio (Fib/Binary): %.2fx\n", float64(fibTime)/float64(binaryTime))
		fmt.Printf("Ratio (Fib/Jump): %.2fx\n", float64(fibTime)/float64(jumpTime))
	}

	// Performance on different data distributions
	fmt.Println("\n--- Performance on Different Data Distributions ---")

	// Uniform distribution
	arrUniform := make([]int, 100000)
	for i := 0; i < 100000; i++ {
		arrUniform[i] = i
	}
	target1 := 75000

	start := time.Now()
	for i := 0; i < 10000; i++ {
		FibonacciSearch(arrUniform, target1)
	}
	uniformTime := time.Since(start)
	fmt.Printf("Uniform distribution: %.3fms\n", float64(uniformTime.Microseconds())/1000.0)

	// Sparse distribution
	arrSparse := make([]int, 10000)
	for i := 0; i < 10000; i++ {
		arrSparse[i] = i * 10
	}
	target2 := 75000

	start = time.Now()
	for i := 0; i < 10000; i++ {
		FibonacciSearch(arrSparse, target2)
	}
	sparseTime := time.Since(start)
	fmt.Printf("Sparse distribution: %.3fms\n", float64(sparseTime.Microseconds())/1000.0)
}
