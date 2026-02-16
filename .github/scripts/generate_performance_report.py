#!/usr/bin/env python3
"""
Generate performance reports from benchmark results.
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

def load_benchmark_data(filepath: str) -> Dict[str, Any]:
    """Load benchmark data from JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}", file=sys.stderr)
        return {}

def format_time(nanoseconds: float) -> str:
    """Format time in human-readable format."""
    if nanoseconds < 1000:
        return f"{nanoseconds:.2f}ns"
    elif nanoseconds < 1_000_000:
        return f"{nanoseconds/1000:.2f}μs"
    elif nanoseconds < 1_000_000_000:
        return f"{nanoseconds/1_000_000:.2f}ms"
    else:
        return f"{nanoseconds/1_000_000_000:.2f}s"

def format_memory(bytes_val: int) -> str:
    """Format memory in human-readable format."""
    if bytes_val < 1024:
        return f"{bytes_val}B"
    elif bytes_val < 1024 * 1024:
        return f"{bytes_val/1024:.2f}KB"
    elif bytes_val < 1024 * 1024 * 1024:
        return f"{bytes_val/(1024*1024):.2f}MB"
    else:
        return f"{bytes_val/(1024*1024*1024):.2f}GB"

def analyze_sorting_benchmarks(data: Dict) -> str:
    """Analyze sorting algorithm benchmarks."""
    report = "## Sorting Algorithms\n\n"
    report += "| Algorithm | Dataset Size | Time (avg) | Time (min) | Time (max) | Memory |\n"
    report += "|-----------|--------------|------------|------------|------------|--------|\n"

    # Parse pytest-benchmark format
    if 'benchmarks' in data:
        for bench in data['benchmarks']:
            name = bench.get('name', 'Unknown')
            stats = bench.get('stats', {})

            # Extract algorithm name and dataset size from test name
            parts = name.split('_')
            if len(parts) >= 2:
                algo_name = parts[1]
                size = parts[-1] if parts[-1].isdigit() else "1000"
            else:
                algo_name = name
                size = "Unknown"

            avg_time = format_time(stats.get('mean', 0) * 1e9)
            min_time = format_time(stats.get('min', 0) * 1e9)
            max_time = format_time(stats.get('max', 0) * 1e9)
            memory = format_memory(bench.get('extra_info', {}).get('memory_peak', 0))

            report += f"| {algo_name} | {size} | {avg_time} | {min_time} | {max_time} | {memory} |\n"

    report += "\n### Analysis\n\n"
    report += "- **Best for small datasets**: Insertion Sort (O(n²) but low overhead)\n"
    report += "- **Best average case**: Quick Sort (O(n log n) with good cache locality)\n"
    report += "- **Best worst case**: Merge Sort, Heap Sort (guaranteed O(n log n))\n"
    report += "- **Best for nearly sorted**: Tim Sort (adaptive, O(n) best case)\n\n"

    return report

def analyze_searching_benchmarks(data: Dict) -> str:
    """Analyze searching algorithm benchmarks."""
    report = "## Searching Algorithms\n\n"
    report += "| Algorithm | Dataset Size | Target Position | Time (avg) | Comparisons |\n"
    report += "|-----------|--------------|-----------------|------------|-------------|\n"

    if 'benchmarks' in data:
        for bench in data['benchmarks']:
            name = bench.get('name', 'Unknown')
            stats = bench.get('stats', {})
            extra = bench.get('extra_info', {})

            algo_name = name.split('_')[1] if '_' in name else name
            size = extra.get('dataset_size', 'Unknown')
            position = extra.get('target_position', 'Random')
            avg_time = format_time(stats.get('mean', 0) * 1e9)
            comparisons = extra.get('comparisons', 'N/A')

            report += f"| {algo_name} | {size} | {position} | {avg_time} | {comparisons} |\n"

    report += "\n### Analysis\n\n"
    report += "- **Binary Search**: O(log n) - Best for sorted arrays\n"
    report += "- **Jump Search**: O(√n) - Good for sorted arrays with sequential access\n"
    report += "- **Interpolation Search**: O(log log n) average - Best for uniformly distributed data\n"
    report += "- **Linear Search**: O(n) - Only option for unsorted data\n\n"

    return report

def analyze_graph_benchmarks(data: Dict) -> str:
    """Analyze graph algorithm benchmarks."""
    report = "## Graph Algorithms\n\n"
    report += "| Algorithm | Vertices | Edges | Time (avg) | Memory |\n"
    report += "|-----------|----------|-------|------------|--------|\n"

    if 'benchmarks' in data:
        for bench in data['benchmarks']:
            name = bench.get('name', 'Unknown')
            stats = bench.get('stats', {})
            extra = bench.get('extra_info', {})

            algo_name = name.split('_')[1] if '_' in name else name
            vertices = extra.get('vertices', 'Unknown')
            edges = extra.get('edges', 'Unknown')
            avg_time = format_time(stats.get('mean', 0) * 1e9)
            memory = format_memory(extra.get('memory_peak', 0))

            report += f"| {algo_name} | {vertices} | {edges} | {avg_time} | {memory} |\n"

    report += "\n### Analysis\n\n"
    report += "- **BFS/DFS**: O(V + E) - Fundamental traversal algorithms\n"
    report += "- **Dijkstra**: O(E log V) - Single-source shortest path\n"
    report += "- **Bellman-Ford**: O(VE) - Handles negative weights\n"
    report += "- **Floyd-Warshall**: O(V³) - All-pairs shortest path\n\n"

    return report

