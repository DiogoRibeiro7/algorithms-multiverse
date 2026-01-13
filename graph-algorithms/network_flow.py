#!/usr/bin/env python3
"""
Network Flow Algorithms Implementation

This module provides implementations of various network flow algorithms including:
- Ford-Fulkerson algorithm with DFS
- Edmonds-Karp algorithm (Ford-Fulkerson with BFS)
- Dinic's algorithm for maximum flow
- Push-Relabel algorithm
- Minimum cost maximum flow
- Maximum bipartite matching
- Minimum cut algorithms

Author: Algorithms Multiverse
License: MIT
"""

import sys
from collections import defaultdict, deque
from typing import List, Tuple, Dict, Optional, Set, Any
import heapq
import math


class FlowNetwork:
    """
    Represents a flow network with capacity constraints.

    This class provides the foundation for all network flow algorithms,
    supporting both directed and undirected graphs with capacities.
    """

    def __init__(self, num_vertices: int):
        """
        Initialize a flow network.

        Args:
            num_vertices: Number of vertices in the network
        """
        self.num_vertices = num_vertices
        self.graph = defaultdict(lambda: defaultdict(int))
        self.flow = defaultdict(lambda: defaultdict(int))

    def add_edge(self, u: int, v: int, capacity: int):
        """
        Add an edge with given capacity to the network.

        Args:
            u: Source vertex
            v: Destination vertex
            capacity: Edge capacity
        """
        self.graph[u][v] += capacity

    def get_residual_capacity(self, u: int, v: int) -> int:
        """
        Get residual capacity of edge (u, v).

        Args:
            u: Source vertex
            v: Destination vertex

        Returns:
            Residual capacity
        """
        return self.graph[u][v] - self.flow[u][v]


class FordFulkerson:
    """
    Ford-Fulkerson algorithm for maximum flow using DFS.

    Time Complexity: O(E * max_flow) where E is number of edges
    Space Complexity: O(V) where V is number of vertices
    """

    def __init__(self, network: FlowNetwork):
        """
        Initialize Ford-Fulkerson algorithm.

        Args:
            network: Flow network
        """
        self.network = network
        self.visited = set()

    def dfs(self, source: int, sink: int, min_capacity: int) -> int:
        """
        DFS to find augmenting path.

        Args:
            source: Current vertex
            sink: Target vertex
            min_capacity: Minimum capacity along the path

        Returns:
            Flow pushed through the path
        """
        if source == sink:
            return min_capacity

        self.visited.add(source)

        for neighbor in self.network.graph[source]:
            residual = self.network.get_residual_capacity(source, neighbor)

            if neighbor not in self.visited and residual > 0:
                flow = self.dfs(neighbor, sink, min(min_capacity, residual))

                if flow > 0:
                    # Update flow
                    self.network.flow[source][neighbor] += flow
                    self.network.flow[neighbor][source] -= flow
                    return flow

        return 0

    def max_flow(self, source: int, sink: int) -> int:
        """
        Find maximum flow from source to sink.

        Args:
            source: Source vertex
            sink: Sink vertex

        Returns:
            Maximum flow value
        """
        max_flow_value = 0

        while True:
            self.visited.clear()
            flow = self.dfs(source, sink, float('inf'))

            if flow == 0:
                break

            max_flow_value += flow

        return max_flow_value

    def min_cut(self, source: int) -> Tuple[Set[int], Set[int]]:
        """
        Find minimum cut after computing maximum flow.

        Args:
            source: Source vertex

        Returns:
            Tuple of (S, T) where S contains source side vertices
        """
        # Perform DFS from source on residual graph
        visited = set()
        queue = [source]

        while queue:
            u = queue.pop()
            if u in visited:
                continue
            visited.add(u)

            for v in self.network.graph[u]:
                if v not in visited and self.network.get_residual_capacity(u, v) > 0:
                    queue.append(v)

        # S = visited vertices, T = remaining vertices
        S = visited
        T = set(range(self.network.num_vertices)) - S

        return S, T


