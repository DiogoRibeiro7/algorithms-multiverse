/*
 * Computational Geometry Algorithms - C Implementation
 * =====================================================
 *
 * High-performance implementation of fundamental computational geometry algorithms.
 * Includes robust floating-point handling and comprehensive edge case coverage.
 *
 * Compilation:
 *   gcc -O3 -o geometry geometry.c -lm
 *
 * Usage:
 *   ./geometry
 *
 * Author: algorithms-multiverse
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>
#include <float.h>

/* Epsilon for floating-point comparisons */
#define EPSILON 1e-10

/* Maximum number of points for static allocations */
#define MAX_POINTS 10000

/* ============================================================================
 * GEOMETRIC PRIMITIVES
 * ============================================================================ */

typedef struct {
    double x;
    double y;
} Point;

typedef struct {
    Point start;
    Point end;
} LineSegment;

/* ============================================================================
 * UTILITY FUNCTIONS
 * ============================================================================ */

/**
 * Compare two floating-point numbers with epsilon tolerance
 */
bool float_equal(double a, double b) {
    return fabs(a - b) < EPSILON;
}

/**
 * Calculate squared distance between two points
 * Avoids sqrt for performance when only comparison is needed
 */
double dist_squared(Point p1, Point p2) {
    double dx = p2.x - p1.x;
    double dy = p2.y - p1.y;
    return dx * dx + dy * dy;
}

/**
 * Calculate Euclidean distance between two points
 */
double distance(Point p1, Point p2) {
    return sqrt(dist_squared(p1, p2));
}

/**
 * Cross product of vectors (p1->p2) and (p1->p3)
 *
 * Result:
 *   > 0: Counter-clockwise turn (left turn)
 *   < 0: Clockwise turn (right turn)
 *   = 0: Collinear
 *
 * Time Complexity: O(1)
 */
double cross_product(Point p1, Point p2, Point p3) {
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x);
}

/**
 * Determine orientation of ordered triplet (p, q, r)
 *
 * Returns:
 *   0: Collinear
 *   1: Clockwise
 *   2: Counter-clockwise
 */
int orientation(Point p, Point q, Point r) {
    double val = cross_product(p, q, r);

    if (fabs(val) < EPSILON) return 0;  /* Collinear */
    return (val > 0) ? 2 : 1;  /* Clockwise or Counter-clockwise */
}

/**
 * Check if point q lies on segment pr (assuming p, q, r are collinear)
 */
bool on_segment(Point p, Point q, Point r) {
    return q.x <= fmax(p.x, r.x) && q.x >= fmin(p.x, r.x) &&
           q.y <= fmax(p.y, r.y) && q.y >= fmin(p.y, r.y);
}

/**
 * Compare function for qsort - sort by y-coordinate, then x
 */
int compare_points_yx(const void *a, const void *b) {
    Point *p1 = (Point *)a;
    Point *p2 = (Point *)b;

    if (fabs(p1->y - p2->y) < EPSILON) {
        if (fabs(p1->x - p2->x) < EPSILON) return 0;
        return (p1->x < p2->x) ? -1 : 1;
    }
    return (p1->y < p2->y) ? -1 : 1;
}

/* ============================================================================
 * CONVEX HULL - GRAHAM SCAN
 * ============================================================================ */

/**
 * Comparison function for polar angle sorting
 * Global variable used to avoid passing extra parameters to qsort
 */
static Point pivot_point;

int compare_polar_angle(const void *a, const void *b) {
    Point *p1 = (Point *)a;
    Point *p2 = (Point *)b;

    double cross = cross_product(pivot_point, *p1, *p2);

    if (fabs(cross) < EPSILON) {
        /* Collinear: closer point comes first */
        double d1 = dist_squared(pivot_point, *p1);
        double d2 = dist_squared(pivot_point, *p2);
        if (fabs(d1 - d2) < EPSILON) return 0;
        return (d1 < d2) ? -1 : 1;
    }

    return (cross > 0) ? -1 : 1;
}

/**
 * Graham Scan Algorithm for Convex Hull
 *
 * Time Complexity: O(n log n)
 * Space Complexity: O(n)
 *
 * Algorithm:
 * 1. Find point with lowest y-coordinate (pivot)
 * 2. Sort all other points by polar angle with pivot
 * 3. Process points maintaining convex hull property
 *
 * @param points: Array of input points
 * @param n: Number of points
 * @param hull: Output array for hull points (must be allocated)
 * @return: Number of hull points
 */
