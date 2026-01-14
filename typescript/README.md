# TypeScript Algorithm Implementation

A comprehensive, type-safe implementation of fundamental algorithms and data structures in TypeScript.

## 🚀 Features

- ✅ **Full TypeScript Support** - Strong typing with generics
- ✅ **Modern ES6+** - Uses latest JavaScript features
- ✅ **Comprehensive Coverage** - 50+ algorithms implemented
- ✅ **Performance Optimized** - Efficient implementations with complexity analysis
- ✅ **Well Documented** - JSDoc comments and examples
- ✅ **Zero Dependencies** - Pure TypeScript implementation
- ✅ **Tree-Shakeable** - Import only what you need

## 📦 Installation

```bash
npm install @algorithms-multiverse/typescript
```

Or using yarn:
```bash
yarn add @algorithms-multiverse/typescript
```

## 🎯 Quick Start

```typescript
import {
    QuickSort,
    BinarySearchTree,
    Graph,
    DynamicProgramming
} from '@algorithms-multiverse/typescript';

// Sorting
const sorter = new QuickSort<number>();
const array = [64, 34, 25, 12, 22, 11, 90];
sorter.sort(array);
console.log(array); // [11, 12, 22, 25, 34, 64, 90]

// Data Structures
const bst = new BinarySearchTree<number>();
[50, 30, 70, 20, 40].forEach(val => bst.insert(val));
console.log(bst.inOrder()); // [20, 30, 40, 50, 70]

// Graph Algorithms
const graph = new Graph<string>();
graph.addEdge('A', 'B', 4);
graph.addEdge('B', 'C', 2);
const distances = ShortestPath.dijkstra(graph, 'A');

// Dynamic Programming
const fib = DynamicProgramming.fibonacci(10);
console.log(fib); // 55
```

## 📚 Modules

### Sorting Algorithms (`sorting.ts`)

| Algorithm | Time Complexity | Space | Stable | Description |
|-----------|----------------|-------|--------|-------------|
| QuickSort | O(n log n) avg | O(log n) | No | Divide and conquer with pivot |
| MergeSort | O(n log n) | O(n) | Yes | Divide and conquer with merging |
| HeapSort | O(n log n) | O(1) | No | Binary heap based |
| TimSort | O(n log n) | O(n) | Yes | Hybrid stable sort (Python/Java default) |
| IntroSort | O(n log n) | O(log n) | No | Hybrid (Quick+Heap+Insertion) |
| RadixSort | O(nk) | O(n) | Yes | Non-comparative integer sort |

**Usage Example:**
```typescript
const sorter = new MergeSort<string>((a, b) => a.localeCompare(b));
const words = ['banana', 'apple', 'cherry'];
sorter.sort(words);
```

### Data Structures (`dataStructures.ts`)

| Structure | Insert | Delete | Search | Space |
|-----------|--------|--------|--------|-------|
| LinkedList | O(1)* | O(n) | O(n) | O(n) |
| Stack | O(1) | O(1) | O(n) | O(n) |
| Queue | O(1) | O(1) | O(n) | O(n) |
| PriorityQueue | O(log n) | O(log n) | O(n) | O(n) |
| BST | O(log n)* | O(log n)* | O(log n)* | O(n) |
| HashTable | O(1)* | O(1)* | O(1)* | O(n) |
| Trie | O(m) | O(m) | O(m) | O(ALPHABET_SIZE * m * n) |

*Average case

**Usage Example:**
```typescript
const trie = new Trie();
['apple', 'app', 'apricot'].forEach(word => trie.insert(word));
console.log(trie.startsWith('app')); // true
console.log(trie.getWordsWithPrefix('app')); // ['app', 'apple']
```

### Graph Algorithms (`graphAlgorithms.ts`)

**Graph Representations:**
- Adjacency List (default)
- Support for weighted/unweighted
- Support for directed/undirected

**Algorithms Included:**
- **Traversal:** BFS, DFS (iterative & recursive)
- **Shortest Path:** Dijkstra, Bellman-Ford, Floyd-Warshall, A*
- **MST:** Kruskal, Prim
- **Others:** Topological Sort, Cycle Detection, Strongly Connected Components

