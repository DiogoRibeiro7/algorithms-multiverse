/**
 * Jump Search Algorithm Implementation
 *
 * Time Complexity: O(√n)
 * Space Complexity: O(1)
 *
 * WHEN TO USE JUMP SEARCH OVER BINARY SEARCH:
 * 1. When backward jumping is costly (e.g., tape storage, linked lists with forward pointers)
 * 2. When data is in a system where jumping is cheaper than repeated divisions
 * 3. As a middle ground between linear search O(n) and binary search O(log n)
 * 4. When you need predictable jump patterns for cache optimization
 *
 * PERFORMANCE CHARACTERISTICS:
 * - Optimal block size: √n (square root of array length)
 * - Better cache performance than binary search in some cases (sequential jumps)
 * - Fewer comparisons than linear search, more than binary search
 * - Good for uniformly distributed data on sequential storage
 *
 * ADVANTAGES OVER BINARY SEARCH:
 * - Only jumps forward (no backward movement)
 * - More cache-friendly due to sequential access pattern
 * - Simpler implementation with predictable memory access
 * - Better for systems where backward seeks are expensive
 */

/**
 * Perform jump search on a sorted array
 * @param {number[]} arr - Sorted array of numbers
 * @param {number} target - Value to search for
 * @returns {number} Index of target if found, -1 otherwise
 */
function jumpSearch(arr, target) {
    const n = arr.length;
    if (n === 0) return -1;

    // Calculate optimal jump size: √n
    const jump = Math.floor(Math.sqrt(n));
    let prev = 0;
    let curr = jump;

    // Jump through blocks until we find a block that might contain target
    while (curr < n && arr[curr] < target) {
        prev = curr;
        curr += jump;
    }

    // Linear search within the identified block
    for (let i = prev; i < Math.min(curr + 1, n); i++) {
        if (arr[i] === target) {
            return i;
        } else if (arr[i] > target) {
            return -1;
        }
    }

    return -1;
}

/**
 * Jump search with customizable block size for cache optimization
 * @param {number[]} arr - Sorted array of numbers
 * @param {number} target - Value to search for
 * @param {number|null} blockSize - Custom block size (default: √n)
 * @returns {number} Index of target if found, -1 otherwise
 */
function jumpSearchOptimized(arr, target, blockSize = null) {
    const n = arr.length;
    if (n === 0) return -1;

    // Use custom block size or default to √n
    const jump = blockSize || Math.floor(Math.sqrt(n));
    let prev = 0;
    let curr = jump;

    // Jump through blocks
    while (curr < n && arr[curr] < target) {
        prev = curr;
        curr += jump;
    }

    // Linear search in the block
    for (let i = prev; i < Math.min(curr + 1, n); i++) {
        if (arr[i] === target) return i;
        if (arr[i] > target) return -1;
    }

    return -1;
}

/**
 * Adaptive jump search that adjusts block size based on data distribution
 * @param {number[]} arr - Sorted array of numbers
 * @param {number} target - Value to search for
 * @returns {number} Index of target if found, -1 otherwise
 */
function adaptiveJumpSearch(arr, target) {
    const n = arr.length;
    if (n === 0) return -1;

    const initialJump = Math.floor(Math.sqrt(n));
    let jump = initialJump;
    let prev = 0;

    // Adaptive jumping: adjust jump size based on value differences
    while (prev < n && arr[Math.min(prev + jump, n - 1)] < target) {
        const nextIdx = Math.min(prev + jump, n - 1);

        // If we're getting close to target, reduce jump size
        if (nextIdx < n - 1) {
            const valueRange = arr[nextIdx] - arr[prev];
            const targetRange = target - arr[prev];

            // Estimate where target might be and adjust jump
            if (valueRange > 0) {
                const estimatedPosition = (targetRange / valueRange) * jump;
                jump = Math.max(1, Math.floor(estimatedPosition * 1.5));
            }
        }

        prev = nextIdx;
        if (prev >= n - 1) break;
    }

    // Linear search in the final block
    const start = Math.max(0, prev - initialJump);
    for (let i = start; i < Math.min(prev + initialJump, n); i++) {
        if (arr[i] === target) return i;
        if (arr[i] > target) return -1;
    }

    return -1;
}

// Performance testing and demonstration
if (require.main === module) {
    // Test correctness
    const testArr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29];
    console.log("Test Array:", testArr);
    console.log(`Jump Search for 15: Index ${jumpSearch(testArr, 15)}`);
    console.log(`Jump Search for 20: Index ${jumpSearch(testArr, 20)}`);
    console.log(`Jump Search for 1: Index ${jumpSearch(testArr, 1)}`);
    console.log(`Jump Search for 29: Index ${jumpSearch(testArr, 29)}`);

    // Performance comparison
    console.log("\n--- Performance Comparison ---");
    const sizes = [1000, 10000, 100000, 1000000];

    for (const size of sizes) {
        // Generate sorted array
        const arr = Array.from({length: size}, (_, i) => i * 2);
        const target = arr[Math.floor(Math.random() * arr.length)];

        // Jump search
        const jumpStart = performance.now();
        for (let i = 0; i < 1000; i++) {
            jumpSearch(arr, target);
        }
        const jumpTime = performance.now() - jumpStart;

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

        console.log(`\nArray size: ${size.toLocaleString()}`);
        console.log(`Jump Search: ${jumpTime.toFixed(3)}ms`);
        console.log(`Binary Search: ${binaryTime.toFixed(3)}ms`);
        console.log(`Ratio (Jump/Binary): ${(jumpTime/binaryTime).toFixed(2)}x`);
    }

    // Cache-friendly block size analysis
    console.log("\n--- Cache-Friendly Block Size Analysis ---");
    const largeArr = Array.from({length: 100000}, (_, i) => i * 2);
    const target = largeArr[Math.floor(Math.random() * largeArr.length)];

    const blockSizes = [32, 64, 128, 256, 512, 1024, Math.floor(Math.sqrt(largeArr.length))];

    for (const blockSize of blockSizes) {
        const start = performance.now();
        for (let i = 0; i < 1000; i++) {
            jumpSearchOptimized(largeArr, target, blockSize);
        }
        const elapsed = performance.now() - start;
        console.log(`Block size ${blockSize.toString().padStart(5)}: ${elapsed.toFixed(3)}ms`);
    }
}

module.exports = {
    jumpSearch,
    jumpSearchOptimized,
    adaptiveJumpSearch
};
