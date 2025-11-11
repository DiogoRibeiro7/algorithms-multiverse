# Dijkstra's Algorithm Performance Comparison

Comprehensive benchmarking tool comparing Binary Heap vs Fibonacci Heap implementations of Dijkstra's shortest path algorithm.

## Features

- **Two Complete Heap Implementations**
  - Binary Heap: O(log n) insert, extract-min, decrease-key
  - Fibonacci Heap: O(1) amortized insert/decrease-key, O(log n) extract-min

- **Dijkstra's Algorithm Variants**
  - Binary Heap implementation
  - Fibonacci Heap implementation
  - Side-by-side comparison on identical graphs

- **Statistical Analysis**
  - Mean, median, standard deviation
  - Min/max execution times
  - 95% confidence intervals
  - Multiple trials for statistical significance

- **Graph Generation**
  - Dense graphs (controllable density)
  - Sparse graphs (grid-based structure)
  - Random weighted edges

- **Performance Metrics**
  - Execution time measurements
  - Heap operation counts
  - Decrease-key operation counts
  - Theoretical vs actual complexity analysis

- **CSV Output**
  - Summary statistics for each configuration
  - Individual trial data for detailed analysis
  - Ready for visualization with plotting tools

## Compilation

```bash
gcc -O3 -o compare_dijkstra compare_dijkstra.c -lm
```

**Compiler flags:**
- `-O3`: Maximum optimization
- `-lm`: Link math library (for logarithm and square root functions)

## Usage

### Run Comprehensive Benchmark

Tests multiple graph sizes (100, 200, 500, 1000, 2000 vertices) with both dense and sparse configurations:

```bash
./compare_dijkstra
```

This will:
1. Run 10 trials for each configuration
2. Print detailed statistics to console
3. Generate CSV files with results

### Custom Graph Test

Test a specific graph configuration:

```bash
./compare_dijkstra <vertices> <edges>
```

**Example:**
```bash
./compare_dijkstra 500 50000
```

## Output Files

### dijkstra_results.csv

Summary statistics for each test configuration:

| Column | Description |
|--------|-------------|
| heap_type | Binary Heap or Fibonacci Heap |
| num_vertices | Number of vertices in graph |
| num_edges | Number of edges in graph |
| density | Graph density (edges / possible edges) |
| mean_time_ms | Mean execution time |
| std_dev_ms | Standard deviation |
| median_ms | Median execution time |
| min_ms | Minimum execution time |
| max_ms | Maximum execution time |
| conf_lower_ms | Lower bound of 95% confidence interval |
| conf_upper_ms | Upper bound of 95% confidence interval |
| heap_operations | Total heap operations |
| decrease_key_ops | Number of decrease-key operations |
| theoretical_complexity | Theoretical operation count |

### dijkstra_trials.csv

Individual trial data for detailed analysis:

| Column | Description |
|--------|-------------|
| heap_type | Binary Heap or Fibonacci Heap |
| num_vertices | Number of vertices |
| trial | Trial number (1-10) |
| time_ms | Execution time for this trial |

## Understanding the Results

### Theoretical Complexity

**Binary Heap:**
- Time: O((V + E) log V)
- Space: O(V)
- Each decrease-key: O(log V)

**Fibonacci Heap:**
- Time: O(E + V log V)
- Space: O(V)
- Amortized decrease-key: O(1)

### When Binary Heap is Faster

Binary heaps often perform better in practice despite worse theoretical complexity:
1. Better cache locality (array-based)
2. Lower constant factors
3. Simpler operations
4. Less memory overhead

### When Fibonacci Heap is Faster

Fibonacci heaps excel when:
1. Graph is very dense (E >> V log V)
2. Many decrease-key operations
3. Theoretical guarantees are important
4. Working with very large graphs

### Performance Ratio Analysis

The tool compares:
- **Theoretical ratio**: (V+E)log V / (E + V log V)
- **Actual ratio**: Binary heap time / Fibonacci heap time

Large differences indicate:
- Implementation quality differences
- Cache effects
- Constant factor overhead
- Memory access patterns

## Example Output

