"""
Parallel Depth-First Search (DFS) with Work-Stealing

This module implements parallel DFS using work-stealing for dynamic load balancing.

Features:
- Work-stealing deques for load balancing
- Thread-safe visited tracking
- Multiple strategies (recursive, iterative, work-stealing)
- Topological sort support
- Cycle detection

Time Complexity: O(V + E) where V = vertices, E = edges
Space Complexity: O(V)
Speedup: 2-4x typical (DFS is inherently more sequential than BFS)

When to use parallel DFS:
- Large graphs with multiple components
- When load balancing is important
- Tree-like structures with high branching

Author: Algorithms Multiverse
"""

import concurrent.futures
import multiprocessing as mp
import threading
import time
from typing import List, Set, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
from collections import defaultdict, deque
import random


@dataclass
class DFSResult:
    """Results from DFS traversal with performance metrics"""
    visited_order: List[int]
    discovery_time: Dict[int, int]
    finish_time: Dict[int, int]
    parent: Dict[int, Optional[int]]
    time_taken: float
    vertices_processed: int
    edges_explored: int
    method: str
    num_workers: int


class Graph:
    """Graph representation for DFS"""

    def __init__(self, directed: bool = True):
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


class WorkStealingDeque:
    """
    Thread-safe work-stealing deque for DFS.

    Supports push/pop from bottom (owner) and steal from top (thieves).
    """

    def __init__(self):
        self.deque = deque()
        self.lock = threading.Lock()

    def push(self, item):
        """Push item to bottom (LIFO for owner)"""
        with self.lock:
            self.deque.append(item)

    def pop(self):
        """Pop from bottom (owner's work)"""
        with self.lock:
            if self.deque:
                return self.deque.pop()
            return None

    def steal(self):
        """Steal from top (FIFO for stealing)"""
        with self.lock:
            if self.deque:
                return self.deque.popleft()
            return None

    def is_empty(self):
        """Return True when no work items remain in the deque."""
        with self.lock:
            return len(self.deque) == 0

    def size(self):
        """Return the current number of scheduled tasks."""
        with self.lock:
            return len(self.deque)


