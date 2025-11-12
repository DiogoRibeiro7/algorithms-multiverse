// Computational Geometry Algorithms Implementation in Go
//
// Computational geometry deals with algorithms for solving geometric problems.
// Common applications include computer graphics, robotics, GIS, and CAD.
//
// Time Complexity varies by algorithm:
// - Convex Hull (Graham Scan): O(n log n)
// - Line Intersection: O(1)
// - Point in Polygon: O(n)
// - Closest Pair: O(n log n)
// - Polygon Area: O(n)
//
// Go features:
// - Geometric primitives (Point, Line, Polygon)
// - Convex hull algorithms (Graham Scan, Jarvis March)
// - Line segment intersection detection
// - Point-in-polygon tests
// - Closest pair of points with divide-and-conquer
// - Parallel processing with goroutines for large point sets
// - Polygon area and perimeter calculations

package main

import (
	"fmt"
	"math"
	"sort"
	"strings"
	"sync"
)

// Point represents a 2D point
type Point struct {
	X, Y float64
}

// NewPoint creates a new point
func NewPoint(x, y float64) Point {
	return Point{X: x, Y: y}
}

// String returns string representation
func (p Point) String() string {
	return fmt.Sprintf("(%.2f, %.2f)", p.X, p.Y)
}

// Distance calculates Euclidean distance between two points
func (p Point) Distance(other Point) float64 {
	dx := p.X - other.X
	dy := p.Y - other.Y
	return math.Sqrt(dx*dx + dy*dy)
}

// ManhattanDistance calculates Manhattan distance
func (p Point) ManhattanDistance(other Point) float64 {
	return math.Abs(p.X-other.X) + math.Abs(p.Y-other.Y)
}

// Line represents a line segment
type Line struct {
	Start, End Point
}

// NewLine creates a new line segment
func NewLine(start, end Point) Line {
	return Line{Start: start, End: end}
}

// Length returns the length of the line segment
func (l Line) Length() float64 {
	return l.Start.Distance(l.End)
}

// Polygon represents a polygon as a list of vertices
type Polygon struct {
	Vertices []Point
}

// NewPolygon creates a new polygon
func NewPolygon(vertices []Point) *Polygon {
	return &Polygon{Vertices: vertices}
}

// GEOMETRIC OPERATIONS

// CrossProduct computes the cross product of vectors OA and OB
//
// Positive: counterclockwise turn
// Negative: clockwise turn
// Zero: collinear
func CrossProduct(O, A, B Point) float64 {
	return (A.X-O.X)*(B.Y-O.Y) - (A.Y-O.Y)*(B.X-O.X)
}

// Orientation determines the orientation of three points
//
// Returns:
// 0: Collinear
// 1: Clockwise
// 2: Counterclockwise
func Orientation(p, q, r Point) int {
	val := (q.Y-p.Y)*(r.X-q.X) - (q.X-p.X)*(r.Y-q.Y)

	if math.Abs(val) < 1e-9 {
		return 0 // Collinear
	}

	if val > 0 {
		return 1 // Clockwise
	}
	return 2 // Counterclockwise
}

// OnSegment checks if point q lies on segment pr (given they're collinear)
func OnSegment(p, q, r Point) bool {
	return q.X <= math.Max(p.X, r.X) && q.X >= math.Min(p.X, r.X) &&
		q.Y <= math.Max(p.Y, r.Y) && q.Y >= math.Min(p.Y, r.Y)
}

// DoSegmentsIntersect checks if line segments intersect
//
// Time Complexity: O(1)
func DoSegmentsIntersect(l1, l2 Line) bool {
	p1, q1 := l1.Start, l1.End
	p2, q2 := l2.Start, l2.End

	o1 := Orientation(p1, q1, p2)
	o2 := Orientation(p1, q1, q2)
	o3 := Orientation(p2, q2, p1)
	o4 := Orientation(p2, q2, q1)

	// General case
	if o1 != o2 && o3 != o4 {
		return true
	}

	// Special cases (collinear points)
	if o1 == 0 && OnSegment(p1, p2, q1) {
		return true
	}
	if o2 == 0 && OnSegment(p1, q2, q1) {
		return true
	}
	if o3 == 0 && OnSegment(p2, p1, q2) {
		return true
	}
	if o4 == 0 && OnSegment(p2, q1, q2) {
		return true
	}

	return false
}

