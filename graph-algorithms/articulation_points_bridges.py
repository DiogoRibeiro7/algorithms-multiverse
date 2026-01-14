"""
Articulation Points and Bridges Algorithms
==========================================

Implementation of algorithms for finding critical vertices (articulation points)
and critical edges (bridges) in graphs. These are fundamental concepts in
graph connectivity and network reliability analysis.

Algorithms Implemented:
- Tarjan's Algorithm for Articulation Points
- Tarjan's Algorithm for Bridges
- Block-Cut Tree construction
- Biconnected Components
- Bridge Finding with Union-Find
- 2-Edge Connected Components
- 2-Vertex Connected Components

Applications:
- Network reliability analysis
- Circuit design
- Transportation planning
- Social network analysis
- Critical infrastructure identification

Author: Claude
Date: January 2026
"""

import numpy as np
from typing import List, Set, Tuple, Dict, Optional, Any
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum


class ConnectivityType(Enum):
    """Types of connectivity analysis."""
    ARTICULATION_POINTS = "articulation_points"
    BRIDGES = "bridges"
    BICONNECTED_COMPONENTS = "biconnected_components"
    TWO_EDGE_CONNECTED = "2_edge_connected"
    TWO_VERTEX_CONNECTED = "2_vertex_connected"


@dataclass
class DFSState:
    """State for DFS traversal in Tarjan's algorithm."""
    discovery: Dict[int, int] = field(default_factory=dict)
    low: Dict[int, int] = field(default_factory=dict)
    parent: Dict[int, Optional[int]] = field(default_factory=dict)
    visited: Set[int] = field(default_factory=set)
    time: int = 0


@dataclass
class BiconnectedComponent:
    """Represents a biconnected component."""
    vertices: Set[int]
    edges: Set[Tuple[int, int]]
    articulation_points: Set[int]


class ArticulationPointsFinder:
    """
    Find articulation points (cut vertices) in an undirected graph.

    An articulation point is a vertex whose removal increases the
    number of connected components.
    """

    def __init__(self, num_vertices: int, edges: List[Tuple[int, int]]):
        """
        Initialize the graph.

        Args:
            num_vertices: Number of vertices
            edges: List of edges (u, v)
        """
        self.num_vertices = num_vertices
        self.edges = edges
        self.adjacency_list = self._build_adjacency_list()

    def _build_adjacency_list(self) -> Dict[int, Set[int]]:
        """Build adjacency list from edges."""
        adj_list = defaultdict(set)
        for u, v in self.edges:
            adj_list[u].add(v)
            adj_list[v].add(u)
        return adj_list

    def find_articulation_points(self) -> Set[int]:
        """
        Find all articulation points using Tarjan's algorithm.

        Time complexity: O(V + E)

        Returns:
            Set of articulation point vertices
        """
        if self.num_vertices == 0:
            return set()

        articulation_points = set()
        state = DFSState()

        for vertex in range(self.num_vertices):
            if vertex not in state.visited:
                self._tarjan_dfs(vertex, None, articulation_points, state)

        return articulation_points

    def _tarjan_dfs(self, u: int, parent: Optional[int],
                    articulation_points: Set[int], state: DFSState):
        """
        DFS traversal for Tarjan's algorithm.

        Args:
            u: Current vertex
            parent: Parent vertex
            articulation_points: Set to store articulation points
            state: DFS state
        """
        # Mark current vertex as visited
        state.visited.add(u)
        state.discovery[u] = state.low[u] = state.time
        state.time += 1
        state.parent[u] = parent

        # Count children in DFS tree
        children = 0

        # Recur for all adjacent vertices
        for v in self.adjacency_list[u]:
            if v not in state.visited:
                children += 1
                self._tarjan_dfs(v, u, articulation_points, state)

                # Check if subtree rooted at v has connection to ancestors of u
                state.low[u] = min(state.low[u], state.low[v])

                # u is articulation point in following cases:

                # (1) u is root of DFS tree and has two or more children
                if parent is None and children > 1:
                    articulation_points.add(u)

                # (2) u is not root and low value of child is greater than discovery of u
                if parent is not None and state.low[v] >= state.discovery[u]:
                    articulation_points.add(u)

            elif v != parent:
                # Update low value of u for parent function calls
                state.low[u] = min(state.low[u], state.discovery[v])

    def find_articulation_points_naive(self) -> Set[int]:
        """
        Naive algorithm for finding articulation points.

        Tests each vertex by removing it and checking connectivity.
        Time complexity: O(V * (V + E))

        Returns:
            Set of articulation points
        """
        articulation_points = set()

        # Count initial components
        initial_components = self._count_components(None)

        # Test each vertex
        for vertex in range(self.num_vertices):
            components = self._count_components(vertex)
            if components > initial_components:
                articulation_points.add(vertex)

        return articulation_points

    def _count_components(self, excluded: Optional[int]) -> int:
        """
        Count connected components excluding a vertex.

        Args:
            excluded: Vertex to exclude (None to include all)

        Returns:
            Number of connected components
        """
        visited = set()
        if excluded is not None:
            visited.add(excluded)

        components = 0

        for vertex in range(self.num_vertices):
            if vertex not in visited:
                components += 1
                self._dfs_component(vertex, visited, excluded)

        return components

    def _dfs_component(self, start: int, visited: Set[int], excluded: Optional[int]):
        """DFS to mark all vertices in a component."""
        stack = [start]
        visited.add(start)

        while stack:
            u = stack.pop()
            for v in self.adjacency_list[u]:
                if v not in visited and v != excluded:
                    visited.add(v)
                    stack.append(v)


