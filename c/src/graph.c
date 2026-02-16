/**
 * @file graph.c
 * @brief Implementation of graph algorithms
 */

#include "graph.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <limits.h>
#include <float.h>
#include <math.h>

#define MIN(a,b) ((a) < (b) ? (a) : (b))
#define MAX(a,b) ((a) > (b) ? (a) : (b))

/* =========================== */
/*    Graph Data Structure     */
/* =========================== */

typedef struct adj_node {
    size_t vertex;
    double weight;
    struct adj_node* next;
} adj_node_t;

typedef struct adj_list {
    adj_node_t* head;
} adj_list_t;

struct graph {
    size_t num_vertices;
    size_t num_edges;
    graph_type_t type;
    graph_repr_t repr;

    /* Different representations */
    double** adj_matrix;      /* For adjacency matrix */
    adj_list_t* adj_lists;    /* For adjacency list */
    edge_t* edge_list;        /* For edge list */
    size_t edge_list_capacity;
};

/* =========================== */
/*   Graph Creation/Destroy    */
/* =========================== */

graph_t* graph_create(size_t num_vertices, graph_type_t type, graph_repr_t repr) {
    graph_t* graph = calloc(1, sizeof(graph_t));
    if (!graph) return NULL;

    graph->num_vertices = num_vertices;
    graph->num_edges = 0;
    graph->type = type;
    graph->repr = repr;

    switch (repr) {
        case GRAPH_ADJ_MATRIX:
            /* Allocate adjacency matrix */
            graph->adj_matrix = calloc(num_vertices, sizeof(double*));
            for (size_t i = 0; i < num_vertices; i++) {
                graph->adj_matrix[i] = calloc(num_vertices, sizeof(double));
                /* Initialize with infinity for weighted graphs */
                if (type & GRAPH_WEIGHTED) {
                    for (size_t j = 0; j < num_vertices; j++) {
                        if (i != j) {
                            graph->adj_matrix[i][j] = INFINITY;
                        }
                    }
                }
            }
            break;

        case GRAPH_ADJ_LIST:
            /* Allocate adjacency lists */
            graph->adj_lists = calloc(num_vertices, sizeof(adj_list_t));
            break;

        case GRAPH_EDGE_LIST:
            /* Allocate edge list */
            graph->edge_list_capacity = 16;
            graph->edge_list = malloc(graph->edge_list_capacity * sizeof(edge_t));
            break;
    }

    return graph;
}

void graph_destroy(graph_t* graph) {
    if (!graph) return;

    switch (graph->repr) {
        case GRAPH_ADJ_MATRIX:
            if (graph->adj_matrix) {
                for (size_t i = 0; i < graph->num_vertices; i++) {
                    free(graph->adj_matrix[i]);
                }
                free(graph->adj_matrix);
            }
            break;

        case GRAPH_ADJ_LIST:
            if (graph->adj_lists) {
                for (size_t i = 0; i < graph->num_vertices; i++) {
                    adj_node_t* current = graph->adj_lists[i].head;
                    while (current) {
                        adj_node_t* temp = current;
                        current = current->next;
                        free(temp);
                    }
                }
                free(graph->adj_lists);
            }
            break;

        case GRAPH_EDGE_LIST:
            free(graph->edge_list);
            break;
    }

    free(graph);
}

graph_t* graph_copy(const graph_t* graph) {
    if (!graph) return NULL;

    graph_t* copy = graph_create(graph->num_vertices, graph->type, graph->repr);
    if (!copy) return NULL;

    switch (graph->repr) {
        case GRAPH_ADJ_MATRIX:
            for (size_t i = 0; i < graph->num_vertices; i++) {
                memcpy(copy->adj_matrix[i], graph->adj_matrix[i],
                       graph->num_vertices * sizeof(double));
            }
            break;

        case GRAPH_ADJ_LIST:
            for (size_t i = 0; i < graph->num_vertices; i++) {
                adj_node_t* current = graph->adj_lists[i].head;
                while (current) {
                    graph_add_edge(copy, i, current->vertex, current->weight);
                    current = current->next;
                }
            }
            break;

        case GRAPH_EDGE_LIST:
            for (size_t i = 0; i < graph->num_edges; i++) {
                graph_add_edge(copy, graph->edge_list[i].src,
                              graph->edge_list[i].dest,
                              graph->edge_list[i].weight);
            }
            break;
    }

    copy->num_edges = graph->num_edges;
    return copy;
}

/* =========================== */
/*    Basic Graph Operations   */
/* =========================== */

