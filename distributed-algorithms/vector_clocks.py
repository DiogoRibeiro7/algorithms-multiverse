"""
Vector Clocks and Logical Time Implementation
=============================================

Educational implementation of logical time algorithms for distributed systems:
- Lamport Timestamps (scalar logical clocks)
- Vector Clocks (vector logical clocks)
- Version Vectors
- Interval Tree Clocks (ITC)
- Causal ordering detection

These algorithms help establish causality and ordering of events
in distributed systems without synchronized physical clocks.

Author: Claude
Date: January 2026
"""

from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass, field
from copy import deepcopy
import json


class LamportClock:
    """
    Lamport Timestamp (Logical Clock) implementation.

    Provides a partial ordering of events in a distributed system.
    Simple but cannot detect concurrent events.
    """

    def __init__(self, process_id: str):
        """
        Initialize Lamport clock.

        Args:
            process_id: Unique identifier for this process
        """
        self.process_id = process_id
        self.counter = 0

    def tick(self) -> int:
        """
        Increment clock for local event.

        Returns:
            Updated timestamp
        """
        self.counter += 1
        return self.counter

    def send(self) -> int:
        """
        Update clock for send event.

        Returns:
            Timestamp to attach to message
        """
        return self.tick()

    def receive(self, received_timestamp: int) -> int:
        """
        Update clock for receive event.

        Args:
            received_timestamp: Timestamp from received message

        Returns:
            Updated local timestamp
        """
        self.counter = max(self.counter, received_timestamp) + 1
        return self.counter

    def get_time(self) -> int:
        """Get current logical time."""
        return self.counter

    def happens_before(self, t1: int, t2: int) -> Optional[bool]:
        """
        Check if t1 happens-before t2.

        Note: Can only determine if t1 < t2, not true causality.

        Returns:
            True if t1 < t2, False if t1 >= t2
        """
        return t1 < t2


class VectorClock:
    """
    Vector Clock implementation.

    Provides a partial ordering that can detect concurrent events.
    Each process maintains a vector of logical times for all processes.
    """

    def __init__(self, process_id: str, process_list: List[str]):
        """
        Initialize vector clock.

        Args:
            process_id: This process's ID
            process_list: List of all process IDs in the system
        """
        self.process_id = process_id
        self.process_list = process_list
        self.clock = {pid: 0 for pid in process_list}

        if process_id not in process_list:
            raise ValueError(f"Process {process_id} not in process list")

    def tick(self) -> Dict[str, int]:
        """
        Increment clock for local event.

        Returns:
            Updated vector clock
        """
        self.clock[self.process_id] += 1
        return self.clock.copy()

    def send(self) -> Dict[str, int]:
        """
        Update clock for send event.

        Returns:
            Vector clock to attach to message
        """
        self.tick()
        return self.clock.copy()

    def receive(self, received_clock: Dict[str, int]) -> Dict[str, int]:
        """
        Update clock for receive event.

        Args:
            received_clock: Vector clock from received message

        Returns:
            Updated local vector clock
        """
        # Update to max of local and received for each process
        for pid in self.process_list:
            if pid in received_clock:
                self.clock[pid] = max(self.clock[pid], received_clock[pid])

        # Increment own component
        self.clock[self.process_id] += 1

        return self.clock.copy()

    def get_time(self) -> Dict[str, int]:
        """Get current vector clock."""
        return self.clock.copy()

    @staticmethod
    def happens_before(vc1: Dict[str, int], vc2: Dict[str, int]) -> bool:
        """
        Check if vc1 happens-before vc2.

        vc1 < vc2 iff:
        - vc1[i] <= vc2[i] for all i, and
        - vc1[j] < vc2[j] for at least one j

        Args:
            vc1: First vector clock
            vc2: Second vector clock

        Returns:
            True if vc1 happens-before vc2
        """
        all_processes = set(vc1.keys()) | set(vc2.keys())

        less_or_equal = all(
            vc1.get(p, 0) <= vc2.get(p, 0) for p in all_processes
        )

        strictly_less = any(
            vc1.get(p, 0) < vc2.get(p, 0) for p in all_processes
        )

        return less_or_equal and strictly_less

    @staticmethod
    def concurrent(vc1: Dict[str, int], vc2: Dict[str, int]) -> bool:
        """
        Check if two events are concurrent (causally independent).

        Events are concurrent if neither happens-before the other.

        Args:
            vc1: First vector clock
            vc2: Second vector clock

        Returns:
            True if events are concurrent
        """
        return (not VectorClock.happens_before(vc1, vc2) and
                not VectorClock.happens_before(vc2, vc1))

    @staticmethod
    def merge(vc1: Dict[str, int], vc2: Dict[str, int]) -> Dict[str, int]:
        """
        Merge two vector clocks (take component-wise maximum).

        Args:
            vc1: First vector clock
            vc2: Second vector clock

        Returns:
            Merged vector clock
        """
        all_processes = set(vc1.keys()) | set(vc2.keys())
        merged = {}

        for p in all_processes:
            merged[p] = max(vc1.get(p, 0), vc2.get(p, 0))

        return merged


