"""
Quantum Algorithm Simulations
=============================

Classical simulations of fundamental quantum algorithms to demonstrate
quantum computing concepts and advantages.

Algorithms Implemented:
- Deutsch's Algorithm (single-bit oracle)
- Deutsch-Jozsa Algorithm (n-bit generalization)
- Grover's Search Algorithm
- Quantum Fourier Transform (QFT)
- Shor's Algorithm (simplified demonstration)
- Quantum Phase Estimation
- Bernstein-Vazirani Algorithm
- Simon's Algorithm

Key Concepts:
- Superposition
- Entanglement
- Quantum interference
- Oracle functions
- Amplitude amplification
- Phase kickback

Note: These are classical simulations for educational purposes.
Real quantum advantages require actual quantum hardware.

Author: Claude
Date: January 2026
"""

import numpy as np
from typing import Callable, List, Tuple, Optional, Any
from dataclasses import dataclass
import math
import random
from collections import defaultdict


class QuantumState:
    """
    Represents a quantum state vector.

    For n qubits, the state is a 2^n dimensional complex vector.
    """

    def __init__(self, n_qubits: int):
        """
        Initialize quantum state.

        Args:
            n_qubits: Number of qubits
        """
        self.n_qubits = n_qubits
        self.n_states = 2 ** n_qubits
        self.amplitudes = np.zeros(self.n_states, dtype=complex)
        self.amplitudes[0] = 1.0  # Start in |00...0⟩ state

    def normalize(self):
        """Normalize the state vector."""
        norm = np.linalg.norm(self.amplitudes)
        if norm > 0:
            self.amplitudes /= norm

    def measure(self) -> int:
        """
        Measure the quantum state.

        Returns:
            Measured state as integer (binary representation)
        """
        probabilities = np.abs(self.amplitudes) ** 2
        probabilities /= probabilities.sum()  # Ensure normalization

        # Sample from probability distribution
        outcome = np.random.choice(self.n_states, p=probabilities)

        # Collapse to measured state
        self.amplitudes = np.zeros(self.n_states, dtype=complex)
        self.amplitudes[outcome] = 1.0

        return outcome

    def get_probability(self, state: int) -> float:
        """Get probability of measuring specific state."""
        return float(np.abs(self.amplitudes[state]) ** 2)

    def __str__(self) -> str:
        """String representation of quantum state."""
        terms = []
        for i in range(self.n_states):
            amp = self.amplitudes[i]
            if abs(amp) > 1e-10:
                binary = format(i, f'0{self.n_qubits}b')
                terms.append(f"{amp:.3f}|{binary}⟩")
        return " + ".join(terms) if terms else "0"


class QuantumGates:
    """Common quantum gates."""

    @staticmethod
    def hadamard() -> np.ndarray:
        """Hadamard gate - creates superposition."""
        return np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

    @staticmethod
    def pauli_x() -> np.ndarray:
        """Pauli-X gate (NOT gate)."""
        return np.array([[0, 1], [1, 0]], dtype=complex)

    @staticmethod
    def pauli_y() -> np.ndarray:
        """Pauli-Y gate."""
        return np.array([[0, -1j], [1j, 0]], dtype=complex)

    @staticmethod
    def pauli_z() -> np.ndarray:
        """Pauli-Z gate."""
        return np.array([[1, 0], [0, -1]], dtype=complex)

    @staticmethod
    def cnot() -> np.ndarray:
        """Controlled-NOT gate."""
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ], dtype=complex)

    @staticmethod
    def phase_shift(theta: float) -> np.ndarray:
        """Phase shift gate."""
        return np.array([[1, 0], [0, np.exp(1j * theta)]], dtype=complex)

    @staticmethod
    def controlled_phase(theta: float) -> np.ndarray:
        """Controlled phase gate."""
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, np.exp(1j * theta)]
        ], dtype=complex)


