# Quick Start Guide

Get started with the graph algorithms library in 5 minutes!

## 🚀 Choose Your Language

Select your preferred language and start coding:

### Python

```python
from graph import Graph, GraphType

# Create a graph
g = Graph(5, GraphType.UNDIRECTED)
g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(2, 3)

# Run algorithms
traversal = g.dfs_iterative(0)
print(f"DFS: {traversal}")

# Visualize (ASCII)
g.visualize()
```

**Run Tests:**
```bash
python test_graph.py
```

**Run Benchmarks:**
```bash
python benchmark_py.py
```

### JavaScript

```javascript
const { Graph, GraphType } = require('./graph.js');

// Create a graph
const g = new Graph(5, GraphType.UNDIRECTED);
g.addEdge(0, 1);
g.addEdge(1, 2);
g.addEdge(2, 3);

// Run algorithms
const traversal = g.dfsIterative(0);
console.log(`DFS: ${traversal}`);

// Visualize
g.visualize();
```

**Run Tests:**
```bash
node test_graph.js
```

**Run Benchmarks:**
```bash
node benchmark_js.js
```

### Java

```java
public class Main {
    public static void main(String[] args) {
        // Create a graph
        Graph g = new Graph(5, Graph.GraphType.UNDIRECTED, false);
        g.addEdge(0, 1);
        g.addEdge(1, 2);
        g.addEdge(2, 3);

        // Run algorithms
        List<Integer> traversal = g.dfsIterative(0);
        System.out.println("DFS: " + traversal);

        // Visualize
        g.visualize();
    }
}
```

**Compile and Run:**
```bash
javac graph.java Main.java
java Main
```

**Run Tests:**
```bash
javac GraphTest.java graph.java
java GraphTest
```

### Go

```go
package main

import "fmt"

func main() {
    // Create a graph
    g := NewGraph(5, Undirected, false, AdjacencyList)
    g.AddEdge(0, 1, 1.0)
    g.AddEdge(1, 2, 1.0)
    g.AddEdge(2, 3, 1.0)

    // Run algorithms
    traversal := g.DFSIterative(0)
    fmt.Printf("DFS: %v\n", traversal)

    // Visualize
    g.Visualize()
}
```

**Run:**
```bash
go run graph.go main.go
```

**Run Tests:**
```bash
go test
```

**Run Benchmarks:**
```bash
go run benchmark_go.go graph.go
```

### C++

```cpp
#include "graph.cpp"

int main() {
    // Create a graph
    Graph g(5, GraphType::UNDIRECTED, false);
    g.addEdge(0, 1);
    g.addEdge(1, 2);
    g.addEdge(2, 3);

    // Run algorithms
    auto traversal = g.dfsIterative(0);
    std::cout << "DFS: ";
    for (int v : traversal) std::cout << v << " ";
    std::cout << std::endl;

    // Visualize
    g.visualize();

    return 0;
}
```

**Compile and Run:**
```bash
g++ -std=c++17 -o main graph.cpp main.cpp
./main
```

**Run Tests:**
```bash
g++ -std=c++17 -o test test_graph.cpp
./test
```

### Rust

```rust
use crate::graph::{Graph, GraphType};

fn main() {
    // Create a graph
    let mut g = Graph::new(5, GraphType::Undirected, false);
    g.add_edge(0, 1, 1.0);
    g.add_edge(1, 2, 1.0);
    g.add_edge(2, 3, 1.0);

    // Run algorithms
    let traversal = g.dfs_iterative(0);
    println!("DFS: {:?}", traversal);

    // Visualize
    g.visualize();
}
```

**Run:**
```bash
cargo run
```

**Run Tests:**
```bash
cargo test
```

## 📊 Common Tasks

### Create Different Graph Types

```python
from graph import Graph, GraphType, RepresentationType

# Directed graph
g1 = Graph(10, GraphType.DIRECTED)

# Weighted graph
g2 = Graph(10, GraphType.UNDIRECTED, weighted=True)

# With adjacency matrix
g3 = Graph(10, GraphType.UNDIRECTED, weighted=False,
           representation=RepresentationType.ADJACENCY_MATRIX)
```

### Generate Random Graphs

```python
from graph import GraphGenerator

# Random sparse graph
g = GraphGenerator.random_graph(100, density=0.1)

# Complete graph
g = GraphGenerator.complete_graph(10)

# Directed Acyclic Graph (DAG)
g = GraphGenerator.dag(50, edge_probability=0.2)

# Bipartite graph
g = GraphGenerator.bipartite_graph(10, 15)
```

### Use Advanced Algorithms (Python Only)

```python
from graph_advanced import AdvancedGraph, GraphType

# Create weighted graph
g = AdvancedGraph(5, GraphType.UNDIRECTED, weighted=True)
g.add_edge(0, 1, 4)
g.add_edge(0, 2, 1)
g.add_edge(1, 3, 1)
g.add_edge(2, 1, 2)
g.add_edge(2, 3, 5)

# Dijkstra's shortest path
distances, predecessors = g.dijkstra(0)
path = g.get_shortest_path(0, 3)
print(f"Shortest path from 0 to 3: {path}")
print(f"Distance: {distances[3]}")

# Minimum Spanning Tree
mst_edges, total_weight = g.prim_mst(0)
print(f"MST edges: {mst_edges}")
print(f"Total weight: {total_weight}")

# Check if bipartite
is_bip, coloring = g.is_bipartite()
print(f"Is bipartite: {is_bip}")

# Find strongly connected components
sccs = g.strongly_connected_components()
print(f"Strongly connected components: {sccs}")
```

