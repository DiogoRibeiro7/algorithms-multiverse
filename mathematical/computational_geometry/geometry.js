/**
 * Computational Geometry Algorithms in JavaScript
 *
 * Comprehensive collection of 2D computational geometry algorithms with
 * web visualization capabilities using HTML5 Canvas.
 *
 * Algorithms included:
 * - Convex Hull: Graham Scan, Jarvis March, QuickHull
 * - Line Operations: Intersection, orientation tests
 * - Point-in-Polygon: Ray casting, winding number
 * - Closest Pair: Divide and conquer
 * - Polygon Operations: Area, centroid, perimeter
 * - Visualization: Canvas-based rendering
 *
 * @author Algorithms Multiverse
 * @module computational_geometry
 */

const EPSILON = 1e-10;

/**
 * Orientation enum for geometric predicates
 */
const Orientation = Object.freeze({
    COLLINEAR: 0,
    CLOCKWISE: 1,
    COUNTERCLOCKWISE: 2
});

/**
 * 2D Point class with robust floating-point comparison
 *
 * Immutable point representation using Object.freeze for hashability
 * and consistent behavior in Sets and Maps.
 *
 * @class Point
 */
class Point {
    /**
     * Create a point
     * @param {number} x - X coordinate
     * @param {number} y - Y coordinate
     */
    constructor(x, y) {
        this.x = x;
        this.y = y;
        Object.freeze(this);
    }

    /**
     * Check equality with epsilon tolerance
     * @param {Point} other - Point to compare
     * @returns {boolean} True if points are equal within epsilon
     */
    equals(other) {
        return Math.abs(this.x - other.x) < EPSILON &&
               Math.abs(this.y - other.y) < EPSILON;
    }

    /**
     * Add vector to point
     * @param {Point} other - Vector to add
     * @returns {Point} New point
     */
    add(other) {
        return new Point(this.x + other.x, this.y + other.y);
    }

    /**
     * Subtract to create vector
     * @param {Point} other - Point to subtract
     * @returns {Point} Resulting vector
     */
    subtract(other) {
        return new Point(this.x - other.x, this.y - other.y);
    }

    /**
     * Dot product
     * @param {Point} other - Vector for dot product
     * @returns {number} Dot product
     */
    dot(other) {
        return this.x * other.x + this.y * other.y;
    }

    /**
     * Cross product (z-component in 3D)
     * @param {Point} other - Vector for cross product
     * @returns {number} Cross product magnitude
     */
    cross(other) {
        return this.x * other.y - this.y * other.x;
    }

    /**
     * Distance from origin
     * @returns {number} Euclidean distance
     */
    magnitude() {
        return Math.sqrt(this.x * this.x + this.y * this.y);
    }

