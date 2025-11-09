"""
Insertion Sort Algorithm Implementation in Python

Time Complexity:
- Best Case: O(n) - when array is already sorted
- Average Case: O(n²)
- Worst Case: O(n²) - when array is reverse sorted
Space Complexity: O(1) for in-place, O(n) for functional approach

Insertion Sort builds the final sorted array one item at a time. It is much less
efficient on large lists than more advanced algorithms like quicksort or merge sort.
However, it has several advantages:
- Simple implementation
- Efficient for small data sets
- Adaptive (efficient for nearly sorted data)
- Stable (preserves relative order of equal elements)
- In-place (only requires O(1) additional memory)
- Online (can sort a list as it receives it)

Python features:
- Type hints for clarity
- Multiple implementation patterns
- Visualization functions
- Performance analysis
"""

from typing import List, TypeVar, Callable, Tuple
import time
import random
from copy import deepcopy

T = TypeVar("T")


def insertion_sort(arr: List[T]) -> List[T]:
    """
    Standard insertion sort implementation.

    Builds the sorted array one element at a time by repeatedly taking the next
    element and inserting it into the correct position.

    Args:
        arr: List to be sorted

    Returns:
        New sorted list

    Time Complexity: O(n²) average and worst case, O(n) best case
    Space Complexity: O(n) for the new list

    Example:
        Initial: [5, 2, 8, 6, 1]
        Step 1:  [2, 5, 8, 6, 1]  # Insert 2
        Step 2:  [2, 5, 8, 6, 1]  # 8 already in place
        Step 3:  [2, 5, 6, 8, 1]  # Insert 6
        Step 4:  [1, 2, 5, 6, 8]  # Insert 1
    """
    if len(arr) <= 1:
        return arr.copy()

    result = arr.copy()
    insertion_sort_in_place(result)
    return result


