/**
 * Computational Geometry Algorithms in Java
 *
 * Comprehensive collection of 2D computational geometry algorithms with
 * robust geometric predicates and exact arithmetic support.
 *
 * Features:
 * - Convex Hull: Graham Scan, Jarvis March, QuickHull
 * - Line Operations: Intersection, orientation tests
 * - Point-in-Polygon: Ray casting, winding number
 * - Closest Pair: Divide and conquer
 * - Polygon Operations: Area, centroid, perimeter
 * - Robust Predicates: Epsilon-based comparisons and exact arithmetic
 *
 * @author Algorithms Multiverse
 * @version 1.0
 */

import java.util.*;
import java.math.BigDecimal;
import java.math.MathContext;

public class ComputationalGeometry {

    private static final double EPSILON = 1e-10;

    /**
     * Orientation enum for geometric predicates
     */
    public enum Orientation {
        COLLINEAR,
        CLOCKWISE,
        COUNTERCLOCKWISE
    }

    /**
     * 2D Point class with robust floating-point comparison
     *
     * Immutable point representation with epsilon-based equality
     * for robust geometric computations.
     */
    public static class Point implements Comparable<Point> {
        public final double x;
        public final double y;

        public Point(double x, double y) {
            this.x = x;
            this.y = y;
        }

        /**
         * Check equality with epsilon tolerance
         */
        public boolean equals(Point other) {
            return Math.abs(this.x - other.x) < EPSILON &&
                   Math.abs(this.y - other.y) < EPSILON;
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null || getClass() != obj.getClass()) return false;
            Point other = (Point) obj;
            return equals(other);
        }

        @Override
        public int hashCode() {
            long xHash = Math.round(x / EPSILON);
            long yHash = Math.round(y / EPSILON);
            return Objects.hash(xHash, yHash);
        }

        /**
         * Natural ordering by x, then y
         */
        @Override
        public int compareTo(Point other) {
            if (Math.abs(this.x - other.x) < EPSILON) {
                return Double.compare(this.y, other.y);
            }
            return Double.compare(this.x, other.x);
        }

        /**
         * Add vector to point
         */
        public Point add(Point other) {
            return new Point(this.x + other.x, this.y + other.y);
        }

        /**
         * Subtract to create vector
         */
        public Point subtract(Point other) {
            return new Point(this.x - other.x, this.y - other.y);
        }

        /**
         * Dot product
         */
        public double dot(Point other) {
            return this.x * other.x + this.y * other.y;
        }

        /**
         * Cross product (z-component in 3D)
         */
        public double cross(Point other) {
            return this.x * other.y - this.y * other.x;
        }

        /**
         * Distance from origin
         */
        public double magnitude() {
            return Math.sqrt(x * x + y * y);
        }

        /**
         * Distance to another point
         */
        public double distanceTo(Point other) {
            double dx = this.x - other.x;
            double dy = this.y - other.y;
            return Math.sqrt(dx * dx + dy * dy);
        }

        /**
         * Squared distance (avoids sqrt for comparisons)
         */
        public double distanceSquaredTo(Point other) {
            double dx = this.x - other.x;
            double dy = this.y - other.y;
            return dx * dx + dy * dy;
        }

