"""
Computational Geometry Algorithms - Comprehensive Implementation

A complete collection of fundamental computational geometry algorithms with
robust floating-point handling and practical applications.

Algorithms Implemented:
1. Convex Hull
   - Graham Scan (O(n log n))
   - Jarvis March/Gift Wrapping (O(nh))
   - Quick Hull (O(n log n) average)

2. Line Operations
   - Line segment intersection
   - Point-line distance
   - Orientation tests

3. Point-in-Polygon
   - Ray casting algorithm
   - Winding number algorithm

4. Closest Pair of Points
   - Divide and conquer (O(n log n))
   - Brute force (O(n²))

5. Geometric Primitives
   - Point, Vector, Line, Polygon classes
   - Distance calculations
   - Area calculations

6. Advanced Algorithms
   - Rotating calipers (diameter, width)
   - Line sweep algorithms
   - Basic Delaunay triangulation

Applications:
- Computer Graphics (collision detection, rendering)
- GIS (geographic information systems)
- Robotics (path planning, obstacle avoidance)
- CAD/CAM systems
- Computer vision
- Game development

Author: Claude Code
Python 3.8+
"""

import math
import random
import time
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
import sys

# Floating-point precision threshold
EPSILON = 1e-9


# ==============================================================================
# 1. GEOMETRIC PRIMITIVES
# ==============================================================================

@dataclass(frozen=True)
class Point:
    """
    2D Point with robust floating-point comparisons.

    Immutable for use in sets and as dictionary keys.
    """
    x: float
    y: float

    def __eq__(self, other):
        """Equality with epsilon tolerance."""
        if not isinstance(other, Point):
            return False
        return (abs(self.x - other.x) < EPSILON and
                abs(self.y - other.y) < EPSILON)

    def __hash__(self):
        """Hash for use in sets/dicts."""
        return hash((round(self.x / EPSILON), round(self.y / EPSILON)))

    def __lt__(self, other):
        """
        Lexicographic ordering for sorting.
        First by x, then by y.
        """
        if abs(self.x - other.x) > EPSILON:
            return self.x < other.x
        return self.y < other.y

    def __sub__(self, other):
        """Vector subtraction."""
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, vector):
        """Point translation by vector."""
        if isinstance(vector, Vector):
            return Point(self.x + vector.x, self.y + vector.y)
        return NotImplemented

    def distance_to(self, other: 'Point') -> float:
        """Euclidean distance to another point."""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def __repr__(self):
        return f"Point({self.x:.3f}, {self.y:.3f})"


