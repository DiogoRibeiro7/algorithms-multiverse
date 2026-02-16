#!/usr/bin/env python3
"""
Segment Tree Implementation

A Segment Tree is a binary tree data structure used for storing intervals or segments.
It allows querying which stored segments contain a given point efficiently.
It's particularly useful for range queries and range updates.

Key Features:
- Efficient range queries (sum, min, max, GCD, etc.)
- Efficient point/range updates
- Lazy propagation for range updates
- Space-efficient compared to 2D arrays for range queries

Time Complexity:
- Build: O(n)
- Query: O(log n)
- Update (point): O(log n)
- Update (range with lazy): O(log n)
- Space: O(n)

Applications:
- Range sum/min/max queries
- Computational geometry (line segment intersection)
- Database systems (interval queries)
- Competitive programming problems
- Graphics rendering (finding visible segments)

Author: Algorithms Multiverse
License: MIT
"""

from typing import List, Optional, Callable, Any, Union, Tuple
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from enum import Enum


class QueryType(Enum):
    """Types of range queries supported"""
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    GCD = "gcd"
    XOR = "xor"
    PRODUCT = "product"


class SegmentTree:
    """
    Segment Tree for range queries and updates

    Generic implementation supporting various operations through custom functions.

    Attributes:
        n: Size of the input array
        tree: Internal tree representation (array-based)
        lazy: Lazy propagation array for range updates
        operation: Binary operation for combining segments
        default_value: Identity element for the operation
        query_type: Type of query operation
    """

    def __init__(self, arr: List[Union[int, float]],
                 query_type: QueryType = QueryType.SUM):
        """
        Initialize Segment Tree from array

        Args:
            arr: Input array
            query_type: Type of range query operation
        """
        self.n = len(arr)
        self.query_type = query_type

        # Set operation and default value based on query type
        self._set_operation(query_type)

        # Calculate tree size (next power of 2)
        tree_size = 2 * (2 ** math.ceil(math.log2(self.n))) - 1
        self.tree = [self.default_value] * tree_size
        self.lazy = [0] * tree_size  # For lazy propagation

        # Build the tree
        if arr:
            self._build(arr, 0, 0, self.n - 1)

    def _set_operation(self, query_type: QueryType):
        """Set operation function and default value based on query type"""
        if query_type == QueryType.SUM:
            self.operation = lambda a, b: a + b
            self.default_value = 0
        elif query_type == QueryType.MIN:
            self.operation = min
            self.default_value = float('inf')
        elif query_type == QueryType.MAX:
            self.operation = max
            self.default_value = float('-inf')
        elif query_type == QueryType.GCD:
            import math
            self.operation = math.gcd
            self.default_value = 0
        elif query_type == QueryType.XOR:
            self.operation = lambda a, b: a ^ b
            self.default_value = 0
        elif query_type == QueryType.PRODUCT:
            self.operation = lambda a, b: a * b
            self.default_value = 1
        else:
            raise ValueError(f"Unsupported query type: {query_type}")

    def _build(self, arr: List[Union[int, float]], node: int,
               start: int, end: int):
        """
        Build the segment tree recursively

        Args:
            arr: Input array
            node: Current node index in tree
            start: Start index of segment
            end: End index of segment
        """
        if start == end:
            # Leaf node
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2

            # Recursively build left and right subtrees
            self._build(arr, left_child, start, mid)
            self._build(arr, right_child, mid + 1, end)

            # Combine children values
            self.tree[node] = self.operation(self.tree[left_child],
                                            self.tree[right_child])

    def query(self, left: int, right: int) -> Union[int, float]:
        """
        Query range [left, right] inclusive

        Args:
            left: Left boundary of range
            right: Right boundary of range

        Returns:
            Result of operation over the range
        """
        if left < 0 or right >= self.n or left > right:
            raise ValueError(f"Invalid range: [{left}, {right}]")

        return self._query_recursive(0, 0, self.n - 1, left, right)

    def _query_recursive(self, node: int, start: int, end: int,
                        query_left: int, query_right: int) -> Union[int, float]:
        """
        Recursively query the segment tree

        Args:
            node: Current node index
            start: Start of node's segment
            end: End of node's segment
            query_left: Left boundary of query
            query_right: Right boundary of query

        Returns:
            Query result
        """
        # Handle lazy propagation
        if self.lazy[node] != 0:
            self._apply_lazy(node, start, end)

        # No overlap
        if start > query_right or end < query_left:
            return self.default_value

        # Complete overlap
        if start >= query_left and end <= query_right:
            return self.tree[node]

        # Partial overlap - query both children
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2

        left_result = self._query_recursive(left_child, start, mid,
                                           query_left, query_right)
        right_result = self._query_recursive(right_child, mid + 1, end,
                                            query_left, query_right)

        return self.operation(left_result, right_result)

    def update_point(self, index: int, value: Union[int, float]):
        """
        Update single element at index

        Args:
            index: Index to update
            value: New value
        """
        if index < 0 or index >= self.n:
            raise ValueError(f"Index {index} out of bounds")

        self._update_point_recursive(0, 0, self.n - 1, index, value)

    def _update_point_recursive(self, node: int, start: int, end: int,
                               index: int, value: Union[int, float]):
        """
        Recursively update a single point

        Args:
            node: Current node index
            start: Start of segment
            end: End of segment
            index: Index to update
            value: New value
        """
        if start == end:
            # Leaf node
            self.tree[node] = value
            return

        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2

        if index <= mid:
            self._update_point_recursive(left_child, start, mid, index, value)
        else:
            self._update_point_recursive(right_child, mid + 1, end, index, value)

        # Update parent
        self.tree[node] = self.operation(self.tree[left_child],
                                        self.tree[right_child])

    def update_range(self, left: int, right: int, value: Union[int, float]):
        """
        Update range [left, right] with lazy propagation

        Args:
            left: Left boundary
            right: Right boundary
            value: Value to add/set (depends on operation)
        """
        if left < 0 or right >= self.n or left > right:
            raise ValueError(f"Invalid range: [{left}, {right}]")

        self._update_range_recursive(0, 0, self.n - 1, left, right, value)

    def _update_range_recursive(self, node: int, start: int, end: int,
                               update_left: int, update_right: int,
                               value: Union[int, float]):
        """
        Recursively update a range with lazy propagation

        Args:
            node: Current node
            start: Start of segment
            end: End of segment
            update_left: Left boundary of update
            update_right: Right boundary of update
            value: Update value
        """
        # Apply pending updates
        if self.lazy[node] != 0:
            self._apply_lazy(node, start, end)

        # No overlap
        if start > update_right or end < update_left:
            return

        # Complete overlap - lazy propagation
        if start >= update_left and end <= update_right:
            if self.query_type == QueryType.SUM:
                self.tree[node] += value * (end - start + 1)
            else:
                # For MIN/MAX, just update the value
                self.tree[node] = value

            # Mark children for lazy update
            if start != end:
                left_child = 2 * node + 1
                right_child = 2 * node + 2
                self.lazy[left_child] += value
                self.lazy[right_child] += value
            return

        # Partial overlap
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2

        self._update_range_recursive(left_child, start, mid,
                                    update_left, update_right, value)
        self._update_range_recursive(right_child, mid + 1, end,
                                    update_left, update_right, value)

        # Update parent
        self.tree[node] = self.operation(self.tree[left_child],
                                        self.tree[right_child])

    def _apply_lazy(self, node: int, start: int, end: int):
        """Apply lazy propagation to node"""
        if self.query_type == QueryType.SUM:
            self.tree[node] += self.lazy[node] * (end - start + 1)
        else:
            self.tree[node] += self.lazy[node]

        # Propagate to children
        if start != end:
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            self.lazy[left_child] += self.lazy[node]
            self.lazy[right_child] += self.lazy[node]

        self.lazy[node] = 0

    def visualize(self, highlight_range: Optional[Tuple[int, int]] = None):
        """
        Visualize the segment tree structure

        Args:
            highlight_range: Optional range to highlight
        """
        if self.n == 0:
            print("Empty tree")
            return

        fig, ax = plt.subplots(1, 1, figsize=(14, 8))
        ax.set_title(f"Segment Tree ({self.query_type.value} queries)")
        ax.axis('off')

        # Calculate tree levels
        levels = math.ceil(math.log2(self.n)) + 1
        positions = {}

        # Position nodes
        self._calculate_positions(0, 0, self.n - 1, positions, 0, 0, 1, levels)

        # Draw edges
        self._draw_edges(0, 0, self.n - 1, positions, ax)

        # Draw nodes
        self._draw_nodes(0, 0, self.n - 1, positions, ax, highlight_range)

        plt.tight_layout()
        plt.show()

    def _calculate_positions(self, node: int, start: int, end: int,
                            positions: dict, level: int,
                            left_bound: float, right_bound: float,
                            max_level: int):
        """Calculate node positions for visualization"""
        mid_x = (left_bound + right_bound) / 2
        y = 1 - (level / max_level)
        positions[(node, start, end)] = (mid_x, y)

        if start != end:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2

            self._calculate_positions(left_child, start, mid, positions,
                                    level + 1, left_bound, mid_x, max_level)
            self._calculate_positions(right_child, mid + 1, end, positions,
                                    level + 1, mid_x, right_bound, max_level)

    def _draw_edges(self, node: int, start: int, end: int,
                   positions: dict, ax):
        """Draw edges in the tree"""
        if start == end:
            return

        x1, y1 = positions[(node, start, end)]
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2

        # Draw edge to left child
        x2, y2 = positions[(left_child, start, mid)]
        ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1)
        self._draw_edges(left_child, start, mid, positions, ax)

        # Draw edge to right child
        x2, y2 = positions[(right_child, mid + 1, end)]
        ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1)
        self._draw_edges(right_child, mid + 1, end, positions, ax)

    def _draw_nodes(self, node: int, start: int, end: int,
                   positions: dict, ax, highlight_range: Optional[Tuple[int, int]]):
        """Draw nodes with labels"""
        x, y = positions[(node, start, end)]

        # Determine node color
        color = 'lightblue'
        if highlight_range:
            h_left, h_right = highlight_range
            if start >= h_left and end <= h_right:
                color = 'lightgreen'  # Complete overlap
            elif not (start > h_right or end < h_left):
                color = 'yellow'  # Partial overlap

        # Draw node
        if start == end:
            # Leaf node - rectangular
            rect = patches.Rectangle((x - 0.03, y - 0.02), 0.06, 0.04,
                                    color=color, ec='black', linewidth=1)
            ax.add_patch(rect)
        else:
            # Internal node - circular
            circle = patches.Circle((x, y), 0.025, color=color,
                                  ec='black', linewidth=1)
            ax.add_patch(circle)

        # Add labels
        ax.text(x, y, f"{self.tree[node]:.0f}" if self.tree[node] != self.default_value else "∞",
                ha='center', va='center', fontsize=8, fontweight='bold')
        ax.text(x, y - 0.04, f"[{start},{end}]",
                ha='center', va='center', fontsize=6, color='gray')

        # Recursive drawing
        if start != end:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            self._draw_nodes(left_child, start, mid, positions, ax, highlight_range)
            self._draw_nodes(right_child, mid + 1, end, positions, ax, highlight_range)


