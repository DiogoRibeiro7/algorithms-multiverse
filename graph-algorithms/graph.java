/**
 * Comprehensive Graph Data Structure Implementation
 * Supports multiple representations and core graph algorithms
 */

import java.util.*;

enum GraphType {
    DIRECTED, UNDIRECTED
}

enum RepresentationType {
    ADJACENCY_LIST, ADJACENCY_MATRIX, EDGE_LIST, CSR
}

class Edge {
    int src, dst;
    double weight;

    Edge(int src, int dst, double weight) {
        this.src = src;
        this.dst = dst;
        this.weight = weight;
    }
}

class Neighbor {
    int vertex;
    double weight;

    Neighbor(int vertex, double weight) {
        this.vertex = vertex;
        this.weight = weight;
    }
}

public class Graph {
    private int numVertices;
    private int numEdges;
    private GraphType graphType;
    private boolean weighted;
    private RepresentationType representation;

    // Different representations
    private Map<Integer, List<Neighbor>> adjList;
    private Double[][] adjMatrix;
    private List<Edge> edges;
    private List<Double> csrValues;
    private List<Integer> csrColIndices;
    private List<Integer> csrRowPtr;

    /**
     * Constructor for Graph
     */
    public Graph(int numVertices, GraphType graphType, boolean weighted,
                RepresentationType representation) {
        this.numVertices = numVertices;
        this.graphType = graphType;
        this.weighted = weighted;
        this.representation = representation;
        this.numEdges = 0;

        // Initialize based on representation type
        switch (representation) {
            case ADJACENCY_LIST:
                this.adjList = new HashMap<>();
                break;
            case ADJACENCY_MATRIX:
                this.adjMatrix = new Double[numVertices][numVertices];
                break;
            case EDGE_LIST:
                this.edges = new ArrayList<>();
                break;
            case CSR:
                this.csrValues = new ArrayList<>();
                this.csrColIndices = new ArrayList<>();
                this.csrRowPtr = new ArrayList<>();
                this.csrRowPtr.add(0);
                break;
        }
    }

    /**
     * Add a new vertex and return its ID
     */
    public int addVertex() {
        int vertexId = numVertices;
        numVertices++;

        if (representation == RepresentationType.ADJACENCY_MATRIX) {
            // Expand matrix
            Double[][] newMatrix = new Double[numVertices][numVertices];
            for (int i = 0; i < numVertices - 1; i++) {
                System.arraycopy(adjMatrix[i], 0, newMatrix[i], 0, numVertices - 1);
            }
            adjMatrix = newMatrix;
        }

        return vertexId;
    }

    /**
     * Add an edge from u to v with optional weight
     */
    public void addEdge(int u, int v, double weight) {
        if (u >= numVertices || v >= numVertices) {
            throw new IllegalArgumentException("Vertex out of range: " + u + " or " + v);
        }

        numEdges++;

        switch (representation) {
            case ADJACENCY_LIST:
                adjList.computeIfAbsent(u, k -> new ArrayList<>()).add(new Neighbor(v, weight));
                if (graphType == GraphType.UNDIRECTED) {
                    adjList.computeIfAbsent(v, k -> new ArrayList<>()).add(new Neighbor(u, weight));
                }
                break;

            case ADJACENCY_MATRIX:
                adjMatrix[u][v] = weight;
                if (graphType == GraphType.UNDIRECTED) {
                    adjMatrix[v][u] = weight;
                }
                break;

            case EDGE_LIST:
                edges.add(new Edge(u, v, weight));
                if (graphType == GraphType.UNDIRECTED) {
                    edges.add(new Edge(v, u, weight));
                }
                break;

            case CSR:
                throw new UnsupportedOperationException("CSR edges should be added via buildCSR()");
        }
    }

    public void addEdge(int u, int v) {
        addEdge(u, v, 1.0);
    }

    /**
     * Build CSR representation from edge list
     */
    public void buildCSR(List<Edge> edgeList) {
        if (representation != RepresentationType.CSR) {
            throw new IllegalStateException("Graph must be CSR type");
        }

        // Sort edges by source vertex
        edgeList.sort(Comparator.comparingInt((Edge e) -> e.src)
                              .thenComparingInt(e -> e.dst));

        csrValues.clear();
        csrColIndices.clear();
        csrRowPtr.clear();
        csrRowPtr.add(0);

        int currentRow = 0;
        for (Edge edge : edgeList) {
            // Fill gaps for vertices with no outgoing edges
            while (currentRow < edge.src) {
                csrRowPtr.add(csrColIndices.size());
                currentRow++;
            }

            csrValues.add(edge.weight);
            csrColIndices.add(edge.dst);
        }

        // Complete row pointers
        while (currentRow < numVertices) {
            csrRowPtr.add(csrColIndices.size());
            currentRow++;
        }

        numEdges = edgeList.size();
    }

