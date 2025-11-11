/**
 * Comprehensive Graph Data Structure Implementation
 * Supports multiple representations and core graph algorithms
 */

#include <iostream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <stack>
#include <algorithm>
#include <random>
#include <string>
#include <iomanip>
#include <sstream>

enum class GraphType {
    DIRECTED,
    UNDIRECTED
};

enum class RepresentationType {
    ADJACENCY_LIST,
    ADJACENCY_MATRIX,
    EDGE_LIST,
    CSR
};

struct Edge {
    int src, dst;
    double weight;

    Edge(int s, int d, double w) : src(s), dst(d), weight(w) {}
};

struct Neighbor {
    int vertex;
    double weight;

    Neighbor(int v, double w) : vertex(v), weight(w) {}
};

class Graph {
private:
    int numVertices;
    int numEdges;
    GraphType graphType;
    bool weighted;
    RepresentationType representation;

    // Different representations
    std::unordered_map<int, std::vector<Neighbor>> adjList;
    std::vector<std::vector<std::optional<double>>> adjMatrix;
    std::vector<Edge> edges;
    std::vector<double> csrValues;
    std::vector<int> csrColIndices;
    std::vector<int> csrRowPtr;

public:
    /**
     * Constructor for Graph
     */
    Graph(int numVertices = 0,
          GraphType graphType = GraphType::UNDIRECTED,
          bool weighted = false,
          RepresentationType representation = RepresentationType::ADJACENCY_LIST)
        : numVertices(numVertices), graphType(graphType), weighted(weighted),
          representation(representation), numEdges(0) {

        // Initialize based on representation type
        switch (representation) {
            case RepresentationType::ADJACENCY_LIST:
                break;  // adjList is already initialized

            case RepresentationType::ADJACENCY_MATRIX:
                adjMatrix.resize(numVertices,
                               std::vector<std::optional<double>>(numVertices, std::nullopt));
                break;

            case RepresentationType::EDGE_LIST:
                break;  // edges vector already initialized

            case RepresentationType::CSR:
                csrRowPtr.push_back(0);
                break;
        }
    }

    /**
     * Add a new vertex and return its ID
     */
    int addVertex() {
        int vertexId = numVertices++;

        if (representation == RepresentationType::ADJACENCY_MATRIX) {
            // Expand matrix
            for (auto& row : adjMatrix) {
                row.push_back(std::nullopt);
            }
            adjMatrix.push_back(std::vector<std::optional<double>>(numVertices, std::nullopt));
        }

        return vertexId;
    }

    /**
     * Add an edge from u to v with optional weight
     */
    void addEdge(int u, int v, double weight = 1.0) {
        if (u >= numVertices || v >= numVertices) {
            throw std::out_of_range("Vertex out of range: " + std::to_string(u) +
                                  " or " + std::to_string(v));
        }

        numEdges++;

        switch (representation) {
            case RepresentationType::ADJACENCY_LIST:
                adjList[u].emplace_back(v, weight);
                if (graphType == GraphType::UNDIRECTED) {
                    adjList[v].emplace_back(u, weight);
                }
                break;

            case RepresentationType::ADJACENCY_MATRIX:
                adjMatrix[u][v] = weight;
                if (graphType == GraphType::UNDIRECTED) {
                    adjMatrix[v][u] = weight;
                }
                break;

            case RepresentationType::EDGE_LIST:
                edges.emplace_back(u, v, weight);
                if (graphType == GraphType::UNDIRECTED) {
                    edges.emplace_back(v, u, weight);
                }
                break;

            case RepresentationType::CSR:
                throw std::runtime_error("CSR edges should be added via buildCSR()");
        }
    }

    /**
     * Build CSR representation from edge list
     */
    void buildCSR(std::vector<Edge> edgeList) {
        if (representation != RepresentationType::CSR) {
            throw std::runtime_error("Graph must be CSR type");
        }

        // Sort edges by source vertex
        std::sort(edgeList.begin(), edgeList.end(),
                 [](const Edge& a, const Edge& b) {
                     return a.src < b.src || (a.src == b.src && a.dst < b.dst);
                 });

        csrValues.clear();
        csrColIndices.clear();
        csrRowPtr.clear();
        csrRowPtr.push_back(0);

        int currentRow = 0;
        for (const auto& edge : edgeList) {
            // Fill gaps for vertices with no outgoing edges
            while (currentRow < edge.src) {
                csrRowPtr.push_back(csrColIndices.size());
                currentRow++;
            }

            csrValues.push_back(edge.weight);
            csrColIndices.push_back(edge.dst);
        }

        // Complete row pointers
        while (currentRow < numVertices) {
            csrRowPtr.push_back(csrColIndices.size());
            currentRow++;
        }

        numEdges = edgeList.size();
    }

