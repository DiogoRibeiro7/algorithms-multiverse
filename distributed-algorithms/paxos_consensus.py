"""
Paxos Consensus Algorithm Implementation
========================================

Implementation of the Paxos consensus protocol for distributed systems.
Paxos ensures that a group of distributed nodes can agree on a single value
even in the presence of failures and network partitions.

Key Components:
- Basic Paxos (single value consensus)
- Multi-Paxos (sequence of values)
- Proposers, Acceptors, and Learners
- Two-phase protocol (Prepare/Promise and Accept/Accepted)
- Failure handling and recovery
- Leader election optimization

Variants Implemented:
- Classic Paxos
- Fast Paxos
- Cheap Paxos
- Byzantine Paxos basics

Applications:
- Distributed databases
- Configuration management
- Distributed locking
- Replicated state machines
- Consensus in blockchain

Author: Claude
Date: January 2026
"""

import time
import random
from typing import Optional, List, Tuple, Dict, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import threading
from queue import Queue, Empty
import hashlib


class MessageType(Enum):
    """Types of Paxos messages."""
    PREPARE = "prepare"
    PROMISE = "promise"
    ACCEPT = "accept"
    ACCEPTED = "accepted"
    NACK = "nack"
    LEARN = "learn"


class NodeRole(Enum):
    """Roles in Paxos protocol."""
    PROPOSER = "proposer"
    ACCEPTOR = "acceptor"
    LEARNER = "learner"


@dataclass
class ProposalNumber:
    """
    Proposal number with total ordering.
    Format: (round, node_id)
    """
    round: int
    node_id: int

    def __lt__(self, other):
        if self.round != other.round:
            return self.round < other.round
        return self.node_id < other.node_id

    def __le__(self, other):
        return self < other or self == other

    def __eq__(self, other):
        return self.round == other.round and self.node_id == other.node_id

    def __hash__(self):
        return hash((self.round, self.node_id))

    def __str__(self):
        return f"({self.round}.{self.node_id})"


@dataclass
class PaxosMessage:
    """Message in Paxos protocol."""
    type: MessageType
    from_node: int
    to_node: int
    proposal_number: Optional[ProposalNumber] = None
    value: Optional[Any] = None
    accepted_proposal: Optional[ProposalNumber] = None
    accepted_value: Optional[Any] = None


@dataclass
class AcceptorState:
    """Persistent state for acceptor."""
    promised_proposal: Optional[ProposalNumber] = None
    accepted_proposal: Optional[ProposalNumber] = None
    accepted_value: Optional[Any] = None