// CONVEX HULL ALGORITHMS

// ConvexHullGraham computes convex hull using Graham Scan
//
// Time Complexity: O(n log n)
// Space Complexity: O(n)
func ConvexHullGraham(points []Point) []Point {
	if len(points) < 3 {
		return points
	}

	// Find the bottom-most point (or left most in case of tie)
	bottom := 0
	for i := 1; i < len(points); i++ {
		if points[i].Y < points[bottom].Y ||
			(points[i].Y == points[bottom].Y && points[i].X < points[bottom].X) {
			bottom = i
		}
	}

	// Swap bottom point to first position
	points[0], points[bottom] = points[bottom], points[0]
	anchor := points[0]

	// Sort points by polar angle with respect to anchor
	sort.Slice(points[1:], func(i, j int) bool {
		i, j = i+1, j+1 // Adjust indices

		cross := CrossProduct(anchor, points[i], points[j])
		if math.Abs(cross) < 1e-9 {
			// Collinear, sort by distance
			return anchor.Distance(points[i]) < anchor.Distance(points[j])
		}
		return cross > 0 // Counterclockwise comes first
	})

	// Build convex hull
	hull := []Point{points[0], points[1], points[2]}

	for i := 3; i < len(points); i++ {
		// Remove points that make clockwise turn
		for len(hull) > 1 &&
			CrossProduct(hull[len(hull)-2], hull[len(hull)-1], points[i]) <= 0 {
			hull = hull[:len(hull)-1]
		}
		hull = append(hull, points[i])
	}

	return hull
}

// ConvexHullJarvis computes convex hull using Jarvis March (Gift Wrapping)
//
// Time Complexity: O(nh) where h is the number of hull points
// Space Complexity: O(h)
func ConvexHullJarvis(points []Point) []Point {
	if len(points) < 3 {
		return points
	}

	hull := make([]Point, 0)

	// Find leftmost point
	leftmost := 0
	for i := 1; i < len(points); i++ {
		if points[i].X < points[leftmost].X ||
			(points[i].X == points[leftmost].X && points[i].Y < points[leftmost].Y) {
			leftmost = i
		}
	}

	current := leftmost

	for {
		hull = append(hull, points[current])

		// Find the most counterclockwise point
		next := (current + 1) % len(points)

		for i := 0; i < len(points); i++ {
			if Orientation(points[current], points[i], points[next]) == 2 {
				next = i
			}
		}

		current = next

		// If we come back to first point, we're done
		if current == leftmost {
			break
		}
	}

	return hull
}

// ParallelConvexHull computes convex hull using parallel divide-and-conquer
//
// Divides points into chunks, computes hull for each chunk in parallel,
// then merges the results
func ParallelConvexHull(points []Point, numWorkers int) []Point {
	if len(points) < 100 {
		return ConvexHullGraham(points)
	}

	chunkSize := len(points) / numWorkers
	hulls := make([][]Point, numWorkers)
	var wg sync.WaitGroup

	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		start := i * chunkSize
		end := start + chunkSize
		if i == numWorkers-1 {
			end = len(points)
		}

		go func(idx int, chunk []Point) {
			defer wg.Done()
			hulls[idx] = ConvexHullGraham(chunk)
		}(i, points[start:end])
	}

	wg.Wait()

	// Merge all hulls
	merged := make([]Point, 0)
	for _, hull := range hulls {
		merged = append(merged, hull...)
	}

	return ConvexHullGraham(merged)
}

// POINT-IN-POLYGON TESTS

// PointInPolygon checks if a point is inside a polygon using ray casting
//
// Time Complexity: O(n)
func PointInPolygon(point Point, polygon *Polygon) bool {
	vertices := polygon.Vertices
	n := len(vertices)
	inside := false

	j := n - 1
	for i := 0; i < n; i++ {
		xi, yi := vertices[i].X, vertices[i].Y
		xj, yj := vertices[j].X, vertices[j].Y

		intersect := ((yi > point.Y) != (yj > point.Y)) &&
			(point.X < (xj-xi)*(point.Y-yi)/(yj-yi)+xi)

		if intersect {
			inside = !inside
		}

		j = i
	}

	return inside
}

