"""
Chord Distributed Hash Table (DHT) Implementation

Chord is a scalable peer-to-peer lookup protocol for distributed systems.
It provides efficient key-value storage and retrieval in O(log N) hops.

Key Features:
- Consistent hashing for load balancing
- Finger tables for efficient routing
- Self-stabilization for handling node failures
- Support for concurrent node joins/leaves

Author: Claude
Date: January 2026
"""

import hashlib
import bisect
import threading
import time
import random
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, Future
import socket
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ChordNode:
    """
    Represents a node in the Chord DHT.

    Attributes:
        node_id: Unique identifier for the node (hash value)
        address: Network address (IP:port) of the node
        predecessor: Reference to predecessor node
        successor: Reference to successor node
        finger_table: Routing table for efficient lookups
        data: Local key-value storage
    """
    node_id: int
    address: str
    predecessor: Optional['ChordNode'] = None
    successor: Optional['ChordNode'] = None
    finger_table: List[Optional['ChordNode']] = field(default_factory=lambda: [None] * 160)
    data: Dict[int, Any] = field(default_factory=dict)
    successor_list: List['ChordNode'] = field(default_factory=list)
    lock: threading.Lock = field(default_factory=threading.Lock)

    def __hash__(self):
        return hash(self.node_id)

    def __eq__(self, other):
        if isinstance(other, ChordNode):
            return self.node_id == other.node_id
        return False