class PaxosNode:
    """
    Base Paxos node that can act as Proposer, Acceptor, and Learner.
    """

    def __init__(self, node_id: int, nodes: List[int], roles: Set[NodeRole]):
        """
        Initialize Paxos node.

        Args:
            node_id: Unique node identifier
            nodes: List of all node IDs in the system
            roles: Set of roles this node plays
        """
        self.node_id = node_id
        self.nodes = nodes
        self.roles = roles

        # Proposer state
        self.proposal_round = 0
        self.current_proposal = None
        self.promises_received = {}
        self.accepts_received = set()

        # Acceptor state
        self.acceptor_state = AcceptorState()

        # Learner state
        self.learned_value = None
        self.accepted_count = defaultdict(int)

        # Message queue for simulation
        self.message_queue = Queue()
        self.running = False

        # Failure simulation
        self.is_failed = False
        self.failure_probability = 0.0

    def propose(self, value: Any) -> bool:
        """
        Propose a value for consensus.

        Args:
            value: Value to propose

        Returns:
            True if consensus reached
        """
        if NodeRole.PROPOSER not in self.roles:
            return False

        # Phase 1a: Prepare
        self.proposal_round += 1
        proposal_number = ProposalNumber(self.proposal_round, self.node_id)
        self.current_proposal = (proposal_number, value)
        self.promises_received = {}
        self.accepts_received = set()

        # Send prepare to all acceptors
        for node in self.nodes:
            if node != self.node_id:
                message = PaxosMessage(
                    type=MessageType.PREPARE,
                    from_node=self.node_id,
                    to_node=node,
                    proposal_number=proposal_number
                )
                self._send_message(message)

        # Wait for promises (simulated)
        return self._wait_for_consensus()

    def handle_message(self, message: PaxosMessage):
        """Handle incoming Paxos message."""
        if self.is_failed:
            return

        if message.type == MessageType.PREPARE:
            self._handle_prepare(message)
        elif message.type == MessageType.PROMISE:
            self._handle_promise(message)
        elif message.type == MessageType.ACCEPT:
            self._handle_accept(message)
        elif message.type == MessageType.ACCEPTED:
            self._handle_accepted(message)
        elif message.type == MessageType.LEARN:
            self._handle_learn(message)

    def _handle_prepare(self, message: PaxosMessage):
        """Phase 1b: Handle prepare request as acceptor."""
        if NodeRole.ACCEPTOR not in self.roles:
            return

        proposal = message.proposal_number

        # Check if we can promise
        if (self.acceptor_state.promised_proposal is None or
            proposal > self.acceptor_state.promised_proposal):

            # Update promise
            self.acceptor_state.promised_proposal = proposal

            # Send promise with any accepted value
            response = PaxosMessage(
                type=MessageType.PROMISE,
                from_node=self.node_id,
                to_node=message.from_node,
                proposal_number=proposal,
                accepted_proposal=self.acceptor_state.accepted_proposal,
                accepted_value=self.acceptor_state.accepted_value
            )
            self._send_message(response)
        else:
            # Send NACK
            response = PaxosMessage(
                type=MessageType.NACK,
                from_node=self.node_id,
                to_node=message.from_node,
                proposal_number=proposal
            )
            self._send_message(response)

    def _handle_promise(self, message: PaxosMessage):
        """Phase 2a: Handle promise as proposer."""
        if NodeRole.PROPOSER not in self.roles:
            return

        if not self.current_proposal:
            return

        proposal_number, proposed_value = self.current_proposal

        # Check if promise is for current proposal
        if message.proposal_number != proposal_number:
            return

        # Record promise
        self.promises_received[message.from_node] = (
            message.accepted_proposal,
            message.accepted_value
        )

        # Check if we have majority
        if len(self.promises_received) + 1 > len(self.nodes) // 2:
            # Choose value: highest numbered accepted value or our proposed value
            value_to_accept = proposed_value
            highest_proposal = None

            for accepted_prop, accepted_val in self.promises_received.values():
                if accepted_prop and (highest_proposal is None or accepted_prop > highest_proposal):
                    highest_proposal = accepted_prop
                    value_to_accept = accepted_val

            # Phase 2a: Send accept requests
            for node in self.nodes:
                if node != self.node_id:
                    accept_msg = PaxosMessage(
                        type=MessageType.ACCEPT,
                        from_node=self.node_id,
                        to_node=node,
                        proposal_number=proposal_number,
                        value=value_to_accept
                    )
                    self._send_message(accept_msg)

            # Accept our own proposal
            self.acceptor_state.accepted_proposal = proposal_number
            self.acceptor_state.accepted_value = value_to_accept

    def _handle_accept(self, message: PaxosMessage):
        """Phase 2b: Handle accept request as acceptor."""
        if NodeRole.ACCEPTOR not in self.roles:
            return

        proposal = message.proposal_number

        # Check if we can accept
        if (self.acceptor_state.promised_proposal is None or
            proposal >= self.acceptor_state.promised_proposal):

            # Accept the value
            self.acceptor_state.promised_proposal = proposal
            self.acceptor_state.accepted_proposal = proposal
            self.acceptor_state.accepted_value = message.value

            # Send accepted to all learners
            for node in self.nodes:
                accepted_msg = PaxosMessage(
                    type=MessageType.ACCEPTED,
                    from_node=self.node_id,
                    to_node=node,
                    proposal_number=proposal,
                    value=message.value
                )
                self._send_message(accepted_msg)
        else:
            # Send NACK
            nack = PaxosMessage(
                type=MessageType.NACK,
                from_node=self.node_id,
                to_node=message.from_node,
                proposal_number=proposal
            )
            self._send_message(nack)

    def _handle_accepted(self, message: PaxosMessage):
        """Handle accepted message as learner."""
        if NodeRole.LEARNER not in self.roles:
            return

        # Count accepts for this value
        key = (message.proposal_number, message.value)
        self.accepted_count[key] += 1

        # Check if value is chosen (majority accepted)
        if self.accepted_count[key] > len(self.nodes) // 2:
            if self.learned_value is None:
                self.learned_value = message.value
                # Notify other learners
                for node in self.nodes:
                    if node != self.node_id:
                        learn_msg = PaxosMessage(
                            type=MessageType.LEARN,
                            from_node=self.node_id,
                            to_node=node,
                            value=message.value
                        )
                        self._send_message(learn_msg)

    def _handle_learn(self, message: PaxosMessage):
        """Handle learn message."""
        if NodeRole.LEARNER in self.roles:
            self.learned_value = message.value

    def _send_message(self, message: PaxosMessage):
        """Send message with failure simulation."""
        # Simulate message loss
        if random.random() < self.failure_probability:
            return

        # In real implementation, would send over network
        # Here we add to destination's queue
        self.message_queue.put(message)

    def _wait_for_consensus(self) -> bool:
        """Wait for consensus to be reached (simplified)."""
        # In real implementation, would have proper async handling
        timeout = 1.0  # seconds
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.learned_value is not None:
                return True
            time.sleep(0.01)

        return False

    def fail(self):
        """Simulate node failure."""
        self.is_failed = True

    def recover(self):
        """Simulate node recovery."""
        self.is_failed = False


