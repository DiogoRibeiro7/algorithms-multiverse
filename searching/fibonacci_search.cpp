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
 * - Golden ratio (φ ≈ 1.618) provides optimal division points for uniform data
 */

#include <iostream>
#include <vector>
#include <chrono>
#include <algorithm>
#include <random>
#include <iomanip>
#include <cmath>

/**
 * Perform Fibonacci search on a sorted array
 */
int fibonacciSearch(const std::vector<int>& arr, int target) {
    int n = arr.size();
    if (n == 0) return -1;

    // Initialize Fibonacci numbers
    int fibM2 = 0;  // (m-2)'th Fibonacci number
    int fibM1 = 1;  // (m-1)'th Fibonacci number
    int fibM = fibM2 + fibM1;  // m'th Fibonacci number

    // Find the smallest Fibonacci number >= n
    while (fibM < n) {
        fibM2 = fibM1;
        fibM1 = fibM;
        fibM = fibM2 + fibM1;
    }

    // Marks the eliminated range from front
    int offset = -1;

    // While there are elements to be inspected
    while (fibM > 1) {
        // Check if fibM2 is a valid index
        int i = std::min(offset + fibM2, n - 1);

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
    if (fibM1 && offset + 1 < n && arr[offset + 1] == target) {
        return offset + 1;
    }

    return -1;
}

/**
 * Optimized Fibonacci search with early termination
 */
int fibonacciSearchOptimized(const std::vector<int>& arr, int target) {
    int n = arr.size();
    if (n == 0) return -1;

    // Quick boundary checks
    if (target < arr[0] || target > arr[n - 1]) {
        return -1;
    }
    if (arr[0] == target) return 0;
    if (arr[n - 1] == target) return n - 1;

    // Initialize Fibonacci numbers
    int fibM2 = 0, fibM1 = 1, fibM = fibM2 + fibM1;

    while (fibM < n) {
        fibM2 = fibM1;
        fibM1 = fibM;
        fibM = fibM2 + fibM1;
    }

    int offset = -1;

    while (fibM > 1) {
        int i = std::min(offset + fibM2, n - 1);

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

    if (fibM1 && offset + 1 < n && arr[offset + 1] == target) {
        return offset + 1;
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

/**
 * Jump search for comparison
 */
int jumpSearch(const std::vector<int>& arr, int target) {
    int n = arr.size();
    int jump = static_cast<int>(std::sqrt(n));
    int prev = 0;

    while (prev < n && arr[std::min(prev + jump, n - 1)] < target) {
        prev += jump;
    }

    for (int i = std::max(0, prev - jump); i < std::min(prev + jump, n); i++) {
        if (arr[i] == target) return i;
    }
    return -1;
}

int main() {
    // Test correctness
    std::vector<int> testArr = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29};
    std::cout << "Test Array: ";
    for (int x : testArr) std::cout << x << " ";
    std::cout << "\n";

    std::cout << "Fibonacci Search for 15: Index " << fibonacciSearch(testArr, 15) << "\n";
    std::cout << "Fibonacci Search for 20: Index " << fibonacciSearch(testArr, 20) << "\n";
    std::cout << "Fibonacci Search for 1: Index " << fibonacciSearch(testArr, 1) << "\n";
    std::cout << "Fibonacci Search for 29: Index " << fibonacciSearch(testArr, 29) << "\n";

    // Performance comparison
    std::cout << "\n--- Performance Comparison ---\n";
    std::vector<int> sizes = {1000, 10000, 100000, 1000000};
    std::mt19937 gen(42);

    for (int size : sizes) {
        std::vector<int> arr(size);
        for (int i = 0; i < size; i++) {
            arr[i] = i * 2;
        }

        std::uniform_int_distribution<> dis(0, arr.size() - 1);
        int target = arr[dis(gen)];

        // Fibonacci search
        auto start = std::chrono::high_resolution_clock::now();
        for (int i = 0; i < 10000; i++) {
            fibonacciSearch(arr, target);
        }
        auto end = std::chrono::high_resolution_clock::now();
        auto fibTime = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

        // Binary search
        start = std::chrono::high_resolution_clock::now();
        for (int i = 0; i < 10000; i++) {
            binarySearch(arr, target);
        }
        end = std::chrono::high_resolution_clock::now();
        auto binaryTime = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

        // Jump search
        start = std::chrono::high_resolution_clock::now();
        for (int i = 0; i < 10000; i++) {
            jumpSearch(arr, target);
        }
        end = std::chrono::high_resolution_clock::now();
        auto jumpTime = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

        std::cout << "\nArray size: " << size << "\n";
        std::cout << "Fibonacci Search: " << std::fixed << std::setprecision(3)
                  << fibTime / 1000.0 << "ms\n";
        std::cout << "Binary Search: " << binaryTime / 1000.0 << "ms\n";
        std::cout << "Jump Search: " << jumpTime / 1000.0 << "ms\n";
        std::cout << "Ratio (Fib/Binary): " << std::setprecision(2)
                  << static_cast<double>(fibTime) / binaryTime << "x\n";
        std::cout << "Ratio (Fib/Jump): "
                  << static_cast<double>(fibTime) / jumpTime << "x\n";
    }

    // Performance on different data distributions
    std::cout << "\n--- Performance on Different Data Distributions ---\n";

    // Uniform distribution
    std::vector<int> arrUniform(100000);
    for (int i = 0; i < 100000; i++) {
        arrUniform[i] = i;
    }
    int target1 = 75000;

    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 10000; i++) {
        fibonacciSearch(arrUniform, target1);
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto uniformTime = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
    std::cout << "Uniform distribution: " << std::fixed << std::setprecision(3)
              << uniformTime / 1000.0 << "ms\n";

    // Sparse distribution
    std::vector<int> arrSparse(10000);
    for (int i = 0; i < 10000; i++) {
        arrSparse[i] = i * 10;
    }
    int target2 = 75000;

    start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 10000; i++) {
        fibonacciSearch(arrSparse, target2);
    }
    end = std::chrono::high_resolution_clock::now();
    auto sparseTime = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
    std::cout << "Sparse distribution: " << sparseTime / 1000.0 << "ms\n";

    return 0;
}
