"""
Benchmark Runner - Cross-Language Performance Testing Framework

This module provides the core benchmark execution engine that can run
performance tests across multiple programming languages, collect metrics,
and store results for analysis.

Features:
- Multi-language support with automatic detection
- Time and memory profiling
- Warmup and multiple iterations
- Compilation handling for compiled languages
- Parallel execution support
- Error handling and timeout management
- Result persistence

Usage:
    runner = BenchmarkRunner(config_path="benchmarks/config/config.yaml")
    results = runner.run_benchmark_suite(scenario="standard")
    runner.save_results(results)

@author Algorithms Multiverse
@version 1.0
"""

import os
import sys
import time
import subprocess
import psutil
import yaml
import json
import sqlite3
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import tempfile
import shutil
import traceback


@dataclass
class BenchmarkResult:
    """Container for benchmark execution results"""
    timestamp: str
    language: str
    file_path: str
    algorithm: str
    input_size: int
    execution_time: float  # seconds
    memory_usage: float  # MB
    cpu_percent: float
    iterations: int
    success: bool
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BenchmarkRunner:
    """
    Main benchmark execution engine

    Handles execution of benchmarks across multiple languages with
    comprehensive performance metrics collection.
    """

    def __init__(self, config_path: str = "benchmarks/config/config.yaml"):
        """Initialize the benchmark runner with configuration"""
        self.config_path = config_path
        self.config = self._load_config()
        self.results: List[BenchmarkResult] = []
        self.temp_dir = tempfile.mkdtemp(prefix="benchmark_")

        # Create necessary directories
        os.makedirs(self.config['reports']['output_dir'], exist_ok=True)
        os.makedirs(os.path.dirname(self.config['storage']['database']), exist_ok=True)

        # Initialize database
        self._init_database()

    def _load_config(self) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: Config file not found at {self.config_path}")
            return self._default_config()

    def _default_config(self) -> Dict:
        """Return default configuration if file not found"""
        return {
            'languages': {
                'python': {'enabled': True, 'command': 'python', 'timeout': 300},
                'javascript': {'enabled': True, 'command': 'node', 'timeout': 300},
            },
            'scenarios': {
                'quick': {'iterations': 3, 'warmup': 1, 'input_sizes': [10, 100]}
            },
            'reports': {'output_dir': 'benchmarks/results'},
            'storage': {'type': 'sqlite', 'database': 'benchmarks/data/benchmark_results.db'}
        }

    def _init_database(self):
        """Initialize SQLite database for storing results"""
        if self.config['storage']['type'] != 'sqlite':
            return

        db_path = self.config['storage']['database']
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS benchmark_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                language TEXT NOT NULL,
                file_path TEXT NOT NULL,
                algorithm TEXT NOT NULL,
                input_size INTEGER NOT NULL,
                execution_time REAL NOT NULL,
                memory_usage REAL NOT NULL,
                cpu_percent REAL,
                iterations INTEGER NOT NULL,
                success BOOLEAN NOT NULL,
                error_message TEXT,
                metadata TEXT,
                run_hash TEXT
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp ON benchmark_results(timestamp)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_language ON benchmark_results(language)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_algorithm ON benchmark_results(algorithm)
        ''')

        conn.commit()
        conn.close()

    def discover_benchmarks(self, root_dir: str = ".") -> List[Dict[str, str]]:
        """
        Discover all benchmark files in the repository

        Returns:
            List of dictionaries containing file path, language, and algorithm info
        """
        benchmarks = []

        for lang_name, lang_config in self.config['languages'].items():
            if not lang_config.get('enabled', True):
                continue

            extensions = lang_config.get('extensions', [])

            for ext in extensions:
                for file_path in Path(root_dir).rglob(f"*{ext}"):
                    # Skip test files, build artifacts, etc.
                    if any(skip in str(file_path) for skip in
                          ['test', '__pycache__', 'node_modules', 'target', 'build']):
                        continue

                    benchmarks.append({
                        'language': lang_name,
                        'file_path': str(file_path),
                        'algorithm': self._extract_algorithm_name(file_path)
                    })

        return benchmarks

    def _extract_algorithm_name(self, file_path: Path) -> str:
        """Extract algorithm name from file path"""
        # Get the parent directory and filename
        parent = file_path.parent.name
        filename = file_path.stem

        # Combine for a meaningful name
        if parent and parent != '.':
            return f"{parent}/{filename}"
        return filename

    def compile_if_needed(self, file_path: str, language: str) -> Optional[str]:
        """
        Compile source file if language requires compilation

        Returns:
            Path to executable or None if no compilation needed
        """
        lang_config = self.config['languages'][language]

        if 'compile' not in lang_config:
            return None  # Interpreted language

        compile_cmd = lang_config['compile']
        file_path_obj = Path(file_path)

        # Generate output path
        output_name = file_path_obj.stem
        if sys.platform == 'win32':
            output_path = os.path.join(self.temp_dir, f"{output_name}.exe")
        else:
            output_path = os.path.join(self.temp_dir, output_name)

        # Build compilation command as argument list
        if language == 'java':
            # Java special case
            cmd = [*compile_cmd.split(), file_path]
        else:
            cmd = [*compile_cmd.split(), output_path, file_path]

        if language == 'c':
            cmd.append("-lm")  # Link math library for C

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                print(f"Compilation failed for {file_path}")
                print(f"Error: {result.stderr}")
                return None

            if language == 'java':
                return file_path_obj.stem  # Return class name for Java

            return output_path

        except subprocess.TimeoutExpired:
            print(f"Compilation timeout for {file_path}")
            return None
        except Exception as e:
            print(f"Compilation error for {file_path}: {e}")
            return None

    def measure_execution(
        self,
        command: list,
        timeout: int,
        input_size: Optional[int] = None
    ) -> Tuple[float, float, float, bool, Optional[str]]:
        """
        Execute command and measure performance metrics

        Returns:
            Tuple of (execution_time, memory_usage, cpu_percent, success, error_message)
        """
        try:
            start_time = time.time()

            # Start process
            process = psutil.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Monitor process
            max_memory = 0
            cpu_samples = []

            try:
                while process.is_running():
                    try:
                        mem_info = process.memory_info()
                        max_memory = max(max_memory, mem_info.rss / 1024 / 1024)  # MB

                        cpu_percent = process.cpu_percent(interval=0.1)
                        cpu_samples.append(cpu_percent)

                        # Check timeout
                        if time.time() - start_time > timeout:
                            process.kill()
                            return 0, 0, 0, False, "Timeout exceeded"
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        break

                # Wait for completion
                stdout, stderr = process.communicate(timeout=5)
                execution_time = time.time() - start_time

                avg_cpu = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0

                success = process.returncode == 0
                error_msg = stderr.decode() if not success else None

                return execution_time, max_memory, avg_cpu, success, error_msg

            except subprocess.TimeoutExpired:
                process.kill()
                return 0, 0, 0, False, "Process timeout"

        except Exception as e:
            return 0, 0, 0, False, str(e)

    def run_single_benchmark(
        self,
        file_path: str,
        language: str,
        algorithm: str,
        input_size: int,
        iterations: int,
        warmup: int = 0
    ) -> BenchmarkResult:
        """
        Run a single benchmark with multiple iterations

        Args:
            file_path: Path to source file
            language: Programming language
            algorithm: Algorithm name
            input_size: Input size for scaling tests
            iterations: Number of iterations to run
            warmup: Number of warmup iterations

        Returns:
            BenchmarkResult with averaged metrics
        """
        print(f"Running {algorithm} ({language}) with input size {input_size}...")

        lang_config = self.config['languages'][language]
        timeout = lang_config.get('timeout', 300)

        # Compile if needed
        compiled_path = self.compile_if_needed(file_path, language)
        if language in ['c', 'cpp', 'rust'] and compiled_path is None:
            return BenchmarkResult(
                timestamp=datetime.now().isoformat(),
                language=language,
                file_path=file_path,
                algorithm=algorithm,
                input_size=input_size,
                execution_time=0,
                memory_usage=0,
                cpu_percent=0,
                iterations=0,
                success=False,
                error_message="Compilation failed"
            )

        # Build execution command
        if language == 'java':
            cmd = ["java", "-cp", str(Path(file_path).parent), compiled_path]
        elif compiled_path:
            cmd = [compiled_path]
        else:
            cmd = [*lang_config['command'].split(), file_path]

        # Add input size argument if needed
        if input_size:
            cmd.append(str(input_size))

        # Warmup runs
        for _ in range(warmup):
            self.measure_execution(cmd, timeout, input_size)

        # Actual benchmark runs
        times = []
        memories = []
        cpus = []
        errors = []

        for i in range(iterations):
            exec_time, memory, cpu, success, error = self.measure_execution(
                cmd, timeout, input_size
            )

            if success:
                times.append(exec_time)
                memories.append(memory)
                cpus.append(cpu)
            else:
                errors.append(error)

        # Calculate averages
        if times:
            avg_time = sum(times) / len(times)
            avg_memory = sum(memories) / len(memories)
            avg_cpu = sum(cpus) / len(cpus)
            success = True
            error_msg = None
        else:
            avg_time = 0
            avg_memory = 0
            avg_cpu = 0
            success = False
            error_msg = "; ".join(errors) if errors else "All iterations failed"

        return BenchmarkResult(
            timestamp=datetime.now().isoformat(),
            language=language,
            file_path=file_path,
            algorithm=algorithm,
            input_size=input_size,
            execution_time=avg_time,
            memory_usage=avg_memory,
            cpu_percent=avg_cpu,
            iterations=len(times),
            success=success,
            error_message=error_msg
        )

    def run_benchmark_suite(
        self,
        scenario: str = "standard",
        filter_language: Optional[str] = None,
        filter_algorithm: Optional[str] = None
    ) -> List[BenchmarkResult]:
        """
        Run complete benchmark suite based on scenario

        Args:
            scenario: Scenario name from config (quick, standard, extensive)
            filter_language: Only run benchmarks for specific language
            filter_algorithm: Only run specific algorithm

        Returns:
            List of BenchmarkResult objects
        """
        scenario_config = self.config['scenarios'].get(scenario, {})
        if not scenario_config:
            print(f"Unknown scenario: {scenario}")
            return []

        print(f"\n{'='*70}")
        print(f"Running Benchmark Suite: {scenario}")
        print(f"Description: {scenario_config.get('description', 'N/A')}")
        print(f"{'='*70}\n")

        iterations = scenario_config.get('iterations', 10)
        warmup = scenario_config.get('warmup', 3)
        input_sizes = scenario_config.get('input_sizes', [100])

        # Discover benchmarks
        benchmarks = self.discover_benchmarks()

        # Apply filters
        if filter_language:
            benchmarks = [b for b in benchmarks if b['language'] == filter_language]

        if filter_algorithm:
            benchmarks = [b for b in benchmarks if filter_algorithm in b['algorithm']]

        print(f"Found {len(benchmarks)} benchmarks to run\n")

        results = []

        for benchmark in benchmarks:
            for input_size in input_sizes:
                try:
                    result = self.run_single_benchmark(
                        file_path=benchmark['file_path'],
                        language=benchmark['language'],
                        algorithm=benchmark['algorithm'],
                        input_size=input_size,
                        iterations=iterations,
                        warmup=warmup
                    )

                    results.append(result)
                    self._print_result(result)

                except Exception as e:
                    print(f"Error running benchmark {benchmark['algorithm']}: {e}")
                    traceback.print_exc()

        self.results = results
        return results

    def _print_result(self, result: BenchmarkResult):
        """Print a single benchmark result"""
        status = "✓" if result.success else "✗"
        print(f"{status} {result.algorithm:40s} "
              f"| {result.language:10s} "
              f"| Size: {result.input_size:6d} "
              f"| Time: {result.execution_time:8.4f}s "
              f"| Memory: {result.memory_usage:8.2f} MB")

    def save_results(self, results: Optional[List[BenchmarkResult]] = None):
        """Save results to database and JSON"""
        if results is None:
            results = self.results

        if not results:
            print("No results to save")
            return

        # Generate run hash for grouping
        run_hash = hashlib.md5(
            datetime.now().isoformat().encode()
        ).hexdigest()[:8]

        # Save to database
        if self.config['storage']['type'] == 'sqlite':
            self._save_to_database(results, run_hash)

        # Save to JSON
        self._save_to_json(results, run_hash)

        print(f"\nResults saved with run hash: {run_hash}")

    def _save_to_database(self, results: List[BenchmarkResult], run_hash: str):
        """Save results to SQLite database"""
        db_path = self.config['storage']['database']
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        for result in results:
            cursor.execute('''
                INSERT INTO benchmark_results
                (timestamp, language, file_path, algorithm, input_size,
                 execution_time, memory_usage, cpu_percent, iterations,
                 success, error_message, metadata, run_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                result.timestamp,
                result.language,
                result.file_path,
                result.algorithm,
                result.input_size,
                result.execution_time,
                result.memory_usage,
                result.cpu_percent,
                result.iterations,
                result.success,
                result.error_message,
                json.dumps(result.metadata) if result.metadata else None,
                run_hash
            ))

        conn.commit()
        conn.close()

    def _save_to_json(self, results: List[BenchmarkResult], run_hash: str):
        """Save results to JSON file"""
        output_dir = self.config['reports']['output_dir']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(output_dir, f"benchmark_{timestamp}_{run_hash}.json")

        data = {
            'run_hash': run_hash,
            'timestamp': datetime.now().isoformat(),
            'results': [asdict(r) for r in results]
        }

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"JSON results saved to: {output_file}")

    def cleanup(self):
        """Clean up temporary files"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


def main():
    """Main entry point for benchmark runner"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Cross-Language Benchmark Runner"
    )
    parser.add_argument(
        '--scenario',
        default='standard',
        choices=['quick', 'standard', 'extensive', 'memory'],
        help='Benchmark scenario to run'
    )
    parser.add_argument(
        '--language',
        help='Filter by specific language'
    )
    parser.add_argument(
        '--algorithm',
        help='Filter by specific algorithm'
    )
    parser.add_argument(
        '--config',
        default='benchmarks/config/config.yaml',
        help='Path to configuration file'
    )

    args = parser.parse_args()

    # Run benchmarks
    runner = BenchmarkRunner(config_path=args.config)

    try:
        results = runner.run_benchmark_suite(
            scenario=args.scenario,
            filter_language=args.language,
            filter_algorithm=args.algorithm
        )

        runner.save_results(results)

        # Print summary
        print(f"\n{'='*70}")
        print("Benchmark Summary")
        print(f"{'='*70}")
        print(f"Total benchmarks run: {len(results)}")
        print(f"Successful: {sum(1 for r in results if r.success)}")
        print(f"Failed: {sum(1 for r in results if not r.success)}")
        print(f"{'='*70}\n")

    finally:
        runner.cleanup()


if __name__ == '__main__':
    main()
