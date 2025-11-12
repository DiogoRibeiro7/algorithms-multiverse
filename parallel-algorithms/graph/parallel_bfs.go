/*
Parallel Breadth-First Search (BFS) Implementation in Go

This implementation leverages Go's goroutines and channels for efficient parallel graph traversal.

Features:
- Level-synchronous parallel BFS
- Channel-based work distribution
- Concurrent visited tracking with sync.Map
- Multiple strategies (level-sync, worker pool)

Time Complexity: O(V + E) where V = vertices, E = edges
Space Complexity: O(V)

Author: Algorithms Multiverse
*/

package main

import (
	"fmt"
	"math/rand"
	"runtime"
	"sync"
	"time"
)

// Graph represents an adjacency list graph
type Graph struct {
	adjList    map[int][]int
	numVertices int
	numEdges   int
	directed   bool
}

// NewGraph creates a new graph
func NewGraph(directed bool) *Graph {
	return &Graph{
		adjList:  make(map[int][]int),
		directed: directed,
	}
}

// AddEdge adds an edge to the graph
func (g *Graph) AddEdge(u, v int) {
	g.adjList[u] = append(g.adjList[u], v)
	if !g.directed {
		g.adjList[v] = append(g.adjList[v], u)
	}

	if u >= g.numVertices {
		g.numVertices = u + 1
	}
	if v >= g.numVertices {
		g.numVertices = v + 1
	}
	g.numEdges++
}

// GetNeighbors returns neighbors of a vertex
func (g *Graph) GetNeighbors(vertex int) []int {
	return g.adjList[vertex]
}

// BFSResult contains results from BFS traversal
type BFSResult struct {
	VisitedOrder  []int
	Distances     map[int]int
	Parent        map[int]int
	TimeTaken     time.Duration
	VerticesProcessed int
	EdgesExplored int
	Method        string
	NumWorkers    int
}

// ParallelBFS handles parallel BFS operations
type ParallelBFS struct {
	graph       *Graph
	numWorkers  int
	visited     sync.Map
	distances   sync.Map
	parent      sync.Map
	visitedOrder []int
	orderMutex  sync.Mutex
	edgesExplored int64
	edgesMutex   sync.Mutex
}

// NewParallelBFS creates a new parallel BFS instance
func NewParallelBFS(graph *Graph, numWorkers int) *ParallelBFS {
	if numWorkers <= 0 {
		numWorkers = runtime.NumCPU()
	}

	return &ParallelBFS{
		graph:      graph,
		numWorkers: numWorkers,
	}
}

// reset clears all state
func (pbfs *ParallelBFS) reset() {
	pbfs.visited = sync.Map{}
	pbfs.distances = sync.Map{}
	pbfs.parent = sync.Map{}
	pbfs.visitedOrder = nil
	pbfs.edgesExplored = 0
}

// addToVisitedOrder adds a vertex to visited order (thread-safe)
func (pbfs *ParallelBFS) addToVisitedOrder(vertex int) {
	pbfs.orderMutex.Lock()
	pbfs.visitedOrder = append(pbfs.visitedOrder, vertex)
	pbfs.orderMutex.Unlock()
}

// incrementEdges increments edge counter (thread-safe)
func (pbfs *ParallelBFS) incrementEdges(count int64) {
	pbfs.edgesMutex.Lock()
	pbfs.edgesExplored += count
	pbfs.edgesMutex.Unlock()
}

// SequentialBFS performs standard sequential BFS
func (pbfs *ParallelBFS) SequentialBFS(start int) BFSResult {
	pbfs.reset()
	startTime := time.Now()

	queue := []int{start}
	pbfs.visited.Store(start, true)
	pbfs.distances.Store(start, 0)
	pbfs.parent.Store(start, -1)
	pbfs.addToVisitedOrder(start)

	for len(queue) > 0 {
		vertex := queue[0]
		queue = queue[1:]

		distance, _ := pbfs.distances.Load(vertex)

		for _, neighbor := range pbfs.graph.GetNeighbors(vertex) {
			pbfs.incrementEdges(1)

			if _, visited := pbfs.visited.Load(neighbor); !visited {
				pbfs.visited.Store(neighbor, true)
				pbfs.distances.Store(neighbor, distance.(int)+1)
				pbfs.parent.Store(neighbor, vertex)
				pbfs.addToVisitedOrder(neighbor)
				queue = append(queue, neighbor)
			}
		}
	}

	return pbfs.buildResult(time.Since(startTime), "sequential", 1)
}

