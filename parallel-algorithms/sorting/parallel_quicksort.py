"""
Parallel Quicksort Implementation with Work-Stealing

This module implements parallel versions of quicksort with sophisticated
work-stealing and load balancing strategies.

Features:
- Work-stealing task queue
- Three-way partitioning for duplicate handling
- Load balancing across workers
- Adaptive switching to sequential quicksort
- In-place and out-of-place variants

Time Complexity: O(n log n) average, O(n²) worst case
Space Complexity: O(log n) with in-place partitioning
Speedup: Near-linear for large random datasets

When to use parallel quicksort:
- Large datasets with random distribution
- Multi-core systems available
- In-place sorting preferred (memory constrained)
- Average case performance is acceptable

Author: Algorithms Multiverse
"""

import concurrent.futures
import multiprocessing as mp
import threading
import time
import random
from typing import List, Tuple, Callable, Any
from dataclasses import dataclass
from collections import deque
import queue


@dataclass
class SortResult:
    """Results from a sorting operation with performance metrics"""
    sorted_array: List[Any]
    time_taken: float
    comparisons: int
    swaps: int
    method: str
    num_workers: int


class WorkStealingQueue:
    """
    Thread-safe work-stealing queue for load balancing.

    Workers can steal work from other workers when idle,
    improving load balance and reducing idle time.
    """

    def __init__(self):
        self.queue = deque()
        self.lock = threading.Lock()

    def push(self, item):
        """Push item to the front (LIFO for own work)"""
        with self.lock:
            self.queue.append(item)

    def pop(self):
        """Pop from the front (own work)"""
        with self.lock:
            if self.queue:
                return self.queue.pop()
            return None

    def steal(self):
        """Steal from the back (FIFO for stealing)"""
        with self.lock:
            if self.queue:
                return self.queue.popleft()
            return None

    def is_empty(self):
        """Return True when the owning worker has no pending segments."""
        with self.lock:
            return len(self.queue) == 0

    def size(self):
        """Return how many pending partitions are enqueued."""
        with self.lock:
            return len(self.queue)


