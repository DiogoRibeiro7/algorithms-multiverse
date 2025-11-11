/**
 * Advanced Dynamic Programming Patterns
 * ======================================
 *
 * A comprehensive guide to advanced DP patterns used in competitive programming
 * and technical interviews. Each pattern includes detailed explanations, multiple
 * examples, and optimization techniques.
 *
 * Patterns covered:
 * 1. Digit DP
 * 2. Tree DP
 * 3. Bitmask DP
 * 4. Probability DP
 * 5. Range DP (Interval DP)
 * 6. Profile DP
 *
 * Run: node advanced_patterns.js
 */

// ============================================================================
// 1. DIGIT DP
// ============================================================================

/**
 * DIGIT DP PATTERN
 * ================
 *
 * When to use:
 * - Count numbers in range [L, R] with specific digit properties
 * - Numbers with digit sum constraints
 * - Numbers without certain digits
 * - Numbers with consecutive digit patterns
 *
 * Key Concept:
 * Build numbers digit by digit from left to right, tracking:
 * - Current position in the number
 * - Whether we're still bounded by the limit
 * - Additional state (sum, last digit, etc.)
 */

class DigitDP {
    /**
     * Count numbers in [left, right] with digit sum divisible by k
     * Time: O(log(right) * k * 2)
     * Space: O(log(right) * k * 2)
     */
    static countDivisibleDigitSum(left, right, k) {
        function countUpTo(num) {
            if (num < 0) return 0;

            const digits = String(num).split('').map(Number);
            const n = digits.length;
            const memo = new Map();

            function dp(pos, digitSum, tight, started) {
                if (pos === n) {
                    return started && digitSum % k === 0 ? 1 : 0;
                }

                const key = `${pos},${digitSum},${tight},${started}`;
                if (memo.has(key)) {
                    return memo.get(key);
                }

                const limit = tight ? digits[pos] : 9;
                let result = 0;

                for (let digit = 0; digit <= limit; digit++) {
                    const newStarted = started || digit > 0;
                    const newSum = newStarted ? (digitSum + digit) % k : 0;
                    const newTight = tight && digit === limit;

                    result += dp(pos + 1, newSum, newTight, newStarted);
                }

                memo.set(key, result);
                return result;
            }

            return dp(0, 0, true, false);
        }

        return countUpTo(right) - countUpTo(left - 1);
    }

    /**
     * Count numbers in [left, right] without forbidden digit
     */
    static countWithoutDigit(left, right, forbidden) {
        function countUpTo(num) {
            if (num < 0) return 0;

            const digits = String(num).split('').map(Number);
            const n = digits.length;
            const memo = new Map();

            function dp(pos, tight, started) {
                if (pos === n) {
                    return started ? 1 : 0;
                }

                const key = `${pos},${tight},${started}`;
                if (memo.has(key)) {
                    return memo.get(key);
                }

                const limit = tight ? digits[pos] : 9;
                let result = 0;

                for (let digit = 0; digit <= limit; digit++) {
                    if (digit === forbidden && (started || digit > 0)) {
                        continue;
                    }

                    const newStarted = started || digit > 0;
                    const newTight = tight && digit === limit;
                    result += dp(pos + 1, newTight, newStarted);
                }

                memo.set(key, result);
                return result;
            }

            return dp(0, true, false);
        }

        return countUpTo(right) - countUpTo(left - 1);
    }
}

// ============================================================================
// 2. TREE DP
// ============================================================================

/**
 * TREE DP PATTERN
 * ===============
 *
 * When to use:
 * - Find optimal solutions on tree structures
 * - Maximum independent set on trees
 * - Tree diameter, center, centroid problems
 * - Subtree aggregations
 */

