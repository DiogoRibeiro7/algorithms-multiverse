/**
 * @file geometry.h
 * @brief Computational geometry algorithms interface
 */

#ifndef AM_GEOMETRY_H
#define AM_GEOMETRY_H

#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Basic geometric structures */
typedef struct {
    double x;
    double y;
} point2d_t;

typedef struct {
    double x;
    double y;
    double z;
} point3d_t;

typedef struct {
    point2d_t start;
    point2d_t end;
} segment2d_t;

typedef struct {
    point3d_t start;
    point3d_t end;
} segment3d_t;

typedef struct {
    point2d_t a;
    point2d_t b;
    point2d_t c;
} triangle2d_t;

typedef struct {
    point2d_t center;
    double radius;
} circle_t;

typedef struct {
    point2d_t* vertices;
    size_t num_vertices;
} polygon_t;

typedef struct {
    double a;  /* ax + by + c = 0 */
    double b;
    double c;
} line2d_t;

typedef struct {
    point3d_t point;
    point3d_t normal;
} plane_t;

typedef struct {
    point2d_t min;
    point2d_t max;
} rect_t;

typedef struct {
    point3d_t min;
    point3d_t max;
} box3d_t;

/* Basic operations */
double point2d_distance(const point2d_t* p1, const point2d_t* p2);
double point3d_distance(const point3d_t* p1, const point3d_t* p2);
double point2d_manhattan_distance(const point2d_t* p1, const point2d_t* p2);
point2d_t point2d_midpoint(const point2d_t* p1, const point2d_t* p2);
point3d_t point3d_midpoint(const point3d_t* p1, const point3d_t* p2);

/* Vector operations */
double dot_product_2d(const point2d_t* v1, const point2d_t* v2);
double dot_product_3d(const point3d_t* v1, const point3d_t* v2);
double cross_product_2d(const point2d_t* v1, const point2d_t* v2);
point3d_t cross_product_3d(const point3d_t* v1, const point3d_t* v2);
double vector2d_magnitude(const point2d_t* v);
double vector3d_magnitude(const point3d_t* v);
point2d_t vector2d_normalize(const point2d_t* v);
point3d_t vector3d_normalize(const point3d_t* v);
double angle_between_vectors_2d(const point2d_t* v1, const point2d_t* v2);
double angle_between_vectors_3d(const point3d_t* v1, const point3d_t* v2);

/* Line and segment operations */
bool segments_intersect(const segment2d_t* s1, const segment2d_t* s2,
                        point2d_t* intersection);
double point_to_line_distance(const point2d_t* point, const line2d_t* line);
double point_to_segment_distance(const point2d_t* point, const segment2d_t* segment);
bool point_on_segment(const point2d_t* point, const segment2d_t* segment);
int point_orientation(const point2d_t* p, const point2d_t* q, const point2d_t* r);

/* Polygon operations */
polygon_t* polygon_create(const point2d_t* vertices, size_t num_vertices);
void polygon_destroy(polygon_t* poly);
double polygon_area(const polygon_t* poly);
double polygon_perimeter(const polygon_t* poly);
point2d_t polygon_centroid(const polygon_t* poly);
bool polygon_is_convex(const polygon_t* poly);
bool polygon_is_simple(const polygon_t* poly);
bool point_in_polygon(const point2d_t* point, const polygon_t* poly);
polygon_t* polygon_offset(const polygon_t* poly, double distance);

/* Convex hull algorithms */
polygon_t* convex_hull_graham_scan(const point2d_t* points, size_t n);
polygon_t* convex_hull_jarvis_march(const point2d_t* points, size_t n);
polygon_t* convex_hull_quickhull(const point2d_t* points, size_t n);
polygon_t* convex_hull_incremental(const point2d_t* points, size_t n);
point3d_t* convex_hull_3d(const point3d_t* points, size_t n, size_t* hull_size);

/* Circle operations */
bool circle_contains_point(const circle_t* circle, const point2d_t* point);
bool circles_intersect(const circle_t* c1, const circle_t* c2,
                       point2d_t* intersections, size_t* count);
circle_t minimum_enclosing_circle(const point2d_t* points, size_t n);
double circle_area(const circle_t* circle);
double circle_circumference(const circle_t* circle);