bool graph_add_edge(graph_t* graph, size_t src, size_t dest, double weight) {
    if (!graph || src >= graph->num_vertices || dest >= graph->num_vertices) {
        return false;
    }

    bool is_directed = (graph->type & GRAPH_DIRECTED) != 0;
    bool is_weighted = (graph->type & GRAPH_WEIGHTED) != 0;
    if (!is_weighted) weight = 1.0;

    switch (graph->repr) {
        case GRAPH_ADJ_MATRIX:
            graph->adj_matrix[src][dest] = weight;
            if (!is_directed) {
                graph->adj_matrix[dest][src] = weight;
            }
            break;

        case GRAPH_ADJ_LIST: {
            /* Add to src's adjacency list */
            adj_node_t* new_node = malloc(sizeof(adj_node_t));
            new_node->vertex = dest;
            new_node->weight = weight;
            new_node->next = graph->adj_lists[src].head;
            graph->adj_lists[src].head = new_node;

            if (!is_directed) {
                /* Add to dest's adjacency list */
                new_node = malloc(sizeof(adj_node_t));
                new_node->vertex = src;
                new_node->weight = weight;
                new_node->next = graph->adj_lists[dest].head;
                graph->adj_lists[dest].head = new_node;
            }
            break;
        }

        case GRAPH_EDGE_LIST: {
            /* Expand edge list if needed */
            if (graph->num_edges >= graph->edge_list_capacity) {
                graph->edge_list_capacity *= 2;
                graph->edge_list = realloc(graph->edge_list,
                    graph->edge_list_capacity * sizeof(edge_t));
            }

            graph->edge_list[graph->num_edges].src = src;
            graph->edge_list[graph->num_edges].dest = dest;
            graph->edge_list[graph->num_edges].weight = weight;
            graph->edge_list[graph->num_edges].data = NULL;
            break;
        }
    }

    graph->num_edges++;
    return true;
}

bool graph_has_edge(const graph_t* graph, size_t src, size_t dest) {
    if (!graph || src >= graph->num_vertices || dest >= graph->num_vertices) {
        return false;
    }

    switch (graph->repr) {
        case GRAPH_ADJ_MATRIX:
            if (graph->type & GRAPH_WEIGHTED) {
                return !isinf(graph->adj_matrix[src][dest]);
            }
            return graph->adj_matrix[src][dest] != 0;

        case GRAPH_ADJ_LIST: {
            adj_node_t* current = graph->adj_lists[src].head;
            while (current) {
                if (current->vertex == dest) return true;
                current = current->next;
            }
            return false;
        }

        case GRAPH_EDGE_LIST:
            for (size_t i = 0; i < graph->num_edges; i++) {
                if (graph->edge_list[i].src == src &&
                    graph->edge_list[i].dest == dest) {
                    return true;
                }
                if (!(graph->type & GRAPH_DIRECTED) &&
                    graph->edge_list[i].src == dest &&
                    graph->edge_list[i].dest == src) {
                    return true;
                }
            }
            return false;
    }

    return false;
}

double graph_get_edge_weight(const graph_t* graph, size_t src, size_t dest) {
    if (!graph || src >= graph->num_vertices || dest >= graph->num_vertices) {
        return INFINITY;
    }

    switch (graph->repr) {
        case GRAPH_ADJ_MATRIX:
            return graph->adj_matrix[src][dest];

        case GRAPH_ADJ_LIST: {
            adj_node_t* current = graph->adj_lists[src].head;
            while (current) {
                if (current->vertex == dest) return current->weight;
                current = current->next;
            }
            return INFINITY;
        }

        case GRAPH_EDGE_LIST:
            for (size_t i = 0; i < graph->num_edges; i++) {
                if (graph->edge_list[i].src == src &&
                    graph->edge_list[i].dest == dest) {
                    return graph->edge_list[i].weight;
                }
            }
            return INFINITY;
    }

    return INFINITY;
}

size_t graph_num_vertices(const graph_t* graph) {
    return graph ? graph->num_vertices : 0;
}

size_t graph_num_edges(const graph_t* graph) {
    return graph ? graph->num_edges : 0;
}

/* =========================== */
/*      Graph Traversal        */
/* =========================== */

void graph_bfs(const graph_t* graph, size_t start,
               void (*visit)(size_t vertex, void* data), void* data) {
    if (!graph || start >= graph->num_vertices || !visit) return;

    bool* visited = calloc(graph->num_vertices, sizeof(bool));
    size_t* queue = malloc(graph->num_vertices * sizeof(size_t));
    size_t front = 0, rear = 0;

    visited[start] = true;
    queue[rear++] = start;

    while (front < rear) {
        size_t vertex = queue[front++];
        visit(vertex, data);

        /* Visit all adjacent vertices */
        switch (graph->repr) {
            case GRAPH_ADJ_MATRIX:
                for (size_t i = 0; i < graph->num_vertices; i++) {
                    if (!visited[i] && graph_has_edge(graph, vertex, i)) {
                        visited[i] = true;
                        queue[rear++] = i;
                    }
                }
                break;

            case GRAPH_ADJ_LIST: {
                adj_node_t* current = graph->adj_lists[vertex].head;
                while (current) {
                    if (!visited[current->vertex]) {
                        visited[current->vertex] = true;
                        queue[rear++] = current->vertex;
                    }
                    current = current->next;
                }
                break;
            }

            case GRAPH_EDGE_LIST:
                for (size_t i = 0; i < graph->num_edges; i++) {
                    if (graph->edge_list[i].src == vertex) {
                        size_t dest = graph->edge_list[i].dest;
                        if (!visited[dest]) {
                            visited[dest] = true;
                            queue[rear++] = dest;
                        }
                    }
                }
                break;
        }
    }

    free(visited);
    free(queue);
}