class VersionVector:
    """
    Version Vector for tracking updates in distributed storage.

    Similar to vector clocks but tracks update counts rather than logical time.
    Used in systems like Amazon Dynamo, Riak, etc.
    """

    def __init__(self, node_id: str):
        """
        Initialize version vector.

        Args:
            node_id: This node's identifier
        """
        self.node_id = node_id
        self.versions: Dict[str, int] = {}

    def increment(self, node: Optional[str] = None) -> Dict[str, int]:
        """
        Increment version for a node.

        Args:
            node: Node to increment (self if None)

        Returns:
            Updated version vector
        """
        if node is None:
            node = self.node_id

        self.versions[node] = self.versions.get(node, 0) + 1
        return self.versions.copy()

    def update(self, other: Dict[str, int]):
        """
        Update with another version vector.

        Args:
            other: Version vector to merge
        """
        for node, version in other.items():
            self.versions[node] = max(self.versions.get(node, 0), version)

    def descends_from(self, other: Dict[str, int]) -> bool:
        """
        Check if this version descends from another.

        Returns:
            True if this >= other for all components
        """
        for node, version in other.items():
            if self.versions.get(node, 0) < version:
                return False
        return True

    def dominates(self, other: Dict[str, int]) -> bool:
        """
        Check if this version strictly dominates another.

        Returns:
            True if this > other (descends from but not equal)
        """
        return self.descends_from(other) and self.versions != other

    def conflicts_with(self, other: Dict[str, int]) -> bool:
        """
        Check if two versions conflict (concurrent updates).

        Returns:
            True if versions are concurrent
        """
        return (not self.descends_from(other) and
                not VersionVector._descends_from_static(other, self.versions))

    @staticmethod
    def _descends_from_static(v1: Dict[str, int], v2: Dict[str, int]) -> bool:
        """Static version of descends_from."""
        for node, version in v2.items():
            if v1.get(node, 0) < version:
                return False
        return True

    def get_version(self) -> Dict[str, int]:
        """Get current version vector."""
        return self.versions.copy()


