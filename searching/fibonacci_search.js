/**
 * Fibonacci Search Algorithm Implementation
 *
 * Time Complexity: O(log n)
 * Space Complexity: O(1)
 *
 * WHEN TO USE FIBONACCI SEARCH OVER BINARY SEARCH:
 * 1. When division/multiplication operations are costly (embedded systems, old CPUs)
 * 2. For data stored on magnetic tapes or systems where jumping backward is expensive
 * 3. When you want to minimize comparisons on average (fewer than binary search)
 * 4. For uniformly distributed sorted data
 *
 * PERFORMANCE CHARACTERISTICS:
 * - Uses Fibonacci numbers to divide the array (golden ratio divisions)
 * - Only uses addition and subtraction (no division or multiplication)
 * - Average case: slightly fewer comparisons than binary search
 * - Works well with sequential access patterns
 * - Better cache performance than binary search in some scenarios
 *
 * ADVANTAGES OVER BINARY SEARCH:
 * - Avoids expensive division operations
 * - Only moves forward (good for tape storage, linked lists)
 * - Golden ratio division can be more optimal for uniformly distributed data
 */

/**
 * Perform Fibonacci search on a sorted array
 * @param {number[]} arr - Sorted array of numbers
 * @param {number} target - Value to search for
 * @returns {number} Index of target if found, -1 otherwise
 */
function fibonacciSearch(arr, target) {
    const n = arr.length;
    if (n === 0) return -1;

    // Initialize Fibonacci numbers
    let fibM2 = 0;  // (m-2)'th Fibonacci number
    let fibM1 = 1;  // (m-1)'th Fibonacci number
    let fibM = fibM2 + fibM1;  // m'th Fibonacci number

    // Find the smallest Fibonacci number >= n
    while (fibM < n) {
        fibM2 = fibM1;
        fibM1 = fibM;
        fibM = fibM2 + fibM1;
    }

    // Marks the eliminated range from front
    let offset = -1;

    // While there are elements to be inspected
    while (fibM > 1) {
        // Check if fibM2 is a valid index
        const i = Math.min(offset + fibM2, n - 1);

        // If target is greater than the value at index fibM2
        if (arr[i] < target) {
            fibM = fibM1;
            fibM1 = fibM2;
            fibM2 = fibM - fibM1;
            offset = i;
        }
        // If target is less than the value at index fibM2
        else if (arr[i] > target) {
            fibM = fibM2;
            fibM1 = fibM1 - fibM2;
            fibM2 = fibM - fibM1;
        }
        // Element found
        else {
            return i;
        }
    }

    // Compare the last element
    if (fibM1 && offset + 1 < n && arr[offset + 1] === target) {
        return offset + 1;
    }

    return -1;
}

/**
 * Alternative Fibonacci search with clearer iteration logic
 * @param {number[]} arr - Sorted array of numbers
 * @param {number} target - Value to search for
 * @returns {number} Index of target if found, -1 otherwise
 */
function fibonacciSearchIterative(arr, target) {
    const n = arr.length;
    if (n === 0) return -1;

    // Generate Fibonacci numbers up to n
    const fibs = [0, 1];
    while (fibs[fibs.length - 1] < n) {
        const len = fibs.length;
        fibs.push(fibs[len - 1] + fibs[len - 2]);
    }

    // Start with the largest Fibonacci number <= n
    let k = fibs.length - 1;
    let offset = 0;

    while (k > 0) {
        // Calculate the index to check
        const idx = Math.min(offset + fibs[k - 1] - 1, n - 1);

        if (arr[idx] === target) {
            return idx;
        } else if (arr[idx] < target) {
            // Move offset forward
            offset = idx + 1;
            k -= 1;
        } else {
            // Reduce the Fibonacci index
            k -= 2;
        }

        // Check if we've exhausted the search space
        if (offset >= n) {
            break;
        }
    }

    return -1;
}

/**
 * Optimized Fibonacci search with early termination
 * @param {number[]} arr - Sorted array of numbers
 * @param {number} target - Value to search for
 * @returns {number} Index of target if found, -1 otherwise
 */
