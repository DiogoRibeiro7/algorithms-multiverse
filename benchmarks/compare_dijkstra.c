/**
 * Dijkstra's Algorithm Performance Comparison
 *
 * Compares Binary Heap vs Fibonacci Heap implementations
 * Includes statistical analysis and CSV output for visualization
 *
 * Compile: gcc -O3 -o compare_dijkstra compare_dijkstra.c -lm
 * Run: ./compare_dijkstra
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <stdbool.h>
#include <limits.h>
#include <float.h>

#define MAX_VERTICES 10000
#define INF INT_MAX
#define NUM_TRIALS 10

// ============================================================================
// DATA STRUCTURES
// ============================================================================

typedef struct Edge {
    int dest;
    int weight;
    struct Edge* next;
} Edge;

typedef struct Graph {
    int num_vertices;
    int num_edges;
    Edge** adj_list;
} Graph;

// Binary Heap Node
typedef struct BinaryHeapNode {
    int vertex;
    int distance;
} BinaryHeapNode;

// Binary Heap
typedef struct BinaryHeap {
    BinaryHeapNode* nodes;
    int* positions;  // Position of vertex in heap
    int size;
    int capacity;
} BinaryHeap;

// Fibonacci Heap Node
typedef struct FibNode {
    int vertex;
    int distance;
    int degree;
    bool marked;
    struct FibNode* parent;
    struct FibNode* child;
    struct FibNode* left;
    struct FibNode* right;
} FibNode;

// Fibonacci Heap
typedef struct FibHeap {
    FibNode* min;
    int num_nodes;
    FibNode** node_map;  // Map vertex to node
} FibHeap;

// Statistics Structure
typedef struct Statistics {
    double mean;
    double std_dev;
    double median;
    double min;
    double max;
    double conf_interval_lower;
    double conf_interval_upper;
} Statistics;

// Benchmark Result
typedef struct BenchmarkResult {
    char heap_type[20];
    int num_vertices;
    int num_edges;
    double execution_times[NUM_TRIALS];
    Statistics stats;
    long heap_operations;
    long decrease_key_ops;
} BenchmarkResult;

// ============================================================================
// GRAPH OPERATIONS
// ============================================================================

Graph* create_graph(int num_vertices) {
    Graph* graph = (Graph*)malloc(sizeof(Graph));
    graph->num_vertices = num_vertices;
    graph->num_edges = 0;
    graph->adj_list = (Edge**)calloc(num_vertices, sizeof(Edge*));
    return graph;
}

void add_edge(Graph* graph, int src, int dest, int weight) {
    Edge* edge = (Edge*)malloc(sizeof(Edge));
    edge->dest = dest;
    edge->weight = weight;
    edge->next = graph->adj_list[src];
    graph->adj_list[src] = edge;
    graph->num_edges++;
}

void free_graph(Graph* graph) {
    for (int i = 0; i < graph->num_vertices; i++) {
        Edge* edge = graph->adj_list[i];
        while (edge) {
            Edge* temp = edge;
            edge = edge->next;
            free(temp);
        }
    }
    free(graph->adj_list);
    free(graph);
}

// Generate random dense graph
Graph* generate_dense_graph(int num_vertices, double density) {
    Graph* graph = create_graph(num_vertices);

    for (int i = 0; i < num_vertices; i++) {
        for (int j = 0; j < num_vertices; j++) {
            if (i != j && (double)rand() / RAND_MAX < density) {
                int weight = rand() % 100 + 1;
                add_edge(graph, i, j, weight);
            }
        }
    }

    return graph;
}

// Generate sparse graph (grid-like)
Graph* generate_sparse_graph(int num_vertices) {
    Graph* graph = create_graph(num_vertices);
    int grid_size = (int)sqrt(num_vertices);

    for (int i = 0; i < grid_size; i++) {
        for (int j = 0; j < grid_size; j++) {
            int v = i * grid_size + j;

            // Right neighbor
            if (j < grid_size - 1) {
                int weight = rand() % 100 + 1;
                add_edge(graph, v, v + 1, weight);
            }

            // Bottom neighbor
            if (i < grid_size - 1) {
                int weight = rand() % 100 + 1;
                add_edge(graph, v, v + grid_size, weight);
            }

            // Diagonal
            if (i < grid_size - 1 && j < grid_size - 1) {
                int weight = rand() % 100 + 1;
                add_edge(graph, v, v + grid_size + 1, weight);
            }
        }
    }

    return graph;
}

// ============================================================================
// BINARY HEAP IMPLEMENTATION
// ============================================================================

BinaryHeap* create_binary_heap(int capacity) {
    BinaryHeap* heap = (BinaryHeap*)malloc(sizeof(BinaryHeap));
    heap->nodes = (BinaryHeapNode*)malloc(capacity * sizeof(BinaryHeapNode));
    heap->positions = (int*)malloc(capacity * sizeof(int));
    heap->size = 0;
    heap->capacity = capacity;

    for (int i = 0; i < capacity; i++) {
        heap->positions[i] = -1;
    }

    return heap;
}

void swap_nodes(BinaryHeap* heap, int i, int j) {
    BinaryHeapNode temp = heap->nodes[i];
    heap->nodes[i] = heap->nodes[j];
    heap->nodes[j] = temp;

    // Update positions
    heap->positions[heap->nodes[i].vertex] = i;
    heap->positions[heap->nodes[j].vertex] = j;
}

void heapify_up(BinaryHeap* heap, int idx) {
    while (idx > 0) {
        int parent = (idx - 1) / 2;
        if (heap->nodes[idx].distance < heap->nodes[parent].distance) {
            swap_nodes(heap, idx, parent);
            idx = parent;
        } else {
            break;
        }
    }
}

void heapify_down(BinaryHeap* heap, int idx) {
    while (true) {
        int smallest = idx;
        int left = 2 * idx + 1;
        int right = 2 * idx + 2;

        if (left < heap->size &&
            heap->nodes[left].distance < heap->nodes[smallest].distance) {
            smallest = left;
        }

        if (right < heap->size &&
            heap->nodes[right].distance < heap->nodes[smallest].distance) {
            smallest = right;
        }

        if (smallest != idx) {
            swap_nodes(heap, idx, smallest);
            idx = smallest;
        } else {
            break;
        }
    }
}

void binary_heap_insert(BinaryHeap* heap, int vertex, int distance) {
    int idx = heap->size++;
    heap->nodes[idx].vertex = vertex;
    heap->nodes[idx].distance = distance;
    heap->positions[vertex] = idx;
    heapify_up(heap, idx);
}

BinaryHeapNode binary_heap_extract_min(BinaryHeap* heap) {
    BinaryHeapNode min = heap->nodes[0];
    heap->positions[min.vertex] = -1;

    heap->nodes[0] = heap->nodes[--heap->size];
    if (heap->size > 0) {
        heap->positions[heap->nodes[0].vertex] = 0;
        heapify_down(heap, 0);
    }

    return min;
}

void binary_heap_decrease_key(BinaryHeap* heap, int vertex, int new_distance) {
    int idx = heap->positions[vertex];
    if (idx == -1) return;

    heap->nodes[idx].distance = new_distance;
    heapify_up(heap, idx);
}

bool binary_heap_is_empty(BinaryHeap* heap) {
    return heap->size == 0;
}

void free_binary_heap(BinaryHeap* heap) {
    free(heap->nodes);
    free(heap->positions);
    free(heap);
}

// ============================================================================
// FIBONACCI HEAP IMPLEMENTATION
// ============================================================================

FibHeap* create_fib_heap(int capacity) {
    FibHeap* heap = (FibHeap*)malloc(sizeof(FibHeap));
    heap->min = NULL;
    heap->num_nodes = 0;
    heap->node_map = (FibNode**)calloc(capacity, sizeof(FibNode*));
    return heap;
}

FibNode* create_fib_node(int vertex, int distance) {
    FibNode* node = (FibNode*)malloc(sizeof(FibNode));
    node->vertex = vertex;
    node->distance = distance;
    node->degree = 0;
    node->marked = false;
    node->parent = NULL;
    node->child = NULL;
    node->left = node;
    node->right = node;
    return node;
}

void fib_heap_link(FibHeap* heap, FibNode* y, FibNode* x) {
    // Remove y from root list
    y->left->right = y->right;
    y->right->left = y->left;

    // Make y a child of x
    y->parent = x;

    if (x->child == NULL) {
        x->child = y;
        y->left = y;
        y->right = y;
    } else {
        y->left = x->child;
        y->right = x->child->right;
        x->child->right->left = y;
        x->child->right = y;
    }

    x->degree++;
    y->marked = false;
}

void fib_heap_consolidate(FibHeap* heap) {
    int max_degree = (int)(log(heap->num_nodes) / log(2)) + 1;
    FibNode** degree_table = (FibNode**)calloc(max_degree + 1, sizeof(FibNode*));

    // Create array of root nodes
    int num_roots = 0;
    FibNode* current = heap->min;
    if (current != NULL) {
        do {
            num_roots++;
            current = current->right;
        } while (current != heap->min);
    }

    FibNode** roots = (FibNode**)malloc(num_roots * sizeof(FibNode*));
    current = heap->min;
    for (int i = 0; i < num_roots; i++) {
        roots[i] = current;
        current = current->right;
    }

    // Consolidate
    for (int i = 0; i < num_roots; i++) {
        FibNode* x = roots[i];
        int degree = x->degree;

        while (degree_table[degree] != NULL) {
            FibNode* y = degree_table[degree];

            if (x->distance > y->distance) {
                FibNode* temp = x;
                x = y;
                y = temp;
            }

            fib_heap_link(heap, y, x);
            degree_table[degree] = NULL;
            degree++;
        }

        degree_table[degree] = x;
    }

    // Rebuild root list
    heap->min = NULL;
    for (int i = 0; i <= max_degree; i++) {
        if (degree_table[i] != NULL) {
            if (heap->min == NULL) {
                heap->min = degree_table[i];
                heap->min->left = heap->min;
                heap->min->right = heap->min;
            } else {
                degree_table[i]->left = heap->min;
                degree_table[i]->right = heap->min->right;
                heap->min->right->left = degree_table[i];
                heap->min->right = degree_table[i];

                if (degree_table[i]->distance < heap->min->distance) {
                    heap->min = degree_table[i];
                }
            }
        }
    }

    free(degree_table);
    free(roots);
}

void fib_heap_insert(FibHeap* heap, int vertex, int distance) {
    FibNode* node = create_fib_node(vertex, distance);
    heap->node_map[vertex] = node;

    if (heap->min == NULL) {
        heap->min = node;
    } else {
        // Insert into root list
        node->left = heap->min;
        node->right = heap->min->right;
        heap->min->right->left = node;
        heap->min->right = node;

        if (distance < heap->min->distance) {
            heap->min = node;
        }
    }

    heap->num_nodes++;
}

FibNode* fib_heap_extract_min(FibHeap* heap) {
    FibNode* min = heap->min;

    if (min != NULL) {
        // Add children to root list
        if (min->child != NULL) {
            FibNode* child = min->child;
            do {
                FibNode* next = child->right;

                // Insert child into root list
                child->left = heap->min;
                child->right = heap->min->right;
                heap->min->right->left = child;
                heap->min->right = child;

                child->parent = NULL;
                child = next;
            } while (child != min->child);
        }

        // Remove min from root list
        min->left->right = min->right;
        min->right->left = min->left;

        if (min == min->right) {
            heap->min = NULL;
        } else {
            heap->min = min->right;
            fib_heap_consolidate(heap);
        }

        heap->num_nodes--;
        heap->node_map[min->vertex] = NULL;
    }

    return min;
}

void fib_heap_cut(FibHeap* heap, FibNode* x, FibNode* y) {
    // Remove x from child list of y
    if (x->right == x) {
        y->child = NULL;
    } else {
        x->left->right = x->right;
        x->right->left = x->left;
        if (y->child == x) {
            y->child = x->right;
        }
    }

    y->degree--;

    // Add x to root list
    x->left = heap->min;
    x->right = heap->min->right;
    heap->min->right->left = x;
    heap->min->right = x;

    x->parent = NULL;
    x->marked = false;
}

void fib_heap_cascading_cut(FibHeap* heap, FibNode* y) {
    FibNode* z = y->parent;

    if (z != NULL) {
        if (!y->marked) {
            y->marked = true;
        } else {
            fib_heap_cut(heap, y, z);
            fib_heap_cascading_cut(heap, z);
        }
    }
}

void fib_heap_decrease_key(FibHeap* heap, int vertex, int new_distance) {
    FibNode* x = heap->node_map[vertex];
    if (x == NULL) return;

    x->distance = new_distance;
    FibNode* y = x->parent;

    if (y != NULL && x->distance < y->distance) {
        fib_heap_cut(heap, x, y);
        fib_heap_cascading_cut(heap, y);
    }

    if (x->distance < heap->min->distance) {
        heap->min = x;
    }
}

bool fib_heap_is_empty(FibHeap* heap) {
    return heap->min == NULL;
}

void free_fib_node(FibNode* node) {
    if (node == NULL) return;

    FibNode* current = node;
    do {
        FibNode* next = current->right;
        if (current->child != NULL) {
            free_fib_node(current->child);
        }
        free(current);
        current = next;
    } while (current != node);
}

void free_fib_heap(FibHeap* heap) {
    if (heap->min != NULL) {
        free_fib_node(heap->min);
    }
    free(heap->node_map);
    free(heap);
}

// ============================================================================
// DIJKSTRA'S ALGORITHM IMPLEMENTATIONS
// ============================================================================

long binary_heap_ops = 0;
long binary_decrease_key_ops = 0;
long fib_heap_ops = 0;
long fib_decrease_key_ops = 0;

void dijkstra_binary_heap(Graph* graph, int source, int* distances) {
    binary_heap_ops = 0;
    binary_decrease_key_ops = 0;

    BinaryHeap* heap = create_binary_heap(graph->num_vertices);
    bool* visited = (bool*)calloc(graph->num_vertices, sizeof(bool));

    // Initialize distances
    for (int i = 0; i < graph->num_vertices; i++) {
        distances[i] = INF;
    }
    distances[source] = 0;

    binary_heap_insert(heap, source, 0);
    binary_heap_ops++;

    while (!binary_heap_is_empty(heap)) {
        BinaryHeapNode min = binary_heap_extract_min(heap);
        binary_heap_ops++;

        int u = min.vertex;
        if (visited[u]) continue;
        visited[u] = true;

        // Process neighbors
        Edge* edge = graph->adj_list[u];
        while (edge != NULL) {
            int v = edge->dest;
            int weight = edge->weight;

            if (!visited[v] && distances[u] != INF) {
                int new_dist = distances[u] + weight;

                if (new_dist < distances[v]) {
                    distances[v] = new_dist;

                    if (heap->positions[v] == -1) {
                        binary_heap_insert(heap, v, new_dist);
                        binary_heap_ops++;
                    } else {
                        binary_heap_decrease_key(heap, v, new_dist);
                        binary_decrease_key_ops++;
                    }
                }
            }

            edge = edge->next;
        }
    }

    free(visited);
    free_binary_heap(heap);
}

void dijkstra_fibonacci_heap(Graph* graph, int source, int* distances) {
    fib_heap_ops = 0;
    fib_decrease_key_ops = 0;

    FibHeap* heap = create_fib_heap(graph->num_vertices);
    bool* visited = (bool*)calloc(graph->num_vertices, sizeof(bool));

    // Initialize distances
    for (int i = 0; i < graph->num_vertices; i++) {
        distances[i] = INF;
    }
    distances[source] = 0;

    fib_heap_insert(heap, source, 0);
    fib_heap_ops++;

    while (!fib_heap_is_empty(heap)) {
        FibNode* min = fib_heap_extract_min(heap);
        fib_heap_ops++;

        int u = min->vertex;
        free(min);

        if (visited[u]) continue;
        visited[u] = true;

        // Process neighbors
        Edge* edge = graph->adj_list[u];
        while (edge != NULL) {
            int v = edge->dest;
            int weight = edge->weight;

            if (!visited[v] && distances[u] != INF) {
                int new_dist = distances[u] + weight;

                if (new_dist < distances[v]) {
                    distances[v] = new_dist;

                    if (heap->node_map[v] == NULL) {
                        fib_heap_insert(heap, v, new_dist);
                        fib_heap_ops++;
                    } else {
                        fib_heap_decrease_key(heap, v, new_dist);
                        fib_decrease_key_ops++;
                    }
                }
            }

            edge = edge->next;
        }
    }

    free(visited);
    free_fib_heap(heap);
}

// ============================================================================
// STATISTICAL ANALYSIS
// ============================================================================

int compare_doubles(const void* a, const void* b) {
    double diff = (*(double*)a - *(double*)b);
    return (diff > 0) - (diff < 0);
}

Statistics compute_statistics(double* data, int n) {
    Statistics stats;

    // Sort data for median
    double* sorted = (double*)malloc(n * sizeof(double));
    memcpy(sorted, data, n * sizeof(double));
    qsort(sorted, n, sizeof(double), compare_doubles);

    // Mean
    double sum = 0;
    for (int i = 0; i < n; i++) {
        sum += data[i];
    }
    stats.mean = sum / n;

    // Standard deviation
    double sq_sum = 0;
    for (int i = 0; i < n; i++) {
        double diff = data[i] - stats.mean;
        sq_sum += diff * diff;
    }
    stats.std_dev = sqrt(sq_sum / n);

    // Median
    if (n % 2 == 0) {
        stats.median = (sorted[n/2 - 1] + sorted[n/2]) / 2.0;
    } else {
        stats.median = sorted[n/2];
    }

    // Min and Max
    stats.min = sorted[0];
    stats.max = sorted[n - 1];

    // 95% Confidence Interval (using t-distribution approximation)
    // For n=10, t-value ≈ 2.262 for 95% CI
    double t_value = 2.262;
    double margin = t_value * (stats.std_dev / sqrt(n));
    stats.conf_interval_lower = stats.mean - margin;
    stats.conf_interval_upper = stats.mean + margin;

    free(sorted);
    return stats;
}

void print_statistics(const char* label, Statistics stats) {
    printf("\n%s:\n", label);
    printf("  Mean:       %.6f ms\n", stats.mean * 1000);
    printf("  Std Dev:    %.6f ms\n", stats.std_dev * 1000);
    printf("  Median:     %.6f ms\n", stats.median * 1000);
    printf("  Min:        %.6f ms\n", stats.min * 1000);
    printf("  Max:        %.6f ms\n", stats.max * 1000);
    printf("  95%% CI:     [%.6f, %.6f] ms\n",
           stats.conf_interval_lower * 1000,
           stats.conf_interval_upper * 1000);
}

// ============================================================================
// BENCHMARKING FRAMEWORK
// ============================================================================

double get_time_seconds() {
    return (double)clock() / CLOCKS_PER_SEC;
}

BenchmarkResult run_benchmark(Graph* graph, const char* heap_type,
                              void (*dijkstra_func)(Graph*, int, int*)) {
    BenchmarkResult result;
    strcpy(result.heap_type, heap_type);
    result.num_vertices = graph->num_vertices;
    result.num_edges = graph->num_edges;

    int* distances = (int*)malloc(graph->num_vertices * sizeof(int));

    printf("Running %s (V=%d, E=%d)...\n",
           heap_type, graph->num_vertices, graph->num_edges);

    for (int trial = 0; trial < NUM_TRIALS; trial++) {
        double start = get_time_seconds();
        dijkstra_func(graph, 0, distances);
        double end = get_time_seconds();

        result.execution_times[trial] = end - start;
        printf("  Trial %d: %.6f ms\n", trial + 1, result.execution_times[trial] * 1000);
    }

    result.stats = compute_statistics(result.execution_times, NUM_TRIALS);

    // Get operation counts from last run
    if (strcmp(heap_type, "Binary Heap") == 0) {
        result.heap_operations = binary_heap_ops;
        result.decrease_key_ops = binary_decrease_key_ops;
    } else {
        result.heap_operations = fib_heap_ops;
        result.decrease_key_ops = fib_decrease_key_ops;
    }

    free(distances);
    return result;
}

void compare_results(BenchmarkResult binary_result, BenchmarkResult fib_result) {
    printf("\n");
    printf("================================================================================\n");
    printf("COMPARISON SUMMARY\n");
    printf("================================================================================\n");

    printf("\nGraph Properties:\n");
    printf("  Vertices: %d\n", binary_result.num_vertices);
    printf("  Edges:    %d\n", binary_result.num_edges);
    printf("  Density:  %.4f\n",
           (double)binary_result.num_edges /
           (binary_result.num_vertices * (binary_result.num_vertices - 1)));

    print_statistics("Binary Heap", binary_result.stats);
    print_statistics("Fibonacci Heap", fib_result.stats);

    printf("\nHeap Operations:\n");
    printf("  Binary Heap:\n");
    printf("    Total ops:        %ld\n", binary_result.heap_operations);
    printf("    Decrease-key ops: %ld\n", binary_result.decrease_key_ops);
    printf("  Fibonacci Heap:\n");
    printf("    Total ops:        %ld\n", fib_result.heap_operations);
    printf("    Decrease-key ops: %ld\n", fib_result.decrease_key_ops);

    double speedup = binary_result.stats.mean / fib_result.stats.mean;
    printf("\nPerformance:\n");
    printf("  Speedup: %.2fx %s\n",
           fabs(speedup),
           speedup > 1 ? "(Fibonacci faster)" : "(Binary faster)");

    // Theoretical complexity analysis
    int V = binary_result.num_vertices;
    int E = binary_result.num_edges;

    printf("\nTheoretical Complexity:\n");
    printf("  Binary Heap:    O((V+E)log V) = O(%d)\n",
           (int)((V + E) * log2(V)));
    printf("  Fibonacci Heap: O(E + V log V) = O(%d)\n",
           (int)(E + V * log2(V)));

    double theoretical_ratio = (double)((V + E) * log2(V)) / (E + V * log2(V));
    double actual_ratio = binary_result.stats.mean / fib_result.stats.mean;

    printf("\nTheoretical vs Actual:\n");
    printf("  Theoretical ratio: %.2f\n", theoretical_ratio);
    printf("  Actual ratio:      %.2f\n", actual_ratio);
    printf("  Difference:        %.2f%%\n",
           fabs(theoretical_ratio - actual_ratio) / theoretical_ratio * 100);
}

// ============================================================================
// CSV OUTPUT
// ============================================================================

void write_csv_header(FILE* file) {
    fprintf(file, "heap_type,num_vertices,num_edges,density,");
    fprintf(file, "mean_time_ms,std_dev_ms,median_ms,min_ms,max_ms,");
    fprintf(file, "conf_lower_ms,conf_upper_ms,");
    fprintf(file, "heap_operations,decrease_key_ops,");
    fprintf(file, "theoretical_complexity\n");
}

void write_csv_result(FILE* file, BenchmarkResult result) {
    double density = (double)result.num_edges /
                     (result.num_vertices * (result.num_vertices - 1));

    int V = result.num_vertices;
    int E = result.num_edges;
    long theoretical;

    if (strcmp(result.heap_type, "Binary Heap") == 0) {
        theoretical = (long)((V + E) * log2(V));
    } else {
        theoretical = (long)(E + V * log2(V));
    }

    fprintf(file, "%s,%d,%d,%.6f,",
            result.heap_type, result.num_vertices, result.num_edges, density);
    fprintf(file, "%.6f,%.6f,%.6f,%.6f,%.6f,",
            result.stats.mean * 1000, result.stats.std_dev * 1000,
            result.stats.median * 1000, result.stats.min * 1000,
            result.stats.max * 1000);
    fprintf(file, "%.6f,%.6f,",
            result.stats.conf_interval_lower * 1000,
            result.stats.conf_interval_upper * 1000);
    fprintf(file, "%ld,%ld,%ld\n",
            result.heap_operations, result.decrease_key_ops, theoretical);
}

void write_detailed_csv(const char* filename, BenchmarkResult* results, int num_results) {
    FILE* file = fopen(filename, "w");
    if (file == NULL) {
        fprintf(stderr, "Error: Could not open %s for writing\n", filename);
        return;
    }

    write_csv_header(file);

    for (int i = 0; i < num_results; i++) {
        write_csv_result(file, results[i]);
    }

    fclose(file);
    printf("\nResults written to %s\n", filename);
}

void write_trials_csv(const char* filename, BenchmarkResult* results, int num_results) {
    FILE* file = fopen(filename, "w");
    if (file == NULL) {
        fprintf(stderr, "Error: Could not open %s for writing\n", filename);
        return;
    }

    fprintf(file, "heap_type,num_vertices,trial,time_ms\n");

    for (int i = 0; i < num_results; i++) {
        for (int trial = 0; trial < NUM_TRIALS; trial++) {
            fprintf(file, "%s,%d,%d,%.6f\n",
                    results[i].heap_type,
                    results[i].num_vertices,
                    trial + 1,
                    results[i].execution_times[trial] * 1000);
        }
    }

    fclose(file);
    printf("Trial data written to %s\n", filename);
}

// ============================================================================
// MAIN BENCHMARK SUITE
// ============================================================================

void run_comprehensive_benchmark() {
    printf("\n");
    printf("================================================================================\n");
    printf("DIJKSTRA'S ALGORITHM PERFORMANCE COMPARISON\n");
    printf("Binary Heap vs Fibonacci Heap\n");
    printf("================================================================================\n");

    // Test configurations
    int vertex_counts[] = {100, 200, 500, 1000, 2000};
    int num_configs = 5;

    BenchmarkResult* all_results =
        (BenchmarkResult*)malloc(num_configs * 4 * sizeof(BenchmarkResult));
    int result_idx = 0;

    for (int i = 0; i < num_configs; i++) {
        int V = vertex_counts[i];

        printf("\n\n");
        printf("================================================================================\n");
        printf("DENSE GRAPH: V=%d\n", V);
        printf("================================================================================\n");

        Graph* dense_graph = generate_dense_graph(V, 0.3);

        BenchmarkResult binary_dense =
            run_benchmark(dense_graph, "Binary Heap", dijkstra_binary_heap);
        all_results[result_idx++] = binary_dense;

        BenchmarkResult fib_dense =
            run_benchmark(dense_graph, "Fibonacci Heap", dijkstra_fibonacci_heap);
        all_results[result_idx++] = fib_dense;

        compare_results(binary_dense, fib_dense);

        free_graph(dense_graph);

        printf("\n\n");
        printf("================================================================================\n");
        printf("SPARSE GRAPH: V=%d\n", V);
        printf("================================================================================\n");

        Graph* sparse_graph = generate_sparse_graph(V);

        BenchmarkResult binary_sparse =
            run_benchmark(sparse_graph, "Binary Heap", dijkstra_binary_heap);
        all_results[result_idx++] = binary_sparse;

        BenchmarkResult fib_sparse =
            run_benchmark(sparse_graph, "Fibonacci Heap", dijkstra_fibonacci_heap);
        all_results[result_idx++] = fib_sparse;

        compare_results(binary_sparse, fib_sparse);

        free_graph(sparse_graph);
    }

    // Write CSV files
    write_detailed_csv("dijkstra_results.csv", all_results, result_idx);
    write_trials_csv("dijkstra_trials.csv", all_results, result_idx);

    free(all_results);
}

void print_usage() {
    printf("\nDijkstra Performance Comparison Tool\n");
    printf("Usage:\n");
    printf("  ./compare_dijkstra          - Run comprehensive benchmark\n");
    printf("  ./compare_dijkstra V E      - Test specific graph (V vertices, E edges)\n");
    printf("\n");
}

// ============================================================================
// MAIN
// ============================================================================

int main(int argc, char* argv[]) {
    srand(time(NULL));

    if (argc == 1) {
        // Run comprehensive benchmark
        run_comprehensive_benchmark();
    } else if (argc == 3) {
        // Custom graph test
        int V = atoi(argv[1]);
        int E = atoi(argv[2]);

        if (V <= 0 || E <= 0) {
            fprintf(stderr, "Error: Invalid graph parameters\n");
            print_usage();
            return 1;
        }

        printf("\nCustom Graph Test: V=%d, E=%d\n", V, E);

        double density = (double)E / (V * (V - 1));
        Graph* graph = generate_dense_graph(V, density);

        BenchmarkResult binary_result =
            run_benchmark(graph, "Binary Heap", dijkstra_binary_heap);
        BenchmarkResult fib_result =
            run_benchmark(graph, "Fibonacci Heap", dijkstra_fibonacci_heap);

        compare_results(binary_result, fib_result);

        free_graph(graph);
    } else {
        print_usage();
        return 1;
    }

    printf("\n\nBenchmark complete!\n");
    printf("CSV files generated:\n");
    printf("  - dijkstra_results.csv: Summary statistics\n");
    printf("  - dijkstra_trials.csv:  Individual trial data\n");
    printf("\n");

    return 0;
}
