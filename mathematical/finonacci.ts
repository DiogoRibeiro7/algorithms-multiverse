/**
 * Fibonacci Sequence Implementation in TypeScript
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
 * TypeScript features:
 * - Strong typing and interfaces
 * - Generics and union types
 * - Decorators and metadata
 * - Advanced type system
 * - Strict null checks
 */

// ============= TYPE DEFINITIONS =============

type FibonacciMethod = 'recursive' | 'iterative' | 'memoized' | 'dp' | 'matrix' | 'golden' | 'cached';

interface BenchmarkResult {
    method: FibonacciMethod;
    result: number | null;
    time: number;
    computations: number;
    error: string | null;
}

interface CacheStats {
    size: number;
    entries: [number, number][];
    hitRate?: number;
    missRate?: number;
}

interface FibonacciProperties {
    value: number;
    index: number;
    isFibonacci: boolean;
    nextFibonacci: number;
    previousFibonacci: number;
    goldenRatioApproximation?: number;
}

interface SequenceOptions {
    start?: number;
    count?: number;
    max?: number;
    includeIndex?: boolean;
}

type Matrix2x2 = [[number, number], [number, number]];

// ============= DECORATORS =============

function measure(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    
    descriptor.value = function(...args: any[]) {
        const start = performance.now();
        const result = originalMethod.apply(this, args);
        const end = performance.now();
        
        console.log(`${propertyKey} took ${(end - start).toFixed(4)}ms`);
        return result;
    };
    
    return descriptor;
}

function memoize(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    const cache = new Map<string, any>();
    
    descriptor.value = function(...args: any[]) {
        const key = JSON.stringify(args);
        
        if (cache.has(key)) {
            return cache.get(key);
        }
        
        const result = originalMethod.apply(this, args);
        cache.set(key, result);
        return result;
    };
    
    return descriptor;
}

// ============= BASIC IMPLEMENTATIONS =============

/**
 * Simple recursive implementation (inefficient)
 */
function fibonacciRecursive(n: number): number {
    if (n < 0) throw new Error('Negative numbers not supported');
    if (n <= 1) return n;
    return fibonacciRecursive(n - 1) + fibonacciRecursive(n - 2);
}

/**
 * Iterative implementation (efficient)
 */
function fibonacciIterative(n: number): number {
    if (n < 0) throw new Error('Negative numbers not supported');
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
    const cache = new Map<number, number>([[0, 0], [1, 1]]);
    
    return function fibonacci(n: number): number {
        if (n < 0) throw new Error('Negative numbers not supported');
        
        if (cache.has(n)) {
            return cache.get(n)!;
        }
        
        const result = fibonacci(n - 1) + fibonacci(n - 2);
        cache.set(n, result);
        return result;
    };
})();

/**
 * Dynamic programming bottom-up approach
 */
