/**
 * Fibonacci Sequence Implementation in JavaScript
 * 
 * Time Complexity:
 * - Recursive: O(2^n)
 * - Dynamic Programming: O(n)
 * - Matrix Exponentiation: O(log n)
 * 
 * Space Complexity:
 * - Recursive: O(n) call stack
 * - Iterative: O(1)
 * - Memoized: O(n)
 * 
 * JavaScript features:
 * - ES6+ syntax
 * - Closures and higher-order functions
 * - Generator functions
 * - Async/await support
 * - Modern class syntax
 */

// ============= BASIC IMPLEMENTATIONS =============

/**
 * Simple recursive implementation (inefficient)
 */
function fibonacciRecursive(n) {
    if (n <= 1) return n;
    return fibonacciRecursive(n - 1) + fibonacciRecursive(n - 2);
}

/**
 * Iterative implementation (efficient)
 */
function fibonacciIterative(n) {
    if (n <= 1) return n;
    
    let a = 0, b = 1;
    for (let i = 2; i <= n; i++) {
        [a, b] = [b, a + b];
    }
    return b;
}

/**
 * Memoized recursive implementation
 */
const fibonacciMemoized = (() => {
    const cache = new Map([[0, 0], [1, 1]]);
    
    return function fibonacci(n) {
        if (cache.has(n)) {
            return cache.get(n);
        }
        
        const result = fibonacci(n - 1) + fibonacci(n - 2);
        cache.set(n, result);
        return result;
    };
})();

/**
 * Dynamic programming bottom-up approach
 */
