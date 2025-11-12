"""
Parallel Breadth-First Search (BFS) Implementation

This module implements parallel BFS with level synchronization for graph traversal.

Features:
- Level-synchronous parallel BFS
- Thread-safe visited set using locks
- Work distribution across multiple workers
- Support for both directed and undirected graphs
- Distance computation and path reconstruction

Time Complexity: O(V + E) where V = vertices, E = edges
Space Complexity: O(V)
Speedup: Depends on graph structure and branching factor

When to use parallel BFS:
- Large graphs (>10,000 vertices)
- High branching factor
- Multi-core systems available
- Level-wise processing needed

Author: Algorithms Multiverse
"""

import concurrent.futures
import multiprocessing as mp
import threading
import time
import queue
from typing import List, Set, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict, deque


@dataclass
class BFSResult:
    """Results from BFS traversal with performance metrics"""
    visited_order: List[int]
    distances: Dict[int, int]
    parent: Dict[int, Optional[int]]
    time_taken: float
    vertices_processed: int
    edges_explored: int
    method: str
    num_workers: int


class Graph:
    """Graph representation for BFS"""

    def __init__(self, directed: bool = False):
        """
        Initialize graph.

        Args:
            directed: Whether graph is directed
        """
        self.adj_list = defaultdict(list)
        self.directed = directed
        self.num_vertices = 0

    def add_edge(self, u: int, v: int):
        """Add edge from u to v"""
        self.adj_list[u].append(v)
        if not self.directed:
            self.adj_list[v].append(u)
        self.num_vertices = max(self.num_vertices, u + 1, v + 1)

    def get_neighbors(self, vertex: int) -> List[int]:
        """Get neighbors of a vertex"""
        return self.adj_list.get(vertex, [])

    def num_edges(self) -> int:
        """Get number of edges"""
        count = sum(len(neighbors) for neighbors in self.adj_list.values())
        return count if self.directed else count // 2