def insertion_sort_in_place(arr: List[T]) -> None:
    """
    In-place insertion sort implementation.

    Args:
        arr: List to be sorted in-place

    Time Complexity: O(n²) average and worst case, O(n) best case
    Space Complexity: O(1)
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # Move elements greater than key one position ahead
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key


def insertion_sort_recursive(arr: List[T], n: int = None) -> List[T]:
    """
    Recursive insertion sort implementation.

    Each recursive call sorts the first n elements, then inserts the nth element.

    Args:
        arr: List to be sorted
        n: Number of elements to sort (used in recursion)

    Returns:
        New sorted list

    Time Complexity: O(n²)
    Space Complexity: O(n) for recursion stack + O(n) for new list
    """
    if n is None:
        result = arr.copy()
        return insertion_sort_recursive(result, len(result))

    # Base case
    if n <= 1:
        return arr

    # Sort first n-1 elements
    arr = insertion_sort_recursive(arr, n - 1)

    # Insert last element at its correct position
    key = arr[n - 1]
    j = n - 2

    while j >= 0 and arr[j] > key:
        arr[j + 1] = arr[j]
        j -= 1

    arr[j + 1] = key
    return arr


def binary_insertion_sort(arr: List[T]) -> List[T]:
    """
    Binary insertion sort - uses binary search to find insertion position.

    Reduces the number of comparisons from O(n²) to O(n log n), but the number
    of swaps remains O(n²). Good when comparisons are expensive.

    Args:
        arr: List to be sorted

    Returns:
        New sorted list

    Time Complexity: O(n²) for moves, O(n log n) for comparisons
    Space Complexity: O(n)
    """
    if len(arr) <= 1:
        return arr.copy()

    result = arr.copy()

    for i in range(1, len(result)):
        key = result[i]

        # Find position using binary search
        pos = binary_search_position(result, 0, i - 1, key)

        # Shift elements to make space
        j = i - 1
        while j >= pos:
            result[j + 1] = result[j]
            j -= 1

        result[pos] = key

    return result


def binary_search_position(arr: List[T], left: int, right: int, key: T) -> int:
    """
    Find the position where key should be inserted to maintain sorted order.

    Args:
        arr: Sorted array
        left: Left boundary
        right: Right boundary
        key: Element to insert

    Returns:
        Position where key should be inserted
    """
    if right <= left:
        return left + 1 if key > arr[left] else left

    mid = (left + right) // 2

    if key == arr[mid]:
        return mid + 1

    if key > arr[mid]:
        return binary_search_position(arr, mid + 1, right, key)

    return binary_search_position(arr, left, mid - 1, key)


def shell_sort(arr: List[T]) -> List[T]:
    """
    Shell sort - a generalization of insertion sort.

    Uses a gap sequence to compare and swap elements that are far apart,
    gradually reducing the gap. Named after Donald Shell (1959).

    Args:
        arr: List to be sorted

    Returns:
        New sorted list

    Time Complexity: Depends on gap sequence
        - Shell's original: O(n²)
        - Knuth's: O(n^(3/2))
        - Best known: O(n log²n)
    Space Complexity: O(n)
    """
    if len(arr) <= 1:
        return arr.copy()

    result = arr.copy()
    n = len(result)

    # Start with a large gap, then reduce
    # Using Knuth's sequence: gap = 3^k - 1 / 2
    gap = 1
    while gap < n // 3:
        gap = 3 * gap + 1

    # Perform gapped insertion sort
    while gap > 0:
        for i in range(gap, n):
            key = result[i]
            j = i

            # Insertion sort with gap
            while j >= gap and result[j - gap] > key:
                result[j] = result[j - gap]
                j -= gap

            result[j] = key

        gap //= 3

    return result


def hybrid_insertion_sort(arr: List[T], threshold: int = 10) -> List[T]:
    """
    Hybrid sort that uses insertion sort for small subarrays.

    This is typically used as part of quicksort or mergesort optimizations.
    For small arrays (< 10-20 elements), insertion sort is often faster.

    Args:
        arr: List to be sorted
        threshold: Size below which to use insertion sort

    Returns:
        New sorted list
    """
    if len(arr) <= threshold:
        return insertion_sort(arr)

    # For larger arrays, this would call another algorithm
    # Here we just use insertion sort for demonstration
    return insertion_sort(arr)


def insertion_sort_with_comparator(arr: List[T], compare: Callable[[T, T], int]) -> List[T]:
    """
    Insertion sort with custom comparison function.

    Args:
        arr: List to be sorted
        compare: Comparison function (a, b) -> int
                 Returns: negative if a < b, 0 if a == b, positive if a > b

    Returns:
        New sorted list

    Example:
        # Sort in descending order
        insertion_sort_with_comparator([3, 1, 4], lambda a, b: b - a)
    """
    if len(arr) <= 1:
        return arr.copy()

    result = arr.copy()

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1

        while j >= 0 and compare(result[j], key) > 0:
            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = key

    return result


def visualize_insertion_sort(arr: List[int]) -> List[str]:
    """
    Create a step-by-step visualization of the insertion sort process.

    Args:
        arr: Array to sort (will be copied)

    Returns:
        List of strings showing each step
    """
    steps = []
    result = arr.copy()
    steps.append(f"Initial: {result}")

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1

        steps.append(f"\nStep {i}: Inserting {key}")
        steps.append(f"  Before: {result}")

        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = key
        steps.append(f"  After:  {result}")

    steps.append(f"\nFinal: {result}")
    return steps


def count_operations(arr: List[T]) -> Tuple[int, int]:
    """
    Count comparisons and swaps during insertion sort.

    Args:
        arr: Array to sort

    Returns:
        Tuple of (comparisons, swaps)
    """
    result = arr.copy()
    comparisons = 0
    swaps = 0

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1

        while j >= 0:
            comparisons += 1
            if result[j] > key:
                result[j + 1] = result[j]
                swaps += 1
                j -= 1
            else:
                break

        result[j + 1] = key

    return comparisons, swaps


def is_stable_demo() -> None:
    """
    Demonstrate that insertion sort is stable.

    A stable sort preserves the relative order of elements with equal keys.
    """
    # Using tuples (value, original_index) to track stability
    data = [(3, 0), (1, 1), (3, 2), (2, 3), (3, 4)]

    print("Stability Demonstration:")
    print(f"Original: {data}")

    sorted_data = insertion_sort(data)
    print(f"Sorted:   {sorted_data}")

    # Check if elements with same value maintain their relative order
    three_indices = [item[1] for item in sorted_data if item[0] == 3]
    is_stable = three_indices == sorted([item[1] for item in data if item[0] == 3])

    print(f"Stable: {is_stable} (indices of 3's: {three_indices})")


def is_sorted(arr: List[T]) -> bool:
    """Check if array is sorted in ascending order."""
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


def demonstrate_insertion_sort():
    """Demonstrate various insertion sort implementations."""
    print("📝 Insertion Sort Implementation in Python")
    print("=" * 60)

    # Test data
    test_arrays = [
        ([64, 34, 25, 12, 22, 11, 90], "Random array"),
        ([5, 2, 8, 6, 1, 9, 4], "Small random array"),
        ([1], "Single element"),
        ([], "Empty array"),
        ([3, 3, 3, 3, 3], "All duplicates"),
        ([9, 8, 7, 6, 5, 4, 3, 2, 1], "Reverse sorted"),
        ([1, 2, 3, 4, 5], "Already sorted"),
        ([1, 3, 2, 4, 5], "Nearly sorted"),
    ]

    print("\n📋 Basic Sorting Tests:")
    print("-" * 60)

    for arr, description in test_arrays:
        original = arr.copy()

        # Test different implementations
        standard_result = insertion_sort(arr)
        binary_result = binary_insertion_sort(arr)
        shell_result = shell_sort(arr)
        recursive_result = insertion_sort_recursive(arr)

        print(f"\nTest: {description}")
        print(f"Original:  {original}")
        print(f"Sorted:    {standard_result}")

        # Verify all results are correct and equal
        results = [standard_result, binary_result, shell_result, recursive_result]
        all_correct = all(is_sorted(result) for result in results)
        all_equal = all(result == standard_result for result in results)

        status = "✓" if all_correct and all_equal else "✗"
        print(f"All implementations match: {status}")

    # Visualization demo
    print("\n\n🎬 Step-by-Step Visualization:")
    print("-" * 60)

    demo_arr = [5, 2, 8, 6, 1]
    steps = visualize_insertion_sort(demo_arr)
    for step in steps:
        print(step)

    # Stability demonstration
    print("\n\n🔒 Stability Demonstration:")
    print("-" * 60)
    is_stable_demo()

    # Performance analysis
    print("\n\n📊 Operation Counting:")
    print("-" * 60)

    test_cases = [
        ([5, 2, 8, 6, 1], "Random"),
        ([1, 2, 3, 4, 5], "Already sorted"),
        ([5, 4, 3, 2, 1], "Reverse sorted"),
    ]

    for arr, desc in test_cases:
        comparisons, swaps = count_operations(arr)
        n = len(arr)

        print(f"\n{desc}: {arr}")
        print(f"Array size (n): {n}")
        print(f"Comparisons: {comparisons}")
        print(f"Swaps: {swaps}")
        print(f"Best case comparisons: {n - 1}")
        print(f"Worst case comparisons: {n * (n - 1) // 2}")


def performance_benchmark():
    """Benchmark insertion sort and show when it's preferred."""
    print("\n\n⚡ Performance Benchmark")
    print("=" * 80)
    print("\nInsertion sort is preferred for:")
    print("  • Small arrays (typically n < 10-20)")
    print("  • Nearly sorted arrays")
    print("  • As part of hybrid sorting algorithms")
    print()

    sizes = [5, 10, 20, 50, 100, 500, 1000]

    # Test different data patterns
    patterns = {
        "Random": lambda n: [random.randint(1, 1000) for _ in range(n)],
        "Nearly Sorted": lambda n: sorted([random.randint(1, 1000) for _ in range(n)]),
        "Reversed": lambda n: list(range(n, 0, -1)),
    }

    methods = {
        "Insertion": insertion_sort,
        "Binary Insert": binary_insertion_sort,
        "Shell Sort": shell_sort,
        "Built-in": lambda arr: sorted(arr),
    }

    for pattern_name, pattern_gen in patterns.items():
        print(f"\n{pattern_name} Data:")
        print("Size".rjust(8), end="")
        for method in methods:
            print(method.rjust(15), end="")
        print()
        print("-" * (8 + 15 * len(methods)))

        for size in sizes:
            test_data = pattern_gen(size)

            print(f"{size:8d}", end="")

            for method_name, method_func in methods.items():
                # Warm-up
                if len(test_data) >= 10:
                    method_func(test_data[:10])

                # Benchmark
                start_time = time.perf_counter()
                result = method_func(test_data.copy())
                end_time = time.perf_counter()

                elapsed_ms = (end_time - start_time) * 1000
                print(f"{elapsed_ms:14.3f}ms", end="")

                # Verify correctness
                if not is_sorted(result if result else []):
                    print(" ✗", end="")

            print()

    # Demonstrate hybrid sort advantage
    print("\n\n🔄 Hybrid Sort Analysis:")
    print("-" * 60)
    print("Comparing overhead for small arrays:\n")

    small_sizes = [5, 10, 15, 20, 25]
    print(f"{'Size':<8} {'Insertion':<15} {'Built-in':<15} {'Speedup':<10}")
    print("-" * 48)

    for size in small_sizes:
        test_data = [random.randint(1, 1000) for _ in range(size)]

        start = time.perf_counter()
        insertion_sort(test_data)
        insertion_time = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        sorted(test_data)
        builtin_time = (time.perf_counter() - start) * 1000

        speedup = builtin_time / insertion_time if insertion_time > 0 else 0

        print(f"{size:<8} {insertion_time:<14.3f}ms {builtin_time:<14.3f}ms {speedup:<10.2f}x")


