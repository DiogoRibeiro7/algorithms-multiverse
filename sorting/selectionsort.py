"""
Selection Sort Algorithm - Educational Implementation

ALGORITHM OVERVIEW:
==================
Selection Sort works by repeatedly finding the minimum element from the unsorted
portion of the array and placing it at the beginning. It divides the array into
two parts: a sorted portion (left) and an unsorted portion (right).

Time Complexity:
- Best Case: O(n²) - Even if array is already sorted, still searches for minimum
- Average Case: O(n²)
- Worst Case: O(n²)
- IMPORTANT: Unlike bubble sort and insertion sort, selection sort ALWAYS performs
  O(n²) comparisons, regardless of input

Space Complexity: O(1) - Sorts in-place with only constant extra space

Stability: NOT stable by default (can be made stable with modifications)
In-place: YES

WHEN TO USE SELECTION SORT:
==========================
1. When memory writes are expensive (minimizes number of swaps)
   - Only performs O(n) swaps, compared to O(n²) for bubble sort
2. When checking for all elements is not a problem
3. For small arrays where simplicity matters more than efficiency
4. Educational purposes - very simple to understand and implement

COMPARISON WITH OTHER O(n²) ALGORITHMS:
======================================
Selection Sort vs Bubble Sort:
- Selection: O(n) swaps, O(n²) comparisons, NOT adaptive
- Bubble: O(n²) swaps, O(n²) comparisons, IS adaptive (O(n) best case)

Selection Sort vs Insertion Sort:
- Selection: O(n) swaps, O(n²) comparisons always, NOT adaptive
- Insertion: O(n²) swaps, O(n²) comparisons worst, IS adaptive (O(n) best case)

Key Advantage: Selection sort makes MINIMUM number of swaps among all comparison sorts!
"""

from typing import List, TypeVar, Callable, Tuple, Optional
import time
import random

T = TypeVar('T')


# ============================================================================
# STANDARD SELECTION SORT
# ============================================================================

def selection_sort(arr: List[T]) -> List[T]:
    """
    Standard selection sort implementation.

    ALGORITHM STEPS:
    ===============
    1. Find the minimum element in the unsorted portion
    2. Swap it with the first element of the unsorted portion
    3. Move the boundary of sorted/unsorted portions one element to the right
    4. Repeat until the entire array is sorted

    Visual Example:
    ==============
    Initial: [64, 25, 12, 22, 11]

    Pass 1: Find min in [64, 25, 12, 22, 11] → 11
            Swap 64 ↔ 11
            Result: [11, 25, 12, 22, 64]
                     ^^^ sorted portion

    Pass 2: Find min in [25, 12, 22, 64] → 12
            Swap 25 ↔ 12
            Result: [11, 12, 25, 22, 64]
                     ^^^^^^^ sorted portion

    Pass 3: Find min in [25, 22, 64] → 22
            Swap 25 ↔ 22
            Result: [11, 12, 22, 25, 64]
                     ^^^^^^^^^^^ sorted portion

    Pass 4: Find min in [25, 64] → 25
            No swap needed
            Result: [11, 12, 22, 25, 64]
                     ^^^^^^^^^^^^^^^ sorted portion

    Time: O(n²), Space: O(n) for new array
    """
    if len(arr) <= 1:
        return arr.copy()

    result = arr.copy()
    selection_sort_in_place(result)
    return result


def selection_sort_in_place(arr: List[T]) -> None:
    """
    In-place selection sort implementation.

    Sorts the array in-place, modifying the original array.

    DETAILED STEP-BY-STEP:
    ======================
    For each position i from 0 to n-1:
        - Assume arr[i] is the minimum
        - Scan all elements from i+1 to n-1
        - Track the index of the actual minimum element
        - After scanning, swap arr[i] with the minimum element found

    Time: O(n²), Space: O(1)
    """
    n = len(arr)

    # Outer loop: Move boundary of unsorted subarray one by one
    for i in range(n - 1):
        # Find the minimum element in the remaining unsorted array
        # Start by assuming the first unsorted element is the minimum
        min_idx = i

        # Inner loop: Search for the minimum in arr[i+1...n-1]
        for j in range(i + 1, n):
            # If we find a smaller element, update min_idx
            if arr[j] < arr[min_idx]:
                min_idx = j

        # Swap the found minimum element with the first element
        # of the unsorted portion
        # Note: This swap happens even if min_idx == i (no-op swap)
        # This is one reason selection sort is not stable
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]


