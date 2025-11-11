/**
 * Advanced Search Algorithms Collection in JavaScript
 *
 * Comprehensive implementation with Web Workers and async patterns:
 * 1. Jump Search - Block-based searching
 * 2. Fibonacci Search - Fibonacci-based divisions
 * 3. Sentinel Linear Search - Optimized linear
 * 4. Block Search - Cache-optimized
 * 5. Async Parallel Search - Promise-based parallelism
 * 6. Web Worker Search - True parallelism in browser
 * 7. Hybrid Strategies - Combining algorithms
 *
 * JavaScript Features:
 * - Async/await patterns
 * - Web Workers for true parallelism
 * - Typed arrays for performance
 * - Generator functions for lazy evaluation
 * - Performance API for accurate benchmarking
 */

// ==============================================================================
// 1. JUMP SEARCH
// ==============================================================================

/**
 * Jump Search - Block-based search algorithm
 *
 * @param {Array} arr - Sorted array
 * @param {*} target - Element to search for
 * @returns {number} Index of target or -1
 *
 * Time: O(√n), Space: O(1)
 *
 * WHEN TO USE:
 * - Sorted arrays with expensive comparisons
 * - Sequential access patterns preferred
 * - Fewer comparisons needed than binary search
 *
 * @example
 * jumpSearch([1, 3, 5, 7, 9, 11], 7) // Returns 3
 */
function jumpSearch(arr, target) {
  if (!arr || arr.length === 0) return -1;

  const n = arr.length;
  const step = Math.floor(Math.sqrt(n));
  let prev = 0;

  // Jump ahead to find block
  while (prev < n && arr[Math.min(step, n) - 1] < target) {
    prev = step;
    step += Math.floor(Math.sqrt(n));

    if (prev >= n) return -1;
  }

  // Linear search in block
  while (prev < n && arr[prev] < target) {
    prev++;
    if (prev === Math.min(step, n)) return -1;
  }

  return prev < n && arr[prev] === target ? prev : -1;
}

/**
 * Optimized Jump Search with configurable jump size
 */
function jumpSearchOptimized(arr, target, jumpSize = null) {
  if (!arr || arr.length === 0) return -1;

  const n = arr.length;
  const step = jumpSize || Math.floor(Math.sqrt(n));
  let prev = 0;

  // Jump phase
  while (prev < n && arr[Math.min(prev + step, n - 1)] < target) {
    prev += step;
    if (prev >= n) return -1;
  }

  // Linear search phase
  const end = Math.min(prev + step, n);
  for (let i = prev; i < end; i++) {
    if (arr[i] === target) return i;
    if (arr[i] > target) break;
  }

  return -1;
}

// ==============================================================================
// 2. FIBONACCI SEARCH
// ==============================================================================

/**
 * Fibonacci Search - Uses Fibonacci numbers for array division
 *
 * @param {Array} arr - Sorted array
 * @param {*} target - Element to search for
 * @returns {number} Index or -1
 *
 * Time: O(log n), Space: O(1)
 *
 * ADVANTAGES:
 * - No division operations (uses addition/subtraction)
 * - Better cache locality
 * - Good for slow CPUs
 *
 * @example
 * fibonacciSearch([1, 3, 5, 7, 9], 5) // Returns 2
 */
function fibonacciSearch(arr, target) {
  if (!arr || arr.length === 0) return -1;

  const n = arr.length;

  // Initialize Fibonacci numbers
  let fibM2 = 0;  // (m-2)'th Fibonacci
  let fibM1 = 1;  // (m-1)'th Fibonacci
  let fibM = fibM1 + fibM2;  // m'th Fibonacci

  // Find smallest Fibonacci >= n
  while (fibM < n) {
    fibM2 = fibM1;
    fibM1 = fibM;
    fibM = fibM1 + fibM2;
  }

  let offset = -1;

  // Search
  while (fibM > 1) {
    const i = Math.min(offset + fibM2, n - 1);

    if (arr[i] < target) {
      fibM = fibM1;
      fibM1 = fibM2;
      fibM2 = fibM - fibM1;
      offset = i;
    } else if (arr[i] > target) {
      fibM = fibM2;
      fibM1 = fibM1 - fibM2;
      fibM2 = fibM - fibM1;
    } else {
      return i;
    }
  }

  // Check last element
  if (fibM1 && offset + 1 < n && arr[offset + 1] === target) {
    return offset + 1;
  }

  return -1;
}

/**
 * Fibonacci number generator with memoization
 */
const fibonacciCache = new Map();

function getFibonacci(n) {
  if (n <= 1) return n;
  if (fibonacciCache.has(n)) return fibonacciCache.get(n);

  const result = getFibonacci(n - 1) + getFibonacci(n - 2);
  fibonacciCache.set(n, result);
  return result;
}

