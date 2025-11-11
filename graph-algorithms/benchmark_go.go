/**
 * Go Benchmark Runner
 * Runs graph algorithm benchmarks and outputs results in JSON format
 */

package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"sort"
	"strings"
	"time"
)

// BenchmarkConfig represents the benchmark configuration
type BenchmarkConfig struct {
	Name        string                 `json:"name"`
	Description string                 `json:"description"`
	Graph       GraphConfig            `json:"graph"`
	Algorithm   string                 `json:"algorithm"`
	StartVertex int                    `json:"start_vertex"`
	Trials      int                    `json:"trials"`
}

// GraphConfig represents graph generation configuration
type GraphConfig struct {
	Vertices       int     `json:"vertices"`
	Type           string  `json:"type"`
	Density        float64 `json:"density"`
	EdgeProbability float64 `json:"edge_probability"`
	Directed       bool    `json:"directed"`
	Weighted       bool    `json:"weighted"`
}

// Config represents the full configuration file
type Config struct {
	Benchmarks []BenchmarkConfig `json:"benchmarks"`
}

// BenchmarkResult represents the result of a benchmark
type BenchmarkResult struct {
	Name             string                 `json:"name"`
	Description      string                 `json:"description"`
	Language         string                 `json:"language"`
	Algorithm        string                 `json:"algorithm"`
	Graph            map[string]interface{} `json:"graph"`
	Trials           int                    `json:"trials"`
	SuccessfulTrials int                    `json:"successful_trials"`
	Status           string                 `json:"status"`
	Error            string                 `json:"error,omitempty"`
	Timing           *TimingStats           `json:"timing,omitempty"`
}

// TimingStats represents timing statistics
type TimingStats struct {
	Mean   float64   `json:"mean"`
	Median float64   `json:"median"`
	StdDev float64   `json:"std_dev"`
	Min    float64   `json:"min"`
	Max    float64   `json:"max"`
	Times  []float64 `json:"times"`
}

// generateGraph creates a graph based on configuration
func generateGraph(config GraphConfig) *Graph {
	graphType := Undirected
	if config.Directed {
		graphType = Directed
	}

	switch config.Type {
	case "random":
		return RandomGraph(config.Vertices, config.Density, graphType, config.Weighted, AdjacencyList)
	case "dag":
		edgeProb := config.EdgeProbability
		if edgeProb == 0 {
			edgeProb = 0.1
		}
		return DAG(config.Vertices, edgeProb, config.Weighted, AdjacencyList)
	default:
		panic(fmt.Sprintf("Unknown graph type: %s", config.Type))
	}
}

// runAlgorithm executes the specified algorithm on the graph
func runAlgorithm(g *Graph, algorithm string, startVertex int) interface{} {
	switch algorithm {
	case "dfs_iterative":
		return g.DFSIterative(startVertex)
	case "dfs_recursive":
		return g.DFSRecursive(startVertex)
	case "bfs":
		return g.BFS(startVertex)
	case "topological_sort":
		return g.TopologicalSort()
	case "connected_components":
		return g.FindConnectedComponents()
	case "has_cycle":
		return g.HasCycle()
	default:
		panic(fmt.Sprintf("Unknown algorithm: %s", algorithm))
	}
}

// computeStats calculates timing statistics
func computeStats(times []float64) *TimingStats {
	if len(times) == 0 {
		return nil
	}

	// Calculate mean
	sum := 0.0
	for _, t := range times {
		sum += t
	}
	mean := sum / float64(len(times))

	// Calculate median
	sorted := make([]float64, len(times))
	copy(sorted, times)
	sort.Float64s(sorted)
	median := sorted[len(sorted)/2]

	// Calculate standard deviation
	stdDev := 0.0
	if len(times) > 1 {
		variance := 0.0
		for _, t := range times {
			variance += math.Pow(t-mean, 2)
		}
		variance /= float64(len(times) - 1)
		stdDev = math.Sqrt(variance)
	}

	// Find min and max
	min := times[0]
	max := times[0]
	for _, t := range times {
		if t < min {
			min = t
		}
		if t > max {
			max = t
		}
	}

	return &TimingStats{
		Mean:   mean,
		Median: median,
		StdDev: stdDev,
		Min:    min,
		Max:    max,
		Times:  times,
	}
}

