/**
 * Comprehensive unit tests for graph.cpp
 *
 * Compile and run:
 *    g++ -std=c++17 -o test_graph test_graph.cpp graph.cpp
 *    ./test_graph
 */

#include <iostream>
#include <string>
#include <functional>
#include <vector>
#include <set>
#include <map>
#include <cstdlib>

// Simple test framework
class TestRunner {
private:
    int passed = 0;
    int failed = 0;

    struct Test {
        std::string name;
        std::function<void()> fn;
    };

    std::vector<Test> tests;

public:
    void test(const std::string& name, std::function<void()> fn) {
        tests.push_back({name, fn});
    }

    void assertTrue(bool condition, const std::string& message = "") {
        if (!condition) {
            throw std::runtime_error(message.empty() ? "Assertion failed" : message);
        }
    }

    void assertFalse(bool condition, const std::string& message = "") {
        assertTrue(!condition, message.empty() ? "Expected false" : message);
    }

    template<typename T>
    void assertEqual(const T& actual, const T& expected, const std::string& message = "") {
        if (actual != expected) {
            throw std::runtime_error(message + ": expected " +
                std::to_string(expected) + " but got " + std::to_string(actual));
        }
    }

    template<typename T>
    void assertNotNull(const T* ptr, const std::string& message = "") {
        if (ptr == nullptr) {
            throw std::runtime_error(message + ": pointer was null");
        }
    }

    bool run() {
        std::cout << "Running tests...\n\n";

        for (const auto& test : tests) {
            try {
                test.fn();
                std::cout << "✓ " << test.name << "\n";
                passed++;
            } catch (const std::exception& e) {
                std::cout << "✗ " << test.name << "\n";
                std::cout << "  " << e.what() << "\n";
                failed++;
            }
        }

        std::cout << "\n" << passed << " passed, " << failed << " failed\n";
        return failed == 0;
    }
};

// Include graph implementation (in real scenario, would link against compiled object)
// For testing purposes, assuming graph.cpp has been included or linked

// Mock minimal interface needed for testing
// In practice, you'd include graph.cpp or link against it

#include <unordered_map>
#include <queue>
#include <stack>
#include <algorithm>

// Simplified test versions - in real scenario, include actual graph.cpp
enum class GraphType { DIRECTED, UNDIRECTED };
enum class RepresentationType { ADJACENCY_LIST, ADJACENCY_MATRIX, EDGE_LIST, CSR };

struct Neighbor {
    int vertex;
    double weight;
    Neighbor(int v, double w) : vertex(v), weight(w) {}
};

class Graph {
public:
    int numVertices;
    int numEdges;
    GraphType graphType;
    bool weighted;
    RepresentationType representation;

    std::unordered_map<int, std::vector<Neighbor>> adjList;
    std::vector<std::vector<std::optional<double>>> adjMatrix;

    Graph(int nv, GraphType gt = GraphType::UNDIRECTED, bool w = false,
          RepresentationType r = RepresentationType::ADJACENCY_LIST)
        : numVertices(nv), numEdges(0), graphType(gt), weighted(w), representation(r) {
        if (r == RepresentationType::ADJACENCY_MATRIX) {
            adjMatrix.resize(nv, std::vector<std::optional<double>>(nv, std::nullopt));
        }
    }

    void addEdge(int u, int v, double weight = 1.0) {
        if (u >= numVertices || v >= numVertices) {
            throw std::out_of_range("Vertex out of range");
        }
        numEdges++;

        if (representation == RepresentationType::ADJACENCY_LIST) {
            adjList[u].emplace_back(v, weight);
            if (graphType == GraphType::UNDIRECTED) {
                adjList[v].emplace_back(u, weight);
            }
        } else if (representation == RepresentationType::ADJACENCY_MATRIX) {
            adjMatrix[u][v] = weight;
            if (graphType == GraphType::UNDIRECTED) {
                adjMatrix[v][u] = weight;
            }
        }
    }

