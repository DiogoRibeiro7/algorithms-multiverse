# Computational Geometry Algorithms

A comprehensive collection of computational geometry algorithms implemented across multiple programming languages with focus on correctness, robustness, and performance.

## Overview

Computational geometry is the study of algorithms for solving geometric problems. These algorithms are fundamental to computer graphics, geographic information systems (GIS), robotics, computer-aided design (CAD), and many other fields.

## Algorithms Implemented

### 1. Convex Hull Algorithms

The convex hull of a set of points is the smallest convex polygon that contains all the points.

#### Graham Scan
- **Time Complexity**: O(n log n)
- **Space Complexity**: O(n)
- **Approach**: Sort points by polar angle, then scan to build hull
- **Advantages**: Efficient for large point sets, simple to implement
- **Applications**: Pattern recognition, image processing, collision detection

#### Jarvis March (Gift Wrapping)
- **Time Complexity**: O(nh) where h is hull size
- **Space Complexity**: O(h)
- **Approach**: Start from leftmost point, wrap around selecting next hull point
- **Advantages**: Output-sensitive (good when h << n)
- **Applications**: When hull size is expected to be small

### 2. Line Intersection

Determining if and where two line segments intersect.

**Algorithms**:
- **Segment-Segment Intersection**: Uses cross products and orientation tests
- **Line-Line Intersection**: Finds intersection point of infinite lines
- **Bentley-Ottmann Algorithm**: Sweep line for multiple segment intersections

**Time Complexity**: O(1) for single pair, O((n+k)log n) for n segments with k intersections

**Applications**:
- CAD systems
- Map overlay in GIS
- Computer graphics rendering
- Robotics path planning

### 3. Point-in-Polygon Tests

Determine if a point lies inside, outside, or on the boundary of a polygon.

#### Ray Casting Algorithm
- **Time Complexity**: O(n) where n is number of vertices
- **Approach**: Cast ray from point, count edge crossings
- **Rule**: Odd crossings = inside, even = outside
- **Robust**: Handles most edge cases

#### Winding Number Algorithm
- **Time Complexity**: O(n)
- **Approach**: Count net number of times polygon winds around point
- **Advantages**: More robust for complex polygons
- **Applications**: Computer graphics, GIS queries

### 4. Closest Pair of Points

Find the two points with minimum Euclidean distance.

**Algorithms**:
- **Brute Force**: O(n²) - check all pairs
- **Divide and Conquer**: O(n log n) - recursively split and merge
- **Sweep Line**: O(n log n) - efficient practical implementation

**Applications**:
- Air traffic control (collision detection)
- Molecular modeling
- Data clustering
- Nearest neighbor search

### 5. Voronoi Diagrams

Partition of plane into regions based on distance to points.

**Properties**:
- Each region contains all points closer to one site than to any other
- Dual of Delaunay triangulation
- Has O(n) vertices and edges for n points

**Algorithms**:
- **Fortune's Algorithm**: O(n log n) sweep line algorithm
- **Incremental**: O(n²) simpler but slower
- **Divide and Conquer**: O(n log n) theoretical

**Applications**:
- Nearest neighbor queries
- Facility location
- Natural phenomena modeling
- Mesh generation

### 6. Triangulation Algorithms

Decompose polygon into triangles.

#### Ear Clipping Algorithm
- **Time Complexity**: O(n²) naive, O(n) with optimization
- **Approach**: Iteratively remove "ear" triangles
- **Works for**: Simple polygons (no holes)

#### Delaunay Triangulation
- **Time Complexity**: O(n log n) average
- **Properties**: Maximizes minimum angle, unique for point set
- **Applications**: Mesh generation, terrain modeling

**Applications**:
- 3D graphics and rendering
- Finite element analysis
- Terrain generation
- Texture mapping

## Language Implementations

### Python (`geometry.py`, `advanced_geometry.py`)
- Full implementation with visualization
- NumPy for efficient array operations
- Matplotlib for plotting (optional)
- ASCII art visualization
- Comprehensive docstrings and type hints

### C (`geometry.c`)
- High-performance implementation
- Manual memory management
- Optimized with compiler hints
- Robust floating-point handling
- Suitable for embedded systems

### Rust (`geometry.rs`)
- Memory-safe implementation
- Zero-cost abstractions
- Type-safe geometric primitives
- Excellent performance
- Iterator-based operations

### Fortran (`geometry.f90`)
- Modern Fortran 90+ features
- Optimized for numerical computation
- Array operations
- Scientific computing focus
- High performance for large datasets

### COBOL (`geometry.cob`)
- Enterprise applications
- Fixed-point arithmetic where appropriate
- Structured procedure divisions
- Business use cases (GIS, mapping)

### R (`geometry.R`)
- Statistical computing focus
- Visualization with base graphics or ggplot2
- Integration with spatial packages
- Data frame operations
- Geographic analysis

## Geometric Primitives

### 2D Primitives
- **Point**: (x, y) coordinates
- **Vector**: Direction and magnitude
- **Line Segment**: Defined by two endpoints
- **Polygon**: Closed sequence of line segments
- **Circle**: Center point and radius

### 3D Primitives (where applicable)
- **Point3D**: (x, y, z) coordinates
- **Vector3D**: 3D direction and magnitude
- **Plane**: Defined by point and normal vector
- **Triangle**: Three points in 3D space

## Floating-Point Precision Handling

Geometric computations are sensitive to floating-point errors. We employ several techniques:

