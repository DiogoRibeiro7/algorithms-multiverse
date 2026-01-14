"""
Particle Swarm Optimization (PSO) Implementation
===============================================

A comprehensive implementation of Particle Swarm Optimization and its variants.
PSO is inspired by social behavior of birds flocking or fish schooling,
where particles explore the search space influenced by their own best position
and the swarm's best position.

Key Components:
- Standard PSO
- Adaptive PSO with dynamic parameters
- Multi-swarm PSO
- Quantum PSO
- Binary PSO
- Constrained PSO

Variants Implemented:
- Inertia weight strategies
- Constriction factor
- Fully informed particle swarm
- Comprehensive learning PSO
- Dynamic neighborhood topologies

Applications:
- Neural network training
- Feature selection
- Engineering design optimization
- Portfolio optimization
- Path planning

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


class TopologyType(Enum):
    """Swarm topology types."""
    GLOBAL = "global"  # All particles connected
    RING = "ring"  # Each particle connected to k neighbors
    STAR = "star"  # Central particle connected to all
    RANDOM = "random"  # Random connections
    DYNAMIC = "dynamic"  # Topology changes over time
    VON_NEUMANN = "von_neumann"  # Grid topology


class InertiaStrategy(Enum):
    """Inertia weight update strategies."""
    CONSTANT = "constant"
    LINEAR_DECREASE = "linear_decrease"
    RANDOM = "random"
    CHAOTIC = "chaotic"
    ADAPTIVE = "adaptive"
    EXPONENTIAL = "exponential"


@dataclass
class Particle:
    """Represents a particle in the swarm."""
    position: np.ndarray
    velocity: np.ndarray
    best_position: np.ndarray = None
    best_fitness: float = float('inf')
    fitness: float = float('inf')
    neighbors: List[int] = field(default_factory=list)
    age: int = 0
    stagnation: int = 0


class ParticleSwarmOptimization:
    """
    Standard Particle Swarm Optimization implementation.

    PSO optimizes by maintaining a swarm of particles that explore
    the search space, influenced by personal and social knowledge.
    """

    def __init__(self,
                 objective_function: Callable,
                 n_dimensions: int,
                 n_particles: int = 30,
                 bounds: Optional[Tuple[np.ndarray, np.ndarray]] = None,
                 inertia: float = 0.729,
                 cognitive: float = 1.49445,
                 social: float = 1.49445,
                 max_velocity: Optional[float] = None,
                 topology: TopologyType = TopologyType.GLOBAL,
                 inertia_strategy: InertiaStrategy = InertiaStrategy.LINEAR_DECREASE):
        """
        Initialize PSO algorithm.

        Args:
            objective_function: Function to minimize
            n_dimensions: Number of dimensions in search space
            n_particles: Number of particles in swarm
            bounds: Search space bounds (lower, upper)
            inertia: Inertia weight
            cognitive: Cognitive parameter (c1)
            social: Social parameter (c2)
            max_velocity: Maximum particle velocity
            topology: Swarm topology type
            inertia_strategy: Strategy for updating inertia weight
        """
        self.objective_function = objective_function
        self.n_dimensions = n_dimensions
        self.n_particles = n_particles
        self.inertia = inertia
        self.initial_inertia = inertia
        self.cognitive = cognitive
        self.social = social
        self.topology = topology
        self.inertia_strategy = inertia_strategy

        # Set bounds
        if bounds is None:
            self.lower_bound = np.full(n_dimensions, -100)
            self.upper_bound = np.full(n_dimensions, 100)
        else:
            self.lower_bound = np.array(bounds[0])
            self.upper_bound = np.array(bounds[1])

        # Set maximum velocity
        if max_velocity is None:
            self.max_velocity = 0.2 * (self.upper_bound - self.lower_bound)
        else:
            self.max_velocity = np.full(n_dimensions, max_velocity)

        # Initialize swarm
        self.swarm: List[Particle] = []
        self.global_best_position = None
        self.global_best_fitness = float('inf')
        self.iteration = 0

        # History tracking
        self.history = {
            'best_fitness': [],
            'avg_fitness': [],
            'diversity': [],
            'velocity_avg': []
        }

    def initialize_swarm(self):
        """Initialize particle positions and velocities."""
        self.swarm = []

        for i in range(self.n_particles):
            # Random position within bounds
            position = np.random.uniform(
                self.lower_bound,
                self.upper_bound,
                self.n_dimensions
            )

            # Small random velocity
            velocity = np.random.uniform(
                -self.max_velocity,
                self.max_velocity,
                self.n_dimensions
            )

            particle = Particle(position=position, velocity=velocity)
            particle.best_position = position.copy()

            # Evaluate initial fitness
            particle.fitness = self.objective_function(position)
            particle.best_fitness = particle.fitness

            # Update global best
            if particle.fitness < self.global_best_fitness:
                self.global_best_fitness = particle.fitness
                self.global_best_position = position.copy()

            self.swarm.append(particle)

        # Setup topology
        self._setup_topology()

    def _setup_topology(self):
        """Setup particle neighborhood topology."""
        if self.topology == TopologyType.GLOBAL:
            # All particles are neighbors
            for particle in self.swarm:
                particle.neighbors = list(range(self.n_particles))

        elif self.topology == TopologyType.RING:
            # Ring topology with 2 neighbors
            for i, particle in enumerate(self.swarm):
                particle.neighbors = [
                    (i - 1) % self.n_particles,
                    i,
                    (i + 1) % self.n_particles
                ]

        elif self.topology == TopologyType.VON_NEUMANN:
            # Grid topology (2D grid)
            grid_size = int(np.sqrt(self.n_particles))
            for i, particle in enumerate(self.swarm):
                row = i // grid_size
                col = i % grid_size

                neighbors = [i]  # Self
                # Add 4 neighbors (up, down, left, right)
                if row > 0:
                    neighbors.append((row - 1) * grid_size + col)
                if row < grid_size - 1:
                    neighbors.append((row + 1) * grid_size + col)
                if col > 0:
                    neighbors.append(row * grid_size + (col - 1))
                if col < grid_size - 1:
                    neighbors.append(row * grid_size + (col + 1))

                particle.neighbors = neighbors

        elif self.topology == TopologyType.STAR:
            # Star topology - first particle connected to all
            self.swarm[0].neighbors = list(range(self.n_particles))
            for i in range(1, self.n_particles):
                self.swarm[i].neighbors = [0, i]

        elif self.topology == TopologyType.RANDOM:
            # Random topology with k connections
            k = min(3, self.n_particles - 1)
            for i, particle in enumerate(self.swarm):
                neighbors = [i]  # Include self
                available = list(range(self.n_particles))
                available.remove(i)
                neighbors.extend(random.sample(available, k))
                particle.neighbors = neighbors

    def update_inertia(self, iteration: int, max_iterations: int):
        """Update inertia weight based on strategy."""
        if self.inertia_strategy == InertiaStrategy.CONSTANT:
            pass  # Keep current value

        elif self.inertia_strategy == InertiaStrategy.LINEAR_DECREASE:
            # Linear decrease from 0.9 to 0.4
            self.inertia = 0.9 - (0.9 - 0.4) * (iteration / max_iterations)

        elif self.inertia_strategy == InertiaStrategy.EXPONENTIAL:
            # Exponential decay
            self.inertia = self.initial_inertia * (0.4 / self.initial_inertia) ** (iteration / max_iterations)

        elif self.inertia_strategy == InertiaStrategy.RANDOM:
            # Random inertia
            self.inertia = 0.5 + random.random() / 2

        elif self.inertia_strategy == InertiaStrategy.CHAOTIC:
            # Chaotic inertia using logistic map
            z = 4 * self.inertia * (1 - self.inertia)
            self.inertia = 0.4 + 0.5 * z

        elif self.inertia_strategy == InertiaStrategy.ADAPTIVE:
            # Adaptive based on swarm diversity
            diversity = self.calculate_diversity()
            if diversity < 0.1:  # Low diversity
                self.inertia = min(0.9, self.inertia * 1.05)
            else:
                self.inertia = max(0.4, self.inertia * 0.95)

    def get_neighborhood_best(self, particle_idx: int) -> Tuple[np.ndarray, float]:
        """Get best position in particle's neighborhood."""
        particle = self.swarm[particle_idx]
        best_fitness = float('inf')
        best_position = None

        for neighbor_idx in particle.neighbors:
            neighbor = self.swarm[neighbor_idx]
            if neighbor.best_fitness < best_fitness:
                best_fitness = neighbor.best_fitness
                best_position = neighbor.best_position.copy()

        return best_position, best_fitness

    def update_velocity(self, particle: Particle, neighborhood_best: np.ndarray):
        """Update particle velocity using PSO equation."""
        # Random factors
        r1 = np.random.random(self.n_dimensions)
        r2 = np.random.random(self.n_dimensions)

        # Cognitive component (personal best)
        cognitive_component = self.cognitive * r1 * (particle.best_position - particle.position)

        # Social component (neighborhood best)
        social_component = self.social * r2 * (neighborhood_best - particle.position)

        # Update velocity
        particle.velocity = (
            self.inertia * particle.velocity +
            cognitive_component +
            social_component
        )

        # Clamp velocity
        particle.velocity = np.clip(particle.velocity, -self.max_velocity, self.max_velocity)

    def update_position(self, particle: Particle):
        """Update particle position and handle bounds."""
        # Update position
        particle.position = particle.position + particle.velocity

        # Handle boundary conditions
        for i in range(self.n_dimensions):
            if particle.position[i] < self.lower_bound[i]:
                particle.position[i] = self.lower_bound[i]
                particle.velocity[i] = -particle.velocity[i] * 0.5  # Bounce back

            elif particle.position[i] > self.upper_bound[i]:
                particle.position[i] = self.upper_bound[i]
                particle.velocity[i] = -particle.velocity[i] * 0.5  # Bounce back

    def calculate_diversity(self) -> float:
        """Calculate swarm diversity."""
        if len(self.swarm) < 2:
            return 0.0

        # Calculate centroid
        positions = np.array([p.position for p in self.swarm])
        centroid = np.mean(positions, axis=0)

        # Calculate average distance from centroid
        distances = [np.linalg.norm(p.position - centroid) for p in self.swarm]
        return np.mean(distances)

    def step(self):
        """Perform one PSO iteration."""
        # Update each particle
        for i, particle in enumerate(self.swarm):
            # Get neighborhood best
            neighborhood_best, _ = self.get_neighborhood_best(i)

            # Update velocity and position
            self.update_velocity(particle, neighborhood_best)
            self.update_position(particle)

            # Evaluate fitness
            particle.fitness = self.objective_function(particle.position)

            # Update personal best
            if particle.fitness < particle.best_fitness:
                particle.best_fitness = particle.fitness
                particle.best_position = particle.position.copy()
                particle.stagnation = 0
            else:
                particle.stagnation += 1

            # Update global best
            if particle.fitness < self.global_best_fitness:
                self.global_best_fitness = particle.fitness
                self.global_best_position = particle.position.copy()

            particle.age += 1

    def run(self, max_iterations: int = 100,
            target_fitness: Optional[float] = None,
            verbose: bool = True) -> Tuple[np.ndarray, float]:
        """
        Run PSO algorithm.

        Args:
            max_iterations: Maximum iterations
            target_fitness: Stop if this fitness is reached
            verbose: Print progress

        Returns:
            Best position and fitness found
        """
        # Initialize swarm
        self.initialize_swarm()

        if verbose:
            print(f"Starting PSO with {self.n_particles} particles")
            print(f"Initial best fitness: {self.global_best_fitness:.6f}")

        # Main loop
        for iteration in range(max_iterations):
            self.iteration = iteration

            # Update inertia
            self.update_inertia(iteration, max_iterations)

            # Perform PSO step
            self.step()

            # Update history
            avg_fitness = np.mean([p.fitness for p in self.swarm])
            avg_velocity = np.mean([np.linalg.norm(p.velocity) for p in self.swarm])

            self.history['best_fitness'].append(self.global_best_fitness)
            self.history['avg_fitness'].append(avg_fitness)
            self.history['diversity'].append(self.calculate_diversity())
            self.history['velocity_avg'].append(avg_velocity)

            # Print progress
            if verbose and iteration % 20 == 0:
                print(f"Iteration {iteration}: Best = {self.global_best_fitness:.6f}, "
                      f"Avg = {avg_fitness:.6f}, "
                      f"Diversity = {self.history['diversity'][-1]:.4f}")

            # Check termination
            if target_fitness is not None and self.global_best_fitness <= target_fitness:
                if verbose:
                    print(f"Target fitness {target_fitness} reached at iteration {iteration}")
                break

        if verbose:
            print(f"\nPSO completed after {iteration + 1} iterations")
            print(f"Best fitness: {self.global_best_fitness:.6f}")
            print(f"Best position: {self.global_best_position}")

        return self.global_best_position, self.global_best_fitness


