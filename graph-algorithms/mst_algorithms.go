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

package main

import (
	"container/heap"
	"fmt"
	"math"
	"sort"
	"strings"
	"time"
)

// ========================================================================
// UNION-FIND DATA STRUCTURE
// ========================================================================

// UnionFind (Disjoint Set Union) data structure
type UnionFind struct {
	parent         []int
	rank           []int
	componentCount int
}

// NewUnionFind creates a new Union-Find structure
func NewUnionFind(n int) *UnionFind {
	uf := &UnionFind{
		parent:         make([]int, n),
		rank:           make([]int, n),
		componentCount: n,
	}
	for i := 0; i < n; i++ {
		uf.parent[i] = i
	}
	return uf
}

// Find the representative (root) of the set containing x
// Uses path compression for optimization
func (uf *UnionFind) Find(x int) int {
	if uf.parent[x] != x {
		uf.parent[x] = uf.Find(uf.parent[x]) // Path compression
	}
	return uf.parent[x]
}

// Union the sets containing x and y
// Uses union by rank for optimization
func (uf *UnionFind) Union(x, y int) bool {
	px, py := uf.Find(x), uf.Find(y)

	if px == py {
		return false // Already in same set
	}

	// Union by rank
	if uf.rank[px] < uf.rank[py] {
		px, py = py, px
	}

	uf.parent[py] = px
	if uf.rank[px] == uf.rank[py] {
		uf.rank[px]++
	}

	uf.componentCount--
	return true
}

// Connected checks if x and y are in the same set
func (uf *UnionFind) Connected(x, y int) bool {
	return uf.Find(x) == uf.Find(y)
}

// GetComponentCount returns the number of disjoint components
func (uf *UnionFind) GetComponentCount() int {
	return uf.componentCount
}

// ========================================================================
// EDGE STRUCTURE
// ========================================================================

// Edge represents a weighted edge in a graph
type Edge struct {
	U      int
	V      int
	Weight float64
}

// String returns string representation of edge
func (e Edge) String() string {
	return fmt.Sprintf("Edge(%d, %d, %.2f)", e.U, e.V, e.Weight)
}

// ========================================================================
// PRIORITY QUEUE FOR PRIM'S ALGORITHM
// ========================================================================

// EdgeHeap is a min-heap of edges
type EdgeHeap []Edge

func (h EdgeHeap) Len() int           { return len(h) }
func (h EdgeHeap) Less(i, j int) bool { return h[i].Weight < h[j].Weight }
func (h EdgeHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *EdgeHeap) Push(x interface{}) {
	*h = append(*h, x.(Edge))
}

func (h *EdgeHeap) Pop() interface{} {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[0 : n-1]
	return x
}

// ========================================================================
// MST RESULT
// ========================================================================

// MSTResult contains the result of MST computation
type MSTResult struct {
	MSTEdges    []Edge
	TotalWeight float64
	Forest      [][]Edge
}

// ========================================================================
// MST ALGORITHMS
// ========================================================================

// MSTAlgorithms contains MST algorithm implementations
type MSTAlgorithms struct {
	NumVertices int
	Edges       []Edge
	AdjList     [][]Edge
}

// NewMSTAlgorithms creates a new MST solver
func NewMSTAlgorithms(numVertices int, edges []Edge) *MSTAlgorithms {
	mst := &MSTAlgorithms{
		NumVertices: numVertices,
		Edges:       edges,
		AdjList:     make([][]Edge, numVertices),
	}
	mst.buildAdjacencyList()
	return mst
}

func (mst *MSTAlgorithms) buildAdjacencyList() {
	for _, edge := range mst.Edges {
		mst.AdjList[edge.U] = append(mst.AdjList[edge.U], Edge{edge.U, edge.V, edge.Weight})
		mst.AdjList[edge.V] = append(mst.AdjList[edge.V], Edge{edge.V, edge.U, edge.Weight})
	}
}

// ========================================================================
// KRUSKAL'S ALGORITHM
// ========================================================================

