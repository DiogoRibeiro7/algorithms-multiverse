"""
Las Vegas Algorithms Implementation
===================================

Implementation of various Las Vegas algorithms - randomized algorithms that
always produce correct results but have randomized running time.

Key Characteristics:
- Always correct output (when it terminates)
- Randomized running time
- Expected polynomial time complexity
- No false positives or false negatives

Algorithms Implemented:
- Randomized QuickSort
- Randomized QuickSelect
- Miller-Rabin Primality Test (Las Vegas variant)
- Randomized Binary Search Tree operations
- Las Vegas N-Queens solver
- Randomized Graph Algorithms (Min-Cut)
- Pollard's Rho for Integer Factorization

Author: Claude
Date: January 2026
"""

import random
import math
from typing import List, Optional, Tuple, Any, Set, Dict
from dataclasses import dataclass
from collections import defaultdict
import time


class RandomizedQuickSort:
    """
    Randomized QuickSort - Las Vegas sorting algorithm.

    Always produces correctly sorted output with randomized pivot selection
    for expected O(n log n) time complexity.
    """

    @staticmethod
    def sort(arr: List[int]) -> List[int]:
        """
        Sort array using randomized QuickSort.

        Args:
            arr: Array to sort

        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr

        # Random pivot selection (Las Vegas approach)
        pivot_idx = random.randint(0, len(arr) - 1)
        pivot = arr[pivot_idx]

        # Three-way partitioning for handling duplicates
        less = [x for i, x in enumerate(arr) if x < pivot]
        equal = [x for x in arr if x == pivot]
        greater = [x for i, x in enumerate(arr) if x > pivot]

        # Recursive sorting
        return (RandomizedQuickSort.sort(less) +
                equal +
                RandomizedQuickSort.sort(greater))

    @staticmethod
    def sort_with_stats(arr: List[int]) -> Tuple[List[int], Dict[str, Any]]:
        """
        Sort with performance statistics.

        Returns:
            Sorted array and statistics
        """
        stats = {
            'comparisons': 0,
            'swaps': 0,
            'recursive_calls': 0,
            'max_depth': 0
        }

        def sort_helper(arr: List[int], depth: int = 0) -> List[int]:
            stats['recursive_calls'] += 1
            stats['max_depth'] = max(stats['max_depth'], depth)

            if len(arr) <= 1:
                return arr

            pivot_idx = random.randint(0, len(arr) - 1)
            pivot = arr[pivot_idx]

            less, equal, greater = [], [], []
            for x in arr:
                stats['comparisons'] += 1
                if x < pivot:
                    less.append(x)
                elif x == pivot:
                    equal.append(x)
                else:
                    greater.append(x)

            return (sort_helper(less, depth + 1) +
                   equal +
                   sort_helper(greater, depth + 1))

        sorted_arr = sort_helper(arr[:])
        return sorted_arr, stats


class RandomizedSelect:
    """
    Randomized Selection Algorithm (QuickSelect).

    Finds the k-th smallest element in expected O(n) time.
    """

    @staticmethod
    def select(arr: List[int], k: int) -> Optional[int]:
        """
        Find k-th smallest element (1-indexed).

        Args:
            arr: Input array
            k: Position to find (1-indexed)

        Returns:
            k-th smallest element or None if k is invalid
        """
        if k < 1 or k > len(arr):
            return None

        return RandomizedSelect._select_helper(arr[:], k - 1)

    @staticmethod
    def _select_helper(arr: List[int], k: int) -> int:
        """Recursive helper for selection."""
        if len(arr) == 1:
            return arr[0]

        # Random pivot
        pivot_idx = random.randint(0, len(arr) - 1)
        pivot = arr[pivot_idx]

        # Partition
        less = [x for x in arr if x < pivot]
        equal = [x for x in arr if x == pivot]
        greater = [x for x in arr if x > pivot]

        if k < len(less):
            return RandomizedSelect._select_helper(less, k)
        elif k < len(less) + len(equal):
            return pivot
        else:
            return RandomizedSelect._select_helper(greater, k - len(less) - len(equal))

    @staticmethod
    def find_median(arr: List[int]) -> float:
        """Find median using randomized selection."""
        n = len(arr)
        if n == 0:
            return 0

        if n % 2 == 1:
            return RandomizedSelect.select(arr, (n + 1) // 2)
        else:
            lower = RandomizedSelect.select(arr, n // 2)
            upper = RandomizedSelect.select(arr, n // 2 + 1)
            return (lower + upper) / 2


class RandomizedNQueens:
    """
    Las Vegas algorithm for N-Queens problem.

    Uses randomization to find valid queen placements.
    Always returns a correct solution (or reports failure).
    """

    def __init__(self, n: int):
        """Initialize N-Queens solver."""
        self.n = n
        self.solutions_found = 0
        self.attempts = 0

    def solve(self, max_attempts: int = 1000) -> Optional[List[int]]:
        """
        Find a valid N-Queens solution using Las Vegas approach.

        Args:
            max_attempts: Maximum random attempts

        Returns:
            Valid queen positions or None
        """
        for attempt in range(max_attempts):
            self.attempts += 1
            solution = self._random_solve()
            if solution:
                self.solutions_found += 1
                return solution
        return None

    def _random_solve(self) -> Optional[List[int]]:
        """Try to find solution with random choices."""
        queens = []
        available_cols = list(range(self.n))

        for row in range(self.n):
            # Randomly shuffle available columns
            random.shuffle(available_cols)

            placed = False
            for col in available_cols[:]:
                if self._is_safe(queens, row, col):
                    queens.append(col)
                    available_cols.remove(col)
                    placed = True
                    break

            if not placed:
                return None  # Backtrack by returning None

        return queens if len(queens) == self.n else None

    def _is_safe(self, queens: List[int], row: int, col: int) -> bool:
        """Check if placing queen at (row, col) is safe."""
        for r, c in enumerate(queens):
            # Check column and diagonals
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True

    def solve_all(self, limit: int = 10) -> List[List[int]]:
        """Find multiple unique solutions."""
        solutions = set()
        attempts = 0
        max_attempts = limit * 1000

        while len(solutions) < limit and attempts < max_attempts:
            attempts += 1
            solution = self._random_solve()
            if solution:
                solutions.add(tuple(solution))

        return [list(sol) for sol in solutions]


class RandomizedMinCut:
    """
    Karger's Randomized Min-Cut Algorithm.

    Las Vegas algorithm for finding minimum cut in a graph.
    """

    @dataclass
    class Edge:
        """Edge in the graph."""
        u: int
        v: int
        weight: float = 1.0

    def __init__(self, vertices: int, edges: List[Edge]):
        """Initialize graph for min-cut."""
        self.vertices = vertices
        self.edges = edges

    def find_min_cut(self, iterations: int = None) -> Tuple[int, Set[int], Set[int]]:
        """
        Find minimum cut using Karger's algorithm.

        Args:
            iterations: Number of iterations (default: n^2 * log(n))

        Returns:
            (cut_size, partition1, partition2)
        """
        if iterations is None:
            iterations = int(self.vertices * self.vertices * math.log(self.vertices))

        min_cut = float('inf')
        best_partition = (set(), set())

        for _ in range(iterations):
            cut_size, partition = self._single_min_cut()
            if cut_size < min_cut:
                min_cut = cut_size
                best_partition = partition

        return min_cut, best_partition[0], best_partition[1]

    def _single_min_cut(self) -> Tuple[int, Tuple[Set[int], Set[int]]]:
        """Single iteration of Karger's algorithm."""
        # Create union-find structure
        parent = list(range(self.vertices))
        rank = [0] * self.vertices

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: int, y: int):
            px, py = find(x), find(y)
            if px == py:
                return
            if rank[px] < rank[py]:
                parent[px] = py
            elif rank[px] > rank[py]:
                parent[py] = px
            else:
                parent[py] = px
                rank[px] += 1

        # Randomly contract edges until 2 components remain
        edges_copy = self.edges[:]
        components = self.vertices

        while components > 2:
            # Random edge selection
            edge_idx = random.randint(0, len(edges_copy) - 1)
            edge = edges_copy[edge_idx]

            if find(edge.u) != find(edge.v):
                union(edge.u, edge.v)
                components -= 1

            # Remove self-loops
            edges_copy = [e for e in edges_copy
                         if find(e.u) != find(e.v)]

        # Count cut edges and create partitions
        cut_size = 0
        partition1, partition2 = set(), set()

        # Find representatives of the two components
        representatives = set()
        for v in range(self.vertices):
            representatives.add(find(v))

        rep_list = list(representatives)
        if len(rep_list) >= 2:
            rep1, rep2 = rep_list[0], rep_list[1]

            for v in range(self.vertices):
                if find(v) == rep1:
                    partition1.add(v)
                else:
                    partition2.add(v)

            # Count cut edges
            for edge in self.edges:
                if ((edge.u in partition1 and edge.v in partition2) or
                    (edge.u in partition2 and edge.v in partition1)):
                    cut_size += edge.weight

        return cut_size, (partition1, partition2)


