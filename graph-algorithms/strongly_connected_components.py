"""
Strongly Connected Components Algorithms
========================================

Implementation of algorithms for finding strongly connected components (SCCs)
in directed graphs. A strongly connected component is a maximal set of vertices
where every vertex is reachable from every other vertex.

Algorithms Implemented:
- Tarjan's Algorithm (single-pass)
- Kosaraju's Algorithm (two-pass)
- Path-based Strong Component Algorithm
- Incremental SCC maintenance
- SCC-based graph condensation
- Topological ordering of SCCs

Applications:
- Compiler optimization (finding loops)
- Social network analysis
- Web crawling (finding website clusters)
- Circuit analysis
- Dependency resolution
- Model checking

Author: Claude
Date: January 2026
"""

import numpy as np
from typing import List, Set, Dict, Tuple, Optional, Any
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
import sys


class SCCAlgorithm(Enum):
    """Types of SCC algorithms."""
    TARJAN = "tarjan"
    KOSARAJU = "kosaraju"
    PATH_BASED = "path_based"


@dataclass
class SCC:
    """Represents a strongly connected component."""
    id: int
    vertices: Set[int]
    incoming_edges: Set[Tuple[int, int]] = field(default_factory=set)
    outgoing_edges: Set[Tuple[int, int]] = field(default_factory=set)


@dataclass
class TarjanState:
    """State for Tarjan's algorithm."""
    index: int = 0
    stack: List[int] = field(default_factory=list)
    indices: Dict[int, int] = field(default_factory=dict)
    lowlinks: Dict[int, int] = field(default_factory=dict)
    on_stack: Set[int] = field(default_factory=set)
    sccs: List[Set[int]] = field(default_factory=list)


