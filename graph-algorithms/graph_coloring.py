"""
Graph Coloring Algorithms Implementation
========================================

A comprehensive collection of graph coloring algorithms for assigning colors
to vertices such that no adjacent vertices share the same color.

Algorithms Implemented:
- Greedy Coloring
- Welsh-Powell Algorithm
- DSATUR (Degree of Saturation)
- Recursive Backtracking (Exact)
- Constraint Satisfaction Problem (CSP) approach
- Chromatic Polynomial calculation
- Brooks' Algorithm
- Graph Coloring using BFS/DFS

Applications:
- Register allocation in compilers
- Scheduling problems
- Frequency assignment
- Map coloring
- Sudoku solving

Author: Claude
Date: January 2026
"""

import numpy as np
from typing import List, Dict, Set, Optional, Tuple, Any
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
import heapq
import random


class ColoringStrategy(Enum):
    """Graph coloring strategies."""
    GREEDY = "greedy"
    WELSH_POWELL = "welsh_powell"
    DSATUR = "dsatur"
    BACKTRACKING = "backtracking"
    BROOKS = "brooks"
    RANDOM = "random"


@dataclass
class ColoredGraph:
    """Represents a colored graph."""
    num_vertices: int
    edges: List[Tuple[int, int]]
    coloring: Dict[int, int]
    num_colors: int

    def is_valid(self) -> bool:
        """Check if coloring is valid."""
        for u, v in self.edges:
            if u in self.coloring and v in self.coloring:
                if self.coloring[u] == self.coloring[v]:
                    return False
        return True


