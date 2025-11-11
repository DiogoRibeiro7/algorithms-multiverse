// Comprehensive Graph Data Structure Implementation
// Supports multiple representations and core graph algorithms

package main

import (
	"fmt"
	"math/rand"
	"sort"
	"strings"
	"time"
)

// GraphType represents whether the graph is directed or undirected
type GraphType int

const (
	Undirected GraphType = iota
	Directed
)

// RepresentationType represents the internal storage format
type RepresentationType int

const (
	AdjacencyList RepresentationType = iota
	AdjacencyMatrix
	EdgeList
	CSR // Compressed Sparse Row
)

// Edge represents a graph edge
type Edge struct {
	Src    int
	Dst    int
	Weight float64
}

// Neighbor represents a neighbor vertex with weight
type Neighbor struct {
	Vertex int
	Weight float64
}

// Graph represents a graph data structure
type Graph struct {
	NumVertices    int
	NumEdges       int
	GraphType      GraphType
	Weighted       bool
	Representation RepresentationType

	// Different representations
	AdjList        map[int][]Neighbor
	AdjMatrix      [][]interface{}
	Edges          []Edge
	CsrValues      []float64
	CsrColIndices  []int
	CsrRowPtr      []int
}

// NewGraph creates a new graph
func NewGraph(numVertices int, graphType GraphType, weighted bool, representation RepresentationType) *Graph {
	g := &Graph{
		NumVertices:    numVertices,
		NumEdges:       0,
		GraphType:      graphType,
		Weighted:       weighted,
		Representation: representation,
	}

	// Initialize based on representation type
	switch representation {
	case AdjacencyList:
		g.AdjList = make(map[int][]Neighbor)

	case AdjacencyMatrix:
		g.AdjMatrix = make([][]interface{}, numVertices)
		for i := range g.AdjMatrix {
			g.AdjMatrix[i] = make([]interface{}, numVertices)
		}

	case EdgeList:
		g.Edges = make([]Edge, 0)

	case CSR:
		g.CsrValues = make([]float64, 0)
		g.CsrColIndices = make([]int, 0)
		g.CsrRowPtr = []int{0}
	}

	return g
}

// AddVertex adds a new vertex and returns its ID
func (g *Graph) AddVertex() int {
	vertexID := g.NumVertices
	g.NumVertices++

	if g.Representation == AdjacencyMatrix {
		// Expand matrix
		for i := range g.AdjMatrix {
			g.AdjMatrix[i] = append(g.AdjMatrix[i], nil)
		}
		g.AdjMatrix = append(g.AdjMatrix, make([]interface{}, g.NumVertices))
	}

	return vertexID
}

// AddEdge adds an edge from u to v with optional weight
func (g *Graph) AddEdge(u, v int, weight float64) error {
	if u >= g.NumVertices || v >= g.NumVertices {
		return fmt.Errorf("vertex out of range: %d or %d", u, v)
	}

	g.NumEdges++

	switch g.Representation {
	case AdjacencyList:
		g.AdjList[u] = append(g.AdjList[u], Neighbor{v, weight})
		if g.GraphType == Undirected {
			g.AdjList[v] = append(g.AdjList[v], Neighbor{u, weight})
		}

	case AdjacencyMatrix:
		g.AdjMatrix[u][v] = weight
		if g.GraphType == Undirected {
			g.AdjMatrix[v][u] = weight
		}

	case EdgeList:
		g.Edges = append(g.Edges, Edge{u, v, weight})
		if g.GraphType == Undirected {
			g.Edges = append(g.Edges, Edge{v, u, weight})
		}

	case CSR:
		return fmt.Errorf("CSR edges should be added via BuildCSR()")
	}

	return nil
}