int graham_scan(Point *points, int n, Point *hull) {
    if (n < 3) {
        /* Hull is all points if less than 3 */
        memcpy(hull, points, n * sizeof(Point));
        return n;
    }

    /* Find pivot point (lowest y, leftmost if tie) */
    int pivot_idx = 0;
    for (int i = 1; i < n; i++) {
        if (points[i].y < points[pivot_idx].y ||
            (float_equal(points[i].y, points[pivot_idx].y) &&
             points[i].x < points[pivot_idx].x)) {
            pivot_idx = i;
        }
    }

    /* Swap pivot to first position */
    Point temp = points[0];
    points[0] = points[pivot_idx];
    points[pivot_idx] = temp;

    /* Set global pivot for sorting */
    pivot_point = points[0];

    /* Sort points by polar angle */
    qsort(points + 1, n - 1, sizeof(Point), compare_polar_angle);

    /* Remove collinear points (keep only farthest) */
    int m = 1;  /* Size of modified array */
    for (int i = 1; i < n; i++) {
        /* Keep last point of collinear sequence */
        while (i < n - 1 &&
               fabs(cross_product(pivot_point, points[i], points[i + 1])) < EPSILON) {
            i++;
        }
        points[m++] = points[i];
    }

    if (m < 3) {
        /* All points are collinear */
        memcpy(hull, points, m * sizeof(Point));
        return m;
    }

    /* Build hull */
    hull[0] = points[0];
    hull[1] = points[1];
    hull[2] = points[2];
    int hull_size = 3;

    for (int i = 3; i < m; i++) {
        /* Remove points that make right turn */
        while (hull_size >= 2 &&
               cross_product(hull[hull_size - 2], hull[hull_size - 1], points[i]) <= EPSILON) {
            hull_size--;
        }
        hull[hull_size++] = points[i];
    }

    return hull_size;
}

/* ============================================================================
 * CONVEX HULL - JARVIS MARCH (GIFT WRAPPING)
 * ============================================================================ */

/**
 * Jarvis March Algorithm for Convex Hull
 *
 * Time Complexity: O(nh) where h is hull size
 * Space Complexity: O(h)
 *
 * Algorithm:
 * 1. Start with leftmost point
 * 2. Find next point by checking which makes smallest angle
 * 3. Repeat until returning to start
 *
 * @param points: Array of input points
 * @param n: Number of points
 * @param hull: Output array for hull points
 * @return: Number of hull points
 */
int jarvis_march(Point *points, int n, Point *hull) {
    if (n < 3) {
        memcpy(hull, points, n * sizeof(Point));
        return n;
    }

    /* Find leftmost point */
    int leftmost = 0;
    for (int i = 1; i < n; i++) {
        if (points[i].x < points[leftmost].x ||
            (float_equal(points[i].x, points[leftmost].x) &&
             points[i].y < points[leftmost].y)) {
            leftmost = i;
        }
    }

    int hull_size = 0;
    int current = leftmost;

    do {
        hull[hull_size++] = points[current];

        /* Find next point */
        int next = 0;
        for (int i = 1; i < n; i++) {
            if (i == current) continue;

            if (next == current) {
                next = i;
            } else {
                double cross = cross_product(points[current], points[next], points[i]);

                if (cross > EPSILON ||
                    (fabs(cross) < EPSILON &&
                     dist_squared(points[current], points[i]) >
                     dist_squared(points[current], points[next]))) {
                    next = i;
                }
            }
        }

        current = next;

    } while (current != leftmost && hull_size < n);

    return hull_size;
}

/* ============================================================================
 * LINE SEGMENT INTERSECTION
 * ============================================================================ */

/**
 * Check if two line segments intersect
 *
 * Time Complexity: O(1)
 *
 * @param seg1, seg2: Line segments to test
 * @param intersection: Output parameter for intersection point (can be NULL)
 * @return: true if segments intersect
 */
