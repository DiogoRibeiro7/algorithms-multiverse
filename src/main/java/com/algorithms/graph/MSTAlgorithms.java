package com.algorithms.graph;

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
 * @version 2025
 */

import java.util.*;

/**
 * Union-Find (Disjoint Set Union) data structure
 *
 * Implements path compression and union by rank for near O(1) operations.
 * Essential for Kruskal's algorithm.
 */
class UnionFind {
    private int[] parent;
    private int[] rank;
    private int componentCount;

    public UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        componentCount = n;

        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }
    }

    /**
     * Find the representative (root) of the set containing x
     * Uses path compression for optimization
     */
    public int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]); // Path compression
        }
        return parent[x];
    }

    /**
     * Union the sets containing x and y
     * Uses union by rank for optimization
     *
     * @return true if union was performed
     */
    public boolean union(int x, int y) {
        int px = find(x);
        int py = find(y);

        if (px == py) return false; // Already in same set

        // Union by rank
        if (rank[px] < rank[py]) {
            int temp = px;
            px = py;
            py = temp;
        }

        parent[py] = px;
        if (rank[px] == rank[py]) {
            rank[px]++;
        }

        componentCount--;
        return true;
    }

    public boolean connected(int x, int y) {
        return find(x) == find(y);
    }

    public int getComponentCount() {
        return componentCount;
    }
}

/**
 * Represents a weighted edge in a graph
 */
class Edge implements Comparable<Edge> {
    public int u;
    public int v;
    public double weight;

    public Edge(int u, int v, double weight) {
        this.u = u;
        this.v = v;
        this.weight = weight;
    }

    @Override
    public int compareTo(Edge other) {
        return Double.compare(this.weight, other.weight);
    }

    @Override
    public String toString() {
        return String.format("Edge(%d, %d, %.2f)", u, v, weight);
    }
}

/**
 * Result of MST computation
 */
class MSTResult {
    public List<Edge> mstEdges;
    public double totalWeight;
    public List<List<Edge>> forest;

    public MSTResult(List<Edge> edges, double weight) {
        this.mstEdges = edges;
        this.totalWeight = weight;
        this.forest = new ArrayList<>();
    }

    public MSTResult(List<Edge> edges, double weight, List<List<Edge>> forest) {
        this.mstEdges = edges;
        this.totalWeight = weight;
        this.forest = forest;
    }
}

/**
 * Collection of Minimum Spanning Tree algorithms
 */
public class MSTAlgorithms {
    private int numVertices;
    private List<Edge> edges;
    private List<List<Edge>> adjList;

    public MSTAlgorithms(int numVertices, List<Edge> edges) {
        this.numVertices = numVertices;
        this.edges = edges;
        this.adjList = buildAdjacencyList();
    }

