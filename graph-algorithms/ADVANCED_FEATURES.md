# Advanced Graph Features

This document describes the advanced features added to the graph algorithms library, including shortest paths, minimum spanning trees, extended generators, and cross-language benchmarking.

## 🚀 New Features

### 1. Advanced Algorithms (`graph_advanced.py`)

#### Shortest Path Algorithms

**Dijkstra's Algorithm**
```python
from graph_advanced import AdvancedGraph, GraphType

g = AdvancedGraph(5, GraphType.DIRECTED, True)
g.add_edge(0, 1, 10)
g.add_edge(0, 2, 3)
# ... add more edges

# Get distances and paths
distances, predecessors = g.dijkstra(0)
path = g.get_shortest_path(0, 4)
print(f"Shortest path: {path}")
```

**Bellman-Ford Algorithm** (handles negative weights)
```python
distances, predecessors, has_cycle = g.bellman_ford(0)
if has_cycle:
    print("Negative cycle detected!")
```

**Floyd-Warshall Algorithm** (all-pairs shortest paths)
```python
dist_matrix, next_matrix = g.floyd_warshall()
path = g.reconstruct_path_floyd(next_matrix, 0, 4)
```

#### Minimum Spanning Tree Algorithms

**Prim's Algorithm**
```python
g = AdvancedGraph(4, GraphType.UNDIRECTED, True)
# Add weighted edges...

mst_edges, total_weight = g.prim_mst(start=0)
print(f"MST edges: {mst_edges}")
print(f"Total weight: {total_weight}")
```

**Kruskal's Algorithm** (with Union-Find)
```python
mst_edges, total_weight = g.kruskal_mst()
```

#### Additional Advanced Algorithms

**Bipartite Graph Detection**
```python
is_bipartite, coloring = g.is_bipartite()
if is_bipartite:
    print(f"Graph is bipartite with coloring: {coloring}")
```

