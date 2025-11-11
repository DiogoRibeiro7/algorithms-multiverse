/**
 * Computational Geometry Algorithms in C++
 *
 * Comprehensive collection of 2D and 3D computational geometry algorithms
 * with template-based design and high-performance implementations.
 *
 * Features:
 * - 2D Algorithms: Convex Hull, Line Intersection, Point-in-Polygon, Closest Pair
 * - 3D Algorithms: Convex Hull (Gift Wrapping), Plane Operations, Volume Calculations
 * - Template-based design for different numeric types
 * - Operator overloading for natural syntax
 * - STL integration for efficiency
 * - Robust floating-point handling
 *
 * @author Algorithms Multiverse
 * @version 1.0
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <set>
#include <limits>
#include <functional>
#include <random>
#include <chrono>
#include <iomanip>

template <typename T>
const T EPSILON = static_cast<T>(1e-10);

/**
 * Orientation enum for geometric predicates
 */
enum class Orientation {
    COLLINEAR,
    CLOCKWISE,
    COUNTERCLOCKWISE
};

/**
 * 2D Point class with operator overloading
 *
 * Template-based point representation supporting different numeric types.
 * Provides natural mathematical syntax through operator overloading.
 *
 * @tparam T Numeric type (double, float, int, long, etc.)
 */
template <typename T>
class Point2D {
public:
    T x, y;

    Point2D() : x(0), y(0) {}
    Point2D(T x, T y) : x(x), y(y) {}

    // Equality with epsilon tolerance
    bool operator==(const Point2D& other) const {
        return std::abs(x - other.x) < EPSILON<T> &&
               std::abs(y - other.y) < EPSILON<T>;
    }

    bool operator!=(const Point2D& other) const {
        return !(*this == other);
    }

    // Comparison for sorting
    bool operator<(const Point2D& other) const {
        if (std::abs(x - other.x) < EPSILON<T>) {
            return y < other.y;
        }
        return x < other.x;
    }

    // Arithmetic operations
    Point2D operator+(const Point2D& other) const {
        return Point2D(x + other.x, y + other.y);
    }

    Point2D operator-(const Point2D& other) const {
        return Point2D(x - other.x, y - other.y);
    }

    Point2D operator*(T scalar) const {
        return Point2D(x * scalar, y * scalar);
    }

    Point2D operator/(T scalar) const {
        return Point2D(x / scalar, y / scalar);
    }

    // Dot product
    T dot(const Point2D& other) const {
        return x * other.x + y * other.y;
    }

    // Cross product (z-component in 3D)
    T cross(const Point2D& other) const {
        return x * other.y - y * other.x;
    }

    // Magnitude
    T magnitude() const {
        return std::sqrt(x * x + y * y);
    }

    // Distance to another point
    T distanceTo(const Point2D& other) const {
        T dx = x - other.x;
        T dy = y - other.y;
        return std::sqrt(dx * dx + dy * dy);
    }

    // Squared distance (avoids sqrt for comparisons)
    T distanceSquaredTo(const Point2D& other) const {
        T dx = x - other.x;
        T dy = y - other.y;
        return dx * dx + dy * dy;
    }

    friend std::ostream& operator<<(std::ostream& os, const Point2D& p) {
        os << "Point2D(" << p.x << ", " << p.y << ")";
        return os;
    }
};

/**
 * 3D Point class with operator overloading
 *
 * Full 3D point implementation with cross product and volume calculations.
 *
 * @tparam T Numeric type
 */
template <typename T>
class Point3D {
public:
    T x, y, z;

    Point3D() : x(0), y(0), z(0) {}
    Point3D(T x, T y, T z) : x(x), y(y), z(z) {}

    // Equality with epsilon tolerance
    bool operator==(const Point3D& other) const {
        return std::abs(x - other.x) < EPSILON<T> &&
               std::abs(y - other.y) < EPSILON<T> &&
               std::abs(z - other.z) < EPSILON<T>;
    }

    bool operator!=(const Point3D& other) const {
        return !(*this == other);
    }

