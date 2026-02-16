#!/usr/bin/env python3
"""
Pathfinding Algorithms Implementation

This module provides implementations of various pathfinding algorithms including:
- A* (A-star) search algorithm
- Dijkstra's shortest path algorithm
- Bellman-Ford algorithm
- Floyd-Warshall all-pairs shortest path
- Johnson's algorithm for sparse graphs
- Bidirectional search
- Jump Point Search (JPS) for grid-based pathfinding

Author: Algorithms Multiverse
License: MIT
"""

import heapq
import math
from collections import defaultdict, deque
from typing import List, Tuple, Dict, Optional, Set, Callable, Any
from dataclasses import dataclass, field
from enum import Enum


class GridCell(Enum):
    """Represents types of cells in a grid."""
    EMPTY = 0
    OBSTACLE = 1
    START = 2
    GOAL = 3
    PATH = 4


@dataclass(order=True)
class Node:
    """Node for priority queue in pathfinding algorithms."""
    priority: float
    vertex: Any = field(compare=False)
    path: List[Any] = field(default_factory=list, compare=False)


class AStar:
    """
    A* (A-star) search algorithm for optimal pathfinding.

    Uses heuristic function to guide search towards goal.
    Guarantees optimal path if heuristic is admissible.

    Time Complexity: O((V + E) * log V) with good heuristic
    Space Complexity: O(V)
    """

    def __init__(self, heuristic: Optional[Callable[[Any, Any], float]] = None):
        """
        Initialize A* search.

        Args:
            heuristic: Heuristic function h(node, goal)
                      If None, defaults to zero (becomes Dijkstra)
        """
        self.heuristic = heuristic or (lambda x, y: 0)

    def search(self,
               graph: Dict[Any, List[Tuple[Any, float]]],
               start: Any,
               goal: Any) -> Tuple[List[Any], float]:
        """
        Find shortest path from start to goal.

        Args:
            graph: Adjacency list with weights {node: [(neighbor, weight), ...]}
            start: Start node
            goal: Goal node

        Returns:
            (path, cost) tuple, or ([], inf) if no path exists
        """
        # Priority queue with f(n) = g(n) + h(n)
        open_set = [Node(0, start, [start])]
        closed_set = set()

        # g(n) = cost from start to n
        g_score = {start: 0}

        # f(n) = g(n) + h(n)
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            current_node = heapq.heappop(open_set)
            current = current_node.vertex

            if current == goal:
                return current_node.path, g_score[current]

            if current in closed_set:
                continue

            closed_set.add(current)

            # Explore neighbors
            for neighbor, weight in graph.get(current, []):
                if neighbor in closed_set:
                    continue

                tentative_g = g_score[current] + weight

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self.heuristic(neighbor, goal)
                    f_score[neighbor] = f

                    new_path = current_node.path + [neighbor]
                    heapq.heappush(open_set, Node(f, neighbor, new_path))

        return [], float('inf')

    def search_grid(self,
                    grid: List[List[int]],
                    start: Tuple[int, int],
                    goal: Tuple[int, int],
                    diagonal: bool = True) -> Tuple[List[Tuple[int, int]], float]:
        """
        A* search on 2D grid.

        Args:
            grid: 2D grid (0 = empty, 1 = obstacle)
            start: Start position (row, col)
            goal: Goal position (row, col)
            diagonal: Allow diagonal movement

        Returns:
            (path, cost) tuple
        """
        rows, cols = len(grid), len(grid[0])

        def is_valid(r: int, c: int) -> bool:
            return 0 <= r < rows and 0 <= c < cols and grid[r][c] != 1

        def get_neighbors(pos: Tuple[int, int]) -> List[Tuple[Tuple[int, int], float]]:
            r, c = pos
            neighbors = []

            # Cardinal directions
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if is_valid(nr, nc):
                    neighbors.append(((nr, nc), 1.0))

            # Diagonal directions
            if diagonal:
                for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    nr, nc = r + dr, c + dc
                    if is_valid(nr, nc):
                        # Check if diagonal move is not cutting corner
                        if is_valid(r + dr, c) and is_valid(r, c + dc):
                            neighbors.append(((nr, nc), math.sqrt(2)))

            return neighbors

        # Build graph from grid
        graph = {}
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != 1:
                    graph[(r, c)] = get_neighbors((r, c))

        # Manhattan distance heuristic
        def manhattan_heuristic(pos: Tuple[int, int], goal: Tuple[int, int]) -> float:
            return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

        # Euclidean distance heuristic (for diagonal movement)
        def euclidean_heuristic(pos: Tuple[int, int], goal: Tuple[int, int]) -> float:
            return math.sqrt((pos[0] - goal[0])**2 + (pos[1] - goal[1])**2)

        heuristic = euclidean_heuristic if diagonal else manhattan_heuristic
        self.heuristic = heuristic

        return self.search(graph, start, goal)