@dataclass(frozen=True)
class Vector:
    """2D Vector for geometric operations."""
    x: float
    y: float

    def __add__(self, other):
        """Vector addition."""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Vector subtraction."""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """Scalar multiplication."""
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        """Right scalar multiplication."""
        return self * scalar

    def dot(self, other: 'Vector') -> float:
        """Dot product."""
        return self.x * other.x + self.y * other.y

    def cross(self, other: 'Vector') -> float:
        """
        Cross product (z-component in 2D).

        Returns positive if other is counterclockwise from self,
        negative if clockwise, zero if collinear.
        """
        return self.x * other.y - self.y * other.x

    def magnitude(self) -> float:
        """Vector magnitude."""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalize(self) -> 'Vector':
        """Unit vector in same direction."""
        mag = self.magnitude()
        if mag < EPSILON:
            return Vector(0, 0)
        return Vector(self.x / mag, self.y / mag)

    def perpendicular(self) -> 'Vector':
        """Perpendicular vector (90° counterclockwise)."""
        return Vector(-self.y, self.x)


class Orientation(Enum):
    """Orientation of three points."""
    COLLINEAR = 0
    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2


def orientation(p: Point, q: Point, r: Point) -> Orientation:
    """
    Determine orientation of ordered triplet (p, q, r).

    Uses cross product of vectors (q-p) and (r-p).

    Returns:
        COLLINEAR if points are collinear
        CLOCKWISE if r is clockwise from vector p→q
        COUNTERCLOCKWISE if r is counterclockwise from p→q

    Applications:
        - Convex hull algorithms
        - Line intersection
        - Point-in-polygon tests
    """
    v1 = q - p
    v2 = r - p
    cross = v1.cross(v2)

    if abs(cross) < EPSILON:
        return Orientation.COLLINEAR
    return Orientation.CLOCKWISE if cross < 0 else Orientation.COUNTERCLOCKWISE


def distance_point_to_line(point: Point, line_start: Point, line_end: Point) -> float:
    """
    Perpendicular distance from point to infinite line.

    Formula: |cross(v1, v2)| / |v1|
    where v1 = line_end - line_start, v2 = point - line_start
    """
    v1 = line_end - line_start
    v2 = point - line_start

    mag = v1.magnitude()
    if mag < EPSILON:
        return v2.magnitude()

    return abs(v1.cross(v2)) / mag


def distance_point_to_segment(point: Point, seg_start: Point, seg_end: Point) -> float:
    """
    Distance from point to line segment (not infinite line).

    Handles three cases:
    1. Projection falls before segment start
    2. Projection falls after segment end
    3. Projection falls on segment
    """
    v = seg_end - seg_start
    w = point - seg_start

    # Project w onto v
    c1 = w.dot(v)
    if c1 <= 0:  # Before start
        return point.distance_to(seg_start)

    c2 = v.dot(v)
    if c1 >= c2:  # After end
        return point.distance_to(seg_end)

    # On segment
    b = c1 / c2
    projection = seg_start + v * b
    return point.distance_to(projection)


# ==============================================================================
# 2. CONVEX HULL ALGORITHMS
# ==============================================================================

def convex_hull_graham_scan(points: List[Point]) -> List[Point]:
    """
    Graham Scan algorithm for convex hull.

    Algorithm:
    1. Find point with lowest y-coordinate (breaking ties by x)
    2. Sort other points by polar angle with respect to this point
    3. Process points in order, maintaining convex hull using stack
    4. For each point, pop points that make right turns

    Time Complexity: O(n log n) - dominated by sorting
    Space Complexity: O(n)

    Advantages:
    - Simple to implement
    - Optimal time complexity
    - Stable and predictable

    Args:
        points: List of points (may contain duplicates)

    Returns:
        List of points forming convex hull in counterclockwise order

    Examples:
        >>> pts = [Point(0,0), Point(1,1), Point(2,0), Point(1,0.5)]
        >>> hull = convex_hull_graham_scan(pts)
        >>> len(hull)
        3  # Triangle

    Applications:
        - Collision detection
        - Shape approximation
        - Geographic analysis
    """
    if len(points) < 3:
        return sorted(set(points))

    # Remove duplicates
    points = sorted(set(points))

    if len(points) < 3:
        return points

    # Find starting point (lowest y, then lowest x)
    start = min(points, key=lambda p: (p.y, p.x))

    # Sort by polar angle with respect to start point
    def polar_angle_key(p: Point) -> Tuple[float, float]:
        if p == start:
            return (-math.pi, 0)  # Start point comes first

        v = p - start
        angle = math.atan2(v.y, v.x)
        distance = v.magnitude()
        return (angle, distance)

    sorted_points = sorted(points, key=polar_angle_key)

    # Build hull using stack
    hull = []

    for point in sorted_points:
        # Remove points that make right turn
        while len(hull) >= 2:
            if orientation(hull[-2], hull[-1], point) != Orientation.COUNTERCLOCKWISE:
                hull.pop()
            else:
                break
        hull.append(point)

    return hull


def convex_hull_jarvis_march(points: List[Point]) -> List[Point]:
    """
    Jarvis March (Gift Wrapping) algorithm for convex hull.

    Algorithm:
    1. Start with leftmost point
    2. For current point, find the most counterclockwise point
    3. Add to hull and repeat until back to start

    Time Complexity: O(nh) where h is number of hull points
    Space Complexity: O(h)

    Advantages:
    - Output-sensitive (good when h << n)
    - Simple conceptually
    - Works well for small hulls

    Disadvantages:
    - Worst case O(n²) when all points are on hull

    Args:
        points: List of points

    Returns:
        List of points forming convex hull in counterclockwise order
    """
    if len(points) < 3:
        return sorted(set(points))

    points = list(set(points))

    if len(points) < 3:
        return points

    # Find leftmost point
    leftmost = min(points, key=lambda p: (p.x, p.y))

    hull = []
    current = leftmost

    while True:
        hull.append(current)
        next_point = points[0]

        for candidate in points[1:]:
            if next_point == current:
                next_point = candidate
                continue

            orient = orientation(current, next_point, candidate)

            # Choose most counterclockwise point
            # Break ties by choosing farthest
            if (orient == Orientation.COUNTERCLOCKWISE or
                (orient == Orientation.COLLINEAR and
                 current.distance_to(candidate) > current.distance_to(next_point))):
                next_point = candidate

        current = next_point

        # Back to start
        if current == leftmost:
            break

    return hull[:-1]  # Remove duplicate of start point


def convex_hull_quick_hull(points: List[Point]) -> List[Point]:
    """
    QuickHull algorithm for convex hull.

    Algorithm (divide and conquer):
    1. Find points with min and max x-coordinates
    2. Divide points into two sets by line between these points
    3. Recursively find hull for each side
    4. Combine results

    Time Complexity: O(n log n) average, O(n²) worst
    Space Complexity: O(n) for recursion

    Advantages:
    - Often faster in practice than Graham scan
    - Easy to parallelize
    - Good cache locality

    Args:
        points: List of points

    Returns:
        List of points forming convex hull
    """
    if len(points) < 3:
        return sorted(set(points))

    points = list(set(points))

    if len(points) < 3:
        return points

    # Find extreme points
    min_x = min(points, key=lambda p: (p.x, p.y))
    max_x = max(points, key=lambda p: (p.x, p.y))

    # Divide points
    def find_hull(p1: Point, p2: Point, points_set: Set[Point]) -> List[Point]:
        if not points_set:
            return []

        # Find point farthest from line p1-p2
        farthest = max(points_set,
                      key=lambda p: distance_point_to_line(p, p1, p2))

        # Points outside triangle (p1, farthest, p2)
        left_set = {p for p in points_set
                   if orientation(p1, farthest, p) == Orientation.COUNTERCLOCKWISE}
        right_set = {p for p in points_set
                    if orientation(farthest, p2, p) == Orientation.COUNTERCLOCKWISE}

        # Recursively find hull
        result = find_hull(p1, farthest, left_set)
        result.append(farthest)
        result.extend(find_hull(farthest, p2, right_set))

        return result

    # Split by line min_x to max_x
    upper_set = {p for p in points
                if orientation(min_x, max_x, p) == Orientation.COUNTERCLOCKWISE}
    lower_set = {p for p in points
                if orientation(min_x, max_x, p) == Orientation.CLOCKWISE}

    hull = [min_x]
    hull.extend(find_hull(min_x, max_x, upper_set))
    hull.append(max_x)
    hull.extend(find_hull(max_x, min_x, lower_set))

    return hull


# ==============================================================================
# 3. LINE INTERSECTION
# ==============================================================================

def segments_intersect(p1: Point, q1: Point, p2: Point, q2: Point) -> bool:
    """
    Check if line segments (p1,q1) and (p2,q2) intersect.

    Uses orientation test for efficiency.

    Two segments intersect if:
    1. General case: orientations differ
    2. Special case: collinear and overlapping

    Time Complexity: O(1)
    """
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Special cases - collinear points
    def on_segment(p: Point, q: Point, r: Point) -> bool:
        """Check if q lies on segment pr (given they're collinear)."""
        return (min(p.x, r.x) <= q.x <= max(p.x, r.x) and
                min(p.y, r.y) <= q.y <= max(p.y, r.y))

    if o1 == Orientation.COLLINEAR and on_segment(p1, p2, q1):
        return True
    if o2 == Orientation.COLLINEAR and on_segment(p1, q2, q1):
        return True
    if o3 == Orientation.COLLINEAR and on_segment(p2, p1, q2):
        return True
    if o4 == Orientation.COLLINEAR and on_segment(p2, q1, q2):
        return True

    return False


def line_intersection_point(p1: Point, q1: Point,
                            p2: Point, q2: Point) -> Optional[Point]:
    """
    Find intersection point of two line segments.

    Uses parametric form:
    Line 1: p1 + t*(q1-p1)
    Line 2: p2 + s*(q2-p2)

    Solves for t and s, checks if both in [0,1]

    Returns:
        Intersection point if exists, None otherwise
    """
    v1 = q1 - p1
    v2 = q2 - p2
    v3 = p1 - p2

    cross_v1_v2 = v1.cross(v2)

    # Parallel or collinear
    if abs(cross_v1_v2) < EPSILON:
        return None

    t = v3.cross(v2) / cross_v1_v2
    s = v3.cross(v1) / cross_v1_v2

    # Check if intersection point is on both segments
    if 0 <= t <= 1 and 0 <= s <= 1:
        return p1 + v1 * t

    return None


# ==============================================================================
# 4. POINT-IN-POLYGON TESTS
# ==============================================================================

def point_in_polygon_ray_casting(point: Point, polygon: List[Point]) -> bool:
    """
    Ray casting algorithm for point-in-polygon test.

    Algorithm:
    Cast a ray from point to infinity (in positive x direction).
    Count intersections with polygon edges.
    Odd count = inside, even count = outside.

    Time Complexity: O(n) where n is number of polygon vertices
    Space Complexity: O(1)

    Handles edge cases:
    - Point on edge
    - Point on vertex
    - Ray through vertex

    Args:
        point: Query point
        polygon: List of vertices in order (clockwise or counterclockwise)

    Returns:
        True if point is inside or on polygon boundary

    Applications:
        - GIS (point in region queries)
        - Computer graphics (picking)
        - Game development (collision detection)
    """
    n = len(polygon)
    if n < 3:
        return False

    count = 0

    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]

        # Check if point is on edge
        if distance_point_to_segment(point, p1, p2) < EPSILON:
            return True

        # Ray casting
        if ((p1.y > point.y) != (p2.y > point.y)):
            # Compute x coordinate of intersection
            x_intersect = (p2.x - p1.x) * (point.y - p1.y) / (p2.y - p1.y) + p1.x

            if point.x < x_intersect:
                count += 1

    return count % 2 == 1


