import Foundation

// MARK: - Linked List

/// Generic doubly-linked list implementation
public class LinkedListNode<T> {
    public var value: T
    public var next: LinkedListNode<T>?
    public weak var previous: LinkedListNode<T>?

    public init(value: T) {
        self.value = value
    }
}

public class LinkedList<T> {
    private var head: LinkedListNode<T>?
    private var tail: LinkedListNode<T>?
    private(set) var count: Int = 0

    public var isEmpty: Bool { head == nil }
    public var first: LinkedListNode<T>? { head }
    public var last: LinkedListNode<T>? { tail }

    /// Append value to the end
    public func append(_ value: T) {
        let newNode = LinkedListNode(value: value)
        if let tailNode = tail {
            newNode.previous = tailNode
            tailNode.next = newNode
        } else {
            head = newNode
        }
        tail = newNode
        count += 1
    }

    /// Prepend value to the beginning
    public func prepend(_ value: T) {
        let newNode = LinkedListNode(value: value)
        if let headNode = head {
            newNode.next = headNode
            headNode.previous = newNode
        } else {
            tail = newNode
        }
        head = newNode
        count += 1
    }

    /// Remove node at index
    public func remove(at index: Int) -> T? {
        guard index >= 0 && index < count else { return nil }

        var current = head
        for _ in 0..<index {
            current = current?.next
        }

        return remove(node: current!)
    }

    /// Remove specific node
    @discardableResult
    public func remove(node: LinkedListNode<T>) -> T {
        let prev = node.previous
        let next = node.next

        if let prev = prev {
            prev.next = next
        } else {
            head = next
        }

        if let next = next {
            next.previous = prev
        } else {
            tail = prev
        }

        count -= 1
        node.next = nil
        node.previous = nil

        return node.value
    }
}

// MARK: - LinkedList Collection conformance

extension LinkedList: Collection {
    public typealias Index = LinkedListIndex<T>

    public var startIndex: Index {
        LinkedListIndex(node: head, tag: 0)
    }

    public var endIndex: Index {
        LinkedListIndex(node: nil, tag: count)
    }

    public subscript(index: Index) -> T {
        index.node!.value
    }

    public func index(after index: Index) -> Index {
        LinkedListIndex(node: index.node?.next, tag: index.tag + 1)
    }
}

public struct LinkedListIndex<T>: Comparable {
    fileprivate let node: LinkedListNode<T>?
    fileprivate let tag: Int

    public static func == (lhs: LinkedListIndex<T>, rhs: LinkedListIndex<T>) -> Bool {
        lhs.tag == rhs.tag
    }

    public static func < (lhs: LinkedListIndex<T>, rhs: LinkedListIndex<T>) -> Bool {
        lhs.tag < rhs.tag
    }
}

// MARK: - Stack

/// LIFO stack implementation
public struct Stack<T> {
    private var array: [T] = []

    public var isEmpty: Bool { array.isEmpty }
    public var count: Int { array.count }
    public var top: T? { array.last }

    public mutating func push(_ element: T) {
        array.append(element)
    }

    @discardableResult
    public mutating func pop() -> T? {
        array.popLast()
    }

    public func peek() -> T? {
        array.last
    }
}

// MARK: - Queue

/// FIFO queue implementation with circular buffer
public struct Queue<T> {
    private var array: [T?]
    private var head: Int = 0
    private var tail: Int = 0
    private var _count: Int = 0

    public init(capacity: Int = 16) {
        array = Array(repeating: nil, count: capacity)
    }

    public var isEmpty: Bool { _count == 0 }
    public var count: Int { _count }
    public var front: T? { isEmpty ? nil : array[head] }

    public mutating func enqueue(_ element: T) {
        if _count == array.count {
            expandCapacity()
        }

        array[tail] = element
        tail = (tail + 1) % array.count
        _count += 1
    }

    @discardableResult
    public mutating func dequeue() -> T? {
        guard !isEmpty else { return nil }

        let element = array[head]
        array[head] = nil
        head = (head + 1) % array.count
        _count -= 1

        return element
    }

    private mutating func expandCapacity() {
        var newArray = [T?](repeating: nil, count: array.count * 2)
        var newIndex = 0
        var oldIndex = head

        while oldIndex != tail {
            newArray[newIndex] = array[oldIndex]
            newIndex += 1
            oldIndex = (oldIndex + 1) % array.count
        }

        head = 0
        tail = _count
        array = newArray
    }
}

// MARK: - Priority Queue

/// Min-heap based priority queue
public struct PriorityQueue<T: Comparable> {
    private var heap: [T] = []

    public var isEmpty: Bool { heap.isEmpty }
    public var count: Int { heap.count }
    public var peek: T? { heap.first }

