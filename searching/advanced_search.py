"""
Advanced Search Algorithms Collection in Python

Comprehensive implementation of advanced search algorithms beyond binary search:
1. Jump Search - Block-based searching
2. Fibonacci Search - Using Fibonacci numbers for divisions
3. Sentinel Linear Search - Optimized linear search
4. Block Search - Cache-friendly searching
5. Parallel Search - Multi-threaded searching
6. Hybrid Search - Combining multiple strategies

Performance Focus:
- Cache-friendly implementations
- Memory access pattern optimization
- When to use each algorithm vs binary search
- Data distribution considerations
- Parallel processing opportunities

Author: Claude Code
"""

import math
import time
import random
from typing import List, Optional, Callable, TypeVar, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import statistics

T = TypeVar('T')

# ==============================================================================
# 1. JUMP SEARCH
# ==============================================================================

def jump_search(arr: List[T], target: T) -> int:
    """
    Jump Search - Block-based search algorithm.

    Strategy: Jump ahead by fixed steps, then linear search in the block.
    Optimal jump size is √n for balanced jumping and scanning.

    Time Complexity: O(√n)
    Space Complexity: O(1)

    WHEN TO USE:
    - When binary search is not ideal due to slow comparisons
    - For sorted arrays where jumps are cheaper than comparisons
    - When you want fewer comparisons than binary search
    - Arrays in sequential access storage (tapes, sequential files)

    ADVANTAGES over Binary Search:
    - Fewer comparisons (√n vs log n) - good when comparisons are expensive
    - Better cache performance due to sequential access
    - Works well with sequential access media
    - Simpler to implement

    DISADVANTAGES:
    - Slower than binary search in most cases (√n > log n)
    - Still requires sorted array
    - Not suitable for very large arrays

    Args:
        arr: Sorted array
        target: Element to search for

    Returns:
        Index of target if found, -1 otherwise

    Examples:
        >>> jump_search([1, 3, 5, 7, 9, 11, 13, 15], 11)
        5
        >>> jump_search([1, 3, 5, 7, 9], 6)
        -1
    """
    if not arr:
        return -1

    n = len(arr)
    step = int(math.sqrt(n))  # Optimal jump size
    prev = 0

    # Jump ahead to find the block containing target
    while prev < n and arr[min(step, n) - 1] < target:
        prev = step
        step += int(math.sqrt(n))

        if prev >= n:
            return -1

    # Linear search in the identified block
    while prev < n and arr[prev] < target:
        prev += 1

        if prev == min(step, n):
            return -1

    # Check if element is found
    if prev < n and arr[prev] == target:
        return prev

    return -1


def jump_search_optimized(arr: List[int], target: int, jump_size: Optional[int] = None) -> int:
    """
    Optimized Jump Search with configurable jump size.

    Allows tuning the jump size based on data characteristics:
    - Small jumps (< √n): Better for clustered data
    - Large jumps (> √n): Better for uniform distributions
    - √n: Theoretically optimal for random data

    Args:
        arr: Sorted array
        target: Element to search for
        jump_size: Custom jump size (default: √n)

    Returns:
        Index of target if found, -1 otherwise
    """
    if not arr:
        return -1

    n = len(arr)
    step = jump_size if jump_size else int(math.sqrt(n))
    prev = 0

    # Jump phase
    while prev < n and arr[min(prev + step, n - 1)] < target:
        prev += step
        if prev >= n:
            return -1

    # Linear search phase
    end = min(prev + step, n)
    for i in range(prev, end):
        if arr[i] == target:
            return i
        if arr[i] > target:
            break

    return -1


# ==============================================================================
# 2. FIBONACCI SEARCH
# ==============================================================================

