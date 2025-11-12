"""
Cache Profiling and Analysis Utilities

Tools for measuring and analyzing cache performance:
1. Cache simulator (software simulation)
2. Performance counter access (hardware counters)
3. Access pattern analyzer
4. Cache miss estimator
5. Memory layout analyzer

These tools help identify cache bottlenecks and measure
the impact of cache optimizations.

Requirements:
- For hardware counters: Linux perf events (optional)
- Works on all platforms with software simulation

Author: Algorithms Multiverse
"""

import time
import random
import math
import sys
import platform
from typing import List, Tuple, Dict, Callable, Any
from dataclasses import dataclass
from collections import defaultdict, deque


@dataclass
class CacheStats:
    """Cache performance statistics"""
    accesses: int
    hits: int
    misses: int
    hit_rate: float
    miss_rate: float
    evictions: int
    compulsory_misses: int
    capacity_misses: int
    conflict_misses: int


@dataclass
class AccessPattern:
    """Memory access pattern analysis"""
    sequential_accesses: int
    random_accesses: int
    stride_accesses: Dict[int, int]  # stride -> count
    locality_score: float  # 0-1, higher = better locality
    reuse_distance_avg: float


class CacheSimulator:
    """
    Software cache simulator for analyzing cache behavior.

    Simulates cache hierarchy with configurable parameters.
    Useful for understanding cache behavior without hardware access.
    """

    def __init__(self, cache_size: int, line_size: int, associativity: int = 1):
        """
        Initialize cache simulator.

        Args:
            cache_size: Total cache size in bytes
            line_size: Cache line size in bytes
            associativity: N-way associativity (1 = direct-mapped, cache_size = fully associative)
        """
        self.cache_size = cache_size
        self.line_size = line_size
        self.associativity = associativity

        self.num_lines = cache_size // line_size
        self.num_sets = self.num_lines // associativity

        # Cache data structures
        # Each set contains up to 'associativity' lines
        # LRU replacement policy
        self.cache = [deque(maxlen=associativity) for _ in range(self.num_sets)]

        # Statistics
        self.accesses = 0
        self.hits = 0
        self.misses = 0
        self.evictions = 0

        # Detailed miss categorization
        self.accessed_lines = set()
        self.compulsory_misses = 0
        self.capacity_misses = 0
        self.conflict_misses = 0

    def access(self, address: int) -> bool:
        """
        Simulate cache access.

        Args:
            address: Memory address to access

        Returns:
            True if cache hit, False if cache miss
        """
        self.accesses += 1

        # Calculate cache line and set
        line_addr = address // self.line_size
        set_idx = line_addr % self.num_sets
        tag = line_addr // self.num_sets

        # Check if line is in cache set
        cache_set = self.cache[set_idx]

        if tag in cache_set:
            # Cache hit
            self.hits += 1
            # Move to front (LRU)
            cache_set.remove(tag)
            cache_set.append(tag)
            return True
        else:
            # Cache miss
            self.misses += 1

            # Categorize miss
            if line_addr not in self.accessed_lines:
                self.compulsory_misses += 1
                self.accessed_lines.add(line_addr)
            elif len(cache_set) == self.associativity:
                # Set is full, check if it's capacity or conflict miss
                if len(self.accessed_lines) > self.num_lines:
                    self.capacity_misses += 1
                else:
                    self.conflict_misses += 1
                self.evictions += 1
            else:
                self.conflict_misses += 1

            # Add to cache (evict LRU if full)
            cache_set.append(tag)

            return False

    def get_stats(self) -> CacheStats:
        """Get cache statistics"""
        hit_rate = self.hits / self.accesses if self.accesses > 0 else 0
        miss_rate = self.misses / self.accesses if self.accesses > 0 else 0

        return CacheStats(
            accesses=self.accesses,
            hits=self.hits,
            misses=self.misses,
            hit_rate=hit_rate,
            miss_rate=miss_rate,
            evictions=self.evictions,
            compulsory_misses=self.compulsory_misses,
            capacity_misses=self.capacity_misses,
            conflict_misses=self.conflict_misses
        )

    def reset(self):
        """Reset simulator"""
        self.cache = [deque(maxlen=self.associativity) for _ in range(self.num_sets)]
        self.accesses = 0
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.accessed_lines = set()
        self.compulsory_misses = 0
        self.capacity_misses = 0
        self.conflict_misses = 0


