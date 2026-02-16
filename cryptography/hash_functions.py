#!/usr/bin/env python3
"""
Cryptographic Hash Functions Implementation

This module provides educational implementations of various hash functions including:
- MD5 (Message Digest 5)
- SHA-256 (Secure Hash Algorithm 256)
- SHA-1 (Secure Hash Algorithm 1)
- Simple hash functions for hash tables

IMPORTANT: These implementations are for educational purposes only.
For production use, always use established cryptographic libraries.

Author: Algorithms Multiverse
License: MIT
"""

import struct
from typing import Union, List
import hashlib  # For verification purposes only


class MD5:
    """
    MD5 (Message Digest 5) hash function implementation.

    Produces a 128-bit (16-byte) hash value.
    MD5 is cryptographically broken and should not be used for security.

    Time Complexity: O(n) where n is message length
    Space Complexity: O(1)
    """

    def __init__(self):
        """Initialize MD5 with constants."""
        # Initialize MD5 constants
        self.k = []
        for i in range(64):
            self.k.append(int(abs(2**32 * abs(np.sin(i + 1)))))

        # Initialize hash values
        self.h = [
            0x67452301,
            0xEFCDAB89,
            0x98BADCFE,
            0x10325476
        ]

        # Rotation amounts
        self.r = [
            7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
            5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
            4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
            6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
        ]

    def _f(self, x: int, y: int, z: int) -> int:
        """MD5 auxiliary function F."""
        return (x & y) | (~x & z)

    def _g(self, x: int, y: int, z: int) -> int:
        """MD5 auxiliary function G."""
        return (x & z) | (y & ~z)

    def _h(self, x: int, y: int, z: int) -> int:
        """MD5 auxiliary function H."""
        return x ^ y ^ z

    def _i(self, x: int, y: int, z: int) -> int:
        """MD5 auxiliary function I."""
        return y ^ (x | ~z)

    def _left_rotate(self, n: int, b: int) -> int:
        """Left rotate a 32-bit integer n by b bits."""
        n &= 0xFFFFFFFF
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

    def _pad_message(self, message: bytes) -> bytes:
        """Pad message to 512-bit blocks."""
        msg_len = len(message)
        message += b'\x80'

        # Pad with zeros until length ≡ 448 (mod 512)
        while len(message) % 64 != 56:
            message += b'\x00'

        # Append original length as 64-bit little-endian
        message += struct.pack('<Q', msg_len * 8)

        return message

    def hash(self, message: Union[str, bytes]) -> str:
        """
        Compute MD5 hash of message.

        Args:
            message: Input message (string or bytes)

        Returns:
            Hexadecimal hash string
        """
        if isinstance(message, str):
            message = message.encode('utf-8')

        # Pad message
        message = self._pad_message(message)

        # Initialize working variables
        a0, b0, c0, d0 = self.h

        # Process message in 512-bit chunks
        for chunk_start in range(0, len(message), 64):
            chunk = message[chunk_start:chunk_start + 64]

            # Break chunk into 16 32-bit words (little-endian)
            w = list(struct.unpack('<16I', chunk))

            # Initialize working variables
            a, b, c, d = a0, b0, c0, d0

            # Main loop
            for i in range(64):
                if i < 16:
                    f = self._f(b, c, d)
                    g = i
                elif i < 32:
                    f = self._g(b, c, d)
                    g = (5 * i + 1) % 16
                elif i < 48:
                    f = self._h(b, c, d)
                    g = (3 * i + 5) % 16
                else:
                    f = self._i(b, c, d)
                    g = (7 * i) % 16

                temp = (a + f + self.k[i] + w[g]) & 0xFFFFFFFF
                temp = self._left_rotate(temp, self.r[i])
                temp = (temp + b) & 0xFFFFFFFF

                a, b, c, d = d, temp, b, c

            # Add this chunk's hash to result
            a0 = (a0 + a) & 0xFFFFFFFF
            b0 = (b0 + b) & 0xFFFFFFFF
            c0 = (c0 + c) & 0xFFFFFFFF
            d0 = (d0 + d) & 0xFFFFFFFF

        # Produce final hash value (little-endian)
        digest = struct.pack('<4I', a0, b0, c0, d0)
        return digest.hex()