# ============================================================================
# BIDIRECTIONAL SELECTION SORT
# ============================================================================

def bidirectional_selection_sort(arr: List[T]) -> List[T]:
    """
    Bidirectional selection sort (also called "double selection sort").

    OPTIMIZATION:
    ============
    Instead of finding just the minimum in each pass, we find BOTH the minimum
    and maximum elements. We place the minimum at the beginning and the maximum
    at the end, reducing the number of passes by approximately half.

    Algorithm:
    - Find both min and max in the unsorted portion
    - Place min at the left boundary
    - Place max at the right boundary
    - Move both boundaries inward

    Visual Example:
    ==============
    Initial: [64, 25, 12, 22, 11, 90, 88]

    Pass 1: Find min=11, max=90 in [64, 25, 12, 22, 11, 90, 88]
            Swap: 64 ↔ 11 (min to front), 90 stays
            Result: [11, 25, 12, 22, 64, 88, 90]
                     ^^                      ^^ sorted

    Pass 2: Find min=12, max=88 in [25, 12, 22, 64, 88]
            Swap: 25 ↔ 12 (min to front), 88 stays
            Result: [11, 12, 22, 25, 64, 88, 90]
                     ^^^^^^              ^^^^^^ sorted

    Pass 3: Find min=22, max=64 in [22, 25, 64]
            22 stays, swap: 64 ↔ 25? No, 64 already at right
            Result: [11, 12, 22, 25, 64, 88, 90]
                     ^^^^^^^^^^      ^^^^^^^^^^ sorted

    Time: Still O(n²), but approximately 2x faster in practice
    Space: O(n) for new array
    """
    if len(arr) <= 1:
        return arr.copy()

    result = arr.copy()
    n = len(result)

    # Process from both ends toward the middle
    left = 0
    right = n - 1

    while left < right:
        # Find both minimum and maximum in the current range
        min_idx = left
        max_idx = left

        for i in range(left, right + 1):
            if result[i] < result[min_idx]:
                min_idx = i
            if result[i] > result[max_idx]:
                max_idx = i

        # Special case: if min_idx == right, we need to swap it first
        # Otherwise, when we swap max_idx to right, we might move the min
        if min_idx == right:
            result[left], result[right] = result[right], result[left]
            if max_idx == left:
                max_idx = right
        else:
            # Swap minimum to the left boundary
            if min_idx != left:
                result[left], result[min_idx] = result[min_idx], result[left]

            # If maximum was at left position, it's now at min_idx
            if max_idx == left:
                max_idx = min_idx

            # Swap maximum to the right boundary
            if max_idx != right:
                result[right], result[max_idx] = result[max_idx], result[right]

        # Move boundaries inward
        left += 1
        right -= 1

    return result


# ============================================================================
# RECURSIVE SELECTION SORT
# ============================================================================

def selection_sort_recursive(arr: List[T]) -> List[T]:
    """
    Recursive implementation of selection sort.

    RECURSIVE APPROACH:
    ==================
    Base case: Array of size 0 or 1 is already sorted
    Recursive case:
        1. Find the minimum element in the array
        2. Swap it with the first element
        3. Recursively sort the rest of the array (excluding the first element)

    Example:
    ========
    selection_sort_recursive([64, 25, 12, 22, 11])
        → Find min=11, swap with 64
        → [11] + selection_sort_recursive([25, 12, 22, 64])
            → Find min=12, swap with 25
            → [11, 12] + selection_sort_recursive([25, 22, 64])
                → Find min=22, swap with 25
                → [11, 12, 22] + selection_sort_recursive([25, 64])
                    → Find min=25, no swap
                    → [11, 12, 22, 25] + selection_sort_recursive([64])
                        → Base case: [64]
                        → Return [64]
                    → Return [11, 12, 22, 25, 64]

    Time: O(n²), Space: O(n) for recursion stack + O(n) for new array
    """
    if len(arr) <= 1:
        return arr.copy()

    result = arr.copy()
    _selection_sort_recursive_helper(result, 0)
    return result


