# Julia Algorithms Implementation

A comprehensive collection of classic computer science algorithms and data structures implemented in Julia, focusing on performance, clarity, and scientific computing applications.

## 📊 Statistics

- **Modules**: 7 specialized modules
- **Algorithms**: 100+ implementations
- **Data Structures**: 10+ fundamental structures
- **Categories**: Sorting, Searching, Graphs, Dynamic Programming, Strings, Data Structures, Numerical
- **Performance**: Optimized for Julia's JIT compilation and type system

## 🚀 Features

- **Type-generic implementations** using Julia's parametric types
- **Multiple dispatch** for algorithm specialization
- **Performance optimization** with Julia's JIT compiler
- **Named tuples** for structured results
- **Parallel algorithms** for multi-core systems
- **Scientific computing focus** with numerical algorithms
- **Comprehensive documentation** with complexity analysis

## 📦 Installation

```julia
# Clone the repository
git clone https://github.com/yourusername/algorithms-multiverse.git
cd algorithms-multiverse/julia

# Activate the project
using Pkg
Pkg.activate(".")
Pkg.instantiate()

# Load the module
using AlgorithmsMultiverse
```

## 🔧 Usage

### Basic Import

```julia
using AlgorithmsMultiverse

# Or import specific modules
using AlgorithmsMultiverse.Sorting
using AlgorithmsMultiverse.Searching
using AlgorithmsMultiverse.GraphAlgorithms
```

### Quick Examples

```julia
# Sorting
arr = [64, 34, 25, 12, 22, 11, 90]
sorted = Sorting.quicksort(copy(arr))
Sorting.mergesort!(arr)  # In-place variant

# Searching
result = Searching.binary_search([1, 3, 5, 7, 9], 5)
println("Found at index: $(result.index)")

# Graph algorithms
g = GraphAlgorithms.Graph()
GraphAlgorithms.add_edge!(g, 1, 2, 1.0)
distances, _ = GraphAlgorithms.dijkstra(g, 1)

# Dynamic programming
lcs_result = DynamicProgramming.lcs("AGGTAB", "GXTXAYB")
println("LCS length: $(lcs_result.length), string: $(lcs_result.string)")
```

## 📚 Module Overview

### 1. Sorting Module (`sorting.jl`)

**15 Sorting Algorithms** with in-place and functional variants:

```julia
# Quick Sort with parallel support
sorted = quicksort(arr)
quicksort!(arr)  # In-place
parallel_quicksort!(arr)  # Multi-threaded

# Merge Sort
mergesort!(arr)
merge_indices = mergesort_indices(arr)  # Returns sorted indices

# Heap Sort
heapsort!(arr)

# Radix Sort for integers
radixsort!(arr)

# Tim Sort (hybrid stable sort)
timsort!(arr)

# Counting Sort
counting_sort(arr, max_val)

# Other algorithms
bubble_sort!, selection_sort!, insertion_sort!
shellsort!, combsort!, gnomesort!
pancake_sort!, cocktail_sort!
```

**Complexity**: O(n log n) average for efficient sorts, O(n²) for simple sorts

### 2. Searching Module (`searching.jl`)

**17 Search Algorithms** for various data structures:

```julia
# Binary search variants
binary_search(arr, target)          # Standard binary search
lower_bound(arr, target)             # First occurrence
upper_bound(arr, target)             # Last position
binary_search_rotated(arr, target)   # Rotated sorted array

# Linear searches
linear_search(arr, target)
sentinel_search(arr, target)

# Advanced searches
ternary_search(arr, target)          # Ternary split
exponential_search(arr, target)      # Unbounded search
fibonacci_search(arr, target)        # Fibonacci-based
jump_search(arr, target)             # Block jumping

# Peak finding
find_peak_1d(arr)                    # 1D peak element
find_peak_2d(matrix)                 # 2D peak element

# K-th element algorithms
quickselect(arr, k)                  # K-th smallest
median_of_medians(arr, k)            # Guaranteed O(n)

# Pattern searching
two_pointer_search(arr, target_sum)  # Two sum problem
```

### 3. Data Structures Module (`data_structures.jl`)

**Fundamental Data Structures** with Julia-optimized implementations:

