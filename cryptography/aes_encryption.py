"""
AES (Advanced Encryption Standard) Implementation
==================================================

Educational implementation of AES encryption algorithm (Rijndael).
Demonstrates core operations: SubBytes, ShiftRows, MixColumns, AddRoundKey.

WARNING: This is for EDUCATIONAL PURPOSES ONLY!
Use established libraries like cryptography or PyCrypto for production.

Author: Claude
Date: January 2026
"""

class AES:
    """
    AES encryption implementation supporting 128, 192, and 256-bit keys.

    This implementation shows the core AES operations for educational purposes.
    It implements ECB mode (simplest but least secure) to focus on the algorithm.
    """

    # S-box for SubBytes transformation
    SBOX = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
    ]

    # Inverse S-box for decryption
    INV_SBOX = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
    ]

    # Round constants for key expansion
    RCON = [
        0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
        0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
        0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
        0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39
    ]

    def __init__(self, key: bytes):
        """
        Initialize AES with a key.

        Args:
            key: Encryption key (16, 24, or 32 bytes for AES-128, AES-192, AES-256)
        """
        key_len = len(key)
        if key_len not in [16, 24, 32]:
            raise ValueError(f"Key must be 16, 24, or 32 bytes long, got {key_len} bytes")

        self.key = key
        self.key_size = key_len
        self.num_rounds = {16: 10, 24: 12, 32: 14}[key_len]

        # Generate round keys
        self.round_keys = self._key_expansion()

    def _key_expansion(self):
        """
        Expand the key into round keys using the AES key schedule.

        Returns:
            List of round keys
        """
        key_bytes = list(self.key)
        key_len = len(key_bytes)
        num_words = (self.num_rounds + 1) * 4

        # Initialize with original key
        expanded = key_bytes[:]

        # Expand key
        for i in range(key_len, num_words * 4):
            temp = expanded[i-4:i]

            if i % key_len == 0:
                # RotWord and SubBytes
                temp = [self.SBOX[b] for b in [temp[1], temp[2], temp[3], temp[0]]]
                # XOR with round constant
                temp[0] ^= self.RCON[i // key_len]
            elif key_len == 32 and i % key_len == 16:
                # Extra SubBytes for AES-256
                temp = [self.SBOX[b] for b in temp]

            # XOR with word from key_len positions earlier
            for j in range(4):
                expanded.append(expanded[i - key_len + j] ^ temp[j])

        # Group into round keys (16 bytes each)
        round_keys = []
        for i in range(0, len(expanded), 16):
            round_keys.append(expanded[i:i+16])

        return round_keys

    def _sub_bytes(self, state):
        """Apply S-box substitution to each byte."""
        return [[self.SBOX[byte] for byte in row] for row in state]

    def _inv_sub_bytes(self, state):
        """Apply inverse S-box substitution."""
        return [[self.INV_SBOX[byte] for byte in row] for row in state]

    def _shift_rows(self, state):
        """Shift rows of the state array."""
        result = []
        for i in range(4):
            row = [state[j][i] for j in range(4)]
            # Shift row i by i positions to the left
            shifted = row[i:] + row[:i]
            result.append(shifted)

        # Transpose back
        return [[result[i][j] for i in range(4)] for j in range(4)]

    def _inv_shift_rows(self, state):
        """Inverse shift rows operation."""
        result = []
        for i in range(4):
            row = [state[j][i] for j in range(4)]
            # Shift row i by i positions to the right
            shifted = row[-i:] + row[:-i] if i > 0 else row
            result.append(shifted)

        # Transpose back
        return [[result[i][j] for i in range(4)] for j in range(4)]

    def _mix_columns(self, state):
        """Mix columns using Galois field multiplication."""
        def galois_multiply(a, b):
            """Multiply in GF(2^8)."""
            p = 0
            for _ in range(8):
                if b & 1:
                    p ^= a
                high_bit = a & 0x80
                a <<= 1
                if high_bit:
                    a ^= 0x1B  # Irreducible polynomial
                b >>= 1
            return p & 0xFF

        result = [[0] * 4 for _ in range(4)]

        for c in range(4):
            result[c][0] = (galois_multiply(2, state[c][0]) ^
                           galois_multiply(3, state[c][1]) ^
                           state[c][2] ^ state[c][3])
            result[c][1] = (state[c][0] ^
                           galois_multiply(2, state[c][1]) ^
                           galois_multiply(3, state[c][2]) ^
                           state[c][3])
            result[c][2] = (state[c][0] ^ state[c][1] ^
                           galois_multiply(2, state[c][2]) ^
                           galois_multiply(3, state[c][3]))
            result[c][3] = (galois_multiply(3, state[c][0]) ^
                           state[c][1] ^ state[c][2] ^
                           galois_multiply(2, state[c][3]))

        return result

    def _inv_mix_columns(self, state):
        """Inverse mix columns operation."""
        def galois_multiply(a, b):
            """Multiply in GF(2^8)."""
            p = 0
            for _ in range(8):
                if b & 1:
                    p ^= a
                high_bit = a & 0x80
                a <<= 1
                if high_bit:
                    a ^= 0x1B
                b >>= 1
            return p & 0xFF

        result = [[0] * 4 for _ in range(4)]

        for c in range(4):
            result[c][0] = (galois_multiply(14, state[c][0]) ^
                           galois_multiply(11, state[c][1]) ^
                           galois_multiply(13, state[c][2]) ^
                           galois_multiply(9, state[c][3]))
            result[c][1] = (galois_multiply(9, state[c][0]) ^
                           galois_multiply(14, state[c][1]) ^
                           galois_multiply(11, state[c][2]) ^
                           galois_multiply(13, state[c][3]))
            result[c][2] = (galois_multiply(13, state[c][0]) ^
                           galois_multiply(9, state[c][1]) ^
                           galois_multiply(14, state[c][2]) ^
                           galois_multiply(11, state[c][3]))
            result[c][3] = (galois_multiply(11, state[c][0]) ^
                           galois_multiply(13, state[c][1]) ^
                           galois_multiply(9, state[c][2]) ^
                           galois_multiply(14, state[c][3]))

        return result

    def _add_round_key(self, state, round_key):
        """XOR state with round key."""
        result = []
        for i in range(4):
            col = []
            for j in range(4):
                col.append(state[i][j] ^ round_key[i * 4 + j])
            result.append(col)
        return result

    def encrypt_block(self, plaintext: bytes) -> bytes:
        """
        Encrypt a single 16-byte block.

        Args:
            plaintext: 16-byte block to encrypt

        Returns:
            16-byte encrypted block
        """
        if len(plaintext) != 16:
            raise ValueError("Block must be exactly 16 bytes")

        # Convert to state array (column-major order)
        state = []
        for i in range(4):
            state.append([plaintext[i], plaintext[i+4],
                         plaintext[i+8], plaintext[i+12]])

        # Initial round
        state = self._add_round_key(state, self.round_keys[0])

        # Main rounds
        for round_num in range(1, self.num_rounds):
            state = self._sub_bytes(state)
            state = self._shift_rows(state)
            state = self._mix_columns(state)
            state = self._add_round_key(state, self.round_keys[round_num])

        # Final round (no MixColumns)
        state = self._sub_bytes(state)
        state = self._shift_rows(state)
        state = self._add_round_key(state, self.round_keys[self.num_rounds])

        # Convert state back to bytes (column-major order)
        ciphertext = bytearray()
        for j in range(4):
            for i in range(4):
                ciphertext.append(state[i][j])

        return bytes(ciphertext)

    def decrypt_block(self, ciphertext: bytes) -> bytes:
        """
        Decrypt a single 16-byte block.

        Args:
            ciphertext: 16-byte block to decrypt

        Returns:
            16-byte decrypted block
        """
        if len(ciphertext) != 16:
            raise ValueError("Block must be exactly 16 bytes")

        # Convert to state array
        state = []
        for i in range(4):
            state.append([ciphertext[i], ciphertext[i+4],
                         ciphertext[i+8], ciphertext[i+12]])

        # Initial round
        state = self._add_round_key(state, self.round_keys[self.num_rounds])

        # Main rounds (inverse order)
        for round_num in range(self.num_rounds - 1, 0, -1):
            state = self._inv_shift_rows(state)
            state = self._inv_sub_bytes(state)
            state = self._add_round_key(state, self.round_keys[round_num])
            state = self._inv_mix_columns(state)

        # Final round
        state = self._inv_shift_rows(state)
        state = self._inv_sub_bytes(state)
        state = self._add_round_key(state, self.round_keys[0])

        # Convert state back to bytes
        plaintext = bytearray()
        for j in range(4):
            for i in range(4):
                plaintext.append(state[i][j])

        return bytes(plaintext)

    def encrypt_ecb(self, plaintext: bytes) -> bytes:
        """
        Encrypt data using ECB mode (Electronic Codebook).

        WARNING: ECB mode is insecure for most use cases!
        It doesn't hide patterns in the plaintext.

        Args:
            plaintext: Data to encrypt (will be padded to 16-byte blocks)

        Returns:
            Encrypted data
        """
        # Add PKCS#7 padding
        padding_length = 16 - (len(plaintext) % 16)
        padded = plaintext + bytes([padding_length] * padding_length)

        # Encrypt each block
        ciphertext = bytearray()
        for i in range(0, len(padded), 16):
            block = padded[i:i+16]
            ciphertext.extend(self.encrypt_block(block))

        return bytes(ciphertext)

    def decrypt_ecb(self, ciphertext: bytes) -> bytes:
        """
        Decrypt data using ECB mode.

        Args:
            ciphertext: Encrypted data (must be multiple of 16 bytes)

        Returns:
            Decrypted data with padding removed
        """
        if len(ciphertext) % 16 != 0:
            raise ValueError("Ciphertext must be multiple of 16 bytes")

        # Decrypt each block
        plaintext = bytearray()
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i+16]
            plaintext.extend(self.decrypt_block(block))

        # Remove PKCS#7 padding
        padding_length = plaintext[-1]
        if padding_length > 16:
            raise ValueError("Invalid padding")

        return bytes(plaintext[:-padding_length])