@dataclass
class IntervalTreeClock:
    """
    Interval Tree Clock (ITC) - Space-efficient vector clocks.

    ITCs provide the same causality tracking as vector clocks but with
    better space efficiency when processes join and leave dynamically.
    """

    class Event:
        """Represents an event in ITC."""
        def __init__(self, id_tree: Any, event_tree: Any):
            self.id = id_tree
            self.event = event_tree

    def __init__(self):
        """Initialize ITC (simplified version)."""
        # Simplified representation
        self.id = 1.0  # Identity (fraction of the ID space)
        self.event_counter = 0

    def fork(self) -> Tuple['IntervalTreeClock', 'IntervalTreeClock']:
        """
        Fork into two clocks (for creating new process).

        Returns:
            Two new ITCs that partition the ID space
        """
        left = IntervalTreeClock()
        right = IntervalTreeClock()

        # Split ID space
        left.id = self.id / 2
        right.id = self.id / 2
        left.event_counter = self.event_counter
        right.event_counter = self.event_counter

        return left, right

    def join(self, other: 'IntervalTreeClock') -> 'IntervalTreeClock':
        """
        Join two clocks (when process leaves).

        Args:
            other: Clock to join with

        Returns:
            Joined clock
        """
        joined = IntervalTreeClock()
        joined.id = self.id + other.id
        joined.event_counter = max(self.event_counter, other.event_counter)
        return joined

    def event(self) -> int:
        """
        Record a local event.

        Returns:
            Event counter
        """
        self.event_counter += 1
        return self.event_counter

    def send(self) -> Tuple[float, int]:
        """
        Prepare clock for sending.

        Returns:
            Clock state to send
        """
        self.event()
        return (self.id, self.event_counter)

    def receive(self, clock_data: Tuple[float, int]):
        """
        Update clock on receive.

        Args:
            clock_data: Received clock state
        """
        _, received_counter = clock_data
        self.event_counter = max(self.event_counter, received_counter) + 1


