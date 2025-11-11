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

import java.util.Arrays;
import java.util.Random;

public class JumpSearch {

    /**
     * Perform jump search on a sorted array
     * @param arr Sorted array of integers
     * @param target Value to search for
     * @return Index of target if found, -1 otherwise
     */
    public static int jumpSearch(int[] arr, int target) {
        int n = arr.length;
        if (n == 0) return -1;

        // Calculate optimal jump size: √n
        int jump = (int) Math.sqrt(n);
        int prev = 0;
        int curr = jump;

        // Jump through blocks until we find a block that might contain target
        while (curr < n && arr[curr] < target) {
            prev = curr;
            curr += jump;
        }

        // Linear search within the identified block
        for (int i = prev; i < Math.min(curr + 1, n); i++) {
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
     * @param arr Sorted array of integers
     * @param target Value to search for
     * @param blockSize Custom block size (use -1 for default √n)
     * @return Index of target if found, -1 otherwise
     */
    public static int jumpSearchOptimized(int[] arr, int target, int blockSize) {
        int n = arr.length;
        if (n == 0) return -1;

        // Use custom block size or default to √n
        int jump = (blockSize == -1) ? (int) Math.sqrt(n) : blockSize;
        jump = Math.max(1, jump);

        int prev = 0;
        int curr = jump;

        // Jump through blocks
        while (curr < n && arr[curr] < target) {
            prev = curr;
            curr += jump;
        }

        // Linear search in the block
        for (int i = prev; i < Math.min(curr + 1, n); i++) {
            if (arr[i] == target) return i;
            if (arr[i] > target) return -1;
        }

        return -1;
    }

    /**
     * Adaptive jump search that adjusts block size based on data distribution
     * @param arr Sorted array of integers
     * @param target Value to search for
     * @return Index of target if found, -1 otherwise
     */
    public static int adaptiveJumpSearch(int[] arr, int target) {
        int n = arr.length;
        if (n == 0) return -1;

        int initialJump = (int) Math.sqrt(n);
        int jump = initialJump;
        int prev = 0;

        // Adaptive jumping: adjust jump size based on value differences
        while (prev < n && arr[Math.min(prev + jump, n - 1)] < target) {
            int nextIdx = Math.min(prev + jump, n - 1);

            // If we're getting close to target, reduce jump size
            if (nextIdx < n - 1) {
                long valueRange = (long) arr[nextIdx] - arr[prev];
                long targetRange = (long) target - arr[prev];

                // Estimate where target might be and adjust jump
                if (valueRange > 0) {
                    double estimatedPosition = ((double) targetRange / valueRange) * jump;
                    jump = Math.max(1, (int) (estimatedPosition * 1.5));
                }
            }

            prev = nextIdx;
            if (prev >= n - 1) break;
        }

        // Linear search in the final block
        int start = Math.max(0, prev - initialJump);
        for (int i = start; i < Math.min(prev + initialJump, n); i++) {
            if (arr[i] == target) return i;
            if (arr[i] > target) return -1;
        }

        return -1;
    }

    /**
     * Binary search implementation for comparison
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

    public static void main(String[] args) {
        // Test correctness
        int[] testArr = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29};
        System.out.println("Test Array: " + Arrays.toString(testArr));
        System.out.println("Jump Search for 15: Index " + jumpSearch(testArr, 15));
        System.out.println("Jump Search for 20: Index " + jumpSearch(testArr, 20));
        System.out.println("Jump Search for 1: Index " + jumpSearch(testArr, 1));
        System.out.println("Jump Search for 29: Index " + jumpSearch(testArr, 29));

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
                jumpSearch(arr, target);
                binarySearch(arr, target);
            }

            // Jump search
            long jumpStart = System.nanoTime();
            for (int i = 0; i < 10000; i++) {
                jumpSearch(arr, target);
            }
            long jumpTime = System.nanoTime() - jumpStart;

            // Binary search
            long binaryStart = System.nanoTime();
            for (int i = 0; i < 10000; i++) {
                binarySearch(arr, target);
            }
            long binaryTime = System.nanoTime() - binaryStart;

            System.out.printf("\nArray size: %,d%n", size);
            System.out.printf("Jump Search: %.3fms%n", jumpTime / 1_000_000.0);
            System.out.printf("Binary Search: %.3fms%n", binaryTime / 1_000_000.0);
            System.out.printf("Ratio (Jump/Binary): %.2fx%n", (double) jumpTime / binaryTime);
        }

        // Cache-friendly block size analysis
        System.out.println("\n--- Cache-Friendly Block Size Analysis ---");
        int[] largeArr = new int[100000];
        for (int i = 0; i < largeArr.length; i++) {
            largeArr[i] = i * 2;
        }
        int target = largeArr[rand.nextInt(largeArr.length)];

        int[] blockSizes = {32, 64, 128, 256, 512, 1024, (int) Math.sqrt(largeArr.length)};

        for (int blockSize : blockSizes) {
            // Warm-up
            for (int i = 0; i < 100; i++) {
                jumpSearchOptimized(largeArr, target, blockSize);
            }

            long start = System.nanoTime();
            for (int i = 0; i < 10000; i++) {
                jumpSearchOptimized(largeArr, target, blockSize);
            }
            long elapsed = System.nanoTime() - start;
            System.out.printf("Block size %5d: %.3fms%n", blockSize, elapsed / 1_000_000.0);
        }
    }
}
