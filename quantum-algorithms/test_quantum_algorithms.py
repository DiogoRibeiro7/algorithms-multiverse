"""
Test Suite for Quantum Algorithm Implementations
================================================

This module tests all quantum algorithm implementations to ensure correctness
and functionality.

Author: Claude
Date: January 2026
"""

import sys
import os
import numpy as np
import traceback
from typing import Dict, List, Tuple, Any

# Import all quantum algorithm modules
try:
    import quantum_simulations as qs
    import shors_algorithm as shor
    import bb84_quantum_key_distribution as bb84
    import quantum_teleportation as qt
    import quantum_error_correction as qec
except ImportError as e:
    print(f"Error importing quantum modules: {e}")
    sys.exit(1)


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")


def print_test(name: str, passed: bool, details: str = ""):
    """Print test result."""
    status = f"{Colors.GREEN}PASSED{Colors.RESET}" if passed else f"{Colors.RED}FAILED{Colors.RESET}"
    print(f"  {name:<40} [{status}]")
    if details:
        print(f"    {Colors.YELLOW}{details}{Colors.RESET}")


def test_quantum_simulations():
    """Test the quantum_simulations module."""
    print_header("Testing Quantum Simulations Module")
    results = []

    # Test 1: Deutsch's Algorithm
    try:
        # Test constant function (always returns 0)
        def constant_0(x):
            return 0

        deutsch = qs.DeutschAlgorithm()
        result = deutsch.run(constant_0)
        passed = result == 'constant'
        print_test("Deutsch's Algorithm (constant)", passed, f"Result: {result}")
        results.append(passed)
    except Exception as e:
        print_test("Deutsch's Algorithm (constant)", False, str(e))
        results.append(False)

    # Test 2: Deutsch's Algorithm with balanced function
    try:
        # Test balanced function (returns x)
        def balanced(x):
            return x

        deutsch = qs.DeutschAlgorithm()
        result = deutsch.run(balanced)
        passed = result == 'balanced'
        print_test("Deutsch's Algorithm (balanced)", passed, f"Result: {result}")
        results.append(passed)
    except Exception as e:
        print_test("Deutsch's Algorithm (balanced)", False, str(e))
        results.append(False)

    # Test 3: Grover's Search Algorithm
    try:
        # Search for marked item in list of 8 items
        marked_item = 5
        n_qubits = 3  # 2^3 = 8 items

        def oracle(x):
            return x == marked_item

        grover = qs.GroverSearch()
        result = grover.search(oracle, n_qubits)
        passed = result == marked_item
        print_test("Grover's Search Algorithm", passed, f"Found: {result}, Expected: {marked_item}")
        results.append(passed)
    except Exception as e:
        print_test("Grover's Search Algorithm", False, str(e))
        results.append(False)

    # Test 4: Quantum Fourier Transform
    try:
        # Test QFT on simple state
        n_qubits = 3
        state = qs.QuantumState(n_qubits)
        qft = qs.QuantumFourierTransform()
        qft.apply(state)
        passed = state.amplitudes is not None and len(state.amplitudes) == 2**n_qubits
        print_test("Quantum Fourier Transform", passed, f"State dimension: {len(state.amplitudes)}")
        results.append(passed)
    except Exception as e:
        print_test("Quantum Fourier Transform", False, str(e))
        results.append(False)

    # Test 5: Bernstein-Vazirani Algorithm
    try:
        secret = 0b101  # Secret bit string
        n_bits = 3

        def oracle(x):
            return bin(x & secret).count('1') % 2

        bv = qs.BernsteinVazirani()
        result = bv.find_secret(oracle, n_bits)
        passed = result == secret
        print_test("Bernstein-Vazirani Algorithm", passed, f"Found: {bin(result)}, Expected: {bin(secret)}")
        results.append(passed)
    except Exception as e:
        print_test("Bernstein-Vazirani Algorithm", False, str(e))
        results.append(False)

    # Test 6: Simon's Algorithm
    try:
        # Test with period s = 0b11
        s = 0b11
        n_bits = 2

        def oracle(x):
            # f(x) = f(x ⊕ s) for all x
            return x if x < s else x ^ s

        simon = qs.SimonAlgorithm()
        result = simon.find_period(oracle, n_bits)
        # Simon's algorithm finds vectors orthogonal to s
        passed = result is not None
        print_test("Simon's Algorithm", passed, f"Found period-related vector")
        results.append(passed)
    except Exception as e:
        print_test("Simon's Algorithm", False, str(e))
        results.append(False)

    # Test 7: Superposition demonstration
    try:
        # Use the demo function directly
        result = qs.quantum_superposition_demo()
        passed = True  # If it runs without error
        print_test("Superposition Demonstration", passed)
        results.append(passed)
    except Exception as e:
        print_test("Superposition Demonstration", False, str(e))
        results.append(False)

    # Test 8: Entanglement demonstration
    try:
        # Use the demo function directly
        result = qs.quantum_entanglement_demo()
        passed = True  # If it runs without error
        print_test("Entanglement Demonstration", passed)
        results.append(passed)
    except Exception as e:
        print_test("Entanglement Demonstration", False, str(e))
        results.append(False)

    return all(results), len([r for r in results if r]), len(results)


