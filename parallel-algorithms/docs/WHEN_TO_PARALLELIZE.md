# When to Parallelize Algorithms

**A comprehensive guide to deciding when parallel algorithms provide benefits.**

---

## 📊 Decision Framework

### The Parallelization Decision Tree

```
Start: Should I parallelize?
    │
    ├─→ Is the problem CPU-bound?
    │       ├─→ No → DON'T PARALLELIZE (I/O bound)
    │       └─→ Yes ↓
    │
    ├─→ Is the dataset large enough?
    │       ├─→ No → DON'T PARALLELIZE (overhead > benefit)
    │       └─→ Yes ↓
    │
    ├─→ Are operations independent?
    │       ├─→ No → Consider pipeline or careful synchronization
    │       └─→ Yes ↓
    │
    ├─→ Do you have multiple cores?
    │       ├─→ No → DON'T PARALLELIZE
    │       └─→ Yes ↓
    │
    └─→ PARALLELIZE! Choose appropriate pattern
```

---

## ✅ When to Parallelize

### 1. Large Data Sets

**Sorting Algorithms:**
```
Merge Sort:  Parallelize if n > 100,000
Quick Sort:  Parallelize if n > 50,000
Radix Sort:  Parallelize if n > 500,000
```

**Matrix Operations:**
```
Matrix Multiplication:  Parallelize if n > 512
Matrix Addition:        Parallelize if n > 2048
Matrix Transpose:       Parallelize if n > 1024
```

**Graph Algorithms:**
```
BFS:          Parallelize if |V| > 10,000
DFS:          Parallelize if |V| > 50,000 (irregular)
Dijkstra:     Parallelize if |V| > 20,000
Connected Components: Parallelize if |V| > 10,000
```

**Search Operations:**
```
Binary Search:  Parallelize for batch queries (>1000)
Linear Search:  Parallelize if n > 1,000,000
Tree Search:    Parallelize for large trees (>100,000 nodes)
```

### 2. Computation-Heavy Operations

#### High Compute-to-Memory Ratio

**Good Candidates:**
- **Image Processing:** Each pixel independently processed
- **Mathematical Simulations:** Monte Carlo methods
- **Cryptography:** Parallel hash computations
- **Machine Learning:** Gradient computations
- **Scientific Computing:** Numerical integration

**Example: Image Blur (3x3 Kernel)**
```
Sequential: 100ms for 1920×1080
Parallel (8 cores): 15ms
Speedup: 6.67x ✓ Excellent
```

#### Mathematical Operations

**Matrix Multiplication (n×n):**
```
Operation count: n³
Memory accesses: n²
Compute-to-memory ratio: n

For n=2048: ~17 billion operations, ~8 million memory accesses
Ratio: ~2000:1 → Excellent for parallelization
```

### 3. Embarrassingly Parallel Problems

**Definition:** Problems with no dependencies between subtasks

**Classic Examples:**

1. **Mandelbrot Set Generation**
   - Each pixel computed independently
   - No communication needed
   - Near-linear scaling

2. **Monte Carlo Simulations**
   - Random sampling
   - Aggregate results at end
   - Perfect for parallelization

3. **Batch Processing**
   - Process images in parallel
   - Convert files
   - Run independent queries

4. **Map Operations**
   - Apply function to each element
   - No shared state
   - Ideal for data parallelism

**Scaling Analysis:**
```
Problem: Apply f(x) to 10M elements
Threads: 8
Expected speedup: ~7.8x (near-linear)
Actual speedup: ~7.5x ✓ Excellent
```

### 4. Available Hardware Resources

**Minimum Recommended Configuration:**

| Algorithm Type | Min Cores | Min RAM | Recommended |
|---------------|-----------|---------|-------------|
| Sorting | 2 | 4GB | 4+ cores, 8GB |
| Matrix Ops | 4 | 8GB | 8+ cores, 16GB |
| Graph Algorithms | 4 | 8GB | 8+ cores, 32GB |
| MapReduce | 4 | 16GB | 16+ cores, 64GB |