class EdmondsKarp:
    """
    Edmonds-Karp algorithm - Ford-Fulkerson with BFS.

    More efficient than basic Ford-Fulkerson as it guarantees
    polynomial time complexity.

    Time Complexity: O(V * E²) where V is vertices, E is edges
    Space Complexity: O(V)
    """

    def __init__(self, network: FlowNetwork):
        """
        Initialize Edmonds-Karp algorithm.

        Args:
            network: Flow network
        """
        self.network = network

    def bfs(self, source: int, sink: int, parent: Dict[int, int]) -> bool:
        """
        BFS to find augmenting path.

        Args:
            source: Source vertex
            sink: Sink vertex
            parent: Dictionary to store path

        Returns:
            True if path found, False otherwise
        """
        visited = {source}
        queue = deque([source])

        while queue:
            u = queue.popleft()

            for v in self.network.graph[u]:
                if v not in visited and self.network.get_residual_capacity(u, v) > 0:
                    visited.add(v)
                    parent[v] = u

                    if v == sink:
                        return True

                    queue.append(v)

        return False

    def max_flow(self, source: int, sink: int) -> int:
        """
        Find maximum flow from source to sink.

        Args:
            source: Source vertex
            sink: Sink vertex

        Returns:
            Maximum flow value
        """
        parent = {}
        max_flow_value = 0

        while self.bfs(source, sink, parent):
            # Find minimum residual capacity along the path
            path_flow = float('inf')
            v = sink

            while v != source:
                u = parent[v]
                path_flow = min(path_flow, self.network.get_residual_capacity(u, v))
                v = u

            # Update flows along the path
            v = sink
            while v != source:
                u = parent[v]
                self.network.flow[u][v] += path_flow
                self.network.flow[v][u] -= path_flow
                v = u

            max_flow_value += path_flow
            parent.clear()

        return max_flow_value

    def get_flow_edges(self) -> List[Tuple[int, int, int]]:
        """
        Get all edges with positive flow.

        Returns:
            List of (u, v, flow) tuples
        """
        edges = []
        for u in self.network.flow:
            for v in self.network.flow[u]:
                if self.network.flow[u][v] > 0:
                    edges.append((u, v, self.network.flow[u][v]))
        return edges


class Dinic:
    """
    Dinic's algorithm for maximum flow using level graphs.

    More efficient than Edmonds-Karp for many networks.

    Time Complexity: O(V² * E)
    Space Complexity: O(V)
    """

    def __init__(self, network: FlowNetwork):
        """
        Initialize Dinic's algorithm.

        Args:
            network: Flow network
        """
        self.network = network
        self.level = {}

    def bfs(self, source: int, sink: int) -> bool:
        """
        BFS to construct level graph.

        Args:
            source: Source vertex
            sink: Sink vertex

        Returns:
            True if sink is reachable, False otherwise
        """
        self.level = {source: 0}
        queue = deque([source])

        while queue:
            u = queue.popleft()

            for v in self.network.graph[u]:
                if v not in self.level and self.network.get_residual_capacity(u, v) > 0:
                    self.level[v] = self.level[u] + 1
                    queue.append(v)

        return sink in self.level

    def dfs(self, u: int, sink: int, flow: int) -> int:
        """
        DFS to send flow using level graph.

        Args:
            u: Current vertex
            sink: Sink vertex
            flow: Current flow

        Returns:
            Flow pushed
        """
        if u == sink:
            return flow

        for v in self.network.graph[u]:
            if v in self.level and self.level[v] == self.level[u] + 1:
                residual = self.network.get_residual_capacity(u, v)

                if residual > 0:
                    pushed = self.dfs(v, sink, min(flow, residual))

                    if pushed > 0:
                        self.network.flow[u][v] += pushed
                        self.network.flow[v][u] -= pushed
                        return pushed

        return 0

    def max_flow(self, source: int, sink: int) -> int:
        """
        Find maximum flow from source to sink.

        Args:
            source: Source vertex
            sink: Sink vertex

        Returns:
            Maximum flow value
        """
        max_flow_value = 0

        while self.bfs(source, sink):
            while True:
                flow = self.dfs(source, sink, float('inf'))
                if flow == 0:
                    break
                max_flow_value += flow

        return max_flow_value


