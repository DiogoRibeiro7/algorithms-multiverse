/**
 * Heap Sort Algorithm Implementation in Swift
 *
 * Time Complexity: O(n log n) - consistently across all cases
 * Space Complexity: O(1) for in-place sorting, O(n) for auxiliary heap
 *
 * Heap Sort is a comparison-based sorting algorithm that uses a binary heap data
 * structure. It divides its input into a sorted and an unsorted region, and it
 * iteratively shrinks the unsorted region by extracting the largest element and
 * inserting it into the sorted region.
 *
 * Swift features:
 * - Generic types and protocols
 * - Value semantics
 * - Error handling
 * - Protocol-oriented programming
 * - Modern Swift features
 */

import Foundation

/// Maintain the max-heap property for a subtree rooted at index i.
///
/// Time Complexity: O(log n)
func heapifyMax<T: Comparable>(_ arr: inout [T], n: Int, i: Int) {
    var largest = i
    let left = 2 * i + 1
    let right = 2 * i + 2

    // Check if left child exists and is greater than root
    if left < n && arr[left] > arr[largest] {
        largest = left
    }

    // Check if right child exists and is greater than largest so far
    if right < n && arr[right] > arr[largest] {
        largest = right
    }

    // If largest is not root, swap and recursively heapify
    if largest != i {
        arr.swapAt(i, largest)
        heapifyMax(&arr, n: n, i: largest)
    }
}

/// Maintain the min-heap property for a subtree rooted at index i.
///
/// Time Complexity: O(log n)
func heapifyMin<T: Comparable>(_ arr: inout [T], n: Int, i: Int) {
    var smallest = i
    let left = 2 * i + 1
    let right = 2 * i + 2

    if left < n && arr[left] < arr[smallest] {
        smallest = left
    }

    if right < n && arr[right] < arr[smallest] {
        smallest = right
    }

    if smallest != i {
        arr.swapAt(i, smallest)
        heapifyMin(&arr, n: n, i: smallest)
    }
}

/// Build a max-heap from an unordered array.
///
/// Time Complexity: O(n)
func buildMaxHeap<T: Comparable>(_ arr: inout [T]) {
    let n = arr.count
    guard n > 0 else { return }

    // Start from the last non-leaf node and heapify each node
    for i in stride(from: n / 2 - 1, through: 0, by: -1) {
        heapifyMax(&arr, n: n, i: i)
    }
}

/// Build a min-heap from an unordered array.
///
/// Time Complexity: O(n)
func buildMinHeap<T: Comparable>(_ arr: inout [T]) {
    let n = arr.count
    guard n > 0 else { return }

    for i in stride(from: n / 2 - 1, through: 0, by: -1) {
        heapifyMin(&arr, n: n, i: i)
    }
}

/// Sort an array using heap sort algorithm.
///
/// Time Complexity: O(n log n)
func heapSort<T: Comparable>(_ arr: [T]) -> [T] {
    if arr.count <= 1 {
        return arr
    }

    var result = arr
    heapSortInPlace(&result)
    return result
}

/// Sort an array in-place using heap sort algorithm.
///
/// Time Complexity: O(n log n)
/// Space Complexity: O(1)
func heapSortInPlace<T: Comparable>(_ arr: inout [T]) {
    let n = arr.count

    // Build a max heap
    buildMaxHeap(&arr)

    // Extract elements from heap one by one
    for i in stride(from: n - 1, to: 0, by: -1) {
        // Move current root to end
        arr.swapAt(0, i)
        // Call heapify on the reduced heap
        heapifyMax(&arr, n: i, i: 0)
    }
}

/// Check if array is sorted in ascending order.
func isSorted<T: Comparable>(_ arr: [T]) -> Bool {
    for i in 0..<arr.count - 1 {
        if arr[i] > arr[i + 1] {
            return false
        }
    }
    return true
}

/// Error types for heap operations
enum HeapError: Error {
    case emptyHeap(String)
    case invalidKey(String)
    case indexOutOfBounds(String)
}

/// Max-Heap data structure implementation.
class MaxHeap<T: Comparable> {
    private var heap: [T]

    init() {
        self.heap = []
    }