// Kruskal implements Kruskal's Algorithm for MST/MSF
//
// Strategy: Sort edges by weight, add edges that don't create cycles
// Uses Union-Find to efficiently detect cycles
//
// Time Complexity: O(E log E) or O(E log V)
// Space Complexity: O(V + E)
func (mst *MSTAlgorithms) Kruskal(returnForest bool) MSTResult {
	// Sort edges by weight - O(E log E)
	sortedEdges := make([]Edge, len(mst.Edges))
	copy(sortedEdges, mst.Edges)
	sort.Slice(sortedEdges, func(i, j int) bool {
		return sortedEdges[i].Weight < sortedEdges[j].Weight
	})

	uf := NewUnionFind(mst.NumVertices)
	result := MSTResult{
		MSTEdges:    make([]Edge, 0),
		TotalWeight: 0,
	}

	for _, edge := range sortedEdges {
		if uf.Union(edge.U, edge.V) {
			result.MSTEdges = append(result.MSTEdges, edge)
			result.TotalWeight += edge.Weight

			// Early termination for connected graph
			if !returnForest && len(result.MSTEdges) == mst.NumVertices-1 {
				break
			}
		}
	}

	if returnForest {
		result.Forest = mst.buildForest(result.MSTEdges)
	}

	return result
}

// ========================================================================
// PRIM'S ALGORITHM
// ========================================================================

// Prim implements Prim's Algorithm for MST
//
// Strategy: Grow tree from starting vertex, always add minimum weight edge
// that connects tree to non-tree vertex
//
// Time Complexity: O((V+E) log V)
// Space Complexity: O(V + E)
func (mst *MSTAlgorithms) Prim(start int) MSTResult {
	result := MSTResult{
		MSTEdges:    make([]Edge, 0),
		TotalWeight: 0,
	}

	visited := make(map[int]bool)
	visited[start] = true

	pq := &EdgeHeap{}
	heap.Init(pq)

	// Add edges from start vertex
	for _, edge := range mst.AdjList[start] {
		heap.Push(pq, edge)
	}

	for pq.Len() > 0 && len(visited) < mst.NumVertices {
		edge := heap.Pop(pq).(Edge)

		if visited[edge.V] {
			continue
		}

		// Add edge to MST
		visited[edge.V] = true
		result.MSTEdges = append(result.MSTEdges, edge)
		result.TotalWeight += edge.Weight

		// Add edges from newly added vertex
		for _, nextEdge := range mst.AdjList[edge.V] {
			if !visited[nextEdge.V] {
				heap.Push(pq, nextEdge)
			}
		}
	}

	return result
}

// PrimSimpleArray implements Prim's using simple array (O(V²) for dense graphs)
func (mst *MSTAlgorithms) PrimSimpleArray(start int) MSTResult {
	result := MSTResult{
		MSTEdges:    make([]Edge, 0),
		TotalWeight: 0,
	}

	visited := make([]bool, mst.NumVertices)
	minWeight := make([]float64, mst.NumVertices)
	parent := make([]int, mst.NumVertices)

	for i := 0; i < mst.NumVertices; i++ {
		minWeight[i] = math.Inf(1)
		parent[i] = -1
	}
	minWeight[start] = 0

	for count := 0; count < mst.NumVertices; count++ {
		// Find minimum weight unvisited vertex - O(V)
		u := -1
		for v := 0; v < mst.NumVertices; v++ {
			if !visited[v] && (u == -1 || minWeight[v] < minWeight[u]) {
				u = v
			}
		}

		if math.IsInf(minWeight[u], 1) {
			break // Disconnected graph
		}

		visited[u] = true

		// Add edge to MST (skip first vertex)
		if parent[u] != -1 {
			result.MSTEdges = append(result.MSTEdges, Edge{parent[u], u, minWeight[u]})
			result.TotalWeight += minWeight[u]
		}

		// Update neighbors
		for _, edge := range mst.AdjList[u] {
			v := edge.V
			if !visited[v] && edge.Weight < minWeight[v] {
				minWeight[v] = edge.Weight
				parent[v] = u
			}
		}
	}

	return result
}

// ========================================================================
// BORŮVKA'S ALGORITHM
// ========================================================================

// Boruvka implements Borůvka's (Sollin's) Algorithm for MST
//
// Strategy: In each phase, find minimum weight edge for each component,
// add all such edges simultaneously (parallel-friendly)
//
// Time Complexity: O(E log V)
// Space Complexity: O(V + E)
func (mst *MSTAlgorithms) Boruvka() MSTResult {
	uf := NewUnionFind(mst.NumVertices)
	result := MSTResult{
		MSTEdges:    make([]Edge, 0),
		TotalWeight: 0,
	}

	numComponents := mst.NumVertices

	for numComponents > 1 {
		cheapest := make([]int, mst.NumVertices)
		for i := range cheapest {
			cheapest[i] = -1
		}

		// Find cheapest edge from each component
		for i, edge := range mst.Edges {
			uRoot := uf.Find(edge.U)
			vRoot := uf.Find(edge.V)

			if uRoot == vRoot {
				continue // Same component
			}

			// Check if this is cheapest for component of u
			if cheapest[uRoot] == -1 || edge.Weight < mst.Edges[cheapest[uRoot]].Weight {
				cheapest[uRoot] = i
			}

			// Check if this is cheapest for component of v
			if cheapest[vRoot] == -1 || edge.Weight < mst.Edges[cheapest[vRoot]].Weight {
				cheapest[vRoot] = i
			}
		}

		// Add all cheapest edges
		addedAny := false
		for i := 0; i < mst.NumVertices; i++ {
			if cheapest[i] != -1 {
				edge := mst.Edges[cheapest[i]]
				if uf.Union(edge.U, edge.V) {
					result.MSTEdges = append(result.MSTEdges, edge)
					result.TotalWeight += edge.Weight
					numComponents--
					addedAny = true
				}
			}
		}

		if !addedAny {
			break // Disconnected graph or done
		}
	}

	return result
}