class StronglyConnectedComponents:
    """
    Find strongly connected components in directed graphs.
    """

    def __init__(self, num_vertices: int, edges: List[Tuple[int, int]]):
        """
        Initialize directed graph.

        Args:
            num_vertices: Number of vertices
            edges: List of directed edges (u, v)
        """
        self.num_vertices = num_vertices
        self.edges = edges
        self.adjacency_list = self._build_adjacency_list()
        self.reverse_adjacency_list = self._build_reverse_adjacency_list()

    def _build_adjacency_list(self) -> Dict[int, Set[int]]:
        """Build adjacency list for directed graph."""
        adj_list = defaultdict(set)
        for u, v in self.edges:
            adj_list[u].add(v)
        # Ensure all vertices are present
        for i in range(self.num_vertices):
            if i not in adj_list:
                adj_list[i] = set()
        return adj_list

    def _build_reverse_adjacency_list(self) -> Dict[int, Set[int]]:
        """Build reverse adjacency list."""
        rev_adj_list = defaultdict(set)
        for u, v in self.edges:
            rev_adj_list[v].add(u)
        # Ensure all vertices are present
        for i in range(self.num_vertices):
            if i not in rev_adj_list:
                rev_adj_list[i] = set()
        return rev_adj_list

    def tarjan_scc(self) -> List[Set[int]]:
        """
        Find SCCs using Tarjan's algorithm.

        Single-pass algorithm with O(V + E) complexity.

        Returns:
            List of SCCs (sets of vertices)
        """
        state = TarjanState()

        for vertex in range(self.num_vertices):
            if vertex not in state.indices:
                self._tarjan_dfs(vertex, state)

        return state.sccs

    def _tarjan_dfs(self, v: int, state: TarjanState):
        """
        DFS for Tarjan's algorithm.

        Args:
            v: Current vertex
            state: Algorithm state
        """
        # Set the depth index for v to the smallest unused index
        state.indices[v] = state.index
        state.lowlinks[v] = state.index
        state.index += 1
        state.stack.append(v)
        state.on_stack.add(v)

        # Consider successors of v
        for w in self.adjacency_list[v]:
            if w not in state.indices:
                # Successor w has not yet been visited; recurse on it
                self._tarjan_dfs(w, state)
                state.lowlinks[v] = min(state.lowlinks[v], state.lowlinks[w])
            elif w in state.on_stack:
                # Successor w is in stack and hence in current SCC
                state.lowlinks[v] = min(state.lowlinks[v], state.indices[w])

        # If v is a root node, pop the stack and print an SCC
        if state.lowlinks[v] == state.indices[v]:
            # Start a new strongly connected component
            scc = set()
            while True:
                w = state.stack.pop()
                state.on_stack.remove(w)
                scc.add(w)
                if w == v:
                    break
            state.sccs.append(scc)

    def kosaraju_scc(self) -> List[Set[int]]:
        """
        Find SCCs using Kosaraju's algorithm.

        Two-pass algorithm with O(V + E) complexity.

        Returns:
            List of SCCs
        """
        # First pass: compute finish times
        visited = set()
        finish_stack = []

        def dfs1(v: int):
            """First DFS to compute finish times."""
            visited.add(v)
            for neighbor in self.adjacency_list[v]:
                if neighbor not in visited:
                    dfs1(neighbor)
            finish_stack.append(v)

        # Run first DFS
        for vertex in range(self.num_vertices):
            if vertex not in visited:
                dfs1(vertex)

        # Second pass: find SCCs in reverse graph
        visited.clear()
        sccs = []

        def dfs2(v: int, scc: Set[int]):
            """Second DFS on reverse graph."""
            visited.add(v)
            scc.add(v)
            for neighbor in self.reverse_adjacency_list[v]:
                if neighbor not in visited:
                    dfs2(neighbor, scc)

        # Process vertices in reverse finish time order
        while finish_stack:
            v = finish_stack.pop()
            if v not in visited:
                scc = set()
                dfs2(v, scc)
                sccs.append(scc)

        return sccs

    def path_based_scc(self) -> List[Set[int]]:
        """
        Find SCCs using path-based algorithm.

        Alternative to Tarjan's with simpler implementation.

        Returns:
            List of SCCs
        """
        sccs = []
        preorder = {}
        preorder_counter = [0]  # Use list to allow modification in nested function
        stack_s = []  # Main stack
        stack_p = []  # Path stack
        visited = set()

        def dfs(v: int):
            """DFS for path-based SCC."""
            preorder[v] = preorder_counter[0]
            preorder_counter[0] += 1
            visited.add(v)
            stack_s.append(v)
            stack_p.append(v)

            for w in self.adjacency_list[v]:
                if w not in visited:
                    dfs(w)
                elif w in preorder and w in stack_s:
                    # w is in current path
                    while stack_p and preorder[stack_p[-1]] > preorder[w]:
                        stack_p.pop()

            if stack_p and stack_p[-1] == v:
                # v is root of SCC
                scc = set()
                while True:
                    w = stack_s.pop()
                    scc.add(w)
                    if w in preorder:
                        del preorder[w]
                    if w == v:
                        break
                sccs.append(scc)
                stack_p.pop()

        # Run DFS from all unvisited vertices
        for vertex in range(self.num_vertices):
            if vertex not in visited:
                dfs(vertex)

        return sccs

    def condensation_graph(self) -> Tuple[List[SCC], List[Tuple[int, int]]]:
        """
        Create condensation graph where each SCC is a single node.

        Returns:
            List of SCC objects and edges between SCCs
        """
        # Find SCCs
        sccs = self.tarjan_scc()

        # Map vertices to SCC IDs
        vertex_to_scc = {}
        scc_objects = []

        for scc_id, vertices in enumerate(sccs):
            scc_obj = SCC(id=scc_id, vertices=vertices)
            scc_objects.append(scc_obj)
            for v in vertices:
                vertex_to_scc[v] = scc_id

        # Find edges between SCCs
        scc_edges = set()
        for u, v in self.edges:
            scc_u = vertex_to_scc[u]
            scc_v = vertex_to_scc[v]
            if scc_u != scc_v:
                scc_edges.add((scc_u, scc_v))
                scc_objects[scc_u].outgoing_edges.add((u, v))
                scc_objects[scc_v].incoming_edges.add((u, v))

        return scc_objects, list(scc_edges)

    def topological_order_of_sccs(self) -> List[int]:
        """
        Get topological ordering of SCCs.

        Returns:
            List of SCC IDs in topological order
        """
        scc_objects, scc_edges = self.condensation_graph()

        # Build adjacency list for condensation graph
        scc_adj = defaultdict(set)
        in_degree = defaultdict(int)

        for scc_u, scc_v in scc_edges:
            scc_adj[scc_u].add(scc_v)
            in_degree[scc_v] += 1

        # Kahn's algorithm for topological sort
        queue = deque()
        for scc_id in range(len(scc_objects)):
            if in_degree[scc_id] == 0:
                queue.append(scc_id)

        topo_order = []
        while queue:
            scc_id = queue.popleft()
            topo_order.append(scc_id)

            for neighbor in scc_adj[scc_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return topo_order

    def is_strongly_connected(self) -> bool:
        """
        Check if entire graph is strongly connected.

        Returns:
            True if graph is strongly connected
        """
        sccs = self.tarjan_scc()
        return len(sccs) == 1

    def find_scc_of_vertex(self, vertex: int) -> Set[int]:
        """
        Find the SCC containing a specific vertex.

        Args:
            vertex: Vertex to find SCC for

        Returns:
            Set of vertices in the same SCC
        """
        sccs = self.tarjan_scc()
        for scc in sccs:
            if vertex in scc:
                return scc
        return {vertex}


class IncrementalSCC:
    """
    Maintain SCCs incrementally as edges are added.

    Useful for dynamic graphs.
    """

    def __init__(self, num_vertices: int):
        """
        Initialize incremental SCC structure.

        Args:
            num_vertices: Number of vertices
        """
        self.num_vertices = num_vertices
        self.edges = []
        self.scc_id = list(range(num_vertices))  # Each vertex starts in its own SCC
        self.scc_members = {i: {i} for i in range(num_vertices)}

    def add_edge(self, u: int, v: int):
        """
        Add an edge and update SCCs.

        Args:
            u: Source vertex
            v: Target vertex
        """
        self.edges.append((u, v))

        # If already in same SCC, no change needed
        if self.scc_id[u] == self.scc_id[v]:
            return

        # Check if this edge creates a cycle (merges SCCs)
        if self._creates_path(v, u):
            # Merge SCCs
            self._merge_sccs(u, v)

    def _creates_path(self, start: int, end: int) -> bool:
        """
        Check if path exists from start to end.

        Args:
            start: Start vertex
            end: End vertex

        Returns:
            True if path exists
        """
        # Build adjacency list from current edges
        adj_list = defaultdict(set)
        for u, v in self.edges:
            adj_list[u].add(v)

        # BFS to find path
        visited = set()
        queue = deque([start])
        visited.add(start)

        while queue:
            current = queue.popleft()
            if current == end:
                return True

            for neighbor in adj_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return False

    def _merge_sccs(self, u: int, v: int):
        """
        Merge SCCs containing u and v.

        Args:
            u: First vertex
            v: Second vertex
        """
        scc_u = self.scc_id[u]
        scc_v = self.scc_id[v]

        # Find all vertices reachable from u's SCC to v's SCC and back
        to_merge = self._find_cycle_members(scc_u, scc_v)

        # Create new SCC ID
        new_scc_id = min(to_merge)

        # Update all vertices in the cycle
        new_members = set()
        for scc in to_merge:
            for vertex in self.scc_members[scc]:
                self.scc_id[vertex] = new_scc_id
                new_members.add(vertex)
            if scc != new_scc_id:
                del self.scc_members[scc]

        self.scc_members[new_scc_id] = new_members

    def _find_cycle_members(self, scc1: int, scc2: int) -> Set[int]:
        """Find all SCCs in cycle between scc1 and scc2."""
        # Simplified: just merge the two SCCs
        # Full implementation would find all SCCs in the cycle
        return {scc1, scc2}

    def get_sccs(self) -> List[Set[int]]:
        """
        Get current SCCs.

        Returns:
            List of SCCs
        """
        return list(self.scc_members.values())


def basic_examples():
    """Basic examples of strongly connected components."""
    print("=" * 60)
    print("STRONGLY CONNECTED COMPONENTS - BASIC EXAMPLES")
    print("=" * 60)

    # Example 1: Simple directed graph
    print("\n1. Simple Directed Graph:")
    print("   0 → 1 → 2")
    print("   ↑       ↓")
    print("   └───────┘")

    edges1 = [(0, 1), (1, 2), (2, 0)]
    scc1 = StronglyConnectedComponents(3, edges1)

    print(f"   Tarjan's SCCs: {scc1.tarjan_scc()}")
    print(f"   Kosaraju's SCCs: {scc1.kosaraju_scc()}")
    print(f"   Is strongly connected: {scc1.is_strongly_connected()}")

    # Example 2: Multiple SCCs
    print("\n2. Graph with Multiple SCCs:")
    print("   0 → 1    3 → 4")
    print("   ↑   ↓    ↑   ↓")
    print("   └← 2      └← 5")

    edges2 = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]
    scc2 = StronglyConnectedComponents(6, edges2)

    print(f"   SCCs: {scc2.tarjan_scc()}")

    # Example 3: DAG (each vertex is its own SCC)
    print("\n3. DAG (Directed Acyclic Graph):")
    print("   0 → 1 → 2")
    print("   ↓   ↓")
    print("   3 → 4")

    edges3 = [(0, 1), (0, 3), (1, 2), (1, 4), (3, 4)]
    scc3 = StronglyConnectedComponents(5, edges3)

    print(f"   SCCs: {scc3.tarjan_scc()}")
    print("   (Each vertex is its own SCC - no cycles)")