static void dfs_recursive(const graph_t* graph, size_t vertex, bool* visited,
                          void (*visit)(size_t, void*), void* data) {
    visited[vertex] = true;
    visit(vertex, data);

    switch (graph->repr) {
        case GRAPH_ADJ_MATRIX:
            for (size_t i = 0; i < graph->num_vertices; i++) {
                if (!visited[i] && graph_has_edge(graph, vertex, i)) {
                    dfs_recursive(graph, i, visited, visit, data);
                }
            }
            break;

        case GRAPH_ADJ_LIST: {
            adj_node_t* current = graph->adj_lists[vertex].head;
            while (current) {
                if (!visited[current->vertex]) {
                    dfs_recursive(graph, current->vertex, visited, visit, data);
                }
                current = current->next;
            }
            break;
        }

        case GRAPH_EDGE_LIST:
            for (size_t i = 0; i < graph->num_edges; i++) {
                if (graph->edge_list[i].src == vertex) {
                    size_t dest = graph->edge_list[i].dest;
                    if (!visited[dest]) {
                        dfs_recursive(graph, dest, visited, visit, data);
                    }
                }
            }
            break;
    }
}

void graph_dfs(const graph_t* graph, size_t start,
               void (*visit)(size_t vertex, void* data), void* data) {
    if (!graph || start >= graph->num_vertices || !visit) return;

    bool* visited = calloc(graph->num_vertices, sizeof(bool));
    dfs_recursive(graph, start, visited, visit, data);
    free(visited);
}

/* =========================== */
/*     Shortest Path Algos     */
/* =========================== */

/* Min heap for Dijkstra */
typedef struct {
    size_t vertex;
    double distance;
} heap_node_t;

typedef struct {
    heap_node_t* nodes;
    size_t* positions;
    size_t size;
    size_t capacity;
} min_heap_t;

static min_heap_t* heap_create(size_t capacity) {
    min_heap_t* heap = malloc(sizeof(min_heap_t));
    heap->nodes = malloc(capacity * sizeof(heap_node_t));
    heap->positions = malloc(capacity * sizeof(size_t));
    heap->size = 0;
    heap->capacity = capacity;
    return heap;
}

static void heap_destroy(min_heap_t* heap) {
    free(heap->nodes);
    free(heap->positions);
    free(heap);
}

static void heap_swap(min_heap_t* heap, size_t i, size_t j) {
    heap->positions[heap->nodes[i].vertex] = j;
    heap->positions[heap->nodes[j].vertex] = i;

    heap_node_t temp = heap->nodes[i];
    heap->nodes[i] = heap->nodes[j];
    heap->nodes[j] = temp;
}

static void heap_decrease_key(min_heap_t* heap, size_t vertex, double distance) {
    size_t i = heap->positions[vertex];
    heap->nodes[i].distance = distance;

    /* Bubble up */
    while (i > 0 && heap->nodes[i].distance < heap->nodes[(i - 1) / 2].distance) {
        heap_swap(heap, i, (i - 1) / 2);
        i = (i - 1) / 2;
    }
}

static heap_node_t heap_extract_min(min_heap_t* heap) {
    heap_node_t min = heap->nodes[0];

    heap->nodes[0] = heap->nodes[heap->size - 1];
    heap->positions[heap->nodes[0].vertex] = 0;
    heap->size--;

    /* Bubble down */
    size_t i = 0;
    while (2 * i + 1 < heap->size) {
        size_t smallest = i;
        size_t left = 2 * i + 1;
        size_t right = 2 * i + 2;

        if (left < heap->size && heap->nodes[left].distance < heap->nodes[smallest].distance) {
            smallest = left;
        }
        if (right < heap->size && heap->nodes[right].distance < heap->nodes[smallest].distance) {
            smallest = right;
        }

        if (smallest != i) {
            heap_swap(heap, i, smallest);
            i = smallest;
        } else {
            break;
        }
    }

    return min;
}

