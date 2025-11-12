"""
Benchmark Report Generator - Multi-Format Report Creation

This module generates comprehensive benchmark reports in multiple formats
including HTML, Markdown, and JSON. Reports include charts, tables, and
detailed analysis.

Features:
- HTML reports with embedded charts
- Markdown reports for documentation
- JSON export for programmatic access
- Performance charts and visualizations
- Historical comparison views
- Executive summary generation
- Customizable templates

Usage:
    generator = ReportGenerator(db_path="benchmarks/data/benchmark_results.db")
    generator.generate_report(format='html', output='report.html')

@author Algorithms Multiverse
@version 1.0
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from benchmarks.framework.analyzer import BenchmarkAnalyzer


class ReportGenerator:
    """
    Multi-format benchmark report generator

    Generates comprehensive reports with analysis, charts, and insights.
    """

    def __init__(
        self,
        db_path: str = "benchmarks/data/benchmark_results.db",
        config_path: str = "benchmarks/config/config.yaml"
    ):
        """Initialize report generator"""
        self.analyzer = BenchmarkAnalyzer(db_path, config_path)
        self.db_path = db_path

    def generate_report(
        self,
        format: str = 'html',
        output_file: str = None,
        include_charts: bool = True
    ) -> str:
        """
        Generate comprehensive benchmark report

        Args:
            format: Output format ('html', 'markdown', 'json')
            output_file: Output file path (auto-generated if None)
            include_charts: Include visualizations

        Returns:
            Path to generated report
        """
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"benchmarks/results/report_{timestamp}.{format}"

        # Generate analysis data
        summary = self.analyzer.generate_summary_report()
        regressions = self.analyzer.detect_regressions()

        if format == 'html':
            content = self._generate_html_report(summary, regressions, include_charts)
        elif format == 'markdown':
            content = self._generate_markdown_report(summary, regressions)
        elif format == 'json':
            content = json.dumps({
                'summary': summary,
                'regressions': [r.__dict__ for r in regressions]
            }, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")

        # Write report
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Report generated: {output_file}")
        return output_file

    def _generate_html_report(
        self,
        summary: Dict,
        regressions: List,
        include_charts: bool
    ) -> str:
        """Generate HTML report"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Benchmark Report - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}

        h2 {{
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #ecf0f1;
        }}

        h3 {{
            color: #7f8c8d;
            margin-top: 20px;
            margin-bottom: 10px;
        }}

        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}

        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .stat-card h3 {{
            color: rgba(255,255,255,0.9);
            font-size: 14px;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .stat-value {{
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .stat-label {{
            font-size: 12px;
            opacity: 0.9;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
        }}

        th {{
            background: #34495e;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #ecf0f1;
        }}

        tr:hover {{
            background: #f8f9fa;
        }}

        .regression {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}

        .regression.severe {{
            background: #f8d7da;
            border-left-color: #dc3545;
        }}

        .regression.moderate {{
            background: #fff3cd;
            border-left-color: #ff9800;
        }}

        .regression.minor {{
            background: #d1ecf1;
            border-left-color: #17a2b8;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }}

        .badge.success {{
            background: #d4edda;
            color: #155724;
        }}

        .badge.warning {{
            background: #fff3cd;
            color: #856404;
        }}

        .badge.danger {{
            background: #f8d7da;
            color: #721c24;
        }}

        .meta-info {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
            font-size: 14px;
            color: #6c757d;
        }}

        .chart-container {{
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}

        footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Benchmark Performance Report</h1>

        <div class="meta-info">
            <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
            <strong>Period:</strong> Last {summary.get('data_period_days', 30)} days |
            <strong>Database:</strong> {Path(self.db_path).name}
        </div>

        <h2>📊 Executive Summary</h2>

        <div class="summary-grid">
            <div class="stat-card">
                <h3>Total Runs</h3>
                <div class="stat-value">{summary['overall_statistics'].get('total_runs', 0):,}</div>
                <div class="stat-label">Benchmark executions</div>
            </div>

            <div class="stat-card">
                <h3>Algorithms Tested</h3>
                <div class="stat-value">{summary['overall_statistics'].get('unique_algorithms', 0)}</div>
                <div class="stat-label">Unique implementations</div>
            </div>

            <div class="stat-card">
                <h3>Languages</h3>
                <div class="stat-value">{summary['overall_statistics'].get('languages_tested', 0)}</div>
                <div class="stat-label">Programming languages</div>
            </div>

            <div class="stat-card">
                <h3>Success Rate</h3>
                <div class="stat-value">
                    {(summary['overall_statistics'].get('successful_runs', 0) / max(summary['overall_statistics'].get('total_runs', 1), 1) * 100):.1f}%
                </div>
                <div class="stat-label">Successful executions</div>
            </div>
        </div>

        <h2>🌐 Language Performance Overview</h2>

        <table>
            <thead>
                <tr>
                    <th>Language</th>
                    <th>Runs</th>
                    <th>Avg Time (s)</th>
                    <th>Avg Memory (MB)</th>
                    <th>Performance</th>
                </tr>
            </thead>
            <tbody>
"""

        # Language performance rows
        for lang_stat in summary.get('language_performance', []):
            avg_time = lang_stat.get('avg_time', 0)
            performance_class = 'success' if avg_time < 1 else ('warning' if avg_time < 5 else 'danger')

            html += f"""
                <tr>
                    <td><strong>{lang_stat['language']}</strong></td>
                    <td>{lang_stat['runs']}</td>
                    <td>{avg_time:.4f}</td>
                    <td>{lang_stat.get('avg_memory', 0):.2f}</td>
                    <td><span class="badge {performance_class}">
                        {'Fast' if avg_time < 1 else ('Moderate' if avg_time < 5 else 'Slow')}
                    </span></td>
                </tr>
"""

        html += """
            </tbody>
        </table>
"""

        # Regressions section
        html += f"""
        <h2>⚠️ Performance Regressions</h2>

        <p>Found <strong>{len(regressions)}</strong> potential regressions in recent benchmarks.</p>
"""

        if regressions:
            for reg in regressions[:10]:  # Show top 10
                html += f"""
        <div class="regression {reg.severity}">
            <h3>{reg.algorithm} ({reg.language})</h3>
            <p>
                <strong>Metric:</strong> {reg.metric.title()} |
                <strong>Change:</strong> <span style="color: #dc3545;">{reg.change_percent:+.1f}%</span> |
                <strong>Severity:</strong> <span class="badge {reg.severity}">{reg.severity.upper()}</span>
            </p>
            <p>
                <strong>Baseline:</strong> {reg.baseline_value:.4f} |
                <strong>Current:</strong> {reg.current_value:.4f} |
                <strong>Input Size:</strong> {reg.input_size}
            </p>
        </div>
"""
        else:
            html += """
        <div class="meta-info">
            ✅ No significant performance regressions detected in the analyzed period.
        </div>
"""

        # Chart placeholder
        if include_charts:
            html += """
        <h2>📈 Performance Trends</h2>

        <div class="chart-container">
            <p><em>Note: Interactive charts can be viewed in the web interface at
            <code>benchmarks/web/interface.html</code></em></p>
        </div>
"""

        html += f"""
        <footer>
            <p>Generated by Algorithms Multiverse Benchmark Framework</p>
            <p>For detailed analysis, use the web interface or run the analyzer CLI</p>
        </footer>
    </div>
</body>
</html>
"""

        return html

    def _generate_markdown_report(
        self,
        summary: Dict,
        regressions: List
    ) -> str:
        """Generate Markdown report"""
        md = f"""# Benchmark Performance Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Period:** Last {summary.get('data_period_days', 30)} days
**Database:** {Path(self.db_path).name}

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Runs | {summary['overall_statistics'].get('total_runs', 0):,} |
| Unique Algorithms | {summary['overall_statistics'].get('unique_algorithms', 0)} |
| Languages Tested | {summary['overall_statistics'].get('languages_tested', 0)} |
| Successful Runs | {summary['overall_statistics'].get('successful_runs', 0)} |
| Success Rate | {(summary['overall_statistics'].get('successful_runs', 0) / max(summary['overall_statistics'].get('total_runs', 1), 1) * 100):.1f}% |
| Avg Execution Time | {summary['overall_statistics'].get('avg_execution_time', 0):.4f}s |
| Avg Memory Usage | {summary['overall_statistics'].get('avg_memory_usage', 0):.2f} MB |

---

## Language Performance Overview

| Language | Runs | Avg Time (s) | Avg Memory (MB) |
|----------|------|-------------|----------------|
"""

        for lang_stat in summary.get('language_performance', []):
            md += f"| {lang_stat['language']} | {lang_stat['runs']} | {lang_stat.get('avg_time', 0):.4f} | {lang_stat.get('avg_memory', 0):.2f} |\n"

        md += f"""
---

## Performance Regressions

**Found {len(regressions)} potential regressions**

"""

        if regressions:
            for i, reg in enumerate(regressions[:10], 1):
                md += f"""
### {i}. {reg.algorithm} ({reg.language})

- **Metric:** {reg.metric.title()}
- **Severity:** {reg.severity.upper()}
- **Change:** {reg.change_percent:+.1f}%
- **Baseline:** {reg.baseline_value:.4f}
- **Current:** {reg.current_value:.4f}
- **Input Size:** {reg.input_size}

"""
        else:
            md += "✅ No significant performance regressions detected.\n\n"

        md += """
---

## Recommendations

1. Review any regressions marked as SEVERE or MODERATE
2. Check for recent code changes that might explain performance degradation
3. Consider running extensive benchmarks for affected algorithms
4. Update baselines if intentional changes were made

---

*Generated by Algorithms Multiverse Benchmark Framework*
"""

        return md

    def generate_comparison_report(
        self,
        algorithm: str,
        output_file: str = None
    ) -> str:
        """Generate cross-language comparison report for specific algorithm"""
        comparison = self.analyzer.compare_languages(algorithm, 1000)

        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"benchmarks/results/comparison_{algorithm}_{timestamp}.html"

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Language Comparison: {algorithm}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1000px; margin: 40px auto; padding: 20px; }}
        h1 {{ color: #2c3e50; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #34495e; color: white; }}
        .fastest {{ background-color: #d4edda; }}
    </style>
</head>
<body>
    <h1>Language Performance Comparison: {algorithm}</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

    <h2>Performance Rankings</h2>
    <table>
        <tr>
            <th>Rank</th>
            <th>Language</th>
            <th>Mean Time (s)</th>
            <th>Std Dev (s)</th>
            <th>Memory (MB)</th>
            <th>Samples</th>
        </tr>
"""

        sorted_langs = sorted(comparison.items(), key=lambda x: x[1].mean_time)

        for rank, (lang, metrics) in enumerate(sorted_langs, 1):
            row_class = ' class="fastest"' if rank == 1 else ''
            html += f"""
        <tr{row_class}>
            <td>{rank}</td>
            <td><strong>{lang}</strong></td>
            <td>{metrics.mean_time:.4f}</td>
            <td>{metrics.std_dev_time:.4f}</td>
            <td>{metrics.mean_memory:.2f}</td>
            <td>{metrics.sample_count}</td>
        </tr>
"""

        html += """
    </table>
</body>
</html>
"""

        with open(output_file, 'w') as f:
            f.write(html)

        print(f"Comparison report generated: {output_file}")
        return output_file

    def close(self):
        """Clean up resources"""
        self.analyzer.close()


def main():
    """Main entry point for report generator"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Benchmark Report Generator"
    )
    parser.add_argument(
        '--format',
        choices=['html', 'markdown', 'json'],
        default='html',
        help='Output format'
    )
    parser.add_argument(
        '--output',
        help='Output file path'
    )
    parser.add_argument(
        '--comparison',
        help='Generate comparison report for specific algorithm'
    )
    parser.add_argument(
        '--no-charts',
        action='store_true',
        help='Exclude charts from report'
    )

    args = parser.parse_args()

    generator = ReportGenerator()

    try:
        if args.comparison:
            generator.generate_comparison_report(args.comparison, args.output)
        else:
            generator.generate_report(
                format=args.format,
                output_file=args.output,
                include_charts=not args.no_charts
            )
    finally:
        generator.close()


if __name__ == '__main__':
    main()
