"""
Gossip Protocols Implementation
===============================

Educational implementation of gossip (epidemic) protocols for
distributed systems. These protocols spread information like
epidemics spread in populations.

Includes:
- Push Gossip
- Pull Gossip
- Push-Pull Gossip
- Anti-Entropy Protocol
- Rumor Mongering
- Aggregate Computation (sum, average, min/max)
- Membership Protocol (SWIM-like)
- Failure Detection

Author: Claude
Date: January 2026
"""

import random
import time
import math
from typing import Dict, List, Set, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import hashlib
import json


class GossipStrategy(Enum):
    """Different gossip strategies."""
    PUSH = "push"  # Node with update pushes to others
    PULL = "pull"  # Node pulls updates from others
    PUSH_PULL = "push_pull"  # Combination of push and pull


@dataclass
class GossipMessage:
    """A gossip message containing updates."""
    sender: str
    version: int
    data: Any
    timestamp: float = field(default_factory=time.time)
    hops: int = 0
    message_id: str = field(default_factory=lambda: str(random.random()))


@dataclass
class NodeInfo:
    """Information about a node in the cluster."""
    node_id: str
    heartbeat: int = 0
    last_seen: float = field(default_factory=time.time)
    suspected: bool = False
    confirmed_dead: bool = False
    metadata: Dict = field(default_factory=dict)


class GossipNode:
    """
    A node in a gossip-based distributed system.

    Implements basic gossip protocol with configurable strategies.
    """

    def __init__(
        self,
        node_id: str,
        fanout: int = 3,
        gossip_interval: float = 1.0,
        strategy: GossipStrategy = GossipStrategy.PUSH_PULL,
        max_hops: int = 10
    ):
        """
        Initialize a gossip node.

        Args:
            node_id: Unique identifier for this node
            fanout: Number of nodes to gossip to in each round
            gossip_interval: Time between gossip rounds (seconds)
            strategy: Gossip strategy to use
            max_hops: Maximum hops for a message
        """
        self.node_id = node_id
        self.fanout = fanout
        self.gossip_interval = gossip_interval
        self.strategy = strategy
        self.max_hops = max_hops

        # Node state
        self.version = 0
        self.data: Dict[str, Any] = {}
        self.peers: Set[str] = set()

        # Message tracking
        self.seen_messages: Set[str] = set()
        self.pending_messages: deque = deque(maxlen=1000)

        # Statistics
        self.messages_sent = 0
        self.messages_received = 0
        self.rounds_participated = 0

    def add_peer(self, peer_id: str):
        """Add a peer node."""
        if peer_id != self.node_id:
            self.peers.add(peer_id)

    def remove_peer(self, peer_id: str):
        """Remove a peer node."""
        self.peers.discard(peer_id)

    def update_data(self, key: str, value: Any):
        """
        Update local data and prepare for gossiping.

        Args:
            key: Data key
            value: Data value
        """
        self.data[key] = value
        self.version += 1

        # Create gossip message
        message = GossipMessage(
            sender=self.node_id,
            version=self.version,
            data={key: value}
        )

        self.pending_messages.append(message)

    def select_gossip_targets(self) -> List[str]:
        """
        Select random nodes to gossip with.

        Returns:
            List of node IDs to gossip to
        """
        if not self.peers:
            return []

        # Select min(fanout, num_peers) random peers
        num_targets = min(self.fanout, len(self.peers))
        return random.sample(list(self.peers), num_targets)

    def gossip_round(self) -> List[Tuple[str, GossipMessage]]:
        """
        Perform one round of gossiping.

        Returns:
            List of (target, message) pairs to send
        """
        self.rounds_participated += 1
        targets = self.select_gossip_targets()
        messages_to_send = []

        if self.strategy == GossipStrategy.PUSH:
            # Push: Send updates to selected peers
            for target in targets:
                for message in self.pending_messages:
                    if message.hops < self.max_hops:
                        messages_to_send.append((target, message))
                        self.messages_sent += 1

        elif self.strategy == GossipStrategy.PULL:
            # Pull: Request updates from selected peers
            pull_request = GossipMessage(
                sender=self.node_id,
                version=self.version,
                data={"type": "pull_request"}
            )
            for target in targets:
                messages_to_send.append((target, pull_request))
                self.messages_sent += 1

        elif self.strategy == GossipStrategy.PUSH_PULL:
            # Push-Pull: Exchange updates with selected peers
            for target in targets:
                # Send our updates
                for message in self.pending_messages:
                    if message.hops < self.max_hops:
                        messages_to_send.append((target, message))
                        self.messages_sent += 1

                # Also request their updates
                pull_request = GossipMessage(
                    sender=self.node_id,
                    version=self.version,
                    data={"type": "pull_request", "version": self.version}
                )
                messages_to_send.append((target, pull_request))
                self.messages_sent += 1

        # Clear pending messages after gossip
        self.pending_messages.clear()

        return messages_to_send

    def receive_message(self, message: GossipMessage) -> Optional[GossipMessage]:
        """
        Process a received gossip message.

        Args:
            message: Received message

        Returns:
            Optional response message
        """
        self.messages_received += 1

        # Check if we've seen this message before
        if message.message_id in self.seen_messages:
            return None

        self.seen_messages.add(message.message_id)

        # Handle pull request
        if isinstance(message.data, dict) and message.data.get("type") == "pull_request":
            # Send our data as response
            response = GossipMessage(
                sender=self.node_id,
                version=self.version,
                data=self.data.copy()
            )
            return response

        # Update our data if message has newer information
        if message.version > self.version:
            if isinstance(message.data, dict):
                self.data.update(message.data)
                self.version = message.version

            # Propagate message further (increment hop count)
            if message.hops < self.max_hops:
                propagated = GossipMessage(
                    sender=message.sender,
                    version=message.version,
                    data=message.data,
                    timestamp=message.timestamp,
                    hops=message.hops + 1,
                    message_id=message.message_id
                )
                self.pending_messages.append(propagated)

        return None

    def get_convergence_time(self, total_nodes: int) -> float:
        """
        Estimate convergence time for gossip.

        Args:
            total_nodes: Total number of nodes in the system

        Returns:
            Estimated rounds to convergence
        """
        # O(log N) convergence for epidemic spreading
        return math.log(total_nodes) / math.log(self.fanout + 1)