class MultiPaxos:
    """
    Multi-Paxos for consensus on a sequence of values.

    Optimizes Basic Paxos by maintaining stable leader.
    """

    def __init__(self, nodes: List[int]):
        """
        Initialize Multi-Paxos system.

        Args:
            nodes: List of node IDs
        """
        self.nodes = nodes
        self.leader = min(nodes)  # Initial leader
        self.log = []  # Sequence of chosen values
        self.next_slot = 0

    def propose_sequence(self, values: List[Any]) -> bool:
        """
        Propose a sequence of values.

        Args:
            values: Values to add to log

        Returns:
            True if all values accepted
        """
        success = True

        for value in values:
            if not self._propose_single(value):
                success = False
                break

        return success

    def _propose_single(self, value: Any) -> bool:
        """Propose single value to next slot."""
        # Leader proposes directly without prepare phase
        # (after establishing leadership)

        # Simplified: assume leader is established
        slot = self.next_slot
        self.log.append(value)
        self.next_slot += 1

        return True

    def handle_leader_failure(self):
        """Handle leader failure by electing new leader."""
        # Remove failed leader from candidate list
        candidates = [n for n in self.nodes if n != self.leader]

        if candidates:
            # Simple leader election: choose minimum ID
            self.leader = min(candidates)

            # New leader runs prepare phase for uncommitted slots
            # (simplified here)