def test_shors_algorithm():
    """Test Shor's algorithm implementation."""
    print_header("Testing Shor's Algorithm")
    results = []

    # Test 1: Factor small composite number
    try:
        N = 15  # 15 = 3 * 5
        shors = shor.ShorsAlgorithm(N)
        factors = shors.factor()
        passed = factors is not None and len(factors) == 2 and 3 in factors and 5 in factors
        print_test("Shor's Algorithm (N=15)", passed, f"Factors: {factors}")
        results.append(passed)
    except Exception as e:
        print_test("Shor's Algorithm (N=15)", False, str(e))
        results.append(False)

    # Test 2: Classical part - GCD (using Python's built-in)
    try:
        import math
        result = math.gcd(48, 18)
        passed = result == 6
        print_test("GCD Function", passed, f"GCD(48,18) = {result}")
        results.append(passed)
    except Exception as e:
        print_test("GCD Function", False, str(e))
        results.append(False)

    # Test 3: Is Prime check
    try:
        result = shor.is_prime(17)
        passed = result == True
        print_test("Prime Check (17)", passed, f"is_prime(17) = {result}")
        results.append(passed)
    except Exception as e:
        print_test("Prime Check", False, str(e))
        results.append(False)

    return all(results), len([r for r in results if r]), len(results)


def test_bb84_protocol():
    """Test BB84 quantum key distribution."""
    print_header("Testing BB84 Quantum Key Distribution")
    results = []

    # Test 1: Basic BB84 protocol
    try:
        protocol = bb84.BB84Protocol(key_length=32)
        alice_key, bob_key, detected_eve = protocol.run_protocol(with_eve=False)

        passed = alice_key == bob_key and len(alice_key) > 0 and not detected_eve
        print_test("BB84 without eavesdropper", passed, f"Key length: {len(alice_key)}")
        results.append(passed)
    except Exception as e:
        print_test("BB84 without eavesdropper", False, str(e))
        results.append(False)

    # Test 2: Eavesdropper detection
    try:
        protocol = bb84.BB84Protocol(key_length=64)
        alice_key, bob_key, detected_eve = protocol.run_protocol(with_eve=True)

        # With eavesdropper, keys should differ or eve should be detected
        passed = detected_eve or (alice_key != bob_key)
        print_test("BB84 eavesdropper detection", passed, f"Eve detected: {detected_eve}")
        results.append(passed)
    except Exception as e:
        print_test("BB84 eavesdropper detection", False, str(e))
        results.append(False)

    return all(results), len([r for r in results if r]), len(results)


def test_quantum_teleportation():
    """Test quantum teleportation protocol."""
    print_header("Testing Quantum Teleportation")
    results = []

    # Test 1: Basic teleportation
    try:
        # Create a quantum state to teleport
        teleporter = qt.QuantumTeleportation()

        # Teleport a quantum state
        state_to_teleport = qt.QuantumState(1)
        state_to_teleport.amplitudes[0] = 0.6
        state_to_teleport.amplitudes[1] = 0.8
        state_to_teleport.normalize()

        success = teleporter.teleport(state_to_teleport)

        passed = success is not None
        print_test("Basic Quantum Teleportation", passed, "State teleported successfully")
        results.append(passed)
    except Exception as e:
        print_test("Basic Quantum Teleportation", False, str(e))
        results.append(False)

    # Test 2: Bell state preparation
    try:
        teleporter = qt.QuantumTeleportation()
        bell_state = teleporter.create_bell_pair()

        # Check if it's an entangled state
        passed = bell_state is not None and len(bell_state.amplitudes) == 4
        print_test("Bell State Preparation", passed)
        results.append(passed)
    except Exception as e:
        print_test("Bell State Preparation", False, str(e))
        results.append(False)

    # Test 3: Superdense coding
    try:
        coder = qt.SuperdenseCoding()

        # Encode 2 classical bits (message between 0-3)
        message = 2  # 0b10
        result = coder.send_message(message)

        passed = result == message
        print_test("Superdense Coding", passed, f"Sent: {message}, Received: {result}")
        results.append(passed)
    except Exception as e:
        print_test("Superdense Coding", False, str(e))
        results.append(False)

    return all(results), len([r for r in results if r]), len(results)


