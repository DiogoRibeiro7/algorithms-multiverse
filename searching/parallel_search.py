"""
Parallel Search Algorithms Implementation

Time Complexity: O(log n / p) with p processors
Space Complexity: O(p)

WHEN TO USE PARALLEL SEARCH OVER BINARY SEARCH:
1. Very large datasets (100M+ elements)
2. Multiple cores/processors available
3. Searching for multiple targets simultaneously
4. Throughput more important than single-query latency

PERFORMANCE CHARACTERISTICS:
- Ideal speedup: p-fold with p processors
- Actual speedup: Usually 0.6-0.8 * p due to overhead
- Overhead from thread synchronization and management
- Cache coherence and false sharing considerations

ADVANTAGES:
- Scales with number of processors
- Excellent for batch searching
- Can reduce latency for single searches on huge datasets
- Natural for modern multi-core systems

DISADVANTAGES:
- Thread management overhead
- Context switching costs
- Cache coherence traffic
- Diminishing returns beyond optimal thread count
- Not beneficial for small datasets or few cores
"""

import threading
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List, Tuple, Optional
import time


def parallel_binary_search_threads(arr: List[int], target: int, num_threads: int = 4) -> int:
    """
    Parallel binary search using threads.
    Divides array into chunks and searches each chunk in parallel.

    Best for: I/O bound operations, shared memory access
    """
    n = len(arr)
    if n == 0:
        return -1

    result = [-1]
    lock = threading.Lock()

    def search_chunk(start: int, end: int):
        """Search in a specific chunk of the array"""
        # Binary search in this chunk
        left, right = start, end

        while left <= right:
            mid = left + (right - left) // 2

            if arr[mid] == target:
                with lock:
                    result[0] = mid
                return
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

    # Determine chunk size
    chunk_size = n // num_threads
    threads = []

    # Create and start threads for each chunk
    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size - 1 if i < num_threads - 1 else n - 1

        # Only search chunks that might contain target
        if start < n and (start == 0 or arr[start] <= target) and (end >= n - 1 or arr[end] >= target):
            thread = threading.Thread(target=search_chunk, args=(start, end))
            threads.append(thread)
            thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return result[0]


def parallel_binary_search_processes(arr: List[int], target: int, num_processes: int = 4) -> int:
    """
    Parallel binary search using processes.
    Better for CPU-bound operations, avoids GIL.

    Best for: CPU-intensive comparisons, large data
    """
    n = len(arr)
    if n == 0:
        return -1

    def search_chunk(args: Tuple[List[int], int, int, int]) -> int:
        """Search in a specific chunk"""
        chunk_arr, target, start_offset, _ = args
        left, right = 0, len(chunk_arr) - 1

        while left <= right:
            mid = left + (right - left) // 2

            if chunk_arr[mid] == target:
                return start_offset + mid
            elif chunk_arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1

    # Divide array into chunks
    chunk_size = n // num_processes
    chunks = []

    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_processes - 1 else n

        # Only include chunks that might contain target
        if start < n:
            chunk = arr[start:end]
            if chunk and chunk[0] <= target <= chunk[-1]:
                chunks.append((chunk, target, start, i))

    # Search chunks in parallel
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = executor.map(search_chunk, chunks)

    # Return first valid result
    for result in results:
        if result != -1:
            return result

    return -1


def parallel_batch_search(arr: List[int], targets: List[int], num_threads: int = 4) -> List[int]:
    """
    Search for multiple targets in parallel.
    Each thread searches for different targets.

    This is often more efficient than parallelizing single searches.
    """
    results = [-1] * len(targets)

    def binary_search(target: int) -> Tuple[int, int]:
        """Binary search returning (target_index, found_position)"""
        left, right = 0, len(arr) - 1

        while left <= right:
            mid = left + (right - left) // 2
            if arr[mid] == target:
                return (targets.index(target), mid)
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return (targets.index(target), -1)

    # Search for all targets in parallel
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        search_results = executor.map(binary_search, targets)

    # Populate results
    for target_idx, position in search_results:
        results[target_idx] = position

    return results


