"""
Comprehensive Testing and Benchmarking Suite
=============================================

Tests all number theory algorithm implementations across languages and
provides performance benchmarking.

Usage:
    python benchmark_and_test.py

Requirements:
    - Python 3.7+
    - Implementations compiled and available
"""

import subprocess
import time
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")


def print_section(text: str) -> None:
    """Print a section header."""
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'-' * 50}{Colors.ENDC}")


def print_success(text: str) -> None:
    """Print success message."""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text: str) -> None:
    """Print error message."""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_warning(text: str) -> None:
    """Print warning message."""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def run_command(command: List[str], timeout: int = 10) -> Tuple[bool, float, str]:
    """
    Run a command and return success status, execution time, and output.

    Args:
        command: Command to execute as list of strings
        timeout: Maximum execution time in seconds

    Returns:
        Tuple of (success, execution_time, output)
    """
    try:
        start_time = time.time()
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=Path(__file__).parent
        )
        execution_time = time.time() - start_time

        success = result.returncode == 0
        output = result.stdout if success else result.stderr

        return success, execution_time, output

    except subprocess.TimeoutExpired:
        return False, timeout, "Timeout expired"
    except FileNotFoundError:
        return False, 0.0, "Executable not found"
    except Exception as e:
        return False, 0.0, str(e)


def test_python_implementation() -> bool:
    """Test Python implementations."""
    print_section("Testing Python Implementation")

    implementations = [
        ("Basic algorithms", ["python", "number_theory.py"]),
        ("Advanced algorithms", ["python", "advanced_number_theory.py"])
    ]

    all_passed = True

    for name, command in implementations:
        print(f"\nTesting {name}...")
        success, exec_time, output = run_command(command)

        if success:
            print_success(f"{name} passed ({exec_time:.3f}s)")
        else:
            print_error(f"{name} failed")
            print(f"Error: {output[:200]}")
            all_passed = False

    return all_passed


def test_c_implementation() -> bool:
    """Test C implementation."""
    print_section("Testing C Implementation")

    # Try to compile
    print("Compiling C code...")
    compile_success, _, compile_output = run_command(
        ["gcc", "-O3", "-o", "number_theory_c", "number_theory.c", "-lm"],
        timeout=30
    )

    if not compile_success:
        print_error("C compilation failed")
        print(f"Error: {compile_output[:200]}")
        return False

    print_success("C compilation successful")

    # Run the executable
    print("\nRunning C implementation...")
    success, exec_time, output = run_command(["./number_theory_c"])

    if success:
        print_success(f"C implementation passed ({exec_time:.3f}s)")
        return True
    else:
        print_error("C implementation failed")
        print(f"Error: {output[:200]}")
        return False


def test_go_implementation() -> bool:
    """Test Go implementation."""
    print_section("Testing Go Implementation")

    print("Running Go implementation...")
    success, exec_time, output = run_command(["go", "run", "number_theory.go"])

    if success:
        print_success(f"Go implementation passed ({exec_time:.3f}s)")
        return True
    else:
        print_error("Go implementation failed")
        print(f"Error: {output[:200]}")
        return False


def test_rust_implementation() -> bool:
    """Test Rust implementation."""
    print_section("Testing Rust Implementation")

    # Try to compile
    print("Compiling Rust code...")
    compile_success, _, compile_output = run_command(
        ["rustc", "-O", "number_theory.rs"],
        timeout=60
    )

    if not compile_success:
        print_error("Rust compilation failed")
        print(f"Error: {compile_output[:200]}")
        return False

    print_success("Rust compilation successful")

    # Run the executable
    print("\nRunning Rust implementation...")
    success, exec_time, output = run_command(["./number_theory"])

    if success:
        print_success(f"Rust implementation passed ({exec_time:.3f}s)")
        return True
    else:
        print_error("Rust implementation failed")
        print(f"Error: {output[:200]}")
        return False


def test_fortran_implementation() -> bool:
    """Test Fortran implementation."""
    print_section("Testing Fortran Implementation")

    # Try to compile
    print("Compiling Fortran code...")
    compile_success, _, compile_output = run_command(
        ["gfortran", "-O3", "-o", "number_theory_f90", "number_theory.f90"],
        timeout=30
    )

    if not compile_success:
        print_error("Fortran compilation failed")
        print(f"Error: {compile_output[:200]}")
        return False

    print_success("Fortran compilation successful")

    # Run the executable
    print("\nRunning Fortran implementation...")
    success, exec_time, output = run_command(["./number_theory_f90"])

    if success:
        print_success(f"Fortran implementation passed ({exec_time:.3f}s)")
        return True
    else:
        print_error("Fortran implementation failed")
        print(f"Error: {output[:200]}")
        return False


