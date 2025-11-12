"""
Markdown Generator - Creates Markdown summary reports
"""

from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MarkdownGenerator:
    """Generates Markdown format performance summaries"""

    def generate(self, results: Dict[str, Any], output_dir: Path) -> Path:
        """
        Generate Markdown summary report

        Args:
            results: Analysis results
            output_dir: Output directory

        Returns:
            Path to generated Markdown file
        """
        output_path = output_dir / 'summary.md'

        markdown = self._build_markdown(results)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        logger.info(f"Generated Markdown summary: {output_path}")
        return output_path

    def _build_markdown(self, results: Dict[str, Any]) -> str:
        """Build complete Markdown document"""
        sections = [
            self._header(results),
            self._summary_section(results),
            self._top_performers_section(results),
            self._regressions_section(results),
            self._recommendations_section(results),
            self._details_section(results)
        ]

        return '\n\n'.join(sections)

    def _header(self, results: Dict[str, Any]) -> str:
        """Generate header section"""
        timestamp = datetime.fromisoformat(results['timestamp'])
        date_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        return f"""# Performance Analysis Report

**Run ID:** `{results['run_id']}`
**Date:** {date_str}
**Categories:** {', '.join(results['benchmarks'].keys())}"""

    def _summary_section(self, results: Dict[str, Any]) -> str:
        """Generate summary statistics section"""
        stats = results['statistics']['summary']

        # Count total algorithms
        total_algorithms = sum(
            len(algorithms)
            for algorithms in results['benchmarks'].values()
        )

        # Count successful benchmarks
        successful = 0
        failed = 0
        for category in results['benchmarks'].values():
            for algorithms in category.values():
                for data in algorithms.values():
                    if 'error' in data:
                        failed += 1
                    else:
                        successful += 1

        md = f"""## Summary

- **Total Algorithms:** {total_algorithms}
- **Total Benchmarks:** {stats['total_benchmarks']}
- **Languages Tested:** {stats['total_languages']}
- **Successful:** {successful}
- **Failed:** {failed}"""

        # Fastest overall
        if stats['fastest_overall'] and stats['fastest_overall']['time'] != float('inf'):
            fastest = stats['fastest_overall']
            md += f"\n- **Fastest Overall:** {fastest['algorithm']} ({fastest['language']}) - {fastest['time']:.2f}ms"

        # Regressions
        if 'trends' in results:
            regression_count = results['trends']['summary']['total_regressions']
            improvement_count = results['trends']['summary']['total_improvements']

            if regression_count > 0:
                md += f"\n- **⚠️ Regressions Detected:** {regression_count}"
            if improvement_count > 0:
                md += f"\n- **✓ Improvements Detected:** {improvement_count}"

        return md

    def _top_performers_section(self, results: Dict[str, Any]) -> str:
        """Generate top performers section"""
        md = "## Top Performers\n\n"

        # Get comparisons from statistical analysis
        if 'comparisons' in results['statistics']:
            comparisons = results['statistics']['comparisons']

            # Sort by speedup factor
            sorted_comparisons = sorted(
                comparisons.items(),
                key=lambda x: x[1]['fastest']['avg_time_ms']
            )[:10]  # Top 10

            if sorted_comparisons:
                md += "| Rank | Algorithm | Language | Avg Time | Category |\n"
                md += "|------|-----------|----------|----------|----------|\n"

                for rank, (key, data) in enumerate(sorted_comparisons, 1):
                    parts = key.split('/')
                    category = parts[0] if parts else 'N/A'
                    algorithm = parts[1] if len(parts) > 1 else 'N/A'

                    fastest = data['fastest']
                    md += f"| {rank} | {algorithm} | {fastest['language']} | {fastest['avg_time_ms']:.2f}ms | {category} |\n"
            else:
                md += "*No comparison data available*\n"
        else:
            md += "*No comparison data available*\n"

        return md

    def _regressions_section(self, results: Dict[str, Any]) -> str:
        """Generate regressions section"""
        if 'trends' not in results:
            return ""

        trends = results['trends']
        regressions = trends.get('regressions', [])

        if not regressions:
            return "## Performance Trends\n\n✓ No performance regressions detected"

        md = "## ⚠️ Performance Regressions\n\n"
        md += "| Algorithm | Language | Regression | Baseline | Current |\n"
        md += "|-----------|----------|------------|----------|----------|\n"

        for reg in regressions:
            md += f"| {reg['algorithm']} | {reg['language']} | "
            md += f"{reg['percent_change']:.1f}% slower | "
            md += f"{reg['baseline']:.2f}ms | {reg['current']:.2f}ms |\n"

        # Improvements
        improvements = trends.get('improvements', [])
        if improvements:
            md += "\n## ✓ Performance Improvements\n\n"
            md += "| Algorithm | Language | Improvement | Baseline | Current |\n"
            md += "|-----------|----------|-------------|----------|----------|\n"

            for imp in improvements:
                md += f"| {imp['algorithm']} | {imp['language']} | "
                md += f"{imp['improvement_percent']:.1f}% faster | "
                md += f"{imp['baseline']:.2f}ms | {imp['current']:.2f}ms |\n"

        return md

    def _recommendations_section(self, results: Dict[str, Any]) -> str:
        """Generate recommendations section"""
        if 'recommendations' not in results:
            return ""

        recommendations = results['recommendations']

        md = "## Recommendations\n\n"

        # Algorithm recommendations
        if 'algorithm_selection' in recommendations:
            algo_recs = recommendations['algorithm_selection']

            if algo_recs:
                md += "### Algorithm Selection\n\n"

                for rec in algo_recs[:5]:  # Top 5
                    md += f"**{rec['category']}:**\n"
                    md += f"- ✓ Recommended: **{rec['recommended']}** - {rec['reason']}\n"

                    if rec.get('avoid'):
                        md += f"- ⚠️ Avoid: **{rec['avoid']}** - {rec['avoid_reason']}\n"

                    if rec.get('alternatives'):
                        md += f"- Alternatives: {', '.join(rec['alternatives'])}\n"

                    md += "\n"

        # Language recommendations
        if 'language_selection' in recommendations:
            lang_rec = recommendations['language_selection']

            if 'recommendation' in lang_rec:
                md += "### Language Selection\n\n"
                md += f"{lang_rec['recommendation']}\n\n"

                if 'rankings' in lang_rec:
                    md += "**Performance Rankings:**\n\n"
                    md += "| Rank | Language | Avg Time | Win Rate |\n"
                    md += "|------|----------|----------|----------|\n"

                    for rank, lang_data in enumerate(lang_rec['rankings'][:5], 1):
                        md += f"| {rank} | {lang_data['language']} | "
                        md += f"{lang_data['avg_time_ms']:.2f}ms | "
                        md += f"{lang_data['win_rate']:.0f}% |\n"

                    md += "\n"

        # Best practices
        if 'best_practices' in recommendations:
            practices = recommendations['best_practices']

            if practices:
                md += "### Best Practices\n\n"

                for practice in practices[:5]:
                    md += f"- **{practice['category']}:** {practice['practice']}\n"

        return md

    def _details_section(self, results: Dict[str, Any]) -> str:
        """Generate detailed results section"""
        md = "## Detailed Results\n\n"

        for category, algorithms in results['benchmarks'].items():
            md += f"### {category.replace('-', ' ').title()}\n\n"

            for algorithm, languages in algorithms.items():
                md += f"**{algorithm}:**\n\n"

                # Create table
                md += "| Language | Avg Time | Median | Std Dev | Min | Max |\n"
                md += "|----------|----------|--------|---------|-----|-----|\n"

                for language, data in languages.items():
                    if 'error' in data:
                        md += f"| {language} | Error | - | - | - | - |\n"
                    else:
                        md += f"| {language} | "
                        md += f"{data['avg_time_ms']:.2f}ms | "
                        md += f"{data['median_time_ms']:.2f}ms | "
                        md += f"{data['stdev_time_ms']:.2f}ms | "
                        md += f"{data['min_time_ms']:.2f}ms | "
                        md += f"{data['max_time_ms']:.2f}ms |\n"

                md += "\n"

        return md

    def generate_pr_comment(self, results: Dict[str, Any]) -> str:
        """
        Generate a concise summary suitable for PR comments

        Args:
            results: Analysis results

        Returns:
            Markdown formatted PR comment
        """
        md = "## 📊 Performance Benchmark Results\n\n"

        # Summary
        stats = results['statistics']['summary']
        md += f"**Benchmarks Run:** {stats['total_benchmarks']}  \n"
        md += f"**Languages:** {stats['total_languages']}  \n"

        # Fastest
        if stats['fastest_overall'] and stats['fastest_overall']['time'] != float('inf'):
            fastest = stats['fastest_overall']
            md += f"**⚡ Fastest:** {fastest['algorithm']} ({fastest['language']}) - {fastest['time']:.2f}ms\n\n"

        # Regressions
        if 'trends' in results:
            regressions = results['trends'].get('regressions', [])

            if regressions:
                md += "### ⚠️ Performance Regressions\n\n"
                for reg in regressions[:3]:  # Top 3
                    md += f"- **{reg['algorithm']}** ({reg['language']}): {reg['percent_change']:.1f}% slower\n"
                md += "\n"
            else:
                md += "### ✅ No Performance Regressions\n\n"

            # Improvements
            improvements = results['trends'].get('improvements', [])
            if improvements:
                md += "### 🚀 Performance Improvements\n\n"
                for imp in improvements[:3]:  # Top 3
                    md += f"- **{imp['algorithm']}** ({imp['language']}): {imp['improvement_percent']:.1f}% faster\n"
                md += "\n"

        md += f"\n---\n*Full report: [View Details](reports/output/{results['run_id']}/dashboard.html)*"

        return md
