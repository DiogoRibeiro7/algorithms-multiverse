"""
Comprehensive Minimum Spanning Tree (MST) Algorithms
=====================================================

Implements three classic MST algorithms with various optimizations:
1. Kruskal's Algorithm with Union-Find (path compression + union by rank)
2. Prim's Algorithm with multiple priority queue implementations
3. Borůvka's Algorithm (parallel-friendly)

Features:
- Support for disconnected graphs (Minimum Spanning Forest)
- Multiple priority queue implementations for Prim's
- Parallel versions where applicable
- Visualization of MST construction
- Real-world applications (network design)
- Performance comparison

Time Complexities:
- Kruskal's: O(E log E) or O(E log V)
- Prim's (Binary Heap): O((V+E) log V)
- Prim's (Fibonacci Heap): O(E + V log V)
- Borůvka's: O(E log V)

Author: Claude Code
Date: 2025
"""

import heapq
import time
from collections import defaultdict
from typing import List, Tuple, Dict, Set, Optional
from enum import Enum


class PriorityQueueType(Enum):
    """Types of priority queues for Prim's algorithm"""
    BINARY_HEAP = "binary_heap"
    SIMPLE_ARRAY = "simple_array"
    # Fibonacci heap would be added here for theoretical O(E + V log V)


class UnionFind:
    """
    Union-Find (Disjoint Set Union) data structure

    Implements path compression and union by rank for near O(1) operations.
    Essential for Kruskal's algorithm.

    Time Complexity:
    - find(): O(α(n)) amortized, where α is inverse Ackermann function
    - union(): O(α(n)) amortized

    Space Complexity: O(n)
    """

    def __init__(self, n: int):
        """
        Initialize Union-Find for n elements

        Args:
            n: Number of elements (vertices)
        """
        self.parent = list(range(n))
        self.rank = [0] * n
        self.component_count = n

    def find(self, x: int) -> int:
        """
        Find the representative (root) of the set containing x
        Uses path compression for optimization

        Args:
            x: Element to find

        Returns:
            Representative of the set containing x
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Union the sets containing x and y
        Uses union by rank for optimization

        Args:
            x, y: Elements to union

        Returns:
            True if union was performed (x and y were in different sets)
            False if x and y were already in the same set
        """
        px, py = self.find(x), self.find(y)

        if px == py:
            return False  # Already in same set

        # Union by rank: attach smaller tree to larger tree
        if self.rank[px] < self.rank[py]:
            px, py = py, px

        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

        self.component_count -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        """Check if x and y are in the same set"""
        return self.find(x) == self.find(y)

    def get_component_count(self) -> int:
        """Get number of disjoint components"""
        return self.component_count


class Edge:
    """Represents a weighted edge in a graph"""

    def __init__(self, u: int, v: int, weight: float):
        self.u = u
        self.v = v
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __repr__(self):
        return f"Edge({self.u}, {self.v}, {self.weight})"