    /**
     * Get neighbors of vertex u with their edge weights
     */
    public List<Neighbor> getNeighbors(int u) {
        switch (representation) {
            case ADJACENCY_LIST:
                return adjList.getOrDefault(u, new ArrayList<>());

            case ADJACENCY_MATRIX:
                List<Neighbor> neighbors = new ArrayList<>();
                for (int v = 0; v < numVertices; v++) {
                    if (adjMatrix[u][v] != null) {
                        neighbors.add(new Neighbor(v, adjMatrix[u][v]));
                    }
                }
                return neighbors;

            case EDGE_LIST:
                List<Neighbor> edgeNeighbors = new ArrayList<>();
                for (Edge edge : edges) {
                    if (edge.src == u) {
                        edgeNeighbors.add(new Neighbor(edge.dst, edge.weight));
                    }
                }
                return edgeNeighbors;

            case CSR:
                List<Neighbor> csrNeighbors = new ArrayList<>();
                int start = csrRowPtr.get(u);
                int end = csrRowPtr.get(u + 1);
                for (int i = start; i < end; i++) {
                    csrNeighbors.add(new Neighbor(csrColIndices.get(i), csrValues.get(i)));
                }
                return csrNeighbors;

            default:
                return new ArrayList<>();
        }
    }

    // === DEPTH-FIRST SEARCH ===

    /**
     * DFS traversal using recursion
     */
    public List<Integer> dfsRecursive(int start) {
        List<Integer> traversal = new ArrayList<>();
        Set<Integer> visited = new HashSet<>();
        dfsHelper(start, visited, traversal);
        return traversal;
    }

    private void dfsHelper(int v, Set<Integer> visited, List<Integer> traversal) {
        visited.add(v);
        traversal.add(v);

        for (Neighbor neighbor : getNeighbors(v)) {
            if (!visited.contains(neighbor.vertex)) {
                dfsHelper(neighbor.vertex, visited, traversal);
            }
        }
    }

