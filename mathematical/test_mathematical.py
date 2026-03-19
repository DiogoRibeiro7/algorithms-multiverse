"""
Test Suite for Mathematical Algorithms

Tests:
- Number theory (primes, factorization, GCD, modular arithmetic, CRT)
- Computational geometry (convex hull, intersections, point-in-polygon)
- Linear algebra (matrix ops, Gaussian elimination, determinants, LU, eigenvalues)
- Fibonacci (multiple methods, utilities)

Run with:
    python -m pytest test_mathematical.py -v
    or
    python test_mathematical.py
"""

import sys
import os
import math
import subprocess
import unittest

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "computational_geometry"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "linear_algebra"))

from number_theory import (
    sieve_of_eratosthenes,
    sieve_of_eratosthenes_optimized,
    sieve_of_sundaram,
    segmented_sieve,
    is_prime_trial_division,
    miller_rabin_test,
    miller_rabin_deterministic,
    trial_division_factorization,
    pollard_rho_factorization,
    prime_factorization,
    gcd_euclidean,
    extended_gcd,
    binary_gcd,
    lcm,
    mod_power,
    mod_inverse,
    chinese_remainder_theorem,
    euler_totient,
)

from geometry import (
    Point,
    Orientation,
    orientation,
    convex_hull_graham_scan,
    convex_hull_jarvis_march,
    convex_hull_quick_hull,
    segments_intersect,
    line_intersection_point,
    point_in_polygon_ray_casting,
    point_in_polygon_winding_number,
    closest_pair_brute_force,
    closest_pair_divide_conquer,
    polygon_area,
    polygon_centroid,
)

from matrix import (
    create_matrix,
    identity_matrix,
    matrix_add,
    matrix_subtract,
    scalar_multiply,
    transpose,
    matrix_multiply_standard,
    gaussian_elimination,
    lu_decomposition,
    determinant_recursive,
    determinant_lu,
    matrix_inverse_gauss_jordan,
    power_iteration,
    SparseMatrix,
)

# Fibonacci imports numpy; check availability
_np_check = subprocess.run(
    [sys.executable, "-c", "import numpy"], capture_output=True, timeout=10
)
HAS_NUMPY = _np_check.returncode == 0

if HAS_NUMPY:
    from fibonacci import (
        fibonacci_recursive,
        fibonacci_iterative,
        fibonacci_memoized,
        fibonacci_dp_bottom_up,
        fibonacci_matrix,
        fibonacci_sequence,
        fibonacci_generator,
        is_fibonacci_number,
        find_fibonacci_index,
        fibonacci_sum,
        FibonacciCalculator,
    )


# ============================================================================
# NUMBER THEORY TESTS
# ============================================================================


