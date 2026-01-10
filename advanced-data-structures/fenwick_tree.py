#!/usr/bin/env python3
"""
Fenwick Tree (Binary Indexed Tree) Implementation

A Fenwick Tree or Binary Indexed Tree (BIT) is a data structure that efficiently
supports prefix sum queries and point updates in logarithmic time. It uses a
clever indexing scheme based on binary representation of indices.

Key Concepts:
- Each node stores the sum of a range of elements
- Range size determined by the last set bit (LSB) in the index
- Parent-child relationship through bit manipulation
- Space-efficient: uses same space as input array

Time Complexity:
- Build: O(n log n) naive, O(n) optimized
- Point Update: O(log n)
- Prefix Sum Query: O(log n)
- Range Sum Query: O(log n)
- Space: O(n)

Applications:
- Cumulative frequency tables
- Computational geometry (2D range queries with 2D BIT)
- Inversion count in arrays
- Arithmetic coding for data compression
- Dynamic ranking/percentile queries
- Coordinate compression problems

Author: Algorithms Multiverse
License: MIT
"""

from typing import List, Optional, Tuple, Union
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle


class FenwickTree:
    """
    Fenwick Tree (Binary Indexed Tree) for efficient range sum queries

    Uses 1-based indexing internally for simpler bit operations.
    The key insight is that each index i is responsible for a range
    of size equal to the largest power of 2 that divides i.

    Attributes:
        n: Size of the array
        tree: Internal tree representation (1-indexed)
        original: Copy of original array for reference
    """

    def __init__(self, arr: List[Union[int, float]]):
        """
        Initialize Fenwick Tree from array

        Args:
            arr: Input array (0-indexed)
        """
        self.n = len(arr)
        self.tree = [0] * (self.n + 1)  # 1-indexed
        self.original = arr.copy()

        # Build tree
        for i, val in enumerate(arr):
            self.update(i, val)

    @staticmethod
    def _lsb(x: int) -> int:
        """
        Get the least significant bit (rightmost set bit)

        This represents the size of the range that index x is responsible for.

        Args:
            x: Index (1-based)

        Returns:
            Value of LSB
        """
        return x & (-x)

    def update(self, index: int, delta: Union[int, float]) -> None:
        """
        Add delta to element at index (0-based)

        Updates all nodes that include this index in their range.

        Args:
            index: Array index (0-based)
            delta: Value to add
        """
        # Convert to 1-based indexing
        index += 1

        # Update all affected nodes
        while index <= self.n:
            self.tree[index] += delta
            index += self._lsb(index)

    def set_value(self, index: int, value: Union[int, float]) -> None:
        """
        Set element at index to specific value

        Args:
            index: Array index (0-based)
            value: New value
        """
        delta = value - self.original[index]
        self.original[index] = value
        self.update(index, delta)

    def prefix_sum(self, index: int) -> Union[int, float]:
        """
        Get sum of elements from 0 to index (inclusive)

        Args:
            index: End index (0-based)

        Returns:
            Prefix sum
        """
        if index < 0:
            return 0

        # Convert to 1-based indexing
        index += 1
        result = 0

        # Sum all relevant nodes
        while index > 0:
            result += self.tree[index]
            index -= self._lsb(index)

        return result

    def range_sum(self, left: int, right: int) -> Union[int, float]:
        """
        Get sum of elements in range [left, right] (inclusive)

        Args:
            left: Start index (0-based)
            right: End index (0-based)

        Returns:
            Range sum
        """
        if left > 0:
            return self.prefix_sum(right) - self.prefix_sum(left - 1)
        else:
            return self.prefix_sum(right)

    def get_value(self, index: int) -> Union[int, float]:
        """
        Get single element value at index

        Args:
            index: Array index (0-based)

        Returns:
            Element value
        """
        return self.range_sum(index, index)

    def find_kth_smallest(self, k: int) -> Optional[int]:
        """
        Find index of kth smallest element (for cumulative frequency)

        Works when tree represents cumulative frequencies.

        Args:
            k: k-th element to find (1-based)

        Returns:
            Index of kth smallest element or None if k > total
        """
        if k <= 0:
            return None

        # Binary search on the tree
        pos = 0
        bit_mask = 1
        while bit_mask <= self.n:
            bit_mask <<= 1
        bit_mask >>= 1

        while bit_mask > 0:
            if pos + bit_mask <= self.n and self.tree[pos + bit_mask] < k:
                pos += bit_mask
                k -= self.tree[pos]
            bit_mask >>= 1

        if k > 0:
            return pos  # Convert to 0-based
        return None

    def visualize(self, highlight_index: Optional[int] = None):
        """
        Visualize the Fenwick Tree structure and responsibilities

        Args:
            highlight_index: Optional index to highlight
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

        # Top plot: Tree structure
        ax1.set_title("Fenwick Tree Structure", fontsize=14, fontweight='bold')
        ax1.set_xlim(-0.5, self.n + 0.5)
        ax1.set_ylim(-1, 3)
        ax1.set_xlabel("Index (1-based)")
        ax1.set_ylabel("Level")

        # Draw nodes and their responsibilities
        for i in range(1, self.n + 1):
            lsb = self._lsb(i)
            level = 0
            temp = i
            while temp & 1 == 0:
                level += 1
                temp >>= 1

            # Node
            color = 'red' if highlight_index and i == highlight_index + 1 else 'lightblue'
            circle = plt.Circle((i, level), 0.3, color=color, ec='black')
            ax1.add_patch(circle)

            # Value
            ax1.text(i, level, f"{self.tree[i]:.0f}", ha='center', va='center',
                    fontweight='bold')

            # Responsibility range
            start = i - lsb + 1
            ax1.plot([start, i], [level - 0.4, level - 0.4], 'g-', linewidth=2)
            ax1.text((start + i) / 2, level - 0.6, f"[{start},{i}]",
                    ha='center', fontsize=8, color='green')

            # Parent connection
            if i + lsb <= self.n:
                parent_level = 0
                temp = i + lsb
                while temp & 1 == 0:
                    parent_level += 1
                    temp >>= 1
                ax1.plot([i, i + lsb], [level + 0.3, parent_level - 0.3],
                        'b--', alpha=0.5)

        ax1.grid(True, alpha=0.3)
        ax1.set_xticks(range(1, self.n + 1))

        # Bottom plot: Array representation
        ax2.set_title("Original Array and Prefix Sums", fontsize=14, fontweight='bold')
        ax2.set_xlim(-0.5, self.n - 0.5)
        ax2.set_ylim(0, max(max(self.original), self.prefix_sum(self.n - 1)) * 1.2)

        # Original array bars
        x_pos = np.arange(self.n)
        bars = ax2.bar(x_pos, self.original, alpha=0.6, color='steelblue',
                      label='Original Values')

        # Prefix sum line
        prefix_sums = [self.prefix_sum(i) for i in range(self.n)]
        ax2.plot(x_pos, prefix_sums, 'r-o', linewidth=2, markersize=6,
                label='Prefix Sums')

        # Highlight
        if highlight_index is not None:
            bars[highlight_index].set_color('red')
            ax2.axvline(x=highlight_index, color='red', linestyle='--', alpha=0.5)

        # Annotations
        for i in range(self.n):
            ax2.text(i, self.original[i] + 1, f"{self.original[i]:.0f}",
                    ha='center', fontsize=8)
            ax2.text(i, prefix_sums[i] + 2, f"Σ={prefix_sums[i]:.0f}",
                    ha='center', fontsize=8, color='red')

        ax2.set_xlabel("Array Index (0-based)")
        ax2.set_ylabel("Value")
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    def print_structure(self):
        """Print the tree structure with explanations"""
        print("Fenwick Tree Structure:")
        print("-" * 50)
        print("Index | Value | Responsibility | Binary")
        print("-" * 50)

        for i in range(1, self.n + 1):
            lsb = self._lsb(i)
            start = i - lsb + 1
            binary = bin(i)[2:].zfill(len(bin(self.n)[2:]))
            print(f"{i:5} | {self.tree[i]:5.0f} | [{start:2},{i:2}]"
                  f"         | {binary}")

        print("-" * 50)
        print(f"Original array: {self.original}")
        print(f"Tree array: {self.tree[1:]}")


class FenwickTree2D:
    """
    2D Fenwick Tree for 2D range sum queries

    Extends the concept to 2 dimensions for rectangular range queries.

    Applications:
    - 2D range sum queries
    - Image processing (sum of pixel values in rectangle)
    - Computational geometry
    """

    def __init__(self, matrix: List[List[Union[int, float]]]):
        """
        Initialize 2D Fenwick Tree from matrix

        Args:
            matrix: 2D array (row-major order)
        """
        if not matrix or not matrix[0]:
            raise ValueError("Matrix cannot be empty")

        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.tree = [[0] * (self.cols + 1) for _ in range(self.rows + 1)]
        self.original = [row.copy() for row in matrix]

        # Build tree
        for i in range(self.rows):
            for j in range(self.cols):
                self.update(i, j, matrix[i][j])

    @staticmethod
    def _lsb(x: int) -> int:
        """Get least significant bit"""
        return x & (-x)

    def update(self, row: int, col: int, delta: Union[int, float]) -> None:
        """
        Add delta to element at (row, col)

        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            delta: Value to add
        """
        # Convert to 1-based
        row += 1
        col += 1

        i = row
        while i <= self.rows:
            j = col
            while j <= self.cols:
                self.tree[i][j] += delta
                j += self._lsb(j)
            i += self._lsb(i)

    def prefix_sum(self, row: int, col: int) -> Union[int, float]:
        """
        Get sum of rectangle from (0,0) to (row,col)

        Args:
            row: End row (0-based)
            col: End column (0-based)

        Returns:
            Rectangle sum
        """
        if row < 0 or col < 0:
            return 0

        # Convert to 1-based
        row += 1
        col += 1
        result = 0

        i = row
        while i > 0:
            j = col
            while j > 0:
                result += self.tree[i][j]
                j -= self._lsb(j)
            i -= self._lsb(i)

        return result

    def range_sum(self, r1: int, c1: int, r2: int, c2: int) -> Union[int, float]:
        """
        Get sum of rectangle from (r1,c1) to (r2,c2) inclusive

        Uses inclusion-exclusion principle.

        Args:
            r1, c1: Top-left corner (0-based)
            r2, c2: Bottom-right corner (0-based)

        Returns:
            Rectangle sum
        """
        # Use inclusion-exclusion
        total = self.prefix_sum(r2, c2)
        if r1 > 0:
            total -= self.prefix_sum(r1 - 1, c2)
        if c1 > 0:
            total -= self.prefix_sum(r2, c1 - 1)
        if r1 > 0 and c1 > 0:
            total += self.prefix_sum(r1 - 1, c1 - 1)

        return total


class RangeFenwickTree:
    """
    Fenwick Tree with range update support using difference array

    Supports both range updates and range queries efficiently.
    Uses two Fenwick trees internally.
    """

    def __init__(self, arr: List[Union[int, float]]):
        """Initialize with array"""
        self.n = len(arr)
        self.bit1 = FenwickTree([0] * self.n)  # For range updates
        self.bit2 = FenwickTree([0] * self.n)  # For range update coefficients

        # Initialize with original values
        for i, val in enumerate(arr):
            self.update_range(i, i, val)

    def update_range(self, left: int, right: int, delta: Union[int, float]) -> None:
        """
        Add delta to all elements in range [left, right]

        Args:
            left: Start index (0-based)
            right: End index (0-based)
            delta: Value to add
        """
        # Update using difference array technique
        self.bit1.update(left, delta)
        self.bit1.update(right + 1, -delta) if right + 1 < self.n else None

        self.bit2.update(left, delta * left)
        self.bit2.update(right + 1, -delta * (right + 1)) if right + 1 < self.n else None

    def prefix_sum(self, index: int) -> Union[int, float]:
        """Get prefix sum up to index"""
        if index < 0:
            return 0
        return self.bit1.prefix_sum(index) * (index + 1) - self.bit2.prefix_sum(index)

    def range_sum(self, left: int, right: int) -> Union[int, float]:
        """Get range sum from left to right"""
        if left > 0:
            return self.prefix_sum(right) - self.prefix_sum(left - 1)
        return self.prefix_sum(right)


def demonstrate_fenwick_tree():
    """Demonstrate Fenwick Tree operations"""
    print("=" * 60)
    print("Fenwick Tree Demonstration")
    print("=" * 60)

    # Create array
    arr = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3]
    print(f"\nOriginal array: {arr}")

    # Create Fenwick Tree
    ft = FenwickTree(arr)

    # Print structure
    ft.print_structure()

    # Test queries
    print("\nPrefix sum queries:")
    for i in [2, 5, 10]:
        print(f"  Sum [0, {i}]: {ft.prefix_sum(i)}")

    print("\nRange sum queries:")
    test_ranges = [(1, 3), (2, 7), (5, 9)]
    for left, right in test_ranges:
        print(f"  Sum [{left}, {right}]: {ft.range_sum(left, right)}")

    # Update
    print("\nUpdating index 4 by +10...")
    ft.update(4, 10)
    print(f"New value at index 4: {ft.get_value(4)}")
    print(f"New sum [2, 7]: {ft.range_sum(2, 7)}")

    # Visualize
    ft.visualize(highlight_index=4)


def demonstrate_2d_fenwick():
    """Demonstrate 2D Fenwick Tree"""
    print("\n" + "=" * 60)
    print("2D Fenwick Tree Demonstration")
    print("=" * 60)

    # Create matrix
    matrix = [
        [3, 0, 1, 4],
        [2, 5, 6, 3],
        [1, 2, 3, 1],
        [4, 1, 2, 5]
    ]

    print("\nOriginal matrix:")
    for row in matrix:
        print("  ", row)

    # Create 2D Fenwick Tree
    ft2d = FenwickTree2D(matrix)

    # Test queries
    print("\nRectangle sum queries:")
    test_rectangles = [
        (0, 0, 1, 1),  # Top-left 2x2
        (1, 1, 2, 2),  # Center 2x2
        (0, 0, 3, 3),  # Entire matrix
    ]

    for r1, c1, r2, c2 in test_rectangles:
        result = ft2d.range_sum(r1, c1, r2, c2)
        print(f"  Sum [{r1},{c1}] to [{r2},{c2}]: {result}")

    # Update
    print("\nUpdating position (1,2) by +10...")
    ft2d.update(1, 2, 10)
    print(f"New sum of entire matrix: {ft2d.range_sum(0, 0, 3, 3)}")


def application_inversion_count():
    """Application: Count inversions in an array using Fenwick Tree"""
    print("\n" + "=" * 60)
    print("Application: Inversion Count")
    print("=" * 60)

    def count_inversions(arr: List[int]) -> int:
        """Count inversions using Fenwick Tree"""
        if not arr:
            return 0

        # Coordinate compression
        sorted_arr = sorted(set(arr))
        compress = {v: i + 1 for i, v in enumerate(sorted_arr)}

        # Use Fenwick Tree to count inversions
        n = len(sorted_arr)
        ft = FenwickTree([0] * n)
        inversions = 0

        for num in reversed(arr):
            compressed = compress[num]
            # Count elements smaller than current that appear after
            inversions += ft.prefix_sum(compressed - 2) if compressed > 1 else 0
            ft.update(compressed - 1, 1)

        return inversions

    # Test
    test_arrays = [
        [2, 4, 1, 3, 5],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [3, 1, 4, 1, 5, 9, 2, 6]
    ]

    for arr in test_arrays:
        inv_count = count_inversions(arr)
        print(f"Array {arr}")
        print(f"  Inversions: {inv_count}")


def benchmark_fenwick_vs_naive():
    """Benchmark Fenwick Tree vs naive approach"""
    print("\n" + "=" * 60)
    print("Performance Benchmark")
    print("=" * 60)

    import time
    import random

    n = 10000
    arr = [random.randint(1, 100) for _ in range(n)]
    queries = 1000

    # Fenwick Tree approach
    ft = FenwickTree(arr)
    start = time.time()
    for _ in range(queries):
        i = random.randint(0, n - 1)
        j = random.randint(i, n - 1)
        ft.range_sum(i, j)
    ft_time = time.time() - start

    # Naive approach
    start = time.time()
    for _ in range(queries):
        i = random.randint(0, n - 1)
        j = random.randint(i, n - 1)
        sum(arr[i:j+1])
    naive_time = time.time() - start

    print(f"\nArray size: {n}")
    print(f"Number of queries: {queries}")
    print(f"\nFenwick Tree time: {ft_time:.4f} seconds")
    print(f"Naive approach time: {naive_time:.4f} seconds")
    print(f"Speedup: {naive_time/ft_time:.2f}x")

    # Update performance
    updates = 100
    start = time.time()
    for _ in range(updates):
        i = random.randint(0, n - 1)
        ft.update(i, random.randint(-10, 10))
    ft_update_time = time.time() - start

    print(f"\nFenwick Tree update time ({updates} updates): {ft_update_time:.4f} seconds")
    print(f"Average per update: {ft_update_time/updates:.6f} seconds")


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_fenwick_tree()
    demonstrate_2d_fenwick()
    application_inversion_count()
    benchmark_fenwick_vs_naive()

    print("\n" + "=" * 60)
    print("Fenwick Tree Implementation Complete!")
    print("=" * 60)