def compiler_optimization_example():
    """Example: Loop detection in control flow graphs."""
    print("\n" + "=" * 60)
    print("COMPILER OPTIMIZATION - LOOP DETECTION")
    print("=" * 60)

    # Control flow graph with loops
    print("\nControl Flow Graph:")
    print("   START(0) → INIT(1) → COND(2) ←─┐")
    print("                           ↓      │")
    print("                        BODY(3) ───┘")
    print("                           ↓")
    print("                        EXIT(4)")

    edges = [
        (0, 1),  # START -> INIT
        (1, 2),  # INIT -> COND
        (2, 3),  # COND -> BODY (loop entry)
        (3, 2),  # BODY -> COND (back edge)
        (2, 4),  # COND -> EXIT (loop exit)
    ]

    scc = StronglyConnectedComponents(5, edges)
    components = scc.tarjan_scc()

    print("\nDetected Loops (SCCs with >1 vertex):")
    for i, comp in enumerate(components):
        if len(comp) > 1:
            nodes = sorted(comp)
            print(f"  Loop {i}: Nodes {nodes}")
            print(f"    Loop header: Node {min(nodes)}")

    # Analyze loop nesting with condensation graph
    condensed, condensed_edges = scc.condensation_graph()

    print("\nCondensation Graph (for loop nesting analysis):")
    for scc_obj in condensed:
        if len(scc_obj.vertices) > 1:
            print(f"  Loop SCC {scc_obj.id}: {sorted(scc_obj.vertices)}")
        else:
            print(f"  Basic Block {scc_obj.id}: {sorted(scc_obj.vertices)}")