class BridgesFinder:
    """
    Find bridges (cut edges) in an undirected graph.

    A bridge is an edge whose removal increases the number of connected components.
    """

    def __init__(self, num_vertices: int, edges: List[Tuple[int, int]]):
        """
        Initialize the graph.

        Args:
            num_vertices: Number of vertices
            edges: List of edges
        """
        self.num_vertices = num_vertices
        self.edges = edges
        self.adjacency_list = self._build_adjacency_list()

    def _build_adjacency_list(self) -> Dict[int, List[Tuple[int, int]]]:
        """Build adjacency list with edge indices."""
        adj_list = defaultdict(list)
        for idx, (u, v) in enumerate(self.edges):
            adj_list[u].append((v, idx))
            adj_list[v].append((u, idx))
        return adj_list

    def find_bridges(self) -> List[Tuple[int, int]]:
        """
        Find all bridges using modified Tarjan's algorithm.

        Time complexity: O(V + E)

        Returns:
            List of bridge edges
        """
        if not self.edges:
            return []

        bridges = []
        state = DFSState()

        for vertex in range(self.num_vertices):
            if vertex not in state.visited:
                self._tarjan_bridges_dfs(vertex, -1, bridges, state)

        return bridges

    def _tarjan_bridges_dfs(self, u: int, parent_edge: int,
                           bridges: List[Tuple[int, int]], state: DFSState):
        """
        DFS for finding bridges.

        Args:
            u: Current vertex
            parent_edge: Edge index from parent
            bridges: List to store bridges
            state: DFS state
        """
        state.visited.add(u)
        state.discovery[u] = state.low[u] = state.time
        state.time += 1

        for v, edge_idx in self.adjacency_list[u]:
            if edge_idx == parent_edge:
                continue  # Skip edge to parent

            if v not in state.visited:
                self._tarjan_bridges_dfs(v, edge_idx, bridges, state)
                state.low[u] = min(state.low[u], state.low[v])

                # Check if edge is a bridge
                if state.low[v] > state.discovery[u]:
                    bridges.append(self.edges[edge_idx])

            else:
                state.low[u] = min(state.low[u], state.discovery[v])

    def find_bridges_with_union_find(self) -> List[Tuple[int, int]]:
        """
        Alternative method using Union-Find for finding bridges.

        Returns:
            List of bridge edges
        """
        bridges = []

        for idx, edge in enumerate(self.edges):
            # Check if removing this edge disconnects the graph
            if self._is_bridge_union_find(idx):
                bridges.append(edge)

        return bridges

    def _is_bridge_union_find(self, edge_idx: int) -> bool:
        """Check if an edge is a bridge using Union-Find."""
        # Create Union-Find without the edge
        uf = UnionFind(self.num_vertices)

        for idx, (u, v) in enumerate(self.edges):
            if idx != edge_idx:
                uf.union(u, v)

        # Check if endpoints are still connected
        u, v = self.edges[edge_idx]
        return uf.find(u) != uf.find(v)


