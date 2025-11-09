/**
 * Heap Sort Algorithm Implementation in Java
 *
 * Time Complexity: O(n log n) - consistently across all cases
 * Space Complexity: O(1) for in-place sorting, O(n) for auxiliary heap
 *
 * Heap Sort is a comparison-based sorting algorithm that uses a binary heap data
 * structure. It divides its input into a sorted and an unsorted region, and it
 * iteratively shrinks the unsorted region by extracting the largest element and
 * inserting it into the sorted region.
 *
 * Java features:
 * - Generic classes and methods
 * - Complete heap data structure
 * - Priority queue implementation
 * - Comprehensive error handling
 * - Visual representation
 */

import java.util.*;
import java.util.function.BiFunction;

public class HeapSort {

    /**
     * Maintain the max-heap property for a subtree rooted at index i.
     *
     * @param arr The array representing the heap
     * @param n   Size of the heap
     * @param i   Index of the root of the subtree
     * @param <T> Type of elements
     *
     * Time Complexity: O(log n)
     */
    public static <T extends Comparable<T>> void heapifyMax(T[] arr, int n, int i) {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        // Check if left child exists and is greater than root
        if (left < n && arr[left].compareTo(arr[largest]) > 0) {
            largest = left;
        }

        // Check if right child exists and is greater than largest so far
        if (right < n && arr[right].compareTo(arr[largest]) > 0) {
            largest = right;
        }

        // If largest is not root, swap and recursively heapify
        if (largest != i) {
            swap(arr, i, largest);
            heapifyMax(arr, n, largest);
        }
    }

    /**
     * Maintain the min-heap property for a subtree rooted at index i.
     *
     * @param arr The array representing the heap
     * @param n   Size of the heap
     * @param i   Index of the root of the subtree
     * @param <T> Type of elements
     *
     * Time Complexity: O(log n)
     */
    public static <T extends Comparable<T>> void heapifyMin(T[] arr, int n, int i) {
        int smallest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < n && arr[left].compareTo(arr[smallest]) < 0) {
            smallest = left;
        }

        if (right < n && arr[right].compareTo(arr[smallest]) < 0) {
            smallest = right;
        }