// BuildCSR builds CSR representation from edge list
func (g *Graph) BuildCSR(edges []Edge) {
	if g.Representation != CSR {
		panic("Graph must be CSR type")
	}

	// Sort edges by source vertex
	sort.Slice(edges, func(i, j int) bool {
		if edges[i].Src != edges[j].Src {
			return edges[i].Src < edges[j].Src
		}
		return edges[i].Dst < edges[j].Dst
	})

	g.CsrValues = make([]float64, 0)
	g.CsrColIndices = make([]int, 0)
	g.CsrRowPtr = []int{0}

	currentRow := 0
	for _, edge := range edges {
		// Fill gaps for vertices with no outgoing edges
		for currentRow < edge.Src {
			g.CsrRowPtr = append(g.CsrRowPtr, len(g.CsrColIndices))
			currentRow++
		}

		g.CsrValues = append(g.CsrValues, edge.Weight)
		g.CsrColIndices = append(g.CsrColIndices, edge.Dst)
	}

	// Complete row pointers
	for currentRow < g.NumVertices {
		g.CsrRowPtr = append(g.CsrRowPtr, len(g.CsrColIndices))
		currentRow++
	}

	g.NumEdges = len(edges)
}

// GetNeighbors returns neighbors of vertex u with their edge weights
func (g *Graph) GetNeighbors(u int) []Neighbor {
	switch g.Representation {
	case AdjacencyList:
		return g.AdjList[u]

	case AdjacencyMatrix:
		neighbors := make([]Neighbor, 0)
		for v := 0; v < g.NumVertices; v++ {
			if g.AdjMatrix[u][v] != nil {
				neighbors = append(neighbors, Neighbor{v, g.AdjMatrix[u][v].(float64)})
			}
		}
		return neighbors

	case EdgeList:
		neighbors := make([]Neighbor, 0)
		for _, edge := range g.Edges {
			if edge.Src == u {
				neighbors = append(neighbors, Neighbor{edge.Dst, edge.Weight})
			}
		}
		return neighbors

	case CSR:
		neighbors := make([]Neighbor, 0)
		start := g.CsrRowPtr[u]
		end := g.CsrRowPtr[u+1]
		for i := start; i < end; i++ {
			neighbors = append(neighbors, Neighbor{g.CsrColIndices[i], g.CsrValues[i]})
		}
		return neighbors
	}

	return nil
}

// === DEPTH-FIRST SEARCH ===

// DFSRecursive performs DFS traversal using recursion
func (g *Graph) DFSRecursive(start int) []int {
	visited := make(map[int]bool)
	traversal := make([]int, 0)
	g.dfsHelper(start, visited, &traversal)
	return traversal
}

func (g *Graph) dfsHelper(v int, visited map[int]bool, traversal *[]int) {
	visited[v] = true
	*traversal = append(*traversal, v)

	for _, neighbor := range g.GetNeighbors(v) {
		if !visited[neighbor.Vertex] {
			g.dfsHelper(neighbor.Vertex, visited, traversal)
		}
	}
}

// DFSIterative performs DFS traversal using iteration with stack
func (g *Graph) DFSIterative(start int) []int {
	visited := make(map[int]bool)
	traversal := make([]int, 0)
	stack := []int{start}

	for len(stack) > 0 {
		v := stack[len(stack)-1]
		stack = stack[:len(stack)-1]

		if !visited[v] {
			visited[v] = true
			traversal = append(traversal, v)

			// Add neighbors in reverse order for consistent ordering
			neighbors := g.GetNeighbors(v)
			for i := len(neighbors) - 1; i >= 0; i-- {
				if !visited[neighbors[i].Vertex] {
					stack = append(stack, neighbors[i].Vertex)
				}
			}
		}
	}

	return traversal
}

// === BREADTH-FIRST SEARCH ===

// BFS performs BFS traversal
func (g *Graph) BFS(start int) []int {
	visited := make(map[int]bool)
	traversal := make([]int, 0)
	queue := []int{start}
	visited[start] = true

	for len(queue) > 0 {
		v := queue[0]
		queue = queue[1:]
		traversal = append(traversal, v)

		for _, neighbor := range g.GetNeighbors(v) {
			if !visited[neighbor.Vertex] {
				visited[neighbor.Vertex] = true
				queue = append(queue, neighbor.Vertex)
			}
		}
	}

	return traversal
}

