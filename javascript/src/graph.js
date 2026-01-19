/**
 * Graph Algorithms Module
 * Comprehensive implementations of graph data structures and algorithms
 */

// Min-heap for priority queue (used in Dijkstra, Prim)
class MinHeap {
    constructor(compareFunc = (a, b) => a - b) {
        this.heap = [];
        this.compare = compareFunc;
    }

    push(item) {
        this.heap.push(item);
        this.bubbleUp(this.heap.length - 1);
    }

    pop() {
        if (this.isEmpty()) return null;
        const min = this.heap[0];
        const last = this.heap.pop();
        if (this.heap.length > 0) {
            this.heap[0] = last;
            this.bubbleDown(0);
        }
        return min;
    }

    bubbleUp(index) {
        while (index > 0) {
            const parentIndex = Math.floor((index - 1) / 2);
            if (this.compare(this.heap[index], this.heap[parentIndex]) < 0) {
                [this.heap[index], this.heap[parentIndex]] = [this.heap[parentIndex], this.heap[index]];
                index = parentIndex;
            } else {
                break;
            }
        }
    }

    bubbleDown(index) {
        while (true) {
            let minIndex = index;
            const leftChild = 2 * index + 1;
            const rightChild = 2 * index + 2;

            if (leftChild < this.heap.length &&
                this.compare(this.heap[leftChild], this.heap[minIndex]) < 0) {
                minIndex = leftChild;
            }

            if (rightChild < this.heap.length &&
                this.compare(this.heap[rightChild], this.heap[minIndex]) < 0) {
                minIndex = rightChild;
            }

            if (minIndex !== index) {
                [this.heap[index], this.heap[minIndex]] = [this.heap[minIndex], this.heap[index]];
                index = minIndex;
            } else {
                break;
            }
        }
    }

    isEmpty() {
        return this.heap.length === 0;
    }

    size() {
        return this.heap.length;
    }
}

// Union-Find (Disjoint Set) data structure
class UnionFind {
    constructor(size) {
        this.parent = Array(size).fill().map((_, i) => i);
        this.rank = Array(size).fill(0);
        this.components = size;
    }

    find(x) {
        if (this.parent[x] !== x) {
            this.parent[x] = this.find(this.parent[x]); // Path compression
        }
        return this.parent[x];
    }

    union(x, y) {
        const rootX = this.find(x);
        const rootY = this.find(y);

        if (rootX === rootY) return false;

        // Union by rank
        if (this.rank[rootX] < this.rank[rootY]) {
            this.parent[rootX] = rootY;
        } else if (this.rank[rootX] > this.rank[rootY]) {
            this.parent[rootY] = rootX;
        } else {
            this.parent[rootY] = rootX;
            this.rank[rootX]++;
        }

        this.components--;
        return true;
    }

    isConnected(x, y) {
        return this.find(x) === this.find(y);
    }

    getComponents() {
        return this.components;
    }
}

/**
 * Graph class supporting both directed and undirected graphs
 */
export class Graph {
    constructor(directed = false) {
        this.adjacencyList = new Map();
        this.directed = directed;
        this.vertices = new Set();
    }

    // Add a vertex to the graph
    addVertex(vertex) {
        if (!this.adjacencyList.has(vertex)) {
            this.adjacencyList.set(vertex, []);
            this.vertices.add(vertex);
        }
    }

    // Add an edge to the graph
    addEdge(from, to, weight = 1) {
        this.addVertex(from);
        this.addVertex(to);

        this.adjacencyList.get(from).push({ vertex: to, weight });

        if (!this.directed) {
            this.adjacencyList.get(to).push({ vertex: from, weight });
        }
    }

    // Remove an edge from the graph
    removeEdge(from, to) {
        if (this.adjacencyList.has(from)) {
            this.adjacencyList.set(from,
                this.adjacencyList.get(from).filter(edge => edge.vertex !== to)
            );
        }

        if (!this.directed && this.adjacencyList.has(to)) {
            this.adjacencyList.set(to,
                this.adjacencyList.get(to).filter(edge => edge.vertex !== from)
            );
        }
    }

