#!/usr/bin/env python3
"""
Skip List Implementation

A Skip List is a probabilistic data structure that allows O(log n) search complexity
as well as O(log n) insertion complexity within an ordered sequence of elements.
It uses multiple layers of linked lists with "express lanes" for faster traversal.

Key Concepts:
- Multiple levels of linked lists
- Each level skips over fewer elements
- Probabilistic balancing (coin flip for promotion)
- No complex rotations like balanced trees
- Expected space: O(n)

Time Complexity (Expected):
- Search: O(log n)
- Insert: O(log n)
- Delete: O(log n)
- Space: O(n)

Applications:
- Database indexing (MemSQL, Redis sorted sets)
- Concurrent data structures (lock-free skip lists)
- P2P networks (distributed hash tables)
- In-memory databases
- Priority queues

Author: Algorithms Multiverse
License: MIT
"""

import random
from typing import Optional, List, Any, Tuple, Generator
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from dataclasses import dataclass


@dataclass
class SkipNode:
    """
    Node in a skip list

    Attributes:
        key: The search key
        value: The stored value
        forward: List of forward pointers for each level
        level: Height of this node (number of levels it appears in)
    """
    key: Any
    value: Any
    forward: List[Optional['SkipNode']]
    level: int

    def __init__(self, key: Any, value: Any, level: int):
        """Initialize a skip list node"""
        self.key = key
        self.value = value
        self.level = level
        self.forward = [None] * (level + 1)

    def __str__(self) -> str:
        return f"Node(key={self.key}, value={self.value}, level={self.level})"


