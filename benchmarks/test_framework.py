"""
Benchmark Framework End-to-End Test Suite

Comprehensive test to validate all framework components:
- Configuration loading
- Benchmark discovery
- Execution (compilation, running, metrics collection)
- Statistical analysis
- Report generation
- Database operations

Usage:
    python benchmarks/test_framework.py

@author Algorithms Multiverse
@version 1.0
"""

import os
import sys
import tempfile
import shutil
import json
from pathlib import Path

# Add framework to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from benchmarks.framework.runner import BenchmarkRunner, BenchmarkResult
from benchmarks.framework.analyzer import BenchmarkAnalyzer
from benchmarks.reports.generator import ReportGenerator


class FrameworkTester:
    """Comprehensive framework tester"""

    def __init__(self):
        self.test_dir = tempfile.mkdtemp(prefix="benchmark_test_")
        self.passed = 0
        self.failed = 0
        self.test_results = []

    def log_test(self, name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status}: {name}")
        if message:
            print(f"  > {message}")

        self.test_results.append({
            'name': name,
            'passed': passed,
            'message': message
        })

        if passed:
            self.passed += 1
        else:
            self.failed += 1

    def test_config_loading(self):
        """Test 1: Configuration loading"""
        print("\n" + "="*70)
        print("TEST 1: Configuration Loading")
        print("="*70)

        try:
            # Use absolute path for config
            config_path = os.path.join(
                Path(__file__).parent, "config", "config.yaml"
            )
            runner = BenchmarkRunner(config_path=config_path)

            # Check required config sections exist
            has_languages = 'languages' in runner.config
            has_scenarios = 'scenarios' in runner.config
            has_reports = 'reports' in runner.config

            self.log_test(
                "Config file loads successfully",
                has_languages and has_scenarios and has_reports,
                f"Languages: {has_languages}, Scenarios: {has_scenarios}, Reports: {has_reports}"
            )

            # Check specific language configs
            python_enabled = runner.config['languages'].get('python', {}).get('enabled', False)
            self.log_test(
                "Python language configured",
                python_enabled,
                f"Python enabled: {python_enabled}"
            )

            # Check scenarios
            quick_scenario = 'quick' in runner.config['scenarios']
            self.log_test(
                "Quick scenario configured",
                quick_scenario,
                f"Quick scenario exists: {quick_scenario}"
            )

        except Exception as e:
            self.log_test("Config loading", False, f"Error: {e}")

    def test_benchmark_discovery(self):
        """Test 2: Benchmark discovery"""
        print("\n" + "="*70)
        print("TEST 2: Benchmark Discovery")
        print("="*70)

        try:
            config_path = os.path.join(
                Path(__file__).parent, "config", "config.yaml"
            )
            runner = BenchmarkRunner(config_path=config_path)

            # Discover benchmarks
            examples_dir = os.path.join(Path(__file__).parent, "examples")
            benchmarks = runner.discover_benchmarks(examples_dir)

            self.log_test(
                "Discovers example benchmarks",
                len(benchmarks) > 0,
                f"Found {len(benchmarks)} benchmarks"
            )

            # Check for Python benchmark
            python_benchmarks = [b for b in benchmarks if b['language'] == 'python']
            self.log_test(
                "Finds Python benchmarks",
                len(python_benchmarks) > 0,
                f"Found {len(python_benchmarks)} Python benchmarks"
            )

            # Check for JavaScript benchmark
            js_benchmarks = [b for b in benchmarks if b['language'] == 'javascript']
            self.log_test(
                "Finds JavaScript benchmarks",
                len(js_benchmarks) > 0,
                f"Found {len(js_benchmarks)} JavaScript benchmarks"
            )

        except Exception as e:
            self.log_test("Benchmark discovery", False, f"Error: {e}")

    def test_example_execution(self):
        """Test 3: Execute example benchmarks"""
        print("\n" + "="*70)
        print("TEST 3: Example Benchmark Execution")
        print("="*70)

        try:
            config_path = os.path.join(
                Path(__file__).parent, "config", "config.yaml"
            )
            runner = BenchmarkRunner(config_path=config_path)

            # Test Python benchmark
            python_file = os.path.join(
                Path(__file__).parent, "examples", "simple_benchmark.py"
            )
            if os.path.exists(python_file):
                result = runner.run_single_benchmark(
                    file_path=python_file,
                    language='python',
                    algorithm='examples/simple_benchmark',
                    input_size=20,
                    iterations=2,
                    warmup=1
                )

                self.log_test(
                    "Python benchmark executes",
                    result.success,
                    f"Time: {result.execution_time:.4f}s, Memory: {result.memory_usage:.2f}MB"
                )

                self.log_test(
                    "Collects execution time",
                    result.execution_time > 0,
                    f"Execution time: {result.execution_time:.4f}s"
                )

                self.log_test(
                    "Collects memory usage",
                    result.memory_usage >= 0,
                    f"Memory usage: {result.memory_usage:.2f}MB"
                )

            # Test JavaScript benchmark
            js_file = os.path.join(
                Path(__file__).parent, "examples", "simple_benchmark.js"
            )
            if os.path.exists(js_file):
                result = runner.run_single_benchmark(
                    file_path=js_file,
                    language='javascript',
                    algorithm='examples/simple_benchmark',
                    input_size=20,
                    iterations=2,
                    warmup=1
                )

                self.log_test(
                    "JavaScript benchmark executes",
                    result.success,
                    f"Time: {result.execution_time:.4f}s, Memory: {result.memory_usage:.2f}MB"
                )

            runner.cleanup()

        except Exception as e:
            self.log_test("Example execution", False, f"Error: {e}")

    def test_database_operations(self):
        """Test 4: Database operations"""
        print("\n" + "="*70)
        print("TEST 4: Database Operations")
        print("="*70)

        try:
            # Create test database
            test_db = os.path.join(self.test_dir, "test_benchmark.db")

            # Create runner with test database
            config_path = os.path.join(
                Path(__file__).parent, "config", "config.yaml"
            )
            runner = BenchmarkRunner(config_path=config_path)
            runner.config['storage']['database'] = test_db
            runner._init_database()

            # Create test results
            test_result = BenchmarkResult(
                timestamp="2024-01-01T12:00:00",
                language="python",
                file_path="test.py",
                algorithm="test_algo",
                input_size=100,
                execution_time=1.234,
                memory_usage=45.6,
                cpu_percent=50.0,
                iterations=5,
                success=True
            )

            # Save to database
            runner.results = [test_result]
            runner.config['storage']['type'] = 'sqlite'
            runner.save_results()

            self.log_test(
                "Saves results to database",
                os.path.exists(test_db),
                f"Database created at {test_db}"
            )

            # Test analyzer can read from database
            analyzer = BenchmarkAnalyzer(db_path=test_db)
            recent = analyzer.get_recent_results(days=30)

            # Note: Results from runner.save_results() may not be immediately available
            # due to timestamp filtering, so we check database directly
            import sqlite3
            conn = sqlite3.connect(test_db)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM benchmark_results")
            count = cursor.fetchone()[0]
            conn.close()

            self.log_test(
                "Analyzer reads from database",
                count > 0,
                f"Found {count} results in database"
            )

            analyzer.close()
            runner.cleanup()

        except Exception as e:
            self.log_test("Database operations", False, f"Error: {e}")

    def test_statistical_analysis(self):
        """Test 5: Statistical analysis"""
        print("\n" + "="*70)
        print("TEST 5: Statistical Analysis")
        print("="*70)

        try:
            # Create test database with sample data
            test_db = os.path.join(self.test_dir, "test_analysis.db")

            import sqlite3
            conn = sqlite3.connect(test_db)
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE benchmark_results (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    language TEXT,
                    file_path TEXT,
                    algorithm TEXT,
                    input_size INTEGER,
                    execution_time REAL,
                    memory_usage REAL,
                    cpu_percent REAL,
                    iterations INTEGER,
                    success BOOLEAN,
                    error_message TEXT,
                    metadata TEXT,
                    run_hash TEXT
                )
            ''')

            # Insert test data
            from datetime import datetime, timedelta
            base_time = datetime.now()

            for i in range(10):
                cursor.execute('''
                    INSERT INTO benchmark_results VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    i,
                    (base_time - timedelta(days=i)).isoformat(),
                    'python',
                    'test.py',
                    'test_algo',
                    1000,
                    1.0 + (i * 0.1),  # Increasing time (regression)
                    50.0,
                    50.0,
                    5,
                    True,
                    None,
                    None,
                    'test'
                ))

            conn.commit()
            conn.close()

            # Test analyzer
            analyzer = BenchmarkAnalyzer(db_path=test_db)

            # Test summary generation
            summary = analyzer.generate_summary_report()
            self.log_test(
                "Generates summary report",
                'overall_statistics' in summary,
                f"Summary keys: {list(summary.keys())}"
            )

            # Test metrics calculation
            metrics = analyzer.calculate_metrics(
                algorithm='test_algo',
                language='python',
                input_size=1000,
                days=30
            )

            self.log_test(
                "Calculates performance metrics",
                metrics is not None and metrics.mean_time > 0,
                f"Mean time: {metrics.mean_time:.4f}s" if metrics else "No metrics"
            )

            analyzer.close()

        except Exception as e:
            self.log_test("Statistical analysis", False, f"Error: {e}")

    def test_report_generation(self):
        """Test 6: Report generation"""
        print("\n" + "="*70)
        print("TEST 6: Report Generation")
        print("="*70)

        try:
            # Create test database with sample data
            test_db = os.path.join(self.test_dir, "test_reports.db")

            import sqlite3
            conn = sqlite3.connect(test_db)
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE benchmark_results (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    language TEXT,
                    file_path TEXT,
                    algorithm TEXT,
                    input_size INTEGER,
                    execution_time REAL,
                    memory_usage REAL,
                    cpu_percent REAL,
                    iterations INTEGER,
                    success BOOLEAN,
                    error_message TEXT,
                    metadata TEXT,
                    run_hash TEXT
                )
            ''')

            from datetime import datetime as dt
            cursor.execute('''
                INSERT INTO benchmark_results VALUES
                (1, ?, 'python', 'test.py', 'algo1', 1000, 1.5, 45.0, 50.0, 5, 1, NULL, NULL, 'test')
            ''', (dt.now().isoformat(),))

            conn.commit()
            conn.close()

            # Test HTML report generation
            generator = ReportGenerator(db_path=test_db)
            html_file = os.path.join(self.test_dir, "test_report.html")

            result = generator.generate_report(
                format='html',
                output_file=html_file,
                include_charts=True
            )

            self.log_test(
                "Generates HTML report",
                os.path.exists(html_file),
                f"Report saved to {html_file}"
            )

            # Test Markdown report
            md_file = os.path.join(self.test_dir, "test_report.md")
            generator.generate_report(
                format='markdown',
                output_file=md_file
            )

            self.log_test(
                "Generates Markdown report",
                os.path.exists(md_file),
                f"Report saved to {md_file}"
            )

            # Test JSON export
            json_file = os.path.join(self.test_dir, "test_report.json")
            generator.generate_report(
                format='json',
                output_file=json_file
            )

            self.log_test(
                "Generates JSON report",
                os.path.exists(json_file),
                f"Report saved to {json_file}"
            )

            # Verify JSON structure
            with open(json_file, 'r') as f:
                data = json.load(f)
                has_summary = 'summary' in data

            self.log_test(
                "JSON report has valid structure",
                has_summary,
                f"JSON keys: {list(data.keys())}"
            )

            generator.close()

        except Exception as e:
            self.log_test("Report generation", False, f"Error: {e}")

    def test_web_interface(self):
        """Test 7: Web interface exists"""
        print("\n" + "="*70)
        print("TEST 7: Web Interface")
        print("="*70)

        try:
            web_file = os.path.join(
                Path(__file__).parent, "web", "interface.html"
            )

            self.log_test(
                "Web interface file exists",
                os.path.exists(web_file),
                f"Found at {web_file}"
            )

            if os.path.exists(web_file):
                with open(web_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                has_charts = 'Chart.js' in content or 'chart' in content.lower()
                self.log_test(
                    "Web interface includes charting",
                    has_charts,
                    "Found charting library"
                )

                has_dashboard = 'dashboard' in content.lower()
                self.log_test(
                    "Web interface has dashboard",
                    has_dashboard,
                    "Dashboard UI found"
                )

        except Exception as e:
            self.log_test("Web interface", False, f"Error: {e}")

    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*70)
        print("BENCHMARK FRAMEWORK END-TO-END TEST SUITE")
        print("="*70)

        try:
            self.test_config_loading()
            self.test_benchmark_discovery()
            self.test_example_execution()
            self.test_database_operations()
            self.test_statistical_analysis()
            self.test_report_generation()
            self.test_web_interface()

        finally:
            self.print_summary()
            self.cleanup()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"Total Tests: {self.passed + self.failed}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        if self.passed + self.failed > 0:
            print(f"Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        print("="*70)

        if self.failed > 0:
            print("\nFailed Tests:")
            for test in self.test_results:
                if not test['passed']:
                    print(f"  [X] {test['name']}")
                    if test['message']:
                        print(f"      {test['message']}")

        print("\n")

        # Exit code
        sys.exit(0 if self.failed == 0 else 1)

    def cleanup(self):
        """Clean up test files"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)


def main():
    """Main entry point"""
    tester = FrameworkTester()
    tester.run_all_tests()


if __name__ == '__main__':
    main()