class PollardsRho:
    """
    Pollard's Rho Algorithm for Integer Factorization.

    Las Vegas algorithm that finds a non-trivial factor.
    """

    @staticmethod
    def factorize(n: int) -> Optional[int]:
        """
        Find a non-trivial factor of n.

        Args:
            n: Number to factorize

        Returns:
            A factor of n or None
        """
        if n <= 1:
            return None
        if n <= 3:
            return n
        if n % 2 == 0:
            return 2

        # Pollard's rho with different random starts
        for _ in range(10):  # Try multiple times with different seeds
            factor = PollardsRho._rho_iteration(n)
            if factor and factor != n and factor != 1:
                return factor

        return None

    @staticmethod
    def _rho_iteration(n: int) -> Optional[int]:
        """Single iteration of Pollard's rho."""
        if n % 2 == 0:
            return 2

        # Random starting point and constant
        x = random.randint(2, n - 1)
        c = random.randint(1, n - 1)
        y = x
        d = 1

        # Floyd's cycle detection
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)

        return d if d != n else None

    @staticmethod
    def complete_factorization(n: int) -> List[int]:
        """Find complete prime factorization."""
        if n <= 1:
            return []

        factors = []
        remaining = n

        # Handle 2 separately
        while remaining % 2 == 0:
            factors.append(2)
            remaining //= 2

        # Find other factors
        while remaining > 1:
            if PollardsRho._is_prime_miller_rabin(remaining):
                factors.append(remaining)
                break

            factor = PollardsRho.factorize(remaining)
            if factor:
                factors.append(factor)
                remaining //= factor
            else:
                factors.append(remaining)
                break

        return sorted(factors)

    @staticmethod
    def _is_prime_miller_rabin(n: int, k: int = 5) -> bool:
        """Miller-Rabin primality test (Las Vegas variant)."""
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False

        # Write n-1 as 2^r * d
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        # Witness loop
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)

            if x == 1 or x == n - 1:
                continue

            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False

        return True


