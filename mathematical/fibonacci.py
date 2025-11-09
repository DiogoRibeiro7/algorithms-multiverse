"""
Fibonacci Sequence Implementation in Multiple Languages
======================================================

Time Complexity:
- Recursive: O(2^n)
- Dynamic Programming: O(n)
- Matrix Exponentiation: O(log n)

Space Complexity:
- Recursive: O(n) call stack
- Iterative: O(1)
- Memoized: O(n)

This file demonstrates the Fibonacci sequence implementation
across multiple programming languages.
"""

# ============= PYTHON IMPLEMENTATION =============

from typing import List, Dict
import time
from functools import lru_cache
import numpy as np


def fibonacci_recursive(n: int) -> int:
    """
    Simple recursive implementation (inefficient).
    Time: O(2^n), Space: O(n)
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n: int) -> int:
    """
    Iterative implementation (efficient).
    Time: O(n), Space: O(1)
    """
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


@lru_cache(maxsize=None)
def fibonacci_memoized(n: int) -> int:
    """
    Memoized recursive implementation.
    Time: O(n), Space: O(n)
    """
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)


def fibonacci_dp_bottom_up(n: int) -> int:
    """
    Dynamic programming bottom-up approach.
    Time: O(n), Space: O(n)
    """
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


def fibonacci_matrix(n: int) -> int:
    """
    Matrix exponentiation approach.
    Time: O(log n), Space: O(log n)
    """
    if n <= 1:
        return n

    def matrix_multiply(A, B):
        return [
            [
                A[0][0] * B[0][0] + A[0][1] * B[1][0],
                A[0][0] * B[0][1] + A[0][1] * B[1][1],
            ],
            [
                A[1][0] * B[0][0] + A[1][1] * B[1][0],
                A[1][0] * B[0][1] + A[1][1] * B[1][1],
            ],
        ]

    def matrix_power(mat, power):
        if power == 1:
            return mat
        if power % 2 == 0:
            half = matrix_power(mat, power // 2)
            return matrix_multiply(half, half)
        else:
            return matrix_multiply(mat, matrix_power(mat, power - 1))

    base_matrix = [[1, 1], [1, 0]]
    result_matrix = matrix_power(base_matrix, n)
    return result_matrix[0][1]


def fibonacci_golden_ratio(n: int) -> int:
    """
    Golden ratio formula (Binet's formula).
    Time: O(1), Space: O(1)
    Note: Limited by floating point precision
    """
    if n <= 1:
        return n

    phi = (1 + 5**0.5) / 2
    psi = (1 - 5**0.5) / 2

    return int((phi**n - psi**n) / 5**0.5 + 0.5)


def fibonacci_sequence(n: int) -> List[int]:
    """Generate first n Fibonacci numbers."""
    if n <= 0:
        return []
    if n == 1:
        return [0]

    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i - 1] + sequence[i - 2])

    return sequence


def fibonacci_generator():
    """Infinite Fibonacci generator."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


class FibonacciCalculator:
    """Class-based Fibonacci calculator with multiple methods."""

    def __init__(self):
        self.cache: Dict[int, int] = {0: 0, 1: 1}

    def calculate(self, n: int, method: str = "iterative") -> int:
        """Calculate Fibonacci number using specified method."""
        methods = {
            "recursive": fibonacci_recursive,
            "iterative": fibonacci_iterative,
            "memoized": fibonacci_memoized,
            "dp": fibonacci_dp_bottom_up,
            "matrix": fibonacci_matrix,
            "golden_ratio": fibonacci_golden_ratio,
            "cached": self._cached_fibonacci,
        }

        if method not in methods:
            raise ValueError(f"Unknown method: {method}")

        return methods[method](n)

    def _cached_fibonacci(self, n: int) -> int:
        """Instance-based caching."""
        if n in self.cache:
            return self.cache[n]

        self.cache[n] = self._cached_fibonacci(n - 1) + self._cached_fibonacci(n - 2)
        return self.cache[n]

    def benchmark_methods(self, n: int) -> Dict[str, float]:
        """Benchmark different methods."""
        methods = ["iterative", "memoized", "dp", "matrix", "golden_ratio"]
        if n <= 35:  # Avoid long recursive times
            methods.append("recursive")

        results = {}
        for method in methods:
            start_time = time.perf_counter()
            try:
                self.calculate(n, method)
                end_time = time.perf_counter()
                results[method] = end_time - start_time
            except Exception as e:
                results[method] = float("inf")  # Error case

        return results


def is_fibonacci_number(num: int) -> bool:
    """Check if a number is a Fibonacci number."""

    def is_perfect_square(x):
        if x < 0:
            return False
        root = int(x**0.5)
        return root * root == x

    # A number is Fibonacci if one or both of (5*n^2 + 4) or (5*n^2 - 4) is a perfect square
    return is_perfect_square(5 * num * num + 4) or is_perfect_square(5 * num * num - 4)


def find_fibonacci_index(target: int) -> int:
    """Find the index of a Fibonacci number."""
    if target < 0:
        return -1

    a, b, index = 0, 1, 0
    while a < target:
        if a == target:
            return index
        a, b = b, a + b
        index += 1

    return -1 if a != target else index


def fibonacci_sum(n: int) -> int:
    """Sum of first n Fibonacci numbers."""
    if n <= 0:
        return 0

    # Sum of first n Fibonacci numbers = F(n+2) - 1
    return fibonacci_iterative(n + 1) - 1


def demonstrate_fibonacci():
    """Demonstrate various Fibonacci implementations."""
    print("🔢 Fibonacci Sequence Implementation in Python")
    print("=" * 50)

    # Test different methods
    test_cases = [0, 1, 5, 10, 20, 30]
    print("\n📋 Method Comparison:")
    print(
        "n".rjust(3),
        "Recursive".rjust(12),
        "Iterative".rjust(12),
        "Memoized".rjust(12),
        "Matrix".rjust(12),
        "Golden".rjust(12),
    )
    print("-" * 65)

    for n in test_cases:
        results = []

        # Only test recursive for small values
        if n <= 30:
            results.append(f"{fibonacci_recursive(n)}")
        else:
            results.append("Too slow")

        results.extend(
            [
                f"{fibonacci_iterative(n)}",
                f"{fibonacci_memoized(n)}",
                f"{fibonacci_matrix(n)}",
                f"{fibonacci_golden_ratio(n)}",
            ]
        )

        print(f"{n:3d}", *[r.rjust(12) for r in results])

    # Fibonacci sequence
    print(f"\n🔢 First 20 Fibonacci numbers:")
    sequence = fibonacci_sequence(20)
    print(" ".join(f"{x:3d}" for x in sequence))

    # Using generator
    print(f"\n🔄 Using Generator (first 15):")
    fib_gen = fibonacci_generator()
    first_15 = [next(fib_gen) for _ in range(15)]
    print(" ".join(f"{x:3d}" for x in first_15))

    # Fibonacci number validation
    print(f"\n✅ Fibonacci Number Validation:")
    test_numbers = [0, 1, 2, 3, 4, 5, 8, 13, 21, 22, 34, 55, 89, 90]
    for num in test_numbers:
        is_fib = is_fibonacci_number(num)
        index = find_fibonacci_index(num) if is_fib else -1
        print(
            f"{num:3d}: {'✓' if is_fib else '✗'} "
            f"{'(F(' + str(index) + '))' if index >= 0 else ''}"
        )

    # Properties and patterns
    print(f"\n📊 Fibonacci Properties:")
    n = 10
    sequence = fibonacci_sequence(n)
    print(f"First {n} Fibonacci numbers: {sequence}")
    print(f"Sum of first {n} numbers: {fibonacci_sum(n)}")
    print(
        f"Golden ratio approximation (F(n)/F(n-1)): {sequence[-1] / sequence[-2]:.6f}"
    )
    print(f"Actual golden ratio: {(1 + 5**0.5) / 2:.6f}")


def performance_benchmark():
    """Benchmark different Fibonacci implementations."""
    print(f"\n⚡ Performance Benchmark")
    print("=" * 30)

    calculator = FibonacciCalculator()
    test_values = [20, 30, 100, 500, 1000]

    print(
        "n".rjust(6),
        "Iterative".rjust(12),
        "Memoized".rjust(12),
        "Matrix".rjust(12),
        "Golden".rjust(12),
    )
    print("-" * 54)

    for n in test_values:
        benchmarks = calculator.benchmark_methods(n)

        results = [
            f"{benchmarks.get('iterative', float('inf')):.6f}",
            f"{benchmarks.get('memoized', float('inf')):.6f}",
            f"{benchmarks.get('matrix', float('inf')):.6f}",
            f"{benchmarks.get('golden_ratio', float('inf')):.6f}",
        ]

        print(f"{n:6d}", *[r.rjust(12) for r in results])


if __name__ == "__main__":
    demonstrate_fibonacci()
    performance_benchmark()

    print("\n✨ Fibonacci demonstration complete!")
