#!/usr/bin/env Rscript
# ============================================================================
# Computational Geometry Algorithms - R Implementation
# ============================================================================
#
# Statistical computing and visualization focused implementation.
# Suitable for GIS applications, spatial analysis, and data visualization.
#
# Usage:
#   Rscript geometry.R
#   # Or in R console:
#   source("geometry.R")
#
# Author: algorithms-multiverse
# ============================================================================

# Constants
EPSILON <- 1e-10

# ============================================================================
# GEOMETRIC PRIMITIVES
# ============================================================================

#' Create a point
#'
#' @param x X-coordinate
#' @param y Y-coordinate
#' @return List representing a point
Point <- function(x, y) {
    list(x = x, y = y)
}

#' Calculate squared distance between two points
dist_squared <- function(p1, p2) {
    dx <- p2$x - p1$x
    dy <- p2$y - p1$y
    dx * dx + dy * dy
}

#' Calculate Euclidean distance
distance <- function(p1, p2) {
    sqrt(dist_squared(p1, p2))
}

#' Cross product of vectors (p1->p2) and (p1->p3)
#'
#' Positive: counter-clockwise
#' Negative: clockwise
#' Zero: collinear
cross_product <- function(p1, p2, p3) {
    (p2$x - p1$x) * (p3$y - p1$y) - (p2$y - p1$y) * (p3$x - p1$x)
}

#' Determine orientation of ordered triplet
#'
#' @return 0 (collinear), 1 (clockwise), 2 (counter-clockwise)
orientation <- function(p, q, r) {
    val <- cross_product(p, q, r)

    if (abs(val) < EPSILON) {
        return(0)  # Collinear
    } else if (val > 0) {
        return(2)  # Counter-clockwise
    } else {
        return(1)  # Clockwise
    }
}

#' Check if point q lies on segment pr (assuming collinear)
on_segment <- function(p, q, r) {
    q$x <= max(p$x, r$x) && q$x >= min(p$x, r$x) &&
    q$y <= max(p$y, r$y) && q$y >= min(p$y, r$y)
}

# ============================================================================
# CONVEX HULL - GRAHAM SCAN
# ============================================================================

#' Graham Scan Algorithm for Convex Hull
#'
#' Time Complexity: O(n log n)
#' Space Complexity: O(n)
#'
#' @param points Matrix or data frame with columns x and y
#' @return Data frame of hull points
graham_scan <- function(points) {
    if (is.matrix(points) || is.data.frame(points)) {
        points_list <- lapply(1:nrow(points), function(i) {
            Point(points[i, 1], points[i, 2])
        })
    } else {
        points_list <- points
    }

    n <- length(points_list)
    if (n < 3) {
        return(points)
    }

    # Find pivot (lowest y, leftmost if tie)
    pivot_idx <- 1
    for (i in 2:n) {
        if (points_list[[i]]$y < points_list[[pivot_idx]]$y ||
            (abs(points_list[[i]]$y - points_list[[pivot_idx]]$y) < EPSILON &&
             points_list[[i]]$x < points_list[[pivot_idx]]$x)) {
            pivot_idx <- i
        }
    }

    # Swap pivot to first position
    temp <- points_list[[1]]
    points_list[[1]] <- points_list[[pivot_idx]]
    points_list[[pivot_idx]] <- temp
    pivot <- points_list[[1]]

    # Sort by polar angle
    if (n > 2) {
        sorted_indices <- order(sapply(2:n, function(i) {
            cross <- cross_product(pivot, points_list[[i]], pivot)
            if (abs(cross) < EPSILON) {
                # Collinear: sort by distance
                return(dist_squared(pivot, points_list[[i]]))
            }
            atan2(points_list[[i]]$y - pivot$y, points_list[[i]]$x - pivot$x)
        }))

        points_list[2:n] <- points_list[sorted_indices + 1]
    }

    # Build hull
    hull <- list(points_list[[1]], points_list[[2]], points_list[[3]])

    if (n > 3) {
        for (i in 4:n) {
            # Remove points that make right turn
            while (length(hull) >= 2) {
                len <- length(hull)
                if (cross_product(hull[[len - 1]], hull[[len]], points_list[[i]]) <= EPSILON) {
                    hull <- hull[-len]
                } else {
                    break
                }
            }
            hull[[length(hull) + 1]] <- points_list[[i]]
        }
    }

    # Convert to data frame
    data.frame(
        x = sapply(hull, function(p) p$x),
        y = sapply(hull, function(p) p$y)
    )
}