    /**
     * DFS traversal using iteration with stack
     */
    public List<Integer> dfsIterative(int start) {
        Set<Integer> visited = new HashSet<>();
        List<Integer> traversal = new ArrayList<>();
        Stack<Integer> stack = new Stack<>();
        stack.push(start);

        while (!stack.isEmpty()) {
            int v = stack.pop();
            if (!visited.contains(v)) {
                visited.add(v);
                traversal.add(v);

                // Add neighbors in reverse order for consistent ordering
                List<Neighbor> neighbors = getNeighbors(v);
                for (int i = neighbors.size() - 1; i >= 0; i--) {
                    int neighbor = neighbors.get(i).vertex;
                    if (!visited.contains(neighbor)) {
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
    public List<Integer> bfs(int start) {
        Set<Integer> visited = new HashSet<>();
        List<Integer> traversal = new ArrayList<>();
        Queue<Integer> queue = new LinkedList<>();

        visited.add(start);
        queue.offer(start);

        while (!queue.isEmpty()) {
            int v = queue.poll();
            traversal.add(v);

            for (Neighbor neighbor : getNeighbors(v)) {
                if (!visited.contains(neighbor.vertex)) {
                    visited.add(neighbor.vertex);
                    queue.offer(neighbor.vertex);
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
    public List<Integer> topologicalSort() {
        if (graphType != GraphType.DIRECTED) {
            throw new IllegalStateException("Topological sort only works for directed graphs");
        }

        // Calculate in-degrees
        int[] inDegree = new int[numVertices];
        for (int u = 0; u < numVertices; u++) {
            for (Neighbor neighbor : getNeighbors(u)) {
                inDegree[neighbor.vertex]++;
            }
        }

        // Queue with vertices having 0 in-degree
        Queue<Integer> queue = new LinkedList<>();
        for (int v = 0; v < numVertices; v++) {
            if (inDegree[v] == 0) {
                queue.offer(v);
            }
        }

        List<Integer> result = new ArrayList<>();

        while (!queue.isEmpty()) {
            int u = queue.poll();
            result.add(u);

            for (Neighbor neighbor : getNeighbors(u)) {
                inDegree[neighbor.vertex]--;
                if (inDegree[neighbor.vertex] == 0) {
                    queue.offer(neighbor.vertex);
                }
            }
        }

        // Check if all vertices were processed (no cycle)
        return result.size() == numVertices ? result : null;
    }

    /**
     * Topological sorting using DFS
     */
    public List<Integer> topologicalSortDFS() {
        if (graphType != GraphType.DIRECTED) {
            throw new IllegalStateException("Topological sort only works for directed graphs");
        }

        Set<Integer> visited = new HashSet<>();
        Set<Integer> recStack = new HashSet<>();
        List<Integer> result = new ArrayList<>();

        for (int v = 0; v < numVertices; v++) {
            if (!visited.contains(v)) {
                if (!topoDFSHelper(v, visited, recStack, result)) {
                    return null;  // Cycle detected
                }
            }
        }

        Collections.reverse(result);
        return result;
    }

    private boolean topoDFSHelper(int v, Set<Integer> visited, Set<Integer> recStack,
                                  List<Integer> result) {
        visited.add(v);
        recStack.add(v);

        for (Neighbor neighbor : getNeighbors(v)) {
            if (!visited.contains(neighbor.vertex)) {
                if (!topoDFSHelper(neighbor.vertex, visited, recStack, result)) {
                    return false;
                }
            } else if (recStack.contains(neighbor.vertex)) {
                return false;  // Cycle detected
            }
        }

        recStack.remove(v);
        result.add(v);
        return true;
    }

    // === CONNECTED COMPONENTS ===

    /**
     * Find all connected components in the graph
     */
    public List<List<Integer>> findConnectedComponents() {
        Set<Integer> visited = new HashSet<>();
        List<List<Integer>> components = new ArrayList<>();

        for (int v = 0; v < numVertices; v++) {
            if (!visited.contains(v)) {
                List<Integer> component = new ArrayList<>();
                Stack<Integer> stack = new Stack<>();
                stack.push(v);

                while (!stack.isEmpty()) {
                    int u = stack.pop();
                    if (!visited.contains(u)) {
                        visited.add(u);
                        component.add(u);

                        for (Neighbor neighbor : getNeighbors(u)) {
                            if (!visited.contains(neighbor.vertex)) {
                                stack.push(neighbor.vertex);
                            }
                        }
                    }
                }

                Collections.sort(component);
                components.add(component);
            }
        }

        return components;
    }

    /**
     * Check if graph is connected
     */
    public boolean isConnected() {
        if (numVertices == 0) return true;
        return findConnectedComponents().size() == 1;
    }

    // === CYCLE DETECTION ===

    /**
     * Detect cycle in undirected graph using DFS
     */
    public boolean hasCycleUndirected() {
        if (graphType != GraphType.UNDIRECTED) {
            throw new IllegalStateException("This method is for undirected graphs");
        }

        Set<Integer> visited = new HashSet<>();

        for (int v = 0; v < numVertices; v++) {
            if (!visited.contains(v)) {
                if (hasCycleUndirectedHelper(v, -1, visited)) {
                    return true;
                }
            }
        }

        return false;
    }

    private boolean hasCycleUndirectedHelper(int v, int parent, Set<Integer> visited) {
        visited.add(v);

        for (Neighbor neighbor : getNeighbors(v)) {
            if (!visited.contains(neighbor.vertex)) {
                if (hasCycleUndirectedHelper(neighbor.vertex, v, visited)) {
                    return true;
                }
            } else if (neighbor.vertex != parent) {
                return true;  // Cycle found
            }
        }

        return false;
    }

    /**
     * Detect cycle in directed graph using DFS with recursion stack
     */
    public boolean hasCycleDirected() {
        if (graphType != GraphType.DIRECTED) {
            throw new IllegalStateException("This method is for directed graphs");
        }

        Set<Integer> visited = new HashSet<>();
        Set<Integer> recStack = new HashSet<>();

        for (int v = 0; v < numVertices; v++) {
            if (!visited.contains(v)) {
                if (hasCycleDirectedHelper(v, visited, recStack)) {
                    return true;
                }
            }
        }

        return false;
    }

    private boolean hasCycleDirectedHelper(int v, Set<Integer> visited, Set<Integer> recStack) {
        visited.add(v);
        recStack.add(v);

        for (Neighbor neighbor : getNeighbors(v)) {
            if (!visited.contains(neighbor.vertex)) {
                if (hasCycleDirectedHelper(neighbor.vertex, visited, recStack)) {
                    return true;
                }
            } else if (recStack.contains(neighbor.vertex)) {
                return true;  // Back edge found
            }
        }

        recStack.remove(v);
        return false;
    }

    /**
     * Detect cycle based on graph type
     */
    public boolean hasCycle() {
        if (graphType == GraphType.DIRECTED) {
            return hasCycleDirected();
        } else {
            return hasCycleUndirected();
        }
    }

    // === GRAPH COLORING ===

    /**
     * Graph coloring using greedy algorithm
     * Returns mapping of vertex -> color
     */
    public Map<Integer, Integer> greedyColoring() {
        Map<Integer, Integer> colors = new HashMap<>();

        for (int v = 0; v < numVertices; v++) {
            // Get colors of neighbors
            Set<Integer> neighborColors = new HashSet<>();
            for (Neighbor neighbor : getNeighbors(v)) {
                if (colors.containsKey(neighbor.vertex)) {
                    neighborColors.add(colors.get(neighbor.vertex));
                }
            }

            // Find first available color
            int color = 0;
            while (neighborColors.contains(color)) {
                color++;
            }

            colors.put(v, color);
        }

        return colors;
    }

    /**
     * Get upper bound on chromatic number
     */
    public int chromaticNumberUpperBound() {
        Map<Integer, Integer> coloring = greedyColoring();
        if (coloring.isEmpty()) return 0;
        return Collections.max(coloring.values()) + 1;
    }

    // === VISUALIZATION ===

    /**
     * Generate ASCII art representation of the graph
     */
    public String toASCII(int maxWidth) {
        StringBuilder sb = new StringBuilder();
        sb.append("=".repeat(maxWidth)).append("\n");
        sb.append(String.format("Graph: %s, %s\n", graphType,
                  weighted ? "weighted" : "unweighted"));
        sb.append(String.format("Representation: %s\n", representation));
        sb.append(String.format("Vertices: %d, Edges: %d\n", numVertices, numEdges));
        sb.append("=".repeat(maxWidth)).append("\n\n");

        switch (representation) {
            case ADJACENCY_LIST:
                sb.append("Adjacency List:\n");
                for (int v = 0; v < numVertices; v++) {
                    List<Neighbor> neighbors = getNeighbors(v);
                    sb.append(String.format("  %d -> [", v));
                    for (int i = 0; i < neighbors.size(); i++) {
                        Neighbor n = neighbors.get(i);
                        if (weighted) {
                            sb.append(String.format("%d(%.1f)", n.vertex, n.weight));
                        } else {
                            sb.append(n.vertex);
                        }
                        if (i < neighbors.size() - 1) sb.append(", ");
                    }
                    sb.append("]\n");
                }
                break;

            case ADJACENCY_MATRIX:
                sb.append("Adjacency Matrix:\n");
                int displaySize = Math.min(numVertices, 15);

                // Header
                sb.append("    ");
                for (int i = 0; i < displaySize; i++) {
                    sb.append(String.format("%4d ", i));
                }
                sb.append("\n    ").append("-".repeat(5 * displaySize)).append("\n");

                for (int i = 0; i < displaySize; i++) {
                    sb.append(String.format("%2d |", i));
                    for (int j = 0; j < displaySize; j++) {
                        if (adjMatrix[i][j] == null) {
                            sb.append("   . ");
                        } else {
                            sb.append(String.format("%4.0f ", adjMatrix[i][j]));
                        }
                    }
                    sb.append("\n");
                }

                if (numVertices > 15) {
                    sb.append("  ... (truncated)\n");
                }
                break;

            case EDGE_LIST:
                sb.append("Edge List:\n");
                int displayLimit = Math.min(edges.size(), 50);
                for (int i = 0; i < displayLimit; i++) {
                    Edge e = edges.get(i);
                    if (weighted) {
                        sb.append(String.format("  %d: %d -> %d (weight: %.1f)\n",
                                  i, e.src, e.dst, e.weight));
                    } else {
                        sb.append(String.format("  %d: %d -> %d\n", i, e.src, e.dst));
                    }
                }
                if (edges.size() > 50) {
                    sb.append(String.format("  ... (%d more edges)\n", edges.size() - 50));
                }
                break;

            case CSR:
                sb.append("CSR (Compressed Sparse Row):\n");
                sb.append("  Values: ").append(csrValues.subList(0, Math.min(20, csrValues.size())));
                if (csrValues.size() > 20) sb.append("...");
                sb.append("\n");

                sb.append("  Col Indices: ").append(csrColIndices.subList(0,
                          Math.min(20, csrColIndices.size())));
                if (csrColIndices.size() > 20) sb.append("...");
                sb.append("\n");

                sb.append("  Row Ptrs: ").append(csrRowPtr.subList(0,
                          Math.min(20, csrRowPtr.size())));
                if (csrRowPtr.size() > 20) sb.append("...");
                sb.append("\n");
                break;
        }

        sb.append("\n").append("=".repeat(maxWidth)).append("\n");
        return sb.toString();
    }

    public String toASCII() {
        return toASCII(80);
    }

    @Override
    public String toString() {
        return toASCII();
    }

    // === GRAPH GENERATORS ===

    public static class GraphGenerator {
        /**
         * Generate a complete graph with n vertices
         */
        public static Graph completeGraph(int n, GraphType graphType,
                                         RepresentationType representation) {
            Graph g = new Graph(n, graphType, false, representation);

            if (representation == RepresentationType.CSR) {
                List<Edge> edges = new ArrayList<>();
                for (int i = 0; i < n; i++) {
                    for (int j = 0; j < n; j++) {
                        if (i != j) {
                            edges.add(new Edge(i, j, 1.0));
                        }
                    }
                }
                g.buildCSR(edges);
            } else {
                for (int i = 0; i < n; i++) {
                    for (int j = i + 1; j < n; j++) {
                        g.addEdge(i, j);
                        if (graphType == GraphType.DIRECTED) {
                            g.addEdge(j, i);
                        }
                    }
                }
            }

            return g;
        }

        public static Graph completeGraph(int n) {
            return completeGraph(n, GraphType.UNDIRECTED, RepresentationType.ADJACENCY_LIST);
        }

        /**
         * Generate a cycle graph with n vertices
         */
        public static Graph cycleGraph(int n, GraphType graphType,
                                      RepresentationType representation) {
            Graph g = new Graph(n, graphType, false, representation);

            if (representation == RepresentationType.CSR) {
                List<Edge> edges = new ArrayList<>();
                for (int i = 0; i < n; i++) {
                    edges.add(new Edge(i, (i + 1) % n, 1.0));
                    if (graphType == GraphType.UNDIRECTED) {
                        edges.add(new Edge((i + 1) % n, i, 1.0));
                    }
                }
                g.buildCSR(edges);
            } else {
                for (int i = 0; i < n; i++) {
                    g.addEdge(i, (i + 1) % n);
                }
            }

            return g;
        }

        public static Graph cycleGraph(int n) {
            return cycleGraph(n, GraphType.UNDIRECTED, RepresentationType.ADJACENCY_LIST);
        }

        /**
         * Generate random graph with Erdős-Rényi model
         */
        public static Graph randomGraph(int n, double edgeProbability,
                                       GraphType graphType, boolean weighted,
                                       RepresentationType representation) {
            Graph g = new Graph(n, graphType, weighted, representation);
            List<Edge> edges = new ArrayList<>();
            Random rand = new Random();

            for (int i = 0; i < n; i++) {
                int start = graphType == GraphType.UNDIRECTED ? i + 1 : 0;
                for (int j = start; j < n; j++) {
                    if (i != j && rand.nextDouble() < edgeProbability) {
                        double weight = weighted ? rand.nextDouble() * 9 + 1 : 1.0;
                        edges.add(new Edge(i, j, weight));
                    }
                }
            }

            if (representation == RepresentationType.CSR) {
                if (graphType == GraphType.UNDIRECTED) {
                    List<Edge> reversed = new ArrayList<>();
                    for (Edge e : edges) {
                        reversed.add(new Edge(e.dst, e.src, e.weight));
                    }
                    edges.addAll(reversed);
                }
                g.buildCSR(edges);
            } else {
                for (Edge e : edges) {
                    g.addEdge(e.src, e.dst, e.weight);
                }
            }

            return g;
        }

        public static Graph randomGraph(int n, double edgeProbability) {
            return randomGraph(n, edgeProbability, GraphType.UNDIRECTED, false,
                             RepresentationType.ADJACENCY_LIST);
        }

        /**
         * Generate a random Directed Acyclic Graph (DAG)
         */
        public static Graph dag(int n, double edgeProbability,
                              RepresentationType representation) {
            Graph g = new Graph(n, GraphType.DIRECTED, false, representation);
            List<Edge> edges = new ArrayList<>();
            Random rand = new Random();

            for (int i = 0; i < n; i++) {
                for (int j = i + 1; j < n; j++) {
                    if (rand.nextDouble() < edgeProbability) {
                        edges.add(new Edge(i, j, 1.0));
                    }
                }
            }

            if (representation == RepresentationType.CSR) {
                g.buildCSR(edges);
            } else {
                for (Edge e : edges) {
                    g.addEdge(e.src, e.dst, e.weight);
                }
            }

            return g;
        }

        public static Graph dag(int n, double edgeProbability) {
            return dag(n, edgeProbability, RepresentationType.ADJACENCY_LIST);
        }
    }

    // === DEMO AND TESTING ===

    public static void demo() {
        System.out.println("=".repeat(80));
        System.out.println("GRAPH DATA STRUCTURES AND ALGORITHMS DEMO");
        System.out.println("=".repeat(80));
        System.out.println();

        // Demo 1: Adjacency List
        System.out.println("1. ADJACENCY LIST REPRESENTATION");
        System.out.println("-".repeat(80));
        Graph g1 = new Graph(5, GraphType.UNDIRECTED, false, RepresentationType.ADJACENCY_LIST);
        g1.addEdge(0, 1);
        g1.addEdge(0, 4);
        g1.addEdge(1, 2);
        g1.addEdge(1, 3);
        g1.addEdge(1, 4);
        g1.addEdge(2, 3);
        g1.addEdge(3, 4);
        System.out.println(g1);

        // Demo 2: DFS and BFS
        System.out.println("2. GRAPH TRAVERSAL");
        System.out.println("-".repeat(80));
        System.out.println("DFS Recursive from 0: " + g1.dfsRecursive(0));
        System.out.println("DFS Iterative from 0: " + g1.dfsIterative(0));
        System.out.println("BFS from 0: " + g1.bfs(0));
        System.out.println();

        // Demo 3: Connected Components
        System.out.println("3. CONNECTED COMPONENTS");
        System.out.println("-".repeat(80));
        Graph g2 = new Graph(7, GraphType.UNDIRECTED, false, RepresentationType.ADJACENCY_LIST);
        g2.addEdge(0, 1);
        g2.addEdge(1, 2);
        g2.addEdge(3, 4);
        g2.addEdge(5, 6);
        System.out.println("Components: " + g2.findConnectedComponents());
        System.out.println("Is connected: " + g2.isConnected());
        System.out.println();

        // Demo 4: Cycle Detection
        System.out.println("4. CYCLE DETECTION");
        System.out.println("-".repeat(80));
        System.out.println("Graph g1 has cycle: " + g1.hasCycle());
        Graph g3 = new Graph(3, GraphType.UNDIRECTED, false, RepresentationType.ADJACENCY_LIST);
        g3.addEdge(0, 1);
        g3.addEdge(1, 2);
        System.out.println("Linear graph has cycle: " + g3.hasCycle());
        System.out.println();

        // Demo 5: Topological Sort
        System.out.println("5. TOPOLOGICAL SORTING");
        System.out.println("-".repeat(80));
        Graph dag = GraphGenerator.dag(6, 0.3);
        System.out.println(dag);
        System.out.println("Topological order: " + dag.topologicalSort());
        System.out.println("Topological order (DFS): " + dag.topologicalSortDFS());
        System.out.println();

        // Demo 6: Graph Coloring
        System.out.println("6. GRAPH COLORING");
        System.out.println("-".repeat(80));
        System.out.println("Greedy coloring: " + g1.greedyColoring());
        System.out.println("Chromatic number (upper bound): " +
                         g1.chromaticNumberUpperBound());
        System.out.println();

        // Demo 7: Different Representations
        System.out.println("7. ADJACENCY MATRIX REPRESENTATION");
        System.out.println("-".repeat(80));
        Graph g4 = new Graph(5, GraphType.DIRECTED, true, RepresentationType.ADJACENCY_MATRIX);
        g4.addEdge(0, 1, 2.5);
        g4.addEdge(0, 2, 1.0);
        g4.addEdge(1, 3, 3.0);
        g4.addEdge(2, 3, 1.5);
        g4.addEdge(3, 4, 2.0);
        System.out.println(g4);

        // Demo 8: Graph Generators
        System.out.println("8. GRAPH GENERATORS");
        System.out.println("-".repeat(80));
        Graph complete = GraphGenerator.completeGraph(5);
        System.out.println("Complete graph K5:");
        System.out.println(complete);

        Graph cycle = GraphGenerator.cycleGraph(6);
        System.out.println("Cycle graph C6:");
        System.out.println(cycle);
    }

    public static void main(String[] args) {
        demo();
    }
}