class PushRelabel:
    """
    Push-Relabel algorithm for maximum flow.

    Often faster in practice than augmenting path algorithms.

    Time Complexity: O(V²E) with gap heuristic and global relabeling
    Space Complexity: O(V)
    """

    def __init__(self, network: FlowNetwork):
        """
        Initialize Push-Relabel algorithm.

        Args:
            network: Flow network
        """
        self.network = network
        self.height = {}
        self.excess = defaultdict(int)
        self.active = set()

    def push(self, u: int, v: int):
        """
        Push flow from u to v.

        Args:
            u: Source vertex
            v: Destination vertex
        """
        delta = min(self.excess[u], self.network.get_residual_capacity(u, v))
        self.network.flow[u][v] += delta
        self.network.flow[v][u] -= delta
        self.excess[u] -= delta
        self.excess[v] += delta

    def relabel(self, u: int):
        """
        Relabel vertex u to maintain valid labeling.

        Args:
            u: Vertex to relabel
        """
        min_height = float('inf')

        for v in self.network.graph[u]:
            if self.network.get_residual_capacity(u, v) > 0:
                min_height = min(min_height, self.height[v])

        if min_height < float('inf'):
            self.height[u] = min_height + 1

    def discharge(self, u: int):
        """
        Discharge excess from vertex u.

        Args:
            u: Vertex to discharge
        """
        while self.excess[u] > 0:
            pushed = False

            for v in self.network.graph[u]:
                if self.network.get_residual_capacity(u, v) > 0 and self.height[u] == self.height[v] + 1:
                    self.push(u, v)
                    pushed = True

                    if self.excess[u] == 0:
                        break

            if not pushed:
                self.relabel(u)

    def max_flow(self, source: int, sink: int) -> int:
        """
        Find maximum flow from source to sink.

        Args:
            source: Source vertex
            sink: Sink vertex

        Returns:
            Maximum flow value
        """
        # Initialize preflow
        self.height = {v: 0 for v in range(self.network.num_vertices)}
        self.height[source] = self.network.num_vertices

        # Saturate edges from source
        for v in self.network.graph[source]:
            capacity = self.network.graph[source][v]
            self.network.flow[source][v] = capacity
            self.network.flow[v][source] = -capacity
            self.excess[v] = capacity

            if v != sink:
                self.active.add(v)

        # Process active vertices
        while self.active:
            u = self.active.pop()
            self.discharge(u)

            if self.excess[u] > 0:
                self.active.add(u)

        return self.excess[sink]


class BipartiteMatching:
    """
    Maximum bipartite matching using network flow.

    Reduces bipartite matching to maximum flow problem.
    """

    def __init__(self, left_size: int, right_size: int):
        """
        Initialize bipartite matching.

        Args:
            left_size: Number of vertices in left partition
            right_size: Number of vertices in right partition
        """
        self.left_size = left_size
        self.right_size = right_size

        # Create flow network with source and sink
        total_vertices = left_size + right_size + 2
        self.network = FlowNetwork(total_vertices)

        self.source = left_size + right_size
        self.sink = left_size + right_size + 1

        # Connect source to left partition
        for i in range(left_size):
            self.network.add_edge(self.source, i, 1)

        # Connect right partition to sink
        for j in range(right_size):
            self.network.add_edge(left_size + j, self.sink, 1)

    def add_edge(self, left: int, right: int):
        """
        Add edge between left and right vertices.

        Args:
            left: Vertex in left partition (0-indexed)
            right: Vertex in right partition (0-indexed)
        """
        if left >= self.left_size or right >= self.right_size:
            raise ValueError("Vertex index out of bounds")

        self.network.add_edge(left, self.left_size + right, 1)

    def max_matching(self) -> List[Tuple[int, int]]:
        """
        Find maximum matching.

        Returns:
            List of matched pairs (left, right)
        """
        # Use Edmonds-Karp for maximum flow
        ek = EdmondsKarp(self.network)
        ek.max_flow(self.source, self.sink)

        # Extract matching from flow
        matching = []
        for u in range(self.left_size):
            for v in range(self.left_size, self.left_size + self.right_size):
                if self.network.flow[u][v] > 0:
                    matching.append((u, v - self.left_size))

        return matching

    def is_perfect_matching(self) -> bool:
        """
        Check if perfect matching exists.

        Returns:
            True if perfect matching exists
        """
        matching = self.max_matching()
        return len(matching) == min(self.left_size, self.right_size)