// === TOPOLOGICAL SORTING ===

// TopologicalSort performs topological sorting using Kahn's algorithm
// Returns nil if graph contains a cycle
func (g *Graph) TopologicalSort() []int {
	if g.GraphType != Directed {
		panic("Topological sort only works for directed graphs")
	}

	// Calculate in-degrees
	inDegree := make([]int, g.NumVertices)
	for u := 0; u < g.NumVertices; u++ {
		for _, neighbor := range g.GetNeighbors(u) {
			inDegree[neighbor.Vertex]++
		}
	}

	// Queue with vertices having 0 in-degree
	queue := make([]int, 0)
	for v := 0; v < g.NumVertices; v++ {
		if inDegree[v] == 0 {
			queue = append(queue, v)
		}
	}

	result := make([]int, 0)

	for len(queue) > 0 {
		u := queue[0]
		queue = queue[1:]
		result = append(result, u)

		for _, neighbor := range g.GetNeighbors(u) {
			inDegree[neighbor.Vertex]--
			if inDegree[neighbor.Vertex] == 0 {
				queue = append(queue, neighbor.Vertex)
			}
		}
	}

	// Check if all vertices were processed (no cycle)
	if len(result) != g.NumVertices {
		return nil
	}

	return result
}

// TopologicalSortDFS performs topological sorting using DFS
func (g *Graph) TopologicalSortDFS() []int {
	if g.GraphType != Directed {
		panic("Topological sort only works for directed graphs")
	}

	visited := make(map[int]bool)
	recStack := make(map[int]bool)
	result := make([]int, 0)

	var dfsHelper func(int) bool
	dfsHelper = func(v int) bool {
		visited[v] = true
		recStack[v] = true

		for _, neighbor := range g.GetNeighbors(v) {
			if !visited[neighbor.Vertex] {
				if !dfsHelper(neighbor.Vertex) {
					return false
				}
			} else if recStack[neighbor.Vertex] {
				return false // Cycle detected
			}
		}

		delete(recStack, v)
		result = append(result, v)
		return true
	}

	for v := 0; v < g.NumVertices; v++ {
		if !visited[v] {
			if !dfsHelper(v) {
				return nil // Cycle detected
			}
		}
	}

	// Reverse result
	for i, j := 0, len(result)-1; i < j; i, j = i+1, j-1 {
		result[i], result[j] = result[j], result[i]
	}

	return result
}

// === CONNECTED COMPONENTS ===

// FindConnectedComponents finds all connected components in the graph
func (g *Graph) FindConnectedComponents() [][]int {
	visited := make(map[int]bool)
	components := make([][]int, 0)

	for v := 0; v < g.NumVertices; v++ {
		if !visited[v] {
			component := make([]int, 0)
			stack := []int{v}

			for len(stack) > 0 {
				u := stack[len(stack)-1]
				stack = stack[:len(stack)-1]

				if !visited[u] {
					visited[u] = true
					component = append(component, u)

					for _, neighbor := range g.GetNeighbors(u) {
						if !visited[neighbor.Vertex] {
							stack = append(stack, neighbor.Vertex)
						}
					}
				}
			}

			sort.Ints(component)
			components = append(components, component)
		}
	}

	return components
}

// IsConnected checks if graph is connected
func (g *Graph) IsConnected() bool {
	if g.NumVertices == 0 {
		return true
	}
	return len(g.FindConnectedComponents()) == 1
}

// === CYCLE DETECTION ===