### Epsilon Comparisons
```python
EPSILON = 1e-10

def float_equal(a, b):
    return abs(a - b) < EPSILON
```

### Exact Geometric Predicates
- Use integer arithmetic when possible
- Cross products instead of angles
- Determinant-based tests
- Avoid trigonometric functions

### Robust Orientation Test
```
orientation(p, q, r) = sign((q.x - p.x)(r.y - p.y) - (q.y - p.y)(r.x - p.x))
```

## Visualization

### ASCII Art (All Languages)
```
    *
   / \
  /   \
 *-----*
```

### Coordinate Output
Points, lines, and polygons can be output as coordinate lists for external visualization.

### Python Matplotlib (Optional)
```python
import matplotlib.pyplot as plt
plt.plot([p.x for p in hull], [p.y for p in hull])
plt.show()
```

## Performance Optimizations

### Spatial Data Structures
- **Quadtree**: Hierarchical space partitioning for 2D
- **KD-Tree**: k-dimensional binary space partitioning
- **Grid**: Uniform spatial hashing

### Algorithmic Optimizations
- **Sweep Line**: Process events in sorted order
- **Divide and Conquer**: Recursively split problems
- **Incremental**: Build solution step by step
- **Randomization**: Expected linear time for some problems

### Implementation Optimizations
- Cache locality: Keep related data together
- Branch prediction: Minimize conditional branches
- Vectorization: SIMD operations where possible
- Parallel processing: Multi-threaded for independent operations

## Edge Cases and Robustness

### Handled Edge Cases

1. **Collinear Points**: Three or more points on same line
2. **Duplicate Points**: Identical coordinates
3. **Degenerate Cases**:
   - Zero-length segments
   - Zero-area triangles
   - Single-point polygons
4. **Boundary Cases**: Points exactly on edges/vertices
5. **Numerical Precision**: Near-zero comparisons
6. **Empty/Small Inputs**: 0, 1, or 2 points

### Test Coverage
- Unit tests for each algorithm
- Property-based tests
- Stress tests with random data
- Known difficult configurations
- Real-world dataset tests

## Real-World Applications

### Computer Graphics
- **Rendering**: Hidden surface removal, clipping
- **Collision Detection**: Bounding volumes, intersection tests
- **Mesh Generation**: Triangulation, simplification
- **Ray Tracing**: Intersection calculations

### Geographic Information Systems (GIS)
- **Spatial Queries**: Point-in-polygon tests
- **Map Overlay**: Line intersection
- **Proximity Analysis**: Voronoi diagrams, nearest neighbor
- **Terrain Modeling**: Triangulation, contour lines

### Robotics
- **Path Planning**: Visibility graphs, convex decomposition
- **Motion Planning**: Configuration space obstacles
- **Sensor Processing**: Point cloud analysis
- **Localization**: Geometric feature matching

### Computer-Aided Design (CAD)
- **Solid Modeling**: Boolean operations
- **Mesh Processing**: Simplification, smoothing
- **Collision Detection**: Assembly validation
- **Tool Path Generation**: CNC machining

## Building and Running

### Python
```bash
python geometry.py
python advanced_geometry.py
```

### C
```bash
gcc -O3 -o geometry geometry.c -lm
./geometry
```

### Rust
```bash
rustc -O geometry.rs
./geometry
```

### Fortran
```bash
gfortran -O3 -o geometry geometry.f90
./geometry
```

### COBOL
```bash
cobc -x -free geometry.cob
./geometry
```

### R
```bash
Rscript geometry.R
```

## Testing

Comprehensive test suite included:
```bash
python test_geometry.py
```

Tests include:
- Basic functionality tests
- Edge case validation
- Performance benchmarks
- Numerical stability tests
- Comparison across implementations

## Complexity Summary

| Algorithm | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Graham Scan | O(n log n) | O(n) |
| Jarvis March | O(nh) | O(h) |
| Line Intersection | O(1) | O(1) |
| Point-in-Polygon | O(n) | O(1) |
| Closest Pair (D&C) | O(n log n) | O(n) |
| Voronoi (Fortune) | O(n log n) | O(n) |
| Ear Clipping | O(n²) | O(n) |

## Mathematical Foundations

### Cross Product (2D)
```
(p2 - p1) × (p3 - p1) = (x2-x1)(y3-y1) - (y2-y1)(x3-x1)
```
- Positive: Counter-clockwise turn
- Negative: Clockwise turn
- Zero: Collinear

### Distance Formulas
- **Euclidean**: sqrt((x2-x1)² + (y2-y1)²)
- **Manhattan**: |x2-x1| + |y2-y1|
- **Squared**: (x2-x1)² + (y2-y1)² (avoids sqrt for comparisons)

### Orientation Test
Given three points p, q, r:
```
orientation = sign(det([q.x-p.x, r.x-p.x],
                       [q.y-p.y, r.y-p.y]))
```

## References

- *Computational Geometry: Algorithms and Applications* by de Berg et al.
- *Introduction to Algorithms* (CLRS), Chapter 33: Computational Geometry
- *Computational Geometry in C* by O'Rourke
- *Geometric Tools for Computer Graphics* by Schneider & Eberly

## License

Part of the algorithms-multiverse repository. See root LICENSE file.

## Contributing

When adding new algorithms:
1. Implement with proper documentation
2. Add comprehensive tests including edge cases
3. Verify numerical stability
4. Benchmark performance
5. Update this README
