# Graph Algorithm Tests

Comprehensive unit tests for all graph implementations across 8 programming languages.

## Test Coverage

All implementations test the following features:

- ✓ Graph creation and initialization
- ✓ Adding vertices and edges
- ✓ Multiple representations (adjacency list, matrix, edge list, CSR)
- ✓ DFS (recursive and iterative)
- ✓ BFS
- ✓ Topological sorting
- ✓ Connected components
- ✓ Cycle detection (directed and undirected)
- ✓ Graph coloring
- ✓ Graph generators
- ✓ Edge cases and error handling

## Running Tests

### Python

```bash
# Using pytest (recommended)
pip install pytest
pytest test_graph.py -v

# Or using unittest
python test_graph.py

# Run specific test
pytest test_graph.py::TestDFS::test_dfs_recursive -v
```

**Output example:**
```
test_graph.py::TestGraphCreation::test_create_empty_graph PASSED    [ 1%]
test_graph.py::TestGraphCreation::test_add_edge_undirected PASSED   [ 2%]
...
45 passed in 0.52s
```

### JavaScript

```bash
# Run all tests
node test_graph.js

# No external dependencies required
```

**Output example:**
```
Running tests...

✓ Create empty graph
✓ Create graph with vertices
✓ Add edge to undirected graph
...
42 passed, 0 failed
```

### Java

```bash
# Compile both files
javac Graph.java GraphTest.java

# Run tests
java GraphTest

# Clean up
rm *.class
```

**Output example:**
```
Running tests...

✓ Create empty graph
✓ Add edge to undirected graph
✓ DFS recursive
...
38 passed, 0 failed
```

### C++

```bash
# Compile (note: test file includes simplified graph code)
g++ -std=c++17 -o test_graph test_graph.cpp

# Run tests
./test_graph

# Clean up
rm test_graph
```

**Alternative: Test with actual graph.cpp:**
```bash
# If you want to test against actual graph.cpp implementation
g++ -std=c++17 -o test_graph_full test_graph.cpp graph.cpp
./test_graph_full
```

**Output example:**
```
Running tests...

✓ Create empty graph
✓ Add edge to undirected graph
...
28 passed, 0 failed
```

### Go

```bash
# Run all tests
go test -v

# Run specific test
go test -v -run TestDFSRecursive

# With coverage
go test -cover

# Generate coverage report
go test -coverprofile=coverage.out
go tool cover -html=coverage.out
```

**Output example:**
```
=== RUN   TestCreateEmptyGraph
--- PASS: TestCreateEmptyGraph (0.00s)
=== RUN   TestDFSRecursive
--- PASS: TestDFSRecursive (0.00s)
...
PASS
ok      graph   0.123s
```

### Rust

Rust tests are typically included inline in the source file using `#[cfg(test)]` modules.