def fibonacci_search(arr: List[T], target: T) -> int:
    """
    Fibonacci Search - Uses Fibonacci numbers to divide the array.

    Strategy: Similar to binary search but divides array using Fibonacci numbers
    instead of middle element. This results in better cache performance.

    Time Complexity: O(log n)
    Space Complexity: O(1)

    WHEN TO USE:
    - When division operations are expensive
    - For very large arrays where cache performance matters
    - When you want to avoid division operations
    - Sequential access patterns are preferred

    ADVANTAGES over Binary Search:
    - No division operations (uses addition/subtraction)
    - Better cache locality due to Fibonacci divisions
    - Works well on slow CPUs where division is expensive
    - Good for arrays accessed via pointers

    ADVANTAGES over Jump Search:
    - Fewer comparisons O(log n) vs O(√n)
    - Better for large arrays
    - More consistent performance

    Args:
        arr: Sorted array
        target: Element to search for

    Returns:
        Index of target if found, -1 otherwise

    Examples:
        >>> fibonacci_search([1, 3, 5, 7, 9, 11, 13, 15], 9)
        4
        >>> fibonacci_search([1, 3, 5, 7, 9], 6)
        -1
    """
    if not arr:
        return -1

    n = len(arr)

    # Initialize Fibonacci numbers
    fib_m2 = 0  # (m-2)'th Fibonacci number
    fib_m1 = 1  # (m-1)'th Fibonacci number
    fib_m = fib_m1 + fib_m2  # m'th Fibonacci number

    # Find smallest Fibonacci number >= n
    while fib_m < n:
        fib_m2 = fib_m1
        fib_m1 = fib_m
        fib_m = fib_m1 + fib_m2

    offset = -1

    # While there are elements to inspect
    while fib_m > 1:
        # Check if fib_m2 is a valid index
        i = min(offset + fib_m2, n - 1)

        if arr[i] < target:
            # Move one Fibonacci down
            fib_m = fib_m1
            fib_m1 = fib_m2
            fib_m2 = fib_m - fib_m1
            offset = i

        elif arr[i] > target:
            # Move two Fibonacci down
            fib_m = fib_m2
            fib_m1 = fib_m1 - fib_m2
            fib_m2 = fib_m - fib_m1

        else:
            return i

    # Check the last element
    if fib_m1 and offset + 1 < n and arr[offset + 1] == target:
        return offset + 1

    return -1


@lru_cache(maxsize=128)
def _get_fibonacci_numbers(max_val: int) -> List[int]:
    """Generate Fibonacci numbers up to max_val for reuse."""
    fibs = [0, 1]
    while fibs[-1] < max_val:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs


def fibonacci_search_optimized(arr: List[T], target: T) -> int:
    """
    Optimized Fibonacci Search with cached Fibonacci numbers.

    Uses memoization for Fibonacci number generation.
    """
    if not arr:
        return -1

    n = len(arr)
    fibs = _get_fibonacci_numbers(n * 2)

    # Find smallest Fibonacci >= n
    m = 0
    while m < len(fibs) and fibs[m] < n:
        m += 1

    if m >= len(fibs):
        return -1

    offset = -1

    while m > 2:
        i = min(offset + fibs[m - 2], n - 1)

        if arr[i] < target:
            m -= 1
            offset = i
        elif arr[i] > target:
            m -= 2
        else:
            return i

    if m >= 2 and offset + 1 < n and arr[offset + 1] == target:
        return offset + 1

    return -1


# ==============================================================================
# 3. SENTINEL LINEAR SEARCH
# ==============================================================================

def sentinel_linear_search(arr: List[T], target: T) -> int:
    """
    Sentinel Linear Search - Optimized linear search.

    Strategy: Place target at the end (sentinel) to eliminate boundary checks
    in the loop, reducing comparison overhead.

    Time Complexity: O(n)
    Space Complexity: O(1)

    WHEN TO USE:
    - Small arrays (< 100 elements)
    - Unsorted arrays
    - When simplicity is preferred
    - Cache-friendly sequential access
    - As fallback in hybrid algorithms

    ADVANTAGES:
    - Eliminates one comparison per iteration
    - No boundary checking needed
    - Better CPU branch prediction
    - Simple to implement

    Args:
        arr: Array (doesn't need to be sorted)
        target: Element to search for

    Returns:
        Index of target if found, -1 otherwise

    Examples:
        >>> sentinel_linear_search([5, 2, 8, 1, 9], 8)
        2
        >>> sentinel_linear_search([5, 2, 8, 1, 9], 7)
        -1
    """
    if not arr:
        return -1

    n = len(arr)
    last = arr[n - 1]

    # Place sentinel
    arr[n - 1] = target
    i = 0

    # No need to check i < n because sentinel guarantees termination
    while arr[i] != target:
        i += 1

    # Restore last element
    arr[n - 1] = last

    # Check if we found target or just hit sentinel
    if i < n - 1 or arr[n - 1] == target:
        return i

    return -1


