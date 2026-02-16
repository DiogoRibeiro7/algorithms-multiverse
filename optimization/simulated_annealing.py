"""
Simulated Annealing Algorithm Implementation
============================================

A comprehensive implementation of simulated annealing for optimization problems.
Includes various cooling schedules, neighborhood generation strategies, and
adaptive mechanisms.

Features:
- Multiple cooling schedules (linear, exponential, logarithmic, adaptive)
- Support for continuous and discrete optimization
- Parallel tempering (replica exchange)
- Adaptive neighborhood sizing
- Restart mechanisms

Author: Claude
Date: January 2026
"""

import random
import numpy as np
import math
from typing import Callable, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import copy
import time


class CoolingSchedule(Enum):
    """Different temperature cooling schedules."""
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    LOGARITHMIC = "logarithmic"
    ADAPTIVE = "adaptive"
    FAST = "fast"
    BOLTZMANN = "boltzmann"


class NeighborhoodType(Enum):
    """Types of neighborhood generation."""
    RANDOM_SWAP = "random_swap"
    RANDOM_INSERTION = "random_insertion"
    RANDOM_REVERSAL = "random_reversal"
    GAUSSIAN_PERTURBATION = "gaussian_perturbation"
    UNIFORM_PERTURBATION = "uniform_perturbation"
    ADAPTIVE = "adaptive"


@dataclass
class SAState:
    """Represents a state in the simulated annealing process."""
    solution: Any
    energy: float
    temperature: float
    iteration: int
    accepted_moves: int = 0
    rejected_moves: int = 0