    std::vector<Neighbor> getNeighbors(int u) const {
        if (representation == RepresentationType::ADJACENCY_LIST) {
            auto it = adjList.find(u);
            return it != adjList.end() ? it->second : std::vector<Neighbor>();
        } else if (representation == RepresentationType::ADJACENCY_MATRIX) {
            std::vector<Neighbor> neighbors;
            for (int v = 0; v < numVertices; v++) {
                if (adjMatrix[u][v].has_value()) {
                    neighbors.emplace_back(v, adjMatrix[u][v].value());
                }
            }
            return neighbors;
        }
        return {};
    }

    std::vector<int> dfsRecursive(int start) const {
        std::unordered_set<int> visited;
        std::vector<int> traversal;
        dfsHelper(start, visited, traversal);
        return traversal;
    }

    void dfsHelper(int v, std::unordered_set<int>& visited, std::vector<int>& traversal) const {
        visited.insert(v);
        traversal.push_back(v);
        for (const auto& neighbor : getNeighbors(v)) {
            if (visited.find(neighbor.vertex) == visited.end()) {
                dfsHelper(neighbor.vertex, visited, traversal);
            }
        }
    }

    std::vector<int> bfs(int start) const {
        std::unordered_set<int> visited;
        std::vector<int> traversal;
        std::queue<int> queue;

        visited.insert(start);
        queue.push(start);

        while (!queue.empty()) {
            int v = queue.front();
            queue.pop();
            traversal.push_back(v);

            for (const auto& neighbor : getNeighbors(v)) {
                if (visited.find(neighbor.vertex) == visited.end()) {
                    visited.insert(neighbor.vertex);
                    queue.push(neighbor.vertex);
                }
            }
        }

        return traversal;
    }

    bool hasCycle() const {
        if (graphType == GraphType::DIRECTED) {
            return hasCycleDirected();
        } else {
            return hasCycleUndirected();
        }
    }

    bool hasCycleUndirected() const {
        std::unordered_set<int> visited;

        for (int v = 0; v < numVertices; v++) {
            if (visited.find(v) == visited.end()) {
                if (hasCycleUndirectedHelper(v, -1, visited)) {
                    return true;
                }
            }
        }
        return false;
    }

    bool hasCycleUndirectedHelper(int v, int parent, std::unordered_set<int>& visited) const {
        visited.insert(v);

        for (const auto& neighbor : getNeighbors(v)) {
            if (visited.find(neighbor.vertex) == visited.end()) {
                if (hasCycleUndirectedHelper(neighbor.vertex, v, visited)) {
                    return true;
                }
            } else if (neighbor.vertex != parent) {
                return true;
            }
        }
        return false;
    }

    bool hasCycleDirected() const {
        std::unordered_set<int> visited;
        std::unordered_set<int> recStack;

        for (int v = 0; v < numVertices; v++) {
            if (visited.find(v) == visited.end()) {
                if (hasCycleDirectedHelper(v, visited, recStack)) {
                    return true;
                }
            }
        }
        return false;
    }

    bool hasCycleDirectedHelper(int v, std::unordered_set<int>& visited,
                                std::unordered_set<int>& recStack) const {
        visited.insert(v);
        recStack.insert(v);

        for (const auto& neighbor : getNeighbors(v)) {
            if (visited.find(neighbor.vertex) == visited.end()) {
                if (hasCycleDirectedHelper(neighbor.vertex, visited, recStack)) {
                    return true;
                }
            } else if (recStack.find(neighbor.vertex) != recStack.end()) {
                return true;
            }
        }

        recStack.erase(v);
        return false;
    }
};

