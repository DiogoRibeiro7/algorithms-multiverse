"""
Simulated Annealing Algorithm Implementation
===========================================

A comprehensive implementation of Simulated Annealing (SA) for optimization problems.
SA is inspired by the annealing process in metallurgy where controlled cooling
allows materials to reach a minimum energy state.

Key Components:
- Temperature scheduling (linear, exponential, logarithmic, adaptive)
- Neighbor generation strategies
- Acceptance probability (Metropolis criterion)
- Reheating and restart strategies
- Parallel tempering

Applications:
- Combinatorial optimization
- Continuous optimization
- Machine learning hyperparameter tuning
- VLSI design
- Scheduling problems

Author: Claude
Date: January 2026
"""

import random
import numpy as np
import math
from typing import Callable, Optional, Any, List, Tuple, Dict, Union
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import copy


class CoolingSchedule(Enum):
    """Temperature cooling schedules."""
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    LOGARITHMIC = "logarithmic"
    ADAPTIVE = "adaptive"
    GEOMETRIC = "geometric"
    FAST = "fast"


class NeighborStrategy(Enum):
    """Strategies for generating neighbor solutions."""
    RANDOM_SWAP = "random_swap"
    RANDOM_FLIP = "random_flip"
    GAUSSIAN_PERTURBATION = "gaussian_perturbation"
    LOCAL_SEARCH = "local_search"
    VARIABLE_NEIGHBORHOOD = "variable_neighborhood"


@dataclass
class Solution:
    """Represents a solution in the search space."""
    state: Any
    energy: float = float('inf')
    metadata: Dict = None


class TemperatureSchedule(ABC):
    """Abstract base class for temperature schedules."""

    @abstractmethod
    def get_temperature(self, iteration: int) -> float:
        """Get temperature at given iteration."""
        pass

    @abstractmethod
    def update(self, accept_rate: float = None):
        """Update schedule parameters if adaptive."""
        pass


class LinearCooling(TemperatureSchedule):
    """Linear temperature cooling."""

    def __init__(self, initial_temp: float, final_temp: float, max_iterations: int):
        self.initial_temp = initial_temp
        self.final_temp = final_temp
        self.max_iterations = max_iterations

    def get_temperature(self, iteration: int) -> float:
        """Calculate temperature at given iteration using linear cooling."""
        if iteration >= self.max_iterations:
            return self.final_temp
        return self.initial_temp - (self.initial_temp - self.final_temp) * (iteration / self.max_iterations)

    def update(self, accept_rate: float = None):
        """Update temperature schedule (no-op for linear cooling)."""
        pass  # Not adaptive


class ExponentialCooling(TemperatureSchedule):
    """Exponential temperature cooling."""

    def __init__(self, initial_temp: float, cooling_rate: float = 0.95):
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.current_temp = initial_temp

    def get_temperature(self, iteration: int) -> float:
        """Calculate temperature at given iteration using exponential decay."""
        return self.initial_temp * (self.cooling_rate ** iteration)

    def update(self, accept_rate: float = None):
        """Update temperature schedule (no-op for exponential cooling)."""
        pass  # Not adaptive


class LogarithmicCooling(TemperatureSchedule):
    """Logarithmic temperature cooling (very slow)."""

    def __init__(self, initial_temp: float, cooling_constant: float = 1.0):
        self.initial_temp = initial_temp
        self.cooling_constant = cooling_constant

    def get_temperature(self, iteration: int) -> float:
        """Calculate temperature at given iteration using logarithmic cooling."""
        return self.initial_temp / (1 + self.cooling_constant * math.log(1 + iteration))

    def update(self, accept_rate: float = None):
        """Update temperature schedule (no-op for logarithmic cooling)."""
        pass  # Not adaptive