class RandomizedBST:
    """
    Randomized Binary Search Tree.

    Uses randomization for balanced tree operations.
    """

    class Node:
        """BST Node."""
        def __init__(self, key: int, value: Any = None):
            self.key = key
            self.value = value
            self.left = None
            self.right = None
            self.size = 1

    def __init__(self):
        """Initialize empty BST."""
        self.root = None

    def insert(self, key: int, value: Any = None):
        """Insert with randomized balancing."""
        self.root = self._insert_at_root_random(self.root, key, value)

    def _insert_at_root_random(self, node: Optional[Node], key: int, value: Any) -> Node:
        """Insert at root with probability 1/(n+1)."""
        if node is None:
            return RandomizedBST.Node(key, value)

        # Randomized decision
        if random.random() < 1 / (node.size + 1):
            return self._insert_at_root(node, key, value)

        # Standard BST insertion
        if key < node.key:
            node.left = self._insert_at_root_random(node.left, key, value)
        else:
            node.right = self._insert_at_root_random(node.right, key, value)

        node.size = 1 + self._size(node.left) + self._size(node.right)
        return node

    def _insert_at_root(self, node: Optional[Node], key: int, value: Any) -> Node:
        """Force insertion at root using rotations."""
        if node is None:
            return RandomizedBST.Node(key, value)

        if key < node.key:
            node.left = self._insert_at_root(node.left, key, value)
            return self._rotate_right(node)
        else:
            node.right = self._insert_at_root(node.right, key, value)
            return self._rotate_left(node)

    def _rotate_left(self, x: Node) -> Node:
        """Left rotation."""
        y = x.right
        x.right = y.left
        y.left = x
        x.size = 1 + self._size(x.left) + self._size(x.right)
        y.size = 1 + self._size(y.left) + self._size(y.right)
        return y

    def _rotate_right(self, y: Node) -> Node:
        """Right rotation."""
        x = y.left
        y.left = x.right
        x.right = y
        y.size = 1 + self._size(y.left) + self._size(y.right)
        x.size = 1 + self._size(x.left) + self._size(x.right)
        return x

    def _size(self, node: Optional[Node]) -> int:
        """Get subtree size."""
        return node.size if node else 0

    def search(self, key: int) -> Optional[Any]:
        """Search for key."""
        node = self.root
        while node:
            if key == node.key:
                return node.value
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None