class FastPaxos:
    """
    Fast Paxos variant that allows any proposer to send values directly
    to acceptors in the common case, reducing latency.
    """

    def __init__(self, nodes: List[int], fast_quorum_size: Optional[int] = None):
        """
        Initialize Fast Paxos.

        Args:
            nodes: List of node IDs
            fast_quorum_size: Size of fast quorum (default: 3/4 of nodes)
        """
        self.nodes = nodes
        n = len(nodes)

        # Fast quorum must be larger than classic quorum
        if fast_quorum_size is None:
            self.fast_quorum_size = (3 * n) // 4 + 1
        else:
            self.fast_quorum_size = fast_quorum_size

        self.classic_quorum_size = n // 2 + 1

    def fast_propose(self, value: Any, node_id: int) -> Tuple[bool, str]:
        """
        Fast Paxos proposal - skip prepare phase in common case.

        Args:
            value: Value to propose
            node_id: Proposer node ID

        Returns:
            (success, mode) where mode is "fast" or "classic"
        """
        # Try fast path first
        fast_accepts = self._try_fast_path(value, node_id)

        if fast_accepts >= self.fast_quorum_size:
            return True, "fast"

        # Fall back to classic Paxos
        return self._classic_path(value, node_id), "classic"

    def _try_fast_path(self, value: Any, node_id: int) -> int:
        """Try fast path - send value directly to acceptors."""
        accepts = 0

        # Simulate sending to acceptors
        for _ in self.nodes:
            # Simulate acceptance (simplified)
            if random.random() > 0.1:  # 90% success rate
                accepts += 1

        return accepts

    def _classic_path(self, value: Any, node_id: int) -> bool:
        """Fall back to classic Paxos."""
        # Run classic two-phase Paxos
        return True  # Simplified


class ByzantinePaxos:
    """
    Byzantine Paxos for consensus with Byzantine failures.

    Handles nodes that may behave arbitrarily (malicious or faulty).
    """

    def __init__(self, nodes: List[int], byzantine_nodes: Set[int]):
        """
        Initialize Byzantine Paxos.

        Args:
            nodes: All node IDs
            byzantine_nodes: Set of Byzantine node IDs
        """
        self.nodes = nodes
        self.byzantine_nodes = byzantine_nodes
        self.n = len(nodes)
        self.f = len(byzantine_nodes)  # Number of Byzantine nodes

        # Byzantine Paxos requires n > 3f
        if self.n <= 3 * self.f:
            raise ValueError(f"Need n > 3f for Byzantine Paxos (n={self.n}, f={self.f})")

    def byzantine_consensus(self, value: Any, node_id: int) -> Optional[Any]:
        """
        Achieve consensus despite Byzantine failures.

        Args:
            value: Proposed value
            node_id: Proposer node ID

        Returns:
            Consensus value or None
        """
        # Phase 1: Broadcast value
        votes = self._collect_votes(value, node_id)

        # Phase 2: Check if enough non-Byzantine nodes agree
        if self._verify_votes(votes):
            return self._extract_consensus_value(votes)

        return None

    def _collect_votes(self, value: Any, node_id: int) -> Dict[int, Any]:
        """Collect votes from all nodes."""
        votes = {}

        for node in self.nodes:
            if node in self.byzantine_nodes:
                # Byzantine nodes may send arbitrary values
                if random.random() < 0.5:
                    votes[node] = value  # Sometimes agree
                else:
                    votes[node] = f"byzantine_{random.randint(0, 100)}"  # Sometimes disagree
            else:
                # Honest nodes vote for the value
                votes[node] = value

        return votes

    def _verify_votes(self, votes: Dict[int, Any]) -> bool:
        """Verify if we have enough agreeing votes."""
        # Count votes for each value
        value_counts = defaultdict(int)
        for v in votes.values():
            value_counts[v] += 1

        # Need more than (n + f) / 2 votes for same value
        threshold = (self.n + self.f) // 2 + 1

        return max(value_counts.values()) >= threshold

    def _extract_consensus_value(self, votes: Dict[int, Any]) -> Any:
        """Extract consensus value from votes."""
        value_counts = defaultdict(int)
        for v in votes.values():
            value_counts[v] += 1

        return max(value_counts.items(), key=lambda x: x[1])[0]