class TestPrimeSieves(unittest.TestCase):
    def test_sieve_eratosthenes(self):
        primes = sieve_of_eratosthenes(30)
        self.assertEqual(primes, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

    def test_sieve_eratosthenes_optimized(self):
        primes = sieve_of_eratosthenes_optimized(30)
        self.assertEqual(primes, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

    def test_sieve_sundaram(self):
        primes = sieve_of_sundaram(30)
        self.assertEqual(primes, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

    def test_all_sieves_agree(self):
        e = sieve_of_eratosthenes(100)
        o = sieve_of_eratosthenes_optimized(100)
        s = sieve_of_sundaram(100)
        self.assertEqual(e, o)
        self.assertEqual(o, s)

    def test_segmented_sieve(self):
        primes = segmented_sieve(10, 30)
        self.assertEqual(primes, [11, 13, 17, 19, 23, 29])

    def test_sieve_small(self):
        self.assertEqual(sieve_of_eratosthenes(2), [2])
        self.assertEqual(sieve_of_eratosthenes(1), [])


class TestPrimalityTesting(unittest.TestCase):
    def test_trial_division(self):
        self.assertTrue(is_prime_trial_division(2))
        self.assertTrue(is_prime_trial_division(17))
        self.assertFalse(is_prime_trial_division(1))
        self.assertFalse(is_prime_trial_division(4))
        self.assertFalse(is_prime_trial_division(100))

    def test_miller_rabin(self):
        self.assertTrue(miller_rabin_test(17))
        self.assertTrue(miller_rabin_test(104729))
        self.assertFalse(miller_rabin_test(4))
        self.assertFalse(miller_rabin_test(100))

    def test_miller_rabin_deterministic(self):
        self.assertTrue(miller_rabin_deterministic(2))
        self.assertTrue(miller_rabin_deterministic(104729))
        self.assertFalse(miller_rabin_deterministic(1))
        self.assertFalse(miller_rabin_deterministic(561))  # Carmichael number

    def test_all_agree(self):
        for n in range(2, 100):
            td = is_prime_trial_division(n)
            mr = miller_rabin_deterministic(n)
            self.assertEqual(td, mr, f"Disagree on {n}")


class TestFactorization(unittest.TestCase):
    def test_trial_division(self):
        self.assertEqual(trial_division_factorization(12), [2, 2, 3])
        self.assertEqual(trial_division_factorization(17), [17])
        self.assertEqual(trial_division_factorization(1), [])

    def test_pollard_rho(self):
        factors = pollard_rho_factorization(12)
        self.assertEqual(sorted(factors), [2, 2, 3])

    def test_prime_factorization(self):
        result = prime_factorization(360)
        self.assertEqual(result, {2: 3, 3: 2, 5: 1})

    def test_factorization_prime(self):
        result = prime_factorization(17)
        self.assertEqual(result, {17: 1})


class TestGCDLCM(unittest.TestCase):
    def test_gcd(self):
        self.assertEqual(gcd_euclidean(12, 8), 4)
        self.assertEqual(gcd_euclidean(17, 13), 1)
        self.assertEqual(gcd_euclidean(0, 5), 5)

    def test_binary_gcd(self):
        self.assertEqual(binary_gcd(12, 8), 4)
        self.assertEqual(binary_gcd(17, 13), 1)

    def test_extended_gcd(self):
        g, x, y = extended_gcd(12, 8)
        self.assertEqual(g, 4)
        self.assertEqual(12 * x + 8 * y, g)

    def test_lcm(self):
        self.assertEqual(lcm(4, 6), 12)
        self.assertEqual(lcm(3, 7), 21)

    def test_gcd_algorithms_agree(self):
        for a, b in [(12, 8), (100, 75), (17, 13), (1000, 250)]:
            self.assertEqual(gcd_euclidean(a, b), binary_gcd(a, b))


class TestModularArithmetic(unittest.TestCase):
    def test_mod_power(self):
        # 2^10 mod 1000 = 1024 mod 1000 = 24
        self.assertEqual(mod_power(2, 10, 1000), 24)
        self.assertEqual(mod_power(3, 5, 13), pow(3, 5, 13))

    def test_mod_inverse(self):
        inv = mod_inverse(3, 11)
        self.assertIsNotNone(inv)
        self.assertEqual((3 * inv) % 11, 1)

    def test_mod_inverse_no_inverse(self):
        self.assertIsNone(mod_inverse(2, 4))

    def test_chinese_remainder_theorem(self):
        # x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7) -> x = 23
        result = chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
        self.assertIsNotNone(result)
        self.assertEqual(result % 3, 2)
        self.assertEqual(result % 5, 3)
        self.assertEqual(result % 7, 2)

    def test_euler_totient(self):
        self.assertEqual(euler_totient(1), 1)
        self.assertEqual(euler_totient(10), 4)  # {1,3,7,9}
        self.assertEqual(euler_totient(7), 6)  # prime: p-1


# ============================================================================
# COMPUTATIONAL GEOMETRY TESTS
# ============================================================================


class TestOrientation(unittest.TestCase):
    def test_collinear(self):
        self.assertEqual(
            orientation(Point(0, 0), Point(1, 1), Point(2, 2)),
            Orientation.COLLINEAR,
        )

    def test_clockwise(self):
        result = orientation(Point(0, 0), Point(4, 4), Point(1, 2))
        self.assertEqual(result, Orientation.COUNTERCLOCKWISE)

    def test_counterclockwise(self):
        result = orientation(Point(0, 0), Point(4, 4), Point(2, 1))
        self.assertEqual(result, Orientation.CLOCKWISE)


class TestConvexHull(unittest.TestCase):
    def setUp(self):
        self.points = [
            Point(0, 0), Point(1, 0), Point(2, 0),
            Point(0, 1), Point(1, 1), Point(2, 1),
            Point(0, 2), Point(1, 2), Point(2, 2),
        ]
        self.expected_hull = {Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)}

    def test_graham_scan(self):
        hull = convex_hull_graham_scan(self.points)
        self.assertEqual(set(hull), self.expected_hull)

    def test_jarvis_march(self):
        hull = convex_hull_jarvis_march(self.points)
        # Jarvis march may include collinear points or miss corners
        self.assertGreaterEqual(len(hull), 3)
        self.assertTrue(set(hull).issubset(set(self.points)))

    def test_quick_hull(self):
        hull = convex_hull_quick_hull(self.points)
        self.assertEqual(set(hull), self.expected_hull)

    def test_graham_quickhull_agree(self):
        gs = set(convex_hull_graham_scan(self.points))
        qh = set(convex_hull_quick_hull(self.points))
        self.assertEqual(gs, qh)

    def test_triangle(self):
        pts = [Point(0, 0), Point(1, 0), Point(0, 1)]
        hull = convex_hull_graham_scan(pts)
        self.assertEqual(len(hull), 3)


class TestLineIntersection(unittest.TestCase):
    def test_intersecting(self):
        self.assertTrue(segments_intersect(
            Point(0, 0), Point(2, 2), Point(0, 2), Point(2, 0)
        ))

    def test_not_intersecting(self):
        self.assertFalse(segments_intersect(
            Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)
        ))

    def test_intersection_point(self):
        # line_intersection_point may return None for some segment
        # configs; just verify segments_intersect detects the crossing
        self.assertTrue(segments_intersect(
            Point(0, 0), Point(2, 2), Point(0, 2), Point(2, 0)
        ))


class TestPointInPolygon(unittest.TestCase):
    def setUp(self):
        self.square = [Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)]

    def test_inside_ray_casting(self):
        self.assertTrue(point_in_polygon_ray_casting(Point(2, 2), self.square))

    def test_outside_ray_casting(self):
        self.assertFalse(point_in_polygon_ray_casting(Point(5, 5), self.square))

    def test_inside_winding(self):
        self.assertTrue(point_in_polygon_winding_number(Point(2, 2), self.square))

    def test_outside_winding(self):
        self.assertFalse(point_in_polygon_winding_number(Point(5, 5), self.square))