class SimulatedAnnealing:
    """
    General-purpose simulated annealing algorithm for optimization.

    Supports both minimization and maximization, various cooling schedules,
    and different neighborhood generation strategies.
    """

    def __init__(
        self,
        objective_function: Callable,
        initial_solution: Any,
        initial_temperature: float = 100.0,
        final_temperature: float = 1e-8,
        max_iterations: int = 10000,
        cooling_schedule: CoolingSchedule = CoolingSchedule.EXPONENTIAL,
        cooling_rate: float = 0.95,
        neighborhood_type: NeighborhoodType = NeighborhoodType.RANDOM_SWAP,
        neighborhood_size: float = 1.0,
        minimize: bool = True,
        restart_threshold: int = 1000,
        seed: Optional[int] = None
    ):
        """
        Initialize the simulated annealing algorithm.

        Args:
            objective_function: Function to optimize
            initial_solution: Starting solution
            initial_temperature: Starting temperature
            final_temperature: Stopping temperature
            max_iterations: Maximum iterations
            cooling_schedule: Type of cooling schedule
            cooling_rate: Rate of temperature decrease
            neighborhood_type: How to generate neighbors
            neighborhood_size: Size of neighborhood perturbation
            minimize: Whether to minimize or maximize
            restart_threshold: Iterations without improvement before restart
            seed: Random seed for reproducibility
        """
        self.objective_function = objective_function
        self.initial_solution = initial_solution
        self.initial_temperature = initial_temperature
        self.final_temperature = final_temperature
        self.max_iterations = max_iterations
        self.cooling_schedule = cooling_schedule
        self.cooling_rate = cooling_rate
        self.neighborhood_type = neighborhood_type
        self.neighborhood_size = neighborhood_size
        self.minimize = minimize
        self.restart_threshold = restart_threshold

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # State tracking
        self.current_state: Optional[SAState] = None
        self.best_state: Optional[SAState] = None
        self.temperature_history: List[float] = []
        self.energy_history: List[float] = []
        self.best_energy_history: List[float] = []
        self.acceptance_rate_history: List[float] = []

    def _evaluate_energy(self, solution: Any) -> float:
        """Evaluate the energy (objective) of a solution."""
        return self.objective_function(solution)

    def _accept_probability(self, current_energy: float, new_energy: float, temperature: float) -> float:
        """
        Calculate probability of accepting a worse solution.

        Uses the Metropolis-Hastings criterion.
        """
        if self.minimize:
            if new_energy < current_energy:
                return 1.0
            delta = new_energy - current_energy
        else:
            if new_energy > current_energy:
                return 1.0
            delta = current_energy - new_energy

        if temperature == 0:
            return 0.0

        return math.exp(-delta / temperature)

    def _linear_cooling(self, iteration: int) -> float:
        """Linear cooling schedule."""
        temp_range = self.initial_temperature - self.final_temperature
        return self.initial_temperature - (temp_range * iteration / self.max_iterations)

    def _exponential_cooling(self, iteration: int) -> float:
        """Exponential cooling schedule."""
        return self.initial_temperature * (self.cooling_rate ** iteration)

    def _logarithmic_cooling(self, iteration: int) -> float:
        """Logarithmic cooling schedule."""
        return self.initial_temperature / (1 + math.log(1 + iteration))

    def _fast_cooling(self, iteration: int) -> float:
        """Fast simulated annealing schedule."""
        return self.initial_temperature / (1 + iteration)

    def _boltzmann_cooling(self, iteration: int) -> float:
        """Boltzmann cooling schedule."""
        return self.initial_temperature / math.log(2 + iteration)

    def _adaptive_cooling(self, iteration: int, acceptance_rate: float) -> float:
        """
        Adaptive cooling based on acceptance rate.

        Slows cooling if acceptance rate is too low,
        speeds up if too high.
        """
        current_temp = self.current_state.temperature

        if acceptance_rate < 0.2:
            # Too few acceptances, slow down cooling
            return current_temp * 0.98
        elif acceptance_rate > 0.8:
            # Too many acceptances, speed up cooling
            return current_temp * 0.90
        else:
            # Normal cooling
            return current_temp * self.cooling_rate

    def _update_temperature(self, iteration: int) -> float:
        """Update temperature based on cooling schedule."""
        if self.cooling_schedule == CoolingSchedule.LINEAR:
            return self._linear_cooling(iteration)
        elif self.cooling_schedule == CoolingSchedule.EXPONENTIAL:
            return self._exponential_cooling(iteration)
        elif self.cooling_schedule == CoolingSchedule.LOGARITHMIC:
            return self._logarithmic_cooling(iteration)
        elif self.cooling_schedule == CoolingSchedule.FAST:
            return self._fast_cooling(iteration)
        elif self.cooling_schedule == CoolingSchedule.BOLTZMANN:
            return self._boltzmann_cooling(iteration)
        elif self.cooling_schedule == CoolingSchedule.ADAPTIVE:
            acceptance_rate = (self.current_state.accepted_moves /
                             max(1, self.current_state.accepted_moves + self.current_state.rejected_moves))
            return self._adaptive_cooling(iteration, acceptance_rate)
        else:
            return self._exponential_cooling(iteration)

    def _generate_neighbor(self, solution: Any) -> Any:
        """
        Generate a neighbor solution based on neighborhood type.

        This is a generic method that dispatches to specific strategies.
        """
        if isinstance(solution, list):
            return self._generate_list_neighbor(solution)
        elif isinstance(solution, np.ndarray):
            return self._generate_array_neighbor(solution)
        else:
            # Assume it's a numeric value
            return self._generate_numeric_neighbor(solution)

    def _generate_list_neighbor(self, solution: List) -> List:
        """Generate neighbor for list-based solutions (e.g., TSP)."""
        neighbor = solution.copy()

        if self.neighborhood_type == NeighborhoodType.RANDOM_SWAP:
            # Swap two random elements
            if len(neighbor) > 1:
                i, j = random.sample(range(len(neighbor)), 2)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

        elif self.neighborhood_type == NeighborhoodType.RANDOM_INSERTION:
            # Remove an element and insert it elsewhere
            if len(neighbor) > 1:
                i = random.randint(0, len(neighbor) - 1)
                element = neighbor.pop(i)
                j = random.randint(0, len(neighbor))
                neighbor.insert(j, element)

        elif self.neighborhood_type == NeighborhoodType.RANDOM_REVERSAL:
            # Reverse a random subsequence (2-opt)
            if len(neighbor) > 1:
                i, j = sorted(random.sample(range(len(neighbor)), 2))
                neighbor[i:j+1] = reversed(neighbor[i:j+1])

        return neighbor

    def _generate_array_neighbor(self, solution: np.ndarray) -> np.ndarray:
        """Generate neighbor for array-based solutions."""
        neighbor = solution.copy()

        if self.neighborhood_type == NeighborhoodType.GAUSSIAN_PERTURBATION:
            # Add Gaussian noise
            noise = np.random.normal(0, self.neighborhood_size, solution.shape)
            neighbor = solution + noise

        elif self.neighborhood_type == NeighborhoodType.UNIFORM_PERTURBATION:
            # Add uniform noise
            noise = np.random.uniform(-self.neighborhood_size, self.neighborhood_size, solution.shape)
            neighbor = solution + noise

        else:
            # Default to Gaussian
            noise = np.random.normal(0, self.neighborhood_size, solution.shape)
            neighbor = solution + noise

        return neighbor

    def _generate_numeric_neighbor(self, solution: Union[int, float]) -> Union[int, float]:
        """Generate neighbor for numeric solutions."""
        if isinstance(solution, int):
            # Integer perturbation
            return solution + random.randint(-max(1, int(self.neighborhood_size)),
                                            max(1, int(self.neighborhood_size)))
        else:
            # Float perturbation
            return solution + random.gauss(0, self.neighborhood_size)

    def run(self, verbose: bool = True) -> Tuple[Any, float]:
        """
        Run the simulated annealing algorithm.

        Args:
            verbose: Whether to print progress

        Returns:
            Best solution and its energy
        """
        # Initialize
        current_solution = copy.deepcopy(self.initial_solution)
        current_energy = self._evaluate_energy(current_solution)

        self.current_state = SAState(
            solution=current_solution,
            energy=current_energy,
            temperature=self.initial_temperature,
            iteration=0
        )

        self.best_state = copy.deepcopy(self.current_state)

        # Track iterations without improvement
        iterations_without_improvement = 0

        # Main annealing loop
        for iteration in range(self.max_iterations):
            # Update temperature
            temperature = self._update_temperature(iteration)
            self.current_state.temperature = temperature
            self.current_state.iteration = iteration

            # Check stopping criterion
            if temperature < self.final_temperature:
                if verbose:
                    print(f"Reached final temperature at iteration {iteration}")
                break

            # Generate neighbor
            neighbor_solution = self._generate_neighbor(self.current_state.solution)
            neighbor_energy = self._evaluate_energy(neighbor_solution)

            # Calculate acceptance probability
            accept_prob = self._accept_probability(
                self.current_state.energy,
                neighbor_energy,
                temperature
            )

            # Accept or reject
            if random.random() < accept_prob:
                # Accept the neighbor
                self.current_state.solution = neighbor_solution
                self.current_state.energy = neighbor_energy
                self.current_state.accepted_moves += 1

                # Update best if improved
                if self.minimize:
                    if neighbor_energy < self.best_state.energy:
                        self.best_state = copy.deepcopy(self.current_state)
                        iterations_without_improvement = 0
                    else:
                        iterations_without_improvement += 1
                else:
                    if neighbor_energy > self.best_state.energy:
                        self.best_state = copy.deepcopy(self.current_state)
                        iterations_without_improvement = 0
                    else:
                        iterations_without_improvement += 1
            else:
                # Reject the neighbor
                self.current_state.rejected_moves += 1
                iterations_without_improvement += 1

            # Store history
            self.temperature_history.append(temperature)
            self.energy_history.append(self.current_state.energy)
            self.best_energy_history.append(self.best_state.energy)

            # Calculate and store acceptance rate
            total_moves = self.current_state.accepted_moves + self.current_state.rejected_moves
            if total_moves > 0:
                acceptance_rate = self.current_state.accepted_moves / total_moves
                self.acceptance_rate_history.append(acceptance_rate)

            # Print progress
            if verbose and iteration % 100 == 0:
                acceptance_rate = self.current_state.accepted_moves / max(1, total_moves)
                print(f"Iteration {iteration}: T = {temperature:.4f}, "
                      f"Current = {self.current_state.energy:.6f}, "
                      f"Best = {self.best_state.energy:.6f}, "
                      f"Accept rate = {acceptance_rate:.2%}")

            # Restart if stuck
            if iterations_without_improvement > self.restart_threshold:
                if verbose:
                    print(f"Restarting at iteration {iteration} (no improvement for {self.restart_threshold} iterations)")

                # Reset temperature and perturb best solution
                self.current_state.temperature = self.initial_temperature * 0.5
                self.current_state.solution = self._generate_neighbor(self.best_state.solution)
                self.current_state.energy = self._evaluate_energy(self.current_state.solution)
                iterations_without_improvement = 0

        return self.best_state.solution, self.best_state.energy