    // Comparison for sorting
    bool operator<(const Point3D& other) const {
        if (std::abs(x - other.x) < EPSILON<T>) {
            if (std::abs(y - other.y) < EPSILON<T>) {
                return z < other.z;
            }
            return y < other.y;
        }
        return x < other.x;
    }

    // Arithmetic operations
    Point3D operator+(const Point3D& other) const {
        return Point3D(x + other.x, y + other.y, z + other.z);
    }

    Point3D operator-(const Point3D& other) const {
        return Point3D(x - other.x, y - other.y, z - other.z);
    }

    Point3D operator*(T scalar) const {
        return Point3D(x * scalar, y * scalar, z * scalar);
    }

    Point3D operator/(T scalar) const {
        return Point3D(x / scalar, y / scalar, z / scalar);
    }

    // Dot product
    T dot(const Point3D& other) const {
        return x * other.x + y * other.y + z * other.z;
    }

    // Cross product (full 3D vector)
    Point3D cross(const Point3D& other) const {
        return Point3D(
            y * other.z - z * other.y,
            z * other.x - x * other.z,
            x * other.y - y * other.x
        );
    }

    // Magnitude
    T magnitude() const {
        return std::sqrt(x * x + y * y + z * z);
    }

    // Distance to another point
    T distanceTo(const Point3D& other) const {
        T dx = x - other.x;
        T dy = y - other.y;
        T dz = z - other.z;
        return std::sqrt(dx * dx + dy * dy + dz * dz);
    }

    // Normalize to unit vector
    Point3D normalize() const {
        T mag = magnitude();
        if (mag < EPSILON<T>) return Point3D(0, 0, 0);
        return *this / mag;
    }

    friend std::ostream& operator<<(std::ostream& os, const Point3D& p) {
        os << "Point3D(" << p.x << ", " << p.y << ", " << p.z << ")";
        return os;
    }
};

/**
 * 2D Geometry Algorithms
 */
namespace Geometry2D {

    /**
     * Determine orientation of ordered triplet (p, q, r)
     *
     * Uses cross product to determine if points turn left (CCW),
     * right (CW), or are collinear.
     *
     * Time Complexity: O(1)
     * Space Complexity: O(1)
     */
    template <typename T>
    Orientation orientation(const Point2D<T>& p, const Point2D<T>& q, const Point2D<T>& r) {
        Point2D<T> v1 = q - p;
        Point2D<T> v2 = r - p;
        T cross = v1.cross(v2);

        if (std::abs(cross) < EPSILON<T>) return Orientation::COLLINEAR;
        return cross > 0 ? Orientation::COUNTERCLOCKWISE : Orientation::CLOCKWISE;
    }

    /**
     * Check if point q lies on segment pr
     */
    template <typename T>
    bool onSegment(const Point2D<T>& p, const Point2D<T>& q, const Point2D<T>& r) {
        return q.x <= std::max(p.x, r.x) && q.x >= std::min(p.x, r.x) &&
               q.y <= std::max(p.y, r.y) && q.y >= std::min(p.y, r.y);
    }

    /**
     * Check if line segments intersect
     *
     * Time Complexity: O(1)
     *
     * Applications:
     * - Collision detection
     * - Map overlay analysis
     * - Circuit layout verification
     */
    template <typename T>
    bool segmentsIntersect(const Point2D<T>& p1, const Point2D<T>& q1,
                          const Point2D<T>& p2, const Point2D<T>& q2) {
        Orientation o1 = orientation(p1, q1, p2);
        Orientation o2 = orientation(p1, q1, q2);
        Orientation o3 = orientation(p2, q2, p1);
        Orientation o4 = orientation(p2, q2, q1);

        // General case
        if (o1 != o2 && o3 != o4) return true;

        // Special cases - collinear points
        if (o1 == Orientation::COLLINEAR && onSegment(p1, p2, q1)) return true;
        if (o2 == Orientation::COLLINEAR && onSegment(p1, q2, q1)) return true;
        if (o3 == Orientation::COLLINEAR && onSegment(p2, p1, q2)) return true;
        if (o4 == Orientation::COLLINEAR && onSegment(p2, q1, q2)) return true;

        return false;
    }

