# Swift Algorithm Implementation

A comprehensive, high-performance implementation of fundamental algorithms and data structures in Swift with iOS optimizations.

## 🚀 Features

- ✅ **Swift 5.9+** - Modern Swift features
- ✅ **iOS Optimized** - Grand Central Dispatch & async/await
- ✅ **Protocol-Oriented** - Swift's powerful protocol system
- ✅ **Performance Focus** - Cache-aware implementations
- ✅ **Type Safe** - Generic implementations with type constraints
- ✅ **Comprehensive Coverage** - 40+ algorithms implemented
- ✅ **Swift Package Manager** - Easy integration

## 📦 Installation

### Swift Package Manager

Add to your `Package.swift`:

```swift
dependencies: [
    .package(url: "https://github.com/algorithms-multiverse/swift.git", from: "1.0.0")
]
```

Or in Xcode:
1. File → Add Package Dependencies
2. Enter the repository URL
3. Click Add Package

## 🎯 Quick Start

```swift
import AlgorithmsMultiverse

// Sorting
var array = [64, 34, 25, 12, 22, 11, 90]
Sorting.quickSort(&array)
print(array) // [11, 12, 22, 25, 34, 64, 90]

// Parallel sorting for large datasets
let largeArray = Array(0..<1000000).shuffled()
let sorted = await Sorting.parallelQuickSort(largeArray)

// Data Structures
let bst = BinarySearchTree<Int>()
[50, 30, 70, 20, 40].forEach { bst.insert($0) }
let inOrder = bst.inOrderTraversal() // [20, 30, 40, 50, 70]

// Graph Algorithms
let graph = Graph<String>()
graph.addEdge(from: "A", to: "B")
graph.addEdge(from: "B", to: "C")
let path = GraphAlgorithms.bfs(graph: graph, start: "A")

// Dynamic Programming
let fib = DynamicProgramming.fibonacci(10) // 55
let lcs = DynamicProgramming.longestCommonSubsequence("ABCDGH", "AEDFHR")
```

## 📚 Modules

### Sorting (`Sorting.swift`)

| Algorithm | Time Complexity | Space | Parallel | In-Place |
|-----------|----------------|-------|----------|----------|
| QuickSort | O(n log n) avg | O(log n) | ✅ | ✅ |
| MergeSort | O(n log n) | O(n) | ❌ | ❌ |
| HeapSort | O(n log n) | O(1) | ❌ | ✅ |
| TimSort | O(n log n) | O(n) | ❌ | ❌ |
| RadixSort | O(nk) | O(n) | ❌ | ❌ |
| CountingSort | O(n + k) | O(k) | ❌ | ❌ |

**Special Features:**
- **Parallel QuickSort** - async/await with TaskGroup
- **QuickSelect** - Find k-th smallest in O(n) average
- **Shuffle** - Fisher-Yates algorithm
- **Performance Benchmarking** - Built-in measurement

**Example:**
```swift
// Parallel sorting with async/await
let sorted = await Sorting.parallelQuickSort(hugeArray)

// Find k-th smallest element
if let kth = Sorting.quickSelect(array, k: 3) {
    print("3rd smallest: \(kth)")
}

// Benchmark performance
let benchmark = SortingBenchmark.measure(array, algorithm: .quickSort)
print("Time: \(benchmark.executionTime)s")
```

### Data Structures (`DataStructures.swift`)

| Structure | Insert | Delete | Search | Special Features |
|-----------|--------|--------|--------|-----------------|
| LinkedList<T> | O(1)* | O(n) | O(n) | Collection conformance |
| Stack<T> | O(1) | O(1) | - | Value type |
| Queue<T> | O(1) | O(1) | - | Circular buffer |
| PriorityQueue<T> | O(log n) | O(log n) | O(1) peek | Min-heap |
| BinarySearchTree<T> | O(log n)* | O(log n)* | O(log n)* | Balance check |
| HashTable<K,V> | O(1)* | O(1)* | O(1)* | Auto-resize |
| Trie | O(m) | O(m) | O(m) | Prefix search |
| Graph<T> | O(1) | O(V) | O(1) | Directed/Undirected |
| DisjointSet<T> | O(α(n)) | - | O(α(n)) | Path compression |
| SegmentTree | O(log n) | O(log n) | O(log n) | Range queries |

*Average case

**Example:**
```swift
// Trie for autocomplete
let trie = Trie()
["program", "programmer", "programming"].forEach { trie.insert($0) }
let suggestions = trie.wordsWithPrefix("prog")

// Graph with custom types
let graph = Graph<String>(isDirected: true)
graph.addEdge(from: "iOS", to: "Swift")
graph.addEdge(from: "Swift", to: "SwiftUI")

// Priority queue with custom comparator
var pq = PriorityQueue<Task> { $0.priority > $1.priority }
pq.enqueue(Task(name: "High", priority: 10))
```

### Graph Algorithms (`GraphAlgorithms.swift`)