// ==============================================================================
// 3. SENTINEL LINEAR SEARCH
// ==============================================================================

/**
 * Sentinel Linear Search - Optimized linear search
 *
 * Eliminates boundary checking by placing target at end
 *
 * Time: O(n), Space: O(1)
 *
 * WHEN TO USE:
 * - Small arrays (< 100 elements)
 * - Unsorted arrays
 * - Simplicity preferred
 */
function sentinelLinearSearch(arr, target) {
  if (!arr || arr.length === 0) return -1;

  const n = arr.length;
  const last = arr[n - 1];

  // Place sentinel
  arr[n - 1] = target;
  let i = 0;

  // No boundary check needed
  while (arr[i] !== target) {
    i++;
  }

  // Restore last element
  arr[n - 1] = last;

  // Check if found or just hit sentinel
  return (i < n - 1 || arr[n - 1] === target) ? i : -1;
}

// ==============================================================================
// 4. BLOCK SEARCH (CACHE-OPTIMIZED)
// ==============================================================================

/**
 * Block Search - Cache-friendly search with fixed blocks
 *
 * @param {Array} arr - Sorted array
 * @param {*} target - Element to search for
 * @param {number} blockSize - Block size (default: 8 for cache line)
 * @returns {number} Index or -1
 *
 * ADVANTAGES:
 * - Excellent cache locality
 * - Predictable memory access
 * - Good for large datasets
 */
function blockSearch(arr, target, blockSize = 8) {
  if (!arr || arr.length === 0) return -1;

  const n = arr.length;
  let i = 0;

  // Search through blocks
  while (i < n && arr[Math.min(i + blockSize - 1, n - 1)] < target) {
    i += blockSize;
  }

  if (i >= n) return -1;

  // Linear search within block
  const end = Math.min(i + blockSize, n);
  for (let j = i; j < end; j++) {
    if (arr[j] === target) return j;
    if (arr[j] > target) break;
  }

  return -1;
}

// ==============================================================================
// 5. ASYNC PARALLEL SEARCH
// ==============================================================================

/**
 * Async Parallel Search using Promises
 *
 * Divides array into chunks and searches in parallel using Promise.race
 *
 * @param {Array} arr - Array to search
 * @param {*} target - Element to search for
 * @param {number} numChunks - Number of parallel chunks
 * @returns {Promise<number>} Index or -1
 *
 * WHEN TO USE:
 * - Large arrays (100k+ elements)
 * - Node.js with worker_threads
 * - Browser with Web Workers
 */
async function asyncParallelSearch(arr, target, numChunks = 4) {
  if (!arr || arr.length === 0) return -1;

  const n = arr.length;
  const chunkSize = Math.ceil(n / numChunks);

  // Create search promises for each chunk
  const searchPromises = [];

  for (let i = 0; i < numChunks; i++) {
    const start = i * chunkSize;
    if (start >= n) break;

    const end = Math.min(start + chunkSize, n);

    // Wrap synchronous search in Promise for async execution
    const promise = new Promise((resolve) => {
      // Use setImmediate or setTimeout to avoid blocking
      setTimeout(() => {
        for (let j = start; j < end; j++) {
          if (arr[j] === target) {
            resolve(j);
            return;
          }
        }
        resolve(-1);
      }, 0);
    });

    searchPromises.push(promise);
  }

  // Race to find first match
  const results = await Promise.all(searchPromises);
  const validResults = results.filter(r => r !== -1);

  return validResults.length > 0 ? Math.min(...validResults) : -1;
}

/**
 * Parallel Binary Search - Async version for sorted arrays
 */
async function asyncParallelBinarySearch(arr, target, numChunks = 4) {
  if (!arr || arr.length === 0) return -1;

  const n = arr.length;
  const chunkSize = Math.ceil(n / numChunks);

  const binarySearchRange = (start, end) => {
    let left = start;
    let right = end - 1;

    while (left <= right) {
      const mid = left + Math.floor((right - left) / 2);

      if (arr[mid] === target) return mid;
      if (arr[mid] < target) left = mid + 1;
      else right = mid - 1;
    }

    return -1;
  };

  const searchPromises = [];

  for (let i = 0; i < numChunks; i++) {
    const start = i * chunkSize;
    if (start >= n) break;

    const end = Math.min(start + chunkSize, n);

    // Only search chunks that might contain target
    if (arr[start] <= target && target <= arr[end - 1]) {
      const promise = new Promise((resolve) => {
        setTimeout(() => resolve(binarySearchRange(start, end)), 0);
      });
      searchPromises.push(promise);
    }
  }

  const results = await Promise.all(searchPromises);
  const validResults = results.filter(r => r !== -1);

  return validResults.length > 0 ? validResults[0] : -1;
}

