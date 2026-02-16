"""
Hill Climbing Algorithm Implementation
======================================

A comprehensive implementation of Hill Climbing and its variants for optimization.
Hill Climbing is a local search algorithm that iteratively moves to better
neighboring solutions until no improvement can be found.

Variants Implemented:
- Simple Hill Climbing
- Steepest Ascent Hill Climbing
- Stochastic Hill Climbing
- First-Choice Hill Climbing
- Random Restart Hill Climbing
- Simulated Hill Climbing
- Variable Neighborhood Hill Climbing
- Late Acceptance Hill Climbing

Applications:
- Continuous optimization
- Discrete optimization
- Feature selection
- Hyperparameter tuning
- Local search in hybrid algorithms

Author: Claude
Date: January 2026
"""

import numpy as np
import random
from typing import Callable, Optional, List, Tuple, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import math
import copy


class HillClimbingVariant(Enum):
    """Hill climbing algorithm variants."""
    SIMPLE = "simple"
    STEEPEST = "steepest_ascent"
    STOCHASTIC = "stochastic"
    FIRST_CHOICE = "first_choice"
    RANDOM_RESTART = "random_restart"
    SIMULATED = "simulated"
    VARIABLE_NEIGHBORHOOD = "variable_neighborhood"
    LATE_ACCEPTANCE = "late_acceptance"


class NeighborhoodType(Enum):
    """Types of neighborhood structures."""
    SINGLE_FLIP = "single_flip"
    SWAP = "swap"
    GAUSSIAN = "gaussian"
    UNIFORM = "uniform"
    ADAPTIVE = "adaptive"
    CUSTOM = "custom"


@dataclass
class Solution:
    """Represents a solution in the search space."""
    state: Any
    fitness: float = -float('inf')
    iteration: int = 0
    neighborhood_size: int = 1