class SkipList:
    """
    Skip List - Probabilistic alternative to balanced trees

    Uses randomization to maintain balance with high probability.
    Each element has a random "height" determining how many levels it appears in.

    Attributes:
        max_level: Maximum allowed level
        p: Probability of promotion to next level
        level: Current maximum level in use
        header: Sentinel node at the beginning
        size: Number of elements
    """

    def __init__(self, max_level: int = 16, p: float = 0.5):
        """
        Initialize Skip List

        Args:
            max_level: Maximum number of levels (typically log n)
            p: Probability of promoting element to next level (typically 0.5)
        """
        self.max_level = max_level
        self.p = p
        self.level = 0
        self.header = SkipNode(None, None, max_level)
        self.size = 0

        # Statistics
        self.comparisons = 0  # For performance analysis

    def _random_level(self) -> int:
        """
        Generate random level using geometric distribution

        Returns level between 0 and max_level-1
        """
        level = 0
        while random.random() < self.p and level < self.max_level - 1:
            level += 1
        return level

    def search(self, key: Any) -> Optional[Any]:
        """
        Search for a key in the skip list

        Args:
            key: Key to search for

        Returns:
            Value if found, None otherwise
        """
        self.comparisons = 0
        current = self.header

        # Start from highest level and move down
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
                self.comparisons += 1

        # Move to next node at level 0
        current = current.forward[0]
        self.comparisons += 1

        if current and current.key == key:
            return current.value
        return None

    def insert(self, key: Any, value: Any) -> None:
        """
        Insert a key-value pair into the skip list

        Args:
            key: Key to insert
            value: Value to store
        """
        # Track path for insertion
        update = [None] * (self.max_level + 1)
        current = self.header

        # Find position to insert
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        # Update existing key
        if current and current.key == key:
            current.value = value
            return

        # Generate random level for new node
        new_level = self._random_level()

        # Update list level if necessary
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level

        # Create and insert new node
        new_node = SkipNode(key, value, new_level)
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

        self.size += 1

    def delete(self, key: Any) -> bool:
        """
        Delete a key from the skip list

        Args:
            key: Key to delete

        Returns:
            True if deleted, False if not found
        """
        update = [None] * (self.max_level + 1)
        current = self.header

        # Find node to delete
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        # Node found
        if current and current.key == key:
            # Update forward pointers
            for i in range(current.level + 1):
                update[i].forward[i] = current.forward[i]

            # Update list level
            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1

            self.size -= 1
            return True

        return False

    def __contains__(self, key: Any) -> bool:
        """Check if key exists in skip list"""
        return self.search(key) is not None

    def __len__(self) -> int:
        """Get number of elements"""
        return self.size

    def get_min(self) -> Optional[Tuple[Any, Any]]:
        """Get minimum key-value pair"""
        first = self.header.forward[0]
        if first:
            return (first.key, first.value)
        return None

    def get_max(self) -> Optional[Tuple[Any, Any]]:
        """Get maximum key-value pair"""
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i]:
                current = current.forward[i]

        if current != self.header:
            return (current.key, current.value)
        return None

    def range_search(self, start_key: Any, end_key: Any) -> List[Tuple[Any, Any]]:
        """
        Find all key-value pairs in range [start_key, end_key]

        Args:
            start_key: Range start (inclusive)
            end_key: Range end (inclusive)

        Returns:
            List of (key, value) tuples in range
        """
        result = []
        current = self.header

        # Find start position
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < start_key:
                current = current.forward[i]

        current = current.forward[0]

        # Collect elements in range
        while current and current.key <= end_key:
            result.append((current.key, current.value))
            current = current.forward[0]

        return result

    def to_list(self) -> List[Tuple[Any, Any]]:
        """Convert skip list to sorted list of (key, value) tuples"""
        result = []
        current = self.header.forward[0]
        while current:
            result.append((current.key, current.value))
            current = current.forward[0]
        return result

    def print_structure(self):
        """Print the skip list structure level by level"""
        print("\nSkip List Structure:")
        print(f"Size: {self.size}, Max Level: {self.level}")
        print("-" * 60)

        for level in range(self.level, -1, -1):
            print(f"Level {level:2}: ", end="")
            current = self.header.forward[level]
            while current:
                print(f"{current.key} -> ", end="")
                current = current.forward[level]
            print("None")

        print("-" * 60)

    def visualize(self, highlight_key: Optional[Any] = None):
        """
        Visualize the skip list structure

        Args:
            highlight_key: Optional key to highlight
        """
        if self.size == 0:
            print("Empty skip list")
            return

        fig, ax = plt.subplots(1, 1, figsize=(14, 8))
        ax.set_title("Skip List Visualization", fontsize=14, fontweight='bold')

        # Collect all nodes at level 0
        nodes = []
        current = self.header.forward[0]
        while current:
            nodes.append(current)
            current = current.forward[0]

        if not nodes:
            return

        # Set up grid
        x_spacing = 1.5
        y_spacing = 0.8
        node_width = 1.0
        node_height = 0.5

        # Draw nodes at each level
        for node_idx, node in enumerate(nodes):
            x_pos = (node_idx + 1) * x_spacing

            for level in range(node.level + 1):
                y_pos = level * y_spacing

                # Node rectangle
                color = 'red' if highlight_key and node.key == highlight_key else 'lightblue'
                rect = patches.Rectangle((x_pos - node_width/2, y_pos - node_height/2),
                                        node_width, node_height,
                                        linewidth=1, edgecolor='black',
                                        facecolor=color)
                ax.add_patch(rect)

                # Node text
                ax.text(x_pos, y_pos, str(node.key),
                       ha='center', va='center', fontweight='bold')

        # Draw header
        for level in range(self.level + 1):
            y_pos = level * y_spacing
            rect = patches.Rectangle((-node_width/2, y_pos - node_height/2),
                                    node_width, node_height,
                                    linewidth=1, edgecolor='black',
                                    facecolor='gray')
            ax.add_patch(rect)
            ax.text(0, y_pos, 'H', ha='center', va='center',
                   fontweight='bold', color='white')

        # Draw forward pointers
        for level in range(self.level + 1):
            y_pos = level * y_spacing
            current = self.header
            x_from = 0

            while current:
                if current.forward[level]:
                    # Find x position of next node
                    x_to = None
                    for idx, node in enumerate(nodes):
                        if node == current.forward[level]:
                            x_to = (idx + 1) * x_spacing
                            break

                    if x_to:
                        # Draw arrow
                        ax.arrow(x_from + node_width/2, y_pos,
                               x_to - x_from - node_width, 0,
                               head_width=0.1, head_length=0.1,
                               fc='black', ec='black', alpha=0.6)

                # Move to next node
                if current == self.header:
                    current = current.forward[level]
                    if current:
                        for idx, node in enumerate(nodes):
                            if node == current:
                                x_from = (idx + 1) * x_spacing
                                break
                else:
                    next_node = current.forward[level]
                    if next_node:
                        for idx, node in enumerate(nodes):
                            if node == next_node:
                                current = next_node
                                x_from = (idx + 1) * x_spacing
                                break
                    else:
                        break

        # Set axis properties
        ax.set_xlim(-1, len(nodes) * x_spacing + 1)
        ax.set_ylim(-0.5, (self.level + 1) * y_spacing + 0.5)
        ax.set_aspect('equal')
        ax.axis('off')

        # Add level labels
        for level in range(self.level + 1):
            ax.text(-1.5, level * y_spacing, f'L{level}',
                   ha='center', va='center', fontsize=10)

        plt.tight_layout()
        plt.show()

    def analyze_structure(self) -> dict:
        """
        Analyze skip list structure and performance characteristics

        Returns:
            Dictionary with analysis metrics
        """
        level_counts = [0] * (self.level + 1)
        current = self.header.forward[0]

        while current:
            for i in range(current.level + 1):
                level_counts[i] += 1
            current = current.forward[0]

        # Calculate average search path length
        total_path_length = 0
        for key, _ in self.to_list():
            self.search(key)
            total_path_length += self.comparisons

        avg_path_length = total_path_length / self.size if self.size > 0 else 0

        return {
            'size': self.size,
            'max_level_used': self.level,
            'level_distribution': level_counts,
            'avg_search_path': avg_path_length,
            'space_overhead': sum(level_counts) / self.size if self.size > 0 else 0
        }


