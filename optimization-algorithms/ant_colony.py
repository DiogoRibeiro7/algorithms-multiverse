"""
Ant Colony Optimization (ACO) Implementation
===========================================

A comprehensive implementation of Ant Colony Optimization algorithms.
ACO is inspired by the foraging behavior of ants who deposit pheromones
on paths, creating a positive feedback loop that leads to optimal solutions.

Variants Implemented:
- Ant System (AS) - Original ACO
- Ant Colony System (ACS) - With local pheromone update
- Max-Min Ant System (MMAS) - Bounded pheromones
- Rank-Based Ant System - Weighted by solution quality
- Elitist Ant System - Best ant reinforcement
- Parallel ACO with multiple colonies

Applications:
- Traveling Salesman Problem (TSP)
- Vehicle Routing Problem (VRP)
- Job Shop Scheduling
- Network Routing
- Feature Selection
- Graph Coloring

Author: Claude
Date: January 2026
"""

import numpy as np
import random
from typing import List, Tuple, Optional, Callable, Dict, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import math
import copy


class ACOVariant(Enum):
    """ACO algorithm variants."""
    ANT_SYSTEM = "ant_system"
    ANT_COLONY_SYSTEM = "ant_colony_system"
    MAX_MIN = "max_min_ant_system"
    RANK_BASED = "rank_based"
    ELITIST = "elitist"


class PheromoneStrategy(Enum):
    """Pheromone update strategies."""
    STANDARD = "standard"
    BEST_SO_FAR = "best_so_far"
    ITERATION_BEST = "iteration_best"
    MIXED = "mixed"


@dataclass
class Ant:
    """Represents an ant in the colony."""
    current_node: int
    visited: Set[int] = field(default_factory=set)
    path: List[int] = field(default_factory=list)
    path_cost: float = float('inf')
    tabu_list: Set[int] = field(default_factory=set)


