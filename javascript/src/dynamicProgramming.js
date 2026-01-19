/**
 * @module dynamicProgramming
 * @description Dynamic programming algorithms
 */

/**
 * 0/1 Knapsack Problem
 * Time: O(nW), Space: O(nW) or O(W) with optimization
 * @param {Array<number>} weights - Item weights
 * @param {Array<number>} values - Item values
 * @param {number} capacity - Knapsack capacity
 * @returns {Object} {maxValue, items}
 */
export function knapsack(weights, values, capacity) {
    const n = weights.length;
    const dp = Array(n + 1).fill().map(() => Array(capacity + 1).fill(0));

    // Build DP table
    for (let i = 1; i <= n; i++) {
        for (let w = 0; w <= capacity; w++) {
            if (weights[i - 1] <= w) {
                dp[i][w] = Math.max(
                    dp[i - 1][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]
                );
            } else {
                dp[i][w] = dp[i - 1][w];
            }
        }
    }

    // Backtrack to find items
    const items = [];
    let w = capacity;
    for (let i = n; i > 0 && w > 0; i--) {
        if (dp[i][w] !== dp[i - 1][w]) {
            items.push(i - 1);
            w -= weights[i - 1];
        }
    }

    return { maxValue: dp[n][capacity], items: items.reverse() };
}

/**
 * Unbounded Knapsack Problem
 * @param {Array<number>} weights - Item weights
 * @param {Array<number>} values - Item values
 * @param {number} capacity - Knapsack capacity
 * @returns {number} Maximum value
 */
export function unboundedKnapsack(weights, values, capacity) {
    const dp = new Array(capacity + 1).fill(0);

    for (let w = 1; w <= capacity; w++) {
        for (let i = 0; i < weights.length; i++) {
            if (weights[i] <= w) {
                dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
            }
        }
    }

    return dp[capacity];
}

/**
 * Fractional Knapsack (Greedy approach)
 * @param {Array<number>} weights - Item weights
 * @param {Array<number>} values - Item values
 * @param {number} capacity - Knapsack capacity
 * @returns {Object} {maxValue, items}
 */
export function fractionalKnapsack(weights, values, capacity) {
    const items = weights.map((weight, index) => ({
        index,
        weight,
        value: values[index],
        ratio: values[index] / weight
    }));

    // Sort by value-to-weight ratio
    items.sort((a, b) => b.ratio - a.ratio);

    let totalValue = 0;
    let remainingCapacity = capacity;
    const selectedItems = [];

    for (const item of items) {
        if (remainingCapacity === 0) break;

        if (item.weight <= remainingCapacity) {
            totalValue += item.value;
            remainingCapacity -= item.weight;
            selectedItems.push({ index: item.index, fraction: 1 });
        } else {
            const fraction = remainingCapacity / item.weight;
            totalValue += item.value * fraction;
            selectedItems.push({ index: item.index, fraction });
            remainingCapacity = 0;
        }
    }

    return { maxValue: totalValue, items: selectedItems };
}

/**
 * Coin Change - Minimum coins
 * Time: O(n*amount), Space: O(amount)
 * @param {Array<number>} coins - Coin denominations
 * @param {number} amount - Target amount
 * @returns {number} Minimum coins needed (-1 if impossible)
 */
export function coinChange(coins, amount) {
    const dp = new Array(amount + 1).fill(Infinity);
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
 * Coin Change - Number of ways
 * @param {Array<number>} coins - Coin denominations
 * @param {number} amount - Target amount
 * @returns {number} Number of ways to make change
 */
export function coinChangeWays(coins, amount) {
    const dp = new Array(amount + 1).fill(0);
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
 * Time: O(mn), Space: O(mn)
 * @param {string} str1 - First string
 * @param {string} str2 - Second string
 * @returns {number} Minimum edit distance
 */
export function editDistance(str1, str2) {
    const m = str1.length;
    const n = str2.length;
    const dp = Array(m + 1).fill().map(() => Array(n + 1).fill(0));

    // Base cases
    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;

    // Fill DP table
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (str1[i - 1] === str2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + Math.min(
                    dp[i - 1][j],     // delete
                    dp[i][j - 1],     // insert
                    dp[i - 1][j - 1]  // replace
                );
            }
        }
    }

    return dp[m][n];
}

/**
 * Longest Increasing Subsequence
 * Time: O(n²), Space: O(n)
 * @param {Array<number>} arr - Input array
 * @returns {Object} {length, sequence}
 */
