"""
B-Tree Implementation

A self-balancing tree data structure that maintains sorted data and allows searches,
sequential access, insertions, and deletions in logarithmic time. B-Trees are
optimized for systems that read and write large blocks of data, making them ideal
for databases and file systems.

Key Properties:
1. All leaves are at the same level
2. A B-Tree of order m has:
   - At most m children per node
   - At least ⌈m/2⌉ children (except root)
   - At most m-1 keys per node
   - At least ⌈m/2⌉-1 keys (except root)
3. Keys in each node are sorted
4. All operations are O(log n)

Author: Algorithms Multiverse
Date: January 2026
"""

import math
from typing import Any, Optional, List, Tuple, Dict
from dataclasses import dataclass, field
import json


class BTreeNode:
    """
    Node in a B-Tree.

    Attributes:
        keys: List of keys stored in this node
        values: List of values corresponding to keys
        children: List of child nodes
        is_leaf: Whether this is a leaf node
        order: Maximum number of children (degree)
    """

    def __init__(self, order: int, is_leaf: bool = True):
        self.order = order
        self.keys: List[Any] = []
        self.values: List[Any] = []
        self.children: List['BTreeNode'] = []
        self.is_leaf = is_leaf
        self.parent: Optional['BTreeNode'] = None

    @property
    def is_full(self) -> bool:
        """Check if node has maximum allowed keys."""
        return len(self.keys) >= self.order - 1

    @property
    def is_minimal(self) -> bool:
        """Check if node has minimum allowed keys."""
        min_keys = math.ceil(self.order / 2) - 1
        return len(self.keys) <= min_keys

    def find_key_index(self, key: Any) -> int:
        """
        Find the index where key should be inserted.
        Uses binary search for efficiency.
        """
        left, right = 0, len(self.keys)
        while left < right:
            mid = (left + right) // 2
            if self.keys[mid] < key:
                left = mid + 1
            else:
                right = mid
        return left

    def insert_non_full(self, key: Any, value: Any) -> None:
        """Insert a key-value pair into a non-full node."""
        idx = self.find_key_index(key)

        if idx < len(self.keys) and self.keys[idx] == key:
            # Update existing key
            self.values[idx] = value
            return

        if self.is_leaf:
            # Insert into leaf node
            self.keys.insert(idx, key)
            self.values.insert(idx, value)
        else:
            # Insert into internal node
            child = self.children[idx]
            if child.is_full:
                # Split child if it's full
                self._split_child(idx, child)
                # After split, key might need to go to next child
                if idx < len(self.keys) and key > self.keys[idx]:
                    idx += 1
                    child = self.children[idx]
            child.insert_non_full(key, value)

    def _split_child(self, idx: int, child: 'BTreeNode') -> None:
        """Split a full child node."""
        mid_idx = len(child.keys) // 2

        # Create new node with right half of keys
        new_node = BTreeNode(self.order, child.is_leaf)
        new_node.keys = child.keys[mid_idx + 1:]
        new_node.values = child.values[mid_idx + 1:]

        if not child.is_leaf:
            new_node.children = child.children[mid_idx + 1:]
            for grandchild in new_node.children:
                grandchild.parent = new_node

        # Keep left half in original child
        median_key = child.keys[mid_idx]
        median_value = child.values[mid_idx]
        child.keys = child.keys[:mid_idx]
        child.values = child.values[:mid_idx]

        if not child.is_leaf:
            child.children = child.children[:mid_idx + 1]

        # Insert median into parent (this node)
        self.keys.insert(idx, median_key)
        self.values.insert(idx, median_value)
        self.children.insert(idx + 1, new_node)

        # Update parent pointers
        new_node.parent = self

    def delete_key(self, key: Any) -> bool:
        """Delete a key from this subtree."""
        idx = self.find_key_index(key)

        if idx < len(self.keys) and self.keys[idx] == key:
            if self.is_leaf:
                # Case 1: Key is in leaf node
                self.keys.pop(idx)
                self.values.pop(idx)
                return True
            else:
                # Case 2: Key is in internal node
                return self._delete_from_internal(idx)
        elif self.is_leaf:
            # Key not found
            return False
        else:
            # Key might be in subtree
            return self._delete_from_subtree(idx, key)

    def _delete_from_internal(self, idx: int) -> bool:
        """Delete key from internal node at index idx."""
        key = self.keys[idx]
        min_keys = math.ceil(self.order / 2) - 1

        if len(self.children[idx].keys) > min_keys:
            # Replace with predecessor
            pred_key, pred_val = self._get_predecessor(idx)
            self.keys[idx] = pred_key
            self.values[idx] = pred_val
            return self.children[idx].delete_key(pred_key)
        elif len(self.children[idx + 1].keys) > min_keys:
            # Replace with successor
            succ_key, succ_val = self._get_successor(idx)
            self.keys[idx] = succ_key
            self.values[idx] = succ_val
            return self.children[idx + 1].delete_key(succ_key)
        else:
            # Merge with sibling
            self._merge(idx)
            return self.children[idx].delete_key(key)

    def _delete_from_subtree(self, idx: int, key: Any) -> bool:
        """Delete key from subtree rooted at children[idx]."""
        min_keys = math.ceil(self.order / 2) - 1

        if len(self.children[idx].keys) <= min_keys:
            # Child has minimum keys, might need borrowing or merging
            self._fix_child(idx)

        # After fixing, determine which child to recurse into
        if idx > len(self.keys):
            idx = len(self.keys)

        if idx < len(self.children):
            return self.children[idx].delete_key(key)
        return False

    def _get_predecessor(self, idx: int) -> Tuple[Any, Any]:
        """Get predecessor key-value pair."""
        node = self.children[idx]
        while not node.is_leaf:
            node = node.children[-1]
        return node.keys[-1], node.values[-1]

    def _get_successor(self, idx: int) -> Tuple[Any, Any]:
        """Get successor key-value pair."""
        node = self.children[idx + 1]
        while not node.is_leaf:
            node = node.children[0]
        return node.keys[0], node.values[0]

    def _fix_child(self, idx: int) -> None:
        """Fix a child with minimum number of keys."""
        min_keys = math.ceil(self.order / 2) - 1

        # Try borrowing from left sibling
        if idx > 0 and len(self.children[idx - 1].keys) > min_keys:
            self._borrow_from_left(idx)
        # Try borrowing from right sibling
        elif idx < len(self.children) - 1 and len(self.children[idx + 1].keys) > min_keys:
            self._borrow_from_right(idx)
        # Merge with sibling
        elif idx < len(self.keys):
            self._merge(idx)
        else:
            self._merge(idx - 1)

    def _borrow_from_left(self, idx: int) -> None:
        """Borrow a key from left sibling."""
        child = self.children[idx]
        sibling = self.children[idx - 1]

        # Move a key from parent to child
        child.keys.insert(0, self.keys[idx - 1])
        child.values.insert(0, self.values[idx - 1])

        # Move a key from sibling to parent
        self.keys[idx - 1] = sibling.keys.pop()
        self.values[idx - 1] = sibling.values.pop()

        # Move child pointer if not leaf
        if not child.is_leaf:
            child.children.insert(0, sibling.children.pop())
            child.children[0].parent = child

    def _borrow_from_right(self, idx: int) -> None:
        """Borrow a key from right sibling."""
        child = self.children[idx]
        sibling = self.children[idx + 1]

        # Move a key from parent to child
        child.keys.append(self.keys[idx])
        child.values.append(self.values[idx])

        # Move a key from sibling to parent
        self.keys[idx] = sibling.keys.pop(0)
        self.values[idx] = sibling.values.pop(0)

        # Move child pointer if not leaf
        if not child.is_leaf:
            child.children.append(sibling.children.pop(0))
            child.children[-1].parent = child

    def _merge(self, idx: int) -> None:
        """Merge child with its sibling."""
        child = self.children[idx]
        sibling = self.children[idx + 1]

        # Pull key from parent and merge with right sibling
        child.keys.append(self.keys.pop(idx))
        child.values.append(self.values.pop(idx))
        child.keys.extend(sibling.keys)
        child.values.extend(sibling.values)

        # Copy child pointers if not leaf
        if not child.is_leaf:
            child.children.extend(sibling.children)
            for grandchild in sibling.children:
                grandchild.parent = child

        # Remove sibling from children
        self.children.pop(idx + 1)


