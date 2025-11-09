/**
 * Heap Sort Algorithm Implementation in C++
 *
 * Time Complexity: O(n log n) - consistently across all cases
 * Space Complexity: O(1) for in-place sorting, O(n) for auxiliary heap
 *
 * Heap Sort is a comparison-based sorting algorithm that uses a binary heap data
 * structure. It divides its input into a sorted and an unsorted region, and it
 * iteratively shrinks the unsorted region by extracting the largest element and
 * inserting it into the sorted region.
 *
 * C++ features:
 * - Template classes and functions
 * - STL integration
 * - Complete heap data structure
 * - Priority queue implementation
 * - Exception handling
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>
#include <iomanip>
#include <stdexcept>
#include <sstream>
#include <functional>

using namespace std;
using namespace std::chrono;

/**
 * Maintain the max-heap property for a subtree rooted at index i.
 *
 * Time Complexity: O(log n)
 */
template <typename T>
void heapifyMax(vector<T>& arr, size_t n, size_t i) {
    size_t largest = i;
    size_t left = 2 * i + 1;
    size_t right = 2 * i + 2;

    // Check if left child exists and is greater than root
    if (left < n && arr[left] > arr[largest]) {
        largest = left;
    }

    // Check if right child exists and is greater than largest so far
    if (right < n && arr[right] > arr[largest]) {
        largest = right;
    }

    // If largest is not root, swap and recursively heapify
    if (largest != i) {
        swap(arr[i], arr[largest]);
        heapifyMax(arr, n, largest);
    }
}

/**
 * Maintain the min-heap property for a subtree rooted at index i.
 *
 * Time Complexity: O(log n)
 */
template <typename T>
void heapifyMin(vector<T>& arr, size_t n, size_t i) {
    size_t smallest = i;
    size_t left = 2 * i + 1;
    size_t right = 2 * i + 2;

    if (left < n && arr[left] < arr[smallest]) {
        smallest = left;
    }

    if (right < n && arr[right] < arr[smallest]) {
        smallest = right;
    }

    if (smallest != i) {
        swap(arr[i], arr[smallest]);
        heapifyMin(arr, n, smallest);
    }
}

/**
 * Build a max-heap from an unordered array.
 *
 * Time Complexity: O(n)
 */
template <typename T>
void buildMaxHeap(vector<T>& arr) {
    size_t n = arr.size();
    // Start from the last non-leaf node and heapify each node
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapifyMax(arr, n, i);
    }
}

/**
 * Build a min-heap from an unordered array.
 *
 * Time Complexity: O(n)
 */
template <typename T>
void buildMinHeap(vector<T>& arr) {
    size_t n = arr.size();
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapifyMin(arr, n, i);
    }
}

/**
 * Sort a vector using heap sort algorithm.
 *
 * Time Complexity: O(n log n)
 */
template <typename T>
vector<T> heapSort(const vector<T>& arr) {
    if (arr.size() <= 1) {
        return arr;
    }

    vector<T> result = arr;
    size_t n = result.size();

    // Build a max heap
    buildMaxHeap(result);

    // Extract elements from heap one by one
    for (size_t i = n - 1; i > 0; i--) {
        // Move current root to end
        swap(result[0], result[i]);
        // Call heapify on the reduced heap
        heapifyMax(result, i, 0);
    }

    return result;
}

/**
 * Sort a vector in-place using heap sort algorithm.
 *
 * Time Complexity: O(n log n)
 * Space Complexity: O(1)
 */