def quicksort_example():
    """Example: Randomized QuickSort performance."""
    print("=" * 60)
    print("RANDOMIZED QUICKSORT - LAS VEGAS ALGORITHM")
    print("=" * 60)

    # Test different input patterns
    test_cases = [
        ("Random", [random.randint(1, 100) for _ in range(20)]),
        ("Sorted", list(range(20))),
        ("Reverse", list(range(20, 0, -1))),
        ("Many Duplicates", [1, 2, 3] * 7),
    ]

    for name, arr in test_cases:
        print(f"\n{name} Input: {arr[:10]}..." if len(arr) > 10 else f"\n{name} Input: {arr}")

        sorted_arr, stats = RandomizedQuickSort.sort_with_stats(arr)

        print(f"Sorted: {sorted_arr[:10]}..." if len(sorted_arr) > 10 else f"Sorted: {sorted_arr}")
        print(f"Statistics:")
        print(f"  Comparisons: {stats['comparisons']}")
        print(f"  Recursive calls: {stats['recursive_calls']}")
        print(f"  Max recursion depth: {stats['max_depth']}")

    # Performance comparison over multiple runs
    print("\n" + "-" * 40)
    print("Performance over 100 runs (n=100):")

    comparisons = []
    for _ in range(100):
        arr = [random.randint(1, 1000) for _ in range(100)]
        _, stats = RandomizedQuickSort.sort_with_stats(arr)
        comparisons.append(stats['comparisons'])

    print(f"Average comparisons: {sum(comparisons) / len(comparisons):.1f}")
    print(f"Min comparisons: {min(comparisons)}")
    print(f"Max comparisons: {max(comparisons)}")


def selection_example():
    """Example: Randomized selection algorithm."""
    print("\n" + "=" * 60)
    print("RANDOMIZED SELECT (QUICKSELECT)")
    print("=" * 60)

    arr = [random.randint(1, 100) for _ in range(20)]
    print(f"Array: {arr}")

    # Find various order statistics
    positions = [1, 5, 10, 15, 20]

    print("\nOrder Statistics:")
    for k in positions:
        result = RandomizedSelect.select(arr, k)
        print(f"  {k}-th smallest: {result}")

    # Verify correctness
    sorted_arr = sorted(arr)
    print(f"\nVerification (sorted): {sorted_arr}")

    # Find median
    median = RandomizedSelect.find_median(arr)
    print(f"\nMedian: {median}")


def n_queens_example():
    """Example: Las Vegas N-Queens solver."""
    print("\n" + "=" * 60)
    print("LAS VEGAS N-QUEENS SOLVER")
    print("=" * 60)

    for n in [4, 6, 8]:
        print(f"\nSolving {n}-Queens:")
        solver = RandomizedNQueens(n)

        # Find one solution
        start_time = time.time()
        solution = solver.solve()
        elapsed = time.time() - start_time

        if solution:
            print(f"Solution found in {solver.attempts} attempts ({elapsed*1000:.2f}ms)")

            # Display board
            board = [['.' for _ in range(n)] for _ in range(n)]
            for row, col in enumerate(solution):
                board[row][col] = 'Q'

            for row in board:
                print("  " + " ".join(row))
        else:
            print("No solution found")

        # Find multiple solutions
        print(f"\nFinding multiple solutions:")
        solver = RandomizedNQueens(n)
        solutions = solver.solve_all(limit=3)
        print(f"Found {len(solutions)} unique solutions")