double* graph_dijkstra(const graph_t* graph, size_t src, size_t* predecessors) {
    if (!graph || src >= graph->num_vertices) return NULL;

    size_t n = graph->num_vertices;
    double* distances = malloc(n * sizeof(double));
    bool* visited = calloc(n, sizeof(bool));

    if (predecessors) {
        for (size_t i = 0; i < n; i++) {
            predecessors[i] = SIZE_MAX;
        }
    }

    /* Initialize distances */
    for (size_t i = 0; i < n; i++) {
        distances[i] = INFINITY;
    }
    distances[src] = 0.0;

    /* Create min heap */
    min_heap_t* heap = heap_create(n);
    for (size_t i = 0; i < n; i++) {
        heap->nodes[i].vertex = i;
        heap->nodes[i].distance = distances[i];
        heap->positions[i] = i;
    }
    heap->size = n;

    while (heap->size > 0) {
        heap_node_t min_node = heap_extract_min(heap);
        size_t u = min_node.vertex;

        if (isinf(distances[u])) break;

        visited[u] = true;

        /* Update distances to neighbors */
        switch (graph->repr) {
            case GRAPH_ADJ_MATRIX:
                for (size_t v = 0; v < n; v++) {
                    if (!visited[v]) {
                        double weight = graph->adj_matrix[u][v];
                        if (!isinf(weight) && distances[u] + weight < distances[v]) {
                            distances[v] = distances[u] + weight;
                            if (predecessors) predecessors[v] = u;
                            heap_decrease_key(heap, v, distances[v]);
                        }
                    }
                }
                break;

            case GRAPH_ADJ_LIST: {
                adj_node_t* current = graph->adj_lists[u].head;
                while (current) {
                    size_t v = current->vertex;
                    if (!visited[v]) {
                        double weight = current->weight;
                        if (distances[u] + weight < distances[v]) {
                            distances[v] = distances[u] + weight;
                            if (predecessors) predecessors[v] = u;
                            heap_decrease_key(heap, v, distances[v]);
                        }
                    }
                    current = current->next;
                }
                break;
            }

            case GRAPH_EDGE_LIST:
                for (size_t i = 0; i < graph->num_edges; i++) {
                    if (graph->edge_list[i].src == u) {
                        size_t v = graph->edge_list[i].dest;
                        if (!visited[v]) {
                            double weight = graph->edge_list[i].weight;
                            if (distances[u] + weight < distances[v]) {
                                distances[v] = distances[u] + weight;
                                if (predecessors) predecessors[v] = u;
                                heap_decrease_key(heap, v, distances[v]);
                            }
                        }
                    }
                }
                break;
        }
    }

    heap_destroy(heap);
    free(visited);
    return distances;
}

double** graph_floyd_warshall(const graph_t* graph, size_t** next) {
    if (!graph) return NULL;

    size_t n = graph->num_vertices;

    /* Allocate distance matrix */
    double** dist = malloc(n * sizeof(double*));
    for (size_t i = 0; i < n; i++) {
        dist[i] = malloc(n * sizeof(double));
        for (size_t j = 0; j < n; j++) {
            if (i == j) {
                dist[i][j] = 0;
            } else {
                dist[i][j] = graph_get_edge_weight(graph, i, j);
            }
        }
    }

    /* Allocate next matrix if requested */
    if (next) {
        *next = malloc(n * sizeof(size_t*));
        for (size_t i = 0; i < n; i++) {
            (*next)[i] = malloc(n * sizeof(size_t));
            for (size_t j = 0; j < n; j++) {
                if (!isinf(dist[i][j]) && i != j) {
                    (*next)[i][j] = j;
                } else {
                    (*next)[i][j] = SIZE_MAX;
                }
            }
        }
    }

    /* Floyd-Warshall algorithm */
    for (size_t k = 0; k < n; k++) {
        for (size_t i = 0; i < n; i++) {
            for (size_t j = 0; j < n; j++) {
                if (!isinf(dist[i][k]) && !isinf(dist[k][j])) {
                    if (dist[i][k] + dist[k][j] < dist[i][j]) {
                        dist[i][j] = dist[i][k] + dist[k][j];
                        if (next) {
                            (*next)[i][j] = (*next)[i][k];
                        }
                    }
                }
            }
        }
    }

    return dist;
}

