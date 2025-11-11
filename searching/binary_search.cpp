/**
 * Comprehensive Binary Search Algorithm Collection - C++
 * =======================================================
 *
 * A complete collection of binary search algorithms implemented
 * in modern C++ (C++17) with templates and STL integration.
 *
 * Algorithms included:
 * 1. Classic Binary Search (iterative & recursive)
 * 2. First/Last Occurrence
 * 3. Rotated Sorted Array Search
 * 4. Exponential Search
 * 5. Interpolation Search
 * 6. Ternary Search
 * 7. Binary Search on Answer (optimization problems)
 * 8. Advanced Utilities
 *
 * Compilation: g++ -std=c++17 -O2 -o binary_search binary_search.cpp
 * Usage: ./binary_search
 */

#include <iostream>
#include <vector>
#include <functional>
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <string>

using namespace std;

// ============================================================================
// 1. CLASSIC BINARY SEARCH
// ============================================================================

/**
 * Classic binary search - Iterative template implementation
 *
 * Template Parameters:
 *   T - Type of elements (must be comparable)
 *
 * Time: O(log n), Space: O(1)
 */
template<typename T>
int binarySearchIterative(const vector<T>& arr, const T& target) {
    int left = 0;
    int right = arr.size() - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1;
}

/**
 * Classic binary search - Recursive implementation
 *
 * Time: O(log n), Space: O(log n) for recursion
 */
template<typename T>
int binarySearchRecursiveHelper(const vector<T>& arr, const T& target,
                                 int left, int right) {
    if (left > right) {
        return -1;
    }

    int mid = left + (right - left) / 2;

    if (arr[mid] == target) {
        return mid;
    } else if (arr[mid] < target) {
        return binarySearchRecursiveHelper(arr, target, mid + 1, right);
    } else {
        return binarySearchRecursiveHelper(arr, target, left, mid - 1);
    }
}

template<typename T>
int binarySearchRecursive(const vector<T>& arr, const T& target) {
    return binarySearchRecursiveHelper(arr, target, 0, arr.size() - 1);
}

/**
 * Binary search with custom comparator
 *
 * Comparator should return:
 *   negative if a < b
 *   0 if a == b
 *   positive if a > b
 */
template<typename T, typename Compare>
int binarySearchWithComparator(const vector<T>& arr, const T& target,
                               Compare comp) {
    int left = 0;
    int right = arr.size() - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;
        int cmp = comp(arr[mid], target);

        if (cmp == 0) {
            return mid;
        } else if (cmp < 0) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1;
}

// ============================================================================
// 2. FIRST/LAST OCCURRENCE (for arrays with duplicates)
// ============================================================================

/**
 * Find first occurrence of target in sorted array
 *
 * Time: O(log n), Space: O(1)
 */
template<typename T>
int findFirstOccurrence(const vector<T>& arr, const T& target) {
    int left = 0;
    int right = arr.size() - 1;
    int result = -1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
            result = mid;
            right = mid - 1;  // Continue searching left
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return result;
}

/**
 * Find last occurrence of target in sorted array
 *
 * Time: O(log n), Space: O(1)
 */
template<typename T>
int findLastOccurrence(const vector<T>& arr, const T& target) {
    int left = 0;
    int right = arr.size() - 1;
    int result = -1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
            result = mid;
            left = mid + 1;  // Continue searching right
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return result;
}

/**
 * Count occurrences of target
 *
 * Time: O(log n), Space: O(1)
 */
template<typename T>
int countOccurrences(const vector<T>& arr, const T& target) {
    int first = findFirstOccurrence(arr, target);
    if (first == -1) return 0;

    int last = findLastOccurrence(arr, target);
    return last - first + 1;
}

/**
 * Find range [first, last] of target occurrences
 *
 * Time: O(log n), Space: O(1)
 */
template<typename T>
pair<int, int> findRange(const vector<T>& arr, const T& target) {
    int first = findFirstOccurrence(arr, target);
    if (first == -1) return {-1, -1};

    int last = findLastOccurrence(arr, target);
    return {first, last};
}

// ============================================================================
// 3. ROTATED SORTED ARRAY SEARCH
// ============================================================================

/**
 * Search in rotated sorted array
 *
 * Example: [4, 5, 6, 7, 0, 1, 2] (rotated from [0, 1, 2, 4, 5, 6, 7])
 *
 * Time: O(log n), Space: O(1)
 */
template<typename T>
int searchRotatedArray(const vector<T>& arr, const T& target) {
    int left = 0;
    int right = arr.size() - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
            return mid;
        }

        // Determine which half is sorted
        if (arr[left] <= arr[mid]) {
            // Left half is sorted
            if (arr[left] <= target && target < arr[mid]) {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        } else {
            // Right half is sorted
            if (arr[mid] < target && target <= arr[right]) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
    }

    return -1;
}

/**
 * Find rotation point (minimum element)
 *
 * Time: O(log n), Space: O(1)
 */
template<typename T>
int findRotationPoint(const vector<T>& arr) {
    int left = 0;
    int right = arr.size() - 1;

    while (left < right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] > arr[right]) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    return left;
}