def _selection_sort_recursive_helper(arr: List[T], start_idx: int) -> None:
    """Helper function for recursive selection sort."""
    # Base case: if we've reached the end, we're done
    if start_idx >= len(arr) - 1:
        return

    # Find the minimum element in arr[start_idx...n-1]
    min_idx = start_idx
    for i in range(start_idx + 1, len(arr)):
        if arr[i] < arr[min_idx]:
            min_idx = i

    # Swap the minimum with the element at start_idx
    if min_idx != start_idx:
        arr[start_idx], arr[min_idx] = arr[min_idx], arr[start_idx]

    # Recursively sort the rest
    _selection_sort_recursive_helper(arr, start_idx + 1)


# ============================================================================
# STABLE SELECTION SORT
# ============================================================================

def stable_selection_sort(arr: List[T]) -> List[T]:
    """
    Stable version of selection sort.

    WHY STANDARD SELECTION SORT IS UNSTABLE:
    ========================================
    When we swap the minimum element with the first element of the unsorted
    portion, we can change the relative order of equal elements.

    Example showing instability:
    Input:  [4a, 5, 3, 2, 4b]  (a and b are just markers, both are 4)
    Pass 1: Find min=2, swap with 4a → [2, 5, 3, 4a, 4b]
    Pass 2: Find min=3, swap with 5  → [2, 3, 5, 4a, 4b]
    Pass 3: Find min=4a, swap with 5 → [2, 3, 4a, 5, 4b]
    Pass 4: Find min=4b, swap with 5 → [2, 3, 4a, 4b, 5]
    Result: 4a comes before 4b ✓ (stable in this case)

    But with: [4a, 2, 4b, 3]
    Pass 1: Swap 4a ↔ 2 → [2, 4a, 4b, 3]
    Pass 2: Swap 4a ↔ 3? No, 3 is min → [2, 3, 4b, 4a]
    Result: 4b comes before 4a ✗ (unstable!)

    MAKING IT STABLE:
    ================
    Instead of swapping, we shift all elements and insert the minimum
    at the correct position. This preserves the relative order.

    Time: O(n²) comparisons + O(n²) shifts
    Space: O(n)
    """
    if len(arr) <= 1:
        return arr.copy()

    result = arr.copy()
    n = len(result)

    for i in range(n - 1):
        # Find minimum in unsorted portion
        min_idx = i
        for j in range(i + 1, n):
            if result[j] < result[min_idx]:
                min_idx = j

        # Instead of swapping, shift elements and insert
        if min_idx != i:
            min_value = result[min_idx]
            # Shift all elements between i and min_idx one position right
            for k in range(min_idx, i, -1):
                result[k] = result[k - 1]
            # Place minimum at position i
            result[i] = min_value

    return result


# ============================================================================
# VISUALIZATION AND STATISTICS
# ============================================================================

class SortStatistics:
    """Tracks sorting operations for analysis."""

    def __init__(self):
        self.comparisons = 0
        self.swaps = 0
        self.array_accesses = 0

    def reset(self):
        self.comparisons = 0
        self.swaps = 0
        self.array_accesses = 0

    def __str__(self):
        return f"Comparisons: {self.comparisons}, Swaps: {self.swaps}, Array Accesses: {self.array_accesses}"


def selection_sort_with_stats(arr: List[T], stats: SortStatistics) -> List[T]:
    """Selection sort with operation counting."""
    stats.reset()
    if len(arr) <= 1:
        return arr.copy()

    result = arr.copy()
    n = len(result)

    for i in range(n - 1):
        min_idx = i
        stats.array_accesses += 1

        for j in range(i + 1, n):
            stats.comparisons += 1
            stats.array_accesses += 2  # Read result[j] and result[min_idx]
            if result[j] < result[min_idx]:
                min_idx = j

        if min_idx != i:
            stats.swaps += 1
            stats.array_accesses += 4  # Two reads, two writes
            result[i], result[min_idx] = result[min_idx], result[i]

    return result


