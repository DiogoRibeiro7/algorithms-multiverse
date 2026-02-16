# Swift Algorithm Implementation

A comprehensive, high-performance implementation of fundamental algorithms and data structures in Swift with iOS optimizations.

## 🚀 Features

- ✅ **Swift 5.9+** - Modern Swift features
- ✅ **iOS Optimized** - Grand Central Dispatch & async/await
- ✅ **Protocol-Oriented** - Swift's powerful protocol system
- ✅ **Performance Focus** - Cache-aware implementations
- ✅ **Type Safe** - Generic implementations with type constraints
- ✅ **Comprehensive Coverage** - 150+ algorithms implemented
- ✅ **Swift Package Manager** - Easy integration

## 📊 Statistics

- **Modules**: 8 comprehensive modules
- **Algorithms**: 150+ implementations
- **Data Structures**: 15+ fundamental structures
- **Categories**: Sorting, Searching, Graphs, Dynamic Programming, Strings, Numerical, Advanced
- **Lines of Code**: ~7,000+
- **iOS Features**: Async/await, GCD, Accelerate framework

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

// Searching
if let index = Searching.binarySearch([1, 3, 5, 7, 9], target: 5) {
    print("Found at index: \(index)")
}

// String Algorithms
let pattern = "ABABCABAB"
let text = "ABABDABACDABABCABAB"
let matches = StringAlgorithms.kmpSearch(text, pattern: pattern)
print("Pattern found at indices: \(matches)")

// Numerical Algorithms
let gcd = NumericalAlgorithms.gcd(48, 18)  // 6
let primes = NumericalAlgorithms.sieveOfEratosthenes(100)

// Data Structures
let bst = BinarySearchTree<Int>()
[50, 30, 70, 20, 40].forEach { bst.insert($0) }

// Graph Algorithms
let graph = Graph<String>()
graph.addEdge(from: "A", to: "B")
let path = GraphAlgorithms.bfs(graph: graph, start: "A")

// Dynamic Programming
let fib = DynamicProgramming.fibonacci(10) // 55
let lcs = DynamicProgramming.longestCommonSubsequence("ABCDGH", "AEDFHR")

