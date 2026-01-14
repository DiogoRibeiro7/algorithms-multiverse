"""
Shor's Factoring Algorithm Implementation

Classical simulation of Shor's algorithm for integer factorization.
This provides educational insight into the quantum algorithm that could
break RSA encryption with a sufficiently large quantum computer.

Key Components:
- Quantum Period Finding (simulated classically)
- Quantum Fourier Transform (QFT)
- Classical pre/post-processing
- Continued fractions algorithm

Author: Claude
Date: January 2026
"""

import numpy as np
import random
import math
from typing import Tuple, Optional, List, Complex
from fractions import Fraction
from dataclasses import dataclass
import warnings


@dataclass
class QuantumState:
    """Represents a quantum state for simulation."""
    amplitudes: np.ndarray
    num_qubits: int

    @property
    def num_states(self) -> int:
        """Number of basis states."""
        return 2 ** self.num_qubits

    def measure(self) -> int:
        """Measure the quantum state."""
        probabilities = np.abs(self.amplitudes) ** 2
        probabilities /= np.sum(probabilities)  # Normalize
        state = np.random.choice(self.num_states, p=probabilities)
        return state

    def normalize(self):
        """Normalize the state vector."""
        norm = np.linalg.norm(self.amplitudes)
        if norm > 0:
            self.amplitudes /= norm


