"""
HTML Dashboard Generator - Creates interactive HTML dashboards with charts
"""

from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


class HTMLDashboardGenerator:
    """Generates interactive HTML dashboards with Plotly charts"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def generate(self, results: Dict[str, Any], output_dir: Path) -> Path:
        """
        Generate HTML dashboard

        Args:
            results: Analysis results
            output_dir: Output directory

        Returns:
            Path to generated HTML file
        """
        output_path = output_dir / 'dashboard.html'

        html = self._build_html(results)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        logger.info(f"Generated HTML dashboard: {output_path}")
        return output_path

    def _build_html(self, results: Dict[str, Any]) -> str:
        """Build complete HTML document"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Performance Analysis Dashboard - {results['run_id']}</title>
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
    <style>
        {self._get_css()}
    </style>
</head>
<body>
    <div class="dashboard">
        {self._header(results)}
        {self._summary_cards(results)}
        {self._charts_section(results)}
        {self._details_section(results)}
    </div>
    <script>
        {self._get_javascript(results)}
    </script>
</body>
</html>"""

    def _get_css(self) -> str:
        """Generate CSS styles"""
        return """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background: #f5f7fa;
    color: #2c3e50;
    line-height: 1.6;
}

.dashboard {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 40px;
    border-radius: 12px;
    margin-bottom: 30px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

header h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
}

header p {
    font-size: 1.1em;
    opacity: 0.9;
}

.summary-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-title {
    font-size: 0.9em;
    color: #7f8c8d;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

.card-value {
    font-size: 2.5em;
    font-weight: bold;
    color: #2c3e50;
}

.card-subtitle {
    font-size: 0.9em;
    color: #95a5a6;
    margin-top: 5px;
}

.card.success .card-value {
    color: #27ae60;
}

.card.warning .card-value {
    color: #f39c12;
}

.card.danger .card-value {
    color: #e74c3c;
}

.section {
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 30px;
}

.section-title {
    font-size: 1.8em;
    margin-bottom: 20px;
    color: #2c3e50;
    border-bottom: 3px solid #667eea;
    padding-bottom: 10px;
}

.chart-container {
    margin-bottom: 40px;
}

.chart-title {
    font-size: 1.3em;
    margin-bottom: 15px;
    color: #34495e;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th, td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ecf0f1;
}

th {
    background: #f8f9fa;
    font-weight: 600;
    color: #2c3e50;
}

tr:hover {
    background: #f8f9fa;
}

.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85em;
    font-weight: 600;
}

.badge-success {
    background: #d4edda;
    color: #155724;
}

.badge-warning {
    background: #fff3cd;
    color: #856404;
}

.badge-danger {
    background: #f8d7da;
    color: #721c24;
}

.badge-info {
    background: #d1ecf1;
    color: #0c5460;
}

@media (max-width: 768px) {
    .dashboard {
        padding: 10px;
    }

    header {
        padding: 20px;
    }

    header h1 {
        font-size: 1.8em;
    }

    .summary-cards {
        grid-template-columns: 1fr;
    }
}
"""

    def _header(self, results: Dict[str, Any]) -> str:
        """Generate header section"""
        timestamp = datetime.fromisoformat(results['timestamp'])
        date_str = timestamp.strftime('%B %d, %Y at %H:%M:%S')

        return f"""
<header>
    <h1>📊 Performance Analysis Dashboard</h1>
    <p><strong>Run ID:</strong> {results['run_id']} | <strong>Date:</strong> {date_str}</p>
    <p><strong>Categories:</strong> {', '.join(results['benchmarks'].keys())}</p>
</header>"""

    def _summary_cards(self, results: Dict[str, Any]) -> str:
        """Generate summary cards"""
        stats = results['statistics']['summary']

        # Count benchmarks
        successful = 0
        failed = 0
        for category in results['benchmarks'].values():
            for algorithms in category.values():
                for data in algorithms.values():
                    if 'error' in data:
                        failed += 1
                    else:
                        successful += 1

        # Get fastest
        fastest_text = "N/A"
        if stats['fastest_overall'] and stats['fastest_overall']['time'] != float('inf'):
            fastest = stats['fastest_overall']
            fastest_text = f"{fastest['algorithm']} ({fastest['language']})"

        # Get regressions
        regression_count = 0
        if 'trends' in results:
            regression_count = results['trends']['summary']['total_regressions']

        card_class = "success" if regression_count == 0 else "danger"

        return f"""
<div class="summary-cards">
    <div class="card">
        <div class="card-title">Total Benchmarks</div>
        <div class="card-value">{stats['total_benchmarks']}</div>
        <div class="card-subtitle">Across {stats['total_languages']} languages</div>
    </div>

    <div class="card success">
        <div class="card-title">Successful</div>
        <div class="card-value">{successful}</div>
        <div class="card-subtitle">{failed} failed</div>
    </div>

    <div class="card {card_class}">
        <div class="card-title">Regressions</div>
        <div class="card-value">{regression_count}</div>
        <div class="card-subtitle">Performance issues</div>
    </div>

    <div class="card">
        <div class="card-title">Fastest Overall</div>
        <div class="card-value" style="font-size: 1.2em;">{fastest_text}</div>
        <div class="card-subtitle">{stats['fastest_overall']['time']:.2f}ms</div>
    </div>
</div>"""

    def _charts_section(self, results: Dict[str, Any]) -> str:
        """Generate charts section"""
        return f"""
