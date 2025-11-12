"""
Recommendation Engine - Generates algorithm selection recommendations
"""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Generates intelligent recommendations for algorithm selection"""

    def __init__(self):
        # Complexity characteristics for common algorithms
        self.complexity_data = {
            'quicksort': {'time': 'O(n log n)', 'space': 'O(log n)', 'stable': False},
            'mergesort': {'time': 'O(n log n)', 'space': 'O(n)', 'stable': True},
            'heapsort': {'time': 'O(n log n)', 'space': 'O(1)', 'stable': False},
            'bubblesort': {'time': 'O(n²)', 'space': 'O(1)', 'stable': True},
            'insertionsort': {'time': 'O(n²)', 'space': 'O(1)', 'stable': True},
            'selectionsort': {'time': 'O(n²)', 'space': 'O(1)', 'stable': False},
            'binarysearch': {'time': 'O(log n)', 'space': 'O(1)', 'sorted_required': True},
            'linearsearch': {'time': 'O(n)', 'space': 'O(1)', 'sorted_required': False},
            'bfs': {'time': 'O(V + E)', 'space': 'O(V)', 'weighted': False},
            'dfs': {'time': 'O(V + E)', 'space': 'O(V)', 'weighted': False},
            'dijkstra': {'time': 'O((V + E) log V)', 'space': 'O(V)', 'weighted': True},
        }

    def generate_recommendations(
        self,
        benchmark_results: Dict[str, Any],
        statistical_analysis: Dict[str, Any],
        trends: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive recommendations

        Args:
            benchmark_results: Raw benchmark data
            statistical_analysis: Statistical analysis results
            trends: Trend analysis results

        Returns:
            Dictionary containing recommendations
        """
        recommendations = {
            'algorithm_selection': self._recommend_algorithms(
                benchmark_results,
                statistical_analysis
            ),
            'language_selection': self._recommend_languages(
                benchmark_results,
                statistical_analysis
            ),
            'optimization_opportunities': self._identify_optimizations(
                benchmark_results,
                trends
            ),
            'stability_concerns': self._identify_stability_issues(
                statistical_analysis
            ),
            'best_practices': self._generate_best_practices(
                benchmark_results,
                statistical_analysis
            )
        }

        return recommendations

    def _recommend_algorithms(
        self,
        results: Dict[str, Any],
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Recommend best algorithms for different scenarios"""
        recommendations = []

        # Group by category
        for category, algorithms in results.items():
            category_perf = {}

            for algorithm, languages in algorithms.items():
                # Get best performance across all languages
                valid_results = [
                    data for data in languages.values()
                    if 'error' not in data
                ]

                if not valid_results:
                    continue

                best_time = min(r['avg_time_ms'] for r in valid_results)
                avg_time = sum(r['avg_time_ms'] for r in valid_results) / len(valid_results)

                category_perf[algorithm] = {
                    'best_time': best_time,
                    'avg_time': avg_time,
                    'implementations': len(valid_results)
                }

            # Sort by performance
            sorted_algorithms = sorted(
                category_perf.items(),
                key=lambda x: x[1]['best_time']
            )

            if len(sorted_algorithms) >= 2:
                best = sorted_algorithms[0]
                worst = sorted_algorithms[-1]

                speedup = worst[1]['best_time'] / best[1]['best_time']

                recommendations.append({
                    'category': category,
                    'recommended': best[0],
                    'reason': f'Best performance: {best[1]["best_time"]:.2f}ms',
                    'avoid': worst[0] if speedup > 10 else None,
                    'avoid_reason': f'{speedup:.1f}x slower than best option' if speedup > 10 else None,
                    'alternatives': [alg for alg, _ in sorted_algorithms[1:3]],
                    'complexity': self.complexity_data.get(best[0].lower().replace(' ', ''), {})
                })

        return recommendations

    def _recommend_languages(
        self,
        results: Dict[str, Any],
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Recommend best languages for performance"""
        language_scores = {}

        # Collect performance data across all algorithms
        for category, algorithms in results.items():
            for algorithm, languages in algorithms.items():
                for language, data in languages.items():
                    if 'error' in data:
                        continue

                    if language not in language_scores:
                        language_scores[language] = {
                            'total_time': 0,
                            'count': 0,
                            'wins': 0  # Number of times this language was fastest
                        }

                    language_scores[language]['total_time'] += data['avg_time_ms']
                    language_scores[language]['count'] += 1

                # Check if this language was fastest for this algorithm
                valid_times = {
                    lang: data['avg_time_ms']
                    for lang, data in languages.items()
                    if 'error' not in data
                }

                if valid_times:
                    fastest_lang = min(valid_times, key=valid_times.get)
                    language_scores[fastest_lang]['wins'] += 1

        # Calculate average performance
        language_rankings = []
        for language, scores in language_scores.items():
            avg_time = scores['total_time'] / scores['count']
            win_rate = scores['wins'] / scores['count'] * 100

            language_rankings.append({
                'language': language,
                'avg_time_ms': avg_time,
                'benchmarks': scores['count'],
                'wins': scores['wins'],
                'win_rate': win_rate
            })

        # Sort by average time
        language_rankings.sort(key=lambda x: x['avg_time_ms'])

        return {
            'rankings': language_rankings,
            'fastest_overall': language_rankings[0]['language'] if language_rankings else None,
            'most_consistent': max(language_rankings, key=lambda x: x['win_rate'])['language'] if language_rankings else None,
            'recommendation': self._generate_language_recommendation(language_rankings)
        }

    def _generate_language_recommendation(self, rankings: List[Dict[str, Any]]) -> str:
        """Generate human-readable language recommendation"""
        if not rankings:
            return "Insufficient data for recommendation"

        fastest = rankings[0]
        most_consistent = max(rankings, key=lambda x: x['win_rate'])

        if fastest['language'] == most_consistent['language']:
            return (
                f"✓ RECOMMENDED: {fastest['language']} - "
                f"Best overall performance with {fastest['win_rate']:.0f}% win rate"
            )
        else:
            return (
                f"✓ RECOMMENDED: {fastest['language']} for raw speed "
                f"({fastest['avg_time_ms']:.2f}ms avg), "
                f"{most_consistent['language']} for consistency "
                f"({most_consistent['win_rate']:.0f}% win rate)"
            )

    def _identify_optimizations(
        self,
        results: Dict[str, Any],
        trends: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify optimization opportunities"""
        opportunities = []

        # Check for regressions
        if 'regressions' in trends and trends['regressions']:
            for regression in trends['regressions']:
                opportunities.append({
                    'type': 'regression',
                    'priority': 'high' if regression['percent_change'] > 25 else 'medium',
                    'algorithm': regression['algorithm'],
                    'language': regression['language'],
                    'issue': f"Performance degraded by {regression['percent_change']:.1f}%",
                    'recommendation': "Review recent changes and profile for bottlenecks"
                })

        # Check for high variability
        for category, algorithms in results.items():
            for algorithm, languages in algorithms.items():
                for language, data in languages.items():
                    if 'error' in data or 'stdev_time_ms' not in data:
                        continue

                    # High coefficient of variation suggests instability
                    cv = (data['stdev_time_ms'] / data['avg_time_ms'] * 100) if data['avg_time_ms'] > 0 else 0

                    if cv > 30:
                        opportunities.append({
                            'type': 'variability',
                            'priority': 'medium',
                            'algorithm': algorithm,
                            'language': language,
                            'issue': f"High performance variability (CV: {cv:.1f}%)",
                            'recommendation': "Check for external factors affecting performance or optimize hot paths"
                        })

        return opportunities

    def _identify_stability_issues(
        self,
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify stability and reliability issues"""
        issues = []

        # Check outliers
        if 'outliers' in analysis:
            for key, outlier_data in analysis['outliers'].items():
                if outlier_data['percentage'] > 10:  # More than 10% outliers
                    parts = key.split('/')
                    issues.append({
                        'type': 'outliers',
                        'severity': 'medium',
                        'algorithm': parts[1] if len(parts) > 1 else 'unknown',
                        'language': parts[2] if len(parts) > 2 else 'unknown',
                        'issue': f"{outlier_data['percentage']:.1f}% of measurements are outliers",
                        'recommendation': "Investigate environmental factors or algorithm implementation"
                    })

        return issues

    def _generate_best_practices(
        self,
        results: Dict[str, Any],
        analysis: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Generate best practices based on analysis"""
        practices = []

        # Performance-based practices
        if 'summary' in analysis:
            fastest = analysis['summary'].get('fastest_overall')
            if fastest:
                practices.append({
                    'category': 'Performance',
                    'practice': f"Use {fastest['algorithm']} ({fastest['language']}) for optimal performance in {fastest['category']}",
                    'impact': 'high'
                })

        # General best practices
        practices.extend([
            {
                'category': 'Algorithm Selection',
                'practice': 'Choose algorithms based on input characteristics (size, distribution, constraints)',
                'impact': 'high'
            },
            {
                'category': 'Language Selection',
                'practice': 'Use compiled languages (C++, Rust) for performance-critical code',
                'impact': 'high'
            },
            {
                'category': 'Memory Management',
                'practice': 'Consider memory-time tradeoffs, especially for large datasets',
                'impact': 'medium'
            },
            {
                'category': 'Testing',
                'practice': 'Run benchmarks multiple times to account for variability',
                'impact': 'medium'
            },
            {
                'category': 'Monitoring',
                'practice': 'Track performance trends to detect regressions early',
                'impact': 'high'
            }
        ])

        return practices

    def recommend_for_use_case(
        self,
        use_case: Dict[str, Any],
        results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Recommend algorithms for specific use case

        Args:
            use_case: Dictionary describing the use case
                     {input_size, memory_constraint, stability_required, etc.}
            results: Benchmark results

        Returns:
            Tailored recommendations
        """
        input_size = use_case.get('input_size', 1000)
        memory_limited = use_case.get('memory_limited', False)
        stability_required = use_case.get('stability_required', False)
        category = use_case.get('category', 'sorting')

        recommendations = []

        if category not in results:
            return {'error': f'No data for category: {category}'}

        for algorithm, languages in results[category].items():
            complexity = self.complexity_data.get(algorithm.lower().replace(' ', ''), {})

            # Filter based on requirements
            if stability_required and not complexity.get('stable', False):
                continue

            # Score algorithm
            score = 0
            reasons = []

            # Performance score
            valid_times = [
                data['avg_time_ms'] for data in languages.values()
                if 'error' not in data
            ]

            if valid_times:
                avg_time = sum(valid_times) / len(valid_times)
                score += 100 / (avg_time + 1)  # Lower time = higher score
                reasons.append(f"Avg time: {avg_time:.2f}ms")

            # Memory score (if we have memory data)
            if memory_limited and 'space' in complexity:
                if 'O(1)' in complexity['space']:
                    score += 20
                    reasons.append("Constant space complexity")
                elif 'O(log n)' in complexity['space']:
                    score += 10
                    reasons.append("Logarithmic space complexity")

            recommendations.append({
                'algorithm': algorithm,
                'score': score,
                'reasons': reasons,
                'complexity': complexity
            })

        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)

        return {
            'use_case': use_case,
            'recommendations': recommendations[:5],  # Top 5
            'best_choice': recommendations[0] if recommendations else None
        }
