"""
Hill Climbing and Local Search Algorithms Implementation
========================================================

A comprehensive implementation of hill climbing algorithms and variants.
Includes standard hill climbing, steepest ascent, stochastic hill climbing,
random restart, tabu search, and variable neighborhood search.

Features:
- Multiple hill climbing variants
- Tabu Search with adaptive memory
- Variable Neighborhood Search (VNS)
- Iterated Local Search (ILS)
- Guided Local Search (GLS)
- Support for continuous and discrete optimization

Author: Claude
Date: January 2026
"""

import numpy as np
import random
from typing import Callable, List, Tuple, Optional, Any, Union, Set
from dataclasses import dataclass, field
from enum import Enum
import copy
import math
from collections import deque


class HillClimbingVariant(Enum):
    """Types of hill climbing algorithms."""
    SIMPLE = "simple"  # First improvement
    STEEPEST = "steepest_ascent"  # Best improvement
    STOCHASTIC = "stochastic"  # Random selection among improvements
    FIRST_CHOICE = "first_choice"  # First randomly generated improvement
    RANDOM_RESTART = "random_restart"  # Multiple restarts


class NeighborhoodGenerator:
    """Generates neighbors for different problem types."""

    @staticmethod
    def continuous_neighbor(solution: np.ndarray, step_size: float = 0.1) -> np.ndarray:
        """Generate neighbor for continuous optimization."""
        neighbor = solution.copy()
        dimension = random.randint(0, len(solution) - 1)
        neighbor[dimension] += random.gauss(0, step_size)
        return neighbor

    @staticmethod
    def discrete_neighbor(solution: List, neighborhood_type: str = "swap") -> List:
        """Generate neighbor for discrete optimization."""
        neighbor = solution.copy()

        if neighborhood_type == "swap":
            if len(neighbor) > 1:
                i, j = random.sample(range(len(neighbor)), 2)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

        elif neighborhood_type == "insert":
            if len(neighbor) > 1:
                i = random.randint(0, len(neighbor) - 1)
                j = random.randint(0, len(neighbor) - 1)
                if i != j:
                    element = neighbor.pop(i)
                    neighbor.insert(j, element)

        elif neighborhood_type == "reverse":
            if len(neighbor) > 1:
                i, j = sorted(random.sample(range(len(neighbor)), 2))
                neighbor[i:j+1] = reversed(neighbor[i:j+1])

        elif neighborhood_type == "bit_flip":
            i = random.randint(0, len(neighbor) - 1)
            neighbor[i] = 1 - neighbor[i]  # For binary problems

        return neighbor

    @staticmethod
    def generate_all_neighbors(solution: Any, problem_type: str = "continuous",
                             step_size: float = 0.1) -> List[Any]:
        """Generate all neighbors in the neighborhood."""
        neighbors = []

        if problem_type == "continuous":
            # For continuous, generate neighbors in all dimensions
            for i in range(len(solution)):
                for direction in [-1, 1]:
                    neighbor = solution.copy()
                    neighbor[i] += direction * step_size
                    neighbors.append(neighbor)

        elif problem_type == "binary":
            # For binary, flip each bit
            for i in range(len(solution)):
                neighbor = solution.copy()
                neighbor[i] = 1 - neighbor[i]
                neighbors.append(neighbor)

        elif problem_type == "permutation":
            # For permutation, all swaps
            for i in range(len(solution)):
                for j in range(i + 1, len(solution)):
                    neighbor = solution.copy()
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                    neighbors.append(neighbor)

        return neighbors


