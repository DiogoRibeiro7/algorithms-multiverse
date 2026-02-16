# Optimization Algorithms

A comprehensive collection of metaheuristic and local search optimization algorithms for solving complex optimization problems including continuous, discrete, and combinatorial optimization challenges.

## 📚 Table of Contents

- [Overview](#overview)
- [Implemented Algorithms](#implemented-algorithms)
- [Installation](#installation)
- [Algorithm Details](#algorithm-details)
- [Usage Examples](#usage-examples)
- [Performance Comparison](#performance-comparison)
- [Applications](#applications)
- [Algorithm Selection Guide](#algorithm-selection-guide)
- [References](#references)

## 🎯 Overview

Optimization algorithms are techniques for finding the best solution from a set of possible solutions. This module implements various metaheuristic algorithms that can handle:

- **Non-convex optimization**: Multiple local optima
- **Large search spaces**: Exponential or infinite possibilities
- **Complex constraints**: Non-linear, discrete, or mixed
- **No gradient information**: Black-box optimization
- **Multi-objective problems**: Trade-offs between objectives

### Key Features

- **Population-based methods**: Explore multiple solutions simultaneously
- **Single-solution methods**: Intensively explore neighborhoods
- **Hybrid approaches**: Combine global and local search
- **Memory structures**: Learn from search history
- **Adaptive mechanisms**: Self-tuning parameters

## 📊 Implemented Algorithms

### 1. Genetic Algorithm (`genetic_algorithm.py`)

| Component | Options | Purpose |
|-----------|---------|---------|
| **Selection** | Tournament, Roulette, Rank, Stochastic Universal | Choose parents |
| **Crossover** | Single-point, Two-point, Uniform, Arithmetic, Order | Create offspring |
| **Mutation** | Bit flip, Gaussian, Swap, Inversion, Scramble | Introduce variation |
| **Variants** | Standard GA, Adaptive GA, Steady-State GA | Different evolution strategies |

### 2. Simulated Annealing (`simulated_annealing.py`)

| Component | Options | Properties |
|-----------|---------|------------|
| **Cooling Schedules** | Linear, Exponential, Logarithmic, Adaptive | Temperature reduction |
| **Acceptance** | Metropolis criterion | Probabilistic acceptance |
| **Variants** | Standard SA, Parallel Tempering, Fast SA | Different strategies |
| **Reheating** | Periodic reheating, Adaptive reheating | Escape local optima |

### 3. Particle Swarm Optimization (`particle_swarm.py`)

| Component | Options | Description |
|-----------|---------|-------------|
| **Topologies** | Global, Ring, Von Neumann, Star, Random | Information sharing |
| **Inertia** | Linear, Exponential, Random, Chaotic, Adaptive | Exploration vs exploitation |
| **Variants** | Standard PSO, Binary PSO, Quantum PSO, Multi-Swarm | Different behaviors |
| **Constriction** | Clerc's constriction, Velocity clamping | Convergence control |

### 4. Ant Colony Optimization (`ant_colony.py`)

| Component | Options | Application |
|-----------|---------|-------------|
| **Variants** | AS, ACS, MMAS, Rank-based, Elitist | Pheromone strategies |
| **Problems** | TSP, VRP, Job Shop, Graph Coloring | Combinatorial optimization |
| **Pheromone** | Evaporation, Bounds, Local/Global update | Trail management |
| **Heuristics** | Distance, Time, Cost-based | Problem-specific guidance |

### 5. Hill Climbing (`hill_climbing.py`)

| Variant | Strategy | Best For |
|---------|----------|----------|
| **Simple** | First improvement | Fast convergence |
| **Steepest Ascent** | Best improvement | Thorough search |
| **Stochastic** | Random from improving | Avoiding determinism |
| **Random Restart** | Multiple starts | Multimodal problems |
| **Variable Neighborhood** | Change neighborhood | Adaptive search |
| **Late Acceptance** | Historical comparison | Escape plateaus |

### 6. Tabu Search (`tabu_search.py`)

| Component | Function | Memory Type |
|-----------|----------|-------------|
| **Tabu List** | Forbid recent moves | Short-term |
| **Aspiration** | Override tabu status | Exception handling |
| **Intensification** | Focus on good regions | Medium-term |
| **Diversification** | Explore new regions | Long-term |
| **Reactive** | Adjust tabu tenure | Adaptive |

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/algorithms-multiverse.git
cd algorithms-multiverse/optimization-algorithms

# Install dependencies (optional - for enhanced features)
pip install numpy
```

## 💡 Algorithm Details

### Genetic Algorithm

**How it works:**
1. Initialize random population
2. Evaluate fitness of individuals
3. Select parents based on fitness
4. Create offspring through crossover
5. Apply mutation for diversity
6. Replace population
7. Repeat until convergence

**Key Parameters:**
- `population_size`: Number of solutions (50-200)
- `mutation_rate`: Probability of mutation (0.01-0.1)
- `crossover_rate`: Probability of crossover (0.6-0.9)
- `selection_pressure`: How strongly to favor better solutions

### Simulated Annealing

**How it works:**
1. Start with initial solution and temperature
2. Generate neighbor solution
3. Accept if better, or with probability if worse
4. Reduce temperature
5. Repeat until frozen

**Key Parameters:**
- `initial_temp`: Starting temperature (problem-dependent)
- `cooling_rate`: Temperature reduction factor (0.8-0.99)
- `neighborhood_size`: Size of perturbation

### Particle Swarm Optimization

**How it works:**
1. Initialize particle positions and velocities
2. Evaluate fitness of each particle
3. Update personal and global best positions
4. Update velocities toward best positions
5. Update positions
6. Repeat until convergence

**Key Parameters:**
- `n_particles`: Swarm size (20-50)
- `inertia`: Balance exploration/exploitation (0.4-0.9)
- `cognitive/social`: Learning factors (1.5-2.5)

### Ant Colony Optimization

**How it works:**
1. Initialize pheromone trails
2. Each ant constructs solution probabilistically
3. Evaluate solution quality
4. Update pheromone trails
5. Evaporate old pheromones
6. Repeat with new ant generation

**Key Parameters:**
- `n_ants`: Colony size (10-50)
- `alpha/beta`: Pheromone/heuristic importance (1-5)
- `rho`: Evaporation rate (0.1-0.5)

### Hill Climbing

**How it works:**
1. Start with initial solution
2. Generate neighboring solutions
3. Move to better neighbor
4. Repeat until no improvement

**Key Parameters:**
- `neighborhood_size`: Search radius
- `max_neighbors`: Neighbors to evaluate
- `restart_threshold`: When to restart

### Tabu Search

**How it works:**
1. Start with initial solution
2. Generate neighbors
3. Select best non-tabu neighbor
4. Update tabu list
5. Apply aspiration if exceptional
6. Repeat with memory guidance

**Key Parameters:**
- `tabu_tenure`: Memory length (7-20)
- `aspiration_level`: Override threshold
- `diversification_trigger`: When to explore

## 💻 Usage Examples

### Example 1: Function Optimization with GA

```python
from genetic_algorithm import GeneticAlgorithm
import numpy as np

# Define objective function (Rastrigin)
def rastrigin(x):
    A = 10
    return -(A * len(x) + np.sum(x**2 - A * np.cos(2 * np.pi * x)))

# Create and run GA
ga = GeneticAlgorithm(
    fitness_function=rastrigin,
    gene_length=10,
    population_size=100,
    mutation_rate=0.02,
    crossover_rate=0.8,
    gene_type='real',
    gene_bounds=(-5.12, 5.12)
)

best = ga.run(max_generations=200)
print(f"Best solution: {best.genes}")
print(f"Fitness: {best.fitness}")
```

### Example 2: TSP with Ant Colony

```python
from ant_colony import AntColonyOptimization
import numpy as np

# Create distance matrix
n_cities = 50
cities = np.random.rand(n_cities, 2) * 100
distance_matrix = np.zeros((n_cities, n_cities))
for i in range(n_cities):
    for j in range(n_cities):
        distance_matrix[i, j] = np.linalg.norm(cities[i] - cities[j])

# Run ACO
aco = AntColonyOptimization(
    distance_matrix=distance_matrix,
    n_ants=25,
    n_iterations=100,
    alpha=1.0,
    beta=3.0,
    rho=0.5
)

best_tour, best_distance = aco.run()
print(f"Best tour distance: {best_distance:.2f}")
```

### Example 3: Continuous Optimization with PSO

```python
from particle_swarm import ParticleSwarmOptimization

# Sphere function
def sphere(x):
    return -np.sum(x**2)

# Run PSO
pso = ParticleSwarmOptimization(
    objective_function=sphere,
    n_dimensions=30,
    n_particles=50,
    bounds=(-10, 10)
)

best_position, best_fitness = pso.run(max_iterations=200)
print(f"Best position norm: {np.linalg.norm(best_position):.6f}")
```

### Example 4: Scheduling with Tabu Search

```python
from tabu_search import TabuSearch

# Job shop scheduling
def makespan(schedule):
    # Calculate completion time
    return max_completion_time

def schedule_neighbor(schedule):
    # Swap two operations
    return new_schedule

ts = TabuSearch(
    objective_function=makespan,
    initial_solution=initial_schedule,
    neighbor_function=schedule_neighbor,
    tabu_tenure=10,
    max_iterations=500
)

best_schedule, best_makespan = ts.run()
```

## 📈 Performance Comparison

### Benchmark Functions

| Algorithm | Sphere | Rastrigin | Rosenbrock | Schwefel | Ackley |
|-----------|--------|-----------|------------|----------|---------|
| **GA** | Good | Excellent | Good | Very Good | Good |
| **SA** | Good | Good | Excellent | Good | Good |
| **PSO** | Excellent | Good | Good | Good | Very Good |
| **ACO** | Poor | Poor | Poor | Poor | Poor |
| **Hill Climbing** | Excellent* | Poor | Good* | Poor | Poor |
| **Tabu Search** | Good | Fair | Good | Fair | Fair |

*Only for convex/unimodal regions

### Combinatorial Problems

| Algorithm | TSP | VRP | Job Shop | Knapsack | Graph Coloring |
|-----------|-----|-----|----------|----------|----------------|
| **GA** | Good | Good | Good | Excellent | Good |
| **SA** | Very Good | Good | Very Good | Good | Good |
| **PSO** | Fair | Fair | Poor | Good | Poor |
| **ACO** | Excellent | Excellent | Good | Poor | Good |
| **Hill Climbing** | Poor | Poor | Poor | Fair | Fair |
| **Tabu Search** | Excellent | Very Good | Excellent | Good | Very Good |

### Algorithm Characteristics

| Algorithm | Global Search | Local Search | Memory | Parallelizable | Parameter Sensitivity |
|-----------|--------------|--------------|---------|----------------|---------------------|
| **GA** | Excellent | Fair | No | Excellent | Medium |
| **SA** | Good | Excellent | No | Good | High |
| **PSO** | Very Good | Good | Limited | Excellent | Low |
| **ACO** | Good | Good | Yes | Good | Medium |
| **Hill Climbing** | Poor | Excellent | No | Excellent | Low |
| **Tabu Search** | Fair | Excellent | Yes | Fair | Medium |

## 🎯 Applications

### By Problem Type

#### Continuous Optimization
- **Best choices**: PSO, GA (real-coded), SA
- **Applications**: Parameter tuning, function optimization, engineering design

#### Discrete Optimization
- **Best choices**: GA (binary), Tabu Search, SA
- **Applications**: Feature selection, knapsack problems, scheduling

#### Combinatorial Optimization
- **Best choices**: ACO, Tabu Search, GA (permutation)
- **Applications**: TSP, VRP, graph problems, assignment problems

#### Constrained Optimization
- **Best choices**: GA (with penalty), PSO (with constraints), Tabu Search
- **Applications**: Resource allocation, engineering design, portfolio optimization

### By Industry

#### Engineering
- Design optimization (GA, PSO)
- Structural optimization (SA, PSO)
- Control system tuning (PSO, GA)

#### Logistics
- Vehicle routing (ACO, Tabu Search)
- Warehouse layout (SA, GA)
- Supply chain optimization (GA, PSO)

#### Finance
- Portfolio optimization (GA, PSO)
- Risk management (SA, GA)
- Trading strategies (GA, PSO)

#### Machine Learning
- Hyperparameter tuning (GA, PSO)
- Feature selection (GA, Tabu Search)
- Neural architecture search (GA)

## 🔍 Algorithm Selection Guide

### Decision Tree

```
Start
│
├─ Problem Type?
│  ├─ Continuous → PSO or SA
│  ├─ Discrete → GA or Tabu Search
│  └─ Combinatorial → ACO or Tabu Search
│
├─ Search Space Size?
│  ├─ Small → Hill Climbing
│  ├─ Medium → SA or Tabu Search
│  └─ Large → GA or PSO
│
├─ Solution Quality Required?
│  ├─ Optimal → Tabu Search + Local Search
│  ├─ Very Good → GA or PSO
│  └─ Good Enough → Hill Climbing + Random Restart
│
└─ Time Available?
   ├─ Very Limited → Hill Climbing
   ├─ Limited → SA or PSO
   └─ Sufficient → GA or ACO
```

### Recommendations by Criteria

| If you need... | Use... | Because... |
|----------------|--------|------------|
| Fast convergence | Hill Climbing, PSO | Exploit local information |
| Global optimum | GA, Multi-start methods | Explore widely |
| Handle constraints | Tabu Search, GA | Flexible frameworks |
| Simple implementation | Hill Climbing, SA | Minimal parameters |
| Parallel execution | GA, PSO | Population-based |
| Avoid revisiting | Tabu Search | Memory structures |

## 🔧 Advanced Techniques

### Hybrid Algorithms

```python
# GA + Local Search
def hybrid_ga_local_search():
    ga = GeneticAlgorithm(...)

    # After each generation
    for individual in population:
        improved = hill_climb(individual)
        individual.genes = improved
```

### Parameter Adaptation

```python
# Adaptive PSO
class AdaptivePSO(PSO):
    def adapt_parameters(self):
        if diversity < threshold:
            self.inertia *= 1.1  # Increase exploration
        else:
            self.inertia *= 0.9  # Increase exploitation
```

### Multi-Objective Optimization

```python
# Pareto-based selection in GA
def pareto_dominance(sol1, sol2):
    return all(obj1 <= obj2 for obj1, obj2 in zip(sol1, sol2))
```

## 📚 References

### Books
- "Metaheuristics: From Design to Implementation" - Talbi
- "Handbook of Metaheuristics" - Glover & Kochenberger
- "Essentials of Metaheuristics" - Luke

### Key Papers
- Holland (1975) - Genetic Algorithms
- Kirkpatrick et al. (1983) - Simulated Annealing
- Kennedy & Eberhart (1995) - Particle Swarm Optimization
- Dorigo (1992) - Ant Colony Optimization
- Glover (1989) - Tabu Search

### Online Resources
- [Metaheuristics Network](http://www.metaheuristics.net/)
- [OR-Library Benchmarks](http://people.brunel.ac.uk/~mastjjb/jeb/info.html)

## ⚠️ Important Considerations

1. **No Free Lunch Theorem**: No single algorithm is best for all problems
2. **Parameter Tuning**: Performance heavily depends on parameter settings
3. **Hybrid Approaches**: Combining algorithms often yields better results
4. **Problem-Specific Knowledge**: Incorporate domain knowledge when possible
5. **Computational Budget**: Balance solution quality with time constraints

## 🤝 Contributing

Areas for expansion:
- Differential Evolution
- Harmony Search
- Artificial Bee Colony
- Firefly Algorithm
- Cuckoo Search
- Grey Wolf Optimizer

---

**Part of the Algorithms Multiverse** - A comprehensive collection of algorithms across multiple domains.

**Last Updated**: January 2026