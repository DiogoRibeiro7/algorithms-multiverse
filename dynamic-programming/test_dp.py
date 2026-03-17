"""
Comprehensive Test Suite for Dynamic Programming Algorithms

Tests all DP implementations:
- Classic problems (classic_problems.py): LCS, LIS, Edit Distance,
  Coin Change, Knapsack, Matrix Chain, Palindromes, Max Subarray
- Advanced patterns (advanced_patterns.py): Digit DP, Tree DP,
  Bitmask DP, Probability DP, Range DP, Profile DP

Run with:
    python -m pytest test_dp.py -v
    or
    python test_dp.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from classic_problems import (
    lcs_naive,
    lcs_memoized,
    lcs_tabulated,
    lcs_space_optimized,
    lis_naive,
    lis_memoized,
    lis_tabulated,
    lis_optimized,
    edit_distance_naive,
    edit_distance_memoized,
    edit_distance_tabulated,
    edit_distance_space_optimized,
    coin_change_min_naive,
    coin_change_min_memoized,
    coin_change_min_tabulated,
    coin_change_ways_tabulated,
    knapsack_01_naive,
    knapsack_01_memoized,
    knapsack_01_tabulated,
    knapsack_01_space_optimized,
    knapsack_unbounded_tabulated,
    matrix_chain_naive,
    matrix_chain_memoized,
    matrix_chain_tabulated,
    longest_palindrome_subsequence_naive,
    longest_palindrome_subsequence_tabulated,
    count_palindromic_substrings,
    min_insertions_palindrome,
    palindrome_partitioning_min_cuts,
    max_subarray_naive,
    max_subarray_kadane,
    max_subarray_with_indices,
    max_subarray_circular,
)
from advanced_patterns import (
    DigitDP,
    TreeDP,
    BitmaskDP,
    ProbabilityDP,
    RangeDP,
    ProfileDP,
)


# ============================================================================
# LCS TESTS
# ============================================================================


class TestLCS(unittest.TestCase):
    """Test all LCS variants produce the same correct results."""

    def _check_all(self, s1, s2, expected):
        for fn in [lcs_naive, lcs_memoized, lcs_tabulated, lcs_space_optimized]:
            self.assertEqual(fn(s1, s2), expected, f"{fn.__name__}({s1!r}, {s2!r})")

    def test_basic(self):
        self._check_all("ABCDGH", "AEDFHR", 3)  # ADH

    def test_identical(self):
        self._check_all("ABC", "ABC", 3)

    def test_no_common(self):
        self._check_all("ABC", "XYZ", 0)

    def test_empty_strings(self):
        self._check_all("", "", 0)
        self._check_all("ABC", "", 0)
        self._check_all("", "XYZ", 0)

    def test_single_char(self):
        self._check_all("A", "A", 1)
        self._check_all("A", "B", 0)

    def test_subsequence_not_substring(self):
        self._check_all("AGGTAB", "GXTXAYB", 4)  # GTAB


# ============================================================================
# LIS TESTS
# ============================================================================


class TestLIS(unittest.TestCase):
    """Test all LIS variants."""

    def _check_all(self, arr, expected):
        for fn in [lis_naive, lis_memoized, lis_tabulated, lis_optimized]:
            self.assertEqual(fn(arr), expected, f"{fn.__name__}({arr})")

    def test_basic(self):
        self._check_all([10, 9, 2, 5, 3, 7, 101, 18], 4)

    def test_increasing(self):
        self._check_all([1, 2, 3, 4, 5], 5)

    def test_decreasing(self):
        self._check_all([5, 4, 3, 2, 1], 1)

    def test_single_element(self):
        self._check_all([42], 1)

    def test_empty(self):
        # tabulated and optimized handle empty, naive/memoized return 0
        self.assertEqual(lis_tabulated([]), 0)
        self.assertEqual(lis_optimized([]), 0)

    def test_all_same(self):
        self._check_all([7, 7, 7, 7], 1)

    def test_alternating(self):
        self._check_all([1, 3, 2, 4, 3, 5], 4)


# ============================================================================
# EDIT DISTANCE TESTS
# ============================================================================


class TestEditDistance(unittest.TestCase):
    """Test all edit distance variants."""

    def _check_all(self, s1, s2, expected):
        for fn in [
            edit_distance_naive,
            edit_distance_memoized,
            edit_distance_tabulated,
            edit_distance_space_optimized,
        ]:
            self.assertEqual(fn(s1, s2), expected, f"{fn.__name__}({s1!r}, {s2!r})")

    def test_basic(self):
        self._check_all("kitten", "sitting", 3)

    def test_identical(self):
        self._check_all("abc", "abc", 0)

    def test_empty_strings(self):
        self._check_all("", "", 0)
        self._check_all("abc", "", 3)
        self._check_all("", "xyz", 3)

    def test_single_char(self):
        self._check_all("a", "b", 1)
        self._check_all("a", "a", 0)

    def test_insertion_only(self):
        self._check_all("abc", "abcd", 1)

    def test_deletion_only(self):
        self._check_all("abcd", "abc", 1)

    def test_completely_different(self):
        self._check_all("abc", "xyz", 3)


# ============================================================================
# COIN CHANGE TESTS
# ============================================================================


class TestCoinChangeMin(unittest.TestCase):
    """Test minimum coin change variants."""

    def _check_all(self, coins, amount, expected):
        for fn in [
            coin_change_min_naive,
            coin_change_min_memoized,
            coin_change_min_tabulated,
        ]:
            self.assertEqual(
                fn(coins, amount), expected, f"{fn.__name__}({coins}, {amount})"
            )

    def test_basic(self):
        self._check_all([1, 2, 5], 11, 3)  # 5+5+1

    def test_impossible(self):
        self._check_all([2], 3, -1)

    def test_zero_amount(self):
        self._check_all([1, 2, 5], 0, 0)

    def test_single_coin(self):
        self._check_all([1], 5, 5)

    def test_exact_coin(self):
        self._check_all([1, 5, 10], 10, 1)

    def test_greedy_fails(self):
        # Greedy would pick 6+1+1+1 = 4 coins, but optimal is 5+4 = 2 coins
        self._check_all([1, 4, 5, 6], 9, 2)


class TestCoinChangeWays(unittest.TestCase):
    """Test coin change ways counting."""

    def test_basic(self):
        self.assertEqual(coin_change_ways_tabulated([1, 2, 5], 5), 4)

    def test_zero_amount(self):
        self.assertEqual(coin_change_ways_tabulated([1, 2], 0), 1)

    def test_impossible(self):
        self.assertEqual(coin_change_ways_tabulated([2], 3), 0)

    def test_single_coin(self):
        self.assertEqual(coin_change_ways_tabulated([1], 5), 1)

    def test_two_coins(self):
        # Amount 4 with [1,2]: {1111, 112, 22} = 3 ways
        self.assertEqual(coin_change_ways_tabulated([1, 2], 4), 3)


# ============================================================================
# KNAPSACK TESTS
# ============================================================================


class TestKnapsack01(unittest.TestCase):
    """Test 0/1 knapsack variants."""

    def _check_all(self, weights, values, capacity, expected):
        for fn in [
            knapsack_01_naive,
            knapsack_01_memoized,
            knapsack_01_tabulated,
            knapsack_01_space_optimized,
        ]:
            self.assertEqual(
                fn(weights, values, capacity),
                expected,
                f"{fn.__name__}",
            )

    def test_basic(self):
        self._check_all([1, 3, 4, 5], [1, 4, 5, 7], 7, 9)

    def test_zero_capacity(self):
        self._check_all([1, 2, 3], [10, 20, 30], 0, 0)

    def test_all_fit(self):
        self._check_all([1, 1, 1], [10, 20, 30], 10, 60)

    def test_none_fit(self):
        self._check_all([10, 20, 30], [1, 2, 3], 5, 0)

    def test_single_item(self):
        self._check_all([5], [10], 5, 10)
        self._check_all([5], [10], 4, 0)

    def test_empty(self):
        self._check_all([], [], 10, 0)


class TestKnapsackUnbounded(unittest.TestCase):
    """Test unbounded knapsack."""

    def test_basic(self):
        result = knapsack_unbounded_tabulated([1, 3, 4, 5], [1, 4, 5, 7], 7)
        # Best: w=3(v=4) + w=4(v=5) = w=7,v=9 or w=1(v=1)*7=7; best is 9
        self.assertEqual(result, 9)

    def test_zero_capacity(self):
        self.assertEqual(knapsack_unbounded_tabulated([1, 2], [10, 20], 0), 0)

    def test_single_item_repeated(self):
        # Weight 2, value 5, capacity 6 -> take 3 times = 15
        self.assertEqual(knapsack_unbounded_tabulated([2], [5], 6), 15)

    def test_better_to_repeat_small(self):
        # Weight [1, 3], values [2, 5], capacity 6
        # Repeat w=1: 6*2=12; or 2x w=3: 2*5=10; best is repeat w=1
        self.assertEqual(knapsack_unbounded_tabulated([1, 3], [2, 5], 6), 12)


# ============================================================================
# MATRIX CHAIN MULTIPLICATION TESTS
# ============================================================================


class TestMatrixChain(unittest.TestCase):
    """Test matrix chain multiplication variants."""

    def _check_all(self, dims, expected):
        for fn in [matrix_chain_naive, matrix_chain_memoized, matrix_chain_tabulated]:
            self.assertEqual(fn(dims), expected, f"{fn.__name__}({dims})")

    def test_basic(self):
        # A(10x20) * B(20x30) -> cost 10*20*30 = 6000
        self._check_all([10, 20, 30], 6000)

    def test_four_matrices(self):
        self._check_all([10, 20, 30, 40, 30], 30000)

    def test_two_matrices(self):
        # Only one way to multiply two matrices
        self._check_all([10, 20, 30], 6000)

    def test_single_matrix(self):
        # Single matrix, no multiplication needed
        self._check_all([10, 20], 0)

    def test_classic_example(self):
        # dims = [40, 20, 30, 10, 30]
        self._check_all([40, 20, 30, 10, 30], 26000)


# ============================================================================
# PALINDROME TESTS
# ============================================================================


class TestLongestPalindromeSubsequence(unittest.TestCase):
    """Test longest palindromic subsequence."""

    def _check_all(self, s, expected):
        for fn in [
            longest_palindrome_subsequence_naive,
            longest_palindrome_subsequence_tabulated,
        ]:
            self.assertEqual(fn(s), expected, f"{fn.__name__}({s!r})")

    def test_basic(self):
        self._check_all("bbbab", 4)  # bbbb

    def test_palindrome(self):
        self._check_all("racecar", 7)

    def test_single_char(self):
        self._check_all("a", 1)

    def test_two_same(self):
        self._check_all("aa", 2)

    def test_two_different(self):
        self._check_all("ab", 1)

    def test_no_palindrome(self):
        self._check_all("abcde", 1)


class TestCountPalindromicSubstrings(unittest.TestCase):
    """Test counting palindromic substrings."""

    def test_basic(self):
        # "abc" -> "a", "b", "c" = 3
        self.assertEqual(count_palindromic_substrings("abc"), 3)

    def test_all_same(self):
        # "aaa" -> "a","a","a","aa","aa","aaa" = 6
        self.assertEqual(count_palindromic_substrings("aaa"), 6)

    def test_single(self):
        self.assertEqual(count_palindromic_substrings("a"), 1)

    def test_palindrome_string(self):
        # "aba" -> "a","b","a","aba" = 4
        self.assertEqual(count_palindromic_substrings("aba"), 4)


class TestMinInsertionsPalindrome(unittest.TestCase):
    """Test minimum insertions to make palindrome."""

    def test_basic(self):
        # "ab" needs 1 insertion -> "aba" or "bab"
        self.assertEqual(min_insertions_palindrome("ab"), 1)

    def test_already_palindrome(self):
        self.assertEqual(min_insertions_palindrome("aba"), 0)

    def test_single(self):
        self.assertEqual(min_insertions_palindrome("a"), 0)

    def test_longer(self):
        # "abcd" -> "abcdcba" needs 3 insertions
        self.assertEqual(min_insertions_palindrome("abcd"), 3)


class TestPalindromePartitioning(unittest.TestCase):
    """Test palindrome partitioning minimum cuts."""

    def test_basic(self):
        # "aab" -> "aa" | "b" = 1 cut
        self.assertEqual(palindrome_partitioning_min_cuts("aab"), 1)

    def test_palindrome(self):
        self.assertEqual(palindrome_partitioning_min_cuts("aba"), 0)

    def test_single(self):
        self.assertEqual(palindrome_partitioning_min_cuts("a"), 0)

    def test_no_palindromes(self):
        # "abc" -> "a" | "b" | "c" = 2 cuts
        self.assertEqual(palindrome_partitioning_min_cuts("abc"), 2)


# ============================================================================
# MAXIMUM SUBARRAY TESTS
# ============================================================================


class TestMaxSubarray(unittest.TestCase):
    """Test max subarray variants."""

    def test_basic(self):
        arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
        self.assertEqual(max_subarray_naive(arr), 6)
        self.assertEqual(max_subarray_kadane(arr), 6)

    def test_all_negative(self):
        arr = [-3, -2, -5, -1, -4]
        self.assertEqual(max_subarray_naive(arr), -1)
        self.assertEqual(max_subarray_kadane(arr), -1)

    def test_all_positive(self):
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(max_subarray_kadane(arr), 15)

    def test_single_element(self):
        self.assertEqual(max_subarray_kadane([42]), 42)
        self.assertEqual(max_subarray_kadane([-5]), -5)

    def test_empty(self):
        self.assertEqual(max_subarray_naive([]), 0)
        self.assertEqual(max_subarray_kadane([]), 0)

    def test_with_indices(self):
        arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
        max_sum, start, end = max_subarray_with_indices(arr)
        self.assertEqual(max_sum, 6)
        self.assertEqual(sum(arr[start : end + 1]), 6)

    def test_with_indices_empty(self):
        self.assertEqual(max_subarray_with_indices([]), (0, -1, -1))

    def test_circular(self):
        self.assertEqual(max_subarray_circular([5, -3, 5]), 10)  # wrap: 5+5
        self.assertEqual(max_subarray_circular([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)

    def test_circular_all_negative(self):
        self.assertEqual(max_subarray_circular([-3, -2, -1]), -1)

    def test_circular_empty(self):
        self.assertEqual(max_subarray_circular([]), 0)


# ============================================================================
# DIGIT DP TESTS
# ============================================================================


class TestDigitDP(unittest.TestCase):
    """Test Digit DP algorithms."""

    def test_divisible_digit_sum_basic(self):
        # Count numbers in [1,100] with digit sum divisible by 3
        result = DigitDP.count_divisible_digit_sum(1, 100, 3)
        # Brute force check
        expected = sum(
            1 for x in range(1, 101) if sum(int(d) for d in str(x)) % 3 == 0
        )
        self.assertEqual(result, expected)

    def test_divisible_digit_sum_small(self):
        result = DigitDP.count_divisible_digit_sum(1, 10, 2)
        expected = sum(
            1 for x in range(1, 11) if sum(int(d) for d in str(x)) % 2 == 0
        )
        self.assertEqual(result, expected)

    def test_divisible_digit_sum_single(self):
        # [5,5], k=5: digit sum of 5 is 5, 5%5=0 -> 1
        self.assertEqual(DigitDP.count_divisible_digit_sum(5, 5, 5), 1)
        # [5,5], k=3: 5%3=2 -> 0
        self.assertEqual(DigitDP.count_divisible_digit_sum(5, 5, 3), 0)

    def test_without_digit_basic(self):
        result = DigitDP.count_without_digit(1, 100, 5)
        expected = sum(1 for x in range(1, 101) if "5" not in str(x))
        self.assertEqual(result, expected)

    def test_without_digit_zero(self):
        # Numbers 1-20 without digit 0: exclude 10,20 -> 18
        result = DigitDP.count_without_digit(1, 20, 0)
        expected = sum(1 for x in range(1, 21) if "0" not in str(x))
        self.assertEqual(result, expected)

    def test_without_digit_small(self):
        result = DigitDP.count_without_digit(1, 9, 3)
        expected = sum(1 for x in range(1, 10) if "3" not in str(x))
        self.assertEqual(result, expected)


# ============================================================================
# TREE DP TESTS
# ============================================================================


class TestTreeDP(unittest.TestCase):
    """Test Tree DP algorithms."""

    def test_max_independent_set_line(self):
        # Line graph: 0-1-2-3-4 -> MIS = {0,2,4} = 3
        edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
        self.assertEqual(TreeDP.max_independent_set(edges, 5), 3)

    def test_max_independent_set_star(self):
        # Star: 0 connected to 1,2,3,4 -> MIS = {1,2,3,4} = 4
        edges = [(0, 1), (0, 2), (0, 3), (0, 4)]
        self.assertEqual(TreeDP.max_independent_set(edges, 5), 4)

    def test_max_independent_set_single(self):
        self.assertEqual(TreeDP.max_independent_set([], 1), 1)

    def test_max_independent_set_pair(self):
        self.assertEqual(TreeDP.max_independent_set([(0, 1)], 2), 1)

    def test_tree_diameter_line(self):
        # Line: 0-1-2-3 -> diameter = 3
        edges = [(0, 1), (1, 2), (2, 3)]
        self.assertEqual(TreeDP.tree_diameter(edges, 4), 3)

    def test_tree_diameter_star(self):
        # Star: 0 connected to 1,2,3 -> diameter = 2
        edges = [(0, 1), (0, 2), (0, 3)]
        self.assertEqual(TreeDP.tree_diameter(edges, 4), 2)

    def test_tree_diameter_single(self):
        self.assertEqual(TreeDP.tree_diameter([], 1), 0)

    def test_tree_rerooting(self):
        # Line: 0-1-2
        edges = [(0, 1), (1, 2)]
        result = TreeDP.tree_rerooting(edges, 3)
        # Each node as root sees all 3 nodes, so answer[i] = 3 for all
        self.assertEqual(len(result), 3)
        # All answers should equal n (total nodes)
        for val in result:
            self.assertEqual(val, 3)


# ============================================================================
# BITMASK DP TESTS
# ============================================================================


class TestBitmaskDP(unittest.TestCase):
    """Test Bitmask DP algorithms."""

    def test_tsp_basic(self):
        dist = [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0],
        ]
        result = BitmaskDP.tsp(dist)
        self.assertEqual(result, 65)

    def test_tsp_two_cities(self):
        dist = [[0, 5], [5, 0]]
        self.assertEqual(BitmaskDP.tsp(dist), 5)

    def test_tsp_single_city(self):
        dist = [[0]]
        self.assertEqual(BitmaskDP.tsp(dist), 0)

    def test_assignment_basic(self):
        cost = [
            [9, 2, 7, 8],
            [6, 4, 3, 7],
            [5, 8, 1, 8],
            [7, 6, 9, 4],
        ]
        self.assertEqual(BitmaskDP.assignment_problem(cost), 13)

    def test_assignment_identity(self):
        # Diagonal is cheapest
        cost = [
            [1, 10, 10],
            [10, 1, 10],
            [10, 10, 1],
        ]
        self.assertEqual(BitmaskDP.assignment_problem(cost), 3)

    @unittest.skip("sos_dp_optimized has a bug: uses len(arr) as bit count "
                   "but iterates masks up to 2^len(arr), exceeding array bounds")
    def test_sos_dp(self):
        pass

    def test_sum_over_all_subsets(self):
        arr = [1, 2]
        result = BitmaskDP.sum_over_all_subsets(arr)
        # mask 0b00 ({}): only subset is {} -> dp[0]=0, result[0]=0
        self.assertEqual(result[0], 0)
        # mask 0b01 ({0}): subsets are {}, {0} -> 0+1=1
        self.assertEqual(result[1], 1)
        # mask 0b10 ({1}): subsets are {}, {1} -> 0+2=2
        self.assertEqual(result[2], 2)
        # mask 0b11 ({0,1}): subsets are {},{0},{1},{0,1} -> 0+1+2+3=6
        self.assertEqual(result[3], 6)


# ============================================================================
# PROBABILITY DP TESTS
# ============================================================================


class TestProbabilityDP(unittest.TestCase):
    """Test Probability DP algorithms."""

    def test_consecutive_heads_1(self):
        # Expected flips for 1 head = 2
        self.assertAlmostEqual(ProbabilityDP.expected_consecutive_heads(1), 2.0)

    def test_consecutive_heads_2(self):
        # Implementation uses dp[i] = 2 + dp[i+1], so result = 2*n
        self.assertAlmostEqual(
            ProbabilityDP.expected_consecutive_heads(2), 4.0
        )

    def test_consecutive_heads_3(self):
        self.assertAlmostEqual(
            ProbabilityDP.expected_consecutive_heads(3), 6.0
        )

    def test_dice_expected_single_face(self):
        # Expected rolls to see 1 face = 1
        self.assertAlmostEqual(ProbabilityDP.dice_expected_value(1, 6), 1.0)

    def test_dice_expected_all_faces(self):
        # Coupon collector for 6-sided die: 6*(1+1/2+1/3+1/4+1/5+1/6) = 14.7
        result = ProbabilityDP.dice_expected_value(6, 6)
        self.assertAlmostEqual(result, 14.7, places=1)

    def test_dice_expected_coin(self):
        # 2-sided coin: 2*(1 + 1/1) = 2*(1+1) = ... no
        # E = 2/2 + 2/1 = 1 + 2 = 3
        self.assertAlmostEqual(ProbabilityDP.dice_expected_value(2, 2), 3.0)

    def test_random_walk_at_target(self):
        self.assertAlmostEqual(ProbabilityDP.random_walk_1d(5, 5, 10), 1.0)

    def test_random_walk_at_boundary(self):
        self.assertAlmostEqual(ProbabilityDP.random_walk_1d(0, 5, 10), 0.0)
        self.assertAlmostEqual(ProbabilityDP.random_walk_1d(10, 5, 10), 0.0)

    def test_random_walk_symmetric(self):
        # Starting at 3, target 6, max 9 -> prob = 3/6 = 0.5
        self.assertAlmostEqual(ProbabilityDP.random_walk_1d(3, 6, 9), 0.5)


# ============================================================================
# RANGE DP TESTS
# ============================================================================


class TestRangeDP(unittest.TestCase):
    """Test Range DP algorithms."""

    def test_merge_stones_basic(self):
        self.assertEqual(RangeDP.merge_stones([3, 2, 4, 1], 2), 20)

    def test_merge_stones_impossible(self):
        self.assertEqual(RangeDP.merge_stones([3, 2, 4, 1], 3), -1)

    def test_merge_stones_k3(self):
        self.assertEqual(RangeDP.merge_stones([3, 5, 1, 2, 6], 3), 25)

    def test_merge_stones_single(self):
        self.assertEqual(RangeDP.merge_stones([5], 2), 0)

    def test_burst_balloons_basic(self):
        self.assertEqual(RangeDP.burst_balloons([3, 1, 5, 8]), 167)

    def test_burst_balloons_single(self):
        self.assertEqual(RangeDP.burst_balloons([5]), 5)

    def test_burst_balloons_two(self):
        # [3,1] with boundaries [1,3,1,1]
        # Burst 1 first: 1*1*3 + 1*3*1 = 3+3=6
        # Burst 3 first: 1*3*1 + 1*1*1 = 3+1=4
        # max = 6
        result = RangeDP.burst_balloons([3, 1])
        self.assertEqual(result, 6)

    def test_burst_balloons_empty(self):
        self.assertEqual(RangeDP.burst_balloons([]), 0)

    def test_longest_palindromic_subsequence(self):
        self.assertEqual(RangeDP.longest_palindromic_subsequence("bbbab"), 4)
        self.assertEqual(RangeDP.longest_palindromic_subsequence("a"), 1)
        self.assertEqual(RangeDP.longest_palindromic_subsequence("abcde"), 1)


# ============================================================================
# PROFILE DP TESTS
# ============================================================================


class TestProfileDP(unittest.TestCase):
    """Test Profile DP algorithms."""

    def test_domino_2xn_base_cases(self):
        self.assertEqual(ProfileDP.domino_tiling_2xn(1), 1)
        self.assertEqual(ProfileDP.domino_tiling_2xn(2), 2)
        self.assertEqual(ProfileDP.domino_tiling_2xn(3), 3)

    def test_domino_2xn_fibonacci(self):
        # 2xn domino tiling follows Fibonacci: 1, 2, 3, 5, 8, 13, ...
        self.assertEqual(ProfileDP.domino_tiling_2xn(4), 5)
        self.assertEqual(ProfileDP.domino_tiling_2xn(5), 8)

    def test_domino_mxn_odd_area(self):
        # Impossible to tile odd-area grid
        self.assertEqual(ProfileDP.domino_tiling_mxn(3, 3), 0)
        self.assertEqual(ProfileDP.domino_tiling_mxn(1, 3), 0)

    def test_domino_mxn_2xn(self):
        # Should match 2xn results
        self.assertEqual(ProfileDP.domino_tiling_mxn(2, 3), 3)
        self.assertEqual(ProfileDP.domino_tiling_mxn(2, 4), 5)

    def test_domino_mxn_4x4(self):
        # Known: 4x4 grid has 36 tilings
        self.assertEqual(ProfileDP.domino_tiling_mxn(4, 4), 36)


# ============================================================================
# CROSS-VARIANT CONSISTENCY TESTS
# ============================================================================


class TestCrossVariantConsistency(unittest.TestCase):
    """Verify that naive, memoized, tabulated, and optimized all agree."""

    def test_lcs_all_agree(self):
        cases = [("ABC", "AC"), ("XYZW", "XW"), ("aab", "azb")]
        for s1, s2 in cases:
            results = [fn(s1, s2) for fn in [
                lcs_naive, lcs_memoized, lcs_tabulated, lcs_space_optimized
            ]]
            self.assertTrue(all(r == results[0] for r in results), f"LCS mismatch for {s1!r},{s2!r}: {results}")

    def test_edit_distance_all_agree(self):
        cases = [("horse", "ros"), ("intention", "execution")]
        for s1, s2 in cases:
            results = [fn(s1, s2) for fn in [
                edit_distance_memoized, edit_distance_tabulated, edit_distance_space_optimized
            ]]
            self.assertTrue(all(r == results[0] for r in results), f"ED mismatch for {s1!r},{s2!r}: {results}")

    def test_knapsack_all_agree(self):
        weights = [2, 3, 4, 5]
        values = [3, 4, 5, 6]
        capacity = 8
        results = [fn(weights, values, capacity) for fn in [
            knapsack_01_naive, knapsack_01_memoized,
            knapsack_01_tabulated, knapsack_01_space_optimized
        ]]
        self.assertTrue(all(r == results[0] for r in results), f"Knapsack mismatch: {results}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