```julia
# Stack (LIFO)
s = Stack{Int}()
push!(s, 42)
item = pop!(s)

# Queue (FIFO)
q = Queue{String}()
enqueue!(q, "hello")
item = dequeue!(q)

# Binary Search Tree
bst = BinarySearchTree{Int}()
insert!(bst, 5)
found = search(bst, 5)
inorder_values = inorder(bst)

# Min Heap
heap = MinHeap{Int}()
push!(heap, 10)
min_val = pop!(heap)

# Trie (Prefix Tree)
trie = Trie()
insert!(trie, "apple")
exists = search(trie, "apple")
has_prefix = starts_with(trie, "app")

# Union-Find (Disjoint Set)
uf = UnionFind(10)
union!(uf, 1, 2)
same_set = connected(uf, 1, 2)
```

### 4. Graph Algorithms Module (`graph_algorithms.jl`)

**Comprehensive Graph Algorithms** with weighted edge support:

```julia
# Graph creation
g = Graph(directed=true)
add_vertex!(g, 1)
add_edge!(g, 1, 2, 3.5)  # From 1 to 2 with weight 3.5

# Traversal algorithms
dfs_order = dfs(g, 1)               # Depth-first search
bfs_order = bfs(g, 1)               # Breadth-first search

# Shortest path algorithms
distances, prev = dijkstra(g, 1)     # Single-source shortest paths
dist, prev = bellman_ford(g, 1)      # Handles negative weights

# Graph properties
has_cycle = has_cycle(g)             # Cycle detection
is_bipartite = is_bipartite(g)       # Bipartite check

# Topological sort (DAG only)
topo_order = topological_sort(g)
```

**Complexity**:
- DFS/BFS: O(V + E)
- Dijkstra: O((V + E) log V)
- Bellman-Ford: O(VE)

### 5. Dynamic Programming Module (`dynamic_programming.jl`)

**20 Classic DP Problems** with solution reconstruction:

```julia
# Sequence problems
fibonacci(10)                         # N-th Fibonacci number

# String algorithms
lcs("ABCDGH", "AEDFHR")             # Longest common subsequence
edit_distance("kitten", "sitting")   # Levenshtein distance
longest_palindrome("babad")          # Longest palindromic substring

# Array problems
lis([10, 9, 2, 5, 3, 7, 101])       # Longest increasing subsequence
max_subarray([-2, 1, -3, 4, -1])    # Maximum subarray (Kadane's)

# Optimization problems
knapsack(weights, values, capacity)  # 0/1 Knapsack
coin_change([1, 2, 5], 11)          # Minimum coins
house_robber([2, 7, 9, 3, 1])       # Maximum non-adjacent sum

# Advanced problems
matrix_chain_multiplication(dims)    # Optimal multiplication order
word_break("leetcode", ["leet", "code"])  # Word segmentation
egg_drop(2, 100)                    # Egg drop puzzle
```

### 6. String Algorithms Module (`string_algorithms.jl`)

**Pattern Matching and String Processing**:

```julia
# Pattern searching
kmp_search("ABABDABACDABABCABAB", "ABABCABAB")     # KMP algorithm
rabin_karp("hello world", "world")                  # Rolling hash
z_algorithm("aabcaabxaaaz")                         # Z-array

# String operations
longest_common_prefix(["flower", "flow", "flight"])  # Common prefix
is_palindrome("racecar")                            # Palindrome check
anagram_check("listen", "silent")                   # Anagram verification
string_compression("aabcccccaaa")                   # Run-length encoding
```

**Complexity**: O(n + m) for pattern matching, O(n) for most operations

### 7. Numerical Algorithms Module (`numerical_algorithms.jl`)

**Mathematical and Numerical Computing Algorithms**:

