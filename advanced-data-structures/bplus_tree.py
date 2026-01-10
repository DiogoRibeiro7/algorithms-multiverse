"""
B+ Tree Implementation

A self-balancing tree data structure that is an extension of B-Tree, optimized
for systems that read and write large blocks of data. Unlike B-Trees, B+ Trees
store all values in leaf nodes, with internal nodes serving only as a roadmap.

Key Properties:
1. All values are stored in leaf nodes
2. Internal nodes only contain keys for navigation
3. Leaf nodes are linked for efficient sequential access
4. All leaf nodes are at the same level
5. Duplicate keys can exist (in internal nodes)
6. Perfect for database indexes and file systems

Advantages over B-Tree:
- Better sequential access due to linked leaves
- More keys fit in internal nodes (no values)
- Consistent search time (always to leaf level)
- Better cache utilization

Author: Algorithms Multiverse
Date: January 2026
"""

import math
from typing import Any, Optional, List, Tuple, Dict, Iterator
from dataclasses import dataclass
import bisect


class BPlusNode:
    """Base class for B+ Tree nodes."""

    def __init__(self, order: int):
        self.order = order
        self.keys: List[Any] = []
        self.parent: Optional['BPlusInternalNode'] = None

    @property
    def is_full(self) -> bool:
        """Check if node has maximum allowed keys."""
        return len(self.keys) >= self.order - 1

    @property
    def is_minimal(self) -> bool:
        """Check if node has minimum allowed keys."""
        min_keys = math.ceil(self.order / 2) - 1
        return len(self.keys) <= min_keys


class BPlusLeafNode(BPlusNode):
    """
    Leaf node in a B+ Tree.
    Stores actual key-value pairs and maintains links to siblings.
    """

    def __init__(self, order: int):
        super().__init__(order)
        self.values: List[Any] = []
        self.next_leaf: Optional['BPlusLeafNode'] = None
        self.prev_leaf: Optional['BPlusLeafNode'] = None

    def insert(self, key: Any, value: Any) -> Optional[Tuple['BPlusLeafNode', Any]]:
        """
        Insert a key-value pair into the leaf.

        Returns:
            Tuple of (new_node, split_key) if split occurred, None otherwise
        """
        # Find insertion position
        idx = bisect.bisect_left(self.keys, key)

        # Update if key exists
        if idx < len(self.keys) and self.keys[idx] == key:
            self.values[idx] = value
            return None

        # Insert at position
        self.keys.insert(idx, key)
        self.values.insert(idx, value)

        # Split if overfull
        if len(self.keys) > self.order - 1:
            return self._split()

        return None

    def _split(self) -> Tuple['BPlusLeafNode', Any]:
        """
        Split the leaf node.

        Returns:
            Tuple of (new_node, split_key)
        """
        mid_idx = len(self.keys) // 2

        # Create new leaf with right half
        new_leaf = BPlusLeafNode(self.order)
        new_leaf.keys = self.keys[mid_idx:]
        new_leaf.values = self.values[mid_idx:]

        # Keep left half in current node
        self.keys = self.keys[:mid_idx]
        self.values = self.values[:mid_idx]

        # Update linked list pointers
        new_leaf.next_leaf = self.next_leaf
        new_leaf.prev_leaf = self
        if self.next_leaf:
            self.next_leaf.prev_leaf = new_leaf
        self.next_leaf = new_leaf

        # Split key is the first key of new leaf (for parent)
        split_key = new_leaf.keys[0]

        return new_leaf, split_key

    def delete(self, key: Any) -> bool:
        """
        Delete a key from the leaf.

        Returns:
            True if key was deleted, False if not found
        """
        idx = bisect.bisect_left(self.keys, key)

        if idx < len(self.keys) and self.keys[idx] == key:
            self.keys.pop(idx)
            self.values.pop(idx)
            return True

        return False

    def borrow_from_left(self, left_sibling: 'BPlusLeafNode', parent_idx: int) -> None:
        """Borrow a key-value pair from left sibling."""
        # Move rightmost key-value from sibling to front
        self.keys.insert(0, left_sibling.keys.pop())
        self.values.insert(0, left_sibling.values.pop())

        # Update parent key
        if self.parent:
            self.parent.keys[parent_idx] = self.keys[0]

    def borrow_from_right(self, right_sibling: 'BPlusLeafNode', parent_idx: int) -> None:
        """Borrow a key-value pair from right sibling."""
        # Move leftmost key-value from sibling to end
        self.keys.append(right_sibling.keys.pop(0))
        self.values.append(right_sibling.values.pop(0))

        # Update parent key
        if self.parent:
            self.parent.keys[parent_idx] = right_sibling.keys[0]

    def merge_with_right(self, right_sibling: 'BPlusLeafNode') -> None:
        """Merge with right sibling."""
        # Combine keys and values
        self.keys.extend(right_sibling.keys)
        self.values.extend(right_sibling.values)

        # Update linked list pointers
        self.next_leaf = right_sibling.next_leaf
        if right_sibling.next_leaf:
            right_sibling.next_leaf.prev_leaf = self