def visualize_selection_sort(arr: List[int]) -> List[str]:
    """
    Create ASCII visualization of selection sort process.

    Shows each step with visual markers for:
    - Sorted portion (marked with ✓)
    - Current minimum being found (marked with *)
    - Element being compared (marked with ?)
    """
    steps = []
    result = arr.copy()
    n = len(result)

    steps.append("=" * 70)
    steps.append("SELECTION SORT VISUALIZATION")
    steps.append("=" * 70)
    steps.append(f"Initial array: {result}")
    steps.append("")

    for i in range(n - 1):
        steps.append(f"Pass {i + 1}:")
        steps.append(f"  Looking for minimum in unsorted portion: {result[i:]}")

        min_idx = i
        min_value = result[i]

        # Show the search process
        for j in range(i + 1, n):
            if result[j] < min_value:
                min_idx = j
                min_value = result[j]
                steps.append(f"    Found new minimum: {min_value} at index {min_idx}")

        # Show the swap
        if min_idx != i:
            steps.append(f"  Swapping {result[i]} ↔ {result[min_idx]}")
            result[i], result[min_idx] = result[min_idx], result[i]
        else:
            steps.append(f"  No swap needed (minimum already in place)")

        # Show current state
        sorted_part = result[:i + 1]
        unsorted_part = result[i + 1:]
        steps.append(f"  Sorted: {sorted_part} | Unsorted: {unsorted_part}")
        steps.append("")

    steps.append(f"Final sorted array: {result}")
    steps.append("=" * 70)

    return steps


def draw_array_bars(arr: List[int], highlight_indices: Optional[List[int]] = None) -> str:
    """
    Create a bar chart visualization of the array.

    Example output:
        ████
        ████
        ████ ████
        ████ ████ ████
    """
    if not arr:
        return ""

    highlight_indices = highlight_indices or []
    max_val = max(arr)
    max_height = 10

    # Normalize values to fit in max_height
    normalized = [int((val / max_val) * max_height) for val in arr]

    lines = []
    for height in range(max_height, 0, -1):
        line = ""
        for i, val in enumerate(normalized):
            if val >= height:
                if i in highlight_indices:
                    line += "▓▓ "
                else:
                    line += "██ "
            else:
                line += "   "
        lines.append(line)

    # Add values at bottom
    value_line = ""
    for val in arr:
        value_line += f"{val:2d} "
    lines.append(value_line)

    return "\n".join(lines)


# ============================================================================
# COMPARISON WITH OTHER O(n²) ALGORITHMS
# ============================================================================

def compare_quadratic_sorts(arr: List[int]) -> dict:
    """
    Compare selection sort with other O(n²) algorithms.

    Returns statistics for:
    - Selection Sort
    - Bubble Sort
    - Insertion Sort
    """
    results = {}

    # Selection Sort
    stats_selection = SortStatistics()
    selection_sort_with_stats(arr, stats_selection)
    results['Selection Sort'] = {
        'comparisons': stats_selection.comparisons,
        'swaps': stats_selection.swaps,
        'array_accesses': stats_selection.array_accesses
    }

    # Bubble Sort (for comparison)
    def bubble_sort_with_stats(arr, stats):
        stats.reset()
        result = arr.copy()
        n = len(result)
        for i in range(n):
            swapped = False
            for j in range(n - i - 1):
                stats.comparisons += 1
                stats.array_accesses += 2
                if result[j] > result[j + 1]:
                    stats.swaps += 1
                    stats.array_accesses += 4
                    result[j], result[j + 1] = result[j + 1], result[j]
                    swapped = True
            if not swapped:
                break
        return result

    stats_bubble = SortStatistics()
    bubble_sort_with_stats(arr, stats_bubble)
    results['Bubble Sort'] = {
        'comparisons': stats_bubble.comparisons,
        'swaps': stats_bubble.swaps,
        'array_accesses': stats_bubble.array_accesses
    }

    # Insertion Sort (for comparison)
    def insertion_sort_with_stats(arr, stats):
        stats.reset()
        result = arr.copy()
        n = len(result)
        for i in range(1, n):
            key = result[i]
            stats.array_accesses += 1
            j = i - 1
            while j >= 0:
                stats.comparisons += 1
                stats.array_accesses += 1
                if result[j] > key:
                    stats.swaps += 1
                    stats.array_accesses += 2
                    result[j + 1] = result[j]
                    j -= 1
                else:
                    break
            result[j + 1] = key
            stats.array_accesses += 1
        return result

    stats_insertion = SortStatistics()
    insertion_sort_with_stats(arr, stats_insertion)
    results['Insertion Sort'] = {
        'comparisons': stats_insertion.comparisons,
        'swaps': stats_insertion.swaps,
        'array_accesses': stats_insertion.array_accesses
    }

    return results