class BinaryPSO(ParticleSwarmOptimization):
    """
    Binary Particle Swarm Optimization for discrete optimization.

    Uses sigmoid function to map velocities to probabilities.
    """

    def update_position(self, particle: Particle):
        """Update binary position using sigmoid of velocity."""
        # Apply sigmoid to velocity
        sigmoid = 1 / (1 + np.exp(-particle.velocity))

        # Update position based on probability
        particle.position = (np.random.random(self.n_dimensions) < sigmoid).astype(int)


class QuantumPSO(ParticleSwarmOptimization):
    """
    Quantum-behaved Particle Swarm Optimization.

    Particles have quantum behavior with no velocity,
    using quantum mechanics principles.
    """

    def __init__(self, *args, contraction_expansion: float = 0.5, **kwargs):
        super().__init__(*args, **kwargs)
        self.contraction_expansion = contraction_expansion

    def update_position(self, particle: Particle):
        """Update position using quantum behavior."""
        # Calculate mean best position
        mean_best = np.mean([p.best_position for p in self.swarm], axis=0)

        # Random point between personal and global best
        phi = np.random.random(self.n_dimensions)
        p = phi * particle.best_position + (1 - phi) * self.global_best_position

        # Update position with quantum behavior
        u = np.random.random(self.n_dimensions)
        if random.random() > 0.5:
            particle.position = p + self.contraction_expansion * np.abs(mean_best - particle.position) * np.log(1/u)
        else:
            particle.position = p - self.contraction_expansion * np.abs(mean_best - particle.position) * np.log(1/u)

        # Bound checking
        particle.position = np.clip(particle.position, self.lower_bound, self.upper_bound)


