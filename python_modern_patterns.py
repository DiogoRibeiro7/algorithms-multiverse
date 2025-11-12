"""
Modern Python Patterns and Features Showcase
=============================================

This module demonstrates modern Python 3.10+ features and best practices
that are applied throughout the algorithms-multiverse codebase.

Features Demonstrated:
1. Python 3.10+ structural pattern matching (match/case)
2. Union types with | syntax
3. Protocol-based duck typing
4. Dataclasses and frozen dataclasses
5. ParamSpec and TypeVarTuple for advanced generics
6. Context managers
7. Async/await patterns
8. functools decorators (cached_property, lru_cache, singledispatch)
9. Type narrowing with TypeGuard
10. Literal types and type aliases

Author: Claude
Version: 2.0 (Python 3.10+ required)
"""

from __future__ import annotations

import asyncio
import functools
import time
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any,
    Generic,
    Literal,
    ParamSpec,
    Protocol,
    TypeAlias,
    TypeGuard,
    TypeVar,
    TypeVarTuple,
)

# ============================================================================
# SECTION 1: Python 3.10+ Type Hints
# ============================================================================

# Modern union types (Python 3.10+)
Number: TypeAlias = int | float
OptionalString: TypeAlias = str | None
Result: TypeAlias = tuple[bool, str | None]

# Generic type variables
T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)
P = ParamSpec("P")
Ts = TypeVarTuple("Ts")


# ============================================================================
# SECTION 2: Protocols for Duck Typing
# ============================================================================


class Comparable(Protocol):
    """Protocol for comparable objects (implements <, >, ==)."""

    def __lt__(self, other: Any, /) -> bool:
        ...

    def __gt__(self, other: Any, /) -> bool:
        ...

    def __eq__(self, other: Any, /) -> bool:
        ...


class Sortable(Protocol):
    """Protocol for sortable collections."""

    def __len__(self) -> int:
        ...

    def __getitem__(self, index: int) -> Comparable:
        ...

    def __setitem__(self, index: int, value: Comparable) -> None:
        ...


class Hashable(Protocol):
    """Protocol for hashable objects."""

    def __hash__(self) -> int:
        ...

    def __eq__(self, other: Any, /) -> bool:
        ...


# ============================================================================
# SECTION 3: Dataclasses and Frozen Dataclasses
# ============================================================================


@dataclass(frozen=True)
class AlgorithmMetrics:
    """
    Immutable metrics for algorithm performance.

    Using frozen=True makes this immutable and hashable.
    """

    name: str
    comparisons: int
    swaps: int
    time_ms: float
    space_complexity: str

    @property
    def operations(self) -> int:
        """Total operations performed."""
        return self.comparisons + self.swaps

    def __str__(self) -> str:
        return (
            f"{self.name}: {self.comparisons} comparisons, "
            f"{self.swaps} swaps, {self.time_ms:.2f}ms"
        )


@dataclass
class SortResult(Generic[T]):
    """Result of a sorting operation with metadata."""

    data: list[T]
    metrics: AlgorithmMetrics
    is_stable: bool = True
    original_order_preserved: bool = False

    def __post_init__(self) -> None:
        """Validate data after initialization."""
        if not isinstance(self.data, list):
            raise TypeError("data must be a list")


@dataclass
class BenchmarkConfig:
    """Configuration for benchmarking algorithms."""

    sizes: list[int] = field(default_factory=lambda: [10, 100, 1000])
    patterns: dict[str, Callable[[int], list[int]]] = field(default_factory=dict)
    iterations: int = 3
    warmup_iterations: int = 1

    def __post_init__(self) -> None:
        if not self.patterns:
            self.patterns = {
                "random": lambda n: list(range(n)),
                "sorted": lambda n: list(range(n)),
                "reversed": lambda n: list(range(n, 0, -1)),
            }


# ============================================================================
# SECTION 4: Enums for Type Safety
# ============================================================================


class SortAlgorithm(Enum):
    """Enumeration of available sorting algorithms."""

    BUBBLE = auto()
    INSERTION = auto()
    SELECTION = auto()
    MERGE = auto()
    QUICK = auto()
    HEAP = auto()


