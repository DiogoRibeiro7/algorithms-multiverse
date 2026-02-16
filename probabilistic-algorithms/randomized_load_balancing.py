"""
Randomized Load Balancing Algorithms

Implementation of various randomized algorithms for load balancing in distributed
systems, including power of two choices, consistent hashing with virtual nodes,
and weighted random selection.

Key Algorithms:
- Random Assignment
- Round Robin with Randomization
- Power of Two Choices
- Weighted Random Selection
- Consistent Hashing Load Balancer
- Least Connections with Randomization
- Adaptive Load Balancing

Author: Claude
Date: January 2026
"""

import random
import numpy as np
from typing import List, Dict, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
import hashlib
import bisect
import time
from collections import defaultdict, deque
import heapq


@dataclass
class Server:
    """Represents a server in the load balancing system."""
    id: str
    capacity: int = 100
    current_load: int = 0
    weight: float = 1.0
    response_times: deque = field(default_factory=lambda: deque(maxlen=100))
    total_requests: int = 0
    failed_requests: int = 0

    @property
    def load_percentage(self) -> float:
        """Get current load as percentage of capacity."""
        return (self.current_load / self.capacity) * 100 if self.capacity > 0 else 0

    @property
    def avg_response_time(self) -> float:
        """Get average response time."""
        return np.mean(self.response_times) if self.response_times else 0

    @property
    def success_rate(self) -> float:
        """Get request success rate."""
        if self.total_requests == 0:
            return 1.0
        return 1.0 - (self.failed_requests / self.total_requests)

    def can_handle_request(self, request_size: int = 1) -> bool:
        """Check if server can handle a request."""
        return self.current_load + request_size <= self.capacity

    def add_request(self, request_size: int = 1, response_time: float = 0.0) -> bool:
        """Add a request to the server."""
        if self.can_handle_request(request_size):
            self.current_load += request_size
            self.total_requests += 1
            if response_time > 0:
                self.response_times.append(response_time)
            return True
        self.failed_requests += 1
        return False

    def remove_request(self, request_size: int = 1):
        """Remove a request from the server."""
        self.current_load = max(0, self.current_load - request_size)


class RandomLoadBalancer:
    """
    Simple random load balancer.

    Randomly selects a server for each request.
    Expected max load: O(log n / log log n) with high probability.
    """

    def __init__(self, servers: List[Server]):
        """Initialize with list of servers."""
        self.servers = servers
        self.request_count = 0

    def select_server(self, request_size: int = 1) -> Optional[Server]:
        """Select a random server."""
        self.request_count += 1
        available_servers = [s for s in self.servers if s.can_handle_request(request_size)]

        if not available_servers:
            return None

        return random.choice(available_servers)

    def get_load_distribution(self) -> Dict[str, float]:
        """Get current load distribution."""
        return {s.id: s.load_percentage for s in self.servers}


class PowerOfTwoChoices:
    """
    Power of Two Choices load balancer.

    Samples two random servers and picks the less loaded one.
    Expected max load: O(log log n) with high probability.
    """

    def __init__(self, servers: List[Server], d: int = 2):
        """
        Initialize load balancer.

        Args:
            servers: List of servers
            d: Number of choices (power of d choices)
        """
        self.servers = servers
        self.d = d
        self.request_count = 0

    def select_server(self, request_size: int = 1) -> Optional[Server]:
        """Select server using power of d choices."""
        self.request_count += 1

        # Sample d random servers
        sample_size = min(self.d, len(self.servers))
        sampled = random.sample(self.servers, sample_size)

        # Filter servers that can handle the request
        available = [s for s in sampled if s.can_handle_request(request_size)]

        if not available:
            # Fallback: check all servers
            available = [s for s in self.servers if s.can_handle_request(request_size)]
            if not available:
                return None

        # Select the least loaded server
        return min(available, key=lambda s: s.current_load)

    def select_server_weighted(self, request_size: int = 1) -> Optional[Server]:
        """Select server with weighted consideration."""
        sampled = random.sample(self.servers, min(self.d, len(self.servers)))
        available = [s for s in sampled if s.can_handle_request(request_size)]

        if not available:
            return None

        # Consider both load and server weight
        return min(available, key=lambda s: s.current_load / s.weight)


