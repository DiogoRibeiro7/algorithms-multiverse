package com.algorithms.graph;

/**
 * Java Benchmark Runner
 * Runs graph algorithm benchmarks and outputs results in JSON format
 */

import java.io.*;
import java.util.*;
import java.nio.file.*;

public class BenchmarkJava {

    /**
     * Generate a graph based on configuration
     */
    private static Graph generateGraph(Map<String, Object> config) {
        int vertices = ((Number) config.get("vertices")).intValue();
        boolean directed = (Boolean) config.getOrDefault("directed", false);
        boolean weighted = (Boolean) config.getOrDefault("weighted", false);
        Graph.GraphType graphType = directed ? Graph.GraphType.DIRECTED : Graph.GraphType.UNDIRECTED;

        String type = (String) config.get("type");

        if ("random".equals(type)) {
            double density = ((Number) config.get("density")).doubleValue();
            return Graph.GraphGenerator.randomGraph(vertices, density, graphType, weighted);
        } else if ("dag".equals(type)) {
            double edgeProbability = ((Number) config.getOrDefault("edge_probability", 0.1)).doubleValue();
            return Graph.GraphGenerator.dag(vertices, edgeProbability, weighted);
        } else {
            throw new IllegalArgumentException("Unknown graph type: " + type);
        }
    }

    /**
     * Run a specific algorithm on the graph
     */
    private static Object runAlgorithm(Graph graph, String algorithm, Map<String, Object> params) {
        try {
            switch (algorithm) {
                case "dfs_iterative": {
                    int start = ((Number) params.getOrDefault("start_vertex", 0)).intValue();
                    return graph.dfsIterative(start);
                }
                case "dfs_recursive": {
                    int start = ((Number) params.getOrDefault("start_vertex", 0)).intValue();
                    return graph.dfsRecursive(start);
                }
                case "bfs": {
                    int start = ((Number) params.getOrDefault("start_vertex", 0)).intValue();
                    return graph.bfs(start);
                }
                case "topological_sort":
                    return graph.topologicalSort();
                case "connected_components":
                    return graph.findConnectedComponents();
                case "has_cycle":
                    return graph.hasCycle();
                default:
                    throw new IllegalArgumentException("Unknown algorithm: " + algorithm);
            }
        } catch (Exception e) {
            System.err.println("Error running algorithm " + algorithm + ": " + e.getMessage());
            return null;
        }
    }

    /**
     * Run a single benchmark and return timing statistics
     */
    @SuppressWarnings("unchecked")
    private static Map<String, Object> benchmarkAlgorithm(Map<String, Object> benchmarkConfig) {
        String name = (String) benchmarkConfig.get("name");
        System.out.println("Running benchmark: " + name);

        // Generate graph once
        Map<String, Object> graphConfig = (Map<String, Object>) benchmarkConfig.get("graph");
        Graph graph = generateGraph(graphConfig);

        String algorithm = (String) benchmarkConfig.get("algorithm");
        int trials = ((Number) benchmarkConfig.getOrDefault("trials", 10)).intValue();

        // Prepare parameters
        Map<String, Object> params = new HashMap<>();
        if (benchmarkConfig.containsKey("start_vertex")) {
            params.put("start_vertex", benchmarkConfig.get("start_vertex"));
        }

        List<Double> times = new ArrayList<>();
        int successCount = 0;

        // Run multiple trials
        for (int trial = 0; trial < trials; trial++) {
            long startTime = System.nanoTime();
            Object result = runAlgorithm(graph, algorithm, params);
            long endTime = System.nanoTime();

            if (result != null) {
                double elapsed = (endTime - startTime) / 1e9; // Convert to seconds
                times.add(elapsed);
                successCount++;
            }
        }

        Map<String, Object> resultMap = new HashMap<>();
        resultMap.put("name", name);
        resultMap.put("language", "Java");

        if (times.isEmpty()) {
            resultMap.put("status", "failed");
            resultMap.put("error", "All trials failed");
            return resultMap;
        }

        // Compute statistics
        double sum = 0;
        for (double t : times) sum += t;
        double mean = sum / times.size();

        List<Double> sortedTimes = new ArrayList<>(times);
        Collections.sort(sortedTimes);
        double median = sortedTimes.get(sortedTimes.size() / 2);

        double stdDev = 0;
        if (times.size() > 1) {
            double variance = 0;
            for (double t : times) {
                variance += Math.pow(t - mean, 2);
            }
            variance /= (times.size() - 1);
            stdDev = Math.sqrt(variance);
        }

        double min = Collections.min(times);
        double max = Collections.max(times);

        // Build result object
        resultMap.put("description", benchmarkConfig.getOrDefault("description", ""));
        resultMap.put("algorithm", algorithm);

        Map<String, Object> graphInfo = new HashMap<>();
        graphInfo.put("vertices", graphConfig.get("vertices"));
        graphInfo.put("type", graphConfig.get("type"));
        graphInfo.put("density", graphConfig.getOrDefault("density", "N/A"));
        graphInfo.put("directed", graphConfig.getOrDefault("directed", false));
        graphInfo.put("weighted", graphConfig.getOrDefault("weighted", false));
        resultMap.put("graph", graphInfo);

        resultMap.put("trials", trials);
        resultMap.put("successful_trials", successCount);
        resultMap.put("status", "success");

        Map<String, Object> timing = new HashMap<>();
        timing.put("mean", mean);
        timing.put("median", median);
        timing.put("std_dev", stdDev);
        timing.put("min", min);
        timing.put("max", max);
        timing.put("times", times);
        resultMap.put("timing", timing);

        return resultMap;
    }

