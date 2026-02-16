"""
Homomorphic Encryption Algorithms
==================================

This module implements various homomorphic encryption schemes that allow
computations on encrypted data without decrypting it first.

Key Features:
- Paillier cryptosystem (additive homomorphic)
- ElGamal encryption (multiplicative homomorphic)
- Simplified BGV scheme (somewhat homomorphic)
- Encrypted arithmetic operations
- Private data analytics examples
- Secure multi-party computation basics

Author: Algorithms Multiverse
Date: 2024
"""

import random
import math
from typing import Tuple, List, Optional, Dict, Any, Union
from dataclasses import dataclass
import numpy as np
from collections import defaultdict
import hashlib
import secrets


def gcd(a: int, b: int) -> int:
    """Compute greatest common divisor"""
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Compute least common multiple"""
    return abs(a * b) // gcd(a, b)


def mod_inverse(a: int, m: int) -> Optional[int]:
    """Compute modular multiplicative inverse"""
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y

    gcd_val, x, _ = extended_gcd(a % m, m)
    if gcd_val != 1:
        return None
    return (x % m + m) % m


def is_prime(n: int, k: int = 5) -> bool:
    """Miller-Rabin primality test"""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        a = random.randrange(2, n - 1)
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


def generate_prime(bits: int) -> int:
    """Generate a random prime number with specified bit length"""
    while True:
        p = random.getrandbits(bits)
        p |= (1 << (bits - 1)) | 1  # Set MSB and LSB to 1
        if is_prime(p):
            return p


@dataclass
class PaillierPublicKey:
    """Paillier public key"""
    n: int
    g: int
    n_sq: int

    def encrypt(self, plaintext: int) -> int:
        """Encrypt a plaintext integer"""
        if plaintext < 0 or plaintext >= self.n:
            raise ValueError(f"Plaintext must be in range [0, {self.n})")

        # Random value r where gcd(r, n) = 1
        while True:
            r = random.randrange(1, self.n)
            if gcd(r, self.n) == 1:
                break

        # Ciphertext = g^m * r^n mod n^2
        ciphertext = (pow(self.g, plaintext, self.n_sq) * pow(r, self.n, self.n_sq)) % self.n_sq
        return ciphertext


@dataclass
class PaillierPrivateKey:
    """Paillier private key"""
    lambda_n: int
    mu: int
    public_key: PaillierPublicKey

    def decrypt(self, ciphertext: int) -> int:
        """Decrypt a ciphertext"""
        n = self.public_key.n
        n_sq = self.public_key.n_sq

        # L function
        def L(x: int) -> int:
            return (x - 1) // n

        # Plaintext = L(c^lambda mod n^2) * mu mod n
        plaintext = (L(pow(ciphertext, self.lambda_n, n_sq)) * self.mu) % n
        return plaintext


class PaillierCryptosystem:
    """Paillier homomorphic encryption (additive homomorphic)"""

    def __init__(self, key_size: int = 512):
        """Initialize Paillier cryptosystem

        Args:
            key_size: Bit size of the modulus (half for each prime)
        """
        self.key_size = key_size

    def generate_keypair(self) -> Tuple[PaillierPublicKey, PaillierPrivateKey]:
        """Generate Paillier key pair"""
        # Generate two large primes
        p = generate_prime(self.key_size // 2)
        q = generate_prime(self.key_size // 2)

        n = p * q
        n_sq = n * n

        # Ensure gcd(pq, (p-1)(q-1)) = 1
        if gcd(n, (p - 1) * (q - 1)) != 1:
            return self.generate_keypair()

        # lambda = lcm(p-1, q-1)
        lambda_n = lcm(p - 1, q - 1)

        # g = n + 1 (simplest generator)
        g = n + 1

        # L function
        def L(x: int) -> int:
            return (x - 1) // n

        # mu = L(g^lambda mod n^2)^-1 mod n
        mu = mod_inverse(L(pow(g, lambda_n, n_sq)), n)

        public_key = PaillierPublicKey(n, g, n_sq)
        private_key = PaillierPrivateKey(lambda_n, mu, public_key)

        return public_key, private_key

    def add_encrypted(self, public_key: PaillierPublicKey, c1: int, c2: int) -> int:
        """Add two encrypted values (homomorphic addition)

        E(m1) * E(m2) = E(m1 + m2)
        """
        return (c1 * c2) % public_key.n_sq

    def multiply_plaintext(self, public_key: PaillierPublicKey, ciphertext: int,
                          plaintext: int) -> int:
        """Multiply encrypted value by plaintext (scalar multiplication)

        E(m)^k = E(k * m)
        """
        return pow(ciphertext, plaintext, public_key.n_sq)

    def subtract_encrypted(self, public_key: PaillierPublicKey, c1: int, c2: int) -> int:
        """Subtract two encrypted values

        E(m1) * E(m2)^-1 = E(m1 - m2)
        """
        c2_inv = mod_inverse(c2, public_key.n_sq)
        return (c1 * c2_inv) % public_key.n_sq


@dataclass
class ElGamalPublicKey:
    """ElGamal public key"""
    p: int  # Prime modulus
    g: int  # Generator
    h: int  # g^x mod p

    def encrypt(self, plaintext: int) -> Tuple[int, int]:
        """Encrypt a plaintext"""
        if plaintext < 0 or plaintext >= self.p:
            raise ValueError(f"Plaintext must be in range [0, {self.p})")

        # Random ephemeral key
        y = random.randrange(1, self.p - 1)

        # Ciphertext = (g^y, m * h^y) mod p
        c1 = pow(self.g, y, self.p)
        c2 = (plaintext * pow(self.h, y, self.p)) % self.p

        return c1, c2


@dataclass
class ElGamalPrivateKey:
    """ElGamal private key"""
    x: int  # Private exponent
    public_key: ElGamalPublicKey

    def decrypt(self, ciphertext: Tuple[int, int]) -> int:
        """Decrypt a ciphertext"""
        c1, c2 = ciphertext
        p = self.public_key.p

        # Plaintext = c2 * (c1^x)^-1 mod p
        s = pow(c1, self.x, p)
        s_inv = mod_inverse(s, p)
        plaintext = (c2 * s_inv) % p

        return plaintext


class ElGamalCryptosystem:
    """ElGamal homomorphic encryption (multiplicative homomorphic)"""

    def __init__(self, key_size: int = 512):
        """Initialize ElGamal cryptosystem"""
        self.key_size = key_size

    def generate_keypair(self) -> Tuple[ElGamalPublicKey, ElGamalPrivateKey]:
        """Generate ElGamal key pair"""
        # Generate safe prime p = 2q + 1
        while True:
            q = generate_prime(self.key_size - 1)
            p = 2 * q + 1
            if is_prime(p):
                break

        # Find generator
        g = 2
        while pow(g, q, p) == 1 or pow(g, 2, p) == 1:
            g += 1

        # Private key
        x = random.randrange(1, p - 1)

        # Public key
        h = pow(g, x, p)

        public_key = ElGamalPublicKey(p, g, h)
        private_key = ElGamalPrivateKey(x, public_key)

        return public_key, private_key

    def multiply_encrypted(self, public_key: ElGamalPublicKey,
                          ct1: Tuple[int, int], ct2: Tuple[int, int]) -> Tuple[int, int]:
        """Multiply two encrypted values (homomorphic multiplication)

        E(m1) * E(m2) = E(m1 * m2)
        """
        c1_1, c2_1 = ct1
        c1_2, c2_2 = ct2
        p = public_key.p

        # Component-wise multiplication
        c1 = (c1_1 * c1_2) % p
        c2 = (c2_1 * c2_2) % p

        return c1, c2

    def power_plaintext(self, public_key: ElGamalPublicKey,
                       ciphertext: Tuple[int, int], exponent: int) -> Tuple[int, int]:
        """Raise encrypted value to plaintext power

        E(m)^k = E(m^k)
        """
        c1, c2 = ciphertext
        p = public_key.p

        # Component-wise exponentiation
        c1_new = pow(c1, exponent, p)
        c2_new = pow(c2, exponent, p)

        return c1_new, c2_new


class SimplifiedBGV:
    """Simplified BGV scheme (somewhat homomorphic encryption)

    This is a toy implementation for educational purposes.
    Real BGV is much more complex with polynomial rings.
    """

    def __init__(self, q: int = 2**16, t: int = 256, n: int = 16):
        """Initialize simplified BGV

        Args:
            q: Ciphertext modulus
            t: Plaintext modulus
            n: Dimension (security parameter)
        """
        self.q = q
        self.t = t
        self.n = n
        self.delta = q // t

    def generate_keypair(self) -> Tuple[np.ndarray, np.ndarray]:
        """Generate key pair"""
        # Secret key: small random vector
        s = np.random.randint(-1, 2, self.n)

        # Public key: (A, b = As + te) where e is small error
        A = np.random.randint(0, self.q, (self.n, self.n))
        e = np.random.randint(-2, 3, self.n)
        b = (A @ s + self.t * e) % self.q

        public_key = (A, b)
        secret_key = s

        return public_key, secret_key

    def encrypt(self, public_key: Tuple[np.ndarray, np.ndarray],
                plaintext: int) -> Tuple[np.ndarray, int]:
        """Encrypt a plaintext"""
        A, b = public_key

        # Random small vector
        r = np.random.randint(0, 2, self.n)

        # Small errors
        e1 = np.random.randint(-2, 3, self.n)
        e2 = np.random.randint(-2, 3)

        # Ciphertext: (c1, c2)
        c1 = (A.T @ r + self.t * e1) % self.q
        c2 = (np.dot(b, r) + self.t * e2 + self.delta * plaintext) % self.q

        return c1, c2

    def decrypt(self, secret_key: np.ndarray,
                ciphertext: Tuple[np.ndarray, int]) -> int:
        """Decrypt a ciphertext"""
        c1, c2 = ciphertext
        s = secret_key

        # Compute c2 - <c1, s>
        inner = (c2 - np.dot(c1, s)) % self.q

        # Round to nearest multiple of delta
        plaintext = round(inner / self.delta) % self.t

        return int(plaintext)

    def add_encrypted(self, ct1: Tuple[np.ndarray, int],
                     ct2: Tuple[np.ndarray, int]) -> Tuple[np.ndarray, int]:
        """Add two ciphertexts (homomorphic addition)"""
        c1_1, c2_1 = ct1
        c1_2, c2_2 = ct2

        c1 = (c1_1 + c1_2) % self.q
        c2 = (c2_1 + c2_2) % self.q

        return c1, c2

    def multiply_plaintext(self, ciphertext: Tuple[np.ndarray, int],
                          scalar: int) -> Tuple[np.ndarray, int]:
        """Multiply ciphertext by plaintext scalar"""
        c1, c2 = ciphertext

        c1_new = (scalar * c1) % self.q
        c2_new = (scalar * c2) % self.q

        return c1_new, c2_new


class HomomorphicApplications:
    """Practical applications of homomorphic encryption"""

    @staticmethod
    def private_voting(candidates: List[str], votes: List[int],
                       paillier: PaillierCryptosystem) -> Dict[str, int]:
        """Implement private voting using Paillier encryption

        Args:
            candidates: List of candidate names
            votes: List of vote indices (which candidate each person voted for)
            paillier: Paillier cryptosystem instance

        Returns:
            Vote tallies without revealing individual votes
        """
        # Generate keys
        public_key, private_key = paillier.generate_keypair()

        # Encrypt individual votes
        encrypted_votes = defaultdict(list)
        for vote_idx in votes:
            # Create one-hot encoded vote
            for i, candidate in enumerate(candidates):
                if i == vote_idx:
                    encrypted_votes[candidate].append(public_key.encrypt(1))
                else:
                    encrypted_votes[candidate].append(public_key.encrypt(0))

        # Tally encrypted votes
        encrypted_tallies = {}
        for candidate in candidates:
            # Start with encryption of 0
            tally = public_key.encrypt(0)
            # Add all encrypted votes
            for vote in encrypted_votes[candidate]:
                tally = paillier.add_encrypted(public_key, tally, vote)
            encrypted_tallies[candidate] = tally

        # Decrypt tallies
        results = {}
        for candidate, encrypted_tally in encrypted_tallies.items():
            results[candidate] = private_key.decrypt(encrypted_tally)

        return results

    @staticmethod
    def private_average(values: List[int], paillier: PaillierCryptosystem) -> float:
        """Compute average of encrypted values

        Args:
            values: List of values to average
            paillier: Paillier cryptosystem instance

        Returns:
            Average without revealing individual values
        """
        public_key, private_key = paillier.generate_keypair()

        # Encrypt all values
        encrypted_values = [public_key.encrypt(val) for val in values]

        # Sum encrypted values
        encrypted_sum = encrypted_values[0]
        for enc_val in encrypted_values[1:]:
            encrypted_sum = paillier.add_encrypted(public_key, encrypted_sum, enc_val)

        # Decrypt sum
        total = private_key.decrypt(encrypted_sum)

        # Compute average
        return total / len(values)

    @staticmethod
    def private_dot_product(vec1: List[int], vec2: List[int],
                          paillier: PaillierCryptosystem) -> int:
        """Compute dot product with one encrypted vector

        Args:
            vec1: First vector (will be encrypted)
            vec2: Second vector (plaintext)
            paillier: Paillier cryptosystem instance

        Returns:
            Dot product without revealing vec1
        """
        if len(vec1) != len(vec2):
            raise ValueError("Vectors must have same length")

        public_key, private_key = paillier.generate_keypair()

        # Encrypt first vector
        encrypted_vec1 = [public_key.encrypt(val) for val in vec1]

        # Compute encrypted dot product
        encrypted_result = public_key.encrypt(0)
        for enc_val, plain_val in zip(encrypted_vec1, vec2):
            # Multiply encrypted by plaintext
            term = paillier.multiply_plaintext(public_key, enc_val, plain_val)
            # Add to result
            encrypted_result = paillier.add_encrypted(public_key, encrypted_result, term)

        # Decrypt result
        return private_key.decrypt(encrypted_result)

    @staticmethod
    def secure_comparison(a: int, b: int, bgv: SimplifiedBGV) -> bool:
        """Compare two numbers using BGV (simplified)

        This is a simplified demonstration. Real secure comparison
        is much more complex.
        """
        public_key, secret_key = bgv.generate_keypair()

        # Encrypt both values
        enc_a = bgv.encrypt(public_key, a % bgv.t)
        enc_b = bgv.encrypt(public_key, b % bgv.t)

        # Compute encrypted difference
        # Note: This is simplified - real comparison needs special circuits
        diff = bgv.add_encrypted(enc_a, bgv.multiply_plaintext(enc_b, -1))

        # Decrypt difference
        diff_plain = bgv.decrypt(secret_key, diff)

        # Check sign (simplified)
        return diff_plain < bgv.t // 2


class PrivateSetIntersection:
    """Private set intersection using homomorphic encryption"""

    def __init__(self, paillier: PaillierCryptosystem):
        """Initialize PSI protocol"""
        self.paillier = paillier

    def compute_intersection(self, set1: Set[int], set2: Set[int]) -> int:
        """Compute size of intersection without revealing sets

        This is a simplified protocol for demonstration.
        """
        public_key, private_key = self.paillier.generate_keypair()

        # Create polynomial from set1
        # P(x) = ∏(x - a) for a in set1
        def evaluate_poly(x: int, s: Set[int]) -> int:
            result = 1
            for elem in s:
                result *= (x - elem)
            return result

        # Party 2 evaluates polynomial at their elements
        encrypted_results = []
        for elem in set2:
            # Encrypt P(elem)
            # If elem in set1, P(elem) = 0
            poly_val = evaluate_poly(elem, set1) % public_key.n
            encrypted_results.append(public_key.encrypt(poly_val))

        # Count zeros (intersection size)
        # In real protocol, this would use a zero-test circuit
        intersection_size = 0
        for enc_result in encrypted_results:
            decrypted = private_key.decrypt(enc_result)
            if decrypted == 0:
                intersection_size += 1

        return intersection_size


class CloudComputation:
    """Secure cloud computation using homomorphic encryption"""

    def __init__(self):
        """Initialize cloud computation service"""
        self.paillier = PaillierCryptosystem(key_size=512)
        self.bgv = SimplifiedBGV()

    def linear_regression_encrypted(self, X_encrypted: List[List[int]],
                                   y: List[int]) -> List[int]:
        """Perform linear regression on encrypted data

        Simplified demonstration - real implementation would be more complex.
        """
        public_key, private_key = self.paillier.generate_keypair()

        n_samples = len(X_encrypted)
        n_features = len(X_encrypted[0]) if X_encrypted else 0

        # Encrypt labels
        y_encrypted = [public_key.encrypt(label) for label in y]

        # Simplified gradient descent (1 iteration for demo)
        # In reality, would need many iterations
        weights_encrypted = [public_key.encrypt(0) for _ in range(n_features)]

        # Compute encrypted gradients
        for i in range(n_samples):
            # Prediction would be dot product of weights and features
            # Simplified: just accumulate feature values
            for j in range(n_features):
                # Update weight_j
                update = self.paillier.multiply_plaintext(
                    public_key, y_encrypted[i], X_encrypted[i][j]
                )
                weights_encrypted[j] = self.paillier.add_encrypted(
                    public_key, weights_encrypted[j], update
                )

        # Decrypt weights (in practice, might keep encrypted)
        weights = [private_key.decrypt(w) for w in weights_encrypted]
        return weights

    def encrypted_search(self, database: List[Tuple[int, str]],
                        query: int) -> Optional[str]:
        """Search encrypted database

        Returns matching record without revealing query or non-matching records.
        """
        public_key, private_key = self.paillier.generate_keypair()

        # Encrypt query
        encrypted_query = public_key.encrypt(query)

        # Search (simplified - real implementation would be more sophisticated)
        for key, value in database:
            # Compute encrypted difference
            encrypted_key = public_key.encrypt(key)
            diff = self.paillier.subtract_encrypted(
                public_key, encrypted_key, encrypted_query
            )

            # Check if difference is zero (match found)
            if private_key.decrypt(diff) == 0:
                return value

        return None


def benchmark_homomorphic_operations():
    """Benchmark homomorphic encryption operations"""
    import time

    print("Benchmarking Homomorphic Encryption Operations")
    print("=" * 50)

    # Paillier benchmarks
    paillier = PaillierCryptosystem(key_size=512)
    public_key, private_key = paillier.generate_keypair()

    # Encryption speed
    plaintext = 12345
    start = time.time()
    ciphertext = public_key.encrypt(plaintext)
    enc_time = time.time() - start
    print(f"Paillier Encryption: {enc_time*1000:.2f} ms")

    # Homomorphic addition
    ct1 = public_key.encrypt(100)
    ct2 = public_key.encrypt(200)
    start = time.time()
    ct_sum = paillier.add_encrypted(public_key, ct1, ct2)
    add_time = time.time() - start
    print(f"Paillier Homomorphic Addition: {add_time*1000:.2f} ms")

    # Decryption speed
    start = time.time()
    result = private_key.decrypt(ct_sum)
    dec_time = time.time() - start
    print(f"Paillier Decryption: {dec_time*1000:.2f} ms")
    print(f"Result: {result} (expected: 300)")

    print("\n" + "-" * 50)

    # ElGamal benchmarks
    elgamal = ElGamalCryptosystem(key_size=512)
    eg_public, eg_private = elgamal.generate_keypair()

    # Encryption
    start = time.time()
    eg_ct = eg_public.encrypt(42)
    enc_time = time.time() - start
    print(f"ElGamal Encryption: {enc_time*1000:.2f} ms")

    # Homomorphic multiplication
    eg_ct1 = eg_public.encrypt(6)
    eg_ct2 = eg_public.encrypt(7)
    start = time.time()
    eg_product = elgamal.multiply_encrypted(eg_public, eg_ct1, eg_ct2)
    mult_time = time.time() - start
    print(f"ElGamal Homomorphic Multiplication: {mult_time*1000:.2f} ms")

    # Decryption
    start = time.time()
    result = eg_private.decrypt(eg_product)
    dec_time = time.time() - start
    print(f"ElGamal Decryption: {dec_time*1000:.2f} ms")
    print(f"Result: {result} (expected: 42)")


def main():
    """Demonstrate homomorphic encryption capabilities"""
    print("=" * 80)
    print("Homomorphic Encryption Demonstration")
    print("=" * 80)

    # 1. Paillier Cryptosystem (Additive Homomorphic)
    print("\n1. Paillier Cryptosystem - Additive Homomorphic Encryption")
    print("-" * 60)

    paillier = PaillierCryptosystem(key_size=512)
    public_key, private_key = paillier.generate_keypair()

    # Encrypt numbers
    a, b = 15, 25
    enc_a = public_key.encrypt(a)
    enc_b = public_key.encrypt(b)
    print(f"Original values: a = {a}, b = {b}")

    # Homomorphic addition
    enc_sum = paillier.add_encrypted(public_key, enc_a, enc_b)
    dec_sum = private_key.decrypt(enc_sum)
    print(f"Homomorphic addition: E({a}) + E({b}) = E({a + b})")
    print(f"Decrypted result: {dec_sum}")

    # Scalar multiplication
    k = 3
    enc_product = paillier.multiply_plaintext(public_key, enc_a, k)
    dec_product = private_key.decrypt(enc_product)
    print(f"Scalar multiplication: {k} * E({a}) = E({k * a})")
    print(f"Decrypted result: {dec_product}")

    # 2. ElGamal Cryptosystem (Multiplicative Homomorphic)
    print("\n2. ElGamal Cryptosystem - Multiplicative Homomorphic Encryption")
    print("-" * 60)

    elgamal = ElGamalCryptosystem(key_size=256)  # Smaller for demo
    eg_public, eg_private = elgamal.generate_keypair()

    # Encrypt numbers
    x, y = 6, 7
    enc_x = eg_public.encrypt(x)
    enc_y = eg_public.encrypt(y)
    print(f"Original values: x = {x}, y = {y}")

    # Homomorphic multiplication
    enc_product = elgamal.multiply_encrypted(eg_public, enc_x, enc_y)
    dec_product = eg_private.decrypt(enc_product)
    print(f"Homomorphic multiplication: E({x}) * E({y}) = E({x * y})")
    print(f"Decrypted result: {dec_product}")

    # 3. Private Voting System
    print("\n3. Private Voting System")
    print("-" * 60)

    candidates = ["Alice", "Bob", "Charlie"]
    votes = [0, 1, 0, 2, 1, 1, 0, 2, 1, 1]  # 10 votes
    print(f"Candidates: {candidates}")
    print(f"Number of votes: {len(votes)}")

    apps = HomomorphicApplications()
    results = apps.private_voting(candidates, votes, paillier)
    print("\nVoting Results (tallied on encrypted votes):")
    for candidate, count in results.items():
        print(f"  {candidate}: {count} votes")

    # 4. Private Average Computation
    print("\n4. Private Average Computation")
    print("-" * 60)

    salaries = [50000, 75000, 60000, 90000, 55000, 80000]
    print(f"Computing average of {len(salaries)} encrypted values")
    avg = apps.private_average(salaries, paillier)
    print(f"Average (computed on encrypted data): ${avg:,.2f}")
    print(f"Actual average: ${sum(salaries)/len(salaries):,.2f}")

    # 5. Private Dot Product
    print("\n5. Private Dot Product")
    print("-" * 60)

    vec1 = [1, 2, 3, 4, 5]
    vec2 = [5, 4, 3, 2, 1]
    print(f"Vector 1 (encrypted): {vec1}")
    print(f"Vector 2 (plaintext): {vec2}")

    dot_product = apps.private_dot_product(vec1, vec2, paillier)
    actual = sum(a * b for a, b in zip(vec1, vec2))
    print(f"Dot product (computed homomorphically): {dot_product}")
    print(f"Actual dot product: {actual}")

    # 6. Simplified BGV Scheme
    print("\n6. Simplified BGV Scheme (Somewhat Homomorphic)")
    print("-" * 60)

    bgv = SimplifiedBGV(q=2**16, t=256, n=8)
    bgv_public, bgv_secret = bgv.generate_keypair()

    # Encrypt and add
    m1, m2 = 42, 58
    enc_m1 = bgv.encrypt(bgv_public, m1)
    enc_m2 = bgv.encrypt(bgv_public, m2)
    print(f"Original values: m1 = {m1}, m2 = {m2}")

    enc_sum = bgv.add_encrypted(enc_m1, enc_m2)
    dec_sum = bgv.decrypt(bgv_secret, enc_sum)
    print(f"Homomorphic addition result: {dec_sum}")
    print(f"Expected: {m1 + m2}")

    # 7. Private Set Intersection
    print("\n7. Private Set Intersection")
    print("-" * 60)

    set1 = {1, 3, 5, 7, 9, 11}
    set2 = {2, 3, 5, 8, 11, 13}
    print(f"Set 1: {set1}")
    print(f"Set 2: {set2}")

    psi = PrivateSetIntersection(paillier)
    intersection_size = psi.compute_intersection(set1, set2)
    actual_intersection = set1 & set2
    print(f"Intersection size (computed privately): {intersection_size}")
    print(f"Actual intersection: {actual_intersection}")

    # 8. Performance Benchmarks
    print("\n8. Performance Benchmarks")
    print("-" * 60)
    benchmark_homomorphic_operations()

    # 9. Use Cases Summary
    print("\n9. Real-World Use Cases")
    print("-" * 60)
    print("• **Healthcare**: Analyze patient data without accessing it")
    print("• **Finance**: Compute credit scores on encrypted financial data")
    print("• **Cloud Computing**: Process data without cloud provider access")
    print("• **Machine Learning**: Train models on encrypted datasets")
    print("• **Blockchain**: Private smart contracts and confidential transactions")
    print("• **Government**: Secure census and statistical analysis")

    print("\n" + "=" * 80)
    print("Homomorphic encryption enables computation on encrypted data!")
    print("The future of privacy-preserving computation")
    print("=" * 80)


if __name__ == "__main__":
    main()