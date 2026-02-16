"""
Genetic Algorithm Implementation
================================

A comprehensive implementation of Genetic Algorithms (GA) for optimization problems.
Genetic algorithms are inspired by natural selection and evolution to find optimal
or near-optimal solutions to complex problems.

Key Components:
- Population initialization
- Fitness evaluation
- Selection methods (tournament, roulette wheel, rank-based)
- Crossover operations (single-point, two-point, uniform)
- Mutation strategies
- Elitism

Applications:
- Function optimization
- Feature selection
- Neural network training
- Scheduling problems
- TSP and routing

Author: Claude
Date: January 2026
"""

import random
import numpy as np
from typing import List, Tuple, Callable, Optional, Any, Dict
from dataclasses import dataclass
from abc import ABC, abstractmethod
import math
from enum import Enum


class SelectionMethod(Enum):
    """Selection methods for choosing parents."""
    TOURNAMENT = "tournament"
    ROULETTE_WHEEL = "roulette_wheel"
    RANK_BASED = "rank_based"
    STOCHASTIC_UNIVERSAL = "stochastic_universal"
    TRUNCATION = "truncation"


class CrossoverMethod(Enum):
    """Crossover methods for creating offspring."""
    SINGLE_POINT = "single_point"
    TWO_POINT = "two_point"
    UNIFORM = "uniform"
    ARITHMETIC = "arithmetic"
    ORDER = "order"  # For permutation problems


class MutationMethod(Enum):
    """Mutation methods for introducing variation."""
    BIT_FLIP = "bit_flip"
    GAUSSIAN = "gaussian"
    SWAP = "swap"
    INVERSION = "inversion"
    SCRAMBLE = "scramble"


@dataclass
class Individual:
    """Represents an individual in the population."""
    genes: np.ndarray
    fitness: float = -float('inf')
    age: int = 0