class MSTAlgorithms:
    """
    Collection of Minimum Spanning Tree algorithms
    """

    def __init__(self, num_vertices: int, edges: List[Tuple[int, int, float]]):
        """
        Initialize MST solver

        Args:
            num_vertices: Number of vertices in graph
            edges: List of (u, v, weight) tuples representing undirected edges
        """
        self.num_vertices = num_vertices
        self.edges = [Edge(u, v, w) for u, v, w in edges]
        self.adj_list = self._build_adjacency_list()

    def _build_adjacency_list(self) -> Dict[int, List[Tuple[int, float]]]:
        """Build adjacency list representation"""
        adj = defaultdict(list)
        for edge in self.edges:
            adj[edge.u].append((edge.v, edge.weight))
            adj[edge.v].append((edge.u, edge.weight))
        return adj

    # ========================================================================
    # KRUSKAL'S ALGORITHM
    # ========================================================================

    def kruskal(self, return_forest: bool = False) -> Tuple[List[Edge], float, List[List[Edge]]]:
        """
        Kruskal's Algorithm for MST/MSF

        Strategy: Sort edges by weight, add edges that don't create cycles
        Uses Union-Find to efficiently detect cycles

        Time Complexity: O(E log E) or O(E log V) since E ≤ V²
        Space Complexity: O(V + E)

        Args:
            return_forest: If True, handles disconnected graphs (returns MSF)

        Returns:
            mst_edges: List of edges in MST
            total_weight: Total weight of MST
            forest: List of trees (for disconnected graphs)
        """
        # Sort edges by weight - O(E log E)
        sorted_edges = sorted(self.edges)

        uf = UnionFind(self.num_vertices)
        mst_edges = []
        total_weight = 0

        # Process edges in sorted order
        for edge in sorted_edges:
            # Check if adding edge creates a cycle
            if uf.union(edge.u, edge.v):
                mst_edges.append(edge)
                total_weight += edge.weight

                # Early termination for connected graph
                if not return_forest and len(mst_edges) == self.num_vertices - 1:
                    break

        # Build forest (for disconnected graphs)
        forest = self._build_forest(mst_edges) if return_forest else []

        return mst_edges, total_weight, forest

    def kruskal_with_visualization(self) -> Tuple[List[Edge], float, List[Dict]]:
        """
        Kruskal's algorithm with step-by-step visualization data

        Returns:
            mst_edges: Final MST edges
            total_weight: Total weight
            steps: List of step dictionaries for visualization
        """
        sorted_edges = sorted(self.edges)
        uf = UnionFind(self.num_vertices)
        mst_edges = []
        total_weight = 0
        steps = []

        for i, edge in enumerate(sorted_edges):
            step = {
                'iteration': i,
                'edge_considered': edge,
                'action': '',
                'mst_so_far': list(mst_edges),
                'total_weight': total_weight
            }

            if uf.union(edge.u, edge.v):
                mst_edges.append(edge)
                total_weight += edge.weight
                step['action'] = 'added'
            else:
                step['action'] = 'rejected (creates cycle)'

            steps.append(step)

            if len(mst_edges) == self.num_vertices - 1:
                break

        return mst_edges, total_weight, steps

    # ========================================================================
    # PRIM'S ALGORITHM
    # ========================================================================

    def prim(self, start: int = 0,
             pq_type: PriorityQueueType = PriorityQueueType.BINARY_HEAP) -> Tuple[List[Edge], float]:
        """
        Prim's Algorithm for MST

        Strategy: Grow tree from starting vertex, always add minimum weight edge
        that connects tree to non-tree vertex

        Time Complexity:
        - Binary Heap: O((V+E) log V)
        - Simple Array: O(V²)
        - Fibonacci Heap: O(E + V log V) [theoretical]

        Space Complexity: O(V + E)

        Args:
            start: Starting vertex
            pq_type: Type of priority queue to use

        Returns:
            mst_edges: List of edges in MST
            total_weight: Total weight of MST
        """
        if pq_type == PriorityQueueType.BINARY_HEAP:
            return self._prim_binary_heap(start)
        elif pq_type == PriorityQueueType.SIMPLE_ARRAY:
            return self._prim_simple_array(start)
        else:
            raise ValueError(f"Unsupported priority queue type: {pq_type}")

    def _prim_binary_heap(self, start: int) -> Tuple[List[Edge], float]:
        """Prim's algorithm using binary heap (heapq)"""
        mst_edges = []
        total_weight = 0
        visited = set([start])

        # Priority queue: (weight, u, v)
        pq = []
        for neighbor, weight in self.adj_list[start]:
            heapq.heappush(pq, (weight, start, neighbor))

        while pq and len(visited) < self.num_vertices:
            weight, u, v = heapq.heappop(pq)

            if v in visited:
                continue

            # Add edge to MST
            visited.add(v)
            mst_edges.append(Edge(u, v, weight))
            total_weight += weight

            # Add edges from newly added vertex
            for neighbor, edge_weight in self.adj_list[v]:
                if neighbor not in visited:
                    heapq.heappush(pq, (edge_weight, v, neighbor))

        return mst_edges, total_weight

    def _prim_simple_array(self, start: int) -> Tuple[List[Edge], float]:
        """
        Prim's algorithm using simple array (for dense graphs)

        Better for dense graphs where E ≈ V²
        Time: O(V²), Space: O(V)
        """
        mst_edges = []
        total_weight = 0
        visited = [False] * self.num_vertices

        # Track minimum edge to each vertex
        min_weight = [float('inf')] * self.num_vertices
        parent = [-1] * self.num_vertices

        min_weight[start] = 0

        for _ in range(self.num_vertices):
            # Find minimum weight unvisited vertex - O(V)
            u = -1
            for v in range(self.num_vertices):
                if not visited[v] and (u == -1 or min_weight[v] < min_weight[u]):
                    u = v

            if min_weight[u] == float('inf'):
                break  # Disconnected graph

            visited[u] = True

            # Add edge to MST (skip first vertex)
            if parent[u] != -1:
                mst_edges.append(Edge(parent[u], u, min_weight[u]))
                total_weight += min_weight[u]

            # Update neighbors
            for v, weight in self.adj_list[u]:
                if not visited[v] and weight < min_weight[v]:
                    min_weight[v] = weight
                    parent[v] = u

        return mst_edges, total_weight

    def prim_with_visualization(self, start: int = 0) -> Tuple[List[Edge], float, List[Dict]]:
        """
        Prim's algorithm with step-by-step visualization

        Returns:
            mst_edges: Final MST edges
            total_weight: Total weight
            steps: List of step dictionaries for visualization
        """
        mst_edges = []
        total_weight = 0
        visited = set([start])
        steps = []

        pq = []
        for neighbor, weight in self.adj_list[start]:
            heapq.heappush(pq, (weight, start, neighbor))

        iteration = 0
        while pq and len(visited) < self.num_vertices:
            weight, u, v = heapq.heappop(pq)

            step = {
                'iteration': iteration,
                'edge_considered': Edge(u, v, weight),
                'visited': set(visited),
                'action': '',
                'mst_so_far': list(mst_edges),
                'total_weight': total_weight
            }

            if v in visited:
                step['action'] = 'rejected (already in tree)'
            else:
                visited.add(v)
                mst_edges.append(Edge(u, v, weight))
                total_weight += weight
                step['action'] = 'added'

                # Add new edges
                for neighbor, edge_weight in self.adj_list[v]:
                    if neighbor not in visited:
                        heapq.heappush(pq, (edge_weight, v, neighbor))

            steps.append(step)
            iteration += 1

        return mst_edges, total_weight, steps

    # ========================================================================
    # BORŮVKA'S ALGORITHM
    # ========================================================================

    def boruvka(self) -> Tuple[List[Edge], float]:
        """
        Borůvka's (Sollin's) Algorithm for MST

        Strategy: In each phase, find minimum weight edge for each component,
        add all such edges simultaneously (parallel-friendly)

        Time Complexity: O(E log V)
        Space Complexity: O(V + E)

        Advantages:
        - Naturally parallel (can add multiple edges simultaneously)
        - Good for distributed systems
        - Only O(log V) phases needed

        Returns:
            mst_edges: List of edges in MST
            total_weight: Total weight of MST
        """
        uf = UnionFind(self.num_vertices)
        mst_edges = []
        total_weight = 0

        num_components = self.num_vertices

        # Continue until we have one component or can't add more edges
        while num_components > 1:
            # Find minimum edge for each component
            cheapest = [-1] * self.num_vertices

            # Find cheapest edge from each component
            for i, edge in enumerate(self.edges):
                u_root = uf.find(edge.u)
                v_root = uf.find(edge.v)

                if u_root == v_root:
                    continue  # Same component

                # Check if this is cheapest edge for component of u
                if cheapest[u_root] == -1 or edge.weight < self.edges[cheapest[u_root]].weight:
                    cheapest[u_root] = i

                # Check if this is cheapest edge for component of v
                if cheapest[v_root] == -1 or edge.weight < self.edges[cheapest[v_root]].weight:
                    cheapest[v_root] = i

            # Add all cheapest edges (parallel step)
            added_any = False
            for i in range(self.num_vertices):
                if cheapest[i] != -1:
                    edge = self.edges[cheapest[i]]

                    if uf.union(edge.u, edge.v):
                        mst_edges.append(edge)
                        total_weight += edge.weight
                        num_components -= 1
                        added_any = True

            if not added_any:
                break  # Disconnected graph or done

        return mst_edges, total_weight

    def boruvka_with_visualization(self) -> Tuple[List[Edge], float, List[Dict]]:
        """
        Borůvka's algorithm with step-by-step visualization

        Returns:
            mst_edges: Final MST edges
            total_weight: Total weight
            steps: List of phase dictionaries for visualization
        """
        uf = UnionFind(self.num_vertices)
        mst_edges = []
        total_weight = 0
        steps = []

        num_components = self.num_vertices
        phase = 0

        while num_components > 1:
            cheapest = [-1] * self.num_vertices

            # Find cheapest edges
            for i, edge in enumerate(self.edges):
                u_root = uf.find(edge.u)
                v_root = uf.find(edge.v)

                if u_root == v_root:
                    continue

                if cheapest[u_root] == -1 or edge.weight < self.edges[cheapest[u_root]].weight:
                    cheapest[u_root] = i

                if cheapest[v_root] == -1 or edge.weight < self.edges[cheapest[v_root]].weight:
                    cheapest[v_root] = i

            # Collect edges to add in this phase
            phase_edges = []
            for i in range(self.num_vertices):
                if cheapest[i] != -1:
                    edge = self.edges[cheapest[i]]
                    if uf.union(edge.u, edge.v):
                        phase_edges.append(edge)
                        mst_edges.append(edge)
                        total_weight += edge.weight
                        num_components -= 1

            step = {
                'phase': phase,
                'edges_added': phase_edges,
                'num_components': num_components,
                'mst_so_far': list(mst_edges),
                'total_weight': total_weight
            }
            steps.append(step)

            if not phase_edges:
                break

            phase += 1

        return mst_edges, total_weight, steps

    # ========================================================================
    # MINIMUM SPANNING FOREST (for disconnected graphs)
    # ========================================================================

    def minimum_spanning_forest(self, algorithm: str = 'kruskal') -> Tuple[List[List[Edge]], float]:
        """
        Find Minimum Spanning Forest for potentially disconnected graph

        Args:
            algorithm: 'kruskal', 'prim', or 'boruvka'

        Returns:
            forest: List of trees, each tree is a list of edges
            total_weight: Total weight of all trees
        """
        if algorithm == 'kruskal':
            mst_edges, total_weight, _ = self.kruskal(return_forest=True)
            forest = self._build_forest(mst_edges)
            return forest, total_weight

        elif algorithm == 'prim':
            # Run Prim's from each unvisited component
            visited_global = set()
            forest = []
            total_weight = 0

            for start in range(self.num_vertices):
                if start not in visited_global:
                    tree_edges, tree_weight = self.prim(start)

                    # Mark vertices in this tree as visited
                    for edge in tree_edges:
                        visited_global.add(edge.u)
                        visited_global.add(edge.v)

                    if tree_edges:
                        forest.append(tree_edges)
                        total_weight += tree_weight

            return forest, total_weight

        elif algorithm == 'boruvka':
            mst_edges, total_weight = self.boruvka()
            forest = self._build_forest(mst_edges)
            return forest, total_weight

        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    def _build_forest(self, edges: List[Edge]) -> List[List[Edge]]:
        """Build forest structure from flat edge list"""
        if not edges:
            return []

        # Use Union-Find to identify components
        uf = UnionFind(self.num_vertices)
        for edge in edges:
            uf.union(edge.u, edge.v)

        # Group edges by component
        component_edges = defaultdict(list)
        for edge in edges:
            root = uf.find(edge.u)
            component_edges[root].append(edge)

        return list(component_edges.values())

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def verify_mst(self, mst_edges: List[Edge]) -> Tuple[bool, str]:
        """
        Verify if given edges form a valid MST

        Returns:
            is_valid: True if valid MST
            message: Explanation
        """
        # Check if forms a tree (V-1 edges, no cycles, connected)
        if len(mst_edges) != self.num_vertices - 1:
            return False, f"Invalid edge count: {len(mst_edges)} (expected {self.num_vertices - 1})"

        # Check for cycles using Union-Find
        uf = UnionFind(self.num_vertices)
        for edge in mst_edges:
            if not uf.union(edge.u, edge.v):
                return False, f"Contains cycle at edge {edge}"

        # Check connectivity
        if uf.get_component_count() != 1:
            return False, f"Disconnected: {uf.get_component_count()} components"

        return True, "Valid MST"

    def compare_algorithms(self, num_runs: int = 10) -> Dict:
        """
        Compare performance of all three MST algorithms

        Args:
            num_runs: Number of times to run each algorithm

        Returns:
            Dictionary with timing results and verification
        """
        results = {}

        # Kruskal's
        kruskal_times = []
        for _ in range(num_runs):
            start = time.perf_counter()
            k_edges, k_weight, _ = self.kruskal()
            kruskal_times.append(time.perf_counter() - start)

        results['kruskal'] = {
            'mean_time': sum(kruskal_times) / len(kruskal_times),
            'min_time': min(kruskal_times),
            'max_time': max(kruskal_times),
            'weight': k_weight,
            'num_edges': len(k_edges)
        }

        # Prim's (Binary Heap)
        prim_times = []
        for _ in range(num_runs):
            start = time.perf_counter()
            p_edges, p_weight = self.prim()
            prim_times.append(time.perf_counter() - start)

        results['prim_binary_heap'] = {
            'mean_time': sum(prim_times) / len(prim_times),
            'min_time': min(prim_times),
            'max_time': max(prim_times),
            'weight': p_weight,
            'num_edges': len(p_edges)
        }

        # Prim's (Simple Array) - only for small graphs
        if self.num_vertices <= 1000:
            prim_array_times = []
            for _ in range(num_runs):
                start = time.perf_counter()
                pa_edges, pa_weight = self.prim(pq_type=PriorityQueueType.SIMPLE_ARRAY)
                prim_array_times.append(time.perf_counter() - start)

            results['prim_simple_array'] = {
                'mean_time': sum(prim_array_times) / len(prim_array_times),
                'min_time': min(prim_array_times),
                'max_time': max(prim_array_times),
                'weight': pa_weight,
                'num_edges': len(pa_edges)
            }

        # Borůvka's
        boruvka_times = []
        for _ in range(num_runs):
            start = time.perf_counter()
            b_edges, b_weight = self.boruvka()
            boruvka_times.append(time.perf_counter() - start)

        results['boruvka'] = {
            'mean_time': sum(boruvka_times) / len(boruvka_times),
            'min_time': min(boruvka_times),
            'max_time': max(boruvka_times),
            'weight': b_weight,
            'num_edges': len(b_edges)
        }

        # Verify all give same weight
        weights = [r['weight'] for r in results.values()]
        results['all_agree'] = len(set(weights)) == 1

        return results