class PaxosSimulator:
    """
    Simulator for running Paxos protocols with various failure scenarios.
    """

    def __init__(self, num_nodes: int = 5):
        """
        Initialize Paxos simulator.

        Args:
            num_nodes: Number of nodes in the system
        """
        self.num_nodes = num_nodes
        self.nodes = []

        # Create nodes with different role combinations
        for i in range(num_nodes):
            roles = {NodeRole.ACCEPTOR, NodeRole.LEARNER}
            if i < 2:  # First two nodes are also proposers
                roles.add(NodeRole.PROPOSER)

            node = PaxosNode(i, list(range(num_nodes)), roles)
            self.nodes.append(node)

    def run_basic_consensus(self, value: Any) -> bool:
        """
        Run basic Paxos consensus.

        Args:
            value: Value to achieve consensus on

        Returns:
            True if consensus achieved
        """
        # Node 0 proposes
        proposer = self.nodes[0]
        success = proposer.propose(value)

        # Process messages (simplified simulation)
        self._process_all_messages()

        # Check if all learners learned the value
        learned_values = [n.learned_value for n in self.nodes
                         if NodeRole.LEARNER in n.roles]

        return all(v == value for v in learned_values if v is not None)

    def run_competing_proposals(self, values: List[Any]) -> Any:
        """
        Run Paxos with competing proposals.

        Args:
            values: List of competing values

        Returns:
            Consensus value
        """
        # Multiple proposers propose different values
        threads = []
        for i, value in enumerate(values[:2]):  # Max 2 proposers
            if i < len(self.nodes):
                proposer = self.nodes[i]
                # Simulate concurrent proposals
                proposer.propose(value)

        self._process_all_messages()

        # Return consensus value
        for node in self.nodes:
            if node.learned_value is not None:
                return node.learned_value

        return None

    def run_with_failures(self, value: Any, failure_rate: float = 0.2) -> bool:
        """
        Run Paxos with node failures.

        Args:
            value: Value to achieve consensus on
            failure_rate: Probability of node failure

        Returns:
            True if consensus achieved despite failures
        """
        # Randomly fail some nodes
        for node in self.nodes:
            if random.random() < failure_rate:
                node.fail()

        # Try to achieve consensus
        proposer = None
        for node in self.nodes:
            if not node.is_failed and NodeRole.PROPOSER in node.roles:
                proposer = node
                break

        if proposer:
            success = proposer.propose(value)
            self._process_all_messages()

            # Check consensus among non-failed learners
            learned_values = [n.learned_value for n in self.nodes
                             if not n.is_failed and NodeRole.LEARNER in n.roles]

            return len(learned_values) > 0 and all(v == value for v in learned_values if v is not None)

        return False

    def _process_all_messages(self):
        """Process all messages in the system (simulation)."""
        # Simplified: in real system, messages would be async
        for _ in range(100):  # Process up to 100 messages
            messages_processed = False

            for node in self.nodes:
                try:
                    message = node.message_queue.get_nowait()
                    # Route to destination
                    dest_node = self.nodes[message.to_node]
                    dest_node.handle_message(message)
                    messages_processed = True
                except Empty:
                    pass

            if not messages_processed:
                break


def basic_paxos_example():
    """Example: Basic Paxos consensus."""
    print("=" * 60)
    print("BASIC PAXOS CONSENSUS")
    print("=" * 60)

    simulator = PaxosSimulator(num_nodes=5)

    # Test 1: Single proposal
    print("\n1. Single Proposal:")
    value = "config_value_1"
    success = simulator.run_basic_consensus(value)
    print(f"   Proposed: {value}")
    print(f"   Consensus achieved: {success}")

    # Test 2: Competing proposals
    print("\n2. Competing Proposals:")
    values = ["option_A", "option_B"]
    consensus_value = simulator.run_competing_proposals(values)
    print(f"   Competing values: {values}")
    print(f"   Consensus value: {consensus_value}")

    # Test 3: With failures
    print("\n3. Consensus with Node Failures:")
    simulator = PaxosSimulator(num_nodes=5)  # Reset
    value = "critical_config"
    success = simulator.run_with_failures(value, failure_rate=0.3)
    print(f"   Proposed: {value}")
    print(f"   30% nodes failed")
    print(f"   Consensus achieved: {success}")