class GeneticAlgorithm:
    """
    Main Genetic Algorithm implementation.

    This is a flexible GA that can be customized for various optimization problems.
    """

    def __init__(self,
                 fitness_function: Callable,
                 gene_length: int,
                 population_size: int = 100,
                 mutation_rate: float = 0.01,
                 crossover_rate: float = 0.8,
                 elitism_count: int = 2,
                 selection_method: SelectionMethod = SelectionMethod.TOURNAMENT,
                 crossover_method: CrossoverMethod = CrossoverMethod.SINGLE_POINT,
                 mutation_method: MutationMethod = MutationMethod.BIT_FLIP,
                 gene_type: str = 'binary',  # 'binary', 'real', 'permutation'
                 gene_bounds: Optional[Tuple[float, float]] = None):
        """
        Initialize Genetic Algorithm.

        Args:
            fitness_function: Function to evaluate fitness of individuals
            gene_length: Length of gene sequence
            population_size: Number of individuals in population
            mutation_rate: Probability of mutation per gene
            crossover_rate: Probability of crossover
            elitism_count: Number of best individuals to preserve
            selection_method: Method for selecting parents
            crossover_method: Method for crossover
            mutation_method: Method for mutation
            gene_type: Type of genes (binary, real, permutation)
            gene_bounds: Bounds for real-valued genes (min, max)
        """
        self.fitness_function = fitness_function
        self.gene_length = gene_length
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count
        self.selection_method = selection_method
        self.crossover_method = crossover_method
        self.mutation_method = mutation_method
        self.gene_type = gene_type
        self.gene_bounds = gene_bounds or (0, 1)

        self.population: List[Individual] = []
        self.generation = 0
        self.best_individual: Optional[Individual] = None
        self.history = {
            'best_fitness': [],
            'avg_fitness': [],
            'diversity': []
        }

    def initialize_population(self):
        """Initialize random population."""
        self.population = []

        for _ in range(self.population_size):
            if self.gene_type == 'binary':
                genes = np.random.randint(0, 2, self.gene_length)
            elif self.gene_type == 'real':
                genes = np.random.uniform(
                    self.gene_bounds[0],
                    self.gene_bounds[1],
                    self.gene_length
                )
            elif self.gene_type == 'permutation':
                genes = np.random.permutation(self.gene_length)
            else:
                raise ValueError(f"Unknown gene type: {self.gene_type}")

            individual = Individual(genes=genes)
            self.population.append(individual)

        # Evaluate initial population
        self.evaluate_population()

    def evaluate_population(self):
        """Evaluate fitness of all individuals."""
        for individual in self.population:
            if individual.fitness == -float('inf'):
                individual.fitness = self.fitness_function(individual.genes)

        # Sort population by fitness (descending)
        self.population.sort(key=lambda x: x.fitness, reverse=True)

        # Update best individual
        if self.best_individual is None or self.population[0].fitness > self.best_individual.fitness:
            self.best_individual = Individual(
                genes=self.population[0].genes.copy(),
                fitness=self.population[0].fitness
            )

    def select_parents(self) -> Tuple[Individual, Individual]:
        """Select two parents for reproduction."""
        if self.selection_method == SelectionMethod.TOURNAMENT:
            return self.tournament_selection(), self.tournament_selection()
        elif self.selection_method == SelectionMethod.ROULETTE_WHEEL:
            return self.roulette_wheel_selection(), self.roulette_wheel_selection()
        elif self.selection_method == SelectionMethod.RANK_BASED:
            return self.rank_based_selection(), self.rank_based_selection()
        elif self.selection_method == SelectionMethod.STOCHASTIC_UNIVERSAL:
            parents = self.stochastic_universal_sampling(2)
            return parents[0], parents[1]
        else:
            return self.truncation_selection(), self.truncation_selection()

    def tournament_selection(self, tournament_size: int = 3) -> Individual:
        """Tournament selection."""
        tournament = random.sample(self.population, tournament_size)
        return max(tournament, key=lambda x: x.fitness)

    def roulette_wheel_selection(self) -> Individual:
        """Roulette wheel selection (fitness proportionate)."""
        # Shift fitness to ensure all positive values
        min_fitness = min(ind.fitness for ind in self.population)
        if min_fitness < 0:
            fitness_values = [ind.fitness - min_fitness + 1 for ind in self.population]
        else:
            fitness_values = [ind.fitness + 1 for ind in self.population]

        total_fitness = sum(fitness_values)
        probabilities = [f / total_fitness for f in fitness_values]

        # Select based on cumulative probabilities
        r = random.random()
        cumsum = 0
        for i, prob in enumerate(probabilities):
            cumsum += prob
            if r <= cumsum:
                return self.population[i]

        return self.population[-1]

    def rank_based_selection(self) -> Individual:
        """Rank-based selection."""
        n = len(self.population)
        # Linear ranking: probability proportional to rank
        ranks = list(range(n, 0, -1))
        total_rank = sum(ranks)
        probabilities = [r / total_rank for r in ranks]

        r = random.random()
        cumsum = 0
        for i, prob in enumerate(probabilities):
            cumsum += prob
            if r <= cumsum:
                return self.population[i]

        return self.population[-1]

    def stochastic_universal_sampling(self, num_parents: int) -> List[Individual]:
        """Stochastic universal sampling for multiple selections."""
        # Calculate selection probabilities
        min_fitness = min(ind.fitness for ind in self.population)
        if min_fitness < 0:
            fitness_values = [ind.fitness - min_fitness + 1 for ind in self.population]
        else:
            fitness_values = [ind.fitness + 1 for ind in self.population]

        total_fitness = sum(fitness_values)

        # Calculate selection points
        pointer_distance = total_fitness / num_parents
        start_point = random.uniform(0, pointer_distance)
        points = [start_point + i * pointer_distance for i in range(num_parents)]

        # Select individuals
        selected = []
        cumsum = 0
        j = 0
        for i, fitness in enumerate(fitness_values):
            cumsum += fitness
            while j < len(points) and points[j] <= cumsum:
                selected.append(self.population[i])
                j += 1

        return selected

    def truncation_selection(self, top_percent: float = 0.5) -> Individual:
        """Truncation selection - select from top percentage."""
        cutoff = int(len(self.population) * top_percent)
        return random.choice(self.population[:cutoff])

    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Perform crossover between two parents."""
        if random.random() > self.crossover_rate:
            # No crossover, return copies of parents
            return (Individual(genes=parent1.genes.copy()),
                   Individual(genes=parent2.genes.copy()))

        if self.crossover_method == CrossoverMethod.SINGLE_POINT:
            return self.single_point_crossover(parent1, parent2)
        elif self.crossover_method == CrossoverMethod.TWO_POINT:
            return self.two_point_crossover(parent1, parent2)
        elif self.crossover_method == CrossoverMethod.UNIFORM:
            return self.uniform_crossover(parent1, parent2)
        elif self.crossover_method == CrossoverMethod.ARITHMETIC:
            return self.arithmetic_crossover(parent1, parent2)
        else:  # ORDER crossover for permutations
            return self.order_crossover(parent1, parent2)

    def single_point_crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Single-point crossover."""
        point = random.randint(1, self.gene_length - 1)

        child1_genes = np.concatenate([parent1.genes[:point], parent2.genes[point:]])
        child2_genes = np.concatenate([parent2.genes[:point], parent1.genes[point:]])

        return Individual(genes=child1_genes), Individual(genes=child2_genes)

    def two_point_crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Two-point crossover."""
        point1 = random.randint(0, self.gene_length - 2)
        point2 = random.randint(point1 + 1, self.gene_length - 1)

        child1_genes = np.concatenate([
            parent1.genes[:point1],
            parent2.genes[point1:point2],
            parent1.genes[point2:]
        ])
        child2_genes = np.concatenate([
            parent2.genes[:point1],
            parent1.genes[point1:point2],
            parent2.genes[point2:]
        ])

        return Individual(genes=child1_genes), Individual(genes=child2_genes)

    def uniform_crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Uniform crossover."""
        mask = np.random.randint(0, 2, self.gene_length, dtype=bool)

        child1_genes = np.where(mask, parent1.genes, parent2.genes)
        child2_genes = np.where(mask, parent2.genes, parent1.genes)

        return Individual(genes=child1_genes), Individual(genes=child2_genes)

    def arithmetic_crossover(self, parent1: Individual, parent2: Individual, alpha: float = 0.5) -> Tuple[Individual, Individual]:
        """Arithmetic crossover for real-valued genes."""
        child1_genes = alpha * parent1.genes + (1 - alpha) * parent2.genes
        child2_genes = (1 - alpha) * parent1.genes + alpha * parent2.genes

        return Individual(genes=child1_genes), Individual(genes=child2_genes)

    def order_crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Order crossover for permutation problems."""
        size = len(parent1.genes)

        # Select random segment
        start = random.randint(0, size - 2)
        end = random.randint(start + 1, size - 1)

        # Child 1
        child1_genes = np.full(size, -1)
        child1_genes[start:end] = parent1.genes[start:end]

        pointer = end
        for gene in parent2.genes:
            if gene not in child1_genes:
                child1_genes[pointer] = gene
                pointer = (pointer + 1) % size

        # Child 2
        child2_genes = np.full(size, -1)
        child2_genes[start:end] = parent2.genes[start:end]

        pointer = end
        for gene in parent1.genes:
            if gene not in child2_genes:
                child2_genes[pointer] = gene
                pointer = (pointer + 1) % size

        return Individual(genes=child1_genes), Individual(genes=child2_genes)

    def mutate(self, individual: Individual) -> Individual:
        """Apply mutation to an individual."""
        if self.mutation_method == MutationMethod.BIT_FLIP:
            return self.bit_flip_mutation(individual)
        elif self.mutation_method == MutationMethod.GAUSSIAN:
            return self.gaussian_mutation(individual)
        elif self.mutation_method == MutationMethod.SWAP:
            return self.swap_mutation(individual)
        elif self.mutation_method == MutationMethod.INVERSION:
            return self.inversion_mutation(individual)
        else:  # SCRAMBLE
            return self.scramble_mutation(individual)

    def bit_flip_mutation(self, individual: Individual) -> Individual:
        """Bit flip mutation for binary genes."""
        mutated_genes = individual.genes.copy()

        for i in range(self.gene_length):
            if random.random() < self.mutation_rate:
                mutated_genes[i] = 1 - mutated_genes[i]

        return Individual(genes=mutated_genes)

    def gaussian_mutation(self, individual: Individual, sigma: float = 0.1) -> Individual:
        """Gaussian mutation for real-valued genes."""
        mutated_genes = individual.genes.copy()

        for i in range(self.gene_length):
            if random.random() < self.mutation_rate:
                mutated_genes[i] += np.random.normal(0, sigma)
                # Ensure within bounds
                mutated_genes[i] = np.clip(
                    mutated_genes[i],
                    self.gene_bounds[0],
                    self.gene_bounds[1]
                )

        return Individual(genes=mutated_genes)

    def swap_mutation(self, individual: Individual) -> Individual:
        """Swap mutation for permutation problems."""
        mutated_genes = individual.genes.copy()

        if random.random() < self.mutation_rate:
            i, j = random.sample(range(self.gene_length), 2)
            mutated_genes[i], mutated_genes[j] = mutated_genes[j], mutated_genes[i]

        return Individual(genes=mutated_genes)

    def inversion_mutation(self, individual: Individual) -> Individual:
        """Inversion mutation - reverse a segment."""
        mutated_genes = individual.genes.copy()

        if random.random() < self.mutation_rate:
            start = random.randint(0, self.gene_length - 2)
            end = random.randint(start + 1, self.gene_length - 1)
            mutated_genes[start:end+1] = mutated_genes[start:end+1][::-1]

        return Individual(genes=mutated_genes)

    def scramble_mutation(self, individual: Individual) -> Individual:
        """Scramble mutation - randomly shuffle a segment."""
        mutated_genes = individual.genes.copy()

        if random.random() < self.mutation_rate:
            start = random.randint(0, self.gene_length - 2)
            end = random.randint(start + 1, self.gene_length - 1)
            segment = mutated_genes[start:end+1].copy()
            np.random.shuffle(segment)
            mutated_genes[start:end+1] = segment

        return Individual(genes=mutated_genes)

    def calculate_diversity(self) -> float:
        """Calculate population diversity."""
        if len(self.population) < 2:
            return 0.0

        # Calculate pairwise distances
        distances = []
        for i in range(len(self.population)):
            for j in range(i + 1, len(self.population)):
                if self.gene_type == 'binary':
                    # Hamming distance for binary
                    dist = np.sum(self.population[i].genes != self.population[j].genes)
                else:
                    # Euclidean distance for real-valued
                    dist = np.linalg.norm(
                        self.population[i].genes - self.population[j].genes
                    )
                distances.append(dist)

        return np.mean(distances) if distances else 0.0

    def evolve_generation(self):
        """Evolve one generation."""
        new_population = []

        # Elitism - keep best individuals
        for i in range(self.elitism_count):
            if i < len(self.population):
                elite = Individual(
                    genes=self.population[i].genes.copy(),
                    fitness=self.population[i].fitness,
                    age=self.population[i].age + 1
                )
                new_population.append(elite)

        # Generate offspring
        while len(new_population) < self.population_size:
            # Select parents
            parent1, parent2 = self.select_parents()

            # Crossover
            child1, child2 = self.crossover(parent1, parent2)

            # Mutation
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)

            # Add to new population
            new_population.extend([child1, child2])

        # Trim to population size
        self.population = new_population[:self.population_size]

        # Evaluate new individuals
        self.evaluate_population()

        # Update statistics
        self.generation += 1
        best_fitness = self.population[0].fitness
        avg_fitness = np.mean([ind.fitness for ind in self.population])
        diversity = self.calculate_diversity()

        self.history['best_fitness'].append(best_fitness)
        self.history['avg_fitness'].append(avg_fitness)
        self.history['diversity'].append(diversity)

    def run(self, max_generations: int = 100,
            target_fitness: Optional[float] = None,
            verbose: bool = True) -> Individual:
        """
        Run the genetic algorithm.

        Args:
            max_generations: Maximum number of generations
            target_fitness: Stop if this fitness is reached
            verbose: Print progress

        Returns:
            Best individual found
        """
        # Initialize population
        self.initialize_population()

        if verbose:
            print(f"Starting GA with population size {self.population_size}")
            print(f"Initial best fitness: {self.best_individual.fitness:.6f}")

        # Evolution loop
        for gen in range(max_generations):
            self.evolve_generation()

            if verbose and gen % 10 == 0:
                print(f"Generation {gen}: Best fitness = {self.best_individual.fitness:.6f}, "
                      f"Avg = {self.history['avg_fitness'][-1]:.6f}, "
                      f"Diversity = {self.history['diversity'][-1]:.4f}")

            # Check termination criteria
            if target_fitness is not None and self.best_individual.fitness >= target_fitness:
                if verbose:
                    print(f"Target fitness {target_fitness} reached at generation {gen}")
                break

        if verbose:
            print(f"\nGA completed after {self.generation} generations")
            print(f"Best fitness: {self.best_individual.fitness:.6f}")

        return self.best_individual


class AdaptiveGeneticAlgorithm(GeneticAlgorithm):
    """
    Adaptive Genetic Algorithm that adjusts parameters during evolution.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_mutation_rate = self.mutation_rate
        self.initial_crossover_rate = self.crossover_rate

    def adapt_parameters(self):
        """Adapt GA parameters based on population statistics."""
        # Adapt mutation rate based on diversity
        diversity = self.history['diversity'][-1] if self.history['diversity'] else 1.0
        avg_diversity = np.mean(self.history['diversity'][-10:]) if len(self.history['diversity']) >= 10 else diversity

        if diversity < avg_diversity * 0.5:
            # Low diversity, increase mutation
            self.mutation_rate = min(0.1, self.mutation_rate * 1.1)
        elif diversity > avg_diversity * 1.5:
            # High diversity, decrease mutation
            self.mutation_rate = max(0.001, self.mutation_rate * 0.9)

        # Adapt crossover rate based on fitness improvement
        if len(self.history['best_fitness']) >= 10:
            recent_improvement = (
                self.history['best_fitness'][-1] -
                self.history['best_fitness'][-10]
            )

            if abs(recent_improvement) < 1e-6:
                # Stagnation, increase exploration
                self.crossover_rate = max(0.5, self.crossover_rate * 0.95)
            else:
                # Making progress, maintain exploitation
                self.crossover_rate = min(0.95, self.crossover_rate * 1.02)

    def evolve_generation(self):
        """Evolve with parameter adaptation."""
        super().evolve_generation()
        self.adapt_parameters()


