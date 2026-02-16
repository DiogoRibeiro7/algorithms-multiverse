"""
Byzantine Fault Tolerance (BFT) Algorithms Implementation
=========================================================

Educational implementation of Byzantine Fault Tolerance algorithms
for distributed systems that can tolerate malicious failures.

Byzantine failures are the most general and difficult type of failure
where nodes can behave arbitrarily (lie, send conflicting messages, etc).

Key Algorithms:
- Byzantine Generals Problem
- Simple Byzantine Agreement
- Practical Byzantine Fault Tolerance (PBFT) - Simplified
- Byzantine Failure Detection

Author: Claude
Date: January 2026
"""

import random
import hashlib
import time
from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, Counter
from enum import Enum
import json


class NodeType(Enum):
    """Types of nodes in Byzantine system."""
    HONEST = "honest"
    BYZANTINE = "byzantine"
    FAULTY = "faulty"


class MessageType(Enum):
    """Types of messages in BFT protocols."""
    PROPOSE = "propose"
    ECHO = "echo"
    READY = "ready"
    COMMIT = "commit"
    VIEW_CHANGE = "view_change"
    PREPARE = "prepare"


@dataclass
class BFTMessage:
    """Generic BFT message structure."""
    sender: str
    msg_type: MessageType
    value: Any
    round: int
    signature: Optional[str] = None
    view: int = 0
    sequence: int = 0


class ByzantineGenerals:
    """
    Classic Byzantine Generals Problem implementation.

    Demonstrates the impossibility result for 3 generals with 1 traitor
    and shows how 4 generals can reach consensus with 1 traitor.
    """

    def __init__(self, n_generals: int, n_byzantine: int):
        """
        Initialize Byzantine Generals scenario.

        Args:
            n_generals: Total number of generals
            n_byzantine: Number of Byzantine (traitorous) generals
        """
        self.n_generals = n_generals
        self.n_byzantine = n_byzantine
        self.generals = []

        # Create generals
        for i in range(n_generals):
            is_byzantine = i < n_byzantine
            general = {
                'id': f'general_{i}',
                'type': NodeType.BYZANTINE if is_byzantine else NodeType.HONEST,
                'is_commander': i == n_generals - 1,
                'decision': None,
                'received_values': defaultdict(list)
            }
            self.generals.append(general)

    def oral_messages(self, initial_value: bool, max_rounds: int) -> Dict[str, Any]:
        """
        OM(m) - Oral Messages algorithm.

        Solves Byzantine Generals with n > 3f where f is number of traitors.

        Args:
            initial_value: Commander's initial value (attack/retreat)
            max_rounds: Number of rounds (should be f+1)

        Returns:
            Decision of each general
        """
        print(f"\n=== Byzantine Generals: OM({max_rounds-1}) Algorithm ===")
        print(f"Generals: {self.n_generals}, Byzantine: {self.n_byzantine}")
        print(f"Commander proposes: {'ATTACK' if initial_value else 'RETREAT'}")

        # Round 0: Commander sends initial value
        commander = self.generals[-1]
        for general in self.generals[:-1]:
            if general['type'] == NodeType.HONEST:
                general['received_values'][commander['id']].append(initial_value)
            else:
                # Byzantine general might receive wrong value
                general['received_values'][commander['id']].append(
                    random.choice([True, False])
                )

        # Subsequent rounds
        for round_num in range(1, max_rounds):
            print(f"\nRound {round_num}:")

            # Each general shares what they heard
            for sender in self.generals[:-1]:  # Exclude commander
                for receiver in self.generals:
                    if sender['id'] != receiver['id'] and not receiver['is_commander']:
                        # Determine what value to send
                        if sender['type'] == NodeType.HONEST:
                            # Honest general forwards what they heard
                            if commander['id'] in sender['received_values']:
                                value = sender['received_values'][commander['id']][-1]
                            else:
                                value = False  # Default
                        else:
                            # Byzantine general sends random values
                            value = random.choice([True, False])

                        receiver['received_values'][sender['id']].append(value)

        # Each general makes decision based on majority
        decisions = {}
        for general in self.generals:
            if general['is_commander']:
                decisions[general['id']] = initial_value
            else:
                # Count votes
                votes = []
                for values in general['received_values'].values():
                    votes.extend(values)

                # Majority decision
                attack_votes = sum(votes)
                retreat_votes = len(votes) - attack_votes

                general['decision'] = attack_votes > retreat_votes
                decisions[general['id']] = general['decision']

                print(f"{general['id']}: Attack={attack_votes}, Retreat={retreat_votes}, "
                      f"Decision={'ATTACK' if general['decision'] else 'RETREAT'}")

        # Check consensus
        honest_decisions = [
            decisions[g['id']] for g in self.generals
            if g['type'] == NodeType.HONEST
        ]

        consensus = len(set(honest_decisions)) == 1
        print(f"\nConsensus achieved: {consensus}")

        return decisions

    def impossibility_demo(self):
        """Demonstrate impossibility with 3 generals, 1 traitor."""
        print("\n=== Impossibility Result: 3 Generals, 1 Traitor ===")

        # Scenario 1: Commander is traitor
        print("\nScenario 1: Commander is traitor")
        print("Commander sends ATTACK to Lieutenant 1")
        print("Commander sends RETREAT to Lieutenant 2")
        print("Result: Lieutenants cannot agree!")

        # Scenario 2: Lieutenant is traitor
        print("\nScenario 2: Lieutenant 1 is traitor")
        print("Commander sends ATTACK to both")
        print("Lieutenant 1 tells Lieutenant 2: 'Commander said RETREAT'")
        print("Lieutenant 2 sees conflicting messages")
        print("Result: Cannot distinguish from Scenario 1!")

        print("\nConclusion: Need n > 3f for f Byzantine failures")


