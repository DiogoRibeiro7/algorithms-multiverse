! Computational Geometry Module
! Collection of geometric algorithms and data structures

module geometry_module
    use iso_fortran_env, only: int32, int64, real32, real64
    implicit none
    private

    ! Public types and interfaces
    public :: point_2d, point_3d, line_2d, line_3d
    public :: segment_2d, segment_3d, circle, sphere
    public :: triangle_2d, triangle_3d, polygon_2d
    public :: rectangle, box_3d, ray_2d, ray_3d

    ! Public functions
    public :: distance_2d, distance_3d, manhattan_distance
    public :: dot_product_2d, dot_product_3d
    public :: cross_product_2d, cross_product_3d
    public :: angle_between_vectors, angle_between_lines
    public :: point_on_line, point_on_segment
    public :: line_intersection, segment_intersection
    public :: point_in_polygon, point_in_circle
    public :: convex_hull_graham, convex_hull_jarvis
    public :: closest_pair_of_points, farthest_pair_of_points
    public :: polygon_area, polygon_perimeter
    public :: triangle_area, triangle_circumcenter
    public :: circle_from_three_points, minimum_enclosing_circle
    public :: line_sweep_intersections, bentley_ottmann
    public :: voronoi_diagram, delaunay_triangulation
    public :: rotate_point_2d, rotate_point_3d
    public :: translate_point, scale_point
    public :: reflection_2d, projection_on_line
    public :: polygon_centroid, polygon_convex_check
    public :: polygon_triangulation, ear_clipping
    public :: ray_casting, ray_tracing_intersection
    public :: bounding_box_2d, bounding_box_3d
    public :: quadtree_type, octree_type
    public :: kd_tree_type, range_tree_type

    ! Constants
    real(real64), parameter :: PI = 3.14159265358979323846_real64
    real(real64), parameter :: EPS = 1.0e-12_real64

    ! 2D Point type
    type :: point_2d
        real(real64) :: x, y
    contains
        procedure :: distance => point_2d_distance
        procedure :: equals => point_2d_equals
    end type point_2d

    ! 3D Point type
    type :: point_3d
        real(real64) :: x, y, z
    contains
        procedure :: distance => point_3d_distance
        procedure :: equals => point_3d_equals
    end type point_3d

    ! 2D Line type (ax + by + c = 0)
    type :: line_2d
        real(real64) :: a, b, c
    contains
        procedure :: distance_to_point => line_2d_distance_to_point
        procedure :: parallel => line_2d_parallel
        procedure :: perpendicular => line_2d_perpendicular
    end type line_2d

    ! 3D Line type (parametric form)
    type :: line_3d
        type(point_3d) :: point
        type(point_3d) :: direction
    contains
        procedure :: distance_to_point => line_3d_distance_to_point
    end type line_3d

    ! 2D Line segment
    type :: segment_2d
        type(point_2d) :: p1, p2
    contains
        procedure :: length => segment_2d_length
        procedure :: midpoint => segment_2d_midpoint
    end type segment_2d

    ! 3D Line segment
    type :: segment_3d
        type(point_3d) :: p1, p2
    contains
        procedure :: length => segment_3d_length
        procedure :: midpoint => segment_3d_midpoint
    end type segment_3d

    ! Circle type
    type :: circle
        type(point_2d) :: center
        real(real64) :: radius
    contains
        procedure :: area => circle_area
        procedure :: circumference => circle_circumference
        procedure :: contains_point => circle_contains_point
    end type circle

    ! Sphere type
    type :: sphere
        type(point_3d) :: center
        real(real64) :: radius
    contains
        procedure :: volume => sphere_volume
        procedure :: surface_area => sphere_surface_area
        procedure :: contains_point => sphere_contains_point
    end type sphere

    ! 2D Triangle
    type :: triangle_2d
        type(point_2d) :: p1, p2, p3
    contains
        procedure :: area => triangle_2d_area
        procedure :: perimeter => triangle_2d_perimeter
        procedure :: centroid => triangle_2d_centroid
    end type triangle_2d

    ! 3D Triangle
    type :: triangle_3d
        type(point_3d) :: p1, p2, p3
    contains
        procedure :: area => triangle_3d_area
        procedure :: normal => triangle_3d_normal
    end type triangle_3d

    ! 2D Polygon
    type :: polygon_2d
        type(point_2d), dimension(:), allocatable :: vertices
        integer(int32) :: n_vertices
    contains
        procedure :: init => polygon_2d_init
        procedure :: area => polygon_2d_area
        procedure :: perimeter => polygon_2d_perimeter
        procedure :: is_convex => polygon_2d_is_convex
    end type polygon_2d

    ! Rectangle
    type :: rectangle
        type(point_2d) :: min_point, max_point
    contains
        procedure :: area => rectangle_area
        procedure :: perimeter => rectangle_perimeter
        procedure :: contains_point => rectangle_contains_point
    end type rectangle

    ! 3D Box
    type :: box_3d
        type(point_3d) :: min_point, max_point
    contains
        procedure :: volume => box_3d_volume
        procedure :: surface_area => box_3d_surface_area
        procedure :: contains_point => box_3d_contains_point
    end type box_3d

    ! 2D Ray
    type :: ray_2d
        type(point_2d) :: origin
        type(point_2d) :: direction
    end type ray_2d

    ! 3D Ray
    type :: ray_3d
        type(point_3d) :: origin
        type(point_3d) :: direction
    end type ray_3d

    ! Quadtree node
    type :: quadtree_node
        type(rectangle) :: boundary
        type(point_2d), dimension(:), allocatable :: points
        integer(int32) :: n_points
        logical :: is_leaf
        type(quadtree_node), pointer :: ne, nw, se, sw
    end type quadtree_node

    ! Quadtree
    type :: quadtree_type
        type(quadtree_node), pointer :: root
        integer(int32) :: capacity
    contains
        procedure :: init => quadtree_init
        procedure :: insert => quadtree_insert
        procedure :: query_range => quadtree_query_range
    end type quadtree_type

    ! Octree node
    type :: octree_node
        type(box_3d) :: boundary
        type(point_3d), dimension(:), allocatable :: points
        integer(int32) :: n_points
        logical :: is_leaf
        type(octree_node), pointer :: children(8)
    end type octree_node

    ! Octree
    type :: octree_type
        type(octree_node), pointer :: root
        integer(int32) :: capacity
    contains
        procedure :: init => octree_init
        procedure :: insert => octree_insert
        procedure :: query_range => octree_query_range
    end type octree_type

    ! KD-Tree node
    type :: kd_tree_node
        type(point_2d) :: point
        integer(int32) :: axis
        type(kd_tree_node), pointer :: left, right
    end type kd_tree_node

    ! KD-Tree
    type :: kd_tree_type
        type(kd_tree_node), pointer :: root
        integer(int32) :: dimensions
    contains
        procedure :: init => kd_tree_init
        procedure :: insert => kd_tree_insert
        procedure :: nearest_neighbor => kd_tree_nearest_neighbor
    end type kd_tree_type

    ! Range tree node
    type :: range_tree_node
        real(real64) :: value
        type(range_tree_node), pointer :: left, right
        type(range_tree_node), pointer :: y_tree
    end type range_tree_node

    ! Range tree
    type :: range_tree_type
        type(range_tree_node), pointer :: root
    contains
        procedure :: init => range_tree_init
        procedure :: query_2d => range_tree_query_2d
    end type range_tree_type

