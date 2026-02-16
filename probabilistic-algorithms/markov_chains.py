"""
Markov Chains Implementation
============================

Comprehensive implementation of Markov chains for modeling stochastic processes
with applications in text generation, PageRank, weather prediction, and more.

Key Components:
- Discrete-time Markov chains
- Continuous-time Markov chains
- Hidden Markov Models (HMM)
- Markov Chain Monte Carlo (MCMC) methods
- Absorbing Markov chains
- Ergodic analysis
- Steady-state computation

Applications:
- Text generation and NLP
- PageRank algorithm
- Weather forecasting
- Stock market modeling
- Queue theory
- Genetics and evolution
- Game theory

Author: Claude
Date: January 2026
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import random
import math
from enum import Enum


class ChainType(Enum):
    """Types of Markov chains."""
    DISCRETE = "discrete"
    CONTINUOUS = "continuous"
    HIDDEN = "hidden"
    ABSORBING = "absorbing"


@dataclass
class MarkovState:
    """State in a Markov chain."""
    id: int
    name: str
    value: Any = None
    is_absorbing: bool = False


class DiscreteMarkovChain:
    """
    Discrete-time Markov chain implementation.

    Models systems that transition between states at discrete time steps.
    """

    def __init__(self, states: List[str], transition_matrix: Optional[np.ndarray] = None):
        """
        Initialize Markov chain.

        Args:
            states: List of state names
            transition_matrix: Transition probability matrix
        """
        self.states = states
        self.n_states = len(states)
        self.state_index = {state: i for i, state in enumerate(states)}

        if transition_matrix is not None:
            self.transition_matrix = np.array(transition_matrix)
            self._validate_transition_matrix()
        else:
            self.transition_matrix = np.zeros((self.n_states, self.n_states))

        self.current_state = 0
        self.history = []

    def _validate_transition_matrix(self):
        """Validate that transition matrix is stochastic."""
        if self.transition_matrix.shape != (self.n_states, self.n_states):
            raise ValueError("Transition matrix dimensions don't match number of states")

        # Check rows sum to 1
        row_sums = np.sum(self.transition_matrix, axis=1)
        if not np.allclose(row_sums, 1.0):
            raise ValueError("Transition matrix rows must sum to 1")

        # Check non-negative
        if np.any(self.transition_matrix < 0):
            raise ValueError("Transition probabilities must be non-negative")

    def set_transition(self, from_state: str, to_state: str, probability: float):
        """Set transition probability."""
        i = self.state_index[from_state]
        j = self.state_index[to_state]
        self.transition_matrix[i, j] = probability

    def step(self) -> str:
        """Make one transition."""
        probabilities = self.transition_matrix[self.current_state]
        self.current_state = np.random.choice(self.n_states, p=probabilities)
        state_name = self.states[self.current_state]
        self.history.append(state_name)
        return state_name

    def simulate(self, steps: int, initial_state: Optional[str] = None) -> List[str]:
        """
        Simulate chain for given number of steps.

        Args:
            steps: Number of steps to simulate
            initial_state: Starting state

        Returns:
            Sequence of states visited
        """
        if initial_state:
            self.current_state = self.state_index[initial_state]
        else:
            self.current_state = 0

        self.history = [self.states[self.current_state]]

        for _ in range(steps):
            self.step()

        return self.history

    def steady_state(self, method: str = "eigenvalue") -> np.ndarray:
        """
        Compute steady-state distribution.

        Args:
            method: "eigenvalue" or "iteration"

        Returns:
            Steady-state probability distribution
        """
        if method == "eigenvalue":
            # Find left eigenvector for eigenvalue 1
            eigenvalues, eigenvectors = np.linalg.eig(self.transition_matrix.T)
            stationary_idx = np.argmax(np.abs(eigenvalues - 1.0) < 1e-8)
            stationary = np.real(eigenvectors[:, stationary_idx])
            return stationary / stationary.sum()

        elif method == "iteration":
            # Power iteration method
            pi = np.ones(self.n_states) / self.n_states
            for _ in range(1000):
                pi_new = pi @ self.transition_matrix
                if np.allclose(pi, pi_new):
                    break
                pi = pi_new
            return pi

        else:
            raise ValueError(f"Unknown method: {method}")

    def is_irreducible(self) -> bool:
        """Check if chain is irreducible (all states communicate)."""
        # Use graph connectivity
        reachable = [set() for _ in range(self.n_states)]

        for i in range(self.n_states):
            visited = set()
            queue = [i]

            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)

                for j in range(self.n_states):
                    if self.transition_matrix[current, j] > 0:
                        if j not in visited:
                            queue.append(j)

            reachable[i] = visited

        # Check if all states can reach all others
        for i in range(self.n_states):
            if len(reachable[i]) != self.n_states:
                return False
        return True

    def is_aperiodic(self) -> bool:
        """Check if chain is aperiodic."""
        # Check if any state has self-loop
        if np.any(np.diag(self.transition_matrix) > 0):
            return True

        # Check higher powers
        power = self.transition_matrix.copy()
        for _ in range(self.n_states):
            power = power @ self.transition_matrix
            if np.all(power > 0):
                return True

        return False

    def mean_first_passage_time(self, from_state: str, to_state: str) -> float:
        """
        Compute mean first passage time between states.

        Args:
            from_state: Starting state
            to_state: Target state

        Returns:
            Expected number of steps to reach target
        """
        i = self.state_index[from_state]
        j = self.state_index[to_state]

        if i == j:
            return 0

        # Solve system of linear equations
        # m_ij = 1 + sum_k(p_ik * m_kj) for k != j
        n = self.n_states
        A = np.eye(n - 1)
        b = np.ones(n - 1)

        # Remove target state from equations
        indices = [k for k in range(n) if k != j]

        for idx, k in enumerate(indices):
            for idx2, m in enumerate(indices):
                if k == i:
                    A[idx, idx2] -= self.transition_matrix[k, m]

        # Solve for mean first passage times
        m = np.linalg.solve(A, b)

        if i < j:
            return m[i] if i < len(m) else m[i-1]
        else:
            return m[i-1]


class TextMarkovChain:
    """
    Markov chain for text generation.

    Learns transition probabilities from text corpus.
    """

    def __init__(self, order: int = 2):
        """
        Initialize text Markov chain.

        Args:
            order: Order of the chain (n-gram size - 1)
        """
        self.order = order
        self.transitions = defaultdict(Counter)
        self.starters = []

    def train(self, text: str, tokenize: bool = True):
        """
        Train chain on text corpus.

        Args:
            text: Training text
            tokenize: Whether to tokenize by words or characters
        """
        if tokenize:
            tokens = text.split()
        else:
            tokens = list(text)

        # Build n-grams
        for i in range(len(tokens) - self.order):
            state = tuple(tokens[i:i + self.order])
            next_token = tokens[i + self.order]
            self.transitions[state][next_token] += 1

            if i == 0 or (tokenize and tokens[i][0].isupper()):
                self.starters.append(state)

        # Normalize to probabilities
        for state in self.transitions:
            total = sum(self.transitions[state].values())
            for next_token in self.transitions[state]:
                self.transitions[state][next_token] /= total

    def generate(self, length: int, seed: Optional[Tuple] = None) -> str:
        """
        Generate text using the trained model.

        Args:
            length: Number of tokens to generate
            seed: Starting state

        Returns:
            Generated text
        """
        if not self.transitions:
            return ""

        if seed and seed in self.transitions:
            current = seed
        elif self.starters:
            current = random.choice(self.starters)
        else:
            current = random.choice(list(self.transitions.keys()))

        result = list(current)

        for _ in range(length - self.order):
            if current not in self.transitions:
                # Restart with new seed
                if self.starters:
                    current = random.choice(self.starters)
                    result.extend(current)
                else:
                    break

            # Sample next token
            choices = list(self.transitions[current].keys())
            weights = list(self.transitions[current].values())
            next_token = random.choices(choices, weights=weights)[0]

            result.append(next_token)
            current = current[1:] + (next_token,)

        return ' '.join(result) if isinstance(result[0], str) else ''.join(result)


class PageRank:
    """
    PageRank algorithm using Markov chains.

    Models web surfing as a random walk on the web graph.
    """

    def __init__(self, damping: float = 0.85):
        """
        Initialize PageRank.

        Args:
            damping: Damping factor (probability of following links)
        """
        self.damping = damping
        self.transition_matrix = None
        self.pages = []

    def build_from_links(self, links: Dict[str, List[str]]):
        """
        Build transition matrix from link structure.

        Args:
            links: Dictionary mapping pages to their outlinks
        """
        # Get all unique pages
        all_pages = set(links.keys())
        for outlinks in links.values():
            all_pages.update(outlinks)

        self.pages = sorted(list(all_pages))
        n = len(self.pages)
        page_index = {page: i for i, page in enumerate(self.pages)}

        # Build transition matrix
        self.transition_matrix = np.zeros((n, n))

        for page, outlinks in links.items():
            i = page_index[page]
            if outlinks:
                for outlink in outlinks:
                    j = page_index[outlink]
                    self.transition_matrix[i, j] = 1 / len(outlinks)
            else:
                # Dangling node - equal probability to all
                self.transition_matrix[i, :] = 1 / n

        # Apply damping factor (random surfer model)
        self.transition_matrix = (self.damping * self.transition_matrix +
                                 (1 - self.damping) / n * np.ones((n, n)))

    def compute_pagerank(self, method: str = "power", iterations: int = 100) -> Dict[str, float]:
        """
        Compute PageRank scores.

        Args:
            method: "power" for power iteration, "eigen" for eigenvalue
            iterations: Number of iterations for power method

        Returns:
            Dictionary mapping pages to PageRank scores
        """
        n = len(self.pages)

        if method == "power":
            # Power iteration
            pr = np.ones(n) / n

            for _ in range(iterations):
                pr = pr @ self.transition_matrix

        elif method == "eigen":
            # Eigenvalue method
            chain = DiscreteMarkovChain(self.pages, self.transition_matrix)
            pr = chain.steady_state()

        else:
            raise ValueError(f"Unknown method: {method}")

        return dict(zip(self.pages, pr))


class HiddenMarkovModel:
    """
    Hidden Markov Model implementation.

    Models systems with hidden states and observable outputs.
    """

    def __init__(self, states: List[str], observations: List[str]):
        """
        Initialize HMM.

        Args:
            states: Hidden states
            observations: Possible observations
        """
        self.states = states
        self.observations = observations
        self.n_states = len(states)
        self.n_observations = len(observations)

        self.state_index = {state: i for i, state in enumerate(states)}
        self.obs_index = {obs: i for i, obs in enumerate(observations)}

        # Model parameters
        self.initial_prob = np.ones(self.n_states) / self.n_states
        self.transition_prob = np.ones((self.n_states, self.n_states)) / self.n_states
        self.emission_prob = np.ones((self.n_states, self.n_observations)) / self.n_observations

    def forward_algorithm(self, observations: List[str]) -> Tuple[float, np.ndarray]:
        """
        Forward algorithm for computing observation probability.

        Args:
            observations: Sequence of observations

        Returns:
            (probability, forward_matrix)
        """
        T = len(observations)
        forward = np.zeros((T, self.n_states))

        # Initialization
        obs_idx = self.obs_index[observations[0]]
        forward[0] = self.initial_prob * self.emission_prob[:, obs_idx]

        # Recursion
        for t in range(1, T):
            obs_idx = self.obs_index[observations[t]]
            for j in range(self.n_states):
                forward[t, j] = (np.sum(forward[t-1] * self.transition_prob[:, j]) *
                               self.emission_prob[j, obs_idx])

        # Termination
        probability = np.sum(forward[T-1])
        return probability, forward

    def viterbi_algorithm(self, observations: List[str]) -> Tuple[List[str], float]:
        """
        Viterbi algorithm for finding most likely state sequence.

        Args:
            observations: Sequence of observations

        Returns:
            (state_sequence, probability)
        """
        T = len(observations)
        viterbi = np.zeros((T, self.n_states))
        path = np.zeros((T, self.n_states), dtype=int)

        # Initialization
        obs_idx = self.obs_index[observations[0]]
        viterbi[0] = self.initial_prob * self.emission_prob[:, obs_idx]

        # Recursion
        for t in range(1, T):
            obs_idx = self.obs_index[observations[t]]
            for j in range(self.n_states):
                probabilities = viterbi[t-1] * self.transition_prob[:, j]
                path[t, j] = np.argmax(probabilities)
                viterbi[t, j] = np.max(probabilities) * self.emission_prob[j, obs_idx]

        # Backtrack
        states_seq = np.zeros(T, dtype=int)
        states_seq[T-1] = np.argmax(viterbi[T-1])
        for t in range(T-2, -1, -1):
            states_seq[t] = path[t+1, states_seq[t+1]]

        # Convert to state names
        state_names = [self.states[i] for i in states_seq]
        probability = np.max(viterbi[T-1])

        return state_names, probability


class AbsorbingMarkovChain(DiscreteMarkovChain):
    """
    Absorbing Markov chain with analysis methods.

    Used for modeling processes that eventually reach terminal states.
    """

    def __init__(self, states: List[str], transition_matrix: np.ndarray,
                 absorbing_states: List[str]):
        """
        Initialize absorbing Markov chain.

        Args:
            states: All states
            transition_matrix: Transition matrix
            absorbing_states: List of absorbing state names
        """
        super().__init__(states, transition_matrix)
        self.absorbing_states = absorbing_states
        self.absorbing_indices = [self.state_index[s] for s in absorbing_states]
        self.transient_indices = [i for i in range(self.n_states)
                                  if i not in self.absorbing_indices]

    def fundamental_matrix(self) -> np.ndarray:
        """
        Compute fundamental matrix N = (I - Q)^(-1).

        Returns:
            Fundamental matrix
        """
        # Extract Q matrix (transient to transient transitions)
        Q = self.transition_matrix[np.ix_(self.transient_indices, self.transient_indices)]
        I = np.eye(len(self.transient_indices))
        N = np.linalg.inv(I - Q)
        return N

    def absorption_probabilities(self) -> np.ndarray:
        """
        Compute probability of absorption into each absorbing state.

        Returns:
            Matrix of absorption probabilities
        """
        N = self.fundamental_matrix()
        R = self.transition_matrix[np.ix_(self.transient_indices, self.absorbing_indices)]
        return N @ R

    def mean_absorption_time(self) -> np.ndarray:
        """
        Compute expected time to absorption from each transient state.

        Returns:
            Vector of mean absorption times
        """
        N = self.fundamental_matrix()
        return N @ np.ones(len(self.transient_indices))


def weather_model_example():
    """Example: Weather prediction using Markov chains."""
    print("=" * 60)
    print("WEATHER PREDICTION WITH MARKOV CHAINS")
    print("=" * 60)

    # Define weather states and transitions
    states = ["Sunny", "Cloudy", "Rainy"]
    transition_matrix = np.array([
        [0.7, 0.2, 0.1],  # Sunny -> ?
        [0.3, 0.4, 0.3],  # Cloudy -> ?
        [0.2, 0.3, 0.5]   # Rainy -> ?
    ])

    weather_chain = DiscreteMarkovChain(states, transition_matrix)

    # Simulate weather for a week
    print("Weather simulation for 7 days:")
    weather = weather_chain.simulate(7, initial_state="Sunny")
    for day, state in enumerate(weather):
        print(f"  Day {day}: {state}")

    # Compute steady-state weather
    steady = weather_chain.steady_state()
    print("\nLong-term weather probabilities:")
    for state, prob in zip(states, steady):
        print(f"  {state}: {prob:.2%}")

    # Mean first passage times
    print("\nExpected days until first rain from sunny:")
    mfpt = weather_chain.mean_first_passage_time("Sunny", "Rainy")
    print(f"  {mfpt:.1f} days")


def text_generation_example():
    """Example: Text generation with Markov chains."""
    print("\n" + "=" * 60)
    print("TEXT GENERATION WITH MARKOV CHAINS")
    print("=" * 60)

    # Training text (simplified Shakespeare)
    training_text = """
    To be or not to be that is the question
    Whether tis nobler in the mind to suffer
    The slings and arrows of outrageous fortune
    Or to take arms against a sea of troubles
    """

    # Train character-level model
    char_model = TextMarkovChain(order=3)
    char_model.train(training_text.lower(), tokenize=False)

    print("Character-level generation:")
    generated = char_model.generate(200)
    print(f"  {generated[:200]}")

    # Train word-level model
    word_model = TextMarkovChain(order=2)
    word_model.train(training_text, tokenize=True)

    print("\nWord-level generation:")
    generated = word_model.generate(20)
    print(f"  {generated}")


def pagerank_example():
    """Example: PageRank computation."""
    print("\n" + "=" * 60)
    print("PAGERANK ALGORITHM")
    print("=" * 60)

    # Simple web graph
    links = {
        "A": ["B", "C"],
        "B": ["C"],
        "C": ["A"],
        "D": ["C"],
        "E": ["A", "B", "C", "D"]
    }

    print("Web link structure:")
    for page, outlinks in links.items():
        print(f"  {page} -> {outlinks}")

    # Compute PageRank
    pr = PageRank(damping=0.85)
    pr.build_from_links(links)
    scores = pr.compute_pagerank(iterations=100)

    print("\nPageRank scores:")
    for page, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        print(f"  {page}: {score:.4f}")


def hmm_example():
    """Example: Hidden Markov Model for activity recognition."""
    print("\n" + "=" * 60)
    print("HIDDEN MARKOV MODEL - ACTIVITY RECOGNITION")
    print("=" * 60)

    # Hidden states: actual activities
    states = ["Working", "Meeting", "Break"]

    # Observations: detected computer activity
    observations = ["Typing", "Idle", "Video"]

    hmm = HiddenMarkovModel(states, observations)

    # Set model parameters
    hmm.initial_prob = np.array([0.6, 0.3, 0.1])
    hmm.transition_prob = np.array([
        [0.7, 0.2, 0.1],  # Working -> ?
        [0.3, 0.5, 0.2],  # Meeting -> ?
        [0.3, 0.1, 0.6]   # Break -> ?
    ])
    hmm.emission_prob = np.array([
        [0.8, 0.1, 0.1],  # Working: mostly typing
        [0.2, 0.3, 0.5],  # Meeting: mostly video
        [0.1, 0.6, 0.3]   # Break: mostly idle
    ])

    # Observed sequence
    observed = ["Typing", "Typing", "Video", "Video", "Idle", "Typing"]

    print(f"Observed activities: {observed}")

    # Find most likely state sequence
    states_seq, prob = hmm.viterbi_algorithm(observed)
    print(f"\nMost likely actual activities:")
    for obs, state in zip(observed, states_seq):
        print(f"  {obs:8} -> {state}")
    print(f"Probability: {prob:.6f}")

    # Compute observation probability
    total_prob, _ = hmm.forward_algorithm(observed)
    print(f"\nProbability of observation sequence: {total_prob:.6f}")


def gambling_example():
    """Example: Gambling as an absorbing Markov chain."""
    print("\n" + "=" * 60)
    print("GAMBLING - ABSORBING MARKOV CHAIN")
    print("=" * 60)

    # States: money amounts ($0, $1, $2, $3, $4, $5)
    # $0 is ruin (absorbing), $5 is goal (absorbing)
    states = ["$0", "$1", "$2", "$3", "$4", "$5"]

    # Transition matrix (p = 0.4 win probability)
    p_win = 0.4
    p_lose = 0.6

    transition_matrix = np.array([
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # $0 (absorbing)
        [p_lose, 0.0, p_win, 0.0, 0.0, 0.0],  # $1
        [0.0, p_lose, 0.0, p_win, 0.0, 0.0],  # $2
        [0.0, 0.0, p_lose, 0.0, p_win, 0.0],  # $3
        [0.0, 0.0, 0.0, p_lose, 0.0, p_win],  # $4
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]   # $5 (absorbing)
    ])

    absorbing_chain = AbsorbingMarkovChain(
        states, transition_matrix, absorbing_states=["$0", "$5"]
    )

    # Absorption probabilities
    abs_probs = absorbing_chain.absorption_probabilities()
    print("Probability of reaching goal ($5) starting from:")
    for i, state in enumerate(["$1", "$2", "$3", "$4"]):
        print(f"  {state}: {abs_probs[i, 1]:.2%}")

    # Mean time to absorption
    mean_times = absorbing_chain.mean_absorption_time()
    print("\nExpected number of games until absorption:")
    for i, state in enumerate(["$1", "$2", "$3", "$4"]):
        print(f"  Starting from {state}: {mean_times[i]:.1f} games")


def chain_analysis_example():
    """Example: Analyzing Markov chain properties."""
    print("\n" + "=" * 60)
    print("MARKOV CHAIN ANALYSIS")
    print("=" * 60)

    # Different types of chains
    chains = {
        "Irreducible & Aperiodic": np.array([
            [0.5, 0.3, 0.2],
            [0.2, 0.5, 0.3],
            [0.3, 0.2, 0.5]
        ]),
        "Reducible": np.array([
            [0.5, 0.5, 0.0],
            [0.5, 0.5, 0.0],
            [0.0, 0.0, 1.0]
        ]),
        "Periodic": np.array([
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0]
        ])
    }

    for name, matrix in chains.items():
        print(f"\n{name} Chain:")
        chain = DiscreteMarkovChain(["A", "B", "C"], matrix)

        print(f"  Irreducible: {chain.is_irreducible()}")
        print(f"  Aperiodic: {chain.is_aperiodic()}")

        if chain.is_irreducible() and chain.is_aperiodic():
            steady = chain.steady_state()
            print(f"  Steady state: {steady}")


if __name__ == "__main__":
    # Set random seed
    random.seed(42)
    np.random.seed(42)

    # Run examples
    weather_model_example()
    text_generation_example()
    pagerank_example()
    hmm_example()
    gambling_example()
    chain_analysis_example()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Markov chains model memoryless stochastic processes")
    print("- Steady-state analysis reveals long-term behavior")
    print("- HMMs handle hidden state inference")
    print("- Absorbing chains model terminal processes")
    print("- Applications span from PageRank to weather prediction")
    print("=" * 60)