**Usage Example:**
```typescript
const graph = new Graph<string>(false); // undirected
graph.addEdge('A', 'B', 5);
graph.addEdge('B', 'C', 3);

// Find shortest path
const distances = ShortestPath.dijkstra(graph, 'A');

// Find minimum spanning tree
const mst = MinimumSpanningTree.kruskal(graph);
```

### Dynamic Programming (`dynamicProgramming.ts`)

**Problems Solved:**
- Fibonacci (with memoization)
- Longest Common Subsequence (LCS)
- Longest Increasing Subsequence (LIS)
- 0/1 Knapsack & Unbounded Knapsack
- Coin Change (minimum coins & number of ways)
- Edit Distance (Levenshtein)
- Maximum Subarray (Kadane's)
- House Robber
- Unique Paths in Grid
- Palindromic Substrings
- Matrix Chain Multiplication
- Word Break
- Regular Expression Matching

**Usage Example:**
```typescript
// Knapsack problem
const weights = [1, 3, 4, 5];
const values = [1, 4, 5, 7];
const capacity = 7;
const result = DynamicProgramming.knapsack(weights, values, capacity);
console.log(result); // { maxValue: 9, items: [1, 2] }

// Edit distance
const dist = DynamicProgramming.editDistance('kitten', 'sitting');
console.log(dist); // 3
```

### String Algorithms (`stringAlgorithms.ts`)

**Pattern Matching:**
- KMP (Knuth-Morris-Pratt)
- Rabin-Karp (Rolling Hash)
- Boyer-Moore
- Z-Algorithm

**String Processing:**
- Manacher's Algorithm (palindromes)
- Longest Common Prefix
- Anagram Detection & Grouping
- String Permutations
- Minimum Window Substring

**Utilities:**
- Case conversions (camelCase, snake_case, kebab-case)
- String validation
- Levenshtein distance

**Usage Example:**
```typescript
// Pattern matching
const text = 'ABABDABACDABABCABAB';
const pattern = 'ABABCABAB';
const matches = StringAlgorithms.kmpSearch(text, pattern);
console.log(matches); // [10]

// Find longest palindrome
const palindrome = StringAlgorithms.manacher('babad');
console.log(palindrome); // 'bab' or 'aba'
```

## 🧪 Testing

Run the test suite:
```bash
npm test
```

Run specific tests:
```bash
npm test -- sorting
npm test -- graph
```

## 📊 Performance

All implementations are optimized for performance while maintaining readability. Each algorithm includes:
- Time complexity analysis
- Space complexity analysis
- Performance statistics tracking
- Benchmarking utilities

```typescript
import { measurePerformance } from '@algorithms-multiverse/typescript';

const { result, timeMs } = measurePerformance(
    DynamicProgramming.fibonacci,
    40
);
console.log(`Fibonacci(40) = ${result}, Time: ${timeMs}ms`);
```

## 🔧 Configuration

### TypeScript Configuration

The library is compiled with strict TypeScript settings:
- `strict: true`
- `noImplicitAny: true`
- `strictNullChecks: true`
- Target: ES2020

### Browser Support

The library targets ES2020 but can be transpiled for older environments using your build tool.

## 📖 API Documentation

Full API documentation is available at: [API Docs](https://algorithms-multiverse.github.io/typescript)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](../CONTRIBUTING.md) for details.

### Development Setup

1. Clone the repository
2. Install dependencies: `npm install`
3. Build: `npm run build`
4. Test: `npm test`
5. Lint: `npm run lint`

## 📄 License

MIT © Algorithms Multiverse

## 🔗 Links

- [GitHub Repository](https://github.com/algorithms-multiverse/typescript)
- [NPM Package](https://www.npmjs.com/package/@algorithms-multiverse/typescript)
- [Issue Tracker](https://github.com/algorithms-multiverse/typescript/issues)

## ✨ Features Roadmap

- [ ] Graph visualization utilities
- [ ] Parallel algorithm implementations using Web Workers
- [ ] WebAssembly optimizations for critical paths
- [ ] React hooks for algorithm visualization
- [ ] More advanced algorithms (FFT, Suffix Arrays, etc.)

## 🙏 Acknowledgments

Special thanks to all contributors and the open-source community for inspiration and feedback.