# Quantum Algorithms Module

## Overview

This module contains classical simulations of fundamental quantum algorithms for educational purposes. These implementations demonstrate quantum computing concepts and theoretical speedups that quantum computers can achieve over classical computers.

## Implemented Algorithms

### 1. Core Quantum Algorithms (`quantum_simulations.py`)

This comprehensive module implements the foundational quantum algorithms:

#### **Deutsch's Algorithm**
- **Purpose**: Determines if a function is constant or balanced with a single evaluation
- **Classical Complexity**: O(2) evaluations
- **Quantum Complexity**: O(1) evaluation
- **Implementation**: `DeutschAlgorithm` class

#### **Grover's Search Algorithm**
- **Purpose**: Searches unsorted databases
- **Classical Complexity**: O(N)
- **Quantum Complexity**: O(√N)
- **Implementation**: `GroverSearch` class
- **Features**: Automatic iteration count, amplitude amplification

#### **Quantum Fourier Transform (QFT)**
- **Purpose**: Fundamental component for many quantum algorithms
- **Applications**: Period finding, phase estimation
- **Implementation**: `QuantumFourierTransform` class
- **Features**: Efficient circuit construction, inverse QFT

#### **Bernstein-Vazirani Algorithm**
- **Purpose**: Finds hidden bit string with single query
- **Classical Complexity**: O(n) queries
- **Quantum Complexity**: O(1) query
- **Implementation**: `BernsteinVazirani` class

#### **Simon's Algorithm**
- **Purpose**: Finds period of 2-to-1 functions
- **Classical Complexity**: Exponential
- **Quantum Complexity**: Polynomial
- **Implementation**: `SimonAlgorithm` class

#### **Additional Features**:
- Quantum state management (`QuantumState` class)
- Quantum gates implementation (`QuantumGates` class)
- Quantum circuit builder (`QuantumCircuit` class)
- Demonstration functions for superposition and entanglement

### 2. Shor's Factoring Algorithm (`shors_algorithm.py`)

Complete implementation of Shor's algorithm for integer factorization:

- **Purpose**: Factor large composite numbers efficiently
- **Classical Complexity**: Sub-exponential (best known)
- **Quantum Complexity**: Polynomial
- **Implementation**: `ShorsAlgorithm` class

#### **Key Components**:
- Quantum period finding
- Quantum Fourier Transform
- Classical pre/post-processing
- Continued fractions algorithm
- Order finding (`OrderFinding` class)
- Modular arithmetic utilities

#### **Features**:
- Handles edge cases (even numbers, prime powers)
- Multiple factorization attempts with different bases
- Educational examples for RSA-style numbers

### 3. BB84 Quantum Key Distribution (`bb84_quantum_key_distribution.py`)

Implementation of the BB84 protocol for quantum cryptography:

- **Purpose**: Secure key distribution using quantum mechanics
- **Security**: Information-theoretically secure against eavesdropping
- **Implementation**: `BB84Protocol` class

#### **Components**:
- Qubit preparation and measurement
- Basis reconciliation
- Eavesdropper detection
- Key sifting and privacy amplification
- E91 protocol variant (`E91Protocol` class)

#### **Features**:
- Simulates quantum channel with noise
- Detects eavesdropping attempts
- Error rate calculation
- Privacy amplification techniques

### 4. Quantum Teleportation (`quantum_teleportation.py`)

Implementation of quantum teleportation and related protocols:

#### **Quantum Teleportation**
- **Purpose**: Transfer quantum states using entanglement
- **Implementation**: `QuantumTeleportation` class
- **Features**: Bell state creation, Bell measurement, classical communication

#### **Superdense Coding**
- **Purpose**: Send 2 classical bits using 1 qubit
- **Implementation**: `SuperdenseCoding` class
- **Features**: Encoding/decoding of classical information

#### **Advanced Features**:
- Gate teleportation (`GateTeleportation` class)
- Noisy teleportation simulation (`NoisyTeleportation` class)
- Multi-qubit teleportation (`MultiQubitTeleportation` class)

### 5. Quantum Error Correction (`quantum_error_correction.py`)

Comprehensive quantum error correction implementations:

#### **Three-Bit Flip Code**
- **Purpose**: Correct single bit-flip errors
- **Implementation**: `ThreeBitFlipCode` class
- **Encoding**: 1 logical qubit → 3 physical qubits

#### **Three-Phase Flip Code**
- **Purpose**: Correct single phase-flip errors
- **Implementation**: `ThreePhaseFlipCode` class

#### **Shor's Nine-Qubit Code**
- **Purpose**: Correct arbitrary single-qubit errors
- **Implementation**: `ShorCode` class
- **Encoding**: 1 logical qubit → 9 physical qubits

#### **Stabilizer Codes**
- **Purpose**: General framework for error correction
- **Implementation**: `StabilizerCode` class
- **Features**: Stabilizer formalism, syndrome extraction

