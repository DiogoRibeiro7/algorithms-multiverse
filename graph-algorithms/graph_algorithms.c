/*
 * Graph Algorithms in C
 *
 * Implementations of fundamental graph algorithms:
 * - Breadth-First Search (BFS)
 * - Depth-First Search (DFS)
 * - Dijkstra's Shortest Path
 *
 * Graph representation: Adjacency List
 */

#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <stdbool.h>

#define MAX_VERTICES 100

// ===================================================================
// DATA STRUCTURES
// ===================================================================

// Adjacency list node
typedef struct AdjListNode {
    int dest;
    int weight;
    struct AdjListNode* next;
} AdjListNode;

// Adjacency list
typedef struct AdjList {
    AdjListNode* head;
} AdjList;

// Graph structure
typedef struct Graph {
    int num_vertices;
    AdjList* array;
} Graph;

// Queue for BFS
typedef struct Queue {
    int items[MAX_VERTICES];
    int front, rear;
} Queue;

// Min heap node for Dijkstra
typedef struct MinHeapNode {
    int vertex;
    int dist;
} MinHeapNode;

// Min heap
typedef struct MinHeap {
    int size;
    int capacity;
    int* pos;  // Position of vertices in heap
    MinHeapNode** array;
} MinHeap;

// ===================================================================
// GRAPH CREATION AND MANIPULATION
// ===================================================================

AdjListNode* create_adj_list_node(int dest, int weight) {
    AdjListNode* new_node = (AdjListNode*)malloc(sizeof(AdjListNode));
    new_node->dest = dest;
    new_node->weight = weight;
    new_node->next = NULL;
    return new_node;
}

Graph* create_graph(int num_vertices) {
    Graph* graph = (Graph*)malloc(sizeof(Graph));
    graph->num_vertices = num_vertices;
    graph->array = (AdjList*)malloc(num_vertices * sizeof(AdjList));

    for (int i = 0; i < num_vertices; i++) {
        graph->array[i].head = NULL;
    }

    return graph;
}

void add_edge(Graph* graph, int src, int dest, int weight) {
    // Add edge from src to dest
    AdjListNode* new_node = create_adj_list_node(dest, weight);
    new_node->next = graph->array[src].head;
    graph->array[src].head = new_node;

    // For undirected graph, add edge from dest to src as well
    new_node = create_adj_list_node(src, weight);
    new_node->next = graph->array[dest].head;
    graph->array[dest].head = new_node;
}

void print_graph(Graph* graph) {
    printf("Graph adjacency list:\n");
    for (int v = 0; v < graph->num_vertices; v++) {
        AdjListNode* current = graph->array[v].head;
        printf("Vertex %d: ", v);
        while (current) {
            printf("-> %d(w:%d) ", current->dest, current->weight);
            current = current->next;
        }
        printf("\n");
    }
}

// ===================================================================
// QUEUE OPERATIONS (for BFS)
// ===================================================================

Queue* create_queue() {
    Queue* q = (Queue*)malloc(sizeof(Queue));
    q->front = q->rear = -1;
    return q;
}

bool is_queue_empty(Queue* q) {
    return q->front == -1;
}

void enqueue(Queue* q, int value) {
    if (q->rear == MAX_VERTICES - 1) {
        printf("Queue overflow!\n");
        return;
    }

    if (q->front == -1) q->front = 0;
    q->rear++;
    q->items[q->rear] = value;
}

int dequeue(Queue* q) {
    if (is_queue_empty(q)) {
        printf("Queue underflow!\n");
        return -1;
    }

    int item = q->items[q->front];
    if (q->front >= q->rear) {
        q->front = q->rear = -1;
    } else {
        q->front++;
    }

    return item;
}

// ===================================================================
// BREADTH-FIRST SEARCH (BFS)
// ===================================================================

void bfs(Graph* graph, int start_vertex) {
    bool visited[MAX_VERTICES] = {false};
    Queue* queue = create_queue();

    visited[start_vertex] = true;
    enqueue(queue, start_vertex);

    printf("BFS traversal starting from vertex %d: ", start_vertex);

    while (!is_queue_empty(queue)) {
        int current = dequeue(queue);
        printf("%d ", current);

        // Visit all adjacent vertices
        AdjListNode* temp = graph->array[current].head;
        while (temp) {
            int adj_vertex = temp->dest;
            if (!visited[adj_vertex]) {
                visited[adj_vertex] = true;
                enqueue(queue, adj_vertex);
            }
            temp = temp->next;
        }
    }

    printf("\n");
    free(queue);
}

// ===================================================================
// DEPTH-FIRST SEARCH (DFS)
// ===================================================================

void dfs_util(Graph* graph, int vertex, bool visited[]) {
    visited[vertex] = true;
    printf("%d ", vertex);

    // Visit all adjacent vertices
    AdjListNode* temp = graph->array[vertex].head;
    while (temp) {
        int adj_vertex = temp->dest;
        if (!visited[adj_vertex]) {
            dfs_util(graph, adj_vertex, visited);
        }
        temp = temp->next;
    }
}

void dfs(Graph* graph, int start_vertex) {
    bool visited[MAX_VERTICES] = {false};

    printf("DFS traversal starting from vertex %d: ", start_vertex);
    dfs_util(graph, start_vertex, visited);
    printf("\n");
}

// ===================================================================
// DIJKSTRA'S SHORTEST PATH
// ===================================================================

MinHeapNode* create_min_heap_node(int v, int dist) {
    MinHeapNode* node = (MinHeapNode*)malloc(sizeof(MinHeapNode));
    node->vertex = v;
    node->dist = dist;
    return node;
}