def min_cut_example():
    """Example: Randomized min-cut algorithm."""
    print("\n" + "=" * 60)
    print("KARGER'S RANDOMIZED MIN-CUT")
    print("=" * 60)

    # Create a simple graph
    edges = [
        RandomizedMinCut.Edge(0, 1),
        RandomizedMinCut.Edge(0, 2),
        RandomizedMinCut.Edge(1, 2),
        RandomizedMinCut.Edge(1, 3),
        RandomizedMinCut.Edge(2, 3),
        RandomizedMinCut.Edge(2, 4),
        RandomizedMinCut.Edge(3, 4),
    ]

    print("Graph edges:")
    for edge in edges:
        print(f"  {edge.u} -- {edge.v}")

    # Find min-cut
    min_cut_algo = RandomizedMinCut(5, edges)
    cut_size, partition1, partition2 = min_cut_algo.find_min_cut(iterations=100)

    print(f"\nMin-cut size: {cut_size}")
    print(f"Partition 1: {sorted(partition1)}")
    print(f"Partition 2: {sorted(partition2)}")

    # Verify cut edges
    cut_edges = []
    for edge in edges:
        if ((edge.u in partition1 and edge.v in partition2) or
            (edge.u in partition2 and edge.v in partition1)):
            cut_edges.append(edge)

    print(f"Cut edges:")
    for edge in cut_edges:
        print(f"  {edge.u} -- {edge.v}")


def factorization_example():
    """Example: Pollard's Rho factorization."""
    print("\n" + "=" * 60)
    print("POLLARD'S RHO FACTORIZATION")
    print("=" * 60)

    test_numbers = [
        91,      # 7 × 13
        323,     # 17 × 19
        1001,    # 7 × 11 × 13
        8051,    # 83 × 97
        104729,  # Prime
    ]

    for n in test_numbers:
        print(f"\nFactoring {n}:")

        # Find single factor
        factor = PollardsRho.factorize(n)
        if factor and factor != 1 and factor != n:
            other = n // factor
            print(f"  Found factor: {factor}")
            print(f"  {n} = {factor} × {other}")
        else:
            print(f"  {n} is likely prime")

        # Complete factorization
        factors = PollardsRho.complete_factorization(n)
        print(f"  Complete factorization: {' × '.join(map(str, factors))}")


def performance_comparison():
    """Compare Las Vegas vs deterministic algorithms."""
    print("\n" + "=" * 60)
    print("LAS VEGAS VS DETERMINISTIC COMPARISON")
    print("=" * 60)

    # Compare sorting algorithms
    print("\nSorting Performance (n=1000):")
    arr = [random.randint(1, 10000) for _ in range(1000)]

    # Randomized QuickSort
    start = time.time()
    sorted_rand = RandomizedQuickSort.sort(arr[:])
    time_rand = time.time() - start

    # Python's built-in sort (Timsort - deterministic)
    start = time.time()
    sorted_det = sorted(arr[:])
    time_det = time.time() - start

    print(f"Randomized QuickSort: {time_rand*1000:.2f}ms")
    print(f"Deterministic Sort:   {time_det*1000:.2f}ms")
    print(f"Results identical: {sorted_rand == sorted_det}")

    # Compare selection algorithms
    print("\nSelection Performance (finding median, n=10000):")
    arr = [random.randint(1, 100000) for _ in range(10000)]

    # Randomized select
    start = time.time()
    median_rand = RandomizedSelect.find_median(arr)
    time_rand = time.time() - start

    # Deterministic (sort and pick)
    start = time.time()
    sorted_arr = sorted(arr)
    median_det = sorted_arr[len(arr)//2] if len(arr) % 2 == 1 else \
                 (sorted_arr[len(arr)//2-1] + sorted_arr[len(arr)//2]) / 2
    time_det = time.time() - start

    print(f"Randomized Select: {time_rand*1000:.2f}ms")
    print(f"Deterministic:     {time_det*1000:.2f}ms")
    print(f"Results match: {abs(median_rand - median_det) < 0.001}")


if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)

    # Run examples
    quicksort_example()
    selection_example()
    n_queens_example()
    min_cut_example()
    factorization_example()
    performance_comparison()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Las Vegas algorithms always produce correct results")
    print("- Running time is randomized, correctness is guaranteed")
    print("- Often achieve better expected performance than deterministic")
    print("- No false positives or false negatives")
    print("- Useful when worst-case must be avoided probabilistically")
    print("=" * 60)