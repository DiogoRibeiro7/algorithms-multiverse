/**
 * C++ Benchmark Runner
 * Runs graph algorithm benchmarks and outputs results in JSON format
 */

#include "graph.cpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <chrono>
#include <cmath>
#include <algorithm>
#include <iomanip>

struct TimingStats {
    double mean;
    double median;
    double std_dev;
    double min;
    double max;
    std::vector<double> times;
};

struct GraphConfig {
    int vertices;
    std::string type;
    double density;
    double edge_probability;
    bool directed;
    bool weighted;
};

struct BenchmarkConfig {
    std::string name;
    std::string description;
    GraphConfig graph;
    std::string algorithm;
    int start_vertex;
    int trials;
};

// Simple JSON value class
class JSONValue {
private:
    std::string value;
public:
    JSONValue(const std::string& s) : value("\"" + s + "\"") {}
    JSONValue(int i) : value(std::to_string(i)) {}
    JSONValue(double d) {
        std::ostringstream oss;
        oss << std::fixed << std::setprecision(9) << d;
        value = oss.str();
    }
    JSONValue(bool b) : value(b ? "true" : "false") {}

    std::string toString() const { return value; }
};

// Generate graph based on configuration
Graph* generateGraph(const GraphConfig& config) {
    GraphType graphType = config.directed ? GraphType::DIRECTED : GraphType::UNDIRECTED;

    if (config.type == "random") {
        return GraphGenerator::randomGraph(config.vertices, config.density, graphType, config.weighted);
    } else if (config.type == "dag") {
        double edgeProb = config.edge_probability > 0 ? config.edge_probability : 0.1;
        return GraphGenerator::dag(config.vertices, edgeProb, config.weighted);
    } else {
        throw std::runtime_error("Unknown graph type: " + config.type);
    }
}

// Run algorithm and return whether it succeeded
bool runAlgorithm(Graph* graph, const std::string& algorithm, int startVertex) {
    try {
        if (algorithm == "dfs_iterative") {
            graph->dfsIterative(startVertex);
        } else if (algorithm == "dfs_recursive") {
            graph->dfsRecursive(startVertex);
        } else if (algorithm == "bfs") {
            graph->bfs(startVertex);
        } else if (algorithm == "topological_sort") {
            graph->topologicalSort();
        } else if (algorithm == "connected_components") {
            graph->findConnectedComponents();
        } else if (algorithm == "has_cycle") {
            graph->hasCycle();
        } else {
            throw std::runtime_error("Unknown algorithm: " + algorithm);
        }
        return true;
    } catch (const std::exception& e) {
        std::cerr << "Error running algorithm " << algorithm << ": " << e.what() << std::endl;
        return false;
    }
}

// Compute timing statistics
TimingStats computeStats(const std::vector<double>& times) {
    TimingStats stats;
    stats.times = times;

    if (times.empty()) {
        stats.mean = stats.median = stats.std_dev = stats.min = stats.max = 0.0;
        return stats;
    }

    // Mean
    double sum = 0.0;
    for (double t : times) sum += t;
    stats.mean = sum / times.size();

    // Median
    std::vector<double> sorted = times;
    std::sort(sorted.begin(), sorted.end());
    stats.median = sorted[sorted.size() / 2];

    // Standard deviation
    if (times.size() > 1) {
        double variance = 0.0;
        for (double t : times) {
            variance += (t - stats.mean) * (t - stats.mean);
        }
        variance /= (times.size() - 1);
        stats.std_dev = std::sqrt(variance);
    } else {
        stats.std_dev = 0.0;
    }

    // Min and max
    stats.min = *std::min_element(times.begin(), times.end());
    stats.max = *std::max_element(times.begin(), times.end());

    return stats;
}

// Write timing stats to JSON
void writeTimingJSON(std::ofstream& out, const TimingStats& stats, const std::string& indent) {
    out << indent << "\"timing\": {\n";
    out << indent << "  \"mean\": " << stats.mean << ",\n";
    out << indent << "  \"median\": " << stats.median << ",\n";
    out << indent << "  \"std_dev\": " << stats.std_dev << ",\n";
    out << indent << "  \"min\": " << stats.min << ",\n";
    out << indent << "  \"max\": " << stats.max << ",\n";
    out << indent << "  \"times\": [";
    for (size_t i = 0; i < stats.times.size(); i++) {
        if (i > 0) out << ", ";
        out << stats.times[i];
    }
    out << "]\n";
    out << indent << "}";
}

