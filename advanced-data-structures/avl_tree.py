#!/usr/bin/env python3
"""
AVL Tree Implementation

An AVL tree is a self-balancing binary search tree where the height difference
between left and right subtrees (balance factor) is at most 1 for every node.
This ensures O(log n) time complexity for insertions, deletions, and searches.

Named after its inventors Adelson-Velsky and Landis (1962).

Key Properties:
- Self-balancing through rotations
- Balance factor = height(left) - height(right) ∈ {-1, 0, 1}
- Height-balanced: guarantees O(log n) operations
- More rigidly balanced than Red-Black trees

Time Complexity:
- Search: O(log n)
- Insert: O(log n)
- Delete: O(log n)
- Space: O(n)

Applications:
- Database indexing where lookups are more frequent than insertions
- Memory-constrained systems (fewer rotations than Red-Black)
- Real-time systems requiring predictable performance

Author: Algorithms Multiverse
License: MIT
"""

from typing import Optional, List, Tuple, Generator
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import deque


class AVLNode:
    """
    Node in an AVL tree

    Attributes:
        key: The value stored in the node
        left: Left child node
        right: Right child node
        height: Height of the node (leaves have height 1)
        balance_factor: Height(left) - Height(right)
    """

    def __init__(self, key: int):
        """Initialize an AVL node with a key"""
        self.key = key
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height: int = 1
        self.balance_factor: int = 0

    def __str__(self) -> str:
        """String representation of the node"""
        return f"Node(key={self.key}, height={self.height}, bf={self.balance_factor})"

    def update_height_and_balance(self):
        """Update the height and balance factor of this node"""
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0

        self.height = 1 + max(left_height, right_height)
        self.balance_factor = left_height - right_height


