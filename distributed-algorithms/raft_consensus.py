"""
Raft Consensus Algorithm Implementation
=======================================

Educational implementation of the Raft consensus algorithm for
distributed systems. Raft is designed to be understandable and
provides strong consistency guarantees.

Key Components:
- Leader Election
- Log Replication
- Safety Properties
- Membership Changes (basic)

Author: Claude
Date: January 2026
"""

import random
import time
from enum import Enum
from typing import List, Optional, Dict, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict
import threading
import queue


class NodeState(Enum):
    """Possible states for a Raft node."""
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"


class MessageType(Enum):
    """Types of messages in Raft protocol."""
    REQUEST_VOTE = "request_vote"
    REQUEST_VOTE_RESPONSE = "request_vote_response"
    APPEND_ENTRIES = "append_entries"
    APPEND_ENTRIES_RESPONSE = "append_entries_response"
    CLIENT_REQUEST = "client_request"


@dataclass
class LogEntry:
    """Represents a single entry in the replicated log."""
    term: int
    index: int
    command: Any
    committed: bool = False


@dataclass
class RequestVote:
    """RequestVote RPC."""
    term: int
    candidate_id: str
    last_log_index: int
    last_log_term: int


@dataclass
class RequestVoteResponse:
    """Response to RequestVote RPC."""
    term: int
    vote_granted: bool


@dataclass
class AppendEntries:
    """AppendEntries RPC (also used as heartbeat)."""
    term: int
    leader_id: str
    prev_log_index: int
    prev_log_term: int
    entries: List[LogEntry]
    leader_commit: int


@dataclass
class AppendEntriesResponse:
    """Response to AppendEntries RPC."""
    term: int
    success: bool
    match_index: int = 0


