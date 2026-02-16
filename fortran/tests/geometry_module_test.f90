! Test suite for geometry algorithms module
program test_geometry_module
    use iso_fortran_env, only: int32, real64
    use geometry_module
    implicit none

    integer :: total_tests = 0, passed_tests = 0
    real(real64), parameter :: EPS = 1e-9

    print '(A)', "========================================"
    print '(A)', "    Geometry Module Test Suite"
    print '(A)', "========================================"

    call test_basic_operations()
    call test_polygon_operations()
    call test_intersection_algorithms()
    call test_convex_hull()
    call test_spatial_data_structures()

    print '(A)', ""
    print '(A)', "========================================"
    print '(A,I0,A,I0)', "Tests passed: ", passed_tests, "/", total_tests
    if (passed_tests == total_tests) then
        print '(A)', "STATUS: ALL TESTS PASSED ✓"
    else
        print '(A)', "STATUS: SOME TESTS FAILED ✗"
    end if
    print '(A)', "========================================"

contains

    subroutine test_basic_operations()
        type(point_2d_type) :: p1, p2
        type(point_3d_type) :: p3d1, p3d2
        real(real64) :: dist, cross, dot
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Basic Geometric Operations..."

        ! Test 2D distance
        p1 = point_2d_type(0.0_real64, 0.0_real64)
        p2 = point_2d_type(3.0_real64, 4.0_real64)
        dist = distance_2d(p1, p2)
        success = abs(dist - 5.0_real64) < EPS
        call report_test("2D distance calculation", success)

        ! Test 3D distance
        p3d1 = point_3d_type(0.0_real64, 0.0_real64, 0.0_real64)
        p3d2 = point_3d_type(2.0_real64, 2.0_real64, 1.0_real64)
        dist = distance_3d(p3d1, p3d2)
        success = abs(dist - 3.0_real64) < EPS
        call report_test("3D distance calculation", success)

        ! Test cross product
        p1 = point_2d_type(1.0_real64, 0.0_real64)
        p2 = point_2d_type(0.0_real64, 1.0_real64)
        cross = cross_product_2d(p1, p2)
        success = abs(cross - 1.0_real64) < EPS
        call report_test("2D cross product", success)

        ! Test dot product
        p1 = point_2d_type(3.0_real64, 4.0_real64)
        p2 = point_2d_type(2.0_real64, 1.0_real64)
        dot = dot_product_2d(p1, p2)
        success = abs(dot - 10.0_real64) < EPS
        call report_test("2D dot product", success)

    end subroutine test_basic_operations

    subroutine test_polygon_operations()
        type(polygon_type) :: poly
        type(point_2d_type) :: test_point
        real(real64) :: area, perimeter
        logical :: inside, success

        print '(A)', ""
        print '(A)', "Testing Polygon Operations..."

        ! Create a square polygon
        poly%num_vertices = 4
        allocate(poly%vertices(4))
        poly%vertices(1) = point_2d_type(0.0_real64, 0.0_real64)
        poly%vertices(2) = point_2d_type(4.0_real64, 0.0_real64)
        poly%vertices(3) = point_2d_type(4.0_real64, 3.0_real64)
        poly%vertices(4) = point_2d_type(0.0_real64, 3.0_real64)

        ! Test polygon area (should be 12 for 4x3 rectangle)
        area = polygon_area(poly)
        success = abs(area - 12.0_real64) < EPS
        call report_test("Polygon area calculation", success)

        ! Test polygon perimeter (should be 14 for 4x3 rectangle)
        perimeter = polygon_perimeter(poly)
        success = abs(perimeter - 14.0_real64) < EPS
        call report_test("Polygon perimeter calculation", success)

        ! Test point in polygon (inside)
        test_point = point_2d_type(2.0_real64, 1.5_real64)
        inside = point_in_polygon(test_point, poly)
        success = inside
        call report_test("Point in polygon (inside)", success)

        ! Test point in polygon (outside)
        test_point = point_2d_type(5.0_real64, 1.5_real64)
        inside = point_in_polygon(test_point, poly)
        success = .not. inside
        call report_test("Point in polygon (outside)", success)

        deallocate(poly%vertices)

    end subroutine test_polygon_operations

    subroutine test_intersection_algorithms()
        type(line_2d_type) :: line1, line2
        type(circle_type) :: circle1, circle2
        type(point_2d_type) :: intersection, intersections(2)
        logical :: intersects, success
        integer :: num_intersections

        print '(A)', ""
        print '(A)', "Testing Intersection Algorithms..."

        ! Test line intersection
        line1%start = point_2d_type(0.0_real64, 0.0_real64)
        line1%end = point_2d_type(4.0_real64, 4.0_real64)
        line2%start = point_2d_type(0.0_real64, 4.0_real64)
        line2%end = point_2d_type(4.0_real64, 0.0_real64)

        intersects = line_intersection(line1, line2, intersection)
        success = intersects .and. abs(intersection%x - 2.0_real64) < EPS &
                  .and. abs(intersection%y - 2.0_real64) < EPS
        call report_test("Line intersection", success)

        ! Test segment intersection
        intersects = segment_intersection(line1, line2, intersection)
        success = intersects
        call report_test("Segment intersection", success)

        ! Test circle intersection
        circle1%center = point_2d_type(0.0_real64, 0.0_real64)
        circle1%radius = 3.0_real64
        circle2%center = point_2d_type(4.0_real64, 0.0_real64)
        circle2%radius = 2.0_real64

        intersects = circle_intersection(circle1, circle2, intersections, num_intersections)
        success = intersects .and. num_intersections == 2
        call report_test("Circle intersection", success)

    end subroutine test_intersection_algorithms

    subroutine test_convex_hull()
        type(point_2d_type), allocatable :: points(:), hull(:)
        integer :: num_hull_points
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Convex Hull Algorithms..."

        ! Create a set of points
        allocate(points(8))
        points(1) = point_2d_type(0.0_real64, 0.0_real64)
        points(2) = point_2d_type(1.0_real64, 1.0_real64)
        points(3) = point_2d_type(2.0_real64, 2.0_real64)
        points(4) = point_2d_type(0.0_real64, 2.0_real64)
        points(5) = point_2d_type(2.0_real64, 0.0_real64)
        points(6) = point_2d_type(1.0_real64, 0.5_real64)
        points(7) = point_2d_type(0.5_real64, 1.0_real64)
        points(8) = point_2d_type(1.5_real64, 1.5_real64)

        ! Test Graham scan
        allocate(hull(8))
        call convex_hull_graham_scan(points, hull, num_hull_points)
        success = num_hull_points == 4  ! Should form a square
        call report_test("Graham scan convex hull", success)

        ! Test Jarvis march
        call convex_hull_jarvis_march(points, hull, num_hull_points)
        success = num_hull_points == 4  ! Should form a square
        call report_test("Jarvis march convex hull", success)

        ! Test closest pair of points
        call test_closest_pair()

        deallocate(points, hull)

    end subroutine test_convex_hull

    subroutine test_closest_pair()
        type(point_2d_type), allocatable :: points(:)
        real(real64) :: min_dist
        logical :: success

        allocate(points(5))
        points(1) = point_2d_type(0.0_real64, 0.0_real64)
        points(2) = point_2d_type(1.0_real64, 0.0_real64)
        points(3) = point_2d_type(5.0_real64, 0.0_real64)
        points(4) = point_2d_type(3.0_real64, 3.0_real64)
        points(5) = point_2d_type(3.0_real64, 4.0_real64)

        min_dist = closest_pair_of_points(points)
        success = abs(min_dist - 1.0_real64) < EPS
        call report_test("Closest pair of points", success)

        deallocate(points)

    end subroutine test_closest_pair

    subroutine test_spatial_data_structures()
        type(kd_tree_type) :: kdtree
        type(quad_tree_type) :: qtree
        type(point_2d_type), allocatable :: points(:), range_results(:)
        type(point_2d_type) :: query_point, nearest
        real(real64) :: x_min, x_max, y_min, y_max
        integer :: num_results
        logical :: success

        print '(A)', ""
        print '(A)', "Testing Spatial Data Structures..."

        ! Test KD-Tree
        allocate(points(5))
        points(1) = point_2d_type(2.0_real64, 3.0_real64)
        points(2) = point_2d_type(5.0_real64, 4.0_real64)
        points(3) = point_2d_type(9.0_real64, 6.0_real64)
        points(4) = point_2d_type(4.0_real64, 7.0_real64)
        points(5) = point_2d_type(8.0_real64, 1.0_real64)

        call kd_tree_build(kdtree, points)
        query_point = point_2d_type(5.5_real64, 4.5_real64)
        nearest = kd_tree_nearest_neighbor(kdtree, query_point)
        success = abs(nearest%x - 5.0_real64) < EPS .and. abs(nearest%y - 4.0_real64) < EPS
        call report_test("KD-Tree nearest neighbor", success)

        ! Test QuadTree
        call quad_tree_insert(qtree, point_2d_type(1.0_real64, 1.0_real64))
        call quad_tree_insert(qtree, point_2d_type(2.0_real64, 2.0_real64))
        call quad_tree_insert(qtree, point_2d_type(3.0_real64, 3.0_real64))
        call quad_tree_insert(qtree, point_2d_type(5.0_real64, 5.0_real64))

        x_min = 0.0_real64
        x_max = 3.5_real64
        y_min = 0.0_real64
        y_max = 3.5_real64
        allocate(range_results(10))
        call quad_tree_query_range(qtree, x_min, x_max, y_min, y_max, range_results, num_results)
        success = num_results == 3  ! Points (1,1), (2,2), (3,3) should be in range
        call report_test("QuadTree range query", success)

        deallocate(points, range_results)

    end subroutine test_spatial_data_structures

    subroutine report_test(test_name, success)
        character(len=*), intent(in) :: test_name
        logical, intent(in) :: success

        total_tests = total_tests + 1
        if (success) then
            passed_tests = passed_tests + 1
            print '(A,A,A)', "  ✓ ", test_name, " ... PASSED"
        else
            print '(A,A,A)', "  ✗ ", test_name, " ... FAILED"
        end if
    end subroutine report_test

end program test_geometry_module