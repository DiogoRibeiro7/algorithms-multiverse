# C# Algorithm Implementation

A comprehensive, high-performance implementation of fundamental algorithms and data structures in C# with LINQ optimizations.

## 🚀 Features

- ✅ **Modern C# 12 / .NET 8** - Latest language features
- ✅ **LINQ Optimized** - Elegant functional programming approaches
- ✅ **Parallel Algorithms** - Multi-core CPU utilization
- ✅ **Generic Implementations** - Type-safe and reusable
- ✅ **Comprehensive Coverage** - 40+ algorithms implemented
- ✅ **NuGet Package Ready** - Easy integration
- ✅ **Full XML Documentation** - IntelliSense support

## 📦 Installation

### NuGet Package Manager
```bash
Install-Package AlgorithmsMultiverse.CSharp
```

### .NET CLI
```bash
dotnet add package AlgorithmsMultiverse.CSharp
```

### PackageReference
```xml
<PackageReference Include="AlgorithmsMultiverse.CSharp" Version="1.0.0" />
```

## 🎯 Quick Start

```csharp
using AlgorithmsMultiverse.CSharp;

// Sorting
var array = new[] { 64, 34, 25, 12, 22, 11, 90 };
SortingAlgorithms.QuickSort(array);
Console.WriteLine(string.Join(", ", array)); // 11, 12, 22, 25, 34, 64, 90

// LINQ-style sorting
var sorted = array.QuickSorted(); // Extension method
var multiKey = data.OrderByStable(x => x.Name).ThenBy(x => x.Age);

// Data Structures
var bst = new BinarySearchTree<int>();
foreach (var value in new[] { 50, 30, 70, 20, 40 })
    bst.Insert(value);
var inOrder = bst.InOrderTraversal(); // 20, 30, 40, 50, 70

// Graph Algorithms
var graph = new Graph<string>();
graph.AddEdge("A", "B");
graph.AddEdge("B", "C");
var path = GraphAlgorithms.BFS(graph, "A").ToList();

// Dynamic Programming
var fib = DynamicProgramming.Fibonacci(10);
var lcs = DynamicProgramming.LongestCommonSubsequence("ABCDGH", "AEDFHR");
```

## 📚 Modules

### Sorting Algorithms (`SortingAlgorithms.cs`)

| Algorithm | Time Complexity | Space | Parallel | LINQ |
|-----------|----------------|-------|----------|------|
| QuickSort | O(n log n) avg | O(log n) | ✅ | ✅ |
| MergeSort | O(n log n) | O(n) | ❌ | ✅ |
| HeapSort | O(n log n) | O(1) | ❌ | ❌ |
| TimSort | O(n log n) | O(n) | ❌ | ✅ |
| CountingSort | O(n + k) | O(k) | ❌ | ❌ |
| RadixSort | O(nk) | O(n) | ❌ | ❌ |
| BucketSort | O(n + k) | O(n) | ❌ | ✅ |

**Special Features:**
- **Parallel QuickSort** - Automatically uses multiple cores
- **LINQ Integration** - Fluent API with `OrderByStable`, `Partition` methods
- **Extension Methods** - `QuickSorted()`, `MergeSorted()` for chaining
- **Performance Benchmarking** - Built-in timing utilities

**Example:**
```csharp
// Parallel sorting for large datasets
var largeArray = Enumerable.Range(0, 1000000).Reverse().ToArray();
SortingAlgorithms.ParallelQuickSort(largeArray);

// LINQ-style multi-key sorting
var people = GetPeople();
var sorted = SortingAlgorithms.MultiKeySort(people,
    p => p.LastName,
    p => p.FirstName);

// Benchmark performance
var benchmark = SortingAlgorithms.BenchmarkSort(testArray,
    arr => SortingAlgorithms.QuickSort(arr));
Console.WriteLine(benchmark);
```

### Data Structures (`DataStructures.cs`)

| Structure | Insert | Delete | Search | Special Features |
|-----------|--------|--------|--------|-----------------|
| LinkedList<T> | O(1)* | O(n) | O(n) | Doubly linked, IEnumerable |
| Stack<T> | O(1) | O(1) | - | Dynamic resizing, TryPop |
| Queue<T> | O(1) | O(1) | - | Circular buffer, TryDequeue |
| PriorityQueue<T> | O(log n) | O(log n) | O(1) peek | Min-heap based |
| BinarySearchTree<T> | O(log n)* | O(log n)* | O(log n)* | All traversals, balance check |
| HashTable<K,V> | O(1)* | O(1)* | O(1)* | Separate chaining, auto-resize |
| Trie | O(m) | O(m) | O(m) | Prefix search, word suggestions |
| Graph<T> | O(1) | O(V) | O(1) | Adjacency list, directed/undirected |

*Average case

**Example:**
```csharp
// Trie for autocomplete
var trie = new Trie();
foreach (var word in dictionary)
    trie.Insert(word);

var suggestions = trie.GetWordsWithPrefix("prog");
// ["program", "programmer", "programming", "progress"]

// Graph with LINQ
var graph = new Graph<int>();
var maxDegreeVertex = graph.GetMaxDegreeVertex(); // Extension method
var components = graph.GetConnectedComponents();
```

### Graph Algorithms (`GraphAlgorithms.cs`)

**Traversal Algorithms:**
- BFS, DFS (iterative & recursive)
- Topological Sort
- Connected Components

**Shortest Path:**
- Dijkstra's Algorithm
- Bellman-Ford (negative weights)
- Floyd-Warshall (all pairs)
- A* Pathfinding

**Minimum Spanning Tree:**
- Kruskal's Algorithm
- Prim's Algorithm

