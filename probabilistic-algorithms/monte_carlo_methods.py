"""
Monte Carlo Methods Implementation
==================================

A comprehensive collection of Monte Carlo algorithms for numerical computation,
simulation, and probabilistic problem solving using random sampling.

Algorithms Implemented:
- Monte Carlo Integration
- Pi Estimation
- Monte Carlo Tree Search (MCTS)
- Metropolis-Hastings Algorithm
- Importance Sampling
- Monte Carlo Matrix Operations
- Random Walk Methods
- Bootstrap Methods

Applications:
- Numerical integration
- Physics simulations
- Financial modeling
- Game AI
- Bayesian inference
- Option pricing

Author: Claude
Date: January 2026
"""

import numpy as np
import random
import math
from typing import Callable, List, Tuple, Dict, Optional, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from collections import defaultdict
import time


@dataclass
class MCTSNode:
    """Node for Monte Carlo Tree Search."""
    state: Any
    parent: Optional['MCTSNode'] = None
    children: List['MCTSNode'] = field(default_factory=list)
    visits: int = 0
    value: float = 0.0
    untried_actions: List[Any] = field(default_factory=list)


class MonteCarloIntegration:
    """
    Monte Carlo methods for numerical integration.

    Estimates definite integrals using random sampling.
    """

    @staticmethod
    def integrate_1d(f: Callable[[float], float],
                     a: float, b: float,
                     n_samples: int = 10000) -> Tuple[float, float]:
        """
        Estimate 1D integral using Monte Carlo.

        Args:
            f: Function to integrate
            a, b: Integration bounds
            n_samples: Number of samples

        Returns:
            Estimate and standard error
        """
        samples = np.random.uniform(a, b, n_samples)
        values = np.array([f(x) for x in samples])

        # Monte Carlo estimate
        estimate = (b - a) * np.mean(values)

        # Standard error
        std_error = (b - a) * np.std(values) / np.sqrt(n_samples)

        return estimate, std_error

    @staticmethod
    def integrate_multidimensional(f: Callable[[np.ndarray], float],
                                  bounds: List[Tuple[float, float]],
                                  n_samples: int = 10000) -> Tuple[float, float]:
        """
        Estimate multidimensional integral.

        Args:
            f: Function to integrate
            bounds: List of (min, max) for each dimension
            n_samples: Number of samples

        Returns:
            Estimate and standard error
        """
        dim = len(bounds)

        # Generate random samples
        samples = np.zeros((n_samples, dim))
        for i, (low, high) in enumerate(bounds):
            samples[:, i] = np.random.uniform(low, high, n_samples)

        # Evaluate function
        values = np.array([f(x) for x in samples])

        # Calculate volume
        volume = np.prod([high - low for low, high in bounds])

        # Monte Carlo estimate
        estimate = volume * np.mean(values)
        std_error = volume * np.std(values) / np.sqrt(n_samples)

        return estimate, std_error

    @staticmethod
    def stratified_sampling(f: Callable[[float], float],
                          a: float, b: float,
                          n_strata: int = 10,
                          samples_per_stratum: int = 100) -> Tuple[float, float]:
        """
        Stratified sampling for variance reduction.

        Args:
            f: Function to integrate
            a, b: Bounds
            n_strata: Number of strata
            samples_per_stratum: Samples per stratum

        Returns:
            Estimate and standard error
        """
        stratum_width = (b - a) / n_strata
        estimates = []

        for i in range(n_strata):
            stratum_start = a + i * stratum_width
            stratum_end = stratum_start + stratum_width

            samples = np.random.uniform(stratum_start, stratum_end, samples_per_stratum)
            stratum_mean = np.mean([f(x) for x in samples])
            estimates.append(stratum_mean * stratum_width)

        estimate = sum(estimates)
        std_error = np.std(estimates) / np.sqrt(n_strata)

        return estimate, std_error

    @staticmethod
    def importance_sampling(f: Callable[[float], float],
                          g: Callable[[float], float],
                          sample_g: Callable[[int], np.ndarray],
                          n_samples: int = 10000) -> Tuple[float, float]:
        """
        Importance sampling for variance reduction.

        Args:
            f: Target function
            g: Importance distribution PDF
            sample_g: Function to sample from g
            n_samples: Number of samples

        Returns:
            Estimate and standard error
        """
        samples = sample_g(n_samples)
        weights = np.array([f(x) / g(x) for x in samples])

        estimate = np.mean(weights)
        std_error = np.std(weights) / np.sqrt(n_samples)

        return estimate, std_error