class SimpleByzantineAgreement:
    """
    Simple Byzantine Agreement protocol.

    Achieves agreement with n > 3f nodes despite f Byzantine failures.
    Uses echo and ready phases for agreement.
    """

    def __init__(self, n_nodes: int, f_byzantine: int):
        """
        Initialize Byzantine Agreement.

        Args:
            n_nodes: Total number of nodes
            f_byzantine: Maximum Byzantine failures to tolerate
        """
        self.n = n_nodes
        self.f = f_byzantine
        self.nodes = {}

        # Create nodes
        for i in range(n_nodes):
            node_id = f"node_{i}"
            self.nodes[node_id] = {
                'id': node_id,
                'type': NodeType.BYZANTINE if i < f_byzantine else NodeType.HONEST,
                'proposed_value': None,
                'echo_sent': False,
                'ready_sent': False,
                'echo_received': defaultdict(set),
                'ready_received': defaultdict(set),
                'decided': False,
                'decision': None
            }

    def broadcast_reliable(self, proposer_id: str, value: Any) -> Dict[str, Any]:
        """
        Reliable broadcast with Byzantine Agreement.

        Args:
            proposer_id: Node proposing the value
            value: Value to agree upon

        Returns:
            Decision of each node
        """
        print(f"\n=== Byzantine Agreement Protocol ===")
        print(f"Nodes: {self.n}, Byzantine: {self.f}")
        print(f"Proposer: {proposer_id}, Value: {value}")

        # Phase 1: Propose
        print("\nPhase 1: PROPOSE")
        proposer = self.nodes[proposer_id]
        proposer['proposed_value'] = value

        # Broadcast to all
        for node_id, node in self.nodes.items():
            if node['type'] == NodeType.HONEST:
                node['echo_received'][value].add(proposer_id)

        # Phase 2: Echo
        print("\nPhase 2: ECHO")
        for node_id, node in self.nodes.items():
            if node['type'] == NodeType.HONEST and not node['echo_sent']:
                # Check if received proposal
                for val, senders in node['echo_received'].items():
                    if len(senders) >= 1 and not node['echo_sent']:
                        # Send echo
                        node['echo_sent'] = True
                        self._send_echo(node_id, val)

        # Phase 3: Ready
        print("\nPhase 3: READY")
        ready_rounds = 0
        while ready_rounds < 2:  # May need multiple ready rounds
            ready_rounds += 1

            for node_id, node in self.nodes.items():
                if node['type'] == NodeType.HONEST and not node['ready_sent']:
                    # Check echo threshold
                    for val, senders in node['echo_received'].items():
                        if len(senders) > (self.n + self.f) / 2:
                            node['ready_sent'] = True
                            self._send_ready(node_id, val)
                            break

                    # Check ready threshold
                    if not node['ready_sent']:
                        for val, senders in node['ready_received'].items():
                            if len(senders) >= self.f + 1:
                                node['ready_sent'] = True
                                self._send_ready(node_id, val)
                                break

        # Phase 4: Decide
        print("\nPhase 4: DECIDE")
        decisions = {}
        for node_id, node in self.nodes.items():
            if node['type'] == NodeType.HONEST:
                for val, senders in node['ready_received'].items():
                    if len(senders) >= 2 * self.f + 1:
                        node['decided'] = True
                        node['decision'] = val
                        decisions[node_id] = val
                        print(f"{node_id} decides: {val}")
                        break

            if node_id not in decisions and node['type'] == NodeType.HONEST:
                # Default decision
                node['decision'] = None
                decisions[node_id] = None

        # Check agreement
        honest_decisions = [
            d for nid, d in decisions.items()
            if self.nodes[nid]['type'] == NodeType.HONEST and d is not None
        ]

        if honest_decisions:
            agreement = len(set(honest_decisions)) == 1
            print(f"\nAgreement achieved: {agreement}")
        else:
            print("\nNo agreement reached")

        return decisions

    def _send_echo(self, sender_id: str, value: Any):
        """Send echo message from a node."""
        sender = self.nodes[sender_id]

        for node_id, node in self.nodes.items():
            if sender['type'] == NodeType.HONEST:
                # Honest node sends correct value
                node['echo_received'][value].add(sender_id)
            else:
                # Byzantine node might send different values
                fake_value = f"fake_{value}" if random.random() < 0.5 else value
                node['echo_received'][fake_value].add(sender_id)

    def _send_ready(self, sender_id: str, value: Any):
        """Send ready message from a node."""
        sender = self.nodes[sender_id]

        for node_id, node in self.nodes.items():
            if sender['type'] == NodeType.HONEST:
                # Honest node sends correct value
                node['ready_received'][value].add(sender_id)
            else:
                # Byzantine node might send different values
                fake_value = f"fake_{value}" if random.random() < 0.5 else value
                node['ready_received'][fake_value].add(sender_id)


