# 💡 Dynamic Programming

This module collects classic **dynamic programming (DP)** problems implemented with a focus on clear recurrence relations, multiple optimization strategies, and practical performance trade-offs.

DP is used when a problem shows **overlapping subproblems** and **optimal substructure**: instead of recomputing the same states, we store and reuse them via memoization (top-down) or tabulation (bottom-up).

---

## 📂 Implementations in this directory

The implementations are provided in multiple languages, each covering the core classic problems and advanced patterns.

| Problem                           | Pattern / Category    | Core idea (state + transition)                                           |
|-----------------------------------|-----------------------|---------------------------------------------------------------------------|
| Fibonacci numbers                 | 1D DP, linear rec.    | \(dp[n] = dp[n-1] + dp[n-2]\) with optional space optimization.           |
| 0/1 Knapsack                      | Knapsack, subset DP   | Max value with capacity constraint using item-by-item transitions.         |
| Longest Common Subsequence (LCS)  | String DP             | Match/mismatch transitions on two indices.                               |
| Coin Change (count / min coins)   | Unbounded knapsack    | Reuse coins across states with order‑independent transitions.             |
| Edit Distance (Levenshtein)       | String edit DP        | Insert / delete / replace operations on prefixes.                        |
| Matrix Chain Multiplication       | Interval DP           | Optimal parenthesization via splitting point \(k\).                       |
| (Additional classic problems)     |                      | e.g. LIS, paths in grid, partitioning, depending on language support.    |

### 🌐 Multi-Language Support
- **Python**: [classic_problems.py](./classic_problems.py), [advanced_patterns.py](./advanced_patterns.py)
- **JavaScript**: [classic_problems.js](./classic_problems.js), [advanced_patterns.js](./advanced_patterns.js)
- **C++**: [classic_problems.cpp](./classic_problems.cpp), [advanced_patterns.cpp](./advanced_patterns.cpp)
- **Rust**: [classic_problems.rs](./classic_problems.rs)
- **Go**: [classic_problems.go](./classic_problems.go)
- **Fortran**: [dp_algorithms.f90](./dp_algorithms.f90)
- **Others**: Swift, C, R implementations available in the directory.

