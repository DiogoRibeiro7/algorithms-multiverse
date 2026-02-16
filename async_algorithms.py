"""
Async Algorithm Processing
===========================

This module demonstrates asynchronous processing of algorithms for:
- Parallel benchmarking
- Concurrent data processing
- Non-blocking I/O operations
- Efficient resource utilization

Python 3.10+ Features:
- Async/await syntax
- Concurrent task execution
- Asyncio gather for parallel processing
- Context managers for async resources
- Modern type hints with async types

Use Cases:
- Benchmarking multiple algorithms simultaneously
- Processing multiple datasets in parallel
- I/O-bound operations (file reading, API calls)
- Real-time algorithm comparison
"""

from __future__ import annotations

import asyncio
import functools
import time
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, Generic, TypeVar

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


# ============================================================================
# DATA STRUCTURES
# ============================================================================


class AlgorithmStatus(Enum):
    """Status of algorithm execution."""

    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


@dataclass
class AsyncAlgorithmResult(Generic[T]):
    """
    Result of an asynchronous algorithm execution.

    Generic dataclass for algorithm results.
    """

    algorithm_name: str
    input_data: list[Any]
    output_data: T | None
    execution_time_ms: float
    status: AlgorithmStatus
    error: Exception | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def success(self) -> bool:
        """Check if execution was successful."""
        return self.status == AlgorithmStatus.COMPLETED and self.error is None

    def __str__(self) -> str:
        if self.success:
            return (
                f"✓ {self.algorithm_name}: {self.execution_time_ms:.2f}ms "
                f"({len(self.input_data)} items)"
            )
        else:
            return f"✗ {self.algorithm_name}: {self.status.name} - {self.error}"


@dataclass
class BenchmarkResult:
    """
    Results from parallel algorithm benchmarking.

    Aggregates multiple algorithm results.
    """

    results: list[AsyncAlgorithmResult]
    total_time_ms: float

    @property
    def successful_count(self) -> int:
        """Count of successful executions."""
        return sum(1 for r in self.results if r.success)

    @property
    def failed_count(self) -> int:
        """Count of failed executions."""
        return sum(1 for r in self.results if not r.success)

    def fastest_algorithm(self) -> AsyncAlgorithmResult | None:
        """Find the fastest successful algorithm."""
        successful = [r for r in self.results if r.success]
        return min(successful, key=lambda r: r.execution_time_ms) if successful else None

    def slowest_algorithm(self) -> AsyncAlgorithmResult | None:
        """Find the slowest successful algorithm."""
        successful = [r for r in self.results if r.success]
        return max(successful, key=lambda r: r.execution_time_ms) if successful else None

    def summary(self) -> str:
        """Generate a summary report."""
        lines = [
            "=" * 80,
            "ASYNC BENCHMARK RESULTS",
            "=" * 80,
            f"Total algorithms: {len(self.results)}",
            f"Successful: {self.successful_count}",
            f"Failed: {self.failed_count}",
            f"Total time: {self.total_time_ms:.2f}ms",
            "",
        ]

        if fastest := self.fastest_algorithm():
            lines.append(f"Fastest: {fastest.algorithm_name} ({fastest.execution_time_ms:.2f}ms)")

        if slowest := self.slowest_algorithm():
            lines.append(f"Slowest: {slowest.algorithm_name} ({slowest.execution_time_ms:.2f}ms)")

        lines.extend(["", "Individual Results:", "-" * 80])

        for result in sorted(self.results, key=lambda r: r.execution_time_ms):
            lines.append(f"  {result}")

        lines.append("=" * 80)
        return "\n".join(lines)


# ============================================================================
# ASYNC ALGORITHM WRAPPERS
# ============================================================================