    /**
     * Distance to another point
     * @param {Point} other - Target point
     * @returns {number} Euclidean distance
     */
    distanceTo(other) {
        const dx = this.x - other.x;
        const dy = this.y - other.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    /**
     * String representation
     * @returns {string} String representation
     */
    toString() {
        return `Point(${this.x.toFixed(3)}, ${this.y.toFixed(3)})`;
    }

    /**
     * Create hash for use in Maps/Sets
     * @returns {string} Hash string
     */
    hash() {
        const xHash = Math.round(this.x / EPSILON);
        const yHash = Math.round(this.y / EPSILON);
        return `${xHash},${yHash}`;
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
 * @param {Point} p - First point
 * @param {Point} q - Second point
 * @param {Point} r - Third point
 * @returns {number} Orientation constant
 */
function orientation(p, q, r) {
    const v1 = q.subtract(p);
    const v2 = r.subtract(p);
    const cross = v1.cross(v2);

    if (Math.abs(cross) < EPSILON) return Orientation.COLLINEAR;
    return cross > 0 ? Orientation.COUNTERCLOCKWISE : Orientation.CLOCKWISE;
}

/**
 * Check if point q lies on segment pr
 *
 * Assumes collinearity has been verified.
 *
 * @param {Point} p - Segment start
 * @param {Point} q - Point to check
 * @param {Point} r - Segment end
 * @returns {boolean} True if q is on segment pr
 */
function onSegment(p, q, r) {
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
 * @param {Point} p1 - First segment start
 * @param {Point} q1 - First segment end
 * @param {Point} p2 - Second segment start
 * @param {Point} q2 - Second segment end
 * @returns {boolean} True if segments intersect
 */
function segmentsIntersect(p1, q1, p2, q2) {
    const o1 = orientation(p1, q1, p2);
    const o2 = orientation(p1, q1, q2);
    const o3 = orientation(p2, q2, p1);
    const o4 = orientation(p2, q2, q1);

    // General case
    if (o1 !== o2 && o3 !== o4) return true;

    // Special cases - collinear points
    if (o1 === Orientation.COLLINEAR && onSegment(p1, p2, q1)) return true;
    if (o2 === Orientation.COLLINEAR && onSegment(p1, q2, q1)) return true;
    if (o3 === Orientation.COLLINEAR && onSegment(p2, p1, q2)) return true;
    if (o4 === Orientation.COLLINEAR && onSegment(p2, q1, q2)) return true;

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
 * @param {Point[]} points - Array of points
 * @returns {Point[]} Convex hull vertices in CCW order
 */
function convexHullGrahamScan(points) {
    if (points.length < 3) return [...points];

    // Remove duplicates
    const uniquePoints = [];
    const seen = new Set();
    for (const p of points) {
        const hash = p.hash();
        if (!seen.has(hash)) {
            seen.add(hash);
            uniquePoints.push(p);
        }
    }

    if (uniquePoints.length < 3) return uniquePoints;

    // Find lowest point (leftmost if tie)
    let start = uniquePoints[0];
    for (let i = 1; i < uniquePoints.length; i++) {
        const p = uniquePoints[i];
        if (p.y < start.y || (Math.abs(p.y - start.y) < EPSILON && p.x < start.x)) {
            start = p;
        }
    }

    // Sort by polar angle
    const sorted = uniquePoints.filter(p => !p.equals(start));
    sorted.sort((a, b) => {
        const o = orientation(start, a, b);
        if (o === Orientation.COLLINEAR) {
            return start.distanceTo(a) - start.distanceTo(b);
        }
        return o === Orientation.COUNTERCLOCKWISE ? -1 : 1;
    });

    // Build hull using stack
    const hull = [start];
    for (const point of sorted) {
        while (hull.length >= 2) {
            const o = orientation(hull[hull.length - 2], hull[hull.length - 1], point);
            if (o !== Orientation.COUNTERCLOCKWISE) {
                hull.pop();
            } else {
                break;
            }
        }
        hull.push(point);
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
 * @param {Point[]} points - Array of points
 * @returns {Point[]} Convex hull vertices in CCW order
 */
function convexHullJarvisMarch(points) {
    if (points.length < 3) return [...points];

    // Remove duplicates
    const uniquePoints = [];
    const seen = new Set();
    for (const p of points) {
        const hash = p.hash();
        if (!seen.has(hash)) {
            seen.add(hash);
            uniquePoints.push(p);
        }
    }

    if (uniquePoints.length < 3) return uniquePoints;

    // Find leftmost point
    let leftmost = uniquePoints[0];
    for (let i = 1; i < uniquePoints.length; i++) {
        const p = uniquePoints[i];
        if (p.x < leftmost.x || (Math.abs(p.x - leftmost.x) < EPSILON && p.y < leftmost.y)) {
            leftmost = p;
        }
    }

    const hull = [];
    let current = leftmost;

    do {
        hull.push(current);
        let next = uniquePoints[0];

        for (const candidate of uniquePoints) {
            if (candidate.equals(current)) continue;

            const o = orientation(current, next, candidate);
            if (next.equals(current) ||
                o === Orientation.COUNTERCLOCKWISE ||
                (o === Orientation.COLLINEAR && current.distanceTo(candidate) > current.distanceTo(next))) {
                next = candidate;
            }
        }

        current = next;
    } while (!current.equals(leftmost) && hull.length < uniquePoints.length + 1);

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
 * @param {Point[]} points - Array of points
 * @returns {Point[]} Convex hull vertices in CCW order
 */
function convexHullQuickHull(points) {
    if (points.length < 3) return [...points];

    // Remove duplicates
    const uniquePoints = [];
    const seen = new Set();
    for (const p of points) {
        const hash = p.hash();
        if (!seen.has(hash)) {
            seen.add(hash);
            uniquePoints.push(p);
        }
    }

    if (uniquePoints.length < 3) return uniquePoints;

    // Find leftmost and rightmost points
    let minPoint = uniquePoints[0];
    let maxPoint = uniquePoints[0];
    for (const p of uniquePoints) {
        if (p.x < minPoint.x) minPoint = p;
        if (p.x > maxPoint.x) maxPoint = p;
    }

    // Helper function to find points on one side of line
    function findHull(p1, p2, points) {
        if (points.length === 0) return [];

        // Find farthest point from line
        let farthest = null;
        let maxDist = 0;

        for (const p of points) {
            const dist = Math.abs(orientation(p1, p2, p));
            if (dist > maxDist) {
                maxDist = dist;
                farthest = p;
            }
        }

        if (farthest === null) return [];

        // Divide points into two groups
        const left = [];
        const right = [];

        for (const p of points) {
            if (p.equals(farthest)) continue;
            if (orientation(p1, farthest, p) === Orientation.COUNTERCLOCKWISE) {
                left.push(p);
            }
            if (orientation(farthest, p2, p) === Orientation.COUNTERCLOCKWISE) {
                right.push(p);
            }
        }

        const leftHull = findHull(p1, farthest, left);
        const rightHull = findHull(farthest, p2, right);

        return [...leftHull, farthest, ...rightHull];
    }

    // Split points by line between min and max
    const upperPoints = [];
    const lowerPoints = [];

    for (const p of uniquePoints) {
        if (p.equals(minPoint) || p.equals(maxPoint)) continue;
        const o = orientation(minPoint, maxPoint, p);
        if (o === Orientation.COUNTERCLOCKWISE) {
            upperPoints.push(p);
        } else if (o === Orientation.CLOCKWISE) {
            lowerPoints.push(p);
        }
    }

    const upperHull = findHull(minPoint, maxPoint, upperPoints);
    const lowerHull = findHull(maxPoint, minPoint, lowerPoints);

    return [minPoint, ...upperHull, maxPoint, ...lowerHull];
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
 * @param {Point} point - Point to test
 * @param {Point[]} polygon - Polygon vertices
 * @returns {boolean} True if point is inside polygon
 */
function pointInPolygonRayCasting(point, polygon) {
    if (polygon.length < 3) return false;

    let inside = false;
    const n = polygon.length;

    for (let i = 0; i < n; i++) {
        const p1 = polygon[i];
        const p2 = polygon[(i + 1) % n];

        // Check if ray crosses edge
        if ((p1.y > point.y) !== (p2.y > point.y)) {
            const xIntersection = (p2.x - p1.x) * (point.y - p1.y) / (p2.y - p1.y) + p1.x;
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
 * @param {Point} point - Point to test
 * @param {Point[]} polygon - Polygon vertices
 * @returns {boolean} True if point is inside polygon
 */
function pointInPolygonWindingNumber(point, polygon) {
    if (polygon.length < 3) return false;

    let windingNumber = 0;
    const n = polygon.length;

    for (let i = 0; i < n; i++) {
        const p1 = polygon[i];
        const p2 = polygon[(i + 1) % n];

        if (p1.y <= point.y) {
            if (p2.y > point.y) {
                if (orientation(p1, p2, point) === Orientation.COUNTERCLOCKWISE) {
                    windingNumber++;
                }
            }
        } else {
            if (p2.y <= point.y) {
                if (orientation(p1, p2, point) === Orientation.CLOCKWISE) {
                    windingNumber--;
                }
            }
        }
    }

    return windingNumber !== 0;
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
 * @param {Point[]} points - Array of points
 * @returns {Object} {point1, point2, distance}
 */
function closestPairDivideConquer(points) {
    if (points.length < 2) return null;

    // Sort by x-coordinate
    const sortedX = [...points].sort((a, b) => a.x - b.x);

    function closestPairRecursive(pointsByX) {
        const n = pointsByX.length;

        // Base cases
        if (n <= 3) {
            let minDist = Infinity;
            let pair = [null, null];
            for (let i = 0; i < n; i++) {
                for (let j = i + 1; j < n; j++) {
                    const dist = pointsByX[i].distanceTo(pointsByX[j]);
                    if (dist < minDist) {
                        minDist = dist;
                        pair = [pointsByX[i], pointsByX[j]];
                    }
                }
            }
            return { point1: pair[0], point2: pair[1], distance: minDist };
        }

        // Divide
        const mid = Math.floor(n / 2);
        const midPoint = pointsByX[mid];

        const leftHalf = pointsByX.slice(0, mid);
        const rightHalf = pointsByX.slice(mid);

        const leftResult = closestPairRecursive(leftHalf);
        const rightResult = closestPairRecursive(rightHalf);

        // Find minimum from left and right
        let minResult = leftResult.distance < rightResult.distance ? leftResult : rightResult;

        // Check strip
        const strip = [];
        for (const p of pointsByX) {
            if (Math.abs(p.x - midPoint.x) < minResult.distance) {
                strip.push(p);
            }
        }

        // Sort strip by y
        strip.sort((a, b) => a.y - b.y);

        // Check points in strip
        for (let i = 0; i < strip.length; i++) {
            for (let j = i + 1; j < strip.length && (strip[j].y - strip[i].y) < minResult.distance; j++) {
                const dist = strip[i].distanceTo(strip[j]);
                if (dist < minResult.distance) {
                    minResult = { point1: strip[i], point2: strip[j], distance: dist };
                }
            }
        }

        return minResult;
    }

    return closestPairRecursive(sortedX);
}

/**
 * Calculate polygon area using Shoelace formula
 *
 * Time Complexity: O(n)
 *
 * @param {Point[]} polygon - Polygon vertices
 * @returns {number} Signed area (positive if CCW)
 */
function polygonArea(polygon) {
    if (polygon.length < 3) return 0;

    let area = 0;
    const n = polygon.length;

    for (let i = 0; i < n; i++) {
        const p1 = polygon[i];
        const p2 = polygon[(i + 1) % n];
        area += p1.x * p2.y - p2.x * p1.y;
    }

    return area / 2;
}

/**
 * Calculate polygon centroid
 *
 * Time Complexity: O(n)
 *
 * @param {Point[]} polygon - Polygon vertices
 * @returns {Point} Centroid point
 */
function polygonCentroid(polygon) {
    if (polygon.length === 0) return null;

    const area = polygonArea(polygon);
    if (Math.abs(area) < EPSILON) {
        // Degenerate case - return average
        let sumX = 0, sumY = 0;
        for (const p of polygon) {
            sumX += p.x;
            sumY += p.y;
        }
        return new Point(sumX / polygon.length, sumY / polygon.length);
    }

    let cx = 0, cy = 0;
    const n = polygon.length;

    for (let i = 0; i < n; i++) {
        const p1 = polygon[i];
        const p2 = polygon[(i + 1) % n];
        const cross = p1.x * p2.y - p2.x * p1.y;
        cx += (p1.x + p2.x) * cross;
        cy += (p1.y + p2.y) * cross;
    }

    const factor = 1 / (6 * area);
    return new Point(cx * factor, cy * factor);
}

/**
 * Calculate polygon perimeter
 *
 * Time Complexity: O(n)
 *
 * @param {Point[]} polygon - Polygon vertices
 * @returns {number} Perimeter length
 */
function polygonPerimeter(polygon) {
    if (polygon.length < 2) return 0;

    let perimeter = 0;
    const n = polygon.length;

    for (let i = 0; i < n; i++) {
        const p1 = polygon[i];
        const p2 = polygon[(i + 1) % n];
        perimeter += p1.distanceTo(p2);
    }

    return perimeter;
}

/**
 * Canvas Visualization Helper
 *
 * Provides methods for visualizing geometric structures on HTML5 Canvas
 */
class GeometryVisualizer {
    /**
     * Create visualizer
     * @param {HTMLCanvasElement} canvas - Canvas element
     * @param {Object} options - Visualization options
     */
    constructor(canvas, options = {}) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.options = {
            pointRadius: 4,
            pointColor: '#3498db',
            hullColor: '#e74c3c',
            lineWidth: 2,
            backgroundColor: '#ecf0f1',
            padding: 40,
            ...options
        };
    }

    /**
     * Clear canvas
     */
    clear() {
        this.ctx.fillStyle = this.options.backgroundColor;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }

    /**
     * Transform point to canvas coordinates
     * @param {Point} point - Point to transform
     * @param {Object} bounds - {minX, maxX, minY, maxY}
     * @returns {Object} {x, y} in canvas coordinates
     */
    toCanvasCoords(point, bounds) {
        const padding = this.options.padding;
        const width = this.canvas.width - 2 * padding;
        const height = this.canvas.height - 2 * padding;

        const rangeX = bounds.maxX - bounds.minX || 1;
        const rangeY = bounds.maxY - bounds.minY || 1;

        return {
            x: padding + (point.x - bounds.minX) / rangeX * width,
            y: this.canvas.height - padding - (point.y - bounds.minY) / rangeY * height
        };
    }

    /**
     * Calculate bounds for point set
     * @param {Point[]} points - Points to bound
     * @returns {Object} {minX, maxX, minY, maxY}
     */
    calculateBounds(points) {
        if (points.length === 0) {
            return { minX: 0, maxX: 1, minY: 0, maxY: 1 };
        }

        let minX = points[0].x, maxX = points[0].x;
        let minY = points[0].y, maxY = points[0].y;

        for (const p of points) {
            minX = Math.min(minX, p.x);
            maxX = Math.max(maxX, p.x);
            minY = Math.min(minY, p.y);
            maxY = Math.max(maxY, p.y);
        }

        // Add margin
        const marginX = (maxX - minX) * 0.1 || 1;
        const marginY = (maxY - minY) * 0.1 || 1;

        return {
            minX: minX - marginX,
            maxX: maxX + marginX,
            minY: minY - marginY,
            maxY: maxY + marginY
        };
    }

    /**
     * Draw a point
     * @param {Point} point - Point to draw
     * @param {Object} bounds - Coordinate bounds
     * @param {Object} options - Drawing options
     */
    drawPoint(point, bounds, options = {}) {
        const coords = this.toCanvasCoords(point, bounds);
        const radius = options.radius || this.options.pointRadius;
        const color = options.color || this.options.pointColor;

        this.ctx.fillStyle = color;
        this.ctx.beginPath();
        this.ctx.arc(coords.x, coords.y, radius, 0, 2 * Math.PI);
        this.ctx.fill();
    }

    /**
     * Draw multiple points
     * @param {Point[]} points - Points to draw
     * @param {Object} options - Drawing options
     */
    drawPoints(points, options = {}) {
        const bounds = this.calculateBounds(points);
        for (const point of points) {
            this.drawPoint(point, bounds, options);
        }
    }

    /**
     * Draw a polygon
     * @param {Point[]} polygon - Polygon vertices
     * @param {Object} bounds - Coordinate bounds
     * @param {Object} options - Drawing options
     */
    drawPolygon(polygon, bounds, options = {}) {
        if (polygon.length < 2) return;

        const color = options.color || this.options.hullColor;
        const lineWidth = options.lineWidth || this.options.lineWidth;
        const fill = options.fill || false;

        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = lineWidth;
        if (fill) {
            this.ctx.fillStyle = options.fillColor || color + '33';
        }

        this.ctx.beginPath();
        const start = this.toCanvasCoords(polygon[0], bounds);
        this.ctx.moveTo(start.x, start.y);

        for (let i = 1; i < polygon.length; i++) {
            const coords = this.toCanvasCoords(polygon[i], bounds);
            this.ctx.lineTo(coords.x, coords.y);
        }

        this.ctx.closePath();
        if (fill) {
            this.ctx.fill();
        }
        this.ctx.stroke();
    }

    /**
     * Visualize convex hull
     * @param {Point[]} points - All points
     * @param {Point[]} hull - Convex hull vertices
     * @param {Object} options - Drawing options
     */
    visualizeConvexHull(points, hull, options = {}) {
        this.clear();
        const bounds = this.calculateBounds(points);

        // Draw all points
        for (const point of points) {
            this.drawPoint(point, bounds, { color: this.options.pointColor });
        }

        // Draw hull
        this.drawPolygon(hull, bounds, {
            color: this.options.hullColor,
            fill: options.fill || false
        });

        // Draw hull points larger
        for (const point of hull) {
            this.drawPoint(point, bounds, {
                color: this.options.hullColor,
                radius: this.options.pointRadius * 1.5
            });
        }
    }

    /**
     * Visualize closest pair
     * @param {Point[]} points - All points
     * @param {Object} result - {point1, point2, distance}
     */
    visualizeClosestPair(points, result) {
        this.clear();
        const bounds = this.calculateBounds(points);

        // Draw all points
        for (const point of points) {
            this.drawPoint(point, bounds);
        }

        // Draw line between closest pair
        if (result && result.point1 && result.point2) {
            const p1 = this.toCanvasCoords(result.point1, bounds);
            const p2 = this.toCanvasCoords(result.point2, bounds);

            this.ctx.strokeStyle = this.options.hullColor;
            this.ctx.lineWidth = this.options.lineWidth;
            this.ctx.beginPath();
            this.ctx.moveTo(p1.x, p1.y);
            this.ctx.lineTo(p2.x, p2.y);
            this.ctx.stroke();

            // Highlight closest points
            this.drawPoint(result.point1, bounds, {
                color: this.options.hullColor,
                radius: this.options.pointRadius * 2
            });
            this.drawPoint(result.point2, bounds, {
                color: this.options.hullColor,
                radius: this.options.pointRadius * 2
            });

            // Draw distance label
            this.ctx.fillStyle = '#2c3e50';
            this.ctx.font = '14px monospace';
            this.ctx.fillText(
                `Distance: ${result.distance.toFixed(3)}`,
                this.options.padding,
                this.options.padding / 2
            );
        }
    }
}

/**
 * Performance Benchmarking Suite
 */
class GeometryBenchmark {
    /**
     * Generate random points
     * @param {number} count - Number of points
     * @param {number} range - Coordinate range
     * @returns {Point[]} Random points
     */
    static generateRandomPoints(count, range = 1000) {
        const points = [];
        for (let i = 0; i < count; i++) {
            points.push(new Point(
                Math.random() * range,
                Math.random() * range
            ));
        }
        return points;
    }

    /**
     * Generate points on circle
     * @param {number} count - Number of points
     * @param {number} radius - Circle radius
     * @returns {Point[]} Points on circle
     */
    static generateCirclePoints(count, radius = 500) {
        const points = [];
        for (let i = 0; i < count; i++) {
            const angle = (2 * Math.PI * i) / count;
            points.push(new Point(
                radius * Math.cos(angle) + radius,
                radius * Math.sin(angle) + radius
            ));
        }
        return points;
    }

    /**
     * Benchmark convex hull algorithms
     * @param {Point[]} points - Test points
     * @returns {Object} Benchmark results
     */
    static benchmarkConvexHull(points) {
        const results = {};

        // Graham Scan
        const grahamStart = performance.now();
        const grahamHull = convexHullGrahamScan(points);
        const grahamTime = performance.now() - grahamStart;
        results.grahamScan = { time: grahamTime, hullSize: grahamHull.length };

        // Jarvis March
        const jarvisStart = performance.now();
        const jarvisHull = convexHullJarvisMarch(points);
        const jarvisTime = performance.now() - jarvisStart;
        results.jarvisMarch = { time: jarvisTime, hullSize: jarvisHull.length };

        // QuickHull
        const quickStart = performance.now();
        const quickHull = convexHullQuickHull(points);
        const quickTime = performance.now() - quickStart;
        results.quickHull = { time: quickTime, hullSize: quickHull.length };

        return results;
    }

    /**
     * Benchmark point-in-polygon algorithms
     * @param {Point[]} testPoints - Points to test
     * @param {Point[]} polygon - Polygon
     * @returns {Object} Benchmark results
     */
    static benchmarkPointInPolygon(testPoints, polygon) {
        // Ray casting
        const rayCastStart = performance.now();
        let rayCastCount = 0;
        for (const p of testPoints) {
            if (pointInPolygonRayCasting(p, polygon)) rayCastCount++;
        }
        const rayCastTime = performance.now() - rayCastStart;

        // Winding number
        const windingStart = performance.now();
        let windingCount = 0;
        for (const p of testPoints) {
            if (pointInPolygonWindingNumber(p, polygon)) windingCount++;
        }
        const windingTime = performance.now() - windingStart;

        return {
            rayCasting: { time: rayCastTime, insideCount: rayCastCount },
            windingNumber: { time: windingTime, insideCount: windingCount }
        };
    }
}

// Export for use in Node.js and browsers
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        Point,
        Orientation,
        EPSILON,
        orientation,
        onSegment,
        segmentsIntersect,
        convexHullGrahamScan,
        convexHullJarvisMarch,
        convexHullQuickHull,
        pointInPolygonRayCasting,
        pointInPolygonWindingNumber,
        closestPairDivideConquer,
        polygonArea,
        polygonCentroid,
        polygonPerimeter,
        GeometryVisualizer,
        GeometryBenchmark
    };
}
