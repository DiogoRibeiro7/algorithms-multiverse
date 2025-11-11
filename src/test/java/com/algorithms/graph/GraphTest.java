package com.algorithms.graph;

/**
 * Comprehensive unit tests for Graph.java
 *
 * Compile and run:
 *    javac Graph.java GraphTest.java
 *    java GraphTest
 */

import java.util.*;

public class GraphTest {
    private static int passed = 0;
    private static int failed = 0;

    // Simple test assertion methods
    private static void assertTrue(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }

    private static void assertFalse(boolean condition, String message) {
        assertTrue(!condition, message);
    }

    private static void assertEqual(Object actual, Object expected, String message) {
        if (!Objects.equals(actual, expected)) {
            throw new AssertionError(message + ": expected " + expected + " but got " + actual);
        }
    }

    private static void assertNotNull(Object obj, String message) {
        if (obj == null) {
            throw new AssertionError(message + ": object was null");
        }
    }

    private static void assertNull(Object obj, String message) {
        if (obj != null) {
            throw new AssertionError(message + ": expected null but got " + obj);
        }
    }

    private static void test(String name, Runnable testFn) {
        try {
            testFn.run();
            System.out.println("✓ " + name);
            passed++;
        } catch (Exception e) {
            System.out.println("✗ " + name);
            System.out.println("  " + e.getMessage());
            failed++;
        }
    }

