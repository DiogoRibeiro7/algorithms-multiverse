/**
 * Bubble Sort Algorithm Implementation in C++
 *
 * Time Complexity:
 * - Best Case: O(n) - when array is already sorted (optimized version)
 * - Average Case: O(n²)
 * - Worst Case: O(n²) - when array is reverse sorted
 * Space Complexity: O(1) for in-place, O(n) for functional approach
 *
 * Bubble Sort works by repeatedly stepping through the list, comparing adjacent
 * elements and swapping them if they are in the wrong order. The pass through
 * the list is repeated until the list is sorted.
 *
 * C++ features:
 * - Template functions for generic programming
 * - STL containers and algorithms
 * - Function overloading
 * - Custom comparators
 * - Iterator support
 * - Modern C++11/14/17 features
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>
#include <iomanip>
#include <functional>
#include <string>
#include <sstream>

using namespace std;
using namespace std::chrono;

/**
 * Basic iterative bubble sort implementation.
 *
 * This is the standard bubble sort algorithm that compares and swaps
 * adjacent elements until the entire container is sorted.
 *
 * @tparam T Type of elements (must support < operator)
 * @param arr Vector to be sorted
 * @return New sorted vector
 *
 * Time Complexity: O(n²) in all cases (no optimization)
 * Space Complexity: O(n) for the new vector
 */
template <typename T>
vector<T> bubbleSortIterative(const vector<T>& arr) {
    if (arr.size() <= 1) {
        return arr;
    }

    vector<T> result = arr;
    size_t n = result.size();

    // Outer loop for number of passes
    for (size_t i = 0; i < n; i++) {
        // Inner loop for comparisons
        // After each pass, the largest element "bubbles up" to its position
        for (size_t j = 0; j < n - i - 1; j++) {
            if (result[j] > result[j + 1]) {
                // Swap adjacent elements
                swap(result[j], result[j + 1]);
            }
        }
    }

    return result;
}

/**
 * Optimized bubble sort with early termination.
 *
 * This version includes a flag to detect if any swaps were made during a pass.
 * If no swaps occur, the array is already sorted and we can terminate early.
 *
 * @tparam T Type of elements (must support < operator)
 * @param arr Vector to be sorted
 * @return New sorted vector
 *
 * Time Complexity:
 *   - Best Case: O(n) when already sorted
 *   - Average/Worst: O(n²)
 * Space Complexity: O(n) for the new vector
 */
template <typename T>
vector<T> bubbleSortOptimized(const vector<T>& arr) {
    if (arr.size() <= 1) {
        return arr;
    }

    vector<T> result = arr;
    size_t n = result.size();

    for (size_t i = 0; i < n; i++) {
        // Flag to optimize for already sorted arrays
        bool swapped = false;

        for (size_t j = 0; j < n - i - 1; j++) {
            if (result[j] > result[j + 1]) {
                swap(result[j], result[j + 1]);
                swapped = true;
            }
        }

        // If no swaps occurred, array is sorted
        if (!swapped) {
            break;
        }
    }

    return result;
}

/**
 * In-place bubble sort implementation (optimized).
 *
 * Sorts the vector in-place without creating a new vector,
 * minimizing space complexity.
 *
 * @tparam T Type of elements (must support < operator)
 * @param arr Vector to be sorted in-place
 *
 * Time Complexity: O(n) best case, O(n²) average/worst
 * Space Complexity: O(1)
 */
template <typename T>
void bubbleSortInPlace(vector<T>& arr) {
    size_t n = arr.size();

    for (size_t i = 0; i < n; i++) {
        bool swapped = false;

        for (size_t j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }

        if (!swapped) {
            break;
        }
    }
}

/**
 * Recursive bubble sort implementation.
 *
 * Each recursive call performs one pass through the array,
 * bubbling the largest element to the end.
 *
 * @tparam T Type of elements (must support < operator)
 * @param arr Vector to be sorted
 * @param n Size of the array portion to sort
 *
 * Time Complexity: O(n²)
 * Space Complexity: O(n) for recursion stack
 */
template <typename T>
void bubbleSortRecursiveHelper(vector<T>& arr, size_t n) {
    // Base case: single element or empty
    if (n <= 1) {
        return;
    }

    // One pass of bubble sort
    // After this pass, the largest element will be at the end
    for (size_t i = 0; i < n - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            swap(arr[i], arr[i + 1]);
        }
    }

    // Recursively sort the first n-1 elements
    bubbleSortRecursiveHelper(arr, n - 1);
}

