/**
 * Simple Benchmark Example - JavaScript
 *
 * Demonstrates how to create a benchmarkable algorithm implementation.
 */

function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

function main() {
    const inputSize = parseInt(process.argv[2]) || 20;
    const n = Math.min(inputSize, 35);

    const result = fibonacci(n);
    console.log(`Fibonacci(${n}) = ${result}`);
}

main();