export function longestIncreasingSubsequence(arr) {
    if (arr.length === 0) return { length: 0, sequence: [] };

    const n = arr.length;
    const dp = new Array(n).fill(1);
    const parent = new Array(n).fill(-1);

    for (let i = 1; i < n; i++) {
        for (let j = 0; j < i; j++) {
            if (arr[j] < arr[i] && dp[j] + 1 > dp[i]) {
                dp[i] = dp[j] + 1;
                parent[i] = j;
            }
        }
    }

    // Find max length and its index
    let maxLength = 0;
    let maxIndex = 0;
    for (let i = 0; i < n; i++) {
        if (dp[i] > maxLength) {
            maxLength = dp[i];
            maxIndex = i;
        }
    }

    // Reconstruct sequence
    const sequence = [];
    let curr = maxIndex;
    while (curr !== -1) {
        sequence.unshift(arr[curr]);
        curr = parent[curr];
    }

    return { length: maxLength, sequence };
}

/**
 * Longest Increasing Subsequence - O(n log n) using binary search
 * @param {Array<number>} arr - Input array
 * @returns {number} Length of LIS
 */
export function longestIncreasingSubsequenceFast(arr) {
    const tails = [];

    for (const num of arr) {
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

        tails[left] = num;
    }

    return tails.length;
}

/**
 * Longest Common Subsequence
 * Time: O(mn), Space: O(mn)
 * @param {string} str1 - First string
 * @param {string} str2 - Second string
 * @returns {Object} {length, sequence}
 */
