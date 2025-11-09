"""
Bubble Sort Algorithm Implementation in Python

Time Complexity:
- Best Case: O(n) - when array is already sorted (optimized version)
- Average Case: O(n²)
- Worst Case: O(n²) - when array is reverse sorted
Space Complexity: O(1) for in-place, O(n) for functional approach

Bubble Sort works by repeatedly stepping through the list, comparing adjacent
elements and swapping them if they are in the wrong order. The pass through
the list is repeated until the list is sorted.

Python features:
- Type hints for clarity
- Multiple implementation patterns (recursive, iterative, optimized)
- Generator expressions
- List comprehensions
- Object-oriented design
"""

from typing import List, TypeVar, Callable, Tuple
import time
import random
from copy import deepcopy

T = TypeVar("T")


def bubble_sort_iterative(arr: List[T]) -> List[T]:
    """
    Basic iterative bubble sort implementation.

    This is the standard bubble sort algorithm that compares and swaps
    adjacent elements until the entire array is sorted.

    Args:
        arr: List to be sorted

    Returns:
        New sorted list

    Time Complexity: O(n²) in all cases (no optimization)
    Space Complexity: O(n) for the new list
    """
    if len(arr) <= 1:
        return arr.copy()

    result = arr.copy()
    n = len(result)

    # Outer loop for number of passes
    for i in range(n):
        # Inner loop for comparisons
        # After each pass, the largest element "bubbles up" to its position
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                # Swap adjacent elements
                result[j], result[j + 1] = result[j + 1], result[j]

    return result


def bubble_sort_optimized(arr: List[T]) -> List[T]:
    """
    Optimized bubble sort with early termination.

    This version includes a flag to detect if any swaps were made during a pass.
    If no swaps occur, the array is already sorted and we can terminate early.

    Args:
        arr: List to be sorted

    Returns:
        New sorted list

    Time Complexity:
        - Best Case: O(n) when already sorted
        - Average/Worst: O(n²)
    Space Complexity: O(n) for the new list
    """
    if len(arr) <= 1:
        return arr.copy()

    result = arr.copy()
    n = len(result)

    for i in range(n):
        # Flag to optimize for already sorted arrays
        swapped = False

        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True

        # If no swaps occurred, array is sorted
        if not swapped:
            break

    return result


def bubble_sort_in_place(arr: List[T]) -> None:
    """
    In-place bubble sort implementation (optimized).

    Sorts the array in-place without creating a new list,
    minimizing space complexity.

    Args:
        arr: List to be sorted in-place

    Time Complexity: O(n) best case, O(n²) average/worst
    Space Complexity: O(1)
    """
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break


def bubble_sort_recursive(arr: List[T], n: int = None) -> List[T]:
    """
    Recursive bubble sort implementation.

    Each recursive call performs one pass through the array,
    bubbling the largest element to the end.

    Args:
        arr: List to be sorted
        n: Size of the array portion to sort (used in recursion)

    Returns:
        New sorted list

    Time Complexity: O(n²)
    Space Complexity: O(n) for recursion stack + O(n) for new list
    """
    if n is None:
        result = arr.copy()
        return bubble_sort_recursive(result, len(result))

    # Base case: single element or empty
    if n <= 1:
        return arr

    # One pass of bubble sort
    # After this pass, the largest element will be at the end
    for i in range(n - 1):
        if arr[i] > arr[i + 1]:
            arr[i], arr[i + 1] = arr[i + 1], arr[i]

    # Recursively sort the first n-1 elements
    return bubble_sort_recursive(arr, n - 1)


def bubble_sort_functional(arr: List[T]) -> List[T]:
    """
    Functional-style bubble sort implementation.

    This implementation creates new lists for each iteration,
    following functional programming principles (immutability).

    Args:
        arr: List to be sorted

    Returns:
        New sorted list

    Time Complexity: O(n²)
    Space Complexity: O(n²) due to list copies
    """
    if len(arr) <= 1:
        return arr.copy()

    def single_pass(lst: List[T]) -> Tuple[List[T], bool]:
        """Perform one pass and return the result with swap status."""
        result = []
        swapped = False

        for i in range(len(lst) - 1):
            if lst[i] > lst[i + 1]:
                result.append(lst[i + 1])
                result.append(lst[i])
                swapped = True
                # Skip next element since we already added it
                if i + 2 < len(lst):
                    result.extend(lst[i + 2:])
                break
            else:
                result.append(lst[i])
        else:
            # Add the last element if we completed the loop
            result.append(lst[-1])

        return result, swapped

    # Simpler functional approach using list comprehension
    result = arr.copy()
    n = len(result)

    for i in range(n):
        swapped = False
        new_result = []

        for j in range(len(result) - 1):
            if result[j] > result[j + 1]:
                new_result.append(result[j + 1])
                new_result.append(result[j])
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True

        if not swapped:
            break

    return result


