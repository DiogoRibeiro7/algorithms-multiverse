// Comprehensive unit tests for graph.go
//
// Run with:
//    go test -v
//    or
//    go test

package main

import (
	"testing"
)

// Test graph creation
func TestCreateEmptyGraph(t *testing.T) {
	g := NewGraph(0, Undirected, false, AdjacencyList)
	if g.NumVertices != 0 {
		t.Errorf("Expected 0 vertices, got %d", g.NumVertices)
	}
	if g.NumEdges != 0 {
		t.Errorf("Expected 0 edges, got %d", g.NumEdges)
	}
}

func TestCreateGraphWithVertices(t *testing.T) {
	g := NewGraph(5, Undirected, false, AdjacencyList)
	if g.NumVertices != 5 {
		t.Errorf("Expected 5 vertices, got %d", g.NumVertices)
	}
	if g.NumEdges != 0 {
		t.Errorf("Expected 0 edges, got %d", g.NumEdges)
	}
}

func TestAddVertex(t *testing.T) {
	g := NewGraph(2, Undirected, false, AdjacencyList)
	vertexID := g.AddVertex()
	if vertexID != 2 {
		t.Errorf("Expected vertex ID 2, got %d", vertexID)
	}
	if g.NumVertices != 3 {
		t.Errorf("Expected 3 vertices, got %d", g.NumVertices)
	}
}

func TestAddEdgeUndirected(t *testing.T) {
	g := NewGraph(3, Undirected, false, AdjacencyList)
	err := g.AddEdge(0, 1, 5.0)
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if g.NumEdges != 1 {
		t.Errorf("Expected 1 edge, got %d", g.NumEdges)
	}

	neighbors := g.GetNeighbors(0)
	if len(neighbors) != 1 {
		t.Errorf("Expected 1 neighbor, got %d", len(neighbors))
	}
	if neighbors[0].Vertex != 1 {
		t.Errorf("Expected neighbor 1, got %d", neighbors[0].Vertex)
	}
}

func TestAddEdgeDirected(t *testing.T) {
	g := NewGraph(3, Directed, false, AdjacencyList)
	g.AddEdge(0, 1, 1.0)
	if g.NumEdges != 1 {
		t.Errorf("Expected 1 edge, got %d", g.NumEdges)
	}

	if len(g.GetNeighbors(0)) != 1 {
		t.Errorf("Expected 1 neighbor for source")
	}
	if len(g.GetNeighbors(1)) != 0 {
		t.Errorf("Expected 0 neighbors for destination")
	}
}

func TestInvalidEdge(t *testing.T) {
	g := NewGraph(3, Undirected, false, AdjacencyList)
	err := g.AddEdge(0, 5, 1.0)
	if err == nil {
		t.Error("Expected error for invalid edge")
	}
}

// Test DFS
func TestDFSRecursive(t *testing.T) {
	g := NewGraph(5, Undirected, false, AdjacencyList)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(0, 4, 1.0)
	g.AddEdge(1, 2, 1.0)
	g.AddEdge(1, 3, 1.0)

	traversal := g.DFSRecursive(0)
	if len(traversal) != 5 {
		t.Errorf("Expected 5 vertices in traversal, got %d", len(traversal))
	}
	if traversal[0] != 0 {
		t.Errorf("Expected start vertex 0, got %d", traversal[0])
	}

	// Check all vertices visited
	visited := make(map[int]bool)
	for _, v := range traversal {
		visited[v] = true
	}
	if len(visited) != 5 {
		t.Errorf("Expected all 5 vertices visited, got %d", len(visited))
	}
}

func TestDFSIterative(t *testing.T) {
	g := NewGraph(5, Undirected, false, AdjacencyList)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(0, 4, 1.0)
	g.AddEdge(1, 2, 1.0)
	g.AddEdge(1, 3, 1.0)

	traversal := g.DFSIterative(0)
	if len(traversal) != 5 {
		t.Errorf("Expected 5 vertices in traversal, got %d", len(traversal))
	}
	if traversal[0] != 0 {
		t.Errorf("Expected start vertex 0, got %d", traversal[0])
	}
}

// Test BFS
func TestBFS(t *testing.T) {
	g := NewGraph(5, Undirected, false, AdjacencyList)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(0, 4, 1.0)
	g.AddEdge(1, 2, 1.0)
	g.AddEdge(1, 3, 1.0)

	traversal := g.BFS(0)
	if len(traversal) != 5 {
		t.Errorf("Expected 5 vertices in traversal, got %d", len(traversal))
	}
	if traversal[0] != 0 {
		t.Errorf("Expected start vertex 0, got %d", traversal[0])
	}
}