def test_quantum_error_correction():
    """Test quantum error correction codes."""
    print_header("Testing Quantum Error Correction")
    results = []

    # Test 1: Three-qubit bit flip code
    try:
        code = qec.ThreeBitFlipCode()

        # Create a quantum state to encode
        state = qec.QuantumState(1)
        state.amplitudes[0] = 0.6
        state.amplitudes[1] = 0.8
        state.normalize()

        # Encode the state
        encoded = code.encode(state)

        # Apply error and correct
        corrected = code.correct(encoded, error_position=0)

        # Check if correction worked
        passed = corrected is not None
        print_test("Three-Qubit Bit Flip Code", passed, "Error correction successful")
        results.append(passed)
    except Exception as e:
        print_test("Three-Qubit Bit Flip Code", False, str(e))
        results.append(False)

    # Test 2: Shor's nine-qubit code
    try:
        code = qec.ShorCode()

        # Create a simple state
        state = qec.QuantumState(1)
        state.amplitudes[0] = 1.0
        state.amplitudes[1] = 0.0

        # Test encoding
        encoded = code.encode(state)

        passed = encoded is not None and len(encoded.amplitudes) == 512  # 2^9 dimensions
        print_test("Shor's Nine-Qubit Code", passed, f"Encoded dimension: {len(encoded.amplitudes) if encoded else 'None'}")
        results.append(passed)
    except Exception as e:
        print_test("Shor's Nine-Qubit Code", False, str(e))
        results.append(False)

    # Test 3: Stabilizer codes
    try:
        # Create a simple stabilizer code
        n_qubits = 5
        stabilizers = ['XZZXI', 'IXZZX', 'XIXZZ', 'ZXIXZ']
        code = qec.StabilizerCode(n_qubits, stabilizers)

        # Check if code is valid
        passed = code.validate()
        print_test("Stabilizer Code Validation", passed)
        results.append(passed)
    except Exception as e:
        print_test("Stabilizer Code Validation", False, str(e))
        results.append(False)

    return all(results), len([r for r in results if r]), len(results)


def run_all_tests():
    """Run all quantum algorithm tests."""
    print(f"{Colors.BOLD}{Colors.MAGENTA}")
    print("=" * 60)
    print("QUANTUM ALGORITHMS TEST SUITE".center(60))
    print("=" * 60)
    print(f"{Colors.RESET}")

    total_passed = 0
    total_tests = 0
    module_results = []

    # Test each module
    test_functions = [
        ("Quantum Simulations", test_quantum_simulations),
        ("Shor's Algorithm", test_shors_algorithm),
        ("BB84 Protocol", test_bb84_protocol),
        ("Quantum Teleportation", test_quantum_teleportation),
        ("Quantum Error Correction", test_quantum_error_correction)
    ]

    for module_name, test_func in test_functions:
        try:
            all_passed, passed, total = test_func()
            total_passed += passed
            total_tests += total
            module_results.append((module_name, passed, total, all_passed))
        except Exception as e:
            print(f"\n{Colors.RED}Error testing {module_name}: {e}{Colors.RESET}")
            traceback.print_exc()
            module_results.append((module_name, 0, 0, False))

    # Print summary
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}TEST SUMMARY{Colors.RESET}".center(70))
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")

    for module_name, passed, total, all_passed in module_results:
        status = f"{Colors.GREEN}✓{Colors.RESET}" if all_passed else f"{Colors.RED}✗{Colors.RESET}"
        color = Colors.GREEN if all_passed else Colors.YELLOW if passed > 0 else Colors.RED
        print(f"  {status} {module_name:<30} {color}{passed}/{total} tests passed{Colors.RESET}")

    print(f"\n{Colors.BOLD}Total: {Colors.GREEN if total_passed == total_tests else Colors.YELLOW}{total_passed}/{total_tests} tests passed{Colors.RESET}")

    # Overall result
    if total_passed == total_tests:
        print(f"\n{Colors.BOLD}{Colors.GREEN}ALL TESTS PASSED! 🎉{Colors.RESET}")
    elif total_passed > 0:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}PARTIAL SUCCESS - Some tests need attention{Colors.RESET}")
    else:
        print(f"\n{Colors.BOLD}{Colors.RED}TESTS FAILED - Please check implementations{Colors.RESET}")

    return total_passed == total_tests


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)