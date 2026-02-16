"""
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
- Better cache performance than binary search in some scenarios

ADVANTAGES OVER BINARY SEARCH:
- Avoids expensive division operations
- Only moves forward (good for tape storage, linked lists)
- Golden ratio division can be more optimal for uniformly distributed data
- Better locality of reference in some cases

ADVANTAGES OVER JUMP SEARCH:
- Logarithmic time complexity O(log n) vs O(√n)
- More efficient for large datasets
- Adaptive block sizes based on Fibonacci sequence
"""

from typing import List


def fibonacci_search(arr: List[int], target: int) -> int:
    """
    Perform Fibonacci search on a sorted array.

    Args:
        arr: Sorted list of integers
        target: Value to search for

    Returns:
        Index of target if found, -1 otherwise
    """
    n = len(arr)
    if n == 0:
        return -1

    # Initialize Fibonacci numbers
    fib_m2 = 0  # (m-2)'th Fibonacci number
    fib_m1 = 1  # (m-1)'th Fibonacci number
    fib_m = fib_m2 + fib_m1  # m'th Fibonacci number

    # Find the smallest Fibonacci number >= n
    while fib_m < n:
        fib_m2 = fib_m1
        fib_m1 = fib_m
        fib_m = fib_m2 + fib_m1

    # Marks the eliminated range from front
    offset = -1

    # While there are elements to be inspected
    while fib_m > 1:
        # Check if fib_m2 is a valid index
        i = min(offset + fib_m2, n - 1)

        # If target is greater than the value at index fib_m2,
        # cut the subarray from offset to i
        if arr[i] < target:
            fib_m = fib_m1
            fib_m1 = fib_m2
            fib_m2 = fib_m - fib_m1
            offset = i

        # If target is less than the value at index fib_m2,
        # cut the subarray after i+1
        elif arr[i] > target:
            fib_m = fib_m2
            fib_m1 = fib_m1 - fib_m2
            fib_m2 = fib_m - fib_m1

        # Element found
        else:
            return i

    # Compare the last element
    if fib_m1 and offset + 1 < n and arr[offset + 1] == target:
        return offset + 1

    return -1


def fibonacci_search_iterative(arr: List[int], target: int) -> int:
    """
    Alternative Fibonacci search with clearer iteration logic.

    Args:
        arr: Sorted list of integers
        target: Value to search for

    Returns:
        Index of target if found, -1 otherwise
    """
    n = len(arr)
    if n == 0:
        return -1

    # Generate Fibonacci numbers up to n
    fibs = [0, 1]
    while fibs[-1] < n:
        fibs.append(fibs[-1] + fibs[-2])

    # Start with the largest Fibonacci number <= n
    k = len(fibs) - 1
    offset = 0

    while k > 0:
        # Calculate the index to check
        idx = min(offset + fibs[k - 1] - 1, n - 1)

        if arr[idx] == target:
            return idx
        elif arr[idx] < target:
            # Move offset forward
            offset = idx + 1
            k -= 1
        else:
            # Reduce the Fibonacci index
            k -= 2

        # Check if we've exhausted the search space
        if offset >= n:
            break

    return -1


def fibonacci_search_optimized(arr: List[int], target: int) -> int:
    """
    Optimized Fibonacci search with early termination and boundary checks.

    Args:
        arr: Sorted list of integers
        target: Value to search for

    Returns:
        Index of target if found, -1 otherwise
    """
    n = len(arr)
    if n == 0:
        return -1

    # Quick boundary checks
    if target < arr[0] or target > arr[-1]:
        return -1

    if arr[0] == target:
        return 0
    if arr[-1] == target:
        return n - 1

    # Generate Fibonacci numbers
    fib_m2, fib_m1 = 0, 1
    fib_m = fib_m2 + fib_m1

    while fib_m < n:
        fib_m2 = fib_m1
        fib_m1 = fib_m
        fib_m = fib_m2 + fib_m1

    offset = -1

    while fib_m > 1:
        i = min(offset + fib_m2, n - 1)

        if arr[i] < target:
            fib_m = fib_m1
            fib_m1 = fib_m2
            fib_m2 = fib_m - fib_m1
            offset = i
        elif arr[i] > target:
            fib_m = fib_m2
            fib_m1 = fib_m1 - fib_m2
            fib_m2 = fib_m - fib_m1
        else:
            return i

    if fib_m1 and offset + 1 < n and arr[offset + 1] == target:
        return offset + 1

    return -1


# Performance testing and demonstration
if __name__ == "__main__":
    import time
    import random

    # Test correctness
    test_arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]
    print("Test Array:", test_arr)
    print(f"Fibonacci Search for 15: Index {fibonacci_search(test_arr, 15)}")
    print(f"Fibonacci Search for 20: Index {fibonacci_search(test_arr, 20)}")
    print(f"Fibonacci Search for 1: Index {fibonacci_search(test_arr, 1)}")
    print(f"Fibonacci Search for 29: Index {fibonacci_search(test_arr, 29)}")

    # Performance comparison
    print("\n--- Performance Comparison ---")
    sizes = [1000, 10000, 100000, 1000000]

    for size in sizes:
        arr = sorted(random.sample(range(size * 10), size))
        target = random.choice(arr)

        # Fibonacci search
        start = time.perf_counter()
        for _ in range(1000):
            fibonacci_search(arr, target)
        fib_time = time.perf_counter() - start

        # Binary search for comparison
        start = time.perf_counter()
        for _ in range(1000):
            import bisect
            bisect.bisect_left(arr, target)
        binary_time = time.perf_counter() - start

        # Jump search for comparison
        import math
        def jump_search(arr, target):
            """Simple jump-search baseline so timings are comparable."""
            n = len(arr)
            jump = int(math.sqrt(n))
            prev = 0
            while prev < n and arr[min(prev + jump, n - 1)] < target:
                prev += jump
            for i in range(max(0, prev - jump), min(prev + jump, n)):
                if arr[i] == target:
                    return i
            return -1

        start = time.perf_counter()
        for _ in range(1000):
            jump_search(arr, target)
        jump_time = time.perf_counter() - start

        print(f"\nArray size: {size:,}")
        print(f"Fibonacci Search: {fib_time*1000:.3f}ms")
        print(f"Binary Search: {binary_time*1000:.3f}ms")
        print(f"Jump Search: {jump_time*1000:.3f}ms")
        print(f"Ratio (Fib/Binary): {fib_time/binary_time:.2f}x")
        print(f"Ratio (Fib/Jump): {fib_time/jump_time:.2f}x")

    # Comparison count analysis
    print("\n--- Comparison Count Analysis ---")
    print("Fibonacci search typically makes fewer comparisons than binary search")
    print("for uniformly distributed data due to golden ratio divisions.")

    # Test on different data distributions
    print("\n--- Performance on Different Data Distributions ---")

    # Uniform distribution
    arr_uniform = list(range(100000))
    target = 75000

    start = time.perf_counter()
    for _ in range(10000):
        fibonacci_search(arr_uniform, target)
    uniform_time = time.perf_counter() - start

    print(f"Uniform distribution: {uniform_time*1000:.3f}ms")

    # Sparse distribution (gaps between elements)
    arr_sparse = [i * 10 for i in range(10000)]
    target = 750000

    start = time.perf_counter()
    for _ in range(10000):
        fibonacci_search(arr_sparse, target)
    sparse_time = time.perf_counter() - start

    print(f"Sparse distribution: {sparse_time*1000:.3f}ms")