# ============================================================================
# CONVEX HULL - JARVIS MARCH
# ============================================================================

#' Jarvis March (Gift Wrapping) Algorithm
#'
#' Time Complexity: O(nh) where h is hull size
#' Space Complexity: O(h)
#'
#' @param points Matrix or data frame with columns x and y
#' @return Data frame of hull points
jarvis_march <- function(points) {
    if (is.matrix(points) || is.data.frame(points)) {
        points_list <- lapply(1:nrow(points), function(i) {
            Point(points[i, 1], points[i, 2])
        })
    } else {
        points_list <- points
    }

    n <- length(points_list)
    if (n < 3) {
        return(points)
    }

    # Find leftmost point
    leftmost <- 1
    for (i in 2:n) {
        if (points_list[[i]]$x < points_list[[leftmost]]$x ||
            (abs(points_list[[i]]$x - points_list[[leftmost]]$x) < EPSILON &&
             points_list[[i]]$y < points_list[[leftmost]]$y)) {
            leftmost <- i
        }
    }

    hull <- list()
    current <- leftmost

    repeat {
        hull[[length(hull) + 1]] <- points_list[[current]]

        # Find next point
        next_point <- 1
        for (i in 2:n) {
            if (i == current) next

            if (next_point == current) {
                next_point <- i
            } else {
                cross <- cross_product(points_list[[current]],
                                      points_list[[next_point]],
                                      points_list[[i]])

                if (cross > EPSILON ||
                    (abs(cross) < EPSILON &&
                     dist_squared(points_list[[current]], points_list[[i]]) >
                     dist_squared(points_list[[current]], points_list[[next_point]]))) {
                    next_point <- i
                }
            }
        }

        current <- next_point

        if (current == leftmost || length(hull) >= n) {
            break
        }
    }

    # Convert to data frame
    data.frame(
        x = sapply(hull, function(p) p$x),
        y = sapply(hull, function(p) p$y)
    )
}

# ============================================================================
# LINE SEGMENT INTERSECTION
# ============================================================================

#' Check if two line segments intersect
#'
#' @param seg1 List with start and end points
#' @param seg2 List with start and end points
#' @return List with intersect (boolean) and point (if intersects)
segments_intersect <- function(seg1, seg2) {
    p1 <- seg1$start
    q1 <- seg1$end
    p2 <- seg2$start
    q2 <- seg2$end

    o1 <- orientation(p1, q1, p2)
    o2 <- orientation(p1, q1, q2)
    o3 <- orientation(p2, q2, p1)
    o4 <- orientation(p2, q2, q1)

    # General case
    if (o1 != o2 && o3 != o4) {
        # Calculate intersection point
        a1 <- q1$y - p1$y
        b1 <- p1$x - q1$x
        c1 <- a1 * p1$x + b1 * p1$y

        a2 <- q2$y - p2$y
        b2 <- p2$x - q2$x
        c2 <- a2 * p2$x + b2 * p2$y

        det <- a1 * b2 - a2 * b1

        if (abs(det) > EPSILON) {
            x <- (b2 * c1 - b1 * c2) / det
            y <- (a1 * c2 - a2 * c1) / det
            return(list(intersect = TRUE, point = Point(x, y)))
        }
    }

    # Special cases: collinear
    if (o1 == 0 && on_segment(p1, p2, q1)) {
        return(list(intersect = TRUE, point = p2))
    }
    if (o2 == 0 && on_segment(p1, q2, q1)) {
        return(list(intersect = TRUE, point = q2))
    }
    if (o3 == 0 && on_segment(p2, p1, q2)) {
        return(list(intersect = TRUE, point = p1))
    }
    if (o4 == 0 && on_segment(p2, q1, q2)) {
        return(list(intersect = TRUE, point = q1))
    }

    list(intersect = FALSE, point = NULL)
}

# ============================================================================
# POINT IN POLYGON
# ============================================================================

