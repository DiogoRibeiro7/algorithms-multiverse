# Ruby Algorithm Implementation

A comprehensive, idiomatic Ruby implementation of fundamental algorithms and data structures.

## 🚀 Features

- ✅ **Ruby 2.7+** - Modern Ruby features
- ✅ **Idiomatic Ruby** - Following Ruby best practices
- ✅ **Thread-Safe** - Parallel algorithms with proper synchronization
- ✅ **Refinements** - Optional Array/Hash extensions
- ✅ **Performance Optimized** - Efficient implementations
- ✅ **Full Documentation** - YARD documentation
- ✅ **RubyGems Ready** - Easy installation
- ✅ **93+ Algorithms** - Across 6 comprehensive modules
- ✅ **Complete Implementation** - All modules fully functional

## 📦 Installation

Add to your Gemfile:

```ruby
gem 'algorithms_multiverse'
```

Or install directly:

```bash
gem install algorithms_multiverse
```

## 🎯 Quick Start

```ruby
require 'algorithms_multiverse'

# Sorting
array = [64, 34, 25, 12, 22, 11, 90]
sorted = AlgorithmsMultiverse::Sorting.quick_sort(array.dup)
puts sorted.inspect # [11, 12, 22, 25, 34, 64, 90]

# Using refinements for cleaner syntax
using AlgorithmsMultiverse::ArrayExtensions
array.quick_sort!  # In-place sorting
sorted = array.merge_sorted  # Functional style

# Data Structures
bst = AlgorithmsMultiverse::DataStructures::BinarySearchTree.new
[50, 30, 70, 20, 40].each { |val| bst.insert(val) }
puts bst.inorder # [20, 30, 40, 50, 70]

# Graph Algorithms
graph = AlgorithmsMultiverse::GraphAlgorithms::Graph.new
graph.add_edge("A", "B", 4)
path = AlgorithmsMultiverse::GraphAlgorithms::BFS.shortest_path(graph, "A", "B")

# Dynamic Programming
fib = AlgorithmsMultiverse::DynamicProgramming.fibonacci(10) # 55
lcs = AlgorithmsMultiverse::DynamicProgramming.lcs("ABCDGH", "AEDFHR")
```

## 📚 Modules

### 1️⃣ Sorting (`sorting.rb`) - 15 algorithms

| Algorithm | Time Complexity | Space | Stable | In-Place |
|-----------|----------------|-------|--------|----------|
| QuickSort | O(n log n) avg | O(log n) | ❌ | ✅ |
| MergeSort | O(n log n) | O(n) | ✅ | ❌ |
| HeapSort | O(n log n) | O(1) | ❌ | ✅ |
| TimSort | O(n log n) | O(n) | ✅ | ❌ |
| RadixSort | O(nk) | O(n) | ✅ | ❌ |
| CountingSort | O(n + k) | O(k) | ✅ | ❌ |
| BucketSort | O(n + k) | O(n) | ✅ | ❌ |
| InsertionSort | O(n²) | O(1) | ✅ | ✅ |
| SelectionSort | O(n²) | O(1) | ❌ | ✅ |
| BubbleSort | O(n²) | O(1) | ✅ | ✅ |
| ShellSort | O(n log²n) | O(1) | ❌ | ✅ |

**Special Features:**
- **Parallel QuickSort** - Thread-based parallel processing
- **QuickSelect** - Find k-th smallest in O(n) average
- **Functional variants** - Non-mutating versions
- **Benchmarking** - Built-in performance measurement

### 2️⃣ Searching (`searching.rb`) - 17 algorithms

**Binary Search Variants:**
- Binary Search (iterative/recursive)
- First/Last occurrence
- Count occurrences
- Search insert position

**Advanced Search:**
- Jump Search - O(√n)
- Interpolation Search - O(log log n) average
- Exponential Search - For unbounded arrays
- Ternary Search - Three-way split
- Fibonacci Search - Using Fibonacci numbers

**Special Cases:**
- Search in rotated array
- Find peak element
- Find minimum in rotated array
- Search in 2D matrix
- Find median of two sorted arrays