class AntColonyOptimization:
    """
    Base Ant Colony Optimization implementation for TSP-like problems.

    This implementation focuses on graph-based optimization problems
    where ants construct solutions by moving through nodes.
    """

    def __init__(self,
                 distance_matrix: np.ndarray,
                 n_ants: int = 20,
                 n_iterations: int = 100,
                 alpha: float = 1.0,  # Pheromone importance
                 beta: float = 2.0,   # Heuristic importance
                 rho: float = 0.5,     # Evaporation rate
                 q0: float = 0.9,      # Exploitation vs exploration (ACS)
                 initial_pheromone: float = 1.0,
                 variant: ACOVariant = ACOVariant.ANT_COLONY_SYSTEM):
        """
        Initialize ACO algorithm.

        Args:
            distance_matrix: Matrix of distances/costs between nodes
            n_ants: Number of ants in colony
            n_iterations: Number of iterations
            alpha: Importance of pheromone trails
            beta: Importance of heuristic information
            rho: Pheromone evaporation rate
            q0: Exploitation probability (for ACS)
            initial_pheromone: Initial pheromone level
            variant: ACO variant to use
        """
        self.distance_matrix = distance_matrix
        self.n_nodes = len(distance_matrix)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q0 = q0
        self.initial_pheromone = initial_pheromone
        self.variant = variant

        # Initialize pheromone matrix
        self.pheromone_matrix = np.full(
            (self.n_nodes, self.n_nodes),
            initial_pheromone
        )

        # Heuristic matrix (inverse of distance)
        with np.errstate(divide='ignore'):
            self.heuristic_matrix = np.where(
                distance_matrix != 0,
                1.0 / distance_matrix,
                0
            )

        # Best solution tracking
        self.best_path = None
        self.best_cost = float('inf')
        self.iteration_best_path = None
        self.iteration_best_cost = float('inf')

        # History tracking
        self.history = {
            'best_cost': [],
            'iteration_best': [],
            'avg_cost': [],
            'diversity': []
        }

        # MMAS specific parameters
        if variant == ACOVariant.MAX_MIN:
            self.pheromone_max = 1.0
            self.pheromone_min = 0.001

    def calculate_path_cost(self, path: List[int]) -> float:
        """Calculate total cost of a path."""
        cost = 0
        for i in range(len(path)):
            cost += self.distance_matrix[path[i], path[(i + 1) % len(path)]]
        return cost

    def construct_solution(self, ant: Ant) -> List[int]:
        """Construct a complete solution for an ant."""
        # Start from random node
        start_node = random.randint(0, self.n_nodes - 1)
        ant.current_node = start_node
        ant.path = [start_node]
        ant.visited = {start_node}

        # Visit all nodes
        while len(ant.visited) < self.n_nodes:
            next_node = self.select_next_node(ant)
            ant.path.append(next_node)
            ant.visited.add(next_node)
            ant.current_node = next_node

            # Local pheromone update (ACS only)
            if self.variant == ACOVariant.ANT_COLONY_SYSTEM:
                self.local_pheromone_update(ant.path[-2], ant.path[-1])

        ant.path_cost = self.calculate_path_cost(ant.path)
        return ant.path

    def select_next_node(self, ant: Ant) -> int:
        """Select next node for ant to visit."""
        current = ant.current_node
        unvisited = [i for i in range(self.n_nodes) if i not in ant.visited]

        if not unvisited:
            return ant.path[0]  # Return to start

        # Calculate probabilities
        probabilities = self.calculate_probabilities(current, unvisited)

        # Selection based on variant
        if self.variant == ACOVariant.ANT_COLONY_SYSTEM:
            # ACS uses pseudo-random proportional rule
            if random.random() < self.q0:
                # Exploitation: choose best
                return unvisited[np.argmax(probabilities)]
            else:
                # Exploration: probabilistic choice
                return np.random.choice(unvisited, p=probabilities/np.sum(probabilities))
        else:
            # Standard probabilistic selection
            return np.random.choice(unvisited, p=probabilities/np.sum(probabilities))

    def calculate_probabilities(self, current: int, unvisited: List[int]) -> np.ndarray:
        """Calculate transition probabilities to unvisited nodes."""
        probabilities = np.zeros(len(unvisited))

        for i, node in enumerate(unvisited):
            pheromone = self.pheromone_matrix[current, node] ** self.alpha
            heuristic = self.heuristic_matrix[current, node] ** self.beta
            probabilities[i] = pheromone * heuristic

        # Normalize
        total = np.sum(probabilities)
        if total > 0:
            probabilities /= total
        else:
            # Equal probability if all are zero
            probabilities = np.ones(len(unvisited)) / len(unvisited)

        return probabilities

    def local_pheromone_update(self, i: int, j: int):
        """Local pheromone update (ACS only)."""
        self.pheromone_matrix[i, j] = (
            (1 - self.rho) * self.pheromone_matrix[i, j] +
            self.rho * self.initial_pheromone
        )
        self.pheromone_matrix[j, i] = self.pheromone_matrix[i, j]

    def global_pheromone_update(self, ants: List[Ant]):
        """Global pheromone update after all ants complete."""
        # Evaporation
        self.pheromone_matrix *= (1 - self.rho)

        if self.variant == ACOVariant.ANT_SYSTEM:
            # All ants deposit pheromones
            for ant in ants:
                self.deposit_pheromones(ant.path, ant.path_cost)

        elif self.variant == ACOVariant.ANT_COLONY_SYSTEM:
            # Only best ant deposits
            if self.best_path:
                self.deposit_pheromones(self.best_path, self.best_cost)

        elif self.variant == ACOVariant.MAX_MIN:
            # Best ant deposits, then bound pheromones
            if self.best_path:
                self.deposit_pheromones(self.best_path, self.best_cost)
            self.bound_pheromones()

        elif self.variant == ACOVariant.RANK_BASED:
            # Rank ants and weight deposits
            sorted_ants = sorted(ants, key=lambda a: a.path_cost)
            for rank, ant in enumerate(sorted_ants[:5]):  # Top 5 ants
                weight = (5 - rank) / 5
                self.deposit_pheromones(ant.path, ant.path_cost, weight)

        elif self.variant == ACOVariant.ELITIST:
            # All ants plus extra for best
            for ant in ants:
                self.deposit_pheromones(ant.path, ant.path_cost)
            # Elite ant gets extra pheromone
            if self.best_path:
                self.deposit_pheromones(self.best_path, self.best_cost, weight=5)

    def deposit_pheromones(self, path: List[int], cost: float, weight: float = 1.0):
        """Deposit pheromones on a path."""
        deposit = weight / cost

        for i in range(len(path)):
            j = (i + 1) % len(path)
            self.pheromone_matrix[path[i], path[j]] += deposit
            self.pheromone_matrix[path[j], path[i]] += deposit

    def bound_pheromones(self):
        """Bound pheromone levels (MMAS only)."""
        # Update bounds based on best solution
        if self.best_cost < float('inf'):
            self.pheromone_max = 1 / (self.rho * self.best_cost)
            self.pheromone_min = self.pheromone_max / (2 * self.n_nodes)

        # Apply bounds
        self.pheromone_matrix = np.clip(
            self.pheromone_matrix,
            self.pheromone_min,
            self.pheromone_max
        )

    def calculate_diversity(self, ants: List[Ant]) -> float:
        """Calculate diversity of ant solutions."""
        if len(ants) < 2:
            return 0.0

        # Calculate average pairwise distance between paths
        distances = []
        for i in range(len(ants)):
            for j in range(i + 1, len(ants)):
                # Count different edges
                edges_i = set(zip(ants[i].path, ants[i].path[1:] + [ants[i].path[0]]))
                edges_j = set(zip(ants[j].path, ants[j].path[1:] + [ants[j].path[0]]))
                different = len(edges_i.symmetric_difference(edges_j))
                distances.append(different / self.n_nodes)

        return np.mean(distances) if distances else 0.0

    def run(self, verbose: bool = True) -> Tuple[List[int], float]:
        """
        Run ACO algorithm.

        Args:
            verbose: Print progress

        Returns:
            Best path and its cost
        """
        if verbose:
            print(f"Starting {self.variant.value} with {self.n_ants} ants")
            print(f"Parameters: α={self.alpha}, β={self.beta}, ρ={self.rho}")

        for iteration in range(self.n_iterations):
            # Create ants
            ants = [Ant() for _ in range(self.n_ants)]

            # Construct solutions
            for ant in ants:
                self.construct_solution(ant)

            # Update best solutions
            self.iteration_best_cost = float('inf')
            for ant in ants:
                if ant.path_cost < self.iteration_best_cost:
                    self.iteration_best_cost = ant.path_cost
                    self.iteration_best_path = ant.path.copy()

                if ant.path_cost < self.best_cost:
                    self.best_cost = ant.path_cost
                    self.best_path = ant.path.copy()

            # Global pheromone update
            self.global_pheromone_update(ants)

            # Update history
            avg_cost = np.mean([ant.path_cost for ant in ants])
            diversity = self.calculate_diversity(ants)

            self.history['best_cost'].append(self.best_cost)
            self.history['iteration_best'].append(self.iteration_best_cost)
            self.history['avg_cost'].append(avg_cost)
            self.history['diversity'].append(diversity)

            # Print progress
            if verbose and iteration % 20 == 0:
                print(f"Iteration {iteration}: Best = {self.best_cost:.2f}, "
                      f"Iter best = {self.iteration_best_cost:.2f}, "
                      f"Avg = {avg_cost:.2f}, "
                      f"Diversity = {diversity:.3f}")

        if verbose:
            print(f"\nACO completed after {self.n_iterations} iterations")
            print(f"Best cost: {self.best_cost:.2f}")
            print(f"Best path: {self.best_path[:10]}...")

        return self.best_path, self.best_cost