function fibonacciSearchOptimized(arr, target) {
    const n = arr.length;
    if (n === 0) return -1;

    // Quick boundary checks
    if (target < arr[0] || target > arr[n - 1]) {
        return -1;
    }
    if (arr[0] === target) return 0;
    if (arr[n - 1] === target) return n - 1;

    // Initialize Fibonacci numbers
    let fibM2 = 0, fibM1 = 1, fibM = fibM2 + fibM1;

    while (fibM < n) {
        fibM2 = fibM1;
        fibM1 = fibM;
        fibM = fibM2 + fibM1;
    }

    let offset = -1;

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

    if (fibM1 && offset + 1 < n && arr[offset + 1] === target) {
        return offset + 1;
    }

    return -1;
}

// Performance testing and demonstration
if (require.main === module) {
    // Test correctness
    const testArr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29];
    console.log("Test Array:", testArr);
    console.log(`Fibonacci Search for 15: Index ${fibonacciSearch(testArr, 15)}`);
    console.log(`Fibonacci Search for 20: Index ${fibonacciSearch(testArr, 20)}`);
    console.log(`Fibonacci Search for 1: Index ${fibonacciSearch(testArr, 1)}`);
    console.log(`Fibonacci Search for 29: Index ${fibonacciSearch(testArr, 29)}`);

    // Performance comparison
    console.log("\n--- Performance Comparison ---");
    const sizes = [1000, 10000, 100000, 1000000];

    for (const size of sizes) {
        // Generate sorted array
        const arr = Array.from({length: size}, (_, i) => i * 2);
        const target = arr[Math.floor(Math.random() * arr.length)];

        // Fibonacci search
        const fibStart = performance.now();
        for (let i = 0; i < 1000; i++) {
            fibonacciSearch(arr, target);
        }
        const fibTime = performance.now() - fibStart;

        // Binary search for comparison
        const binarySearch = (arr, target) => {
            let left = 0, right = arr.length - 1;
            while (left <= right) {
                const mid = Math.floor((left + right) / 2);
                if (arr[mid] === target) return mid;
                if (arr[mid] < target) left = mid + 1;
                else right = mid - 1;
            }
            return -1;
        };

        const binaryStart = performance.now();
        for (let i = 0; i < 1000; i++) {
            binarySearch(arr, target);
        }
        const binaryTime = performance.now() - binaryStart;

        // Jump search for comparison
        const jumpSearch = (arr, target) => {
            const n = arr.length;
            const jump = Math.floor(Math.sqrt(n));
            let prev = 0;
            while (prev < n && arr[Math.min(prev + jump, n - 1)] < target) {
                prev += jump;
            }
            for (let i = Math.max(0, prev - jump); i < Math.min(prev + jump, n); i++) {
                if (arr[i] === target) return i;
            }
            return -1;
        };

        const jumpStart = performance.now();
        for (let i = 0; i < 1000; i++) {
            jumpSearch(arr, target);
        }
        const jumpTime = performance.now() - jumpStart;

        console.log(`\nArray size: ${size.toLocaleString()}`);
        console.log(`Fibonacci Search: ${fibTime.toFixed(3)}ms`);
        console.log(`Binary Search: ${binaryTime.toFixed(3)}ms`);
        console.log(`Jump Search: ${jumpTime.toFixed(3)}ms`);
        console.log(`Ratio (Fib/Binary): ${(fibTime/binaryTime).toFixed(2)}x`);
        console.log(`Ratio (Fib/Jump): ${(fibTime/jumpTime).toFixed(2)}x`);
    }

    // Performance on different data distributions
    console.log("\n--- Performance on Different Data Distributions ---");

    // Uniform distribution
    const arrUniform = Array.from({length: 100000}, (_, i) => i);
    const target1 = 75000;

    const uniformStart = performance.now();
    for (let i = 0; i < 10000; i++) {
        fibonacciSearch(arrUniform, target1);
    }
    const uniformTime = performance.now() - uniformStart;
    console.log(`Uniform distribution: ${uniformTime.toFixed(3)}ms`);

    // Sparse distribution
    const arrSparse = Array.from({length: 10000}, (_, i) => i * 10);
    const target2 = 750000;

    const sparseStart = performance.now();
    for (let i = 0; i < 10000; i++) {
        fibonacciSearch(arrSparse, target2);
    }
    const sparseTime = performance.now() - sparseStart;
    console.log(`Sparse distribution: ${sparseTime.toFixed(3)}ms`);
}

module.exports = {
    fibonacciSearch,
    fibonacciSearchIterative,
    fibonacciSearchOptimized
};
