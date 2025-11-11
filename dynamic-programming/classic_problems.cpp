/**
 * Dynamic Programming Classic Problems
 * =====================================
 *
 * Comprehensive implementations of classic DP problems with multiple
 * solution approaches: naive recursive, memoized (top-down),
 * tabulated (bottom-up), and space-optimized versions.
 *
 * Compile: g++ -std=c++17 -O2 classic_problems.cpp -o classic_problems
 * Run: ./classic_problems
 */

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <climits>
#include <numeric>

using namespace std;

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
 */

/**
 * Naive recursive solution.
 * Time: O(2^(m+n))
 * Space: O(m+n)
 */
int lcsNaive(const string& s1, const string& s2, int i = 0, int j = 0) {
    if (i == s1.length() || j == s2.length()) {
        return 0;
    }

    if (s1[i] == s2[j]) {
        return 1 + lcsNaive(s1, s2, i + 1, j + 1);
    } else {
        return max(lcsNaive(s1, s2, i + 1, j), lcsNaive(s1, s2, i, j + 1));
    }
}

/**
 * Memoized solution.
 * Time: O(m*n)
 * Space: O(m*n)
 */
int lcsMemoizedHelper(const string& s1, const string& s2, int i, int j,
                      unordered_map<string, int>& memo) {
    if (i == s1.length() || j == s2.length()) {
        return 0;
    }

    string key = to_string(i) + "," + to_string(j);
    if (memo.find(key) != memo.end()) {
        return memo[key];
    }

    int result;
    if (s1[i] == s2[j]) {
        result = 1 + lcsMemoizedHelper(s1, s2, i + 1, j + 1, memo);
    } else {
        result = max(lcsMemoizedHelper(s1, s2, i + 1, j, memo),
                    lcsMemoizedHelper(s1, s2, i, j + 1, memo));
    }

    memo[key] = result;
    return result;
}

int lcsMemoized(const string& s1, const string& s2) {
    unordered_map<string, int> memo;
    return lcsMemoizedHelper(s1, s2, 0, 0, memo);
}

/**
 * Tabulated solution.
 * Time: O(m*n)
 * Space: O(m*n)
 */
int lcsTabulated(const string& s1, const string& s2) {
    int m = s1.length();
    int n = s2.length();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s1[i - 1] == s2[j - 1]) {
                dp[i][j] = 1 + dp[i - 1][j - 1];
            } else {
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
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
int lcsSpaceOptimized(string s1, string s2) {
    if (s1.length() < s2.length()) {
        swap(s1, s2);
    }

    int m = s1.length();
    int n = s2.length();
    vector<int> prev(n + 1, 0);
    vector<int> curr(n + 1, 0);

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s1[i - 1] == s2[j - 1]) {
                curr[j] = 1 + prev[j - 1];
            } else {
                curr[j] = max(prev[j], curr[j - 1]);
            }
        }
        swap(prev, curr);
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
 */

/**
 * Naive recursive solution.
 * Time: O(2^n)
 * Space: O(n)
 */
int lisNaiveHelper(const vector<int>& arr, int idx, int prev) {
    if (idx == arr.size()) {
        return 0;
    }

    int exclude = lisNaiveHelper(arr, idx + 1, prev);
    int include = 0;
    if (arr[idx] > prev) {
        include = 1 + lisNaiveHelper(arr, idx + 1, arr[idx]);
    }

    return max(exclude, include);
}

int lisNaive(const vector<int>& arr) {
    return lisNaiveHelper(arr, 0, INT_MIN);
}

/**
 * Tabulated O(n^2) solution.
 * Time: O(n^2)
 * Space: O(n)
 */
int lisTabulated(const vector<int>& arr) {
    if (arr.empty()) return 0;

    int n = arr.size();
    vector<int> dp(n, 1);

    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (arr[j] < arr[i]) {
                dp[i] = max(dp[i], dp[j] + 1);
            }
        }
    }

    return *max_element(dp.begin(), dp.end());
}

/**
 * Optimized solution using binary search.
 * Time: O(n log n)
 * Space: O(n)
 */