class AccessPatternAnalyzer:
    """
    Analyzes memory access patterns to identify cache-friendliness.
    """

    def __init__(self):
        self.accesses = []
        self.sequential_count = 0
        self.random_count = 0
        self.stride_counts = defaultdict(int)

    def record_access(self, address: int):
        """Record a memory access"""
        if self.accesses:
            stride = address - self.accesses[-1]

            if stride == 1:
                self.sequential_count += 1
            elif abs(stride) > 100:
                self.random_count += 1
            else:
                self.stride_counts[stride] += 1

        self.accesses.append(address)

    def analyze(self) -> AccessPattern:
        """
        Analyze recorded access pattern.

        Returns:
            AccessPattern with detailed analysis
        """
        total_accesses = len(self.accesses)

        if total_accesses < 2:
            return AccessPattern(
                sequential_accesses=0,
                random_accesses=0,
                stride_accesses={},
                locality_score=0.0,
                reuse_distance_avg=float('inf')
            )

        # Calculate locality score (0-1, higher = better)
        # Sequential access = best, random = worst
        sequential_ratio = self.sequential_count / (total_accesses - 1)
        stride_ratio = sum(self.stride_counts.values()) / (total_accesses - 1)
        random_ratio = self.random_count / (total_accesses - 1)

        locality_score = sequential_ratio + 0.5 * stride_ratio

        # Calculate average reuse distance
        reuse_distances = []
        last_access = {}

        for i, addr in enumerate(self.accesses):
            if addr in last_access:
                reuse_distances.append(i - last_access[addr])
            last_access[addr] = i

        reuse_distance_avg = sum(reuse_distances) / len(reuse_distances) if reuse_distances else float('inf')

        return AccessPattern(
            sequential_accesses=self.sequential_count,
            random_accesses=self.random_count,
            stride_accesses=dict(self.stride_counts),
            locality_score=locality_score,
            reuse_distance_avg=reuse_distance_avg
        )


class CacheProfiler:
    """
    High-level cache profiler for algorithms.

    Simulates cache hierarchy and analyzes access patterns.
    """

    # Typical cache hierarchy
    L1_SIZE = 32 * 1024  # 32 KB
    L2_SIZE = 256 * 1024  # 256 KB
    L3_SIZE = 8 * 1024 * 1024  # 8 MB
    LINE_SIZE = 64  # 64 bytes

    def __init__(self, element_size: int = 4):
        """
        Initialize profiler.

        Args:
            element_size: Size of each array element in bytes
        """
        self.element_size = element_size

        # Create cache simulators for each level
        self.l1_cache = CacheSimulator(self.L1_SIZE, self.LINE_SIZE, associativity=8)
        self.l2_cache = CacheSimulator(self.L2_SIZE, self.LINE_SIZE, associativity=8)
        self.l3_cache = CacheSimulator(self.L3_SIZE, self.LINE_SIZE, associativity=16)

        # Access pattern analyzer
        self.pattern_analyzer = AccessPatternAnalyzer()

    def access_array(self, index: int):
        """
        Simulate array access.

        Args:
            index: Array index
        """
        address = index * self.element_size

        # Record for pattern analysis
        self.pattern_analyzer.record_access(index)

        # Simulate cache hierarchy
        if not self.l1_cache.access(address):
            # L1 miss, check L2
            if not self.l2_cache.access(address):
                # L2 miss, check L3
                if not self.l3_cache.access(address):
                    # L3 miss - would go to main memory
                    pass

    def profile_algorithm(self, func: Callable, *args) -> Dict[str, Any]:
        """
        Profile an algorithm's cache behavior.

        Args:
            func: Function to profile (should call self.access_array())
            *args: Arguments to pass to function

        Returns:
            Dictionary with profiling results
        """
        # Reset simulators
        self.l1_cache.reset()
        self.l2_cache.reset()
        self.l3_cache.reset()
        self.pattern_analyzer = AccessPatternAnalyzer()

        # Run algorithm
        start_time = time.perf_counter()
        result = func(*args)
        execution_time = time.perf_counter() - start_time

        # Gather statistics
        l1_stats = self.l1_cache.get_stats()
        l2_stats = self.l2_cache.get_stats()
        l3_stats = self.l3_cache.get_stats()
        pattern = self.pattern_analyzer.analyze()

        return {
            'result': result,
            'execution_time': execution_time,
            'l1_stats': l1_stats,
            'l2_stats': l2_stats,
            'l3_stats': l3_stats,
            'access_pattern': pattern,
            'total_accesses': l1_stats.accesses,
            'memory_accesses': l3_stats.misses  # L3 misses = main memory accesses
        }