// HasCycleUndirected detects cycle in undirected graph using DFS
func (g *Graph) HasCycleUndirected() bool {
	if g.GraphType != Undirected {
		panic("This method is for undirected graphs")
	}

	visited := make(map[int]bool)

	var dfsHelper func(int, int) bool
	dfsHelper = func(v, parent int) bool {
		visited[v] = true

		for _, neighbor := range g.GetNeighbors(v) {
			if !visited[neighbor.Vertex] {
				if dfsHelper(neighbor.Vertex, v) {
					return true
				}
			} else if neighbor.Vertex != parent {
				return true // Cycle found
			}
		}

		return false
	}

	for v := 0; v < g.NumVertices; v++ {
		if !visited[v] {
			if dfsHelper(v, -1) {
				return true
			}
		}
	}

	return false
}

// HasCycleDirected detects cycle in directed graph using DFS with recursion stack
func (g *Graph) HasCycleDirected() bool {
	if g.GraphType != Directed {
		panic("This method is for directed graphs")
	}

	visited := make(map[int]bool)
	recStack := make(map[int]bool)

	var dfsHelper func(int) bool
	dfsHelper = func(v int) bool {
		visited[v] = true
		recStack[v] = true

		for _, neighbor := range g.GetNeighbors(v) {
			if !visited[neighbor.Vertex] {
				if dfsHelper(neighbor.Vertex) {
					return true
				}
			} else if recStack[neighbor.Vertex] {
				return true // Back edge found
			}
		}

		delete(recStack, v)
		return false
	}

	for v := 0; v < g.NumVertices; v++ {
		if !visited[v] {
			if dfsHelper(v) {
				return true
			}
		}
	}

	return false
}

// HasCycle detects cycle based on graph type
func (g *Graph) HasCycle() bool {
	if g.GraphType == Directed {
		return g.HasCycleDirected()
	}
	return g.HasCycleUndirected()
}

// === GRAPH COLORING ===

// GreedyColoring performs graph coloring using greedy algorithm
func (g *Graph) GreedyColoring() map[int]int {
	colors := make(map[int]int)

	for v := 0; v < g.NumVertices; v++ {
		// Get colors of neighbors
		neighborColors := make(map[int]bool)
		for _, neighbor := range g.GetNeighbors(v) {
			if color, exists := colors[neighbor.Vertex]; exists {
				neighborColors[color] = true
			}
		}

		// Find first available color
		color := 0
		for neighborColors[color] {
			color++
		}

		colors[v] = color
	}

	return colors
}

// ChromaticNumberUpperBound returns upper bound on chromatic number
func (g *Graph) ChromaticNumberUpperBound() int {
	coloring := g.GreedyColoring()
	if len(coloring) == 0 {
		return 0
	}

	maxColor := 0
	for _, color := range coloring {
		if color > maxColor {
			maxColor = color
		}
	}
	return maxColor + 1
}

// === VISUALIZATION ===

