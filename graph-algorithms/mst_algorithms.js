/**
 * Comprehensive Minimum Spanning Tree (MST) Algorithms
 * =====================================================
 *
 * Implements three classic MST algorithms with various optimizations:
 * 1. Kruskal's Algorithm with Union-Find (path compression + union by rank)
 * 2. Prim's Algorithm with multiple priority queue implementations
 * 3. Borůvka's Algorithm (parallel-friendly)
 *
 * Features:
 * - Support for disconnected graphs (Minimum Spanning Forest)
 * - Multiple priority queue implementations for Prim's
 * - Visualization of MST construction
 * - Real-world applications (network design)
 * - Performance comparison
 *
 * Time Complexities:
 * - Kruskal's: O(E log E) or O(E log V)
 * - Prim's (Binary Heap): O((V+E) log V)
 * - Borůvka's: O(E log V)
 *
 * @author Claude Code
 * @date 2025
 */

class MinHeap {
    /**
     * Binary min-heap for Prim's algorithm
     */
    constructor() {
        this.heap = [];
    }

    push(item) {
        this.heap.push(item);
        this._bubbleUp(this.heap.length - 1);
    }

    pop() {
        if (this.heap.length === 0) return null;
        if (this.heap.length === 1) return this.heap.pop();

        const min = this.heap[0];
        this.heap[0] = this.heap.pop();
        this._bubbleDown(0);
        return min;
    }

    isEmpty() {
        return this.heap.length === 0;
    }

    _bubbleUp(index) {
        while (index > 0) {
            const parentIndex = Math.floor((index - 1) / 2);
            if (this.heap[parentIndex].weight <= this.heap[index].weight) break;

            [this.heap[parentIndex], this.heap[index]] =
                [this.heap[index], this.heap[parentIndex]];
            index = parentIndex;
        }
    }

    _bubbleDown(index) {
        const length = this.heap.length;

        while (true) {
            let smallest = index;
            const leftChild = 2 * index + 1;
            const rightChild = 2 * index + 2;

            if (leftChild < length && this.heap[leftChild].weight < this.heap[smallest].weight) {
                smallest = leftChild;
            }

            if (rightChild < length && this.heap[rightChild].weight < this.heap[smallest].weight) {
                smallest = rightChild;
            }

            if (smallest === index) break;

            [this.heap[index], this.heap[smallest]] =
                [this.heap[smallest], this.heap[index]];
            index = smallest;
        }
    }
}

class UnionFind {
    /**
     * Union-Find (Disjoint Set Union) data structure
     *
     * Implements path compression and union by rank for near O(1) operations.
     * Essential for Kruskal's algorithm.
     *
     * Time Complexity:
     * - find(): O(α(n)) amortized, where α is inverse Ackermann function
     * - union(): O(α(n)) amortized
     *
     * Space Complexity: O(n)
     */
    constructor(n) {
        this.parent = Array.from({ length: n }, (_, i) => i);
        this.rank = Array(n).fill(0);
        this.componentCount = n;
    }

    /**
     * Find the representative (root) of the set containing x
     * Uses path compression for optimization
     */
    find(x) {
        if (this.parent[x] !== x) {
            this.parent[x] = this.find(this.parent[x]); // Path compression
        }
        return this.parent[x];
    }

    /**
     * Union the sets containing x and y
     * Uses union by rank for optimization
     *
     * @returns {boolean} True if union was performed
     */
    union(x, y) {
        let px = this.find(x);
        let py = this.find(y);

        if (px === py) return false; // Already in same set

        // Union by rank
        if (this.rank[px] < this.rank[py]) {
            [px, py] = [py, px];
        }

        this.parent[py] = px;
        if (this.rank[px] === this.rank[py]) {
            this.rank[px]++;
        }

        this.componentCount--;
        return true;
    }

    connected(x, y) {
        return this.find(x) === this.find(y);
    }

    getComponentCount() {
        return this.componentCount;
    }
}

class Edge {
    /**
     * Represents a weighted edge in a graph
     */
    constructor(u, v, weight) {
        this.u = u;
        this.v = v;
        this.weight = weight;
    }

    toString() {
        return `Edge(${this.u}, ${this.v}, ${this.weight})`;
    }
}

class MSTAlgorithms {
    /**
     * Collection of Minimum Spanning Tree algorithms
     */
    constructor(numVertices, edges) {
        this.numVertices = numVertices;
        this.edges = edges.map(([u, v, w]) => new Edge(u, v, w));
        this.adjList = this._buildAdjacencyList();
    }

