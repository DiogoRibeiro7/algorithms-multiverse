"""
Extended Graph Generators
Includes various specialized graph types for testing and analysis
"""

import random
import math
from graph import Graph, GraphType, RepresentationType


class ExtendedGraphGenerator:
    """Extended graph generation utilities"""

    @staticmethod
    def bipartite_graph(n1: int, n2: int, edge_probability: float = 0.5,
                       weighted: bool = False) -> Graph:
        """
        Generate random bipartite graph

        Args:
            n1: Number of vertices in first set
            n2: Number of vertices in second set
            edge_probability: Probability of edge between sets
            weighted: Whether to add random weights
        """
        g = Graph(n1 + n2, GraphType.UNDIRECTED, weighted)

        for i in range(n1):
            for j in range(n1, n1 + n2):
                if random.random() < edge_probability:
                    weight = random.uniform(1.0, 10.0) if weighted else 1.0
                    g.add_edge(i, j, weight)

        return g

    @staticmethod
    def complete_bipartite(n1: int, n2: int, weighted: bool = False) -> Graph:
        """Generate complete bipartite graph K(n1, n2)"""
        g = Graph(n1 + n2, GraphType.UNDIRECTED, weighted)

        for i in range(n1):
            for j in range(n1, n1 + n2):
                weight = random.uniform(1.0, 10.0) if weighted else 1.0
                g.add_edge(i, j, weight)

        return g

    @staticmethod
    def tree(n: int, weighted: bool = False) -> Graph:
        """
        Generate random tree (connected acyclic graph)
        Uses Prüfer sequence
        """
        if n <= 1:
            return Graph(n, GraphType.UNDIRECTED, weighted)

        # Generate random Prüfer sequence
        prufer = [random.randint(0, n - 1) for _ in range(n - 2)]

        # Convert to tree
        g = Graph(n, GraphType.UNDIRECTED, weighted)

        # Count degrees
        degree = [1] * n
        for node in prufer:
            degree[node] += 1

        # Build tree from Prüfer sequence
        for node in prufer:
            # Find leaf with smallest label
            for leaf in range(n):
                if degree[leaf] == 1:
                    weight = random.uniform(1.0, 10.0) if weighted else 1.0
                    g.add_edge(leaf, node, weight)
                    degree[leaf] -= 1
                    degree[node] -= 1
                    break

        # Connect last two vertices with degree 1
        leaves = [i for i in range(n) if degree[i] == 1]
        if len(leaves) == 2:
            weight = random.uniform(1.0, 10.0) if weighted else 1.0
            g.add_edge(leaves[0], leaves[1], weight)

        return g

    @staticmethod
    def binary_tree(levels: int, weighted: bool = False) -> Graph:
        """Generate complete binary tree"""
        n = 2 ** levels - 1
        g = Graph(n, GraphType.UNDIRECTED, weighted)

        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n:
                weight = random.uniform(1.0, 10.0) if weighted else 1.0
                g.add_edge(i, left, weight)

            if right < n:
                weight = random.uniform(1.0, 10.0) if weighted else 1.0
                g.add_edge(i, right, weight)

        return g

    @staticmethod
    def star_graph(n: int, weighted: bool = False) -> Graph:
        """Generate star graph (one center connected to all others)"""
        g = Graph(n, GraphType.UNDIRECTED, weighted)

        for i in range(1, n):
            weight = random.uniform(1.0, 10.0) if weighted else 1.0
            g.add_edge(0, i, weight)

        return g

    @staticmethod
    def wheel_graph(n: int, weighted: bool = False) -> Graph:
        """Generate wheel graph (cycle with center vertex)"""
        if n < 4:
            raise ValueError("Wheel graph requires at least 4 vertices")

        g = Graph(n, GraphType.UNDIRECTED, weighted)

        # Create cycle for outer vertices
        for i in range(1, n - 1):
            weight = random.uniform(1.0, 10.0) if weighted else 1.0
            g.add_edge(i, i + 1, weight)

        weight = random.uniform(1.0, 10.0) if weighted else 1.0
        g.add_edge(n - 1, 1, weight)

        # Connect center (vertex 0) to all others
        for i in range(1, n):
            weight = random.uniform(1.0, 10.0) if weighted else 1.0
            g.add_edge(0, i, weight)

        return g

    @staticmethod
    def grid_graph(rows: int, cols: int, weighted: bool = False,
                  diagonal: bool = False) -> Graph:
        """
        Generate 2D grid graph

        Args:
            rows: Number of rows
            cols: Number of columns
            weighted: Whether to add random weights
            diagonal: Whether to include diagonal connections
        """
        n = rows * cols
        g = Graph(n, GraphType.UNDIRECTED, weighted)

        def get_vertex(r: int, c: int) -> int:
            return r * cols + c

        for r in range(rows):
            for c in range(cols):
                v = get_vertex(r, c)

                # Right neighbor
                if c < cols - 1:
                    weight = random.uniform(1.0, 10.0) if weighted else 1.0
                    g.add_edge(v, get_vertex(r, c + 1), weight)

                # Bottom neighbor
                if r < rows - 1:
                    weight = random.uniform(1.0, 10.0) if weighted else 1.0
                    g.add_edge(v, get_vertex(r + 1, c), weight)

                # Diagonal neighbors
                if diagonal:
                    if r < rows - 1 and c < cols - 1:
                        weight = random.uniform(1.0, 10.0) if weighted else 1.0
                        g.add_edge(v, get_vertex(r + 1, c + 1), weight)

                    if r < rows - 1 and c > 0:
                        weight = random.uniform(1.0, 10.0) if weighted else 1.0
                        g.add_edge(v, get_vertex(r + 1, c - 1), weight)

        return g

    @staticmethod
    def path_graph(n: int, weighted: bool = False) -> Graph:
        """Generate path graph (linear chain)"""
        g = Graph(n, GraphType.UNDIRECTED, weighted)

        for i in range(n - 1):
            weight = random.uniform(1.0, 10.0) if weighted else 1.0
            g.add_edge(i, i + 1, weight)

        return g

    @staticmethod
    def barabasi_albert(n: int, m: int, weighted: bool = False) -> Graph:
        """
        Generate scale-free network using Barabási-Albert preferential attachment

        Args:
            n: Number of vertices
            m: Number of edges to attach from new node to existing nodes
        """
        if m < 1 or m >= n:
            raise ValueError("m must be between 1 and n-1")

        g = Graph(n, GraphType.UNDIRECTED, weighted)

        # Start with complete graph of m+1 nodes
        for i in range(m + 1):
            for j in range(i + 1, m + 1):
                weight = random.uniform(1.0, 10.0) if weighted else 1.0
                g.add_edge(i, j, weight)

        # Track degrees for preferential attachment
        degrees = [m] * (m + 1)

        # Add remaining nodes
        for new_node in range(m + 1, n):
            # Select m nodes to connect to based on preferential attachment
            total_degree = sum(degrees)
            targets = set()

            while len(targets) < m:
                # Random selection weighted by degree
                r = random.random() * total_degree
                cumsum = 0

                for i, deg in enumerate(degrees):
                    cumsum += deg
                    if cumsum >= r:
                        targets.add(i)
                        break

            # Add edges
            for target in targets:
                weight = random.uniform(1.0, 10.0) if weighted else 1.0
                g.add_edge(new_node, target, weight)
                degrees[target] += 1

            degrees.append(len(targets))

        return g

    @staticmethod
    def watts_strogatz(n: int, k: int, beta: float, weighted: bool = False) -> Graph:
        """
        Generate small-world network using Watts-Strogatz model

        Args:
            n: Number of vertices
            k: Each vertex is connected to k nearest neighbors (k must be even)
            beta: Rewiring probability (0 = regular graph, 1 = random graph)
        """
        if k >= n:
            raise ValueError("k must be less than n")
        if k % 2 != 0:
            raise ValueError("k must be even")

        g = Graph(n, GraphType.UNDIRECTED, weighted)

        # Create ring lattice
        for i in range(n):
            for j in range(1, k // 2 + 1):
                neighbor = (i + j) % n
                weight = random.uniform(1.0, 10.0) if weighted else 1.0
                g.add_edge(i, neighbor, weight)

        # Rewire edges
        edges = []
        for i in range(n):
            for j in g.get_neighbors(i):
                if i < j[0]:  # Avoid duplicates in undirected graph
                    edges.append((i, j[0]))

        for i, j in edges:
            if random.random() < beta:
                # Rewire: remove (i,j) and add (i, random)
                # First, we need to remove the edge (implementation simplified)
                new_target = random.randint(0, n - 1)
                while new_target == i or any(n[0] == new_target for n in g.get_neighbors(i)):
                    new_target = random.randint(0, n - 1)

                weight = random.uniform(1.0, 10.0) if weighted else 1.0
                g.add_edge(i, new_target, weight)

        return g

    @staticmethod
    def erdos_renyi(n: int, p: float, directed: bool = False,
                   weighted: bool = False) -> Graph:
        """
        Generate Erdős-Rényi random graph G(n, p)

        Args:
            n: Number of vertices
            p: Probability of edge between any two vertices
            directed: Whether graph is directed
            weighted: Whether to add random weights
        """
        graph_type = GraphType.DIRECTED if directed else GraphType.UNDIRECTED
        g = Graph(n, graph_type, weighted)

        for i in range(n):
            start = 0 if directed else i + 1
            for j in range(start, n):
                if i != j and random.random() < p:
                    weight = random.uniform(1.0, 10.0) if weighted else 1.0
                    g.add_edge(i, j, weight)

        return g

    @staticmethod
    def petersen_graph() -> Graph:
        """Generate the famous Petersen graph"""
        g = Graph(10, GraphType.UNDIRECTED, False)

        # Outer pentagon
        for i in range(5):
            g.add_edge(i, (i + 1) % 5)

        # Inner pentagram
        for i in range(5):
            g.add_edge(i + 5, (i + 2) % 5 + 5)

        # Connect outer to inner
        for i in range(5):
            g.add_edge(i, i + 5)

        return g

    @staticmethod
    def hypercube(dimension: int) -> Graph:
        """Generate hypercube graph of given dimension"""
        n = 2 ** dimension
        g = Graph(n, GraphType.UNDIRECTED, False)

        for i in range(n):
            for bit in range(dimension):
                # Flip bit to get neighbor
                neighbor = i ^ (1 << bit)
                if i < neighbor:  # Add each edge once
                    g.add_edge(i, neighbor)

        return g

    @staticmethod
    def planar_random(n: int, max_degree: int = 5) -> Graph:
        """
        Generate random planar graph (approximately)
        Uses degree-constrained random generation
        """
        g = Graph(n, GraphType.UNDIRECTED, False)
        degrees = [0] * n

        edges_added = 0
        max_edges = 3 * n - 6  # Planar graph edge limit

        attempts = 0
        max_attempts = n * n

        while edges_added < max_edges and attempts < max_attempts:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)

            if u != v and degrees[u] < max_degree and degrees[v] < max_degree:
                # Check if edge doesn't exist
                existing = any(neighbor[0] == v for neighbor in g.get_neighbors(u))

                if not existing:
                    g.add_edge(u, v)
                    degrees[u] += 1
                    degrees[v] += 1
                    edges_added += 1

            attempts += 1

        return g