class IndexableSkipList(SkipList):
    """
    Skip List with O(log n) random access by index

    Maintains subtree sizes for indexed access.
    """

    def __init__(self, *args, **kwargs):
        """Initialize indexable skip list"""
        super().__init__(*args, **kwargs)
        # Add span information for each forward pointer
        self.header.span = [0] * (self.max_level + 1)

    def insert(self, key: Any, value: Any) -> None:
        """Insert with span updates for indexing"""
        update = [None] * (self.max_level + 1)
        rank = [0] * (self.max_level + 1)
        current = self.header

        # Find position and calculate ranks
        for i in range(self.level, -1, -1):
            rank[i] = 0 if i == self.level else rank[i + 1]
            while current.forward[i] and current.forward[i].key < key:
                if hasattr(current, 'span'):
                    rank[i] += current.span[i]
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        # Update existing key
        if current and current.key == key:
            current.value = value
            return

        # Insert new node with spans
        new_level = self._random_level()
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                rank[i] = 0
                update[i] = self.header
                if not hasattr(self.header, 'span'):
                    self.header.span = [0] * (self.max_level + 1)
                self.header.span[i] = self.size
            self.level = new_level

        # Create new node
        new_node = SkipNode(key, value, new_level)
        new_node.span = [0] * (new_level + 1)

        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

            # Update spans
            if hasattr(update[i], 'span'):
                new_node.span[i] = update[i].span[i] - (rank[0] - rank[i])
                update[i].span[i] = (rank[0] - rank[i]) + 1

        # Update spans for untouched levels
        for i in range(new_level + 1, self.level + 1):
            if hasattr(update[i], 'span'):
                update[i].span[i] += 1

        self.size += 1

    def get_by_index(self, index: int) -> Optional[Tuple[Any, Any]]:
        """
        Get element at given index (0-based)

        Args:
            index: Index to access

        Returns:
            (key, value) tuple or None
        """
        if index < 0 or index >= self.size:
            return None

        current = self.header
        traversed = 0

        for i in range(self.level, -1, -1):
            while current.forward[i] and traversed + current.span[i] <= index:
                traversed += current.span[i]
                current = current.forward[i]

        current = current.forward[0]
        if current:
            return (current.key, current.value)
        return None