export function longestCommonSubsequenceDp(str1, str2) {
    const m = str1.length;
    const n = str2.length;
    const dp = Array(m + 1).fill().map(() => Array(n + 1).fill(0));

    // Fill DP table
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (str1[i - 1] === str2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    // Backtrack to find sequence
    let i = m, j = n;
    const sequence = [];

    while (i > 0 && j > 0) {
        if (str1[i - 1] === str2[j - 1]) {
            sequence.unshift(str1[i - 1]);
            i--;
            j--;
        } else if (dp[i - 1][j] > dp[i][j - 1]) {
            i--;
        } else {
            j--;
        }
    }

    return { length: dp[m][n], sequence: sequence.join('') };
}

/**
 * Matrix Chain Multiplication
 * Time: O(n³), Space: O(n²)
 * @param {Array<number>} dimensions - Matrix dimensions
 * @returns {number} Minimum number of multiplications
 */
export function matrixChainMultiplication(dimensions) {
    const n = dimensions.length - 1;
    const dp = Array(n).fill().map(() => Array(n).fill(0));

    for (let len = 2; len <= n; len++) {
        for (let i = 0; i <= n - len; i++) {
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
 * Maximum Subarray Sum (Kadane's Algorithm)
 * Time: O(n), Space: O(1)
 * @param {Array<number>} arr - Input array
 * @returns {Object} {maxSum, start, end}
 */
export function maxSubarraySum(arr) {
    let maxSoFar = arr[0];
    let maxEndingHere = arr[0];
    let start = 0;
    let end = 0;
    let tempStart = 0;

    for (let i = 1; i < arr.length; i++) {
        if (arr[i] > maxEndingHere + arr[i]) {
            maxEndingHere = arr[i];
            tempStart = i;
        } else {
            maxEndingHere = maxEndingHere + arr[i];
        }

        if (maxEndingHere > maxSoFar) {
            maxSoFar = maxEndingHere;
            start = tempStart;
            end = i;
        }
    }

    return {
        maxSum: maxSoFar,
        start,
        end,
        subarray: arr.slice(start, end + 1)
    };
}

/**
 * Maximum Product Subarray
 * Time: O(n), Space: O(1)
 * @param {Array<number>} arr - Input array
 * @returns {number} Maximum product
 */
export function maxProductSubarray(arr) {
    let maxSoFar = arr[0];
    let maxEndingHere = arr[0];
    let minEndingHere = arr[0];

    for (let i = 1; i < arr.length; i++) {
        const temp = maxEndingHere;
        maxEndingHere = Math.max(arr[i], arr[i] * maxEndingHere, arr[i] * minEndingHere);
        minEndingHere = Math.min(arr[i], arr[i] * temp, arr[i] * minEndingHere);
        maxSoFar = Math.max(maxSoFar, maxEndingHere);
    }

    return maxSoFar;
}

/**
 * House Robber Problem
 * Time: O(n), Space: O(1)
 * @param {Array<number>} houses - House values
 * @returns {number} Maximum value that can be robbed
 */
export function houseRobber(houses) {
    if (houses.length === 0) return 0;
    if (houses.length === 1) return houses[0];

    let prev2 = houses[0];
    let prev1 = Math.max(houses[0], houses[1]);

    for (let i = 2; i < houses.length; i++) {
        const current = Math.max(prev1, prev2 + houses[i]);
        prev2 = prev1;
        prev1 = current;
    }

    return prev1;
}

/**
 * House Robber II (Circular)
 * @param {Array<number>} houses - House values in circle
 * @returns {number} Maximum value that can be robbed
 */
export function houseRobberCircular(houses) {
    if (houses.length === 0) return 0;
    if (houses.length === 1) return houses[0];
    if (houses.length === 2) return Math.max(houses[0], houses[1]);

    // Rob houses 0 to n-2
    const rob1 = houseRobberRange(houses, 0, houses.length - 2);
    // Rob houses 1 to n-1
    const rob2 = houseRobberRange(houses, 1, houses.length - 1);

    return Math.max(rob1, rob2);
}

function houseRobberRange(houses, start, end) {
    let prev2 = houses[start];
    let prev1 = Math.max(houses[start], houses[start + 1]);

    for (let i = start + 2; i <= end; i++) {
        const current = Math.max(prev1, prev2 + houses[i]);
        prev2 = prev1;
        prev1 = current;
    }

    return prev1;
}

/**
 * Climbing Stairs
 * Time: O(n), Space: O(1)
 * @param {number} n - Number of stairs
 * @returns {number} Number of ways to climb
 */
export function climbingStairs(n) {
    if (n <= 2) return n;

    let prev2 = 1;
    let prev1 = 2;

    for (let i = 3; i <= n; i++) {
        const current = prev1 + prev2;
        prev2 = prev1;
        prev1 = current;
    }

    return prev1;
}

/**
 * Unique Paths in Grid
 * Time: O(mn), Space: O(mn)
 * @param {number} m - Number of rows
 * @param {number} n - Number of columns
 * @returns {number} Number of unique paths
 */
export function uniquePaths(m, n) {
    const dp = Array(m).fill().map(() => Array(n).fill(1));

    for (let i = 1; i < m; i++) {
        for (let j = 1; j < n; j++) {
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
        }
    }

    return dp[m - 1][n - 1];
}

/**
 * Unique Paths with Obstacles
 * @param {Array<Array<number>>} grid - Grid with obstacles (1)
 * @returns {number} Number of unique paths
 */
export function uniquePathsWithObstacles(grid) {
    const m = grid.length;
    const n = grid[0].length;

    if (grid[0][0] === 1 || grid[m - 1][n - 1] === 1) return 0;

    const dp = Array(m).fill().map(() => Array(n).fill(0));
    dp[0][0] = 1;

    // Fill first row
    for (let j = 1; j < n; j++) {
        dp[0][j] = grid[0][j] === 1 ? 0 : dp[0][j - 1];
    }

    // Fill first column
    for (let i = 1; i < m; i++) {
        dp[i][0] = grid[i][0] === 1 ? 0 : dp[i - 1][0];
    }

    // Fill rest of the grid
    for (let i = 1; i < m; i++) {
        for (let j = 1; j < n; j++) {
            if (grid[i][j] === 1) {
                dp[i][j] = 0;
            } else {
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
            }
        }
    }

    return dp[m - 1][n - 1];
}

/**
 * Minimum Path Sum
 * @param {Array<Array<number>>} grid - Grid with values
 * @returns {number} Minimum path sum
 */
export function minPathSum(grid) {
    const m = grid.length;
    const n = grid[0].length;
    const dp = Array(m).fill().map(() => Array(n).fill(0));

    dp[0][0] = grid[0][0];

    // Fill first row
    for (let j = 1; j < n; j++) {
        dp[0][j] = dp[0][j - 1] + grid[0][j];
    }

    // Fill first column
    for (let i = 1; i < m; i++) {
        dp[i][0] = dp[i - 1][0] + grid[i][0];
    }

    // Fill rest of the grid
    for (let i = 1; i < m; i++) {
        for (let j = 1; j < n; j++) {
            dp[i][j] = Math.min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j];
        }
    }

    return dp[m - 1][n - 1];
}

/**
 * Partition Equal Subset Sum
 * @param {Array<number>} nums - Array of numbers
 * @returns {boolean} Can partition into equal subsets
 */
export function canPartition(nums) {
    const sum = nums.reduce((a, b) => a + b, 0);

    if (sum % 2 !== 0) return false;

    const target = sum / 2;
    const dp = new Array(target + 1).fill(false);
    dp[0] = true;

    for (const num of nums) {
        for (let i = target; i >= num; i--) {
            dp[i] = dp[i] || dp[i - num];
        }
    }

    return dp[target];
}

/**
 * Target Sum (Plus/Minus)
 * @param {Array<number>} nums - Array of numbers
 * @param {number} target - Target sum
 * @returns {number} Number of ways to achieve target
 */
export function targetSum(nums, target) {
    const sum = nums.reduce((a, b) => a + b, 0);

    if ((sum + target) % 2 !== 0 || Math.abs(target) > sum) return 0;

    const subsetSum = (sum + target) / 2;
    const dp = new Array(subsetSum + 1).fill(0);
    dp[0] = 1;

    for (const num of nums) {
        for (let i = subsetSum; i >= num; i--) {
            dp[i] += dp[i - num];
        }
    }

    return dp[subsetSum];
}

/**
 * Palindrome Partitioning - Minimum Cuts
 * @param {string} s - Input string
 * @returns {number} Minimum cuts needed
 */
export function minPalindromePartition(s) {
    const n = s.length;
    const isPalindrome = Array(n).fill().map(() => Array(n).fill(false));

    // Build palindrome table
    for (let i = 0; i < n; i++) {
        isPalindrome[i][i] = true;
    }

    for (let len = 2; len <= n; len++) {
        for (let i = 0; i <= n - len; i++) {
            const j = i + len - 1;
            if (s[i] === s[j]) {
                isPalindrome[i][j] = len === 2 || isPalindrome[i + 1][j - 1];
            }
        }
    }

    // DP for minimum cuts
    const dp = new Array(n).fill(0);

    for (let i = 0; i < n; i++) {
        if (isPalindrome[0][i]) {
            dp[i] = 0;
        } else {
            dp[i] = i;
            for (let j = 1; j <= i; j++) {
                if (isPalindrome[j][i]) {
                    dp[i] = Math.min(dp[i], dp[j - 1] + 1);
                }
            }
        }
    }

    return dp[n - 1];
}

/**
 * Word Break
 * @param {string} s - String to break
 * @param {Array<string>} wordDict - Dictionary of words
 * @returns {boolean} Can break into words
 */
export function wordBreak(s, wordDict) {
    const wordSet = new Set(wordDict);
    const dp = new Array(s.length + 1).fill(false);
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
 * @param {string} s - String to match
 * @param {string} p - Pattern with . and *
 * @returns {boolean} True if matches
 */
export function regexMatch(s, p) {
    const m = s.length;
    const n = p.length;
    const dp = Array(m + 1).fill().map(() => Array(n + 1).fill(false));

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
                    dp[i][j] = dp[i][j] || dp[i - 1][j]; // One or more occurrences
                }
            }
        }
    }

    return dp[m][n];
}

/**
 * Stock Buy and Sell with K Transactions
 * @param {number} k - Maximum transactions
 * @param {Array<number>} prices - Stock prices
 * @returns {number} Maximum profit
 */
export function maxProfitKTransactions(k, prices) {
    if (!prices || prices.length === 0) return 0;

    const n = prices.length;

    if (k >= Math.floor(n / 2)) {
        // Can make as many transactions as we want
        let profit = 0;
        for (let i = 1; i < n; i++) {
            if (prices[i] > prices[i - 1]) {
                profit += prices[i] - prices[i - 1];
            }
        }
        return profit;
    }

    const buy = new Array(k + 1).fill(-prices[0]);
    const sell = new Array(k + 1).fill(0);

    for (let i = 1; i < n; i++) {
        for (let j = k; j >= 1; j--) {
            sell[j] = Math.max(sell[j], buy[j] + prices[i]);
            buy[j] = Math.max(buy[j], sell[j - 1] - prices[i]);
        }
    }

    return sell[k];
}

/**
 * Egg Drop Problem
 * @param {number} eggs - Number of eggs
 * @param {number} floors - Number of floors
 * @returns {number} Minimum trials in worst case
 */
export function eggDrop(eggs, floors) {
    const dp = Array(eggs + 1).fill().map(() => Array(floors + 1).fill(0));

    // Base cases
    for (let i = 1; i <= eggs; i++) {
        dp[i][1] = 1; // One trial for one floor
        dp[i][0] = 0; // Zero trials for zero floors
    }

    for (let j = 1; j <= floors; j++) {
        dp[1][j] = j; // Need j trials for j floors with 1 egg
    }

    // Fill rest of the table
    for (let i = 2; i <= eggs; i++) {
        for (let j = 2; j <= floors; j++) {
            dp[i][j] = Infinity;

            for (let x = 1; x <= j; x++) {
                const res = 1 + Math.max(
                    dp[i - 1][x - 1], // Egg breaks
                    dp[i][j - x]      // Egg doesn't break
                );
                dp[i][j] = Math.min(dp[i][j], res);
            }
        }
    }

    return dp[eggs][floors];
}

// Export all dynamic programming algorithms
export default {
    knapsack,
    unboundedKnapsack,
    fractionalKnapsack,
    coinChange,
    coinChangeWays,
    editDistance,
    longestIncreasingSubsequence,
    longestIncreasingSubsequenceFast,
    longestCommonSubsequenceDp,
    matrixChainMultiplication,
    maxSubarraySum,
    maxProductSubarray,
    houseRobber,
    houseRobberCircular,
    climbingStairs,
    uniquePaths,
    uniquePathsWithObstacles,
    minPathSum,
    canPartition,
    targetSum,
    minPalindromePartition,
    wordBreak,
    regexMatch,
    maxProfitKTransactions,
    eggDrop
};