class ShorsAlgorithm:
    """
    Implementation of Shor's factoring algorithm.

    This is a classical simulation that demonstrates the key concepts
    of the quantum algorithm.
    """

    def __init__(self, verbose: bool = True):
        """
        Initialize Shor's algorithm.

        Args:
            verbose: Print detailed steps
        """
        self.verbose = verbose

    def factor(self, N: int, max_attempts: int = 10) -> Optional[Tuple[int, int]]:
        """
        Factor an integer N using Shor's algorithm.

        Args:
            N: Integer to factor (should be composite)
            max_attempts: Maximum factoring attempts

        Returns:
            Tuple of factors or None if failed
        """
        if self.verbose:
            print(f"Factoring N = {N}")

        # Step 1: Check if N is even
        if N % 2 == 0:
            return 2, N // 2

        # Step 2: Check if N = a^b for integers a > 1 and b >= 2
        factor = self._check_prime_power(N)
        if factor:
            return factor

        # Step 3: Main quantum subroutine (simulated)
        for attempt in range(max_attempts):
            if self.verbose:
                print(f"\nAttempt {attempt + 1}:")

            # Choose random a < N coprime to N
            a = random.randint(2, N - 1)
            gcd_a_N = math.gcd(a, N)

            if gcd_a_N > 1:
                # Lucky! Found a factor classically
                if self.verbose:
                    print(f"  Found factor classically: gcd({a}, {N}) = {gcd_a_N}")
                return gcd_a_N, N // gcd_a_N

            if self.verbose:
                print(f"  Chose a = {a}")

            # Find period r using quantum period finding (simulated)
            r = self._find_period_classical(a, N)

            if r is None:
                if self.verbose:
                    print(f"  Period finding failed")
                continue

            if self.verbose:
                print(f"  Found period r = {r}")

            # Check if r is even and a^(r/2) ≠ -1 (mod N)
            if r % 2 != 0:
                if self.verbose:
                    print(f"  Period r = {r} is odd, trying again")
                continue

            x = pow(a, r // 2, N)
            if x == N - 1:
                if self.verbose:
                    print(f"  a^(r/2) ≡ -1 (mod N), trying again")
                continue

            # Compute factors
            factor1 = math.gcd(x - 1, N)
            factor2 = math.gcd(x + 1, N)

            if factor1 > 1 and factor1 < N:
                if self.verbose:
                    print(f"  Found factors: {factor1} and {N // factor1}")
                return factor1, N // factor1

            if factor2 > 1 and factor2 < N:
                if self.verbose:
                    print(f"  Found factors: {factor2} and {N // factor2}")
                return factor2, N // factor2

        if self.verbose:
            print(f"\nFactorization failed after {max_attempts} attempts")
        return None

    def _check_prime_power(self, N: int) -> Optional[Tuple[int, int]]:
        """Check if N = a^b for some integers a > 1, b >= 2."""
        for b in range(2, int(math.log2(N)) + 1):
            a = int(N ** (1 / b))
            if a ** b == N:
                return a, N // a
        return None

    def _find_period_classical(self, a: int, N: int) -> Optional[int]:
        """
        Classical simulation of quantum period finding.

        In a real quantum computer, this would use quantum parallelism.
        """
        # For small N, we can find period classically
        if N < 1000:
            return self._find_period_naive(a, N)

        # For larger N, use quantum simulation
        return self._quantum_period_finding_simulation(a, N)

    def _find_period_naive(self, a: int, N: int, max_period: int = 1000) -> Optional[int]:
        """Find period using naive classical method."""
        current = a % N
        for r in range(1, min(max_period, N)):
            if current == 1:
                return r
            current = (current * a) % N
        return None

    def _quantum_period_finding_simulation(self, a: int, N: int) -> Optional[int]:
        """
        Simulate quantum period finding using QFT.

        This is a simplified simulation of the quantum circuit.
        """
        # Number of qubits needed
        n = math.ceil(math.log2(N))
        q = 2 * n  # Use 2n qubits for better precision

        if self.verbose:
            print(f"  Using {q} qubits for period finding")

        # In real quantum algorithm, we'd prepare superposition and apply
        # modular exponentiation. Here we simulate the measurement outcome.

        # Simulate measuring the second register (gets random f(x) value)
        # This collapses first register to superposition of x where f(x) = measured_value
        measured_value = random.randint(0, N - 1)

        # Find period using continued fractions on simulated QFT measurement
        Q = 2 ** q

        # Simulate QFT measurement (would give us s/r for some s)
        # In practice, we'd measure multiple times
        for _ in range(10):  # Try multiple measurements
            # Simulate measurement giving us approximately k*Q/r for some k
            r_candidate = random.randint(2, N - 1)  # Actual period

            # Check if this r works
            if pow(a, r_candidate, N) == 1:
                # Verify it's the smallest such r
                for i in range(1, r_candidate):
                    if pow(a, i, N) == 1:
                        return i
                return r_candidate

        # Fallback to continued fractions method
        return self._period_from_continued_fractions(a, N, q)

    def _period_from_continued_fractions(self, a: int, N: int, q: int) -> Optional[int]:
        """
        Extract period using continued fractions algorithm.

        This simulates extracting the period from QFT measurement.
        """
        Q = 2 ** q

        # Simulate a measurement outcome (in reality from QFT)
        # We simulate getting a value close to s*Q/r for unknown r
        actual_period = self._find_period_naive(a, N, 100)
        if not actual_period:
            return None

        s = random.randint(0, actual_period - 1)
        measured = (s * Q) // actual_period

        # Add some noise to simulate measurement error
        noise = random.randint(-1, 1)
        measured = max(0, min(Q - 1, measured + noise))

        # Use continued fractions to find r
        fraction = Fraction(measured, Q).limit_denominator(N)

        r_candidate = fraction.denominator

        # Verify the period
        if pow(a, r_candidate, N) == 1:
            return r_candidate

        # Try multiples
        for mult in range(2, 10):
            if pow(a, r_candidate * mult, N) == 1:
                return r_candidate * mult

        return None

    def demonstrate_quantum_speedup(self, N: int):
        """
        Demonstrate the quantum speedup conceptually.

        Args:
            N: Number to factor
        """
        import time

        print(f"\n=== Quantum Speedup Demonstration for N = {N} ===\n")

        # Classical trial division
        print("Classical Trial Division:")
        start = time.time()
        factor = self._classical_trial_division(N)
        classical_time = time.time() - start
        print(f"  Found factor: {factor}")
        print(f"  Time: {classical_time:.6f} seconds")
        print(f"  Operations: O(√N) = O({int(math.sqrt(N))})")

        # Shor's algorithm (simulated)
        print("\nShor's Algorithm (simulated):")
        start = time.time()
        factors = self.factor(N, max_attempts=5)
        quantum_time = time.time() - start
        if factors:
            print(f"  Found factors: {factors[0]} × {factors[1]}")
        print(f"  Simulation time: {quantum_time:.6f} seconds")
        print(f"  Quantum operations: O((log N)³) = O({int(math.log2(N)**3)})")

        print(f"\nNote: Real quantum computer would show exponential speedup")
        print(f"Classical: O(exp(∛(log N log log N)))")
        print(f"Quantum: O((log N)³)")

    def _classical_trial_division(self, N: int) -> Optional[int]:
        """Classical factoring by trial division."""
        if N % 2 == 0:
            return 2

        sqrt_N = int(math.sqrt(N))
        for i in range(3, min(sqrt_N + 1, 10000), 2):
            if N % i == 0:
                return i
        return None


class QuantumFourierTransform:
    """
    Quantum Fourier Transform implementation.

    Core component of Shor's algorithm for period finding.
    """

    @staticmethod
    def qft(state: np.ndarray, inverse: bool = False) -> np.ndarray:
        """
        Apply Quantum Fourier Transform.

        Args:
            state: Input quantum state
            inverse: Apply inverse QFT if True

        Returns:
            Transformed state
        """
        n = int(math.log2(len(state)))
        N = len(state)

        # Create QFT matrix
        omega = np.exp(2j * np.pi / N)
        if inverse:
            omega = np.conj(omega)

        # Construct QFT matrix
        qft_matrix = np.zeros((N, N), dtype=complex)
        for j in range(N):
            for k in range(N):
                qft_matrix[j, k] = omega ** (j * k) / np.sqrt(N)

        if inverse:
            qft_matrix = np.conj(qft_matrix)

        return qft_matrix @ state

    @staticmethod
    def demonstrate_qft():
        """Demonstrate QFT on small examples."""
        print("=== Quantum Fourier Transform Demo ===\n")

        # Example 1: Uniform superposition
        n = 3  # 3 qubits
        N = 2 ** n

        # Create uniform superposition
        state = np.ones(N) / np.sqrt(N)
        print(f"Input state (uniform superposition):")
        print(f"  |ψ⟩ = {' + '.join([f'|{i}⟩' for i in range(N)])} / √{N}")

        # Apply QFT
        qft_state = QuantumFourierTransform.qft(state)

        print(f"\nAfter QFT:")
        print(f"  Amplitudes: {np.round(qft_state, 3)}")

        # Example 2: Computational basis state
        state = np.zeros(N)
        state[3] = 1  # |3⟩ state
        print(f"\n\nInput state: |3⟩")

        qft_state = QuantumFourierTransform.qft(state)
        print(f"After QFT:")
        for i in range(N):
            amp = qft_state[i]
            if abs(amp) > 0.01:
                print(f"  |{i}⟩: {amp:.3f}")


class OrderFinding:
    """
    Order finding subroutine for Shor's algorithm.

    Finds the order r of a modulo N (smallest r such that a^r ≡ 1 mod N).
    """

    @staticmethod
    def find_order_quantum_simulation(a: int, N: int) -> Optional[int]:
        """
        Simulate quantum order finding.

        Args:
            a: Base
            N: Modulus

        Returns:
            Order r or None if failed
        """
        if math.gcd(a, N) != 1:
            return None

        # Number of qubits
        n = math.ceil(math.log2(N))
        q = 2 * n

        # This simulates the quantum circuit:
        # 1. Initialize first register in superposition
        # 2. Apply modular exponentiation
        # 3. Measure second register
        # 4. Apply QFT to first register
        # 5. Measure and extract period

        # For simulation, we use classical period finding
        # with continued fractions
        Q = 2 ** q

        # Find actual period classically (for simulation)
        actual_r = None
        current = 1
        for r in range(1, N):
            current = (current * a) % N
            if current == 1:
                actual_r = r
                break

        if not actual_r:
            return None

        # Simulate quantum measurement
        # We'd measure s/r in lowest terms where s is random
        s = random.randint(0, actual_r - 1)
        if math.gcd(s, actual_r) > 1:
            # Unlucky measurement, try again
            s = 0

        measured_value = (s * Q) // actual_r

        # Extract period using continued fractions
        cf = Fraction(measured_value, Q).limit_denominator(N)

        if cf.denominator < N and pow(a, cf.denominator, N) == 1:
            return cf.denominator

        return actual_r


# Classical helper algorithms
def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean algorithm.

    Returns (gcd, x, y) such that a*x + b*y = gcd(a, b)
    """
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y


def modular_inverse(a: int, m: int) -> Optional[int]:
    """
    Find modular multiplicative inverse of a modulo m.

    Returns x such that (a * x) % m == 1
    """
    gcd, x, _ = extended_gcd(a, m)

    if gcd != 1:
        return None  # Modular inverse doesn't exist

    return (x % m + m) % m


def is_prime(n: int) -> bool:
    """Miller-Rabin primality test."""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witnesses to test
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    for a in witnesses:
        if a >= n:
            break

        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


# Example usage and demonstrations
def example_basic_factoring():
    """Demonstrate basic Shor's algorithm factoring."""
    print("=== Basic Shor's Algorithm Demo ===\n")

    shor = ShorsAlgorithm(verbose=True)

    test_numbers = [15, 21, 35, 77, 91]

    for N in test_numbers:
        print(f"\nFactoring N = {N}:")
        print("-" * 30)

        result = shor.factor(N, max_attempts=5)

        if result:
            factor1, factor2 = result
            print(f"\nSuccess! {N} = {factor1} × {factor2}")

            # Verify
            if factor1 * factor2 == N:
                print("✓ Factorization verified")
        else:
            print(f"\nFailed to factor {N}")


def example_rsa_breaking():
    """Demonstrate breaking small RSA keys."""
    print("=== Breaking Small RSA Example ===\n")

    # Generate small RSA-like modulus
    p, q = 61, 53  # Small primes
    N = p * q
    phi_N = (p - 1) * (q - 1)
    e = 17  # Public exponent

    print(f"RSA Parameters:")
    print(f"  p = {p}, q = {q}")
    print(f"  N = p × q = {N}")
    print(f"  Public exponent e = {e}")

    # Factor N using Shor's algorithm
    print(f"\nUsing Shor's algorithm to factor N = {N}...")

    shor = ShorsAlgorithm(verbose=False)
    result = shor.factor(N)

    if result:
        found_p, found_q = result
        print(f"  Found factors: {found_p} and {found_q}")

        # Compute private key
        found_phi = (found_p - 1) * (found_q - 1)
        d = modular_inverse(e, found_phi)

        print(f"\nRecovered private key d = {d}")

        # Test encryption/decryption
        message = 42
        encrypted = pow(message, e, N)
        decrypted = pow(encrypted, d, N)

        print(f"\nTest encryption:")
        print(f"  Original message: {message}")
        print(f"  Encrypted: {encrypted}")
        print(f"  Decrypted: {decrypted}")
        print(f"  Success: {message == decrypted}")


def example_quantum_components():
    """Demonstrate quantum components of Shor's algorithm."""
    print("=== Quantum Components Demo ===\n")

    # Demonstrate QFT
    QuantumFourierTransform.demonstrate_qft()

    print("\n" + "=" * 50 + "\n")

    # Demonstrate order finding
    print("=== Order Finding Demo ===\n")

    a, N = 7, 15
    print(f"Finding order of {a} modulo {N}")

    order = OrderFinding.find_order_quantum_simulation(a, N)
    print(f"  Found order: {order}")

    # Verify
    if order:
        result = pow(a, order, N)
        print(f"  Verification: {a}^{order} mod {N} = {result}")
        print(f"  Correct: {result == 1}")


def analyze_complexity():
    """Analyze computational complexity."""
    print("=== Complexity Analysis ===\n")

    bit_sizes = [8, 16, 32, 64, 128, 256, 512, 1024, 2048]

    print(f"{'Bits':<10} {'Classical (GNFS)':<25} {'Quantum (Shor)':<25}")
    print("-" * 60)

    for bits in bit_sizes:
        # Classical: General Number Field Sieve
        # Complexity: exp(∛(64/9) * (log N)^(1/3) * (log log N)^(2/3))
        log_N = bits * math.log(2)
        log_log_N = math.log(log_N)
        classical = math.exp((64/9) ** (1/3) * (log_N ** (1/3)) * (log_log_N ** (2/3)))

        # Quantum: Shor's algorithm
        # Complexity: O((log N)³)
        quantum = bits ** 3

        print(f"{bits:<10} {classical:<25.2e} {quantum:<25.0f}")

    print("\nNote: Classical uses General Number Field Sieve complexity")
    print("Quantum speedup becomes astronomical for large keys")
    print("2048-bit RSA: Classical ~10^30 operations, Quantum ~10^9 operations")


def example_period_finding():
    """Demonstrate the period finding subroutine."""
    print("=== Period Finding Subroutine ===\n")

    # Example: Find period of 3^x mod 35
    a, N = 3, 35
    print(f"Finding period of f(x) = {a}^x mod {N}")

    # Show the sequence
    print(f"\nSequence:")
    values = []
    current = 1
    for x in range(20):
        current = (current * a) % N
        values.append(current)
        print(f"  f({x+1}) = {current}")

        if current == 1:
            print(f"\nPeriod found: r = {x + 1}")
            break

    # Use this for factoring
    r = x + 1
    if r % 2 == 0:
        x_val = pow(a, r // 2, N)
        factor1 = math.gcd(x_val - 1, N)
        factor2 = math.gcd(x_val + 1, N)

        print(f"\nUsing period for factoring:")
        print(f"  {a}^({r}/2) mod {N} = {x_val}")
        print(f"  gcd({x_val} - 1, {N}) = {factor1}")
        print(f"  gcd({x_val} + 1, {N}) = {factor2}")

        if factor1 > 1 and factor1 < N:
            print(f"  Found factor: {factor1}")
            print(f"  {N} = {factor1} × {N // factor1}")


if __name__ == "__main__":
    # Run examples
    example_basic_factoring()
    print("\n" + "=" * 60 + "\n")

    example_rsa_breaking()
    print("\n" + "=" * 60 + "\n")

    example_quantum_components()
    print("\n" + "=" * 60 + "\n")

    example_period_finding()
    print("\n" + "=" * 60 + "\n")

    analyze_complexity()

    # Demonstrate quantum speedup
    shor = ShorsAlgorithm(verbose=False)
    shor.demonstrate_quantum_speedup(15 * 17)  # Factor 255

    print("\n" + "=" * 60)
    print("Key Insights:")
    print("=" * 60)
    print("""
1. Shor's algorithm provides exponential speedup for factoring,
   threatening current RSA encryption with quantum computers.

2. The algorithm cleverly reduces factoring to period finding,
   which can be solved efficiently with quantum parallelism.

3. Key quantum components:
   - Superposition for parallel computation
   - Quantum Fourier Transform for period extraction
   - Entanglement for modular exponentiation

4. Classical parts remain important:
   - GCD calculations
   - Continued fractions
   - Verification steps

5. Current limitations:
   - Requires ~2n qubits for n-bit numbers
   - Needs high-fidelity quantum gates
   - Error correction overhead is significant

6. Practical implications:
   - 2048-bit RSA needs ~4000+ logical qubits
   - Current quantum computers have ~100-1000 noisy qubits
   - Post-quantum cryptography is being developed

7. The algorithm demonstrates quantum computing's potential
   for solving specific problems exponentially faster.
    """)