class WeightedRandomLoadBalancer:
    """
    Weighted random selection load balancer.

    Servers are selected with probability proportional to their weights.
    """

    def __init__(self, servers: List[Server]):
        """Initialize with weighted servers."""
        self.servers = servers
        self.update_weights()

    def update_weights(self):
        """Update cumulative weights for efficient sampling."""
        self.weights = [s.weight for s in self.servers]
        self.cumulative_weights = []
        cumsum = 0
        for w in self.weights:
            cumsum += w
            self.cumulative_weights.append(cumsum)
        self.total_weight = cumsum

    def select_server(self, request_size: int = 1) -> Optional[Server]:
        """Select server based on weights."""
        if not self.servers or self.total_weight == 0:
            return None

        # Binary search for weighted random selection
        rand_val = random.random() * self.total_weight
        idx = bisect.bisect_left(self.cumulative_weights, rand_val)
        idx = min(idx, len(self.servers) - 1)

        server = self.servers[idx]
        if server.can_handle_request(request_size):
            return server

        # Try other servers if selected one is full
        for s in self.servers:
            if s.can_handle_request(request_size):
                return s

        return None

    def adjust_weights_by_performance(self):
        """Dynamically adjust weights based on server performance."""
        for server in self.servers:
            # Adjust weight based on success rate and response time
            performance_score = server.success_rate
            if server.avg_response_time > 0:
                # Normalize response time (lower is better)
                performance_score *= (1.0 / (1 + server.avg_response_time))

            # Update weight (keep minimum weight of 0.1)
            server.weight = max(0.1, server.weight * (0.9 + 0.2 * performance_score))

        self.update_weights()


class ConsistentHashingLoadBalancer:
    """
    Consistent hashing with virtual nodes for load balancing.

    Minimizes remapping when servers are added/removed.
    """

    def __init__(self, servers: List[Server], virtual_nodes: int = 150):
        """
        Initialize consistent hashing.

        Args:
            servers: List of servers
            virtual_nodes: Number of virtual nodes per server
        """
        self.servers = {s.id: s for s in servers}
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.sorted_keys = []
        self._build_ring()

    def _hash(self, key: str) -> int:
        """Generate hash for a key."""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def _build_ring(self):
        """Build the consistent hash ring."""
        self.ring = {}
        for server_id, server in self.servers.items():
            for i in range(self.virtual_nodes):
                virtual_key = f"{server_id}:{i}"
                hash_value = self._hash(virtual_key)
                self.ring[hash_value] = server

        self.sorted_keys = sorted(self.ring.keys())

    def select_server(self, request_key: str) -> Optional[Server]:
        """Select server for a given request key."""
        if not self.ring:
            return None

        hash_value = self._hash(request_key)

        # Find the first server clockwise from the hash
        idx = bisect.bisect_right(self.sorted_keys, hash_value)
        if idx == len(self.sorted_keys):
            idx = 0

        server = self.ring[self.sorted_keys[idx]]

        # If server is overloaded, try the next one
        attempts = 0
        while not server.can_handle_request() and attempts < len(self.sorted_keys):
            idx = (idx + 1) % len(self.sorted_keys)
            server = self.ring[self.sorted_keys[idx]]
            attempts += 1

        return server if server.can_handle_request() else None

    def add_server(self, server: Server):
        """Add a new server to the ring."""
        self.servers[server.id] = server

        # Add virtual nodes for the new server
        for i in range(self.virtual_nodes):
            virtual_key = f"{server.id}:{i}"
            hash_value = self._hash(virtual_key)
            self.ring[hash_value] = server
            bisect.insort(self.sorted_keys, hash_value)

    def remove_server(self, server_id: str):
        """Remove a server from the ring."""
        if server_id not in self.servers:
            return

        # Remove virtual nodes
        for i in range(self.virtual_nodes):
            virtual_key = f"{server_id}:{i}"
            hash_value = self._hash(virtual_key)
            if hash_value in self.ring:
                del self.ring[hash_value]
                self.sorted_keys.remove(hash_value)

        del self.servers[server_id]


