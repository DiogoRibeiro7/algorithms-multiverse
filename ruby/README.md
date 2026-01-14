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

# Parallel sorting for large datasets
huge_array = (1..1_000_000).to_a.shuffle
sorted = AlgorithmsMultiverse::Sorting.parallel_quick_sort(huge_array)

# Data Structures (to be implemented)
bst = AlgorithmsMultiverse::BinarySearchTree.new
[50, 30, 70, 20, 40].each { |val| bst.insert(val) }
puts bst.in_order_traversal # [20, 30, 40, 50, 70]

# Graph Algorithms (to be implemented)
graph = AlgorithmsMultiverse::Graph.new
graph.add_edge("A", "B")
path = AlgorithmsMultiverse::GraphAlgorithms.bfs(graph, "A")

# Dynamic Programming (to be implemented)
fib = AlgorithmsMultiverse::DynamicProgramming.fibonacci(10) # 55
```

## 📚 Modules

### Sorting (`sorting.rb`)

| Algorithm | Time Complexity | Space | Stable | In-Place |
|-----------|----------------|-------|--------|----------|
| QuickSort | O(n log n) avg | O(log n) | ❌ | ✅ |
| MergeSort | O(n log n) | O(n) | ✅ | ❌ |
| HeapSort | O(n log n) | O(1) | ❌ | ✅ |
| TimSort | O(n log n) | O(n) | ✅ | ❌ |
| RadixSort | O(nk) | O(n) | ✅ | ❌ |
| CountingSort | O(n + k) | O(k) | ✅ | ❌ |
| BucketSort | O(n + k) | O(n) | ✅ | ❌ |

**Special Features:**
- **Parallel QuickSort** - Thread-based parallel processing
- **QuickSelect** - Find k-th smallest in O(n) average
- **Functional variants** - Non-mutating versions
- **Benchmarking** - Built-in performance measurement

**Example:**
```ruby
# Functional style (non-mutating)
sorted = AlgorithmsMultiverse::Sorting.quick_sort_functional(array)

# In-place sorting
AlgorithmsMultiverse::Sorting.heap_sort(array)

# Find k-th smallest element
third_smallest = AlgorithmsMultiverse::Sorting.quick_select(array, 2)

# Parallel sorting for large arrays
sorted = AlgorithmsMultiverse::Sorting.parallel_quick_sort(huge_array)

# Benchmark performance
result = AlgorithmsMultiverse::Sorting.benchmark(array, algorithm: :merge_sort)
puts "Time: #{result[:time]}s, Sorted: #{result[:sorted]}"
```

### Data Structures (Coming Soon)

- **LinkedList** - Doubly linked list with enumerable
- **Stack** - LIFO with thread safety
- **Queue** - FIFO with circular buffer
- **PriorityQueue** - Min-heap implementation
- **BinarySearchTree** - With balancing check
- **HashTable** - Open addressing & separate chaining
- **Trie** - Prefix tree for strings
- **Graph** - Adjacency list representation
- **DisjointSet** - Union-Find with path compression

### Graph Algorithms (Coming Soon)

- **Traversal**: BFS, DFS, Topological Sort
- **Shortest Path**: Dijkstra, Bellman-Ford, A*
- **MST**: Kruskal, Prim
- **Advanced**: SCC, Cycle Detection, Bipartite Check

### Dynamic Programming (Coming Soon)

- **Classic Problems**: Fibonacci, LCS, LIS, Edit Distance
- **Optimization**: Knapsack, Coin Change, Matrix Chain
- **String Problems**: Palindromes, Word Break
- **Graph DP**: Shortest Paths, Max Flow

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

### Custom Comparators

Most algorithms support custom comparison:

```ruby
# Sort by custom field
people = [
  { name: "Alice", age: 30 },
  { name: "Bob", age: 25 }
]

sorted = AlgorithmsMultiverse::Sorting.quick_sort(people) do |a, b|
  a[:age] <=> b[:age]
end
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

| Algorithm | Time | Space | Notes |
|-----------|------|-------|-------|
| QuickSort | O(n log n) avg | O(log n) | In-place, not stable |
| MergeSort | O(n log n) | O(n) | Stable, good for linked lists |
| HeapSort | O(n log n) | O(1) | In-place, not stable |
| CountingSort | O(n + k) | O(k) | For integers in known range |
| RadixSort | O(nk) | O(n) | k = number of digits |

## 🔧 Development

After checking out the repo:

```bash
bundle install           # Install dependencies
bundle exec rspec       # Run tests
bundle exec rubocop     # Check style
bundle exec yard doc    # Generate documentation
```

## 📄 License

MIT © Algorithms Multiverse

## 🔗 Links

- [GitHub Repository](https://github.com/algorithms-multiverse/ruby)
- [RubyGems](https://rubygems.org/gems/algorithms_multiverse)
- [Documentation](https://rubydoc.info/gems/algorithms_multiverse)