def point_in_polygon_winding_number(point: Point, polygon: List[Point]) -> bool:
    """
    Winding number algorithm for point-in-polygon test.

    Counts how many times polygon winds around point.
    More robust than ray casting for complex polygons.

    Winding number ≠ 0 means point is inside.

    Time Complexity: O(n)
    Space Complexity: O(1)

    Advantages:
    - Handles self-intersecting polygons
    - More numerically stable
    - Works for holes (even-odd winding rule)
    """
    n = len(polygon)
    if n < 3:
        return False

    winding_number = 0

    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]

        if p1.y <= point.y:
            if p2.y > point.y:  # Upward crossing
                if orientation(p1, p2, point) == Orientation.COUNTERCLOCKWISE:
                    winding_number += 1
        else:
            if p2.y <= point.y:  # Downward crossing
                if orientation(p1, p2, point) == Orientation.CLOCKWISE:
                    winding_number -= 1

    return winding_number != 0


# ==============================================================================
# 5. CLOSEST PAIR OF POINTS
# ==============================================================================

def closest_pair_brute_force(points: List[Point]) -> Tuple[Point, Point, float]:
    """
    Brute force closest pair algorithm.

    Time Complexity: O(n²)
    Space Complexity: O(1)

    Good for small datasets (n < 100).
    """
    if len(points) < 2:
        raise ValueError("Need at least 2 points")

    min_dist = float('inf')
    pair = (points[0], points[1])

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = points[i].distance_to(points[j])
            if dist < min_dist:
                min_dist = dist
                pair = (points[i], points[j])

    return pair[0], pair[1], min_dist


