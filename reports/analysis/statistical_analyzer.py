"""
Statistical Analyzer - Performs statistical analysis on benchmark data
"""

import statistics
import numpy as np
from typing import Dict, List, Any
from scipy import stats
import logging

logger = logging.getLogger(__name__)


class StatisticalAnalyzer:
    """Performs comprehensive statistical analysis on performance data"""

    def analyze(self, benchmark_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform complete statistical analysis

        Args:
            benchmark_results: Raw benchmark results

        Returns:
            Statistical analysis results
        """
        analysis = {
            'summary': self._generate_summary(benchmark_results),
            'distributions': self._analyze_distributions(benchmark_results),
            'comparisons': self._compare_implementations(benchmark_results),
            'outliers': self._detect_outliers(benchmark_results),
            'confidence_intervals': self._calculate_confidence_intervals(benchmark_results)
        }

        return analysis

    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics"""
        summary = {
            'total_benchmarks': 0,
            'total_languages': set(),
            'total_algorithms': 0,
            'fastest_overall': None,
            'slowest_overall': None
        }

        fastest = {'time': float('inf')}
        slowest = {'time': 0}

        for category, algorithms in results.items():
            for algorithm, languages in algorithms.items():
                summary['total_algorithms'] += 1

                for language, data in languages.items():
                    if 'error' in data:
                        continue

                    summary['total_benchmarks'] += 1
                    summary['total_languages'].add(language)

                    avg_time = data['avg_time_ms']

                    if avg_time < fastest['time']:
                        fastest = {
                            'time': avg_time,
                            'algorithm': algorithm,
                            'language': language,
                            'category': category
                        }

                    if avg_time > slowest['time']:
                        slowest = {
                            'time': avg_time,
                            'algorithm': algorithm,
                            'language': language,
                            'category': category
                        }

        summary['fastest_overall'] = fastest
        summary['slowest_overall'] = slowest
        summary['total_languages'] = len(summary['total_languages'])

        return summary

    def _analyze_distributions(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze execution time distributions"""
        distributions = {}

        for category, algorithms in results.items():
            for algorithm, languages in algorithms.items():
                for language, data in languages.items():
                    if 'error' in data or 'times_ms' not in data:
                        continue

                    times = data['times_ms']
                    key = f"{category}/{algorithm}/{language}"

                    # Perform normality test
                    if len(times) >= 8:
                        stat, p_value = stats.shapiro(times)
                        is_normal = p_value > 0.05
                    else:
                        is_normal = None

                    distributions[key] = {
                        'mean': statistics.mean(times),
                        'median': statistics.median(times),
                        'mode': statistics.mode(times) if len(set(times)) < len(times) else None,
                        'stdev': statistics.stdev(times) if len(times) > 1 else 0,
                        'variance': statistics.variance(times) if len(times) > 1 else 0,
                        'skewness': stats.skew(times),
                        'kurtosis': stats.kurtosis(times),
                        'is_normal_distribution': is_normal,
                        'percentiles': {
                            '25': np.percentile(times, 25),
                            '50': np.percentile(times, 50),
                            '75': np.percentile(times, 75),
                            '95': np.percentile(times, 95),
                            '99': np.percentile(times, 99)
                        }
                    }

        return distributions

    def _compare_implementations(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Compare implementations of same algorithm across languages"""
        comparisons = {}

        for category, algorithms in results.items():
            for algorithm, languages in algorithms.items():
                # Get all valid implementations
                valid_langs = {
                    lang: data for lang, data in languages.items()
                    if 'error' not in data
                }

                if len(valid_langs) < 2:
                    continue

                # Find fastest and slowest
                sorted_langs = sorted(
                    valid_langs.items(),
                    key=lambda x: x[1]['avg_time_ms']
                )

                fastest_lang, fastest_data = sorted_langs[0]
                slowest_lang, slowest_data = sorted_langs[-1]

                # Calculate speedup factors
                speedups = {}
                for lang, data in valid_langs.items():
                    speedup = data['avg_time_ms'] / fastest_data['avg_time_ms']
                    speedups[lang] = speedup

                comparisons[f"{category}/{algorithm}"] = {
                    'languages_tested': list(valid_langs.keys()),
                    'fastest': {
                        'language': fastest_lang,
                        'avg_time_ms': fastest_data['avg_time_ms']
                    },
                    'slowest': {
                        'language': slowest_lang,
                        'avg_time_ms': slowest_data['avg_time_ms']
                    },
                    'speedup_factor': slowest_data['avg_time_ms'] / fastest_data['avg_time_ms'],
                    'speedups': speedups,
                    'all_times': {lang: data['avg_time_ms'] for lang, data in valid_langs.items()}
                }

        return comparisons

    def _detect_outliers(self, results: Dict[str, Any]) -> Dict[str, List[Any]]:
        """Detect outliers using IQR method"""
        outliers = {}

        for category, algorithms in results.items():
            for algorithm, languages in algorithms.items():
                for language, data in languages.items():
                    if 'error' in data or 'times_ms' not in data:
                        continue

                    times = data['times_ms']
                    q1 = np.percentile(times, 25)
                    q3 = np.percentile(times, 75)
                    iqr = q3 - q1

                    lower_bound = q1 - 1.5 * iqr
                    upper_bound = q3 + 1.5 * iqr

                    detected_outliers = [
                        t for t in times if t < lower_bound or t > upper_bound
                    ]

                    if detected_outliers:
                        key = f"{category}/{algorithm}/{language}"
                        outliers[key] = {
                            'outliers': detected_outliers,
                            'count': len(detected_outliers),
                            'percentage': len(detected_outliers) / len(times) * 100,
                            'bounds': {'lower': lower_bound, 'upper': upper_bound}
                        }

        return outliers

    def _calculate_confidence_intervals(
        self,
        results: Dict[str, Any],
        confidence=0.95
    ) -> Dict[str, Any]:
        """Calculate confidence intervals for execution times"""
        intervals = {}

        for category, algorithms in results.items():
            for algorithm, languages in algorithms.items():
                for language, data in languages.items():
                    if 'error' in data or 'times_ms' not in data:
                        continue

                    times = data['times_ms']
                    mean = statistics.mean(times)
                    std_err = statistics.stdev(times) / np.sqrt(len(times))

                    # Calculate confidence interval
                    ci = stats.t.interval(
                        confidence,
                        len(times) - 1,
                        loc=mean,
                        scale=std_err
                    )

                    key = f"{category}/{algorithm}/{language}"
                    intervals[key] = {
                        'mean': mean,
                        'confidence_level': confidence,
                        'lower_bound': ci[0],
                        'upper_bound': ci[1],
                        'margin_of_error': ci[1] - mean
                    }

        return intervals

    def compare_languages(self, results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Compare performance across languages for a single algorithm"""
        if not results:
            return {}

        # Calculate relative performance
        times = {lang: data['avg_time_ms'] for lang, data in results.items() if 'error' not in data}

        if not times:
            return {}

        fastest_time = min(times.values())

        return {
            'absolute_times': times,
            'relative_to_fastest': {
                lang: time / fastest_time
                for lang, time in times.items()
            },
            'fastest_language': min(times, key=times.get),
            'slowest_language': max(times, key=times.get),
            'speed_difference': max(times.values()) / min(times.values())
        }

    def analyze_scalability(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how performance scales with input size"""
        if len(results) < 2:
            return {}

        sizes = [r['input_size'] for r in results]
        times = [r['avg_time_ms'] for r in results]

        # Fit to different complexity curves
        log_n = np.log(sizes)
        n_log_n = np.array(sizes) * np.log(sizes)

        fits = {}

        # O(n) fit
        slope, intercept, r_value, _, _ = stats.linregress(sizes, times)
        fits['O(n)'] = {
            'r_squared': r_value ** 2,
            'formula': f'{slope:.4f}n + {intercept:.4f}'
        }

        # O(log n) fit
        slope, intercept, r_value, _, _ = stats.linregress(log_n, times)
        fits['O(log n)'] = {
            'r_squared': r_value ** 2,
            'formula': f'{slope:.4f}log(n) + {intercept:.4f}'
        }

        # O(n log n) fit
        slope, intercept, r_value, _, _ = stats.linregress(n_log_n, times)
        fits['O(n log n)'] = {
            'r_squared': r_value ** 2,
            'formula': f'{slope:.4f}n*log(n) + {intercept:.4f}'
        }

        # O(n²) fit
        sizes_squared = [s ** 2 for s in sizes]
        slope, intercept, r_value, _, _ = stats.linregress(sizes_squared, times)
        fits['O(n²)'] = {
            'r_squared': r_value ** 2,
            'formula': f'{slope:.4f}n² + {intercept:.4f}'
        }

        # Find best fit
        best_fit = max(fits, key=lambda k: fits[k]['r_squared'])

        return {
            'input_sizes': sizes,
            'execution_times': times,
            'fits': fits,
            'best_fit_complexity': best_fit,
            'best_fit_r_squared': fits[best_fit]['r_squared']
        }
