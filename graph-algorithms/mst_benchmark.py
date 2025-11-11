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
from typing import List, Tuple, Dict
from mst_algorithms import MSTAlgorithms
import pandas as pd


class GraphGenerator:
    """Generate different types of graphs for benchmarking"""

    @staticmethod
    def random_graph(n: int, edge_probability: float, min_weight: float = 1, max_weight: float = 100) -> List[Tuple[int, int, float]]:
        """
        Generate random graph with given edge probability

        Args:
            n: Number of vertices
            edge_probability: Probability of edge between any two vertices
            min_weight: Minimum edge weight
            max_weight: Maximum edge weight

        Returns:
            List of edges
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
        """Generate complete graph (all possible edges)"""
        return GraphGenerator.random_graph(n, 1.0, min_weight, max_weight)

    @staticmethod
    def sparse_graph(n: int, edges_per_vertex: int = 3) -> List[Tuple[int, int, float]]:
        """Generate sparse graph with approximately edges_per_vertex edges per vertex"""
        num_edges = n * edges_per_vertex // 2
        edge_probability = num_edges / (n * (n - 1) / 2)
        return GraphGenerator.random_graph(n, edge_probability)

    @staticmethod
    def grid_graph(rows: int, cols: int) -> List[Tuple[int, int, float]]:
        """Generate 2D grid graph"""
        edges = []
        n = rows * cols

        def to_index(r, c):
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
        """Generate cycle graph"""
        edges = []
        for i in range(n):
            j = (i + 1) % n
            weight = np.random.uniform(1, 100)
            edges.append((i, j, weight))
        return edges


class MSTBenchmark:
    """Benchmark suite for MST algorithms"""

    def __init__(self):
        self.results = []

    def benchmark_algorithm(self, algorithm: str, mst: MSTAlgorithms, num_runs: int = 10) -> Dict:
        """
        Benchmark a single algorithm

        Args:
            algorithm: 'kruskal', 'prim', or 'boruvka'
            mst: MSTAlgorithms instance
            num_runs: Number of times to run the algorithm

        Returns:
            Dictionary with timing statistics
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

    def run_benchmark(self, graph_type: str, num_vertices: int, num_runs: int = 10, **kwargs) -> Dict:
        """
        Run benchmark on a specific graph type and size

        Args:
            graph_type: Type of graph to generate
            num_vertices: Number of vertices
            num_runs: Number of times to run each algorithm
            **kwargs: Additional arguments for graph generation

        Returns:
            Dictionary with benchmark results
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

    def run_comprehensive_benchmark(self, num_runs: int = 10):
        """Run comprehensive benchmark across different graph types and sizes"""
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

    def analyze_results(self):
        """Analyze benchmark results and generate insights"""
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

    def visualize_results(self, df: pd.DataFrame, save_path: str = 'mst_benchmark_results.png'):
        """Create visualization of benchmark results"""
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

    def save_results(self, filename: str = 'mst_benchmark_results.json'):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Results saved to {filename}")


def main():
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