bool segments_intersect(LineSegment seg1, LineSegment seg2, Point *intersection) {
    Point p1 = seg1.start, q1 = seg1.end;
    Point p2 = seg2.start, q2 = seg2.end;

    int o1 = orientation(p1, q1, p2);
    int o2 = orientation(p1, q1, q2);
    int o3 = orientation(p2, q2, p1);
    int o4 = orientation(p2, q2, q1);

    /* General case */
    if (o1 != o2 && o3 != o4) {
        if (intersection != NULL) {
            /* Calculate intersection point */
            double a1 = q1.y - p1.y;
            double b1 = p1.x - q1.x;
            double c1 = a1 * p1.x + b1 * p1.y;

            double a2 = q2.y - p2.y;
            double b2 = p2.x - q2.x;
            double c2 = a2 * p2.x + b2 * p2.y;

            double det = a1 * b2 - a2 * b1;

            if (fabs(det) > EPSILON) {
                intersection->x = (b2 * c1 - b1 * c2) / det;
                intersection->y = (a1 * c2 - a2 * c1) / det;
            }
        }
        return true;
    }

    /* Special cases: collinear points */
    if (o1 == 0 && on_segment(p1, p2, q1)) return true;
    if (o2 == 0 && on_segment(p1, q2, q1)) return true;
    if (o3 == 0 && on_segment(p2, p1, q2)) return true;
    if (o4 == 0 && on_segment(p2, q1, q2)) return true;

    return false;
}

/* ============================================================================
 * POINT IN POLYGON
 * ============================================================================ */

/**
 * Ray Casting Algorithm - Check if point is inside polygon
 *
 * Time Complexity: O(n) where n is number of vertices
 *
 * Algorithm:
 * Cast a ray from point to infinity and count edge crossings.
 * Odd crossings = inside, even = outside
 *
 * @param point: Point to test
 * @param polygon: Array of polygon vertices
 * @param n: Number of vertices
 * @return: true if point is inside polygon
 */
bool point_in_polygon(Point point, Point *polygon, int n) {
    if (n < 3) return false;

    /* Create ray from point to infinity (horizontal right) */
    Point extreme = {DBL_MAX, point.y};
    LineSegment ray = {point, extreme};

    int count = 0;

    for (int i = 0; i < n; i++) {
        LineSegment edge = {polygon[i], polygon[(i + 1) % n]};

        if (segments_intersect(edge, ray, NULL)) {
            /* Check if point is collinear with edge */
            if (orientation(edge.start, point, edge.end) == 0) {
                return on_segment(edge.start, point, edge.end);
            }
            count++;
        }
    }

    /* Odd count = inside, even = outside */
    return (count % 2 == 1);
}

/* ============================================================================
 * CLOSEST PAIR OF POINTS
 * ============================================================================ */

/**
 * Brute force closest pair - O(n^2)
 */
double closest_pair_brute(Point *points, int n, Point *p1, Point *p2) {
    double min_dist = DBL_MAX;

    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            double d = distance(points[i], points[j]);
            if (d < min_dist) {
                min_dist = d;
                if (p1 != NULL) *p1 = points[i];
                if (p2 != NULL) *p2 = points[j];
            }
        }
    }

    return min_dist;
}

/**
 * Helper function for divide-and-conquer closest pair
 */
double closest_in_strip(Point *strip, int size, double d, Point *p1, Point *p2) {
    double min_dist = d;

    /* Sort strip by y-coordinate */
    qsort(strip, size, sizeof(Point), compare_points_yx);

    /* Check points within distance d */
    for (int i = 0; i < size; i++) {
        for (int j = i + 1; j < size && (strip[j].y - strip[i].y) < min_dist; j++) {
            double dist = distance(strip[i], strip[j]);
            if (dist < min_dist) {
                min_dist = dist;
                if (p1 != NULL) *p1 = strip[i];
                if (p2 != NULL) *p2 = strip[j];
            }
        }
    }

    return min_dist;
}

/**
 * Compare function for sorting by x-coordinate
 */
int compare_x(const void *a, const void *b) {
    Point *p1 = (Point *)a;
    Point *p2 = (Point *)b;
    if (fabs(p1->x - p2->x) < EPSILON) return 0;
    return (p1->x < p2->x) ? -1 : 1;
}

/**
 * Recursive helper for divide-and-conquer closest pair
 */
