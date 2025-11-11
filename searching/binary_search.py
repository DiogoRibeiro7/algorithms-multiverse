"""
Binary Search Algorithm Collection in Python

This module implements comprehensive binary search algorithms and variants.

Time Complexity:
- Classic Binary Search: O(log n)
- Exponential Search: O(log n)
- Interpolation Search: O(log log n) average, O(n) worst
- Ternary Search: O(log₃ n)

Space Complexity:
- Iterative: O(1)
- Recursive: O(log n) for call stack

Python features:
- Type hints for better code documentation
- Generic implementations with custom comparators
- Functional programming with lambda functions
- Comprehensive docstrings
- Exception handling for edge cases
"""

from typing import List, Optional, Callable, Any, TypeVar, Tuple
from functools import cmp_to_key
import bisect

T = TypeVar('T')


# ==============================================================================
# 1. CLASSIC BINARY SEARCH
# ==============================================================================

def binary_search_iterative(arr: List[T], target: T) -> int:
    """
    Classic binary search - iterative implementation.

    Searches for target in a sorted array using binary search.

    Args:
        arr: Sorted list of comparable elements
        target: Element to search for

    Returns:
        Index of target if found, -1 otherwise

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Examples:
        >>> binary_search_iterative([1, 3, 5, 7, 9], 5)
        2
        >>> binary_search_iterative([1, 3, 5, 7, 9], 6)
        -1
        >>> binary_search_iterative([], 5)
        -1
        >>> binary_search_iterative([1], 1)
        0
    """
    if not arr:
        return -1

    left, right = 0, len(arr) - 1

    while left <= right:
        # Avoid integer overflow: mid = (left + right) // 2
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def binary_search_recursive(arr: List[T], target: T, left: Optional[int] = None,
                           right: Optional[int] = None) -> int:
    """
    Classic binary search - recursive implementation.

    Args:
        arr: Sorted list of comparable elements
        target: Element to search for
        left: Left boundary (default: 0)
        right: Right boundary (default: len(arr) - 1)

    Returns:
        Index of target if found, -1 otherwise

    Time Complexity: O(log n)
    Space Complexity: O(log n) due to recursion stack

    Examples:
        >>> binary_search_recursive([1, 3, 5, 7, 9], 7)
        3
        >>> binary_search_recursive([1, 3, 5, 7, 9], 2)
        -1
    """
    if not arr:
        return -1

    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1

    if left > right:
        return -1

    mid = left + (right - left) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


def binary_search_generic(arr: List[T], target: T,
                         comparator: Optional[Callable[[T, T], int]] = None) -> int:
    """
    Generic binary search with custom comparator.

    Args:
        arr: Sorted list of elements
        target: Element to search for
        comparator: Custom comparison function (a, b) -> int
                   Returns: negative if a < b, 0 if a == b, positive if a > b

    Returns:
        Index of target if found, -1 otherwise

    Examples:
        >>> # Search with custom comparator (case-insensitive strings)
        >>> arr = ['apple', 'Banana', 'cherry', 'Date']
        >>> binary_search_generic(arr, 'banana',
        ...     lambda a, b: a.lower().__eq__(b.lower()) - (a.lower() > b.lower()))
        1
    """
    if not arr:
        return -1

    def default_compare(a: T, b: T) -> int:
        if a < b:
            return -1
        elif a > b:
            return 1
        return 0

    compare = comparator or default_compare
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2
        cmp_result = compare(arr[mid], target)

        if cmp_result == 0:
            return mid
        elif cmp_result < 0:
            left = mid + 1
        else:
            right = mid - 1

    return -1


# ==============================================================================
# 2. FINDING FIRST/LAST OCCURRENCE
# ==============================================================================

def find_first_occurrence(arr: List[T], target: T) -> int:
    """
    Find the first (leftmost) occurrence of target in sorted array.

    Useful when array contains duplicates.

    Args:
        arr: Sorted list (may contain duplicates)
        target: Element to search for

    Returns:
        Index of first occurrence, -1 if not found

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Examples:
        >>> find_first_occurrence([1, 2, 2, 2, 3, 4, 5], 2)
        1
        >>> find_first_occurrence([1, 1, 1, 1, 1], 1)
        0
        >>> find_first_occurrence([1, 2, 3], 4)
        -1
    """
    if not arr:
        return -1

    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            result = mid
            right = mid - 1  # Continue searching in left half
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