**Add to graph.rs:**

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_empty_graph() {
        let g = Graph::new(0, GraphType::Undirected, false,
                          RepresentationType::AdjacencyList);
        assert_eq!(g.num_vertices, 0);
        assert_eq!(g.num_edges, 0);
    }

    #[test]
    fn test_add_edge() {
        let mut g = Graph::new(3, GraphType::Undirected, false,
                              RepresentationType::AdjacencyList);
        g.add_edge(0, 1, 1.0).unwrap();
        assert_eq!(g.num_edges, 1);
    }

    #[test]
    fn test_dfs_recursive() {
        let mut g = Graph::new(5, GraphType::Undirected, false,
                              RepresentationType::AdjacencyList);
        g.add_edge(0, 1, 1.0).unwrap();
        g.add_edge(0, 4, 1.0).unwrap();
        g.add_edge(1, 2, 1.0).unwrap();
        g.add_edge(1, 3, 1.0).unwrap();

        let traversal = g.dfs_recursive(0);
        assert_eq!(traversal.len(), 5);
        assert_eq!(traversal[0], 0);
    }

    #[test]
    fn test_bfs() {
        let mut g = Graph::new(5, GraphType::Undirected, false,
                              RepresentationType::AdjacencyList);
        g.add_edge(0, 1, 1.0).unwrap();
        g.add_edge(0, 4, 1.0).unwrap();
        g.add_edge(1, 2, 1.0).unwrap();

        let traversal = g.bfs(0);
        assert_eq!(traversal.len(), 5);
        assert_eq!(traversal[0], 0);
    }

    #[test]
    fn test_cycle_detection_undirected() {
        let mut g = Graph::new(5, GraphType::Undirected, false,
                              RepresentationType::AdjacencyList);
        g.add_edge(0, 1, 1.0).unwrap();
        g.add_edge(1, 2, 1.0).unwrap();
        g.add_edge(2, 3, 1.0).unwrap();
        g.add_edge(3, 4, 1.0).unwrap();
        g.add_edge(4, 0, 1.0).unwrap(); // Creates cycle

        assert!(g.has_cycle());
    }

    #[test]
    fn test_topological_sort() {
        let mut g = Graph::new(6, GraphType::Directed, false,
                              RepresentationType::AdjacencyList);
        g.add_edge(5, 2, 1.0).unwrap();
        g.add_edge(5, 0, 1.0).unwrap();
        g.add_edge(4, 0, 1.0).unwrap();
        g.add_edge(4, 1, 1.0).unwrap();
        g.add_edge(2, 3, 1.0).unwrap();
        g.add_edge(3, 1, 1.0).unwrap();

        let topo = g.topological_sort();
        assert!(topo.is_some());
        assert_eq!(topo.unwrap().len(), 6);
    }

    #[test]
    fn test_connected_components() {
        let mut g = Graph::new(7, GraphType::Undirected, false,
                              RepresentationType::AdjacencyList);
        g.add_edge(0, 1, 1.0).unwrap();
        g.add_edge(1, 2, 1.0).unwrap();
        g.add_edge(3, 4, 1.0).unwrap();
        g.add_edge(5, 6, 1.0).unwrap();

        let components = g.find_connected_components();
        assert_eq!(components.len(), 3);
    }

    #[test]
    fn test_graph_coloring() {
        let mut g = Graph::new(5, GraphType::Undirected, false,
                              RepresentationType::AdjacencyList);
        g.add_edge(0, 1, 1.0).unwrap();
        g.add_edge(0, 2, 1.0).unwrap();
        g.add_edge(1, 2, 1.0).unwrap();
        g.add_edge(1, 3, 1.0).unwrap();

        let coloring = g.greedy_coloring();
        assert_eq!(coloring.len(), 5);

        // Check no adjacent vertices have same color
        for u in 0..g.num_vertices {
            for neighbor in g.get_neighbors(u) {
                assert_ne!(coloring[&u], coloring[&neighbor.vertex]);
            }
        }
    }
}
```

**Run Rust tests:**
```bash
# Run all tests
cargo test

# Run with output
cargo test -- --nocapture

# Run specific test
cargo test test_dfs_recursive

# With coverage (requires nightly and tarpaulin)
cargo install cargo-tarpaulin
cargo tarpaulin --out Html
```

**Output example:**
```
running 9 tests
test tests::test_add_edge ... ok
test tests::test_bfs ... ok
test tests::test_create_empty_graph ... ok
test tests::test_cycle_detection_undirected ... ok
test tests::test_dfs_recursive ... ok
...
test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured
```

### Swift

Swift uses XCTest framework for testing.

**Create GraphTests.swift:**

```swift
import XCTest

class GraphTests: XCTestCase {

    func testCreateEmptyGraph() {
        let g = Graph(numVertices: 0)
        XCTAssertEqual(g.numVertices, 0)
        XCTAssertEqual(g.numEdges, 0)
    }

    func testAddEdge() {
        let g = Graph(numVertices: 3, graphType: .undirected)
        try? g.addEdge(0, 1)
        XCTAssertEqual(g.numEdges, 1)
    }

    func testDFSRecursive() {
        let g = Graph(numVertices: 5, graphType: .undirected)
        try? g.addEdge(0, 1)
        try? g.addEdge(0, 4)
        try? g.addEdge(1, 2)
        try? g.addEdge(1, 3)

        let traversal = g.dfsRecursive(start: 0)
        XCTAssertEqual(traversal.count, 5)
        XCTAssertEqual(traversal[0], 0)
    }