class HillClimbing:
    """
    Base Hill Climbing implementation.

    A simple local search that moves to improving neighbors.
    """

    def __init__(self,
                 objective_function: Callable,
                 initial_solution: Any,
                 neighbor_function: Optional[Callable] = None,
                 variant: HillClimbingVariant = HillClimbingVariant.STEEPEST,
                 max_iterations: int = 1000,
                 max_neighbors: int = 100,
                 neighborhood_size: float = 0.1):
        """
        Initialize Hill Climbing algorithm.

        Args:
            objective_function: Function to maximize (use negative for minimization)
            initial_solution: Starting solution
            neighbor_function: Function to generate neighbors
            variant: Hill climbing variant
            max_iterations: Maximum iterations
            max_neighbors: Maximum neighbors to evaluate
            neighborhood_size: Size of neighborhood for continuous spaces
        """
        self.objective_function = objective_function
        self.initial_solution = initial_solution
        self.neighbor_function = neighbor_function
        self.variant = variant
        self.max_iterations = max_iterations
        self.max_neighbors = max_neighbors
        self.neighborhood_size = neighborhood_size

        # Solution tracking
        self.current_solution = None
        self.best_solution = None
        self.iteration = 0

        # History tracking
        self.history = {
            'fitness': [],
            'improvements': [],
            'plateau_length': [],
            'neighborhood_size': []
        }

        # Variant-specific parameters
        self.restart_threshold = 100  # For random restart
        self.acceptance_history_length = 500  # For late acceptance
        self.acceptance_history = []

    def generate_neighbors(self, solution: Any, n_neighbors: Optional[int] = None) -> List[Any]:
        """Generate neighboring solutions."""
        if n_neighbors is None:
            n_neighbors = self.max_neighbors

        neighbors = []

        if self.neighbor_function:
            # Use custom neighbor function
            for _ in range(n_neighbors):
                neighbor = self.neighbor_function(solution)
                neighbors.append(neighbor)
        else:
            # Default neighborhood generation
            if isinstance(solution, np.ndarray):
                neighbors = self._generate_continuous_neighbors(solution, n_neighbors)
            elif isinstance(solution, list):
                neighbors = self._generate_discrete_neighbors(solution, n_neighbors)
            else:
                raise ValueError("No neighbor function provided and cannot infer type")

        return neighbors

    def _generate_continuous_neighbors(self, solution: np.ndarray, n_neighbors: int) -> List[np.ndarray]:
        """Generate neighbors for continuous optimization."""
        neighbors = []

        for _ in range(n_neighbors):
            # Gaussian perturbation
            perturbation = np.random.normal(0, self.neighborhood_size, solution.shape)
            neighbor = solution + perturbation
            neighbors.append(neighbor)

        return neighbors

    def _generate_discrete_neighbors(self, solution: List, n_neighbors: int) -> List[List]:
        """Generate neighbors for discrete optimization."""
        neighbors = []

        for _ in range(n_neighbors):
            neighbor = solution.copy()

            # Random swap
            if len(solution) > 1:
                i, j = random.sample(range(len(solution)), 2)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

            neighbors.append(neighbor)

        return neighbors

    def simple_hill_climb(self) -> bool:
        """
        Simple hill climbing - accepts first improving neighbor.

        Returns:
            True if improvement found
        """
        # Generate one neighbor at a time
        for _ in range(self.max_neighbors):
            neighbors = self.generate_neighbors(self.current_solution.state, 1)
            neighbor = neighbors[0]
            neighbor_fitness = self.objective_function(neighbor)

            if neighbor_fitness > self.current_solution.fitness:
                self.current_solution = Solution(neighbor, neighbor_fitness, self.iteration)
                return True

        return False

    def steepest_ascent_hill_climb(self) -> bool:
        """
        Steepest ascent - evaluates all neighbors and picks best.

        Returns:
            True if improvement found
        """
        neighbors = self.generate_neighbors(self.current_solution.state)

        best_neighbor = None
        best_fitness = self.current_solution.fitness

        for neighbor in neighbors:
            fitness = self.objective_function(neighbor)
            if fitness > best_fitness:
                best_fitness = fitness
                best_neighbor = neighbor

        if best_neighbor is not None:
            self.current_solution = Solution(best_neighbor, best_fitness, self.iteration)
            return True

        return False

    def stochastic_hill_climb(self) -> bool:
        """
        Stochastic hill climbing - randomly selects from improving neighbors.

        Returns:
            True if improvement found
        """
        neighbors = self.generate_neighbors(self.current_solution.state)

        # Find all improving neighbors
        improving_neighbors = []
        for neighbor in neighbors:
            fitness = self.objective_function(neighbor)
            if fitness > self.current_solution.fitness:
                improving_neighbors.append((neighbor, fitness))

        if improving_neighbors:
            # Randomly select one
            neighbor, fitness = random.choice(improving_neighbors)
            self.current_solution = Solution(neighbor, fitness, self.iteration)
            return True

        return False

    def first_choice_hill_climb(self) -> bool:
        """
        First-choice hill climbing - generates random neighbors until improvement found.

        Returns:
            True if improvement found
        """
        for _ in range(self.max_neighbors):
            neighbor = self.generate_neighbors(self.current_solution.state, 1)[0]
            fitness = self.objective_function(neighbor)

            if fitness > self.current_solution.fitness:
                self.current_solution = Solution(neighbor, fitness, self.iteration)
                return True

        return False

    def simulated_hill_climb(self, temperature: float = 0.1) -> bool:
        """
        Simulated hill climbing - occasionally accepts worse solutions.

        Args:
            temperature: Probability of accepting worse solution

        Returns:
            True if move accepted
        """
        neighbors = self.generate_neighbors(self.current_solution.state, 1)
        neighbor = neighbors[0]
        neighbor_fitness = self.objective_function(neighbor)

        delta = neighbor_fitness - self.current_solution.fitness

        if delta > 0 or random.random() < temperature:
            self.current_solution = Solution(neighbor, neighbor_fitness, self.iteration)
            return True

        return False

    def late_acceptance_hill_climb(self) -> bool:
        """
        Late acceptance hill climbing - compares with historical fitness.

        Returns:
            True if move accepted
        """
        neighbors = self.generate_neighbors(self.current_solution.state, 1)
        neighbor = neighbors[0]
        neighbor_fitness = self.objective_function(neighbor)

        # Initialize history
        if not self.acceptance_history:
            self.acceptance_history = [self.current_solution.fitness] * self.acceptance_history_length

        # Compare with historical fitness
        v = self.iteration % self.acceptance_history_length
        if neighbor_fitness >= self.acceptance_history[v]:
            self.current_solution = Solution(neighbor, neighbor_fitness, self.iteration)
            self.acceptance_history[v] = neighbor_fitness
            return True

        return False

    def variable_neighborhood_hill_climb(self) -> bool:
        """
        Variable neighborhood - changes neighborhood structure.

        Returns:
            True if improvement found
        """
        improvement_found = False

        # Try different neighborhood sizes
        neighborhood_sizes = [0.01, 0.05, 0.1, 0.2, 0.5]

        for size in neighborhood_sizes:
            old_size = self.neighborhood_size
            self.neighborhood_size = size

            # Try with current neighborhood
            neighbors = self.generate_neighbors(self.current_solution.state, 10)

            for neighbor in neighbors:
                fitness = self.objective_function(neighbor)
                if fitness > self.current_solution.fitness:
                    self.current_solution = Solution(neighbor, fitness, self.iteration)
                    improvement_found = True
                    break

            self.neighborhood_size = old_size

            if improvement_found:
                break

        return improvement_found

    def step(self) -> bool:
        """
        Perform one hill climbing step based on variant.

        Returns:
            True if improvement found or move accepted
        """
        if self.variant == HillClimbingVariant.SIMPLE:
            return self.simple_hill_climb()
        elif self.variant == HillClimbingVariant.STEEPEST:
            return self.steepest_ascent_hill_climb()
        elif self.variant == HillClimbingVariant.STOCHASTIC:
            return self.stochastic_hill_climb()
        elif self.variant == HillClimbingVariant.FIRST_CHOICE:
            return self.first_choice_hill_climb()
        elif self.variant == HillClimbingVariant.SIMULATED:
            temperature = 1.0 - (self.iteration / self.max_iterations)
            return self.simulated_hill_climb(temperature)
        elif self.variant == HillClimbingVariant.VARIABLE_NEIGHBORHOOD:
            return self.variable_neighborhood_hill_climb()
        elif self.variant == HillClimbingVariant.LATE_ACCEPTANCE:
            return self.late_acceptance_hill_climb()
        else:
            return self.steepest_ascent_hill_climb()

    def run(self, verbose: bool = True) -> Tuple[Any, float]:
        """
        Run hill climbing algorithm.

        Args:
            verbose: Print progress

        Returns:
            Best solution and its fitness
        """
        # Initialize
        initial_fitness = self.objective_function(self.initial_solution)
        self.current_solution = Solution(self.initial_solution, initial_fitness, 0)
        self.best_solution = Solution(
            copy.deepcopy(self.initial_solution),
            initial_fitness,
            0
        )

        if verbose:
            print(f"Starting {self.variant.value} Hill Climbing")
            print(f"Initial fitness: {initial_fitness:.6f}")

        plateau_count = 0
        improvements = 0

        # Main loop
        for iteration in range(self.max_iterations):
            self.iteration = iteration

            # Perform step
            improved = self.step()

            if improved:
                improvements += 1
                plateau_count = 0

                # Update best
                if self.current_solution.fitness > self.best_solution.fitness:
                    self.best_solution = Solution(
                        copy.deepcopy(self.current_solution.state),
                        self.current_solution.fitness,
                        iteration
                    )
            else:
                plateau_count += 1

            # Update history
            self.history['fitness'].append(self.current_solution.fitness)
            self.history['improvements'].append(improvements)
            self.history['plateau_length'].append(plateau_count)
            self.history['neighborhood_size'].append(self.neighborhood_size)

            # Print progress
            if verbose and iteration % 100 == 0:
                print(f"Iteration {iteration}: Current = {self.current_solution.fitness:.6f}, "
                      f"Best = {self.best_solution.fitness:.6f}, "
                      f"Plateau = {plateau_count}")

            # Early stopping for simple variants
            if self.variant in [HillClimbingVariant.SIMPLE, HillClimbingVariant.STEEPEST]:
                if plateau_count >= 50:  # No improvement for 50 iterations
                    if verbose:
                        print(f"Stopped at iteration {iteration} (plateau)")
                    break

        if verbose:
            print(f"\nHill Climbing completed after {iteration + 1} iterations")
            print(f"Best fitness: {self.best_solution.fitness:.6f}")
            print(f"Total improvements: {improvements}")

        return self.best_solution.state, self.best_solution.fitness