    // Remove a vertex from the graph
    removeVertex(vertex) {
        if (!this.adjacencyList.has(vertex)) return;

        // Remove all edges to this vertex
        for (const [v, edges] of this.adjacencyList) {
            this.adjacencyList.set(v,
                edges.filter(edge => edge.vertex !== vertex)
            );
        }

        // Remove the vertex itself
        this.adjacencyList.delete(vertex);
        this.vertices.delete(vertex);
    }

    // Get neighbors of a vertex
    getNeighbors(vertex) {
        return this.adjacencyList.get(vertex) || [];
    }

    // Get all vertices
    getVertices() {
        return Array.from(this.vertices);
    }

    // Get vertex count
    getVertexCount() {
        return this.vertices.size;
    }

    // Get edge count
    getEdgeCount() {
        let count = 0;
        for (const edges of this.adjacencyList.values()) {
            count += edges.length;
        }
        return this.directed ? count : count / 2;
    }

    // Check if graph has a vertex
    hasVertex(vertex) {
        return this.adjacencyList.has(vertex);
    }

    // Check if graph has an edge
    hasEdge(from, to) {
        if (!this.adjacencyList.has(from)) return false;
        return this.adjacencyList.get(from).some(edge => edge.vertex === to);
    }

    // Get degree of a vertex
    getDegree(vertex) {
        if (!this.adjacencyList.has(vertex)) return 0;

        if (this.directed) {
            return {
                inDegree: this.getInDegree(vertex),
                outDegree: this.getOutDegree(vertex)
            };
        }

        return this.adjacencyList.get(vertex).length;
    }

    // Get in-degree of a vertex (for directed graphs)
    getInDegree(vertex) {
        let inDegree = 0;
        for (const [v, edges] of this.adjacencyList) {
            if (v !== vertex) {
                for (const edge of edges) {
                    if (edge.vertex === vertex) inDegree++;
                }
            }
        }
        return inDegree;
    }

    // Get out-degree of a vertex (for directed graphs)
    getOutDegree(vertex) {
        if (!this.adjacencyList.has(vertex)) return 0;
        return this.adjacencyList.get(vertex).length;
    }

    // Create adjacency matrix representation
    toAdjacencyMatrix() {
        const vertices = this.getVertices();
        const n = vertices.length;
        const matrix = Array(n).fill().map(() => Array(n).fill(Infinity));
        const vertexToIndex = new Map();

        vertices.forEach((v, i) => {
            vertexToIndex.set(v, i);
            matrix[i][i] = 0;
        });

        for (const [from, edges] of this.adjacencyList) {
            const fromIndex = vertexToIndex.get(from);
            for (const { vertex: to, weight } of edges) {
                const toIndex = vertexToIndex.get(to);
                matrix[fromIndex][toIndex] = weight;
            }
        }

        return { matrix, vertices, vertexToIndex };
    }

    // Clone the graph
    clone() {
        const newGraph = new Graph(this.directed);
        for (const vertex of this.vertices) {
            newGraph.addVertex(vertex);
        }
        for (const [from, edges] of this.adjacencyList) {
            for (const { vertex: to, weight } of edges) {
                if (this.directed || from <= to) {
                    newGraph.addEdge(from, to, weight);
                }
            }
        }
        return newGraph;
    }
}

// Breadth-First Search
export function bfs(graph, startVertex, visitFunc = null) {
    const visited = new Set();
    const queue = [startVertex];
    const result = [];

    visited.add(startVertex);

    while (queue.length > 0) {
        const vertex = queue.shift();
        result.push(vertex);

        if (visitFunc) visitFunc(vertex);

        for (const { vertex: neighbor } of graph.getNeighbors(vertex)) {
            if (!visited.has(neighbor)) {
                visited.add(neighbor);
                queue.push(neighbor);
            }
        }
    }

    return result;
}