def optimize_function_example():
    """Example: Optimize a complex mathematical function."""
    print("=" * 60)
    print("GENETIC ALGORITHM - FUNCTION OPTIMIZATION")
    print("=" * 60)

    # Define Rastrigin function (multimodal with many local minima)
    def rastrigin(x: np.ndarray) -> float:
        """Rastrigin function - challenging optimization problem."""
        n = len(x)
        A = 10
        return -(A * n + np.sum(x**2 - A * np.cos(2 * np.pi * x)))

    # Create GA
    ga = GeneticAlgorithm(
        fitness_function=rastrigin,
        gene_length=10,
        population_size=100,
        mutation_rate=0.02,
        crossover_rate=0.8,
        elitism_count=2,
        selection_method=SelectionMethod.TOURNAMENT,
        crossover_method=CrossoverMethod.ARITHMETIC,
        mutation_method=MutationMethod.GAUSSIAN,
        gene_type='real',
        gene_bounds=(-5.12, 5.12)
    )

    # Run optimization
    best = ga.run(max_generations=200, verbose=True)

    print(f"\nBest solution found: {best.genes}")
    print(f"Fitness (negative Rastrigin): {best.fitness:.6f}")
    print(f"Actual Rastrigin value: {-best.fitness:.6f}")

    # Theoretical minimum is 0 at x = [0, 0, ..., 0]
    distance_from_optimal = np.linalg.norm(best.genes)
    print(f"Distance from optimal: {distance_from_optimal:.6f}")


