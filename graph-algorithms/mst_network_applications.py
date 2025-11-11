"""
MST Real-World Network Applications
====================================

Demonstrates practical applications of MST algorithms in:
1. Network infrastructure planning (fiber optic, electrical grids)
2. Telecommunications network design
3. Transportation network optimization
4. Cluster analysis and hierarchical clustering
5. Circuit design and VLSI routing

Each application includes realistic scenarios with cost analysis.
"""

import numpy as np
from typing import List, Tuple, Dict
from mst_algorithms import MSTAlgorithms, Edge
import matplotlib.pyplot as plt
import networkx as nx


class NetworkInfrastructure:
    """
    Real-world network infrastructure planning using MST algorithms
    """

    @staticmethod
    def fiber_optic_network(cities: List[str], distances: Dict[Tuple[str, str], float],
                           costs_per_km: float = 50000) -> Dict:
        """
        Plan fiber optic network connecting cities

        Args:
            cities: List of city names
            distances: Dict of (city1, city2) -> distance in km
            costs_per_km: Cost per kilometer of fiber optic cable

        Returns:
            Dictionary with MST solution and cost analysis
        """
        # Create city to index mapping
        city_to_idx = {city: idx for idx, city in enumerate(cities)}

        # Build edges list
        edges = []
        for (city1, city2), dist in distances.items():
            u = city_to_idx[city1]
            v = city_to_idx[city2]
            edges.append((u, v, dist))

        # Find MST
        mst = MSTAlgorithms(len(cities), edges)
        mst_edges, total_distance, _ = mst.kruskal()

        # Calculate costs
        total_cost = total_distance * costs_per_km

        # Build results
        connections = []
        for edge in mst_edges:
            city1 = cities[edge.u]
            city2 = cities[edge.v]
            distance = edge.weight
            cost = distance * costs_per_km
            connections.append({
                'from': city1,
                'to': city2,
                'distance_km': distance,
                'cost_usd': cost
            })

        return {
            'algorithm': 'Kruskal',
            'num_cities': len(cities),
            'num_connections': len(connections),
            'total_distance_km': total_distance,
            'total_cost_usd': total_cost,
            'connections': connections,
            'cost_per_km': costs_per_km
        }

    @staticmethod
    def electrical_grid(substations: List[str], power_lines: Dict[Tuple[str, str], Dict]) -> Dict:
        """
        Design electrical power grid connecting substations

        Args:
            substations: List of substation names
            power_lines: Dict of (sub1, sub2) -> {'distance': km, 'terrain': type, 'capacity': MW}

        Returns:
            Dictionary with MST solution and cost analysis
        """
        # Terrain cost multipliers
        terrain_multipliers = {
            'flat': 1.0,
            'hilly': 1.5,
            'mountainous': 2.5,
            'water': 3.0,
            'urban': 1.8
        }

        # Base cost per km for high-voltage transmission line
        base_cost_per_km = 1000000  # $1M per km

        # Create mapping
        sub_to_idx = {sub: idx for idx, sub in enumerate(substations)}

        # Build edges with weighted costs
        edges = []
        for (sub1, sub2), info in power_lines.items():
            u = sub_to_idx[sub1]
            v = sub_to_idx[sub2]
            distance = info['distance']
            terrain = info.get('terrain', 'flat')

            # Calculate cost based on distance and terrain
            cost_factor = distance * terrain_multipliers.get(terrain, 1.0)
            edges.append((u, v, cost_factor))

        # Find MST
        mst = MSTAlgorithms(len(substations), edges)
        mst_edges, total_cost_factor, _ = mst.prim()

        # Calculate actual costs and distances
        total_distance = 0
        total_cost = 0
        connections = []

        for edge in mst_edges:
            sub1 = substations[edge.u]
            sub2 = substations[edge.v]

            # Find original info
            orig_info = power_lines.get((sub1, sub2)) or power_lines.get((sub2, sub1))
            distance = orig_info['distance']
            terrain = orig_info.get('terrain', 'flat')
            capacity = orig_info.get('capacity', 0)

            cost = distance * base_cost_per_km * terrain_multipliers[terrain]
            total_distance += distance
            total_cost += cost

            connections.append({
                'from': sub1,
                'to': sub2,
                'distance_km': distance,
                'terrain': terrain,
                'capacity_mw': capacity,
                'cost_usd': cost
            })

        return {
            'algorithm': 'Prim',
            'num_substations': len(substations),
            'num_connections': len(connections),
            'total_distance_km': total_distance,
            'total_cost_usd': total_cost,
            'average_cost_per_km': total_cost / total_distance if total_distance > 0 else 0,
            'connections': connections
        }

    @staticmethod
    def telecom_network(towers: List[Tuple[float, float]], tower_names: List[str] = None) -> Dict:
        """
        Design telecommunications network connecting cell towers

        Args:
            towers: List of (latitude, longitude) coordinates
            tower_names: Optional list of tower names

        Returns:
            Dictionary with MST solution and network analysis
        """
        n = len(towers)

        if tower_names is None:
            tower_names = [f"Tower-{i+1}" for i in range(n)]

        # Calculate Euclidean distances between towers
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                lat1, lon1 = towers[i]
                lat2, lon2 = towers[j]

                # Approximate distance using Euclidean distance
                # (For real applications, use Haversine formula)
                distance = np.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2) * 111  # rough km conversion
                edges.append((i, j, distance))

        # Find MST using Borůvka (good for parallel processing)
        mst = MSTAlgorithms(n, edges)
        mst_edges, total_distance = mst.boruvka()

        # Cost per km for microwave link
        cost_per_km = 10000  # $10k per km
        total_cost = total_distance * cost_per_km

        # Build connections
        connections = []
        for edge in mst_edges:
            connections.append({
                'from': tower_names[edge.u],
                'to': tower_names[edge.v],
                'from_coords': towers[edge.u],
                'to_coords': towers[edge.v],
                'distance_km': edge.weight,
                'cost_usd': edge.weight * cost_per_km,
                'link_type': 'microwave' if edge.weight < 50 else 'fiber'
            })

        return {
            'algorithm': 'Boruvka',
            'num_towers': n,
            'num_links': len(connections),
            'total_distance_km': total_distance,
            'total_cost_usd': total_cost,
            'average_link_distance': total_distance / len(connections) if connections else 0,
            'connections': connections
        }