class SHA256:
    """
    SHA-256 (Secure Hash Algorithm 256-bit) implementation.

    Produces a 256-bit (32-byte) hash value.
    Part of the SHA-2 family, widely used and considered secure.

    Time Complexity: O(n) where n is message length
    Space Complexity: O(1)
    """

    def __init__(self):
        """Initialize SHA-256 with constants."""
        # Initialize hash values (first 32 bits of fractional parts of square roots of first 8 primes)
        self.h = [
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
            0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        ]

        # Initialize round constants (first 32 bits of fractional parts of cube roots of first 64 primes)
        self.k = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
            0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
            0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
            0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
            0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
            0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
            0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
            0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
            0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]

    def _rotr(self, n: int, b: int) -> int:
        """Right rotate a 32-bit integer n by b bits."""
        return ((n >> b) | (n << (32 - b))) & 0xFFFFFFFF

    def _pad_message(self, message: bytes) -> bytes:
        """Pad message to 512-bit blocks."""
        msg_len = len(message)
        message += b'\x80'

        # Pad with zeros until length ≡ 448 (mod 512)
        while len(message) % 64 != 56:
            message += b'\x00'

        # Append original length as 64-bit big-endian
        message += struct.pack('>Q', msg_len * 8)

        return message

    def hash(self, message: Union[str, bytes]) -> str:
        """
        Compute SHA-256 hash of message.

        Args:
            message: Input message (string or bytes)

        Returns:
            Hexadecimal hash string
        """
        if isinstance(message, str):
            message = message.encode('utf-8')

        # Pad message
        message = self._pad_message(message)

        # Initialize working variables
        h0, h1, h2, h3, h4, h5, h6, h7 = self.h

        # Process message in 512-bit chunks
        for chunk_start in range(0, len(message), 64):
            chunk = message[chunk_start:chunk_start + 64]

            # Break chunk into 16 32-bit words (big-endian)
            w = list(struct.unpack('>16I', chunk))

            # Extend to 64 words
            for i in range(16, 64):
                s0 = self._rotr(w[i-15], 7) ^ self._rotr(w[i-15], 18) ^ (w[i-15] >> 3)
                s1 = self._rotr(w[i-2], 17) ^ self._rotr(w[i-2], 19) ^ (w[i-2] >> 10)
                w.append((w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF)

            # Initialize working variables
            a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

            # Compression function main loop
            for i in range(64):
                S1 = self._rotr(e, 6) ^ self._rotr(e, 11) ^ self._rotr(e, 25)
                ch = (e & f) ^ (~e & g)
                temp1 = (h + S1 + ch + self.k[i] + w[i]) & 0xFFFFFFFF
                S0 = self._rotr(a, 2) ^ self._rotr(a, 13) ^ self._rotr(a, 22)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = (S0 + maj) & 0xFFFFFFFF

                h = g
                g = f
                f = e
                e = (d + temp1) & 0xFFFFFFFF
                d = c
                c = b
                b = a
                a = (temp1 + temp2) & 0xFFFFFFFF

            # Add compressed chunk to current hash value
            h0 = (h0 + a) & 0xFFFFFFFF
            h1 = (h1 + b) & 0xFFFFFFFF
            h2 = (h2 + c) & 0xFFFFFFFF
            h3 = (h3 + d) & 0xFFFFFFFF
            h4 = (h4 + e) & 0xFFFFFFFF
            h5 = (h5 + f) & 0xFFFFFFFF
            h6 = (h6 + g) & 0xFFFFFFFF
            h7 = (h7 + h) & 0xFFFFFFFF

        # Produce final hash value (big-endian)
        digest = struct.pack('>8I', h0, h1, h2, h3, h4, h5, h6, h7)
        return digest.hex()


class SHA1:
    """
    SHA-1 (Secure Hash Algorithm 1) implementation.

    Produces a 160-bit (20-byte) hash value.
    Cryptographically broken, should not be used for security.

    Time Complexity: O(n) where n is message length
    Space Complexity: O(1)
    """

    def __init__(self):
        """Initialize SHA-1 with constants."""
        # Initialize hash values
        self.h = [
            0x67452301,
            0xEFCDAB89,
            0x98BADCFE,
            0x10325476,
            0xC3D2E1F0
        ]

    def _left_rotate(self, n: int, b: int) -> int:
        """Left rotate a 32-bit integer n by b bits."""
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

    def _pad_message(self, message: bytes) -> bytes:
        """Pad message to 512-bit blocks."""
        msg_len = len(message)
        message += b'\x80'

        # Pad with zeros until length ≡ 448 (mod 512)
        while len(message) % 64 != 56:
            message += b'\x00'

        # Append original length as 64-bit big-endian
        message += struct.pack('>Q', msg_len * 8)

        return message

    def hash(self, message: Union[str, bytes]) -> str:
        """
        Compute SHA-1 hash of message.

        Args:
            message: Input message (string or bytes)

        Returns:
            Hexadecimal hash string
        """
        if isinstance(message, str):
            message = message.encode('utf-8')

        # Pad message
        message = self._pad_message(message)

        # Initialize working variables
        h0, h1, h2, h3, h4 = self.h

        # Process message in 512-bit chunks
        for chunk_start in range(0, len(message), 64):
            chunk = message[chunk_start:chunk_start + 64]

            # Break chunk into 16 32-bit words (big-endian)
            w = list(struct.unpack('>16I', chunk))

            # Extend to 80 words
            for i in range(16, 80):
                w.append(self._left_rotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1))

            # Initialize working variables
            a, b, c, d, e = h0, h1, h2, h3, h4

            # Main loop
            for i in range(80):
                if i < 20:
                    f = (b & c) | (~b & d)
                    k = 0x5A827999
                elif i < 40:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                elif i < 60:
                    f = (b & c) | (b & d) | (c & d)
                    k = 0x8F1BBCDC
                else:
                    f = b ^ c ^ d
                    k = 0xCA62C1D6

                temp = (self._left_rotate(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF
                e = d
                d = c
                c = self._left_rotate(b, 30)
                b = a
                a = temp

            # Add this chunk's hash to result
            h0 = (h0 + a) & 0xFFFFFFFF
            h1 = (h1 + b) & 0xFFFFFFFF
            h2 = (h2 + c) & 0xFFFFFFFF
            h3 = (h3 + d) & 0xFFFFFFFF
            h4 = (h4 + e) & 0xFFFFFFFF

        # Produce final hash value (big-endian)
        digest = struct.pack('>5I', h0, h1, h2, h3, h4)
        return digest.hex()


class SimpleHash:
    """
    Simple hash functions for hash tables and non-cryptographic uses.
    """

    @staticmethod
    def djb2(s: str) -> int:
        """
        DJB2 hash function by Dan Bernstein.
        Simple and effective for strings.
        """
        hash_value = 5381
        for char in s:
            hash_value = ((hash_value << 5) + hash_value) + ord(char)
        return hash_value & 0xFFFFFFFF

    @staticmethod
    def fnv1a(data: bytes) -> int:
        """
        FNV-1a hash function (Fowler-Noll-Vo).
        Good distribution for hash tables.
        """
        FNV_PRIME = 0x01000193
        FNV_OFFSET = 0x811C9DC5

        hash_value = FNV_OFFSET
        for byte in data:
            hash_value ^= byte
            hash_value = (hash_value * FNV_PRIME) & 0xFFFFFFFF

        return hash_value

    @staticmethod
    def murmur2(data: bytes, seed: int = 0) -> int:
        """
        MurmurHash2 - fast non-cryptographic hash.
        Good for hash tables and checksums.
        """
        M = 0x5bd1e995
        R = 24

        length = len(data)
        h = seed ^ length

        # Process 4-byte chunks
        for i in range(0, length - 3, 4):
            k = struct.unpack('<I', data[i:i+4])[0]
            k = (k * M) & 0xFFFFFFFF
            k ^= k >> R
            k = (k * M) & 0xFFFFFFFF
            h = (h * M) & 0xFFFFFFFF
            h ^= k

        # Process remaining bytes
        remainder = length % 4
        if remainder >= 3:
            h ^= data[-remainder] << 16
        if remainder >= 2:
            h ^= data[-remainder+1] << 8
        if remainder >= 1:
            h ^= data[-remainder+2]
            h = (h * M) & 0xFFFFFFFF

        # Final mix
        h ^= h >> 13
        h = (h * M) & 0xFFFFFFFF
        h ^= h >> 15

        return h

    @staticmethod
    def jenkins(data: bytes) -> int:
        """
        Jenkins one-at-a-time hash.
        Simple and effective general-purpose hash.
        """
        hash_value = 0

        for byte in data:
            hash_value += byte
            hash_value += hash_value << 10
            hash_value ^= hash_value >> 6
            hash_value &= 0xFFFFFFFF

        hash_value += hash_value << 3
        hash_value ^= hash_value >> 11
        hash_value += hash_value << 15

        return hash_value & 0xFFFFFFFF


def compare_hashes(message: str):
    """
    Compare different hash functions.

    Args:
        message: Input message to hash
    """
    print(f"Message: '{message}'")
    print("=" * 60)

    # Cryptographic hashes
    md5 = MD5()
    sha256 = SHA256()
    sha1 = SHA1()

    print("Cryptographic Hashes:")
    print(f"MD5:    {md5.hash(message)}")
    print(f"SHA-1:  {sha1.hash(message)}")
    print(f"SHA-256: {sha256.hash(message)}")

    # Verify with standard library
    print("\nVerification with hashlib:")
    print(f"MD5:    {hashlib.md5(message.encode()).hexdigest()}")
    print(f"SHA-1:  {hashlib.sha1(message.encode()).hexdigest()}")
    print(f"SHA-256: {hashlib.sha256(message.encode()).hexdigest()}")

    # Non-cryptographic hashes
    print("\nNon-Cryptographic Hashes:")
    print(f"DJB2:    {SimpleHash.djb2(message):08x}")
    print(f"FNV-1a:  {SimpleHash.fnv1a(message.encode()):08x}")
    print(f"Murmur2: {SimpleHash.murmur2(message.encode()):08x}")
    print(f"Jenkins: {SimpleHash.jenkins(message.encode()):08x}")


def collision_demo():
    """Demonstrate hash collisions and distribution."""
    print("\nHash Distribution Analysis")
    print("=" * 60)

    # Generate test strings
    test_strings = [f"test{i}" for i in range(10000)]

    # Test distribution for different hash functions
    for name, hash_func in [
        ("DJB2", lambda s: SimpleHash.djb2(s) % 1000),
        ("FNV-1a", lambda s: SimpleHash.fnv1a(s.encode()) % 1000),
        ("Murmur2", lambda s: SimpleHash.murmur2(s.encode()) % 1000),
    ]:
        buckets = {}
        for s in test_strings:
            h = hash_func(s)
            buckets[h] = buckets.get(h, 0) + 1

        # Calculate statistics
        min_bucket = min(buckets.values())
        max_bucket = max(buckets.values())
        avg_bucket = len(test_strings) / 1000

        print(f"\n{name} Distribution (10000 items, 1000 buckets):")
        print(f"  Min bucket size: {min_bucket}")
        print(f"  Max bucket size: {max_bucket}")
        print(f"  Average bucket size: {avg_bucket:.2f}")
        print(f"  Empty buckets: {1000 - len(buckets)}")


def example_usage():
    """Demonstrate hash functions."""
    print("=" * 60)
    print("Hash Functions Demonstration")
    print("=" * 60)

    # Example 1: Basic hashing
    print("\n1. Basic Hash Examples")
    print("-" * 40)

    messages = [
        "Hello, World!",
        "The quick brown fox jumps over the lazy dog",
        "",
        "a"
    ]

    for msg in messages:
        print(f"\nMessage: '{msg}' (length: {len(msg)})")
        sha256 = SHA256()
        print(f"SHA-256: {sha256.hash(msg)}")

    # Example 2: Hash comparison
    print("\n2. Hash Function Comparison")
    print("-" * 40)
    compare_hashes("Hello, World!")

    # Example 3: Avalanche effect
    print("\n3. Avalanche Effect (small change, big difference)")
    print("-" * 40)

    msg1 = "The quick brown fox"
    msg2 = "The quick brown Fox"  # Changed one letter

    sha256 = SHA256()
    hash1 = sha256.hash(msg1)
    hash2 = sha256.hash(msg2)

    print(f"Message 1: '{msg1}'")
    print(f"SHA-256:   {hash1}")
    print(f"\nMessage 2: '{msg2}'")
    print(f"SHA-256:   {hash2}")

    # Count different bits
    diff_count = sum(c1 != c2 for c1, c2 in zip(hash1, hash2))
    print(f"\nCharacters different: {diff_count}/{len(hash1)} ({diff_count/len(hash1)*100:.1f}%)")

    # Example 4: Distribution analysis
    collision_demo()

    # Example 5: Performance comparison
    print("\n4. Performance Test (hashing 1MB of data)")
    print("-" * 40)

    import time
    data = b"x" * (1024 * 1024)  # 1MB of data

    # SHA-256
    start = time.time()
    sha256 = SHA256()
    sha256.hash(data)
    sha256_time = time.time() - start

    # MD5
    start = time.time()
    md5 = MD5()
    md5.hash(data)
    md5_time = time.time() - start

    print(f"SHA-256: {sha256_time:.3f} seconds")
    print(f"MD5:     {md5_time:.3f} seconds")


# Fix for numpy import
import math

# Replace numpy functions in MD5 class
class MD5:
    """MD5 hash function implementation (fixed without numpy)."""

    def __init__(self):
        """Initialize MD5 with constants."""
        # Initialize MD5 constants
        self.k = []
        for i in range(64):
            self.k.append(int(abs(2**32 * abs(math.sin(i + 1)))))

        # Initialize hash values
        self.h = [
            0x67452301,
            0xEFCDAB89,
            0x98BADCFE,
            0x10325476
        ]

        # Rotation amounts
        self.r = [
            7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
            5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
            4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
            6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
        ]

    def _f(self, x: int, y: int, z: int) -> int:
        """MD5 auxiliary function F."""
        return (x & y) | (~x & z)

    def _g(self, x: int, y: int, z: int) -> int:
        """MD5 auxiliary function G."""
        return (x & z) | (y & ~z)

    def _h(self, x: int, y: int, z: int) -> int:
        """MD5 auxiliary function H."""
        return x ^ y ^ z

    def _i(self, x: int, y: int, z: int) -> int:
        """MD5 auxiliary function I."""
        return y ^ (x | ~z)

    def _left_rotate(self, n: int, b: int) -> int:
        """Left rotate a 32-bit integer n by b bits."""
        n &= 0xFFFFFFFF
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

    def _pad_message(self, message: bytes) -> bytes:
        """Pad message to 512-bit blocks."""
        msg_len = len(message)
        message += b'\x80'

        # Pad with zeros until length ≡ 448 (mod 512)
        while len(message) % 64 != 56:
            message += b'\x00'

        # Append original length as 64-bit little-endian
        message += struct.pack('<Q', msg_len * 8)

        return message

    def hash(self, message: Union[str, bytes]) -> str:
        """
        Compute MD5 hash of message.

        Args:
            message: Input message (string or bytes)

        Returns:
            Hexadecimal hash string
        """
        if isinstance(message, str):
            message = message.encode('utf-8')

        # Pad message
        message = self._pad_message(message)

        # Initialize working variables
        a0, b0, c0, d0 = self.h

        # Process message in 512-bit chunks
        for chunk_start in range(0, len(message), 64):
            chunk = message[chunk_start:chunk_start + 64]

            # Break chunk into 16 32-bit words (little-endian)
            w = list(struct.unpack('<16I', chunk))

            # Initialize working variables
            a, b, c, d = a0, b0, c0, d0

            # Main loop
            for i in range(64):
                if i < 16:
                    f = self._f(b, c, d)
                    g = i
                elif i < 32:
                    f = self._g(b, c, d)
                    g = (5 * i + 1) % 16
                elif i < 48:
                    f = self._h(b, c, d)
                    g = (3 * i + 5) % 16
                else:
                    f = self._i(b, c, d)
                    g = (7 * i) % 16

                temp = (a + f + self.k[i] + w[g]) & 0xFFFFFFFF
                temp = self._left_rotate(temp, self.r[i])
                temp = (temp + b) & 0xFFFFFFFF

                a, b, c, d = d, temp, b, c

            # Add this chunk's hash to result
            a0 = (a0 + a) & 0xFFFFFFFF
            b0 = (b0 + b) & 0xFFFFFFFF
            c0 = (c0 + c) & 0xFFFFFFFF
            d0 = (d0 + d) & 0xFFFFFFFF

        # Produce final hash value (little-endian)
        digest = struct.pack('<4I', a0, b0, c0, d0)
        return digest.hex()


if __name__ == "__main__":
    example_usage()