"""
Comprehensive Linked List Implementations in Python

This module implements four linked list variants:
1. Singly Linked List
2. Doubly Linked List
3. Circular Linked List
4. Skip List (Probabilistic Data Structure)

Features:
- Basic operations: insert, delete, search, traverse
- Advanced operations: reverse, merge, split, cycle detection
- Iterator/generator support
- Memory efficient implementations
- Performance comparisons with arrays

Time Complexity Comparison:
                    Array   Linked List
Access by index:    O(1)    O(n)
Insert at head:     O(n)    O(1)
Insert at tail:     O(1)*   O(n) or O(1) with tail pointer
Insert at middle:   O(n)    O(n)
Delete at head:     O(n)    O(1)
Delete at tail:     O(1)*   O(n) or O(1) for doubly linked
Search:             O(n)    O(n)
* with dynamic arrays

Use Cases for Linked Lists:
- Frequent insertions/deletions at beginning
- Unknown or dynamic size
- Implementation of stacks, queues, graphs
- LRU caches
- Undo functionality
- Music playlists
- Browser history (doubly linked)

Cache Performance:
- Arrays have better cache locality (contiguous memory)
- Linked lists have poor spatial locality (scattered nodes)
- Arrays preferred for read-heavy workloads
- Linked lists preferred for write-heavy workloads at ends
"""

from typing import Generic, TypeVar, Optional, Iterator, List, Callable
import random

T = TypeVar('T')

# ============================================================================
# SINGLY LINKED LIST
# ============================================================================

class SinglyNode(Generic[T]):
    """Node for singly linked list."""

    def __init__(self, data: T):
        self.data = data
        self.next: Optional['SinglyNode[T]'] = None


