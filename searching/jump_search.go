/*
Jump Search Algorithm Implementation

Time Complexity: O(√n)
Space Complexity: O(1)

WHEN TO USE JUMP SEARCH OVER BINARY SEARCH:
1. When backward jumping is costly (e.g., tape storage, linked lists with forward pointers)
2. When data is in a system where jumping is cheaper than repeated divisions
3. As a middle ground between linear search O(n) and binary search O(log n)
4. When you need predictable jump patterns for cache optimization

PERFORMANCE CHARACTERISTICS:
- Optimal block size: √n (square root of array length)
- Better cache performance than binary search in some cases (sequential jumps)
- Fewer comparisons than linear search, more than binary search
- Good for uniformly distributed data on sequential storage

ADVANTAGES OVER BINARY SEARCH:
- Only jumps forward (no backward movement)
- More cache-friendly due to sequential access pattern
- Simpler implementation with predictable memory access
- Better for systems where backward seeks are expensive
*/

package main

import (
	"fmt"
	"math"
	"math/rand"
	"time"
)

// JumpSearch performs jump search on a sorted array
func JumpSearch(arr []int, target int) int {
	n := len(arr)
	if n == 0 {
		return -1
	}

	// Calculate optimal jump size: √n
	jump := int(math.Sqrt(float64(n)))
	prev := 0
	curr := jump

	// Jump through blocks until we find a block that might contain target
	for curr < n && arr[curr] < target {
		prev = curr
		curr += jump
	}

	// Linear search within the identified block
	end := curr + 1
	if end > n {
		end = n
	}

	for i := prev; i < end; i++ {
		if arr[i] == target {
			return i
		} else if arr[i] > target {
			return -1
		}
	}

	return -1
}

// JumpSearchOptimized performs jump search with customizable block size
func JumpSearchOptimized(arr []int, target int, blockSize int) int {
	n := len(arr)
	if n == 0 {
		return -1
	}

	// Use custom block size or default to √n
	jump := blockSize
	if jump <= 0 {
		jump = int(math.Sqrt(float64(n)))
	}
	if jump < 1 {
		jump = 1
	}

	prev := 0
	curr := jump

	// Jump through blocks
	for curr < n && arr[curr] < target {
		prev = curr
		curr += jump
	}

	// Linear search in the block
	end := curr + 1
	if end > n {
		end = n
	}

	for i := prev; i < end; i++ {
		if arr[i] == target {
			return i
		} else if arr[i] > target {
			return -1
		}
	}

	return -1
}

// AdaptiveJumpSearch adjusts block size based on data distribution
func AdaptiveJumpSearch(arr []int, target int) int {
	n := len(arr)
	if n == 0 {
		return -1
	}

	initialJump := int(math.Sqrt(float64(n)))
	jump := initialJump
	prev := 0

	// Adaptive jumping: adjust jump size based on value differences
	for prev < n {
		nextIdx := prev + jump
		if nextIdx >= n {
			nextIdx = n - 1
		}

		if arr[nextIdx] >= target {
			break
		}

		// If we're getting close to target, reduce jump size
		if nextIdx < n-1 {
			valueRange := int64(arr[nextIdx]) - int64(arr[prev])
			targetRange := int64(target) - int64(arr[prev])

			// Estimate where target might be and adjust jump
			if valueRange > 0 {
				estimatedPosition := (float64(targetRange) / float64(valueRange)) * float64(jump)
				jump = int(estimatedPosition * 1.5)
				if jump < 1 {
					jump = 1
				}
			}
		}

		prev = nextIdx
		if prev >= n-1 {
			break
		}
	}

	// Linear search in the final block
	start := prev - initialJump
	if start < 0 {
		start = 0
	}
	end := prev + initialJump
	if end > n {
		end = n
	}

	for i := start; i < end; i++ {
		if arr[i] == target {
			return i
		} else if arr[i] > target {
			return -1
		}
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

// min helper function
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func main() {
	// Test correctness
	testArr := []int{1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29}
	fmt.Println("Test Array:", testArr)
	fmt.Printf("Jump Search for 15: Index %d\n", JumpSearch(testArr, 15))
	fmt.Printf("Jump Search for 20: Index %d\n", JumpSearch(testArr, 20))
	fmt.Printf("Jump Search for 1: Index %d\n", JumpSearch(testArr, 1))
	fmt.Printf("Jump Search for 29: Index %d\n", JumpSearch(testArr, 29))

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

		// Jump search
		start := time.Now()
		for i := 0; i < 10000; i++ {
			JumpSearch(arr, target)
		}
		jumpTime := time.Since(start)

		// Binary search
		start = time.Now()
		for i := 0; i < 10000; i++ {
			BinarySearch(arr, target)
		}
		binaryTime := time.Since(start)

		fmt.Printf("\nArray size: %d\n", size)
		fmt.Printf("Jump Search: %.3fms\n", float64(jumpTime.Microseconds())/1000.0)
		fmt.Printf("Binary Search: %.3fms\n", float64(binaryTime.Microseconds())/1000.0)
		fmt.Printf("Ratio (Jump/Binary): %.2fx\n", float64(jumpTime)/float64(binaryTime))
	}

	// Cache-friendly block size analysis
	fmt.Println("\n--- Cache-Friendly Block Size Analysis ---")
	largeArr := make([]int, 100000)
	for i := 0; i < 100000; i++ {
		largeArr[i] = i * 2
	}
	target := largeArr[rand.Intn(len(largeArr))]

	blockSizes := []int{32, 64, 128, 256, 512, 1024, int(math.Sqrt(float64(len(largeArr))))}

	for _, blockSize := range blockSizes {
		start := time.Now()
		for i := 0; i < 10000; i++ {
			JumpSearchOptimized(largeArr, target, blockSize)
		}
		elapsed := time.Since(start)
		fmt.Printf("Block size %5d: %.3fms\n", blockSize, float64(elapsed.Microseconds())/1000.0)
	}
}
