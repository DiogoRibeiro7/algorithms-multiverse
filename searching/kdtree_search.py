"""
K-D Tree (K-Dimensional Tree) for Geometric Search

Time Complexity:
- Construction: O(n log n)
- Search: O(log n) average, O(n) worst case
- Nearest Neighbor: O(log n) average, O(n) worst case
- Range Query: O(n^(1-1/k) + m) where m is number of points in range

Space Complexity: O(n)

WHEN TO USE KD-TREES:
1. Multi-dimensional spatial data (2D, 3D points)
2. Nearest neighbor queries
3. Range searches in k dimensions
4. Low to moderate dimensions (k < 20)

PERFORMANCE CHARACTERISTICS:
- Excellent for low dimensions (2-10)
- Degrades in high dimensions (curse of dimensionality)
- Better than linear scan for d < log(n)
- Balanced tree provides best performance

ADVANTAGES:
- Logarithmic search for low dimensions
- Space efficient O(n)
- Supports multiple query types
- Simple to implement

DISADVANTAGES:
- Poor performance in high dimensions (d > 20)
- Balancing required for optimal performance
- Range queries can degrade to O(n)
- Not good for dynamic datasets (insertions/deletions)

APPLICATIONS:
- Geographic information systems (GIS)
- Computer graphics (collision detection)
- Machine learning (k-NN classification)
- Robotics (path planning)
- Point cloud processing
"""

from typing import List, Tuple, Optional
import math


class KDNode:
    """Node in a KD-Tree"""

    def __init__(self, point: List[float], axis: int):
        self.point = point
        self.axis = axis
        self.left: Optional[KDNode] = None
        self.right: Optional[KDNode] = None


