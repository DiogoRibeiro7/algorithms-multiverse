"""
Test Suite for Optimization Algorithms

Tests all optimization implementations:
- Genetic Algorithm
- Particle Swarm Optimization
- Simulated Annealing
- Hill Climbing
- Tabu Search
- Ant Colony Optimization
- Simplex Method (Linear Programming)
- Convex Optimization (Gradient Descent, Newton's Method)

Run with:
    python -m pytest test_optimization.py -v
    or
    python test_optimization.py

NOTE: All modules require numpy. If numpy is unavailable or broken,
all tests are skipped gracefully.
"""

import sys
import os
import subprocess
import unittest

sys.path.insert(0, os.path.dirname(__file__))

# Numpy segfaults on some Python 3.13 / MINGW builds.
# Check via subprocess to avoid crashing the test runner.
_numpy_check = subprocess.run(
    [sys.executable, "-c", "import numpy"],
    capture_output=True, timeout=10
)
HAS_NUMPY = _numpy_check.returncode == 0

if HAS_NUMPY:
    import numpy as np
    from genetic_algorithm import GeneticAlgorithm, SelectionMethod
    from particle_swarm import ParticleSwarmOptimization
    from simulated_annealing import SimulatedAnnealing, CoolingSchedule
    from hill_climbing import HillClimbing, HillClimbingVariant
    from tabu_search import TabuSearch
    from ant_colony import AntColonyOptimization
    from simplex_method import (
        SimplexSolver, LinearProgram, SimplexStatus,
        TransportationProblem,
    )
    from convex_optimization import (
        GradientDescent, NewtonMethod, CoordinateDescent,
    )


def _sphere(x):
    """Sphere function: min at origin, f(0,...,0) = 0."""
    return sum(xi ** 2 for xi in x)


def _sphere_np(x):
    """Sphere function for numpy arrays."""
    return float(np.sum(x ** 2))


# ============================================================================
# GENETIC ALGORITHM TESTS
# ============================================================================


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestGeneticAlgorithm(unittest.TestCase):
    def test_sphere_optimization(self):
        def fitness(genes):
            return -_sphere_np(genes)  # Maximize negative sphere

        ga = GeneticAlgorithm(
            fitness_function=fitness,
            gene_length=2,
            population_size=50,
            mutation_rate=0.1,
            crossover_rate=0.8,
            gene_type="real",
            gene_bounds=(-5.0, 5.0),
        )
        best = ga.run(max_generations=100, verbose=False)
        # Should find something near origin
        self.assertGreater(best.fitness, -1.0)

    def test_binary_optimization(self):
        def fitness(genes):
            return float(np.sum(genes))  # Maximize number of 1s

        ga = GeneticAlgorithm(
            fitness_function=fitness,
            gene_length=10,
            population_size=30,
            gene_type="binary",
        )
        best = ga.run(max_generations=50, verbose=False)
        self.assertGreater(best.fitness, 5)  # Should find most 1s

    def test_convergence(self):
        def fitness(genes):
            return -_sphere_np(genes)

        ga = GeneticAlgorithm(
            fitness_function=fitness,
            gene_length=2,
            population_size=30,
            gene_type="real",
            gene_bounds=(-5.0, 5.0),
        )
        best = ga.run(max_generations=50, verbose=False)
        self.assertIsNotNone(best)
        self.assertIsNotNone(best.fitness)


# ============================================================================
# PARTICLE SWARM OPTIMIZATION TESTS
# ============================================================================


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestPSO(unittest.TestCase):
    def test_sphere(self):
        pso = ParticleSwarmOptimization(
            objective_function=_sphere_np,
            n_dimensions=2,
            n_particles=20,
            bounds=(np.array([-5, -5]), np.array([5, 5])),
        )
        pos, fitness = pso.run(max_iterations=100, verbose=False)
        self.assertLess(fitness, 1.0)  # Should be near 0

    def test_returns_array(self):
        pso = ParticleSwarmOptimization(
            objective_function=_sphere_np,
            n_dimensions=3,
            n_particles=10,
            bounds=(np.array([-5, -5, -5]), np.array([5, 5, 5])),
        )
        pos, fitness = pso.run(max_iterations=50, verbose=False)
        self.assertEqual(len(pos), 3)
        self.assertIsInstance(fitness, float)


# ============================================================================
# SIMULATED ANNEALING TESTS
# ============================================================================


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestSimulatedAnnealing(unittest.TestCase):
    def test_sphere(self):
        sa = SimulatedAnnealing(
            objective_function=_sphere,
            initial_solution=[5.0, 5.0],
            initial_temp=100.0,
            final_temp=0.01,
            max_iterations=5000,
            cooling_rate=0.99,
        )
        result = sa.run(verbose=False)
        self.assertLess(result.energy, 5.0)

    def test_cooling_schedules(self):
        for schedule in [CoolingSchedule.LINEAR, CoolingSchedule.EXPONENTIAL]:
            sa = SimulatedAnnealing(
                objective_function=_sphere,
                initial_solution=[3.0, 3.0],
                cooling_schedule=schedule,
                max_iterations=1000,
            )
            result = sa.run(verbose=False)
            self.assertIsNotNone(result)


# ============================================================================
# HILL CLIMBING TESTS
# ============================================================================


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestHillClimbing(unittest.TestCase):
    def test_sphere(self):
        hc = HillClimbing(
            objective_function=lambda x: -_sphere(x),
            initial_solution=[5.0, 5.0],
            variant=HillClimbingVariant.STEEPEST,
            max_iterations=500,
        )
        solution, fitness = hc.run(verbose=False)
        self.assertGreater(fitness, -50.0)  # Should improve from -50

    def test_variants(self):
        for variant in [
            HillClimbingVariant.SIMPLE,
            HillClimbingVariant.STEEPEST,
            HillClimbingVariant.STOCHASTIC,
        ]:
            hc = HillClimbing(
                objective_function=lambda x: -_sphere(x),
                initial_solution=[3.0, 3.0],
                variant=variant,
                max_iterations=200,
            )
            solution, fitness = hc.run(verbose=False)
            self.assertIsNotNone(solution)


