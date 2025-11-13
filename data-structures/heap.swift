/*
 * ==============================================================================
 * Heap Data Structures in Swift
 *
 * Binary heap implementation for priority queues using Swift's
 * generics and protocols for type-safe, reusable code.
 *
 * Implementations:
 * - Generic Min Heap
 * - Generic Max Heap
 * - Priority Queue
 * - Heap Sort
 *
 * Swift's generics allow heap to work with any Comparable type!
 *
 * Compile: swiftc -O heap.swift
 * Run: ./heap
 *
 * @author Algorithms Multiverse
 * @version 1.0
 * ==============================================================================
 */

import Foundation

// ==============================================================================
// Generic Heap Structure
// ==============================================================================

struct Heap<T: Comparable> {
    private var elements: [T] = []
    private let orderCriteria: (T, T) -> Bool

    init(orderCriteria: @escaping (T, T) -> Bool) {
        self.orderCriteria = orderCriteria
    }

    // MARK: - Properties

    var count: Int { elements.count }
    var isEmpty: Bool { elements.isEmpty }
    var peek: T? { elements.first }

    // MARK: - Helper Functions

    private func parentIndex(of index: Int) -> Int { (index - 1) / 2 }
    private func leftChildIndex(of index: Int) -> Int { 2 * index + 1 }
    private func rightChildIndex(of index: Int) -> Int { 2 * index + 2 }

    // MARK: - Heap Operations

    /// Insert element
    ///
    /// Time Complexity: O(log n)
    mutating func insert(_ element: T) {
        elements.append(element)
        heapifyUp(from: elements.count - 1)
    }

    /// Extract root (min or max)
    ///
    /// Time Complexity: O(log n)
    mutating func extract() -> T? {
        guard !isEmpty else { return nil }

        if elements.count == 1 {
            return elements.removeLast()
        }

        let root = elements[0]
        elements[0] = elements.removeLast()
        heapifyDown(from: 0)

        return root
    }

    // MARK: - Heapify Operations

    private mutating func heapifyUp(from index: Int) {
        var childIndex = index
        let child = elements[childIndex]
        var parentIndex = self.parentIndex(of: childIndex)

        while childIndex > 0 && orderCriteria(child, elements[parentIndex]) {
            elements[childIndex] = elements[parentIndex]
            childIndex = parentIndex
            parentIndex = self.parentIndex(of: childIndex)
        }

        elements[childIndex] = child
    }

    private mutating func heapifyDown(from index: Int) {
        var parentIndex = index

        while true {
            let leftChildIndex = self.leftChildIndex(of: parentIndex)
            let rightChildIndex = self.rightChildIndex(of: parentIndex)
            var targetIndex = parentIndex

            if leftChildIndex < count && orderCriteria(elements[leftChildIndex], elements[targetIndex]) {
                targetIndex = leftChildIndex
            }

            if rightChildIndex < count && orderCriteria(elements[rightChildIndex], elements[targetIndex]) {
                targetIndex = rightChildIndex
            }

            if targetIndex == parentIndex {
                return
            }

            elements.swapAt(parentIndex, targetIndex)
            parentIndex = targetIndex
        }
    }

    // MARK: - Build Heap

    /// Build heap from array
    ///
    /// Time Complexity: O(n)
    static func buildHeap(from array: [T], orderCriteria: @escaping (T, T) -> Bool) -> Heap<T> {
        var heap = Heap(orderCriteria: orderCriteria)
        heap.elements = array

        if !array.isEmpty {
            for i in stride(from: array.count / 2 - 1, through: 0, by: -1) {
                heap.heapifyDown(from: i)
            }
        }

        return heap
    }
}

// ==============================================================================
// Convenience Initializers
// ==============================================================================

extension Heap {
    /// Create a min heap
    static func minHeap() -> Heap<T> {
        return Heap(orderCriteria: <)
    }

    /// Create a max heap
    static func maxHeap() -> Heap<T> {
        return Heap(orderCriteria: >)
    }
}

// ==============================================================================
// Heap Sort
// ==============================================================================

/// Heap Sort
///
/// Time Complexity: O(n log n)
/// Space Complexity: O(1) - in-place
///
/// Applications:
/// - Guaranteed O(n log n) worst case
/// - In-place sorting
func heapSort<T: Comparable>(_ array: [T]) -> [T] {
    var heap = Heap<T>.maxHeap()

    // Build heap
    for element in array {
        heap.insert(element)
    }

    // Extract elements
    var sorted = [T]()
    while let max = heap.extract() {
        sorted.insert(max, at: 0)
    }

    return sorted
}

// ==============================================================================
// Priority Queue
// ==============================================================================

struct PriorityQueue<T: Comparable> {
    private var heap: Heap<T>