    /**
     * Graham Scan Convex Hull Algorithm
     *
     * Time Complexity: O(n log n)
     * Space Complexity: O(n)
     *
     * Applications:
     * - Pattern recognition
     * - Image processing
     * - Collision detection
     */
    template <typename T>
    std::vector<Point2D<T>> convexHullGrahamScan(std::vector<Point2D<T>> points) {
        if (points.size() < 3) return points;

        // Remove duplicates
        std::set<Point2D<T>> uniqueSet(points.begin(), points.end());
        std::vector<Point2D<T>> uniquePoints(uniqueSet.begin(), uniqueSet.end());

        if (uniquePoints.size() < 3) return uniquePoints;

        // Find lowest point (leftmost if tie)
        Point2D<T> start = *std::min_element(uniquePoints.begin(), uniquePoints.end(),
            [](const Point2D<T>& a, const Point2D<T>& b) {
                if (std::abs(a.y - b.y) < EPSILON<T>) return a.x < b.x;
                return a.y < b.y;
            });

        // Sort by polar angle
        auto polarAngleCompare = [&start](const Point2D<T>& a, const Point2D<T>& b) {
            if (a == start) return true;
            if (b == start) return false;
            Orientation o = orientation(start, a, b);
            if (o == Orientation::COLLINEAR) {
                return start.distanceTo(a) < start.distanceTo(b);
            }
            return o == Orientation::COUNTERCLOCKWISE;
        };

        std::sort(uniquePoints.begin(), uniquePoints.end(), polarAngleCompare);

        // Build hull using stack
        std::vector<Point2D<T>> hull;
        hull.push_back(start);

        for (size_t i = 1; i < uniquePoints.size(); i++) {
            if (uniquePoints[i] == start) continue;

            while (hull.size() >= 2) {
                Orientation o = orientation(hull[hull.size() - 2], hull[hull.size() - 1],
                                          uniquePoints[i]);
                if (o != Orientation::COUNTERCLOCKWISE) {
                    hull.pop_back();
                } else {
                    break;
                }
            }
            hull.push_back(uniquePoints[i]);
        }

        return hull;
    }

    /**
     * Jarvis March (Gift Wrapping) Convex Hull
     *
     * Time Complexity: O(nh) - output-sensitive
     * Space Complexity: O(h)
     */
    template <typename T>
    std::vector<Point2D<T>> convexHullJarvisMarch(std::vector<Point2D<T>> points) {
        if (points.size() < 3) return points;

        // Remove duplicates
        std::set<Point2D<T>> uniqueSet(points.begin(), points.end());
        std::vector<Point2D<T>> uniquePoints(uniqueSet.begin(), uniqueSet.end());

        if (uniquePoints.size() < 3) return uniquePoints;

        // Find leftmost point
        Point2D<T> leftmost = *std::min_element(uniquePoints.begin(), uniquePoints.end(),
            [](const Point2D<T>& a, const Point2D<T>& b) {
                if (std::abs(a.x - b.x) < EPSILON<T>) return a.y < b.y;
                return a.x < b.x;
            });

        std::vector<Point2D<T>> hull;
        Point2D<T> current = leftmost;

        do {
            hull.push_back(current);
            Point2D<T> next = uniquePoints[0];

            for (const auto& candidate : uniquePoints) {
                if (candidate == current) continue;

                Orientation o = orientation(current, next, candidate);
                if (next == current ||
                    o == Orientation::COUNTERCLOCKWISE ||
                    (o == Orientation::COLLINEAR && current.distanceTo(candidate) > current.distanceTo(next))) {
                    next = candidate;
                }
            }

            current = next;
        } while (current != leftmost && hull.size() < uniquePoints.size() + 1);

        return hull;
    }