**Memory Bandwidth Considerations:**

```python
# Check if memory-bound
memory_bandwidth = 25.6  # GB/s (DDR4-3200)
data_size = 8  # GB
processing_time = 0.1  # seconds per element

memory_time = data_size / memory_bandwidth  # 0.31s
compute_time = processing_time * len(data)  # varies

if memory_time > compute_time:
    print("Memory-bound - limited parallelization benefit")
else:
    print("Compute-bound - good parallelization potential")
```

---

## ⚠️ When NOT to Parallelize

### 1. Small Data Sets

**The Overhead Problem:**

```
Thread creation overhead: ~50µs per thread
Context switch overhead: ~5µs per switch
Synchronization overhead: ~100ns per lock

For small n, overhead > actual work!
```

**Break-Even Analysis:**

```python
# Sequential time
T_seq = n * operation_time

# Parallel time
T_par = thread_overhead + (n * operation_time) / num_threads + sync_overhead

# Break-even point
n_breakeven = (thread_overhead + sync_overhead) /
              (operation_time * (1 - 1/num_threads))
```

**Real Example: Sorting 1000 elements**
```
Sequential: 0.05ms
Parallel (4 threads): 0.25ms
Result: 5x SLOWER! ✗
```

**Cutoff Thresholds (Empirical):**

| Algorithm | Sequential Cutoff | Reason |
|-----------|------------------|---------|
| Merge Sort | 10,000-50,000 | Thread overhead |
| Quicksort | 5,000-20,000 | Partition imbalance |
| Matrix Mult | 512×512 | Cache efficiency |
| BFS | 1,000 nodes | Graph structure |

### 2. I/O-Bound Operations

**Characteristics:**
- Waiting for disk/network
- Database queries
- File operations
- Network requests

**Why Parallelization Doesn't Help:**

```
Problem: Read 100 files from disk

Sequential: Limited by disk I/O (100 MB/s)
Time: (100 files × 10MB) / 100 MB/s = 10s

Parallel (4 threads): Still limited by same disk!
Time: ~10s (no improvement, maybe worse due to seeking)

Better solution: Async I/O, not parallelism
```

**Exception:** Multiple disks or network connections
```
4 separate disks: Can achieve ~4x speedup
4 network connections: Can improve throughput
```

### 3. High Synchronization Overhead

**Amdahl's Law Impact:**

```
Speedup = 1 / (S + P/N)
where:
  S = Serial fraction (including synchronization)
  P = Parallel fraction
  N = Number of threads
```

**Example: 50% Synchronization**
```
With 8 cores:
Max speedup = 1 / (0.5 + 0.5/8) = 1.6x only!

Not worth the complexity!
```

**High-Contention Scenarios:**

1. **Shared Counter Updates**
   ```cpp
   // Every thread needs to update
   std::atomic<int> counter;
   for (auto& item : data) {
       counter++;  // Contention!
   }
   ```

2. **Fine-Grained Locking**
   ```java
   // Lock on every operation
   synchronized(lock) {
       map.put(key, value);  // Bottleneck!
   }
   ```

3. **Producer-Consumer with Small Buffer**
   ```go
   ch := make(chan int, 10)  // Small buffer
   // Frequent blocking on channel operations
   ```

### 4. Complex Dependencies

**Sequential by Nature:**

1. **Recursive Dependencies**
   ```
   Fibonacci: F(n) = F(n-1) + F(n-2)
   Each step depends on previous
   Hard to parallelize effectively
   ```

2. **Cumulative Operations**
   ```python
   # Prefix sum
   result[0] = arr[0]
   for i in range(1, n):
       result[i] = result[i-1] + arr[i]  # Dependency chain
   ```

