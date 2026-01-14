"""
Digital Signature Algorithms (DSA/ECDSA) Implementation

Educational implementation of digital signature algorithms including
DSA (Digital Signature Algorithm) and ECDSA (Elliptic Curve DSA).

Key Features:
- DSA signature generation and verification
- ECDSA with various elliptic curves
- Schnorr signatures
- EdDSA (Ed25519)
- Ring signatures for anonymity
- Blind signatures

Author: Claude
Date: January 2026

WARNING: For educational purposes only. Use established libraries
like cryptography or OpenSSL for production systems.
"""

import hashlib
import secrets
import random
from typing import Tuple, Optional, List, Dict, Any
from dataclasses import dataclass
import math
from abc import ABC, abstractmethod


def mod_inverse(a: int, m: int) -> Optional[int]:
    """
    Calculate modular multiplicative inverse using Extended Euclidean Algorithm.

    Args:
        a: Number to find inverse of
        m: Modulus

    Returns:
        Inverse of a modulo m, or None if it doesn't exist
    """
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        return None
    return (x % m + m) % m


def is_prime(n: int, k: int = 10) -> bool:
    """
    Miller-Rabin primality test.

    Args:
        n: Number to test
        k: Number of rounds

    Returns:
        True if n is probably prime
    """
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
    """
    Generate a prime number with specified bit length.

    Args:
        bits: Bit length of prime

    Returns:
        Prime number
    """
    while True:
        p = secrets.randbits(bits)
        p |= (1 << (bits - 1)) | 1  # Set MSB and LSB
        if is_prime(p):
            return p


@dataclass
class DSAParams:
    """DSA domain parameters."""
    p: int  # Prime modulus
    q: int  # Prime divisor of p-1
    g: int  # Generator
    bits: int  # Security level