def traveling_salesman_example():
    """Example: Solve Traveling Salesman Problem using GA."""
    print("\n" + "=" * 60)
    print("GENETIC ALGORITHM - TRAVELING SALESMAN PROBLEM")
    print("=" * 60)

    # Generate random cities
    n_cities = 20
    np.random.seed(42)
    cities = np.random.rand(n_cities, 2) * 100

    # Calculate distance matrix
    dist_matrix = np.zeros((n_cities, n_cities))
    for i in range(n_cities):
        for j in range(n_cities):
            dist_matrix[i, j] = np.linalg.norm(cities[i] - cities[j])

    def tsp_fitness(route: np.ndarray) -> float:
        """Calculate negative total distance for a route."""
        total_distance = 0
        for i in range(len(route)):
            total_distance += dist_matrix[route[i], route[(i + 1) % len(route)]]
        return -total_distance

    # Create GA for TSP
    ga = GeneticAlgorithm(
        fitness_function=tsp_fitness,
        gene_length=n_cities,
        population_size=200,
        mutation_rate=0.05,
        crossover_rate=0.9,
        elitism_count=5,
        selection_method=SelectionMethod.TOURNAMENT,
        crossover_method=CrossoverMethod.ORDER,
        mutation_method=MutationMethod.SWAP,
        gene_type='permutation'
    )

    # Run optimization
    best = ga.run(max_generations=500, verbose=True)

    print(f"\nBest route found: {best.genes}")
    print(f"Total distance: {-best.fitness:.2f}")