class AVLTree:
    """
    AVL Tree - Self-balancing Binary Search Tree

    Maintains balance through rotations after insertions and deletions,
    ensuring logarithmic time complexity for all operations.

    Attributes:
        root: Root node of the tree
        size: Number of nodes in the tree
        rotation_count: Number of rotations performed (for analysis)
    """

    def __init__(self):
        """Initialize an empty AVL tree"""
        self.root: Optional[AVLNode] = None
        self.size: int = 0
        self.rotation_count: int = 0

    def _get_height(self, node: Optional[AVLNode]) -> int:
        """Get height of a node (0 for None)"""
        return node.height if node else 0

    def _get_balance_factor(self, node: Optional[AVLNode]) -> int:
        """Get balance factor of a node"""
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_left(self, z: AVLNode) -> AVLNode:
        """
        Perform left rotation on node z

            z                y
           / \              / \
          T1  y    -->     z   T3
             / \          / \
            T2 T3        T1 T2

        Args:
            z: Node to rotate

        Returns:
            New root of subtree (y)
        """
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights and balance factors
        z.update_height_and_balance()
        y.update_height_and_balance()

        self.rotation_count += 1
        return y

    def _rotate_right(self, z: AVLNode) -> AVLNode:
        """
        Perform right rotation on node z

            z                y
           / \              / \
          y  T3    -->     T1  z
         / \                  / \
        T1 T2                T2 T3

        Args:
            z: Node to rotate

        Returns:
            New root of subtree (y)
        """
        y = z.left
        T2 = y.right

        # Perform rotation
        y.right = z
        z.left = T2

        # Update heights and balance factors
        z.update_height_and_balance()
        y.update_height_and_balance()

        self.rotation_count += 1
        return y

    def _rebalance(self, node: AVLNode, key: int) -> AVLNode:
        """
        Rebalance the tree at the given node after insertion/deletion

        Four cases for imbalance:
        1. Left-Left: Single right rotation
        2. Right-Right: Single left rotation
        3. Left-Right: Left rotation on left child, then right rotation
        4. Right-Left: Right rotation on right child, then left rotation

        Args:
            node: Node to check for rebalancing
            key: Key that was inserted/deleted (for determining rotation type)

        Returns:
            New root of rebalanced subtree
        """
        # Update height and balance factor
        node.update_height_and_balance()
        balance = node.balance_factor

        # Left heavy (balance > 1)
        if balance > 1:
            # Left-Left case
            if key < node.left.key:
                return self._rotate_right(node)
            # Left-Right case
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

        # Right heavy (balance < -1)
        if balance < -1:
            # Right-Right case
            if key > node.right.key:
                return self._rotate_left(node)
            # Right-Left case
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

        return node

    def insert(self, key: int) -> None:
        """
        Insert a key into the AVL tree

        Args:
            key: Value to insert
        """
        self.root = self._insert_recursive(self.root, key)
        self.size += 1

    def _insert_recursive(self, node: Optional[AVLNode], key: int) -> AVLNode:
        """
        Recursively insert a key and rebalance

        Args:
            node: Current node in recursion
            key: Value to insert

        Returns:
            Root of modified subtree
        """
        # Standard BST insertion
        if not node:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert_recursive(node.left, key)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key)
        else:
            # Duplicate keys not allowed
            return node

        # Rebalance the node
        return self._rebalance(node, key)

    def delete(self, key: int) -> bool:
        """
        Delete a key from the AVL tree

        Args:
            key: Value to delete

        Returns:
            True if deleted, False if not found
        """
        if not self.search(key):
            return False

        self.root = self._delete_recursive(self.root, key)
        self.size -= 1
        return True

    def _delete_recursive(self, node: Optional[AVLNode], key: int) -> Optional[AVLNode]:
        """
        Recursively delete a key and rebalance

        Args:
            node: Current node in recursion
            key: Value to delete

        Returns:
            Root of modified subtree
        """
        if not node:
            return None

        # Standard BST deletion
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Node with only one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Node with two children: Get inorder successor
            min_node = self._find_min(node.right)
            node.key = min_node.key
            node.right = self._delete_recursive(node.right, min_node.key)

        # Rebalance after deletion
        if not node:
            return None

        node.update_height_and_balance()
        balance = node.balance_factor

        # Left heavy
        if balance > 1:
            if self._get_balance_factor(node.left) >= 0:
                return self._rotate_right(node)
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

        # Right heavy
        if balance < -1:
            if self._get_balance_factor(node.right) <= 0:
                return self._rotate_left(node)
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

        return node

    def _find_min(self, node: AVLNode) -> AVLNode:
        """Find the minimum node in a subtree"""
        while node.left:
            node = node.left
        return node

    def search(self, key: int) -> bool:
        """
        Search for a key in the tree

        Args:
            key: Value to search for

        Returns:
            True if found, False otherwise
        """
        return self._search_recursive(self.root, key) is not None

    def _search_recursive(self, node: Optional[AVLNode], key: int) -> Optional[AVLNode]:
        """Recursively search for a key"""
        if not node:
            return None

        if key == node.key:
            return node
        elif key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    def get_min(self) -> Optional[int]:
        """Get the minimum value in the tree"""
        if not self.root:
            return None
        node = self.root
        while node.left:
            node = node.left
        return node.key

    def get_max(self) -> Optional[int]:
        """Get the maximum value in the tree"""
        if not self.root:
            return None
        node = self.root
        while node.right:
            node = node.right
        return node.key

    def get_height(self) -> int:
        """Get the height of the tree"""
        return self._get_height(self.root)

    def is_balanced(self) -> bool:
        """
        Check if the tree is properly balanced (AVL property)

        Returns:
            True if balanced, False otherwise
        """
        return self._check_balance(self.root)[0]

    def _check_balance(self, node: Optional[AVLNode]) -> Tuple[bool, int]:
        """
        Recursively check balance and return (is_balanced, height)

        Args:
            node: Node to check

        Returns:
            Tuple of (is_balanced, height)
        """
        if not node:
            return True, 0

        left_balanced, left_height = self._check_balance(node.left)
        if not left_balanced:
            return False, 0

        right_balanced, right_height = self._check_balance(node.right)
        if not right_balanced:
            return False, 0

        # Check balance factor
        balance = left_height - right_height
        if abs(balance) > 1:
            return False, 0

        return True, 1 + max(left_height, right_height)

    def inorder_traversal(self) -> List[int]:
        """
        Perform inorder traversal (sorted order)

        Returns:
            List of keys in sorted order
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node: Optional[AVLNode], result: List[int]):
        """Recursive inorder traversal"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.key)
            self._inorder_recursive(node.right, result)

    def preorder_traversal(self) -> List[int]:
        """
        Perform preorder traversal

        Returns:
            List of keys in preorder
        """
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node: Optional[AVLNode], result: List[int]):
        """Recursive preorder traversal"""
        if node:
            result.append(node.key)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def level_order_traversal(self) -> List[List[int]]:
        """
        Perform level-order traversal (BFS)

        Returns:
            List of lists, each containing keys at that level
        """
        if not self.root:
            return []

        result = []
        queue = deque([self.root])

        while queue:
            level_size = len(queue)
            level_values = []

            for _ in range(level_size):
                node = queue.popleft()
                level_values.append(node.key)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(level_values)

        return result

    def print_tree(self, node: Optional[AVLNode] = None, level: int = 0, prefix: str = "Root: "):
        """
        Print tree structure with indentation

        Args:
            node: Current node (default: root)
            level: Current depth level
            prefix: Prefix string for printing
        """
        if node is None:
            node = self.root

        if node is not None:
            print(" " * (level * 4) + prefix + f"{node.key} (h={node.height}, bf={node.balance_factor})")

            if node.left or node.right:
                if node.left:
                    self.print_tree(node.left, level + 1, "L--- ")
                else:
                    print(" " * ((level + 1) * 4) + "L--- None")

                if node.right:
                    self.print_tree(node.right, level + 1, "R--- ")
                else:
                    print(" " * ((level + 1) * 4) + "R--- None")

    def visualize(self, highlight_node: Optional[int] = None, title: str = "AVL Tree"):
        """
        Visualize the AVL tree using matplotlib

        Args:
            highlight_node: Key to highlight in red
            title: Title for the plot
        """
        if not self.root:
            print("Empty tree")
            return

        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        ax.set_title(title)
        ax.axis('off')

        # Calculate positions
        positions = {}
        self._calculate_positions(self.root, positions, 0, 0, 1)

        # Normalize positions
        if positions:
            min_x = min(pos[0] for pos in positions.values())
            max_x = max(pos[0] for pos in positions.values())
            max_y = max(pos[1] for pos in positions.values())

            for node in positions:
                x, y = positions[node]
                # Normalize x to [0.1, 0.9]
                if max_x > min_x:
                    x = 0.1 + 0.8 * (x - min_x) / (max_x - min_x)
                else:
                    x = 0.5
                # Normalize y to [0.1, 0.9]
                if max_y > 0:
                    y = 0.9 - 0.8 * y / max_y
                else:
                    y = 0.5
                positions[node] = (x, y)

        # Draw edges
        self._draw_edges(self.root, positions, ax)

        # Draw nodes
        self._draw_nodes(self.root, positions, ax, highlight_node)

        plt.tight_layout()
        plt.show()

    def _calculate_positions(self, node: Optional[AVLNode], positions: dict,
                            depth: int, left: float, right: float):
        """Calculate positions for visualization"""
        if not node:
            return

        mid = (left + right) / 2
        positions[node.key] = (mid, depth)

        if node.left:
            self._calculate_positions(node.left, positions, depth + 1, left, mid)
        if node.right:
            self._calculate_positions(node.right, positions, depth + 1, mid, right)

    def _draw_edges(self, node: Optional[AVLNode], positions: dict, ax):
        """Draw edges between nodes"""
        if not node:
            return

        x1, y1 = positions[node.key]

        if node.left:
            x2, y2 = positions[node.left.key]
            ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1)
            self._draw_edges(node.left, positions, ax)

        if node.right:
            x2, y2 = positions[node.right.key]
            ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1)
            self._draw_edges(node.right, positions, ax)

    def _draw_nodes(self, node: Optional[AVLNode], positions: dict, ax, highlight_node: Optional[int]):
        """Draw nodes with labels"""
        if not node:
            return

        x, y = positions[node.key]

        # Choose color
        if highlight_node and node.key == highlight_node:
            color = 'red'
        elif abs(node.balance_factor) > 1:
            color = 'orange'  # Unbalanced (shouldn't happen in correct AVL)
        else:
            color = 'lightblue'

        # Draw node circle
        circle = patches.Circle((x, y), 0.03, color=color, ec='black', linewidth=2)
        ax.add_patch(circle)

        # Add text
        ax.text(x, y, str(node.key), ha='center', va='center', fontsize=10, fontweight='bold')
        ax.text(x, y - 0.05, f"h={node.height}", ha='center', va='center', fontsize=7)
        ax.text(x, y - 0.07, f"bf={node.balance_factor}", ha='center', va='center', fontsize=7, color='gray')

        # Recursively draw children
        if node.left:
            self._draw_nodes(node.left, positions, ax, highlight_node)
        if node.right:
            self._draw_nodes(node.right, positions, ax, highlight_node)


