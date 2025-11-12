"""
Benchmark Analyzer - Statistical Analysis and Performance Insights

This module provides comprehensive statistical analysis of benchmark results,
including trend detection, regression analysis, performance comparisons,
and anomaly detection.

Features:
- Statistical metrics calculation (mean, median, std dev, percentiles)
- Performance trend analysis over time
- Regression detection against baselines
- Cross-language performance comparison
- Scalability analysis (performance vs input size)
- Outlier and anomaly detection
- Historical data analysis

Usage:
    analyzer = BenchmarkAnalyzer(db_path="benchmarks/data/benchmark_results.db")
    report = analyzer.generate_analysis_report()
    regressions = analyzer.detect_regressions()

@author Algorithms Multiverse
@version 1.0
"""

import sqlite3
import json
import yaml
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict
import statistics


@dataclass
class PerformanceMetrics:
    """Statistical metrics for a benchmark"""
    algorithm: str
    language: str
    input_size: int

    # Time metrics
    mean_time: float
    median_time: float
    std_dev_time: float
    min_time: float
    max_time: float
    percentile_95_time: float

    # Memory metrics
    mean_memory: float
    median_memory: float
    std_dev_memory: float
    max_memory: float

    # Metadata
    sample_count: int
    last_run: str


@dataclass
class RegressionAlert:
    """Alert for performance regression"""
    algorithm: str
    language: str
    input_size: int
    metric: str  # 'time' or 'memory'
    baseline_value: float
    current_value: float
    change_percent: float
    severity: str  # 'minor', 'moderate', 'severe'
    timestamp: str


@dataclass
class TrendAnalysis:
    """Performance trend over time"""
    algorithm: str
    language: str
    input_size: int
    metric: str
    trend_direction: str  # 'improving', 'degrading', 'stable'
    slope: float  # Rate of change
    confidence: float  # Statistical confidence
    data_points: int