    _buildAdjacencyList() {
        const adj = Array.from({ length: this.numVertices }, () => []);
        for (const edge of this.edges) {
            adj[edge.u].push({ v: edge.v, weight: edge.weight });
            adj[edge.v].push({ v: edge.u, weight: edge.weight });
        }
        return adj;
    }

    // ========================================================================
    // KRUSKAL'S ALGORITHM
    // ========================================================================

    /**
     * Kruskal's Algorithm for MST/MSF
     *
     * Strategy: Sort edges by weight, add edges that don't create cycles
     * Uses Union-Find to efficiently detect cycles
     *
     * Time Complexity: O(E log E) or O(E log V)
     * Space Complexity: O(V + E)
     *
     * @param {boolean} returnForest - If true, handles disconnected graphs
     * @returns {Object} { mstEdges, totalWeight, forest }
     */
    kruskal(returnForest = false) {
        // Sort edges by weight - O(E log E)
        const sortedEdges = [...this.edges].sort((a, b) => a.weight - b.weight);

        const uf = new UnionFind(this.numVertices);
        const mstEdges = [];
        let totalWeight = 0;

        for (const edge of sortedEdges) {
            if (uf.union(edge.u, edge.v)) {
                mstEdges.push(edge);
                totalWeight += edge.weight;

                // Early termination for connected graph
                if (!returnForest && mstEdges.length === this.numVertices - 1) {
                    break;
                }
            }
        }

        const forest = returnForest ? this._buildForest(mstEdges) : [];

        return { mstEdges, totalWeight, forest };
    }

    /**
     * Kruskal's algorithm with step-by-step visualization data
     */
    kruskalWithVisualization() {
        const sortedEdges = [...this.edges].sort((a, b) => a.weight - b.weight);
        const uf = new UnionFind(this.numVertices);
        const mstEdges = [];
        let totalWeight = 0;
        const steps = [];

        for (let i = 0; i < sortedEdges.length; i++) {
            const edge = sortedEdges[i];
            const step = {
                iteration: i,
                edgeConsidered: edge,
                action: '',
                mstSoFar: [...mstEdges],
                totalWeight: totalWeight
            };

            if (uf.union(edge.u, edge.v)) {
                mstEdges.push(edge);
                totalWeight += edge.weight;
                step.action = 'added';
            } else {
                step.action = 'rejected (creates cycle)';
            }

            steps.push(step);

            if (mstEdges.length === this.numVertices - 1) {
                break;
            }
        }

        return { mstEdges, totalWeight, steps };
    }

    // ========================================================================
    // PRIM'S ALGORITHM
    // ========================================================================

    /**
     * Prim's Algorithm for MST
     *
     * Strategy: Grow tree from starting vertex, always add minimum weight edge
     * that connects tree to non-tree vertex
     *
     * Time Complexity: O((V+E) log V) with binary heap
     * Space Complexity: O(V + E)
     *
     * @param {number} start - Starting vertex
     * @returns {Object} { mstEdges, totalWeight }
     */
    prim(start = 0) {
        const mstEdges = [];
        let totalWeight = 0;
        const visited = new Set([start]);

        const pq = new MinHeap();

        // Add edges from start vertex
        for (const { v, weight } of this.adjList[start]) {
            pq.push({ weight, u: start, v });
        }

        while (!pq.isEmpty() && visited.size < this.numVertices) {
            const { weight, u, v } = pq.pop();

            if (visited.has(v)) continue;

            // Add edge to MST
            visited.add(v);
            mstEdges.push(new Edge(u, v, weight));
            totalWeight += weight;

            // Add edges from newly added vertex
            for (const { v: neighbor, weight: edgeWeight } of this.adjList[v]) {
                if (!visited.has(neighbor)) {
                    pq.push({ weight: edgeWeight, u: v, v: neighbor });
                }
            }
        }

        return { mstEdges, totalWeight };
    }

    /**
     * Prim's algorithm using simple array (O(V²) for dense graphs)
     */
    primSimpleArray(start = 0) {
        const mstEdges = [];
        let totalWeight = 0;
        const visited = Array(this.numVertices).fill(false);
        const minWeight = Array(this.numVertices).fill(Infinity);
        const parent = Array(this.numVertices).fill(-1);

        minWeight[start] = 0;

        for (let count = 0; count < this.numVertices; count++) {
            // Find minimum weight unvisited vertex - O(V)
            let u = -1;
            for (let v = 0; v < this.numVertices; v++) {
                if (!visited[v] && (u === -1 || minWeight[v] < minWeight[u])) {
                    u = v;
                }
            }

            if (minWeight[u] === Infinity) break; // Disconnected graph

            visited[u] = true;

            // Add edge to MST (skip first vertex)
            if (parent[u] !== -1) {
                mstEdges.push(new Edge(parent[u], u, minWeight[u]));
                totalWeight += minWeight[u];
            }

            // Update neighbors
            for (const { v, weight } of this.adjList[u]) {
                if (!visited[v] && weight < minWeight[v]) {
                    minWeight[v] = weight;
                    parent[v] = u;
                }
            }
        }

        return { mstEdges, totalWeight };
    }