// Run a single benchmark
void runBenchmark(const BenchmarkConfig& config, std::ofstream& outFile, bool isFirst) {
    std::cout << "Running benchmark: " << config.name << std::endl;

    // Generate graph
    Graph* graph = generateGraph(config.graph);

    // Run trials
    std::vector<double> times;
    int successCount = 0;

    for (int i = 0; i < config.trials; i++) {
        auto start = std::chrono::high_resolution_clock::now();
        bool success = runAlgorithm(graph, config.algorithm, config.start_vertex);
        auto end = std::chrono::high_resolution_clock::now();

        if (success) {
            std::chrono::duration<double> elapsed = end - start;
            times.push_back(elapsed.count());
            successCount++;
        }
    }

    // Write result
    if (!isFirst) outFile << ",\n";
    outFile << "  {\n";
    outFile << "    \"name\": \"" << config.name << "\",\n";
    outFile << "    \"description\": \"" << config.description << "\",\n";
    outFile << "    \"language\": \"C++\",\n";
    outFile << "    \"algorithm\": \"" << config.algorithm << "\",\n";
    outFile << "    \"graph\": {\n";
    outFile << "      \"vertices\": " << config.graph.vertices << ",\n";
    outFile << "      \"type\": \"" << config.graph.type << "\",\n";
    outFile << "      \"density\": " << config.graph.density << ",\n";
    outFile << "      \"directed\": " << (config.graph.directed ? "true" : "false") << ",\n";
    outFile << "      \"weighted\": " << (config.graph.weighted ? "true" : "false") << "\n";
    outFile << "    },\n";
    outFile << "    \"trials\": " << config.trials << ",\n";
    outFile << "    \"successful_trials\": " << successCount << ",\n";

    if (times.empty()) {
        outFile << "    \"status\": \"failed\",\n";
        outFile << "    \"error\": \"All trials failed\"\n";
        std::cout << "  Status: failed" << std::endl << std::endl;
    } else {
        outFile << "    \"status\": \"success\",\n";
        TimingStats stats = computeStats(times);
        writeTimingJSON(outFile, stats, "    ");
        outFile << "\n";

        std::cout << "  Mean: " << std::fixed << std::setprecision(3)
                  << (stats.mean * 1000) << " ms" << std::endl;
        std::cout << "  Std Dev: " << (stats.std_dev * 1000) << " ms" << std::endl;
        std::cout << "  Min: " << (stats.min * 1000) << " ms" << std::endl;
        std::cout << "  Max: " << (stats.max * 1000) << " ms" << std::endl;
        std::cout << std::endl;
    }

    outFile << "  }";

    delete graph;
}

int main() {
    std::cout << std::string(80, '=') << std::endl;
    std::cout << "C++ Graph Algorithms Benchmark" << std::endl;
    std::cout << std::string(80, '=') << std::endl;
    std::cout << std::endl;

    std::cout << "Note: This C++ benchmark runner uses hardcoded test cases." << std::endl;
    std::cout << "For full JSON config support, integrate a JSON parsing library." << std::endl;
    std::cout << std::endl;

    // Hardcoded benchmarks
    std::vector<BenchmarkConfig> benchmarks;

    // DFS on sparse graph
    benchmarks.push_back({
        "DFS_Iterative_Sparse",
        "DFS iterative on sparse graph",
        {1000, "random", 0.05, 0.0, false, false},
        "dfs_iterative",
        0,
        10
    });

    // BFS on sparse graph
    benchmarks.push_back({
        "BFS_Sparse",
        "BFS on sparse graph",
        {1000, "random", 0.05, 0.0, false, false},
        "bfs",
        0,
        10
    });

    // Connected components
    benchmarks.push_back({
        "Connected_Components_Sparse",
        "Find connected components in sparse graph",
        {1000, "random", 0.02, 0.0, false, false},
        "connected_components",
        0,
        10
    });

    // Topological sort on DAG
    benchmarks.push_back({
        "Topological_Sort_DAG",
        "Topological sort on directed acyclic graph",
        {100, "dag", 0.0, 0.1, true, false},
        "topological_sort",
        0,
        10
    });

    // Open output file
    std::ofstream outFile("results_cpp.json");
    outFile << "[\n";

    // Run benchmarks
    for (size_t i = 0; i < benchmarks.size(); i++) {
        runBenchmark(benchmarks[i], outFile, i == 0);
    }

    outFile << "\n]\n";
    outFile.close();

    std::cout << std::string(80, '=') << std::endl;
    std::cout << "Results saved to results_cpp.json" << std::endl;
    std::cout << std::string(80, '=') << std::endl;

    return 0;
}
