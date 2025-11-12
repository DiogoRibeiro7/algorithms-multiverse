#!/usr/bin/env python3
"""
Automated Performance Analysis and Reporting System
Generates comprehensive performance reports across all algorithm implementations
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import sqlite3

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from reports.analysis.benchmark_runner import BenchmarkRunner
from reports.analysis.statistical_analyzer import StatisticalAnalyzer
from reports.analysis.trend_detector import TrendDetector
from reports.analysis.memory_profiler import MemoryProfiler
from reports.analysis.recommendation_engine import RecommendationEngine
from reports.dashboard.html_generator import HTMLDashboardGenerator
from reports.dashboard.pdf_generator import PDFReportGenerator
from reports.dashboard.markdown_generator import MarkdownGenerator
from reports.database.performance_db import PerformanceDatabase
from reports.alerts.alert_manager import AlertManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reports/logs/generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PerformanceReportGenerator:
    """
    Main orchestrator for performance analysis and reporting
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the performance report generator

        Args:
            config: Configuration dictionary for the generator
        """
        self.config = config or self._load_default_config()
        self.timestamp = datetime.now()
        self.run_id = self.timestamp.strftime("%Y%m%d_%H%M%S")

        # Initialize components
        self.db = PerformanceDatabase(self.config.get('database_path', 'reports/data/performance.db'))
        self.benchmark_runner = BenchmarkRunner(self.config)
        self.statistical_analyzer = StatisticalAnalyzer()
        self.trend_detector = TrendDetector(self.db)
        self.memory_profiler = MemoryProfiler()
        self.recommendation_engine = RecommendationEngine()
        self.alert_manager = AlertManager(self.config)

        # Report generators
        self.html_generator = HTMLDashboardGenerator(self.config)
        self.pdf_generator = PDFReportGenerator(self.config)
        self.markdown_generator = MarkdownGenerator()

        logger.info(f"Performance Report Generator initialized - Run ID: {self.run_id}")

    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        config_path = Path(__file__).parent / 'config.json'

        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)

        # Default configuration
        return {
            'database_path': 'reports/data/performance.db',
            'output_dir': 'reports/output',
            'benchmark_iterations': 100,
            'input_sizes': [10, 100, 1000, 10000],
            'languages': ['python', 'javascript', 'java', 'cpp', 'go', 'rust'],
            'algorithm_categories': ['sorting', 'searching', 'graph-algorithms', 'dynamic-programming'],
            'regression_threshold': 0.10,  # 10% regression threshold
            'memory_profiling_enabled': True,
            'generate_html': True,
            'generate_pdf': True,
            'generate_markdown': True,
            'generate_json': True,
            'alert_email': None,
            'alert_slack_webhook': None
        }

    def run_full_analysis(self, categories: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Run complete performance analysis pipeline

        Args:
            categories: List of algorithm categories to analyze (default: all)

        Returns:
            Dictionary containing all analysis results
        """
        logger.info("="*80)
        logger.info("Starting Full Performance Analysis")
        logger.info("="*80)

        categories = categories or self.config['algorithm_categories']

        # Phase 1: Execute Benchmarks
        logger.info("\n[Phase 1/6] Executing Benchmarks")
        benchmark_results = self.benchmark_runner.run_all_benchmarks(categories)

        # Phase 2: Statistical Analysis
        logger.info("\n[Phase 2/6] Performing Statistical Analysis")
        statistical_analysis = self.statistical_analyzer.analyze(benchmark_results)

        # Phase 3: Trend Detection
        logger.info("\n[Phase 3/6] Detecting Performance Trends")
        trends = self.trend_detector.detect_trends(benchmark_results)

        # Phase 4: Memory Profiling
        logger.info("\n[Phase 4/6] Profiling Memory Usage")
        memory_profiles = {}
        if self.config.get('memory_profiling_enabled', True):
            memory_profiles = self.memory_profiler.profile_all(categories)

        # Phase 5: Generate Recommendations
        logger.info("\n[Phase 5/6] Generating Recommendations")
        recommendations = self.recommendation_engine.generate_recommendations(
            benchmark_results,
            statistical_analysis,
            trends
        )

        # Compile all results
        analysis_results = {
            'run_id': self.run_id,
            'timestamp': self.timestamp.isoformat(),
            'config': self.config,
            'benchmarks': benchmark_results,
            'statistics': statistical_analysis,
            'trends': trends,
            'memory': memory_profiles,
            'recommendations': recommendations
        }

        # Phase 6: Store Results
        logger.info("\n[Phase 6/6] Storing Results in Database")
        self.db.store_results(analysis_results)

        # Check for regressions and send alerts
        self._check_and_alert_regressions(trends)

        logger.info("\n" + "="*80)
        logger.info("Full Performance Analysis Complete")
        logger.info("="*80)

        return analysis_results

    def generate_reports(self, analysis_results: Dict[str, Any]) -> Dict[str, Path]:
        """
        Generate all configured reports

        Args:
            analysis_results: Results from performance analysis

        Returns:
            Dictionary mapping report type to output file path
        """
        logger.info("\n" + "="*80)
        logger.info("Generating Reports")
        logger.info("="*80)

        output_paths = {}
        output_dir = Path(self.config['output_dir']) / self.run_id
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate JSON data export
        if self.config.get('generate_json', True):
            logger.info("\nGenerating JSON data export...")
            json_path = output_dir / 'performance_data.json'
            with open(json_path, 'w') as f:
                json.dump(analysis_results, f, indent=2, default=str)
            output_paths['json'] = json_path
            logger.info(f"✓ JSON export: {json_path}")

        # Generate HTML dashboard
        if self.config.get('generate_html', True):
            logger.info("\nGenerating HTML dashboard...")
            html_path = self.html_generator.generate(analysis_results, output_dir)
            output_paths['html'] = html_path
            logger.info(f"✓ HTML dashboard: {html_path}")

        # Generate PDF report
        if self.config.get('generate_pdf', True):
            logger.info("\nGenerating PDF report...")
            pdf_path = self.pdf_generator.generate(analysis_results, output_dir)
            output_paths['pdf'] = pdf_path
            logger.info(f"✓ PDF report: {pdf_path}")

        # Generate Markdown summary
        if self.config.get('generate_markdown', True):
            logger.info("\nGenerating Markdown summary...")
            md_path = self.markdown_generator.generate(analysis_results, output_dir)
            output_paths['markdown'] = md_path
            logger.info(f"✓ Markdown summary: {md_path}")

        # Create latest symlink
        latest_link = Path(self.config['output_dir']) / 'latest'
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(output_dir, target_is_directory=True)

        logger.info("\n" + "="*80)
        logger.info(f"All reports generated in: {output_dir}")
        logger.info(f"Latest reports: {latest_link}")
        logger.info("="*80)

        return output_paths

    def _check_and_alert_regressions(self, trends: Dict[str, Any]):
        """
        Check for performance regressions and send alerts

        Args:
            trends: Trend analysis results
        """
        regressions = trends.get('regressions', [])

        if regressions:
            logger.warning(f"\n⚠️  Detected {len(regressions)} performance regression(s)")

            for regression in regressions:
                logger.warning(
                    f"  - {regression['algorithm']} ({regression['language']}): "
                    f"{regression['regression_percent']:.1f}% slower"
                )

            # Send alerts
            if self.config.get('alert_email') or self.config.get('alert_slack_webhook'):
                self.alert_manager.send_regression_alert(regressions, self.run_id)

    def run_quick_benchmark(self, algorithm: str, language: str) -> Dict[str, Any]:
        """
        Run a quick benchmark for a specific algorithm and language

        Args:
            algorithm: Algorithm name (e.g., 'quicksort')
            language: Language name (e.g., 'python')

        Returns:
            Benchmark results
        """
        logger.info(f"Running quick benchmark: {algorithm} ({language})")
        result = self.benchmark_runner.run_single_benchmark(algorithm, language)
        logger.info(f"✓ Completed in {result['total_time']:.2f}s")
        return result

    def compare_implementations(
        self,
        algorithm: str,
        languages: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Compare implementations of the same algorithm across languages

        Args:
            algorithm: Algorithm name
            languages: List of languages to compare (default: all)

        Returns:
            Comparison results
        """
        languages = languages or self.config['languages']
        logger.info(f"Comparing {algorithm} across {len(languages)} languages")

        results = {}
        for lang in languages:
            try:
                results[lang] = self.benchmark_runner.run_single_benchmark(algorithm, lang)
            except Exception as e:
                logger.error(f"Failed to benchmark {algorithm} in {lang}: {e}")

        # Analyze comparison
        comparison = self.statistical_analyzer.compare_languages(results)

        return {
            'algorithm': algorithm,
            'languages': languages,
            'results': results,
            'comparison': comparison
        }

    def analyze_scalability(self, algorithm: str, language: str) -> Dict[str, Any]:
        """
        Analyze how an algorithm scales with input size

        Args:
            algorithm: Algorithm name
            language: Language name

        Returns:
            Scalability analysis results
        """
        logger.info(f"Analyzing scalability: {algorithm} ({language})")

        input_sizes = self.config.get('input_sizes', [10, 100, 1000, 10000])
        results = []

        for size in input_sizes:
            result = self.benchmark_runner.run_with_size(algorithm, language, size)
            results.append(result)

        # Perform scalability analysis
        scalability = self.statistical_analyzer.analyze_scalability(results)

        return {
            'algorithm': algorithm,
            'language': language,
            'input_sizes': input_sizes,
            'results': results,
            'scalability': scalability
        }


def main():
    """Main entry point for the performance report generator"""
    parser = argparse.ArgumentParser(
        description='Automated Performance Analysis and Reporting System'
    )

    parser.add_argument(
        '--mode',
        choices=['full', 'quick', 'compare', 'scalability'],
        default='full',
        help='Analysis mode'
    )

    parser.add_argument(
        '--algorithm',
        help='Specific algorithm to analyze (for quick/compare/scalability modes)'
    )

    parser.add_argument(
        '--language',
        help='Specific language (for quick/scalability modes)'
    )

    parser.add_argument(
        '--languages',
        nargs='+',
        help='Languages to compare (for compare mode)'
    )

    parser.add_argument(
        '--categories',
        nargs='+',
        help='Algorithm categories to analyze (default: all)'
    )

    parser.add_argument(
        '--config',
        type=Path,
        help='Path to configuration file'
    )

    parser.add_argument(
        '--no-reports',
        action='store_true',
        help='Skip report generation (only run analysis)'
    )

    parser.add_argument(
        '--output',
        type=Path,
        help='Custom output directory'
    )

    args = parser.parse_args()

    # Load configuration
    config = None
    if args.config:
        with open(args.config) as f:
            config = json.load(f)

    # Initialize generator
    generator = PerformanceReportGenerator(config)

    # Override output directory if specified
    if args.output:
        generator.config['output_dir'] = str(args.output)

    # Execute based on mode
    try:
        if args.mode == 'full':
            # Full analysis pipeline
            results = generator.run_full_analysis(args.categories)

            if not args.no_reports:
                output_paths = generator.generate_reports(results)
                print("\n" + "="*80)
                print("📊 Reports Generated:")
                print("="*80)
                for report_type, path in output_paths.items():
                    print(f"  {report_type.upper()}: {path}")
                print("="*80)

        elif args.mode == 'quick':
            if not args.algorithm or not args.language:
                parser.error("--algorithm and --language required for quick mode")

            result = generator.run_quick_benchmark(args.algorithm, args.language)
            print(json.dumps(result, indent=2, default=str))

        elif args.mode == 'compare':
            if not args.algorithm:
                parser.error("--algorithm required for compare mode")

            result = generator.compare_implementations(args.algorithm, args.languages)
            print(json.dumps(result, indent=2, default=str))

        elif args.mode == 'scalability':
            if not args.algorithm or not args.language:
                parser.error("--algorithm and --language required for scalability mode")

            result = generator.analyze_scalability(args.algorithm, args.language)
            print(json.dumps(result, indent=2, default=str))

        logger.info("\n✅ Performance analysis completed successfully")
        return 0

    except Exception as e:
        logger.error(f"❌ Performance analysis failed: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