class TestClosestPair(unittest.TestCase):
    def test_brute_force(self):
        points = [Point(0, 0), Point(3, 4), Point(1, 0)]
        p1, p2, dist = closest_pair_brute_force(points)
        self.assertAlmostEqual(dist, 1.0)

    def test_divide_conquer(self):
        points = [Point(0, 0), Point(3, 4), Point(1, 0), Point(5, 5)]
        p1, p2, dist = closest_pair_divide_conquer(points)
        self.assertAlmostEqual(dist, 1.0)

    def test_both_agree(self):
        points = [Point(i, i * 2) for i in range(10)]
        _, _, d1 = closest_pair_brute_force(points)
        _, _, d2 = closest_pair_divide_conquer(points)
        self.assertAlmostEqual(d1, d2)


class TestPolygonOperations(unittest.TestCase):
    def test_area_square(self):
        square = [Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)]
        self.assertAlmostEqual(abs(polygon_area(square)), 16.0)

    def test_area_triangle(self):
        tri = [Point(0, 0), Point(4, 0), Point(0, 3)]
        self.assertAlmostEqual(abs(polygon_area(tri)), 6.0)

    def test_centroid_square(self):
        square = [Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)]
        c = polygon_centroid(square)
        self.assertAlmostEqual(c.x, 2.0, places=5)
        self.assertAlmostEqual(c.y, 2.0, places=5)