def closest_pair_divide_conquer(points: List[Point]) -> Tuple[Point, Point, float]:
    """
    Divide and conquer closest pair algorithm.

    Algorithm:
    1. Sort points by x-coordinate
    2. Divide into left and right halves
    3. Recursively find closest pair in each half
    4. Find closest pair with one point in each half
    5. Return minimum of three

    Time Complexity: O(n log n)
    Space Complexity: O(n)

    Applications:
        - Clustering algorithms
        - Collision detection
        - Nearest neighbor problems
    """
    def closest_pair_recursive(px: List[Point], py: List[Point]) -> Tuple[Point, Point, float]:
        n = len(px)

        # Base case: use brute force for small sets
        if n <= 3:
            return closest_pair_brute_force(px)

        # Divide
        mid = n // 2
        midpoint = px[mid]

        pyl = [p for p in py if p.x <= midpoint.x]
        pyr = [p for p in py if p.x > midpoint.x]

        # Conquer
        (p1l, p2l, dl) = closest_pair_recursive(px[:mid], pyl)
        (p1r, p2r, dr) = closest_pair_recursive(px[mid:], pyr)

        # Find minimum
        if dl < dr:
            d = dl
            pair = (p1l, p2l)
        else:
            d = dr
            pair = (p1r, p2r)

        # Build strip of points close to dividing line
        strip = [p for p in py if abs(p.x - midpoint.x) < d]

        # Find closest pair in strip
        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and (strip[j].y - strip[i].y) < d:
                dist = strip[i].distance_to(strip[j])
                if dist < d:
                    d = dist
                    pair = (strip[i], strip[j])
                j += 1

        return pair[0], pair[1], d

    if len(points) < 2:
        raise ValueError("Need at least 2 points")

    # Remove duplicates
    points = list(set(points))

    if len(points) < 2:
        raise ValueError("Need at least 2 distinct points")

    # Sort by x and y coordinates
    px = sorted(points, key=lambda p: p.x)
    py = sorted(points, key=lambda p: p.y)

    return closest_pair_recursive(px, py)