int lisOptimized(const vector<int>& arr) {
    if (arr.empty()) return 0;

    vector<int> tails;

    for (int num : arr) {
        auto pos = lower_bound(tails.begin(), tails.end(), num);
        if (pos == tails.end()) {
            tails.push_back(num);
        } else {
            *pos = num;
        }
    }

    return tails.size();
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
 * - Autocorrect systems
 */

/**
 * Naive recursive solution.
 * Time: O(3^max(m,n))
 * Space: O(max(m, n))
 */
int editDistanceNaive(const string& s1, const string& s2, int i, int j) {
    if (i == 0) return j;
    if (j == 0) return i;

    if (s1[i - 1] == s2[j - 1]) {
        return editDistanceNaive(s1, s2, i - 1, j - 1);
    }

    return 1 + min({
        editDistanceNaive(s1, s2, i, j - 1),     // insert
        editDistanceNaive(s1, s2, i - 1, j),     // delete
        editDistanceNaive(s1, s2, i - 1, j - 1)  // replace
    });
}

int editDistanceNaive(const string& s1, const string& s2) {
    return editDistanceNaive(s1, s2, s1.length(), s2.length());
}

/**
 * Memoized solution.
 * Time: O(m*n)
 * Space: O(m*n)
 */
int editDistanceMemoizedHelper(const string& s1, const string& s2, int i, int j,
                                unordered_map<string, int>& memo) {
    if (i == 0) return j;
    if (j == 0) return i;

    string key = to_string(i) + "," + to_string(j);
    if (memo.find(key) != memo.end()) {
        return memo[key];
    }

    int result;
    if (s1[i - 1] == s2[j - 1]) {
        result = editDistanceMemoizedHelper(s1, s2, i - 1, j - 1, memo);
    } else {
        result = 1 + min({
            editDistanceMemoizedHelper(s1, s2, i, j - 1, memo),
            editDistanceMemoizedHelper(s1, s2, i - 1, j, memo),
            editDistanceMemoizedHelper(s1, s2, i - 1, j - 1, memo)
        });
    }

    memo[key] = result;
    return result;
}

int editDistanceMemoized(const string& s1, const string& s2) {
    unordered_map<string, int> memo;
    return editDistanceMemoizedHelper(s1, s2, s1.length(), s2.length(), memo);
}

/**
 * Tabulated solution.
 * Time: O(m*n)
 * Space: O(m*n)
 */
int editDistanceTabulated(const string& s1, const string& s2) {
    int m = s1.length();
    int n = s2.length();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1));

    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int j = 0; j <= n; j++) dp[0][j] = j;

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s1[i - 1] == s2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + min({dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1]});
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
int editDistanceSpaceOptimized(string s1, string s2) {
    if (s1.length() < s2.length()) {
        swap(s1, s2);
    }

    int n = s2.length();
    vector<int> prev(n + 1);
    vector<int> curr(n + 1);

    for (int j = 0; j <= n; j++) {
        prev[j] = j;
    }

    for (int i = 1; i <= s1.length(); i++) {
        curr[0] = i;
        for (int j = 1; j <= n; j++) {
            if (s1[i - 1] == s2[j - 1]) {
                curr[j] = prev[j - 1];
            } else {
                curr[j] = 1 + min({curr[j - 1], prev[j], prev[j - 1]});
            }
        }
        swap(prev, curr);
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
 */

/**
 * Naive recursive - minimum coins.
 * Time: O(amount^len(coins))
 * Space: O(amount)
 */
int coinChangeMinNaiveHelper(const vector<int>& coins, int remaining) {
    if (remaining == 0) return 0;
    if (remaining < 0) return INT_MAX;

    int minCoins = INT_MAX;
    for (int coin : coins) {
        int result = coinChangeMinNaiveHelper(coins, remaining - coin);
        if (result != INT_MAX) {
            minCoins = min(minCoins, result + 1);
        }
    }

    return minCoins;
}

int coinChangeMinNaive(const vector<int>& coins, int amount) {
    int result = coinChangeMinNaiveHelper(coins, amount);
    return result == INT_MAX ? -1 : result;
}

/**
 * Memoized - minimum coins.
 * Time: O(amount * len(coins))
 * Space: O(amount)
 */
int coinChangeMinMemoizedHelper(const vector<int>& coins, int remaining,
                                 unordered_map<int, int>& memo) {
    if (remaining == 0) return 0;
    if (remaining < 0) return INT_MAX;

    if (memo.find(remaining) != memo.end()) {
        return memo[remaining];
    }

    int minCoins = INT_MAX;
    for (int coin : coins) {
        int result = coinChangeMinMemoizedHelper(coins, remaining - coin, memo);
        if (result != INT_MAX) {
            minCoins = min(minCoins, result + 1);
        }
    }

    memo[remaining] = minCoins;
    return minCoins;
}

int coinChangeMinMemoized(const vector<int>& coins, int amount) {
    unordered_map<int, int> memo;
    int result = coinChangeMinMemoizedHelper(coins, amount, memo);
    return result == INT_MAX ? -1 : result;
}

/**
 * Tabulated - minimum coins.
 * Time: O(amount * len(coins))
 * Space: O(amount)
 */
int coinChangeMinTabulated(const vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, INT_MAX);
    dp[0] = 0;

    for (int i = 1; i <= amount; i++) {
        for (int coin : coins) {
            if (coin <= i && dp[i - coin] != INT_MAX) {
                dp[i] = min(dp[i], dp[i - coin] + 1);
            }
        }
    }

    return dp[amount] == INT_MAX ? -1 : dp[amount];
}

/**
 * Count number of ways to make change.
 * Time: O(amount * len(coins))
 * Space: O(amount)
 */
int coinChangeWaysTabulated(const vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, 0);
    dp[0] = 1;

    for (int coin : coins) {
        for (int i = coin; i <= amount; i++) {
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
 */

/**
 * 0/1 Knapsack - Naive recursive.
 * Time: O(2^n)
 * Space: O(n)
 */
int knapsack01NaiveHelper(const vector<int>& weights, const vector<int>& values,
                          int capacity, int idx) {
    if (idx == weights.size() || capacity == 0) {
        return 0;
    }

    int skip = knapsack01NaiveHelper(weights, values, capacity, idx + 1);
    int take = 0;
    if (weights[idx] <= capacity) {
        take = values[idx] + knapsack01NaiveHelper(weights, values,
                                                    capacity - weights[idx], idx + 1);
    }

    return max(skip, take);
}

int knapsack01Naive(const vector<int>& weights, const vector<int>& values, int capacity) {
    return knapsack01NaiveHelper(weights, values, capacity, 0);
}

/**
 * 0/1 Knapsack - Tabulated.
 * Time: O(n * capacity)
 * Space: O(n * capacity)
 */
int knapsack01Tabulated(const vector<int>& weights, const vector<int>& values, int capacity) {
    int n = weights.size();
    vector<vector<int>> dp(n + 1, vector<int>(capacity + 1, 0));

    for (int i = 1; i <= n; i++) {
        for (int w = 0; w <= capacity; w++) {
            dp[i][w] = dp[i - 1][w];
            if (weights[i - 1] <= w) {
                dp[i][w] = max(dp[i][w],
                             dp[i - 1][w - weights[i - 1]] + values[i - 1]);
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
int knapsack01SpaceOptimized(const vector<int>& weights, const vector<int>& values,
                             int capacity) {
    vector<int> dp(capacity + 1, 0);

    for (int i = 0; i < weights.size(); i++) {
        for (int w = capacity; w >= weights[i]; w--) {
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }

    return dp[capacity];
}

/**
 * Unbounded Knapsack.
 * Time: O(n * capacity)
 * Space: O(capacity)
 */
int knapsackUnboundedTabulated(const vector<int>& weights, const vector<int>& values,
                                int capacity) {
    vector<int> dp(capacity + 1, 0);

    for (int w = 1; w <= capacity; w++) {
        for (int i = 0; i < weights.size(); i++) {
            if (weights[i] <= w) {
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i]);
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
 */

/**
 * Naive recursive solution.
 * Time: O(2^n)
 * Space: O(n)
 */
int matrixChainNaive(const vector<int>& dims, int i, int j) {
    if (i == j) return 0;

    int minCost = INT_MAX;
    for (int k = i; k < j; k++) {
        int cost = matrixChainNaive(dims, i, k) +
                   matrixChainNaive(dims, k + 1, j) +
                   dims[i - 1] * dims[k] * dims[j];
        minCost = min(minCost, cost);
    }

    return minCost;
}

int matrixChainNaive(const vector<int>& dims) {
    return matrixChainNaive(dims, 1, dims.size() - 1);
}

/**
 * Memoized solution.
 * Time: O(n^3)
 * Space: O(n^2)
 */
int matrixChainMemoizedHelper(const vector<int>& dims, int i, int j,
                               unordered_map<string, int>& memo) {
    if (i == j) return 0;

    string key = to_string(i) + "," + to_string(j);
    if (memo.find(key) != memo.end()) {
        return memo[key];
    }

    int minCost = INT_MAX;
    for (int k = i; k < j; k++) {
        int cost = matrixChainMemoizedHelper(dims, i, k, memo) +
                   matrixChainMemoizedHelper(dims, k + 1, j, memo) +
                   dims[i - 1] * dims[k] * dims[j];
        minCost = min(minCost, cost);
    }

    memo[key] = minCost;
    return minCost;
}

int matrixChainMemoized(const vector<int>& dims) {
    unordered_map<string, int> memo;
    return matrixChainMemoizedHelper(dims, 1, dims.size() - 1, memo);
}

/**
 * Tabulated solution.
 * Time: O(n^3)
 * Space: O(n^2)
 */
int matrixChainTabulated(const vector<int>& dims) {
    int n = dims.size();
    vector<vector<int>> dp(n, vector<int>(n, 0));

    for (int length = 2; length < n; length++) {
        for (int i = 1; i < n - length + 1; i++) {
            int j = i + length - 1;
            dp[i][j] = INT_MAX;

            for (int k = i; k < j; k++) {
                int cost = dp[i][k] + dp[k + 1][j] +
                          dims[i - 1] * dims[k] * dims[j];
                dp[i][j] = min(dp[i][j], cost);
            }
        }
    }

    return dp[1][n - 1];
}

// ============================================================================
// 7. PALINDROME PROBLEMS
// ============================================================================

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
int longestPalindromeSubsequenceTabulated(const string& s) {
    int n = s.length();
    vector<vector<int>> dp(n, vector<int>(n, 0));

    for (int i = 0; i < n; i++) {
        dp[i][i] = 1;
    }

    for (int length = 2; length <= n; length++) {
        for (int i = 0; i < n - length + 1; i++) {
            int j = i + length - 1;

            if (s[i] == s[j]) {
                dp[i][j] = 2 + (i + 1 <= j - 1 ? dp[i + 1][j - 1] : 0);
            } else {
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1]);
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
int expandAroundCenter(const string& s, int left, int right) {
    int count = 0;
    while (left >= 0 && right < s.length() && s[left] == s[right]) {
        count++;
        left--;
        right++;
    }
    return count;
}

int countPalindromicSubstrings(const string& s) {
    int total = 0;
    for (int i = 0; i < s.length(); i++) {
        total += expandAroundCenter(s, i, i);      // odd length
        total += expandAroundCenter(s, i, i + 1);  // even length
    }
    return total;
}

/**
 * Minimum insertions to make palindrome.
 * Time: O(n^2)
 * Space: O(n^2)
 */
int minInsertionsPalindrome(const string& s) {
    return s.length() - longestPalindromeSubsequenceTabulated(s);
}

/**
 * Minimum cuts for palindrome partitioning.
 * Time: O(n^2)
 * Space: O(n^2)
 */
int palindromePartitioningMinCuts(const string& s) {
    int n = s.length();

    vector<vector<bool>> isPalindrome(n, vector<bool>(n, false));
    for (int i = 0; i < n; i++) {
        isPalindrome[i][i] = true;
    }

    for (int length = 2; length <= n; length++) {
        for (int i = 0; i < n - length + 1; i++) {
            int j = i + length - 1;
            if (s[i] == s[j]) {
                isPalindrome[i][j] = (length == 2) || isPalindrome[i + 1][j - 1];
            }
        }
    }

    vector<int> dp(n, INT_MAX);
    for (int i = 0; i < n; i++) {
        if (isPalindrome[0][i]) {
            dp[i] = 0;
        } else {
            for (int j = 0; j < i; j++) {
                if (isPalindrome[j + 1][i]) {
                    dp[i] = min(dp[i], dp[j] + 1);
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
 */

/**
 * Naive solution - check all subarrays.
 * Time: O(n^2)
 * Space: O(1)
 */
int maxSubarrayNaive(const vector<int>& arr) {
    if (arr.empty()) return 0;

    int maxSum = INT_MIN;
    for (int i = 0; i < arr.size(); i++) {
        int currentSum = 0;
        for (int j = i; j < arr.size(); j++) {
            currentSum += arr[j];
            maxSum = max(maxSum, currentSum);
        }
    }

    return maxSum;
}

/**
 * Kadane's Algorithm - optimal.
 * Time: O(n)
 * Space: O(1)
 */
int maxSubarrayKadane(const vector<int>& arr) {
    if (arr.empty()) return 0;

    int maxSum = arr[0];
    int currentSum = arr[0];

    for (int i = 1; i < arr.size(); i++) {
        currentSum = max(arr[i], currentSum + arr[i]);
        maxSum = max(maxSum, currentSum);
    }

    return maxSum;
}

/**
 * Kadane's with indices.
 */
struct SubarrayResult {
    int maxSum;
    int start;
    int end;
};

SubarrayResult maxSubarrayWithIndices(const vector<int>& arr) {
    if (arr.empty()) return {0, -1, -1};

    int maxSum = arr[0];
    int currentSum = arr[0];
    int start = 0, end = 0, tempStart = 0;

    for (int i = 1; i < arr.size(); i++) {
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

    return {maxSum, start, end};
}

/**
 * Maximum subarray in circular array.
 * Time: O(n)
 * Space: O(1)
 */
int kadaneMin(const vector<int>& arr) {
    int minSum = arr[0];
    int currentSum = arr[0];
    for (int i = 1; i < arr.size(); i++) {
        currentSum = min(arr[i], currentSum + arr[i]);
        minSum = min(minSum, currentSum);
    }
    return minSum;
}

int maxSubarrayCircular(const vector<int>& arr) {
    if (arr.empty()) return 0;

    int maxNormal = maxSubarrayKadane(arr);
    if (maxNormal < 0) return maxNormal;

    int totalSum = accumulate(arr.begin(), arr.end(), 0);
    int minSum = kadaneMin(arr);
    int maxCircular = totalSum - minSum;

    return max(maxNormal, maxCircular);
}

// ============================================================================
// MAIN - EXAMPLE USAGE AND TESTING
// ============================================================================

int main() {
    cout << string(70, '=') << endl;
    cout << "DYNAMIC PROGRAMMING CLASSIC PROBLEMS - EXAMPLES" << endl;
    cout << string(70, '=') << endl;

    // LCS Examples
    cout << "\n1. Longest Common Subsequence:" << endl;
    string s1 = "ABCDGH", s2 = "AEDFHR";
    cout << "   Strings: '" << s1 << "', '" << s2 << "'" << endl;
    cout << "   Naive: " << lcsNaive(s1, s2) << endl;
    cout << "   Memoized: " << lcsMemoized(s1, s2) << endl;
    cout << "   Tabulated: " << lcsTabulated(s1, s2) << endl;
    cout << "   Space-optimized: " << lcsSpaceOptimized(s1, s2) << endl;

    // LIS Examples
    cout << "\n2. Longest Increasing Subsequence:" << endl;
    vector<int> arr1 = {10, 9, 2, 5, 3, 7, 101, 18};
    cout << "   Array: [";
    for (int i = 0; i < arr1.size(); i++) {
        cout << arr1[i] << (i < arr1.size() - 1 ? ", " : "");
    }
    cout << "]" << endl;
    cout << "   Naive: " << lisNaive(arr1) << endl;
    cout << "   Tabulated O(n^2): " << lisTabulated(arr1) << endl;
    cout << "   Optimized O(n log n): " << lisOptimized(arr1) << endl;

    // Edit Distance
    cout << "\n3. Edit Distance:" << endl;
    string str1 = "kitten", str2 = "sitting";
    cout << "   Strings: '" << str1 << "', '" << str2 << "'" << endl;
    cout << "   Naive: " << editDistanceNaive(str1, str2) << endl;
    cout << "   Memoized: " << editDistanceMemoized(str1, str2) << endl;
    cout << "   Tabulated: " << editDistanceTabulated(str1, str2) << endl;
    cout << "   Space-optimized: " << editDistanceSpaceOptimized(str1, str2) << endl;

    // Coin Change
    cout << "\n4. Coin Change:" << endl;
    vector<int> coins = {1, 2, 5};
    int amount = 11;
    cout << "   Coins: [1, 2, 5], Amount: " << amount << endl;
    cout << "   Min coins (naive): " << coinChangeMinNaive(coins, amount) << endl;
    cout << "   Min coins (memoized): " << coinChangeMinMemoized(coins, amount) << endl;
    cout << "   Min coins (tabulated): " << coinChangeMinTabulated(coins, amount) << endl;
    cout << "   Ways to make change: " << coinChangeWaysTabulated(coins, amount) << endl;

    // Knapsack
    cout << "\n5. Knapsack Problem:" << endl;
    vector<int> weights = {1, 3, 4, 5};
    vector<int> values = {1, 4, 5, 7};
    int capacity = 7;
    cout << "   Weights: [1, 3, 4, 5], Values: [1, 4, 5, 7], Capacity: " << capacity << endl;
    cout << "   0/1 Naive: " << knapsack01Naive(weights, values, capacity) << endl;
    cout << "   0/1 Tabulated: " << knapsack01Tabulated(weights, values, capacity) << endl;
    cout << "   0/1 Space-optimized: " << knapsack01SpaceOptimized(weights, values, capacity) << endl;
    cout << "   Unbounded: " << knapsackUnboundedTabulated(weights, values, capacity) << endl;

    // Matrix Chain
    cout << "\n6. Matrix Chain Multiplication:" << endl;
    vector<int> dims = {10, 20, 30, 40, 30};
    cout << "   Dimensions: [10, 20, 30, 40, 30]" << endl;
    cout << "   Naive: " << matrixChainNaive(dims) << endl;
    cout << "   Memoized: " << matrixChainMemoized(dims) << endl;
    cout << "   Tabulated: " << matrixChainTabulated(dims) << endl;

    // Palindromes
    cout << "\n7. Palindrome Problems:" << endl;
    string pStr = "bbbab";
    cout << "   String: '" << pStr << "'" << endl;
    cout << "   Longest palindromic subsequence: "
         << longestPalindromeSubsequenceTabulated(pStr) << endl;
    cout << "   Count palindromic substrings: "
         << countPalindromicSubstrings(pStr) << endl;
    cout << "   Min insertions for palindrome: "
         << minInsertionsPalindrome(pStr) << endl;
    cout << "   Min cuts for palindrome partition: "
         << palindromePartitioningMinCuts(pStr) << endl;

    // Maximum Subarray
    cout << "\n8. Maximum Subarray Sum:" << endl;
    vector<int> arr2 = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    cout << "   Array: [-2, 1, -3, 4, -1, 2, 1, -5, 4]" << endl;
    cout << "   Naive: " << maxSubarrayNaive(arr2) << endl;
    cout << "   Kadane's: " << maxSubarrayKadane(arr2) << endl;
    SubarrayResult result = maxSubarrayWithIndices(arr2);
    cout << "   With indices: sum=" << result.maxSum
         << ", range=[" << result.start << ":" << (result.end + 1) << "]" << endl;

    vector<int> arrCircular = {5, -3, 5};
    cout << "   Circular array: [5, -3, 5]" << endl;
    cout << "   Max circular sum: " << maxSubarrayCircular(arrCircular) << endl;

    cout << "\n" << string(70, '=') << endl;

    return 0;
}