/* Triangle operations */
double triangle_area(const triangle2d_t* tri);
double triangle_perimeter(const triangle2d_t* tri);
point2d_t triangle_centroid(const triangle2d_t* tri);
circle_t triangle_circumcircle(const triangle2d_t* tri);
circle_t triangle_incircle(const triangle2d_t* tri);
bool point_in_triangle(const point2d_t* point, const triangle2d_t* tri);

/* Closest pair problem */
void closest_pair_2d(const point2d_t* points, size_t n,
                     point2d_t* p1, point2d_t* p2, double* distance);
void closest_pair_3d(const point3d_t* points, size_t n,
                     point3d_t* p1, point3d_t* p2, double* distance);

/* Triangulation */
typedef struct {
    size_t v1, v2, v3;
} triangle_indices_t;

triangle_indices_t* delaunay_triangulation(const point2d_t* points, size_t n,
                                           size_t* num_triangles);
triangle_indices_t* polygon_triangulate(const polygon_t* poly,
                                        size_t* num_triangles);

/* Voronoi diagram */
typedef struct voronoi_diagram voronoi_diagram_t;

voronoi_diagram_t* voronoi_create(const point2d_t* points, size_t n);
void voronoi_destroy(voronoi_diagram_t* diagram);
polygon_t* voronoi_get_cell(const voronoi_diagram_t* diagram, size_t index);

/* Spatial data structures */
typedef struct kd_tree kd_tree_t;
typedef struct quad_tree quad_tree_t;
typedef struct r_tree r_tree_t;

/* KD-Tree */
kd_tree_t* kd_tree_create_2d(const point2d_t* points, size_t n);
kd_tree_t* kd_tree_create_3d(const point3d_t* points, size_t n);
void kd_tree_destroy(kd_tree_t* tree);
void kd_tree_insert_2d(kd_tree_t* tree, const point2d_t* point);
void kd_tree_insert_3d(kd_tree_t* tree, const point3d_t* point);
point2d_t* kd_tree_nearest_neighbor_2d(const kd_tree_t* tree,
                                       const point2d_t* query);
point3d_t* kd_tree_nearest_neighbor_3d(const kd_tree_t* tree,
                                       const point3d_t* query);
point2d_t** kd_tree_range_query_2d(const kd_tree_t* tree, const rect_t* range,
                                   size_t* count);

/* QuadTree */
quad_tree_t* quad_tree_create(const rect_t* boundary, size_t capacity);
void quad_tree_destroy(quad_tree_t* tree);
bool quad_tree_insert(quad_tree_t* tree, const point2d_t* point);
point2d_t** quad_tree_query_range(const quad_tree_t* tree, const rect_t* range,
                                  size_t* count);
point2d_t** quad_tree_query_circle(const quad_tree_t* tree, const circle_t* circle,
                                   size_t* count);

/* R-Tree */
r_tree_t* r_tree_create(size_t min_entries, size_t max_entries);
void r_tree_destroy(r_tree_t* tree);
bool r_tree_insert(r_tree_t* tree, const rect_t* rect, void* data);
void** r_tree_search(const r_tree_t* tree, const rect_t* search_rect,
                     size_t* count);

/* Sweep line algorithms */
segment2d_t* find_all_intersections(const segment2d_t* segments, size_t n,
                                    size_t* num_intersections);
double union_of_rectangles_area(const rect_t* rectangles, size_t n);

/* Geometric transformations */
point2d_t point2d_rotate(const point2d_t* p, double angle);
point2d_t point2d_translate(const point2d_t* p, double dx, double dy);
point2d_t point2d_scale(const point2d_t* p, double sx, double sy);
polygon_t* polygon_rotate(const polygon_t* poly, double angle);
polygon_t* polygon_translate(const polygon_t* poly, double dx, double dy);
polygon_t* polygon_scale(const polygon_t* poly, double sx, double sy);

/* Boolean operations on polygons */
polygon_t* polygon_union(const polygon_t* p1, const polygon_t* p2);
polygon_t* polygon_intersection(const polygon_t* p1, const polygon_t* p2);
polygon_t* polygon_difference(const polygon_t* p1, const polygon_t* p2);

#ifdef __cplusplus
}
#endif

#endif /* AM_GEOMETRY_H */