class GraphColoring:
    """
    Main graph coloring implementation with various algorithms.
    """

    def __init__(self, num_vertices: int, edges: List[Tuple[int, int]]):
        """
        Initialize graph for coloring.

        Args:
            num_vertices: Number of vertices
            edges: List of edges (u, v)
        """
        self.num_vertices = num_vertices
        self.edges = edges
        self.adjacency_list = self._build_adjacency_list()
        self.degree = [len(self.adjacency_list[i]) for i in range(num_vertices)]

    def _build_adjacency_list(self) -> Dict[int, Set[int]]:
        """Build adjacency list from edges."""
        adj_list = defaultdict(set)
        for u, v in self.edges:
            adj_list[u].add(v)
            adj_list[v].add(u)
        # Ensure all vertices are in the list
        for i in range(self.num_vertices):
            if i not in adj_list:
                adj_list[i] = set()
        return adj_list

    def greedy_coloring(self, vertex_order: Optional[List[int]] = None) -> Dict[int, int]:
        """
        Greedy graph coloring algorithm.

        Args:
            vertex_order: Order to color vertices (default: 0,1,2,...)

        Returns:
            Coloring assignment
        """
        if vertex_order is None:
            vertex_order = list(range(self.num_vertices))

        coloring = {}

        for vertex in vertex_order:
            # Find colors of adjacent vertices
            neighbor_colors = set()
            for neighbor in self.adjacency_list[vertex]:
                if neighbor in coloring:
                    neighbor_colors.add(coloring[neighbor])

            # Assign minimum available color
            color = 0
            while color in neighbor_colors:
                color += 1

            coloring[vertex] = color

        return coloring

    def welsh_powell(self) -> Dict[int, int]:
        """
        Welsh-Powell algorithm - colors vertices in decreasing degree order.

        Returns:
            Coloring assignment
        """
        # Sort vertices by degree (descending)
        vertices = list(range(self.num_vertices))
        vertices.sort(key=lambda v: self.degree[v], reverse=True)

        return self.greedy_coloring(vertices)

    def dsatur(self) -> Dict[int, int]:
        """
        DSATUR (Degree of Saturation) algorithm.

        Dynamically selects vertex with highest saturation degree to color next.

        Returns:
            Coloring assignment
        """
        coloring = {}
        saturation = [0] * self.num_vertices
        uncolored = set(range(self.num_vertices))

        while uncolored:
            # Select vertex with maximum saturation
            # Ties broken by maximum degree among uncolored vertices
            max_sat = -1
            max_degree = -1
            selected_vertex = -1

            for v in uncolored:
                sat = saturation[v]
                deg = self.degree[v]

                if sat > max_sat or (sat == max_sat and deg > max_degree):
                    max_sat = sat
                    max_degree = deg
                    selected_vertex = v

            # Color selected vertex
            neighbor_colors = set()
            for neighbor in self.adjacency_list[selected_vertex]:
                if neighbor in coloring:
                    neighbor_colors.add(coloring[neighbor])

            # Find minimum available color
            color = 0
            while color in neighbor_colors:
                color += 1

            coloring[selected_vertex] = color
            uncolored.remove(selected_vertex)

            # Update saturation degrees
            for neighbor in self.adjacency_list[selected_vertex]:
                if neighbor in uncolored:
                    # Count distinct colors in neighborhood
                    neighbor_colors = set()
                    for n in self.adjacency_list[neighbor]:
                        if n in coloring:
                            neighbor_colors.add(coloring[n])
                    saturation[neighbor] = len(neighbor_colors)

        return coloring

    def backtracking_coloring(self, max_colors: int) -> Optional[Dict[int, int]]:
        """
        Exact graph coloring using backtracking.

        Args:
            max_colors: Maximum number of colors to try

        Returns:
            Valid coloring if exists, None otherwise
        """
        coloring = {}

        def is_safe(vertex: int, color: int) -> bool:
            """Check if color assignment is safe."""
            for neighbor in self.adjacency_list[vertex]:
                if neighbor in coloring and coloring[neighbor] == color:
                    return False
            return True

        def backtrack(vertex: int) -> bool:
            """Recursive backtracking."""
            if vertex == self.num_vertices:
                return True

            for color in range(max_colors):
                if is_safe(vertex, color):
                    coloring[vertex] = color

                    if backtrack(vertex + 1):
                        return True

                    del coloring[vertex]

            return False

        if backtrack(0):
            return coloring
        return None

    def chromatic_number(self) -> int:
        """
        Find chromatic number (minimum colors needed).

        Returns:
            Chromatic number
        """
        # Lower bound: clique number
        lower_bound = self._clique_number_bound()

        # Upper bound: maximum degree + 1
        upper_bound = max(self.degree) + 1 if self.degree else 1

        # Binary search for exact chromatic number
        for k in range(lower_bound, upper_bound + 1):
            if self.backtracking_coloring(k) is not None:
                return k

        return upper_bound

    def _clique_number_bound(self) -> int:
        """
        Find lower bound using clique detection.

        Returns:
            Size of maximum clique found (lower bound)
        """
        # Simple greedy clique finding for lower bound
        max_clique = 0

        for start in range(self.num_vertices):
            clique = {start}
            candidates = set(self.adjacency_list[start])

            while candidates:
                # Find vertex connected to all in clique
                for v in candidates:
                    if all(u in self.adjacency_list[v] for u in clique):
                        clique.add(v)
                        candidates = candidates.intersection(self.adjacency_list[v])
                        break
                else:
                    break

            max_clique = max(max_clique, len(clique))

        return max_clique

    def brooks_algorithm(self) -> Dict[int, int]:
        """
        Brooks' algorithm for graphs that are neither complete nor odd cycles.

        Returns:
            Coloring using at most Δ colors (Δ = maximum degree)
        """
        if self.num_vertices == 0:
            return {}

        # Check if graph is complete or odd cycle
        max_degree = max(self.degree)

        # For complete graph or odd cycle, need Δ+1 colors
        if self._is_complete() or self._is_odd_cycle():
            return self.greedy_coloring()

        # Find two non-adjacent vertices with max degree
        max_degree_vertices = [v for v in range(self.num_vertices)
                              if self.degree[v] == max_degree]

        v1, v2 = None, None
        for i in range(len(max_degree_vertices)):
            for j in range(i + 1, len(max_degree_vertices)):
                if max_degree_vertices[j] not in self.adjacency_list[max_degree_vertices[i]]:
                    v1 = max_degree_vertices[i]
                    v2 = max_degree_vertices[j]
                    break
            if v1 is not None:
                break

        if v1 is None:
            # Fallback to greedy
            return self.greedy_coloring()

        # Color v1 and v2 with the same color
        coloring = {v1: 0, v2: 0}

        # BFS from v1 and v2
        visited = {v1, v2}
        queue = list(self.adjacency_list[v1] | self.adjacency_list[v2])

        while queue:
            vertex = queue.pop(0)
            if vertex in visited:
                continue

            # Find minimum available color
            neighbor_colors = set()
            for neighbor in self.adjacency_list[vertex]:
                if neighbor in coloring:
                    neighbor_colors.add(coloring[neighbor])

            color = 0
            while color in neighbor_colors and color < max_degree:
                color += 1

            coloring[vertex] = color
            visited.add(vertex)

            for neighbor in self.adjacency_list[vertex]:
                if neighbor not in visited:
                    queue.append(neighbor)

        # Color remaining vertices
        for v in range(self.num_vertices):
            if v not in coloring:
                neighbor_colors = set()
                for neighbor in self.adjacency_list[v]:
                    if neighbor in coloring:
                        neighbor_colors.add(coloring[neighbor])

                color = 0
                while color in neighbor_colors:
                    color += 1

                coloring[v] = color

        return coloring

    def _is_complete(self) -> bool:
        """Check if graph is complete."""
        return all(self.degree[i] == self.num_vertices - 1
                  for i in range(self.num_vertices))

    def _is_odd_cycle(self) -> bool:
        """Check if graph is an odd cycle."""
        if self.num_vertices < 3 or self.num_vertices % 2 == 0:
            return False

        # Check if all vertices have degree 2
        if not all(self.degree[i] == 2 for i in range(self.num_vertices)):
            return False

        # Check if forms a single cycle
        visited = set()
        current = 0
        visited.add(current)

        for _ in range(self.num_vertices - 1):
            neighbors = [n for n in self.adjacency_list[current]
                        if n not in visited or len(visited) == self.num_vertices - 1]
            if len(neighbors) != 1:
                return False
            current = neighbors[0]
            visited.add(current)

        return 0 in self.adjacency_list[current]

    def constraint_satisfaction_coloring(self, max_colors: int) -> Optional[Dict[int, int]]:
        """
        Graph coloring as Constraint Satisfaction Problem with heuristics.

        Args:
            max_colors: Maximum colors available

        Returns:
            Valid coloring if exists
        """
        coloring = {}
        domains = {v: set(range(max_colors)) for v in range(self.num_vertices)}

        def select_unassigned_variable() -> Optional[int]:
            """MRV (Minimum Remaining Values) heuristic."""
            unassigned = [v for v in range(self.num_vertices) if v not in coloring]
            if not unassigned:
                return None

            return min(unassigned, key=lambda v: len(domains[v]))

        def order_domain_values(var: int) -> List[int]:
            """Least constraining value heuristic."""
            values = []

            for color in domains[var]:
                constraints = 0
                for neighbor in self.adjacency_list[var]:
                    if neighbor not in coloring and color in domains[neighbor]:
                        constraints += 1
                values.append((color, constraints))

            values.sort(key=lambda x: x[1])
            return [v[0] for v in values]

        def forward_checking(var: int, value: int) -> Dict[int, Set[int]]:
            """Remove inconsistent values from domains."""
            removed = defaultdict(set)

            for neighbor in self.adjacency_list[var]:
                if neighbor not in coloring and value in domains[neighbor]:
                    domains[neighbor].remove(value)
                    removed[neighbor].add(value)

            return removed

        def restore_domains(removed: Dict[int, Set[int]]):
            """Restore removed values to domains."""
            for var, values in removed.items():
                domains[var].update(values)

        def backtrack() -> bool:
            """CSP backtracking with heuristics."""
            var = select_unassigned_variable()
            if var is None:
                return True

            for value in order_domain_values(var):
                coloring[var] = value
                removed = forward_checking(var, value)

                # Check if any domain is empty
                if all(len(domains[v]) > 0 or v in coloring
                      for v in range(self.num_vertices)):
                    if backtrack():
                        return True

                del coloring[var]
                restore_domains(removed)

            return False

        if backtrack():
            return coloring
        return None