class LazySegmentTree(SegmentTree):
    """
    Segment Tree with enhanced lazy propagation support

    Extends basic segment tree with more sophisticated lazy propagation
    for efficient range updates.
    """

    def __init__(self, arr: List[Union[int, float]],
                 query_type: QueryType = QueryType.SUM):
        """Initialize lazy segment tree"""
        super().__init__(arr, query_type)
        self.lazy_set = [None] * len(self.lazy)  # For range set operations

    def set_range(self, left: int, right: int, value: Union[int, float]):
        """
        Set all elements in range to a specific value

        Args:
            left: Left boundary
            right: Right boundary
            value: Value to set
        """
        self._set_range_recursive(0, 0, self.n - 1, left, right, value)

    def _set_range_recursive(self, node: int, start: int, end: int,
                            update_left: int, update_right: int,
                            value: Union[int, float]):
        """Recursively set range values"""
        # Apply pending updates
        self._apply_lazy_set(node, start, end)

        # No overlap
        if start > update_right or end < update_left:
            return

        # Complete overlap
        if start >= update_left and end <= update_right:
            self.lazy_set[node] = value
            self._apply_lazy_set(node, start, end)
            return

        # Partial overlap
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2

        self._set_range_recursive(left_child, start, mid,
                                 update_left, update_right, value)
        self._set_range_recursive(right_child, mid + 1, end,
                                 update_left, update_right, value)

        # Update parent
        self.tree[node] = self.operation(self.tree[left_child],
                                        self.tree[right_child])

    def _apply_lazy_set(self, node: int, start: int, end: int):
        """Apply lazy set operation"""
        if self.lazy_set[node] is not None:
            if self.query_type == QueryType.SUM:
                self.tree[node] = self.lazy_set[node] * (end - start + 1)
            else:
                self.tree[node] = self.lazy_set[node]

            # Propagate to children
            if start != end:
                left_child = 2 * node + 1
                right_child = 2 * node + 2
                self.lazy_set[left_child] = self.lazy_set[node]
                self.lazy_set[right_child] = self.lazy_set[node]
                # Clear add lazy since we're setting
                self.lazy[left_child] = 0
                self.lazy[right_child] = 0

            self.lazy_set[node] = None


