"""
Aggregate and Visualize Cross-Language Benchmark Results
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_results(languages: List[str]) -> List[Dict[str, Any]]:
    """Load benchmark results from all language result files"""
    all_results = []

    for lang in languages:
        result_file = f'results_{lang.lower()}.json'

        try:
            with open(result_file, 'r') as f:
                results = json.load(f)
                all_results.extend(results)
                print(f"Loaded {len(results)} results from {result_file}")
        except FileNotFoundError:
            print(f"Warning: {result_file} not found, skipping {lang}")
        except json.JSONDecodeError as e:
            print(f"Error parsing {result_file}: {e}")

    return all_results

def filter_successful_results(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """Convert results to DataFrame and filter successful runs"""
    records = []

    for result in results:
        if result.get('status') != 'success':
            continue

        timing = result.get('timing', {})
        if not timing:
            continue

        record = {
            'name': result['name'],
            'language': result['language'],
            'algorithm': result['algorithm'],
            'vertices': result['graph']['vertices'],
            'graph_type': result['graph']['type'],
            'density': result['graph'].get('density', 'N/A'),
            'directed': result['graph']['directed'],
            'weighted': result['graph']['weighted'],
            'mean_time': timing['mean'],
            'median_time': timing['median'],
            'std_dev': timing['std_dev'],
            'min_time': timing['min'],
            'max_time': timing['max'],
            'trials': result.get('trials', 0),
            'successful_trials': result.get('successful_trials', 0)
        }
        records.append(record)

    df = pd.DataFrame(records)
    print(f"\nProcessed {len(df)} successful benchmark results")
    return df

def create_performance_comparison(df: pd.DataFrame, output_dir: Path):
    """Create performance comparison charts for each benchmark"""
    output_dir.mkdir(exist_ok=True)

    # Get unique benchmark names
    benchmarks = df['name'].unique()

    for benchmark_name in benchmarks:
        data = df[df['name'] == benchmark_name].copy()

        if data.empty:
            continue

        # Sort by mean time for better visualization
        data = data.sort_values('mean_time')

        # Create figure
        plt.figure(figsize=(12, 6))

        # Bar plot
        plt.subplot(1, 2, 1)
        bars = plt.bar(data['language'], data['mean_time'] * 1000)

        # Color bars by performance
        colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(bars)))
        for bar, color in zip(bars, colors):
            bar.set_color(color)

        plt.xlabel('Language')
        plt.ylabel('Mean Time (ms)')
        plt.title(f'{benchmark_name}\nPerformance Comparison')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)

        # Add value labels on bars
        for i, (idx, row) in enumerate(data.iterrows()):
            plt.text(i, row['mean_time'] * 1000 + (data['mean_time'].max() * 1000 * 0.02),
                    f"{row['mean_time'] * 1000:.2f}",
                    ha='center', va='bottom', fontsize=9)

        # Speedup comparison (relative to slowest)
        plt.subplot(1, 2, 2)
        slowest_time = data['mean_time'].max()
        data['speedup'] = slowest_time / data['mean_time']

        bars = plt.bar(data['language'], data['speedup'])
        colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(bars)))
        for bar, color in zip(bars, colors):
            bar.set_color(color)

        plt.xlabel('Language')
        plt.ylabel('Speedup (vs slowest)')
        plt.title(f'{benchmark_name}\nRelative Performance')
        plt.xticks(rotation=45, ha='right')
        plt.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
        plt.grid(axis='y', alpha=0.3)

        # Add value labels
        for i, (idx, row) in enumerate(data.iterrows()):
            plt.text(i, row['speedup'] + 0.05, f"{row['speedup']:.2f}x",
                    ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        output_file = output_dir / f'comparison_{benchmark_name.replace(" ", "_")}.png'
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"Created: {output_file}")

def create_algorithm_comparison(df: pd.DataFrame, output_dir: Path):
    """Compare performance across algorithms for each language"""
    languages = df['language'].unique()

    for language in languages:
        lang_data = df[df['language'] == language].copy()

        if lang_data.empty:
            continue

        # Group by algorithm
        algorithm_data = lang_data.groupby('algorithm')['mean_time'].mean().sort_values()

        if algorithm_data.empty:
            continue

        plt.figure(figsize=(10, 6))
        bars = plt.barh(range(len(algorithm_data)), algorithm_data.values * 1000)

        # Color bars
        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(bars)))
        for bar, color in zip(bars, colors):
            bar.set_color(color)

        plt.yticks(range(len(algorithm_data)), algorithm_data.index)
        plt.xlabel('Mean Time (ms)')
        plt.title(f'{language} - Algorithm Performance Comparison')
        plt.grid(axis='x', alpha=0.3)

        # Add value labels
        for i, val in enumerate(algorithm_data.values):
            plt.text(val * 1000 + (algorithm_data.max() * 1000 * 0.02), i,
                    f"{val * 1000:.2f}",
                    va='center', fontsize=9)

        plt.tight_layout()
        output_file = output_dir / f'algorithms_{language.lower()}.png'
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"Created: {output_file}")

def create_overall_heatmap(df: pd.DataFrame, output_dir: Path):
    """Create a heatmap showing performance across all benchmarks and languages"""
    # Pivot table: benchmarks vs languages
    pivot = df.pivot_table(values='mean_time', index='name', columns='language', aggfunc='mean')

    if pivot.empty:
        print("Not enough data for heatmap")
        return

    # Convert to milliseconds
    pivot = pivot * 1000

    plt.figure(figsize=(12, max(8, len(pivot) * 0.5)))

    # Create heatmap
    sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn_r',
                cbar_kws={'label': 'Mean Time (ms)'}, linewidths=0.5)

    plt.title('Performance Heatmap: All Benchmarks vs Languages')
    plt.xlabel('Language')
    plt.ylabel('Benchmark')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    plt.tight_layout()
    output_file = output_dir / 'heatmap_overall.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"Created: {output_file}")

def create_summary_table(df: pd.DataFrame, output_dir: Path):
    """Create summary statistics table"""
    summary_data = []

    for language in df['language'].unique():
        lang_data = df[df['language'] == language]

        summary_data.append({
            'Language': language,
            'Benchmarks Run': len(lang_data),
            'Avg Time (ms)': f"{lang_data['mean_time'].mean() * 1000:.3f}",
            'Min Time (ms)': f"{lang_data['mean_time'].min() * 1000:.3f}",
            'Max Time (ms)': f"{lang_data['mean_time'].max() * 1000:.3f}",
            'Std Dev (ms)': f"{lang_data['mean_time'].std() * 1000:.3f}"
        })

    summary_df = pd.DataFrame(summary_data)
    summary_df = summary_df.sort_values('Avg Time (ms)')

    # Save to CSV
    csv_file = output_dir / 'summary_statistics.csv'
    summary_df.to_csv(csv_file, index=False)
    print(f"Created: {csv_file}")

    # Print to console
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(summary_df.to_string(index=False))
    print("=" * 80)

def create_variability_analysis(df: pd.DataFrame, output_dir: Path):
    """Analyze timing variability across trials"""
    benchmarks = df['name'].unique()

    for benchmark_name in benchmarks:
        data = df[df['name'] == benchmark_name].copy()

        if data.empty or len(data) < 2:
            continue

        plt.figure(figsize=(10, 6))

        # Box plot showing variability
        languages = data['language'].tolist()
        times = [data[data['language'] == lang]['mean_time'].values * 1000 for lang in languages]

        bp = plt.boxplot([data[data['language'] == lang]['mean_time'].values * 1000
                          for lang in data['language']],
                         labels=data['language'],
                         patch_artist=True)

        # Color boxes
        colors = plt.cm.Set3(np.linspace(0, 1, len(bp['boxes'])))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)

        plt.xlabel('Language')
        plt.ylabel('Time (ms)')
        plt.title(f'{benchmark_name}\nTiming Variability Analysis')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        output_file = output_dir / f'variability_{benchmark_name.replace(" ", "_")}.png'
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"Created: {output_file}")

def main():
    """Main aggregation and visualization function"""
    print("=" * 80)
    print("Cross-Language Benchmark Results Aggregation")
    print("=" * 80)
    print()

    # Languages to check
    languages = ['Python', 'JavaScript', 'Java', 'C++', 'Go', 'Rust']

    # Load results
    results = load_results(languages)

    if not results:
        print("Error: No results found!")
        sys.exit(1)

    # Convert to DataFrame
    df = filter_successful_results(results)

    if df.empty:
        print("Error: No successful benchmark results found!")
        sys.exit(1)

    # Create output directory
    output_dir = Path('benchmark_results')
    output_dir.mkdir(exist_ok=True)

    # Generate visualizations
    print("\nGenerating visualizations...")
    create_performance_comparison(df, output_dir)
    create_algorithm_comparison(df, output_dir)
    create_overall_heatmap(df, output_dir)
    create_variability_analysis(df, output_dir)
    create_summary_table(df, output_dir)

    print("\n" + "=" * 80)
    print("All visualizations created successfully!")
    print(f"Results saved to: {output_dir.absolute()}")
    print("=" * 80)

if __name__ == '__main__':
    main()
