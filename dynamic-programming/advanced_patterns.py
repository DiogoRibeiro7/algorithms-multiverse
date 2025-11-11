"""
Advanced Dynamic Programming Patterns
======================================

A comprehensive guide to advanced DP patterns used in competitive programming
and technical interviews. Each pattern includes detailed explanations, multiple
examples, and optimization techniques.

Patterns covered:
1. Digit DP
2. Tree DP
3. Bitmask DP
4. Probability DP
5. Range DP (Interval DP)
6. Profile DP
"""

from typing import List, Tuple, Dict
from functools import lru_cache


# ============================================================================
# 1. DIGIT DP
# ============================================================================

"""
DIGIT DP PATTERN
================

When to use:
- Count numbers in range [L, R] with specific digit properties
- Numbers with digit sum constraints
- Numbers without certain digits
- Numbers with consecutive digit patterns

Key Concept:
Build numbers digit by digit from left to right, tracking:
- Current position in the number
- Whether we're still bounded by the limit
- Additional state (sum, last digit, etc.)

Common States:
- pos: current position
- tight: whether we're still at the upper bound
- started: whether we've placed a non-zero digit
- state: problem-specific state (sum, count, etc.)
"""


class DigitDP:
    """
    Problem 1: Count numbers in [L, R] with digit sum divisible by K
    """

    @staticmethod
    def count_divisible_digit_sum(left: int, right: int, k: int) -> int:
        """
        Count numbers in [left, right] whose digit sum is divisible by k.

        Time: O(log(right) * k * 2)
        Space: O(log(right) * k * 2)
        """
        def count_up_to(num: int) -> int:
            if num < 0:
                return 0

            digits = [int(d) for d in str(num)]
            n = len(digits)
            memo = {}

            def dp(pos: int, digit_sum: int, tight: bool, started: bool) -> int:
                # Base case
                if pos == n:
                    return 1 if started and digit_sum % k == 0 else 0

                # Memoization
                state = (pos, digit_sum, tight, started)
                if state in memo:
                    return memo[state]

                # Current digit limit
                limit = digits[pos] if tight else 9
                result = 0

                for digit in range(0, limit + 1):
                    # Skip leading zeros
                    new_started = started or (digit > 0)
                    new_sum = (digit_sum + digit) % k if new_started else 0
                    new_tight = tight and (digit == limit)

                    result += dp(pos + 1, new_sum, new_tight, new_started)

                memo[state] = result
                return result

            return dp(0, 0, True, False)

        return count_up_to(right) - count_up_to(left - 1)

    @staticmethod
    def count_without_digit(left: int, right: int, forbidden: int) -> int:
        """
        Count numbers in [left, right] that don't contain digit 'forbidden'.

        Example: count_without_digit(1, 100, 5) counts numbers without digit 5
        """
        def count_up_to(num: int) -> int:
            if num < 0:
                return 0

            digits = [int(d) for d in str(num)]
            n = len(digits)
            memo = {}

            def dp(pos: int, tight: bool, started: bool) -> int:
                if pos == n:
                    return 1 if started else 0

                state = (pos, tight, started)
                if state in memo:
                    return memo[state]

                limit = digits[pos] if tight else 9
                result = 0

                for digit in range(0, limit + 1):
                    # Skip forbidden digit (unless it's leading zero)
                    if digit == forbidden and (started or digit > 0):
                        continue

                    new_started = started or (digit > 0)
                    new_tight = tight and (digit == limit)
                    result += dp(pos + 1, new_tight, new_started)

                memo[state] = result
                return result

            return dp(0, True, False)

        return count_up_to(right) - count_up_to(left - 1)


# ============================================================================
# 2. TREE DP
# ============================================================================

"""
TREE DP PATTERN
===============

When to use:
- Find optimal solutions on tree structures
- Maximum independent set on trees
- Tree diameter, center, centroid problems
- Subtree aggregations

Key Concepts:
- Process tree bottom-up (post-order traversal)
- dp[node][state] represents optimal value for subtree rooted at node
- States often represent: include/exclude node, different subtree configurations

Common Patterns:
- Rerooting technique: compute answer when each node is the root
- Two-pass DP: first down the tree, then up
"""


