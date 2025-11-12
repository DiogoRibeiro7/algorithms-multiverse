# 📐 Algorithm Complexity Guide

**A comprehensive guide to understanding Big O notation, time complexity, space complexity, and algorithm analysis techniques.**

---

## 📑 Table of Contents

- [Introduction](#introduction)
- [What is Big O Notation?](#what-is-big-o-notation)
- [Common Complexity Classes](#common-complexity-classes)
- [Time Complexity](#time-complexity)
  - [Constant Time O(1)](#constant-time-o1)
  - [Logarithmic Time O(log n)](#logarithmic-time-olog-n)
  - [Linear Time O(n)](#linear-time-on)
  - [Linearithmic Time O(n log n)](#linearithmic-time-on-log-n)
  - [Quadratic Time O(n²)](#quadratic-time-on)
  - [Cubic Time O(n³)](#cubic-time-on)
  - [Exponential Time O(2ⁿ)](#exponential-time-o2)
  - [Factorial Time O(n!)](#factorial-time-on-1)
- [Space Complexity](#space-complexity)
- [Best, Average, and Worst Case](#best-average-and-worst-case)
- [Amortized Analysis](#amortized-analysis)
- [Master Theorem](#master-theorem)
- [Complexity Decision Tree](#complexity-decision-tree)
- [Practical Examples](#practical-examples)
- [Common Pitfalls](#common-pitfalls)
- [Optimization Strategies](#optimization-strategies)

---

## Introduction

Algorithm complexity analysis helps us understand:
- How an algorithm's performance scales with input size
- Which algorithm to choose for a given problem
- Performance bottlenecks in our code
- Trade-offs between different approaches

**Key Concepts**:
- **Time Complexity**: How execution time grows with input size
- **Space Complexity**: How memory usage grows with input size
- **Big O Notation**: Mathematical notation for describing complexity

---

## What is Big O Notation?

Big O notation describes the **upper bound** (worst-case scenario) of an algorithm's growth rate.

### Formal Definition

For a function f(n), we say **f(n) = O(g(n))** if there exist constants c > 0 and n₀ ≥ 0 such that:

```
f(n) ≤ c · g(n)  for all n ≥ n₀
```

### Intuitive Meaning

Big O tells us **how the runtime grows** as the input size (n) increases, **ignoring constants and lower-order terms**.

**Examples**:
- `3n² + 5n + 10` → `O(n²)` (n² dominates as n grows)
- `n log n + 1000n` → `O(n log n)` (n log n dominates)
- `100` → `O(1)` (constant, doesn't depend on n)

### Why Ignore Constants?

```python
# Both are O(n), but Algorithm A is faster in practice
def algorithm_a(arr):
    for i in arr:        # Runs n times
        process(i)       # Takes 1ms

def algorithm_b(arr):
    for i in arr:        # Runs n times
        slow_process(i)  # Takes 100ms
```

Big O focuses on **growth rate**, not absolute performance. For small n, constants matter. For large n, growth rate dominates.

---

## Common Complexity Classes

### Complexity Hierarchy

**Fastest → Slowest**:
```
O(1) < O(log log n) < O(log n) < O(√n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!)
```

### Visual Comparison

For n = 1000:
| Complexity | Operations | Practical Meaning |
|------------|-----------|-------------------|
| O(1) | 1 | Instant |
| O(log n) | ~10 | Extremely fast |
| O(n) | 1,000 | Fast |
| O(n log n) | ~10,000 | Acceptable |
| O(n²) | 1,000,000 | Slow for large n |
| O(2ⁿ) | 10³⁰⁰+ | Computationally infeasible |
| O(n!) | Astronomical | Impossible for n > 20 |

### Growth Rate Chart

```
Time (operations)
      ↑
      |                                                       n!
      |                                                    /
10⁶   |                                              2ⁿ  /
      |                                            /   /
      |                                      n³  /   /
10⁴   |                                    /   /   /
      |                              n²  /   /   /
      |                            /   /   /   /
10²   |                    n log n   /   /   /
      |            n    /           /   /   /
      |         /      /           /   /   /
  1   |    log n     /           /   /   /
      |____________________________________→ n (input size)
          10²      10⁴      10⁶
```

---

## Time Complexity

### Constant Time: O(1)

**Definition**: Runtime doesn't depend on input size.

**Examples**:
```python
# Array access
def get_first(arr):
    return arr[0]  # O(1)

# Hash map lookup
def get_value(hash_map, key):
    return hash_map[key]  # O(1) average case

# Arithmetic operations
def add_numbers(a, b):
    return a + b  # O(1)
```

**Real-world**:
- Accessing array element by index
- Inserting/deleting at head of linked list
- Push/pop on stack
- Hash table operations (average case)

---

### Logarithmic Time: O(log n)

**Definition**: Runtime increases logarithmically with input size. Typically involves dividing problem in half repeatedly.

**Intuition**: If you double the input size, you only add one more operation.

**Examples**:
```python
# Binary search
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1  # O(log n)

# Finding element in balanced BST
def find_in_bst(root, val):
    if not root or root.val == val:
        return root

    if val < root.val:
        return find_in_bst(root.left, val)
    else:
        return find_in_bst(root.right, val)  # O(log n)
```

**Why log n?**
- Each step eliminates half the remaining elements
- n → n/2 → n/4 → n/8 → ... → 1
- Number of divisions until reaching 1: log₂(n)

**Real-world**:
- Binary search in sorted array
- Operations on balanced trees (BST, AVL, Red-Black)
- Finding element in heap
- Certain divide-and-conquer algorithms

---

### Linear Time: O(n)

**Definition**: Runtime scales linearly with input size.

**Examples**:
```python
# Linear search
def linear_search(arr, target):
    for i, val in enumerate(arr):  # Visits each element once
        if val == target:
            return i
    return -1  # O(n)

# Sum array
def sum_array(arr):
    total = 0
    for num in arr:  # O(n)
        total += num
    return total

# Find maximum
def find_max(arr):
    max_val = arr[0]
    for num in arr:  # O(n)
        if num > max_val:
            max_val = num
    return max_val
```

**Real-world**:
- Traversing array/linked list
- Linear search
- Finding min/max in unsorted array
- Checking if array contains duplicates (single pass with hash set)

---

### Linearithmic Time: O(n log n)

**Definition**: Combination of linear and logarithmic growth. Common in efficient sorting algorithms.

**Intuition**: Divide and conquer with linear work at each level.

**Examples**:
```python
# Merge sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])      # T(n/2)
    right = merge_sort(arr[mid:])     # T(n/2)

    return merge(left, right)         # O(n) work

# Quick sort (average case)
def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]    # O(n)
    middle = [x for x in arr if x == pivot]  # O(n)
    right = [x for x in arr if x > pivot]    # O(n)

    return quick_sort(left) + middle + quick_sort(right)
```

**Why n log n?**
- Recursive tree has log n levels (each level divides by 2)
- Each level does O(n) work
- Total: O(n) × O(log n) = O(n log n)

**Real-world**:
- Merge sort, heap sort, quick sort (average)
- Building heap from array
- Sorting-based algorithms
- Many divide-and-conquer algorithms

---

### Quadratic Time: O(n²)

**Definition**: Runtime proportional to the square of input size. Often involves nested loops.

**Examples**:
```python
# Bubble sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):           # Outer loop: n times
        for j in range(n - i - 1):  # Inner loop: ~n times
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr  # O(n²)

# Check for duplicates (naive)
def has_duplicate(arr):
    for i in range(len(arr)):         # n times
        for j in range(i + 1, len(arr)):  # ~n times
            if arr[i] == arr[j]:
                return True
    return False  # O(n²)

# Matrix multiplication (naive)
def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]

    for i in range(n):        # n times
        for j in range(n):    # n times
            for k in range(n):  # n times → Actually O(n³)
                C[i][j] += A[i][k] * B[k][j]

    return C
```

**Real-world**:
- Bubble sort, selection sort, insertion sort
- Checking all pairs in array
- Simple nested loop algorithms
- Naive string matching

---

### Cubic Time: O(n³)

**Definition**: Runtime proportional to the cube of input size. Often three nested loops.

**Examples**:
```python
# Floyd-Warshall (all-pairs shortest path)
def floyd_warshall(graph):
    n = len(graph)
    dist = [row[:] for row in graph]

    for k in range(n):           # n times
        for i in range(n):       # n times
            for j in range(n):   # n times → O(n³)
                dist[i][j] = min(dist[i][j],
                                 dist[i][k] + dist[k][j])

    return dist

# Matrix multiplication (naive)
def matrix_mult(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            for k in range(n):  # Three nested loops → O(n³)
                C[i][j] += A[i][k] * B[k][j]

    return C
```

**Real-world**:
- Floyd-Warshall algorithm
- Naive matrix multiplication
- Checking all triplets in dataset
- Some graph algorithms

---

### Exponential Time: O(2ⁿ)

**Definition**: Runtime doubles with each additional input element. Extremely slow for large n.

**Examples**:
```python
# Naive Fibonacci (recursive)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)  # O(2ⁿ)

# Generate all subsets
def subsets(arr):
    if not arr:
        return [[]]

    first = arr[0]
    rest_subsets = subsets(arr[1:])

    # Each element doubles the number of subsets
    return rest_subsets + [[first] + s for s in rest_subsets]  # O(2ⁿ)

# Traveling salesman (brute force)
def tsp_brute_force(graph):
    # Try all n! permutations
    # Actually O(n!), even worse than O(2ⁿ)
    pass
```

**Why 2ⁿ?**
- Each recursive call makes 2 more calls
- Creates binary tree of depth n
- Total nodes in tree: 2⁰ + 2¹ + 2² + ... + 2ⁿ = 2ⁿ⁺¹ - 1 ≈ O(2ⁿ)

**Real-world**:
- Brute force subset generation
- Naive recursive Fibonacci
- Solving NP-complete problems without optimization
- Backtracking without pruning

**Practical Limits**:
- n = 20: ~1 million operations (feasible)
- n = 30: ~1 billion operations (slow)
- n = 40: ~1 trillion operations (infeasible)

---

### Factorial Time: O(n!)

**Definition**: Runtime factorial with input size. Only feasible for very small n.

**Examples**:
```python
# Generate all permutations
def permutations(arr):
    if len(arr) <= 1:
        return [arr]

    result = []
    for i in range(len(arr)):
        rest = arr[:i] + arr[i+1:]
        for p in permutations(rest):
            result.append([arr[i]] + p)

    return result  # O(n!)

# Traveling salesman (brute force)
def tsp_brute(cities):
    min_cost = float('inf')

    # Try all n! permutations
    for perm in permutations(cities):
        cost = calculate_tour_cost(perm)
        min_cost = min(min_cost, cost)

    return min_cost  # O(n!)
```

**Why n!?**
- n choices for first element
- (n-1) choices for second
- (n-2) choices for third
- ...
- Total: n × (n-1) × (n-2) × ... × 1 = n!

**Practical Limits**:
- n = 10: 3,628,800 operations (feasible)
- n = 15: ~1.3 trillion operations (very slow)
- n = 20: ~2.4 × 10¹⁸ operations (impossible)

**Real-world**:
- Brute force TSP
- Generating all permutations
- Brute force subset sum
- Certain backtracking problems

---

## Space Complexity

Space complexity measures **additional memory** used by an algorithm, excluding input.

### Common Space Complexities

| Complexity | Description | Example |
|------------|-------------|---------|
| O(1) | Constant space | Variables, pointers |
| O(log n) | Logarithmic space | Balanced tree recursion |
| O(n) | Linear space | Array copy, hash map |
| O(n²) | Quadratic space | 2D matrix |

### Examples

```python
# O(1) space
def sum_array(arr):
    total = 0  # Single variable
    for num in arr:
        total += num
    return total

# O(n) space
def reverse_array(arr):
    return arr[::-1]  # Creates new array

# O(n) recursive space (call stack)
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)  # n stack frames

# O(log n) space
def binary_search_recursive(arr, target, left, right):
    if left > right:
        return -1

    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)
    # log n recursive calls on stack
```

---

## Best, Average, and Worst Case

Most algorithms have different performance depending on input.

### Quick Sort Example

```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + [pivot] + quick_sort(right)
```

**Best Case**: O(n log n)
- Pivot always splits array in half
- Example: [5, 3, 7, 1, 9] with median pivot

**Average Case**: O(n log n)
- Random pivot selection
- Expected balanced splits

**Worst Case**: O(n²)
- Pivot is always smallest/largest
- Example: [1, 2, 3, 4, 5] with first element as pivot
- Degenerates to selection sort

### When Each Matters

- **Best Case**: Rarely useful (optimistic scenario)
- **Average Case**: Most practical (expected performance)
- **Worst Case**: Important for guarantees (Big O typically describes this)

---

## Amortized Analysis

**Amortized complexity**: Average time per operation over a sequence of operations.

### Dynamic Array Example

```python
class DynamicArray:
    def __init__(self):
        self.arr = [None] * 1
        self.size = 0
        self.capacity = 1

    def append(self, item):
        if self.size == self.capacity:
            self._resize()  # O(n) occasionally

        self.arr[self.size] = item
        self.size += 1

    def _resize(self):
        self.capacity *= 2
        new_arr = [None] * self.capacity
        for i in range(self.size):
            new_arr[i] = self.arr[i]
        self.arr = new_arr
```

**Analysis**:
- Most appends: O(1)
- Resize happens at powers of 2: O(n)
- Over n operations: 1 + 2 + 4 + 8 + ... + n = 2n - 1
- Amortized: O(2n - 1) / n = O(1) per operation

**Key Insight**: Expensive operations are rare enough that average cost remains low.

---

## Master Theorem

For analyzing divide-and-conquer recursions of the form:
```
T(n) = a · T(n/b) + f(n)
```

Where:
- `a` = number of recursive calls
- `n/b` = size of each subproblem
- `f(n)` = cost of work outside recursion

### Three Cases

**Case 1**: If `f(n) = O(n^c)` where `c < log_b(a)`
→ `T(n) = Θ(n^log_b(a))`

**Case 2**: If `f(n) = Θ(n^c log^k(n))` where `c = log_b(a)`
→ `T(n) = Θ(n^c log^(k+1)(n))`

**Case 3**: If `f(n) = Ω(n^c)` where `c > log_b(a)`
→ `T(n) = Θ(f(n))`

### Examples

**Merge Sort**:
```
T(n) = 2T(n/2) + O(n)
a = 2, b = 2, f(n) = O(n)
log_2(2) = 1, so f(n) = Θ(n^1)
→ Case 2: T(n) = Θ(n log n)
```

**Binary Search**:
```
T(n) = T(n/2) + O(1)
a = 1, b = 2, f(n) = O(1)
log_2(1) = 0, so f(n) = Θ(n^0)
→ Case 2: T(n) = Θ(log n)
```

---

## Complexity Decision Tree

```
How to choose the right complexity:

START
  │
  ├─ Single operation? ──→ O(1)
  │
  ├─ Divide problem in half repeatedly? ──→ O(log n)
  │
  ├─ Visit each element once? ──→ O(n)
  │
  ├─ Divide and conquer with linear work? ──→ O(n log n)
  │
  ├─ Nested loops over all elements? ──→ O(n²) or O(n³)
  │
  ├─ Generate all subsets? ──→ O(2ⁿ)
  │
  └─ Generate all permutations? ──→ O(n!)
```

---

## Practical Examples

### Example 1: Two Sum

**Problem**: Find two numbers in array that sum to target.

**Approach 1 - Brute Force**: O(n²)
```python
def two_sum_brute(arr, target):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] + arr[j] == target:
                return [i, j]
    return None
```

**Approach 2 - Hash Map**: O(n)
```python
def two_sum_optimal(arr, target):
    seen = {}
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return None
```

### Example 2: Finding Duplicates

**Approach 1 - Nested Loops**: O(n²)
```python
def has_duplicate_slow(arr):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False
```

**Approach 2 - Sorting**: O(n log n)
```python
def has_duplicate_sort(arr):
    arr.sort()
    for i in range(len(arr) - 1):
        if arr[i] == arr[i + 1]:
            return True
    return False
```

**Approach 3 - Hash Set**: O(n)
```python
def has_duplicate_optimal(arr):
    seen = set()
    for num in arr:
        if num in seen:
            return True
        seen.add(num)
    return False
```

---

## Common Pitfalls

### 1. Ignoring Hidden Loops

```python
# Looks like O(n) but actually O(n²)
def bad_concatenation(arr):
    result = ""
    for item in arr:
        result += str(item)  # String concat is O(n) in Python!
    return result

# Correct: O(n)
def good_concatenation(arr):
    return "".join(str(item) for item in arr)
```

### 2. Confusing Space Complexity

```python
# O(1) time, O(1) space (in-place)
def reverse_in_place(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

# O(1) time, O(n) space (creates new array)
def reverse_copy(arr):
    return arr[::-1]
```

### 3. Amortized vs Worst Case

```python
# Dynamic array append:
# - Amortized: O(1)
# - Worst case single operation: O(n)

arr = []
arr.append(1)  # Could trigger resize: O(n) worst case
```

---

## Optimization Strategies

### 1. Choose Better Data Structures

| Operation | Array | Hash Set | BST |
|-----------|-------|----------|-----|
| Search | O(n) | O(1) | O(log n) |
| Insert | O(1)* | O(1) | O(log n) |
| Delete | O(n) | O(1) | O(log n) |

### 2. Avoid Unnecessary Work

```python
# Bad: O(n²)
def count_unique_bad(arr):
    unique = []
    for item in arr:
        if item not in unique:  # O(n) lookup
            unique.append(item)
    return len(unique)

# Good: O(n)
def count_unique_good(arr):
    return len(set(arr))  # O(1) lookup in set
```

### 3. Use Memoization

```python
# Without memoization: O(2ⁿ)
def fib_slow(n):
    if n <= 1:
        return n
    return fib_slow(n - 1) + fib_slow(n - 2)

# With memoization: O(n)
def fib_fast(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n

    memo[n] = fib_fast(n - 1, memo) + fib_fast(n - 2, memo)
    return memo[n]
```

### 4. Early Termination

```python
# Can short-circuit when found
def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i  # Early exit!
    return -1
```

---

## Summary

| Complexity | Name | Example | When n = 1M |
|------------|------|---------|-------------|
| O(1) | Constant | Hash table lookup | 1 op |
| O(log n) | Logarithmic | Binary search | ~20 ops |
| O(n) | Linear | Array scan | 1M ops |
| O(n log n) | Linearithmic | Merge sort | ~20M ops |
| O(n²) | Quadratic | Bubble sort | 1T ops |
| O(2ⁿ) | Exponential | Naive Fibonacci | Impossible |
| O(n!) | Factorial | All permutations | Impossible |

**Key Takeaways**:
1. Big O describes growth rate, not absolute performance
2. Focus on worst-case unless specified otherwise
3. Space-time tradeoffs are common
4. Better algorithms > micro-optimizations
5. O(n log n) is often the best we can do for comparison-based sorting

---

**Next**: [LEARNING_PATH.md](./LEARNING_PATH.md) | [API_REFERENCE.md](./API_REFERENCE.md)

**[⬆ Back to Main README](./README.md)**