/**
 * Recursive bubble sort wrapper.
 *
 * @tparam T Type of elements (must support < operator)
 * @param arr Vector to be sorted
 * @return New sorted vector
 */
template <typename T>
vector<T> bubbleSortRecursive(const vector<T>& arr) {
    vector<T> result = arr;
    bubbleSortRecursiveHelper(result, result.size());
    return result;
}

/**
 * Bubble sort with custom comparison function.
 *
 * @tparam T Type of elements
 * @tparam Compare Comparison function type
 * @param arr Vector to be sorted
 * @param comp Comparison function
 * @return New sorted vector
 */
template <typename T, typename Compare>
vector<T> bubbleSortWithComparator(const vector<T>& arr, Compare comp) {
    if (arr.size() <= 1) {
        return arr;
    }

    vector<T> result = arr;
    size_t n = result.size();

    for (size_t i = 0; i < n; i++) {
        bool swapped = false;

        for (size_t j = 0; j < n - i - 1; j++) {
            if (comp(result[j], result[j + 1])) {
                swap(result[j], result[j + 1]);
                swapped = true;
            }
        }

        if (!swapped) {
            break;
        }
    }

    return result;
}

/**
 * Cocktail Shaker Sort (bidirectional bubble sort).
 *
 * An optimized version of bubble sort that sorts in both directions
 * alternately, which can be more efficient for certain data patterns.
 *
 * @tparam T Type of elements (must support < operator)
 * @param arr Vector to be sorted
 * @return New sorted vector
 *
 * Time Complexity: O(n²) worst case, but often faster than standard bubble sort
 * Space Complexity: O(n)
 */
template <typename T>
vector<T> cocktailSort(const vector<T>& arr) {
    if (arr.size() <= 1) {
        return arr;
    }

    vector<T> result = arr;
    size_t start = 0;
    size_t end = result.size() - 1;
    bool swapped = true;

    while (swapped) {
        swapped = false;

        // Forward pass (like bubble sort)
        for (size_t i = start; i < end; i++) {
            if (result[i] > result[i + 1]) {
                swap(result[i], result[i + 1]);
                swapped = true;
            }
        }

        if (!swapped) {
            break;
        }

        swapped = false;
        end--;

        // Backward pass
        for (size_t i = end; i > start; i--) {
            if (result[i - 1] > result[i]) {
                swap(result[i - 1], result[i]);
                swapped = true;
            }
        }

        start++;
    }

    return result;
}

/**
 * Check if vector is sorted in ascending order.
 *
 * @tparam T Type of elements (must support < operator)
 * @param arr Vector to check
 * @return True if sorted
 */
template <typename T>
bool isSorted(const vector<T>& arr) {
    for (size_t i = 0; i < arr.size() - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            return false;
        }
    }
    return true;
}

/**
 * Statistics structure for tracking sort operations.
 */
struct SortStatistics {
    size_t comparisons = 0;
    size_t swaps = 0;
    size_t iterations = 0;

    void reset() {
        comparisons = 0;
        swaps = 0;
        iterations = 0;
    }

    string toString() const {
        ostringstream oss;
        oss << "Comparisons: " << comparisons
            << ", Swaps: " << swaps
            << ", Iterations: " << iterations;
        return oss.str();
    }
};

/**
 * Bubble sort with statistics tracking.
 *
 * @tparam T Type of elements (must support < operator)
 * @param arr Vector to be sorted
 * @param stats Statistics object to update
 * @return New sorted vector
 */
template <typename T>
vector<T> bubbleSortWithStats(const vector<T>& arr, SortStatistics& stats) {
    stats.reset();

    if (arr.size() <= 1) {
        return arr;
    }

    vector<T> result = arr;
    size_t n = result.size();

    for (size_t i = 0; i < n; i++) {
        stats.iterations++;
        bool swapped = false;

        for (size_t j = 0; j < n - i - 1; j++) {
            stats.comparisons++;
            if (result[j] > result[j + 1]) {
                swap(result[j], result[j + 1]);
                stats.swaps++;
                swapped = true;
            }
        }

        if (!swapped) {
            break;
        }
    }

    return result;
}

/**
 * BubbleSorter class with state and statistics.
 *
 * @tparam T Type of elements to sort
 */
template <typename T>
class BubbleSorter {
private:
    SortStatistics stats;

public:
    vector<T> sort(const vector<T>& arr) {
        return bubbleSortWithStats(arr, stats);
    }