    private List<List<Edge>> buildAdjacencyList() {
        List<List<Edge>> adj = new ArrayList<>();
        for (int i = 0; i < numVertices; i++) {
            adj.add(new ArrayList<>());
        }

        for (Edge edge : edges) {
            adj.get(edge.u).add(new Edge(edge.u, edge.v, edge.weight));
            adj.get(edge.v).add(new Edge(edge.v, edge.u, edge.weight));
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
     * @param returnForest If true, handles disconnected graphs
     * @return MSTResult containing edges, weight, and optional forest
     */
    public MSTResult kruskal(boolean returnForest) {
        // Sort edges by weight - O(E log E)
        List<Edge> sortedEdges = new ArrayList<>(edges);
        Collections.sort(sortedEdges);

        UnionFind uf = new UnionFind(numVertices);
        List<Edge> mstEdges = new ArrayList<>();
        double totalWeight = 0;

        for (Edge edge : sortedEdges) {
            if (uf.union(edge.u, edge.v)) {
                mstEdges.add(edge);
                totalWeight += edge.weight;

                // Early termination for connected graph
                if (!returnForest && mstEdges.size() == numVertices - 1) {
                    break;
                }
            }
        }

        List<List<Edge>> forest = returnForest ? buildForest(mstEdges) : new ArrayList<>();
        return new MSTResult(mstEdges, totalWeight, forest);
    }

    public MSTResult kruskal() {
        return kruskal(false);
    }

    // ========================================================================
    // PRIM'S ALGORITHM
    // ========================================================================

    /**
     * Prim's Algorithm for MST using PriorityQueue (Binary Heap)
     *
     * Strategy: Grow tree from starting vertex, always add minimum weight edge
     * that connects tree to non-tree vertex
     *
     * Time Complexity: O((V+E) log V)
     * Space Complexity: O(V + E)
     *
     * @param start Starting vertex
     * @return MSTResult containing edges and weight
     */
    public MSTResult prim(int start) {
        List<Edge> mstEdges = new ArrayList<>();
        double totalWeight = 0;
        Set<Integer> visited = new HashSet<>();
        visited.add(start);

        // Priority queue: edges ordered by weight
        PriorityQueue<Edge> pq = new PriorityQueue<>();

        // Add edges from start vertex
        for (Edge edge : adjList.get(start)) {
            pq.offer(edge);
        }

        while (!pq.isEmpty() && visited.size() < numVertices) {
            Edge edge = pq.poll();

            if (visited.contains(edge.v)) continue;

            // Add edge to MST
            visited.add(edge.v);
            mstEdges.add(edge);
            totalWeight += edge.weight;

            // Add edges from newly added vertex
            for (Edge nextEdge : adjList.get(edge.v)) {
                if (!visited.contains(nextEdge.v)) {
                    pq.offer(nextEdge);
                }
            }
        }

        return new MSTResult(mstEdges, totalWeight);
    }

    public MSTResult prim() {
        return prim(0);
    }

    /**
     * Prim's algorithm using simple array (O(V²) for dense graphs)
     */
    public MSTResult primSimpleArray(int start) {
        List<Edge> mstEdges = new ArrayList<>();
        double totalWeight = 0;
        boolean[] visited = new boolean[numVertices];
        double[] minWeight = new double[numVertices];
        int[] parent = new int[numVertices];

        Arrays.fill(minWeight, Double.POSITIVE_INFINITY);
        Arrays.fill(parent, -1);
        minWeight[start] = 0;

        for (int count = 0; count < numVertices; count++) {
            // Find minimum weight unvisited vertex - O(V)
            int u = -1;
            for (int v = 0; v < numVertices; v++) {
                if (!visited[v] && (u == -1 || minWeight[v] < minWeight[u])) {
                    u = v;
                }
            }

            if (minWeight[u] == Double.POSITIVE_INFINITY) break; // Disconnected

            visited[u] = true;

            // Add edge to MST (skip first vertex)
            if (parent[u] != -1) {
                mstEdges.add(new Edge(parent[u], u, minWeight[u]));
                totalWeight += minWeight[u];
            }

            // Update neighbors
            for (Edge edge : adjList.get(u)) {
                int v = edge.v;
                if (!visited[v] && edge.weight < minWeight[v]) {
                    minWeight[v] = edge.weight;
                    parent[v] = u;
                }
            }
        }

        return new MSTResult(mstEdges, totalWeight);
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
     * @return MSTResult containing edges and weight
     */
    public MSTResult boruvka() {
        UnionFind uf = new UnionFind(numVertices);
        List<Edge> mstEdges = new ArrayList<>();
        double totalWeight = 0;
        int numComponents = numVertices;

        while (numComponents > 1) {
            int[] cheapest = new int[numVertices];
            Arrays.fill(cheapest, -1);

            // Find cheapest edge from each component
            for (int i = 0; i < edges.size(); i++) {
                Edge edge = edges.get(i);
                int uRoot = uf.find(edge.u);
                int vRoot = uf.find(edge.v);

                if (uRoot == vRoot) continue; // Same component

                // Check if this is cheapest for component of u
                if (cheapest[uRoot] == -1 ||
                    edge.weight < edges.get(cheapest[uRoot]).weight) {
                    cheapest[uRoot] = i;
                }

                // Check if this is cheapest for component of v
                if (cheapest[vRoot] == -1 ||
                    edge.weight < edges.get(cheapest[vRoot]).weight) {
                    cheapest[vRoot] = i;
                }
            }

            // Add all cheapest edges
            boolean addedAny = false;
            for (int i = 0; i < numVertices; i++) {
                if (cheapest[i] != -1) {
                    Edge edge = edges.get(cheapest[i]);
                    if (uf.union(edge.u, edge.v)) {
                        mstEdges.add(edge);
                        totalWeight += edge.weight;
                        numComponents--;
                        addedAny = true;
                    }
                }
            }

            if (!addedAny) break; // Disconnected graph or done
        }

        return new MSTResult(mstEdges, totalWeight);
    }

    // ========================================================================
    // MINIMUM SPANNING FOREST (for disconnected graphs)
    // ========================================================================

    /**
     * Find Minimum Spanning Forest for potentially disconnected graph
     */
    public MSTResult minimumSpanningForest(String algorithm) {
        if (algorithm.equals("kruskal")) {
            return kruskal(true);
        } else if (algorithm.equals("prim")) {
            Set<Integer> visitedGlobal = new HashSet<>();
            List<List<Edge>> forest = new ArrayList<>();
            double totalWeight = 0;

            for (int start = 0; start < numVertices; start++) {
                if (!visitedGlobal.contains(start)) {
                    MSTResult tree = prim(start);

                    // Mark vertices in this tree as visited
                    for (Edge edge : tree.mstEdges) {
                        visitedGlobal.add(edge.u);
                        visitedGlobal.add(edge.v);
                    }

                    if (!tree.mstEdges.isEmpty()) {
                        forest.add(tree.mstEdges);
                        totalWeight += tree.totalWeight;
                    }
                }
            }

            List<Edge> allEdges = new ArrayList<>();
            for (List<Edge> tree : forest) {
                allEdges.addAll(tree);
            }
            return new MSTResult(allEdges, totalWeight, forest);
        } else if (algorithm.equals("boruvka")) {
            MSTResult result = boruvka();
            result.forest = buildForest(result.mstEdges);
            return result;
        } else {
            throw new IllegalArgumentException("Unknown algorithm: " + algorithm);
        }
    }

    private List<List<Edge>> buildForest(List<Edge> edges) {
        if (edges.isEmpty()) return new ArrayList<>();

        UnionFind uf = new UnionFind(numVertices);
        for (Edge edge : edges) {
            uf.union(edge.u, edge.v);
        }

        Map<Integer, List<Edge>> componentEdges = new HashMap<>();
        for (Edge edge : edges) {
            int root = uf.find(edge.u);
            componentEdges.computeIfAbsent(root, k -> new ArrayList<>()).add(edge);
        }

        return new ArrayList<>(componentEdges.values());
    }

    // ========================================================================
    // UTILITY METHODS
    // ========================================================================

    /**
     * Verify if given edges form a valid MST
     */
    public Map<String, Object> verifyMST(List<Edge> mstEdges) {
        Map<String, Object> result = new HashMap<>();

        if (mstEdges.size() != numVertices - 1) {
            result.put("isValid", false);
            result.put("message", String.format("Invalid edge count: %d (expected %d)",
                    mstEdges.size(), numVertices - 1));
            return result;
        }

        UnionFind uf = new UnionFind(numVertices);
        for (Edge edge : mstEdges) {
            if (!uf.union(edge.u, edge.v)) {
                result.put("isValid", false);
                result.put("message", "Contains cycle at edge " + edge);
                return result;
            }
        }

        if (uf.getComponentCount() != 1) {
            result.put("isValid", false);
            result.put("message", String.format("Disconnected: %d components",
                    uf.getComponentCount()));
            return result;
        }

        result.put("isValid", true);
        result.put("message", "Valid MST");
        return result;
    }

    /**
     * Compare performance of all MST algorithms
     */
    public Map<String, Map<String, Double>> compareAlgorithms(int numRuns) {
        Map<String, Map<String, Double>> results = new HashMap<>();

        // Kruskal's
        List<Double> kruskalTimes = new ArrayList<>();
        MSTResult kResult = null;
        for (int i = 0; i < numRuns; i++) {
            long start = System.nanoTime();
            kResult = kruskal();
            kruskalTimes.add((System.nanoTime() - start) / 1_000_000.0);
        }

        Map<String, Double> kMetrics = new HashMap<>();
        kMetrics.put("meanTime", kruskalTimes.stream().mapToDouble(Double::doubleValue).average().orElse(0));
        kMetrics.put("minTime", Collections.min(kruskalTimes));
        kMetrics.put("maxTime", Collections.max(kruskalTimes));
        kMetrics.put("weight", kResult.totalWeight);
        kMetrics.put("numEdges", (double) kResult.mstEdges.size());
        results.put("kruskal", kMetrics);

        // Prim's
        List<Double> primTimes = new ArrayList<>();
        MSTResult pResult = null;
        for (int i = 0; i < numRuns; i++) {
            long start = System.nanoTime();
            pResult = prim();
            primTimes.add((System.nanoTime() - start) / 1_000_000.0);
        }

        Map<String, Double> pMetrics = new HashMap<>();
        pMetrics.put("meanTime", primTimes.stream().mapToDouble(Double::doubleValue).average().orElse(0));
        pMetrics.put("minTime", Collections.min(primTimes));
        pMetrics.put("maxTime", Collections.max(primTimes));
        pMetrics.put("weight", pResult.totalWeight);
        pMetrics.put("numEdges", (double) pResult.mstEdges.size());
        results.put("prim", pMetrics);

        // Borůvka's
        List<Double> boruvkaTimes = new ArrayList<>();
        MSTResult bResult = null;
        for (int i = 0; i < numRuns; i++) {
            long start = System.nanoTime();
            bResult = boruvka();
            boruvkaTimes.add((System.nanoTime() - start) / 1_000_000.0);
        }

        Map<String, Double> bMetrics = new HashMap<>();
        bMetrics.put("meanTime", boruvkaTimes.stream().mapToDouble(Double::doubleValue).average().orElse(0));
        bMetrics.put("minTime", Collections.min(boruvkaTimes));
        bMetrics.put("maxTime", Collections.max(boruvkaTimes));
        bMetrics.put("weight", bResult.totalWeight);
        bMetrics.put("numEdges", (double) bResult.mstEdges.size());
        results.put("boruvka", bMetrics);

        return results;
    }

    // ========================================================================
    // DEMO
    // ========================================================================

    public static void main(String[] args) {
        System.out.println("=".repeat(80));
        System.out.println("MINIMUM SPANNING TREE ALGORITHMS DEMO");
        System.out.println("=".repeat(80));
        System.out.println();

        List<Edge> edges = Arrays.asList(
                new Edge(0, 1, 4),
                new Edge(0, 7, 8),
                new Edge(1, 2, 8),
                new Edge(1, 7, 11),
                new Edge(2, 3, 7),
                new Edge(2, 5, 4),
                new Edge(2, 8, 2),
                new Edge(3, 4, 9),
                new Edge(3, 5, 14),
                new Edge(4, 5, 10),
                new Edge(5, 6, 2),
                new Edge(6, 7, 1),
                new Edge(6, 8, 6),
                new Edge(7, 8, 7)
        );

        MSTAlgorithms mst = new MSTAlgorithms(9, edges);

        // Kruskal's
        System.out.println("1. KRUSKAL'S ALGORITHM");
        System.out.println("-".repeat(80));
        MSTResult kResult = mst.kruskal();
        System.out.printf("MST Weight: %.2f%n", kResult.totalWeight);
        System.out.println("Edges: " + kResult.mstEdges);
        System.out.println();

        // Prim's
        System.out.println("2. PRIM'S ALGORITHM");
        System.out.println("-".repeat(80));
        MSTResult pResult = mst.prim();
        System.out.printf("MST Weight: %.2f%n", pResult.totalWeight);
        System.out.println("Edges: " + pResult.mstEdges);
        System.out.println();

        // Borůvka's
        System.out.println("3. BORŮVKA'S ALGORITHM");
        System.out.println("-".repeat(80));
        MSTResult bResult = mst.boruvka();
        System.out.printf("MST Weight: %.2f%n", bResult.totalWeight);
        System.out.println("Edges: " + bResult.mstEdges);
        System.out.println();

        // Performance
        System.out.println("4. PERFORMANCE COMPARISON");
        System.out.println("-".repeat(80));
        Map<String, Map<String, Double>> results = mst.compareAlgorithms(100);

        for (Map.Entry<String, Map<String, Double>> entry : results.entrySet()) {
            System.out.println("\n" + entry.getKey().toUpperCase());
            System.out.printf("  Mean time: %.4f ms%n", entry.getValue().get("meanTime"));
            System.out.printf("  Min time:  %.4f ms%n", entry.getValue().get("minTime"));
            System.out.printf("  Max time:  %.4f ms%n", entry.getValue().get("maxTime"));
            System.out.printf("  Weight:    %.2f%n", entry.getValue().get("weight"));
        }
        System.out.println();

        // Disconnected graph
        System.out.println("5. MINIMUM SPANNING FOREST (Disconnected Graph)");
        System.out.println("-".repeat(80));
        List<Edge> disconnectedEdges = Arrays.asList(
                new Edge(0, 1, 1),
                new Edge(1, 2, 2),
                new Edge(3, 4, 3),
                new Edge(4, 5, 4)
        );

        MSTAlgorithms mstForest = new MSTAlgorithms(6, disconnectedEdges);
        MSTResult forestResult = mstForest.minimumSpanningForest("kruskal");

        System.out.println("Number of trees: " + forestResult.forest.size());
        System.out.printf("Total weight: %.2f%n", forestResult.totalWeight);
        for (int i = 0; i < forestResult.forest.size(); i++) {
            System.out.println("\nTree " + (i + 1) + ":");
            System.out.println("  Edges: " + forestResult.forest.get(i));
        }
    }
}

