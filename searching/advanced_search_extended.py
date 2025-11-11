"""
Extended Advanced Search Algorithms - Python
============================================

Additional advanced search algorithms including:
1. Approximate String Matching (Fuzzy Search)
   - Levenshtein distance-based search
   - Hamming distance search
   - Fuzzy matching with tolerance
   - Phonetic matching (Soundex, Metaphone)

2. Geometric Search Algorithms
   - KD-Tree for multidimensional search
   - Range Trees for orthogonal range queries
   - Nearest neighbor search
   - Range queries

3. Specialized Search Algorithms
   - Two-pointer technique
   - Sliding window search
   - Galloping search

Performance Focus:
- Space-partitioning data structures
- Cache-friendly geometric algorithms
- Approximate matching with configurable tolerance
- Efficient nearest neighbor queries

Time Complexity varies by algorithm (documented per function)
"""

import math
from typing import List, Tuple, Optional, Callable, Any
from dataclasses import dataclass
from collections import deque
import heapq


# ==============================================================================
# 1. APPROXIMATE STRING MATCHING (FUZZY SEARCH)
# ==============================================================================

def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate Levenshtein (edit) distance between two strings.

    The minimum number of single-character edits (insertions, deletions,
    substitutions) required to change one string into another.

    Time: O(m * n), Space: O(min(m, n))

    Args:
        s1, s2: Strings to compare

    Returns:
        Edit distance
    """
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    if not s2:
        return len(s1)

    # Use two rows for space optimization
    prev_row = list(range(len(s2) + 1))
    curr_row = [0] * (len(s2) + 1)

    for i, c1 in enumerate(s1):
        curr_row[0] = i + 1

        for j, c2 in enumerate(s2):
            # Cost of substitution
            cost = 0 if c1 == c2 else 1

            curr_row[j + 1] = min(
                prev_row[j + 1] + 1,      # Deletion
                curr_row[j] + 1,           # Insertion
                prev_row[j] + cost         # Substitution
            )

        prev_row, curr_row = curr_row, prev_row

    return prev_row[-1]


def fuzzy_search(text: str, pattern: str, max_distance: int = 2) -> List[Tuple[int, int]]:
    """
    Find all approximate matches of pattern in text.

    Uses sliding window with Levenshtein distance to find matches
    within specified edit distance.

    Time: O(n * m * k) where k is pattern length
    Space: O(m)

    WHEN TO USE:
    - Spell checking
    - DNA sequence matching with mutations
    - Searching with typos
    - Flexible text search

    Args:
        text: Text to search in
        pattern: Pattern to find
        max_distance: Maximum edit distance allowed

    Returns:
        List of (start, end) positions with distance <= max_distance

    Examples:
        >>> fuzzy_search("hello world", "helo", max_distance=1)
        [(0, 5)]
    """
    matches = []
    pattern_len = len(pattern)
    text_len = len(text)

    # Try all possible windows in text
    for i in range(text_len - pattern_len + max_distance + 1):
        # Try different window sizes (pattern_len ± max_distance)
        for window_size in range(
            max(1, pattern_len - max_distance),
            min(text_len - i + 1, pattern_len + max_distance + 1)
        ):
            window = text[i:i + window_size]
            distance = levenshtein_distance(pattern, window)

            if distance <= max_distance:
                matches.append((i, i + window_size))
                break  # Found match at this position

    return matches


def hamming_distance(s1: str, s2: str) -> Optional[int]:
    """
    Calculate Hamming distance (number of positions with different characters).

    Only works for strings of equal length.

    Time: O(n), Space: O(1)

    Args:
        s1, s2: Strings to compare (must be equal length)

    Returns:
        Number of differing positions, or None if lengths differ
    """
    if len(s1) != len(s2):
        return None

    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def fuzzy_search_hamming(text: str, pattern: str, max_distance: int = 1) -> List[int]:
    """
    Find approximate matches using Hamming distance (fixed-length windows).

    Faster than Levenshtein for fixed-length patterns.

    Time: O(n * m), Space: O(1)

    Args:
        text: Text to search in
        pattern: Pattern to find
        max_distance: Maximum Hamming distance allowed

    Returns:
        List of starting positions of matches
    """
    matches = []
    pattern_len = len(pattern)

    for i in range(len(text) - pattern_len + 1):
        window = text[i:i + pattern_len]
        distance = hamming_distance(pattern, window)

        if distance is not None and distance <= max_distance:
            matches.append(i)

    return matches


def soundex(name: str) -> str:
    """
    Generate Soundex code for phonetic matching.

    Soundex is a phonetic algorithm for indexing names by sound.
    Useful for matching names that sound similar but are spelled differently.

    Time: O(n), Space: O(1)

    Args:
        name: Name to encode

    Returns:
        4-character Soundex code

    Examples:
        >>> soundex("Robert")
        'R163'
        >>> soundex("Rupert")
        'R163'
    """
    if not name:
        return "0000"

    # Soundex mapping
    soundex_map = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6'
    }

    name = name.upper()
    code = name[0]  # Keep first letter
    prev_digit = soundex_map.get(name[0], '0')

    for char in name[1:]:
        if len(code) >= 4:
            break

        digit = soundex_map.get(char, '0')

        # Skip vowels and duplicates
        if digit != '0' and digit != prev_digit:
            code += digit
            prev_digit = digit
        elif digit == '0':
            prev_digit = '0'

    # Pad with zeros
    return (code + '000')[:4]


def phonetic_search(names: List[str], query: str) -> List[str]:
    """
    Find phonetically similar names using Soundex.

    Time: O(n * m) where m is average name length
    Space: O(n)

    Args:
        names: List of names to search
        query: Name to search for

    Returns:
        List of names that sound similar to query
    """
    query_code = soundex(query)
    return [name for name in names if soundex(name) == query_code]


# ==============================================================================
# 2. GEOMETRIC SEARCH - KD-TREE
# ==============================================================================

@dataclass
class KDNode:
    """Node in a KD-Tree."""
    point: List[float]
    left: Optional['KDNode'] = None
    right: Optional['KDNode'] = None
    axis: int = 0


class KDTree:
    """
    KD-Tree for efficient multidimensional search.

    A space-partitioning data structure for organizing points in k-dimensional space.

    Time Complexity:
    - Build: O(n log n)
    - Search: O(log n) average, O(n) worst
    - Nearest neighbor: O(log n) average
    - Range query: O(n^(1-1/k) + m) where m is result size

    Space: O(n)

    WHEN TO USE:
    - Nearest neighbor search in multiple dimensions
    - Range queries in 2D/3D space
    - Geographic information systems (GIS)
    - Computer graphics (ray tracing, collision detection)
    - Machine learning (k-NN classification)

    ADVANTAGES:
    - Efficient for moderate dimensions (k ≤ 20)
    - Balanced tree gives O(log n) search
    - Space efficient

    DISADVANTAGES:
    - Performance degrades in high dimensions (curse of dimensionality)
    - Building can be expensive
    - Not dynamic-friendly (insertions/deletions require rebalancing)
    """

    def __init__(self, points: List[List[float]]):
        """
        Build KD-Tree from points.

        Args:
            points: List of k-dimensional points
        """
        self.k = len(points[0]) if points else 0
        self.root = self._build(points, 0)

    def _build(self, points: List[List[float]], depth: int) -> Optional[KDNode]:
        """Recursively build KD-Tree."""
        if not points:
            return None

        axis = depth % self.k

        # Sort points by current axis and choose median
        points.sort(key=lambda p: p[axis])
        median = len(points) // 2

        return KDNode(
            point=points[median],
            axis=axis,
            left=self._build(points[:median], depth + 1),
            right=self._build(points[median + 1:], depth + 1)
        )

    def nearest_neighbor(self, query: List[float]) -> Tuple[List[float], float]:
        """
        Find nearest neighbor to query point.

        Time: O(log n) average, O(n) worst

        Args:
            query: Query point

        Returns:
            Tuple of (nearest_point, distance)
        """
        best = [None, float('inf')]  # [point, distance]

        def search(node: Optional[KDNode], depth: int = 0):
            if node is None:
                return

            # Calculate distance to current point
            dist = self._distance(query, node.point)

            if dist < best[1]:
                best[0] = node.point
                best[1] = dist

            axis = depth % self.k
            diff = query[axis] - node.point[axis]

            # Decide which subtree to search first
            if diff < 0:
                near, far = node.left, node.right
            else:
                near, far = node.right, node.left

            # Search near subtree
            search(near, depth + 1)

            # Check if we need to search far subtree
            if abs(diff) < best[1]:
                search(far, depth + 1)

        search(self.root)
        return best[0], best[1]

    def range_query(self, lower: List[float], upper: List[float]) -> List[List[float]]:
        """
        Find all points within rectangular range.

        Time: O(n^(1-1/k) + m) where m is result size

        Args:
            lower: Lower bounds for each dimension
            upper: Upper bounds for each dimension

        Returns:
            List of points in range
        """
        results = []

        def search(node: Optional[KDNode]):
            if node is None:
                return

            # Check if point is in range
            if all(lower[i] <= node.point[i] <= upper[i] for i in range(self.k)):
                results.append(node.point)

            # Check if we need to search left subtree
            if lower[node.axis] <= node.point[node.axis]:
                search(node.left)

            # Check if we need to search right subtree
            if upper[node.axis] >= node.point[node.axis]:
                search(node.right)

        search(self.root)
        return results

    def k_nearest_neighbors(self, query: List[float], k: int) -> List[Tuple[List[float], float]]:
        """
        Find k nearest neighbors to query point.

        Time: O(k log n) average

        Args:
            query: Query point
            k: Number of neighbors

        Returns:
            List of (point, distance) tuples, sorted by distance
        """
        heap = []  # Max heap of k nearest

        def search(node: Optional[KDNode], depth: int = 0):
            if node is None:
                return

            dist = self._distance(query, node.point)

            if len(heap) < k:
                heapq.heappush(heap, (-dist, node.point))
            elif dist < -heap[0][0]:
                heapq.heapreplace(heap, (-dist, node.point))

            axis = depth % self.k
            diff = query[axis] - node.point[axis]

            # Search order
            if diff < 0:
                near, far = node.left, node.right
            else:
                near, far = node.right, node.left

            search(near, depth + 1)

            # Check if we need to search far subtree
            if len(heap) < k or abs(diff) < -heap[0][0]:
                search(far, depth + 1)

        search(self.root)

        # Convert to min heap and return
        return [(point, -dist) for dist, point in sorted(heap, reverse=True)]

    @staticmethod
    def _distance(p1: List[float], p2: List[float]) -> float:
        """Euclidean distance between two points."""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


# ==============================================================================
# 3. RANGE TREE (1D Range Query)
# ==============================================================================

class RangeTree:
    """
    Range Tree for efficient 1D range queries on sorted data.

    Augmented balanced BST that stores additional information
    for efficient range queries.

    Time Complexity:
    - Build: O(n log n)
    - Range query: O(log n + k) where k is result size
    - Point query: O(log n)

    Space: O(n)

    WHEN TO USE:
    - Frequent range queries on static data
    - Database range queries
    - Time series analysis
    - Coordinate-based queries

    Note: For higher dimensions, use layered range trees (more complex)
    """

    def __init__(self, values: List[float]):
        """
        Build range tree from values.

        Args:
            values: Sorted or unsorted list of values
        """
        self.values = sorted(values)
        self.n = len(values)

    def range_query(self, low: float, high: float) -> List[float]:
        """
        Find all values in range [low, high].

        Uses binary search for boundaries.

        Time: O(log n + k) where k is result size

        Args:
            low: Lower bound (inclusive)
            high: Upper bound (inclusive)

        Returns:
            List of values in range
        """
        # Binary search for lower bound
        left = self._lower_bound(low)
        # Binary search for upper bound
        right = self._upper_bound(high)

        return self.values[left:right + 1]

    def _lower_bound(self, target: float) -> int:
        """Find first index where value >= target."""
        left, right = 0, self.n

        while left < right:
            mid = (left + right) // 2
            if self.values[mid] < target:
                left = mid + 1
            else:
                right = mid

        return left

    def _upper_bound(self, target: float) -> int:
        """Find last index where value <= target."""
        left, right = -1, self.n - 1

        while left < right:
            mid = (left + right + 1) // 2
            if self.values[mid] <= target:
                left = mid
            else:
                right = mid - 1

        return right

    def count_range(self, low: float, high: float) -> int:
        """
        Count values in range [low, high].

        Time: O(log n)
        """
        left = self._lower_bound(low)
        right = self._upper_bound(high)
        return max(0, right - left + 1)


# ==============================================================================
# 4. SPECIALIZED SEARCH ALGORITHMS
# ==============================================================================

def two_pointer_search(arr: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Two-pointer technique to find pair that sums to target.

    Useful for finding pairs, triplets, or ranges satisfying conditions.

    Time: O(n), Space: O(1)

    WHEN TO USE:
    - Finding pairs with specific sum
    - Container with most water problems
    - Trapping rain water
    - Partitioning problems

    Args:
        arr: Sorted array
        target: Target sum

    Returns:
        Tuple of (left_index, right_index) or None

    Examples:
        >>> two_pointer_search([1, 2, 3, 4, 5, 6], 9)
        (2, 5)
    """
    left, right = 0, len(arr) - 1

    while left < right:
        current_sum = arr[left] + arr[right]

        if current_sum == target:
            return (left, right)
        elif current_sum < target:
            left += 1
        else:
            right -= 1

    return None


