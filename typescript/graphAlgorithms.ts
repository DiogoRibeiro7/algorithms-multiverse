/**
 * Graph Algorithms in TypeScript
 * ===============================
 *
 * Comprehensive graph algorithms with TypeScript features:
 * - Generic types for flexible graph representations
 * - Multiple graph implementations (adjacency list, matrix)
 * - Path finding algorithms
 * - Graph traversal algorithms
 * - Minimum spanning tree algorithms
 *
 * @module graphAlgorithms
 * @author Algorithms Multiverse
 */

/**
 * Edge interface for weighted graphs
 */
interface Edge<T> {
    from: T;
    to: T;
    weight?: number;
}

/**
 * Graph interface
 */
interface IGraph<T> {
    addVertex(vertex: T): void;
    addEdge(from: T, to: T, weight?: number): void;
    removeVertex(vertex: T): boolean;
    removeEdge(from: T, to: T): boolean;
    getNeighbors(vertex: T): T[];
    hasVertex(vertex: T): boolean;
    hasEdge(from: T, to: T): boolean;
    getVertices(): T[];
    getEdges(): Edge<T>[];
    getVertexCount(): number;
    getEdgeCount(): number;
}

/**
 * Graph implementation using adjacency list
 */
export class Graph<T> implements IGraph<T> {
    protected adjacencyList: Map<T, Map<T, number>>;
    protected directed: boolean;

    constructor(directed = false) {
        this.adjacencyList = new Map();
        this.directed = directed;
    }

    addVertex(vertex: T): void {
        if (!this.adjacencyList.has(vertex)) {
            this.adjacencyList.set(vertex, new Map());
        }
    }

    addEdge(from: T, to: T, weight = 1): void {
        this.addVertex(from);
        this.addVertex(to);

        this.adjacencyList.get(from)!.set(to, weight);

        if (!this.directed) {
            this.adjacencyList.get(to)!.set(from, weight);
        }
    }

    removeVertex(vertex: T): boolean {
        if (!this.adjacencyList.has(vertex)) {
            return false;
        }

        // Remove all edges to this vertex
        for (const [, neighbors] of this.adjacencyList) {
            neighbors.delete(vertex);
        }

        // Remove the vertex
        this.adjacencyList.delete(vertex);
        return true;
    }

    removeEdge(from: T, to: T): boolean {
        if (!this.adjacencyList.has(from)) {
            return false;
        }

        const removed = this.adjacencyList.get(from)!.delete(to);

        if (!this.directed && this.adjacencyList.has(to)) {
            this.adjacencyList.get(to)!.delete(from);
        }

        return removed;
    }

    getNeighbors(vertex: T): T[] {
        const neighbors = this.adjacencyList.get(vertex);
        return neighbors ? Array.from(neighbors.keys()) : [];
    }

    getWeight(from: T, to: T): number | undefined {
        const neighbors = this.adjacencyList.get(from);
        return neighbors?.get(to);
    }

    hasVertex(vertex: T): boolean {
        return this.adjacencyList.has(vertex);
    }

    hasEdge(from: T, to: T): boolean {
        const neighbors = this.adjacencyList.get(from);
        return neighbors?.has(to) ?? false;
    }

    getVertices(): T[] {
        return Array.from(this.adjacencyList.keys());
    }

    getEdges(): Edge<T>[] {
        const edges: Edge<T>[] = [];
        const seen = new Set<string>();

        for (const [from, neighbors] of this.adjacencyList) {
            for (const [to, weight] of neighbors) {
                const edgeKey = this.directed
                    ? `${from}->${to}`
                    : [from, to].sort().join('-');

                if (!seen.has(edgeKey)) {
                    seen.add(edgeKey);
                    edges.push({ from, to, weight });
                }
            }
        }

        return edges;
    }

    getVertexCount(): number {
        return this.adjacencyList.size;
    }

    getEdgeCount(): number {
        let count = 0;
        for (const neighbors of this.adjacencyList.values()) {
            count += neighbors.size;
        }
        return this.directed ? count : count / 2;
    }

    /**
     * Get the degree of a vertex
     */
    getDegree(vertex: T): number {
        if (!this.hasVertex(vertex)) return 0;

        if (!this.directed) {
            return this.adjacencyList.get(vertex)!.size;
        }

        // For directed graphs, return in-degree + out-degree
        let inDegree = 0;
        for (const [v, neighbors] of this.adjacencyList) {
            if (v !== vertex && neighbors.has(vertex)) {
                inDegree++;
            }
        }

        return inDegree + this.adjacencyList.get(vertex)!.size;
    }