class RaftNode:
    """
    A single node in a Raft cluster.

    This is a simplified implementation for educational purposes.
    Real implementations would handle network failures, persistence, etc.
    """

    def __init__(self, node_id: str, peers: List[str],
                 election_timeout_range: Tuple[int, int] = (150, 300)):
        """
        Initialize a Raft node.

        Args:
            node_id: Unique identifier for this node
            peers: List of other node IDs in the cluster
            election_timeout_range: Range for random election timeout (ms)
        """
        self.node_id = node_id
        self.peers = peers
        self.state = NodeState.FOLLOWER

        # Persistent state (should be stored on disk in real implementation)
        self.current_term = 0
        self.voted_for: Optional[str] = None
        self.log: List[LogEntry] = []

        # Volatile state
        self.commit_index = 0
        self.last_applied = 0

        # Leader-specific volatile state
        self.next_index: Dict[str, int] = {}
        self.match_index: Dict[str, int] = {}

        # Election state
        self.election_timeout_range = election_timeout_range
        self.reset_election_timer()
        self.votes_received = 0

        # For simulation
        self.running = False
        self.message_queue = queue.Queue()
        self.current_leader: Optional[str] = None

    def reset_election_timer(self):
        """Reset the election timeout to a random value."""
        self.election_timeout = random.uniform(*self.election_timeout_range) / 1000.0
        self.last_heartbeat_time = time.time()

    def start_election(self):
        """Start a new election."""
        self.state = NodeState.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        self.votes_received = 1  # Vote for self
        self.reset_election_timer()

        print(f"Node {self.node_id}: Starting election for term {self.current_term}")

        # Request votes from all peers
        last_log_index = len(self.log) - 1
        last_log_term = self.log[last_log_index].term if self.log else 0

        request = RequestVote(
            term=self.current_term,
            candidate_id=self.node_id,
            last_log_index=last_log_index,
            last_log_term=last_log_term
        )

        for peer in self.peers:
            self.send_message(peer, MessageType.REQUEST_VOTE, request)

    def become_leader(self):
        """Transition to leader state."""
        self.state = NodeState.LEADER
        self.current_leader = self.node_id
        print(f"Node {self.node_id}: Became leader for term {self.current_term}")

        # Initialize leader state
        for peer in self.peers:
            self.next_index[peer] = len(self.log)
            self.match_index[peer] = 0

        # Send initial heartbeat
        self.send_heartbeat()

    def become_follower(self, term: int):
        """Transition to follower state."""
        self.state = NodeState.FOLLOWER
        self.current_term = term
        self.voted_for = None
        self.votes_received = 0
        self.reset_election_timer()

    def send_heartbeat(self):
        """Send heartbeat (empty AppendEntries) to all peers."""
        for peer in self.peers:
            prev_log_index = self.next_index[peer] - 1
            prev_log_term = 0
            if prev_log_index >= 0 and prev_log_index < len(self.log):
                prev_log_term = self.log[prev_log_index].term

            append_entries = AppendEntries(
                term=self.current_term,
                leader_id=self.node_id,
                prev_log_index=prev_log_index,
                prev_log_term=prev_log_term,
                entries=[],  # Heartbeat has no entries
                leader_commit=self.commit_index
            )

            self.send_message(peer, MessageType.APPEND_ENTRIES, append_entries)

    def handle_request_vote(self, request: RequestVote) -> RequestVoteResponse:
        """Handle RequestVote RPC."""
        # Reply false if term < currentTerm
        if request.term < self.current_term:
            return RequestVoteResponse(self.current_term, False)

        # If RPC request term > currentTerm, update and become follower
        if request.term > self.current_term:
            self.become_follower(request.term)

        # Check if we can vote for this candidate
        vote_granted = False
        if (self.voted_for is None or self.voted_for == request.candidate_id):
            # Check if candidate's log is at least as up-to-date as ours
            last_log_index = len(self.log) - 1
            last_log_term = self.log[last_log_index].term if self.log else 0

            if (request.last_log_term > last_log_term or
                (request.last_log_term == last_log_term and
                 request.last_log_index >= last_log_index)):
                vote_granted = True
                self.voted_for = request.candidate_id
                self.reset_election_timer()

        return RequestVoteResponse(self.current_term, vote_granted)

    def handle_request_vote_response(self, response: RequestVoteResponse):
        """Handle response to RequestVote RPC."""
        if self.state != NodeState.CANDIDATE:
            return

        if response.term > self.current_term:
            self.become_follower(response.term)
            return

        if response.vote_granted:
            self.votes_received += 1
            # Check if we have majority
            if self.votes_received > (len(self.peers) + 1) // 2:
                self.become_leader()

    def handle_append_entries(self, request: AppendEntries) -> AppendEntriesResponse:
        """Handle AppendEntries RPC."""
        # Reply false if term < currentTerm
        if request.term < self.current_term:
            return AppendEntriesResponse(self.current_term, False)

        # If RPC request term > currentTerm, update and become follower
        if request.term > self.current_term:
            self.become_follower(request.term)

        # Reset election timer when receiving from current leader
        self.reset_election_timer()
        self.current_leader = request.leader_id

        # Check if log contains entry at prevLogIndex with prevLogTerm
        if request.prev_log_index >= 0:
            if (request.prev_log_index >= len(self.log) or
                self.log[request.prev_log_index].term != request.prev_log_term):
                return AppendEntriesResponse(self.current_term, False)

        # Append new entries (if any)
        if request.entries:
            # Remove conflicting entries
            insert_index = request.prev_log_index + 1
            self.log = self.log[:insert_index]
            # Append new entries
            self.log.extend(request.entries)

        # Update commit index
        if request.leader_commit > self.commit_index:
            self.commit_index = min(request.leader_commit, len(self.log) - 1)
            self.apply_committed_entries()

        return AppendEntriesResponse(
            self.current_term,
            True,
            request.prev_log_index + len(request.entries)
        )

    def handle_append_entries_response(self, peer: str, response: AppendEntriesResponse):
        """Handle response to AppendEntries RPC."""
        if self.state != NodeState.LEADER:
            return

        if response.term > self.current_term:
            self.become_follower(response.term)
            return

        if response.success:
            # Update match_index and next_index
            self.match_index[peer] = response.match_index
            self.next_index[peer] = response.match_index + 1

            # Check if we can advance commit_index
            self.update_commit_index()
        else:
            # Decrement next_index and retry
            self.next_index[peer] = max(0, self.next_index[peer] - 1)

    def update_commit_index(self):
        """Update commit index based on majority replication."""
        if self.state != NodeState.LEADER:
            return

        # Find the highest index replicated on majority of servers
        for n in range(self.commit_index + 1, len(self.log)):
            if self.log[n].term == self.current_term:
                replicated_count = 1  # Count self
                for peer in self.peers:
                    if self.match_index.get(peer, 0) >= n:
                        replicated_count += 1

                if replicated_count > (len(self.peers) + 1) // 2:
                    self.commit_index = n
                    self.apply_committed_entries()

    def apply_committed_entries(self):
        """Apply committed entries to state machine."""
        while self.last_applied < self.commit_index:
            self.last_applied += 1
            entry = self.log[self.last_applied]
            print(f"Node {self.node_id}: Applied command {entry.command} at index {self.last_applied}")

    def append_command(self, command: Any) -> bool:
        """
        Append a new command to the log (leader only).

        Args:
            command: Command to append

        Returns:
            True if accepted (is leader), False otherwise
        """
        if self.state != NodeState.LEADER:
            return False

        # Append to own log
        entry = LogEntry(
            term=self.current_term,
            index=len(self.log),
            command=command
        )
        self.log.append(entry)

        # Replicate to followers
        self.replicate_log()
        return True

    def replicate_log(self):
        """Replicate log entries to all followers."""
        if self.state != NodeState.LEADER:
            return

        for peer in self.peers:
            prev_log_index = self.next_index[peer] - 1
            prev_log_term = 0
            if prev_log_index >= 0 and prev_log_index < len(self.log):
                prev_log_term = self.log[prev_log_index].term

            # Send all entries from next_index onwards
            entries = self.log[self.next_index[peer]:]

            append_entries = AppendEntries(
                term=self.current_term,
                leader_id=self.node_id,
                prev_log_index=prev_log_index,
                prev_log_term=prev_log_term,
                entries=entries,
                leader_commit=self.commit_index
            )

            self.send_message(peer, MessageType.APPEND_ENTRIES, append_entries)

    def send_message(self, target: str, msg_type: MessageType, content: Any):
        """
        Send a message to another node.

        In a real implementation, this would use network communication.
        """
        # For simulation, just print
        print(f"Node {self.node_id} -> Node {target}: {msg_type.value}")

    def check_election_timeout(self):
        """Check if election timeout has elapsed."""
        if self.state != NodeState.LEADER:
            elapsed = time.time() - self.last_heartbeat_time
            if elapsed > self.election_timeout:
                print(f"Node {self.node_id}: Election timeout! Starting election...")
                self.start_election()