# ============================================================================
# DEMONSTRATIONS AND TESTING
# ============================================================================

def demonstrate_selection_sort():
    """Comprehensive demonstration of selection sort."""
    print("📚 SELECTION SORT - EDUCATIONAL DEMONSTRATION")
    print("=" * 80)

    # Test cases
    test_cases = [
        ([64, 25, 12, 22, 11], "Random array"),
        ([5, 2, 8, 6, 1, 9, 4], "Small random array"),
        ([1], "Single element"),
        ([], "Empty array"),
        ([3, 3, 3, 3, 3], "All duplicates"),
        ([9, 8, 7, 6, 5, 4, 3, 2, 1], "Reverse sorted"),
        ([1, 2, 3, 4, 5], "Already sorted"),
        ([1, 3, 2, 4, 5], "Nearly sorted"),
    ]

    print("\n📋 BASIC FUNCTIONALITY TESTS:")
    print("-" * 80)

    for arr, desc in test_cases:
        original = arr.copy()
        standard = selection_sort(arr)
        bidirectional = bidirectional_selection_sort(arr)
        recursive = selection_sort_recursive(arr)
        stable = stable_selection_sort(arr)

        print(f"\nTest: {desc}")
        print(f"Original:      {original}")
        print(f"Standard:      {standard}")
        print(f"Bidirectional: {bidirectional}")
        print(f"Recursive:     {recursive}")
        print(f"Stable:        {stable}")

        all_equal = (standard == bidirectional == recursive == stable == sorted(arr))
        status = "✓" if all_equal else "✗"
        print(f"All correct: {status}")

    # Visualization
    print("\n\n🎬 STEP-BY-STEP VISUALIZATION:")
    print("-" * 80)
    demo_arr = [64, 25, 12, 22, 11]
    steps = visualize_selection_sort(demo_arr)
    for step in steps:
        print(step)

    # Statistics comparison
    print("\n\n📊 ALGORITHM COMPARISON (O(n²) Algorithms):")
    print("-" * 80)

    comparison_cases = [
        ([5, 2, 8, 6, 1], "Random"),
        ([1, 2, 3, 4, 5], "Already sorted"),
        ([5, 4, 3, 2, 1], "Reverse sorted"),
    ]

    for arr, desc in comparison_cases:
        print(f"\n{desc}: {arr}")
        results = compare_quadratic_sorts(arr)

        print(f"{'Algorithm':<20} {'Comparisons':<15} {'Swaps':<15} {'Array Accesses':<15}")
        print("-" * 65)
        for algo, stats in results.items():
            print(f"{algo:<20} {stats['comparisons']:<15} {stats['swaps']:<15} {stats['array_accesses']:<15}")

        # Analysis
        sel_swaps = results['Selection Sort']['swaps']
        bub_swaps = results['Bubble Sort']['swaps']
        ins_swaps = results['Insertion Sort']['swaps']

        print(f"\n  Key Observation:")
        print(f"  - Selection Sort made {sel_swaps} swaps (minimum among all)")
        print(f"  - Bubble Sort made {bub_swaps} swaps")
        print(f"  - Insertion Sort made {ins_swaps} swaps")

    # Memory analysis
    print("\n\n💾 MEMORY USAGE ANALYSIS:")
    print("-" * 80)
    print("""
Selection Sort Memory Characteristics:

1. In-Place Sorting:
   - Space Complexity: O(1) auxiliary space
   - Only uses a constant amount of extra memory (min_idx, loop variables)
   - Original array is modified in-place

2. Comparison with Other Algorithms:
   Algorithm          Auxiliary Space
   -----------------------------------------
   Selection Sort     O(1)
   Bubble Sort        O(1)
   Insertion Sort     O(1)
   Merge Sort         O(n)
   Quick Sort         O(log n) average

3. Memory Writes:
   - Selection Sort: O(n) swaps (minimum writes)
   - Bubble Sort: O(n²) swaps in worst case
   - Insertion Sort: O(n²) shifts in worst case

   ⭐ This makes Selection Sort ideal when writing to memory is expensive!
      Examples: Flash memory, EEPROM, or distributed systems

4. Cache Performance:
   - Poor cache locality during the search for minimum
   - Each pass scans the entire unsorted portion
   - Comparison: Insertion sort has better cache performance
    """)

    # Use cases
    print("\n📌 WHEN TO USE SELECTION SORT:")
    print("-" * 80)
    print("""
✅ GOOD USE CASES:

1. Minimal Memory Writes:
   - Flash memory or EEPROM (limited write cycles)
   - Distributed systems where network writes are expensive
   - Example: Sorting data where swaps involve expensive disk I/O

2. Small Datasets:
   - When simplicity is more important than efficiency
   - Educational purposes to understand sorting concepts

3. Known Small Data:
   - Embedded systems with small, fixed-size arrays
   - When n is guaranteed to be small (< 20 elements)

4. Minimal Memory:
   - When O(1) auxiliary space is required
   - Cannot afford recursive call stack or temporary arrays

❌ POOR USE CASES:

1. Large Datasets:
   - Always O(n²) time, never adapts to input
   - Much slower than O(n log n) algorithms

2. Nearly Sorted Data:
   - Unlike insertion sort, doesn't benefit from sorted input
   - Still performs all O(n²) comparisons

3. Stable Sorting Required:
   - Standard selection sort is not stable
   - Making it stable adds overhead

4. Real-time Systems:
   - Non-adaptive nature means worst-case is always hit
   - Insertion sort or merge sort preferred
    """)


