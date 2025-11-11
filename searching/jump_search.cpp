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
 * MEMORY ACCESS OPTIMIZATION:
 * - Sequential access pattern improves CPU cache utilization
 * - Prefetching works better with predictable jump patterns
 * - Reduced cache misses compared to binary search's random access
 * - Better performance on hardware with slow random access (HDD, tape)
 */

#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>
#include <algorithm>
#include <random>
#include <iomanip>

/**
 * Perform jump search on a sorted array
 * @param arr Sorted vector of integers
 * @param target Value to search for
 * @return Index of target if found, -1 otherwise
 */
int jumpSearch(const std::vector<int>& arr, int target) {
    int n = arr.size();
    if (n == 0) return -1;

    // Calculate optimal jump size: √n
    int jump = static_cast<int>(std::sqrt(n));
    int prev = 0;
    int curr = jump;

    // Jump through blocks until we find a block that might contain target
    while (curr < n && arr[curr] < target) {
        prev = curr;
        curr += jump;
    }

    // Linear search within the identified block
    for (int i = prev; i < std::min(curr + 1, n); i++) {
        if (arr[i] == target) {
            return i;
        } else if (arr[i] > target) {
            return -1;
        }
    }

    return -1;
}

/**
 * Jump search with customizable block size for cache optimization
 * Cache line sizes are typically 64 bytes (16 ints), so block sizes
 * that are multiples of this tend to perform better
 */
int jumpSearchOptimized(const std::vector<int>& arr, int target, int blockSize = -1) {
    int n = arr.size();
    if (n == 0) return -1;

    // Use custom block size or default to √n
    int jump = (blockSize == -1) ? static_cast<int>(std::sqrt(n)) : blockSize;
    jump = std::max(1, jump);

    int prev = 0;
    int curr = jump;

    // Jump through blocks
    while (curr < n && arr[curr] < target) {
        prev = curr;
        curr += jump;
    }

    // Linear search in the block
    for (int i = prev; i < std::min(curr + 1, n); i++) {
        if (arr[i] == target) return i;
        if (arr[i] > target) return -1;
    }

    return -1;
}

/**
 * Cache-aligned jump search using __builtin_prefetch for even better performance
 * This version explicitly prefetches data to optimize cache usage
 */
int jumpSearchPrefetch(const std::vector<int>& arr, int target) {
    int n = arr.size();
    if (n == 0) return -1;

    int jump = static_cast<int>(std::sqrt(n));
    int prev = 0;
    int curr = jump;

    // Jump through blocks with prefetching
    while (curr < n && arr[curr] < target) {
        prev = curr;
        curr += jump;

        // Prefetch next block
        if (curr + jump < n) {
            __builtin_prefetch(&arr[curr + jump], 0, 1);
        }
    }

    // Linear search with prefetching
    int end = std::min(curr + 1, n);
    for (int i = prev; i < end; i++) {
        // Prefetch ahead in the linear search
        if (i + 8 < end) {
            __builtin_prefetch(&arr[i + 8], 0, 1);
        }

        if (arr[i] == target) return i;
        if (arr[i] > target) return -1;
    }

    return -1;
}

/**
 * Adaptive jump search that adjusts block size based on data distribution
 */
int adaptiveJumpSearch(const std::vector<int>& arr, int target) {
    int n = arr.size();
    if (n == 0) return -1;

    int initialJump = static_cast<int>(std::sqrt(n));
    int jump = initialJump;
    int prev = 0;

    // Adaptive jumping
    while (prev < n && arr[std::min(prev + jump, n - 1)] < target) {
        int nextIdx = std::min(prev + jump, n - 1);

        if (nextIdx < n - 1) {
            long long valueRange = static_cast<long long>(arr[nextIdx]) - arr[prev];
            long long targetRange = static_cast<long long>(target) - arr[prev];

            if (valueRange > 0) {
                double estimatedPosition = (static_cast<double>(targetRange) / valueRange) * jump;
                jump = std::max(1, static_cast<int>(estimatedPosition * 1.5));
            }
        }

        prev = nextIdx;
        if (prev >= n - 1) break;
    }

    // Linear search in the final block
    int start = std::max(0, prev - initialJump);
    for (int i = start; i < std::min(prev + initialJump, n); i++) {
        if (arr[i] == target) return i;
        if (arr[i] > target) return -1;
    }

    return -1;
}