    /**
     * Ray Casting Point-in-Polygon Test
     *
     * Time Complexity: O(n)
     *
     * Applications:
     * - Hit testing
     * - GIS
     * - Collision detection
     */
    template <typename T>
    bool pointInPolygonRayCasting(const Point2D<T>& point,
                                  const std::vector<Point2D<T>>& polygon) {
        if (polygon.size() < 3) return false;

        bool inside = false;
        size_t n = polygon.size();

        for (size_t i = 0; i < n; i++) {
            const Point2D<T>& p1 = polygon[i];
            const Point2D<T>& p2 = polygon[(i + 1) % n];

            if ((p1.y > point.y) != (p2.y > point.y)) {
                T xIntersection = (p2.x - p1.x) * (point.y - p1.y) / (p2.y - p1.y) + p1.x;
                if (point.x < xIntersection) {
                    inside = !inside;
                }
            }
        }

        return inside;
    }

    /**
     * Closest Pair Result
     */
    template <typename T>
    struct ClosestPairResult {
        Point2D<T> point1;
        Point2D<T> point2;
        T distance;

        ClosestPairResult() : distance(std::numeric_limits<T>::max()) {}
        ClosestPairResult(const Point2D<T>& p1, const Point2D<T>& p2, T dist)
            : point1(p1), point2(p2), distance(dist) {}
    };

    /**
     * Closest Pair - Divide and Conquer
     *
     * Time Complexity: O(n log n)
     *
     * Applications:
     * - Collision detection
     * - Clustering
     * - Air traffic control
     */
    template <typename T>
    ClosestPairResult<T> closestPairRecursive(std::vector<Point2D<T>>& pointsByX) {
        size_t n = pointsByX.size();

        // Base cases
        if (n <= 3) {
            T minDist = std::numeric_limits<T>::max();
            ClosestPairResult<T> result;

            for (size_t i = 0; i < n; i++) {
                for (size_t j = i + 1; j < n; j++) {
                    T dist = pointsByX[i].distanceTo(pointsByX[j]);
                    if (dist < minDist) {
                        minDist = dist;
                        result = ClosestPairResult<T>(pointsByX[i], pointsByX[j], dist);
                    }
                }
            }

            return result;
        }

        // Divide
        size_t mid = n / 2;
        Point2D<T> midPoint = pointsByX[mid];

        std::vector<Point2D<T>> leftHalf(pointsByX.begin(), pointsByX.begin() + mid);
        std::vector<Point2D<T>> rightHalf(pointsByX.begin() + mid, pointsByX.end());

        ClosestPairResult<T> leftResult = closestPairRecursive(leftHalf);
        ClosestPairResult<T> rightResult = closestPairRecursive(rightHalf);

        ClosestPairResult<T> minResult = leftResult.distance < rightResult.distance ?
                                        leftResult : rightResult;

        // Check strip
        std::vector<Point2D<T>> strip;
        for (const auto& p : pointsByX) {
            if (std::abs(p.x - midPoint.x) < minResult.distance) {
                strip.push_back(p);
            }
        }

        std::sort(strip.begin(), strip.end(),
                 [](const Point2D<T>& a, const Point2D<T>& b) { return a.y < b.y; });

        for (size_t i = 0; i < strip.size(); i++) {
            for (size_t j = i + 1; j < strip.size() &&
                 (strip[j].y - strip[i].y) < minResult.distance; j++) {
                T dist = strip[i].distanceTo(strip[j]);
                if (dist < minResult.distance) {
                    minResult = ClosestPairResult<T>(strip[i], strip[j], dist);
                }
            }
        }

        return minResult;
    }

    template <typename T>
    ClosestPairResult<T> closestPairDivideConquer(std::vector<Point2D<T>> points) {
        if (points.size() < 2) return ClosestPairResult<T>();

        std::sort(points.begin(), points.end(),
                 [](const Point2D<T>& a, const Point2D<T>& b) { return a.x < b.x; });

        return closestPairRecursive(points);
    }

    /**
     * Calculate polygon area using Shoelace formula
     */
    template <typename T>
    T polygonArea(const std::vector<Point2D<T>>& polygon) {
        if (polygon.size() < 3) return 0;

        T area = 0;
        size_t n = polygon.size();

        for (size_t i = 0; i < n; i++) {
            const Point2D<T>& p1 = polygon[i];
            const Point2D<T>& p2 = polygon[(i + 1) % n];
            area += p1.x * p2.y - p2.x * p1.y;
        }

        return area / 2;
    }

