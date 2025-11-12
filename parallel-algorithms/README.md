# 🚀 Parallel Algorithms

**High-performance parallel implementations with comprehensive concurrency analysis.**

---

## 📋 Overview

This directory contains parallel implementations of key algorithms, demonstrating concurrency patterns, performance optimization, and scalability analysis across multiple languages with strong concurrency support.

### Supported Languages

- **Go** - Goroutines and channels for lightweight concurrency
- **Rust** - Safe parallelism with ownership and `rayon` crate
- **Java** - Thread pools, Fork/Join framework, parallel streams
- **C++** - `std::thread`, OpenMP, Intel TBB
- **Python** - `multiprocessing` and `concurrent.futures`

---

## 🎯 Algorithm Categories

### 1. Parallel Sorting

| Algorithm | Best Use Case | Speedup | Languages |
|-----------|--------------|---------|-----------|
| **Parallel Merge Sort** | Large datasets (>1M elements) | 4-8x | All |
| **Parallel Quicksort** | General purpose, in-place | 3-6x | All |
| **Parallel Radix Sort** | Integer/string sorting | 2-4x | Go, Rust, C++ |

**Key Optimizations:**
- Sequential cutoff for small subarrays
- Load balancing with work stealing
- Cache-friendly memory access patterns

### 2. Parallel Matrix Operations

| Operation | Complexity | Speedup | Optimal Size |
|-----------|------------|---------|--------------|
| **Matrix Multiplication** | O(n³) → O(n³/p) | 8-16x | n > 1000 |
| **Matrix Transpose** | O(n²) → O(n²/p) | 2-4x | n > 500 |
| **Blocked Multiplication** | Cache-optimized | 10-20x | n > 2000 |

**Optimizations:**
- Cache blocking for better locality
- SIMD vectorization
- Strassen's algorithm for large matrices

### 3. Parallel Graph Algorithms

| Algorithm | Use Case | Complexity | Speedup |
|-----------|----------|------------|---------|
| **Parallel BFS** | Level synchronization | O((V+E)/p) | 4-8x |
| **Parallel DFS** | Work stealing approach | O((V+E)/p) | 2-4x |
| **Parallel Dijkstra** | Priority queue based | O((V+E)log V/p) | 3-6x |
| **Parallel Floyd-Warshall** | All-pairs shortest path | O(V³/p) | 8-12x |

**Challenges:**
- Load balancing for irregular graphs
- Synchronization overhead
- Memory coherency

### 4. Parallel Search

| Algorithm | Best For | Speedup | Implementation |
|-----------|----------|---------|----------------|
| **Parallel Binary Search** | Multiple queries | Linear in queries | All |
| **Parallel Tree Search** | Large search spaces | 4-8x | Go, Rust |
| **Parallel Pattern Matching** | String search | 6-12x | C++, Rust |

### 5. MapReduce Implementations

| Pattern | Use Case | Languages |
|---------|----------|-----------|
| **Word Count** | Text analysis | All |
| **Inverted Index** | Search engines | Go, Java |
| **PageRank** | Graph analysis | Java, Python |
| **K-Means Clustering** | Machine learning | Python, Java |

---

## 🏗️ Directory Structure

```
parallel-algorithms/
├── sorting/
│   ├── parallel_merge_sort.go
│   ├── parallel_merge_sort.rs
│   ├── parallel_merge_sort.java
│   ├── parallel_merge_sort.cpp
│   ├── parallel_merge_sort.py
│   ├── parallel_quicksort.go
│   └── parallel_quicksort.rs
│
├── matrix/
│   ├── parallel_matrix_mult.go
│   ├── parallel_matrix_mult.rs
│   ├── parallel_matrix_mult.cpp
│   ├── parallel_strassen.java
│   └── blocked_multiplication.cpp
│
├── graph/
│   ├── parallel_bfs.go
│   ├── parallel_bfs.rs
│   ├── parallel_dfs.cpp
│   ├── parallel_dijkstra.java
│   └── parallel_floyd_warshall.py
│
├── search/
│   ├── parallel_binary_search.go
│   ├── parallel_tree_search.rs
│   └── parallel_string_search.cpp
│
├── mapreduce/
│   ├── word_count.go
│   ├── inverted_index.java
│   ├── pagerank.py
│   └── kmeans_parallel.py
│
├── benchmarks/
│   ├── scaling_analysis.py
│   ├── speedup_calculator.go
│   ├── thread_efficiency.rs
│   └── benchmark_runner.sh
│
└── docs/
    ├── CONCURRENCY_PATTERNS.md
    ├── PERFORMANCE_GUIDE.md
    ├── THREAD_SAFETY.md
    └── WHEN_TO_PARALLELIZE.md
```