def galloping_search(arr: List[int], target: int) -> int:
    """
    Galloping (exponential) search with exponentially increasing steps.

    Similar to exponential search but with adaptive step size.
    Very efficient when target is near the beginning.

    Time: O(log i) where i is position of target
    Space: O(1)

    WHEN TO USE:
    - Target expected near beginning of array
    - Merging sorted sequences
    - When you have hint about target location

    Args:
        arr: Sorted array
        target: Element to find

    Returns:
        Index of target or -1
    """
    if not arr or arr[0] > target:
        return -1

    if arr[0] == target:
        return 0

    # Galloping phase - find range
    bound = 1
    while bound < len(arr) and arr[bound] < target:
        bound *= 2

    # Binary search in range [bound//2, min(bound, len-1)]
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


def sliding_window_search(arr: List[int], window_size: int,
                          condition: Callable[[List[int]], bool]) -> List[int]:
    """
    Sliding window search for subarrays satisfying a condition.

    Efficient for finding subarrays/substrings with specific properties.

    Time: O(n), Space: O(k) where k is window size

    WHEN TO USE:
    - Finding subarrays with specific sum
    - Longest substring problems
    - Maximum/minimum in sliding windows
    - Pattern matching in sequences

    Args:
        arr: Input array
        window_size: Size of sliding window
        condition: Function to test window

    Returns:
        List of starting indices where condition is true
    """
    results = []

    for i in range(len(arr) - window_size + 1):
        window = arr[i:i + window_size]
        if condition(window):
            results.append(i)

    return results