template <typename T>
void heapSortInPlace(vector<T>& arr) {
    size_t n = arr.size();

    // Build a max heap
    buildMaxHeap(arr);

    // Extract elements from heap one by one
    for (size_t i = n - 1; i > 0; i--) {
        swap(arr[0], arr[i]);
        heapifyMax(arr, i, 0);
    }
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
 * Max-Heap data structure implementation.
 */
template <typename T>
class MaxHeap {
private:
    vector<T> heap;

    size_t parent(size_t i) const {
        return (i - 1) / 2;
    }

    size_t left(size_t i) const {
        return 2 * i + 1;
    }

    size_t right(size_t i) const {
        return 2 * i + 2;
    }

    void bubbleUp(size_t i) {
        while (i > 0 && heap[parent(i)] < heap[i]) {
            swap(heap[i], heap[parent(i)]);
            i = parent(i);
        }
    }

    void heapifyDown(size_t i) {
        size_t largest = i;
        size_t l = left(i);
        size_t r = right(i);

        if (l < heap.size() && heap[l] > heap[largest]) {
            largest = l;
        }

        if (r < heap.size() && heap[r] > heap[largest]) {
            largest = r;
        }

        if (largest != i) {
            swap(heap[i], heap[largest]);
            heapifyDown(largest);
        }
    }

public:
    MaxHeap() {}

    MaxHeap(const vector<T>& initialData) : heap(initialData) {
        buildHeap();
    }

    void buildHeap() {
        for (int i = heap.size() / 2 - 1; i >= 0; i--) {
            heapifyDown(i);
        }
    }

    /**
     * Insert a new key into the heap.
     *
     * Time Complexity: O(log n)
     */
    void insert(const T& key) {
        heap.push_back(key);
        bubbleUp(heap.size() - 1);
    }

    /**
     * Remove and return the maximum element (root) from the heap.
     *
     * Time Complexity: O(log n)
     */
    T extractMax() {
        if (heap.empty()) {
            throw out_of_range("extractMax from empty heap");
        }

        if (heap.size() == 1) {
            T max = heap.back();
            heap.pop_back();
            return max;
        }

        T max = heap[0];
        heap[0] = heap.back();
        heap.pop_back();
        heapifyDown(0);

        return max;
    }

    /**
     * Get the maximum element without removing it.
     */
    T getMax() const {
        if (heap.empty()) {
            throw out_of_range("getMax from empty heap");
        }
        return heap[0];
    }

    /**
     * Increase the value of a key at index i.
     */
    void increaseKey(size_t i, const T& newKey) {
        if (i >= heap.size()) {
            throw out_of_range("Index out of bounds");
        }

        if (newKey < heap[i]) {
            throw invalid_argument("New key is smaller than current key");
        }

        heap[i] = newKey;
        bubbleUp(i);
    }

    /**
     * Decrease the value of a key at index i.
     */
    void decreaseKey(size_t i, const T& newKey) {
        if (i >= heap.size()) {
            throw out_of_range("Index out of bounds");
        }

        if (newKey > heap[i]) {
            throw invalid_argument("New key is greater than current key");
        }

        heap[i] = newKey;
        heapifyDown(i);
    }

    size_t size() const {
        return heap.size();
    }

    bool isEmpty() const {
        return heap.empty();
    }

    vector<T> toVector() const {
        return heap;
    }

    /**
     * Create ASCII art visualization of the heap.
     */
    string visualize() const {
        if (heap.empty()) {
            return "Empty heap";
        }

        ostringstream oss;
        visualizeHelper(0, "", "", oss);
        return oss.str();
    }

private:
    void visualizeHelper(size_t i, const string& prefix, const string& childPrefix, ostringstream& oss) const {
        if (i >= heap.size()) {
            return;
        }

        oss << prefix << heap[i] << "\n";

        size_t leftIdx = left(i);
        size_t rightIdx = right(i);

        if (leftIdx < heap.size() || rightIdx < heap.size()) {
            if (leftIdx < heap.size()) {
                if (rightIdx < heap.size()) {
                    visualizeHelper(leftIdx, childPrefix + "├── ", childPrefix + "│   ", oss);
                } else {
                    visualizeHelper(leftIdx, childPrefix + "└── ", childPrefix + "    ", oss);
                }
            }

            if (rightIdx < heap.size()) {
                visualizeHelper(rightIdx, childPrefix + "└── ", childPrefix + "    ", oss);
            }
        }
    }
};

/**
 * Min-Heap data structure implementation.
 */
template <typename T>
class MinHeap {
private:
    vector<T> heap;

    size_t parent(size_t i) const {
        return (i - 1) / 2;
    }

    size_t left(size_t i) const {
        return 2 * i + 1;
    }

    size_t right(size_t i) const {
        return 2 * i + 2;
    }

    void bubbleUp(size_t i) {
        while (i > 0 && heap[parent(i)] > heap[i]) {
            swap(heap[i], heap[parent(i)]);
            i = parent(i);
        }
    }

    void heapifyDown(size_t i) {
        size_t smallest = i;
        size_t l = left(i);
        size_t r = right(i);

        if (l < heap.size() && heap[l] < heap[smallest]) {
            smallest = l;
        }

        if (r < heap.size() && heap[r] < heap[smallest]) {
            smallest = r;
        }

        if (smallest != i) {
            swap(heap[i], heap[smallest]);
            heapifyDown(smallest);
        }
    }

public:
    MinHeap() {}

    MinHeap(const vector<T>& initialData) : heap(initialData) {
        buildHeap();
    }

    void buildHeap() {
        for (int i = heap.size() / 2 - 1; i >= 0; i--) {
            heapifyDown(i);
        }
    }

    void insert(const T& key) {
        heap.push_back(key);
        bubbleUp(heap.size() - 1);
    }

    T extractMin() {
        if (heap.empty()) {
            throw out_of_range("extractMin from empty heap");
        }

        if (heap.size() == 1) {
            T min = heap.back();
            heap.pop_back();
            return min;
        }

        T min = heap[0];
        heap[0] = heap.back();
        heap.pop_back();
        heapifyDown(0);

        return min;
    }

    T getMin() const {
        if (heap.empty()) {
            throw out_of_range("getMin from empty heap");
        }
        return heap[0];
    }

    size_t size() const {
        return heap.size();
    }

    bool isEmpty() const {
        return heap.empty();
    }

    string visualize() const {
        if (heap.empty()) {
            return "Empty heap";
        }

        ostringstream oss;
        visualizeHelper(0, "", "", oss);
        return oss.str();
    }

private:
    void visualizeHelper(size_t i, const string& prefix, const string& childPrefix, ostringstream& oss) const {
        if (i >= heap.size()) {
            return;
        }

        oss << prefix << heap[i] << "\n";

        size_t leftIdx = left(i);
        size_t rightIdx = right(i);

        if (leftIdx < heap.size() || rightIdx < heap.size()) {
            if (leftIdx < heap.size()) {
                if (rightIdx < heap.size()) {
                    visualizeHelper(leftIdx, childPrefix + "├── ", childPrefix + "│   ", oss);
                } else {
                    visualizeHelper(leftIdx, childPrefix + "└── ", childPrefix + "    ", oss);
                }
            }

            if (rightIdx < heap.size()) {
                visualizeHelper(rightIdx, childPrefix + "└── ", childPrefix + "    ", oss);
            }
        }
    }
};

/**
 * Priority Queue implementation using a max-heap.
 */
template <typename T>
class PriorityQueue {
private:
    MaxHeap<T> heap;

public:
    void enqueue(const T& item) {
        heap.insert(item);
    }

    T dequeue() {
        return heap.extractMax();
    }

    T peek() const {
        return heap.getMax();
    }

    bool isEmpty() const {
        return heap.isEmpty();
    }

    size_t size() const {
        return heap.size();
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
 * Demonstrate heap sort and heap data structure.
 */
void demonstrateHeapSort() {
    cout << "🏔️  Heap Sort Implementation in C++" << endl;
    cout << string(60, '=') << endl;

    // Test data
    vector<vector<int>> testArrays = {
        {64, 34, 25, 12, 22, 11, 90},
        {5, 2, 8, 6, 1, 9, 4},
        {1},
        {},
        {3, 3, 3, 3, 3},
        {9, 8, 7, 6, 5, 4, 3, 2, 1},
        {1, 2, 3, 4, 5}
    };

    vector<string> descriptions = {
        "Random array",
        "Small random array",
        "Single element",
        "Empty array",
        "All duplicates",
        "Reverse sorted",
        "Already sorted"
    };

    cout << "\n📋 Basic Sorting Tests:" << endl;
    cout << string(60, '-') << endl;

    for (size_t i = 0; i < testArrays.size(); i++) {
        const auto& arr = testArrays[i];
        const auto& desc = descriptions[i];

        vector<int> original = arr;
        auto sortedArr = heapSort(arr);

        cout << "\nTest: " << desc << endl;
        printVector(original, "Original");
        printVector(sortedArr, "Sorted  ");
        cout << "Correct:  " << (isSorted(sortedArr) ? "✓" : "✗") << endl;
    }

    cout << "\n" << string(60, '-') << endl;

    // Demonstrate heap visualization
    cout << "\n🌲 Heap Visualization:" << endl;
    cout << string(60, '-') << endl;

    vector<int> data = {64, 34, 25, 12, 22, 11, 90};
    MaxHeap<int> maxHeap(data);

    cout << "\nMax-Heap built from: ";
    printVector(data, "");
    cout << maxHeap.visualize() << endl;

    cout << "Min-Heap built from: ";
    printVector(data, "");
    MinHeap<int> minHeap(data);
    cout << minHeap.visualize() << endl;

    // Demonstrate heap operations
    cout << "🔧 Heap Operations:" << endl;
    cout << string(60, '-') << endl;

    MaxHeap<int> heap;
    vector<int> operations = {50, 30, 70, 20, 40, 60, 80};

    cout << "\nInserting elements: ";
    printVector(operations, "");
    for (int val : operations) {
        heap.insert(val);
        cout << "Inserted " << val << ", Max: " << heap.getMax() << endl;
    }

    cout << "\nHeap structure:" << endl;
    cout << heap.visualize() << endl;

    cout << "Extracting elements:" << endl;
    vector<int> extracted;
    while (!heap.isEmpty()) {
        int val = heap.extractMax();
        extracted.push_back(val);
        cout << "Extracted: " << val << endl;
    }

    printVector(extracted, "Extraction order");

    // Demonstrate priority queue
    cout << "\n📬 Priority Queue Demo:" << endl;
    cout << string(60, '-') << endl;

    PriorityQueue<int> pq;
    vector<int> tasks = {5, 1, 9, 3, 7};

    cout << "\nEnqueuing tasks with priorities: ";
    printVector(tasks, "");
    for (int priority : tasks) {
        pq.enqueue(priority);
        cout << "Enqueued priority " << priority << ", Top priority: " << pq.peek() << endl;
    }

    cout << "\nProcessing tasks by priority:" << endl;
    while (!pq.isEmpty()) {
        int priority = pq.dequeue();
        cout << "Processing task with priority: " << priority << endl;
    }
}

/**
 * Benchmark heap sort.
 */
void performanceBenchmark() {
    cout << "\n\n⚡ Performance Benchmark" << endl;
    cout << string(80, '=') << endl;

    vector<size_t> sizes = {100, 500, 1000, 5000, 10000};
    random_device rd;
    mt19937 gen(42);
    uniform_int_distribution<> dis(1, 1000);

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

    for (const auto& [patternName, patternGen] : patterns) {
        cout << "\n" << patternName << " Data:" << endl;
        cout << left << setw(8) << "Size" << right << setw(15) << "Heap Sort" << setw(15) << "std::sort" << endl;
        cout << string(38, '-') << endl;

        for (size_t size : sizes) {
            auto testData = patternGen(size);
            cout << left << setw(8) << size;

            // Heap Sort
            auto start = high_resolution_clock::now();
            auto result = heapSort(testData);
            auto end = high_resolution_clock::now();
            auto duration = duration_cast<microseconds>(end - start);
            double elapsedMs = duration.count() / 1000.0;
            cout << right << setw(14) << fixed << setprecision(2) << elapsedMs << "ms";

            // std::sort
            auto testData2 = testData;
            start = high_resolution_clock::now();
            sort(testData2.begin(), testData2.end());
            end = high_resolution_clock::now();
            duration = duration_cast<microseconds>(end - start);
            elapsedMs = duration.count() / 1000.0;
            cout << setw(14) << elapsedMs << "ms" << endl;
        }
    }
}

/**
 * Test edge cases.
 */
void testEdgeCases() {
    cout << "\n\n🧪 Edge Cases and Error Handling" << endl;
    cout << string(60, '=') << endl;

    cout << "\n1. Testing empty heap operations:" << endl;
    try {
        MaxHeap<int> heap;
        heap.extractMax();
        cout << "   ✗ Should have thrown exception" << endl;
    } catch (const out_of_range& e) {
        cout << "   ✓ Correctly threw: " << e.what() << endl;
    }

    cout << "\n2. Testing increaseKey with smaller value:" << endl;
    try {
        MaxHeap<int> heap(vector<int>{10, 20, 30});
        heap.increaseKey(0, 5);
        cout << "   ✗ Should have thrown exception" << endl;
    } catch (const invalid_argument& e) {
        cout << "   ✓ Correctly threw: " << e.what() << endl;
    }

    cout << "\n3. Testing with duplicates:" << endl;
    vector<int> arr = {5, 5, 5, 5, 5};
    auto sorted = heapSort(arr);
    printVector(arr, "   Original");
    printVector(sorted, "   Sorted  ");
    cout << "   Correct:  " << (sorted == arr ? "✓" : "✗") << endl;
}

int main() {
    demonstrateHeapSort();
    performanceBenchmark();
    testEdgeCases();

    cout << "\n✨ Heap Sort demonstration complete!" << endl;

    return 0;
}