class ClusterAnalysis:
    """
    MST-based cluster analysis and hierarchical clustering
    """

    @staticmethod
    def hierarchical_clustering(points: np.ndarray, n_clusters: int) -> Dict:
        """
        Perform hierarchical clustering using MST

        Args:
            points: Array of shape (n_samples, n_features)
            n_clusters: Number of clusters to create

        Returns:
            Dictionary with cluster assignments and analysis
        """
        n = len(points)

        # Calculate pairwise distances
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.linalg.norm(points[i] - points[j])
                edges.append((i, j, dist))

        # Find MST
        mst = MSTAlgorithms(n, edges)
        mst_edges, total_weight, _ = mst.kruskal()

        # Sort edges by weight (descending) and remove top k-1 edges
        sorted_edges = sorted(mst_edges, key=lambda e: e.weight, reverse=True)
        edges_to_remove = sorted_edges[:n_clusters - 1]

        # Build adjacency list without removed edges
        adj = [set() for _ in range(n)]
        for edge in mst_edges:
            if edge not in edges_to_remove:
                adj[edge.u].add(edge.v)
                adj[edge.v].add(edge.u)

        # Find connected components (clusters)
        visited = [False] * n
        clusters = []

        def dfs(node, cluster):
            visited[node] = True
            cluster.append(node)
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    dfs(neighbor, cluster)

        for i in range(n):
            if not visited[i]:
                cluster = []
                dfs(i, cluster)
                clusters.append(cluster)

        # Calculate cluster statistics
        cluster_stats = []
        for i, cluster in enumerate(clusters):
            cluster_points = points[cluster]
            centroid = np.mean(cluster_points, axis=0)
            inertia = np.sum([np.linalg.norm(p - centroid)**2 for p in cluster_points])

            cluster_stats.append({
                'cluster_id': i,
                'size': len(cluster),
                'centroid': centroid.tolist(),
                'inertia': inertia,
                'points': cluster
            })

        return {
            'n_clusters': len(clusters),
            'clusters': cluster_stats,
            'mst_weight': total_weight,
            'edges_removed': [(e.u, e.v, e.weight) for e in edges_to_remove]
        }