class RaftCluster:
    """
    Simulates a Raft cluster for testing and demonstration.
    """

    def __init__(self, num_nodes: int = 5):
        """
        Initialize a Raft cluster.

        Args:
            num_nodes: Number of nodes in the cluster
        """
        self.node_ids = [f"node_{i}" for i in range(num_nodes)]
        self.nodes = {}

        # Create nodes
        for node_id in self.node_ids:
            peers = [nid for nid in self.node_ids if nid != node_id]
            self.nodes[node_id] = RaftNode(node_id, peers)

    def simulate_step(self):
        """Simulate one step of the cluster."""
        # Check election timeouts
        for node in self.nodes.values():
            node.check_election_timeout()

        # Send heartbeats from leaders
        for node in self.nodes.values():
            if node.state == NodeState.LEADER:
                node.send_heartbeat()

    def get_leader(self) -> Optional[str]:
        """Get the current leader node ID."""
        for node_id, node in self.nodes.items():
            if node.state == NodeState.LEADER:
                return node_id
        return None

    def submit_command(self, command: Any) -> bool:
        """
        Submit a command to the cluster.

        Args:
            command: Command to execute

        Returns:
            True if accepted, False if no leader
        """
        leader_id = self.get_leader()
        if leader_id:
            return self.nodes[leader_id].append_command(command)
        return False

    def get_state_summary(self) -> Dict[str, str]:
        """Get summary of cluster state."""
        return {
            node_id: {
                'state': node.state.value,
                'term': node.current_term,
                'log_length': len(node.log),
                'commit_index': node.commit_index
            }
            for node_id, node in self.nodes.items()
        }


def example_usage():
    """Demonstrate Raft consensus algorithm."""
    print("=" * 60)
    print("RAFT CONSENSUS ALGORITHM DEMONSTRATION")
    print("=" * 60)

    # Create a 5-node cluster
    cluster = RaftCluster(num_nodes=5)

    print("\n1. Initial Cluster State:")
    print("-" * 40)
    for node_id, info in cluster.get_state_summary().items():
        print(f"{node_id}: {info}")

    print("\n2. Simulating Election:")
    print("-" * 40)

    # Simulate a few steps to trigger election
    for i in range(3):
        print(f"\nStep {i+1}:")
        cluster.simulate_step()
        time.sleep(0.1)  # Small delay for visualization

        leader = cluster.get_leader()
        if leader:
            print(f"Leader elected: {leader}")
            break

    print("\n3. Current Cluster State:")
    print("-" * 40)
    for node_id, info in cluster.get_state_summary().items():
        print(f"{node_id}: {info}")

    print("\n4. Log Replication:")
    print("-" * 40)

    # Submit some commands
    commands = ["SET x 1", "SET y 2", "SET z 3"]
    for cmd in commands:
        if cluster.submit_command(cmd):
            print(f"Command submitted: {cmd}")
        else:
            print(f"Failed to submit command (no leader): {cmd}")

    print("\n5. Raft Properties:")
    print("-" * 40)

    properties = {
        "Election Safety": "At most one leader per term",
        "Leader Append-Only": "Leader never overwrites its log",
        "Log Matching": "If two logs have same entry, they're identical up to that entry",
        "Leader Completeness": "Committed entries appear in all future leaders' logs",
        "State Machine Safety": "All servers apply same commands in same order"
    }

    for prop, desc in properties.items():
        print(f"• {prop}: {desc}")

    print("\n6. Failure Scenarios:")
    print("-" * 40)

    scenarios = [
        "Network Partition: Cluster splits into two groups",
        "Leader Failure: New leader elected from remaining nodes",
        "Follower Failure: System continues with remaining nodes",
        "Byzantine Failure: NOT handled by Raft (use PBFT instead)"
    ]

    for scenario in scenarios:
        print(f"• {scenario}")

    print("\n7. Use Cases:")
    print("-" * 40)

    use_cases = [
        "etcd - Distributed key-value store",
        "Consul - Service discovery and configuration",
        "CockroachDB - Distributed SQL database",
        "TiKV - Distributed transactional key-value database"
    ]

    for use_case in use_cases:
        print(f"• {use_case}")

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Raft provides strong consistency in distributed systems")
    print("- Leader election ensures single point of coordination")
    print("- Log replication ensures all nodes have same data")
    print("- Designed to be understandable (vs Paxos)")
    print("- Handles node failures but not Byzantine failures")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()