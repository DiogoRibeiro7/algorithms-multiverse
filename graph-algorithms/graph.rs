// Comprehensive Graph Data Structure Implementation
// Supports multiple representations and core graph algorithms

use std::collections::{HashMap, HashSet, VecDeque};
use rand::Rng;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum GraphType {
    Directed,
    Undirected,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum RepresentationType {
    AdjacencyList,
    AdjacencyMatrix,
    EdgeList,
    CSR, // Compressed Sparse Row
}

#[derive(Debug, Clone)]
pub struct Edge {
    pub src: usize,
    pub dst: usize,
    pub weight: f64,
}

#[derive(Debug, Clone)]
pub struct Neighbor {
    pub vertex: usize,
    pub weight: f64,
}

pub struct Graph {
    num_vertices: usize,
    num_edges: usize,
    graph_type: GraphType,
    weighted: bool,
    representation: RepresentationType,

    // Different representations
    adj_list: HashMap<usize, Vec<Neighbor>>,
    adj_matrix: Vec<Vec<Option<f64>>>,
    edges: Vec<Edge>,
    csr_values: Vec<f64>,
    csr_col_indices: Vec<usize>,
    csr_row_ptr: Vec<usize>,
}

impl Graph {
    /// Create a new graph
    pub fn new(
        num_vertices: usize,
        graph_type: GraphType,
        weighted: bool,
        representation: RepresentationType,
    ) -> Self {
        let mut graph = Graph {
            num_vertices,
            num_edges: 0,
            graph_type,
            weighted,
            representation,
            adj_list: HashMap::new(),
            adj_matrix: Vec::new(),
            edges: Vec::new(),
            csr_values: Vec::new(),
            csr_col_indices: Vec::new(),
            csr_row_ptr: Vec::new(),
        };

        // Initialize based on representation type
        match representation {
            RepresentationType::AdjacencyList => {
                // adj_list is already initialized
            }
            RepresentationType::AdjacencyMatrix => {
                graph.adj_matrix = vec![vec![None; num_vertices]; num_vertices];
            }
            RepresentationType::EdgeList => {
                // edges is already initialized
            }
            RepresentationType::CSR => {
                graph.csr_row_ptr.push(0);
            }
        }

        graph
    }

    /// Add a new vertex and return its ID
    pub fn add_vertex(&mut self) -> usize {
        let vertex_id = self.num_vertices;
        self.num_vertices += 1;

        if self.representation == RepresentationType::AdjacencyMatrix {
            // Expand matrix
            for row in &mut self.adj_matrix {
                row.push(None);
            }
            self.adj_matrix.push(vec![None; self.num_vertices]);
        }

        vertex_id
    }

    /// Add an edge from u to v with optional weight
    pub fn add_edge(&mut self, u: usize, v: usize, weight: f64) -> Result<(), String> {
        if u >= self.num_vertices || v >= self.num_vertices {
            return Err(format!("Vertex out of range: {} or {}", u, v));
        }

        self.num_edges += 1;

        match self.representation {
            RepresentationType::AdjacencyList => {
                self.adj_list
                    .entry(u)
                    .or_insert_with(Vec::new)
                    .push(Neighbor { vertex: v, weight });

                if self.graph_type == GraphType::Undirected {
                    self.adj_list
                        .entry(v)
                        .or_insert_with(Vec::new)
                        .push(Neighbor { vertex: u, weight });
                }
            }
            RepresentationType::AdjacencyMatrix => {
                self.adj_matrix[u][v] = Some(weight);
                if self.graph_type == GraphType::Undirected {
                    self.adj_matrix[v][u] = Some(weight);
                }
            }
            RepresentationType::EdgeList => {
                self.edges.push(Edge {
                    src: u,
                    dst: v,
                    weight,
                });
                if self.graph_type == GraphType::Undirected {
                    self.edges.push(Edge {
                        src: v,
                        dst: u,
                        weight,
                    });
                }
            }
            RepresentationType::CSR => {
                return Err("CSR edges should be added via build_csr()".to_string());
            }
        }

        Ok(())
    }

    /// Build CSR representation from edge list
    pub fn build_csr(&mut self, mut edges: Vec<Edge>) {
        assert_eq!(
            self.representation,
            RepresentationType::CSR,
            "Graph must be CSR type"
        );

        // Sort edges by source vertex
        edges.sort_by(|a, b| a.src.cmp(&b.src).then(a.dst.cmp(&b.dst)));

        self.csr_values.clear();
        self.csr_col_indices.clear();
        self.csr_row_ptr.clear();
        self.csr_row_ptr.push(0);

        let mut current_row = 0;
        for edge in &edges {
            // Fill gaps for vertices with no outgoing edges
            while current_row < edge.src {
                self.csr_row_ptr.push(self.csr_col_indices.len());
                current_row += 1;
            }

            self.csr_values.push(edge.weight);
            self.csr_col_indices.push(edge.dst);
        }

        // Complete row pointers
        while current_row < self.num_vertices {
            self.csr_row_ptr.push(self.csr_col_indices.len());
            current_row += 1;
        }

        self.num_edges = edges.len();
    }

    /// Get neighbors of vertex u with their edge weights
    pub fn get_neighbors(&self, u: usize) -> Vec<Neighbor> {
        match self.representation {
            RepresentationType::AdjacencyList => {
                self.adj_list.get(&u).cloned().unwrap_or_default()
            }
            RepresentationType::AdjacencyMatrix => {
                let mut neighbors = Vec::new();
                for (v, &weight_opt) in self.adj_matrix[u].iter().enumerate() {
                    if let Some(weight) = weight_opt {
                        neighbors.push(Neighbor { vertex: v, weight });
                    }
                }
                neighbors
            }
            RepresentationType::EdgeList => {
                let mut neighbors = Vec::new();
                for edge in &self.edges {
                    if edge.src == u {
                        neighbors.push(Neighbor {
                            vertex: edge.dst,
                            weight: edge.weight,
                        });
                    }
                }
                neighbors
            }
            RepresentationType::CSR => {
                let mut neighbors = Vec::new();
                let start = self.csr_row_ptr[u];
                let end = self.csr_row_ptr[u + 1];
                for i in start..end {
                    neighbors.push(Neighbor {
                        vertex: self.csr_col_indices[i],
                        weight: self.csr_values[i],
                    });
                }
                neighbors
            }
        }
    }

    // === DEPTH-FIRST SEARCH ===

    /// DFS traversal using recursion
    pub fn dfs_recursive(&self, start: usize) -> Vec<usize> {
        let mut visited = HashSet::new();
        let mut traversal = Vec::new();
        self.dfs_helper(start, &mut visited, &mut traversal);
        traversal
    }

    fn dfs_helper(&self, v: usize, visited: &mut HashSet<usize>, traversal: &mut Vec<usize>) {
        visited.insert(v);
        traversal.push(v);

        for neighbor in self.get_neighbors(v) {
            if !visited.contains(&neighbor.vertex) {
                self.dfs_helper(neighbor.vertex, visited, traversal);
            }
        }
    }

    /// DFS traversal using iteration with stack
    pub fn dfs_iterative(&self, start: usize) -> Vec<usize> {
        let mut visited = HashSet::new();
        let mut traversal = Vec::new();
        let mut stack = vec![start];

        while let Some(v) = stack.pop() {
            if !visited.contains(&v) {
                visited.insert(v);
                traversal.push(v);

                // Add neighbors in reverse order for consistent ordering
                let neighbors = self.get_neighbors(v);
                for neighbor in neighbors.iter().rev() {
                    if !visited.contains(&neighbor.vertex) {
                        stack.push(neighbor.vertex);
                    }
                }
            }
        }

        traversal
    }

    // === BREADTH-FIRST SEARCH ===

    /// BFS traversal
    pub fn bfs(&self, start: usize) -> Vec<usize> {
        let mut visited = HashSet::new();
        let mut traversal = Vec::new();
        let mut queue = VecDeque::new();

        visited.insert(start);
        queue.push_back(start);

        while let Some(v) = queue.pop_front() {
            traversal.push(v);

            for neighbor in self.get_neighbors(v) {
                if !visited.contains(&neighbor.vertex) {
                    visited.insert(neighbor.vertex);
                    queue.push_back(neighbor.vertex);
                }
            }
        }

        traversal
    }

    // === TOPOLOGICAL SORTING ===

    /// Topological sorting using Kahn's algorithm (BFS-based)
    /// Returns None if graph contains a cycle
    pub fn topological_sort(&self) -> Option<Vec<usize>> {
        assert_eq!(
            self.graph_type,
            GraphType::Directed,
            "Topological sort only works for directed graphs"
        );

        // Calculate in-degrees
        let mut in_degree = vec![0; self.num_vertices];
        for u in 0..self.num_vertices {
            for neighbor in self.get_neighbors(u) {
                in_degree[neighbor.vertex] += 1;
            }
        }

        // Queue with vertices having 0 in-degree
        let mut queue: VecDeque<usize> = in_degree
            .iter()
            .enumerate()
            .filter(|(_, &deg)| deg == 0)
            .map(|(v, _)| v)
            .collect();

        let mut result = Vec::new();

        while let Some(u) = queue.pop_front() {
            result.push(u);

            for neighbor in self.get_neighbors(u) {
                in_degree[neighbor.vertex] -= 1;
                if in_degree[neighbor.vertex] == 0 {
                    queue.push_back(neighbor.vertex);
                }
            }
        }

        // Check if all vertices were processed (no cycle)
        if result.len() == self.num_vertices {
            Some(result)
        } else {
            None
        }
    }

    /// Topological sorting using DFS
    pub fn topological_sort_dfs(&self) -> Option<Vec<usize>> {
        assert_eq!(
            self.graph_type,
            GraphType::Directed,
            "Topological sort only works for directed graphs"
        );

        let mut visited = HashSet::new();
        let mut rec_stack = HashSet::new();
        let mut result = Vec::new();

        for v in 0..self.num_vertices {
            if !visited.contains(&v) {
                if !self.topo_dfs_helper(v, &mut visited, &mut rec_stack, &mut result) {
                    return None; // Cycle detected
                }
            }
        }

        result.reverse();
        Some(result)
    }

    fn topo_dfs_helper(
        &self,
        v: usize,
        visited: &mut HashSet<usize>,
        rec_stack: &mut HashSet<usize>,
        result: &mut Vec<usize>,
    ) -> bool {
        visited.insert(v);
        rec_stack.insert(v);

        for neighbor in self.get_neighbors(v) {
            if !visited.contains(&neighbor.vertex) {
                if !self.topo_dfs_helper(neighbor.vertex, visited, rec_stack, result) {
                    return false;
                }
            } else if rec_stack.contains(&neighbor.vertex) {
                return false; // Cycle detected
            }
        }

        rec_stack.remove(&v);
        result.push(v);
        true
    }

    // === CONNECTED COMPONENTS ===

    /// Find all connected components in the graph
    pub fn find_connected_components(&self) -> Vec<Vec<usize>> {
        let mut visited = HashSet::new();
        let mut components = Vec::new();

        for v in 0..self.num_vertices {
            if !visited.contains(&v) {
                let mut component = Vec::new();
                let mut stack = vec![v];

                while let Some(u) = stack.pop() {
                    if !visited.contains(&u) {
                        visited.insert(u);
                        component.push(u);

                        for neighbor in self.get_neighbors(u) {
                            if !visited.contains(&neighbor.vertex) {
                                stack.push(neighbor.vertex);
                            }
                        }
                    }
                }

                component.sort();
                components.push(component);
            }
        }

        components
    }

    /// Check if graph is connected
    pub fn is_connected(&self) -> bool {
        if self.num_vertices == 0 {
            return true;
        }
        self.find_connected_components().len() == 1
    }

    // === CYCLE DETECTION ===

    /// Detect cycle in undirected graph using DFS
    pub fn has_cycle_undirected(&self) -> bool {
        assert_eq!(
            self.graph_type,
            GraphType::Undirected,
            "This method is for undirected graphs"
        );

        let mut visited = HashSet::new();

        for v in 0..self.num_vertices {
            if !visited.contains(&v) {
                if self.has_cycle_undirected_helper(v, None, &mut visited) {
                    return true;
                }
            }
        }

        false
    }

    fn has_cycle_undirected_helper(
        &self,
        v: usize,
        parent: Option<usize>,
        visited: &mut HashSet<usize>,
    ) -> bool {
        visited.insert(v);

        for neighbor in self.get_neighbors(v) {
            if !visited.contains(&neighbor.vertex) {
                if self.has_cycle_undirected_helper(neighbor.vertex, Some(v), visited) {
                    return true;
                }
            } else if Some(neighbor.vertex) != parent {
                return true; // Cycle found
            }
        }

        false
    }

    /// Detect cycle in directed graph using DFS with recursion stack
    pub fn has_cycle_directed(&self) -> bool {
        assert_eq!(
            self.graph_type,
            GraphType::Directed,
            "This method is for directed graphs"
        );

        let mut visited = HashSet::new();
        let mut rec_stack = HashSet::new();

        for v in 0..self.num_vertices {
            if !visited.contains(&v) {
                if self.has_cycle_directed_helper(v, &mut visited, &mut rec_stack) {
                    return true;
                }
            }
        }

        false
    }

    fn has_cycle_directed_helper(
        &self,
        v: usize,
        visited: &mut HashSet<usize>,
        rec_stack: &mut HashSet<usize>,
    ) -> bool {
        visited.insert(v);
        rec_stack.insert(v);

        for neighbor in self.get_neighbors(v) {
            if !visited.contains(&neighbor.vertex) {
                if self.has_cycle_directed_helper(neighbor.vertex, visited, rec_stack) {
                    return true;
                }
            } else if rec_stack.contains(&neighbor.vertex) {
                return true; // Back edge found
            }
        }

        rec_stack.remove(&v);
        false
    }

    /// Detect cycle based on graph type
    pub fn has_cycle(&self) -> bool {
        match self.graph_type {
            GraphType::Directed => self.has_cycle_directed(),
            GraphType::Undirected => self.has_cycle_undirected(),
        }
    }

    // === GRAPH COLORING ===

    /// Graph coloring using greedy algorithm
    /// Returns mapping of vertex -> color
    pub fn greedy_coloring(&self) -> HashMap<usize, usize> {
        let mut colors = HashMap::new();

        for v in 0..self.num_vertices {
            // Get colors of neighbors
            let mut neighbor_colors = HashSet::new();
            for neighbor in self.get_neighbors(v) {
                if let Some(&color) = colors.get(&neighbor.vertex) {
                    neighbor_colors.insert(color);
                }
            }

            // Find first available color
            let mut color = 0;
            while neighbor_colors.contains(&color) {
                color += 1;
            }

            colors.insert(v, color);
        }

        colors
    }

    /// Get upper bound on chromatic number
    pub fn chromatic_number_upper_bound(&self) -> usize {
        let coloring = self.greedy_coloring();
        if coloring.is_empty() {
            return 0;
        }
        coloring.values().max().unwrap() + 1
    }

    // === VISUALIZATION ===

    /// Generate ASCII art representation of the graph
    pub fn to_ascii(&self, max_width: usize) -> String {
        let mut output = String::new();

        output.push_str(&"=".repeat(max_width));
        output.push('\n');
        output.push_str(&format!(
            "Graph: {:?}, {}\n",
            self.graph_type,
            if self.weighted { "weighted" } else { "unweighted" }
        ));
        output.push_str(&format!("Representation: {:?}\n", self.representation));
        output.push_str(&format!(
            "Vertices: {}, Edges: {}\n",
            self.num_vertices, self.num_edges
        ));
        output.push_str(&"=".repeat(max_width));
        output.push_str("\n\n");

        match self.representation {
            RepresentationType::AdjacencyList => {
                output.push_str("Adjacency List:\n");
                for v in 0..self.num_vertices {
                    let neighbors = self.get_neighbors(v);
                    output.push_str(&format!("  {} -> [", v));
                    for (i, neighbor) in neighbors.iter().enumerate() {
                        if self.weighted {
                            output.push_str(&format!("{}({:.1})", neighbor.vertex, neighbor.weight));
                        } else {
                            output.push_str(&format!("{}", neighbor.vertex));
                        }
                        if i < neighbors.len() - 1 {
                            output.push_str(", ");
                        }
                    }
                    output.push_str("]\n");
                }
            }
            RepresentationType::AdjacencyMatrix => {
                output.push_str("Adjacency Matrix:\n");
                let display_size = self.num_vertices.min(15);

                // Header
                output.push_str("    ");
                for i in 0..display_size {
                    output.push_str(&format!("{:4} ", i));
                }
                output.push_str(&format!("\n    {}\n", "-".repeat(5 * display_size)));

                for i in 0..display_size {
                    output.push_str(&format!("{:2} |", i));
                    for j in 0..display_size {
                        if let Some(weight) = self.adj_matrix[i][j] {
                            output.push_str(&format!("{:4.0} ", weight));
                        } else {
                            output.push_str("   . ");
                        }
                    }
                    output.push('\n');
                }

                if self.num_vertices > 15 {
                    output.push_str("  ... (truncated)\n");
                }
            }
            RepresentationType::EdgeList => {
                output.push_str("Edge List:\n");
                let display_limit = self.edges.len().min(50);
                for (i, edge) in self.edges.iter().take(display_limit).enumerate() {
                    if self.weighted {
                        output.push_str(&format!(
                            "  {}: {} -> {} (weight: {:.1})\n",
                            i, edge.src, edge.dst, edge.weight
                        ));
                    } else {
                        output.push_str(&format!("  {}: {} -> {}\n", i, edge.src, edge.dst));
                    }
                }
                if self.edges.len() > 50 {
                    output.push_str(&format!("  ... ({} more edges)\n", self.edges.len() - 50));
                }
            }
            RepresentationType::CSR => {
                output.push_str("CSR (Compressed Sparse Row):\n");
                let val_limit = self.csr_values.len().min(20);
                output.push_str("  Values: [");
                for (i, &val) in self.csr_values.iter().take(val_limit).enumerate() {
                    output.push_str(&format!("{:.1}", val));
                    if i < val_limit - 1 {
                        output.push_str(", ");
                    }
                }
                if self.csr_values.len() > 20 {
                    output.push_str(", ...");
                }
                output.push_str("]\n");

                let col_limit = self.csr_col_indices.len().min(20);
                output.push_str("  Col Indices: [");
                for (i, &col) in self.csr_col_indices.iter().take(col_limit).enumerate() {
                    output.push_str(&format!("{}", col));
                    if i < col_limit - 1 {
                        output.push_str(", ");
                    }
                }
                if self.csr_col_indices.len() > 20 {
                    output.push_str(", ...");
                }
                output.push_str("]\n");

                let row_limit = self.csr_row_ptr.len().min(20);
                output.push_str("  Row Ptrs: [");
                for (i, &row) in self.csr_row_ptr.iter().take(row_limit).enumerate() {
                    output.push_str(&format!("{}", row));
                    if i < row_limit - 1 {
                        output.push_str(", ");
                    }
                }
                if self.csr_row_ptr.len() > 20 {
                    output.push_str(", ...");
                }
                output.push_str("]\n");
            }
        }

        output.push('\n');
        output.push_str(&"=".repeat(max_width));
        output.push('\n');

        output
    }
}

// === GRAPH GENERATORS ===

/// Generate a complete graph with n vertices
pub fn complete_graph(
    n: usize,
    graph_type: GraphType,
    representation: RepresentationType,
) -> Graph {
    let mut g = Graph::new(n, graph_type, false, representation);

    if representation == RepresentationType::CSR {
        let mut edges = Vec::new();
        for i in 0..n {
            for j in 0..n {
                if i != j {
                    edges.push(Edge {
                        src: i,
                        dst: j,
                        weight: 1.0,
                    });
                }
            }
        }
        g.build_csr(edges);
    } else {
        for i in 0..n {
            for j in (i + 1)..n {
                g.add_edge(i, j, 1.0).unwrap();
                if graph_type == GraphType::Directed {
                    g.add_edge(j, i, 1.0).unwrap();
                }
            }
        }
    }

    g
}

/// Generate a cycle graph with n vertices
pub fn cycle_graph(n: usize, graph_type: GraphType, representation: RepresentationType) -> Graph {
    let mut g = Graph::new(n, graph_type, false, representation);

    if representation == RepresentationType::CSR {
        let mut edges = Vec::new();
        for i in 0..n {
            edges.push(Edge {
                src: i,
                dst: (i + 1) % n,
                weight: 1.0,
            });
            if graph_type == GraphType::Undirected {
                edges.push(Edge {
                    src: (i + 1) % n,
                    dst: i,
                    weight: 1.0,
                });
            }
        }
        g.build_csr(edges);
    } else {
        for i in 0..n {
            g.add_edge(i, (i + 1) % n, 1.0).unwrap();
        }
    }

    g
}

/// Generate random graph with Erdős-Rényi model
pub fn random_graph(
    n: usize,
    edge_probability: f64,
    graph_type: GraphType,
    weighted: bool,
    representation: RepresentationType,
) -> Graph {
    let mut g = Graph::new(n, graph_type, weighted, representation);
    let mut edges = Vec::new();
    let mut rng = rand::thread_rng();

    for i in 0..n {
        let start = if graph_type == GraphType::Undirected { i + 1 } else { 0 };
        for j in start..n {
            if i != j && rng.gen::<f64>() < edge_probability {
                let weight = if weighted {
                    rng.gen::<f64>() * 9.0 + 1.0
                } else {
                    1.0
                };
                edges.push(Edge {
                    src: i,
                    dst: j,
                    weight,
                });
            }
        }
    }

    if representation == RepresentationType::CSR {
        if graph_type == GraphType::Undirected {
            let original_len = edges.len();
            for i in 0..original_len {
                edges.push(Edge {
                    src: edges[i].dst,
                    dst: edges[i].src,
                    weight: edges[i].weight,
                });
            }
        }
        g.build_csr(edges);
    } else {
        for edge in edges {
            g.add_edge(edge.src, edge.dst, edge.weight).unwrap();
        }
    }

    g
}

/// Generate a random Directed Acyclic Graph (DAG)
pub fn dag(n: usize, edge_probability: f64, representation: RepresentationType) -> Graph {
    let mut g = Graph::new(n, GraphType::Directed, false, representation);
    let mut edges = Vec::new();
    let mut rng = rand::thread_rng();

    for i in 0..n {
        for j in (i + 1)..n {
            if rng.gen::<f64>() < edge_probability {
                edges.push(Edge {
                    src: i,
                    dst: j,
                    weight: 1.0,
                });
            }
        }
    }

    if representation == RepresentationType::CSR {
        g.build_csr(edges);
    } else {
        for edge in edges {
            g.add_edge(edge.src, edge.dst, edge.weight).unwrap();
        }
    }

    g
}

// === DEMO AND TESTING ===

fn demo() {
    println!("{}", "=".repeat(80));
    println!("GRAPH DATA STRUCTURES AND ALGORITHMS DEMO");
    println!("{}", "=".repeat(80));
    println!();

    // Demo 1: Adjacency List
    println!("1. ADJACENCY LIST REPRESENTATION");
    println!("{}", "-".repeat(80));
    let mut g1 = Graph::new(5, GraphType::Undirected, false, RepresentationType::AdjacencyList);
    g1.add_edge(0, 1, 1.0).unwrap();
    g1.add_edge(0, 4, 1.0).unwrap();
    g1.add_edge(1, 2, 1.0).unwrap();
    g1.add_edge(1, 3, 1.0).unwrap();
    g1.add_edge(1, 4, 1.0).unwrap();
    g1.add_edge(2, 3, 1.0).unwrap();
    g1.add_edge(3, 4, 1.0).unwrap();
    print!("{}", g1.to_ascii(80));

    // Demo 2: DFS and BFS
    println!("2. GRAPH TRAVERSAL");
    println!("{}", "-".repeat(80));
    println!("DFS Recursive from 0: {:?}", g1.dfs_recursive(0));
    println!("DFS Iterative from 0: {:?}", g1.dfs_iterative(0));
    println!("BFS from 0: {:?}", g1.bfs(0));
    println!();

    // Demo 3: Connected Components
    println!("3. CONNECTED COMPONENTS");
    println!("{}", "-".repeat(80));
    let mut g2 = Graph::new(7, GraphType::Undirected, false, RepresentationType::AdjacencyList);
    g2.add_edge(0, 1, 1.0).unwrap();
    g2.add_edge(1, 2, 1.0).unwrap();
    g2.add_edge(3, 4, 1.0).unwrap();
    g2.add_edge(5, 6, 1.0).unwrap();
    println!("Components: {:?}", g2.find_connected_components());
    println!("Is connected: {}", g2.is_connected());
    println!();

    // Demo 4: Cycle Detection
    println!("4. CYCLE DETECTION");
    println!("{}", "-".repeat(80));
    println!("Graph g1 has cycle: {}", g1.has_cycle());
    let mut g3 = Graph::new(3, GraphType::Undirected, false, RepresentationType::AdjacencyList);
    g3.add_edge(0, 1, 1.0).unwrap();
    g3.add_edge(1, 2, 1.0).unwrap();
    println!("Linear graph has cycle: {}", g3.has_cycle());
    println!();

    // Demo 5: Topological Sort
    println!("5. TOPOLOGICAL SORTING");
    println!("{}", "-".repeat(80));
    let dag_graph = dag(6, 0.3, RepresentationType::AdjacencyList);
    print!("{}", dag_graph.to_ascii(80));
    println!("Topological order: {:?}", dag_graph.topological_sort());
    println!("Topological order (DFS): {:?}", dag_graph.topological_sort_dfs());
    println!();

    // Demo 6: Graph Coloring
    println!("6. GRAPH COLORING");
    println!("{}", "-".repeat(80));
    println!("Greedy coloring: {:?}", g1.greedy_coloring());
    println!("Chromatic number (upper bound): {}", g1.chromatic_number_upper_bound());
    println!();

    // Demo 7: Different Representations
    println!("7. ADJACENCY MATRIX REPRESENTATION");
    println!("{}", "-".repeat(80));
    let mut g4 = Graph::new(5, GraphType::Directed, true, RepresentationType::AdjacencyMatrix);
    g4.add_edge(0, 1, 2.5).unwrap();
    g4.add_edge(0, 2, 1.0).unwrap();
    g4.add_edge(1, 3, 3.0).unwrap();
    g4.add_edge(2, 3, 1.5).unwrap();
    g4.add_edge(3, 4, 2.0).unwrap();
    print!("{}", g4.to_ascii(80));

    // Demo 8: Graph Generators
    println!("8. GRAPH GENERATORS");
    println!("{}", "-".repeat(80));
    let complete = complete_graph(5, GraphType::Undirected, RepresentationType::AdjacencyList);
    println!("Complete graph K5:");
    print!("{}", complete.to_ascii(80));

    let cycle = cycle_graph(6, GraphType::Undirected, RepresentationType::AdjacencyList);
    println!("Cycle graph C6:");
    print!("{}", cycle.to_ascii(80));
}

fn main() {
    demo();
}