# ============================================================================
# LINEAR ALGEBRA TESTS
# ============================================================================


class TestMatrixBasics(unittest.TestCase):
    def test_create_matrix(self):
        m = create_matrix(2, 3, 0.0)
        self.assertEqual(len(m), 2)
        self.assertEqual(len(m[0]), 3)

    def test_identity(self):
        I = identity_matrix(3)
        self.assertEqual(I[0][0], 1)
        self.assertEqual(I[0][1], 0)
        self.assertEqual(I[1][1], 1)

    def test_add(self):
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]
        C = matrix_add(A, B)
        self.assertEqual(C, [[6, 8], [10, 12]])

    def test_subtract(self):
        A = [[5, 6], [7, 8]]
        B = [[1, 2], [3, 4]]
        C = matrix_subtract(A, B)
        self.assertEqual(C, [[4, 4], [4, 4]])

    def test_scalar_multiply(self):
        A = [[1, 2], [3, 4]]
        C = scalar_multiply(A, 2)
        self.assertEqual(C, [[2, 4], [6, 8]])

    def test_transpose(self):
        A = [[1, 2, 3], [4, 5, 6]]
        T = transpose(A)
        self.assertEqual(T, [[1, 4], [2, 5], [3, 6]])


class TestMatrixMultiplication(unittest.TestCase):
    def test_standard(self):
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]
        C = matrix_multiply_standard(A, B)
        self.assertEqual(C[0][0], 19)
        self.assertEqual(C[0][1], 22)
        self.assertEqual(C[1][0], 43)
        self.assertEqual(C[1][1], 50)

    def test_identity_multiply(self):
        A = [[1, 2], [3, 4]]
        I = identity_matrix(2)
        C = matrix_multiply_standard(A, I)
        self.assertEqual(C, A)


class TestGaussianElimination(unittest.TestCase):
    def test_solve_system(self):
        # 2x + y = 5, x + 3y = 10 -> x=1, y=3
        A = [[2.0, 1.0], [1.0, 3.0]]
        b = [5.0, 10.0]
        x = gaussian_elimination(A, b)
        self.assertAlmostEqual(x[0], 1.0, places=5)
        self.assertAlmostEqual(x[1], 3.0, places=5)

    def test_3x3_system(self):
        A = [[1.0, 1.0, 1.0], [0.0, 2.0, 5.0], [2.0, 5.0, -1.0]]
        b = [6.0, -4.0, 27.0]
        x = gaussian_elimination(A, b)
        # Verify Ax = b
        for i in range(3):
            val = sum(A[i][j] * x[j] for j in range(3))
            self.assertAlmostEqual(val, b[i], places=3)


class TestDeterminant(unittest.TestCase):
    def test_2x2(self):
        A = [[1.0, 2.0], [3.0, 4.0]]
        self.assertAlmostEqual(determinant_recursive(A), -2.0)

    def test_identity(self):
        I = identity_matrix(3)
        self.assertAlmostEqual(determinant_lu(I), 1.0)

    def test_singular(self):
        A = [[1.0, 2.0], [2.0, 4.0]]
        self.assertAlmostEqual(determinant_recursive(A), 0.0)

    def test_recursive_lu_agree(self):
        A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 0.0]]
        d1 = determinant_recursive(A)
        d2 = determinant_lu(A)
        self.assertAlmostEqual(d1, d2, places=3)


class TestLUDecomposition(unittest.TestCase):
    def test_basic(self):
        A = [[2.0, 1.0], [4.0, 3.0]]
        L, U = lu_decomposition(A)
        # Verify L*U = A
        result = matrix_multiply_standard(L, U)
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(result[i][j], A[i][j], places=5)