def dependency_resolution_example():
    """Example: Package dependency resolution."""
    print("\n" + "=" * 60)
    print("PACKAGE DEPENDENCY RESOLUTION")
    print("=" * 60)

    # Package dependencies (A depends on B means A → B)
    packages = ['app', 'lib1', 'lib2', 'lib3', 'utils', 'core', 'test']
    dependencies = [
        (0, 1),  # app depends on lib1
        (0, 2),  # app depends on lib2
        (1, 4),  # lib1 depends on utils
        (2, 3),  # lib2 depends on lib3
        (3, 2),  # lib3 depends on lib2 (circular!)
        (4, 5),  # utils depends on core
        (6, 0),  # test depends on app
    ]

    print("Package Dependencies:")
    for u, v in dependencies:
        print(f"  {packages[u]} → {packages[v]}")

    scc = StronglyConnectedComponents(len(packages), dependencies)
    components = scc.tarjan_scc()

    # Check for circular dependencies
    print("\nCircular Dependencies (SCCs with >1 package):")
    has_circular = False
    for comp in components:
        if len(comp) > 1:
            has_circular = True
            circular_packages = [packages[i] for i in sorted(comp)]
            print(f"  Circular: {' ↔ '.join(circular_packages)}")

    if not has_circular:
        print("  None found - dependencies form a DAG")

    # Build order (topological sort of SCCs)
    topo_order = scc.topological_order_of_sccs()
    print("\nBuild Order (respecting dependencies):")

    for scc_id in reversed(topo_order):  # Reverse for build order
        comp = components[scc_id]
        if len(comp) > 1:
            comp_packages = [packages[i] for i in sorted(comp)]
            print(f"  Build together: {', '.join(comp_packages)}")
        else:
            vertex = list(comp)[0]
            print(f"  Build: {packages[vertex]}")


