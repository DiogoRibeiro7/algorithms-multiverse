"""
Heap Sort Algorithm Implementation in Python

Time Complexity: O(n log n) - consistently across all cases
Space Complexity: O(1) for in-place sorting, O(n) for auxiliary heap

Heap Sort is a comparison-based sorting algorithm that uses a binary heap data
structure. It divides its input into a sorted and an unsorted region, and it
iteratively shrinks the unsorted region by extracting the largest element and
inserting it into the sorted region.

Python features:
- Type hints for clarity
- Object-oriented heap data structure
- Priority queue implementation
- Visual heap representation
- Comprehensive testing
"""

from typing import List, TypeVar, Callable, Optional, Generic, Any
import time
import random
from copy import deepcopy
import math

T = TypeVar("T")


def heapify_max(arr: List[T], n: int, i: int) -> None:
    """
    Maintain the max-heap property for a subtree rooted at index i.

    Args:
        arr: The array representing the heap
        n: Size of the heap
        i: Index of the root of the subtree

    Time Complexity: O(log n)
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # Check if left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Check if right child exists and is greater than largest so far
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If largest is not root, swap and recursively heapify
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify_max(arr, n, largest)


def heapify_min(arr: List[T], n: int, i: int) -> None:
    """
    Maintain the min-heap property for a subtree rooted at index i.

    Args:
        arr: The array representing the heap
        n: Size of the heap
        i: Index of the root of the subtree

    Time Complexity: O(log n)
    """
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # Check if left child exists and is smaller than root
    if left < n and arr[left] < arr[smallest]:
        smallest = left

    # Check if right child exists and is smaller than smallest so far
    if right < n and arr[right] < arr[smallest]:
        smallest = right

    # If smallest is not root, swap and recursively heapify
    if smallest != i:
        arr[i], arr[smallest] = arr[smallest], arr[i]
        heapify_min(arr, n, smallest)


def build_max_heap(arr: List[T]) -> None:
    """
    Build a max-heap from an unordered array.

    Args:
        arr: Array to be converted into a max-heap

    Time Complexity: O(n)
    """
    n = len(arr)
    # Start from the last non-leaf node and heapify each node
    for i in range(n // 2 - 1, -1, -1):
        heapify_max(arr, n, i)


def build_min_heap(arr: List[T]) -> None:
    """
    Build a min-heap from an unordered array.

    Args:
        arr: Array to be converted into a min-heap

    Time Complexity: O(n)
    """
    n = len(arr)
    # Start from the last non-leaf node and heapify each node
    for i in range(n // 2 - 1, -1, -1):
        heapify_min(arr, n, i)


def heap_sort(arr: List[T]) -> List[T]:
    """
    Sort an array using heap sort algorithm.

    Args:
        arr: Array to be sorted

    Returns:
        New sorted array

    Time Complexity: O(n log n)
    Space Complexity: O(n) for the new array
    """
    if len(arr) <= 1:
        return arr.copy()

    result = arr.copy()
    heap_sort_in_place(result)
    return result


def heap_sort_in_place(arr: List[T]) -> None:
    """
    Sort an array in-place using heap sort algorithm.

    Args:
        arr: Array to be sorted in-place

    Time Complexity: O(n log n)
    Space Complexity: O(1)
    """
    n = len(arr)

    # Build a max heap
    build_max_heap(arr)

    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        # Move current root to end
        arr[0], arr[i] = arr[i], arr[0]
        # Call heapify on the reduced heap
        heapify_max(arr, i, 0)


def heap_sort_descending(arr: List[T]) -> List[T]:
    """
    Sort an array in descending order using heap sort.

    Args:
        arr: Array to be sorted

    Returns:
        New sorted array in descending order

    Time Complexity: O(n log n)
    """
    if len(arr) <= 1:
        return arr.copy()

    result = arr.copy()
    n = len(result)

    # Build a min heap for descending order
    build_min_heap(result)

    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        result[0], result[i] = result[i], result[0]
        heapify_min(result, i, 0)

    return result


class MaxHeap(Generic[T]):
    """
    Max-Heap data structure implementation.

    A max-heap is a complete binary tree where each node is greater than or
    equal to its children.
    """

    def __init__(self, initial_data: Optional[List[T]] = None):
        """Initialize the max-heap with optional initial data."""
        self.heap: List[T] = []
        if initial_data:
            self.heap = initial_data.copy()
            build_max_heap(self.heap)

    def parent(self, i: int) -> int:
        """Get the parent index of node i."""
        return (i - 1) // 2

    def left(self, i: int) -> int:
        """Get the left child index of node i."""
        return 2 * i + 1

    def right(self, i: int) -> int:
        """Get the right child index of node i."""
        return 2 * i + 2

    def insert(self, key: T) -> None:
        """
        Insert a new key into the heap.

        Time Complexity: O(log n)
        """
        # Add the new key at the end
        self.heap.append(key)
        # Fix the heap property if violated
        self._bubble_up(len(self.heap) - 1)

    def _bubble_up(self, i: int) -> None:
        """Move the element at index i up to maintain heap property."""
        while i > 0 and self.heap[self.parent(i)] < self.heap[i]:
            parent_idx = self.parent(i)
            self.heap[i], self.heap[parent_idx] = self.heap[parent_idx], self.heap[i]
            i = parent_idx

    def extract_max(self) -> T:
        """
        Remove and return the maximum element (root) from the heap.

        Returns:
            The maximum element

        Raises:
            IndexError: If heap is empty

        Time Complexity: O(log n)
        """
        if not self.heap:
            raise IndexError("extract_max from empty heap")

        if len(self.heap) == 1:
            return self.heap.pop()

        # Store the maximum value
        max_val = self.heap[0]
        # Move the last element to root
        self.heap[0] = self.heap.pop()
        # Heapify the root
        heapify_max(self.heap, len(self.heap), 0)

        return max_val

    def get_max(self) -> T:
        """
        Get the maximum element without removing it.

        Returns:
            The maximum element

        Raises:
            IndexError: If heap is empty
        """
        if not self.heap:
            raise IndexError("get_max from empty heap")
        return self.heap[0]

    def increase_key(self, i: int, new_key: T) -> None:
        """
        Increase the value of a key at index i.

        Args:
            i: Index of the key to increase
            new_key: New value (must be greater than current value)

        Raises:
            ValueError: If new_key is smaller than current key
            IndexError: If index is out of bounds

        Time Complexity: O(log n)
        """
        if i < 0 or i >= len(self.heap):
            raise IndexError(f"Index {i} out of bounds")

        if new_key < self.heap[i]:
            raise ValueError("New key is smaller than current key")

        self.heap[i] = new_key
        self._bubble_up(i)

    def decrease_key(self, i: int, new_key: T) -> None:
        """
        Decrease the value of a key at index i.

        Args:
            i: Index of the key to decrease
            new_key: New value (must be smaller than current value)

        Raises:
            ValueError: If new_key is greater than current key
            IndexError: If index is out of bounds

        Time Complexity: O(log n)
        """
        if i < 0 or i >= len(self.heap):
            raise IndexError(f"Index {i} out of bounds")

        if new_key > self.heap[i]:
            raise ValueError("New key is greater than current key")

        self.heap[i] = new_key
        heapify_max(self.heap, len(self.heap), i)

    def size(self) -> int:
        """Return the size of the heap."""
        return len(self.heap)

    def is_empty(self) -> bool:
        """Check if the heap is empty."""
        return len(self.heap) == 0

    def to_list(self) -> List[T]:
        """Return a copy of the heap as a list."""
        return self.heap.copy()

    def visualize(self) -> str:
        """
        Create ASCII art visualization of the heap.

        Returns:
            String representation of the heap tree
        """
        if not self.heap:
            return "Empty heap"

        lines = []
        self._visualize_helper(0, "", "", lines)
        return "\n".join(lines)

    def _visualize_helper(self, i: int, prefix: str, child_prefix: str, lines: List[str]) -> None:
        """Helper method for visualizing the heap."""
        if i >= len(self.heap):
            return

        lines.append(prefix + str(self.heap[i]))

        left_idx = self.left(i)
        right_idx = self.right(i)

        if left_idx < len(self.heap) or right_idx < len(self.heap):
            if left_idx < len(self.heap):
                if right_idx < len(self.heap):
                    self._visualize_helper(left_idx, child_prefix + "├── ", child_prefix + "│   ", lines)
                else:
                    self._visualize_helper(left_idx, child_prefix + "└── ", child_prefix + "    ", lines)

            if right_idx < len(self.heap):
                self._visualize_helper(right_idx, child_prefix + "└── ", child_prefix + "    ", lines)


class MinHeap(Generic[T]):
    """
    Min-Heap data structure implementation.

    A min-heap is a complete binary tree where each node is less than or
    equal to its children.
    """

    def __init__(self, initial_data: Optional[List[T]] = None):
        """Initialize the min-heap with optional initial data."""
        self.heap: List[T] = []
        if initial_data:
            self.heap = initial_data.copy()
            build_min_heap(self.heap)

    def parent(self, i: int) -> int:
        """Get the parent index of node i."""
        return (i - 1) // 2

    def left(self, i: int) -> int:
        """Get the left child index of node i."""
        return 2 * i + 1

    def right(self, i: int) -> int:
        """Get the right child index of node i."""
        return 2 * i + 2

    def insert(self, key: T) -> None:
        """
        Insert a new key into the heap.

        Time Complexity: O(log n)
        """
        self.heap.append(key)
        self._bubble_up(len(self.heap) - 1)

    def _bubble_up(self, i: int) -> None:
        """Move the element at index i up to maintain heap property."""
        while i > 0 and self.heap[self.parent(i)] > self.heap[i]:
            parent_idx = self.parent(i)
            self.heap[i], self.heap[parent_idx] = self.heap[parent_idx], self.heap[i]
            i = parent_idx

    def extract_min(self) -> T:
        """
        Remove and return the minimum element (root) from the heap.

        Returns:
            The minimum element

        Raises:
            IndexError: If heap is empty

        Time Complexity: O(log n)
        """
        if not self.heap:
            raise IndexError("extract_min from empty heap")

        if len(self.heap) == 1:
            return self.heap.pop()

        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        heapify_min(self.heap, len(self.heap), 0)

        return min_val

    def get_min(self) -> T:
        """
        Get the minimum element without removing it.

        Returns:
            The minimum element

        Raises:
            IndexError: If heap is empty
        """
        if not self.heap:
            raise IndexError("get_min from empty heap")
        return self.heap[0]

    def size(self) -> int:
        """Return the size of the heap."""
        return len(self.heap)

    def is_empty(self) -> bool:
        """Check if the heap is empty."""
        return len(self.heap) == 0

    def visualize(self) -> str:
        """
        Create ASCII art visualization of the heap.

        Returns:
            String representation of the heap tree
        """
        if not self.heap:
            return "Empty heap"

        lines = []
        self._visualize_helper(0, "", "", lines)
        return "\n".join(lines)

    def _visualize_helper(self, i: int, prefix: str, child_prefix: str, lines: List[str]) -> None:
        """Helper method for visualizing the heap."""
        if i >= len(self.heap):
            return

        lines.append(prefix + str(self.heap[i]))

        left_idx = self.left(i)
        right_idx = self.right(i)

        if left_idx < len(self.heap) or right_idx < len(self.heap):
            if left_idx < len(self.heap):
                if right_idx < len(self.heap):
                    self._visualize_helper(left_idx, child_prefix + "├── ", child_prefix + "│   ", lines)
                else:
                    self._visualize_helper(left_idx, child_prefix + "└── ", child_prefix + "    ", lines)

            if right_idx < len(self.heap):
                self._visualize_helper(right_idx, child_prefix + "└── ", child_prefix + "    ", lines)


class PriorityQueue(Generic[T]):
    """
    Priority Queue implementation using a max-heap.

    Higher priority values are served first.
    """

    def __init__(self):
        """Initialize an empty priority queue."""
        self.heap = MaxHeap[T]()

    def enqueue(self, item: T) -> None:
        """
        Add an item to the priority queue.

        Args:
            item: Item to add

        Time Complexity: O(log n)
        """
        self.heap.insert(item)

    def dequeue(self) -> T:
        """
        Remove and return the highest priority item.

        Returns:
            The highest priority item

        Raises:
            IndexError: If queue is empty

        Time Complexity: O(log n)
        """
        return self.heap.extract_max()

    def peek(self) -> T:
        """
        Get the highest priority item without removing it.

        Returns:
            The highest priority item

        Raises:
            IndexError: If queue is empty
        """
        return self.heap.get_max()

    def is_empty(self) -> bool:
        """Check if the priority queue is empty."""
        return self.heap.is_empty()

    def size(self) -> int:
        """Return the size of the priority queue."""
        return self.heap.size()


def is_sorted(arr: List[T]) -> bool:
    """Check if array is sorted in ascending order."""
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


def demonstrate_heap_sort():
    """Demonstrate heap sort and heap data structure."""
    print("🏔️  Heap Sort Implementation in Python")
    print("=" * 60)

    # Test data
    test_arrays = [
        ([64, 34, 25, 12, 22, 11, 90], "Random array"),
        ([5, 2, 8, 6, 1, 9, 4], "Small random array"),
        ([1], "Single element"),
        ([], "Empty array"),
        ([3, 3, 3, 3, 3], "All duplicates"),
        ([9, 8, 7, 6, 5, 4, 3, 2, 1], "Reverse sorted"),
        ([1, 2, 3, 4, 5], "Already sorted"),
    ]

    print("\n📋 Basic Sorting Tests:")
    print("-" * 60)

    for arr, description in test_arrays:
        original = arr.copy()
        sorted_arr = heap_sort(arr)

        print(f"\nTest: {description}")
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}")
        print(f"Correct:  {'✓' if is_sorted(sorted_arr) else '✗'}")

    print("\n" + "-" * 60)

    # Demonstrate heap visualization
    print("\n🌲 Heap Visualization:")
    print("-" * 60)

    data = [64, 34, 25, 12, 22, 11, 90]
    max_heap = MaxHeap(data)

    print("\nMax-Heap built from:", data)
    print(max_heap.visualize())

    print("\nMin-Heap built from:", data)
    min_heap = MinHeap(data)
    print(min_heap.visualize())

    # Demonstrate heap operations
    print("\n🔧 Heap Operations:")
    print("-" * 60)

    heap = MaxHeap[int]()
    operations = [50, 30, 70, 20, 40, 60, 80]

    print("\nInserting elements:", operations)
    for val in operations:
        heap.insert(val)
        print(f"Inserted {val}, Max: {heap.get_max()}")

    print("\nHeap structure:")
    print(heap.visualize())

    print("\nExtracting elements:")
    extracted = []
    while not heap.is_empty():
        val = heap.extract_max()
        extracted.append(val)
        print(f"Extracted: {val}")

    print(f"Extraction order: {extracted}")
    print(f"Is descending: {'✓' if extracted == sorted(extracted, reverse=True) else '✗'}")

    # Demonstrate priority queue
    print("\n📬 Priority Queue Demo:")
    print("-" * 60)

    pq = PriorityQueue[int]()
    tasks = [5, 1, 9, 3, 7]

    print(f"\nEnqueuing tasks with priorities: {tasks}")
    for priority in tasks:
        pq.enqueue(priority)
        print(f"Enqueued priority {priority}, Top priority: {pq.peek()}")

    print("\nProcessing tasks by priority:")
    while not pq.is_empty():
        priority = pq.dequeue()
        print(f"Processing task with priority: {priority}")


def performance_benchmark():
    """Benchmark heap sort against other O(n log n) algorithms."""
    print("\n\n⚡ Performance Benchmark")
    print("=" * 80)

    sizes = [100, 500, 1000, 5000, 10000]

    # Test different data patterns
    patterns = {
        "Random": lambda n: [random.randint(1, 1000) for _ in range(n)],
        "Sorted": lambda n: list(range(n)),
        "Reversed": lambda n: list(range(n, 0, -1)),
        "Nearly Sorted": lambda n: list(range(n)) if n < 10 else
                         list(range(n-5)) + [n-1, n-3, n-2, n-4, n-5] + list(range(n-5, n)),
    }

    methods = {
        "Heap Sort": heap_sort,
        "Built-in": lambda arr: sorted(arr),
    }

    # Try to import merge sort and quick sort if available
    try:
        from mergesort import merge_sort_recursive
        methods["Merge Sort"] = merge_sort_recursive
    except ImportError:
        pass

    for pattern_name, pattern_gen in patterns.items():
        print(f"\n{pattern_name} Data:")
        print("Size".rjust(8), end="")
        for method in methods:
            print(method.rjust(15), end="")
        print()
        print("-" * (8 + 15 * len(methods)))

        for size in sizes:
            test_data = pattern_gen(size)

            print(f"{size:8d}", end="")

            for method_name, method_func in methods.items():
                # Warm-up
                method_func(test_data[:100])

                # Benchmark
                start_time = time.perf_counter()
                result = method_func(test_data.copy())
                end_time = time.perf_counter()

                elapsed_ms = (end_time - start_time) * 1000
                print(f"{elapsed_ms:14.2f}ms", end="")

                # Verify correctness
                if not is_sorted(result if result else []):
                    print(" ✗", end="")

            print()


def test_edge_cases():
    """Test edge cases and error handling."""
    print("\n\n🧪 Edge Cases and Error Handling")
    print("=" * 60)

    print("\n1. Testing empty heap operations:")
    try:
        heap = MaxHeap[int]()
        heap.extract_max()
        print("   ✗ Should have raised IndexError")
    except IndexError as e:
        print(f"   ✓ Correctly raised: {e}")

    print("\n2. Testing get_max on empty heap:")
    try:
        heap = MaxHeap[int]()
        heap.get_max()
        print("   ✗ Should have raised IndexError")
    except IndexError as e:
        print(f"   ✓ Correctly raised: {e}")

    print("\n3. Testing increase_key with smaller value:")
    try:
        heap = MaxHeap([10, 20, 30])
        heap.increase_key(0, 5)
        print("   ✗ Should have raised ValueError")
    except ValueError as e:
        print(f"   ✓ Correctly raised: {e}")

    print("\n4. Testing decrease_key with larger value:")
    try:
        heap = MaxHeap([10, 20, 30])
        heap.decrease_key(0, 50)
        print("   ✗ Should have raised ValueError")
    except ValueError as e:
        print(f"   ✓ Correctly raised: {e}")

    print("\n5. Testing index out of bounds:")
    try:
        heap = MaxHeap([10, 20, 30])
        heap.increase_key(10, 50)
        print("   ✗ Should have raised IndexError")
    except IndexError as e:
        print(f"   ✓ Correctly raised: {e}")

    print("\n6. Testing with duplicates:")
    arr = [5, 5, 5, 5, 5]
    sorted_arr = heap_sort(arr)
    print(f"   Original: {arr}")
    print(f"   Sorted:   {sorted_arr}")
    print(f"   Correct:  {'✓' if sorted_arr == arr else '✗'}")

    print("\n7. Testing heap property after operations:")
    heap = MaxHeap([15, 10, 20, 8, 12, 25])
    print(f"   Initial heap: {heap.to_list()}")

    heap.insert(30)
    print(f"   After insert(30): {heap.to_list()}")
    print(f"   Max is 30: {'✓' if heap.get_max() == 30 else '✗'}")

    max_val = heap.extract_max()
    print(f"   Extracted: {max_val}")
    print(f"   New max is 25: {'✓' if heap.get_max() == 25 else '✗'}")


def analyze_heap_properties():
    """Analyze heap properties and complexity."""
    print("\n\n🔍 Heap Properties Analysis")
    print("=" * 60)

    data = [64, 34, 25, 12, 22, 11, 90]

    print(f"\nOriginal array: {data}")

    # Build max heap
    max_heap_arr = data.copy()
    build_max_heap(max_heap_arr)
    print(f"Max-heap array: {max_heap_arr}")

    # Verify max-heap property
    is_valid_max_heap = True
    for i in range(len(max_heap_arr)):
        left = 2 * i + 1
        right = 2 * i + 2

        if left < len(max_heap_arr) and max_heap_arr[i] < max_heap_arr[left]:
            is_valid_max_heap = False
            break
        if right < len(max_heap_arr) and max_heap_arr[i] < max_heap_arr[right]:
            is_valid_max_heap = False
            break

    print(f"Valid max-heap: {'✓' if is_valid_max_heap else '✗'}")

    # Build min heap
    min_heap_arr = data.copy()
    build_min_heap(min_heap_arr)
    print(f"Min-heap array: {min_heap_arr}")

    # Verify min-heap property
    is_valid_min_heap = True
    for i in range(len(min_heap_arr)):
        left = 2 * i + 1
        right = 2 * i + 2

        if left < len(min_heap_arr) and min_heap_arr[i] > min_heap_arr[left]:
            is_valid_min_heap = False
            break
        if right < len(min_heap_arr) and min_heap_arr[i] > min_heap_arr[right]:
            is_valid_min_heap = False
            break

    print(f"Valid min-heap: {'✓' if is_valid_min_heap else '✗'}")

    # Height analysis
    n = len(data)
    height = math.floor(math.log2(n))
    print(f"\nHeap size: {n}")
    print(f"Heap height: {height}")
    print(f"Max elements at height h: {2 ** height}")


if __name__ == "__main__":
    demonstrate_heap_sort()
    performance_benchmark()
    test_edge_cases()
    analyze_heap_properties()

    print("\n✨ Heap Sort demonstration complete!")