double closest_pair_recursive(Point *px, int n, Point *p1, Point *p2) {
    /* Use brute force for small sizes */
    if (n <= 3) {
        return closest_pair_brute(px, n, p1, p2);
    }

    /* Divide */
    int mid = n / 2;
    Point midpoint = px[mid];

    Point left_p1, left_p2, right_p1, right_p2;
    double dl = closest_pair_recursive(px, mid, &left_p1, &left_p2);
    double dr = closest_pair_recursive(px + mid, n - mid, &right_p1, &right_p2);

    /* Find smaller distance */
    double d = dl;
    if (p1 != NULL && p2 != NULL) {
        *p1 = left_p1;
        *p2 = left_p2;
    }

    if (dr < d) {
        d = dr;
        if (p1 != NULL && p2 != NULL) {
            *p1 = right_p1;
            *p2 = right_p2;
        }
    }

    /* Build strip of points close to dividing line */
    Point strip[MAX_POINTS];
    int strip_size = 0;

    for (int i = 0; i < n; i++) {
        if (fabs(px[i].x - midpoint.x) < d) {
            strip[strip_size++] = px[i];
        }
    }

    /* Check strip for closer pairs */
    Point strip_p1, strip_p2;
    double strip_dist = closest_in_strip(strip, strip_size, d, &strip_p1, &strip_p2);

    if (strip_dist < d) {
        if (p1 != NULL && p2 != NULL) {
            *p1 = strip_p1;
            *p2 = strip_p2;
        }
        return strip_dist;
    }

    return d;
}

/**
 * Closest Pair of Points - Divide and Conquer
 *
 * Time Complexity: O(n log n)
 * Space Complexity: O(n)
 *
 * @param points: Array of points
 * @param n: Number of points
 * @param p1, p2: Output closest pair
 * @return: Minimum distance
 */
double closest_pair(Point *points, int n, Point *p1, Point *p2) {
    if (n < 2) return DBL_MAX;

    /* Create copy and sort by x-coordinate */
    Point *px = (Point *)malloc(n * sizeof(Point));
    memcpy(px, points, n * sizeof(Point));
    qsort(px, n, sizeof(Point), compare_x);

    double result = closest_pair_recursive(px, n, p1, p2);

    free(px);
    return result;
}

/* ============================================================================
 * POLYGON AREA
 * ============================================================================ */

/**
 * Calculate area of polygon using shoelace formula
 *
 * Time Complexity: O(n)
 *
 * @param polygon: Array of vertices
 * @param n: Number of vertices
 * @return: Area (positive for counter-clockwise, negative for clockwise)
 */
double polygon_area(Point *polygon, int n) {
    if (n < 3) return 0.0;

    double area = 0.0;
    for (int i = 0; i < n; i++) {
        int j = (i + 1) % n;
        area += polygon[i].x * polygon[j].y;
        area -= polygon[j].x * polygon[i].y;
    }

    return area / 2.0;
}

/* ============================================================================
 * TESTING AND DEMONSTRATION
 * ============================================================================ */

void print_separator(char c, int length) {
    for (int i = 0; i < length; i++) putchar(c);
    putchar('\n');
}

void test_convex_hull() {
    printf("\n1. CONVEX HULL ALGORITHMS\n");
    print_separator('-', 50);

    /* Test points */
    Point points[] = {
        {0, 3}, {1, 1}, {2, 2}, {4, 4},
        {0, 0}, {1, 2}, {3, 1}, {3, 3}
    };
    int n = sizeof(points) / sizeof(points[0]);

    printf("Input points (%d):\n", n);
    for (int i = 0; i < n; i++) {
        printf("  (%.1f, %.1f)\n", points[i].x, points[i].y);
    }

    /* Graham Scan */
    Point hull1[MAX_POINTS];
    Point *test_points1 = (Point *)malloc(n * sizeof(Point));
    memcpy(test_points1, points, n * sizeof(Point));
    int hull_size1 = graham_scan(test_points1, n, hull1);

    printf("\nGraham Scan - Hull points (%d):\n", hull_size1);
    for (int i = 0; i < hull_size1; i++) {
        printf("  (%.1f, %.1f)\n", hull1[i].x, hull1[i].y);
    }
    free(test_points1);

    /* Jarvis March */
    Point hull2[MAX_POINTS];
    int hull_size2 = jarvis_march(points, n, hull2);

    printf("\nJarvis March - Hull points (%d):\n", hull_size2);
    for (int i = 0; i < hull_size2; i++) {
        printf("  (%.1f, %.1f)\n", hull2[i].x, hull2[i].y);
    }
}

