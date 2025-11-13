# 🌟 Algorithms Multiverse

<div align="center"><a href="https://opensource.org/licenses/MIT">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
</a>
<a href="#-languages-included">
  <img src="https://img.shields.io/badge/Languages-14-blue.svg" alt="Languages">
</a>
<a href="#-algorithm-categories">
  <img src="https://img.shields.io/badge/Algorithms-280+-green.svg" alt="Algorithms">
</a>
<a href="#-documentation">
  <img src="https://img.shields.io/badge/Docs-Comprehensive-orange.svg" alt="Documentation">
</a>
<a href="#fortran-implementations">
  <img src="https://img.shields.io/badge/Fortran-Modern-red.svg" alt="Fortran">
</a>

<strong>A comprehensive, production-ready collection of fundamental algorithms and data structures implemented across 14 programming languages.</strong>

<em>Perfect for learning, comparing language syntax, technical interviews, and understanding algorithmic concepts.</em>

<a href="#-quick-start">Quick Start</a> • <a href="#-documentation">Documentation</a> • <a href="#-algorithm-categories">Algorithms</a> • <a href="#-contributing">Contributing</a> • <a href="./visualizer/">Visualizer</a></div>

--------------------------------------------------------------------------------

## 📑 Table of Contents

- [Purpose & Vision](#-purpose--vision)
- [Quick Start](#-quick-start)
- [Algorithm Categories](#-algorithm-categories)
- [Languages Included](#-languages-included)
- [Fortran Implementations](#-fortran-implementations)
- [Cache-Aware Algorithms](#-cache-aware-algorithms)
- [Parallel Algorithms](#-parallel-algorithms)
- [Project Structure](#-project-structure)
- [Documentation](#-documentation)
- [Interactive Visualizer](#-interactive-algorithm-visualizer)
- [Complexity Quick Reference](#-complexity-quick-reference)
- [Testing & Quality](#-testing--quality)
- [Contributing](#-contributing)
- [Learning Resources](#-learning-resources)
- [License](#-license)

--------------------------------------------------------------------------------

## 🎯 Purpose & Vision

### What is Algorithms Multiverse?

A **multi-language algorithm repository** designed for:

- 📚 **Learning**: Understand algorithms by seeing them implemented in different programming paradigms
- 🔄 **Comparison**: Compare syntax, idioms, and approaches across 14 languages
- 📖 **Reference**: Quick lookup for algorithm implementations with complexity analysis
- 🎓 **Education**: Comprehensive documentation, visualizations, and learning paths
- 💼 **Interview Prep**: Production-ready implementations with test cases
- 🚀 **Performance**: Benchmarked implementations with optimization notes
- 🔬 **Scientific Computing**: Extensive Fortran implementations for numerical analysis

### Why Multi-Language?

- See how **the same algorithm** is expressed in different languages
- Understand **language-specific optimizations** and idioms
- Learn **multiple languages** through familiar algorithms
- Compare **performance characteristics** across implementations
- Build **polyglot programming** skills
- Explore **legacy languages** (Fortran, COBOL) in modern contexts

--------------------------------------------------------------------------------

## 🚀 Quick Start

### For Beginners

<details><summary>
  <b>Start Here if You're New to Algorithms</b>
</summary>

1\. <strong>Clone the repository:</strong>
   <code>bash
   git clone https://github.com/diogoribeiro7/algorithms-multiverse.git
   cd algorithms-multiverse</code>

2\. <strong>Start with the visualizer</strong> (no coding required):
   <code>bash
   cd visualizer
   python -m http.server 8080
   # Open http://localhost:8080 in your browser</code>

3\. <strong>Run your first algorithm</strong> (Python example):
   <code>bash
   cd sorting
   python3 bubble_sort.py</code>

4\. <strong>Try Fortran data structures</strong>:
   <code>bash
   cd data-structures
   ./test_all_fortran_ds.sh</code></details>

### For Intermediate Users

<details><summary>
  <b>Start Here if You Know the Basics</b>
</summary>

1\. <strong>Explore algorithm categories:</strong>
   <code>bash
   # Graph algorithms with BFS/DFS
   cd graph-algorithms
   python3 graph_traversal.py

   # Dynamic programming
   cd dynamic-programming
   gfortran -O2 -o dp_test dp_algorithms.f90 &amp;&amp; ./dp_test

   # Cache-aware algorithms
   cd cache-aware-algorithms
   python3 benchmarks/run_all_benchmarks.py</code>

2\. <strong>Compare language implementations:</strong>
   <code>bash
   # See QuickSort in multiple languages
   cat sorting/quicksort.{py,f90,c,go,rs}</code>

3\. <strong>Run comprehensive Fortran test suite:</strong>
   <code>bash
   ./build_fortran.sh</code></details>

### For Advanced Users

<details><summary>
  <b>Start Here if You're an Experienced Developer</b>
</summary>

1\. <strong>Explore advanced implementations:</strong>
   <code>bash
   # Fortran numerical algorithms
   cd numerical
   gfortran -O3 -o numerical numerical_algorithms.f90 &amp;&amp; ./numerical

   # Cache-optimized algorithms
   cd cache-aware-algorithms/matrix
   python3 cache_blocked_matrix_multiply.py

   # Computational geometry
   cd computational-geometry
   gfortran -O3 -o geometry geometry.f90 &amp;&amp; ./geometry</code>

2\. <strong>Review production code:</strong>
   - Modern Fortran implementations: <a href="./FORTRAN_IMPLEMENTATIONS.md">FORTRAN_IMPLEMENTATIONS.md</a>
   - Cache-aware optimizations: <a href="./cache-aware-algorithms/README.md">cache-aware-algorithms/README.md</a>
   - Data structures: <a href="./data-structures/FORTRAN_DATA_STRUCTURES.md">data-structures/FORTRAN_DATA_STRUCTURES.md</a>

3\. <strong>Run benchmarks:</strong>
   <code>bash
   cd benchmarks
   python3 run_benchmarks.py --all</code></details>

--------------------------------------------------------------------------------

## 📊 Algorithm Categories

### 🔢 Sorting Algorithms

**12+ algorithms | 15+ languages | Animated visualizations**

Algorithm   | Time (Best) | Time (Avg) | Time (Worst) | Space    | Stable | Languages
----------- | ----------- | ---------- | ------------ | -------- | ------ | ---------
Quick Sort  | O(n log n)  | O(n log n) | O(n²)        | O(log n) | ✗      | ✅ 10+
Merge Sort  | O(n log n)  | O(n log n) | O(n log n)   | O(n)     | ✓      | ✅ 10+
Heap Sort   | O(n log n)  | O(n log n) | O(n log n)   | O(1)     | ✗      | ✅ 8+
Bubble Sort | O(n)        | O(n²)      | O(n²)        | O(1)     | ✓      | ✅ 12+

**New**: Complete Fortran implementations with benchmarks

**Directory**: [`sorting/`](./sorting/)

### 🔍 Searching Algorithms

**15+ variants | 10 languages | Fortran-optimized**

- Binary Search (iterative & recursive)
- Interpolation Search
- Jump Search
- Exponential Search
- Ternary Search
- Fibonacci Search

**Advanced Features**: First/Last occurrence, rotated arrays, optimization problems

**Directory**: [`searching/`](./searching/)

### 🌳 Data Structures

**10+ structures | Multiple languages | Fortran complete**

#### Core Structures (Fortran Implementation):

- **Binary Search Tree** (bst.f90) - Complete BST with all traversals
- **Stack** (stack.f90) - Array & linked implementations with applications
- **Queue** (queue.f90) - Circular, linked, priority queue, deque
- **Trie** (trie.f90) - Prefix tree with auto-complete
- **Linked Lists** - Singly & doubly linked
- **Hash Tables** - Separate chaining

#### Additional Structures:

- Trees: AVL, Red-Black (planned), Segment Trees
- Heaps: Min/Max heaps, Priority Queues
- Advanced: Union-Find, LRU Cache

**See**: [FORTRAN_DATA_STRUCTURES.md](./data-structures/FORTRAN_DATA_STRUCTURES.md)

**Directory**: [`data-structures/`](./data-structures/)

### 📈 Graph Algorithms

**12+ algorithms | Full test coverage | Fortran implementation**

**Traversal**:

- Depth-First Search (DFS)
- Breadth-First Search (BFS)
- Topological Sort

**Shortest Path**:

- Dijkstra's Algorithm - O(E log V)
- Bellman-Ford - O(VE)
- Floyd-Warshall - O(V³)

**Fortran**: Complete graph algorithms in `graph-algorithms/graph_algorithms.f90`

**Directory**: [`graph-algorithms/`](./graph-algorithms/)

### 💡 Dynamic Programming

**15+ classic problems | Fortran optimized**

Fortran implementations include:

- Fibonacci (memoization, tabulation, space-optimized)
- 0/1 Knapsack Problem
- Longest Common Subsequence (LCS)
- Coin Change Problem
- Edit Distance (Levenshtein)
- Matrix Chain Multiplication

**Performance**: Fortran implementations leverage array operations for optimal performance

**Directory**: [`dynamic-programming/`](./dynamic-programming/)

### 🔤 String Algorithms

**12+ algorithms | Pattern matching | Fortran complete**

- KMP (Knuth-Morris-Pratt) Pattern Matching
- Rabin-Karp Algorithm
- Naive Pattern Matching
- Longest Palindromic Substring
- String Hashing

**Fortran**: Complete string processing suite in `string-algorithms/string_algorithms.f90`

**Directory**: [`string-algorithms/`](./string-algorithms/)

### 🔢 Mathematical Algorithms

**25+ algorithms | Scientific computing focus**

**Number Theory** (8 languages):

- Sieve of Eratosthenes
- GCD & LCM (Euclidean, Extended GCD)
- Modular Arithmetic
- Primality Testing (Miller-Rabin)
- Prime Factorization

**Computational Geometry** (6 languages):

- Convex Hull (Graham Scan)
- Line Segment Intersection
- Point-in-Polygon Test

**Numerical Methods** (Fortran):

- Root Finding (Bisection, Newton-Raphson, Secant)
- Numerical Integration (Trapezoidal, Simpson's)
- Matrix Operations & Determinants
- Linear System Solving (Gaussian Elimination)
- Polynomial Evaluation (Horner's Method)

**Directory**: [`numerical/`](./numerical/), [`number-theory/`](./number-theory/), [`computational-geometry/`](./computational-geometry/)

### ⚡ Cache-Aware Algorithms

**NEW: Performance-optimized implementations**

- **Cache-Efficient Binary Search**: Eytzinger layout, 2-3x speedup
- **Cache-Blocked Matrix Multiplication**: 10-50x speedup
- **Cache-Optimized B-Trees**: Minimized cache misses
- **Cache-Oblivious Sorting**: Optimal for all cache levels
- **Cache-Friendly Graph Algorithms**: CSR format, level-synchronous BFS

**Features**:

- Software cache simulator
- Memory access pattern analysis
- Comprehensive benchmarks
- Performance visualization

**Directory**: [`cache-aware-algorithms/`](./cache-aware-algorithms/)

### 🔀 Parallel Algorithms

**Concurrent implementations with performance analysis**

- Parallel sorting algorithms
- Parallel matrix operations
- MapReduce patterns
- Thread-safe data structures

**Directory**: [`parallel-algorithms/`](./parallel-algorithms/)

--------------------------------------------------------------------------------

## 🌐 Languages Included

Language                                                                                       | Status     | Files | Focus Areas               | Notes
---------------------------------------------------------------------------------------------- | ---------- | ----- | ------------------------- | ------------------------------
![](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)         | ✅ Primary  | 104   | All categories            | Clean, type hints, cache-aware
Fortran                                                                                        | ✅ Complete | 20    | Scientific, Numerical, DS | Modern Fortran 90/95/2003/2008
![](https://img.shields.io/badge/C-A8B9CC?style=flat&logo=c&logoColor=black)                   | ✅ Complete | 14    | System-level, Performance | Manual memory management
![](https://img.shields.io/badge/C++-00599C?style=flat&logo=c%2B%2B&logoColor=white)           | ✅ Complete | 19    | Performance-critical      | STL, modern C++17/20
![](https://img.shields.io/badge/Go-00ADD8?style=flat&logo=go&logoColor=white)                 | ✅ Complete | 33    | Concurrency, Systems      | Goroutines, channels
![](https://img.shields.io/badge/Rust-000000?style=flat&logo=rust&logoColor=white)             | ✅ Complete | 24    | Memory safety             | Zero-cost abstractions
![](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) | ✅ Complete | 35    | Web, All categories       | ES6+, async/await
![](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white) | ✅ Growing  | 3     | Type-safe JS              | Strict mode, generics
R                                                                                              | ✅ Stats    | 9     | Statistical algorithms    | Vectorized operations
COBOL                                                                                          | ✅ Legacy   | 8     | Enterprise systems        | Free format, modern syntax
![](https://img.shields.io/badge/Kotlin-7F52FF?style=flat&logo=kotlin&logoColor=white)         | ✅ Complete | 7     | JVM platform              | Functional, concise
![](https://img.shields.io/badge/Ruby-CC342D?style=flat&logo=ruby&logoColor=white)             | 🚧 Partial | 3     | Sorting, Data Structures  | Idiomatic Ruby
![](https://img.shields.io/badge/C%23-239120?style=flat&logo=c-sharp&logoColor=white)          | 🚧 Partial | 4     | .NET ecosystem            | LINQ, async patterns
![](https://img.shields.io/badge/Swift-FA7343?style=flat&logo=swift&logoColor=white)           | 🚧 Partial | 10    | Apple platforms           | Protocol-oriented

**Legend**: ✅ Complete | 🚧 In Progress | 📝 Planned

--------------------------------------------------------------------------------

## 🏗️ Fortran Implementations

### Why Fortran?

Fortran remains the gold standard for:

- **Scientific Computing**: Native array operations, numerical stability
- **High Performance**: Optimized compilers, vectorization
- **Legacy Systems**: 60+ years of production code
- **Numerical Analysis**: Unmatched for mathematical computations

### What's Implemented

**Complete Implementations** (11 Programs):

1. **Sorting Algorithms** (`sorting/`)

  - QuickSort with 3-way partitioning
  - MergeSort (top-down & bottom-up)
  - HeapSort with priority queue

2. **Search Algorithms** (`searching/advanced_search.f90`)

  - Binary (iterative & recursive)
  - Interpolation, Jump, Exponential
  - Ternary, Fibonacci search
  - Performance comparisons

3. **Data Structures** (`data-structures/`)

  - **Binary Search Tree**: Full operations, traversals, balance checking
  - **Stack**: Array & linked, bracket matching, postfix evaluation
  - **Queue**: Circular, linked, priority queue, deque
  - **Trie**: Prefix matching, auto-complete
  - Linked Lists (singly & doubly)
  - Hash Tables

4. **Graph Algorithms** (`graph-algorithms/graph_algorithms.f90`)

  - BFS, DFS traversals
  - Dijkstra's shortest path
  - Adjacency matrix representation

5. **Dynamic Programming** (`dynamic-programming/dp_algorithms.f90`)

  - Fibonacci (3 variants)
  - 0/1 Knapsack
  - Longest Common Subsequence
  - Coin Change, Edit Distance
  - Matrix Chain Multiplication

6. **String Algorithms** (`string-algorithms/string_algorithms.f90`)

  - KMP pattern matching
  - Rabin-Karp (rolling hash)
  - Longest palindromic substring
  - String hashing

7. **Numerical Methods** (`numerical/numerical_algorithms.f90`)

  - Root finding (Bisection, Newton-Raphson, Secant)
  - Integration (Trapezoidal, Simpson's Rule)
  - Matrix operations & determinants
  - Linear system solving
  - Polynomial evaluation (Horner's method)

8. **Number Theory** (`number-theory/number_theory.f90`)

  - Sieve of Eratosthenes
  - GCD/LCM algorithms
  - Modular arithmetic

9. **Computational Geometry** (`computational-geometry/geometry.f90`)

  - Convex Hull (Graham Scan)
  - Line segment intersection

### Modern Fortran Features

- **Type-bound procedures** (OOP)
- **Pointers and dynamic allocation**
- **Recursive procedures**
- **Modules and encapsulation**
- **Intent specifications**
- **Array operations**

### Building and Testing

```bash
# Build and test all Fortran implementations
./build_fortran.sh

# Test data structures specifically
cd data-structures
./test_all_fortran_ds.sh

# Individual tests
gfortran -O2 -o bst_test bst.f90 && ./bst_test
```

### Documentation

- [FORTRAN_IMPLEMENTATIONS.md](./FORTRAN_IMPLEMENTATIONS.md) - Complete guide
- [FORTRAN_DATA_STRUCTURES.md](./data-structures/FORTRAN_DATA_STRUCTURES.md) - Data structures reference
- Inline documentation in all source files

--------------------------------------------------------------------------------

## 📁 Project Structure

```
algorithms-multiverse/
├── 📂 sorting/                    # Sorting algorithms (15+ implementations)
│   ├── quicksort.{py,f90,c,go,rs}
│   ├── mergesort.{py,f90,c}
│   └── heapsort.f90
│
├── 📂 searching/                  # Search algorithms
│   ├── advanced_search.{py,f90,cpp,go}
│   └── binary_search.*
│
├── 📂 data-structures/            # Fundamental structures
│   ├── bst.f90                   # Binary Search Tree
│   ├── stack.f90                 # Stack implementations
│   ├── queue.f90                 # Queue variants
│   ├── trie.f90                  # Trie/Prefix tree
│   ├── linkedlist.f90            # Linked lists
│   ├── hashtable.f90             # Hash tables
│   ├── test_all_fortran_ds.sh   # Test suite
│   └── FORTRAN_DATA_STRUCTURES.md
│
├── 📂 graph-algorithms/           # Graph theory
│   ├── graph_algorithms.{py,f90,c}
│   ├── dijkstra.*
│   └── bfs_dfs.*
│
├── 📂 dynamic-programming/        # DP problems
│   ├── dp_algorithms.f90
│   ├── knapsack.*
│   └── lcs.*
│
├── 📂 string-algorithms/          # String processing
│   ├── string_algorithms.f90
│   ├── kmp.*
│   └── suffix_array.*
│
├── 📂 numerical/                  # Numerical methods
│   └── numerical_algorithms.f90
│
├── 📂 number-theory/              # Number theory
│   └── number_theory.{py,f90,c,go,rs}
│
├── 📂 computational-geometry/     # Geometry algorithms
│   └── geometry.{c,f90,rs}
│
├── 📂 cache-aware-algorithms/     # Performance-optimized
│   ├── search/
│   ├── matrix/
│   ├── sorting/
│   ├── graph/
│   ├── profiling/
│   └── README.md
│
├── 📂 parallel-algorithms/        # Concurrent implementations
│   ├── sorting/
│   ├── matrix/
│   └── mapreduce/
│
├── 📂 visualizer/                 # Web-based visualizer
│   ├── index.html
│   └── js/
│
├── 📂 benchmarks/                 # Performance testing
│
├── 📂 docs/                       # Documentation
│
├── 📄 build_fortran.sh            # Fortran test runner
├── 📄 FORTRAN_IMPLEMENTATIONS.md  # Fortran guide
├── 📄 COMPLEXITY_GUIDE.md
├── 📄 IMPLEMENTATION_STATUS.md
└── 📄 README.md
```

--------------------------------------------------------------------------------

## 📚 Documentation

Comprehensive documentation for all skill levels:

Document                                                                   | Purpose                     | Audience
-------------------------------------------------------------------------- | --------------------------- | -------------
[README.md](./README.md)                                                   | Main overview & quick start | Everyone
[FORTRAN_IMPLEMENTATIONS.md](./FORTRAN_IMPLEMENTATIONS.md)                 | Complete Fortran guide      | Fortran users
[FORTRAN_DATA_STRUCTURES.md](./data-structures/FORTRAN_DATA_STRUCTURES.md) | Data structures in Fortran  | Intermediate
[COMPLEXITY_GUIDE.md](./COMPLEXITY_GUIDE.md)                               | Big O notation, analysis    | Beginners
[IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md)                     | What's implemented where    | Everyone
[cache-aware-algorithms/README.md](./cache-aware-algorithms/README.md)     | Performance optimization    | Advanced

--------------------------------------------------------------------------------

## 🎨 Interactive Algorithm Visualizer

**Live visualization of algorithm execution!**

[![Visualizer](https://img.shields.io/badge/Try%20It-Live%20Demo-brightgreen.svg)](./visualizer/)

Features:

- ✅ Sorting algorithms with animated charts
- ✅ Tree traversals with SVG visualization
- ✅ Graph algorithms (BFS, DFS, Dijkstra)
- ✅ Dynamic programming table filling
- ✅ Side-by-side comparison
- ✅ Adjustable speed (1x-10x)

```bash
cd visualizer
python -m http.server 8080
# Open http://localhost:8080
```

--------------------------------------------------------------------------------

## ⚡ Complexity Quick Reference

### Time Complexity Classes

Notation   | Name         | Example Algorithms
---------- | ------------ | -------------------------------
O(1)       | Constant     | Array access, hash lookup
O(log n)   | Logarithmic  | Binary search, balanced trees
O(n)       | Linear       | Linear search, traversal
O(n log n) | Linearithmic | Merge/Quick/Heap sort
O(n²)      | Quadratic    | Bubble/Selection/Insertion sort
O(2ⁿ)      | Exponential  | Subset generation

**Fastest → Slowest**:

```
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!)
```

--------------------------------------------------------------------------------

## ✅ Testing & Quality

### Test Coverage

- ✅ **Unit Tests**: 800+ test cases across all implementations
- ✅ **Integration Tests**: Cross-language validation
- ✅ **Edge Cases**: Empty, single elements, duplicates, large inputs
- ✅ **Performance Tests**: Complexity validation
- ✅ **Fortran Test Suite**: Automated with `build_fortran.sh`

### Running Tests

**Fortran**:

```bash
./build_fortran.sh
cd data-structures && ./test_all_fortran_ds.sh
```

**Python**:

```bash
pytest
pytest --cov=. --cov-report=html
```

**Others**: See language-specific test instructions in [IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md)

--------------------------------------------------------------------------------

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines.

### What to Contribute

- ✨ New algorithm implementations
- 🌐 Additional language support
- 📊 Performance optimizations
- 🐛 Bug fixes
- 📚 Documentation improvements
- 🧪 Additional test cases
- 🎨 Visualizer enhancements

### Quick Start

1. Fork the repository
2. Create a feature branch
3. Add your implementation with:

  - Clear documentation
  - Test cases
  - Complexity analysis
  - Example usage

4. Submit a pull request

--------------------------------------------------------------------------------

## 📚 Learning Resources

### Internal Resources

- [FORTRAN_IMPLEMENTATIONS.md](./FORTRAN_IMPLEMENTATIONS.md) - Fortran guide
- [COMPLEXITY_GUIDE.md](./COMPLEXITY_GUIDE.md) - Big O analysis
- [Interactive Visualizer](./visualizer/) - See algorithms in action
- [Cache-Aware Guide](./cache-aware-algorithms/README.md) - Performance optimization

### External Resources

- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)
- [VisuAlgo](https://visualgo.net/)
- [LeetCode](https://leetcode.com/)

### Books

- "Introduction to Algorithms" (CLRS)
- "The Algorithm Design Manual" (Skiena)
- "Modern Fortran" (Milan Curcic)

--------------------------------------------------------------------------------

## 📄 License

MIT License - Feel free to use these implementations for learning, reference, and commercial projects.

See [LICENSE](./LICENSE) for full details.

--------------------------------------------------------------------------------

## 🌟 Acknowledgments

**Created and maintained by**: [Diogo Ribeiro](https://github.com/diogoribeiro7)

This project demonstrates:

- Algorithm design across 15+ languages
- Modern Fortran in scientific computing
- Cache-aware performance optimization
- Production-ready code practices
- Comprehensive documentation
- Open-source collaboration

--------------------------------------------------------------------------------

## 📊 Repository Stats

![Lines of Code](https://img.shields.io/badge/Lines%20of%20Code-152k%2B-blue) ![Languages](https://img.shields.io/badge/Languages-14-green) ![Algorithms](https://img.shields.io/badge/Algorithm%20Files-286-orange) ![Test Coverage](https://img.shields.io/badge/Test%20Coverage-85%25%2B-brightgreen) ![Fortran Files](https://img.shields.io/badge/Fortran-20%20Files-red)

--------------------------------------------------------------------------------

## 🚀 Latest Additions

### Recent Updates:

- ✅ **Complete Fortran Data Structures**: BST, Stack, Queue, Trie
- ✅ **Fortran Numerical Methods**: Root finding, integration, matrix ops
- ✅ **Cache-Aware Algorithms**: 2-50x performance improvements
- ✅ **Parallel Algorithms**: Concurrent implementations
- ✅ **Comprehensive Test Suites**: `build_fortran.sh`, `test_all_fortran_ds.sh`
- ✅ **Extended Documentation**: 1000+ lines of Fortran guides

--------------------------------------------------------------------------------

<div align="center"><strong>Happy Coding! 🚀</strong>

&gt; <em>"The best way to learn algorithms is to implement them yourself."</em>

<strong>Star this repository if you find it helpful!</strong> ⭐

<a href="#-algorithms-multiverse">⬆ Back to Top</a>

<strong>GitHub</strong>: <a href="https://github.com/diogoribeiro7">@diogoribeiro7</a></div>
