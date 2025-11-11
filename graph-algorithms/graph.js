/**
 * Comprehensive Graph Data Structure Implementation
 * Supports multiple representations and core graph algorithms
 */

const GraphType = {
    DIRECTED: 'directed',
    UNDIRECTED: 'undirected'
};

const RepresentationType = {
    ADJACENCY_LIST: 'adjacency_list',
    ADJACENCY_MATRIX: 'adjacency_matrix',
    EDGE_LIST: 'edge_list',
    CSR: 'csr'  // Compressed Sparse Row
};

class Graph {
    /**
     * Comprehensive graph implementation supporting multiple representations
     * @param {number} numVertices - Number of vertices
     * @param {string} graphType - DIRECTED or UNDIRECTED
     * @param {boolean} weighted - Whether edges have weights
     * @param {string} representation - Type of representation to use
     */
    constructor(
        numVertices = 0,
        graphType = GraphType.UNDIRECTED,
        weighted = false,
        representation = RepresentationType.ADJACENCY_LIST
    ) {
        this.numVertices = numVertices;
        this.graphType = graphType;
        this.weighted = weighted;
        this.representation = representation;
        this.numEdges = 0;

        // Initialize based on representation type
        if (representation === RepresentationType.ADJACENCY_LIST) {
            this.adjList = new Map();
        } else if (representation === RepresentationType.ADJACENCY_MATRIX) {
            this.adjMatrix = Array(numVertices).fill(null)
                .map(() => Array(numVertices).fill(null));
        } else if (representation === RepresentationType.EDGE_LIST) {
            this.edges = [];
        } else if (representation === RepresentationType.CSR) {
            this.csrValues = [];
            this.csrColIndices = [];
            this.csrRowPtr = [0];
        }
    }

    /**
     * Add a new vertex and return its ID
     */
    addVertex() {
        const vertexId = this.numVertices;
        this.numVertices++;

        if (this.representation === RepresentationType.ADJACENCY_MATRIX) {
            // Expand matrix
            for (let row of this.adjMatrix) {
                row.push(null);
            }
            this.adjMatrix.push(Array(this.numVertices).fill(null));
        } else if (this.representation === RepresentationType.ADJACENCY_LIST) {
            this.adjList.set(vertexId, []);
        }

        return vertexId;
    }

    /**
     * Add an edge from u to v with optional weight
     */
    addEdge(u, v, weight = 1.0) {
        if (u >= this.numVertices || v >= this.numVertices) {
            throw new Error(`Vertex out of range: ${u} or ${v}`);
        }

        this.numEdges++;

        if (this.representation === RepresentationType.ADJACENCY_LIST) {
            if (!this.adjList.has(u)) this.adjList.set(u, []);
            this.adjList.get(u).push([v, weight]);

            if (this.graphType === GraphType.UNDIRECTED) {
                if (!this.adjList.has(v)) this.adjList.set(v, []);
                this.adjList.get(v).push([u, weight]);
            }
        } else if (this.representation === RepresentationType.ADJACENCY_MATRIX) {
            this.adjMatrix[u][v] = weight;
            if (this.graphType === GraphType.UNDIRECTED) {
                this.adjMatrix[v][u] = weight;
            }
        } else if (this.representation === RepresentationType.EDGE_LIST) {
            this.edges.push([u, v, weight]);
            if (this.graphType === GraphType.UNDIRECTED) {
                this.edges.push([v, u, weight]);
            }
        } else if (this.representation === RepresentationType.CSR) {
            throw new Error('CSR edges should be added via buildCSR()');
        }
    }

    /**
     * Build CSR representation from edge list
     */
    buildCSR(edges) {
        if (this.representation !== RepresentationType.CSR) {
            throw new Error('Graph must be CSR type');
        }

        // Sort edges by source vertex
        const sortedEdges = edges.sort((a, b) => a[0] - b[0] || a[1] - b[1]);

        this.csrValues = [];
        this.csrColIndices = [];
        this.csrRowPtr = [0];

        let currentRow = 0;
        for (const [u, v, weight] of sortedEdges) {
            // Fill gaps for vertices with no outgoing edges
            while (currentRow < u) {
                this.csrRowPtr.push(this.csrColIndices.length);
                currentRow++;
            }

            this.csrValues.push(weight);
            this.csrColIndices.push(v);
        }

        // Complete row pointers
        while (currentRow < this.numVertices) {
            this.csrRowPtr.push(this.csrColIndices.length);
            currentRow++;
        }

        this.numEdges = sortedEdges.length;
    }