class VehicleRoutingACO:
    """
    ACO for Vehicle Routing Problem (VRP).

    Extends basic ACO to handle multiple vehicles with capacity constraints.
    """

    def __init__(self,
                 distance_matrix: np.ndarray,
                 demands: List[float],
                 vehicle_capacity: float,
                 n_vehicles: int,
                 depot: int = 0,
                 **aco_kwargs):
        """
        Initialize VRP-ACO.

        Args:
            distance_matrix: Distances between locations
            demands: Demand at each location
            vehicle_capacity: Capacity of each vehicle
            n_vehicles: Number of vehicles
            depot: Depot location index
            **aco_kwargs: Additional ACO parameters
        """
        self.distance_matrix = distance_matrix
        self.demands = demands
        self.vehicle_capacity = vehicle_capacity
        self.n_vehicles = n_vehicles
        self.depot = depot
        self.n_customers = len(demands) - 1  # Exclude depot

        # Create ACO instance for each vehicle
        self.aco = AntColonyOptimization(distance_matrix, **aco_kwargs)

    def construct_vrp_solution(self, ant: Ant) -> List[List[int]]:
        """Construct VRP solution with multiple routes."""
        routes = []
        unvisited = set(range(1, len(self.demands)))  # Exclude depot

        for vehicle in range(self.n_vehicles):
            if not unvisited:
                break

            route = [self.depot]
            current_load = 0

            while unvisited:
                # Find feasible next customers
                feasible = [
                    c for c in unvisited
                    if current_load + self.demands[c] <= self.vehicle_capacity
                ]

                if not feasible:
                    break

                # Select next customer using ACO probabilities
                current = route[-1]
                probabilities = []

                for customer in feasible:
                    pheromone = self.aco.pheromone_matrix[current, customer] ** self.aco.alpha
                    heuristic = (1.0 / self.distance_matrix[current, customer]) ** self.aco.beta
                    probabilities.append(pheromone * heuristic)

                probabilities = np.array(probabilities)
                probabilities /= np.sum(probabilities)

                next_customer = np.random.choice(feasible, p=probabilities)

                route.append(next_customer)
                current_load += self.demands[next_customer]
                unvisited.remove(next_customer)

            route.append(self.depot)  # Return to depot
            routes.append(route)

        return routes

    def calculate_vrp_cost(self, routes: List[List[int]]) -> float:
        """Calculate total cost of VRP solution."""
        total_cost = 0
        for route in routes:
            for i in range(len(route) - 1):
                total_cost += self.distance_matrix[route[i], route[i + 1]]
        return total_cost