class AESModes:
    """
    Additional modes of operation for AES.

    Implements CBC (Cipher Block Chaining) and CTR (Counter) modes.
    """

    @staticmethod
    def encrypt_cbc(key: bytes, plaintext: bytes, iv: bytes) -> bytes:
        """
        Encrypt using CBC mode (Cipher Block Chaining).

        Args:
            key: AES key
            plaintext: Data to encrypt
            iv: Initialization vector (16 bytes)

        Returns:
            Encrypted data (IV prepended)
        """
        if len(iv) != 16:
            raise ValueError("IV must be 16 bytes")

        aes = AES(key)

        # Add PKCS#7 padding
        padding_length = 16 - (len(plaintext) % 16)
        padded = plaintext + bytes([padding_length] * padding_length)

        # Encrypt with CBC
        ciphertext = bytearray()
        prev_block = iv

        for i in range(0, len(padded), 16):
            block = padded[i:i+16]
            # XOR with previous ciphertext block
            xored = bytes(a ^ b for a, b in zip(block, prev_block))
            encrypted = aes.encrypt_block(xored)
            ciphertext.extend(encrypted)
            prev_block = encrypted

        # Prepend IV
        return iv + bytes(ciphertext)

    @staticmethod
    def decrypt_cbc(key: bytes, ciphertext: bytes) -> bytes:
        """
        Decrypt using CBC mode.

        Args:
            key: AES key
            ciphertext: Encrypted data (with IV prepended)

        Returns:
            Decrypted data
        """
        if len(ciphertext) < 32 or len(ciphertext) % 16 != 0:
            raise ValueError("Invalid ciphertext length")

        aes = AES(key)

        # Extract IV
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]

        # Decrypt with CBC
        plaintext = bytearray()
        prev_block = iv

        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i+16]
            decrypted = aes.decrypt_block(block)
            # XOR with previous ciphertext block
            xored = bytes(a ^ b for a, b in zip(decrypted, prev_block))
            plaintext.extend(xored)
            prev_block = block

        # Remove padding
        padding_length = plaintext[-1]
        return bytes(plaintext[:-padding_length])

    @staticmethod
    def encrypt_ctr(key: bytes, plaintext: bytes, nonce: bytes) -> bytes:
        """
        Encrypt using CTR mode (Counter).

        CTR mode turns AES into a stream cipher.

        Args:
            key: AES key
            plaintext: Data to encrypt
            nonce: 8-byte nonce

        Returns:
            Encrypted data (nonce prepended)
        """
        if len(nonce) != 8:
            raise ValueError("Nonce must be 8 bytes")

        aes = AES(key)
        ciphertext = bytearray()

        for counter, i in enumerate(range(0, len(plaintext), 16)):
            # Create counter block: nonce + counter
            counter_block = nonce + counter.to_bytes(8, 'big')
            keystream = aes.encrypt_block(counter_block)

            # XOR plaintext with keystream
            block = plaintext[i:i+16]
            for j in range(len(block)):
                ciphertext.append(block[j] ^ keystream[j])

        # Prepend nonce
        return nonce + bytes(ciphertext)

    @staticmethod
    def decrypt_ctr(key: bytes, ciphertext: bytes) -> bytes:
        """
        Decrypt using CTR mode.

        Note: CTR encryption and decryption are the same operation.

        Args:
            key: AES key
            ciphertext: Encrypted data (with nonce prepended)

        Returns:
            Decrypted data
        """
        if len(ciphertext) < 8:
            raise ValueError("Ciphertext too short")

        nonce = ciphertext[:8]
        ciphertext = ciphertext[8:]

        # CTR decryption is the same as encryption
        return AESModes.encrypt_ctr(key, ciphertext, nonce)[8:]


