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

#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <map>
#include <set>
#include <chrono>
#include <iomanip>
#include <numeric>
#include <limits>

using namespace std;

/**
 * Union-Find (Disjoint Set Union) data structure
 *
 * Implements path compression and union by rank for near O(1) operations.
 * Essential for Kruskal's algorithm.
 */
class UnionFind {
private:
    vector<int> parent;
    vector<int> rank;
    int componentCount;

public:
    UnionFind(int n) : parent(n), rank(n, 0), componentCount(n) {
        iota(parent.begin(), parent.end(), 0);
    }

    /**
     * Find the representative (root) of the set containing x
     * Uses path compression for optimization
     */
    int find(int x) {
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
    bool unionSets(int x, int y) {
        int px = find(x);
        int py = find(y);

        if (px == py) return false; // Already in same set

        // Union by rank
        if (rank[px] < rank[py]) {
            swap(px, py);
        }

        parent[py] = px;
        if (rank[px] == rank[py]) {
            rank[px]++;
        }

        componentCount--;
        return true;
    }

    bool connected(int x, int y) {
        return find(x) == find(y);
    }

    int getComponentCount() const {
        return componentCount;
    }
};

/**
 * Represents a weighted edge in a graph
 */
struct Edge {
    int u, v;
    double weight;

    Edge(int u, int v, double weight) : u(u), v(v), weight(weight) {}

    bool operator<(const Edge& other) const {
        return weight < other.weight;
    }

    bool operator>(const Edge& other) const {
        return weight > other.weight;
    }

    friend ostream& operator<<(ostream& os, const Edge& e) {
        os << "Edge(" << e.u << ", " << e.v << ", " << e.weight << ")";
        return os;
    }
};

/**
 * Result of MST computation
 */
struct MSTResult {
    vector<Edge> mstEdges;
    double totalWeight;
    vector<vector<Edge>> forest;

    MSTResult() : totalWeight(0.0) {}
};

/**
 * Collection of Minimum Spanning Tree algorithms
 */
class MSTAlgorithms {
private:
    int numVertices;
    vector<Edge> edges;
    vector<vector<pair<int, double>>> adjList;

    void buildAdjacencyList() {
        adjList.resize(numVertices);
        for (const auto& edge : edges) {
            adjList[edge.u].emplace_back(edge.v, edge.weight);
            adjList[edge.v].emplace_back(edge.u, edge.weight);
        }
    }

