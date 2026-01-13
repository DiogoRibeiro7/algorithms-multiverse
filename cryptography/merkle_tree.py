#!/usr/bin/env python3
"""
Merkle Tree Implementation

A Merkle tree (hash tree) is a tree in which every leaf node is labelled with
the cryptographic hash of a data block, and every non-leaf node is labelled
with the hash of its child nodes' labels.

Applications:
- Bitcoin and other cryptocurrencies
- Distributed version control systems (Git)
- Peer-to-peer file sharing (BitTorrent)
- Certificate transparency
- Database systems (Cassandra, DynamoDB)

Author: Algorithms Multiverse
License: MIT
"""

import hashlib
from typing import List, Optional, Tuple, Union, Dict, Any
from dataclasses import dataclass
import json
import math


@dataclass
class MerkleNode:
    """Represents a node in the Merkle tree."""
    hash: str
    left: Optional['MerkleNode'] = None
    right: Optional['MerkleNode'] = None
    data: Optional[str] = None
    is_leaf: bool = False


class MerkleTree:
    """
    Merkle Tree implementation for efficient data verification.

    Features:
    - Build tree from data blocks
    - Generate and verify Merkle proofs
    - Support for odd number of leaves
    - Efficient updates and recalculation

    Time Complexity:
    - Build: O(n log n) where n is number of leaves
    - Proof generation: O(log n)
    - Proof verification: O(log n)
    Space Complexity: O(n)
    """

    def __init__(self, data_blocks: List[Union[str, bytes]],
                 hash_function=hashlib.sha256):
        """
        Initialize Merkle Tree with data blocks.

        Args:
            data_blocks: List of data to create leaves from
            hash_function: Hash function to use (default: SHA-256)
        """
        self.hash_function = hash_function
        self.leaves = []
        self.root = None
        self.tree_layers = []

        if data_blocks:
            self.build_tree(data_blocks)

    def _hash(self, data: Union[str, bytes]) -> str:
        """
        Hash data using the specified hash function.

        Args:
            data: Data to hash

        Returns:
            Hexadecimal hash string
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return self.hash_function(data).hexdigest()

    def _hash_pair(self, left: str, right: str) -> str:
        """
        Hash a pair of hashes.

        Args:
            left: Left hash
            right: Right hash

        Returns:
            Combined hash
        """
        combined = left + right
        return self._hash(combined)

    def build_tree(self, data_blocks: List[Union[str, bytes]]):
        """
        Build Merkle tree from data blocks.

        Args:
            data_blocks: List of data blocks
        """
        if not data_blocks:
            self.root = None
            return

        # Create leaf nodes
        self.leaves = []
        current_layer = []

        for data in data_blocks:
            hash_value = self._hash(data)
            node = MerkleNode(hash=hash_value, data=str(data), is_leaf=True)
            self.leaves.append(node)
            current_layer.append(node)

        self.tree_layers = [current_layer[:]]

        # Build tree layers
        while len(current_layer) > 1:
            next_layer = []

            # Process pairs
            for i in range(0, len(current_layer), 2):
                left_node = current_layer[i]

                # Handle odd number of nodes
                if i + 1 < len(current_layer):
                    right_node = current_layer[i + 1]
                else:
                    # Duplicate last node if odd number
                    right_node = left_node

                # Create parent node
                parent_hash = self._hash_pair(left_node.hash, right_node.hash)
                parent_node = MerkleNode(
                    hash=parent_hash,
                    left=left_node,
                    right=right_node
                )
                next_layer.append(parent_node)

            self.tree_layers.append(next_layer[:])
            current_layer = next_layer

        self.root = current_layer[0] if current_layer else None

    def get_root_hash(self) -> Optional[str]:
        """
        Get the root hash of the tree.

        Returns:
            Root hash or None if tree is empty
        """
        return self.root.hash if self.root else None

    def generate_proof(self, data_index: int) -> Optional[List[Tuple[str, str]]]:
        """
        Generate Merkle proof for data at given index.

        Args:
            data_index: Index of data block to prove

        Returns:
            List of (hash, position) tuples forming the proof path
        """
        if not self.leaves or data_index >= len(self.leaves):
            return None

        proof = []
        current_index = data_index

        # Traverse up the tree
        for layer in self.tree_layers[:-1]:  # Exclude root layer
            # Determine sibling index
            if current_index % 2 == 0:
                # Current is left, sibling is right
                sibling_index = current_index + 1
                position = 'right'
            else:
                # Current is right, sibling is left
                sibling_index = current_index - 1
                position = 'left'

            # Add sibling hash to proof if it exists
            if sibling_index < len(layer):
                sibling_hash = layer[sibling_index].hash
            else:
                # Use current hash if no sibling (odd number case)
                sibling_hash = layer[current_index].hash

            proof.append((sibling_hash, position))

            # Move to parent index in next layer
            current_index = current_index // 2

        return proof

    def verify_proof(self, data: Union[str, bytes], proof: List[Tuple[str, str]],
                     root_hash: str) -> bool:
        """
        Verify Merkle proof for given data.

        Args:
            data: Data to verify
            proof: Merkle proof (list of (hash, position) tuples)
            root_hash: Expected root hash

        Returns:
            True if proof is valid
        """
        # Start with hash of the data
        current_hash = self._hash(data)

        # Apply proof path
        for sibling_hash, position in proof:
            if position == 'left':
                # Sibling is on the left
                current_hash = self._hash_pair(sibling_hash, current_hash)
            else:
                # Sibling is on the right
                current_hash = self._hash_pair(current_hash, sibling_hash)

        # Check if computed root matches expected root
        return current_hash == root_hash

    def get_leaves(self) -> List[str]:
        """
        Get all leaf hashes.

        Returns:
            List of leaf hashes
        """
        return [leaf.hash for leaf in self.leaves]

    def get_tree_layers(self) -> List[List[str]]:
        """
        Get all tree layers as hashes.

        Returns:
            List of layers, each containing list of hashes
        """
        layers = []
        for layer in self.tree_layers:
            layers.append([node.hash for node in layer])
        return layers

    def visualize(self, max_width: int = 80) -> str:
        """
        Create ASCII visualization of the tree.

        Args:
            max_width: Maximum width for display

        Returns:
            String representation of tree
        """
        if not self.root:
            return "Empty tree"

        result = []
        result.append("Merkle Tree Structure:")
        result.append("=" * max_width)

        # Display each layer
        for i, layer in enumerate(reversed(self.tree_layers)):
            level = len(self.tree_layers) - i - 1
            result.append(f"\nLevel {level}:")

            for node in layer:
                # Truncate hash for display
                hash_display = node.hash[:8] + "..."
                if node.is_leaf and node.data:
                    result.append(f"  [{hash_display}] <- '{node.data[:20]}...'")
                else:
                    result.append(f"  [{hash_display}]")

        result.append("\n" + "=" * max_width)
        result.append(f"Root Hash: {self.root.hash}")

        return "\n".join(result)


class MerkleTreeAudit:
    """
    Merkle Tree with audit trail capabilities.

    Useful for maintaining a verifiable log of changes.
    """

    def __init__(self):
        """Initialize Merkle audit trail."""
        self.trees = []  # History of trees
        self.audit_log = []  # Log of operations

    def append(self, data: Union[str, bytes]):
        """
        Append data and create new tree version.

        Args:
            data: Data to append
        """
        # Get current data blocks
        if self.trees:
            current_data = self._get_current_data()
            current_data.append(data)
        else:
            current_data = [data]

        # Create new tree
        new_tree = MerkleTree(current_data)
        self.trees.append(new_tree)

        # Log operation
        self.audit_log.append({
            'operation': 'append',
            'data': str(data),
            'root_hash': new_tree.get_root_hash(),
            'tree_size': len(current_data)
        })

    def _get_current_data(self) -> List[str]:
        """Get current data from latest tree."""
        if not self.trees:
            return []

        latest_tree = self.trees[-1]
        return [node.data for node in latest_tree.leaves if node.data]

    def get_consistency_proof(self, old_size: int, new_size: int) -> List[str]:
        """
        Generate consistency proof between two tree sizes.

        Args:
            old_size: Size of old tree
            new_size: Size of new tree

        Returns:
            List of hashes forming consistency proof
        """
        if old_size >= new_size:
            return []

        # Find trees with specified sizes
        old_tree = None
        new_tree = None

        for tree in self.trees:
            if len(tree.leaves) == old_size:
                old_tree = tree
            if len(tree.leaves) == new_size:
                new_tree = tree

        if not old_tree or not new_tree:
            return []

        # Generate consistency proof
        proof = []
        # Simplified: return intermediate hashes
        for i in range(old_size, new_size):
            if i < len(new_tree.leaves):
                proof.append(new_tree.leaves[i].hash)

        return proof

    def verify_consistency(self, old_root: str, new_root: str,
                           proof: List[str]) -> bool:
        """
        Verify consistency between two tree versions.

        Args:
            old_root: Root hash of old tree
            new_root: Root hash of new tree
            proof: Consistency proof

        Returns:
            True if trees are consistent
        """
        # Simplified verification
        # In practice, this would involve reconstructing partial trees
        return old_root in str(self.trees) and new_root in str(self.trees)

    def get_audit_trail(self) -> List[Dict[str, Any]]:
        """Get complete audit trail."""
        return self.audit_log


class SparseMerkleTree:
    """
    Sparse Merkle Tree implementation.

    Efficient for large, sparse datasets where most leaves are empty.
    Used in some blockchain applications.
    """

    def __init__(self, depth: int = 256, hash_function=hashlib.sha256):
        """
        Initialize Sparse Merkle Tree.

        Args:
            depth: Tree depth (default 256 for 256-bit keys)
            hash_function: Hash function to use
        """
        self.depth = depth
        self.hash_function = hash_function
        self.nodes = {}  # Store only non-empty nodes
        self.default_hashes = self._compute_default_hashes()

    def _hash(self, data: bytes) -> bytes:
        """Hash data."""
        return self.hash_function(data).digest()

    def _compute_default_hashes(self) -> List[bytes]:
        """Compute default hashes for empty subtrees."""
        defaults = [b'\x00' * 32]  # Empty leaf

        for _ in range(self.depth):
            prev = defaults[-1]
            defaults.append(self._hash(prev + prev))

        return defaults

    def update(self, key: int, value: bytes):
        """
        Update value at key.

        Args:
            key: Key (integer index)
            value: Value to store
        """
        path = self._get_path(key)
        self._update_recursive(path, 0, value)

    def _get_path(self, key: int) -> List[bool]:
        """Get binary path to key."""
        path = []
        for i in range(self.depth):
            path.append(bool(key & (1 << (self.depth - 1 - i))))
        return path

    def _update_recursive(self, path: List[bool], depth: int, value: bytes):
        """Recursively update nodes."""
        if depth == self.depth:
            # Leaf level
            self.nodes[tuple(path)] = self._hash(value)
            return

        # Continue down the tree
        direction = path[depth]
        child_path = path[:depth+1]

        self._update_recursive(path, depth + 1, value)

        # Update current node
        left_path = path[:depth] + [False]
        right_path = path[:depth] + [True]

        left_hash = self.nodes.get(tuple(left_path),
                                   self.default_hashes[self.depth - depth - 1])
        right_hash = self.nodes.get(tuple(right_path),
                                    self.default_hashes[self.depth - depth - 1])

        self.nodes[tuple(path[:depth])] = self._hash(left_hash + right_hash)

    def get_root(self) -> bytes:
        """Get root hash."""
        return self.nodes.get((), self.default_hashes[-1])

    def generate_proof(self, key: int) -> List[Tuple[bytes, bool]]:
        """Generate membership/non-membership proof."""
        proof = []
        path = self._get_path(key)

        for depth in range(self.depth):
            sibling_path = path[:depth] + [not path[depth]]
            sibling_hash = self.nodes.get(tuple(sibling_path),
                                         self.default_hashes[self.depth - depth - 1])
            proof.append((sibling_hash, path[depth]))

        return proof


def example_usage():
    """Demonstrate Merkle tree functionality."""
    print("=" * 60)
    print("Merkle Tree Demonstration")
    print("=" * 60)

    # Example 1: Basic Merkle Tree
    print("\n1. Basic Merkle Tree")
    print("-" * 40)

    # Create tree from data blocks
    data_blocks = ["Block 0", "Block 1", "Block 2", "Block 3"]
    tree = MerkleTree(data_blocks)

    print(f"Data blocks: {data_blocks}")
    print(f"Root hash: {tree.get_root_hash()}")

    # Display tree structure
    print("\n" + tree.visualize())

    # Example 2: Merkle Proof Generation and Verification
    print("\n2. Merkle Proof")
    print("-" * 40)

    # Generate proof for "Block 2" (index 2)
    proof = tree.generate_proof(2)
    root_hash = tree.get_root_hash()

    print(f"Generating proof for 'Block 2' (index 2)")
    print("Proof path:")
    for hash_val, position in proof:
        print(f"  - {hash_val[:16]}... ({position})")

    # Verify proof
    is_valid = tree.verify_proof("Block 2", proof, root_hash)
    print(f"\nProof verification: {'Valid' if is_valid else 'Invalid'}")

    # Try invalid proof
    is_valid_fake = tree.verify_proof("Block X", proof, root_hash)
    print(f"Fake data verification: {'Valid' if is_valid_fake else 'Invalid'}")

    # Example 3: Merkle Tree with Odd Number of Leaves
    print("\n3. Odd Number of Leaves")
    print("-" * 40)

    odd_data = ["A", "B", "C", "D", "E"]  # 5 blocks
    odd_tree = MerkleTree(odd_data)

    print(f"Data blocks: {odd_data}")
    print(f"Root hash: {odd_tree.get_root_hash()}")
    print(f"Tree layers: {len(odd_tree.tree_layers)} levels")

    # Example 4: Merkle Audit Trail
    print("\n4. Merkle Audit Trail")
    print("-" * 40)

    audit = MerkleTreeAudit()

    # Simulate adding data over time
    entries = ["Transaction 1", "Transaction 2", "Transaction 3"]

    for entry in entries:
        audit.append(entry)
        print(f"Added: {entry}")
        print(f"  New root: {audit.trees[-1].get_root_hash()[:16]}...")

    # Display audit log
    print("\nAudit Log:")
    for log_entry in audit.get_audit_trail():
        print(f"  {log_entry['operation']}: {log_entry['data'][:20]}... "
              f"(size: {log_entry['tree_size']})")

    # Example 5: Large Tree Performance
    print("\n5. Large Tree Performance")
    print("-" * 40)

    import time

    sizes = [100, 1000, 10000]
    for size in sizes:
        # Create large dataset
        large_data = [f"Data_{i}" for i in range(size)]

        # Measure build time
        start = time.time()
        large_tree = MerkleTree(large_data)
        build_time = time.time() - start

        # Measure proof generation
        start = time.time()
        proof = large_tree.generate_proof(size // 2)
        proof_time = time.time() - start

        # Measure verification
        start = time.time()
        large_tree.verify_proof(large_data[size // 2], proof,
                               large_tree.get_root_hash())
        verify_time = time.time() - start

        print(f"\nSize: {size} blocks")
        print(f"  Build time: {build_time:.4f}s")
        print(f"  Proof generation: {proof_time:.6f}s")
        print(f"  Proof verification: {verify_time:.6f}s")
        print(f"  Proof size: {len(proof)} hashes")

    # Example 6: Blockchain-style Usage
    print("\n6. Blockchain-style Usage")
    print("-" * 40)

    # Simulate blockchain transactions
    transactions = [
        "Alice -> Bob: 10 BTC",
        "Bob -> Charlie: 5 BTC",
        "Charlie -> David: 3 BTC",
        "David -> Alice: 2 BTC",
        "Alice -> Charlie: 7 BTC",
        "Bob -> David: 4 BTC",
        "Charlie -> Alice: 1 BTC",
        "David -> Bob: 6 BTC"
    ]

    blockchain_tree = MerkleTree(transactions)
    merkle_root = blockchain_tree.get_root_hash()

    print(f"Block transactions: {len(transactions)}")
    print(f"Merkle root: {merkle_root[:32]}...")

    # Verify specific transaction
    tx_index = 3
    tx_proof = blockchain_tree.generate_proof(tx_index)
    tx_valid = blockchain_tree.verify_proof(transactions[tx_index],
                                           tx_proof, merkle_root)

    print(f"\nVerifying transaction {tx_index}: '{transactions[tx_index]}'")
    print(f"Proof valid: {tx_valid}")
    print(f"Proof size: {len(tx_proof) * 32} bytes "
          f"(vs {len(transactions) * 32} bytes for all hashes)")


if __name__ == "__main__":
    example_usage()