def demonstrate_skip_list():
    """Demonstrate skip list operations"""
    print("=" * 60)
    print("Skip List Demonstration")
    print("=" * 60)

    # Create skip list
    sl = SkipList(max_level=4, p=0.5)

    # Insert elements
    elements = [(3, "three"), (7, "seven"), (1, "one"), (4, "four"),
                (2, "two"), (6, "six"), (5, "five"), (8, "eight")]

    print("\nInserting elements:")
    for key, value in elements:
        print(f"  Insert ({key}, {value})")
        sl.insert(key, value)

    # Print structure
    sl.print_structure()

    # Search operations
    print("\nSearch operations:")
    search_keys = [4, 9, 1]
    for key in search_keys:
        result = sl.search(key)
        print(f"  Search({key}): {result}")

    # Range search
    print("\nRange search [3, 6]:")
    range_result = sl.range_search(3, 6)
    for key, value in range_result:
        print(f"  ({key}, {value})")

    # Min and max
    print(f"\nMin: {sl.get_min()}")
    print(f"Max: {sl.get_max()}")

    # Delete
    print("\nDeleting key 4...")
    sl.delete(4)
    sl.print_structure()

    # Visualize
    sl.visualize(highlight_key=5)

    # Analyze structure
    analysis = sl.analyze_structure()
    print("\nStructure Analysis:")
    for key, value in analysis.items():
        print(f"  {key}: {value}")


def benchmark_skip_list():
    """Benchmark skip list vs Python's sorted containers"""
    print("\n" + "=" * 60)
    print("Skip List Performance Benchmark")
    print("=" * 60)

    import time
    import random

    n = 10000
    operations = 1000

    # Prepare random data
    keys = list(range(n))
    random.shuffle(keys)

    # Skip List
    sl = SkipList(max_level=16, p=0.5)
    start = time.time()
    for key in keys:
        sl.insert(key, f"value_{key}")
    sl_insert_time = time.time() - start

    # Search benchmark
    search_keys = random.sample(keys, operations)
    start = time.time()
    for key in search_keys:
        sl.search(key)
    sl_search_time = time.time() - start

    # Python sorted list comparison
    sorted_list = []
    start = time.time()
    for key in keys:
        sorted_list.append((key, f"value_{key}"))
        sorted_list.sort()
    list_insert_time = time.time() - start

    # Binary search in sorted list
    import bisect
    start = time.time()
    for key in search_keys:
        idx = bisect.bisect_left(sorted_list, (key, ""))
        if idx < len(sorted_list) and sorted_list[idx][0] == key:
            _ = sorted_list[idx][1]
    list_search_time = time.time() - start

    print(f"\nData size: {n} elements")
    print(f"Operations: {operations}")
    print("\nInsertion Performance:")
    print(f"  Skip List: {sl_insert_time:.4f} seconds")
    print(f"  Sorted List: {list_insert_time:.4f} seconds")
    print(f"  Speedup: {list_insert_time/sl_insert_time:.2f}x")
    print("\nSearch Performance:")
    print(f"  Skip List: {sl_search_time:.4f} seconds")
    print(f"  Binary Search: {list_search_time:.4f} seconds")
    print(f"  Ratio: {sl_search_time/list_search_time:.2f}x")