### Generate Special Graph Types (Python Only)

```python
from graph_generators_extended import ExtendedGraphGenerator

# Scale-free network (Barabási-Albert)
network = ExtendedGraphGenerator.barabasi_albert(n=100, m=3)

# Small-world network (Watts-Strogatz)
network = ExtendedGraphGenerator.watts_strogatz(n=100, k=4, beta=0.3)

# Grid graph
grid = ExtendedGraphGenerator.grid_graph(rows=10, cols=10, diagonal=True)

# Binary tree
tree = ExtendedGraphGenerator.binary_tree(levels=4)

# Petersen graph
petersen = ExtendedGraphGenerator.petersen_graph()

# Hypercube
hypercube = ExtendedGraphGenerator.hypercube(dimension=4)
```

## 🧪 Running Tests

### All Languages at Once

```bash
# Python
python test_graph.py

# JavaScript
node test_graph.js

# Java
javac GraphTest.java graph.java && java GraphTest

# Go
go test

# C++
g++ -std=c++17 -o test test_graph.cpp && ./test

# Rust
cargo test
```

## 📊 Running Benchmarks

### Cross-Language Benchmark Suite

```bash
# Run all benchmarks and generate visualizations
./run_all_benchmarks.sh

# Results will be in:
# - results_python.json
# - results_javascript.json
# - results_java.json
# - results_go.json
# - results_cpp.json
# - benchmark_results/ (visualizations)
```

### Individual Language Benchmarks

```bash
# Python (supports all algorithms)
python benchmark_py.py

# JavaScript (basic algorithms)
node benchmark_js.js

# Go (basic algorithms)
go run benchmark_go.go graph.go

# C++ (basic algorithms)
g++ -std=c++17 -O3 -o benchmark_cpp benchmark_cpp.cpp
./benchmark_cpp
```

### Analyze Results

```bash
# Install dependencies
pip install -r requirements_benchmark.txt

# Generate visualizations
python aggregate_results.py

# View results in benchmark_results/ directory
```

## 📚 Common Algorithms

### Traversal
- `dfs_iterative(start)` - Depth-First Search (iterative)
- `dfs_recursive(start)` - Depth-First Search (recursive)
- `bfs(start)` - Breadth-First Search

### Analysis
- `has_cycle()` - Detect cycles
- `find_connected_components()` - Find connected components
- `is_connected()` - Check if graph is connected
- `topological_sort()` - Topological ordering (DAG)
- `graph_coloring()` - Greedy graph coloring

### Shortest Path (Python Advanced)
- `dijkstra(source)` - Single-source shortest paths
- `bellman_ford(source)` - Handles negative weights
- `floyd_warshall()` - All-pairs shortest paths

### Minimum Spanning Tree (Python Advanced)
- `prim_mst(start)` - Prim's algorithm
- `kruskal_mst()` - Kruskal's algorithm

### Network Analysis (Python Advanced)
- `is_bipartite()` - Check if bipartite
- `strongly_connected_components()` - Find SCCs
- `articulation_points()` - Find cut vertices
- `bridges()` - Find cut edges
- `max_flow(source, sink)` - Maximum flow

## 🎓 Learning Path

1. **Start Simple** - Create a small graph, add edges, run DFS/BFS
2. **Explore Generators** - Generate different graph types
3. **Test Algorithms** - Try cycle detection, connected components
4. **Advanced Algorithms** - Dijkstra, MST, flow algorithms (Python)
5. **Performance** - Run benchmarks, compare languages
6. **Custom Applications** - Build your own graph-based solutions

## 📖 Documentation

- **README.md** - Main documentation
- **ADVANCED_FEATURES.md** - Advanced algorithms guide
- **TEST_README.md** - Testing guide
- **BENCHMARK_README.md** - Benchmarking guide
- **PROJECT_SUMMARY.md** - Complete project overview

## 💡 Tips

1. **Start with small graphs** for testing and visualization
2. **Use generators** for creating test cases
3. **Run tests** after making changes
4. **Compare implementations** across languages to learn different approaches
5. **Use benchmarks** to understand performance characteristics
6. **Read the complexity** comments to understand algorithm efficiency

## 🤔 Common Questions

**Q: Which language should I use?**
A: Python for easiest start and most features. C++/Go for best performance. JavaScript for web applications.

**Q: How do I visualize large graphs?**
A: ASCII visualization works for small graphs. For large graphs, export to formats like DOT and use external tools.

**Q: Why is Python slower?**
A: Python is interpreted and dynamically typed. See benchmarks for detailed comparisons.

**Q: Can I use this in production?**
A: Yes! The code is well-tested and documented. Consider performance requirements when choosing language.

**Q: How do I add a new algorithm?**
A: Add the method to the Graph class, write tests, update documentation.

## 🆘 Getting Help

1. Check the README for your language
2. Read the relevant documentation file
3. Look at the test files for usage examples
4. Run the demo functions in each implementation
5. Check the GitHub issues (if applicable)

## 🎯 Next Steps

Now that you're set up:

1. ✅ Run your first graph algorithm
2. ✅ Generate a random graph
3. ✅ Run the test suite
4. ✅ Try the benchmarks
5. ✅ Build something cool!

Happy graph coding! 🚀