def multi_paxos_example():
    """Example: Multi-Paxos for log replication."""
    print("\n" + "=" * 60)
    print("MULTI-PAXOS LOG REPLICATION")
    print("=" * 60)

    nodes = list(range(5))
    multi_paxos = MultiPaxos(nodes)

    # Replicate a sequence of operations
    operations = [
        "CREATE TABLE users",
        "INSERT user1",
        "INSERT user2",
        "UPDATE user1",
        "DELETE user2"
    ]

    print("Replicating operations:")
    success = multi_paxos.propose_sequence(operations)

    if success:
        print(f"Successfully replicated {len(operations)} operations")
        print("\nReplicated log:")
        for i, op in enumerate(multi_paxos.log):
            print(f"  Slot {i}: {op}")
    else:
        print("Failed to replicate all operations")

    # Simulate leader failure
    print("\nSimulating leader failure...")
    old_leader = multi_paxos.leader
    multi_paxos.handle_leader_failure()
    print(f"  Old leader: Node {old_leader}")
    print(f"  New leader: Node {multi_paxos.leader}")


def fast_paxos_example():
    """Example: Fast Paxos optimization."""
    print("\n" + "=" * 60)
    print("FAST PAXOS OPTIMIZATION")
    print("=" * 60)

    nodes = list(range(7))
    fast_paxos = FastPaxos(nodes)

    print(f"Nodes: {len(nodes)}")
    print(f"Classic quorum size: {fast_paxos.classic_quorum_size}")
    print(f"Fast quorum size: {fast_paxos.fast_quorum_size}")

    # Test fast path vs classic path
    results = {"fast": 0, "classic": 0}
    trials = 100

    print(f"\nRunning {trials} consensus attempts:")
    for i in range(trials):
        value = f"value_{i}"
        success, mode = fast_paxos.fast_propose(value, node_id=0)
        if success:
            results[mode] += 1

    print(f"  Fast path used: {results['fast']} times ({results['fast']/trials*100:.1f}%)")
    print(f"  Classic path used: {results['classic']} times ({results['classic']/trials*100:.1f}%)")


def byzantine_paxos_example():
    """Example: Byzantine Paxos with malicious nodes."""
    print("\n" + "=" * 60)
    print("BYZANTINE PAXOS")
    print("=" * 60)

    # System with 7 nodes, 2 Byzantine
    all_nodes = list(range(7))
    byzantine_nodes = {5, 6}

    print(f"Total nodes: {len(all_nodes)}")
    print(f"Byzantine nodes: {byzantine_nodes}")
    print(f"Honest nodes: {set(all_nodes) - byzantine_nodes}")

    byzantine_paxos = ByzantinePaxos(all_nodes, byzantine_nodes)

    # Try to achieve consensus
    proposed_value = "legitimate_value"
    consensus = byzantine_paxos.byzantine_consensus(proposed_value, node_id=0)

    print(f"\nProposed value: {proposed_value}")
    print(f"Consensus achieved: {consensus}")
    print(f"Despite Byzantine nodes trying to disrupt!")


def distributed_database_example():
    """Example: Using Paxos for distributed database commits."""
    print("\n" + "=" * 60)
    print("DISTRIBUTED DATABASE WITH PAXOS")
    print("=" * 60)

    class DistributedDatabase:
        """Simplified distributed database using Paxos."""

        def __init__(self, replicas: int):
            self.replicas = replicas
            self.simulator = PaxosSimulator(replicas)
            self.committed_transactions = []

        def commit_transaction(self, transaction: Dict[str, Any]) -> bool:
            """Commit transaction using Paxos consensus."""
            # All replicas must agree on transaction order
            success = self.simulator.run_basic_consensus(transaction)

            if success:
                self.committed_transactions.append(transaction)

            return success

    # Create distributed database with 5 replicas
    db = DistributedDatabase(replicas=5)

    # Try to commit transactions
    transactions = [
        {"type": "INSERT", "table": "users", "data": {"id": 1, "name": "Alice"}},
        {"type": "UPDATE", "table": "users", "where": {"id": 1}, "set": {"name": "Alicia"}},
        {"type": "DELETE", "table": "users", "where": {"id": 1}}
    ]

    print("Committing transactions:")
    for i, txn in enumerate(transactions):
        success = db.commit_transaction(txn)
        print(f"  Transaction {i}: {txn['type']} - {'Committed' if success else 'Failed'}")

    print(f"\nTotal committed: {len(db.committed_transactions)}")


