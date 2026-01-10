#!/usr/bin/env python3
"""
Red-Black Tree Implementation

A self-balancing binary search tree where each node has an additional color
attribute (red or black). The tree maintains balance through color properties
and rotations, ensuring O(log n) worst-case time for basic operations.

Properties:
1. Every node is either red or black
2. The root is black
3. All leaves (NIL) are black
4. Red nodes cannot have red children (no red-red parent-child)
5. All paths from root to leaves have the same number of black nodes

Author: Algorithms Multiverse
License: MIT
"""

from typing import Optional, List, Tuple, Any, Generator
from dataclasses import dataclass
from enum import Enum
import sys


class Color(Enum):
    """Node colors for Red-Black Tree"""
    RED = 0
    BLACK = 1


@dataclass
class RBNode:
    """Node in a Red-Black Tree"""
    key: int
    value: Any = None
    color: Color = Color.RED
    parent: Optional['RBNode'] = None
    left: Optional['RBNode'] = None
    right: Optional['RBNode'] = None

    def __repr__(self) -> str:
        color_str = "R" if self.color == Color.RED else "B"
        return f"RBNode({self.key}:{color_str})"


class RBTree:
    """
    Red-Black Tree implementation with insert, delete, search operations.

    Provides O(log n) guaranteed worst-case time complexity for basic operations
    through color-based balancing rules and rotations.
    """

    def __init__(self):
        """Initialize an empty Red-Black Tree with NIL sentinel"""
        self.NIL = RBNode(key=0, color=Color.BLACK)
        self.root = self.NIL
        self._size = 0

    @property
    def size(self) -> int:
        """Return the number of nodes in the tree"""
        return self._size

    def is_empty(self) -> bool:
        """Check if the tree is empty"""
        return self.root == self.NIL

    def insert(self, key: int, value: Any = None) -> None:
        """
        Insert a new key-value pair into the tree.

        Args:
            key: The key to insert
            value: Optional value associated with the key
        """
        # Create new node
        z = RBNode(key=key, value=value, color=Color.RED)
        z.left = self.NIL
        z.right = self.NIL

        # Find insertion position
        y = self.NIL
        x = self.root

        while x != self.NIL:
            y = x
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                # Key already exists, update value
                x.value = value
                return

        # Set parent
        z.parent = y

        # Insert as root or child
        if y == self.NIL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        self._size += 1

        # Fix Red-Black properties
        self._insert_fixup(z)

    def _insert_fixup(self, z: RBNode) -> None:
        """Fix Red-Black tree properties after insertion"""
        while z.parent and z.parent.color == Color.RED:
            if z.parent == z.parent.parent.left:
                # Parent is left child
                y = z.parent.parent.right  # Uncle

                if y.color == Color.RED:
                    # Case 1: Uncle is red
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        # Case 2: z is right child
                        z = z.parent
                        self._rotate_left(z)
                    # Case 3: z is left child
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self._rotate_right(z.parent.parent)
            else:
                # Parent is right child (symmetric cases)
                y = z.parent.parent.left  # Uncle

                if y.color == Color.RED:
                    # Case 1: Uncle is red
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        # Case 2: z is left child
                        z = z.parent
                        self._rotate_right(z)
                    # Case 3: z is right child
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self._rotate_left(z.parent.parent)

        # Ensure root is black
        self.root.color = Color.BLACK

    def delete(self, key: int) -> bool:
        """
        Delete a node with the given key from the tree.

        Args:
            key: The key to delete

        Returns:
            True if the key was found and deleted, False otherwise
        """
        z = self._find_node(key)
        if z == self.NIL:
            return False

        self._delete_node(z)
        self._size -= 1
        return True

    def _delete_node(self, z: RBNode) -> None:
        """Delete a node from the tree and fix properties"""
        y = z
        y_original_color = y.color

        if z.left == self.NIL:
            # No left child
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            # No right child
            x = z.left
            self._transplant(z, z.left)
        else:
            # Two children - find successor
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right

            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        # Fix properties if a black node was removed
        if y_original_color == Color.BLACK:
            self._delete_fixup(x)

    def _delete_fixup(self, x: RBNode) -> None:
        """Fix Red-Black tree properties after deletion"""
        while x != self.root and x.color == Color.BLACK:
            if x == x.parent.left:
                w = x.parent.right  # Sibling

                if w.color == Color.RED:
                    # Case 1: Sibling is red
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self._rotate_left(x.parent)
                    w = x.parent.right

                if w.left.color == Color.BLACK and w.right.color == Color.BLACK:
                    # Case 2: Both of sibling's children are black
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.right.color == Color.BLACK:
                        # Case 3: Sibling's right child is black
                        w.left.color = Color.BLACK
                        w.color = Color.RED
                        self._rotate_right(w)
                        w = x.parent.right
                    # Case 4: Sibling's right child is red
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.right.color = Color.BLACK
                    self._rotate_left(x.parent)
                    x = self.root
            else:
                # Symmetric cases
                w = x.parent.left  # Sibling

                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self._rotate_right(x.parent)
                    w = x.parent.left

                if w.right.color == Color.BLACK and w.left.color == Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.left.color == Color.BLACK:
                        w.right.color = Color.BLACK
                        w.color = Color.RED
                        self._rotate_left(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.left.color = Color.BLACK
                    self._rotate_right(x.parent)
                    x = self.root

        x.color = Color.BLACK

    def _rotate_left(self, x: RBNode) -> None:
        """Perform left rotation around node x"""
        y = x.right
        x.right = y.left

        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _rotate_right(self, x: RBNode) -> None:
        """Perform right rotation around node x"""
        y = x.left
        x.left = y.right

        if y.right != self.NIL:
            y.right.parent = x

        y.parent = x.parent

        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def _transplant(self, u: RBNode, v: RBNode) -> None:
        """Replace subtree rooted at u with subtree rooted at v"""
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def search(self, key: int) -> Optional[Any]:
        """
        Search for a key in the tree and return its value.

        Args:
            key: The key to search for

        Returns:
            The value associated with the key, or None if not found
        """
        node = self._find_node(key)
        return node.value if node != self.NIL else None

    def contains(self, key: int) -> bool:
        """Check if a key exists in the tree"""
        return self._find_node(key) != self.NIL

    def _find_node(self, key: int) -> RBNode:
        """Find a node with the given key"""
        x = self.root
        while x != self.NIL:
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                return x
        return self.NIL

    def get_min(self) -> Optional[int]:
        """Get the minimum key in the tree"""
        if self.root == self.NIL:
            return None
        return self._minimum(self.root).key

    def get_max(self) -> Optional[int]:
        """Get the maximum key in the tree"""
        if self.root == self.NIL:
            return None
        return self._maximum(self.root).key

    def _minimum(self, x: RBNode) -> RBNode:
        """Find the node with minimum key in subtree rooted at x"""
        while x.left != self.NIL:
            x = x.left
        return x

    def _maximum(self, x: RBNode) -> RBNode:
        """Find the node with maximum key in subtree rooted at x"""
        while x.right != self.NIL:
            x = x.right
        return x

    def predecessor(self, key: int) -> Optional[int]:
        """Find the predecessor of a given key"""
        node = self._find_node(key)
        if node == self.NIL:
            return None

        if node.left != self.NIL:
            return self._maximum(node.left).key

        y = node.parent
        while y != self.NIL and node == y.left:
            node = y
            y = y.parent

        return y.key if y != self.NIL else None

    def successor(self, key: int) -> Optional[int]:
        """Find the successor of a given key"""
        node = self._find_node(key)
        if node == self.NIL:
            return None

        if node.right != self.NIL:
            return self._minimum(node.right).key

        y = node.parent
        while y != self.NIL and node == y.right:
            node = y
            y = y.parent

        return y.key if y != self.NIL else None

    def inorder_traversal(self) -> List[int]:
        """Return keys in sorted order"""
        result = []
        self._inorder_helper(self.root, result)
        return result

    def _inorder_helper(self, node: RBNode, result: List[int]) -> None:
        """Helper for inorder traversal"""
        if node != self.NIL:
            self._inorder_helper(node.left, result)
            result.append(node.key)
            self._inorder_helper(node.right, result)

    def preorder_traversal(self) -> List[int]:
        """Return keys in preorder"""
        result = []
        self._preorder_helper(self.root, result)
        return result

    def _preorder_helper(self, node: RBNode, result: List[int]) -> None:
        """Helper for preorder traversal"""
        if node != self.NIL:
            result.append(node.key)
            self._preorder_helper(node.left, result)
            self._preorder_helper(node.right, result)

    def postorder_traversal(self) -> List[int]:
        """Return keys in postorder"""
        result = []
        self._postorder_helper(self.root, result)
        return result

    def _postorder_helper(self, node: RBNode, result: List[int]) -> None:
        """Helper for postorder traversal"""
        if node != self.NIL:
            self._postorder_helper(node.left, result)
            self._postorder_helper(node.right, result)
            result.append(node.key)

    def level_order_traversal(self) -> List[List[int]]:
        """Return keys level by level"""
        if self.root == self.NIL:
            return []

        result = []
        queue = [self.root]

        while queue:
            level_size = len(queue)
            level = []

            for _ in range(level_size):
                node = queue.pop(0)
                level.append(node.key)

                if node.left != self.NIL:
                    queue.append(node.left)
                if node.right != self.NIL:
                    queue.append(node.right)

            result.append(level)

        return result

    def get_height(self) -> int:
        """Get the height of the tree"""
        return self._get_height_helper(self.root)

    def _get_height_helper(self, node: RBNode) -> int:
        """Helper to calculate height"""
        if node == self.NIL:
            return -1
        return 1 + max(self._get_height_helper(node.left),
                      self._get_height_helper(node.right))

    def get_black_height(self) -> int:
        """Get the black height of the tree (black nodes on any path to leaf)"""
        return self._get_black_height_helper(self.root)

    def _get_black_height_helper(self, node: RBNode) -> int:
        """Helper to calculate black height"""
        if node == self.NIL:
            return 0

        left_height = self._get_black_height_helper(node.left)
        increment = 1 if node.color == Color.BLACK else 0

        return left_height + increment

    def verify_properties(self) -> bool:
        """
        Verify that all Red-Black tree properties are satisfied.

        Returns:
            True if all properties are satisfied, False otherwise
        """
        try:
            # Property 1: Root is black
            if self.root != self.NIL and self.root.color != Color.BLACK:
                return False

            # Properties 2-5: Check recursively
            self._verify_properties_helper(self.root)
            return True
        except:
            return False

    def _verify_properties_helper(self, node: RBNode) -> int:
        """
        Helper to verify properties recursively.

        Returns:
            The black height of the subtree

        Raises:
            Exception if any property is violated
        """
        if node == self.NIL:
            return 0

        # Property 4: Red node cannot have red children
        if node.color == Color.RED:
            if (node.left != self.NIL and node.left.color == Color.RED) or \
               (node.right != self.NIL and node.right.color == Color.RED):
                raise Exception("Red node has red child")

        # Property 5: All paths have same black height
        left_height = self._verify_properties_helper(node.left)
        right_height = self._verify_properties_helper(node.right)

        if left_height != right_height:
            raise Exception("Black heights don't match")

        increment = 1 if node.color == Color.BLACK else 0
        return left_height + increment

    def visualize(self, node: Optional[RBNode] = None, prefix: str = "", is_tail: bool = True) -> str:
        """
        Generate a visual representation of the tree structure.

        Args:
            node: Starting node (default: root)
            prefix: Prefix for the current line
            is_tail: Whether this is the last child

        Returns:
            String representation of the tree
        """
        if node is None:
            node = self.root

        if node == self.NIL:
            return ""

        result = []
        color_char = "R" if node.color == Color.RED else "B"
        result.append(f"{prefix}{'└── ' if is_tail else '├── '}{node.key}({color_char})\n")

        children = []
        if node.left != self.NIL:
            children.append((node.left, False))
        if node.right != self.NIL:
            children.append((node.right, True))

        for i, (child, is_last) in enumerate(children):
            is_last_child = (i == len(children) - 1)
            extension = "    " if is_tail else "│   "
            result.append(self.visualize(child, prefix + extension, is_last_child))

        return "".join(result)

    def clear(self) -> None:
        """Clear all nodes from the tree"""
        self.root = self.NIL
        self._size = 0

    def __len__(self) -> int:
        """Return the size of the tree"""
        return self._size

    def __contains__(self, key: int) -> bool:
        """Check if a key is in the tree"""
        return self.contains(key)

    def __str__(self) -> str:
        """String representation of the tree"""
        if self.is_empty():
            return "RBTree(empty)"
        return f"RBTree(size={self._size}, root={self.root.key}, height={self.get_height()})"

    def __repr__(self) -> str:
        """Detailed string representation"""
        return self.__str__()


# Example usage and testing
if __name__ == "__main__":
    # Create a Red-Black Tree
    rbt = RBTree()

    # Test insertions
    test_values = [7, 3, 18, 10, 22, 8, 11, 26, 2, 6, 13]
    print("Inserting values:", test_values)
    for val in test_values:
        rbt.insert(val)

    # Display tree structure
    print("\nTree structure:")
    print(rbt.visualize())

    # Test properties
    print(f"Tree properties valid: {rbt.verify_properties()}")
    print(f"Size: {rbt.size}")
    print(f"Height: {rbt.get_height()}")
    print(f"Black height: {rbt.get_black_height()}")

    # Test search
    print(f"\nSearch for 10: {rbt.search(10) is not None}")
    print(f"Search for 15: {rbt.search(15) is not None}")

    # Test traversals
    print(f"\nInorder traversal: {rbt.inorder_traversal()}")
    print(f"Level order: {rbt.level_order_traversal()}")

    # Test deletion
    print("\nDeleting 18...")
    rbt.delete(18)
    print("Tree after deletion:")
    print(rbt.visualize())
    print(f"Properties still valid: {rbt.verify_properties()}")

    # Test min/max
    print(f"\nMin: {rbt.get_min()}")
    print(f"Max: {rbt.get_max()}")

    # Test predecessor/successor
    print(f"Predecessor of 10: {rbt.predecessor(10)}")
    print(f"Successor of 10: {rbt.successor(10)}")