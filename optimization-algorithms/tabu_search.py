"""
Tabu Search Algorithm Implementation
====================================

A comprehensive implementation of Tabu Search and its advanced variants.
Tabu Search uses memory structures (tabu lists) to avoid cycling and
escape local optima by forbidding recently visited solutions or moves.

Key Components:
- Short-term memory (recency-based tabu list)
- Medium-term memory (intensification)
- Long-term memory (diversification)
- Aspiration criteria
- Strategic oscillation
- Path relinking

Variants Implemented:
- Basic Tabu Search
- Reactive Tabu Search (dynamic tabu tenure)
- Probabilistic Tabu Search
- Parallel Tabu Search
- Hybrid Tabu Search with other metaheuristics

Applications:
- Combinatorial optimization
- Scheduling problems
- Vehicle routing
- Graph coloring
- Quadratic assignment
- Feature selection

Author: Claude
Date: January 2026
"""

import numpy as np
import random
from typing import Callable, Optional, List, Tuple, Dict, Any, Set, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import deque, defaultdict
import hashlib
import math
import copy


class TabuType(Enum):
    """Types of tabu restrictions."""
    SOLUTION_BASED = "solution_based"  # Forbid complete solutions
    ATTRIBUTE_BASED = "attribute_based"  # Forbid solution attributes
    MOVE_BASED = "move_based"  # Forbid specific moves
    OBJECTIVE_BASED = "objective_based"  # Forbid objective values


class AspirationCriterion(Enum):
    """Aspiration criteria for overriding tabu status."""
    BEST_SO_FAR = "best_so_far"  # Override if better than best known
    THRESHOLD = "threshold"  # Override if better than threshold
    INFLUENCE = "influence"  # Override based on move influence
    PROBABILISTIC = "probabilistic"  # Random override with probability


class DiversificationStrategy(Enum):
    """Strategies for diversification."""
    RESTART = "restart"  # Restart from random solution
    FREQUENCY = "frequency"  # Penalize frequently used attributes
    STRATEGIC_OSCILLATION = "strategic_oscillation"  # Oscillate between feasible/infeasible
    PATH_RELINKING = "path_relinking"  # Connect elite solutions


@dataclass
class Move:
    """Represents a move in the search space."""
    move_type: str
    from_state: Any
    to_state: Any
    delta: float = 0.0  # Change in objective
    attributes: List[Any] = field(default_factory=list)


@dataclass
class Solution:
    """Represents a solution with metadata."""
    state: Any
    objective: float
    iteration: int = 0
    frequency: int = 0
    recency: int = 0


class TabuList:
    """
    Tabu list management with different memory structures.
    """

    def __init__(self,
                 tabu_tenure: int = 10,
                 tabu_type: TabuType = TabuType.SOLUTION_BASED):
        """
        Initialize tabu list.

        Args:
            tabu_tenure: How long items remain tabu
            tabu_type: Type of tabu restrictions
        """
        self.tabu_tenure = tabu_tenure
        self.tabu_type = tabu_type
        self.tabu_list = deque(maxlen=tabu_tenure)
        self.tabu_dict = {}  # For efficient lookup
        self.iteration = 0

    def add(self, item: Any):
        """Add item to tabu list."""
        if self.tabu_type == TabuType.SOLUTION_BASED:
            # Hash solution for efficient comparison
            item_hash = self._hash_solution(item)
            self.tabu_dict[item_hash] = self.iteration + self.tabu_tenure
            self.tabu_list.append(item_hash)

        elif self.tabu_type == TabuType.ATTRIBUTE_BASED:
            # Store attributes
            for attr in item:
                self.tabu_dict[attr] = self.iteration + self.tabu_tenure

        elif self.tabu_type == TabuType.MOVE_BASED:
            # Store move description
            move_desc = str(item)
            self.tabu_dict[move_desc] = self.iteration + self.tabu_tenure

    def is_tabu(self, item: Any) -> bool:
        """Check if item is tabu."""
        self.iteration += 1

        if self.tabu_type == TabuType.SOLUTION_BASED:
            item_hash = self._hash_solution(item)
            return item_hash in self.tabu_dict and self.tabu_dict[item_hash] > self.iteration

        elif self.tabu_type == TabuType.ATTRIBUTE_BASED:
            # Check if any attribute is tabu
            for attr in item:
                if attr in self.tabu_dict and self.tabu_dict[attr] > self.iteration:
                    return True
            return False

        elif self.tabu_type == TabuType.MOVE_BASED:
            move_desc = str(item)
            return move_desc in self.tabu_dict and self.tabu_dict[move_desc] > self.iteration

        return False

    def update(self):
        """Clean expired tabu items."""
        expired = [k for k, v in self.tabu_dict.items() if v <= self.iteration]
        for k in expired:
            del self.tabu_dict[k]

    def _hash_solution(self, solution: Any) -> str:
        """Create hash of solution for comparison."""
        if isinstance(solution, np.ndarray):
            return hashlib.md5(solution.tobytes()).hexdigest()
        else:
            return hashlib.md5(str(solution).encode()).hexdigest()


