# Algorithms Multiverse - C Implementation

A comprehensive algorithm library written in modern C (C11 standard) providing efficient implementations of fundamental algorithms and data structures.

## Features

### 🔍 Sorting Algorithms (15+ implementations)
- **Basic Sorts**: Bubble, Insertion, Selection
- **Efficient Sorts**: Quick Sort, Merge Sort, Heap Sort
- **Specialized Sorts**: Radix Sort, Counting Sort, Bucket Sort
- **Hybrid Sorts**: Tim Sort, Intro Sort
- **Other Sorts**: Shell Sort, Comb Sort, Gnome Sort, Cocktail Sort
- **Parallel Implementations**: OpenMP-accelerated versions

### 🎯 Searching Algorithms
- Linear Search, Binary Search (iterative and recursive)
- Jump Search, Interpolation Search, Exponential Search
- Fibonacci Search, Ternary Search
- Finding kth smallest/largest elements
- Peak finding in 1D and 2D arrays
- Two-sum and three-sum problems

### 📦 Data Structures
- **Linear Structures**: Stack, Queue, Deque, Priority Queue
- **Lists**: Singly and Doubly Linked Lists
- **Trees**: Binary Search Tree, AVL Tree, Red-Black Tree, B-Tree
- **Hash Tables**: With multiple hash functions
- **Advanced**: Trie, Disjoint Set, Segment Tree, Fenwick Tree
- **Heap**: Min/Max heap implementations

### 📝 String Algorithms
- **Pattern Matching**: KMP, Rabin-Karp, Boyer-Moore, Z-algorithm
- **String Distances**: Levenshtein, Hamming, Jaro-Winkler
- **Palindromes**: Detection, longest palindrome, Manacher's algorithm
- **String Operations**: Reverse, case conversion, trimming
- **Hashing**: DJB2, FNV-1a, MurmurHash3
- **Suffix Structures**: Suffix arrays and trees

### 🔢 Numerical Algorithms
- **Number Theory**: GCD, LCM, modular arithmetic
- **Prime Numbers**: Primality tests, sieves, factorization
- **Combinatorics**: Factorials, binomial coefficients, Catalan numbers
- **Sequences**: Fibonacci, Lucas, Tribonacci, Collatz
- **Numerical Methods**: Newton-Raphson, bisection, integration
- **Interpolation**: Linear, Lagrange, Newton, spline
- **Random**: Various distributions and generators

### 📈 Additional Modules
- **Graph Algorithms**: BFS, DFS, Dijkstra, MST algorithms
- **Dynamic Programming**: Classic DP problems and solutions
- **Computational Geometry**: Convex hull, closest pair, intersections
- **Cryptography**: Classical ciphers, hashing, basic RSA
- **Matrix Operations**: Multiplication, decomposition, solving systems
- **Statistics**: Descriptive stats, regression, hypothesis testing
- **Optimization**: Gradient descent, genetic algorithms, simulated annealing
- **Streaming**: Reservoir sampling, sketches, online algorithms

## Building

### Prerequisites
- C compiler with C11 support (gcc, clang, or MSVC)
- Make build system
- OpenMP (optional, for parallel algorithms)

### Compilation

```bash
# Build debug version (default)
make

# Build release version (optimized)
make BUILD_MODE=release

# Build with specific compiler
make CC=clang

# Build and run tests
make test

# Build examples
make examples

# Clean build artifacts
make clean
```

### Installation

```bash
# Install to /usr/local (default)
sudo make install

# Install to custom location
sudo make install PREFIX=/opt/algorithms

# Uninstall
sudo make uninstall
```

## Usage

### Basic Example