def social_network_analysis_example():
    """Example: Finding communities in social networks."""
    print("\n" + "=" * 60)
    print("SOCIAL NETWORK ANALYSIS - INFLUENCE GROUPS")
    print("=" * 60)

    # Directed follower graph (A → B means A follows B)
    users = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace']
    follows = [
        (0, 1), (1, 2), (2, 0),  # Alice, Bob, Charlie follow each other
        (3, 4), (4, 3),          # David and Eve follow each other
        (1, 3),                  # Bob follows David (one-way)
        (5, 6), (6, 5),          # Frank and Grace follow each other
        (4, 5),                  # Eve follows Frank (one-way)
    ]

    print("Follower Network:")
    for u, v in follows:
        print(f"  {users[u]} follows {users[v]}")

    scc = StronglyConnectedComponents(len(users), follows)
    components = scc.tarjan_scc()

    print("\nMutual Influence Groups (SCCs):")
    for i, comp in enumerate(components):
        group_users = [users[j] for j in sorted(comp)]
        if len(comp) > 1:
            print(f"  Group {i}: {', '.join(group_users)} (mutual followers)")
        else:
            print(f"  Individual {i}: {group_users[0]} (no mutual connections)")

    # Analyze influence flow
    condensed, condensed_edges = scc.condensation_graph()
    print("\nInfluence Flow Between Groups:")
    for scc_u, scc_v in condensed_edges:
        group_u = [users[j] for j in sorted(condensed[scc_u].vertices)]
        group_v = [users[j] for j in sorted(condensed[scc_v].vertices)]
        print(f"  {group_u} → {group_v}")


def web_crawling_example():
    """Example: Web page connectivity analysis."""
    print("\n" + "=" * 60)
    print("WEB CRAWLING - SITE STRUCTURE ANALYSIS")
    print("=" * 60)

    # Web pages and their links
    pages = ['home', 'about', 'products', 'p1', 'p2', 'blog', 'post1', 'post2', 'contact']
    links = [
        (0, 1), (0, 2), (0, 5), (0, 8),  # home links to main sections
        (1, 0),                           # about links back to home
        (2, 3), (2, 4),                   # products links to p1, p2
        (3, 2), (4, 2),                   # products link back
        (3, 4), (4, 3),                   # cross-links between products
        (5, 6), (5, 7),                   # blog links to posts
        (6, 5), (7, 5),                   # posts link back to blog
        (6, 7), (7, 6),                   # cross-links between posts
        (8, 0),                           # contact links to home
    ]

    print("Site Structure:")
    for u, v in links:
        print(f"  {pages[u]} → {pages[v]}")

    scc = StronglyConnectedComponents(len(pages), links)
    components = scc.tarjan_scc()

    print("\nStrongly Connected Page Groups:")
    for i, comp in enumerate(components):
        group_pages = [pages[j] for j in sorted(comp)]
        print(f"  Group {i}: {', '.join(group_pages)}")

    # Identify navigation structure
    print("\nNavigation Analysis:")
    for comp in components:
        if 0 in comp:  # Contains home page
            reachable = [pages[j] for j in sorted(comp)]
            print(f"  Core navigation loop: {', '.join(reachable)}")

    # Find isolated sections
    condensed, condensed_edges = scc.condensation_graph()
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)

    for u, v in condensed_edges:
        out_degree[u] += 1
        in_degree[v] += 1

    print("\nSite Sections:")
    for scc_obj in condensed:
        section_pages = [pages[i] for i in sorted(scc_obj.vertices)]
        if in_degree[scc_obj.id] == 0:
            print(f"  Entry section: {', '.join(section_pages)}")
        elif out_degree[scc_obj.id] == 0:
            print(f"  Dead-end section: {', '.join(section_pages)}")