    const SortStatistics& getStats() const {
        return stats;
    }

    void resetStats() {
        stats.reset();
    }
};

/**
 * Print a vector with a label.
 */
template <typename T>
void printVector(const vector<T>& arr, const string& label) {
    cout << label << ": [";
    for (size_t i = 0; i < arr.size(); i++) {
        cout << arr[i];
        if (i < arr.size() - 1) {
            cout << ", ";
        }
    }
    cout << "]" << endl;
}

/**
 * Demonstrate various bubble sort implementations.
 */
void demonstrateBubbleSort() {
    cout << "🫧 Bubble Sort Implementation in C++" << endl;
    cout << string(50, '=') << endl;

    // Test data - comprehensive edge cases
    vector<vector<int>> testArrays = {
        {64, 34, 25, 12, 22, 11, 90},
        {5, 2, 8, 6, 1, 9, 4},
        {1},
        {},
        {3, 3, 3, 3, 3},
        {9, 8, 7, 6, 5, 4, 3, 2, 1},
        {1, 2, 3, 4, 5},
        {5, 1, 4, 2, 3}
    };

    vector<string> descriptions = {
        "Random array",
        "Small random array",
        "Single element",
        "Empty array",
        "All duplicates",
        "Reverse sorted",
        "Already sorted",
        "Nearly sorted"
    };

    cout << "\n📋 Basic Sorting Tests:" << endl;
    cout << string(50, '-') << endl;

    for (size_t i = 0; i < testArrays.size(); i++) {
        const auto& arr = testArrays[i];
        const auto& desc = descriptions[i];

        vector<int> original = arr;

        // Test different implementations
        auto iterativeResult = bubbleSortIterative(arr);
        auto optimizedResult = bubbleSortOptimized(arr);
        auto recursiveResult = bubbleSortRecursive(arr);
        auto cocktailResult = cocktailSort(arr);

        // Test in-place
        auto inplaceResult = arr;
        bubbleSortInPlace(inplaceResult);

        cout << "\nTest: " << desc << endl;
        printVector(original, "Original");
        printVector(iterativeResult, "Sorted  ");

        // Verify all results are correct and equal
        bool allCorrect = isSorted(iterativeResult) && isSorted(optimizedResult) &&
                         isSorted(recursiveResult) && isSorted(cocktailResult) &&
                         isSorted(inplaceResult);
        bool allEqual = (iterativeResult == optimizedResult) &&
                       (iterativeResult == recursiveResult) &&
                       (iterativeResult == cocktailResult) &&
                       (iterativeResult == inplaceResult);

        string status = (allCorrect && allEqual) ? "✓" : "✗";
        cout << "All implementations match: " << status << endl;
    }

    cout << "\n" << string(50, '-') << endl;

    // String sorting
    vector<string> words = {"banana", "apple", "cherry", "date", "elderberry"};
    auto sortedWords = bubbleSortOptimized(words);

    cout << "\n🔤 Word sorting:" << endl;
    printVector(words, "Original    ");
    printVector(sortedWords, "Alphabetical");

    // Custom comparison (descending)
    vector<int> numbers = {3, 1, 4, 1, 5, 9, 2, 6};
    auto descSorted = bubbleSortWithComparator(numbers, greater<int>());

    cout << "\n🔢 Custom comparison (descending):" << endl;
    printVector(numbers, "Original  ");
    printVector(descSorted, "Descending");
}

/**
 * Benchmark different bubble sort implementations.
 */
