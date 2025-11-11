# Cross-Language Graph Algorithm Benchmarks

This directory contains a comprehensive benchmarking framework for comparing graph algorithm performance across multiple programming languages.

## 📋 Overview

The benchmark framework compares implementations of graph algorithms in:
- **Python** - Full implementation with advanced algorithms
- **JavaScript** - Basic algorithms (Node.js)
- **Java** - Basic algorithms
- **C++** - Basic algorithms with -O3 optimization
- **Go** - Basic algorithms with native compilation
- **Rust** - Coming soon

## 🚀 Quick Start

### Prerequisites

Install language runtimes:
- **Python 3.8+**: https://www.python.org/
- **Node.js 14+**: https://nodejs.org/
- **Java JDK 11+**: https://adoptium.net/
- **Go 1.18+**: https://go.dev/
- **g++ with C++17**: Part of GCC

Install Python visualization dependencies:
```bash
pip install -r requirements_benchmark.txt
```

### Running All Benchmarks

On Unix/Linux/macOS:
```bash
chmod +x run_all_benchmarks.sh
./run_all_benchmarks.sh
```

On Windows (Git Bash or WSL):
```bash
bash run_all_benchmarks.sh
```

### Running Individual Language Benchmarks

**Python:**
```bash
python3 benchmark_py.py
```

**JavaScript:**
```bash
node benchmark_js.js
```

**Java:**
```bash
javac BenchmarkJava.java
java BenchmarkJava
```

**Go:**
```bash
go run benchmark_go.go graph.go
```

**C++:**
```bash
g++ -std=c++17 -O3 -o benchmark_cpp benchmark_cpp.cpp
./benchmark_cpp
```

## 📊 Understanding the Results

### Result Files

Each language produces a JSON result file:
- `results_python.json`
- `results_javascript.json`
- `results_java.json`
- `results_go.json`
- `results_cpp.json`

### Result Format

```json
{
  "name": "DFS_Iterative_Sparse",
  "description": "DFS iterative on sparse graph",
  "language": "Python",
  "algorithm": "dfs_iterative",
  "graph": {
    "vertices": 1000,
    "type": "random",
    "density": 0.05,
    "directed": false,
    "weighted": false
  },
  "trials": 10,
  "successful_trials": 10,
  "status": "success",
  "timing": {
    "mean": 0.00234,
    "median": 0.00231,
    "std_dev": 0.00012,
    "min": 0.00219,
    "max": 0.00256,
    "times": [...]
  }
}
```

### Visualizations

After running `aggregate_results.py`, visualizations are created in `benchmark_results/`:

1. **Performance Comparison Charts** (`comparison_*.png`)
   - Bar charts comparing mean execution time across languages
   - Relative speedup comparison

2. **Algorithm Comparison** (`algorithms_*.png`)
   - Performance of different algorithms within each language

3. **Overall Heatmap** (`heatmap_overall.png`)
   - Heatmap showing all benchmarks vs all languages

4. **Variability Analysis** (`variability_*.png`)
   - Box plots showing timing consistency

5. **Summary Statistics** (`summary_statistics.csv`)
   - Aggregate statistics for all languages

## ⚙️ Configuration

### Benchmark Configuration File

Edit `benchmark_config.json` to add or modify benchmarks:

```json
{
  "benchmarks": [
    {
      "name": "DFS_Iterative_Sparse",
      "description": "DFS iterative on sparse graph",
      "graph": {
        "vertices": 1000,
        "type": "random",
        "density": 0.05,
        "directed": false,
        "weighted": false
      },
      "algorithm": "dfs_iterative",
      "start_vertex": 0,
      "trials": 10
    }
  ]
}
```

### Supported Algorithms

**Basic Algorithms** (all languages except Rust):
- `dfs_iterative` - Depth-First Search (iterative)
- `dfs_recursive` - Depth-First Search (recursive)
- `bfs` - Breadth-First Search
- `topological_sort` - Topological sorting (DAG)
- `connected_components` - Find connected components
- `has_cycle` - Cycle detection

**Advanced Algorithms** (Python only):
- `dijkstra` - Dijkstra's shortest path
- `prim_mst` - Prim's minimum spanning tree
- `kruskal_mst` - Kruskal's minimum spanning tree

### Supported Graph Types

**Random Graph:**
```json
{
  "vertices": 1000,
  "type": "random",
  "density": 0.05,
  "directed": false,
  "weighted": false
}
```

**Directed Acyclic Graph (DAG):**
```json
{
  "vertices": 100,
  "type": "dag",
  "edge_probability": 0.1,
  "directed": true,
  "weighted": false
}
```

## 📈 Expected Performance

Typical performance characteristics (lower is better):

### DFS on Sparse Graph (1000 vertices, 5% density)

| Language   | Avg Time (ms) | Relative Performance |
|------------|---------------|----------------------|
| C++        | 0.5           | Baseline (fastest)   |
| Go         | 1.2           | 2.4x slower          |
| Java       | 1.5           | 3.0x slower          |
| JavaScript | 3.0           | 6.0x slower          |
| Python     | 8.0           | 16.0x slower         |

