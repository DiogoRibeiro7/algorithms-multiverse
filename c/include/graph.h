/**
 * @file graph.h
 * @brief Graph algorithms interface
 */

#ifndef AM_GRAPH_H
#define AM_GRAPH_H

#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Graph representation types */
typedef enum {
    GRAPH_ADJ_MATRIX,
    GRAPH_ADJ_LIST,
    GRAPH_EDGE_LIST
} graph_repr_t;

/* Graph types */
typedef enum {
    GRAPH_UNDIRECTED = 0,
    GRAPH_DIRECTED = 1,
    GRAPH_WEIGHTED = 2,
    GRAPH_DIRECTED_WEIGHTED = 3
} graph_type_t;

/* Forward declarations */
typedef struct graph graph_t;
typedef struct edge edge_t;
typedef struct vertex vertex_t;

/* Edge structure */
struct edge {
    size_t src;
    size_t dest;
    double weight;
    void* data;
};

/* Vertex structure */
struct vertex {
    size_t id;
    void* data;
    size_t degree;
    edge_t** edges;
};

/* Graph creation and destruction */
graph_t* graph_create(size_t num_vertices, graph_type_t type, graph_repr_t repr);
void graph_destroy(graph_t* graph);
graph_t* graph_copy(const graph_t* graph);

/* Basic graph operations */
bool graph_add_edge(graph_t* graph, size_t src, size_t dest, double weight);
bool graph_remove_edge(graph_t* graph, size_t src, size_t dest);
bool graph_has_edge(const graph_t* graph, size_t src, size_t dest);
double graph_get_edge_weight(const graph_t* graph, size_t src, size_t dest);
bool graph_add_vertex(graph_t* graph, void* data);
bool graph_remove_vertex(graph_t* graph, size_t vertex);
size_t graph_num_vertices(const graph_t* graph);
size_t graph_num_edges(const graph_t* graph);
size_t graph_degree(const graph_t* graph, size_t vertex);
size_t graph_in_degree(const graph_t* graph, size_t vertex);
size_t graph_out_degree(const graph_t* graph, size_t vertex);

/* Graph traversal */
void graph_bfs(const graph_t* graph, size_t start,
               void (*visit)(size_t vertex, void* data), void* data);
void graph_dfs(const graph_t* graph, size_t start,
               void (*visit)(size_t vertex, void* data), void* data);
size_t* graph_bfs_path(const graph_t* graph, size_t start, size_t* visited);
size_t* graph_dfs_path(const graph_t* graph, size_t start, size_t* visited);

/* Shortest path algorithms */
double* graph_dijkstra(const graph_t* graph, size_t src, size_t* predecessors);
double** graph_floyd_warshall(const graph_t* graph, size_t** next);
bool graph_bellman_ford(const graph_t* graph, size_t src,
                        double* distances, size_t* predecessors);
double graph_a_star(const graph_t* graph, size_t start, size_t goal,
                    double (*heuristic)(size_t, size_t), size_t** path, size_t* path_len);

/* Minimum spanning tree */
edge_t* graph_kruskal_mst(const graph_t* graph, size_t* num_edges, double* total_weight);
edge_t* graph_prim_mst(const graph_t* graph, size_t* num_edges, double* total_weight);

/* Topological sorting */
size_t* graph_topological_sort(const graph_t* graph, bool* has_cycle);
bool graph_has_cycle(const graph_t* graph);

/* Strongly connected components */
size_t graph_strongly_connected_components(const graph_t* graph, size_t* components);
size_t graph_kosaraju_scc(const graph_t* graph, size_t* components);
size_t graph_tarjan_scc(const graph_t* graph, size_t* components);

/* Graph coloring */
size_t graph_greedy_coloring(const graph_t* graph, size_t* colors);
bool graph_is_bipartite(const graph_t* graph, size_t* colors);

/* Network flow */
double graph_ford_fulkerson(const graph_t* graph, size_t source, size_t sink);
double graph_edmonds_karp(const graph_t* graph, size_t source, size_t sink);
double graph_dinic(const graph_t* graph, size_t source, size_t sink);

/* Graph properties */
bool graph_is_connected(const graph_t* graph);
bool graph_is_eulerian(const graph_t* graph);
bool graph_is_hamiltonian(const graph_t* graph);
bool graph_is_planar(const graph_t* graph);
bool graph_is_tree(const graph_t* graph);
bool graph_is_dag(const graph_t* graph);
size_t graph_diameter(const graph_t* graph);
double graph_clustering_coefficient(const graph_t* graph, size_t vertex);
double graph_avg_clustering_coefficient(const graph_t* graph);

/* Articulation points and bridges */
size_t* graph_articulation_points(const graph_t* graph, size_t* count);
edge_t* graph_bridges(const graph_t* graph, size_t* count);

/* Matching algorithms */
size_t graph_max_bipartite_matching(const graph_t* graph, size_t* matching);
edge_t* graph_hungarian_algorithm(const graph_t* graph, size_t* num_edges);

/* Community detection */
size_t graph_louvain_communities(const graph_t* graph, size_t* communities);
double graph_modularity(const graph_t* graph, const size_t* communities);

/* Graph generation */
graph_t* graph_generate_complete(size_t n);
graph_t* graph_generate_cycle(size_t n);
graph_t* graph_generate_path(size_t n);
graph_t* graph_generate_random(size_t n, double edge_probability);
graph_t* graph_generate_random_weighted(size_t n, double edge_probability,
                                        double min_weight, double max_weight);

/* Graph I/O */
graph_t* graph_load_from_file(const char* filename);
bool graph_save_to_file(const graph_t* graph, const char* filename);
void graph_print(const graph_t* graph);
char* graph_to_dot(const graph_t* graph);

#ifdef __cplusplus
}
#endif

#endif /* AM_GRAPH_H */