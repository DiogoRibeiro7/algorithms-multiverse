"""
MST Algorithms Benchmark Suite
================================

Comprehensive benchmarking of MST algorithms across:
- Different graph sizes
- Different graph densities
- Different graph types (random, complete, sparse, grid)
- Performance metrics collection
- Statistical analysis

Usage:
    python mst_benchmark.py --graphs all --runs 100 --output results.json
"""

import time
import json
import argparse
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Any, List, Tuple, Dict
from mst_algorithms import MSTAlgorithms
import pandas as pd


class GraphGenerator:
    """
    Generate synthetic graphs used by the MST benchmark harness.

    All helpers are deterministic only with respect to the numpy PRNG seed.
    The helpers return edge lists that can be directly consumed by
    ``MSTAlgorithms`` without additional normalization.
    """

    @staticmethod
    def random_graph(n: int, edge_probability: float, min_weight: float = 1, max_weight: float = 100) -> List[Tuple[int, int, float]]:
        """
        Generate an Erdős–Rényi random graph with weighted edges.

        Args:
            n (int): Number of vertices to create.
            edge_probability (float): Independent probability of including each undirected edge.
            min_weight (float): Minimum inclusive edge weight sampled from a uniform distribution.
            max_weight (float): Maximum inclusive edge weight sampled from a uniform distribution.

        Returns:
            list[tuple[int, int, float]]: Edge tuples in ``(u, v, weight)`` form.

        Side Effects:
            Relies on the global numpy RNG; set ``np.random.seed`` externally for reproducibility.

        Complexity:
            O(n²) to sample every potential edge.

        Examples:
            >>> edges = GraphGenerator.random_graph(4, edge_probability=0.5, min_weight=1, max_weight=3)
            >>> len(edges) <= 6
            True
        """
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if np.random.random() < edge_probability:
                    weight = np.random.uniform(min_weight, max_weight)
                    edges.append((i, j, weight))
        return edges

    @staticmethod
    def complete_graph(n: int, min_weight: float = 1, max_weight: float = 100) -> List[Tuple[int, int, float]]:
        """
        Generate a fully connected undirected graph with weighted edges.

        Args:
            n (int): Number of vertices.
            min_weight (float): Minimum edge weight for the sampling distribution.
            max_weight (float): Maximum edge weight for the sampling distribution.

        Returns:
            list[tuple[int, int, float]]: Edge list covering every ``(u, v)`` pair.

        Side Effects:
            Relies on numpy's RNG for weight sampling.

        Complexity:
            O(n²) due to the dense edge construction.

        Examples:
            >>> edges = GraphGenerator.complete_graph(3)
            >>> len(edges)
            3
        """
        return GraphGenerator.random_graph(n, 1.0, min_weight, max_weight)

    @staticmethod
    def sparse_graph(n: int, edges_per_vertex: int = 3) -> List[Tuple[int, int, float]]:
        """
        Generate a sparse graph that approximates the requested degree.

        Args:
            n (int): Number of vertices.
            edges_per_vertex (int): Target average degree (undirected count).

        Returns:
            list[tuple[int, int, float]]: Edge list representing the sampled sparse graph.

        Side Effects:
            Relies on numpy's RNG for edge/weight sampling.

        Complexity:
            O(n * edges_per_vertex). Uses Erdős–Rényi sampling to approximate the target degree.
        """
        num_edges = n * edges_per_vertex // 2
        edge_probability = num_edges / (n * (n - 1) / 2)
        return GraphGenerator.random_graph(n, edge_probability)

    @staticmethod
    def grid_graph(rows: int, cols: int) -> List[Tuple[int, int, float]]:
        """
        Generate a 2D lattice graph with random weights on the orthogonal edges.

        Args:
            rows (int): Number of rows in the lattice.
            cols (int): Number of columns in the lattice.

        Returns:
            list[tuple[int, int, float]]: Edge list covering horizontal/vertical neighbors.

        Side Effects:
            Draws uniformly random weights via numpy for each edge.

        Complexity:
            O(rows * cols) because each vertex is visited once.

        Examples:
            >>> edges = GraphGenerator.grid_graph(2, 2)
            >>> len(edges)  # 2 horizontal + 2 vertical edges in a 2x2 lattice
            4
        """
        edges = []
        n = rows * cols

        def to_index(r, c):
            """Map lattice coordinates to an absolute vertex index."""
            return r * cols + c

        for r in range(rows):
            for c in range(cols):
                i = to_index(r, c)

                # Right neighbor
                if c + 1 < cols:
                    j = to_index(r, c + 1)
                    weight = np.random.uniform(1, 100)
                    edges.append((i, j, weight))

                # Bottom neighbor
                if r + 1 < rows:
                    j = to_index(r + 1, c)
                    weight = np.random.uniform(1, 100)
                    edges.append((i, j, weight))

        return edges

    @staticmethod
    def weighted_cycle(n: int) -> List[Tuple[int, int, float]]:
        """
        Generate a simple cycle graph with random edge weights.

        Args:
            n (int): Number of vertices.

        Returns:
            list[tuple[int, int, float]]: Edges describing a ring topology.

        Side Effects:
            Samples weights with numpy's RNG.

        Complexity:
            O(n) because exactly one edge per vertex is emitted.

        Examples:
            >>> edges = GraphGenerator.weighted_cycle(4)
            >>> len(edges)
            4
        """
        edges = []
        for i in range(n):
            j = (i + 1) % n
            weight = np.random.uniform(1, 100)
            edges.append((i, j, weight))
        return edges