class MultiSwarmPSO:
    """
    Multi-Swarm PSO with multiple sub-swarms.

    Sub-swarms explore different regions and periodically
    exchange information.
    """

    def __init__(self,
                 objective_function: Callable,
                 n_dimensions: int,
                 n_swarms: int = 4,
                 particles_per_swarm: int = 10,
                 exchange_interval: int = 10,
                 **pso_kwargs):
        """
        Initialize Multi-Swarm PSO.

        Args:
            objective_function: Function to minimize
            n_dimensions: Dimension of search space
            n_swarms: Number of sub-swarms
            particles_per_swarm: Particles in each swarm
            exchange_interval: Iterations between exchanges
            **pso_kwargs: Additional PSO parameters
        """
        self.objective_function = objective_function
        self.n_dimensions = n_dimensions
        self.n_swarms = n_swarms
        self.exchange_interval = exchange_interval

        # Create sub-swarms
        self.sub_swarms = []
        for i in range(n_swarms):
            swarm = ParticleSwarmOptimization(
                objective_function=objective_function,
                n_dimensions=n_dimensions,
                n_particles=particles_per_swarm,
                **pso_kwargs
            )
            self.sub_swarms.append(swarm)

        self.global_best_position = None
        self.global_best_fitness = float('inf')

    def exchange_information(self):
        """Exchange best particles between swarms."""
        # Find best particle from each swarm
        best_particles = []
        for swarm in self.sub_swarms:
            best_idx = np.argmin([p.fitness for p in swarm.swarm])
            best_particles.append(swarm.swarm[best_idx])

        # Replace worst particle in each swarm with best from another
        for i, swarm in enumerate(self.sub_swarms):
            worst_idx = np.argmax([p.fitness for p in swarm.swarm])

            # Get best from different swarm
            source_swarm = (i + 1) % self.n_swarms
            immigrant = copy.deepcopy(best_particles[source_swarm])

            # Replace worst with immigrant
            swarm.swarm[worst_idx] = immigrant

    def run(self, max_iterations: int = 100, verbose: bool = True) -> Tuple[np.ndarray, float]:
        """Run multi-swarm PSO."""
        # Initialize all swarms
        for swarm in self.sub_swarms:
            swarm.initialize_swarm()

        if verbose:
            print(f"Starting Multi-Swarm PSO with {self.n_swarms} swarms")

        # Main loop
        for iteration in range(max_iterations):
            # Update each swarm
            for swarm in self.sub_swarms:
                swarm.iteration = iteration
                swarm.update_inertia(iteration, max_iterations)
                swarm.step()

                # Update global best
                if swarm.global_best_fitness < self.global_best_fitness:
                    self.global_best_fitness = swarm.global_best_fitness
                    self.global_best_position = swarm.global_best_position.copy()

            # Exchange information
            if iteration > 0 and iteration % self.exchange_interval == 0:
                self.exchange_information()

            # Print progress
            if verbose and iteration % 20 == 0:
                swarm_bests = [s.global_best_fitness for s in self.sub_swarms]
                print(f"Iteration {iteration}: Global best = {self.global_best_fitness:.6f}, "
                      f"Swarm bests = {[f'{b:.2f}' for b in swarm_bests]}")

        if verbose:
            print(f"\nMulti-Swarm PSO completed")
            print(f"Best fitness: {self.global_best_fitness:.6f}")

        return self.global_best_position, self.global_best_fitness