class SimplifiedPBFT:
    """
    Simplified version of Practical Byzantine Fault Tolerance (PBFT).

    PBFT is the most influential BFT consensus protocol for
    practical systems. This is a simplified educational version.
    """

    def __init__(self, n_replicas: int, f_byzantine: int):
        """
        Initialize PBFT system.

        Args:
            n_replicas: Total number of replicas (n = 3f + 1)
            f_byzantine: Maximum Byzantine failures to tolerate
        """
        self.n = n_replicas
        self.f = f_byzantine
        self.replicas = {}
        self.view = 0
        self.sequence = 0

        # Create replicas
        for i in range(n_replicas):
            replica_id = f"replica_{i}"
            self.replicas[replica_id] = {
                'id': replica_id,
                'type': NodeType.BYZANTINE if i < f_byzantine else NodeType.HONEST,
                'is_primary': i == 0,
                'view': 0,
                'log': [],
                'prepared': defaultdict(set),
                'committed': defaultdict(set),
                'executed': set()
            }

    def request(self, client_request: str) -> bool:
        """
        Process client request through PBFT protocol.

        Args:
            client_request: Request from client

        Returns:
            True if request committed
        """
        print(f"\n=== Simplified PBFT Protocol ===")
        print(f"Replicas: {self.n}, Byzantine: {self.f}")
        print(f"Client request: {client_request}")

        # Find primary
        primary = None
        for replica in self.replicas.values():
            if replica['is_primary']:
                primary = replica
                break

        if not primary:
            print("No primary found!")
            return False

        self.sequence += 1

        # Phase 1: Pre-prepare (Primary only)
        print(f"\nPhase 1: PRE-PREPARE (Primary: {primary['id']})")

        # Create pre-prepare message
        digest = self._hash(client_request)
        pre_prepare_msg = {
            'view': self.view,
            'sequence': self.sequence,
            'digest': digest,
            'request': client_request
        }

        # Primary multicasts pre-prepare
        for replica in self.replicas.values():
            if not replica['is_primary']:
                if primary['type'] == NodeType.HONEST:
                    # Send correct message
                    replica['log'].append(pre_prepare_msg)
                else:
                    # Byzantine primary might send different messages
                    if random.random() < 0.5:
                        fake_msg = pre_prepare_msg.copy()
                        fake_msg['digest'] = self._hash("fake_" + client_request)
                        replica['log'].append(fake_msg)
                    else:
                        replica['log'].append(pre_prepare_msg)

        # Phase 2: Prepare (All backups)
        print("\nPhase 2: PREPARE")

        for replica_id, replica in self.replicas.items():
            if not replica['is_primary'] and replica['type'] == NodeType.HONEST:
                # Check pre-prepare message
                if replica['log']:
                    msg = replica['log'][-1]
                    # Broadcast prepare
                    self._broadcast_prepare(replica_id, msg['sequence'], msg['digest'])

        # Collect prepares
        prepare_count = defaultdict(int)
        for replica in self.replicas.values():
            if replica['type'] == NodeType.HONEST:
                for seq, digests in replica['prepared'].items():
                    for digest in digests:
                        prepare_count[(seq, digest)] += 1

        # Check if prepared (2f prepares)
        prepared = False
        prepared_digest = None
        for (seq, digest), count in prepare_count.items():
            if count >= 2 * self.f and seq == self.sequence:
                prepared = True
                prepared_digest = digest
                print(f"Prepared: sequence={seq}, digest={digest[:8]}...")
                break

        if not prepared:
            print("Failed to prepare!")
            return False

        # Phase 3: Commit
        print("\nPhase 3: COMMIT")

        for replica_id, replica in self.replicas.items():
            if replica['type'] == NodeType.HONEST:
                # Send commit for prepared value
                self._broadcast_commit(replica_id, self.sequence, prepared_digest)

        # Collect commits
        commit_count = defaultdict(int)
        for replica in self.replicas.values():
            if replica['type'] == NodeType.HONEST:
                for seq, digests in replica['committed'].items():
                    for digest in digests:
                        commit_count[(seq, digest)] += 1

        # Check if committed (2f+1 commits)
        committed = False
        for (seq, digest), count in commit_count.items():
            if count >= 2 * self.f + 1 and seq == self.sequence:
                committed = True
                print(f"Committed: sequence={seq}, digest={digest[:8]}...")

                # Execute request
                for replica in self.replicas.values():
                    if replica['type'] == NodeType.HONEST:
                        replica['executed'].add((seq, digest))
                        print(f"{replica['id']} executed request")
                break

        return committed

    def _broadcast_prepare(self, sender_id: str, sequence: int, digest: str):
        """Broadcast prepare message."""
        sender = self.replicas[sender_id]

        for replica in self.replicas.values():
            if sender['type'] == NodeType.HONEST:
                replica['prepared'][sequence].add(digest)
            else:
                # Byzantine might send wrong digest
                if random.random() < 0.5:
                    replica['prepared'][sequence].add("fake_" + digest)
                else:
                    replica['prepared'][sequence].add(digest)

    def _broadcast_commit(self, sender_id: str, sequence: int, digest: str):
        """Broadcast commit message."""
        sender = self.replicas[sender_id]

        for replica in self.replicas.values():
            if sender['type'] == NodeType.HONEST:
                replica['committed'][sequence].add(digest)
            else:
                # Byzantine might send wrong digest
                if random.random() < 0.5:
                    replica['committed'][sequence].add("fake_" + digest)
                else:
                    replica['committed'][sequence].add(digest)

    def _hash(self, data: str) -> str:
        """Compute hash of data."""
        return hashlib.sha256(data.encode()).hexdigest()

    def view_change(self):
        """
        Initiate view change (leader election).

        This is a simplified version of PBFT view change.
        """
        print(f"\n=== View Change ===")
        print(f"Old view: {self.view}")

        self.view += 1
        new_primary_idx = self.view % self.n

        # Update primary
        for i, replica in enumerate(self.replicas.values()):
            replica['is_primary'] = (i == new_primary_idx)
            replica['view'] = self.view

        print(f"New view: {self.view}")
        print(f"New primary: replica_{new_primary_idx}")


