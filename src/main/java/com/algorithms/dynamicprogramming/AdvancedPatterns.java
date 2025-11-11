package com.algorithms.dynamicprogramming;

import java.util.*;

/**
 * Advanced Dynamic Programming Patterns
 * ======================================
 *
 * A comprehensive guide to advanced DP patterns used in competitive programming
 * and technical interviews.
 *
 * Patterns covered:
 * 1. Digit DP
 * 2. Tree DP
 * 3. Bitmask DP
 * 4. Probability DP
 * 5. Range DP (Interval DP)
 * 6. Profile DP
 *
 * Compile: javac advanced_patterns.java
 * Run: java advanced_patterns
 */
public class advanced_patterns {

    // ========================================================================
    // 1. DIGIT DP
    // ========================================================================

    /**
     * DIGIT DP PATTERN
     * When to use:
     * - Count numbers in range [L, R] with specific digit properties
     * - Numbers with digit sum constraints
     * - Numbers without certain digits
     */
    static class DigitDP {
        /**
         * Count numbers in [left, right] with digit sum divisible by k
         * Time: O(log(right) * k * 2)
         */
        public static long countDivisibleDigitSum(long left, long right, int k) {
            return countUpTo(right, k) - countUpTo(left - 1, k);
        }

        private static long countUpTo(long num, int k) {
            if (num < 0) return 0;

            String numStr = String.valueOf(num);
            int n = numStr.length();
            Map<String, Long> memo = new HashMap<>();

            return dp(0, 0, true, false, numStr, k, memo);
        }

        private static long dp(int pos, int digitSum, boolean tight, boolean started,
                               String digits, int k, Map<String, Long> memo) {
            if (pos == digits.length()) {
                return (started && digitSum % k == 0) ? 1 : 0;
            }

            String key = pos + "," + digitSum + "," + tight + "," + started;
            if (memo.containsKey(key)) {
                return memo.get(key);
            }

            int limit = tight ? (digits.charAt(pos) - '0') : 9;
            long result = 0;

            for (int digit = 0; digit <= limit; digit++) {
                boolean newStarted = started || digit > 0;
                int newSum = newStarted ? (digitSum + digit) % k : 0;
                boolean newTight = tight && (digit == limit);

                result += dp(pos + 1, newSum, newTight, newStarted, digits, k, memo);
            }

            memo.put(key, result);
            return result;
        }

        /**
         * Count numbers without forbidden digit
         */
        public static long countWithoutDigit(long left, long right, int forbidden) {
            return countUpToWithout(right, forbidden) - countUpToWithout(left - 1, forbidden);
        }

        private static long countUpToWithout(long num, int forbidden) {
            if (num < 0) return 0;

            String numStr = String.valueOf(num);
            Map<String, Long> memo = new HashMap<>();

            return dpWithout(0, true, false, numStr, forbidden, memo);
        }

        private static long dpWithout(int pos, boolean tight, boolean started,
                                       String digits, int forbidden, Map<String, Long> memo) {
            if (pos == digits.length()) {
                return started ? 1 : 0;
            }

            String key = pos + "," + tight + "," + started;
            if (memo.containsKey(key)) {
                return memo.get(key);
            }

            int limit = tight ? (digits.charAt(pos) - '0') : 9;
            long result = 0;

            for (int digit = 0; digit <= limit; digit++) {
                if (digit == forbidden && (started || digit > 0)) {
                    continue;
                }

                boolean newStarted = started || digit > 0;
                boolean newTight = tight && (digit == limit);
                result += dpWithout(pos + 1, newTight, newStarted, digits, forbidden, memo);
            }

            memo.put(key, result);
            return result;
        }
    }

    // ========================================================================
    // 2. TREE DP
    // ========================================================================

    /**
     * TREE DP PATTERN
     * When to use:
     * - Find optimal solutions on tree structures
     * - Maximum independent set, diameter, rerooting
     */
    static class TreeDP {
        /**
         * Maximum Independent Set on Tree
         * Time: O(n), Space: O(n)
         */
        public static int maxIndependentSet(int[][] edges, int n) {
            List<List<Integer>> graph = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                graph.add(new ArrayList<>());
            }

            for (int[] edge : edges) {
                graph.get(edge[0]).add(edge[1]);
                graph.get(edge[1]).add(edge[0]);
            }