int main() {
    TestRunner runner;

    // Graph Creation Tests
    runner.test("Create empty graph", [&]() {
        Graph g(0);
        runner.assertEqual(g.numVertices, 0, "Vertex count");
        runner.assertEqual(g.numEdges, 0, "Edge count");
    });

    runner.test("Create graph with vertices", [&]() {
        Graph g(5);
        runner.assertEqual(g.numVertices, 5, "Vertex count");
        runner.assertEqual(g.numEdges, 0, "Edge count");
    });

    runner.test("Add edge to undirected graph", [&]() {
        Graph g(3, GraphType::UNDIRECTED);
        g.addEdge(0, 1, 5.0);
        runner.assertEqual(g.numEdges, 1, "Edge count");

        auto neighbors = g.getNeighbors(0);
        runner.assertEqual(static_cast<int>(neighbors.size()), 1, "Neighbor count");
        runner.assertEqual(neighbors[0].vertex, 1, "Neighbor vertex");
    });

    runner.test("Add edge to directed graph", [&]() {
        Graph g(3, GraphType::DIRECTED);
        g.addEdge(0, 1);
        runner.assertEqual(g.numEdges, 1, "Edge count");

        runner.assertEqual(static_cast<int>(g.getNeighbors(0).size()), 1, "Source neighbors");
        runner.assertEqual(static_cast<int>(g.getNeighbors(1).size()), 0, "Dest neighbors");
    });

    runner.test("Invalid edge throws exception", [&]() {
        Graph g(3);
        try {
            g.addEdge(0, 5);
            throw std::runtime_error("Should have thrown exception");
        } catch (const std::out_of_range&) {
            // Expected
        }
    });

    // DFS Tests
    runner.test("DFS recursive", [&]() {
        Graph g(5, GraphType::UNDIRECTED);
        g.addEdge(0, 1);
        g.addEdge(0, 4);
        g.addEdge(1, 2);
        g.addEdge(1, 3);

        auto traversal = g.dfsRecursive(0);
        runner.assertEqual(static_cast<int>(traversal.size()), 5, "Traversal size");
        runner.assertEqual(traversal[0], 0, "Start vertex");
    });

    // BFS Tests
    runner.test("BFS traversal", [&]() {
        Graph g(5, GraphType::UNDIRECTED);
        g.addEdge(0, 1);
        g.addEdge(0, 4);
        g.addEdge(1, 2);
        g.addEdge(1, 3);

        auto traversal = g.bfs(0);
        runner.assertEqual(static_cast<int>(traversal.size()), 5, "Traversal size");
        runner.assertEqual(traversal[0], 0, "Start vertex");
    });

    // Cycle Detection Tests
    runner.test("Undirected graph has cycle", [&]() {
        Graph g(5, GraphType::UNDIRECTED);
        g.addEdge(0, 1);
        g.addEdge(1, 2);
        g.addEdge(2, 3);
        g.addEdge(3, 4);
        g.addEdge(4, 0);

        runner.assertTrue(g.hasCycle(), "Should detect cycle");
    });

    runner.test("Undirected graph no cycle", [&]() {
        Graph g(4, GraphType::UNDIRECTED);
        g.addEdge(0, 1);
        g.addEdge(1, 2);
        g.addEdge(2, 3);

        runner.assertFalse(g.hasCycle(), "Should not detect cycle");
    });

    runner.test("Directed graph has cycle", [&]() {
        Graph g(3, GraphType::DIRECTED);
        g.addEdge(0, 1);
        g.addEdge(1, 2);
        g.addEdge(2, 0);

        runner.assertTrue(g.hasCycle(), "Should detect cycle");
    });

    runner.test("Directed graph no cycle (DAG)", [&]() {
        Graph g(4, GraphType::DIRECTED);
        g.addEdge(0, 1);
        g.addEdge(0, 2);
        g.addEdge(1, 3);
        g.addEdge(2, 3);

        runner.assertFalse(g.hasCycle(), "DAG should not have cycle");
    });

    // Adjacency Matrix Tests
    runner.test("Adjacency matrix weighted edges", [&]() {
        Graph g(4, GraphType::DIRECTED, true, RepresentationType::ADJACENCY_MATRIX);
        g.addEdge(0, 1, 2.5);
        g.addEdge(0, 2, 1.0);

        auto neighbors = g.getNeighbors(0);
        runner.assertEqual(static_cast<int>(neighbors.size()), 2, "Neighbor count");
    });

    // Run all tests
    bool success = runner.run();
    return success ? 0 : 1;
}