**Strongly Connected Components** (Kosaraju's Algorithm)
```python
sccs = g.strongly_connected_components()
print(f"SCCs: {sccs}")
```

**Articulation Points and Bridges** (Tarjan's Algorithm)
```python
articulation_points = g.articulation_points()
bridges = g.bridges()
```

**Maximum Flow** (Ford-Fulkerson with Edmonds-Karp)
```python
max_flow_value = g.max_flow(source=0, sink=5)
print(f"Maximum flow: {max_flow_value}")
```

### 2. Extended Graph Generators (`graph_generators_extended.py`)

#### Specialized Graph Types

**Bipartite Graphs**
```python
from graph_generators_extended import ExtendedGraphGenerator

# Random bipartite
g = ExtendedGraphGenerator.bipartite_graph(n1=5, n2=4, edge_probability=0.5)

# Complete bipartite
g = ExtendedGraphGenerator.complete_bipartite(3, 3)
```

**Tree Structures**
```python
# Random tree
g = ExtendedGraphGenerator.tree(n=20)

# Binary tree
g = ExtendedGraphGenerator.binary_tree(levels=4)

# Star graph
g = ExtendedGraphGenerator.star_graph(n=10)
```

**Geometric Graphs**
```python
# Grid graph
g = ExtendedGraphGenerator.grid_graph(rows=5, cols=5, diagonal=True)

# Wheel graph
g = ExtendedGraphGenerator.wheel_graph(n=8)

# Path graph
g = ExtendedGraphGenerator.path_graph(n=15)
```

**Network Models**
```python
# Scale-free network (Barabási-Albert)
g = ExtendedGraphGenerator.barabasi_albert(n=100, m=3)

# Small-world network (Watts-Strogatz)
g = ExtendedGraphGenerator.watts_strogatz(n=100, k=4, beta=0.3)

# Random graph (Erdős-Rényi)
g = ExtendedGraphGenerator.erdos_renyi(n=50, p=0.1)
```

**Special Graphs**
```python
# Petersen graph
g = ExtendedGraphGenerator.petersen_graph()

# Hypercube
g = ExtendedGraphGenerator.hypercube(dimension=4)

# Planar graph
g = ExtendedGraphGenerator.planar_random(n=20, max_degree=5)
```

## 📊 Cross-Language Benchmarking

### Benchmark Framework Design

To compare performance across languages, create uniform test cases:

#### 1. Common Test Graph Specification (JSON)

```json
{
  "benchmarks": [
    {
      "name": "DFS on Dense Graph",
      "graph": {
        "vertices": 1000,
        "type": "dense",
        "density": 0.3
      },
      "algorithm": "dfs_iterative",
      "trials": 10
    },
    {
      "name": "Dijkstra on Sparse Graph",
      "graph": {
        "vertices": 5000,
        "type": "sparse"
      },
      "algorithm": "dijkstra",
      "trials": 10
    }
  ]
}
```

#### 2. Language-Specific Benchmark Implementations

**Python Benchmark**
```python
# benchmark_py.py
import time
import json
from graph import Graph, GraphGenerator

def benchmark_algorithm(graph, algorithm, trials=10):
    times = []
    for _ in range(trials):
        start = time.perf_counter()
        # Run algorithm
        if algorithm == "dfs_iterative":
            graph.dfs_iterative(0)
        elif algorithm == "dijkstra":
            from graph_advanced import AdvancedGraph
            AdvancedGraph.dijkstra(graph, 0)
        end = time.perf_counter()
        times.append(end - start)

    return {
        "mean": sum(times) / len(times),
        "min": min(times),
        "max": max(times),
        "times": times
    }

# Load config and run benchmarks
with open('benchmark_config.json') as f:
    config = json.load(f)

results = []
for bench in config['benchmarks']:
    # Generate graph
    if bench['graph']['type'] == 'dense':
        g = GraphGenerator.random_graph(
            bench['graph']['vertices'],
            bench['graph']['density']
        )
    # Run benchmark
    result = benchmark_algorithm(g, bench['algorithm'], bench['trials'])
    results.append({
        "language": "Python",
        "benchmark": bench['name'],
        "result": result
    })

# Save results
with open('results_python.json', 'w') as f:
    json.dump(results, f, indent=2)
```

**JavaScript Benchmark**
```javascript
// benchmark_js.js
const { Graph, GraphGenerator } = require('./graph.js');
const fs = require('fs');

function benchmarkAlgorithm(graph, algorithm, trials = 10) {
    const times = [];
    for (let i = 0; i < trials; i++) {
        const start = process.hrtime.bigint();

        if (algorithm === 'dfs_iterative') {
            graph.dfsIterative(0);
        } else if (algorithm === 'bfs') {
            graph.bfs(0);
        }

        const end = process.hrtime.bigint();
        times.push(Number(end - start) / 1e9); // Convert to seconds
    }

    return {
        mean: times.reduce((a, b) => a + b) / times.length,
        min: Math.min(...times),
        max: Math.max(...times),
        times: times
    };
}

// Run benchmarks and save results
```

**Go Benchmark**
```go
// benchmark_test.go
package main

import (
    "testing"
    "time"
)

func BenchmarkDFSIterative1000(b *testing.B) {
    g := RandomGraph(1000, 0.3, Undirected, false, AdjacencyList)
    b.ResetTimer()

    for i := 0; i < b.N; i++ {
        g.DFSIterative(0)
    }
}

func BenchmarkBFS1000(b *testing.B) {
    g := RandomGraph(1000, 0.3, Undirected, false, AdjacencyList)
    b.ResetTimer()

    for i := 0; i < b.N; i++ {
        g.BFS(0)
    }
}

// Run with: go test -bench=. -benchtime=10s
```

#### 3. Results Aggregation and Visualization

**Aggregate Results Script**
```python
# aggregate_results.py
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load results from all languages
results = []
for lang in ['python', 'javascript', 'java', 'cpp', 'go', 'rust']:
    try:
        with open(f'results_{lang}.json') as f:
            results.extend(json.load(f))
    except FileNotFoundError:
        print(f"No results for {lang}")

# Convert to DataFrame
df = pd.DataFrame(results)

# Create comparison plots
for benchmark_name in df['benchmark'].unique():
    data = df[df['benchmark'] == benchmark_name]

    plt.figure(figsize=(10, 6))
    plt.bar(data['language'], data['result'].apply(lambda x: x['mean']))
    plt.title(f'Performance Comparison: {benchmark_name}')
    plt.ylabel('Time (seconds)')
    plt.xlabel('Language')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'benchmark_{benchmark_name.replace(" ", "_")}.png')
    plt.close()
```

### Running Complete Benchmark Suite

**Master Benchmark Runner**
```bash
#!/bin/bash
# run_all_benchmarks.sh

echo "Running cross-language benchmarks..."

# Python
echo "Running Python benchmarks..."
python3 benchmark_py.py

# JavaScript
echo "Running JavaScript benchmarks..."
node benchmark_js.js

# Java
echo "Running Java benchmarks..."
javac BenchmarkJava.java
java BenchmarkJava

# Go
echo "Running Go benchmarks..."
go test -bench=. -benchtime=10s > results_go.txt

# C++
echo "Running C++ benchmarks..."
g++ -O3 -o benchmark_cpp benchmark_cpp.cpp
./benchmark_cpp

# Aggregate and visualize
echo "Aggregating results..."
python3 aggregate_results.py

echo "Done! Check benchmark_*.png for visualizations"
```

## 📈 Performance Analysis

### Expected Results

Based on algorithmic complexity and language characteristics:

**DFS/BFS Performance (1000 vertices, density 0.3)**
| Language   | Avg Time (ms) | Relative Speed |
|------------|---------------|----------------|
| C++        | 0.5           | 1.0x (baseline)|
| Rust       | 0.6           | 0.83x          |
| Go         | 1.2           | 0.42x          |
| Java       | 1.5           | 0.33x          |
| JavaScript | 3.0           | 0.17x          |
| Python     | 8.0           | 0.06x          |

**Dijkstra's Algorithm (5000 vertices, sparse)**
| Language   | Avg Time (ms) | Relative Speed |
|------------|---------------|----------------|
| C++        | 15            | 1.0x           |
| Rust       | 16            | 0.94x          |
| Go         | 25            | 0.60x          |
| Java       | 30            | 0.50x          |
| JavaScript | 60            | 0.25x          |
| Python     | 150           | 0.10x          |

### Factors Affecting Performance

1. **Memory Management**: C++/Rust (manual/RAII) vs GC languages
2. **Type System**: Static (C++/Rust/Java/Go) vs Dynamic (Python/JS)
3. **Runtime**: Compiled (C++/Rust/Go) vs JIT (Java/JS) vs Interpreted (Python)
4. **Data Structure Overhead**: HashMap costs vary by language
5. **Optimization**: Compiler flags make significant difference

## 🎯 Usage Examples

### Example 1: Finding Critical Paths in Project Network

```python
from graph_advanced import AdvancedGraph

# Create project dependency graph
project = AdvancedGraph(8, GraphType.DIRECTED, True)
# Add tasks with durations
project.add_edge(0, 1, 3)  # Task 0->1 takes 3 days
project.add_edge(0, 2, 5)
# ... add all dependencies

# Find critical path (longest path in DAG)
distances, _ = project.dijkstra(0)
critical_path_length = max(distances.values())
print(f"Project duration: {critical_path_length} days")
```

### Example 2: Network Analysis

```python
from graph_generators_extended import ExtendedGraphGenerator

# Generate scale-free network
network = ExtendedGraphGenerator.barabasi_albert(1000, 3)

# Analyze network properties
print(f"Vertices: {network.num_vertices}")
print(f"Edges: {network.num_edges}")
print(f"Average degree: {2 * network.num_edges / network.num_vertices}")

# Find hub nodes (articulation points)
hubs = network.articulation_points()
print(f"Hub nodes: {hubs}")
```

### Example 3: Social Network Communities

```python
from graph_advanced import AdvancedGraph

# Load social network
social = AdvancedGraph(100, GraphType.UNDIRECTED, False)
# ... load edges

# Find communities (strongly connected components)
communities = social.strongly_connected_components()
print(f"Found {len(communities)} communities")

# Check if network is small-world
is_bip, _ = social.is_bipartite()
print(f"Is bipartite: {is_bip}")
```

## 📚 Algorithm Complexity Reference

| Algorithm | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| Dijkstra | O((V+E) log V) | O(V) | With binary heap |
| Bellman-Ford | O(VE) | O(V) | Handles negative weights |
| Floyd-Warshall | O(V³) | O(V²) | All-pairs shortest paths |
| Prim's MST | O((V+E) log V) | O(V) | With binary heap |
| Kruskal's MST | O(E log E) | O(V) | With Union-Find |
| SCC (Kosaraju) | O(V+E) | O(V) | Two DFS passes |
| Articulation Points | O(V+E) | O(V) | Single DFS |
| Max Flow (Edmonds-Karp) | O(VE²) | O(V²) | BFS-based |

## 🔧 Extending to Other Languages

To add advanced algorithms to other languages:

### JavaScript
```javascript
// Add to graph.js
class AdvancedGraph extends Graph {
    dijkstra(source) {
        // Implementation...
    }
}
```

### Java
```java
// Extend Graph.java
public class AdvancedGraph extends Graph {
    public Map<Integer, Double> dijkstra(int source) {
        // Implementation...
    }
}
```

### Implementation Priority

1. **Essential**: Dijkstra, Prim/Kruskal MST
2. **Important**: Bellman-Ford, SCC
3. **Advanced**: Floyd-Warshall, Max Flow, Articulation Points

## 📦 Complete Feature Matrix

| Feature | Python | JavaScript | Java | C++ | Go | Rust | Swift | Kotlin |
|---------|--------|------------|------|-----|-----|------|-------|--------|
| **Basic Algorithms** ||||||||
| DFS | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| BFS | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Topological Sort | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Advanced Algorithms** ||||||||
| Dijkstra | ✓ | - | - | - | - | - | - | - |
| Bellman-Ford | ✓ | - | - | - | - | - | - | - |
| Floyd-Warshall | ✓ | - | - | - | - | - | - | - |
| Prim's MST | ✓ | - | - | - | - | - | - | - |
| Kruskal's MST | ✓ | - | - | - | - | - | - | - |
| **Graph Types** ||||||||
| Basic Generators | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Extended Generators | ✓ | - | - | - | - | - | - | - |
| **Testing** ||||||||
| Unit Tests | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Benchmarks | ✓ | partial | partial | partial | ✓ | - | - | - |

Legend: ✓ = Complete, partial = Partially implemented, - = Not yet implemented

## 🚀 Next Steps

1. **Implement advanced algorithms in all languages**
2. **Complete benchmark framework with automated runners**
3. **Add more network analysis algorithms** (betweenness centrality, PageRank)
4. **Create interactive visualizations** (D3.js, Plotly)
5. **Add parallel/concurrent implementations**
6. **Create GPU-accelerated versions** for large graphs

## 📖 References

1. Cormen, T. H., et al. (2009). Introduction to Algorithms (3rd ed.). MIT Press.
2. Sedgewick, R., & Wayne, K. (2011). Algorithms (4th ed.). Addison-Wesley.
3. Newman, M. (2010). Networks: An Introduction. Oxford University Press.
4. Barabási, A. L. (2016). Network Science. Cambridge University Press.