class MinCostMaxFlow:
    """
    Minimum cost maximum flow using successive shortest path algorithm.

    Finds maximum flow with minimum total cost.
    """

    def __init__(self, num_vertices: int):
        """
        Initialize minimum cost maximum flow.

        Args:
            num_vertices: Number of vertices
        """
        self.num_vertices = num_vertices
        self.capacity = defaultdict(lambda: defaultdict(int))
        self.cost = defaultdict(lambda: defaultdict(int))
        self.flow = defaultdict(lambda: defaultdict(int))

    def add_edge(self, u: int, v: int, capacity: int, cost: int):
        """
        Add edge with capacity and cost.

        Args:
            u: Source vertex
            v: Destination vertex
            capacity: Edge capacity
            cost: Cost per unit flow
        """
        self.capacity[u][v] += capacity
        self.cost[u][v] = cost
        self.cost[v][u] = -cost

    def bellman_ford(self, source: int, sink: int) -> Tuple[List[int], List[int]]:
        """
        Find shortest path using Bellman-Ford.

        Args:
            source: Source vertex
            sink: Sink vertex

        Returns:
            Distance array and parent array
        """
        dist = [float('inf')] * self.num_vertices
        parent = [-1] * self.num_vertices
        dist[source] = 0

        # Relax edges
        for _ in range(self.num_vertices - 1):
            for u in range(self.num_vertices):
                if dist[u] == float('inf'):
                    continue

                for v in self.capacity[u]:
                    residual = self.capacity[u][v] - self.flow[u][v]

                    if residual > 0 and dist[u] + self.cost[u][v] < dist[v]:
                        dist[v] = dist[u] + self.cost[u][v]
                        parent[v] = u

        return dist, parent

    def min_cost_max_flow(self, source: int, sink: int) -> Tuple[int, int]:
        """
        Find minimum cost maximum flow.

        Args:
            source: Source vertex
            sink: Sink vertex

        Returns:
            (max_flow, min_cost) tuple
        """
        max_flow = 0
        min_cost = 0

        while True:
            dist, parent = self.bellman_ford(source, sink)

            if dist[sink] == float('inf'):
                break

            # Find minimum residual capacity along path
            path_flow = float('inf')
            v = sink

            while v != source:
                u = parent[v]
                path_flow = min(path_flow, self.capacity[u][v] - self.flow[u][v])
                v = u

            # Update flow along path
            v = sink
            while v != source:
                u = parent[v]
                self.flow[u][v] += path_flow
                self.flow[v][u] -= path_flow
                min_cost += path_flow * self.cost[u][v]
                v = u

            max_flow += path_flow

        return max_flow, min_cost