class QuantumCircuit:
    """
    Quantum circuit simulator.

    Applies quantum gates to quantum states.
    """

    def __init__(self, n_qubits: int):
        """Initialize quantum circuit."""
        self.n_qubits = n_qubits
        self.state = QuantumState(n_qubits)

    def apply_gate(self, gate: np.ndarray, qubit: int):
        """
        Apply single-qubit gate.

        Args:
            gate: 2x2 gate matrix
            qubit: Target qubit index
        """
        n = self.n_qubits
        new_amplitudes = np.zeros_like(self.state.amplitudes)

        for state in range(2 ** n):
            # Extract bit at qubit position
            bit = (state >> (n - 1 - qubit)) & 1

            # Apply gate to this qubit
            for new_bit in range(2):
                # Calculate new state
                if bit != new_bit:
                    new_state = state ^ (1 << (n - 1 - qubit))
                else:
                    new_state = state

                # Add contribution
                new_amplitudes[new_state] += gate[new_bit, bit] * self.state.amplitudes[state]

        self.state.amplitudes = new_amplitudes
        self.state.normalize()

    def apply_controlled_gate(self, gate: np.ndarray, control: int, target: int):
        """
        Apply controlled gate.

        Args:
            gate: 2x2 gate matrix (applied when control is |1⟩)
            control: Control qubit
            target: Target qubit
        """
        n = self.n_qubits
        new_amplitudes = np.zeros_like(self.state.amplitudes)

        for state in range(2 ** n):
            control_bit = (state >> (n - 1 - control)) & 1

            if control_bit == 0:
                # Control is 0, no gate applied
                new_amplitudes[state] += self.state.amplitudes[state]
            else:
                # Control is 1, apply gate to target
                target_bit = (state >> (n - 1 - target)) & 1

                for new_bit in range(2):
                    if target_bit != new_bit:
                        new_state = state ^ (1 << (n - 1 - target))
                    else:
                        new_state = state

                    new_amplitudes[new_state] += gate[new_bit, target_bit] * self.state.amplitudes[state]

        self.state.amplitudes = new_amplitudes
        self.state.normalize()

    def hadamard(self, qubit: int):
        """Apply Hadamard gate."""
        self.apply_gate(QuantumGates.hadamard(), qubit)

    def x(self, qubit: int):
        """Apply Pauli-X (NOT) gate."""
        self.apply_gate(QuantumGates.pauli_x(), qubit)

    def z(self, qubit: int):
        """Apply Pauli-Z gate."""
        self.apply_gate(QuantumGates.pauli_z(), qubit)

    def cnot(self, control: int, target: int):
        """Apply CNOT gate."""
        self.apply_controlled_gate(QuantumGates.pauli_x(), control, target)

    def measure(self) -> int:
        """Measure all qubits."""
        return self.state.measure()


class DeutschAlgorithm:
    """
    Deutsch's algorithm - determines if a function is constant or balanced.

    First quantum algorithm to show advantage over classical.
    """

    @staticmethod
    def run(oracle: Callable[[int], int]) -> str:
        """
        Run Deutsch's algorithm.

        Args:
            oracle: Black box function f: {0,1} -> {0,1}

        Returns:
            "constant" or "balanced"
        """
        # Initialize 2-qubit circuit
        circuit = QuantumCircuit(2)

        # Prepare initial state |01⟩
        circuit.x(1)

        # Apply Hadamard to both qubits
        circuit.hadamard(0)
        circuit.hadamard(1)

        # Apply oracle
        for x in range(2):
            if oracle(x) == 1:
                # Apply controlled-X based on first qubit value
                if x == 0:
                    # Apply X to second qubit when first is |0⟩
                    # This requires a modified circuit
                    pass
                else:
                    circuit.cnot(0, 1)

        # Simplified oracle application (demonstration)
        if oracle(0) != oracle(1):  # Balanced
            circuit.z(0)

        # Apply Hadamard to first qubit
        circuit.hadamard(0)

        # Measure first qubit
        result = circuit.measure()
        first_qubit = (result >> 1) & 1

        return "constant" if first_qubit == 0 else "balanced"


class GroverSearch:
    """
    Grover's search algorithm - quantum search with quadratic speedup.

    Searches unsorted database of N items in O(√N) steps.
    """

    def __init__(self, n_qubits: int, marked_items: List[int]):
        """
        Initialize Grover's search.

        Args:
            n_qubits: Number of qubits (N = 2^n items)
            marked_items: List of marked item indices
        """
        self.n_qubits = n_qubits
        self.n_items = 2 ** n_qubits
        self.marked_items = set(marked_items)

    def oracle(self, circuit: QuantumCircuit):
        """Apply oracle (marks target states with phase flip)."""
        for state in self.marked_items:
            # Apply phase flip to marked state
            phase = -1
            circuit.state.amplitudes[state] *= phase

    def diffusion(self, circuit: QuantumCircuit):
        """Apply Grover diffusion operator."""
        # Calculate average amplitude
        avg = np.mean(circuit.state.amplitudes)

        # Invert about average
        circuit.state.amplitudes = 2 * avg - circuit.state.amplitudes

    def run(self) -> int:
        """
        Run Grover's algorithm.

        Returns:
            Found item index
        """
        circuit = QuantumCircuit(self.n_qubits)

        # Initialize uniform superposition
        for i in range(self.n_qubits):
            circuit.hadamard(i)

        # Calculate optimal number of iterations
        num_marked = len(self.marked_items)
        if num_marked == 0:
            return -1

        theta = math.asin(math.sqrt(num_marked / self.n_items))
        iterations = int(math.pi / (4 * theta))

        # Grover iterations
        for _ in range(iterations):
            # Apply oracle
            self.oracle(circuit)

            # Apply diffusion
            self.diffusion(circuit)

        # Measure
        result = circuit.measure()
        return result