// ============================================================================
// 4. EXPONENTIAL SEARCH
// ============================================================================

/**
 * Exponential search - finds range then applies binary search
 *
 * Time: O(log n), Space: O(1)
 */
template<typename T>
int exponentialSearch(const vector<T>& arr, const T& target) {
    int n = arr.size();

    if (n == 0) return -1;
    if (arr[0] == target) return 0;

    // Find range for binary search
    int i = 1;
    while (i < n && arr[i] <= target) {
        i *= 2;
    }

    // Binary search in range [i/2, min(i, n-1)]
    int left = i / 2;
    int right = min(i, n - 1);

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1;
}

// ============================================================================
// 5. INTERPOLATION SEARCH
// ============================================================================

/**
 * Interpolation search for uniformly distributed numerical data
 *
 * Time: O(log log n) average, O(n) worst
 * Space: O(1)
 */
int interpolationSearch(const vector<int>& arr, int target) {
    int left = 0;
    int right = arr.size() - 1;

    while (left <= right && target >= arr[left] && target <= arr[right]) {
        if (left == right) {
            return arr[left] == target ? left : -1;
        }

        // Interpolation formula
        int pos = left + ((target - arr[left]) * (right - left)) /
                         (arr[right] - arr[left]);

        if (arr[pos] == target) {
            return pos;
        } else if (arr[pos] < target) {
            left = pos + 1;
        } else {
            right = pos - 1;
        }
    }

    return -1;
}

// ============================================================================
// 6. TERNARY SEARCH
// ============================================================================

/**
 * Ternary search on sorted array
 *
 * Time: O(log₃ n) ≈ O(log n)
 * Space: O(1)
 */
template<typename T>
int ternarySearch(const vector<T>& arr, const T& target) {
    int left = 0;
    int right = arr.size() - 1;

    while (left <= right) {
        int mid1 = left + (right - left) / 3;
        int mid2 = right - (right - left) / 3;

        if (arr[mid1] == target) return mid1;
        if (arr[mid2] == target) return mid2;

        if (target < arr[mid1]) {
            right = mid1 - 1;
        } else if (target > arr[mid2]) {
            left = mid2 + 1;
        } else {
            left = mid1 + 1;
            right = mid2 - 1;
        }
    }

    return -1;
}

/**
 * Ternary search for finding maximum of unimodal function
 *
 * Time: O(log₃(range/precision))
 */
template<typename Func>
double ternarySearchMaximum(Func fn, double left, double right,
                            double precision = 1e-6) {
    while (right - left > precision) {
        double mid1 = left + (right - left) / 3.0;
        double mid2 = right - (right - left) / 3.0;

        if (fn(mid1) < fn(mid2)) {
            left = mid1;
        } else {
            right = mid2;
        }
    }

    return (left + right) / 2.0;
}

// ============================================================================
// 7. BINARY SEARCH ON ANSWER (Optimization Problems)
// ============================================================================

/**
 * Binary search on answer space with predicate function
 *
 * Finds smallest value in range where predicate returns true
 *
 * Time: O(log(range) * T) where T is predicate evaluation time
 */
template<typename Predicate>
int binarySearchOnAnswer(Predicate predicate, int left, int right) {
    int result = right + 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (predicate(mid)) {
            result = mid;
            right = mid - 1;  // Try to find smaller answer
        } else {
            left = mid + 1;
        }
    }

    return result;
}

/**
 * Find integer square root using binary search
 *
 * Time: O(log n), Space: O(1)
 */
int findSquareRoot(int n) {
    if (n < 0) throw invalid_argument("Square root of negative number");
    if (n <= 1) return n;

    int left = 1;
    int right = n / 2;
    int result = 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;
        long long square = (long long)mid * mid;

        if (square == n) {
            return mid;
        } else if (square < n) {
            result = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return result;
}

/**
 * Find square root with decimal precision
 *
 * Time: O(log(n/precision))
 */
double findSquareRootDecimal(double n, double precision = 0.01) {
    if (n < 0) throw invalid_argument("Square root of negative number");
    if (n <= 1) return n;

    double left = 0;
    double right = n;

    while (right - left > precision) {
        double mid = (left + right) / 2.0;
        double square = mid * mid;

        if (abs(square - n) < precision) {
            return mid;
        } else if (square < n) {
            left = mid;
        } else {
            right = mid;
        }
    }

    return (left + right) / 2.0;
}

// ============================================================================
// 8. ADVANCED UTILITIES
// ============================================================================

/**
 * Find insertion position for element in sorted array
 *
 * Time: O(log n), Space: O(1)
 */
template<typename T>
int findInsertPosition(const vector<T>& arr, const T& target) {
    int left = 0;
    int right = arr.size();

    while (left < right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    return left;
}

/**
 * Find closest element to target in sorted array
 *
 * Time: O(log n), Space: O(1)
 */
template<typename T>
int findClosest(const vector<T>& arr, const T& target) {
    if (arr.empty()) return -1;
    if (arr.size() == 1) return 0;

    int left = 0;
    int right = arr.size() - 1;

    while (left < right - 1) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid;
        } else {
            right = mid;
        }
    }

    // Compare distances
    if (abs(arr[left] - target) <= abs(arr[right] - target)) {
        return left;
    }
    return right;
}