def find_last_occurrence(arr: List[T], target: T) -> int:
    """
    Find the last (rightmost) occurrence of target in sorted array.

    Args:
        arr: Sorted list (may contain duplicates)
        target: Element to search for

    Returns:
        Index of last occurrence, -1 if not found

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Examples:
        >>> find_last_occurrence([1, 2, 2, 2, 3, 4, 5], 2)
        3
        >>> find_last_occurrence([1, 1, 1, 1, 1], 1)
        4
        >>> find_last_occurrence([1, 2, 3], 4)
        -1
    """
    if not arr:
        return -1

    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            result = mid
            left = mid + 1  # Continue searching in right half
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


def count_occurrences(arr: List[T], target: T) -> int:
    """
    Count total occurrences of target in sorted array.

    Uses first and last occurrence to calculate count.

    Args:
        arr: Sorted list (may contain duplicates)
        target: Element to count

    Returns:
        Number of occurrences

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Examples:
        >>> count_occurrences([1, 2, 2, 2, 3, 4, 5], 2)
        3
        >>> count_occurrences([1, 2, 3], 4)
        0
    """
    first = find_first_occurrence(arr, target)
    if first == -1:
        return 0

    last = find_last_occurrence(arr, target)
    return last - first + 1


# ==============================================================================
# 3. BINARY SEARCH ON ROTATED SORTED ARRAY
# ==============================================================================

def search_rotated_array(arr: List[T], target: T) -> int:
    """
    Search in a rotated sorted array.

    Array was originally sorted, then rotated at some pivot point.
    Example: [4, 5, 6, 7, 0, 1, 2] is [0, 1, 2, 4, 5, 6, 7] rotated at index 4.

    Args:
        arr: Rotated sorted array (no duplicates)
        target: Element to search for

    Returns:
        Index of target if found, -1 otherwise

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Examples:
        >>> search_rotated_array([4, 5, 6, 7, 0, 1, 2], 0)
        4
        >>> search_rotated_array([4, 5, 6, 7, 0, 1, 2], 3)
        -1
        >>> search_rotated_array([1], 0)
        -1
    """
    if not arr:
        return -1

    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid

        # Determine which half is sorted
        if arr[left] <= arr[mid]:
            # Left half is sorted
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is sorted
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1


def find_rotation_point(arr: List[T]) -> int:
    """
    Find the index of rotation point (minimum element) in rotated sorted array.

    Args:
        arr: Rotated sorted array

    Returns:
        Index of minimum element (rotation point)

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Examples:
        >>> find_rotation_point([4, 5, 6, 7, 0, 1, 2])
        4
        >>> find_rotation_point([1, 2, 3, 4, 5])
        0
    """
    if not arr:
        return -1

    left, right = 0, len(arr) - 1

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] > arr[right]:
            left = mid + 1
        else:
            right = mid

    return left


# ==============================================================================
# 4. EXPONENTIAL SEARCH
# ==============================================================================

def exponential_search(arr: List[T], target: T) -> int:
    """
    Exponential search - useful for unbounded/infinite arrays.

    First finds a range where element might exist, then performs binary search.
    Particularly efficient when target is closer to the beginning.

    Args:
        arr: Sorted list
        target: Element to search for

    Returns:
        Index of target if found, -1 otherwise

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Examples:
        >>> exponential_search([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 7)
        6
        >>> exponential_search([1, 2, 3, 4, 5], 10)
        -1
    """
    if not arr:
        return -1

    if arr[0] == target:
        return 0

    # Find range for binary search by repeated doubling
    i = 1
    n = len(arr)
    while i < n and arr[i] <= target:
        i *= 2

    # Perform binary search in found range
    left = i // 2
    right = min(i, n - 1)

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


# ==============================================================================
# 5. INTERPOLATION SEARCH
# ==============================================================================

def interpolation_search(arr: List[int], target: int) -> int:
    """
    Interpolation search - better than binary search for uniformly distributed data.

    Uses value information to guess position (like looking up a phone book).

    Args:
        arr: Sorted list of integers
        target: Integer to search for

    Returns:
        Index of target if found, -1 otherwise

    Time Complexity: O(log log n) average, O(n) worst case
    Space Complexity: O(1)

    Examples:
        >>> interpolation_search([10, 20, 30, 40, 50, 60, 70, 80, 90], 70)
        6
        >>> interpolation_search([1, 2, 4, 8, 16, 32, 64], 16)
        4
    """
    if not arr:
        return -1

    left, right = 0, len(arr) - 1

    while left <= right and arr[left] <= target <= arr[right]:
        if left == right:
            if arr[left] == target:
                return left
            return -1

        # Interpolation formula
        pos = left + ((target - arr[left]) * (right - left) //
                     (arr[right] - arr[left]))

        # Ensure pos is within bounds
        pos = max(left, min(pos, right))

        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            left = pos + 1
        else:
            right = pos - 1

    return -1