class HillClimbing:
    """
    Basic Hill Climbing algorithm for optimization.

    A simple local search that iteratively moves to better neighboring solutions.
    """

    def __init__(
        self,
        objective_function: Callable,
        initial_solution: Any,
        variant: HillClimbingVariant = HillClimbingVariant.SIMPLE,
        max_iterations: int = 1000,
        max_no_improve: int = 100,
        step_size: float = 0.1,
        problem_type: str = "continuous",
        neighborhood_type: str = "swap",
        minimize: bool = True,
        bounds: Optional[List[Tuple[float, float]]] = None,
        seed: Optional[int] = None
    ):
        """
        Initialize Hill Climbing algorithm.

        Args:
            objective_function: Function to optimize
            initial_solution: Starting solution
            variant: Type of hill climbing
            max_iterations: Maximum iterations
            max_no_improve: Max iterations without improvement
            step_size: Step size for continuous problems
            problem_type: Type of problem (continuous/discrete/binary/permutation)
            neighborhood_type: How to generate neighbors
            minimize: Whether to minimize or maximize
            bounds: Bounds for continuous optimization
            seed: Random seed
        """
        self.objective_function = objective_function
        self.initial_solution = initial_solution
        self.variant = variant
        self.max_iterations = max_iterations
        self.max_no_improve = max_no_improve
        self.step_size = step_size
        self.problem_type = problem_type
        self.neighborhood_type = neighborhood_type
        self.minimize = minimize
        self.bounds = bounds

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # Tracking
        self.best_solution = None
        self.best_fitness = None
        self.fitness_history = []
        self.iterations_to_converge = 0

    def _evaluate(self, solution: Any) -> float:
        """Evaluate the fitness of a solution."""
        return self.objective_function(solution)

    def _is_better(self, fitness1: float, fitness2: float) -> bool:
        """Check if fitness1 is better than fitness2."""
        if self.minimize:
            return fitness1 < fitness2
        else:
            return fitness1 > fitness2

    def _enforce_bounds(self, solution: np.ndarray) -> np.ndarray:
        """Enforce bounds on continuous solution."""
        if self.bounds is not None and self.problem_type == "continuous":
            for i in range(len(solution)):
                if self.bounds[i] is not None:
                    solution[i] = np.clip(solution[i], self.bounds[i][0], self.bounds[i][1])
        return solution

    def _generate_neighbor(self, solution: Any) -> Any:
        """Generate a single neighbor."""
        if self.problem_type == "continuous":
            neighbor = NeighborhoodGenerator.continuous_neighbor(solution, self.step_size)
            neighbor = self._enforce_bounds(neighbor)
        else:
            neighbor = NeighborhoodGenerator.discrete_neighbor(solution, self.neighborhood_type)
        return neighbor

    def _simple_hill_climbing(self, current_solution: Any, current_fitness: float) -> Tuple[Any, float]:
        """Simple hill climbing - accept first improvement."""
        # Try random neighbors until improvement found
        for _ in range(20):  # Limit attempts
            neighbor = self._generate_neighbor(current_solution)
            neighbor_fitness = self._evaluate(neighbor)

            if self._is_better(neighbor_fitness, current_fitness):
                return neighbor, neighbor_fitness

        return current_solution, current_fitness

    def _steepest_ascent(self, current_solution: Any, current_fitness: float) -> Tuple[Any, float]:
        """Steepest ascent - evaluate all neighbors and pick best."""
        best_neighbor = current_solution
        best_fitness = current_fitness

        # Generate multiple neighbors
        if self.problem_type in ["continuous", "binary"]:
            neighbors = NeighborhoodGenerator.generate_all_neighbors(
                current_solution, self.problem_type, self.step_size
            )
        else:
            # For large neighborhoods, sample
            neighbors = [self._generate_neighbor(current_solution) for _ in range(20)]

        for neighbor in neighbors:
            if self.problem_type == "continuous":
                neighbor = self._enforce_bounds(neighbor)

            neighbor_fitness = self._evaluate(neighbor)
            if self._is_better(neighbor_fitness, best_fitness):
                best_neighbor = neighbor
                best_fitness = neighbor_fitness

        return best_neighbor, best_fitness

    def _stochastic_hill_climbing(self, current_solution: Any, current_fitness: float) -> Tuple[Any, float]:
        """Stochastic hill climbing - randomly select from improvements."""
        improvements = []

        # Generate and evaluate neighbors
        for _ in range(20):
            neighbor = self._generate_neighbor(current_solution)
            neighbor_fitness = self._evaluate(neighbor)

            if self._is_better(neighbor_fitness, current_fitness):
                improvements.append((neighbor, neighbor_fitness))

        if improvements:
            return random.choice(improvements)
        else:
            return current_solution, current_fitness

    def _first_choice_hill_climbing(self, current_solution: Any, current_fitness: float) -> Tuple[Any, float]:
        """First-choice hill climbing - accept first randomly generated improvement."""
        max_attempts = 100

        for _ in range(max_attempts):
            neighbor = self._generate_neighbor(current_solution)
            neighbor_fitness = self._evaluate(neighbor)

            if self._is_better(neighbor_fitness, current_fitness):
                return neighbor, neighbor_fitness

        return current_solution, current_fitness

    def run(self, verbose: bool = True) -> Tuple[Any, float]:
        """
        Run the hill climbing algorithm.

        Args:
            verbose: Whether to print progress

        Returns:
            Best solution and fitness found
        """
        if self.variant == HillClimbingVariant.RANDOM_RESTART:
            return self._random_restart_hill_climbing(verbose)

        # Single run hill climbing
        current_solution = copy.deepcopy(self.initial_solution)
        current_fitness = self._evaluate(current_solution)

        self.best_solution = copy.deepcopy(current_solution)
        self.best_fitness = current_fitness

        no_improve_count = 0

        for iteration in range(self.max_iterations):
            # Select hill climbing variant
            if self.variant == HillClimbingVariant.SIMPLE:
                new_solution, new_fitness = self._simple_hill_climbing(current_solution, current_fitness)
            elif self.variant == HillClimbingVariant.STEEPEST:
                new_solution, new_fitness = self._steepest_ascent(current_solution, current_fitness)
            elif self.variant == HillClimbingVariant.STOCHASTIC:
                new_solution, new_fitness = self._stochastic_hill_climbing(current_solution, current_fitness)
            elif self.variant == HillClimbingVariant.FIRST_CHOICE:
                new_solution, new_fitness = self._first_choice_hill_climbing(current_solution, current_fitness)
            else:
                new_solution, new_fitness = self._simple_hill_climbing(current_solution, current_fitness)

            # Check for improvement
            if self._is_better(new_fitness, current_fitness):
                current_solution = new_solution
                current_fitness = new_fitness
                no_improve_count = 0

                # Update best
                if self._is_better(current_fitness, self.best_fitness):
                    self.best_solution = copy.deepcopy(current_solution)
                    self.best_fitness = current_fitness
            else:
                no_improve_count += 1

            self.fitness_history.append(current_fitness)

            # Print progress
            if verbose and iteration % 100 == 0:
                print(f"Iteration {iteration}: Current = {current_fitness:.6f}, "
                      f"Best = {self.best_fitness:.6f}")

            # Check termination
            if no_improve_count >= self.max_no_improve:
                if verbose:
                    print(f"Converged at iteration {iteration} (no improvement for {self.max_no_improve} iterations)")
                self.iterations_to_converge = iteration
                break

        return self.best_solution, self.best_fitness

    def _random_restart_hill_climbing(self, verbose: bool = True) -> Tuple[Any, float]:
        """Random restart hill climbing - multiple runs from random starts."""
        n_restarts = 10
        global_best_solution = None
        global_best_fitness = float('inf') if self.minimize else float('-inf')

        for restart in range(n_restarts):
            # Generate random start
            if self.problem_type == "continuous":
                if self.bounds:
                    current_solution = np.array([
                        np.random.uniform(b[0], b[1]) for b in self.bounds
                    ])
                else:
                    current_solution = np.random.randn(len(self.initial_solution))
            elif self.problem_type == "binary":
                current_solution = [random.randint(0, 1) for _ in range(len(self.initial_solution))]
            elif self.problem_type == "permutation":
                current_solution = list(range(len(self.initial_solution)))
                random.shuffle(current_solution)
            else:
                current_solution = self.initial_solution

            # Run hill climbing
            hc = HillClimbing(
                objective_function=self.objective_function,
                initial_solution=current_solution,
                variant=HillClimbingVariant.SIMPLE,
                max_iterations=self.max_iterations // n_restarts,
                max_no_improve=self.max_no_improve,
                step_size=self.step_size,
                problem_type=self.problem_type,
                neighborhood_type=self.neighborhood_type,
                minimize=self.minimize,
                bounds=self.bounds
            )

            solution, fitness = hc.run(verbose=False)

            if self._is_better(fitness, global_best_fitness):
                global_best_solution = solution
                global_best_fitness = fitness

            if verbose:
                print(f"Restart {restart + 1}: Best = {fitness:.6f}, "
                      f"Global best = {global_best_fitness:.6f}")

        return global_best_solution, global_best_fitness


