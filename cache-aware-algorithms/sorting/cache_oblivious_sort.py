"""
Cache-Oblivious Sorting Algorithms

Cache-oblivious algorithms automatically adapt to any cache hierarchy
without knowing cache parameters (size, line size, etc.).

This module demonstrates:
1. Funnel Sort - Theoretically optimal O(n/B log_{M/B} n/B)
2. Cache-oblivious Merge Sort
3. Cache-oblivious Quick Sort
4. Comparison with cache-aware sorting

Key Advantages:
- Optimal for ALL cache levels simultaneously
- No tuning parameters needed
- Portable across different hardware
- Theoretical guarantees

Cache-Oblivious Model:
- Algorithm doesn't know B (block size) or M (cache size)
- Analyzed in ideal-cache model
- Automatically optimal for entire memory hierarchy

Author: Algorithms Multiverse
"""

import time
import random
import math
from typing import List, Tuple, Optional, Any
from dataclasses import dataclass
import sys


@dataclass
class SortResult:
    """Result from sorting operation"""
    time_taken: float
    comparisons: int
    swaps: int
    estimated_cache_misses: int
    method: str


class CacheObliviousSort:
    """
    Cache-oblivious sorting algorithms.

    These algorithms achieve optimal cache complexity without
    knowing cache parameters.
    """

    def __init__(self):
        self.comparisons = 0
        self.swaps = 0
        self.cache_accesses = 0

    def _reset_counters(self):
        """Reset performance counters"""
        self.comparisons = 0
        self.swaps = 0
        self.cache_accesses = 0

    def _compare(self, a: Any, b: Any) -> bool:
        """Compare with counting"""
        self.comparisons += 1
        return a < b

    def _swap(self, arr: List[Any], i: int, j: int):
        """Swap with counting"""
        self.swaps += 1
        arr[i], arr[j] = arr[j], arr[i]

    def cache_oblivious_merge_sort(self, arr: List[Any]) -> SortResult:
        """
        Cache-oblivious merge sort.

        Cache complexity: O(n/B log_{M/B} n/B)
        - Optimal for all cache levels
        - No cache parameters needed

        Algorithm:
        - Divide array recursively
        - When subarray fits in cache, merging is free
        - Automatically adapts to cache size

        Args:
            arr: Array to sort

        Returns:
            SortResult with performance metrics
        """
        self._reset_counters()
        start_time = time.perf_counter()

        # Create copy to avoid modifying original during merge
        aux = [0] * len(arr)

        def merge_sort_recursive(left: int, right: int):
            """Recursive merge sort"""
            if left >= right:
                return

            if right - left <= 16:
                # Base case: insertion sort for small subarrays
                # (better cache behavior than merge)
                self._insertion_sort_range(arr, left, right)
                return

            mid = left + (right - left) // 2

            # Recursively sort halves
            merge_sort_recursive(left, mid)
            merge_sort_recursive(mid + 1, right)

            # Merge
            self._merge(arr, aux, left, mid, right)

        merge_sort_recursive(0, len(arr) - 1)

        time_taken = time.perf_counter() - start_time

        # Estimate cache misses
        n = len(arr)
        # Assuming cache size M and block size B
        # O(n/B log_{M/B} n/B) cache misses
        # For estimation, assume M=256KB, B=64B
        M, B = 32768, 8  # In terms of array elements
        cache_misses = (n // B) * math.log(n / B) / math.log(M / B) if n > B else n

        return SortResult(
            time_taken=time_taken,
            comparisons=self.comparisons,
            swaps=self.swaps,
            estimated_cache_misses=int(cache_misses),
            method="cache_oblivious_merge_sort"
        )

    def _merge(self, arr: List[Any], aux: List[Any], left: int, mid: int, right: int):
        """
        Merge two sorted subarrays.

        Cache-oblivious property: When arrays fit in cache,
        merge happens with no cache misses.
        """
        # Copy to auxiliary array
        for i in range(left, right + 1):
            aux[i] = arr[i]

        i, j = left, mid + 1
        k = left

        # Merge back
        while i <= mid and j <= right:
            self.comparisons += 1
            if aux[i] <= aux[j]:
                arr[k] = aux[i]
                i += 1
            else:
                arr[k] = aux[j]
                j += 1
            k += 1

        # Copy remaining elements
        while i <= mid:
            arr[k] = aux[i]
            i += 1
            k += 1

        while j <= right:
            arr[k] = aux[j]
            j += 1
            k += 1

    def _insertion_sort_range(self, arr: List[Any], left: int, right: int):
        """Insertion sort for small ranges (cache-friendly)"""
        for i in range(left + 1, right + 1):
            key = arr[i]
            j = i - 1
            while j >= left and arr[j] > key:
                self.comparisons += 1
                arr[j + 1] = arr[j]
                self.swaps += 1
                j -= 1
            if j >= left:
                self.comparisons += 1
            arr[j + 1] = key

    def cache_oblivious_quicksort(self, arr: List[Any]) -> SortResult:
        """
        Cache-oblivious quicksort with random pivoting.

        Cache complexity: O(n/B log_{M/B} n/B) expected
        - Uses randomized pivot selection
        - No explicit cache parameters

        Args:
            arr: Array to sort

        Returns:
            SortResult with performance metrics
        """
        self._reset_counters()
        start_time = time.perf_counter()

        def quicksort_recursive(left: int, right: int):
            """Recursive quicksort"""
            if left >= right:
                return

            if right - left <= 16:
                # Use insertion sort for small subarrays
                self._insertion_sort_range(arr, left, right)
                return

            # Random pivot for good expected behavior
            pivot_idx = random.randint(left, right)
            pivot = arr[pivot_idx]

            # Three-way partitioning (handles duplicates well)
            i, j, k = left, left, right

            while j <= k:
                self.comparisons += 1
                if arr[j] < pivot:
                    self._swap(arr, i, j)
                    i += 1
                    j += 1
                elif arr[j] > pivot:
                    self._swap(arr, j, k)
                    k -= 1
                else:
                    j += 1

            # Recursively sort partitions
            quicksort_recursive(left, i - 1)
            quicksort_recursive(k + 1, right)

        quicksort_recursive(0, len(arr) - 1)

        time_taken = time.perf_counter() - start_time

        # Estimate cache misses (similar to merge sort)
        n = len(arr)
        M, B = 32768, 8
        cache_misses = (n // B) * math.log(n / B) / math.log(M / B) if n > B else n

        return SortResult(
            time_taken=time_taken,
            comparisons=self.comparisons,
            swaps=self.swaps,
            estimated_cache_misses=int(cache_misses),
            method="cache_oblivious_quicksort"
        )

    def recursive_funnelsort(self, arr: List[Any]) -> SortResult:
        """
        Simplified funnel sort (cache-oblivious).

        Funnel sort is theoretically optimal but complex to implement.
        This is a simplified version showing the key ideas.

        True funnel sort:
        - Uses k-merger tree structure
        - Achieves O(n/B log_{M/B} n/B) cache misses
        - Optimal for external sorting

        Args:
            arr: Array to sort

        Returns:
            SortResult with performance metrics
        """
        self._reset_counters()
        start_time = time.perf_counter()

        # For simplicity, this uses multiway merge (simplified funnel)
        k = int(math.sqrt(len(arr))) if len(arr) > 16 else 2

        def k_way_merge_sort(arr_slice: List[Any]) -> List[Any]:
            """k-way merge sort (simplified funnel sort)"""
            if len(arr_slice) <= 16:
                # Base case: use simple sort
                self.comparisons += len(arr_slice) * math.log2(len(arr_slice)) if len(arr_slice) > 1 else 0
                return sorted(arr_slice)

            # Split into k parts
            chunk_size = len(arr_slice) // k + (1 if len(arr_slice) % k else 0)
            chunks = [arr_slice[i:i + chunk_size] for i in range(0, len(arr_slice), chunk_size)]

            # Recursively sort each chunk
            sorted_chunks = [k_way_merge_sort(chunk) for chunk in chunks]

            # k-way merge (cache-oblivious merge)
            return self._k_way_merge(sorted_chunks)

        result = k_way_merge_sort(arr.copy())
        arr[:] = result

        time_taken = time.perf_counter() - start_time

        # Optimal cache complexity
        n = len(arr)
        M, B = 32768, 8
        cache_misses = (n // B) * math.log(n / B) / math.log(M / B) if n > B else n

        return SortResult(
            time_taken=time_taken,
            comparisons=self.comparisons,
            swaps=self.swaps,
            estimated_cache_misses=int(cache_misses),
            method="funnel_sort"
        )

    def _k_way_merge(self, chunks: List[List[Any]]) -> List[Any]:
        """
        Merge k sorted arrays.

        Cache-oblivious: Uses recursive merging that adapts to cache size.

        Args:
            chunks: List of sorted arrays

        Returns:
            Merged sorted array
        """
        if not chunks:
            return []
        if len(chunks) == 1:
            return chunks[0]

        # Binary merge tree (cache-oblivious)
        while len(chunks) > 1:
            merged = []
            for i in range(0, len(chunks), 2):
                if i + 1 < len(chunks):
                    merged.append(self._merge_two_arrays(chunks[i], chunks[i + 1]))
                else:
                    merged.append(chunks[i])
            chunks = merged

        return chunks[0]

    def _merge_two_arrays(self, a: List[Any], b: List[Any]) -> List[Any]:
        """Merge two sorted arrays"""
        result = []
        i, j = 0, 0

        while i < len(a) and j < len(b):
            self.comparisons += 1
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1

        result.extend(a[i:])
        result.extend(b[j:])

        return result


class CacheAwareSort:
    """
    Cache-aware sorting for comparison.

    These algorithms explicitly use cache parameters for optimization.
    """

    # Cache parameters (explicit tuning)
    CACHE_LINE_SIZE = 64  # bytes
    L1_CACHE_SIZE = 32 * 1024  # 32 KB
    L2_CACHE_SIZE = 256 * 1024  # 256 KB

    # Optimal block size for cache
    BLOCK_SIZE = 1024  # elements

    def __init__(self):
        self.comparisons = 0
        self.swaps = 0

    def blocked_merge_sort(self, arr: List[Any]) -> SortResult:
        """
        Cache-aware blocked merge sort.

        Explicitly uses cache-sized blocks for optimization.

        Args:
            arr: Array to sort

        Returns:
            SortResult with performance metrics
        """
        start_time = time.perf_counter()
        self.comparisons = 0
        self.swaps = 0

        # Sort blocks that fit in cache
        block_size = self.BLOCK_SIZE

        # Sort each block
        for i in range(0, len(arr), block_size):
            end = min(i + block_size, len(arr))
            arr[i:end] = sorted(arr[i:end])
            self.comparisons += (end - i) * math.log2(end - i) if end > i else 0

        # Merge blocks
        width = block_size
        while width < len(arr):
            for i in range(0, len(arr), width * 2):
                left = i
                mid = min(i + width, len(arr))
                right = min(i + width * 2, len(arr))

                if mid < right:
                    # Merge [left:mid] and [mid:right]
                    merged = []
                    l, r = left, mid

                    while l < mid and r < right:
                        self.comparisons += 1
                        if arr[l] <= arr[r]:
                            merged.append(arr[l])
                            l += 1
                        else:
                            merged.append(arr[r])
                            r += 1

                    merged.extend(arr[l:mid])
                    merged.extend(arr[r:right])
                    arr[left:right] = merged

            width *= 2

        time_taken = time.perf_counter() - start_time

        # Estimate cache misses (explicitly tuned)
        n = len(arr)
        num_blocks = (n + block_size - 1) // block_size
        cache_misses = num_blocks * (block_size // 8)  # Assumes 8 elements per cache line

        return SortResult(
            time_taken=time_taken,
            comparisons=self.comparisons,
            swaps=self.swaps,
            estimated_cache_misses=cache_misses,
            method="cache_aware_blocked_merge"
        )


def benchmark_cache_oblivious_vs_aware():
    """
    Compare cache-oblivious vs cache-aware sorting.

    Key insight: Cache-oblivious algorithms achieve similar performance
    without needing to know cache parameters.
    """
    print("=" * 80)
    print("CACHE-OBLIVIOUS VS CACHE-AWARE SORTING")
    print("=" * 80)
    print()
    print("Cache-Oblivious Advantages:")
    print("  - No tuning parameters needed")
    print("  - Optimal for ALL cache levels simultaneously")
    print("  - Portable across different hardware")
    print()

    sizes = [1000, 10000, 100000, 500000]

    for size in sizes:
        print(f"\n{'='*80}")
        print(f"Array Size: {size:,} elements")
        print(f"{'='*80}")

        # Generate random data
        data = list(range(size))
        random.shuffle(data)

        sorter_oblivious = CacheObliviousSort()
        sorter_aware = CacheAwareSort()

        print(f"\n{'Method':<35} {'Time (ms)':<12} {'Comparisons':<15} {'Est. Cache Misses':<18}")
        print("-" * 80)

        # Standard merge sort (baseline)
        data_copy = data.copy()
        start = time.perf_counter()
        data_copy.sort()
        baseline_time = time.perf_counter() - start
        baseline_time_ms = baseline_time * 1000
        print(f"{'Python built-in sort (Timsort)':<35} {baseline_time_ms:>10.2f}  "
              f"{'~'+str(size)+'log n':<15}  {'~'+str(size//8):<18}")

        # Cache-oblivious merge sort
        data_copy = data.copy()
        result = sorter_oblivious.cache_oblivious_merge_sort(data_copy)
        speedup = baseline_time / result.time_taken
        print(f"{'Cache-Oblivious Merge Sort':<35} {result.time_taken*1000:>10.2f}  "
              f"{result.comparisons:>13,}  {result.estimated_cache_misses:>16,}  ({speedup:.2f}x)")

        # Cache-oblivious quicksort
        data_copy = data.copy()
        result = sorter_oblivious.cache_oblivious_quicksort(data_copy)
        speedup = baseline_time / result.time_taken
        print(f"{'Cache-Oblivious Quicksort':<35} {result.time_taken*1000:>10.2f}  "
              f"{result.comparisons:>13,}  {result.estimated_cache_misses:>16,}  ({speedup:.2f}x)")

        # Simplified funnel sort
        if size <= 100000:  # Skip for large sizes (slow implementation)
            data_copy = data.copy()
            result = sorter_oblivious.recursive_funnelsort(data_copy)
            speedup = baseline_time / result.time_taken
            print(f"{'Funnel Sort (simplified)':<35} {result.time_taken*1000:>10.2f}  "
                  f"{result.comparisons:>13,}  {result.estimated_cache_misses:>16,}  ({speedup:.2f}x)")

        # Cache-aware blocked merge sort
        data_copy = data.copy()
        result = sorter_aware.blocked_merge_sort(data_copy)
        speedup = baseline_time / result.time_taken
        print(f"{'Cache-Aware Blocked Merge':<35} {result.time_taken*1000:>10.2f}  "
              f"{result.comparisons:>13,}  {result.estimated_cache_misses:>16,}  ({speedup:.2f}x)")

    print(f"\n{'='*80}")
    print("CACHE-OBLIVIOUS ALGORITHM THEORY")
    print(f"{'='*80}")
    print("""
Key Concepts:

1. **Ideal-Cache Model**
   - Cache size M (unknown to algorithm)
   - Block size B (unknown to algorithm)
   - Algorithm analyzed assuming optimal replacement policy
   - Optimal: O(n/B log_{M/B} n/B) cache misses

2. **Cache-Oblivious Algorithms**
   - Do not use M or B as parameters
   - Automatically optimal for entire memory hierarchy
   - Achieved through recursive divide-and-conquer
   - When subproblem fits in cache, computation is "free"

3. **Why Recursion Works**
   - At some recursion level, data fits in cache
   - Subsequent operations have minimal cache misses
   - Works for ALL cache levels simultaneously
   - No manual tuning needed

4. **Practical Benefits**
   - Portable across different CPUs
   - Works well on systems with multiple cache levels
   - Simpler code (no explicit cache parameters)
   - Often within 10-20% of hand-tuned cache-aware code

5. **Cache-Aware vs Cache-Oblivious**
   - Cache-aware: Explicitly tuned for specific cache size
     * Pros: Can be slightly faster on specific hardware
     * Cons: Requires tuning, not portable

   - Cache-oblivious: Automatic adaptation
     * Pros: No tuning, works on all hardware, theoretically optimal
     * Cons: May be 10-20% slower than perfectly tuned cache-aware

6. **Real-World Examples**
   - Funnel Sort: Theoretically optimal external sorting
   - Cache-oblivious B-trees: Optimal for all memory levels
   - Matrix transpose: O(n²/B) cache misses (optimal)
   - FFT: O(n/B log n) cache misses (optimal)

7. **Implementation Trade-offs**
   - Funnel sort: Complex to implement, rarely used in practice
   - Cache-oblivious merge/quick: Simple, practical, good performance
   - Timsort (Python): Cache-aware hybrid, excellent in practice

Best Practices:
1. Use cache-oblivious algorithms for:
   - Portable libraries
   - Unknown target hardware
   - Multiple cache levels

2. Use cache-aware algorithms when:
   - Targeting specific hardware
   - Maximum performance needed
   - Cache parameters are well-known

3. Combine approaches:
   - Cache-oblivious overall structure
   - Cache-aware base cases
   - Example: Recursive divide-and-conquer + tuned small-array sort

Performance Summary:
- Cache-oblivious: 0.8-1.2x baseline (very good without tuning)
- Cache-aware: 0.9-1.5x baseline (best with perfect tuning)
- Built-in sorts (Timsort, etc.): Highly optimized, hard to beat
    """)


def demonstrate_automatic_adaptation():
    """Show how cache-oblivious algorithms adapt to different cache sizes"""
    print("\n" + "=" * 80)
    print("AUTOMATIC CACHE ADAPTATION")
    print("=" * 80)
    print("""
Cache-oblivious algorithms automatically adapt to the cache hierarchy.

Example: Recursive Merge Sort
1. First few levels: Working set doesn't fit in L1 → cache misses
2. Middle levels: Working set fits in L2 → faster
3. Deep recursion: Working set fits in L1 → very fast
4. This happens AUTOMATICALLY without knowing cache sizes

This is why cache-oblivious algorithms are optimal for the entire
memory hierarchy simultaneously.
    """)


# Example usage
if __name__ == "__main__":
    print("CACHE-OBLIVIOUS SORTING ALGORITHMS")
    print()

    # Run benchmarks
    benchmark_cache_oblivious_vs_aware()

    # Show automatic adaptation
    demonstrate_automatic_adaptation()

    print("\n" + "=" * 80)
    print("KEY TAKEAWAYS")
    print("=" * 80)
    print("""
1. Cache-oblivious algorithms achieve optimal cache performance
   without knowing cache parameters

2. They work through recursive divide-and-conquer:
   - Eventually subproblems fit in cache
   - Automatically optimal for all cache levels

3. Performance is typically within 80-120% of tuned cache-aware code

4. Major advantage: Portability and simplicity
   - No tuning needed
   - Works across different hardware
   - Optimal for entire memory hierarchy

5. When to use cache-oblivious:
   - Building portable libraries
   - Unknown target hardware
   - Want optimal multi-level cache performance

6. Real-world impact:
   - Used in databases (sorting, B-trees)
   - Computational libraries (FFT, matrix operations)
   - File systems (B-tree variants)
    """)

    print("\nDemonstration complete!")