# ==============================================================================
# 6. TERNARY SEARCH
# ==============================================================================

def ternary_search(arr: List[T], target: T) -> int:
    """
    Ternary search - divides array into three parts instead of two.

    Generally less efficient than binary search for searching,
    but useful for finding maximum/minimum of unimodal functions.

    Args:
        arr: Sorted list
        target: Element to search for

    Returns:
        Index of target if found, -1 otherwise

    Time Complexity: O(log₃ n) ≈ O(log n)
    Space Complexity: O(1)

    Examples:
        >>> ternary_search([1, 2, 3, 4, 5, 6, 7, 8, 9], 5)
        4
        >>> ternary_search([1, 2, 3], 4)
        -1
    """
    if not arr:
        return -1

    left, right = 0, len(arr) - 1

    while left <= right:
        # Divide into three parts
        mid1 = left + (right - left) // 3
        mid2 = right - (right - left) // 3

        if arr[mid1] == target:
            return mid1
        if arr[mid2] == target:
            return mid2

        if target < arr[mid1]:
            right = mid1 - 1
        elif target > arr[mid2]:
            left = mid2 + 1
        else:
            left = mid1 + 1
            right = mid2 - 1

    return -1


def ternary_search_maximum(func: Callable[[float], float],
                          left: float, right: float,
                          epsilon: float = 1e-9) -> float:
    """
    Ternary search for finding maximum of unimodal function.

    Args:
        func: Unimodal function (single peak)
        left: Left boundary
        right: Right boundary
        epsilon: Precision threshold

    Returns:
        x value where function reaches maximum

    Time Complexity: O(log(range/epsilon))

    Examples:
        >>> # Find maximum of -x^2 + 4x + 1 (peak at x=2)
        >>> f = lambda x: -x**2 + 4*x + 1
        >>> abs(ternary_search_maximum(f, -10, 10) - 2.0) < 1e-6
        True
    """
    while right - left > epsilon:
        mid1 = left + (right - left) / 3
        mid2 = right - (right - left) / 3

        if func(mid1) < func(mid2):
            left = mid1
        else:
            right = mid2

    return (left + right) / 2


# ==============================================================================
# 7. BINARY SEARCH ON ANSWER (OPTIMIZATION PROBLEMS)
# ==============================================================================

def binary_search_on_answer(predicate: Callable[[int], bool],
                           low: int, high: int) -> Optional[int]:
    """
    Binary search on answer space for optimization problems.

    Finds the minimum/maximum value that satisfies a monotonic predicate.
    Useful for problems like "minimum capacity", "maximum distance", etc.

    Args:
        predicate: Function that returns True if answer is feasible
        low: Minimum possible answer
        high: Maximum possible answer

    Returns:
        Minimum value where predicate is True, None if no solution

    Time Complexity: O(log(high - low) * T) where T is predicate time

    Examples:
        >>> # Find minimum capacity to ship packages within D days
        >>> def can_ship(capacity, weights, days):
        ...     day_count, current_weight = 1, 0
        ...     for w in weights:
        ...         if current_weight + w > capacity:
        ...             day_count += 1
        ...             current_weight = w
        ...         else:
        ...             current_weight += w
        ...     return day_count <= days
        >>>
        >>> weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        >>> binary_search_on_answer(lambda cap: can_ship(cap, weights, 5), 1, 55)
        15
    """
    result = None

    while low <= high:
        mid = low + (high - low) // 2

        if predicate(mid):
            result = mid
            high = mid - 1  # Try to find smaller answer
        else:
            low = mid + 1

    return result


def find_square_root(n: int, precision: int = 0) -> float:
    """
    Find square root using binary search.

    Args:
        n: Number to find square root of (non-negative)
        precision: Number of decimal places (0 for integer result)

    Returns:
        Square root of n

    Time Complexity: O(log n * precision)
    Space Complexity: O(1)

    Examples:
        >>> find_square_root(16)
        4.0
        >>> find_square_root(25)
        5.0
        >>> abs(find_square_root(10, 2) - 3.16) < 0.01
        True
    """
    if n < 0:
        raise ValueError("Cannot compute square root of negative number")

    if n == 0 or n == 1:
        return float(n)

    # Integer part
    left, right = 0, n
    result = 0

    while left <= right:
        mid = left + (right - left) // 2

        if mid * mid == n:
            result = mid
            break
        elif mid * mid < n:
            result = mid
            left = mid + 1
        else:
            right = mid - 1

    if precision == 0:
        return float(result)

    # Decimal part
    increment = 0.1
    for _ in range(precision):
        while result * result <= n:
            result += increment
        result -= increment
        increment /= 10

    return result