class ChordDHT:
    """
    Chord Distributed Hash Table implementation.

    Provides scalable key-value storage with O(log N) lookup time.
    """

    def __init__(self, m_bits: int = 160, stabilize_interval: float = 1.0):
        """
        Initialize Chord DHT.

        Args:
            m_bits: Number of bits in the hash space (default 160 for SHA-1)
            stabilize_interval: Interval for stabilization in seconds
        """
        self.m_bits = m_bits
        self.max_id = 2 ** m_bits
        self.nodes: Dict[int, ChordNode] = {}
        self.stabilize_interval = stabilize_interval
        self.running = False
        self.stabilizer_thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()

    def hash_key(self, key: str) -> int:
        """Generate hash for a given key."""
        hash_obj = hashlib.sha1(key.encode())
        return int(hash_obj.hexdigest(), 16) % self.max_id

    def hash_address(self, address: str) -> int:
        """Generate hash for a node address."""
        return self.hash_key(address)

    def distance(self, id1: int, id2: int) -> int:
        """Calculate clockwise distance between two IDs in the ring."""
        if id2 >= id1:
            return id2 - id1
        else:
            return self.max_id - id1 + id2

    def in_range(self, key: int, start: int, end: int, inclusive_end: bool = False) -> bool:
        """Check if key is in the range (start, end] on the ring."""
        if start == end:
            return inclusive_end
        elif start < end:
            if inclusive_end:
                return start < key <= end
            else:
                return start < key < end
        else:  # Range wraps around
            if inclusive_end:
                return key > start or key <= end
            else:
                return key > start or key < end

    def create_node(self, address: str) -> ChordNode:
        """Create a new node with the given address."""
        node_id = self.hash_address(address)
        node = ChordNode(node_id, address)

        with self.lock:
            # First node in the network
            if not self.nodes:
                node.predecessor = node
                node.successor = node
                for i in range(self.m_bits):
                    node.finger_table[i] = node

            self.nodes[node_id] = node

        logger.info(f"Created node {node_id} at {address}")
        return node

    def join(self, new_node: ChordNode, known_node: Optional[ChordNode] = None):
        """
        Join a node to the Chord network.

        Args:
            new_node: The node to join
            known_node: An existing node in the network (optional)
        """
        if known_node is None:
            # First node in the network
            new_node.predecessor = new_node
            new_node.successor = new_node
            self._init_finger_table(new_node, new_node)
        else:
            # Join existing network
            self._init_finger_table(new_node, known_node)
            self._update_others(new_node)
            self._transfer_keys(new_node)

        logger.info(f"Node {new_node.node_id} joined the network")

    def _init_finger_table(self, node: ChordNode, known_node: ChordNode):
        """Initialize finger table when joining."""
        # Find successor
        node.finger_table[0] = self._find_successor(known_node, node.node_id)
        node.successor = node.finger_table[0]

        # Set predecessor
        if node.successor:
            node.predecessor = node.successor.predecessor
            node.successor.predecessor = node

        # Initialize rest of finger table
        for i in range(self.m_bits - 1):
            finger_start = (node.node_id + 2 ** (i + 1)) % self.max_id

            # Optimization: check if we can reuse previous finger
            if self.in_range(finger_start, node.node_id,
                           node.finger_table[i].node_id if node.finger_table[i] else node.node_id):
                node.finger_table[i + 1] = node.finger_table[i]
            else:
                node.finger_table[i + 1] = self._find_successor(known_node, finger_start)

    def _find_successor(self, start_node: ChordNode, key: int) -> ChordNode:
        """Find the successor node responsible for a given key."""
        node = self._find_predecessor(start_node, key)
        return node.successor if node.successor else node

    def _find_predecessor(self, start_node: ChordNode, key: int) -> ChordNode:
        """Find the predecessor of the node responsible for a key."""
        current = start_node

        while current.successor and not self.in_range(key, current.node_id,
                                                       current.successor.node_id, True):
            current = self._closest_preceding_finger(current, key)
            if current == start_node:  # Prevent infinite loop
                break

        return current

    def _closest_preceding_finger(self, node: ChordNode, key: int) -> ChordNode:
        """Find the closest finger that precedes the key."""
        for i in range(self.m_bits - 1, -1, -1):
            finger = node.finger_table[i]
            if finger and self.in_range(finger.node_id, node.node_id, key):
                return finger
        return node

    def _update_others(self, node: ChordNode):
        """Update finger tables of other nodes when a new node joins."""
        for i in range(self.m_bits):
            # Find nodes that should have this node in their finger table
            predecessor_id = (node.node_id - 2 ** i + self.max_id) % self.max_id
            predecessor = self._find_predecessor(node, predecessor_id)
            if predecessor:
                self._update_finger_table(predecessor, node, i)

    def _update_finger_table(self, node: ChordNode, new_node: ChordNode, finger_idx: int):
        """Update a specific finger table entry."""
        finger_start = (node.node_id + 2 ** finger_idx) % self.max_id

        if node.finger_table[finger_idx] is None or \
           self.in_range(new_node.node_id, node.node_id, node.finger_table[finger_idx].node_id):
            node.finger_table[finger_idx] = new_node

            # Recursively update predecessor
            if node.predecessor and node.predecessor != node:
                self._update_finger_table(node.predecessor, new_node, finger_idx)

    def _transfer_keys(self, new_node: ChordNode):
        """Transfer keys from successor to new node."""
        if not new_node.successor or new_node.successor == new_node:
            return

        successor = new_node.successor
        keys_to_transfer = []

        with successor.lock:
            for key in list(successor.data.keys()):
                if self.in_range(key, new_node.predecessor.node_id if new_node.predecessor else 0,
                               new_node.node_id, True):
                    keys_to_transfer.append((key, successor.data[key]))
                    del successor.data[key]

        with new_node.lock:
            for key, value in keys_to_transfer:
                new_node.data[key] = value

        logger.info(f"Transferred {len(keys_to_transfer)} keys to node {new_node.node_id}")

    def leave(self, node: ChordNode):
        """Remove a node from the Chord network."""
        with self.lock:
            if node.node_id not in self.nodes:
                return

            # Transfer data to successor
            if node.successor and node.successor != node:
                with node.successor.lock:
                    node.successor.data.update(node.data)

            # Update predecessor and successor pointers
            if node.predecessor and node.predecessor != node:
                node.predecessor.successor = node.successor
            if node.successor and node.successor != node:
                node.successor.predecessor = node.predecessor

            # Remove from nodes dict
            del self.nodes[node.node_id]

        logger.info(f"Node {node.node_id} left the network")

    def lookup(self, key: str, start_node: Optional[ChordNode] = None) -> Tuple[Optional[Any], int]:
        """
        Look up a value in the DHT.

        Args:
            key: The key to look up
            start_node: Node to start the search from

        Returns:
            Tuple of (value, hop_count)
        """
        if not self.nodes:
            return None, 0

        if start_node is None:
            start_node = random.choice(list(self.nodes.values()))

        key_hash = self.hash_key(key)
        hop_count = 0
        current = start_node

        # Find responsible node
        while current:
            hop_count += 1

            # Check if current node is responsible
            if current.predecessor and self.in_range(key_hash,
                                                     current.predecessor.node_id,
                                                     current.node_id, True):
                with current.lock:
                    return current.data.get(key_hash), hop_count

            # Route to next node
            next_node = self._closest_preceding_finger(current, key_hash)
            if next_node == current:
                # We've reached the responsible node
                with current.lock:
                    return current.data.get(key_hash), hop_count

            current = next_node

            if hop_count > self.m_bits * 2:  # Prevent infinite loops
                break

        return None, hop_count

    def store(self, key: str, value: Any, start_node: Optional[ChordNode] = None) -> bool:
        """
        Store a key-value pair in the DHT.

        Args:
            key: The key to store
            value: The value to store
            start_node: Node to start from

        Returns:
            Success status
        """
        if not self.nodes:
            return False

        if start_node is None:
            start_node = random.choice(list(self.nodes.values()))

        key_hash = self.hash_key(key)

        # Find responsible node
        responsible_node = self._find_successor(start_node, key_hash)

        if responsible_node:
            with responsible_node.lock:
                responsible_node.data[key_hash] = value
            logger.info(f"Stored key {key} (hash: {key_hash}) at node {responsible_node.node_id}")
            return True

        return False

    def delete(self, key: str, start_node: Optional[ChordNode] = None) -> bool:
        """Delete a key from the DHT."""
        if not self.nodes:
            return False

        if start_node is None:
            start_node = random.choice(list(self.nodes.values()))

        key_hash = self.hash_key(key)

        # Find responsible node
        responsible_node = self._find_successor(start_node, key_hash)

        if responsible_node:
            with responsible_node.lock:
                if key_hash in responsible_node.data:
                    del responsible_node.data[key_hash]
                    logger.info(f"Deleted key {key} from node {responsible_node.node_id}")
                    return True

        return False

    def stabilize(self):
        """Periodically verify and fix node pointers."""
        for node in list(self.nodes.values()):
            self._stabilize_node(node)
            self._fix_fingers(node)

    def _stabilize_node(self, node: ChordNode):
        """Stabilize a single node."""
        if not node.successor:
            return

        # Check if there's a node between us and our successor
        x = node.successor.predecessor
        if x and x != node and self.in_range(x.node_id, node.node_id, node.successor.node_id):
            node.successor = x

        # Notify successor
        if node.successor and node.successor != node:
            self._notify(node.successor, node)

    def _notify(self, node: ChordNode, potential_predecessor: ChordNode):
        """Notify a node about a potential predecessor."""
        if node.predecessor is None or \
           self.in_range(potential_predecessor.node_id, node.predecessor.node_id, node.node_id):
            node.predecessor = potential_predecessor

    def _fix_fingers(self, node: ChordNode):
        """Periodically refresh finger table entries."""
        # Fix a random finger
        i = random.randint(0, self.m_bits - 1)
        finger_start = (node.node_id + 2 ** i) % self.max_id
        node.finger_table[i] = self._find_successor(node, finger_start)

    def start_stabilization(self):
        """Start the stabilization thread."""
        if self.running:
            return

        self.running = True
        self.stabilizer_thread = threading.Thread(target=self._stabilization_loop)
        self.stabilizer_thread.start()

    def stop_stabilization(self):
        """Stop the stabilization thread."""
        self.running = False
        if self.stabilizer_thread:
            self.stabilizer_thread.join()

    def _stabilization_loop(self):
        """Main stabilization loop."""
        while self.running:
            try:
                self.stabilize()
                time.sleep(self.stabilize_interval)
            except Exception as e:
                logger.error(f"Stabilization error: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the DHT."""
        if not self.nodes:
            return {"nodes": 0, "keys": 0}

        total_keys = sum(len(node.data) for node in self.nodes.values())
        avg_keys = total_keys / len(self.nodes) if self.nodes else 0

        # Calculate load distribution
        key_counts = [len(node.data) for node in self.nodes.values()]
        min_keys = min(key_counts) if key_counts else 0
        max_keys = max(key_counts) if key_counts else 0

        return {
            "nodes": len(self.nodes),
            "total_keys": total_keys,
            "avg_keys_per_node": avg_keys,
            "min_keys": min_keys,
            "max_keys": max_keys,
            "load_balance": min_keys / max_keys if max_keys > 0 else 1.0
        }


class ChordSimulator:
    """
    Simulator for testing Chord DHT behavior.
    """

    def __init__(self, num_nodes: int = 10, m_bits: int = 10):
        """
        Initialize simulator.

        Args:
            num_nodes: Number of nodes to simulate
            m_bits: Bit space size (smaller for simulation)
        """
        self.dht = ChordDHT(m_bits=m_bits)
        self.num_nodes = num_nodes
        self.nodes: List[ChordNode] = []

    def setup_network(self):
        """Set up the initial Chord network."""
        # Create first node
        first_node = self.dht.create_node(f"node_0")
        self.dht.join(first_node)
        self.nodes.append(first_node)

        # Add remaining nodes
        for i in range(1, self.num_nodes):
            node = self.dht.create_node(f"node_{i}")
            self.dht.join(node, first_node)
            self.nodes.append(node)
            time.sleep(0.01)  # Small delay for stabilization

        # Run stabilization
        for _ in range(5):
            self.dht.stabilize()

        print(f"Created network with {self.num_nodes} nodes")

    def test_operations(self, num_operations: int = 100):
        """Test store and lookup operations."""
        if not self.nodes:
            print("No nodes in network")
            return

        success_count = 0
        hop_counts = []

        # Store values
        print(f"\nStoring {num_operations} key-value pairs...")
        for i in range(num_operations):
            key = f"key_{i}"
            value = f"value_{i}"
            if self.dht.store(key, value):
                success_count += 1

        print(f"Successfully stored {success_count}/{num_operations} items")

        # Lookup values
        print(f"\nLooking up {num_operations} keys...")
        found_count = 0
        for i in range(num_operations):
            key = f"key_{i}"
            value, hops = self.dht.lookup(key)
            if value == f"value_{i}":
                found_count += 1
                hop_counts.append(hops)

        print(f"Successfully found {found_count}/{num_operations} items")
        if hop_counts:
            avg_hops = sum(hop_counts) / len(hop_counts)
            print(f"Average lookup hops: {avg_hops:.2f}")
            print(f"Max hops: {max(hop_counts)}, Min hops: {min(hop_counts)}")

        # Show stats
        stats = self.dht.get_stats()
        print(f"\nDHT Statistics:")
        print(f"  Total nodes: {stats['nodes']}")
        print(f"  Total keys: {stats['total_keys']}")
        print(f"  Avg keys per node: {stats['avg_keys_per_node']:.2f}")
        print(f"  Load balance: {stats['load_balance']:.2%}")

    def test_churn(self, num_iterations: int = 5):
        """Test network behavior under churn (nodes joining/leaving)."""
        print(f"\nTesting churn with {num_iterations} iterations...")

        for iteration in range(num_iterations):
            print(f"\nIteration {iteration + 1}:")

            # Remove a random node
            if len(self.nodes) > 1:
                node_to_remove = random.choice(self.nodes[1:])  # Don't remove first node
                self.dht.leave(node_to_remove)
                self.nodes.remove(node_to_remove)
                print(f"  Removed node {node_to_remove.node_id}")

            # Add a new node
            new_node = self.dht.create_node(f"node_new_{iteration}")
            self.dht.join(new_node, self.nodes[0])
            self.nodes.append(new_node)
            print(f"  Added node {new_node.node_id}")

            # Stabilize
            for _ in range(3):
                self.dht.stabilize()

            # Test some lookups
            success = 0
            for i in range(10):
                key = f"key_{i}"
                value, _ = self.dht.lookup(key)
                if value == f"value_{i}":
                    success += 1

            print(f"  Lookup success rate: {success}/10")

    def visualize_ring(self):
        """Simple visualization of the Chord ring."""
        if not self.nodes:
            print("No nodes to visualize")
            return

        print("\nChord Ring Structure:")
        print("=" * 50)

        sorted_nodes = sorted(self.nodes, key=lambda n: n.node_id)

        for node in sorted_nodes:
            pred_id = node.predecessor.node_id if node.predecessor else "None"
            succ_id = node.successor.node_id if node.successor else "None"
            print(f"Node {node.node_id:5d}: pred={pred_id:5s}, succ={succ_id:5s}, "
                  f"keys={len(node.data)}")

        print("=" * 50)


# Example usage functions
def example_basic_operations():
    """Demonstrate basic Chord DHT operations."""
    print("=== Basic Chord DHT Operations ===\n")

    # Create DHT with small bit space for demonstration
    dht = ChordDHT(m_bits=8)

    # Create and join nodes
    node1 = dht.create_node("192.168.1.1:5000")
    dht.join(node1)

    node2 = dht.create_node("192.168.1.2:5000")
    dht.join(node2, node1)

    node3 = dht.create_node("192.168.1.3:5000")
    dht.join(node3, node1)

    # Stabilize the network
    for _ in range(3):
        dht.stabilize()

    # Store some data
    print("Storing data...")
    dht.store("user:alice", {"email": "alice@example.com", "age": 30})
    dht.store("user:bob", {"email": "bob@example.com", "age": 25})
    dht.store("config:database", {"host": "localhost", "port": 5432})

    # Retrieve data
    print("\nRetrieving data...")
    alice_data, hops = dht.lookup("user:alice")
    print(f"user:alice -> {alice_data} (found in {hops} hops)")

    config_data, hops = dht.lookup("config:database")
    print(f"config:database -> {config_data} (found in {hops} hops)")

    # Show statistics
    stats = dht.get_stats()
    print(f"\nNetwork stats: {stats}")


def example_large_scale_simulation():
    """Simulate a larger Chord network."""
    print("=== Large Scale Chord Simulation ===\n")

    # Create simulator with more nodes
    simulator = ChordSimulator(num_nodes=20, m_bits=10)

    # Set up network
    simulator.setup_network()

    # Visualize initial ring
    simulator.visualize_ring()

    # Test operations
    simulator.test_operations(num_operations=200)

    # Test under churn
    simulator.test_churn(num_iterations=3)

    # Final visualization
    simulator.visualize_ring()


def example_fault_tolerance():
    """Demonstrate fault tolerance in Chord."""
    print("=== Chord Fault Tolerance ===\n")

    dht = ChordDHT(m_bits=8)
    nodes = []

    # Create network with 10 nodes
    print("Creating 10-node network...")
    for i in range(10):
        node = dht.create_node(f"node_{i}")
        if i == 0:
            dht.join(node)
        else:
            dht.join(node, nodes[0])
        nodes.append(node)

    # Stabilize
    for _ in range(5):
        dht.stabilize()

    # Store data across the network
    print("\nStoring 50 key-value pairs...")
    for i in range(50):
        dht.store(f"data_{i}", f"value_{i}")

    initial_stats = dht.get_stats()
    print(f"Initial stats: {initial_stats}")

    # Simulate node failures
    print("\nSimulating 3 node failures...")
    failed_nodes = random.sample(nodes[1:], 3)  # Don't fail the first node
    for node in failed_nodes:
        print(f"  Node {node.node_id} failed")
        dht.leave(node)
        nodes.remove(node)

    # Stabilize after failures
    for _ in range(5):
        dht.stabilize()

    # Check data availability
    print("\nChecking data availability after failures...")
    available_count = 0
    for i in range(50):
        value, _ = dht.lookup(f"data_{i}")
        if value == f"value_{i}":
            available_count += 1

    print(f"Data availability: {available_count}/50 ({available_count*2}%)")

    final_stats = dht.get_stats()
    print(f"Final stats: {final_stats}")


if __name__ == "__main__":
    # Run examples
    example_basic_operations()
    print("\n" + "=" * 60 + "\n")

    example_large_scale_simulation()
    print("\n" + "=" * 60 + "\n")

    example_fault_tolerance()

    print("\n" + "=" * 60)
    print("Key Insights:")
    print("=" * 60)
    print("""
1. Chord provides O(log N) lookup performance in large networks
2. The protocol is self-stabilizing and handles node failures gracefully
3. Consistent hashing ensures good load balancing
4. Finger tables provide efficient routing without full routing tables
5. The system can handle high churn rates with periodic stabilization
6. Data availability is maintained through replication (not shown here)
7. Chord is foundational for many P2P systems (BitTorrent DHT, etc.)
    """)