class TSPSimulatedAnnealing:
    """
    Specialized simulated annealing for Traveling Salesman Problem.
    """

    def __init__(
        self,
        distance_matrix: np.ndarray,
        initial_temperature: Optional[float] = None,
        final_temperature: float = 0.01,
        cooling_rate: float = 0.995,
        max_iterations: int = 100000,
        seed: Optional[int] = None
    ):
        """
        Initialize TSP simulated annealing.

        Args:
            distance_matrix: Matrix of distances between cities
            initial_temperature: Starting temperature (auto-calculated if None)
            final_temperature: Stopping temperature
            cooling_rate: Temperature reduction factor
            max_iterations: Maximum iterations
            seed: Random seed
        """
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
        self.final_temperature = final_temperature
        self.cooling_rate = cooling_rate
        self.max_iterations = max_iterations

        # Auto-calculate initial temperature if not provided
        if initial_temperature is None:
            self.initial_temperature = self._estimate_initial_temperature()
        else:
            self.initial_temperature = initial_temperature

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

    def _calculate_tour_distance(self, tour: List[int]) -> float:
        """Calculate total distance of a tour."""
        distance = 0
        for i in range(len(tour)):
            from_city = tour[i]
            to_city = tour[(i + 1) % len(tour)]
            distance += self.distance_matrix[from_city][to_city]
        return distance

    def _estimate_initial_temperature(self) -> float:
        """Estimate good initial temperature based on random sampling."""
        sample_size = min(100, self.num_cities * 10)
        distances = []

        for _ in range(sample_size):
            tour = list(range(self.num_cities))
            random.shuffle(tour)
            distances.append(self._calculate_tour_distance(tour))

        # Set initial temperature to accept ~80% of moves initially
        std_dev = np.std(distances)
        return std_dev * 2

    def _two_opt_neighbor(self, tour: List[int]) -> List[int]:
        """Generate neighbor using 2-opt move."""
        neighbor = tour.copy()
        i, j = sorted(random.sample(range(len(tour)), 2))
        neighbor[i:j+1] = reversed(neighbor[i:j+1])
        return neighbor

    def _three_opt_neighbor(self, tour: List[int]) -> List[int]:
        """Generate neighbor using 3-opt move."""
        neighbor = tour.copy()
        n = len(tour)

        # Select three edges to remove
        edges = sorted(random.sample(range(n), 3))
        i, j, k = edges

        # Try different reconnection patterns
        patterns = [
            # Pattern 1: reverse segment 1
            lambda t: t[:i] + t[i:j][::-1] + t[j:k] + t[k:],
            # Pattern 2: reverse segment 2
            lambda t: t[:i] + t[i:j] + t[j:k][::-1] + t[k:],
            # Pattern 3: reverse both segments
            lambda t: t[:i] + t[i:j][::-1] + t[j:k][::-1] + t[k:],
            # Pattern 4: swap segments
            lambda t: t[:i] + t[j:k] + t[i:j] + t[k:],
        ]

        # Choose random pattern
        pattern = random.choice(patterns)
        return pattern(neighbor)

    def run(self, initial_tour: Optional[List[int]] = None, verbose: bool = True) -> Tuple[List[int], float]:
        """
        Run TSP simulated annealing.

        Args:
            initial_tour: Starting tour (random if None)
            verbose: Whether to print progress

        Returns:
            Best tour and its distance
        """
        # Initialize tour
        if initial_tour is None:
            current_tour = list(range(self.num_cities))
            random.shuffle(current_tour)
        else:
            current_tour = initial_tour.copy()

        current_distance = self._calculate_tour_distance(current_tour)
        best_tour = current_tour.copy()
        best_distance = current_distance

        temperature = self.initial_temperature

        # Main loop
        for iteration in range(self.max_iterations):
            # Generate neighbor
            if random.random() < 0.8:
                neighbor_tour = self._two_opt_neighbor(current_tour)
            else:
                neighbor_tour = self._three_opt_neighbor(current_tour)

            neighbor_distance = self._calculate_tour_distance(neighbor_tour)

            # Accept or reject
            delta = neighbor_distance - current_distance
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current_tour = neighbor_tour
                current_distance = neighbor_distance

                # Update best
                if current_distance < best_distance:
                    best_tour = current_tour.copy()
                    best_distance = current_distance

            # Cool down
            temperature *= self.cooling_rate

            # Stop if temperature too low
            if temperature < self.final_temperature:
                break

            # Print progress
            if verbose and iteration % 1000 == 0:
                print(f"Iteration {iteration}: T = {temperature:.4f}, "
                      f"Current = {current_distance:.2f}, Best = {best_distance:.2f}")

        return best_tour, best_distance