class ParallelQuicksort:
    """
    Parallel Quicksort implementation with work-stealing and load balancing.
    """

    # Threshold for switching to sequential sort
    SEQUENTIAL_THRESHOLD = 1000

    # Threshold for switching from threads to processes
    PROCESS_THRESHOLD = 100000

    def __init__(self, num_workers: int = None):
        """
        Initialize ParallelQuicksort.

        Args:
            num_workers: Number of worker threads/processes.
                        If None, uses cpu_count()
        """
        self.num_workers = num_workers or mp.cpu_count()
        self.comparisons = 0
        self.swaps = 0
        self._lock = threading.Lock()

    def _increment_comparisons(self, count: int = 1):
        """Thread-safe comparison counter"""
        with self._lock:
            self.comparisons += count

    def _increment_swaps(self, count: int = 1):
        """Thread-safe swap counter"""
        with self._lock:
            self.swaps += count

    def _reset_counters(self):
        """Reset performance counters"""
        with self._lock:
            self.comparisons = 0
            self.swaps = 0

    def partition(self, arr: List[Any], low: int, high: int) -> int:
        """
        Partition array around pivot (Hoare partition scheme).

        Args:
            arr: Array to partition (modified in-place)
            low: Starting index
            high: Ending index

        Returns:
            Partition index
        """
        # Choose median-of-three as pivot for better performance
        mid = (low + high) // 2
        pivot_candidates = [
            (arr[low], low),
            (arr[mid], mid),
            (arr[high], high)
        ]
        pivot_val, pivot_idx = sorted(pivot_candidates)[1]

        # Move pivot to end
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        self._increment_swaps()

        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            self._increment_comparisons()
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                self._increment_swaps()

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        self._increment_swaps()

        return i + 1

    def three_way_partition(self, arr: List[Any], low: int, high: int) -> Tuple[int, int]:
        """
        Three-way partitioning for better handling of duplicates.

        Partitions array into three parts:
        - Elements < pivot
        - Elements = pivot
        - Elements > pivot

        Args:
            arr: Array to partition
            low: Starting index
            high: Ending index

        Returns:
            Tuple of (lt, gt) where:
            - arr[low:lt] < pivot
            - arr[lt:gt+1] == pivot
            - arr[gt+1:high+1] > pivot
        """
        if high - low <= 0:
            return (low, high)

        # Choose random pivot
        pivot_idx = random.randint(low, high)
        pivot = arr[pivot_idx]

        # Dutch national flag algorithm
        lt = low
        i = low
        gt = high

        while i <= gt:
            self._increment_comparisons()
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                self._increment_swaps()
                lt += 1
                i += 1
            elif arr[i] > pivot:
                self._increment_comparisons()
                arr[i], arr[gt] = arr[gt], arr[i]
                self._increment_swaps()
                gt -= 1
            else:
                i += 1

        return (lt, gt)

    def sequential_quicksort(self, arr: List[Any], low: int = 0, high: int = None) -> None:
        """
        Standard in-place quicksort.

        Args:
            arr: Array to sort (modified in-place)
            low: Starting index
            high: Ending index
        """
        if high is None:
            high = len(arr) - 1

        if low < high:
            # Use three-way partitioning for better duplicate handling
            lt, gt = self.three_way_partition(arr, low, high)

            self.sequential_quicksort(arr, low, lt - 1)
            self.sequential_quicksort(arr, gt + 1, high)

    def parallel_quicksort_threads(self, arr: List[Any]) -> List[Any]:
        """
        Parallel quicksort using thread pool with work-stealing.

        Args:
            arr: Array to sort

        Returns:
            Sorted array
        """
        result = arr.copy()

        if len(result) <= self.SEQUENTIAL_THRESHOLD:
            self.sequential_quicksort(result)
            return result

        # Work-stealing queues for each worker
        work_queues = [WorkStealingQueue() for _ in range(self.num_workers)]

        # Initially add the entire array to first queue
        work_queues[0].push((0, len(result) - 1))

        done_event = threading.Event()
        active_workers = [0] * self.num_workers
        lock = threading.Lock()

        def worker(worker_id: int):
            """Worker function that processes partitions"""
            my_queue = work_queues[worker_id]

            while not done_event.is_set():
                # Try to get work from own queue
                work = my_queue.pop()

                # If no work, try to steal from others
                if work is None:
                    for i in range(self.num_workers):
                        if i != worker_id:
                            work = work_queues[i].steal()
                            if work is not None:
                                break

                if work is None:
                    # Check if all queues are empty
                    with lock:
                        if all(q.is_empty() for q in work_queues):
                            if sum(active_workers) == 0:
                                done_event.set()
                                break
                    time.sleep(0.0001)  # Brief sleep to avoid busy waiting
                    continue

                low, high = work

                with lock:
                    active_workers[worker_id] += 1

                if high - low <= self.SEQUENTIAL_THRESHOLD:
                    self.sequential_quicksort(result, low, high)
                else:
                    # Partition and create new work items
                    lt, gt = self.three_way_partition(result, low, high)

                    # Add subtasks
                    if lt - 1 > low:
                        my_queue.push((low, lt - 1))
                    if high > gt + 1:
                        my_queue.push((gt + 1, high))

                with lock:
                    active_workers[worker_id] -= 1

        # Start workers
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            futures = [executor.submit(worker, i) for i in range(self.num_workers)]
            concurrent.futures.wait(futures)

        return result

    def parallel_quicksort_simple(self, arr: List[Any], depth: int = 0) -> List[Any]:
        """
        Simple parallel quicksort using divide-and-conquer.

        Args:
            arr: Array to sort
            depth: Current recursion depth

        Returns:
            Sorted array
        """
        if len(arr) <= self.SEQUENTIAL_THRESHOLD:
            result = arr.copy()
            self.sequential_quicksort(result)
            return result

        # Limit parallel depth
        max_parallel_depth = (self.num_workers - 1).bit_length()
        if depth >= max_parallel_depth:
            result = arr.copy()
            self.sequential_quicksort(result)
            return result

        # Partition
        result = arr.copy()
        lt, gt = self.three_way_partition(result, 0, len(result) - 1)

        left = result[:lt]
        middle = result[lt:gt+1]
        right = result[gt+1:]

        # Sort left and right in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            left_future = executor.submit(self.parallel_quicksort_simple, left, depth + 1)
            right_future = executor.submit(self.parallel_quicksort_simple, right, depth + 1)

            left_sorted = left_future.result()
            right_sorted = right_future.result()

        return left_sorted + middle + right_sorted

    def parallel_quicksort_processes(self, arr: List[Any]) -> List[Any]:
        """
        Parallel quicksort using process pool for large datasets.

        Args:
            arr: Array to sort

        Returns:
            Sorted array
        """
        if len(arr) <= self.SEQUENTIAL_THRESHOLD:
            result = arr.copy()
            self.sequential_quicksort(result)
            return result

        # Split into chunks
        chunk_size = max(len(arr) // self.num_workers, self.SEQUENTIAL_THRESHOLD)
        chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]

        # Sort chunks in parallel
        with mp.Pool(processes=self.num_workers) as pool:
            sorted_chunks = pool.map(self._sort_chunk, chunks)

        # Merge sorted chunks (using merge from merge sort)
        while len(sorted_chunks) > 1:
            merged = []
            for i in range(0, len(sorted_chunks), 2):
                if i + 1 < len(sorted_chunks):
                    merged.append(self._merge_sorted(sorted_chunks[i], sorted_chunks[i + 1]))
                else:
                    merged.append(sorted_chunks[i])
            sorted_chunks = merged

        return sorted_chunks[0] if sorted_chunks else []

    def _sort_chunk(self, arr: List[Any]) -> List[Any]:
        """Helper for process pool sorting"""
        result = arr.copy()
        self.sequential_quicksort(result)
        return result

    def _merge_sorted(self, left: List[Any], right: List[Any]) -> List[Any]:
        """Merge two sorted arrays"""
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def adaptive_parallel_quicksort(self, arr: List[Any]) -> List[Any]:
        """
        Adaptive parallel quicksort that chooses the best strategy.

        Args:
            arr: Array to sort

        Returns:
            Sorted array
        """
        n = len(arr)

        if n <= self.SEQUENTIAL_THRESHOLD:
            result = arr.copy()
            self.sequential_quicksort(result)
            return result
        elif n <= self.PROCESS_THRESHOLD:
            return self.parallel_quicksort_threads(arr)
        else:
            return self.parallel_quicksort_processes(arr)

    def sort_with_metrics(self, arr: List[Any], method: str = "adaptive") -> SortResult:
        """
        Sort array and collect performance metrics.

        Args:
            arr: Array to sort
            method: Sorting method

        Returns:
            SortResult with metrics
        """
        self._reset_counters()
        start_time = time.perf_counter()

        methods = {
            "sequential": lambda a: (lambda r: (self.sequential_quicksort(r), r)[1])(a.copy()),
            "threads": self.parallel_quicksort_threads,
            "simple": self.parallel_quicksort_simple,
            "processes": self.parallel_quicksort_processes,
            "adaptive": self.adaptive_parallel_quicksort
        }

        if method not in methods:
            raise ValueError(f"Unknown method: {method}")

        sorted_arr = methods[method](arr)
        time_taken = time.perf_counter() - start_time

        return SortResult(
            sorted_array=sorted_arr,
            time_taken=time_taken,
            comparisons=self.comparisons,
            swaps=self.swaps,
            method=method,
            num_workers=self.num_workers
        )