class TreeDP:
    """
    Problem 1: Maximum Independent Set on Tree
    Find maximum number of non-adjacent nodes
    """

    @staticmethod
    def max_independent_set(edges: List[Tuple[int, int]], n: int) -> int:
        """
        Find maximum independent set (no two adjacent nodes selected).

        Time: O(n)
        Space: O(n)

        State:
        dp[node][0] = max nodes when node is NOT included
        dp[node][1] = max nodes when node IS included
        """
        # Build adjacency list
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        dp = [[0, 0] for _ in range(n)]

        def dfs(node: int, parent: int) -> None:
            dp[node][0] = 0  # Not including current node
            dp[node][1] = 1  # Including current node

            for child in graph[node]:
                if child == parent:
                    continue

                dfs(child, node)

                # If we don't include current node, we can choose max from child
                dp[node][0] += max(dp[child][0], dp[child][1])

                # If we include current node, we can't include children
                dp[node][1] += dp[child][0]

        dfs(0, -1)
        return max(dp[0][0], dp[0][1])

    @staticmethod
    def tree_diameter(edges: List[Tuple[int, int]], n: int) -> int:
        """
        Find the diameter (longest path) in the tree.

        Time: O(n)
        Space: O(n)

        For each node, track:
        - max_depth[node] = longest path going down from node
        - diameter = max over all nodes of (two longest paths from node)
        """
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        diameter = [0]

        def dfs(node: int, parent: int) -> int:
            # Returns the maximum depth from this node
            max_depths = [0, 0]  # Track two longest paths

            for child in graph[node]:
                if child == parent:
                    continue

                child_depth = dfs(child, node) + 1

                # Update two longest paths
                if child_depth > max_depths[0]:
                    max_depths[1] = max_depths[0]
                    max_depths[0] = child_depth
                elif child_depth > max_depths[1]:
                    max_depths[1] = child_depth

            # Diameter through this node
            diameter[0] = max(diameter[0], max_depths[0] + max_depths[1])

            return max_depths[0]

        dfs(0, -1)
        return diameter[0]

    @staticmethod
    def tree_rerooting(edges: List[Tuple[int, int]], n: int) -> List[int]:
        """
        For each node, compute answer when that node is the root.

        Example: For each node, count number of nodes in its subtree.
        This uses the rerooting technique.

        Time: O(n)
        Space: O(n)
        """
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        # First pass: compute for root = 0
        subtree_size = [0] * n

        def dfs1(node: int, parent: int) -> int:
            size = 1
            for child in graph[node]:
                if child != parent:
                    size += dfs1(child, node)
            subtree_size[node] = size
            return size

        dfs1(0, -1)

        # Second pass: reroot and compute for each node
        answer = [0] * n

        def dfs2(node: int, parent: int, parent_contribution: int) -> None:
            # When node is root, answer includes all subtrees + parent contribution
            answer[node] = subtree_size[node] + parent_contribution

            for child in graph[node]:
                if child != parent:
                    # When rerooting to child:
                    # - Remove child's subtree
                    # - Add everything else (including parent)
                    new_parent_contribution = answer[node] - subtree_size[child]
                    dfs2(child, node, new_parent_contribution)

        dfs2(0, -1, 0)
        return answer


# ============================================================================
# 3. BITMASK DP
# ============================================================================

"""
BITMASK DP PATTERN
==================

When to use:
- Small sets (typically n ≤ 20)
- Problems involving subsets, permutations
- Traveling Salesman Problem (TSP)
- Assignment problems
- Covering problems

Key Concepts:
- Represent subsets as bitmasks (integers)
- dp[mask] or dp[mask][i] represents state for subset represented by mask
- Iterate over subsets efficiently

Bit Operations:
- Check if i-th bit is set: mask & (1 << i)
- Set i-th bit: mask | (1 << i)
- Clear i-th bit: mask & ~(1 << i)
- Toggle i-th bit: mask ^ (1 << i)
- Count set bits: bin(mask).count('1') or use bit manipulation
- Iterate over submasks: submask = (submask - 1) & mask
"""