class SinglyLinkedList(Generic[T]):
    """
    Singly Linked List - each node points to next node only.

    Advantages:
    - Simple implementation
    - Less memory per node (one pointer)
    - O(1) insertion at head

    Disadvantages:
    - Can only traverse forward
    - O(n) to find previous node
    - O(n) deletion at tail
    """

    def __init__(self):
        self.head: Optional[SinglyNode[T]] = None
        self.size = 0

    def insert_at_head(self, data: T) -> None:
        """Insert at beginning. O(1)"""
        new_node = SinglyNode(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def insert_at_tail(self, data: T) -> None:
        """Insert at end. O(n)"""
        new_node = SinglyNode(data)

        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

        self.size += 1

    def insert_at_position(self, data: T, position: int) -> None:
        """Insert at specific position. O(n)"""
        if position < 0 or position > self.size:
            raise IndexError("Position out of bounds")

        if position == 0:
            self.insert_at_head(data)
            return

        new_node = SinglyNode(data)
        current = self.head

        for _ in range(position - 1):
            current = current.next

        new_node.next = current.next
        current.next = new_node
        self.size += 1

    def delete_at_head(self) -> Optional[T]:
        """Delete from beginning. O(1)"""
        if not self.head:
            return None

        data = self.head.data
        self.head = self.head.next
        self.size -= 1
        return data

    def delete_at_tail(self) -> Optional[T]:
        """Delete from end. O(n)"""
        if not self.head:
            return None

        if not self.head.next:
            data = self.head.data
            self.head = None
            self.size -= 1
            return data

        current = self.head
        while current.next.next:
            current = current.next

        data = current.next.data
        current.next = None
        self.size -= 1
        return data

    def delete_value(self, value: T) -> bool:
        """Delete first occurrence of value. O(n)"""
        if not self.head:
            return False

        if self.head.data == value:
            self.head = self.head.next
            self.size -= 1
            return True

        current = self.head
        while current.next:
            if current.next.data == value:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next

        return False

    def search(self, value: T) -> Optional[SinglyNode[T]]:
        """Search for value. O(n)"""
        current = self.head
        while current:
            if current.data == value:
                return current
            current = current.next
        return None

    def reverse(self) -> None:
        """Reverse the list in-place. O(n)"""
        prev = None
        current = self.head

        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        self.head = prev

    def get_middle(self) -> Optional[T]:
        """Get middle element using slow/fast pointers. O(n)"""
        if not self.head:
            return None

        slow = fast = self.head

        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        return slow.data

    def detect_cycle(self) -> bool:
        """Detect cycle using Floyd's algorithm. O(n)"""
        if not self.head:
            return False

        slow = fast = self.head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True

        return False

    def merge_sorted(self, other: 'SinglyLinkedList[T]') -> 'SinglyLinkedList[T]':
        """Merge two sorted lists. O(n + m)"""
        result = SinglyLinkedList[T]()

        current1 = self.head
        current2 = other.head

        # Find the head of merged list
        if not current1:
            result.head = current2
            result.size = other.size
            return result
        if not current2:
            result.head = current1
            result.size = self.size
            return result

        if current1.data <= current2.data:
            result.head = current1
            current1 = current1.next
        else:
            result.head = current2
            current2 = current2.next

        current = result.head

        while current1 and current2:
            if current1.data <= current2.data:
                current.next = current1
                current1 = current1.next
            else:
                current.next = current2
                current2 = current2.next
            current = current.next

        current.next = current1 if current1 else current2
        result.size = self.size + other.size

        return result

    def __iter__(self) -> Iterator[T]:
        """Iterator support."""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        return ' -> '.join(str(data) for data in self) + ' -> None'


# ============================================================================
# DOUBLY LINKED LIST
# ============================================================================

class DoublyNode(Generic[T]):
    """Node for doubly linked list."""

    def __init__(self, data: T):
        self.data = data
        self.next: Optional['DoublyNode[T]'] = None
        self.prev: Optional['DoublyNode[T]'] = None


class DoublyLinkedList(Generic[T]):
    """
    Doubly Linked List - each node points to both next and previous.

    Advantages:
    - Bidirectional traversal
    - O(1) deletion at tail (with tail pointer)
    - Easier deletion of specific node
    - Better for implementing deque

    Disadvantages:
    - More memory per node (two pointers)
    - Slightly more complex operations
    """

    def __init__(self):
        self.head: Optional[DoublyNode[T]] = None
        self.tail: Optional[DoublyNode[T]] = None
        self.size = 0

    def insert_at_head(self, data: T) -> None:
        """Insert at beginning. O(1)"""
        new_node = DoublyNode(data)

        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.size += 1

    def insert_at_tail(self, data: T) -> None:
        """Insert at end. O(1)"""
        new_node = DoublyNode(data)

        if not self.tail:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def delete_at_head(self) -> Optional[T]:
        """Delete from beginning. O(1)"""
        if not self.head:
            return None

        data = self.head.data

        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None

        self.size -= 1
        return data

    def delete_at_tail(self) -> Optional[T]:
        """Delete from end. O(1)"""
        if not self.tail:
            return None

        data = self.tail.data

        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None

        self.size -= 1
        return data

    def delete_node(self, node: DoublyNode[T]) -> None:
        """Delete specific node. O(1) with node reference"""
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        self.size -= 1

    def reverse(self) -> None:
        """Reverse the list in-place. O(n)"""
        current = self.head
        self.head, self.tail = self.tail, self.head

        while current:
            current.prev, current.next = current.next, current.prev
            current = current.prev  # Move to next (which is now prev)

    def __iter__(self) -> Iterator[T]:
        """Forward iterator."""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def reverse_iter(self) -> Iterator[T]:
        """Backward iterator."""
        current = self.tail
        while current:
            yield current.data
            current = current.prev

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        return ' <-> '.join(str(data) for data in self) + ' <-> None'


# ============================================================================
# CIRCULAR LINKED LIST
# ============================================================================

class CircularLinkedList(Generic[T]):
    """
    Circular Linked List - last node points back to first.

    Advantages:
    - Can traverse entire list from any node
    - Useful for round-robin scheduling
    - No null pointers
    - Natural for cyclic data

    Disadvantages:
    - Need special care to avoid infinite loops
    - Slightly more complex operations

    Use Cases:
    - Round-robin CPU scheduling
    - Multiplayer game turns
    - Music playlist on repeat
    - Circular buffers
    """

    def __init__(self):
        self.head: Optional[SinglyNode[T]] = None
        self.size = 0

    def insert_at_head(self, data: T) -> None:
        """Insert at beginning. O(n) to find last node"""
        new_node = SinglyNode(data)

        if not self.head:
            new_node.next = new_node  # Points to itself
            self.head = new_node
        else:
            # Find last node
            current = self.head
            while current.next != self.head:
                current = current.next

            new_node.next = self.head
            current.next = new_node
            self.head = new_node

        self.size += 1

    def insert_at_tail(self, data: T) -> None:
        """Insert at end. O(n)"""
        new_node = SinglyNode(data)

        if not self.head:
            new_node.next = new_node
            self.head = new_node
        else:
            current = self.head
            while current.next != self.head:
                current = current.next

            current.next = new_node
            new_node.next = self.head

        self.size += 1

    def delete_at_head(self) -> Optional[T]:
        """Delete from beginning. O(n)"""
        if not self.head:
            return None

        data = self.head.data

        if self.head.next == self.head:
            self.head = None
        else:
            # Find last node
            current = self.head
            while current.next != self.head:
                current = current.next

            current.next = self.head.next
            self.head = self.head.next

        self.size -= 1
        return data

    def traverse(self, callback: Callable[[T], None]) -> None:
        """Traverse and apply callback. O(n)"""
        if not self.head:
            return

        current = self.head
        while True:
            callback(current.data)
            current = current.next
            if current == self.head:
                break

    def __iter__(self) -> Iterator[T]:
        """Iterator support."""
        if not self.head:
            return

        current = self.head
        while True:
            yield current.data
            current = current.next
            if current == self.head:
                break

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        if not self.head:
            return "Empty"
        return ' -> '.join(str(data) for data in self) + ' -> (head)'


# ============================================================================
# SKIP LIST
# ============================================================================

class SkipNode(Generic[T]):
    """Node for skip list with multiple forward pointers."""

    def __init__(self, data: T, level: int):
        self.data = data
        self.forward: List[Optional['SkipNode[T]']] = [None] * (level + 1)


class SkipList(Generic[T]):
    """
    Skip List - probabilistic data structure for fast search.

    Complexity:
    - Search: O(log n) average
    - Insert: O(log n) average
    - Delete: O(log n) average
    - Space: O(n log n) expected

    Advantages:
    - Faster than regular linked list for search
    - Simpler than balanced trees
    - Probabilistic balancing (no rotations)
    - Good for concurrent access

    Disadvantages:
    - More memory overhead
    - Probabilistic (worst case still O(n))
    - Cache performance worse than B-trees

    Use Cases:
    - In-memory databases (Redis uses skip lists)
    - Concurrent data structures
    - Alternative to balanced trees
    - Level-based indexing
    """

    MAX_LEVEL = 16
    P = 0.5  # Probability factor

    def __init__(self):
        self.level = 0
        self.header = SkipNode(None, self.MAX_LEVEL)
        self.size = 0

    def _random_level(self) -> int:
        """Generate random level using probability P."""
        level = 0
        while random.random() < self.P and level < self.MAX_LEVEL:
            level += 1
        return level

    def insert(self, data: T) -> None:
        """Insert element. O(log n) average"""
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.header

        # Find position to insert
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].data < data:
                current = current.forward[i]
            update[i] = current

        # Generate random level
        new_level = self._random_level()

        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level

        # Create new node
        new_node = SkipNode(data, new_level)

        # Update forward pointers
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

        self.size += 1

    def search(self, data: T) -> bool:
        """Search for element. O(log n) average"""
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].data < data:
                current = current.forward[i]

        current = current.forward[0]
        return current is not None and current.data == data

    def delete(self, data: T) -> bool:
        """Delete element. O(log n) average"""
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.header

        # Find node to delete
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].data < data:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current is None or current.data != data:
            return False

        # Remove node
        for i in range(self.level + 1):
            if update[i].forward[i] != current:
                break
            update[i].forward[i] = current.forward[i]

        # Update level
        while self.level > 0 and self.header.forward[self.level] is None:
            self.level -= 1

        self.size -= 1
        return True

    def __iter__(self) -> Iterator[T]:
        """Iterator at lowest level."""
        current = self.header.forward[0]
        while current:
            yield current.data
            current = current.forward[0]

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        return f"SkipList({list(self)})"