def bubble_sort_with_comparator(arr: List[T], compare: Callable[[T, T], int] = None) -> List[T]:
    """
    Bubble sort with custom comparison function.

    Args:
        arr: List to be sorted
        compare: Comparison function (a, b) -> int
                 Returns: negative if a < b, 0 if a == b, positive if a > b

    Returns:
        New sorted list

    Example:
        # Sort in descending order
        bubble_sort_with_comparator([3, 1, 4], lambda a, b: b - a)
    """
    if compare is None:
        compare = lambda a, b: (a > b) - (a < b)

    result = arr.copy()
    n = len(result)

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            if compare(result[j], result[j + 1]) > 0:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True

        if not swapped:
            break

    return result


def cocktail_sort(arr: List[T]) -> List[T]:
    """
    Cocktail Shaker Sort (bidirectional bubble sort).

    An optimized version of bubble sort that sorts in both directions
    alternately, which can be more efficient for certain data patterns.

    Args:
        arr: List to be sorted

    Returns:
        New sorted list

    Time Complexity: O(n²) worst case, but often faster than standard bubble sort
    Space Complexity: O(n)
    """
    if len(arr) <= 1:
        return arr.copy()

    result = arr.copy()
    start = 0
    end = len(result) - 1
    swapped = True

    while swapped:
        swapped = False

        # Forward pass (like bubble sort)
        for i in range(start, end):
            if result[i] > result[i + 1]:
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True

        if not swapped:
            break

        swapped = False
        end -= 1

        # Backward pass
        for i in range(end - 1, start - 1, -1):
            if result[i] > result[i + 1]:
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True

        start += 1

    return result


def is_sorted(arr: List[T]) -> bool:
    """Check if array is sorted in ascending order."""
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


def demonstrate_bubble_sort():
    """Demonstrate various bubble sort implementations."""
    print("🫧 Bubble Sort Implementation in Python")
    print("=" * 50)

    # Test data - comprehensive edge cases
    test_arrays = [
        ([64, 34, 25, 12, 22, 11, 90], "Random array"),
        ([5, 2, 8, 6, 1, 9, 4], "Small random array"),
        ([1], "Single element"),
        ([], "Empty array"),
        ([3, 3, 3, 3, 3], "All duplicates"),
        ([9, 8, 7, 6, 5, 4, 3, 2, 1], "Reverse sorted"),
        ([1, 2, 3, 4, 5], "Already sorted"),
        ([5, 1, 4, 2, 3], "Nearly sorted"),
    ]

    print("\n📋 Basic Sorting Tests:")
    print("-" * 50)

    for arr, description in test_arrays:
        original = arr.copy()

        # Test different implementations
        iterative_result = bubble_sort_iterative(arr)
        optimized_result = bubble_sort_optimized(arr)
        recursive_result = bubble_sort_recursive(arr)
        cocktail_result = cocktail_sort(arr)

        # Test in-place
        inplace_result = arr.copy()
        bubble_sort_in_place(inplace_result)

        print(f"\nTest: {description}")
        print(f"Original:  {original}")
        print(f"Sorted:    {iterative_result}")

        # Verify all results are correct and equal
        results = [iterative_result, optimized_result, recursive_result,
                   cocktail_result, inplace_result]
        all_correct = all(is_sorted(result) for result in results)
        all_equal = all(result == iterative_result for result in results)

        status = "✓" if all_correct and all_equal else "✗"
        print(f"All implementations match: {status}")

    print("\n" + "-" * 50)

    # String sorting
    words = ["banana", "apple", "cherry", "date", "elderberry"]
    sorted_words = bubble_sort_optimized(words)

    print(f"\n🔤 Word sorting:")
    print(f"Original:     {words}")
    print(f"Alphabetical: {sorted_words}")

    # Custom comparison
    numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    desc_sorted = bubble_sort_with_comparator(numbers, lambda a, b: b - a)

    print(f"\n🔢 Custom comparison (descending):")
    print(f"Original:   {numbers}")
    print(f"Descending: {desc_sorted}")