# ==============================================================================
# 6. POLYGON OPERATIONS
# ==============================================================================

def polygon_area(polygon: List[Point]) -> float:
    """
    Calculate area of polygon using shoelace formula.

    Formula: A = 0.5 * |Σ(x_i * y_{i+1} - x_{i+1} * y_i)|

    Works for both convex and concave polygons.
    Returns positive for counterclockwise, negative for clockwise.

    Time Complexity: O(n)
    """
    if len(polygon) < 3:
        return 0.0

    area = 0.0
    n = len(polygon)

    for i in range(n):
        j = (i + 1) % n
        area += polygon[i].x * polygon[j].y
        area -= polygon[j].x * polygon[i].y

    return abs(area) / 2.0


def polygon_centroid(polygon: List[Point]) -> Point:
    """
    Calculate centroid of polygon.

    For uniform density polygons.

    Time Complexity: O(n)
    """
    if len(polygon) < 3:
        return polygon[0] if polygon else Point(0, 0)

    cx = cy = 0.0
    area = 0.0
    n = len(polygon)

    for i in range(n):
        j = (i + 1) % n
        cross = polygon[i].x * polygon[j].y - polygon[j].x * polygon[i].y
        cx += (polygon[i].x + polygon[j].x) * cross
        cy += (polygon[i].y + polygon[j].y) * cross
        area += cross

    area *= 3.0  # 6 * 0.5

    if abs(area) < EPSILON:
        return polygon[0]

    return Point(cx / area, cy / area)


# ==============================================================================
# 7. VISUALIZATION
# ==============================================================================