class LeastConnectionsRandomized:
    """
    Least connections with randomization.

    Combines least connections with randomization to avoid herding.
    """

    def __init__(self, servers: List[Server], sample_size: int = 3):
        """
        Initialize load balancer.

        Args:
            servers: List of servers
            sample_size: Number of servers to sample
        """
        self.servers = servers
        self.sample_size = sample_size

    def select_server(self, request_size: int = 1) -> Optional[Server]:
        """Select server with least connections from random sample."""
        sample = random.sample(self.servers,
                              min(self.sample_size, len(self.servers)))

        available = [s for s in sample if s.can_handle_request(request_size)]

        if not available:
            # Fallback to all servers
            available = [s for s in self.servers if s.can_handle_request(request_size)]

        if not available:
            return None

        # Select server with least current load
        return min(available, key=lambda s: s.current_load)


class AdaptiveLoadBalancer:
    """
    Adaptive load balancer that switches strategies based on load patterns.
    """

    def __init__(self, servers: List[Server]):
        """Initialize adaptive load balancer."""
        self.servers = servers
        self.strategies = {
            'random': RandomLoadBalancer(servers),
            'power_of_two': PowerOfTwoChoices(servers),
            'weighted': WeightedRandomLoadBalancer(servers),
            'least_conn_random': LeastConnectionsRandomized(servers)
        }
        self.current_strategy = 'power_of_two'
        self.performance_history = defaultdict(list)
        self.request_count = 0
        self.evaluation_period = 100

    def select_server(self, request_size: int = 1) -> Optional[Server]:
        """Select server using current strategy."""
        self.request_count += 1

        # Periodically evaluate and switch strategies
        if self.request_count % self.evaluation_period == 0:
            self._evaluate_and_switch()

        return self.strategies[self.current_strategy].select_server(request_size)

    def _evaluate_and_switch(self):
        """Evaluate performance and switch strategy if needed."""
        # Calculate current load imbalance
        loads = [s.current_load for s in self.servers]
        if not loads:
            return

        load_variance = np.var(loads)
        max_load = max(loads)
        avg_load = np.mean(loads)

        # Simple heuristic for strategy selection
        if load_variance > avg_load * 2:
            # High imbalance - use power of two
            self.current_strategy = 'power_of_two'
        elif max_load > avg_load * 1.5:
            # Moderate imbalance - use least connections
            self.current_strategy = 'least_conn_random'
        else:
            # Low imbalance - random is sufficient
            self.current_strategy = 'random'

        self.performance_history[self.current_strategy].append({
            'variance': load_variance,
            'max_load': max_load,
            'avg_load': avg_load
        })


class JoinShortestQueue:
    """
    Join-the-Shortest-Queue (JSQ) with randomization.

    Optimal for minimizing average wait time.
    """

    def __init__(self, servers: List[Server]):
        """Initialize JSQ load balancer."""
        self.servers = servers
        # Use heap for efficient shortest queue operations
        self.server_heap = []
        self._rebuild_heap()

    def _rebuild_heap(self):
        """Rebuild the heap structure."""
        self.server_heap = [(s.current_load, random.random(), s)
                           for s in self.servers]
        heapq.heapify(self.server_heap)

    def select_server(self, request_size: int = 1) -> Optional[Server]:
        """Select server with shortest queue."""
        # Rebuild heap periodically for accuracy
        if random.random() < 0.1:  # 10% chance
            self._rebuild_heap()

        # Try servers in order of increasing load
        temp_removed = []
        selected = None

        while self.server_heap and selected is None:
            load, rand, server = heapq.heappop(self.server_heap)

            if server.can_handle_request(request_size):
                selected = server
                # Update and reinsert
                heapq.heappush(self.server_heap,
                              (server.current_load + request_size, random.random(), server))
            else:
                temp_removed.append((load, rand, server))

        # Reinsert servers that couldn't handle request
        for item in temp_removed:
            heapq.heappush(self.server_heap, item)

        return selected