class TreeDP {
    /**
     * Maximum Independent Set on Tree
     * Time: O(n), Space: O(n)
     */
    static maxIndependentSet(edges, n) {
        const graph = Array.from({ length: n }, () => []);
        for (const [u, v] of edges) {
            graph[u].push(v);
            graph[v].push(u);
        }

        const dp = Array.from({ length: n }, () => [0, 0]);

        function dfs(node, parent) {
            dp[node][0] = 0; // Not including node
            dp[node][1] = 1; // Including node

            for (const child of graph[node]) {
                if (child === parent) continue;

                dfs(child, node);

                dp[node][0] += Math.max(dp[child][0], dp[child][1]);
                dp[node][1] += dp[child][0];
            }
        }

        dfs(0, -1);
        return Math.max(dp[0][0], dp[0][1]);
    }

    /**
     * Tree Diameter (longest path)
     * Time: O(n), Space: O(n)
     */
    static treeDiameter(edges, n) {
        const graph = Array.from({ length: n }, () => []);
        for (const [u, v] of edges) {
            graph[u].push(v);
            graph[v].push(u);
        }

        let diameter = 0;

        function dfs(node, parent) {
            const maxDepths = [0, 0];

            for (const child of graph[node]) {
                if (child === parent) continue;

                const childDepth = dfs(child, node) + 1;

                if (childDepth > maxDepths[0]) {
                    maxDepths[1] = maxDepths[0];
                    maxDepths[0] = childDepth;
                } else if (childDepth > maxDepths[1]) {
                    maxDepths[1] = childDepth;
                }
            }

            diameter = Math.max(diameter, maxDepths[0] + maxDepths[1]);
            return maxDepths[0];
        }

        dfs(0, -1);
        return diameter;
    }

    /**
     * Tree Rerooting (compute answer for each node as root)
     * Time: O(n), Space: O(n)
     */
    static treeRerooting(edges, n) {
        const graph = Array.from({ length: n }, () => []);
        for (const [u, v] of edges) {
            graph[u].push(v);
            graph[v].push(u);
        }

        const subtreeSize = Array(n).fill(0);
        const answer = Array(n).fill(0);

        function dfs1(node, parent) {
            let size = 1;
            for (const child of graph[node]) {
                if (child !== parent) {
                    size += dfs1(child, node);
                }
            }
            subtreeSize[node] = size;
            return size;
        }

        function dfs2(node, parent, parentContribution) {
            answer[node] = subtreeSize[node] + parentContribution;

            for (const child of graph[node]) {
                if (child !== parent) {
                    const newParentContribution = answer[node] - subtreeSize[child];
                    dfs2(child, node, newParentContribution);
                }
            }
        }

        dfs1(0, -1);
        dfs2(0, -1, 0);
        return answer;
    }
}

// ============================================================================
// 3. BITMASK DP
// ============================================================================

/**
 * BITMASK DP PATTERN
 * ==================
 *
 * When to use:
 * - Small sets (typically n ≤ 20)
 * - Problems involving subsets, permutations
 * - Traveling Salesman Problem (TSP)
 * - Assignment problems
 */

class BitmaskDP {
    /**
     * Traveling Salesman Problem
     * Time: O(n^2 * 2^n), Space: O(n * 2^n)
     */
    static tsp(dist) {
        const n = dist.length;
        const INF = Infinity;

        const dp = Array.from({ length: 1 << n }, () => Array(n).fill(INF));
        dp[1][0] = 0; // Start at city 0

        for (let mask = 0; mask < (1 << n); mask++) {
            for (let last = 0; last < n; last++) {
                if (dp[mask][last] === INF) continue;
                if (!(mask & (1 << last))) continue;

                for (let next = 0; next < n; next++) {
                    if (mask & (1 << next)) continue;

                    const newMask = mask | (1 << next);
                    dp[newMask][next] = Math.min(
                        dp[newMask][next],
                        dp[mask][last] + dist[last][next]
                    );
                }
            }
        }

        const fullMask = (1 << n) - 1;
        return Math.min(...dp[fullMask]);
    }