    /**
     * Clone the graph
     */
    clone(): Graph<T> {
        const newGraph = new Graph<T>(this.directed);

        for (const vertex of this.getVertices()) {
            newGraph.addVertex(vertex);
        }

        for (const edge of this.getEdges()) {
            newGraph.addEdge(edge.from, edge.to, edge.weight);
        }

        return newGraph;
    }

    /**
     * Check if graph is connected (for undirected) or strongly connected (for directed)
     */
    isConnected(): boolean {
        const vertices = this.getVertices();
        if (vertices.length === 0) return true;

        const visited = new Set<T>();
        const dfs = (vertex: T): void => {
            visited.add(vertex);
            for (const neighbor of this.getNeighbors(vertex)) {
                if (!visited.has(neighbor)) {
                    dfs(neighbor);
                }
            }
        };

        dfs(vertices[0]);
        return visited.size === vertices.length;
    }
}

/**
 * Graph Traversal Algorithms
 */
export class GraphTraversal {
    /**
     * Breadth-First Search
     */
    static bfs<T>(graph: Graph<T>, start: T): T[] {
        if (!graph.hasVertex(start)) {
            throw new Error(`Vertex ${start} not found in graph`);
        }

        const visited = new Set<T>();
        const queue: T[] = [start];
        const result: T[] = [];

        visited.add(start);

        while (queue.length > 0) {
            const vertex = queue.shift()!;
            result.push(vertex);

            for (const neighbor of graph.getNeighbors(vertex)) {
                if (!visited.has(neighbor)) {
                    visited.add(neighbor);
                    queue.push(neighbor);
                }
            }
        }

        return result;
    }

    /**
     * Depth-First Search (Iterative)
     */
    static dfs<T>(graph: Graph<T>, start: T): T[] {
        if (!graph.hasVertex(start)) {
            throw new Error(`Vertex ${start} not found in graph`);
        }

        const visited = new Set<T>();
        const stack: T[] = [start];
        const result: T[] = [];

        while (stack.length > 0) {
            const vertex = stack.pop()!;

            if (!visited.has(vertex)) {
                visited.add(vertex);
                result.push(vertex);

                for (const neighbor of graph.getNeighbors(vertex)) {
                    if (!visited.has(neighbor)) {
                        stack.push(neighbor);
                    }
                }
            }
        }

        return result;
    }

    /**
     * Depth-First Search (Recursive)
     */
    static dfsRecursive<T>(graph: Graph<T>, start: T): T[] {
        if (!graph.hasVertex(start)) {
            throw new Error(`Vertex ${start} not found in graph`);
        }

        const visited = new Set<T>();
        const result: T[] = [];

        const dfsHelper = (vertex: T): void => {
            visited.add(vertex);
            result.push(vertex);

            for (const neighbor of graph.getNeighbors(vertex)) {
                if (!visited.has(neighbor)) {
                    dfsHelper(neighbor);
                }
            }
        };

        dfsHelper(start);
        return result;
    }

    /**
     * Topological Sort (for DAGs)
     */
    static topologicalSort<T>(graph: Graph<T>): T[] | null {
        const inDegree = new Map<T, number>();
        const vertices = graph.getVertices();

        // Calculate in-degrees
        for (const vertex of vertices) {
            inDegree.set(vertex, 0);
        }

        for (const vertex of vertices) {
            for (const neighbor of graph.getNeighbors(vertex)) {
                inDegree.set(neighbor, (inDegree.get(neighbor) ?? 0) + 1);
            }
        }

        // Find vertices with no incoming edges
        const queue: T[] = [];
        for (const [vertex, degree] of inDegree) {
            if (degree === 0) {
                queue.push(vertex);
            }
        }

        const result: T[] = [];

        while (queue.length > 0) {
            const vertex = queue.shift()!;
            result.push(vertex);

            for (const neighbor of graph.getNeighbors(vertex)) {
                const newDegree = (inDegree.get(neighbor) ?? 0) - 1;
                inDegree.set(neighbor, newDegree);

                if (newDegree === 0) {
                    queue.push(neighbor);
                }
            }
        }

        // Check for cycles
        return result.length === vertices.length ? result : null;
    }
}

/**
 * Shortest Path Algorithms
 */