// ToASCII generates ASCII art representation of the graph
func (g *Graph) ToASCII(maxWidth int) string {
	var sb strings.Builder

	sb.WriteString(strings.Repeat("=", maxWidth) + "\n")
	graphTypeStr := "UNDIRECTED"
	if g.GraphType == Directed {
		graphTypeStr = "DIRECTED"
	}
	weightedStr := "unweighted"
	if g.Weighted {
		weightedStr = "weighted"
	}
	sb.WriteString(fmt.Sprintf("Graph: %s, %s\n", graphTypeStr, weightedStr))

	repStr := ""
	switch g.Representation {
	case AdjacencyList:
		repStr = "ADJACENCY_LIST"
	case AdjacencyMatrix:
		repStr = "ADJACENCY_MATRIX"
	case EdgeList:
		repStr = "EDGE_LIST"
	case CSR:
		repStr = "CSR"
	}
	sb.WriteString(fmt.Sprintf("Representation: %s\n", repStr))
	sb.WriteString(fmt.Sprintf("Vertices: %d, Edges: %d\n", g.NumVertices, g.NumEdges))
	sb.WriteString(strings.Repeat("=", maxWidth) + "\n\n")

	switch g.Representation {
	case AdjacencyList:
		sb.WriteString("Adjacency List:\n")
		for v := 0; v < g.NumVertices; v++ {
			neighbors := g.GetNeighbors(v)
			sb.WriteString(fmt.Sprintf("  %d -> [", v))
			for i, neighbor := range neighbors {
				if g.Weighted {
					sb.WriteString(fmt.Sprintf("%d(%.1f)", neighbor.Vertex, neighbor.Weight))
				} else {
					sb.WriteString(fmt.Sprintf("%d", neighbor.Vertex))
				}
				if i < len(neighbors)-1 {
					sb.WriteString(", ")
				}
			}
			sb.WriteString("]\n")
		}

	case AdjacencyMatrix:
		sb.WriteString("Adjacency Matrix:\n")
		displaySize := g.NumVertices
		if displaySize > 15 {
			displaySize = 15
		}

		// Header
		sb.WriteString("    ")
		for i := 0; i < displaySize; i++ {
			sb.WriteString(fmt.Sprintf("%4d ", i))
		}
		sb.WriteString("\n    " + strings.Repeat("-", 5*displaySize) + "\n")

		for i := 0; i < displaySize; i++ {
			sb.WriteString(fmt.Sprintf("%2d |", i))
			for j := 0; j < displaySize; j++ {
				if g.AdjMatrix[i][j] == nil {
					sb.WriteString("   . ")
				} else {
					sb.WriteString(fmt.Sprintf("%4.0f ", g.AdjMatrix[i][j].(float64)))
				}
			}
			sb.WriteString("\n")
		}

		if g.NumVertices > 15 {
			sb.WriteString("  ... (truncated)\n")
		}

	case EdgeList:
		sb.WriteString("Edge List:\n")
		displayLimit := len(g.Edges)
		if displayLimit > 50 {
			displayLimit = 50
		}
		for i := 0; i < displayLimit; i++ {
			edge := g.Edges[i]
			if g.Weighted {
				sb.WriteString(fmt.Sprintf("  %d: %d -> %d (weight: %.1f)\n",
					i, edge.Src, edge.Dst, edge.Weight))
			} else {
				sb.WriteString(fmt.Sprintf("  %d: %d -> %d\n", i, edge.Src, edge.Dst))
			}
		}
		if len(g.Edges) > 50 {
			sb.WriteString(fmt.Sprintf("  ... (%d more edges)\n", len(g.Edges)-50))
		}

	case CSR:
		sb.WriteString("CSR (Compressed Sparse Row):\n")
		valLimit := len(g.CsrValues)
		if valLimit > 20 {
			valLimit = 20
		}
		sb.WriteString("  Values: [")
		for i := 0; i < valLimit; i++ {
			sb.WriteString(fmt.Sprintf("%.1f", g.CsrValues[i]))
			if i < valLimit-1 {
				sb.WriteString(", ")
			}
		}
		if len(g.CsrValues) > 20 {
			sb.WriteString(", ...")
		}
		sb.WriteString("]\n")

		colLimit := len(g.CsrColIndices)
		if colLimit > 20 {
			colLimit = 20
		}
		sb.WriteString("  Col Indices: [")
		for i := 0; i < colLimit; i++ {
			sb.WriteString(fmt.Sprintf("%d", g.CsrColIndices[i]))
			if i < colLimit-1 {
				sb.WriteString(", ")
			}
		}
		if len(g.CsrColIndices) > 20 {
			sb.WriteString(", ...")
		}
		sb.WriteString("]\n")

		rowLimit := len(g.CsrRowPtr)
		if rowLimit > 20 {
			rowLimit = 20
		}
		sb.WriteString("  Row Ptrs: [")
		for i := 0; i < rowLimit; i++ {
			sb.WriteString(fmt.Sprintf("%d", g.CsrRowPtr[i]))
			if i < rowLimit-1 {
				sb.WriteString(", ")
			}
		}
		if len(g.CsrRowPtr) > 20 {
			sb.WriteString(", ...")
		}
		sb.WriteString("]\n")
	}

	sb.WriteString("\n" + strings.Repeat("=", maxWidth) + "\n")
	return sb.String()
}