def feature_selection_example():
    """Example: Feature selection for machine learning."""
    print("\n" + "=" * 60)
    print("GENETIC ALGORITHM - FEATURE SELECTION")
    print("=" * 60)

    # Simulated dataset with 50 features, only first 10 are relevant
    np.random.seed(42)
    n_samples = 100
    n_features = 50
    n_relevant = 10

    # Generate data
    X = np.random.randn(n_samples, n_features)
    # True weights (only first 10 features matter)
    true_weights = np.zeros(n_features)
    true_weights[:n_relevant] = np.random.randn(n_relevant)
    y = X @ true_weights + np.random.randn(n_samples) * 0.1

    def feature_fitness(selected_features: np.ndarray) -> float:
        """Evaluate feature subset using cross-validation score."""
        if np.sum(selected_features) == 0:
            return -1000  # Penalty for no features

        # Use only selected features
        X_selected = X[:, selected_features.astype(bool)]

        # Simple validation: correlation with target
        correlations = [np.corrcoef(X_selected[:, i], y)[0, 1]**2
                       for i in range(X_selected.shape[1])]

        # Fitness = average correlation - penalty for too many features
        avg_corr = np.mean(correlations) if correlations else 0
        n_selected = np.sum(selected_features)

        return avg_corr - 0.001 * n_selected

    # Create GA for feature selection
    ga = GeneticAlgorithm(
        fitness_function=feature_fitness,
        gene_length=n_features,
        population_size=50,
        mutation_rate=0.02,
        crossover_rate=0.8,
        elitism_count=2,
        selection_method=SelectionMethod.ROULETTE_WHEEL,
        crossover_method=CrossoverMethod.UNIFORM,
        mutation_method=MutationMethod.BIT_FLIP,
        gene_type='binary'
    )

    # Run optimization
    best = ga.run(max_generations=100, verbose=True)

    selected_indices = np.where(best.genes)[0]
    print(f"\nSelected features: {selected_indices}")
    print(f"Number of features selected: {len(selected_indices)}")
    print(f"Fitness score: {best.fitness:.4f}")

    # Check how many relevant features were found
    relevant_found = len([i for i in selected_indices if i < n_relevant])
    print(f"Relevant features found: {relevant_found}/{n_relevant}")