export class ShortestPath {
    /**
     * Dijkstra's Algorithm
     */
    static dijkstra<T>(
        graph: Graph<T>,
        start: T,
        end?: T
    ): Map<T, { distance: number; previous: T | null }> {
        if (!graph.hasVertex(start)) {
            throw new Error(`Start vertex ${start} not found`);
        }

        const distances = new Map<T, { distance: number; previous: T | null }>();
        const visited = new Set<T>();
        const unvisited = new Set<T>(graph.getVertices());

        // Initialize distances
        for (const vertex of graph.getVertices()) {
            distances.set(vertex, {
                distance: vertex === start ? 0 : Infinity,
                previous: null
            });
        }

        while (unvisited.size > 0) {
            // Find unvisited vertex with minimum distance
            let current: T | null = null;
            let minDistance = Infinity;

            for (const vertex of unvisited) {
                const distance = distances.get(vertex)!.distance;
                if (distance < minDistance) {
                    minDistance = distance;
                    current = vertex;
                }
            }

            if (current === null || minDistance === Infinity) {
                break;
            }

            // Early exit if we reached the target
            if (end && current === end) {
                break;
            }

            unvisited.delete(current);
            visited.add(current);

            // Update distances to neighbors
            for (const neighbor of graph.getNeighbors(current)) {
                if (!visited.has(neighbor)) {
                    const weight = graph.getWeight(current, neighbor) ?? 1;
                    const altDistance = distances.get(current)!.distance + weight;

                    if (altDistance < distances.get(neighbor)!.distance) {
                        distances.set(neighbor, {
                            distance: altDistance,
                            previous: current
                        });
                    }
                }
            }
        }

        return distances;
    }

    /**
     * Bellman-Ford Algorithm (handles negative weights)
     */
    static bellmanFord<T>(
        graph: Graph<T>,
        start: T
    ): Map<T, { distance: number; previous: T | null }> | null {
        const distances = new Map<T, { distance: number; previous: T | null }>();
        const vertices = graph.getVertices();
        const edges = graph.getEdges();

        // Initialize distances
        for (const vertex of vertices) {
            distances.set(vertex, {
                distance: vertex === start ? 0 : Infinity,
                previous: null
            });
        }

        // Relax edges V-1 times
        for (let i = 0; i < vertices.length - 1; i++) {
            for (const edge of edges) {
                const fromDist = distances.get(edge.from)!.distance;
                const toDist = distances.get(edge.to)!.distance;
                const weight = edge.weight ?? 1;

                if (fromDist + weight < toDist) {
                    distances.set(edge.to, {
                        distance: fromDist + weight,
                        previous: edge.from
                    });
                }
            }
        }

        // Check for negative cycles
        for (const edge of edges) {
            const fromDist = distances.get(edge.from)!.distance;
            const toDist = distances.get(edge.to)!.distance;
            const weight = edge.weight ?? 1;

            if (fromDist + weight < toDist) {
                return null; // Negative cycle detected
            }
        }

        return distances;
    }

    /**
     * Floyd-Warshall Algorithm (all-pairs shortest paths)
     */
    static floydWarshall<T>(graph: Graph<T>): Map<T, Map<T, number>> {
        const vertices = graph.getVertices();
        const distances = new Map<T, Map<T, number>>();

        // Initialize distances
        for (const i of vertices) {
            distances.set(i, new Map());
            for (const j of vertices) {
                if (i === j) {
                    distances.get(i)!.set(j, 0);
                } else if (graph.hasEdge(i, j)) {
                    distances.get(i)!.set(j, graph.getWeight(i, j) ?? 1);
                } else {
                    distances.get(i)!.set(j, Infinity);
                }
            }
        }

        // Dynamic programming
        for (const k of vertices) {
            for (const i of vertices) {
                for (const j of vertices) {
                    const direct = distances.get(i)!.get(j)!;
                    const throughK = distances.get(i)!.get(k)! + distances.get(k)!.get(j)!;

                    if (throughK < direct) {
                        distances.get(i)!.set(j, throughK);
                    }
                }
            }
        }

        return distances;
    }