// Test topological sorting
func TestTopologicalSort(t *testing.T) {
	g := NewGraph(6, Directed, false, AdjacencyList)
	g.AddEdge(5, 2, 1.0)
	g.AddEdge(5, 0, 1.0)
	g.AddEdge(4, 0, 1.0)
	g.AddEdge(4, 1, 1.0)
	g.AddEdge(2, 3, 1.0)
	g.AddEdge(3, 1, 1.0)

	topo := g.TopologicalSort()
	if topo == nil {
		t.Error("Expected topological sort result, got nil")
	}
	if len(topo) != 6 {
		t.Errorf("Expected 6 vertices in topo sort, got %d", len(topo))
	}

	// Verify topological ordering
	position := make(map[int]int)
	for i, v := range topo {
		position[v] = i
	}

	for u := 0; u < g.NumVertices; u++ {
		for _, neighbor := range g.GetNeighbors(u) {
			if position[u] >= position[neighbor.Vertex] {
				t.Errorf("Edge %d->%d violates topological order", u, neighbor.Vertex)
			}
		}
	}
}

func TestTopologicalSortDFS(t *testing.T) {
	g := NewGraph(4, Directed, false, AdjacencyList)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(0, 2, 1.0)
	g.AddEdge(1, 2, 1.0)
	g.AddEdge(2, 3, 1.0)

	topo := g.TopologicalSortDFS()
	if topo == nil {
		t.Error("Expected topological sort result, got nil")
	}
	if len(topo) != 4 {
		t.Errorf("Expected 4 vertices in topo sort, got %d", len(topo))
	}
}

func TestTopologicalSortDetectsCycle(t *testing.T) {
	g := NewGraph(3, Directed, false, AdjacencyList)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, 1.0)
	g.AddEdge(2, 0, 1.0) // Creates cycle

	topo := g.TopologicalSort()
	if topo != nil {
		t.Error("Expected nil for cyclic graph, got result")
	}
}

// Test connected components
func TestSingleConnectedComponent(t *testing.T) {
	g := NewGraph(4, Undirected, false, AdjacencyList)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, 1.0)
	g.AddEdge(2, 3, 1.0)

	components := g.FindConnectedComponents()
	if len(components) != 1 {
		t.Errorf("Expected 1 component, got %d", len(components))
	}
	if len(components[0]) != 4 {
		t.Errorf("Expected 4 vertices in component, got %d", len(components[0]))
	}
}

func TestMultipleConnectedComponents(t *testing.T) {
	g := NewGraph(7, Undirected, false, AdjacencyList)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, 1.0)
	g.AddEdge(3, 4, 1.0)
	g.AddEdge(5, 6, 1.0)

	components := g.FindConnectedComponents()
	if len(components) != 3 {
		t.Errorf("Expected 3 components, got %d", len(components))
	}
}

func TestIsConnected(t *testing.T) {
	g1 := NewGraph(3, Undirected, false, AdjacencyList)
	g1.AddEdge(0, 1, 1.0)
	g1.AddEdge(1, 2, 1.0)
	if !g1.IsConnected() {
		t.Error("Expected graph to be connected")
	}

	g2 := NewGraph(4, Undirected, false, AdjacencyList)
	g2.AddEdge(0, 1, 1.0)
	g2.AddEdge(2, 3, 1.0)
	if g2.IsConnected() {
		t.Error("Expected graph to be disconnected")
	}
}

// Test cycle detection
func TestUndirectedGraphHasCycle(t *testing.T) {
	g := NewGraph(5, Undirected, false, AdjacencyList)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, 1.0)
	g.AddEdge(2, 3, 1.0)
	g.AddEdge(3, 4, 1.0)
	g.AddEdge(4, 0, 1.0) // Creates cycle

	if !g.HasCycle() {
		t.Error("Expected cycle to be detected")
	}
}

func TestUndirectedGraphNoCycle(t *testing.T) {
	g := NewGraph(4, Undirected, false, AdjacencyList)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, 1.0)
	g.AddEdge(2, 3, 1.0)

	if g.HasCycle() {
		t.Error("Expected no cycle")
	}
}

func TestDirectedGraphHasCycle(t *testing.T) {
	g := NewGraph(3, Directed, false, AdjacencyList)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, 1.0)
	g.AddEdge(2, 0, 1.0) // Creates cycle

	if !g.HasCycle() {
		t.Error("Expected cycle to be detected")
	}
}

func TestDirectedGraphNoCycle(t *testing.T) {
	g := NewGraph(4, Directed, false, AdjacencyList)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(0, 2, 1.0)
	g.AddEdge(1, 3, 1.0)
	g.AddEdge(2, 3, 1.0)

	if g.HasCycle() {
		t.Error("Expected no cycle in DAG")
	}
}