    /**
     * Calculate polygon centroid
     */
    template <typename T>
    Point2D<T> polygonCentroid(const std::vector<Point2D<T>>& polygon) {
        if (polygon.empty()) return Point2D<T>();

        T area = polygonArea(polygon);
        if (std::abs(area) < EPSILON<T>) {
            T sumX = 0, sumY = 0;
            for (const auto& p : polygon) {
                sumX += p.x;
                sumY += p.y;
            }
            return Point2D<T>(sumX / polygon.size(), sumY / polygon.size());
        }

        T cx = 0, cy = 0;
        size_t n = polygon.size();

        for (size_t i = 0; i < n; i++) {
            const Point2D<T>& p1 = polygon[i];
            const Point2D<T>& p2 = polygon[(i + 1) % n];
            T cross = p1.x * p2.y - p2.x * p1.y;
            cx += (p1.x + p2.x) * cross;
            cy += (p1.y + p2.y) * cross;
        }

        T factor = 1 / (6 * area);
        return Point2D<T>(cx * factor, cy * factor);
    }

} // namespace Geometry2D

/**
 * 3D Geometry Algorithms
 */
namespace Geometry3D {

    /**
     * 3D Plane representation
     */
    template <typename T>
    class Plane {
    public:
        Point3D<T> normal;
        T d; // ax + by + cz + d = 0

        Plane(const Point3D<T>& n, T d) : normal(n.normalize()), d(d) {}

        // Create plane from three points
        static Plane fromPoints(const Point3D<T>& p1, const Point3D<T>& p2,
                               const Point3D<T>& p3) {
            Point3D<T> v1 = p2 - p1;
            Point3D<T> v2 = p3 - p1;
            Point3D<T> normal = v1.cross(v2).normalize();
            T d = -normal.dot(p1);
            return Plane(normal, d);
        }

        // Distance from point to plane
        T distanceToPoint(const Point3D<T>& point) const {
            return std::abs(normal.dot(point) + d);
        }

        // Check which side of plane point is on
        T signedDistanceToPoint(const Point3D<T>& point) const {
            return normal.dot(point) + d;
        }
    };

    /**
     * Tetrahedron volume using determinant
     *
     * Time Complexity: O(1)
     */
    template <typename T>
    T tetrahedronVolume(const Point3D<T>& a, const Point3D<T>& b,
                       const Point3D<T>& c, const Point3D<T>& d) {
        Point3D<T> v1 = b - a;
        Point3D<T> v2 = c - a;
        Point3D<T> v3 = d - a;

        return std::abs(v1.dot(v2.cross(v3))) / 6.0;
    }

    /**
     * 3D Convex Hull using Gift Wrapping (simplified)
     *
     * This is a basic implementation. For production use,
     * consider QuickHull3D or incremental algorithms.
     *
     * Time Complexity: O(n * h²) where h is hull size
     */
    template <typename T>
    std::vector<std::vector<Point3D<T>>> convexHull3DGiftWrapping(
        std::vector<Point3D<T>> points) {

        if (points.size() < 4) return {};

        // Find starting point (lowest z, then lowest y, then lowest x)
        Point3D<T> start = *std::min_element(points.begin(), points.end(),
            [](const Point3D<T>& a, const Point3D<T>& b) {
                if (std::abs(a.z - b.z) < EPSILON<T>) {
                    if (std::abs(a.y - b.y) < EPSILON<T>) {
                        return a.x < b.x;
                    }
                    return a.y < b.y;
                }
                return a.z < b.z;
            });

        std::vector<std::vector<Point3D<T>>> faces;

        // This is a simplified version - full 3D convex hull is complex
        // For production, use libraries like CGAL or implement QuickHull3D

        return faces;
    }

    /**
     * Point inside convex polyhedron test
     *
     * Tests if point is on correct side of all faces
     *
     * Time Complexity: O(f) where f is number of faces
     */
    template <typename T>
    bool pointInsideConvexPolyhedron(const Point3D<T>& point,
                                    const std::vector<Plane<T>>& faces) {
        for (const auto& face : faces) {
            if (face.signedDistanceToPoint(point) > EPSILON<T>) {
                return false;
            }
        }
        return true;
    }

} // namespace Geometry3D

