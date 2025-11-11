/**
 * Dynamic Programming Classic Problems
 * =====================================
 *
 * Comprehensive implementations of classic DP problems with multiple
 * solution approaches: naive recursive, memoized (top-down),
 * tabulated (bottom-up), and space-optimized versions.
 */

// ============================================================================
// 1. LONGEST COMMON SUBSEQUENCE (LCS)
// ============================================================================

/**
 * Problem: Find the length of the longest subsequence common to two sequences.
 *
 * Real-world applications:
 * - Version control systems (diff algorithms)
 * - DNA sequence analysis
 * - Plagiarism detection
 * - File comparison tools
 */

/**
 * Naive recursive solution.
 * Time: O(2^(m+n))
 * Space: O(m+n)
 */
function lcsNaive(s1, s2, i = 0, j = 0) {
    if (i === s1.length || j === s2.length) {
        return 0;
    }

    if (s1[i] === s2[j]) {
        return 1 + lcsNaive(s1, s2, i + 1, j + 1);
    } else {
        return Math.max(
            lcsNaive(s1, s2, i + 1, j),
            lcsNaive(s1, s2, i, j + 1)
        );
    }
}

/**
 * Memoized solution.
 * Time: O(m*n)
 * Space: O(m*n)
 */
function lcsMemoized(s1, s2) {
    const memo = new Map();

    function helper(i, j) {
        if (i === s1.length || j === s2.length) {
            return 0;
        }

        const key = `${i},${j}`;
        if (memo.has(key)) {
            return memo.get(key);
        }

        let result;
        if (s1[i] === s2[j]) {
            result = 1 + helper(i + 1, j + 1);
        } else {
            result = Math.max(helper(i + 1, j), helper(i, j + 1));
        }

        memo.set(key, result);
        return result;
    }

    return helper(0, 0);
}

/**
 * Tabulated solution.
 * Time: O(m*n)
 * Space: O(m*n)
 */
