/**
 * Insertion Sort Algorithm Implementation in C++
 *
 * Time Complexity:
 * - Best Case: O(n) - when array is already sorted
 * - Average Case: O(n²)
 * - Worst Case: O(n²) - when array is reverse sorted
 * Space Complexity: O(1) for in-place, O(n) for functional approach
 *
 * Insertion Sort builds the final sorted array one item at a time.
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

using namespace std;
using namespace std::chrono;

/**
 * Standard insertion sort implementation.
 *
 * Time Complexity: O(n²) average and worst case, O(n) best case
 * Space Complexity: O(n) for the new vector
 *
 * Example visualization:
 *   Initial: [5, 2, 8, 6, 1]
 *   Step 1:  [2, 5, 8, 6, 1]  // Insert 2
 *   Step 2:  [2, 5, 8, 6, 1]  // 8 already in place
 *   Step 3:  [2, 5, 6, 8, 1]  // Insert 6
 *   Step 4:  [1, 2, 5, 6, 8]  // Insert 1
 */
template <typename T>
vector<T> insertionSort(const vector<T>& arr) {
    if (arr.size() <= 1) {
        return arr;
    }

    vector<T> result = arr;
    insertionSortInPlace(result);
    return result;
}

/**
 * In-place insertion sort implementation.
 *
 * Time Complexity: O(n²) average and worst case, O(n) best case
 * Space Complexity: O(1)
 */
template <typename T>
void insertionSortInPlace(vector<T>& arr) {
    for (size_t i = 1; i < arr.size(); i++) {
        T key = arr[i];
        int j = i - 1;

        // Move elements greater than key one position ahead
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }

        arr[j + 1] = key;
    }
}

/**
 * Recursive insertion sort implementation.
 *
 * Time Complexity: O(n²)
 * Space Complexity: O(n) for recursion stack
 */
template <typename T>
void insertionSortRecursiveHelper(vector<T>& arr, size_t n) {
    // Base case
    if (n <= 1) {
        return;
    }

    // Sort first n-1 elements
    insertionSortRecursiveHelper(arr, n - 1);

    // Insert last element at its correct position
    T key = arr[n - 1];
    int j = n - 2;

    while (j >= 0 && arr[j] > key) {
        arr[j + 1] = arr[j];
        j--;
    }

    arr[j + 1] = key;
}

/**
 * Recursive insertion sort wrapper.
 */
template <typename T>
vector<T> insertionSortRecursive(const vector<T>& arr) {
    vector<T> result = arr;
    insertionSortRecursiveHelper(result, result.size());
    return result;
}

/**
 * Binary insertion sort - uses binary search to find insertion position.
 *
 * Time Complexity: O(n²) for moves, O(n log n) for comparisons
 * Space Complexity: O(n)
 */
template <typename T>
int binarySearchPosition(const vector<T>& arr, int left, int right, const T& key) {
    if (right <= left) {
        return key > arr[left] ? left + 1 : left;
    }

    int mid = (left + right) / 2;

    if (key == arr[mid]) {
        return mid + 1;
    }

    if (key > arr[mid]) {
        return binarySearchPosition(arr, mid + 1, right, key);
    }

    return binarySearchPosition(arr, left, mid - 1, key);
}

template <typename T>
vector<T> binaryInsertionSort(const vector<T>& arr) {
    if (arr.size() <= 1) {
        return arr;
    }

    vector<T> result = arr;

    for (size_t i = 1; i < result.size(); i++) {
        T key = result[i];

        // Find position using binary search
        int pos = binarySearchPosition(result, 0, i - 1, key);

        // Shift elements to make space
        for (int j = i - 1; j >= pos; j--) {
            result[j + 1] = result[j];
        }

        result[pos] = key;
    }

    return result;
}

/**
 * Shell sort - a generalization of insertion sort.
 *
 * Time Complexity: Depends on gap sequence (O(n log²n) for good sequences)
 */
template <typename T>
vector<T> shellSort(const vector<T>& arr) {
    if (arr.size() <= 1) {
        return arr;
    }

    vector<T> result = arr;
    size_t n = result.size();

    // Start with a large gap, then reduce (Knuth's sequence)
    size_t gap = 1;
    while (gap < n / 3) {
        gap = 3 * gap + 1;
    }

    // Perform gapped insertion sort
    while (gap > 0) {
        for (size_t i = gap; i < n; i++) {
            T key = result[i];
            size_t j = i;

            // Insertion sort with gap
            while (j >= gap && result[j - gap] > key) {
                result[j] = result[j - gap];
                j -= gap;
            }

            result[j] = key;
        }

        gap /= 3;
    }

    return result;
}

/**
 * Insertion sort with custom comparison function.
 */
template <typename T, typename Compare>
vector<T> insertionSortWithComparator(const vector<T>& arr, Compare comp) {
    if (arr.size() <= 1) {
        return arr;
    }

    vector<T> result = arr;

    for (size_t i = 1; i < result.size(); i++) {
        T key = result[i];
        int j = i - 1;

        while (j >= 0 && comp(result[j], key)) {
            result[j + 1] = result[j];
            j--;
        }

        result[j + 1] = key;
    }

    return result;
}