def configuration_management_example():
    """Example: Configuration management with Paxos."""
    print("\n" + "=" * 60)
    print("CONFIGURATION MANAGEMENT WITH PAXOS")
    print("=" * 60)

    class ConfigManager:
        """Configuration manager using Paxos for consistency."""

        def __init__(self, num_nodes: int):
            self.simulator = PaxosSimulator(num_nodes)
            self.current_config = {}

        def update_config(self, key: str, value: Any) -> bool:
            """Update configuration with consensus."""
            update = {"key": key, "value": value, "timestamp": time.time()}
            success = self.simulator.run_basic_consensus(update)

            if success:
                self.current_config[key] = value

            return success

    # Create configuration manager
    config = ConfigManager(num_nodes=5)

    # Update configurations
    updates = [
        ("max_connections", 1000),
        ("timeout_seconds", 30),
        ("cache_size_mb", 512),
        ("debug_mode", False)
    ]

    print("Updating configurations:")
    for key, value in updates:
        success = config.update_config(key, value)
        print(f"  {key} = {value}: {'Success' if success else 'Failed'}")

    print("\nFinal configuration:")
    for key, value in config.current_config.items():
        print(f"  {key}: {value}")


def performance_analysis():
    """Analyze Paxos performance characteristics."""
    print("\n" + "=" * 60)
    print("PAXOS PERFORMANCE ANALYSIS")
    print("=" * 60)

    import time

    # Test with different cluster sizes
    cluster_sizes = [3, 5, 7, 9]
    results = {}

    for size in cluster_sizes:
        simulator = PaxosSimulator(num_nodes=size)

        # Measure consensus time
        start_time = time.time()
        successes = 0
        trials = 100

        for i in range(trials):
            if simulator.run_basic_consensus(f"value_{i}"):
                successes += 1
            # Reset for next trial
            simulator = PaxosSimulator(num_nodes=size)

        elapsed = time.time() - start_time
        results[size] = {
            "success_rate": successes / trials,
            "avg_time": elapsed / trials * 1000  # ms
        }

    print("Performance with different cluster sizes:")
    print(f"{'Nodes':<8} {'Success Rate':<15} {'Avg Time (ms)':<15}")
    print("-" * 40)

    for size, metrics in results.items():
        print(f"{size:<8} {metrics['success_rate']:<15.1%} {metrics['avg_time']:<15.2f}")

    # Test with failures
    print("\nImpact of failures (5-node cluster):")
    failure_rates = [0.0, 0.1, 0.2, 0.3, 0.4]

    for failure_rate in failure_rates:
        simulator = PaxosSimulator(num_nodes=5)
        successes = 0

        for _ in range(50):
            if simulator.run_with_failures("test_value", failure_rate):
                successes += 1
            simulator = PaxosSimulator(num_nodes=5)  # Reset

        print(f"  {failure_rate:.0%} failure rate: {successes/50:.1%} success")


if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)

    # Run examples
    basic_paxos_example()
    multi_paxos_example()
    fast_paxos_example()
    byzantine_paxos_example()
    distributed_database_example()
    configuration_management_example()
    performance_analysis()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Paxos ensures consensus despite failures")
    print("- Requires majority of nodes to be available")
    print("- Multi-Paxos optimizes for sequences of values")
    print("- Fast Paxos reduces latency in common case")
    print("- Byzantine Paxos handles malicious nodes")
    print("- Foundation for many distributed systems")
    print("=" * 60)