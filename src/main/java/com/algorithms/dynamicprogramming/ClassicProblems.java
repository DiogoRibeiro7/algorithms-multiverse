package com.algorithms.dynamicprogramming;

import java.util.*;

/**
 * Dynamic Programming Classic Problems
 * =====================================
 *
 * Comprehensive implementations of classic DP problems with multiple
 * solution approaches: naive recursive, memoized (top-down),
 * tabulated (bottom-up), and space-optimized versions.
 *
 * @author Algorithms Multiverse
 */
public class classic_problems {

    // ========================================================================
    // 1. LONGEST COMMON SUBSEQUENCE (LCS)
    // ========================================================================

    /**
     * Problem: Find the length of the longest subsequence common to two sequences.
     *
     * Real-world applications:
     * - Version control systems (diff algorithms)
     * - DNA sequence analysis
     * - Plagiarism detection
     */

    /**
     * Naive recursive solution.
     * Time: O(2^(m+n))
     * Space: O(m+n)
     */
    public static int lcsNaive(String s1, String s2) {
        return lcsNaiveHelper(s1, s2, 0, 0);
    }

    private static int lcsNaiveHelper(String s1, String s2, int i, int j) {
        if (i == s1.length() || j == s2.length()) {
            return 0;
        }

        if (s1.charAt(i) == s2.charAt(j)) {
            return 1 + lcsNaiveHelper(s1, s2, i + 1, j + 1);
        } else {
            return Math.max(
                lcsNaiveHelper(s1, s2, i + 1, j),
                lcsNaiveHelper(s1, s2, i, j + 1)
            );
        }
    }

    /**
     * Memoized solution.
     * Time: O(m*n)
     * Space: O(m*n)
     */
    public static int lcsMemoized(String s1, String s2) {
        Map<String, Integer> memo = new HashMap<>();
        return lcsMemoizedHelper(s1, s2, 0, 0, memo);
    }

    private static int lcsMemoizedHelper(String s1, String s2, int i, int j,
                                          Map<String, Integer> memo) {
        if (i == s1.length() || j == s2.length()) {
            return 0;
        }

        String key = i + "," + j;
        if (memo.containsKey(key)) {
            return memo.get(key);
        }

        int result;
        if (s1.charAt(i) == s2.charAt(j)) {
            result = 1 + lcsMemoizedHelper(s1, s2, i + 1, j + 1, memo);
        } else {
            result = Math.max(
                lcsMemoizedHelper(s1, s2, i + 1, j, memo),
                lcsMemoizedHelper(s1, s2, i, j + 1, memo)
            );
        }

        memo.put(key, result);
        return result;
    }

    /**
     * Tabulated solution.
     * Time: O(m*n)
     * Space: O(m*n)
     */
    public static int lcsTabulated(String s1, String s2) {
        int m = s1.length();
        int n = s2.length();
        int[][] dp = new int[m + 1][n + 1];

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                    dp[i][j] = 1 + dp[i - 1][j - 1];
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }

        return dp[m][n];
    }

    /**
     * Space-optimized solution.
     * Time: O(m*n)
     * Space: O(min(m, n))
     */
    public static int lcsSpaceOptimized(String s1, String s2) {
        if (s1.length() < s2.length()) {
            String temp = s1;
            s1 = s2;
            s2 = temp;
        }

        int m = s1.length();
        int n = s2.length();
        int[] prev = new int[n + 1];
        int[] curr = new int[n + 1];

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                    curr[j] = 1 + prev[j - 1];
                } else {
                    curr[j] = Math.max(prev[j], curr[j - 1]);
                }
            }
            int[] temp = prev;
            prev = curr;
            curr = temp;
        }

        return prev[n];
    }

    // ========================================================================
    // 2. LONGEST INCREASING SUBSEQUENCE (LIS)
    // ========================================================================

    /**
     * Problem: Find the length of the longest strictly increasing subsequence.
     *
     * Real-world applications:
     * - Stock market trend analysis
     * - Task scheduling
     */

    /**
     * Naive recursive solution.
     * Time: O(2^n)
     * Space: O(n)
     */
    public static int lisNaive(int[] arr) {
        return lisNaiveHelper(arr, 0, Integer.MIN_VALUE);
    }

    private static int lisNaiveHelper(int[] arr, int idx, int prev) {
        if (idx == arr.length) {
            return 0;
        }

        int exclude = lisNaiveHelper(arr, idx + 1, prev);
        int include = 0;
        if (arr[idx] > prev) {
            include = 1 + lisNaiveHelper(arr, idx + 1, arr[idx]);
        }

        return Math.max(exclude, include);
    }

    /**
     * Memoized solution.
     * Time: O(n^2)
     * Space: O(n^2)
     */
    public static int lisMemoized(int[] arr) {
        Map<String, Integer> memo = new HashMap<>();
        return lisMemoizedHelper(arr, 0, -1, memo);
    }

    private static int lisMemoizedHelper(int[] arr, int idx, int prevIdx,
                                          Map<String, Integer> memo) {
        if (idx == arr.length) {
            return 0;
        }

        String key = idx + "," + prevIdx;
        if (memo.containsKey(key)) {
            return memo.get(key);
        }

        int exclude = lisMemoizedHelper(arr, idx + 1, prevIdx, memo);
        int include = 0;
        if (prevIdx == -1 || arr[idx] > arr[prevIdx]) {
            include = 1 + lisMemoizedHelper(arr, idx + 1, idx, memo);
        }

        int result = Math.max(exclude, include);
        memo.put(key, result);
        return result;
    }

    /**
     * Tabulated O(n^2) solution.
     * Time: O(n^2)
     * Space: O(n)
     */
    public static int lisTabulated(int[] arr) {
        if (arr.length == 0) return 0;

        int n = arr.length;
        int[] dp = new int[n];
        Arrays.fill(dp, 1);

        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (arr[j] < arr[i]) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                }
            }
        }

        return Arrays.stream(dp).max().getAsInt();
    }

    /**
     * Optimized solution using binary search.
     * Time: O(n log n)
     * Space: O(n)
     */
    public static int lisOptimized(int[] arr) {
        if (arr.length == 0) return 0;

        List<Integer> tails = new ArrayList<>();

        for (int num : arr) {
            int pos = Collections.binarySearch(tails, num);
            if (pos < 0) {
                pos = -(pos + 1);
            }

            if (pos == tails.size()) {
                tails.add(num);
            } else {
                tails.set(pos, num);
            }
        }

        return tails.size();
    }

    // ========================================================================
    // 3. EDIT DISTANCE (LEVENSHTEIN DISTANCE)
    // ========================================================================

    /**
     * Problem: Minimum operations (insert, delete, replace) to convert s1 to s2.
     *
     * Real-world applications:
     * - Spell checkers
     * - DNA sequence alignment
     * - Autocorrect systems
     */

    /**
     * Naive recursive solution.
     * Time: O(3^max(m,n))
     * Space: O(max(m, n))
     */
    public static int editDistanceNaive(String s1, String s2) {
        return editDistanceNaiveHelper(s1, s2, s1.length(), s2.length());
    }

    private static int editDistanceNaiveHelper(String s1, String s2, int i, int j) {
        if (i == 0) return j;
        if (j == 0) return i;

        if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
            return editDistanceNaiveHelper(s1, s2, i - 1, j - 1);
        }

        return 1 + Math.min(
            Math.min(
                editDistanceNaiveHelper(s1, s2, i, j - 1),     // insert
                editDistanceNaiveHelper(s1, s2, i - 1, j)      // delete
            ),
            editDistanceNaiveHelper(s1, s2, i - 1, j - 1)      // replace
        );
    }

    /**
     * Memoized solution.
     * Time: O(m*n)
     * Space: O(m*n)
     */
    public static int editDistanceMemoized(String s1, String s2) {
        Map<String, Integer> memo = new HashMap<>();
        return editDistanceMemoizedHelper(s1, s2, s1.length(), s2.length(), memo);
    }

    private static int editDistanceMemoizedHelper(String s1, String s2, int i, int j,
                                                   Map<String, Integer> memo) {
        if (i == 0) return j;
        if (j == 0) return i;

        String key = i + "," + j;
        if (memo.containsKey(key)) {
            return memo.get(key);
        }

        int result;
        if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
            result = editDistanceMemoizedHelper(s1, s2, i - 1, j - 1, memo);
        } else {
            result = 1 + Math.min(
                Math.min(
                    editDistanceMemoizedHelper(s1, s2, i, j - 1, memo),
                    editDistanceMemoizedHelper(s1, s2, i - 1, j, memo)
                ),
                editDistanceMemoizedHelper(s1, s2, i - 1, j - 1, memo)
            );
        }

        memo.put(key, result);
        return result;
    }

    /**
     * Tabulated solution.
     * Time: O(m*n)
     * Space: O(m*n)
     */
    public static int editDistanceTabulated(String s1, String s2) {
        int m = s1.length();
        int n = s2.length();
        int[][] dp = new int[m + 1][n + 1];

        for (int i = 0; i <= m; i++) dp[i][0] = i;
        for (int j = 0; j <= n; j++) dp[0][j] = j;

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(
                        Math.min(dp[i][j - 1], dp[i - 1][j]),
                        dp[i - 1][j - 1]
                    );
                }
            }
        }

        return dp[m][n];
    }

    /**
     * Space-optimized solution.
     * Time: O(m*n)
     * Space: O(min(m, n))
     */
    public static int editDistanceSpaceOptimized(String s1, String s2) {
        if (s1.length() < s2.length()) {
            String temp = s1;
            s1 = s2;
            s2 = temp;
        }

        int n = s2.length();
        int[] prev = new int[n + 1];
        int[] curr = new int[n + 1];

        for (int j = 0; j <= n; j++) {
            prev[j] = j;
        }

        for (int i = 1; i <= s1.length(); i++) {
            curr[0] = i;
            for (int j = 1; j <= n; j++) {
                if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                    curr[j] = prev[j - 1];
                } else {
                    curr[j] = 1 + Math.min(
                        Math.min(curr[j - 1], prev[j]),
                        prev[j - 1]
                    );
                }
            }
            int[] temp = prev;
            prev = curr;
            curr = temp;
        }

        return prev[n];
    }

    // ========================================================================
    // 4. COIN CHANGE PROBLEM
    // ========================================================================

    /**
     * Problem: Find minimum coins needed or count ways to make change.
     *
     * Real-world applications:
     * - Vending machines
     * - Currency exchange
     */

    /**
     * Naive recursive - minimum coins.
     * Time: O(amount^len(coins))
     * Space: O(amount)
     */
    public static int coinChangeMinNaive(int[] coins, int amount) {
        int result = coinChangeMinNaiveHelper(coins, amount);
        return result == Integer.MAX_VALUE ? -1 : result;
    }

    private static int coinChangeMinNaiveHelper(int[] coins, int remaining) {
        if (remaining == 0) return 0;
        if (remaining < 0) return Integer.MAX_VALUE;

        int minCoins = Integer.MAX_VALUE;
        for (int coin : coins) {
            int result = coinChangeMinNaiveHelper(coins, remaining - coin);
            if (result != Integer.MAX_VALUE) {
                minCoins = Math.min(minCoins, result + 1);
            }
        }

        return minCoins;
    }

    /**
     * Memoized - minimum coins.
     * Time: O(amount * len(coins))
     * Space: O(amount)
     */
    public static int coinChangeMinMemoized(int[] coins, int amount) {
        Map<Integer, Integer> memo = new HashMap<>();
        int result = coinChangeMinMemoizedHelper(coins, amount, memo);
        return result == Integer.MAX_VALUE ? -1 : result;
    }

    private static int coinChangeMinMemoizedHelper(int[] coins, int remaining,
                                                    Map<Integer, Integer> memo) {
        if (remaining == 0) return 0;
        if (remaining < 0) return Integer.MAX_VALUE;

        if (memo.containsKey(remaining)) {
            return memo.get(remaining);
        }

        int minCoins = Integer.MAX_VALUE;
        for (int coin : coins) {
            int result = coinChangeMinMemoizedHelper(coins, remaining - coin, memo);
            if (result != Integer.MAX_VALUE) {
                minCoins = Math.min(minCoins, result + 1);
            }
        }

        memo.put(remaining, minCoins);
        return minCoins;
    }

    /**
     * Tabulated - minimum coins.
     * Time: O(amount * len(coins))
     * Space: O(amount)
     */
    public static int coinChangeMinTabulated(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, Integer.MAX_VALUE);
        dp[0] = 0;

        for (int i = 1; i <= amount; i++) {
            for (int coin : coins) {
                if (coin <= i && dp[i - coin] != Integer.MAX_VALUE) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
                }
            }
        }

        return dp[amount] == Integer.MAX_VALUE ? -1 : dp[amount];
    }

    /**
     * Count number of ways to make change.
     * Time: O(amount * len(coins))
     * Space: O(amount)
     */
    public static int coinChangeWaysTabulated(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        dp[0] = 1;

        for (int coin : coins) {
            for (int i = coin; i <= amount; i++) {
                dp[i] += dp[i - coin];
            }
        }

        return dp[amount];
    }

    // ========================================================================
    // 5. KNAPSACK PROBLEMS
    // ========================================================================

    /**
     * Problem: Maximize value within weight capacity.
     *
     * Real-world applications:
     * - Resource allocation
     * - Portfolio optimization
     */

    /**
     * 0/1 Knapsack - Naive recursive.
     * Time: O(2^n)
     * Space: O(n)
     */
    public static int knapsack01Naive(int[] weights, int[] values, int capacity) {
        return knapsack01NaiveHelper(weights, values, capacity, 0);
    }

    private static int knapsack01NaiveHelper(int[] weights, int[] values,
                                              int capacity, int idx) {
        if (idx == weights.length || capacity == 0) {
            return 0;
        }

        int skip = knapsack01NaiveHelper(weights, values, capacity, idx + 1);
        int take = 0;
        if (weights[idx] <= capacity) {
            take = values[idx] + knapsack01NaiveHelper(weights, values,
                capacity - weights[idx], idx + 1);
        }

        return Math.max(skip, take);
    }

    /**
     * 0/1 Knapsack - Memoized.
     * Time: O(n * capacity)
     * Space: O(n * capacity)
     */
    public static int knapsack01Memoized(int[] weights, int[] values, int capacity) {
        Map<String, Integer> memo = new HashMap<>();
        return knapsack01MemoizedHelper(weights, values, capacity, 0, memo);
    }

    private static int knapsack01MemoizedHelper(int[] weights, int[] values,
                                                 int remaining, int idx,
                                                 Map<String, Integer> memo) {
        if (idx == weights.length || remaining == 0) {
            return 0;
        }

        String key = idx + "," + remaining;
        if (memo.containsKey(key)) {
            return memo.get(key);
        }

        int skip = knapsack01MemoizedHelper(weights, values, remaining, idx + 1, memo);
        int take = 0;
        if (weights[idx] <= remaining) {
            take = values[idx] + knapsack01MemoizedHelper(weights, values,
                remaining - weights[idx], idx + 1, memo);
        }

        int result = Math.max(skip, take);
        memo.put(key, result);
        return result;
    }

    /**
     * 0/1 Knapsack - Tabulated.
     * Time: O(n * capacity)
     * Space: O(n * capacity)
     */
    public static int knapsack01Tabulated(int[] weights, int[] values, int capacity) {
        int n = weights.length;
        int[][] dp = new int[n + 1][capacity + 1];

        for (int i = 1; i <= n; i++) {
            for (int w = 0; w <= capacity; w++) {
                dp[i][w] = dp[i - 1][w];
                if (weights[i - 1] <= w) {
                    dp[i][w] = Math.max(
                        dp[i][w],
                        dp[i - 1][w - weights[i - 1]] + values[i - 1]
                    );
                }
            }
        }

        return dp[n][capacity];
    }

    /**
     * 0/1 Knapsack - Space optimized.
     * Time: O(n * capacity)
     * Space: O(capacity)
     */
    public static int knapsack01SpaceOptimized(int[] weights, int[] values, int capacity) {
        int[] dp = new int[capacity + 1];

        for (int i = 0; i < weights.length; i++) {
            for (int w = capacity; w >= weights[i]; w--) {
                dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
            }
        }

        return dp[capacity];
    }

    /**
     * Unbounded Knapsack.
     * Time: O(n * capacity)
     * Space: O(capacity)
     */
    public static int knapsackUnboundedTabulated(int[] weights, int[] values, int capacity) {
        int[] dp = new int[capacity + 1];

        for (int w = 1; w <= capacity; w++) {
            for (int i = 0; i < weights.length; i++) {
                if (weights[i] <= w) {
                    dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
                }
            }
        }

        return dp[capacity];
    }

    // ========================================================================
    // 6. MATRIX CHAIN MULTIPLICATION
    // ========================================================================

    /**
     * Problem: Find optimal parenthesization to minimize multiplications.
     *
     * Real-world applications:
     * - Compiler optimization
     * - Database query optimization
     */

    /**
     * Naive recursive solution.
     * Time: O(2^n)
     * Space: O(n)
     */
    public static int matrixChainNaive(int[] dims) {
        return matrixChainNaiveHelper(dims, 1, dims.length - 1);
    }

    private static int matrixChainNaiveHelper(int[] dims, int i, int j) {
        if (i == j) return 0;

        int minCost = Integer.MAX_VALUE;
        for (int k = i; k < j; k++) {
            int cost =
                matrixChainNaiveHelper(dims, i, k) +
                matrixChainNaiveHelper(dims, k + 1, j) +
                dims[i - 1] * dims[k] * dims[j];
            minCost = Math.min(minCost, cost);
        }

        return minCost;
    }

    /**
     * Memoized solution.
     * Time: O(n^3)
     * Space: O(n^2)
     */
    public static int matrixChainMemoized(int[] dims) {
        Map<String, Integer> memo = new HashMap<>();
        return matrixChainMemoizedHelper(dims, 1, dims.length - 1, memo);
    }

    private static int matrixChainMemoizedHelper(int[] dims, int i, int j,
                                                  Map<String, Integer> memo) {
        if (i == j) return 0;

        String key = i + "," + j;
        if (memo.containsKey(key)) {
            return memo.get(key);
        }

        int minCost = Integer.MAX_VALUE;
        for (int k = i; k < j; k++) {
            int cost =
                matrixChainMemoizedHelper(dims, i, k, memo) +
                matrixChainMemoizedHelper(dims, k + 1, j, memo) +
                dims[i - 1] * dims[k] * dims[j];
            minCost = Math.min(minCost, cost);
        }

        memo.put(key, minCost);
        return minCost;
    }

    /**
     * Tabulated solution.
     * Time: O(n^3)
     * Space: O(n^2)
     */
    public static int matrixChainTabulated(int[] dims) {
        int n = dims.length;
        int[][] dp = new int[n][n];

        for (int length = 2; length < n; length++) {
            for (int i = 1; i < n - length + 1; i++) {
                int j = i + length - 1;
                dp[i][j] = Integer.MAX_VALUE;

                for (int k = i; k < j; k++) {
                    int cost =
                        dp[i][k] +
                        dp[k + 1][j] +
                        dims[i - 1] * dims[k] * dims[j];
                    dp[i][j] = Math.min(dp[i][j], cost);
                }
            }
        }

        return dp[1][n - 1];
    }

    // ========================================================================
    // 7. PALINDROME PROBLEMS
    // ========================================================================

    /**
     * Real-world applications:
     * - DNA sequence analysis
     * - Text processing
     */

    /**
     * Longest palindromic subsequence - Tabulated.
     * Time: O(n^2)
     * Space: O(n^2)
     */
    public static int longestPalindromeSubsequenceTabulated(String s) {
        int n = s.length();
        int[][] dp = new int[n][n];

        for (int i = 0; i < n; i++) {
            dp[i][i] = 1;
        }

        for (int length = 2; length <= n; length++) {
            for (int i = 0; i < n - length + 1; i++) {
                int j = i + length - 1;

                if (s.charAt(i) == s.charAt(j)) {
                    dp[i][j] = 2 + (i + 1 <= j - 1 ? dp[i + 1][j - 1] : 0);
                } else {
                    dp[i][j] = Math.max(dp[i + 1][j], dp[i][j - 1]);
                }
            }
        }

        return dp[0][n - 1];
    }

    /**
     * Count palindromic substrings.
     * Time: O(n^2)
     * Space: O(1)
     */
    public static int countPalindromicSubstrings(String s) {
        int total = 0;
        for (int i = 0; i < s.length(); i++) {
            total += expandAroundCenter(s, i, i);      // odd length
            total += expandAroundCenter(s, i, i + 1);  // even length
        }
        return total;
    }

    private static int expandAroundCenter(String s, int left, int right) {
        int count = 0;
        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
            count++;
            left--;
            right++;
        }
        return count;
    }

    /**
     * Minimum insertions to make palindrome.
     * Time: O(n^2)
     * Space: O(n^2)
     */
    public static int minInsertionsPalindrome(String s) {
        return s.length() - longestPalindromeSubsequenceTabulated(s);
    }

    /**
     * Minimum cuts for palindrome partitioning.
     * Time: O(n^2)
     * Space: O(n^2)
     */
    public static int palindromePartitioningMinCuts(String s) {
        int n = s.length();

        boolean[][] isPalindrome = new boolean[n][n];
        for (int i = 0; i < n; i++) {
            isPalindrome[i][i] = true;
        }

        for (int length = 2; length <= n; length++) {
            for (int i = 0; i < n - length + 1; i++) {
                int j = i + length - 1;
                if (s.charAt(i) == s.charAt(j)) {
                    isPalindrome[i][j] = (length == 2) || isPalindrome[i + 1][j - 1];
                }
            }
        }

        int[] dp = new int[n];
        Arrays.fill(dp, Integer.MAX_VALUE);

        for (int i = 0; i < n; i++) {
            if (isPalindrome[0][i]) {
                dp[i] = 0;
            } else {
                for (int j = 0; j < i; j++) {
                    if (isPalindrome[j + 1][i]) {
                        dp[i] = Math.min(dp[i], dp[j] + 1);
                    }
                }
            }
        }

        return dp[n - 1];
    }

    // ========================================================================
    // 8. MAXIMUM SUBARRAY SUM (KADANE'S ALGORITHM)
    // ========================================================================

    /**
     * Problem: Find contiguous subarray with maximum sum.
     *
     * Real-world applications:
     * - Stock market analysis
     * - Signal processing
     */

    /**
     * Naive solution - check all subarrays.
     * Time: O(n^2)
     * Space: O(1)
     */
    public static int maxSubarrayNaive(int[] arr) {
        if (arr.length == 0) return 0;

        int maxSum = Integer.MIN_VALUE;
        for (int i = 0; i < arr.length; i++) {
            int currentSum = 0;
            for (int j = i; j < arr.length; j++) {
                currentSum += arr[j];
                maxSum = Math.max(maxSum, currentSum);
            }
        }

        return maxSum;
    }

    /**
     * Kadane's Algorithm - optimal.
     * Time: O(n)
     * Space: O(1)
     */
    public static int maxSubarrayKadane(int[] arr) {
        if (arr.length == 0) return 0;

        int maxSum = arr[0];
        int currentSum = arr[0];

        for (int i = 1; i < arr.length; i++) {
            currentSum = Math.max(arr[i], currentSum + arr[i]);
            maxSum = Math.max(maxSum, currentSum);
        }

        return maxSum;
    }

    /**
     * Kadane's with indices.
     */
    public static class SubarrayResult {
        public int maxSum;
        public int start;
        public int end;

        public SubarrayResult(int maxSum, int start, int end) {
            this.maxSum = maxSum;
            this.start = start;
            this.end = end;
        }
    }

    public static SubarrayResult maxSubarrayWithIndices(int[] arr) {
        if (arr.length == 0) return new SubarrayResult(0, -1, -1);

        int maxSum = arr[0];
        int currentSum = arr[0];
        int start = 0, end = 0, tempStart = 0;

        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > currentSum + arr[i]) {
                currentSum = arr[i];
                tempStart = i;
            } else {
                currentSum = currentSum + arr[i];
            }

            if (currentSum > maxSum) {
                maxSum = currentSum;
                start = tempStart;
                end = i;
            }
        }

        return new SubarrayResult(maxSum, start, end);
    }

    /**
     * Maximum subarray in circular array.
     * Time: O(n)
     * Space: O(1)
     */
    public static int maxSubarrayCircular(int[] arr) {
        if (arr.length == 0) return 0;

        int maxNormal = maxSubarrayKadane(arr);
        if (maxNormal < 0) return maxNormal;

        int totalSum = 0;
        for (int num : arr) {
            totalSum += num;
        }

        int minSum = kadaneMin(arr);
        int maxCircular = totalSum - minSum;

        return Math.max(maxNormal, maxCircular);
    }

    private static int kadaneMin(int[] arr) {
        int minSum = arr[0];
        int currentSum = arr[0];
        for (int i = 1; i < arr.length; i++) {
            currentSum = Math.min(arr[i], currentSum + arr[i]);
            minSum = Math.min(minSum, currentSum);
        }
        return minSum;
    }

    // ========================================================================
    // MAIN - EXAMPLE USAGE AND TESTING
    // ========================================================================

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("DYNAMIC PROGRAMMING CLASSIC PROBLEMS - EXAMPLES");
        System.out.println("=".repeat(70));

        // LCS Examples
        System.out.println("\n1. Longest Common Subsequence:");
        String s1 = "ABCDGH", s2 = "AEDFHR";
        System.out.println("   Strings: '" + s1 + "', '" + s2 + "'");
        System.out.println("   Naive: " + lcsNaive(s1, s2));
        System.out.println("   Memoized: " + lcsMemoized(s1, s2));
        System.out.println("   Tabulated: " + lcsTabulated(s1, s2));
        System.out.println("   Space-optimized: " + lcsSpaceOptimized(s1, s2));

        // LIS Examples
        System.out.println("\n2. Longest Increasing Subsequence:");
        int[] arr1 = {10, 9, 2, 5, 3, 7, 101, 18};
        System.out.println("   Array: " + Arrays.toString(arr1));
        System.out.println("   Naive: " + lisNaive(arr1));
        System.out.println("   Memoized: " + lisMemoized(arr1));
        System.out.println("   Tabulated O(n^2): " + lisTabulated(arr1));
        System.out.println("   Optimized O(n log n): " + lisOptimized(arr1));

        // Edit Distance
        System.out.println("\n3. Edit Distance:");
        String str1 = "kitten", str2 = "sitting";
        System.out.println("   Strings: '" + str1 + "', '" + str2 + "'");
        System.out.println("   Naive: " + editDistanceNaive(str1, str2));
        System.out.println("   Memoized: " + editDistanceMemoized(str1, str2));
        System.out.println("   Tabulated: " + editDistanceTabulated(str1, str2));
        System.out.println("   Space-optimized: " + editDistanceSpaceOptimized(str1, str2));

        // Coin Change
        System.out.println("\n4. Coin Change:");
        int[] coins = {1, 2, 5};
        int amount = 11;
        System.out.println("   Coins: " + Arrays.toString(coins) + ", Amount: " + amount);
        System.out.println("   Min coins (naive): " + coinChangeMinNaive(coins, amount));
        System.out.println("   Min coins (memoized): " + coinChangeMinMemoized(coins, amount));
        System.out.println("   Min coins (tabulated): " + coinChangeMinTabulated(coins, amount));
        System.out.println("   Ways to make change: " + coinChangeWaysTabulated(coins, amount));

        // Knapsack
        System.out.println("\n5. Knapsack Problem:");
        int[] weights = {1, 3, 4, 5};
        int[] values = {1, 4, 5, 7};
        int capacity = 7;
        System.out.println("   Weights: " + Arrays.toString(weights) +
                         ", Values: " + Arrays.toString(values) +
                         ", Capacity: " + capacity);
        System.out.println("   0/1 Naive: " + knapsack01Naive(weights, values, capacity));
        System.out.println("   0/1 Memoized: " + knapsack01Memoized(weights, values, capacity));
        System.out.println("   0/1 Tabulated: " + knapsack01Tabulated(weights, values, capacity));
        System.out.println("   0/1 Space-optimized: " + knapsack01SpaceOptimized(weights, values, capacity));
        System.out.println("   Unbounded: " + knapsackUnboundedTabulated(weights, values, capacity));

        // Matrix Chain
        System.out.println("\n6. Matrix Chain Multiplication:");
        int[] dims = {10, 20, 30, 40, 30};
        System.out.println("   Dimensions: " + Arrays.toString(dims));
        System.out.println("   Naive: " + matrixChainNaive(dims));
        System.out.println("   Memoized: " + matrixChainMemoized(dims));
        System.out.println("   Tabulated: " + matrixChainTabulated(dims));

        // Palindromes
        System.out.println("\n7. Palindrome Problems:");
        String pStr = "bbbab";
        System.out.println("   String: '" + pStr + "'");
        System.out.println("   Longest palindromic subsequence: " +
                         longestPalindromeSubsequenceTabulated(pStr));
        System.out.println("   Count palindromic substrings: " +
                         countPalindromicSubstrings(pStr));
        System.out.println("   Min insertions for palindrome: " +
                         minInsertionsPalindrome(pStr));
        System.out.println("   Min cuts for palindrome partition: " +
                         palindromePartitioningMinCuts(pStr));

        // Maximum Subarray
        System.out.println("\n8. Maximum Subarray Sum:");
        int[] arr2 = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        System.out.println("   Array: " + Arrays.toString(arr2));
        System.out.println("   Naive: " + maxSubarrayNaive(arr2));
        System.out.println("   Kadane's: " + maxSubarrayKadane(arr2));
        SubarrayResult result = maxSubarrayWithIndices(arr2);
        System.out.println("   With indices: sum=" + result.maxSum +
                         ", range=[" + result.start + ":" + (result.end + 1) + "]");

        int[] arrCircular = {5, -3, 5};
        System.out.println("   Circular array: " + Arrays.toString(arrCircular));
        System.out.println("   Max circular sum: " + maxSubarrayCircular(arrCircular));

        System.out.println("\n" + "=".repeat(70));
    }
}