```julia
# Number theory
gcd(48, 18)                          # Greatest common divisor
lcm(12, 18)                          # Least common multiple
sieve_of_eratosthenes(100)           # Prime numbers up to n
is_prime(17)                         # Primality test
prime_factors(60)                    # Prime factorization

# Modular arithmetic
power_mod(3, 5, 7)                   # (3^5) % 7
binary_exponentiation(2, 10)         # Fast exponentiation

# Matrix operations
fibonacci_matrix(100)                 # N-th Fibonacci using matrices
matrix_power(A, n)                    # Matrix exponentiation

# Numerical methods
newton_raphson(f, df, x0)            # Root finding
bisection_method(f, a, b)            # Root by bisection
trapezoidal_integration(f, 0, 1)     # Numerical integration
simpsons_rule(f, 0, 1, 1000)         # Simpson's integration

# Linear algebra
gaussian_elimination(A, b)            # Solve Ax = b
```

**Features**:
- Arbitrary precision arithmetic support
- Optimized matrix operations
- Numerical stability considerations

## 🎯 Performance Optimizations

### Julia-Specific Optimizations

1. **Type Stability**: All functions are type-stable for JIT optimization
2. **In-place Operations**: `!` suffix indicates mutation for memory efficiency
3. **Parallel Algorithms**: Multi-threaded variants using `Threads.@threads`
4. **SIMD Vectorization**: Automatic vectorization for numerical operations
5. **Memory Layout**: Column-major ordering for matrices

### Example: Parallel Quick Sort

```julia
# Automatically uses multiple threads for large arrays
arr = rand(1_000_000)
@time parallel_quicksort!(arr)  # Much faster on multi-core systems
```

## 🧪 Testing

```julia
# Run tests
using Pkg
Pkg.test()

# Or run specific test files
include("test/test_sorting.jl")
include("test/test_searching.jl")
```

## 📖 Algorithm Complexity Reference

| Category | Algorithm | Time (Avg) | Time (Worst) | Space |
|----------|-----------|------------|--------------|--------|
| **Sorting** | Quick Sort | O(n log n) | O(n²) | O(log n) |
| | Merge Sort | O(n log n) | O(n log n) | O(n) |
| | Heap Sort | O(n log n) | O(n log n) | O(1) |
| | Tim Sort | O(n log n) | O(n log n) | O(n) |
| | Radix Sort | O(d(n+k)) | O(d(n+k)) | O(n+k) |
| **Searching** | Binary Search | O(log n) | O(log n) | O(1) |
| | Jump Search | O(√n) | O(√n) | O(1) |
| | Interpolation | O(log log n) | O(n) | O(1) |
| **Graph** | DFS/BFS | O(V+E) | O(V+E) | O(V) |
| | Dijkstra | O(E log V) | O(E log V) | O(V) |
| | Bellman-Ford | O(VE) | O(VE) | O(V) |
| **DP** | LCS | O(mn) | O(mn) | O(mn) |
| | Knapsack | O(nW) | O(nW) | O(nW) |
| | Edit Distance | O(mn) | O(mn) | O(mn) |
| **String** | KMP | O(n+m) | O(n+m) | O(m) |
| | Rabin-Karp | O(n+m) | O(nm) | O(1) |
| | Z-Algorithm | O(n) | O(n) | O(n) |

## 🔬 Scientific Computing Applications

Julia implementation is optimized for:

- **Numerical Analysis**: Root finding, integration, linear systems
- **Data Science**: Sorting, searching, and processing large datasets
- **Graph Analytics**: Network analysis, pathfinding, optimization
- **Bioinformatics**: String matching, sequence alignment (LCS)
- **Operations Research**: Knapsack, shortest paths, optimization

## 🛠️ Development

### Adding New Algorithms

1. Add implementation to appropriate module
2. Export function from module
3. Update main module exports
4. Add tests
5. Update documentation

### Code Style

- Use lowercase with underscores for functions
- Add type annotations where helpful
- Include docstrings with complexity analysis
- Prefer in-place operations with `!` suffix
- Use `where T` for generic types

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please ensure:
- Code follows Julia style conventions
- Includes comprehensive tests
- Adds appropriate documentation
- Maintains type stability

## 📚 References

- Cormen, Leiserson, Rivest, Stein. "Introduction to Algorithms"
- Julia Performance Tips: https://docs.julialang.org/en/v1/manual/performance-tips/
- Julia Style Guide: https://docs.julialang.org/en/v1/manual/style-guide/

---

*Part of the Algorithms Multiverse Project - Comprehensive algorithm implementations across multiple programming languages.*