def analyze_adaptiveness():
    """Demonstrate insertion sort's adaptive nature."""
    print("\n\n🎯 Adaptiveness Analysis")
    print("=" * 60)
    print("Insertion sort performs better on nearly sorted data:\n")

    base_size = 100

    # Create arrays with varying degrees of sortedness
    test_cases = [
        (list(range(base_size)), "Fully sorted", 0),
        (list(range(base_size))[::-1], "Fully reversed", 100),
    ]

    # Nearly sorted with different inversion counts
    for inv_percent in [5, 10, 20, 50]:
        arr = list(range(base_size))
        inversions = (base_size * inv_percent) // 100
        for _ in range(inversions):
            i, j = random.randint(0, base_size - 1), random.randint(0, base_size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        test_cases.append((arr, f"{inv_percent}% unsorted", inv_percent))

    print(f"{'Condition':<20} {'Time (ms)':<12} {'Comparisons':<12} {'Swaps':<12}")
    print("-" * 56)

    for arr, desc, _ in test_cases:
        start = time.perf_counter()
        insertion_sort(arr.copy())
        elapsed = (time.perf_counter() - start) * 1000

        comps, swaps = count_operations(arr)

        print(f"{desc:<20} {elapsed:<11.3f}  {comps:<11}  {swaps:<11}")


if __name__ == "__main__":
    demonstrate_insertion_sort()
    performance_benchmark()
    analyze_adaptiveness()

    print("\n✨ Insertion Sort demonstration complete!")