// Advanced Algorithms
let (encoded, tree) = AdvancedAlgorithms.HuffmanCoding.encode("hello world")
let points = [Point2D(0, 0), Point2D(1, 1), Point2D(2, 0)]
let hull = AdvancedAlgorithms.convexHull(points)
```

## 📚 Modules

### 1. Sorting (`Sorting.swift`)

**15+ Sorting Algorithms** with performance optimizations:

| Algorithm | Time Complexity | Space | Parallel | In-Place |
|-----------|----------------|-------|----------|----------|
| QuickSort | O(n log n) avg | O(log n) | ✅ | ✅ |
| MergeSort | O(n log n) | O(n) | ❌ | ❌ |
| HeapSort | O(n log n) | O(1) | ❌ | ✅ |
| TimSort | O(n log n) | O(n) | ❌ | ❌ |
| IntroSort | O(n log n) | O(log n) | ❌ | ✅ |
| RadixSort | O(nk) | O(n) | ❌ | ❌ |
| CountingSort | O(n + k) | O(k) | ❌ | ❌ |
| ShellSort | O(n^1.3) | O(1) | ❌ | ✅ |

**Special Features:**
- **Parallel QuickSort** - async/await with TaskGroup
- **QuickSelect** - Find k-th smallest in O(n) average
- **Performance Benchmarking** - Built-in measurement

### 2. Searching (`Searching.swift`)

**20+ Search Algorithms** for various use cases:

**Binary Search Variants:**
- Standard binary search
- Lower bound (first occurrence)
- Upper bound (last position)
- Count occurrences
- Search in rotated array

**Advanced Search:**
- Jump search - O(√n)
- Interpolation search - O(log log n) average
- Exponential search - For unbounded arrays
- Ternary search - Three-way split
- Fibonacci search - Using Fibonacci numbers

**Specialized Algorithms:**
- Two-pointer technique
- Three-sum problem
- Peak finding
- Quick select (k-th element)
- Parallel search with GCD

### 3. Data Structures (`DataStructures.swift`)

**15+ Essential Data Structures:**

| Structure | Insert | Delete | Search | Special Features |
|-----------|--------|--------|--------|-----------------|
| LinkedList<T> | O(1)* | O(n) | O(n) | Collection conformance |
| Stack<T> | O(1) | O(1) | O(n) | LIFO operations |
| Queue<T> | O(1) | O(1) | O(n) | FIFO operations |
| PriorityQueue<T> | O(log n) | O(log n) | O(n) | Min/Max heap-based |
| BinarySearchTree<T> | O(log n)* | O(log n)* | O(log n)* | In-order traversal |
| HashTable<K, V> | O(1)* | O(1)* | O(1)* | Chaining for collisions |
| Trie | O(m) | O(m) | O(m) | Prefix operations |
| SegmentTree<T> | O(n) build | O(log n) | O(log n) | Range queries |
| DisjointSet | O(α(n)) | - | O(α(n)) | Union-find operations |
| Graph<T> | O(1) | O(E) | O(V+E) | Adjacency list |

*Average case

### 4. Graph Algorithms (`GraphAlgorithms.swift`)

**15+ Graph Algorithms** for networks and pathfinding:

**Traversal:**
- BFS (Breadth-First Search)
- DFS (Depth-First Search)
- Bidirectional Search

**Shortest Path:**
- Dijkstra's algorithm
- A* pathfinding
- Bellman-Ford (negative weights)
- Floyd-Warshall (all pairs)

**Minimum Spanning Tree:**
- Kruskal's algorithm
- Prim's algorithm

**Advanced:**
- Topological Sort (DAG)
- Kosaraju's algorithm (SCC)
- Tarjan's algorithm (SCC)
- Cycle detection
- Bipartite checking

### 5. Dynamic Programming (`DynamicProgramming.swift`)

**20+ Classic DP Problems** with optimal solutions:

**Sequences:**
- Fibonacci (iterative & matrix)
- Longest Common Subsequence (LCS)
- Longest Increasing Subsequence (LIS)
- Maximum subarray (Kadane's)

**String Problems:**
- Edit distance (Levenshtein)
- Longest palindrome
- Word break
- Pattern matching

**Optimization:**
- 0/1 Knapsack
- Unbounded knapsack
- Coin change (minimum coins)
- Coin change (ways to make change)
- Rod cutting

**Advanced:**
- Matrix chain multiplication
- Egg dropping problem
- House robber
- Stock trading with cooldown

### 6. String Algorithms (`StringAlgorithms.swift`)

**15+ String Processing Algorithms:**

**Pattern Matching:**
- KMP (Knuth-Morris-Pratt) - O(n+m)
- Rabin-Karp (rolling hash) - O(n+m) average
- Boyer-Moore - O(nm) worst, O(n/m) best
- Z-Algorithm - O(n)

**Palindromes:**
- Palindrome check - O(n)
- Longest palindromic substring (Manacher's) - O(n)
- All palindromes - O(n²)

**String Operations:**
- Longest common prefix
- Longest common substring
- Anagram checking
- Find all anagrams
- Minimum window substring

**String Metrics:**
- Edit distance (Levenshtein)
- Hamming distance

**Compression:**
- Run-length encoding/decoding

**Advanced:**
- Suffix array construction - O(n log n)

### 7. Numerical Algorithms (`NumericalAlgorithms.swift`)

**30+ Mathematical Algorithms:**

**Number Theory:**
- GCD (Euclidean algorithm)
- Extended GCD
- LCM
- Prime checking (trial division & Miller-Rabin)
- Sieve of Eratosthenes
- Prime factorization
- Euler's totient function

**Modular Arithmetic:**
- Modular exponentiation
- Modular inverse
- Chinese Remainder Theorem

**Combinatorics:**
- Factorial
- Binomial coefficients (nCr)
- Pascal's triangle
- Catalan numbers

**Sequences:**
- Fibonacci (iterative & matrix)

**Numerical Methods:**
- Newton-Raphson (root finding)
- Bisection method
- Simpson's rule (integration)
- Trapezoidal rule (integration)
- Numerical derivative

**Linear Algebra:**
- Gaussian elimination
- LU decomposition
- Matrix multiplication
- Matrix exponentiation

**Signal Processing:**
- Fast Fourier Transform (FFT)

### 8. Advanced Algorithms (`AdvancedAlgorithms.swift`)

**20+ Specialized Algorithms:**

**Compression:**
- Huffman coding
- LZW compression

**Cryptography (Educational):**
- Caesar cipher
- Vigenère cipher
- XOR cipher

**Computational Geometry:**
- Convex hull (Graham scan)
- Closest pair of points
- Line segment intersection
- Collinearity check

**Probabilistic Data Structures:**
- Bloom filter
- Skip list
- Reservoir sampling

## 🎯 iOS-Specific Optimizations

### Parallel Processing

```swift
// Parallel sorting with async/await
let sorted = await Sorting.parallelQuickSort(hugeArray)