async def async_execute_algorithm(
    algorithm: Callable[[list[T]], list[T]],
    data: list[T],
    name: str | None = None,
) -> AsyncAlgorithmResult[list[T]]:
    """
    Execute a synchronous algorithm in a thread to avoid blocking the event loop.

    Args:
        algorithm (Callable[[list[T]], list[T]]): CPU-bound function that accepts a copy
            of ``data`` and returns a transformed list.
        data (list[T]): Input payload; copied before the algorithm runs so callers keep
            ownership of their original data.
        name (str | None): Optional label for logging/results. Defaults to the callable name.

    Returns:
        AsyncAlgorithmResult[list[T]]: Captures output data, execution time in milliseconds,
        and any exception that occurred.

    Examples:
        >>> import asyncio
        >>> from async_algorithms import async_execute_algorithm
        >>> async def demo():
        ...     result = await async_execute_algorithm(sorted, [3, 1, 2])
        ...     return result.output_data, round(result.execution_time_ms) >= 0
        >>> asyncio.run(demo())
        ([1, 2, 3], True)
    """
    algorithm_name = name or algorithm.__name__
    status = AlgorithmStatus.PENDING

    try:
        status = AlgorithmStatus.RUNNING
        start_time = time.perf_counter()

        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        output_data = await loop.run_in_executor(None, algorithm, data.copy())

        execution_time = (time.perf_counter() - start_time) * 1000
        status = AlgorithmStatus.COMPLETED

        return AsyncAlgorithmResult(
            algorithm_name=algorithm_name,
            input_data=data,
            output_data=output_data,
            execution_time_ms=execution_time,
            status=status,
        )

    except Exception as e:
        execution_time = (time.perf_counter() - start_time) * 1000 if "start_time" in locals() else 0
        return AsyncAlgorithmResult(
            algorithm_name=algorithm_name,
            input_data=data,
            output_data=None,
            execution_time_ms=execution_time,
            status=AlgorithmStatus.FAILED,
            error=e,
        )


async def async_benchmark_algorithms(
    algorithms: dict[str, Callable[[list[T]], list[T]]],
    test_data: list[T],
    timeout: float | None = None,
) -> BenchmarkResult:
    """
    Benchmark multiple algorithms concurrently.

    Args:
        algorithms (dict[str, Callable]): Mapping of algorithm name to synchronous function.
        test_data (list[T]): Shared dataset provided to every algorithm; each run receives a copy.
        timeout (float | None): Optional timeout **in seconds** for the combined tasks; exceeding
            this raises ``asyncio.TimeoutError``.

    Returns:
        BenchmarkResult: Aggregated result set where ``total_time_ms`` is the wall-clock duration.

    Examples:
        >>> import asyncio
        >>> from async_algorithms import async_benchmark_algorithms
        >>> async def demo():
        ...     algorithms = {'sorted': sorted, 'reverse': lambda xs: list(reversed(xs))}
        ...     result = await async_benchmark_algorithms(algorithms, [3, 2, 1])
        ...     return sorted(result.algorithms)
        >>> asyncio.run(demo())
        ['reverse', 'sorted']
    """
    start_time = time.perf_counter()

    # Create tasks for all algorithms
    tasks = [
        async_execute_algorithm(algo_func, test_data, name)
        for name, algo_func in algorithms.items()
    ]

    # Execute all tasks concurrently
    if timeout:
        results = await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), timeout=timeout)
    else:
        results = await asyncio.gather(*tasks, return_exceptions=True)

    # Handle exceptions in results
    processed_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            algo_name = list(algorithms.keys())[i]
            processed_results.append(
                AsyncAlgorithmResult(
                    algorithm_name=algo_name,
                    input_data=test_data,
                    output_data=None,
                    execution_time_ms=0,
                    status=AlgorithmStatus.FAILED,
                    error=result,
                )
            )
        else:
            processed_results.append(result)

    total_time = (time.perf_counter() - start_time) * 1000

    return BenchmarkResult(results=processed_results, total_time_ms=total_time)


# ============================================================================
# ASYNC SORTING ALGORITHMS
# ============================================================================


async def async_merge_sort(arr: list[T]) -> list[T]:
    """
    Asynchronous merge sort implementation.

    Recursively splits and sorts in parallel.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    # Create tasks for sorting both halves
    left_task = asyncio.create_task(async_merge_sort(arr[:mid]))
    right_task = asyncio.create_task(async_merge_sort(arr[mid:]))

    # Wait for both to complete
    left = await left_task
    right = await right_task

    # Merge the sorted halves
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


async def async_quick_sort(arr: list[T]) -> list[T]:
    """
    Asynchronous quick sort implementation.

    Partitions and sorts subarrays in parallel.
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    # Sort left and right partitions concurrently
    left_task = asyncio.create_task(async_quick_sort(left))
    right_task = asyncio.create_task(async_quick_sort(right))

    sorted_left = await left_task
    sorted_right = await right_task

    return sorted_left + middle + sorted_right