    init(initialData: [T]) {
        self.heap = initialData
        buildHeap()
    }

    private func parent(_ i: Int) -> Int {
        return (i - 1) / 2
    }

    private func left(_ i: Int) -> Int {
        return 2 * i + 1
    }

    private func right(_ i: Int) -> Int {
        return 2 * i + 2
    }

    private func buildHeap() {
        let n = heap.count
        guard n > 0 else { return }

        for i in stride(from: n / 2 - 1, through: 0, by: -1) {
            heapifyDown(i)
        }
    }

    private func bubbleUp(_ i: Int) {
        var index = i
        while index > 0 && heap[parent(index)] < heap[index] {
            let parentIndex = parent(index)
            heap.swapAt(index, parentIndex)
            index = parentIndex
        }
    }

    private func heapifyDown(_ i: Int) {
        var largest = i
        let l = left(i)
        let r = right(i)

        if l < heap.count && heap[l] > heap[largest] {
            largest = l
        }

        if r < heap.count && heap[r] > heap[largest] {
            largest = r
        }

        if largest != i {
            heap.swapAt(i, largest)
            heapifyDown(largest)
        }
    }

    /// Insert a new key into the heap.
    ///
    /// Time Complexity: O(log n)
    func insert(_ key: T) {
        heap.append(key)
        bubbleUp(heap.count - 1)
    }

    /// Remove and return the maximum element (root) from the heap.
    ///
    /// Time Complexity: O(log n)
    func extractMax() throws -> T {
        guard !heap.isEmpty else {
            throw HeapError.emptyHeap("extractMax from empty heap")
        }

        if heap.count == 1 {
            return heap.removeLast()
        }

        let max = heap[0]
        heap[0] = heap.removeLast()
        heapifyDown(0)

        return max
    }

    /// Get the maximum element without removing it.
    func getMax() throws -> T {
        guard !heap.isEmpty else {
            throw HeapError.emptyHeap("getMax from empty heap")
        }
        return heap[0]
    }

    /// Increase the value of a key at index i.
    ///
    /// Time Complexity: O(log n)
    func increaseKey(at i: Int, to newKey: T) throws {
        guard i >= 0 && i < heap.count else {
            throw HeapError.indexOutOfBounds("Index \\(i) out of bounds")
        }

        guard newKey >= heap[i] else {
            throw HeapError.invalidKey("New key is smaller than current key")
        }

        heap[i] = newKey
        bubbleUp(i)
    }

    /// Decrease the value of a key at index i.
    ///
    /// Time Complexity: O(log n)
    func decreaseKey(at i: Int, to newKey: T) throws {
        guard i >= 0 && i < heap.count else {
            throw HeapError.indexOutOfBounds("Index \\(i) out of bounds")
        }

        guard newKey <= heap[i] else {
            throw HeapError.invalidKey("New key is greater than current key")
        }

        heap[i] = newKey
        heapifyDown(i)
    }

    /// Return the size of the heap.
    var size: Int {
        return heap.count
    }

    /// Check if the heap is empty.
    var isEmpty: Bool {
        return heap.isEmpty
    }

    /// Return a copy of the heap array.
    func toArray() -> [T] {
        return heap
    }

    /// Create ASCII art visualization of the heap.
    func visualize() -> String {
        guard !heap.isEmpty else {
            return "Empty heap"
        }

        var lines: [String] = []
        visualizeHelper(i: 0, prefix: "", childPrefix: "", lines: &lines)
        return lines.joined(separator: "\\n")
    }

    private func visualizeHelper(i: Int, prefix: String, childPrefix: String, lines: inout [String]) {
        guard i < heap.count else { return }

        lines.append("\\(prefix)\\(heap[i])")

        let leftIdx = left(i)
        let rightIdx = right(i)

        if leftIdx < heap.count || rightIdx < heap.count {
            if leftIdx < heap.count {
                if rightIdx < heap.count {
                    visualizeHelper(i: leftIdx, prefix: childPrefix + "├── ", childPrefix: childPrefix + "│   ", lines: &lines)
                } else {
                    visualizeHelper(i: leftIdx, prefix: childPrefix + "└── ", childPrefix: childPrefix + "    ", lines: &lines)
                }
            }

            if rightIdx < heap.count {
                visualizeHelper(i: rightIdx, prefix: childPrefix + "└── ", childPrefix: childPrefix + "    ", lines: &lines)
            }
        }
    }
}