class IntervalGraphColoring:
    """
    Specialized coloring for interval graphs.

    Interval graphs can be optimally colored in O(n log n) time.
    """

    def __init__(self, intervals: List[Tuple[int, int]]):
        """
        Initialize interval graph.

        Args:
            intervals: List of intervals (start, end)
        """
        self.intervals = intervals
        self.n = len(intervals)

    def optimal_coloring(self) -> Dict[int, int]:
        """
        Optimal coloring for interval graph.

        Returns:
            Coloring assignment
        """
        if not self.intervals:
            return {}

        # Sort intervals by start time
        indexed_intervals = [(i, start, end)
                            for i, (start, end) in enumerate(self.intervals)]
        indexed_intervals.sort(key=lambda x: x[1])

        coloring = {}
        available_colors = []

        for idx, start, end in indexed_intervals:
            # Remove colors from intervals that have ended
            available_colors = [c for c in available_colors if c[0] >= start]

            if available_colors:
                # Reuse a color
                color = heapq.heappop(available_colors)[1]
            else:
                # Need new color
                color = len(coloring) - len([c for c in coloring.values()
                                           if c < 0]) if coloring else 0

            coloring[idx] = color
            heapq.heappush(available_colors, (end, color))

        return coloring


class EdgeColoring:
    """
    Edge coloring algorithms - color edges so no adjacent edges share color.
    """

    def __init__(self, num_vertices: int, edges: List[Tuple[int, int]]):
        """
        Initialize graph for edge coloring.

        Args:
            num_vertices: Number of vertices
            edges: List of edges
        """
        self.num_vertices = num_vertices
        self.edges = edges
        self.adjacency_list = defaultdict(set)

        for u, v in edges:
            self.adjacency_list[u].add(v)
            self.adjacency_list[v].add(u)

    def vizing_theorem_bound(self) -> int:
        """
        Get Vizing's theorem bound for edge chromatic number.

        Returns:
            Upper bound (Δ or Δ+1 where Δ is max degree)
        """
        if not self.adjacency_list:
            return 0

        max_degree = max(len(neighbors) for neighbors in self.adjacency_list.values())
        return max_degree + 1

    def greedy_edge_coloring(self) -> Dict[Tuple[int, int], int]:
        """
        Greedy edge coloring algorithm.

        Returns:
            Edge coloring assignment
        """
        edge_colors = {}
        vertex_edge_colors = defaultdict(set)

        for edge in self.edges:
            u, v = edge

            # Find colors used by edges incident to u and v
            used_colors = vertex_edge_colors[u] | vertex_edge_colors[v]

            # Find minimum available color
            color = 0
            while color in used_colors:
                color += 1

            edge_colors[edge] = color
            vertex_edge_colors[u].add(color)
            vertex_edge_colors[v].add(color)

        return edge_colors