bool graph_bellman_ford(const graph_t* graph, size_t src,
                        double* distances, size_t* predecessors) {
    if (!graph || src >= graph->num_vertices || !distances) return false;

    size_t n = graph->num_vertices;

    /* Initialize distances */
    for (size_t i = 0; i < n; i++) {
        distances[i] = INFINITY;
        if (predecessors) predecessors[i] = SIZE_MAX;
    }
    distances[src] = 0;

    /* Relax edges n-1 times */
    for (size_t i = 0; i < n - 1; i++) {
        bool updated = false;

        /* Iterate through all edges */
        for (size_t u = 0; u < n; u++) {
            if (isinf(distances[u])) continue;

            switch (graph->repr) {
                case GRAPH_ADJ_MATRIX:
                    for (size_t v = 0; v < n; v++) {
                        double weight = graph->adj_matrix[u][v];
                        if (!isinf(weight) && distances[u] + weight < distances[v]) {
                            distances[v] = distances[u] + weight;
                            if (predecessors) predecessors[v] = u;
                            updated = true;
                        }
                    }
                    break;

                case GRAPH_ADJ_LIST: {
                    adj_node_t* current = graph->adj_lists[u].head;
                    while (current) {
                        size_t v = current->vertex;
                        double weight = current->weight;
                        if (distances[u] + weight < distances[v]) {
                            distances[v] = distances[u] + weight;
                            if (predecessors) predecessors[v] = u;
                            updated = true;
                        }
                        current = current->next;
                    }
                    break;
                }

                case GRAPH_EDGE_LIST:
                    /* This is more efficient for edge list */
                    break;
            }
        }

        /* For edge list representation */
        if (graph->repr == GRAPH_EDGE_LIST) {
            for (size_t j = 0; j < graph->num_edges; j++) {
                size_t u = graph->edge_list[j].src;
                size_t v = graph->edge_list[j].dest;
                double weight = graph->edge_list[j].weight;

                if (!isinf(distances[u]) && distances[u] + weight < distances[v]) {
                    distances[v] = distances[u] + weight;
                    if (predecessors) predecessors[v] = u;
                    updated = true;
                }
            }
        }

        if (!updated) break;
    }

    /* Check for negative cycles */
    for (size_t u = 0; u < n; u++) {
        if (isinf(distances[u])) continue;

        switch (graph->repr) {
            case GRAPH_ADJ_MATRIX:
            case GRAPH_ADJ_LIST:
                for (size_t v = 0; v < n; v++) {
                    double weight = graph_get_edge_weight(graph, u, v);
                    if (!isinf(weight) && distances[u] + weight < distances[v]) {
                        return false;  /* Negative cycle detected */
                    }
                }
                break;

            case GRAPH_EDGE_LIST:
                /* Handled below */
                break;
        }
    }

    if (graph->repr == GRAPH_EDGE_LIST) {
        for (size_t j = 0; j < graph->num_edges; j++) {
            size_t u = graph->edge_list[j].src;
            size_t v = graph->edge_list[j].dest;
            double weight = graph->edge_list[j].weight;

            if (!isinf(distances[u]) && distances[u] + weight < distances[v]) {
                return false;  /* Negative cycle detected */
            }
        }
    }

    return true;  /* No negative cycle */
}

/* =========================== */
/*   Minimum Spanning Tree     */
/* =========================== */

/* Disjoint Set Union for Kruskal's algorithm */
typedef struct {
    size_t* parent;
    size_t* rank;
    size_t size;
} dsu_t;

static dsu_t* dsu_create(size_t n) {
    dsu_t* dsu = malloc(sizeof(dsu_t));
    dsu->parent = malloc(n * sizeof(size_t));
    dsu->rank = calloc(n, sizeof(size_t));
    dsu->size = n;

    for (size_t i = 0; i < n; i++) {
        dsu->parent[i] = i;
    }

    return dsu;
}

static void dsu_destroy(dsu_t* dsu) {
    free(dsu->parent);
    free(dsu->rank);
    free(dsu);
}

static size_t dsu_find(dsu_t* dsu, size_t x) {
    if (dsu->parent[x] != x) {
        dsu->parent[x] = dsu_find(dsu, dsu->parent[x]);  /* Path compression */
    }
    return dsu->parent[x];
}

static bool dsu_union(dsu_t* dsu, size_t x, size_t y) {
    size_t root_x = dsu_find(dsu, x);
    size_t root_y = dsu_find(dsu, y);

    if (root_x == root_y) return false;

    /* Union by rank */
    if (dsu->rank[root_x] < dsu->rank[root_y]) {
        dsu->parent[root_x] = root_y;
    } else if (dsu->rank[root_x] > dsu->rank[root_y]) {
        dsu->parent[root_y] = root_x;
    } else {
        dsu->parent[root_y] = root_x;
        dsu->rank[root_x]++;
    }

    return true;
}

static int edge_compare(const void* a, const void* b) {
    edge_t* edge_a = (edge_t*)a;
    edge_t* edge_b = (edge_t*)b;

    if (edge_a->weight < edge_b->weight) return -1;
    if (edge_a->weight > edge_b->weight) return 1;
    return 0;
}