class KDTree:
    """
    K-Dimensional Tree for efficient spatial searching
    """

    def __init__(self, points: List[List[float]], k: int = 2):
        """
        Initialize KD-Tree with list of points

        Args:
            points: List of k-dimensional points
            k: Number of dimensions
        """
        self.k = k
        self.root = self._build(points, 0)

    def _build(self, points: List[List[float]], depth: int) -> Optional[KDNode]:
        """
        Recursively build KD-Tree

        Args:
            points: List of points to build tree from
            depth: Current depth in tree

        Returns:
            Root node of subtree
        """
        if not points:
            return None

        # Cycle through axes
        axis = depth % self.k

        # Sort points by current axis and choose median
        points.sort(key=lambda p: p[axis])
        median = len(points) // 2

        # Create node and recursively build subtrees
        node = KDNode(points[median], axis)
        node.left = self._build(points[:median], depth + 1)
        node.right = self._build(points[median + 1:], depth + 1)

        return node

    def search(self, point: List[float]) -> bool:
        """
        Search for exact point in tree

        Args:
            point: Point to search for

        Returns:
            True if point exists in tree
        """
        def _search_recursive(node: Optional[KDNode], target: List[float], depth: int) -> bool:
            if node is None:
                return False

            # Check if current node matches
            if node.point == target:
                return True

            # Determine which subtree to search
            axis = depth % self.k
            if target[axis] < node.point[axis]:
                return _search_recursive(node.left, target, depth + 1)
            else:
                return _search_recursive(node.right, target, depth + 1)

        return _search_recursive(self.root, point, 0)

    def nearest_neighbor(self, target: List[float]) -> Tuple[List[float], float]:
        """
        Find nearest neighbor to target point

        Args:
            target: Query point

        Returns:
            Tuple of (nearest_point, distance)
        """
        best = [None, float('inf')]

        def _nn_recursive(node: Optional[KDNode], target: List[float], depth: int):
            if node is None:
                return

            # Calculate distance to current node
            dist = self._distance(node.point, target)

            # Update best if closer
            if dist < best[1]:
                best[0] = node.point
                best[1] = dist

            # Determine which side to search first
            axis = depth % self.k
            diff = target[axis] - node.point[axis]

            # Search near side first
            if diff < 0:
                _nn_recursive(node.left, target, depth + 1)
                # Check if we need to search far side
                if diff * diff < best[1]:
                    _nn_recursive(node.right, target, depth + 1)
            else:
                _nn_recursive(node.right, target, depth + 1)
                # Check if we need to search far side
                if diff * diff < best[1]:
                    _nn_recursive(node.left, target, depth + 1)

        _nn_recursive(self.root, target, 0)
        return best[0], math.sqrt(best[1])

    def k_nearest_neighbors(self, target: List[float], k: int) -> List[Tuple[List[float], float]]:
        """
        Find k nearest neighbors to target point

        Args:
            target: Query point
            k: Number of neighbors to find

        Returns:
            List of (point, distance) tuples
        """
        import heapq

        # Use max heap to keep track of k nearest
        # Store as negative distance for max heap behavior
        heap = []

        def _knn_recursive(node: Optional[KDNode], target: List[float], depth: int):
            if node is None:
                return

            # Calculate distance to current node
            dist = self._distance(node.point, target)

            # Add to heap if we have less than k points or this is closer
            if len(heap) < k:
                heapq.heappush(heap, (-dist, node.point))
            elif dist < -heap[0][0]:
                heapq.heapreplace(heap, (-dist, node.point))

            # Determine which side to search
            axis = depth % self.k
            diff = target[axis] - node.point[axis]

            # Search near side first
            if diff < 0:
                _knn_recursive(node.left, target, depth + 1)
                # Check if we need to search far side
                if len(heap) < k or diff * diff < -heap[0][0]:
                    _knn_recursive(node.right, target, depth + 1)
            else:
                _knn_recursive(node.right, target, depth + 1)
                # Check if we need to search far side
                if len(heap) < k or diff * diff < -heap[0][0]:
                    _knn_recursive(node.left, target, depth + 1)

        _knn_recursive(self.root, target, 0)

        # Convert heap to sorted list
        result = [(point, math.sqrt(-dist)) for dist, point in heap]
        result.sort(key=lambda x: x[1])
        return result

    def range_search(self, lower: List[float], upper: List[float]) -> List[List[float]]:
        """
        Find all points within a rectangular range

        Args:
            lower: Lower bounds for each dimension
            upper: Upper bounds for each dimension

        Returns:
            List of points within range
        """
        result = []

        def _range_recursive(node: Optional[KDNode], depth: int):
            if node is None:
                return

            # Check if current point is in range
            in_range = all(lower[i] <= node.point[i] <= upper[i] for i in range(self.k))
            if in_range:
                result.append(node.point)

            # Determine which subtrees to search
            axis = depth % self.k

            # Search left if range overlaps left subtree
            if lower[axis] <= node.point[axis]:
                _range_recursive(node.left, depth + 1)

            # Search right if range overlaps right subtree
            if upper[axis] >= node.point[axis]:
                _range_recursive(node.right, depth + 1)

        _range_recursive(self.root, 0)
        return result

    def radius_search(self, center: List[float], radius: float) -> List[Tuple[List[float], float]]:
        """
        Find all points within radius of center

        Args:
            center: Center point
            radius: Search radius

        Returns:
            List of (point, distance) tuples within radius
        """
        result = []
        radius_squared = radius * radius

        def _radius_recursive(node: Optional[KDNode], depth: int):
            if node is None:
                return

            # Calculate distance to current node
            dist_squared = self._distance(node.point, center)

            # Add to result if within radius
            if dist_squared <= radius_squared:
                result.append((node.point, math.sqrt(dist_squared)))

            # Determine which subtrees might contain points in radius
            axis = depth % self.k
            diff = center[axis] - node.point[axis]

            # Always search near side
            if diff < 0:
                _radius_recursive(node.left, depth + 1)
                # Search far side if circle intersects splitting plane
                if diff * diff <= radius_squared:
                    _radius_recursive(node.right, depth + 1)
            else:
                _radius_recursive(node.right, depth + 1)
                # Search far side if circle intersects splitting plane
                if diff * diff <= radius_squared:
                    _radius_recursive(node.left, depth + 1)

        _radius_recursive(self.root, 0)
        result.sort(key=lambda x: x[1])
        return result

    def _distance(self, p1: List[float], p2: List[float]) -> float:
        """
        Calculate squared Euclidean distance (faster, no sqrt)

        Args:
            p1: First point
            p2: Second point

        Returns:
            Squared distance
        """
        return sum((a - b) ** 2 for a, b in zip(p1, p2))