    /**
     * Get neighbors of vertex u with their edge weights
     */
    std::vector<Neighbor> getNeighbors(int u) const {
        switch (representation) {
            case RepresentationType::ADJACENCY_LIST: {
                auto it = adjList.find(u);
                return it != adjList.end() ? it->second : std::vector<Neighbor>();
            }

            case RepresentationType::ADJACENCY_MATRIX: {
                std::vector<Neighbor> neighbors;
                for (int v = 0; v < numVertices; v++) {
                    if (adjMatrix[u][v].has_value()) {
                        neighbors.emplace_back(v, adjMatrix[u][v].value());
                    }
                }
                return neighbors;
            }

            case RepresentationType::EDGE_LIST: {
                std::vector<Neighbor> neighbors;
                for (const auto& edge : edges) {
                    if (edge.src == u) {
                        neighbors.emplace_back(edge.dst, edge.weight);
                    }
                }
                return neighbors;
            }

            case RepresentationType::CSR: {
                std::vector<Neighbor> neighbors;
                int start = csrRowPtr[u];
                int end = csrRowPtr[u + 1];
                for (int i = start; i < end; i++) {
                    neighbors.emplace_back(csrColIndices[i], csrValues[i]);
                }
                return neighbors;
            }
        }
        return {};
    }

    // === DEPTH-FIRST SEARCH ===