// ParallelBFSLevelSync performs level-synchronous parallel BFS
func (pbfs *ParallelBFS) ParallelBFSLevelSync(start int) BFSResult {
	pbfs.reset()
	startTime := time.Now()

	currentLevel := []int{start}
	pbfs.visited.Store(start, true)
	pbfs.distances.Store(start, 0)
	pbfs.parent.Store(start, -1)
	pbfs.addToVisitedOrder(start)

	level := 0

	for len(currentLevel) > 0 {
		// Channel to collect next level vertices
		nextLevelChan := make(chan int, len(currentLevel)*10)
		var wg sync.WaitGroup

		// Process current level in parallel
		for _, vertex := range currentLevel {
			wg.Add(1)
			go func(v int) {
				defer wg.Done()

				localEdges := int64(0)
				for _, neighbor := range pbfs.graph.GetNeighbors(v) {
					localEdges++

					// Try to mark as visited
					if _, visited := pbfs.visited.LoadOrStore(neighbor, true); !visited {
						pbfs.distances.Store(neighbor, level+1)
						pbfs.parent.Store(neighbor, v)
						nextLevelChan <- neighbor
					}
				}
				pbfs.incrementEdges(localEdges)
			}(vertex)
		}

		// Wait for all goroutines to finish
		wg.Wait()
		close(nextLevelChan)

		// Collect next level
		currentLevel = nil
		for vertex := range nextLevelChan {
			currentLevel = append(currentLevel, vertex)
			pbfs.addToVisitedOrder(vertex)
		}

		level++
	}

	return pbfs.buildResult(time.Since(startTime), "level_sync", pbfs.numWorkers)
}

// ParallelBFSWorkerPool uses worker pool pattern
func (pbfs *ParallelBFS) ParallelBFSWorkerPool(start int) BFSResult {
	pbfs.reset()
	startTime := time.Now()

	// Channels for work distribution
	workQueue := make(chan int, pbfs.numWorkers*2)
	done := make(chan bool)

	// Initialize
	pbfs.visited.Store(start, true)
	pbfs.distances.Store(start, 0)
	pbfs.parent.Store(start, -1)
	pbfs.addToVisitedOrder(start)
	workQueue <- start

	// Track active workers
	var activeWorkers int32
	var workerMutex sync.Mutex

	// Worker function
	worker := func() {
		for {
			select {
			case vertex, ok := <-workQueue:
				if !ok {
					return
				}

				workerMutex.Lock()
				activeWorkers++
				workerMutex.Unlock()

				distance, _ := pbfs.distances.Load(vertex)
				localEdges := int64(0)

				for _, neighbor := range pbfs.graph.GetNeighbors(vertex) {
					localEdges++

					if _, visited := pbfs.visited.LoadOrStore(neighbor, true); !visited {
						pbfs.distances.Store(neighbor, distance.(int)+1)
						pbfs.parent.Store(neighbor, vertex)
						pbfs.addToVisitedOrder(neighbor)

						select {
						case workQueue <- neighbor:
						case <-time.After(10 * time.Millisecond):
							// Queue might be full, skip
						}
					}
				}

				pbfs.incrementEdges(localEdges)

				workerMutex.Lock()
				activeWorkers--
				workerMutex.Unlock()

			case <-time.After(100 * time.Millisecond):
				// Check if all work is done
				workerMutex.Lock()
				if activeWorkers == 0 && len(workQueue) == 0 {
					workerMutex.Unlock()
					done <- true
					return
				}
				workerMutex.Unlock()
			}
		}
	}

	// Start workers
	for i := 0; i < pbfs.numWorkers; i++ {
		go worker()
	}

	// Wait for completion
	<-done
	close(workQueue)

	return pbfs.buildResult(time.Since(startTime), "worker_pool", pbfs.numWorkers)
}

// buildResult creates BFSResult from current state
func (pbfs *ParallelBFS) buildResult(duration time.Duration, method string, workers int) BFSResult {
	distances := make(map[int]int)
	parent := make(map[int]int)

	pbfs.distances.Range(func(key, value interface{}) bool {
		distances[key.(int)] = value.(int)
		return true
	})

	pbfs.parent.Range(func(key, value interface{}) bool {
		parent[key.(int)] = value.(int)
		return true
	})

	return BFSResult{
		VisitedOrder:      pbfs.visitedOrder,
		Distances:         distances,
		Parent:            parent,
		TimeTaken:         duration,
		VerticesProcessed: len(pbfs.visitedOrder),
		EdgesExplored:     int(pbfs.edgesExplored),
		Method:            method,
		NumWorkers:        workers,
	}
}

// createRandomGraph creates a random graph for testing
func createRandomGraph(numVertices, edgesPerVertex int) *Graph {
	graph := NewGraph(false)

	for v := 0; v < numVertices; v++ {
		for i := 0; i < edgesPerVertex; i++ {
			neighbor := rand.Intn(numVertices)
			if neighbor != v {
				graph.AddEdge(v, neighbor)
			}
		}
	}

	return graph
}