    /**
     * Prim's algorithm with step-by-step visualization
     */
    primWithVisualization(start = 0) {
        const mstEdges = [];
        let totalWeight = 0;
        const visited = new Set([start]);
        const steps = [];

        const pq = new MinHeap();
        for (const { v, weight } of this.adjList[start]) {
            pq.push({ weight, u: start, v });
        }

        let iteration = 0;
        while (!pq.isEmpty() && visited.size < this.numVertices) {
            const { weight, u, v } = pq.pop();

            const step = {
                iteration: iteration++,
                edgeConsidered: new Edge(u, v, weight),
                visited: new Set(visited),
                action: '',
                mstSoFar: [...mstEdges],
                totalWeight: totalWeight
            };

            if (visited.has(v)) {
                step.action = 'rejected (already in tree)';
            } else {
                visited.add(v);
                mstEdges.push(new Edge(u, v, weight));
                totalWeight += weight;
                step.action = 'added';

                // Add new edges
                for (const { v: neighbor, weight: edgeWeight } of this.adjList[v]) {
                    if (!visited.has(neighbor)) {
                        pq.push({ weight: edgeWeight, u: v, v: neighbor });
                    }
                }
            }

            steps.push(step);
        }

        return { mstEdges, totalWeight, steps };
    }

    // ========================================================================
    // BORŮVKA'S ALGORITHM
    // ========================================================================

    /**
     * Borůvka's (Sollin's) Algorithm for MST
     *
     * Strategy: In each phase, find minimum weight edge for each component,
     * add all such edges simultaneously (parallel-friendly)
     *
     * Time Complexity: O(E log V)
     * Space Complexity: O(V + E)
     *
     * @returns {Object} { mstEdges, totalWeight }
     */
    boruvka() {
        const uf = new UnionFind(this.numVertices);
        const mstEdges = [];
        let totalWeight = 0;
        let numComponents = this.numVertices;

        while (numComponents > 1) {
            const cheapest = Array(this.numVertices).fill(-1);

            // Find cheapest edge from each component
            for (let i = 0; i < this.edges.length; i++) {
                const edge = this.edges[i];
                const uRoot = uf.find(edge.u);
                const vRoot = uf.find(edge.v);

                if (uRoot === vRoot) continue; // Same component

                // Check if this is cheapest for component of u
                if (cheapest[uRoot] === -1 ||
                    edge.weight < this.edges[cheapest[uRoot]].weight) {
                    cheapest[uRoot] = i;
                }

                // Check if this is cheapest for component of v
                if (cheapest[vRoot] === -1 ||
                    edge.weight < this.edges[cheapest[vRoot]].weight) {
                    cheapest[vRoot] = i;
                }
            }

            // Add all cheapest edges
            let addedAny = false;
            for (let i = 0; i < this.numVertices; i++) {
                if (cheapest[i] !== -1) {
                    const edge = this.edges[cheapest[i]];
                    if (uf.union(edge.u, edge.v)) {
                        mstEdges.push(edge);
                        totalWeight += edge.weight;
                        numComponents--;
                        addedAny = true;
                    }
                }
            }

            if (!addedAny) break; // Disconnected graph or done
        }

        return { mstEdges, totalWeight };
    }