/**
 * Find peak element in array
 *
 * Time: O(log n), Space: O(1)
 */
template<typename T>
int findPeakElement(const vector<T>& arr) {
    if (arr.empty()) return -1;
    if (arr.size() == 1) return 0;

    int left = 0;
    int right = arr.size() - 1;

    while (left < right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] < arr[mid + 1]) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    return left;
}

// ============================================================================
// HELPER FUNCTIONS FOR EXAMPLES
// ============================================================================

template<typename T>
void printVector(const vector<T>& arr, const string& label = "") {
    if (!label.empty()) {
        cout << label << ": ";
    }
    cout << "[";
    for (size_t i = 0; i < arr.size(); i++) {
        cout << arr[i];
        if (i < arr.size() - 1) cout << ", ";
    }
    cout << "]" << endl;
}

void printSeparator() {
    cout << string(70, '=') << endl;
}

// ============================================================================
// EXAMPLES AND TESTING
// ============================================================================

void exampleClassicSearch() {
    printSeparator();
    cout << "EXAMPLE 1: Classic Binary Search" << endl;
    printSeparator();

    vector<int> arr = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
    printVector(arr, "Array");

    cout << "Search for 7: index " << binarySearchIterative(arr, 7) << endl;
    cout << "Search for 11: index " << binarySearchRecursive(arr, 11) << endl;
    cout << "Search for 20: index " << binarySearchIterative(arr, 20) << endl;
    cout << endl;
}

void exampleFirstLastOccurrence() {
    printSeparator();
    cout << "EXAMPLE 2: First/Last Occurrence (Duplicates)" << endl;
    printSeparator();

    vector<int> arr = {1, 2, 2, 2, 3, 4, 4, 5, 5, 5, 5};
    printVector(arr, "Array");

    cout << "First occurrence of 2: index " << findFirstOccurrence(arr, 2) << endl;
    cout << "Last occurrence of 2: index " << findLastOccurrence(arr, 2) << endl;
    cout << "Count of 5: " << countOccurrences(arr, 5) << endl;

    auto [first, last] = findRange(arr, 4);
    cout << "Range of 4: [" << first << ", " << last << "]" << endl;
    cout << endl;
}

void exampleRotatedArray() {
    printSeparator();
    cout << "EXAMPLE 3: Rotated Sorted Array" << endl;
    printSeparator();

    vector<int> rotated = {4, 5, 6, 7, 0, 1, 2};
    printVector(rotated, "Array");

    cout << "Search for 0: index " << searchRotatedArray(rotated, 0) << endl;
    cout << "Search for 5: index " << searchRotatedArray(rotated, 5) << endl;
    cout << "Rotation point: index " << findRotationPoint(rotated) << endl;
    cout << endl;
}

void exampleSquareRoot() {
    printSeparator();
    cout << "EXAMPLE 4: Square Root using Binary Search" << endl;
    printSeparator();

    cout << fixed << setprecision(2);
    cout << "√50 (integer): " << findSquareRoot(50) << endl;
    cout << "√50 (decimal): " << findSquareRootDecimal(50, 0.01) << endl;
    cout << "√100: " << findSquareRoot(100) << endl;
    cout << endl;
}

void exampleBinarySearchOnAnswer() {
    printSeparator();
    cout << "EXAMPLE 5: Binary Search on Answer - Ship Packages" << endl;
    printSeparator();

    vector<int> weights = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int days = 5;

    auto canShip = [&weights, days](int capacity) {
        int dayCount = 1;
        int currentWeight = 0;

        for (int w : weights) {
            if (currentWeight + w > capacity) {
                dayCount++;
                currentWeight = w;
            } else {
                currentWeight += w;
            }
        }

        return dayCount <= days;
    };

    int minCapacity = binarySearchOnAnswer(canShip, 1, 55);

    printVector(weights, "Weights");
    cout << "Days: " << days << endl;
    cout << "Minimum ship capacity: " << minCapacity << endl;
    cout << endl;
}

void examplePeakElement() {
    printSeparator();
    cout << "EXAMPLE 6: Find Peak Element" << endl;
    printSeparator();

    vector<int> peaks = {1, 3, 20, 4, 1, 0};
    int peakIdx = findPeakElement(peaks);

    printVector(peaks, "Array");
    cout << "Peak at index " << peakIdx << ", value: " << peaks[peakIdx] << endl;
    cout << endl;
}

int main() {
    printSeparator();
    cout << "BINARY SEARCH ALGORITHM COLLECTION - C++" << endl;
    printSeparator();
    cout << endl;

    exampleClassicSearch();
    exampleFirstLastOccurrence();
    exampleRotatedArray();
    exampleSquareRoot();
    exampleBinarySearchOnAnswer();
    examplePeakElement();

    printSeparator();
    cout << "All examples completed!" << endl;
    printSeparator();

    return 0;
}
