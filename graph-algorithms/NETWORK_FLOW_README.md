# Network Flow and Pathfinding Algorithms

A comprehensive collection of network flow, pathfinding, and assignment algorithms implemented in Python.

## 📚 Table of Contents

- [Overview](#overview)
- [Implemented Algorithms](#implemented-algorithms)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Algorithm Details](#algorithm-details)
- [Performance Comparisons](#performance-comparisons)
- [Applications](#applications)
- [References](#references)

## 🎯 Overview

This module provides production-ready implementations of fundamental network flow and pathfinding algorithms, featuring:

- **Network Flow**: Maximum flow, minimum cut, and cost optimization algorithms
- **Pathfinding**: Shortest path and heuristic search algorithms
- **Assignment Problems**: Optimal assignment and matching algorithms
- **Clear Documentation**: Comprehensive explanations and examples
- **Optimized Performance**: Efficient implementations with proper time/space complexity

## 📊 Implemented Algorithms

### Network Flow Algorithms (`network_flow.py`)

| Algorithm | Type | Time Complexity | Space Complexity | Use Case |
|-----------|------|-----------------|------------------|----------|
| **Ford-Fulkerson** | Max Flow | O(E × max_flow) | O(V) | Small networks, integer capacities |
| **Edmonds-Karp** | Max Flow | O(V × E²) | O(V) | General max flow, guaranteed polynomial |
| **Dinic's Algorithm** | Max Flow | O(V² × E) | O(V) | Dense networks, better practical performance |
| **Push-Relabel** | Max Flow | O(V²E) | O(V) | Often fastest in practice |
| **Min Cost Max Flow** | Cost Flow | O(V²E²) | O(V²) | Minimum cost flow problems |
| **Bipartite Matching** | Matching | O(V × E) | O(V) | Assignment problems, job scheduling |

### Pathfinding Algorithms (`pathfinding.py`)

| Algorithm | Type | Time Complexity | Space Complexity | Use Case |
|-----------|------|-----------------|------------------|----------|
| **A* Search** | Heuristic | O((V+E) log V) | O(V) | Optimal path with good heuristic |
| **Dijkstra** | Shortest Path | O((V+E) log V) | O(V) | Non-negative weights, all paths |
| **Bellman-Ford** | Shortest Path | O(V × E) | O(V) | Negative weights, cycle detection |
| **Floyd-Warshall** | All Pairs | O(V³) | O(V²) | All-pairs shortest paths |
| **Bidirectional Search** | Search | O(√(V+E)) | O(V) | Large graphs, known endpoints |
| **Jump Point Search** | Grid Path | O(V log V) | O(V) | Grid-based pathfinding |

### Assignment Algorithms (`hungarian_algorithm.py`)

| Algorithm | Type | Time Complexity | Space Complexity | Use Case |
|-----------|------|-----------------|------------------|----------|
| **Hungarian Algorithm** | Assignment | O(n³) | O(n²) | Optimal assignment, job scheduling |
| **Kuhn-Munkres** | Assignment | O(n³) | O(n²) | Weighted bipartite matching |

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/algorithms-multiverse.git
cd algorithms-multiverse/graph-algorithms

# Install dependencies
pip install numpy

# Run examples
python network_flow.py
python pathfinding.py
python hungarian_algorithm.py
```

## 💻 Usage Examples

### Network Flow

#### Ford-Fulkerson / Edmonds-Karp

```python
from network_flow import FlowNetwork, FordFulkerson, EdmondsKarp

# Create flow network
network = FlowNetwork(6)
network.add_edge(0, 1, 16)
network.add_edge(0, 2, 13)
network.add_edge(1, 3, 12)
network.add_edge(2, 1, 4)
network.add_edge(2, 4, 14)
network.add_edge(3, 5, 20)
network.add_edge(4, 3, 7)
network.add_edge(4, 5, 4)

# Find maximum flow with Ford-Fulkerson
ff = FordFulkerson(network)
max_flow = ff.max_flow(0, 5)
print(f"Maximum flow: {max_flow}")

# Find minimum cut
S, T = ff.min_cut(0)
print(f"Minimum cut - S: {S}, T: {T}")

# Use Edmonds-Karp (more efficient)
network2 = FlowNetwork(6)
# ... add same edges
ek = EdmondsKarp(network2)
max_flow = ek.max_flow(0, 5)

# Get flow on each edge
flow_edges = ek.get_flow_edges()
for u, v, flow in flow_edges:
    print(f"Edge {u} -> {v}: flow = {flow}")
```

#### Bipartite Matching

```python
from network_flow import BipartiteMatching

# Create bipartite graph (4 people, 4 jobs)
bm = BipartiteMatching(left_size=4, right_size=4)

# Add possible assignments
bm.add_edge(0, 0)  # Person 0 can do Job 0
bm.add_edge(0, 1)  # Person 0 can do Job 1
bm.add_edge(1, 1)  # Person 1 can do Job 1
bm.add_edge(1, 2)  # Person 1 can do Job 2
bm.add_edge(2, 2)  # Person 2 can do Job 2
bm.add_edge(2, 3)  # Person 2 can do Job 3
bm.add_edge(3, 3)  # Person 3 can do Job 3

# Find maximum matching
matching = bm.max_matching()
for person, job in matching:
    print(f"Person {person} assigned to Job {job}")

# Check if perfect matching exists
if bm.is_perfect_matching():
    print("Perfect matching found!")
```

#### Minimum Cost Maximum Flow

```python
from network_flow import MinCostMaxFlow

# Create network with costs
mcmf = MinCostMaxFlow(4)
mcmf.add_edge(0, 1, capacity=2, cost=1)
mcmf.add_edge(0, 2, capacity=1, cost=3)
mcmf.add_edge(1, 3, capacity=1, cost=2)
mcmf.add_edge(2, 3, capacity=2, cost=1)

# Find min cost max flow
max_flow, min_cost = mcmf.min_cost_max_flow(0, 3)
print(f"Maximum flow: {max_flow}, Minimum cost: {min_cost}")
```

### Pathfinding

#### A* Search

```python
from pathfinding import AStar

# Create graph with weighted edges
graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('E', 2), ('F', 6)],
    'E': [('C', 10), ('D', 2), ('F', 3)],
    'F': [('D', 6), ('E', 3)]
}

# Define heuristic function (estimated distance to goal)
def heuristic(node, goal):
    estimates = {'A': 10, 'B': 8, 'C': 6, 'D': 4, 'E': 2, 'F': 0}
    return estimates.get(node, 0)

# Find optimal path
astar = AStar(heuristic=heuristic)
path, cost = astar.search(graph, 'A', 'F')
print(f"Path: {' -> '.join(path)}")
print(f"Cost: {cost}")
```

#### A* on 2D Grid

```python
from pathfinding import AStar

# Create grid (0 = empty, 1 = obstacle)
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

# Find path from top-left to bottom-right
astar = AStar()
path, cost = astar.search_grid(
    grid,
    start=(0, 0),
    goal=(4, 4),
    diagonal=True  # Allow diagonal movement
)

print(f"Path found with cost: {cost}")
for position in path:
    print(f"  {position}")
```

#### Dijkstra's Algorithm

```python
from pathfinding import Dijkstra

# Find shortest paths from source to all vertices
dijkstra = Dijkstra()
all_paths = dijkstra.shortest_paths(graph, 'A')

for vertex, (distance, path) in all_paths.items():
    print(f"To {vertex}: distance={distance}, path={' -> '.join(path)}")

# Find specific path
path, distance = dijkstra.shortest_path(graph, 'A', 'F')
```

#### Jump Point Search (JPS)

```python
from pathfinding import JumpPointSearch

# Efficient grid pathfinding
grid = [[0]*10 for _ in range(10)]
# Add obstacles...

jps = JumpPointSearch(grid)
path, cost = jps.search((0, 0), (9, 9))

# JPS is much faster than A* on large grids
print(f"JPS found path with {len(path)} waypoints")
```

### Assignment Problems

#### Hungarian Algorithm

```python
from hungarian_algorithm import HungarianAlgorithm

# Cost matrix: workers (rows) vs jobs (columns)
cost_matrix = [
    [4, 2, 8, 5],
    [2, 3, 7, 6],
    [3, 4, 5, 7],
    [5, 8, 3, 4]
]

# Find minimum cost assignment
hungarian = HungarianAlgorithm(cost_matrix)
assignments, total_cost = hungarian.solve()

for worker, job in assignments:
    print(f"Worker {worker} -> Job {job} (cost: {cost_matrix[worker][job]})")
print(f"Total cost: {total_cost}")

# Maximization problem (e.g., profit)
profit_matrix = [
    [10, 19, 8, 15],
    [10, 18, 7, 17],
    [13, 16, 9, 14],
    [12, 19, 8, 18]
]

hungarian_max = HungarianAlgorithm(profit_matrix, maximize=True)
assignments, total_profit = hungarian_max.solve()
print(f"Maximum profit: {total_profit}")
```

## 📖 Algorithm Details

### Network Flow Algorithms

#### Ford-Fulkerson

**Concept**: Repeatedly finds augmenting paths from source to sink using DFS.

**Key Features**:
- Simple implementation
- Works well with integer capacities
- Can find minimum cut after max flow
- Not guaranteed polynomial time with real numbers

**When to Use**:
- Small networks
- Integer capacities
- Need minimum cut
- Teaching/learning purposes

#### Edmonds-Karp

**Concept**: Ford-Fulkerson with BFS for finding augmenting paths.

**Key Features**:
- Guaranteed O(VE²) time complexity
- More predictable performance
- Always finds shortest augmenting path
- Standard choice for general max flow

**When to Use**:
- General max flow problems
- Need guaranteed polynomial time
- Real-valued capacities
- Medium-sized networks

#### Dinic's Algorithm

**Concept**: Uses level graphs and blocking flows for efficiency.

**Key Features**:
- O(V²E) complexity
- Often faster in practice than Edmonds-Karp
- Good for dense graphs
- Efficient with unit capacities

**When to Use**:
- Dense networks
- Unit capacity networks
- Large scale problems
- When Edmonds-Karp is too slow

### Pathfinding Algorithms

#### A* Search

**Concept**: Best-first search guided by f(n) = g(n) + h(n).

**Key Features**:
- Optimal if heuristic is admissible
- Faster than Dijkstra with good heuristic
- Memory efficient with proper implementation
- Works on graphs and grids

**When to Use**:
- Have good heuristic function
- Single source-target pathfinding
- Game AI and robotics
- Navigation systems

#### Jump Point Search (JPS)

**Concept**: Optimized A* for uniform-cost grids by pruning symmetrical paths.

**Key Features**:
- Up to 10x faster than A* on grids
- Maintains optimality
- Reduces memory usage
- Identifies "jump points" to skip unnecessary nodes

**When to Use**:
- Large grid-based maps
- Game pathfinding
- Robotics navigation
- Real-time applications

## 📊 Performance Comparisons

### Maximum Flow Performance

| Algorithm | Small (V<100) | Medium (V<1000) | Large (V>1000) | Dense | Sparse |
|-----------|---------------|-----------------|----------------|-------|--------|
| Ford-Fulkerson | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ |
| Edmonds-Karp | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Dinic | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Push-Relabel | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |

### Pathfinding Performance

| Algorithm | Single Pair | All Pairs | Negative Weights | Grid | Heuristic |
|-----------|-------------|-----------|------------------|------|-----------|
| A* | ⭐⭐⭐⭐ | ⭐ | ❌ | ⭐⭐⭐ | Required |
| Dijkstra | ⭐⭐⭐ | ⭐⭐ | ❌ | ⭐⭐ | Not used |
| Bellman-Ford | ⭐⭐ | ⭐ | ✅ | ⭐ | Not used |
| Floyd-Warshall | ⭐ | ⭐⭐⭐⭐ | ✅ | ⭐ | Not used |
| JPS | ⭐⭐⭐⭐ | ⭐ | ❌ | ⭐⭐⭐⭐ | Built-in |

## 🔧 Applications

### Network Flow Applications

1. **Transportation Networks**
   - Traffic flow optimization
   - Supply chain management
   - Pipeline capacity planning

2. **Computer Networks**
   - Bandwidth allocation
   - Data routing
   - Network reliability

3. **Resource Allocation**
   - Job scheduling
   - Project assignment
   - Machine scheduling

4. **Bioinformatics**
   - Protein interaction networks
   - Metabolic pathways
   - Gene regulatory networks

### Pathfinding Applications

1. **Navigation Systems**
   - GPS routing
   - Indoor navigation
   - Drone path planning

2. **Game Development**
   - NPC movement
   - Strategic planning
   - Map exploration

3. **Robotics**
   - Motion planning
   - Obstacle avoidance
   - Multi-robot coordination

4. **Network Routing**
   - Packet routing
   - Circuit design
   - Social network analysis

## 📚 References

### Papers
- Ford, L.R.; Fulkerson, D.R. (1956). "Maximal Flow through a Network"
- Edmonds, J.; Karp, R.M. (1972). "Theoretical improvements in algorithmic efficiency"
- Goldberg, A.V.; Tarjan, R.E. (1988). "A new approach to the maximum-flow problem"
- Hart, P.E.; Nilsson, N.J.; Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths"
- Harabor, D.; Grastien, A. (2011). "Online Graph Pruning for Pathfinding on Grid Maps"

### Books
- "Introduction to Algorithms" - Cormen, Leiserson, Rivest, Stein
- "Network Flows: Theory, Algorithms, and Applications" - Ahuja, Magnanti, Orlin
- "Artificial Intelligence: A Modern Approach" - Russell, Norvig
- "Combinatorial Optimization: Algorithms and Complexity" - Papadimitriou, Steiglitz

## 📄 License

MIT License - See [LICENSE](../../LICENSE) file for details.

## 🌟 Contributing

Contributions are welcome! Areas for improvement:
- Additional algorithms (Min-cost circulation, Gomory-Hu trees)
- Performance optimizations
- Visualization tools
- Additional test cases
- Language ports

---

Part of the **Algorithms Multiverse** project - A comprehensive collection of algorithms across multiple programming languages.

**Last Updated**: January 2026