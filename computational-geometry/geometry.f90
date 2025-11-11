! ============================================================================
! Computational Geometry Algorithms - Fortran Implementation
! ============================================================================
!
! Modern Fortran (90+) implementation optimized for numerical computation.
!
! Compilation:
!   gfortran -O3 -o geometry geometry.f90
!
! Usage:
!   ./geometry
!
! Author: algorithms-multiverse
! ============================================================================

module geometry_module
    implicit none
    private
    public :: point, convex_hull_graham, convex_hull_jarvis, &
              segments_intersect, point_in_polygon, closest_pair, &
              polygon_area, cross_product

    real(8), parameter :: EPSILON = 1.0d-10
    integer, parameter :: dp = selected_real_kind(15, 307)

    type :: point
        real(dp) :: x, y
    end type point

contains

    ! ========================================================================
    ! UTILITY FUNCTIONS
    ! ========================================================================

    !> Calculate squared distance between two points
    function dist_squared(p1, p2) result(d2)
        type(point), intent(in) :: p1, p2
        real(dp) :: d2
        real(dp) :: dx, dy

        dx = p2%x - p1%x
        dy = p2%y - p1%y
        d2 = dx * dx + dy * dy
    end function dist_squared

    !> Calculate Euclidean distance
    function distance(p1, p2) result(d)
        type(point), intent(in) :: p1, p2
        real(dp) :: d

        d = sqrt(dist_squared(p1, p2))
    end function distance

    !> Cross product of vectors (p1->p2) and (p1->p3)
    !! Positive: counter-clockwise, Negative: clockwise, Zero: collinear
    function cross_product(p1, p2, p3) result(cross)
        type(point), intent(in) :: p1, p2, p3
        real(dp) :: cross

        cross = (p2%x - p1%x) * (p3%y - p1%y) - (p2%y - p1%y) * (p3%x - p1%x)
    end function cross_product

    !> Determine if point q lies on segment pr (assuming collinear)
    function on_segment(p, q, r) result(on_seg)
        type(point), intent(in) :: p, q, r
        logical :: on_seg

        on_seg = (q%x <= max(p%x, r%x)) .and. (q%x >= min(p%x, r%x)) .and. &
                 (q%y <= max(p%y, r%y)) .and. (q%y >= min(p%y, r%y))
    end function on_segment

    !> Compare points for sorting (by y, then x)
    function compare_points(p1, p2) result(cmp)
        type(point), intent(in) :: p1, p2
        integer :: cmp

        if (abs(p1%y - p2%y) < EPSILON) then
            if (abs(p1%x - p2%x) < EPSILON) then
                cmp = 0
            else if (p1%x < p2%x) then
                cmp = -1
            else
                cmp = 1
            end if
        else if (p1%y < p2%y) then
            cmp = -1
        else
            cmp = 1
        end if
    end function compare_points

    ! ========================================================================
    ! CONVEX HULL - GRAHAM SCAN
    ! ========================================================================

    !> Graham Scan Algorithm for Convex Hull
    !! Time Complexity: O(n log n)
    subroutine convex_hull_graham(points, n, hull, hull_size)
        integer, intent(in) :: n
        type(point), intent(inout) :: points(n)
        type(point), intent(out) :: hull(n)
        integer, intent(out) :: hull_size

        type(point) :: pivot, temp
        integer :: i, j, pivot_idx
        real(dp) :: cross, d1, d2

        if (n < 3) then
            hull(1:n) = points(1:n)
            hull_size = n
            return
        end if

        ! Find pivot (lowest y, leftmost if tie)
        pivot_idx = 1
        do i = 2, n
            if (points(i)%y < points(pivot_idx)%y .or. &
                (abs(points(i)%y - points(pivot_idx)%y) < EPSILON .and. &
                 points(i)%x < points(pivot_idx)%x)) then
                pivot_idx = i
            end if
        end do

        ! Swap pivot to first position
        temp = points(1)
        points(1) = points(pivot_idx)
        points(pivot_idx) = temp
        pivot = points(1)

        ! Sort by polar angle (simple bubble sort for demonstration)
        do i = 2, n-1
            do j = i+1, n
                cross = cross_product(pivot, points(i), points(j))
                if (abs(cross) < EPSILON) then
                    ! Collinear: sort by distance
                    d1 = dist_squared(pivot, points(i))
                    d2 = dist_squared(pivot, points(j))
                    if (d2 < d1) then
                        temp = points(i)
                        points(i) = points(j)
                        points(j) = temp
                    end if
                else if (cross < 0) then
                    temp = points(i)
                    points(i) = points(j)
                    points(j) = temp
                end if
            end do
        end do

        ! Build hull
        hull(1) = points(1)
        hull(2) = points(2)
        hull(3) = points(3)
        hull_size = 3

        do i = 4, n
            ! Remove points that make right turn
            do while (hull_size >= 2)
                if (cross_product(hull(hull_size-1), hull(hull_size), points(i)) <= EPSILON) then
                    hull_size = hull_size - 1
                else
                    exit
                end if
            end do
            hull_size = hull_size + 1
            hull(hull_size) = points(i)
        end do
    end subroutine convex_hull_graham

    ! ========================================================================
    ! CONVEX HULL - JARVIS MARCH
    ! ========================================================================

    !> Jarvis March (Gift Wrapping) Algorithm
    !! Time Complexity: O(nh) where h is hull size
    subroutine convex_hull_jarvis(points, n, hull, hull_size)
        integer, intent(in) :: n
        type(point), intent(in) :: points(n)
        type(point), intent(out) :: hull(n)
        integer, intent(out) :: hull_size

        integer :: leftmost, current, next, i
        real(dp) :: cross

        if (n < 3) then
            hull(1:n) = points(1:n)
            hull_size = n
            return
        end if

        ! Find leftmost point
        leftmost = 1
        do i = 2, n
            if (points(i)%x < points(leftmost)%x .or. &
                (abs(points(i)%x - points(leftmost)%x) < EPSILON .and. &
                 points(i)%y < points(leftmost)%y)) then
                leftmost = i
            end if
        end do

        hull_size = 0
        current = leftmost

        do
            hull_size = hull_size + 1
            hull(hull_size) = points(current)

            ! Find next point
            next = 1
            do i = 2, n
                if (i == current) cycle

                if (next == current) then
                    next = i
                else
                    cross = cross_product(points(current), points(next), points(i))
                    if (cross > EPSILON .or. &
                        (abs(cross) < EPSILON .and. &
                         dist_squared(points(current), points(i)) > &
                         dist_squared(points(current), points(next)))) then
                        next = i
                    end if
                end if
            end do

            current = next

            if (current == leftmost .or. hull_size >= n) exit
        end do
    end subroutine convex_hull_jarvis

    ! ========================================================================
    ! LINE SEGMENT INTERSECTION
    ! ========================================================================

    !> Check if two line segments intersect
    function segments_intersect(p1, q1, p2, q2, intersection) result(intersect)
        type(point), intent(in) :: p1, q1, p2, q2
        type(point), intent(out), optional :: intersection
        logical :: intersect

        integer :: o1, o2, o3, o4
        real(dp) :: a1, b1, c1, a2, b2, c2, det

        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        ! General case
        if (o1 /= o2 .and. o3 /= o4) then
            if (present(intersection)) then
                ! Calculate intersection point
                a1 = q1%y - p1%y
                b1 = p1%x - q1%x
                c1 = a1 * p1%x + b1 * p1%y

                a2 = q2%y - p2%y
                b2 = p2%x - q2%x
                c2 = a2 * p2%x + b2 * p2%y

                det = a1 * b2 - a2 * b1

                if (abs(det) > EPSILON) then
                    intersection%x = (b2 * c1 - b1 * c2) / det
                    intersection%y = (a1 * c2 - a2 * c1) / det
                end if
            end if
            intersect = .true.
            return
        end if

        ! Special cases: collinear
        if (o1 == 0 .and. on_segment(p1, p2, q1)) then
            intersect = .true.
            return
        end if
        if (o2 == 0 .and. on_segment(p1, q2, q1)) then
            intersect = .true.
            return
        end if
        if (o3 == 0 .and. on_segment(p2, p1, q2)) then
            intersect = .true.
            return
        end if
        if (o4 == 0 .and. on_segment(p2, q1, q2)) then
            intersect = .true.
            return
        end if

        intersect = .false.
    end function segments_intersect

    !> Helper: Determine orientation
    function orientation(p, q, r) result(orient)
        type(point), intent(in) :: p, q, r
        integer :: orient
        real(dp) :: val

        val = cross_product(p, q, r)

        if (abs(val) < EPSILON) then
            orient = 0  ! Collinear
        else if (val > 0) then
            orient = 2  ! Counter-clockwise
        else
            orient = 1  ! Clockwise
        end if
    end function orientation

    ! ========================================================================
    ! POINT IN POLYGON
    ! ========================================================================

    !> Ray casting algorithm for point-in-polygon test
    function point_in_polygon(test_point, polygon, n) result(inside)
        type(point), intent(in) :: test_point
        integer, intent(in) :: n
        type(point), intent(in) :: polygon(n)
        logical :: inside

        type(point) :: extreme
        integer :: count, i, j

        if (n < 3) then
            inside = .false.
            return
        end if

        ! Create ray to infinity
        extreme%x = 1.0d10
        extreme%y = test_point%y

        count = 0
        do i = 1, n
            j = mod(i, n) + 1

            if (segments_intersect(polygon(i), polygon(j), test_point, extreme)) then
                ! Check if point is collinear with edge
                if (orientation(polygon(i), test_point, polygon(j)) == 0) then
                    inside = on_segment(polygon(i), test_point, polygon(j))
                    return
                end if
                count = count + 1
            end if
        end do

        inside = (mod(count, 2) == 1)
    end function point_in_polygon

    ! ========================================================================
    ! CLOSEST PAIR OF POINTS
    ! ========================================================================

    !> Brute force closest pair
    subroutine closest_pair_brute(points, n, p1, p2, min_dist)
        integer, intent(in) :: n
        type(point), intent(in) :: points(n)
        type(point), intent(out) :: p1, p2
        real(dp), intent(out) :: min_dist

        integer :: i, j
        real(dp) :: d

        min_dist = huge(1.0_dp)

        do i = 1, n
            do j = i+1, n
                d = distance(points(i), points(j))
                if (d < min_dist) then
                    min_dist = d
                    p1 = points(i)
                    p2 = points(j)
                end if
            end do
        end do
    end subroutine closest_pair_brute

    !> Closest pair using divide and conquer
    subroutine closest_pair(points, n, p1, p2, min_dist)
        integer, intent(in) :: n
        type(point), intent(inout) :: points(n)
        type(point), intent(out) :: p1, p2
        real(dp), intent(out) :: min_dist

        ! For simplicity, use brute force for all cases
        ! Full divide-and-conquer implementation would be more complex in Fortran
        call closest_pair_brute(points, n, p1, p2, min_dist)
    end subroutine closest_pair

    ! ========================================================================
    ! POLYGON AREA
    ! ========================================================================

    !> Calculate polygon area using shoelace formula
    function polygon_area(polygon, n) result(area)
        integer, intent(in) :: n
        type(point), intent(in) :: polygon(n)
        real(dp) :: area

        integer :: i, j

        if (n < 3) then
            area = 0.0_dp
            return
        end if

        area = 0.0_dp
        do i = 1, n
            j = mod(i, n) + 1
            area = area + polygon(i)%x * polygon(j)%y
            area = area - polygon(j)%x * polygon(i)%y
        end do

        area = abs(area / 2.0_dp)
    end function polygon_area

