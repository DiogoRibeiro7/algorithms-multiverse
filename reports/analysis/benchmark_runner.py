"""
Benchmark Runner - Executes benchmarks across all languages
"""

import subprocess
import time
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import statistics

logger = logging.getLogger(__name__)


class BenchmarkRunner:
    """Executes performance benchmarks across multiple languages"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.root_dir = Path(__file__).parent.parent.parent
        self.benchmark_iterations = config.get('benchmark_iterations', 100)

        # Language-specific execution commands
        self.executors = {
            'python': ['python3', '{file}'],
            'javascript': ['node', '{file}'],
            'java': ['java', '-cp', 'target/classes', '{class}'],
            'cpp': ['./{executable}'],
            'c': ['./{executable}'],
            'go': ['go', 'run', '{file}'],
            'rust': ['cargo', 'run', '--release', '--bin', '{name}'],
            'ruby': ['ruby', '{file}'],
            'typescript': ['ts-node', '{file}']
        }

    def run_all_benchmarks(self, categories: List[str]) -> Dict[str, Any]:
        """
        Run benchmarks for all algorithms in specified categories

        Args:
            categories: List of algorithm categories

        Returns:
            Complete benchmark results
        """
        all_results = {}

        for category in categories:
            logger.info(f"Benchmarking {category}...")
            category_results = self._benchmark_category(category)
            all_results[category] = category_results

        return all_results

    def _benchmark_category(self, category: str) -> Dict[str, Any]:
        """Benchmark all algorithms in a category"""
        category_dir = self.root_dir / category
        if not category_dir.exists():
            logger.warning(f"Category directory not found: {category}")
            return {}

        results = {}
        algorithms = self._discover_algorithms(category_dir)

        for algorithm_name, implementations in algorithms.items():
            logger.info(f"  Benchmarking {algorithm_name}...")
            algorithm_results = {}

            for language, file_path in implementations.items():
                try:
                    result = self._run_benchmark(algorithm_name, language, file_path)
                    algorithm_results[language] = result
                    logger.info(f"    ✓ {language}: {result['avg_time_ms']:.2f}ms")
                except Exception as e:
                    logger.error(f"    ✗ {language}: {e}")
                    algorithm_results[language] = {'error': str(e)}

            results[algorithm_name] = algorithm_results

        return results

    def _discover_algorithms(self, category_dir: Path) -> Dict[str, Dict[str, Path]]:
        """
        Discover algorithms and their implementations

        Returns:
            Dict mapping algorithm name to dict of language -> file path
        """
        algorithms = {}

        # Common algorithm file patterns
        patterns = {
            'python': '*.py',
            'javascript': '*.js',
            'java': '*.java',
            'cpp': '*.cpp',
            'c': '*.c',
            'go': '*.go',
            'rust': '*.rs',
            'ruby': '*.rb',
            'typescript': '*.ts'
        }

        for lang, pattern in patterns.items():
            for file in category_dir.glob(pattern):
                # Extract algorithm name from filename
                algo_name = file.stem.replace('_', ' ').title()

                if algo_name not in algorithms:
                    algorithms[algo_name] = {}

                algorithms[algo_name][lang] = file

        return algorithms

    def _run_benchmark(
        self,
        algorithm: str,
        language: str,
        file_path: Path
    ) -> Dict[str, Any]:
        """
        Execute a single benchmark

        Args:
            algorithm: Algorithm name
            language: Programming language
            file_path: Path to implementation file

        Returns:
            Benchmark results including timing and statistics
        """
        times = []
        memory_usages = []

        # Warm-up run
        self._execute_once(language, file_path)

        # Benchmark runs
        for i in range(self.benchmark_iterations):
            start_time = time.perf_counter()
            result = self._execute_once(language, file_path)
            end_time = time.perf_counter()

            execution_time = (end_time - start_time) * 1000  # Convert to ms
            times.append(execution_time)

            if result and 'memory' in result:
                memory_usages.append(result['memory'])

        # Calculate statistics
        return {
            'algorithm': algorithm,
            'language': language,
            'iterations': self.benchmark_iterations,
            'times_ms': times,
            'avg_time_ms': statistics.mean(times),
            'median_time_ms': statistics.median(times),
            'stdev_time_ms': statistics.stdev(times) if len(times) > 1 else 0,
            'min_time_ms': min(times),
            'max_time_ms': max(times),
            'memory_usages': memory_usages,
            'avg_memory_mb': statistics.mean(memory_usages) if memory_usages else None,
            'input_size': self.config.get('default_input_size', 1000)
        }

    def _execute_once(self, language: str, file_path: Path) -> Optional[Dict[str, Any]]:
        """Execute the algorithm once"""
        if language not in self.executors:
            raise ValueError(f"Unsupported language: {language}")

        # Prepare command
        cmd_template = self.executors[language]
        format_args = {
            "file": str(file_path),
            "executable": file_path.stem,
            "class": file_path.stem,
            "name": file_path.stem,
        }
        cmd = [arg.format_map(format_args) for arg in cmd_template]

        # Execute
        try:
            result = subprocess.run(
                cmd,
                cwd=file_path.parent,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                logger.warning(f"Execution failed: {result.stderr}")
                return None

            # Try to parse JSON output if available
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {'output': result.stdout}

        except subprocess.TimeoutExpired:
            logger.error(f"Execution timeout for {language}: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Execution error: {e}")
            return None

    def run_single_benchmark(self, algorithm: str, language: str) -> Dict[str, Any]:
        """Run benchmark for a single algorithm/language combination"""
        # Find the implementation file
        for category in self.config['algorithm_categories']:
            category_dir = self.root_dir / category
            algorithms = self._discover_algorithms(category_dir)

            for algo_name, implementations in algorithms.items():
                if algo_name.lower() == algorithm.lower() and language in implementations:
                    return self._run_benchmark(
                        algorithm,
                        language,
                        implementations[language]
                    )

        raise FileNotFoundError(f"Implementation not found: {algorithm} ({language})")

    def run_with_size(self, algorithm: str, language: str, input_size: int) -> Dict[str, Any]:
        """Run benchmark with specific input size"""
        # Save current config
        original_size = self.config.get('default_input_size')

        # Set new size
        self.config['default_input_size'] = input_size

        try:
            result = self.run_single_benchmark(algorithm, language)
            result['input_size'] = input_size
            return result
        finally:
            # Restore original size
            if original_size is not None:
                self.config['default_input_size'] = original_size