# ============================================================================
# PARALLEL DATA PROCESSING
# ============================================================================


async def async_process_datasets(
    datasets: list[list[T]],
    algorithm: Callable[[list[T]], list[T]],
    max_concurrent: int = 5,
) -> list[AsyncAlgorithmResult[list[T]]]:
    """
    Process datasets concurrently with a semaphore throttling maximum concurrency.

    Args:
        datasets (list[list[T]]): Collection of workloads to feed into ``algorithm``; each is copied.
        algorithm (Callable[[list[T]], list[T]]): CPU-bound callable to run for each dataset.
        max_concurrent (int): Maximum number of tasks scheduled at once; protects shared resources.

    Returns:
        list[AsyncAlgorithmResult[list[T]]]: Result list preserving dataset order.

    Examples:
        >>> import asyncio
        >>> from async_algorithms import async_process_datasets
        >>> async def demo():
        ...     datasets = [[3, 1], [2, 2], [5, 0]]
        ...     results = await async_process_datasets(datasets, sorted, max_concurrent=2)
        ...     return [r.output_data for r in results]
        >>> asyncio.run(demo())
        [[1, 3], [2, 2], [0, 5]]
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_with_semaphore(
        data: list[T], index: int
    ) -> AsyncAlgorithmResult[list[T]]:
        async with semaphore:
            return await async_execute_algorithm(
                algorithm, data, f"{algorithm.__name__}_dataset_{index}"
            )

    tasks = [process_with_semaphore(dataset, i) for i, dataset in enumerate(datasets)]

    return await asyncio.gather(*tasks)


async def async_map_algorithm(
    data_items: list[T],
    transform: Callable[[T], T],
    chunk_size: int = 100,
) -> list[T]:
    """
    Apply a transformation to data items in fixed-size chunks using executors.

    Args:
        data_items (list[T]): Input data to transform.
        transform (Callable[[T], T]): Function executed on each element inside a thread executor.
        chunk_size (int): Chunk partition size; larger values reduce overhead but increase latency.

    Returns:
        list[T]: Flattened list of transformed elements.

    Examples:
        >>> import asyncio
        >>> from async_algorithms import async_map_algorithm
        >>> asyncio.run(async_map_algorithm([1, 2, 3], lambda x: x * 10, chunk_size=2))
        [10, 20, 30]
    """

    async def process_chunk(chunk: list[T]) -> list[T]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: [transform(item) for item in chunk])

    # Split into chunks
    chunks = [data_items[i : i + chunk_size] for i in range(0, len(data_items), chunk_size)]

    # Process chunks concurrently
    tasks = [process_chunk(chunk) for chunk in chunks]
    results = await asyncio.gather(*tasks)

    # Flatten results
    return [item for chunk_result in results for item in chunk_result]


# ============================================================================
# ASYNC FILE I/O OPERATIONS
# ============================================================================


async def async_read_algorithm_input(file_path: Path) -> list[int]:
    """
    Asynchronously read algorithm input from file.

    Demonstrates async file I/O.
    """
    loop = asyncio.get_event_loop()

    def read_file() -> list[int]:
        with open(file_path, "r") as f:
            return [int(line.strip()) for line in f if line.strip().isdigit()]

    return await loop.run_in_executor(None, read_file)


async def async_write_algorithm_output(file_path: Path, data: list[int]) -> None:
    """
    Asynchronously write algorithm output to file.

    Demonstrates async file writing.
    """
    loop = asyncio.get_event_loop()

    def write_file() -> None:
        with open(file_path, "w") as f:
            for item in data:
                f.write(f"{item}\n")

    await loop.run_in_executor(None, write_file)


# ============================================================================
# PROGRESS TRACKING
# ============================================================================


async def async_execute_with_progress(
    algorithms: dict[str, Callable[[list[T]], list[T]]],
    test_data: list[T],
    progress_callback: Callable[[str, float], None] | None = None,
) -> BenchmarkResult:
    """
    Execute algorithms sequentially while emitting percentage updates.

    Args:
        algorithms (dict[str, Callable]): Mapping of algorithm name to callable.
        test_data (list[T]): Dataset copied for each execution.
        progress_callback (Callable[[str, float], None] | None): Invoked after each algorithm
            completes with the algorithm name and completion percentage (0–100).

    Returns:
        BenchmarkResult: Similar to :func:`async_benchmark_algorithms` but tasks execute sequentially
        so progress is deterministic.

    Examples:
        >>> import asyncio
        >>> from async_algorithms import async_execute_with_progress
        >>> updates = []
        >>> async def demo():
        ...     def on_progress(name, percent):
        ...         updates.append((name, round(percent)))
        ...     result = await async_execute_with_progress({'sorted': sorted}, [2, 1], on_progress)
        ...     return result.successful_count
        >>> asyncio.run(demo())
        1
        >>> updates
        [('sorted', 100)]
    """
    total = len(algorithms)
    completed = 0

    async def execute_with_callback(
        name: str, algo: Callable[[list[T]], list[T]]
    ) -> AsyncAlgorithmResult[list[T]]:
        nonlocal completed

        result = await async_execute_algorithm(algo, test_data, name)

        completed += 1
        if progress_callback:
            progress = (completed / total) * 100
            progress_callback(name, progress)

        return result

    start_time = time.perf_counter()

    tasks = [execute_with_callback(name, algo) for name, algo in algorithms.items()]
    results = await asyncio.gather(*tasks)

    total_time = (time.perf_counter() - start_time) * 1000

    return BenchmarkResult(results=results, total_time_ms=total_time)


# ============================================================================
# DEMONSTRATION
# ============================================================================


async def demonstrate_async_algorithms() -> None:
    """Demonstrate asynchronous algorithm processing."""

    print("=" * 80)
    print("ASYNCHRONOUS ALGORITHM PROCESSING DEMO")
    print("=" * 80)

    # Test data
    test_data = list(range(100, 0, -1))  # Reversed list

    print("\n1. ASYNC SORTING ALGORITHMS")
    print("-" * 80)

    # Async sorting
    print("Sorting with async merge sort...")
    start = time.perf_counter()
    sorted_data = await async_merge_sort(test_data.copy())
    elapsed = (time.perf_counter() - start) * 1000
    print(f"  Result: {sorted_data[:10]}... (first 10 items)")
    print(f"  Time: {elapsed:.2f}ms")

    print("\nSorting with async quick sort...")
    start = time.perf_counter()
    sorted_data = await async_quick_sort(test_data.copy())
    elapsed = (time.perf_counter() - start) * 1000
    print(f"  Result: {sorted_data[:10]}... (first 10 items)")
    print(f"  Time: {elapsed:.2f}ms")

    # Parallel benchmarking
    print("\n2. PARALLEL ALGORITHM BENCHMARKING")
    print("-" * 80)

    algorithms = {
        "Python sorted()": sorted,
        "List sort()": lambda arr: arr.sort() or arr,
    }

    print("Benchmarking algorithms in parallel...")
    benchmark_result = await async_benchmark_algorithms(algorithms, test_data)

    print(benchmark_result.summary())

    # Multiple datasets
    print("\n3. PROCESSING MULTIPLE DATASETS")
    print("-" * 80)

    datasets = [list(range(50, 0, -1)) for _ in range(5)]

    print(f"Processing {len(datasets)} datasets in parallel...")
    results = await async_process_datasets(datasets, sorted, max_concurrent=3)

    print(f"Processed {len(results)} datasets:")
    for result in results:
        print(f"  {result}")

    # Progress tracking
    print("\n4. PROGRESS TRACKING")
    print("-" * 80)

    def progress_callback(algo_name: str, progress: float):
        print(f"  Progress: {progress:.1f}% - Completed {algo_name}")

    print("Running with progress tracking...")
    await async_execute_with_progress(algorithms, test_data, progress_callback)

    print("\n" + "=" * 80)
    print("✨ Async demonstration complete!")
    print("=" * 80)


def main() -> None:
    """Main entry point."""
    asyncio.run(demonstrate_async_algorithms())


if __name__ == "__main__":
    main()
