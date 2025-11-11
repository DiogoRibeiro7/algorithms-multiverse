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
 * Compile: g++ -std=c++17 -O2 advanced_patterns.cpp -o advanced_patterns
 * Run: ./advanced_patterns
 */

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <climits>
#include <cmath>
#include <numeric>
#include <bitset>

using namespace std;

// ============================================================================
// 1. DIGIT DP
// ============================================================================

/**
 * DIGIT DP PATTERN
 * When to use:
 * - Count numbers in range [L, R] with specific digit properties
 * - Numbers with digit sum/product constraints
 * - Numbers without certain digits
 */

namespace DigitDP {
    unordered_map<string, long long> memo;

    long long dp(int pos, int digitSum, bool tight, bool started,
                 const string& digits, int k) {
        if (pos == digits.size()) {
            return (started && digitSum % k == 0) ? 1 : 0;
        }

        string key = to_string(pos) + "," + to_string(digitSum) + "," +
                     to_string(tight) + "," + to_string(started);
        if (memo.find(key) != memo.end()) {
            return memo[key];
        }

        int limit = tight ? (digits[pos] - '0') : 9;
        long long result = 0;

        for (int digit = 0; digit <= limit; digit++) {
            bool newStarted = started || (digit > 0);
            int newSum = newStarted ? (digitSum + digit) % k : 0;
            bool newTight = tight && (digit == limit);

            result += dp(pos + 1, newSum, newTight, newStarted, digits, k);
        }

        memo[key] = result;
        return result;
    }

    long long countUpTo(long long num, int k) {
        if (num < 0) return 0;

        string digits = to_string(num);
        memo.clear();
        return dp(0, 0, true, false, digits, k);
    }

    /**
     * Count numbers in [left, right] with digit sum divisible by k
     * Time: O(log(right) * k * 2)
     */
    long long countDivisibleDigitSum(long long left, long long right, int k) {
        return countUpTo(right, k) - countUpTo(left - 1, k);
    }

    // Count without forbidden digit
    unordered_map<string, long long> memo2;

    long long dpWithout(int pos, bool tight, bool started,
                        const string& digits, int forbidden) {
        if (pos == digits.size()) {
            return started ? 1 : 0;
        }

        string key = to_string(pos) + "," + to_string(tight) + "," + to_string(started);
        if (memo2.find(key) != memo2.end()) {
            return memo2[key];
        }

        int limit = tight ? (digits[pos] - '0') : 9;
        long long result = 0;

        for (int digit = 0; digit <= limit; digit++) {
            if (digit == forbidden && (started || digit > 0)) {
                continue;
            }

            bool newStarted = started || (digit > 0);
            bool newTight = tight && (digit == limit);
            result += dpWithout(pos + 1, newTight, newStarted, digits, forbidden);
        }

        memo2[key] = result;
        return result;
    }

    long long countWithoutDigit(long long left, long long right, int forbidden) {
        string rightStr = to_string(right);
        string leftStr = to_string(left - 1);

        memo2.clear();
        long long rightCount = dpWithout(0, true, false, rightStr, forbidden);

        memo2.clear();
        long long leftCount = (left > 0) ? dpWithout(0, true, false, leftStr, forbidden) : 0;

        return rightCount - leftCount;
    }
}

// ============================================================================
// 2. TREE DP
// ============================================================================

/**
 * TREE DP PATTERN
 * When to use:
 * - Optimal solutions on tree structures
 * - Maximum independent set, diameter, rerooting
 */

namespace TreeDP {
    /**
     * Maximum Independent Set on Tree
     * Time: O(n), Space: O(n)
     */
    void dfsIndependent(int node, int parent, const vector<vector<int>>& graph,
                        vector<vector<int>>& dp) {
        dp[node][0] = 0;
        dp[node][1] = 1;

        for (int child : graph[node]) {
            if (child == parent) continue;

            dfsIndependent(child, node, graph, dp);

            dp[node][0] += max(dp[child][0], dp[child][1]);
            dp[node][1] += dp[child][0];
        }
    }

    int maxIndependentSet(const vector<pair<int, int>>& edges, int n) {
        vector<vector<int>> graph(n);
        for (const auto& [u, v] : edges) {
            graph[u].push_back(v);
            graph[v].push_back(u);
        }

        vector<vector<int>> dp(n, vector<int>(2, 0));
        dfsIndependent(0, -1, graph, dp);

        return max(dp[0][0], dp[0][1]);
    }

