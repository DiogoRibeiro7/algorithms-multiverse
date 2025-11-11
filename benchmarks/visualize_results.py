#!/usr/bin/env python3
"""
Visualization script for Dijkstra benchmark results

Usage:
    python visualize_results.py

Requires:
    pip install pandas matplotlib seaborn
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_data():
    """Load benchmark results from CSV files"""
    results_file = Path('dijkstra_results.csv')
    trials_file = Path('dijkstra_trials.csv')

    if not results_file.exists():
        raise FileNotFoundError(
            "dijkstra_results.csv not found. Run the benchmark first."
        )

    results = pd.read_csv(results_file)
    trials = pd.read_csv(trials_file) if trials_file.exists() else None

    return results, trials

def plot_performance_comparison(results, output_dir='plots'):
    """Plot execution time vs graph size"""
    Path(output_dir).mkdir(exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Separate dense and sparse
    dense_mask = results['density'] > 0.1

    # Dense graphs
    dense_data = results[dense_mask]
    for heap_type in dense_data['heap_type'].unique():
        data = dense_data[dense_data['heap_type'] == heap_type]
        ax1.errorbar(
            data['num_vertices'],
            data['mean_time_ms'],
            yerr=data['std_dev_ms'],
            label=heap_type,
            marker='o',
            markersize=8,
            capsize=5,
            linewidth=2
        )

    ax1.set_xlabel('Number of Vertices', fontsize=12)
    ax1.set_ylabel('Execution Time (ms)', fontsize=12)
    ax1.set_title('Dense Graphs Performance', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    # Sparse graphs
    sparse_data = results[~dense_mask]
    for heap_type in sparse_data['heap_type'].unique():
        data = sparse_data[sparse_data['heap_type'] == heap_type]
        ax2.errorbar(
            data['num_vertices'],
            data['mean_time_ms'],
            yerr=data['std_dev_ms'],
            label=heap_type,
            marker='s',
            markersize=8,
            capsize=5,
            linewidth=2
        )

    ax2.set_xlabel('Number of Vertices', fontsize=12)
    ax2.set_ylabel('Execution Time (ms)', fontsize=12)
    ax2.set_title('Sparse Graphs Performance', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    ax2.set_yscale('log')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/performance_comparison.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/performance_comparison.png")
    plt.close()

def plot_speedup_analysis(results, output_dir='plots'):
    """Plot speedup ratio between heaps"""
    Path(output_dir).mkdir(exist_ok=True)

    # Calculate speedup for each configuration
    binary_data = results[results['heap_type'] == 'Binary Heap'].copy()
    fib_data = results[results['heap_type'] == 'Fibonacci Heap'].copy()

    # Merge on graph properties
    merged = binary_data.merge(
        fib_data,
        on=['num_vertices', 'num_edges'],
        suffixes=('_binary', '_fib')
    )

    merged['speedup'] = merged['mean_time_ms_fib'] / merged['mean_time_ms_binary']
    merged['graph_type'] = merged['density_binary'].apply(
        lambda x: 'Dense' if x > 0.1 else 'Sparse'
    )

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Speedup by vertices
    for graph_type in ['Dense', 'Sparse']:
        data = merged[merged['graph_type'] == graph_type]
        ax1.plot(
            data['num_vertices'],
            data['speedup'],
            marker='o',
            markersize=10,
            linewidth=2,
            label=graph_type
        )

    ax1.axhline(y=1.0, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Equal Performance')
    ax1.set_xlabel('Number of Vertices', fontsize=12)
    ax1.set_ylabel('Speedup (Fib time / Binary time)', fontsize=12)
    ax1.set_title('Performance Ratio Analysis', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')

    # Add annotations
    ax1.text(0.05, 0.95, 'Values > 1: Binary faster\nValues < 1: Fibonacci faster',
             transform=ax1.transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # Operations comparison
    ax2.scatter(
        merged['decrease_key_ops_binary'],
        merged['speedup'],
        s=merged['num_edges'] / 100,
        alpha=0.6,
        c=merged['density_binary'],
        cmap='viridis'
    )

    ax2.axhline(y=1.0, color='red', linestyle='--', linewidth=2, alpha=0.7)
    ax2.set_xlabel('Decrease-Key Operations', fontsize=12)
    ax2.set_ylabel('Speedup', fontsize=12)
    ax2.set_title('Speedup vs Decrease-Key Operations', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    cbar = plt.colorbar(ax2.collections[0], ax=ax2)
    cbar.set_label('Graph Density', fontsize=11)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/speedup_analysis.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/speedup_analysis.png")
    plt.close()

def plot_trial_distributions(trials, output_dir='plots'):
    """Plot distribution of trial times"""
    if trials is None:
        print("No trials data available")
        return

    Path(output_dir).mkdir(exist_ok=True)

    # Select a few representative configurations
    vertices_to_plot = sorted(trials['num_vertices'].unique())[-3:]  # Last 3 sizes

    fig, axes = plt.subplots(1, len(vertices_to_plot), figsize=(15, 5))
    if len(vertices_to_plot) == 1:
        axes = [axes]

    for idx, num_v in enumerate(vertices_to_plot):
        data = trials[trials['num_vertices'] == num_v]

        sns.violinplot(
            data=data,
            x='heap_type',
            y='time_ms',
            ax=axes[idx],
            palette='Set2'
        )

        axes[idx].set_title(f'V = {num_v}', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('')
        axes[idx].set_ylabel('Time (ms)' if idx == 0 else '', fontsize=11)
        axes[idx].grid(True, alpha=0.3, axis='y')

        # Rotate labels
        axes[idx].tick_params(axis='x', rotation=45)

    plt.suptitle('Trial Time Distributions', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/trial_distributions.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/trial_distributions.png")
    plt.close()

def plot_theoretical_vs_actual(results, output_dir='plots'):
    """Compare theoretical and actual complexity"""
    Path(output_dir).mkdir(exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Actual time vs theoretical complexity
    for heap_type in results['heap_type'].unique():
        data = results[results['heap_type'] == heap_type]
        ax1.scatter(
            data['theoretical_complexity'],
            data['mean_time_ms'],
            label=heap_type,
            alpha=0.7,
            s=100
        )

    ax1.set_xlabel('Theoretical Complexity (operations)', fontsize=12)
    ax1.set_ylabel('Actual Time (ms)', fontsize=12)
    ax1.set_title('Theoretical vs Actual Performance', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    # Time per operation
    results_copy = results.copy()
    results_copy['time_per_op'] = (
        results_copy['mean_time_ms'] / results_copy['theoretical_complexity'] * 1e6
    )

    for heap_type in results_copy['heap_type'].unique():
        data = results_copy[results_copy['heap_type'] == heap_type]
        ax2.plot(
            data['num_vertices'],
            data['time_per_op'],
            marker='o',
            markersize=8,
            linewidth=2,
            label=heap_type
        )

    ax2.set_xlabel('Number of Vertices', fontsize=12)
    ax2.set_ylabel('Time per Operation (ns)', fontsize=12)
    ax2.set_title('Amortized Time per Operation', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/theoretical_vs_actual.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/theoretical_vs_actual.png")
    plt.close()

def plot_operations_breakdown(results, output_dir='plots'):
    """Plot breakdown of heap operations"""
    Path(output_dir).mkdir(exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Operations count
    binary_data = results[results['heap_type'] == 'Binary Heap']
    fib_data = results[results['heap_type'] == 'Fibonacci Heap']

    x = np.arange(len(binary_data))
    width = 0.35

    ax1.bar(x - width/2, binary_data['heap_operations'], width,
            label='Total Ops', alpha=0.8)
    ax1.bar(x + width/2, binary_data['decrease_key_ops'], width,
            label='Decrease-Key', alpha=0.8)

    ax1.set_xlabel('Configuration Index', fontsize=12)
    ax1.set_ylabel('Operation Count', fontsize=12)
    ax1.set_title('Binary Heap Operations', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.set_yscale('log')

    ax2.bar(x - width/2, fib_data['heap_operations'], width,
            label='Total Ops', alpha=0.8)
    ax2.bar(x + width/2, fib_data['decrease_key_ops'], width,
            label='Decrease-Key', alpha=0.8)

    ax2.set_xlabel('Configuration Index', fontsize=12)
    ax2.set_ylabel('Operation Count', fontsize=12)
    ax2.set_title('Fibonacci Heap Operations', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_yscale('log')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/operations_breakdown.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/operations_breakdown.png")
    plt.close()

def generate_summary_report(results, trials, output_dir='plots'):
    """Generate text summary report"""
    Path(output_dir).mkdir(exist_ok=True)

    with open(f'{output_dir}/summary_report.txt', 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("DIJKSTRA BENCHMARK SUMMARY REPORT\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"Total Configurations Tested: {len(results) // 2}\n")
        f.write(f"Heap Types: {', '.join(results['heap_type'].unique())}\n")
        f.write(f"Vertex Counts: {sorted(results['num_vertices'].unique())}\n\n")

        f.write("=" * 80 + "\n")
        f.write("PERFORMANCE SUMMARY\n")
        f.write("=" * 80 + "\n\n")

        # Calculate overall statistics
        binary_data = results[results['heap_type'] == 'Binary Heap']
        fib_data = results[results['heap_type'] == 'Fibonacci Heap']

        f.write("Binary Heap:\n")
        f.write(f"  Mean execution time: {binary_data['mean_time_ms'].mean():.3f} ms\n")
        f.write(f"  Min execution time:  {binary_data['min_ms'].min():.3f} ms\n")
        f.write(f"  Max execution time:  {binary_data['max_ms'].max():.3f} ms\n\n")

        f.write("Fibonacci Heap:\n")
        f.write(f"  Mean execution time: {fib_data['mean_time_ms'].mean():.3f} ms\n")
        f.write(f"  Min execution time:  {fib_data['min_ms'].min():.3f} ms\n")
        f.write(f"  Max execution time:  {fib_data['max_ms'].max():.3f} ms\n\n")

        # Winner analysis
        merged = binary_data.merge(fib_data, on=['num_vertices', 'num_edges'],
                                   suffixes=('_binary', '_fib'))

        binary_wins = (merged['mean_time_ms_binary'] < merged['mean_time_ms_fib']).sum()
        fib_wins = len(merged) - binary_wins

        f.write(f"\nBinary Heap faster in: {binary_wins}/{len(merged)} configurations "
                f"({binary_wins/len(merged)*100:.1f}%)\n")
        f.write(f"Fibonacci Heap faster in: {fib_wins}/{len(merged)} configurations "
                f"({fib_wins/len(merged)*100:.1f}%)\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("KEY FINDINGS\n")
        f.write("=" * 80 + "\n\n")

        avg_speedup = (merged['mean_time_ms_fib'] / merged['mean_time_ms_binary']).mean()
        if avg_speedup > 1:
            f.write(f"1. Binary Heap is {avg_speedup:.2f}x faster on average\n")
        else:
            f.write(f"1. Fibonacci Heap is {1/avg_speedup:.2f}x faster on average\n")

        f.write(f"\n2. Average decrease-key operations: "
                f"{binary_data['decrease_key_ops'].mean():.0f}\n")

        f.write(f"\n3. Largest graph tested: "
                f"V={results['num_vertices'].max()}, "
                f"E={results['num_edges'].max()}\n")

    print(f"Saved: {output_dir}/summary_report.txt")

def main():
    """Main execution function"""
    print("Loading benchmark data...")
    results, trials = load_data()

    print("\nGenerating visualizations...")
    plot_performance_comparison(results)
    plot_speedup_analysis(results)
    plot_theoretical_vs_actual(results)
    plot_operations_breakdown(results)

    if trials is not None:
        plot_trial_distributions(trials)

    generate_summary_report(results, trials)

    print("\n" + "=" * 80)
    print("Visualization complete!")
    print("=" * 80)
    print("\nGenerated files in 'plots/' directory:")
    print("  - performance_comparison.png")
    print("  - speedup_analysis.png")
    print("  - theoretical_vs_actual.png")
    print("  - operations_breakdown.png")
    if trials is not None:
        print("  - trial_distributions.png")
    print("  - summary_report.txt")
    print("\n")

if __name__ == '__main__':
    try:
        main()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease run the benchmark first:")
        print("  ./compare_dijkstra")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