// Test graph coloring
func TestGreedyColoring(t *testing.T) {
	g := NewGraph(5, Undirected, false, AdjacencyList)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(0, 2, 1.0)
	g.AddEdge(1, 2, 1.0)
	g.AddEdge(1, 3, 1.0)
	g.AddEdge(2, 3, 1.0)
	g.AddEdge(3, 4, 1.0)

	coloring := g.GreedyColoring()

	if len(coloring) != 5 {
		t.Errorf("Expected all 5 vertices colored, got %d", len(coloring))
	}

	// Check no adjacent vertices have same color
	for u := 0; u < g.NumVertices; u++ {
		for _, neighbor := range g.GetNeighbors(u) {
			if coloring[u] == coloring[neighbor.Vertex] {
				t.Errorf("Adjacent vertices %d and %d have same color", u, neighbor.Vertex)
			}
		}
	}
}

func TestChromaticNumberCompleteGraph(t *testing.T) {
	g := CompleteGraph(4, Undirected, AdjacencyList)
	chromatic := g.ChromaticNumberUpperBound()

	if chromatic != 4 {
		t.Errorf("Expected chromatic number 4 for K4, got %d", chromatic)
	}
}

// Test graph generators
func TestCompleteGraphGenerator(t *testing.T) {
	g := CompleteGraph(5, Undirected, AdjacencyList)

	if g.NumVertices != 5 {
		t.Errorf("Expected 5 vertices, got %d", g.NumVertices)
	}
	if g.NumEdges != 10 {
		t.Errorf("Expected 10 edges for K5, got %d", g.NumEdges)
	}

	for v := 0; v < 5; v++ {
		neighbors := g.GetNeighbors(v)
		if len(neighbors) != 4 {
			t.Errorf("Expected degree 4 for all vertices, got %d for vertex %d",
				len(neighbors), v)
		}
	}
}

func TestCycleGraphGenerator(t *testing.T) {
	g := CycleGraph(6, Undirected, AdjacencyList)

	if g.NumVertices != 6 {
		t.Errorf("Expected 6 vertices, got %d", g.NumVertices)
	}
	if g.NumEdges != 6 {
		t.Errorf("Expected 6 edges, got %d", g.NumEdges)
	}

	for v := 0; v < 6; v++ {
		neighbors := g.GetNeighbors(v)
		if len(neighbors) != 2 {
			t.Errorf("Expected degree 2 for all vertices, got %d for vertex %d",
				len(neighbors), v)
		}
	}
}

func TestRandomGraphGenerator(t *testing.T) {
	g := RandomGraph(10, 0.5, Undirected, false, AdjacencyList)

	if g.NumVertices != 10 {
		t.Errorf("Expected 10 vertices, got %d", g.NumVertices)
	}
	if g.NumEdges == 0 {
		t.Error("Expected some edges in random graph")
	}
}

func TestDAGGenerator(t *testing.T) {
	g := DAG(10, 0.3, AdjacencyList)

	if g.NumVertices != 10 {
		t.Errorf("Expected 10 vertices, got %d", g.NumVertices)
	}
	if g.HasCycle() {
		t.Error("DAG should not have cycle")
	}

	topo := g.TopologicalSort()
	if topo == nil {
		t.Error("DAG should be topologically sortable")
	}
}

// Test different representations
func TestAdjacencyMatrixWeightedEdges(t *testing.T) {
	g := NewGraph(4, Directed, true, AdjacencyMatrix)
	g.AddEdge(0, 1, 2.5)
	g.AddEdge(0, 2, 1.0)

	neighbors := g.GetNeighbors(0)
	if len(neighbors) != 2 {
		t.Errorf("Expected 2 neighbors, got %d", len(neighbors))
	}
}

// Test visualization
func TestASCIIVisualization(t *testing.T) {
	g := NewGraph(3, Undirected, false, AdjacencyList)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, 1.0)

	ascii := g.ToASCII(80)

	if len(ascii) == 0 {
		t.Error("Expected non-empty ASCII output")
	}
	// Check for expected content
	// Note: Actual checks would depend on exact format
}

// Test edge cases
func TestEmptyGraphOperations(t *testing.T) {
	g := NewGraph(0, Undirected, false, AdjacencyList)

	components := g.FindConnectedComponents()
	if len(components) != 0 {
		t.Errorf("Expected no components, got %d", len(components))
	}

	if !g.IsConnected() {
		t.Error("Empty graph should be considered connected")
	}
}

func TestSingleVertexGraph(t *testing.T) {
	g := NewGraph(1, Undirected, false, AdjacencyList)

	components := g.FindConnectedComponents()
	if len(components) != 1 {
		t.Errorf("Expected 1 component, got %d", len(components))
	}
	if len(components[0]) != 1 {
		t.Errorf("Expected 1 vertex in component, got %d", len(components[0]))
	}
}

func TestGetNeighborsNoEdges(t *testing.T) {
	g := NewGraph(3, Undirected, false, AdjacencyList)
	neighbors := g.GetNeighbors(0)
	if len(neighbors) != 0 {
		t.Errorf("Expected no neighbors, got %d", len(neighbors))
	}
}