# ==============================================================================
# EXAMPLES AND TESTING
# ==============================================================================

def example_fuzzy_search():
    print("=" * 70)
    print("EXAMPLE 1: Fuzzy String Matching")
    print("=" * 70)

    text = "The quick brown fox jumps over the lazy dog"

    # Levenshtein-based fuzzy search
    matches = fuzzy_search(text, "quik", max_distance=1)
    print(f"Text: '{text}'")
    print(f"Fuzzy search for 'quik' (max distance=1): {matches}")
    for start, end in matches:
        print(f"  Found: '{text[start:end]}' at position {start}")

    # Hamming-based search
    matches = fuzzy_search_hamming(text, "quick", max_distance=1)
    print(f"\nHamming search for 'quick' (max distance=1): {matches}")

    # Phonetic search
    names = ["Robert", "Rupert", "Rubin", "Robin", "Rebecca", "Roger"]
    similar = phonetic_search(names, "Robert")
    print(f"\nPhonetic search for 'Robert': {similar}")
    print()


def example_kdtree():
    print("=" * 70)
    print("EXAMPLE 2: KD-Tree Geometric Search")
    print("=" * 70)

    # 2D points
    points = [
        [2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]
    ]

    tree = KDTree(points)

    # Nearest neighbor
    query = [6, 3]
    nearest, dist = tree.nearest_neighbor(query)
    print(f"Points: {points}")
    print(f"Nearest to {query}: {nearest} (distance: {dist:.2f})")

    # K nearest neighbors
    k_nearest = tree.k_nearest_neighbors(query, k=3)
    print(f"\n3 nearest neighbors to {query}:")
    for point, dist in k_nearest:
        print(f"  {point} (distance: {dist:.2f})")

    # Range query
    lower, upper = [3, 2], [8, 7]
    in_range = tree.range_query(lower, upper)
    print(f"\nPoints in range {lower} to {upper}: {in_range}")
    print()


