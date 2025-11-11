"""
Python Benchmark Runner
Runs graph algorithm benchmarks and outputs results in JSON format
"""

import time
import json
import sys
import statistics
from typing import Dict, List, Any, Optional
from graph import Graph, GraphType, GraphGenerator
from graph_advanced import AdvancedGraph

def generate_graph(config: Dict[str, Any]) -> Graph:
    """Generate a graph based on configuration"""
    vertices = config['vertices']
    graph_type = GraphType.DIRECTED if config.get('directed', False) else GraphType.UNDIRECTED
    weighted = config.get('weighted', False)

    if config['type'] == 'random':
        return GraphGenerator.random_graph(vertices, config['density'], graph_type, weighted)
    elif config['type'] == 'dag':
        return GraphGenerator.dag(vertices, config.get('edge_probability', 0.1), weighted)
    else:
        raise ValueError(f"Unknown graph type: {config['type']}")

def run_algorithm(graph: Graph, algorithm: str, params: Dict[str, Any]) -> Optional[Any]:
    """Run a specific algorithm on the graph"""
    try:
        if algorithm == 'dfs_iterative':
            start = params.get('start_vertex', 0)
            return graph.dfs_iterative(start)
        elif algorithm == 'dfs_recursive':
            start = params.get('start_vertex', 0)
            return graph.dfs_recursive(start)
        elif algorithm == 'bfs':
            start = params.get('start_vertex', 0)
            return graph.bfs(start)
        elif algorithm == 'topological_sort':
            return graph.topological_sort()
        elif algorithm == 'connected_components':
            return graph.find_connected_components()
        elif algorithm == 'has_cycle':
            return graph.has_cycle()
        elif algorithm == 'dijkstra':
            if not isinstance(graph, AdvancedGraph):
                graph = AdvancedGraph.from_graph(graph)
            start = params.get('start_vertex', 0)
            return graph.dijkstra(start)
        elif algorithm == 'prim_mst':
            if not isinstance(graph, AdvancedGraph):
                graph = AdvancedGraph.from_graph(graph)
            start = params.get('start_vertex', 0)
            return graph.prim_mst(start)
        elif algorithm == 'kruskal_mst':
            if not isinstance(graph, AdvancedGraph):
                graph = AdvancedGraph.from_graph(graph)
            return graph.kruskal_mst()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    except Exception as e:
        print(f"Error running algorithm {algorithm}: {e}", file=sys.stderr)
        return None

def benchmark_algorithm(benchmark_config: Dict[str, Any]) -> Dict[str, Any]:
    """Run a single benchmark and return timing statistics"""
    print(f"Running benchmark: {benchmark_config['name']}")

    # Generate graph once
    graph = generate_graph(benchmark_config['graph'])

    algorithm = benchmark_config['algorithm']
    trials = benchmark_config.get('trials', 10)

    # Prepare parameters
    params = {}
    if 'start_vertex' in benchmark_config:
        params['start_vertex'] = benchmark_config['start_vertex']

    times = []
    success_count = 0

    # Run multiple trials
    for trial in range(trials):
        start_time = time.perf_counter()
        result = run_algorithm(graph, algorithm, params)
        end_time = time.perf_counter()

        if result is not None:
            elapsed = end_time - start_time
            times.append(elapsed)
            success_count += 1

    if not times:
        return {
            'name': benchmark_config['name'],
            'language': 'Python',
            'status': 'failed',
            'error': 'All trials failed'
        }

    # Compute statistics
    return {
        'name': benchmark_config['name'],
        'description': benchmark_config.get('description', ''),
        'language': 'Python',
        'algorithm': algorithm,
        'graph': {
            'vertices': benchmark_config['graph']['vertices'],
            'type': benchmark_config['graph']['type'],
            'density': benchmark_config['graph'].get('density', 'N/A'),
            'directed': benchmark_config['graph'].get('directed', False),
            'weighted': benchmark_config['graph'].get('weighted', False)
        },
        'trials': trials,
        'successful_trials': success_count,
        'status': 'success',
        'timing': {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times),
            'times': times
        }
    }

def main():
    """Main benchmark runner"""
    # Load benchmark configuration
    config_file = 'benchmark_config.json'

    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing configuration file: {e}", file=sys.stderr)
        sys.exit(1)

    print("=" * 80)
    print("Python Graph Algorithms Benchmark")
    print("=" * 80)
    print()

    benchmarks = config.get('benchmarks', [])
    results = []

    for benchmark_config in benchmarks:
        try:
            result = benchmark_algorithm(benchmark_config)
            results.append(result)

            if result['status'] == 'success':
                timing = result['timing']
                print(f"  Mean: {timing['mean']*1000:.3f} ms")
                print(f"  Std Dev: {timing['std_dev']*1000:.3f} ms")
                print(f"  Min: {timing['min']*1000:.3f} ms")
                print(f"  Max: {timing['max']*1000:.3f} ms")
            else:
                print(f"  Status: {result['status']}")
                if 'error' in result:
                    print(f"  Error: {result['error']}")
            print()
        except Exception as e:
            print(f"  Error: {e}")
            print()
            results.append({
                'name': benchmark_config['name'],
                'language': 'Python',
                'status': 'error',
                'error': str(e)
            })

    # Save results
    output_file = 'results_python.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print("=" * 80)
    print(f"Results saved to {output_file}")
    print("=" * 80)

if __name__ == '__main__':
    main()