class RandomRestartHillClimbing:
    """
    Random Restart Hill Climbing.

    Performs multiple hill climbing runs from random starting points.
    """

    def __init__(self,
                 objective_function: Callable,
                 solution_generator: Callable,
                 n_restarts: int = 10,
                 **hc_kwargs):
        """
        Initialize Random Restart Hill Climbing.

        Args:
            objective_function: Function to optimize
            solution_generator: Function to generate random solutions
            n_restarts: Number of restarts
            **hc_kwargs: Arguments for hill climbing
        """
        self.objective_function = objective_function
        self.solution_generator = solution_generator
        self.n_restarts = n_restarts
        self.hc_kwargs = hc_kwargs

        self.best_solution = None
        self.best_fitness = -float('inf')
        self.restart_results = []

    def run(self, verbose: bool = True) -> Tuple[Any, float]:
        """Run random restart hill climbing."""
        if verbose:
            print(f"Starting Random Restart Hill Climbing with {self.n_restarts} restarts")

        for restart in range(self.n_restarts):
            # Generate random starting point
            initial = self.solution_generator()

            # Run hill climbing
            hc = HillClimbing(
                objective_function=self.objective_function,
                initial_solution=initial,
                **self.hc_kwargs
            )

            solution, fitness = hc.run(verbose=False)

            self.restart_results.append({
                'restart': restart,
                'solution': solution,
                'fitness': fitness,
                'iterations': hc.iteration
            })

            # Update best
            if fitness > self.best_fitness:
                self.best_fitness = fitness
                self.best_solution = solution

            if verbose:
                print(f"Restart {restart + 1}: Fitness = {fitness:.6f}, "
                      f"Best so far = {self.best_fitness:.6f}")

        if verbose:
            print(f"\nRandom Restart completed")
            print(f"Best fitness: {self.best_fitness:.6f}")

            # Statistics
            fitnesses = [r['fitness'] for r in self.restart_results]
            print(f"Average fitness: {np.mean(fitnesses):.6f}")
            print(f"Std deviation: {np.std(fitnesses):.6f}")

        return self.best_solution, self.best_fitness


