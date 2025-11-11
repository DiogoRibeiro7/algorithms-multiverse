"""
Advanced Graph Algorithms Extension
Includes shortest path, MST, and other advanced algorithms

This extends the basic Graph class from graph.py
"""

import heapq
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set
from graph import Graph, GraphType, RepresentationType


class UnionFind:
    """Union-Find data structure for Kruskal's algorithm"""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        """Find with path compression"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union by rank, returns True if union happened"""
        px, py = self.find(x), self.find(y)

        if px == py:
            return False

        if self.rank[px] < self.rank[py]:
            px, py = py, px

        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

        return True


class AdvancedGraph(Graph):
    """Extended Graph with advanced algorithms"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_graph(cls, graph: Graph) -> 'AdvancedGraph':
        """Create an AdvancedGraph from a regular Graph"""
        adv_graph = cls(graph.num_vertices, graph.graph_type, graph.weighted, graph.representation)

        # Copy all edges
        for u in range(graph.num_vertices):
            for v, weight in graph.get_neighbors(u):
                # Only add once for undirected graphs (u < v to avoid duplicates)
                if graph.graph_type == GraphType.DIRECTED or u < v:
                    adv_graph.add_edge(u, v, weight)

        return adv_graph

    # ========================================================================
    # SHORTEST PATH ALGORITHMS
    # ========================================================================

    def dijkstra(self, source: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
        """
        Dijkstra's shortest path algorithm

        Returns:
            distances: Dict mapping vertex -> shortest distance from source
            predecessors: Dict mapping vertex -> predecessor in shortest path
        """
        if not self.weighted:
            raise ValueError("Dijkstra requires weighted graph (use BFS for unweighted)")

        distances = {v: float('inf') for v in range(self.num_vertices)}
        distances[source] = 0
        predecessors = {v: None for v in range(self.num_vertices)}

        # Priority queue: (distance, vertex)
        pq = [(0, source)]
        visited = set()

        while pq:
            dist, u = heapq.heappop(pq)

            if u in visited:
                continue
            visited.add(u)

            if dist > distances[u]:
                continue

            for v, weight in self.get_neighbors(u):
                new_dist = distances[u] + weight

                if new_dist < distances[v]:
                    distances[v] = new_dist
                    predecessors[v] = u
                    heapq.heappush(pq, (new_dist, v))

        return distances, predecessors

    def get_shortest_path(self, source: int, target: int) -> Optional[List[int]]:
        """Get shortest path from source to target using Dijkstra"""
        distances, predecessors = self.dijkstra(source)

        if distances[target] == float('inf'):
            return None  # No path exists

        # Reconstruct path
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = predecessors[current]

        return path[::-1]

    def bellman_ford(self, source: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]], bool]:
        """
        Bellman-Ford shortest path algorithm (handles negative weights)

        Returns:
            distances: Dict mapping vertex -> shortest distance
            predecessors: Dict mapping vertex -> predecessor
            has_negative_cycle: True if negative cycle detected
        """
        distances = {v: float('inf') for v in range(self.num_vertices)}
        distances[source] = 0
        predecessors = {v: None for v in range(self.num_vertices)}

        # Relax edges V-1 times
        for _ in range(self.num_vertices - 1):
            updated = False
            for u in range(self.num_vertices):
                if distances[u] == float('inf'):
                    continue

                for v, weight in self.get_neighbors(u):
                    new_dist = distances[u] + weight
                    if new_dist < distances[v]:
                        distances[v] = new_dist
                        predecessors[v] = u
                        updated = True

            if not updated:
                break  # Early termination

        # Check for negative cycles
        has_negative_cycle = False
        for u in range(self.num_vertices):
            if distances[u] == float('inf'):
                continue

            for v, weight in self.get_neighbors(u):
                if distances[u] + weight < distances[v]:
                    has_negative_cycle = True
                    break

            if has_negative_cycle:
                break

        return distances, predecessors, has_negative_cycle

    def floyd_warshall(self) -> Tuple[List[List[float]], List[List[Optional[int]]]]:
        """
        Floyd-Warshall all-pairs shortest path algorithm

        Returns:
            distances: 2D list of shortest distances between all pairs
            next_vertex: 2D list for path reconstruction
        """
        INF = float('inf')
        n = self.num_vertices

        # Initialize distance matrix
        dist = [[INF] * n for _ in range(n)]
        next_v = [[None] * n for _ in range(n)]

        # Distance from vertex to itself is 0
        for i in range(n):
            dist[i][i] = 0

        # Add edges
        for u in range(n):
            for v, weight in self.get_neighbors(u):
                dist[u][v] = weight
                next_v[u][v] = v

        # Floyd-Warshall main loop
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_v[i][j] = next_v[i][k]

        return dist, next_v

    def reconstruct_path_floyd(self, next_v: List[List[Optional[int]]],
                               source: int, target: int) -> Optional[List[int]]:
        """Reconstruct path from Floyd-Warshall next_vertex matrix"""
        if next_v[source][target] is None:
            return None

        path = [source]
        while source != target:
            source = next_v[source][target]
            path.append(source)

        return path

    # ========================================================================
    # MINIMUM SPANNING TREE ALGORITHMS
    # ========================================================================

    def prim_mst(self, start: int = 0) -> Tuple[List[Tuple[int, int, float]], float]:
        """
        Prim's algorithm for Minimum Spanning Tree

        Returns:
            mst_edges: List of (u, v, weight) tuples
            total_weight: Total weight of MST
        """
        if self.graph_type == GraphType.DIRECTED:
            raise ValueError("MST requires undirected graph")

        if not self.weighted:
            raise ValueError("MST requires weighted graph")

        mst_edges = []
        total_weight = 0
        visited = set()

        # Priority queue: (weight, u, v)
        pq = []
        visited.add(start)

        # Add all edges from start vertex
        for v, weight in self.get_neighbors(start):
            heapq.heappush(pq, (weight, start, v))

        while pq and len(visited) < self.num_vertices:
            weight, u, v = heapq.heappop(pq)

            if v in visited:
                continue

            visited.add(v)
            mst_edges.append((u, v, weight))
            total_weight += weight

            # Add edges from newly added vertex
            for w, edge_weight in self.get_neighbors(v):
                if w not in visited:
                    heapq.heappush(pq, (edge_weight, v, w))

        return mst_edges, total_weight

    def kruskal_mst(self) -> Tuple[List[Tuple[int, int, float]], float]:
        """
        Kruskal's algorithm for Minimum Spanning Tree

        Returns:
            mst_edges: List of (u, v, weight) tuples
            total_weight: Total weight of MST
        """
        if self.graph_type == GraphType.DIRECTED:
            raise ValueError("MST requires undirected graph")

        if not self.weighted:
            raise ValueError("MST requires weighted graph")

        # Collect all edges
        edges = []
        seen_edges = set()

        for u in range(self.num_vertices):
            for v, weight in self.get_neighbors(u):
                # Avoid duplicate edges in undirected graph
                edge = tuple(sorted([u, v]))
                if edge not in seen_edges:
                    seen_edges.add(edge)
                    edges.append((weight, u, v))

        # Sort edges by weight
        edges.sort()

        # Use Union-Find
        uf = UnionFind(self.num_vertices)
        mst_edges = []
        total_weight = 0

        for weight, u, v in edges:
            if uf.union(u, v):
                mst_edges.append((u, v, weight))
                total_weight += weight

                if len(mst_edges) == self.num_vertices - 1:
                    break

        return mst_edges, total_weight

    # ========================================================================
    # ADDITIONAL ALGORITHMS
    # ========================================================================

    def is_bipartite(self) -> Tuple[bool, Optional[Dict[int, int]]]:
        """
        Check if graph is bipartite using 2-coloring

        Returns:
            is_bipartite: True if graph is bipartite
            coloring: Dict mapping vertex -> color (0 or 1), None if not bipartite
        """
        color = {}

        for start in range(self.num_vertices):
            if start in color:
                continue

            # BFS coloring
            queue = [start]
            color[start] = 0

            while queue:
                u = queue.pop(0)

                for v, _ in self.get_neighbors(u):
                    if v not in color:
                        color[v] = 1 - color[u]
                        queue.append(v)
                    elif color[v] == color[u]:
                        return False, None

        return True, color

    def strongly_connected_components(self) -> List[List[int]]:
        """
        Find strongly connected components using Kosaraju's algorithm
        Only for directed graphs
        """
        if self.graph_type != GraphType.DIRECTED:
            raise ValueError("SCC only applicable to directed graphs")

        # Step 1: DFS to get finish times
        visited = set()
        finish_stack = []

        def dfs1(v):
            visited.add(v)
            for neighbor, _ in self.get_neighbors(v):
                if neighbor not in visited:
                    dfs1(neighbor)
            finish_stack.append(v)

        for v in range(self.num_vertices):
            if v not in visited:
                dfs1(v)

        # Step 2: Create transpose graph
        transpose_adj = defaultdict(list)
        for u in range(self.num_vertices):
            for v, weight in self.get_neighbors(u):
                transpose_adj[v].append((u, weight))

        # Step 3: DFS on transpose in reverse finish order
        visited.clear()
        sccs = []

        def dfs2(v, component):
            visited.add(v)
            component.append(v)
            for neighbor, _ in transpose_adj[v]:
                if neighbor not in visited:
                    dfs2(neighbor, component)

        while finish_stack:
            v = finish_stack.pop()
            if v not in visited:
                component = []
                dfs2(v, component)
                sccs.append(sorted(component))

        return sccs

    def articulation_points(self) -> Set[int]:
        """
        Find articulation points (cut vertices) using Tarjan's algorithm
        Only for undirected graphs
        """
        if self.graph_type != GraphType.UNDIRECTED:
            raise ValueError("Articulation points only for undirected graphs")

        visited = set()
        disc = {}  # Discovery time
        low = {}   # Lowest discovery time reachable
        parent = {}
        ap = set()  # Articulation points
        time = [0]  # Use list to allow modification in nested function

        def dfs(u):
            children = 0
            visited.add(u)
            disc[u] = low[u] = time[0]
            time[0] += 1

            for v, _ in self.get_neighbors(u):
                if v not in visited:
                    children += 1
                    parent[v] = u
                    dfs(v)

                    low[u] = min(low[u], low[v])

                    # Check if u is articulation point
                    if parent.get(u) is None and children > 1:
                        ap.add(u)  # Root with multiple children

                    if parent.get(u) is not None and low[v] >= disc[u]:
                        ap.add(u)

                elif v != parent.get(u):
                    low[u] = min(low[u], disc[v])

        for v in range(self.num_vertices):
            if v not in visited:
                parent[v] = None
                dfs(v)

        return ap

    def bridges(self) -> List[Tuple[int, int]]:
        """
        Find bridges (cut edges) using Tarjan's algorithm
        Only for undirected graphs
        """
        if self.graph_type != GraphType.UNDIRECTED:
            raise ValueError("Bridges only for undirected graphs")

        visited = set()
        disc = {}
        low = {}
        parent = {}
        bridges_list = []
        time = [0]

        def dfs(u):
            visited.add(u)
            disc[u] = low[u] = time[0]
            time[0] += 1

            for v, _ in self.get_neighbors(u):
                if v not in visited:
                    parent[v] = u
                    dfs(v)

                    low[u] = min(low[u], low[v])

                    # Check if u-v is a bridge
                    if low[v] > disc[u]:
                        bridges_list.append((u, v))

                elif v != parent.get(u):
                    low[u] = min(low[u], disc[v])

        for v in range(self.num_vertices):
            if v not in visited:
                parent[v] = None
                dfs(v)

        return bridges_list

    def max_flow(self, source: int, sink: int) -> float:
        """
        Ford-Fulkerson algorithm with BFS (Edmonds-Karp) for maximum flow
        """
        # Create residual graph
        residual = [[0.0] * self.num_vertices for _ in range(self.num_vertices)]

        for u in range(self.num_vertices):
            for v, capacity in self.get_neighbors(u):
                residual[u][v] = capacity

        def bfs_find_path():
            """Find augmenting path using BFS"""
            visited = set([source])
            parent = {source: None}
            queue = [source]

            while queue:
                u = queue.pop(0)

                if u == sink:
                    # Reconstruct path
                    path = []
                    current = sink
                    while current != source:
                        path.append(current)
                        current = parent[current]
                    path.append(source)
                    return path[::-1]

                for v in range(self.num_vertices):
                    if v not in visited and residual[u][v] > 0:
                        visited.add(v)
                        parent[v] = u
                        queue.append(v)

            return None

        max_flow_value = 0

        while True:
            path = bfs_find_path()
            if path is None:
                break

            # Find minimum capacity along path
            min_capacity = float('inf')
            for i in range(len(path) - 1):
                min_capacity = min(min_capacity, residual[path[i]][path[i+1]])

            # Update residual graph
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                residual[u][v] -= min_capacity
                residual[v][u] += min_capacity

            max_flow_value += min_capacity

        return max_flow_value


def demo_advanced():
    """Demonstrate advanced algorithms"""
    print("=" * 80)
    print("ADVANCED GRAPH ALGORITHMS DEMO")
    print("=" * 80)
    print()

    # Dijkstra's Algorithm
    print("1. DIJKSTRA'S SHORTEST PATH")
    print("-" * 80)
    g1 = AdvancedGraph(5, GraphType.DIRECTED, True)
    g1.add_edge(0, 1, 10)
    g1.add_edge(0, 2, 3)
    g1.add_edge(1, 2, 1)
    g1.add_edge(1, 3, 2)
    g1.add_edge(2, 1, 4)
    g1.add_edge(2, 3, 8)
    g1.add_edge(2, 4, 2)
    g1.add_edge(3, 4, 7)
    g1.add_edge(4, 3, 9)

    distances, _ = g1.dijkstra(0)
    print(f"Shortest distances from vertex 0: {distances}")

    path = g1.get_shortest_path(0, 4)
    print(f"Shortest path 0 -> 4: {path}")
    print()

    # Minimum Spanning Tree
    print("2. MINIMUM SPANNING TREE")
    print("-" * 80)
    g2 = AdvancedGraph(4, GraphType.UNDIRECTED, True)
    g2.add_edge(0, 1, 10)
    g2.add_edge(0, 2, 6)
    g2.add_edge(0, 3, 5)
    g2.add_edge(1, 3, 15)
    g2.add_edge(2, 3, 4)

    mst_prim, weight_prim = g2.prim_mst(0)
    print(f"Prim's MST: {mst_prim}")
    print(f"Total weight: {weight_prim}")

    mst_kruskal, weight_kruskal = g2.kruskal_mst()
    print(f"Kruskal's MST: {mst_kruskal}")
    print(f"Total weight: {weight_kruskal}")
    print()

    # Bipartite Check
    print("3. BIPARTITE CHECK")
    print("-" * 80)
    g3 = AdvancedGraph(4, GraphType.UNDIRECTED)
    g3.add_edge(0, 1)
    g3.add_edge(0, 3)
    g3.add_edge(1, 2)
    g3.add_edge(2, 3)

    is_bip, coloring = g3.is_bipartite()
    print(f"Is bipartite: {is_bip}")
    print(f"Coloring: {coloring}")
    print()

    # Strongly Connected Components
    print("4. STRONGLY CONNECTED COMPONENTS")
    print("-" * 80)
    g4 = AdvancedGraph(8, GraphType.DIRECTED)
    g4.add_edge(0, 1)
    g4.add_edge(1, 2)
    g4.add_edge(2, 0)
    g4.add_edge(2, 3)
    g4.add_edge(3, 4)
    g4.add_edge(4, 5)
    g4.add_edge(5, 3)
    g4.add_edge(6, 5)
    g4.add_edge(6, 7)
    g4.add_edge(7, 6)

    sccs = g4.strongly_connected_components()
    print(f"Strongly connected components: {sccs}")
    print()

    # Articulation Points and Bridges
    print("5. ARTICULATION POINTS AND BRIDGES")
    print("-" * 80)
    g5 = AdvancedGraph(5, GraphType.UNDIRECTED)
    g5.add_edge(0, 1)
    g5.add_edge(1, 2)
    g5.add_edge(2, 0)
    g5.add_edge(1, 3)
    g5.add_edge(3, 4)

    ap = g5.articulation_points()
    bridges = g5.bridges()
    print(f"Articulation points: {ap}")
    print(f"Bridges: {bridges}")
    print()


if __name__ == "__main__":
    demo_advanced()