// Depth-First Search (iterative)
export function dfs(graph, startVertex, visitFunc = null) {
    const visited = new Set();
    const stack = [startVertex];
    const result = [];

    while (stack.length > 0) {
        const vertex = stack.pop();

        if (!visited.has(vertex)) {
            visited.add(vertex);
            result.push(vertex);

            if (visitFunc) visitFunc(vertex);

            for (const { vertex: neighbor } of graph.getNeighbors(vertex)) {
                if (!visited.has(neighbor)) {
                    stack.push(neighbor);
                }
            }
        }
    }

    return result;
}

// Depth-First Search (recursive)
export function dfsRecursive(graph, startVertex, visitFunc = null) {
    const visited = new Set();
    const result = [];

    function dfsHelper(vertex) {
        visited.add(vertex);
        result.push(vertex);

        if (visitFunc) visitFunc(vertex);

        for (const { vertex: neighbor } of graph.getNeighbors(vertex)) {
            if (!visited.has(neighbor)) {
                dfsHelper(neighbor);
            }
        }
    }

    dfsHelper(startVertex);
    return result;
}

// Dijkstra's shortest path algorithm
export function dijkstra(graph, startVertex) {
    const distances = new Map();
    const previous = new Map();
    const visited = new Set();
    const heap = new MinHeap((a, b) => a.distance - b.distance);

    // Initialize distances
    for (const vertex of graph.getVertices()) {
        distances.set(vertex, vertex === startVertex ? 0 : Infinity);
        previous.set(vertex, null);
    }

    heap.push({ vertex: startVertex, distance: 0 });

    while (!heap.isEmpty()) {
        const { vertex: current } = heap.pop();

        if (visited.has(current)) continue;
        visited.add(current);

        for (const { vertex: neighbor, weight } of graph.getNeighbors(current)) {
            const altDistance = distances.get(current) + weight;

            if (altDistance < distances.get(neighbor)) {
                distances.set(neighbor, altDistance);
                previous.set(neighbor, current);
                heap.push({ vertex: neighbor, distance: altDistance });
            }
        }
    }

    // Helper function to reconstruct path
    const getPath = (endVertex) => {
        const path = [];
        let current = endVertex;

        while (current !== null) {
            path.unshift(current);
            current = previous.get(current);
        }

        return path[0] === startVertex ? path : [];
    };

    return { distances, previous, getPath };
}

// Bellman-Ford algorithm (handles negative weights)
export function bellmanFord(graph, startVertex) {
    const distances = new Map();
    const previous = new Map();
    const vertices = graph.getVertices();

    // Initialize distances
    for (const vertex of vertices) {
        distances.set(vertex, vertex === startVertex ? 0 : Infinity);
        previous.set(vertex, null);
    }

    // Relax edges |V| - 1 times
    for (let i = 0; i < vertices.length - 1; i++) {
        let updated = false;

        for (const from of vertices) {
            if (distances.get(from) === Infinity) continue;

            for (const { vertex: to, weight } of graph.getNeighbors(from)) {
                const altDistance = distances.get(from) + weight;

                if (altDistance < distances.get(to)) {
                    distances.set(to, altDistance);
                    previous.set(to, from);
                    updated = true;
                }
            }
        }

        if (!updated) break; // Early termination if no updates
    }

    // Check for negative cycles
    let hasNegativeCycle = false;
    for (const from of vertices) {
        if (distances.get(from) === Infinity) continue;

        for (const { vertex: to, weight } of graph.getNeighbors(from)) {
            if (distances.get(from) + weight < distances.get(to)) {
                hasNegativeCycle = true;
                break;
            }
        }
        if (hasNegativeCycle) break;
    }

    // Helper function to reconstruct path
    const getPath = (endVertex) => {
        if (hasNegativeCycle) return null;

        const path = [];
        let current = endVertex;

        while (current !== null) {
            path.unshift(current);
            current = previous.get(current);
        }

        return path[0] === startVertex ? path : [];
    };

    return { distances, previous, hasNegativeCycle, getPath };
}