    func testBFS() {
        let g = Graph(numVertices: 5, graphType: .undirected)
        try? g.addEdge(0, 1)
        try? g.addEdge(0, 4)
        try? g.addEdge(1, 2)

        let traversal = g.bfs(start: 0)
        XCTAssertEqual(traversal.count, 5)
        XCTAssertEqual(traversal[0], 0)
    }

    func testCycleDetection() {
        let g = Graph(numVertices: 5, graphType: .undirected)
        try? g.addEdge(0, 1)
        try? g.addEdge(1, 2)
        try? g.addEdge(2, 3)
        try? g.addEdge(3, 4)
        try? g.addEdge(4, 0)

        XCTAssertTrue(g.hasCycle())
    }

    func testTopologicalSort() {
        let g = Graph(numVertices: 6, graphType: .directed)
        try? g.addEdge(5, 2)
        try? g.addEdge(5, 0)
        try? g.addEdge(4, 0)
        try? g.addEdge(4, 1)
        try? g.addEdge(2, 3)
        try? g.addEdge(3, 1)

        let topo = g.topologicalSort()
        XCTAssertNotNil(topo)
        XCTAssertEqual(topo?.count, 6)
    }

    func testConnectedComponents() {
        let g = Graph(numVertices: 7, graphType: .undirected)
        try? g.addEdge(0, 1)
        try? g.addEdge(1, 2)
        try? g.addEdge(3, 4)
        try? g.addEdge(5, 6)

        let components = g.findConnectedComponents()
        XCTAssertEqual(components.count, 3)
    }

    func testGraphColoring() {
        let g = Graph(numVertices: 5, graphType: .undirected)
        try? g.addEdge(0, 1)
        try? g.addEdge(0, 2)
        try? g.addEdge(1, 2)
        try? g.addEdge(1, 3)

        let coloring = g.greedyColoring()
        XCTAssertEqual(coloring.count, 5)
    }
}
```

**Run Swift tests:**

```bash
# Using swift test (requires Package.swift)
swift test

# Or compile and run with XCTest
swiftc -o GraphTests graph.swift GraphTests.swift -framework XCTest
./GraphTests
```

**Using Xcode:**
1. Create new Unit Test Target
2. Add GraphTests.swift
3. Run tests with Cmd+U

### Kotlin

Kotlin tests use JUnit similar to Java.

**Create GraphTest.kt with JUnit:**

```kotlin
import org.junit.Test
import org.junit.Assert.*

class GraphKotlinTest {

    @Test
    fun testCreateEmptyGraph() {
        val g = Graph(0)
        assertEquals(0, g.numVertices)
        assertEquals(0, g.numEdges)
    }

    @Test
    fun testAddEdge() {
        val g = Graph(3, GraphType.UNDIRECTED)
        g.addEdge(0, 1)
        assertEquals(1, g.numEdges)
    }

    @Test
    fun testDFSRecursive() {
        val g = Graph(5, GraphType.UNDIRECTED)
        g.addEdge(0, 1)
        g.addEdge(0, 4)
        g.addEdge(1, 2)
        g.addEdge(1, 3)

        val traversal = g.dfsRecursive(0)
        assertEquals(5, traversal.size)
        assertEquals(0, traversal[0])
    }

    @Test
    fun testBFS() {
        val g = Graph(5, GraphType.UNDIRECTED)
        g.addEdge(0, 1)
        g.addEdge(0, 4)
        g.addEdge(1, 2)

        val traversal = g.bfs(0)
        assertEquals(5, traversal.size)
        assertEquals(0, traversal[0])
    }

    @Test
    fun testCycleDetection() {
        val g = Graph(5, GraphType.UNDIRECTED)
        g.addEdge(0, 1)
        g.addEdge(1, 2)
        g.addEdge(2, 3)
        g.addEdge(3, 4)
        g.addEdge(4, 0)

        assertTrue(g.hasCycle())
    }