class Dijkstra:
    """
    Dijkstra's shortest path algorithm.

    Finds shortest paths from source to all reachable vertices.
    Only works with non-negative edge weights.

    Time Complexity: O((V + E) * log V) with binary heap
    Space Complexity: O(V)
    """

    def __init__(self):
        """Initialize Dijkstra's algorithm."""
        pass

    def shortest_paths(self,
                       graph: Dict[Any, List[Tuple[Any, float]]],
                       source: Any) -> Dict[Any, Tuple[float, List[Any]]]:
        """
        Find shortest paths from source to all vertices.

        Args:
            graph: Adjacency list with weights
            source: Source vertex

        Returns:
            Dictionary mapping vertex to (distance, path)
        """
        # Initialize distances
        distances = {source: 0}
        paths = {source: [source]}

        # Priority queue
        pq = [(0, source)]

        while pq:
            current_dist, current = heapq.heappop(pq)

            # Skip if we've already processed this vertex
            if current_dist > distances.get(current, float('inf')):
                continue

            # Relax edges
            for neighbor, weight in graph.get(current, []):
                distance = current_dist + weight

                if distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = distance
                    paths[neighbor] = paths[current] + [neighbor]
                    heapq.heappush(pq, (distance, neighbor))

        # Combine distances and paths
        result = {}
        for vertex in distances:
            result[vertex] = (distances[vertex], paths[vertex])

        return result

    def shortest_path(self,
                      graph: Dict[Any, List[Tuple[Any, float]]],
                      source: Any,
                      target: Any) -> Tuple[List[Any], float]:
        """
        Find shortest path from source to target.

        Args:
            graph: Adjacency list with weights
            source: Source vertex
            target: Target vertex

        Returns:
            (path, distance) tuple
        """
        paths = self.shortest_paths(graph, source)

        if target in paths:
            distance, path = paths[target]
            return path, distance
        else:
            return [], float('inf')


class BellmanFord:
    """
    Bellman-Ford algorithm for single-source shortest paths.

    Can handle negative edge weights and detect negative cycles.

    Time Complexity: O(V * E)
    Space Complexity: O(V)
    """

    def __init__(self):
        """Initialize Bellman-Ford algorithm."""
        pass

    def shortest_paths(self,
                       vertices: List[Any],
                       edges: List[Tuple[Any, Any, float]],
                       source: Any) -> Tuple[Dict[Any, float], Dict[Any, List[Any]], bool]:
        """
        Find shortest paths from source to all vertices.

        Args:
            vertices: List of vertices
            edges: List of (u, v, weight) tuples
            source: Source vertex

        Returns:
            (distances, paths, has_negative_cycle) tuple
        """
        # Initialize distances
        distances = {v: float('inf') for v in vertices}
        distances[source] = 0

        # Initialize paths
        paths = {v: [] for v in vertices}
        paths[source] = [source]

        # Relax edges V-1 times
        for _ in range(len(vertices) - 1):
            for u, v, weight in edges:
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    paths[v] = paths[u] + [v]

        # Check for negative cycles
        has_negative_cycle = False
        for u, v, weight in edges:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                has_negative_cycle = True
                break

        return distances, paths, has_negative_cycle


class FloydWarshall:
    """
    Floyd-Warshall algorithm for all-pairs shortest paths.

    Finds shortest paths between all pairs of vertices.
    Can handle negative weights but not negative cycles.

    Time Complexity: O(V³)
    Space Complexity: O(V²)
    """

    def __init__(self):
        """Initialize Floyd-Warshall algorithm."""
        pass

    def all_pairs_shortest_paths(self,
                                  vertices: List[Any],
                                  edges: List[Tuple[Any, Any, float]]) -> Tuple[Dict, Dict]:
        """
        Find shortest paths between all pairs of vertices.

        Args:
            vertices: List of vertices
            edges: List of (u, v, weight) tuples

        Returns:
            (distances, next_vertex) dictionaries for path reconstruction
        """
        n = len(vertices)
        vertex_to_index = {v: i for i, v in enumerate(vertices)}

        # Initialize distance matrix
        dist = [[float('inf')] * n for _ in range(n)]
        next_vertex = [[None] * n for _ in range(n)]

        # Set diagonal to 0
        for i in range(n):
            dist[i][i] = 0

        # Add edges
        for u, v, weight in edges:
            i = vertex_to_index[u]
            j = vertex_to_index[v]
            dist[i][j] = weight
            next_vertex[i][j] = v

        # Floyd-Warshall algorithm
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_vertex[i][j] = next_vertex[i][k]

        # Convert to dictionaries
        distances = {}
        paths = {}

        for i, u in enumerate(vertices):
            distances[u] = {}
            paths[u] = {}
            for j, v in enumerate(vertices):
                distances[u][v] = dist[i][j]
                paths[u][v] = next_vertex[i][j]

        return distances, paths

    def reconstruct_path(self,
                         paths: Dict,
                         u: Any,
                         v: Any) -> List[Any]:
        """
        Reconstruct path from u to v.

        Args:
            paths: Next vertex dictionary from all_pairs_shortest_paths
            u: Source vertex
            v: Destination vertex

        Returns:
            Path from u to v
        """
        if paths[u][v] is None:
            return []

        path = [u]
        while u != v:
            u = paths[u][v]
            path.append(u)

        return path