# Simulation and testing functions
def simulate_load_balancing(balancer, num_requests: int = 10000,
                           arrival_rate: float = 100.0) -> Dict[str, Any]:
    """
    Simulate load balancing with Poisson arrivals.

    Args:
        balancer: Load balancer instance
        num_requests: Number of requests to simulate
        arrival_rate: Average arrival rate (requests per time unit)

    Returns:
        Simulation statistics
    """
    current_time = 0
    completed_requests = []
    rejected_requests = 0

    for i in range(num_requests):
        # Poisson arrival times
        inter_arrival = np.random.exponential(1 / arrival_rate)
        current_time += inter_arrival

        # Random request size (1-5 units)
        request_size = np.random.randint(1, 6)

        # Select server
        server = balancer.select_server(request_size)

        if server:
            # Simulate processing time
            processing_time = np.random.exponential(0.1 * request_size)
            server.add_request(request_size, processing_time)

            completed_requests.append({
                'server': server.id,
                'arrival_time': current_time,
                'processing_time': processing_time,
                'size': request_size
            })

            # Simulate request completion (simplified)
            if random.random() < 0.3:  # 30% chance to complete
                server.remove_request(request_size)
        else:
            rejected_requests += 1

    # Calculate statistics
    if hasattr(balancer, 'servers'):
        servers = balancer.servers
    elif hasattr(balancer, 'servers') and isinstance(balancer.servers, dict):
        servers = list(balancer.servers.values())
    else:
        servers = []

    loads = [s.current_load for s in servers]

    stats = {
        'total_requests': num_requests,
        'completed_requests': len(completed_requests),
        'rejected_requests': rejected_requests,
        'rejection_rate': rejected_requests / num_requests,
        'avg_load': np.mean(loads) if loads else 0,
        'max_load': max(loads) if loads else 0,
        'min_load': min(loads) if loads else 0,
        'load_variance': np.var(loads) if loads else 0,
        'load_std': np.std(loads) if loads else 0,
        'load_distribution': {s.id: s.current_load for s in servers}
    }

    return stats


# Example usage and demonstrations
def example_power_of_choices():
    """Demonstrate power of two choices vs random selection."""
    print("=== Power of Two Choices vs Random Selection ===\n")

    # Create servers
    num_servers = 10
    servers_random = [Server(f"server_{i}", capacity=100) for i in range(num_servers)]
    servers_power2 = [Server(f"server_{i}", capacity=100) for i in range(num_servers)]

    # Create load balancers
    random_lb = RandomLoadBalancer(servers_random)
    power2_lb = PowerOfTwoChoices(servers_power2, d=2)

    # Run simulation
    num_requests = 1000

    print("Random Load Balancer:")
    stats_random = simulate_load_balancing(random_lb, num_requests)
    print(f"  Max load: {stats_random['max_load']}")
    print(f"  Load variance: {stats_random['load_variance']:.2f}")
    print(f"  Rejection rate: {stats_random['rejection_rate']:.2%}")

    print("\nPower of Two Choices:")
    stats_power2 = simulate_load_balancing(power2_lb, num_requests)
    print(f"  Max load: {stats_power2['max_load']}")
    print(f"  Load variance: {stats_power2['load_variance']:.2f}")
    print(f"  Rejection rate: {stats_power2['rejection_rate']:.2%}")

    print(f"\nImprovement in max load: {(stats_random['max_load'] - stats_power2['max_load']) / stats_random['max_load'] * 100:.1f}%")
    print(f"Improvement in variance: {(stats_random['load_variance'] - stats_power2['load_variance']) / stats_random['load_variance'] * 100:.1f}%")