MinHeap* create_min_heap(int capacity) {
    MinHeap* heap = (MinHeap*)malloc(sizeof(MinHeap));
    heap->pos = (int*)malloc(capacity * sizeof(int));
    heap->size = 0;
    heap->capacity = capacity;
    heap->array = (MinHeapNode**)malloc(capacity * sizeof(MinHeapNode*));
    return heap;
}

void swap_min_heap_nodes(MinHeapNode** a, MinHeapNode** b) {
    MinHeapNode* temp = *a;
    *a = *b;
    *b = temp;
}

void min_heapify(MinHeap* heap, int idx) {
    int smallest = idx;
    int left = 2 * idx + 1;
    int right = 2 * idx + 2;

    if (left < heap->size && heap->array[left]->dist < heap->array[smallest]->dist)
        smallest = left;

    if (right < heap->size && heap->array[right]->dist < heap->array[smallest]->dist)
        smallest = right;

    if (smallest != idx) {
        MinHeapNode* smallest_node = heap->array[smallest];
        MinHeapNode* idx_node = heap->array[idx];

        heap->pos[smallest_node->vertex] = idx;
        heap->pos[idx_node->vertex] = smallest;

        swap_min_heap_nodes(&heap->array[smallest], &heap->array[idx]);
        min_heapify(heap, smallest);
    }
}

bool is_heap_empty(MinHeap* heap) {
    return heap->size == 0;
}

MinHeapNode* extract_min(MinHeap* heap) {
    if (is_heap_empty(heap)) return NULL;

    MinHeapNode* root = heap->array[0];
    MinHeapNode* last_node = heap->array[heap->size - 1];
    heap->array[0] = last_node;

    heap->pos[root->vertex] = heap->size - 1;
    heap->pos[last_node->vertex] = 0;

    heap->size--;
    min_heapify(heap, 0);

    return root;
}

void decrease_key(MinHeap* heap, int v, int dist) {
    int i = heap->pos[v];
    heap->array[i]->dist = dist;

    while (i && heap->array[i]->dist < heap->array[(i - 1) / 2]->dist) {
        heap->pos[heap->array[i]->vertex] = (i - 1) / 2;
        heap->pos[heap->array[(i - 1) / 2]->vertex] = i;
        swap_min_heap_nodes(&heap->array[i], &heap->array[(i - 1) / 2]);
        i = (i - 1) / 2;
    }
}

bool is_in_min_heap(MinHeap* heap, int v) {
    return heap->pos[v] < heap->size;
}

void dijkstra(Graph* graph, int src) {
    int V = graph->num_vertices;
    int dist[MAX_VERTICES];

    MinHeap* heap = create_min_heap(V);

    // Initialize distances and heap
    for (int v = 0; v < V; v++) {
        dist[v] = INT_MAX;
        heap->array[v] = create_min_heap_node(v, dist[v]);
        heap->pos[v] = v;
    }

    heap->array[src] = create_min_heap_node(src, dist[src]);
    heap->pos[src] = src;
    dist[src] = 0;
    decrease_key(heap, src, dist[src]);

    heap->size = V;

    // Process all vertices
    while (!is_heap_empty(heap)) {
        MinHeapNode* min_node = extract_min(heap);
        int u = min_node->vertex;

        AdjListNode* current = graph->array[u].head;
        while (current != NULL) {
            int v = current->dest;

            if (is_in_min_heap(heap, v) && dist[u] != INT_MAX &&
                current->weight + dist[u] < dist[v]) {
                dist[v] = dist[u] + current->weight;
                decrease_key(heap, v, dist[v]);
            }
            current = current->next;
        }
    }

    // Print results
    printf("\nDijkstra's shortest paths from vertex %d:\n", src);
    printf("Vertex\tDistance from Source\n");
    for (int i = 0; i < V; i++) {
        printf("%d\t\t", i);
        if (dist[i] == INT_MAX)
            printf("INF\n");
        else
            printf("%d\n", dist[i]);
    }
}

// ===================================================================
// MAIN DEMONSTRATION
// ===================================================================

int main() {
    printf("====================================================================\n");
    printf("                    GRAPH ALGORITHMS IN C\n");
    printf("====================================================================\n\n");

    // Create a graph
    int num_vertices = 6;
    Graph* graph = create_graph(num_vertices);

    // Add edges (undirected graph with weights)
    add_edge(graph, 0, 1, 4);
    add_edge(graph, 0, 2, 3);
    add_edge(graph, 1, 2, 1);
    add_edge(graph, 1, 3, 2);
    add_edge(graph, 2, 3, 4);
    add_edge(graph, 3, 4, 2);
    add_edge(graph, 4, 5, 6);

    // Print graph structure
    print_graph(graph);
    printf("\n");

    // Test BFS
    printf("Test 1: Breadth-First Search (BFS)\n");
    printf("--------------------------------------------------------------------\n");
    bfs(graph, 0);
    printf("\n");

    // Test DFS
    printf("Test 2: Depth-First Search (DFS)\n");
    printf("--------------------------------------------------------------------\n");
    dfs(graph, 0);
    printf("\n");

    // Test Dijkstra
    printf("Test 3: Dijkstra's Shortest Path Algorithm\n");
    printf("--------------------------------------------------------------------\n");
    dijkstra(graph, 0);

    printf("\n====================================================================\n");
    printf("Key Points:\n");
    printf("- BFS: O(V + E) time, explores level by level, shortest path (unweighted)\n");
    printf("- DFS: O(V + E) time, explores depth-first, good for connectivity\n");
    printf("- Dijkstra: O((V + E) log V) time, shortest path in weighted graphs\n");
    printf("- All use adjacency list representation for efficiency\n");
    printf("====================================================================\n");

    return 0;
}
