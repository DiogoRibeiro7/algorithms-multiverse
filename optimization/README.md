# Optimization Algorithms

A comprehensive collection of metaheuristic and local search optimization algorithms for solving complex optimization problems.

## 📚 Table of Contents

- [Overview](#overview)
- [Implemented Algorithms](#implemented-algorithms)
- [Installation](#installation)
- [Algorithm Details](#algorithm-details)
- [Usage Examples](#usage-examples)
- [Algorithm Comparison](#algorithm-comparison)
- [Applications](#applications)
- [Performance Tips](#performance-tips)
- [References](#references)

## 🎯 Overview

This module provides educational implementations of various optimization algorithms, including evolutionary algorithms, swarm intelligence, and local search methods. These algorithms are designed to solve complex optimization problems where traditional methods may fail.

### Key Features

- **Multiple Algorithm Families**: Evolutionary, swarm-based, physics-inspired, and local search
- **Problem Type Support**: Continuous, discrete, binary, and combinatorial optimization
- **Variants and Extensions**: Multiple variants of each algorithm
- **Parallel Capabilities**: Support for parallel evaluation where applicable
- **Comprehensive Examples**: TSP, function optimization, knapsack, graph coloring

## 📊 Implemented Algorithms

### 1. Genetic Algorithms (`genetic_algorithm.py`)

| Algorithm | Description | Best For |
|-----------|-------------|----------|
| **Standard GA** | Classical genetic algorithm | General optimization |
| **Binary GA** | Specialized for binary problems | Feature selection, knapsack |
| **Real-Valued GA** | Continuous optimization | Function optimization |
| **TSP GA** | Specialized for TSP | Routing problems |
| **Multi-Objective GA** | Pareto optimization | Multi-criteria problems |

**Key Components:**
- Selection: Tournament, Roulette Wheel, Rank-based
- Crossover: Single-point, Two-point, Uniform, Arithmetic
- Mutation: Bit-flip, Gaussian, Polynomial, Adaptive
- Elitism and diversity preservation

### 2. Simulated Annealing (`simulated_annealing.py`)

| Variant | Description | Characteristics |
|---------|-------------|-----------------|
| **Standard SA** | Classic simulated annealing | Probabilistic acceptance |
| **Adaptive SA** | Dynamic temperature adjustment | Better convergence |
| **Fast SA** | Accelerated cooling | Quick solutions |
| **Parallel Tempering** | Multiple temperature chains | Enhanced exploration |
| **TSP SA** | Specialized for TSP | 2-opt, 3-opt moves |

**Cooling Schedules:**
- Linear, Exponential, Logarithmic
- Adaptive, Fast, Boltzmann
- Custom schedules supported

### 3. Particle Swarm Optimization (`particle_swarm.py`)

| Variant | Description | Features |
|---------|-------------|----------|
| **Standard PSO** | Classic particle swarm | Global/local best |
| **Quantum PSO** | Quantum-behaved particles | Better exploration |
| **Multi-Objective PSO** | Pareto optimization | Archive-based |
| **Adaptive PSO** | Time-varying parameters | Balanced search |

**Topologies:**
- Global, Ring, Von Neumann
- Random, Star
- Dynamic topology switching

### 4. Ant Colony Optimization (`ant_colony.py`)

| Variant | Description | Characteristics |
|---------|-------------|-----------------|
| **Ant System (AS)** | Original ACO | All ants deposit |
| **Ant Colony System (ACS)** | Enhanced ACO | Best ant only |
| **MAX-MIN AS** | Bounded pheromone | Prevents stagnation |
| **Rank-Based AS** | Ranked deposits | Elite ants |
| **Elitist AS** | Best-so-far reinforcement | Fast convergence |

**Applications:**
- TSP and routing problems
- Graph coloring
- Scheduling problems

### 5. Hill Climbing & Local Search (`hill_climbing.py`)

| Algorithm | Description | Properties |
|-----------|-------------|------------|
| **Simple HC** | First improvement | Fast, local |
| **Steepest Ascent** | Best improvement | Thorough search |
| **Stochastic HC** | Random selection | Escape plateaus |
| **Random Restart** | Multiple starts | Global search |
| **Tabu Search** | Memory-based | Avoid cycling |
| **VNS** | Variable neighborhoods | Systematic exploration |

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/algorithms-multiverse.git
cd algorithms-multiverse/optimization

# No external dependencies for basic functionality
# For enhanced features, install numpy
pip install numpy
```

## 💻 Usage Examples

### Example 1: Function Optimization with GA

```python
from genetic_algorithm import RealValuedGA
import numpy as np

# Define objective function (Rastrigin)
def rastrigin(x):
    n = len(x)
    return 10 * n + sum(xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x)

# Create and run GA
ga = RealValuedGA(
    fitness_function=rastrigin,
    bounds=[(-5.12, 5.12)] * 5,  # 5D problem
    population_size=50,
    max_generations=200,
    minimize=True
)

best_solution = ga.run(verbose=True)
print(f"Best solution: {best_solution.genes}")
print(f"Best fitness: {best_solution.fitness}")
```

### Example 2: TSP with Simulated Annealing

```python
from simulated_annealing import TSPSimulatedAnnealing
import numpy as np

# Create distance matrix
cities = np.random.rand(20, 2) * 100
distance_matrix = np.zeros((20, 20))
for i in range(20):
    for j in range(20):
        if i != j:
            distance_matrix[i][j] = np.linalg.norm(cities[i] - cities[j])

# Solve TSP
tsp_sa = TSPSimulatedAnnealing(
    distance_matrix=distance_matrix,
    cooling_rate=0.995,
    max_iterations=10000
)

best_tour, best_distance = tsp_sa.run()
print(f"Best tour distance: {best_distance}")
```

### Example 3: Multi-Objective Optimization with PSO

```python
from particle_swarm import MultiObjectivePSO

# Define multiple objectives
def objective1(x):
    return x[0]**2 + x[1]**2

def objective2(x):
    return (x[0] - 2)**2 + (x[1] - 2)**2

# Run multi-objective PSO
mopso = MultiObjectivePSO(
    objective_functions=[objective1, objective2],
    bounds=[(-5, 5), (-5, 5)],
    swarm_size=100,
    max_iterations=200
)

pareto_set = mopso.run()
print(f"Found {len(pareto_set)} Pareto-optimal solutions")
```

### Example 4: Combinatorial Optimization with ACO

```python
from ant_colony import AntColonyOptimization, ACOVariant

# TSP with ACO
aco = AntColonyOptimization(
    distance_matrix=distance_matrix,
    n_ants=20,
    n_iterations=100,
    variant=ACOVariant.MMAS,  # MAX-MIN Ant System
    local_search=LocalSearch.TWO_OPT
)

best_tour, best_length = aco.run()
print(f"Best tour found: {best_tour}")
print(f"Tour length: {best_length}")
```

### Example 5: Local Search with Tabu Search

```python
from hill_climbing import TabuSearch

# Define neighborhood function
def tsp_fitness(tour):
    return sum(distance_matrix[tour[i]][tour[(i+1)%len(tour)]]
               for i in range(len(tour)))

# Run Tabu Search
initial_tour = list(range(n_cities))
random.shuffle(initial_tour)

ts = TabuSearch(
    objective_function=tsp_fitness,
    initial_solution=initial_tour,
    tabu_tenure=20,
    max_iterations=500,
    problem_type="permutation"
)

best_tour, best_length = ts.run()
```

## 📈 Algorithm Comparison

### Continuous Optimization Performance

| Algorithm | Global Search | Local Search | Speed | Memory | Parallelizable |
|-----------|--------------|--------------|-------|--------|----------------|
| GA | Excellent | Good | Slow | High | Yes |
| SA | Good | Excellent | Medium | Low | No |
| PSO | Very Good | Good | Fast | Medium | Yes |
| ACO | Good | Good | Slow | High | Yes |
| Hill Climbing | Poor | Excellent | Very Fast | Low | No |
| Tabu Search | Good | Excellent | Fast | Medium | No |

### Problem Type Suitability

| Problem Type | Best Algorithms | Second Choice |
|--------------|-----------------|---------------|
| Continuous | PSO, GA | SA, VNS |
| Binary | Binary GA | Hill Climbing |
| Permutation (TSP) | ACO, SA | GA, Tabu Search |
| Multi-Objective | MOPSO, MOGA | Weighted Sum |
| Constrained | GA with penalties | PSO with repairs |
| Dynamic | PSO, Adaptive GA | ACO |

## 🔧 Performance Tips

### General Optimization

1. **Parameter Tuning**
   - Start with recommended defaults
   - Use grid search or meta-optimization
   - Balance exploration vs exploitation

2. **Problem-Specific Customization**
   - Design appropriate fitness functions
   - Choose suitable representations
   - Implement problem-specific operators

3. **Hybridization**
   - Combine global and local search
   - Use local search to refine solutions
   - Implement memetic algorithms

### Algorithm-Specific Tips

**Genetic Algorithms:**
- Population size: 50-200 typically
- Crossover rate: 0.7-0.9
- Mutation rate: 1/chromosome_length
- Use elitism (2-5% of population)

**Simulated Annealing:**
- Initial temperature: Accept 80% of moves initially
- Cooling rate: 0.95-0.99 for thorough search
- Use adaptive cooling for unknown landscapes

**Particle Swarm:**
- Swarm size: 20-50 particles
- w (inertia): 0.4-0.9 (decrease over time)
- c1, c2: Around 2.0
- Use constriction factor for stability

**Ant Colony:**
- Ants: Problem size / 2
- α (pheromone): 1.0
- β (heuristic): 2.0-5.0
- ρ (evaporation): 0.1-0.5

## 🎯 Applications

### Real-World Use Cases

1. **Engineering Design**
   - Structural optimization
   - Circuit design
   - Control system tuning

2. **Machine Learning**
   - Hyperparameter optimization
   - Feature selection
   - Neural architecture search

3. **Logistics & Operations**
   - Vehicle routing
   - Scheduling
   - Resource allocation

4. **Finance**
   - Portfolio optimization
   - Risk management
   - Trading strategies

5. **Bioinformatics**
   - Protein folding
   - Gene expression analysis
   - Drug design

## 📊 Benchmark Functions

The module includes implementations for testing on standard benchmark functions:

- **Sphere**: Simple unimodal
- **Rastrigin**: Highly multimodal
- **Rosenbrock**: Narrow valley
- **Ackley**: Many local optima
- **Griewank**: Product of cosines
- **Schwefel**: Deceptive

## 🔬 Advanced Features

### Constraint Handling
- Penalty methods
- Repair mechanisms
- Feasibility preservation

### Multi-Objective
- Pareto dominance
- Crowding distance
- Archive management

### Adaptive Mechanisms
- Parameter self-adaptation
- Operator selection
- Population sizing

## 📚 References

### Books
- "Introduction to Evolutionary Computing" - Eiben & Smith
- "Swarm Intelligence" - Kennedy & Eberhart
- "Ant Colony Optimization" - Dorigo & Stützle
- "Handbook of Metaheuristics" - Glover & Kochenberger

### Papers
- Holland (1975) - Genetic Algorithms
- Kirkpatrick et al. (1983) - Simulated Annealing
- Kennedy & Eberhart (1995) - Particle Swarm
- Dorigo et al. (1996) - Ant System
- Glover (1989) - Tabu Search

## ⚠️ Important Notes

1. **Educational Implementation**: These are simplified versions for learning
2. **No Free Lunch**: No single algorithm is best for all problems
3. **Parameter Sensitivity**: Performance heavily depends on parameters
4. **Problem Knowledge**: Use domain knowledge when available
5. **Hybridization**: Combining algorithms often improves results

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional algorithms (CMA-ES, DE, ABC)
- More problem-specific variants
- Parallel implementations
- Visualization tools
- Additional benchmark problems

---

**Part of the Algorithms Multiverse** - A comprehensive collection of algorithms across multiple domains.

**Last Updated**: January 2026