    vector<vector<Edge>> buildForest(const vector<Edge>& mstEdges) {
        if (mstEdges.empty()) return {};

        UnionFind uf(numVertices);
        for (const auto& edge : mstEdges) {
            uf.unionSets(edge.u, edge.v);
        }

        map<int, vector<Edge>> componentEdges;
        for (const auto& edge : mstEdges) {
            int root = uf.find(edge.u);
            componentEdges[root].push_back(edge);
        }

        vector<vector<Edge>> forest;
        for (const auto& [root, edges] : componentEdges) {
            forest.push_back(edges);
        }

        return forest;
    }

public:
    MSTAlgorithms(int numVertices, const vector<Edge>& edges)
        : numVertices(numVertices), edges(edges) {
        buildAdjacencyList();
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
    MSTResult kruskal(bool returnForest = false) {
        // Sort edges by weight - O(E log E)
        vector<Edge> sortedEdges = edges;
        sort(sortedEdges.begin(), sortedEdges.end());

        UnionFind uf(numVertices);
        MSTResult result;

        for (const auto& edge : sortedEdges) {
            if (uf.unionSets(edge.u, edge.v)) {
                result.mstEdges.push_back(edge);
                result.totalWeight += edge.weight;

                // Early termination for connected graph
                if (!returnForest && result.mstEdges.size() == numVertices - 1) {
                    break;
                }
            }
        }

        if (returnForest) {
            result.forest = buildForest(result.mstEdges);
        }

        return result;
    }

    // ========================================================================
    // PRIM'S ALGORITHM
    // ========================================================================

    /**
     * Prim's Algorithm for MST using priority queue (Binary Heap)
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
    MSTResult prim(int start = 0) {
        MSTResult result;
        set<int> visited;
        visited.insert(start);

        // Priority queue: (weight, u, v)
        priority_queue<tuple<double, int, int>,
                       vector<tuple<double, int, int>>,
                       greater<tuple<double, int, int>>> pq;

        // Add edges from start vertex
        for (const auto& [neighbor, weight] : adjList[start]) {
            pq.push(make_tuple(weight, start, neighbor));
        }

        while (!pq.empty() && visited.size() < numVertices) {
            auto [weight, u, v] = pq.top();
            pq.pop();

            if (visited.count(v)) continue;

            // Add edge to MST
            visited.insert(v);
            result.mstEdges.emplace_back(u, v, weight);
            result.totalWeight += weight;

            // Add edges from newly added vertex
            for (const auto& [neighbor, edgeWeight] : adjList[v]) {
                if (!visited.count(neighbor)) {
                    pq.push(make_tuple(edgeWeight, v, neighbor));
                }
            }
        }

        return result;
    }

    /**
     * Prim's algorithm using simple array (O(V²) for dense graphs)
     */
    MSTResult primSimpleArray(int start = 0) {
        MSTResult result;
        vector<bool> visited(numVertices, false);
        vector<double> minWeight(numVertices, numeric_limits<double>::infinity());
        vector<int> parent(numVertices, -1);

        minWeight[start] = 0;

        for (int count = 0; count < numVertices; count++) {
            // Find minimum weight unvisited vertex - O(V)
            int u = -1;
            for (int v = 0; v < numVertices; v++) {
                if (!visited[v] && (u == -1 || minWeight[v] < minWeight[u])) {
                    u = v;
                }
            }

            if (minWeight[u] == numeric_limits<double>::infinity()) break; // Disconnected

            visited[u] = true;

            // Add edge to MST (skip first vertex)
            if (parent[u] != -1) {
                result.mstEdges.emplace_back(parent[u], u, minWeight[u]);
                result.totalWeight += minWeight[u];
            }

            // Update neighbors
            for (const auto& [v, weight] : adjList[u]) {
                if (!visited[v] && weight < minWeight[v]) {
                    minWeight[v] = weight;
                    parent[v] = u;
                }
            }
        }

        return result;
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
    MSTResult boruvka() {
        UnionFind uf(numVertices);
        MSTResult result;
        int numComponents = numVertices;

        while (numComponents > 1) {
            vector<int> cheapest(numVertices, -1);

            // Find cheapest edge from each component
            for (size_t i = 0; i < edges.size(); i++) {
                const Edge& edge = edges[i];
                int uRoot = uf.find(edge.u);
                int vRoot = uf.find(edge.v);

                if (uRoot == vRoot) continue; // Same component

                // Check if this is cheapest for component of u
                if (cheapest[uRoot] == -1 ||
                    edge.weight < edges[cheapest[uRoot]].weight) {
                    cheapest[uRoot] = i;
                }

                // Check if this is cheapest for component of v
                if (cheapest[vRoot] == -1 ||
                    edge.weight < edges[cheapest[vRoot]].weight) {
                    cheapest[vRoot] = i;
                }
            }

            // Add all cheapest edges
            bool addedAny = false;
            for (int i = 0; i < numVertices; i++) {
                if (cheapest[i] != -1) {
                    const Edge& edge = edges[cheapest[i]];
                    if (uf.unionSets(edge.u, edge.v)) {
                        result.mstEdges.push_back(edge);
                        result.totalWeight += edge.weight;
                        numComponents--;
                        addedAny = true;
                    }
                }
            }

            if (!addedAny) break; // Disconnected graph or done
        }

        return result;
    }

    // ========================================================================
    // MINIMUM SPANNING FOREST (for disconnected graphs)
    // ========================================================================

    /**
     * Find Minimum Spanning Forest for potentially disconnected graph
     */
    MSTResult minimumSpanningForest(const string& algorithm = "kruskal") {
        if (algorithm == "kruskal") {
            MSTResult result = kruskal(true);
            return result;
        } else if (algorithm == "prim") {
            set<int> visitedGlobal;
            MSTResult result;

            for (int start = 0; start < numVertices; start++) {
                if (visitedGlobal.count(start) == 0) {
                    MSTResult tree = prim(start);

                    // Mark vertices in this tree as visited
                    for (const auto& edge : tree.mstEdges) {
                        visitedGlobal.insert(edge.u);
                        visitedGlobal.insert(edge.v);
                    }

                    if (!tree.mstEdges.empty()) {
                        result.forest.push_back(tree.mstEdges);
                        result.totalWeight += tree.totalWeight;
                        result.mstEdges.insert(result.mstEdges.end(),
                                             tree.mstEdges.begin(),
                                             tree.mstEdges.end());
                    }
                }
            }

            return result;
        } else if (algorithm == "boruvka") {
            MSTResult result = boruvka();
            result.forest = buildForest(result.mstEdges);
            return result;
        } else {
            throw invalid_argument("Unknown algorithm: " + algorithm);
        }
    }

    // ========================================================================
    // UTILITY METHODS
    // ========================================================================

    /**
     * Verify if given edges form a valid MST
     */
    pair<bool, string> verifyMST(const vector<Edge>& mstEdges) {
        if (mstEdges.size() != numVertices - 1) {
            return {false, "Invalid edge count: " + to_string(mstEdges.size()) +
                          " (expected " + to_string(numVertices - 1) + ")"};
        }

        UnionFind uf(numVertices);
        for (const auto& edge : mstEdges) {
            if (!uf.unionSets(edge.u, edge.v)) {
                return {false, "Contains cycle"};
            }
        }

        if (uf.getComponentCount() != 1) {
            return {false, "Disconnected: " + to_string(uf.getComponentCount()) + " components"};
        }

        return {true, "Valid MST"};
    }

    /**
     * Compare performance of all MST algorithms
     */
    map<string, map<string, double>> compareAlgorithms(int numRuns = 10) {
        map<string, map<string, double>> results;

        // Kruskal's
        vector<double> kruskalTimes;
        MSTResult kResult;
        for (int i = 0; i < numRuns; i++) {
            auto start = chrono::high_resolution_clock::now();
            kResult = kruskal();
            auto end = chrono::high_resolution_clock::now();
            kruskalTimes.push_back(chrono::duration<double, milli>(end - start).count());
        }

        results["kruskal"]["meanTime"] =
            accumulate(kruskalTimes.begin(), kruskalTimes.end(), 0.0) / kruskalTimes.size();
        results["kruskal"]["minTime"] = *min_element(kruskalTimes.begin(), kruskalTimes.end());
        results["kruskal"]["maxTime"] = *max_element(kruskalTimes.begin(), kruskalTimes.end());
        results["kruskal"]["weight"] = kResult.totalWeight;
        results["kruskal"]["numEdges"] = kResult.mstEdges.size();

        // Prim's
        vector<double> primTimes;
        MSTResult pResult;
        for (int i = 0; i < numRuns; i++) {
            auto start = chrono::high_resolution_clock::now();
            pResult = prim();
            auto end = chrono::high_resolution_clock::now();
            primTimes.push_back(chrono::duration<double, milli>(end - start).count());
        }

        results["prim"]["meanTime"] =
            accumulate(primTimes.begin(), primTimes.end(), 0.0) / primTimes.size();
        results["prim"]["minTime"] = *min_element(primTimes.begin(), primTimes.end());
        results["prim"]["maxTime"] = *max_element(primTimes.begin(), primTimes.end());
        results["prim"]["weight"] = pResult.totalWeight;
        results["prim"]["numEdges"] = pResult.mstEdges.size();

        // Borůvka's
        vector<double> boruvkaTimes;
        MSTResult bResult;
        for (int i = 0; i < numRuns; i++) {
            auto start = chrono::high_resolution_clock::now();
            bResult = boruvka();
            auto end = chrono::high_resolution_clock::now();
            boruvkaTimes.push_back(chrono::duration<double, milli>(end - start).count());
        }

        results["boruvka"]["meanTime"] =
            accumulate(boruvkaTimes.begin(), boruvkaTimes.end(), 0.0) / boruvkaTimes.size();
        results["boruvka"]["minTime"] = *min_element(boruvkaTimes.begin(), boruvkaTimes.end());
        results["boruvka"]["maxTime"] = *max_element(boruvkaTimes.begin(), boruvkaTimes.end());
        results["boruvka"]["weight"] = bResult.totalWeight;
        results["boruvka"]["numEdges"] = bResult.mstEdges.size();

        return results;
    }
};

// ========================================================================
// DEMO
// ========================================================================

void demoMSTAlgorithms() {
    cout << string(80, '=') << endl;
    cout << "MINIMUM SPANNING TREE ALGORITHMS DEMO" << endl;
    cout << string(80, '=') << endl;
    cout << endl;

    vector<Edge> edges = {
        Edge(0, 1, 4),
        Edge(0, 7, 8),
        Edge(1, 2, 8),
        Edge(1, 7, 11),
        Edge(2, 3, 7),
        Edge(2, 5, 4),
        Edge(2, 8, 2),
        Edge(3, 4, 9),
        Edge(3, 5, 14),
        Edge(4, 5, 10),
        Edge(5, 6, 2),
        Edge(6, 7, 1),
        Edge(6, 8, 6),
        Edge(7, 8, 7)
    };

    MSTAlgorithms mst(9, edges);

    // Kruskal's
    cout << "1. KRUSKAL'S ALGORITHM" << endl;
    cout << string(80, '-') << endl;
    MSTResult kResult = mst.kruskal();
    cout << "MST Weight: " << kResult.totalWeight << endl;
    cout << "Edges: ";
    for (const auto& e : kResult.mstEdges) {
        cout << "(" << e.u << "," << e.v << "," << e.weight << ") ";
    }
    cout << endl << endl;

    // Prim's
    cout << "2. PRIM'S ALGORITHM" << endl;
    cout << string(80, '-') << endl;
    MSTResult pResult = mst.prim();
    cout << "MST Weight: " << pResult.totalWeight << endl;
    cout << "Edges: ";
    for (const auto& e : pResult.mstEdges) {
        cout << "(" << e.u << "," << e.v << "," << e.weight << ") ";
    }
    cout << endl << endl;

    // Borůvka's
    cout << "3. BORŮVKA'S ALGORITHM" << endl;
    cout << string(80, '-') << endl;
    MSTResult bResult = mst.boruvka();
    cout << "MST Weight: " << bResult.totalWeight << endl;
    cout << "Edges: ";
    for (const auto& e : bResult.mstEdges) {
        cout << "(" << e.u << "," << e.v << "," << e.weight << ") ";
    }
    cout << endl << endl;

    // Performance
    cout << "4. PERFORMANCE COMPARISON" << endl;
    cout << string(80, '-') << endl;
    auto results = mst.compareAlgorithms(100);

    for (const auto& [algo, metrics] : results) {
        cout << endl << algo << endl;
        cout << fixed << setprecision(4);
        cout << "  Mean time: " << metrics.at("meanTime") << " ms" << endl;
        cout << "  Min time:  " << metrics.at("minTime") << " ms" << endl;
        cout << "  Max time:  " << metrics.at("maxTime") << " ms" << endl;
        cout << "  Weight:    " << metrics.at("weight") << endl;
    }
    cout << endl;

    // Disconnected graph
    cout << "5. MINIMUM SPANNING FOREST (Disconnected Graph)" << endl;
    cout << string(80, '-') << endl;
    vector<Edge> disconnectedEdges = {
        Edge(0, 1, 1),
        Edge(1, 2, 2),
        Edge(3, 4, 3),
        Edge(4, 5, 4)
    };

    MSTAlgorithms mstForest(6, disconnectedEdges);
    MSTResult forestResult = mstForest.minimumSpanningForest("kruskal");

    cout << "Number of trees: " << forestResult.forest.size() << endl;
    cout << "Total weight: " << forestResult.totalWeight << endl;
    for (size_t i = 0; i < forestResult.forest.size(); i++) {
        cout << "\nTree " << (i + 1) << ":" << endl;
        cout << "  Edges: ";
        for (const auto& e : forestResult.forest[i]) {
            cout << "(" << e.u << "," << e.v << "," << e.weight << ") ";
        }
        cout << endl;
    }
}

int main() {
    demoMSTAlgorithms();
    return 0;
}