edge_t* graph_kruskal_mst(const graph_t* graph, size_t* num_edges, double* total_weight) {
    if (!graph || !num_edges) return NULL;

    size_t n = graph->num_vertices;
    *num_edges = 0;
    if (total_weight) *total_weight = 0;

    /* Collect all edges */
    edge_t* all_edges = malloc(graph->num_edges * 2 * sizeof(edge_t));
    size_t edge_count = 0;

    switch (graph->repr) {
        case GRAPH_ADJ_MATRIX:
            for (size_t i = 0; i < n; i++) {
                for (size_t j = (graph->type & GRAPH_DIRECTED) ? 0 : i + 1; j < n; j++) {
                    if (!isinf(graph->adj_matrix[i][j]) && graph->adj_matrix[i][j] != 0) {
                        all_edges[edge_count].src = i;
                        all_edges[edge_count].dest = j;
                        all_edges[edge_count].weight = graph->adj_matrix[i][j];
                        all_edges[edge_count].data = NULL;
                        edge_count++;
                    }
                }
            }
            break;

        case GRAPH_ADJ_LIST:
            for (size_t i = 0; i < n; i++) {
                adj_node_t* current = graph->adj_lists[i].head;
                while (current) {
                    if (!(graph->type & GRAPH_DIRECTED) && i > current->vertex) {
                        current = current->next;
                        continue;  /* Avoid duplicates for undirected graphs */
                    }
                    all_edges[edge_count].src = i;
                    all_edges[edge_count].dest = current->vertex;
                    all_edges[edge_count].weight = current->weight;
                    all_edges[edge_count].data = NULL;
                    edge_count++;
                    current = current->next;
                }
            }
            break;

        case GRAPH_EDGE_LIST:
            memcpy(all_edges, graph->edge_list, graph->num_edges * sizeof(edge_t));
            edge_count = graph->num_edges;
            break;
    }

    /* Sort edges by weight */
    qsort(all_edges, edge_count, sizeof(edge_t), edge_compare);

    /* Kruskal's algorithm */
    edge_t* mst = malloc((n - 1) * sizeof(edge_t));
    dsu_t* dsu = dsu_create(n);

    for (size_t i = 0; i < edge_count && *num_edges < n - 1; i++) {
        if (dsu_union(dsu, all_edges[i].src, all_edges[i].dest)) {
            mst[(*num_edges)++] = all_edges[i];
            if (total_weight) *total_weight += all_edges[i].weight;
        }
    }

    dsu_destroy(dsu);
    free(all_edges);

    return mst;
}

edge_t* graph_prim_mst(const graph_t* graph, size_t* num_edges, double* total_weight) {
    if (!graph || !num_edges) return NULL;

    size_t n = graph->num_vertices;
    *num_edges = 0;
    if (total_weight) *total_weight = 0;

    if (n == 0) return NULL;

    edge_t* mst = malloc((n - 1) * sizeof(edge_t));
    bool* in_mst = calloc(n, sizeof(bool));
    double* key = malloc(n * sizeof(double));
    size_t* parent = malloc(n * sizeof(size_t));

    /* Initialize keys and parent */
    for (size_t i = 0; i < n; i++) {
        key[i] = INFINITY;
        parent[i] = SIZE_MAX;
    }

    /* Start from vertex 0 */
    key[0] = 0;

    for (size_t count = 0; count < n; count++) {
        /* Find minimum key vertex not in MST */
        size_t u = SIZE_MAX;
        double min_key = INFINITY;

        for (size_t v = 0; v < n; v++) {
            if (!in_mst[v] && key[v] < min_key) {
                min_key = key[v];
                u = v;
            }
        }

        if (u == SIZE_MAX) break;  /* No more connected vertices */

        in_mst[u] = true;

        /* Add edge to MST if not the starting vertex */
        if (parent[u] != SIZE_MAX) {
            mst[*num_edges].src = parent[u];
            mst[*num_edges].dest = u;
            mst[*num_edges].weight = key[u];
            mst[*num_edges].data = NULL;
            (*num_edges)++;
            if (total_weight) *total_weight += key[u];
        }

        /* Update key values of adjacent vertices */
        switch (graph->repr) {
            case GRAPH_ADJ_MATRIX:
                for (size_t v = 0; v < n; v++) {
                    double weight = graph->adj_matrix[u][v];
                    if (!in_mst[v] && !isinf(weight) && weight < key[v]) {
                        key[v] = weight;
                        parent[v] = u;
                    }
                }
                break;

            case GRAPH_ADJ_LIST: {
                adj_node_t* current = graph->adj_lists[u].head;
                while (current) {
                    size_t v = current->vertex;
                    double weight = current->weight;
                    if (!in_mst[v] && weight < key[v]) {
                        key[v] = weight;
                        parent[v] = u;
                    }
                    current = current->next;
                }
                break;
            }

            case GRAPH_EDGE_LIST:
                for (size_t i = 0; i < graph->num_edges; i++) {
                    if (graph->edge_list[i].src == u) {
                        size_t v = graph->edge_list[i].dest;
                        double weight = graph->edge_list[i].weight;
                        if (!in_mst[v] && weight < key[v]) {
                            key[v] = weight;
                            parent[v] = u;
                        }
                    } else if (!(graph->type & GRAPH_DIRECTED) &&
                               graph->edge_list[i].dest == u) {
                        size_t v = graph->edge_list[i].src;
                        double weight = graph->edge_list[i].weight;
                        if (!in_mst[v] && weight < key[v]) {
                            key[v] = weight;
                            parent[v] = u;
                        }
                    }
                }
                break;
        }
    }

    free(in_mst);
    free(key);
    free(parent);

    return mst;
}