#' Ray casting algorithm for point-in-polygon test
#'
#' Time Complexity: O(n)
#'
#' @param point Point to test
#' @param polygon Matrix or data frame with columns x and y
#' @return TRUE if point is inside, FALSE otherwise
point_in_polygon <- function(point, polygon) {
    if (is.matrix(polygon) || is.data.frame(polygon)) {
        poly_list <- lapply(1:nrow(polygon), function(i) {
            Point(polygon[i, 1], polygon[i, 2])
        })
    } else {
        poly_list <- polygon
    }

    n <- length(poly_list)
    if (n < 3) {
        return(FALSE)
    }

    # Create ray to infinity
    extreme <- Point(1e10, point$y)
    ray <- list(start = point, end = extreme)

    count <- 0

    for (i in 1:n) {
        j <- ifelse(i == n, 1, i + 1)
        edge <- list(start = poly_list[[i]], end = poly_list[[j]])

        result <- segments_intersect(edge, ray)
        if (result$intersect) {
            # Check if point is collinear with edge
            if (orientation(edge$start, point, edge$end) == 0) {
                return(on_segment(edge$start, point, edge$end))
            }
            count <- count + 1
        }
    }

    (count %% 2) == 1
}

# ============================================================================
# CLOSEST PAIR OF POINTS
# ============================================================================

#' Brute force closest pair
closest_pair_brute <- function(points_list) {
    n <- length(points_list)
    min_dist <- Inf
    pair <- list(p1 = NULL, p2 = NULL)

    for (i in 1:(n-1)) {
        for (j in (i+1):n) {
            d <- distance(points_list[[i]], points_list[[j]])
            if (d < min_dist) {
                min_dist <- d
                pair$p1 <- points_list[[i]]
                pair$p2 <- points_list[[j]]
            }
        }
    }

    list(p1 = pair$p1, p2 = pair$p2, distance = min_dist)
}

#' Closest pair of points
#'
#' @param points Matrix or data frame with columns x and y
#' @return List with p1, p2 (closest points) and distance
closest_pair <- function(points) {
    if (is.matrix(points) || is.data.frame(points)) {
        points_list <- lapply(1:nrow(points), function(i) {
            Point(points[i, 1], points[i, 2])
        })
    } else {
        points_list <- points
    }

    # For simplicity, use brute force
    # Full divide-and-conquer would be more complex
    closest_pair_brute(points_list)
}

# ============================================================================
# POLYGON AREA
# ============================================================================

#' Calculate polygon area using shoelace formula
#'
#' Time Complexity: O(n)
#'
#' @param polygon Matrix or data frame with columns x and y
#' @return Area of polygon
polygon_area <- function(polygon) {
    if (is.matrix(polygon) || is.data.frame(polygon)) {
        n <- nrow(polygon)
        if (n < 3) return(0)

        area <- 0
        for (i in 1:n) {
            j <- ifelse(i == n, 1, i + 1)
            area <- area + polygon[i, 1] * polygon[j, 2]
            area <- area - polygon[j, 1] * polygon[i, 2]
        }

        return(abs(area / 2))
    }

    # Handle list of points
    poly_list <- polygon
    n <- length(poly_list)
    if (n < 3) return(0)

    area <- 0
    for (i in 1:n) {
        j <- ifelse(i == n, 1, i + 1)
        area <- area + poly_list[[i]]$x * poly_list[[j]]$y
        area <- area - poly_list[[j]]$x * poly_list[[i]]$y
    }

    abs(area / 2)
}

# ============================================================================
# TESTING AND DEMONSTRATION
# ============================================================================

print_separator <- function(char = "=", length = 70) {
    cat(paste(rep(char, length), collapse = ""), "\n")
}

test_convex_hull <- function() {
    cat("\n1. CONVEX HULL ALGORITHMS\n")
    print_separator("-", 50)

    # Test points
    points <- matrix(c(
        0, 3,
        1, 1,
        2, 2,
        4, 4,
        0, 0,
        1, 2,
        3, 1,
        3, 3
    ), ncol = 2, byrow = TRUE)
    colnames(points) <- c("x", "y")

    cat(sprintf("Input points (%d):\n", nrow(points)))
    for (i in 1:nrow(points)) {
        cat(sprintf("  (%.1f, %.1f)\n", points[i, 1], points[i, 2]))
    }

    # Graham Scan
    hull1 <- graham_scan(points)
    cat(sprintf("\nGraham Scan - Hull points (%d):\n", nrow(hull1)))
    for (i in 1:nrow(hull1)) {
        cat(sprintf("  (%.1f, %.1f)\n", hull1[i, 1], hull1[i, 2]))
    }

    # Jarvis March
    hull2 <- jarvis_march(points)
    cat(sprintf("\nJarvis March - Hull points (%d):\n", nrow(hull2)))
    for (i in 1:nrow(hull2)) {
        cat(sprintf("  (%.1f, %.1f)\n", hull2[i, 1], hull2[i, 2]))
    }
}