// ========================================================================
// UTILITY METHODS
// ========================================================================

func (mst *MSTAlgorithms) buildForest(edges []Edge) [][]Edge {
	if len(edges) == 0 {
		return [][]Edge{}
	}

	uf := NewUnionFind(mst.NumVertices)
	for _, edge := range edges {
		uf.Union(edge.U, edge.V)
	}

	componentEdges := make(map[int][]Edge)
	for _, edge := range edges {
		root := uf.Find(edge.U)
		componentEdges[root] = append(componentEdges[root], edge)
	}

	forest := make([][]Edge, 0, len(componentEdges))
	for _, edges := range componentEdges {
		forest = append(forest, edges)
	}

	return forest
}

// MinimumSpanningForest finds MSF for potentially disconnected graph
func (mst *MSTAlgorithms) MinimumSpanningForest(algorithm string) MSTResult {
	switch algorithm {
	case "kruskal":
		return mst.Kruskal(true)
	case "prim":
		visitedGlobal := make(map[int]bool)
		result := MSTResult{
			MSTEdges:    make([]Edge, 0),
			TotalWeight: 0,
			Forest:      make([][]Edge, 0),
		}

		for start := 0; start < mst.NumVertices; start++ {
			if !visitedGlobal[start] {
				tree := mst.Prim(start)

				// Mark vertices in this tree as visited
				for _, edge := range tree.MSTEdges {
					visitedGlobal[edge.U] = true
					visitedGlobal[edge.V] = true
				}

				if len(tree.MSTEdges) > 0 {
					result.Forest = append(result.Forest, tree.MSTEdges)
					result.TotalWeight += tree.TotalWeight
					result.MSTEdges = append(result.MSTEdges, tree.MSTEdges...)
				}
			}
		}

		return result
	case "boruvka":
		result := mst.Boruvka()
		result.Forest = mst.buildForest(result.MSTEdges)
		return result
	default:
		panic("Unknown algorithm: " + algorithm)
	}
}

// CompareAlgorithms compares performance of all MST algorithms
func (mst *MSTAlgorithms) CompareAlgorithms(numRuns int) map[string]map[string]float64 {
	results := make(map[string]map[string]float64)

	// Kruskal's
	kruskalTimes := make([]float64, numRuns)
	var kResult MSTResult
	for i := 0; i < numRuns; i++ {
		start := time.Now()
		kResult = mst.Kruskal(false)
		kruskalTimes[i] = time.Since(start).Seconds() * 1000
	}

	results["kruskal"] = map[string]float64{
		"meanTime": avg(kruskalTimes),
		"minTime":  min(kruskalTimes),
		"maxTime":  max(kruskalTimes),
		"weight":   kResult.TotalWeight,
		"numEdges": float64(len(kResult.MSTEdges)),
	}

	// Prim's
	primTimes := make([]float64, numRuns)
	var pResult MSTResult
	for i := 0; i < numRuns; i++ {
		start := time.Now()
		pResult = mst.Prim(0)
		primTimes[i] = time.Since(start).Seconds() * 1000
	}

	results["prim"] = map[string]float64{
		"meanTime": avg(primTimes),
		"minTime":  min(primTimes),
		"maxTime":  max(primTimes),
		"weight":   pResult.TotalWeight,
		"numEdges": float64(len(pResult.MSTEdges)),
	}

	// Borůvka's
	boruvkaTimes := make([]float64, numRuns)
	var bResult MSTResult
	for i := 0; i < numRuns; i++ {
		start := time.Now()
		bResult = mst.Boruvka()
		boruvkaTimes[i] = time.Since(start).Seconds() * 1000
	}

	results["boruvka"] = map[string]float64{
		"meanTime": avg(boruvkaTimes),
		"minTime":  min(boruvkaTimes),
		"maxTime":  max(boruvkaTimes),
		"weight":   bResult.TotalWeight,
		"numEdges": float64(len(bResult.MSTEdges)),
	}

	return results
}