/**
 * Binary search for comparison
 */
int binarySearch(const std::vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

int main() {
    // Test correctness
    std::vector<int> testArr = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29};
    std::cout << "Test Array: ";
    for (int x : testArr) std::cout << x << " ";
    std::cout << "\n";

    std::cout << "Jump Search for 15: Index " << jumpSearch(testArr, 15) << "\n";
    std::cout << "Jump Search for 20: Index " << jumpSearch(testArr, 20) << "\n";
    std::cout << "Jump Search for 1: Index " << jumpSearch(testArr, 1) << "\n";
    std::cout << "Jump Search for 29: Index " << jumpSearch(testArr, 29) << "\n";

    // Performance comparison
    std::cout << "\n--- Performance Comparison ---\n";
    std::vector<int> sizes = {1000, 10000, 100000, 1000000};
    std::random_device rd;
    std::mt19937 gen(42);

    for (int size : sizes) {
        std::vector<int> arr(size);
        for (int i = 0; i < size; i++) {
            arr[i] = i * 2;
        }

        std::uniform_int_distribution<> dis(0, arr.size() - 1);
        int target = arr[dis(gen)];

        // Jump search
        auto start = std::chrono::high_resolution_clock::now();
        for (int i = 0; i < 10000; i++) {
            jumpSearch(arr, target);
        }
        auto end = std::chrono::high_resolution_clock::now();
        auto jumpTime = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

        // Jump search with prefetch
        start = std::chrono::high_resolution_clock::now();
        for (int i = 0; i < 10000; i++) {
            jumpSearchPrefetch(arr, target);
        }
        end = std::chrono::high_resolution_clock::now();
        auto prefetchTime = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

        // Binary search
        start = std::chrono::high_resolution_clock::now();
        for (int i = 0; i < 10000; i++) {
            binarySearch(arr, target);
        }
        end = std::chrono::high_resolution_clock::now();
        auto binaryTime = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

        std::cout << "\nArray size: " << size << "\n";
        std::cout << "Jump Search: " << std::fixed << std::setprecision(3)
                  << jumpTime / 1000.0 << "ms\n";
        std::cout << "Jump Search (prefetch): " << prefetchTime / 1000.0 << "ms\n";
        std::cout << "Binary Search: " << binaryTime / 1000.0 << "ms\n";
        std::cout << "Ratio (Jump/Binary): " << std::setprecision(2)
                  << static_cast<double>(jumpTime) / binaryTime << "x\n";
        std::cout << "Ratio (Prefetch/Binary): "
                  << static_cast<double>(prefetchTime) / binaryTime << "x\n";
    }

    // Cache-friendly block size analysis
    std::cout << "\n--- Cache-Friendly Block Size Analysis ---\n";
    std::vector<int> largeArr(100000);
    for (int i = 0; i < 100000; i++) {
        largeArr[i] = i * 2;
    }
    std::uniform_int_distribution<> dis(0, largeArr.size() - 1);
    int target = largeArr[dis(gen)];

    std::vector<int> blockSizes = {16, 32, 64, 128, 256, 512, 1024,
                                    static_cast<int>(std::sqrt(largeArr.size()))};

    for (int blockSize : blockSizes) {
        auto start = std::chrono::high_resolution_clock::now();
        for (int i = 0; i < 10000; i++) {
            jumpSearchOptimized(largeArr, target, blockSize);
        }
        auto end = std::chrono::high_resolution_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

        std::cout << "Block size " << std::setw(5) << blockSize << ": "
                  << std::fixed << std::setprecision(3) << elapsed / 1000.0 << "ms\n";
    }

    return 0;
}