    /**
     * Tree Diameter
     * Time: O(n), Space: O(n)
     */
    int dfsDiameter(int node, int parent, const vector<vector<int>>& graph, int& diameter) {
        vector<int> maxDepths = {0, 0};

        for (int child : graph[node]) {
            if (child == parent) continue;

            int childDepth = dfsDiameter(child, node, graph, diameter) + 1;

            if (childDepth > maxDepths[0]) {
                maxDepths[1] = maxDepths[0];
                maxDepths[0] = childDepth;
            } else if (childDepth > maxDepths[1]) {
                maxDepths[1] = childDepth;
            }
        }

        diameter = max(diameter, maxDepths[0] + maxDepths[1]);
        return maxDepths[0];
    }

    int treeDiameter(const vector<pair<int, int>>& edges, int n) {
        vector<vector<int>> graph(n);
        for (const auto& [u, v] : edges) {
            graph[u].push_back(v);
            graph[v].push_back(u);
        }

        int diameter = 0;
        dfsDiameter(0, -1, graph, diameter);
        return diameter;
    }
}

// ============================================================================
// 3. BITMASK DP
// ============================================================================

/**
 * BITMASK DP PATTERN
 * When to use:
 * - Small sets (n ≤ 20)
 * - TSP, assignment, subset problems
 */

namespace BitmaskDP {
    /**
     * Traveling Salesman Problem
     * Time: O(n^2 * 2^n), Space: O(n * 2^n)
     */
    int tsp(const vector<vector<int>>& dist) {
        int n = dist.size();
        int INF = INT_MAX / 2;

        vector<vector<int>> dp(1 << n, vector<int>(n, INF));
        dp[1][0] = 0;

        for (int mask = 0; mask < (1 << n); mask++) {
            for (int last = 0; last < n; last++) {
                if (dp[mask][last] == INF) continue;
                if (!(mask & (1 << last))) continue;

                for (int next = 0; next < n; next++) {
                    if (mask & (1 << next)) continue;

                    int newMask = mask | (1 << next);
                    dp[newMask][next] = min(dp[newMask][next],
                                           dp[mask][last] + dist[last][next]);
                }
            }
        }

        int fullMask = (1 << n) - 1;
        int result = INF;
        for (int i = 0; i < n; i++) {
            result = min(result, dp[fullMask][i]);
        }

        return result;
    }

    /**
     * Assignment Problem
     * Time: O(n * 2^n), Space: O(2^n)
     */
    int assignmentProblem(const vector<vector<int>>& cost) {
        int n = cost.size();
        int INF = INT_MAX / 2;

        vector<int> dp(1 << n, INF);
        dp[0] = 0;

        for (int mask = 0; mask < (1 << n); mask++) {
            if (dp[mask] == INF) continue;

            int person = __builtin_popcount(mask);
            if (person >= n) continue;

            for (int task = 0; task < n; task++) {
                if (mask & (1 << task)) continue;

                int newMask = mask | (1 << task);
                dp[newMask] = min(dp[newMask], dp[mask] + cost[person][task]);
            }
        }

        return dp[(1 << n) - 1];
    }

    /**
     * Optimized SOS DP
     * Time: O(n * 2^n), Space: O(2^n)
     */
    vector<int> sosDP(const vector<int>& arr) {
        int n = arr.size();
        vector<int> dp = arr;

        for (int i = 0; i < n; i++) {
            for (int mask = 0; mask < (1 << n); mask++) {
                if (mask & (1 << i)) {
                    dp[mask] += dp[mask ^ (1 << i)];
                }
            }
        }

        return dp;
    }
}

// ============================================================================
// 4. PROBABILITY DP
// ============================================================================

/**
 * PROBABILITY DP PATTERN
 * When to use:
 * - Expected value problems
 * - Probability calculations with states
 */

namespace ProbabilityDP {
    /**
     * Expected flips for n consecutive heads
     * Time: O(n), Space: O(n)
     */
    double expectedConsecutiveHeads(int n) {
        vector<double> dp(n + 1, 0.0);

        for (int i = n - 1; i >= 0; i--) {
            dp[i] = 2.0 + dp[i + 1];
        }

        return dp[0];
    }

    /**
     * Expected rolls to see all n faces (Coupon Collector)
     */
    double diceExpectedValue(int n, int faces = 6) {
        double expected = 0.0;
        for (int k = 0; k < n; k++) {
            expected += (double)faces / (faces - k);
        }
        return expected;
    }