class ByzantineFailureDetector:
    """
    Byzantine failure detection mechanisms.

    Detects Byzantine behavior through various techniques.
    """

    def __init__(self, n_nodes: int):
        """
        Initialize failure detector.

        Args:
            n_nodes: Number of nodes to monitor
        """
        self.n_nodes = n_nodes
        self.message_history = defaultdict(list)
        self.byzantine_scores = defaultdict(float)
        self.threshold = 0.7

    def detect_equivocation(self, messages: List[BFTMessage]) -> Set[str]:
        """
        Detect equivocation (sending different values for same round).

        Args:
            messages: List of messages to analyze

        Returns:
            Set of equivocating node IDs
        """
        equivocators = set()

        # Group messages by sender and round
        by_sender_round = defaultdict(list)
        for msg in messages:
            key = (msg.sender, msg.round, msg.msg_type)
            by_sender_round[key].append(msg.value)

        # Check for different values
        for (sender, round, msg_type), values in by_sender_round.items():
            unique_values = set(map(str, values))
            if len(unique_values) > 1:
                equivocators.add(sender)
                print(f"Equivocation detected: {sender} sent {len(unique_values)} "
                      f"different values in round {round}")

        return equivocators

    def detect_timing_violations(self, node_id: str,
                                expected_time: float,
                                actual_time: float,
                                tolerance: float = 0.1) -> bool:
        """
        Detect timing violations (too early/late responses).

        Args:
            node_id: Node to check
            expected_time: Expected response time
            actual_time: Actual response time
            tolerance: Acceptable deviation

        Returns:
            True if violation detected
        """
        deviation = abs(actual_time - expected_time) / expected_time

        if deviation > tolerance:
            self.byzantine_scores[node_id] += 0.3
            print(f"Timing violation: {node_id} deviated by {deviation:.2%}")
            return True

        return False

    def detect_invalid_signatures(self, messages: List[BFTMessage]) -> Set[str]:
        """
        Detect invalid message signatures.

        Args:
            messages: Messages to verify

        Returns:
            Set of nodes with invalid signatures
        """
        invalid_nodes = set()

        for msg in messages:
            if msg.signature:
                # Simplified signature verification
                expected_sig = self._compute_signature(msg)
                if msg.signature != expected_sig:
                    invalid_nodes.add(msg.sender)
                    self.byzantine_scores[msg.sender] += 0.5
                    print(f"Invalid signature from {msg.sender}")

        return invalid_nodes

    def detect_message_omission(self, node_id: str,
                               expected_msgs: int,
                               received_msgs: int) -> bool:
        """
        Detect selective message omission.

        Args:
            node_id: Node to check
            expected_msgs: Expected number of messages
            received_msgs: Actually received messages

        Returns:
            True if likely omission attack
        """
        omission_rate = 1 - (received_msgs / expected_msgs)

        if omission_rate > 0.3:  # Missing >30% messages
            self.byzantine_scores[node_id] += omission_rate * 0.4
            print(f"Message omission: {node_id} omitted {omission_rate:.1%} messages")
            return True

        return False

    def get_byzantine_nodes(self) -> Set[str]:
        """
        Get nodes likely exhibiting Byzantine behavior.

        Returns:
            Set of suspected Byzantine node IDs
        """
        byzantine_nodes = {
            node_id for node_id, score in self.byzantine_scores.items()
            if score >= self.threshold
        }

        return byzantine_nodes

    def _compute_signature(self, msg: BFTMessage) -> str:
        """Compute message signature (simplified)."""
        data = f"{msg.sender}:{msg.msg_type.value}:{msg.value}:{msg.round}"
        return hashlib.md5(data.encode()).hexdigest()[:8]