// Floyd-Warshall algorithm (all-pairs shortest paths)
export function floydWarshall(graph) {
    const { matrix, vertices } = graph.toAdjacencyMatrix();
    const n = vertices.length;
    const dist = matrix.map(row => [...row]);
    const next = Array(n).fill().map(() => Array(n).fill(null));

    // Initialize next matrix for path reconstruction
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            if (i !== j && dist[i][j] !== Infinity) {
                next[i][j] = j;
            }
        }
    }

    // Main algorithm
    for (let k = 0; k < n; k++) {
        for (let i = 0; i < n; i++) {
            for (let j = 0; j < n; j++) {
                if (dist[i][k] !== Infinity && dist[k][j] !== Infinity) {
                    if (dist[i][k] + dist[k][j] < dist[i][j]) {
                        dist[i][j] = dist[i][k] + dist[k][j];
                        next[i][j] = next[i][k];
                    }
                }
            }
        }
    }

    // Check for negative cycles
    let hasNegativeCycle = false;
    for (let i = 0; i < n; i++) {
        if (dist[i][i] < 0) {
            hasNegativeCycle = true;
            break;
        }
    }

    // Helper function to reconstruct path
    const getPath = (start, end) => {
        const startIdx = vertices.indexOf(start);
        const endIdx = vertices.indexOf(end);

        if (startIdx === -1 || endIdx === -1) return [];
        if (next[startIdx][endIdx] === null) return [];

        const path = [start];
        let current = startIdx;

        while (current !== endIdx) {
            current = next[current][endIdx];
            path.push(vertices[current]);
        }

        return path;
    };

    return { distances: dist, vertices, hasNegativeCycle, getPath };
}

// Kruskal's Minimum Spanning Tree algorithm
export function kruskal(graph) {
    if (graph.directed) {
        throw new Error("MST algorithms require undirected graphs");
    }

    const edges = [];
    const vertices = graph.getVertices();
    const vertexToIndex = new Map();

    // Create vertex to index mapping
    vertices.forEach((v, i) => vertexToIndex.set(v, i));

    // Collect all edges
    const seenEdges = new Set();
    for (const [from, neighbors] of graph.adjacencyList) {
        for (const { vertex: to, weight } of neighbors) {
            const edgeKey = from < to ? `${from}-${to}` : `${to}-${from}`;
            if (!seenEdges.has(edgeKey)) {
                edges.push({ from, to, weight });
                seenEdges.add(edgeKey);
            }
        }
    }

    // Sort edges by weight
    edges.sort((a, b) => a.weight - b.weight);

    // Use Union-Find to detect cycles
    const uf = new UnionFind(vertices.length);
    const mst = [];
    let totalWeight = 0;

    for (const edge of edges) {
        const fromIdx = vertexToIndex.get(edge.from);
        const toIdx = vertexToIndex.get(edge.to);

        if (uf.union(fromIdx, toIdx)) {
            mst.push(edge);
            totalWeight += edge.weight;

            if (mst.length === vertices.length - 1) break;
        }
    }

    return { edges: mst, totalWeight };
}

// Prim's Minimum Spanning Tree algorithm
export function prim(graph, startVertex = null) {
    if (graph.directed) {
        throw new Error("MST algorithms require undirected graphs");
    }

    const vertices = graph.getVertices();
    if (vertices.length === 0) return { edges: [], totalWeight: 0 };

    if (startVertex === null) {
        startVertex = vertices[0];
    }

    const visited = new Set();
    const mst = [];
    let totalWeight = 0;

    const heap = new MinHeap((a, b) => a.weight - b.weight);

    // Start with the startVertex
    visited.add(startVertex);

    // Add all edges from startVertex to heap
    for (const edge of graph.getNeighbors(startVertex)) {
        heap.push({ from: startVertex, to: edge.vertex, weight: edge.weight });
    }

    while (!heap.isEmpty() && visited.size < vertices.length) {
        const edge = heap.pop();

        if (visited.has(edge.to)) continue;

        // Add edge to MST
        mst.push(edge);
        totalWeight += edge.weight;
        visited.add(edge.to);

        // Add all edges from newly visited vertex
        for (const nextEdge of graph.getNeighbors(edge.to)) {
            if (!visited.has(nextEdge.vertex)) {
                heap.push({ from: edge.to, to: nextEdge.vertex, weight: nextEdge.weight });
            }
        }
    }

    return { edges: mst, totalWeight };
}