    public mutating func enqueue(_ element: T) {
        heap.append(element)
        siftUp(from: heap.count - 1)
    }

    @discardableResult
    public mutating func dequeue() -> T? {
        guard !heap.isEmpty else { return nil }

        if heap.count == 1 {
            return heap.removeFirst()
        }

        let value = heap[0]
        heap[0] = heap.removeLast()
        siftDown(from: 0)

        return value
    }

    private mutating func siftUp(from index: Int) {
        var child = index
        var parent = parentIndex(of: child)

        while child > 0 && heap[child] < heap[parent] {
            heap.swapAt(child, parent)
            child = parent
            parent = parentIndex(of: child)
        }
    }

    private mutating func siftDown(from index: Int) {
        var parent = index

        while true {
            let left = leftChildIndex(of: parent)
            let right = rightChildIndex(of: parent)
            var candidate = parent

            if left < heap.count && heap[left] < heap[candidate] {
                candidate = left
            }
            if right < heap.count && heap[right] < heap[candidate] {
                candidate = right
            }
            if candidate == parent {
                return
            }

            heap.swapAt(parent, candidate)
            parent = candidate
        }
    }

    private func parentIndex(of index: Int) -> Int {
        (index - 1) / 2
    }

    private func leftChildIndex(of index: Int) -> Int {
        2 * index + 1
    }

    private func rightChildIndex(of index: Int) -> Int {
        2 * index + 2
    }
}

// MARK: - Binary Search Tree

/// Binary Search Tree node
public class BinaryTreeNode<T: Comparable> {
    public var value: T
    public var left: BinaryTreeNode<T>?
    public var right: BinaryTreeNode<T>?

    public init(value: T) {
        self.value = value
    }
}

/// Binary Search Tree implementation
public class BinarySearchTree<T: Comparable> {
    private var root: BinaryTreeNode<T>?

    public var isEmpty: Bool { root == nil }

    /// Insert value into BST
    public func insert(_ value: T) {
        root = insert(value, into: root)
    }

    private func insert(_ value: T, into node: BinaryTreeNode<T>?) -> BinaryTreeNode<T> {
        guard let node = node else {
            return BinaryTreeNode(value: value)
        }

        if value < node.value {
            node.left = insert(value, into: node.left)
        } else if value > node.value {
            node.right = insert(value, into: node.right)
        }

        return node
    }

    /// Search for value
    public func search(_ value: T) -> Bool {
        search(value, in: root)
    }

    private func search(_ value: T, in node: BinaryTreeNode<T>?) -> Bool {
        guard let node = node else { return false }

        if value == node.value {
            return true
        } else if value < node.value {
            return search(value, in: node.left)
        } else {
            return search(value, in: node.right)
        }
    }

    /// Delete value from BST
    public func delete(_ value: T) {
        root = delete(value, from: root)
    }

    private func delete(_ value: T, from node: BinaryTreeNode<T>?) -> BinaryTreeNode<T>? {
        guard let node = node else { return nil }

        if value < node.value {
            node.left = delete(value, from: node.left)
        } else if value > node.value {
            node.right = delete(value, from: node.right)
        } else {
            // Node to be deleted found
            if node.left == nil {
                return node.right
            } else if node.right == nil {
                return node.left
            }

            // Node with two children
            node.value = minValue(in: node.right!)
            node.right = delete(node.value, from: node.right)
        }

        return node
    }

    private func minValue(in node: BinaryTreeNode<T>) -> T {
        var current = node
        while let left = current.left {
            current = left
        }
        return current.value
    }

    /// In-order traversal
    public func inOrderTraversal() -> [T] {
        var result: [T] = []
        inOrderHelper(root, &result)
        return result
    }

    private func inOrderHelper(_ node: BinaryTreeNode<T>?, _ result: inout [T]) {
        guard let node = node else { return }

        inOrderHelper(node.left, &result)
        result.append(node.value)
        inOrderHelper(node.right, &result)
    }

    /// Get tree height
    public var height: Int {
        height(of: root)
    }

    private func height(of node: BinaryTreeNode<T>?) -> Int {
        guard let node = node else { return 0 }
        return 1 + max(height(of: node.left), height(of: node.right))
    }

    /// Check if tree is balanced
    public var isBalanced: Bool {
        checkBalance(root) != -1
    }

    private func checkBalance(_ node: BinaryTreeNode<T>?) -> Int {
        guard let node = node else { return 0 }

        let leftHeight = checkBalance(node.left)
        if leftHeight == -1 { return -1 }

        let rightHeight = checkBalance(node.right)
        if rightHeight == -1 { return -1 }

        if abs(leftHeight - rightHeight) > 1 { return -1 }

        return max(leftHeight, rightHeight) + 1
    }
}