def analyze_dp_benchmarks(data: Dict) -> str:
    """Analyze dynamic programming benchmarks."""
    report = "## Dynamic Programming\n\n"
    report += "| Problem | Input Size | Time (avg) | Space | Memoized |\n"
    report += "|---------|------------|------------|-------|----------|\n"

    if 'benchmarks' in data:
        for bench in data['benchmarks']:
            name = bench.get('name', 'Unknown')
            stats = bench.get('stats', {})
            extra = bench.get('extra_info', {})

            problem = name.split('_')[1] if '_' in name else name
            size = extra.get('input_size', 'Unknown')
            avg_time = format_time(stats.get('mean', 0) * 1e9)
            space = format_memory(extra.get('memory_peak', 0))
            memoized = "Yes" if 'memo' in name.lower() else "No"

            report += f"| {problem} | {size} | {avg_time} | {space} | {memoized} |\n"

    report += "\n### Analysis\n\n"
    report += "- **Memoization**: Significant speedup for overlapping subproblems\n"
    report += "- **Space-Time Tradeoff**: Can often reduce space from O(n²) to O(n)\n"
    report += "- **Bottom-up vs Top-down**: Bottom-up usually more cache-friendly\n\n"

    return report

def analyze_memory_profile(filepath: str) -> str:
    """Analyze memory profiling results."""
    report = "## Memory Analysis\n\n"

    try:
        with open(filepath, 'r') as f:
            content = f.read()

        report += "### Memory Usage Summary\n\n"
        report += "```\n"
        report += content[:1000]  # First 1000 chars
        if len(content) > 1000:
            report += "\n... (truncated)\n"
        report += "```\n\n"

        # Extract key metrics if available
        if "peak memory" in content.lower():
            report += "### Key Findings\n\n"
            report += "- Peak memory usage detected\n"
            report += "- Consider using generators for large datasets\n"
            report += "- Profile memory-intensive operations separately\n\n"

    except Exception as e:
        report += f"Error loading memory profile: {e}\n\n"

    return report

def generate_summary(all_reports: List[str]) -> str:
    """Generate executive summary."""
    summary = "# Performance Benchmark Report\n\n"
    summary += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    summary += "## Executive Summary\n\n"
    summary += "This report contains comprehensive performance benchmarks for algorithms across multiple categories:\n\n"
    summary += "- **Sorting Algorithms**: Comparison of 10+ sorting implementations\n"
    summary += "- **Searching Algorithms**: Binary search variants and linear search optimizations\n"
    summary += "- **Graph Algorithms**: Traversal and shortest path algorithms\n"
    summary += "- **Dynamic Programming**: Classic DP problems with memoization analysis\n"
    summary += "- **Memory Profiling**: Heap usage and allocation patterns\n\n"

    summary += "## Key Recommendations\n\n"
    summary += "1. **Use appropriate algorithms for data characteristics**:\n"
    summary += "   - Small datasets (< 50 elements): Simple O(n²) algorithms often faster\n"
    summary += "   - Large datasets: O(n log n) algorithms essential\n"
    summary += "   - Nearly sorted data: Adaptive algorithms like TimSort excel\n\n"

    summary += "2. **Consider memory constraints**:\n"
    summary += "   - In-place algorithms for memory-constrained environments\n"
    summary += "   - Trade space for time when memory is available\n\n"

    summary += "3. **Profile before optimizing**:\n"
    summary += "   - Measure actual performance in production-like conditions\n"
    summary += "   - Focus optimization efforts on bottlenecks\n\n"

    return summary

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Generate performance report from benchmark results')
    parser.add_argument('--language', required=True, help='Programming language')
    parser.add_argument('--sorting', help='Sorting benchmark JSON file')
    parser.add_argument('--searching', help='Searching benchmark JSON file')
    parser.add_argument('--graph', help='Graph benchmark JSON file')
    parser.add_argument('--dp', help='Dynamic programming benchmark JSON file')
    parser.add_argument('--memory', help='Memory profiling report')
    parser.add_argument('--output', required=True, help='Output report file')

    args = parser.parse_args()

    reports = []

    # Add summary
    summary = generate_summary(reports)
    reports.insert(0, summary)

    # Process each benchmark type
    if args.sorting and Path(args.sorting).exists():
        data = load_benchmark_data(args.sorting)
        reports.append(analyze_sorting_benchmarks(data))

    if args.searching and Path(args.searching).exists():
        data = load_benchmark_data(args.searching)
        reports.append(analyze_searching_benchmarks(data))

    if args.graph and Path(args.graph).exists():
        data = load_benchmark_data(args.graph)
        reports.append(analyze_graph_benchmarks(data))

    if args.dp and Path(args.dp).exists():
        data = load_benchmark_data(args.dp)
        reports.append(analyze_dp_benchmarks(data))

    if args.memory and Path(args.memory).exists():
        reports.append(analyze_memory_profile(args.memory))

    # Add language-specific notes
    reports.append(f"\n## Language-Specific Notes ({args.language.capitalize()})\n\n")

    language_notes = {
        'python': "- CPython interpreter overhead affects small dataset performance\n- NumPy operations significantly faster for numerical algorithms\n- Consider PyPy for computation-heavy workloads\n",
        'typescript': "- V8 JIT optimization improves with warm-up runs\n- TypedArrays provide better performance for numerical operations\n- Consider WebAssembly for critical paths\n",
        'rust': "- Zero-cost abstractions maintain C-like performance\n- Compile with --release for accurate benchmarks\n- SIMD intrinsics available for further optimization\n",
        'java': "- JVM warm-up required for accurate measurements\n- JIT compilation improves performance over time\n- Consider GraalVM for better startup performance\n",
    }

    if args.language in language_notes:
        reports.append(language_notes[args.language])

    # Write report
    full_report = '\n'.join(reports)

    with open(args.output, 'w') as f:
        f.write(full_report)

    print(f"Performance report generated: {args.output}")

if __name__ == "__main__":
    main()