/// Min-Heap data structure implementation.
class MinHeap<T: Comparable> {
    private var heap: [T]

    init() {
        self.heap = []
    }

    init(initialData: [T]) {
        self.heap = initialData
        buildHeap()
    }

    private func parent(_ i: Int) -> Int {
        return (i - 1) / 2
    }

    private func left(_ i: Int) -> Int {
        return 2 * i + 1
    }

    private func right(_ i: Int) -> Int {
        return 2 * i + 2
    }

    private func buildHeap() {
        let n = heap.count
        guard n > 0 else { return }

        for i in stride(from: n / 2 - 1, through: 0, by: -1) {
            heapifyDown(i)
        }
    }

    private func bubbleUp(_ i: Int) {
        var index = i
        while index > 0 && heap[parent(index)] > heap[index] {
            let parentIndex = parent(index)
            heap.swapAt(index, parentIndex)
            index = parentIndex
        }
    }

    private func heapifyDown(_ i: Int) {
        var smallest = i
        let l = left(i)
        let r = right(i)

        if l < heap.count && heap[l] < heap[smallest] {
            smallest = l
        }

        if r < heap.count && heap[r] < heap[smallest] {
            smallest = r
        }

        if smallest != i {
            heap.swapAt(i, smallest)
            heapifyDown(smallest)
        }
    }

    func insert(_ key: T) {
        heap.append(key)
        bubbleUp(heap.count - 1)
    }

    func extractMin() throws -> T {
        guard !heap.isEmpty else {
            throw HeapError.emptyHeap("extractMin from empty heap")
        }

        if heap.count == 1 {
            return heap.removeLast()
        }

        let min = heap[0]
        heap[0] = heap.removeLast()
        heapifyDown(0)

        return min
    }

    func getMin() throws -> T {
        guard !heap.isEmpty else {
            throw HeapError.emptyHeap("getMin from empty heap")
        }
        return heap[0]
    }

    var size: Int {
        return heap.count
    }

    var isEmpty: Bool {
        return heap.isEmpty
    }

    func visualize() -> String {
        guard !heap.isEmpty else {
            return "Empty heap"
        }

        var lines: [String] = []
        visualizeHelper(i: 0, prefix: "", childPrefix: "", lines: &lines)
        return lines.joined(separator: "\\n")
    }

    private func visualizeHelper(i: Int, prefix: String, childPrefix: String, lines: inout [String]) {
        guard i < heap.count else { return }

        lines.append("\\(prefix)\\(heap[i])")

        let leftIdx = left(i)
        let rightIdx = right(i)

        if leftIdx < heap.count || rightIdx < heap.count {
            if leftIdx < heap.count {
                if rightIdx < heap.count {
                    visualizeHelper(i: leftIdx, prefix: childPrefix + "├── ", childPrefix: childPrefix + "│   ", lines: &lines)
                } else {
                    visualizeHelper(i: leftIdx, prefix: childPrefix + "└── ", childPrefix: childPrefix + "    ", lines: &lines)
                }
            }

            if rightIdx < heap.count {
                visualizeHelper(i: rightIdx, prefix: childPrefix + "└── ", childPrefix: childPrefix + "    ", lines: &lines)
            }
        }
    }
}

/// Priority Queue implementation using a max-heap.
class PriorityQueue<T: Comparable> {
    private let heap: MaxHeap<T>

    init() {
        self.heap = MaxHeap()
    }

    func enqueue(_ item: T) {
        heap.insert(item)
    }

    func dequeue() throws -> T {
        return try heap.extractMax()
    }

    func peek() throws -> T {
        return try heap.getMax()
    }

    var isEmpty: Bool {
        return heap.isEmpty
    }

    var size: Int {
        return heap.size
    }
}