    /**
     * Assignment Problem
     * Time: O(n * 2^n), Space: O(2^n)
     */
    static assignmentProblem(cost) {
        const n = cost.length;
        const INF = Infinity;

        const dp = Array(1 << n).fill(INF);
        dp[0] = 0;

        for (let mask = 0; mask < (1 << n); mask++) {
            if (dp[mask] === INF) continue;

            const person = this.popcount(mask);
            if (person >= n) continue;

            for (let task = 0; task < n; task++) {
                if (mask & (1 << task)) continue;

                const newMask = mask | (1 << task);
                dp[newMask] = Math.min(dp[newMask], dp[mask] + cost[person][task]);
            }
        }

        return dp[(1 << n) - 1];
    }

    /**
     * Optimized SOS (Sum Over Subsets) DP
     * Time: O(n * 2^n), Space: O(2^n)
     */
    static sosDP(arr) {
        const n = arr.length;
        const dp = [...arr];

        for (let i = 0; i < n; i++) {
            for (let mask = 0; mask < (1 << n); mask++) {
                if (mask & (1 << i)) {
                    dp[mask] += dp[mask ^ (1 << i)];
                }
            }
        }

        return dp;
    }

    static popcount(n) {
        let count = 0;
        while (n) {
            count += n & 1;
            n >>= 1;
        }
        return count;
    }
}

// ============================================================================
// 4. PROBABILITY DP
// ============================================================================

/**
 * PROBABILITY DP PATTERN
 * ======================
 *
 * When to use:
 * - Expected value problems
 * - Probability calculations with states
 * - Game theory with randomness
 */

class ProbabilityDP {
    /**
     * Expected flips for n consecutive heads
     * Time: O(n), Space: O(n)
     */
    static expectedConsecutiveHeads(n) {
        const dp = Array(n + 1).fill(0);

        for (let i = n - 1; i >= 0; i--) {
            dp[i] = 2 + dp[i + 1];
        }

        return dp[0];
    }

    /**
     * Expected rolls to see all n faces (Coupon Collector)
     * Time: O(n), Space: O(1)
     */
    static diceExpectedValue(n, faces = 6) {
        let expected = 0.0;
        for (let k = 0; k < n; k++) {
            expected += faces / (faces - k);
        }
        return expected;
    }

    /**
     * 1D Random Walk - probability of reaching target
     * Time: O(maxPos), Space: O(maxPos)
     */
    static randomWalk1D(start, target, maxPos) {
        if (start <= 0 || start >= maxPos) return 0.0;
        if (start === target) return 1.0;

        const dp = Array(maxPos).fill(0);
        dp[target] = 1.0;

        for (let i = 0; i < target; i++) {
            dp[i] = i / target;
        }

        for (let i = target + 1; i < maxPos; i++) {
            dp[i] = (maxPos - i) / (maxPos - target);
        }

        return dp[start];
    }
}

// ============================================================================
// 5. RANGE DP (INTERVAL DP)
// ============================================================================

/**
 * RANGE DP PATTERN
 * ================
 *
 * When to use:
 * - Problems on contiguous subarrays/substrings
 * - Optimal parenthesization
 * - Merging intervals optimally
 */

class RangeDP {
    /**
     * Merge Stones (K-merge variant)
     * Time: O(n^3 / k), Space: O(n^2)
     */
    static mergeStones(stones, k) {
        const n = stones.length;

        if ((n - 1) % (k - 1) !== 0) {
            return -1;
        }

        const prefix = [0];
        for (const stone of stones) {
            prefix.push(prefix[prefix.length - 1] + stone);
        }

        const INF = Infinity;
        const dp = Array.from({ length: n }, () => Array(n).fill(INF));

        for (let i = 0; i < n; i++) {
            dp[i][i] = 0;
        }

        for (let length = 2; length <= n; length++) {
            for (let i = 0; i <= n - length; i++) {
                const j = i + length - 1;

                for (let mid = i; mid < j; mid += k - 1) {
                    dp[i][j] = Math.min(dp[i][j], dp[i][mid] + dp[mid + 1][j]);
                }

                if ((j - i) % (k - 1) === 0) {
                    dp[i][j] += prefix[j + 1] - prefix[i];
                }
            }
        }

        return dp[0][n - 1] !== INF ? dp[0][n - 1] : -1;
    }