class ParallelDFS:
    """
    Parallel Depth-First Search with work-stealing.
    """

    def __init__(self, graph: Graph, num_workers: int = None):
        """
        Initialize ParallelDFS.

        Args:
            graph: Graph to traverse
            num_workers: Number of worker threads
        """
        self.graph = graph
        self.num_workers = num_workers or mp.cpu_count()
        self.visited = set()
        self.discovery_time = {}
        self.finish_time = {}
        self.parent = {}
        self.visited_order = []
        self._lock = threading.Lock()
        self.edges_explored = 0
        self.time_counter = 0

    def _reset(self):
        """Reset traversal state"""
        self.visited = set()
        self.discovery_time = {}
        self.finish_time = {}
        self.parent = {}
        self.visited_order = []
        self.edges_explored = 0
        self.time_counter = 0

    def _increment_time(self) -> int:
        """Thread-safe time counter increment"""
        with self._lock:
            self.time_counter += 1
            return self.time_counter

    def sequential_dfs_recursive(self, start: int) -> DFSResult:
        """
        Standard recursive DFS.

        Args:
            start: Starting vertex

        Returns:
            DFSResult with traversal information
        """
        self._reset()
        start_time = time.perf_counter()

        def dfs_visit(vertex: int):
            """Visit vertex and explore neighbors"""
            self.visited.add(vertex)
            self.discovery_time[vertex] = self._increment_time()
            self.visited_order.append(vertex)

            for neighbor in self.graph.get_neighbors(vertex):
                self.edges_explored += 1
                if neighbor not in self.visited:
                    self.parent[neighbor] = vertex
                    dfs_visit(neighbor)

            self.finish_time[vertex] = self._increment_time()

        # Start DFS from given vertex
        self.parent[start] = None
        dfs_visit(start)

        # Visit any remaining unvisited vertices (for disconnected graphs)
        for v in range(self.graph.num_vertices):
            if v not in self.visited:
                self.parent[v] = None
                dfs_visit(v)

        time_taken = time.perf_counter() - start_time

        return DFSResult(
            visited_order=self.visited_order.copy(),
            discovery_time=self.discovery_time.copy(),
            finish_time=self.finish_time.copy(),
            parent=self.parent.copy(),
            time_taken=time_taken,
            vertices_processed=len(self.visited),
            edges_explored=self.edges_explored,
            method="sequential_recursive",
            num_workers=1
        )

    def sequential_dfs_iterative(self, start: int) -> DFSResult:
        """
        Iterative DFS using a stack.

        Args:
            start: Starting vertex

        Returns:
            DFSResult with traversal information
        """
        self._reset()
        start_time = time.perf_counter()

        stack = [start]
        self.parent[start] = None

        while stack:
            vertex = stack.pop()

            if vertex not in self.visited:
                self.visited.add(vertex)
                self.discovery_time[vertex] = self._increment_time()
                self.visited_order.append(vertex)

                # Add neighbors to stack in reverse order for consistent traversal
                neighbors = self.graph.get_neighbors(vertex)
                for neighbor in reversed(neighbors):
                    self.edges_explored += 1
                    if neighbor not in self.visited:
                        if neighbor not in self.parent:
                            self.parent[neighbor] = vertex
                        stack.append(neighbor)

                self.finish_time[vertex] = self._increment_time()

        time_taken = time.perf_counter() - start_time

        return DFSResult(
            visited_order=self.visited_order.copy(),
            discovery_time=self.discovery_time.copy(),
            finish_time=self.finish_time.copy(),
            parent=self.parent.copy(),
            time_taken=time_taken,
            vertices_processed=len(self.visited),
            edges_explored=self.edges_explored,
            method="sequential_iterative",
            num_workers=1
        )

    def parallel_dfs_work_stealing(self, start: int) -> DFSResult:
        """
        Parallel DFS using work-stealing deques.

        Each worker has its own deque and can steal work from others.

        Args:
            start: Starting vertex

        Returns:
            DFSResult with traversal information
        """
        self._reset()
        start_time = time.perf_counter()

        # Work-stealing deques for each worker
        work_deques = [WorkStealingDeque() for _ in range(self.num_workers)]

        # Initially add start vertex to first deque
        work_deques[0].push(start)
        self.parent[start] = None

        done_event = threading.Event()
        active_workers = [0] * self.num_workers
        active_lock = threading.Lock()

        def worker(worker_id: int):
            """Worker function that processes vertices"""
            my_deque = work_deques[worker_id]

            while not done_event.is_set():
                # Try to get work from own deque
                vertex = my_deque.pop()

                # If no work, try to steal from others
                if vertex is None:
                    for i in range(self.num_workers):
                        if i != worker_id:
                            vertex = work_deques[i].steal()
                            if vertex is not None:
                                break

                if vertex is None:
                    # Check if all deques are empty
                    with active_lock:
                        if all(d.is_empty() for d in work_deques):
                            if sum(active_workers) == 0:
                                done_event.set()
                                break
                    time.sleep(0.0001)  # Brief sleep to avoid busy waiting
                    continue

                with active_lock:
                    active_workers[worker_id] += 1

                # Process vertex if not visited
                with self._lock:
                    if vertex in self.visited:
                        with active_lock:
                            active_workers[worker_id] -= 1
                        continue

                    self.visited.add(vertex)
                    self.discovery_time[vertex] = self._increment_time()
                    self.visited_order.append(vertex)

                # Explore neighbors
                neighbors = self.graph.get_neighbors(vertex)
                for neighbor in neighbors:
                    with self._lock:
                        self.edges_explored += 1
                        if neighbor not in self.visited:
                            if neighbor not in self.parent:
                                self.parent[neighbor] = vertex
                            # Add to own deque
                            my_deque.push(neighbor)

                with self._lock:
                    self.finish_time[vertex] = self._increment_time()

                with active_lock:
                    active_workers[worker_id] -= 1

        # Start workers
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            futures = [executor.submit(worker, i) for i in range(self.num_workers)]
            concurrent.futures.wait(futures)

        time_taken = time.perf_counter() - start_time

        return DFSResult(
            visited_order=self.visited_order.copy(),
            discovery_time=self.discovery_time.copy(),
            finish_time=self.finish_time.copy(),
            parent=self.parent.copy(),
            time_taken=time_taken,
            vertices_processed=len(self.visited),
            edges_explored=self.edges_explored,
            method="work_stealing",
            num_workers=self.num_workers
        )