    public static void main(String[] args) {
        System.out.println("Running tests...\n");

        // Graph Creation Tests
        test("Create empty graph", () -> {
            Graph g = new Graph(0, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            assertEqual(g.numVertices, 0, "Vertex count");
            assertEqual(g.numEdges, 0, "Edge count");
        });

        test("Create graph with vertices", () -> {
            Graph g = new Graph(5, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            assertEqual(g.numVertices, 5, "Vertex count");
            assertEqual(g.numEdges, 0, "Edge count");
        });

        test("Add vertex", () -> {
            Graph g = new Graph(2, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            int vertexId = g.addVertex();
            assertEqual(vertexId, 2, "New vertex ID");
            assertEqual(g.numVertices, 3, "Vertex count after adding");
        });

        test("Add edge to undirected graph", () -> {
            Graph g = new Graph(3, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g.addEdge(0, 1, 5.0);
            assertEqual(g.numEdges, 1, "Edge count");

            List<Neighbor> neighbors = g.getNeighbors(0);
            assertEqual(neighbors.size(), 1, "Neighbor count");
            assertEqual(neighbors.get(0).vertex, 1, "Neighbor vertex");
        });

        test("Add edge to directed graph", () -> {
            Graph g = new Graph(3, GraphType.DIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g.addEdge(0, 1);
            assertEqual(g.numEdges, 1, "Edge count");

            assertEqual(g.getNeighbors(0).size(), 1, "Source neighbors");
            assertEqual(g.getNeighbors(1).size(), 0, "Dest neighbors");
        });

        test("Invalid edge throws exception", () -> {
            Graph g = new Graph(3, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            try {
                g.addEdge(0, 5);
                throw new AssertionError("Should have thrown exception");
            } catch (IllegalArgumentException e) {
                // Expected
            }
        });

        // DFS Tests
        test("DFS recursive", () -> {
            Graph g = new Graph(5, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g.addEdge(0, 1);
            g.addEdge(0, 4);
            g.addEdge(1, 2);
            g.addEdge(1, 3);

            List<Integer> traversal = g.dfsRecursive(0);
            assertEqual(traversal.size(), 5, "Traversal size");
            assertEqual(traversal.get(0), 0, "Start vertex");
        });

        test("DFS iterative", () -> {
            Graph g = new Graph(5, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g.addEdge(0, 1);
            g.addEdge(0, 4);
            g.addEdge(1, 2);
            g.addEdge(1, 3);

            List<Integer> traversal = g.dfsIterative(0);
            assertEqual(traversal.size(), 5, "Traversal size");
            assertEqual(traversal.get(0), 0, "Start vertex");
        });

        // BFS Tests
        test("BFS traversal", () -> {
            Graph g = new Graph(5, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g.addEdge(0, 1);
            g.addEdge(0, 4);
            g.addEdge(1, 2);
            g.addEdge(1, 3);

            List<Integer> traversal = g.bfs(0);
            assertEqual(traversal.size(), 5, "Traversal size");
            assertEqual(traversal.get(0), 0, "Start vertex");
        });

        // Topological Sort Tests
        test("Topological sort on DAG", () -> {
            Graph g = new Graph(6, GraphType.DIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g.addEdge(5, 2);
            g.addEdge(5, 0);
            g.addEdge(4, 0);
            g.addEdge(4, 1);
            g.addEdge(2, 3);
            g.addEdge(3, 1);

            List<Integer> topo = g.topologicalSort();
            assertNotNull(topo, "Topological sort result");
            assertEqual(topo.size(), 6, "Topological sort size");

            // Verify ordering
            Map<Integer, Integer> position = new HashMap<>();
            for (int i = 0; i < topo.size(); i++) {
                position.put(topo.get(i), i);
            }

            for (int u = 0; u < g.numVertices; u++) {
                for (Neighbor neighbor : g.getNeighbors(u)) {
                    assertTrue(position.get(u) < position.get(neighbor.vertex),
                        "Topological order violated");
                }
            }
        });

        test("Topological sort DFS", () -> {
            Graph g = new Graph(4, GraphType.DIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g.addEdge(0, 1);
            g.addEdge(0, 2);
            g.addEdge(1, 2);
            g.addEdge(2, 3);

            List<Integer> topo = g.topologicalSortDFS();
            assertNotNull(topo, "Topological sort DFS result");
            assertEqual(topo.size(), 4, "Topological sort size");
        });

        test("Topological sort detects cycle", () -> {
            Graph g = new Graph(3, GraphType.DIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g.addEdge(0, 1);
            g.addEdge(1, 2);
            g.addEdge(2, 0);

            List<Integer> topo = g.topologicalSort();
            assertNull(topo, "Should return null for cyclic graph");
        });

        // Connected Components Tests
        test("Single connected component", () -> {
            Graph g = new Graph(4, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g.addEdge(0, 1);
            g.addEdge(1, 2);
            g.addEdge(2, 3);

            List<List<Integer>> components = g.findConnectedComponents();
            assertEqual(components.size(), 1, "Number of components");
            assertEqual(components.get(0).size(), 4, "Component size");
        });

        test("Multiple connected components", () -> {
            Graph g = new Graph(7, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g.addEdge(0, 1);
            g.addEdge(1, 2);
            g.addEdge(3, 4);
            g.addEdge(5, 6);

            List<List<Integer>> components = g.findConnectedComponents();
            assertEqual(components.size(), 3, "Number of components");
        });

        test("Is connected", () -> {
            Graph g1 = new Graph(3, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g1.addEdge(0, 1);
            g1.addEdge(1, 2);
            assertTrue(g1.isConnected(), "Connected graph");

            Graph g2 = new Graph(4, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g2.addEdge(0, 1);
            g2.addEdge(2, 3);
            assertFalse(g2.isConnected(), "Disconnected graph");
        });

        // Cycle Detection Tests
        test("Undirected graph has cycle", () -> {
            Graph g = new Graph(5, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g.addEdge(0, 1);
            g.addEdge(1, 2);
            g.addEdge(2, 3);
            g.addEdge(3, 4);
            g.addEdge(4, 0);

            assertTrue(g.hasCycle(), "Should detect cycle");
        });

        test("Undirected graph no cycle", () -> {
            Graph g = new Graph(4, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g.addEdge(0, 1);
            g.addEdge(1, 2);
            g.addEdge(2, 3);

            assertFalse(g.hasCycle(), "Should not detect cycle");
        });

        test("Directed graph has cycle", () -> {
            Graph g = new Graph(3, GraphType.DIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g.addEdge(0, 1);
            g.addEdge(1, 2);
            g.addEdge(2, 0);

            assertTrue(g.hasCycle(), "Should detect cycle");
        });

        test("Directed graph no cycle (DAG)", () -> {
            Graph g = new Graph(4, GraphType.DIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g.addEdge(0, 1);
            g.addEdge(0, 2);
            g.addEdge(1, 3);
            g.addEdge(2, 3);

            assertFalse(g.hasCycle(), "DAG should not have cycle");
        });

        // Graph Coloring Tests
        test("Greedy coloring", () -> {
            Graph g = new Graph(5, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g.addEdge(0, 1);
            g.addEdge(0, 2);
            g.addEdge(1, 2);
            g.addEdge(1, 3);
            g.addEdge(2, 3);
            g.addEdge(3, 4);

            Map<Integer, Integer> coloring = g.greedyColoring();

            assertEqual(coloring.size(), 5, "All vertices colored");

            // Check no adjacent vertices have same color
            for (int u = 0; u < g.numVertices; u++) {
                for (Neighbor neighbor : g.getNeighbors(u)) {
                    assertTrue(!coloring.get(u).equals(coloring.get(neighbor.vertex)),
                        "Adjacent vertices have same color");
                }
            }
        });

        test("Chromatic number complete graph", () -> {
            Graph g = Graph.GraphGenerator.completeGraph(4);
            int chromatic = g.chromaticNumberUpperBound();

            assertEqual(chromatic, 4, "Complete graph K4 chromatic number");
        });

        // Graph Generator Tests
        test("Complete graph generator", () -> {
            Graph g = Graph.GraphGenerator.completeGraph(5);

            assertEqual(g.numVertices, 5, "Vertex count");
            assertEqual(g.numEdges, 10, "Edge count for K5");

            for (int v = 0; v < 5; v++) {
                assertEqual(g.getNeighbors(v).size(), 4, "Vertex degree");
            }
        });

        test("Cycle graph generator", () -> {
            Graph g = Graph.GraphGenerator.cycleGraph(6);

            assertEqual(g.numVertices, 6, "Vertex count");
            assertEqual(g.numEdges, 6, "Edge count");

            for (int v = 0; v < 6; v++) {
                assertEqual(g.getNeighbors(v).size(), 2, "Vertex degree");
            }
        });

        test("Random graph generator", () -> {
            Graph g = Graph.GraphGenerator.randomGraph(10, 0.5);

            assertEqual(g.numVertices, 10, "Vertex count");
            assertTrue(g.numEdges > 0, "Should have edges");
        });

        test("DAG generator", () -> {
            Graph g = Graph.GraphGenerator.dag(10, 0.3);

            assertEqual(g.numVertices, 10, "Vertex count");
            assertFalse(g.hasCycle(), "DAG should not have cycle");

            List<Integer> topo = g.topologicalSort();
            assertNotNull(topo, "Should be able to topologically sort");
        });

        // Adjacency Matrix Tests
        test("Adjacency matrix weighted edges", () -> {
            Graph g = new Graph(4, GraphType.DIRECTED, true,
                RepresentationType.ADJACENCY_MATRIX);
            g.addEdge(0, 1, 2.5);
            g.addEdge(0, 2, 1.0);

            List<Neighbor> neighbors = g.getNeighbors(0);
            assertEqual(neighbors.size(), 2, "Neighbor count");
        });

        // Visualization Tests
        test("ASCII visualization", () -> {
            Graph g = new Graph(3, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);
            g.addEdge(0, 1);
            g.addEdge(1, 2);

            String ascii = g.toASCII();
            assertTrue(ascii.contains("Graph:"), "Contains graph info");
            assertTrue(ascii.contains("Vertices: 3"), "Contains vertex count");
        });

        // Edge Cases
        test("Empty graph operations", () -> {
            Graph g = new Graph(0, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);

            assertEqual(g.findConnectedComponents().size(), 0, "No components");
            assertTrue(g.isConnected(), "Empty graph is connected");
        });

        test("Single vertex graph", () -> {
            Graph g = new Graph(1, GraphType.UNDIRECTED, false,
                RepresentationType.ADJACENCY_LIST);

            List<List<Integer>> components = g.findConnectedComponents();
            assertEqual(components.size(), 1, "One component");
            assertEqual(components.get(0).get(0), 0, "Contains vertex 0");
        });

        // Print results
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed > 0 ? 1 : 0);
    }
}