class AdaptiveCooling(TemperatureSchedule):
    """Adaptive temperature cooling based on acceptance rate."""

    def __init__(self, initial_temp: float, target_accept_rate: float = 0.4):
        self.current_temp = initial_temp
        self.target_accept_rate = target_accept_rate
        self.adaptation_rate = 0.1

    def get_temperature(self, iteration: int) -> float:
        """Return current adaptive temperature."""
        return self.current_temp

    def update(self, accept_rate: float = None):
        """Adjust temperature based on acceptance rate."""
        if accept_rate is not None:
            if accept_rate < self.target_accept_rate:
                # Too few acceptances, increase temperature
                self.current_temp *= (1 + self.adaptation_rate)
            elif accept_rate > self.target_accept_rate * 1.5:
                # Too many acceptances, decrease temperature
                self.current_temp *= (1 - self.adaptation_rate)


class SimulatedAnnealing:
    """
    Main Simulated Annealing implementation.

    A probabilistic optimization algorithm that accepts worse solutions
    with decreasing probability as temperature decreases.
    """

    def __init__(self,
                 objective_function: Callable,
                 initial_solution: Any,
                 neighbor_function: Optional[Callable] = None,
                 cooling_schedule: CoolingSchedule = CoolingSchedule.EXPONENTIAL,
                 initial_temp: float = 100.0,
                 final_temp: float = 0.01,
                 max_iterations: int = 10000,
                 cooling_rate: float = 0.95,
                 min_acceptance_rate: float = 0.001):
        """
        Initialize Simulated Annealing algorithm.

        Args:
            objective_function: Function to minimize
            initial_solution: Starting solution
            neighbor_function: Function to generate neighbor solutions
            cooling_schedule: Temperature reduction strategy
            initial_temp: Starting temperature
            final_temp: Minimum temperature before stopping
            max_iterations: Maximum number of iterations
            cooling_rate: Rate of temperature decrease
            min_acceptance_rate: Minimum acceptance rate before reheating
        """
        self.objective_function = objective_function
        self.initial_solution = initial_solution
        self.neighbor_function = neighbor_function
        self.cooling_schedule_type = cooling_schedule
        self.initial_temp = initial_temp
        self.final_temp = final_temp
        self.max_iterations = max_iterations
        self.cooling_rate = cooling_rate
        self.min_acceptance_rate = min_acceptance_rate

        # Initialize temperature schedule
        self.temperature_schedule = self._create_temperature_schedule()

        # Solution tracking
        self.current_solution = None
        self.best_solution = None
        self.history = {
            'energy': [],
            'best_energy': [],
            'temperature': [],
            'acceptance_rate': []
        }

        # Statistics
        self.accepted_moves = 0
        self.rejected_moves = 0
        self.iteration = 0

    def _create_temperature_schedule(self) -> TemperatureSchedule:
        """Create temperature schedule based on type."""
        if self.cooling_schedule_type == CoolingSchedule.LINEAR:
            return LinearCooling(self.initial_temp, self.final_temp, self.max_iterations)
        elif self.cooling_schedule_type == CoolingSchedule.EXPONENTIAL:
            return ExponentialCooling(self.initial_temp, self.cooling_rate)
        elif self.cooling_schedule_type == CoolingSchedule.LOGARITHMIC:
            return LogarithmicCooling(self.initial_temp)
        elif self.cooling_schedule_type == CoolingSchedule.ADAPTIVE:
            return AdaptiveCooling(self.initial_temp)
        else:
            return ExponentialCooling(self.initial_temp, self.cooling_rate)

    def _default_neighbor(self, solution: Any) -> Any:
        """Default neighbor generation for different data types."""
        if isinstance(solution, np.ndarray):
            # For arrays, perturb random elements
            neighbor = solution.copy()
            if solution.dtype == bool:
                # Binary array - flip random bits
                idx = random.randint(0, len(solution) - 1)
                neighbor[idx] = not neighbor[idx]
            elif np.issubdtype(solution.dtype, np.integer):
                # Integer array - swap two elements
                if len(solution) > 1:
                    i, j = random.sample(range(len(solution)), 2)
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            else:
                # Real-valued array - Gaussian perturbation
                idx = random.randint(0, len(solution) - 1)
                neighbor[idx] += np.random.normal(0, 0.1)
            return neighbor
        elif isinstance(solution, list):
            # For lists, swap two elements
            neighbor = solution.copy()
            if len(neighbor) > 1:
                i, j = random.sample(range(len(neighbor)), 2)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            return neighbor
        else:
            # For other types, use provided neighbor function
            raise ValueError("No neighbor function provided for this solution type")

    def acceptance_probability(self, current_energy: float, new_energy: float, temperature: float) -> float:
        """
        Calculate probability of accepting new solution.

        Uses Metropolis criterion: always accept better solutions,
        accept worse solutions with probability exp(-delta/T).
        """
        if new_energy <= current_energy:
            return 1.0

        if temperature <= 0:
            return 0.0

        return math.exp(-(new_energy - current_energy) / temperature)

    def anneal_step(self, temperature: float) -> bool:
        """
        Perform one annealing step.

        Returns:
            True if new solution was accepted
        """
        # Generate neighbor
        if self.neighbor_function:
            neighbor = self.neighbor_function(self.current_solution.state)
        else:
            neighbor = self._default_neighbor(self.current_solution.state)

        # Evaluate neighbor
        neighbor_energy = self.objective_function(neighbor)

        # Decide whether to accept
        accept_prob = self.acceptance_probability(
            self.current_solution.energy,
            neighbor_energy,
            temperature
        )

        if random.random() < accept_prob:
            # Accept new solution
            self.current_solution = Solution(neighbor, neighbor_energy)
            self.accepted_moves += 1

            # Update best solution if necessary
            if neighbor_energy < self.best_solution.energy:
                self.best_solution = Solution(
                    copy.deepcopy(neighbor),
                    neighbor_energy
                )

            return True
        else:
            self.rejected_moves += 1
            return False

    def run(self, verbose: bool = True,
            callback: Optional[Callable] = None) -> Solution:
        """
        Run the simulated annealing algorithm.

        Args:
            verbose: Print progress information
            callback: Optional callback function called each iteration

        Returns:
            Best solution found
        """
        # Initialize
        initial_energy = self.objective_function(self.initial_solution)
        self.current_solution = Solution(self.initial_solution, initial_energy)
        self.best_solution = Solution(
            copy.deepcopy(self.initial_solution),
            initial_energy
        )

        if verbose:
            print(f"Starting Simulated Annealing")
            print(f"Initial energy: {initial_energy:.6f}")
            print(f"Temperature: {self.initial_temp:.4f} -> {self.final_temp:.4f}")

        # Main annealing loop
        acceptance_window = []
        window_size = 100

        for iteration in range(self.max_iterations):
            self.iteration = iteration

            # Get current temperature
            temperature = self.temperature_schedule.get_temperature(iteration)

            # Stop if temperature too low
            if temperature < self.final_temp:
                if verbose:
                    print(f"Temperature {temperature:.6f} below final temp {self.final_temp:.6f}")
                break

            # Perform annealing step
            accepted = self.anneal_step(temperature)
            acceptance_window.append(accepted)

            # Keep window size fixed
            if len(acceptance_window) > window_size:
                acceptance_window.pop(0)

            # Calculate acceptance rate
            accept_rate = sum(acceptance_window) / len(acceptance_window)

            # Update adaptive schedule
            if self.cooling_schedule_type == CoolingSchedule.ADAPTIVE:
                self.temperature_schedule.update(accept_rate)

            # Store history
            self.history['energy'].append(self.current_solution.energy)
            self.history['best_energy'].append(self.best_solution.energy)
            self.history['temperature'].append(temperature)
            self.history['acceptance_rate'].append(accept_rate)

            # Callback
            if callback:
                callback(self, iteration)

            # Print progress
            if verbose and iteration % 1000 == 0:
                print(f"Iteration {iteration}: Energy = {self.current_solution.energy:.6f}, "
                      f"Best = {self.best_solution.energy:.6f}, "
                      f"Temp = {temperature:.4f}, "
                      f"Accept rate = {accept_rate:.3f}")

            # Check for restart conditions
            if accept_rate < self.min_acceptance_rate and iteration > window_size:
                if verbose:
                    print(f"Low acceptance rate {accept_rate:.4f}, considering restart")

        if verbose:
            print(f"\nSimulated Annealing completed after {iteration} iterations")
            print(f"Best energy: {self.best_solution.energy:.6f}")
            print(f"Acceptance rate: {self.accepted_moves}/{self.accepted_moves + self.rejected_moves} "
                  f"({100 * self.accepted_moves / (self.accepted_moves + self.rejected_moves):.1f}%)")

        return self.best_solution