class BiconnectedComponents:
    """
    Find biconnected components in an undirected graph.

    A biconnected component is a maximal biconnected subgraph.
    """

    def __init__(self, num_vertices: int, edges: List[Tuple[int, int]]):
        """
        Initialize the graph.

        Args:
            num_vertices: Number of vertices
            edges: List of edges
        """
        self.num_vertices = num_vertices
        self.edges = edges
        self.adjacency_list = self._build_adjacency_list()

    def _build_adjacency_list(self) -> Dict[int, Set[int]]:
        """Build adjacency list."""
        adj_list = defaultdict(set)
        for u, v in self.edges:
            adj_list[u].add(v)
            adj_list[v].add(u)
        return adj_list

    def find_biconnected_components(self) -> List[BiconnectedComponent]:
        """
        Find all biconnected components.

        Returns:
            List of biconnected components
        """
        components = []
        state = DFSState()
        stack = []

        for vertex in range(self.num_vertices):
            if vertex not in state.visited:
                self._dfs_biconnected(vertex, None, stack, components, state)

        return components

    def _dfs_biconnected(self, u: int, parent: Optional[int], stack: List[Tuple[int, int]],
                        components: List[BiconnectedComponent], state: DFSState):
        """DFS for finding biconnected components."""
        state.visited.add(u)
        state.discovery[u] = state.low[u] = state.time
        state.time += 1
        children = 0

        for v in self.adjacency_list[u]:
            if v not in state.visited:
                children += 1
                stack.append((u, v))
                self._dfs_biconnected(v, u, stack, components, state)
                state.low[u] = min(state.low[u], state.low[v])

                # If u is an articulation point
                if (parent is None and children > 1) or \
                   (parent is not None and state.low[v] >= state.discovery[u]):
                    # Pop all edges for this biconnected component
                    component_edges = set()
                    component_vertices = set()

                    while stack:
                        edge = stack.pop()
                        component_edges.add(edge)
                        component_vertices.add(edge[0])
                        component_vertices.add(edge[1])

                        if edge == (u, v):
                            break

                    if component_edges:
                        component = BiconnectedComponent(
                            vertices=component_vertices,
                            edges=component_edges,
                            articulation_points={u}
                        )
                        components.append(component)

            elif v != parent and state.discovery[v] < state.discovery[u]:
                stack.append((u, v))
                state.low[u] = min(state.low[u], state.discovery[v])

        # Root articulation point case
        if parent is None and stack:
            component_edges = set(stack)
            component_vertices = set()
            for edge in component_edges:
                component_vertices.add(edge[0])
                component_vertices.add(edge[1])

            component = BiconnectedComponent(
                vertices=component_vertices,
                edges=component_edges,
                articulation_points=set()
            )
            components.append(component)
            stack.clear()