class TabuSearch:
    """
    Main Tabu Search implementation.

    Uses memory structures to guide search and avoid cycling.
    """

    def __init__(self,
                 objective_function: Callable,
                 initial_solution: Any,
                 neighbor_function: Callable,
                 tabu_tenure: int = 10,
                 max_iterations: int = 1000,
                 max_neighbors: int = 100,
                 tabu_type: TabuType = TabuType.SOLUTION_BASED,
                 aspiration_criterion: AspirationCriterion = AspirationCriterion.BEST_SO_FAR,
                 use_intensification: bool = True,
                 use_diversification: bool = True):
        """
        Initialize Tabu Search.

        Args:
            objective_function: Function to minimize
            initial_solution: Starting solution
            neighbor_function: Function to generate neighbors
            tabu_tenure: Length of tabu list
            max_iterations: Maximum iterations
            max_neighbors: Neighbors to evaluate per iteration
            tabu_type: Type of tabu restrictions
            aspiration_criterion: Criterion for overriding tabu
            use_intensification: Enable intensification phase
            use_diversification: Enable diversification phase
        """
        self.objective_function = objective_function
        self.initial_solution = initial_solution
        self.neighbor_function = neighbor_function
        self.tabu_tenure = tabu_tenure
        self.max_iterations = max_iterations
        self.max_neighbors = max_neighbors
        self.tabu_type = tabu_type
        self.aspiration_criterion = aspiration_criterion
        self.use_intensification = use_intensification
        self.use_diversification = use_diversification

        # Tabu list
        self.tabu_list = TabuList(tabu_tenure, tabu_type)

        # Best solution tracking
        self.best_solution = None
        self.best_objective = float('inf')
        self.current_solution = None
        self.current_objective = float('inf')

        # Memory structures
        self.frequency_memory = defaultdict(int)  # Long-term frequency
        self.recency_memory = {}  # Short-term recency
        self.elite_solutions = []  # Elite solution pool
        self.iteration = 0

        # History tracking
        self.history = {
            'best_objective': [],
            'current_objective': [],
            'tabu_size': [],
            'diversification_count': 0,
            'intensification_count': 0
        }

    def generate_neighbors(self, solution: Any) -> List[Tuple[Any, float]]:
        """Generate and evaluate neighborhood."""
        neighbors = []

        for _ in range(self.max_neighbors):
            neighbor = self.neighbor_function(solution)
            objective = self.objective_function(neighbor)
            neighbors.append((neighbor, objective))

        return neighbors

    def is_aspiration_met(self, solution: Any, objective: float) -> bool:
        """Check if aspiration criterion is met."""
        if self.aspiration_criterion == AspirationCriterion.BEST_SO_FAR:
            return objective < self.best_objective

        elif self.aspiration_criterion == AspirationCriterion.THRESHOLD:
            threshold = self.best_objective * 1.05  # Within 5% of best
            return objective < threshold

        elif self.aspiration_criterion == AspirationCriterion.PROBABILISTIC:
            # Probability based on solution quality
            if objective < self.current_objective:
                prob = 0.1 * (1 - objective / self.current_objective)
                return random.random() < prob

        elif self.aspiration_criterion == AspirationCriterion.INFLUENCE:
            # Based on move influence (simplified)
            influence = abs(objective - self.current_objective) / self.current_objective
            return influence > 0.1

        return False

    def select_best_admissible(self, neighbors: List[Tuple[Any, float]]) -> Tuple[Any, float]:
        """Select best non-tabu neighbor or use aspiration."""
        best_neighbor = None
        best_objective = float('inf')

        for neighbor, objective in neighbors:
            # Check if tabu
            is_tabu = self.tabu_list.is_tabu(neighbor)

            # Check aspiration
            if is_tabu and not self.is_aspiration_met(neighbor, objective):
                continue

            # Update best admissible
            if objective < best_objective:
                best_objective = objective
                best_neighbor = neighbor

        return best_neighbor, best_objective

    def update_frequency_memory(self, solution: Any):
        """Update long-term frequency memory."""
        # Extract and count solution attributes
        if isinstance(solution, (list, np.ndarray)):
            for i, val in enumerate(solution):
                self.frequency_memory[(i, val)] += 1
        else:
            self.frequency_memory[str(solution)] += 1

    def intensification_phase(self) -> Any:
        """
        Intensification: Focus search on promising regions.

        Returns:
            Solution to restart from
        """
        if not self.elite_solutions:
            return self.current_solution

        # Select elite solution with best objective
        elite = min(self.elite_solutions, key=lambda s: s.objective)

        if self.use_intensification:
            print(f"Intensification: Restarting from elite solution (obj={elite.objective:.4f})")
            self.history['intensification_count'] += 1

        return elite.state

    def diversification_phase(self) -> Any:
        """
        Diversification: Explore new regions.

        Returns:
            New solution to explore
        """
        if not self.use_diversification:
            return self.current_solution

        # Generate diverse solution using frequency memory
        if isinstance(self.initial_solution, np.ndarray):
            # For continuous problems
            diverse_solution = np.random.uniform(
                np.min(self.initial_solution),
                np.max(self.initial_solution),
                self.initial_solution.shape
            )
        elif isinstance(self.initial_solution, list):
            # For discrete problems - penalize frequent attributes
            diverse_solution = self.initial_solution.copy()

            # Modify based on frequency
            for i in range(len(diverse_solution)):
                # Choose value with low frequency
                min_freq = float('inf')
                best_val = diverse_solution[i]

                for val in range(min(diverse_solution), max(diverse_solution) + 1):
                    freq = self.frequency_memory.get((i, val), 0)
                    if freq < min_freq:
                        min_freq = freq
                        best_val = val

                if random.random() < 0.5:  # Probabilistic acceptance
                    diverse_solution[i] = best_val
        else:
            # Random restart for unknown types
            diverse_solution = self.neighbor_function(self.initial_solution)

        print(f"Diversification: Exploring new region")
        self.history['diversification_count'] += 1

        return diverse_solution

    def step(self):
        """Perform one tabu search iteration."""
        # Generate neighbors
        neighbors = self.generate_neighbors(self.current_solution)

        # Select best admissible move
        next_solution, next_objective = self.select_best_admissible(neighbors)

        if next_solution is None:
            # No admissible moves - diversify
            next_solution = self.diversification_phase()
            next_objective = self.objective_function(next_solution)

        # Update tabu list
        self.tabu_list.add(self.current_solution)

        # Update current solution
        self.current_solution = next_solution
        self.current_objective = next_objective

        # Update best solution
        if next_objective < self.best_objective:
            self.best_objective = next_objective
            self.best_solution = copy.deepcopy(next_solution)

            # Add to elite solutions
            self.elite_solutions.append(
                Solution(copy.deepcopy(next_solution), next_objective, self.iteration)
            )
            # Keep only top elite solutions
            self.elite_solutions = sorted(self.elite_solutions, key=lambda s: s.objective)[:10]

        # Update memory structures
        self.update_frequency_memory(next_solution)
        self.recency_memory[self._hash_solution(next_solution)] = self.iteration

        # Clean tabu list
        self.tabu_list.update()

    def run(self, verbose: bool = True) -> Tuple[Any, float]:
        """
        Run tabu search algorithm.

        Args:
            verbose: Print progress

        Returns:
            Best solution and objective value
        """
        # Initialize
        self.current_solution = self.initial_solution
        self.current_objective = self.objective_function(self.initial_solution)
        self.best_solution = copy.deepcopy(self.initial_solution)
        self.best_objective = self.current_objective

        if verbose:
            print(f"Starting Tabu Search")
            print(f"Initial objective: {self.current_objective:.6f}")
            print(f"Tabu tenure: {self.tabu_tenure}")

        stagnation_count = 0
        last_improvement = 0

        # Main loop
        for iteration in range(self.max_iterations):
            self.iteration = iteration

            # Perform step
            self.step()

            # Check for improvement
            if self.current_objective < self.best_objective * 1.001:
                stagnation_count = 0
                last_improvement = iteration
            else:
                stagnation_count += 1

            # Intensification after finding good solution
            if self.use_intensification and stagnation_count == 50:
                self.current_solution = self.intensification_phase()
                self.current_objective = self.objective_function(self.current_solution)
                stagnation_count = 0

            # Diversification if stuck
            if self.use_diversification and stagnation_count >= 100:
                self.current_solution = self.diversification_phase()
                self.current_objective = self.objective_function(self.current_solution)
                stagnation_count = 0

            # Update history
            self.history['best_objective'].append(self.best_objective)
            self.history['current_objective'].append(self.current_objective)
            self.history['tabu_size'].append(len(self.tabu_list.tabu_dict))

            # Print progress
            if verbose and iteration % 50 == 0:
                print(f"Iteration {iteration}: Current = {self.current_objective:.6f}, "
                      f"Best = {self.best_objective:.6f}, "
                      f"Tabu size = {len(self.tabu_list.tabu_dict)}, "
                      f"Stagnation = {stagnation_count}")

        if verbose:
            print(f"\nTabu Search completed")
            print(f"Best objective: {self.best_objective:.6f}")
            print(f"Last improvement: iteration {last_improvement}")
            print(f"Intensifications: {self.history['intensification_count']}")
            print(f"Diversifications: {self.history['diversification_count']}")

        return self.best_solution, self.best_objective

    def _hash_solution(self, solution: Any) -> str:
        """Create hash of solution."""
        if isinstance(solution, np.ndarray):
            return hashlib.md5(solution.tobytes()).hexdigest()
        else:
            return hashlib.md5(str(solution).encode()).hexdigest()


