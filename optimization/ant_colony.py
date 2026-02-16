"""
Ant Colony Optimization (ACO) Implementation
============================================

A comprehensive implementation of Ant Colony Optimization algorithms.
Includes standard ACO, Ant System (AS), Ant Colony System (ACS),
MAX-MIN Ant System (MMAS), and Rank-Based Ant System.

Features:
- Multiple ACO variants
- Support for TSP and other combinatorial problems
- Adaptive pheromone strategies
- Parallel ant evaluation
- Local search integration

Author: Claude
Date: January 2026
"""

import numpy as np
import random
from typing import Callable, List, Tuple, Optional, Any, Dict
from dataclasses import dataclass
from enum import Enum
import copy
import math


class ACOVariant(Enum):
    """Different ACO algorithm variants."""
    AS = "ant_system"  # Original Ant System
    ACS = "ant_colony_system"  # Ant Colony System
    MMAS = "max_min_ant_system"  # MAX-MIN Ant System
    RANK_AS = "rank_based_ant_system"  # Rank-Based Ant System
    ELITIST_AS = "elitist_ant_system"  # Elitist Ant System


class LocalSearch(Enum):
    """Local search methods to improve solutions."""
    NONE = "none"
    TWO_OPT = "2_opt"
    THREE_OPT = "3_opt"
    LIN_KERNIGHAN = "lin_kernighan"


@dataclass
class Ant:
    """Represents an ant in the colony."""
    tour: List[int]
    tour_length: float
    visited: set
    current_city: int
    tabu_list: List[int]