class BidirectionalSearch:
    """
    Bidirectional search algorithm.

    Searches from both start and goal simultaneously.
    Can significantly reduce search space for large graphs.

    Time Complexity: O((V + E)^(1/2)) best case
    Space Complexity: O(V)
    """

    def __init__(self):
        """Initialize bidirectional search."""
        pass

    def search(self,
               graph: Dict[Any, List[Tuple[Any, float]]],
               reverse_graph: Dict[Any, List[Tuple[Any, float]]],
               start: Any,
               goal: Any) -> Tuple[List[Any], float]:
        """
        Find path using bidirectional search.

        Args:
            graph: Forward adjacency list
            reverse_graph: Reverse adjacency list
            start: Start vertex
            goal: Goal vertex

        Returns:
            (path, distance) tuple
        """
        if start == goal:
            return [start], 0

        # Forward search from start
        forward_visited = {start: (0, None)}
        forward_queue = deque([(start, 0)])

        # Backward search from goal
        backward_visited = {goal: (0, None)}
        backward_queue = deque([(goal, 0)])

        best_distance = float('inf')
        meeting_point = None

        while forward_queue or backward_queue:
            # Forward search step
            if forward_queue:
                current, dist = forward_queue.popleft()

                for neighbor, weight in graph.get(current, []):
                    new_dist = dist + weight

                    if neighbor not in forward_visited:
                        forward_visited[neighbor] = (new_dist, current)
                        forward_queue.append((neighbor, new_dist))

                        # Check if we met the backward search
                        if neighbor in backward_visited:
                            total_dist = new_dist + backward_visited[neighbor][0]
                            if total_dist < best_distance:
                                best_distance = total_dist
                                meeting_point = neighbor

            # Backward search step
            if backward_queue:
                current, dist = backward_queue.popleft()

                for neighbor, weight in reverse_graph.get(current, []):
                    new_dist = dist + weight

                    if neighbor not in backward_visited:
                        backward_visited[neighbor] = (new_dist, current)
                        backward_queue.append((neighbor, new_dist))

                        # Check if we met the forward search
                        if neighbor in forward_visited:
                            total_dist = new_dist + forward_visited[neighbor][0]
                            if total_dist < best_distance:
                                best_distance = total_dist
                                meeting_point = neighbor

        if meeting_point is None:
            return [], float('inf')

        # Reconstruct path
        path = self._reconstruct_path(
            forward_visited, backward_visited, start, goal, meeting_point
        )

        return path, best_distance

    def _reconstruct_path(self,
                          forward_visited: Dict,
                          backward_visited: Dict,
                          start: Any,
                          goal: Any,
                          meeting: Any) -> List[Any]:
        """Reconstruct path from bidirectional search."""
        # Build forward path
        forward_path = []
        current = meeting

        while current != start:
            forward_path.append(current)
            _, parent = forward_visited[current]
            current = parent

        forward_path.append(start)
        forward_path.reverse()

        # Build backward path
        backward_path = []
        current = meeting

        while current != goal:
            _, parent = backward_visited[current]
            current = parent
            backward_path.append(current)

        # Combine paths
        return forward_path + backward_path