class ParallelTempering:
    """
    Parallel Tempering (Replica Exchange) Simulated Annealing.

    Runs multiple SA instances at different temperatures and
    periodically exchanges solutions between them.
    """

    def __init__(self,
                 objective_function: Callable,
                 initial_solution: Any,
                 n_replicas: int = 4,
                 temp_range: Tuple[float, float] = (0.1, 100),
                 exchange_interval: int = 100,
                 **sa_kwargs):
        """
        Initialize Parallel Tempering.

        Args:
            objective_function: Function to minimize
            initial_solution: Starting solution
            n_replicas: Number of parallel replicas
            temp_range: Temperature range (min, max)
            exchange_interval: Iterations between exchange attempts
            **sa_kwargs: Additional arguments for SA instances
        """
        self.objective_function = objective_function
        self.n_replicas = n_replicas
        self.exchange_interval = exchange_interval

        # Create temperature ladder (geometric spacing)
        temps = np.geomspace(temp_range[0], temp_range[1], n_replicas)

        # Create SA instances at different temperatures
        self.replicas = []
        for i, temp in enumerate(temps):
            sa = SimulatedAnnealing(
                objective_function=objective_function,
                initial_solution=copy.deepcopy(initial_solution),
                initial_temp=temp,
                final_temp=temp * 0.01,  # Keep relative cooling
                cooling_schedule=CoolingSchedule.EXPONENTIAL,
                **sa_kwargs
            )
            self.replicas.append(sa)

        self.exchange_history = []

    def exchange_replicas(self):
        """Attempt to exchange solutions between adjacent replicas."""
        exchanges = 0

        for i in range(self.n_replicas - 1):
            # Get adjacent replicas
            replica1 = self.replicas[i]
            replica2 = self.replicas[i + 1]

            # Get current energies and temperatures
            E1 = replica1.current_solution.energy
            E2 = replica2.current_solution.energy
            T1 = replica1.temperature_schedule.get_temperature(replica1.iteration)
            T2 = replica2.temperature_schedule.get_temperature(replica2.iteration)

            # Calculate exchange probability (Metropolis criterion)
            delta = (E2 - E1) * (1/T1 - 1/T2)

            if delta <= 0 or random.random() < math.exp(-delta):
                # Exchange solutions
                replica1.current_solution, replica2.current_solution = \
                    replica2.current_solution, replica1.current_solution
                exchanges += 1

        self.exchange_history.append(exchanges)
        return exchanges

    def run(self, max_iterations: int = 10000, verbose: bool = True) -> Solution:
        """
        Run parallel tempering.

        Args:
            max_iterations: Maximum iterations per replica
            verbose: Print progress

        Returns:
            Best solution found across all replicas
        """
        if verbose:
            print(f"Starting Parallel Tempering with {self.n_replicas} replicas")

        best_solution = None
        best_energy = float('inf')

        for iteration in range(0, max_iterations, self.exchange_interval):
            # Run each replica for exchange_interval iterations
            for replica in self.replicas:
                # Run SA steps
                for _ in range(min(self.exchange_interval, max_iterations - iteration)):
                    temp = replica.temperature_schedule.get_temperature(replica.iteration)
                    replica.anneal_step(temp)
                    replica.iteration += 1

                # Update global best
                if replica.best_solution.energy < best_energy:
                    best_energy = replica.best_solution.energy
                    best_solution = replica.best_solution

            # Attempt exchanges
            exchanges = self.exchange_replicas()

            if verbose and iteration % 1000 == 0:
                energies = [r.current_solution.energy for r in self.replicas]
                print(f"Iteration {iteration}: Best = {best_energy:.6f}, "
                      f"Exchanges = {exchanges}, "
                      f"Energies = {[f'{e:.2f}' for e in energies]}")

        if verbose:
            print(f"\nParallel Tempering completed")
            print(f"Best energy: {best_energy:.6f}")
            print(f"Total exchanges: {sum(self.exchange_history)}")

        return best_solution