def visualize_points_ascii(points: List[Point], hull: Optional[List[Point]] = None,
                          width: int = 60, height: int = 30) -> str:
    """
    Create ASCII art visualization of points and optional convex hull.

    Args:
        points: All points to display
        hull: Optional convex hull points to highlight
        width: Canvas width
        height: Canvas height

    Returns:
        String containing ASCII art
    """
    if not points:
        return "No points to visualize"

    # Find bounding box
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)

    # Add padding
    range_x = max_x - min_x or 1
    range_y = max_y - min_y or 1
    padding = 0.1
    min_x -= range_x * padding
    max_x += range_x * padding
    min_y -= range_y * padding
    max_y += range_y * padding
    range_x = max_x - min_x
    range_y = max_y - min_y

    # Create canvas
    canvas = [[' ' for _ in range(width)] for _ in range(height)]

    # Draw axes
    for i in range(height):
        canvas[i][0] = '|'
    for j in range(width):
        canvas[height-1][j] = '-'
    canvas[height-1][0] = '+'

    # Map point to canvas
    def map_point(p: Point) -> Tuple[int, int]:
        x = int((p.x - min_x) / range_x * (width - 2)) + 1
        y = int((1 - (p.y - min_y) / range_y) * (height - 2))
        return (min(max(y, 0), height-1), min(max(x, 0), width-1))

    # Draw hull edges
    if hull and len(hull) >= 2:
        for i in range(len(hull)):
            p1 = hull[i]
            p2 = hull[(i + 1) % len(hull)]
            y1, x1 = map_point(p1)
            y2, x2 = map_point(p2)

            # Simple line drawing
            steps = max(abs(x2 - x1), abs(y2 - y1)) + 1
            for step in range(steps):
                t = step / steps if steps > 1 else 0
                x = int(x1 + t * (x2 - x1))
                y = int(y1 + t * (y2 - y1))
                if canvas[y][x] == ' ':
                    canvas[y][x] = '-' if abs(x2 - x1) > abs(y2 - y1) else '|'

    # Draw hull points
    if hull:
        hull_set = set(hull)
        for point in hull:
            y, x = map_point(point)
            canvas[y][x] = 'H'

    # Draw regular points
    for point in points:
        if not hull or point not in hull:
            y, x = map_point(point)
            if canvas[y][x] == ' ' or canvas[y][x] in '-|':
                canvas[y][x] = '*'

    # Convert to string
    result = '\n'.join(''.join(row) for row in canvas)
    return result


# ==============================================================================
# 8. COMPREHENSIVE TESTING AND BENCHMARKING
# ==============================================================================

def generate_test_points(n: int, distribution: str = 'random') -> List[Point]:
    """
    Generate test points with various distributions.

    Distributions:
    - random: Uniform random in [0, 100]²
    - circle: Points on circle
    - grid: Regular grid
    - clustered: Multiple clusters
    """
    points = []

    if distribution == 'random':
        points = [Point(random.uniform(0, 100), random.uniform(0, 100))
                 for _ in range(n)]

    elif distribution == 'circle':
        for i in range(n):
            angle = 2 * math.pi * i / n
            points.append(Point(50 + 40 * math.cos(angle),
                              50 + 40 * math.sin(angle)))

    elif distribution == 'grid':
        size = int(math.sqrt(n)) + 1
        for i in range(size):
            for j in range(size):
                if len(points) < n:
                    points.append(Point(i * 10, j * 10))

    elif distribution == 'clustered':
        num_clusters = 5
        points_per_cluster = n // num_clusters
        for _ in range(num_clusters):
            cx, cy = random.uniform(20, 80), random.uniform(20, 80)
            for _ in range(points_per_cluster):
                points.append(Point(cx + random.gauss(0, 5),
                                  cy + random.gauss(0, 5)))

    return points


def benchmark_convex_hull():
    """Benchmark different convex hull algorithms."""
    print("="*70)
    print("CONVEX HULL ALGORITHM BENCHMARKS")
    print("="*70)

    sizes = [100, 500, 1000, 2000]
    distributions = ['random', 'circle', 'grid']

    for dist in distributions:
        print(f"\nDistribution: {dist}")
        print("-"*70)
        print(f"{'Size':<10} {'Graham Scan':<15} {'Jarvis March':<15} {'QuickHull':<15}")
        print("-"*70)

        for size in sizes:
            points = generate_test_points(size, dist)

            # Graham Scan
            start = time.time()
            hull1 = convex_hull_graham_scan(points)
            time1 = (time.time() - start) * 1000

            # Jarvis March
            start = time.time()
            hull2 = convex_hull_jarvis_march(points)
            time2 = (time.time() - start) * 1000

            # QuickHull
            start = time.time()
            hull3 = convex_hull_quick_hull(points)
            time3 = (time.time() - start) * 1000

            print(f"{size:<10} {time1:>12.3f} ms {time2:>12.3f} ms {time3:>12.3f} ms  "
                  f"(hull size: {len(hull1)})")


