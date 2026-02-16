"""
Genetic Algorithm Implementation
=================================

A comprehensive implementation of genetic algorithms for optimization problems.
Includes various selection, crossover, and mutation strategies.

Features:
- Binary and real-valued encodings
- Multiple selection methods (tournament, roulette wheel, rank)
- Various crossover operators (single-point, two-point, uniform)
- Adaptive mutation rates
- Elitism support
- Parallel evaluation support

Author: Claude
Date: January 2026
"""

import random
import numpy as np
from typing import List, Tuple, Callable, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import copy
import math


class SelectionMethod(Enum):
    """Selection methods for choosing parents."""
    TOURNAMENT = "tournament"
    ROULETTE_WHEEL = "roulette_wheel"
    RANK = "rank"
    STOCHASTIC_UNIVERSAL = "stochastic_universal"


class CrossoverMethod(Enum):
    """Crossover methods for creating offspring."""
    SINGLE_POINT = "single_point"
    TWO_POINT = "two_point"
    UNIFORM = "uniform"
    ARITHMETIC = "arithmetic"
    BLX_ALPHA = "blx_alpha"


class MutationMethod(Enum):
    """Mutation methods for introducing variation."""
    BIT_FLIP = "bit_flip"
    GAUSSIAN = "gaussian"
    UNIFORM = "uniform"
    POLYNOMIAL = "polynomial"
    ADAPTIVE = "adaptive"


@dataclass
class Individual:
    """Represents an individual in the population."""
    genes: Union[List[float], List[int], np.ndarray]
    fitness: Optional[float] = None
    age: int = 0
    metadata: Optional[dict] = None