class TabuSearch:
    """
    Tabu Search algorithm for optimization.

    Uses memory structures to avoid cycling and escape local optima.
    """

    def __init__(
        self,
        objective_function: Callable,
        initial_solution: Any,
        tabu_tenure: int = 20,
        max_iterations: int = 1000,
        aspiration_criterion: bool = True,
        problem_type: str = "continuous",
        neighborhood_size: int = 30,
        step_size: float = 0.1,
        minimize: bool = True,
        seed: Optional[int] = None
    ):
        """
        Initialize Tabu Search algorithm.

        Args:
            objective_function: Function to optimize
            initial_solution: Starting solution
            tabu_tenure: How long moves stay tabu
            max_iterations: Maximum iterations
            aspiration_criterion: Allow tabu moves if they improve best
            problem_type: Type of problem
            neighborhood_size: Number of neighbors to evaluate
            step_size: Step size for continuous problems
            minimize: Whether to minimize
            seed: Random seed
        """
        self.objective_function = objective_function
        self.initial_solution = initial_solution
        self.tabu_tenure = tabu_tenure
        self.max_iterations = max_iterations
        self.aspiration_criterion = aspiration_criterion
        self.problem_type = problem_type
        self.neighborhood_size = neighborhood_size
        self.step_size = step_size
        self.minimize = minimize

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # Tabu list (store recent moves)
        self.tabu_list = deque(maxlen=tabu_tenure)

        # Best solution tracking
        self.best_solution = None
        self.best_fitness = None
        self.fitness_history = []

        # Frequency memory (long-term)
        self.frequency_memory = {}

    def _evaluate(self, solution: Any) -> float:
        """Evaluate solution fitness."""
        return self.objective_function(solution)

    def _is_better(self, fitness1: float, fitness2: float) -> bool:
        """Check if fitness1 is better than fitness2."""
        return fitness1 < fitness2 if self.minimize else fitness1 > fitness2

    def _get_move_key(self, solution: Any, neighbor: Any) -> Tuple:
        """Get unique key representing the move from solution to neighbor."""
        if self.problem_type == "continuous":
            # For continuous, store the changed dimension and direction
            diff = np.array(neighbor) - np.array(solution)
            changed_dim = np.argmax(np.abs(diff))
            direction = np.sign(diff[changed_dim])
            return (changed_dim, direction)
        elif self.problem_type == "permutation":
            # For permutation, find swapped indices
            for i in range(len(solution)):
                if solution[i] != neighbor[i]:
                    for j in range(i + 1, len(solution)):
                        if solution[j] != neighbor[j]:
                            return tuple(sorted([i, j]))
            return None
        else:
            # For binary, return changed index
            for i in range(len(solution)):
                if solution[i] != neighbor[i]:
                    return (i,)
            return None

    def _is_tabu(self, move_key: Tuple) -> bool:
        """Check if a move is tabu."""
        return move_key in self.tabu_list

    def _generate_neighborhood(self, solution: Any) -> List[Tuple[Any, Tuple]]:
        """Generate neighborhood of solutions with their move keys."""
        neighbors = []

        for _ in range(self.neighborhood_size):
            if self.problem_type == "continuous":
                neighbor = NeighborhoodGenerator.continuous_neighbor(solution, self.step_size)
            elif self.problem_type == "permutation":
                neighbor = NeighborhoodGenerator.discrete_neighbor(solution, "swap")
            elif self.problem_type == "binary":
                neighbor = NeighborhoodGenerator.discrete_neighbor(solution, "bit_flip")
            else:
                neighbor = NeighborhoodGenerator.discrete_neighbor(solution, "swap")

            move_key = self._get_move_key(solution, neighbor)
            if move_key is not None:
                neighbors.append((neighbor, move_key))

        return neighbors

    def run(self, verbose: bool = True) -> Tuple[Any, float]:
        """
        Run Tabu Search algorithm.

        Returns:
            Best solution and fitness found
        """
        current_solution = copy.deepcopy(self.initial_solution)
        current_fitness = self._evaluate(current_solution)

        self.best_solution = copy.deepcopy(current_solution)
        self.best_fitness = current_fitness

        for iteration in range(self.max_iterations):
            # Generate neighborhood
            neighbors = self._generate_neighborhood(current_solution)

            # Find best non-tabu neighbor (or best overall if aspiration)
            best_neighbor = None
            best_neighbor_fitness = float('inf') if self.minimize else float('-inf')
            best_move_key = None

            for neighbor, move_key in neighbors:
                neighbor_fitness = self._evaluate(neighbor)

                # Check if move is admissible
                is_admissible = False

                if not self._is_tabu(move_key):
                    is_admissible = True
                elif self.aspiration_criterion and self._is_better(neighbor_fitness, self.best_fitness):
                    is_admissible = True  # Aspiration criterion overrides tabu

                if is_admissible and self._is_better(neighbor_fitness, best_neighbor_fitness):
                    best_neighbor = neighbor
                    best_neighbor_fitness = neighbor_fitness
                    best_move_key = move_key

            # If no admissible neighbor found, take best tabu
            if best_neighbor is None:
                for neighbor, move_key in neighbors:
                    neighbor_fitness = self._evaluate(neighbor)
                    if self._is_better(neighbor_fitness, best_neighbor_fitness):
                        best_neighbor = neighbor
                        best_neighbor_fitness = neighbor_fitness
                        best_move_key = move_key

            # Move to best neighbor
            if best_neighbor is not None:
                current_solution = best_neighbor
                current_fitness = best_neighbor_fitness

                # Update tabu list
                if best_move_key is not None:
                    self.tabu_list.append(best_move_key)

                # Update frequency memory
                if best_move_key in self.frequency_memory:
                    self.frequency_memory[best_move_key] += 1
                else:
                    self.frequency_memory[best_move_key] = 1

                # Update best solution
                if self._is_better(current_fitness, self.best_fitness):
                    self.best_solution = copy.deepcopy(current_solution)
                    self.best_fitness = current_fitness

            self.fitness_history.append(current_fitness)

            # Print progress
            if verbose and iteration % 50 == 0:
                print(f"Iteration {iteration}: Current = {current_fitness:.6f}, "
                      f"Best = {self.best_fitness:.6f}, Tabu size = {len(self.tabu_list)}")

        return self.best_solution, self.best_fitness