def demonstrate_probabilistic_analysis():
    """Analyze probabilistic properties of skip lists"""
    print("\n" + "=" * 60)
    print("Probabilistic Analysis")
    print("=" * 60)

    # Test different probability values
    probabilities = [0.25, 0.5, 0.75]
    n = 1000

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for idx, p in enumerate(probabilities):
        sl = SkipList(max_level=20, p=p)

        # Insert elements
        for i in range(n):
            sl.insert(i, f"value_{i}")

        # Analyze level distribution
        analysis = sl.analyze_structure()
        levels = analysis['level_distribution']

        # Plot distribution
        ax = axes[idx]
        ax.bar(range(len(levels)), levels, color='steelblue')
        ax.set_title(f'Level Distribution (p={p})')
        ax.set_xlabel('Level')
        ax.set_ylabel('Number of Nodes')
        ax.grid(True, alpha=0.3)

        # Add statistics
        expected_at_level = [n * (p ** i) for i in range(len(levels))]
        ax.plot(range(len(levels)), expected_at_level, 'r--',
               label='Expected', linewidth=2)
        ax.legend()

        print(f"\nProbability p={p}:")
        print(f"  Max level used: {analysis['max_level_used']}")
        print(f"  Avg search path: {analysis['avg_search_path']:.2f}")
        print(f"  Space overhead: {analysis['space_overhead']:.2f}x")

    plt.suptitle('Skip List Level Distribution with Different Probabilities')
    plt.tight_layout()
    plt.show()


def application_example_lru_cache():
    """Example: LRU Cache implementation using Skip List"""
    print("\n" + "=" * 60)
    print("Application: LRU Cache with Skip List")
    print("=" * 60)

    class LRUCache:
        """LRU Cache using Skip List for O(log n) operations"""

        def __init__(self, capacity: int):
            self.capacity = capacity
            self.sl = SkipList()
            self.time_counter = 0
            self.key_to_time = {}

        def get(self, key: int) -> Optional[Any]:
            """Get value and update access time"""
            if key not in self.key_to_time:
                return None

            # Get current value
            old_time = self.key_to_time[key]
            value = self.sl.search(old_time)

            # Update with new timestamp
            self.sl.delete(old_time)
            self.time_counter += 1
            self.sl.insert(self.time_counter, (key, value))
            self.key_to_time[key] = self.time_counter

            return value

        def put(self, key: int, value: Any) -> None:
            """Put key-value pair in cache"""
            # Update existing key
            if key in self.key_to_time:
                old_time = self.key_to_time[key]
                self.sl.delete(old_time)
            # Evict if at capacity
            elif len(self.key_to_time) >= self.capacity:
                # Remove least recently used (minimum time)
                lru = self.sl.get_min()
                if lru:
                    lru_time, (lru_key, _) = lru[0], lru[1]
                    self.sl.delete(lru_time)
                    del self.key_to_time[lru_key]

            # Insert new
            self.time_counter += 1
            self.sl.insert(self.time_counter, (key, value))
            self.key_to_time[key] = self.time_counter

        def display(self):
            """Display cache contents in LRU order"""
            print("Cache contents (LRU -> MRU):")
            for time, (key, value) in self.sl.to_list():
                print(f"  Key: {key}, Value: {value}")

    # Test LRU Cache
    cache = LRUCache(capacity=3)

    operations = [
        ("put", 1, "one"),
        ("put", 2, "two"),
        ("put", 3, "three"),
        ("get", 1, None),
        ("put", 4, "four"),  # Evicts 2
        ("get", 2, None),    # Returns None
        ("get", 3, None),
        ("put", 5, "five"),  # Evicts 4
    ]

    for op in operations:
        if op[0] == "put":
            print(f"Put({op[1]}, {op[2]})")
            cache.put(op[1], op[2])
        else:
            result = cache.get(op[1])
            print(f"Get({op[1]}) = {result}")

    print("\nFinal cache state:")
    cache.display()


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_skip_list()
    benchmark_skip_list()
    demonstrate_probabilistic_analysis()
    application_example_lru_cache()

    print("\n" + "=" * 60)
    print("Skip List Implementation Complete!")
    print("=" * 60)