class BitmaskDP:
    """
    Problem 1: Traveling Salesman Problem (TSP)
    """

    @staticmethod
    def tsp(dist: List[List[int]]) -> int:
        """
        Find minimum cost Hamiltonian path starting from city 0.

        Time: O(n^2 * 2^n)
        Space: O(n * 2^n)

        State:
        dp[mask][i] = minimum cost to visit cities in mask, ending at city i
        """
        n = len(dist)
        INF = float('inf')

        # dp[mask][i] = min cost to visit cities in mask, currently at i
        dp = [[INF] * n for _ in range(1 << n)]
        dp[1][0] = 0  # Start at city 0

        for mask in range(1 << n):
            for last in range(n):
                if dp[mask][last] == INF:
                    continue
                if not (mask & (1 << last)):
                    continue

                # Try to go to next city
                for next_city in range(n):
                    if mask & (1 << next_city):
                        continue  # Already visited

                    new_mask = mask | (1 << next_city)
                    dp[new_mask][next_city] = min(
                        dp[new_mask][next_city],
                        dp[mask][last] + dist[last][next_city]
                    )

        # Find minimum cost to visit all cities
        full_mask = (1 << n) - 1
        return min(dp[full_mask])

    @staticmethod
    def assignment_problem(cost: List[List[int]]) -> int:
        """
        Assign n tasks to n people to minimize total cost.

        Time: O(n * 2^n)
        Space: O(2^n)

        State:
        dp[mask] = min cost to assign tasks in mask to first popcount(mask) people
        """
        n = len(cost)
        INF = float('inf')

        dp = [INF] * (1 << n)
        dp[0] = 0

        for mask in range(1 << n):
            if dp[mask] == INF:
                continue

            # Current person is the popcount(mask)-th person
            person = bin(mask).count('1')
            if person >= n:
                continue

            # Try assigning each unassigned task to this person
            for task in range(n):
                if mask & (1 << task):
                    continue  # Task already assigned

                new_mask = mask | (1 << task)
                dp[new_mask] = min(dp[new_mask], dp[mask] + cost[person][task])

        return dp[(1 << n) - 1]

    @staticmethod
    def sum_over_all_subsets(arr: List[int]) -> List[int]:
        """
        For each subset, compute sum of all its subsets.

        This demonstrates the SOS (Sum Over Subsets) DP technique.

        Time: O(n * 2^n)
        Space: O(2^n)
        """
        n = len(arr)

        # dp[mask] = sum of arr[i] for all i in mask
        dp = [0] * (1 << n)

        # Initialize: dp[mask] = arr values for singleton sets
        for mask in range(1 << n):
            for i in range(n):
                if mask & (1 << i):
                    dp[mask] += arr[i]

        # SOS DP: for each mask, sum over all its subsets
        result = [0] * (1 << n)

        for mask in range(1 << n):
            # Iterate over all submasks
            submask = mask
            while True:
                result[mask] += dp[submask]
                if submask == 0:
                    break
                submask = (submask - 1) & mask

        return result

    @staticmethod
    def sos_dp_optimized(arr: List[int]) -> List[int]:
        """
        Optimized SOS DP that iterates in O(n * 2^n) instead of O(3^n).

        For each mask, compute sum of arr[submask] for all submask ⊆ mask.
        """
        n = len(arr)
        dp = arr[:]

        # Iterate over each bit position
        for i in range(n):
            # For each mask, add contribution from masks without i-th bit
            for mask in range(1 << n):
                if mask & (1 << i):
                    dp[mask] += dp[mask ^ (1 << i)]

        return dp


# ============================================================================
# 4. PROBABILITY DP
# ============================================================================