class GuidedLocalSearch:
    """
    Guided Local Search - Uses penalties to escape local optima.

    Augments objective function with penalties for frequently visited features.
    """

    def __init__(self,
                 objective_function: Callable,
                 feature_function: Callable,
                 initial_solution: Any,
                 lambda_param: float = 0.3,
                 **hc_kwargs):
        """
        Initialize Guided Local Search.

        Args:
            objective_function: Original objective
            feature_function: Function to extract features from solution
            initial_solution: Starting solution
            lambda_param: Penalty weighting parameter
            **hc_kwargs: Hill climbing parameters
        """
        self.objective_function = objective_function
        self.feature_function = feature_function
        self.initial_solution = initial_solution
        self.lambda_param = lambda_param
        self.hc_kwargs = hc_kwargs

        # Penalty tracking
        self.penalties = {}
        self.feature_costs = {}

    def augmented_objective(self, solution: Any) -> float:
        """Objective function augmented with penalties."""
        original_fitness = self.objective_function(solution)

        # Calculate penalty term
        features = self.feature_function(solution)
        penalty = 0

        for feature in features:
            if feature in self.penalties:
                penalty -= self.lambda_param * self.penalties[feature]

        return original_fitness + penalty

    def update_penalties(self, solution: Any):
        """Update penalties based on current local optimum."""
        features = self.feature_function(solution)

        # Calculate utility of penalizing each feature
        utilities = {}
        for feature in features:
            if feature not in self.feature_costs:
                self.feature_costs[feature] = 1.0  # Default cost

            penalty_count = self.penalties.get(feature, 0)
            utility = self.feature_costs[feature] / (1 + penalty_count)
            utilities[feature] = utility

        # Penalize feature with maximum utility
        if utilities:
            max_feature = max(utilities, key=utilities.get)
            self.penalties[max_feature] = self.penalties.get(max_feature, 0) + 1

    def run(self, max_iterations: int = 100, verbose: bool = True) -> Tuple[Any, float]:
        """Run guided local search."""
        if verbose:
            print("Starting Guided Local Search")

        best_solution = self.initial_solution
        best_fitness = self.objective_function(self.initial_solution)

        for iteration in range(max_iterations):
            # Run hill climbing with augmented objective
            hc = HillClimbing(
                objective_function=self.augmented_objective,
                initial_solution=best_solution,
                **self.hc_kwargs
            )

            local_optimum, _ = hc.run(verbose=False)

            # Evaluate with original objective
            fitness = self.objective_function(local_optimum)

            if fitness > best_fitness:
                best_fitness = fitness
                best_solution = local_optimum

            # Update penalties to escape local optimum
            self.update_penalties(local_optimum)

            if verbose and iteration % 10 == 0:
                print(f"Iteration {iteration}: Best = {best_fitness:.6f}, "
                      f"Penalties = {len(self.penalties)}")

        if verbose:
            print(f"\nGuided Local Search completed")
            print(f"Best fitness: {best_fitness:.6f}")

        return best_solution, best_fitness