    /**
     * Simple JSON writer (avoids external dependencies)
     */
    private static String toJSON(Object obj) {
        return toJSON(obj, 0);
    }

    @SuppressWarnings("unchecked")
    private static String toJSON(Object obj, int indent) {
        if (obj == null) {
            return "null";
        } else if (obj instanceof String) {
            return "\"" + obj.toString().replace("\"", "\\\"") + "\"";
        } else if (obj instanceof Number || obj instanceof Boolean) {
            return obj.toString();
        } else if (obj instanceof Map) {
            StringBuilder sb = new StringBuilder();
            String indentStr = "  ".repeat(indent);
            String nextIndentStr = "  ".repeat(indent + 1);
            sb.append("{\n");
            Map<String, Object> map = (Map<String, Object>) obj;
            List<String> keys = new ArrayList<>(map.keySet());
            for (int i = 0; i < keys.size(); i++) {
                String key = keys.get(i);
                sb.append(nextIndentStr).append("\"").append(key).append("\": ");
                sb.append(toJSON(map.get(key), indent + 1));
                if (i < keys.size() - 1) {
                    sb.append(",");
                }
                sb.append("\n");
            }
            sb.append(indentStr).append("}");
            return sb.toString();
        } else if (obj instanceof List) {
            StringBuilder sb = new StringBuilder();
            List<?> list = (List<?>) obj;
            sb.append("[");
            for (int i = 0; i < list.size(); i++) {
                if (i > 0) sb.append(", ");
                sb.append(toJSON(list.get(i), indent));
            }
            sb.append("]");
            return sb.toString();
        } else {
            return "\"" + obj.toString() + "\"";
        }
    }

    /**
     * Parse JSON (simple implementation for benchmark config)
     */
    @SuppressWarnings("unchecked")
    private static Map<String, Object> parseJSON(String json) {
        // Use a proper JSON parser in production
        // For simplicity, this is a placeholder
        throw new UnsupportedOperationException("JSON parsing not implemented. Use a proper JSON library.");
    }

    /**
     * Main benchmark runner
     */
    public static void main(String[] args) {
        String configFile = "benchmark_config.json";

        System.out.println("=".repeat(80));
        System.out.println("Java Graph Algorithms Benchmark");
        System.out.println("=".repeat(80));
        System.out.println();

        System.out.println("Note: This Java benchmark runner requires a JSON parsing library.");
        System.out.println("Please add a JSON library (like org.json or Gson) to fully implement this.");
        System.out.println("For now, running a simple hardcoded test...");
        System.out.println();

        // Hardcoded benchmark for demonstration
        Map<String, Object> graphConfig = new HashMap<>();
        graphConfig.put("vertices", 100);
        graphConfig.put("type", "random");
        graphConfig.put("density", 0.1);
        graphConfig.put("directed", false);
        graphConfig.put("weighted", false);

        Map<String, Object> benchmarkConfig = new HashMap<>();
        benchmarkConfig.put("name", "DFS_Test");
        benchmarkConfig.put("description", "Simple DFS test");
        benchmarkConfig.put("graph", graphConfig);
        benchmarkConfig.put("algorithm", "dfs_iterative");
        benchmarkConfig.put("start_vertex", 0);
        benchmarkConfig.put("trials", 10);

        Map<String, Object> result = benchmarkAlgorithm(benchmarkConfig);

        if ("success".equals(result.get("status"))) {
            @SuppressWarnings("unchecked")
            Map<String, Object> timing = (Map<String, Object>) result.get("timing");
            System.out.printf("  Mean: %.3f ms%n", (Double) timing.get("mean") * 1000);
            System.out.printf("  Std Dev: %.3f ms%n", (Double) timing.get("std_dev") * 1000);
            System.out.printf("  Min: %.3f ms%n", (Double) timing.get("min") * 1000);
            System.out.printf("  Max: %.3f ms%n", (Double) timing.get("max") * 1000);
        } else {
            System.out.println("  Status: " + result.get("status"));
            if (result.containsKey("error")) {
                System.out.println("  Error: " + result.get("error"));
            }
        }
        System.out.println();

        // Save results
        List<Map<String, Object>> results = new ArrayList<>();
        results.add(result);

        String outputFile = "results_java.json";
        try {
            String json = toJSON(results);
            Files.write(Paths.get(outputFile), json.getBytes());
            System.out.println("=".repeat(80));
            System.out.println("Results saved to " + outputFile);
            System.out.println("=".repeat(80));
        } catch (IOException e) {
            System.err.println("Error writing results: " + e.getMessage());
        }
    }
}