# ============================================================================
# DEMONSTRATION AND BENCHMARKING
# ============================================================================

def demonstrate_linked_lists():
    """Demonstrate all linked list variants."""

    print("=" * 80)
    print("COMPREHENSIVE LINKED LIST DEMONSTRATIONS")
    print("=" * 80)

    # Singly Linked List
    print("\n1. SINGLY LINKED LIST")
    print("-" * 80)
    sll = SinglyLinkedList[int]()

    print("Inserting: 1, 2, 3 at head")
    sll.insert_at_head(3)
    sll.insert_at_head(2)
    sll.insert_at_head(1)
    print(f"List: {sll}")

    print("\nInserting: 4, 5 at tail")
    sll.insert_at_tail(4)
    sll.insert_at_tail(5)
    print(f"List: {sll}")

    print(f"\nMiddle element: {sll.get_middle()}")

    print("\nReversing list...")
    sll.reverse()
    print(f"List: {sll}")

    # Doubly Linked List
    print("\n2. DOUBLY LINKED LIST")
    print("-" * 80)
    dll = DoublyLinkedList[str]()

    print("Inserting: A, B, C at head")
    dll.insert_at_head("C")
    dll.insert_at_head("B")
    dll.insert_at_head("A")
    print(f"List: {dll}")

    print("\nInserting: D, E at tail")
    dll.insert_at_tail("D")
    dll.insert_at_tail("E")
    print(f"List: {dll}")

    print("\nForward iteration:", list(dll))
    print("Backward iteration:", list(dll.reverse_iter()))

    print("\nDeleting head and tail...")
    dll.delete_at_head()
    dll.delete_at_tail()
    print(f"List: {dll}")

    # Circular Linked List
    print("\n3. CIRCULAR LINKED LIST")
    print("-" * 80)
    cll = CircularLinkedList[int]()

    print("Inserting: 1, 2, 3, 4, 5")
    for i in range(1, 6):
        cll.insert_at_tail(i)
    print(f"List: {cll}")

    print("\nTraversing (will loop back):")
    count = 0
    for item in cll:
        print(f"  {item}", end=" ")
        count += 1
        if count >= 8:  # Show it loops
            print("...")
            break
    print()

    # Skip List
    print("\n4. SKIP LIST")
    print("-" * 80)
    sl = SkipList[int]()

    print("Inserting: 3, 7, 1, 9, 5, 2, 8, 4, 6")
    for val in [3, 7, 1, 9, 5, 2, 8, 4, 6]:
        sl.insert(val)

    print(f"Skip list (sorted): {list(sl)}")

    print("\nSearching for 5:", sl.search(5))
    print("Searching for 10:", sl.search(10))

    print("\nDeleting 5...")
    sl.delete(5)
    print(f"Skip list: {list(sl)}")

    # Performance comparison
    print("\n5. PERFORMANCE COMPARISON: LINKED LIST VS ARRAY")
    print("-" * 80)
    print("""
    Operation           Array       Singly LL   Doubly LL   Skip List
    ----------------------------------------------------------------
    Access by index     O(1)        O(n)        O(n)        O(log n)
    Insert at head      O(n)        O(1)        O(1)        O(log n)
    Insert at tail      O(1)*       O(n)        O(1)        O(log n)
    Delete at head      O(n)        O(1)        O(1)        O(log n)
    Delete at tail      O(1)*       O(n)        O(1)        O(log n)
    Search              O(n)        O(n)        O(n)        O(log n)
    Memory overhead     Low         Medium      High        Very High
    Cache locality      Excellent   Poor        Poor        Poor

    * Amortized for dynamic arrays

    WHEN TO USE LINKED LISTS:
    ✓ Frequent insertions/deletions at beginning or end
    ✓ Size unknown or highly variable
    ✓ Don't need random access
    ✓ Implementing stacks, queues, or graphs
    ✓ Memory fragmentation acceptable

    WHEN TO USE ARRAYS:
    ✓ Random access needed
    ✓ Read-heavy workloads
    ✓ Size known or slowly growing
    ✓ Cache performance critical
    ✓ Memory locality important
    """)

    print("\n6. USE CASE EXAMPLES")
    print("-" * 80)
    print("""
    Singly Linked List:
    - Stack implementation
    - Simple queues
    - Hash table chaining
    - Undo functionality

    Doubly Linked List:
    - Browser history (back/forward)
    - LRU cache
    - Deque implementation
    - Music player (prev/next)
    - Text editor (cursor movement)

    Circular Linked List:
    - Round-robin scheduling
    - Multiplayer games (turn order)
    - Circular buffers
    - Music playlist on repeat

    Skip List:
    - In-memory databases (Redis)
    - Concurrent data structures
    - Sorted collections
    - Alternative to balanced trees
    """)

    print("=" * 80)
    print("✨ All demonstrations complete!")
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_linked_lists()