class PiEstimation:
    """
    Various methods for estimating π using Monte Carlo.
    """

    @staticmethod
    def circle_method(n_samples: int = 10000) -> float:
        """
        Estimate π using unit circle in unit square.

        Args:
            n_samples: Number of random points

        Returns:
            Estimate of π
        """
        inside_circle = 0

        for _ in range(n_samples):
            x = random.random()
            y = random.random()

            if x*x + y*y <= 1:
                inside_circle += 1

        return 4 * inside_circle / n_samples

    @staticmethod
    def buffon_needle(n_samples: int = 10000,
                      needle_length: float = 1.0,
                      strip_width: float = 2.0) -> float:
        """
        Estimate π using Buffon's needle problem.

        Args:
            n_samples: Number of needle drops
            needle_length: Length of needle
            strip_width: Distance between parallel lines

        Returns:
            Estimate of π
        """
        if needle_length > strip_width:
            raise ValueError("Needle length must be <= strip width")

        crosses = 0

        for _ in range(n_samples):
            # Random position and angle
            center = random.uniform(0, strip_width / 2)
            angle = random.uniform(0, math.pi)

            # Check if needle crosses a line
            if center <= (needle_length / 2) * math.sin(angle):
                crosses += 1

        if crosses == 0:
            return 0

        return (2 * needle_length * n_samples) / (crosses * strip_width)

    @staticmethod
    def monte_carlo_series(n_samples: int = 10000) -> float:
        """
        Estimate π using Monte Carlo integration of arctan series.

        Returns:
            Estimate of π
        """
        # Integrate 4/(1+x²) from 0 to 1
        def f(x):
            return 4 / (1 + x*x)

        samples = np.random.uniform(0, 1, n_samples)
        values = [f(x) for x in samples]

        return np.mean(values)


class MonteCarloTreeSearch:
    """
    Monte Carlo Tree Search for game playing and decision making.
    """

    def __init__(self,
                 game_state: Any,
                 get_actions: Callable,
                 apply_action: Callable,
                 is_terminal: Callable,
                 evaluate: Callable,
                 exploration_constant: float = math.sqrt(2)):
        """
        Initialize MCTS.

        Args:
            game_state: Initial game state
            get_actions: Function to get available actions
            apply_action: Function to apply action to state
            is_terminal: Check if state is terminal
            evaluate: Evaluate terminal state
            exploration_constant: UCB exploration parameter
        """
        self.root = MCTSNode(state=game_state)
        self.get_actions = get_actions
        self.apply_action = apply_action
        self.is_terminal = is_terminal
        self.evaluate = evaluate
        self.exploration_constant = exploration_constant

    def search(self, n_simulations: int = 1000) -> Any:
        """
        Run MCTS simulations.

        Args:
            n_simulations: Number of simulations

        Returns:
            Best action
        """
        for _ in range(n_simulations):
            node = self._tree_policy(self.root)
            reward = self._default_policy(node.state)
            self._backup(node, reward)

        # Return best action
        return self._best_child(self.root, exploration_constant=0).state

    def _tree_policy(self, node: MCTSNode) -> MCTSNode:
        """Select node to expand using tree policy."""
        while not self.is_terminal(node.state):
            if node.untried_actions is None:
                node.untried_actions = self.get_actions(node.state)

            if node.untried_actions:
                return self._expand(node)
            else:
                node = self._best_child(node, self.exploration_constant)

        return node

    def _expand(self, node: MCTSNode) -> MCTSNode:
        """Expand tree with new child."""
        action = node.untried_actions.pop()
        new_state = self.apply_action(node.state, action)

        child = MCTSNode(state=new_state, parent=node)
        node.children.append(child)

        return child

    def _best_child(self, node: MCTSNode, exploration_constant: float) -> MCTSNode:
        """Select best child using UCB formula."""
        def ucb(child: MCTSNode) -> float:
            if child.visits == 0:
                return float('inf')

            exploitation = child.value / child.visits
            exploration = exploration_constant * math.sqrt(
                2 * math.log(node.visits) / child.visits
            )

            return exploitation + exploration

        return max(node.children, key=ucb)

    def _default_policy(self, state: Any) -> float:
        """Random rollout from state."""
        current_state = state

        while not self.is_terminal(current_state):
            actions = self.get_actions(current_state)
            if not actions:
                break

            action = random.choice(actions)
            current_state = self.apply_action(current_state, action)

        return self.evaluate(current_state)

    def _backup(self, node: MCTSNode, reward: float):
        """Backup reward through tree."""
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent


class MetropolisHastings:
    """
    Metropolis-Hastings algorithm for sampling from complex distributions.
    """

    def __init__(self,
                 target_distribution: Callable[[Any], float],
                 proposal_distribution: Callable[[Any], Any],
                 initial_state: Any):
        """
        Initialize Metropolis-Hastings sampler.

        Args:
            target_distribution: Target distribution (up to normalization)
            proposal_distribution: Proposal for new states
            initial_state: Initial state
        """
        self.target = target_distribution
        self.proposal = proposal_distribution
        self.current_state = initial_state
        self.samples = []
        self.accepted = 0
        self.rejected = 0

    def sample(self, n_samples: int,
              burn_in: int = 1000,
              thin: int = 1) -> List[Any]:
        """
        Generate samples using Metropolis-Hastings.

        Args:
            n_samples: Number of samples to generate
            burn_in: Number of burn-in samples to discard
            thin: Keep every thin-th sample

        Returns:
            List of samples
        """
        all_samples = []

        for i in range(burn_in + n_samples * thin):
            # Propose new state
            proposed_state = self.proposal(self.current_state)

            # Calculate acceptance ratio
            current_prob = self.target(self.current_state)
            proposed_prob = self.target(proposed_state)

            if current_prob == 0:
                acceptance_ratio = 1
            else:
                acceptance_ratio = min(1, proposed_prob / current_prob)

            # Accept or reject
            if random.random() < acceptance_ratio:
                self.current_state = proposed_state
                self.accepted += 1
            else:
                self.rejected += 1

            # Store sample
            if i >= burn_in and (i - burn_in) % thin == 0:
                all_samples.append(self.current_state)

        self.samples = all_samples
        return all_samples

    def get_acceptance_rate(self) -> float:
        """Get acceptance rate of proposals."""
        total = self.accepted + self.rejected
        if total == 0:
            return 0
        return self.accepted / total