// runBenchmark executes a single benchmark
func runBenchmark(config BenchmarkConfig) BenchmarkResult {
	fmt.Printf("Running benchmark: %s\n", config.Name)

	// Generate graph
	graph := generateGraph(config.Graph)

	// Run trials
	times := make([]float64, 0, config.Trials)
	successCount := 0

	for i := 0; i < config.Trials; i++ {
		start := time.Now()
		result := runAlgorithm(graph, config.Algorithm, config.StartVertex)
		elapsed := time.Since(start).Seconds()

		if result != nil {
			times = append(times, elapsed)
			successCount++
		}
	}

	result := BenchmarkResult{
		Name:        config.Name,
		Description: config.Description,
		Language:    "Go",
		Algorithm:   config.Algorithm,
		Trials:      config.Trials,
		Graph: map[string]interface{}{
			"vertices": config.Graph.Vertices,
			"type":     config.Graph.Type,
			"density":  config.Graph.Density,
			"directed": config.Graph.Directed,
			"weighted": config.Graph.Weighted,
		},
	}

	if len(times) == 0 {
		result.Status = "failed"
		result.Error = "All trials failed"
		return result
	}

	result.Status = "success"
	result.SuccessfulTrials = successCount
	result.Timing = computeStats(times)

	return result
}

func main() {
	configFile := "benchmark_config.json"

	// Load configuration
	data, err := ioutil.ReadFile(configFile)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error reading config file: %v\n", err)
		os.Exit(1)
	}

	var config Config
	if err := json.Unmarshal(data, &config); err != nil {
		fmt.Fprintf(os.Stderr, "Error parsing config file: %v\n", err)
		os.Exit(1)
	}

	fmt.Println(strings.Repeat("=", 80))
	fmt.Println("Go Graph Algorithms Benchmark")
	fmt.Println(strings.Repeat("=", 80))
	fmt.Println()

	results := make([]BenchmarkResult, 0, len(config.Benchmarks))

	for _, benchConfig := range config.Benchmarks {
		// Skip advanced algorithms not yet implemented in Go
		if benchConfig.Algorithm == "dijkstra" || benchConfig.Algorithm == "prim_mst" || benchConfig.Algorithm == "kruskal_mst" {
			fmt.Printf("Running benchmark: %s\n", benchConfig.Name)
			fmt.Printf("  Skipped: %s not yet implemented in Go\n\n", benchConfig.Algorithm)
			results = append(results, BenchmarkResult{
				Name:     benchConfig.Name,
				Language: "Go",
				Status:   "skipped",
				Error:    "Algorithm not yet implemented",
			})
			continue
		}

		result := runBenchmark(benchConfig)
		results = append(results, result)

		if result.Status == "success" {
			timing := result.Timing
			fmt.Printf("  Mean: %.3f ms\n", timing.Mean*1000)
			fmt.Printf("  Std Dev: %.3f ms\n", timing.StdDev*1000)
			fmt.Printf("  Min: %.3f ms\n", timing.Min*1000)
			fmt.Printf("  Max: %.3f ms\n", timing.Max*1000)
		} else {
			fmt.Printf("  Status: %s\n", result.Status)
			if result.Error != "" {
				fmt.Printf("  Error: %s\n", result.Error)
			}
		}
		fmt.Println()
	}

	// Save results
	outputFile := "results_go.json"
	jsonData, err := json.MarshalIndent(results, "", "  ")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error marshaling results: %v\n", err)
		os.Exit(1)
	}

	if err := ioutil.WriteFile(outputFile, jsonData, 0644); err != nil {
		fmt.Fprintf(os.Stderr, "Error writing results: %v\n", err)
		os.Exit(1)
	}

	fmt.Println(strings.Repeat("=", 80))
	fmt.Printf("Results saved to %s\n", outputFile)
	fmt.Println(strings.Repeat("=", 80))
}