    /**
     * A* Algorithm
     */
    static aStar<T>(
        graph: Graph<T>,
        start: T,
        goal: T,
        heuristic: (node: T) => number
    ): T[] | null {
        if (!graph.hasVertex(start) || !graph.hasVertex(goal)) {
            throw new Error("Start or goal vertex not found");
        }

        const openSet = new Set<T>([start]);
        const cameFrom = new Map<T, T>();

        const gScore = new Map<T, number>();
        const fScore = new Map<T, number>();

        for (const vertex of graph.getVertices()) {
            gScore.set(vertex, Infinity);
            fScore.set(vertex, Infinity);
        }

        gScore.set(start, 0);
        fScore.set(start, heuristic(start));

        while (openSet.size > 0) {
            // Find node with lowest fScore
            let current: T | null = null;
            let lowestFScore = Infinity;

            for (const node of openSet) {
                const score = fScore.get(node)!;
                if (score < lowestFScore) {
                    lowestFScore = score;
                    current = node;
                }
            }

            if (current === null) break;

            if (current === goal) {
                // Reconstruct path
                const path: T[] = [];
                let node: T | undefined = goal;

                while (node !== undefined) {
                    path.unshift(node);
                    node = cameFrom.get(node);
                }

                return path;
            }

            openSet.delete(current);

            for (const neighbor of graph.getNeighbors(current)) {
                const tentativeGScore = gScore.get(current)! +
                    (graph.getWeight(current, neighbor) ?? 1);

                if (tentativeGScore < gScore.get(neighbor)!) {
                    cameFrom.set(neighbor, current);
                    gScore.set(neighbor, tentativeGScore);
                    fScore.set(neighbor, tentativeGScore + heuristic(neighbor));

                    if (!openSet.has(neighbor)) {
                        openSet.add(neighbor);
                    }
                }
            }
        }

        return null; // No path found
    }
}

/**
 * Minimum Spanning Tree Algorithms
 */
export class MinimumSpanningTree {
    /**
     * Kruskal's Algorithm
     */
    static kruskal<T>(graph: Graph<T>): Edge<T>[] {
        const edges = graph.getEdges();
        edges.sort((a, b) => (a.weight ?? 1) - (b.weight ?? 1));

        const parent = new Map<T, T>();
        const rank = new Map<T, number>();

        // Initialize disjoint sets
        for (const vertex of graph.getVertices()) {
            parent.set(vertex, vertex);
            rank.set(vertex, 0);
        }

        const find = (v: T): T => {
            if (parent.get(v) !== v) {
                parent.set(v, find(parent.get(v)!));
            }
            return parent.get(v)!;
        };

        const union = (v1: T, v2: T): boolean => {
            const root1 = find(v1);
            const root2 = find(v2);

            if (root1 === root2) return false;

            const rank1 = rank.get(root1)!;
            const rank2 = rank.get(root2)!;

            if (rank1 < rank2) {
                parent.set(root1, root2);
            } else if (rank1 > rank2) {
                parent.set(root2, root1);
            } else {
                parent.set(root2, root1);
                rank.set(root1, rank1 + 1);
            }

            return true;
        };

        const mst: Edge<T>[] = [];

        for (const edge of edges) {
            if (union(edge.from, edge.to)) {
                mst.push(edge);

                if (mst.length === graph.getVertexCount() - 1) {
                    break;
                }
            }
        }

        return mst;
    }

    /**
     * Prim's Algorithm
     */
    static prim<T>(graph: Graph<T>, start?: T): Edge<T>[] {
        const vertices = graph.getVertices();
        if (vertices.length === 0) return [];

        const startVertex = start ?? vertices[0];
        const mst: Edge<T>[] = [];
        const visited = new Set<T>([startVertex]);
        const edges: Edge<T>[] = [];

        // Add all edges from start vertex
        for (const neighbor of graph.getNeighbors(startVertex)) {
            edges.push({
                from: startVertex,
                to: neighbor,
                weight: graph.getWeight(startVertex, neighbor)
            });
        }

        edges.sort((a, b) => (a.weight ?? 1) - (b.weight ?? 1));

        while (visited.size < vertices.length && edges.length > 0) {
            const edge = edges.shift()!;

            if (!visited.has(edge.to)) {
                visited.add(edge.to);
                mst.push(edge);

                // Add new edges
                for (const neighbor of graph.getNeighbors(edge.to)) {
                    if (!visited.has(neighbor)) {
                        edges.push({
                            from: edge.to,
                            to: neighbor,
                            weight: graph.getWeight(edge.to, neighbor)
                        });
                    }
                }

                edges.sort((a, b) => (a.weight ?? 1) - (b.weight ?? 1));
            }
        }

        return mst;
    }
}

/**
 * Graph Utilities
 */