### 3️⃣ Data Structures (`data_structures.rb`) - 13 structures

**Linear Structures:**
- Stack - LIFO with array backing
- Queue - FIFO with array backing
- Deque - Double-ended queue
- LinkedList - Singly linked with full operations
- DoublyLinkedList - Bidirectional traversal

**Tree Structures:**
- BinarySearchTree - With all traversals
- MinHeap - Priority queue operations
- MaxHeap - Maximum priority
- Trie - Prefix tree with autocomplete

**Advanced Structures:**
- HashTable - Chaining collision resolution
- DisjointSet - Union-Find with path compression
- PriorityQueue - Custom comparator support

### 4️⃣ Graph Algorithms (`graph_algorithms.rb`) - 12 algorithms

**Graph Representation:**
- Adjacency list based
- Weighted/unweighted
- Directed/undirected

**Algorithms:**
- DFS - With cycle detection
- BFS - With shortest path
- Dijkstra's - Single source shortest path
- Bellman-Ford - Negative weight handling
- Floyd-Warshall - All pairs shortest paths
- Kruskal's MST - Using disjoint sets
- Prim's MST - Using priority queue
- Topological Sort - Two implementations
- Strongly Connected Components - Kosaraju's and Tarjan's
- Bipartite Check

### 5️⃣ Dynamic Programming (`dynamic_programming.rb`) - 20 problems

**Classic Problems:**
- Fibonacci (memoization/tabulation)
- Longest Common Subsequence
- Longest Increasing Subsequence
- Edit Distance (Levenshtein)