        @Override
        public String toString() {
            return String.format("Point(%.3f, %.3f)", x, y);
        }
    }

    /**
     * Robust geometric predicates using exact arithmetic
     *
     * For critical applications where floating-point errors are unacceptable,
     * these methods use BigDecimal for exact computation.
     */
    public static class RobustPredicates {
        private static final MathContext MC = MathContext.DECIMAL128;

        /**
         * Exact orientation test using BigDecimal
         *
         * More robust than floating-point for nearly-collinear points
         */
        public static Orientation orientationExact(Point p, Point q, Point r) {
            BigDecimal px = new BigDecimal(p.x, MC);
            BigDecimal py = new BigDecimal(p.y, MC);
            BigDecimal qx = new BigDecimal(q.x, MC);
            BigDecimal qy = new BigDecimal(q.y, MC);
            BigDecimal rx = new BigDecimal(r.x, MC);
            BigDecimal ry = new BigDecimal(r.y, MC);

            // Calculate (q - p) × (r - p)
            BigDecimal v1x = qx.subtract(px, MC);
            BigDecimal v1y = qy.subtract(py, MC);
            BigDecimal v2x = rx.subtract(px, MC);
            BigDecimal v2y = ry.subtract(py, MC);

            BigDecimal cross = v1x.multiply(v2y, MC).subtract(v1y.multiply(v2x, MC), MC);

            int sign = cross.compareTo(BigDecimal.ZERO);
            if (sign == 0) return Orientation.COLLINEAR;
            return sign > 0 ? Orientation.COUNTERCLOCKWISE : Orientation.CLOCKWISE;
        }

        /**
         * Exact incircle test
         *
         * Tests if point d is inside the circle defined by points a, b, c
         * Critical for Delaunay triangulation
         */
        public static boolean inCircleExact(Point a, Point b, Point c, Point d) {
            BigDecimal ax = new BigDecimal(a.x, MC);
            BigDecimal ay = new BigDecimal(a.y, MC);
            BigDecimal bx = new BigDecimal(b.x, MC);
            BigDecimal by = new BigDecimal(b.y, MC);
            BigDecimal cx = new BigDecimal(c.x, MC);
            BigDecimal cy = new BigDecimal(c.y, MC);
            BigDecimal dx = new BigDecimal(d.x, MC);
            BigDecimal dy = new BigDecimal(d.y, MC);

            BigDecimal adx = ax.subtract(dx, MC);
            BigDecimal ady = ay.subtract(dy, MC);
            BigDecimal bdx = bx.subtract(dx, MC);
            BigDecimal bdy = by.subtract(dy, MC);
            BigDecimal cdx = cx.subtract(dx, MC);
            BigDecimal cdy = cy.subtract(dy, MC);

            BigDecimal abdet = adx.multiply(bdy, MC).subtract(bdx.multiply(ady, MC), MC);
            BigDecimal bcdet = bdx.multiply(cdy, MC).subtract(cdx.multiply(bdy, MC), MC);
            BigDecimal cadet = cdx.multiply(ady, MC).subtract(adx.multiply(cdy, MC), MC);

            BigDecimal alift = adx.multiply(adx, MC).add(ady.multiply(ady, MC), MC);
            BigDecimal blift = bdx.multiply(bdx, MC).add(bdy.multiply(bdy, MC), MC);
            BigDecimal clift = cdx.multiply(cdx, MC).add(cdy.multiply(cdy, MC), MC);

            BigDecimal det = alift.multiply(bcdet, MC)
                            .add(blift.multiply(cadet, MC), MC)
                            .add(clift.multiply(abdet, MC), MC);

            return det.compareTo(BigDecimal.ZERO) > 0;
        }
    }

    /**
     * Determine orientation of ordered triplet (p, q, r)
     *
     * Uses cross product to determine if points turn left (CCW),
     * right (CW), or are collinear.
     *
     * Time Complexity: O(1)
     * Space Complexity: O(1)
     *
     * @param p First point
     * @param q Second point
     * @param r Third point
     * @return Orientation constant
     */
    public static Orientation orientation(Point p, Point q, Point r) {
        Point v1 = q.subtract(p);
        Point v2 = r.subtract(p);
        double cross = v1.cross(v2);

        if (Math.abs(cross) < EPSILON) return Orientation.COLLINEAR;
        return cross > 0 ? Orientation.COUNTERCLOCKWISE : Orientation.CLOCKWISE;
    }

    /**
     * Check if point q lies on segment pr
     *
     * Assumes collinearity has been verified.
     */
    public static boolean onSegment(Point p, Point q, Point r) {
        return q.x <= Math.max(p.x, r.x) && q.x >= Math.min(p.x, r.x) &&
               q.y <= Math.max(p.y, r.y) && q.y >= Math.min(p.y, r.y);
    }

    /**
     * Check if line segments intersect
     *
     * Uses orientation tests to determine if segments (p1,q1) and (p2,q2)
     * intersect. Handles general and special cases.
     *
     * Time Complexity: O(1)
     * Space Complexity: O(1)
     *
     * Applications:
     * - Collision detection in games
     * - Map overlay analysis in GIS
     * - Circuit layout verification
     *
     * @param p1 First segment start
     * @param q1 First segment end
     * @param p2 Second segment start
     * @param q2 Second segment end
     * @return true if segments intersect
     */
    public static boolean segmentsIntersect(Point p1, Point q1, Point p2, Point q2) {
        Orientation o1 = orientation(p1, q1, p2);
        Orientation o2 = orientation(p1, q1, q2);
        Orientation o3 = orientation(p2, q2, p1);
        Orientation o4 = orientation(p2, q2, q1);

        // General case
        if (o1 != o2 && o3 != o4) return true;

        // Special cases - collinear points
        if (o1 == Orientation.COLLINEAR && onSegment(p1, p2, q1)) return true;
        if (o2 == Orientation.COLLINEAR && onSegment(p1, q2, q1)) return true;
        if (o3 == Orientation.COLLINEAR && onSegment(p2, p1, q2)) return true;
        if (o4 == Orientation.COLLINEAR && onSegment(p2, q1, q2)) return true;

        return false;
    }

    /**
     * Graham Scan Convex Hull Algorithm
     *
     * Finds convex hull using sorting and stack-based approach.
     *
     * Algorithm:
     * 1. Find lowest point (leftmost if tie)
     * 2. Sort by polar angle from lowest point
     * 3. Use stack to maintain hull vertices
     * 4. For each point, remove points that make right turn
     *
     * Time Complexity: O(n log n) - dominated by sorting
     * Space Complexity: O(n) - for hull storage
     *
     * Advantages:
     * - Fast for most distributions
     * - Simple to implement
     * - Predictable performance
     *
     * Applications:
     * - Pattern recognition
     * - Image processing
     * - Collision detection
     *
     * @param points Array of points
     * @return List of convex hull vertices in CCW order
     */
    public static List<Point> convexHullGrahamScan(List<Point> points) {
        if (points.size() < 3) return new ArrayList<>(points);

        // Remove duplicates
        Set<Point> uniqueSet = new LinkedHashSet<>(points);
        List<Point> uniquePoints = new ArrayList<>(uniqueSet);

        if (uniquePoints.size() < 3) return uniquePoints;

        // Find lowest point (leftmost if tie)
        Point start = uniquePoints.get(0);
        for (Point p : uniquePoints) {
            if (p.y < start.y || (Math.abs(p.y - start.y) < EPSILON && p.x < start.x)) {
                start = p;
            }
        }

        // Sort by polar angle
        final Point finalStart = start;
        List<Point> sorted = new ArrayList<>(uniquePoints);
        sorted.remove(finalStart);
        sorted.sort((a, b) -> {
            Orientation o = orientation(finalStart, a, b);
            if (o == Orientation.COLLINEAR) {
                return Double.compare(finalStart.distanceTo(a), finalStart.distanceTo(b));
            }
            return o == Orientation.COUNTERCLOCKWISE ? -1 : 1;
        });

        // Build hull using stack
        List<Point> hull = new ArrayList<>();
        hull.add(finalStart);

        for (Point point : sorted) {
            while (hull.size() >= 2) {
                Orientation o = orientation(hull.get(hull.size() - 2),
                                          hull.get(hull.size() - 1),
                                          point);
                if (o != Orientation.COUNTERCLOCKWISE) {
                    hull.remove(hull.size() - 1);
                } else {
                    break;
                }
            }
            hull.add(point);
        }

        return hull;
    }

    /**
     * Jarvis March (Gift Wrapping) Convex Hull Algorithm
     *
     * Finds convex hull by wrapping around point set.
     * Output-sensitive algorithm.
     *
     * Algorithm:
     * 1. Start with leftmost point
     * 2. Find most counterclockwise point from current
     * 3. Repeat until back to start
     *
     * Time Complexity: O(nh) - n points, h hull vertices
     * Space Complexity: O(h) - hull storage
     *
     * Best for: Small number of hull vertices
     *
     * Applications:
     * - Gift wrapping visualization
     * - When hull size is small
     * - Online algorithms
     *
     * @param points Array of points
     * @return List of convex hull vertices in CCW order
     */
    public static List<Point> convexHullJarvisMarch(List<Point> points) {
        if (points.size() < 3) return new ArrayList<>(points);

        // Remove duplicates
        Set<Point> uniqueSet = new LinkedHashSet<>(points);
        List<Point> uniquePoints = new ArrayList<>(uniqueSet);

        if (uniquePoints.size() < 3) return uniquePoints;

        // Find leftmost point
        Point leftmost = uniquePoints.get(0);
        for (Point p : uniquePoints) {
            if (p.x < leftmost.x || (Math.abs(p.x - leftmost.x) < EPSILON && p.y < leftmost.y)) {
                leftmost = p;
            }
        }

        List<Point> hull = new ArrayList<>();
        Point current = leftmost;

        do {
            hull.add(current);
            Point next = uniquePoints.get(0);

            for (Point candidate : uniquePoints) {
                if (candidate.equals(current)) continue;

                Orientation o = orientation(current, next, candidate);
                if (next.equals(current) ||
                    o == Orientation.COUNTERCLOCKWISE ||
                    (o == Orientation.COLLINEAR && current.distanceTo(candidate) > current.distanceTo(next))) {
                    next = candidate;
                }
            }

            current = next;
        } while (!current.equals(leftmost) && hull.size() < uniquePoints.size() + 1);

        return hull;
    }

    /**
     * QuickHull Algorithm
     *
     * Divide-and-conquer approach similar to QuickSort.
     *
     * Algorithm:
     * 1. Find points with min/max x-coordinates
     * 2. Divide points by line between min/max
     * 3. Recursively find farthest point from line
     * 4. Build hull from recursive results
     *
     * Time Complexity: O(n log n) average, O(n²) worst case
     * Space Complexity: O(n) - recursion stack
     *
     * Best for: Random point distributions
     *
     * @param points Array of points
     * @return List of convex hull vertices in CCW order
     */
    public static List<Point> convexHullQuickHull(List<Point> points) {
        if (points.size() < 3) return new ArrayList<>(points);

        // Remove duplicates
        Set<Point> uniqueSet = new LinkedHashSet<>(points);
        List<Point> uniquePoints = new ArrayList<>(uniqueSet);

        if (uniquePoints.size() < 3) return uniquePoints;

        // Find leftmost and rightmost points
        Point minPoint = uniquePoints.get(0);
        Point maxPoint = uniquePoints.get(0);
        for (Point p : uniquePoints) {
            if (p.x < minPoint.x) minPoint = p;
            if (p.x > maxPoint.x) maxPoint = p;
        }

        // Split points by line between min and max
        List<Point> upperPoints = new ArrayList<>();
        List<Point> lowerPoints = new ArrayList<>();

        for (Point p : uniquePoints) {
            if (p.equals(minPoint) || p.equals(maxPoint)) continue;
            Orientation o = orientation(minPoint, maxPoint, p);
            if (o == Orientation.COUNTERCLOCKWISE) {
                upperPoints.add(p);
            } else if (o == Orientation.CLOCKWISE) {
                lowerPoints.add(p);
            }
        }

        List<Point> hull = new ArrayList<>();
        hull.add(minPoint);
        hull.addAll(findHull(minPoint, maxPoint, upperPoints));
        hull.add(maxPoint);
        hull.addAll(findHull(maxPoint, minPoint, lowerPoints));

        return hull;
    }

    /**
     * Helper for QuickHull - recursively find hull points
     */
    private static List<Point> findHull(Point p1, Point p2, List<Point> points) {
        if (points.isEmpty()) return new ArrayList<>();

        // Find farthest point from line
        Point farthest = null;
        double maxDist = 0;

        for (Point p : points) {
            double dist = Math.abs(orientation(p1, p2, p).ordinal());
            if (dist > maxDist) {
                maxDist = dist;
                farthest = p;
            }
        }

        if (farthest == null) return new ArrayList<>();

        // Divide points into two groups
        List<Point> left = new ArrayList<>();
        List<Point> right = new ArrayList<>();

        for (Point p : points) {
            if (p.equals(farthest)) continue;
            if (orientation(p1, farthest, p) == Orientation.COUNTERCLOCKWISE) {
                left.add(p);
            }
            if (orientation(farthest, p2, p) == Orientation.COUNTERCLOCKWISE) {
                right.add(p);
            }
        }

        List<Point> result = new ArrayList<>();
        result.addAll(findHull(p1, farthest, left));
        result.add(farthest);
        result.addAll(findHull(farthest, p2, right));

        return result;
    }

    /**
     * Ray Casting Point-in-Polygon Test
     *
     * Determines if point is inside polygon by counting ray intersections.
     *
     * Algorithm:
     * 1. Cast horizontal ray from point to infinity
     * 2. Count intersections with polygon edges
     * 3. Odd count = inside, even count = outside
     *
     * Time Complexity: O(n) - n polygon vertices
     * Space Complexity: O(1)
     *
     * Applications:
     * - Hit testing in graphics
     * - Geographic information systems
     * - Collision detection
     *
     * @param point Point to test
     * @param polygon Polygon vertices
     * @return true if point is inside polygon
     */
    public static boolean pointInPolygonRayCasting(Point point, List<Point> polygon) {
        if (polygon.size() < 3) return false;

        boolean inside = false;
        int n = polygon.size();

        for (int i = 0; i < n; i++) {
            Point p1 = polygon.get(i);
            Point p2 = polygon.get((i + 1) % n);

            // Check if ray crosses edge
            if ((p1.y > point.y) != (p2.y > point.y)) {
                double xIntersection = (p2.x - p1.x) * (point.y - p1.y) / (p2.y - p1.y) + p1.x;
                if (point.x < xIntersection) {
                    inside = !inside;
                }
            }
        }

        return inside;
    }

    /**
     * Winding Number Point-in-Polygon Test
     *
     * Counts number of times polygon winds around point.
     * More robust than ray casting for edge cases.
     *
     * Time Complexity: O(n)
     * Space Complexity: O(1)
     *
     * @param point Point to test
     * @param polygon Polygon vertices
     * @return true if point is inside polygon
     */
    public static boolean pointInPolygonWindingNumber(Point point, List<Point> polygon) {
        if (polygon.size() < 3) return false;

        int windingNumber = 0;
        int n = polygon.size();

        for (int i = 0; i < n; i++) {
            Point p1 = polygon.get(i);
            Point p2 = polygon.get((i + 1) % n);

            if (p1.y <= point.y) {
                if (p2.y > point.y) {
                    if (orientation(p1, p2, point) == Orientation.COUNTERCLOCKWISE) {
                        windingNumber++;
                    }
                }
            } else {
                if (p2.y <= point.y) {
                    if (orientation(p1, p2, point) == Orientation.CLOCKWISE) {
                        windingNumber--;
                    }
                }
            }
        }

        return windingNumber != 0;
    }

    /**
     * Result class for closest pair
     */
    public static class ClosestPairResult {
        public final Point point1;
        public final Point point2;
        public final double distance;

        public ClosestPairResult(Point point1, Point point2, double distance) {
            this.point1 = point1;
            this.point2 = point2;
            this.distance = distance;
        }

        @Override
        public String toString() {
            return String.format("ClosestPair(%s, %s, distance=%.3f)",
                               point1, point2, distance);
        }
    }

    /**
     * Closest Pair of Points - Divide and Conquer
     *
     * Finds two closest points efficiently using divide and conquer.
     *
     * Algorithm:
     * 1. Sort points by x-coordinate
     * 2. Recursively find closest in left and right halves
     * 3. Check strip across midline
     *
     * Time Complexity: O(n log n)
     * Space Complexity: O(n)
     *
     * Applications:
     * - Collision detection
     * - Clustering
     * - Air traffic control
     *
     * @param points Array of points
     * @return ClosestPairResult with both points and distance
     */
    public static ClosestPairResult closestPairDivideConquer(List<Point> points) {
        if (points.size() < 2) return null;

        // Sort by x-coordinate
        List<Point> sortedX = new ArrayList<>(points);
        sortedX.sort(Comparator.comparingDouble(p -> p.x));

        return closestPairRecursive(sortedX);
    }

    /**
     * Helper for closest pair - recursive implementation
     */
    private static ClosestPairResult closestPairRecursive(List<Point> pointsByX) {
        int n = pointsByX.size();

        // Base cases
        if (n <= 3) {
            double minDist = Double.POSITIVE_INFINITY;
            Point p1 = null, p2 = null;

            for (int i = 0; i < n; i++) {
                for (int j = i + 1; j < n; j++) {
                    double dist = pointsByX.get(i).distanceTo(pointsByX.get(j));
                    if (dist < minDist) {
                        minDist = dist;
                        p1 = pointsByX.get(i);
                        p2 = pointsByX.get(j);
                    }
                }
            }

            return new ClosestPairResult(p1, p2, minDist);
        }

        // Divide
        int mid = n / 2;
        Point midPoint = pointsByX.get(mid);

        List<Point> leftHalf = pointsByX.subList(0, mid);
        List<Point> rightHalf = pointsByX.subList(mid, n);

        ClosestPairResult leftResult = closestPairRecursive(leftHalf);
        ClosestPairResult rightResult = closestPairRecursive(rightHalf);

        // Find minimum from left and right
        ClosestPairResult minResult = leftResult.distance < rightResult.distance ?
                                     leftResult : rightResult;

        // Check strip
        List<Point> strip = new ArrayList<>();
        for (Point p : pointsByX) {
            if (Math.abs(p.x - midPoint.x) < minResult.distance) {
                strip.add(p);
            }
        }

        // Sort strip by y
        strip.sort(Comparator.comparingDouble(p -> p.y));

        // Check points in strip
        for (int i = 0; i < strip.size(); i++) {
            for (int j = i + 1; j < strip.size() &&
                 (strip.get(j).y - strip.get(i).y) < minResult.distance; j++) {
                double dist = strip.get(i).distanceTo(strip.get(j));
                if (dist < minResult.distance) {
                    minResult = new ClosestPairResult(strip.get(i), strip.get(j), dist);
                }
            }
        }

        return minResult;
    }

    /**
     * Calculate polygon area using Shoelace formula
     *
     * Time Complexity: O(n)
     *
     * @param polygon Polygon vertices
     * @return Signed area (positive if CCW)
     */
    public static double polygonArea(List<Point> polygon) {
        if (polygon.size() < 3) return 0;

        double area = 0;
        int n = polygon.size();

        for (int i = 0; i < n; i++) {
            Point p1 = polygon.get(i);
            Point p2 = polygon.get((i + 1) % n);
            area += p1.x * p2.y - p2.x * p1.y;
        }

        return area / 2;
    }

    /**
     * Calculate polygon centroid
     *
     * Time Complexity: O(n)
     *
     * @param polygon Polygon vertices
     * @return Centroid point
     */
    public static Point polygonCentroid(List<Point> polygon) {
        if (polygon.isEmpty()) return null;

        double area = polygonArea(polygon);
        if (Math.abs(area) < EPSILON) {
            // Degenerate case - return average
            double sumX = 0, sumY = 0;
            for (Point p : polygon) {
                sumX += p.x;
                sumY += p.y;
            }
            return new Point(sumX / polygon.size(), sumY / polygon.size());
        }

        double cx = 0, cy = 0;
        int n = polygon.size();

        for (int i = 0; i < n; i++) {
            Point p1 = polygon.get(i);
            Point p2 = polygon.get((i + 1) % n);
            double cross = p1.x * p2.y - p2.x * p1.y;
            cx += (p1.x + p2.x) * cross;
            cy += (p1.y + p2.y) * cross;
        }

        double factor = 1 / (6 * area);
        return new Point(cx * factor, cy * factor);
    }

    /**
     * Calculate polygon perimeter
     *
     * Time Complexity: O(n)
     *
     * @param polygon Polygon vertices
     * @return Perimeter length
     */
    public static double polygonPerimeter(List<Point> polygon) {
        if (polygon.size() < 2) return 0;

        double perimeter = 0;
        int n = polygon.size();

        for (int i = 0; i < n; i++) {
            Point p1 = polygon.get(i);
            Point p2 = polygon.get((i + 1) % n);
            perimeter += p1.distanceTo(p2);
        }

        return perimeter;
    }

    /**
     * Performance Benchmarking
     */
    public static class Benchmark {
        /**
         * Generate random points
         */
        public static List<Point> generateRandomPoints(int count, double range) {
            List<Point> points = new ArrayList<>();
            Random random = new Random();
            for (int i = 0; i < count; i++) {
                points.add(new Point(random.nextDouble() * range, random.nextDouble() * range));
            }
            return points;
        }

        /**
         * Generate points on circle
         */
        public static List<Point> generateCirclePoints(int count, double radius) {
            List<Point> points = new ArrayList<>();
            for (int i = 0; i < count; i++) {
                double angle = (2 * Math.PI * i) / count;
                points.add(new Point(
                    radius * Math.cos(angle) + radius,
                    radius * Math.sin(angle) + radius
                ));
            }
            return points;
        }

        /**
         * Benchmark convex hull algorithms
         */
        public static void benchmarkConvexHull(List<Point> points) {
            System.out.println("Benchmarking Convex Hull Algorithms:");
            System.out.println("Points: " + points.size());

            long start = System.nanoTime();
            List<Point> graham = convexHullGrahamScan(points);
            long grahamTime = System.nanoTime() - start;
            System.out.printf("Graham Scan: %.3f ms (hull size: %d)%n",
                            grahamTime / 1_000_000.0, graham.size());

            start = System.nanoTime();
            List<Point> jarvis = convexHullJarvisMarch(points);
            long jarvisTime = System.nanoTime() - start;
            System.out.printf("Jarvis March: %.3f ms (hull size: %d)%n",
                            jarvisTime / 1_000_000.0, jarvis.size());

            start = System.nanoTime();
            List<Point> quick = convexHullQuickHull(points);
            long quickTime = System.nanoTime() - start;
            System.out.printf("QuickHull: %.3f ms (hull size: %d)%n",
                            quickTime / 1_000_000.0, quick.size());
        }
    }

    /**
     * Example usage and tests
     */
    public static void main(String[] args) {
        System.out.println("=== Computational Geometry Library ===\n");

        // Test convex hull
        System.out.println("1. Convex Hull Test:");
        List<Point> points = Arrays.asList(
            new Point(0, 0),
            new Point(1, 1),
            new Point(2, 2),
            new Point(0, 2),
            new Point(2, 0),
            new Point(1, 0.5)
        );

        List<Point> hull = convexHullGrahamScan(points);
        System.out.println("Graham Scan Hull: " + hull);

        // Test point in polygon
        System.out.println("\n2. Point-in-Polygon Test:");
        List<Point> square = Arrays.asList(
            new Point(0, 0),
            new Point(2, 0),
            new Point(2, 2),
            new Point(0, 2)
        );

        Point inside = new Point(1, 1);
        Point outside = new Point(3, 3);

        System.out.println("Point (1,1) in square: " +
                         pointInPolygonRayCasting(inside, square));
        System.out.println("Point (3,3) in square: " +
                         pointInPolygonRayCasting(outside, square));

        // Test closest pair
        System.out.println("\n3. Closest Pair Test:");
        List<Point> randomPoints = Benchmark.generateRandomPoints(10, 100);
        ClosestPairResult result = closestPairDivideConquer(randomPoints);
        System.out.println("Closest pair: " + result);

        // Benchmark
        System.out.println("\n4. Performance Benchmark:");
        List<Point> benchmarkPoints = Benchmark.generateRandomPoints(1000, 1000);
        Benchmark.benchmarkConvexHull(benchmarkPoints);
    }
}