// PointInPolygonWindingNumber uses winding number algorithm
//
// More robust for complex polygons
// Time Complexity: O(n)
func PointInPolygonWindingNumber(point Point, polygon *Polygon) bool {
	vertices := polygon.Vertices
	windingNumber := 0

	for i := 0; i < len(vertices); i++ {
		j := (i + 1) % len(vertices)

		if vertices[i].Y <= point.Y {
			if vertices[j].Y > point.Y {
				if CrossProduct(vertices[i], vertices[j], point) > 0 {
					windingNumber++
				}
			}
		} else {
			if vertices[j].Y <= point.Y {
				if CrossProduct(vertices[i], vertices[j], point) < 0 {
					windingNumber--
				}
			}
		}
	}

	return windingNumber != 0
}

// CLOSEST PAIR OF POINTS

// ClosestPairBruteForce finds closest pair using brute force
//
// Time Complexity: O(n²)
func ClosestPairBruteForce(points []Point) (Point, Point, float64) {
	if len(points) < 2 {
		return Point{}, Point{}, math.Inf(1)
	}

	minDist := math.Inf(1)
	var p1, p2 Point

	for i := 0; i < len(points); i++ {
		for j := i + 1; j < len(points); j++ {
			dist := points[i].Distance(points[j])
			if dist < minDist {
				minDist = dist
				p1, p2 = points[i], points[j]
			}
		}
	}

	return p1, p2, minDist
}

// ClosestPair finds closest pair using divide-and-conquer
//
// Time Complexity: O(n log n)
func ClosestPair(points []Point) (Point, Point, float64) {
	// Sort by X coordinate
	sortedX := make([]Point, len(points))
	copy(sortedX, points)
	sort.Slice(sortedX, func(i, j int) bool {
		return sortedX[i].X < sortedX[j].X
	})

	// Sort by Y coordinate
	sortedY := make([]Point, len(points))
	copy(sortedY, points)
	sort.Slice(sortedY, func(i, j int) bool {
		return sortedY[i].Y < sortedY[j].Y
	})

	return closestPairRecursive(sortedX, sortedY)
}

func closestPairRecursive(sortedX, sortedY []Point) (Point, Point, float64) {
	n := len(sortedX)

	// Base case: use brute force for small inputs
	if n <= 3 {
		return ClosestPairBruteForce(sortedX)
	}

	// Divide
	mid := n / 2
	midPoint := sortedX[mid]

	leftX := sortedX[:mid]
	rightX := sortedX[mid:]

	leftY := make([]Point, 0, mid)
	rightY := make([]Point, 0, n-mid)

	for _, p := range sortedY {
		if p.X <= midPoint.X {
			leftY = append(leftY, p)
		} else {
			rightY = append(rightY, p)
		}
	}

	// Conquer
	p1L, p2L, distL := closestPairRecursive(leftX, leftY)
	p1R, p2R, distR := closestPairRecursive(rightX, rightY)

	// Find minimum
	minDist := distL
	p1, p2 := p1L, p2L

	if distR < minDist {
		minDist = distR
		p1, p2 = p1R, p2R
	}

	// Check strip
	strip := make([]Point, 0)
	for _, p := range sortedY {
		if math.Abs(p.X-midPoint.X) < minDist {
			strip = append(strip, p)
		}
	}

	// Check strip for closer pairs
	for i := 0; i < len(strip); i++ {
		j := i + 1
		for j < len(strip) && strip[j].Y-strip[i].Y < minDist {
			dist := strip[i].Distance(strip[j])
			if dist < minDist {
				minDist = dist
				p1, p2 = strip[i], strip[j]
			}
			j++
		}
	}

	return p1, p2, minDist
}

// POLYGON OPERATIONS

// PolygonArea calculates the area of a polygon
//
// Uses the Shoelace formula
// Time Complexity: O(n)
func (p *Polygon) Area() float64 {
	if len(p.Vertices) < 3 {
		return 0
	}

	area := 0.0
	n := len(p.Vertices)

	for i := 0; i < n; i++ {
		j := (i + 1) % n
		area += p.Vertices[i].X * p.Vertices[j].Y
		area -= p.Vertices[j].X * p.Vertices[i].Y
	}

	return math.Abs(area) / 2.0
}