"""
PROBABILITY DP PATTERN
======================

When to use:
- Expected value problems
- Probability calculations with states
- Game theory with randomness
- Markov chains

Key Concepts:
- E[X] = sum of prob(outcome) * value(outcome)
- Work backwards from terminal states
- Be careful with dependencies and conditional probabilities

Common Patterns:
- Expected number of steps to reach goal
- Probability of winning/reaching state
- Expected score/value
"""


class ProbabilityDP:
    """
    Problem 1: Expected number of coin flips to get consecutive heads
    """

    @staticmethod
    def expected_consecutive_heads(n: int) -> float:
        """
        Expected number of coin flips to get n consecutive heads.

        State:
        dp[i] = expected flips to get n heads, starting with i consecutive heads

        Recurrence:
        dp[i] = 1 + 0.5 * dp[i+1] + 0.5 * dp[0]  (for i < n)
        dp[n] = 0 (base case)

        Time: O(n)
        Space: O(n)
        """
        # Solve system of linear equations
        # dp[i] = 1 + 0.5 * dp[i+1] + 0.5 * dp[0]

        dp = [0.0] * (n + 1)

        # Work backwards
        for i in range(n - 1, -1, -1):
            if i == n - 1:
                # dp[n-1] = 1 + 0.5 * 0 + 0.5 * dp[0]
                # dp[n-1] = 1 + 0.5 * dp[0]
                pass
            else:
                dp[i] = 1 + 0.5 * dp[i + 1] + 0.5 * dp[0]

        # Solve for dp[0]
        # dp[0] = 1 + 0.5 * dp[1] + 0.5 * dp[0]
        # 0.5 * dp[0] = 1 + 0.5 * dp[1]
        # dp[0] = 2 + dp[1]

        # Let's compute it iteratively
        dp[n] = 0
        for i in range(n - 1, -1, -1):
            dp[i] = 2 + dp[i + 1]

        return dp[0]

    @staticmethod
    def dice_expected_value(n: int, faces: int = 6) -> float:
        """
        Expected number of rolls to see all n faces on a dice.
        This is the "coupon collector" problem.

        Time: O(n)
        Space: O(1)
        """
        # E[time to get k+1 faces | have k faces] = faces / (faces - k)
        # Total E[time] = sum of faces / (faces - k) for k from 0 to n-1

        expected = 0.0
        for k in range(n):
            expected += faces / (faces - k)

        return expected

    @staticmethod
    def random_walk_1d(start: int, target: int, max_pos: int) -> float:
        """
        1D random walk: probability of reaching target before falling off cliff.

        Position start, want to reach target (target < max_pos).
        Each step: move +1 or -1 with equal probability.
        Fall off if reach 0 or max_pos.

        Time: O(max_pos)
        Space: O(max_pos)
        """
        if start <= 0 or start >= max_pos:
            return 0.0
        if start == target:
            return 1.0

        # dp[i] = probability of reaching target starting from position i
        dp = [0.0] * max_pos
        dp[target] = 1.0

        # Solve system of linear equations
        # dp[i] = 0.5 * dp[i-1] + 0.5 * dp[i+1] for 0 < i < max_pos, i != target

        # This forms a tridiagonal system, but for random walk,
        # we can solve it directly using the linearity property

        # For positions before target
        # dp[i] = i / target for i < target
        for i in range(target):
            dp[i] = i / target

        # For positions after target
        # dp[i] = (max_pos - i) / (max_pos - target) for i > target
        for i in range(target + 1, max_pos):
            dp[i] = (max_pos - i) / (max_pos - target)

        return dp[start]


# ============================================================================
# 5. RANGE DP (INTERVAL DP)
# ============================================================================

"""
RANGE DP (INTERVAL DP) PATTERN
===============================

When to use:
- Problems on contiguous subarrays/substrings
- Optimal parenthesization
- Palindrome problems
- Merging intervals optimally

Key Concepts:
- dp[i][j] = answer for subarray/substring from i to j
- Iterate over increasing lengths
- Try all possible split points

Iteration Pattern:
for length in range(2, n+1):
    for i in range(n - length + 1):
        j = i + length - 1
        for k in range(i, j):  # split point
            dp[i][j] = optimize(dp[i][k], dp[k+1][j])
"""