    /**
     * Borůvka's algorithm with step-by-step visualization
     */
    boruvkaWithVisualization() {
        const uf = new UnionFind(this.numVertices);
        const mstEdges = [];
        let totalWeight = 0;
        const steps = [];
        let numComponents = this.numVertices;
        let phase = 0;

        while (numComponents > 1) {
            const cheapest = Array(this.numVertices).fill(-1);

            // Find cheapest edges
            for (let i = 0; i < this.edges.length; i++) {
                const edge = this.edges[i];
                const uRoot = uf.find(edge.u);
                const vRoot = uf.find(edge.v);

                if (uRoot === vRoot) continue;

                if (cheapest[uRoot] === -1 ||
                    edge.weight < this.edges[cheapest[uRoot]].weight) {
                    cheapest[uRoot] = i;
                }

                if (cheapest[vRoot] === -1 ||
                    edge.weight < this.edges[cheapest[vRoot]].weight) {
                    cheapest[vRoot] = i;
                }
            }

            // Collect edges to add in this phase
            const phaseEdges = [];
            for (let i = 0; i < this.numVertices; i++) {
                if (cheapest[i] !== -1) {
                    const edge = this.edges[cheapest[i]];
                    if (uf.union(edge.u, edge.v)) {
                        phaseEdges.push(edge);
                        mstEdges.push(edge);
                        totalWeight += edge.weight;
                        numComponents--;
                    }
                }
            }

            steps.push({
                phase: phase++,
                edgesAdded: phaseEdges,
                numComponents,
                mstSoFar: [...mstEdges],
                totalWeight
            });

            if (phaseEdges.length === 0) break;
        }

        return { mstEdges, totalWeight, steps };
    }

    // ========================================================================
    // MINIMUM SPANNING FOREST (for disconnected graphs)
    // ========================================================================

    /**
     * Find Minimum Spanning Forest for potentially disconnected graph
     */
    minimumSpanningForest(algorithm = 'kruskal') {
        if (algorithm === 'kruskal') {
            const { mstEdges, totalWeight } = this.kruskal(true);
            const forest = this._buildForest(mstEdges);
            return { forest, totalWeight };
        } else if (algorithm === 'prim') {
            const visitedGlobal = new Set();
            const forest = [];
            let totalWeight = 0;

            for (let start = 0; start < this.numVertices; start++) {
                if (!visitedGlobal.has(start)) {
                    const { mstEdges: treeEdges, totalWeight: treeWeight } = this.prim(start);

                    // Mark vertices in this tree as visited
                    for (const edge of treeEdges) {
                        visitedGlobal.add(edge.u);
                        visitedGlobal.add(edge.v);
                    }

                    if (treeEdges.length > 0) {
                        forest.push(treeEdges);
                        totalWeight += treeWeight;
                    }
                }
            }

            return { forest, totalWeight };
        } else if (algorithm === 'boruvka') {
            const { mstEdges, totalWeight } = this.boruvka();
            const forest = this._buildForest(mstEdges);
            return { forest, totalWeight };
        } else {
            throw new Error(`Unknown algorithm: ${algorithm}`);
        }
    }

    _buildForest(edges) {
        if (edges.length === 0) return [];

        const uf = new UnionFind(this.numVertices);
        for (const edge of edges) {
            uf.union(edge.u, edge.v);
        }

        const componentEdges = new Map();
        for (const edge of edges) {
            const root = uf.find(edge.u);
            if (!componentEdges.has(root)) {
                componentEdges.set(root, []);
            }
            componentEdges.get(root).push(edge);
        }

        return Array.from(componentEdges.values());
    }

    // ========================================================================
    // UTILITY METHODS
    // ========================================================================

    /**
     * Verify if given edges form a valid MST
     */
    verifyMST(mstEdges) {
        if (mstEdges.length !== this.numVertices - 1) {
            return {
                isValid: false,
                message: `Invalid edge count: ${mstEdges.length} (expected ${this.numVertices - 1})`
            };
        }

        const uf = new UnionFind(this.numVertices);
        for (const edge of mstEdges) {
            if (!uf.union(edge.u, edge.v)) {
                return {
                    isValid: false,
                    message: `Contains cycle at edge ${edge}`
                };
            }
        }

        if (uf.getComponentCount() !== 1) {
            return {
                isValid: false,
                message: `Disconnected: ${uf.getComponentCount()} components`
            };
        }

        return { isValid: true, message: 'Valid MST' };
    }

