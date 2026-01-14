# Distributed Algorithms

A comprehensive collection of fundamental distributed systems algorithms including consensus protocols, synchronization mechanisms, failure detection, and coordination algorithms.

## 📚 Table of Contents

- [Overview](#overview)
- [Implemented Algorithms](#implemented-algorithms)
- [Installation](#installation)
- [Algorithm Details](#algorithm-details)
- [Usage Examples](#usage-examples)
- [Performance & Trade-offs](#performance--trade-offs)
- [Real-World Applications](#real-world-applications)
- [References](#references)

## 🎯 Overview

Distributed algorithms are designed to coordinate multiple nodes in a network to achieve common goals despite challenges like network delays, failures, and lack of global state. These algorithms form the foundation of modern distributed systems.

### Key Challenges Addressed

- **Consensus**: Agreement among distributed nodes
- **Synchronization**: Coordinating actions across time
- **Fault Tolerance**: Operating despite node/network failures
- **Consistency**: Maintaining coherent state across nodes
- **Scalability**: Efficient operation with many nodes

## 📊 Implemented Algorithms

### 1. Consensus Algorithms (`raft_consensus.py`)

| Algorithm | Type | Fault Tolerance | Consistency | Use Case |
|-----------|------|-----------------|-------------|----------|
| **Raft Consensus** | Leader-based | Crash failures | Strong | Distributed databases |
| **Leader Election** | Voting | f < n/2 | Eventually consistent | Cluster coordination |
| **Log Replication** | State machine | Network partitions | Linearizable | Replicated state |

### 2. Logical Time & Causality (`vector_clocks.py`)

| Algorithm | Purpose | Space | Comparison Time | Properties |
|-----------|---------|-------|-----------------|------------|
| **Lamport Timestamps** | Total ordering | O(1) | O(1) | Partial causality |
| **Vector Clocks** | Causal ordering | O(n) | O(n) | Full causality |
| **Version Vectors** | Conflict detection | O(n) | O(n) | Sibling detection |
| **Matrix Clocks** | Global knowledge | O(n²) | O(n²) | Complete info |
| **Interval Tree Clocks** | Dynamic nodes | O(active) | O(log n) | Fork-join |

### 3. Gossip Protocols (`gossip_protocols.py`)

| Protocol | Type | Convergence | Message Load | Reliability |
|----------|------|-------------|--------------|-------------|
| **Push Gossip** | Epidemic | O(log n) | High initially | Good |
| **Pull Gossip** | Anti-entropy | O(log n) | Steady | Better |
| **Push-Pull** | Hybrid | O(log n) | Balanced | Best |
| **SWIM Protocol** | Membership | O(1) per node | Constant | High |
| **Gossip Aggregation** | Computation | O(log n) | Low | Eventual |

### 4. Byzantine Fault Tolerance (`byzantine_fault_tolerance.py`)

| Algorithm | Fault Model | Requirement | Rounds | Messages | Use Case |
|-----------|-------------|-------------|---------|----------|----------|
| **Byzantine Generals** | Byzantine | n > 3f | f+1 | Exponential | Theory |
| **Byzantine Agreement** | Byzantine | n > 3f | 3-4 | O(n²) | Agreement |
| **PBFT (Simplified)** | Byzantine | n ≥ 3f+1 | 3 phases | O(n²) | Blockchains |
| **Failure Detection** | Byzantine | - | Continuous | - | Monitoring |

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/algorithms-multiverse.git
cd algorithms-multiverse/distributed-algorithms

# No external dependencies required for basic functionality
# For enhanced features:
pip install numpy  # For matrix operations in vector clocks
```

## 💡 Algorithm Details

### Raft Consensus Algorithm

Raft provides a complete solution for replicated state machines with understandable semantics.

**Key Components:**
- **Leader Election**: Uses randomized timeouts to elect leaders
- **Log Replication**: Leaders append entries and replicate to followers
- **Safety**: Ensures linearizability and prevents split-brain

**Properties:**
- Strong consistency (linearizable)
- Availability with majority (f < n/2)
- Network partition tolerance
- Understandable (vs. Paxos)

### Vector Clocks & Logical Time

Logical time algorithms order events in distributed systems without synchronized physical clocks.

**Lamport Timestamps:**
- Simple counter-based ordering
- Preserves happens-before relation
- Cannot detect concurrent events

**Vector Clocks:**
- Array of logical clocks
- Detects causality and concurrency
- Used in distributed databases

### Gossip Protocols

Epidemic-style information dissemination with probabilistic guarantees.

**Properties:**
- Logarithmic convergence time
- Resilient to failures
- Eventually consistent
- Scalable to large networks

### Byzantine Fault Tolerance

Handles arbitrary (malicious) failures where nodes can lie or send conflicting messages.

**Key Insights:**
- Requires n ≥ 3f+1 nodes for f Byzantine failures
- Impossible with n ≤ 3f (proven impossibility result)
- Trade-off between fault tolerance and performance

## 💻 Usage Examples

### Example 1: Raft Consensus

```python
from raft_consensus import RaftCluster

# Create a 5-node Raft cluster
cluster = RaftCluster(num_nodes=5)

# Simulate leader election
for step in range(3):
    cluster.simulate_step()
    leader = cluster.get_leader()
    if leader:
        print(f"Leader elected: {leader}")
        break

# Submit commands to the cluster
commands = ["SET x 1", "SET y 2", "INCREMENT z"]
for cmd in commands:
    if cluster.submit_command(cmd):
        print(f"Command '{cmd}' accepted")

# Check cluster state
state = cluster.get_state_summary()
print(f"Cluster state: {state}")
```

### Example 2: Vector Clocks for Causality

```python
from vector_clocks import VectorClock, CausalityTracker

# Create vector clocks for 3 nodes
vc1 = VectorClock(node_id="A", num_nodes=3)
vc2 = VectorClock(node_id="B", num_nodes=3)
vc3 = VectorClock(node_id="C", num_nodes=3)

# Simulate events
vc1.increment()  # A performs local operation
msg1 = vc1.prepare_send()  # A sends to B

vc2.receive(msg1)  # B receives from A
vc2.increment()  # B performs local operation
msg2 = vc2.prepare_send()  # B sends to C

vc3.receive(msg2)  # C receives from B

# Check causality
print(f"A happened before C: {vc1.happened_before(vc3)}")
print(f"A concurrent with C: {vc1.is_concurrent(vc3)}")
```

### Example 3: Gossip Protocol for Information Spread

```python
from gossip_protocols import GossipProtocol

# Create gossip network
gossip = GossipProtocol(num_nodes=100, fanout=3)

# Start rumor from node 0
gossip.start_rumor(node_id=0, rumor="System update available")

# Simulate gossip rounds
rounds = 0
while not gossip.is_converged():
    gossip.round()
    rounds += 1
    infected = gossip.get_infected_count()
    print(f"Round {rounds}: {infected}/100 nodes informed")

print(f"Converged in {rounds} rounds")
```

### Example 4: Byzantine Agreement

```python
from byzantine_fault_tolerance import SimpleByzantineAgreement

# Create system with 7 nodes, tolerating 2 Byzantine failures
agreement = SimpleByzantineAgreement(n_nodes=7, f_byzantine=2)

# Proposer broadcasts value
decisions = agreement.broadcast_reliable(
    proposer_id="node_0",
    value="COMMIT_TRANSACTION"
)

# Check if honest nodes agreed
honest_decisions = [d for d in decisions.values() if d is not None]
if len(set(honest_decisions)) == 1:
    print(f"Consensus reached: {honest_decisions[0]}")
```

## 📈 Performance & Trade-offs

### Consensus Algorithm Comparison

| Algorithm | Fault Model | Performance | Complexity | Best For |
|-----------|------------|-------------|------------|----------|
| **Raft** | Crash | Fast | Simple | General purpose |
| **Paxos** | Crash | Fast | Complex | Proven systems |
| **PBFT** | Byzantine | Slower | Moderate | Blockchains |
| **HotStuff** | Byzantine | Linear | Simple | Modern blockchains |

### Time & Message Complexity

| Algorithm | Time Complexity | Message Complexity | Space per Node |
|-----------|----------------|-------------------|----------------|
| Raft | O(1) normal, O(n) election | O(n) per entry | O(log entries) |
| Vector Clocks | O(1) update | O(n) per message | O(n) |
| Gossip | O(log n) convergence | O(n log n) total | O(1) or O(n) |
| PBFT | O(1) normal case | O(n²) | O(log entries) |

### CAP Theorem Trade-offs

Different algorithms make different trade-offs:

| Algorithm | Consistency | Availability | Partition Tolerance |
|-----------|-------------|--------------|-------------------|
| Raft | Strong | Majority | Yes |
| Gossip | Eventual | High | Yes |
| PBFT | Strong | 2f+1 nodes | Limited |
| Vector Clocks | Causal | High | Yes |

## 🌍 Real-World Applications

### Production Systems Using These Algorithms

#### **Raft Consensus**
- **etcd**: Distributed key-value store (Kubernetes)
- **Consul**: Service mesh and discovery
- **CockroachDB**: Distributed SQL database
- **TiKV**: Distributed transactional key-value database

#### **Vector Clocks**
- **Amazon DynamoDB**: Conflict resolution
- **Riak**: Distributed database
- **Voldemort**: LinkedIn's distributed store
- **Apache Cassandra**: Last-write-wins with timestamps

#### **Gossip Protocols**
- **Apache Cassandra**: Cluster membership and failure detection
- **Consul**: Health checking and service discovery
- **SWIM**: Membership protocol used by Serf, Memberlist
- **Bitcoin**: Transaction and block propagation

#### **Byzantine Fault Tolerance**
- **Hyperledger Fabric**: Permissioned blockchain
- **Tendermint**: Cosmos blockchain consensus
- **LibraBFT/DiemBFT**: Facebook's blockchain
- **NEO**: Delegated Byzantine Fault Tolerance

## 🔬 Advanced Topics

### Hybrid Approaches

```python
# Example: Combining Raft with Gossip for large clusters

class HybridConsensus:
    """
    Use Raft for core consensus group,
    Gossip for disseminating decisions to followers.
    """
    def __init__(self, core_size=5, total_nodes=1000):
        self.raft_core = RaftCluster(core_size)
        self.gossip_network = GossipProtocol(total_nodes)

    def propose(self, value):
        # Core group reaches consensus
        if self.raft_core.submit_command(value):
            # Disseminate via gossip
            leader = self.raft_core.get_leader()
            self.gossip_network.start_rumor(
                node_id=leader,
                rumor={"type": "decision", "value": value}
            )
```

### Dynamic Membership

```python
# Example: Raft configuration changes

def add_node_to_cluster(cluster, new_node_id):
    """
    Safe configuration change in Raft:
    1. Append configuration entry to log
    2. Replicate to majority of OLD configuration
    3. Replicate to majority of NEW configuration
    4. Commit when both majorities accept
    """
    old_config = cluster.get_configuration()
    new_config = old_config + [new_node_id]

    # Joint consensus phase
    joint_entry = ConfigChange(old_config, new_config)
    cluster.submit_command(joint_entry)

    # Final configuration
    final_entry = ConfigChange(new_config)
    cluster.submit_command(final_entry)
```

## 📚 References

### Foundational Papers

**Consensus:**
- Lamport (1998) - "The Part-Time Parliament" (Paxos)
- Ongaro & Ousterhout (2014) - "In Search of an Understandable Consensus Algorithm" (Raft)
- Castro & Liskov (1999) - "Practical Byzantine Fault Tolerance"

**Logical Time:**
- Lamport (1978) - "Time, Clocks, and the Ordering of Events"
- Mattern (1989) - "Virtual Time and Global States"
- Fidge (1991) - "Logical Time in Distributed Computing Systems"

**Gossip Protocols:**
- Demers et al. (1987) - "Epidemic Algorithms for Replicated Database Maintenance"
- Das et al. (2002) - "SWIM: Scalable Weakly-consistent Infection-style Process Group Membership"

**Byzantine Agreement:**
- Lamport, Shostak, Pease (1982) - "The Byzantine Generals Problem"
- Fischer, Lynch, Paterson (1985) - "Impossibility of Distributed Consensus with One Faulty Process"

### Books
- "Distributed Systems" by van Steen & Tanenbaum
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "Introduction to Reliable and Secure Distributed Programming" by Cachin, Guerraoui, Rodrigues

## 🔍 Debugging Distributed Algorithms

### Common Issues and Solutions

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Split Brain** | Multiple leaders | Use majority quorum |
| **Livelock** | No progress | Add randomization |
| **Causality Violation** | Wrong event order | Use vector clocks |
| **Byzantine Behavior** | Inconsistent state | Add message authentication |
| **Network Partition** | Cluster split | Design for partition tolerance |

### Testing Strategies

```python
# Example: Testing distributed algorithm resilience

def chaos_test(algorithm, failure_rate=0.1):
    """Inject random failures to test resilience."""
    for round in range(100):
        # Random node failures
        if random.random() < failure_rate:
            failed_node = random.choice(algorithm.nodes)
            algorithm.fail_node(failed_node)

        # Random message delays
        if random.random() < failure_rate:
            algorithm.delay_messages(rounds=random.randint(1, 5))

        # Random network partitions
        if random.random() < failure_rate / 2:
            partition = random.sample(
                algorithm.nodes,
                len(algorithm.nodes) // 2
            )
            algorithm.partition_network(partition)

        # Check invariants
        assert algorithm.check_safety()
        assert algorithm.check_liveness()
```

## ⚠️ Important Considerations

1. **Network Assumptions**: Most algorithms assume reliable message delivery (eventually)
2. **Timing Assumptions**: Synchronous vs. asynchronous vs. partially synchronous
3. **Failure Models**: Crash vs. Byzantine affects algorithm choice
4. **Scalability Limits**: Consider message complexity for large clusters
5. **Consistency Trade-offs**: Strong consistency impacts availability

## 🤝 Contributing

Areas for improvement and expansion:
- Additional consensus algorithms (Multi-Paxos, Viewstamped Replication)
- Advanced BFT protocols (HotStuff, Tendermint)
- Distributed transactions (2PC, 3PC, Saga)
- Distributed locking algorithms
- Performance benchmarks and comparisons

---

**Part of the Algorithms Multiverse** - A comprehensive collection of algorithms across multiple domains.

**Last Updated**: January 2026