def continuous_optimization_example():
    """Example: Optimize continuous functions."""
    print("=" * 60)
    print("HILL CLIMBING - CONTINUOUS OPTIMIZATION")
    print("=" * 60)

    # Sphere function (simple convex)
    def sphere(x: np.ndarray) -> float:
        """Sphere function - single global optimum."""
        return -np.sum(x**2)

    # Test different variants
    variants = [
        HillClimbingVariant.SIMPLE,
        HillClimbingVariant.STEEPEST,
        HillClimbingVariant.STOCHASTIC,
        HillClimbingVariant.SIMULATED,
        HillClimbingVariant.LATE_ACCEPTANCE
    ]

    initial = np.random.uniform(-5, 5, 10)
    results = {}

    for variant in variants:
        print(f"\nTesting {variant.value}...")

        hc = HillClimbing(
            objective_function=sphere,
            initial_solution=initial.copy(),
            variant=variant,
            max_iterations=500,
            neighborhood_size=0.1
        )

        solution, fitness = hc.run(verbose=False)
        results[variant.value] = fitness

        print(f"Final fitness: {fitness:.6f}")
        print(f"Distance from optimal: {np.linalg.norm(solution):.6f}")

    print("\n" + "-" * 40)
    print("VARIANT COMPARISON:")
    for variant, fitness in sorted(results.items(), key=lambda x: -x[1]):
        print(f"{variant:20s}: {fitness:.6f}")


def discrete_optimization_example():
    """Example: N-Queens problem using hill climbing."""
    print("\n" + "=" * 60)
    print("HILL CLIMBING - N-QUEENS PROBLEM")
    print("=" * 60)

    n = 8  # 8-queens

    def count_conflicts(queens: List[int]) -> int:
        """Count number of queen conflicts."""
        conflicts = 0
        n = len(queens)

        for i in range(n):
            for j in range(i + 1, n):
                # Check if queens attack each other
                if queens[i] == queens[j]:  # Same row
                    conflicts += 1
                elif abs(queens[i] - queens[j]) == abs(i - j):  # Diagonal
                    conflicts += 1

        return conflicts

    def queens_fitness(queens: List[int]) -> float:
        """Fitness is negative conflicts (maximize to minimize conflicts)."""
        return -count_conflicts(queens)

    def queens_neighbor(queens: List[int]) -> List[int]:
        """Generate neighbor by moving one queen."""
        neighbor = queens.copy()
        col = random.randint(0, len(queens) - 1)
        neighbor[col] = random.randint(0, len(queens) - 1)
        return neighbor

    # Random initial placement
    initial = [random.randint(0, n-1) for _ in range(n)]

    print(f"Initial conflicts: {count_conflicts(initial)}")

    # Simple hill climbing
    hc = HillClimbing(
        objective_function=queens_fitness,
        initial_solution=initial,
        neighbor_function=queens_neighbor,
        variant=HillClimbingVariant.STEEPEST,
        max_iterations=1000,
        max_neighbors=50
    )

    solution, fitness = hc.run(verbose=True)
    final_conflicts = count_conflicts(solution)

    print(f"\nFinal solution: {solution}")
    print(f"Final conflicts: {final_conflicts}")

    if final_conflicts == 0:
        print("Solution found! Board configuration:")
        for row in range(n):
            line = ""
            for col in range(n):
                if solution[col] == row:
                    line += "Q "
                else:
                    line += ". "
            print(line)


def random_restart_example():
    """Example: Random restart for multimodal function."""
    print("\n" + "=" * 60)
    print("RANDOM RESTART HILL CLIMBING")
    print("=" * 60)

    # Rastrigin function - highly multimodal
    def rastrigin(x: np.ndarray) -> float:
        """Rastrigin function - many local optima."""
        A = 10
        n = len(x)
        return -(A * n + np.sum(x**2 - A * np.cos(2 * np.pi * x)))

    def random_solution():
        """Generate random solution."""
        return np.random.uniform(-5.12, 5.12, 5)

    # Random restart
    rrhc = RandomRestartHillClimbing(
        objective_function=rastrigin,
        solution_generator=random_solution,
        n_restarts=20,
        variant=HillClimbingVariant.STEEPEST,
        max_iterations=200,
        neighborhood_size=0.1
    )

    best_solution, best_fitness = rrhc.run(verbose=True)

    print(f"\nBest solution: {best_solution}")
    print(f"Best fitness: {best_fitness:.6f}")
    print(f"Distance from global optimum: {np.linalg.norm(best_solution):.6f}")