// benchmarkAllMethods benchmarks all BFS methods
func benchmarkAllMethods(graph *Graph, start int) map[string]BFSResult {
	results := make(map[string]BFSResult)

	methods := []string{"sequential", "level_sync", "worker_pool"}

	for _, method := range methods {
		bfs := NewParallelBFS(graph, runtime.NumCPU())

		var result BFSResult
		switch method {
		case "sequential":
			result = bfs.SequentialBFS(start)
		case "level_sync":
			result = bfs.ParallelBFSLevelSync(start)
		case "worker_pool":
			result = bfs.ParallelBFSWorkerPool(start)
		}

		results[method] = result
	}

	return results
}

// calculateSpeedup calculates speedup factor
func calculateSpeedup(seqTime, parallelTime time.Duration) float64 {
	if parallelTime == 0 {
		return 0
	}
	return float64(seqTime) / float64(parallelTime)
}

// repeatString repeats a string n times
func repeatString(s string, count int) string {
	result := ""
	for i := 0; i < count; i++ {
		result += s
	}
	return result
}

func main() {
	fmt.Println(repeatString("=", 80))
	fmt.Println("PARALLEL BREADTH-FIRST SEARCH (BFS) - Go Implementation")
	fmt.Println(repeatString("=", 80))
	fmt.Printf("Number of CPUs available: %d\n", runtime.NumCPU())

	// Test with different graph sizes
	testCases := []struct {
		numVertices    int
		edgesPerVertex int
	}{
		{1000, 5},
		{5000, 10},
		{10000, 15},
	}

	for _, tc := range testCases {
		fmt.Printf("\n%s\n", repeatString("=", 80))
		fmt.Printf("Testing with %d vertices, ~%d edges per vertex\n",
			tc.numVertices, tc.edgesPerVertex)
		fmt.Printf("%s\n", repeatString("=", 80))

		// Create random graph
		graph := createRandomGraph(tc.numVertices, tc.edgesPerVertex)
		fmt.Printf("Graph: %d vertices, ~%d edges\n",
			graph.numVertices, graph.numEdges)

		// Benchmark all methods
		results := benchmarkAllMethods(graph, 0)

		// Display results
		fmt.Printf("\n%-20s %-15s %-15s %-10s\n",
			"Method", "Time", "Vertices", "Speedup")
		fmt.Println(repeatString("-", 80))

		var seqTime time.Duration
		if result, ok := results["sequential"]; ok {
			seqTime = result.TimeTaken
		}

		for _, method := range []string{"sequential", "level_sync", "worker_pool"} {
			if result, ok := results[method]; ok {
				speedup := calculateSpeedup(seqTime, result.TimeTaken)

				fmt.Printf("%-20s %13s  %13d  %8.2fx\n",
					method,
					result.TimeTaken,
					result.VerticesProcessed,
					speedup)
			}
		}
	}

	fmt.Printf("\n%s\n", repeatString("=", 80))
	fmt.Println("WHEN TO USE PARALLEL BFS IN GO")
	fmt.Printf("%s\n", repeatString("=", 80))
	fmt.Println(`
Parallel BFS with goroutines is beneficial when:

✓ Large graphs (>10,000 vertices)
✓ High branching factor (many neighbors per vertex)
✓ Multiple CPU cores available
✓ Graph fits in memory

Go-specific advantages:
✓ Lightweight goroutines (2-8KB stack)
✓ Efficient channel communication
✓ sync.Map for concurrent visited tracking
✓ Built-in CSP concurrency model
✓ Easy to reason about with goroutines and channels

Key strategies:

1. Level-Synchronous (Recommended)
   - Maintains exact BFS ordering
   - Barrier synchronization between levels
   - Best for correctness

2. Worker Pool
   - Continuous work distribution
   - Better load balancing
   - May not maintain exact order

Performance characteristics:
- Speedup limited by graph diameter (sequential depth)
- Best for "wide" graphs (high branching factor)
- Worse for "deep" graphs (low branching factor)
- Goroutine overhead: ~200ns per spawn
- Channel overhead: ~100ns per operation

Challenges addressed:
- Thread contention: Using sync.Map for lock-free reads
- Load imbalance: Level synchronization or worker pools
- Memory bandwidth: Efficient data structures
- Goroutine explosion: Controlled spawning

Best practices:
1. Use level-synchronous for exact BFS ordering
2. Use worker pool for better load balance
3. Use sync.Map for concurrent visited tracking
4. Buffer channels appropriately (2x-10x workers)
5. Profile with pprof to identify bottlenecks

Applications:
- Social network analysis
- Web crawling
- Network routing
- Shortest path finding
- Connected components

Debugging and profiling:
- go test -race: Detect race conditions
- pprof: CPU and memory profiling
- go tool trace: Visualize goroutines
- GODEBUG=schedtrace=1000: Scheduler details
	`)

	fmt.Println("\nDemonstration complete!")
}