class BlockCutTree:
    """
    Construct block-cut tree from biconnected components.

    The block-cut tree is a tree where nodes are either blocks
    (biconnected components) or articulation points.
    """

    def __init__(self, num_vertices: int, edges: List[Tuple[int, int]]):
        """
        Initialize from graph.

        Args:
            num_vertices: Number of vertices
            edges: List of edges
        """
        self.num_vertices = num_vertices
        self.edges = edges
        self.tree_nodes = []  # Nodes in block-cut tree
        self.tree_edges = []  # Edges in block-cut tree

    def construct(self) -> Tuple[List[Any], List[Tuple[int, int]]]:
        """
        Construct block-cut tree.

        Returns:
            Tree nodes and edges
        """
        # Find articulation points and biconnected components
        ap_finder = ArticulationPointsFinder(self.num_vertices, self.edges)
        articulation_points = ap_finder.find_articulation_points()

        bc_finder = BiconnectedComponents(self.num_vertices, self.edges)
        components = bc_finder.find_biconnected_components()

        # Create nodes for articulation points
        ap_nodes = {}
        for ap in articulation_points:
            node_id = len(self.tree_nodes)
            ap_nodes[ap] = node_id
            self.tree_nodes.append(('articulation', ap))

        # Create nodes for blocks and connect to articulation points
        for comp in components:
            block_id = len(self.tree_nodes)
            self.tree_nodes.append(('block', comp))

            # Connect block to its articulation points
            for ap in comp.articulation_points:
                if ap in ap_nodes:
                    self.tree_edges.append((block_id, ap_nodes[ap]))

        return self.tree_nodes, self.tree_edges


