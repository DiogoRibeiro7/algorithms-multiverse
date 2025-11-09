"""
Binary Tree Implementation in Python

Time Complexity:
- Insert: O(log n) average, O(n) worst case
- Search: O(log n) average, O(n) worst case
- Delete: O(log n) average, O(n) worst case

Space Complexity: O(n) for storage, O(log n) for recursion stack

Python features:
- Object-oriented design
- Generator expressions
- Magic methods
- Type hints
"""

from typing import Optional, List, Iterator, Any
from collections import deque
import json


class TreeNode:
    """A single node in the binary tree."""

    def __init__(self, data: Any) -> None:
        self.data = data
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return f"TreeNode({self.data})"


class BinaryTree:
    """
    Binary Tree implementation with various traversal and utility methods.
    """

    def __init__(self) -> None:
        self.root: Optional[TreeNode] = None
        self.size = 0

    def insert(self, data: Any) -> None:
        """Insert a new node into the tree."""
        if self.root is None:
            self.root = TreeNode(data)
        else:
            self._insert_recursive(self.root, data)
        self.size += 1

    def _insert_recursive(self, node: TreeNode, data: Any) -> None:
        """Helper method for recursive insertion."""
        if data < node.data:
            if node.left is None:
                node.left = TreeNode(data)
            else:
                self._insert_recursive(node.left, data)
        else:
            if node.right is None:
                node.right = TreeNode(data)
            else:
                self._insert_recursive(node.right, data)

    def search(self, data: Any) -> bool:
        """Search for a value in the tree."""
        return self._search_recursive(self.root, data)

    def _search_recursive(self, node: Optional[TreeNode], data: Any) -> bool:
        """Helper method for recursive search."""
        if node is None:
            return False

        if data == node.data:
            return True
        elif data < node.data:
            return self._search_recursive(node.left, data)
        else:
            return self._search_recursive(node.right, data)

    def delete(self, data: Any) -> bool:
        """Delete a node from the tree."""
        if self.root is None:
            return False

        self.root, deleted = self._delete_recursive(self.root, data)
        if deleted:
            self.size -= 1
        return deleted

    def _delete_recursive(
        self, node: Optional[TreeNode], data: Any
    ) -> tuple[Optional[TreeNode], bool]:
        """Helper method for recursive deletion."""
        if node is None:
            return None, False

        if data < node.data:
            node.left, deleted = self._delete_recursive(node.left, data)
            return node, deleted
        elif data > node.data:
            node.right, deleted = self._delete_recursive(node.right, data)
            return node, deleted
        else:
            # Node to delete found
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            else:
                # Node has two children
                min_node = self._find_min(node.right)
                node.data = min_node.data
                node.right, _ = self._delete_recursive(node.right, min_node.data)
                return node, True

    def _find_min(self, node: TreeNode) -> TreeNode:
        """Find the minimum value node in a subtree."""
        while node.left is not None:
            node = node.left
        return node

    def _find_max(self, node: TreeNode) -> TreeNode:
        """Find the maximum value node in a subtree."""
        while node.right is not None:
            node = node.right
        return node

    # Traversal Methods

    def inorder_traversal(self) -> Iterator[Any]:
        """In-order traversal (left, root, right)."""
        yield from self._inorder_recursive(self.root)

    def _inorder_recursive(self, node: Optional[TreeNode]) -> Iterator[Any]:
        """Helper for in-order traversal."""
        if node is not None:
            yield from self._inorder_recursive(node.left)
            yield node.data
            yield from self._inorder_recursive(node.right)

    def preorder_traversal(self) -> Iterator[Any]:
        """Pre-order traversal (root, left, right)."""
        yield from self._preorder_recursive(self.root)

    def _preorder_recursive(self, node: Optional[TreeNode]) -> Iterator[Any]:
        """Helper for pre-order traversal."""
        if node is not None:
            yield node.data
            yield from self._preorder_recursive(node.left)
            yield from self._preorder_recursive(node.right)

    def postorder_traversal(self) -> Iterator[Any]:
        """Post-order traversal (left, right, root)."""
        yield from self._postorder_recursive(self.root)

    def _postorder_recursive(self, node: Optional[TreeNode]) -> Iterator[Any]:
        """Helper for post-order traversal."""
        if node is not None:
            yield from self._postorder_recursive(node.left)
            yield from self._postorder_recursive(node.right)
            yield node.data

    def level_order_traversal(self) -> Iterator[Any]:
        """Level-order (breadth-first) traversal."""
        if self.root is None:
            return

        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            yield node.data

            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

    # Utility Methods

    def height(self) -> int:
        """Calculate the height of the tree."""
        return self._height_recursive(self.root)

    def _height_recursive(self, node: Optional[TreeNode]) -> int:
        """Helper for calculating height."""
        if node is None:
            return -1

        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)

        return 1 + max(left_height, right_height)

    def depth(self, data: Any) -> int:
        """Calculate the depth of a specific node."""
        return self._depth_recursive(self.root, data, 0)

    def _depth_recursive(
        self, node: Optional[TreeNode], data: Any, current_depth: int
    ) -> int:
        """Helper for calculating depth."""
        if node is None:
            return -1

        if node.data == data:
            return current_depth

        if data < node.data:
            return self._depth_recursive(node.left, data, current_depth + 1)
        else:
            return self._depth_recursive(node.right, data, current_depth + 1)

    def is_balanced(self) -> bool:
        """Check if the tree is height-balanced."""
        return self._is_balanced_recursive(self.root)[0]

    def _is_balanced_recursive(self, node: Optional[TreeNode]) -> tuple[bool, int]:
        """Helper for checking if tree is balanced."""
        if node is None:
            return True, -1

        left_balanced, left_height = self._is_balanced_recursive(node.left)
        right_balanced, right_height = self._is_balanced_recursive(node.right)

        balanced = (
            left_balanced and right_balanced and abs(left_height - right_height) <= 1
        )
        height = 1 + max(left_height, right_height)

        return balanced, height

    def count_nodes(self) -> int:
        """Count the total number of nodes."""
        return self.size

    def count_leaves(self) -> int:
        """Count the number of leaf nodes."""
        return self._count_leaves_recursive(self.root)

    def _count_leaves_recursive(self, node: Optional[TreeNode]) -> int:
        """Helper for counting leaf nodes."""
        if node is None:
            return 0

        if node.left is None and node.right is None:
            return 1

        return self._count_leaves_recursive(node.left) + self._count_leaves_recursive(
            node.right
        )

    def get_level_nodes(self, level: int) -> List[Any]:
        """Get all nodes at a specific level."""
        result = []
        self._get_level_nodes_recursive(self.root, level, 0, result)
        return result

    def _get_level_nodes_recursive(
        self,
        node: Optional[TreeNode],
        target_level: int,
        current_level: int,
        result: List[Any],
    ) -> None:
        """Helper for getting nodes at a specific level."""
        if node is None:
            return

        if current_level == target_level:
            result.append(node.data)
        else:
            self._get_level_nodes_recursive(
                node.left, target_level, current_level + 1, result
            )
            self._get_level_nodes_recursive(
                node.right, target_level, current_level + 1, result
            )

    def to_list(self) -> List[Any]:
        """Convert tree to sorted list (in-order traversal)."""
        return list(self.inorder_traversal())

    def to_json(self) -> str:
        """Convert tree to JSON representation."""
        return json.dumps(self._to_dict(self.root), indent=2)

    def _to_dict(self, node: Optional[TreeNode]) -> Optional[dict]:
        """Helper for JSON conversion."""
        if node is None:
            return None

        return {
            "data": node.data,
            "left": self._to_dict(node.left),
            "right": self._to_dict(node.right),
        }

    def pretty_print(self) -> None:
        """Print the tree in a visual format."""
        if self.root is None:
            print("Empty tree")
            return

        self._pretty_print_recursive(self.root, "", True)

    def _pretty_print_recursive(
        self, node: Optional[TreeNode], prefix: str, is_last: bool
    ) -> None:
        """Helper for pretty printing."""
        if node is not None:
            print(prefix + ("└── " if is_last else "├── ") + str(node.data))

            children = []
            if node.left is not None:
                children.append(node.left)
            if node.right is not None:
                children.append(node.right)

            for i, child in enumerate(children):
                is_last_child = i == len(children) - 1
                extension = "    " if is_last else "│   "
                self._pretty_print_recursive(child, prefix + extension, is_last_child)

    # Magic Methods

    def __len__(self) -> int:
        return self.size

    def __contains__(self, data: Any) -> bool:
        return self.search(data)

    def __bool__(self) -> bool:
        return self.root is not None

    def __iter__(self) -> Iterator[Any]:
        return self.inorder_traversal()

    def __str__(self) -> str:
        return str(list(self.inorder_traversal()))

    def __repr__(self) -> str:
        return f"BinaryTree({list(self.inorder_traversal())})"


