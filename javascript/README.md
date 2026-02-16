# Algorithms Multiverse - JavaScript Implementation

A comprehensive collection of algorithms and data structures implemented in modern JavaScript (ES6+).

## 📁 Project Structure

```
javascript/
├── src/
│   ├── sorting.js            # Sorting algorithms
│   ├── searching.js          # Searching algorithms
│   ├── dataStructures.js     # Data structure implementations
│   ├── stringAlgorithms.js   # String processing algorithms
│   ├── numerical.js          # Numerical and mathematical algorithms
│   ├── dynamicProgramming.js # Dynamic programming solutions
│   ├── graph.js              # Graph algorithms and structures
│   ├── matrix.js             # Matrix operations and linear algebra
│   ├── utils.js              # Utility functions and helpers
│   └── index.js              # Main export file
├── tests/
│   ├── sorting.test.js       # Sorting algorithm tests
│   ├── searching.test.js     # Searching algorithm tests
│   ├── dataStructures.test.js # Data structure tests
│   └── runAllTests.js        # Test runner script
├── examples/
│   ├── pathfinding.js        # Graph pathfinding examples
│   ├── textAnalysis.js       # String algorithm examples
│   └── optimization.js       # Dynamic programming examples
├── package.json              # Node.js package configuration
└── README.md                # This file
```

## 🚀 Getting Started

### Installation

```bash
# Clone the repository
git clone <repository-url>

# Navigate to JavaScript directory
cd algorithms-multiverse/javascript

# Install dependencies (if any)
npm install
```

### Usage

#### Import specific modules

```javascript
import { quickSort, mergeSort } from './src/sorting.js';
import { Graph, dijkstra } from './src/graph.js';
import { BinarySearchTree } from './src/dataStructures.js';
```

#### Import everything

```javascript
import algorithms from './src/index.js';

// Use algorithms
const sorted = algorithms.sorting.quickSort([3, 1, 4, 1, 5]);
const graph = new algorithms.graph.Graph();
```

## 📚 Available Algorithms

### Sorting Algorithms
- Bubble Sort
- Insertion Sort
- Selection Sort
- Merge Sort
- Quick Sort
- Heap Sort
- Radix Sort
- Counting Sort
- Bucket Sort
- Shell Sort
- Cocktail Sort
- Comb Sort
- Gnome Sort
- Cycle Sort
- Odd-Even Sort
- Bitonic Sort

### Searching Algorithms
- Linear Search
- Binary Search
- Jump Search
- Interpolation Search
- Exponential Search
- Fibonacci Search
- Ternary Search
- Two Sum / Three Sum
- Search in Rotated Array
- Find Peak Element
- Search in 2D Matrix

### Data Structures
- Stack
- Queue
- Linked List (Singly & Doubly)
- Binary Search Tree
- AVL Tree
- Red-Black Tree
- Min/Max Heap
- Trie (Prefix Tree)
- Disjoint Set (Union-Find)
- Segment Tree
- Fenwick Tree (Binary Indexed Tree)

### String Algorithms
- KMP Pattern Matching
- Rabin-Karp Algorithm
- Boyer-Moore Algorithm
- Levenshtein Distance
- Longest Common Subsequence
- Longest Palindromic Substring
- String Hashing
- Z-Algorithm
- Manacher's Algorithm

### Graph Algorithms
- BFS / DFS
- Dijkstra's Shortest Path
- Bellman-Ford Algorithm
- Floyd-Warshall Algorithm
- Kruskal's MST
- Prim's MST
- Topological Sort
- Strongly Connected Components
- Cycle Detection
- Bridge & Articulation Point Finding
- Graph Coloring
- Eulerian Path
- Hamiltonian Path
- Maximum Flow (Ford-Fulkerson)

### Dynamic Programming
- 0/1 Knapsack
- Coin Change
- Longest Increasing Subsequence
- Edit Distance
- Matrix Chain Multiplication
- Unique Paths in Grid
- Maximum Subarray Sum
- Stock Buy/Sell Problems
- Word Break
- Palindrome Partitioning
- Regular Expression Matching

### Numerical Algorithms
- GCD / LCM
- Prime Number Checking
- Sieve of Eratosthenes
- Prime Factorization
- Fibonacci Numbers
- Factorial
- Binomial Coefficients
- Fast Exponentiation
- Modular Arithmetic
- Newton-Raphson Method
- Numerical Integration

### Matrix Operations
- Matrix Addition/Subtraction
- Matrix Multiplication
- Matrix Transpose
- Determinant Calculation
- Matrix Inversion
- LU Decomposition
- QR Decomposition
- Cholesky Decomposition
- Eigenvalue Decomposition
- Singular Value Decomposition
- Solving Linear Systems

## 🧪 Running Tests

```bash
# Run all tests
node tests/runAllTests.js

# Run specific test file
node tests/sorting.test.js
node tests/searching.test.js
node tests/dataStructures.test.js
```

## 💡 Examples

Check the `examples/` directory for practical demonstrations:

### Pathfinding Example
```bash
node examples/pathfinding.js
```
Demonstrates graph algorithms for route optimization and network analysis.

### Text Analysis Example
```bash
node examples/textAnalysis.js
```
Shows string algorithms for pattern matching, spell checking, and text similarity.

### Optimization Example
```bash
node examples/optimization.js
```
Illustrates dynamic programming solutions for resource allocation and optimization problems.

## 📊 Performance Characteristics

### Time Complexities

| Algorithm | Best Case | Average Case | Worst Case | Space |
|-----------|----------|--------------|------------|-------|
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) |
| Dijkstra's | O(V²) | O(E log V) | O(E log V) | O(V) |
| BFS/DFS | O(V + E) | O(V + E) | O(V + E) | O(V) |

## 🔧 Utility Functions

The `utils.js` module provides helpful utilities:

- Array operations (shuffle, chunk, flatten, unique)
- Mathematical functions (GCD, LCM, combinations, permutations)
- Random utilities (random selection, weighted choice)
- Functional programming helpers (compose, pipe, memoize)
- Performance measurement tools
- Bit manipulation utilities

## 🤝 Contributing

Contributions are welcome! When adding new algorithms:

1. Implement the algorithm in the appropriate module
2. Add comprehensive tests
3. Include usage examples
4. Update documentation
5. Ensure code follows ES6+ standards

## 📄 License

[License details here]

## 🔗 Related Implementations

- [C Implementation](../c/README.md)
- [Python Implementation](../python/README.md)
- [Rust Implementation](../rust/README.md)
- [Go Implementation](../go/README.md)

## 📧 Contact

[Contact information here]