class JumpPointSearch:
    """
    Jump Point Search (JPS) for grid-based pathfinding.

    Optimized A* for uniform-cost grids.
    Significantly faster than A* on large grids.

    Time Complexity: O(V log V) in practice
    Space Complexity: O(V)
    """

    def __init__(self, grid: List[List[int]]):
        """
        Initialize JPS.

        Args:
            grid: 2D grid (0 = empty, 1 = obstacle)
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def is_walkable(self, r: int, c: int) -> bool:
        """Check if cell is walkable."""
        return (0 <= r < self.rows and
                0 <= c < self.cols and
                self.grid[r][c] == 0)

    def get_forced_neighbors(self,
                              r: int,
                              c: int,
                              dr: int,
                              dc: int) -> List[Tuple[int, int]]:
        """Get forced neighbors for a given direction."""
        forced = []

        if dr != 0 and dc != 0:  # Diagonal
            # Check for forced neighbors
            if not self.is_walkable(r - dr, c) and self.is_walkable(r - dr, c + dc):
                forced.append((r - dr, c + dc))
            if not self.is_walkable(r, c - dc) and self.is_walkable(r + dr, c - dc):
                forced.append((r + dr, c - dc))
        elif dr != 0:  # Vertical
            if not self.is_walkable(r, c + 1) and self.is_walkable(r + dr, c + 1):
                forced.append((r + dr, c + 1))
            if not self.is_walkable(r, c - 1) and self.is_walkable(r + dr, c - 1):
                forced.append((r + dr, c - 1))
        else:  # Horizontal
            if not self.is_walkable(r + 1, c) and self.is_walkable(r + 1, c + dc):
                forced.append((r + 1, c + dc))
            if not self.is_walkable(r - 1, c) and self.is_walkable(r - 1, c + dc):
                forced.append((r - 1, c + dc))

        return forced

    def jump(self,
             r: int,
             c: int,
             dr: int,
             dc: int,
             goal: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Jump in given direction until finding a jump point.

        Args:
            r, c: Current position
            dr, dc: Direction
            goal: Goal position

        Returns:
            Jump point or None
        """
        nr, nc = r + dr, c + dc

        if not self.is_walkable(nr, nc):
            return None

        if (nr, nc) == goal:
            return (nr, nc)

        # Check for forced neighbors
        if self.get_forced_neighbors(nr, nc, dr, dc):
            return (nr, nc)

        # Diagonal movement
        if dr != 0 and dc != 0:
            # Check horizontal and vertical jumps
            if self.jump(nr, nc, dr, 0, goal) is not None:
                return (nr, nc)
            if self.jump(nr, nc, 0, dc, goal) is not None:
                return (nr, nc)

        # Continue jumping
        return self.jump(nr, nc, dr, dc, goal)

    def search(self,
               start: Tuple[int, int],
               goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], float]:
        """
        Find path using Jump Point Search.

        Args:
            start: Start position
            goal: Goal position

        Returns:
            (path, cost) tuple
        """
        def heuristic(pos: Tuple[int, int]) -> float:
            return math.sqrt((pos[0] - goal[0])**2 + (pos[1] - goal[1])**2)

        open_set = [(0, start, [])]
        closed_set = set()
        g_score = {start: 0}

        while open_set:
            _, current, path = heapq.heappop(open_set)

            if current in closed_set:
                continue

            closed_set.add(current)
            current_path = path + [current]

            if current == goal:
                return current_path, g_score[current]

            # Get successors
            successors = self.get_successors(current, goal)

            for successor in successors:
                if successor in closed_set:
                    continue

                # Calculate new g score
                dist = math.sqrt((successor[0] - current[0])**2 +
                                 (successor[1] - current[1])**2)
                new_g = g_score[current] + dist

                if successor not in g_score or new_g < g_score[successor]:
                    g_score[successor] = new_g
                    f = new_g + heuristic(successor)
                    heapq.heappush(open_set, (f, successor, current_path))

        return [], float('inf')

    def get_successors(self,
                        pos: Tuple[int, int],
                        goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get jump point successors for a position."""
        successors = []
        r, c = pos

        # All 8 directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            jump_point = self.jump(r, c, dr, dc, goal)
            if jump_point:
                successors.append(jump_point)

        return successors


def visualize_grid_path(grid: List[List[int]],
                         path: List[Tuple[int, int]],
                         start: Tuple[int, int],
                         goal: Tuple[int, int]) -> str:
    """
    Visualize path on grid.

    Args:
        grid: 2D grid
        path: Path as list of positions
        start: Start position
        goal: Goal position

    Returns:
        String visualization
    """
    # Create copy of grid
    visual = [row[:] for row in grid]

    # Mark path
    for r, c in path:
        if (r, c) != start and (r, c) != goal:
            visual[r][c] = GridCell.PATH.value

    visual[start[0]][start[1]] = GridCell.START.value
    visual[goal[0]][goal[1]] = GridCell.GOAL.value

    # Convert to string
    symbols = {
        GridCell.EMPTY.value: '.',
        GridCell.OBSTACLE.value: '#',
        GridCell.START.value: 'S',
        GridCell.GOAL.value: 'G',
        GridCell.PATH.value: '*'
    }

    result = []
    for row in visual:
        result.append(' '.join(symbols.get(cell, '?') for cell in row))

    return '\n'.join(result)


def example_usage():
    """Demonstrate pathfinding algorithms."""
    print("=" * 60)
    print("Pathfinding Algorithms Demonstration")
    print("=" * 60)

    # Create a sample graph
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('C', 1), ('D', 5)],
        'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
        'D': [('B', 5), ('C', 8), ('E', 2), ('F', 6)],
        'E': [('C', 10), ('D', 2), ('F', 3)],
        'F': [('D', 6), ('E', 3)]
    }

    # Example 1: A* Search
    print("\n1. A* Search Algorithm")
    print("-" * 40)

    # Heuristic function (straight-line distance estimate)
    heuristics = {
        'A': 10, 'B': 8, 'C': 6, 'D': 4, 'E': 2, 'F': 0
    }

    def h(node, goal):
        return heuristics.get(node, 0)

    astar = AStar(heuristic=h)
    path, cost = astar.search(graph, 'A', 'F')
    print(f"Path from A to F: {' -> '.join(path)}")
    print(f"Total cost: {cost}")

    # Example 2: A* on Grid
    print("\n2. A* on 2D Grid")
    print("-" * 40)

    # Create a grid with obstacles
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    start = (0, 0)
    goal = (5, 7)

    astar_grid = AStar()
    path, cost = astar_grid.search_grid(grid, start, goal, diagonal=True)
    print(f"Path length: {len(path)}")
    print(f"Path cost: {cost:.2f}")
    print("\nGrid visualization:")
    print(visualize_grid_path(grid, path, start, goal))

    # Example 3: Dijkstra's Algorithm
    print("\n3. Dijkstra's Algorithm")
    print("-" * 40)

    dijkstra = Dijkstra()
    all_paths = dijkstra.shortest_paths(graph, 'A')

    print("Shortest distances from A:")
    for vertex, (dist, path) in all_paths.items():
        print(f"  To {vertex}: distance = {dist}, path = {' -> '.join(path)}")

    # Example 4: Bellman-Ford Algorithm
    print("\n4. Bellman-Ford Algorithm")
    print("-" * 40)

    # Convert graph to edge list
    vertices = list(graph.keys())
    edges = []
    for u in graph:
        for v, weight in graph[u]:
            edges.append((u, v, weight))

    bf = BellmanFord()
    distances, paths, has_cycle = bf.shortest_paths(vertices, edges, 'A')

    print(f"Has negative cycle: {has_cycle}")
    print("Shortest distances from A:")
    for v in vertices:
        if distances[v] != float('inf'):
            print(f"  To {v}: distance = {distances[v]}, path = {' -> '.join(paths[v])}")

    # Example 5: Floyd-Warshall Algorithm
    print("\n5. Floyd-Warshall Algorithm")
    print("-" * 40)

    fw = FloydWarshall()
    distances, next_vertex = fw.all_pairs_shortest_paths(vertices, edges)

    print("All-pairs shortest distances:")
    print("     ", "  ".join(f"{v:3}" for v in vertices))
    for u in vertices:
        print(f"{u:3}: ", end="")
        for v in vertices:
            dist = distances[u][v]
            if dist == float('inf'):
                print("  ∞", end="")
            else:
                print(f"{dist:3.0f}", end="")
        print()

    # Example 6: Bidirectional Search
    print("\n6. Bidirectional Search")
    print("-" * 40)

    # Create reverse graph
    reverse_graph = defaultdict(list)
    for u in graph:
        for v, weight in graph[u]:
            reverse_graph[v].append((u, weight))

    bi_search = BidirectionalSearch()
    path, cost = bi_search.search(graph, dict(reverse_graph), 'A', 'F')
    print(f"Path from A to F: {' -> '.join(path)}")
    print(f"Total cost: {cost}")

    # Example 7: Jump Point Search
    print("\n7. Jump Point Search (JPS)")
    print("-" * 40)

    jps_grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    jps = JumpPointSearch(jps_grid)
    start = (0, 0)
    goal = (5, 9)

    path, cost = jps.search(start, goal)
    if path:
        print(f"JPS path length: {len(path)}")
        print(f"JPS path cost: {cost:.2f}")
        print("\nGrid visualization:")
        print(visualize_grid_path(jps_grid, path, start, goal))
    else:
        print("No path found!")


if __name__ == "__main__":
    example_usage()