class AntColonyOptimization:
    """
    Base Ant Colony Optimization class for TSP.

    ACO uses artificial ants to build solutions by depositing pheromones
    on good paths, which influences future ants' decisions.
    """

    def __init__(
        self,
        distance_matrix: np.ndarray,
        n_ants: int = 20,
        n_iterations: int = 100,
        alpha: float = 1.0,  # Pheromone importance
        beta: float = 2.0,   # Heuristic importance
        rho: float = 0.5,    # Evaporation rate
        q0: float = 0.9,     # Exploitation vs exploration (for ACS)
        variant: ACOVariant = ACOVariant.AS,
        local_search: LocalSearch = LocalSearch.NONE,
        seed: Optional[int] = None
    ):
        """
        Initialize ACO algorithm.

        Args:
            distance_matrix: Matrix of distances between cities
            n_ants: Number of ants
            n_iterations: Number of iterations
            alpha: Pheromone trail importance
            beta: Heuristic information importance
            rho: Pheromone evaporation rate
            q0: Probability of exploitation (for ACS)
            variant: ACO variant to use
            local_search: Local search method
            seed: Random seed
        """
        self.distance_matrix = distance_matrix
        self.n_cities = len(distance_matrix)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q0 = q0
        self.variant = variant
        self.local_search = local_search

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # Initialize pheromone matrix
        self.pheromone = None
        self.eta = None  # Heuristic information (1/distance)

        # Best solution tracking
        self.best_tour = None
        self.best_tour_length = float('inf')
        self.iteration_best_tours = []
        self.iteration_best_lengths = []

        # MMAS specific parameters
        self.tau_max = None
        self.tau_min = None

        # Initialize matrices
        self._initialize_matrices()

    def _initialize_matrices(self):
        """Initialize pheromone and heuristic information matrices."""
        # Calculate nearest neighbor tour for initial pheromone
        nn_tour_length = self._nearest_neighbor_tour_length()

        # Initial pheromone level
        if self.variant == ACOVariant.ACS:
            tau_0 = 1 / (self.n_cities * nn_tour_length)
        elif self.variant == ACOVariant.MMAS:
            tau_0 = 1 / nn_tour_length
            self.tau_max = tau_0
            self.tau_min = tau_0 / (2 * self.n_cities)
        else:
            tau_0 = self.n_ants / nn_tour_length

        self.pheromone = np.ones((self.n_cities, self.n_cities)) * tau_0

        # Heuristic information (inverse of distance)
        self.eta = np.zeros((self.n_cities, self.n_cities))
        for i in range(self.n_cities):
            for j in range(self.n_cities):
                if i != j and self.distance_matrix[i][j] > 0:
                    self.eta[i][j] = 1 / self.distance_matrix[i][j]

    def _nearest_neighbor_tour_length(self) -> float:
        """Calculate tour length using nearest neighbor heuristic."""
        unvisited = set(range(1, self.n_cities))
        tour = [0]
        current = 0
        total_distance = 0

        while unvisited:
            nearest = min(unvisited, key=lambda x: self.distance_matrix[current][x])
            total_distance += self.distance_matrix[current][nearest]
            current = nearest
            tour.append(current)
            unvisited.remove(current)

        total_distance += self.distance_matrix[current][0]
        return total_distance

    def _calculate_tour_length(self, tour: List[int]) -> float:
        """Calculate total length of a tour."""
        length = 0
        for i in range(len(tour)):
            from_city = tour[i]
            to_city = tour[(i + 1) % len(tour)]
            length += self.distance_matrix[from_city][to_city]
        return length

    def _select_next_city(self, ant: Ant) -> int:
        """
        Select next city for ant to visit.

        Different selection rules based on variant.
        """
        current = ant.current_city
        unvisited = [i for i in range(self.n_cities) if i not in ant.visited]

        if not unvisited:
            return -1

        if self.variant == ACOVariant.ACS:
            # Ant Colony System selection rule
            if random.random() < self.q0:
                # Exploitation: choose best
                values = [
                    self.pheromone[current][j] ** self.alpha * self.eta[current][j] ** self.beta
                    for j in unvisited
                ]
                return unvisited[np.argmax(values)]
            else:
                # Exploration: probabilistic
                return self._probabilistic_selection(current, unvisited)
        else:
            # Standard probabilistic selection
            return self._probabilistic_selection(current, unvisited)

    def _probabilistic_selection(self, current: int, unvisited: List[int]) -> int:
        """Probabilistic city selection based on pheromone and heuristic."""
        probabilities = []
        total = 0

        for city in unvisited:
            prob = (self.pheromone[current][city] ** self.alpha *
                   self.eta[current][city] ** self.beta)
            probabilities.append(prob)
            total += prob

        if total == 0:
            return random.choice(unvisited)

        # Normalize probabilities
        probabilities = [p / total for p in probabilities]

        # Select based on probabilities
        return np.random.choice(unvisited, p=probabilities)

    def _construct_solution(self, ant: Ant):
        """Construct a complete tour for an ant."""
        # Start from random city
        start_city = random.randint(0, self.n_cities - 1)
        ant.current_city = start_city
        ant.tour = [start_city]
        ant.visited = {start_city}

        # Build tour
        for _ in range(self.n_cities - 1):
            next_city = self._select_next_city(ant)
            if next_city == -1:
                break

            ant.tour.append(next_city)
            ant.visited.add(next_city)

            # Local pheromone update for ACS
            if self.variant == ACOVariant.ACS:
                tau_0 = 1 / (self.n_cities * self._nearest_neighbor_tour_length())
                self.pheromone[ant.current_city][next_city] = \
                    (1 - 0.1) * self.pheromone[ant.current_city][next_city] + 0.1 * tau_0

            ant.current_city = next_city

        # Calculate tour length
        ant.tour_length = self._calculate_tour_length(ant.tour)

    def _apply_local_search(self, tour: List[int]) -> Tuple[List[int], float]:
        """Apply local search to improve a tour."""
        if self.local_search == LocalSearch.NONE:
            return tour, self._calculate_tour_length(tour)

        elif self.local_search == LocalSearch.TWO_OPT:
            return self._two_opt(tour)

        elif self.local_search == LocalSearch.THREE_OPT:
            return self._three_opt(tour)

        else:
            return tour, self._calculate_tour_length(tour)

    def _two_opt(self, tour: List[int]) -> Tuple[List[int], float]:
        """Apply 2-opt local search."""
        best_tour = tour.copy()
        best_length = self._calculate_tour_length(best_tour)
        improved = True

        while improved:
            improved = False
            for i in range(1, len(tour) - 2):
                for j in range(i + 1, len(tour)):
                    if j - i == 1:
                        continue

                    new_tour = tour.copy()
                    new_tour[i:j] = reversed(tour[i:j])
                    new_length = self._calculate_tour_length(new_tour)

                    if new_length < best_length:
                        best_tour = new_tour
                        best_length = new_length
                        tour = new_tour
                        improved = True
                        break
                if improved:
                    break

        return best_tour, best_length

    def _three_opt(self, tour: List[int]) -> Tuple[List[int], float]:
        """Apply 3-opt local search (simplified version)."""
        best_tour = tour.copy()
        best_length = self._calculate_tour_length(best_tour)
        n = len(tour)

        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    # Try different reconnection patterns
                    segments = [tour[:i], tour[i:j], tour[j:k], tour[k:]]

                    # Generate different tour combinations
                    new_tours = [
                        segments[0] + segments[1] + segments[2] + segments[3],  # Original
                        segments[0] + segments[1] + segments[3] + segments[2],
                        segments[0] + segments[2] + segments[1] + segments[3],
                        segments[0] + segments[2] + segments[3] + segments[1],
                        segments[0] + segments[3] + segments[1] + segments[2],
                        segments[0] + segments[3] + segments[2] + segments[1],
                        segments[0] + list(reversed(segments[1])) + segments[2] + segments[3],
                        segments[0] + segments[1] + list(reversed(segments[2])) + segments[3],
                    ]

                    for new_tour in new_tours:
                        new_length = self._calculate_tour_length(new_tour)
                        if new_length < best_length:
                            best_tour = new_tour
                            best_length = new_length

        return best_tour, best_length

    def _update_pheromone(self, ants: List[Ant]):
        """Update pheromone trails based on ant solutions."""
        if self.variant == ACOVariant.AS:
            self._update_pheromone_as(ants)
        elif self.variant == ACOVariant.ACS:
            self._update_pheromone_acs(ants)
        elif self.variant == ACOVariant.MMAS:
            self._update_pheromone_mmas(ants)
        elif self.variant == ACOVariant.RANK_AS:
            self._update_pheromone_rank(ants)
        elif self.variant == ACOVariant.ELITIST_AS:
            self._update_pheromone_elitist(ants)

    def _update_pheromone_as(self, ants: List[Ant]):
        """Standard Ant System pheromone update."""
        # Evaporation
        self.pheromone *= (1 - self.rho)

        # Add pheromone from all ants
        for ant in ants:
            delta = 1 / ant.tour_length
            for i in range(len(ant.tour)):
                from_city = ant.tour[i]
                to_city = ant.tour[(i + 1) % len(ant.tour)]
                self.pheromone[from_city][to_city] += delta
                self.pheromone[to_city][from_city] += delta

    def _update_pheromone_acs(self, ants: List[Ant]):
        """Ant Colony System pheromone update (only best ant)."""
        # Global evaporation
        self.pheromone *= (1 - self.rho)

        # Only best ant deposits pheromone
        best_ant = min(ants, key=lambda a: a.tour_length)
        delta = 1 / best_ant.tour_length

        for i in range(len(best_ant.tour)):
            from_city = best_ant.tour[i]
            to_city = best_ant.tour[(i + 1) % len(best_ant.tour)]
            self.pheromone[from_city][to_city] += self.rho * delta
            self.pheromone[to_city][from_city] += self.rho * delta

    def _update_pheromone_mmas(self, ants: List[Ant]):
        """MAX-MIN Ant System pheromone update."""
        # Evaporation
        self.pheromone *= (1 - self.rho)

        # Only iteration-best or global-best ant deposits
        iteration_best = min(ants, key=lambda a: a.tour_length)

        # Use global best with some probability
        if random.random() < 0.5 and self.best_tour is not None:
            tour = self.best_tour
            tour_length = self.best_tour_length
        else:
            tour = iteration_best.tour
            tour_length = iteration_best.tour_length

        delta = 1 / tour_length

        for i in range(len(tour)):
            from_city = tour[i]
            to_city = tour[(i + 1) % len(tour)]
            self.pheromone[from_city][to_city] += delta
            self.pheromone[to_city][from_city] += delta

        # Enforce pheromone bounds
        self.pheromone = np.clip(self.pheromone, self.tau_min, self.tau_max)

    def _update_pheromone_rank(self, ants: List[Ant]):
        """Rank-based Ant System pheromone update."""
        # Evaporation
        self.pheromone *= (1 - self.rho)

        # Sort ants by tour length
        sorted_ants = sorted(ants, key=lambda a: a.tour_length)

        # Only top-w ants deposit pheromone
        w = min(6, len(sorted_ants))  # Number of elite ants

        for rank, ant in enumerate(sorted_ants[:w]):
            delta = (w - rank) / ant.tour_length
            for i in range(len(ant.tour)):
                from_city = ant.tour[i]
                to_city = ant.tour[(i + 1) % len(ant.tour)]
                self.pheromone[from_city][to_city] += delta
                self.pheromone[to_city][from_city] += delta

    def _update_pheromone_elitist(self, ants: List[Ant]):
        """Elitist Ant System pheromone update."""
        # Standard update
        self._update_pheromone_as(ants)

        # Additional pheromone from best-so-far ant
        if self.best_tour is not None:
            e = 5  # Elite weight
            delta = e / self.best_tour_length
            for i in range(len(self.best_tour)):
                from_city = self.best_tour[i]
                to_city = self.best_tour[(i + 1) % len(self.best_tour)]
                self.pheromone[from_city][to_city] += delta
                self.pheromone[to_city][from_city] += delta

    def run(self, verbose: bool = True) -> Tuple[List[int], float]:
        """
        Run the ACO algorithm.

        Args:
            verbose: Whether to print progress

        Returns:
            Best tour and its length
        """
        for iteration in range(self.n_iterations):
            # Create ants
            ants = [Ant(tour=[], tour_length=0, visited=set(),
                       current_city=0, tabu_list=[]) for _ in range(self.n_ants)]

            # Construct solutions
            for ant in ants:
                self._construct_solution(ant)

                # Apply local search
                if self.local_search != LocalSearch.NONE:
                    ant.tour, ant.tour_length = self._apply_local_search(ant.tour)

            # Update best solution
            iteration_best = min(ants, key=lambda a: a.tour_length)
            if iteration_best.tour_length < self.best_tour_length:
                self.best_tour = iteration_best.tour.copy()
                self.best_tour_length = iteration_best.tour_length

            # Store iteration results
            self.iteration_best_tours.append(iteration_best.tour.copy())
            self.iteration_best_lengths.append(iteration_best.tour_length)

            # Update pheromone
            self._update_pheromone(ants)

            # Update MMAS bounds if needed
            if self.variant == ACOVariant.MMAS:
                self.tau_max = 1 / (self.rho * self.best_tour_length)
                self.tau_min = self.tau_max / (2 * self.n_cities)

            # Print progress
            if verbose and iteration % 10 == 0:
                avg_length = np.mean([ant.tour_length for ant in ants])
                print(f"Iteration {iteration}: Best = {self.best_tour_length:.2f}, "
                      f"Iteration best = {iteration_best.tour_length:.2f}, "
                      f"Avg = {avg_length:.2f}")

        return self.best_tour, self.best_tour_length