/* =========================== */
/*     Graph Properties        */
/* =========================== */

bool graph_is_connected(const graph_t* graph) {
    if (!graph || graph->num_vertices == 0) return true;

    bool* visited = calloc(graph->num_vertices, sizeof(bool));
    size_t count = 0;

    /* Count vertices reachable from vertex 0 */
    void count_vertex(size_t vertex, void* data) {
        (*(size_t*)data)++;
    }

    graph_dfs(graph, 0, count_vertex, &count);
    free(visited);

    return count == graph->num_vertices;
}

bool graph_has_cycle(const graph_t* graph) {
    if (!graph) return false;

    size_t n = graph->num_vertices;
    bool* visited = calloc(n, sizeof(bool));
    bool* rec_stack = calloc(n, sizeof(bool));
    bool has_cycle = false;

    /* Helper function for DFS cycle detection */
    bool dfs_cycle(size_t v) {
        visited[v] = true;
        rec_stack[v] = true;

        switch (graph->repr) {
            case GRAPH_ADJ_MATRIX:
                for (size_t i = 0; i < n; i++) {
                    if (graph_has_edge(graph, v, i)) {
                        if (!visited[i]) {
                            if (dfs_cycle(i)) return true;
                        } else if (rec_stack[i]) {
                            return true;
                        }
                    }
                }
                break;

            case GRAPH_ADJ_LIST: {
                adj_node_t* current = graph->adj_lists[v].head;
                while (current) {
                    if (!visited[current->vertex]) {
                        if (dfs_cycle(current->vertex)) return true;
                    } else if (rec_stack[current->vertex]) {
                        return true;
                    }
                    current = current->next;
                }
                break;
            }

            case GRAPH_EDGE_LIST:
                for (size_t i = 0; i < graph->num_edges; i++) {
                    if (graph->edge_list[i].src == v) {
                        size_t dest = graph->edge_list[i].dest;
                        if (!visited[dest]) {
                            if (dfs_cycle(dest)) return true;
                        } else if (rec_stack[dest]) {
                            return true;
                        }
                    }
                }
                break;
        }

        rec_stack[v] = false;
        return false;
    }

    /* Check all components */
    for (size_t i = 0; i < n; i++) {
        if (!visited[i]) {
            if (dfs_cycle(i)) {
                has_cycle = true;
                break;
            }
        }
    }

    free(visited);
    free(rec_stack);
    return has_cycle;
}

/* =========================== */
/*      Topological Sort       */
/* =========================== */

size_t* graph_topological_sort(const graph_t* graph, bool* has_cycle) {
    if (!graph) return NULL;

    size_t n = graph->num_vertices;
    size_t* in_degree = calloc(n, sizeof(size_t));
    size_t* result = malloc(n * sizeof(size_t));
    size_t result_count = 0;

    /* Calculate in-degrees */
    for (size_t u = 0; u < n; u++) {
        switch (graph->repr) {
            case GRAPH_ADJ_MATRIX:
                for (size_t v = 0; v < n; v++) {
                    if (graph_has_edge(graph, u, v)) {
                        in_degree[v]++;
                    }
                }
                break;

            case GRAPH_ADJ_LIST: {
                adj_node_t* current = graph->adj_lists[u].head;
                while (current) {
                    in_degree[current->vertex]++;
                    current = current->next;
                }
                break;
            }

            case GRAPH_EDGE_LIST:
                for (size_t i = 0; i < graph->num_edges; i++) {
                    if (graph->edge_list[i].src == u) {
                        in_degree[graph->edge_list[i].dest]++;
                    }
                }
                break;
        }
    }

    /* Create queue of vertices with in-degree 0 */
    size_t* queue = malloc(n * sizeof(size_t));
    size_t front = 0, rear = 0;

    for (size_t i = 0; i < n; i++) {
        if (in_degree[i] == 0) {
            queue[rear++] = i;
        }
    }

    /* Process vertices */
    while (front < rear) {
        size_t u = queue[front++];
        result[result_count++] = u;

        /* Decrease in-degree of neighbors */
        switch (graph->repr) {
            case GRAPH_ADJ_MATRIX:
                for (size_t v = 0; v < n; v++) {
                    if (graph_has_edge(graph, u, v)) {
                        in_degree[v]--;
                        if (in_degree[v] == 0) {
                            queue[rear++] = v;
                        }
                    }
                }
                break;

            case GRAPH_ADJ_LIST: {
                adj_node_t* current = graph->adj_lists[u].head;
                while (current) {
                    in_degree[current->vertex]--;
                    if (in_degree[current->vertex] == 0) {
                        queue[rear++] = current->vertex;
                    }
                    current = current->next;
                }
                break;
            }

            case GRAPH_EDGE_LIST:
                for (size_t i = 0; i < graph->num_edges; i++) {
                    if (graph->edge_list[i].src == u) {
                        size_t v = graph->edge_list[i].dest;
                        in_degree[v]--;
                        if (in_degree[v] == 0) {
                            queue[rear++] = v;
                        }
                    }
                }
                break;
        }
    }

    free(queue);
    free(in_degree);

    if (has_cycle) {
        *has_cycle = (result_count != n);
    }

    if (result_count != n) {
        free(result);
        return NULL;
    }

    return result;
}

