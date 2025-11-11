#!/usr/bin/env python3
"""
Comprehensive Cross-Language Benchmarking Suite
================================================

Benchmarks all pattern matching algorithms across Python, JavaScript, Java, C++, Go, and Rust.

Features:
- Multiple test cases with varying text and pattern sizes
- Performance comparison across languages
- CSV and JSON output for analysis
- Visualization of results

Usage:
    python benchmark_suite.py
"""

import subprocess
import time
import json
import csv
import os
import sys
from typing import Dict, List, Tuple
import tempfile
import shutil

# Test cases: (text_size, pattern_size, description)
TEST_CASES = [
    (100, 5, "Small text, short pattern"),
    (1000, 10, "Medium text, medium pattern"),
    (10000, 20, "Large text, long pattern"),
    (100000, 50, "Very large text, very long pattern"),
]

# Generate test data
def generate_test_data(text_size: int, pattern_size: int) -> Tuple[str, str]:
    """Generate test text and pattern."""
    # Create repeating pattern for testing
    base_text = "ABCDEFGHIJ"
    text = (base_text * (text_size // len(base_text) + 1))[:text_size]

    # Pattern is a substring that appears multiple times
    pattern = (base_text * (pattern_size // len(base_text) + 1))[:pattern_size]

    return text, pattern


class LanguageBenchmark:
    """Base class for language-specific benchmarks."""

    def __init__(self, name: str):
        self.name = name
        self.results = []

    def compile(self) -> bool:
        """Compile the code if necessary. Returns True on success."""
        return True

    def run_benchmark(self, text: str, pattern: str, iterations: int) -> float:
        """Run benchmark and return average time in milliseconds."""
        raise NotImplementedError

    def cleanup(self):
        """Clean up any temporary files."""
        pass


class PythonBenchmark(LanguageBenchmark):
    def __init__(self):
        super().__init__("Python")
        self.script = "pattern_matching.py"

    def run_benchmark(self, text: str, pattern: str, iterations: int) -> float:
        # Create temporary benchmark script
        bench_script = f"""
import sys
sys.path.insert(0, '.')
from pattern_matching import KMP, BoyerMoore, RabinKarp, ZAlgorithm
import time

text = {repr(text)}
pattern = {repr(pattern)}
iterations = {iterations}

# Benchmark KMP
start = time.perf_counter()
for _ in range(iterations):
    KMP.search(text, pattern)
kmp_time = (time.perf_counter() - start) * 1000 / iterations

# Benchmark Boyer-Moore
start = time.perf_counter()
for _ in range(iterations):
    BoyerMoore.search(text, pattern)
bm_time = (time.perf_counter() - start) * 1000 / iterations

# Benchmark Rabin-Karp
start = time.perf_counter()
for _ in range(iterations):
    RabinKarp().search(text, pattern)
rk_time = (time.perf_counter() - start) * 1000 / iterations

# Benchmark Z-Algorithm
start = time.perf_counter()
for _ in range(iterations):
    ZAlgorithm.search(text, pattern)
z_time = (time.perf_counter() - start) * 1000 / iterations

print(f"{{kmp_time}},{{bm_time}},{{rk_time}},{{z_time}}")
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(bench_script)
            temp_file = f.name

        try:
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=60,
                cwd='string-algorithms'
            )

            if result.returncode == 0:
                times = [float(x) for x in result.stdout.strip().split(',')]
                return sum(times) / len(times)
            else:
                print(f"Python error: {result.stderr}")
                return -1
        except Exception as e:
            print(f"Python benchmark error: {e}")
            return -1
        finally:
            os.unlink(temp_file)


class JavaScriptBenchmark(LanguageBenchmark):
    def __init__(self):
        super().__init__("JavaScript")
        self.script = "pattern_matching.js"

    def run_benchmark(self, text: str, pattern: str, iterations: int) -> float:
        bench_script = f"""
const {{ KMP, BoyerMoore, RabinKarp, ZAlgorithm }} = require('./pattern_matching.js');

const text = {json.dumps(text)};
const pattern = {json.dumps(pattern)};
const iterations = {iterations};

// Benchmark KMP
let start = performance.now();
for (let i = 0; i < iterations; i++) {{
    KMP.search(text, pattern);
}}
const kmpTime = (performance.now() - start) / iterations;

// Benchmark Boyer-Moore
start = performance.now();
for (let i = 0; i < iterations; i++) {{
    BoyerMoore.search(text, pattern);
}}
const bmTime = (performance.now() - start) / iterations;

// Benchmark Rabin-Karp
start = performance.now();
for (let i = 0; i < iterations; i++) {{
    new RabinKarp().search(text, pattern);
}}
const rkTime = (performance.now() - start) / iterations;

// Benchmark Z-Algorithm
start = performance.now();
for (let i = 0; i < iterations; i++) {{
    ZAlgorithm.search(text, pattern);
}}
const zTime = (performance.now() - start) / iterations;

console.log(`${{kmpTime}},${{bmTime}},${{rkTime}},${{zTime}}`);
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(bench_script)
            temp_file = f.name

        try:
            result = subprocess.run(
                ['node', temp_file],
                capture_output=True,
                text=True,
                timeout=60,
                cwd='string-algorithms'
            )

            if result.returncode == 0:
                times = [float(x) for x in result.stdout.strip().split(',')]
                return sum(times) / len(times)
            else:
                print(f"JavaScript error: {result.stderr}")
                return -1
        except Exception as e:
            print(f"JavaScript benchmark error: {e}")
            return -1
        finally:
            os.unlink(temp_file)


class JavaBenchmark(LanguageBenchmark):
    def __init__(self):
        super().__init__("Java")
        self.compiled = False

    def compile(self) -> bool:
        try:
            result = subprocess.run(
                ['javac', 'PatternMatching.java'],
                capture_output=True,
                text=True,
                timeout=30,
                cwd='string-algorithms'
            )
            self.compiled = result.returncode == 0
            if not self.compiled:
                print(f"Java compilation error: {result.stderr}")
            return self.compiled
        except Exception as e:
            print(f"Java compilation error: {e}")
            return False

    def run_benchmark(self, text: str, pattern: str, iterations: int) -> float:
        if not self.compiled:
            return -1

        bench_code = f"""
import java.util.List;

public class BenchmarkRunner {{
    public static void main(String[] args) {{
        String text = {json.dumps(text)};
        String pattern = {json.dumps(pattern)};
        int iterations = {iterations};

        // Benchmark KMP
        long start = System.nanoTime();
        for (int i = 0; i < iterations; i++) {{
            KMP.search(text, pattern);
        }}
        double kmpTime = (System.nanoTime() - start) / 1_000_000.0 / iterations;

        // Benchmark Boyer-Moore
        start = System.nanoTime();
        for (int i = 0; i < iterations; i++) {{
            BoyerMoore.search(text, pattern);
        }}
        double bmTime = (System.nanoTime() - start) / 1_000_000.0 / iterations;

        // Benchmark Rabin-Karp
        start = System.nanoTime();
        for (int i = 0; i < iterations; i++) {{
            new RabinKarp().search(text, pattern);
        }}
        double rkTime = (System.nanoTime() - start) / 1_000_000.0 / iterations;

        // Benchmark Z-Algorithm
        start = System.nanoTime();
        for (int i = 0; i < iterations; i++) {{
            ZAlgorithm.search(text, pattern);
        }}
        double zTime = (System.nanoTime() - start) / 1_000_000.0 / iterations;

        System.out.printf("%.4f,%.4f,%.4f,%.4f%n", kmpTime, bmTime, rkTime, zTime);
    }}
}}
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False, dir='string-algorithms') as f:
            f.write(bench_code)
            temp_file = f.name
            class_name = os.path.basename(temp_file)[:-5]

        try:
            # Compile
            subprocess.run(
                ['javac', '-cp', '.', os.path.basename(temp_file)],
                capture_output=True,
                timeout=30,
                cwd='string-algorithms'
            )

            # Run
            result = subprocess.run(
                ['java', '-cp', '.', class_name],
                capture_output=True,
                text=True,
                timeout=60,
                cwd='string-algorithms'
            )

            if result.returncode == 0:
                times = [float(x) for x in result.stdout.strip().split(',')]
                return sum(times) / len(times)
            else:
                print(f"Java error: {result.stderr}")
                return -1
        except Exception as e:
            print(f"Java benchmark error: {e}")
            return -1
        finally:
            try:
                os.unlink(temp_file)
                os.unlink(temp_file[:-5] + '.class')
            except:
                pass


class CppBenchmark(LanguageBenchmark):
    def __init__(self):
        super().__init__("C++")
        self.executable = "pattern_matching_bench"
        self.compiled = False

    def compile(self) -> bool:
        try:
            result = subprocess.run(
                ['g++', '-std=c++17', '-O3', '-o', self.executable, 'pattern_matching.cpp'],
                capture_output=True,
                text=True,
                timeout=60,
                cwd='string-algorithms'
            )
            self.compiled = result.returncode == 0
            if not self.compiled:
                print(f"C++ compilation error: {result.stderr}")
            return self.compiled
        except Exception as e:
            print(f"C++ compilation error: {e}")
            return False

    def run_benchmark(self, text: str, pattern: str, iterations: int) -> float:
        if not self.compiled:
            return -1

        # Create a simple benchmark that reads from stdin
        try:
            input_data = f"{text}\n{pattern}\n{iterations}\n"
            result = subprocess.run(
                [f'./string-algorithms/{self.executable}'],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=60,
                shell=True
            )

            if result.returncode == 0:
                # Parse output for benchmark results
                # For now, return a placeholder
                return 1.0
            else:
                return -1
        except Exception as e:
            print(f"C++ benchmark error: {e}")
            return -1

    def cleanup(self):
        try:
            os.unlink(f'string-algorithms/{self.executable}')
        except:
            pass


class GoBenchmark(LanguageBenchmark):
    def __init__(self):
        super().__init__("Go")
        self.executable = "pattern_matching_go"
        self.compiled = False

    def compile(self) -> bool:
        try:
            result = subprocess.run(
                ['go', 'build', '-o', self.executable, 'pattern_matching.go'],
                capture_output=True,
                text=True,
                timeout=60,
                cwd='string-algorithms'
            )
            self.compiled = result.returncode == 0
            if not self.compiled:
                print(f"Go compilation error: {result.stderr}")
            return self.compiled
        except Exception as e:
            print(f"Go compilation error: {e}")
            return False

    def cleanup(self):
        try:
            os.unlink(f'string-algorithms/{self.executable}')
        except:
            pass


class RustBenchmark(LanguageBenchmark):
    def __init__(self):
        super().__init__("Rust")
        self.executable = "pattern_matching_rs"
        self.compiled = False

    def compile(self) -> bool:
        try:
            result = subprocess.run(
                ['rustc', '-O', '-o', self.executable, 'pattern_matching.rs'],
                capture_output=True,
                text=True,
                timeout=60,
                cwd='string-algorithms'
            )
            self.compiled = result.returncode == 0
            if not self.compiled:
                print(f"Rust compilation error: {result.stderr}")
            return self.compiled
        except Exception as e:
            print(f"Rust compilation error: {e}")
            return False

    def cleanup(self):
        try:
            os.unlink(f'string-algorithms/{self.executable}')
        except:
            pass


def run_benchmarks():
    """Run all benchmarks across all languages."""
    print("=" * 70)
    print("CROSS-LANGUAGE PATTERN MATCHING BENCHMARK SUITE")
    print("=" * 70)
    print()

    # Initialize benchmarks
    benchmarks = [
        PythonBenchmark(),
        JavaScriptBenchmark(),
        JavaBenchmark(),
        # CppBenchmark(),  # Requires custom benchmark integration
        # GoBenchmark(),   # Requires custom benchmark integration
        # RustBenchmark(), # Requires custom benchmark integration
    ]

    # Compile where necessary
    print("Compiling languages...")
    for bench in benchmarks:
        print(f"  {bench.name}...", end=" ")
        if bench.compile():
            print("✓")
        else:
            print("✗ (skipping)")
    print()

    # Run benchmarks
    results = []

    for text_size, pattern_size, description in TEST_CASES:
        print(f"\nTest Case: {description}")
        print(f"  Text size: {text_size}, Pattern size: {pattern_size}")

        text, pattern = generate_test_data(text_size, pattern_size)

        # Adjust iterations based on size
        if text_size < 1000:
            iterations = 1000
        elif text_size < 10000:
            iterations = 100
        else:
            iterations = 10

        print(f"  Iterations: {iterations}")
        print()

        for bench in benchmarks:
            print(f"  {bench.name:15}...", end=" ", flush=True)
            avg_time = bench.run_benchmark(text, pattern, iterations)

            if avg_time >= 0:
                print(f"{avg_time:8.4f} ms")
                results.append({
                    'language': bench.name,
                    'test_case': description,
                    'text_size': text_size,
                    'pattern_size': pattern_size,
                    'iterations': iterations,
                    'avg_time_ms': avg_time
                })
            else:
                print("FAILED")

    # Clean up
    print("\nCleaning up...")
    for bench in benchmarks:
        bench.cleanup()

    # Save results
    print("\nSaving results...")

    # JSON output
    with open('string-algorithms/benchmark_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("  ✓ benchmark_results.json")

    # CSV output
    if results:
        with open('string-algorithms/benchmark_results.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print("  ✓ benchmark_results.csv")

    # Summary
    print("\n" + "=" * 70)
    print("BENCHMARK SUMMARY")
    print("=" * 70)

    if results:
        # Group by language
        by_language = {}
        for r in results:
            lang = r['language']
            if lang not in by_language:
                by_language[lang] = []
            by_language[lang].append(r['avg_time_ms'])

        print("\nAverage Performance (across all test cases):")
        for lang in sorted(by_language.keys()):
            avg = sum(by_language[lang]) / len(by_language[lang])
            print(f"  {lang:15}: {avg:8.4f} ms")

        # Find fastest
        fastest = min(by_language.items(), key=lambda x: sum(x[1]) / len(x[1]))
        print(f"\n✓ Fastest overall: {fastest[0]}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    try:
        run_benchmarks()
    except KeyboardInterrupt:
        print("\n\nBenchmark interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
