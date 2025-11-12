"""
Memory Profiler - Profiles memory usage of algorithm implementations
"""

import subprocess
import psutil
import os
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import statistics

logger = logging.getLogger(__name__)


class MemoryProfiler:
    """Profiles memory usage across different algorithm implementations"""

    def __init__(self):
        self.root_dir = Path(__file__).parent.parent.parent

        # Language-specific memory profiling commands
        self.profilers = {
            'python': self._profile_python,
            'javascript': self._profile_nodejs,
            'java': self._profile_java,
            'cpp': self._profile_cpp,
            'c': self._profile_c,
            'go': self._profile_go,
            'rust': self._profile_rust
        }

    def profile_all(self, categories: List[str]) -> Dict[str, Any]:
        """
        Profile memory usage for all algorithms in specified categories

        Args:
            categories: List of algorithm categories

        Returns:
            Memory profiling results
        """
        all_profiles = {}

        for category in categories:
            logger.info(f"Profiling memory usage for {category}...")
            category_profiles = self._profile_category(category)
            all_profiles[category] = category_profiles

        return all_profiles

    def _profile_category(self, category: str) -> Dict[str, Any]:
        """Profile all algorithms in a category"""
        category_dir = self.root_dir / category

        if not category_dir.exists():
            logger.warning(f"Category directory not found: {category}")
            return {}

        profiles = {}
        algorithms = self._discover_algorithms(category_dir)

        for algorithm_name, implementations in algorithms.items():
            logger.info(f"  Profiling {algorithm_name}...")
            algorithm_profiles = {}

            for language, file_path in implementations.items():
                if language not in self.profilers:
                    continue

                try:
                    profile = self.profilers[language](file_path)
                    algorithm_profiles[language] = profile
                    logger.info(
                        f"    ✓ {language}: "
                        f"{profile['avg_memory_mb']:.2f}MB avg, "
                        f"{profile['peak_memory_mb']:.2f}MB peak"
                    )
                except Exception as e:
                    logger.error(f"    ✗ {language}: {e}")
                    algorithm_profiles[language] = {'error': str(e)}

            profiles[algorithm_name] = algorithm_profiles

        return profiles

    def _discover_algorithms(self, category_dir: Path) -> Dict[str, Dict[str, Path]]:
        """Discover algorithms and their implementations"""
        algorithms = {}

        patterns = {
            'python': '*.py',
            'javascript': '*.js',
            'java': '*.java',
            'cpp': '*.cpp',
            'c': '*.c',
            'go': '*.go',
            'rust': '*.rs'
        }

        for lang, pattern in patterns.items():
            for file in category_dir.glob(pattern):
                algo_name = file.stem.replace('_', ' ').title()

                if algo_name not in algorithms:
                    algorithms[algo_name] = {}

                algorithms[algo_name][lang] = file

        return algorithms

    def _profile_python(self, file_path: Path) -> Dict[str, Any]:
        """Profile Python script memory usage"""
        try:
            # Use memory_profiler if available, otherwise use psutil
            memory_measurements = []
            runs = 5

            for _ in range(runs):
                # Start subprocess
                process = psutil.Popen(
                    ['python3', str(file_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=file_path.parent
                )

                peak_memory = 0
                samples = []

                # Monitor memory while process runs
                while process.poll() is None:
                    try:
                        mem_info = process.memory_info()
                        memory_mb = mem_info.rss / (1024 * 1024)  # Convert to MB
                        samples.append(memory_mb)
                        peak_memory = max(peak_memory, memory_mb)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        break

                if samples:
                    memory_measurements.append({
                        'avg': statistics.mean(samples),
                        'peak': peak_memory
                    })

            if not memory_measurements:
                return {'error': 'No memory measurements collected'}

            return {
                'avg_memory_mb': statistics.mean([m['avg'] for m in memory_measurements]),
                'peak_memory_mb': max([m['peak'] for m in memory_measurements]),
                'min_memory_mb': min([m['avg'] for m in memory_measurements]),
                'measurements': len(memory_measurements)
            }

        except Exception as e:
            return {'error': str(e)}

    def _profile_nodejs(self, file_path: Path) -> Dict[str, Any]:
        """Profile Node.js script memory usage"""
        try:
            memory_measurements = []
            runs = 5

            for _ in range(runs):
                process = psutil.Popen(
                    ['node', '--expose-gc', str(file_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=file_path.parent
                )

                peak_memory = 0
                samples = []

                while process.poll() is None:
                    try:
                        mem_info = process.memory_info()
                        memory_mb = mem_info.rss / (1024 * 1024)
                        samples.append(memory_mb)
                        peak_memory = max(peak_memory, memory_mb)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        break

                if samples:
                    memory_measurements.append({
                        'avg': statistics.mean(samples),
                        'peak': peak_memory
                    })

            if not memory_measurements:
                return {'error': 'No memory measurements collected'}

            return {
                'avg_memory_mb': statistics.mean([m['avg'] for m in memory_measurements]),
                'peak_memory_mb': max([m['peak'] for m in memory_measurements]),
                'min_memory_mb': min([m['avg'] for m in memory_measurements]),
                'measurements': len(memory_measurements)
            }

        except Exception as e:
            return {'error': str(e)}

    def _profile_java(self, file_path: Path) -> Dict[str, Any]:
        """Profile Java program memory usage"""
        try:
            # Compile if needed
            class_name = file_path.stem

            memory_measurements = []
            runs = 5

            for _ in range(runs):
                process = psutil.Popen(
                    ['java', '-Xms32m', '-Xmx256m', class_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=file_path.parent
                )

                peak_memory = 0
                samples = []

                while process.poll() is None:
                    try:
                        mem_info = process.memory_info()
                        memory_mb = mem_info.rss / (1024 * 1024)
                        samples.append(memory_mb)
                        peak_memory = max(peak_memory, memory_mb)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        break

                if samples:
                    memory_measurements.append({
                        'avg': statistics.mean(samples),
                        'peak': peak_memory
                    })

            if not memory_measurements:
                return {'error': 'No memory measurements collected'}

            return {
                'avg_memory_mb': statistics.mean([m['avg'] for m in memory_measurements]),
                'peak_memory_mb': max([m['peak'] for m in memory_measurements]),
                'min_memory_mb': min([m['avg'] for m in memory_measurements]),
                'measurements': len(memory_measurements)
            }

        except Exception as e:
            return {'error': str(e)}

    def _profile_cpp(self, file_path: Path) -> Dict[str, Any]:
        """Profile C++ program memory usage using Valgrind if available"""
        executable = file_path.parent / file_path.stem

        if not executable.exists():
            return {'error': 'Executable not found - please compile first'}

        try:
            # Try using valgrind for detailed profiling
            result = subprocess.run(
                ['valgrind', '--tool=massif', '--massif-out-file=/tmp/massif.out',
                 str(executable)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=file_path.parent
            )

            # Parse massif output
            if os.path.exists('/tmp/massif.out'):
                # Basic parsing - could be enhanced
                return self._fallback_profile(executable)
            else:
                return self._fallback_profile(executable)

        except (subprocess.TimeoutExpired, FileNotFoundError):
            # Fallback to psutil monitoring
            return self._fallback_profile(executable)
        except Exception as e:
            return {'error': str(e)}

    def _profile_c(self, file_path: Path) -> Dict[str, Any]:
        """Profile C program memory usage"""
        # Same as C++ for now
        return self._profile_cpp(file_path)

    def _profile_go(self, file_path: Path) -> Dict[str, Any]:
        """Profile Go program memory usage"""
        try:
            memory_measurements = []
            runs = 5

            for _ in range(runs):
                process = psutil.Popen(
                    ['go', 'run', str(file_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=file_path.parent
                )

                peak_memory = 0
                samples = []

                while process.poll() is None:
                    try:
                        mem_info = process.memory_info()
                        memory_mb = mem_info.rss / (1024 * 1024)
                        samples.append(memory_mb)
                        peak_memory = max(peak_memory, memory_mb)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        break

                if samples:
                    memory_measurements.append({
                        'avg': statistics.mean(samples),
                        'peak': peak_memory
                    })

            if not memory_measurements:
                return {'error': 'No memory measurements collected'}

            return {
                'avg_memory_mb': statistics.mean([m['avg'] for m in memory_measurements]),
                'peak_memory_mb': max([m['peak'] for m in memory_measurements]),
                'min_memory_mb': min([m['avg'] for m in memory_measurements]),
                'measurements': len(memory_measurements)
            }

        except Exception as e:
            return {'error': str(e)}

    def _profile_rust(self, file_path: Path) -> Dict[str, Any]:
        """Profile Rust program memory usage"""
        try:
            memory_measurements = []
            runs = 5

            for _ in range(runs):
                process = psutil.Popen(
                    ['cargo', 'run', '--release'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=file_path.parent
                )

                peak_memory = 0
                samples = []

                while process.poll() is None:
                    try:
                        mem_info = process.memory_info()
                        memory_mb = mem_info.rss / (1024 * 1024)
                        samples.append(memory_mb)
                        peak_memory = max(peak_memory, memory_mb)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        break

                if samples:
                    memory_measurements.append({
                        'avg': statistics.mean(samples),
                        'peak': peak_memory
                    })

            if not memory_measurements:
                return {'error': 'No memory measurements collected'}

            return {
                'avg_memory_mb': statistics.mean([m['avg'] for m in memory_measurements]),
                'peak_memory_mb': max([m['peak'] for m in memory_measurements]),
                'min_memory_mb': min([m['avg'] for m in memory_measurements]),
                'measurements': len(memory_measurements)
            }

        except Exception as e:
            return {'error': str(e)}

    def _fallback_profile(self, executable: Path) -> Dict[str, Any]:
        """Fallback memory profiling using psutil"""
        try:
            memory_measurements = []
            runs = 5

            for _ in range(runs):
                process = psutil.Popen(
                    [str(executable)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=executable.parent
                )

                peak_memory = 0
                samples = []

                while process.poll() is None:
                    try:
                        mem_info = process.memory_info()
                        memory_mb = mem_info.rss / (1024 * 1024)
                        samples.append(memory_mb)
                        peak_memory = max(peak_memory, memory_mb)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        break

                if samples:
                    memory_measurements.append({
                        'avg': statistics.mean(samples),
                        'peak': peak_memory
                    })

            if not memory_measurements:
                return {'error': 'No memory measurements collected'}

            return {
                'avg_memory_mb': statistics.mean([m['avg'] for m in memory_measurements]),
                'peak_memory_mb': max([m['peak'] for m in memory_measurements]),
                'min_memory_mb': min([m['avg'] for m in memory_measurements]),
                'measurements': len(memory_measurements)
            }

        except Exception as e:
            return {'error': str(e)}
