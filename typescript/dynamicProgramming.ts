/**
 * Dynamic Programming Algorithms in TypeScript
 * =============================================
 *
 * Classic dynamic programming problems with optimizations:
 * - Memoization and tabulation approaches
 * - Space optimization techniques
 * - Generic implementations
 *
 * @module dynamicProgramming
 * @author Algorithms Multiverse
 */

/**
 * Memoization decorator for functions
 */
function memoize<Args extends any[], Return>(
    fn: (...args: Args) => Return,
    keyGenerator?: (...args: Args) => string
): (...args: Args) => Return {
    const cache = new Map<string, Return>();
    const getKey = keyGenerator || ((...args: Args) => JSON.stringify(args));

    return (...args: Args): Return => {
        const key = getKey(...args);
        if (cache.has(key)) {
            return cache.get(key)!;
        }
        const result = fn(...args);
        cache.set(key, result);
        return result;
    };
}

/**
 * Dynamic Programming Solutions Class
 */
export class DynamicProgramming {
    /**
     * Fibonacci Number (Multiple approaches)
     */
    static fibonacci(n: number): number {
        if (n <= 1) return n;

        let prev = 0;
        let curr = 1;

        for (let i = 2; i <= n; i++) {
            const temp = curr;
            curr = prev + curr;
            prev = temp;
        }

        return curr;
    }

    /**
     * Fibonacci with memoization
     */
    static fibonacciMemo = memoize((n: number): number => {
        if (n <= 1) return n;
        return DynamicProgramming.fibonacciMemo(n - 1) +
               DynamicProgramming.fibonacciMemo(n - 2);
    });

    /**
     * Longest Common Subsequence
     */
    static longestCommonSubsequence(text1: string, text2: string): number {
        const m = text1.length;
        const n = text2.length;
        const dp: number[][] = Array(m + 1)
            .fill(0)
            .map(() => Array(n + 1).fill(0));

        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                if (text1[i - 1] === text2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }

        return dp[m][n];
    }

    /**
     * Get the actual LCS string
     */
    static getLCS(text1: string, text2: string): string {
        const m = text1.length;
        const n = text2.length;
        const dp: number[][] = Array(m + 1)
            .fill(0)
            .map(() => Array(n + 1).fill(0));

        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                if (text1[i - 1] === text2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }

        // Backtrack to find the LCS
        let lcs = "";
        let i = m, j = n;

        while (i > 0 && j > 0) {
            if (text1[i - 1] === text2[j - 1]) {
                lcs = text1[i - 1] + lcs;
                i--;
                j--;
            } else if (dp[i - 1][j] > dp[i][j - 1]) {
                i--;
            } else {
                j--;
            }
        }

        return lcs;
    }

    /**
     * Longest Increasing Subsequence
     */
    static longestIncreasingSubsequence(nums: number[]): number {
        if (nums.length === 0) return 0;

        const dp: number[] = new Array(nums.length).fill(1);

        for (let i = 1; i < nums.length; i++) {
            for (let j = 0; j < i; j++) {
                if (nums[j] < nums[i]) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                }
            }
        }