// MARK: - Hash Table

/// Hash table with separate chaining
public class HashTable<Key: Hashable, Value> {
    private typealias Bucket = [(key: Key, value: Value)]
    private var buckets: [Bucket]
    private(set) var count = 0

    public init(capacity: Int = 16) {
        buckets = Array(repeating: [], count: capacity)
    }

    /// Get or set value for key
    public subscript(key: Key) -> Value? {
        get {
            getValue(for: key)
        }
        set {
            if let value = newValue {
                updateValue(value, for: key)
            } else {
                removeValue(for: key)
            }
        }
    }

    private func index(for key: Key) -> Int {
        abs(key.hashValue) % buckets.count
    }

    private func getValue(for key: Key) -> Value? {
        let index = index(for: key)
        for (k, v) in buckets[index] {
            if k == key { return v }
        }
        return nil
    }

    private func updateValue(_ value: Value, for key: Key) {
        let index = index(for: key)

        for (i, element) in buckets[index].enumerated() {
            if element.key == key {
                buckets[index][i].value = value
                return
            }
        }

        buckets[index].append((key: key, value: value))
        count += 1

        if count > buckets.count * 3/4 {
            resize()
        }
    }

    private func removeValue(for key: Key) {
        let index = index(for: key)

        for (i, element) in buckets[index].enumerated() {
            if element.key == key {
                buckets[index].remove(at: i)
                count -= 1
                return
            }
        }
    }

    private func resize() {
        let oldBuckets = buckets
        buckets = Array(repeating: [], count: oldBuckets.count * 2)
        count = 0

        for bucket in oldBuckets {
            for (key, value) in bucket {
                updateValue(value, for: key)
            }
        }
    }
}

// MARK: - Trie

/// Trie node for string operations
public class TrieNode {
    public var children: [Character: TrieNode] = [:]
    public var isEndOfWord: Bool = false
    public var frequency: Int = 0
}

/// Trie (Prefix Tree) implementation
public class Trie {
    private let root = TrieNode()

    /// Insert word into trie
    public func insert(_ word: String) {
        var current = root
        for char in word {
            if let child = current.children[char] {
                current = child
            } else {
                let newNode = TrieNode()
                current.children[char] = newNode
                current = newNode
            }
        }
        current.isEndOfWord = true
        current.frequency += 1
    }

    /// Search for word
    public func search(_ word: String) -> Bool {
        guard let node = searchNode(word) else { return false }
        return node.isEndOfWord
    }

    /// Check if any word starts with prefix
    public func startsWith(_ prefix: String) -> Bool {
        searchNode(prefix) != nil
    }

    private func searchNode(_ str: String) -> TrieNode? {
        var current = root
        for char in str {
            guard let child = current.children[char] else { return nil }
            current = child
        }
        return current
    }

    /// Get all words with given prefix
    public func wordsWithPrefix(_ prefix: String) -> [String] {
        var results: [String] = []
        guard let prefixNode = searchNode(prefix) else { return results }

        dfsCollectWords(from: prefixNode, prefix: prefix, results: &results)
        return results
    }

    private func dfsCollectWords(from node: TrieNode, prefix: String, results: inout [String]) {
        if node.isEndOfWord {
            results.append(prefix)
        }

        for (char, child) in node.children {
            dfsCollectWords(from: child, prefix: prefix + String(char), results: &results)
        }
    }

    /// Delete word from trie
    public func delete(_ word: String) {
        deleteHelper(root, word, 0)
    }

    @discardableResult
    private func deleteHelper(_ node: TrieNode, _ word: String, _ index: Int) -> Bool {
        if index == word.count {
            if !node.isEndOfWord { return false }
            node.isEndOfWord = false
            return node.children.isEmpty
        }

        let char = Array(word)[index]
        guard let child = node.children[char] else { return false }

        let shouldDeleteChild = deleteHelper(child, word, index + 1)

        if shouldDeleteChild {
            node.children[char] = nil
            return node.children.isEmpty && !node.isEndOfWord
        }

        return false
    }
}

// MARK: - Graph

/// Generic graph implementation with adjacency list
public class Graph<T: Hashable> {
    private var adjacencyList: [T: Set<T>] = [:]
    public var isDirected: Bool

    public init(isDirected: Bool = false) {
        self.isDirected = isDirected
    }

    public var vertices: Set<T> {
        Set(adjacencyList.keys)
    }

    public var edgeCount: Int {
        adjacencyList.values.reduce(0) { $0 + $1.count } / (isDirected ? 1 : 2)
    }

    /// Add vertex to graph
    public func addVertex(_ vertex: T) {
        if adjacencyList[vertex] == nil {
            adjacencyList[vertex] = []
        }
    }