def parallel_interpolation_search(arr: List[int], target: int, num_threads: int = 4) -> int:
    """
    Parallel interpolation search.
    Estimates likely position and searches nearby regions in parallel.

    Best for: Uniformly distributed large datasets
    """
    n = len(arr)
    if n == 0:
        return -1

    if target < arr[0] or target > arr[-1]:
        return -1

    # Estimate position
    ratio = (target - arr[0]) / (arr[-1] - arr[0])
    estimated_pos = int(ratio * (n - 1))

    # Search window around estimated position
    window_size = n // (num_threads * 2)
    result = [-1]
    lock = threading.Lock()

    def search_window(start: int, end: int):
        """Search in a window"""
        start = max(0, start)
        end = min(n - 1, end)

        for i in range(start, end + 1):
            if arr[i] == target:
                with lock:
                    result[0] = i
                return

    threads = []

    # Create windows around estimated position
    for i in range(num_threads):
        offset = (i - num_threads // 2) * window_size
        start = estimated_pos + offset
        end = start + window_size

        thread = threading.Thread(target=search_window, args=(start, end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # If not found in windows, fall back to binary search
    if result[0] == -1:
        left, right = 0, n - 1
        while left <= right:
            mid = left + (right - left) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

    return result[0]


def adaptive_parallel_search(arr: List[int], target: int) -> int:
    """
    Adaptively chooses between sequential and parallel search
    based on array size and system capabilities.
    """
    n = len(arr)

    # For small arrays, sequential is faster
    if n < 100000:
        left, right = 0, n - 1
        while left <= right:
            mid = left + (right - left) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    # For large arrays, use parallel
    num_cores = mp.cpu_count()
    optimal_threads = min(num_cores, 8)  # Cap at 8 for diminishing returns

    return parallel_binary_search_threads(arr, target, optimal_threads)


# Performance testing and demonstration
if __name__ == "__main__":
    import random

    print("=== Parallel Search Algorithm Demonstrations ===\n")

    # Test correctness
    test_arr = sorted(random.sample(range(1000), 100))
    target = random.choice(test_arr)

    print("1. Correctness Test")
    print(f"Array size: {len(test_arr)}")
    print(f"Target: {target}")
    print(f"Sequential result: {test_arr.index(target) if target in test_arr else -1}")
    print(f"Parallel threads result: {parallel_binary_search_threads(test_arr, target)}")
    print()

    # Batch search demonstration
    print("2. Batch Search (Multiple Targets)")
    targets = random.sample(test_arr, 10)
    batch_results = parallel_batch_search(test_arr, targets, num_threads=4)
    print(f"Searching for {len(targets)} targets in parallel")
    print(f"Results: {batch_results[:5]}... (showing first 5)")
    print()

    # Performance comparison
    print("3. Performance Comparison (Large Dataset)")
    sizes = [100000, 1000000, 10000000]

    for size in sizes:
        print(f"\nArray size: {size:,}")
        arr = list(range(0, size * 2, 2))
        target = random.choice(arr)

        # Sequential binary search
        start = time.perf_counter()
        for _ in range(100):
            left, right = 0, len(arr) - 1
            while left <= right:
                mid = left + (right - left) // 2
                if arr[mid] == target:
                    break
                elif arr[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
        seq_time = time.perf_counter() - start

        # Parallel binary search with threads
        start = time.perf_counter()
        for _ in range(100):
            parallel_binary_search_threads(arr, target, num_threads=4)
        parallel_time = time.perf_counter() - start

        print(f"Sequential: {seq_time*1000:.3f}ms")
        print(f"Parallel (4 threads): {parallel_time*1000:.3f}ms")
        print(f"Speedup: {seq_time/parallel_time:.2f}x")

        # Note: For single searches, overhead often exceeds benefit
        # Parallel search shines with batch operations

    # Batch search performance
    print("\n4. Batch Search Performance")
    arr = list(range(0, 10000000, 2))
    num_targets_list = [10, 100, 1000]

    for num_targets in num_targets_list:
        targets = [random.choice(arr) for _ in range(num_targets)]

        # Sequential
        start = time.perf_counter()
        seq_results = []
        for target in targets:
            left, right = 0, len(arr) - 1
            while left <= right:
                mid = left + (right - left) // 2
                if arr[mid] == target:
                    seq_results.append(mid)
                    break
                elif arr[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            else:
                seq_results.append(-1)
        seq_batch_time = time.perf_counter() - start

        # Parallel
        start = time.perf_counter()
        parallel_results = parallel_batch_search(arr, targets, num_threads=8)
        parallel_batch_time = time.perf_counter() - start

        print(f"\nSearching for {num_targets} targets:")
        print(f"Sequential: {seq_batch_time*1000:.3f}ms")
        print(f"Parallel (8 threads): {parallel_batch_time*1000:.3f}ms")
        print(f"Speedup: {seq_batch_time/parallel_batch_time:.2f}x")

    print("\n=== Key Takeaways ===")
    print("• Single searches: Parallel has overhead, often slower")
    print("• Batch searches: Parallel excels, near-linear speedup")
    print("• Large datasets (10M+): Parallel can help even for single searches")
    print("• Optimal thread count: Usually 4-8, diminishing returns after")
    print("• Best use case: Searching for many targets simultaneously")