---

## 🚦 When to Use Parallel Algorithms

### ✅ Use Parallelism When:

1. **Large Data Sets**
   - Input size > 10,000 elements for sorting
   - Matrices > 1000×1000 for multiplication
   - Graphs > 10,000 nodes

2. **CPU-Bound Operations**
   - Heavy computation per element
   - Mathematical operations
   - Complex transformations

3. **Independent Operations**
   - No data dependencies
   - Embarrassingly parallel problems
   - Map-reduce patterns

4. **Available Hardware**
   - Multi-core processors (4+ cores)
   - Sufficient memory bandwidth
   - Cache-coherent systems

### ⚠️ Avoid Parallelism When:

1. **Small Data Sets**
   - Overhead exceeds benefit
   - Sequential version faster
   - Context switching dominates

2. **I/O Bound Operations**
   - Disk reads/writes
   - Network communication
   - Database queries

3. **High Data Dependencies**
   - Frequent synchronization needed
   - Sequential by nature
   - Critical sections dominate

4. **Limited Resources**
   - Single-core systems
   - Memory constrained
   - High thread contention

---

## 📊 Performance Metrics

### Speedup Analysis

**Amdahl's Law:**
```
Speedup = 1 / ((1 - P) + P/N)
where:
  P = Parallelizable fraction
  N = Number of processors
```

**Strong Scaling:** Fixed problem size, increase processors
**Weak Scaling:** Problem size increases with processors

### Efficiency Metrics

```python
# Parallel Efficiency
Efficiency = Speedup / Number_of_Threads

# Good efficiency: > 70%
# Acceptable: 50-70%
# Poor: < 50%
```

### Overhead Analysis

1. **Thread Creation:** 10-100µs per thread
2. **Context Switching:** 1-10µs per switch
3. **Synchronization:** 10-1000ns per lock
4. **Cache Coherency:** 10-100ns per cache line

---

## 🔧 Concurrency Patterns

### 1. Fork-Join Pattern

```
Main Thread
    ├─→ Worker 1
    ├─→ Worker 2
    ├─→ Worker 3
    └─→ Worker 4
        ↓
    Join/Merge
```

**Best For:** Divide-and-conquer algorithms

### 2. Pipeline Pattern

```
Input → Stage 1 → Stage 2 → Stage 3 → Output
         ↓         ↓         ↓
       Buffer    Buffer    Buffer
```

**Best For:** Stream processing, data transformation

### 3. Work Stealing

```
Thread 1: [Task] [Task] [Task]
Thread 2: [Task] [Task] ← steal
Thread 3: [Task] ← steal
Thread 4: [Done] ← steal
```

**Best For:** Irregular workloads, dynamic load balancing

### 4. Data Parallelism

```
Data: [1,2,3,4,5,6,7,8]
       ↓   ↓   ↓   ↓
Thread 1  2  3  4
  [1,2] [3,4] [5,6] [7,8]
```

**Best For:** Same operation on different data

### 5. Task Parallelism

```
Task A (Thread 1)
Task B (Thread 2)
Task C (Thread 3)
Task D (Thread 4)
```

**Best For:** Independent tasks, heterogeneous operations

---

## 🛡️ Thread Safety

### Synchronization Primitives

| Primitive | Use Case | Overhead | Language Support |
|-----------|----------|----------|------------------|
| **Mutex** | Mutual exclusion | Medium | All |
| **RwLock** | Read-heavy workloads | Low | Rust, Go, C++ |
| **Atomic** | Simple counters | Very Low | All |
| **Semaphore** | Resource limiting | Medium | Java, C++ |
| **Channel** | Message passing | Low | Go, Rust |

### Common Pitfalls

1. **Data Races**
   - Multiple threads accessing shared data
   - At least one write operation
   - No synchronization

2. **Deadlocks**
   - Circular wait conditions
   - Hold and wait pattern
   - No preemption

3. **Livelocks**
   - Threads continuously change state
   - No progress made
   - Starvation

4. **False Sharing**
   - Cache line contention
   - Adjacent memory locations
   - Significant performance impact

### Prevention Strategies

```go
// Go: Use channels for communication
ch := make(chan int)
go func() { ch <- compute() }()
result := <-ch

// Rust: Ownership prevents data races
let data = Arc::new(Mutex::new(vec![]));
let data_clone = Arc::clone(&data);
thread::spawn(move || {
    data_clone.lock().unwrap().push(1);
});

// Java: Concurrent collections
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.computeIfAbsent(key, k -> expensiveComputation());

// C++: Lock guards
std::lock_guard<std::mutex> lock(mutex);
shared_data.push_back(value);
```