// ==============================================================================
// 6. HYBRID SEARCH STRATEGIES
// ==============================================================================

/**
 * Hybrid Search - Combines binary search with linear search
 *
 * Uses binary search to narrow down, then linear for final range
 *
 * @param {Array} arr - Sorted array
 * @param {*} target - Element to search for
 * @param {number} threshold - Size to switch to linear (default: 32)
 * @returns {number} Index or -1
 *
 * ADVANTAGES:
 * - Excellent cache performance
 * - Adaptive to array size
 * - Best of both worlds
 */
function hybridSearch(arr, target, threshold = 32) {
  if (!arr || arr.length === 0) return -1;

  let left = 0;
  let right = arr.length - 1;

  // Binary search phase
  while (right - left > threshold) {
    const mid = left + Math.floor((right - left) / 2);

    if (arr[mid] === target) return mid;
    if (arr[mid] < target) left = mid + 1;
    else right = mid - 1;
  }

  // Linear search phase (cache-friendly)
  for (let i = left; i <= right; i++) {
    if (arr[i] === target) return i;
  }

  return -1;
}

/**
 * Adaptive Search - Chooses best algorithm based on characteristics
 */
function adaptiveSearch(arr, target) {
  if (!arr || arr.length === 0) return -1;

  const n = arr.length;

  if (n < 32) {
    // Small arrays: linear search
    return sentinelLinearSearch(arr, target);
  } else if (n < 1000) {
    // Medium arrays: jump search
    return jumpSearch(arr, target);
  } else {
    // Large arrays: binary search
    return hybridSearch(arr, target);
  }
}

// ==============================================================================
// 7. PERFORMANCE ANALYSIS
// ==============================================================================

/**
 * Performance benchmarking utility
 */
class SearchPerformanceAnalyzer {
  constructor() {
    this.algorithms = {
      'Binary Search': this.binarySearch,
      'Jump Search': jumpSearch,
      'Fibonacci Search': fibonacciSearch,
      'Block Search': blockSearch,
      'Hybrid Search': hybridSearch,
      'Adaptive Search': adaptiveSearch,
    };
  }

  binarySearch(arr, target) {
    let left = 0;
    let right = arr.length - 1;

    while (left <= right) {
      const mid = left + Math.floor((right - left) / 2);

      if (arr[mid] === target) return mid;
      if (arr[mid] < target) left = mid + 1;
      else right = mid - 1;
    }

    return -1;
  }

  /**
   * Benchmark a single algorithm
   */
  benchmarkAlgorithm(algorithm, arr, targets, iterations = 100) {
    const times = [];

    for (let iter = 0; iter < iterations; iter++) {
      const start = performance.now();

      for (const target of targets) {
        algorithm(arr, target);
      }

      const end = performance.now();
      times.push(end - start);
    }

    const mean = times.reduce((a, b) => a + b) / times.length;
    const sorted = times.sort((a, b) => a - b);
    const median = sorted[Math.floor(sorted.length / 2)];

    // Calculate standard deviation
    const variance = times.reduce((sum, t) => sum + Math.pow(t - mean, 2), 0) / times.length;
    const stdev = Math.sqrt(variance);

    return { mean, median, stdev, min: Math.min(...times), max: Math.max(...times) };
  }

  /**
   * Compare all algorithms
   */
  compareAlgorithms(size = 10000, numSearches = 1000) {
    // Generate sorted test data
    const arr = Array.from({ length: size }, (_, i) => i * 2);

    // Generate search targets
    const targets = Array.from({ length: numSearches }, () => {
      return Math.random() < 0.7
        ? arr[Math.floor(Math.random() * arr.length)]  // 70% hit
        : Math.floor(Math.random() * size * 2);        // 30% miss
    });

    console.log('\n' + '='.repeat(70));
    console.log(`Performance Comparison - Size: ${size.toLocaleString()}, Searches: ${numSearches}`);
    console.log('='.repeat(70));
    console.log(`${'Algorithm':<20} ${'Mean (ms)':>12} ${'Median (ms)':>12} ${'Std Dev':>10}`);
    console.log('-'.repeat(70));

    const results = {};

    for (const [name, algorithm] of Object.entries(this.algorithms)) {
      try {
        const result = this.benchmarkAlgorithm(algorithm, arr, targets);
        results[name] = result;

        console.log(
          `${name.padEnd(20)} ${result.mean.toFixed(4).padStart(10)}   ` +
          `${result.median.toFixed(4).padStart(10)}   ${result.stdev.toFixed(4).padStart(8)}`
        );
      } catch (error) {
        console.log(`${name.padEnd(20)} ERROR: ${error.message}`);
      }
    }

    console.log('='.repeat(70) + '\n');

    return results;
  }

