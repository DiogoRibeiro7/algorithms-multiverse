#!/usr/bin/env python3
"""
Consistent Hashing Implementation

Consistent hashing is a distributed hashing scheme that operates independently
of the number of servers in a distributed hash table. It provides better
distribution properties and minimal remapping when nodes are added or removed.

Applications:
- Distributed caching (Memcached, Redis Cluster)
- Load balancing
- Distributed databases (Cassandra, DynamoDB)
- Content Delivery Networks (CDNs)
- Distributed storage systems

Key Properties:
- Minimal data movement when nodes join/leave
- Balanced load distribution
- Fault tolerance
- Scalability

Author: Algorithms Multiverse
License: MIT
"""

import hashlib
import bisect
from typing import List, Dict, Optional, Any, Tuple, Callable
from collections import defaultdict
import json


class ConsistentHash:
    """
    Consistent Hashing implementation with virtual nodes.

    Features:
    - Virtual nodes for better distribution
    - Configurable hash function
    - Node weights for heterogeneous clusters
    - Replication support

    Time Complexity:
    - Add node: O(v log n) where v is virtual nodes, n is total nodes
    - Remove node: O(v log n)
    - Get node: O(log n)
    Space Complexity: O(n * v)
    """

    def __init__(self, virtual_nodes: int = 150,
                 hash_function: Callable = None):
        """
        Initialize consistent hash ring.

        Args:
            virtual_nodes: Number of virtual nodes per physical node
            hash_function: Hash function to use (default: MD5)
        """
        self.virtual_nodes = virtual_nodes
        self.hash_function = hash_function or self._default_hash
        self.ring = {}  # Hash -> Node mapping
        self.sorted_keys = []  # Sorted hash values
        self.nodes = set()  # Physical nodes
        self.node_weights = {}  # Node -> weight mapping
        self.replicas = defaultdict(list)  # Node -> virtual nodes

    def _default_hash(self, key: str) -> int:
        """
        Default hash function using MD5.

        Args:
            key: Key to hash

        Returns:
            Integer hash value
        """
        md5 = hashlib.md5(key.encode('utf-8'))
        return int(md5.hexdigest(), 16)

    def _hash_key(self, key: str) -> int:
        """
        Hash a key to a position on the ring.

        Args:
            key: Key to hash

        Returns:
            Hash value
        """
        return self.hash_function(key)

    def add_node(self, node: str, weight: float = 1.0):
        """
        Add a node to the hash ring.

        Args:
            node: Node identifier
            weight: Node weight (for heterogeneous nodes)
        """
        if node in self.nodes:
            return

        self.nodes.add(node)
        self.node_weights[node] = weight

        # Calculate virtual nodes based on weight
        num_replicas = int(self.virtual_nodes * weight)

        # Add virtual nodes
        for i in range(num_replicas):
            virtual_key = f"{node}:{i}"
            hash_value = self._hash_key(virtual_key)

            self.ring[hash_value] = node
            self.replicas[node].append(hash_value)
            bisect.insort(self.sorted_keys, hash_value)

    def remove_node(self, node: str):
        """
        Remove a node from the hash ring.

        Args:
            node: Node identifier to remove
        """
        if node not in self.nodes:
            return

        self.nodes.discard(node)

        # Remove all virtual nodes
        for hash_value in self.replicas[node]:
            del self.ring[hash_value]
            index = bisect.bisect_left(self.sorted_keys, hash_value)
            if index < len(self.sorted_keys) and \
               self.sorted_keys[index] == hash_value:
                self.sorted_keys.pop(index)

        del self.replicas[node]
        del self.node_weights[node]

    def get_node(self, key: str) -> Optional[str]:
        """
        Get the node responsible for a key.

        Args:
            key: Key to locate

        Returns:
            Node identifier or None if ring is empty
        """
        if not self.sorted_keys:
            return None

        hash_value = self._hash_key(key)

        # Find the first node with hash >= key hash
        index = bisect.bisect_right(self.sorted_keys, hash_value)

        # Wrap around to the first node if necessary
        if index == len(self.sorted_keys):
            index = 0

        return self.ring[self.sorted_keys[index]]

    def get_nodes(self, key: str, count: int = 3) -> List[str]:
        """
        Get multiple nodes for replication.

        Args:
            key: Key to locate
            count: Number of nodes to return

        Returns:
            List of node identifiers
        """
        if not self.sorted_keys:
            return []

        nodes = []
        seen = set()
        hash_value = self._hash_key(key)

        index = bisect.bisect_right(self.sorted_keys, hash_value)

        for _ in range(len(self.sorted_keys)):
            if index >= len(self.sorted_keys):
                index = 0

            node = self.ring[self.sorted_keys[index]]

            if node not in seen:
                nodes.append(node)
                seen.add(node)

                if len(nodes) >= count:
                    break

            index += 1

        return nodes

    def get_node_keys_range(self, node: str) -> List[Tuple[int, int]]:
        """
        Get the key ranges handled by a node.

        Args:
            node: Node identifier

        Returns:
            List of (start, end) hash ranges
        """
        if node not in self.nodes:
            return []

        ranges = []
        node_hashes = sorted(self.replicas[node])

        for hash_value in node_hashes:
            index = self.sorted_keys.index(hash_value)
            prev_index = (index - 1) % len(self.sorted_keys)
            start = self.sorted_keys[prev_index] + 1
            end = hash_value

            ranges.append((start, end))

        return ranges

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the hash ring.

        Returns:
            Dictionary with ring statistics
        """
        if not self.nodes:
            return {
                'nodes': 0,
                'virtual_nodes': 0,
                'load_distribution': {}
            }

        # Calculate load distribution
        load_distribution = defaultdict(int)
        total_range = 2**128  # Assuming 128-bit hash

        for node in self.nodes:
            ranges = self.get_node_keys_range(node)
            total_load = sum(end - start for start, end in ranges)
            load_percentage = (total_load / total_range) * 100
            load_distribution[node] = load_percentage

        return {
            'nodes': len(self.nodes),
            'virtual_nodes': len(self.sorted_keys),
            'avg_virtual_per_node': len(self.sorted_keys) / len(self.nodes),
            'load_distribution': dict(load_distribution)
        }


class ConsistentHashWithLoad:
    """
    Consistent hashing with bounded load.

    Ensures no node gets more than (1 + ε) times the average load.
    Based on "Consistent Hashing with Bounded Loads" by Mirrokni et al.
    """

    def __init__(self, capacity_factor: float = 1.25):
        """
        Initialize consistent hash with bounded load.

        Args:
            capacity_factor: Maximum load factor (1 + ε)
        """
        self.capacity_factor = capacity_factor
        self.ring = ConsistentHash()
        self.node_load = defaultdict(int)
        self.key_mapping = {}  # Key -> Node mapping

    def add_node(self, node: str):
        """Add a node."""
        self.ring.add_node(node)
        self._rebalance()

    def remove_node(self, node: str):
        """Remove a node and reassign its keys."""
        if node not in self.ring.nodes:
            return

        # Find keys assigned to this node
        keys_to_reassign = [k for k, n in self.key_mapping.items() if n == node]

        # Remove node
        self.ring.remove_node(node)
        del self.node_load[node]

        # Reassign keys
        for key in keys_to_reassign:
            del self.key_mapping[key]
            self.assign_key(key)

    def assign_key(self, key: str) -> str:
        """
        Assign a key to a node with bounded load.

        Args:
            key: Key to assign

        Returns:
            Assigned node
        """
        if not self.ring.nodes:
            return None

        # Calculate average load
        total_keys = sum(self.node_load.values())
        avg_load = total_keys / len(self.ring.nodes) if self.ring.nodes else 0
        max_load = int(avg_load * self.capacity_factor) + 1

        # Try primary node
        primary = self.ring.get_node(key)

        if self.node_load[primary] < max_load:
            self.node_load[primary] += 1
            self.key_mapping[key] = primary
            return primary

        # Try backup nodes
        nodes = self.ring.get_nodes(key, len(self.ring.nodes))

        for node in nodes:
            if self.node_load[node] < max_load:
                self.node_load[node] += 1
                self.key_mapping[key] = node
                return node

        # Fallback to least loaded node
        min_node = min(self.node_load.keys(),
                       key=lambda n: self.node_load[n])
        self.node_load[min_node] += 1
        self.key_mapping[key] = min_node
        return min_node

    def _rebalance(self):
        """Rebalance keys after node changes."""
        if not self.ring.nodes:
            return

        # Recalculate limits
        total_keys = sum(self.node_load.values())
        avg_load = total_keys / len(self.ring.nodes)
        max_load = int(avg_load * self.capacity_factor) + 1

        # Find overloaded nodes
        overloaded = [n for n, load in self.node_load.items()
                      if load > max_load]

        for node in overloaded:
            # Move excess keys
            excess = self.node_load[node] - max_load
            keys_to_move = [k for k, n in self.key_mapping.items()
                           if n == node][:excess]

            for key in keys_to_move:
                del self.key_mapping[key]
                self.node_load[node] -= 1
                self.assign_key(key)


class RendezvousHash:
    """
    Rendezvous Hashing (Highest Random Weight).

    Alternative to consistent hashing with simpler implementation.
    """

    def __init__(self, hash_function: Callable = None):
        """
        Initialize rendezvous hash.

        Args:
            hash_function: Hash function to use
        """
        self.nodes = set()
        self.hash_function = hash_function or self._default_hash

    def _default_hash(self, key: str) -> int:
        """Default hash function."""
        return int(hashlib.sha256(key.encode()).hexdigest(), 16)

    def add_node(self, node: str):
        """Add a node."""
        self.nodes.add(node)

    def remove_node(self, node: str):
        """Remove a node."""
        self.nodes.discard(node)

    def get_node(self, key: str) -> Optional[str]:
        """
        Get node for key using HRW.

        Args:
            key: Key to locate

        Returns:
            Node with highest weight
        """
        if not self.nodes:
            return None

        max_weight = -1
        selected_node = None

        for node in self.nodes:
            combined = f"{key}:{node}"
            weight = self.hash_function(combined)

            if weight > max_weight:
                max_weight = weight
                selected_node = node

        return selected_node

    def get_nodes(self, key: str, count: int = 3) -> List[str]:
        """Get multiple nodes sorted by weight."""
        weights = []

        for node in self.nodes:
            combined = f"{key}:{node}"
            weight = self.hash_function(combined)
            weights.append((weight, node))

        weights.sort(reverse=True)
        return [node for _, node in weights[:count]]


class JumpHash:
    """
    Jump Consistent Hash - Google's algorithm.

    Very fast and simple, but doesn't support arbitrary node names.
    Nodes are numbered 0 to n-1.
    """

    @staticmethod
    def hash(key: int, num_buckets: int) -> int:
        """
        Jump consistent hash algorithm.

        Args:
            key: Integer key
            num_buckets: Number of buckets

        Returns:
            Bucket number (0 to num_buckets-1)
        """
        b = -1
        j = 0

        while j < num_buckets:
            b = j
            key = ((key * 2862933555777941757) + 1) & 0xFFFFFFFFFFFFFFFF
            j = int((b + 1) * (2**31 / ((key >> 33) + 1)))

        return b


def visualize_ring(ch: ConsistentHash, keys: List[str] = None):
    """
    Visualize the hash ring distribution.

    Args:
        ch: ConsistentHash instance
        keys: Optional keys to show placement
    """
    if not ch.nodes:
        print("Empty ring")
        return

    print("\nHash Ring Visualization")
    print("=" * 60)

    # Show nodes and virtual nodes
    print(f"Physical nodes: {len(ch.nodes)}")
    print(f"Virtual nodes: {len(ch.sorted_keys)}")
    print(f"Virtual nodes per physical node: {ch.virtual_nodes}")

    # Show ring segments
    print("\nRing segments (first 10):")
    for i, hash_val in enumerate(ch.sorted_keys[:10]):
        node = ch.ring[hash_val]
        print(f"  {i}: {hash_val:040x} -> {node}")

    # Show load distribution
    stats = ch.get_stats()
    print("\nLoad distribution:")
    for node, load in stats['load_distribution'].items():
        print(f"  {node}: {load:.2f}%")

    # Show key placement
    if keys:
        print("\nKey placement:")
        for key in keys:
            node = ch.get_node(key)
            hash_val = ch._hash_key(key)
            print(f"  '{key}' (hash: {hash_val:020x}) -> {node}")


def example_usage():
    """Demonstrate consistent hashing."""
    print("=" * 60)
    print("Consistent Hashing Demonstration")
    print("=" * 60)

    # Example 1: Basic Consistent Hashing
    print("\n1. Basic Consistent Hashing")
    print("-" * 40)

    ch = ConsistentHash(virtual_nodes=50)

    # Add nodes
    nodes = ["server1", "server2", "server3"]
    for node in nodes:
        ch.add_node(node)

    print(f"Added nodes: {nodes}")

    # Test key distribution
    keys = ["user:1", "user:2", "user:3", "session:abc", "cache:xyz"]
    key_mapping = {}

    for key in keys:
        node = ch.get_node(key)
        key_mapping[key] = node
        print(f"  Key '{key}' -> {node}")

    # Example 2: Node Addition/Removal
    print("\n2. Node Addition/Removal")
    print("-" * 40)

    print("Adding server4...")
    ch.add_node("server4")

    # Check key remapping
    remapped = 0
    for key in keys:
        new_node = ch.get_node(key)
        if new_node != key_mapping[key]:
            print(f"  Key '{key}' moved: {key_mapping[key]} -> {new_node}")
            remapped += 1

    print(f"Keys remapped: {remapped}/{len(keys)} ({remapped/len(keys)*100:.1f}%)")

    print("\nRemoving server2...")
    ch.remove_node("server2")

    # Check remapping again
    for key in keys:
        new_node = ch.get_node(key)
        if key_mapping[key] == "server2":
            print(f"  Key '{key}' from server2 -> {new_node}")

    # Example 3: Replication
    print("\n3. Replication Support")
    print("-" * 40)

    key = "important:data"
    replicas = ch.get_nodes(key, count=3)
    print(f"Replicas for '{key}': {replicas}")

    # Example 4: Weighted Nodes
    print("\n4. Weighted Nodes (Heterogeneous Cluster)")
    print("-" * 40)

    weighted_ch = ConsistentHash(virtual_nodes=40)

    # Add nodes with different capacities
    weighted_ch.add_node("small_server", weight=0.5)
    weighted_ch.add_node("medium_server", weight=1.0)
    weighted_ch.add_node("large_server", weight=2.0)

    print("Node weights:")
    print("  small_server: 0.5x capacity")
    print("  medium_server: 1.0x capacity")
    print("  large_server: 2.0x capacity")

    # Test distribution
    node_counts = defaultdict(int)
    for i in range(1000):
        node = weighted_ch.get_node(f"key_{i}")
        node_counts[node] += 1

    print("\nKey distribution (1000 keys):")
    for node, count in node_counts.items():
        print(f"  {node}: {count} keys ({count/10:.1f}%)")

    # Example 5: Bounded Load
    print("\n5. Bounded Load Consistent Hashing")
    print("-" * 40)

    bounded_ch = ConsistentHashWithLoad(capacity_factor=1.25)

    # Add nodes
    for i in range(3):
        bounded_ch.add_node(f"node{i}")

    # Assign keys
    print("Assigning 30 keys with bounded load (max 1.25x average):")
    for i in range(30):
        node = bounded_ch.assign_key(f"key{i}")

    print("\nLoad distribution:")
    for node, load in bounded_ch.node_load.items():
        print(f"  {node}: {load} keys")

    avg_load = 30 / 3
    max_allowed = avg_load * 1.25
    print(f"\nAverage load: {avg_load:.1f}")
    print(f"Max allowed load: {max_allowed:.1f}")

    # Example 6: Rendezvous Hashing
    print("\n6. Rendezvous Hashing (HRW)")
    print("-" * 40)

    hrw = RendezvousHash()
    for node in ["nodeA", "nodeB", "nodeC"]:
        hrw.add_node(node)

    test_keys = ["key1", "key2", "key3"]
    hrw_mapping = {}

    print("Initial mapping:")
    for key in test_keys:
        node = hrw.get_node(key)
        hrw_mapping[key] = node
        print(f"  {key} -> {node}")

    print("\nAdding nodeD...")
    hrw.add_node("nodeD")

    print("New mapping:")
    for key in test_keys:
        new_node = hrw.get_node(key)
        if new_node != hrw_mapping[key]:
            print(f"  {key}: {hrw_mapping[key]} -> {new_node} (moved)")
        else:
            print(f"  {key}: {new_node} (unchanged)")

    # Example 7: Jump Hash
    print("\n7. Jump Hash")
    print("-" * 40)

    print("Jump hash distribution (5 buckets):")
    bucket_counts = defaultdict(int)
    for i in range(100):
        bucket = JumpHash.hash(i, 5)
        bucket_counts[bucket] += 1

    for bucket in range(5):
        count = bucket_counts[bucket]
        print(f"  Bucket {bucket}: {count} items ({count}%)")

    # Example 8: Visualization
    print("\n8. Ring Visualization")
    print("-" * 40)

    viz_ch = ConsistentHash(virtual_nodes=10)
    for i in range(3):
        viz_ch.add_node(f"srv{i}")

    visualize_ring(viz_ch, ["test1", "test2", "test3"])


if __name__ == "__main__":
    example_usage()