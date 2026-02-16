# Cryptography and Security Algorithms

A comprehensive collection of cryptographic algorithms and distributed systems security implementations for educational purposes.

## ⚠️ Important Security Notice

**These implementations are for EDUCATIONAL PURPOSES ONLY!**

These algorithms are simplified to demonstrate cryptographic concepts and should NOT be used in production systems. For real-world applications, always use established, audited cryptographic libraries like:
- OpenSSL
- libsodium
- Python's `cryptography` library
- Bouncy Castle

## 📚 Table of Contents

- [Overview](#overview)
- [Implemented Algorithms](#implemented-algorithms)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Algorithm Details](#algorithm-details)
- [Security Considerations](#security-considerations)
- [Applications](#applications)
- [References](#references)

## 🎯 Overview

This module provides educational implementations of fundamental cryptographic algorithms and distributed systems security mechanisms, including:

- **Hash Functions**: Cryptographic hashes for data integrity
- **Merkle Trees**: Efficient data verification structures
- **Public Key Cryptography**: RSA encryption and digital signatures
- **Distributed Systems**: Consistent hashing for scalable systems

## 📊 Implemented Algorithms

### Hash Functions (`hash_functions.py`)

| Algorithm | Type | Output Size | Security Status | Use Case |
|-----------|------|-------------|-----------------|----------|
| **MD5** | Cryptographic | 128-bit | ❌ Broken | Legacy systems, checksums |
| **SHA-1** | Cryptographic | 160-bit | ❌ Broken | Git (legacy), checksums |
| **SHA-256** | Cryptographic | 256-bit | ✅ Secure | Bitcoin, TLS, general use |
| **DJB2** | Non-crypto | 32-bit | N/A | Hash tables |
| **FNV-1a** | Non-crypto | 32-bit | N/A | Hash tables |
| **MurmurHash2** | Non-crypto | 32-bit | N/A | Hash tables, bloom filters |
| **Jenkins** | Non-crypto | 32-bit | N/A | Hash tables |

### Merkle Trees (`merkle_tree.py`)

| Feature | Description | Complexity |
|---------|-------------|------------|
| **Build Tree** | Construct from data blocks | O(n log n) |
| **Generate Proof** | Create inclusion proof | O(log n) |
| **Verify Proof** | Verify data inclusion | O(log n) |
| **Sparse Merkle Tree** | For large, sparse datasets | O(log n) |
| **Audit Trail** | Verifiable log of changes | O(n) |

### RSA Encryption (`rsa_encryption.py`)

| Operation | Description | Security |
|-----------|-------------|----------|
| **Key Generation** | Generate public/private keypair | Depends on key size |
| **Encryption** | Encrypt with public key | ✅ Secure with proper padding |
| **Decryption** | Decrypt with private key | ✅ Secure |
| **Digital Signatures** | Sign/verify messages | ✅ Secure |
| **CRT Optimization** | Fast decryption | ~4x speedup |

### Consistent Hashing (`consistent_hashing.py`)

| Implementation | Description | Use Case |
|----------------|-------------|----------|
| **Basic Consistent Hash** | Virtual nodes for distribution | Distributed cache |
| **Bounded Load** | Limit max load per node | Load balancing |
| **Rendezvous Hash** | HRW hashing | Simpler alternative |
| **Jump Hash** | Google's fast algorithm | Numbered buckets |

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/algorithms-multiverse.git
cd algorithms-multiverse/cryptography

# No external dependencies required for basic functionality
python hash_functions.py
python merkle_tree.py
python rsa_encryption.py
python consistent_hashing.py
```

## 💻 Usage Examples

### Hash Functions

```python
from hash_functions import SHA256, MD5, SimpleHash

# Cryptographic hash
sha256 = SHA256()
hash_value = sha256.hash("Hello, World!")
print(f"SHA-256: {hash_value}")

# MD5 (for legacy compatibility)
md5 = MD5()
md5_hash = md5.hash("Hello, World!")
print(f"MD5: {md5_hash}")

# Non-cryptographic hash for hash tables
djb2_hash = SimpleHash.djb2("key123")
bucket = djb2_hash % 100  # Map to bucket
```

### Merkle Trees

```python
from merkle_tree import MerkleTree

# Create Merkle tree from data blocks
data_blocks = ["Transaction 1", "Transaction 2", "Transaction 3", "Transaction 4"]
tree = MerkleTree(data_blocks)

# Get root hash (for blockchain header)
root_hash = tree.get_root_hash()
print(f"Merkle root: {root_hash}")

# Generate and verify proof
index = 2  # Prove "Transaction 3" is in the tree
proof = tree.generate_proof(index)

# Verify proof (can be done by anyone with root hash)
is_valid = tree.verify_proof("Transaction 3", proof, root_hash)
print(f"Proof valid: {is_valid}")

# Visualize tree structure
print(tree.visualize())
```

### RSA Encryption

```python
from rsa_encryption import RSA, RSAHelper

# Generate keypair
rsa = RSA(key_size=1024)  # Use 2048+ for real applications
public_key, private_key = rsa.generate_keypair()

# Encrypt message
message = "Secret message"
encrypted = RSAHelper.encrypt_string(message, public_key)

# Decrypt message
decrypted = RSAHelper.decrypt_string(encrypted, private_key)
print(f"Decrypted: {decrypted}")

# Digital signature
message_hash = hash("Important document")
signature = rsa.sign(message_hash, private_key)

# Verify signature
is_valid = rsa.verify(message_hash, signature, public_key)
print(f"Signature valid: {is_valid}")
```

### Consistent Hashing

```python
from consistent_hashing import ConsistentHash, ConsistentHashWithLoad

# Basic consistent hashing for distributed cache
ch = ConsistentHash(virtual_nodes=150)

# Add cache servers
ch.add_node("cache-server-1")
ch.add_node("cache-server-2")
ch.add_node("cache-server-3")

# Find server for a key
key = "user:12345:profile"
server = ch.get_node(key)
print(f"Key '{key}' maps to {server}")

# Get replicas for redundancy
replicas = ch.get_nodes(key, count=3)
print(f"Replicas: {replicas}")

# Handle server failure
ch.remove_node("cache-server-2")
new_server = ch.get_node(key)  # Key automatically remapped

# Bounded load for better distribution
bounded = ConsistentHashWithLoad(capacity_factor=1.25)
bounded.add_node("node1")
bounded.add_node("node2")
bounded.add_node("node3")

# Keys distributed with max 1.25x average load
for i in range(100):
    node = bounded.assign_key(f"key{i}")
```

## 📖 Algorithm Details

### SHA-256 (Secure Hash Algorithm)

**How it works:**
1. Message padding to 512-bit blocks
2. Initialize hash values with fractional parts of square roots of first 8 primes
3. Process each 512-bit chunk:
   - Extend 16 words to 64 words
   - 64 rounds of compression function
   - Update hash values
4. Produce 256-bit hash

**Properties:**
- One-way function (can't reverse)
- Avalanche effect (small change = completely different hash)
- Collision resistant (hard to find two inputs with same hash)
- Fixed output size regardless of input

### Merkle Trees

**Structure:**
- Binary tree of hashes
- Leaf nodes: Hash of data blocks
- Internal nodes: Hash of concatenated child hashes
- Root: Single hash representing entire dataset

**Merkle Proof:**
- Path from leaf to root
- List of sibling hashes
- Allows verification with O(log n) hashes instead of O(n)

**Applications:**
- Bitcoin/Blockchain: Transaction verification
- Git: Commit trees
- Certificate transparency
- Distributed databases

### RSA Algorithm

**Mathematical Foundation:**
- Based on difficulty of factoring large primes
- Uses modular exponentiation
- Public key: (n, e) where n = p×q
- Private key: (n, d) where d×e ≡ 1 (mod φ(n))

**Operations:**
- Encryption: c = m^e mod n
- Decryption: m = c^d mod n
- Signing: s = m^d mod n
- Verification: m = s^e mod n

### Consistent Hashing

**Key Concepts:**
- Hash space forms a ring (0 to 2^n-1)
- Nodes placed on ring using hash function
- Keys assigned to closest node clockwise
- Virtual nodes for better distribution

**Benefits:**
- Minimal remapping when nodes join/leave
- Only K/N keys need remapping (K=keys, N=nodes)
- Load balancing with virtual nodes
- Supports replication naturally

## 🔐 Security Considerations

### Hash Functions

**DO NOT USE MD5/SHA-1 for:**
- Password hashing
- Digital signatures
- Any security-critical application

**Use proper algorithms:**
- Passwords: bcrypt, scrypt, Argon2
- General hashing: SHA-256, SHA-3, BLAKE2

### RSA Implementation Limitations

**This implementation lacks:**
- Padding schemes (OAEP, PKCS#1)
- Side-channel attack protection
- Secure random number generation
- Large prime generation
- Key validation

**For production use:**
- Minimum 2048-bit keys (4096-bit recommended)
- Use established libraries
- Implement proper padding
- Protect against timing attacks

### Merkle Tree Security

**Considerations:**
- Hash function must be collision-resistant
- Second preimage attacks on intermediate nodes
- Tree structure can leak information
- Need secure root distribution

## 🔧 Applications

### Cryptographic Hashes

1. **Data Integrity**
   - File checksums
   - Download verification
   - Data deduplication

2. **Digital Signatures**
   - Document signing
   - Code signing
   - Certificate generation

3. **Blockchain**
   - Block hashing
   - Proof of work
   - Address generation

### Merkle Trees

1. **Blockchain/Cryptocurrency**
   - Bitcoin transaction verification
   - Ethereum state trees
   - Light client protocols

2. **Distributed Systems**
   - Anti-entropy protocols
   - Distributed databases
   - P2P file sharing

3. **Certificate Transparency**
   - SSL certificate logs
   - Audit proofs
   - Consistency proofs

### RSA Applications

1. **Secure Communication**
   - TLS/SSL certificates
   - Email encryption (PGP)
   - SSH authentication

2. **Digital Signatures**
   - Software distribution
   - Legal documents
   - Code signing

3. **Key Exchange**
   - Hybrid encryption
   - Session key distribution

### Consistent Hashing

1. **Distributed Caching**
   - Memcached
   - Redis Cluster
   - CDN cache distribution

2. **Load Balancing**
   - Web server distribution
   - Database sharding
   - Microservice routing

3. **Distributed Storage**
   - Amazon DynamoDB
   - Apache Cassandra
   - Distributed file systems

## 📊 Performance Comparisons

### Hash Function Performance

| Algorithm | Speed | Security | Use Case |
|-----------|-------|----------|----------|
| MD5 | Very Fast | ❌ Broken | Checksums only |
| SHA-1 | Fast | ❌ Broken | Legacy systems |
| SHA-256 | Moderate | ✅ Secure | General purpose |
| SHA-3 | Moderate | ✅ Secure | Future-proof |
| Non-crypto | Fastest | N/A | Hash tables |

### Consistent Hashing Variants

| Method | Add/Remove Node | Lookup | Memory |
|--------|-----------------|--------|---------|
| Basic | O(v log n) | O(log n) | O(n×v) |
| Bounded Load | O(v log n + k) | O(log n) | O(n×v + k) |
| Rendezvous | O(1) | O(n) | O(n) |
| Jump Hash | O(1) | O(1) | O(1) |

Where: v = virtual nodes, n = physical nodes, k = keys

## 📚 References

### Papers
- Rivest, Shamir, Adleman (1978). "A Method for Obtaining Digital Signatures and Public-Key Cryptosystems"
- Merkle (1987). "A Digital Signature Based on a Conventional Encryption Function"
- Karger et al. (1997). "Consistent Hashing and Random Trees"
- Lamping, Veach (2014). "A Fast, Minimal Memory, Consistent Hash Algorithm" (Jump Hash)

### Books
- "Applied Cryptography" - Bruce Schneier
- "Introduction to Modern Cryptography" - Katz & Lindell
- "Cryptography Engineering" - Ferguson, Schneier, Kohno
- "Distributed Systems" - van Steen & Tanenbaum

### Standards
- FIPS 180-4: Secure Hash Standard (SHA)
- PKCS #1: RSA Cryptography Specifications
- RFC 6962: Certificate Transparency

## 📄 License

MIT License - See [LICENSE](../../LICENSE) file for details.

## 🌟 Contributing

Contributions are welcome! Areas for improvement:
- Additional algorithms (AES, ECC, Diffie-Hellman)
- Performance optimizations
- Security enhancements (for educational purposes)
- Visualization tools
- More test cases

---

**Remember**: These implementations are for learning cryptographic concepts. Always use professionally audited libraries for production systems!

Part of the **Algorithms Multiverse** project - A comprehensive collection of algorithms across multiple programming languages.

**Last Updated**: January 2026