class AntiEntropyProtocol:
    """
    Anti-entropy protocol for eventual consistency.

    Periodically exchanges complete state to resolve inconsistencies.
    """

    def __init__(self, node_id: str):
        """
        Initialize anti-entropy protocol.

        Args:
            node_id: Node identifier
        """
        self.node_id = node_id
        self.data: Dict[str, Tuple[Any, int]] = {}  # key -> (value, timestamp)
        self.vector_clock: Dict[str, int] = {node_id: 0}

    def update(self, key: str, value: Any):
        """Update a key-value pair."""
        self.vector_clock[self.node_id] += 1
        timestamp = self.vector_clock[self.node_id]
        self.data[key] = (value, timestamp)

    def merge(self, other_data: Dict[str, Tuple[Any, int]],
              other_clock: Dict[str, int]):
        """
        Merge data from another node.

        Args:
            other_data: Data from other node
            other_clock: Vector clock from other node
        """
        # Update vector clock
        for node, timestamp in other_clock.items():
            self.vector_clock[node] = max(
                self.vector_clock.get(node, 0),
                timestamp
            )

        # Merge data (last-write-wins based on timestamp)
        for key, (value, timestamp) in other_data.items():
            if key not in self.data or self.data[key][1] < timestamp:
                self.data[key] = (value, timestamp)

    def get_digest(self) -> Dict[str, int]:
        """
        Get digest of current state for comparison.

        Returns:
            Digest mapping keys to timestamps
        """
        return {key: timestamp for key, (_, timestamp) in self.data.items()}

    def get_missing_updates(self, other_digest: Dict[str, int]) -> Dict[str, Tuple[Any, int]]:
        """
        Get updates that other node is missing.

        Args:
            other_digest: Digest from other node

        Returns:
            Updates to send
        """
        updates = {}
        for key, (value, timestamp) in self.data.items():
            if key not in other_digest or other_digest[key] < timestamp:
                updates[key] = (value, timestamp)
        return updates