    /**
     * Get neighbors of vertex u with their edge weights
     */
    getNeighbors(u) {
        if (this.representation === RepresentationType.ADJACENCY_LIST) {
            return this.adjList.get(u) || [];
        } else if (this.representation === RepresentationType.ADJACENCY_MATRIX) {
            const neighbors = [];
            for (let v = 0; v < this.numVertices; v++) {
                if (this.adjMatrix[u][v] !== null) {
                    neighbors.push([v, this.adjMatrix[u][v]]);
                }
            }
            return neighbors;
        } else if (this.representation === RepresentationType.EDGE_LIST) {
            const neighbors = [];
            for (const [src, dst, weight] of this.edges) {
                if (src === u) {
                    neighbors.push([dst, weight]);
                }
            }
            return neighbors;
        } else if (this.representation === RepresentationType.CSR) {
            const start = this.csrRowPtr[u];
            const end = this.csrRowPtr[u + 1];
            const neighbors = [];
            for (let i = start; i < end; i++) {
                neighbors.push([this.csrColIndices[i], this.csrValues[i]]);
            }
            return neighbors;
        }
        return [];
    }

    // === DEPTH-FIRST SEARCH ===

    /**
     * DFS traversal using recursion
     */
    dfsRecursive(start, visited = new Set()) {
        const traversal = [];

        const dfsHelper = (v) => {
            visited.add(v);
            traversal.push(v);

            for (const [neighbor, _] of this.getNeighbors(v)) {
                if (!visited.has(neighbor)) {
                    dfsHelper(neighbor);
                }
            }
        };

        dfsHelper(start);
        return traversal;
    }

    /**
     * DFS traversal using iteration with stack
     */
    dfsIterative(start) {
        const visited = new Set();
        const traversal = [];
        const stack = [start];

        while (stack.length > 0) {
            const v = stack.pop();
            if (!visited.has(v)) {
                visited.add(v);
                traversal.push(v);

                // Add neighbors in reverse order for consistent ordering
                const neighbors = this.getNeighbors(v);
                for (let i = neighbors.length - 1; i >= 0; i--) {
                    const [neighbor, _] = neighbors[i];
                    if (!visited.has(neighbor)) {
                        stack.push(neighbor);
                    }
                }
            }
        }

        return traversal;
    }

    // === BREADTH-FIRST SEARCH ===

    /**
     * BFS traversal
     */
    bfs(start) {
        const visited = new Set([start]);
        const traversal = [];
        const queue = [start];

        while (queue.length > 0) {
            const v = queue.shift();
            traversal.push(v);

            for (const [neighbor, _] of this.getNeighbors(v)) {
                if (!visited.has(neighbor)) {
                    visited.add(neighbor);
                    queue.push(neighbor);
                }
            }
        }

        return traversal;
    }

    // === TOPOLOGICAL SORTING ===

    /**
     * Topological sorting using Kahn's algorithm (BFS-based)
     * Returns null if graph contains a cycle
     */
    topologicalSort() {
        if (this.graphType !== GraphType.DIRECTED) {
            throw new Error('Topological sort only works for directed graphs');
        }

        // Calculate in-degrees
        const inDegree = Array(this.numVertices).fill(0);
        for (let u = 0; u < this.numVertices; u++) {
            for (const [v, _] of this.getNeighbors(u)) {
                inDegree[v]++;
            }
        }

        // Queue with vertices having 0 in-degree
        const queue = [];
        for (let v = 0; v < this.numVertices; v++) {
            if (inDegree[v] === 0) {
                queue.push(v);
            }
        }

        const result = [];

        while (queue.length > 0) {
            const u = queue.shift();
            result.push(u);

            for (const [v, _] of this.getNeighbors(u)) {
                inDegree[v]--;
                if (inDegree[v] === 0) {
                    queue.push(v);
                }
            }
        }

        // Check if all vertices were processed (no cycle)
        return result.length === this.numVertices ? result : null;
    }