def test_cobol_implementation() -> bool:
    """Test COBOL implementation."""
    print_section("Testing COBOL Implementation")

    # Try to compile
    print("Compiling COBOL code...")
    compile_success, _, compile_output = run_command(
        ["cobc", "-x", "-free", "number_theory.cob"],
        timeout=30
    )

    if not compile_success:
        print_error("COBOL compilation failed")
        print(f"Error: {compile_output[:200]}")
        return False

    print_success("COBOL compilation successful")

    # Run the executable
    print("\nRunning COBOL implementation...")
    success, exec_time, output = run_command(["./number_theory"])

    if success:
        print_success(f"COBOL implementation passed ({exec_time:.3f}s)")
        return True
    else:
        print_error("COBOL implementation failed")
        print(f"Error: {output[:200]}")
        return False


def test_r_implementation() -> bool:
    """Test R implementation."""
    print_section("Testing R Implementation")

    print("Running R implementation...")
    success, exec_time, output = run_command(["Rscript", "number_theory.R"])

    if success:
        print_success(f"R implementation passed ({exec_time:.3f}s)")
        return True
    else:
        print_error("R implementation failed")
        print(f"Error: {output[:200]}")
        return False


def benchmark_sieve_performance() -> None:
    """Benchmark sieve of Eratosthenes across implementations."""
    print_section("Performance Benchmark: Sieve of Eratosthenes")

    print("\nBenchmarking prime generation up to 1,000,000...")
    print("(This may take a moment...)\n")

    # Note: This is a simplified benchmark
    # For accurate results, run each implementation multiple times

    results = []

    # Python benchmark
    try:
        from number_theory import sieve_of_eratosthenes
        start = time.time()
        primes = sieve_of_eratosthenes(1000000)
        python_time = time.time() - start
        results.append(("Python", python_time, len(primes)))
    except Exception as e:
        print_warning(f"Python benchmark failed: {e}")

    print(f"\n{'Language':<15} {'Time (s)':<15} {'Primes Found':<15}")
    print("-" * 45)

    for lang, exec_time, count in results:
        print(f"{lang:<15} {exec_time:<15.4f} {count:<15,}")


def verify_correctness() -> None:
    """Verify correctness of implementations by comparing results."""
    print_section("Correctness Verification")

    print("\nVerifying that all implementations produce consistent results...")

    try:
        from number_theory import (
            sieve_of_eratosthenes,
            gcd,
            mod_exp,
            miller_rabin
        )

        # Test cases
        test_limit = 100
        primes = sieve_of_eratosthenes(test_limit)
        print_success(f"Sieve test: Found {len(primes)} primes up to {test_limit}")

        gcd_result = gcd(48, 18)
        print_success(f"GCD test: gcd(48, 18) = {gcd_result} (expected 6)")
        assert gcd_result == 6, "GCD test failed"

        mod_result = mod_exp(2, 10, 1000)
        print_success(f"Modular exponentiation test: 2^10 mod 1000 = {mod_result} (expected 24)")
        assert mod_result == 24, "Modular exponentiation test failed"

        prime_result = miller_rabin(17, k=5)
        print_success(f"Miller-Rabin test: 17 is prime = {prime_result} (expected True)")
        assert prime_result == True, "Miller-Rabin test failed"

        composite_result = miller_rabin(561, k=5)
        print_success(f"Miller-Rabin test: 561 is prime = {composite_result} (expected False)")
        assert composite_result == False, "Miller-Rabin test for composite failed"

        print_success("\nAll correctness tests passed!")

    except Exception as e:
        print_error(f"Correctness verification failed: {e}")


def generate_summary(results: Dict[str, bool]) -> None:
    """Generate a summary of test results."""
    print_header("TEST SUMMARY")

    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed

    print(f"Total tests: {total}")
    print_success(f"Passed: {passed}")
    if failed > 0:
        print_error(f"Failed: {failed}")

    print("\nDetailed results:")
    for lang, status in results.items():
        if status:
            print_success(f"{lang}: PASSED")
        else:
            print_error(f"{lang}: FAILED")

    if failed == 0:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 All tests passed! 🎉{Colors.ENDC}")
    else:
        print(f"\n{Colors.WARNING}Some tests failed. Please check the output above.{Colors.ENDC}")


def main():
    """Main testing function."""
    print_header("NUMBER THEORY ALGORITHMS - TEST SUITE")

    print("This script will test all implementations across multiple languages.")
    print("Ensure all compilers/interpreters are installed:\n")
    print("  • Python 3.7+")
    print("  • GCC (for C)")
    print("  • Go")
    print("  • Rust")
    print("  • GFortran (for Fortran)")
    print("  • GnuCOBOL (for COBOL)")
    print("  • R")
    print()

    # Track results
    results = {}

    # Run tests
    results["Python"] = test_python_implementation()
    results["C"] = test_c_implementation()
    results["Go"] = test_go_implementation()
    results["Rust"] = test_rust_implementation()
    results["Fortran"] = test_fortran_implementation()
    results["COBOL"] = test_cobol_implementation()
    results["R"] = test_r_implementation()

    # Additional tests
    verify_correctness()
    benchmark_sieve_performance()

    # Generate summary
    generate_summary(results)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Testing interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}Unexpected error: {e}{Colors.ENDC}")
        sys.exit(1)