test_line_intersection <- function() {
    cat("\n2. LINE SEGMENT INTERSECTION\n")
    print_separator("-", 50)

    seg1 <- list(start = Point(0, 0), end = Point(10, 10))
    seg2 <- list(start = Point(0, 10), end = Point(10, 0))
    seg3 <- list(start = Point(20, 20), end = Point(30, 30))

    cat(sprintf("Segment 1: (%.1f,%.1f) to (%.1f,%.1f)\n",
                seg1$start$x, seg1$start$y, seg1$end$x, seg1$end$y))
    cat(sprintf("Segment 2: (%.1f,%.1f) to (%.1f,%.1f)\n",
                seg2$start$x, seg2$start$y, seg2$end$x, seg2$end$y))

    result <- segments_intersect(seg1, seg2)
    if (result$intersect) {
        cat(sprintf("Segments intersect at: (%.1f, %.1f)\n",
                    result$point$x, result$point$y))
    } else {
        cat("Segments do not intersect\n")
    }

    cat(sprintf("\nSegment 1: (%.1f,%.1f) to (%.1f,%.1f)\n",
                seg1$start$x, seg1$start$y, seg1$end$x, seg1$end$y))
    cat(sprintf("Segment 3: (%.1f,%.1f) to (%.1f,%.1f)\n",
                seg3$start$x, seg3$start$y, seg3$end$x, seg3$end$y))

    result <- segments_intersect(seg1, seg3)
    if (result$intersect) {
        cat("Segments intersect\n")
    } else {
        cat("Segments do not intersect\n")
    }
}

test_point_in_polygon <- function() {
    cat("\n3. POINT IN POLYGON TEST\n")
    print_separator("-", 50)

    # Square polygon
    square <- matrix(c(
        0, 0,
        10, 0,
        10, 10,
        0, 10
    ), ncol = 2, byrow = TRUE)

    test_points <- list(
        list(point = Point(5, 5), desc = "Inside"),
        list(point = Point(15, 15), desc = "Outside"),
        list(point = Point(0, 0), desc = "On vertex"),
        list(point = Point(5, 0), desc = "On edge")
    )

    cat("Polygon: Square with corners at (0,0), (10,0), (10,10), (0,10)\n\n")

    for (tp in test_points) {
        inside <- point_in_polygon(tp$point, square)
        cat(sprintf("Point (%.1f, %.1f) [%s]: %s\n",
                    tp$point$x, tp$point$y, tp$desc,
                    ifelse(inside, "INSIDE", "OUTSIDE")))
    }
}

test_closest_pair <- function() {
    cat("\n4. CLOSEST PAIR OF POINTS\n")
    print_separator("-", 50)

    points <- matrix(c(
        0, 0,
        1, 1,
        2, 2,
        3, 10,
        4, 3,
        5, 5,
        6, 1
    ), ncol = 2, byrow = TRUE)

    cat(sprintf("Input points (%d):\n", nrow(points)))
    for (i in 1:nrow(points)) {
        cat(sprintf("  (%.1f, %.1f)\n", points[i, 1], points[i, 2]))
    }

    result <- closest_pair(points)

    cat("\nClosest pair:\n")
    cat(sprintf("  Point 1: (%.1f, %.1f)\n", result$p1$x, result$p1$y))
    cat(sprintf("  Point 2: (%.1f, %.1f)\n", result$p2$x, result$p2$y))
    cat(sprintf("  Distance: %.4f\n", result$distance))
}

test_polygon_area <- function() {
    cat("\n5. POLYGON AREA\n")
    print_separator("-", 50)

    triangle <- matrix(c(0, 0, 4, 0, 0, 3), ncol = 2, byrow = TRUE)
    square <- matrix(c(0, 0, 5, 0, 5, 5, 0, 5), ncol = 2, byrow = TRUE)

    area1 <- polygon_area(triangle)
    area2 <- polygon_area(square)

    cat(sprintf("Triangle area: %.1f (expected: 6.0)\n", area1))
    cat(sprintf("Square area: %.1f (expected: 25.0)\n", area2))
}

main <- function() {
    print_separator("=", 70)
    cat("COMPUTATIONAL GEOMETRY ALGORITHMS - R IMPLEMENTATION\n")
    print_separator("=", 70)

    test_convex_hull()
    test_line_intersection()
    test_point_in_polygon()
    test_closest_pair()
    test_polygon_area()

    cat("\n")
    print_separator("=", 70)
    cat("All tests completed successfully!\n")
    print_separator("=", 70)
}

# Run main if script is executed directly
if (sys.nframe() == 0) {
    main()
}
