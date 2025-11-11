/**
 * Comprehensive Minimum Spanning Tree (MST) Algorithms
 * =====================================================
 *
 * Implements three classic MST algorithms with various optimizations:
 * 1. Kruskal's Algorithm with Union-Find (path compression + union by rank)
 * 2. Prim's Algorithm with BinaryHeap priority queue
 * 3. Borůvka's Algorithm (parallel-friendly)
 *
 * Features:
 * - Support for disconnected graphs (Minimum Spanning Forest)
 * - Memory-safe Rust implementations
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

use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap, HashSet};
use std::time::Instant;

// ========================================================================
// UNION-FIND DATA STRUCTURE
// ========================================================================

/// Union-Find (Disjoint Set Union) data structure
///
/// Implements path compression and union by rank for near O(1) operations.
pub struct UnionFind {
    parent: Vec<usize>,
    rank: Vec<usize>,
    component_count: usize,
}

impl UnionFind {
    pub fn new(n: usize) -> Self {
        UnionFind {
            parent: (0..n).collect(),
            rank: vec![0; n],
            component_count: n,
        }
    }

    /// Find the representative (root) of the set containing x
    /// Uses path compression for optimization
    pub fn find(&mut self, x: usize) -> usize {
        if self.parent[x] != x {
            self.parent[x] = self.find(self.parent[x]); // Path compression
        }
        self.parent[x]
    }

    /// Union the sets containing x and y
    /// Uses union by rank for optimization
    pub fn union(&mut self, x: usize, y: usize) -> bool {
        let mut px = self.find(x);
        let mut py = self.find(y);

        if px == py {
            return false; // Already in same set
        }

        // Union by rank
        if self.rank[px] < self.rank[py] {
            std::mem::swap(&mut px, &mut py);
        }

        self.parent[py] = px;
        if self.rank[px] == self.rank[py] {
            self.rank[px] += 1;
        }

        self.component_count -= 1;
        true
    }

    pub fn connected(&mut self, x: usize, y: usize) -> bool {
        self.find(x) == self.find(y)
    }

    pub fn get_component_count(&self) -> usize {
        self.component_count
    }
}

// ========================================================================
// EDGE STRUCTURE
// ========================================================================

/// Represents a weighted edge in a graph
#[derive(Debug, Clone, Copy)]
pub struct Edge {
    pub u: usize,
    pub v: usize,
    pub weight: f64,
}

impl Edge {
    pub fn new(u: usize, v: usize, weight: f64) -> Self {
        Edge { u, v, weight }
    }
}

impl PartialEq for Edge {
    fn eq(&self, other: &Self) -> bool {
        self.weight == other.weight
    }
}

impl Eq for Edge {}

impl PartialOrd for Edge {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        // Reverse ordering for min-heap
        other.weight.partial_cmp(&self.weight)
    }
}

impl Ord for Edge {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap_or(Ordering::Equal)
    }
}

// ========================================================================
// MST RESULT
// ========================================================================

/// Result of MST computation
#[derive(Debug)]
pub struct MSTResult {
    pub mst_edges: Vec<Edge>,
    pub total_weight: f64,
    pub forest: Vec<Vec<Edge>>,
}

impl MSTResult {
    fn new() -> Self {
        MSTResult {
            mst_edges: Vec::new(),
            total_weight: 0.0,
            forest: Vec::new(),
        }
    }
}

// ========================================================================
// MST ALGORITHMS
// ========================================================================

/// Collection of Minimum Spanning Tree algorithms
pub struct MSTAlgorithms {
    num_vertices: usize,
    edges: Vec<Edge>,
    adj_list: Vec<Vec<Edge>>,
}

impl MSTAlgorithms {
    pub fn new(num_vertices: usize, edges: Vec<Edge>) -> Self {
        let mut mst = MSTAlgorithms {
            num_vertices,
            edges,
            adj_list: vec![Vec::new(); num_vertices],
        };
        mst.build_adjacency_list();
        mst
    }

    fn build_adjacency_list(&mut self) {
        for edge in &self.edges {
            self.adj_list[edge.u].push(*edge);
            self.adj_list[edge.v].push(Edge::new(edge.v, edge.u, edge.weight));
        }
    }

    // ========================================================================
    // KRUSKAL'S ALGORITHM
    // ========================================================================

    /// Kruskal's Algorithm for MST/MSF
    ///
    /// Strategy: Sort edges by weight, add edges that don't create cycles
    /// Uses Union-Find to efficiently detect cycles
    ///
    /// Time Complexity: O(E log E) or O(E log V)
    /// Space Complexity: O(V + E)
    pub fn kruskal(&self, return_forest: bool) -> MSTResult {
        // Sort edges by weight - O(E log E)
        let mut sorted_edges = self.edges.clone();
        sorted_edges.sort_by(|a, b| a.weight.partial_cmp(&b.weight).unwrap());

        let mut uf = UnionFind::new(self.num_vertices);
        let mut result = MSTResult::new();

        for edge in sorted_edges {
            if uf.union(edge.u, edge.v) {
                result.mst_edges.push(edge);
                result.total_weight += edge.weight;

                // Early termination for connected graph
                if !return_forest && result.mst_edges.len() == self.num_vertices - 1 {
                    break;
                }
            }
        }

        if return_forest {
            result.forest = self.build_forest(&result.mst_edges);
        }

        result
    }

    // ========================================================================
    // PRIM'S ALGORITHM
    // ========================================================================

    /// Prim's Algorithm for MST
    ///
    /// Strategy: Grow tree from starting vertex, always add minimum weight edge
    /// that connects tree to non-tree vertex
    ///
    /// Time Complexity: O((V+E) log V)
    /// Space Complexity: O(V + E)
    pub fn prim(&self, start: usize) -> MSTResult {
        let mut result = MSTResult::new();
        let mut visited = HashSet::new();
        visited.insert(start);

        let mut pq = BinaryHeap::new();

        // Add edges from start vertex
        for edge in &self.adj_list[start] {
            pq.push(*edge);
        }

        while let Some(edge) = pq.pop() {
            if visited.contains(&edge.v) {
                continue;
            }

            if visited.len() >= self.num_vertices {
                break;
            }

            // Add edge to MST
            visited.insert(edge.v);
            result.mst_edges.push(edge);
            result.total_weight += edge.weight;

            // Add edges from newly added vertex
            for next_edge in &self.adj_list[edge.v] {
                if !visited.contains(&next_edge.v) {
                    pq.push(*next_edge);
                }
            }
        }

        result
    }

    /// Prim's algorithm using simple array (O(V²) for dense graphs)
    pub fn prim_simple_array(&self, start: usize) -> MSTResult {
        let mut result = MSTResult::new();
        let mut visited = vec![false; self.num_vertices];
        let mut min_weight = vec![f64::INFINITY; self.num_vertices];
        let mut parent = vec![None; self.num_vertices];

        min_weight[start] = 0.0;

        for _ in 0..self.num_vertices {
            // Find minimum weight unvisited vertex - O(V)
            let mut u = None;
            let mut min_val = f64::INFINITY;
            for v in 0..self.num_vertices {
                if !visited[v] && min_weight[v] < min_val {
                    min_val = min_weight[v];
                    u = Some(v);
                }
            }

            if let Some(u) = u {
                if min_weight[u] == f64::INFINITY {
                    break; // Disconnected graph
                }

                visited[u] = true;

                // Add edge to MST (skip first vertex)
                if let Some(p) = parent[u] {
                    result.mst_edges.push(Edge::new(p, u, min_weight[u]));
                    result.total_weight += min_weight[u];
                }

                // Update neighbors
                for edge in &self.adj_list[u] {
                    let v = edge.v;
                    if !visited[v] && edge.weight < min_weight[v] {
                        min_weight[v] = edge.weight;
                        parent[v] = Some(u);
                    }
                }
            }
        }

        result
    }

    // ========================================================================
    // BORŮVKA'S ALGORITHM
    // ========================================================================

    /// Borůvka's (Sollin's) Algorithm for MST
    ///
    /// Strategy: In each phase, find minimum weight edge for each component,
    /// add all such edges simultaneously (parallel-friendly)
    ///
    /// Time Complexity: O(E log V)
    /// Space Complexity: O(V + E)
    pub fn boruvka(&self) -> MSTResult {
        let mut uf = UnionFind::new(self.num_vertices);
        let mut result = MSTResult::new();
        let mut num_components = self.num_vertices;

        while num_components > 1 {
            let mut cheapest = vec![None; self.num_vertices];

            // Find cheapest edge from each component
            for (i, edge) in self.edges.iter().enumerate() {
                let u_root = uf.find(edge.u);
                let v_root = uf.find(edge.v);

                if u_root == v_root {
                    continue; // Same component
                }

                // Check if this is cheapest for component of u
                if cheapest[u_root].is_none() || edge.weight < self.edges[cheapest[u_root].unwrap()].weight {
                    cheapest[u_root] = Some(i);
                }

                // Check if this is cheapest for component of v
                if cheapest[v_root].is_none() || edge.weight < self.edges[cheapest[v_root].unwrap()].weight {
                    cheapest[v_root] = Some(i);
                }
            }

            // Add all cheapest edges
            let mut added_any = false;
            for i in 0..self.num_vertices {
                if let Some(idx) = cheapest[i] {
                    let edge = self.edges[idx];
                    if uf.union(edge.u, edge.v) {
                        result.mst_edges.push(edge);
                        result.total_weight += edge.weight;
                        num_components -= 1;
                        added_any = true;
                    }
                }
            }

            if !added_any {
                break; // Disconnected graph or done
            }
        }

        result
    }

    // ========================================================================
    // UTILITY METHODS
    // ========================================================================

    fn build_forest(&self, edges: &[Edge]) -> Vec<Vec<Edge>> {
        if edges.is_empty() {
            return Vec::new();
        }

        let mut uf = UnionFind::new(self.num_vertices);
        for edge in edges {
            uf.union(edge.u, edge.v);
        }

        let mut component_edges: HashMap<usize, Vec<Edge>> = HashMap::new();
        for edge in edges {
            let root = uf.find(edge.u);
            component_edges.entry(root).or_insert_with(Vec::new).push(*edge);
        }

        component_edges.into_iter().map(|(_, edges)| edges).collect()
    }

    /// Find Minimum Spanning Forest for potentially disconnected graph
    pub fn minimum_spanning_forest(&self, algorithm: &str) -> MSTResult {
        match algorithm {
            "kruskal" => self.kruskal(true),
            "prim" => {
                let mut visited_global = HashSet::new();
                let mut result = MSTResult::new();

                for start in 0..self.num_vertices {
                    if !visited_global.contains(&start) {
                        let tree = self.prim(start);

                        // Mark vertices in this tree as visited
                        for edge in &tree.mst_edges {
                            visited_global.insert(edge.u);
                            visited_global.insert(edge.v);
                        }

                        if !tree.mst_edges.is_empty() {
                            result.forest.push(tree.mst_edges.clone());
                            result.total_weight += tree.total_weight;
                            result.mst_edges.extend(tree.mst_edges);
                        }
                    }
                }

                result
            }
            "boruvka" => {
                let mut result = self.boruvka();
                result.forest = self.build_forest(&result.mst_edges);
                result
            }
            _ => panic!("Unknown algorithm: {}", algorithm),
        }
    }

    /// Compare performance of all MST algorithms
    pub fn compare_algorithms(&self, num_runs: usize) -> HashMap<String, HashMap<String, f64>> {
        let mut results = HashMap::new();

        // Kruskal's
        let mut kruskal_times = Vec::new();
        let mut k_result = None;
        for _ in 0..num_runs {
            let start = Instant::now();
            k_result = Some(self.kruskal(false));
            kruskal_times.push(start.elapsed().as_secs_f64() * 1000.0);
        }
        let k_result = k_result.unwrap();

        let mut k_metrics = HashMap::new();
        k_metrics.insert("meanTime".to_string(), kruskal_times.iter().sum::<f64>() / kruskal_times.len() as f64);
        k_metrics.insert("minTime".to_string(), kruskal_times.iter().cloned().fold(f64::INFINITY, f64::min));
        k_metrics.insert("maxTime".to_string(), kruskal_times.iter().cloned().fold(f64::NEG_INFINITY, f64::max));
        k_metrics.insert("weight".to_string(), k_result.total_weight);
        k_metrics.insert("numEdges".to_string(), k_result.mst_edges.len() as f64);
        results.insert("kruskal".to_string(), k_metrics);

        // Prim's
        let mut prim_times = Vec::new();
        let mut p_result = None;
        for _ in 0..num_runs {
            let start = Instant::now();
            p_result = Some(self.prim(0));
            prim_times.push(start.elapsed().as_secs_f64() * 1000.0);
        }
        let p_result = p_result.unwrap();

        let mut p_metrics = HashMap::new();
        p_metrics.insert("meanTime".to_string(), prim_times.iter().sum::<f64>() / prim_times.len() as f64);
        p_metrics.insert("minTime".to_string(), prim_times.iter().cloned().fold(f64::INFINITY, f64::min));
        p_metrics.insert("maxTime".to_string(), prim_times.iter().cloned().fold(f64::NEG_INFINITY, f64::max));
        p_metrics.insert("weight".to_string(), p_result.total_weight);
        p_metrics.insert("numEdges".to_string(), p_result.mst_edges.len() as f64);
        results.insert("prim".to_string(), p_metrics);

        // Borůvka's
        let mut boruvka_times = Vec::new();
        let mut b_result = None;
        for _ in 0..num_runs {
            let start = Instant::now();
            b_result = Some(self.boruvka());
            boruvka_times.push(start.elapsed().as_secs_f64() * 1000.0);
        }
        let b_result = b_result.unwrap();

        let mut b_metrics = HashMap::new();
        b_metrics.insert("meanTime".to_string(), boruvka_times.iter().sum::<f64>() / boruvka_times.len() as f64);
        b_metrics.insert("minTime".to_string(), boruvka_times.iter().cloned().fold(f64::INFINITY, f64::min));
        b_metrics.insert("maxTime".to_string(), boruvka_times.iter().cloned().fold(f64::NEG_INFINITY, f64::max));
        b_metrics.insert("weight".to_string(), b_result.total_weight);
        b_metrics.insert("numEdges".to_string(), b_result.mst_edges.len() as f64);
        results.insert("boruvka".to_string(), b_metrics);

        results
    }
}

// ========================================================================
// DEMO
// ========================================================================

fn demo_mst_algorithms() {
    println!("{}", "=".repeat(80));
    println!("MINIMUM SPANNING TREE ALGORITHMS DEMO");
    println!("{}", "=".repeat(80));
    println!();

    let edges = vec![
        Edge::new(0, 1, 4.0),
        Edge::new(0, 7, 8.0),
        Edge::new(1, 2, 8.0),
        Edge::new(1, 7, 11.0),
        Edge::new(2, 3, 7.0),
        Edge::new(2, 5, 4.0),
        Edge::new(2, 8, 2.0),
        Edge::new(3, 4, 9.0),
        Edge::new(3, 5, 14.0),
        Edge::new(4, 5, 10.0),
        Edge::new(5, 6, 2.0),
        Edge::new(6, 7, 1.0),
        Edge::new(6, 8, 6.0),
        Edge::new(7, 8, 7.0),
    ];

    let mst = MSTAlgorithms::new(9, edges);

    // Kruskal's
    println!("1. KRUSKAL'S ALGORITHM");
    println!("{}", "-".repeat(80));
    let k_result = mst.kruskal(false);
    println!("MST Weight: {:.2}", k_result.total_weight);
    print!("Edges: ");
    for e in &k_result.mst_edges {
        print!("({},{},{:.0}) ", e.u, e.v, e.weight);
    }
    println!("\n");

    // Prim's
    println!("2. PRIM'S ALGORITHM");
    println!("{}", "-".repeat(80));
    let p_result = mst.prim(0);
    println!("MST Weight: {:.2}", p_result.total_weight);
    print!("Edges: ");
    for e in &p_result.mst_edges {
        print!("({},{},{:.0}) ", e.u, e.v, e.weight);
    }
    println!("\n");

    // Borůvka's
    println!("3. BORŮVKA'S ALGORITHM");
    println!("{}", "-".repeat(80));
    let b_result = mst.boruvka();
    println!("MST Weight: {:.2}", b_result.total_weight);
    print!("Edges: ");
    for e in &b_result.mst_edges {
        print!("({},{},{:.0}) ", e.u, e.v, e.weight);
    }
    println!("\n");

    // Performance
    println!("4. PERFORMANCE COMPARISON");
    println!("{}", "-".repeat(80));
    let results = mst.compare_algorithms(100);

    for (algo, metrics) in results.iter() {
        println!("\n{}", algo.to_uppercase());
        println!("  Mean time: {:.4} ms", metrics["meanTime"]);
        println!("  Min time:  {:.4} ms", metrics["minTime"]);
        println!("  Max time:  {:.4} ms", metrics["maxTime"]);
        println!("  Weight:    {:.2}", metrics["weight"]);
    }
    println!();

    // Disconnected graph
    println!("5. MINIMUM SPANNING FOREST (Disconnected Graph)");
    println!("{}", "-".repeat(80));
    let disconnected_edges = vec![
        Edge::new(0, 1, 1.0),
        Edge::new(1, 2, 2.0),
        Edge::new(3, 4, 3.0),
        Edge::new(4, 5, 4.0),
    ];

    let mst_forest = MSTAlgorithms::new(6, disconnected_edges);
    let forest_result = mst_forest.minimum_spanning_forest("kruskal");

    println!("Number of trees: {}", forest_result.forest.len());
    println!("Total weight: {:.2}", forest_result.total_weight);
    for (i, tree) in forest_result.forest.iter().enumerate() {
        println!("\nTree {}:", i + 1);
        print!("  Edges: ");
        for e in tree {
            print!("({},{},{:.0}) ", e.u, e.v, e.weight);
        }
        println!();
    }
}

fn main() {
    demo_mst_algorithms();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_union_find() {
        let mut uf = UnionFind::new(5);
        assert!(uf.union(0, 1));
        assert!(uf.union(2, 3));
        assert!(uf.connected(0, 1));
        assert!(!uf.connected(0, 2));
        assert!(uf.union(1, 3));
        assert!(uf.connected(0, 3));
    }

    #[test]
    fn test_kruskal() {
        let edges = vec![
            Edge::new(0, 1, 1.0),
            Edge::new(1, 2, 2.0),
            Edge::new(0, 2, 3.0),
        ];
        let mst = MSTAlgorithms::new(3, edges);
        let result = mst.kruskal(false);
        assert_eq!(result.mst_edges.len(), 2);
        assert_eq!(result.total_weight, 3.0);
    }

    #[test]
    fn test_prim() {
        let edges = vec![
            Edge::new(0, 1, 1.0),
            Edge::new(1, 2, 2.0),
            Edge::new(0, 2, 3.0),
        ];
        let mst = MSTAlgorithms::new(3, edges);
        let result = mst.prim(0);
        assert_eq!(result.mst_edges.len(), 2);
        assert_eq!(result.total_weight, 3.0);
    }

    #[test]
    fn test_boruvka() {
        let edges = vec![
            Edge::new(0, 1, 1.0),
            Edge::new(1, 2, 2.0),
            Edge::new(0, 2, 3.0),
        ];
        let mst = MSTAlgorithms::new(3, edges);
        let result = mst.boruvka();
        assert_eq!(result.mst_edges.len(), 2);
        assert_eq!(result.total_weight, 3.0);
    }
}