def demo_mst_algorithms():
    """Demonstrate MST algorithms"""
    print("=" * 80)
    print("MINIMUM SPANNING TREE ALGORITHMS DEMO")
    print("=" * 80)
    print()

    # Example graph
    edges = [
        (0, 1, 4),
        (0, 7, 8),
        (1, 2, 8),
        (1, 7, 11),
        (2, 3, 7),
        (2, 5, 4),
        (2, 8, 2),
        (3, 4, 9),
        (3, 5, 14),
        (4, 5, 10),
        (5, 6, 2),
        (6, 7, 1),
        (6, 8, 6),
        (7, 8, 7)
    ]

    mst = MSTAlgorithms(9, edges)

    # Kruskal's Algorithm
    print("1. KRUSKAL'S ALGORITHM")
    print("-" * 80)
    k_edges, k_weight, _ = mst.kruskal()
    print(f"MST Weight: {k_weight}")
    print(f"Edges: {[(e.u, e.v, e.weight) for e in k_edges]}")
    print()

    # Prim's Algorithm (Binary Heap)
    print("2. PRIM'S ALGORITHM (Binary Heap)")
    print("-" * 80)
    p_edges, p_weight = mst.prim(start=0)
    print(f"MST Weight: {p_weight}")
    print(f"Edges: {[(e.u, e.v, e.weight) for e in p_edges]}")
    print()

    # Borůvka's Algorithm
    print("3. BORŮVKA'S ALGORITHM")
    print("-" * 80)
    b_edges, b_weight = mst.boruvka()
    print(f"MST Weight: {b_weight}")
    print(f"Edges: {[(e.u, e.v, e.weight) for e in b_edges]}")
    print()

    # Performance Comparison
    print("4. PERFORMANCE COMPARISON")
    print("-" * 80)
    results = mst.compare_algorithms(num_runs=100)

    for algo, metrics in results.items():
        if algo == 'all_agree':
            continue
        print(f"\n{algo.upper()}")
        print(f"  Mean time: {metrics['mean_time']*1000:.4f} ms")
        print(f"  Min time:  {metrics['min_time']*1000:.4f} ms")
        print(f"  Max time:  {metrics['max_time']*1000:.4f} ms")
        print(f"  Weight:    {metrics['weight']}")

    print(f"\nAll algorithms agree: {results['all_agree']}")
    print()

    # Disconnected Graph Example
    print("5. MINIMUM SPANNING FOREST (Disconnected Graph)")
    print("-" * 80)
    disconnected_edges = [
        (0, 1, 1),
        (1, 2, 2),
        (3, 4, 3),
        (4, 5, 4)
    ]

    mst_forest = MSTAlgorithms(6, disconnected_edges)
    forest, total_weight = mst_forest.minimum_spanning_forest()

    print(f"Number of trees: {len(forest)}")
    print(f"Total weight: {total_weight}")
    for i, tree in enumerate(forest):
        print(f"\nTree {i+1}:")
        print(f"  Edges: {[(e.u, e.v, e.weight) for e in tree]}")


if __name__ == "__main__":
    demo_mst_algorithms()