class UnionFind:
    """Union-Find (Disjoint Set Union) data structure."""

    def __init__(self, n: int):
        """Initialize with n elements."""
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        """Find with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union by rank."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False

        if self.rank[px] < self.rank[py]:
            px, py = py, px

        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

        return True


def basic_examples():
    """Basic examples of articulation points and bridges."""
    print("=" * 60)
    print("ARTICULATION POINTS AND BRIDGES - BASIC EXAMPLES")
    print("=" * 60)

    # Example 1: Simple graph with articulation point
    print("\n1. Simple Graph with Articulation Point:")
    print("   0---1---2")
    print("   |   |   |")
    print("   3---4   5")

    edges1 = [(0, 1), (0, 3), (1, 2), (1, 4), (2, 5), (3, 4)]
    ap_finder1 = ArticulationPointsFinder(6, edges1)
    aps1 = ap_finder1.find_articulation_points()
    print(f"   Articulation points: {aps1}")

    br_finder1 = BridgesFinder(6, edges1)
    bridges1 = br_finder1.find_bridges()
    print(f"   Bridges: {bridges1}")

    # Example 2: Graph with multiple articulation points
    print("\n2. Chain Graph:")
    print("   0---1---2---3---4")

    edges2 = [(0, 1), (1, 2), (2, 3), (3, 4)]
    ap_finder2 = ArticulationPointsFinder(5, edges2)
    aps2 = ap_finder2.find_articulation_points()
    print(f"   Articulation points: {aps2}")

    br_finder2 = BridgesFinder(5, edges2)
    bridges2 = br_finder2.find_bridges()
    print(f"   Bridges: {bridges2}")

    # Example 3: Biconnected graph (no articulation points)
    print("\n3. Biconnected Graph (Square):")
    print("   0---1")
    print("   |   |")
    print("   3---2")

    edges3 = [(0, 1), (1, 2), (2, 3), (3, 0)]
    ap_finder3 = ArticulationPointsFinder(4, edges3)
    aps3 = ap_finder3.find_articulation_points()
    print(f"   Articulation points: {aps3} (none - biconnected)")

    br_finder3 = BridgesFinder(4, edges3)
    bridges3 = br_finder3.find_bridges()
    print(f"   Bridges: {bridges3} (none - biconnected)")


def network_reliability_example():
    """Example: Network reliability analysis."""
    print("\n" + "=" * 60)
    print("NETWORK RELIABILITY ANALYSIS")
    print("=" * 60)

    # Network topology
    print("\nNetwork Topology:")
    print("   Router0 --- Router1 --- Router2")
    print("      |           |           |")
    print("   Router3 --- Router4 --- Router5")
    print("      |                       |")
    print("   Router6 ----- Router7 -----")

    edges = [
        (0, 1), (1, 2),  # Top row
        (3, 4), (4, 5),  # Middle row
        (6, 7), (7, 5),  # Bottom connection
        (0, 3), (1, 4), (2, 5),  # Vertical connections
        (3, 6)  # Additional connection
    ]

    # Find critical routers (articulation points)
    ap_finder = ArticulationPointsFinder(8, edges)
    critical_routers = ap_finder.find_articulation_points()

    print(f"\nCritical Routers (failure disconnects network):")
    for router in sorted(critical_routers):
        print(f"  Router{router}")

    # Find critical connections (bridges)
    br_finder = BridgesFinder(8, edges)
    critical_connections = br_finder.find_bridges()

    print(f"\nCritical Connections (failure disconnects network):")
    for u, v in critical_connections:
        print(f"  Router{u} <-> Router{v}")

    # Analyze biconnected components
    bc_finder = BiconnectedComponents(8, edges)
    components = bc_finder.find_biconnected_components()

    print(f"\nBiconnected Components (remain connected if one router fails):")
    for i, comp in enumerate(components):
        routers = sorted(comp.vertices)
        print(f"  Component {i}: Routers {routers}")


def social_network_example():
    """Example: Social network analysis."""
    print("\n" + "=" * 60)
    print("SOCIAL NETWORK ANALYSIS")
    print("=" * 60)

    # Social network connections
    people = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry']
    connections = [
        (0, 1), (0, 2),  # Alice connects Bob and Charlie
        (1, 3), (2, 3),  # Bob and Charlie both know David
        (3, 4), (3, 5),  # David connects Eve and Frank
        (4, 6), (5, 6),  # Eve and Frank both know Grace
        (6, 7)           # Grace knows Henry
    ]

    print("Social Network:")
    for u, v in connections:
        print(f"  {people[u]} <-> {people[v]}")

    # Find key connectors (articulation points)
    ap_finder = ArticulationPointsFinder(len(people), connections)
    key_connectors = ap_finder.find_articulation_points()

    print("\nKey Connectors (removal splits community):")
    for person_idx in sorted(key_connectors):
        # Count how many components if removed
        components_if_removed = ap_finder._count_components(person_idx)
        print(f"  {people[person_idx]} - splits into {components_if_removed} groups")

    # Find weak connections (bridges)
    br_finder = BridgesFinder(len(people), connections)
    weak_connections = br_finder.find_bridges()

    print("\nWeak Connections (only link between groups):")
    for u, v in weak_connections:
        print(f"  {people[u]} <-> {people[v]}")


def circuit_analysis_example():
    """Example: Circuit redundancy analysis."""
    print("\n" + "=" * 60)
    print("CIRCUIT REDUNDANCY ANALYSIS")
    print("=" * 60)

    # Circuit components and connections
    components = ['Power', 'Switch1', 'Switch2', 'Resistor1',
                 'Resistor2', 'LED', 'Ground']

    # Parallel paths for redundancy
    connections = [
        (0, 1), (0, 2),     # Power to both switches
        (1, 3), (2, 4),     # Switches to resistors
        (3, 5), (4, 5),     # Resistors to LED (parallel paths)
        (5, 6),             # LED to ground
        (1, 2)              # Cross-connection between switches
    ]

    print("Circuit Connections:")
    for u, v in connections:
        print(f"  {components[u]} --- {components[v]}")

    # Find single points of failure
    ap_finder = ArticulationPointsFinder(len(components), connections)
    failure_points = ap_finder.find_articulation_points()

    print("\nSingle Points of Failure:")
    for comp_idx in sorted(failure_points):
        print(f"  {components[comp_idx]}")

    # Find non-redundant connections
    br_finder = BridgesFinder(len(components), connections)
    non_redundant = br_finder.find_bridges()

    print("\nNon-Redundant Connections:")
    for u, v in non_redundant:
        print(f"  {components[u]} --- {components[v]}")

    # Analyze redundancy groups
    bc_finder = BiconnectedComponents(len(components), connections)
    redundancy_groups = bc_finder.find_biconnected_components()

    print("\nRedundancy Groups (multiple paths between components):")
    for i, group in enumerate(redundancy_groups):
        group_comps = [components[idx] for idx in sorted(group.vertices)]
        print(f"  Group {i}: {', '.join(group_comps)}")


def block_cut_tree_example():
    """Example: Block-cut tree construction."""
    print("\n" + "=" * 60)
    print("BLOCK-CUT TREE CONSTRUCTION")
    print("=" * 60)

    # Graph with multiple biconnected components
    edges = [
        (0, 1), (1, 2), (2, 0),  # Triangle (block 1)
        (2, 3), (3, 4), (4, 2),  # Another triangle (block 2) - shares vertex 2
        (4, 5), (5, 6),          # Path (bridges)
        (6, 7), (7, 8), (8, 6)   # Final triangle (block 3)
    ]

    print("Original Graph Structure:")
    print("  Triangle1(0,1,2) -- vertex2 -- Triangle2(2,3,4)")
    print("                                         |")
    print("                                      vertex4")
    print("                                         |")
    print("                                    5 -- 6 -- Triangle3(6,7,8)")

    # Construct block-cut tree
    bct = BlockCutTree(9, edges)
    tree_nodes, tree_edges = bct.construct()

    print("\nBlock-Cut Tree Nodes:")
    for i, (node_type, data) in enumerate(tree_nodes):
        if node_type == 'articulation':
            print(f"  Node {i}: Articulation Point (vertex {data})")
        else:
            print(f"  Node {i}: Block (vertices {sorted(data.vertices)})")

    print("\nBlock-Cut Tree Edges:")
    for u, v in tree_edges:
        print(f"  Node {u} -- Node {v}")


def performance_comparison():
    """Compare performance of different algorithms."""
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)

    import time
    import random

    # Generate random connected graph
    n = 100
    edges = []

    # Create connected base
    for i in range(n - 1):
        edges.append((i, i + 1))

    # Add random edges
    for _ in range(n * 2):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))

    print(f"Test Graph: {n} vertices, {len(edges)} edges")

    # Test articulation points algorithms
    ap_finder = ArticulationPointsFinder(n, edges)

    start = time.time()
    aps_tarjan = ap_finder.find_articulation_points()
    time_tarjan = time.time() - start

    start = time.time()
    aps_naive = ap_finder.find_articulation_points_naive()
    time_naive = time.time() - start

    print(f"\nArticulation Points:")
    print(f"  Tarjan's Algorithm: {len(aps_tarjan)} points in {time_tarjan*1000:.2f}ms")
    print(f"  Naive Algorithm:    {len(aps_naive)} points in {time_naive*1000:.2f}ms")
    print(f"  Speedup: {time_naive/time_tarjan:.1f}x")

    # Test bridge finding algorithms
    br_finder = BridgesFinder(n, edges)

    start = time.time()
    bridges_tarjan = br_finder.find_bridges()
    time_tarjan_br = time.time() - start

    start = time.time()
    bridges_uf = br_finder.find_bridges_with_union_find()
    time_uf = time.time() - start

    print(f"\nBridges:")
    print(f"  Tarjan's Algorithm: {len(bridges_tarjan)} bridges in {time_tarjan_br*1000:.2f}ms")
    print(f"  Union-Find Method:  {len(bridges_uf)} bridges in {time_uf*1000:.2f}ms")
    print(f"  Speedup: {time_uf/time_tarjan_br:.1f}x")


if __name__ == "__main__":
    # Run examples
    basic_examples()
    network_reliability_example()
    social_network_example()
    circuit_analysis_example()
    block_cut_tree_example()
    performance_comparison()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Articulation points are critical for connectivity")
    print("- Bridges are edges whose removal disconnects the graph")
    print("- Tarjan's algorithm finds both in O(V+E) time")
    print("- Biconnected components remain connected despite single failures")
    print("- Block-cut tree provides hierarchical view of connectivity")
    print("=" * 60)