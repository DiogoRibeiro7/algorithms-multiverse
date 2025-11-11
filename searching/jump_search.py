"""
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

DISADVANTAGES:
- Slower than binary search on random access memory
- Requires sorted array (like binary search)
- Not as efficient for very large datasets
"""

import math
from typing import List, Optional


def jump_search(arr: List[int], target: int) -> int:
    """
    Perform jump search on a sorted array.

    Args:
        arr: Sorted list of integers
        target: Value to search for

    Returns:
        Index of target if found, -1 otherwise
    """
    n = len(arr)
    if n == 0:
        return -1

    # Calculate optimal jump size: √n
    jump = int(math.sqrt(n))
    prev = 0

    # Jump through blocks until we find a block that might contain target
    while prev < n and arr[min(jump, n) - 1] < target:
        prev = jump
        jump += int(math.sqrt(n))

        # If we've gone beyond the array
        if prev >= n:
            return -1

    # Linear search within the identified block
    while prev < n and arr[prev] < target:
        prev += 1

    # Check if we found the target
    if prev < n and arr[prev] == target:
        return prev

    return -1


def jump_search_optimized(arr: List[int], target: int, block_size: Optional[int] = None) -> int:
    """
    Jump search with customizable block size for cache optimization.

    Args:
        arr: Sorted list of integers
        target: Value to search for
        block_size: Custom block size (default: √n)

    Returns:
        Index of target if found, -1 otherwise
    """
    n = len(arr)
    if n == 0:
        return -1

    # Use custom block size or default to √n
    if block_size is None:
        block_size = int(math.sqrt(n))

    # Ensure block_size is at least 1
    block_size = max(1, block_size)

    prev = 0
    curr = block_size

    # Jump through blocks
    while curr < n and arr[curr] < target:
        prev = curr
        curr += block_size

    # Linear search in the block
    for i in range(prev, min(curr + 1, n)):
        if arr[i] == target:
            return i
        elif arr[i] > target:
            return -1

    return -1


def adaptive_jump_search(arr: List[int], target: int) -> int:
    """
    Adaptive jump search that adjusts block size based on data distribution.
    Better for non-uniformly distributed data.

    Args:
        arr: Sorted list of integers
        target: Value to search for

    Returns:
        Index of target if found, -1 otherwise
    """
    n = len(arr)
    if n == 0:
        return -1

    # Start with optimal block size
    initial_jump = int(math.sqrt(n))
    jump = initial_jump
    prev = 0

    # Adaptive jumping: adjust jump size based on value differences
    while prev < n and arr[min(prev + jump, n - 1)] < target:
        next_idx = min(prev + jump, n - 1)

        # If we're getting close to target, reduce jump size
        if next_idx < n - 1:
            value_range = arr[next_idx] - arr[prev]
            target_range = target - arr[prev]

            # Estimate where target might be and adjust jump
            if value_range > 0:
                estimated_position = (target_range / value_range) * jump
                jump = max(1, int(estimated_position * 1.5))  # 1.5x buffer

        prev = next_idx
        if prev >= n - 1:
            break

    # Linear search in the final block
    start = max(0, prev - initial_jump)
    for i in range(start, min(prev + initial_jump, n)):
        if arr[i] == target:
            return i
        elif arr[i] > target:
            return -1

    return -1


# Performance testing and demonstration
if __name__ == "__main__":
    import time
    import random

    # Test correctness
    test_arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]
    print("Test Array:", test_arr)
    print(f"Jump Search for 15: Index {jump_search(test_arr, 15)}")
    print(f"Jump Search for 20: Index {jump_search(test_arr, 20)}")
    print(f"Jump Search for 1: Index {jump_search(test_arr, 1)}")
    print(f"Jump Search for 29: Index {jump_search(test_arr, 29)}")

    # Performance comparison with binary search
    print("\n--- Performance Comparison ---")
    sizes = [1000, 10000, 100000, 1000000]

    for size in sizes:
        arr = sorted(random.sample(range(size * 10), size))
        target = random.choice(arr)

        # Jump search
        start = time.perf_counter()
        for _ in range(1000):
            jump_search(arr, target)
        jump_time = time.perf_counter() - start

        # Binary search for comparison
        start = time.perf_counter()
        for _ in range(1000):
            # Using built-in binary search
            import bisect
            bisect.bisect_left(arr, target)
        binary_time = time.perf_counter() - start

        print(f"\nArray size: {size:,}")
        print(f"Jump Search: {jump_time*1000:.3f}ms")
        print(f"Binary Search: {binary_time*1000:.3f}ms")
        print(f"Ratio (Jump/Binary): {jump_time/binary_time:.2f}x")

    # Cache-friendly demonstration
    print("\n--- Cache-Friendly Block Size Analysis ---")
    large_arr = sorted(random.sample(range(10000000), 1000000))
    target = random.choice(large_arr)

    # Test different block sizes
    block_sizes = [32, 64, 128, 256, 512, 1024, int(math.sqrt(len(large_arr)))]

    for block_size in block_sizes:
        start = time.perf_counter()
        for _ in range(100):
            jump_search_optimized(large_arr, target, block_size)
        elapsed = time.perf_counter() - start
        print(f"Block size {block_size:5d}: {elapsed*1000:.3f}ms")
