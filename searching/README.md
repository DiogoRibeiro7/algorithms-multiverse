# Search Algorithms Collection

A comprehensive collection of binary search and advanced search algorithms implemented across multiple programming languages. Perfect for learning, comparing language syntax, understanding search algorithms, and practical applications.

## 🎯 What's New: Advanced Search Algorithms!

We've added a complete collection of **advanced search algorithms** beyond binary search:
- **Jump Search** - Block-based searching (O(√n))
- **Fibonacci Search** - No division operations
- **Interpolation Search** - O(log log n) for uniform data
- **Block Search** - Cache-optimized searching
- **Parallel Search** - Multi-threaded implementations
- **Hybrid Search** - Combining multiple strategies

📖 See [`ADVANCED_SEARCH_GUIDE.md`](./ADVANCED_SEARCH_GUIDE.md) for detailed usage guide and decision criteria.

## Table of Contents

- [Overview](#overview)
- [Binary Search Algorithms](#binary-search-algorithms)
- [Advanced Search Algorithms](#advanced-search-algorithms)
- [Language Implementations](#language-implementations)
- [Complexity Analysis](#complexity-analysis)
- [Usage Examples](#usage-examples)
- [Real-World Applications](#real-world-applications)
- [Running the Code](#running-the-code)
- [Performance Benchmarks](#performance-benchmarks)
- [Contributing](#contributing)

## Overview

Binary search is one of the most fundamental and efficient search algorithms in computer science. This collection provides implementations of classic binary search along with numerous powerful variants for solving diverse optimization and search problems.

### Why Binary Search?

- **Efficiency**: O(log n) time complexity - dramatically faster than linear search
- **Versatility**: Applicable to many problem domains beyond simple searching
- **Foundation**: Understanding binary search is crucial for many advanced algorithms
- **Interview Essential**: Frequently appears in technical interviews

## Binary Search Algorithms

### 1. Classic Binary Search

**Description**: Standard binary search on a sorted array.

**Implementations**:
- Iterative version (space efficient)
- Recursive version (elegant and educational)
- Generic with custom comparators

**Time Complexity**: O(log n)
**Space Complexity**: O(1) iterative, O(log n) recursive

**Use Cases**:
- Searching in sorted databases
- Dictionary lookups
- Finding elements in sorted collections

### 2. First/Last Occurrence

**Description**: Find the leftmost or rightmost occurrence of a target in an array with duplicates.

**Variants**:
- Find first occurrence
- Find last occurrence
- Count all occurrences
- Find range [first, last]

**Time Complexity**: O(log n)
**Space Complexity**: O(1)

**Use Cases**:
- Finding version ranges in sorted logs
- Determining time ranges in event data
- Database range queries

### 3. Rotated Sorted Array Search

**Description**: Search in an array that was originally sorted but rotated at some pivot.

**Variants**:
- Search for element
- Find rotation point (minimum element)

**Time Complexity**: O(log n)
**Space Complexity**: O(1)

**Use Cases**:
- Circular buffers
- Sorted data with wraparound
- Ring buffer implementations

**Example**:
```
Original: [0, 1, 2, 4, 5, 6, 7]
Rotated:  [4, 5, 6, 7, 0, 1, 2]  (rotated at index 4)
```

### 4. Exponential Search

**Description**: Finds a range where the target might exist, then performs binary search.

**Time Complexity**: O(log n)
**Space Complexity**: O(1)

**Advantages**:
- Excellent for unbounded/infinite arrays
- Better than binary search when target is near the beginning
- Useful when array size is unknown

**Use Cases**:
- Streaming data
- Infinite sequences
- Unknown array bounds

### 5. Interpolation Search

**Description**: Uses value information to estimate position (similar to looking up a phone book).

**Time Complexity**:
- Average: O(log log n) for uniformly distributed data
- Worst: O(n) for non-uniform data

**Space Complexity**: O(1)

**Best For**:
- Uniformly distributed numerical data
- Large sorted arrays
- When value distribution is known

**Use Cases**:
- Searching in numerical databases
- Phonebook lookups
- Evenly distributed datasets

### 6. Ternary Search

**Description**: Divides the search space into three parts instead of two.

**Implementations**:
- Array search variant
- Finding maximum/minimum of unimodal functions

**Time Complexity**: O(log₃ n) ≈ O(log n)
**Space Complexity**: O(1)

**Use Cases**:
- Finding maximum of unimodal functions (single peak)
- Optimization problems
- Calculus applications (finding extrema)

**Example Application**:
```python
# Find the maximum of f(x) = -(x-5)² + 25
# The function has a peak at x = 5
```

### 7. Binary Search on Answer (Optimization)

**Description**: Binary search on the answer space rather than a given array. Incredibly powerful for optimization problems.

**Implementations**:
- Generic predicate-based search
- Integer square root
- Decimal square root
- Nth root calculation

**Time Complexity**: O(log(range) * T) where T is predicate evaluation time
**Space Complexity**: O(1)

**Problem Types**:
- **Minimization**: "What's the minimum capacity needed?"
- **Maximization**: "What's the maximum distance achievable?"
- **Threshold finding**: "What's the smallest/largest value that satisfies condition X?"

**Real-World Examples**:
- Shipping capacity calculation
- Resource allocation
- Rate limiting
- Mathematical computations (square root, nth root)

**Classic Problems**:
- Minimize maximum pages in book allocation
- Ship packages within D days
- Painter's partition problem
- Aggressive cows problem

### 8. Advanced Utilities

**Implementations**:
- Find insertion position for sorted array
- Find closest element to target
- Find peak element
- Search insert position

**Use Cases**:
- Maintaining sorted collections
- Nearest neighbor search
- Peak finding in signals
- Auto-complete suggestions

## Advanced Search Algorithms

Beyond binary search, we provide optimized implementations of advanced search algorithms for specific use cases:

### 9. Jump Search

**Time Complexity**: O(√n)
**Space Complexity**: O(1)

**When to Use**:
- Comparisons are expensive (e.g., string/object comparisons)
- Sequential access patterns preferred (tapes, streams)
- Want fewer comparisons than binary search

**Key Advantage**: Only O(√n) comparisons vs O(log n) for binary search

**Implementations**: Python (`advanced_search.py`), JavaScript (`advanced_search.js`)

### 10. Fibonacci Search

**Time Complexity**: O(log n)
**Space Complexity**: O(1)

**When to Use**:
- Division operations are expensive (embedded systems, old CPUs)
- Large arrays where cache performance matters
- Want to avoid modulo operations

**Key Advantage**: No division operations - uses only addition/subtraction

**Implementations**: Python, JavaScript

### 11. Interpolation Search

**Time Complexity**: O(log log n) average, O(n) worst
**Space Complexity**: O(1)

**When to Use**:
- Data is uniformly distributed
- Numeric data (integers, floats)
- Array size > 10,000 elements

**Key Advantage**: O(log log n) beats binary search's O(log n) for uniform data

**Implementations**: Included in binary search files, Python, JavaScript advanced versions

### 12. Block Search (Cache-Optimized)

**Time Complexity**: O(n/block_size + block_size) = O(√n)
**Space Complexity**: O(1)

**When to Use**:
- Cache performance is critical
- Very large arrays (>1GB)
- Memory access patterns matter

**Key Advantage**: Excellent cache locality and predictable memory access

**Implementations**: Python, JavaScript

### 13. Parallel Search

**Time Complexity**: O(n / num_cores) with parallelism
**Space Complexity**: O(num_cores)

**When to Use**:
- Very large arrays (millions of elements)
- Multi-core CPUs available
- Search time is critical
- Can be used with sorted or unsorted data

**Key Advantage**: Linear speedup with number of cores

**Implementations**: Python (ThreadPoolExecutor), JavaScript (async/Promises)

### 14. Hybrid Search

**Time Complexity**: O(log n + threshold)
**Space Complexity**: O(1)

**When to Use**:
- General-purpose optimized search
- Want best cache locality
- Arrays of any size

**Key Advantage**: Combines binary search efficiency with linear search cache-friendliness

**Implementations**: Python, JavaScript

### 15. Adaptive Search

**Time Complexity**: Varies (auto-selects best algorithm)
**Space Complexity**: O(1)

**When to Use**:
- Array characteristics unknown
- General library implementation
- Want automatic optimization

**Key Advantage**: Automatically chooses optimal algorithm based on input characteristics

**Implementations**: Python, JavaScript

### Algorithm Selection Quick Guide

| Array Size | Data Type | Best Algorithm | Reason |
|------------|-----------|----------------|--------|
| < 100 | Any | Sentinel Linear | Simple, cache-friendly |
| 100-1000 | Sorted | Jump Search | Good balance |
| 1000-10000 | Sorted | Binary Search | O(log n) optimal |
| 10000+ | Sorted, Uniform | Interpolation | O(log log n) |
| 10000+ | Sorted | Fibonacci | No division, cache-friendly |
| Very Large | Sorted | Hybrid Search | Best cache locality |
| Very Large | Unsorted | Parallel Search | Multi-core advantage |

📖 **Detailed Guide**: See [`ADVANCED_SEARCH_GUIDE.md`](./ADVANCED_SEARCH_GUIDE.md) for comprehensive decision criteria, performance analysis, and real-world examples.

## Language Implementations

### Binary Search Collection

All algorithms are implemented in the following languages with language-specific features:

| Language | File | Key Features |
|----------|------|--------------|
| **Python** | `binary_search.py` | Type hints, list comprehensions, docstrings, doctests |
| **Java** | `BinarySearch.java` | Generics, comparators, functional interfaces, streams |
| **C** | `binary_search.c` | Function pointers, efficient memory usage, manual memory management |
| **Go** | `binary_search.go` | Interfaces, goroutines-ready, slices, first-class functions |
| **Rust** | `binary_search.rs` | Ownership, traits, zero-cost abstractions, memory safety |
| **Swift** | `binary_search.swift` | Protocols, optionals, value types, functional programming |
| **Fortran** | `binary_search.f90` | Module system, array operations, numerical computing |
| **COBOL** | `BINARYSEARCH.cob` | Business logic, table handling, structured programming |
| **R** | `binary_search.R` | Vectorization, statistical computing, functional style |

### Advanced Search Collection

| Language | File | Advanced Algorithms Included |
|----------|------|------------------------------|
| **Python** | `advanced_search.py` | Jump, Fibonacci, Sentinel, Block, Parallel, Hybrid, Adaptive + Performance Analyzer |
| **JavaScript** | `advanced_search.js` | Jump, Fibonacci, Block, Async Parallel, Hybrid, Adaptive + Web Workers ready |

📖 **Comprehensive Guide**: [`ADVANCED_SEARCH_GUIDE.md`](./ADVANCED_SEARCH_GUIDE.md) - Decision trees, performance analysis, and real-world use cases

## Complexity Analysis

### Time Complexity Comparison

| Algorithm | Best Case | Average Case | Worst Case | Notes |
|-----------|-----------|--------------|------------|-------|
| **Basic Algorithms** |
| Linear Search | O(1) | O(n) | O(n) | Unsorted arrays |
| Binary Search | O(1) | O(log n) | O(log n) | Sorted arrays standard |
| **Binary Search Variants** |
| Exponential Search | O(1) | O(log n) | O(log n) | Better for nearby elements |
| Interpolation Search | O(1) | O(log log n) | O(n) | Uniform distribution only |
| Ternary Search | O(1) | O(log₃ n) | O(log₃ n) | Unimodal functions |
| **Advanced Algorithms** |
| Jump Search | O(1) | O(√n) | O(√n) | Fewer comparisons |
| Fibonacci Search | O(1) | O(log n) | O(log n) | No division operations |
| Block Search | O(1) | O(√n) | O(√n) | Cache-optimized |
| Hybrid Search | O(1) | O(log n) | O(log n) | Best cache locality |
| Parallel Search | O(1) | O(n / cores) | O(n / cores) | Multi-threaded |

### Space Complexity

| Implementation | Space Complexity | Notes |
|----------------|------------------|-------|
| Iterative | O(1) | Constant space |
| Recursive | O(log n) | Call stack depth |
| With auxiliary arrays | O(n) | Depends on implementation |

## Usage Examples

### Python Example

```python
from binary_search import *

# Classic search
arr = [1, 3, 5, 7, 9, 11, 13, 15]
result = binary_search_iterative(arr, 7)
print(f"Found at index: {result}")  # Output: 3

# Find all occurrences
arr_dup = [1, 2, 2, 2, 3, 4, 4, 5]
count = count_occurrences(arr_dup, 2)
print(f"Count: {count}")  # Output: 3

# Rotated array search
rotated = [4, 5, 6, 7, 0, 1, 2]
result = search_rotated_array(rotated, 0)
print(f"Found at index: {result}")  # Output: 4

# Square root
sqrt = find_square_root(50, precision=2)
print(f"√50 ≈ {sqrt}")  # Output: 7.07

# Binary search on answer - example: find minimum capacity
def can_ship(capacity, weights, days):
    day_count, current_weight = 1, 0
    for w in weights:
        if current_weight + w > capacity:
            day_count += 1
            current_weight = w
        else:
            current_weight += w
    return day_count <= days

weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
min_capacity = binary_search_on_answer(
    lambda cap: can_ship(cap, weights, 5),
    1, 55
)
print(f"Minimum capacity: {min_capacity}")  # Output: 15
```

### Java Example

```java
// Classic search
Integer[] arr = {1, 3, 5, 7, 9, 11, 13, 15};
int result = BinarySearch.binarySearchIterative(arr, 7);
System.out.println("Found at index: " + result);

// Custom comparator (case-insensitive strings)
String[] strings = {"Apple", "banana", "Cherry", "date"};
int idx = BinarySearch.binarySearchWithComparator(
    strings,
    "cherry",
    String.CASE_INSENSITIVE_ORDER
);

// Find closest element
int[] numbers = {1, 3, 5, 7, 9};
int closest = BinarySearch.findClosest(numbers, 6);
System.out.println("Closest: " + numbers[closest]);  // Output: 5 or 7
```

### Go Example

```go
// Classic search
arr := []int{1, 3, 5, 7, 9, 11, 13, 15}
result := BinarySearchIterative(arr, 7)
fmt.Printf("Found at index: %d\n", result)

// Exponential search (good for large arrays)
largeArr := make([]int, 1000000)
for i := range largeArr {
    largeArr[i] = i * 2
}
result = ExponentialSearch(largeArr, 100000)

// Find peak element
peaks := []int{1, 3, 20, 4, 1, 0}
peak := FindPeakElement(peaks)
fmt.Printf("Peak at index: %d, value: %d\n", peak, peaks[peak])
```

## Real-World Applications

### 1. Database Systems
- **Index searching**: B-tree indexes use binary search principles
- **Range queries**: Finding records within a date/value range
- **Join operations**: Merge joins in sorted tables

### 2. Version Control
- **Git bisect**: Finding the commit that introduced a bug
- **Binary search through commits**: O(log n) instead of O(n)

### 3. Computer Graphics
- **Ray tracing**: Finding intersections
- **Texture mapping**: Efficient lookups

### 4. Resource Allocation
- **Cloud computing**: Determining minimum resources needed
- **Network bandwidth**: Optimal allocation algorithms
- **Memory management**: Finding suitable memory blocks

### 5. Machine Learning
- **Hyperparameter tuning**: Finding optimal parameters
- **Threshold selection**: Classification decision boundaries
- **Feature selection**: Binary search for feature importance

### 6. Game Development
- **Collision detection**: Spatial partitioning
- **Difficulty balancing**: Finding right challenge level
- **Resource streaming**: Loading assets based on distance

### 7. Financial Systems
- **Options pricing**: Newton-Raphson with binary search
- **Risk calculation**: Finding breakeven points
- **Portfolio optimization**: Efficient frontier computation

## Running the Code

### Python
```bash
cd searching/
python3 binary_search.py
```

### Java
```bash
cd searching/
javac BinarySearch.java
java BinarySearch
```

### C
```bash
cd searching/
gcc -o binary_search binary_search.c -lm
./binary_search
```

### Go
```bash
cd searching/
go run binary_search.go
```

### Rust
```bash
cd searching/
rustc binary_search.rs
./binary_search
```

### Swift
```bash
cd searching/
swift binary_search.swift
```

### Fortran
```bash
cd searching/
gfortran -o binary_search binary_search.f90
./binary_search
```

### COBOL
```bash
cd searching/
cobc -x BINARYSEARCH.cob
./BINARYSEARCH
```

### R
```bash
cd searching/
Rscript binary_search.R
```

## Performance Benchmarks

Typical performance on an array of 1,000,000 elements (100 searches):

| Algorithm | Time (ms) | Notes |
|-----------|-----------|-------|
| Binary (Iterative) | 0.05 | Fastest for general use |
| Binary (Recursive) | 0.06 | Slightly slower due to recursion |
| Exponential Search | 0.07 | Better for elements near start |
| Interpolation Search | 0.03 | Best for uniform distribution |
| Ternary Search | 0.08 | More comparisons than binary |

**Note**: Actual performance varies based on:
- Hardware specifications
- Compiler optimizations
- Data distribution
- Cache locality

## Common Pitfalls and Best Practices

### Pitfalls to Avoid

1. **Integer Overflow**:
   ```python
   # Bad
   mid = (left + right) / 2

   # Good
   mid = left + (right - left) / 2
   ```

2. **Off-by-One Errors**:
   - Always verify loop conditions (`<=` vs `<`)
   - Check array bounds carefully
   - Test with single-element arrays

3. **Unsorted Input**:
   - Binary search ONLY works on sorted data
   - Always verify data is sorted first

4. **Infinite Loops**:
   - Ensure search space shrinks each iteration
   - Verify termination conditions

### Best Practices

1. **Choose the Right Variant**:
   - Use classic binary search for standard sorted arrays
   - Use interpolation for uniformly distributed numerical data
   - Use exponential search when target is likely near the beginning

2. **Handle Edge Cases**:
   ```python
   # Always check
   - Empty arrays
   - Single element
   - All duplicates
   - Element not present
   ```

3. **Optimize for Your Use Case**:
   - Iterative for production (better space complexity)
   - Recursive for clarity and education
   - Consider cache locality for large arrays

## Test Coverage

Each implementation includes:
- ✅ Empty array handling
- ✅ Single element arrays
- ✅ Element not found cases
- ✅ First/last element searches
- ✅ Duplicate handling
- ✅ Large array stress tests
- ✅ Edge case validation

## Educational Resources

### Visualization
- [VisuAlgo Binary Search](https://visualgo.net/en/bst)
- [Algorithm Visualizer](https://algorithm-visualizer.org/)

### Practice Problems
- LeetCode: Binary Search tag
- HackerRank: Search section
- CodeForces: Binary Search problems

### Further Reading
- "Introduction to Algorithms" (CLRS) - Chapter 12
- "Programming Pearls" by Jon Bentley - Column 4
- "The Algorithm Design Manual" by Steven Skiena

## Contributing

Contributions are welcome! Please ensure:

1. Code follows language-specific conventions
2. All variants are implemented
3. Comprehensive comments and documentation
4. Test cases included
5. Performance benchmarks updated

## License

MIT License - Feel free to use these implementations for learning and reference.

## Acknowledgments

This collection is part of the [Algorithms Multiverse](../) project - a comprehensive multi-language algorithm repository.

---

**Happy Searching! 🔍**

> "The best way to understand algorithms is to implement them yourself - and then implement them again in a different language!" - Algorithms Multiverse