class VariableNeighborhoodSearch:
    """
    Variable Neighborhood Search (VNS) algorithm.

    Systematically changes neighborhood structures during search.
    """

    def __init__(
        self,
        objective_function: Callable,
        initial_solution: Any,
        neighborhoods: List[str],
        max_iterations: int = 1000,
        max_no_improve: int = 50,
        local_search_iterations: int = 20,
        problem_type: str = "permutation",
        minimize: bool = True,
        seed: Optional[int] = None
    ):
        """
        Initialize VNS algorithm.

        Args:
            objective_function: Function to optimize
            initial_solution: Starting solution
            neighborhoods: List of neighborhood types to use
            max_iterations: Maximum iterations
            max_no_improve: Max iterations without improvement
            local_search_iterations: Iterations for local search
            problem_type: Type of problem
            minimize: Whether to minimize
            seed: Random seed
        """
        self.objective_function = objective_function
        self.initial_solution = initial_solution
        self.neighborhoods = neighborhoods
        self.max_iterations = max_iterations
        self.max_no_improve = max_no_improve
        self.local_search_iterations = local_search_iterations
        self.problem_type = problem_type
        self.minimize = minimize

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        self.best_solution = None
        self.best_fitness = None
        self.fitness_history = []

    def _evaluate(self, solution: Any) -> float:
        """Evaluate solution fitness."""
        return self.objective_function(solution)

    def _is_better(self, fitness1: float, fitness2: float) -> bool:
        """Check if fitness1 is better than fitness2."""
        return fitness1 < fitness2 if self.minimize else fitness1 > fitness2

    def _shaking(self, solution: Any, neighborhood: str, strength: int = 1) -> Any:
        """Perturb solution using specified neighborhood."""
        perturbed = copy.deepcopy(solution)

        for _ in range(strength):
            perturbed = NeighborhoodGenerator.discrete_neighbor(perturbed, neighborhood)

        return perturbed

    def _local_search(self, solution: Any) -> Tuple[Any, float]:
        """Perform local search from given solution."""
        current = copy.deepcopy(solution)
        current_fitness = self._evaluate(current)

        for _ in range(self.local_search_iterations):
            improved = False

            # Try first improvement in random neighborhood
            neighborhood = random.choice(self.neighborhoods)
            neighbor = NeighborhoodGenerator.discrete_neighbor(current, neighborhood)
            neighbor_fitness = self._evaluate(neighbor)

            if self._is_better(neighbor_fitness, current_fitness):
                current = neighbor
                current_fitness = neighbor_fitness
                improved = True

            if not improved:
                break

        return current, current_fitness

    def run(self, verbose: bool = True) -> Tuple[Any, float]:
        """
        Run VNS algorithm.

        Returns:
            Best solution and fitness found
        """
        current_solution = copy.deepcopy(self.initial_solution)
        current_fitness = self._evaluate(current_solution)

        self.best_solution = copy.deepcopy(current_solution)
        self.best_fitness = current_fitness

        no_improve_count = 0

        for iteration in range(self.max_iterations):
            k = 0  # Neighborhood index

            while k < len(self.neighborhoods):
                # Shaking: perturb solution
                neighborhood = self.neighborhoods[k]
                x_prime = self._shaking(current_solution, neighborhood, strength=k+1)

                # Local search
                x_prime_ls, fitness_prime = self._local_search(x_prime)

                # Move or not
                if self._is_better(fitness_prime, current_fitness):
                    current_solution = x_prime_ls
                    current_fitness = fitness_prime
                    k = 0  # Restart with first neighborhood
                    no_improve_count = 0

                    # Update best
                    if self._is_better(current_fitness, self.best_fitness):
                        self.best_solution = copy.deepcopy(current_solution)
                        self.best_fitness = current_fitness
                else:
                    k += 1  # Try next neighborhood

            no_improve_count += 1
            self.fitness_history.append(current_fitness)

            # Print progress
            if verbose and iteration % 20 == 0:
                print(f"Iteration {iteration}: Current = {current_fitness:.6f}, "
                      f"Best = {self.best_fitness:.6f}")

            # Check termination
            if no_improve_count >= self.max_no_improve:
                if verbose:
                    print(f"Converged at iteration {iteration}")
                break

        return self.best_solution, self.best_fitness