def optimize_function_example():
    """Example: Optimize a complex mathematical function."""
    print("=" * 60)
    print("SIMULATED ANNEALING - FUNCTION OPTIMIZATION")
    print("=" * 60)

    # Ackley function - highly multimodal
    def ackley(x: np.ndarray) -> float:
        """Ackley function - many local minima."""
        n = len(x)
        sum_sq = np.sum(x**2)
        sum_cos = np.sum(np.cos(2 * np.pi * x))

        term1 = -20 * np.exp(-0.2 * np.sqrt(sum_sq / n))
        term2 = -np.exp(sum_cos / n)

        return term1 + term2 + 20 + np.e

    # Neighbor function for continuous optimization
    def continuous_neighbor(x: np.ndarray, step_size: float = 0.5) -> np.ndarray:
        """Generate neighbor by Gaussian perturbation."""
        neighbor = x.copy()
        # Perturb random dimensions
        n_perturb = random.randint(1, max(1, len(x) // 3))
        indices = random.sample(range(len(x)), n_perturb)

        for idx in indices:
            neighbor[idx] += np.random.normal(0, step_size)
            neighbor[idx] = np.clip(neighbor[idx], -5, 5)  # Keep in bounds

        return neighbor

    # Initial solution
    initial = np.random.uniform(-5, 5, 10)

    # Create SA instance
    sa = SimulatedAnnealing(
        objective_function=ackley,
        initial_solution=initial,
        neighbor_function=continuous_neighbor,
        cooling_schedule=CoolingSchedule.EXPONENTIAL,
        initial_temp=10.0,
        final_temp=0.001,
        max_iterations=10000,
        cooling_rate=0.995
    )

    # Run optimization
    best = sa.run(verbose=True)

    print(f"\nBest solution found: {best.state}")
    print(f"Function value: {best.energy:.6f}")
    print(f"Global minimum is 0 at origin")
    print(f"Distance from optimal: {np.linalg.norm(best.state):.6f}")


def traveling_salesman_example():
    """Example: Solve TSP using Simulated Annealing."""
    print("\n" + "=" * 60)
    print("SIMULATED ANNEALING - TRAVELING SALESMAN PROBLEM")
    print("=" * 60)

    # Generate random cities
    np.random.seed(42)
    n_cities = 30
    cities = np.random.rand(n_cities, 2) * 100

    # Distance matrix
    dist_matrix = np.zeros((n_cities, n_cities))
    for i in range(n_cities):
        for j in range(n_cities):
            dist_matrix[i, j] = np.linalg.norm(cities[i] - cities[j])

    def tsp_cost(tour: List[int]) -> float:
        """Calculate total tour distance."""
        total = 0
        for i in range(len(tour)):
            total += dist_matrix[tour[i], tour[(i + 1) % len(tour)]]
        return total

    def tsp_neighbor(tour: List[int]) -> List[int]:
        """Generate neighbor using 2-opt swap."""
        new_tour = tour.copy()

        # Choose swap type
        if random.random() < 0.5:
            # 2-opt: reverse a segment
            i = random.randint(0, len(tour) - 2)
            j = random.randint(i + 1, len(tour) - 1)
            new_tour[i:j+1] = new_tour[i:j+1][::-1]
        else:
            # Or-opt: move a city to different position
            i = random.randint(0, len(tour) - 1)
            j = random.randint(0, len(tour) - 1)
            if i != j:
                city = new_tour.pop(i)
                new_tour.insert(j, city)

        return new_tour

    # Initial random tour
    initial_tour = list(range(n_cities))
    random.shuffle(initial_tour)

    # Create SA instance
    sa = SimulatedAnnealing(
        objective_function=tsp_cost,
        initial_solution=initial_tour,
        neighbor_function=tsp_neighbor,
        cooling_schedule=CoolingSchedule.ADAPTIVE,
        initial_temp=100.0,
        final_temp=0.01,
        max_iterations=50000,
        cooling_rate=0.99
    )

    # Run optimization
    best = sa.run(verbose=True)

    print(f"\nBest tour distance: {best.energy:.2f}")
    print(f"Tour: {best.state[:10]}...")  # Show first 10 cities


def scheduling_example():
    """Example: Job shop scheduling problem."""
    print("\n" + "=" * 60)
    print("SIMULATED ANNEALING - JOB SHOP SCHEDULING")
    print("=" * 60)

    # Simple job shop: 3 machines, 5 jobs
    # Each job has operations that must be done in order on specific machines
    jobs = [
        [(0, 3), (1, 2), (2, 2)],  # Job 0: machine 0 for 3 units, then 1 for 2, then 2 for 2
        [(0, 2), (2, 1), (1, 4)],  # Job 1
        [(1, 4), (2, 3)],          # Job 2
        [(2, 2), (0, 1), (1, 3)],  # Job 3
        [(1, 3), (0, 2)]           # Job 4
    ]

    def schedule_makespan(schedule: List[Tuple[int, int]]) -> float:
        """Calculate makespan (total completion time) for a schedule."""
        # schedule is list of (job_id, operation_id) pairs

        # Track machine availability and job progress
        machine_time = [0, 0, 0]  # 3 machines
        job_time = [0] * 5  # 5 jobs

        for job_id, op_id in schedule:
            if op_id >= len(jobs[job_id]):
                continue  # Invalid operation

            machine, duration = jobs[job_id][op_id]

            # Operation starts when both machine and previous job operations are done
            start_time = max(machine_time[machine], job_time[job_id])
            end_time = start_time + duration

            machine_time[machine] = end_time
            job_time[job_id] = end_time

        return max(machine_time)  # Makespan is when last machine finishes

    def schedule_neighbor(schedule: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Generate neighbor by swapping two operations."""
        new_schedule = schedule.copy()

        # Find swappable operations (different jobs)
        attempts = 0
        while attempts < 10:
            i = random.randint(0, len(schedule) - 2)
            j = random.randint(i + 1, min(i + 5, len(schedule) - 1))

            # Check if swap is valid (different jobs)
            if new_schedule[i][0] != new_schedule[j][0]:
                new_schedule[i], new_schedule[j] = new_schedule[j], new_schedule[i]
                break
            attempts += 1

        return new_schedule

    # Create initial schedule (all operations in order)
    initial_schedule = []
    for job_id, job in enumerate(jobs):
        for op_id in range(len(job)):
            initial_schedule.append((job_id, op_id))
    random.shuffle(initial_schedule)

    # Create SA instance
    sa = SimulatedAnnealing(
        objective_function=schedule_makespan,
        initial_solution=initial_schedule,
        neighbor_function=schedule_neighbor,
        cooling_schedule=CoolingSchedule.EXPONENTIAL,
        initial_temp=50.0,
        final_temp=0.01,
        max_iterations=10000,
        cooling_rate=0.99
    )

    # Run optimization
    best = sa.run(verbose=True)

    print(f"\nBest makespan: {best.energy:.0f} time units")
    print(f"Schedule (first 10 operations): {best.state[:10]}")


def parallel_tempering_example():
    """Example: Parallel Tempering for difficult optimization."""
    print("\n" + "=" * 60)
    print("PARALLEL TEMPERING - DECEPTIVE FUNCTION")
    print("=" * 60)

    # Deceptive function with strong local minima
    def deceptive(x: np.ndarray) -> float:
        """Function with deceptive local minima."""
        # Global minimum at origin
        global_term = np.sum(x**2)

        # Add strong local minima
        local_minima = [
            (np.array([2, 2]), 0.8),
            (np.array([-2, -2]), 0.8),
            (np.array([2, -2]), 0.8),
            (np.array([-2, 2]), 0.8)
        ]

        min_local = float('inf')
        for center, depth in local_minima:
            if len(center) == len(x):
                dist = np.linalg.norm(x[:2] - center)
                local = depth * np.exp(-dist**2)
                min_local = min(min_local, -local)

        return global_term + min_local

    def neighbor_fn(x):
        """Neighbor function."""
        neighbor = x.copy()
        idx = random.randint(0, len(x) - 1)
        neighbor[idx] += np.random.normal(0, 0.3)
        return neighbor

    # Initial solution
    initial = np.random.uniform(-5, 5, 2)

    # Create Parallel Tempering instance
    pt = ParallelTempering(
        objective_function=deceptive,
        initial_solution=initial,
        n_replicas=6,
        temp_range=(0.1, 50),
        exchange_interval=100,
        neighbor_function=neighbor_fn,
        max_iterations=5000
    )

    # Run optimization
    best = pt.run(max_iterations=5000, verbose=True)

    print(f"\nBest solution: {best.state}")
    print(f"Function value: {best.energy:.6f}")
    print(f"Global minimum is ~0 at origin")
    print(f"Distance from optimal: {np.linalg.norm(best.state):.6f}")


def comparison_example():
    """Compare different cooling schedules."""
    print("\n" + "=" * 60)
    print("COOLING SCHEDULE COMPARISON")
    print("=" * 60)

    # Test function - Rosenbrock
    def rosenbrock(x: np.ndarray) -> float:
        """Rosenbrock function."""
        return sum(100 * (x[i+1] - x[i]**2)**2 + (1 - x[i])**2
                  for i in range(len(x) - 1))

    def neighbor(x):
        n = x.copy()
        idx = random.randint(0, len(x) - 1)
        n[idx] += np.random.normal(0, 0.1)
        return n

    initial = np.random.uniform(-2, 2, 5)
    schedules = [
        CoolingSchedule.LINEAR,
        CoolingSchedule.EXPONENTIAL,
        CoolingSchedule.LOGARITHMIC,
        CoolingSchedule.ADAPTIVE
    ]

    results = {}

    for schedule in schedules:
        print(f"\nTesting {schedule.value} cooling...")

        sa = SimulatedAnnealing(
            objective_function=rosenbrock,
            initial_solution=initial.copy(),
            neighbor_function=neighbor,
            cooling_schedule=schedule,
            initial_temp=10.0,
            final_temp=0.001,
            max_iterations=5000,
            cooling_rate=0.99
        )

        best = sa.run(verbose=False)
        results[schedule.value] = best.energy

        print(f"Final energy: {best.energy:.6f}")
        print(f"Acceptance rate: {100 * sa.accepted_moves / (sa.accepted_moves + sa.rejected_moves):.1f}%")

    print("\n" + "-" * 40)
    print("RESULTS SUMMARY:")
    for schedule, energy in sorted(results.items(), key=lambda x: x[1]):
        print(f"{schedule:15s}: {energy:.6f}")


if __name__ == "__main__":
    # Run examples
    optimize_function_example()
    traveling_salesman_example()
    scheduling_example()
    parallel_tempering_example()
    comparison_example()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- SA escapes local optima through probabilistic acceptance")
    print("- Temperature schedule critically affects performance")
    print("- Adaptive cooling can improve robustness")
    print("- Parallel tempering helps for deceptive landscapes")
    print("- Good neighbor functions are problem-specific")
    print("=" * 60)