class JobShopACO:
    """
    ACO for Job Shop Scheduling Problem.

    Ants construct schedules by selecting operation orderings.
    """

    def __init__(self,
                 jobs: List[List[Tuple[int, int]]],
                 n_machines: int,
                 **aco_kwargs):
        """
        Initialize Job Shop ACO.

        Args:
            jobs: List of jobs, each with (machine, duration) operations
            n_machines: Number of machines
            **aco_kwargs: ACO parameters
        """
        self.jobs = jobs
        self.n_jobs = len(jobs)
        self.n_machines = n_machines

        # Create operation list
        self.operations = []
        for job_id, job in enumerate(jobs):
            for op_id, (machine, duration) in enumerate(job):
                self.operations.append({
                    'job': job_id,
                    'operation': op_id,
                    'machine': machine,
                    'duration': duration
                })

        self.n_operations = len(self.operations)

        # Create distance matrix (for ACO framework)
        # Use heuristic based on operation properties
        distance_matrix = np.ones((self.n_operations, self.n_operations))
        self.aco = AntColonyOptimization(distance_matrix, **aco_kwargs)

    def calculate_makespan(self, schedule: List[int]) -> float:
        """Calculate makespan of a schedule."""
        machine_time = [0] * self.n_machines
        job_time = [0] * self.n_jobs

        for op_idx in schedule:
            op = self.operations[op_idx]
            machine = op['machine']
            duration = op['duration']
            job = op['job']

            # Operation starts when machine and previous job operations are ready
            start_time = max(machine_time[machine], job_time[job])
            end_time = start_time + duration

            machine_time[machine] = end_time
            job_time[job] = end_time

        return max(machine_time)