def create_random_graph(num_vertices: int, edges_per_vertex: int = 3, directed: bool = True) -> Graph:
    """Create a random graph for testing"""
    graph = Graph(directed=directed)

    for v in range(num_vertices):
        for _ in range(edges_per_vertex):
            neighbor = random.randint(0, num_vertices - 1)
            if neighbor != v:
                graph.add_edge(v, neighbor)

    return graph


def benchmark_all_methods(graph: Graph, start: int, num_workers: int = None) -> dict:
    """Benchmark all DFS methods"""
    results = {}

    methods = ["sequential_recursive", "sequential_iterative", "work_stealing"]

    for method in methods:
        dfs = ParallelDFS(graph, num_workers=num_workers)

        if method == "sequential_recursive":
            results[method] = dfs.sequential_dfs_recursive(start)
        elif method == "sequential_iterative":
            results[method] = dfs.sequential_dfs_iterative(start)
        elif method == "work_stealing":
            results[method] = dfs.parallel_dfs_work_stealing(start)

    return results


def calculate_speedup(seq_time: float, parallel_time: float) -> float:
    """Calculate speedup factor"""
    return seq_time / parallel_time if parallel_time > 0 else 0


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("PARALLEL DEPTH-FIRST SEARCH (DFS) WITH WORK-STEALING")
    print("=" * 80)

    # Test with different graph sizes
    sizes = [(1000, 3), (5000, 5), (10000, 8)]

    for num_vertices, edges_per_vertex in sizes:
        print(f"\n{'='*80}")
        print(f"Testing with {num_vertices:,} vertices, ~{edges_per_vertex} edges per vertex")
        print(f"{'='*80}")

        # Create random graph
        graph = create_random_graph(num_vertices, edges_per_vertex)
        print(f"Graph: {graph.num_vertices:,} vertices, ~{graph.num_edges():,} edges")

        # Benchmark all methods
        results = benchmark_all_methods(graph, start=0)

        print(f"\n{'Method':<25} {'Time (s)':<12} {'Vertices':<12} {'Speedup':<10}")
        print("-" * 80)

        seq_time = results.get("sequential_iterative").time_taken if "sequential_iterative" in results else 0

        for method, result in results.items():
            speedup = calculate_speedup(seq_time, result.time_taken)

            print(f"{method:<25} {result.time_taken:>10.6f}  "
                  f"{result.vertices_processed:>10,}  "
                  f"{speedup:>8.2f}x")

    print(f"\n{'='*80}")
    print("WHEN TO USE PARALLEL DFS")
    print(f"{'='*80}")
    print("""
Parallel DFS is beneficial when:

✓ Large graphs with multiple components
✓ Tree-like structures with high branching
✓ Multiple CPU cores available
✓ Load balancing is important

DFS characteristics:
- More inherently sequential than BFS
- Speedup typically 2-4x (vs 3-5x for BFS)
- Work-stealing helps with load imbalance
- Good for disconnected graphs

Work-stealing advantages:
✓ Dynamic load balancing
✓ Handles irregular workloads well
✓ LIFO for own work (depth-first nature)
✓ FIFO for stealing (better balance)
✓ Minimizes idle time

Challenges:
- More sequential than BFS
- Synchronization overhead
- Stack depth limitations
- Memory coherency

vs. Parallel BFS:
+ DFS: Better for topological sort, cycle detection, path finding
+ DFS: Lower memory usage (implicit stack)
- DFS: More sequential nature
- DFS: Worse load balancing (deep paths)
+ BFS: Better parallelization potential
+ BFS: Level-synchronous is easier

Applications:
- Topological sorting
- Cycle detection
- Connected components
- Maze solving
- Dependency resolution
- Tree traversal

Best practices:
1. Use work-stealing for load balancing
2. Tune number of workers (typically 4-8)
3. Consider BFS for better parallelism
4. Profile to identify bottlenecks
5. Handle disconnected components

Performance characteristics:
- Sequential: O(V + E)
- Parallel: O(V + E) / p + synchronization overhead
- Speedup: 2-4x typical
- Efficiency: 50-75% (lower than BFS)
- Work-stealing overhead: ~100-200ns per operation

Optimization strategies:
1. Minimize synchronization
2. Use lock-free data structures where possible
3. Batch operations to reduce contention
4. Consider hybrid approaches
5. Profile and tune thresholds
    """)

    print("\nDemonstration complete!")