class ParallelTempering:
    """
    Parallel tempering (replica exchange) for enhanced exploration.

    Runs multiple SA instances at different temperatures and exchanges states.
    """

    def __init__(
        self,
        objective_function: Callable,
        initial_solution: Any,
        num_replicas: int = 4,
        min_temperature: float = 0.1,
        max_temperature: float = 100.0,
        exchange_interval: int = 100,
        max_iterations: int = 10000,
        minimize: bool = True,
        seed: Optional[int] = None
    ):
        """
        Initialize parallel tempering.

        Args:
            objective_function: Function to optimize
            initial_solution: Starting solution
            num_replicas: Number of temperature replicas
            min_temperature: Minimum temperature
            max_temperature: Maximum temperature
            exchange_interval: Iterations between exchange attempts
            max_iterations: Maximum iterations
            minimize: Whether to minimize
            seed: Random seed
        """
        self.objective_function = objective_function
        self.initial_solution = initial_solution
        self.num_replicas = num_replicas
        self.exchange_interval = exchange_interval
        self.max_iterations = max_iterations
        self.minimize = minimize

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # Create temperature ladder (geometric spacing)
        self.temperatures = np.geomspace(min_temperature, max_temperature, num_replicas)

        # Create replicas
        self.replicas = []
        for temp in self.temperatures:
            replica = SimulatedAnnealing(
                objective_function=objective_function,
                initial_solution=copy.deepcopy(initial_solution),
                initial_temperature=temp,
                final_temperature=temp * 0.99,  # Keep temperature relatively constant
                max_iterations=exchange_interval,
                minimize=minimize
            )
            self.replicas.append(replica)

    def _exchange_probability(self, energy1: float, energy2: float, temp1: float, temp2: float) -> float:
        """Calculate probability of exchanging two replicas."""
        if self.minimize:
            delta = (energy2 - energy1) * (1/temp1 - 1/temp2)
        else:
            delta = (energy1 - energy2) * (1/temp1 - 1/temp2)

        return min(1.0, math.exp(delta))

    def run(self, verbose: bool = True) -> Tuple[Any, float]:
        """
        Run parallel tempering.

        Returns:
            Best solution and its energy
        """
        best_solution = copy.deepcopy(self.initial_solution)
        best_energy = self.objective_function(best_solution)

        num_exchanges = self.max_iterations // self.exchange_interval

        for exchange_round in range(num_exchanges):
            # Run each replica for exchange_interval iterations
            for i, replica in enumerate(self.replicas):
                solution, energy = replica.run(verbose=False)

                # Update global best
                if self.minimize:
                    if energy < best_energy:
                        best_solution = copy.deepcopy(solution)
                        best_energy = energy
                else:
                    if energy > best_energy:
                        best_solution = copy.deepcopy(solution)
                        best_energy = energy

            # Attempt replica exchanges
            for i in range(self.num_replicas - 1):
                # Try to exchange replicas i and i+1
                energy1 = self.replicas[i].best_state.energy
                energy2 = self.replicas[i+1].best_state.energy
                temp1 = self.temperatures[i]
                temp2 = self.temperatures[i+1]

                exchange_prob = self._exchange_probability(energy1, energy2, temp1, temp2)

                if random.random() < exchange_prob:
                    # Exchange solutions
                    self.replicas[i].initial_solution, self.replicas[i+1].initial_solution = \
                        self.replicas[i+1].best_state.solution, self.replicas[i].best_state.solution

            if verbose and exchange_round % 10 == 0:
                energies = [r.best_state.energy for r in self.replicas]
                print(f"Exchange round {exchange_round}: Best = {best_energy:.6f}, "
                      f"Replica energies = {[f'{e:.2f}' for e in energies]}")

        return best_solution, best_energy


