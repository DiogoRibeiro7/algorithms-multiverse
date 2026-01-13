#!/usr/bin/env python3
"""
RSA Encryption Implementation (Educational)

RSA (Rivest-Shamir-Adleman) is a public-key cryptosystem widely used for
secure data transmission. This is an educational implementation showing
the mathematical principles behind RSA.

WARNING: This implementation is for educational purposes only!
It lacks many security features required for production use:
- No padding schemes (OAEP, PKCS#1)
- Small key sizes
- No side-channel attack protection
- Simplified prime generation

For production, use established libraries like cryptography or PyCrypto.

Author: Algorithms Multiverse
License: MIT
"""

import random
import math
from typing import Tuple, List, Optional
import base64
import json


class RSA:
    """
    Educational RSA implementation demonstrating the algorithm.

    RSA Algorithm:
    1. Choose two large prime numbers p and q
    2. Compute n = p * q (modulus)
    3. Compute φ(n) = (p-1) * (q-1) (Euler's totient)
    4. Choose e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1 (public exponent)
    5. Compute d such that d * e ≡ 1 (mod φ(n)) (private exponent)
    6. Public key: (n, e), Private key: (n, d)

    Time Complexity: O(k³) for k-bit operations
    Space Complexity: O(k) for k-bit keys
    """

    def __init__(self, key_size: int = 1024):
        """
        Initialize RSA with specified key size.

        Args:
            key_size: Size of the key in bits (default 1024)
        """
        self.key_size = key_size
        self.public_key = None
        self.private_key = None

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """
        Compute Greatest Common Divisor using Euclid's algorithm.

        Args:
            a: First number
            b: Second number

        Returns:
            GCD of a and b
        """
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """
        Extended Euclidean Algorithm.

        Returns (gcd, x, y) such that a*x + b*y = gcd

        Args:
            a: First number
            b: Second number

        Returns:
            (gcd, x, y) tuple
        """
        if a == 0:
            return b, 0, 1

        gcd, x1, y1 = RSA.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1

        return gcd, x, y

    @staticmethod
    def mod_inverse(a: int, m: int) -> Optional[int]:
        """
        Compute modular multiplicative inverse.

        Find x such that a*x ≡ 1 (mod m)

        Args:
            a: Number to find inverse of
            m: Modulus

        Returns:
            Modular inverse or None if it doesn't exist
        """
        gcd, x, _ = RSA.extended_gcd(a, m)

        if gcd != 1:
            return None  # Modular inverse doesn't exist

        return (x % m + m) % m

    @staticmethod
    def is_prime(n: int, k: int = 5) -> bool:
        """
        Miller-Rabin primality test.

        Args:
            n: Number to test
            k: Number of rounds (higher = more accurate)

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

    @staticmethod
    def generate_prime(bits: int) -> int:
        """
        Generate a random prime number of specified bit length.

        Args:
            bits: Number of bits

        Returns:
            Prime number
        """
        while True:
            # Generate random odd number
            num = random.getrandbits(bits)
            num |= (1 << bits - 1) | 1  # Set MSB and LSB to 1

            if RSA.is_prime(num):
                return num

    def generate_keypair(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Generate RSA public and private key pair.

        Returns:
            ((n, e), (n, d)) - public and private keys
        """
        # Step 1: Generate two distinct primes p and q
        p = self.generate_prime(self.key_size // 2)
        q = self.generate_prime(self.key_size // 2)

        while p == q:
            q = self.generate_prime(self.key_size // 2)

        # Step 2: Compute n = p * q
        n = p * q

        # Step 3: Compute Euler's totient φ(n) = (p-1) * (q-1)
        phi = (p - 1) * (q - 1)

        # Step 4: Choose public exponent e
        # Common choices: 3, 17, 65537
        e = 65537  # 2^16 + 1, a popular choice

        # Ensure gcd(e, φ(n)) = 1
        while self.gcd(e, phi) != 1:
            e = random.randrange(2, phi)

        # Step 5: Compute private exponent d
        d = self.mod_inverse(e, phi)

        # Store keys
        self.public_key = (n, e)
        self.private_key = (n, d)

        # Also store prime factors for optimization (CRT)
        self.p = p
        self.q = q

        return self.public_key, self.private_key

    def encrypt(self, message: int, public_key: Tuple[int, int]) -> int:
        """
        Encrypt message using public key.

        Args:
            message: Integer message (must be < n)
            public_key: (n, e) tuple

        Returns:
            Encrypted message
        """
        n, e = public_key

        if message >= n:
            raise ValueError("Message too large for key size")

        # c = m^e mod n
        ciphertext = pow(message, e, n)
        return ciphertext

    def decrypt(self, ciphertext: int, private_key: Tuple[int, int]) -> int:
        """
        Decrypt ciphertext using private key.

        Args:
            ciphertext: Encrypted message
            private_key: (n, d) tuple

        Returns:
            Decrypted message
        """
        n, d = private_key

        # m = c^d mod n
        message = pow(ciphertext, d, n)
        return message

    def decrypt_crt(self, ciphertext: int) -> int:
        """
        Decrypt using Chinese Remainder Theorem (faster).

        Requires knowledge of p and q.

        Args:
            ciphertext: Encrypted message

        Returns:
            Decrypted message
        """
        if not hasattr(self, 'p') or not hasattr(self, 'q'):
            raise ValueError("CRT decryption requires prime factors")

        n, d = self.private_key

        # Compute d mod (p-1) and d mod (q-1)
        dp = d % (self.p - 1)
        dq = d % (self.q - 1)

        # Compute m_p = c^dp mod p and m_q = c^dq mod q
        mp = pow(ciphertext, dp, self.p)
        mq = pow(ciphertext, dq, self.q)

        # Use CRT to combine
        q_inv = self.mod_inverse(self.q, self.p)
        h = (q_inv * (mp - mq)) % self.p
        m = mq + h * self.q

        return m

    def sign(self, message: int, private_key: Tuple[int, int]) -> int:
        """
        Create digital signature for message.

        Args:
            message: Message to sign (or its hash)
            private_key: (n, d) tuple

        Returns:
            Digital signature
        """
        # Signing is same as decrypting with private key
        return self.decrypt(message, private_key)

    def verify(self, message: int, signature: int,
               public_key: Tuple[int, int]) -> bool:
        """
        Verify digital signature.

        Args:
            message: Original message (or its hash)
            signature: Digital signature
            public_key: (n, e) tuple

        Returns:
            True if signature is valid
        """
        # Verify by encrypting signature with public key
        decrypted = self.encrypt(signature, public_key)
        return decrypted == message


class RSAHelper:
    """Helper functions for RSA operations."""

    @staticmethod
    def encode_message(message: str) -> int:
        """
        Encode string message to integer.

        Args:
            message: String message

        Returns:
            Integer representation
        """
        return int.from_bytes(message.encode('utf-8'), 'big')

    @staticmethod
    def decode_message(encoded: int, length: Optional[int] = None) -> str:
        """
        Decode integer to string message.

        Args:
            encoded: Integer representation
            length: Expected byte length

        Returns:
            String message
        """
        if length:
            byte_data = encoded.to_bytes(length, 'big')
        else:
            # Calculate required bytes
            byte_length = (encoded.bit_length() + 7) // 8
            byte_data = encoded.to_bytes(byte_length, 'big')

        return byte_data.decode('utf-8', errors='ignore')

    @staticmethod
    def encrypt_string(message: str, public_key: Tuple[int, int]) -> List[int]:
        """
        Encrypt string message in chunks.

        Args:
            message: String message
            public_key: RSA public key

        Returns:
            List of encrypted chunks
        """
        n, e = public_key
        chunk_size = (n.bit_length() - 1) // 8  # Bytes per chunk

        # Split message into chunks
        chunks = []
        message_bytes = message.encode('utf-8')

        for i in range(0, len(message_bytes), chunk_size):
            chunk = message_bytes[i:i + chunk_size]
            chunk_int = int.from_bytes(chunk, 'big')
            chunks.append(chunk_int)

        # Encrypt each chunk
        rsa = RSA()
        encrypted_chunks = []
        for chunk in chunks:
            encrypted = rsa.encrypt(chunk, public_key)
            encrypted_chunks.append(encrypted)

        return encrypted_chunks

    @staticmethod
    def decrypt_string(encrypted_chunks: List[int],
                       private_key: Tuple[int, int]) -> str:
        """
        Decrypt string message from chunks.

        Args:
            encrypted_chunks: List of encrypted chunks
            private_key: RSA private key

        Returns:
            Decrypted string message
        """
        rsa = RSA()
        decrypted_bytes = b''

        for chunk in encrypted_chunks:
            decrypted_int = rsa.decrypt(chunk, private_key)
            # Calculate byte length
            byte_length = (decrypted_int.bit_length() + 7) // 8
            decrypted_bytes += decrypted_int.to_bytes(byte_length, 'big')

        return decrypted_bytes.decode('utf-8', errors='ignore')

    @staticmethod
    def export_key(key: Tuple[int, int], key_type: str = "public") -> str:
        """
        Export key to JSON string.

        Args:
            key: (n, exponent) tuple
            key_type: "public" or "private"

        Returns:
            JSON string representation
        """
        n, exponent = key
        key_data = {
            "type": key_type,
            "n": n,
            "exponent": exponent
        }
        return json.dumps(key_data)

    @staticmethod
    def import_key(key_json: str) -> Tuple[int, int]:
        """
        Import key from JSON string.

        Args:
            key_json: JSON string representation

        Returns:
            (n, exponent) tuple
        """
        key_data = json.loads(key_json)
        return (key_data["n"], key_data["exponent"])


def example_usage():
    """Demonstrate RSA functionality."""
    print("=" * 60)
    print("RSA Encryption Demonstration")
    print("=" * 60)

    # Example 1: Basic RSA Operations
    print("\n1. Basic RSA Encryption/Decryption")
    print("-" * 40)

    # Generate key pair
    rsa = RSA(key_size=512)  # Small key for demo
    public_key, private_key = rsa.generate_keypair()

    print(f"Public key (n, e):")
    print(f"  n: {public_key[0]}")
    print(f"  e: {public_key[1]}")
    print(f"\nPrivate key (n, d):")
    print(f"  n: {private_key[0]}")
    print(f"  d: {private_key[1]}")

    # Encrypt/decrypt a number
    message = 42
    encrypted = rsa.encrypt(message, public_key)
    decrypted = rsa.decrypt(encrypted, private_key)

    print(f"\nOriginal message: {message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {message == decrypted}")

    # Example 2: String Encryption
    print("\n2. String Encryption")
    print("-" * 40)

    text = "Hello, RSA!"
    print(f"Original text: '{text}'")

    # Encrypt string
    encrypted_chunks = RSAHelper.encrypt_string(text, public_key)
    print(f"Encrypted chunks: {len(encrypted_chunks)} chunks")
    print(f"First chunk: {encrypted_chunks[0]}")

    # Decrypt string
    decrypted_text = RSAHelper.decrypt_string(encrypted_chunks, private_key)
    print(f"Decrypted text: '{decrypted_text}'")
    print(f"Match: {text == decrypted_text}")

    # Example 3: Digital Signatures
    print("\n3. Digital Signatures")
    print("-" * 40)

    # Sign a message
    message_text = "This is an important document"
    message_hash = hash(message_text) % public_key[0]  # Simple hash for demo
    print(f"Message: '{message_text}'")
    print(f"Message hash: {message_hash}")

    # Create signature
    signature = rsa.sign(message_hash, private_key)
    print(f"Signature: {signature}")

    # Verify signature
    is_valid = rsa.verify(message_hash, signature, public_key)
    print(f"Signature valid: {is_valid}")

    # Try with tampered message
    tampered_hash = (message_hash + 1) % public_key[0]
    is_valid_tampered = rsa.verify(tampered_hash, signature, public_key)
    print(f"Tampered message valid: {is_valid_tampered}")

    # Example 4: CRT Optimization
    print("\n4. Chinese Remainder Theorem Optimization")
    print("-" * 40)

    import time

    large_message = 123456789
    encrypted_large = rsa.encrypt(large_message, public_key)

    # Standard decryption
    start = time.time()
    for _ in range(100):
        decrypted_standard = rsa.decrypt(encrypted_large, private_key)
    standard_time = time.time() - start

    # CRT decryption
    start = time.time()
    for _ in range(100):
        decrypted_crt = rsa.decrypt_crt(encrypted_large)
    crt_time = time.time() - start

    print(f"Standard decryption: {standard_time:.4f}s for 100 operations")
    print(f"CRT decryption: {crt_time:.4f}s for 100 operations")
    print(f"Speedup: {standard_time/crt_time:.2f}x")
    print(f"Results match: {decrypted_standard == decrypted_crt}")

    # Example 5: Key Exchange Simulation
    print("\n5. Key Exchange Simulation")
    print("-" * 40)

    # Alice generates her keys
    alice_rsa = RSA(key_size=512)
    alice_public, alice_private = alice_rsa.generate_keypair()

    # Bob generates his keys
    bob_rsa = RSA(key_size=512)
    bob_public, bob_private = bob_rsa.generate_keypair()

    print("Alice and Bob have generated their key pairs")

    # Alice sends encrypted message to Bob
    alice_message = "Meet at midnight"
    alice_encrypted = RSAHelper.encrypt_string(alice_message, bob_public)
    print(f"\nAlice encrypts with Bob's public key: '{alice_message}'")

    # Bob decrypts
    bob_decrypted = RSAHelper.decrypt_string(alice_encrypted, bob_private)
    print(f"Bob decrypts with his private key: '{bob_decrypted}'")

    # Bob sends signed response
    bob_response = "Confirmed"
    bob_response_hash = hash(bob_response) % bob_public[0]
    bob_signature = bob_rsa.sign(bob_response_hash, bob_private)
    print(f"\nBob signs response: '{bob_response}'")

    # Alice verifies
    alice_verified = alice_rsa.verify(bob_response_hash, bob_signature, bob_public)
    print(f"Alice verifies signature: {alice_verified}")

    # Example 6: Security Demonstration
    print("\n6. Security Demonstration")
    print("-" * 40)

    # Show difficulty of factorization
    small_n = 77  # 7 * 11
    print(f"Small n = {small_n}")

    # Brute force factorization (only for small numbers!)
    for i in range(2, int(small_n**0.5) + 1):
        if small_n % i == 0:
            print(f"Factored: {i} * {small_n // i}")
            break

    # Large n is computationally infeasible to factor
    print(f"\nLarge n (512-bit): {public_key[0]}")
    print("Factoring this would take astronomical time!")

    # Example 7: Key Import/Export
    print("\n7. Key Import/Export")
    print("-" * 40)

    # Export keys
    public_json = RSAHelper.export_key(public_key, "public")
    private_json = RSAHelper.export_key(private_key, "private")

    print("Exported public key (JSON):")
    print(public_json[:100] + "...")

    # Import keys
    imported_public = RSAHelper.import_key(public_json)
    print(f"\nImported successfully: {imported_public == public_key}")


if __name__ == "__main__":
    example_usage()