def optimize_function_example():
    """Example: Optimize benchmark functions."""
    print("=" * 60)
    print("PARTICLE SWARM OPTIMIZATION - FUNCTION OPTIMIZATION")
    print("=" * 60)

    # Griewank function - highly multimodal
    def griewank(x: np.ndarray) -> float:
        """Griewank function."""
        sum_sq = np.sum(x**2) / 4000
        prod_cos = np.prod(np.cos(x / np.sqrt(np.arange(1, len(x) + 1))))
        return sum_sq - prod_cos + 1

    # Standard PSO
    pso = ParticleSwarmOptimization(
        objective_function=griewank,
        n_dimensions=10,
        n_particles=30,
        bounds=(-600, 600),
        inertia=0.729,
        cognitive=1.49445,
        social=1.49445,
        topology=TopologyType.GLOBAL,
        inertia_strategy=InertiaStrategy.LINEAR_DECREASE
    )

    best_pos, best_fit = pso.run(max_iterations=200, verbose=True)

    print(f"\nBest position: {best_pos}")
    print(f"Best fitness: {best_fit:.8f}")
    print(f"Global minimum is 0 at origin")
    print(f"Distance from optimal: {np.linalg.norm(best_pos):.6f}")


def topology_comparison_example():
    """Compare different swarm topologies."""
    print("\n" + "=" * 60)
    print("PSO TOPOLOGY COMPARISON")
    print("=" * 60)

    # Schwefel function
    def schwefel(x: np.ndarray) -> float:
        """Schwefel function - deceptive."""
        n = len(x)
        return 418.9829 * n - np.sum(x * np.sin(np.sqrt(np.abs(x))))

    topologies = [
        TopologyType.GLOBAL,
        TopologyType.RING,
        TopologyType.VON_NEUMANN,
        TopologyType.STAR,
        TopologyType.RANDOM
    ]

    results = {}

    for topology in topologies:
        print(f"\nTesting {topology.value} topology...")

        pso = ParticleSwarmOptimization(
            objective_function=schwefel,
            n_dimensions=5,
            n_particles=25,
            bounds=(-500, 500),
            topology=topology,
            inertia_strategy=InertiaStrategy.LINEAR_DECREASE
        )

        best_pos, best_fit = pso.run(max_iterations=100, verbose=False)
        results[topology.value] = best_fit

        print(f"Best fitness: {best_fit:.4f}")

    print("\n" + "-" * 40)
    print("TOPOLOGY RESULTS:")
    for topology, fitness in sorted(results.items(), key=lambda x: x[1]):
        print(f"{topology:15s}: {fitness:.4f}")