function fibonacciDP(n) {
    if (n <= 1) return n;
    
    const dp = new Array(n + 1);
    dp[0] = 0;
    dp[1] = 1;
    
    for (let i = 2; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    
    return dp[n];
}

/**
 * Matrix exponentiation approach
 */
function fibonacciMatrix(n) {
    if (n <= 1) return n;
    
    function multiplyMatrix(a, b) {
        return [
            [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]
        ];
    }
    
    function matrixPower(matrix, power) {
        if (power === 1) return matrix;
        
        if (power % 2 === 0) {
            const half = matrixPower(matrix, power / 2);
            return multiplyMatrix(half, half);
        } else {
            return multiplyMatrix(matrix, matrixPower(matrix, power - 1));
        }
    }
    
    const baseMatrix = [[1, 1], [1, 0]];
    const resultMatrix = matrixPower(baseMatrix, n);
    return resultMatrix[0][1];
}

/**
 * Golden ratio formula (Binet's formula)
 * Limited by floating point precision
 */
function fibonacciGoldenRatio(n) {
    if (n <= 1) return n;
    
    const phi = (1 + Math.sqrt(5)) / 2;
    const psi = (1 - Math.sqrt(5)) / 2;
    
    return Math.round((Math.pow(phi, n) - Math.pow(psi, n)) / Math.sqrt(5));
}

// ============= GENERATOR FUNCTIONS =============

/**
 * Infinite Fibonacci generator
 */
function* fibonacciGenerator() {
    let a = 0, b = 1;
    yield a;
    yield b;
    
    while (true) {
        [a, b] = [b, a + b];
        yield b;
    }
}

/**
 * Finite Fibonacci generator
 */
function* fibonacciSequence(count) {
    let a = 0, b = 1;
    
    for (let i = 0; i < count; i++) {
        if (i === 0) yield a;
        else if (i === 1) yield b;
        else {
            [a, b] = [b, a + b];
            yield b;
        }
    }
}

/**
 * Range-based Fibonacci generator
 */
function* fibonacciRange(start, end) {
    let a = 0, b = 1, current = 0;
    
    // Skip to start
    for (let i = 0; i < start; i++) {
        if (i <= 1) {
            current = i;
        } else {
            [a, b] = [b, a + b];
            current = b;
        }
    }
    
    // Generate from start to end
    for (let i = start; i <= end; i++) {
        yield current;
        
        if (i < end) {
            if (i === 0) {
                current = 1;
                a = 0;
                b = 1;
            } else {
                [a, b] = [b, a + b];
                current = b;
            }
        }
    }
}

// ============= CLASS-BASED IMPLEMENTATION =============

class FibonacciCalculator {
    constructor() {
        this.cache = new Map([[0, 0], [1, 1]]);
        this.computations = 0;
    }
    
    /**
     * Calculate Fibonacci number using specified method
     */
    calculate(n, method = 'iterative') {
        this.computations = 0;
        
        const methods = {
            'recursive': this.recursive.bind(this),
            'iterative': this.iterative.bind(this),
            'memoized': this.memoized.bind(this),
            'dp': this.dynamicProgramming.bind(this),
            'matrix': this.matrixExponentiation.bind(this),
            'golden': this.goldenRatio.bind(this),
            'cached': this.cached.bind(this)
        };
        
        if (!(method in methods)) {
            throw new Error(`Unknown method: ${method}`);
        }
        
        return methods[method](n);
    }
    
    recursive(n) {
        this.computations++;
        if (n <= 1) return n;
        return this.recursive(n - 1) + this.recursive(n - 2);
    }
    
    iterative(n) {
        this.computations++;
        if (n <= 1) return n;
        
        let a = 0, b = 1;
        for (let i = 2; i <= n; i++) {
            [a, b] = [b, a + b];
        }
        return b;
    }
    
    memoized(n) {
        this.computations++;
        if (n <= 1) return n;
        
        if (this.cache.has(n)) {
            return this.cache.get(n);
        }
        
        const result = this.memoized(n - 1) + this.memoized(n - 2);
        this.cache.set(n, result);
        return result;
    }
    
    dynamicProgramming(n) {
        this.computations++;
        return fibonacciDP(n);
    }
    
    matrixExponentiation(n) {
        this.computations++;
        return fibonacciMatrix(n);
    }
    
    goldenRatio(n) {
        this.computations++;
        return fibonacciGoldenRatio(n);
    }
    
    cached(n) {
        this.computations++;
        if (this.cache.has(n)) {
            return this.cache.get(n);
        }
        
        const result = this.iterative(n);
        this.cache.set(n, result);
        return result;
    }
    
    /**
     * Benchmark different methods
     */
    benchmark(n) {
        const methods = ['iterative', 'memoized', 'dp', 'matrix', 'golden'];
        if (n <= 35) methods.push('recursive'); // Avoid long recursive times
        
        const results = {};
        
        for (const method of methods) {
            const startTime = performance.now();
            try {
                const result = this.calculate(n, method);
                const endTime = performance.now();
                
                results[method] = {
                    result,
                    time: endTime - startTime,
                    computations: this.computations,
                    error: null
                };
            } catch (error) {
                results[method] = {
                    result: null,
                    time: Infinity,
                    computations: this.computations,
                    error: error.message
                };
            }
        }
        
        return results;
    }
    
    /**
     * Clear the cache
     */
    clearCache() {
        this.cache.clear();
        this.cache.set(0, 0);
        this.cache.set(1, 1);
    }
    
    /**
     * Get cache statistics
     */
    getCacheStats() {
        return {
            size: this.cache.size,
            entries: [...this.cache.entries()]
        };
    }
}

// ============= UTILITY FUNCTIONS =============

/**
 * Check if a number is a Fibonacci number
 */
function isFibonacciNumber(num) {
    if (num < 0) return false;
    
    // A number is Fibonacci if one or both of (5*n^2 + 4) or (5*n^2 - 4) is a perfect square
    function isPerfectSquare(x) {
        const root = Math.sqrt(x);
        return Math.floor(root) * Math.floor(root) === x;
    }
    
    return isPerfectSquare(5 * num * num + 4) || isPerfectSquare(5 * num * num - 4);
}

/**
 * Find the index of a Fibonacci number
 */
function findFibonacciIndex(target) {
    if (target < 0) return -1;
    if (target === 0) return 0;
    if (target === 1) return 1;
    
    let a = 0, b = 1, index = 1;
    
    while (b < target) {
        [a, b] = [b, a + b];
        index++;
    }
    
    return b === target ? index : -1;
}

/**
 * Get Fibonacci sequence as array
 */
function fibonacciSequenceArray(count) {
    if (count <= 0) return [];
    if (count === 1) return [0];
    
    const sequence = [0, 1];
    
    for (let i = 2; i < count; i++) {
        sequence.push(sequence[i - 1] + sequence[i - 2]);
    }
    
    return sequence;
}

/**
 * Sum of first n Fibonacci numbers
 */
function fibonacciSum(n) {
    if (n <= 0) return 0;
    
    // Sum of first n Fibonacci numbers = F(n+2) - 1
    return fibonacciIterative(n + 1) - 1;
}

/**
 * Get Fibonacci numbers up to a maximum value
 */
function fibonacciUpTo(max) {
    const result = [];
    let a = 0, b = 1;
    
    while (a <= max) {
        result.push(a);
        [a, b] = [b, a + b];
    }
    
    return result;
}

// ============= ASYNC/AWAIT IMPLEMENTATIONS =============

/**
 * Async Fibonacci calculator with delay
 */
async function fibonacciAsync(n, delay = 1) {
    if (n <= 1) return n;
    
    await new Promise(resolve => setTimeout(resolve, delay));
    
    const [a, b] = await Promise.all([
        fibonacciAsync(n - 1, delay),
        fibonacciAsync(n - 2, delay)
    ]);
    
    return a + b;
}

/**
 * Worker-based parallel Fibonacci (simulation)
 */
async function fibonacciParallel(n) {
    if (n <= 1) return n;
    if (n <= 30) return fibonacciIterative(n); // Use iterative for small numbers
    
    // Simulate parallel computation
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(fibonacciIterative(n));
        }, Math.random() * 10);
    });
}