class MSTBenchmark:
    """
    Benchmark suite for evaluating MST implementations under different workloads.

    The class keeps an in-memory list of benchmark results so that multiple
    scenarios can be analyzed before serializing or visualizing the outcome.
    """

    def __init__(self) -> None:
        """Initialize the benchmark runner with an empty results buffer."""
        self.results: List[Dict[str, Any]] = []

    def benchmark_algorithm(self, algorithm: str, mst: MSTAlgorithms, num_runs: int = 10) -> Dict[str, float]:
        """
        Run a specific MST algorithm repeatedly and capture descriptive stats.

        Args:
            algorithm (str): Algorithm name (`'kruskal'`, `'prim'`, or `'boruvka'`).
            mst (MSTAlgorithms): Pre-built MST problem instance.
            num_runs (int): Number of timed iterations to execute.

        Returns:
            dict: Aggregate statistics (mean, std, percentiles) computed from the runs.

        Raises:
            ValueError: If an unsupported algorithm name is provided.

        Complexity:
            O(num_runs * (V log V + E)) assuming typical priority-queue based MST implementations.
        """
        times = []

        for _ in range(num_runs):
            start = time.perf_counter()

            if algorithm == 'kruskal':
                mst.kruskal()
            elif algorithm == 'prim':
                mst.prim()
            elif algorithm == 'boruvka':
                mst.boruvka()
            else:
                raise ValueError(f"Unknown algorithm: {algorithm}")

            elapsed = (time.perf_counter() - start) * 1000  # Convert to ms
            times.append(elapsed)

        return {
            'mean': np.mean(times),
            'std': np.std(times),
            'min': np.min(times),
            'max': np.max(times),
            'median': np.median(times),
            'p95': np.percentile(times, 95),
            'p99': np.percentile(times, 99)
        }

    def run_benchmark(self, graph_type: str, num_vertices: int, num_runs: int = 10, **kwargs) -> Dict[str, Any] | None:
        """
        Generate a graph of the requested type and benchmark every MST variant.

        Args:
            graph_type (str): One of ``random``, ``complete``, ``sparse``, or ``grid``.
            num_vertices (int): Desired vertex count; grid graphs are snapped to a square.
            num_runs (int): Number of timing iterations for each MST algorithm.
            **kwargs: Generator-specific overrides such as ``edge_probability``.

        Returns:
            dict | None: Benchmark payload appended to ``self.results`` or ``None`` if no edges exist.

        Raises:
        ValueError: When an unsupported ``graph_type`` is provided.

        Side Effects:
            Prints progress to stdout, mutates ``self.results``, and uses numpy's RNG during graph generation.

        Examples:
            >>> benchmark = MSTBenchmark()
            >>> _ = benchmark.run_benchmark('random', 6, num_runs=1, edge_probability=0.4)
            >>> len(benchmark.results) >= 1
            True
        """
        print(f"Benchmarking {graph_type} graph with {num_vertices} vertices...")

        # Generate graph
        if graph_type == 'random':
            edges = GraphGenerator.random_graph(num_vertices, kwargs.get('edge_probability', 0.1))
        elif graph_type == 'complete':
            edges = GraphGenerator.complete_graph(num_vertices)
        elif graph_type == 'sparse':
            edges = GraphGenerator.sparse_graph(num_vertices, kwargs.get('edges_per_vertex', 3))
        elif graph_type == 'grid':
            # Force the grid to be square so MSTAlgorithms receives a consistent vertex count.
            size = int(np.sqrt(num_vertices))
            edges = GraphGenerator.grid_graph(size, size)
            num_vertices = size * size  # Adjust to actual size
        else:
            raise ValueError(f"Unknown graph type: {graph_type}")

        if not edges:
            print(f"  Warning: No edges generated for {graph_type} graph")
            return None

        mst = MSTAlgorithms(num_vertices, edges)

        # Benchmark each algorithm
        result = {
            'graph_type': graph_type,
            'num_vertices': num_vertices,
            'num_edges': len(edges),
            'density': len(edges) / (num_vertices * (num_vertices - 1) / 2),
            'algorithms': {}
        }

        for algo in ['kruskal', 'prim', 'boruvka']:
            try:
                stats = self.benchmark_algorithm(algo, mst, num_runs)
                result['algorithms'][algo] = stats
                print(f"  {algo}: {stats['mean']:.4f} ms (±{stats['std']:.4f})")
            except Exception as e:
                print(f"  {algo}: ERROR - {e}")
                result['algorithms'][algo] = None

        self.results.append(result)
        return result

    def run_comprehensive_benchmark(self, num_runs: int = 10) -> None:
        """
        Execute a curated suite of graph configurations for regression tracking.

        Args:
            num_runs (int): Number of timing iterations per MST algorithm.

        Side Effects:
            Prints a textual progress report and extends ``self.results``.
        """
        print("=" * 80)
        print("MST ALGORITHMS COMPREHENSIVE BENCHMARK")
        print("=" * 80)
        print()

        # Test configurations
        configs = [
            # Sparse graphs
            {'graph_type': 'sparse', 'num_vertices': 100, 'edges_per_vertex': 3},
            {'graph_type': 'sparse', 'num_vertices': 500, 'edges_per_vertex': 3},
            {'graph_type': 'sparse', 'num_vertices': 1000, 'edges_per_vertex': 3},

            # Dense graphs
            {'graph_type': 'random', 'num_vertices': 100, 'edge_probability': 0.5},
            {'graph_type': 'random', 'num_vertices': 200, 'edge_probability': 0.5},

            # Very sparse (tree-like)
            {'graph_type': 'sparse', 'num_vertices': 500, 'edges_per_vertex': 2},
            {'graph_type': 'sparse', 'num_vertices': 1000, 'edges_per_vertex': 2},

            # Grid graphs
            {'graph_type': 'grid', 'num_vertices': 100},
            {'graph_type': 'grid', 'num_vertices': 400},

            # Complete graphs (small only - very expensive!)
            {'graph_type': 'complete', 'num_vertices': 50},
            {'graph_type': 'complete', 'num_vertices': 100},
        ]

        for config in configs:
            self.run_benchmark(**config, num_runs=num_runs)
            print()

    def analyze_results(self) -> pd.DataFrame | None:
        """
        Convert accumulated benchmark runs into a pandas DataFrame for inspection.

        Returns:
            pandas.DataFrame | None: Flattened dataset or ``None`` if there are no results yet.

        Side Effects:
            Prints a detailed human-readable analysis (fastest by type, scalability, densities).

        Examples:
            >>> benchmark = MSTBenchmark()
            >>> _ = benchmark.run_benchmark('sparse', 5, num_runs=1, edges_per_vertex=2)
            >>> df = benchmark.analyze_results()
            >>> list(df.columns)
            ['graph_type', 'num_vertices', 'num_edges', 'density', 'algorithm', 'mean', 'std', 'min', 'max', 'median', 'p95', 'p99']
        """
        if not self.results:
            print("No results to analyze!")
            return

        print("=" * 80)
        print("BENCHMARK ANALYSIS")
        print("=" * 80)
        print()

        # Convert to DataFrame for easier analysis
        rows = []
        for result in self.results:
            for algo, stats in result['algorithms'].items():
                if stats:
                    rows.append({
                        'graph_type': result['graph_type'],
                        'num_vertices': result['num_vertices'],
                        'num_edges': result['num_edges'],
                        'density': result['density'],
                        'algorithm': algo,
                        **stats
                    })

        df = pd.DataFrame(rows)

        # 1. Winner by graph type
        print("1. FASTEST ALGORITHM BY GRAPH TYPE")
        print("-" * 80)
        for graph_type in df['graph_type'].unique():
            subset = df[df['graph_type'] == graph_type]
            fastest = subset.loc[subset['mean'].idxmin()]
            print(f"{graph_type:15s}: {fastest['algorithm']:10s} "
                  f"({fastest['mean']:.4f} ms)")
        print()

        # 2. Scalability analysis
        print("2. SCALABILITY ANALYSIS (Time vs Graph Size)")
        print("-" * 80)
        for algo in ['kruskal', 'prim', 'boruvka']:
            algo_df = df[df['algorithm'] == algo].sort_values('num_vertices')
            if len(algo_df) > 1:
                print(f"\n{algo}:")
                for _, row in algo_df.iterrows():
                    print(f"  V={row['num_vertices']:4d}, E={row['num_edges']:5d}: "
                          f"{row['mean']:8.4f} ms")
        print()

        # 3. Density analysis
        print("3. PERFORMANCE VS GRAPH DENSITY")
        print("-" * 80)
        density_bins = [(0, 0.1, 'Very Sparse'), (0.1, 0.3, 'Sparse'),
                        (0.3, 0.7, 'Medium'), (0.7, 1.0, 'Dense')]

        for low, high, label in density_bins:
            subset = df[(df['density'] >= low) & (df['density'] < high)]
            if not subset.empty:
                print(f"\n{label} (density {low:.1f}-{high:.1f}):")
                for algo in ['kruskal', 'prim', 'boruvka']:
                    algo_subset = subset[subset['algorithm'] == algo]
                    if not algo_subset.empty:
                        mean_time = algo_subset['mean'].mean()
                        print(f"  {algo:10s}: {mean_time:.4f} ms (avg)")
        print()

        return df

    def visualize_results(self, df: pd.DataFrame, save_path: str = 'mst_benchmark_results.png') -> None:
        """
        Plot summary charts for the provided benchmark DataFrame.

        Args:
            df (pandas.DataFrame): Flattened timing statistics from ``analyze_results``.
            save_path (str): Destination path for the exported PNG.

        Side Effects:
            Writes a PNG to disk and opens the Matplotlib window via ``plt.show``.
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('MST Algorithms Benchmark Results', fontsize=16, fontweight='bold')

        # 1. Performance by graph size (line plot)
        ax1 = axes[0, 0]
        for algo in ['kruskal', 'prim', 'boruvka']:
            algo_df = df[df['algorithm'] == algo].sort_values('num_vertices')
            ax1.plot(algo_df['num_vertices'], algo_df['mean'],
                    marker='o', label=algo, linewidth=2)
        ax1.set_xlabel('Number of Vertices')
        ax1.set_ylabel('Mean Time (ms)')
        ax1.set_title('Performance vs Graph Size')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. Performance by density (scatter)
        ax2 = axes[0, 1]
        for algo in ['kruskal', 'prim', 'boruvka']:
            algo_df = df[df['algorithm'] == algo]
            ax2.scatter(algo_df['density'], algo_df['mean'],
                       label=algo, alpha=0.6, s=100)
        ax2.set_xlabel('Graph Density')
        ax2.set_ylabel('Mean Time (ms)')
        ax2.set_title('Performance vs Graph Density')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # 3. Box plots by algorithm
        ax3 = axes[1, 0]
        data = [df[df['algorithm'] == algo]['mean'].values
                for algo in ['kruskal', 'prim', 'boruvka']]
        ax3.boxplot(data, labels=['Kruskal', 'Prim', 'Boruvka'])
        ax3.set_ylabel('Mean Time (ms)')
        ax3.set_title('Time Distribution by Algorithm')
        ax3.grid(True, alpha=0.3, axis='y')

        # 4. Heatmap of winner by graph type and size
        ax4 = axes[1, 1]
        pivot = df.pivot_table(values='mean', index='graph_type',
                              columns='algorithm', aggfunc='mean')
        sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn_r',
                   ax=ax4, cbar_kws={'label': 'Mean Time (ms)'})
        ax4.set_title('Average Performance by Graph Type')

        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\nVisualization saved to {save_path}")
        plt.show()

    def save_results(self, filename: str = 'mst_benchmark_results.json') -> None:
        """
        Serialize collected benchmark results to disk.

        Args:
            filename (str): Target JSON file path.

        Side Effects:
            Writes the JSON file and prints a confirmation message.
        """
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Results saved to {filename}")


def main() -> None:
    """
    Parse CLI arguments and run the requested MST benchmark workflow.

    Side Effects:
        Prints progress to stdout, writes JSON/PNG files, and may launch Matplotlib windows.
    """
    parser = argparse.ArgumentParser(description='MST Algorithms Benchmark Suite')
    parser.add_argument('--graphs', type=str, default='all',
                       help='Graph types to benchmark (all, sparse, dense, grid)')
    parser.add_argument('--runs', type=int, default=10,
                       help='Number of runs per benchmark')
    parser.add_argument('--output', type=str, default='mst_benchmark_results.json',
                       help='Output JSON file')
    parser.add_argument('--visualize', action='store_true',
                       help='Generate visualization')

    args = parser.parse_args()

    benchmark = MSTBenchmark()

    if args.graphs == 'all':
        benchmark.run_comprehensive_benchmark(num_runs=args.runs)
    else:
        # Run specific graph types
        for graph_type in args.graphs.split(','):
            benchmark.run_benchmark(graph_type.strip(), 500, num_runs=args.runs)

    # Analyze and visualize
    df = benchmark.analyze_results()

    if args.visualize and df is not None:
        benchmark.visualize_results(df)

    benchmark.save_results(args.output)


if __name__ == "__main__":
    # For direct execution without args
    import sys

    if len(sys.argv) == 1:
        # Run default comprehensive benchmark
        benchmark = MSTBenchmark()
        benchmark.run_comprehensive_benchmark(num_runs=10)
        df = benchmark.analyze_results()
        if df is not None:
            benchmark.visualize_results(df)
        benchmark.save_results()
    else:
        main()