def incremental_scc_example():
    """Example: Incremental SCC maintenance."""
    print("\n" + "=" * 60)
    print("INCREMENTAL SCC MAINTENANCE")
    print("=" * 60)

    print("Building graph incrementally:")

    inc_scc = IncrementalSCC(5)

    # Add edges one by one
    edges_to_add = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 2)]

    for u, v in edges_to_add:
        print(f"\nAdding edge {u} → {v}")
        inc_scc.add_edge(u, v)

        current_sccs = inc_scc.get_sccs()
        print(f"  Current SCCs: {[sorted(scc) for scc in current_sccs]}")

        # Check if this created a cycle
        if len(current_sccs) < 5:
            print(f"  → Merged SCCs due to cycle")


def performance_comparison():
    """Compare performance of different SCC algorithms."""
    print("\n" + "=" * 60)
    print("ALGORITHM PERFORMANCE COMPARISON")
    print("=" * 60)

    import time
    import random

    # Generate random directed graph
    n = 100
    edge_prob = 0.05
    edges = []

    for i in range(n):
        for j in range(n):
            if i != j and random.random() < edge_prob:
                edges.append((i, j))

    print(f"Test Graph: {n} vertices, {len(edges)} edges")

    scc = StronglyConnectedComponents(n, edges)

    # Test Tarjan's algorithm
    start = time.time()
    tarjan_result = scc.tarjan_scc()
    tarjan_time = time.time() - start

    # Test Kosaraju's algorithm
    start = time.time()
    kosaraju_result = scc.kosaraju_scc()
    kosaraju_time = time.time() - start

    # Test Path-based algorithm
    start = time.time()
    path_based_result = scc.path_based_scc()
    path_based_time = time.time() - start

    print(f"\nResults:")
    print(f"  Tarjan's:    {len(tarjan_result)} SCCs in {tarjan_time*1000:.2f}ms")
    print(f"  Kosaraju's:  {len(kosaraju_result)} SCCs in {kosaraju_time*1000:.2f}ms")
    print(f"  Path-based:  {len(path_based_result)} SCCs in {path_based_time*1000:.2f}ms")

    # Analyze SCC sizes
    scc_sizes = sorted([len(scc) for scc in tarjan_result], reverse=True)
    print(f"\nSCC Size Distribution:")
    print(f"  Largest SCC: {scc_sizes[0]} vertices")
    print(f"  Singleton SCCs: {sum(1 for s in scc_sizes if s == 1)}")
    print(f"  Non-trivial SCCs: {sum(1 for s in scc_sizes if s > 1)}")


if __name__ == "__main__":
    # Run examples
    basic_examples()
    compiler_optimization_example()
    dependency_resolution_example()
    social_network_analysis_example()
    web_crawling_example()
    incremental_scc_example()
    performance_comparison()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- SCCs identify cyclic dependencies in directed graphs")
    print("- Tarjan's algorithm finds SCCs in a single DFS pass")
    print("- Kosaraju's uses two DFS passes but is conceptually simpler")
    print("- Condensation graph reduces cyclic graph to DAG")
    print("- Critical for dependency analysis and loop detection")
    print("=" * 60)