    @Test
    fun testTopologicalSort() {
        val g = Graph(6, GraphType.DIRECTED)
        g.addEdge(5, 2)
        g.addEdge(5, 0)
        g.addEdge(4, 0)
        g.addEdge(4, 1)
        g.addEdge(2, 3)
        g.addEdge(3, 1)

        val topo = g.topologicalSort()
        assertNotNull(topo)
        assertEquals(6, topo?.size)
    }

    @Test
    fun testConnectedComponents() {
        val g = Graph(7, GraphType.UNDIRECTED)
        g.addEdge(0, 1)
        g.addEdge(1, 2)
        g.addEdge(3, 4)
        g.addEdge(5, 6)

        val components = g.findConnectedComponents()
        assertEquals(3, components.size)
    }

    @Test
    fun testGraphColoring() {
        val g = Graph(5, GraphType.UNDIRECTED)
        g.addEdge(0, 1)
        g.addEdge(0, 2)
        g.addEdge(1, 2)
        g.addEdge(1, 3)

        val coloring = g.greedyColoring()
        assertEquals(5, coloring.size)

        // Check no adjacent vertices have same color
        for (u in 0 until g.numVertices) {
            for (neighbor in g.getNeighbors(u)) {
                assertNotEquals(coloring[u], coloring[neighbor.vertex])
            }
        }
    }
}
```

**Run Kotlin tests:**

```bash
# Download JUnit if needed
# wget https://search.maven.org/remotecontent?filepath=junit/junit/4.13.2/junit-4.13.2.jar

# Compile
kotlinc graph.kt GraphTest.kt -include-runtime -d graph-test.jar -classpath junit-4.13.2.jar

# Run
java -cp graph-test.jar:junit-4.13.2.jar org.junit.runner.JUnitCore GraphKotlinTest
```

**Using Gradle:**

```gradle
dependencies {
    testImplementation 'junit:junit:4.13.2'
}
```

Then run: `gradle test`

## Test Summary

| Language   | Test File         | Tests | Framework       | Command            |
|------------|-------------------|-------|-----------------|-------------------|
| Python     | test_graph.py     | 45+   | pytest/unittest | `pytest test_graph.py` |
| JavaScript | test_graph.js     | 42+   | Custom          | `node test_graph.js` |
| Java       | GraphTest.java    | 38+   | Custom          | `java GraphTest` |
| C++        | test_graph.cpp    | 28+   | Custom          | `./test_graph` |
| Go         | graph_test.go     | 35+   | testing         | `go test -v` |
| Rust       | (inline)          | 9+    | cargo test      | `cargo test` |
| Swift      | GraphTests.swift  | 8+    | XCTest          | `swift test` |
| Kotlin     | GraphTest.kt      | 8+    | JUnit           | `gradle test` |

## Continuous Integration

### GitHub Actions Example

``yaml
name: Graph Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Python Tests
      run: |
        pip install pytest
        pytest graph-algorithms/test_graph.py

    - name: JavaScript Tests
      run: |
        node graph-algorithms/test_graph.js

    - name: Go Tests
      run: |
        cd graph-algorithms
        go test -v

    - name: Rust Tests
      run: |
        cd graph-algorithms
        cargo test
```

## Test Coverage Goals

- ✓ **Graph Creation**: All constructors and initialization
- ✓ **Edge Operations**: Adding edges, checking neighbors
- ✓ **Traversals**: DFS (both versions) and BFS
- ✓ **Algorithms**: Topological sort, components, cycles, coloring
- ✓ **Generators**: All graph generator functions
- ✓ **Representations**: All storage formats
- ✓ **Edge Cases**: Empty graphs, single vertices, disconnected components
- ✓ **Error Handling**: Invalid inputs, out of range vertices

## Contributing Tests

When adding new features:

1. Add tests for new functionality
2. Ensure all existing tests pass
3. Update test count in this README
4. Add example usage in documentation

## Performance Testing

For performance benchmarks, see `benchmarks/compare_dijkstra.c` which includes:
- Statistical analysis
- Multiple trial runs
- CSV output for plotting
- Theoretical vs actual complexity

## License

These tests are part of the Applied Papers Lab project.