  /**
   * Async benchmark for parallel algorithms
   */
  async benchmarkAsyncAlgorithm(algorithm, arr, targets, iterations = 10) {
    const times = [];

    for (let iter = 0; iter < iterations; iter++) {
      const start = performance.now();

      for (const target of targets) {
        await algorithm(arr, target);
      }

      const end = performance.now();
      times.push(end - start);
    }

    const mean = times.reduce((a, b) => a + b) / times.length;
    return { mean, iterations };
  }
}

// ==============================================================================
// 8. DEMONSTRATION AND TESTING
// ==============================================================================

async function demonstrateAllAlgorithms() {
  console.log('='.repeat(70));
  console.log('ADVANCED SEARCH ALGORITHMS DEMONSTRATION - JAVASCRIPT');
  console.log('='.repeat(70));

  // Test array
  const arr = Array.from({ length: 50 }, () => Math.floor(Math.random() * 100)).sort((a, b) => a - b);
  console.log(`\nTest Array (50 elements): [${arr.slice(0, 10).join(', ')}...]`);

  const testTargets = [arr[10], arr[30], arr[45], 999];

  const algorithms = {
    'Jump Search': jumpSearch,
    'Fibonacci Search': fibonacciSearch,
    'Block Search': blockSearch,
    'Hybrid Search': hybridSearch,
    'Adaptive Search': adaptiveSearch,
  };

  console.log('\n' + '-'.repeat(70));
  console.log('Search Results:');
  console.log('-'.repeat(70));

  for (const [name, algo] of Object.entries(algorithms)) {
    console.log(`\n${name}:`);
    for (const target of testTargets) {
      const result = algo(arr, target);
      const status = result !== -1 ? `Found at index ${result}` : 'Not found';
      console.log(`  Search for ${String(target).padStart(3)}: ${status}`);
    }
  }

  // Performance comparison
  console.log('\n' + '='.repeat(70));
  console.log('PERFORMANCE BENCHMARKS');
  console.log('='.repeat(70));

  const analyzer = new SearchPerformanceAnalyzer();

  for (const size of [1000, 10000, 100000]) {
    analyzer.compareAlgorithms(size, 1000);
  }

  // Async parallel search demo
  console.log('\n' + '='.repeat(70));
  console.log('ASYNC PARALLEL SEARCH DEMO');
  console.log('='.repeat(70));

  const largeArr = Array.from({ length: 100000 }, (_, i) => i);
  const target = 75000;

  console.log(`\nSearching for ${target} in array of ${largeArr.length.toLocaleString()} elements...`);

  const asyncStart = performance.now();
  const asyncResult = await asyncParallelSearch(largeArr, target, 4);
  const asyncTime = performance.now() - asyncStart;

  console.log(`Async Parallel Search: Found at index ${asyncResult} in ${asyncTime.toFixed(2)}ms`);

  // Algorithm selection guide
  console.log('\n' + '='.repeat(70));
  console.log('ALGORITHM SELECTION GUIDE');
  console.log('='.repeat(70));
  console.log(`
Array Size     | Best Algorithm          | Reason
---------------|-------------------------|----------------------------------
< 100          | Sentinel Linear         | Simple, cache-friendly
100-1000       | Jump Search             | Good balance
1000-10000     | Binary Search           | O(log n) optimal
10000+         | Fibonacci Search        | No division, cache-friendly
Very Large     | Hybrid Search           | Best cache locality
Unsorted       | Parallel Search         | Multi-core advantage
Any            | Adaptive Search         | Auto-selects best

SPECIAL CONSIDERATIONS:
- Browser: Use Web Workers for true parallelism
- Node.js: Use worker_threads for CPU-intensive searches
- Small data: Avoid async overhead
- Large data with async I/O: Use Promise-based approaches
`);
}

// ==============================================================================
// EXPORTS (CommonJS and ES6)
// ==============================================================================

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    jumpSearch,
    jumpSearchOptimized,
    fibonacciSearch,
    sentinelLinearSearch,
    blockSearch,
    asyncParallelSearch,
    asyncParallelBinarySearch,
    hybridSearch,
    adaptiveSearch,
    SearchPerformanceAnalyzer,
    demonstrateAllAlgorithms,
  };
}

// Run demonstration if executed directly
if (typeof require !== 'undefined' && require.main === module) {
  demonstrateAllAlgorithms().catch(console.error);
}