def feature_selection_example():
    """Example: Feature selection using hill climbing."""
    print("\n" + "=" * 60)
    print("HILL CLIMBING - FEATURE SELECTION")
    print("=" * 60)

    # Simulated dataset
    np.random.seed(42)
    n_features = 20
    n_relevant = 5

    def feature_fitness(selected: np.ndarray) -> float:
        """Fitness for feature subset."""
        n_selected = np.sum(selected)

        if n_selected == 0:
            return -1000

        # Reward relevant features (first 5)
        relevant_score = np.sum(selected[:n_relevant])

        # Penalize irrelevant features
        irrelevant_penalty = np.sum(selected[n_relevant:])

        # Penalize too many features
        size_penalty = 0.01 * n_selected

        return relevant_score - 0.5 * irrelevant_penalty - size_penalty

    def feature_neighbor(selected: np.ndarray) -> np.ndarray:
        """Flip one feature."""
        neighbor = selected.copy()
        idx = random.randint(0, len(selected) - 1)
        neighbor[idx] = 1 - neighbor[idx]
        return neighbor

    # Start with random subset
    initial = np.random.randint(0, 2, n_features)

    hc = HillClimbing(
        objective_function=feature_fitness,
        initial_solution=initial,
        neighbor_function=feature_neighbor,
        variant=HillClimbingVariant.STEEPEST,
        max_iterations=500,
        max_neighbors=n_features
    )

    best_features, best_fitness = hc.run(verbose=True)

    selected_indices = np.where(best_features)[0]
    print(f"\nSelected features: {selected_indices}")
    print(f"Number selected: {len(selected_indices)}")
    print(f"Relevant features found: {len([i for i in selected_indices if i < n_relevant])}/{n_relevant}")


def guided_local_search_example():
    """Example: Guided local search for TSP."""
    print("\n" + "=" * 60)
    print("GUIDED LOCAL SEARCH - TSP")
    print("=" * 60)

    # Small TSP instance
    np.random.seed(42)
    n_cities = 15
    cities = np.random.rand(n_cities, 2) * 100

    # Distance matrix
    dist_matrix = np.zeros((n_cities, n_cities))
    for i in range(n_cities):
        for j in range(n_cities):
            dist_matrix[i, j] = np.linalg.norm(cities[i] - cities[j])

    def tsp_fitness(tour: List[int]) -> float:
        """TSP tour length (negative for maximization)."""
        length = 0
        for i in range(len(tour)):
            length += dist_matrix[tour[i], tour[(i + 1) % len(tour)]]
        return -length

    def tsp_neighbor(tour: List[int]) -> List[int]:
        """2-opt neighbor."""
        neighbor = tour.copy()
        i = random.randint(0, len(tour) - 2)
        j = random.randint(i + 1, len(tour) - 1)
        neighbor[i:j+1] = reversed(neighbor[i:j+1])
        return neighbor

    def tsp_features(tour: List[int]) -> List[Tuple[int, int]]:
        """Extract edges as features."""
        edges = []
        for i in range(len(tour)):
            edge = (tour[i], tour[(i + 1) % len(tour)])
            edges.append(tuple(sorted(edge)))
        return edges

    # Initial random tour
    initial_tour = list(range(n_cities))
    random.shuffle(initial_tour)

    # Guided local search
    gls = GuidedLocalSearch(
        objective_function=tsp_fitness,
        feature_function=tsp_features,
        initial_solution=initial_tour,
        lambda_param=0.1,
        neighbor_function=tsp_neighbor,
        variant=HillClimbingVariant.STEEPEST,
        max_iterations=100,
        max_neighbors=50
    )

    best_tour, best_fitness = gls.run(max_iterations=50, verbose=True)

    print(f"\nBest tour length: {-best_fitness:.2f}")
    print(f"Tour: {best_tour[:10]}...")


if __name__ == "__main__":
    # Run examples
    continuous_optimization_example()
    discrete_optimization_example()
    random_restart_example()
    feature_selection_example()
    guided_local_search_example()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Hill climbing is simple but gets stuck in local optima")
    print("- Steepest ascent is thorough but computationally expensive")
    print("- Random restart helps escape local optima")
    print("- Variable neighborhoods adapt to problem structure")
    print("- Guided local search uses memory to avoid revisiting")
    print("=" * 60)