class RumorMongering:
    """
    Rumor mongering (or epidemic) protocol.

    Nodes can be in three states: susceptible, infected, or removed.
    """

    class State(Enum):
        """Enumeration of possible node states in rumor mongering protocol."""

        SUSCEPTIBLE = "susceptible"  # Hasn't received update
        INFECTED = "infected"  # Has update, actively spreading
        REMOVED = "removed"  # Has update, stopped spreading

    def __init__(self, node_id: str, removal_probability: float = 0.1):
        """
        Initialize rumor mongering protocol.

        Args:
            node_id: Node identifier
            removal_probability: Probability of stopping rumor spreading
        """
        self.node_id = node_id
        self.removal_probability = removal_probability
        self.state = RumorMongering.State.SUSCEPTIBLE
        self.rumors: Dict[str, Any] = {}
        self.active_rumors: Set[str] = set()

    def receive_rumor(self, rumor_id: str, content: Any) -> bool:
        """
        Receive a rumor.

        Args:
            rumor_id: Unique rumor identifier
            content: Rumor content

        Returns:
            True if rumor was new (node was susceptible)
        """
        if rumor_id in self.rumors:
            # Already know this rumor
            # Sender might want to stop spreading
            return False

        # New rumor - become infected
        self.rumors[rumor_id] = content
        self.active_rumors.add(rumor_id)
        self.state = RumorMongering.State.INFECTED
        return True

    def spread_rumors(self, targets: List[str]) -> List[Tuple[str, str, Any]]:
        """
        Spread active rumors to targets.

        Args:
            targets: List of target node IDs

        Returns:
            List of (target, rumor_id, content) tuples
        """
        messages = []
        rumors_to_remove = []

        for rumor_id in self.active_rumors:
            for target in targets:
                messages.append((target, rumor_id, self.rumors[rumor_id]))

            # Decide whether to stop spreading this rumor
            if random.random() < self.removal_probability:
                rumors_to_remove.append(rumor_id)

        # Remove rumors we're no longer spreading
        for rumor_id in rumors_to_remove:
            self.active_rumors.discard(rumor_id)

        # Update state if no active rumors
        if not self.active_rumors and self.rumors:
            self.state = RumorMongering.State.REMOVED

        return messages


class GossipAggregation:
    """
    Gossip-based aggregation for computing global aggregates.

    Can compute sum, average, min, max, etc. across all nodes.
    """

    def __init__(self, node_id: str, initial_value: float):
        """
        Initialize aggregation protocol.

        Args:
            node_id: Node identifier
            initial_value: This node's initial value
        """
        self.node_id = node_id
        self.sum = initial_value
        self.weight = 1.0
        self.rounds = 0

    def exchange(self, other_sum: float, other_weight: float) -> Tuple[float, float]:
        """
        Exchange with another node (averaging).

        Args:
            other_sum: Other node's sum
            other_weight: Other node's weight

        Returns:
            Values to send to other node
        """
        # Average our values
        total_sum = self.sum + other_sum
        total_weight = self.weight + other_weight

        # Each node gets half
        self.sum = total_sum / 2
        self.weight = total_weight / 2

        self.rounds += 1

        return (self.sum, self.weight)

    def get_estimate(self) -> float:
        """
        Get current estimate of global average.

        Returns:
            Estimated average
        """
        if self.weight == 0:
            return 0
        return self.sum / self.weight

    def get_convergence_rate(self) -> float:
        """
        Get convergence rate based on rounds.

        Returns:
            Exponential convergence rate
        """
        # Error decreases exponentially with rounds
        return math.exp(-self.rounds / 10)