def demonstrate_avl_operations():
    """Demonstrate AVL tree operations with visualization"""
    print("=" * 60)
    print("AVL Tree Demonstration")
    print("=" * 60)

    # Create tree and insert values
    avl = AVLTree()
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]

    print("\nInserting values:", values)
    for val in values:
        avl.insert(val)

    print(f"\nTree size: {avl.size}")
    print(f"Tree height: {avl.get_height()}")
    print(f"Total rotations performed: {avl.rotation_count}")
    print(f"Tree is balanced: {avl.is_balanced()}")

    # Print tree structure
    print("\nTree structure:")
    avl.print_tree()

    # Traversals
    print("\nTraversals:")
    print(f"Inorder (sorted): {avl.inorder_traversal()}")
    print(f"Preorder: {avl.preorder_traversal()}")
    print(f"Level-order: {avl.level_order_traversal()}")

    # Min and Max
    print(f"\nMin value: {avl.get_min()}")
    print(f"Max value: {avl.get_max()}")

    # Search
    search_key = 35
    print(f"\nSearching for {search_key}: {avl.search(search_key)}")

    # Visualize initial tree
    avl.visualize(title="AVL Tree - After Insertions")

    # Delete some nodes
    delete_keys = [20, 30, 50]
    print(f"\nDeleting nodes: {delete_keys}")
    for key in delete_keys:
        avl.delete(key)

    print(f"\nAfter deletions:")
    print(f"Tree size: {avl.size}")
    print(f"Tree is balanced: {avl.is_balanced()}")
    print(f"Inorder traversal: {avl.inorder_traversal()}")

    # Visualize after deletions
    avl.visualize(title="AVL Tree - After Deletions")