        if (smallest != i) {
            swap(arr, i, smallest);
            heapifyMin(arr, n, smallest);
        }
    }

    /**
     * Build a max-heap from an unordered array.
     *
     * @param arr Array to be converted into a max-heap
     * @param <T> Type of elements
     *
     * Time Complexity: O(n)
     */
    public static <T extends Comparable<T>> void buildMaxHeap(T[] arr) {
        int n = arr.length;
        // Start from the last non-leaf node and heapify each node
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapifyMax(arr, n, i);
        }
    }

    /**
     * Build a min-heap from an unordered array.
     *
     * @param arr Array to be converted into a min-heap
     * @param <T> Type of elements
     *
     * Time Complexity: O(n)
     */
    public static <T extends Comparable<T>> void buildMinHeap(T[] arr) {
        int n = arr.length;
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapifyMin(arr, n, i);
        }
    }

    /**
     * Sort an array using heap sort algorithm.
     *
     * @param arr Array to be sorted
     * @param <T> Type of elements
     * @return New sorted array
     *
     * Time Complexity: O(n log n)
     */
    public static <T extends Comparable<T>> T[] heapSort(T[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        T[] result = arr.clone();
        heapSortInPlace(result);
        return result;
    }

    /**
     * Sort an array in-place using heap sort algorithm.
     *
     * @param arr Array to be sorted in-place
     * @param <T> Type of elements
     *
     * Time Complexity: O(n log n)
     * Space Complexity: O(1)
     */
    public static <T extends Comparable<T>> void heapSortInPlace(T[] arr) {
        int n = arr.length;

        // Build a max heap
        buildMaxHeap(arr);

        // Extract elements from heap one by one
        for (int i = n - 1; i > 0; i--) {
            // Move current root to end
            swap(arr, 0, i);
            // Call heapify on the reduced heap
            heapifyMax(arr, i, 0);
        }
    }

    /**
     * Heap sort for int arrays.
     */
    public static int[] heapSort(int[] arr) {
        if (arr.length <= 1) {
            return arr.clone();
        }

        int[] result = arr.clone();
        heapSortInPlace(result);
        return result;
    }

    /**
     * In-place heap sort for int arrays.
     */
    public static void heapSortInPlace(int[] arr) {
        int n = arr.length;

        // Build max heap
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapifyMaxInt(arr, n, i);
        }

        // Extract elements
        for (int i = n - 1; i > 0; i--) {
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;
            heapifyMaxInt(arr, i, 0);
        }
    }

    private static void heapifyMaxInt(int[] arr, int n, int i) {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < n && arr[left] > arr[largest]) {
            largest = left;
        }

        if (right < n && arr[right] > arr[largest]) {
            largest = right;
        }

        if (largest != i) {
            int temp = arr[i];
            arr[i] = arr[largest];
            arr[largest] = temp;
            heapifyMaxInt(arr, n, largest);
        }
    }

    private static <T> void swap(T[] arr, int i, int j) {
        T temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    /**
     * Check if array is sorted.
     */
    public static <T extends Comparable<T>> boolean isSorted(T[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            if (arr[i].compareTo(arr[i + 1]) > 0) {
                return false;
            }
        }
        return true;
    }

    public static boolean isSorted(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            if (arr[i] > arr[i + 1]) {
                return false;
            }
        }
        return true;
    }

    /**
     * Max-Heap data structure implementation.
     *
     * @param <T> Type of elements (must be Comparable)
     */
    public static class MaxHeap<T extends Comparable<T>> {
        private ArrayList<T> heap;

        public MaxHeap() {
            this.heap = new ArrayList<>();
        }

        public MaxHeap(T[] initialData) {
            this.heap = new ArrayList<>(Arrays.asList(initialData));
            buildHeap();
        }

        private int parent(int i) {
            return (i - 1) / 2;
        }

        private int left(int i) {
            return 2 * i + 1;
        }

        private int right(int i) {
            return 2 * i + 2;
        }

        private void buildHeap() {
            for (int i = heap.size() / 2 - 1; i >= 0; i--) {
                heapifyDown(i);
            }
        }

        /**
         * Insert a new key into the heap.
         *
         * Time Complexity: O(log n)
         */
        public void insert(T key) {
            heap.add(key);
            bubbleUp(heap.size() - 1);
        }

        private void bubbleUp(int i) {
            while (i > 0 && heap.get(parent(i)).compareTo(heap.get(i)) < 0) {
                Collections.swap(heap, i, parent(i));
                i = parent(i);
            }
        }

        /**
         * Remove and return the maximum element (root) from the heap.
         *
         * Time Complexity: O(log n)
         */
        public T extractMax() {
            if (heap.isEmpty()) {
                throw new NoSuchElementException("extractMax from empty heap");
            }

            if (heap.size() == 1) {
                return heap.remove(0);
            }

            T max = heap.get(0);
            heap.set(0, heap.remove(heap.size() - 1));
            heapifyDown(0);

            return max;
        }

        private void heapifyDown(int i) {
            int largest = i;
            int left = left(i);
            int right = right(i);

            if (left < heap.size() && heap.get(left).compareTo(heap.get(largest)) > 0) {
                largest = left;
            }

            if (right < heap.size() && heap.get(right).compareTo(heap.get(largest)) > 0) {
                largest = right;
            }

            if (largest != i) {
                Collections.swap(heap, i, largest);
                heapifyDown(largest);
            }
        }

        /**
         * Get the maximum element without removing it.
         */
        public T getMax() {
            if (heap.isEmpty()) {
                throw new NoSuchElementException("getMax from empty heap");
            }
            return heap.get(0);
        }

        /**
         * Increase the value of a key at index i.
         */
        public void increaseKey(int i, T newKey) {
            if (i < 0 || i >= heap.size()) {
                throw new IndexOutOfBoundsException("Index " + i + " out of bounds");
            }

            if (newKey.compareTo(heap.get(i)) < 0) {
                throw new IllegalArgumentException("New key is smaller than current key");
            }

            heap.set(i, newKey);
            bubbleUp(i);
        }

        /**
         * Decrease the value of a key at index i.
         */
        public void decreaseKey(int i, T newKey) {
            if (i < 0 || i >= heap.size()) {
                throw new IndexOutOfBoundsException("Index " + i + " out of bounds");
            }

            if (newKey.compareTo(heap.get(i)) > 0) {
                throw new IllegalArgumentException("New key is greater than current key");
            }

            heap.set(i, newKey);
            heapifyDown(i);
        }

        public int size() {
            return heap.size();
        }

        public boolean isEmpty() {
            return heap.isEmpty();
        }

        public List<T> toList() {
            return new ArrayList<>(heap);
        }

        /**
         * Create ASCII art visualization of the heap.
         */
        public String visualize() {
            if (heap.isEmpty()) {
                return "Empty heap";
            }

            StringBuilder sb = new StringBuilder();
            visualizeHelper(0, "", "", sb);
            return sb.toString();
        }

        private void visualizeHelper(int i, String prefix, String childPrefix, StringBuilder sb) {
            if (i >= heap.size()) {
                return;
            }

            sb.append(prefix).append(heap.get(i)).append("\n");

            int leftIdx = left(i);
            int rightIdx = right(i);

            if (leftIdx < heap.size() || rightIdx < heap.size()) {
                if (leftIdx < heap.size()) {
                    if (rightIdx < heap.size()) {
                        visualizeHelper(leftIdx, childPrefix + "├── ", childPrefix + "│   ", sb);
                    } else {
                        visualizeHelper(leftIdx, childPrefix + "└── ", childPrefix + "    ", sb);
                    }
                }

                if (rightIdx < heap.size()) {
                    visualizeHelper(rightIdx, childPrefix + "└── ", childPrefix + "    ", sb);
                }
            }
        }
    }

    /**
     * Min-Heap data structure implementation.
     */
    public static class MinHeap<T extends Comparable<T>> {
        private ArrayList<T> heap;

        public MinHeap() {
            this.heap = new ArrayList<>();
        }

        public MinHeap(T[] initialData) {
            this.heap = new ArrayList<>(Arrays.asList(initialData));
            buildHeap();
        }

        private int parent(int i) {
            return (i - 1) / 2;
        }

        private int left(int i) {
            return 2 * i + 1;
        }

        private int right(int i) {
            return 2 * i + 2;
        }

        private void buildHeap() {
            for (int i = heap.size() / 2 - 1; i >= 0; i--) {
                heapifyDown(i);
            }
        }

        public void insert(T key) {
            heap.add(key);
            bubbleUp(heap.size() - 1);
        }

        private void bubbleUp(int i) {
            while (i > 0 && heap.get(parent(i)).compareTo(heap.get(i)) > 0) {
                Collections.swap(heap, i, parent(i));
                i = parent(i);
            }
        }

        public T extractMin() {
            if (heap.isEmpty()) {
                throw new NoSuchElementException("extractMin from empty heap");
            }

            if (heap.size() == 1) {
                return heap.remove(0);
            }

            T min = heap.get(0);
            heap.set(0, heap.remove(heap.size() - 1));
            heapifyDown(0);

            return min;
        }

        private void heapifyDown(int i) {
            int smallest = i;
            int left = left(i);
            int right = right(i);

            if (left < heap.size() && heap.get(left).compareTo(heap.get(smallest)) < 0) {
                smallest = left;
            }

            if (right < heap.size() && heap.get(right).compareTo(heap.get(smallest)) < 0) {
                smallest = right;
            }

            if (smallest != i) {
                Collections.swap(heap, i, smallest);
                heapifyDown(smallest);
            }
        }

        public T getMin() {
            if (heap.isEmpty()) {
                throw new NoSuchElementException("getMin from empty heap");
            }
            return heap.get(0);
        }

        public int size() {
            return heap.size();
        }

        public boolean isEmpty() {
            return heap.isEmpty();
        }

        public String visualize() {
            if (heap.isEmpty()) {
                return "Empty heap";
            }

            StringBuilder sb = new StringBuilder();
            visualizeHelper(0, "", "", sb);
            return sb.toString();
        }

        private void visualizeHelper(int i, String prefix, String childPrefix, StringBuilder sb) {
            if (i >= heap.size()) {
                return;
            }

            sb.append(prefix).append(heap.get(i)).append("\n");

            int leftIdx = left(i);
            int rightIdx = right(i);

            if (leftIdx < heap.size() || rightIdx < heap.size()) {
                if (leftIdx < heap.size()) {
                    if (rightIdx < heap.size()) {
                        visualizeHelper(leftIdx, childPrefix + "├── ", childPrefix + "│   ", sb);
                    } else {
                        visualizeHelper(leftIdx, childPrefix + "└── ", childPrefix + "    ", sb);
                    }
                }

                if (rightIdx < heap.size()) {
                    visualizeHelper(rightIdx, childPrefix + "└── ", childPrefix + "    ", sb);
                }
            }
        }
    }

    /**
     * Priority Queue implementation using a max-heap.
     */
    public static class PriorityQueue<T extends Comparable<T>> {
        private MaxHeap<T> heap;

        public PriorityQueue() {
            this.heap = new MaxHeap<>();
        }

        public void enqueue(T item) {
            heap.insert(item);
        }

        public T dequeue() {
            return heap.extractMax();
        }

        public T peek() {
            return heap.getMax();
        }

        public boolean isEmpty() {
            return heap.isEmpty();
        }

        public int size() {
            return heap.size();
        }
    }

    /**
     * Demonstrate heap sort and heap data structure.
     */
    public static void demonstrateHeapSort() {
        System.out.println("🏔️  Heap Sort Implementation in Java");
        System.out.println("=".repeat(60));

        // Test data
        Object[][] testCases = {
            {new Integer[]{64, 34, 25, 12, 22, 11, 90}, "Random array"},
            {new Integer[]{5, 2, 8, 6, 1, 9, 4}, "Small random array"},
            {new Integer[]{1}, "Single element"},
            {new Integer[]{}, "Empty array"},
            {new Integer[]{3, 3, 3, 3, 3}, "All duplicates"},
            {new Integer[]{9, 8, 7, 6, 5, 4, 3, 2, 1}, "Reverse sorted"},
            {new Integer[]{1, 2, 3, 4, 5}, "Already sorted"}
        };

        System.out.println("\n📋 Basic Sorting Tests:");
        System.out.println("-".repeat(60));

        for (Object[] testCase : testCases) {
            Integer[] arr = (Integer[]) testCase[0];
            String desc = (String) testCase[1];

            Integer[] original = arr.clone();
            Integer[] sortedArr = heapSort(arr);

            System.out.println("\nTest: " + desc);
            System.out.println("Original: " + Arrays.toString(original));
            System.out.println("Sorted:   " + Arrays.toString(sortedArr));
            System.out.println("Correct:  " + (isSorted(sortedArr) ? "✓" : "✗"));
        }

        System.out.println("\n" + "-".repeat(60));

        // Demonstrate heap visualization
        System.out.println("\n🌲 Heap Visualization:");
        System.out.println("-".repeat(60));

        Integer[] data = {64, 34, 25, 12, 22, 11, 90};
        MaxHeap<Integer> maxHeap = new MaxHeap<>(data);

        System.out.println("\nMax-Heap built from: " + Arrays.toString(data));
        System.out.println(maxHeap.visualize());

        System.out.println("Min-Heap built from: " + Arrays.toString(data));
        MinHeap<Integer> minHeap = new MinHeap<>(data);
        System.out.println(minHeap.visualize());

        // Demonstrate heap operations
        System.out.println("🔧 Heap Operations:");
        System.out.println("-".repeat(60));

        MaxHeap<Integer> heap = new MaxHeap<>();
        int[] operations = {50, 30, 70, 20, 40, 60, 80};

        System.out.println("\nInserting elements: " + Arrays.toString(operations));
        for (int val : operations) {
            heap.insert(val);
            System.out.println("Inserted " + val + ", Max: " + heap.getMax());
        }

        System.out.println("\nHeap structure:");
        System.out.println(heap.visualize());

        System.out.println("Extracting elements:");
        List<Integer> extracted = new ArrayList<>();
        while (!heap.isEmpty()) {
            int val = heap.extractMax();
            extracted.add(val);
            System.out.println("Extracted: " + val);
        }

        System.out.println("Extraction order: " + extracted);

        // Demonstrate priority queue
        System.out.println("\n📬 Priority Queue Demo:");
        System.out.println("-".repeat(60));

        PriorityQueue<Integer> pq = new PriorityQueue<>();
        int[] tasks = {5, 1, 9, 3, 7};

        System.out.println("\nEnqueuing tasks with priorities: " + Arrays.toString(tasks));
        for (int priority : tasks) {
            pq.enqueue(priority);
            System.out.println("Enqueued priority " + priority + ", Top priority: " + pq.peek());
        }

        System.out.println("\nProcessing tasks by priority:");
        while (!pq.isEmpty()) {
            int priority = pq.dequeue();
            System.out.println("Processing task with priority: " + priority);
        }
    }

    /**
     * Benchmark heap sort.
     */
    public static void performanceBenchmark() {
        System.out.println("\n\n⚡ Performance Benchmark");
        System.out.println("=".repeat(80));

        int[] sizes = {100, 500, 1000, 5000, 10000};
        Random random = new Random(42);

        Map<String, java.util.function.Function<Integer, int[]>> patterns = new LinkedHashMap<>();
        patterns.put("Random", n -> random.ints(n, 1, 1001).toArray());
        patterns.put("Sorted", n -> java.util.stream.IntStream.range(0, n).toArray());
        patterns.put("Reversed", n -> java.util.stream.IntStream.range(0, n).map(i -> n - i).toArray());

        for (Map.Entry<String, java.util.function.Function<Integer, int[]>> pattern : patterns.entrySet()) {
            System.out.println("\n" + pattern.getKey() + " Data:");
            System.out.printf("%-8s%15s%15s%n", "Size", "Heap Sort", "Arrays.sort");
            System.out.println("-".repeat(38));

            for (int size : sizes) {
                int[] testData = pattern.getValue().apply(size);
                System.out.printf("%-8d", size);

                // Heap Sort
                long start = System.nanoTime();
                int[] result = heapSort(testData);
                long end = System.nanoTime();
                double elapsedMs = (end - start) / 1_000_000.0;
                System.out.printf("%14.2fms", elapsedMs);

                // Arrays.sort
                int[] testData2 = testData.clone();
                start = System.nanoTime();
                Arrays.sort(testData2);
                end = System.nanoTime();
                elapsedMs = (end - start) / 1_000_000.0;
                System.out.printf("%14.2fms%n", elapsedMs);
            }
        }
    }

    /**
     * Test edge cases.
     */
    public static void testEdgeCases() {
        System.out.println("\n\n🧪 Edge Cases and Error Handling");
        System.out.println("=".repeat(60));

        System.out.println("\n1. Testing empty heap operations:");
        try {
            MaxHeap<Integer> heap = new MaxHeap<>();
            heap.extractMax();
            System.out.println("   ✗ Should have thrown exception");
        } catch (NoSuchElementException e) {
            System.out.println("   ✓ Correctly threw: " + e.getMessage());
        }

        System.out.println("\n2. Testing increaseKey with smaller value:");
        try {
            MaxHeap<Integer> heap = new MaxHeap<>(new Integer[]{10, 20, 30});
            heap.increaseKey(0, 5);
            System.out.println("   ✗ Should have thrown exception");
        } catch (IllegalArgumentException e) {
            System.out.println("   ✓ Correctly threw: " + e.getMessage());
        }

        System.out.println("\n3. Testing with duplicates:");
        int[] arr = {5, 5, 5, 5, 5};
        int[] sorted = heapSort(arr);
        System.out.println("   Original: " + Arrays.toString(arr));
        System.out.println("   Sorted:   " + Arrays.toString(sorted));
        System.out.println("   Correct:  " + (Arrays.equals(sorted, arr) ? "✓" : "✗"));
    }

    public static void main(String[] args) {
        demonstrateHeapSort();
        performanceBenchmark();
        testEdgeCases();

        System.out.println("\n✨ Heap Sort demonstration complete!");
    }
}