**Traversal:**
- BFS (iterative)
- DFS (recursive & iterative)
- Topological Sort (DFS & Kahn's)

**Shortest Path:**
- Dijkstra's Algorithm
- A* Pathfinding
- Bellman-Ford
- Floyd-Warshall

**Minimum Spanning Tree:**
- Kruskal's Algorithm
- Prim's Algorithm

**Advanced:**
- Strongly Connected Components (Kosaraju)
- Cycle Detection (directed & undirected)
- Bipartite Check
- Parallel BFS (async/await)

**Example:**
```swift
// Dijkstra with weighted graph
let weighted = WeightedGraph<String>()
weighted.addEdge(from: "A", to: "B", weight: 4.0)
weighted.addEdge(from: "B", to: "C", weight: 2.0)
let distances = GraphAlgorithms.dijkstra(graph: weighted, start: "A")

// A* pathfinding
let path = GraphAlgorithms.aStar(
    graph: weighted,
    start: startNode,
    goal: goalNode,
    heuristic: { (a, b) in euclideanDistance(a, b) }
)

// Parallel BFS
let visited = await GraphAlgorithms.parallelBFS(graph: graph, start: "A")
```

### Dynamic Programming (`DynamicProgramming.swift`)

**Classic Problems:**
- Fibonacci (memoized, iterative, sequence)
- Longest Common Subsequence
- Longest Increasing Subsequence
- Edit Distance (Levenshtein)
- Maximum Subarray (Kadane's)

**Optimization:**
- 0/1 Knapsack
- Unbounded Knapsack
- Coin Change (min coins & ways)
- Matrix Chain Multiplication
- House Robber (linear & circular)

**String Problems:**
- Longest Palindromic Substring
- Longest Palindromic Subsequence
- Word Break

**Stock Trading:**
- Single Transaction
- Multiple Transactions
- K Transactions

**Example:**
```swift
// Knapsack with item tracking
let (maxValue, items) = DynamicProgramming.knapsack01(
    weights: [1, 3, 4, 5],
    values: [1, 4, 5, 7],
    capacity: 7
)

// Edit distance with operations
let (distance, ops) = DynamicProgramming.editDistance("kitten", "sitting")
print("Distance: \(distance)")
ops.forEach { print($0) }

// Word break with all solutions
let solutions = DynamicProgramming.wordBreakAll(
    "catsanddog",
    Set(["cat", "cats", "and", "sand", "dog"])
)
// ["cats and dog", "cat sand dog"]
```

## 🔧 Advanced Features

### iOS & macOS Optimizations

The library is optimized for Apple platforms:

```swift
// Grand Central Dispatch integration
@available(iOS 13.0, macOS 10.15, *)
let sorted = await Sorting.parallelQuickSort(array)

// Structured concurrency with TaskGroup
let result = await withTaskGroup(of: [T].self) { group in
    // Parallel processing
}
```

### Protocol-Oriented Design

```swift
// Sortable collections
protocol SortableCollection {
    associatedtype Element: Comparable
    func sorted(by algorithm: SortingAlgorithm) -> [Element]
}

// Generic constraints
func process<T: Comparable>(_ items: [T]) -> [T]
```

### Collection Extensions

```swift
// Array extensions
let sorted = array.sorted(using: .timSort)
let isSorted = array.isSorted
let kth = array.kthSmallest(3)

// Custom shuffle
var deck = Array(1...52)
deck.shuffle()
```

## 🧪 Testing

Run tests:
```bash
swift test
```

Run specific test:
```bash
swift test --filter SortingTests
```

## 📊 Performance

All implementations are optimized for performance:
- Cache-friendly data structures
- Minimal allocations
- Copy-on-write optimizations
- Parallel algorithms for large datasets

### Benchmarking

```swift
let benchmark = SortingBenchmark.measure(array, algorithm: .quickSort)
print("""
    Algorithm: \(benchmark.algorithm)
    Elements: \(benchmark.elementCount)
    Time: \(benchmark.executionTime)s
    Sorted: \(benchmark.isSorted)
""")
```

## 🔍 Complexity Reference

| Algorithm | Time | Space | Notes |
|-----------|------|-------|-------|
| QuickSort | O(n log n) avg | O(log n) | In-place |
| MergeSort | O(n log n) | O(n) | Stable |
| Dijkstra | O((V+E) log V) | O(V) | Binary heap |
| BFS/DFS | O(V+E) | O(V) | Graph traversal |
| Knapsack | O(nW) | O(W) | Pseudo-polynomial |
| LCS | O(mn) | O(mn) | Can optimize space |

## 📱 Platform Support

- iOS 15.0+
- macOS 12.0+
- watchOS 8.0+
- tvOS 15.0+
- Swift 5.9+

## 📄 License

MIT © Algorithms Multiverse

## 🔗 Links

- [GitHub Repository](https://github.com/algorithms-multiverse/swift)
- [Documentation](https://algorithms-multiverse.github.io/swift)
- [Swift Package Index](https://swiftpackageindex.com/algorithms-multiverse/swift)