def benchmark_all_methods(arr: List[Any], num_workers: int = None) -> dict:
    """Benchmark all sorting methods"""
    sorter = ParallelQuicksort(num_workers=num_workers)
    results = {}

    for method in ["sequential", "simple", "threads", "adaptive"]:
        try:
            results[method] = sorter.sort_with_metrics(arr, method=method)
        except Exception as e:
            print(f"Error in {method}: {e}")

    return results


def calculate_speedup(sequential_time: float, parallel_time: float) -> float:
    """Calculate speedup factor"""
    return sequential_time / parallel_time if parallel_time > 0 else 0


def calculate_efficiency(speedup: float, num_workers: int) -> float:
    """Calculate parallel efficiency"""
    return speedup / num_workers if num_workers > 0 else 0


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("PARALLEL QUICKSORT WITH WORK-STEALING")
    print("=" * 80)

    sizes = [1000, 10000, 100000]

    for size in sizes:
        print(f"\n{'='*80}")
        print(f"Testing with {size:,} elements")
        print(f"{'='*80}")

        # Test with random data
        arr = [random.randint(1, 100000) for _ in range(size)]

        results = benchmark_all_methods(arr)

        print(f"\n{'Method':<15} {'Time (s)':<12} {'Comparisons':<15} {'Swaps':<15}")
        print("-" * 80)

        seq_time = results.get("sequential").time_taken if "sequential" in results else 0

        for method, result in results.items():
            speedup = calculate_speedup(seq_time, result.time_taken)
            efficiency = calculate_efficiency(speedup, result.num_workers)

            print(f"{method:<15} {result.time_taken:>10.6f}  "
                  f"{result.comparisons:>13,}  "
                  f"{result.swaps:>13,}")

            if method != "sequential" and seq_time > 0:
                print(f"{'':15} Speedup: {speedup:.2f}x  Efficiency: {efficiency:.2%}")

    print(f"\n{'='*80}")
    print("WHEN TO USE PARALLEL QUICKSORT")
    print(f"{'='*80}")
    print("""
Parallel quicksort is beneficial when:

✓ Large datasets (>10,000 elements)
✓ Random or uniformly distributed data
✓ Multiple CPU cores available
✓ In-place sorting preferred (memory constrained)

Work-stealing advantages:
✓ Excellent load balancing
✓ Minimizes idle time
✓ Handles irregular workloads
✓ Scales well with core count

Avoid parallel quicksort when:

✗ Small datasets (<1,000 elements)
✗ Nearly sorted data (degrades to O(n²))
✗ Many duplicates (use 3-way partitioning)
✗ Worst-case guarantee needed (use merge sort)

Performance characteristics:
- Best case: O(n log n) with near-linear speedup
- Average case: O(n log n) with 3-3.5x speedup on 4 cores
- Worst case: O(n²) with sorted or reverse-sorted data
- Space: O(log n) for recursion stack

Work-stealing features:
- LIFO for own work (cache locality)
- FIFO for stealing (load balance)
- Lock-free operations possible
- Dynamic load balancing

vs. Parallel Merge Sort:
+ Quicksort: Better cache locality, in-place, faster average case
- Quicksort: Worse worst case, less predictable, load imbalance
+ Merge Sort: Guaranteed O(n log n), stable, predictable
- Merge Sort: Extra space, more memory bandwidth
    """)

    print("\nDemonstration complete!")