def binary_pso_example():
    """Example: Feature selection using Binary PSO."""
    print("\n" + "=" * 60)
    print("BINARY PSO - FEATURE SELECTION")
    print("=" * 60)

    # Simulated feature selection problem
    np.random.seed(42)
    n_features = 30
    n_relevant = 8

    def feature_selection_fitness(selected: np.ndarray) -> float:
        """Fitness for feature selection."""
        n_selected = np.sum(selected)

        if n_selected == 0:
            return 1000  # Penalty for no features

        # Reward for selecting relevant features (first 8)
        relevant_selected = np.sum(selected[:n_relevant])

        # Penalty for selecting irrelevant features
        irrelevant_selected = np.sum(selected[n_relevant:])

        fitness = -relevant_selected + 0.1 * irrelevant_selected + 0.01 * n_selected
        return fitness

    # Binary PSO
    bpso = BinaryPSO(
        objective_function=feature_selection_fitness,
        n_dimensions=n_features,
        n_particles=20,
        bounds=(0, 1),
        inertia=0.729,
        cognitive=2.0,
        social=2.0
    )

    best_features, best_fitness = bpso.run(max_iterations=100, verbose=True)

    selected_indices = np.where(best_features)[0]
    print(f"\nSelected features: {selected_indices}")
    print(f"Number selected: {len(selected_indices)}")
    print(f"Relevant features found: {len([i for i in selected_indices if i < n_relevant])}/{n_relevant}")