def example_usage():
    """Demonstrate network flow algorithms."""
    print("=" * 60)
    print("Network Flow Algorithms Demonstration")
    print("=" * 60)

    # Example 1: Ford-Fulkerson
    print("\n1. Ford-Fulkerson Algorithm")
    print("-" * 40)

    network1 = FlowNetwork(6)
    network1.add_edge(0, 1, 16)
    network1.add_edge(0, 2, 13)
    network1.add_edge(1, 2, 10)
    network1.add_edge(1, 3, 12)
    network1.add_edge(2, 1, 4)
    network1.add_edge(2, 4, 14)
    network1.add_edge(3, 2, 9)
    network1.add_edge(3, 5, 20)
    network1.add_edge(4, 3, 7)
    network1.add_edge(4, 5, 4)

    ff = FordFulkerson(network1)
    max_flow = ff.max_flow(0, 5)
    print(f"Maximum flow from 0 to 5: {max_flow}")

    S, T = ff.min_cut(0)
    print(f"Minimum cut - S: {S}, T: {T}")

    # Example 2: Edmonds-Karp
    print("\n2. Edmonds-Karp Algorithm")
    print("-" * 40)

    network2 = FlowNetwork(6)
    network2.add_edge(0, 1, 16)
    network2.add_edge(0, 2, 13)
    network2.add_edge(1, 2, 10)
    network2.add_edge(1, 3, 12)
    network2.add_edge(2, 1, 4)
    network2.add_edge(2, 4, 14)
    network2.add_edge(3, 2, 9)
    network2.add_edge(3, 5, 20)
    network2.add_edge(4, 3, 7)
    network2.add_edge(4, 5, 4)

    ek = EdmondsKarp(network2)
    max_flow = ek.max_flow(0, 5)
    print(f"Maximum flow from 0 to 5: {max_flow}")

    flow_edges = ek.get_flow_edges()
    print("Flow on edges:")
    for u, v, flow in flow_edges:
        print(f"  Edge {u} -> {v}: {flow}")

    # Example 3: Dinic's Algorithm
    print("\n3. Dinic's Algorithm")
    print("-" * 40)

    network3 = FlowNetwork(6)
    network3.add_edge(0, 1, 10)
    network3.add_edge(0, 2, 10)
    network3.add_edge(1, 2, 2)
    network3.add_edge(1, 3, 4)
    network3.add_edge(1, 4, 8)
    network3.add_edge(2, 4, 9)
    network3.add_edge(3, 5, 10)
    network3.add_edge(4, 3, 6)
    network3.add_edge(4, 5, 10)

    dinic = Dinic(network3)
    max_flow = dinic.max_flow(0, 5)
    print(f"Maximum flow from 0 to 5: {max_flow}")

    # Example 4: Bipartite Matching
    print("\n4. Maximum Bipartite Matching")
    print("-" * 40)

    # Create bipartite graph with 4 left vertices and 4 right vertices
    bm = BipartiteMatching(4, 4)

    # Add edges
    bm.add_edge(0, 0)  # Person 0 -> Job 0
    bm.add_edge(0, 1)  # Person 0 -> Job 1
    bm.add_edge(1, 1)  # Person 1 -> Job 1
    bm.add_edge(1, 2)  # Person 1 -> Job 2
    bm.add_edge(2, 2)  # Person 2 -> Job 2
    bm.add_edge(2, 3)  # Person 2 -> Job 3
    bm.add_edge(3, 3)  # Person 3 -> Job 3

    matching = bm.max_matching()
    print(f"Maximum matching size: {len(matching)}")
    print("Matching pairs:")
    for left, right in matching:
        print(f"  Person {left} -> Job {right}")

    print(f"Is perfect matching? {bm.is_perfect_matching()}")

    # Example 5: Min Cost Max Flow
    print("\n5. Minimum Cost Maximum Flow")
    print("-" * 40)

    mcmf = MinCostMaxFlow(4)
    mcmf.add_edge(0, 1, 2, 1)  # capacity=2, cost=1
    mcmf.add_edge(0, 2, 1, 3)  # capacity=1, cost=3
    mcmf.add_edge(1, 2, 1, 1)  # capacity=1, cost=1
    mcmf.add_edge(1, 3, 1, 2)  # capacity=1, cost=2
    mcmf.add_edge(2, 3, 2, 1)  # capacity=2, cost=1

    max_flow, min_cost = mcmf.min_cost_max_flow(0, 3)
    print(f"Maximum flow: {max_flow}")
    print(f"Minimum cost: {min_cost}")

    # Example 6: Push-Relabel
    print("\n6. Push-Relabel Algorithm")
    print("-" * 40)

    network4 = FlowNetwork(6)
    network4.add_edge(0, 1, 16)
    network4.add_edge(0, 2, 13)
    network4.add_edge(1, 2, 10)
    network4.add_edge(1, 3, 12)
    network4.add_edge(2, 1, 4)
    network4.add_edge(2, 4, 14)
    network4.add_edge(3, 2, 9)
    network4.add_edge(3, 5, 20)
    network4.add_edge(4, 3, 7)
    network4.add_edge(4, 5, 4)

    pr = PushRelabel(network4)
    max_flow = pr.max_flow(0, 5)
    print(f"Maximum flow from 0 to 5: {max_flow}")


if __name__ == "__main__":
    example_usage()