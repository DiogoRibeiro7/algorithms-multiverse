"""
Merge Sort Algorithm Implementation in Python

Time Complexity: O(n log n) - consistently across all cases
Space Complexity: O(n) for auxiliary arrays

Python features:
- Type hints for clarity
- Multiple implementation patterns
- Generator expressions
- List comprehensions
- Object-oriented design
"""

from typing import List, TypeVar, Callable, Any, Iterator
import time
import random
from copy import deepcopy

T = TypeVar("T")


def merge_sort_recursive(arr: List[T]) -> List[T]:
    """
    Recursive merge sort implementation.

    Args:
        arr: List to be sorted

    Returns:
        New sorted list
    """
    if len(arr) <= 1:
        return arr.copy()

    mid = len(arr) // 2
    left = merge_sort_recursive(arr[:mid])
    right = merge_sort_recursive(arr[mid:])

    return merge(left, right)


def merge(left: List[T], right: List[T]) -> List[T]:
    """
    Merge two sorted lists into one sorted list.

    Args:
        left: First sorted list
        right: Second sorted list

    Returns:
        Merged sorted list
    """
    result = []
    i = j = 0

    # Merge while both lists have elements
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])

    return result


def merge_sort_in_place(arr: List[T], left: int = 0, right: int = None) -> None:
    """
    In-place merge sort implementation.

    Args:
        arr: List to be sorted in-place
        left: Left boundary (inclusive)
        right: Right boundary (inclusive)
    """
    if right is None:
        right = len(arr) - 1

    if left < right:
        mid = (left + right) // 2

        merge_sort_in_place(arr, left, mid)
        merge_sort_in_place(arr, mid + 1, right)
        merge_in_place(arr, left, mid, right)


def merge_in_place(arr: List[T], left: int, mid: int, right: int) -> None:
    """
    Merge two sorted subarrays in-place.

    Args:
        arr: The array containing the subarrays
        left: Start of first subarray
        mid: End of first subarray
        right: End of second subarray
    """
    # Create temporary arrays
    left_temp = arr[left : mid + 1]
    right_temp = arr[mid + 1 : right + 1]

    i = j = 0
    k = left

    # Merge the temporary arrays back into arr[left..right]
    while i < len(left_temp) and j < len(right_temp):
        if left_temp[i] <= right_temp[j]:
            arr[k] = left_temp[i]
            i += 1
        else:
            arr[k] = right_temp[j]
            j += 1
        k += 1

    # Copy remaining elements
    while i < len(left_temp):
        arr[k] = left_temp[i]
        i += 1
        k += 1

    while j < len(right_temp):
        arr[k] = right_temp[j]
        j += 1
        k += 1


def merge_sort_iterative(arr: List[T]) -> List[T]:
    """
    Iterative merge sort implementation.

    Args:
        arr: List to be sorted

    Returns:
        New sorted list
    """
    if len(arr) <= 1:
        return arr.copy()

    result = arr.copy()
    size = 1

    while size < len(result):
        left = 0

        while left < len(result) - 1:
            mid = min(left + size - 1, len(result) - 1)
            right = min(left + size * 2 - 1, len(result) - 1)

            if mid < right:
                merge_in_place(result, left, mid, right)

            left += size * 2

        size *= 2

    return result


def is_sorted(arr: List[T]) -> bool:
    """Check if array is sorted."""
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


def demonstrate_merge_sort():
    """Demonstrate various merge sort implementations."""
    print("🔀 Merge Sort Implementation in Python")
    print("=" * 45)

    # Test data
    test_arrays = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 8, 6, 1, 9, 4],
        [1],
        [],
        [3, 3, 3, 3, 3],
        [9, 8, 7, 6, 5, 4, 3, 2, 1],
    ]

    print("\n📋 Basic Sorting Tests:")
    print("-" * 30)

    for i, arr in enumerate(test_arrays):
        original = arr.copy()

        # Test different implementations
        recursive_result = merge_sort_recursive(arr)
        iterative_result = merge_sort_iterative(arr)

        # Test in-place
        inplace_result = arr.copy()
        merge_sort_in_place(inplace_result)

        print(f"Test {i + 1}:")
        print(f"Original:   {original}")
        print(f"Recursive:  {recursive_result}")
        print(f"Iterative:  {iterative_result}")
        print(f"In-place:   {inplace_result}")

        # Verify all results are correct and equal
        results = [recursive_result, iterative_result, inplace_result]
        all_correct = all(is_sorted(result) for result in results)
        all_equal = all(result == recursive_result for result in results)

        print(f"All correct: {'✓' if all_correct else '✗'}")
        print(f"All equal:   {'✓' if all_equal else '✗'}")
        print("-" * 40)

    # String sorting
    words = ["banana", "apple", "cherry", "date", "elderberry"]
    sorted_words = merge_sort_recursive(words)

    print(f"\nWord sorting:")
    print(f"Original:     {words}")
    print(f"Alphabetical: {sorted_words}")


def performance_benchmark():
    """Benchmark different merge sort implementations."""
    print(f"\n⚡ Performance Benchmark")
    print("=" * 30)

    sizes = [1000, 5000, 10000, 50000]
    methods = {
        "Recursive": merge_sort_recursive,
        "Iterative": merge_sort_iterative,
        "Built-in": lambda arr: sorted(arr),
    }

    print("Size".rjust(8), end="")
    for method in methods:
        print(method.rjust(12), end="")
    print()
    print("-" * (8 + 12 * len(methods)))

    for size in sizes:
        # Generate random data
        test_data = [random.randint(1, 1000) for _ in range(size)]

        print(f"{size:8d}", end="")

        for method_name, method_func in methods.items():
            # Warm up
            method_func(test_data[:100])

            # Benchmark
            start_time = time.perf_counter()
            result = method_func(test_data.copy())
            end_time = time.perf_counter()

            elapsed_ms = (end_time - start_time) * 1000
            print(f"{elapsed_ms:11.2f}ms", end="")

            # Verify correctness
            if not is_sorted(result if result else []):
                print(" ✗", end="")
            else:
                print("", end="")

        print()


if __name__ == "__main__":
    demonstrate_merge_sort()
    performance_benchmark()

    print("\n✨ Merge Sort demonstration complete!")
