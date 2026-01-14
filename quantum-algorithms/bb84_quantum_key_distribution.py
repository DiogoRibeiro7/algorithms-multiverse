"""
BB84 Quantum Key Distribution Protocol Implementation

Simulation of the BB84 protocol for quantum key distribution,
demonstrating quantum cryptography principles for secure communication.

Key Features:
- Quantum state preparation and measurement
- Basis reconciliation
- Error estimation and privacy amplification
- Eavesdropper detection
- Information reconciliation protocols

Author: Claude
Date: January 2026
"""

import numpy as np
import random
import hashlib
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import math


class Basis(Enum):
    """Quantum measurement basis."""
    COMPUTATIONAL = "Z"  # {|0⟩, |1⟩}
    HADAMARD = "X"       # {|+⟩, |-⟩}


class Polarization(Enum):
    """Photon polarization states."""
    HORIZONTAL = 0      # |0⟩ or |→⟩
    VERTICAL = 1        # |1⟩ or |↑⟩
    DIAGONAL = 2        # |+⟩ or |↗⟩
    ANTI_DIAGONAL = 3   # |-⟩ or |↖⟩


@dataclass
class Qubit:
    """
    Represents a qubit state for BB84.

    In BB84, we use four states:
    - |0⟩ (horizontal)
    - |1⟩ (vertical)
    - |+⟩ = (|0⟩ + |1⟩)/√2 (diagonal)
    - |-⟩ = (|0⟩ - |1⟩)/√2 (anti-diagonal)
    """
    bit: int  # 0 or 1
    basis: Basis
    state_vector: Optional[np.ndarray] = None

    def __post_init__(self):
        """Initialize the state vector."""
        if self.state_vector is None:
            if self.basis == Basis.COMPUTATIONAL:
                if self.bit == 0:
                    self.state_vector = np.array([1, 0], dtype=complex)  # |0⟩
                else:
                    self.state_vector = np.array([0, 1], dtype=complex)  # |1⟩
            else:  # Hadamard basis
                if self.bit == 0:
                    self.state_vector = np.array([1, 1], dtype=complex) / np.sqrt(2)  # |+⟩
                else:
                    self.state_vector = np.array([1, -1], dtype=complex) / np.sqrt(2)  # |-⟩

    def measure(self, measurement_basis: Basis) -> int:
        """
        Measure the qubit in the specified basis.

        Returns:
            Measurement result (0 or 1)
        """
        if measurement_basis == self.basis:
            # Same basis - deterministic result
            return self.bit
        else:
            # Different basis - random result
            return random.randint(0, 1)


@dataclass
class BB84Channel:
    """
    Quantum channel for BB84 protocol.

    Simulates transmission of qubits with optional eavesdropping.
    """
    error_rate: float = 0.0  # Natural channel error rate
    eavesdropper_present: bool = False
    eavesdrop_probability: float = 0.5  # Probability Eve intercepts each qubit

    def transmit(self, qubit: Qubit) -> Qubit:
        """
        Transmit a qubit through the channel.

        Args:
            qubit: Input qubit

        Returns:
            Output qubit (possibly altered by noise or eavesdropping)
        """
        # Eavesdropping attack (intercept-resend)
        if self.eavesdropper_present and random.random() < self.eavesdrop_probability:
            # Eve randomly chooses a basis and measures
            eve_basis = random.choice(list(Basis))
            measured_bit = qubit.measure(eve_basis)

            # Eve sends a new qubit based on measurement
            qubit = Qubit(measured_bit, eve_basis)

        # Natural channel errors
        if random.random() < self.error_rate:
            # Flip the bit with some probability
            qubit.bit = 1 - qubit.bit
            # Recreate the state vector
            qubit.__post_init__()

        return qubit