3. **Stateful Algorithms**
   ```
   Graph traversal with specific order
   State machines
   Iterative refinement
   ```

---

## 📈 Performance Prediction

### Calculating Expected Speedup

**1. Identify Parallel Fraction (P)**

```python
def analyze_code(algorithm):
    total_time = profile(algorithm)

    parallelizable_time = 0
    for section in algorithm:
        if section.is_independent():
            parallelizable_time += section.time

    P = parallelizable_time / total_time
    return P
```

**2. Apply Amdahl's Law**

```python
def expected_speedup(P, N):
    """
    P: Parallel fraction (0-1)
    N: Number of processors
    """
    return 1 / ((1 - P) + P / N)

# Examples
print(f"95% parallel, 8 cores: {expected_speedup(0.95, 8):.2f}x")  # 5.93x
print(f"75% parallel, 8 cores: {expected_speedup(0.75, 8):.2f}x")  # 3.05x
print(f"50% parallel, 8 cores: {expected_speedup(0.50, 8):.2f}x")  # 1.60x
```

**3. Factor in Overhead**

```python
def realistic_speedup(P, N, overhead):
    """
    overhead: Fraction of time spent in parallel overhead (0-1)
    """
    ideal = expected_speedup(P, N)
    return ideal / (1 + overhead)

# With 10% overhead
print(f"95% parallel, 8 cores, 10% overhead: "
      f"{realistic_speedup(0.95, 8, 0.1):.2f}x")  # 5.39x
```

### Measuring Actual Performance

**Scaling Analysis Script:**

```python
import time
import multiprocessing as mp

def benchmark_scaling(algorithm, data, max_threads):
    results = []

    # Sequential baseline
    start = time.perf_counter()
    algorithm(data, threads=1)
    sequential_time = time.perf_counter() - start

    # Parallel versions
    for n_threads in [2, 4, 8, 16]:
        if n_threads > max_threads:
            break

        start = time.perf_counter()
        algorithm(data, threads=n_threads)
        parallel_time = time.perf_counter() - start

        speedup = sequential_time / parallel_time
        efficiency = speedup / n_threads * 100

        results.append({
            'threads': n_threads,
            'time': parallel_time,
            'speedup': speedup,
            'efficiency': efficiency
        })

    return results

# Interpret results
def should_use_parallel(results):
    # Good parallelization: efficiency > 70% at 4 cores
    four_core = next(r for r in results if r['threads'] == 4)
    return four_core['efficiency'] > 70
```

---

## 🎯 Algorithm-Specific Guidelines

### Sorting Algorithms

| Algorithm | Parallel Threshold | Expected Speedup | Notes |
|-----------|-------------------|------------------|-------|
| Merge Sort | 100K elements | 4-7x (8 cores) | Excellent load balance |
| Quicksort | 50K elements | 3-5x (8 cores) | Partition imbalance |
| Radix Sort | 500K elements | 2-4x (8 cores) | Memory bandwidth limited |
| Heap Sort | N/A | Poor | Sequential by nature |
| Insertion Sort | N/A | Poor | Small n, sequential |

**Decision Matrix:**
```
n < 10,000:     Use sequential (any algorithm)
10K < n < 100K: Use sequential or simple parallel
n > 100K:       Use parallel merge sort
n > 1M:         Use parallel with careful tuning
```

### Matrix Operations

**Matrix Multiplication (n×n):**

| Size | Sequential | Parallel (4 cores) | Parallel (8 cores) |
|------|-----------|-------------------|-------------------|
| 128 | 2ms | 3ms ✗ | 4ms ✗ |
| 512 | 150ms | 45ms ✓ | 25ms ✓ |
| 1024 | 1.2s | 350ms ✓ | 190ms ✓ |
| 2048 | 9.5s | 2.6s ✓ | 1.4s ✓ |