            int[][] dp = new int[n][2];
            dfsIndependent(0, -1, graph, dp);

            return Math.max(dp[0][0], dp[0][1]);
        }

        private static void dfsIndependent(int node, int parent, List<List<Integer>> graph, int[][] dp) {
            dp[node][0] = 0;
            dp[node][1] = 1;

            for (int child : graph.get(node)) {
                if (child == parent) continue;

                dfsIndependent(child, node, graph, dp);

                dp[node][0] += Math.max(dp[child][0], dp[child][1]);
                dp[node][1] += dp[child][0];
            }
        }

        /**
         * Tree Diameter
         * Time: O(n), Space: O(n)
         */
        public static int treeDiameter(int[][] edges, int n) {
            List<List<Integer>> graph = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                graph.add(new ArrayList<>());
            }

            for (int[] edge : edges) {
                graph.get(edge[0]).add(edge[1]);
                graph.get(edge[1]).add(edge[0]);
            }

            int[] diameter = new int[1];
            dfsDiameter(0, -1, graph, diameter);

            return diameter[0];
        }

        private static int dfsDiameter(int node, int parent, List<List<Integer>> graph, int[] diameter) {
            int[] maxDepths = {0, 0};

            for (int child : graph.get(node)) {
                if (child == parent) continue;

                int childDepth = dfsDiameter(child, node, graph, diameter) + 1;

                if (childDepth > maxDepths[0]) {
                    maxDepths[1] = maxDepths[0];
                    maxDepths[0] = childDepth;
                } else if (childDepth > maxDepths[1]) {
                    maxDepths[1] = childDepth;
                }
            }

            diameter[0] = Math.max(diameter[0], maxDepths[0] + maxDepths[1]);
            return maxDepths[0];
        }
    }

    // ========================================================================
    // 3. BITMASK DP
    // ========================================================================

    /**
     * BITMASK DP PATTERN
     * When to use:
     * - Small sets (n ≤ 20)
     * - TSP, assignment problems, subset problems
     */
    static class BitmaskDP {
        /**
         * Traveling Salesman Problem
         * Time: O(n^2 * 2^n), Space: O(n * 2^n)
         */
        public static int tsp(int[][] dist) {
            int n = dist.length;
            int INF = Integer.MAX_VALUE / 2;

            int[][] dp = new int[1 << n][n];
            for (int[] row : dp) {
                Arrays.fill(row, INF);
            }
            dp[1][0] = 0;

            for (int mask = 0; mask < (1 << n); mask++) {
                for (int last = 0; last < n; last++) {
                    if (dp[mask][last] == INF) continue;
                    if ((mask & (1 << last)) == 0) continue;

                    for (int next = 0; next < n; next++) {
                        if ((mask & (1 << next)) != 0) continue;

                        int newMask = mask | (1 << next);
                        dp[newMask][next] = Math.min(
                            dp[newMask][next],
                            dp[mask][last] + dist[last][next]
                        );
                    }
                }
            }

            int fullMask = (1 << n) - 1;
            int result = INF;
            for (int i = 0; i < n; i++) {
                result = Math.min(result, dp[fullMask][i]);
            }

            return result;
        }

        /**
         * Assignment Problem
         * Time: O(n * 2^n), Space: O(2^n)
         */
        public static int assignmentProblem(int[][] cost) {
            int n = cost.length;
            int INF = Integer.MAX_VALUE / 2;

            int[] dp = new int[1 << n];
            Arrays.fill(dp, INF);
            dp[0] = 0;

            for (int mask = 0; mask < (1 << n); mask++) {
                if (dp[mask] == INF) continue;

                int person = Integer.bitCount(mask);
                if (person >= n) continue;

                for (int task = 0; task < n; task++) {
                    if ((mask & (1 << task)) != 0) continue;

                    int newMask = mask | (1 << task);
                    dp[newMask] = Math.min(dp[newMask], dp[mask] + cost[person][task]);
                }
            }

            return dp[(1 << n) - 1];
        }

        /**
         * Optimized SOS DP
         * Time: O(n * 2^n), Space: O(2^n)
         */
        public static int[] sosDP(int[] arr) {
            int n = arr.length;
            int[] dp = arr.clone();

            for (int i = 0; i < n; i++) {
                for (int mask = 0; mask < (1 << n); mask++) {
                    if ((mask & (1 << i)) != 0) {
                        dp[mask] += dp[mask ^ (1 << i)];
                    }
                }
            }

            return dp;
        }
    }

    // ========================================================================
    // 4. PROBABILITY DP
    // ========================================================================

    /**
     * PROBABILITY DP PATTERN
     * When to use:
     * - Expected value problems
     * - Probability calculations with states
     */
    static class ProbabilityDP {
        /**
         * Expected flips for n consecutive heads
         * Time: O(n), Space: O(n)
         */
        public static double expectedConsecutiveHeads(int n) {
            double[] dp = new double[n + 1];

            for (int i = n - 1; i >= 0; i--) {
                dp[i] = 2 + dp[i + 1];
            }

            return dp[0];
        }

        /**
         * Expected rolls to see all n faces (Coupon Collector)
         */
        public static double diceExpectedValue(int n, int faces) {
            double expected = 0.0;
            for (int k = 0; k < n; k++) {
                expected += (double) faces / (faces - k);
            }
            return expected;
        }

        /**
         * 1D Random Walk
         */
        public static double randomWalk1D(int start, int target, int maxPos) {
            if (start <= 0 || start >= maxPos) return 0.0;
            if (start == target) return 1.0;

            double[] dp = new double[maxPos];
            dp[target] = 1.0;

            for (int i = 0; i < target; i++) {
                dp[i] = (double) i / target;
            }

            for (int i = target + 1; i < maxPos; i++) {
                dp[i] = (double) (maxPos - i) / (maxPos - target);
            }

            return dp[start];
        }
    }

    // ========================================================================
    // 5. RANGE DP
    // ========================================================================

    /**
     * RANGE DP PATTERN
     * When to use:
     * - Problems on contiguous subarrays
     * - Merging intervals optimally
     */
    static class RangeDP {
        /**
         * Merge Stones (K-merge variant)
         * Time: O(n^3 / k), Space: O(n^2)
         */
        public static int mergeStones(int[] stones, int k) {
            int n = stones.length;

            if ((n - 1) % (k - 1) != 0) {
                return -1;
            }

            int[] prefix = new int[n + 1];
            for (int i = 0; i < n; i++) {
                prefix[i + 1] = prefix[i] + stones[i];
            }

            int INF = Integer.MAX_VALUE / 2;
            int[][] dp = new int[n][n];
            for (int[] row : dp) {
                Arrays.fill(row, INF);
            }

            for (int i = 0; i < n; i++) {
                dp[i][i] = 0;
            }

            for (int length = 2; length <= n; length++) {
                for (int i = 0; i <= n - length; i++) {
                    int j = i + length - 1;

                    for (int mid = i; mid < j; mid += k - 1) {
                        dp[i][j] = Math.min(dp[i][j], dp[i][mid] + dp[mid + 1][j]);
                    }

                    if ((j - i) % (k - 1) == 0) {
                        dp[i][j] += prefix[j + 1] - prefix[i];
                    }
                }
            }

            return dp[0][n - 1] != INF ? dp[0][n - 1] : -1;
        }

        /**
         * Burst Balloons
         * Time: O(n^3), Space: O(n^2)
         */
        public static int burstBalloons(int[] nums) {
            int n = nums.length;
            int[] balloons = new int[n + 2];
            balloons[0] = 1;
            balloons[n + 1] = 1;
            System.arraycopy(nums, 0, balloons, 1, n);

            int len = balloons.length;
            int[][] dp = new int[len][len];

            for (int length = 2; length < len; length++) {
                for (int i = 0; i < len - length; i++) {
                    int j = i + length;

                    for (int k = i + 1; k < j; k++) {
                        int coins = balloons[i] * balloons[k] * balloons[j];
                        dp[i][j] = Math.max(dp[i][j], dp[i][k] + dp[k][j] + coins);
                    }
                }
            }

            return dp[0][len - 1];
        }
    }

    // ========================================================================
    // 6. PROFILE DP
    // ========================================================================

    /**
     * PROFILE DP PATTERN
     * When to use:
     * - Grid tiling problems
     * - Problems where current row depends on previous row
     */
    static class ProfileDP {
        /**
         * Domino Tiling (2×n grid)
         * Time: O(n), Space: O(1)
         */
        public static long dominoTiling2xN(int n) {
            long MOD = 1000000007;

            long[] dp = new long[4];
            dp[0] = 1;

            for (int col = 0; col < n; col++) {
                long[] newDp = new long[4];

                for (int profile = 0; profile < 4; profile++) {
                    if (dp[profile] == 0) continue;

                    fill(0, profile, 0, dp, newDp, MOD);
                }

                dp = newDp;
            }

            return dp[0];
        }

        private static void fill(int pos, int curr, int next, long[] dp, long[] newDp, long MOD) {
            if (pos == 2) {
                newDp[next] = (newDp[next] + dp[curr]) % MOD;
                return;
            }

            if ((curr & (1 << pos)) != 0) {
                fill(pos + 1, curr, next, dp, newDp, MOD);
            } else {
                // Vertical
                fill(pos + 1, curr | (1 << pos), next | (1 << pos), dp, newDp, MOD);

                // Horizontal
                if (pos + 1 < 2 && (curr & (1 << (pos + 1))) == 0) {
                    fill(pos + 2, curr | (1 << pos) | (1 << (pos + 1)), next, dp, newDp, MOD);
                }
            }
        }
    }

    // ========================================================================
    // MAIN - EXAMPLE USAGE
    // ========================================================================

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("ADVANCED DYNAMIC PROGRAMMING PATTERNS - EXAMPLES");
        System.out.println("=".repeat(70));

        // Digit DP
        System.out.println("\n1. DIGIT DP:");
        System.out.println("   Count numbers in [1, 100] with digit sum divisible by 3:");
        System.out.println("   Result: " + DigitDP.countDivisibleDigitSum(1, 100, 3));

        System.out.println("   Count numbers in [1, 100] without digit 5:");
        System.out.println("   Result: " + DigitDP.countWithoutDigit(1, 100, 5));

        // Tree DP
        System.out.println("\n2. TREE DP:");
        int[][] edges = {{0, 1}, {0, 2}, {1, 3}, {1, 4}};
        int n = 5;
        System.out.println("   Tree edges: " + Arrays.deepToString(edges));
        System.out.println("   Maximum independent set: " + TreeDP.maxIndependentSet(edges, n));
        System.out.println("   Tree diameter: " + TreeDP.treeDiameter(edges, n));

        // Bitmask DP
        System.out.println("\n3. BITMASK DP:");
        int[][] dist = {
            {0, 10, 15, 20},
            {10, 0, 35, 25},
            {15, 35, 0, 30},
            {20, 25, 30, 0}
        };
        System.out.println("   TSP distance matrix:");
        for (int[] row : dist) {
            System.out.println("   " + Arrays.toString(row));
        }
        System.out.println("   Minimum TSP cost: " + BitmaskDP.tsp(dist));

        int[][] cost = {
            {9, 2, 7, 8},
            {6, 4, 3, 7},
            {5, 8, 1, 8},
            {7, 6, 9, 4}
        };
        System.out.println("\n   Assignment problem cost matrix:");
        for (int[] row : cost) {
            System.out.println("   " + Arrays.toString(row));
        }
        System.out.println("   Minimum assignment cost: " + BitmaskDP.assignmentProblem(cost));

        // Probability DP
        System.out.println("\n4. PROBABILITY DP:");
        int numHeads = 3;
        System.out.printf("   Expected flips for %d consecutive heads: %.2f%n",
            numHeads, ProbabilityDP.expectedConsecutiveHeads(numHeads));
        System.out.printf("   Expected rolls to see all 6 faces: %.2f%n",
            ProbabilityDP.diceExpectedValue(6, 6));

        // Range DP
        System.out.println("\n5. RANGE DP:");
        int[] stones = {3, 2, 4, 1};
        int k = 2;
        System.out.println("   Stones: " + Arrays.toString(stones) + ", K: " + k);
        System.out.println("   Minimum cost to merge: " + RangeDP.mergeStones(stones, k));

        int[] balloons = {3, 1, 5, 8};
        System.out.println("   Balloons: " + Arrays.toString(balloons));
        System.out.println("   Maximum coins: " + RangeDP.burstBalloons(balloons));

        // Profile DP
        System.out.println("\n6. PROFILE DP:");
        int gridSize = 5;
        System.out.println("   Domino tiling 2×" + gridSize + ":");
        System.out.println("   Number of ways: " + ProfileDP.dominoTiling2xN(gridSize));

        System.out.println("\n" + "=".repeat(70));
    }
}