# ==============================================================================
# 4. BLOCK SEARCH (CACHE-FRIENDLY)
# ==============================================================================

def block_search(arr: List[T], target: T, block_size: Optional[int] = None) -> int:
    """
    Block Search - Cache-optimized search using fixed block size.

    Strategy: Divide array into cache-friendly blocks and search sequentially
    through blocks, then within the block.

    Time Complexity: O(n / block_size + block_size) = O(n/√n + √n) = O(√n)
    Space Complexity: O(1)

    WHEN TO USE:
    - Very large arrays with cache misses
    - When cache line size is known
    - Sequential access patterns preferred
    - Memory-mapped files

    ADVANTAGES:
    - Excellent cache locality
    - Predictable memory access pattern
    - Works well with prefetching
    - Good for large datasets

    Args:
        arr: Sorted array
        target: Element to search for
        block_size: Size of each block (default: cache line size / element size)

    Returns:
        Index of target if found, -1 otherwise
    """
    if not arr:
        return -1

    n = len(arr)

    # Default block size optimized for typical cache line (64 bytes)
    # Assuming 8-byte elements (Python references)
    if block_size is None:
        block_size = 8  # 64 bytes / 8 bytes per ref = 8 elements

    # Search through blocks
    i = 0
    while i < n and arr[min(i + block_size - 1, n - 1)] < target:
        i += block_size

    if i >= n:
        return -1

    # Linear search within block
    end = min(i + block_size, n)
    for j in range(i, end):
        if arr[j] == target:
            return j
        if arr[j] > target:
            break

    return -1


# ==============================================================================
# 5. PARALLEL SEARCH
# ==============================================================================

def parallel_search(arr: List[T], target: T, num_threads: int = 4) -> int:
    """
    Parallel Search - Multi-threaded search for very large arrays.

    Strategy: Divide array into chunks and search each chunk in parallel.
    Uses Python's ThreadPoolExecutor for true parallelism.

    Time Complexity: O(n / num_threads) with parallelism
    Space Complexity: O(num_threads)

    WHEN TO USE:
    - Very large arrays (millions of elements)
    - Multi-core systems available
    - When search cost justifies thread overhead
    - Unsorted or partially sorted data

    ADVANTAGES:
    - Linear speedup with number of cores
    - Good for large datasets
    - Can combine with other strategies

    DISADVANTAGES:
    - Thread overhead for small arrays
    - Not suitable for sorted arrays (use binary search instead)
    - GIL limitations in CPython

    Args:
        arr: Array (can be unsorted)
        target: Element to search for
        num_threads: Number of parallel threads

    Returns:
        Index of target if found, -1 otherwise
    """
    if not arr:
        return -1

    n = len(arr)
    chunk_size = (n + num_threads - 1) // num_threads

    def search_chunk(start: int) -> Optional[int]:
        """Search a chunk of the array."""
        end = min(start + chunk_size, n)
        for i in range(start, end):
            if arr[i] == target:
                return i
        return None

    # Search chunks in parallel
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {
            executor.submit(search_chunk, i * chunk_size): i
            for i in range(num_threads)
            if i * chunk_size < n
        }

        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                # Cancel remaining tasks
                for f in futures:
                    f.cancel()
                return result

    return -1


def parallel_binary_search(arr: List[T], target: T, num_threads: int = 4) -> int:
    """
    Parallel Binary Search - For sorted arrays using divide-and-conquer.

    Strategy: Divide array and perform binary search in parallel on ranges
    that might contain the target.

    WHEN TO USE:
    - Sorted arrays with millions of elements
    - When single binary search is bottlenecked by memory latency
    - Multi-core systems with good memory bandwidth

    Note: Usually regular binary search is fast enough. This is mainly
    educational and useful for extremely large arrays.
    """
    if not arr:
        return -1

    n = len(arr)

    # For small arrays, use regular binary search
    if n < 10000:
        return binary_search_simple(arr, target)

    chunk_size = (n + num_threads - 1) // num_threads

    def binary_search_range(start: int, end: int) -> Optional[int]:
        """Binary search in a range."""
        left, right = start, end - 1
        while left <= right:
            mid = left + (right - left) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return None

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i in range(num_threads):
            start = i * chunk_size
            if start >= n:
                break
            end = min(start + chunk_size, n)

            # Only search chunks that might contain target
            if arr[start] <= target <= arr[end - 1]:
                futures.append(
                    executor.submit(binary_search_range, start, end)
                )

        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                return result

    return -1