/**
 * Check if vector is sorted.
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

    void reset() {
        comparisons = 0;
        swaps = 0;
    }

    string toString() const {
        return "Comparisons: " + to_string(comparisons) + ", Swaps: " + to_string(swaps);
    }
};

/**
 * Insertion sort with statistics tracking.
 */
template <typename T>
vector<T> insertionSortWithStats(const vector<T>& arr, SortStatistics& stats) {
    stats.reset();

    if (arr.size() <= 1) {
        return arr;
    }

    vector<T> result = arr;

    for (size_t i = 1; i < result.size(); i++) {
        T key = result[i];
        int j = i - 1;

        while (j >= 0) {
            stats.comparisons++;
            if (result[j] > key) {
                result[j + 1] = result[j];
                stats.swaps++;
                j--;
            } else {
                break;
            }
        }

        result[j + 1] = key;
    }

    return result;
}

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
 * Visualize insertion sort steps.
 */
vector<string> visualizeInsertionSort(const vector<int>& arr) {
    vector<string> steps;
    vector<int> result = arr;

    ostringstream oss;
    oss << "Initial: [";
    for (size_t i = 0; i < result.size(); i++) {
        oss << result[i];
        if (i < result.size() - 1) oss << ", ";
    }
    oss << "]";
    steps.push_back(oss.str());

    for (size_t i = 1; i < result.size(); i++) {
        int key = result[i];
        int j = i - 1;

        steps.push_back("\nStep " + to_string(i) + ": Inserting " + to_string(key));

        oss.str("");
        oss << "  Before: [";
        for (size_t k = 0; k < result.size(); k++) {
            oss << result[k];
            if (k < result.size() - 1) oss << ", ";
        }
        oss << "]";
        steps.push_back(oss.str());

        while (j >= 0 && result[j] > key) {
            result[j + 1] = result[j];
            j--;
        }

        result[j + 1] = key;

        oss.str("");
        oss << "  After:  [";
        for (size_t k = 0; k < result.size(); k++) {
            oss << result[k];
            if (k < result.size() - 1) oss << ", ";
        }
        oss << "]";
        steps.push_back(oss.str());
    }

    oss.str("");
    oss << "\nFinal: [";
    for (size_t i = 0; i < result.size(); i++) {
        oss << result[i];
        if (i < result.size() - 1) oss << ", ";
    }
    oss << "]";
    steps.push_back(oss.str());

    return steps;
}

/**
 * Demonstrate stability of insertion sort.
 */
void demonstrateStability() {
    struct Pair {
        int value;
        int originalIndex;

        bool operator>(const Pair& other) const {
            return value > other.value;
        }
    };

    vector<Pair> data = {{3, 0}, {1, 1}, {3, 2}, {2, 3}, {3, 4}};

    cout << "Stability Demonstration:" << endl;
    cout << "Original: ";
    for (const auto& p : data) {
        cout << "(" << p.value << "," << p.originalIndex << ") ";
    }
    cout << endl;

    auto sorted = insertionSort(data);
    cout << "Sorted:   ";
    for (const auto& p : sorted) {
        cout << "(" << p.value << "," << p.originalIndex << ") ";
    }
    cout << endl;

    // Check stability
    vector<int> threeIndices;
    for (const auto& p : sorted) {
        if (p.value == 3) {
            threeIndices.push_back(p.originalIndex);
        }
    }

    bool isStable = (threeIndices == vector<int>{0, 2, 4});
    cout << "Stable: " << (isStable ? "true" : "false") << " (indices of 3's: [";
    for (size_t i = 0; i < threeIndices.size(); i++) {
        cout << threeIndices[i];
        if (i < threeIndices.size() - 1) cout << ", ";
    }
    cout << "])" << endl;
}

/**
 * Demonstrate various insertion sort implementations.
 */