def example_range_tree():
    print("=" * 70)
    print("EXAMPLE 3: Range Tree Queries")
    print("=" * 70)

    values = [1, 5, 3, 8, 2, 9, 4, 7, 6]
    tree = RangeTree(values)

    print(f"Values: {sorted(values)}")

    # Range query
    result = tree.range_query(3, 7)
    print(f"Values in range [3, 7]: {result}")

    # Count in range
    count = tree.count_range(3, 7)
    print(f"Count in range [3, 7]: {count}")
    print()


def example_specialized():
    print("=" * 70)
    print("EXAMPLE 4: Specialized Search Algorithms")
    print("=" * 70)

    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Two-pointer search
    result = two_pointer_search(arr, 15)
    if result:
        i, j = result
        print(f"Two-pointer: {arr[i]} + {arr[j]} = 15")

    # Galloping search
    idx = galloping_search(arr, 7)
    print(f"Galloping search for 7: index {idx}")

    # Sliding window
    windows = sliding_window_search(arr, 3, lambda w: sum(w) > 15)
    print(f"Windows of size 3 with sum > 15: {windows}")
    print()


if __name__ == "__main__":
    print("=" * 70)
    print("EXTENDED ADVANCED SEARCH ALGORITHMS")
    print("=" * 70)
    print()

    example_fuzzy_search()
    example_kdtree()
    example_range_tree()
    example_specialized()

    print("=" * 70)
    print("All examples completed!")
    print("=" * 70)