class SWIMProtocol:
    """
    SWIM (Scalable Weakly-consistent Infection-style Membership) Protocol.

    Efficient membership and failure detection protocol.
    """

    def __init__(
        self,
        node_id: str,
        ping_interval: float = 1.0,
        ping_timeout: float = 0.5,
        suspect_timeout: float = 5.0
    ):
        """
        Initialize SWIM protocol.

        Args:
            node_id: Node identifier
            ping_interval: Interval between ping rounds
            ping_timeout: Timeout for ping response
            suspect_timeout: Time before marking suspected node as dead
        """
        self.node_id = node_id
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.suspect_timeout = suspect_timeout

        # Membership list
        self.members: Dict[str, NodeInfo] = {
            node_id: NodeInfo(node_id=node_id)
        }

        # Failure detection state
        self.incarnation = 0
        self.ping_requests: Dict[str, float] = {}
        self.indirect_ping_requests: Dict[str, Set[str]] = {}

    def add_member(self, member_id: str):
        """Add a new member to the cluster."""
        if member_id not in self.members:
            self.members[member_id] = NodeInfo(node_id=member_id)

    def ping(self, target: str) -> bool:
        """
        Ping a target node.

        Args:
            target: Node to ping

        Returns:
            True if ping sent successfully
        """
        if target not in self.members:
            return False

        self.ping_requests[target] = time.time()
        return True

    def receive_ping(self, sender: str) -> bool:
        """
        Process received ping.

        Args:
            sender: Node that sent ping

        Returns:
            True if processed successfully
        """
        # Update sender's info
        if sender in self.members:
            self.members[sender].last_seen = time.time()
            self.members[sender].heartbeat += 1
            self.members[sender].suspected = False
            return True
        return False

    def receive_ack(self, sender: str):
        """Process ping acknowledgment."""
        if sender in self.ping_requests:
            del self.ping_requests[sender]

        if sender in self.members:
            self.members[sender].last_seen = time.time()
            self.members[sender].suspected = False

    def indirect_ping(self, target: str, mediators: List[str]):
        """
        Request indirect ping through mediators.

        Args:
            target: Node to ping indirectly
            mediators: Nodes to use as mediators
        """
        self.indirect_ping_requests[target] = set(mediators)

    def check_timeouts(self):
        """Check for timed out pings and update node states."""
        current_time = time.time()

        # Check direct ping timeouts
        for target, ping_time in list(self.ping_requests.items()):
            if current_time - ping_time > self.ping_timeout:
                # Direct ping failed, mark as suspected
                if target in self.members:
                    self.members[target].suspected = True
                del self.ping_requests[target]

        # Check suspected nodes
        for member in self.members.values():
            if member.suspected:
                if current_time - member.last_seen > self.suspect_timeout:
                    member.confirmed_dead = True

    def get_alive_members(self) -> List[str]:
        """Get list of alive members."""
        return [
            member_id for member_id, info in self.members.items()
            if not info.confirmed_dead
        ]

    def get_suspected_members(self) -> List[str]:
        """Get list of suspected members."""
        return [
            member_id for member_id, info in self.members.items()
            if info.suspected and not info.confirmed_dead
        ]


class GossipSimulator:
    """
    Simulates a gossip protocol network for testing.
    """

    def __init__(self, num_nodes: int, fanout: int = 3):
        """
        Initialize gossip simulator.

        Args:
            num_nodes: Number of nodes in the network
            fanout: Fanout for each node
        """
        self.num_nodes = num_nodes
        self.nodes: Dict[str, GossipNode] = {}

        # Create nodes
        for i in range(num_nodes):
            node_id = f"node_{i}"
            node = GossipNode(node_id, fanout=fanout)

            # Add all other nodes as peers (fully connected)
            for j in range(num_nodes):
                if i != j:
                    node.add_peer(f"node_{j}")

            self.nodes[node_id] = node

    def inject_update(self, node_id: str, key: str, value: Any):
        """Inject an update at a specific node."""
        if node_id in self.nodes:
            self.nodes[node_id].update_data(key, value)

    def simulate_round(self):
        """Simulate one round of gossiping."""
        # Collect all messages to send
        all_messages = []
        for node in self.nodes.values():
            messages = node.gossip_round()
            all_messages.extend(messages)

        # Deliver messages
        for target, message in all_messages:
            if target in self.nodes:
                response = self.nodes[target].receive_message(message)
                if response:
                    # Deliver response back
                    if message.sender in self.nodes:
                        self.nodes[message.sender].receive_message(response)

    def check_convergence(self, key: str) -> bool:
        """Check if all nodes have converged on a value for a key."""
        values = []
        for node in self.nodes.values():
            if key in node.data:
                values.append(node.data[key])

        return len(values) == self.num_nodes and len(set(values)) == 1

    def get_infection_count(self, key: str) -> int:
        """Get number of nodes that have received an update."""
        count = 0
        for node in self.nodes.values():
            if key in node.data:
                count += 1
        return count


