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
 */

import java.util.Arrays;
import java.util.Random;

public class FibonacciSearch {

    /**
     * Perform Fibonacci search on a sorted array
     * @param arr Sorted array of integers
     * @param target Value to search for
     * @return Index of target if found, -1 otherwise
     */
    public static int fibonacciSearch(int[] arr, int target) {
        int n = arr.length;
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
            int i = Math.min(offset + fibM2, n - 1);

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
        if (fibM1 == 1 && offset + 1 < n && arr[offset + 1] == target) {
            return offset + 1;
        }

        return -1;
    }

    /**
     * Optimized Fibonacci search with early termination
     * @param arr Sorted array of integers
     * @param target Value to search for
     * @return Index of target if found, -1 otherwise
     */
    public static int fibonacciSearchOptimized(int[] arr, int target) {
        int n = arr.length;
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
            int i = Math.min(offset + fibM2, n - 1);

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

        if (fibM1 == 1 && offset + 1 < n && arr[offset + 1] == target) {
            return offset + 1;
        }

        return -1;
    }

    /**
     * Binary search for comparison
     */
    private static int binarySearch(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
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
    private static int jumpSearch(int[] arr, int target) {
        int n = arr.length;
        int jump = (int) Math.sqrt(n);
        int prev = 0;

        while (prev < n && arr[Math.min(prev + jump, n - 1)] < target) {
            prev += jump;
        }

        for (int i = Math.max(0, prev - jump); i < Math.min(prev + jump, n); i++) {
            if (arr[i] == target) return i;
        }
        return -1;
    }

    public static void main(String[] args) {
        // Test correctness
        int[] testArr = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29};
        System.out.println("Test Array: " + Arrays.toString(testArr));
        System.out.println("Fibonacci Search for 15: Index " + fibonacciSearch(testArr, 15));
        System.out.println("Fibonacci Search for 20: Index " + fibonacciSearch(testArr, 20));
        System.out.println("Fibonacci Search for 1: Index " + fibonacciSearch(testArr, 1));
        System.out.println("Fibonacci Search for 29: Index " + fibonacciSearch(testArr, 29));

        // Performance comparison
        System.out.println("\n--- Performance Comparison ---");
        int[] sizes = {1000, 10000, 100000, 1000000};
        Random rand = new Random(42);

        for (int size : sizes) {
            int[] arr = new int[size];
            for (int i = 0; i < size; i++) {
                arr[i] = i * 2;
            }
            int target = arr[rand.nextInt(arr.length)];

            // Warm-up
            for (int i = 0; i < 100; i++) {
                fibonacciSearch(arr, target);
                binarySearch(arr, target);
                jumpSearch(arr, target);
            }

            // Fibonacci search
            long fibStart = System.nanoTime();
            for (int i = 0; i < 10000; i++) {
                fibonacciSearch(arr, target);
            }
            long fibTime = System.nanoTime() - fibStart;

            // Binary search
            long binaryStart = System.nanoTime();
            for (int i = 0; i < 10000; i++) {
                binarySearch(arr, target);
            }
            long binaryTime = System.nanoTime() - binaryStart;

            // Jump search
            long jumpStart = System.nanoTime();
            for (int i = 0; i < 10000; i++) {
                jumpSearch(arr, target);
            }
            long jumpTime = System.nanoTime() - jumpStart;

            System.out.printf("\nArray size: %,d%n", size);
            System.out.printf("Fibonacci Search: %.3fms%n", fibTime / 1_000_000.0);
            System.out.printf("Binary Search: %.3fms%n", binaryTime / 1_000_000.0);
            System.out.printf("Jump Search: %.3fms%n", jumpTime / 1_000_000.0);
            System.out.printf("Ratio (Fib/Binary): %.2fx%n", (double) fibTime / binaryTime);
            System.out.printf("Ratio (Fib/Jump): %.2fx%n", (double) fibTime / jumpTime);
        }

        // Performance on different data distributions
        System.out.println("\n--- Performance on Different Data Distributions ---");

        // Uniform distribution
        int[] arrUniform = new int[100000];
        for (int i = 0; i < arrUniform.length; i++) {
            arrUniform[i] = i;
        }
        int target1 = 75000;

        long uniformStart = System.nanoTime();
        for (int i = 0; i < 10000; i++) {
            fibonacciSearch(arrUniform, target1);
        }
        long uniformTime = System.nanoTime() - uniformStart;
        System.out.printf("Uniform distribution: %.3fms%n", uniformTime / 1_000_000.0);

        // Sparse distribution
        int[] arrSparse = new int[10000];
        for (int i = 0; i < arrSparse.length; i++) {
            arrSparse[i] = i * 10;
        }
        int target2 = 75000;

        long sparseStart = System.nanoTime();
        for (int i = 0; i < 10000; i++) {
            fibonacciSearch(arrSparse, target2);
        }
        long sparseTime = System.nanoTime() - sparseStart;
        System.out.printf("Sparse distribution: %.3fms%n", sparseTime / 1_000_000.0);
    }
}