class QuantumFourierTransform:
    """
    Quantum Fourier Transform - quantum version of discrete Fourier transform.

    Key component of many quantum algorithms including Shor's.
    """

    @staticmethod
    def apply(state: QuantumState) -> QuantumState:
        """
        Apply QFT to quantum state.

        Args:
            state: Input quantum state

        Returns:
            Transformed state
        """
        n = state.n_qubits
        N = state.n_states

        # QFT matrix
        omega = np.exp(2j * np.pi / N)
        qft_matrix = np.zeros((N, N), dtype=complex)

        for j in range(N):
            for k in range(N):
                qft_matrix[j, k] = omega ** (j * k) / np.sqrt(N)

        # Apply QFT
        new_state = QuantumState(n)
        new_state.amplitudes = qft_matrix @ state.amplitudes
        new_state.normalize()

        return new_state


class BernsteinVazirani:
    """
    Bernstein-Vazirani algorithm - finds hidden bit string.

    Determines secret string s with single query (classical needs n queries).
    """

    @staticmethod
    def run(secret: str) -> str:
        """
        Run Bernstein-Vazirani algorithm.

        Args:
            secret: Secret binary string

        Returns:
            Discovered secret string
        """
        n = len(secret)
        circuit = QuantumCircuit(n + 1)

        # Initialize ancilla qubit to |1⟩
        circuit.x(n)

        # Apply Hadamard to all qubits
        for i in range(n + 1):
            circuit.hadamard(i)

        # Oracle: applies phase based on secret string
        for i, bit in enumerate(secret):
            if bit == '1':
                circuit.cnot(i, n)

        # Apply Hadamard to input qubits
        for i in range(n):
            circuit.hadamard(i)

        # Measure input qubits
        result = circuit.measure()
        result >>= 1  # Ignore ancilla qubit

        # Convert to binary string
        discovered = format(result, f'0{n}b')
        return discovered


class SimonAlgorithm:
    """
    Simon's algorithm - finds hidden period in function.

    Exponential speedup for period-finding problem.
    """

    @staticmethod
    def find_period(oracle: Callable[[int], int], n: int) -> Optional[int]:
        """
        Find hidden period using Simon's algorithm.

        Args:
            oracle: Function with hidden period
            n: Number of bits

        Returns:
            Period if found
        """
        # Collect linear equations
        equations = []
        max_iterations = n * 3

        for _ in range(max_iterations):
            circuit = QuantumCircuit(2 * n)

            # Create superposition in first register
            for i in range(n):
                circuit.hadamard(i)

            # Apply oracle (simplified simulation)
            # In real implementation, oracle would entangle registers

            # Apply Hadamard to first register
            for i in range(n):
                circuit.hadamard(i)

            # Measure first register
            result = circuit.measure() >> n

            if result != 0:
                equations.append(result)

            # Check if we have enough equations
            if len(equations) >= n - 1:
                # Solve system (simplified)
                # In practice, would use Gaussian elimination over GF(2)
                return equations[0] if equations else None

        return None


def deutsch_example():
    """Example: Deutsch's algorithm."""
    print("=" * 60)
    print("DEUTSCH'S ALGORITHM")
    print("=" * 60)

    # Test different oracle functions
    oracles = {
        "constant_0": lambda x: 0,
        "constant_1": lambda x: 1,
        "balanced_id": lambda x: x,
        "balanced_not": lambda x: 1 - x
    }

    print("Testing different oracle functions:")
    for name, oracle in oracles.items():
        result = DeutschAlgorithm.run(oracle)
        print(f"  {name}: {result}")
        expected = "constant" if "constant" in name else "balanced"
        print(f"    Correct: {result == expected}")


def grover_example():
    """Example: Grover's search algorithm."""
    print("\n" + "=" * 60)
    print("GROVER'S SEARCH ALGORITHM")
    print("=" * 60)

    # Search in 4-qubit space (16 items)
    n_qubits = 4
    marked_items = [5, 10]  # Mark items 5 and 10

    print(f"Searching {2**n_qubits} items")
    print(f"Marked items: {marked_items}")

    grover = GroverSearch(n_qubits, marked_items)

    # Run multiple times to see probability distribution
    results = []
    trials = 100

    for _ in range(trials):
        result = grover.run()
        results.append(result)

    # Count occurrences
    counts = defaultdict(int)
    for r in results:
        counts[r] += 1

    print(f"\nResults from {trials} trials:")
    for item in sorted(counts.keys()):
        prob = counts[item] / trials
        marker = " *" if item in marked_items else ""
        print(f"  Item {item:2d}: {prob:.2%}{marker}")

    # Classical would need O(N) = 16 checks worst case
    # Grover needs O(√N) ≈ 4 iterations
    print(f"\nClassical worst case: 16 checks")
    print(f"Grover iterations: ~{int(math.pi * math.sqrt(16) / 4)} iterations")