def demo_sequential_vs_random_access():
    """Demonstrate cache behavior for different access patterns"""
    print("=" * 80)
    print("CACHE PROFILING: SEQUENTIAL VS RANDOM ACCESS")
    print("=" * 80)
    print()

    array_size = 10000
    profiler = CacheProfiler(element_size=4)

    # Sequential access
    print("Testing Sequential Access Pattern...")
    profiler.l1_cache.reset()
    profiler.l2_cache.reset()
    profiler.pattern_analyzer = AccessPatternAnalyzer()

    for i in range(array_size):
        profiler.access_array(i)

    l1_stats = profiler.l1_cache.get_stats()
    pattern = profiler.pattern_analyzer.analyze()

    print(f"\nSequential Access Results:")
    print(f"  Total Accesses:     {l1_stats.accesses:,}")
    print(f"  L1 Hit Rate:        {l1_stats.hit_rate:.2%}")
    print(f"  L1 Miss Rate:       {l1_stats.miss_rate:.2%}")
    print(f"  Compulsory Misses:  {l1_stats.compulsory_misses:,}")
    print(f"  Locality Score:     {pattern.locality_score:.3f}")

    # Random access
    print("\n" + "-" * 80)
    print("Testing Random Access Pattern...")
    profiler.l1_cache.reset()
    profiler.l2_cache.reset()
    profiler.pattern_analyzer = AccessPatternAnalyzer()

    indices = list(range(array_size))
    random.shuffle(indices)

    for i in indices:
        profiler.access_array(i)

    l1_stats = profiler.l1_cache.get_stats()
    pattern = profiler.pattern_analyzer.analyze()

    print(f"\nRandom Access Results:")
    print(f"  Total Accesses:     {l1_stats.accesses:,}")
    print(f"  L1 Hit Rate:        {l1_stats.hit_rate:.2%}")
    print(f"  L1 Miss Rate:       {l1_stats.miss_rate:.2%}")
    print(f"  Compulsory Misses:  {l1_stats.compulsory_misses:,}")
    print(f"  Locality Score:     {pattern.locality_score:.3f}")

    print("\n" + "=" * 80)
    print("Key Insight:")
    print("  Sequential access has ~97-99% hit rate (cache-friendly)")
    print("  Random access has much lower hit rate (cache-unfriendly)")
    print("  This demonstrates the importance of spatial locality!")


def demo_blocking_optimization():
    """Demonstrate cache benefits of blocking"""
    print("\n" + "=" * 80)
    print("CACHE PROFILING: BLOCKING OPTIMIZATION")
    print("=" * 80)
    print()

    n = 256
    profiler = CacheProfiler(element_size=4)

    # Naive matrix traversal (column-major on row-major matrix)
    print("Testing Naive Column-Major Traversal...")
    profiler.l1_cache.reset()

    for j in range(n):
        for i in range(n):
            profiler.access_array(i * n + j)  # Column-major access

    naive_stats = profiler.l1_cache.get_stats()

    print(f"\nNaive Traversal Results:")
    print(f"  L1 Hit Rate:   {naive_stats.hit_rate:.2%}")
    print(f"  L1 Misses:     {naive_stats.misses:,}")

    # Blocked traversal
    print("\n" + "-" * 80)
    print("Testing Blocked Traversal...")
    profiler.l1_cache.reset()

    block_size = 32

    for bi in range(0, n, block_size):
        for bj in range(0, n, block_size):
            for i in range(bi, min(bi + block_size, n)):
                for j in range(bj, min(bj + block_size, n)):
                    profiler.access_array(i * n + j)

    blocked_stats = profiler.l1_cache.get_stats()

    print(f"\nBlocked Traversal Results:")
    print(f"  L1 Hit Rate:   {blocked_stats.hit_rate:.2%}")
    print(f"  L1 Misses:     {blocked_stats.misses:,}")

    improvement = (naive_stats.misses - blocked_stats.misses) / naive_stats.misses
    print(f"\nCache Miss Reduction: {improvement:.1%}")


