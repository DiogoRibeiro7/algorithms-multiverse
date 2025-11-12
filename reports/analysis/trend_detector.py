"""
Trend Detector - Analyzes performance trends and detects regressions
"""

import statistics
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class TrendDetector:
    """Detects performance trends and regressions over time"""

    def __init__(self, db):
        """
        Initialize trend detector

        Args:
            db: PerformanceDatabase instance
        """
        self.db = db

    def detect_trends(self, current_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect performance trends and regressions

        Args:
            current_results: Current benchmark results

        Returns:
            Dictionary containing trend analysis and regressions
        """
        trends = {
            'regressions': [],
            'improvements': [],
            'stable': [],
            'new_benchmarks': []
        }

        for category, algorithms in current_results.items():
            for algorithm, languages in algorithms.items():
                for language, data in languages.items():
                    if 'error' in data:
                        continue

                    # Get historical data
                    historical = self.db.get_historical_data(algorithm, language, limit=10)

                    if not historical:
                        # New benchmark with no history
                        trends['new_benchmarks'].append({
                            'algorithm': algorithm,
                            'language': language,
                            'category': category,
                            'current_time': data['avg_time_ms']
                        })
                        continue

                    # Calculate baseline (median of historical data)
                    baseline = statistics.median([h['avg_time_ms'] for h in historical])
                    current_time = data['avg_time_ms']

                    # Calculate percentage change
                    percent_change = ((current_time - baseline) / baseline) * 100

                    # Determine trend status
                    trend_info = {
                        'algorithm': algorithm,
                        'language': language,
                        'category': category,
                        'baseline': baseline,
                        'current': current_time,
                        'percent_change': percent_change,
                        'historical_count': len(historical)
                    }

                    # Regression threshold (default 10%)
                    regression_threshold = 10.0
                    improvement_threshold = -10.0

                    if percent_change > regression_threshold:
                        trend_info['regression_percent'] = percent_change
                        trends['regressions'].append(trend_info)
                        logger.warning(
                            f"Regression detected: {algorithm} ({language}) "
                            f"- {percent_change:.1f}% slower"
                        )
                    elif percent_change < improvement_threshold:
                        trend_info['improvement_percent'] = abs(percent_change)
                        trends['improvements'].append(trend_info)
                        logger.info(
                            f"Improvement detected: {algorithm} ({language}) "
                            f"- {abs(percent_change):.1f}% faster"
                        )
                    else:
                        trends['stable'].append(trend_info)

        # Summary statistics
        trends['summary'] = {
            'total_regressions': len(trends['regressions']),
            'total_improvements': len(trends['improvements']),
            'total_stable': len(trends['stable']),
            'total_new': len(trends['new_benchmarks'])
        }

        return trends

    def analyze_long_term_trends(
        self,
        algorithm: str,
        language: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze long-term performance trends

        Args:
            algorithm: Algorithm name
            language: Language name
            days: Number of days to analyze

        Returns:
            Long-term trend analysis
        """
        trends = self.db.get_performance_trends(algorithm, language, days)

        if len(trends) < 2:
            return {'status': 'insufficient_data', 'data_points': len(trends)}

        times = [t['avg_time_ms'] for t in trends]
        timestamps = [t['timestamp'] for t in trends]

        # Calculate trend direction using linear regression slope
        n = len(times)
        x = list(range(n))
        x_mean = statistics.mean(x)
        y_mean = statistics.mean(times)

        numerator = sum((x[i] - x_mean) * (times[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator

        # Determine trend direction
        if slope > 0.01:  # Getting slower
            direction = 'degrading'
        elif slope < -0.01:  # Getting faster
            direction = 'improving'
        else:
            direction = 'stable'

        # Calculate volatility (coefficient of variation)
        stdev = statistics.stdev(times) if len(times) > 1 else 0
        mean = statistics.mean(times)
        volatility = (stdev / mean * 100) if mean > 0 else 0

        return {
            'algorithm': algorithm,
            'language': language,
            'direction': direction,
            'slope': slope,
            'volatility_percent': volatility,
            'data_points': n,
            'time_range': {
                'start': timestamps[0],
                'end': timestamps[-1]
            },
            'performance': {
                'mean': mean,
                'stdev': stdev,
                'min': min(times),
                'max': max(times),
                'latest': times[-1]
            }
        }

    def detect_anomalies(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect performance anomalies

        Args:
            results: Benchmark results

        Returns:
            List of detected anomalies
        """
        anomalies = []

        for category, algorithms in results.items():
            for algorithm, languages in algorithms.items():
                for language, data in languages.items():
                    if 'error' in data or 'times_ms' not in data:
                        continue

                    times = data['times_ms']

                    if len(times) < 3:
                        continue

                    # Calculate z-scores for outlier detection
                    mean = statistics.mean(times)
                    stdev = statistics.stdev(times)

                    if stdev == 0:
                        continue

                    z_scores = [(t - mean) / stdev for t in times]

                    # Detect extreme outliers (|z| > 3)
                    extreme_outliers = [
                        (i, times[i], z) for i, z in enumerate(z_scores)
                        if abs(z) > 3
                    ]

                    if extreme_outliers:
                        anomalies.append({
                            'algorithm': algorithm,
                            'language': language,
                            'category': category,
                            'type': 'extreme_outliers',
                            'count': len(extreme_outliers),
                            'outliers': [
                                {'iteration': i, 'time': t, 'z_score': z}
                                for i, t, z in extreme_outliers
                            ],
                            'mean': mean,
                            'stdev': stdev
                        })

                    # Detect high variability (CV > 50%)
                    cv = (stdev / mean * 100) if mean > 0 else 0
                    if cv > 50:
                        anomalies.append({
                            'algorithm': algorithm,
                            'language': language,
                            'category': category,
                            'type': 'high_variability',
                            'coefficient_of_variation': cv,
                            'mean': mean,
                            'stdev': stdev
                        })

        return anomalies

    def compare_with_baseline(
        self,
        results: Dict[str, Any],
        baseline_run_id: str
    ) -> Dict[str, Any]:
        """
        Compare current results with a specific baseline run

        Args:
            results: Current benchmark results
            baseline_run_id: Run ID to use as baseline

        Returns:
            Comparison results
        """
        baseline_results = self.db.get_latest_benchmarks(baseline_run_id)

        if not baseline_results:
            return {'error': 'Baseline run not found'}

        comparisons = []

        for category, algorithms in results.items():
            for algorithm, languages in algorithms.items():
                for language, data in languages.items():
                    if 'error' in data:
                        continue

                    # Find baseline data
                    baseline_data = None
                    if category in baseline_results:
                        if algorithm in baseline_results[category]:
                            if language in baseline_results[category][algorithm]:
                                baseline_data = baseline_results[category][algorithm][language]

                    if not baseline_data:
                        continue

                    current_time = data['avg_time_ms']
                    baseline_time = baseline_data['avg_time_ms']

                    percent_change = ((current_time - baseline_time) / baseline_time) * 100

                    comparisons.append({
                        'algorithm': algorithm,
                        'language': language,
                        'category': category,
                        'baseline_time': baseline_time,
                        'current_time': current_time,
                        'percent_change': percent_change,
                        'status': 'regression' if percent_change > 10 else
                                 'improvement' if percent_change < -10 else 'stable'
                    })

        return {
            'baseline_run_id': baseline_run_id,
            'comparisons': comparisons,
            'summary': {
                'total_compared': len(comparisons),
                'regressions': sum(1 for c in comparisons if c['status'] == 'regression'),
                'improvements': sum(1 for c in comparisons if c['status'] == 'improvement'),
                'stable': sum(1 for c in comparisons if c['status'] == 'stable')
            }
        }