def example_usage():
    """Demonstrate gossip protocols."""
    print("=" * 60)
    print("GOSSIP PROTOCOLS DEMONSTRATION")
    print("=" * 60)

    # Example 1: Basic Gossip Spreading
    print("\n1. Basic Gossip Protocol:")
    print("-" * 40)

    simulator = GossipSimulator(num_nodes=10, fanout=3)

    # Inject update at one node
    simulator.inject_update("node_0", "temperature", 25.5)

    # Simulate gossip rounds
    for round_num in range(10):
        simulator.simulate_round()
        infected = simulator.get_infection_count("temperature")
        print(f"Round {round_num + 1}: {infected}/{simulator.num_nodes} nodes have update")

        if simulator.check_convergence("temperature"):
            print(f"Converged in {round_num + 1} rounds!")
            break

    # Example 2: Anti-Entropy Protocol
    print("\n2. Anti-Entropy Protocol:")
    print("-" * 40)

    node1 = AntiEntropyProtocol("node1")
    node2 = AntiEntropyProtocol("node2")

    # Different updates at different nodes
    node1.update("key1", "value1")
    node1.update("key2", "value2")
    node2.update("key2", "value2_modified")
    node2.update("key3", "value3")

    print(f"Node1 data: {node1.data}")
    print(f"Node2 data: {node2.data}")

    # Exchange and merge
    node1.merge(node2.data, node2.vector_clock)
    node2.merge(node1.data, node1.vector_clock)

    print(f"\nAfter merge:")
    print(f"Node1 data: {node1.data}")
    print(f"Node2 data: {node2.data}")

    # Example 3: Rumor Mongering
    print("\n3. Rumor Mongering Protocol:")
    print("-" * 40)

    rumors = [RumorMongering(f"node_{i}") for i in range(5)]

    # Start rumor at node 0
    rumors[0].receive_rumor("rumor1", "Important news!")

    # Simulate spreading
    for round_num in range(5):
        print(f"\nRound {round_num + 1}:")
        for i, node in enumerate(rumors):
            if node.state == RumorMongering.State.INFECTED:
                # Select random targets
                targets = random.sample(range(len(rumors)), 2)
                messages = node.spread_rumors([f"node_{t}" for t in targets])

                # Deliver messages
                for target_id, rumor_id, content in messages:
                    target_idx = int(target_id.split("_")[1])
                    if rumors[target_idx].receive_rumor(rumor_id, content):
                        print(f"  Node {target_idx} infected")

        # Count infected nodes
        infected = sum(1 for r in rumors if "rumor1" in r.rumors)
        print(f"  Total infected: {infected}/5")

    # Example 4: Gossip Aggregation
    print("\n4. Gossip-based Aggregation:")
    print("-" * 40)

    # Create nodes with values
    values = [10, 20, 30, 40, 50]
    aggregators = [GossipAggregation(f"node_{i}", values[i]) for i in range(5)]

    print(f"Initial values: {values}")
    print(f"True average: {sum(values) / len(values)}")

    # Simulate pairwise exchanges
    for round_num in range(10):
        # Random pairwise exchanges
        for _ in range(2):
            i, j = random.sample(range(5), 2)
            sum_i, weight_i = aggregators[i].exchange(
                aggregators[j].sum,
                aggregators[j].weight
            )
            aggregators[j].sum = sum_i
            aggregators[j].weight = weight_i

        # Check estimates
        estimates = [agg.get_estimate() for agg in aggregators]
        avg_estimate = sum(estimates) / len(estimates)
        print(f"Round {round_num + 1}: Average estimate = {avg_estimate:.2f}")

    # Example 5: SWIM Protocol
    print("\n5. SWIM Membership Protocol:")
    print("-" * 40)

    swim = SWIMProtocol("node1")
    swim.add_member("node2")
    swim.add_member("node3")
    swim.add_member("node4")

    # Simulate pings
    swim.ping("node2")
    swim.receive_ack("node2")
    print(f"Alive members: {swim.get_alive_members()}")

    # Simulate failure
    swim.ping("node3")
    time.sleep(0.6)  # Timeout
    swim.check_timeouts()
    print(f"Suspected members: {swim.get_suspected_members()}")

    # Example 6: Properties and Applications
    print("\n6. Gossip Protocol Properties:")
    print("-" * 40)

    properties = {
        "Scalability": "O(log N) convergence time",
        "Fault Tolerance": "Handles node failures gracefully",
        "Eventual Consistency": "All nodes eventually agree",
        "Decentralization": "No single point of failure",
        "Simplicity": "Easy to implement and understand",
        "Probabilistic": "Guarantees with high probability"
    }

    for prop, desc in properties.items():
        print(f"• {prop}: {desc}")

    print("\nApplications:")
    applications = [
        "Database replication (Cassandra, Riak)",
        "Membership management (SWIM, Serf)",
        "Monitoring and alerting systems",
        "Blockchain networks (Bitcoin, Ethereum)",
        "Multicast protocols",
        "Distributed aggregation and statistics"
    ]

    for app in applications:
        print(f"• {app}")

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Gossip protocols spread information exponentially")
    print("- O(log N) rounds for complete dissemination")
    print("- Highly fault-tolerant and scalable")
    print("- Trade-off: redundant messages vs. reliability")
    print("- Perfect for eventual consistency systems")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()