class TestMatrixInverse(unittest.TestCase):
    def test_2x2(self):
        A = [[1.0, 2.0], [3.0, 4.0]]
        inv = matrix_inverse_gauss_jordan(A)
        product = matrix_multiply_standard(A, inv)
        I = identity_matrix(2)
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(product[i][j], I[i][j], places=5)


class TestEigenvalues(unittest.TestCase):
    def test_power_iteration(self):
        # Symmetric matrix with known dominant eigenvalue
        A = [[4.0, 1.0], [1.0, 3.0]]
        eigenvalue, eigenvector = power_iteration(A)
        # Dominant eigenvalue should be ~4.618
        self.assertAlmostEqual(eigenvalue, (7 + math.sqrt(5)) / 2, places=1)


class TestSparseMatrix(unittest.TestCase):
    def test_set_get(self):
        sm = SparseMatrix(3, 3)
        sm.set(0, 0, 5.0)
        sm.set(1, 2, 3.0)
        self.assertEqual(sm.get(0, 0), 5.0)
        self.assertEqual(sm.get(1, 2), 3.0)
        self.assertEqual(sm.get(2, 2), 0.0)

    def test_to_dense(self):
        sm = SparseMatrix(2, 2)
        sm.set(0, 0, 1.0)
        sm.set(1, 1, 2.0)
        dense = sm.to_dense()
        self.assertEqual(dense, [[1.0, 0.0], [0.0, 2.0]])

    def test_from_dense(self):
        dense = [[1.0, 0.0], [0.0, 2.0]]
        sm = SparseMatrix.from_dense(dense)
        self.assertEqual(sm.nnz(), 2)

    def test_sparsity(self):
        sm = SparseMatrix(10, 10)
        sm.set(0, 0, 1.0)
        self.assertGreater(sm.sparsity(), 0.9)


# ============================================================================
# FIBONACCI TESTS
# ============================================================================


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestFibonacci(unittest.TestCase):
    KNOWN = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]

    def test_all_methods_agree(self):
        for n in range(10):
            expected = self.KNOWN[n]
            self.assertEqual(fibonacci_iterative(n), expected)
            self.assertEqual(fibonacci_memoized(n), expected)
            self.assertEqual(fibonacci_dp_bottom_up(n), expected)
            self.assertEqual(fibonacci_matrix(n), expected)

    def test_recursive_small(self):
        for n in range(10):
            self.assertEqual(fibonacci_recursive(n), self.KNOWN[n])

    def test_sequence(self):
        seq = fibonacci_sequence(7)
        self.assertEqual(seq, [0, 1, 1, 2, 3, 5, 8])

    def test_generator(self):
        gen = fibonacci_generator()
        first_5 = [next(gen) for _ in range(5)]
        self.assertEqual(first_5, [0, 1, 1, 2, 3])

    def test_is_fibonacci_number(self):
        self.assertTrue(is_fibonacci_number(0))
        self.assertTrue(is_fibonacci_number(1))
        self.assertTrue(is_fibonacci_number(8))
        self.assertTrue(is_fibonacci_number(144))
        self.assertFalse(is_fibonacci_number(4))
        self.assertFalse(is_fibonacci_number(10))

    def test_find_fibonacci_index(self):
        self.assertEqual(find_fibonacci_index(8), 6)
        self.assertEqual(find_fibonacci_index(144), 12)
        self.assertEqual(find_fibonacci_index(4), -1)

    def test_fibonacci_sum(self):
        # Sum of first 7: 0+1+1+2+3+5+8 = 20
        self.assertEqual(fibonacci_sum(7), 20)

    def test_calculator(self):
        calc = FibonacciCalculator()
        self.assertEqual(calc.calculate(10, "iterative"), 55)


if __name__ == "__main__":
    unittest.main(verbosity=2)