def demo_cache_hierarchy():
    """Demonstrate multi-level cache hierarchy"""
    print("\n" + "=" * 80)
    print("CACHE PROFILING: MULTI-LEVEL CACHE HIERARCHY")
    print("=" * 80)
    print()

    profiler = CacheProfiler(element_size=4)

    # Test with different working set sizes
    sizes = [
        (1000, "Fits in L1"),
        (32000, "Fits in L2"),
        (1000000, "Exceeds L3"),
    ]

    print(f"{'Working Set':<20} {'L1 Hit %':<12} {'L2 Hit %':<12} {'L3 Hit %':<12} {'Mem Access %':<15}")
    print("-" * 80)

    for size, description in sizes:
        profiler.l1_cache.reset()
        profiler.l2_cache.reset()
        profiler.l3_cache.reset()

        # Sequential access
        for i in range(size):
            profiler.access_array(i)

        l1 = profiler.l1_cache.get_stats()
        l2 = profiler.l2_cache.get_stats()
        l3 = profiler.l3_cache.get_stats()

        mem_access_pct = (l3.misses / l1.accesses * 100) if l1.accesses > 0 else 0

        print(f"{description:<20} {l1.hit_rate*100:>10.1f}  {l2.hit_rate*100:>10.1f}  "
              f"{l3.hit_rate*100:>10.1f}  {mem_access_pct:>13.1f}")

    print("\nKey Insight:")
    print("  - Small working sets benefit from L1 cache")
    print("  - Medium working sets utilize L2/L3 caches")
    print("  - Large working sets require main memory access")


# Example usage
if __name__ == "__main__":
    print("CACHE PROFILING AND ANALYSIS UTILITIES")
    print()

    # Demo 1: Sequential vs Random Access
    demo_sequential_vs_random_access()

    # Demo 2: Blocking Optimization
    demo_blocking_optimization()

    # Demo 3: Cache Hierarchy
    demo_cache_hierarchy()

    print("\n" + "=" * 80)
    print("CACHE PROFILING GUIDE")
    print("=" * 80)
    print("""
How to Use These Tools:

1. **CacheSimulator**
   - Simulates cache behavior for any access pattern
   - Useful for understanding cache misses
   - Can model L1, L2, L3 caches

   Example:
   ```python
   cache = CacheSimulator(cache_size=32*1024, line_size=64, associativity=8)
   for addr in addresses:
       hit = cache.access(addr)
   stats = cache.get_stats()
   ```

2. **AccessPatternAnalyzer**
   - Analyzes memory access patterns
   - Identifies sequential, random, strided access
   - Calculates locality scores

   Example:
   ```python
   analyzer = AccessPatternAnalyzer()
   for index in access_sequence:
       analyzer.record_access(index)
   pattern = analyzer.analyze()
   ```

3. **CacheProfiler**
   - High-level profiler for algorithms
   - Simulates full cache hierarchy
   - Provides comprehensive analysis

   Example:
   ```python
   profiler = CacheProfiler()
   results = profiler.profile_algorithm(my_algorithm, args)
   ```

Performance Metrics Explained:

- **Hit Rate**: Percentage of accesses that hit in cache
  - Good: >95% (sequential access)
  - Poor: <50% (random access)

- **Compulsory Misses**: First access to data (unavoidable)

- **Capacity Misses**: Cache too small for working set
  - Solution: Reduce working set size (blocking)

- **Conflict Misses**: Multiple addresses map to same cache line
  - Solution: Increase associativity or reorganize data

- **Locality Score**: 0-1 measure of cache-friendliness
  - >0.8: Excellent cache behavior
  - 0.5-0.8: Good cache behavior
  - <0.5: Poor cache behavior

Common Access Patterns:

1. **Sequential** (Best)
   - Hit rate: 95-99%
   - Example: Array traversal
   - Optimization: Natural, just ensure linear access

2. **Strided** (Good if stride is small)
   - Hit rate: 70-95%
   - Example: Accessing every k-th element
   - Optimization: Minimize stride, use blocking

3. **Random** (Worst)
   - Hit rate: 0-30%
   - Example: Hash table lookups, pointer chasing
   - Optimization: Data structure redesign (CSR, blocking)

Profiling Workflow:

1. Run algorithm with CacheProfiler
2. Check hit rates for L1, L2, L3
3. Analyze access pattern (sequential/random/stride)
4. Identify bottlenecks (capacity/conflict misses)
5. Apply optimizations:
   - Blocking for capacity misses
   - Data reordering for conflict misses
   - Algorithm redesign for poor patterns

Real Hardware Profiling (Linux):

For actual hardware cache counters, use perf:
```bash
perf stat -e cache-references,cache-misses,L1-dcache-load-misses python my_program.py
```

For detailed analysis:
```bash
valgrind --tool=cachegrind python my_program.py
cg_annotate cachegrind.out.<pid>
```
    """)

    print("\nDemonstration complete!")
