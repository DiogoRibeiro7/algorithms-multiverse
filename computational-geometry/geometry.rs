/*
 * Computational Geometry Algorithms - Rust Implementation
 * =======================================================
 *
 * Memory-safe, high-performance implementation with zero-cost abstractions.
 *
 * Compilation:
 *   rustc -O geometry.rs
 *
 * Usage:
 *   ./geometry
 *
 * Author: algorithms-multiverse
 */

use std::f64;
use std::cmp::Ordering;

const EPSILON: f64 = 1e-10;

// ============================================================================
// GEOMETRIC PRIMITIVES
// ============================================================================

#[derive(Debug, Clone, Copy, PartialEq)]
struct Point {
    x: f64,
    y: f64,
}

impl Point {
    fn new(x: f64, y: f64) -> Self {
        Point { x, y }
    }

    fn distance_squared(&self, other: &Point) -> f64 {
        let dx = self.x - other.x;
        let dy = self.y - other.y;
        dx * dx + dy * dy
    }

    fn distance(&self, other: &Point) -> f64 {
        self.distance_squared(other).sqrt()
    }
}

#[derive(Debug, Clone, Copy)]
struct LineSegment {
    start: Point,
    end: Point,
}

impl LineSegment {
    fn new(start: Point, end: Point) -> Self {
        LineSegment { start, end }
    }
}

// ============================================================================
// GEOMETRIC PREDICATES
// ============================================================================