void test_line_intersection() {
    printf("\n2. LINE SEGMENT INTERSECTION\n");
    print_separator('-', 50);

    LineSegment seg1 = {{0, 0}, {10, 10}};
    LineSegment seg2 = {{0, 10}, {10, 0}};
    LineSegment seg3 = {{20, 20}, {30, 30}};

    Point intersection;

    printf("Segment 1: (%.1f,%.1f) to (%.1f,%.1f)\n",
           seg1.start.x, seg1.start.y, seg1.end.x, seg1.end.y);
    printf("Segment 2: (%.1f,%.1f) to (%.1f,%.1f)\n",
           seg2.start.x, seg2.start.y, seg2.end.x, seg2.end.y);

    if (segments_intersect(seg1, seg2, &intersection)) {
        printf("Segments intersect at: (%.1f, %.1f)\n",
               intersection.x, intersection.y);
    } else {
        printf("Segments do not intersect\n");
    }

    printf("\nSegment 1: (%.1f,%.1f) to (%.1f,%.1f)\n",
           seg1.start.x, seg1.start.y, seg1.end.x, seg1.end.y);
    printf("Segment 3: (%.1f,%.1f) to (%.1f,%.1f)\n",
           seg3.start.x, seg3.start.y, seg3.end.x, seg3.end.y);

    if (segments_intersect(seg1, seg3, &intersection)) {
        printf("Segments intersect at: (%.1f, %.1f)\n",
               intersection.x, intersection.y);
    } else {
        printf("Segments do not intersect\n");
    }
}

void test_point_in_polygon() {
    printf("\n3. POINT IN POLYGON TEST\n");
    print_separator('-', 50);

    /* Square polygon */
    Point square[] = {{0, 0}, {10, 0}, {10, 10}, {0, 10}};
    int n = 4;

    Point test_points[] = {
        {5, 5},    /* Inside */
        {15, 15},  /* Outside */
        {0, 0},    /* On vertex */
        {5, 0}     /* On edge */
    };

    printf("Polygon: Square with corners at (0,0), (10,0), (10,10), (0,10)\n\n");

    for (int i = 0; i < 4; i++) {
        bool inside = point_in_polygon(test_points[i], square, n);
        printf("Point (%.1f, %.1f): %s\n",
               test_points[i].x, test_points[i].y,
               inside ? "INSIDE" : "OUTSIDE");
    }
}

void test_closest_pair() {
    printf("\n4. CLOSEST PAIR OF POINTS\n");
    print_separator('-', 50);

    Point points[] = {
        {0, 0}, {1, 1}, {2, 2}, {3, 10},
        {4, 3}, {5, 5}, {6, 1}
    };
    int n = sizeof(points) / sizeof(points[0]);

    printf("Input points (%d):\n", n);
    for (int i = 0; i < n; i++) {
        printf("  (%.1f, %.1f)\n", points[i].x, points[i].y);
    }

    Point p1, p2;
    double min_dist = closest_pair(points, n, &p1, &p2);

    printf("\nClosest pair:\n");
    printf("  Point 1: (%.1f, %.1f)\n", p1.x, p1.y);
    printf("  Point 2: (%.1f, %.1f)\n", p2.x, p2.y);
    printf("  Distance: %.4f\n", min_dist);
}

void test_polygon_area() {
    printf("\n5. POLYGON AREA\n");
    print_separator('-', 50);

    Point triangle[] = {{0, 0}, {4, 0}, {0, 3}};
    Point square[] = {{0, 0}, {5, 0}, {5, 5}, {0, 5}};

    double area1 = fabs(polygon_area(triangle, 3));
    double area2 = fabs(polygon_area(square, 4));

    printf("Triangle area: %.1f (expected: 6.0)\n", area1);
    printf("Square area: %.1f (expected: 25.0)\n", area2);
}

int main() {
    print_separator('=', 70);
    printf("COMPUTATIONAL GEOMETRY ALGORITHMS - C IMPLEMENTATION\n");
    print_separator('=', 70);

    test_convex_hull();
    test_line_intersection();
    test_point_in_polygon();
    test_closest_pair();
    test_polygon_area();

    printf("\n");
    print_separator('=', 70);
    printf("All tests completed successfully!\n");
    print_separator('=', 70);

    return 0;
}