class RangeDP:
    """
    Problem 1: Minimum cost to merge stones (K-merge variant)
    """

    @staticmethod
    def merge_stones(stones: List[int], k: int) -> int:
        """
        Merge stones in piles of exactly k at a time.
        Each merge costs the sum of stones merged.
        Return minimum cost, or -1 if impossible.

        Time: O(n^3 / k)
        Space: O(n^2)
        """
        n = len(stones)

        # Check if merge is possible
        if (n - 1) % (k - 1) != 0:
            return -1

        # Prefix sums for range sum queries
        prefix = [0]
        for stone in stones:
            prefix.append(prefix[-1] + stone)

        INF = float('inf')

        # dp[i][j][m] = min cost to merge stones[i:j+1] into m piles
        # We only need m = 1 and m = k, so we can optimize space
        dp = [[INF] * n for _ in range(n)]

        # Base case: single pile
        for i in range(n):
            dp[i][i] = 0

        # Iterate over increasing lengths
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1

                # Try all split points
                for mid in range(i, j, k - 1):
                    # Merge [i, mid] and [mid+1, j]
                    # [i, mid] must be merged to 1 pile
                    # [mid+1, j] must form (k-1) piles or be further mergeable
                    dp[i][j] = min(dp[i][j], dp[i][mid] + dp[mid + 1][j])

                # If we can form exactly k piles, merge them into 1
                if (j - i) % (k - 1) == 0:
                    dp[i][j] += prefix[j + 1] - prefix[i]

        return dp[0][n - 1] if dp[0][n - 1] != INF else -1

    @staticmethod
    def burst_balloons(nums: List[int]) -> int:
        """
        Burst balloons to maximize coins.
        When bursting balloon i, gain nums[i-1] * nums[i] * nums[i+1] coins.

        Time: O(n^3)
        Space: O(n^2)

        Key insight: Think about which balloon to burst LAST in range [i, j]
        """
        # Add boundary balloons with value 1
        balloons = [1] + nums + [1]
        n = len(balloons)

        # dp[i][j] = max coins from bursting balloons (i+1) to (j-1)
        dp = [[0] * n for _ in range(n)]

        # Iterate over increasing lengths
        for length in range(2, n):
            for i in range(n - length):
                j = i + length

                # Try bursting each balloon k as the LAST one in range (i, j)
                for k in range(i + 1, j):
                    coins = balloons[i] * balloons[k] * balloons[j]
                    dp[i][j] = max(dp[i][j], dp[i][k] + dp[k][j] + coins)

        return dp[0][n - 1]

    @staticmethod
    def longest_palindromic_subsequence(s: str) -> int:
        """
        Find length of longest palindromic subsequence.

        Time: O(n^2)
        Space: O(n^2)

        This is a classic Range DP problem.
        """
        n = len(s)
        dp = [[0] * n for _ in range(n)]

        # Base case: single characters
        for i in range(n):
            dp[i][i] = 1

        # Iterate over increasing lengths
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1

                if s[i] == s[j]:
                    dp[i][j] = 2 + (dp[i + 1][j - 1] if i + 1 <= j - 1 else 0)
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

        return dp[0][n - 1]


# ============================================================================
# 6. PROFILE DP
# ============================================================================

"""
PROFILE DP PATTERN
==================

When to use:
- Grid problems with complex constraints
- Tiling/covering problems
- Problems where current row depends on previous row
- Broken profile dynamic programming

Key Concepts:
- Process grid row by row (or column by column)
- Use bitmask to represent "profile" of previous row
- Profile indicates which cells extend into current row

Common Applications:
- Domino tiling
- Grid covering with various shapes
- Scheduling on parallel machines
- Network flow with constraints

State:
dp[row][profile] = number of ways to fill up to current row
                   with given profile (which cells are filled)
"""