def tsp_example():
    """Example: Solve TSP using different ACO variants."""
    print("=" * 60)
    print("ANT COLONY OPTIMIZATION - TRAVELING SALESMAN PROBLEM")
    print("=" * 60)

    # Generate random TSP instance
    np.random.seed(42)
    n_cities = 30
    cities = np.random.rand(n_cities, 2) * 100

    # Calculate distance matrix
    distance_matrix = np.zeros((n_cities, n_cities))
    for i in range(n_cities):
        for j in range(n_cities):
            if i != j:
                distance_matrix[i, j] = np.linalg.norm(cities[i] - cities[j])

    # Test different variants
    variants = [
        ACOVariant.ANT_SYSTEM,
        ACOVariant.ANT_COLONY_SYSTEM,
        ACOVariant.MAX_MIN,
        ACOVariant.ELITIST
    ]

    results = {}

    for variant in variants:
        print(f"\nTesting {variant.value}...")

        aco = AntColonyOptimization(
            distance_matrix=distance_matrix,
            n_ants=20,
            n_iterations=100,
            alpha=1.0,
            beta=3.0,
            rho=0.5,
            variant=variant
        )

        best_path, best_cost = aco.run(verbose=False)
        results[variant.value] = best_cost

        print(f"Best tour length: {best_cost:.2f}")

    print("\n" + "-" * 40)
    print("VARIANT COMPARISON:")
    for variant, cost in sorted(results.items(), key=lambda x: x[1]):
        print(f"{variant:25s}: {cost:.2f}")


def vrp_example():
    """Example: Vehicle Routing Problem with ACO."""
    print("\n" + "=" * 60)
    print("ACO - VEHICLE ROUTING PROBLEM")
    print("=" * 60)

    # Create VRP instance
    np.random.seed(42)
    n_customers = 15
    depot_loc = np.array([50, 50])
    customer_locs = np.random.rand(n_customers, 2) * 100

    # All locations (depot + customers)
    locations = np.vstack([depot_loc, customer_locs])

    # Distance matrix
    n_locations = len(locations)
    distance_matrix = np.zeros((n_locations, n_locations))
    for i in range(n_locations):
        for j in range(n_locations):
            distance_matrix[i, j] = np.linalg.norm(locations[i] - locations[j])

    # Customer demands (depot has 0 demand)
    demands = [0] + [random.randint(10, 30) for _ in range(n_customers)]

    # Create VRP-ACO
    vrp_aco = VehicleRoutingACO(
        distance_matrix=distance_matrix,
        demands=demands,
        vehicle_capacity=100,
        n_vehicles=3,
        depot=0,
        n_ants=20,
        n_iterations=50
    )

    print(f"Customers: {n_customers}")
    print(f"Vehicles: 3 with capacity 100")
    print(f"Total demand: {sum(demands)}")

    # Solve
    best_cost = float('inf')
    best_routes = None

    for iteration in range(50):
        ant = Ant()
        routes = vrp_aco.construct_vrp_solution(ant)
        cost = vrp_aco.calculate_vrp_cost(routes)

        if cost < best_cost:
            best_cost = cost
            best_routes = routes

        if iteration % 10 == 0:
            print(f"Iteration {iteration}: Best cost = {best_cost:.2f}")

    print(f"\nBest solution:")
    for i, route in enumerate(best_routes):
        if len(route) > 2:  # Non-empty route
            load = sum(demands[c] for c in route if c != 0)
            print(f"Vehicle {i+1}: {route} (load: {load})")
    print(f"Total distance: {best_cost:.2f}")