        return Math.max(...dp);
    }

    /**
     * LIS with O(n log n) using binary search
     */
    static lisOptimized(nums: number[]): number {
        const tails: number[] = [];

        for (const num of nums) {
            let left = 0;
            let right = tails.length;

            while (left < right) {
                const mid = Math.floor((left + right) / 2);
                if (tails[mid] < num) {
                    left = mid + 1;
                } else {
                    right = mid;
                }
            }

            if (left === tails.length) {
                tails.push(num);
            } else {
                tails[left] = num;
            }
        }

        return tails.length;
    }

    /**
     * 0/1 Knapsack Problem
     */
    static knapsack(
        weights: number[],
        values: number[],
        capacity: number
    ): { maxValue: number; items: number[] } {
        const n = weights.length;
        const dp: number[][] = Array(n + 1)
            .fill(0)
            .map(() => Array(capacity + 1).fill(0));

        for (let i = 1; i <= n; i++) {
            for (let w = 1; w <= capacity; w++) {
                if (weights[i - 1] <= w) {
                    dp[i][w] = Math.max(
                        dp[i - 1][w],
                        values[i - 1] + dp[i - 1][w - weights[i - 1]]
                    );
                } else {
                    dp[i][w] = dp[i - 1][w];
                }
            }
        }

        // Backtrack to find items
        const items: number[] = [];
        let i = n, w = capacity;

        while (i > 0 && w > 0) {
            if (dp[i][w] !== dp[i - 1][w]) {
                items.push(i - 1);
                w -= weights[i - 1];
            }
            i--;
        }

        return {
            maxValue: dp[n][capacity],
            items: items.reverse()
        };
    }

    /**
     * Unbounded Knapsack (items can be used multiple times)
     */
    static unboundedKnapsack(
        weights: number[],
        values: number[],
        capacity: number
    ): number {
        const dp: number[] = new Array(capacity + 1).fill(0);

        for (let w = 1; w <= capacity; w++) {
            for (let i = 0; i < weights.length; i++) {
                if (weights[i] <= w) {
                    dp[w] = Math.max(dp[w], values[i] + dp[w - weights[i]]);
                }
            }
        }

        return dp[capacity];
    }

    /**
     * Coin Change Problem (Minimum coins)
     */
    static coinChange(coins: number[], amount: number): number {
        const dp: number[] = new Array(amount + 1).fill(Infinity);
        dp[0] = 0;

        for (let i = 1; i <= amount; i++) {
            for (const coin of coins) {
                if (coin <= i) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
                }
            }
        }

        return dp[amount] === Infinity ? -1 : dp[amount];
    }

    /**
     * Coin Change 2 (Number of ways to make amount)
     */
    static coinChangeWays(coins: number[], amount: number): number {
        const dp: number[] = new Array(amount + 1).fill(0);
        dp[0] = 1;

        for (const coin of coins) {
            for (let i = coin; i <= amount; i++) {
                dp[i] += dp[i - coin];
            }
        }

        return dp[amount];
    }

    /**
     * Edit Distance (Levenshtein Distance)
     */
    static editDistance(word1: string, word2: string): number {
        const m = word1.length;
        const n = word2.length;
        const dp: number[][] = Array(m + 1)
            .fill(0)
            .map(() => Array(n + 1).fill(0));

        // Initialize base cases
        for (let i = 0; i <= m; i++) {
            dp[i][0] = i;
        }
        for (let j = 0; j <= n; j++) {
            dp[0][j] = j;
        }

        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                if (word1[i - 1] === word2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(
                        dp[i - 1][j],    // Delete
                        dp[i][j - 1],    // Insert
                        dp[i - 1][j - 1] // Replace
                    );
                }
            }
        }

        return dp[m][n];
    }

    /**
     * Maximum Subarray Sum (Kadane's Algorithm)
     */
    static maxSubarraySum(nums: number[]): number {
        let maxSoFar = nums[0];
        let maxEndingHere = nums[0];

        for (let i = 1; i < nums.length; i++) {
            maxEndingHere = Math.max(nums[i], maxEndingHere + nums[i]);
            maxSoFar = Math.max(maxSoFar, maxEndingHere);
        }

        return maxSoFar;
    }

    /**
     * Get the actual maximum subarray
     */
    static getMaxSubarray(nums: number[]): number[] {
        let maxSoFar = nums[0];
        let maxEndingHere = nums[0];
        let start = 0, end = 0, tempStart = 0;

        for (let i = 1; i < nums.length; i++) {
            if (nums[i] > maxEndingHere + nums[i]) {
                maxEndingHere = nums[i];
                tempStart = i;
            } else {
                maxEndingHere = maxEndingHere + nums[i];
            }

            if (maxEndingHere > maxSoFar) {
                maxSoFar = maxEndingHere;
                start = tempStart;
                end = i;
            }
        }

        return nums.slice(start, end + 1);
    }

    /**
     * House Robber Problem
     */
    static houseRobber(nums: number[]): number {
        if (nums.length === 0) return 0;
        if (nums.length === 1) return nums[0];

        let prev2 = 0;
        let prev1 = nums[0];

        for (let i = 1; i < nums.length; i++) {
            const current = Math.max(prev1, prev2 + nums[i]);
            prev2 = prev1;
            prev1 = current;
        }

        return prev1;
    }

    /**
     * Unique Paths in Grid
     */
    static uniquePaths(m: number, n: number): number {
        const dp: number[] = new Array(n).fill(1);

        for (let i = 1; i < m; i++) {
            for (let j = 1; j < n; j++) {
                dp[j] += dp[j - 1];
            }
        }

        return dp[n - 1];
    }

    /**
     * Unique Paths with Obstacles
     */
    static uniquePathsWithObstacles(obstacleGrid: number[][]): number {
        const m = obstacleGrid.length;
        const n = obstacleGrid[0].length;

        if (obstacleGrid[0][0] === 1 || obstacleGrid[m - 1][n - 1] === 1) {
            return 0;
        }

        const dp: number[] = new Array(n).fill(0);
        dp[0] = 1;

        for (let i = 0; i < m; i++) {
            for (let j = 0; j < n; j++) {
                if (obstacleGrid[i][j] === 1) {
                    dp[j] = 0;
                } else if (j > 0) {
                    dp[j] += dp[j - 1];
                }
            }
        }

        return dp[n - 1];
    }

    /**
     * Palindromic Substrings Count
     */
    static countPalindromicSubstrings(s: string): number {
        const n = s.length;
        let count = 0;

        // Expand around center approach
        const expandAroundCenter = (left: number, right: number): void => {
            while (left >= 0 && right < n && s[left] === s[right]) {
                count++;
                left--;
                right++;
            }
        };

        for (let i = 0; i < n; i++) {
            expandAroundCenter(i, i);     // Odd length palindromes
            expandAroundCenter(i, i + 1); // Even length palindromes
        }

        return count;
    }

    /**
     * Longest Palindromic Substring
     */
    static longestPalindromicSubstring(s: string): string {
        if (s.length === 0) return "";

        let start = 0;
        let maxLen = 0;

        const expandAroundCenter = (left: number, right: number): void => {
            while (left >= 0 && right < s.length && s[left] === s[right]) {
                const currentLen = right - left + 1;
                if (currentLen > maxLen) {
                    start = left;
                    maxLen = currentLen;
                }
                left--;
                right++;
            }
        };

        for (let i = 0; i < s.length; i++) {
            expandAroundCenter(i, i);
            expandAroundCenter(i, i + 1);
        }

        return s.substring(start, start + maxLen);
    }

    /**
     * Matrix Chain Multiplication
     */
    static matrixChainMultiplication(dimensions: number[]): number {
        const n = dimensions.length - 1;
        const dp: number[][] = Array(n)
            .fill(0)
            .map(() => Array(n).fill(0));

        for (let len = 2; len <= n; len++) {
            for (let i = 0; i < n - len + 1; i++) {
                const j = i + len - 1;
                dp[i][j] = Infinity;

                for (let k = i; k < j; k++) {
                    const cost = dp[i][k] + dp[k + 1][j] +
                        dimensions[i] * dimensions[k + 1] * dimensions[j + 1];
                    dp[i][j] = Math.min(dp[i][j], cost);
                }
            }
        }

        return dp[0][n - 1];
    }

    /**
     * Partition Equal Subset Sum
     */
    static canPartition(nums: number[]): boolean {
        const sum = nums.reduce((a, b) => a + b, 0);

        if (sum % 2 !== 0) return false;

        const target = sum / 2;
        const dp: boolean[] = new Array(target + 1).fill(false);
        dp[0] = true;

        for (const num of nums) {
            for (let i = target; i >= num; i--) {
                dp[i] = dp[i] || dp[i - num];
            }
        }

        return dp[target];
    }

    /**
     * Word Break Problem
     */
    static wordBreak(s: string, wordDict: string[]): boolean {
        const wordSet = new Set(wordDict);
        const dp: boolean[] = new Array(s.length + 1).fill(false);
        dp[0] = true;

        for (let i = 1; i <= s.length; i++) {
            for (let j = 0; j < i; j++) {
                if (dp[j] && wordSet.has(s.substring(j, i))) {
                    dp[i] = true;
                    break;
                }
            }
        }

        return dp[s.length];
    }

    /**
     * Regular Expression Matching
     */
    static isMatch(s: string, p: string): boolean {
        const m = s.length;
        const n = p.length;
        const dp: boolean[][] = Array(m + 1)
            .fill(false)
            .map(() => Array(n + 1).fill(false));

        dp[0][0] = true;

        // Handle patterns like a*, a*b*, etc.
        for (let j = 1; j <= n; j++) {
            if (p[j - 1] === '*') {
                dp[0][j] = dp[0][j - 2];
            }
        }

        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                if (p[j - 1] === '.' || p[j - 1] === s[i - 1]) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else if (p[j - 1] === '*') {
                    dp[i][j] = dp[i][j - 2]; // Zero occurrences

                    if (p[j - 2] === '.' || p[j - 2] === s[i - 1]) {
                        dp[i][j] = dp[i][j] || dp[i - 1][j]; // One or more
                    }
                }
            }
        }

        return dp[m][n];
    }
}