// ============= DEMONSTRATION AND TESTING =============

function demonstrateFibonacci() {
    console.log('🔢 Fibonacci Sequence Implementation in JavaScript');
    console.log('=' .repeat(50));
    
    // Test different methods
    const testCases = [0, 1, 5, 10, 20, 30];
    console.log('\n📋 Method Comparison:');
    console.log('n'.padStart(3), 'Recursive'.padStart(12), 'Iterative'.padStart(12), 
                'Memoized'.padStart(12), 'Matrix'.padStart(12), 'Golden'.padStart(12));
    console.log('-'.repeat(65));
    
    const calculator = new FibonacciCalculator();
    
    for (const n of testCases) {
        const results = [];
        
        // Only test recursive for small values
        if (n <= 30) {
            results.push(calculator.calculate(n, 'recursive').toString());
        } else {
            results.push('Too slow');
        }
        
        results.push(
            calculator.calculate(n, 'iterative').toString(),
            calculator.calculate(n, 'memoized').toString(),
            calculator.calculate(n, 'matrix').toString(),
            calculator.calculate(n, 'golden').toString()
        );
        
        console.log(n.toString().padStart(3), ...results.map(r => r.padStart(12)));
    }
    
    // Fibonacci sequence
    console.log('\n🔢 First 20 Fibonacci numbers:');
    const sequence = fibonacciSequenceArray(20);
    console.log(sequence.map(n => n.toString().padStart(4)).join(' '));
    
    // Using generators
    console.log('\n🔄 Using Generator (first 15):');
    const gen = fibonacciGenerator();
    const first15 = [];
    for (let i = 0; i < 15; i++) {
        first15.push(gen.next().value);
    }
    console.log(first15.map(n => n.toString().padStart(4)).join(' '));
    
    // Range generator
    console.log('\n📍 Range Generator (indices 10-15):');
    const rangeGen = fibonacciRange(10, 15);
    const rangeValues = [...rangeGen];
    console.log(rangeValues.map(n => n.toString().padStart(6)).join(' '));
    
    // Fibonacci number validation
    console.log('\n✅ Fibonacci Number Validation:');
    const testNumbers = [0, 1, 2, 3, 4, 5, 8, 13, 21, 22, 34, 55, 89, 90];
    for (const num of testNumbers) {
        const isFib = isFibonacciNumber(num);
        const index = findFibonacciIndex(num);
        console.log(`${num.toString().padStart(3)}: ${isFib ? '✓' : '✗'} ${index >= 0 ? `(F(${index}))` : ''}`);
    }
    
    // Properties and patterns
    console.log('\n📊 Fibonacci Properties:');
    const n = 10;
    const seq = fibonacciSequenceArray(n);
    console.log(`First ${n} Fibonacci numbers: [${seq.join(', ')}]`);
    console.log(`Sum of first ${n} numbers: ${fibonacciSum(n)}`);
    
    if (seq.length >= 2) {
        const goldenRatio = seq[seq.length - 1] / seq[seq.length - 2];
        console.log(`Golden ratio approximation (F(n)/F(n-1)): ${goldenRatio.toFixed(6)}`);
        console.log(`Actual golden ratio: ${((1 + Math.sqrt(5)) / 2).toFixed(6)}`);
    }
    
    // Numbers up to a limit
    const upTo100 = fibonacciUpTo(100);
    console.log(`\nFibonacci numbers up to 100: [${upTo100.join(', ')}]`);
}