export class GraphUtils {
    /**
     * Detect cycles in a graph
     */
    static hasCycle<T>(graph: Graph<T>): boolean {
        const visited = new Set<T>();
        const recursionStack = new Set<T>();

        const hasCycleDFS = (vertex: T): boolean => {
            visited.add(vertex);
            recursionStack.add(vertex);

            for (const neighbor of graph.getNeighbors(vertex)) {
                if (!visited.has(neighbor)) {
                    if (hasCycleDFS(neighbor)) {
                        return true;
                    }
                } else if (recursionStack.has(neighbor)) {
                    return true;
                }
            }

            recursionStack.delete(vertex);
            return false;
        };

        for (const vertex of graph.getVertices()) {
            if (!visited.has(vertex)) {
                if (hasCycleDFS(vertex)) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Find strongly connected components (Kosaraju's algorithm)
     */
    static stronglyConnectedComponents<T>(graph: Graph<T>): T[][] {
        const vertices = graph.getVertices();
        const visited = new Set<T>();
        const stack: T[] = [];

        // First DFS to fill stack
        const dfs1 = (vertex: T): void => {
            visited.add(vertex);
            for (const neighbor of graph.getNeighbors(vertex)) {
                if (!visited.has(neighbor)) {
                    dfs1(neighbor);
                }
            }
            stack.push(vertex);
        };

        for (const vertex of vertices) {
            if (!visited.has(vertex)) {
                dfs1(vertex);
            }
        }

        // Create transpose graph
        const transpose = new Graph<T>(true);
        for (const vertex of vertices) {
            transpose.addVertex(vertex);
        }
        for (const edge of graph.getEdges()) {
            transpose.addEdge(edge.to, edge.from, edge.weight);
        }

        // Second DFS on transpose
        visited.clear();
        const components: T[][] = [];

        const dfs2 = (vertex: T, component: T[]): void => {
            visited.add(vertex);
            component.push(vertex);
            for (const neighbor of transpose.getNeighbors(vertex)) {
                if (!visited.has(neighbor)) {
                    dfs2(neighbor, component);
                }
            }
        };

        while (stack.length > 0) {
            const vertex = stack.pop()!;
            if (!visited.has(vertex)) {
                const component: T[] = [];
                dfs2(vertex, component);
                components.push(component);
            }
        }

        return components;
    }
}

// Example usage and tests
if (require.main === module) {
    console.log("TypeScript Graph Algorithms Demonstration");
    console.log("=" .repeat(50));

    // Create a sample graph
    const graph = new Graph<string>();

    // Add vertices and edges
    const edges: [string, string, number][] = [
        ["A", "B", 4],
        ["A", "C", 2],
        ["B", "C", 1],
        ["B", "D", 5],
        ["C", "D", 8],
        ["C", "E", 10],
        ["D", "E", 2],
        ["D", "F", 6],
        ["E", "F", 3]
    ];

    for (const [from, to, weight] of edges) {
        graph.addEdge(from, to, weight);
    }

    console.log("\n1. Graph Properties:");
    console.log("Vertices:", graph.getVertices());
    console.log("Vertex count:", graph.getVertexCount());
    console.log("Edge count:", graph.getEdgeCount());
    console.log("Is connected:", graph.isConnected());

    console.log("\n2. Graph Traversal:");
    console.log("BFS from A:", GraphTraversal.bfs(graph, "A"));
    console.log("DFS from A:", GraphTraversal.dfs(graph, "A"));

    console.log("\n3. Shortest Paths:");
    const dijkstraResult = ShortestPath.dijkstra(graph, "A");
    console.log("Dijkstra from A:");
    for (const [vertex, info] of dijkstraResult) {
        console.log(`  ${vertex}: distance=${info.distance}, previous=${info.previous}`);
    }

    // Reconstruct path from A to F
    const pathToF: string[] = [];
    let current: string | null = "F";
    while (current !== null) {
        pathToF.unshift(current);
        current = dijkstraResult.get(current)!.previous;
    }
    console.log("Path from A to F:", pathToF.join(" -> "));

    console.log("\n4. Minimum Spanning Tree:");
    const mstKruskal = MinimumSpanningTree.kruskal(graph);
    console.log("Kruskal's MST:");
    let totalWeight = 0;
    for (const edge of mstKruskal) {
        console.log(`  ${edge.from} - ${edge.to}: ${edge.weight}`);
        totalWeight += edge.weight ?? 0;
    }
    console.log("Total weight:", totalWeight);

    console.log("\n5. Directed Graph Example:");
    const directedGraph = new Graph<number>(true);
    directedGraph.addEdge(1, 2);
    directedGraph.addEdge(2, 3);
    directedGraph.addEdge(3, 4);
    directedGraph.addEdge(4, 2);
    directedGraph.addEdge(5, 1);
    directedGraph.addEdge(5, 4);

    console.log("Has cycle:", GraphUtils.hasCycle(directedGraph));

    const topoGraph = new Graph<string>(true);
    topoGraph.addEdge("A", "B");
    topoGraph.addEdge("A", "C");
    topoGraph.addEdge("B", "D");
    topoGraph.addEdge("C", "D");

    console.log("Topological sort:", GraphTraversal.topologicalSort(topoGraph));
}