def performance_benchmark():
    """Benchmark different bubble sort implementations."""
    print(f"\n\n⚡ Performance Benchmark")
    print("=" * 70)

    sizes = [100, 500, 1000, 2000]

    # Test different data patterns
    patterns = {
        "Random": lambda n: [random.randint(1, 1000) for _ in range(n)],
        "Sorted": lambda n: list(range(n)),
        "Reversed": lambda n: list(range(n, 0, -1)),
        "Nearly Sorted": lambda n: list(range(n)) if n < 10 else
                         list(range(n-5)) + [n-1, n-3, n-2, n-4, n-5] + list(range(n-5, n)),
    }

    methods = {
        "Iterative": bubble_sort_iterative,
        "Optimized": bubble_sort_optimized,
        "Recursive": bubble_sort_recursive,
        "Cocktail": cocktail_sort,
        "Built-in": lambda arr: sorted(arr),
    }

    for pattern_name, pattern_gen in patterns.items():
        print(f"\n{pattern_name} Data:")
        print("Size".rjust(8), end="")
        for method in methods:
            print(method.rjust(12), end="")
        print()
        print("-" * (8 + 12 * len(methods)))

        for size in sizes:
            # Generate test data
            test_data = pattern_gen(size)

            print(f"{size:8d}", end="")

            for method_name, method_func in methods.items():
                # Skip recursive for large sizes (stack overflow risk)
                if method_name == "Recursive" and size > 1000:
                    print(f"{'N/A':>12}", end="")
                    continue

                # Benchmark
                try:
                    start_time = time.perf_counter()
                    result = method_func(test_data.copy())
                    end_time = time.perf_counter()

                    elapsed_ms = (end_time - start_time) * 1000
                    print(f"{elapsed_ms:11.2f}ms", end="")

                    # Verify correctness
                    if not is_sorted(result if result else []):
                        print(" ✗", end="")
                except RecursionError:
                    print(f"{'OVERFLOW':>12}", end="")

            print()


def count_comparisons_and_swaps(arr: List[T]) -> Tuple[int, int]:
    """
    Count the number of comparisons and swaps made during bubble sort.

    Args:
        arr: List to be sorted

    Returns:
        Tuple of (comparisons, swaps)
    """
    result = arr.copy()
    n = len(result)
    comparisons = 0
    swaps = 0

    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swaps += 1

    return comparisons, swaps


def analyze_algorithm():
    """Analyze bubble sort behavior with different inputs."""
    print(f"\n\n🔍 Algorithm Analysis")
    print("=" * 50)

    test_cases = [
        ([5, 2, 8, 6, 1], "Random"),
        ([1, 2, 3, 4, 5], "Already sorted"),
        ([5, 4, 3, 2, 1], "Reverse sorted"),
    ]

    for arr, description in test_cases:
        comparisons, swaps = count_comparisons_and_swaps(arr)
        n = len(arr)

        print(f"\n{description}: {arr}")
        print(f"Array size (n): {n}")
        print(f"Comparisons: {comparisons} (theoretical max: {n * (n - 1) // 2})")
        print(f"Swaps: {swaps}")
        print(f"Efficiency: {(1 - swaps / max(comparisons, 1)) * 100:.1f}% "
              f"(fewer swaps is better)")


class BubbleSorter:
    """
    Object-oriented wrapper for bubble sort with statistics tracking.
    """

    def __init__(self):
        self.comparisons = 0
        self.swaps = 0
        self.iterations = 0

    def sort(self, arr: List[T]) -> List[T]:
        """Sort array and track statistics."""
        self.reset_stats()
        result = arr.copy()
        n = len(result)

        for i in range(n):
            self.iterations += 1
            swapped = False

            for j in range(0, n - i - 1):
                self.comparisons += 1
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
                    self.swaps += 1
                    swapped = True

            if not swapped:
                break

        return result

    def reset_stats(self):
        """Reset statistics counters."""
        self.comparisons = 0
        self.swaps = 0
        self.iterations = 0

    def get_stats(self) -> dict:
        """Get sorting statistics."""
        return {
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "iterations": self.iterations,
        }


if __name__ == "__main__":
    demonstrate_bubble_sort()
    performance_benchmark()
    analyze_algorithm()

    # Demonstrate OOP approach
    print(f"\n\n📊 Object-Oriented Approach")
    print("=" * 50)

    sorter = BubbleSorter()
    test_array = [64, 34, 25, 12, 22, 11, 90]

    sorted_array = sorter.sort(test_array)
    stats = sorter.get_stats()

    print(f"Original: {test_array}")
    print(f"Sorted:   {sorted_array}")
    print(f"Statistics: {stats}")

    print("\n✨ Bubble Sort demonstration complete!")