def example_consistent_hashing():
    """Demonstrate consistent hashing with server additions/removals."""
    print("=== Consistent Hashing Load Balancer ===\n")

    # Create initial servers
    servers = [Server(f"server_{i}", capacity=100) for i in range(5)]
    ch_lb = ConsistentHashingLoadBalancer(servers, virtual_nodes=50)

    # Generate requests
    requests = [f"request_{i}" for i in range(100)]
    initial_mapping = {}

    print("Initial request distribution:")
    for req in requests:
        server = ch_lb.select_server(req)
        if server:
            initial_mapping[req] = server.id
            server.add_request()

    server_counts = defaultdict(int)
    for server_id in initial_mapping.values():
        server_counts[server_id] += 1

    for server_id, count in sorted(server_counts.items()):
        print(f"  {server_id}: {count} requests")

    # Add a new server
    print("\nAdding server_5...")
    new_server = Server("server_5", capacity=100)
    ch_lb.add_server(new_server)

    # Check remapping
    remapped = 0
    new_mapping = {}
    for req in requests:
        server = ch_lb.select_server(req)
        if server:
            new_mapping[req] = server.id
            if initial_mapping.get(req) != server.id:
                remapped += 1

    print(f"Requests remapped: {remapped}/{len(requests)} ({remapped/len(requests)*100:.1f}%)")
    print(f"Expected remapping: ~{100/6:.1f}% (1/n for n servers)")


def example_weighted_selection():
    """Demonstrate weighted random selection."""
    print("=== Weighted Random Load Balancing ===\n")

    # Create servers with different capacities/weights
    servers = [
        Server("small_server", capacity=50, weight=0.5),
        Server("medium_server", capacity=100, weight=1.0),
        Server("large_server", capacity=200, weight=2.0),
    ]

    weighted_lb = WeightedRandomLoadBalancer(servers)

    # Run simulation
    num_requests = 1000
    server_selections = defaultdict(int)

    for _ in range(num_requests):
        server = weighted_lb.select_server()
        if server:
            server_selections[server.id] += 1
            server.add_request()
            # Simulate some completions
            if random.random() < 0.3:
                server.remove_request()

    print("Server selection distribution:")
    total_weight = sum(s.weight for s in servers)
    for server in servers:
        actual = server_selections[server.id]
        expected = (server.weight / total_weight) * num_requests
        print(f"  {server.id}:")
        print(f"    Weight: {server.weight}")
        print(f"    Selected: {actual} times")
        print(f"    Expected: {expected:.0f} times")
        print(f"    Deviation: {abs(actual - expected) / expected * 100:.1f}%")


def example_adaptive_strategy():
    """Demonstrate adaptive load balancing."""
    print("=== Adaptive Load Balancing ===\n")

    # Create servers
    servers = [Server(f"server_{i}", capacity=100) for i in range(10)]
    adaptive_lb = AdaptiveLoadBalancer(servers)

    # Simulate different load patterns
    patterns = [
        ("Uniform Load", lambda: random.randint(1, 3)),
        ("Heavy Load", lambda: random.randint(5, 10)),
        ("Bursty Load", lambda: random.randint(1, 20) if random.random() < 0.2 else 1),
    ]

    for pattern_name, size_generator in patterns:
        print(f"\n{pattern_name}:")

        # Reset servers
        for server in servers:
            server.current_load = 0

        # Run requests
        for i in range(500):
            request_size = size_generator()
            server = adaptive_lb.select_server(request_size)
            if server:
                server.add_request(request_size)
                # Simulate completions
                if random.random() < 0.4:
                    server.remove_request(min(request_size, server.current_load))

        # Report results
        loads = [s.current_load for s in servers]
        print(f"  Strategy used: {adaptive_lb.current_strategy}")
        print(f"  Load variance: {np.var(loads):.2f}")
        print(f"  Max load: {max(loads)}")
        print(f"  Load balance factor: {max(loads) / (sum(loads) / len(loads)):.2f}")