class BPlusInternalNode(BPlusNode):
    """
    Internal node in a B+ Tree.
    Only stores keys for navigation, no values.
    """

    def __init__(self, order: int):
        super().__init__(order)
        self.children: List[BPlusNode] = []

    def insert_after_split(self, child: BPlusNode, new_node: BPlusNode, split_key: Any) -> Optional[Tuple['BPlusInternalNode', Any]]:
        """
        Insert a new child after a split.

        Returns:
            Tuple of (new_node, split_key) if this node splits, None otherwise
        """
        # Find position of original child
        child_idx = self.children.index(child)

        # Insert split key and new child
        self.keys.insert(child_idx, split_key)
        self.children.insert(child_idx + 1, new_node)

        # Update parent pointers
        new_node.parent = self

        # Split if overfull
        if len(self.keys) > self.order - 1:
            return self._split()

        return None

    def _split(self) -> Tuple['BPlusInternalNode', Any]:
        """
        Split the internal node.

        Returns:
            Tuple of (new_node, split_key)
        """
        mid_idx = len(self.keys) // 2

        # Create new internal node with right half
        new_internal = BPlusInternalNode(self.order)
        new_internal.keys = self.keys[mid_idx + 1:]
        new_internal.children = self.children[mid_idx + 1:]

        # Update parent pointers for moved children
        for child in new_internal.children:
            child.parent = new_internal

        # Keep left half in current node
        split_key = self.keys[mid_idx]
        self.keys = self.keys[:mid_idx]
        self.children = self.children[:mid_idx + 1]

        return new_internal, split_key

    def delete_child_key(self, child_idx: int) -> None:
        """Remove a child and its associated key."""
        if child_idx > 0:
            self.keys.pop(child_idx - 1)
        elif child_idx < len(self.keys):
            self.keys.pop(child_idx)
        self.children.pop(child_idx)

    def borrow_from_left(self, left_sibling: 'BPlusInternalNode', parent_idx: int) -> None:
        """Borrow a key and child from left sibling."""
        # Move parent key down
        self.keys.insert(0, self.parent.keys[parent_idx])

        # Move sibling's rightmost key up to parent
        self.parent.keys[parent_idx] = left_sibling.keys.pop()

        # Move sibling's rightmost child
        borrowed_child = left_sibling.children.pop()
        self.children.insert(0, borrowed_child)
        borrowed_child.parent = self

    def borrow_from_right(self, right_sibling: 'BPlusInternalNode', parent_idx: int) -> None:
        """Borrow a key and child from right sibling."""
        # Move parent key down
        self.keys.append(self.parent.keys[parent_idx])

        # Move sibling's leftmost key up to parent
        self.parent.keys[parent_idx] = right_sibling.keys.pop(0)

        # Move sibling's leftmost child
        borrowed_child = right_sibling.children.pop(0)
        self.children.append(borrowed_child)
        borrowed_child.parent = self

    def merge_with_right(self, right_sibling: 'BPlusInternalNode', parent_key: Any) -> None:
        """Merge with right sibling."""
        # Add parent key
        self.keys.append(parent_key)

        # Combine keys and children
        self.keys.extend(right_sibling.keys)
        self.children.extend(right_sibling.children)

        # Update parent pointers
        for child in right_sibling.children:
            child.parent = self