// PolygonPerimeter calculates the perimeter
//
// Time Complexity: O(n)
func (p *Polygon) Perimeter() float64 {
	if len(p.Vertices) < 2 {
		return 0
	}

	perimeter := 0.0
	n := len(p.Vertices)

	for i := 0; i < n; i++ {
		j := (i + 1) % n
		perimeter += p.Vertices[i].Distance(p.Vertices[j])
	}

	return perimeter
}

// Centroid calculates the centroid of a polygon
//
// Time Complexity: O(n)
func (p *Polygon) Centroid() Point {
	if len(p.Vertices) == 0 {
		return Point{}
	}

	cx, cy := 0.0, 0.0
	area := 0.0
	n := len(p.Vertices)

	for i := 0; i < n; i++ {
		j := (i + 1) % n
		cross := p.Vertices[i].X*p.Vertices[j].Y - p.Vertices[j].X*p.Vertices[i].Y
		cx += (p.Vertices[i].X + p.Vertices[j].X) * cross
		cy += (p.Vertices[i].Y + p.Vertices[j].Y) * cross
		area += cross
	}

	area /= 2.0

	if math.Abs(area) < 1e-9 {
		return Point{}
	}

	cx /= (6.0 * area)
	cy /= (6.0 * area)

	return Point{cx, cy}
}

// IsConvex checks if the polygon is convex
//
// Time Complexity: O(n)
func (p *Polygon) IsConvex() bool {
	if len(p.Vertices) < 3 {
		return false
	}

	n := len(p.Vertices)
	sign := 0

	for i := 0; i < n; i++ {
		j := (i + 1) % n
		k := (i + 2) % n

		cross := CrossProduct(p.Vertices[i], p.Vertices[j], p.Vertices[k])

		if math.Abs(cross) > 1e-9 {
			if cross > 0 {
				if sign < 0 {
					return false
				}
				sign = 1
			} else {
				if sign > 0 {
					return false
				}
				sign = -1
			}
		}
	}

	return true
}