class DataPattern(Enum):
    """Common data patterns for testing."""

    RANDOM = auto()
    SORTED = auto()
    REVERSED = auto()
    NEARLY_SORTED = auto()
    ALL_EQUAL = auto()


# ============================================================================
# SECTION 5: Structural Pattern Matching (Python 3.10+)
# ============================================================================


def analyze_algorithm_performance(metrics: AlgorithmMetrics) -> str:
    """
    Analyze algorithm performance using structural pattern matching.

    Demonstrates Python 3.10+ match/case statements.
    """
    match (metrics.comparisons, metrics.swaps):
        case (0, 0):
            return "No operations performed - likely empty input"

        case (comp, 0) if comp > 0:
            return f"Read-only algorithm: {comp} comparisons, no modifications"

        case (comp, swaps) if swaps > comp * 2:
            return f"Write-heavy: {swaps} swaps exceed {comp} comparisons"

        case (comp, swaps) if comp > 1000 and swaps < 100:
            return f"Comparison-heavy but efficient: {comp} comps, {swaps} swaps"

        case _:
            return f"Standard performance: {metrics.comparisons} comparisons, {metrics.swaps} swaps"


def classify_data_pattern(data: list[Number]) -> DataPattern:
    """
    Classify data pattern using structural pattern matching.

    Demonstrates matching on list patterns.
    """
    match data:
        case []:
            return DataPattern.RANDOM  # Empty case

        case [_]:
            return DataPattern.RANDOM  # Single element

        case [x, y] if x == y:
            return DataPattern.ALL_EQUAL

        case [first, *rest] if all(first == x for x in rest):
            return DataPattern.ALL_EQUAL

        case [first, *rest] if all(a <= b for a, b in zip(data, rest)):
            return DataPattern.SORTED

        case [first, *rest] if all(a >= b for a, b in zip(data, rest)):
            return DataPattern.REVERSED

        case _:
            # Check if nearly sorted (< 10% inversions)
            inversions = sum(1 for i in range(len(data) - 1) if data[i] > data[i + 1])
            return DataPattern.NEARLY_SORTED if inversions < len(data) * 0.1 else DataPattern.RANDOM


def get_algorithm_complexity(algo: SortAlgorithm, pattern: DataPattern) -> str:
    """
    Get time complexity based on algorithm and data pattern.

    Demonstrates matching on enum values.
    """
    match (algo, pattern):
        case (SortAlgorithm.BUBBLE | SortAlgorithm.INSERTION, DataPattern.SORTED):
            return "O(n)"

        case (SortAlgorithm.BUBBLE | SortAlgorithm.INSERTION | SortAlgorithm.SELECTION, _):
            return "O(n²)"

        case (SortAlgorithm.MERGE | SortAlgorithm.HEAP, _):
            return "O(n log n)"

        case (SortAlgorithm.QUICK, DataPattern.SORTED | DataPattern.REVERSED):
            return "O(n²) - worst case"

        case (SortAlgorithm.QUICK, _):
            return "O(n log n) - average"

        case _:
            return "Unknown complexity"


# ============================================================================
# SECTION 6: TypeGuard for Type Narrowing
# ============================================================================


def is_list_of_ints(data: list[Any]) -> TypeGuard[list[int]]:
    """
    Type guard to narrow list[Any] to list[int].

    Helps type checkers understand type refinement.
    """
    return all(isinstance(x, int) for x in data)


def is_comparable(obj: Any) -> TypeGuard[Comparable]:
    """Type guard for Comparable protocol."""
    return hasattr(obj, "__lt__") and hasattr(obj, "__gt__") and hasattr(obj, "__eq__")


def process_data(data: list[Any]) -> list[int]:
    """
    Process data with type narrowing.

    After the type guard, type checkers know data is list[int].
    """
    if is_list_of_ints(data):
        # Type checker knows data is list[int] here
        return sorted(data)
    else:
        raise TypeError("Expected list of integers")


# ============================================================================
# SECTION 7: Generic Functions with ParamSpec
# ============================================================================


def timer(func: Callable[P, T]) -> Callable[P, tuple[T, float]]:
    """
    Decorator that times function execution.

    ParamSpec preserves function signature.
    """
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> tuple[T, float]:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed

    return wrapper