You can explore the Fortran-based DP suite described in the [root README.md](../README.md#-dynamic-programming) under **Dynamic Programming**.

---

## 🧩 Problem descriptions & categorization

### 1. Fibonacci Numbers
- **Problem**: Compute the \(n\)-th Fibonacci number efficiently.
- **Category**: 1D DP, linear recurrence.
- **State**: \(dp[i]\) = \(i\)-th Fibonacci number.
- **Transition**: \(dp[i] = dp[i-1] + dp[i-2]\) for \(i \ge 2\).
- **Typical use**: Introductory example to show the cost of naive recursion vs DP.

### 2. 0/1 Knapsack
- **Problem**: Given weights and values of items, maximize total value without exceeding capacity, each item used at most once.
- **Category**: Knapsack, subset selection DP.
- **State** (2D): \(dp[i][w]\) = max value using first \(i\) items with capacity \(w\).
- **Transition**:
  - Skip item \(i\): \(dp[i][w] = dp[i-1][w]\).
  - Take item \(i\): \(dp[i][w] = dp[i-1][w - weight_i] + value_i\) if \(weight_i \le w\).

### 3. Longest Common Subsequence (LCS)
- **Problem**: Given strings \(A\) and \(B\), find length of their longest common subsequence.
- **Category**: 2D string DP.
- **State**: \(dp[i][j]\) = LCS length of prefixes \(A[0..i-1]\) and \(B[0..j-1]\).
- **Transition**:
  - If \(A[i-1] == B[j-1]\): \(dp[i][j] = 1 + dp[i-1][j-1]\).
  - Else: \(dp[i][j] = \max(dp[i-1][j], dp[i][j-1])\).

### 4. Coin Change
Two common variants:
1. **Count ways to make a sum**:
   - **State**: \(dp[amount]\) = number of ways to make `amount`.
   - **Transition**: For each coin value `c`, update \(dp[a]\) using \(dp[a - c]\).
2. **Minimum number of coins**:
   - **State**: \(dp[amount]\) = minimum coins to make `amount` (or \(+\infty\) if impossible).
   - **Transition**: \(dp[a] = \min(dp[a], 1 + dp[a - c])\) over all coins `c`.

**Category**: Unbounded knapsack / counting DP.

### 5. Edit Distance (Levenshtein)
- **Problem**: Minimum number of edits (insert, delete, replace) to convert string \(A\) into \(B\).
- **Category**: 2D string edit DP.
- **State**: \(dp[i][j]\) = minimum edits to convert prefix \(A[0..i-1]\) to \(B[0..j-1]\).
- **Transition**:
  - If characters equal: cost = \(dp[i-1][j-1]\).
  - Else: cost = \(1 + \min(dp[i-1][j]\) delete, \(dp[i][j-1]\) insert, \(dp[i-1][j-1]\) replace\).

### 6. Matrix Chain Multiplication
- **Problem**: Choose parenthesization of a chain of matrices to minimize scalar multiplications.
- **Category**: Interval DP / range DP.
- **State**: \(dp[i][j]\) = minimum cost to multiply matrices \(i..j\).
- **Transition**: \(dp[i][j] = \min_{i \le k < j} dp[i][k] + dp[k+1][j] + cost(i,k,j)\).

---

## ⏱️ Complexity analysis

Below are typical complexities for the standard and optimized DP formulations implemented in this module.

| Problem                      | Baseline (no DP)                     | DP with memoization                | DP with tabulation / optimizations          |
|-----------------------------|--------------------------------------|------------------------------------|--------------------------------------------|
| Fibonacci                   | Exponential time, \(O(2^n)\)         | \(O(n)\) time, \(O(n)\) space      | \(O(n)\) time, \(O(1)\) space (2 vars).   |
| 0/1 Knapsack                | Exponential subsets, \(O(2^n)\)      | \(O(n \cdot W)\) time, \(O(n \cdot W)\) space | \(O(n \cdot W)\) time, \(O(W)\) space via 1D DP. |
| LCS                         | Exponential backtracking             | \(O(n \cdot m)\) time, \(O(n \cdot m)\) space | Can be reduced to \(O(\min(n,m))\) space. |
| Coin Change (count / min)   | Exponential recursive search         | \(O(N \cdot A)\) time, \(O(A)\) or \(O(N \cdot A)\) space | Iterative tabulation; often 1D \(O(A)\) space. |
| Edit Distance               | Exponential naive recursion          | \(O(n \cdot m)\) time, \(O(n \cdot m)\) space | Space‑optimized \(O(\min(n,m))\).         |
| Matrix Chain Multiplication | Exponential number of parenthesizations | \(O(n^3)\) time, \(O(n^2)\) space | Some special cases admit faster solutions. |

Here `n`, `m` are string lengths, `W` is knapsack capacity, `A` is target amount, and `N` is number of coins/items.

---

## 🧠 Memoization vs tabulation

This directory provides **at least one memoized** and **one tabulated** version for the core problems to illustrate trade‑offs.

### Memoization (top-down)
- Start from the original problem and use recursion.
- Cache each subproblem result (e.g. with a dictionary/array).
- Only compute states that are actually reachable.
- **Pros**: Natural mapping from recursive definition to code, easy to derive from brute force.
- **Cons**: Recursion depth limits, overhead of function calls, harder to control iteration order.

### Tabulation (bottom-up)
- Define a table of all relevant states.
- Fill the table in an order that guarantees dependencies are computed first.
- Usually iterates with explicit loops and avoids recursion.
- **Pros**: No recursion overhead, often easier to optimize and reason about memory layout, friendlier to cache and vectorization (especially in Fortran implementations).
- **Cons**: May fill states that are never used; requires explicit ordering of transitions.

**Rule of thumb** used in this module:
- Start with memoization when exploring a new recurrence.
- Move to tabulation (and possibly space optimization) for production-grade and performance-critical implementations.

---

## 🔗 Related problems & further reading

The DP techniques in this directory generalize to many other problems, such as:
- **Longest Increasing Subsequence (LIS)** – 1D DP on prefixes.
- **Path counting / minimum path sum in grid** – 2D grid DP.
- **Partition problems (subset sum, equal partition)** – knapsack-style state definitions.
- **Scheduling and interval DP** – weighted interval scheduling, segment DP.

You can also connect these implementations with:
- Root [README.md](../README.md#-dynamic-programming) section **Dynamic Programming** for a high-level overview.
- [COMPLEXITY_GUIDE.md](../COMPLEXITY_GUIDE.md) for general rules on time and space complexity notation.

---

## ✅ How to extend this module

When adding a new dynamic programming algorithm:
1. **Define the state clearly** (what does `dp[i]` / `dp[i][j]` mean).
2. **Write the recurrence** on paper before coding.
3. **Choose memoization or tabulation**, following the patterns above.
4. **Document complexity** in terms of input parameters.
5. **Add tests** covering edge cases (empty input, minimal sizes, large bounds).

This keeps the DP directory aligned with the repository-wide documentation and quality standards.