void performanceBenchmark() {
    cout << "\n\n⚡ Performance Benchmark" << endl;
    cout << string(70, '=') << endl;

    vector<size_t> sizes = {100, 500, 1000, 2000};
    random_device rd;
    mt19937 gen(42); // Fixed seed for reproducibility
    uniform_int_distribution<> dis(1, 1000);

    // Test different data patterns
    map<string, function<vector<int>(size_t)>> patterns;
    patterns["Random"] = [&](size_t n) {
        vector<int> arr(n);
        generate(arr.begin(), arr.end(), [&]() { return dis(gen); });
        return arr;
    };
    patterns["Sorted"] = [](size_t n) {
        vector<int> arr(n);
        iota(arr.begin(), arr.end(), 0);
        return arr;
    };
    patterns["Reversed"] = [](size_t n) {
        vector<int> arr(n);
        iota(arr.begin(), arr.end(), 0);
        reverse(arr.begin(), arr.end());
        return arr;
    };
    patterns["Nearly Sorted"] = [&](size_t n) {
        vector<int> arr(n);
        iota(arr.begin(), arr.end(), 0);
        for (size_t i = 0; i < min(size_t(5), n / 10); i++) {
            size_t idx1 = dis(gen) % n;
            size_t idx2 = dis(gen) % n;
            swap(arr[idx1], arr[idx2]);
        }
        return arr;
    };

    map<string, function<vector<int>(const vector<int>&)>> methods;
    methods["Iterative"] = bubbleSortIterative<int>;
    methods["Optimized"] = bubbleSortOptimized<int>;
    methods["Recursive"] = bubbleSortRecursive<int>;
    methods["Cocktail"] = cocktailSort<int>;
    methods["std::sort"] = [](const vector<int>& arr) {
        vector<int> result = arr;
        sort(result.begin(), result.end());
        return result;
    };

    for (const auto& [patternName, patternGen] : patterns) {
        cout << "\n" << patternName << " Data:" << endl;

        // Header
        cout << left << setw(8) << "Size";
        for (const auto& [methodName, _] : methods) {
            cout << right << setw(12) << methodName;
        }
        cout << endl;
        cout << string(8 + 12 * methods.size(), '-') << endl;

        for (size_t size : sizes) {
            auto testData = patternGen(size);
            cout << left << setw(8) << size;

            for (const auto& [methodName, methodFunc] : methods) {
                // Skip recursive for large sizes
                if (methodName == "Recursive" && size > 1000) {
                    cout << right << setw(12) << "N/A";
                    continue;
                }

                try {
                    // Warm-up
                    methodFunc(testData);

                    // Benchmark
                    auto start = high_resolution_clock::now();
                    auto result = methodFunc(testData);
                    auto end = high_resolution_clock::now();

                    auto duration = duration_cast<microseconds>(end - start);
                    double elapsedMs = duration.count() / 1000.0;

                    cout << right << setw(11) << fixed << setprecision(2) << elapsedMs << "ms";

                    // Verify correctness
                    if (!isSorted(result)) {
                        cout << " ✗";
                    }
                } catch (const exception& e) {
                    cout << right << setw(12) << "ERROR";
                }
            }

            cout << endl;
        }
    }
}

/**
 * Analyze bubble sort behavior with different inputs.
 */
void analyzeAlgorithm() {
    cout << "\n\n🔍 Algorithm Analysis" << endl;
    cout << string(50, '=') << endl;

    vector<vector<int>> testCases = {
        {5, 2, 8, 6, 1},
        {1, 2, 3, 4, 5},
        {5, 4, 3, 2, 1}
    };

    vector<string> descriptions = {
        "Random",
        "Already sorted",
        "Reverse sorted"
    };

    for (size_t i = 0; i < testCases.size(); i++) {
        const auto& arr = testCases[i];
        const auto& desc = descriptions[i];

        SortStatistics stats;
        bubbleSortWithStats(arr, stats);

        size_t n = arr.size();
        size_t theoreticalMax = n * (n - 1) / 2;

        cout << "\n" << desc << ": ";
        printVector(arr, "");
        cout << "Array size (n): " << n << endl;
        cout << "Comparisons: " << stats.comparisons
             << " (theoretical max: " << theoreticalMax << ")" << endl;
        cout << "Swaps: " << stats.swaps << endl;
        cout << "Efficiency: " << fixed << setprecision(1)
             << ((1.0 - stats.swaps / max(stats.comparisons, size_t(1))) * 100.0)
             << "% (fewer swaps is better)" << endl;
    }
}

/**
 * Main function for demonstration.
 */
int main() {
    demonstrateBubbleSort();
    performanceBenchmark();
    analyzeAlgorithm();

    // Demonstrate OOP approach
    cout << "\n\n📊 Object-Oriented Approach" << endl;
    cout << string(50, '=') << endl;

    BubbleSorter<int> sorter;
    vector<int> testArray = {64, 34, 25, 12, 22, 11, 90};

    auto sortedArray = sorter.sort(testArray);
    const auto& stats = sorter.getStats();

    printVector(testArray, "Original");
    printVector(sortedArray, "Sorted  ");
    cout << "Statistics: " << stats.toString() << endl;

    cout << "\n✨ Bubble Sort demonstration complete!" << endl;

    return 0;
}
