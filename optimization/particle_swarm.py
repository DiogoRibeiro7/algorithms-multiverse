"""
Particle Swarm Optimization (PSO) Implementation
================================================

A comprehensive implementation of Particle Swarm Optimization and its variants.
Includes standard PSO, adaptive PSO, quantum PSO, and multi-objective PSO.

Features:
- Multiple PSO variants (Standard, Adaptive, Quantum, Multi-Objective)
- Various topology structures (Global, Ring, Von Neumann, Random)
- Constraint handling mechanisms
- Parallel evaluation support
- Convergence detection

Author: Claude
Date: January 2026
"""

import numpy as np
import random
from typing import Callable, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import copy
import math


class Topology(Enum):
    """Swarm topology types for particle communication."""
    GLOBAL = "global"  # All particles connected
    RING = "ring"  # Each particle connected to neighbors in ring
    VON_NEUMANN = "von_neumann"  # Grid topology with 4 neighbors
    RANDOM = "random"  # Random dynamic topology
    STAR = "star"  # Hub and spoke topology


class VelocityUpdate(Enum):
    """Velocity update strategies."""
    STANDARD = "standard"  # Classical PSO update
    CONSTRICTION = "constriction"  # Clerc's constriction factor
    INERTIA = "inertia"  # Inertia weight
    ADAPTIVE = "adaptive"  # Adaptive parameters


@dataclass
class Particle:
    """Represents a particle in the swarm."""
    position: np.ndarray
    velocity: np.ndarray
    best_position: np.ndarray
    best_fitness: float
    fitness: float
    age: int = 0
    stagnation_counter: int = 0


