"""
Sublinear Search Algorithms Implementation

INTERPOLATION SEARCH:
Time Complexity: O(log log n) average, O(n) worst case
Space Complexity: O(1)

WHEN TO USE INTERPOLATION SEARCH OVER BINARY SEARCH:
1. For uniformly distributed sorted data
2. When data values correlate with their positions
3. For large datasets where log log n improvement matters
4. When you can estimate target position from value

ADVANTAGES:
- O(log log n) for uniformly distributed data (better than binary's O(log n))
- Fewer iterations needed for well-distributed data
- Natural for datasets like phone books, dictionaries

DISADVANTAGES:
- Poor performance (O(n)) for non-uniform data
- Requires numeric data or comparable values
- Vulnerable to data distribution

EXPONENTIAL SEARCH:
Time Complexity: O(log n)
Space Complexity: O(1)

WHEN TO USE EXPONENTIAL SEARCH:
1. For unbounded or infinite arrays
2. When target is likely near the beginning
3. For sorted linked lists (better than binary search)
4. When array size is unknown

ADVANTAGES:
- Works with unbounded arrays
- Better than binary search when target is near start
- Only searches relevant portion of array
- Good for unknown array sizes

PERFORMANCE ON DIFFERENT DATA DISTRIBUTIONS:
- Uniform data: Interpolation search excels
- Clustered data: Exponential search better
- Unknown size: Exponential search only option
- Small arrays: Binary search often faster due to simplicity
"""

from typing import List, Optional


def interpolation_search(arr: List[int], target: int) -> int:
    """
    Interpolation search - estimates position based on value.
    Best for uniformly distributed data.

    Args:
        arr: Sorted list of integers
        target: Value to search for

    Returns:
        Index of target if found, -1 otherwise
    """
    left, right = 0, len(arr) - 1

    while left <= right and arr[left] <= target <= arr[right]:
        # If the range has only one element
        if left == right:
            if arr[left] == target:
                return left
            return -1

        # Estimate position using interpolation formula
        # pos = left + ((target - arr[left]) / (arr[right] - arr[left])) * (right - left)
        range_val = arr[right] - arr[left]
        if range_val == 0:
            if arr[left] == target:
                return left
            return -1

        pos = left + int(((target - arr[left]) * (right - left)) / range_val)

        # Ensure pos is within bounds
        pos = max(left, min(pos, right))

        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            left = pos + 1
        else:
            right = pos - 1

    return -1


def interpolation_search_robust(arr: List[int], target: int) -> int:
    """
    Robust interpolation search with safeguards against poor data distribution.
    Falls back to binary search behavior when interpolation overshoots.

    Args:
        arr: Sorted list of integers
        target: Value to search for

    Returns:
        Index of target if found, -1 otherwise
    """
    left, right = 0, len(arr) - 1
    iterations = 0
    max_iterations = 64  # Safeguard against worst-case

    while left <= right and arr[left] <= target <= arr[right]:
        iterations += 1

        # Fall back to binary search if too many iterations
        if iterations > max_iterations:
            mid = left + (right - left) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
            continue

        if left == right:
            if arr[left] == target:
                return left
            return -1

        # Interpolation formula with overflow protection
        range_val = arr[right] - arr[left]
        if range_val == 0:
            if arr[left] == target:
                return left
            return -1

        # Use floating point for more accurate interpolation
        ratio = (target - arr[left]) / range_val
        pos = left + int(ratio * (right - left))

        # Bounds checking
        pos = max(left, min(pos, right))

        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            left = pos + 1
        else:
            right = pos - 1

    return -1