**Recommendation:**
- n < 256: Sequential
- 256 ≤ n < 512: Consider parallel with blocking
- n ≥ 512: Use parallel
- n ≥ 2048: Use parallel + SIMD + blocking

### Graph Algorithms

**BFS Parallelization:**

```
Graph Properties Impact:

1. Dense graphs (E ≈ V²):
   - Better load balance
   - Good speedup (4-6x with 8 cores)

2. Sparse graphs (E ≈ V):
   - Irregular workload
   - Moderate speedup (2-4x with 8 cores)

3. Scale-free graphs:
   - High variance in degree
   - Poor load balance
   - Limited speedup (1.5-3x with 8 cores)
```

**Cutoff Thresholds:**

| Graph Type | Min Nodes | Expected Speedup |
|------------|-----------|------------------|
| Dense | 5,000 | 4-6x |
| Sparse | 20,000 | 2-4x |
| Trees | 50,000 | 1.5-3x |
| Power-law | 10,000 | 2-3x |

---

## 🔬 Profiling Before Parallelizing

### Step 1: Profile Sequential Version

```python
import cProfile
import pstats

# Profile code
profiler = cProfile.Profile()
profiler.enable()
result = algorithm(data)
profiler.disable()

# Analyze
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)

# Identify hotspots
# Look for functions with:
# 1. High cumulative time
# 2. Low call count (avoid fine-grained parallelism)
# 3. Independent operations
```

### Step 2: Identify Bottlenecks

**CPU-Bound Check:**
```bash
# Linux: Use top or htop
top -p <pid>

# High CPU usage (>90%) → CPU-bound ✓
# Low CPU usage (<50%) → I/O-bound ✗
```

**Memory-Bound Check:**
```python
import psutil

process = psutil.Process()
mem_info = process.memory_info()

# High memory bandwidth usage → Consider cache optimization
# Before further parallelization
```

### Step 3: Estimate Parallel Fraction

```python
def estimate_parallel_fraction(profile_data):
    """
    Analyze profiling data to estimate parallelizable fraction
    """
    total_time = sum(func.total_time for func in profile_data)

    parallel_time = 0
    for func in profile_data:
        if func.is_pure_function() and not func.has_side_effects():
            parallel_time += func.total_time

    return parallel_time / total_time
```

---

## 📋 Checklist: Should I Parallelize?

Use this checklist to make the decision:

- [ ] **Problem is CPU-bound** (not I/O-bound)
- [ ] **Dataset is sufficiently large** (see thresholds above)
- [ ] **Operations are mostly independent** (<20% synchronization)
- [ ] **Multiple cores available** (≥4 cores recommended)
- [ ] **Parallel fraction >75%** (using Amdahl's law)
- [ ] **Expected speedup >2x** (worth the complexity)
- [ ] **Memory bandwidth sufficient** (not memory-bound)
- [ ] **Can handle thread-safety** (no race conditions)
- [ ] **Profiling shows hotspots** (specific areas to parallelize)
- [ ] **Maintenance cost acceptable** (team understands concurrency)

**Decision Rule:**
- ≥8 checks passed: **Parallelize!** ✓
- 5-7 checks passed: **Maybe** - prototype and measure
- <5 checks passed: **Don't parallelize** ✗

---

## 📚 Further Reading

- **Books:**
  - "The Art of Multiprocessor Programming" by Herlihy & Shavit
  - "Programming Massively Parallel Processors" by Kirk & Hwu
  - "Structured Parallel Programming" by McCool, Reinders & Robison

- **Papers:**
  - "Amdahl's Law in the Multicore Era" (Hill & Marty, 2008)
  - "Work-Stealing for Multi-Core Systems" (Leiserson & Blumofe, 1999)

- **Online Resources:**
  - Intel Threading Building Blocks Guide
  - Rust Rayon Documentation
  - Go Concurrency Patterns

---

**Remember:** *Parallelization adds complexity. Only do it when the benefits clearly outweigh the costs!*