// Example usage and tests
if (require.main === module) {
    console.log("TypeScript Dynamic Programming Demonstration");
    console.log("=" .repeat(50));

    console.log("\n1. Fibonacci Numbers:");
    console.log("fib(10):", DynamicProgramming.fibonacci(10));
    console.log("fib(20) memoized:", DynamicProgramming.fibonacciMemo(20));

    console.log("\n2. Longest Common Subsequence:");
    const text1 = "ABCDGH";
    const text2 = "AEDFHR";
    console.log(`LCS("${text1}", "${text2}"):`, DynamicProgramming.longestCommonSubsequence(text1, text2));
    console.log("LCS string:", DynamicProgramming.getLCS(text1, text2));

    console.log("\n3. Longest Increasing Subsequence:");
    const nums = [10, 9, 2, 5, 3, 7, 101, 18];
    console.log("Array:", nums);
    console.log("LIS length:", DynamicProgramming.longestIncreasingSubsequence(nums));
    console.log("LIS optimized:", DynamicProgramming.lisOptimized(nums));

    console.log("\n4. Knapsack Problem:");
    const weights = [1, 3, 4, 5];
    const values = [1, 4, 5, 7];
    const capacity = 7;
    const knapsackResult = DynamicProgramming.knapsack(weights, values, capacity);
    console.log("Items weight:", weights);
    console.log("Items value:", values);
    console.log("Capacity:", capacity);
    console.log("Result:", knapsackResult);

    console.log("\n5. Coin Change:");
    const coins = [1, 2, 5];
    const amount = 11;
    console.log("Coins:", coins);
    console.log("Amount:", amount);
    console.log("Minimum coins:", DynamicProgramming.coinChange(coins, amount));
    console.log("Number of ways:", DynamicProgramming.coinChangeWays(coins, amount));

    console.log("\n6. Edit Distance:");
    const word1 = "horse";
    const word2 = "ros";
    console.log(`Edit distance("${word1}", "${word2}"):`, DynamicProgramming.editDistance(word1, word2));

    console.log("\n7. Maximum Subarray:");
    const array = [-2, 1, -3, 4, -1, 2, 1, -5, 4];
    console.log("Array:", array);
    console.log("Max sum:", DynamicProgramming.maxSubarraySum(array));
    console.log("Max subarray:", DynamicProgramming.getMaxSubarray(array));

    console.log("\n8. House Robber:");
    const houses = [2, 7, 9, 3, 1];
    console.log("Houses:", houses);
    console.log("Max robbery:", DynamicProgramming.houseRobber(houses));

    console.log("\n9. Unique Paths:");
    console.log("3x7 grid paths:", DynamicProgramming.uniquePaths(3, 7));

    console.log("\n10. Palindromic Substrings:");
    const str = "aaa";
    console.log(`String: "${str}"`);
    console.log("Palindromic substrings count:", DynamicProgramming.countPalindromicSubstrings(str));
    console.log("Longest palindrome:", DynamicProgramming.longestPalindromicSubstring("babad"));

    console.log("\n11. Word Break:");
    const s = "leetcode";
    const wordDict = ["leet", "code"];
    console.log(`Can break "${s}" with dict:`, wordDict, "->", DynamicProgramming.wordBreak(s, wordDict));
}