def exponential_search(arr: List[int], target: int) -> int:
    """
    Exponential search - finds range then applies binary search.
    Excellent for unbounded arrays or when target is near start.

    Args:
        arr: Sorted list of integers
        target: Value to search for

    Returns:
        Index of target if found, -1 otherwise
    """
    n = len(arr)
    if n == 0:
        return -1

    # Check if first element is the target
    if arr[0] == target:
        return 0

    # Find range for binary search by repeated doubling
    bound = 1
    while bound < n and arr[bound] < target:
        bound *= 2

    # Perform binary search in the found range
    left = bound // 2
    right = min(bound, n - 1)

    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def exponential_search_unbounded(arr: List[int], target: int, size_hint: Optional[int] = None) -> int:
    """
    Exponential search optimized for unbounded arrays.
    Useful when array size is unknown or very large.

    Args:
        arr: Sorted list of integers (may be very large)
        target: Value to search for
        size_hint: Optional hint about array size for optimization

    Returns:
        Index of target if found, -1 otherwise
    """
    if len(arr) == 0:
        return -1

    if arr[0] == target:
        return 0

    # Exponentially increase bound
    bound = 1
    max_bound = size_hint if size_hint else float('inf')

    while bound < len(arr) and bound < max_bound:
        if arr[bound] >= target:
            break
        bound *= 2

    # Binary search in the range [bound//2, min(bound, len(arr)-1)]
    left = bound // 2
    right = min(bound, len(arr) - 1)

    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def adaptive_search(arr: List[int], target: int) -> int:
    """
    Adaptive search that chooses between interpolation and binary search
    based on data distribution assessment.

    Args:
        arr: Sorted list of integers
        target: Value to search for

    Returns:
        Index of target if found, -1 otherwise
    """
    n = len(arr)
    if n == 0:
        return -1

    # Sample the array to assess distribution uniformity
    if n > 100:
        samples = 10
        sample_indices = [i * n // samples for i in range(samples)]
        differences = []

        for i in range(len(sample_indices) - 1):
            idx1, idx2 = sample_indices[i], sample_indices[i + 1]
            value_diff = arr[idx2] - arr[idx1]
            index_diff = idx2 - idx1
            if index_diff > 0:
                differences.append(value_diff / index_diff)

        # Calculate coefficient of variation
        if differences:
            mean_diff = sum(differences) / len(differences)
            if mean_diff > 0:
                variance = sum((d - mean_diff) ** 2 for d in differences) / len(differences)
                cv = (variance ** 0.5) / mean_diff

                # If distribution is uniform (low CV), use interpolation
                if cv < 0.5:
                    return interpolation_search_robust(arr, target)

    # Otherwise use binary search
    left, right = 0, n - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


# Performance testing and demonstration
if __name__ == "__main__":
    import time
    import random

    # Test correctness
    test_arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]
    print("Test Array:", test_arr)
    print(f"Interpolation Search for 15: Index {interpolation_search(test_arr, 15)}")
    print(f"Interpolation Search for 20: Index {interpolation_search(test_arr, 20)}")
    print(f"Exponential Search for 15: Index {exponential_search(test_arr, 15)}")
    print(f"Exponential Search for 1: Index {exponential_search(test_arr, 1)}")

    # Performance comparison on uniform data
    print("\n--- Performance on Uniform Data ---")
    sizes = [10000, 100000, 1000000]

    for size in sizes:
        # Uniform distribution
        arr = list(range(0, size * 10, 10))
        target = random.choice(arr)

        # Interpolation search
        start = time.perf_counter()
        for _ in range(1000):
            interpolation_search(arr, target)
        interp_time = time.perf_counter() - start

        # Binary search (for comparison)
        start = time.perf_counter()
        for _ in range(1000):
            import bisect
            bisect.bisect_left(arr, target)
        binary_time = time.perf_counter() - start

        # Exponential search
        start = time.perf_counter()
        for _ in range(1000):
            exponential_search(arr, target)
        exp_time = time.perf_counter() - start

        print(f"\nArray size: {size:,}")
        print(f"Interpolation Search: {interp_time*1000:.3f}ms")
        print(f"Binary Search: {binary_time*1000:.3f}ms")
        print(f"Exponential Search: {exp_time*1000:.3f}ms")
        print(f"Ratio (Interp/Binary): {interp_time/binary_time:.2f}x")
        print(f"Ratio (Exp/Binary): {exp_time/binary_time:.2f}x")

    # Performance on non-uniform data (clustered)
    print("\n--- Performance on Clustered Data ---")
    arr_clustered = []
    for i in range(100):
        arr_clustered.extend([i * 1000] * 100)  # Clusters of same values
    arr_clustered.sort()
    target = arr_clustered[len(arr_clustered) // 2]

    start = time.perf_counter()
    for _ in range(1000):
        interpolation_search(arr_clustered, target)
    interp_clustered = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(1000):
        import bisect
        bisect.bisect_left(arr_clustered, target)
    binary_clustered = time.perf_counter() - start

    print(f"Interpolation Search: {interp_clustered*1000:.3f}ms")
    print(f"Binary Search: {binary_clustered*1000:.3f}ms")
    print(f"Ratio (Interp/Binary): {interp_clustered/binary_clustered:.2f}x")
    print("(Note: Interpolation performs poorly on non-uniform data)")

    # Exponential search on targets near beginning
    print("\n--- Exponential Search: Target Near Beginning ---")
    arr_large = list(range(1000000))

    for target_pos in [10, 100, 1000, 10000]:
        target = arr_large[target_pos]

        start = time.perf_counter()
        for _ in range(1000):
            exponential_search(arr_large, target)
        exp_time = time.perf_counter() - start

        start = time.perf_counter()
        for _ in range(1000):
            import bisect
            bisect.bisect_left(arr_large, target)
        binary_time = time.perf_counter() - start

        print(f"\nTarget at index {target_pos}:")
        print(f"Exponential Search: {exp_time*1000:.3f}ms")
        print(f"Binary Search: {binary_time*1000:.3f}ms")
        print(f"Ratio (Exp/Binary): {exp_time/binary_time:.2f}x")