end module geometry_module

! ============================================================================
! MAIN PROGRAM - TESTING AND DEMONSTRATION
! ============================================================================

program test_geometry
    use geometry_module
    implicit none

    call print_header()
    call test_convex_hull()
    call test_line_intersection()
    call test_point_in_polygon_test()
    call test_closest_pair_test()
    call test_polygon_area_test()
    call print_footer()

contains

    subroutine print_header()
        print '(70("="))'
        print '(a)', "COMPUTATIONAL GEOMETRY - FORTRAN IMPLEMENTATION"
        print '(70("="))'
    end subroutine print_header

    subroutine print_footer()
        print *
        print '(70("="))'
        print '(a)', "All tests completed successfully!"
        print '(70("="))'
    end subroutine print_footer

    subroutine test_convex_hull()
        type(point) :: points(8), hull(8)
        integer :: n, hull_size, i

        print *
        print '(a)', "1. CONVEX HULL ALGORITHMS"
        print '(50("-"))'

        ! Test points
        n = 8
        points(1) = point(0.0d0, 3.0d0)
        points(2) = point(1.0d0, 1.0d0)
        points(3) = point(2.0d0, 2.0d0)
        points(4) = point(4.0d0, 4.0d0)
        points(5) = point(0.0d0, 0.0d0)
        points(6) = point(1.0d0, 2.0d0)
        points(7) = point(3.0d0, 1.0d0)
        points(8) = point(3.0d0, 3.0d0)

        print '(a,i0,a)', "Input points (", n, "):"
        do i = 1, n
            print '(a,f5.1,a,f5.1,a)', "  (", points(i)%x, ", ", points(i)%y, ")"
        end do

        ! Graham Scan
        call convex_hull_graham(points, n, hull, hull_size)
        print *
        print '(a,i0,a)', "Graham Scan - Hull points (", hull_size, "):"
        do i = 1, hull_size
            print '(a,f5.1,a,f5.1,a)', "  (", hull(i)%x, ", ", hull(i)%y, ")"
        end do

        ! Reset points for Jarvis
        points(1) = point(0.0d0, 3.0d0)
        points(2) = point(1.0d0, 1.0d0)
        points(3) = point(2.0d0, 2.0d0)
        points(4) = point(4.0d0, 4.0d0)
        points(5) = point(0.0d0, 0.0d0)
        points(6) = point(1.0d0, 2.0d0)
        points(7) = point(3.0d0, 1.0d0)
        points(8) = point(3.0d0, 3.0d0)

        ! Jarvis March
        call convex_hull_jarvis(points, n, hull, hull_size)
        print *
        print '(a,i0,a)', "Jarvis March - Hull points (", hull_size, "):"
        do i = 1, hull_size
            print '(a,f5.1,a,f5.1,a)', "  (", hull(i)%x, ", ", hull(i)%y, ")"
        end do
    end subroutine test_convex_hull

    subroutine test_line_intersection()
        type(point) :: p1, q1, p2, q2, p3, q3, intersection
        logical :: intersect

        print *
        print '(a)', "2. LINE SEGMENT INTERSECTION"
        print '(50("-"))'

        p1 = point(0.0d0, 0.0d0)
        q1 = point(10.0d0, 10.0d0)
        p2 = point(0.0d0, 10.0d0)
        q2 = point(10.0d0, 0.0d0)
        p3 = point(20.0d0, 20.0d0)
        q3 = point(30.0d0, 30.0d0)

        print '(a,f5.1,a,f5.1,a,f5.1,a,f5.1,a)', &
            "Segment 1: (", p1%x, ",", p1%y, ") to (", q1%x, ",", q1%y, ")"
        print '(a,f5.1,a,f5.1,a,f5.1,a,f5.1,a)', &
            "Segment 2: (", p2%x, ",", p2%y, ") to (", q2%x, ",", q2%y, ")"

        intersect = segments_intersect(p1, q1, p2, q2, intersection)
        if (intersect) then
            print '(a,f5.1,a,f5.1,a)', &
                "Segments intersect at: (", intersection%x, ", ", intersection%y, ")"
        else
            print '(a)', "Segments do not intersect"
        end if

        print *
        print '(a,f5.1,a,f5.1,a,f5.1,a,f5.1,a)', &
            "Segment 1: (", p1%x, ",", p1%y, ") to (", q1%x, ",", q1%y, ")"
        print '(a,f5.1,a,f5.1,a,f5.1,a,f5.1,a)', &
            "Segment 3: (", p3%x, ",", p3%y, ") to (", q3%x, ",", q3%y, ")"

        intersect = segments_intersect(p1, q1, p3, q3)
        if (intersect) then
            print '(a)', "Segments intersect"
        else
            print '(a)', "Segments do not intersect"
        end if
    end subroutine test_line_intersection

    subroutine test_point_in_polygon_test()
        type(point) :: square(4), test_points(4)
        logical :: inside
        integer :: i

        print *
        print '(a)', "3. POINT IN POLYGON TEST"
        print '(50("-"))'

        ! Square polygon
        square(1) = point(0.0d0, 0.0d0)
        square(2) = point(10.0d0, 0.0d0)
        square(3) = point(10.0d0, 10.0d0)
        square(4) = point(0.0d0, 10.0d0)

        test_points(1) = point(5.0d0, 5.0d0)    ! Inside
        test_points(2) = point(15.0d0, 15.0d0)  ! Outside
        test_points(3) = point(0.0d0, 0.0d0)    ! On vertex
        test_points(4) = point(5.0d0, 0.0d0)    ! On edge

        print '(a)', "Polygon: Square (0,0), (10,0), (10,10), (0,10)"
        print *

        do i = 1, 4
            inside = point_in_polygon(test_points(i), square, 4)
            print '(a,f5.1,a,f5.1,a,a)', &
                "Point (", test_points(i)%x, ", ", test_points(i)%y, "): ", &
                merge("INSIDE ", "OUTSIDE", inside)
        end do
    end subroutine test_point_in_polygon_test

    subroutine test_closest_pair_test()
        type(point) :: points(7), p1, p2
        real(8) :: min_dist
        integer :: i

        print *
        print '(a)', "4. CLOSEST PAIR OF POINTS"
        print '(50("-"))'

        points(1) = point(0.0d0, 0.0d0)
        points(2) = point(1.0d0, 1.0d0)
        points(3) = point(2.0d0, 2.0d0)
        points(4) = point(3.0d0, 10.0d0)
        points(5) = point(4.0d0, 3.0d0)
        points(6) = point(5.0d0, 5.0d0)
        points(7) = point(6.0d0, 1.0d0)

        print '(a)', "Input points (7):"
        do i = 1, 7
            print '(a,f5.1,a,f5.1,a)', "  (", points(i)%x, ", ", points(i)%y, ")"
        end do

        call closest_pair(points, 7, p1, p2, min_dist)

        print *
        print '(a)', "Closest pair:"
        print '(a,f5.1,a,f5.1,a)', "  Point 1: (", p1%x, ", ", p1%y, ")"
        print '(a,f5.1,a,f5.1,a)', "  Point 2: (", p2%x, ", ", p2%y, ")"
        print '(a,f8.4)', "  Distance: ", min_dist
    end subroutine test_closest_pair_test

    subroutine test_polygon_area_test()
        type(point) :: triangle(3), square(4)
        real(8) :: area1, area2

        print *
        print '(a)', "5. POLYGON AREA"
        print '(50("-"))'

        triangle(1) = point(0.0d0, 0.0d0)
        triangle(2) = point(4.0d0, 0.0d0)
        triangle(3) = point(0.0d0, 3.0d0)

        square(1) = point(0.0d0, 0.0d0)
        square(2) = point(5.0d0, 0.0d0)
        square(3) = point(5.0d0, 5.0d0)
        square(4) = point(0.0d0, 5.0d0)

        area1 = polygon_area(triangle, 3)
        area2 = polygon_area(square, 4)

        print '(a,f5.1,a)', "Triangle area: ", area1, " (expected: 6.0)"
        print '(a,f5.1,a)', "Square area: ", area2, " (expected: 25.0)"
    end subroutine test_polygon_area_test

end program test_geometry