// === GRAPH GENERATORS ===

// CompleteGraph generates a complete graph with n vertices
func CompleteGraph(n int, graphType GraphType, representation RepresentationType) *Graph {
	g := NewGraph(n, graphType, false, representation)

	if representation == CSR {
		edges := make([]Edge, 0)
		for i := 0; i < n; i++ {
			for j := 0; j < n; j++ {
				if i != j {
					edges = append(edges, Edge{i, j, 1.0})
				}
			}
		}
		g.BuildCSR(edges)
	} else {
		for i := 0; i < n; i++ {
			for j := i + 1; j < n; j++ {
				g.AddEdge(i, j, 1.0)
				if graphType == Directed {
					g.AddEdge(j, i, 1.0)
				}
			}
		}
	}

	return g
}

// CycleGraph generates a cycle graph with n vertices
func CycleGraph(n int, graphType GraphType, representation RepresentationType) *Graph {
	g := NewGraph(n, graphType, false, representation)

	if representation == CSR {
		edges := make([]Edge, 0)
		for i := 0; i < n; i++ {
			edges = append(edges, Edge{i, (i + 1) % n, 1.0})
			if graphType == Undirected {
				edges = append(edges, Edge{(i + 1) % n, i, 1.0})
			}
		}
		g.BuildCSR(edges)
	} else {
		for i := 0; i < n; i++ {
			g.AddEdge(i, (i+1)%n, 1.0)
		}
	}

	return g
}

// RandomGraph generates random graph with Erdős-Rényi model
func RandomGraph(n int, edgeProbability float64, graphType GraphType, weighted bool, representation RepresentationType) *Graph {
	g := NewGraph(n, graphType, weighted, representation)
	edges := make([]Edge, 0)
	rand.Seed(time.Now().UnixNano())

	for i := 0; i < n; i++ {
		start := 0
		if graphType == Undirected {
			start = i + 1
		}
		for j := start; j < n; j++ {
			if i != j && rand.Float64() < edgeProbability {
				weight := 1.0
				if weighted {
					weight = rand.Float64()*9 + 1
				}
				edges = append(edges, Edge{i, j, weight})
			}
		}
	}

	if representation == CSR {
		if graphType == Undirected {
			originalLen := len(edges)
			for i := 0; i < originalLen; i++ {
				edges = append(edges, Edge{edges[i].Dst, edges[i].Src, edges[i].Weight})
			}
		}
		g.BuildCSR(edges)
	} else {
		for _, edge := range edges {
			g.AddEdge(edge.Src, edge.Dst, edge.Weight)
		}
	}

	return g
}

// DAG generates a random Directed Acyclic Graph
func DAG(n int, edgeProbability float64, representation RepresentationType) *Graph {
	g := NewGraph(n, Directed, false, representation)
	edges := make([]Edge, 0)
	rand.Seed(time.Now().UnixNano())

	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if rand.Float64() < edgeProbability {
				edges = append(edges, Edge{i, j, 1.0})
			}
		}
	}

	if representation == CSR {
		g.BuildCSR(edges)
	} else {
		for _, edge := range edges {
			g.AddEdge(edge.Src, edge.Dst, edge.Weight)
		}
	}

	return g
}

// === DEMO AND TESTING ===