function fibonacciDP(n: number): number {
    if (n < 0) throw new Error('Negative numbers not supported');
    if (n <= 1) return n;
    
    const dp: number[] = new Array(n + 1);
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
function fibonacciMatrix(n: number): number {
    if (n < 0) throw new Error('Negative numbers not supported');
    if (n <= 1) return n;
    
    function multiplyMatrix(a: Matrix2x2, b: Matrix2x2): Matrix2x2 {
        return [
            [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]
        ];
    }
    
    function matrixPower(matrix: Matrix2x2, power: number): Matrix2x2 {
        if (power === 1) return matrix;
        
        if (power % 2 === 0) {
            const half = matrixPower(matrix, Math.floor(power / 2));
            return multiplyMatrix(half, half);
        } else {
            return multiplyMatrix(matrix, matrixPower(matrix, power - 1));
        }
    }
    
    const baseMatrix: Matrix2x2 = [[1, 1], [1, 0]];
    const resultMatrix = matrixPower(baseMatrix, n);
    return resultMatrix[0][1];
}

/**
 * Golden ratio formula (Binet's formula)
 */
function fibonacciGoldenRatio(n: number): number {
    if (n < 0) throw new Error('Negative numbers not supported');
    if (n <= 1) return n;
    
    const phi = (1 + Math.sqrt(5)) / 2;
    const psi = (1 - Math.sqrt(5)) / 2;
    
    return Math.round((Math.pow(phi, n) - Math.pow(psi, n)) / Math.sqrt(5));
}

// ============= GENERATOR FUNCTIONS =============

/**
 * Infinite Fibonacci generator
 */
function* fibonacciGenerator(): Generator<number, never, unknown> {
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
function* fibonacciSequence(count: number): Generator<number, void, unknown> {
    if (count <= 0) return;
    
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
function* fibonacciRange(start: number, end: number): Generator<number, void, unknown> {
    if (start < 0 || end < start) return;
    
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
    private cache: Map<number, number>;
    private computations: number;
    private cacheHits: number;
    private cacheMisses: number;
    
    constructor() {
        this.cache = new Map<number, number>([[0, 0], [1, 1]]);
        this.computations = 0;
        this.cacheHits = 0;
        this.cacheMisses = 0;
    }
    
    /**
     * Calculate Fibonacci number using specified method
     */
    calculate(n: number, method: FibonacciMethod = 'iterative'): number {
        this.computations = 0;
        
        const methods: Record<FibonacciMethod, (n: number) => number> = {
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
    
    @measure
    private recursive(n: number): number {
        this.computations++;
        if (n <= 1) return n;
        return this.recursive(n - 1) + this.recursive(n - 2);
    }
    
    @measure
    private iterative(n: number): number {
        this.computations++;
        return fibonacciIterative(n);
    }
    
    @memoize
    private memoized(n: number): number {
        this.computations++;
        if (n <= 1) return n;
        
        if (this.cache.has(n)) {
            this.cacheHits++;
            return this.cache.get(n)!;
        }
        
        this.cacheMisses++;
        const result = this.memoized(n - 1) + this.memoized(n - 2);
        this.cache.set(n, result);
        return result;
    }
    
    private dynamicProgramming(n: number): number {
        this.computations++;
        return fibonacciDP(n);
    }
    
    private matrixExponentiation(n: number): number {
        this.computations++;
        return fibonacciMatrix(n);
    }
    
    private goldenRatio(n: number): number {
        this.computations++;
        return fibonacciGoldenRatio(n);
    }
    
    private cached(n: number): number {
        this.computations++;
        if (this.cache.has(n)) {
            this.cacheHits++;
            return this.cache.get(n)!;
        }
        
        this.cacheMisses++;
        const result = this.iterative(n);
        this.cache.set(n, result);
        return result;
    }
    
    /**
     * Benchmark different methods
     */
    benchmark(n: number): Record<FibonacciMethod, BenchmarkResult> {
        const methods: FibonacciMethod[] = ['iterative', 'memoized', 'dp', 'matrix', 'golden'];
        if (n <= 35) methods.push('recursive'); // Avoid long recursive times
        
        const results: Record<string, BenchmarkResult> = {};
        
        for (const method of methods) {
            const startTime = performance.now();
            try {
                const result = this.calculate(n, method);
                const endTime = performance.now();
                
                results[method] = {
                    method,
                    result,
                    time: endTime - startTime,
                    computations: this.computations,
                    error: null
                };
            } catch (error) {
                results[method] = {
                    method,
                    result: null,
                    time: Infinity,
                    computations: this.computations,
                    error: error instanceof Error ? error.message : 'Unknown error'
                };
            }
        }
        
        return results as Record<FibonacciMethod, BenchmarkResult>;
    }
    
    /**
     * Get Fibonacci properties for a number
     */
    getProperties(n: number): FibonacciProperties {
        const value = this.calculate(n);
        const isFib = this.isFibonacciNumber(value);
        
        return {
            value,
            index: n,
            isFibonacci: isFib,
            nextFibonacci: this.calculate(n + 1),
            previousFibonacci: n > 0 ? this.calculate(n - 1) : 0,
            goldenRatioApproximation: n > 0 ? value / this.calculate(n - 1) : undefined
        };
    }
    
    /**
     * Clear the cache
     */
    clearCache(): void {
        this.cache.clear();
        this.cache.set(0, 0);
        this.cache.set(1, 1);
        this.cacheHits = 0;
        this.cacheMisses = 0;
    }
    
    /**
     * Get cache statistics
     */
    getCacheStats(): CacheStats {
        const total = this.cacheHits + this.cacheMisses;
        return {
            size: this.cache.size,
            entries: [...this.cache.entries()],
            hitRate: total > 0 ? this.cacheHits / total : 0,
            missRate: total > 0 ? this.cacheMisses / total : 0
        };
    }
    
    /**
     * Check if a number is a Fibonacci number
     */
    isFibonacciNumber(num: number): boolean {
        if (num < 0) return false;
        
        function isPerfectSquare(x: number): boolean {
            const root = Math.sqrt(x);
            return Math.floor(root) * Math.floor(root) === x;
        }
        
        return isPerfectSquare(5 * num * num + 4) || isPerfectSquare(5 * num * num - 4);
    }
}

// ============= UTILITY FUNCTIONS =============

/**
 * Find the index of a Fibonacci number
 */
function findFibonacciIndex(target: number): number {
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
function fibonacciSequenceArray(count: number): number[] {
    if (count <= 0) return [];
    if (count === 1) return [0];
    
    const sequence: number[] = [0, 1];
    
    for (let i = 2; i < count; i++) {
        sequence.push(sequence[i - 1] + sequence[i - 2]);
    }
    
    return sequence;
}

/**
 * Sum of first n Fibonacci numbers
 */
function fibonacciSum(n: number): number {
    if (n <= 0) return 0;
    
    // Sum of first n Fibonacci numbers = F(n+2) - 1
    return fibonacciIterative(n + 1) - 1;
}

/**
 * Get Fibonacci numbers up to a maximum value
 */
function fibonacciUpTo(max: number): number[] {
    const result: number[] = [];
    let a = 0, b = 1;
    
    while (a <= max) {
        result.push(a);
        [a, b] = [b, a + b];
    }
    
    return result;
}

/**
 * Generate Fibonacci sequence with options
 */
function generateSequence(options: SequenceOptions): number[] | { index: number; value: number }[] {
    const { start = 0, count = 10, max, includeIndex = false } = options;
    
    if (max !== undefined) {
        const upTo = fibonacciUpTo(max);
        return includeIndex 
            ? upTo.map((value, index) => ({ index, value }))
            : upTo;
    }
    
    const sequence: number[] = [];
    const gen = fibonacciRange(start, start + count - 1);
    
    for (const value of gen) {
        sequence.push(value);
    }
    
    return includeIndex 
        ? sequence.map((value, index) => ({ index: start + index, value }))
        : sequence;
}

// ============= ASYNC/AWAIT IMPLEMENTATIONS =============

/**
 * Async Fibonacci calculator with delay
 */
async function fibonacciAsync(n: number, delay: number = 1): Promise<number> {
    if (n <= 1) return n;
    
    await new Promise<void>(resolve => setTimeout(resolve, delay));
    
    const [a, b] = await Promise.all([
        fibonacciAsync(n - 1, delay),
        fibonacciAsync(n - 2, delay)
    ]);
    
    return a + b;
}

/**
 * Worker-based parallel Fibonacci (simulation)
 */
async function fibonacciParallel(n: number): Promise<number> {
    if (n <= 1) return n;
    if (n <= 30) return fibonacciIterative(n); // Use iterative for small numbers
    
    // Simulate parallel computation
    return new Promise<number>((resolve) => {
        setTimeout(() => {
            resolve(fibonacciIterative(n));
        }, Math.random() * 10);
    });
}

// ============= ADVANCED TYPES AND INTERFACES =============

interface FibonacciAnalysis {
    sequence: number[];
    properties: {
        goldenRatio: number;
        ratioApproximations: number[];
        sumOfSequence: number;
        evenCount: number;
        oddCount: number;
        primeCount: number;
    };
    patterns: {
        divisibleBy3: number[];
        divisibleBy5: number[];
        perfectSquares: number[];
    };
}

/**
 * Comprehensive Fibonacci analysis
 */
function analyzeFibonacci(count: number): FibonacciAnalysis {
    const sequence = fibonacciSequenceArray(count);
    const goldenRatio = (1 + Math.sqrt(5)) / 2;
    
    const ratioApproximations: number[] = [];
    for (let i = 1; i < sequence.length; i++) {
        if (sequence[i - 1] !== 0) {
            ratioApproximations.push(sequence[i] / sequence[i - 1]);
        }
    }
    
    function isPrime(num: number): boolean {
        if (num < 2) return false;
        for (let i = 2; i <= Math.sqrt(num); i++) {
            if (num % i === 0) return false;
        }
        return true;
    }
    
    function isPerfectSquare(num: number): boolean {
        const root = Math.sqrt(num);
        return Math.floor(root) * Math.floor(root) === num;
    }
    
    return {
        sequence,
        properties: {
            goldenRatio,
            ratioApproximations,
            sumOfSequence: sequence.reduce((sum, num) => sum + num, 0),
            evenCount: sequence.filter(num => num % 2 === 0).length,
            oddCount: sequence.filter(num => num % 2 !== 0).length,
            primeCount: sequence.filter(isPrime).length
        },
        patterns: {
            divisibleBy3: sequence.filter(num => num % 3 === 0),
            divisibleBy5: sequence.filter(num => num % 5 === 0),
            perfectSquares: sequence.filter(isPerfectSquare)
        }
    };
}

// ============= DEMONSTRATION AND TESTING =============

function demonstrateFibonacci(): void {
    console.log('🔢 Fibonacci Sequence Implementation in TypeScript');
    console.log('='.repeat(52));
    
    // Test different methods
    const testCases: number[] = [0, 1, 5, 10, 20, 30];
    console.log('\n📋 Method Comparison:');
    console.log('n'.padStart(3), 'Recursive'.padStart(12), 'Iterative'.padStart(12), 
                'Memoized'.padStart(12), 'Matrix'.padStart(12), 'Golden'.padStart(12));
    console.log('-'.repeat(65));
    
    const calculator = new FibonacciCalculator();
    
    for (const n of testCases) {
        const results: string[] = [];
        
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
    const first15: number[] = [];
    for (let i = 0; i < 15; i++) {
        first15.push(gen.next().value);
    }
    console.log(first15.map(n => n.toString().padStart(4)).join(' '));
    
    // Properties analysis
    console.log('\n📊 Fibonacci Properties for F(15):');
    const props = calculator.getProperties(15);
    console.log(`Value: ${props.value}`);
    console.log(`Is Fibonacci: ${props.isFibonacci}`);
    console.log(`Next: ${props.nextFibonacci}`);
    console.log(`Previous: ${props.previousFibonacci}`);
    if (props.goldenRatioApproximation) {
        console.log(`Ratio: ${props.goldenRatioApproximation.toFixed(6)}`);
    }
    
    // Advanced analysis
    console.log('\n🔍 Advanced Analysis (first 20):');
    const analysis = analyzeFibonacci(20);
    console.log(`Sum: ${analysis.properties.sumOfSequence}`);
    console.log(`Even count: ${analysis.properties.evenCount}`);
    console.log(`Odd count: ${analysis.properties.oddCount}`);
    console.log(`Prime count: ${analysis.properties.primeCount}`);
    console.log(`Divisible by 3: [${analysis.patterns.divisibleBy3.join(', ')}]`);
    console.log(`Perfect squares: [${analysis.patterns.perfectSquares.join(', ')}]`);
    
    // Cache statistics
    console.log('\n💾 Cache Statistics:');
    const stats = calculator.getCacheStats();
    console.log(`Cache size: ${stats.size}`);
    console.log(`Hit rate: ${((stats.hitRate || 0) * 100).toFixed(1)}%`);
    console.log(`Miss rate: ${((stats.missRate || 0) * 100).toFixed(1)}%`);
}

function performanceBenchmark(): void {
    console.log('\n⚡ Performance Benchmark');
    console.log('='.repeat(30));
    
    const calculator = new FibonacciCalculator();
    const testValues: number[] = [20, 30, 100, 500, 1000];
    
    console.log('n'.padStart(6), 'Iterative'.padStart(12), 'Memoized'.padStart(12), 
                'Matrix'.padStart(12), 'Golden'.padStart(12));
    console.log('-'.repeat(54));
    
    for (const n of testValues) {
        const benchmarks = calculator.benchmark(n);
        
        const results: string[] = [
            (benchmarks.iterative?.time || 0).toFixed(4),
            (benchmarks.memoized?.time || 0).toFixed(4),
            (benchmarks.matrix?.time || 0).toFixed(4),
            (benchmarks.golden?.time || 0).toFixed(4)
        ];
        
        console.log(n.toString().padStart(6), ...results.map(r => (r + 'ms').padStart(12)));
    }
}

async function asyncDemonstration(): Promise<void> {
    console.log('\n🔄 Async/Await Demonstration');
    console.log('='.repeat(30));
    
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

async function main(): Promise<void> {
    demonstrateFibonacci();
    performanceBenchmark();
    await asyncDemonstration();
    
    console.log('\n✨ Fibonacci demonstration complete!');
}

// Export for modules
export {
    FibonacciMethod,
    BenchmarkResult,
    CacheStats,
    FibonacciProperties,
    SequenceOptions,
    Matrix2x2,
    FibonacciAnalysis,
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
    findFibonacciIndex,
    fibonacciSequenceArray,
    fibonacciSum,
    fibonacciUpTo,
    generateSequence,
    fibonacciAsync,
    fibonacciParallel,
    analyzeFibonacci,
    demonstrateFibonacci,
    performanceBenchmark,
    main
};

// Run if in Node.js environment
if (typeof window === 'undefined') {
    main().catch(console.error);
}