def example_usage():
    """Demonstrate simulated annealing functionality."""
    print("=" * 60)
    print("SIMULATED ANNEALING EXAMPLES")
    print("=" * 60)

    # Example 1: Function optimization
    print("\n1. Continuous Function Optimization (Ackley Function):")
    print("-" * 40)

    def ackley(x):
        """Ackley function - multimodal test function."""
        n = len(x)
        sum1 = sum(xi**2 for xi in x)
        sum2 = sum(np.cos(2*np.pi*xi) for xi in x)
        return -20 * np.exp(-0.2 * np.sqrt(sum1/n)) - np.exp(sum2/n) + 20 + np.e

    # Initial solution
    initial = np.random.uniform(-5, 5, 5)

    sa = SimulatedAnnealing(
        objective_function=ackley,
        initial_solution=initial,
        initial_temperature=10.0,
        final_temperature=0.01,
        max_iterations=5000,
        cooling_schedule=CoolingSchedule.EXPONENTIAL,
        cooling_rate=0.99,
        neighborhood_type=NeighborhoodType.GAUSSIAN_PERTURBATION,
        neighborhood_size=0.5,
        minimize=True,
        seed=42
    )

    best_solution, best_energy = sa.run(verbose=False)
    print(f"Best solution: {[f'{x:.4f}' for x in best_solution]}")
    print(f"Best energy: {best_energy:.6f}")
    print(f"(Global optimum is at [0,0,0,0,0] with energy 0)")

    # Example 2: TSP
    print("\n2. Traveling Salesman Problem:")
    print("-" * 40)

    # Create TSP instance
    np.random.seed(42)
    num_cities = 15
    cities = np.random.rand(num_cities, 2) * 100

    # Distance matrix
    distance_matrix = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                distance_matrix[i][j] = np.linalg.norm(cities[i] - cities[j])

    tsp_sa = TSPSimulatedAnnealing(
        distance_matrix=distance_matrix,
        cooling_rate=0.995,
        max_iterations=10000,
        seed=42
    )

    best_tour, best_distance = tsp_sa.run(verbose=False)
    print(f"Best tour found: {best_tour[:8]}...")
    print(f"Tour distance: {best_distance:.2f}")

    # Example 3: Discrete optimization (Graph coloring simulation)
    print("\n3. Discrete Optimization (Pseudo Graph Coloring):")
    print("-" * 40)

    def graph_coloring_cost(coloring):
        """Simulated cost function for graph coloring."""
        # Simulate conflicts (lower is better)
        conflicts = 0
        n = len(coloring)
        for i in range(n):
            for j in range(i+1, n):
                # Simulate edge probability
                if (i + j) % 3 == 0:  # Simulated edge
                    if coloring[i] == coloring[j]:
                        conflicts += 1
        return conflicts

    # Initial random coloring (4 colors for 10 nodes)
    initial_coloring = [random.randint(0, 3) for _ in range(10)]

    sa_discrete = SimulatedAnnealing(
        objective_function=graph_coloring_cost,
        initial_solution=initial_coloring,
        initial_temperature=5.0,
        final_temperature=0.01,
        max_iterations=2000,
        neighborhood_type=NeighborhoodType.RANDOM_SWAP,
        minimize=True,
        seed=42
    )

    best_coloring, best_conflicts = sa_discrete.run(verbose=False)
    print(f"Best coloring: {best_coloring}")
    print(f"Number of conflicts: {int(best_conflicts)}")

    # Example 4: Parallel tempering
    print("\n4. Parallel Tempering (Enhanced Exploration):")
    print("-" * 40)

    def rosenbrock(x):
        """Rosenbrock function - narrow valley."""
        return sum(100*(x[i+1] - x[i]**2)**2 + (1 - x[i])**2
                  for i in range(len(x)-1))

    initial = np.random.uniform(-2, 2, 4)

    pt = ParallelTempering(
        objective_function=rosenbrock,
        initial_solution=initial,
        num_replicas=4,
        min_temperature=0.01,
        max_temperature=10.0,
        exchange_interval=100,
        max_iterations=2000,
        minimize=True,
        seed=42
    )

    best_solution, best_energy = pt.run(verbose=False)
    print(f"Best solution: {[f'{x:.4f}' for x in best_solution]}")
    print(f"Best energy: {best_energy:.6f}")
    print(f"(Global optimum is at [1,1,1,1] with energy 0)")

    # Example 5: Adaptive cooling demonstration
    print("\n5. Adaptive Cooling Schedule:")
    print("-" * 40)

    def sphere(x):
        """Simple sphere function."""
        return sum(xi**2 for xi in x)

    initial = np.random.uniform(-10, 10, 3)

    sa_adaptive = SimulatedAnnealing(
        objective_function=sphere,
        initial_solution=initial,
        initial_temperature=50.0,
        cooling_schedule=CoolingSchedule.ADAPTIVE,
        max_iterations=1000,
        neighborhood_type=NeighborhoodType.GAUSSIAN_PERTURBATION,
        neighborhood_size=1.0,
        minimize=True,
        seed=42
    )

    best_solution, best_energy = sa_adaptive.run(verbose=False)

    # Show temperature and acceptance rate evolution
    print("Temperature evolution (first 10 and last 10):")
    temps = sa_adaptive.temperature_history
    for i in [0, 1, 2, 3, 4, -5, -4, -3, -2, -1]:
        if abs(i) < len(temps):
            print(f"  Iteration {i if i >= 0 else len(temps)+i}: T = {temps[i]:.4f}")

    print(f"\nFinal solution: {[f'{x:.4f}' for x in best_solution]}")
    print(f"Final energy: {best_energy:.6f}")

    # Show annealing progress
    print("\n6. Annealing Progress Visualization:")
    print("-" * 40)

    # Run with tracking
    initial = [5.0, 5.0, 5.0]
    sa_vis = SimulatedAnnealing(
        objective_function=sphere,
        initial_solution=initial,
        initial_temperature=10.0,
        cooling_rate=0.95,
        max_iterations=500,
        neighborhood_type=NeighborhoodType.GAUSSIAN_PERTURBATION,
        minimize=True,
        seed=42
    )

    sa_vis.run(verbose=False)

    # Visualize energy over time
    print("Energy reduction over time:")
    energy_hist = sa_vis.energy_history
    for i in range(0, len(energy_hist), 50):
        energy = energy_hist[i]
        bar_length = int(50 * (1 - energy / energy_hist[0]))
        bar = '=' * bar_length + '-' * (50 - bar_length)
        print(f"Iter {i:3d}: [{bar}] {energy:.4f}")

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- SA can escape local optima through probabilistic acceptance")
    print("- Temperature schedule is crucial for performance")
    print("- Higher temperatures allow more exploration")
    print("- Neighborhood generation affects solution quality")
    print("- Parallel tempering improves global search")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()