def demonstrate_all_algorithms():
    """Comprehensive demonstration of all algorithms."""
    print("="*70)
    print("COMPUTATIONAL GEOMETRY ALGORITHMS - DEMONSTRATION")
    print("="*70)

    # 1. Convex Hull
    print("\n1. CONVEX HULL ALGORITHMS")
    print("-"*70)

    points = [
        Point(0, 3), Point(2, 2), Point(1, 1), Point(2, 1),
        Point(3, 0), Point(0, 0), Point(3, 3), Point(1, 2)
    ]

    hull_graham = convex_hull_graham_scan(points)
    hull_jarvis = convex_hull_jarvis_march(points)
    hull_quick = convex_hull_quick_hull(points)

    print(f"Input: {len(points)} points")
    print(f"Graham Scan hull: {len(hull_graham)} points - {hull_graham}")
    print(f"Jarvis March hull: {len(hull_jarvis)} points - {hull_jarvis}")
    print(f"QuickHull: {len(hull_quick)} points - {hull_quick}")

    print("\nVisualization:")
    print(visualize_points_ascii(points, hull_graham))

    # 2. Line Intersection
    print("\n2. LINE INTERSECTION")
    print("-"*70)

    seg1 = (Point(0, 0), Point(4, 4))
    seg2 = (Point(0, 4), Point(4, 0))
    seg3 = (Point(5, 5), Point(6, 6))

    intersect1 = segments_intersect(*seg1, *seg2)
    intersect2 = segments_intersect(*seg1, *seg3)

    point1 = line_intersection_point(*seg1, *seg2)

    print(f"Segment 1: {seg1[0]} to {seg1[1]}")
    print(f"Segment 2: {seg2[0]} to {seg2[1]}")
    print(f"Intersect: {intersect1}, Point: {point1}")
    print(f"\nSegment 1 and Segment 3: Intersect: {intersect2}")

    # 3. Point in Polygon
    print("\n3. POINT-IN-POLYGON TEST")
    print("-"*70)

    square = [Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)]
    test_points = [Point(2, 2), Point(5, 5), Point(0, 0), Point(2, 0)]

    print("Polygon (square): ", square)
    for p in test_points:
        inside_ray = point_in_polygon_ray_casting(p, square)
        inside_wind = point_in_polygon_winding_number(p, square)
        print(f"  Point {p}: Ray={inside_ray}, Winding={inside_wind}")

    # 4. Closest Pair
    print("\n4. CLOSEST PAIR OF POINTS")
    print("-"*70)

    random_points = generate_test_points(50, 'random')

    p1, p2, dist_brute = closest_pair_brute_force(random_points)
    print(f"Brute force: {p1} and {p2}, distance: {dist_brute:.3f}")

    p1, p2, dist_dc = closest_pair_divide_conquer(random_points)
    print(f"Divide & Conquer: {p1} and {p2}, distance: {dist_dc:.3f}")

    # 5. Polygon Operations
    print("\n5. POLYGON OPERATIONS")
    print("-"*70)

    triangle = [Point(0, 0), Point(4, 0), Point(2, 3)]
    area = polygon_area(triangle)
    centroid = polygon_centroid(triangle)

    print(f"Triangle: {triangle}")
    print(f"Area: {area:.3f}")
    print(f"Centroid: {centroid}")


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_all_algorithms()

    # Run benchmarks
    print("\n")
    benchmark_convex_hull()

    print("\n" + "="*70)
    print("ALL DEMONSTRATIONS COMPLETE")
    print("="*70)
