"""
Comprehensive Test Suite for All Advanced Search Algorithms

This file demonstrates and tests all implemented search algorithms
with various data types and distributions.
"""

import random
import time
from typing import List, Callable
import sys

# Import all search algorithm implementations
from jump_search import jump_search, jump_search_optimized
from fibonacci_search import fibonacci_search, fibonacci_search_optimized
from sublinear_search import (
    interpolation_search,
    exponential_search,
    adaptive_search
)
from parallel_search import (
    parallel_binary_search_threads,
    parallel_batch_search
)
from fuzzy_search import (
    levenshtein_distance,
    jaro_winkler_distance,
    fuzzy_search_in_array
)
from kdtree_search import KDTree


class SearchAlgorithmTester:
    """Comprehensive tester for search algorithms"""

    def __init__(self):
        self.results = {}

    def test_correctness(self):
        """Test correctness of all algorithms"""
        print("="*70)
        print("CORRECTNESS TESTS")
        print("="*70)

        # Test array
        arr = sorted(random.sample(range(1000), 100))
        target = arr[50]  # Guaranteed to exist
        missing = 1001  # Guaranteed not to exist

        tests = {
            "Jump Search": lambda: jump_search(arr, target),
            "Fibonacci Search": lambda: fibonacci_search(arr, target),
            "Interpolation Search": lambda: interpolation_search(arr, target),
            "Exponential Search": lambda: exponential_search(arr, target),
            "Adaptive Search": lambda: adaptive_search(arr, target),
        }

        print(f"\nTest Array Size: {len(arr)}")
        print(f"Target Value: {target} (should be found)")
        print(f"Missing Value: {missing} (should return -1)\n")

        all_passed = True
        for name, func in tests.items():
            try:
                result_found = func()
                result_missing = jump_search(arr, missing)

                found_correct = result_found >= 0 and arr[result_found] == target
                missing_correct = result_missing == -1

                status = "✓ PASS" if (found_correct and missing_correct) else "✗ FAIL"
                print(f"{name:25s}: {status}")

                if not (found_correct and missing_correct):
                    all_passed = False
                    print(f"  Expected found at valid index, got: {result_found}")
                    print(f"  Expected -1 for missing, got: {result_missing}")

            except Exception as e:
                print(f"{name:25s}: ✗ FAIL (Exception: {e})")
                all_passed = False

        print(f"\n{'='*70}")
        print(f"Overall: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")
        print(f"{'='*70}\n")

    def benchmark_algorithms(self, arr_size: int = 100000):
        """Benchmark all algorithms"""
        print("="*70)
        print(f"PERFORMANCE BENCHMARK - Array Size: {arr_size:,}")
        print("="*70)

        # Generate test data
        arr = list(range(0, arr_size * 2, 2))  # Uniform distribution
        target = arr[arr_size // 2]  # Middle element

        algorithms = {
            "Binary Search (baseline)": lambda: self._binary_search(arr, target),
            "Jump Search": lambda: jump_search(arr, target),
            "Fibonacci Search": lambda: fibonacci_search(arr, target),
            "Interpolation Search": lambda: interpolation_search(arr, target),
            "Exponential Search": lambda: exponential_search(arr, target),
            "Adaptive Search": lambda: adaptive_search(arr, target),
        }

        iterations = 1000
        results = []

        print(f"\nRunning {iterations} iterations for each algorithm...\n")

        # Baseline binary search time
        baseline_time = None

        for name, func in algorithms.items():
            # Warm-up
            for _ in range(10):
                func()

            # Benchmark
            start = time.perf_counter()
            for _ in range(iterations):
                func()
            elapsed = time.perf_counter() - start

            if baseline_time is None:
                baseline_time = elapsed

            ratio = elapsed / baseline_time
            results.append((name, elapsed * 1000, ratio))

        # Print results
        print(f"{'Algorithm':<30s} {'Time (ms)':<12s} {'vs Binary':<10s}")
        print("-" * 70)

        for name, time_ms, ratio in results:
            print(f"{name:<30s} {time_ms:>10.3f} ms   {ratio:>6.2f}x")

        print()

    def test_data_distributions(self):
        """Test algorithms on different data distributions"""
        print("="*70)
        print("PERFORMANCE ON DIFFERENT DATA DISTRIBUTIONS")
        print("="*70)

        distributions = {
            "Uniform": list(range(0, 100000, 10)),
            "Clustered": [i // 100 * 1000 for i in range(10000)],
            "Random": sorted(random.sample(range(1000000), 10000)),
            "Power Law": sorted([int(random.random() ** 3 * 100000) for _ in range(10000)])
        }

        algorithms = {
            "Binary": self._binary_search,
            "Interpolation": interpolation_search,
            "Fibonacci": fibonacci_search,
        }

        print()
        for dist_name, arr in distributions.items():
            print(f"\n{dist_name} Distribution (n={len(arr):,}):")
            print("-" * 70)

            target = arr[len(arr) // 2]

            for algo_name, algo_func in algorithms.items():
                start = time.perf_counter()
                for _ in range(1000):
                    algo_func(arr, target)
                elapsed = time.perf_counter() - start

                print(f"  {algo_name:20s}: {elapsed*1000:>8.3f} ms")

    def test_fuzzy_search(self):
        """Test fuzzy string matching algorithms"""
        print("\n" + "="*70)
        print("FUZZY STRING MATCHING TESTS")
        print("="*70)

        # Levenshtein distance tests
        print("\n1. Levenshtein Distance (Edit Distance):")
        print("-" * 70)
        test_pairs = [
            ("kitten", "sitting"),
            ("saturday", "sunday"),
            ("algorithm", "algorythm"),
            ("python", "pithon"),
        ]

        for s1, s2 in test_pairs:
            dist = levenshtein_distance(s1, s2)
            print(f"  '{s1}' → '{s2}': {dist} edits")

        # Jaro-Winkler similarity tests
        print("\n2. Jaro-Winkler Similarity (Good for names):")
        print("-" * 70)
        name_pairs = [
            ("Martha", "Marhta"),
            ("Dwayne", "Duane"),
            ("DIXON", "DICKSON"),
        ]

        for s1, s2 in name_pairs:
            similarity = jaro_winkler_distance(s1, s2)
            print(f"  '{s1}' vs '{s2}': {similarity:.3f}")

        # Fuzzy search in array
        print("\n3. Fuzzy Search in Array:")
        print("-" * 70)
        dictionary = sorted([
            "algorithm", "python", "search", "binary",
            "interpolation", "fibonacci", "fuzzy"
        ])

        query = "algoritm"  # Typo
        matches = fuzzy_search_in_array(dictionary, query, max_distance=2)
        print(f"  Searching for '{query}' (typo):")
        for idx, word, dist in matches:
            print(f"    Found '{word}' at index {idx}, distance {dist}")

    def test_kdtree(self):
        """Test KD-Tree spatial search"""
        print("\n" + "="*70)
        print("KD-TREE SPATIAL SEARCH TESTS")
        print("="*70)

        # 2D test
        print("\n1. 2D Point Search:")
        print("-" * 70)
        points_2d = [
            [2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]
        ]
        tree_2d = KDTree(points_2d, k=2)

        query = [6, 3]
        nearest, dist = tree_2d.nearest_neighbor(query)
        print(f"  Query point: {query}")
        print(f"  Nearest neighbor: {nearest} at distance {dist:.2f}")

        # K-nearest neighbors
        k = 3
        k_nearest = tree_2d.k_nearest_neighbors(query, k)
        print(f"\n  {k} nearest neighbors:")
        for i, (point, distance) in enumerate(k_nearest, 1):
            print(f"    {i}. {point} at distance {distance:.2f}")

        # Range search
        print("\n2. Range Search:")
        print("-" * 70)
        lower = [3, 2]
        upper = [8, 6]
        in_range = tree_2d.range_search(lower, upper)
        print(f"  Range: [{lower}, {upper}]")
        print(f"  Points in range: {in_range}")

        # Performance test
        print("\n3. KD-Tree Performance (vs Linear Scan):")
        print("-" * 70)

        for size in [1000, 10000]:
            points = [[random.uniform(0, 1000) for _ in range(3)] for _ in range(size)]
            tree = KDTree(points, k=3)
            query = [500, 500, 500]

            # KD-Tree search
            start = time.perf_counter()
            for _ in range(100):
                tree.nearest_neighbor(query)
            kd_time = time.perf_counter() - start

            # Linear scan
            start = time.perf_counter()
            for _ in range(100):
                best_dist = float('inf')
                for point in points:
                    dist = sum((a - b) ** 2 for a, b in zip(point, query))
                    if dist < best_dist:
                        best_dist = dist
            linear_time = time.perf_counter() - start

            speedup = linear_time / kd_time
            print(f"  Size {size:5d}: KD-Tree={kd_time*1000:6.2f}ms, "
                  f"Linear={linear_time*1000:7.2f}ms, Speedup={speedup:5.1f}x")

    def test_parallel_search(self):
        """Test parallel search algorithms"""
        print("\n" + "="*70)
        print("PARALLEL SEARCH TESTS")
        print("="*70)

        arr = list(range(0, 1000000, 2))

        # Batch search test
        print("\n1. Batch Search Performance:")
        print("-" * 70)

        for num_targets in [10, 100, 1000]:
            targets = [random.choice(arr) for _ in range(num_targets)]

            # Sequential
            start = time.perf_counter()
            seq_results = []
            for target in targets:
                idx = self._binary_search(arr, target)
                seq_results.append(idx)
            seq_time = time.perf_counter() - start

            # Parallel
            start = time.perf_counter()
            par_results = parallel_batch_search(arr, targets, num_threads=4)
            par_time = time.perf_counter() - start

            speedup = seq_time / par_time
            print(f"  {num_targets:4d} targets: Sequential={seq_time*1000:6.2f}ms, "
                  f"Parallel={par_time*1000:6.2f}ms, Speedup={speedup:4.2f}x")

    def _binary_search(self, arr: List[int], target: int) -> int:
        """Standard binary search for comparison"""
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

    def run_all_tests(self):
        """Run all test suites"""
        print("\n" + "="*70)
        print("  ADVANCED SEARCH ALGORITHMS - COMPREHENSIVE TEST SUITE")
        print("="*70)

        self.test_correctness()
        self.benchmark_algorithms()
        self.test_data_distributions()
        self.test_fuzzy_search()
        self.test_kdtree()
        self.test_parallel_search()

        print("\n" + "="*70)
        print("  ALL TESTS COMPLETED")
        print("="*70 + "\n")


if __name__ == "__main__":
    tester = SearchAlgorithmTester()
    tester.run_all_tests()