def memoize(func: Callable[P, T]) -> Callable[P, T]:
    """
    Memoization decorator using ParamSpec.

    Better than lru_cache for type checking.
    """
    cache: dict[tuple[Any, ...], T] = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        # Create cache key from arguments
        key = (args, tuple(sorted(kwargs.items())))

        if key not in cache:
            cache[key] = func(*args, **kwargs)

        return cache[key]

    return wrapper


# ============================================================================
# SECTION 8: Context Managers
# ============================================================================


@contextmanager
def algorithm_timer(name: str) -> Iterator[dict[str, float]]:
    """
    Context manager for timing algorithm execution.

    Usage:
        with algorithm_timer("Quick Sort") as stats:
            quick_sort(data)
        print(f"Took {stats['elapsed_ms']:.2f}ms")
    """
    stats: dict[str, float] = {}
    start = time.perf_counter()

    try:
        yield stats
    finally:
        elapsed = time.perf_counter() - start
        stats["elapsed_ms"] = elapsed * 1000
        print(f"[{name}] Completed in {elapsed * 1000:.2f}ms")


@dataclass
class PerformanceProfiler:
    """Context manager class for detailed performance profiling."""

    operation: str
    metrics: dict[str, Any] = field(default_factory=dict)

    def __enter__(self) -> PerformanceProfiler:
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.elapsed = time.perf_counter() - self.start_time
        self.metrics["elapsed_ms"] = self.elapsed * 1000

        if exc_type is None:
            print(f"✓ {self.operation}: {self.elapsed * 1000:.2f}ms")
        else:
            print(f"✗ {self.operation}: Failed with {exc_type.__name__}")


# ============================================================================
# SECTION 9: Async/Await Patterns
# ============================================================================


