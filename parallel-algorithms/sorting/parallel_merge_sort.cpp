/*
 * Parallel Merge Sort Implementation in C++
 *
 * This implementation uses OpenMP for parallel execution, providing:
 * - Low-level control over parallelism
 * - Compiler directives for parallelization
 * - Portable across platforms
 * - Excellent performance
 *
 * Features:
 * - OpenMP parallel sections and tasks
 * - Thread-safe operations
 * - Atomic operations for counters
 * - RAII for resource management
 * - Modern C++17/20 features
 *
 * Time Complexity: O(n log n)
 * Space Complexity: O(n)
 *
 * To compile and run:
 *   g++ -std=c++17 -fopenmp -O3 parallel_merge_sort.cpp -o parallel_merge_sort
 *   ./parallel_merge_sort
 *
 * Or with clang:
 *   clang++ -std=c++17 -fopenmp -O3 parallel_merge_sort.cpp -o parallel_merge_sort
 *
 * Author: Algorithms Multiverse
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>
#include <iomanip>
#include <atomic>
#include <string>
#include <map>
#include <cmath>

#ifdef _OPENMP
#include <omp.h>
#endif

// Result structure for sorting operations
struct SortResult {
    std::vector<int> sortedArray;
    double timeTaken;  // seconds
    long long comparisons;
    std::string method;
    int numThreads;
};

class ParallelMergeSort {
private:
    static constexpr int SEQUENTIAL_THRESHOLD = 1000;
    static constexpr int PROCESS_THRESHOLD = 100000;

    int numThreads;
    std::atomic<long long> comparisons;

    // Merge two sorted vectors
    std::vector<int> merge(const std::vector<int>& left,
                          const std::vector<int>& right,
                          bool countComparisons = true) {
        std::vector<int> result;
        result.reserve(left.size() + right.size());

        size_t i = 0, j = 0;

        while (i < left.size() && j < right.size()) {
            if (countComparisons) {
                comparisons.fetch_add(1, std::memory_order_relaxed);
            }

            if (left[i] <= right[j]) {
                result.push_back(left[i++]);
            } else {
                result.push_back(right[j++]);
            }
        }

        result.insert(result.end(), left.begin() + i, left.end());
        result.insert(result.end(), right.begin() + j, right.end());

        return result;
    }

public:
    ParallelMergeSort(int threads = 0)
        : numThreads(threads > 0 ? threads : omp_get_max_threads()),
          comparisons(0) {
#ifdef _OPENMP
        omp_set_num_threads(numThreads);
#endif
    }

    // Sequential merge sort for base cases
    std::vector<int> sequentialMergeSort(const std::vector<int>& arr) {
        if (arr.size() <= 1) {
            return arr;
        }

        size_t mid = arr.size() / 2;
        std::vector<int> left(arr.begin(), arr.begin() + mid);
        std::vector<int> right(arr.begin() + mid, arr.end());

        left = sequentialMergeSort(left);
        right = sequentialMergeSort(right);

        return merge(left, right);
    }

    // Parallel merge sort using OpenMP tasks
    std::vector<int> parallelMergeSortTasks(const std::vector<int>& arr, int depth = 0) {
        if (arr.size() <= SEQUENTIAL_THRESHOLD) {
            return sequentialMergeSort(arr);
        }

        // Limit parallel depth to prevent task explosion
        int maxDepth = static_cast<int>(std::log2(numThreads));
        if (depth >= maxDepth) {
            return sequentialMergeSort(arr);
        }

        size_t mid = arr.size() / 2;
        std::vector<int> left(arr.begin(), arr.begin() + mid);
        std::vector<int> right(arr.begin() + mid, arr.end());

        std::vector<int> leftResult, rightResult;

#ifdef _OPENMP
        #pragma omp parallel sections
        {
            #pragma omp section
            {
                leftResult = parallelMergeSortTasks(left, depth + 1);
            }
            #pragma omp section
            {
                rightResult = parallelMergeSortTasks(right, depth + 1);
            }
        }
#else
        leftResult = parallelMergeSortTasks(left, depth + 1);
        rightResult = parallelMergeSortTasks(right, depth + 1);
#endif

        return merge(leftResult, rightResult);
    }

    // Parallel merge sort using OpenMP task directive (more efficient)
    std::vector<int> parallelMergeSortTaskDirective(const std::vector<int>& arr, int depth = 0) {
        if (arr.size() <= SEQUENTIAL_THRESHOLD) {
            return sequentialMergeSort(arr);
        }

        int maxDepth = static_cast<int>(std::log2(numThreads));
        if (depth >= maxDepth) {
            return sequentialMergeSort(arr);
        }

        size_t mid = arr.size() / 2;
        std::vector<int> left(arr.begin(), arr.begin() + mid);
        std::vector<int> right(arr.begin() + mid, arr.end());

        std::vector<int> leftResult, rightResult;

#ifdef _OPENMP
        #pragma omp task shared(leftResult) if(depth < maxDepth)
        leftResult = parallelMergeSortTaskDirective(left, depth + 1);

        #pragma omp task shared(rightResult) if(depth < maxDepth)
        rightResult = parallelMergeSortTaskDirective(right, depth + 1);

        #pragma omp taskwait
#else
        leftResult = parallelMergeSortTaskDirective(left, depth + 1);
        rightResult = parallelMergeSortTaskDirective(right, depth + 1);
#endif

        return merge(leftResult, rightResult);
    }

    // Wrapper for task directive version
    std::vector<int> parallelMergeSortTaskWrapper(const std::vector<int>& arr) {
        std::vector<int> result;
#ifdef _OPENMP
        #pragma omp parallel
        {
            #pragma omp single
            result = parallelMergeSortTaskDirective(arr, 0);
        }
#else
        result = parallelMergeSortTaskDirective(arr, 0);
#endif
        return result;
    }

    // Parallel merge sort using chunking strategy
    std::vector<int> parallelMergeSortChunked(const std::vector<int>& arr) {
        if (arr.size() <= SEQUENTIAL_THRESHOLD) {
            return sequentialMergeSort(arr);
        }

        size_t chunkSize = std::max(arr.size() / numThreads,
                                    static_cast<size_t>(SEQUENTIAL_THRESHOLD));

        std::vector<std::vector<int>> chunks;
        for (size_t i = 0; i < arr.size(); i += chunkSize) {
            size_t end = std::min(i + chunkSize, arr.size());
            chunks.emplace_back(arr.begin() + i, arr.begin() + end);
        }

        // Sort chunks in parallel
        std::vector<std::vector<int>> sortedChunks(chunks.size());

#ifdef _OPENMP
        #pragma omp parallel for
#endif
        for (size_t i = 0; i < chunks.size(); ++i) {
            sortedChunks[i] = sequentialMergeSort(chunks[i]);
        }

        // Merge sorted chunks
        while (sortedChunks.size() > 1) {
            std::vector<std::vector<int>> merged;

            for (size_t i = 0; i < sortedChunks.size(); i += 2) {
                if (i + 1 < sortedChunks.size()) {
                    merged.push_back(merge(sortedChunks[i], sortedChunks[i + 1], false));
                } else {
                    merged.push_back(sortedChunks[i]);
                }
            }

            sortedChunks = std::move(merged);
        }

        return sortedChunks.empty() ? std::vector<int>() : sortedChunks[0];
    }

    // Adaptive parallel merge sort
    std::vector<int> adaptiveParallelMergeSort(const std::vector<int>& arr) {
        size_t n = arr.size();

        if (n <= SEQUENTIAL_THRESHOLD) {
            return sequentialMergeSort(arr);
        } else if (n <= PROCESS_THRESHOLD) {
            return parallelMergeSortTaskWrapper(arr);
        } else {
            return parallelMergeSortChunked(arr);
        }
    }

    // Sort with metrics
    SortResult sortWithMetrics(const std::vector<int>& arr, const std::string& method) {
        comparisons.store(0, std::memory_order_relaxed);

        auto start = std::chrono::high_resolution_clock::now();

        std::vector<int> sorted;
        if (method == "sequential") {
            sorted = sequentialMergeSort(arr);
        } else if (method == "tasks") {
            sorted = parallelMergeSortTasks(arr);
        } else if (method == "task_directive") {
            sorted = parallelMergeSortTaskWrapper(arr);
        } else if (method == "chunked") {
            sorted = parallelMergeSortChunked(arr);
        } else if (method == "adaptive") {
            sorted = adaptiveParallelMergeSort(arr);
        } else {
            sorted = adaptiveParallelMergeSort(arr);
        }

        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> duration = end - start;

        return SortResult{
            sorted,
            duration.count(),
            comparisons.load(std::memory_order_relaxed),
            method,
            numThreads
        };
    }

    // Check if array is sorted
    static bool isSorted(const std::vector<int>& arr) {
        for (size_t i = 1; i < arr.size(); ++i) {
            if (arr[i] < arr[i - 1]) {
                return false;
            }
        }
        return true;
    }

    // Calculate speedup
    static double calculateSpeedup(double seqTime, double parallelTime) {
        return parallelTime > 0 ? seqTime / parallelTime : 0.0;
    }

    // Calculate efficiency
    static double calculateEfficiency(double speedup, int numThreads) {
        return numThreads > 0 ? speedup / numThreads : 0.0;
    }
};

// Benchmark all methods
std::map<std::string, SortResult> benchmarkAllMethods(const std::vector<int>& arr, int numThreads) {
    std::map<std::string, SortResult> results;
    std::vector<std::string> methods = {
        "sequential", "tasks", "task_directive", "chunked", "adaptive"
    };

    ParallelMergeSort sorter(numThreads);

    for (const auto& method : methods) {
        results[method] = sorter.sortWithMetrics(arr, method);
    }

    return results;
}

int main() {
    std::cout << std::string(80, '=') << "\n";
    std::cout << "PARALLEL MERGE SORT DEMONSTRATION (C++ with OpenMP)\n";
    std::cout << std::string(80, '=') << "\n";

#ifdef _OPENMP
    std::cout << "OpenMP is enabled\n";
    std::cout << "Number of available threads: " << omp_get_max_threads() << "\n";
#else
    std::cout << "OpenMP is NOT enabled (sequential execution only)\n";
#endif

    // Test with different sizes
    std::vector<int> sizes = {1000, 10000, 100000};

    for (int size : sizes) {
        std::cout << "\n" << std::string(80, '=') << "\n";
        std::cout << "Testing with " << size << " elements\n";
        std::cout << std::string(80, '=') << "\n";

        // Generate random array
        std::vector<int> arr(size);
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(0, 100000);

        for (int& val : arr) {
            val = dis(gen);
        }

        // Benchmark all methods
        auto results = benchmarkAllMethods(arr, omp_get_max_threads());

        // Display results
        std::cout << "\n" << std::left << std::setw(18) << "Method"
                  << std::setw(15) << "Time (s)"
                  << std::setw(20) << "Comparisons"
                  << std::setw(10) << "Verified" << "\n";
        std::cout << std::string(80, '-') << "\n";

        double seqTime = results.count("sequential") ? results["sequential"].timeTaken : 0.0;

        for (const auto& [method, result] : results) {
            std::string verified = ParallelMergeSort::isSorted(result.sortedArray) ? "✓" : "✗";

            std::cout << std::left << std::setw(18) << method
                      << std::fixed << std::setprecision(6)
                      << std::setw(15) << result.timeTaken
                      << std::setw(20) << result.comparisons
                      << std::setw(10) << verified << "\n";

            if (method != "sequential" && seqTime > 0) {
                double speedup = ParallelMergeSort::calculateSpeedup(seqTime, result.timeTaken);
                double efficiency = ParallelMergeSort::calculateEfficiency(speedup, result.numThreads);
                std::cout << std::setw(18) << ""
                          << "Speedup: " << std::fixed << std::setprecision(2) << speedup << "x  "
                          << "Efficiency: " << std::fixed << std::setprecision(2)
                          << efficiency * 100 << "%\n";
            }
        }
    }

    std::cout << "\n" << std::string(80, '=') << "\n";
    std::cout << "OPENMP SCALABILITY ANALYSIS\n";
    std::cout << std::string(80, '=') << "\n";

    // Test with different thread counts
    std::cout << "\nScalability test (50,000 elements):\n";

    std::vector<int> testArr(50000);
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 100000);
    for (int& val : testArr) {
        val = dis(gen);
    }

    std::cout << "\n" << std::left << std::setw(10) << "Threads"
              << std::setw(15) << "Time (s)"
              << std::setw(10) << "Speedup" << "\n";
    std::cout << std::string(40, '-') << "\n";

    double baselineTime = 0.0;
    int maxThreads = omp_get_max_threads();

    for (int threads = 1; threads <= maxThreads; ++threads) {
        ParallelMergeSort sorter(threads);
        auto result = sorter.sortWithMetrics(testArr, "task_directive");

        if (threads == 1) {
            baselineTime = result.timeTaken;
        }

        double speedup = ParallelMergeSort::calculateSpeedup(baselineTime, result.timeTaken);
        std::cout << std::left << std::setw(10) << threads
                  << std::fixed << std::setprecision(6) << std::setw(15) << result.timeTaken
                  << std::fixed << std::setprecision(2) << speedup << "x\n";
    }

    std::cout << "\n" << std::string(80, '=') << "\n";
    std::cout << "WHEN TO USE PARALLEL MERGE SORT IN C++ WITH OPENMP\n";
    std::cout << std::string(80, '=') << "\n";
    std::cout << R"(
Parallel merge sort with OpenMP is beneficial when:

✓ Dataset size > 10,000 elements
✓ Multiple CPU cores available
✓ CPU-bound comparison operations
✓ Low-level control needed

C++ + OpenMP advantages:
✓ Compiler directives (easy to parallelize)
✓ Low overhead (~100-200ns per task)
✓ Excellent performance (near-native)
✓ Portable across compilers (GCC, Clang, Intel, MSVC)
✓ Fine-grained control over threads
✓ No runtime overhead (compiled to native code)

Avoid parallel merge sort when:

✗ Small datasets (<1,000 elements)
✗ Single-core systems
✗ OpenMP not available
✗ Simple comparisons with negligible CPU cost

Strategy selection:
- Sequential: < 1,000 elements
- Tasks/Sections: 1,000 - 100,000 elements (recursive)
- Task Directive: Best performance (work stealing)
- Chunked: > 100,000 elements (better cache locality)
- Adaptive: Let the algorithm decide

Performance characteristics:
- Task creation: ~100-200ns overhead
- Work stealing: Built into OpenMP runtime
- Typical speedup: 3.5-3.8x on 4 cores
- Efficiency: 85-95% for optimal workload
- Cache effects: Significant for large arrays

Best practices:
1. Use #pragma omp task for recursive algorithms
2. Use #pragma omp parallel for for independent iterations
3. Limit task depth to prevent explosion
4. Use if clause to control parallelization
5. Compile with -O3 for optimization
6. Profile with perf or gprof

OpenMP directives used:
- #pragma omp parallel: Create parallel region
- #pragma omp sections: Divide work into sections
- #pragma omp task: Create asynchronous task
- #pragma omp taskwait: Wait for child tasks
- #pragma omp parallel for: Parallel loop

Memory considerations:
- Stack allocation preferred (faster)
- Avoid heap allocations in hot paths
- Consider cache line size (64 bytes)
- Use std::vector::reserve() to avoid reallocations

Compiler flags:
- GCC/Clang: -fopenmp -O3
- Intel: -qopenmp -O3
- MSVC: /openmp /O2

Environment variables:
- OMP_NUM_THREADS: Set number of threads
- OMP_SCHEDULE: Set scheduling policy
- OMP_PROC_BIND: Set thread affinity

Comparison with other approaches:
- OpenMP: Easiest to use, good performance
- TBB: Better abstractions, C++ friendly
- std::thread: Full control, more code
- std::async: High-level, limited control
)";

    std::cout << "\nDemonstration complete!\n";

    return 0;
}