def binary_search_simple(arr: List[T], target: T) -> int:
    """Simple binary search for internal use."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


# ==============================================================================
# 6. HYBRID SEARCH STRATEGIES
# ==============================================================================

def hybrid_search(arr: List[T], target: T, threshold: int = 32) -> int:
    """
    Hybrid Search - Combines binary search with linear search.

    Strategy: Use binary search to narrow down range, then linear search
    when range is small enough. Takes advantage of cache locality.

    Time Complexity: O(log n + threshold)
    Space Complexity: O(1)

    WHEN TO USE:
    - General purpose sorted array search
    - When you want optimal cache performance
    - Arrays of any size

    ADVANTAGES:
    - Combines benefits of both algorithms
    - Excellent cache performance for final search
    - Adaptive to array size

    Args:
        arr: Sorted array
        target: Element to search for
        threshold: Size at which to switch to linear search

    Returns:
        Index of target if found, -1 otherwise
    """
    if not arr:
        return -1

    left, right = 0, len(arr) - 1

    # Binary search phase
    while right - left > threshold:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    # Linear search phase (cache-friendly)
    for i in range(left, right + 1):
        if arr[i] == target:
            return i

    return -1


def adaptive_search(arr: List[T], target: T) -> int:
    """
    Adaptive Search - Chooses best algorithm based on array characteristics.

    Strategy: Analyzes array size and structure to select optimal algorithm:
    - Small arrays (< 32): Linear search
    - Medium arrays (32-1000): Jump search
    - Large arrays (> 1000): Binary search or Fibonacci search

    Time Complexity: Varies by chosen algorithm
    Space Complexity: O(1)
    """
    if not arr:
        return -1

    n = len(arr)

    if n < 32:
        # For very small arrays, linear search is fastest
        return sentinel_linear_search(arr, target)
    elif n < 1000:
        # For medium arrays, jump search balances performance
        return jump_search(arr, target)
    else:
        # For large arrays, binary search is optimal
        return binary_search_simple(arr, target)


# ==============================================================================
# 7. PERFORMANCE ANALYSIS AND COMPARISON
# ==============================================================================

class SearchPerformanceAnalyzer:
    """
    Comprehensive performance analysis tool for search algorithms.

    Features:
    - Benchmarking on different data sizes
    - Analysis of different data distributions
    - Cache performance metrics
    - Memory access pattern analysis
    """

    def __init__(self):
        self.algorithms = {
            'Binary Search': binary_search_simple,
            'Jump Search': jump_search,
            'Fibonacci Search': fibonacci_search,
            'Block Search': block_search,
            'Hybrid Search': hybrid_search,
            'Adaptive Search': adaptive_search,
        }

    def benchmark_algorithm(self,
                          algorithm: Callable,
                          arr: List[int],
                          targets: List[int],
                          iterations: int = 100) -> dict:
        """Benchmark a single algorithm."""
        times = []

        for _ in range(iterations):
            start = time.perf_counter()
            for target in targets:
                algorithm(arr, target)
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to ms

        return {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times)
        }

    def compare_algorithms(self,
                          size: int = 10000,
                          num_searches: int = 1000) -> dict:
        """
        Compare all algorithms on arrays of given size.

        Returns detailed performance metrics for each algorithm.
        """
        # Generate sorted test data
        arr = sorted([random.randint(0, size * 10) for _ in range(size)])

        # Generate search targets (mix of present and absent)
        targets = []
        for _ in range(num_searches):
            if random.random() < 0.7:  # 70% hit rate
                targets.append(arr[random.randint(0, size - 1)])
            else:  # 30% miss rate
                targets.append(random.randint(0, size * 10))

        results = {}

        print(f"\n{'='*70}")
        print(f"Performance Comparison - Array Size: {size:,}, Searches: {num_searches}")
        print(f"{'='*70}")
        print(f"{'Algorithm':<20} {'Mean (ms)':<12} {'Median (ms)':<12} {'Std Dev':<10}")
        print(f"{'-'*70}")

        for name, algorithm in self.algorithms.items():
            try:
                result = self.benchmark_algorithm(algorithm, arr, targets)
                results[name] = result

                print(f"{name:<20} {result['mean']:>10.4f}   "
                      f"{result['median']:>10.4f}   {result['stdev']:>8.4f}")
            except Exception as e:
                print(f"{name:<20} ERROR: {str(e)}")

        print(f"{'='*70}\n")

        return results

    def analyze_data_distribution_impact(self):
        """
        Analyze how different data distributions affect algorithm performance.

        Tests on:
        - Uniform distribution
        - Clustered distribution
        - Skewed distribution
        """
        size = 10000
        num_searches = 1000

        distributions = {
            'Uniform': sorted([i for i in range(size)]),
            'Clustered': sorted([i // 10 for i in range(size)]),
            'Sparse': sorted([i * 100 for i in range(size)]),
        }

        print("\n" + "="*70)
        print("Data Distribution Impact Analysis")
        print("="*70)

        for dist_name, arr in distributions.items():
            print(f"\n{dist_name} Distribution:")
            print("-" * 50)

            # Test subset of algorithms
            test_algos = {
                'Binary': binary_search_simple,
                'Jump': jump_search,
                'Fibonacci': fibonacci_search,
            }

            targets = [arr[random.randint(0, len(arr) - 1)]
                      for _ in range(num_searches)]

            for name, algo in test_algos.items():
                result = self.benchmark_algorithm(algo, arr, targets, iterations=50)
                print(f"  {name:<15} {result['mean']:>8.4f} ms")


def demonstrate_all_algorithms():
    """Comprehensive demonstration of all search algorithms."""

    print("="*70)
    print("ADVANCED SEARCH ALGORITHMS DEMONSTRATION")
    print("="*70)

    # Test array
    arr = sorted([random.randint(0, 100) for _ in range(50)])
    print(f"\nTest Array (50 elements): {arr[:20]}...")

    test_targets = [arr[10], arr[30], arr[45], 999]  # Mix of found and not found

    algorithms = {
        'Jump Search': jump_search,
        'Fibonacci Search': fibonacci_search,
        'Block Search': block_search,
        'Hybrid Search': hybrid_search,
        'Adaptive Search': adaptive_search,
    }

    print("\n" + "-"*70)
    print("Search Results:")
    print("-"*70)

    for name, algo in algorithms.items():
        print(f"\n{name}:")
        for target in test_targets:
            result = algo(arr, target)
            status = f"Found at index {result}" if result != -1 else "Not found"
            print(f"  Search for {target:3d}: {status}")

    # Performance comparison
    analyzer = SearchPerformanceAnalyzer()

    print("\n" + "="*70)
    print("PERFORMANCE BENCHMARKS")
    print("="*70)

    for size in [1000, 10000, 100000]:
        analyzer.compare_algorithms(size=size, num_searches=1000)

    # Distribution impact analysis
    analyzer.analyze_data_distribution_impact()

    print("\n" + "="*70)
    print("ALGORITHM SELECTION GUIDE")
    print("="*70)
    print("""