    init() {
        heap = Heap.minHeap()
    }

    var isEmpty: Bool { heap.isEmpty }
    var count: Int { heap.count }
    var peek: T? { heap.peek }

    mutating func enqueue(_ element: T) {
        heap.insert(element)
    }

    mutating func dequeue() -> T? {
        heap.extract()
    }
}

// ==============================================================================
// Main Program - Examples and Tests
// ==============================================================================

print("==============================================================================")
print("                HEAP DATA STRUCTURES IN SWIFT")
print("            Generic Priority Queues & Heap Sort")
print("==============================================================================\n")

// Example 1: Min Heap
print("Example 1: Min Heap (Priority Queue)")
print(String(repeating: "=", count: 80))

var minHeap = Heap<Int>.minHeap()
let values = [15, 10, 20, 8, 21, 5]

print("Inserting:", values.map { String($0) }.joined(separator: ", "))
for value in values {
    minHeap.insert(value)
}

print("Minimum (peek):", minHeap.peek ?? 0)

print("\nExtracting minimum elements:")
while let min = minHeap.extract() {
    print("  Extracted:", min)
}
print()

// Example 2: Max Heap
print("Example 2: Max Heap")
print(String(repeating: "=", count: 80))

var maxHeap = Heap<Int>.maxHeap()
let values2 = [15, 10, 20, 8, 21, 5]

print("Inserting:", values2.map { String($0) }.joined(separator: ", "))
for value in values2 {
    maxHeap.insert(value)
}

print("Maximum:", maxHeap.peek ?? 0)
print()

// Example 3: Heap Sort
print("Example 3: Heap Sort")
print(String(repeating: "=", count: 80))

let unsorted = [12, 11, 13, 5, 6, 7]
print("Original:", unsorted.map { String($0) }.joined(separator: ", "))

let sorted = heapSort(unsorted)
print("Sorted:  ", sorted.map { String($0) }.joined(separator: ", "))
print()

// Example 4: Build Heap from Array
print("Example 4: Build Min Heap from Array")
print(String(repeating: "=", count: 80))

let array = [9, 5, 6, 2, 3, 7, 1, 4, 8]
print("Array:", array.map { String($0) }.joined(separator: ", "))

let builtHeap = Heap.buildHeap(from: array, orderCriteria: <)
print("Minimum:", builtHeap.peek ?? 0)
print()

// Example 5: Priority Queue Application
print("Example 5: Priority Queue (Task Scheduling)")
print(String(repeating: "=", count: 80))

struct Task: Comparable {
    let name: String
    let priority: Int

    static func < (lhs: Task, rhs: Task) -> Bool {
        lhs.priority < rhs.priority
    }

    static func == (lhs: Task, rhs: Task) -> Bool {
        lhs.priority == rhs.priority
    }
}

var taskQueue = PriorityQueue<Task>()

let tasks = [
    Task(name: "Email", priority: 3),
    Task(name: "Meeting", priority: 1),
    Task(name: "Code Review", priority: 2),
    Task(name: "Bug Fix", priority: 1),
    Task(name: "Documentation", priority: 4)
]

print("Adding tasks:")
for task in tasks {
    print(String(format: "  %@ (priority %d)", task.name, task.priority))
    taskQueue.enqueue(task)
}

print("\nProcessing tasks by priority:")
while let task = taskQueue.dequeue() {
    print(String(format: "  Processing: %@ (priority %d)", task.name, task.priority))
}
print()

// Example 6: Generic Heap with Strings
print("Example 6: Generic Heap with Strings")
print(String(repeating: "=", count: 80))

var stringHeap = Heap<String>.minHeap()
let words = ["banana", "apple", "cherry", "date", "elderberry"]

print("Inserting:", words.joined(separator: ", "))
for word in words {
    stringHeap.insert(word)
}

print("Extracting in sorted order:")
while let word = stringHeap.extract() {
    print("  ", word)
}
print()

// Summary
print(String(repeating: "=", count: 80))
print("Summary: Heap Data Structures in Swift")
print(String(repeating: "=", count: 80))
print("✓ Generic implementation works with any Comparable type")
print("✓ Min/Max Heap: O(log n) insert/extract")
print("✓ Peek: O(1) to get min/max")
print("✓ Build heap: O(n) from array")
print("✓ Heap sort: O(n log n) guaranteed")
print("\nSwift Advantages:")
print("- Type-safe generics")
print("- Protocol-oriented design")
print("- Value semantics with copy-on-write")
print("\nApplications:")
print("- Priority queues (task scheduling)")
print("- Dijkstra's shortest path")
print("- Heap sort")
print("- Finding k largest/smallest elements")
print(String(repeating: "=", count: 80))