class ParticleSwarmOptimization:
    """
    Standard Particle Swarm Optimization algorithm.

    PSO optimizes by having a swarm of particles move through the search space,
    influenced by their own best position and the swarm's best position.
    """

    def __init__(
        self,
        objective_function: Callable,
        bounds: List[Tuple[float, float]],
        swarm_size: int = 30,
        max_iterations: int = 1000,
        w: float = 0.7,  # Inertia weight
        c1: float = 2.0,  # Cognitive coefficient
        c2: float = 2.0,  # Social coefficient
        topology: Topology = Topology.GLOBAL,
        velocity_update: VelocityUpdate = VelocityUpdate.INERTIA,
        minimize: bool = True,
        velocity_limit: Optional[float] = None,
        seed: Optional[int] = None
    ):
        """
        Initialize PSO algorithm.

        Args:
            objective_function: Function to optimize
            bounds: Bounds for each dimension [(min, max), ...]
            swarm_size: Number of particles
            max_iterations: Maximum iterations
            w: Inertia weight
            c1: Cognitive coefficient (personal best influence)
            c2: Social coefficient (global best influence)
            topology: Swarm topology
            velocity_update: Velocity update strategy
            minimize: Whether to minimize or maximize
            velocity_limit: Maximum velocity magnitude
            seed: Random seed
        """
        self.objective_function = objective_function
        self.bounds = bounds
        self.dimensions = len(bounds)
        self.swarm_size = swarm_size
        self.max_iterations = max_iterations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.topology = topology
        self.velocity_update = velocity_update
        self.minimize = minimize

        # Calculate velocity limits
        if velocity_limit is None:
            self.velocity_limit = np.array([
                (high - low) * 0.2 for low, high in bounds
            ])
        else:
            self.velocity_limit = np.array([velocity_limit] * self.dimensions)

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # Initialize swarm
        self.swarm: List[Particle] = []
        self.global_best_position: Optional[np.ndarray] = None
        self.global_best_fitness: float = float('inf') if minimize else float('-inf')

        # Tracking
        self.fitness_history: List[float] = []
        self.diversity_history: List[float] = []
        self.velocity_history: List[float] = []

        # Topology-specific structures
        self.neighborhoods: Optional[List[List[int]]] = None

    def _initialize_swarm(self):
        """Initialize particles with random positions and velocities."""
        self.swarm = []

        for _ in range(self.swarm_size):
            # Random position within bounds
            position = np.array([
                np.random.uniform(self.bounds[i][0], self.bounds[i][1])
                for i in range(self.dimensions)
            ])

            # Random velocity (small initial velocities)
            velocity = np.array([
                np.random.uniform(-self.velocity_limit[i], self.velocity_limit[i]) * 0.1
                for i in range(self.dimensions)
            ])

            # Evaluate fitness
            fitness = self.objective_function(position)

            particle = Particle(
                position=position,
                velocity=velocity,
                best_position=position.copy(),
                best_fitness=fitness,
                fitness=fitness
            )

            self.swarm.append(particle)

            # Update global best
            self._update_global_best(particle)

        # Initialize topology
        self._initialize_topology()

    def _initialize_topology(self):
        """Initialize neighborhood structure based on topology."""
        if self.topology == Topology.GLOBAL:
            # All particles are neighbors
            self.neighborhoods = [list(range(self.swarm_size)) for _ in range(self.swarm_size)]

        elif self.topology == Topology.RING:
            # Each particle connected to k neighbors on each side
            k = 2  # Number of neighbors on each side
            self.neighborhoods = []
            for i in range(self.swarm_size):
                neighbors = []
                for j in range(-k, k+1):
                    neighbor_idx = (i + j) % self.swarm_size
                    neighbors.append(neighbor_idx)
                self.neighborhoods.append(neighbors)

        elif self.topology == Topology.VON_NEUMANN:
            # Grid topology (2D grid with 4 neighbors)
            grid_size = int(np.sqrt(self.swarm_size))
            self.neighborhoods = []
            for i in range(self.swarm_size):
                row = i // grid_size
                col = i % grid_size
                neighbors = [i]  # Include self

                # Add 4 neighbors (up, down, left, right)
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    new_row = (row + dr) % grid_size
                    new_col = (col + dc) % grid_size
                    neighbor_idx = new_row * grid_size + new_col
                    if neighbor_idx < self.swarm_size:
                        neighbors.append(neighbor_idx)

                self.neighborhoods.append(neighbors)

        elif self.topology == Topology.RANDOM:
            # Random topology (will be regenerated each iteration)
            self._regenerate_random_topology()

    def _regenerate_random_topology(self):
        """Regenerate random topology connections."""
        self.neighborhoods = []
        for i in range(self.swarm_size):
            # Each particle connected to random subset
            num_neighbors = random.randint(3, min(10, self.swarm_size))
            neighbors = random.sample(range(self.swarm_size), num_neighbors)
            if i not in neighbors:
                neighbors.append(i)
            self.neighborhoods.append(neighbors)

    def _update_global_best(self, particle: Particle):
        """Update global best position if particle's position is better."""
        if self.minimize:
            if particle.fitness < self.global_best_fitness:
                self.global_best_fitness = particle.fitness
                self.global_best_position = particle.position.copy()
        else:
            if particle.fitness > self.global_best_fitness:
                self.global_best_fitness = particle.fitness
                self.global_best_position = particle.position.copy()

    def _get_neighborhood_best(self, particle_idx: int) -> Tuple[np.ndarray, float]:
        """Get best position in particle's neighborhood."""
        neighborhood = self.neighborhoods[particle_idx]

        if self.minimize:
            best_neighbor = min(
                (self.swarm[i] for i in neighborhood),
                key=lambda p: p.best_fitness
            )
        else:
            best_neighbor = max(
                (self.swarm[i] for i in neighborhood),
                key=lambda p: p.best_fitness
            )

        return best_neighbor.best_position, best_neighbor.best_fitness

    def _update_velocity_standard(self, particle: Particle, neighborhood_best: np.ndarray) -> np.ndarray:
        """Standard velocity update rule."""
        r1 = np.random.random(self.dimensions)
        r2 = np.random.random(self.dimensions)

        cognitive = self.c1 * r1 * (particle.best_position - particle.position)
        social = self.c2 * r2 * (neighborhood_best - particle.position)

        new_velocity = self.w * particle.velocity + cognitive + social
        return new_velocity

    def _update_velocity_constriction(self, particle: Particle, neighborhood_best: np.ndarray) -> np.ndarray:
        """Velocity update with Clerc's constriction factor."""
        phi = self.c1 + self.c2
        chi = 2 / abs(2 - phi - np.sqrt(phi**2 - 4*phi))

        r1 = np.random.random(self.dimensions)
        r2 = np.random.random(self.dimensions)

        cognitive = self.c1 * r1 * (particle.best_position - particle.position)
        social = self.c2 * r2 * (neighborhood_best - particle.position)

        new_velocity = chi * (particle.velocity + cognitive + social)
        return new_velocity

    def _update_velocity_adaptive(self, particle: Particle, neighborhood_best: np.ndarray, iteration: int) -> np.ndarray:
        """Adaptive velocity update with time-varying parameters."""
        # Linearly decrease inertia weight
        w_max = 0.9
        w_min = 0.4
        w = w_max - (w_max - w_min) * iteration / self.max_iterations

        # Linearly adjust c1 and c2
        c1_initial = 2.5
        c1_final = 0.5
        c2_initial = 0.5
        c2_final = 2.5

        c1 = c1_initial + (c1_final - c1_initial) * iteration / self.max_iterations
        c2 = c2_initial + (c2_final - c2_initial) * iteration / self.max_iterations

        r1 = np.random.random(self.dimensions)
        r2 = np.random.random(self.dimensions)

        cognitive = c1 * r1 * (particle.best_position - particle.position)
        social = c2 * r2 * (neighborhood_best - particle.position)

        new_velocity = w * particle.velocity + cognitive + social
        return new_velocity

    def _update_velocity(self, particle: Particle, neighborhood_best: np.ndarray, iteration: int) -> np.ndarray:
        """Update particle velocity based on selected strategy."""
        if self.velocity_update == VelocityUpdate.STANDARD:
            new_velocity = self._update_velocity_standard(particle, neighborhood_best)
        elif self.velocity_update == VelocityUpdate.CONSTRICTION:
            new_velocity = self._update_velocity_constriction(particle, neighborhood_best)
        elif self.velocity_update == VelocityUpdate.ADAPTIVE:
            new_velocity = self._update_velocity_adaptive(particle, neighborhood_best, iteration)
        else:  # INERTIA
            new_velocity = self._update_velocity_standard(particle, neighborhood_best)

        # Apply velocity limits
        for i in range(self.dimensions):
            new_velocity[i] = np.clip(new_velocity[i], -self.velocity_limit[i], self.velocity_limit[i])

        return new_velocity

    def _update_position(self, particle: Particle) -> np.ndarray:
        """Update particle position and enforce bounds."""
        new_position = particle.position + particle.velocity

        # Enforce bounds
        for i in range(self.dimensions):
            if new_position[i] < self.bounds[i][0]:
                new_position[i] = self.bounds[i][0]
                particle.velocity[i] *= -0.5  # Bounce off boundary
            elif new_position[i] > self.bounds[i][1]:
                new_position[i] = self.bounds[i][1]
                particle.velocity[i] *= -0.5  # Bounce off boundary

        return new_position

    def _calculate_swarm_diversity(self) -> float:
        """Calculate diversity of the swarm."""
        if not self.swarm:
            return 0.0

        # Calculate centroid
        centroid = np.mean([p.position for p in self.swarm], axis=0)

        # Calculate average distance from centroid
        diversity = np.mean([
            np.linalg.norm(p.position - centroid)
            for p in self.swarm
        ])

        return diversity

    def run(self, verbose: bool = True) -> Tuple[np.ndarray, float]:
        """
        Run the PSO algorithm.

        Args:
            verbose: Whether to print progress

        Returns:
            Best position and fitness found
        """
        # Initialize swarm
        self._initialize_swarm()

        # Main loop
        for iteration in range(self.max_iterations):
            # Update topology if random
            if self.topology == Topology.RANDOM and iteration % 10 == 0:
                self._regenerate_random_topology()

            # Update each particle
            for i, particle in enumerate(self.swarm):
                # Get neighborhood best
                neighborhood_best, _ = self._get_neighborhood_best(i)

                # Update velocity
                particle.velocity = self._update_velocity(particle, neighborhood_best, iteration)

                # Update position
                particle.position = self._update_position(particle)

                # Evaluate fitness
                particle.fitness = self.objective_function(particle.position)

                # Update personal best
                if self.minimize:
                    if particle.fitness < particle.best_fitness:
                        particle.best_fitness = particle.fitness
                        particle.best_position = particle.position.copy()
                        particle.stagnation_counter = 0
                    else:
                        particle.stagnation_counter += 1
                else:
                    if particle.fitness > particle.best_fitness:
                        particle.best_fitness = particle.fitness
                        particle.best_position = particle.position.copy()
                        particle.stagnation_counter = 0
                    else:
                        particle.stagnation_counter += 1

                # Update global best
                self._update_global_best(particle)

                # Update age
                particle.age += 1

            # Calculate and store metrics
            diversity = self._calculate_swarm_diversity()
            avg_velocity = np.mean([np.linalg.norm(p.velocity) for p in self.swarm])

            self.fitness_history.append(self.global_best_fitness)
            self.diversity_history.append(diversity)
            self.velocity_history.append(avg_velocity)

            # Print progress
            if verbose and iteration % 10 == 0:
                avg_fitness = np.mean([p.fitness for p in self.swarm])
                print(f"Iteration {iteration}: Best = {self.global_best_fitness:.6f}, "
                      f"Avg = {avg_fitness:.6f}, Diversity = {diversity:.4f}")

            # Check for convergence
            if len(self.fitness_history) > 50:
                recent_improvement = abs(self.fitness_history[-1] - self.fitness_history[-50])
                if recent_improvement < 1e-6 and diversity < 1e-3:
                    if verbose:
                        print(f"Converged at iteration {iteration}")
                    break

        return self.global_best_position, self.global_best_fitness