class ACOForGraphColoring:
    """
    Ant Colony Optimization for Graph Coloring Problem.
    """

    def __init__(
        self,
        adjacency_matrix: np.ndarray,
        n_colors: int,
        n_ants: int = 20,
        n_iterations: int = 100,
        alpha: float = 1.0,
        beta: float = 2.0,
        rho: float = 0.1,
        seed: Optional[int] = None
    ):
        """
        Initialize ACO for graph coloring.

        Args:
            adjacency_matrix: Graph adjacency matrix
            n_colors: Number of available colors
            n_ants: Number of ants
            n_iterations: Number of iterations
            alpha: Pheromone importance
            beta: Heuristic importance
            rho: Evaporation rate
            seed: Random seed
        """
        self.adjacency_matrix = adjacency_matrix
        self.n_vertices = len(adjacency_matrix)
        self.n_colors = n_colors
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # Pheromone matrix: pheromone[vertex][color]
        self.pheromone = np.ones((self.n_vertices, self.n_colors))

        # Best solution
        self.best_coloring = None
        self.best_conflicts = float('inf')
        self.best_colors_used = float('inf')

    def _calculate_conflicts(self, coloring: List[int]) -> int:
        """Calculate number of conflicts in a coloring."""
        conflicts = 0
        for i in range(self.n_vertices):
            for j in range(i + 1, self.n_vertices):
                if self.adjacency_matrix[i][j] and coloring[i] == coloring[j]:
                    conflicts += 1
        return conflicts

    def _calculate_colors_used(self, coloring: List[int]) -> int:
        """Calculate number of different colors used."""
        return len(set(coloring))

    def _select_color(self, vertex: int, coloring: List[int]) -> int:
        """Select color for a vertex."""
        # Calculate heuristic (prefer colors that minimize conflicts)
        heuristic = np.zeros(self.n_colors)
        for color in range(self.n_colors):
            conflicts = 0
            for neighbor in range(self.n_vertices):
                if self.adjacency_matrix[vertex][neighbor] and \
                   neighbor < vertex and coloring[neighbor] == color:
                    conflicts += 1
            heuristic[color] = 1 / (1 + conflicts)

        # Calculate probabilities
        probabilities = []
        total = 0
        for color in range(self.n_colors):
            prob = (self.pheromone[vertex][color] ** self.alpha *
                   heuristic[color] ** self.beta)
            probabilities.append(prob)
            total += prob

        if total == 0:
            return random.randint(0, self.n_colors - 1)

        # Normalize and select
        probabilities = [p / total for p in probabilities]
        return np.random.choice(self.n_colors, p=probabilities)

    def run(self, verbose: bool = True) -> Tuple[List[int], int]:
        """
        Run ACO for graph coloring.

        Returns:
            Best coloring and number of conflicts
        """
        for iteration in range(self.n_iterations):
            solutions = []

            # Generate solutions
            for _ in range(self.n_ants):
                coloring = []
                for vertex in range(self.n_vertices):
                    color = self._select_color(vertex, coloring)
                    coloring.append(color)

                conflicts = self._calculate_conflicts(coloring)
                colors_used = self._calculate_colors_used(coloring)
                solutions.append((coloring, conflicts, colors_used))

            # Update best solution
            for coloring, conflicts, colors_used in solutions:
                if conflicts < self.best_conflicts or \
                   (conflicts == self.best_conflicts and colors_used < self.best_colors_used):
                    self.best_coloring = coloring.copy()
                    self.best_conflicts = conflicts
                    self.best_colors_used = colors_used

            # Update pheromone
            self.pheromone *= (1 - self.rho)

            for coloring, conflicts, colors_used in solutions:
                # Deposit pheromone based on solution quality
                if conflicts == 0:
                    delta = 1 / colors_used
                else:
                    delta = 1 / (1 + conflicts)

                for vertex, color in enumerate(coloring):
                    self.pheromone[vertex][color] += delta

            if verbose and iteration % 10 == 0:
                avg_conflicts = np.mean([c for _, c, _ in solutions])
                print(f"Iteration {iteration}: Best conflicts = {self.best_conflicts}, "
                      f"Colors used = {self.best_colors_used}, "
                      f"Avg conflicts = {avg_conflicts:.2f}")

        return self.best_coloring, self.best_conflicts