def demonstrate_segment_tree():
    """Demonstrate segment tree operations"""
    print("=" * 60)
    print("Segment Tree Demonstration")
    print("=" * 60)

    # Create array
    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    print(f"\nOriginal array: {arr}")

    # Test different query types
    for query_type in [QueryType.SUM, QueryType.MIN, QueryType.MAX]:
        print(f"\n{'-' * 40}")
        print(f"Query Type: {query_type.value}")
        print(f"{'-' * 40}")

        st = SegmentTree(arr, query_type)

        # Range queries
        test_ranges = [(0, 3), (2, 5), (0, 7), (4, 4)]
        for left, right in test_ranges:
            result = st.query(left, right)
            print(f"Query [{left}, {right}]: {result}")

        # Point update
        st.update_point(3, 10)
        print(f"\nAfter updating index 3 to 10:")
        result = st.query(0, 7)
        print(f"Query [0, 7]: {result}")

        # Visualize
        if query_type == QueryType.SUM:
            st.visualize(highlight_range=(2, 5))


def demonstrate_lazy_propagation():
    """Demonstrate lazy propagation for range updates"""
    print("\n" + "=" * 60)
    print("Lazy Propagation Demonstration")
    print("=" * 60)

    arr = [1, 2, 3, 4, 5, 6, 7, 8]
    print(f"\nOriginal array: {arr}")

    lst = LazySegmentTree(arr, QueryType.SUM)

    # Initial sum
    print(f"Initial sum [0, 7]: {lst.query(0, 7)}")

    # Range update
    lst.update_range(2, 5, 10)
    print(f"\nAfter adding 10 to range [2, 5]:")
    print(f"Sum [0, 7]: {lst.query(0, 7)}")
    print(f"Sum [2, 5]: {lst.query(2, 5)}")

    # Range set
    lst.set_range(3, 6, 100)
    print(f"\nAfter setting range [3, 6] to 100:")
    print(f"Sum [0, 7]: {lst.query(0, 7)}")
    print(f"Sum [3, 6]: {lst.query(3, 6)}")