/// Cross product of vectors (p1->p2) and (p1->p3)
/// Positive: counter-clockwise, Negative: clockwise, Zero: collinear
fn cross_product(p1: Point, p2: Point, p3: Point) -> f64 {
    (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
}

/// Determine orientation of ordered triplet
#[derive(Debug, PartialEq)]
enum Orientation {
    Collinear,
    Clockwise,
    CounterClockwise,
}

fn orientation(p: Point, q: Point, r: Point) -> Orientation {
    let val = cross_product(p, q, r);

    if val.abs() < EPSILON {
        Orientation::Collinear
    } else if val > 0.0 {
        Orientation::CounterClockwise
    } else {
        Orientation::Clockwise
    }
}

/// Check if point q lies on segment pr (assuming collinear)
fn on_segment(p: Point, q: Point, r: Point) -> bool {
    q.x <= p.x.max(r.x) && q.x >= p.x.min(r.x) &&
    q.y <= p.y.max(r.y) && q.y >= p.y.min(r.y)
}

// ============================================================================
// CONVEX HULL - GRAHAM SCAN
// ============================================================================

/// Graham Scan Algorithm
/// Time Complexity: O(n log n)
fn graham_scan(points: &[Point]) -> Vec<Point> {
    let n = points.len();
    if n < 3 {
        return points.to_vec();
    }

    let mut points = points.to_vec();

    // Find pivot (lowest y, leftmost if tie)
    let mut pivot_idx = 0;
    for i in 1..n {
        if points[i].y < points[pivot_idx].y ||
           (points[i].y - points[pivot_idx].y).abs() < EPSILON &&
           points[i].x < points[pivot_idx].x {
            pivot_idx = i;
        }
    }

    points.swap(0, pivot_idx);
    let pivot = points[0];

    // Sort by polar angle
    points[1..].sort_by(|a, b| {
        let cross = cross_product(pivot, *a, *b);

        if cross.abs() < EPSILON {
            // Collinear: sort by distance
            let d1 = pivot.distance_squared(a);
            let d2 = pivot.distance_squared(b);
            d1.partial_cmp(&d2).unwrap_or(Ordering::Equal)
        } else if cross > 0.0 {
            Ordering::Less
        } else {
            Ordering::Greater
        }
    });

    // Build hull
    let mut hull = vec![points[0], points[1], points[2]];

    for i in 3..points.len() {
        while hull.len() >= 2 {
            let len = hull.len();
            if cross_product(hull[len - 2], hull[len - 1], points[i]) <= EPSILON {
                hull.pop();
            } else {
                break;
            }
        }
        hull.push(points[i]);
    }

    hull
}

// ============================================================================
// CONVEX HULL - JARVIS MARCH
// ============================================================================

/// Jarvis March (Gift Wrapping) Algorithm
/// Time Complexity: O(nh) where h is hull size
fn jarvis_march(points: &[Point]) -> Vec<Point> {
    let n = points.len();
    if n < 3 {
        return points.to_vec();
    }

    // Find leftmost point
    let mut leftmost = 0;
    for i in 1..n {
        if points[i].x < points[leftmost].x ||
           (points[i].x - points[leftmost].x).abs() < EPSILON &&
           points[i].y < points[leftmost].y {
            leftmost = i;
        }
    }

    let mut hull = Vec::new();
    let mut current = leftmost;

    loop {
        hull.push(points[current]);

        // Find next point
        let mut next = 0;
        for i in 1..n {
            if i == current {
                continue;
            }

            if next == current {
                next = i;
            } else {
                let cross = cross_product(points[current], points[next], points[i]);

                if cross > EPSILON ||
                   (cross.abs() < EPSILON &&
                    points[current].distance_squared(&points[i]) >
                    points[current].distance_squared(&points[next])) {
                    next = i;
                }
            }
        }

        current = next;

        if current == leftmost {
            break;
        }
    }

    hull
}

// ============================================================================
// LINE SEGMENT INTERSECTION
// ============================================================================

/// Check if two line segments intersect
/// Returns Some(intersection_point) if they intersect
fn segments_intersect(seg1: LineSegment, seg2: LineSegment) -> Option<Point> {
    let p1 = seg1.start;
    let q1 = seg1.end;
    let p2 = seg2.start;
    let q2 = seg2.end;

    let o1 = orientation(p1, q1, p2);
    let o2 = orientation(p1, q1, q2);
    let o3 = orientation(p2, q2, p1);
    let o4 = orientation(p2, q2, q1);

    // General case
    if o1 != o2 && o3 != o4 {
        // Calculate intersection point
        let a1 = q1.y - p1.y;
        let b1 = p1.x - q1.x;
        let c1 = a1 * p1.x + b1 * p1.y;

        let a2 = q2.y - p2.y;
        let b2 = p2.x - q2.x;
        let c2 = a2 * p2.x + b2 * p2.y;

        let det = a1 * b2 - a2 * b1;

        if det.abs() > EPSILON {
            let x = (b2 * c1 - b1 * c2) / det;
            let y = (a1 * c2 - a2 * c1) / det;
            return Some(Point::new(x, y));
        }
    }

    // Special cases: collinear
    if o1 == Orientation::Collinear && on_segment(p1, p2, q1) {
        return Some(p2);
    }
    if o2 == Orientation::Collinear && on_segment(p1, q2, q1) {
        return Some(q2);
    }
    if o3 == Orientation::Collinear && on_segment(p2, p1, q2) {
        return Some(p1);
    }
    if o4 == Orientation::Collinear && on_segment(p2, q1, q2) {
        return Some(q1);
    }

    None
}

// ============================================================================
// POINT IN POLYGON
// ============================================================================

/// Ray casting algorithm for point-in-polygon test
/// Time Complexity: O(n)
fn point_in_polygon(point: Point, polygon: &[Point]) -> bool {
    let n = polygon.len();
    if n < 3 {
        return false;
    }

    // Create ray to infinity
    let extreme = Point::new(f64::MAX, point.y);
    let ray = LineSegment::new(point, extreme);

    let mut count = 0;

    for i in 0..n {
        let edge = LineSegment::new(polygon[i], polygon[(i + 1) % n]);

        if segments_intersect(edge, ray).is_some() {
            // Check if point is collinear with edge
            if orientation(edge.start, point, edge.end) == Orientation::Collinear {
                return on_segment(edge.start, point, edge.end);
            }
            count += 1;
        }
    }

    count % 2 == 1
}

// ============================================================================
// CLOSEST PAIR OF POINTS
// ============================================================================

/// Brute force closest pair
fn closest_pair_brute(points: &[Point]) -> (Point, Point, f64) {
    let mut min_dist = f64::MAX;
    let mut pair = (points[0], points[1]);

    for i in 0..points.len() {
        for j in (i + 1)..points.len() {
            let d = points[i].distance(&points[j]);
            if d < min_dist {
                min_dist = d;
                pair = (points[i], points[j]);
            }
        }
    }

    (pair.0, pair.1, min_dist)
}

/// Divide and conquer closest pair
/// Time Complexity: O(n log n)
fn closest_pair(points: &[Point]) -> (Point, Point, f64) {
    if points.len() < 2 {
        return (Point::new(0.0, 0.0), Point::new(0.0, 0.0), f64::MAX);
    }

    let mut sorted = points.to_vec();
    sorted.sort_by(|a, b| a.x.partial_cmp(&b.x).unwrap_or(Ordering::Equal));

    closest_pair_recursive(&sorted)
}

fn closest_pair_recursive(points: &[Point]) -> (Point, Point, f64) {
    let n = points.len();

    if n <= 3 {
        return closest_pair_brute(points);
    }

    let mid = n / 2;
    let midpoint = points[mid];

    let (left_p1, left_p2, dl) = closest_pair_recursive(&points[..mid]);
    let (right_p1, right_p2, dr) = closest_pair_recursive(&points[mid..]);

    let mut min_dist = dl;
    let mut pair = (left_p1, left_p2);

    if dr < min_dist {
        min_dist = dr;
        pair = (right_p1, right_p2);
    }

    // Check strip
    let mut strip: Vec<Point> = points
        .iter()
        .filter(|p| (p.x - midpoint.x).abs() < min_dist)
        .cloned()
        .collect();

    strip.sort_by(|a, b| a.y.partial_cmp(&b.y).unwrap_or(Ordering::Equal));

    for i in 0..strip.len() {
        let mut j = i + 1;
        while j < strip.len() && (strip[j].y - strip[i].y) < min_dist {
            let d = strip[i].distance(&strip[j]);
            if d < min_dist {
                min_dist = d;
                pair = (strip[i], strip[j]);
            }
            j += 1;
        }
    }

    (pair.0, pair.1, min_dist)
}

// ============================================================================
// POLYGON AREA
// ============================================================================

/// Calculate polygon area using shoelace formula
fn polygon_area(polygon: &[Point]) -> f64 {
    let n = polygon.len();
    if n < 3 {
        return 0.0;
    }

    let mut area = 0.0;
    for i in 0..n {
        let j = (i + 1) % n;
        area += polygon[i].x * polygon[j].y;
        area -= polygon[j].x * polygon[i].y;
    }

    (area / 2.0).abs()
}

// ============================================================================
// TESTING AND DEMONSTRATION
// ============================================================================

fn print_separator(c: char, length: usize) {
    println!("{}", c.to_string().repeat(length));
}

fn test_convex_hull() {
    println!("\n1. CONVEX HULL ALGORITHMS");
    print_separator('-', 50);

    let points = vec![
        Point::new(0.0, 3.0),
        Point::new(1.0, 1.0),
        Point::new(2.0, 2.0),
        Point::new(4.0, 4.0),
        Point::new(0.0, 0.0),
        Point::new(1.0, 2.0),
        Point::new(3.0, 1.0),
        Point::new(3.0, 3.0),
    ];

    println!("Input points ({}):", points.len());
    for p in &points {
        println!("  ({:.1}, {:.1})", p.x, p.y);
    }

    let hull1 = graham_scan(&points);
    println!("\nGraham Scan - Hull points ({}):", hull1.len());
    for p in &hull1 {
        println!("  ({:.1}, {:.1})", p.x, p.y);
    }

    let hull2 = jarvis_march(&points);
    println!("\nJarvis March - Hull points ({}):", hull2.len());
    for p in &hull2 {
        println!("  ({:.1}, {:.1})", p.x, p.y);
    }
}

fn test_line_intersection() {
    println!("\n2. LINE SEGMENT INTERSECTION");
    print_separator('-', 50);

    let seg1 = LineSegment::new(Point::new(0.0, 0.0), Point::new(10.0, 10.0));
    let seg2 = LineSegment::new(Point::new(0.0, 10.0), Point::new(10.0, 0.0));
    let seg3 = LineSegment::new(Point::new(20.0, 20.0), Point::new(30.0, 30.0));

    println!("Segment 1: ({:.1},{:.1}) to ({:.1},{:.1})",
             seg1.start.x, seg1.start.y, seg1.end.x, seg1.end.y);
    println!("Segment 2: ({:.1},{:.1}) to ({:.1},{:.1})",
             seg2.start.x, seg2.start.y, seg2.end.x, seg2.end.y);

    match segments_intersect(seg1, seg2) {
        Some(p) => println!("Segments intersect at: ({:.1}, {:.1})", p.x, p.y),
        None => println!("Segments do not intersect"),
    }

    println!("\nSegment 1: ({:.1},{:.1}) to ({:.1},{:.1})",
             seg1.start.x, seg1.start.y, seg1.end.x, seg1.end.y);
    println!("Segment 3: ({:.1},{:.1}) to ({:.1},{:.1})",
             seg3.start.x, seg3.start.y, seg3.end.x, seg3.end.y);

    match segments_intersect(seg1, seg3) {
        Some(p) => println!("Segments intersect at: ({:.1}, {:.1})", p.x, p.y),
        None => println!("Segments do not intersect"),
    }
}

fn test_point_in_polygon() {
    println!("\n3. POINT IN POLYGON TEST");
    print_separator('-', 50);

    let square = vec![
        Point::new(0.0, 0.0),
        Point::new(10.0, 0.0),
        Point::new(10.0, 10.0),
        Point::new(0.0, 10.0),
    ];

    let test_points = vec![
        (Point::new(5.0, 5.0), "Inside"),
        (Point::new(15.0, 15.0), "Outside"),
        (Point::new(0.0, 0.0), "On vertex"),
        (Point::new(5.0, 0.0), "On edge"),
    ];

    println!("Polygon: Square with corners at (0,0), (10,0), (10,10), (0,10)\n");

    for (point, desc) in &test_points {
        let inside = point_in_polygon(*point, &square);
        println!("Point ({:.1}, {:.1}) [{}]: {}",
                 point.x, point.y, desc,
                 if inside { "INSIDE" } else { "OUTSIDE" });
    }
}

fn test_closest_pair() {
    println!("\n4. CLOSEST PAIR OF POINTS");
    print_separator('-', 50);

    let points = vec![
        Point::new(0.0, 0.0),
        Point::new(1.0, 1.0),
        Point::new(2.0, 2.0),
        Point::new(3.0, 10.0),
        Point::new(4.0, 3.0),
        Point::new(5.0, 5.0),
        Point::new(6.0, 1.0),
    ];

    println!("Input points ({}):", points.len());
    for p in &points {
        println!("  ({:.1}, {:.1})", p.x, p.y);
    }

    let (p1, p2, dist) = closest_pair(&points);

    println!("\nClosest pair:");
    println!("  Point 1: ({:.1}, {:.1})", p1.x, p1.y);
    println!("  Point 2: ({:.1}, {:.1})", p2.x, p2.y);
    println!("  Distance: {:.4}", dist);
}

fn test_polygon_area() {
    println!("\n5. POLYGON AREA");
    print_separator('-', 50);

    let triangle = vec![
        Point::new(0.0, 0.0),
        Point::new(4.0, 0.0),
        Point::new(0.0, 3.0),
    ];

    let square = vec![
        Point::new(0.0, 0.0),
        Point::new(5.0, 0.0),
        Point::new(5.0, 5.0),
        Point::new(0.0, 5.0),
    ];

    let area1 = polygon_area(&triangle);
    let area2 = polygon_area(&square);

    println!("Triangle area: {:.1} (expected: 6.0)", area1);
    println!("Square area: {:.1} (expected: 25.0)", area2);
}

fn main() {
    print_separator('=', 70);
    println!("COMPUTATIONAL GEOMETRY ALGORITHMS - RUST IMPLEMENTATION");
    print_separator('=', 70);

    test_convex_hull();
    test_line_intersection();
    test_point_in_polygon();
    test_closest_pair();
    test_polygon_area();

    println!();
    print_separator('=', 70);
    println!("All tests completed successfully!");
    print_separator('=', 70);
}