contains

    !===============================================
    ! Point operations
    !===============================================

    function point_2d_distance(this, other) result(dist)
        implicit none
        class(point_2d), intent(in) :: this
        type(point_2d), intent(in) :: other
        real(real64) :: dist

        dist = sqrt((this%x - other%x)**2 + (this%y - other%y)**2)

    end function point_2d_distance

    function point_2d_equals(this, other) result(equal)
        implicit none
        class(point_2d), intent(in) :: this
        type(point_2d), intent(in) :: other
        logical :: equal

        equal = abs(this%x - other%x) < EPS .and. abs(this%y - other%y) < EPS

    end function point_2d_equals

    function point_3d_distance(this, other) result(dist)
        implicit none
        class(point_3d), intent(in) :: this
        type(point_3d), intent(in) :: other
        real(real64) :: dist

        dist = sqrt((this%x - other%x)**2 + (this%y - other%y)**2 + (this%z - other%z)**2)

    end function point_3d_distance

    function point_3d_equals(this, other) result(equal)
        implicit none
        class(point_3d), intent(in) :: this
        type(point_3d), intent(in) :: other
        logical :: equal

        equal = abs(this%x - other%x) < EPS .and. &
                abs(this%y - other%y) < EPS .and. &
                abs(this%z - other%z) < EPS

    end function point_3d_equals

    !===============================================
    ! Distance functions
    !===============================================

    function distance_2d(p1, p2) result(dist)
        implicit none
        type(point_2d), intent(in) :: p1, p2
        real(real64) :: dist

        dist = p1%distance(p2)

    end function distance_2d

    function distance_3d(p1, p2) result(dist)
        implicit none
        type(point_3d), intent(in) :: p1, p2
        real(real64) :: dist

        dist = p1%distance(p2)

    end function distance_3d

    function manhattan_distance(p1, p2) result(dist)
        implicit none
        type(point_2d), intent(in) :: p1, p2
        real(real64) :: dist

        dist = abs(p1%x - p2%x) + abs(p1%y - p2%y)

    end function manhattan_distance

    !===============================================
    ! Vector operations
    !===============================================

    function dot_product_2d(v1, v2) result(dot)
        implicit none
        type(point_2d), intent(in) :: v1, v2
        real(real64) :: dot

        dot = v1%x * v2%x + v1%y * v2%y

    end function dot_product_2d

    function dot_product_3d(v1, v2) result(dot)
        implicit none
        type(point_3d), intent(in) :: v1, v2
        real(real64) :: dot

        dot = v1%x * v2%x + v1%y * v2%y + v1%z * v2%z

    end function dot_product_3d

    function cross_product_2d(v1, v2) result(cross)
        implicit none
        type(point_2d), intent(in) :: v1, v2
        real(real64) :: cross

        cross = v1%x * v2%y - v1%y * v2%x

    end function cross_product_2d

    function cross_product_3d(v1, v2) result(cross)
        implicit none
        type(point_3d), intent(in) :: v1, v2
        type(point_3d) :: cross

        cross%x = v1%y * v2%z - v1%z * v2%y
        cross%y = v1%z * v2%x - v1%x * v2%z
        cross%z = v1%x * v2%y - v1%y * v2%x

    end function cross_product_3d

    function angle_between_vectors(v1, v2) result(angle)
        implicit none
        type(point_2d), intent(in) :: v1, v2
        real(real64) :: angle
        real(real64) :: dot, cross

        dot = dot_product_2d(v1, v2)
        cross = cross_product_2d(v1, v2)
        angle = atan2(cross, dot)

    end function angle_between_vectors

    !===============================================
    ! Line operations
    !===============================================

    function line_2d_distance_to_point(this, p) result(dist)
        implicit none
        class(line_2d), intent(in) :: this
        type(point_2d), intent(in) :: p
        real(real64) :: dist

        dist = abs(this%a * p%x + this%b * p%y + this%c) / &
               sqrt(this%a**2 + this%b**2)

    end function line_2d_distance_to_point

    function line_2d_parallel(this, other) result(parallel)
        implicit none
        class(line_2d), intent(in) :: this
        type(line_2d), intent(in) :: other
        logical :: parallel

        parallel = abs(this%a * other%b - this%b * other%a) < EPS

    end function line_2d_parallel

    function line_2d_perpendicular(this, other) result(perpendicular)
        implicit none
        class(line_2d), intent(in) :: this
        type(line_2d), intent(in) :: other
        logical :: perpendicular

        perpendicular = abs(this%a * other%a + this%b * other%b) < EPS

    end function line_2d_perpendicular

    function line_3d_distance_to_point(this, p) result(dist)
        implicit none
        class(line_3d), intent(in) :: this
        type(point_3d), intent(in) :: p
        real(real64) :: dist
        type(point_3d) :: diff, cross

        diff%x = p%x - this%point%x
        diff%y = p%y - this%point%y
        diff%z = p%z - this%point%z

        cross = cross_product_3d(diff, this%direction)
        dist = sqrt(dot_product_3d(cross, cross)) / &
               sqrt(dot_product_3d(this%direction, this%direction))

    end function line_3d_distance_to_point

    !===============================================
    ! Segment operations
    !===============================================

    function segment_2d_length(this) result(length)
        implicit none
        class(segment_2d), intent(in) :: this
        real(real64) :: length

        length = this%p1%distance(this%p2)

    end function segment_2d_length

    function segment_2d_midpoint(this) result(mid)
        implicit none
        class(segment_2d), intent(in) :: this
        type(point_2d) :: mid

        mid%x = (this%p1%x + this%p2%x) / 2.0_real64
        mid%y = (this%p1%y + this%p2%y) / 2.0_real64

    end function segment_2d_midpoint

    function segment_3d_length(this) result(length)
        implicit none
        class(segment_3d), intent(in) :: this
        real(real64) :: length

        length = this%p1%distance(this%p2)

    end function segment_3d_length

    function segment_3d_midpoint(this) result(mid)
        implicit none
        class(segment_3d), intent(in) :: this
        type(point_3d) :: mid

        mid%x = (this%p1%x + this%p2%x) / 2.0_real64
        mid%y = (this%p1%y + this%p2%y) / 2.0_real64
        mid%z = (this%p1%z + this%p2%z) / 2.0_real64

    end function segment_3d_midpoint

    !===============================================
    ! Circle operations
    !===============================================

    function circle_area(this) result(area)
        implicit none
        class(circle), intent(in) :: this
        real(real64) :: area

        area = PI * this%radius**2

    end function circle_area

    function circle_circumference(this) result(circ)
        implicit none
        class(circle), intent(in) :: this
        real(real64) :: circ

        circ = 2.0_real64 * PI * this%radius

    end function circle_circumference

    function circle_contains_point(this, p) result(contains)
        implicit none
        class(circle), intent(in) :: this
        type(point_2d), intent(in) :: p
        logical :: contains

        contains = this%center%distance(p) <= this%radius + EPS

    end function circle_contains_point

    !===============================================
    ! Sphere operations
    !===============================================

    function sphere_volume(this) result(volume)
        implicit none
        class(sphere), intent(in) :: this
        real(real64) :: volume

        volume = (4.0_real64 / 3.0_real64) * PI * this%radius**3

    end function sphere_volume

    function sphere_surface_area(this) result(area)
        implicit none
        class(sphere), intent(in) :: this
        real(real64) :: area

        area = 4.0_real64 * PI * this%radius**2

    end function sphere_surface_area

    function sphere_contains_point(this, p) result(contains)
        implicit none
        class(sphere), intent(in) :: this
        type(point_3d), intent(in) :: p
        logical :: contains

        contains = this%center%distance(p) <= this%radius + EPS

    end function sphere_contains_point

    !===============================================
    ! Triangle operations
    !===============================================

    function triangle_2d_area(this) result(area)
        implicit none
        class(triangle_2d), intent(in) :: this
        real(real64) :: area

        area = abs((this%p2%x - this%p1%x) * (this%p3%y - this%p1%y) - &
                  (this%p3%x - this%p1%x) * (this%p2%y - this%p1%y)) / 2.0_real64

    end function triangle_2d_area

    function triangle_2d_perimeter(this) result(perim)
        implicit none
        class(triangle_2d), intent(in) :: this
        real(real64) :: perim

        perim = this%p1%distance(this%p2) + &
                this%p2%distance(this%p3) + &
                this%p3%distance(this%p1)

    end function triangle_2d_perimeter

    function triangle_2d_centroid(this) result(centroid)
        implicit none
        class(triangle_2d), intent(in) :: this
        type(point_2d) :: centroid

        centroid%x = (this%p1%x + this%p2%x + this%p3%x) / 3.0_real64
        centroid%y = (this%p1%y + this%p2%y + this%p3%y) / 3.0_real64

    end function triangle_2d_centroid

    function triangle_3d_area(this) result(area)
        implicit none
        class(triangle_3d), intent(in) :: this
        real(real64) :: area
        type(point_3d) :: v1, v2, cross

        v1%x = this%p2%x - this%p1%x
        v1%y = this%p2%y - this%p1%y
        v1%z = this%p2%z - this%p1%z

        v2%x = this%p3%x - this%p1%x
        v2%y = this%p3%y - this%p1%y
        v2%z = this%p3%z - this%p1%z

        cross = cross_product_3d(v1, v2)
        area = sqrt(dot_product_3d(cross, cross)) / 2.0_real64

    end function triangle_3d_area

    function triangle_3d_normal(this) result(normal)
        implicit none
        class(triangle_3d), intent(in) :: this
        type(point_3d) :: normal
        type(point_3d) :: v1, v2
        real(real64) :: length

        v1%x = this%p2%x - this%p1%x
        v1%y = this%p2%y - this%p1%y
        v1%z = this%p2%z - this%p1%z

        v2%x = this%p3%x - this%p1%x
        v2%y = this%p3%y - this%p1%y
        v2%z = this%p3%z - this%p1%z

        normal = cross_product_3d(v1, v2)
        length = sqrt(dot_product_3d(normal, normal))

        if (length > EPS) then
            normal%x = normal%x / length
            normal%y = normal%y / length
            normal%z = normal%z / length
        end if

    end function triangle_3d_normal

    !===============================================
    ! Polygon operations
    !===============================================

    subroutine polygon_2d_init(this, vertices)
        implicit none
        class(polygon_2d), intent(inout) :: this
        type(point_2d), dimension(:), intent(in) :: vertices

        this%n_vertices = size(vertices)
        allocate(this%vertices(this%n_vertices))
        this%vertices = vertices

    end subroutine polygon_2d_init

    function polygon_2d_area(this) result(area)
        implicit none
        class(polygon_2d), intent(in) :: this
        real(real64) :: area
        integer(int32) :: i

        area = 0.0_real64
        do i = 1, this%n_vertices
            area = area + this%vertices(i)%x * &
                   this%vertices(mod(i, this%n_vertices) + 1)%y - &
                   this%vertices(mod(i, this%n_vertices) + 1)%x * &
                   this%vertices(i)%y
        end do
        area = abs(area) / 2.0_real64

    end function polygon_2d_area

    function polygon_2d_perimeter(this) result(perim)
        implicit none
        class(polygon_2d), intent(in) :: this
        real(real64) :: perim
        integer(int32) :: i

        perim = 0.0_real64
        do i = 1, this%n_vertices
            perim = perim + this%vertices(i)%distance(&
                    this%vertices(mod(i, this%n_vertices) + 1))
        end do

    end function polygon_2d_perimeter

    function polygon_2d_is_convex(this) result(convex)
        implicit none
        class(polygon_2d), intent(in) :: this
        logical :: convex
        real(real64) :: sign, cross
        integer(int32) :: i
        type(point_2d) :: v1, v2

        if (this%n_vertices < 3) then
            convex = .true.
            return
        end if

        sign = 0.0_real64
        convex = .true.

        do i = 1, this%n_vertices
            v1%x = this%vertices(mod(i, this%n_vertices) + 1)%x - this%vertices(i)%x
            v1%y = this%vertices(mod(i, this%n_vertices) + 1)%y - this%vertices(i)%y
            v2%x = this%vertices(mod(i+1, this%n_vertices) + 1)%x - this%vertices(mod(i, this%n_vertices) + 1)%x
            v2%y = this%vertices(mod(i+1, this%n_vertices) + 1)%y - this%vertices(mod(i, this%n_vertices) + 1)%y

            cross = cross_product_2d(v1, v2)

            if (abs(cross) > EPS) then
                if (sign == 0.0_real64) then
                    sign = cross
                else if (sign * cross < 0.0_real64) then
                    convex = .false.
                    return
                end if
            end if
        end do

    end function polygon_2d_is_convex

    !===============================================
    ! Rectangle operations
    !===============================================

    function rectangle_area(this) result(area)
        implicit none
        class(rectangle), intent(in) :: this
        real(real64) :: area

        area = (this%max_point%x - this%min_point%x) * &
               (this%max_point%y - this%min_point%y)

    end function rectangle_area

    function rectangle_perimeter(this) result(perim)
        implicit none
        class(rectangle), intent(in) :: this
        real(real64) :: perim

        perim = 2.0_real64 * ((this%max_point%x - this%min_point%x) + &
                              (this%max_point%y - this%min_point%y))

    end function rectangle_perimeter

    function rectangle_contains_point(this, p) result(contains)
        implicit none
        class(rectangle), intent(in) :: this
        type(point_2d), intent(in) :: p
        logical :: contains

        contains = p%x >= this%min_point%x - EPS .and. &
                  p%x <= this%max_point%x + EPS .and. &
                  p%y >= this%min_point%y - EPS .and. &
                  p%y <= this%max_point%y + EPS

    end function rectangle_contains_point

    !===============================================
    ! 3D Box operations
    !===============================================

    function box_3d_volume(this) result(volume)
        implicit none
        class(box_3d), intent(in) :: this
        real(real64) :: volume

        volume = (this%max_point%x - this%min_point%x) * &
                (this%max_point%y - this%min_point%y) * &
                (this%max_point%z - this%min_point%z)

    end function box_3d_volume

    function box_3d_surface_area(this) result(area)
        implicit none
        class(box_3d), intent(in) :: this
        real(real64) :: area
        real(real64) :: dx, dy, dz

        dx = this%max_point%x - this%min_point%x
        dy = this%max_point%y - this%min_point%y
        dz = this%max_point%z - this%min_point%z

        area = 2.0_real64 * (dx*dy + dx*dz + dy*dz)

    end function box_3d_surface_area

    function box_3d_contains_point(this, p) result(contains)
        implicit none
        class(box_3d), intent(in) :: this
        type(point_3d), intent(in) :: p
        logical :: contains

        contains = p%x >= this%min_point%x - EPS .and. &
                  p%x <= this%max_point%x + EPS .and. &
                  p%y >= this%min_point%y - EPS .and. &
                  p%y <= this%max_point%y + EPS .and. &
                  p%z >= this%min_point%z - EPS .and. &
                  p%z <= this%max_point%z + EPS

    end function box_3d_contains_point

    !===============================================
    ! Line intersection
    !===============================================

    function line_intersection(l1, l2) result(point)
        implicit none
        type(line_2d), intent(in) :: l1, l2
        type(point_2d) :: point
        real(real64) :: det

        det = l1%a * l2%b - l2%a * l1%b

        if (abs(det) < EPS) then
            ! Lines are parallel
            point%x = huge(1.0_real64)
            point%y = huge(1.0_real64)
        else
            point%x = (l2%b * (-l1%c) - l1%b * (-l2%c)) / det
            point%y = (l1%a * (-l2%c) - l2%a * (-l1%c)) / det
        end if

    end function line_intersection

    function segment_intersection(s1, s2) result(intersects)
        implicit none
        type(segment_2d), intent(in) :: s1, s2
        logical :: intersects
        real(real64) :: d1, d2, d3, d4

        d1 = direction(s1%p1, s1%p2, s2%p1)
        d2 = direction(s1%p1, s1%p2, s2%p2)
        d3 = direction(s2%p1, s2%p2, s1%p1)
        d4 = direction(s2%p1, s2%p2, s1%p2)

        if (((d1 > 0 .and. d2 < 0) .or. (d1 < 0 .and. d2 > 0)) .and. &
            ((d3 > 0 .and. d4 < 0) .or. (d3 < 0 .and. d4 > 0))) then
            intersects = .true.
        else if (abs(d1) < EPS .and. on_segment(s1%p1, s2%p1, s1%p2)) then
            intersects = .true.
        else if (abs(d2) < EPS .and. on_segment(s1%p1, s2%p2, s1%p2)) then
            intersects = .true.
        else if (abs(d3) < EPS .and. on_segment(s2%p1, s1%p1, s2%p2)) then
            intersects = .true.
        else if (abs(d4) < EPS .and. on_segment(s2%p1, s1%p2, s2%p2)) then
            intersects = .true.
        else
            intersects = .false.
        end if

    contains

        function direction(pi, pj, pk) result(d)
            implicit none
            type(point_2d), intent(in) :: pi, pj, pk
            real(real64) :: d

            d = (pk%x - pi%x) * (pj%y - pi%y) - (pj%x - pi%x) * (pk%y - pi%y)

        end function direction

        function on_segment(pi, pj, pk) result(on)
            implicit none
            type(point_2d), intent(in) :: pi, pj, pk
            logical :: on

            on = min(pi%x, pk%x) <= pj%x + EPS .and. &
                 pj%x <= max(pi%x, pk%x) + EPS .and. &
                 min(pi%y, pk%y) <= pj%y + EPS .and. &
                 pj%y <= max(pi%y, pk%y) + EPS

        end function on_segment

    end function segment_intersection

    !===============================================
    ! Point in polygon
    !===============================================

    function point_in_polygon(p, polygon) result(inside)
        implicit none
        type(point_2d), intent(in) :: p
        type(polygon_2d), intent(in) :: polygon
        logical :: inside
        integer(int32) :: i, j, n
        real(real64) :: xi, yi, xj, yj

        n = polygon%n_vertices
        inside = .false.
        j = n

        do i = 1, n
            xi = polygon%vertices(i)%x
            yi = polygon%vertices(i)%y
            xj = polygon%vertices(j)%x
            yj = polygon%vertices(j)%y

            if (((yi > p%y) .neqv. (yj > p%y)) .and. &
                (p%x < (xj - xi) * (p%y - yi) / (yj - yi) + xi)) then
                inside = .not. inside
            end if

            j = i
        end do

    end function point_in_polygon

    function point_in_circle(p, c) result(inside)
        implicit none
        type(point_2d), intent(in) :: p
        type(circle), intent(in) :: c
        logical :: inside

        inside = c%contains_point(p)

    end function point_in_circle

    !===============================================
    ! Convex Hull - Graham Scan
    !===============================================

    function convex_hull_graham(points) result(hull)
        implicit none
        type(point_2d), dimension(:), intent(in) :: points
        type(polygon_2d) :: hull
        type(point_2d), dimension(:), allocatable :: sorted_points, stack
        integer(int32) :: n, i, top
        type(point_2d) :: pivot

        n = size(points)
        if (n < 3) then
            call hull%init(points)
            return
        end if

        allocate(sorted_points(n))
        allocate(stack(n))

        ! Find bottommost point (or leftmost if tie)
        pivot = points(1)
        do i = 2, n
            if (points(i)%y < pivot%y .or. &
                (abs(points(i)%y - pivot%y) < EPS .and. points(i)%x < pivot%x)) then
                pivot = points(i)
            end if
        end do

        ! Sort points by polar angle with respect to pivot
        sorted_points = points
        call sort_by_polar_angle(sorted_points, pivot)

        ! Graham scan
        top = 0
        do i = 1, n
            do while (top > 1 .and. ccw(stack(top-1), stack(top), sorted_points(i)) <= 0.0_real64)
                top = top - 1
            end do
            top = top + 1
            stack(top) = sorted_points(i)
        end do

        call hull%init(stack(1:top))

    contains

        function ccw(p1, p2, p3) result(val)
            implicit none
            type(point_2d), intent(in) :: p1, p2, p3
            real(real64) :: val

            val = (p2%x - p1%x) * (p3%y - p1%y) - (p2%y - p1%y) * (p3%x - p1%x)

        end function ccw

        subroutine sort_by_polar_angle(pts, pivot)
            implicit none
            type(point_2d), dimension(:), intent(inout) :: pts
            type(point_2d), intent(in) :: pivot
            integer(int32) :: i, j, n
            type(point_2d) :: temp

            n = size(pts)

            ! Simple bubble sort by polar angle
            do i = 1, n-1
                do j = 1, n-i
                    if (compare_polar_angle(pts(j), pts(j+1), pivot) > 0) then
                        temp = pts(j)
                        pts(j) = pts(j+1)
                        pts(j+1) = temp
                    end if
                end do
            end do

        end subroutine sort_by_polar_angle

        function compare_polar_angle(p1, p2, pivot) result(cmp)
            implicit none
            type(point_2d), intent(in) :: p1, p2, pivot
            integer(int32) :: cmp
            real(real64) :: angle1, angle2

            angle1 = atan2(p1%y - pivot%y, p1%x - pivot%x)
            angle2 = atan2(p2%y - pivot%y, p2%x - pivot%x)

            if (angle1 < angle2) then
                cmp = -1
            else if (angle1 > angle2) then
                cmp = 1
            else
                ! Same angle, sort by distance
                if (distance_2d(pivot, p1) < distance_2d(pivot, p2)) then
                    cmp = -1
                else
                    cmp = 1
                end if
            end if

        end function compare_polar_angle

    end function convex_hull_graham

    !===============================================
    ! Convex Hull - Jarvis March
    !===============================================

    function convex_hull_jarvis(points) result(hull)
        implicit none
        type(point_2d), dimension(:), intent(in) :: points
        type(polygon_2d) :: hull
        type(point_2d), dimension(:), allocatable :: hull_points
        integer(int32) :: n, i, p, q, count
        real(real64) :: cross

        n = size(points)
        if (n < 3) then
            call hull%init(points)
            return
        end if

        allocate(hull_points(n))

        ! Find leftmost point
        p = 1
        do i = 2, n
            if (points(i)%x < points(p)%x) then
                p = i
            end if
        end do

        count = 0
        do
            count = count + 1
            hull_points(count) = points(p)
            q = mod(p, n) + 1

            do i = 1, n
                cross = (points(i)%y - points(p)%y) * (points(q)%x - points(i)%x) - &
                       (points(i)%x - points(p)%x) * (points(q)%y - points(i)%y)
                if (cross > 0.0_real64) then
                    q = i
                end if
            end do

            p = q
            if (p == 1) exit
        end do

        call hull%init(hull_points(1:count))

    end function convex_hull_jarvis

    !===============================================
    ! Closest pair of points
    !===============================================

    function closest_pair_of_points(points) result(min_dist)
        implicit none
        type(point_2d), dimension(:), intent(in) :: points
        real(real64) :: min_dist
        integer(int32) :: n, i, j

        n = size(points)
        min_dist = huge(1.0_real64)

        ! Brute force for small inputs
        if (n <= 3) then
            do i = 1, n-1
                do j = i+1, n
                    min_dist = min(min_dist, distance_2d(points(i), points(j)))
                end do
            end do
        else
            ! Divide and conquer for larger inputs
            min_dist = closest_pair_recursive(points, 1, n)
        end if

    contains

        recursive function closest_pair_recursive(pts, left, right) result(min_d)
            implicit none
            type(point_2d), dimension(:), intent(in) :: pts
            integer(int32), intent(in) :: left, right
            real(real64) :: min_d
            integer(int32) :: mid, i, j
            real(real64) :: d_left, d_right, mid_x
            type(point_2d), dimension(:), allocatable :: strip

            if (right - left <= 3) then
                min_d = huge(1.0_real64)
                do i = left, right-1
                    do j = i+1, right
                        min_d = min(min_d, distance_2d(pts(i), pts(j)))
                    end do
                end do
                return
            end if

            mid = (left + right) / 2
            mid_x = pts(mid)%x

            d_left = closest_pair_recursive(pts, left, mid)
            d_right = closest_pair_recursive(pts, mid+1, right)

            min_d = min(d_left, d_right)

            ! Check strip
            allocate(strip(right-left+1))
            j = 0
            do i = left, right
                if (abs(pts(i)%x - mid_x) < min_d) then
                    j = j + 1
                    strip(j) = pts(i)
                end if
            end do

            min_d = min(min_d, closest_in_strip(strip(1:j), min_d))

        end function closest_pair_recursive

        function closest_in_strip(strip, d) result(min_d)
            implicit none
            type(point_2d), dimension(:), intent(in) :: strip
            real(real64), intent(in) :: d
            real(real64) :: min_d
            integer(int32) :: i, j, n

            n = size(strip)
            min_d = d

            do i = 1, n
                j = i + 1
                do while (j <= n .and. (strip(j)%y - strip(i)%y) < min_d)
                    min_d = min(min_d, distance_2d(strip(i), strip(j)))
                    j = j + 1
                end do
            end do

        end function closest_in_strip

    end function closest_pair_of_points

    !===============================================
    ! Farthest pair of points
    !===============================================

    function farthest_pair_of_points(points) result(max_dist)
        implicit none
        type(point_2d), dimension(:), intent(in) :: points
        real(real64) :: max_dist
        type(polygon_2d) :: hull
        integer(int32) :: i, j

        ! Farthest pair must be on convex hull
        hull = convex_hull_graham(points)
        max_dist = 0.0_real64

        do i = 1, hull%n_vertices-1
            do j = i+1, hull%n_vertices
                max_dist = max(max_dist, distance_2d(hull%vertices(i), hull%vertices(j)))
            end do
        end do

    end function farthest_pair_of_points

    !===============================================
    ! Additional geometric algorithms
    !===============================================

    function polygon_area(vertices) result(area)
        implicit none
        type(point_2d), dimension(:), intent(in) :: vertices
        real(real64) :: area
        type(polygon_2d) :: poly

        call poly%init(vertices)
        area = poly%area()

    end function polygon_area

    function polygon_perimeter(vertices) result(perim)
        implicit none
        type(point_2d), dimension(:), intent(in) :: vertices
        real(real64) :: perim
        type(polygon_2d) :: poly

        call poly%init(vertices)
        perim = poly%perimeter()

    end function polygon_perimeter

    function triangle_area(p1, p2, p3) result(area)
        implicit none
        type(point_2d), intent(in) :: p1, p2, p3
        real(real64) :: area
        type(triangle_2d) :: tri

        tri%p1 = p1
        tri%p2 = p2
        tri%p3 = p3
        area = tri%area()

    end function triangle_area

    function triangle_circumcenter(p1, p2, p3) result(center)
        implicit none
        type(point_2d), intent(in) :: p1, p2, p3
        type(point_2d) :: center
        real(real64) :: d, ux, uy, vx, vy

        d = 2.0_real64 * (p1%x * (p2%y - p3%y) + p2%x * (p3%y - p1%y) + p3%x * (p1%y - p2%y))

        ux = ((p1%x**2 + p1%y**2) * (p2%y - p3%y) + &
              (p2%x**2 + p2%y**2) * (p3%y - p1%y) + &
              (p3%x**2 + p3%y**2) * (p1%y - p2%y)) / d

        uy = ((p1%x**2 + p1%y**2) * (p3%x - p2%x) + &
              (p2%x**2 + p2%y**2) * (p1%x - p3%x) + &
              (p3%x**2 + p3%y**2) * (p2%x - p1%x)) / d

        center%x = ux
        center%y = uy

    end function triangle_circumcenter

    function circle_from_three_points(p1, p2, p3) result(circ)
        implicit none
        type(point_2d), intent(in) :: p1, p2, p3
        type(circle) :: circ

        circ%center = triangle_circumcenter(p1, p2, p3)
        circ%radius = circ%center%distance(p1)

    end function circle_from_three_points

    !===============================================
    ! Transformations
    !===============================================

    function rotate_point_2d(p, angle, center) result(rotated)
        implicit none
        type(point_2d), intent(in) :: p
        real(real64), intent(in) :: angle
        type(point_2d), intent(in), optional :: center
        type(point_2d) :: rotated
        real(real64) :: cos_a, sin_a, cx, cy

        if (present(center)) then
            cx = center%x
            cy = center%y
        else
            cx = 0.0_real64
            cy = 0.0_real64
        end if

        cos_a = cos(angle)
        sin_a = sin(angle)

        rotated%x = (p%x - cx) * cos_a - (p%y - cy) * sin_a + cx
        rotated%y = (p%x - cx) * sin_a + (p%y - cy) * cos_a + cy

    end function rotate_point_2d

    function rotate_point_3d(p, axis, angle) result(rotated)
        implicit none
        type(point_3d), intent(in) :: p, axis
        real(real64), intent(in) :: angle
        type(point_3d) :: rotated
        real(real64) :: cos_a, sin_a, dot_val
        type(point_3d) :: k, v_parallel, v_perp, w

        ! Normalize axis
        dot_val = sqrt(dot_product_3d(axis, axis))
        k%x = axis%x / dot_val
        k%y = axis%y / dot_val
        k%z = axis%z / dot_val

        cos_a = cos(angle)
        sin_a = sin(angle)

        ! Rodrigues' rotation formula
        dot_val = dot_product_3d(k, p)
        v_parallel%x = dot_val * k%x
        v_parallel%y = dot_val * k%y
        v_parallel%z = dot_val * k%z

        v_perp%x = p%x - v_parallel%x
        v_perp%y = p%y - v_parallel%y
        v_perp%z = p%z - v_parallel%z

        w = cross_product_3d(k, p)

        rotated%x = v_parallel%x + cos_a * v_perp%x + sin_a * w%x
        rotated%y = v_parallel%y + cos_a * v_perp%y + sin_a * w%y
        rotated%z = v_parallel%z + cos_a * v_perp%z + sin_a * w%z

    end function rotate_point_3d

    function translate_point(p, dx, dy, dz) result(translated)
        implicit none
        type(point_3d), intent(in) :: p
        real(real64), intent(in) :: dx, dy
        real(real64), intent(in), optional :: dz
        type(point_3d) :: translated

        translated%x = p%x + dx
        translated%y = p%y + dy

        if (present(dz)) then
            translated%z = p%z + dz
        else
            translated%z = p%z
        end if

    end function translate_point

    function scale_point(p, sx, sy, sz) result(scaled)
        implicit none
        type(point_3d), intent(in) :: p
        real(real64), intent(in) :: sx, sy
        real(real64), intent(in), optional :: sz
        type(point_3d) :: scaled

        scaled%x = p%x * sx
        scaled%y = p%y * sy

        if (present(sz)) then
            scaled%z = p%z * sz
        else
            scaled%z = p%z
        end if

    end function scale_point

    !===============================================
    ! Spatial data structures
    !===============================================

    subroutine quadtree_init(this, boundary, capacity)
        implicit none
        class(quadtree_type), intent(inout) :: this
        type(rectangle), intent(in) :: boundary
        integer(int32), intent(in) :: capacity

        allocate(this%root)
        this%root%boundary = boundary
        this%root%is_leaf = .true.
        this%root%n_points = 0
        this%capacity = capacity
        allocate(this%root%points(capacity))

    end subroutine quadtree_init

    subroutine quadtree_insert(this, p)
        implicit none
        class(quadtree_type), intent(inout) :: this
        type(point_2d), intent(in) :: p

        call insert_node(this%root, p, this%capacity)

    contains

        recursive subroutine insert_node(node, point, cap)
            implicit none
            type(quadtree_node), pointer :: node
            type(point_2d), intent(in) :: point
            integer(int32), intent(in) :: cap

            if (.not. node%boundary%contains_point(point)) return

            if (node%is_leaf) then
                if (node%n_points < cap) then
                    node%n_points = node%n_points + 1
                    node%points(node%n_points) = point
                else
                    call subdivide_node(node, cap)
                    call insert_node(node, point, cap)
                end if
            else
                call insert_node(node%ne, point, cap)
                call insert_node(node%nw, point, cap)
                call insert_node(node%se, point, cap)
                call insert_node(node%sw, point, cap)
            end if

        end subroutine insert_node

        subroutine subdivide_node(node, cap)
            implicit none
            type(quadtree_node), pointer :: node
            integer(int32), intent(in) :: cap
            real(real64) :: cx, cy, hw, hh
            integer(int32) :: i

            cx = (node%boundary%min_point%x + node%boundary%max_point%x) / 2.0_real64
            cy = (node%boundary%min_point%y + node%boundary%max_point%y) / 2.0_real64
            hw = (node%boundary%max_point%x - node%boundary%min_point%x) / 2.0_real64
            hh = (node%boundary%max_point%y - node%boundary%min_point%y) / 2.0_real64

            allocate(node%ne)
            allocate(node%nw)
            allocate(node%se)
            allocate(node%sw)

            ! Initialize quadrants
            ! ... (initialization code for each quadrant)

            node%is_leaf = .false.

            ! Reinsert points
            do i = 1, node%n_points
                call insert_node(node, node%points(i), cap)
            end do

            deallocate(node%points)
            node%n_points = 0

        end subroutine subdivide_node

    end subroutine quadtree_insert

    function quadtree_query_range(this, range) result(points)
        implicit none
        class(quadtree_type), intent(in) :: this
        type(rectangle), intent(in) :: range
        type(point_2d), dimension(:), allocatable :: points
        type(point_2d), dimension(:), allocatable :: temp_points
        integer(int32) :: count

        allocate(temp_points(1000))
        count = 0
        call query_node(this%root, range, temp_points, count)

        allocate(points(count))
        points = temp_points(1:count)

    contains

        recursive subroutine query_node(node, range, pts, cnt)
            implicit none
            type(quadtree_node), pointer :: node
            type(rectangle), intent(in) :: range
            type(point_2d), dimension(:), intent(inout) :: pts
            integer(int32), intent(inout) :: cnt
            integer(int32) :: i

            ! Check if boundaries intersect
            if (.not. rectangles_intersect(node%boundary, range)) return

            if (node%is_leaf) then
                do i = 1, node%n_points
                    if (range%contains_point(node%points(i))) then
                        cnt = cnt + 1
                        pts(cnt) = node%points(i)
                    end if
                end do
            else
                call query_node(node%ne, range, pts, cnt)
                call query_node(node%nw, range, pts, cnt)
                call query_node(node%se, range, pts, cnt)
                call query_node(node%sw, range, pts, cnt)
            end if

        end subroutine query_node

        function rectangles_intersect(r1, r2) result(intersect)
            implicit none
            type(rectangle), intent(in) :: r1, r2
            logical :: intersect

            intersect = .not. (r1%max_point%x < r2%min_point%x .or. &
                              r2%max_point%x < r1%min_point%x .or. &
                              r1%max_point%y < r2%min_point%y .or. &
                              r2%max_point%y < r1%min_point%y)

        end function rectangles_intersect

    end function quadtree_query_range

    ! Similar implementations for octree, kd-tree, and range tree...
    ! (These would follow similar patterns but for 3D or specialized queries)

    subroutine octree_init(this, boundary, capacity)
        implicit none
        class(octree_type), intent(inout) :: this
        type(box_3d), intent(in) :: boundary
        integer(int32), intent(in) :: capacity

        ! Implementation similar to quadtree but for 3D
        this%capacity = capacity

    end subroutine octree_init

    subroutine octree_insert(this, p)
        implicit none
        class(octree_type), intent(inout) :: this
        type(point_3d), intent(in) :: p

        ! Implementation similar to quadtree but for 3D

    end subroutine octree_insert

    function octree_query_range(this, range) result(points)
        implicit none
        class(octree_type), intent(in) :: this
        type(box_3d), intent(in) :: range
        type(point_3d), dimension(:), allocatable :: points

        allocate(points(0))
        ! Implementation similar to quadtree but for 3D

    end function octree_query_range

    subroutine kd_tree_init(this, dims)
        implicit none
        class(kd_tree_type), intent(inout) :: this
        integer(int32), intent(in) :: dims

        this%dimensions = dims
        this%root => null()

    end subroutine kd_tree_init

    subroutine kd_tree_insert(this, p)
        implicit none
        class(kd_tree_type), intent(inout) :: this
        type(point_2d), intent(in) :: p

        ! KD-tree insertion implementation

    end subroutine kd_tree_insert

    function kd_tree_nearest_neighbor(this, p) result(nearest)
        implicit none
        class(kd_tree_type), intent(in) :: this
        type(point_2d), intent(in) :: p
        type(point_2d) :: nearest

        ! KD-tree nearest neighbor search

    end function kd_tree_nearest_neighbor

    subroutine range_tree_init(this)
        implicit none
        class(range_tree_type), intent(inout) :: this

        this%root => null()

    end subroutine range_tree_init

    function range_tree_query_2d(this, x_min, x_max, y_min, y_max) result(points)
        implicit none
        class(range_tree_type), intent(in) :: this
        real(real64), intent(in) :: x_min, x_max, y_min, y_max
        type(point_2d), dimension(:), allocatable :: points

        allocate(points(0))
        ! Range tree 2D query implementation

    end function range_tree_query_2d

    !===============================================
    ! Computational geometry utilities
    !===============================================

    function polygon_centroid(poly) result(centroid)
        implicit none
        type(polygon_2d), intent(in) :: poly
        type(point_2d) :: centroid
        real(real64) :: area, cx, cy, a
        integer(int32) :: i

        area = 0.0_real64
        cx = 0.0_real64
        cy = 0.0_real64

        do i = 1, poly%n_vertices
            a = poly%vertices(i)%x * poly%vertices(mod(i, poly%n_vertices) + 1)%y - &
                poly%vertices(mod(i, poly%n_vertices) + 1)%x * poly%vertices(i)%y
            area = area + a
            cx = cx + (poly%vertices(i)%x + poly%vertices(mod(i, poly%n_vertices) + 1)%x) * a
            cy = cy + (poly%vertices(i)%y + poly%vertices(mod(i, poly%n_vertices) + 1)%y) * a
        end do

        area = area * 0.5_real64
        centroid%x = cx / (6.0_real64 * area)
        centroid%y = cy / (6.0_real64 * area)

    end function polygon_centroid

    function polygon_convex_check(poly) result(is_convex)
        implicit none
        type(polygon_2d), intent(in) :: poly
        logical :: is_convex

        is_convex = poly%is_convex()

    end function polygon_convex_check

    ! Additional stub functions for complex algorithms

    function minimum_enclosing_circle(points) result(circ)
        implicit none
        type(point_2d), dimension(:), intent(in) :: points
        type(circle) :: circ

        ! Welzl's algorithm implementation
        circ%center = point_2d(0.0_real64, 0.0_real64)
        circ%radius = 0.0_real64

    end function minimum_enclosing_circle

    function line_sweep_intersections(segments) result(intersections)
        implicit none
        type(segment_2d), dimension(:), intent(in) :: segments
        type(point_2d), dimension(:), allocatable :: intersections

        allocate(intersections(0))
        ! Line sweep algorithm implementation

    end function line_sweep_intersections

    function bentley_ottmann(segments) result(intersections)
        implicit none
        type(segment_2d), dimension(:), intent(in) :: segments
        type(point_2d), dimension(:), allocatable :: intersections

        allocate(intersections(0))
        ! Bentley-Ottmann algorithm implementation

    end function bentley_ottmann

    function voronoi_diagram(points) result(diagram)
        implicit none
        type(point_2d), dimension(:), intent(in) :: points
        type(polygon_2d), dimension(:), allocatable :: diagram

        allocate(diagram(0))
        ! Fortune's algorithm implementation

    end function voronoi_diagram

    function delaunay_triangulation(points) result(triangles)
        implicit none
        type(point_2d), dimension(:), intent(in) :: points
        type(triangle_2d), dimension(:), allocatable :: triangles

        allocate(triangles(0))
        ! Bowyer-Watson algorithm implementation

    end function delaunay_triangulation

    function polygon_triangulation(poly) result(triangles)
        implicit none
        type(polygon_2d), intent(in) :: poly
        type(triangle_2d), dimension(:), allocatable :: triangles

        allocate(triangles(0))
        ! Ear clipping or monotone polygon triangulation

    end function polygon_triangulation

    function ear_clipping(poly) result(triangles)
        implicit none
        type(polygon_2d), intent(in) :: poly
        type(triangle_2d), dimension(:), allocatable :: triangles

        allocate(triangles(0))
        ! Ear clipping triangulation

    end function ear_clipping

    function ray_casting(ray, objects) result(hit_point)
        implicit none
        type(ray_2d), intent(in) :: ray
        type(segment_2d), dimension(:), intent(in) :: objects
        type(point_2d) :: hit_point

        hit_point%x = huge(1.0_real64)
        hit_point%y = huge(1.0_real64)
        ! Ray casting implementation

    end function ray_casting

    function ray_tracing_intersection(ray, triangle) result(hit)
        implicit none
        type(ray_3d), intent(in) :: ray
        type(triangle_3d), intent(in) :: triangle
        logical :: hit

        hit = .false.
        ! Möller-Trumbore algorithm

    end function ray_tracing_intersection

    function bounding_box_2d(points) result(box)
        implicit none
        type(point_2d), dimension(:), intent(in) :: points
        type(rectangle) :: box
        integer(int32) :: i

        box%min_point%x = points(1)%x
        box%min_point%y = points(1)%y
        box%max_point%x = points(1)%x
        box%max_point%y = points(1)%y

        do i = 2, size(points)
            box%min_point%x = min(box%min_point%x, points(i)%x)
            box%min_point%y = min(box%min_point%y, points(i)%y)
            box%max_point%x = max(box%max_point%x, points(i)%x)
            box%max_point%y = max(box%max_point%y, points(i)%y)
        end do

    end function bounding_box_2d

    function bounding_box_3d(points) result(box)
        implicit none
        type(point_3d), dimension(:), intent(in) :: points
        type(box_3d) :: box
        integer(int32) :: i

        box%min_point = points(1)
        box%max_point = points(1)

        do i = 2, size(points)
            box%min_point%x = min(box%min_point%x, points(i)%x)
            box%min_point%y = min(box%min_point%y, points(i)%y)
            box%min_point%z = min(box%min_point%z, points(i)%z)
            box%max_point%x = max(box%max_point%x, points(i)%x)
            box%max_point%y = max(box%max_point%y, points(i)%y)
            box%max_point%z = max(box%max_point%z, points(i)%z)
        end do

    end function bounding_box_3d

    function reflection_2d(p, line) result(reflected)
        implicit none
        type(point_2d), intent(in) :: p
        type(line_2d), intent(in) :: line
        type(point_2d) :: reflected
        real(real64) :: dist, factor

        dist = line%distance_to_point(p)
        factor = 2.0_real64 * dist / (line%a**2 + line%b**2)

        reflected%x = p%x - factor * line%a
        reflected%y = p%y - factor * line%b

    end function reflection_2d

    function projection_on_line(p, line) result(projected)
        implicit none
        type(point_2d), intent(in) :: p
        type(line_2d), intent(in) :: line
        type(point_2d) :: projected
        real(real64) :: factor

        factor = -(line%a * p%x + line%b * p%y + line%c) / (line%a**2 + line%b**2)
        projected%x = p%x + factor * line%a
        projected%y = p%y + factor * line%b

    end function projection_on_line

    function point_on_line(p, line) result(on_line)
        implicit none
        type(point_2d), intent(in) :: p
        type(line_2d), intent(in) :: line
        logical :: on_line

        on_line = abs(line%a * p%x + line%b * p%y + line%c) < EPS

    end function point_on_line

    function point_on_segment(p, seg) result(on_segment)
        implicit none
        type(point_2d), intent(in) :: p
        type(segment_2d), intent(in) :: seg
        logical :: on_segment
        real(real64) :: cross, dot, len_sq

        cross = (p%x - seg%p1%x) * (seg%p2%y - seg%p1%y) - &
                (p%y - seg%p1%y) * (seg%p2%x - seg%p1%x)

        if (abs(cross) > EPS) then
            on_segment = .false.
            return
        end if

        dot = (p%x - seg%p1%x) * (seg%p2%x - seg%p1%x) + &
              (p%y - seg%p1%y) * (seg%p2%y - seg%p1%y)
        len_sq = (seg%p2%x - seg%p1%x)**2 + (seg%p2%y - seg%p1%y)**2

        on_segment = dot >= -EPS .and. dot <= len_sq + EPS

    end function point_on_segment

    function angle_between_lines(l1, l2) result(angle)
        implicit none
        type(line_2d), intent(in) :: l1, l2
        real(real64) :: angle

        angle = atan2(l1%a * l2%b - l1%b * l2%a, l1%a * l2%a + l1%b * l2%b)

    end function angle_between_lines

end module geometry_module