**Optimization Problems:**
- 0/1 Knapsack
- Coin Change (min coins and ways)
- Rod Cutting
- Matrix Chain Multiplication
- Maximum Subarray (Kadane's)

**Partition & Sum:**
- Subset Sum
- Partition Equal Sum
- House Robber

**Advanced:**
- Word Break
- Egg Drop Problem
- Palindrome Partitioning
- Longest Palindromic Subsequence

### 6️⃣ String Algorithms (`string_algorithms.rb`) - 16 algorithms

**Pattern Matching:**
- KMP (Knuth-Morris-Pratt)
- Rabin-Karp (Rolling Hash)
- Boyer-Moore
- Z-Algorithm

**Palindromes:**
- Longest Palindromic Substring
- Manacher's Algorithm

**Advanced Matching:**
- Wildcard Matching (* and ?)
- Regular Expression (. and *)
- Minimum Window Substring

**String Operations:**
- Anagram Detection
- Find All Anagrams
- String Compression/Decompression
- String Rotation Check
- Longest Common Prefix

## 🔧 Advanced Features

### Using Refinements

Refinements provide cleaner syntax without polluting global namespace:

```ruby
using AlgorithmsMultiverse::ArrayExtensions

# Now arrays have additional methods
array.quick_sorted     # Returns sorted copy
array.quick_sort!      # Sorts in place
array.kth_smallest(3)  # Find 3rd smallest
array.sorted?          # Check if sorted
```

### Parallel Processing

Leverage multiple CPU cores for better performance:

```ruby
# Automatic thread pooling for large arrays
sorted = AlgorithmsMultiverse::Sorting.parallel_quick_sort(large_array)

# Configure thread threshold
sorted = AlgorithmsMultiverse::Sorting.parallel_quick_sort(
  array,
  threshold: 5000  # Use threads for arrays > 5000 elements
)
```

### Example Usage - Complete Workflow

```ruby
require 'algorithms_multiverse'

# Problem: Find shortest path in a network
graph = AlgorithmsMultiverse::GraphAlgorithms::Graph.new(directed: false)

# Add cities and distances
cities = [
  ["NYC", "Boston", 215],
  ["NYC", "Philadelphia", 95],
  ["Boston", "Philadelphia", 300],
  ["Philadelphia", "Washington", 140]
]

cities.each { |from, to, distance| graph.add_edge(from, to, distance) }

# Find shortest path
result = AlgorithmsMultiverse::GraphAlgorithms::Dijkstra.shortest_path(graph, "NYC", "Washington")
puts "Path: #{result[:path].join(' -> ')}"
puts "Distance: #{result[:distance]} miles"

# Problem: Text pattern matching
text = "The quick brown fox jumps over the lazy dog"
pattern = "fox"

# Find all occurrences using KMP
matches = AlgorithmsMultiverse::StringAlgorithms.kmp_search(text, pattern)
puts "Pattern found at positions: #{matches}"

# Problem: Resource allocation (Knapsack)
items = {
  weights: [10, 20, 30],
  values: [60, 100, 120]
}
capacity = 50

result = AlgorithmsMultiverse::DynamicProgramming.knapsack(
  items[:weights],
  items[:values],
  capacity
)
puts "Maximum value: #{result[:max_value]}"
puts "Items to take: #{result[:items].map { |i| "Item #{i + 1}" }}"
```

## 🧪 Testing

Run tests:
```bash
bundle exec rspec
```

Run with coverage:
```bash
COVERAGE=true bundle exec rspec
```

## 📊 Performance

All implementations are optimized for Ruby:
- Minimize object allocations
- Use built-in methods where faster
- Parallel processing for large datasets
- Careful algorithm selection

### Benchmarking

```ruby
require 'benchmark'

arrays = {
  small: (1..100).to_a.shuffle,
  medium: (1..10_000).to_a.shuffle,
  large: (1..100_000).to_a.shuffle
}

Benchmark.bm(15) do |x|
  arrays.each do |size, array|
    x.report("#{size} quick:") do
      AlgorithmsMultiverse::Sorting.quick_sort(array.dup)
    end

    x.report("#{size} merge:") do
      AlgorithmsMultiverse::Sorting.merge_sort(array.dup)
    end
  end
end
```

## 🔍 Complexity Reference

| Category | Algorithm | Time | Space | Notes |
|----------|-----------|------|-------|-------|
| **Sorting** |
| | QuickSort | O(n log n) avg | O(log n) | In-place, not stable |
| | MergeSort | O(n log n) | O(n) | Stable, good for linked lists |
| | HeapSort | O(n log n) | O(1) | In-place, not stable |
| | TimSort | O(n log n) | O(n) | Hybrid stable sort |
| **Searching** |
| | Binary Search | O(log n) | O(1) | Requires sorted array |
| | Interpolation | O(log log n) avg | O(1) | For uniform distribution |
| | Jump Search | O(√n) | O(1) | Block jumping approach |
| **Graph** |
| | DFS/BFS | O(V + E) | O(V) | Linear traversal |
| | Dijkstra | O(E log V) | O(V) | With priority queue |
| | Floyd-Warshall | O(V³) | O(V²) | All pairs shortest paths |
| **Dynamic Programming** |
| | LCS | O(mn) | O(mn) | Can be optimized to O(min(m,n)) |
| | Knapsack | O(nW) | O(nW) | Pseudo-polynomial |
| | Edit Distance | O(mn) | O(mn) | Levenshtein distance |
| **String** |
| | KMP | O(n + m) | O(m) | Linear pattern matching |
| | Rabin-Karp | O(n + m) avg | O(1) | Rolling hash |
| | Manacher | O(n) | O(n) | All palindromes |

## 🔧 Development

After checking out the repo:

```bash
bundle install           # Install dependencies
bundle exec rspec       # Run tests
bundle exec rubocop     # Check style
bundle exec yard doc    # Generate documentation
```

## 📈 Project Statistics

- **Total Algorithms**: 93+
- **Modules**: 6
- **Data Structures**: 13
- **Lines of Code**: ~5,000+
- **Test Coverage**: Target 90%+

## 📄 License

MIT © Algorithms Multiverse

## 🔗 Links

- [Main Repository](https://github.com/diogoribeiro7/algorithms-multiverse)
- [RubyGems](https://rubygems.org/gems/algorithms_multiverse)
- [Documentation](https://rubydoc.info/gems/algorithms_multiverse)