```c
#include <stdio.h>
#include "algorithms_multiverse.h"

int main(void) {
    // Initialize library
    am_init();

    // Sorting example
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    size_t n = sizeof(arr) / sizeof(arr[0]);

    quick_sort(arr, n);
    printf("Sorted array: ");
    for (size_t i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    // Searching example
    search_result_t result = binary_search(arr, n, 25);
    if (result.found) {
        printf("Found 25 at index %zu\n", result.index);
    }

    // String algorithms example
    const char* text = "Hello World";
    const char* pattern = "World";
    pattern_match_result_t* matches = string_kmp_search(text, pattern);
    printf("Pattern found %zu times\n", matches->count);
    pattern_match_result_free(matches);

    // Numerical algorithms
    printf("GCD(48, 18) = %lld\n", gcd(48, 18));
    printf("10! = %lld\n", factorial(10));
    printf("Is 97 prime? %s\n", is_prime(97) ? "Yes" : "No");

    // Clean up
    am_cleanup();
    return 0;
}
```

### Compiling Your Program

```bash
# Using static library
gcc -o myprogram myprogram.c -L/path/to/lib -lalgorithms_multiverse -lm

# Using shared library
gcc -o myprogram myprogram.c -L/path/to/lib -lalgorithms_multiverse -lm -Wl,-rpath,/path/to/lib

# With OpenMP support
gcc -o myprogram myprogram.c -L/path/to/lib -lalgorithms_multiverse -lm -fopenmp
```

## Performance

The library includes optimized implementations with:
- **Time Complexity**: Documented for each algorithm
- **Space Complexity**: Memory-efficient implementations
- **Cache Optimization**: Data structure layout for better cache performance
- **Parallel Processing**: OpenMP support for suitable algorithms
- **SIMD**: Vectorization hints for compiler optimization

### Benchmarking

```c
// Benchmark sorting algorithms
int* arr = generate_random_array(10000, 0, 1000);
sort_stats_t stats = benchmark_sort(SORT_QUICK, arr, 10000);
printf("Quick Sort: %.3f ms\n", stats.time_ms);
free(arr);
```

## Testing

The library includes a comprehensive test suite:

```bash
# Run all tests
make test

# Run specific test
make test-sorting
make test-searching
make test-strings

# Run with coverage analysis
make coverage
```

## Examples

Complete examples are provided in the `examples/` directory:

- `comprehensive_example.c` - Demonstrates all major features
- `sorting_example.c` - Sorting algorithms comparison
- `graph_example.c` - Graph algorithms usage
- `string_example.c` - String processing examples

## Documentation

Generate full API documentation with Doxygen:

```bash
make docs
```

Documentation will be available in `docs/html/index.html`.

## Memory Management

The library provides memory tracking capabilities:

```c
// Print memory statistics
am_print_memory_stats();

// Use aligned allocation
void* buffer = am_aligned_alloc(1024, 64);  // 1KB aligned to 64 bytes
// ... use buffer ...
am_aligned_free(buffer);
```

## Thread Safety

- Most algorithms are thread-safe for read operations
- Data structures require external synchronization for concurrent access
- Parallel algorithms use OpenMP for thread management

## Platform Support

- **Linux**: Full support with gcc/clang
- **macOS**: Full support with clang/gcc
- **Windows**: Support with MinGW/MSVC
- **FreeBSD**: Full support

## Contributing

Contributions are welcome! Please ensure:
1. Code follows C11 standard
2. All tests pass
3. Memory leaks are checked with valgrind
4. Documentation is updated

## License

This project is part of the Algorithms Multiverse collection.

## Performance Comparison

| Algorithm | Time Complexity | Space Complexity | Best For |
|-----------|----------------|------------------|----------|
| Quick Sort | O(n log n) avg | O(log n) | General purpose |
| Merge Sort | O(n log n) | O(n) | Stable sorting |
| Heap Sort | O(n log n) | O(1) | Memory constrained |
| Radix Sort | O(nk) | O(n+k) | Integer sorting |
| Binary Search | O(log n) | O(1) | Sorted arrays |
| Hash Table | O(1) avg | O(n) | Fast lookups |
| B-Tree | O(log n) | O(n) | Database indexes |

## Acknowledgments

- OpenMP for parallel processing support
- Inspired by various algorithm textbooks and research papers
- Community contributions and feedback

---

For more information, visit the [Algorithms Multiverse](https://github.com/algorithms-multiverse) repository.