class RandomWalkMethods:
    """
    Random walk algorithms for various applications.
    """

    @staticmethod
    def simple_random_walk_1d(n_steps: int,
                             step_size: float = 1.0,
                             bias: float = 0.5) -> np.ndarray:
        """
        1D random walk simulation.

        Args:
            n_steps: Number of steps
            step_size: Size of each step
            bias: Probability of moving right

        Returns:
            Position after each step
        """
        positions = np.zeros(n_steps + 1)

        for i in range(n_steps):
            if random.random() < bias:
                positions[i + 1] = positions[i] + step_size
            else:
                positions[i + 1] = positions[i] - step_size

        return positions

    @staticmethod
    def random_walk_2d(n_steps: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        2D random walk on grid.

        Args:
            n_steps: Number of steps

        Returns:
            X and Y coordinates
        """
        # Possible moves: up, down, left, right
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        x = np.zeros(n_steps + 1)
        y = np.zeros(n_steps + 1)

        for i in range(n_steps):
            dx, dy = random.choice(moves)
            x[i + 1] = x[i] + dx
            y[i + 1] = y[i] + dy

        return x, y

    @staticmethod
    def self_avoiding_walk(n_steps: int,
                          max_attempts: int = 1000) -> Optional[List[Tuple[int, int]]]:
        """
        Self-avoiding random walk on 2D grid.

        Args:
            n_steps: Target number of steps
            max_attempts: Maximum attempts to find valid walk

        Returns:
            Path if found, None otherwise
        """
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for _ in range(max_attempts):
            path = [(0, 0)]
            visited = {(0, 0)}

            for _ in range(n_steps):
                current = path[-1]
                valid_moves = []

                for dx, dy in moves:
                    next_pos = (current[0] + dx, current[1] + dy)
                    if next_pos not in visited:
                        valid_moves.append(next_pos)

                if not valid_moves:
                    break  # Dead end

                next_pos = random.choice(valid_moves)
                path.append(next_pos)
                visited.add(next_pos)

            if len(path) == n_steps + 1:
                return path

        return None

    @staticmethod
    def first_passage_time(target: int,
                          n_simulations: int = 1000,
                          max_steps: int = 10000) -> Tuple[float, float]:
        """
        Estimate first passage time to target in 1D random walk.

        Args:
            target: Target position
            n_simulations: Number of simulations
            max_steps: Maximum steps per simulation

        Returns:
            Mean and std of first passage time
        """
        passage_times = []

        for _ in range(n_simulations):
            position = 0
            for step in range(1, max_steps + 1):
                # Random walk step
                position += random.choice([-1, 1])

                if position == target:
                    passage_times.append(step)
                    break

        if not passage_times:
            return float('inf'), float('inf')

        return np.mean(passage_times), np.std(passage_times)


class MonteCarloOptimization:
    """
    Monte Carlo methods for optimization problems.
    """

    @staticmethod
    def random_search(objective: Callable[[np.ndarray], float],
                     bounds: List[Tuple[float, float]],
                     n_samples: int = 10000,
                     minimize: bool = True) -> Tuple[np.ndarray, float]:
        """
        Random search optimization.

        Args:
            objective: Objective function
            bounds: Variable bounds
            n_samples: Number of random samples
            minimize: Whether to minimize (vs maximize)

        Returns:
            Best solution and its objective value
        """
        dim = len(bounds)
        best_solution = None
        best_value = float('inf') if minimize else -float('inf')

        for _ in range(n_samples):
            # Generate random solution
            solution = np.zeros(dim)
            for i, (low, high) in enumerate(bounds):
                solution[i] = random.uniform(low, high)

            # Evaluate
            value = objective(solution)

            # Update best
            if (minimize and value < best_value) or (not minimize and value > best_value):
                best_value = value
                best_solution = solution.copy()

        return best_solution, best_value

    @staticmethod
    def cross_entropy_method(objective: Callable[[np.ndarray], float],
                           bounds: List[Tuple[float, float]],
                           n_samples: int = 100,
                           elite_frac: float = 0.2,
                           n_iterations: int = 50) -> Tuple[np.ndarray, float]:
        """
        Cross-entropy method for optimization.

        Args:
            objective: Objective function
            bounds: Variable bounds
            n_samples: Samples per iteration
            elite_frac: Fraction of elite samples
            n_iterations: Number of iterations

        Returns:
            Best solution and objective value
        """
        dim = len(bounds)
        n_elite = int(n_samples * elite_frac)

        # Initialize distribution parameters
        means = np.array([(low + high) / 2 for low, high in bounds])
        stds = np.array([(high - low) / 4 for low, high in bounds])

        best_solution = None
        best_value = float('inf')

        for iteration in range(n_iterations):
            # Sample from current distribution
            samples = np.zeros((n_samples, dim))
            for i in range(dim):
                samples[:, i] = np.random.normal(means[i], stds[i], n_samples)
                # Clip to bounds
                samples[:, i] = np.clip(samples[:, i], bounds[i][0], bounds[i][1])

            # Evaluate samples
            values = np.array([objective(s) for s in samples])

            # Select elite samples
            elite_indices = np.argsort(values)[:n_elite]
            elite_samples = samples[elite_indices]

            # Update distribution
            means = np.mean(elite_samples, axis=0)
            stds = np.std(elite_samples, axis=0)

            # Track best
            min_idx = np.argmin(values)
            if values[min_idx] < best_value:
                best_value = values[min_idx]
                best_solution = samples[min_idx].copy()

        return best_solution, best_value


class BootstrapMethods:
    """
    Bootstrap methods for statistical inference.
    """

    @staticmethod
    def bootstrap_confidence_interval(data: np.ndarray,
                                     statistic: Callable[[np.ndarray], float],
                                     n_bootstrap: int = 10000,
                                     confidence: float = 0.95) -> Tuple[float, float, float]:
        """
        Bootstrap confidence interval for a statistic.

        Args:
            data: Original data
            statistic: Statistic to compute
            n_bootstrap: Number of bootstrap samples
            confidence: Confidence level

        Returns:
            Point estimate and confidence interval
        """
        n = len(data)
        bootstrap_stats = []

        for _ in range(n_bootstrap):
            # Resample with replacement
            bootstrap_sample = np.random.choice(data, size=n, replace=True)
            bootstrap_stats.append(statistic(bootstrap_sample))

        # Point estimate
        point_estimate = statistic(data)

        # Percentile method for confidence interval
        alpha = 1 - confidence
        lower = np.percentile(bootstrap_stats, 100 * alpha / 2)
        upper = np.percentile(bootstrap_stats, 100 * (1 - alpha / 2))

        return point_estimate, lower, upper

    @staticmethod
    def bootstrap_hypothesis_test(data1: np.ndarray,
                                 data2: np.ndarray,
                                 statistic: Callable[[np.ndarray, np.ndarray], float],
                                 n_bootstrap: int = 10000) -> float:
        """
        Bootstrap hypothesis test for difference between groups.

        Args:
            data1, data2: Two data groups
            statistic: Test statistic
            n_bootstrap: Number of bootstrap samples

        Returns:
            P-value
        """
        observed_stat = statistic(data1, data2)

        # Combine data under null hypothesis
        combined = np.concatenate([data1, data2])
        n1, n2 = len(data1), len(data2)

        bootstrap_stats = []

        for _ in range(n_bootstrap):
            # Permute combined data
            permuted = np.random.permutation(combined)
            boot_data1 = permuted[:n1]
            boot_data2 = permuted[n1:]

            bootstrap_stats.append(statistic(boot_data1, boot_data2))

        # Calculate p-value
        p_value = np.mean(np.abs(bootstrap_stats) >= np.abs(observed_stat))

        return p_value


def integration_examples():
    """Examples of Monte Carlo integration."""
    print("=" * 60)
    print("MONTE CARLO INTEGRATION")
    print("=" * 60)

    mc = MonteCarloIntegration()

    # Example 1: Simple 1D integral
    print("\n1. Integrate x² from 0 to 1:")
    def f1(x):
        return x**2

    estimate, error = mc.integrate_1d(f1, 0, 1, n_samples=10000)
    exact = 1/3
    print(f"   Monte Carlo: {estimate:.6f} ± {error:.6f}")
    print(f"   Exact value: {exact:.6f}")
    print(f"   Error: {abs(estimate - exact):.6f}")

    # Example 2: Multidimensional integral
    print("\n2. Integrate exp(-(x²+y²)) over unit circle:")
    def f2(point):
        x, y = point
        if x**2 + y**2 <= 1:
            return math.exp(-(x**2 + y**2))
        return 0

    estimate, error = mc.integrate_multidimensional(
        f2, [(-1, 1), (-1, 1)], n_samples=50000
    )
    print(f"   Monte Carlo: {estimate:.6f} ± {error:.6f}")

    # Example 3: Stratified sampling
    print("\n3. Stratified sampling for sin(x) from 0 to π:")
    def f3(x):
        return math.sin(x)

    estimate_regular, error_regular = mc.integrate_1d(f3, 0, math.pi, n_samples=1000)
    estimate_stratified, error_stratified = mc.stratified_sampling(
        f3, 0, math.pi, n_strata=10, samples_per_stratum=100
    )

    print(f"   Regular MC: {estimate_regular:.6f} ± {error_regular:.6f}")
    print(f"   Stratified: {estimate_stratified:.6f} ± {error_stratified:.6f}")
    print(f"   Exact value: 2.0")


def pi_estimation_examples():
    """Examples of π estimation."""
    print("\n" + "=" * 60)
    print("PI ESTIMATION")
    print("=" * 60)

    pi_est = PiEstimation()

    # Different methods with increasing samples
    sample_sizes = [100, 1000, 10000, 100000]

    print("\nCircle Method:")
    for n in sample_sizes:
        estimate = pi_est.circle_method(n)
        error = abs(estimate - math.pi)
        print(f"   n={n:6d}: π ≈ {estimate:.6f}, error = {error:.6f}")

    print("\nBuffon's Needle:")
    for n in sample_sizes[:3]:  # Fewer samples as it's slower
        estimate = pi_est.buffon_needle(n)
        error = abs(estimate - math.pi)
        print(f"   n={n:6d}: π ≈ {estimate:.6f}, error = {error:.6f}")

    print("\nMonte Carlo Series:")
    for n in sample_sizes:
        estimate = pi_est.monte_carlo_series(n)
        error = abs(estimate - math.pi)
        print(f"   n={n:6d}: π ≈ {estimate:.6f}, error = {error:.6f}")


def random_walk_examples():
    """Examples of random walk methods."""
    print("\n" + "=" * 60)
    print("RANDOM WALK METHODS")
    print("=" * 60)

    rw = RandomWalkMethods()

    # 1D random walk
    print("\n1. 1D Random Walk (1000 steps):")
    positions = rw.simple_random_walk_1d(1000)
    print(f"   Final position: {positions[-1]:.0f}")
    print(f"   Max distance: {np.max(np.abs(positions)):.0f}")
    print(f"   RMS displacement: {np.sqrt(np.mean(positions**2)):.2f}")

    # 2D random walk
    print("\n2. 2D Random Walk (1000 steps):")
    x, y = rw.random_walk_2d(1000)
    final_distance = np.sqrt(x[-1]**2 + y[-1]**2)
    print(f"   Final position: ({x[-1]:.0f}, {y[-1]:.0f})")
    print(f"   Distance from origin: {final_distance:.2f}")

    # Self-avoiding walk
    print("\n3. Self-Avoiding Walk (50 steps):")
    path = rw.self_avoiding_walk(50)
    if path:
        print(f"   Success! Path length: {len(path)}")
        print(f"   Final position: {path[-1]}")
    else:
        print(f"   Failed to find valid path")

    # First passage time
    print("\n4. First Passage Time to position 10:")
    mean_time, std_time = rw.first_passage_time(10, n_simulations=1000)
    print(f"   Mean time: {mean_time:.1f} ± {std_time:.1f} steps")
    print(f"   Theoretical (1D): {10**2} steps")


def metropolis_hastings_example():
    """Example of Metropolis-Hastings sampling."""
    print("\n" + "=" * 60)
    print("METROPOLIS-HASTINGS SAMPLING")
    print("=" * 60)

    # Sample from a mixture of Gaussians
    def target(x):
        """Mixture of two Gaussians."""
        return (0.3 * math.exp(-0.5 * (x - 2)**2) +
                0.7 * math.exp(-0.5 * (x + 1)**2))

    def proposal(x):
        """Random walk proposal."""
        return x + random.gauss(0, 0.5)

    # Run sampler
    mh = MetropolisHastings(target, proposal, initial_state=0.0)
    samples = mh.sample(n_samples=10000, burn_in=1000)

    print(f"Generated {len(samples)} samples")
    print(f"Acceptance rate: {mh.get_acceptance_rate():.2%}")
    print(f"Sample mean: {np.mean(samples):.3f}")
    print(f"Sample std: {np.std(samples):.3f}")

    # Check convergence to target distribution
    # True mean is approximately 0.3*2 + 0.7*(-1) = -0.1
    print(f"Expected mean (approx): -0.1")


def optimization_example():
    """Example of Monte Carlo optimization."""
    print("\n" + "=" * 60)
    print("MONTE CARLO OPTIMIZATION")
    print("=" * 60)

    # Rastrigin function - many local minima
    def rastrigin(x):
        n = len(x)
        return 10 * n + sum(xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x)

    bounds = [(-5.12, 5.12)] * 5
    mc_opt = MonteCarloOptimization()

    # Random search
    print("\n1. Random Search (10000 samples):")
    solution, value = mc_opt.random_search(rastrigin, bounds, n_samples=10000)
    print(f"   Best solution: {solution}")
    print(f"   Best value: {value:.6f}")
    print(f"   Global minimum is 0 at origin")

    # Cross-entropy method
    print("\n2. Cross-Entropy Method:")
    solution, value = mc_opt.cross_entropy_method(
        rastrigin, bounds,
        n_samples=100,
        elite_frac=0.2,
        n_iterations=50
    )
    print(f"   Best solution: {solution}")
    print(f"   Best value: {value:.6f}")
    print(f"   Distance from global optimum: {np.linalg.norm(solution):.6f}")


def bootstrap_example():
    """Example of bootstrap methods."""
    print("\n" + "=" * 60)
    print("BOOTSTRAP METHODS")
    print("=" * 60)

    bootstrap = BootstrapMethods()

    # Generate sample data
    np.random.seed(42)
    data = np.random.exponential(2, 100)

    # Bootstrap confidence interval for mean
    print("\n1. Bootstrap CI for mean:")
    mean, lower, upper = bootstrap.bootstrap_confidence_interval(
        data, np.mean, n_bootstrap=10000
    )
    print(f"   Mean: {mean:.3f}")
    print(f"   95% CI: [{lower:.3f}, {upper:.3f}]")
    print(f"   True mean: 2.0")

    # Bootstrap hypothesis test
    print("\n2. Bootstrap hypothesis test:")
    data1 = np.random.normal(0, 1, 50)
    data2 = np.random.normal(0.5, 1, 50)

    def mean_diff(d1, d2):
        return np.mean(d1) - np.mean(d2)

    p_value = bootstrap.bootstrap_hypothesis_test(
        data1, data2, mean_diff, n_bootstrap=10000
    )
    print(f"   P-value: {p_value:.4f}")
    print(f"   Significant at α=0.05: {p_value < 0.05}")


if __name__ == "__main__":
    # Run examples
    integration_examples()
    pi_estimation_examples()
    random_walk_examples()
    metropolis_hastings_example()
    optimization_example()
    bootstrap_example()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Monte Carlo methods use randomness to solve deterministic problems")
    print("- Convergence rate is typically O(1/√n) independent of dimension")
    print("- Variance reduction techniques improve efficiency")
    print("- MCMC enables sampling from complex distributions")
    print("- Bootstrap provides distribution-free statistical inference")
    print("=" * 60)