def nth_root(n: float, root: int, epsilon: float = 1e-9) -> float:
    """
    Find nth root using binary search.

    Args:
        n: Number to find root of
        root: Which root to find (e.g., 2 for square root, 3 for cube root)
        epsilon: Precision threshold

    Returns:
        nth root of n

    Examples:
        >>> abs(nth_root(27, 3) - 3.0) < 1e-6
        True
        >>> abs(nth_root(16, 4) - 2.0) < 1e-6
        True
    """
    if n < 0 and root % 2 == 0:
        raise ValueError("Cannot compute even root of negative number")

    if n == 0:
        return 0.0

    negative = n < 0
    n = abs(n)

    left, right = 0.0, max(1.0, n)

    while right - left > epsilon:
        mid = (left + right) / 2
        value = mid ** root

        if abs(value - n) < epsilon:
            return -mid if negative else mid
        elif value < n:
            left = mid
        else:
            right = mid

    result = (left + right) / 2
    return -result if negative else result


# ==============================================================================
# 8. ADVANCED BINARY SEARCH UTILITIES
# ==============================================================================

def binary_search_insert_position(arr: List[T], target: T) -> int:
    """
    Find the index where target should be inserted to maintain sorted order.

    Args:
        arr: Sorted list
        target: Element to insert

    Returns:
        Index where target should be inserted

    Time Complexity: O(log n)

    Examples:
        >>> binary_search_insert_position([1, 3, 5, 6], 5)
        2
        >>> binary_search_insert_position([1, 3, 5, 6], 2)
        1
        >>> binary_search_insert_position([1, 3, 5, 6], 7)
        4
    """
    left, right = 0, len(arr)

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left


def binary_search_range(arr: List[T], target: T) -> Tuple[int, int]:
    """
    Find the range [start, end] of target in sorted array.

    Args:
        arr: Sorted list (may contain duplicates)
        target: Element to search for

    Returns:
        Tuple of (first_index, last_index), (-1, -1) if not found

    Examples:
        >>> binary_search_range([5, 7, 7, 8, 8, 10], 8)
        (3, 4)
        >>> binary_search_range([5, 7, 7, 8, 8, 10], 6)
        (-1, -1)
    """
    first = find_first_occurrence(arr, target)
    if first == -1:
        return (-1, -1)

    last = find_last_occurrence(arr, target)
    return (first, last)


def binary_search_closest(arr: List[int], target: int) -> int:
    """
    Find the element closest to target in sorted array.

    Args:
        arr: Sorted list of integers
        target: Target value

    Returns:
        Index of closest element

    Examples:
        >>> arr = [1, 3, 5, 7, 9]
        >>> binary_search_closest(arr, 6)
        2
        >>> binary_search_closest(arr, 4)
        1
    """
    if not arr:
        return -1

    if len(arr) == 1:
        return 0

    left, right = 0, len(arr) - 1

    # If target is outside the array range
    if target <= arr[left]:
        return left
    if target >= arr[right]:
        return right

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid

    # Compare left and left-1 to find closest
    if left > 0 and abs(arr[left - 1] - target) < abs(arr[left] - target):
        return left - 1

    return left


# ==============================================================================
# DEMONSTRATION AND TESTING
# ==============================================================================