    /**
     * Topological sorting using DFS
     */
    topologicalSortDFS() {
        if (this.graphType !== GraphType.DIRECTED) {
            throw new Error('Topological sort only works for directed graphs');
        }

        const visited = new Set();
        const recStack = new Set();
        const result = [];

        const dfsHelper = (v) => {
            visited.add(v);
            recStack.add(v);

            for (const [neighbor, _] of this.getNeighbors(v)) {
                if (!visited.has(neighbor)) {
                    if (!dfsHelper(neighbor)) {
                        return false;
                    }
                } else if (recStack.has(neighbor)) {
                    return false;  // Cycle detected
                }
            }

            recStack.delete(v);
            result.push(v);
            return true;
        };

        for (let v = 0; v < this.numVertices; v++) {
            if (!visited.has(v)) {
                if (!dfsHelper(v)) {
                    return null;  // Cycle detected
                }
            }
        }

        return result.reverse();
    }

    // === CONNECTED COMPONENTS ===

    /**
     * Find all connected components in the graph
     */
    findConnectedComponents() {
        const visited = new Set();
        const components = [];

        for (let v = 0; v < this.numVertices; v++) {
            if (!visited.has(v)) {
                const component = [];
                const stack = [v];

                while (stack.length > 0) {
                    const u = stack.pop();
                    if (!visited.has(u)) {
                        visited.add(u);
                        component.push(u);

                        for (const [neighbor, _] of this.getNeighbors(u)) {
                            if (!visited.has(neighbor)) {
                                stack.push(neighbor);
                            }
                        }
                    }
                }

                components.push(component.sort((a, b) => a - b));
            }
        }

        return components;
    }

    /**
     * Check if graph is connected
     */
    isConnected() {
        if (this.numVertices === 0) return true;
        return this.findConnectedComponents().length === 1;
    }

    // === CYCLE DETECTION ===