    /**
     * Burst Balloons
     * Time: O(n^3), Space: O(n^2)
     */
    static burstBalloons(nums) {
        const balloons = [1, ...nums, 1];
        const n = balloons.length;

        const dp = Array.from({ length: n }, () => Array(n).fill(0));

        for (let length = 2; length < n; length++) {
            for (let i = 0; i < n - length; i++) {
                const j = i + length;

                for (let k = i + 1; k < j; k++) {
                    const coins = balloons[i] * balloons[k] * balloons[j];
                    dp[i][j] = Math.max(dp[i][j], dp[i][k] + dp[k][j] + coins);
                }
            }
        }

        return dp[0][n - 1];
    }

    /**
     * Longest Palindromic Subsequence
     * Time: O(n^2), Space: O(n^2)
     */
    static longestPalindromicSubsequence(s) {
        const n = s.length;
        const dp = Array.from({ length: n }, () => Array(n).fill(0));

        for (let i = 0; i < n; i++) {
            dp[i][i] = 1;
        }

        for (let length = 2; length <= n; length++) {
            for (let i = 0; i <= n - length; i++) {
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
}

// ============================================================================
// 6. PROFILE DP
// ============================================================================

/**
 * PROFILE DP PATTERN
 * ==================
 *
 * When to use:
 * - Grid problems with complex constraints
 * - Tiling/covering problems
 * - Problems where current row depends on previous row
 */

class ProfileDP {
    /**
     * Domino Tiling (2×n grid)
     * Time: O(n), Space: O(1)
     */
    static dominoTiling2xN(n) {
        const MOD = 1000000007;

        const dp = [0, 0, 0, 0];
        dp[0] = 1;

        for (let col = 0; col < n; col++) {
            const newDp = [0, 0, 0, 0];

            for (let profile = 0; profile < 4; profile++) {
                if (dp[profile] === 0) continue;

                const fill = (pos, curr, next) => {
                    if (pos === 2) {
                        newDp[next] = (newDp[next] + dp[profile]) % MOD;
                        return;
                    }

                    if (curr & (1 << pos)) {
                        fill(pos + 1, curr, next);
                    } else {
                        // Vertical domino
                        fill(pos + 1, curr | (1 << pos), next | (1 << pos));

                        // Horizontal domino
                        if (pos + 1 < 2 && !(curr & (1 << (pos + 1)))) {
                            fill(pos + 2, curr | (1 << pos) | (1 << (pos + 1)), next);
                        }
                    }
                };

                fill(0, profile, 0);
            }

            dp[0] = newDp[0];
            dp[1] = newDp[1];
            dp[2] = newDp[2];
            dp[3] = newDp[3];
        }

        return dp[0];
    }

    /**
     * Domino Tiling (m×n grid)
     * Time: O(n * 2^m * 2^m), Space: O(2^m)
     */
    static dominoTilingMxN(m, n) {
        if ((m * n) % 2 === 1) return 0;

        const MOD = 1000000007;
        let dp = Array(1 << m).fill(0);
        dp[0] = 1;

        for (let col = 0; col < n; col++) {
            const newDp = Array(1 << m).fill(0);

            for (let mask = 0; mask < (1 << m); mask++) {
                if (dp[mask] === 0) continue;

                const fill = (row, curr, nxt) => {
                    if (row === m) {
                        newDp[nxt] = (newDp[nxt] + dp[mask]) % MOD;
                        return;
                    }

                    if (curr & (1 << row)) {
                        fill(row + 1, curr, nxt);
                    } else {
                        // Vertical
                        fill(row + 1, curr | (1 << row), nxt | (1 << row));

                        // Horizontal
                        if (row + 1 < m && !(curr & (1 << (row + 1)))) {
                            fill(row + 2, curr | (1 << row) | (1 << (row + 1)), nxt);
                        }
                    }
                };

                fill(0, mask, 0);
            }

            dp = newDp;
        }

        return dp[0];
    }
}

// ============================================================================
// EXAMPLE USAGE AND TESTING
// ============================================================================

console.log('='.repeat(70));
console.log('ADVANCED DYNAMIC PROGRAMMING PATTERNS - EXAMPLES');
console.log('='.repeat(70));

// Digit DP Examples
console.log('\n1. DIGIT DP:');
console.log('   Count numbers in [1, 100] with digit sum divisible by 3:');
let result = DigitDP.countDivisibleDigitSum(1, 100, 3);
console.log(`   Result: ${result}`);

console.log('   Count numbers in [1, 100] without digit 5:');
result = DigitDP.countWithoutDigit(1, 100, 5);
console.log(`   Result: ${result}`);

// Tree DP Examples
console.log('\n2. TREE DP:');
const edges = [[0, 1], [0, 2], [1, 3], [1, 4]];
const n = 5;
console.log(`   Tree edges: ${JSON.stringify(edges)}`);
console.log(`   Maximum independent set: ${TreeDP.maxIndependentSet(edges, n)}`);
console.log(`   Tree diameter: ${TreeDP.treeDiameter(edges, n)}`);

// Bitmask DP Examples
console.log('\n3. BITMASK DP:');
const dist = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
];
console.log('   TSP distance matrix:');
dist.forEach(row => console.log(`   ${JSON.stringify(row)}`));
console.log(`   Minimum TSP cost: ${BitmaskDP.tsp(dist)}`);

const cost = [
    [9, 2, 7, 8],
    [6, 4, 3, 7],
    [5, 8, 1, 8],
    [7, 6, 9, 4]
];
console.log('\n   Assignment problem cost matrix:');
cost.forEach(row => console.log(`   ${JSON.stringify(row)}`));
console.log(`   Minimum assignment cost: ${BitmaskDP.assignmentProblem(cost)}`);

// Probability DP Examples
console.log('\n4. PROBABILITY DP:');
const numHeads = 3;
console.log(`   Expected flips for ${numHeads} consecutive heads: ${ProbabilityDP.expectedConsecutiveHeads(numHeads).toFixed(2)}`);
console.log(`   Expected rolls to see all 6 faces: ${ProbabilityDP.diceExpectedValue(6).toFixed(2)}`);

// Range DP Examples
console.log('\n5. RANGE DP:');
const stones = [3, 2, 4, 1];
const k = 2;
console.log(`   Stones: ${JSON.stringify(stones)}, K: ${k}`);
console.log(`   Minimum cost to merge: ${RangeDP.mergeStones(stones, k)}`);

const balloons = [3, 1, 5, 8];
console.log(`   Balloons: ${JSON.stringify(balloons)}`);
console.log(`   Maximum coins: ${RangeDP.burstBalloons(balloons)}`);

// Profile DP Examples
console.log('\n6. PROFILE DP:');
const gridSize = 5;
console.log(`   Domino tiling 2×${gridSize}:`);
console.log(`   Number of ways: ${ProfileDP.dominoTiling2xN(gridSize)}`);

const m = 4, gridN = 4;
console.log(`   Domino tiling ${m}×${gridN}:`);
console.log(`   Number of ways: ${ProfileDP.dominoTilingMxN(m, gridN)}`);

console.log('\n' + '='.repeat(70));

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        DigitDP,
        TreeDP,
        BitmaskDP,
        ProbabilityDP,
        RangeDP,
        ProfileDP
    };
}