/* =========================== */
/*      Graph Generation       */
/* =========================== */

graph_t* graph_generate_complete(size_t n) {
    graph_t* graph = graph_create(n, GRAPH_UNDIRECTED, GRAPH_ADJ_MATRIX);
    if (!graph) return NULL;

    for (size_t i = 0; i < n; i++) {
        for (size_t j = i + 1; j < n; j++) {
            graph_add_edge(graph, i, j, 1.0);
        }
    }

    return graph;
}

graph_t* graph_generate_cycle(size_t n) {
    if (n < 3) return NULL;

    graph_t* graph = graph_create(n, GRAPH_UNDIRECTED, GRAPH_ADJ_LIST);
    if (!graph) return NULL;

    for (size_t i = 0; i < n; i++) {
        graph_add_edge(graph, i, (i + 1) % n, 1.0);
    }

    return graph;
}

graph_t* graph_generate_path(size_t n) {
    if (n == 0) return NULL;

    graph_t* graph = graph_create(n, GRAPH_UNDIRECTED, GRAPH_ADJ_LIST);
    if (!graph) return NULL;

    for (size_t i = 0; i < n - 1; i++) {
        graph_add_edge(graph, i, i + 1, 1.0);
    }

    return graph;
}

graph_t* graph_generate_random(size_t n, double edge_probability) {
    graph_t* graph = graph_create(n, GRAPH_UNDIRECTED, GRAPH_ADJ_MATRIX);
    if (!graph) return NULL;

    for (size_t i = 0; i < n; i++) {
        for (size_t j = i + 1; j < n; j++) {
            if ((double)rand() / RAND_MAX < edge_probability) {
                graph_add_edge(graph, i, j, 1.0);
            }
        }
    }

    return graph;
}

/* =========================== */
/*         Graph I/O           */
/* =========================== */

void graph_print(const graph_t* graph) {
    if (!graph) {
        printf("Graph is NULL\n");
        return;
    }

    printf("Graph: %zu vertices, %zu edges\n", graph->num_vertices, graph->num_edges);
    printf("Type: %s %s\n",
           (graph->type & GRAPH_DIRECTED) ? "Directed" : "Undirected",
           (graph->type & GRAPH_WEIGHTED) ? "Weighted" : "Unweighted");

    switch (graph->repr) {
        case GRAPH_ADJ_MATRIX:
            printf("Adjacency Matrix:\n");
            for (size_t i = 0; i < graph->num_vertices; i++) {
                for (size_t j = 0; j < graph->num_vertices; j++) {
                    if (isinf(graph->adj_matrix[i][j])) {
                        printf("  ∞ ");
                    } else {
                        printf("%3.0f ", graph->adj_matrix[i][j]);
                    }
                }
                printf("\n");
            }
            break;

        case GRAPH_ADJ_LIST:
            printf("Adjacency List:\n");
            for (size_t i = 0; i < graph->num_vertices; i++) {
                printf("%zu: ", i);
                adj_node_t* current = graph->adj_lists[i].head;
                while (current) {
                    printf("(%zu, %.1f) ", current->vertex, current->weight);
                    current = current->next;
                }
                printf("\n");
            }
            break;

        case GRAPH_EDGE_LIST:
            printf("Edge List:\n");
            for (size_t i = 0; i < graph->num_edges; i++) {
                printf("(%zu, %zu, %.1f)\n",
                       graph->edge_list[i].src,
                       graph->edge_list[i].dest,
                       graph->edge_list[i].weight);
            }
            break;
    }
}