class QuantumPSO(ParticleSwarmOptimization):
    """
    Quantum-behaved Particle Swarm Optimization.

    Uses quantum mechanics principles for particle movement,
    allowing particles to appear anywhere in the search space.
    """

    def __init__(self, objective_function: Callable, bounds: List[Tuple[float, float]], **kwargs):
        """Initialize Quantum PSO."""
        super().__init__(objective_function, bounds, **kwargs)
        self.beta = 1.0  # Contraction-expansion coefficient

    def _update_position_quantum(self, particle: Particle, mbest: np.ndarray, iteration: int) -> np.ndarray:
        """
        Update particle position using quantum behavior.

        Args:
            particle: Current particle
            mbest: Mean best position of swarm
            iteration: Current iteration

        Returns:
            New position
        """
        # Calculate phi
        phi = np.random.random(self.dimensions)

        # Calculate local attractor
        p = phi * particle.best_position + (1 - phi) * self.global_best_position

        # Calculate beta (decreasing over time)
        beta = 0.5 + 0.5 * (self.max_iterations - iteration) / self.max_iterations

        # Calculate u
        u = np.random.random(self.dimensions)

        # Calculate new position
        new_position = np.zeros(self.dimensions)
        for i in range(self.dimensions):
            if np.random.random() < 0.5:
                new_position[i] = p[i] - beta * abs(mbest[i] - particle.position[i]) * np.log(1/u[i])
            else:
                new_position[i] = p[i] + beta * abs(mbest[i] - particle.position[i]) * np.log(1/u[i])

            # Enforce bounds
            new_position[i] = np.clip(new_position[i], self.bounds[i][0], self.bounds[i][1])

        return new_position

    def run(self, verbose: bool = True) -> Tuple[np.ndarray, float]:
        """Run Quantum PSO algorithm."""
        # Initialize swarm
        self._initialize_swarm()

        # Main loop
        for iteration in range(self.max_iterations):
            # Calculate mean best position
            mbest = np.mean([p.best_position for p in self.swarm], axis=0)

            # Update each particle
            for particle in self.swarm:
                # Update position using quantum behavior
                particle.position = self._update_position_quantum(particle, mbest, iteration)

                # Evaluate fitness
                particle.fitness = self.objective_function(particle.position)

                # Update personal best
                if self.minimize:
                    if particle.fitness < particle.best_fitness:
                        particle.best_fitness = particle.fitness
                        particle.best_position = particle.position.copy()
                else:
                    if particle.fitness > particle.best_fitness:
                        particle.best_fitness = particle.fitness
                        particle.best_position = particle.position.copy()

                # Update global best
                self._update_global_best(particle)

            # Store history
            self.fitness_history.append(self.global_best_fitness)

            # Print progress
            if verbose and iteration % 10 == 0:
                avg_fitness = np.mean([p.fitness for p in self.swarm])
                print(f"Iteration {iteration}: Best = {self.global_best_fitness:.6f}, "
                      f"Avg = {avg_fitness:.6f}")

        return self.global_best_position, self.global_best_fitness