def example_usage():
    """Demonstrate Byzantine Fault Tolerance algorithms."""
    print("=" * 60)
    print("BYZANTINE FAULT TOLERANCE DEMONSTRATION")
    print("=" * 60)

    # 1. Byzantine Generals Problem
    print("\n1. BYZANTINE GENERALS PROBLEM")
    print("-" * 40)

    # Show impossibility
    generals = ByzantineGenerals(3, 1)
    generals.impossibility_demo()

    # Show solution with 4 generals
    print("\n\nSolution with 4 generals, 1 traitor:")
    generals = ByzantineGenerals(4, 1)
    generals.oral_messages(initial_value=True, max_rounds=2)

    # 2. Byzantine Agreement
    print("\n\n2. BYZANTINE AGREEMENT PROTOCOL")
    print("-" * 40)

    agreement = SimpleByzantineAgreement(n_nodes=7, f_byzantine=2)
    decisions = agreement.broadcast_reliable("node_0", "value_X")

    # 3. Simplified PBFT
    print("\n\n3. PRACTICAL BYZANTINE FAULT TOLERANCE (PBFT)")
    print("-" * 40)

    pbft = SimplifiedPBFT(n_replicas=4, f_byzantine=1)

    # Process some requests
    requests = [
        "transfer(A, B, 100)",
        "balance(A)",
        "deposit(C, 50)"
    ]

    for req in requests[:1]:  # Demo with first request
        success = pbft.request(req)
        print(f"Request '{req}' committed: {success}")

    # Demonstrate view change
    pbft.view_change()

    # 4. Byzantine Failure Detection
    print("\n\n4. BYZANTINE FAILURE DETECTION")
    print("-" * 40)

    detector = ByzantineFailureDetector(n_nodes=5)

    # Create some messages with Byzantine behavior
    messages = [
        BFTMessage("node_1", MessageType.PREPARE, "value_A", round=1),
        BFTMessage("node_1", MessageType.PREPARE, "value_B", round=1),  # Equivocation!
        BFTMessage("node_2", MessageType.PREPARE, "value_A", round=1),
        BFTMessage("node_3", MessageType.PREPARE, "value_A", round=1),
    ]

    equivocators = detector.detect_equivocation(messages)
    print(f"Detected equivocators: {equivocators}")

    # Check timing violations
    detector.detect_timing_violations("node_4", expected_time=1.0, actual_time=1.5)

    # Check message omission
    detector.detect_message_omission("node_4", expected_msgs=10, received_msgs=6)

    # Get suspected Byzantine nodes
    byzantine_nodes = detector.get_byzantine_nodes()
    print(f"\nSuspected Byzantine nodes: {byzantine_nodes}")

    # 5. Key Properties and Insights
    print("\n\n5. KEY PROPERTIES OF BFT SYSTEMS")
    print("-" * 40)

    properties = {
        "Safety": "All honest nodes agree on same value",
        "Liveness": "System makes progress despite failures",
        "Fault Tolerance": "Tolerates f Byzantine failures with n ≥ 3f+1 nodes",
        "Message Complexity": "O(n²) messages per consensus round",
        "Time Complexity": "O(f) rounds in synchronous model"
    }

    for prop, desc in properties.items():
        print(f"• {prop}: {desc}")

    print("\n6. COMPARISON OF BFT ALGORITHMS")
    print("-" * 40)

    comparison = {
        "Byzantine Generals (OM)": {
            "Fault tolerance": "n > 3f",
            "Rounds": "f + 1",
            "Messages": "Exponential",
            "Use case": "Theoretical foundation"
        },
        "PBFT": {
            "Fault tolerance": "n ≥ 3f + 1",
            "Rounds": "3 phases",
            "Messages": "O(n²)",
            "Use case": "Permissioned blockchains"
        },
        "HotStuff": {
            "Fault tolerance": "n ≥ 3f + 1",
            "Rounds": "Linear",
            "Messages": "O(n)",
            "Use case": "Modern blockchains"
        },
        "Tendermint": {
            "Fault tolerance": "n ≥ 3f + 1",
            "Rounds": "2 phases",
            "Messages": "O(n²)",
            "Use case": "Cosmos blockchain"
        }
    }

    for algo, props in comparison.items():
        print(f"\n{algo}:")
        for key, value in props.items():
            print(f"  - {key}: {value}")

    print("\n7. REAL-WORLD APPLICATIONS")
    print("-" * 40)

    applications = [
        "Blockchain consensus (Bitcoin's Nakamoto consensus is probabilistic BFT)",
        "Distributed databases (CockroachDB uses Raft, but BFT variants exist)",
        "State machine replication in critical systems",
        "Secure multiparty computation",
        "Fault-tolerant cloud services",
        "Military command and control systems"
    ]

    for app in applications:
        print(f"• {app}")

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Byzantine failures are the hardest to handle (arbitrary behavior)")
    print("- Requires n ≥ 3f+1 nodes to tolerate f Byzantine failures")
    print("- Trade-off between fault tolerance and performance")
    print("- Critical for blockchain and distributed ledger technologies")
    print("- Detection mechanisms can identify Byzantine behavior")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()