class BPlusTree:
    """
    B+ Tree implementation optimized for database indexing and range queries.

    Features:
    - All values stored in leaves for better cache utilization
    - Linked leaf nodes for efficient sequential access
    - Internal nodes only store keys (more keys per node)
    - Support for duplicate key handling
    - Efficient range queries and bulk operations
    - Iterator support for sequential access

    Time Complexity:
    - Search: O(log n)
    - Insert: O(log n)
    - Delete: O(log n)
    - Range Query: O(log n + k) where k is number of results
    - Sequential Scan: O(n)

    Space Complexity: O(n)
    """

    def __init__(self, order: int = 5):
        """
        Initialize B+ Tree.

        Args:
            order: Maximum number of children per node (minimum 3)
        """
        if order < 3:
            raise ValueError("B+ Tree order must be at least 3")

        self.order = order
        self.root = BPlusLeafNode(order)
        self.size = 0

    def insert(self, key: Any, value: Any = None) -> None:
        """
        Insert a key-value pair into the B+ Tree.

        Args:
            key: Key to insert
            value: Optional value associated with key
        """
        if value is None:
            value = key

        # Check if key exists (for size tracking)
        if self.search(key) is None:
            self.size += 1

        # Find leaf node
        leaf = self._find_leaf(key)

        # Insert into leaf
        result = leaf.insert(key, value)

        # Handle split if needed
        if result:
            new_node, split_key = result
            self._handle_split(leaf, new_node, split_key)

    def _handle_split(self, original_node: BPlusNode, new_node: BPlusNode, split_key: Any) -> None:
        """Handle node split propagation."""
        if original_node.parent is None:
            # Create new root
            new_root = BPlusInternalNode(self.order)
            new_root.keys = [split_key]
            new_root.children = [original_node, new_node]
            original_node.parent = new_root
            new_node.parent = new_root
            self.root = new_root
        else:
            # Insert into parent
            parent = original_node.parent
            result = parent.insert_after_split(original_node, new_node, split_key)

            # Propagate split if needed
            if result:
                new_parent, parent_split_key = result
                self._handle_split(parent, new_parent, parent_split_key)

    def search(self, key: Any) -> Optional[Any]:
        """
        Search for a key in the B+ Tree.

        Args:
            key: Key to search for

        Returns:
            Value associated with key, or None if not found
        """
        leaf = self._find_leaf(key)
        idx = bisect.bisect_left(leaf.keys, key)

        if idx < len(leaf.keys) and leaf.keys[idx] == key:
            return leaf.values[idx]

        return None

    def _find_leaf(self, key: Any) -> BPlusLeafNode:
        """Find the leaf node where key should be."""
        node = self.root

        while not isinstance(node, BPlusLeafNode):
            idx = bisect.bisect_right(node.keys, key)
            node = node.children[idx]

        return node

    def delete(self, key: Any) -> bool:
        """
        Delete a key from the B+ Tree.

        Args:
            key: Key to delete

        Returns:
            True if key was deleted, False if not found
        """
        leaf = self._find_leaf(key)

        if not leaf.delete(key):
            return False

        self.size -= 1

        # Handle underflow
        self._handle_delete(leaf)

        return True

    def _handle_delete(self, node: BPlusNode) -> None:
        """Handle node underflow after deletion."""
        min_keys = math.ceil(self.order / 2) - 1

        # Root node special case
        if node == self.root:
            if isinstance(self.root, BPlusInternalNode) and len(self.root.keys) == 0:
                # Make only child the new root
                self.root = self.root.children[0]
                self.root.parent = None
            return

        # Check if underflow
        if len(node.keys) >= min_keys:
            return

        parent = node.parent
        node_idx = parent.children.index(node)

        # Try borrowing from or merging with siblings
        if node_idx > 0:
            left_sibling = parent.children[node_idx - 1]
            if len(left_sibling.keys) > min_keys:
                # Borrow from left
                if isinstance(node, BPlusLeafNode):
                    node.borrow_from_left(left_sibling, node_idx - 1)
                else:
                    node.borrow_from_left(left_sibling, node_idx - 1)
                return

        if node_idx < len(parent.children) - 1:
            right_sibling = parent.children[node_idx + 1]
            if len(right_sibling.keys) > min_keys:
                # Borrow from right
                if isinstance(node, BPlusLeafNode):
                    node.borrow_from_right(right_sibling, node_idx)
                else:
                    node.borrow_from_right(right_sibling, node_idx)
                return

        # Merge with sibling
        if node_idx > 0:
            # Merge with left sibling
            left_sibling = parent.children[node_idx - 1]
            if isinstance(node, BPlusLeafNode):
                left_sibling.merge_with_right(node)
            else:
                left_sibling.merge_with_right(node, parent.keys[node_idx - 1])
            parent.delete_child_key(node_idx)
        else:
            # Merge with right sibling
            right_sibling = parent.children[node_idx + 1]
            if isinstance(node, BPlusLeafNode):
                node.merge_with_right(right_sibling)
            else:
                node.merge_with_right(right_sibling, parent.keys[node_idx])
            parent.delete_child_key(node_idx + 1)

        # Handle parent underflow
        self._handle_delete(parent)

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

        # Find starting leaf
        leaf = self._find_leaf(min_key)

        # Scan through linked leaves
        while leaf:
            for i, key in enumerate(leaf.keys):
                if key > max_key:
                    return result
                if key >= min_key:
                    result.append((key, leaf.values[i]))

            leaf = leaf.next_leaf

        return result

    def get_min(self) -> Optional[Tuple[Any, Any]]:
        """Get minimum key-value pair."""
        # Find leftmost leaf
        node = self.root
        while not isinstance(node, BPlusLeafNode):
            node = node.children[0]

        if node.keys:
            return (node.keys[0], node.values[0])
        return None

    def get_max(self) -> Optional[Tuple[Any, Any]]:
        """Get maximum key-value pair."""
        # Find rightmost leaf
        node = self.root
        while not isinstance(node, BPlusLeafNode):
            node = node.children[-1]

        if node.keys:
            return (node.keys[-1], node.values[-1])
        return None

    def bulk_load(self, items: List[Tuple[Any, Any]], sorted_input: bool = False) -> None:
        """
        Efficiently load multiple items.

        Args:
            items: List of (key, value) tuples
            sorted_input: Whether input is already sorted
        """
        if not items:
            return

        if sorted_input:
            # Build tree bottom-up for sorted data
            self._bulk_load_sorted(items)
        else:
            # Standard insertion
            for key, value in items:
                self.insert(key, value)

    def _bulk_load_sorted(self, items: List[Tuple[Any, Any]]) -> None:
        """
        Optimized bulk loading for sorted data.
        Builds tree bottom-up for better performance.
        """
        # Create leaf nodes
        leaves = []
        current_leaf = BPlusLeafNode(self.order)
        leaves.append(current_leaf)

        for key, value in items:
            if len(current_leaf.keys) >= self.order - 1:
                # Create new leaf
                new_leaf = BPlusLeafNode(self.order)
                current_leaf.next_leaf = new_leaf
                new_leaf.prev_leaf = current_leaf
                leaves.append(new_leaf)
                current_leaf = new_leaf

            current_leaf.keys.append(key)
            current_leaf.values.append(value)

        # Build tree bottom-up
        self._build_tree_from_leaves(leaves)
        self.size = len(items)

    def _build_tree_from_leaves(self, leaves: List[BPlusLeafNode]) -> None:
        """Build tree structure from leaf nodes."""
        if len(leaves) == 1:
            self.root = leaves[0]
            return

        # Build internal nodes level by level
        current_level = leaves
        while len(current_level) > 1:
            next_level = []
            current_parent = BPlusInternalNode(self.order)
            next_level.append(current_parent)

            for i, node in enumerate(current_level):
                # Add to current parent
                node.parent = current_parent
                current_parent.children.append(node)

                # Add separator key (except for first child)
                if i > 0:
                    if isinstance(node, BPlusLeafNode):
                        current_parent.keys.append(node.keys[0])
                    else:
                        # Use appropriate key from internal node
                        current_parent.keys.append(node.keys[0] if node.keys else None)

                # Check if parent is full
                if len(current_parent.children) >= self.order:
                    current_parent = BPlusInternalNode(self.order)
                    next_level.append(current_parent)

            current_level = next_level

        self.root = current_level[0]

    def __iter__(self) -> Iterator[Tuple[Any, Any]]:
        """Iterate over all key-value pairs in sorted order."""
        # Find leftmost leaf
        node = self.root
        while not isinstance(node, BPlusLeafNode):
            node = node.children[0]

        # Iterate through linked leaves
        while node:
            for key, value in zip(node.keys, node.values):
                yield (key, value)
            node = node.next_leaf

    def get_height(self) -> int:
        """Get the height of the B+ Tree."""
        height = 0
        node = self.root
        while not isinstance(node, BPlusLeafNode):
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
            'min_keys_per_node': math.ceil(self.order / 2) - 1,
            'max_keys_per_node': self.order - 1
        }

        # Calculate node statistics
        total_nodes = 0
        internal_nodes = 0
        leaf_nodes = 0
        total_keys = 0
        total_values = 0

        def count_nodes(node):
            nonlocal total_nodes, internal_nodes, leaf_nodes, total_keys, total_values

            total_nodes += 1
            total_keys += len(node.keys)

            if isinstance(node, BPlusLeafNode):
                leaf_nodes += 1
                total_values += len(node.values)
            else:
                internal_nodes += 1
                for child in node.children:
                    count_nodes(child)

        count_nodes(self.root)

        stats.update({
            'total_nodes': total_nodes,
            'internal_nodes': internal_nodes,
            'leaf_nodes': leaf_nodes,
            'total_keys': total_keys,
            'total_values': total_values,
            'avg_keys_per_node': total_keys / total_nodes if total_nodes > 0 else 0,
            'space_utilization': total_keys / (total_nodes * (self.order - 1)) if total_nodes > 0 else 0,
            'values_per_leaf': total_values / leaf_nodes if leaf_nodes > 0 else 0
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
        if not self.root:
            return "Empty B+ Tree"

        lines = []
        self._visualize_helper(self.root, "", True, 0, max_depth, lines)
        return "\n".join(lines)

    def _visualize_helper(self, node: BPlusNode, prefix: str, is_tail: bool,
                         depth: int, max_depth: int, lines: List[str]) -> None:
        """Helper for tree visualization."""
        if not node or depth > max_depth:
            return

        # Create node representation
        if isinstance(node, BPlusLeafNode):
            items_str = ", ".join(f"{k}:{v}" for k, v in zip(node.keys, node.values))
            node_str = f"Leaf[{items_str}]"
        else:
            keys_str = ", ".join(str(k) for k in node.keys)
            node_str = f"Internal[{keys_str}]"

        # Add to output
        connector = "+-- " if is_tail else "|-- "
        lines.append(prefix + connector + node_str)

        # Add children for internal nodes
        if isinstance(node, BPlusInternalNode):
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
        Validate B+ Tree properties.

        Returns:
            True if tree is valid, False otherwise
        """
        if not self.root:
            return True

        # Check all properties
        return (self._validate_structure() and
                self._validate_keys() and
                self._validate_leaf_links() and
                self._validate_parent_pointers())

    def _validate_structure(self) -> bool:
        """Validate tree structure properties."""
        # All leaves at same level
        leaf_levels = []

        def check_leaves(node, level):
            if isinstance(node, BPlusLeafNode):
                leaf_levels.append(level)
            else:
                for child in node.children:
                    check_leaves(child, level + 1)

        check_leaves(self.root, 0)
        if len(set(leaf_levels)) > 1:
            return False

        # Node size constraints
        min_keys = math.ceil(self.order / 2) - 1

        def check_node_sizes(node, is_root=False):
            min_allowed = 0 if is_root else min_keys
            max_allowed = self.order - 1

            if len(node.keys) < min_allowed or len(node.keys) > max_allowed:
                return False

            if isinstance(node, BPlusInternalNode):
                if len(node.children) != len(node.keys) + 1:
                    return False
                for child in node.children:
                    if not check_node_sizes(child, is_root=False):
                        return False

            return True

        return check_node_sizes(self.root, is_root=True)

    def _validate_keys(self) -> bool:
        """Validate key ordering properties."""

        def check_keys(node):
            # Keys in node are sorted
            for i in range(len(node.keys) - 1):
                if node.keys[i] >= node.keys[i + 1]:
                    return False

            # Check internal node key relationships
            if isinstance(node, BPlusInternalNode):
                for i, child in enumerate(node.children):
                    # Recursively check children
                    if not check_keys(child):
                        return False

                    # Check separator keys
                    if isinstance(child, BPlusLeafNode):
                        if i > 0 and child.keys[0] != node.keys[i - 1]:
                            return False

            return True

        return check_keys(self.root)

    def _validate_leaf_links(self) -> bool:
        """Validate leaf node linked list."""
        # Find leftmost leaf
        node = self.root
        while not isinstance(node, BPlusLeafNode):
            node = node.children[0]

        prev_max = None
        while node:
            # Check ordering between leaves
            if prev_max is not None and node.keys and node.keys[0] <= prev_max:
                return False

            # Check bidirectional links
            if node.next_leaf and node.next_leaf.prev_leaf != node:
                return False

            prev_max = node.keys[-1] if node.keys else None
            node = node.next_leaf

        return True

    def _validate_parent_pointers(self) -> bool:
        """Validate parent-child pointer consistency."""

        def check_parents(node):
            if isinstance(node, BPlusInternalNode):
                for child in node.children:
                    if child.parent != node:
                        return False
                    if not check_parents(child):
                        return False
            return True

        return check_parents(self.root)


def example_usage():
    """Demonstrate B+ Tree usage."""
    print("B+ Tree Example")
    print("=" * 50)

    # Create B+ Tree with order 4
    bplus = BPlusTree(order=4)

    # Insert some data
    data = [
        (10, "ten"), (20, "twenty"), (5, "five"), (6, "six"),
        (12, "twelve"), (30, "thirty"), (7, "seven"), (17, "seventeen"),
        (3, "three"), (4, "four"), (2, "two"), (1, "one"),
        (15, "fifteen"), (25, "twenty-five"), (35, "thirty-five")
    ]

    print("Inserting data...")
    for key, value in data:
        bplus.insert(key, value)
        print(f"  Inserted: {key} -> {value}")

    # Display tree structure
    print("\nTree Structure:")
    print(bplus.visualize())

    # Search operations
    print("\nSearch Operations:")
    for key in [6, 15, 25, 100]:
        result = bplus.search(key)
        print(f"  Search({key}): {result}")

    # Range query
    print("\nRange Query [5, 20]:")
    range_results = bplus.range_query(5, 20)
    for key, value in range_results:
        print(f"  {key}: {value}")

    # Sequential scan using iterator
    print("\nFirst 5 items (sequential scan):")
    for i, (key, value) in enumerate(bplus):
        if i >= 5:
            break
        print(f"  {key}: {value}")

    # Min and Max
    print(f"\nMinimum: {bplus.get_min()}")
    print(f"Maximum: {bplus.get_max()}")

    # Delete operations
    print("\nDelete Operations:")
    for key in [6, 15, 30]:
        success = bplus.delete(key)
        print(f"  Delete({key}): {'Success' if success else 'Not found'}")

    print("\nTree After Deletions:")
    print(bplus.visualize())

    # Tree statistics
    print("\nTree Statistics:")
    stats = bplus.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")

    # Validate tree
    print(f"\nTree Valid: {bplus.validate()}")

    # Bulk loading example
    print("\n" + "=" * 50)
    print("Bulk Loading Example (Sorted Data)")

    bplus2 = BPlusTree(order=5)
    bulk_data = [(i, f"value_{i}") for i in range(1, 51)]
    bplus2.bulk_load(bulk_data, sorted_input=True)

    print("Loaded 50 sorted items")
    print("\nTree Structure:")
    print(bplus2.visualize(max_depth=2))

    print(f"\nTree Statistics:")
    stats2 = bplus2.get_statistics()
    print(f"  Height: {stats2['height']}")
    print(f"  Total Nodes: {stats2['total_nodes']}")
    print(f"  Internal Nodes: {stats2['internal_nodes']}")
    print(f"  Leaf Nodes: {stats2['leaf_nodes']}")
    print(f"  Space Utilization: {stats2['space_utilization']:.2%}")

    # Demonstrate leaf linking
    print("\n" + "=" * 50)
    print("Leaf Node Linking (Sequential Access)")

    # Range query is efficient due to linked leaves
    print("\nRange [15, 35]:")
    for key, value in bplus2.range_query(15, 35):
        print(f"  {key}: {value}")

    print("\nB+ Tree vs B-Tree Comparison:")
    print("  B+ Tree Advantages:")
    print("    - All values in leaves (better cache utilization)")
    print("    - Linked leaves (efficient range queries)")
    print("    - More keys per internal node (shallower tree)")
    print("    - Consistent search time (always to leaf)")
    print("    - Better for sequential access patterns")


if __name__ == "__main__":
    example_usage()