# Performance testing and demonstration
if __name__ == "__main__":
    import random
    import time

    print("=== KD-Tree Geometric Search Demonstrations ===\n")

    # 1. Basic 2D example
    print("1. Basic 2D Point Search")
    points_2d = [
        [2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]
    ]

    tree_2d = KDTree(points_2d, k=2)

    # Exact search
    search_point = [7, 2]
    found = tree_2d.search(search_point)
    print(f"Searching for {search_point}: {'Found' if found else 'Not found'}")

    # Nearest neighbor
    query = [6, 3]
    nearest, dist = tree_2d.nearest_neighbor(query)
    print(f"Nearest neighbor to {query}: {nearest} at distance {dist:.2f}")

    # K nearest neighbors
    k_nearest = tree_2d.k_nearest_neighbors(query, k=3)
    print(f"3 nearest neighbors to {query}:")
    for point, distance in k_nearest:
        print(f"  {point} at distance {distance:.2f}")

    print()

    # 2. Range search
    print("2. Range Search (2D Rectangle)")
    lower = [3, 2]
    upper = [8, 6]
    in_range = tree_2d.range_search(lower, upper)
    print(f"Points in range [{lower}, {upper}]: {in_range}")

    # Radius search
    center = [5, 4]
    radius = 3
    in_radius = tree_2d.radius_search(center, radius)
    print(f"\nPoints within radius {radius} of {center}:")
    for point, dist in in_radius:
        print(f"  {point} at distance {dist:.2f}")

    print()

    # 3. 3D example
    print("3. 3D Point Cloud")
    points_3d = [
        [random.uniform(0, 100) for _ in range(3)]
        for _ in range(1000)
    ]
    tree_3d = KDTree(points_3d, k=3)

    query_3d = [50, 50, 50]
    nearest_3d, dist_3d = tree_3d.nearest_neighbor(query_3d)
    print(f"Nearest to {query_3d}:")
    print(f"  Point: [{nearest_3d[0]:.1f}, {nearest_3d[1]:.1f}, {nearest_3d[2]:.1f}]")
    print(f"  Distance: {dist_3d:.2f}")

    print()

    # 4. Performance comparison
    print("4. Performance Comparison: KD-Tree vs Linear Scan\n")

    dimensions = [2, 3, 5, 10]
    sizes = [1000, 10000, 100000]

    for dim in dimensions:
        print(f"Dimension: {dim}")

        for size in sizes:
            # Generate random points
            points = [
                [random.uniform(0, 1000) for _ in range(dim)]
                for _ in range(size)
            ]

            # Build KD-Tree
            build_start = time.perf_counter()
            tree = KDTree(points, k=dim)
            build_time = time.perf_counter() - build_start

            # Query point
            query = [random.uniform(0, 1000) for _ in range(dim)]

            # KD-Tree search
            kd_start = time.perf_counter()
            for _ in range(100):
                tree.nearest_neighbor(query)
            kd_time = time.perf_counter() - kd_start

            # Linear scan
            def linear_nn(points, query):
                best_dist = float('inf')
                best_point = None
                for point in points:
                    dist = sum((a - b) ** 2 for a, b in zip(point, query))
                    if dist < best_dist:
                        best_dist = dist
                        best_point = point
                return best_point, math.sqrt(best_dist)

            linear_start = time.perf_counter()
            for _ in range(100):
                linear_nn(points, query)
            linear_time = time.perf_counter() - linear_start

            print(f"  Size {size:6d}: Build={build_time*1000:6.1f}ms, "
                  f"KD={kd_time*1000:6.1f}ms, Linear={linear_time*1000:7.1f}ms, "
                  f"Speedup={linear_time/kd_time:5.1f}x")

        print()

    # 5. Curse of dimensionality demonstration
    print("5. Curse of Dimensionality")
    print("Performance degrades in high dimensions:\n")

    size = 10000
    for dim in [2, 5, 10, 20, 50]:
        points = [
            [random.uniform(0, 1000) for _ in range(dim)]
            for _ in range(size)
        ]

        tree = KDTree(points, k=dim)
        query = [random.uniform(0, 1000) for _ in range(dim)]

        start = time.perf_counter()
        for _ in range(10):
            tree.nearest_neighbor(query)
        elapsed = time.perf_counter() - start

        print(f"  Dimension {dim:2d}: {elapsed*100:.2f}ms per query")

    print("\n=== Key Takeaways ===")
    print("• Excellent performance for 2-10 dimensions")
    print("• Construction time: O(n log n), one-time cost")
    print("• Query time: O(log n) average for low dimensions")
    print("• Degrades significantly beyond 20 dimensions")
    print("• Best for: GIS, graphics, ML (k-NN), point clouds")
    print("• Consider alternatives for high dimensions (LSH, ball trees)")