def performance_benchmark():
    """Benchmark selection sort performance."""
    print("\n\n⚡ PERFORMANCE BENCHMARK")
    print("=" * 80)

    sizes = [10, 20, 50, 100, 200, 500]

    patterns = {
        'Random': lambda n: [random.randint(1, 1000) for _ in range(n)],
        'Sorted': lambda n: list(range(n)),
        'Reversed': lambda n: list(range(n, 0, -1)),
        'Nearly Sorted': lambda n: list(range(n))[::-1][:n//10] + list(range(n))[n//10:],
    }

    for pattern_name, pattern_gen in patterns.items():
        print(f"\n{pattern_name} Data:")
        print(f"{'Size':<10} {'Standard':<15} {'Bidirectional':<15} {'Recursive':<15}")
        print("-" * 55)

        for size in sizes:
            test_data = pattern_gen(size)

            # Standard
            start = time.time()
            selection_sort(test_data)
            time_standard = (time.time() - start) * 1000

            # Bidirectional
            start = time.time()
            bidirectional_selection_sort(test_data)
            time_bidirectional = (time.time() - start) * 1000

            # Recursive
            start = time.time()
            selection_sort_recursive(test_data)
            time_recursive = (time.time() - start) * 1000

            print(f"{size:<10} {time_standard:>10.3f}ms {time_bidirectional:>10.3f}ms {time_recursive:>10.3f}ms")


if __name__ == "__main__":
    demonstrate_selection_sort()
    performance_benchmark()

    print("\n✨ Selection Sort demonstration complete!")
