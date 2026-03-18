# 💡 Dynamic Programming

This module collects classic and advanced **dynamic programming (DP)** problems implemented with a focus on clear recurrence relations, multiple optimization strategies, and practical performance trade-offs.

## 🎯 What is Dynamic Programming?

Dynamic Programming (DP) is an algorithmic technique for solving optimization problems by breaking them down into simpler, overlapping subproblems. It is particularly effective for problems exhibiting:

1.  **Overlapping Subproblems**: The problem can be broken down into subproblems which are reused several times.
2.  **Optimal Substructure**: An optimal solution to the problem contains optimal solutions to the subproblems.

Instead of recomputing the same states, DP stores and reuses results via **memoization** (top-down) or **tabulation** (bottom-up), often reducing exponential-time complexity to polynomial-time.

---

## 📂 Implementations in this directory

The implementations are provided in multiple languages, covering core classic problems and advanced competitive programming patterns found in [classic_problems.py](./classic_problems.py) and [advanced_patterns.py](./advanced_patterns.py).

| Problem                           | Category / Pattern    | Core idea (state + transition)                                           |
|-----------------------------------|-----------------------|---------------------------------------------------------------------------|
| Fibonacci numbers                 | 1D DP, linear rec.    | $dp[n] = dp[n-1] + dp[n-2]$ with optional space optimization.           |
| 0/1 Knapsack                      | Knapsack, subset DP   | Max value with capacity constraint using item-by-item transitions.         |
| Longest Common Subsequence (LCS)  | String DP             | Match/mismatch transitions on two indices.                               |
| Coin Change (count / min coins)   | Unbounded knapsack    | Reuse coins across states with order‑independent transitions.             |
| Edit Distance (Levenshtein)       | String edit DP        | Insert / delete / replace operations on prefixes.                        |
| Matrix Chain Multiplication       | Interval DP           | Optimal parenthesization via splitting point $k$.                       |
| Digit DP                          | Counting DP           | Count numbers in range $[L, R]$ with specific digit properties.            |
| Tree DP                           | Graph/Hierarchical DP | Optimal solutions on tree structures (e.g., Max Independent Set).         |
| Bitmask DP                        | Combinatorial DP      | Represent subsets as bitmasks (e.g., Traveling Salesman Problem).         |
| Probability DP                    | Expected Value DP     | Expected number of steps or winning probabilities.                       |
| Profile DP                        | Grid/Tiling DP        | Row-by-row grid filling with bitmask profiles (e.g., Domino Tiling).      |

---

## 🧩 Problem descriptions & categorization

### 1. Fibonacci Numbers
- **Problem**: Compute the $n$-th Fibonacci number efficiently.
- **Category**: 1D DP, linear recurrence.
- **State**: $dp[i]$ = $i$-th Fibonacci number (the value itself).
- **Recurrence**: $dp[i] = dp[i-1] + dp[i-2]$ for $i \ge 2$, with base cases $dp[0]=0, dp[1]=1$.
- **Why DP?**: Naive recursion is $O(\phi^n) \approx O(2^n)$; DP is $O(n)$ time and $O(1)$ space.

### 2. 0/1 Knapsack
- **Problem**: Maximize total value within weight capacity $W$, where each item can be used at most once.
- **Category**: Knapsack, subset selection DP.
- **State** (2D): $dp[i][w]$ = maximum value using a subset of the first $i$ items with total weight exactly $w$ (or $\le w$).
- **Recurrence**:
  - Skip item $i$: $dp[i][w] = dp[i-1][w]$.
  - Take item $i$: $dp[i][w] = \max(dp[i-1][w], dp[i-1][w - w_i] + v_i)$ if $w_i \le w$.
- **Space Optimization**: Can be reduced to $O(W)$ space by traversing the weight $w$ backwards.

### 3. Longest Common Subsequence (LCS)
- **Problem**: Given strings $A$ and $B$, find the length of their longest common subsequence.
- **Category**: 2D string DP.
- **State**: $dp[i][j]$ = length of the LCS of prefixes $A[0..i-1]$ and $B[0..j-1]$.
- **Recurrence**:
  - If $A[i-1] == B[j-1]$, then $dp[i][j] = 1 + dp[i-1][j-1]$.
  - Otherwise, $dp[i][j] = \max(dp[i-1][j], dp[i][j-1])$.

