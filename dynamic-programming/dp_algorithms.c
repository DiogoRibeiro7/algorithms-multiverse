/*
 * Dynamic Programming Algorithms in C
 *
 * Classic DP problems:
 * - Fibonacci Sequence (with memoization and tabulation)
 * - 0/1 Knapsack Problem
 * - Longest Common Subsequence (LCS)
 * - Coin Change Problem
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX 1000

// ===================================================================
// FIBONACCI SEQUENCE
// ===================================================================

// Naive recursive (exponential time)
long long fib_recursive(int n) {
    if (n <= 1) return n;
    return fib_recursive(n - 1) + fib_recursive(n - 2);
}

// Memoization (top-down DP)
long long fib_memo_helper(int n, long long memo[]) {
    if (memo[n] != -1) return memo[n];
    if (n <= 1) return n;

    memo[n] = fib_memo_helper(n - 1, memo) + fib_memo_helper(n - 2, memo);
    return memo[n];
}

long long fib_memo(int n) {
    long long memo[MAX];
    for (int i = 0; i <= n; i++) memo[i] = -1;
    return fib_memo_helper(n, memo);
}

// Tabulation (bottom-up DP)
long long fib_tabulation(int n) {
    if (n <= 1) return n;

    long long dp[MAX];
    dp[0] = 0;
    dp[1] = 1;

    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }

    return dp[n];
}

// Space-optimized
long long fib_optimized(int n) {
    if (n <= 1) return n;

    long long prev2 = 0, prev1 = 1, curr;

    for (int i = 2; i <= n; i++) {
        curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }

    return prev1;
}

// ===================================================================
// 0/1 KNAPSACK PROBLEM
// ===================================================================

int max(int a, int b) {
    return (a > b) ? a : b;
}

int knapsack(int W, int wt[], int val[], int n) {
    int dp[n + 1][W + 1];

    // Build table bottom-up
    for (int i = 0; i <= n; i++) {
        for (int w = 0; w <= W; w++) {
            if (i == 0 || w == 0) {
                dp[i][w] = 0;
            } else if (wt[i - 1] <= w) {
                dp[i][w] = max(val[i - 1] + dp[i - 1][w - wt[i - 1]],
                              dp[i - 1][w]);
            } else {
                dp[i][w] = dp[i - 1][w];
            }
        }
    }

    return dp[n][W];
}

// ===================================================================
// LONGEST COMMON SUBSEQUENCE (LCS)
// ===================================================================

int lcs(char* X, char* Y, int m, int n) {
    int dp[m + 1][n + 1];

    // Build LCS table
    for (int i = 0; i <= m; i++) {
        for (int j = 0; j <= n; j++) {
            if (i == 0 || j == 0) {
                dp[i][j] = 0;
            } else if (X[i - 1] == Y[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    return dp[m][n];
}

// ===================================================================
// COIN CHANGE PROBLEM
// ===================================================================

int coin_change(int coins[], int n, int amount) {
    int dp[amount + 1];

    // Initialize with infinity (large value)
    for (int i = 0; i <= amount; i++) {
        dp[i] = amount + 1;
    }

    dp[0] = 0;  // 0 coins needed for amount 0

    // Build up the dp array
    for (int i = 1; i <= amount; i++) {
        for (int j = 0; j < n; j++) {
            if (coins[j] <= i) {
                dp[i] = (dp[i] < dp[i - coins[j]] + 1) ?
                        dp[i] : (dp[i - coins[j]] + 1);
            }
        }
    }

    return (dp[amount] > amount) ? -1 : dp[amount];
}

// ===================================================================
// MAIN DEMONSTRATION
// ===================================================================

int main() {
    printf("====================================================================\n");
    printf("              DYNAMIC PROGRAMMING ALGORITHMS IN C\n");
    printf("====================================================================\n\n");

    // Test 1: Fibonacci
    printf("Test 1: Fibonacci Sequence\n");
    printf("--------------------------------------------------------------------\n");
    int n = 40;

    printf("Computing Fibonacci(%d) using different methods:\n\n", n);

    // Memoization
    clock_t start = clock();
    long long result = fib_memo(n);
    clock_t end = clock();
    double time_memo = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Memoization (top-down):  F(%d) = %lld (%.6f seconds)\n", n, result, time_memo);

    // Tabulation
    start = clock();
    result = fib_tabulation(n);
    end = clock();
    double time_tab = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Tabulation (bottom-up):  F(%d) = %lld (%.6f seconds)\n", n, result, time_tab);

    // Optimized
    start = clock();
    result = fib_optimized(n);
    end = clock();
    double time_opt = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Space-optimized:         F(%d) = %lld (%.6f seconds)\n", n, result, time_opt);

    printf("\nNote: Naive recursive would take exponential time!\n\n");

    // Test 2: Knapsack
    printf("Test 2: 0/1 Knapsack Problem\n");
    printf("--------------------------------------------------------------------\n");
    int val[] = {60, 100, 120};
    int wt[] = {10, 20, 30};
    int W = 50;
    int n_items = sizeof(val) / sizeof(val[0]);

    printf("Items: {value, weight}\n");
    for (int i = 0; i < n_items; i++) {
        printf("  Item %d: {%d, %d}\n", i + 1, val[i], wt[i]);
    }
    printf("Knapsack capacity: %d\n\n", W);

    int max_value = knapsack(W, wt, val, n_items);
    printf("Maximum value: %d\n\n", max_value);

    // Test 3: LCS
    printf("Test 3: Longest Common Subsequence (LCS)\n");
    printf("--------------------------------------------------------------------\n");
    char X[] = "AGGTAB";
    char Y[] = "GXTXAYB";

    printf("String X: %s\n", X);
    printf("String Y: %s\n", Y);

    int lcs_length = lcs(X, Y, strlen(X), strlen(Y));
    printf("Length of LCS: %d\n", lcs_length);
    printf("(The LCS is \"GTAB\")\n\n");

    // Test 4: Coin Change
    printf("Test 4: Coin Change Problem\n");
    printf("--------------------------------------------------------------------\n");
    int coins[] = {1, 5, 10, 25};
    int n_coins = sizeof(coins) / sizeof(coins[0]);
    int amount = 63;

    printf("Coins: {");
    for (int i = 0; i < n_coins; i++) {
        printf("%d%s", coins[i], (i < n_coins - 1) ? ", " : "");
    }
    printf("}\n");
    printf("Amount: %d\n\n", amount);

    int min_coins = coin_change(coins, n_coins, amount);
    if (min_coins == -1) {
        printf("Cannot make change for this amount\n\n");
    } else {
        printf("Minimum coins needed: %d\n", min_coins);
        printf("(Solution: 2×25 + 1×10 + 3×1 = 6 coins)\n\n");
    }

    // Summary
    printf("====================================================================\n");
    printf("Key Points:\n");
    printf("- Dynamic Programming: Solve complex problems by breaking into subproblems\n");
    printf("- Memoization (top-down): Store results of subproblems as computed\n");
    printf("- Tabulation (bottom-up): Build solutions from smallest subproblems up\n");
    printf("- Space optimization: Often can reduce space complexity\n");
    printf("\n");
    printf("Complexity Analysis:\n");
    printf("- Fibonacci: O(n) time, O(n) space (can be O(1) space)\n");
    printf("- Knapsack: O(nW) time, O(nW) space\n");
    printf("- LCS: O(mn) time, O(mn) space\n");
    printf("- Coin Change: O(n*amount) time, O(amount) space\n");
    printf("====================================================================\n");

    return 0;
}