    /**
     * DFS traversal using recursion
     */
    std::vector<int> dfsRecursive(int start) const {
        std::unordered_set<int> visited;
        std::vector<int> traversal;
        dfsHelper(start, visited, traversal);
        return traversal;
    }

private:
    void dfsHelper(int v, std::unordered_set<int>& visited,
                  std::vector<int>& traversal) const {
        visited.insert(v);
        traversal.push_back(v);

        for (const auto& neighbor : getNeighbors(v)) {
            if (visited.find(neighbor.vertex) == visited.end()) {
                dfsHelper(neighbor.vertex, visited, traversal);
            }
        }
    }

public:
    /**
     * DFS traversal using iteration with stack
     */
    std::vector<int> dfsIterative(int start) const {
        std::unordered_set<int> visited;
        std::vector<int> traversal;
        std::stack<int> stack;
        stack.push(start);

        while (!stack.empty()) {
            int v = stack.top();
            stack.pop();

            if (visited.find(v) == visited.end()) {
                visited.insert(v);
                traversal.push_back(v);

                // Add neighbors in reverse order for consistent ordering
                auto neighbors = getNeighbors(v);
                for (auto it = neighbors.rbegin(); it != neighbors.rend(); ++it) {
                    if (visited.find(it->vertex) == visited.end()) {
                        stack.push(it->vertex);
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

    // === TOPOLOGICAL SORTING ===

    /**
     * Topological sorting using Kahn's algorithm (BFS-based)
     * Returns empty vector if graph contains a cycle
     */
    std::vector<int> topologicalSort() const {
        if (graphType != GraphType::DIRECTED) {
            throw std::runtime_error("Topological sort only works for directed graphs");
        }

        // Calculate in-degrees
        std::vector<int> inDegree(numVertices, 0);
        for (int u = 0; u < numVertices; u++) {
            for (const auto& neighbor : getNeighbors(u)) {
                inDegree[neighbor.vertex]++;
            }
        }

        // Queue with vertices having 0 in-degree
        std::queue<int> queue;
        for (int v = 0; v < numVertices; v++) {
            if (inDegree[v] == 0) {
                queue.push(v);
            }
        }

        std::vector<int> result;

        while (!queue.empty()) {
            int u = queue.front();
            queue.pop();
            result.push_back(u);

            for (const auto& neighbor : getNeighbors(u)) {
                inDegree[neighbor.vertex]--;
                if (inDegree[neighbor.vertex] == 0) {
                    queue.push(neighbor.vertex);
                }
            }
        }

        // Check if all vertices were processed (no cycle)
        return result.size() == static_cast<size_t>(numVertices) ? result : std::vector<int>();
    }

    /**
     * Topological sorting using DFS
     */
    std::vector<int> topologicalSortDFS() const {
        if (graphType != GraphType::DIRECTED) {
            throw std::runtime_error("Topological sort only works for directed graphs");
        }

        std::unordered_set<int> visited;
        std::unordered_set<int> recStack;
        std::vector<int> result;

        for (int v = 0; v < numVertices; v++) {
            if (visited.find(v) == visited.end()) {
                if (!topoDFSHelper(v, visited, recStack, result)) {
                    return {};  // Cycle detected
                }
            }
        }

        std::reverse(result.begin(), result.end());
        return result;
    }

private:
    bool topoDFSHelper(int v, std::unordered_set<int>& visited,
                      std::unordered_set<int>& recStack,
                      std::vector<int>& result) const {
        visited.insert(v);
        recStack.insert(v);

        for (const auto& neighbor : getNeighbors(v)) {
            if (visited.find(neighbor.vertex) == visited.end()) {
                if (!topoDFSHelper(neighbor.vertex, visited, recStack, result)) {
                    return false;
                }
            } else if (recStack.find(neighbor.vertex) != recStack.end()) {
                return false;  // Cycle detected
            }
        }

        recStack.erase(v);
        result.push_back(v);
        return true;
    }

public:
    // === CONNECTED COMPONENTS ===

    /**
     * Find all connected components in the graph
     */
    std::vector<std::vector<int>> findConnectedComponents() const {
        std::unordered_set<int> visited;
        std::vector<std::vector<int>> components;

        for (int v = 0; v < numVertices; v++) {
            if (visited.find(v) == visited.end()) {
                std::vector<int> component;
                std::stack<int> stack;
                stack.push(v);

                while (!stack.empty()) {
                    int u = stack.top();
                    stack.pop();

                    if (visited.find(u) == visited.end()) {
                        visited.insert(u);
                        component.push_back(u);

                        for (const auto& neighbor : getNeighbors(u)) {
                            if (visited.find(neighbor.vertex) == visited.end()) {
                                stack.push(neighbor.vertex);
                            }
                        }
                    }
                }

                std::sort(component.begin(), component.end());
                components.push_back(component);
            }
        }

        return components;
    }

    /**
     * Check if graph is connected
     */
    bool isConnected() const {
        if (numVertices == 0) return true;
        return findConnectedComponents().size() == 1;
    }

    // === CYCLE DETECTION ===

    /**
     * Detect cycle in undirected graph using DFS
     */
    bool hasCycleUndirected() const {
        if (graphType != GraphType::UNDIRECTED) {
            throw std::runtime_error("This method is for undirected graphs");
        }

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

private:
    bool hasCycleUndirectedHelper(int v, int parent,
                                 std::unordered_set<int>& visited) const {
        visited.insert(v);

        for (const auto& neighbor : getNeighbors(v)) {
            if (visited.find(neighbor.vertex) == visited.end()) {
                if (hasCycleUndirectedHelper(neighbor.vertex, v, visited)) {
                    return true;
                }
            } else if (neighbor.vertex != parent) {
                return true;  // Cycle found
            }
        }

        return false;
    }

public:
    /**
     * Detect cycle in directed graph using DFS with recursion stack
     */
    bool hasCycleDirected() const {
        if (graphType != GraphType::DIRECTED) {
            throw std::runtime_error("This method is for directed graphs");
        }

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

private:
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
                return true;  // Back edge found
            }
        }

        recStack.erase(v);
        return false;
    }

public:
    /**
     * Detect cycle based on graph type
     */
    bool hasCycle() const {
        return graphType == GraphType::DIRECTED ? hasCycleDirected() : hasCycleUndirected();
    }

    // === GRAPH COLORING ===

    /**
     * Graph coloring using greedy algorithm
     * Returns mapping of vertex -> color
     */
    std::unordered_map<int, int> greedyColoring() const {
        std::unordered_map<int, int> colors;

        for (int v = 0; v < numVertices; v++) {
            // Get colors of neighbors
            std::unordered_set<int> neighborColors;
            for (const auto& neighbor : getNeighbors(v)) {
                if (colors.find(neighbor.vertex) != colors.end()) {
                    neighborColors.insert(colors.at(neighbor.vertex));
                }
            }

            // Find first available color
            int color = 0;
            while (neighborColors.find(color) != neighborColors.end()) {
                color++;
            }

            colors[v] = color;
        }

        return colors;
    }

    /**
     * Get upper bound on chromatic number
     */
    int chromaticNumberUpperBound() const {
        auto coloring = greedyColoring();
        if (coloring.empty()) return 0;

        int maxColor = 0;
        for (const auto& [vertex, color] : coloring) {
            maxColor = std::max(maxColor, color);
        }
        return maxColor + 1;
    }

    // === VISUALIZATION ===

    /**
     * Generate ASCII art representation of the graph
     */
    std::string toASCII(int maxWidth = 80) const {
        std::ostringstream oss;
        oss << std::string(maxWidth, '=') << "\n";
        oss << "Graph: " << (graphType == GraphType::DIRECTED ? "DIRECTED" : "UNDIRECTED")
            << ", " << (weighted ? "weighted" : "unweighted") << "\n";
        oss << "Representation: ";
        switch (representation) {
            case RepresentationType::ADJACENCY_LIST: oss << "ADJACENCY_LIST"; break;
            case RepresentationType::ADJACENCY_MATRIX: oss << "ADJACENCY_MATRIX"; break;
            case RepresentationType::EDGE_LIST: oss << "EDGE_LIST"; break;
            case RepresentationType::CSR: oss << "CSR"; break;
        }
        oss << "\n";
        oss << "Vertices: " << numVertices << ", Edges: " << numEdges << "\n";
        oss << std::string(maxWidth, '=') << "\n\n";

        switch (representation) {
            case RepresentationType::ADJACENCY_LIST:
                oss << "Adjacency List:\n";
                for (int v = 0; v < numVertices; v++) {
                    auto neighbors = getNeighbors(v);
                    oss << "  " << v << " -> [";
                    for (size_t i = 0; i < neighbors.size(); i++) {
                        if (weighted) {
                            oss << neighbors[i].vertex << "(" << std::fixed
                                << std::setprecision(1) << neighbors[i].weight << ")";
                        } else {
                            oss << neighbors[i].vertex;
                        }
                        if (i < neighbors.size() - 1) oss << ", ";
                    }
                    oss << "]\n";
                }
                break;

            case RepresentationType::ADJACENCY_MATRIX: {
                oss << "Adjacency Matrix:\n";
                int displaySize = std::min(numVertices, 15);

                // Header
                oss << "    ";
                for (int i = 0; i < displaySize; i++) {
                    oss << std::setw(4) << i << " ";
                }
                oss << "\n    " << std::string(5 * displaySize, '-') << "\n";

                for (int i = 0; i < displaySize; i++) {
                    oss << std::setw(2) << i << " |";
                    for (int j = 0; j < displaySize; j++) {
                        if (!adjMatrix[i][j].has_value()) {
                            oss << "   . ";
                        } else {
                            oss << std::setw(4) << static_cast<int>(adjMatrix[i][j].value()) << " ";
                        }
                    }
                    oss << "\n";
                }

                if (numVertices > 15) {
                    oss << "  ... (truncated)\n";
                }
                break;
            }

            case RepresentationType::EDGE_LIST:
                oss << "Edge List:\n";
                for (size_t i = 0; i < std::min(edges.size(), size_t(50)); i++) {
                    if (weighted) {
                        oss << "  " << i << ": " << edges[i].src << " -> " << edges[i].dst
                            << " (weight: " << std::fixed << std::setprecision(1)
                            << edges[i].weight << ")\n";
                    } else {
                        oss << "  " << i << ": " << edges[i].src << " -> " << edges[i].dst << "\n";
                    }
                }
                if (edges.size() > 50) {
                    oss << "  ... (" << edges.size() - 50 << " more edges)\n";
                }
                break;

            case RepresentationType::CSR:
                oss << "CSR (Compressed Sparse Row):\n";
                oss << "  Values: [";
                for (size_t i = 0; i < std::min(csrValues.size(), size_t(20)); i++) {
                    oss << csrValues[i];
                    if (i < std::min(csrValues.size(), size_t(20)) - 1) oss << ", ";
                }
                if (csrValues.size() > 20) oss << ", ...";
                oss << "]\n";

                oss << "  Col Indices: [";
                for (size_t i = 0; i < std::min(csrColIndices.size(), size_t(20)); i++) {
                    oss << csrColIndices[i];
                    if (i < std::min(csrColIndices.size(), size_t(20)) - 1) oss << ", ";
                }
                if (csrColIndices.size() > 20) oss << ", ...";
                oss << "]\n";

                oss << "  Row Ptrs: [";
                for (size_t i = 0; i < std::min(csrRowPtr.size(), size_t(20)); i++) {
                    oss << csrRowPtr[i];
                    if (i < std::min(csrRowPtr.size(), size_t(20)) - 1) oss << ", ";
                }
                if (csrRowPtr.size() > 20) oss << ", ...";
                oss << "]\n";
                break;
        }

        oss << "\n" << std::string(maxWidth, '=') << "\n";
        return oss.str();
    }

    // === GRAPH GENERATORS ===

    static Graph completeGraph(int n, GraphType graphType = GraphType::UNDIRECTED,
                              RepresentationType representation = RepresentationType::ADJACENCY_LIST) {
        Graph g(n, graphType, false, representation);

        if (representation == RepresentationType::CSR) {
            std::vector<Edge> edges;
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    if (i != j) {
                        edges.emplace_back(i, j, 1.0);
                    }
                }
            }
            g.buildCSR(edges);
        } else {
            for (int i = 0; i < n; i++) {
                for (int j = i + 1; j < n; j++) {
                    g.addEdge(i, j);
                    if (graphType == GraphType::DIRECTED) {
                        g.addEdge(j, i);
                    }
                }
            }
        }

        return g;
    }

    static Graph cycleGraph(int n, GraphType graphType = GraphType::UNDIRECTED,
                           RepresentationType representation = RepresentationType::ADJACENCY_LIST) {
        Graph g(n, graphType, false, representation);

        if (representation == RepresentationType::CSR) {
            std::vector<Edge> edges;
            for (int i = 0; i < n; i++) {
                edges.emplace_back(i, (i + 1) % n, 1.0);
                if (graphType == GraphType::UNDIRECTED) {
                    edges.emplace_back((i + 1) % n, i, 1.0);
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

    static Graph randomGraph(int n, double edgeProbability,
                            GraphType graphType = GraphType::UNDIRECTED,
                            bool weighted = false,
                            RepresentationType representation = RepresentationType::ADJACENCY_LIST) {
        Graph g(n, graphType, weighted, representation);
        std::vector<Edge> edgeList;
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_real_distribution<> dis(0.0, 1.0);
        std::uniform_real_distribution<> weightDis(1.0, 10.0);

        for (int i = 0; i < n; i++) {
            int start = graphType == GraphType::UNDIRECTED ? i + 1 : 0;
            for (int j = start; j < n; j++) {
                if (i != j && dis(gen) < edgeProbability) {
                    double weight = weighted ? weightDis(gen) : 1.0;
                    edgeList.emplace_back(i, j, weight);
                }
            }
        }

        if (representation == RepresentationType::CSR) {
            if (graphType == GraphType::UNDIRECTED) {
                size_t originalSize = edgeList.size();
                for (size_t i = 0; i < originalSize; i++) {
                    edgeList.emplace_back(edgeList[i].dst, edgeList[i].src, edgeList[i].weight);
                }
            }
            g.buildCSR(edgeList);
        } else {
            for (const auto& edge : edgeList) {
                g.addEdge(edge.src, edge.dst, edge.weight);
            }
        }

        return g;
    }

    static Graph dag(int n, double edgeProbability,
                    RepresentationType representation = RepresentationType::ADJACENCY_LIST) {
        Graph g(n, GraphType::DIRECTED, false, representation);
        std::vector<Edge> edgeList;
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_real_distribution<> dis(0.0, 1.0);

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (dis(gen) < edgeProbability) {
                    edgeList.emplace_back(i, j, 1.0);
                }
            }
        }

        if (representation == RepresentationType::CSR) {
            g.buildCSR(edgeList);
        } else {
            for (const auto& edge : edgeList) {
                g.addEdge(edge.src, edge.dst, edge.weight);
            }
        }

        return g;
    }
};

// === DEMO AND TESTING ===

void demo() {
    std::cout << std::string(80, '=') << "\n";
    std::cout << "GRAPH DATA STRUCTURES AND ALGORITHMS DEMO\n";
    std::cout << std::string(80, '=') << "\n\n";

    // Demo 1: Adjacency List
    std::cout << "1. ADJACENCY LIST REPRESENTATION\n";
    std::cout << std::string(80, '-') << "\n";
    Graph g1(5, GraphType::UNDIRECTED, false, RepresentationType::ADJACENCY_LIST);
    g1.addEdge(0, 1);
    g1.addEdge(0, 4);
    g1.addEdge(1, 2);
    g1.addEdge(1, 3);
    g1.addEdge(1, 4);
    g1.addEdge(2, 3);
    g1.addEdge(3, 4);
    std::cout << g1.toASCII() << "\n";

    // Demo 2: DFS and BFS
    std::cout << "2. GRAPH TRAVERSAL\n";
    std::cout << std::string(80, '-') << "\n";
    auto dfsRec = g1.dfsRecursive(0);
    std::cout << "DFS Recursive from 0: ";
    for (int v : dfsRec) std::cout << v << " ";
    std::cout << "\n";

    auto dfsIter = g1.dfsIterative(0);
    std::cout << "DFS Iterative from 0: ";
    for (int v : dfsIter) std::cout << v << " ";
    std::cout << "\n";

    auto bfsResult = g1.bfs(0);
    std::cout << "BFS from 0: ";
    for (int v : bfsResult) std::cout << v << " ";
    std::cout << "\n\n";

    // Demo 3: Connected Components
    std::cout << "3. CONNECTED COMPONENTS\n";
    std::cout << std::string(80, '-') << "\n";
    Graph g2(7, GraphType::UNDIRECTED);
    g2.addEdge(0, 1);
    g2.addEdge(1, 2);
    g2.addEdge(3, 4);
    g2.addEdge(5, 6);
    auto components = g2.findConnectedComponents();
    std::cout << "Components: ";
    for (const auto& comp : components) {
        std::cout << "[";
        for (size_t i = 0; i < comp.size(); i++) {
            std::cout << comp[i];
            if (i < comp.size() - 1) std::cout << ", ";
        }
        std::cout << "] ";
    }
    std::cout << "\nIs connected: " << (g2.isConnected() ? "true" : "false") << "\n\n";

    // Demo 4: Cycle Detection
    std::cout << "4. CYCLE DETECTION\n";
    std::cout << std::string(80, '-') << "\n";
    std::cout << "Graph g1 has cycle: " << (g1.hasCycle() ? "true" : "false") << "\n";
    Graph g3(3, GraphType::UNDIRECTED);
    g3.addEdge(0, 1);
    g3.addEdge(1, 2);
    std::cout << "Linear graph has cycle: " << (g3.hasCycle() ? "true" : "false") << "\n\n";

    // Demo 5: Topological Sort
    std::cout << "5. TOPOLOGICAL SORTING\n";
    std::cout << std::string(80, '-') << "\n";
    auto dag = Graph::dag(6, 0.3);
    std::cout << dag.toASCII();
    auto topo = dag.topologicalSort();
    std::cout << "Topological order: ";
    for (int v : topo) std::cout << v << " ";
    std::cout << "\n\n";

    // Demo 6: Graph Coloring
    std::cout << "6. GRAPH COLORING\n";
    std::cout << std::string(80, '-') << "\n";
    auto coloring = g1.greedyColoring();
    std::cout << "Greedy coloring: ";
    for (const auto& [v, c] : coloring) {
        std::cout << "(" << v << ":" << c << ") ";
    }
    std::cout << "\nChromatic number (upper bound): " << g1.chromaticNumberUpperBound() << "\n\n";

    // Demo 7: Different Representations
    std::cout << "7. ADJACENCY MATRIX REPRESENTATION\n";
    std::cout << std::string(80, '-') << "\n";
    Graph g4(5, GraphType::DIRECTED, true, RepresentationType::ADJACENCY_MATRIX);
    g4.addEdge(0, 1, 2.5);
    g4.addEdge(0, 2, 1.0);
    g4.addEdge(1, 3, 3.0);
    g4.addEdge(2, 3, 1.5);
    g4.addEdge(3, 4, 2.0);
    std::cout << g4.toASCII() << "\n";

    // Demo 8: Graph Generators
    std::cout << "8. GRAPH GENERATORS\n";
    std::cout << std::string(80, '-') << "\n";
    auto complete = Graph::completeGraph(5);
    std::cout << "Complete graph K5:\n" << complete.toASCII() << "\n";

    auto cycle = Graph::cycleGraph(6);
    std::cout << "Cycle graph C6:\n" << cycle.toASCII() << "\n";
}

int main() {
    demo();
    return 0;
}