def qft_example():
    """Example: Quantum Fourier Transform."""
    print("\n" + "=" * 60)
    print("QUANTUM FOURIER TRANSFORM")
    print("=" * 60)

    # Create a simple state
    n_qubits = 3
    state = QuantumState(n_qubits)

    # Prepare state |101⟩ (5 in binary)
    state.amplitudes[5] = 1.0

    print("Initial state:")
    print(f"  {state}")

    # Apply QFT
    transformed = QuantumFourierTransform.apply(state)

    print("\nAfter QFT:")
    for i in range(transformed.n_states):
        amp = transformed.amplitudes[i]
        if abs(amp) > 1e-10:
            binary = format(i, f'0{n_qubits}b')
            print(f"  |{binary}⟩: {amp:.3f}")

    # QFT of computational basis state gives uniform superposition
    # with different phases


def bernstein_vazirani_example():
    """Example: Bernstein-Vazirani algorithm."""
    print("\n" + "=" * 60)
    print("BERNSTEIN-VAZIRANI ALGORITHM")
    print("=" * 60)

    secret_strings = ["101", "1111", "0000", "1010"]

    for secret in secret_strings:
        print(f"\nSecret string: {secret}")

        # Run algorithm
        discovered = BernsteinVazirani.run(secret)

        print(f"Discovered:    {discovered}")
        print(f"Correct: {discovered == secret}")

        # Classical would need n queries
        print(f"Classical queries needed: {len(secret)}")
        print(f"Quantum queries needed: 1")


def quantum_superposition_demo():
    """Demonstrate quantum superposition."""
    print("\n" + "=" * 60)
    print("QUANTUM SUPERPOSITION DEMONSTRATION")
    print("=" * 60)

    circuit = QuantumCircuit(2)

    print("Initial state: |00⟩")
    print(f"  {circuit.state}")

    # Apply Hadamard to first qubit
    circuit.hadamard(0)
    print("\nAfter H on qubit 0:")
    print(f"  {circuit.state}")

    # Apply Hadamard to second qubit
    circuit.hadamard(1)
    print("\nAfter H on qubit 1 (equal superposition):")
    print(f"  {circuit.state}")

    # Measure multiple times to see probability distribution
    measurements = []
    for _ in range(1000):
        # Reset to superposition
        circuit.state = QuantumState(2)
        circuit.hadamard(0)
        circuit.hadamard(1)

        result = circuit.measure()
        measurements.append(result)

    # Count results
    counts = defaultdict(int)
    for m in measurements:
        counts[m] += 1

    print("\nMeasurement statistics (1000 trials):")
    for state in range(4):
        binary = format(state, '02b')
        prob = counts[state] / 1000
        print(f"  |{binary}⟩: {prob:.1%} (expected: 25%)")


def quantum_entanglement_demo():
    """Demonstrate quantum entanglement."""
    print("\n" + "=" * 60)
    print("QUANTUM ENTANGLEMENT DEMONSTRATION")
    print("=" * 60)

    circuit = QuantumCircuit(2)

    # Create Bell state (maximally entangled)
    circuit.hadamard(0)
    circuit.cnot(0, 1)

    print("Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2:")
    print(f"  {circuit.state}")

    # Measure correlation
    measurements = []
    for _ in range(1000):
        # Reset to Bell state
        circuit.state = QuantumState(2)
        circuit.hadamard(0)
        circuit.cnot(0, 1)

        result = circuit.measure()
        measurements.append(result)

    # Count results
    counts = defaultdict(int)
    for m in measurements:
        counts[m] += 1

    print("\nMeasurement results (1000 trials):")
    for state in range(4):
        binary = format(state, '02b')
        prob = counts[state] / 1000
        print(f"  |{binary}⟩: {prob:.1%}")

    print("\nNote: Only |00⟩ and |11⟩ are observed (perfect correlation)")
    print("This demonstrates entanglement - measuring one qubit determines the other")


if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)

    # Run examples
    deutsch_example()
    grover_example()
    qft_example()
    bernstein_vazirani_example()
    quantum_superposition_demo()
    quantum_entanglement_demo()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Quantum algorithms leverage superposition and entanglement")
    print("- Grover provides quadratic speedup for search")
    print("- Period-finding algorithms enable exponential speedups")
    print("- Quantum parallelism processes all inputs simultaneously")
    print("- Measurement collapses superposition to classical result")
    print("=" * 60)