// Parallel search across multiple cores
let indices = await Searching.parallelSearch(largeArray, target: value)
```

### Performance Measurement

```swift
let benchmark = SortingBenchmark.measure(array, algorithm: .quickSort)
print("Execution time: \(benchmark.executionTime)s")
print("Memory used: \(benchmark.memoryUsage) bytes")
```

### Cache-Aware Implementations

- Optimized for Apple Silicon cache hierarchy
- Data locality improvements in sorting algorithms
- Memory-efficient data structures

## 🧪 Testing

```swift
// Run all tests
swift test

// Run specific test suite
swift test --filter SortingTests

// Performance tests
swift test --filter PerformanceTests
```

## 📖 Algorithm Complexity Reference

| Category | Algorithm | Time (Avg) | Time (Worst) | Space |
|----------|-----------|------------|--------------|-------|
| **Sorting** | Quick Sort | O(n log n) | O(n²) | O(log n) |
| | Merge Sort | O(n log n) | O(n log n) | O(n) |
| | Tim Sort | O(n log n) | O(n log n) | O(n) |
| **Searching** | Binary Search | O(log n) | O(log n) | O(1) |
| | Interpolation | O(log log n) | O(n) | O(1) |
| | Jump Search | O(√n) | O(√n) | O(1) |
| **Graph** | DFS/BFS | O(V+E) | O(V+E) | O(V) |
| | Dijkstra | O(E log V) | O(E log V) | O(V) |
| | A* | O(E) | O(V²) | O(V) |
| **DP** | LCS | O(mn) | O(mn) | O(mn) |
| | Knapsack | O(nW) | O(nW) | O(nW) |
| | Edit Distance | O(mn) | O(mn) | O(mn) |
| **String** | KMP | O(n+m) | O(n+m) | O(m) |
| | Rabin-Karp | O(n+m) | O(nm) | O(1) |
| | Manacher | O(n) | O(n) | O(n) |
| **Numerical** | FFT | O(n log n) | O(n log n) | O(n) |
| | Sieve | O(n log log n) | O(n log log n) | O(n) |
| | GCD | O(log min(a,b)) | O(log min(a,b)) | O(1) |

## 🎨 Protocol-Oriented Design

The library makes extensive use of Swift protocols:

```swift
// Custom types can work with algorithms
struct Person: Comparable {
    let name: String
    let age: Int

    static func < (lhs: Person, rhs: Person) -> Bool {
        return lhs.age < rhs.age
    }
}

let people = [Person(name: "Alice", age: 30), Person(name: "Bob", age: 25)]
let sorted = Sorting.quickSort(people)
```

## 🔧 Customization

### Custom Comparators

```swift
// Sort with custom comparison
let sorted = array.sorted { abs($0) < abs($1) }

// Binary search with custom comparator
let index = Searching.binarySearch(array, target: value) { a, b in
    a.property.compare(b.property)
}
```

### Algorithm Selection

```swift
// Choose algorithm based on data characteristics
let algorithm: SortingAlgorithm = array.count < 50 ? .insertionSort : .quickSort
let sorted = Sorting.sort(array, using: algorithm)
```

## 🚀 Performance Tips

1. **Use in-place algorithms** when possible to reduce memory allocation
2. **Leverage parallel algorithms** for large datasets (>10,000 elements)
3. **Choose appropriate data structures** - Hash tables for lookups, trees for ordered data
4. **Profile with Instruments** to identify bottlenecks
5. **Use value types** (structs) for better cache locality
6. **Avoid unnecessary copies** - use `inout` parameters

## 📱 iOS App Integration

```swift
import AlgorithmsMultiverse
import UIKit

class DataProcessor {
    // Process large datasets efficiently
    func processData(_ data: [Int]) async -> ProcessedResult {
        // Sort data in parallel
        let sorted = await Sorting.parallelQuickSort(data)

        // Find patterns
        let patterns = StringAlgorithms.findPatterns(in: sorted)

        // Optimize with dynamic programming
        let optimized = DynamicProgramming.optimize(patterns)

        return ProcessedResult(optimized)
    }
}
```

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows Swift API Design Guidelines
- Comprehensive unit tests included
- Performance benchmarks for new algorithms
- Documentation with complexity analysis

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Based on classical algorithms from CLRS
- Optimized for Apple platforms
- Part of the Algorithms Multiverse project

---

*High-performance Swift implementations for iOS, macOS, and beyond.*