/// Demonstrate heap sort and heap data structure.
func demonstrateHeapSort() {
    print("🏔️  Heap Sort Implementation in Swift")
    print(String(repeating: "=", count: 60))

    // Test data
    let testCases: [([Int], String)] = [
        ([64, 34, 25, 12, 22, 11, 90], "Random array"),
        ([5, 2, 8, 6, 1, 9, 4], "Small random array"),
        ([1], "Single element"),
        ([], "Empty array"),
        ([3, 3, 3, 3, 3], "All duplicates"),
        ([9, 8, 7, 6, 5, 4, 3, 2, 1], "Reverse sorted"),
        ([1, 2, 3, 4, 5], "Already sorted")
    ]

    print("\\n📋 Basic Sorting Tests:")
    print(String(repeating: "-", count: 60))

    for (arr, desc) in testCases {
        let original = arr
        let sortedArr = heapSort(arr)

        print("\\nTest: \\(desc)")
        print("Original: \\(original)")
        print("Sorted:   \\(sortedArr)")
        print("Correct:  \\(isSorted(sortedArr) ? "✓" : "✗")")
    }

    print("\\n" + String(repeating: "-", count: 60))

    // Demonstrate heap visualization
    print("\\n🌲 Heap Visualization:")
    print(String(repeating: "-", count: 60))

    let data = [64, 34, 25, 12, 22, 11, 90]
    let maxHeap = MaxHeap(initialData: data)

    print("\\nMax-Heap built from: \\(data)")
    print(maxHeap.visualize())

    print("\\nMin-Heap built from: \\(data)")
    let minHeap = MinHeap(initialData: data)
    print(minHeap.visualize())

    // Demonstrate heap operations
    print("\\n🔧 Heap Operations:")
    print(String(repeating: "-", count: 60))

    let heap = MaxHeap<Int>()
    let operations = [50, 30, 70, 20, 40, 60, 80]

    print("\\nInserting elements: \\(operations)")
    for val in operations {
        heap.insert(val)
        if let max = try? heap.getMax() {
            print("Inserted \\(val), Max: \\(max)")
        }
    }

    print("\\nHeap structure:")
    print(heap.visualize())

    print("\\nExtracting elements:")
    var extracted: [Int] = []
    while !heap.isEmpty {
        if let val = try? heap.extractMax() {
            extracted.append(val)
            print("Extracted: \\(val)")
        }
    }

    print("Extraction order: \\(extracted)")

    // Demonstrate priority queue
    print("\\n📬 Priority Queue Demo:")
    print(String(repeating: "-", count: 60))

    let pq = PriorityQueue<Int>()
    let tasks = [5, 1, 9, 3, 7]

    print("\\nEnqueuing tasks with priorities: \\(tasks)")
    for priority in tasks {
        pq.enqueue(priority)
        if let top = try? pq.peek() {
            print("Enqueued priority \\(priority), Top priority: \\(top)")
        }
    }

    print("\\nProcessing tasks by priority:")
    while !pq.isEmpty {
        if let priority = try? pq.dequeue() {
            print("Processing task with priority: \\(priority)")
        }
    }
}

/// Test edge cases.
func testEdgeCases() {
    print("\\n\\n🧪 Edge Cases and Error Handling")
    print(String(repeating: "=", count: 60))

    print("\\n1. Testing empty heap operations:")
    let heap1 = MaxHeap<Int>()
    do {
        _ = try heap1.extractMax()
        print("   ✗ Should have thrown error")
    } catch {
        print("   ✓ Correctly threw: \\(error)")
    }

    print("\\n2. Testing increaseKey with smaller value:")
    let heap2 = MaxHeap(initialData: [10, 20, 30])
    do {
        try heap2.increaseKey(at: 0, to: 5)
        print("   ✗ Should have thrown error")
    } catch {
        print("   ✓ Correctly threw: \\(error)")
    }

    print("\\n3. Testing with duplicates:")
    let arr = [5, 5, 5, 5, 5]
    let sorted = heapSort(arr)
    print("   Original: \\(arr)")
    print("   Sorted:   \\(sorted)")
    print("   Correct:  \\(sorted == arr ? "✓" : "✗")")
}

// Main execution
demonstrateHeapSort()
testEdgeCases()

print("\\n✨ Heap Sort demonstration complete!")