// Topological Sort using DFS
export function topologicalSort(graph) {
    if (!graph.directed) {
        throw new Error("Topological sort requires a directed graph");
    }

    const visited = new Set();
    const stack = [];

    function dfsHelper(vertex) {
        visited.add(vertex);

        for (const { vertex: neighbor } of graph.getNeighbors(vertex)) {
            if (!visited.has(neighbor)) {
                dfsHelper(neighbor);
            }
        }

        stack.push(vertex);
    }

    // Visit all vertices
    for (const vertex of graph.getVertices()) {
        if (!visited.has(vertex)) {
            dfsHelper(vertex);
        }
    }

    return stack.reverse();
}

// Kahn's algorithm for topological sort
export function kahnTopologicalSort(graph) {
    if (!graph.directed) {
        throw new Error("Topological sort requires a directed graph");
    }

    const inDegree = new Map();
    const queue = [];
    const result = [];

    // Calculate in-degrees
    for (const vertex of graph.getVertices()) {
        inDegree.set(vertex, graph.getInDegree(vertex));
        if (inDegree.get(vertex) === 0) {
            queue.push(vertex);
        }
    }

    // Process vertices with 0 in-degree
    while (queue.length > 0) {
        const vertex = queue.shift();
        result.push(vertex);

        for (const { vertex: neighbor } of graph.getNeighbors(vertex)) {
            inDegree.set(neighbor, inDegree.get(neighbor) - 1);
            if (inDegree.get(neighbor) === 0) {
                queue.push(neighbor);
            }
        }
    }

    // Check for cycles
    if (result.length !== graph.getVertexCount()) {
        throw new Error("Graph contains a cycle");
    }

    return result;
}

// Detect cycle in undirected graph using DFS
export function hasCycleUndirected(graph) {
    if (graph.directed) {
        throw new Error("Use hasCycleDirected for directed graphs");
    }

    const visited = new Set();

    function dfsHelper(vertex, parent) {
        visited.add(vertex);

        for (const { vertex: neighbor } of graph.getNeighbors(vertex)) {
            if (!visited.has(neighbor)) {
                if (dfsHelper(neighbor, vertex)) return true;
            } else if (neighbor !== parent) {
                return true;
            }
        }

        return false;
    }

    for (const vertex of graph.getVertices()) {
        if (!visited.has(vertex)) {
            if (dfsHelper(vertex, null)) return true;
        }
    }

    return false;
}

// Detect cycle in directed graph using DFS
export function hasCycleDirected(graph) {
    if (!graph.directed) {
        throw new Error("Use hasCycleUndirected for undirected graphs");
    }

    const WHITE = 0; // Not visited
    const GRAY = 1;  // Currently visiting
    const BLACK = 2; // Finished visiting

    const colors = new Map();

    // Initialize all vertices as white
    for (const vertex of graph.getVertices()) {
        colors.set(vertex, WHITE);
    }

    function dfsHelper(vertex) {
        colors.set(vertex, GRAY);

        for (const { vertex: neighbor } of graph.getNeighbors(vertex)) {
            if (colors.get(neighbor) === GRAY) {
                return true; // Back edge found
            }
            if (colors.get(neighbor) === WHITE) {
                if (dfsHelper(neighbor)) return true;
            }
        }

        colors.set(vertex, BLACK);
        return false;
    }

    for (const vertex of graph.getVertices()) {
        if (colors.get(vertex) === WHITE) {
            if (dfsHelper(vertex)) return true;
        }
    }

    return false;
}

