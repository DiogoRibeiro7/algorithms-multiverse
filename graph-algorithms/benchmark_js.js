/**
 * JavaScript Benchmark Runner
 * Runs graph algorithm benchmarks and outputs results in JSON format
 */

const { Graph, GraphType, GraphGenerator } = require('./graph.js');
const fs = require('fs');

/**
 * Generate a graph based on configuration
 */
function generateGraph(config) {
    const vertices = config.vertices;
    const graphType = config.directed ? GraphType.DIRECTED : GraphType.UNDIRECTED;
    const weighted = config.weighted || false;

    if (config.type === 'random') {
        return GraphGenerator.randomGraph(vertices, config.density, graphType, weighted);
    } else if (config.type === 'dag') {
        return GraphGenerator.dag(vertices, config.edge_probability || 0.1, weighted);
    } else {
        throw new Error(`Unknown graph type: ${config.type}`);
    }
}

/**
 * Run a specific algorithm on the graph
 */
function runAlgorithm(graph, algorithm, params) {
    try {
        switch (algorithm) {
            case 'dfs_iterative':
                const dfsStart = params.start_vertex || 0;
                return graph.dfsIterative(dfsStart);
            case 'dfs_recursive':
                const dfsRecStart = params.start_vertex || 0;
                return graph.dfsRecursive(dfsRecStart);
            case 'bfs':
                const bfsStart = params.start_vertex || 0;
                return graph.bfs(bfsStart);
            case 'topological_sort':
                return graph.topologicalSort();
            case 'connected_components':
                return graph.findConnectedComponents();
            case 'has_cycle':
                return graph.hasCycle();
            default:
                throw new Error(`Unknown algorithm: ${algorithm}`);
        }
    } catch (error) {
        console.error(`Error running algorithm ${algorithm}:`, error.message);
        return null;
    }
}

/**
 * Run a single benchmark and return timing statistics
 */
function benchmarkAlgorithm(benchmarkConfig) {
    console.log(`Running benchmark: ${benchmarkConfig.name}`);

    // Generate graph once
    const graph = generateGraph(benchmarkConfig.graph);

    const algorithm = benchmarkConfig.algorithm;
    const trials = benchmarkConfig.trials || 10;

    // Prepare parameters
    const params = {};
    if (benchmarkConfig.start_vertex !== undefined) {
        params.start_vertex = benchmarkConfig.start_vertex;
    }

    const times = [];
    let successCount = 0;

    // Run multiple trials
    for (let trial = 0; trial < trials; trial++) {
        const startTime = process.hrtime.bigint();
        const result = runAlgorithm(graph, algorithm, params);
        const endTime = process.hrtime.bigint();

        if (result !== null) {
            const elapsed = Number(endTime - startTime) / 1e9; // Convert to seconds
            times.push(elapsed);
            successCount++;
        }
    }

    if (times.length === 0) {
        return {
            name: benchmarkConfig.name,
            language: 'JavaScript',
            status: 'failed',
            error: 'All trials failed'
        };
    }

    // Compute statistics
    const mean = times.reduce((a, b) => a + b) / times.length;
    const sortedTimes = [...times].sort((a, b) => a - b);
    const median = sortedTimes[Math.floor(sortedTimes.length / 2)];

    let stdDev = 0;
    if (times.length > 1) {
        const variance = times.reduce((sum, t) => sum + Math.pow(t - mean, 2), 0) / (times.length - 1);
        stdDev = Math.sqrt(variance);
    }

    return {
        name: benchmarkConfig.name,
        description: benchmarkConfig.description || '',
        language: 'JavaScript',
        algorithm: algorithm,
        graph: {
            vertices: benchmarkConfig.graph.vertices,
            type: benchmarkConfig.graph.type,
            density: benchmarkConfig.graph.density || 'N/A',
            directed: benchmarkConfig.graph.directed || false,
            weighted: benchmarkConfig.graph.weighted || false
        },
        trials: trials,
        successful_trials: successCount,
        status: 'success',
        timing: {
            mean: mean,
            median: median,
            std_dev: stdDev,
            min: Math.min(...times),
            max: Math.max(...times),
            times: times
        }
    };
}

/**
 * Main benchmark runner
 */
function main() {
    const configFile = 'benchmark_config.json';

    // Load benchmark configuration
    let config;
    try {
        const configData = fs.readFileSync(configFile, 'utf8');
        config = JSON.parse(configData);
    } catch (error) {
        console.error(`Error loading configuration file '${configFile}':`, error.message);
        process.exit(1);
    }

    console.log('='.repeat(80));
    console.log('JavaScript Graph Algorithms Benchmark');
    console.log('='.repeat(80));
    console.log();

    const benchmarks = config.benchmarks || [];
    const results = [];

    for (const benchmarkConfig of benchmarks) {
        try {
            // Skip advanced algorithms not yet implemented in JS
            if (['dijkstra', 'prim_mst', 'kruskal_mst'].includes(benchmarkConfig.algorithm)) {
                console.log(`  Skipped: ${benchmarkConfig.algorithm} not yet implemented in JavaScript`);
                console.log();
                results.push({
                    name: benchmarkConfig.name,
                    language: 'JavaScript',
                    status: 'skipped',
                    reason: 'Algorithm not yet implemented'
                });
                continue;
            }

            const result = benchmarkAlgorithm(benchmarkConfig);
            results.push(result);

            if (result.status === 'success') {
                const timing = result.timing;
                console.log(`  Mean: ${(timing.mean * 1000).toFixed(3)} ms`);
                console.log(`  Std Dev: ${(timing.std_dev * 1000).toFixed(3)} ms`);
                console.log(`  Min: ${(timing.min * 1000).toFixed(3)} ms`);
                console.log(`  Max: ${(timing.max * 1000).toFixed(3)} ms`);
            } else {
                console.log(`  Status: ${result.status}`);
                if (result.error) {
                    console.log(`  Error: ${result.error}`);
                }
            }
            console.log();
        } catch (error) {
            console.log(`  Error: ${error.message}`);
            console.log();
            results.push({
                name: benchmarkConfig.name,
                language: 'JavaScript',
                status: 'error',
                error: error.message
            });
        }
    }

    // Save results
    const outputFile = 'results_javascript.json';
    fs.writeFileSync(outputFile, JSON.stringify(results, null, 2));

    console.log('='.repeat(80));
    console.log(`Results saved to ${outputFile}`);
    console.log('='.repeat(80));
}

if (require.main === module) {
    main();
}

module.exports = { generateGraph, runAlgorithm, benchmarkAlgorithm };