def demonstrate_all_variants():
    """Demonstrate all binary search variants with examples."""

    print("=" * 70)
    print("BINARY SEARCH ALGORITHM COLLECTION - PYTHON")
    print("=" * 70)

    # 1. Classic Binary Search
    print("\n1. CLASSIC BINARY SEARCH")
    print("-" * 50)
    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    targets = [7, 10, 1, 19]

    for target in targets:
        idx_iter = binary_search_iterative(arr, target)
        idx_rec = binary_search_recursive(arr, target)
        print(f"Search {target:2d}: Iterative={idx_iter:2d}, Recursive={idx_rec:2d}")

    # 2. First/Last Occurrence
    print("\n2. FIRST/LAST OCCURRENCE")
    print("-" * 50)
    arr_dup = [1, 2, 2, 2, 3, 4, 4, 4, 4, 5]
    for target in [2, 4, 6]:
        first = find_first_occurrence(arr_dup, target)
        last = find_last_occurrence(arr_dup, target)
        count = count_occurrences(arr_dup, target)
        print(f"Target {target}: First={first:2d}, Last={last:2d}, Count={count}")

    # 3. Rotated Array Search
    print("\n3. ROTATED ARRAY SEARCH")
    print("-" * 50)
    rotated = [4, 5, 6, 7, 0, 1, 2]
    rotation_point = find_rotation_point(rotated)
    print(f"Rotated array: {rotated}")
    print(f"Rotation point: {rotation_point} (value: {rotated[rotation_point]})")

    for target in [0, 3, 6]:
        idx = search_rotated_array(rotated, target)
        print(f"Search {target}: Index={idx}")

    # 4. Exponential Search
    print("\n4. EXPONENTIAL SEARCH")
    print("-" * 50)
    large_arr = list(range(1, 101, 2))  # [1, 3, 5, ..., 99]
    for target in [15, 51, 99]:
        idx = exponential_search(large_arr, target)
        print(f"Search {target:2d} in array of size {len(large_arr)}: Index={idx}")

    # 5. Interpolation Search
    print("\n5. INTERPOLATION SEARCH")
    print("-" * 50)
    uniform_arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for target in [30, 75, 100]:
        idx = interpolation_search(uniform_arr, target)
        print(f"Search {target:3d}: Index={idx}")

    # 6. Ternary Search
    print("\n6. TERNARY SEARCH")
    print("-" * 50)
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for target in [5, 1, 10, 11]:
        idx = ternary_search(arr, target)
        print(f"Search {target:2d}: Index={idx}")

    # Unimodal function
    func = lambda x: -(x - 5) ** 2 + 25  # Peak at x=5
    max_x = ternary_search_maximum(func, 0, 10)
    print(f"Maximum of -(x-5)² + 25 at x ≈ {max_x:.6f}")

    # 7. Binary Search on Answer
    print("\n7. BINARY SEARCH ON ANSWER")
    print("-" * 50)

    # Square root examples
    for n in [16, 25, 50, 100]:
        sqrt = find_square_root(n, precision=2)
        print(f"√{n:3d} ≈ {sqrt:.2f}")

    # Cube root
    cube_root = nth_root(27, 3)
    print(f"∛27 ≈ {cube_root:.6f}")

    # 8. Advanced Utilities
    print("\n8. ADVANCED UTILITIES")
    print("-" * 50)
    arr = [1, 3, 5, 6, 8, 10]

    for target in [2, 5, 11]:
        pos = binary_search_insert_position(arr, target)
        print(f"Insert position for {target:2d}: {pos}")

    arr_closest = [1, 3, 5, 7, 9]
    for target in [4, 6, 8]:
        idx = binary_search_closest(arr_closest, target)
        print(f"Closest to {target}: Index={idx}, Value={arr_closest[idx]}")

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


def run_performance_tests():
    """Run performance benchmarks on different search algorithms."""
    import time
    import random

    print("\n" + "=" * 70)
    print("PERFORMANCE BENCHMARKS")
    print("=" * 70)

    sizes = [1000, 10000, 100000]

    for size in sizes:
        print(f"\nArray size: {size:,}")
        print("-" * 50)

        # Generate sorted array
        arr = sorted([random.randint(1, size * 10) for _ in range(size)])
        targets = [arr[random.randint(0, size - 1)] for _ in range(100)]

        # Binary Search (Iterative)
        start = time.perf_counter()
        for target in targets:
            binary_search_iterative(arr, target)
        time_binary_iter = (time.perf_counter() - start) * 1000

        # Binary Search (Recursive)
        start = time.perf_counter()
        for target in targets:
            binary_search_recursive(arr, target)
        time_binary_rec = (time.perf_counter() - start) * 1000

        # Exponential Search
        start = time.perf_counter()
        for target in targets:
            exponential_search(arr, target)
        time_exponential = (time.perf_counter() - start) * 1000

        # Interpolation Search
        start = time.perf_counter()
        for target in targets:
            interpolation_search(arr, target)
        time_interpolation = (time.perf_counter() - start) * 1000

        # Ternary Search
        start = time.perf_counter()
        for target in targets:
            ternary_search(arr, target)
        time_ternary = (time.perf_counter() - start) * 1000

        print(f"Binary (Iterative):    {time_binary_iter:8.3f} ms")
        print(f"Binary (Recursive):    {time_binary_rec:8.3f} ms")
        print(f"Exponential Search:    {time_exponential:8.3f} ms")
        print(f"Interpolation Search:  {time_interpolation:8.3f} ms")
        print(f"Ternary Search:        {time_ternary:8.3f} ms")


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_all_variants()

    # Run performance tests
    run_performance_tests()

    # Run doctests
    print("\n" + "=" * 70)
    print("RUNNING DOCTESTS")
    print("=" * 70)
    import doctest
    results = doctest.testmod(verbose=False)
    print(f"Doctests: {results.attempted} tests, {results.failed} failures")

    if results.failed == 0:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed!")