function performanceBenchmark() {
    console.log('\n⚡ Performance Benchmark');
    console.log('=' .repeat(30));
    
    const calculator = new FibonacciCalculator();
    const testValues = [20, 30, 100, 500, 1000];
    
    console.log('n'.padStart(6), 'Iterative'.padStart(12), 'Memoized'.padStart(12), 
                'Matrix'.padStart(12), 'Golden'.padStart(12));
    console.log('-'.repeat(54));
    
    for (const n of testValues) {
        const benchmarks = calculator.benchmark(n);
        
        const results = [
            (benchmarks.iterative?.time || 0).toFixed(4),
            (benchmarks.memoized?.time || 0).toFixed(4),
            (benchmarks.matrix?.time || 0).toFixed(4),
            (benchmarks.golden?.time || 0).toFixed(4)
        ];
        
        console.log(n.toString().padStart(6), ...results.map(r => (r + 'ms').padStart(12)));
    }
}

async function asyncDemonstration() {
    console.log('\n🔄 Async/Await Demonstration');
    console.log('=' .repeat(30));
    
    try {
        console.log('Computing F(10) with async...');
        const startTime = Date.now();
        const result = await fibonacciAsync(10, 0); // No delay for speed
        const endTime = Date.now();
        
        console.log(`Result: ${result}`);
        console.log(`Time: ${endTime - startTime}ms`);
        
        // Parallel computation simulation
        console.log('\nParallel computation simulation:');
        const parallelStart = Date.now();
        const parallelResults = await Promise.all([
            fibonacciParallel(20),
            fibonacciParallel(25),
            fibonacciParallel(30)
        ]);
        const parallelEnd = Date.now();
        
        console.log(`Results: [${parallelResults.join(', ')}]`);
        console.log(`Parallel time: ${parallelEnd - parallelStart}ms`);
        
    } catch (error) {
        console.error('Error in async demonstration:', error);
    }
}

// ============= MAIN EXECUTION =============

async function main() {
    demonstrateFibonacci();
    performanceBenchmark();
    await asyncDemonstration();
    
    console.log('\n✨ Fibonacci demonstration complete!');
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        fibonacciRecursive,
        fibonacciIterative,
        fibonacciMemoized,
        fibonacciDP,
        fibonacciMatrix,
        fibonacciGoldenRatio,
        fibonacciGenerator,
        fibonacciSequence,
        fibonacciRange,
        FibonacciCalculator,
        isFibonacciNumber,
        findFibonacciIndex,
        fibonacciSequenceArray,
        fibonacciSum,
        fibonacciUpTo,
        fibonacciAsync,
        fibonacciParallel,
        demonstrateFibonacci,
        performanceBenchmark,
        main
    };
}

// Run if in browser or Node.js
if (typeof window === 'undefined') {
    main().catch(console.error);
}