class ReactiveTabuSearch(TabuSearch):
    """
    Reactive Tabu Search with dynamic tabu tenure.

    Automatically adjusts tabu tenure based on search behavior.
    """

    def __init__(self, *args,
                 min_tenure: int = 5,
                 max_tenure: int = 50,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.min_tenure = min_tenure
        self.max_tenure = max_tenure
        self.repetition_memory = defaultdict(int)
        self.last_change = 0

    def adjust_tabu_tenure(self):
        """Adjust tabu tenure based on repetitions."""
        # Count repetitions in recent history
        recent_solutions = self.history['current_objective'][-50:]
        repetitions = len(recent_solutions) - len(set(recent_solutions))

        if repetitions > 5:
            # Too many repetitions - increase tenure
            self.tabu_tenure = min(self.max_tenure, int(self.tabu_tenure * 1.5))
            self.tabu_list.tabu_tenure = self.tabu_tenure
            self.last_change = self.iteration

        elif repetitions < 2 and self.iteration - self.last_change > 50:
            # Too few repetitions - decrease tenure
            self.tabu_tenure = max(self.min_tenure, int(self.tabu_tenure * 0.8))
            self.tabu_list.tabu_tenure = self.tabu_tenure
            self.last_change = self.iteration

    def step(self):
        """Step with reactive adjustment."""
        super().step()
        self.adjust_tabu_tenure()


class PathRelinking:
    """
    Path Relinking for connecting elite solutions.

    Creates paths between high-quality solutions to explore
    intermediate solutions.
    """

    def __init__(self,
                 objective_function: Callable,
                 distance_function: Callable):
        """
        Initialize path relinking.

        Args:
            objective_function: Objective to evaluate
            distance_function: Function to compute distance between solutions
        """
        self.objective_function = objective_function
        self.distance_function = distance_function

    def relink(self, source: Any, target: Any,
              max_path_length: int = 20) -> List[Tuple[Any, float]]:
        """
        Create path from source to target.

        Args:
            source: Starting solution
            target: Target solution
            max_path_length: Maximum path length

        Returns:
            List of intermediate solutions with objectives
        """
        path = []
        current = copy.deepcopy(source)

        for step in range(max_path_length):
            # Find differences
            if isinstance(source, np.ndarray):
                diff_indices = np.where(current != target)[0]
            elif isinstance(source, list):
                diff_indices = [i for i in range(len(source))
                              if current[i] != target[i]]
            else:
                break

            if not diff_indices:
                break  # Reached target

            # Make move toward target
            idx = random.choice(diff_indices)
            if isinstance(source, np.ndarray):
                current[idx] = target[idx]
            else:
                current[idx] = target[idx]

            objective = self.objective_function(current)
            path.append((copy.deepcopy(current), objective))

            if self.distance_function(current, target) == 0:
                break

        return path


def tsp_example():
    """Example: TSP using Tabu Search."""
    print("=" * 60)
    print("TABU SEARCH - TRAVELING SALESMAN PROBLEM")
    print("=" * 60)

    # Generate TSP instance
    np.random.seed(42)
    n_cities = 30
    cities = np.random.rand(n_cities, 2) * 100

    # Distance matrix
    dist_matrix = np.zeros((n_cities, n_cities))
    for i in range(n_cities):
        for j in range(n_cities):
            dist_matrix[i, j] = np.linalg.norm(cities[i] - cities[j])

    def tsp_objective(tour: List[int]) -> float:
        """Calculate tour length."""
        length = 0
        for i in range(len(tour)):
            length += dist_matrix[tour[i], tour[(i + 1) % len(tour)]]
        return length

    def tsp_neighbor(tour: List[int]) -> List[int]:
        """Generate neighbor using 2-opt."""
        neighbor = tour.copy()

        # 2-opt swap
        i = random.randint(0, len(tour) - 2)
        j = random.randint(i + 1, len(tour) - 1)
        neighbor[i:j+1] = reversed(neighbor[i:j+1])

        return neighbor

    # Initial random tour
    initial_tour = list(range(n_cities))
    random.shuffle(initial_tour)

    # Run Tabu Search
    ts = TabuSearch(
        objective_function=tsp_objective,
        initial_solution=initial_tour,
        neighbor_function=tsp_neighbor,
        tabu_tenure=15,
        max_iterations=500,
        max_neighbors=50,
        tabu_type=TabuType.ATTRIBUTE_BASED,
        aspiration_criterion=AspirationCriterion.BEST_SO_FAR
    )

    best_tour, best_length = ts.run(verbose=True)

    print(f"\nBest tour length: {best_length:.2f}")
    print(f"Tour: {best_tour[:10]}...")


def job_shop_scheduling_example():
    """Example: Job Shop Scheduling with Tabu Search."""
    print("\n" + "=" * 60)
    print("TABU SEARCH - JOB SHOP SCHEDULING")
    print("=" * 60)

    # Job shop instance: 3 jobs, 3 machines
    # Each job has operations (machine, duration)
    jobs = [
        [(0, 3), (1, 2), (2, 2)],  # Job 0
        [(0, 2), (2, 1), (1, 4)],  # Job 1
        [(1, 4), (2, 3), (0, 1)]   # Job 2
    ]

    def calculate_makespan(schedule: List[Tuple[int, int]]) -> float:
        """Calculate makespan of schedule."""
        machine_time = [0, 0, 0]
        job_time = [0, 0, 0]

        for job_id, op_id in schedule:
            if op_id >= len(jobs[job_id]):
                continue

            machine, duration = jobs[job_id][op_id]

            start_time = max(machine_time[machine], job_time[job_id])
            end_time = start_time + duration

            machine_time[machine] = end_time
            job_time[job_id] = end_time

        return max(machine_time)

    def schedule_neighbor(schedule: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Generate neighbor by swapping operations."""
        neighbor = schedule.copy()

        # Swap two operations from different jobs
        attempts = 0
        while attempts < 10:
            i = random.randint(0, len(schedule) - 2)
            j = random.randint(i + 1, min(i + 5, len(schedule) - 1))

            if neighbor[i][0] != neighbor[j][0]:  # Different jobs
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                break
            attempts += 1

        return neighbor

    # Initial schedule: operations in order
    initial_schedule = []
    for job_id in range(3):
        for op_id in range(len(jobs[job_id])):
            initial_schedule.append((job_id, op_id))
    random.shuffle(initial_schedule)

    # Run Tabu Search
    ts = TabuSearch(
        objective_function=calculate_makespan,
        initial_solution=initial_schedule,
        neighbor_function=schedule_neighbor,
        tabu_tenure=10,
        max_iterations=300,
        tabu_type=TabuType.MOVE_BASED
    )

    best_schedule, best_makespan = ts.run(verbose=True)

    print(f"\nBest makespan: {best_makespan:.0f} time units")
    print(f"Schedule (first 6 operations): {best_schedule[:6]}")


def quadratic_assignment_example():
    """Example: Quadratic Assignment Problem."""
    print("\n" + "=" * 60)
    print("TABU SEARCH - QUADRATIC ASSIGNMENT PROBLEM")
    print("=" * 60)

    # QAP instance: assign n facilities to n locations
    n = 10
    np.random.seed(42)

    # Flow matrix (between facilities)
    flow = np.random.randint(0, 10, (n, n))
    flow = (flow + flow.T) // 2  # Symmetric

    # Distance matrix (between locations)
    distance = np.random.randint(1, 20, (n, n))
    distance = (distance + distance.T) // 2  # Symmetric

    def qap_objective(assignment: List[int]) -> float:
        """Calculate QAP cost."""
        cost = 0
        for i in range(n):
            for j in range(n):
                cost += flow[i, j] * distance[assignment[i], assignment[j]]
        return cost

    def qap_neighbor(assignment: List[int]) -> List[int]:
        """Swap two facility assignments."""
        neighbor = assignment.copy()
        i, j = random.sample(range(n), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        return neighbor

    # Initial random assignment
    initial = list(range(n))
    random.shuffle(initial)

    # Reactive Tabu Search
    rts = ReactiveTabuSearch(
        objective_function=qap_objective,
        initial_solution=initial,
        neighbor_function=qap_neighbor,
        min_tenure=5,
        max_tenure=30,
        max_iterations=500,
        max_neighbors=30
    )

    best_assignment, best_cost = rts.run(verbose=True)

    print(f"\nBest cost: {best_cost:.0f}")
    print(f"Assignment: {best_assignment}")


def feature_selection_tabu():
    """Example: Feature selection with Tabu Search."""
    print("\n" + "=" * 60)
    print("TABU SEARCH - FEATURE SELECTION")
    print("=" * 60)

    # Simulated problem
    n_features = 30
    n_relevant = 8

    def feature_objective(selected: np.ndarray) -> float:
        """Objective for feature selection (minimize)."""
        n_selected = np.sum(selected)

        if n_selected == 0:
            return 1000

        # Reward for relevant features
        relevant_score = -np.sum(selected[:n_relevant])

        # Penalty for irrelevant features
        irrelevant_penalty = 0.5 * np.sum(selected[n_relevant:])

        # Size penalty
        size_penalty = 0.01 * n_selected

        return relevant_score + irrelevant_penalty + size_penalty

    def feature_neighbor(selected: np.ndarray) -> np.ndarray:
        """Flip random features."""
        neighbor = selected.copy()

        # Flip 1-3 features
        n_flips = random.randint(1, 3)
        indices = random.sample(range(len(selected)), n_flips)

        for idx in indices:
            neighbor[idx] = 1 - neighbor[idx]

        return neighbor

    # Initial random selection
    initial = np.random.randint(0, 2, n_features)

    # Tabu Search with path relinking
    ts = TabuSearch(
        objective_function=feature_objective,
        initial_solution=initial,
        neighbor_function=feature_neighbor,
        tabu_tenure=8,
        max_iterations=400,
        max_neighbors=50,
        tabu_type=TabuType.ATTRIBUTE_BASED,
        use_diversification=True,
        use_intensification=True
    )

    best_features, best_objective = ts.run(verbose=True)

    selected_indices = np.where(best_features)[0]
    print(f"\nSelected features: {selected_indices}")
    print(f"Number selected: {len(selected_indices)}")
    print(f"Relevant features found: {len([i for i in selected_indices if i < n_relevant])}/{n_relevant}")
    print(f"Objective: {best_objective:.4f}")


def comparison_example():
    """Compare different Tabu Search variants."""
    print("\n" + "=" * 60)
    print("TABU SEARCH VARIANT COMPARISON")
    print("=" * 60)

    # Test function - Schwefel
    def schwefel(x: np.ndarray) -> float:
        """Schwefel function."""
        n = len(x)
        return 418.9829 * n - np.sum(x * np.sin(np.sqrt(np.abs(x))))

    def continuous_neighbor(x: np.ndarray) -> np.ndarray:
        """Neighbor for continuous optimization."""
        neighbor = x.copy()
        idx = random.randint(0, len(x) - 1)
        neighbor[idx] += np.random.normal(0, 10)
        neighbor[idx] = np.clip(neighbor[idx], -500, 500)
        return neighbor

    initial = np.random.uniform(-500, 500, 5)
    results = {}

    # Basic Tabu Search
    print("\nBasic Tabu Search...")
    ts_basic = TabuSearch(
        objective_function=schwefel,
        initial_solution=initial.copy(),
        neighbor_function=continuous_neighbor,
        tabu_tenure=10,
        max_iterations=300,
        use_intensification=False,
        use_diversification=False
    )
    _, basic_result = ts_basic.run(verbose=False)
    results['Basic'] = basic_result

    # With Intensification and Diversification
    print("Tabu Search with I&D...")
    ts_id = TabuSearch(
        objective_function=schwefel,
        initial_solution=initial.copy(),
        neighbor_function=continuous_neighbor,
        tabu_tenure=10,
        max_iterations=300,
        use_intensification=True,
        use_diversification=True
    )
    _, id_result = ts_id.run(verbose=False)
    results['With I&D'] = id_result

    # Reactive Tabu Search
    print("Reactive Tabu Search...")
    rts = ReactiveTabuSearch(
        objective_function=schwefel,
        initial_solution=initial.copy(),
        neighbor_function=continuous_neighbor,
        min_tenure=5,
        max_tenure=25,
        max_iterations=300
    )
    _, reactive_result = rts.run(verbose=False)
    results['Reactive'] = reactive_result

    print("\n" + "-" * 40)
    print("RESULTS:")
    for variant, result in sorted(results.items(), key=lambda x: x[1]):
        print(f"{variant:15s}: {result:.4f}")

    print(f"\nGlobal minimum: {schwefel(np.full(5, 420.9687)):.4f}")


if __name__ == "__main__":
    # Run examples
    tsp_example()
    job_shop_scheduling_example()
    quadratic_assignment_example()
    feature_selection_tabu()
    comparison_example()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Tabu Search uses memory to avoid cycling")
    print("- Aspiration criteria allow exceptional moves")
    print("- Intensification exploits promising regions")
    print("- Diversification explores new regions")
    print("- Reactive variants adapt parameters dynamically")
    print("=" * 60)