func demo() {
	fmt.Println(strings.Repeat("=", 80))
	fmt.Println("GRAPH DATA STRUCTURES AND ALGORITHMS DEMO")
	fmt.Println(strings.Repeat("=", 80))
	fmt.Println()

	// Demo 1: Adjacency List
	fmt.Println("1. ADJACENCY LIST REPRESENTATION")
	fmt.Println(strings.Repeat("-", 80))
	g1 := NewGraph(5, Undirected, false, AdjacencyList)
	g1.AddEdge(0, 1, 1.0)
	g1.AddEdge(0, 4, 1.0)
	g1.AddEdge(1, 2, 1.0)
	g1.AddEdge(1, 3, 1.0)
	g1.AddEdge(1, 4, 1.0)
	g1.AddEdge(2, 3, 1.0)
	g1.AddEdge(3, 4, 1.0)
	fmt.Println(g1.ToASCII(80))

	// Demo 2: DFS and BFS
	fmt.Println("2. GRAPH TRAVERSAL")
	fmt.Println(strings.Repeat("-", 80))
	fmt.Printf("DFS Recursive from 0: %v\n", g1.DFSRecursive(0))
	fmt.Printf("DFS Iterative from 0: %v\n", g1.DFSIterative(0))
	fmt.Printf("BFS from 0: %v\n", g1.BFS(0))
	fmt.Println()

	// Demo 3: Connected Components
	fmt.Println("3. CONNECTED COMPONENTS")
	fmt.Println(strings.Repeat("-", 80))
	g2 := NewGraph(7, Undirected, false, AdjacencyList)
	g2.AddEdge(0, 1, 1.0)
	g2.AddEdge(1, 2, 1.0)
	g2.AddEdge(3, 4, 1.0)
	g2.AddEdge(5, 6, 1.0)
	fmt.Printf("Components: %v\n", g2.FindConnectedComponents())
	fmt.Printf("Is connected: %v\n", g2.IsConnected())
	fmt.Println()

	// Demo 4: Cycle Detection
	fmt.Println("4. CYCLE DETECTION")
	fmt.Println(strings.Repeat("-", 80))
	fmt.Printf("Graph g1 has cycle: %v\n", g1.HasCycle())
	g3 := NewGraph(3, Undirected, false, AdjacencyList)
	g3.AddEdge(0, 1, 1.0)
	g3.AddEdge(1, 2, 1.0)
	fmt.Printf("Linear graph has cycle: %v\n", g3.HasCycle())
	fmt.Println()

	// Demo 5: Topological Sort
	fmt.Println("5. TOPOLOGICAL SORTING")
	fmt.Println(strings.Repeat("-", 80))
	dag := DAG(6, 0.3, AdjacencyList)
	fmt.Print(dag.ToASCII(80))
	fmt.Printf("Topological order: %v\n", dag.TopologicalSort())
	fmt.Printf("Topological order (DFS): %v\n", dag.TopologicalSortDFS())
	fmt.Println()

	// Demo 6: Graph Coloring
	fmt.Println("6. GRAPH COLORING")
	fmt.Println(strings.Repeat("-", 80))
	fmt.Printf("Greedy coloring: %v\n", g1.GreedyColoring())
	fmt.Printf("Chromatic number (upper bound): %d\n", g1.ChromaticNumberUpperBound())
	fmt.Println()

	// Demo 7: Different Representations
	fmt.Println("7. ADJACENCY MATRIX REPRESENTATION")
	fmt.Println(strings.Repeat("-", 80))
	g4 := NewGraph(5, Directed, true, AdjacencyMatrix)
	g4.AddEdge(0, 1, 2.5)
	g4.AddEdge(0, 2, 1.0)
	g4.AddEdge(1, 3, 3.0)
	g4.AddEdge(2, 3, 1.5)
	g4.AddEdge(3, 4, 2.0)
	fmt.Print(g4.ToASCII(80))

	// Demo 8: Graph Generators
	fmt.Println("8. GRAPH GENERATORS")
	fmt.Println(strings.Repeat("-", 80))
	complete := CompleteGraph(5, Undirected, AdjacencyList)
	fmt.Println("Complete graph K5:")
	fmt.Print(complete.ToASCII(80))

	cycle := CycleGraph(6, Undirected, AdjacencyList)
	fmt.Println("Cycle graph C6:")
	fmt.Print(cycle.ToASCII(80))
}

func main() {
	demo()
}
