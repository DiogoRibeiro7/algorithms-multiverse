"""
Comprehensive Graph Data Structure Implementation
Supports multiple representations and core graph algorithms
"""

from collections import deque, defaultdict
from enum import Enum
from typing import List, Set, Dict, Tuple, Optional, Any
import random


class GraphType(Enum):
    DIRECTED = "directed"
    UNDIRECTED = "undirected"


class RepresentationType(Enum):
    ADJACENCY_LIST = "adjacency_list"
    ADJACENCY_MATRIX = "adjacency_matrix"
    EDGE_LIST = "edge_list"
    CSR = "csr"  # Compressed Sparse Row


class Graph:
    """
    Comprehensive graph implementation supporting multiple representations
    and both weighted/unweighted, directed/undirected graphs.
    """

    def __init__(self, num_vertices: int = 0,
                 graph_type: GraphType = GraphType.UNDIRECTED,
                 weighted: bool = False,
                 representation: RepresentationType = RepresentationType.ADJACENCY_LIST):
        self.num_vertices = num_vertices
        self.graph_type = graph_type
        self.weighted = weighted
        self.representation = representation
        self.num_edges = 0

        # Initialize based on representation type
        if representation == RepresentationType.ADJACENCY_LIST:
            self.adj_list: Dict[int, List[Tuple[int, float]]] = defaultdict(list)
        elif representation == RepresentationType.ADJACENCY_MATRIX:
            self.adj_matrix: List[List[Optional[float]]] = [
                [None for _ in range(num_vertices)] for _ in range(num_vertices)
            ]
        elif representation == RepresentationType.EDGE_LIST:
            self.edges: List[Tuple[int, int, float]] = []
        elif representation == RepresentationType.CSR:
            self.csr_values: List[float] = []
            self.csr_col_indices: List[int] = []
            self.csr_row_ptr: List[int] = [0]

    def add_vertex(self) -> int:
        """Add a new vertex and return its ID"""
        vertex_id = self.num_vertices
        self.num_vertices += 1

        if self.representation == RepresentationType.ADJACENCY_MATRIX:
            # Expand matrix
            for row in self.adj_matrix:
                row.append(None)
            self.adj_matrix.append([None for _ in range(self.num_vertices)])

        return vertex_id

    def add_edge(self, u: int, v: int, weight: float = 1.0):
        """Add an edge from u to v with optional weight"""
        if u >= self.num_vertices or v >= self.num_vertices:
            raise ValueError(f"Vertex out of range: {u} or {v}")

        self.num_edges += 1

        if self.representation == RepresentationType.ADJACENCY_LIST:
            self.adj_list[u].append((v, weight))
            if self.graph_type == GraphType.UNDIRECTED:
                self.adj_list[v].append((u, weight))

        elif self.representation == RepresentationType.ADJACENCY_MATRIX:
            self.adj_matrix[u][v] = weight
            if self.graph_type == GraphType.UNDIRECTED:
                self.adj_matrix[v][u] = weight

        elif self.representation == RepresentationType.EDGE_LIST:
            self.edges.append((u, v, weight))
            if self.graph_type == GraphType.UNDIRECTED:
                self.edges.append((v, u, weight))

        elif self.representation == RepresentationType.CSR:
            # CSR is typically built in batch, convert from edge list
            raise NotImplementedError("CSR edges should be added via build_csr()")

    def build_csr(self, edges: List[Tuple[int, int, float]]):
        """Build CSR representation from edge list"""
        if self.representation != RepresentationType.CSR:
            raise ValueError("Graph must be CSR type")

        # Sort edges by source vertex
        sorted_edges = sorted(edges, key=lambda x: (x[0], x[1]))

        self.csr_values = []
        self.csr_col_indices = []
        self.csr_row_ptr = [0]

        current_row = 0
        for u, v, weight in sorted_edges:
            # Fill gaps for vertices with no outgoing edges
            while current_row < u:
                self.csr_row_ptr.append(len(self.csr_col_indices))
                current_row += 1

            self.csr_values.append(weight)
            self.csr_col_indices.append(v)

        # Complete row pointers
        while current_row < self.num_vertices:
            self.csr_row_ptr.append(len(self.csr_col_indices))
            current_row += 1

        self.num_edges = len(sorted_edges)

    def get_neighbors(self, u: int) -> List[Tuple[int, float]]:
        """Get neighbors of vertex u with their edge weights"""
        if self.representation == RepresentationType.ADJACENCY_LIST:
            return self.adj_list.get(u, [])

        elif self.representation == RepresentationType.ADJACENCY_MATRIX:
            neighbors = []
            for v in range(self.num_vertices):
                if self.adj_matrix[u][v] is not None:
                    neighbors.append((v, self.adj_matrix[u][v]))
            return neighbors

        elif self.representation == RepresentationType.EDGE_LIST:
            neighbors = []
            for src, dst, weight in self.edges:
                if src == u:
                    neighbors.append((dst, weight))
            return neighbors

        elif self.representation == RepresentationType.CSR:
            start = self.csr_row_ptr[u]
            end = self.csr_row_ptr[u + 1]
            return [(self.csr_col_indices[i], self.csr_values[i])
                    for i in range(start, end)]

        return []

    # === DEPTH-FIRST SEARCH ===

    def dfs_recursive(self, start: int, visited: Optional[Set[int]] = None) -> List[int]:
        """DFS traversal using recursion"""
        if visited is None:
            visited = set()

        traversal = []

        def dfs_helper(v: int):
            visited.add(v)
            traversal.append(v)

            for neighbor, _ in self.get_neighbors(v):
                if neighbor not in visited:
                    dfs_helper(neighbor)

        dfs_helper(start)
        return traversal

    def dfs_iterative(self, start: int) -> List[int]:
        """DFS traversal using iteration with stack"""
        visited = set()
        traversal = []
        stack = [start]

        while stack:
            v = stack.pop()
            if v not in visited:
                visited.add(v)
                traversal.append(v)

                # Add neighbors in reverse order for consistent ordering
                neighbors = self.get_neighbors(v)
                for neighbor, _ in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return traversal

    # === BREADTH-FIRST SEARCH ===

    def bfs(self, start: int) -> List[int]:
        """BFS traversal"""
        visited = set([start])
        traversal = []
        queue = deque([start])

        while queue:
            v = queue.popleft()
            traversal.append(v)

            for neighbor, _ in self.get_neighbors(v):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return traversal

    # === TOPOLOGICAL SORTING ===

    def topological_sort(self) -> Optional[List[int]]:
        """
        Topological sorting using Kahn's algorithm (BFS-based).
        Returns None if graph contains a cycle.
        Only works for directed graphs.
        """
        if self.graph_type != GraphType.DIRECTED:
            raise ValueError("Topological sort only works for directed graphs")

        # Calculate in-degrees
        in_degree = [0] * self.num_vertices
        for u in range(self.num_vertices):
            for v, _ in self.get_neighbors(u):
                in_degree[v] += 1

        # Queue with vertices having 0 in-degree
        queue = deque([v for v in range(self.num_vertices) if in_degree[v] == 0])
        result = []

        while queue:
            u = queue.popleft()
            result.append(u)

            for v, _ in self.get_neighbors(u):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        # Check if all vertices were processed (no cycle)
        if len(result) != self.num_vertices:
            return None  # Cycle detected

        return result

    def topological_sort_dfs(self) -> Optional[List[int]]:
        """Topological sorting using DFS"""
        if self.graph_type != GraphType.DIRECTED:
            raise ValueError("Topological sort only works for directed graphs")

        visited = set()
        rec_stack = set()
        result = []

        def dfs_helper(v: int) -> bool:
            visited.add(v)
            rec_stack.add(v)

            for neighbor, _ in self.get_neighbors(v):
                if neighbor not in visited:
                    if not dfs_helper(neighbor):
                        return False
                elif neighbor in rec_stack:
                    return False  # Cycle detected

            rec_stack.remove(v)
            result.append(v)
            return True

        for v in range(self.num_vertices):
            if v not in visited:
                if not dfs_helper(v):
                    return None  # Cycle detected

        return result[::-1]  # Reverse to get correct order

    # === CONNECTED COMPONENTS ===

    def find_connected_components(self) -> List[List[int]]:
        """Find all connected components in the graph"""
        visited = set()
        components = []

        for v in range(self.num_vertices):
            if v not in visited:
                component = []
                stack = [v]

                while stack:
                    u = stack.pop()
                    if u not in visited:
                        visited.add(u)
                        component.append(u)

                        for neighbor, _ in self.get_neighbors(u):
                            if neighbor not in visited:
                                stack.append(neighbor)

                components.append(sorted(component))

        return components

    def is_connected(self) -> bool:
        """Check if graph is connected"""
        if self.num_vertices == 0:
            return True
        return len(self.find_connected_components()) == 1

    # === CYCLE DETECTION ===

    def has_cycle_undirected(self) -> bool:
        """Detect cycle in undirected graph using DFS"""
        if self.graph_type != GraphType.UNDIRECTED:
            raise ValueError("This method is for undirected graphs")

        visited = set()

        def dfs_helper(v: int, parent: int) -> bool:
            visited.add(v)

            for neighbor, _ in self.get_neighbors(v):
                if neighbor not in visited:
                    if dfs_helper(neighbor, v):
                        return True
                elif neighbor != parent:
                    return True  # Cycle found

            return False

        for v in range(self.num_vertices):
            if v not in visited:
                if dfs_helper(v, -1):
                    return True

        return False

    def has_cycle_directed(self) -> bool:
        """Detect cycle in directed graph using DFS with recursion stack"""
        if self.graph_type != GraphType.DIRECTED:
            raise ValueError("This method is for directed graphs")

        visited = set()
        rec_stack = set()

        def dfs_helper(v: int) -> bool:
            visited.add(v)
            rec_stack.add(v)

            for neighbor, _ in self.get_neighbors(v):
                if neighbor not in visited:
                    if dfs_helper(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True  # Back edge found

            rec_stack.remove(v)
            return False

        for v in range(self.num_vertices):
            if v not in visited:
                if dfs_helper(v):
                    return True

        return False

    def has_cycle(self) -> bool:
        """Detect cycle based on graph type"""
        if self.graph_type == GraphType.DIRECTED:
            return self.has_cycle_directed()
        else:
            return self.has_cycle_undirected()

    # === GRAPH COLORING ===

    def greedy_coloring(self) -> Dict[int, int]:
        """
        Graph coloring using greedy algorithm.
        Returns mapping of vertex -> color.
        """
        colors = {}

        for v in range(self.num_vertices):
            # Get colors of neighbors
            neighbor_colors = set()
            for neighbor, _ in self.get_neighbors(v):
                if neighbor in colors:
                    neighbor_colors.add(colors[neighbor])

            # Find first available color
            color = 0
            while color in neighbor_colors:
                color += 1

            colors[v] = color

        return colors

    def chromatic_number_upper_bound(self) -> int:
        """Get upper bound on chromatic number"""
        coloring = self.greedy_coloring()
        return max(coloring.values()) + 1 if coloring else 0

    # === VISUALIZATION ===

    def to_ascii(self, max_width: int = 80) -> str:
        """Generate ASCII art representation of the graph"""
        lines = []
        lines.append("=" * max_width)
        lines.append(f"Graph: {self.graph_type.value}, "
                    f"{'weighted' if self.weighted else 'unweighted'}")
        lines.append(f"Representation: {self.representation.value}")
        lines.append(f"Vertices: {self.num_vertices}, Edges: {self.num_edges}")
        lines.append("=" * max_width)
        lines.append("")

        if self.representation == RepresentationType.ADJACENCY_LIST:
            lines.append("Adjacency List:")
            for v in range(self.num_vertices):
                neighbors = self.get_neighbors(v)
                if neighbors:
                    neighbor_str = ", ".join([
                        f"{n}({w:.1f})" if self.weighted else str(n)
                        for n, w in neighbors
                    ])
                    lines.append(f"  {v} -> [{neighbor_str}]")
                else:
                    lines.append(f"  {v} -> []")

        elif self.representation == RepresentationType.ADJACENCY_MATRIX:
            lines.append("Adjacency Matrix:")
            # Header
            header = "    " + " ".join([f"{i:4}" for i in range(min(self.num_vertices, 15))])
            lines.append(header)
            lines.append("    " + "-" * (5 * min(self.num_vertices, 15)))

            for i in range(min(self.num_vertices, 15)):
                row_vals = []
                for j in range(min(self.num_vertices, 15)):
                    val = self.adj_matrix[i][j]
                    if val is None:
                        row_vals.append("   .")
                    else:
                        row_vals.append(f"{val:4.0f}")
                lines.append(f"{i:2} |" + " ".join(row_vals))

            if self.num_vertices > 15:
                lines.append("  ... (truncated)")

        elif self.representation == RepresentationType.EDGE_LIST:
            lines.append("Edge List:")
            for i, (u, v, w) in enumerate(self.edges[:50]):  # Limit display
                if self.weighted:
                    lines.append(f"  {i}: {u} -> {v} (weight: {w:.1f})")
                else:
                    lines.append(f"  {i}: {u} -> {v}")
            if len(self.edges) > 50:
                lines.append(f"  ... ({len(self.edges) - 50} more edges)")

        elif self.representation == RepresentationType.CSR:
            lines.append("CSR (Compressed Sparse Row):")
            lines.append(f"  Values: {self.csr_values[:20]}{'...' if len(self.csr_values) > 20 else ''}")
            lines.append(f"  Col Indices: {self.csr_col_indices[:20]}{'...' if len(self.csr_col_indices) > 20 else ''}")
            lines.append(f"  Row Ptrs: {self.csr_row_ptr[:20]}{'...' if len(self.csr_row_ptr) > 20 else ''}")

        lines.append("")
        lines.append("=" * max_width)

        return "\n".join(lines)

    def __str__(self) -> str:
        return self.to_ascii()

    # === MEMORY AND PERFORMANCE ANALYSIS ===

    def memory_usage(self) -> Dict[str, Any]:
        """Estimate memory usage of current representation"""
        import sys

        stats = {
            "representation": self.representation.value,
            "vertices": self.num_vertices,
            "edges": self.num_edges
        }

        if self.representation == RepresentationType.ADJACENCY_LIST:
            size = sys.getsizeof(self.adj_list)
            for v in self.adj_list:
                size += sys.getsizeof(self.adj_list[v])
                for edge in self.adj_list[v]:
                    size += sys.getsizeof(edge)
            stats["bytes"] = size
            stats["avg_bytes_per_edge"] = size / max(self.num_edges, 1)

        elif self.representation == RepresentationType.ADJACENCY_MATRIX:
            stats["bytes"] = sys.getsizeof(self.adj_matrix) + \
                           self.num_vertices * self.num_vertices * sys.getsizeof(None)
            stats["space_complexity"] = f"O(V²) = O({self.num_vertices}²)"

        elif self.representation == RepresentationType.EDGE_LIST:
            stats["bytes"] = sys.getsizeof(self.edges) + \
                           len(self.edges) * sys.getsizeof((0, 0, 0.0))
            stats["space_complexity"] = f"O(E) = O({self.num_edges})"

        elif self.representation == RepresentationType.CSR:
            stats["bytes"] = (sys.getsizeof(self.csr_values) +
                           sys.getsizeof(self.csr_col_indices) +
                           sys.getsizeof(self.csr_row_ptr))
            stats["space_complexity"] = f"O(V+E) = O({self.num_vertices}+{self.num_edges})"

        return stats


# === GRAPH GENERATORS ===

class GraphGenerator:
    """Utilities for generating test graphs"""

    @staticmethod
    def complete_graph(n: int, graph_type: GraphType = GraphType.UNDIRECTED,
                      representation: RepresentationType = RepresentationType.ADJACENCY_LIST) -> Graph:
        """Generate a complete graph with n vertices"""
        g = Graph(n, graph_type, False, representation)

        if representation == RepresentationType.CSR:
            edges = []
            for i in range(n):
                for j in range(n):
                    if i != j:
                        edges.append((i, j, 1.0))
                        if graph_type == GraphType.UNDIRECTED:
                            break
            g.build_csr(edges)
        else:
            for i in range(n):
                for j in range(i + 1, n):
                    g.add_edge(i, j)
                    if graph_type == GraphType.DIRECTED:
                        g.add_edge(j, i)

        return g

    @staticmethod
    def cycle_graph(n: int, graph_type: GraphType = GraphType.UNDIRECTED,
                   representation: RepresentationType = RepresentationType.ADJACENCY_LIST) -> Graph:
        """Generate a cycle graph with n vertices"""
        g = Graph(n, graph_type, False, representation)

        if representation == RepresentationType.CSR:
            edges = [(i, (i + 1) % n, 1.0) for i in range(n)]
            if graph_type == GraphType.UNDIRECTED:
                edges += [((i + 1) % n, i, 1.0) for i in range(n)]
            g.build_csr(edges)
        else:
            for i in range(n):
                g.add_edge(i, (i + 1) % n)

        return g

    @staticmethod
    def random_graph(n: int, edge_probability: float,
                    graph_type: GraphType = GraphType.UNDIRECTED,
                    weighted: bool = False,
                    representation: RepresentationType = RepresentationType.ADJACENCY_LIST) -> Graph:
        """Generate random graph with Erdős-Rényi model"""
        g = Graph(n, graph_type, weighted, representation)

        edges = []
        for i in range(n):
            start = i + 1 if graph_type == GraphType.UNDIRECTED else 0
            for j in range(start, n):
                if i != j and random.random() < edge_probability:
                    weight = random.uniform(1.0, 10.0) if weighted else 1.0
                    edges.append((i, j, weight))

        if representation == RepresentationType.CSR:
            if graph_type == GraphType.UNDIRECTED:
                edges += [(v, u, w) for u, v, w in edges]
            g.build_csr(sorted(edges))
        else:
            for u, v, w in edges:
                g.add_edge(u, v, w)

        return g

    @staticmethod
    def dag(n: int, edge_probability: float,
           representation: RepresentationType = RepresentationType.ADJACENCY_LIST) -> Graph:
        """Generate a random Directed Acyclic Graph (DAG)"""
        g = Graph(n, GraphType.DIRECTED, False, representation)

        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < edge_probability:
                    edges.append((i, j, 1.0))

        if representation == RepresentationType.CSR:
            g.build_csr(edges)
        else:
            for u, v, w in edges:
                g.add_edge(u, v, w)

        return g


# === DEMO AND TESTING ===

def demo():
    """Demonstrate graph functionality"""
    print("=" * 80)
    print("GRAPH DATA STRUCTURES AND ALGORITHMS DEMO")
    print("=" * 80)
    print()

    # Demo 1: Adjacency List
    print("1. ADJACENCY LIST REPRESENTATION")
    print("-" * 80)
    g1 = Graph(5, GraphType.UNDIRECTED, False, RepresentationType.ADJACENCY_LIST)
    g1.add_edge(0, 1)
    g1.add_edge(0, 4)
    g1.add_edge(1, 2)
    g1.add_edge(1, 3)
    g1.add_edge(1, 4)
    g1.add_edge(2, 3)
    g1.add_edge(3, 4)
    print(g1)
    print()

    # Demo 2: DFS and BFS
    print("2. GRAPH TRAVERSAL")
    print("-" * 80)
    print(f"DFS Recursive from 0: {g1.dfs_recursive(0)}")
    print(f"DFS Iterative from 0: {g1.dfs_iterative(0)}")
    print(f"BFS from 0: {g1.bfs(0)}")
    print()

    # Demo 3: Connected Components
    print("3. CONNECTED COMPONENTS")
    print("-" * 80)
    g2 = Graph(7, GraphType.UNDIRECTED)
    g2.add_edge(0, 1)
    g2.add_edge(1, 2)
    g2.add_edge(3, 4)
    g2.add_edge(5, 6)
    components = g2.find_connected_components()
    print(f"Components: {components}")
    print(f"Is connected: {g2.is_connected()}")
    print()

    # Demo 4: Cycle Detection
    print("4. CYCLE DETECTION")
    print("-" * 80)
    print(f"Graph g1 has cycle: {g1.has_cycle()}")
    g3 = Graph(3, GraphType.UNDIRECTED)
    g3.add_edge(0, 1)
    g3.add_edge(1, 2)
    print(f"Linear graph has cycle: {g3.has_cycle()}")
    print()

    # Demo 5: Topological Sort
    print("5. TOPOLOGICAL SORTING")
    print("-" * 80)
    dag = GraphGenerator.dag(6, 0.3)
    print(dag)
    topo = dag.topological_sort()
    print(f"Topological order: {topo}")
    topo_dfs = dag.topological_sort_dfs()
    print(f"Topological order (DFS): {topo_dfs}")
    print()

    # Demo 6: Graph Coloring
    print("6. GRAPH COLORING")
    print("-" * 80)
    coloring = g1.greedy_coloring()
    print(f"Greedy coloring: {coloring}")
    print(f"Chromatic number (upper bound): {g1.chromatic_number_upper_bound()}")
    print()

    # Demo 7: Different Representations
    print("7. ADJACENCY MATRIX REPRESENTATION")
    print("-" * 80)
    g4 = Graph(5, GraphType.DIRECTED, True, RepresentationType.ADJACENCY_MATRIX)
    g4.add_edge(0, 1, 2.5)
    g4.add_edge(0, 2, 1.0)
    g4.add_edge(1, 3, 3.0)
    g4.add_edge(2, 3, 1.5)
    g4.add_edge(3, 4, 2.0)
    print(g4)
    print()

    # Demo 8: Performance Comparison
    print("8. MEMORY USAGE ANALYSIS")
    print("-" * 80)
    sizes = [10, 50, 100]
    for size in sizes:
        g_list = GraphGenerator.random_graph(size, 0.3, representation=RepresentationType.ADJACENCY_LIST)
        g_matrix = GraphGenerator.random_graph(size, 0.3, representation=RepresentationType.ADJACENCY_MATRIX)

        mem_list = g_list.memory_usage()
        mem_matrix = g_matrix.memory_usage()

        print(f"\nGraph size: {size} vertices")
        print(f"  Adjacency List: {mem_list['bytes']} bytes")
        print(f"  Adjacency Matrix: {mem_matrix['bytes']} bytes")
    print()

    # Demo 9: Graph Generators
    print("9. GRAPH GENERATORS")
    print("-" * 80)
    complete = GraphGenerator.complete_graph(5)
    print("Complete graph K5:")
    print(complete)
    print()

    cycle = GraphGenerator.cycle_graph(6)
    print("Cycle graph C6:")
    print(cycle)
    print()


if __name__ == "__main__":
    demo()