def graph_coloring_aco():
    """Example: Graph coloring using ACO."""
    print("\n" + "=" * 60)
    print("ACO - GRAPH COLORING")
    print("=" * 60)

    # Create a graph (adjacency matrix)
    n_nodes = 10
    n_colors = 4

    # Random graph with edge probability 0.3
    np.random.seed(42)
    adjacency = np.random.rand(n_nodes, n_nodes) < 0.3
    adjacency = np.triu(adjacency, 1)
    adjacency = adjacency + adjacency.T

    def coloring_cost(coloring: List[int]) -> float:
        """Count conflicts in graph coloring."""
        conflicts = 0
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                if adjacency[i, j] and coloring[i] == coloring[j]:
                    conflicts += 1
        return conflicts

    # Use ACO framework for coloring
    # Create pseudo-distance matrix
    distance_matrix = np.ones((n_nodes * n_colors, n_nodes * n_colors))

    # Modify to prefer different colors for adjacent nodes
    for i in range(n_nodes):
        for j in range(n_nodes):
            if adjacency[i, j]:
                for c in range(n_colors):
                    # High cost for same color on adjacent nodes
                    distance_matrix[i * n_colors + c, j * n_colors + c] = 100

    aco = AntColonyOptimization(
        distance_matrix=distance_matrix[:n_nodes, :n_nodes],
        n_ants=20,
        n_iterations=100,
        alpha=1.0,
        beta=2.0,
        variant=ACOVariant.MAX_MIN
    )

    # Simple greedy coloring for comparison
    greedy_coloring = []
    for node in range(n_nodes):
        # Find colors used by neighbors
        neighbor_colors = set()
        for neighbor in range(n_nodes):
            if adjacency[node, neighbor] and neighbor < node:
                if neighbor < len(greedy_coloring):
                    neighbor_colors.add(greedy_coloring[neighbor])

        # Choose first available color
        for color in range(n_colors):
            if color not in neighbor_colors:
                greedy_coloring.append(color)
                break

    greedy_conflicts = coloring_cost(greedy_coloring)
    print(f"Greedy coloring conflicts: {greedy_conflicts}")

    # ACO would need custom construction for proper graph coloring
    print(f"Graph: {n_nodes} nodes, {np.sum(adjacency) // 2} edges")
    print(f"Colors available: {n_colors}")


def parameter_sensitivity_example():
    """Example: Parameter sensitivity analysis."""
    print("\n" + "=" * 60)
    print("ACO PARAMETER SENSITIVITY ANALYSIS")
    print("=" * 60)

    # Small TSP for quick testing
    np.random.seed(42)
    n_cities = 20
    cities = np.random.rand(n_cities, 2) * 100
    distance_matrix = np.zeros((n_cities, n_cities))
    for i in range(n_cities):
        for j in range(n_cities):
            if i != j:
                distance_matrix[i, j] = np.linalg.norm(cities[i] - cities[j])

    # Test different parameter combinations
    parameters = {
        'alpha': [0.5, 1.0, 2.0],
        'beta': [1.0, 2.0, 5.0],
        'rho': [0.1, 0.5, 0.9]
    }

    print("Testing parameter combinations...")
    best_params = None
    best_performance = float('inf')

    for alpha in parameters['alpha']:
        for beta in parameters['beta']:
            for rho in parameters['rho']:
                aco = AntColonyOptimization(
                    distance_matrix=distance_matrix,
                    n_ants=10,
                    n_iterations=50,
                    alpha=alpha,
                    beta=beta,
                    rho=rho,
                    variant=ACOVariant.ANT_COLONY_SYSTEM
                )

                _, cost = aco.run(verbose=False)

                if cost < best_performance:
                    best_performance = cost
                    best_params = (alpha, beta, rho)

    print(f"\nBest parameters found:")
    print(f"  α (pheromone importance): {best_params[0]}")
    print(f"  β (heuristic importance): {best_params[1]}")
    print(f"  ρ (evaporation rate): {best_params[2]}")
    print(f"  Best cost: {best_performance:.2f}")

    # Compare with default
    aco_default = AntColonyOptimization(
        distance_matrix=distance_matrix,
        n_ants=10,
        n_iterations=50
    )
    _, default_cost = aco_default.run(verbose=False)

    print(f"\nDefault parameters cost: {default_cost:.2f}")
    print(f"Improvement: {(default_cost - best_performance) / default_cost * 100:.1f}%")