async def async_merge_sort(arr: list[T]) -> list[T]:
    """
    Async merge sort - demonstrates async recursion.

    Useful for I/O-bound operations or when sorting multiple arrays.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    # Sort both halves concurrently
    left_task = asyncio.create_task(async_merge_sort(arr[:mid]))
    right_task = asyncio.create_task(async_merge_sort(arr[mid:]))

    left = await left_task
    right = await right_task

    # Merge
    result: list[T] = []
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


async def async_parallel_sort(arrays: list[list[T]]) -> list[list[T]]:
    """
    Sort multiple arrays in parallel using async.

    Demonstrates concurrent processing.
    """
    tasks = [asyncio.create_task(async_merge_sort(arr)) for arr in arrays]
    return await asyncio.gather(*tasks)


async def async_benchmark_algorithm(
    func: Callable[[list[T]], list[T]],
    data: list[T],
    iterations: int = 3,
) -> AlgorithmMetrics:
    """
    Async benchmark for sorting algorithms.

    Allows non-blocking performance testing.
    """
    total_time = 0.0

    for _ in range(iterations):
        test_data = data.copy()
        start = time.perf_counter()

        # Simulate async operation
        await asyncio.sleep(0)  # Yield control
        result = func(test_data)

        elapsed = time.perf_counter() - start
        total_time += elapsed

    avg_time = (total_time / iterations) * 1000

    return AlgorithmMetrics(
        name=func.__name__,
        comparisons=0,  # Would need instrumentation
        swaps=0,
        time_ms=avg_time,
        space_complexity="O(n)",
    )


# ============================================================================
# SECTION 10: functools and itertools Optimizations
# ============================================================================


@functools.lru_cache(maxsize=1000)
def fibonacci_cached(n: int) -> int:
    """
    Fibonacci with automatic memoization.

    lru_cache provides automatic caching.
    """
    if n <= 1:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)


@functools.singledispatch
def process_value(value: Any) -> str:
    """
    Single dispatch generic function.

    Different implementations based on type.
    """
    return f"Generic: {value}"


@process_value.register
def _(value: int) -> str:
    return f"Integer: {value:,}"


@process_value.register
def _(value: list) -> str:
    return f"List of {len(value)} items"


@process_value.register
def _(value: dict) -> str:
    return f"Dict with {len(value)} keys"


class Algorithm:
    """Class demonstrating cached_property."""

    def __init__(self, data: list[int]):
        self.data = data

    @functools.cached_property
    def sorted_data(self) -> list[int]:
        """Computed once and cached."""
        print("Computing sorted data...")
        return sorted(self.data)

    @functools.cached_property
    def data_stats(self) -> dict[str, float]:
        """Expensive computation, cached after first call."""
        return {
            "mean": sum(self.data) / len(self.data),
            "min": min(self.data),
            "max": max(self.data),
        }


def sliding_window_max(arr: list[int], k: int) -> list[int]:
    """
    Find maximum in sliding window using itertools.

    Demonstrates efficient iteration patterns.
    """
    from itertools import islice

    result = []
    for i in range(len(arr) - k + 1):
        window = islice(arr, i, i + k)
        result.append(max(window))

    return result


def pairwise_comparison(arr: list[T]) -> list[tuple[T, T]]:
    """
    Generate pairwise comparisons efficiently.

    Uses itertools for memory efficiency.
    """
    from itertools import combinations

    return list(combinations(arr, 2))


# ============================================================================
# DEMONSTRATION
# ============================================================================


def demonstrate_modern_patterns() -> None:
    """Demonstrate all modern Python patterns."""

    print("=" * 80)
    print("MODERN PYTHON PATTERNS SHOWCASE")
    print("=" * 80)

    # Pattern 1: Structural Pattern Matching
    print("\n1. STRUCTURAL PATTERN MATCHING (Python 3.10+)")
    print("-" * 80)

    metrics = AlgorithmMetrics(
        name="Quick Sort",
        comparisons=150,
        swaps=45,
        time_ms=2.5,
        space_complexity="O(log n)",
    )

    print(f"Metrics: {metrics}")
    print(f"Analysis: {analyze_algorithm_performance(metrics)}")

    # Pattern 2: Dataclasses
    print("\n2. DATACLASSES")
    print("-" * 80)

    result = SortResult(
        data=[1, 2, 3, 4, 5],
        metrics=metrics,
        is_stable=True,
    )

    print(f"Result: {result.data}")
    print(f"Stable: {result.is_stable}")

    # Pattern 3: Context Managers
    print("\n3. CONTEXT MANAGERS")
    print("-" * 80)

    with algorithm_timer("Bubble Sort"):
        time.sleep(0.1)  # Simulate work

    with PerformanceProfiler("Insertion Sort") as profiler:
        time.sleep(0.05)

    # Pattern 4: functools
    print("\n4. FUNCTOOLS OPTIMIZATIONS")
    print("-" * 80)

    print(f"Fibonacci(30): {fibonacci_cached(30)}")
    print(f"Fibonacci(30) again (cached): {fibonacci_cached(30)}")

    print(f"Process int: {process_value(42)}")
    print(f"Process list: {process_value([1, 2, 3])}")
    print(f"Process dict: {process_value({'a': 1, 'b': 2})}")

    # Pattern 5: Cached Properties
    print("\n5. CACHED PROPERTIES")
    print("-" * 80)

    algo = Algorithm([5, 2, 8, 1, 9])
    print(f"First access to sorted_data:")
    print(f"  {algo.sorted_data}")
    print(f"Second access (cached):")
    print(f"  {algo.sorted_data}")

    # Pattern 6: Type Guards
    print("\n6. TYPE GUARDS")
    print("-" * 80)

    mixed_data: list[Any] = [1, 2, 3, 4, 5]
    if is_list_of_ints(mixed_data):
        processed = process_data(mixed_data)
        print(f"Processed: {processed}")

    # Pattern 7: Async
    print("\n7. ASYNC/AWAIT")
    print("-" * 80)

    async def demo_async():
        data = [5, 2, 8, 1, 9, 3, 7]
        sorted_data = await async_merge_sort(data)
        print(f"Async sorted: {sorted_data}")

        # Sort multiple arrays concurrently
        arrays = [[3, 1, 4], [2, 7, 1], [9, 5, 6]]
        results = await async_parallel_sort(arrays)
        print(f"Parallel sorted: {results}")

    asyncio.run(demo_async())

    print("\n" + "=" * 80)
    print("✨ All modern patterns demonstrated!")
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_modern_patterns()