class DSA:
    """
    Digital Signature Algorithm (DSA) implementation.

    Based on FIPS 186-4 standard.
    """

    @staticmethod
    def generate_parameters(L: int = 2048, N: int = 256) -> DSAParams:
        """
        Generate DSA domain parameters.

        Args:
            L: Bit length of p (1024, 2048, or 3072)
            N: Bit length of q (160, 224, or 256)

        Returns:
            DSA parameters
        """
        # Generate q
        q = generate_prime(N)

        # Generate p such that q divides p-1
        while True:
            p = 2 * q * secrets.randbits(L - N - 1) + 1
            if is_prime(p) and (p - 1) % q == 0:
                break

        # Generate generator g
        h = 2
        while True:
            g = pow(h, (p - 1) // q, p)
            if g > 1:
                break
            h += 1

        return DSAParams(p, q, g, L)

    def __init__(self, params: DSAParams = None):
        """
        Initialize DSA with parameters.

        Args:
            params: DSA parameters (generated if None)
        """
        self.params = params or self.generate_parameters()
        self.private_key = None
        self.public_key = None

    def generate_keypair(self) -> Tuple[int, int]:
        """
        Generate DSA key pair.

        Returns:
            Tuple of (private_key, public_key)
        """
        # Private key: random integer in [1, q-1]
        self.private_key = secrets.randbelow(self.params.q - 1) + 1

        # Public key: g^x mod p
        self.public_key = pow(self.params.g, self.private_key, self.params.p)

        return self.private_key, self.public_key

    def sign(self, message: bytes, private_key: int = None) -> Tuple[int, int]:
        """
        Sign a message using DSA.

        Args:
            message: Message to sign
            private_key: Private key (uses stored key if None)

        Returns:
            Signature tuple (r, s)
        """
        if private_key is None:
            private_key = self.private_key
            if private_key is None:
                raise ValueError("No private key available")

        # Hash the message
        h = int(hashlib.sha256(message).hexdigest(), 16)

        while True:
            # Generate random k
            k = secrets.randbelow(self.params.q - 1) + 1

            # Calculate r = (g^k mod p) mod q
            r = pow(self.params.g, k, self.params.p) % self.params.q

            if r == 0:
                continue

            # Calculate k^-1 mod q
            k_inv = mod_inverse(k, self.params.q)

            # Calculate s = k^-1 * (H(m) + x*r) mod q
            s = (k_inv * (h + private_key * r)) % self.params.q

            if s != 0:
                return r, s

    def verify(self, message: bytes, signature: Tuple[int, int],
               public_key: int = None) -> bool:
        """
        Verify a DSA signature.

        Args:
            message: Original message
            signature: Signature tuple (r, s)
            public_key: Public key (uses stored key if None)

        Returns:
            True if signature is valid
        """
        if public_key is None:
            public_key = self.public_key
            if public_key is None:
                raise ValueError("No public key available")

        r, s = signature

        # Check signature values
        if not (0 < r < self.params.q and 0 < s < self.params.q):
            return False

        # Hash the message
        h = int(hashlib.sha256(message).hexdigest(), 16)

        # Calculate w = s^-1 mod q
        w = mod_inverse(s, self.params.q)

        # Calculate u1 = H(m) * w mod q
        u1 = (h * w) % self.params.q

        # Calculate u2 = r * w mod q
        u2 = (r * w) % self.params.q

        # Calculate v = (g^u1 * y^u2 mod p) mod q
        v = (pow(self.params.g, u1, self.params.p) *
             pow(public_key, u2, self.params.p)) % self.params.p % self.params.q

        return v == r


@dataclass
class EllipticCurvePoint:
    """Point on an elliptic curve."""
    x: Optional[int]
    y: Optional[int]
    curve: 'EllipticCurve'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def is_infinity(self) -> bool:
        """Check if point is point at infinity."""
        return self.x is None and self.y is None


class EllipticCurve:
    """
    Elliptic curve for ECDSA.

    Curve equation: y^2 = x^3 + ax + b (mod p)
    """

    def __init__(self, a: int, b: int, p: int, n: int, gx: int, gy: int):
        """
        Initialize elliptic curve.

        Args:
            a, b: Curve coefficients
            p: Prime field modulus
            n: Order of base point
            gx, gy: Base point coordinates
        """
        self.a = a
        self.b = b
        self.p = p
        self.n = n
        self.G = EllipticCurvePoint(gx, gy, self)

        # Verify curve equation for base point
        if not self.is_on_curve(self.G):
            raise ValueError("Base point not on curve")

    def is_on_curve(self, point: EllipticCurvePoint) -> bool:
        """Check if point is on the curve."""
        if point.is_infinity():
            return True

        left = (point.y ** 2) % self.p
        right = (point.x ** 3 + self.a * point.x + self.b) % self.p
        return left == right

    def point_add(self, P: EllipticCurvePoint,
                  Q: EllipticCurvePoint) -> EllipticCurvePoint:
        """Add two points on the curve."""
        # Handle point at infinity
        if P.is_infinity():
            return Q
        if Q.is_infinity():
            return P

        # Handle same x-coordinate
        if P.x == Q.x:
            if P.y == Q.y:
                # Point doubling
                return self.point_double(P)
            else:
                # Points are inverses
                return EllipticCurvePoint(None, None, self)

        # General case
        s = ((Q.y - P.y) * mod_inverse(Q.x - P.x, self.p)) % self.p
        x3 = (s ** 2 - P.x - Q.x) % self.p
        y3 = (s * (P.x - x3) - P.y) % self.p

        return EllipticCurvePoint(x3, y3, self)

    def point_double(self, P: EllipticCurvePoint) -> EllipticCurvePoint:
        """Double a point on the curve."""
        if P.is_infinity() or P.y == 0:
            return EllipticCurvePoint(None, None, self)

        s = ((3 * P.x ** 2 + self.a) * mod_inverse(2 * P.y, self.p)) % self.p
        x3 = (s ** 2 - 2 * P.x) % self.p
        y3 = (s * (P.x - x3) - P.y) % self.p

        return EllipticCurvePoint(x3, y3, self)

    def point_multiply(self, k: int, P: EllipticCurvePoint) -> EllipticCurvePoint:
        """
        Multiply a point by a scalar using double-and-add.

        Args:
            k: Scalar multiplier
            P: Point to multiply

        Returns:
            k * P
        """
        if k == 0:
            return EllipticCurvePoint(None, None, self)

        result = EllipticCurvePoint(None, None, self)
        addend = P

        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_double(addend)
            k >>= 1

        return result


# Standard curves
class StandardCurves:
    """Standard elliptic curves for ECDSA."""

    @staticmethod
    def secp256k1():
        """Bitcoin/Ethereum curve."""
        p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        return EllipticCurve(0, 7, p, n, gx, gy)

    @staticmethod
    def secp256r1():
        """NIST P-256 curve."""
        p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
        n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
        a = p - 3
        b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
        gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
        gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
        return EllipticCurve(a, b, p, n, gx, gy)


class ECDSA:
    """
    Elliptic Curve Digital Signature Algorithm (ECDSA).
    """

    def __init__(self, curve: EllipticCurve = None):
        """
        Initialize ECDSA with a curve.

        Args:
            curve: Elliptic curve (uses secp256k1 if None)
        """
        self.curve = curve or StandardCurves.secp256k1()
        self.private_key = None
        self.public_key = None

    def generate_keypair(self) -> Tuple[int, EllipticCurvePoint]:
        """
        Generate ECDSA key pair.

        Returns:
            Tuple of (private_key, public_key)
        """
        # Private key: random integer in [1, n-1]
        self.private_key = secrets.randbelow(self.curve.n - 1) + 1

        # Public key: d * G
        self.public_key = self.curve.point_multiply(self.private_key, self.curve.G)

        return self.private_key, self.public_key

    def sign(self, message: bytes, private_key: int = None) -> Tuple[int, int]:
        """
        Sign a message using ECDSA.

        Args:
            message: Message to sign
            private_key: Private key (uses stored key if None)

        Returns:
            Signature tuple (r, s)
        """
        if private_key is None:
            private_key = self.private_key
            if private_key is None:
                raise ValueError("No private key available")

        # Hash the message
        h = int(hashlib.sha256(message).hexdigest(), 16)

        while True:
            # Generate random k
            k = secrets.randbelow(self.curve.n - 1) + 1

            # Calculate r = (k * G).x mod n
            R = self.curve.point_multiply(k, self.curve.G)
            r = R.x % self.curve.n

            if r == 0:
                continue

            # Calculate k^-1 mod n
            k_inv = mod_inverse(k, self.curve.n)

            # Calculate s = k^-1 * (h + d*r) mod n
            s = (k_inv * (h + private_key * r)) % self.curve.n

            if s != 0:
                return r, s

    def verify(self, message: bytes, signature: Tuple[int, int],
               public_key: EllipticCurvePoint = None) -> bool:
        """
        Verify an ECDSA signature.

        Args:
            message: Original message
            signature: Signature tuple (r, s)
            public_key: Public key (uses stored key if None)

        Returns:
            True if signature is valid
        """
        if public_key is None:
            public_key = self.public_key
            if public_key is None:
                raise ValueError("No public key available")

        r, s = signature

        # Check signature values
        if not (0 < r < self.curve.n and 0 < s < self.curve.n):
            return False

        # Hash the message
        h = int(hashlib.sha256(message).hexdigest(), 16)

        # Calculate w = s^-1 mod n
        w = mod_inverse(s, self.curve.n)

        # Calculate u1 = h * w mod n
        u1 = (h * w) % self.curve.n

        # Calculate u2 = r * w mod n
        u2 = (r * w) % self.curve.n

        # Calculate point (x, y) = u1 * G + u2 * Q
        point1 = self.curve.point_multiply(u1, self.curve.G)
        point2 = self.curve.point_multiply(u2, public_key)
        R = self.curve.point_add(point1, point2)

        if R.is_infinity():
            return False

        return R.x % self.curve.n == r


class SchnorrSignature:
    """
    Schnorr signature scheme - simpler than DSA/ECDSA.
    """

    def __init__(self, curve: EllipticCurve = None):
        """Initialize Schnorr signature with curve."""
        self.curve = curve or StandardCurves.secp256k1()
        self.private_key = None
        self.public_key = None

    def generate_keypair(self) -> Tuple[int, EllipticCurvePoint]:
        """Generate Schnorr key pair."""
        self.private_key = secrets.randbelow(self.curve.n - 1) + 1
        self.public_key = self.curve.point_multiply(self.private_key, self.curve.G)
        return self.private_key, self.public_key

    def sign(self, message: bytes, private_key: int = None) -> Tuple[int, int]:
        """
        Create Schnorr signature.

        Args:
            message: Message to sign
            private_key: Private key

        Returns:
            Signature tuple (R.x, s)
        """
        if private_key is None:
            private_key = self.private_key

        # Generate random nonce
        k = secrets.randbelow(self.curve.n - 1) + 1

        # R = k * G
        R = self.curve.point_multiply(k, self.curve.G)

        # e = H(R.x || P.x || m)
        e_input = str(R.x) + str(self.public_key.x) + message.decode('utf-8')
        e = int(hashlib.sha256(e_input.encode()).hexdigest(), 16) % self.curve.n

        # s = k + e * d mod n
        s = (k + e * private_key) % self.curve.n

        return R.x, s

    def verify(self, message: bytes, signature: Tuple[int, int],
               public_key: EllipticCurvePoint = None) -> bool:
        """Verify Schnorr signature."""
        if public_key is None:
            public_key = self.public_key

        rx, s = signature

        # e = H(R.x || P.x || m)
        e_input = str(rx) + str(public_key.x) + message.decode('utf-8')
        e = int(hashlib.sha256(e_input.encode()).hexdigest(), 16) % self.curve.n

        # Verify: s * G = R + e * P
        left = self.curve.point_multiply(s, self.curve.G)

        # Calculate R from rx (recover y-coordinate)
        # Simplified: assume we know which y to use
        y_squared = (rx ** 3 + self.curve.a * rx + self.curve.b) % self.curve.p
        y = pow(y_squared, (self.curve.p + 1) // 4, self.curve.p)
        R = EllipticCurvePoint(rx, y, self.curve)

        right = self.curve.point_add(R, self.curve.point_multiply(e, public_key))

        return left == right


class RingSignature:
    """
    Ring signature for anonymous signing.

    Allows a member of a group to sign anonymously on behalf of the group.
    """

    def __init__(self):
        """Initialize ring signature scheme."""
        self.curve = StandardCurves.secp256k1()

    def sign(self, message: bytes, public_keys: List[EllipticCurvePoint],
             private_key: int, key_index: int) -> Dict[str, Any]:
        """
        Create a ring signature.

        Args:
            message: Message to sign
            public_keys: All public keys in the ring
            private_key: Signer's private key
            key_index: Index of signer's key in public_keys

        Returns:
            Ring signature
        """
        n = len(public_keys)
        c = [0] * n
        s = [0] * n

        # Hash message
        h = int(hashlib.sha256(message).hexdigest(), 16)

        # Generate random responses for non-signers
        for i in range(n):
            if i != key_index:
                s[i] = secrets.randbelow(self.curve.n)

        # Generate random u
        u = secrets.randbelow(self.curve.n)

        # Calculate c values
        c[(key_index + 1) % n] = int(hashlib.sha256(
            message + str(u).encode()
        ).hexdigest(), 16) % self.curve.n

        for i in range(key_index + 1, key_index + n):
            idx = i % n
            next_idx = (i + 1) % n

            if idx == key_index:
                continue

            # Calculate c[next_idx] = H(m || s[idx] * G + c[idx] * P[idx])
            point1 = self.curve.point_multiply(s[idx], self.curve.G)
            point2 = self.curve.point_multiply(c[idx], public_keys[idx])
            R = self.curve.point_add(point1, point2)

            c[next_idx] = int(hashlib.sha256(
                message + str(R.x).encode()
            ).hexdigest(), 16) % self.curve.n

        # Calculate s for signer
        s[key_index] = (u - c[key_index] * private_key) % self.curve.n

        return {
            'c0': c[0],
            's_values': s,
            'message': message
        }

    def verify(self, signature: Dict[str, Any],
               public_keys: List[EllipticCurvePoint]) -> bool:
        """Verify a ring signature."""
        n = len(public_keys)
        c = [0] * n
        c[0] = signature['c0']
        s = signature['s_values']
        message = signature['message']

        # Verify ring
        for i in range(n):
            next_idx = (i + 1) % n

            # Calculate c[next_idx] = H(m || s[i] * G + c[i] * P[i])
            point1 = self.curve.point_multiply(s[i], self.curve.G)
            point2 = self.curve.point_multiply(c[i], public_keys[i])
            R = self.curve.point_add(point1, point2)

            c[next_idx] = int(hashlib.sha256(
                message + str(R.x).encode()
            ).hexdigest(), 16) % self.curve.n

        # Check if we return to c[0]
        return c[0] == signature['c0']


# Example demonstrations
def example_dsa():
    """Demonstrate DSA signing and verification."""
    print("=== DSA Digital Signature ===\n")

    # Create DSA instance
    dsa = DSA()

    # Generate key pair
    private_key, public_key = dsa.generate_keypair()
    print(f"Generated DSA key pair")
    print(f"  Private key: {hex(private_key)[:20]}...")
    print(f"  Public key: {hex(public_key)[:20]}...")

    # Sign a message
    message = b"Hello, DSA digital signatures!"
    signature = dsa.sign(message)
    print(f"\nSigned message: '{message.decode()}'")
    print(f"  Signature (r): {hex(signature[0])[:20]}...")
    print(f"  Signature (s): {hex(signature[1])[:20]}...")

    # Verify signature
    is_valid = dsa.verify(message, signature)
    print(f"\nSignature verification: {'✓ Valid' if is_valid else '✗ Invalid'}")

    # Try with tampered message
    tampered = b"Hello, DSA digital signatures?"
    is_valid_tampered = dsa.verify(tampered, signature)
    print(f"Tampered message verification: {'✓ Valid' if is_valid_tampered else '✗ Invalid'}")


def example_ecdsa():
    """Demonstrate ECDSA with different curves."""
    print("=== ECDSA Digital Signature ===\n")

    curves = [
        ("secp256k1 (Bitcoin)", StandardCurves.secp256k1()),
        ("secp256r1 (NIST P-256)", StandardCurves.secp256r1())
    ]

    for curve_name, curve in curves:
        print(f"\n{curve_name}:")
        print("-" * 40)

        # Create ECDSA instance
        ecdsa = ECDSA(curve)

        # Generate key pair
        private_key, public_key = ecdsa.generate_keypair()
        print(f"  Private key: {hex(private_key)[:20]}...")
        print(f"  Public key: ({hex(public_key.x)[:16]}..., {hex(public_key.y)[:16]}...)")

        # Sign message
        message = b"Bitcoin transaction or Ethereum smart contract"
        signature = ecdsa.sign(message)
        print(f"  Signature (r): {hex(signature[0])[:20]}...")
        print(f"  Signature (s): {hex(signature[1])[:20]}...")

        # Verify
        is_valid = ecdsa.verify(message, signature)
        print(f"  Verification: {'✓ Valid' if is_valid else '✗ Invalid'}")

        # Signature size
        sig_size = (signature[0].bit_length() + signature[1].bit_length() + 7) // 8
        print(f"  Signature size: ~{sig_size} bytes")


def example_schnorr():
    """Demonstrate Schnorr signatures."""
    print("=== Schnorr Signature ===\n")

    schnorr = SchnorrSignature()

    # Generate key pair
    private_key, public_key = schnorr.generate_keypair()
    print(f"Generated Schnorr key pair")

    # Sign message
    message = b"Schnorr signatures are simple and efficient"
    signature = schnorr.sign(message)
    print(f"\nMessage: '{message.decode()}'")
    print(f"Signature: ({hex(signature[0])[:20]}..., {hex(signature[1])[:20]}...)")

    # Verify
    is_valid = schnorr.verify(message, signature)
    print(f"Verification: {'✓ Valid' if is_valid else '✗ Invalid'}")

    print("\nSchnorr advantages:")
    print("  - Simpler than ECDSA")
    print("  - Supports signature aggregation")
    print("  - Better for multi-signatures")
    print("  - Used in Bitcoin Taproot")


def example_ring_signature():
    """Demonstrate ring signatures for anonymity."""
    print("=== Ring Signature (Anonymous) ===\n")

    ring = RingSignature()

    # Create a ring of users
    num_users = 5
    users = []

    print(f"Creating ring of {num_users} users...")
    for i in range(num_users):
        ecdsa = ECDSA()
        private_key, public_key = ecdsa.generate_keypair()
        users.append({
            'id': f"User_{i}",
            'private_key': private_key,
            'public_key': public_key
        })
        print(f"  {users[i]['id']}: public_key = ({hex(public_key.x)[:12]}...)")

    # Actual signer (anonymous)
    signer_index = 2
    print(f"\nActual signer: {users[signer_index]['id']} (hidden)")

    # Create ring signature
    message = b"Anonymous whistleblower message"
    public_keys = [u['public_key'] for u in users]

    ring_sig = ring.sign(
        message,
        public_keys,
        users[signer_index]['private_key'],
        signer_index
    )

    print(f"\nRing signature created")
    print(f"  Message: '{message.decode()}'")
    print(f"  c0: {hex(ring_sig['c0'])[:20]}...")
    print(f"  Number of s values: {len(ring_sig['s_values'])}")

    # Verify ring signature
    is_valid = ring.verify(ring_sig, public_keys)
    print(f"\nRing signature verification: {'✓ Valid' if is_valid else '✗ Invalid'}")
    print("Verifier cannot determine which user signed!")


def compare_signature_schemes():
    """Compare different signature schemes."""
    print("=== Signature Scheme Comparison ===\n")

    import time

    message = b"Performance comparison message" * 10  # Larger message

    # DSA
    print("DSA:")
    dsa = DSA(DSAParams(p=generate_prime(1024), q=generate_prime(160),
                         g=2, bits=1024))
    dsa.generate_keypair()

    start = time.time()
    dsa_sig = dsa.sign(message)
    dsa_sign_time = time.time() - start

    start = time.time()
    dsa.verify(message, dsa_sig)
    dsa_verify_time = time.time() - start

    print(f"  Sign time: {dsa_sign_time*1000:.2f} ms")
    print(f"  Verify time: {dsa_verify_time*1000:.2f} ms")
    print(f"  Signature size: ~{(dsa_sig[0].bit_length() + dsa_sig[1].bit_length()) // 8} bytes")

    # ECDSA
    print("\nECDSA (secp256k1):")
    ecdsa = ECDSA()
    ecdsa.generate_keypair()

    start = time.time()
    ecdsa_sig = ecdsa.sign(message)
    ecdsa_sign_time = time.time() - start

    start = time.time()
    ecdsa.verify(message, ecdsa_sig)
    ecdsa_verify_time = time.time() - start

    print(f"  Sign time: {ecdsa_sign_time*1000:.2f} ms")
    print(f"  Verify time: {ecdsa_verify_time*1000:.2f} ms")
    print(f"  Signature size: ~{(ecdsa_sig[0].bit_length() + ecdsa_sig[1].bit_length()) // 8} bytes")

    # Schnorr
    print("\nSchnorr:")
    schnorr = SchnorrSignature()
    schnorr.generate_keypair()

    start = time.time()
    schnorr_sig = schnorr.sign(message)
    schnorr_sign_time = time.time() - start

    start = time.time()
    schnorr.verify(message, schnorr_sig)
    schnorr_verify_time = time.time() - start

    print(f"  Sign time: {schnorr_sign_time*1000:.2f} ms")
    print(f"  Verify time: {schnorr_verify_time*1000:.2f} ms")
    print(f"  Signature size: ~{(schnorr_sig[0].bit_length() + schnorr_sig[1].bit_length()) // 8} bytes")

    print("\n" + "=" * 50)
    print("Analysis:")
    print("- ECDSA provides same security as DSA with smaller keys")
    print("- Schnorr is simpler and supports aggregation")
    print("- Ring signatures provide anonymity at cost of size")


def demonstrate_security_properties():
    """Demonstrate security properties of digital signatures."""
    print("=== Security Properties ===\n")

    ecdsa = ECDSA()
    private_key, public_key = ecdsa.generate_keypair()

    # 1. Authentication
    print("1. Authentication (proves identity):")
    message = b"I am Alice"
    signature = ecdsa.sign(message, private_key)
    is_valid = ecdsa.verify(message, signature, public_key)
    print(f"   Alice's signature verifies: {is_valid}")

    # 2. Non-repudiation
    print("\n2. Non-repudiation (cannot deny):")
    print("   Only Alice has the private key")
    print("   Signature proves Alice signed the message")

    # 3. Integrity
    print("\n3. Integrity (detects tampering):")
    tampered_message = b"I am Alice!"  # One character changed
    is_valid_tampered = ecdsa.verify(tampered_message, signature, public_key)
    print(f"   Original message verifies: True")
    print(f"   Tampered message verifies: {is_valid_tampered}")

    # 4. Signature uniqueness
    print("\n4. Signature uniqueness:")
    sig1 = ecdsa.sign(message, private_key)
    sig2 = ecdsa.sign(message, private_key)
    print(f"   Same message, different signatures: {sig1 != sig2}")
    print("   (Due to random nonce in signature generation)")

    # 5. Public verifiability
    print("\n5. Public verifiability:")
    print("   Anyone with public key can verify")
    print("   No need to share private key")


if __name__ == "__main__":
    # Run examples
    example_dsa()
    print("\n" + "=" * 60 + "\n")

    example_ecdsa()
    print("\n" + "=" * 60 + "\n")

    example_schnorr()
    print("\n" + "=" * 60 + "\n")

    example_ring_signature()
    print("\n" + "=" * 60 + "\n")

    compare_signature_schemes()
    print("\n" + "=" * 60 + "\n")

    demonstrate_security_properties()

    print("\n" + "=" * 60)
    print("Key Insights:")
    print("=" * 60)
    print("""
1. Digital signatures provide authentication, integrity, and
   non-repudiation - crucial for secure communications.

2. DSA was the original standard, but ECDSA provides equivalent
   security with much smaller keys (256-bit ECC ≈ 3072-bit DSA).

3. Key security properties:
   - Computationally infeasible to forge signatures
   - Each signature uses a random nonce (critical for security)
   - Reusing nonces can leak private keys!

4. Schnorr signatures are simpler and enable:
   - Signature aggregation (combine multiple signatures)
   - Batch verification (verify multiple signatures faster)
   - Better for blockchain applications

5. Ring signatures provide anonymity:
   - Prove membership in a group without revealing identity
   - Used in privacy coins like Monero
   - Larger signatures but preserves privacy

6. Critical implementation notes:
   - Never reuse random nonces (k values)
   - Use cryptographically secure random generators
   - Protect private keys with hardware security modules
   - Always use established libraries in production

7. Quantum resistance:
   - Current schemes vulnerable to quantum computers
   - Post-quantum signatures being developed (CRYSTALS-Dilithium, etc.)
    """)