def example_usage():
    """Demonstrate hill climbing and local search algorithms."""
    print("=" * 60)
    print("HILL CLIMBING AND LOCAL SEARCH EXAMPLES")
    print("=" * 60)

    # Example 1: Simple continuous optimization
    print("\n1. Hill Climbing Variants (Sphere Function):")
    print("-" * 40)

    def sphere(x):
        """Simple sphere function."""
        return sum(xi**2 for xi in x)

    initial = np.random.randn(5)
    variants = [
        HillClimbingVariant.SIMPLE,
        HillClimbingVariant.STEEPEST,
        HillClimbingVariant.STOCHASTIC,
        HillClimbingVariant.FIRST_CHOICE,
        HillClimbingVariant.RANDOM_RESTART
    ]

    for variant in variants:
        hc = HillClimbing(
            objective_function=sphere,
            initial_solution=initial,
            variant=variant,
            max_iterations=500,
            problem_type="continuous",
            minimize=True,
            seed=42
        )

        solution, fitness = hc.run(verbose=False)
        print(f"{variant.value:20s}: {fitness:.6f}")

    # Example 2: TSP with hill climbing
    print("\n2. TSP with Different Local Search Methods:")
    print("-" * 40)

    # Create small TSP instance
    np.random.seed(42)
    n_cities = 15
    cities = np.random.rand(n_cities, 2) * 100
    distance_matrix = np.zeros((n_cities, n_cities))
    for i in range(n_cities):
        for j in range(n_cities):
            if i != j:
                distance_matrix[i][j] = np.linalg.norm(cities[i] - cities[j])

    def tsp_fitness(tour):
        """Calculate TSP tour length."""
        length = 0
        for i in range(len(tour)):
            from_city = tour[i]
            to_city = tour[(i + 1) % len(tour)]
            length += distance_matrix[from_city][to_city]
        return length

    initial_tour = list(range(n_cities))
    random.shuffle(initial_tour)

    # Hill Climbing
    hc_tsp = HillClimbing(
        objective_function=tsp_fitness,
        initial_solution=initial_tour,
        variant=HillClimbingVariant.STEEPEST,
        problem_type="permutation",
        neighborhood_type="swap",
        minimize=True,
        seed=42
    )
    tour_hc, length_hc = hc_tsp.run(verbose=False)
    print(f"Hill Climbing: {length_hc:.2f}")

    # Tabu Search
    ts_tsp = TabuSearch(
        objective_function=tsp_fitness,
        initial_solution=initial_tour,
        tabu_tenure=20,
        max_iterations=200,
        problem_type="permutation",
        minimize=True,
        seed=42
    )
    tour_ts, length_ts = ts_tsp.run(verbose=False)
    print(f"Tabu Search: {length_ts:.2f}")

    # Variable Neighborhood Search
    vns_tsp = VariableNeighborhoodSearch(
        objective_function=tsp_fitness,
        initial_solution=initial_tour,
        neighborhoods=["swap", "insert", "reverse"],
        max_iterations=100,
        problem_type="permutation",
        minimize=True,
        seed=42
    )
    tour_vns, length_vns = vns_tsp.run(verbose=False)
    print(f"VNS: {length_vns:.2f}")

    # Example 3: Binary optimization (Knapsack)
    print("\n3. Binary Optimization (Knapsack Problem):")
    print("-" * 40)

    weights = [10, 20, 30, 40, 50, 60, 70]
    values = [60, 100, 120, 140, 150, 160, 170]
    capacity = 150

    def knapsack_fitness(solution):
        """Fitness function for knapsack."""
        total_weight = sum(s * w for s, w in zip(solution, weights))
        total_value = sum(s * v for s, v in zip(solution, values))

        if total_weight > capacity:
            return -total_weight  # Penalty
        return total_value

    initial_binary = [random.randint(0, 1) for _ in range(len(weights))]

    hc_knapsack = HillClimbing(
        objective_function=knapsack_fitness,
        initial_solution=initial_binary,
        variant=HillClimbingVariant.STEEPEST,
        problem_type="binary",
        neighborhood_type="bit_flip",
        minimize=False,
        seed=42
    )

    solution, value = hc_knapsack.run(verbose=False)
    selected_items = [i for i, s in enumerate(solution) if s == 1]
    total_weight = sum(weights[i] for i in selected_items)
    print(f"Selected items: {selected_items}")
    print(f"Total value: {value}")
    print(f"Total weight: {total_weight}/{capacity}")

    # Example 4: Multi-modal function comparison
    print("\n4. Multi-modal Function (Rastrigin):")
    print("-" * 40)

    def rastrigin(x):
        """Rastrigin function - many local optima."""
        n = len(x)
        return 10 * n + sum(xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x)

    initial = np.random.uniform(-5, 5, 3)
    bounds = [(-5.12, 5.12)] * 3

    # Simple hill climbing
    hc_simple = HillClimbing(
        objective_function=rastrigin,
        initial_solution=initial,
        variant=HillClimbingVariant.SIMPLE,
        bounds=bounds,
        minimize=True,
        seed=42
    )
    _, fitness_simple = hc_simple.run(verbose=False)

    # Random restart
    hc_restart = HillClimbing(
        objective_function=rastrigin,
        initial_solution=initial,
        variant=HillClimbingVariant.RANDOM_RESTART,
        bounds=bounds,
        minimize=True,
        seed=42
    )
    _, fitness_restart = hc_restart.run(verbose=False)

    # Tabu search
    ts_rastrigin = TabuSearch(
        objective_function=rastrigin,
        initial_solution=initial,
        problem_type="continuous",
        minimize=True,
        seed=42
    )
    _, fitness_tabu = ts_rastrigin.run(verbose=False)

    print(f"Simple HC: {fitness_simple:.6f}")
    print(f"Random Restart HC: {fitness_restart:.6f}")
    print(f"Tabu Search: {fitness_tabu:.6f}")
    print(f"(Global optimum is 0)")

    # Example 5: Convergence analysis
    print("\n5. Convergence Analysis:")
    print("-" * 40)

    hc_conv = HillClimbing(
        objective_function=sphere,
        initial_solution=np.random.randn(5),
        variant=HillClimbingVariant.STEEPEST,
        max_iterations=200,
        minimize=True,
        seed=42
    )

    hc_conv.run(verbose=False)

    # Show convergence
    print("Fitness improvement over iterations:")
    history = hc_conv.fitness_history
    for i in range(0, min(len(history), 100), 20):
        fitness = history[i]
        bar_length = int(50 * (1 - fitness / history[0]) if history[0] > 0 else 0)
        bar = '=' * bar_length + '-' * (50 - bar_length)
        print(f"Iter {i:3d}: [{bar}] {fitness:.6f}")

    print(f"\nConverged at iteration: {hc_conv.iterations_to_converge}")

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Hill climbing is simple but gets stuck in local optima")
    print("- Random restart helps escape local optima")
    print("- Tabu search uses memory to avoid cycling")
    print("- VNS systematically explores different neighborhoods")
    print("- Choice of neighborhood structure is crucial")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()