### 4. Coin Change
- **Problem**: Minimum coins needed to make amount $A$ (min) or number of ways to make $A$ (count).
- **Category**: Unbounded knapsack / counting DP.
- **State**: $dp[a]$ = optimal value (min count or total ways) for target amount $a$.
- **Recurrence (Min Coins)**: $dp[a] = \min_{c \in \text{coins}}(dp[a - c] + 1)$.

### 5. Advanced Patterns
- **Digit DP**: Solves counting problems on a range of numbers by processing digits one by one (e.g., "count numbers with digit sum $K$"). State: `(index, is_less, current_sum)`.
- **Tree DP**: Performs DP on a tree structure, often using post-order DFS. State: `dp[u]` depends on `dp[v]` for all children `v` of `u`.
- **Bitmask DP**: Used when we need to track a subset of elements (usually $n \le 20$). State: `dp[mask]` where `mask` is a bitmask representing the subset.

---

## ⏱️ Complexity analysis

Below are typical complexities for standard vs optimized DP implementations included in this module.

| Problem                      | Naive Recursion                      | DP with Memoization                | Space Optimized DP                          |
|-----------------------------|--------------------------------------|------------------------------------|--------------------------------------------|
| Fibonacci                   | $O(2^n)$                             | $O(n)$                             | $O(1)$                                     |
| 0/1 Knapsack                | $O(2^n)$                             | $O(n \cdot W)$                     | $O(W)$                                     |
| LCS                         | $O(2^{n+m})$                         | $O(n \cdot m)$                     | $O(\min(n, m))$                            |
| Edit Distance               | $O(3^{n+m})$                         | $O(n \cdot m)$                     | $O(\min(n, m))$                            |
| Matrix Chain                | $O(\text{Exponential})$              | $O(n^3)$                           | $O(n^2)$                                   |
| TSP (Bitmask)               | $O(n!)$                              | $O(n^2 2^n)$                       | $O(n 2^n)$                                 |

---

## 🧠 Memoization vs tabulation

This directory provides both approaches to highlight their trade-offs:

### Memoization (top‑down)
- **Style**: Starts from the main problem and recursively breaks it down.
- **Storage**: Uses a hash map or array to cache results.
- **Pros**: Only computes subproblems that are actually reachable; often easier to implement from a recursive definition.
- **Cons**: Higher overhead due to function calls; risk of stack overflow on deep recursions.

### Tabulation (bottom‑up)
- **Style**: Solves all subproblems starting from the base cases and builds up to the target.
- **Storage**: Uses an $n$-dimensional array (table).
- **Pros**: No recursion overhead; often allows for simpler space optimizations; better cache performance.
- **Cons**: Computes solutions for all states, even if they aren't part of the optimal path.

---

## 🔗 Related problems & resources

The DP techniques in this directory generalize to many other problems:
- **Longest Increasing Subsequence (LIS)** – 1D prefix DP.
- **Maximum Subarray Sum (Kadane's)** – Simple state-tracking DP.
- **Grid Path Problems** – Moving from $(0,0)$ to $(n,m)$ with constraints.
- [LeetCode DP Study Guide](https://leetcode.com/discuss/study-guide/458695/Dynamic-Programming-Patterns)
- [CP-Algorithms: DP](https://cp-algorithms.com/dynamic_programming/intro.html)
- [MIT 6.006: Dynamic Programming](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/pages/lecture-notes-and-readings/)

---

## ✅ How to extend this module

1.  **State Definition**: Clearly define what $dp[i]$ or $dp[i][j]$ represents.
2.  **Transitions**: Document the recurrence relation in the code comments.
3.  **Cross-Language**: Consider porting the solution to multiple languages (Python, C++, Fortran).
4.  **Tests**: Add a test in `test_dp.py` covering edge cases like empty inputs or large bounds.