// DemonstrateComputationalGeometry demonstrates geometry algorithms
func DemonstrateComputationalGeometry() {
	fmt.Println("📐 Computational Geometry Algorithms in Go")
	fmt.Println(strings.Repeat("=", 80))

	// Basic point operations
	fmt.Println("\n📍 Point Operations:")
	fmt.Println(strings.Repeat("-", 80))

	p1 := NewPoint(0, 0)
	p2 := NewPoint(3, 4)
	p3 := NewPoint(1, 1)

	fmt.Printf("Point 1: %s\n", p1)
	fmt.Printf("Point 2: %s\n", p2)
	fmt.Printf("Point 3: %s\n", p3)
	fmt.Printf("\nEuclidean distance (p1 to p2): %.2f\n", p1.Distance(p2))
	fmt.Printf("Manhattan distance (p1 to p2): %.2f\n", p1.ManhattanDistance(p2))

	// Line intersection
	fmt.Println("\n\n📏 Line Segment Intersection:")
	fmt.Println(strings.Repeat("-", 80))

	l1 := NewLine(NewPoint(1, 1), NewPoint(10, 1))
	l2 := NewLine(NewPoint(1, 2), NewPoint(10, 2))
	l3 := NewLine(NewPoint(5, 0), NewPoint(5, 5))

	fmt.Printf("Line 1: %s -> %s\n", l1.Start, l1.End)
	fmt.Printf("Line 2: %s -> %s\n", l2.Start, l2.End)
	fmt.Printf("Line 3: %s -> %s\n", l3.Start, l3.End)

	fmt.Printf("\nL1 intersects L2: %v\n", DoSegmentsIntersect(l1, l2))
	fmt.Printf("L1 intersects L3: %v\n", DoSegmentsIntersect(l1, l3))
	fmt.Printf("L2 intersects L3: %v\n", DoSegmentsIntersect(l2, l3))

	// Convex hull
	fmt.Println("\n\n🔷 Convex Hull:")
	fmt.Println(strings.Repeat("-", 80))

	points := []Point{
		{0, 3}, {1, 1}, {2, 2}, {4, 4},
		{0, 0}, {1, 2}, {3, 1}, {3, 3},
	}

	fmt.Println("Points:")
	for i, p := range points {
		fmt.Printf("  %d: %s\n", i, p)
	}

	hullGraham := ConvexHullGraham(points)
	fmt.Println("\nConvex Hull (Graham Scan):")
	for i, p := range hullGraham {
		fmt.Printf("  %d: %s\n", i, p)
	}

	hullJarvis := ConvexHullJarvis(points)
	fmt.Println("\nConvex Hull (Jarvis March):")
	for i, p := range hullJarvis {
		fmt.Printf("  %d: %s\n", i, p)
	}

	// Point in polygon
	fmt.Println("\n\n🔍 Point in Polygon:")
	fmt.Println(strings.Repeat("-", 80))

	square := NewPolygon([]Point{
		{0, 0}, {4, 0}, {4, 4}, {0, 4},
	})

	testPoints := []Point{
		{2, 2},   // Inside
		{5, 5},   // Outside
		{0, 0},   // Vertex
		{2, 0},   // Edge
		{-1, -1}, // Outside
	}

	fmt.Println("Polygon: Square with corners at (0,0), (4,0), (4,4), (0,4)")
	fmt.Println("\nTesting points:")
	for _, p := range testPoints {
		inside := PointInPolygon(p, square)
		status := "Outside"
		if inside {
			status = "Inside"
		}
		fmt.Printf("  %s: %s\n", p, status)
	}

	// Closest pair of points
	fmt.Println("\n\n🎯 Closest Pair of Points:")
	fmt.Println(strings.Repeat("-", 80))

	randomPoints := []Point{
		{2, 3}, {12, 30}, {40, 50}, {5, 1}, {12, 10}, {3, 4},
	}

	fmt.Println("Points:")
	for _, p := range randomPoints {
		fmt.Printf("  %s\n", p)
	}

	p1Brute, p2Brute, distBrute := ClosestPairBruteForce(randomPoints)
	fmt.Printf("\nBrute Force:\n")
	fmt.Printf("  Closest pair: %s and %s\n", p1Brute, p2Brute)
	fmt.Printf("  Distance: %.2f\n", distBrute)

	p1Opt, p2Opt, distOpt := ClosestPair(randomPoints)
	fmt.Printf("\nDivide-and-Conquer:\n")
	fmt.Printf("  Closest pair: %s and %s\n", p1Opt, p2Opt)
	fmt.Printf("  Distance: %.2f\n", distOpt)

	// Polygon properties
	fmt.Println("\n\n🔺 Polygon Properties:")
	fmt.Println(strings.Repeat("-", 80))

	triangle := NewPolygon([]Point{
		{0, 0}, {4, 0}, {2, 3},
	})

	fmt.Println("Triangle vertices:", triangle.Vertices)
	fmt.Printf("Area: %.2f\n", triangle.Area())
	fmt.Printf("Perimeter: %.2f\n", triangle.Perimeter())
	fmt.Printf("Centroid: %s\n", triangle.Centroid())
	fmt.Printf("Is convex: %v\n", triangle.IsConvex())

	// Parallel convex hull
	fmt.Println("\n\n🚀 Parallel Convex Hull (Large Dataset):")
	fmt.Println(strings.Repeat("-", 80))

	// Generate large point set
	largePointSet := make([]Point, 1000)
	for i := 0; i < 1000; i++ {
		largePointSet[i] = NewPoint(
			float64(i%100),
			float64(i/100),
		)
	}

	fmt.Printf("Computing convex hull for %d points...\n", len(largePointSet))
	hull := ParallelConvexHull(largePointSet, 4)
	fmt.Printf("Hull has %d vertices\n", len(hull))

	// Complex polygon
	fmt.Println("\n\n⭐ Complex Polygon:")
	fmt.Println(strings.Repeat("-", 80))

	hexagon := NewPolygon([]Point{
		{1, 0}, {2, 0}, {3, 1}, {2, 2}, {1, 2}, {0, 1},
	})

	fmt.Println("Regular hexagon:")
	fmt.Printf("  Area: %.2f\n", hexagon.Area())
	fmt.Printf("  Perimeter: %.2f\n", hexagon.Perimeter())
	fmt.Printf("  Centroid: %s\n", hexagon.Centroid())
	fmt.Printf("  Is convex: %v\n", hexagon.IsConvex())
}

func main() {
	DemonstrateComputationalGeometry()
	fmt.Println("\n✨ Computational geometry demonstration complete!")
}