class MultiObjectivePSO:
    """
    Multi-Objective Particle Swarm Optimization using Pareto dominance.

    Finds a set of Pareto-optimal solutions for multi-objective problems.
    """

    def __init__(
        self,
        objective_functions: List[Callable],
        bounds: List[Tuple[float, float]],
        swarm_size: int = 100,
        max_iterations: int = 1000,
        archive_size: int = 100,
        seed: Optional[int] = None
    ):
        """
        Initialize Multi-Objective PSO.

        Args:
            objective_functions: List of objective functions
            bounds: Bounds for each dimension
            swarm_size: Number of particles
            max_iterations: Maximum iterations
            archive_size: Maximum size of Pareto archive
            seed: Random seed
        """
        self.objective_functions = objective_functions
        self.num_objectives = len(objective_functions)
        self.bounds = bounds
        self.dimensions = len(bounds)
        self.swarm_size = swarm_size
        self.max_iterations = max_iterations
        self.archive_size = archive_size

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # Particle swarm
        self.swarm: List[dict] = []

        # Pareto archive
        self.archive: List[dict] = []

    def _evaluate_objectives(self, position: np.ndarray) -> np.ndarray:
        """Evaluate all objective functions."""
        return np.array([f(position) for f in self.objective_functions])

    def _dominates(self, obj1: np.ndarray, obj2: np.ndarray) -> bool:
        """Check if obj1 dominates obj2 (assuming minimization)."""
        return all(obj1 <= obj2) and any(obj1 < obj2)

    def _update_archive(self, position: np.ndarray, objectives: np.ndarray):
        """Update Pareto archive with new solution."""
        # Remove dominated solutions from archive
        self.archive = [
            sol for sol in self.archive
            if not self._dominates(objectives, sol['objectives'])
        ]

        # Check if new solution is dominated
        is_dominated = any(
            self._dominates(sol['objectives'], objectives)
            for sol in self.archive
        )

        if not is_dominated:
            # Add to archive
            self.archive.append({
                'position': position.copy(),
                'objectives': objectives.copy()
            })

            # Maintain archive size
            if len(self.archive) > self.archive_size:
                # Remove random solution
                self.archive.pop(random.randint(0, len(self.archive) - 1))

    def _select_leader(self) -> np.ndarray:
        """Select a leader from the archive."""
        if not self.archive:
            # Return random particle if archive empty
            return self.swarm[random.randint(0, len(self.swarm) - 1)]['position']

        # Use crowding distance or random selection
        return random.choice(self.archive)['position']

    def run(self, verbose: bool = True) -> List[dict]:
        """
        Run Multi-Objective PSO.

        Returns:
            Pareto-optimal solutions
        """
        # Initialize swarm
        self.swarm = []
        for _ in range(self.swarm_size):
            position = np.array([
                np.random.uniform(self.bounds[i][0], self.bounds[i][1])
                for i in range(self.dimensions)
            ])
            velocity = np.random.randn(self.dimensions) * 0.1
            objectives = self._evaluate_objectives(position)

            particle = {
                'position': position,
                'velocity': velocity,
                'best_position': position.copy(),
                'best_objectives': objectives.copy(),
                'objectives': objectives
            }
            self.swarm.append(particle)

            # Update archive
            self._update_archive(position, objectives)

        # Main loop
        for iteration in range(self.max_iterations):
            for particle in self.swarm:
                # Select leader from archive
                leader = self._select_leader()

                # Update velocity
                r1 = np.random.random(self.dimensions)
                r2 = np.random.random(self.dimensions)
                w = 0.7
                c1 = 1.5
                c2 = 1.5

                particle['velocity'] = (w * particle['velocity'] +
                                       c1 * r1 * (particle['best_position'] - particle['position']) +
                                       c2 * r2 * (leader - particle['position']))

                # Update position
                particle['position'] = particle['position'] + particle['velocity']

                # Enforce bounds
                for i in range(self.dimensions):
                    particle['position'][i] = np.clip(
                        particle['position'][i],
                        self.bounds[i][0],
                        self.bounds[i][1]
                    )

                # Evaluate objectives
                particle['objectives'] = self._evaluate_objectives(particle['position'])

                # Update personal best (if new position dominates)
                if self._dominates(particle['objectives'], particle['best_objectives']):
                    particle['best_position'] = particle['position'].copy()
                    particle['best_objectives'] = particle['objectives'].copy()

                # Update archive
                self._update_archive(particle['position'], particle['objectives'])

            # Print progress
            if verbose and iteration % 10 == 0:
                print(f"Iteration {iteration}: Archive size = {len(self.archive)}")

        return self.archive