def example_join_shortest_queue():
    """Demonstrate join-the-shortest-queue."""
    print("=== Join-the-Shortest-Queue ===\n")

    servers = [Server(f"server_{i}", capacity=100) for i in range(8)]
    jsq_lb = JoinShortestQueue(servers)

    # Compare with random
    servers_random = [Server(f"server_{i}", capacity=100) for i in range(8)]
    random_lb = RandomLoadBalancer(servers_random)

    num_requests = 2000

    # JSQ simulation
    for _ in range(num_requests):
        server = jsq_lb.select_server(random.randint(1, 5))
        if server:
            server.add_request()
            if random.random() < 0.3:
                server.remove_request()

    # Random simulation
    for _ in range(num_requests):
        server = random_lb.select_server(random.randint(1, 5))
        if server:
            server.add_request()
            if random.random() < 0.3:
                server.remove_request()

    # Compare results
    jsq_loads = sorted([s.current_load for s in servers])
    random_loads = sorted([s.current_load for s in servers_random])

    print("Load distribution (sorted):")
    print(f"  JSQ:    {jsq_loads}")
    print(f"  Random: {random_loads}")

    print(f"\nJSQ Metrics:")
    print(f"  Max load: {max(jsq_loads)}")
    print(f"  Load variance: {np.var(jsq_loads):.2f}")

    print(f"\nRandom Metrics:")
    print(f"  Max load: {max(random_loads)}")
    print(f"  Load variance: {np.var(random_loads):.2f}")


def analyze_theoretical_bounds():
    """Analyze theoretical bounds for different algorithms."""
    print("=== Theoretical Analysis ===\n")

    n_values = [10, 50, 100, 500, 1000]
    m = 10000  # Number of balls (requests)

    print(f"Throwing {m} balls into n bins:\n")
    print(f"{'n':<10} {'Random (expected max)':<25} {'Power-of-2 (expected max)':<25}")
    print("-" * 60)

    for n in n_values:
        # Random allocation expected max load
        random_max = m/n + np.sqrt(2 * m/n * np.log(n))

        # Power of two choices expected max load
        power2_max = m/n + np.log(np.log(n)) / np.log(2)

        print(f"{n:<10} {random_max:<25.2f} {power2_max:<25.2f}")

    print("\nNote: These are theoretical approximations.")
    print("Power of two choices achieves exponential improvement in max load!")


if __name__ == "__main__":
    # Run examples
    example_power_of_choices()
    print("\n" + "=" * 60 + "\n")

    example_consistent_hashing()
    print("\n" + "=" * 60 + "\n")

    example_weighted_selection()
    print("\n" + "=" * 60 + "\n")

    example_adaptive_strategy()
    print("\n" + "=" * 60 + "\n")

    example_join_shortest_queue()
    print("\n" + "=" * 60 + "\n")

    analyze_theoretical_bounds()

    print("\n" + "=" * 60)
    print("Key Insights:")
    print("=" * 60)
    print("""
1. Power of Two Choices provides exponential improvement over random
   selection with minimal overhead (just one extra sample).

2. Consistent hashing minimizes disruption when servers are added/removed,
   crucial for distributed caching and storage systems.

3. Weighted selection allows heterogeneous server capacities to be
   utilized effectively.

4. Adaptive strategies can respond to changing load patterns, switching
   between algorithms based on current conditions.

5. Join-Shortest-Queue is optimal for minimizing average wait time
   but requires global knowledge of queue lengths.

6. Randomization helps avoid thundering herd problems and provides
   good expected performance with simple implementations.

7. Real-world systems often combine multiple techniques:
   - Consistent hashing for session affinity
   - Power of two for load distribution
   - Weights for heterogeneous resources
    """)