def adaptive_ga_example():
    """Example: Adaptive GA that adjusts parameters."""
    print("\n" + "=" * 60)
    print("ADAPTIVE GENETIC ALGORITHM")
    print("=" * 60)

    # Sphere function - simple but good for testing adaptation
    def sphere(x: np.ndarray) -> float:
        """Sphere function - minimize sum of squares."""
        return -np.sum(x**2)

    # Create adaptive GA
    ga = AdaptiveGeneticAlgorithm(
        fitness_function=sphere,
        gene_length=30,
        population_size=50,
        mutation_rate=0.01,
        crossover_rate=0.9,
        elitism_count=2,
        selection_method=SelectionMethod.RANK_BASED,
        crossover_method=CrossoverMethod.TWO_POINT,
        mutation_method=MutationMethod.GAUSSIAN,
        gene_type='real',
        gene_bounds=(-10, 10)
    )

    # Run optimization
    best = ga.run(max_generations=100, verbose=True)

    print(f"\nBest solution fitness: {best.fitness:.6f}")
    print(f"Distance from optimal: {np.linalg.norm(best.genes):.6f}")

    # Show parameter adaptation
    print("\nParameter adaptation:")
    print(f"Initial mutation rate: {ga.initial_mutation_rate:.4f}")
    print(f"Final mutation rate: {ga.mutation_rate:.4f}")
    print(f"Initial crossover rate: {ga.initial_crossover_rate:.4f}")
    print(f"Final crossover rate: {ga.crossover_rate:.4f}")


if __name__ == "__main__":
    # Run examples
    optimize_function_example()
    traveling_salesman_example()
    feature_selection_example()
    adaptive_ga_example()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- GA is effective for complex optimization with many local optima")
    print("- Selection pressure vs diversity is crucial balance")
    print("- Problem encoding (gene representation) greatly affects performance")
    print("- Adaptive parameters can prevent premature convergence")
    print("- GA is parallelizable and scales well")
    print("=" * 60)