function lcsTabulated(s1, s2) {
    const m = s1.length;
    const n = s2.length;
    const dp = Array(m + 1).fill(null)
        .map(() => Array(n + 1).fill(0));

    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (s1[i - 1] === s2[j - 1]) {
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
function lcsSpaceOptimized(s1, s2) {
    if (s1.length < s2.length) {
        [s1, s2] = [s2, s1];
    }

    const n = s2.length;
    let prev = Array(n + 1).fill(0);
    let curr = Array(n + 1).fill(0);

    for (let i = 1; i <= s1.length; i++) {
        for (let j = 1; j <= n; j++) {
            if (s1[i - 1] === s2[j - 1]) {
                curr[j] = 1 + prev[j - 1];
            } else {
                curr[j] = Math.max(prev[j], curr[j - 1]);
            }
        }
        [prev, curr] = [curr, prev];
    }

    return prev[n];
}

// ============================================================================
// 2. LONGEST INCREASING SUBSEQUENCE (LIS)
// ============================================================================

/**
 * Problem: Find the length of the longest strictly increasing subsequence.
 *
 * Real-world applications:
 * - Stock market trend analysis
 * - Task scheduling
 * - Patience sorting
 */

/**
 * Naive recursive solution.
 * Time: O(2^n)
 * Space: O(n)
 */
function lisNaive(arr, idx = 0, prev = -Infinity) {
    if (idx === arr.length) {
        return 0;
    }

    const exclude = lisNaive(arr, idx + 1, prev);
    const include = arr[idx] > prev
        ? 1 + lisNaive(arr, idx + 1, arr[idx])
        : 0;

    return Math.max(exclude, include);
}

/**
 * Memoized solution.
 * Time: O(n^2)
 * Space: O(n^2)
 */
function lisMemoized(arr) {
    const memo = new Map();

    function helper(idx, prevIdx) {
        if (idx === arr.length) {
            return 0;
        }

        const key = `${idx},${prevIdx}`;
        if (memo.has(key)) {
            return memo.get(key);
        }

        const exclude = helper(idx + 1, prevIdx);
        const include = (prevIdx === -1 || arr[idx] > arr[prevIdx])
            ? 1 + helper(idx + 1, idx)
            : 0;

        const result = Math.max(exclude, include);
        memo.set(key, result);
        return result;
    }

    return helper(0, -1);
}

/**
 * Tabulated O(n^2) solution.
 * Time: O(n^2)
 * Space: O(n)
 */
function lisTabulated(arr) {
    if (arr.length === 0) return 0;

    const n = arr.length;
    const dp = Array(n).fill(1);

    for (let i = 1; i < n; i++) {
        for (let j = 0; j < i; j++) {
            if (arr[j] < arr[i]) {
                dp[i] = Math.max(dp[i], dp[j] + 1);
            }
        }
    }

    return Math.max(...dp);
}

/**
 * Optimized solution using binary search.
 * Time: O(n log n)
 * Space: O(n)
 */
function lisOptimized(arr) {
    if (arr.length === 0) return 0;

    const tails = [];

    function binarySearch(val) {
        let left = 0, right = tails.length;
        while (left < right) {
            const mid = Math.floor((left + right) / 2);
            if (tails[mid] < val) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        return left;
    }

    for (const num of arr) {
        const pos = binarySearch(num);
        if (pos === tails.length) {
            tails.push(num);
        } else {
            tails[pos] = num;
        }
    }

    return tails.length;
}

// ============================================================================
// 3. EDIT DISTANCE (LEVENSHTEIN DISTANCE)
// ============================================================================

/**
 * Problem: Minimum operations (insert, delete, replace) to convert s1 to s2.
 *
 * Real-world applications:
 * - Spell checkers
 * - DNA sequence alignment
 * - Fuzzy string matching
 * - Autocorrect systems
 */

/**
 * Naive recursive solution.
 * Time: O(3^max(m,n))
 * Space: O(max(m, n))
 */
function editDistanceNaive(s1, s2, i = s1.length, j = s2.length) {
    if (i === 0) return j;
    if (j === 0) return i;

    if (s1[i - 1] === s2[j - 1]) {
        return editDistanceNaive(s1, s2, i - 1, j - 1);
    }

    return 1 + Math.min(
        editDistanceNaive(s1, s2, i, j - 1),     // insert
        editDistanceNaive(s1, s2, i - 1, j),     // delete
        editDistanceNaive(s1, s2, i - 1, j - 1)  // replace
    );
}

/**
 * Memoized solution.
 * Time: O(m*n)
 * Space: O(m*n)
 */
function editDistanceMemoized(s1, s2) {
    const memo = new Map();

    function helper(i, j) {
        if (i === 0) return j;
        if (j === 0) return i;

        const key = `${i},${j}`;
        if (memo.has(key)) {
            return memo.get(key);
        }

        let result;
        if (s1[i - 1] === s2[j - 1]) {
            result = helper(i - 1, j - 1);
        } else {
            result = 1 + Math.min(
                helper(i, j - 1),     // insert
                helper(i - 1, j),     // delete
                helper(i - 1, j - 1)  // replace
            );
        }

        memo.set(key, result);
        return result;
    }

    return helper(s1.length, s2.length);
}

/**
 * Tabulated solution.
 * Time: O(m*n)
 * Space: O(m*n)
 */
function editDistanceTabulated(s1, s2) {
    const m = s1.length;
    const n = s2.length;
    const dp = Array(m + 1).fill(null)
        .map(() => Array(n + 1).fill(0));

    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;

    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (s1[i - 1] === s2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + Math.min(
                    dp[i][j - 1],     // insert
                    dp[i - 1][j],     // delete
                    dp[i - 1][j - 1]  // replace
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
function editDistanceSpaceOptimized(s1, s2) {
    if (s1.length < s2.length) {
        [s1, s2] = [s2, s1];
    }

    const n = s2.length;
    let prev = Array.from({ length: n + 1 }, (_, i) => i);
    let curr = Array(n + 1).fill(0);

    for (let i = 1; i <= s1.length; i++) {
        curr[0] = i;
        for (let j = 1; j <= n; j++) {
            if (s1[i - 1] === s2[j - 1]) {
                curr[j] = prev[j - 1];
            } else {
                curr[j] = 1 + Math.min(curr[j - 1], prev[j], prev[j - 1]);
            }
        }
        [prev, curr] = [curr, prev];
    }

    return prev[n];
}

// ============================================================================
// 4. COIN CHANGE PROBLEM
// ============================================================================

/**
 * Problem: Find minimum coins needed or count ways to make change.
 *
 * Real-world applications:
 * - Vending machines
 * - Currency exchange
 * - Resource allocation
 */

/**
 * Naive recursive - minimum coins.
 * Time: O(amount^len(coins))
 * Space: O(amount)
 */
function coinChangeMinNaive(coins, amount) {
    function helper(remaining) {
        if (remaining === 0) return 0;
        if (remaining < 0) return Infinity;

        let minCoins = Infinity;
        for (const coin of coins) {
            const result = helper(remaining - coin);
            if (result !== Infinity) {
                minCoins = Math.min(minCoins, result + 1);
            }
        }
        return minCoins;
    }

    const result = helper(amount);
    return result === Infinity ? -1 : result;
}

/**
 * Memoized - minimum coins.
 * Time: O(amount * len(coins))
 * Space: O(amount)
 */
function coinChangeMinMemoized(coins, amount) {
    const memo = new Map();

    function helper(remaining) {
        if (remaining === 0) return 0;
        if (remaining < 0) return Infinity;

        if (memo.has(remaining)) {
            return memo.get(remaining);
        }

        let minCoins = Infinity;
        for (const coin of coins) {
            const result = helper(remaining - coin);
            if (result !== Infinity) {
                minCoins = Math.min(minCoins, result + 1);
            }
        }

        memo.set(remaining, minCoins);
        return minCoins;
    }

    const result = helper(amount);
    return result === Infinity ? -1 : result;
}

/**
 * Tabulated - minimum coins.
 * Time: O(amount * len(coins))
 * Space: O(amount)
 */
function coinChangeMinTabulated(coins, amount) {
    const dp = Array(amount + 1).fill(Infinity);
    dp[0] = 0;

    for (let i = 1; i <= amount; i++) {
        for (const coin of coins) {
            if (coin <= i && dp[i - coin] !== Infinity) {
                dp[i] = Math.min(dp[i], dp[i - coin] + 1);
            }
        }
    }

    return dp[amount] === Infinity ? -1 : dp[amount];
}

/**
 * Count number of ways to make change.
 * Time: O(amount * len(coins))
 * Space: O(amount)
 */
function coinChangeWaysTabulated(coins, amount) {
    const dp = Array(amount + 1).fill(0);
    dp[0] = 1;

    for (const coin of coins) {
        for (let i = coin; i <= amount; i++) {
            dp[i] += dp[i - coin];
        }
    }

    return dp[amount];
}

// ============================================================================
// 5. KNAPSACK PROBLEMS
// ============================================================================

/**
 * Problem: Maximize value within weight capacity.
 *
 * Real-world applications:
 * - Resource allocation
 * - Portfolio optimization
 * - Cargo loading
 */

/**
 * 0/1 Knapsack - Naive recursive.
 * Time: O(2^n)
 * Space: O(n)
 */
function knapsack01Naive(weights, values, capacity, idx = 0) {
    if (idx === weights.length || capacity === 0) {
        return 0;
    }

    const skip = knapsack01Naive(weights, values, capacity, idx + 1);
    const take = weights[idx] <= capacity
        ? values[idx] + knapsack01Naive(weights, values, capacity - weights[idx], idx + 1)
        : 0;

    return Math.max(skip, take);
}

/**
 * 0/1 Knapsack - Memoized.
 * Time: O(n * capacity)
 * Space: O(n * capacity)
 */
function knapsack01Memoized(weights, values, capacity) {
    const memo = new Map();

    function helper(idx, remaining) {
        if (idx === weights.length || remaining === 0) {
            return 0;
        }

        const key = `${idx},${remaining}`;
        if (memo.has(key)) {
            return memo.get(key);
        }

        const skip = helper(idx + 1, remaining);
        const take = weights[idx] <= remaining
            ? values[idx] + helper(idx + 1, remaining - weights[idx])
            : 0;

        const result = Math.max(skip, take);
        memo.set(key, result);
        return result;
    }

    return helper(0, capacity);
}

/**
 * 0/1 Knapsack - Tabulated.
 * Time: O(n * capacity)
 * Space: O(n * capacity)
 */
function knapsack01Tabulated(weights, values, capacity) {
    const n = weights.length;
    const dp = Array(n + 1).fill(null)
        .map(() => Array(capacity + 1).fill(0));

    for (let i = 1; i <= n; i++) {
        for (let w = 0; w <= capacity; w++) {
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
function knapsack01SpaceOptimized(weights, values, capacity) {
    const dp = Array(capacity + 1).fill(0);

    for (let i = 0; i < weights.length; i++) {
        for (let w = capacity; w >= weights[i]; w--) {
            dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }

    return dp[capacity];
}

/**
 * Unbounded Knapsack - unlimited items.
 * Time: O(n * capacity)
 * Space: O(capacity)
 */
function knapsackUnboundedTabulated(weights, values, capacity) {
    const dp = Array(capacity + 1).fill(0);

    for (let w = 1; w <= capacity; w++) {
        for (let i = 0; i < weights.length; i++) {
            if (weights[i] <= w) {
                dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
            }
        }
    }

    return dp[capacity];
}

// ============================================================================
// 6. MATRIX CHAIN MULTIPLICATION
// ============================================================================

/**
 * Problem: Find optimal parenthesization to minimize multiplications.
 *
 * Real-world applications:
 * - Compiler optimization
 * - Database query optimization
 * - Computer graphics
 */

/**
 * Naive recursive solution.
 * Time: O(2^n)
 * Space: O(n)
 */
function matrixChainNaive(dims, i = 1, j = dims.length - 1) {
    if (i === j) return 0;

    let minCost = Infinity;
    for (let k = i; k < j; k++) {
        const cost =
            matrixChainNaive(dims, i, k) +
            matrixChainNaive(dims, k + 1, j) +
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
function matrixChainMemoized(dims) {
    const memo = new Map();

    function helper(i, j) {
        if (i === j) return 0;

        const key = `${i},${j}`;
        if (memo.has(key)) {
            return memo.get(key);
        }

        let minCost = Infinity;
        for (let k = i; k < j; k++) {
            const cost =
                helper(i, k) +
                helper(k + 1, j) +
                dims[i - 1] * dims[k] * dims[j];
            minCost = Math.min(minCost, cost);
        }

        memo.set(key, minCost);
        return minCost;
    }

    return helper(1, dims.length - 1);
}

/**
 * Tabulated solution.
 * Time: O(n^3)
 * Space: O(n^2)
 */
function matrixChainTabulated(dims) {
    const n = dims.length;
    const dp = Array(n).fill(null)
        .map(() => Array(n).fill(0));

    for (let length = 2; length < n; length++) {
        for (let i = 1; i < n - length + 1; i++) {
            const j = i + length - 1;
            dp[i][j] = Infinity;

            for (let k = i; k < j; k++) {
                const cost =
                    dp[i][k] +
                    dp[k + 1][j] +
                    dims[i - 1] * dims[k] * dims[j];
                dp[i][j] = Math.min(dp[i][j], cost);
            }
        }
    }

    return dp[1][n - 1];
}

// ============================================================================
// 7. PALINDROME PROBLEMS
// ============================================================================

/**
 * Problems: Longest palindromic subsequence, count palindromes, min cuts.
 *
 * Real-world applications:
 * - DNA sequence analysis
 * - Text processing
 * - Pattern recognition
 */

/**
 * Longest palindromic subsequence - Naive.
 * Time: O(2^n)
 * Space: O(n)
 */
function longestPalindromeSubsequenceNaive(s, i = 0, j = s.length - 1) {
    if (i > j) return 0;
    if (i === j) return 1;

    if (s[i] === s[j]) {
        return 2 + longestPalindromeSubsequenceNaive(s, i + 1, j - 1);
    } else {
        return Math.max(
            longestPalindromeSubsequenceNaive(s, i + 1, j),
            longestPalindromeSubsequenceNaive(s, i, j - 1)
        );
    }
}

/**
 * Longest palindromic subsequence - Tabulated.
 * Time: O(n^2)
 * Space: O(n^2)
 */
function longestPalindromeSubsequenceTabulated(s) {
    const n = s.length;
    const dp = Array(n).fill(null)
        .map(() => Array(n).fill(0));

    for (let i = 0; i < n; i++) {
        dp[i][i] = 1;
    }

    for (let length = 2; length <= n; length++) {
        for (let i = 0; i < n - length + 1; i++) {
            const j = i + length - 1;

            if (s[i] === s[j]) {
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
function countPalindromicSubstrings(s) {
    function expandAroundCenter(left, right) {
        let count = 0;
        while (left >= 0 && right < s.length && s[left] === s[right]) {
            count++;
            left--;
            right++;
        }
        return count;
    }

    let total = 0;
    for (let i = 0; i < s.length; i++) {
        total += expandAroundCenter(i, i);      // odd length
        total += expandAroundCenter(i, i + 1);  // even length
    }

    return total;
}

/**
 * Minimum insertions to make palindrome.
 * Time: O(n^2)
 * Space: O(n^2)
 */
function minInsertionsPalindrome(s) {
    return s.length - longestPalindromeSubsequenceTabulated(s);
}

/**
 * Minimum cuts for palindrome partitioning.
 * Time: O(n^2)
 * Space: O(n^2)
 */
function palindromePartitioningMinCuts(s) {
    const n = s.length;

    // Build palindrome table
    const isPalindrome = Array(n).fill(null)
        .map(() => Array(n).fill(false));

    for (let i = 0; i < n; i++) {
        isPalindrome[i][i] = true;
    }

    for (let length = 2; length <= n; length++) {
        for (let i = 0; i < n - length + 1; i++) {
            const j = i + length - 1;
            if (s[i] === s[j]) {
                isPalindrome[i][j] = (length === 2) || isPalindrome[i + 1][j - 1];
            }
        }
    }

    // DP for minimum cuts
    const dp = Array(n).fill(Infinity);
    for (let i = 0; i < n; i++) {
        if (isPalindrome[0][i]) {
            dp[i] = 0;
        } else {
            for (let j = 0; j < i; j++) {
                if (isPalindrome[j + 1][i]) {
                    dp[i] = Math.min(dp[i], dp[j] + 1);
                }
            }
        }
    }

    return dp[n - 1];
}

// ============================================================================
// 8. MAXIMUM SUBARRAY SUM (KADANE'S ALGORITHM)
// ============================================================================

/**
 * Problem: Find contiguous subarray with maximum sum.
 *
 * Real-world applications:
 * - Stock market analysis
 * - Signal processing
 * - Image processing
 */

/**
 * Naive solution - check all subarrays.
 * Time: O(n^2)
 * Space: O(1)
 */
function maxSubarrayNaive(arr) {
    if (arr.length === 0) return 0;

    let maxSum = -Infinity;
    for (let i = 0; i < arr.length; i++) {
        let currentSum = 0;
        for (let j = i; j < arr.length; j++) {
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
function maxSubarrayKadane(arr) {
    if (arr.length === 0) return 0;

    let maxSum = arr[0];
    let currentSum = arr[0];

    for (let i = 1; i < arr.length; i++) {
        currentSum = Math.max(arr[i], currentSum + arr[i]);
        maxSum = Math.max(maxSum, currentSum);
    }

    return maxSum;
}

/**
 * Kadane's with indices.
 * Time: O(n)
 * Space: O(1)
 * Returns: { maxSum, start, end }
 */
function maxSubarrayWithIndices(arr) {
    if (arr.length === 0) return { maxSum: 0, start: -1, end: -1 };

    let maxSum = arr[0];
    let currentSum = arr[0];
    let start = 0, end = 0, tempStart = 0;

    for (let i = 1; i < arr.length; i++) {
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

    return { maxSum, start, end };
}

/**
 * Maximum subarray in circular array.
 * Time: O(n)
 * Space: O(1)
 */
function maxSubarrayCircular(arr) {
    if (arr.length === 0) return 0;

    function kadaneMin(arr) {
        let minSum = arr[0];
        let currentSum = arr[0];
        for (let i = 1; i < arr.length; i++) {
            currentSum = Math.min(arr[i], currentSum + arr[i]);
            minSum = Math.min(minSum, currentSum);
        }
        return minSum;
    }

    const maxNormal = maxSubarrayKadane(arr);
    if (maxNormal < 0) return maxNormal;

    const totalSum = arr.reduce((a, b) => a + b, 0);
    const minSum = kadaneMin(arr);
    const maxCircular = totalSum - minSum;

    return Math.max(maxNormal, maxCircular);
}

// ============================================================================
// EXAMPLE USAGE AND TESTING
// ============================================================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        // LCS
        lcsNaive, lcsMemoized, lcsTabulated, lcsSpaceOptimized,
        // LIS
        lisNaive, lisMemoized, lisTabulated, lisOptimized,
        // Edit Distance
        editDistanceNaive, editDistanceMemoized, editDistanceTabulated, editDistanceSpaceOptimized,
        // Coin Change
        coinChangeMinNaive, coinChangeMinMemoized, coinChangeMinTabulated, coinChangeWaysTabulated,
        // Knapsack
        knapsack01Naive, knapsack01Memoized, knapsack01Tabulated, knapsack01SpaceOptimized,
        knapsackUnboundedTabulated,
        // Matrix Chain
        matrixChainNaive, matrixChainMemoized, matrixChainTabulated,
        // Palindrome
        longestPalindromeSubsequenceNaive, longestPalindromeSubsequenceTabulated,
        countPalindromicSubstrings, minInsertionsPalindrome, palindromePartitioningMinCuts,
        // Max Subarray
        maxSubarrayNaive, maxSubarrayKadane, maxSubarrayWithIndices, maxSubarrayCircular
    };
}

// Example usage
console.log('='.repeat(70));
console.log('DYNAMIC PROGRAMMING CLASSIC PROBLEMS - EXAMPLES');
console.log('='.repeat(70));

// LCS
console.log('\n1. Longest Common Subsequence:');
const s1 = 'ABCDGH', s2 = 'AEDFHR';
console.log(`   Strings: '${s1}', '${s2}'`);
console.log(`   Naive: ${lcsNaive(s1, s2)}`);
console.log(`   Memoized: ${lcsMemoized(s1, s2)}`);
console.log(`   Tabulated: ${lcsTabulated(s1, s2)}`);
console.log(`   Space-optimized: ${lcsSpaceOptimized(s1, s2)}`);

// LIS
console.log('\n2. Longest Increasing Subsequence:');
const arr1 = [10, 9, 2, 5, 3, 7, 101, 18];
console.log(`   Array: [${arr1}]`);
console.log(`   Naive: ${lisNaive(arr1)}`);
console.log(`   Memoized: ${lisMemoized(arr1)}`);
console.log(`   Tabulated O(n^2): ${lisTabulated(arr1)}`);
console.log(`   Optimized O(n log n): ${lisOptimized(arr1)}`);

// Edit Distance
console.log('\n3. Edit Distance:');
const str1 = 'kitten', str2 = 'sitting';
console.log(`   Strings: '${str1}', '${str2}'`);
console.log(`   Naive: ${editDistanceNaive(str1, str2)}`);
console.log(`   Memoized: ${editDistanceMemoized(str1, str2)}`);
console.log(`   Tabulated: ${editDistanceTabulated(str1, str2)}`);
console.log(`   Space-optimized: ${editDistanceSpaceOptimized(str1, str2)}`);

// Coin Change
console.log('\n4. Coin Change:');
const coins = [1, 2, 5], amount = 11;
console.log(`   Coins: [${coins}], Amount: ${amount}`);
console.log(`   Min coins (naive): ${coinChangeMinNaive(coins, amount)}`);
console.log(`   Min coins (memoized): ${coinChangeMinMemoized(coins, amount)}`);
console.log(`   Min coins (tabulated): ${coinChangeMinTabulated(coins, amount)}`);
console.log(`   Ways to make change: ${coinChangeWaysTabulated(coins, amount)}`);

// Knapsack
console.log('\n5. Knapsack Problem:');
const weights = [1, 3, 4, 5], values = [1, 4, 5, 7], capacity = 7;
console.log(`   Weights: [${weights}], Values: [${values}], Capacity: ${capacity}`);
console.log(`   0/1 Naive: ${knapsack01Naive(weights, values, capacity)}`);
console.log(`   0/1 Memoized: ${knapsack01Memoized(weights, values, capacity)}`);
console.log(`   0/1 Tabulated: ${knapsack01Tabulated(weights, values, capacity)}`);
console.log(`   0/1 Space-optimized: ${knapsack01SpaceOptimized(weights, values, capacity)}`);
console.log(`   Unbounded: ${knapsackUnboundedTabulated(weights, values, capacity)}`);

// Matrix Chain
console.log('\n6. Matrix Chain Multiplication:');
const dims = [10, 20, 30, 40, 30];
console.log(`   Dimensions: [${dims}]`);
console.log(`   Naive: ${matrixChainNaive(dims)}`);
console.log(`   Memoized: ${matrixChainMemoized(dims)}`);
console.log(`   Tabulated: ${matrixChainTabulated(dims)}`);

// Palindromes
console.log('\n7. Palindrome Problems:');
const pStr = 'bbbab';
console.log(`   String: '${pStr}'`);
console.log(`   Longest palindromic subsequence: ${longestPalindromeSubsequenceTabulated(pStr)}`);
console.log(`   Count palindromic substrings: ${countPalindromicSubstrings(pStr)}`);
console.log(`   Min insertions for palindrome: ${minInsertionsPalindrome(pStr)}`);
console.log(`   Min cuts for palindrome partition: ${palindromePartitioningMinCuts(pStr)}`);

// Maximum Subarray
console.log('\n8. Maximum Subarray Sum:');
const arr2 = [-2, 1, -3, 4, -1, 2, 1, -5, 4];
console.log(`   Array: [${arr2}]`);
console.log(`   Naive: ${maxSubarrayNaive(arr2)}`);
console.log(`   Kadane's: ${maxSubarrayKadane(arr2)}`);
const result = maxSubarrayWithIndices(arr2);
console.log(`   With indices: sum=${result.maxSum}, range=[${result.start}:${result.end + 1}]`);

const arrCircular = [5, -3, 5];
console.log(`   Circular array: [${arrCircular}]`);
console.log(`   Max circular sum: ${maxSubarrayCircular(arrCircular)}`);

console.log('\n' + '='.repeat(70));