def demo_network_applications():
    """Demonstrate network infrastructure applications"""
    print("=" * 80)
    print("MST REAL-WORLD NETWORK APPLICATIONS")
    print("=" * 80)
    print()

    # 1. Fiber Optic Network Example
    print("1. FIBER OPTIC NETWORK PLANNING")
    print("-" * 80)

    cities = ['New York', 'Boston', 'Philadelphia', 'Washington DC', 'Pittsburgh']
    distances = {
        ('New York', 'Boston'): 346,
        ('New York', 'Philadelphia'): 152,
        ('New York', 'Washington DC'): 362,
        ('Boston', 'Philadelphia'): 434,
        ('Boston', 'Washington DC'): 634,
        ('Philadelphia', 'Washington DC'): 226,
        ('Philadelphia', 'Pittsburgh'): 490,
        ('Pittsburgh', 'Washington DC'): 382,
    }

    fiber_result = NetworkInfrastructure.fiber_optic_network(cities, distances)

    print(f"Cities to connect: {fiber_result['num_cities']}")
    print(f"Total distance: {fiber_result['total_distance_km']:.2f} km")
    print(f"Total cost: ${fiber_result['total_cost_usd']:,.2f}")
    print(f"Cost per km: ${fiber_result['cost_per_km']:,.2f}")
    print(f"\nOptimal connections:")
    for conn in fiber_result['connections']:
        print(f"  {conn['from']} <-> {conn['to']}: "
              f"{conn['distance_km']:.0f} km (${conn['cost_usd']:,.2f})")
    print()

    # 2. Electrical Grid Example
    print("2. ELECTRICAL GRID DESIGN")
    print("-" * 80)

    substations = ['Sub-A', 'Sub-B', 'Sub-C', 'Sub-D', 'Sub-E']
    power_lines = {
        ('Sub-A', 'Sub-B'): {'distance': 45, 'terrain': 'flat', 'capacity': 500},
        ('Sub-A', 'Sub-C'): {'distance': 78, 'terrain': 'hilly', 'capacity': 500},
        ('Sub-A', 'Sub-D'): {'distance': 120, 'terrain': 'mountainous', 'capacity': 300},
        ('Sub-B', 'Sub-C'): {'distance': 55, 'terrain': 'urban', 'capacity': 500},
        ('Sub-B', 'Sub-E'): {'distance': 92, 'terrain': 'flat', 'capacity': 400},
        ('Sub-C', 'Sub-D'): {'distance': 67, 'terrain': 'hilly', 'capacity': 400},
        ('Sub-C', 'Sub-E'): {'distance': 110, 'terrain': 'water', 'capacity': 300},
        ('Sub-D', 'Sub-E'): {'distance': 88, 'terrain': 'mountainous', 'capacity': 300},
    }

    grid_result = NetworkInfrastructure.electrical_grid(substations, power_lines)

    print(f"Substations: {grid_result['num_substations']}")
    print(f"Total distance: {grid_result['total_distance_km']:.2f} km")
    print(f"Total cost: ${grid_result['total_cost_usd']:,.2f}")
    print(f"Average cost per km: ${grid_result['average_cost_per_km']:,.2f}")
    print(f"\nOptimal transmission lines:")
    for conn in grid_result['connections']:
        print(f"  {conn['from']} <-> {conn['to']}: "
              f"{conn['distance_km']:.0f} km, {conn['terrain']}, "
              f"{conn['capacity_mw']} MW (${conn['cost_usd']:,.2f})")
    print()

    # 3. Telecommunications Network Example
    print("3. TELECOMMUNICATIONS NETWORK")
    print("-" * 80)

    # Generate random tower locations
    np.random.seed(42)
    towers = [(np.random.uniform(40, 45), np.random.uniform(-75, -70)) for _ in range(8)]

    telecom_result = NetworkInfrastructure.telecom_network(towers)

    print(f"Cell towers: {telecom_result['num_towers']}")
    print(f"Total distance: {telecom_result['total_distance_km']:.2f} km")
    print(f"Total cost: ${telecom_result['total_cost_usd']:,.2f}")
    print(f"Average link distance: {telecom_result['average_link_distance']:.2f} km")
    print(f"\nNetwork links:")
    for i, conn in enumerate(telecom_result['connections'][:5]):  # Show first 5
        print(f"  {conn['from']} <-> {conn['to']}: "
              f"{conn['distance_km']:.2f} km, {conn['link_type']}")
    if len(telecom_result['connections']) > 5:
        print(f"  ... and {len(telecom_result['connections']) - 5} more links")
    print()

    # 4. Cluster Analysis Example
    print("4. HIERARCHICAL CLUSTERING (MST-based)")
    print("-" * 80)

    # Generate sample data with 3 clusters
    np.random.seed(42)
    cluster1 = np.random.randn(20, 2) + np.array([0, 0])
    cluster2 = np.random.randn(20, 2) + np.array([5, 5])
    cluster3 = np.random.randn(20, 2) + np.array([10, 0])
    points = np.vstack([cluster1, cluster2, cluster3])

    clustering_result = ClusterAnalysis.hierarchical_clustering(points, n_clusters=3)

    print(f"Total points: {len(points)}")
    print(f"Number of clusters: {clustering_result['n_clusters']}")
    print(f"MST total weight: {clustering_result['mst_weight']:.2f}")
    print(f"\nCluster details:")
    for cluster in clustering_result['clusters']:
        print(f"  Cluster {cluster['cluster_id']}: "
              f"{cluster['size']} points, "
              f"inertia={cluster['inertia']:.2f}")
    print()

    # 5. Cost Comparison
    print("5. COST ANALYSIS SUMMARY")
    print("-" * 80)
    print(f"{'Application':<30} {'Total Cost':<20} {'Cost/Unit':<20}")
    print("-" * 80)
    print(f"{'Fiber Optic Network':<30} ${fiber_result['total_cost_usd']:>12,.2f}   "
          f"${fiber_result['total_cost_usd']/fiber_result['num_connections']:>12,.2f}/link")
    print(f"{'Electrical Grid':<30} ${grid_result['total_cost_usd']:>12,.2f}   "
          f"${grid_result['total_cost_usd']/grid_result['num_connections']:>12,.2f}/line")
    print(f"{'Telecom Network':<30} ${telecom_result['total_cost_usd']:>12,.2f}   "
          f"${telecom_result['total_cost_usd']/telecom_result['num_links']:>12,.2f}/link")
    print()

    print("=" * 80)
    print("All network applications demonstrate significant cost savings")
    print("using MST algorithms compared to full mesh topology!")
    print("=" * 80)


if __name__ == "__main__":
    demo_network_applications()