class CausalityTracker:
    """
    Tracks causality relationships between events in a distributed system.
    """

    def __init__(self):
        """Initialize causality tracker."""
        self.events: Dict[str, Dict[str, int]] = {}  # Event ID -> Vector Clock
        self.causal_graph: Dict[str, Set[str]] = {}  # Event -> Set of caused events

    def add_event(self, event_id: str, vector_clock: Dict[str, int]):
        """
        Add an event with its vector clock.

        Args:
            event_id: Unique event identifier
            vector_clock: Vector clock at time of event
        """
        self.events[event_id] = vector_clock.copy()
        self.causal_graph[event_id] = set()

        # Find all events this event causally depends on
        for other_id, other_vc in self.events.items():
            if other_id != event_id:
                if VectorClock.happens_before(other_vc, vector_clock):
                    self.causal_graph[other_id].add(event_id)

    def get_causal_order(self) -> List[str]:
        """
        Get a topological ordering of events respecting causality.

        Returns:
            List of event IDs in causal order
        """
        # Build in-degree map
        in_degree = {event: 0 for event in self.events}
        for event, caused in self.causal_graph.items():
            for e in caused:
                in_degree[e] += 1

        # Topological sort
        queue = [e for e, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            event = queue.pop(0)
            result.append(event)

            for caused in self.causal_graph.get(event, set()):
                in_degree[caused] -= 1
                if in_degree[caused] == 0:
                    queue.append(caused)

        return result

    def are_concurrent(self, event1: str, event2: str) -> bool:
        """
        Check if two events are concurrent.

        Args:
            event1: First event ID
            event2: Second event ID

        Returns:
            True if events are concurrent
        """
        if event1 not in self.events or event2 not in self.events:
            return False

        vc1 = self.events[event1]
        vc2 = self.events[event2]

        return VectorClock.concurrent(vc1, vc2)

    def get_concurrent_events(self, event_id: str) -> Set[str]:
        """
        Get all events concurrent with a given event.

        Args:
            event_id: Event to check

        Returns:
            Set of concurrent event IDs
        """
        concurrent = set()

        if event_id not in self.events:
            return concurrent

        for other_id in self.events:
            if other_id != event_id and self.are_concurrent(event_id, other_id):
                concurrent.add(other_id)

        return concurrent


class MatrixClock:
    """
    Matrix Clock - Extension of vector clocks for group communication.

    Each process maintains a matrix where:
    - Row i: process i's view of the vector clocks of all processes
    - M[i][j]: process i's knowledge of process j's logical clock
    """

    def __init__(self, process_id: str, process_list: List[str]):
        """
        Initialize matrix clock.

        Args:
            process_id: This process's ID
            process_list: List of all process IDs
        """
        self.process_id = process_id
        self.process_list = process_list
        self.process_index = process_list.index(process_id)
        self.n = len(process_list)

        # Initialize matrix
        self.matrix = [[0] * self.n for _ in range(self.n)]

    def tick(self):
        """Increment clock for local event."""
        self.matrix[self.process_index][self.process_index] += 1

    def send(self) -> List[List[int]]:
        """
        Prepare matrix clock for sending.

        Returns:
            Matrix clock to send
        """
        self.tick()
        return [row[:] for row in self.matrix]

    def receive(self, sender_id: str, received_matrix: List[List[int]]):
        """
        Update matrix clock on receive.

        Args:
            sender_id: ID of sending process
            received_matrix: Received matrix clock
        """
        sender_index = self.process_list.index(sender_id)

        # Update knowledge of sender's row
        self.matrix[sender_index] = received_matrix[sender_index][:]

        # Update own knowledge based on sender's knowledge
        for i in range(self.n):
            for j in range(self.n):
                if i != self.process_index:
                    self.matrix[i][j] = max(self.matrix[i][j], received_matrix[i][j])

        # Increment own clock
        self.tick()

    def get_min_known(self) -> List[int]:
        """
        Get minimum known vector clock across all processes.

        This represents the events known by ALL processes.

        Returns:
            Minimum vector clock
        """
        min_vector = [float('inf')] * self.n

        for j in range(self.n):
            for i in range(self.n):
                min_vector[j] = min(min_vector[j], self.matrix[i][j])

        return [int(v) if v != float('inf') else 0 for v in min_vector]


def example_usage():
    """Demonstrate vector clocks and logical time algorithms."""
    print("=" * 60)
    print("VECTOR CLOCKS AND LOGICAL TIME")
    print("=" * 60)

    # Example 1: Lamport Timestamps
    print("\n1. Lamport Timestamps:")
    print("-" * 40)

    # Three processes
    p1_lamport = LamportClock("P1")
    p2_lamport = LamportClock("P2")
    p3_lamport = LamportClock("P3")

    # Simulate events
    print("P1 local event:", p1_lamport.tick())
    msg1 = p1_lamport.send()
    print(f"P1 sends message with timestamp {msg1}")

    print("P2 receives:", p2_lamport.receive(msg1))
    print("P2 local event:", p2_lamport.tick())
    msg2 = p2_lamport.send()
    print(f"P2 sends message with timestamp {msg2}")

    print("P3 receives from P2:", p3_lamport.receive(msg2))
    print("P1 receives from P2:", p1_lamport.receive(msg2))

    print(f"\nFinal timestamps: P1={p1_lamport.get_time()}, "
          f"P2={p2_lamport.get_time()}, P3={p3_lamport.get_time()}")

    # Example 2: Vector Clocks
    print("\n2. Vector Clocks:")
    print("-" * 40)

    processes = ["P1", "P2", "P3"]
    p1_vector = VectorClock("P1", processes)
    p2_vector = VectorClock("P2", processes)
    p3_vector = VectorClock("P3", processes)

    # P1 events
    p1_e1 = p1_vector.tick()
    print(f"P1 event 1: {p1_e1}")

    msg_p1_p2 = p1_vector.send()
    print(f"P1 sends to P2: {msg_p1_p2}")

    # P2 receives from P1
    p2_e1 = p2_vector.receive(msg_p1_p2)
    print(f"P2 receives from P1: {p2_e1}")

    # P2 local event
    p2_e2 = p2_vector.tick()
    print(f"P2 event 2: {p2_e2}")

    # P3 independent event (concurrent)
    p3_e1 = p3_vector.tick()
    print(f"P3 event 1: {p3_e1}")

    # Check relationships
    print("\nCausality Analysis:")
    print(f"P1->P2 happens before P2 event 2: "
          f"{VectorClock.happens_before(msg_p1_p2, p2_e2)}")
    print(f"P3 event 1 concurrent with P2 event 2: "
          f"{VectorClock.concurrent(p3_e1, p2_e2)}")

    # Example 3: Version Vectors
    print("\n3. Version Vectors (Distributed Storage):")
    print("-" * 40)

    # Two replicas of a data item
    replica1 = VersionVector("R1")
    replica2 = VersionVector("R2")

    # Updates at different replicas
    v1 = replica1.increment()
    print(f"Replica 1 update: {v1}")

    v2 = replica1.increment()
    print(f"Replica 1 update: {v2}")

    # Concurrent update at replica 2
    replica2.update(v1)  # Sync with replica 1's first update
    v3 = replica2.increment()
    print(f"Replica 2 update: {v3}")

    # Check for conflicts
    print(f"\nVersion {v2} dominates {v1}: "
          f"{VersionVector._descends_from_static(v2, v1)}")
    print(f"Version {v2} conflicts with {v3}: "
          f"{replica1.conflicts_with(v3)}")

    # Example 4: Causality Tracking
    print("\n4. Causality Tracking:")
    print("-" * 40)

    tracker = CausalityTracker()

    # Add events with their vector clocks
    events = [
        ("E1", {"P1": 1, "P2": 0, "P3": 0}),
        ("E2", {"P1": 2, "P2": 0, "P3": 0}),
        ("E3", {"P1": 2, "P2": 1, "P3": 0}),
        ("E4", {"P1": 0, "P2": 0, "P3": 1}),  # Concurrent with E1, E2, E3
        ("E5", {"P1": 2, "P2": 1, "P3": 1}),  # After E3 and E4
    ]

    for event_id, vc in events:
        tracker.add_event(event_id, vc)

    print("Causal ordering:", tracker.get_causal_order())
    print(f"E4 concurrent with E1: {tracker.are_concurrent('E4', 'E1')}")
    print(f"E4 concurrent with E2: {tracker.are_concurrent('E4', 'E2')}")
    print(f"E1 concurrent with E2: {tracker.are_concurrent('E1', 'E2')}")

    # Example 5: Matrix Clocks
    print("\n5. Matrix Clocks (Group Communication):")
    print("-" * 40)

    processes = ["P1", "P2", "P3"]
    p1_matrix = MatrixClock("P1", processes)
    p2_matrix = MatrixClock("P2", processes)

    # P1 events
    p1_matrix.tick()
    p1_matrix.tick()
    msg_matrix = p1_matrix.send()

    print(f"P1's matrix after 2 events:")
    for row in msg_matrix:
        print(f"  {row}")

    # P2 receives
    p2_matrix.receive("P1", msg_matrix)

    print(f"\nP2's matrix after receiving from P1:")
    for row in p2_matrix.matrix:
        print(f"  {row}")

    print(f"\nMin known by all: {p2_matrix.get_min_known()}")

    # Example 6: Applications
    print("\n6. Applications of Vector Clocks:")
    print("-" * 40)

    applications = {
        "Distributed Databases": "Conflict detection in Dynamo, Riak",
        "Version Control": "Tracking concurrent edits",
        "Distributed Debugging": "Ordering events across processes",
        "Message Ordering": "Causal message delivery",
        "Snapshot Algorithms": "Consistent global snapshots",
        "CRDTs": "Conflict-free replicated data types"
    }

    for app, desc in applications.items():
        print(f"• {app}: {desc}")

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Lamport timestamps: Simple but can't detect concurrency")
    print("- Vector clocks: Detect causality and concurrency")
    print("- Version vectors: Track updates in distributed storage")
    print("- Matrix clocks: Track group knowledge")
    print("- Trade-off: More information vs. space overhead")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()