**Advanced:**
- Strongly Connected Components (Kosaraju)
- Cycle Detection
- Bipartite Check
- All Paths Between Vertices

**Parallel Algorithms:**
- Parallel BFS
- Parallel Dijkstra from all vertices

**Example:**
```csharp
// Dijkstra with custom graph
var weightedGraph = new Dictionary<string, List<(string, double)>>
{
    ["A"] = new() { ("B", 4), ("C", 2) },
    ["B"] = new() { ("C", 1), ("D", 5) },
    ["C"] = new() { ("D", 8), ("E", 10) },
    ["D"] = new() { ("E", 2) },
    ["E"] = new()
};

var distances = GraphAlgorithms.Dijkstra(weightedGraph, "A");
foreach (var (vertex, (distance, previous)) in distances)
    Console.WriteLine($"{vertex}: {distance} via {previous}");

// A* pathfinding
var path = GraphAlgorithms.AStar(
    graph,
    start,
    goal,
    (a, b) => ManhattanDistance(a, b) // heuristic
);

// Parallel graph processing
var parallelBFS = await GraphAlgorithms.ParallelBFS(graph, start);
```

### Dynamic Programming (`DynamicProgramming.cs`)

**Classic Problems:**
- Fibonacci (memoized, iterative, sequence generator)
- Longest Common Subsequence (with backtracking)
- Longest Increasing Subsequence (O(n²) and O(n log n))
- Edit Distance (Levenshtein with operations)
- Maximum Subarray (Kadane's algorithm)

**Optimization Problems:**
- 0/1 Knapsack (with item selection)
- Unbounded Knapsack
- Fractional Knapsack
- Coin Change (min coins & ways)
- Matrix Chain Multiplication

**String Problems:**
- Longest Palindromic Substring
- Word Break (with all solutions)

**Advanced Features:**
- LINQ integration for elegant solutions
- Memoization decorator
- Extension methods for common patterns

**Example:**
```csharp
// Knapsack with item tracking
var (maxValue, selectedItems) = DynamicProgramming.Knapsack01(
    weights: new[] { 1, 3, 4, 5 },
    values: new[] { 1, 4, 5, 7 },
    capacity: 7
);
Console.WriteLine($"Max value: {maxValue}, Items: {string.Join(", ", selectedItems)}");

// Generate Fibonacci sequence with LINQ
var first10Fib = DynamicProgramming.FibonacciSequence()
    .Take(10)
    .ToList();

// Get all coin combinations
var combinations = DynamicProgramming.GetCoinCombinations(
    new[] { 1, 2, 5 },
    11
);

// Word break with all solutions
var solutions = DynamicProgramming.WordBreakSolutions(
    "catsanddog",
    new HashSet<string> { "cat", "cats", "and", "sand", "dog" }
);
// ["cats and dog", "cat sand dog"]

// Memoization extension
Func<int, long> fib = null;
fib = n => n <= 1 ? n : fib(n - 1) + fib(n - 2);
var memoizedFib = fib.Memoize();
```

## 🔧 Advanced Features

### LINQ Integration

The library extensively uses LINQ for elegant, functional programming solutions:

```csharp
// Find all paths using LINQ
var allPaths = GraphAlgorithms.FindAllPaths(graph, start, end)
    .Where(path => path.Count <= maxLength)
    .OrderBy(path => path.Count);

// Generate all subsets
var subsets = array.GenerateSubsets()
    .Where(subset => subset.Sum() == target);

// Stable sorting with custom key
var stableSorted = collection
    .OrderByStable(x => x.Priority)
    .ThenBy(x => x.Timestamp);
```

### Parallel Processing

Leverage multi-core CPUs for better performance:

```csharp
// Parallel sorting
SortingAlgorithms.ParallelQuickSort(largeArray);

// Parallel graph traversal
var result = await GraphAlgorithms.ParallelBFS(graph, start);

// Parallel LINQ sorting
var sorted = SortingAlgorithms.ParallelLinqSort(collection);
```

### Extension Methods

Convenient extension methods for common operations:

```csharp
// Array extensions
var sorted = array.QuickSorted();
var isSorted = array.IsSorted();

// Graph extensions
bool hasPath = graph.HasPath(start, end);
var reachable = graph.GetReachableVertices(start);
var matrix = graph.ToAdjacencyMatrix();

// DP extensions
bool canPartition = array.CanPartition();
var memoized = expensiveFunc.Memoize();
```

## 🧪 Testing

Run unit tests:
```bash
dotnet test
```

Run benchmarks:
```bash
dotnet run -c Release --project Benchmarks
```

## 📊 Performance

All implementations are optimized for performance:
- Cache-friendly data structures
- Minimal allocations
- Parallel algorithms for large datasets
- SIMD optimizations where applicable

## 🔍 Complexity Reference

| Algorithm | Time | Space | Notes |
|-----------|------|-------|-------|
| QuickSort | O(n log n) avg | O(log n) | In-place, unstable |
| MergeSort | O(n log n) | O(n) | Stable |
| Dijkstra | O((V+E) log V) | O(V) | With binary heap |
| BFS/DFS | O(V+E) | O(V) | Graph traversal |
| Kruskal | O(E log E) | O(V) | MST |
| LCS | O(mn) | O(mn) | Can optimize to O(min(m,n)) space |
| Knapsack | O(nW) | O(W) | Pseudo-polynomial |

## 📄 License

MIT © Algorithms Multiverse

## 🔗 Links

- [GitHub Repository](https://github.com/algorithms-multiverse/csharp)
- [NuGet Package](https://www.nuget.org/packages/AlgorithmsMultiverse.CSharp)
- [API Documentation](https://algorithms-multiverse.github.io/csharp)