    /// Add edge between vertices
    public func addEdge(from: T, to: T) {
        addVertex(from)
        addVertex(to)

        adjacencyList[from]?.insert(to)
        if !isDirected {
            adjacencyList[to]?.insert(from)
        }
    }

    /// Get neighbors of vertex
    public func neighbors(of vertex: T) -> Set<T> {
        adjacencyList[vertex] ?? []
    }

    /// Check if edge exists
    public func hasEdge(from: T, to: T) -> Bool {
        adjacencyList[from]?.contains(to) ?? false
    }

    /// Get degree of vertex
    public func degree(of vertex: T) -> Int {
        if isDirected {
            return inDegree(of: vertex) + outDegree(of: vertex)
        } else {
            return adjacencyList[vertex]?.count ?? 0
        }
    }

    /// Get in-degree (directed graphs)
    public func inDegree(of vertex: T) -> Int {
        guard isDirected else { return degree(of: vertex) }

        var count = 0
        for (_, neighbors) in adjacencyList {
            if neighbors.contains(vertex) {
                count += 1
            }
        }
        return count
    }

    /// Get out-degree (directed graphs)
    public func outDegree(of vertex: T) -> Int {
        adjacencyList[vertex]?.count ?? 0
    }
}

// MARK: - Disjoint Set (Union-Find)

/// Union-Find data structure with path compression and union by rank
public class DisjointSet<T: Hashable> {
    private var parent: [T: T] = [:]
    private var rank: [T: Int] = [:]

    /// Find with path compression
    public func find(_ element: T) -> T {
        if parent[element] == nil {
            parent[element] = element
            rank[element] = 0
            return element
        }

        if parent[element] != element {
            parent[element] = find(parent[element]!)
        }

        return parent[element]!
    }

    /// Union by rank
    public func union(_ a: T, _ b: T) {
        let rootA = find(a)
        let rootB = find(b)

        if rootA == rootB { return }

        let rankA = rank[rootA] ?? 0
        let rankB = rank[rootB] ?? 0

        if rankA < rankB {
            parent[rootA] = rootB
        } else if rankA > rankB {
            parent[rootB] = rootA
        } else {
            parent[rootB] = rootA
            rank[rootA] = rankA + 1
        }
    }

    /// Check if elements are in same set
    public func isConnected(_ a: T, _ b: T) -> Bool {
        find(a) == find(b)
    }

    /// Get number of disjoint sets
    public var setCount: Int {
        Set(parent.keys.map { find($0) }).count
    }
}

// MARK: - Segment Tree

/// Segment tree for range queries
public class SegmentTree {
    private var tree: [Int]
    private var n: Int

    public init(_ array: [Int]) {
        n = array.count
        tree = Array(repeating: 0, count: 4 * n)
        if n > 0 {
            build(array, 0, 0, n - 1)
        }
    }

    private func build(_ array: [Int], _ node: Int, _ start: Int, _ end: Int) {
        if start == end {
            tree[node] = array[start]
        } else {
            let mid = (start + end) / 2
            let leftChild = 2 * node + 1
            let rightChild = 2 * node + 2

            build(array, leftChild, start, mid)
            build(array, rightChild, mid + 1, end)

            tree[node] = tree[leftChild] + tree[rightChild]
        }
    }

    /// Query sum in range [l, r]
    public func query(_ l: Int, _ r: Int) -> Int {
        guard n > 0 else { return 0 }
        return query(0, 0, n - 1, l, r)
    }

    private func query(_ node: Int, _ start: Int, _ end: Int, _ l: Int, _ r: Int) -> Int {
        if r < start || end < l {
            return 0
        }

        if l <= start && end <= r {
            return tree[node]
        }

        let mid = (start + end) / 2
        let leftChild = 2 * node + 1
        let rightChild = 2 * node + 2

        let leftSum = query(leftChild, start, mid, l, r)
        let rightSum = query(rightChild, mid + 1, end, l, r)

        return leftSum + rightSum
    }

    /// Update value at index
    public func update(_ index: Int, _ value: Int) {
        guard n > 0 else { return }
        update(0, 0, n - 1, index, value)
    }

    private func update(_ node: Int, _ start: Int, _ end: Int, _ index: Int, _ value: Int) {
        if start == end {
            tree[node] = value
        } else {
            let mid = (start + end) / 2
            let leftChild = 2 * node + 1
            let rightChild = 2 * node + 2

            if index <= mid {
                update(leftChild, start, mid, index, value)
            } else {
                update(rightChild, mid + 1, end, index, value)
            }

            tree[node] = tree[leftChild] + tree[rightChild]
        }
    }
}