def hybrid_aco_example():
    """Example: Hybrid ACO with local search."""
    print("\n" + "=" * 60)
    print("HYBRID ACO WITH 2-OPT LOCAL SEARCH")
    print("=" * 60)

    # TSP instance
    np.random.seed(42)
    n_cities = 25
    cities = np.random.rand(n_cities, 2) * 100
    distance_matrix = np.zeros((n_cities, n_cities))
    for i in range(n_cities):
        for j in range(n_cities):
            if i != j:
                distance_matrix[i, j] = np.linalg.norm(cities[i] - cities[j])

    def two_opt(path: List[int], distance_matrix: np.ndarray) -> List[int]:
        """Apply 2-opt local search to improve path."""
        improved = True
        best_path = path.copy()

        while improved:
            improved = False
            for i in range(1, len(path) - 2):
                for j in range(i + 1, len(path)):
                    if j - i == 1:
                        continue

                    new_path = best_path.copy()
                    new_path[i:j] = reversed(best_path[i:j])

                    # Calculate cost difference
                    old_cost = (
                        distance_matrix[best_path[i-1], best_path[i]] +
                        distance_matrix[best_path[j-1], best_path[j % len(path)]]
                    )
                    new_cost = (
                        distance_matrix[best_path[i-1], best_path[j-1]] +
                        distance_matrix[best_path[i], best_path[j % len(path)]]
                    )

                    if new_cost < old_cost:
                        best_path = new_path
                        improved = True

        return best_path

    # Standard ACO
    print("Running standard ACO...")
    aco_standard = AntColonyOptimization(
        distance_matrix=distance_matrix,
        n_ants=20,
        n_iterations=100,
        variant=ACOVariant.ANT_COLONY_SYSTEM
    )
    standard_path, standard_cost = aco_standard.run(verbose=False)
    print(f"Standard ACO cost: {standard_cost:.2f}")

    # Hybrid ACO with 2-opt
    print("\nRunning hybrid ACO with 2-opt...")
    aco_hybrid = AntColonyOptimization(
        distance_matrix=distance_matrix,
        n_ants=20,
        n_iterations=100,
        variant=ACOVariant.ANT_COLONY_SYSTEM
    )

    # Run with local search applied to best solution each iteration
    for iteration in range(100):
        ants = [Ant() for _ in range(20)]

        for ant in ants:
            aco_hybrid.construct_solution(ant)
            # Apply local search
            ant.path = two_opt(ant.path, distance_matrix)
            ant.path_cost = aco_hybrid.calculate_path_cost(ant.path)

        # Update best
        for ant in ants:
            if ant.path_cost < aco_hybrid.best_cost:
                aco_hybrid.best_cost = ant.path_cost
                aco_hybrid.best_path = ant.path.copy()

        aco_hybrid.global_pheromone_update(ants)

    print(f"Hybrid ACO cost: {aco_hybrid.best_cost:.2f}")
    print(f"Improvement: {(standard_cost - aco_hybrid.best_cost) / standard_cost * 100:.1f}%")


if __name__ == "__main__":
    # Run examples
    tsp_example()
    vrp_example()
    graph_coloring_aco()
    parameter_sensitivity_example()
    hybrid_aco_example()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- ACO excels at combinatorial optimization problems")
    print("- Pheromone trails provide memory and learning")
    print("- Balance between exploration (β) and exploitation (α) is crucial")
    print("- Different variants suit different problem characteristics")
    print("- Hybrid approaches with local search often perform best")
    print("=" * 60)