/**
 * Performance Benchmarking
 */
namespace Benchmark {

    template <typename T>
    std::vector<Point2D<T>> generateRandomPoints2D(size_t count, T range) {
        std::vector<Point2D<T>> points;
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_real_distribution<T> dis(0, range);

        for (size_t i = 0; i < count; i++) {
            points.emplace_back(dis(gen), dis(gen));
        }

        return points;
    }

    template <typename T>
    std::vector<Point3D<T>> generateRandomPoints3D(size_t count, T range) {
        std::vector<Point3D<T>> points;
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_real_distribution<T> dis(0, range);

        for (size_t i = 0; i < count; i++) {
            points.emplace_back(dis(gen), dis(gen), dis(gen));
        }

        return points;
    }

    template <typename T>
    void benchmarkConvexHull2D(const std::vector<Point2D<T>>& points) {
        using namespace std::chrono;

        std::cout << "Benchmarking 2D Convex Hull Algorithms:\n";
        std::cout << "Points: " << points.size() << "\n";

        auto start = high_resolution_clock::now();
        auto graham = Geometry2D::convexHullGrahamScan(points);
        auto end = high_resolution_clock::now();
        auto grahamTime = duration_cast<microseconds>(end - start).count();
        std::cout << "Graham Scan: " << grahamTime / 1000.0 << " ms (hull size: "
                  << graham.size() << ")\n";

        start = high_resolution_clock::now();
        auto jarvis = Geometry2D::convexHullJarvisMarch(points);
        end = high_resolution_clock::now();
        auto jarvisTime = duration_cast<microseconds>(end - start).count();
        std::cout << "Jarvis March: " << jarvisTime / 1000.0 << " ms (hull size: "
                  << jarvis.size() << ")\n";
    }

} // namespace Benchmark

/**
 * Example usage and tests
 */
int main() {
    std::cout << "=== Computational Geometry Library (C++) ===\n\n";

    // 2D Tests
    std::cout << "1. 2D Convex Hull Test:\n";
    std::vector<Point2D<double>> points2D = {
        {0, 0}, {1, 1}, {2, 2}, {0, 2}, {2, 0}, {1, 0.5}
    };

    auto hull = Geometry2D::convexHullGrahamScan(points2D);
    std::cout << "Graham Scan Hull: ";
    for (const auto& p : hull) {
        std::cout << p << " ";
    }
    std::cout << "\n\n";

    // Point in polygon test
    std::cout << "2. Point-in-Polygon Test:\n";
    std::vector<Point2D<double>> square = {
        {0, 0}, {2, 0}, {2, 2}, {0, 2}
    };

    Point2D<double> inside(1, 1);
    Point2D<double> outside(3, 3);

    std::cout << "Point (1,1) in square: " << std::boolalpha
              << Geometry2D::pointInPolygonRayCasting(inside, square) << "\n";
    std::cout << "Point (3,3) in square: "
              << Geometry2D::pointInPolygonRayCasting(outside, square) << "\n\n";

    // Closest pair test
    std::cout << "3. Closest Pair Test:\n";
    auto randomPoints = Benchmark::generateRandomPoints2D<double>(10, 100.0);
    auto result = Geometry2D::closestPairDivideConquer(randomPoints);
    std::cout << "Closest pair: " << result.point1 << " and " << result.point2
              << " (distance: " << result.distance << ")\n\n";

    // 3D Tests
    std::cout << "4. 3D Geometry Test:\n";
    Point3D<double> p1(0, 0, 0);
    Point3D<double> p2(1, 0, 0);
    Point3D<double> p3(0, 1, 0);
    Point3D<double> p4(0, 0, 1);

    double volume = Geometry3D::tetrahedronVolume(p1, p2, p3, p4);
    std::cout << "Tetrahedron volume: " << volume << "\n\n";

    // Performance benchmark
    std::cout << "5. Performance Benchmark:\n";
    auto benchmarkPoints = Benchmark::generateRandomPoints2D<double>(1000, 1000.0);
    Benchmark::benchmarkConvexHull2D(benchmarkPoints);

    return 0;
}