// Find strongly connected components using Kosaraju's algorithm
export function stronglyConnectedComponents(graph) {
    if (!graph.directed) {
        throw new Error("SCC requires a directed graph");
    }

    const visited = new Set();
    const stack = [];

    // First DFS to get finish times
    function dfs1(vertex) {
        visited.add(vertex);

        for (const { vertex: neighbor } of graph.getNeighbors(vertex)) {
            if (!visited.has(neighbor)) {
                dfs1(neighbor);
            }
        }

        stack.push(vertex);
    }

    // Create transpose graph
    const transpose = new Graph(true);
    for (const vertex of graph.getVertices()) {
        transpose.addVertex(vertex);
    }
    for (const [from, edges] of graph.adjacencyList) {
        for (const { vertex: to, weight } of edges) {
            transpose.addEdge(to, from, weight);
        }
    }

    // Second DFS on transpose
    function dfs2(vertex, component) {
        visited.add(vertex);
        component.push(vertex);

        for (const { vertex: neighbor } of transpose.getNeighbors(vertex)) {
            if (!visited.has(neighbor)) {
                dfs2(neighbor, component);
            }
        }
    }

    // First pass
    for (const vertex of graph.getVertices()) {
        if (!visited.has(vertex)) {
            dfs1(vertex);
        }
    }

    // Second pass
    visited.clear();
    const components = [];

    while (stack.length > 0) {
        const vertex = stack.pop();
        if (!visited.has(vertex)) {
            const component = [];
            dfs2(vertex, component);
            components.push(component);
        }
    }

    return components;
}

// Check if graph is bipartite using BFS coloring
export function isBipartite(graph) {
    const colors = new Map();

    function bfsColoring(start) {
        const queue = [start];
        colors.set(start, 0);

        while (queue.length > 0) {
            const vertex = queue.shift();
            const currentColor = colors.get(vertex);

            for (const { vertex: neighbor } of graph.getNeighbors(vertex)) {
                if (!colors.has(neighbor)) {
                    colors.set(neighbor, 1 - currentColor);
                    queue.push(neighbor);
                } else if (colors.get(neighbor) === currentColor) {
                    return false;
                }
            }
        }

        return true;
    }

    for (const vertex of graph.getVertices()) {
        if (!colors.has(vertex)) {
            if (!bfsColoring(vertex)) return false;
        }
    }

    return true;
}

// Find bridges in undirected graph (edges whose removal increases components)
export function findBridges(graph) {
    if (graph.directed) {
        throw new Error("Bridge finding requires undirected graph");
    }

    const bridges = [];
    const visited = new Set();
    const disc = new Map();
    const low = new Map();
    const parent = new Map();
    let time = 0;

    function dfsHelper(vertex) {
        visited.add(vertex);
        disc.set(vertex, time);
        low.set(vertex, time);
        time++;

        for (const { vertex: neighbor } of graph.getNeighbors(vertex)) {
            if (!visited.has(neighbor)) {
                parent.set(neighbor, vertex);
                dfsHelper(neighbor);

                low.set(vertex, Math.min(low.get(vertex), low.get(neighbor)));

                // Check if edge is a bridge
                if (low.get(neighbor) > disc.get(vertex)) {
                    bridges.push([vertex, neighbor]);
                }
            } else if (neighbor !== parent.get(vertex)) {
                low.set(vertex, Math.min(low.get(vertex), disc.get(neighbor)));
            }
        }
    }

    for (const vertex of graph.getVertices()) {
        if (!visited.has(vertex)) {
            dfsHelper(vertex);
        }
    }

    return bridges;
}

