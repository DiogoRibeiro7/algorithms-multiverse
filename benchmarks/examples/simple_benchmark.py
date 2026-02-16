"""
Simple Benchmark Example

Demonstrates how to create a benchmarkable algorithm implementation.
The framework will automatically discover and execute this.
"""

import sys
import time


def fibonacci(n):
    """Calculate nth Fibonacci number (intentionally inefficient for benchmarking)"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def main():
    """Benchmark entry point that runs the recursive Fibonacci workload."""
    # Get input size from command line (required for benchmarking)
    input_size = int(sys.argv[1]) if len(sys.argv) > 1 else 20

    # Scale input to reasonable range for this algorithm
    n = min(input_size, 35)  # Cap to avoid excessive runtime

    # Perform the computation
    result = fibonacci(n)

    # Print result (optional - used for verification)
    print(f"Fibonacci({n}) = {result}")


if __name__ == '__main__':
    main()