def demo_extended_generators():
    """Demonstrate extended graph generators"""
    print("=" * 80)
    print("EXTENDED GRAPH GENERATORS DEMO")
    print("=" * 80)
    print()

    generators = [
        ("Bipartite Graph (3, 4)", ExtendedGraphGenerator.bipartite_graph(3, 4, 0.6)),
        ("Complete Bipartite K(3,3)", ExtendedGraphGenerator.complete_bipartite(3, 3)),
        ("Random Tree (10 vertices)", ExtendedGraphGenerator.tree(10)),
        ("Binary Tree (4 levels)", ExtendedGraphGenerator.binary_tree(4)),
        ("Star Graph (8 vertices)", ExtendedGraphGenerator.star_graph(8)),
        ("Wheel Graph (7 vertices)", ExtendedGraphGenerator.wheel_graph(7)),
        ("Grid Graph (4x4)", ExtendedGraphGenerator.grid_graph(4, 4)),
        ("Path Graph (10 vertices)", ExtendedGraphGenerator.path_graph(10)),
        ("Barabási-Albert (20, m=2)", ExtendedGraphGenerator.barabasi_albert(20, 2)),
        ("Watts-Strogatz (20, k=4, β=0.3)", ExtendedGraphGenerator.watts_strogatz(20, 4, 0.3)),
        ("Erdős-Rényi (15, p=0.3)", ExtendedGraphGenerator.erdos_renyi(15, 0.3)),
        ("Petersen Graph", ExtendedGraphGenerator.petersen_graph()),
        ("Hypercube (4D)", ExtendedGraphGenerator.hypercube(4)),
    ]

    for name, graph in generators:
        print(f"{name}:")
        print(f"  Vertices: {graph.num_vertices}")
        print(f"  Edges: {graph.num_edges}")
        print(f"  Density: {graph.num_edges / (graph.num_vertices * (graph.num_vertices - 1) / 2):.4f}")
        print(f"  Connected: {graph.is_connected()}")
        print(f"  Has Cycle: {graph.has_cycle()}")
        print()


if __name__ == "__main__":
    demo_extended_generators()