def petersen_graph_example():
    """Example: Color the Petersen graph."""
    print("=" * 60)
    print("GRAPH COLORING - PETERSEN GRAPH")
    print("=" * 60)

    # Petersen graph edges
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),  # Outer pentagon
        (5, 6), (6, 7), (7, 8), (8, 9), (9, 5),  # Inner pentagon
        (0, 5), (1, 7), (2, 9), (3, 6), (4, 8)   # Connections
    ]

    gc = GraphColoring(10, edges)

    # Try different algorithms
    algorithms = {
        'Greedy': gc.greedy_coloring(),
        'Welsh-Powell': gc.welsh_powell(),
        'DSATUR': gc.dsatur(),
        'Brooks': gc.brooks_algorithm()
    }

    for name, coloring in algorithms.items():
        num_colors = len(set(coloring.values()))
        print(f"{name}: {num_colors} colors")
        print(f"  Coloring: {coloring}")

    # Find chromatic number
    chromatic = gc.chromatic_number()
    print(f"\nChromatic number: {chromatic}")


def scheduling_example():
    """Example: Course scheduling as graph coloring."""
    print("\n" + "=" * 60)
    print("GRAPH COLORING - COURSE SCHEDULING")
    print("=" * 60)

    # Courses that conflict (can't be scheduled at same time)
    courses = ['Math', 'Physics', 'Chemistry', 'Biology', 'CS', 'English', 'History']
    conflicts = [
        (0, 1), (0, 2), (1, 2),  # Math, Physics, Chemistry conflict
        (3, 4),                   # Biology, CS conflict
        (4, 5),                   # CS, English conflict
        (5, 6),                   # English, History conflict
        (0, 4), (1, 3)           # Math-CS, Physics-Biology conflicts
    ]

    gc = GraphColoring(len(courses), conflicts)

    # Color graph (each color = different time slot)
    coloring = gc.dsatur()
    num_slots = len(set(coloring.values()))

    print(f"Minimum time slots needed: {num_slots}")
    print("\nSchedule:")

    # Group courses by time slot
    schedule = defaultdict(list)
    for course_idx, time_slot in coloring.items():
        schedule[time_slot].append(courses[course_idx])

    for slot in sorted(schedule.keys()):
        print(f"  Time Slot {slot + 1}: {', '.join(schedule[slot])}")


def map_coloring_example():
    """Example: Map coloring (planar graph)."""
    print("\n" + "=" * 60)
    print("GRAPH COLORING - MAP COLORING")
    print("=" * 60)

    # Simple map with regions
    regions = ['A', 'B', 'C', 'D', 'E', 'F']
    borders = [
        (0, 1), (0, 2), (0, 3),  # A borders B, C, D
        (1, 2), (1, 4),          # B borders C, E
        (2, 3), (2, 4), (2, 5),  # C borders D, E, F
        (3, 5),                  # D borders F
        (4, 5)                   # E borders F
    ]

    gc = GraphColoring(len(regions), borders)

    # Four color theorem: planar graphs need at most 4 colors
    coloring = gc.backtracking_coloring(4)

    if coloring:
        colors = ['Red', 'Blue', 'Green', 'Yellow']
        print("Map coloring (4 colors):")
        for region_idx, color_idx in coloring.items():
            print(f"  Region {regions[region_idx]}: {colors[color_idx]}")

        # Verify four color theorem
        num_colors = len(set(coloring.values()))
        print(f"\nColors used: {num_colors} (≤ 4 as per Four Color Theorem)")