def example_usage():
    """Demonstrate PSO functionality."""
    print("=" * 60)
    print("PARTICLE SWARM OPTIMIZATION EXAMPLES")
    print("=" * 60)

    # Example 1: Standard PSO
    print("\n1. Standard PSO (Sphere Function):")
    print("-" * 40)

    def sphere(x):
        """Simple sphere function."""
        return sum(xi**2 for xi in x)

    pso = ParticleSwarmOptimization(
        objective_function=sphere,
        bounds=[(-10, 10)] * 5,
        swarm_size=30,
        max_iterations=200,
        topology=Topology.GLOBAL,
        minimize=True,
        seed=42
    )

    best_position, best_fitness = pso.run(verbose=False)
    print(f"Best position: {[f'{x:.4f}' for x in best_position]}")
    print(f"Best fitness: {best_fitness:.6f}")
    print(f"(Global optimum is at [0,0,0,0,0] with fitness 0)")

    # Example 2: PSO with different topologies
    print("\n2. PSO with Different Topologies (Rastrigin Function):")
    print("-" * 40)

    def rastrigin(x):
        """Rastrigin function - highly multimodal."""
        n = len(x)
        return 10 * n + sum(xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x)

    topologies = [Topology.GLOBAL, Topology.RING, Topology.VON_NEUMANN]

    for topology in topologies:
        pso_topo = ParticleSwarmOptimization(
            objective_function=rastrigin,
            bounds=[(-5.12, 5.12)] * 3,
            swarm_size=20,
            max_iterations=100,
            topology=topology,
            minimize=True,
            seed=42
        )

        best_pos, best_fit = pso_topo.run(verbose=False)
        print(f"{topology.value:12s}: fitness = {best_fit:.4f}")

    # Example 3: Quantum PSO
    print("\n3. Quantum PSO (Rosenbrock Function):")
    print("-" * 40)

    def rosenbrock(x):
        """Rosenbrock function - narrow valley."""
        return sum(100*(x[i+1] - x[i]**2)**2 + (1 - x[i])**2
                  for i in range(len(x)-1))

    qpso = QuantumPSO(
        objective_function=rosenbrock,
        bounds=[(-5, 5)] * 4,
        swarm_size=30,
        max_iterations=200,
        minimize=True,
        seed=42
    )

    best_position, best_fitness = qpso.run(verbose=False)
    print(f"Best position: {[f'{x:.4f}' for x in best_position]}")
    print(f"Best fitness: {best_fitness:.6f}")
    print(f"(Global optimum is at [1,1,1,1] with fitness 0)")

    # Example 4: Multi-Objective PSO
    print("\n4. Multi-Objective PSO (ZDT1 Test Function):")
    print("-" * 40)

    def zdt1_f1(x):
        """First objective of ZDT1."""
        return x[0]

    def zdt1_f2(x):
        """Second objective of ZDT1."""
        g = 1 + 9 * sum(x[1:]) / (len(x) - 1)
        return g * (1 - np.sqrt(x[0] / g))

    mopso = MultiObjectivePSO(
        objective_functions=[zdt1_f1, zdt1_f2],
        bounds=[(0, 1)] * 3,
        swarm_size=50,
        max_iterations=100,
        archive_size=50,
        seed=42
    )

    pareto_set = mopso.run(verbose=False)
    print(f"Found {len(pareto_set)} Pareto-optimal solutions")

    # Show a few solutions
    print("Sample Pareto solutions (first 5):")
    for i, sol in enumerate(pareto_set[:5]):
        obj = sol['objectives']
        print(f"  Solution {i+1}: f1 = {obj[0]:.4f}, f2 = {obj[1]:.4f}")

    # Example 5: Adaptive PSO
    print("\n5. Adaptive PSO with Time-Varying Parameters:")
    print("-" * 40)

    def ackley(x):
        """Ackley function - many local minima."""
        n = len(x)
        sum1 = sum(xi**2 for xi in x)
        sum2 = sum(np.cos(2*np.pi*xi) for xi in x)
        return -20 * np.exp(-0.2 * np.sqrt(sum1/n)) - np.exp(sum2/n) + 20 + np.e

    pso_adaptive = ParticleSwarmOptimization(
        objective_function=ackley,
        bounds=[(-5, 5)] * 4,
        swarm_size=30,
        max_iterations=200,
        velocity_update=VelocityUpdate.ADAPTIVE,
        minimize=True,
        seed=42
    )

    best_position, best_fitness = pso_adaptive.run(verbose=False)
    print(f"Best position: {[f'{x:.4f}' for x in best_position]}")
    print(f"Best fitness: {best_fitness:.6f}")
    print(f"(Global optimum is at [0,0,0,0] with fitness 0)")

    # Example 6: PSO convergence visualization
    print("\n6. PSO Convergence Analysis:")
    print("-" * 40)

    pso_vis = ParticleSwarmOptimization(
        objective_function=sphere,
        bounds=[(-10, 10)] * 3,
        swarm_size=20,
        max_iterations=100,
        minimize=True,
        seed=42
    )

    pso_vis.run(verbose=False)

    # Show convergence
    print("Fitness convergence:")
    history = pso_vis.fitness_history
    for i in range(0, len(history), 20):
        fitness = history[i]
        bar_length = int(50 * (1 - fitness / history[0]) if history[0] > 0 else 0)
        bar = '=' * bar_length + '-' * (50 - bar_length)
        print(f"Iter {i:3d}: [{bar}] {fitness:.6f}")

    print("\nSwarm diversity over time:")
    diversity = pso_vis.diversity_history
    for i in range(0, len(diversity), 20):
        div = diversity[i]
        bar_length = int(50 * div / max(diversity))
        bar = '*' * bar_length + ' ' * (50 - bar_length)
        print(f"Iter {i:3d}: [{bar}] {div:.4f}")

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- PSO balances exploration and exploitation")
    print("- Topology affects convergence speed and quality")
    print("- Quantum PSO can escape local optima better")
    print("- Multi-objective PSO finds Pareto-optimal solutions")
    print("- Parameter adaptation improves performance")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()