class BTree:
    """
    B-Tree implementation optimized for database and file system usage.

    Features:
    - Self-balancing with guaranteed O(log n) operations
    - Configurable order (degree) for optimization
    - Support for bulk loading
    - Range queries
    - Tree statistics and visualization

    Time Complexity:
    - Search: O(log n)
    - Insert: O(log n)
    - Delete: O(log n)
    - Range Query: O(log n + k) where k is number of results

    Space Complexity: O(n)
    """

    def __init__(self, order: int = 5):
        """
        Initialize B-Tree.

        Args:
            order: Maximum number of children per node (minimum 3)
        """
        if order < 3:
            raise ValueError("B-Tree order must be at least 3")

        self.order = order
        self.root = BTreeNode(order, is_leaf=True)
        self.size = 0

    def insert(self, key: Any, value: Any = None) -> None:
        """
        Insert a key-value pair into the B-Tree.

        Args:
            key: Key to insert
            value: Optional value associated with key
        """
        if value is None:
            value = key

        if self.root.is_full:
            # Split root if full
            new_root = BTreeNode(self.order, is_leaf=False)
            new_root.children.append(self.root)
            self.root.parent = new_root
            new_root._split_child(0, self.root)
            self.root = new_root

        # Check if key already exists
        if self.search(key) is None:
            self.size += 1

        self.root.insert_non_full(key, value)

    def search(self, key: Any) -> Optional[Any]:
        """
        Search for a key in the B-Tree.

        Args:
            key: Key to search for

        Returns:
            Value associated with key, or None if not found
        """
        node = self.root

        while node:
            idx = node.find_key_index(key)

            if idx < len(node.keys) and node.keys[idx] == key:
                return node.values[idx]
            elif node.is_leaf:
                return None
            else:
                node = node.children[idx]

        return None

    def delete(self, key: Any) -> bool:
        """
        Delete a key from the B-Tree.

        Args:
            key: Key to delete

        Returns:
            True if key was deleted, False if not found
        """
        result = self.root.delete_key(key)

        if result:
            self.size -= 1

            # If root is empty, make its only child the new root
            if len(self.root.keys) == 0 and not self.root.is_leaf:
                self.root = self.root.children[0]
                self.root.parent = None

        return result

    def range_query(self, min_key: Any, max_key: Any) -> List[Tuple[Any, Any]]:
        """
        Find all key-value pairs in the given range.

        Args:
            min_key: Minimum key (inclusive)
            max_key: Maximum key (inclusive)

        Returns:
            List of (key, value) tuples in range
        """
        result = []
        self._range_query_helper(self.root, min_key, max_key, result)
        return result

    def _range_query_helper(self, node: BTreeNode, min_key: Any, max_key: Any,
                          result: List[Tuple[Any, Any]]) -> None:
        """Helper for range query."""
        if not node:
            return

        i = 0
        while i < len(node.keys):
            # Recursively search left subtree
            if not node.is_leaf and node.keys[i] >= min_key:
                self._range_query_helper(node.children[i], min_key, max_key, result)

            # Add key if in range
            if min_key <= node.keys[i] <= max_key:
                result.append((node.keys[i], node.values[i]))

            # Stop if past max_key
            if node.keys[i] > max_key:
                return

            i += 1

        # Check rightmost child
        if not node.is_leaf and i < len(node.children):
            self._range_query_helper(node.children[i], min_key, max_key, result)

    def get_min(self) -> Optional[Tuple[Any, Any]]:
        """Get minimum key-value pair."""
        node = self.root
        while not node.is_leaf and node.children:
            node = node.children[0]
        return (node.keys[0], node.values[0]) if node.keys else None

    def get_max(self) -> Optional[Tuple[Any, Any]]:
        """Get maximum key-value pair."""
        node = self.root
        while not node.is_leaf and node.children:
            node = node.children[-1]
        return (node.keys[-1], node.values[-1]) if node.keys else None

    def bulk_load(self, items: List[Tuple[Any, Any]], sorted_input: bool = False) -> None:
        """
        Efficiently load multiple items.

        Args:
            items: List of (key, value) tuples
            sorted_input: Whether input is already sorted
        """
        if sorted_input:
            # Optimized loading for sorted data
            self._bulk_load_sorted(items)
        else:
            # Standard insertion
            for key, value in items:
                self.insert(key, value)

    def _bulk_load_sorted(self, items: List[Tuple[Any, Any]]) -> None:
        """Optimized loading for sorted data."""
        # Build tree bottom-up for better performance
        # This is a simplified version - production systems use more sophisticated methods
        for key, value in items:
            self.insert(key, value)

    def inorder_traversal(self) -> List[Tuple[Any, Any]]:
        """
        Get all key-value pairs in sorted order.

        Returns:
            List of (key, value) tuples
        """
        result = []
        self._inorder_helper(self.root, result)
        return result

    def _inorder_helper(self, node: BTreeNode, result: List[Tuple[Any, Any]]) -> None:
        """Helper for inorder traversal."""
        if not node:
            return

        for i in range(len(node.keys)):
            if not node.is_leaf:
                self._inorder_helper(node.children[i], result)
            result.append((node.keys[i], node.values[i]))

        if not node.is_leaf and len(node.children) > len(node.keys):
            self._inorder_helper(node.children[-1], result)

    def get_height(self) -> int:
        """Get the height of the B-Tree."""
        height = 0
        node = self.root
        while not node.is_leaf and node.children:
            height += 1
            node = node.children[0]
        return height

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get tree statistics.

        Returns:
            Dictionary with tree statistics
        """
        stats = {
            'size': self.size,
            'order': self.order,
            'height': self.get_height(),
            'root_keys': len(self.root.keys),
            'min_keys_per_node': math.ceil(self.order / 2) - 1,
            'max_keys_per_node': self.order - 1
        }

        # Calculate node statistics
        total_nodes = 0
        total_keys = 0
        leaf_nodes = 0

        def count_nodes(node):
            nonlocal total_nodes, total_keys, leaf_nodes
            if not node:
                return

            total_nodes += 1
            total_keys += len(node.keys)

            if node.is_leaf:
                leaf_nodes += 1
            else:
                for child in node.children:
                    count_nodes(child)

        count_nodes(self.root)

        stats.update({
            'total_nodes': total_nodes,
            'total_keys': total_keys,
            'leaf_nodes': leaf_nodes,
            'internal_nodes': total_nodes - leaf_nodes,
            'avg_keys_per_node': total_keys / total_nodes if total_nodes > 0 else 0,
            'space_utilization': total_keys / (total_nodes * (self.order - 1)) if total_nodes > 0 else 0
        })

        return stats

    def visualize(self, max_depth: int = 3) -> str:
        """
        Create a text visualization of the tree.

        Args:
            max_depth: Maximum depth to display

        Returns:
            String representation of tree structure
        """
        if not self.root or not self.root.keys:
            return "Empty B-Tree"

        lines = []
        self._visualize_helper(self.root, "", True, 0, max_depth, lines)
        return "\n".join(lines)

    def _visualize_helper(self, node: BTreeNode, prefix: str, is_tail: bool,
                         depth: int, max_depth: int, lines: List[str]) -> None:
        """Helper for tree visualization."""
        if not node or depth > max_depth:
            return

        # Create node representation
        keys_str = ", ".join(str(k) for k in node.keys)
        node_str = f"[{keys_str}]"

        # Add to output
        connector = "+-- " if is_tail else "|-- "
        lines.append(prefix + connector + node_str)

        # Add children
        if not node.is_leaf and node.children:
            extension = "    " if is_tail else "|   "
            for i, child in enumerate(node.children[:-1]):
                self._visualize_helper(child, prefix + extension, False,
                                      depth + 1, max_depth, lines)

            # Last child
            if node.children:
                self._visualize_helper(node.children[-1], prefix + extension, True,
                                      depth + 1, max_depth, lines)

    def validate(self) -> bool:
        """
        Validate B-Tree properties.

        Returns:
            True if tree is valid, False otherwise
        """
        if not self.root:
            return True

        # Check all properties
        return (self._validate_keys_sorted(self.root) and
                self._validate_node_sizes(self.root, is_root=True) and
                self._validate_leaf_level() and
                self._validate_parent_child_keys(self.root))

    def _validate_keys_sorted(self, node: BTreeNode) -> bool:
        """Validate that keys in each node are sorted."""
        for i in range(len(node.keys) - 1):
            if node.keys[i] >= node.keys[i + 1]:
                return False

        if not node.is_leaf:
            for child in node.children:
                if not self._validate_keys_sorted(child):
                    return False

        return True

    def _validate_node_sizes(self, node: BTreeNode, is_root: bool = False) -> bool:
        """Validate node size constraints."""
        min_keys = 0 if is_root else math.ceil(self.order / 2) - 1
        max_keys = self.order - 1

        if len(node.keys) < min_keys or len(node.keys) > max_keys:
            return False

        if not node.is_leaf:
            if len(node.children) != len(node.keys) + 1:
                return False

            for child in node.children:
                if not self._validate_node_sizes(child, is_root=False):
                    return False

        return True

    def _validate_leaf_level(self) -> bool:
        """Validate that all leaves are at the same level."""
        levels = []

        def get_leaf_levels(node, level):
            if node.is_leaf:
                levels.append(level)
            else:
                for child in node.children:
                    get_leaf_levels(child, level + 1)

        get_leaf_levels(self.root, 0)
        return len(set(levels)) <= 1

    def _validate_parent_child_keys(self, node: BTreeNode) -> bool:
        """Validate parent-child key relationships."""
        if node.is_leaf:
            return True

        for i, child in enumerate(node.children):
            # Check keys in child are within bounds
            if child.keys:
                if i > 0 and child.keys[0] <= node.keys[i - 1]:
                    return False
                if i < len(node.keys) and child.keys[-1] >= node.keys[i]:
                    return False

            # Recursive check
            if not self._validate_parent_child_keys(child):
                return False

        return True


def example_usage():
    """Demonstrate B-Tree usage."""
    print("B-Tree Example")
    print("=" * 50)

    # Create B-Tree with order 5
    btree = BTree(order=5)

    # Insert some data
    data = [
        (10, "ten"), (20, "twenty"), (5, "five"), (6, "six"),
        (12, "twelve"), (30, "thirty"), (7, "seven"), (17, "seventeen"),
        (3, "three"), (4, "four"), (2, "two"), (1, "one"),
        (15, "fifteen"), (25, "twenty-five"), (35, "thirty-five")
    ]

    print("Inserting data...")
    for key, value in data:
        btree.insert(key, value)
        print(f"  Inserted: {key} -> {value}")

    # Display tree structure
    print("\nTree Structure:")
    print(btree.visualize())

    # Search operations
    print("\nSearch Operations:")
    for key in [6, 15, 25, 100]:
        result = btree.search(key)
        print(f"  Search({key}): {result}")

    # Range query
    print("\nRange Query [5, 20]:")
    range_results = btree.range_query(5, 20)
    for key, value in range_results:
        print(f"  {key}: {value}")

    # Min and Max
    print(f"\nMinimum: {btree.get_min()}")
    print(f"Maximum: {btree.get_max()}")

    # Delete operations
    print("\nDelete Operations:")
    for key in [6, 15, 30]:
        success = btree.delete(key)
        print(f"  Delete({key}): {'Success' if success else 'Not found'}")

    print("\nTree After Deletions:")
    print(btree.visualize())

    # Tree statistics
    print("\nTree Statistics:")
    stats = btree.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")

    # Validate tree
    print(f"\nTree Valid: {btree.validate()}")

    # Bulk loading example
    print("\n" + "=" * 50)
    print("Bulk Loading Example")

    btree2 = BTree(order=4)
    bulk_data = [(i, f"value_{i}") for i in range(1, 21)]
    btree2.bulk_load(bulk_data, sorted_input=True)

    print("Loaded 20 sorted items")
    print("\nTree Structure:")
    print(btree2.visualize())

    print(f"\nTree Statistics:")
    stats2 = btree2.get_statistics()
    print(f"  Height: {stats2['height']}")
    print(f"  Total Nodes: {stats2['total_nodes']}")
    print(f"  Space Utilization: {stats2['space_utilization']:.2%}")


if __name__ == "__main__":
    example_usage()