def compare_with_bst():
    """Compare AVL tree with regular BST performance"""
    print("\n" + "=" * 60)
    print("AVL Tree vs Regular BST Comparison")
    print("=" * 60)

    import random
    import time

    # Test with sorted input (worst case for BST)
    n = 1000
    sorted_data = list(range(n))

    # AVL Tree with sorted input
    avl = AVLTree()
    start = time.time()
    for val in sorted_data:
        avl.insert(val)
    avl_time = time.time() - start

    print(f"\nSorted input ({n} elements):")
    print(f"AVL Tree height: {avl.get_height()}")
    print(f"AVL insertion time: {avl_time:.4f} seconds")
    print(f"AVL rotations performed: {avl.rotation_count}")

    # Expected height for balanced tree
    import math
    expected_height = math.ceil(math.log2(n + 1))
    print(f"Expected balanced height: ~{expected_height}")

    # Random input test
    random_data = list(range(n))
    random.shuffle(random_data)

    avl2 = AVLTree()
    start = time.time()
    for val in random_data:
        avl2.insert(val)
    avl_random_time = time.time() - start

    print(f"\nRandom input ({n} elements):")
    print(f"AVL Tree height: {avl2.get_height()}")
    print(f"AVL insertion time: {avl_random_time:.4f} seconds")
    print(f"AVL rotations performed: {avl2.rotation_count}")

    # Search performance
    search_values = random.sample(range(n), min(100, n))

    start = time.time()
    for val in search_values:
        avl.search(val)
    search_time = time.time() - start

    print(f"\nSearch performance ({len(search_values)} searches):")
    print(f"AVL search time: {search_time:.4f} seconds")
    print(f"Average time per search: {search_time/len(search_values):.6f} seconds")


def test_balance_factor():
    """Test and visualize balance factor maintenance"""
    print("\n" + "=" * 60)
    print("Balance Factor Demonstration")
    print("=" * 60)

    avl = AVLTree()

    # Create an imbalanced scenario that triggers rotations
    print("\nInserting values to trigger rotations:")

    # Left-Left case
    print("\n1. Left-Left case (needs right rotation):")
    values = [30, 20, 10]
    for val in values:
        avl.insert(val)
        print(f"   Inserted {val}")
    avl.print_tree()

    # Right-Right case
    print("\n2. Right-Right case (needs left rotation):")
    values = [40, 50, 60]
    for val in values:
        avl.insert(val)
        print(f"   Inserted {val}")
    avl.print_tree()

    # Left-Right case
    print("\n3. Left-Right case (needs left-right rotation):")
    avl2 = AVLTree()
    values = [30, 10, 20]
    for val in values:
        avl2.insert(val)
        print(f"   Inserted {val}")
    avl2.print_tree()

    # Right-Left case
    print("\n4. Right-Left case (needs right-left rotation):")
    avl3 = AVLTree()
    values = [10, 30, 20]
    for val in values:
        avl3.insert(val)
        print(f"   Inserted {val}")
    avl3.print_tree()


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_avl_operations()
    compare_with_bst()
    test_balance_factor()

    print("\n" + "=" * 60)
    print("AVL Tree Implementation Complete!")
    print("=" * 60)