class BB84Protocol:
    """
    Implementation of the BB84 Quantum Key Distribution protocol.
    """

    def __init__(self, channel: BB84Channel = None):
        """
        Initialize BB84 protocol.

        Args:
            channel: Quantum channel for transmission
        """
        self.channel = channel or BB84Channel()
        self.statistics = {
            'total_qubits_sent': 0,
            'matching_bases': 0,
            'final_key_length': 0,
            'error_rate': 0.0,
            'eavesdropper_detected': False
        }

    def generate_random_bits(self, n: int) -> List[int]:
        """Generate n random bits."""
        return [random.randint(0, 1) for _ in range(n)]

    def generate_random_bases(self, n: int) -> List[Basis]:
        """Generate n random basis choices."""
        return [random.choice(list(Basis)) for _ in range(n)]

    def alice_prepare(self, num_qubits: int) -> Tuple[List[Qubit], List[int], List[Basis]]:
        """
        Alice prepares quantum states.

        Args:
            num_qubits: Number of qubits to prepare

        Returns:
            Tuple of (qubits, bits, bases)
        """
        # Generate random bits and bases
        bits = self.generate_random_bits(num_qubits)
        bases = self.generate_random_bases(num_qubits)

        # Prepare qubits
        qubits = [Qubit(bit, basis) for bit, basis in zip(bits, bases)]

        self.statistics['total_qubits_sent'] = num_qubits

        return qubits, bits, bases

    def bob_measure(self, qubits: List[Qubit]) -> Tuple[List[int], List[Basis]]:
        """
        Bob measures received qubits.

        Args:
            qubits: Received qubits

        Returns:
            Tuple of (measured bits, measurement bases)
        """
        # Bob randomly chooses measurement bases
        bob_bases = self.generate_random_bases(len(qubits))

        # Measure qubits
        measured_bits = []
        for qubit, basis in zip(qubits, bob_bases):
            bit = qubit.measure(basis)
            measured_bits.append(bit)

        return measured_bits, bob_bases

    def basis_reconciliation(self, alice_bases: List[Basis],
                           bob_bases: List[Basis]) -> List[int]:
        """
        Publicly compare bases and keep matching indices.

        Args:
            alice_bases: Alice's basis choices
            bob_bases: Bob's basis choices

        Returns:
            Indices where bases match
        """
        matching_indices = []
        for i, (a_basis, b_basis) in enumerate(zip(alice_bases, bob_bases)):
            if a_basis == b_basis:
                matching_indices.append(i)

        self.statistics['matching_bases'] = len(matching_indices)

        return matching_indices

    def extract_sifted_key(self, bits: List[int],
                          matching_indices: List[int]) -> List[int]:
        """
        Extract sifted key from matching basis positions.

        Args:
            bits: Original bit string
            matching_indices: Indices where bases matched

        Returns:
            Sifted key
        """
        return [bits[i] for i in matching_indices]

    def estimate_error_rate(self, alice_key: List[int],
                          bob_key: List[int],
                          sample_size: Optional[int] = None) -> Tuple[float, List[int], List[int]]:
        """
        Estimate error rate by comparing a sample of bits.

        Args:
            alice_key: Alice's sifted key
            bob_key: Bob's sifted key
            sample_size: Number of bits to sample (default: 10% of key)

        Returns:
            Tuple of (error_rate, alice_remaining, bob_remaining)
        """
        if sample_size is None:
            sample_size = max(1, len(alice_key) // 10)

        sample_size = min(sample_size, len(alice_key))

        # Randomly select indices for error estimation
        sample_indices = random.sample(range(len(alice_key)), sample_size)
        sample_indices.sort()

        # Compare sampled bits
        errors = 0
        for idx in sample_indices:
            if alice_key[idx] != bob_key[idx]:
                errors += 1

        error_rate = errors / sample_size if sample_size > 0 else 0

        # Remove sampled bits from keys
        alice_remaining = [alice_key[i] for i in range(len(alice_key))
                          if i not in sample_indices]
        bob_remaining = [bob_key[i] for i in range(len(bob_key))
                        if i not in sample_indices]

        self.statistics['error_rate'] = error_rate

        return error_rate, alice_remaining, bob_remaining

    def error_correction(self, alice_key: List[int],
                        bob_key: List[int]) -> Tuple[List[int], List[int]]:
        """
        Perform error correction using CASCADE protocol (simplified).

        Args:
            alice_key: Alice's key
            bob_key: Bob's key

        Returns:
            Error-corrected keys
        """
        # Simplified error correction: use parity checks
        corrected_alice = []
        corrected_bob = []

        block_size = 8  # Process in blocks

        for i in range(0, len(alice_key) - block_size + 1, block_size):
            alice_block = alice_key[i:i + block_size]
            bob_block = bob_key[i:i + block_size]

            # Calculate parity
            alice_parity = sum(alice_block) % 2
            bob_parity = sum(bob_block) % 2

            if alice_parity == bob_parity:
                # Likely no error (or even number of errors)
                corrected_alice.extend(alice_block)
                corrected_bob.extend(bob_block)
            else:
                # Binary search for error (simplified)
                # In practice, would use more sophisticated methods
                if len(alice_block) > 1:
                    # Just skip this block in simplified version
                    pass

        return corrected_alice, corrected_bob

    def privacy_amplification(self, key: List[int],
                            error_rate: float) -> List[int]:
        """
        Perform privacy amplification to reduce Eve's information.

        Args:
            key: Input key
            error_rate: Estimated channel error rate

        Returns:
            Shortened but more secure key
        """
        if not key:
            return []

        # Calculate how much to compress based on error rate
        # Higher error rate means more potential eavesdropping
        compression_factor = 1 - 2 * error_rate
        compressed_length = max(1, int(len(key) * compression_factor))

        # Use universal hashing (simplified with SHA-256)
        key_bytes = bytes(key)
        hash_output = hashlib.sha256(key_bytes).digest()

        # Convert hash to bits
        amplified_key = []
        for byte in hash_output[:compressed_length // 8]:
            for i in range(8):
                amplified_key.append((byte >> i) & 1)

        return amplified_key[:compressed_length]

    def run_protocol(self, num_qubits: int = 1000,
                    error_threshold: float = 0.11) -> Tuple[List[int], List[int], bool]:
        """
        Run complete BB84 protocol.

        Args:
            num_qubits: Number of qubits to transmit
            error_threshold: Maximum acceptable error rate

        Returns:
            Tuple of (alice_key, bob_key, success)
        """
        print(f"=== Running BB84 Protocol ===")
        print(f"Transmitting {num_qubits} qubits...")

        # Step 1: Alice prepares qubits
        qubits, alice_bits, alice_bases = self.alice_prepare(num_qubits)

        # Step 2: Transmit qubits through channel
        transmitted_qubits = [self.channel.transmit(q) for q in qubits]

        # Step 3: Bob measures qubits
        bob_bits, bob_bases = self.bob_measure(transmitted_qubits)

        # Step 4: Basis reconciliation (public channel)
        matching_indices = self.basis_reconciliation(alice_bases, bob_bases)
        print(f"Matching bases: {len(matching_indices)}/{num_qubits}")

        # Step 5: Extract sifted keys
        alice_sifted = self.extract_sifted_key(alice_bits, matching_indices)
        bob_sifted = self.extract_sifted_key(bob_bits, matching_indices)

        # Step 6: Error rate estimation
        error_rate, alice_key, bob_key = self.estimate_error_rate(
            alice_sifted, bob_sifted
        )
        print(f"Estimated error rate: {error_rate:.2%}")

        # Step 7: Eavesdropper detection
        if error_rate > error_threshold:
            print(f"⚠️  Error rate exceeds threshold ({error_threshold:.2%})")
            print("Possible eavesdropper detected! Aborting protocol.")
            self.statistics['eavesdropper_detected'] = True
            return [], [], False

        # Step 8: Error correction
        alice_corrected, bob_corrected = self.error_correction(alice_key, bob_key)

        # Step 9: Privacy amplification
        alice_final = self.privacy_amplification(alice_corrected, error_rate)
        bob_final = self.privacy_amplification(bob_corrected, error_rate)

        self.statistics['final_key_length'] = len(alice_final)

        # Verify keys match (they should after error correction)
        success = alice_final == bob_final

        if success:
            print(f"✓ Protocol successful! Final key length: {len(alice_final)} bits")
        else:
            print("✗ Key agreement failed")

        return alice_final, bob_final, success


class E91Protocol:
    """
    E91 Protocol - Entanglement-based quantum key distribution.

    Uses EPR pairs and Bell inequality violation to detect eavesdropping.
    """

    def __init__(self):
        """Initialize E91 protocol."""
        self.bell_parameter = 0.0

    def create_entangled_pair(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create an EPR pair (Bell state).

        Returns:
            Tuple of entangled state vectors
        """
        # Create |Φ+⟩ = (|00⟩ + |11⟩)/√2
        bell_state = np.zeros((4,), dtype=complex)
        bell_state[0] = 1 / np.sqrt(2)  # |00⟩
        bell_state[3] = 1 / np.sqrt(2)  # |11⟩

        return bell_state

    def measure_correlation(self, alice_angle: float,
                          bob_angle: float) -> float:
        """
        Calculate quantum correlation E(a,b) for given measurement angles.

        Args:
            alice_angle: Alice's measurement angle
            bob_angle: Bob's measurement angle

        Returns:
            Correlation value
        """
        # For EPR pairs: E(a,b) = -cos(a - b)
        return -np.cos(alice_angle - bob_angle)

    def calculate_bell_parameter(self, angles: List[Tuple[float, float]]) -> float:
        """
        Calculate CHSH Bell parameter S.

        Args:
            angles: List of (alice_angle, bob_angle) pairs

        Returns:
            Bell parameter S
        """
        # CHSH inequality: |S| ≤ 2 (classical), |S| ≤ 2√2 (quantum)
        # S = E(a,b) - E(a,b') + E(a',b) + E(a',b')

        correlations = [self.measure_correlation(a, b) for a, b in angles]

        # Standard CHSH angles
        S = correlations[0] - correlations[1] + correlations[2] + correlations[3]

        self.bell_parameter = S
        return S

    def detect_eavesdropping(self, bell_parameter: float) -> bool:
        """
        Detect eavesdropping using Bell inequality violation.

        Args:
            bell_parameter: Calculated Bell parameter

        Returns:
            True if eavesdropping detected
        """
        # Quantum mechanics predicts S = 2√2 ≈ 2.828
        # Classical limit is S = 2
        # If S < 2.4, likely eavesdropping

        quantum_expected = 2 * np.sqrt(2)
        threshold = 2.4

        if abs(bell_parameter) < threshold:
            return True  # Eavesdropping detected

        return False


class QuantumCryptanalysis:
    """
    Analysis of quantum cryptographic protocols.
    """

    @staticmethod
    def calculate_information_gain(error_rate: float) -> float:
        """
        Calculate Eve's information gain from intercept-resend attack.

        Args:
            error_rate: Observed error rate

        Returns:
            Eve's information (in bits per qubit)
        """
        if error_rate == 0:
            return 0

        # For intercept-resend attack
        # Eve gains ~50% information when she guesses wrong basis
        # This introduces 25% error rate

        # Shannon entropy
        if error_rate >= 0.5:
            return 1.0

        h = lambda p: -p * np.log2(p) - (1 - p) * np.log2(1 - p) if 0 < p < 1 else 0
        eve_info = h(error_rate)

        return eve_info

    @staticmethod
    def calculate_secure_key_rate(raw_key_rate: float,
                                 error_rate: float) -> float:
        """
        Calculate secure key generation rate.

        Args:
            raw_key_rate: Rate of raw key generation
            error_rate: Channel error rate

        Returns:
            Secure key rate
        """
        if error_rate >= 0.11:
            return 0  # Too much error/eavesdropping

        # Secure key rate formula (simplified)
        # R = raw_rate * [1 - h(error_rate) - f * h(error_rate)]
        # where h is binary entropy and f is error correction inefficiency

        h = lambda p: -p * np.log2(p) - (1 - p) * np.log2(1 - p) if 0 < p < 1 else 0
        f = 1.2  # Error correction inefficiency

        secure_rate = raw_key_rate * max(0, 1 - h(error_rate) - f * h(error_rate))

        return secure_rate


# Example demonstrations
def example_basic_bb84():
    """Demonstrate basic BB84 protocol."""
    print("=== Basic BB84 Demonstration ===\n")

    # Create channel without eavesdropping
    channel = BB84Channel(error_rate=0.01, eavesdropper_present=False)
    protocol = BB84Protocol(channel)

    # Run protocol
    alice_key, bob_key, success = protocol.run_protocol(num_qubits=1000)

    print(f"\nProtocol Statistics:")
    for key, value in protocol.statistics.items():
        print(f"  {key}: {value}")

    if success and alice_key:
        print(f"\nSample of final key (first 32 bits):")
        print(f"  Alice: {''.join(map(str, alice_key[:32]))}")
        print(f"  Bob:   {''.join(map(str, bob_key[:32]))}")


def example_eavesdropper_detection():
    """Demonstrate eavesdropper detection."""
    print("=== Eavesdropper Detection Demo ===\n")

    print("Scenario 1: No eavesdropper")
    print("-" * 30)
    channel = BB84Channel(error_rate=0.02, eavesdropper_present=False)
    protocol = BB84Protocol(channel)
    _, _, success = protocol.run_protocol(num_qubits=500)

    print(f"\n{'Scenario 2: With eavesdropper'}")
    print("-" * 30)
    channel = BB84Channel(error_rate=0.02,
                         eavesdropper_present=True,
                         eavesdrop_probability=0.5)
    protocol = BB84Protocol(channel)
    _, _, success = protocol.run_protocol(num_qubits=500)


def example_e91_protocol():
    """Demonstrate E91 protocol with Bell inequality."""
    print("=== E91 Protocol (Bell States) ===\n")

    e91 = E91Protocol()

    # Standard CHSH measurement angles
    alice_angles = [0, np.pi/4]
    bob_angles = [np.pi/8, 3*np.pi/8]

    # Create angle pairs for CHSH
    angle_pairs = [
        (alice_angles[0], bob_angles[0]),  # (a, b)
        (alice_angles[0], bob_angles[1]),  # (a, b')
        (alice_angles[1], bob_angles[0]),  # (a', b)
        (alice_angles[1], bob_angles[1])   # (a', b')
    ]

    # Calculate Bell parameter
    S = e91.calculate_bell_parameter(angle_pairs)

    print(f"Bell parameter S = {S:.3f}")
    print(f"Classical limit: |S| ≤ 2")
    print(f"Quantum limit: |S| ≤ 2√2 ≈ {2*np.sqrt(2):.3f}")

    # Check for eavesdropping
    eavesdropping = e91.detect_eavesdropping(S)

    if eavesdropping:
        print("⚠️  Possible eavesdropping detected!")
    else:
        print("✓ No eavesdropping detected")
        print(f"Bell inequality violated: Quantum correlation confirmed")


def example_security_analysis():
    """Analyze security of quantum key distribution."""
    print("=== Security Analysis ===\n")

    analyzer = QuantumCryptanalysis()

    print("Error Rate vs Eve's Information:")
    print("-" * 40)
    error_rates = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25]

    for error_rate in error_rates:
        eve_info = analyzer.calculate_information_gain(error_rate)
        secure_rate = analyzer.calculate_secure_key_rate(1.0, error_rate)

        print(f"Error rate: {error_rate:5.1%}")
        print(f"  Eve's information: {eve_info:.3f} bits")
        print(f"  Secure key rate: {secure_rate:.3f}")
        print()

    print("Key Insights:")
    print("- Error rate > 11%: Protocol aborted (too much eavesdropping)")
    print("- Error rate < 11%: Can extract secure key")
    print("- Privacy amplification reduces key length but ensures security")


def compare_classical_vs_quantum():
    """Compare classical and quantum key distribution."""
    print("=== Classical vs Quantum Key Distribution ===\n")

    print("Classical Key Exchange (e.g., Diffie-Hellman):")
    print("  ✓ Efficient implementation")
    print("  ✓ No special hardware required")
    print("  ✗ Vulnerable to quantum computers (Shor's algorithm)")
    print("  ✗ Security based on computational assumptions")
    print("  ✗ No eavesdropping detection")

    print("\nQuantum Key Distribution (BB84/E91):")
    print("  ✓ Information-theoretic security")
    print("  ✓ Eavesdropping detection guaranteed")
    print("  ✓ Future-proof against quantum computers")
    print("  ✗ Requires quantum hardware")
    print("  ✗ Limited transmission distance")
    print("  ✗ Lower key generation rate")

    print("\n" + "=" * 50)
    print("Practical Implementations:")
    print("- Commercial QKD systems: ~100 km range")
    print("- Key rates: 1-10 Mbps at short distances")
    print("- Satellite QKD: Global coverage possible")
    print("- Integration with classical crypto: Hybrid systems")


def simulate_real_world_qkd():
    """Simulate realistic QKD scenario."""
    print("=== Real-World QKD Simulation ===\n")

    # Simulate different channel conditions
    scenarios = [
        ("Laboratory (1 km fiber)", 0.001, False),
        ("Urban network (10 km)", 0.02, False),
        ("Long-distance (50 km)", 0.05, False),
        ("Compromised channel", 0.02, True),
    ]

    for name, error_rate, eavesdropper in scenarios:
        print(f"\nScenario: {name}")
        print("-" * 40)

        channel = BB84Channel(
            error_rate=error_rate,
            eavesdropper_present=eavesdropper,
            eavesdrop_probability=0.3 if eavesdropper else 0
        )

        protocol = BB84Protocol(channel)

        # Run with more qubits for better statistics
        alice_key, bob_key, success = protocol.run_protocol(
            num_qubits=10000,
            error_threshold=0.11
        )

        if success:
            print(f"Key generation rate: {len(alice_key)/10000:.2%}")
            print(f"Effective key length: {len(alice_key)} bits")

            # Calculate secure transmission capacity
            key_rate = len(alice_key) / 10000  # bits per qubit
            print(f"Secure capacity: {key_rate:.3f} bits/qubit")


if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)

    # Run examples
    example_basic_bb84()
    print("\n" + "=" * 60 + "\n")

    example_eavesdropper_detection()
    print("\n" + "=" * 60 + "\n")

    example_e91_protocol()
    print("\n" + "=" * 60 + "\n")

    example_security_analysis()
    print("\n" + "=" * 60 + "\n")

    compare_classical_vs_quantum()
    print("\n" + "=" * 60 + "\n")

    simulate_real_world_qkd()

    print("\n" + "=" * 60)
    print("Key Insights:")
    print("=" * 60)
    print("""
1. BB84 provides unconditional security based on quantum mechanics,
   not computational assumptions like classical cryptography.

2. Eavesdropping is detectable through increased error rates due to
   the no-cloning theorem and measurement disturbance.

3. The protocol naturally detects man-in-the-middle attacks that
   are undetectable in classical key exchange.

4. Key components:
   - Random basis selection provides security
   - Basis reconciliation reveals no information about key
   - Privacy amplification removes partial information

5. Practical challenges:
   - Quantum channel losses limit distance (~100 km fiber)
   - Hardware imperfections create side channels
   - Low key generation rates compared to classical

6. E91 protocol uses entanglement and Bell inequalities for
   even stronger security guarantees.

7. QKD is already commercially deployed for high-security
   applications like banking and government communications.

8. Future developments:
   - Quantum repeaters for long-distance QKD
   - Device-independent QKD protocols
   - Integration with post-quantum cryptography
    """)