def example_usage():
    """Demonstrate AES encryption functionality."""
    print("=" * 60)
    print("AES ENCRYPTION DEMONSTRATION")
    print("=" * 60)

    # Test AES-128
    print("\n1. AES-128 ECB Mode:")
    key_128 = b"ThisIs16ByteKey!"  # 16 bytes = 128 bits
    aes_128 = AES(key_128)

    plaintext = b"Hello, AES World! This is a test message."
    print(f"Plaintext: {plaintext.decode()}")

    encrypted = aes_128.encrypt_ecb(plaintext)
    print(f"Encrypted (hex): {encrypted.hex()}")

    decrypted = aes_128.decrypt_ecb(encrypted)
    print(f"Decrypted: {decrypted.decode()}")

    # Test AES-256
    print("\n2. AES-256 ECB Mode:")
    key_256 = b"This_Is_A_32_Byte_Key_ForAES_256"  # 32 bytes = 256 bits
    aes_256 = AES(key_256)

    plaintext = b"AES-256 provides stronger security!"
    encrypted_256 = aes_256.encrypt_ecb(plaintext)
    decrypted_256 = aes_256.decrypt_ecb(encrypted_256)

    print(f"Plaintext: {plaintext.decode()}")
    print(f"Encrypted (hex): {encrypted_256.hex()}")
    print(f"Decrypted: {decrypted_256.decode()}")

    # Test CBC mode
    print("\n3. AES-128 CBC Mode (more secure than ECB):")
    import os
    key = b"AnotherSecretKey"
    iv = os.urandom(16)  # Random initialization vector

    plaintext = b"CBC mode hides patterns in the plaintext!"
    encrypted_cbc = AESModes.encrypt_cbc(key, plaintext, iv)
    decrypted_cbc = AESModes.decrypt_cbc(key, encrypted_cbc)

    print(f"Plaintext: {plaintext.decode()}")
    print(f"IV (hex): {iv.hex()}")
    print(f"Encrypted (hex): {encrypted_cbc.hex()}")
    print(f"Decrypted: {decrypted_cbc.decode()}")

    # Test CTR mode
    print("\n4. AES-128 CTR Mode (stream cipher mode):")
    nonce = os.urandom(8)  # Random nonce

    plaintext = b"CTR mode turns AES into a stream cipher!"
    encrypted_ctr = AESModes.encrypt_ctr(key, plaintext, nonce)
    decrypted_ctr = AESModes.decrypt_ctr(key, encrypted_ctr)

    print(f"Plaintext: {plaintext.decode()}")
    print(f"Nonce (hex): {nonce.hex()}")
    print(f"Encrypted (hex): {encrypted_ctr.hex()}")
    print(f"Decrypted: {decrypted_ctr.decode()}")

    # Demonstrate why ECB is insecure
    print("\n5. Why ECB Mode is Insecure:")
    print("-" * 40)

    # Repetitive plaintext
    repetitive = b"SAME_BLOCK_16BYT" * 3  # Same 16-byte block repeated
    print(f"Repetitive plaintext: {repetitive.decode()}")

    encrypted_ecb = aes_128.encrypt_ecb(repetitive)
    print(f"ECB encrypted (hex): {encrypted_ecb.hex()}")

    # Show that same blocks encrypt to same ciphertext
    blocks = [encrypted_ecb[i:i+16] for i in range(0, len(encrypted_ecb)-16, 16)]
    print(f"Block 1: {blocks[0].hex()}")
    print(f"Block 2: {blocks[1].hex()}")
    print(f"Block 3: {blocks[2].hex()}")
    print("Notice: All blocks are identical! Patterns preserved!")

    # Compare with CBC
    encrypted_cbc = AESModes.encrypt_cbc(key_128, repetitive, iv)
    blocks_cbc = [encrypted_cbc[i+16:i+32] for i in range(0, len(encrypted_cbc)-32, 16)]
    print(f"\nCBC Block 1: {blocks_cbc[0].hex()}")
    print(f"CBC Block 2: {blocks_cbc[1].hex()}")
    print(f"CBC Block 3: {blocks_cbc[2].hex()}")
    print("Notice: All blocks are different! Patterns hidden!")

    print("\n" + "=" * 60)
    print("SECURITY WARNINGS:")
    print("1. This is an educational implementation")
    print("2. DO NOT use for production systems")
    print("3. ECB mode is insecure - use CBC or CTR")
    print("4. Always use proper padding schemes")
    print("5. Use established libraries like 'cryptography'")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()