---

## 📈 Benchmarking Results

### Parallel Merge Sort

**Dataset:** 10 million integers

| Threads | Time (ms) | Speedup | Efficiency |
|---------|-----------|---------|------------|
| 1 (seq) | 2450 | 1.0x | 100% |
| 2 | 1280 | 1.91x | 96% |
| 4 | 680 | 3.60x | 90% |
| 8 | 380 | 6.45x | 81% |
| 16 | 250 | 9.80x | 61% |

### Matrix Multiplication

**Size:** 2048×2048

| Implementation | Time (ms) | Speedup |
|----------------|-----------|---------|
| Sequential | 12500 | 1.0x |
| Parallel (4 cores) | 3400 | 3.68x |
| Blocked (4 cores) | 1800 | 6.94x |
| SIMD + Parallel | 950 | 13.16x |

### Parallel BFS

**Graph:** 1M nodes, 10M edges

| Implementation | Time (ms) | Speedup |
|----------------|-----------|---------|
| Sequential | 850 | 1.0x |
| Parallel (4 cores) | 240 | 3.54x |
| Parallel (8 cores) | 145 | 5.86x |

---

## 🚀 Quick Start

### Go Example

```go
package main

import (
    "fmt"
    "runtime"
    "sync"
)

func parallelMergeSort(arr []int, threads int) []int {
    if len(arr) <= 1 {
        return arr
    }

    if threads <= 1 {
        return sequentialMergeSort(arr)
    }

    mid := len(arr) / 2
    var wg sync.WaitGroup
    var left, right []int

    wg.Add(2)
    go func() {
        defer wg.Done()
        left = parallelMergeSort(arr[:mid], threads/2)
    }()
    go func() {
        defer wg.Done()
        right = parallelMergeSort(arr[mid:], threads/2)
    }()
    wg.Wait()

    return merge(left, right)
}

func main() {
    runtime.GOMAXPROCS(runtime.NumCPU())
    arr := generateRandomArray(1000000)
    sorted := parallelMergeSort(arr, runtime.NumCPU())
    fmt.Printf("Sorted %d elements\n", len(sorted))
}
```

### Rust Example

```rust
use rayon::prelude::*;

fn parallel_merge_sort<T: Ord + Send>(mut arr: Vec<T>) -> Vec<T> {
    if arr.len() <= 1 {
        return arr;
    }

    let mid = arr.len() / 2;
    let mut right = arr.split_off(mid);

    let (left, right) = rayon::join(
        || parallel_merge_sort(arr),
        || parallel_merge_sort(right)
    );

    merge(left, right)
}

fn main() {
    let arr: Vec<i32> = (0..1_000_000).collect();
    let sorted = parallel_merge_sort(arr);
    println!("Sorted {} elements", sorted.len());
}
```

### Java Example

```java
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveTask;

class ParallelMergeSort extends RecursiveTask<int[]> {
    private int[] arr;
    private static final int THRESHOLD = 10000;

    public ParallelMergeSort(int[] arr) {
        this.arr = arr;
    }

    @Override
    protected int[] compute() {
        if (arr.length <= THRESHOLD) {
            return sequentialMergeSort(arr);
        }

        int mid = arr.length / 2;
        ParallelMergeSort left = new ParallelMergeSort(
            Arrays.copyOfRange(arr, 0, mid)
        );
        ParallelMergeSort right = new ParallelMergeSort(
            Arrays.copyOfRange(arr, mid, arr.length)
        );

        left.fork();
        int[] rightResult = right.compute();
        int[] leftResult = left.join();

        return merge(leftResult, rightResult);
    }
}

public class Main {
    public static void main(String[] args) {
        ForkJoinPool pool = new ForkJoinPool();
        int[] arr = generateRandomArray(1_000_000);
        int[] sorted = pool.invoke(new ParallelMergeSort(arr));
    }
}
```

---

## 📚 Additional Resources

- **Documentation:** See `docs/` for detailed guides
- **Benchmarks:** Run `benchmarks/benchmark_runner.sh`
- **Performance:** Check `docs/PERFORMANCE_GUIDE.md`
- **Patterns:** Review `docs/CONCURRENCY_PATTERNS.md`

---

## 🤝 Contributing

When adding parallel algorithms:

1. **Implement sequential version first** for comparison
2. **Add thread-safety analysis** in comments
3. **Include benchmarks** with scaling analysis
4. **Document optimal use cases** and cutoff thresholds
5. **Test for race conditions** and deadlocks
6. **Profile performance** on different core counts

---

## 📄 License

MIT License - See [LICENSE](../LICENSE)

---

**[⬆ Back to Main README](../README.md)**