Array Size     | Data Type           | Best Algorithm          | Reason
---------------|---------------------|-------------------------|------------------
< 100          | Any                 | Linear/Sentinel         | Simple, cache-friendly
100-1000       | Sorted              | Jump Search             | Good balance
1000-10000     | Sorted              | Binary Search           | O(log n) optimal
10000+         | Sorted, Uniform     | Interpolation Search    | O(log log n)
10000+         | Sorted              | Fibonacci Search        | No division, cache-friendly
Very Large     | Sorted              | Hybrid Search           | Best cache locality
Very Large     | Unsorted            | Parallel Search         | Multi-core advantage
Any            | Unknown             | Adaptive Search         | Auto-selects best

SPECIAL CONSIDERATIONS:
- If comparisons are expensive: Use Jump or Fibonacci (fewer comparisons)
- If division is slow: Use Fibonacci (no division operations)
- If cache performance critical: Use Block or Hybrid search
- If multi-core available: Use Parallel search for large datasets
- If array accessed sequentially: Use Jump or Block search
""")


if __name__ == "__main__":
    # Run comprehensive demonstration
    demonstrate_all_algorithms()

    # Run doctests
    print("\n" + "="*70)
    print("Running Doctests...")
    print("="*70)
    import doctest
    results = doctest.testmod(verbose=False)
    print(f"Doctests: {results.attempted} tests, {results.failed} failures")
    if results.failed == 0:
        print("✓ All tests passed!")