def benchmark_segment_tree():
    """Benchmark segment tree vs naive approach"""
    print("\n" + "=" * 60)
    print("Performance Benchmark")
    print("=" * 60)

    import time
    import random

    n = 10000
    arr = [random.randint(1, 100) for _ in range(n)]
    queries = [(random.randint(0, n-100), random.randint(0, n-100) + random.randint(1, 99))
               for _ in range(1000)]
    # Fix invalid ranges
    queries = [(min(a, b), max(a, b)) for a, b in queries if a < n and b < n]

    # Segment Tree approach
    st = SegmentTree(arr, QueryType.SUM)

    start = time.time()
    st_results = [st.query(l, r) for l, r in queries]
    st_time = time.time() - start

    # Naive approach
    start = time.time()
    naive_results = [sum(arr[l:r+1]) for l, r in queries]
    naive_time = time.time() - start

    print(f"\nArray size: {n}")
    print(f"Number of queries: {len(queries)}")
    print(f"\nSegment Tree time: {st_time:.4f} seconds")
    print(f"Naive approach time: {naive_time:.4f} seconds")
    print(f"Speedup: {naive_time/st_time:.2f}x")

    # Verify correctness
    assert st_results == naive_results, "Results don't match!"
    print("\n✓ Results verified correct")


def application_example_skyline():
    """Example application: Skyline problem using segment tree"""
    print("\n" + "=" * 60)
    print("Application: Skyline Problem")
    print("=" * 60)

    # Buildings: (left, right, height)
    buildings = [(2, 9, 10), (3, 7, 15), (5, 12, 12), (15, 20, 10), (19, 24, 8)]
    print("\nBuildings (left, right, height):")
    for b in buildings:
        print(f"  {b}")

    # Find the range of coordinates
    max_coord = max(b[1] for b in buildings) + 1
    heights = [0] * max_coord

    # Use segment tree to track maximum height at each point
    st = LazySegmentTree(heights, QueryType.MAX)

    # Process each building
    for left, right, height in buildings:
        for i in range(left, right):
            current = st.query(i, i)
            if height > current:
                st.update_point(i, height)

    # Extract skyline
    print("\nSkyline heights:")
    skyline = []
    prev_height = 0
    for i in range(max_coord):
        height = st.query(i, i)
        if height != prev_height:
            skyline.append((i, height))
            prev_height = height

    for point in skyline:
        print(f"  x={point[0]}: height={point[1]}")

    # Visualize skyline
    plt.figure(figsize=(12, 6))
    for left, right, height in buildings:
        plt.plot([left, left, right, right], [0, height, height, 0], 'b-', alpha=0.3)
        plt.fill_between([left, right], [0, 0], [height, height], alpha=0.1)

    # Draw skyline
    x_coords = [0]
    y_coords = [0]
    for x, h in skyline:
        x_coords.extend([x, x])
        y_coords.extend([y_coords[-1], h])
    x_coords.append(max_coord)
    y_coords.append(0)

    plt.plot(x_coords, y_coords, 'r-', linewidth=2, label='Skyline')
    plt.xlabel('X Coordinate')
    plt.ylabel('Height')
    plt.title('Skyline Problem Solution')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_segment_tree()
    demonstrate_lazy_propagation()
    benchmark_segment_tree()
    application_example_skyline()

    print("\n" + "=" * 60)
    print("Segment Tree Implementation Complete!")
    print("=" * 60)