class ProfileDP:
    """
    Problem 1: Domino Tiling (2×n grid with 1×2 dominoes)
    """

    @staticmethod
    def domino_tiling_2xn(n: int) -> int:
        """
        Count ways to tile 2×n grid with 1×2 dominoes.

        Time: O(n)
        Space: O(1)

        This is actually Fibonacci! But we'll show the profile DP approach.

        Profile has 2 bits (one for each row):
        - 0: cell is empty
        - 1: cell is filled (extends from previous column)
        """
        MOD = 10**9 + 7

        # dp[profile] = ways to reach this column with this profile
        # profile is a 2-bit number
        dp = [0] * 4
        dp[0] = 1  # Start with empty profile

        for col in range(n):
            new_dp = [0] * 4

            for profile in range(4):
                if dp[profile] == 0:
                    continue

                # Try to fill current column
                # We'll use a recursive function to try all valid tilings
                def fill_column(pos: int, curr_profile: int, next_profile: int):
                    if pos == 2:
                        # Successfully filled this column
                        new_dp[next_profile] = (new_dp[next_profile] + dp[profile]) % MOD
                        return

                    if curr_profile & (1 << pos):
                        # Current cell is already filled from previous column
                        fill_column(pos + 1, curr_profile, next_profile)
                    else:
                        # Current cell is empty, we must fill it

                        # Option 1: Place vertical domino (extends to next column)
                        fill_column(pos + 1, curr_profile | (1 << pos), next_profile | (1 << pos))

                        # Option 2: Place horizontal domino (if next position is also empty)
                        if pos + 1 < 2 and not (curr_profile & (1 << (pos + 1))):
                            fill_column(pos + 2, curr_profile | (1 << pos) | (1 << (pos + 1)), next_profile)

                fill_column(0, profile, 0)

            dp = new_dp

        return dp[0]  # Final profile should be empty

    @staticmethod
    def domino_tiling_mxn(m: int, n: int) -> int:
        """
        Count ways to tile m×n grid with 1×2 dominoes.

        Time: O(n * 2^m * 2^m)
        Space: O(2^m)

        More general version using profile DP.
        """
        if (m * n) % 2 == 1:
            return 0  # Impossible to tile odd number of cells

        MOD = 10**9 + 7

        dp = [0] * (1 << m)
        dp[0] = 1

        def generate_next_profile(col: int, row: int, curr_mask: int, next_mask: int, curr_count: int) -> int:
            """Generate all valid ways to fill current column."""
            if row == m:
                return dp[curr_mask] if next_mask == 0 else 0

            result = 0

            if curr_mask & (1 << row):
                # Current cell filled from previous column
                result += generate_next_profile(col, row + 1, curr_mask, next_mask, curr_count)
            else:
                # Place vertical domino
                result += generate_next_profile(col, row + 1, curr_mask | (1 << row), next_mask | (1 << row), curr_count)

                # Place horizontal domino
                if row + 1 < m and not (curr_mask & (1 << (row + 1))):
                    result += generate_next_profile(col, row + 2, curr_mask | (1 << row) | (1 << (row + 1)), next_mask, curr_count)

            return result % MOD

        for col in range(n):
            new_dp = [0] * (1 << m)

            for mask in range(1 << m):
                if dp[mask] == 0:
                    continue

                # Try all valid ways to fill this column
                def fill(row: int, curr: int, nxt: int):
                    if row == m:
                        new_dp[nxt] = (new_dp[nxt] + dp[mask]) % MOD
                        return

                    if curr & (1 << row):
                        fill(row + 1, curr, nxt)
                    else:
                        # Vertical
                        fill(row + 1, curr | (1 << row), nxt | (1 << row))
                        # Horizontal
                        if row + 1 < m and not (curr & (1 << (row + 1))):
                            fill(row + 2, curr | (1 << row) | (1 << (row + 1)), nxt)

                fill(0, mask, 0)

            dp = new_dp

        return dp[0]