    /**
     * Compare performance of all MST algorithms
     */
    compareAlgorithms(numRuns = 10) {
        const results = {};

        // Kruskal's
        const kruskalTimes = [];
        let kResult;
        for (let i = 0; i < numRuns; i++) {
            const start = performance.now();
            kResult = this.kruskal();
            kruskalTimes.push(performance.now() - start);
        }

        results.kruskal = {
            meanTime: kruskalTimes.reduce((a, b) => a + b) / kruskalTimes.length,
            minTime: Math.min(...kruskalTimes),
            maxTime: Math.max(...kruskalTimes),
            weight: kResult.totalWeight,
            numEdges: kResult.mstEdges.length
        };

        // Prim's
        const primTimes = [];
        let pResult;
        for (let i = 0; i < numRuns; i++) {
            const start = performance.now();
            pResult = this.prim();
            primTimes.push(performance.now() - start);
        }

        results.prim = {
            meanTime: primTimes.reduce((a, b) => a + b) / primTimes.length,
            minTime: Math.min(...primTimes),
            maxTime: Math.max(...primTimes),
            weight: pResult.totalWeight,
            numEdges: pResult.mstEdges.length
        };

        // Borůvka's
        const boruvkaTimes = [];
        let bResult;
        for (let i = 0; i < numRuns; i++) {
            const start = performance.now();
            bResult = this.boruvka();
            boruvkaTimes.push(performance.now() - start);
        }

        results.boruvka = {
            meanTime: boruvkaTimes.reduce((a, b) => a + b) / boruvkaTimes.length,
            minTime: Math.min(...boruvkaTimes),
            maxTime: Math.max(...boruvkaTimes),
            weight: bResult.totalWeight,
            numEdges: bResult.mstEdges.length
        };

        // Check if all agree
        const weights = [kResult.totalWeight, pResult.totalWeight, bResult.totalWeight];
        results.allAgree = new Set(weights).size === 1;

        return results;
    }
}

// ========================================================================
// DEMO
// ========================================================================

function demoMSTAlgorithms() {
    console.log('='.repeat(80));
    console.log('MINIMUM SPANNING TREE ALGORITHMS DEMO');
    console.log('='.repeat(80));
    console.log();

    const edges = [
        [0, 1, 4],
        [0, 7, 8],
        [1, 2, 8],
        [1, 7, 11],
        [2, 3, 7],
        [2, 5, 4],
        [2, 8, 2],
        [3, 4, 9],
        [3, 5, 14],
        [4, 5, 10],
        [5, 6, 2],
        [6, 7, 1],
        [6, 8, 6],
        [7, 8, 7]
    ];

    const mst = new MSTAlgorithms(9, edges);

    // Kruskal's
    console.log("1. KRUSKAL'S ALGORITHM");
    console.log('-'.repeat(80));
    const kResult = mst.kruskal();
    console.log(`MST Weight: ${kResult.totalWeight}`);
    console.log(`Edges: ${kResult.mstEdges.map(e => `(${e.u},${e.v},${e.weight})`).join(', ')}`);
    console.log();

    // Prim's
    console.log("2. PRIM'S ALGORITHM");
    console.log('-'.repeat(80));
    const pResult = mst.prim();
    console.log(`MST Weight: ${pResult.totalWeight}`);
    console.log(`Edges: ${pResult.mstEdges.map(e => `(${e.u},${e.v},${e.weight})`).join(', ')}`);
    console.log();

    // Borůvka's
    console.log("3. BORŮVKA'S ALGORITHM");
    console.log('-'.repeat(80));
    const bResult = mst.boruvka();
    console.log(`MST Weight: ${bResult.totalWeight}`);
    console.log(`Edges: ${bResult.mstEdges.map(e => `(${e.u},${e.v},${e.weight})`).join(', ')}`);
    console.log();

    // Performance
    console.log('4. PERFORMANCE COMPARISON');
    console.log('-'.repeat(80));
    const results = mst.compareAlgorithms(100);

    for (const [algo, metrics] of Object.entries(results)) {
        if (algo === 'allAgree') continue;
        console.log(`\n${algo.toUpperCase()}`);
        console.log(`  Mean time: ${metrics.meanTime.toFixed(4)} ms`);
        console.log(`  Min time:  ${metrics.minTime.toFixed(4)} ms`);
        console.log(`  Max time:  ${metrics.maxTime.toFixed(4)} ms`);
        console.log(`  Weight:    ${metrics.weight}`);
    }

    console.log(`\nAll algorithms agree: ${results.allAgree}`);
    console.log();

    // Disconnected graph
    console.log('5. MINIMUM SPANNING FOREST (Disconnected Graph)');
    console.log('-'.repeat(80));
    const disconnectedEdges = [
        [0, 1, 1],
        [1, 2, 2],
        [3, 4, 3],
        [4, 5, 4]
    ];

    const mstForest = new MSTAlgorithms(6, disconnectedEdges);
    const { forest, totalWeight } = mstForest.minimumSpanningForest();

    console.log(`Number of trees: ${forest.length}`);
    console.log(`Total weight: ${totalWeight}`);
    forest.forEach((tree, i) => {
        console.log(`\nTree ${i + 1}:`);
        console.log(`  Edges: ${tree.map(e => `(${e.u},${e.v},${e.weight})`).join(', ')}`);
    });
}

// Run demo if executed directly
if (typeof require !== 'undefined' && require.main === module) {
    demoMSTAlgorithms();
}

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MSTAlgorithms, UnionFind, Edge, MinHeap };
}