class BenchmarkAnalyzer:
    """
    Statistical analyzer for benchmark results

    Provides comprehensive analysis including regressions, trends,
    comparisons, and scalability metrics.
    """

    def __init__(
        self,
        db_path: str = "benchmarks/data/benchmark_results.db",
        config_path: str = "benchmarks/config/config.yaml"
    ):
        """Initialize analyzer with database and config"""
        self.db_path = db_path
        self.config = self._load_config(config_path)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {}

    def get_recent_results(
        self,
        days: int = 7,
        algorithm: Optional[str] = None,
        language: Optional[str] = None
    ) -> List[Dict]:
        """Get recent benchmark results"""
        cursor = self.conn.cursor()

        cutoff = (datetime.now() - timedelta(days=days)).isoformat()

        query = '''
            SELECT * FROM benchmark_results
            WHERE timestamp > ? AND success = 1
        '''
        params = [cutoff]

        if algorithm:
            query += ' AND algorithm = ?'
            params.append(algorithm)

        if language:
            query += ' AND language = ?'
            params.append(language)

        query += ' ORDER BY timestamp DESC'

        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def calculate_metrics(
        self,
        algorithm: str,
        language: str,
        input_size: int,
        days: int = 30
    ) -> Optional[PerformanceMetrics]:
        """Calculate statistical metrics for a specific benchmark"""
        results = self.get_recent_results(days=days, algorithm=algorithm, language=language)

        # Filter by input size
        results = [r for r in results if r['input_size'] == input_size]

        if not results:
            return None

        times = [r['execution_time'] for r in results]
        memories = [r['memory_usage'] for r in results]

        return PerformanceMetrics(
            algorithm=algorithm,
            language=language,
            input_size=input_size,
            mean_time=np.mean(times),
            median_time=np.median(times),
            std_dev_time=np.std(times),
            min_time=np.min(times),
            max_time=np.max(times),
            percentile_95_time=np.percentile(times, 95),
            mean_memory=np.mean(memories),
            median_memory=np.median(memories),
            std_dev_memory=np.std(memories),
            max_memory=np.max(memories),
            sample_count=len(results),
            last_run=max(r['timestamp'] for r in results)
        )

    def detect_regressions(
        self,
        baseline_days: int = 30,
        recent_days: int = 7,
        threshold_percent: float = None
    ) -> List[RegressionAlert]:
        """
        Detect performance regressions by comparing recent vs baseline

        Args:
            baseline_days: Days to look back for baseline
            recent_days: Recent period to compare
            threshold_percent: Custom threshold (uses config if None)

        Returns:
            List of regression alerts
        """
        if threshold_percent is None:
            threshold_percent = self.config.get('thresholds', {}).get(
                'max_time_increase_percent', 20
            )

        alerts = []

        # Get unique algorithm/language combinations
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT DISTINCT algorithm, language, input_size
            FROM benchmark_results
            WHERE success = 1
        ''')

        combinations = cursor.fetchall()

        for algo, lang, size in combinations:
            # Get baseline metrics
            baseline_end = datetime.now() - timedelta(days=recent_days)
            baseline_start = baseline_end - timedelta(days=baseline_days)

            baseline_results = self._get_results_in_range(
                algo, lang, size, baseline_start, baseline_end
            )

            if not baseline_results:
                continue

            # Get recent metrics
            recent_results = self.get_recent_results(
                days=recent_days, algorithm=algo, language=lang
            )
            recent_results = [r for r in recent_results if r['input_size'] == size]

            if not recent_results:
                continue

            # Compare time performance
            baseline_time = np.median([r['execution_time'] for r in baseline_results])
            recent_time = np.median([r['execution_time'] for r in recent_results])

            time_change = ((recent_time - baseline_time) / baseline_time) * 100

            if time_change > threshold_percent:
                alerts.append(RegressionAlert(
                    algorithm=algo,
                    language=lang,
                    input_size=size,
                    metric='time',
                    baseline_value=baseline_time,
                    current_value=recent_time,
                    change_percent=time_change,
                    severity=self._determine_severity(time_change, threshold_percent),
                    timestamp=datetime.now().isoformat()
                ))

            # Compare memory performance
            baseline_memory = np.median([r['memory_usage'] for r in baseline_results])
            recent_memory = np.median([r['memory_usage'] for r in recent_results])

            memory_threshold = self.config.get('thresholds', {}).get(
                'max_memory_increase_percent', 30
            )
            memory_change = ((recent_memory - baseline_memory) / baseline_memory) * 100

            if memory_change > memory_threshold:
                alerts.append(RegressionAlert(
                    algorithm=algo,
                    language=lang,
                    input_size=size,
                    metric='memory',
                    baseline_value=baseline_memory,
                    current_value=recent_memory,
                    change_percent=memory_change,
                    severity=self._determine_severity(memory_change, memory_threshold),
                    timestamp=datetime.now().isoformat()
                ))

        return alerts

    def _get_results_in_range(
        self,
        algorithm: str,
        language: str,
        input_size: int,
        start_time: datetime,
        end_time: datetime
    ) -> List[Dict]:
        """Get results within a time range"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM benchmark_results
            WHERE algorithm = ? AND language = ? AND input_size = ?
            AND timestamp BETWEEN ? AND ?
            AND success = 1
            ORDER BY timestamp
        ''', (algorithm, language, input_size, start_time.isoformat(), end_time.isoformat()))

        return [dict(row) for row in cursor.fetchall()]

    def _determine_severity(self, change_percent: float, threshold: float) -> str:
        """Determine severity of regression"""
        if change_percent < threshold * 1.5:
            return 'minor'
        elif change_percent < threshold * 2.5:
            return 'moderate'
        else:
            return 'severe'

    def analyze_trends(
        self,
        algorithm: str,
        language: str,
        input_size: int,
        days: int = 90
    ) -> Optional[TrendAnalysis]:
        """
        Analyze performance trend over time

        Uses linear regression to determine if performance is
        improving, degrading, or stable.
        """
        results = self.get_recent_results(days=days, algorithm=algorithm, language=language)
        results = [r for r in results if r['input_size'] == input_size]

        if len(results) < 5:  # Need minimum data points
            return None

        # Convert timestamps to numerical values (days from first)
        timestamps = [datetime.fromisoformat(r['timestamp']) for r in results]
        first_time = min(timestamps)
        x = np.array([(t - first_time).total_seconds() / 86400 for t in timestamps])
        y = np.array([r['execution_time'] for r in results])

        # Linear regression
        if len(x) > 1:
            slope, intercept = np.polyfit(x, y, 1)

            # Calculate R-squared for confidence
            y_pred = slope * x + intercept
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

            # Determine trend direction
            if abs(slope) < 0.001:  # Essentially flat
                direction = 'stable'
            elif slope < 0:
                direction = 'improving'
            else:
                direction = 'degrading'

            return TrendAnalysis(
                algorithm=algorithm,
                language=language,
                input_size=input_size,
                metric='time',
                trend_direction=direction,
                slope=slope,
                confidence=r_squared,
                data_points=len(results)
            )

        return None

    def compare_languages(
        self,
        algorithm: str,
        input_size: int,
        days: int = 30
    ) -> Dict[str, PerformanceMetrics]:
        """Compare performance across languages for same algorithm"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT DISTINCT language FROM benchmark_results
            WHERE algorithm = ? AND input_size = ? AND success = 1
        ''', (algorithm, input_size))

        languages = [row[0] for row in cursor.fetchall()]

        comparison = {}
        for lang in languages:
            metrics = self.calculate_metrics(algorithm, lang, input_size, days)
            if metrics:
                comparison[lang] = metrics

        return comparison

    def analyze_scalability(
        self,
        algorithm: str,
        language: str,
        days: int = 30
    ) -> Dict[int, Dict[str, float]]:
        """
        Analyze how performance scales with input size

        Returns dict mapping input_size to performance metrics
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT DISTINCT input_size FROM benchmark_results
            WHERE algorithm = ? AND language = ? AND success = 1
            ORDER BY input_size
        ''', (algorithm, language))

        input_sizes = [row[0] for row in cursor.fetchall()]

        scalability = {}
        for size in input_sizes:
            metrics = self.calculate_metrics(algorithm, language, size, days)
            if metrics:
                scalability[size] = {
                    'mean_time': metrics.mean_time,
                    'mean_memory': metrics.mean_memory,
                    'std_dev_time': metrics.std_dev_time
                }

        return scalability

    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate comprehensive summary report"""
        cursor = self.conn.cursor()

        # Overall statistics
        cursor.execute('''
            SELECT
                COUNT(*) as total_runs,
                COUNT(DISTINCT algorithm) as unique_algorithms,
                COUNT(DISTINCT language) as languages_tested,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_runs,
                AVG(execution_time) as avg_execution_time,
                AVG(memory_usage) as avg_memory_usage
            FROM benchmark_results
            WHERE timestamp > datetime('now', '-30 days')
        ''')

        stats = dict(cursor.fetchone())

        # Recent performance by language
        cursor.execute('''
            SELECT
                language,
                COUNT(*) as runs,
                AVG(execution_time) as avg_time,
                AVG(memory_usage) as avg_memory
            FROM benchmark_results
            WHERE timestamp > datetime('now', '-7 days') AND success = 1
            GROUP BY language
            ORDER BY avg_time
        ''')

        language_stats = [dict(row) for row in cursor.fetchall()]

        # Detect regressions
        regressions = self.detect_regressions()

        return {
            'generated_at': datetime.now().isoformat(),
            'overall_statistics': stats,
            'language_performance': language_stats,
            'regressions_found': len(regressions),
            'regression_details': [asdict(r) for r in regressions[:10]],  # Top 10
            'data_period_days': 30
        }

    def export_analysis(
        self,
        output_file: str,
        format: str = 'json'
    ):
        """Export analysis results to file"""
        report = self.generate_summary_report()

        if format == 'json':
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
        elif format == 'yaml':
            with open(output_file, 'w') as f:
                yaml.dump(report, f, default_flow_style=False)

        print(f"Analysis exported to: {output_file}")

    def close(self):
        """Close database connection"""
        self.conn.close()


def main():
    """Main entry point for analyzer"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Benchmark Results Analyzer"
    )
    parser.add_argument(
        '--db',
        default='benchmarks/data/benchmark_results.db',
        help='Path to benchmark database'
    )
    parser.add_argument(
        '--action',
        choices=['summary', 'regressions', 'trends', 'compare'],
        default='summary',
        help='Analysis action to perform'
    )
    parser.add_argument(
        '--algorithm',
        help='Specific algorithm to analyze'
    )
    parser.add_argument(
        '--language',
        help='Specific language to analyze'
    )
    parser.add_argument(
        '--output',
        help='Output file for export'
    )

    args = parser.parse_args()

    analyzer = BenchmarkAnalyzer(db_path=args.db)

    try:
        if args.action == 'summary':
            report = analyzer.generate_summary_report()
            print(json.dumps(report, indent=2))

            if args.output:
                analyzer.export_analysis(args.output)

        elif args.action == 'regressions':
            regressions = analyzer.detect_regressions()

            if regressions:
                print(f"\nFound {len(regressions)} performance regressions:\n")
                for reg in regressions:
                    print(f"[{reg.severity.upper()}] {reg.algorithm} ({reg.language})")
                    print(f"  Metric: {reg.metric}")
                    print(f"  Change: {reg.change_percent:+.1f}%")
                    print(f"  Baseline: {reg.baseline_value:.4f}")
                    print(f"  Current: {reg.current_value:.4f}\n")
            else:
                print("No regressions detected!")

        elif args.action == 'compare' and args.algorithm:
            comparison = analyzer.compare_languages(args.algorithm, 1000)

            print(f"\nLanguage Comparison for {args.algorithm}:\n")
            for lang, metrics in sorted(
                comparison.items(),
                key=lambda x: x[1].mean_time
            ):
                print(f"{lang:15s}: {metrics.mean_time:8.4f}s "
                      f"(±{metrics.std_dev_time:.4f}s) "
                      f"Memory: {metrics.mean_memory:.2f} MB")

    finally:
        analyzer.close()


if __name__ == '__main__':
    main()