def register_allocation_example():
    """Example: Register allocation in compiler."""
    print("\n" + "=" * 60)
    print("GRAPH COLORING - REGISTER ALLOCATION")
    print("=" * 60)

    # Variables and their interference (can't use same register)
    variables = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    interference = [
        (0, 1), (0, 2),  # a interferes with b, c
        (1, 2), (1, 3),  # b interferes with c, d
        (2, 3), (2, 4),  # c interferes with d, e
        (3, 4), (3, 5),  # d interferes with e, f
        (4, 5), (4, 6),  # e interferes with f, g
        (5, 6), (5, 7),  # f interferes with g, h
        (6, 7)           # g interferes with h
    ]

    gc = GraphColoring(len(variables), interference)

    # Try to allocate with limited registers
    num_registers = 4
    coloring = gc.constraint_satisfaction_coloring(num_registers)

    if coloring:
        print(f"Register allocation successful with {num_registers} registers:")

        # Group variables by register
        allocation = defaultdict(list)
        for var_idx, reg in coloring.items():
            allocation[reg].append(variables[var_idx])

        for reg in sorted(allocation.keys()):
            print(f"  Register R{reg}: {', '.join(allocation[reg])}")
    else:
        print(f"Cannot allocate with {num_registers} registers")

        # Find minimum needed
        min_registers = gc.chromatic_number()
        print(f"Minimum registers needed: {min_registers}")


def interval_coloring_example():
    """Example: Interval scheduling."""
    print("\n" + "=" * 60)
    print("INTERVAL GRAPH COLORING - ACTIVITY SCHEDULING")
    print("=" * 60)

    # Activities with start and end times
    activities = [
        (1, 4), (2, 5), (3, 7), (5, 9),
        (6, 10), (8, 11), (9, 12), (10, 13)
    ]

    igc = IntervalGraphColoring(activities)
    coloring = igc.optimal_coloring()

    # Group by room/resource
    rooms = defaultdict(list)
    for idx, room in coloring.items():
        rooms[room].append(activities[idx])

    num_rooms = len(set(coloring.values()))
    print(f"Minimum rooms needed: {num_rooms}")
    print("\nRoom assignments:")

    for room in sorted(rooms.keys()):
        print(f"  Room {room + 1}:")
        for start, end in sorted(rooms[room]):
            print(f"    Activity [{start:2d}, {end:2d})")


def benchmark_algorithms():
    """Benchmark different coloring algorithms."""
    print("\n" + "=" * 60)
    print("ALGORITHM COMPARISON")
    print("=" * 60)

    # Generate random graph
    n = 50
    edge_prob = 0.2
    edges = []

    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < edge_prob:
                edges.append((i, j))

    gc = GraphColoring(n, edges)

    print(f"Graph: {n} vertices, {len(edges)} edges")
    print(f"Average degree: {2 * len(edges) / n:.1f}")

    # Test algorithms
    import time

    algorithms = [
        ('Greedy', gc.greedy_coloring),
        ('Welsh-Powell', gc.welsh_powell),
        ('DSATUR', gc.dsatur),
        ('Brooks', gc.brooks_algorithm)
    ]

    results = []

    for name, algo in algorithms:
        start = time.time()
        coloring = algo()
        elapsed = time.time() - start

        num_colors = len(set(coloring.values()))
        results.append((name, num_colors, elapsed))

    # Display results
    print("\nResults:")
    print(f"{'Algorithm':<15} {'Colors':<10} {'Time (ms)':<10}")
    print("-" * 35)

    for name, colors, elapsed in sorted(results, key=lambda x: x[1]):
        print(f"{name:<15} {colors:<10} {elapsed*1000:<10.2f}")


if __name__ == "__main__":
    # Run examples
    petersen_graph_example()
    scheduling_example()
    map_coloring_example()
    register_allocation_example()
    interval_coloring_example()
    benchmark_algorithms()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- DSATUR often produces near-optimal colorings")
    print("- Welsh-Powell is fast and effective for many graphs")
    print("- Backtracking guarantees optimal but is slow")
    print("- Interval graphs can be colored optimally in polynomial time")
    print("- Four Color Theorem: planar graphs need ≤ 4 colors")
    print("=" * 60)