// Find articulation points (vertices whose removal increases components)
export function findArticulationPoints(graph) {
    if (graph.directed) {
        throw new Error("Articulation point finding requires undirected graph");
    }

    const articulationPoints = new Set();
    const visited = new Set();
    const disc = new Map();
    const low = new Map();
    const parent = new Map();
    let time = 0;

    function dfsHelper(vertex) {
        let children = 0;
        visited.add(vertex);
        disc.set(vertex, time);
        low.set(vertex, time);
        time++;

        for (const { vertex: neighbor } of graph.getNeighbors(vertex)) {
            if (!visited.has(neighbor)) {
                children++;
                parent.set(neighbor, vertex);
                dfsHelper(neighbor);

                low.set(vertex, Math.min(low.get(vertex), low.get(neighbor)));

                // Check if vertex is an articulation point
                if (parent.get(vertex) === undefined && children > 1) {
                    articulationPoints.add(vertex);
                }

                if (parent.get(vertex) !== undefined && low.get(neighbor) >= disc.get(vertex)) {
                    articulationPoints.add(vertex);
                }
            } else if (neighbor !== parent.get(vertex)) {
                low.set(vertex, Math.min(low.get(vertex), disc.get(neighbor)));
            }
        }
    }

    for (const vertex of graph.getVertices()) {
        if (!visited.has(vertex)) {
            parent.set(vertex, undefined);
            dfsHelper(vertex);
        }
    }

    return Array.from(articulationPoints);
}

// Graph coloring using greedy algorithm
export function graphColoring(graph, maxColors = null) {
    const colors = new Map();
    const vertices = graph.getVertices();

    // Sort vertices by degree (heuristic for better coloring)
    vertices.sort((a, b) => {
        const degA = graph.directed ? graph.getOutDegree(a) : graph.getDegree(a);
        const degB = graph.directed ? graph.getOutDegree(b) : graph.getDegree(b);
        return degB - degA;
    });

    for (const vertex of vertices) {
        const neighborColors = new Set();

        for (const { vertex: neighbor } of graph.getNeighbors(vertex)) {
            if (colors.has(neighbor)) {
                neighborColors.add(colors.get(neighbor));
            }
        }

        // Find the smallest color not used by neighbors
        let color = 0;
        while (neighborColors.has(color)) {
            color++;
            if (maxColors !== null && color >= maxColors) {
                throw new Error(`Cannot color graph with ${maxColors} colors`);
            }
        }

        colors.set(vertex, color);
    }

    const chromaticNumber = Math.max(...colors.values()) + 1;

    return { colors, chromaticNumber };
}

// Find Eulerian path/circuit
export function findEulerianPath(graph) {
    // Check if Eulerian path exists
    let oddDegreeVertices = 0;
    let startVertex = null;

    for (const vertex of graph.getVertices()) {
        const degree = graph.directed ?
            graph.getOutDegree(vertex) - graph.getInDegree(vertex) :
            graph.getDegree(vertex);

        if (!graph.directed && degree % 2 === 1) {
            oddDegreeVertices++;
            if (startVertex === null) startVertex = vertex;
        } else if (graph.directed && Math.abs(degree) > 1) {
            return null; // No Eulerian path exists
        } else if (graph.directed && degree === 1) {
            startVertex = vertex;
        }
    }

    if (!graph.directed && oddDegreeVertices > 2) {
        return null; // No Eulerian path exists
    }

    if (startVertex === null) {
        startVertex = graph.getVertices()[0];
    }

    // Hierholzer's algorithm
    const tempGraph = graph.clone();
    const stack = [startVertex];
    const path = [];

    while (stack.length > 0) {
        const vertex = stack[stack.length - 1];
        const neighbors = tempGraph.getNeighbors(vertex);

        if (neighbors.length > 0) {
            const next = neighbors[0].vertex;
            tempGraph.removeEdge(vertex, next);
            stack.push(next);
        } else {
            path.push(stack.pop());
        }
    }

    return path.reverse();
}