    /**
     * Detect cycle in undirected graph using DFS
     */
    hasCycleUndirected() {
        if (this.graphType !== GraphType.UNDIRECTED) {
            throw new Error('This method is for undirected graphs');
        }

        const visited = new Set();

        const dfsHelper = (v, parent) => {
            visited.add(v);

            for (const [neighbor, _] of this.getNeighbors(v)) {
                if (!visited.has(neighbor)) {
                    if (dfsHelper(neighbor, v)) {
                        return true;
                    }
                } else if (neighbor !== parent) {
                    return true;  // Cycle found
                }
            }

            return false;
        };

        for (let v = 0; v < this.numVertices; v++) {
            if (!visited.has(v)) {
                if (dfsHelper(v, -1)) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Detect cycle in directed graph using DFS with recursion stack
     */
    hasCycleDirected() {
        if (this.graphType !== GraphType.DIRECTED) {
            throw new Error('This method is for directed graphs');
        }

        const visited = new Set();
        const recStack = new Set();

        const dfsHelper = (v) => {
            visited.add(v);
            recStack.add(v);

            for (const [neighbor, _] of this.getNeighbors(v)) {
                if (!visited.has(neighbor)) {
                    if (dfsHelper(neighbor)) {
                        return true;
                    }
                } else if (recStack.has(neighbor)) {
                    return true;  // Back edge found
                }
            }

            recStack.delete(v);
            return false;
        };

        for (let v = 0; v < this.numVertices; v++) {
            if (!visited.has(v)) {
                if (dfsHelper(v)) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Detect cycle based on graph type
     */
    hasCycle() {
        if (this.graphType === GraphType.DIRECTED) {
            return this.hasCycleDirected();
        } else {
            return this.hasCycleUndirected();
        }
    }

    // === GRAPH COLORING ===

    /**
     * Graph coloring using greedy algorithm
     * Returns mapping of vertex -> color
     */
    greedyColoring() {
        const colors = new Map();

        for (let v = 0; v < this.numVertices; v++) {
            // Get colors of neighbors
            const neighborColors = new Set();
            for (const [neighbor, _] of this.getNeighbors(v)) {
                if (colors.has(neighbor)) {
                    neighborColors.add(colors.get(neighbor));
                }
            }

            // Find first available color
            let color = 0;
            while (neighborColors.has(color)) {
                color++;
            }

            colors.set(v, color);
        }

        return colors;
    }

    /**
     * Get upper bound on chromatic number
     */
    chromaticNumberUpperBound() {
        const coloring = this.greedyColoring();
        if (coloring.size === 0) return 0;
        return Math.max(...coloring.values()) + 1;
    }

    // === VISUALIZATION ===

    /**
     * Generate ASCII art representation of the graph
     */
    toASCII(maxWidth = 80) {
        const lines = [];
        lines.push('='.repeat(maxWidth));
        lines.push(`Graph: ${this.graphType}, ${this.weighted ? 'weighted' : 'unweighted'}`);
        lines.push(`Representation: ${this.representation}`);
        lines.push(`Vertices: ${this.numVertices}, Edges: ${this.numEdges}`);
        lines.push('='.repeat(maxWidth));
        lines.push('');

        if (this.representation === RepresentationType.ADJACENCY_LIST) {
            lines.push('Adjacency List:');
            for (let v = 0; v < this.numVertices; v++) {
                const neighbors = this.getNeighbors(v);
                if (neighbors.length > 0) {
                    const neighborStr = neighbors.map(([n, w]) =>
                        this.weighted ? `${n}(${w.toFixed(1)})` : String(n)
                    ).join(', ');
                    lines.push(`  ${v} -> [${neighborStr}]`);
                } else {
                    lines.push(`  ${v} -> []`);
                }
            }
        } else if (this.representation === RepresentationType.ADJACENCY_MATRIX) {
            lines.push('Adjacency Matrix:');
            const displaySize = Math.min(this.numVertices, 15);

            // Header
            const header = '    ' + Array.from({length: displaySize}, (_, i) =>
                String(i).padStart(4)).join(' ');
            lines.push(header);
            lines.push('    ' + '-'.repeat(5 * displaySize));

            for (let i = 0; i < displaySize; i++) {
                const rowVals = [];
                for (let j = 0; j < displaySize; j++) {
                    const val = this.adjMatrix[i][j];
                    rowVals.push(val === null ? '   .' : String(val).padStart(4));
                }
                lines.push(`${String(i).padStart(2)} |` + rowVals.join(' '));
            }

            if (this.numVertices > 15) {
                lines.push('  ... (truncated)');
            }
        } else if (this.representation === RepresentationType.EDGE_LIST) {
            lines.push('Edge List:');
            const displayLimit = Math.min(this.edges.length, 50);
            for (let i = 0; i < displayLimit; i++) {
                const [u, v, w] = this.edges[i];
                if (this.weighted) {
                    lines.push(`  ${i}: ${u} -> ${v} (weight: ${w.toFixed(1)})`);
                } else {
                    lines.push(`  ${i}: ${u} -> ${v}`);
                }
            }
            if (this.edges.length > 50) {
                lines.push(`  ... (${this.edges.length - 50} more edges)`);
            }
        } else if (this.representation === RepresentationType.CSR) {
            lines.push('CSR (Compressed Sparse Row):');
            const valuesStr = this.csrValues.slice(0, 20).join(', ');
            const colStr = this.csrColIndices.slice(0, 20).join(', ');
            const rowStr = this.csrRowPtr.slice(0, 20).join(', ');

            lines.push(`  Values: [${valuesStr}${this.csrValues.length > 20 ? ', ...' : ''}]`);
            lines.push(`  Col Indices: [${colStr}${this.csrColIndices.length > 20 ? ', ...' : ''}]`);
            lines.push(`  Row Ptrs: [${rowStr}${this.csrRowPtr.length > 20 ? ', ...' : ''}]`);
        }

        lines.push('');
        lines.push('='.repeat(maxWidth));

        return lines.join('\n');
    }

    toString() {
        return this.toASCII();
    }

    // === MEMORY AND PERFORMANCE ANALYSIS ===

    /**
     * Estimate memory usage of current representation
     */
    memoryUsage() {
        const stats = {
            representation: this.representation,
            vertices: this.numVertices,
            edges: this.numEdges
        };

        if (this.representation === RepresentationType.ADJACENCY_LIST) {
            // Rough estimation in JavaScript
            let bytes = 100; // Map overhead
            for (const [v, neighbors] of this.adjList) {
                bytes += 8 + neighbors.length * 24; // Array overhead + entries
            }
            stats.bytes = bytes;
            stats.avgBytesPerEdge = bytes / Math.max(this.numEdges, 1);
        } else if (this.representation === RepresentationType.ADJACENCY_MATRIX) {
            stats.bytes = this.numVertices * this.numVertices * 8;
            stats.spaceComplexity = `O(V²) = O(${this.numVertices}²)`;
        } else if (this.representation === RepresentationType.EDGE_LIST) {
            stats.bytes = this.edges.length * 24;
            stats.spaceComplexity = `O(E) = O(${this.numEdges})`;
        } else if (this.representation === RepresentationType.CSR) {
            stats.bytes = (this.csrValues.length + this.csrColIndices.length +
                         this.csrRowPtr.length) * 8;
            stats.spaceComplexity = `O(V+E) = O(${this.numVertices}+${this.numEdges})`;
        }

        return stats;
    }
}

// === GRAPH GENERATORS ===

class GraphGenerator {
    /**
     * Generate a complete graph with n vertices
     */
    static completeGraph(n, graphType = GraphType.UNDIRECTED,
                        representation = RepresentationType.ADJACENCY_LIST) {
        const g = new Graph(n, graphType, false, representation);

        if (representation === RepresentationType.CSR) {
            const edges = [];
            for (let i = 0; i < n; i++) {
                for (let j = 0; j < n; j++) {
                    if (i !== j) {
                        edges.push([i, j, 1.0]);
                    }
                }
            }
            g.buildCSR(edges);
        } else {
            for (let i = 0; i < n; i++) {
                for (let j = i + 1; j < n; j++) {
                    g.addEdge(i, j);
                    if (graphType === GraphType.DIRECTED) {
                        g.addEdge(j, i);
                    }
                }
            }
        }

        return g;
    }

    /**
     * Generate a cycle graph with n vertices
     */
    static cycleGraph(n, graphType = GraphType.UNDIRECTED,
                     representation = RepresentationType.ADJACENCY_LIST) {
        const g = new Graph(n, graphType, false, representation);

        if (representation === RepresentationType.CSR) {
            const edges = [];
            for (let i = 0; i < n; i++) {
                edges.push([i, (i + 1) % n, 1.0]);
                if (graphType === GraphType.UNDIRECTED) {
                    edges.push([(i + 1) % n, i, 1.0]);
                }
            }
            g.buildCSR(edges);
        } else {
            for (let i = 0; i < n; i++) {
                g.addEdge(i, (i + 1) % n);
            }
        }

        return g;
    }

    /**
     * Generate random graph with Erdős-Rényi model
     */
    static randomGraph(n, edgeProbability,
                      graphType = GraphType.UNDIRECTED,
                      weighted = false,
                      representation = RepresentationType.ADJACENCY_LIST) {
        const g = new Graph(n, graphType, weighted, representation);
        const edges = [];

        for (let i = 0; i < n; i++) {
            const start = graphType === GraphType.UNDIRECTED ? i + 1 : 0;
            for (let j = start; j < n; j++) {
                if (i !== j && Math.random() < edgeProbability) {
                    const weight = weighted ? Math.random() * 9 + 1 : 1.0;
                    edges.push([i, j, weight]);
                }
            }
        }

        if (representation === RepresentationType.CSR) {
            if (graphType === GraphType.UNDIRECTED) {
                const reversed = edges.map(([u, v, w]) => [v, u, w]);
                edges.push(...reversed);
            }
            g.buildCSR(edges.sort((a, b) => a[0] - b[0] || a[1] - b[1]));
        } else {
            for (const [u, v, w] of edges) {
                g.addEdge(u, v, w);
            }
        }

        return g;
    }

    /**
     * Generate a random Directed Acyclic Graph (DAG)
     */
    static dag(n, edgeProbability,
              representation = RepresentationType.ADJACENCY_LIST) {
        const g = new Graph(n, GraphType.DIRECTED, false, representation);
        const edges = [];

        for (let i = 0; i < n; i++) {
            for (let j = i + 1; j < n; j++) {
                if (Math.random() < edgeProbability) {
                    edges.push([i, j, 1.0]);
                }
            }
        }

        if (representation === RepresentationType.CSR) {
            g.buildCSR(edges);
        } else {
            for (const [u, v, w] of edges) {
                g.addEdge(u, v, w);
            }
        }

        return g;
    }
}

// === DEMO AND TESTING ===

function demo() {
    console.log('='.repeat(80));
    console.log('GRAPH DATA STRUCTURES AND ALGORITHMS DEMO');
    console.log('='.repeat(80));
    console.log();

    // Demo 1: Adjacency List
    console.log('1. ADJACENCY LIST REPRESENTATION');
    console.log('-'.repeat(80));
    const g1 = new Graph(5, GraphType.UNDIRECTED, false, RepresentationType.ADJACENCY_LIST);
    g1.addEdge(0, 1);
    g1.addEdge(0, 4);
    g1.addEdge(1, 2);
    g1.addEdge(1, 3);
    g1.addEdge(1, 4);
    g1.addEdge(2, 3);
    g1.addEdge(3, 4);
    console.log(g1.toASCII());
    console.log();

    // Demo 2: DFS and BFS
    console.log('2. GRAPH TRAVERSAL');
    console.log('-'.repeat(80));
    console.log(`DFS Recursive from 0: ${g1.dfsRecursive(0)}`);
    console.log(`DFS Iterative from 0: ${g1.dfsIterative(0)}`);
    console.log(`BFS from 0: ${g1.bfs(0)}`);
    console.log();

    // Demo 3: Connected Components
    console.log('3. CONNECTED COMPONENTS');
    console.log('-'.repeat(80));
    const g2 = new Graph(7, GraphType.UNDIRECTED);
    g2.addEdge(0, 1);
    g2.addEdge(1, 2);
    g2.addEdge(3, 4);
    g2.addEdge(5, 6);
    const components = g2.findConnectedComponents();
    console.log(`Components: ${JSON.stringify(components)}`);
    console.log(`Is connected: ${g2.isConnected()}`);
    console.log();

    // Demo 4: Cycle Detection
    console.log('4. CYCLE DETECTION');
    console.log('-'.repeat(80));
    console.log(`Graph g1 has cycle: ${g1.hasCycle()}`);
    const g3 = new Graph(3, GraphType.UNDIRECTED);
    g3.addEdge(0, 1);
    g3.addEdge(1, 2);
    console.log(`Linear graph has cycle: ${g3.hasCycle()}`);
    console.log();

    // Demo 5: Topological Sort
    console.log('5. TOPOLOGICAL SORTING');
    console.log('-'.repeat(80));
    const dag = GraphGenerator.dag(6, 0.3);
    console.log(dag.toASCII());
    const topo = dag.topologicalSort();
    console.log(`Topological order: ${topo}`);
    const topoDFS = dag.topologicalSortDFS();
    console.log(`Topological order (DFS): ${topoDFS}`);
    console.log();

    // Demo 6: Graph Coloring
    console.log('6. GRAPH COLORING');
    console.log('-'.repeat(80));
    const coloring = g1.greedyColoring();
    console.log(`Greedy coloring: ${JSON.stringify([...coloring])}`);
    console.log(`Chromatic number (upper bound): ${g1.chromaticNumberUpperBound()}`);
    console.log();

    // Demo 7: Different Representations
    console.log('7. ADJACENCY MATRIX REPRESENTATION');
    console.log('-'.repeat(80));
    const g4 = new Graph(5, GraphType.DIRECTED, true, RepresentationType.ADJACENCY_MATRIX);
    g4.addEdge(0, 1, 2.5);
    g4.addEdge(0, 2, 1.0);
    g4.addEdge(1, 3, 3.0);
    g4.addEdge(2, 3, 1.5);
    g4.addEdge(3, 4, 2.0);
    console.log(g4.toASCII());
    console.log();

    // Demo 8: Performance Comparison
    console.log('8. MEMORY USAGE ANALYSIS');
    console.log('-'.repeat(80));
    const sizes = [10, 50, 100];
    for (const size of sizes) {
        const gList = GraphGenerator.randomGraph(size, 0.3, GraphType.UNDIRECTED,
                                                 false, RepresentationType.ADJACENCY_LIST);
        const gMatrix = GraphGenerator.randomGraph(size, 0.3, GraphType.UNDIRECTED,
                                                   false, RepresentationType.ADJACENCY_MATRIX);

        const memList = gList.memoryUsage();
        const memMatrix = gMatrix.memoryUsage();

        console.log(`\nGraph size: ${size} vertices`);
        console.log(`  Adjacency List: ~${memList.bytes} bytes`);
        console.log(`  Adjacency Matrix: ~${memMatrix.bytes} bytes`);
    }
    console.log();

    // Demo 9: Graph Generators
    console.log('9. GRAPH GENERATORS');
    console.log('-'.repeat(80));
    const complete = GraphGenerator.completeGraph(5);
    console.log('Complete graph K5:');
    console.log(complete.toASCII());
    console.log();

    const cycle = GraphGenerator.cycleGraph(6);
    console.log('Cycle graph C6:');
    console.log(cycle.toASCII());
    console.log();
}

// Run demo if executed directly
if (typeof require !== 'undefined' && require.main === module) {
    demo();
}

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Graph, GraphGenerator, GraphType, RepresentationType };
}