*Note: Actual results vary based on hardware, OS, and runtime versions*

### Performance Factors

1. **Compilation vs Interpretation**
   - Compiled languages (C++, Go) are generally fastest
   - JIT-compiled (Java, JavaScript) are middle-tier
   - Interpreted (Python) is slowest but most flexible

2. **Memory Management**
   - Manual/RAII (C++): Fastest but most complex
   - Garbage collection (Java, Go, JS): Automatic but with overhead
   - Reference counting (Python): Simplest but slowest

3. **Data Structure Implementation**
   - HashMap/Dictionary performance varies significantly
   - C++ `unordered_map` vs Python `dict` vs Go `map`

4. **Optimization Levels**
   - C++ with `-O3` flag
   - Go native optimizations
   - JIT warmup for Java/JavaScript

## 🔬 Adding New Benchmarks

### 1. Add to Configuration

Edit `benchmark_config.json`:
```json
{
  "name": "MyNewBenchmark",
  "description": "Description of the benchmark",
  "graph": {
    "vertices": 500,
    "type": "random",
    "density": 0.1,
    "directed": false,
    "weighted": true
  },
  "algorithm": "bfs",
  "start_vertex": 0,
  "trials": 10
}
```

### 2. Run Benchmarks

```bash
./run_all_benchmarks.sh
```

### 3. Analyze Results

Results will automatically be included in visualizations.

## 🔧 Troubleshooting

### Python Import Errors

```bash
# Install dependencies
pip install -r requirements_benchmark.txt

# Or install individually
pip install pandas matplotlib seaborn numpy
```

### Java Compilation Issues

The Java benchmark runner currently uses a simplified JSON writer. For full functionality, add a JSON library:

```bash
# Example with org.json
# Download json-20230227.jar from https://mvnrepository.com/artifact/org.json/json
javac -cp .:json-20230227.jar BenchmarkJava.java
java -cp .:json-20230227.jar BenchmarkJava
```

### C++ Compilation Errors

Ensure C++17 support:
```bash
g++ --version  # Should be 7.0 or higher
g++ -std=c++17 -O3 -o benchmark_cpp benchmark_cpp.cpp
```

### Permission Denied on Shell Script

```bash
chmod +x run_all_benchmarks.sh
```

### Go Module Errors

If you're in a Go module, run outside or disable modules:
```bash
GO111MODULE=off go run benchmark_go.go graph.go
```

## 📚 File Structure

```
graph-algorithms/
├── benchmark_config.json          # Benchmark configuration
├── benchmark_py.py                # Python benchmark runner
├── benchmark_js.js                # JavaScript benchmark runner
├── BenchmarkJava.java             # Java benchmark runner
├── benchmark_go.go                # Go benchmark runner
├── benchmark_cpp.cpp              # C++ benchmark runner
├── aggregate_results.py           # Result aggregation and visualization
├── run_all_benchmarks.sh          # Master benchmark script
├── requirements_benchmark.txt     # Python dependencies
├── BENCHMARK_README.md            # This file
│
├── results_python.json            # Generated results (Python)
├── results_javascript.json        # Generated results (JavaScript)
├── results_java.json              # Generated results (Java)
├── results_go.json                # Generated results (Go)
├── results_cpp.json               # Generated results (C++)
│
└── benchmark_results/             # Generated visualizations
    ├── comparison_*.png           # Performance comparisons
    ├── algorithms_*.png           # Algorithm comparisons
    ├── heatmap_overall.png        # Overall heatmap
    ├── variability_*.png          # Variability analysis
    └── summary_statistics.csv     # Summary table
```

## 🎯 Best Practices

1. **Run Multiple Times**
   - Results can vary between runs
   - The config specifies 10 trials per benchmark
   - Consider running the entire suite 3-5 times for publication-quality results

2. **System Load**
   - Close unnecessary applications
   - Avoid running benchmarks during heavy system load
   - Consider disabling CPU frequency scaling

3. **Warmup**
   - JIT-compiled languages (Java, JavaScript) may show different results on first run
   - The framework automatically runs multiple trials to account for this

4. **Fair Comparison**
   - All implementations use equivalent algorithms
   - Same graph structures and sizes
   - Same operations counted

5. **Hardware Consistency**
   - Run all benchmarks on the same machine
   - Note hardware specs when sharing results

## 📖 References

1. Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
2. Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
3. Computer Language Benchmarks Game: https://benchmarksgame-team.pages.debian.net/

## 🤝 Contributing

To add a new language:

1. Implement the benchmark runner following existing patterns
2. Parse `benchmark_config.json` or use hardcoded benchmarks
3. Output results in the standard JSON format
4. Add language to `run_all_benchmarks.sh`
5. Update this README

## 📝 License

Part of the Applied Papers Lab graph algorithms project.