    /**
     * 1D Random Walk
     */
    double randomWalk1D(int start, int target, int maxPos) {
        if (start <= 0 || start >= maxPos) return 0.0;
        if (start == target) return 1.0;

        vector<double> dp(maxPos, 0.0);
        dp[target] = 1.0;

        for (int i = 0; i < target; i++) {
            dp[i] = (double)i / target;
        }

        for (int i = target + 1; i < maxPos; i++) {
            dp[i] = (double)(maxPos - i) / (maxPos - target);
        }

        return dp[start];
    }
}

// ============================================================================
// 5. RANGE DP
// ============================================================================

/**
 * RANGE DP PATTERN
 * When to use:
 * - Problems on contiguous subarrays
 * - Merging intervals optimally
 */

namespace RangeDP {
    /**
     * Merge Stones (K-merge variant)
     * Time: O(n^3 / k), Space: O(n^2)
     */
    int mergeStones(const vector<int>& stones, int k) {
        int n = stones.size();

        if ((n - 1) % (k - 1) != 0) {
            return -1;
        }

        vector<int> prefix(n + 1, 0);
        for (int i = 0; i < n; i++) {
            prefix[i + 1] = prefix[i] + stones[i];
        }

        int INF = INT_MAX / 2;
        vector<vector<int>> dp(n, vector<int>(n, INF));

        for (int i = 0; i < n; i++) {
            dp[i][i] = 0;
        }

        for (int length = 2; length <= n; length++) {
            for (int i = 0; i <= n - length; i++) {
                int j = i + length - 1;

                for (int mid = i; mid < j; mid += k - 1) {
                    dp[i][j] = min(dp[i][j], dp[i][mid] + dp[mid + 1][j]);
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
    int burstBalloons(const vector<int>& nums) {
        int n = nums.size();
        vector<int> balloons(n + 2);
        balloons[0] = 1;
        balloons[n + 1] = 1;
        for (int i = 0; i < n; i++) {
            balloons[i + 1] = nums[i];
        }

        int len = balloons.size();
        vector<vector<int>> dp(len, vector<int>(len, 0));

        for (int length = 2; length < len; length++) {
            for (int i = 0; i < len - length; i++) {
                int j = i + length;

                for (int k = i + 1; k < j; k++) {
                    int coins = balloons[i] * balloons[k] * balloons[j];
                    dp[i][j] = max(dp[i][j], dp[i][k] + dp[k][j] + coins);
                }
            }
        }

        return dp[0][len - 1];
    }
}

// ============================================================================
// 6. PROFILE DP
// ============================================================================

/**
 * PROFILE DP PATTERN
 * When to use:
 * - Grid tiling problems
 * - Problems where current row depends on previous row
 */

namespace ProfileDP {
    const long long MOD = 1000000007;

    void fill(int pos, int curr, int next, const vector<long long>& dp,
              vector<long long>& newDp) {
        if (pos == 2) {
            newDp[next] = (newDp[next] + dp[curr]) % MOD;
            return;
        }

        if (curr & (1 << pos)) {
            fill(pos + 1, curr, next, dp, newDp);
        } else {
            // Vertical domino
            fill(pos + 1, curr | (1 << pos), next | (1 << pos), dp, newDp);

            // Horizontal domino
            if (pos + 1 < 2 && !(curr & (1 << (pos + 1)))) {
                fill(pos + 2, curr | (1 << pos) | (1 << (pos + 1)), next, dp, newDp);
            }
        }
    }

    /**
     * Domino Tiling (2×n grid)
     * Time: O(n), Space: O(1)
     */
    long long dominoTiling2xN(int n) {
        vector<long long> dp(4, 0);
        dp[0] = 1;

        for (int col = 0; col < n; col++) {
            vector<long long> newDp(4, 0);

            for (int profile = 0; profile < 4; profile++) {
                if (dp[profile] == 0) continue;

                fill(0, profile, 0, dp, newDp);
            }

            dp = newDp;
        }

        return dp[0];
    }

    void fillMxN(int row, int curr, int nxt, int m, const vector<long long>& dp,
                 vector<long long>& newDp, int mask) {
        if (row == m) {
            newDp[nxt] = (newDp[nxt] + dp[mask]) % MOD;
            return;
        }

        if (curr & (1 << row)) {
            fillMxN(row + 1, curr, nxt, m, dp, newDp, mask);
        } else {
            // Vertical
            fillMxN(row + 1, curr | (1 << row), nxt | (1 << row), m, dp, newDp, mask);

            // Horizontal
            if (row + 1 < m && !(curr & (1 << (row + 1)))) {
                fillMxN(row + 2, curr | (1 << row) | (1 << (row + 1)), nxt, m, dp, newDp, mask);
            }
        }
    }

    /**
     * Domino Tiling (m×n grid)
     * Time: O(n * 2^m * 2^m), Space: O(2^m)
     */
    long long dominoTilingMxN(int m, int n) {
        if ((m * n) % 2 == 1) return 0;

        vector<long long> dp(1 << m, 0);
        dp[0] = 1;

        for (int col = 0; col < n; col++) {
            vector<long long> newDp(1 << m, 0);

            for (int mask = 0; mask < (1 << m); mask++) {
                if (dp[mask] == 0) continue;

                fillMxN(0, mask, 0, m, dp, newDp, mask);
            }

            dp = newDp;
        }

        return dp[0];
    }
}

// ============================================================================
// MAIN - EXAMPLE USAGE
// ============================================================================

int main() {
    cout << string(70, '=') << endl;
    cout << "ADVANCED DYNAMIC PROGRAMMING PATTERNS - EXAMPLES" << endl;
    cout << string(70, '=') << endl;

    // Digit DP
    cout << "\n1. DIGIT DP:" << endl;
    cout << "   Count numbers in [1, 100] with digit sum divisible by 3:" << endl;
    cout << "   Result: " << DigitDP::countDivisibleDigitSum(1, 100, 3) << endl;

    cout << "   Count numbers in [1, 100] without digit 5:" << endl;
    cout << "   Result: " << DigitDP::countWithoutDigit(1, 100, 5) << endl;

    // Tree DP
    cout << "\n2. TREE DP:" << endl;
    vector<pair<int, int>> edges = {{0, 1}, {0, 2}, {1, 3}, {1, 4}};
    int n = 5;
    cout << "   Tree edges: [[0,1], [0,2], [1,3], [1,4]]" << endl;
    cout << "   Maximum independent set: " << TreeDP::maxIndependentSet(edges, n) << endl;
    cout << "   Tree diameter: " << TreeDP::treeDiameter(edges, n) << endl;

    // Bitmask DP
    cout << "\n3. BITMASK DP:" << endl;
    vector<vector<int>> dist = {
        {0, 10, 15, 20},
        {10, 0, 35, 25},
        {15, 35, 0, 30},
        {20, 25, 30, 0}
    };
    cout << "   TSP distance matrix:" << endl;
    for (const auto& row : dist) {
        cout << "   [";
        for (int i = 0; i < row.size(); i++) {
            cout << row[i] << (i < row.size() - 1 ? ", " : "");
        }
        cout << "]" << endl;
    }
    cout << "   Minimum TSP cost: " << BitmaskDP::tsp(dist) << endl;

    vector<vector<int>> cost = {
        {9, 2, 7, 8},
        {6, 4, 3, 7},
        {5, 8, 1, 8},
        {7, 6, 9, 4}
    };
    cout << "\n   Assignment problem cost matrix:" << endl;
    for (const auto& row : cost) {
        cout << "   [";
        for (int i = 0; i < row.size(); i++) {
            cout << row[i] << (i < row.size() - 1 ? ", " : "");
        }
        cout << "]" << endl;
    }
    cout << "   Minimum assignment cost: " << BitmaskDP::assignmentProblem(cost) << endl;

    // Probability DP
    cout << "\n4. PROBABILITY DP:" << endl;
    int numHeads = 3;
    cout << "   Expected flips for " << numHeads << " consecutive heads: "
         << ProbabilityDP::expectedConsecutiveHeads(numHeads) << endl;
    cout << "   Expected rolls to see all 6 faces: "
         << ProbabilityDP::diceExpectedValue(6) << endl;

    // Range DP
    cout << "\n5. RANGE DP:" << endl;
    vector<int> stones = {3, 2, 4, 1};
    int k = 2;
    cout << "   Stones: [3, 2, 4, 1], K: " << k << endl;
    cout << "   Minimum cost to merge: " << RangeDP::mergeStones(stones, k) << endl;

    vector<int> balloons = {3, 1, 5, 8};
    cout << "   Balloons: [3, 1, 5, 8]" << endl;
    cout << "   Maximum coins: " << RangeDP::burstBalloons(balloons) << endl;

    // Profile DP
    cout << "\n6. PROFILE DP:" << endl;
    int gridSize = 5;
    cout << "   Domino tiling 2×" << gridSize << ":" << endl;
    cout << "   Number of ways: " << ProfileDP::dominoTiling2xN(gridSize) << endl;

    int m = 4, gridN = 4;
    cout << "   Domino tiling " << m << "×" << gridN << ":" << endl;
    cout << "   Number of ways: " << ProfileDP::dominoTilingMxN(m, gridN) << endl;

    cout << "\n" << string(70, '=') << endl;

    return 0;
}