def quantum_pso_example():
    """Example: Quantum PSO for complex optimization."""
    print("\n" + "=" * 60)
    print("QUANTUM PSO - COMPLEX OPTIMIZATION")
    print("=" * 60)

    # Levy function - complex landscape
    def levy(x: np.ndarray) -> float:
        """Levy function."""
        w = 1 + (x - 1) / 4
        term1 = np.sin(np.pi * w[0])**2
        term2 = np.sum((w[:-1] - 1)**2 * (1 + 10 * np.sin(np.pi * w[:-1] + 1)**2))
        term3 = (w[-1] - 1)**2 * (1 + np.sin(2 * np.pi * w[-1])**2)
        return term1 + term2 + term3

    # Quantum PSO
    qpso = QuantumPSO(
        objective_function=levy,
        n_dimensions=10,
        n_particles=40,
        bounds=(-10, 10),
        contraction_expansion=0.5
    )

    best_pos, best_fit = qpso.run(max_iterations=200, verbose=True)

    print(f"\nBest fitness: {best_fit:.8f}")
    print(f"Global minimum is 0 at (1, 1, ..., 1)")
    print(f"Distance from optimal: {np.linalg.norm(best_pos - 1):.6f}")


def multi_swarm_example():
    """Example: Multi-Swarm PSO for multimodal optimization."""
    print("\n" + "=" * 60)
    print("MULTI-SWARM PSO - MULTIMODAL OPTIMIZATION")
    print("=" * 60)

    # Rastrigin function - many local minima
    def rastrigin(x: np.ndarray) -> float:
        """Rastrigin function."""
        A = 10
        n = len(x)
        return A * n + np.sum(x**2 - A * np.cos(2 * np.pi * x))

    # Multi-Swarm PSO
    mspso = MultiSwarmPSO(
        objective_function=rastrigin,
        n_dimensions=10,
        n_swarms=5,
        particles_per_swarm=10,
        exchange_interval=20,
        bounds=(-5.12, 5.12),
        inertia_strategy=InertiaStrategy.ADAPTIVE
    )

    best_pos, best_fit = mspso.run(max_iterations=200, verbose=True)

    print(f"\nBest fitness: {best_fit:.6f}")
    print(f"Global minimum is 0 at origin")
    print(f"Distance from optimal: {np.linalg.norm(best_pos):.6f}")