def demonstrate_binary_tree():
    """Demonstrate various binary tree operations."""
    print("🌳 Binary Tree Implementation in Python")
    print("=" * 45)

    # Create and populate tree
    tree = BinaryTree()
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]

    print("\n📥 Inserting values:", values)
    for value in values:
        tree.insert(value)

    print(f"Tree size: {len(tree)}")
    print(f"Tree height: {tree.height()}")
    print(f"Is balanced: {tree.is_balanced()}")

    # Visual representation
    print("\n🎨 Tree Structure:")
    tree.pretty_print()

    # Traversals
    print("\n🚶 Tree Traversals:")
    print(f"In-order:    {list(tree.inorder_traversal())}")
    print(f"Pre-order:   {list(tree.preorder_traversal())}")
    print(f"Post-order:  {list(tree.postorder_traversal())}")
    print(f"Level-order: {list(tree.level_order_traversal())}")

    # Search operations
    print("\n🔍 Search Operations:")
    search_values = [25, 75, 50, 100]
    for value in search_values:
        found = value in tree
        depth = tree.depth(value) if found else -1
        print(f"Search {value}: {'Found' if found else 'Not found'} (depth: {depth})")

    # Level operations
    print("\n📏 Level Operations:")
    for level in range(tree.height() + 1):
        nodes = tree.get_level_nodes(level)
        print(f"Level {level}: {nodes}")

    # Statistics
    print(f"\n📊 Tree Statistics:")
    print(f"Total nodes: {tree.count_nodes()}")
    print(f"Leaf nodes: {tree.count_leaves()}")
    print(f"Height: {tree.height()}")

    # Deletion
    print(f"\n🗑️ Deletion Operations:")
    delete_values = [10, 30, 50]
    for value in delete_values:
        print(f"Deleting {value}...")
        deleted = tree.delete(value)
        print(f"Success: {deleted}, New tree: {tree}")
        if deleted:
            print("Updated tree structure:")
            tree.pretty_print()

    # JSON representation
    print(f"\n📄 JSON Representation:")
    print(tree.to_json())


def performance_test():
    """Test performance with larger datasets."""
    import random
    import time

    print("\n⚡ Performance Testing")
    print("=" * 25)

    sizes = [1000, 5000, 10000]

    for size in sizes:
        print(f"\nTesting with {size} elements:")

        # Generate random data
        data = list(range(size))
        random.shuffle(data)

        tree = BinaryTree()

        # Test insertion
        start_time = time.time()
        for value in data:
            tree.insert(value)
        insertion_time = time.time() - start_time

        # Test search
        search_data = random.sample(data, min(100, len(data)))
        start_time = time.time()
        for value in search_data:
            tree.search(value)
        search_time = time.time() - start_time

        # Test traversal
        start_time = time.time()
        list(tree.inorder_traversal())
        traversal_time = time.time() - start_time

        print(f"  Insertion:  {insertion_time:.4f}s")
        print(f"  Search:     {search_time:.4f}s")
        print(f"  Traversal:  {traversal_time:.4f}s")
        print(f"  Height:     {tree.height()}")
        print(f"  Balanced:   {tree.is_balanced()}")


if __name__ == "__main__":
    demonstrate_binary_tree()
    performance_test()

    print("\n✨ Binary Tree demonstration complete!")