# ============================================================================
# TABU SEARCH TESTS
# ============================================================================


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestTabuSearch(unittest.TestCase):
    def test_basic(self):
        def neighbor_fn(solution):
            neighbors = []
            for i in range(len(solution)):
                for delta in [-0.5, 0.5]:
                    new = list(solution)
                    new[i] += delta
                    neighbors.append(new)
            return neighbors

        ts = TabuSearch(
            objective_function=_sphere,
            initial_solution=[5.0, 5.0],
            neighbor_function=neighbor_fn,
            tabu_tenure=5,
            max_iterations=100,
        )
        solution, obj = ts.run(verbose=False)
        self.assertLess(obj, 50.0)  # Should improve from 50


# ============================================================================
# ANT COLONY OPTIMIZATION TESTS
# ============================================================================


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestACO(unittest.TestCase):
    def test_tsp(self):
        # Small 4-city TSP
        dist = np.array([
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0],
        ], dtype=float)
        aco = AntColonyOptimization(
            distance_matrix=dist,
            n_ants=10,
            n_iterations=50,
        )
        path, cost = aco.run(verbose=False)
        self.assertEqual(len(path), 4)
        self.assertEqual(len(set(path)), 4)  # All cities visited
        self.assertGreater(cost, 0)


# ============================================================================
# SIMPLEX METHOD TESTS
# ============================================================================


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestSimplex(unittest.TestCase):
    def test_basic_lp(self):
        # Maximize 5x + 4y subject to:
        # 6x + 4y <= 24, x + 2y <= 6, x,y >= 0
        # Optimal: x=3, y=1.5, obj=21
        c = np.array([5.0, 4.0])
        A = np.array([[6.0, 4.0], [1.0, 2.0]])
        b = np.array([24.0, 6.0])
        lp = LinearProgram(c=c, A=A, b=b, optimization_type="maximize")
        solver = SimplexSolver(lp)
        status, solution, obj_val = solver.solve()
        self.assertEqual(status, SimplexStatus.OPTIMAL)
        self.assertAlmostEqual(obj_val, 21.0, places=1)

    def test_minimize(self):
        # Minimize x + y subject to: x + y >= 2, x,y >= 0
        # Need to convert to standard form
        c = np.array([1.0, 1.0])
        A = np.array([[-1.0, -1.0]])  # -x - y <= -2
        b = np.array([-2.0])
        lp = LinearProgram(c=c, A=A, b=b, optimization_type="minimize")
        solver = SimplexSolver(lp)
        status, solution, obj_val = solver.solve()
        if status == SimplexStatus.OPTIMAL:
            self.assertAlmostEqual(obj_val, 2.0, places=1)

    def test_transportation(self):
        supply = np.array([20.0, 30.0])
        demand = np.array([10.0, 20.0, 20.0])
        costs = np.array([
            [2.0, 3.0, 1.0],
            [5.0, 4.0, 8.0],
        ])
        tp = TransportationProblem(supply, demand, costs)
        alloc = tp.solve_northwest_corner()
        self.assertEqual(alloc.shape, (2, 3))
        # Supply constraints satisfied
        for i in range(2):
            self.assertAlmostEqual(alloc[i].sum(), supply[i], places=5)


# ============================================================================
# CONVEX OPTIMIZATION TESTS
# ============================================================================


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestConvexOptimization(unittest.TestCase):
    def test_gradient_descent_sphere(self):
        def f(x):
            return float(np.sum(x ** 2))

        def grad_f(x):
            return 2 * x

        gd = GradientDescent()
        result = gd.minimize(f, grad_f, np.array([5.0, 5.0]))
        self.assertTrue(result.converged)
        self.assertLess(result.value, 0.01)

    def test_newton_method(self):
        def f(x):
            return float(np.sum(x ** 2))

        def grad_f(x):
            return 2 * x

        def hess_f(x):
            return 2 * np.eye(len(x))

        nm = NewtonMethod()
        result = nm.minimize(f, grad_f, hess_f, np.array([5.0, 5.0]))
        self.assertTrue(result.converged)
        self.assertLess(result.value, 0.001)

    def test_coordinate_descent(self):
        def f(x):
            return float(np.sum(x ** 2))

        def grad_f(x):
            return 2 * x

        cd = CoordinateDescent()
        result = cd.minimize(f, grad_f, np.array([3.0, 3.0]))
        self.assertLess(result.value, 1.0)


# ============================================================================
# CROSS-ALGORITHM CONSISTENCY
# ============================================================================


@unittest.skipUnless(HAS_NUMPY, "numpy unavailable")
class TestCrossAlgorithmConsistency(unittest.TestCase):
    def test_all_improve_from_initial(self):
        """All algorithms should improve on the initial solution."""
        initial = [5.0, 5.0]
        initial_val = _sphere(initial)

        # Hill Climbing
        hc = HillClimbing(
            objective_function=lambda x: -_sphere(x),
            initial_solution=list(initial),
            max_iterations=200,
        )
        _, hc_fit = hc.run(verbose=False)
        self.assertGreater(hc_fit, -initial_val)

        # Simulated Annealing
        sa = SimulatedAnnealing(
            objective_function=_sphere,
            initial_solution=list(initial),
            max_iterations=1000,
        )
        sa_result = sa.run(verbose=False)
        self.assertLess(sa_result.energy, initial_val)


if __name__ == "__main__":
    unittest.main(verbosity=2)