# ============================================================================
# COMMON PITFALLS AND DEBUGGING STRATEGIES
# ============================================================================

"""
COMMON PITFALLS:
================

1. Digit DP:
   - Forgetting to handle leading zeros
   - Not tracking 'tight' constraint properly
   - Off-by-one errors in position indexing

2. Tree DP:
   - Forgetting to handle the root specially
   - Not considering all possible states at each node
   - Issues with rerooting (not updating contributions correctly)

3. Bitmask DP:
   - Integer overflow with large bitmasks
   - Incorrect bit manipulation operations
   - Not iterating submasks efficiently (O(3^n) vs O(2^n))

4. Probability DP:
   - Mixing up conditional probabilities
   - Not handling dependencies correctly
   - Numerical precision issues

5. Range DP:
   - Wrong iteration order (must go by increasing length)
   - Not considering all split points
   - Forgetting base cases

6. Profile DP:
   - Not considering all valid transitions
   - Incorrectly tracking filled/empty cells
   - Complexity explosion with large profiles

DEBUGGING STRATEGIES:
=====================

1. Start with small test cases
2. Verify base cases thoroughly
3. Check state transitions manually
4. Use memoization to detect if state space is correct
5. Print intermediate DP values
6. Verify that impossible states are handled
7. Check boundary conditions
8. For optimization problems, verify optimal substructure
"""


# ============================================================================
# EXAMPLE USAGE AND TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ADVANCED DYNAMIC PROGRAMMING PATTERNS - EXAMPLES")
    print("=" * 70)

    # Digit DP Examples
    print("\n1. DIGIT DP:")
    print("   Count numbers in [1, 100] with digit sum divisible by 3:")
    result = DigitDP.count_divisible_digit_sum(1, 100, 3)
    print(f"   Result: {result}")

    print("   Count numbers in [1, 100] without digit 5:")
    result = DigitDP.count_without_digit(1, 100, 5)
    print(f"   Result: {result}")

    # Tree DP Examples
    print("\n2. TREE DP:")
    edges = [(0, 1), (0, 2), (1, 3), (1, 4)]
    n = 5
    print(f"   Tree edges: {edges}")
    print(f"   Maximum independent set: {TreeDP.max_independent_set(edges, n)}")
    print(f"   Tree diameter: {TreeDP.tree_diameter(edges, n)}")

    # Bitmask DP Examples
    print("\n3. BITMASK DP:")
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    print("   TSP distance matrix:")
    for row in dist:
        print(f"   {row}")
    print(f"   Minimum TSP cost: {BitmaskDP.tsp(dist)}")

    cost = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4]
    ]
    print("\n   Assignment problem cost matrix:")
    for row in cost:
        print(f"   {row}")
    print(f"   Minimum assignment cost: {BitmaskDP.assignment_problem(cost)}")

    # Probability DP Examples
    print("\n4. PROBABILITY DP:")
    n = 3
    print(f"   Expected flips for {n} consecutive heads: {ProbabilityDP.expected_consecutive_heads(n):.2f}")
    print(f"   Expected rolls to see all 6 faces: {ProbabilityDP.dice_expected_value(6):.2f}")

    # Range DP Examples
    print("\n5. RANGE DP:")
    stones = [3, 2, 4, 1]
    k = 2
    print(f"   Stones: {stones}, K: {k}")
    print(f"   Minimum cost to merge: {RangeDP.merge_stones(stones, k)}")

    balloons = [3, 1, 5, 8]
    print(f"   Balloons: {balloons}")
    print(f"   Maximum coins: {RangeDP.burst_balloons(balloons)}")

    # Profile DP Examples
    print("\n6. PROFILE DP:")
    n = 5
    print(f"   Domino tiling 2×{n}:")
    print(f"   Number of ways: {ProfileDP.domino_tiling_2xn(n)}")

    m, n = 4, 4
    print(f"   Domino tiling {m}×{n}:")
    print(f"   Number of ways: {ProfileDP.domino_tiling_mxn(m, n)}")

    print("\n" + "=" * 70)