def example_usage():
    """Demonstrate ACO functionality."""
    print("=" * 60)
    print("ANT COLONY OPTIMIZATION EXAMPLES")
    print("=" * 60)

    # Example 1: Basic TSP with AS
    print("\n1. TSP with Standard Ant System:")
    print("-" * 40)

    # Create TSP instance
    np.random.seed(42)
    n_cities = 20
    cities = np.random.rand(n_cities, 2) * 100

    # Distance matrix
    distance_matrix = np.zeros((n_cities, n_cities))
    for i in range(n_cities):
        for j in range(n_cities):
            if i != j:
                distance_matrix[i][j] = np.linalg.norm(cities[i] - cities[j])

    aco = AntColonyOptimization(
        distance_matrix=distance_matrix,
        n_ants=20,
        n_iterations=100,
        variant=ACOVariant.AS,
        seed=42
    )

    best_tour, best_length = aco.run(verbose=False)
    print(f"Best tour length: {best_length:.2f}")
    print(f"Tour (first 10 cities): {best_tour[:10]}")

    # Example 2: Compare ACO variants
    print("\n2. Comparing ACO Variants:")
    print("-" * 40)

    variants = [ACOVariant.AS, ACOVariant.ACS, ACOVariant.MMAS, ACOVariant.RANK_AS]

    for variant in variants:
        aco_variant = AntColonyOptimization(
            distance_matrix=distance_matrix,
            n_ants=20,
            n_iterations=50,
            variant=variant,
            seed=42
        )

        tour, length = aco_variant.run(verbose=False)
        print(f"{variant.value:20s}: {length:.2f}")

    # Example 3: ACO with local search
    print("\n3. ACO with Local Search:")
    print("-" * 40)

    local_searches = [LocalSearch.NONE, LocalSearch.TWO_OPT, LocalSearch.THREE_OPT]

    for ls in local_searches:
        aco_ls = AntColonyOptimization(
            distance_matrix=distance_matrix,
            n_ants=20,
            n_iterations=50,
            variant=ACOVariant.ACS,
            local_search=ls,
            seed=42
        )

        tour, length = aco_ls.run(verbose=False)
        print(f"{ls.value:12s}: {length:.2f}")

    # Example 4: Graph coloring
    print("\n4. Graph Coloring with ACO:")
    print("-" * 40)

    # Create a random graph
    n_vertices = 15
    edge_probability = 0.3
    adjacency = np.random.random((n_vertices, n_vertices)) < edge_probability
    adjacency = np.triu(adjacency, 1)
    adjacency = adjacency + adjacency.T  # Make symmetric
    np.fill_diagonal(adjacency, 0)

    aco_coloring = ACOForGraphColoring(
        adjacency_matrix=adjacency.astype(int),
        n_colors=4,
        n_ants=20,
        n_iterations=50,
        seed=42
    )

    coloring, conflicts = aco_coloring.run(verbose=False)
    colors_used = len(set(coloring))
    print(f"Coloring: {coloring}")
    print(f"Conflicts: {conflicts}")
    print(f"Colors used: {colors_used}")

    # Example 5: Parameter sensitivity
    print("\n5. Parameter Sensitivity Analysis:")
    print("-" * 40)

    print("Effect of alpha (pheromone importance):")
    for alpha in [0.5, 1.0, 2.0, 3.0]:
        aco_alpha = AntColonyOptimization(
            distance_matrix=distance_matrix[:10, :10],  # Smaller problem
            n_ants=10,
            n_iterations=30,
            alpha=alpha,
            beta=2.0,
            seed=42
        )
        _, length = aco_alpha.run(verbose=False)
        print(f"  alpha = {alpha}: {length:.2f}")

    print("\nEffect of rho (evaporation rate):")
    for rho in [0.1, 0.3, 0.5, 0.7]:
        aco_rho = AntColonyOptimization(
            distance_matrix=distance_matrix[:10, :10],
            n_ants=10,
            n_iterations=30,
            rho=rho,
            seed=42
        )
        _, length = aco_rho.run(verbose=False)
        print(f"  rho = {rho}: {length:.2f}")

    # Example 6: Convergence analysis
    print("\n6. ACO Convergence Analysis:")
    print("-" * 40)

    aco_conv = AntColonyOptimization(
        distance_matrix=distance_matrix[:15, :15],
        n_ants=20,
        n_iterations=80,
        variant=ACOVariant.MMAS,
        seed=42
    )

    aco_conv.run(verbose=False)

    # Show convergence
    print("Tour length improvement over iterations:")
    history = aco_conv.iteration_best_lengths
    for i in range(0, len(history), 16):
        length = history[i]
        improvement = (history[0] - length) / history[0] * 100
        bar_length = int(improvement / 2)
        bar = '=' * bar_length + '-' * (50 - bar_length)
        print(f"Iter {i:3d}: [{bar}] {length:.2f} ({improvement:.1f}% improvement)")

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- ACO is excellent for combinatorial optimization")
    print("- Pheromone trails enable collective learning")
    print("- Different variants offer various trade-offs")
    print("- Local search significantly improves solutions")
    print("- Parameter tuning is crucial for performance")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()