```
================================================================================
DENSE GRAPH: V=1000
================================================================================
Running Binary Heap (V=1000, E=299700)...
  Trial 1: 45.234000 ms
  Trial 2: 44.987000 ms
  ...

Running Fibonacci Heap (V=1000, E=299700)...
  Trial 1: 52.123000 ms
  Trial 2: 51.890000 ms
  ...

================================================================================
COMPARISON SUMMARY
================================================================================

Graph Properties:
  Vertices: 1000
  Edges:    299700
  Density:  0.2999

Binary Heap:
  Mean:       45.123000 ms
  Std Dev:    0.234000 ms
  Median:     45.100000 ms
  Min:        44.890000 ms
  Max:        45.500000 ms
  95% CI:     [44.956000, 45.290000] ms

Fibonacci Heap:
  Mean:       52.001000 ms
  Std Dev:    0.456000 ms
  Median:     51.980000 ms
  Min:        51.234000 ms
  Max:        52.890000 ms
  95% CI:     [51.674000, 52.328000] ms

Heap Operations:
  Binary Heap:
    Total ops:        598700
    Decrease-key ops: 298700
  Fibonacci Heap:
    Total ops:        598700
    Decrease-key ops: 298700

Performance:
  Speedup: 1.15x (Binary faster)

Theoretical Complexity:
  Binary Heap:    O((V+E)log V) = O(2989700)
  Fibonacci Heap: O(E + V log V) = O(309700)

Theoretical vs Actual:
  Theoretical ratio: 9.65
  Actual ratio:      1.15
  Difference:        87.95%
```

## Visualization

Use the CSV output files with Python/R/Excel to create:

1. **Performance comparison charts**
   - Time vs graph size
   - Binary vs Fibonacci speedup

2. **Statistical box plots**
   - Distribution of execution times
   - Confidence intervals

3. **Operation count analysis**
   - Theoretical vs actual operations
   - Decrease-key operation impact

### Example Python Visualization

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load results
df = pd.read_csv('dijkstra_results.csv')

# Plot execution time vs vertices
fig, ax = plt.subplots(figsize=(10, 6))
for heap_type in df['heap_type'].unique():
    data = df[df['heap_type'] == heap_type]
    ax.errorbar(data['num_vertices'], data['mean_time_ms'],
                yerr=data['std_dev_ms'], label=heap_type,
                marker='o', capsize=5)

ax.set_xlabel('Number of Vertices')
ax.set_ylabel('Execution Time (ms)')
ax.set_title('Dijkstra Performance: Binary vs Fibonacci Heap')
ax.legend()
ax.grid(True, alpha=0.3)
plt.savefig('dijkstra_comparison.png', dpi=300, bbox_inches='tight')
```

## Implementation Notes

### Binary Heap

- Array-based implementation
- Parent at index (i-1)/2
- Children at indices 2i+1 and 2i+2
- Position tracking for O(1) vertex lookup
- Heapify up/down for maintaining heap property

### Fibonacci Heap

- Lazy consolidation strategy
- Circular doubly-linked lists
- Cascading cuts for amortized bounds
- Marked nodes for efficiency
- Consolidate on extract-min only

### Graph Representation

- Adjacency list for efficiency
- Random weighted edges (1-100)
- Dense: user-controlled density
- Sparse: grid-based connectivity (O(V) edges)

## Benchmarking Methodology

1. **Multiple Trials**: 10 runs per configuration for statistical significance
2. **Identical Graphs**: Same graph instance for both heap types
3. **Warm-up**: First extraction discarded (not implemented, could add)
4. **Clock Resolution**: Uses `clock()` for timing (microsecond precision)
5. **Operation Counting**: Tracks all heap operations for analysis

## Limitations

1. **Clock Precision**: Limited by system clock granularity
2. **No Process Isolation**: Other processes may affect timing
3. **Memory Effects**: No explicit cache warming
4. **Graph Size**: Limited by available memory
5. **Fixed Trial Count**: 10 trials may be insufficient for very fast operations

## Future Enhancements

- [ ] Pairing heap implementation
- [ ] Multi-threaded benchmarking
- [ ] Memory usage profiling
- [ ] Cache miss analysis
- [ ] Various graph types (planar, scale-free, etc.)
- [ ] Visualization generation built-in
- [ ] JSON output format
- [ ] Configurable trial count
- [ ] Process affinity settings

## References

1. Fredman, M. L., & Tarjan, R. E. (1987). Fibonacci heaps and their uses in improved network optimization algorithms. *Journal of the ACM*, 34(3), 596-615.

2. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.

3. Dijkstra, E. W. (1959). A note on two problems in connexion with graphs. *Numerische mathematik*, 1(1), 269-271.

## License

This benchmark is part of the Applied Papers Lab project.