// Find Hamiltonian path using backtracking
export function findHamiltonianPath(graph, startVertex = null) {
    const vertices = graph.getVertices();
    const n = vertices.length;

    if (n === 0) return [];
    if (startVertex === null) startVertex = vertices[0];

    const path = [startVertex];
    const visited = new Set([startVertex]);

    function backtrack(current) {
        if (path.length === n) return true;

        for (const { vertex: neighbor } of graph.getNeighbors(current)) {
            if (!visited.has(neighbor)) {
                path.push(neighbor);
                visited.add(neighbor);

                if (backtrack(neighbor)) return true;

                path.pop();
                visited.delete(neighbor);
            }
        }

        return false;
    }

    if (backtrack(startVertex)) {
        return path;
    }

    // Try other starting vertices
    for (const vertex of vertices) {
        if (vertex !== startVertex) {
            path.length = 0;
            path.push(vertex);
            visited.clear();
            visited.add(vertex);

            if (backtrack(vertex)) {
                return path;
            }
        }
    }

    return null;
}

// Maximum flow using Ford-Fulkerson with BFS (Edmonds-Karp)
export function maxFlow(graph, source, sink) {
    if (!graph.directed) {
        throw new Error("Max flow requires a directed graph");
    }

    // Create residual graph
    const residual = new Graph(true);
    for (const vertex of graph.getVertices()) {
        residual.addVertex(vertex);
    }

    const capacity = new Map();
    for (const [from, edges] of graph.adjacencyList) {
        for (const { vertex: to, weight } of edges) {
            residual.addEdge(from, to, weight);
            residual.addEdge(to, from, 0);
            capacity.set(`${from}-${to}`, weight);
            capacity.set(`${to}-${from}`, 0);
        }
    }

    // BFS to find augmenting path
    function bfs(source, sink, parent) {
        const visited = new Set([source]);
        const queue = [source];

        while (queue.length > 0) {
            const vertex = queue.shift();

            for (const { vertex: next, weight } of residual.getNeighbors(vertex)) {
                if (!visited.has(next) && weight > 0) {
                    visited.add(next);
                    parent.set(next, vertex);
                    if (next === sink) return true;
                    queue.push(next);
                }
            }
        }

        return false;
    }

    let totalFlow = 0;
    const parent = new Map();

    while (bfs(source, sink, parent)) {
        // Find minimum residual capacity along the path
        let pathFlow = Infinity;
        let current = sink;

        while (current !== source) {
            const prev = parent.get(current);
            const edges = residual.getNeighbors(prev);
            for (const edge of edges) {
                if (edge.vertex === current) {
                    pathFlow = Math.min(pathFlow, edge.weight);
                    break;
                }
            }
            current = prev;
        }

        // Update residual capacities
        current = sink;
        while (current !== source) {
            const prev = parent.get(current);

            // Update forward edge
            const forwardEdges = residual.getNeighbors(prev);
            for (let i = 0; i < forwardEdges.length; i++) {
                if (forwardEdges[i].vertex === current) {
                    forwardEdges[i].weight -= pathFlow;
                    break;
                }
            }

            // Update backward edge
            const backwardEdges = residual.getNeighbors(current);
            for (let i = 0; i < backwardEdges.length; i++) {
                if (backwardEdges[i].vertex === prev) {
                    backwardEdges[i].weight += pathFlow;
                    break;
                }
            }

            current = prev;
        }

        totalFlow += pathFlow;
        parent.clear();
    }

    return totalFlow;
}

// Export all functions as a default object for convenience
export default {
    Graph,
    MinHeap,
    UnionFind,
    bfs,
    dfs,
    dfsRecursive,
    dijkstra,
    bellmanFord,
    floydWarshall,
    kruskal,
    prim,
    topologicalSort,
    kahnTopologicalSort,
    hasCycleUndirected,
    hasCycleDirected,
    stronglyConnectedComponents,
    isBipartite,
    findBridges,
    findArticulationPoints,
    graphColoring,
    findEulerianPath,
    findHamiltonianPath,
    maxFlow
};