#### **Surface Codes**
- **Purpose**: Topological error correction
- **Implementation**: `SurfaceCode` class
- **Features**: 2D lattice structure, nearest-neighbor interactions

#### **Additional Features**:
- Noise channel simulation (`NoiseChannel` class)
- Error correction simulator (`ErrorCorrectionSimulator` class)
- Various error types (bit flip, phase flip, depolarizing)

## Usage Examples

### Running Deutsch's Algorithm
```python
from quantum_simulations import DeutschAlgorithm

# Define a balanced function
def balanced_function(x):
    return x  # Returns 0 for input 0, 1 for input 1

# Run the algorithm
deutsch = DeutschAlgorithm()
result = deutsch.run(balanced_function)
print(f"Function is: {result}")  # Output: "Function is: balanced"
```

### Factoring with Shor's Algorithm
```python
from shors_algorithm import ShorsAlgorithm

# Factor a composite number
N = 15
shors = ShorsAlgorithm(N)
factors = shors.factor(N)
print(f"Factors of {N}: {factors}")  # Output: "Factors of 15: [3, 5]"
```

### BB84 Key Distribution
```python
from bb84_quantum_key_distribution import BB84Protocol

# Run the protocol
protocol = BB84Protocol()
alice_key, bob_key, eve_detected = protocol.run_protocol(with_eve=False)
print(f"Keys match: {alice_key == bob_key}")
print(f"Eve detected: {eve_detected}")
```

### Quantum Teleportation
```python
from quantum_teleportation import QuantumTeleportation, QuantumState

# Create and teleport a quantum state
teleporter = QuantumTeleportation()
state = QuantumState(num_qubits=1)
state.amplitudes = [0.6, 0.8]  # |ψ⟩ = 0.6|0⟩ + 0.8|1⟩
state.normalize()

teleported_state = teleporter.teleport(state)
print("State successfully teleported!")
```

### Quantum Error Correction
```python
from quantum_error_correction import ThreeBitFlipCode, QuantumState

# Create an error correction code
code = ThreeBitFlipCode()

# Encode a quantum state
state = QuantumState(n_qubits=1)
state.amplitudes = [0.6, 0.8]
state.normalize()

encoded = code.encode(state)
# Simulate error and correction
corrected = code.correct(encoded, error_position=0)
```

## Educational Demonstrations

Each module includes demonstration functions that showcase the algorithms:

```python
# Run example demonstrations
from quantum_simulations import (
    deutsch_example,
    grover_example,
    qft_example,
    bernstein_vazirani_example,
    quantum_superposition_demo,
    quantum_entanglement_demo
)

# Run any demonstration
deutsch_example()
grover_example()
quantum_superposition_demo()
```

## Key Quantum Concepts Demonstrated

1. **Superposition**: Quantum states existing in multiple states simultaneously
2. **Entanglement**: Quantum correlations between particles
3. **Interference**: Constructive and destructive amplitude interference
4. **Measurement**: Probabilistic collapse of quantum states
5. **Oracle Functions**: Black-box function evaluation in quantum algorithms
6. **Amplitude Amplification**: Enhancing probabilities of desired outcomes
7. **Phase Kickback**: Information encoding in relative phases
8. **Quantum Parallelism**: Evaluating functions on superpositions
9. **No-Cloning Theorem**: Impossibility of copying arbitrary quantum states
10. **Quantum Error Correction**: Protecting quantum information from decoherence

## Complexity Comparisons

| Algorithm | Classical | Quantum | Speedup |
|-----------|-----------|----------|---------|
| Database Search | O(N) | O(√N) | Quadratic |
| Integer Factorization | Sub-exponential | Polynomial | Exponential |
| Hidden Bit String | O(n) | O(1) | Linear |
| Period Finding | Exponential | Polynomial | Exponential |
| Deutsch's Problem | O(2) | O(1) | Constant |

## Testing

A comprehensive test suite is provided in `test_quantum_algorithms.py`:

```bash
python test_quantum_algorithms.py
```

## Requirements

- Python 3.8+
- NumPy
- Optional: matplotlib for visualizations

## Notes

- These are **classical simulations** for educational purposes
- Real quantum advantages require actual quantum hardware
- Simulation complexity grows exponentially with qubit count
- Limited to small problem sizes due to classical simulation constraints

## Future Enhancements

- [ ] Visualization tools for quantum circuits
- [ ] Additional algorithms (Quantum walks, HHL, VQE)
- [ ] Integration with quantum cloud services (IBM Q, AWS Braket)
- [ ] Performance optimizations for larger simulations
- [ ] Interactive Jupyter notebooks

## References

1. Nielsen, M. A., & Chuang, I. L. (2010). Quantum Computation and Quantum Information
2. Mermin, N. D. (2007). Quantum Computer Science: An Introduction
3. Yanofsky, N. S., & Mannucci, M. A. (2008). Quantum Computing for Computer Scientists
4. Rieffel, E., & Polak, W. (2011). Quantum Computing: A Gentle Introduction

## Author

Created as part of the Algorithms Multiverse project - January 2026