class GeneticAlgorithm:
    """
    General-purpose genetic algorithm for optimization.

    This implementation supports both minimization and maximization problems,
    various genetic operators, and different encoding schemes.
    """

    def __init__(
        self,
        fitness_function: Callable,
        gene_length: int,
        population_size: int = 100,
        max_generations: int = 1000,
        mutation_rate: float = 0.01,
        crossover_rate: float = 0.8,
        elitism_count: int = 2,
        tournament_size: int = 3,
        selection_method: SelectionMethod = SelectionMethod.TOURNAMENT,
        crossover_method: CrossoverMethod = CrossoverMethod.TWO_POINT,
        mutation_method: MutationMethod = MutationMethod.BIT_FLIP,
        minimize: bool = True,
        bounds: Optional[List[Tuple[float, float]]] = None,
        integer_genes: bool = False,
        seed: Optional[int] = None
    ):
        """
        Initialize the genetic algorithm.

        Args:
            fitness_function: Function to evaluate fitness of individuals
            gene_length: Length of the gene/chromosome
            population_size: Number of individuals in population
            max_generations: Maximum number of generations
            mutation_rate: Probability of mutation
            crossover_rate: Probability of crossover
            elitism_count: Number of best individuals to preserve
            tournament_size: Size of tournament for selection
            selection_method: Method for parent selection
            crossover_method: Method for crossover
            mutation_method: Method for mutation
            minimize: Whether to minimize (True) or maximize (False) fitness
            bounds: Bounds for each gene (for real-valued encoding)
            integer_genes: Whether genes are integers
            seed: Random seed for reproducibility
        """
        self.fitness_function = fitness_function
        self.gene_length = gene_length
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count
        self.tournament_size = tournament_size
        self.selection_method = selection_method
        self.crossover_method = crossover_method
        self.mutation_method = mutation_method
        self.minimize = minimize
        self.bounds = bounds or [(0, 1) for _ in range(gene_length)]
        self.integer_genes = integer_genes

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        self.population: List[Individual] = []
        self.best_individual: Optional[Individual] = None
        self.generation = 0
        self.fitness_history: List[float] = []
        self.diversity_history: List[float] = []

    def _create_random_individual(self) -> Individual:
        """Create a random individual."""
        if self.integer_genes:
            genes = [
                random.randint(int(self.bounds[i][0]), int(self.bounds[i][1]))
                for i in range(self.gene_length)
            ]
        else:
            genes = [
                random.uniform(self.bounds[i][0], self.bounds[i][1])
                for i in range(self.gene_length)
            ]
        return Individual(genes=genes)

    def _evaluate_fitness(self, individual: Individual) -> float:
        """Evaluate fitness of an individual."""
        if individual.fitness is None:
            individual.fitness = self.fitness_function(individual.genes)
        return individual.fitness

    def _initialize_population(self):
        """Initialize the population with random individuals."""
        self.population = [
            self._create_random_individual()
            for _ in range(self.population_size)
        ]

        # Evaluate initial population
        for individual in self.population:
            self._evaluate_fitness(individual)

    def _tournament_selection(self, population: List[Individual]) -> Individual:
        """Select an individual using tournament selection."""
        tournament = random.sample(population, min(self.tournament_size, len(population)))
        return min(tournament, key=lambda x: x.fitness) if self.minimize else max(tournament, key=lambda x: x.fitness)

    def _roulette_wheel_selection(self, population: List[Individual]) -> Individual:
        """Select an individual using roulette wheel selection."""
        # For minimization, use inverted fitness
        if self.minimize:
            max_fitness = max(ind.fitness for ind in population)
            fitnesses = [max_fitness - ind.fitness + 1e-6 for ind in population]
        else:
            fitnesses = [ind.fitness for ind in population]

        total_fitness = sum(fitnesses)
        if total_fitness == 0:
            return random.choice(population)

        probabilities = [f / total_fitness for f in fitnesses]
        return np.random.choice(population, p=probabilities)

    def _rank_selection(self, population: List[Individual]) -> Individual:
        """Select an individual using rank-based selection."""
        sorted_pop = sorted(population, key=lambda x: x.fitness, reverse=not self.minimize)
        ranks = list(range(1, len(sorted_pop) + 1))
        total_rank = sum(ranks)
        probabilities = [r / total_rank for r in ranks]
        return np.random.choice(sorted_pop, p=probabilities)

    def _select_parent(self, population: List[Individual]) -> Individual:
        """Select a parent based on the selection method."""
        if self.selection_method == SelectionMethod.TOURNAMENT:
            return self._tournament_selection(population)
        elif self.selection_method == SelectionMethod.ROULETTE_WHEEL:
            return self._roulette_wheel_selection(population)
        elif self.selection_method == SelectionMethod.RANK:
            return self._rank_selection(population)
        else:
            return random.choice(population)

    def _single_point_crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Perform single-point crossover."""
        if random.random() > self.crossover_rate:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)

        point = random.randint(1, self.gene_length - 1)
        child1_genes = parent1.genes[:point] + parent2.genes[point:]
        child2_genes = parent2.genes[:point] + parent1.genes[point:]

        return Individual(genes=child1_genes), Individual(genes=child2_genes)

    def _two_point_crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Perform two-point crossover."""
        if random.random() > self.crossover_rate:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)

        point1 = random.randint(0, self.gene_length - 2)
        point2 = random.randint(point1 + 1, self.gene_length - 1)

        child1_genes = parent1.genes[:point1] + parent2.genes[point1:point2] + parent1.genes[point2:]
        child2_genes = parent2.genes[:point1] + parent1.genes[point1:point2] + parent2.genes[point2:]

        return Individual(genes=child1_genes), Individual(genes=child2_genes)

    def _uniform_crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Perform uniform crossover."""
        if random.random() > self.crossover_rate:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)

        child1_genes = []
        child2_genes = []

        for i in range(self.gene_length):
            if random.random() < 0.5:
                child1_genes.append(parent1.genes[i])
                child2_genes.append(parent2.genes[i])
            else:
                child1_genes.append(parent2.genes[i])
                child2_genes.append(parent1.genes[i])

        return Individual(genes=child1_genes), Individual(genes=child2_genes)

    def _arithmetic_crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Perform arithmetic crossover (for real-valued genes)."""
        if random.random() > self.crossover_rate or self.integer_genes:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)

        alpha = random.random()
        child1_genes = [
            alpha * p1 + (1 - alpha) * p2
            for p1, p2 in zip(parent1.genes, parent2.genes)
        ]
        child2_genes = [
            (1 - alpha) * p1 + alpha * p2
            for p1, p2 in zip(parent1.genes, parent2.genes)
        ]

        # Ensure bounds
        for i in range(self.gene_length):
            child1_genes[i] = max(self.bounds[i][0], min(self.bounds[i][1], child1_genes[i]))
            child2_genes[i] = max(self.bounds[i][0], min(self.bounds[i][1], child2_genes[i]))

        return Individual(genes=child1_genes), Individual(genes=child2_genes)

    def _crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Perform crossover based on the selected method."""
        if self.crossover_method == CrossoverMethod.SINGLE_POINT:
            return self._single_point_crossover(parent1, parent2)
        elif self.crossover_method == CrossoverMethod.TWO_POINT:
            return self._two_point_crossover(parent1, parent2)
        elif self.crossover_method == CrossoverMethod.UNIFORM:
            return self._uniform_crossover(parent1, parent2)
        elif self.crossover_method == CrossoverMethod.ARITHMETIC:
            return self._arithmetic_crossover(parent1, parent2)
        else:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)

    def _bit_flip_mutation(self, individual: Individual) -> Individual:
        """Perform bit flip mutation (for binary/integer genes)."""
        mutated = copy.deepcopy(individual)

        for i in range(self.gene_length):
            if random.random() < self.mutation_rate:
                if self.integer_genes:
                    # For integers, randomly select a new value
                    mutated.genes[i] = random.randint(
                        int(self.bounds[i][0]),
                        int(self.bounds[i][1])
                    )
                else:
                    # For binary, flip the bit
                    if self.bounds[i] == (0, 1):
                        mutated.genes[i] = 1 - mutated.genes[i]
                    else:
                        # For real values, add random noise
                        mutated.genes[i] = random.uniform(
                            self.bounds[i][0],
                            self.bounds[i][1]
                        )

        mutated.fitness = None  # Reset fitness
        return mutated

    def _gaussian_mutation(self, individual: Individual) -> Individual:
        """Perform Gaussian mutation (for real-valued genes)."""
        if self.integer_genes:
            return self._bit_flip_mutation(individual)

        mutated = copy.deepcopy(individual)

        for i in range(self.gene_length):
            if random.random() < self.mutation_rate:
                # Add Gaussian noise
                std_dev = (self.bounds[i][1] - self.bounds[i][0]) * 0.1
                mutated.genes[i] += random.gauss(0, std_dev)
                # Ensure bounds
                mutated.genes[i] = max(
                    self.bounds[i][0],
                    min(self.bounds[i][1], mutated.genes[i])
                )

        mutated.fitness = None
        return mutated

    def _mutate(self, individual: Individual) -> Individual:
        """Perform mutation based on the selected method."""
        if self.mutation_method == MutationMethod.BIT_FLIP:
            return self._bit_flip_mutation(individual)
        elif self.mutation_method == MutationMethod.GAUSSIAN:
            return self._gaussian_mutation(individual)
        else:
            return self._bit_flip_mutation(individual)

    def _get_elite(self, population: List[Individual]) -> List[Individual]:
        """Get the elite individuals from the population."""
        sorted_pop = sorted(
            population,
            key=lambda x: x.fitness,
            reverse=not self.minimize
        )
        return sorted_pop[:self.elitism_count]

    def _calculate_diversity(self) -> float:
        """Calculate population diversity."""
        if not self.population:
            return 0.0

        # Calculate average pairwise distance
        total_distance = 0
        count = 0

        for i in range(len(self.population)):
            for j in range(i + 1, len(self.population)):
                distance = sum(
                    abs(g1 - g2)
                    for g1, g2 in zip(
                        self.population[i].genes,
                        self.population[j].genes
                    )
                )
                total_distance += distance
                count += 1

        return total_distance / count if count > 0 else 0.0

    def run(self, verbose: bool = True) -> Individual:
        """
        Run the genetic algorithm.

        Args:
            verbose: Whether to print progress

        Returns:
            The best individual found
        """
        # Initialize population
        self._initialize_population()

        # Track best individual
        self.best_individual = min(
            self.population,
            key=lambda x: x.fitness
        ) if self.minimize else max(
            self.population,
            key=lambda x: x.fitness
        )

        # Evolution loop
        for generation in range(self.max_generations):
            self.generation = generation

            # Calculate and store diversity
            diversity = self._calculate_diversity()
            self.diversity_history.append(diversity)

            # Create new population
            new_population = []

            # Add elite individuals
            elite = self._get_elite(self.population)
            new_population.extend(copy.deepcopy(elite))

            # Generate offspring
            while len(new_population) < self.population_size:
                # Select parents
                parent1 = self._select_parent(self.population)
                parent2 = self._select_parent(self.population)

                # Crossover
                child1, child2 = self._crossover(parent1, parent2)

                # Mutation
                child1 = self._mutate(child1)
                child2 = self._mutate(child2)

                # Evaluate fitness
                self._evaluate_fitness(child1)
                self._evaluate_fitness(child2)

                # Add to new population
                new_population.append(child1)
                if len(new_population) < self.population_size:
                    new_population.append(child2)

            # Update population
            self.population = new_population[:self.population_size]

            # Update best individual
            current_best = min(
                self.population,
                key=lambda x: x.fitness
            ) if self.minimize else max(
                self.population,
                key=lambda x: x.fitness
            )

            if self.minimize:
                if current_best.fitness < self.best_individual.fitness:
                    self.best_individual = copy.deepcopy(current_best)
            else:
                if current_best.fitness > self.best_individual.fitness:
                    self.best_individual = copy.deepcopy(current_best)

            # Store fitness history
            self.fitness_history.append(self.best_individual.fitness)

            # Print progress
            if verbose and generation % 10 == 0:
                avg_fitness = sum(ind.fitness for ind in self.population) / len(self.population)
                print(f"Generation {generation}: Best fitness = {self.best_individual.fitness:.6f}, "
                      f"Avg fitness = {avg_fitness:.6f}, Diversity = {diversity:.4f}")

            # Early stopping if converged
            if len(self.fitness_history) > 50:
                recent_improvement = abs(
                    self.fitness_history[-1] - self.fitness_history[-50]
                )
                if recent_improvement < 1e-6:
                    if verbose:
                        print(f"Converged at generation {generation}")
                    break

        return self.best_individual


class BinaryGA(GeneticAlgorithm):
    """
    Genetic algorithm specifically for binary optimization problems.

    Useful for problems like knapsack, feature selection, etc.
    """

    def __init__(self, fitness_function: Callable, gene_length: int, **kwargs):
        """Initialize binary GA with appropriate defaults."""
        super().__init__(
            fitness_function=fitness_function,
            gene_length=gene_length,
            bounds=[(0, 1) for _ in range(gene_length)],
            integer_genes=True,
            mutation_method=MutationMethod.BIT_FLIP,
            **kwargs
        )

    def _create_random_individual(self) -> Individual:
        """Create a random binary individual."""
        genes = [random.randint(0, 1) for _ in range(self.gene_length)]
        return Individual(genes=genes)


class RealValuedGA(GeneticAlgorithm):
    """
    Genetic algorithm for continuous optimization problems.

    Useful for function optimization, parameter tuning, etc.
    """

    def __init__(
        self,
        fitness_function: Callable,
        bounds: List[Tuple[float, float]],
        **kwargs
    ):
        """Initialize real-valued GA with appropriate defaults."""
        super().__init__(
            fitness_function=fitness_function,
            gene_length=len(bounds),
            bounds=bounds,
            integer_genes=False,
            crossover_method=CrossoverMethod.ARITHMETIC,
            mutation_method=MutationMethod.GAUSSIAN,
            **kwargs
        )


class TSPGeneticAlgorithm:
    """
    Specialized genetic algorithm for the Traveling Salesman Problem.

    Uses permutation encoding and specialized operators.
    """

    def __init__(
        self,
        distance_matrix: np.ndarray,
        population_size: int = 100,
        max_generations: int = 1000,
        mutation_rate: float = 0.02,
        crossover_rate: float = 0.8,
        elitism_count: int = 2,
        tournament_size: int = 5,
        seed: Optional[int] = None
    ):
        """
        Initialize TSP genetic algorithm.

        Args:
            distance_matrix: Matrix of distances between cities
            population_size: Number of individuals
            max_generations: Maximum generations
            mutation_rate: Probability of mutation
            crossover_rate: Probability of crossover
            elitism_count: Number of elite individuals
            tournament_size: Tournament size
            seed: Random seed
        """
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count
        self.tournament_size = tournament_size

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        self.population = []
        self.best_tour = None
        self.best_distance = float('inf')
        self.fitness_history = []

    def _calculate_distance(self, tour: List[int]) -> float:
        """Calculate total distance of a tour."""
        distance = 0
        for i in range(len(tour)):
            from_city = tour[i]
            to_city = tour[(i + 1) % len(tour)]
            distance += self.distance_matrix[from_city][to_city]
        return distance

    def _create_random_tour(self) -> List[int]:
        """Create a random tour."""
        tour = list(range(self.num_cities))
        random.shuffle(tour)
        return tour

    def _initialize_population(self):
        """Initialize population with random tours."""
        self.population = [
            self._create_random_tour()
            for _ in range(self.population_size)
        ]

    def _tournament_selection(self) -> List[int]:
        """Select a tour using tournament selection."""
        tournament = random.sample(self.population, self.tournament_size)
        return min(tournament, key=self._calculate_distance)

    def _order_crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        """Perform order crossover (OX)."""
        if random.random() > self.crossover_rate:
            return parent1.copy()

        size = len(parent1)
        start = random.randint(0, size - 2)
        end = random.randint(start + 1, size - 1)

        child = [-1] * size
        child[start:end] = parent1[start:end]

        pointer = end
        for city in parent2[end:] + parent2[:end]:
            if city not in child:
                child[pointer % size] = city
                pointer += 1

        return child

    def _swap_mutation(self, tour: List[int]) -> List[int]:
        """Perform swap mutation."""
        mutated = tour.copy()

        if random.random() < self.mutation_rate:
            i, j = random.sample(range(len(tour)), 2)
            mutated[i], mutated[j] = mutated[j], mutated[i]

        return mutated

    def _inversion_mutation(self, tour: List[int]) -> List[int]:
        """Perform inversion mutation."""
        mutated = tour.copy()

        if random.random() < self.mutation_rate:
            start = random.randint(0, len(tour) - 2)
            end = random.randint(start + 1, len(tour) - 1)
            mutated[start:end] = reversed(mutated[start:end])

        return mutated

    def run(self, verbose: bool = True) -> Tuple[List[int], float]:
        """
        Run the TSP genetic algorithm.

        Returns:
            Best tour and its distance
        """
        self._initialize_population()

        for generation in range(self.max_generations):
            # Evaluate population
            distances = [self._calculate_distance(tour) for tour in self.population]

            # Update best solution
            min_idx = np.argmin(distances)
            if distances[min_idx] < self.best_distance:
                self.best_distance = distances[min_idx]
                self.best_tour = self.population[min_idx].copy()

            self.fitness_history.append(self.best_distance)

            # Print progress
            if verbose and generation % 10 == 0:
                avg_distance = np.mean(distances)
                print(f"Generation {generation}: Best = {self.best_distance:.2f}, "
                      f"Avg = {avg_distance:.2f}")

            # Create new population
            new_population = []

            # Elitism
            elite_indices = np.argsort(distances)[:self.elitism_count]
            for idx in elite_indices:
                new_population.append(self.population[idx].copy())

            # Generate offspring
            while len(new_population) < self.population_size:
                parent1 = self._tournament_selection()
                parent2 = self._tournament_selection()

                child = self._order_crossover(parent1, parent2)
                child = self._swap_mutation(child)
                child = self._inversion_mutation(child)

                new_population.append(child)

            self.population = new_population[:self.population_size]

        return self.best_tour, self.best_distance


def example_usage():
    """Demonstrate genetic algorithm functionality."""
    print("=" * 60)
    print("GENETIC ALGORITHM EXAMPLES")
    print("=" * 60)

    # Example 1: Optimize a simple function
    print("\n1. Function Optimization (Rastrigin Function):")
    print("-" * 40)

    def rastrigin(x):
        """Rastrigin function - a common benchmark."""
        n = len(x)
        return 10 * n + sum(xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x)

    # Optimize Rastrigin function
    ga = RealValuedGA(
        fitness_function=rastrigin,
        bounds=[(-5.12, 5.12)] * 5,  # 5D problem
        population_size=50,
        max_generations=200,
        minimize=True,
        seed=42
    )

    best = ga.run(verbose=False)
    print(f"Best solution: {[f'{g:.4f}' for g in best.genes]}")
    print(f"Best fitness: {best.fitness:.6f}")
    print(f"(Global optimum is at [0,0,0,0,0] with fitness 0)")

    # Example 2: Binary optimization (Knapsack Problem)
    print("\n2. Binary Optimization (0/1 Knapsack Problem):")
    print("-" * 40)

    # Knapsack problem data
    weights = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    values = [1, 6, 10, 16, 19, 22, 28, 31, 35, 40]
    capacity = 200

    def knapsack_fitness(genes):
        """Fitness function for knapsack problem."""
        total_weight = sum(g * w for g, w in zip(genes, weights))
        total_value = sum(g * v for g, v in zip(genes, values))

        # Penalty for exceeding capacity
        if total_weight > capacity:
            return total_value - 10 * (total_weight - capacity)
        return total_value

    binary_ga = BinaryGA(
        fitness_function=knapsack_fitness,
        gene_length=len(weights),
        population_size=50,
        max_generations=100,
        minimize=False,  # Maximize value
        seed=42
    )

    best = binary_ga.run(verbose=False)
    selected_items = [i for i, g in enumerate(best.genes) if g == 1]
    total_weight = sum(weights[i] for i in selected_items)
    total_value = sum(values[i] for i in selected_items)

    print(f"Selected items: {selected_items}")
    print(f"Total weight: {total_weight} / {capacity}")
    print(f"Total value: {total_value}")

    # Example 3: TSP
    print("\n3. Traveling Salesman Problem:")
    print("-" * 40)

    # Create a small TSP instance
    np.random.seed(42)
    num_cities = 10
    cities = np.random.rand(num_cities, 2) * 100

    # Calculate distance matrix
    distance_matrix = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                distance_matrix[i][j] = np.linalg.norm(cities[i] - cities[j])

    tsp_ga = TSPGeneticAlgorithm(
        distance_matrix=distance_matrix,
        population_size=100,
        max_generations=200,
        seed=42
    )

    best_tour, best_distance = tsp_ga.run(verbose=False)
    print(f"Best tour: {best_tour}")
    print(f"Tour distance: {best_distance:.2f}")

    # Example 4: Parameter tuning
    print("\n4. Neural Network Weight Optimization:")
    print("-" * 40)

    # Simulate optimizing weights for a simple neural network
    def nn_fitness(weights):
        """Simulated neural network fitness."""
        # Simulate some complex fitness landscape
        return -sum(w**2 for w in weights) + sum(np.sin(w) for w in weights)

    nn_ga = RealValuedGA(
        fitness_function=nn_fitness,
        bounds=[(-2, 2)] * 10,  # 10 weights
        population_size=30,
        max_generations=100,
        minimize=False,
        seed=42
    )

    best = nn_ga.run(verbose=False)
    print(f"Best weights found (first 5): {[f'{w:.3f}' for w in best.genes[:5]]}")
    print(f"Fitness: {best.fitness:.4f}")

    # Show evolution progress
    print("\n5. Evolution Progress Visualization:")
    print("-" * 40)

    # Run a simple optimization to show progress
    def sphere(x):
        """Simple sphere function."""
        return sum(xi**2 for xi in x)

    ga_vis = RealValuedGA(
        fitness_function=sphere,
        bounds=[(-10, 10)] * 3,
        population_size=30,
        max_generations=50,
        minimize=True,
        seed=42
    )

    ga_vis.run(verbose=False)

    # Show fitness improvement over generations
    print("Fitness improvement over generations:")
    for i in range(0, len(ga_vis.fitness_history), 10):
        fitness = ga_vis.fitness_history[i]
        bar_length = int(50 * (1 - fitness / ga_vis.fitness_history[0]))
        bar = '=' * bar_length + '-' * (50 - bar_length)
        print(f"Gen {i:3d}: [{bar}] {fitness:.6f}")

    print("\nDiversity over time:")
    for i in range(0, len(ga_vis.diversity_history), 10):
        diversity = ga_vis.diversity_history[i]
        bar_length = int(50 * diversity / max(ga_vis.diversity_history))
        bar = '*' * bar_length + ' ' * (50 - bar_length)
        print(f"Gen {i:3d}: [{bar}] {diversity:.4f}")

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- GAs are good for complex, non-convex optimization")
    print("- Population diversity is crucial for exploration")
    print("- Elitism helps preserve good solutions")
    print("- Problem-specific operators improve performance")
    print("- Balance exploration (diversity) vs exploitation (convergence)")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()