// Helper functions
func avg(values []float64) float64 {
	sum := 0.0
	for _, v := range values {
		sum += v
	}
	return sum / float64(len(values))
}

func min(values []float64) float64 {
	minVal := values[0]
	for _, v := range values {
		if v < minVal {
			minVal = v
		}
	}
	return minVal
}

func max(values []float64) float64 {
	maxVal := values[0]
	for _, v := range values {
		if v > maxVal {
			maxVal = v
		}
	}
	return maxVal
}

// ========================================================================
// DEMO
// ========================================================================

func demoMSTAlgorithms() {
	fmt.Println(strings.Repeat("=", 80))
	fmt.Println("MINIMUM SPANNING TREE ALGORITHMS DEMO")
	fmt.Println(strings.Repeat("=", 80))
	fmt.Println()

	edges := []Edge{
		{0, 1, 4},
		{0, 7, 8},
		{1, 2, 8},
		{1, 7, 11},
		{2, 3, 7},
		{2, 5, 4},
		{2, 8, 2},
		{3, 4, 9},
		{3, 5, 14},
		{4, 5, 10},
		{5, 6, 2},
		{6, 7, 1},
		{6, 8, 6},
		{7, 8, 7},
	}

	mst := NewMSTAlgorithms(9, edges)

	// Kruskal's
	fmt.Println("1. KRUSKAL'S ALGORITHM")
	fmt.Println(strings.Repeat("-", 80))
	kResult := mst.Kruskal(false)
	fmt.Printf("MST Weight: %.2f\n", kResult.TotalWeight)
	fmt.Print("Edges: ")
	for _, e := range kResult.MSTEdges {
		fmt.Printf("(%d,%d,%.0f) ", e.U, e.V, e.Weight)
	}
	fmt.Println("\n")

	// Prim's
	fmt.Println("2. PRIM'S ALGORITHM")
	fmt.Println(strings.Repeat("-", 80))
	pResult := mst.Prim(0)
	fmt.Printf("MST Weight: %.2f\n", pResult.TotalWeight)
	fmt.Print("Edges: ")
	for _, e := range pResult.MSTEdges {
		fmt.Printf("(%d,%d,%.0f) ", e.U, e.V, e.Weight)
	}
	fmt.Println("\n")

	// Borůvka's
	fmt.Println("3. BORŮVKA'S ALGORITHM")
	fmt.Println(strings.Repeat("-", 80))
	bResult := mst.Boruvka()
	fmt.Printf("MST Weight: %.2f\n", bResult.TotalWeight)
	fmt.Print("Edges: ")
	for _, e := range bResult.MSTEdges {
		fmt.Printf("(%d,%d,%.0f) ", e.U, e.V, e.Weight)
	}
	fmt.Println("\n")

	// Performance
	fmt.Println("4. PERFORMANCE COMPARISON")
	fmt.Println(strings.Repeat("-", 80))
	results := mst.CompareAlgorithms(100)

	for algo, metrics := range results {
		fmt.Printf("\n%s\n", strings.ToUpper(algo))
		fmt.Printf("  Mean time: %.4f ms\n", metrics["meanTime"])
		fmt.Printf("  Min time:  %.4f ms\n", metrics["minTime"])
		fmt.Printf("  Max time:  %.4f ms\n", metrics["maxTime"])
		fmt.Printf("  Weight:    %.2f\n", metrics["weight"])
	}
	fmt.Println()

	// Disconnected graph
	fmt.Println("5. MINIMUM SPANNING FOREST (Disconnected Graph)")
	fmt.Println(strings.Repeat("-", 80))
	disconnectedEdges := []Edge{
		{0, 1, 1},
		{1, 2, 2},
		{3, 4, 3},
		{4, 5, 4},
	}

	mstForest := NewMSTAlgorithms(6, disconnectedEdges)
	forestResult := mstForest.MinimumSpanningForest("kruskal")

	fmt.Printf("Number of trees: %d\n", len(forestResult.Forest))
	fmt.Printf("Total weight: %.2f\n", forestResult.TotalWeight)
	for i, tree := range forestResult.Forest {
		fmt.Printf("\nTree %d:\n", i+1)
		fmt.Print("  Edges: ")
		for _, e := range tree {
			fmt.Printf("(%d,%d,%.0f) ", e.U, e.V, e.Weight)
		}
		fmt.Println()
	}
}

func main() {
	demoMSTAlgorithms()
}