class ParallelBFS:
    """
    Parallel Breadth-First Search with level synchronization.
    """

    def __init__(self, graph: Graph, num_workers: int = None):
        """
        Initialize ParallelBFS.

        Args:
            graph: Graph to traverse
            num_workers: Number of worker threads
        """
        self.graph = graph
        self.num_workers = num_workers or mp.cpu_count()
        self.visited = set()
        self.distances = {}
        self.parent = {}
        self.visited_order = []
        self._lock = threading.Lock()
        self.edges_explored = 0

    def _reset(self):
        """Reset traversal state"""
        self.visited = set()
        self.distances = {}
        self.parent = {}
        self.visited_order = []
        self.edges_explored = 0

    def sequential_bfs(self, start: int) -> BFSResult:
        """
        Standard sequential BFS.

        Args:
            start: Starting vertex

        Returns:
            BFSResult with traversal information
        """
        self._reset()
        start_time = time.perf_counter()

        q = deque([start])
        self.visited.add(start)
        self.distances[start] = 0
        self.parent[start] = None
        self.visited_order.append(start)

        while q:
            vertex = q.popleft()

            for neighbor in self.graph.get_neighbors(vertex):
                self.edges_explored += 1
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.distances[neighbor] = self.distances[vertex] + 1
                    self.parent[neighbor] = vertex
                    self.visited_order.append(neighbor)
                    q.append(neighbor)

        time_taken = time.perf_counter() - start_time

        return BFSResult(
            visited_order=self.visited_order.copy(),
            distances=self.distances.copy(),
            parent=self.parent.copy(),
            time_taken=time_taken,
            vertices_processed=len(self.visited),
            edges_explored=self.edges_explored,
            method="sequential",
            num_workers=1
        )

    def parallel_bfs_level_sync(self, start: int) -> BFSResult:
        """
        Level-synchronous parallel BFS.

        Processes each level in parallel before moving to the next level.
        This maintains BFS ordering and correctness.

        Args:
            start: Starting vertex

        Returns:
            BFSResult with traversal information
        """
        self._reset()
        start_time = time.perf_counter()

        # Initialize with start vertex
        current_level = [start]
        self.visited.add(start)
        self.distances[start] = 0
        self.parent[start] = None
        self.visited_order.append(start)
        level = 0

        while current_level:
            next_level = []
            next_level_lock = threading.Lock()

            def process_vertex(vertex: int):
                """Process a single vertex and discover neighbors"""
                local_neighbors = []

                for neighbor in self.graph.get_neighbors(vertex):
                    with self._lock:
                        self.edges_explored += 1
                        # Check if already visited
                        if neighbor not in self.visited:
                            self.visited.add(neighbor)
                            self.distances[neighbor] = level + 1
                            self.parent[neighbor] = vertex
                            local_neighbors.append(neighbor)

                # Add discovered neighbors to next level
                if local_neighbors:
                    with next_level_lock:
                        next_level.extend(local_neighbors)
                        self.visited_order.extend(local_neighbors)

            # Process current level in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
                executor.map(process_vertex, current_level)

            current_level = next_level
            level += 1

        time_taken = time.perf_counter() - start_time

        return BFSResult(
            visited_order=self.visited_order.copy(),
            distances=self.distances.copy(),
            parent=self.parent.copy(),
            time_taken=time_taken,
            vertices_processed=len(self.visited),
            edges_explored=self.edges_explored,
            method="level_sync",
            num_workers=self.num_workers
        )

    def parallel_bfs_concurrent_queue(self, start: int) -> BFSResult:
        """
        Parallel BFS using concurrent queue.

        Workers continuously fetch work from a shared queue.
        Less synchronized than level-sync but may not maintain exact BFS order.

        Args:
            start: Starting vertex

        Returns:
            BFSResult with traversal information
        """
        self._reset()
        start_time = time.perf_counter()

        # Thread-safe queue
        work_queue = queue.Queue()
        work_queue.put(start)
        self.visited.add(start)
        self.distances[start] = 0
        self.parent[start] = None
        self.visited_order.append(start)

        # Track active workers
        active_workers = [0]
        active_lock = threading.Lock()
        done_event = threading.Event()

        def worker():
            """Worker that processes vertices from queue"""
            while not done_event.is_set():
                try:
                    vertex = work_queue.get(timeout=0.001)

                    with active_lock:
                        active_workers[0] += 1

                    # Process vertex
                    for neighbor in self.graph.get_neighbors(vertex):
                        with self._lock:
                            self.edges_explored += 1
                            if neighbor not in self.visited:
                                self.visited.add(neighbor)
                                self.distances[neighbor] = self.distances[vertex] + 1
                                self.parent[neighbor] = vertex
                                self.visited_order.append(neighbor)
                                work_queue.put(neighbor)

                    with active_lock:
                        active_workers[0] -= 1

                    work_queue.task_done()

                except queue.Empty:
                    # Check if all done
                    with active_lock:
                        if work_queue.empty() and active_workers[0] == 0:
                            done_event.set()

        # Start workers
        threads = []
        for _ in range(self.num_workers):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)

        # Wait for completion
        for t in threads:
            t.join()

        time_taken = time.perf_counter() - start_time

        return BFSResult(
            visited_order=self.visited_order.copy(),
            distances=self.distances.copy(),
            parent=self.parent.copy(),
            time_taken=time_taken,
            vertices_processed=len(self.visited),
            edges_explored=self.edges_explored,
            method="concurrent_queue",
            num_workers=self.num_workers
        )

    def parallel_bfs_bag_of_tasks(self, start: int) -> BFSResult:
        """
        Parallel BFS using bag-of-tasks pattern.

        Processes vertices in batches for better load balancing.

        Args:
            start: Starting vertex

        Returns:
            BFSResult with traversal information
        """
        self._reset()
        start_time = time.perf_counter()

        current_batch = [start]
        self.visited.add(start)
        self.distances[start] = 0
        self.parent[start] = None
        self.visited_order.append(start)
        distance = 0

        while current_batch:
            # Split batch among workers
            batch_size = max(1, len(current_batch) // self.num_workers)
            batches = [current_batch[i:i + batch_size]
                      for i in range(0, len(current_batch), batch_size)]

            next_batch = []
            next_batch_lock = threading.Lock()

            def process_batch(vertices: List[int]):
                """Process a batch of vertices"""
                local_next = []

                for vertex in vertices:
                    for neighbor in self.graph.get_neighbors(vertex):
                        with self._lock:
                            self.edges_explored += 1
                            if neighbor not in self.visited:
                                self.visited.add(neighbor)
                                self.distances[neighbor] = distance + 1
                                self.parent[neighbor] = vertex
                                local_next.append(neighbor)

                with next_batch_lock:
                    next_batch.extend(local_next)
                    self.visited_order.extend(local_next)

            # Process batches in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
                executor.map(process_batch, batches)

            current_batch = next_batch
            distance += 1

        time_taken = time.perf_counter() - start_time

        return BFSResult(
            visited_order=self.visited_order.copy(),
            distances=self.distances.copy(),
            parent=self.parent.copy(),
            time_taken=time_taken,
            vertices_processed=len(self.visited),
            edges_explored=self.edges_explored,
            method="bag_of_tasks",
            num_workers=self.num_workers
        )


def create_random_graph(num_vertices: int, edges_per_vertex: int = 5) -> Graph:
    """Create a random graph for testing"""
    import random
    graph = Graph(directed=False)

    for v in range(num_vertices):
        # Add random edges
        for _ in range(edges_per_vertex):
            neighbor = random.randint(0, num_vertices - 1)
            if neighbor != v:
                graph.add_edge(v, neighbor)

    return graph


def benchmark_all_methods(graph: Graph, start: int, num_workers: int = None) -> dict:
    """Benchmark all BFS methods"""
    results = {}

    methods = ["sequential", "level_sync", "concurrent_queue", "bag_of_tasks"]

    for method in methods:
        bfs = ParallelBFS(graph, num_workers=num_workers)

        if method == "sequential":
            results[method] = bfs.sequential_bfs(start)
        elif method == "level_sync":
            results[method] = bfs.parallel_bfs_level_sync(start)
        elif method == "concurrent_queue":
            results[method] = bfs.parallel_bfs_concurrent_queue(start)
        elif method == "bag_of_tasks":
            results[method] = bfs.parallel_bfs_bag_of_tasks(start)

    return results


def calculate_speedup(seq_time: float, parallel_time: float) -> float:
    """Calculate speedup factor"""
    return seq_time / parallel_time if parallel_time > 0 else 0


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("PARALLEL BREADTH-FIRST SEARCH (BFS)")
    print("=" * 80)

    # Test with different graph sizes
    sizes = [(1000, 5), (5000, 10), (10000, 15)]

    for num_vertices, edges_per_vertex in sizes:
        print(f"\n{'='*80}")
        print(f"Testing with {num_vertices:,} vertices, ~{edges_per_vertex} edges per vertex")
        print(f"{'='*80}")

        # Create random graph
        graph = create_random_graph(num_vertices, edges_per_vertex)
        print(f"Graph: {graph.num_vertices:,} vertices, ~{graph.num_edges():,} edges")

        # Benchmark all methods
        results = benchmark_all_methods(graph, start=0)

        print(f"\n{'Method':<20} {'Time (s)':<12} {'Vertices':<12} {'Speedup':<10}")
        print("-" * 80)

        seq_time = results.get("sequential").time_taken if "sequential" in results else 0

        for method, result in results.items():
            speedup = calculate_speedup(seq_time, result.time_taken)

            print(f"{method:<20} {result.time_taken:>10.6f}  "
                  f"{result.vertices_processed:>10,}  "
                  f"{speedup:>8.2f}x")

    print(f"\n{'='*80}")
    print("WHEN TO USE PARALLEL BFS")
    print(f"{'='*80}")
    print("""
Parallel BFS is beneficial when:

✓ Large graphs (>10,000 vertices)
✓ High branching factor (many neighbors per vertex)
✓ Multiple CPU cores available
✓ Graph fits in memory

Key strategies:
1. Level-synchronous: Best for correctness, maintains BFS order
2. Concurrent queue: Good balance of performance and simplicity
3. Bag-of-tasks: Best load balancing for irregular graphs

Performance characteristics:
- Speedup limited by graph diameter (sequential depth)
- Best for "wide" graphs (high branching factor)
- Worse for "deep" graphs (low branching factor)
- Synchronization overhead for small graphs

Challenges:
- Thread contention on visited set
- Load imbalance for irregular graphs
- Memory bandwidth limitations
- Synchronization overhead

Best practices:
1. Use level-synchronous for exact BFS ordering
2. Use concurrent queue for better load balance
3. Optimize visited set (lock-free data structures)
4. Consider graph partitioning for very large graphs
5. Profile to identify bottlenecks

Applications:
- Social network analysis
- Web crawling
- Network routing
- Shortest path finding
- Connected components
    """)

    print("\nDemonstration complete!")