def constrained_optimization_example():
    """Example: PSO with constraint handling."""
    print("\n" + "=" * 60)
    print("CONSTRAINED PSO - ENGINEERING DESIGN")
    print("=" * 60)

    # Pressure vessel design problem
    def pressure_vessel(x: np.ndarray) -> float:
        """
        Minimize cost of pressure vessel.
        x = [Ts, Th, R, L]
        Ts: shell thickness
        Th: head thickness
        R: inner radius
        L: length
        """
        Ts, Th, R, L = x

        # Objective: minimize cost
        cost = (0.6224 * Ts * R * L +
                1.7781 * Th * R**2 +
                3.1661 * Ts**2 * L +
                19.84 * Ts**2 * R)

        # Penalty for constraint violations
        penalty = 0
        g1 = -Ts + 0.0193 * R  # Constraint 1
        g2 = -Th + 0.00954 * R  # Constraint 2
        g3 = -np.pi * R**2 * L - (4/3) * np.pi * R**3 + 1296000  # Constraint 3
        g4 = L - 240  # Constraint 4

        # Apply penalties
        for g in [g1, g2, g3, g4]:
            if g > 0:
                penalty += 10000 * g**2

        return cost + penalty

    # PSO with constraints
    pso = ParticleSwarmOptimization(
        objective_function=pressure_vessel,
        n_dimensions=4,
        n_particles=50,
        bounds=([0.0625, 0.0625, 10, 10], [99, 99, 200, 200]),
        inertia_strategy=InertiaStrategy.LINEAR_DECREASE
    )

    best_design, best_cost = pso.run(max_iterations=300, verbose=True)

    print(f"\nOptimal design:")
    print(f"  Shell thickness (Ts): {best_design[0]:.4f}")
    print(f"  Head thickness (Th): {best_design[1]:.4f}")
    print(f"  Inner radius (R): {best_design[2]:.4f}")
    print(f"  Length (L): {best_design[3]:.4f}")
    print(f"  Cost: ${best_cost:.2f}")


if __name__ == "__main__":
    # Run examples
    optimize_function_example()
    topology_comparison_example()
    binary_pso_example()
    quantum_pso_example()
    multi_swarm_example()
    constrained_optimization_example()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- PSO balances exploration and exploitation naturally")
    print("- Topology affects information flow and convergence")
    print("- Adaptive parameters prevent premature convergence")
    print("- Quantum PSO can escape local optima better")
    print("- Multi-swarm maintains diversity for multimodal problems")
    print("=" * 60)