void demonstrateInsertionSort() {
    cout << "📝 Insertion Sort Implementation in C++" << endl;
    cout << string(60, '=') << endl;

    // Test data
    vector<vector<int>> testArrays = {
        {64, 34, 25, 12, 22, 11, 90},
        {5, 2, 8, 6, 1, 9, 4},
        {1},
        {},
        {3, 3, 3, 3, 3},
        {9, 8, 7, 6, 5, 4, 3, 2, 1},
        {1, 2, 3, 4, 5},
        {1, 3, 2, 4, 5}
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
    cout << string(60, '-') << endl;

    for (size_t i = 0; i < testArrays.size(); i++) {
        const auto& arr = testArrays[i];
        const auto& desc = descriptions[i];

        vector<int> original = arr;
        auto standardResult = insertionSort(arr);
        auto binaryResult = binaryInsertionSort(arr);
        auto shellResult = shellSort(arr);
        auto recursiveResult = insertionSortRecursive(arr);

        cout << "\nTest: " << desc << endl;
        printVector(original, "Original");
        printVector(standardResult, "Sorted  ");

        bool allCorrect = isSorted(standardResult) && isSorted(binaryResult) &&
                         isSorted(shellResult) && isSorted(recursiveResult);
        bool allEqual = (standardResult == binaryResult) &&
                       (standardResult == shellResult) &&
                       (standardResult == recursiveResult);

        string status = (allCorrect && allEqual) ? "✓" : "✗";
        cout << "All implementations match: " << status << endl;
    }

    // Visualization demo
    cout << "\n\n🎬 Step-by-Step Visualization:" << endl;
    cout << string(60, '-') << endl;

    vector<int> demoArr = {5, 2, 8, 6, 1};
    auto steps = visualizeInsertionSort(demoArr);
    for (const auto& step : steps) {
        cout << step << endl;
    }

    // Stability demonstration
    cout << "\n\n🔒 Stability Demonstration:" << endl;
    cout << string(60, '-') << endl;
    demonstrateStability();

    // Performance analysis
    cout << "\n\n📊 Operation Counting:" << endl;
    cout << string(60, '-') << endl;

    vector<vector<int>> statTestCases = {
        {5, 2, 8, 6, 1},
        {1, 2, 3, 4, 5},
        {5, 4, 3, 2, 1}
    };
    vector<string> statDescs = {"Random", "Already sorted", "Reverse sorted"};

    for (size_t i = 0; i < statTestCases.size(); i++) {
        const auto& arr = statTestCases[i];
        const auto& desc = statDescs[i];

        SortStatistics stats;
        insertionSortWithStats(arr, stats);

        size_t n = arr.size();
        cout << "\n" << desc << ": ";
        printVector(arr, "");
        cout << "Array size (n): " << n << endl;
        cout << "Comparisons: " << stats.comparisons << endl;
        cout << "Swaps: " << stats.swaps << endl;
        cout << "Best case comparisons: " << (n - 1) << endl;
        cout << "Worst case comparisons: " << (n * (n - 1) / 2) << endl;
    }
}

/**
 * Benchmark insertion sort.
 */
void performanceBenchmark() {
    cout << "\n\n⚡ Performance Benchmark" << endl;
    cout << string(80, '=') << endl;
    cout << "\nInsertion sort is preferred for:" << endl;
    cout << "  • Small arrays (typically n < 10-20)" << endl;
    cout << "  • Nearly sorted arrays" << endl;
    cout << "  • As part of hybrid sorting algorithms" << endl;
    cout << endl;

    vector<size_t> sizes = {5, 10, 20, 50, 100, 500, 1000};
    random_device rd;
    mt19937 gen(42);
    uniform_int_distribution<> dis(1, 1000);

    map<string, function<vector<int>(size_t)>> patterns;
    patterns["Random"] = [&](size_t n) {
        vector<int> arr(n);
        generate(arr.begin(), arr.end(), [&]() { return dis(gen); });
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
    patterns["Reversed"] = [](size_t n) {
        vector<int> arr(n);
        iota(arr.begin(), arr.end(), 0);
        reverse(arr.begin(), arr.end());
        return arr;
    };

    for (const auto& [patternName, patternGen] : patterns) {
        cout << "\n" << patternName << " Data:" << endl;
        cout << left << setw(8) << "Size" << right << setw(15) << "Insertion"
             << setw(15) << "Binary" << setw(15) << "Shell" << setw(15) << "std::sort" << endl;
        cout << string(68, '-') << endl;

        for (size_t size : sizes) {
            auto testData = patternGen(size);
            cout << left << setw(8) << size;

            // Insertion Sort
            auto start = high_resolution_clock::now();
            insertionSort(testData);
            auto end = high_resolution_clock::now();
            auto duration = duration_cast<microseconds>(end - start);
            cout << right << setw(14) << fixed << setprecision(3) << duration.count() / 1000.0 << "ms";

            // Binary Insertion Sort
            start = high_resolution_clock::now();
            binaryInsertionSort(testData);
            end = high_resolution_clock::now();
            duration = duration_cast<microseconds>(end - start);
            cout << setw(14) << duration.count() / 1000.0 << "ms";

            // Shell Sort
            start = high_resolution_clock::now();
            shellSort(testData);
            end = high_resolution_clock::now();
            duration = duration_cast<microseconds>(end - start);
            cout << setw(14) << duration.count() / 1000.0 << "ms";

            // std::sort
            auto testData2 = testData;
            start = high_resolution_clock::now();
            sort(testData2.begin(), testData2.end());
            end = high_resolution_clock::now();
            duration = duration_cast<microseconds>(end - start);
            cout << setw(14) << duration.count() / 1000.0 << "ms" << endl;
        }
    }
}

int main() {
    demonstrateInsertionSort();
    performanceBenchmark();

    cout << "\n✨ Insertion Sort demonstration complete!" << endl;

    return 0;
}