<div class="section">
    <h2 class="section-title">📈 Performance Visualizations</h2>

    <div class="chart-container">
        <h3 class="chart-title">Performance Comparison by Algorithm</h3>
        <div id="chart-performance-comparison"></div>
    </div>

    <div class="chart-container">
        <h3 class="chart-title">Language Performance Rankings</h3>
        <div id="chart-language-rankings"></div>
    </div>

    <div class="chart-container">
        <h3 class="chart-title">Performance Distribution</h3>
        <div id="chart-distribution"></div>
    </div>
</div>"""

    def _details_section(self, results: Dict[str, Any]) -> str:
        """Generate detailed results section"""
        html = '<div class="section">\n'
        html += '    <h2 class="section-title">📋 Detailed Results</h2>\n'

        for category, algorithms in results['benchmarks'].items():
            html += f'    <h3>{category.replace("-", " ").title()}</h3>\n'

            for algorithm, languages in algorithms.items():
                html += f'    <h4>{algorithm}</h4>\n'
                html += '    <table>\n'
                html += '        <thead>\n'
                html += '            <tr>\n'
                html += '                <th>Language</th>\n'
                html += '                <th>Avg Time</th>\n'
                html += '                <th>Median</th>\n'
                html += '                <th>Std Dev</th>\n'
                html += '                <th>Min</th>\n'
                html += '                <th>Max</th>\n'
                html += '                <th>Status</th>\n'
                html += '            </tr>\n'
                html += '        </thead>\n'
                html += '        <tbody>\n'

                for language, data in languages.items():
                    if 'error' in data:
                        html += f'            <tr>\n'
                        html += f'                <td><strong>{language}</strong></td>\n'
                        html += f'                <td colspan="5">Error: {data["error"]}</td>\n'
                        html += f'                <td><span class="badge badge-danger">Failed</span></td>\n'
                        html += f'            </tr>\n'
                    else:
                        html += f'            <tr>\n'
                        html += f'                <td><strong>{language}</strong></td>\n'
                        html += f'                <td>{data["avg_time_ms"]:.2f}ms</td>\n'
                        html += f'                <td>{data["median_time_ms"]:.2f}ms</td>\n'
                        html += f'                <td>{data["stdev_time_ms"]:.2f}ms</td>\n'
                        html += f'                <td>{data["min_time_ms"]:.2f}ms</td>\n'
                        html += f'                <td>{data["max_time_ms"]:.2f}ms</td>\n'
                        html += f'                <td><span class="badge badge-success">Success</span></td>\n'
                        html += f'            </tr>\n'

                html += '        </tbody>\n'
                html += '    </table>\n'

        html += '</div>\n'
        return html

    def _get_javascript(self, results: Dict[str, Any]) -> str:
        """Generate JavaScript for charts"""
        # Prepare data for charts
        chart_data = self._prepare_chart_data(results)

        return f"""
// Chart 1: Performance Comparison
const perfData = {json.dumps(chart_data['performance_comparison'])};
const perfLayout = {{
    title: 'Average Execution Time by Algorithm',
    xaxis: {{ title: 'Algorithm' }},
    yaxis: {{ title: 'Time (ms)', type: 'log' }},
    barmode: 'group',
    height: 500
}};
Plotly.newPlot('chart-performance-comparison', perfData, perfLayout);

// Chart 2: Language Rankings
const langData = {json.dumps(chart_data['language_rankings'])};
const langLayout = {{
    title: 'Average Performance by Language',
    xaxis: {{ title: 'Language' }},
    yaxis: {{ title: 'Average Time (ms)' }},
    height: 400
}};
Plotly.newPlot('chart-language-rankings', langData, langLayout);

// Chart 3: Distribution
const distData = {json.dumps(chart_data['distribution'])};
const distLayout = {{
    title: 'Execution Time Distribution',
    xaxis: {{ title: 'Time (ms)' }},
    yaxis: {{ title: 'Frequency' }},
    height: 400
}};
Plotly.newPlot('chart-distribution', distData, distLayout);
"""

    def _prepare_chart_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for charts"""
        # Performance comparison data
        perf_data = []
        languages_seen = set()

        for category, algorithms in results['benchmarks'].items():
            for algorithm, languages in algorithms.items():
                for language, data in languages.items():
                    if 'error' not in data:
                        languages_seen.add(language)

        # Create traces for each language
        for lang in languages_seen:
            x_values = []
            y_values = []

            for category, algorithms in results['benchmarks'].items():
                for algorithm, languages in algorithms.items():
                    if lang in languages and 'error' not in languages[lang]:
                        x_values.append(f"{algorithm}")
                        y_values.append(languages[lang]['avg_time_ms'])

            if x_values:
                perf_data.append({
                    'x': x_values,
                    'y': y_values,
                    'name': lang,
                    'type': 'bar'
                })

        # Language rankings data
        lang_stats = {}
        for category, algorithms in results['benchmarks'].items():
            for algorithm, languages in algorithms.items():
                for language, data in languages.items():
                    if 'error' not in data:
                        if language not in lang_stats:
                            lang_stats[language] = []
                        lang_stats[language].append(data['avg_time_ms'])

        lang_rankings = [{
            'x': list(lang_stats.keys()),
            'y': [sum(times) / len(times) for times in lang_stats.values()],
            'type': 'bar',
            'marker': {'color': '#667eea'}
        }]

        # Distribution data (histogram of all execution times)
        all_times = []
        for category, algorithms in results['benchmarks'].items():
            for algorithm, languages in algorithms.items():
                for language, data in languages.items():
                    if 'error' not in data:
                        all_times.append(data['avg_time_ms'])

        distribution = [{
            'x': all_times,
            'type': 'histogram',
            'marker': {'color': '#764ba2'}
        }]

        return {
            'performance_comparison': perf_data,
            'language_rankings': lang_rankings,
            'distribution': distribution
        }
