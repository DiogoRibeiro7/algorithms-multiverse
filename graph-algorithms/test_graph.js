/**
 * Comprehensive unit tests for graph.js
 *
 * Run with:
 *    node test_graph.js
 */

const { Graph, GraphGenerator, GraphType, RepresentationType } = require('./graph.js');

// Simple test framework
class TestRunner {
    constructor() {
        this.passed = 0;
        this.failed = 0;
        this.tests = [];
    }

    test(name, fn) {
        this.tests.push({ name, fn });
    }

    assert(condition, message) {
        if (!condition) {
            throw new Error(message || 'Assertion failed');
        }
    }

    assertEqual(actual, expected, message) {
        if (actual !== expected) {
            throw new Error(message || `Expected ${expected} but got ${actual}`);
        }
    }

    assertArrayEqual(actual, expected, message) {
        if (JSON.stringify(actual) !== JSON.stringify(expected)) {
            throw new Error(message || `Arrays not equal: ${JSON.stringify(actual)} !== ${JSON.stringify(expected)}`);
        }
    }

    assertTrue(condition, message) {
        this.assert(condition === true, message || 'Expected true');
    }

    assertFalse(condition, message) {
        this.assert(condition === false, message || 'Expected false');
    }

    assertThrows(fn, message) {
        try {
            fn();
            throw new Error(message || 'Expected function to throw');
        } catch (e) {
            if (e.message === message || !message) {
                // Expected exception
            } else {
                throw e;
            }
        }
    }

    async run() {
        console.log('Running tests...\n');

        for (const {name, fn} of this.tests) {
            try {
                await fn.call(this);
                console.log(`✓ ${name}`);
                this.passed++;
            } catch (error) {
                console.log(`✗ ${name}`);
                console.log(`  ${error.message}`);
                this.failed++;
            }
        }

        console.log(`\n${this.passed} passed, ${this.failed} failed`);
        return this.failed === 0;
    }
}

const runner = new TestRunner();

// ============================================================================
// Graph Creation Tests
// ============================================================================

runner.test('Create empty graph', function() {
    const g = new Graph(0);
    this.assertEqual(g.numVertices, 0);
    this.assertEqual(g.numEdges, 0);
});

runner.test('Create graph with vertices', function() {
    const g = new Graph(5);
    this.assertEqual(g.numVertices, 5);
    this.assertEqual(g.numEdges, 0);
});

runner.test('Add vertex', function() {
    const g = new Graph(2);
    const vertexId = g.addVertex();
    this.assertEqual(vertexId, 2);
    this.assertEqual(g.numVertices, 3);
});

runner.test('Add edge to undirected graph', function() {
    const g = new Graph(3, GraphType.UNDIRECTED);
    g.addEdge(0, 1, 5.0);
    this.assertEqual(g.numEdges, 1);

    const neighbors = g.getNeighbors(0);
    this.assertEqual(neighbors.length, 1);
    this.assertEqual(neighbors[0][0], 1);
    this.assertEqual(neighbors[0][1], 5.0);
});

runner.test('Add edge to directed graph', function() {
    const g = new Graph(3, GraphType.DIRECTED);
    g.addEdge(0, 1);
    this.assertEqual(g.numEdges, 1);

    this.assertEqual(g.getNeighbors(0).length, 1);
    this.assertEqual(g.getNeighbors(1).length, 0);
});

runner.test('Invalid edge throws error', function() {
    const g = new Graph(3);
    this.assertThrows(() => g.addEdge(0, 5));
});

// ============================================================================
// Adjacency List Tests
// ============================================================================

runner.test('Adjacency list neighbors', function() {
    const g = new Graph(5, GraphType.UNDIRECTED, false, RepresentationType.ADJACENCY_LIST);
    g.addEdge(0, 1);
    g.addEdge(0, 4);
    g.addEdge(1, 2);
    g.addEdge(1, 3);
    g.addEdge(1, 4);

    const neighbors = g.getNeighbors(1);
    const vertices = neighbors.map(n => n[0]);
    this.assertTrue(vertices.includes(0));
    this.assertTrue(vertices.includes(2));
    this.assertTrue(vertices.includes(3));
    this.assertTrue(vertices.includes(4));
});

// ============================================================================
// Adjacency Matrix Tests
// ============================================================================

runner.test('Adjacency matrix weighted edges', function() {
    const g = new Graph(4, GraphType.DIRECTED, true, RepresentationType.ADJACENCY_MATRIX);
    g.addEdge(0, 1, 2.5);
    g.addEdge(0, 2, 1.0);

    const neighbors = g.getNeighbors(0);
    this.assertEqual(neighbors.length, 2);

    const weights = {};
    neighbors.forEach(([v, w]) => weights[v] = w);
    this.assertEqual(weights[1], 2.5);
    this.assertEqual(weights[2], 1.0);
});

// ============================================================================
// DFS Tests
// ============================================================================

runner.test('DFS recursive', function() {
    const g = new Graph(5, GraphType.UNDIRECTED);
    g.addEdge(0, 1);
    g.addEdge(0, 4);
    g.addEdge(1, 2);
    g.addEdge(1, 3);
    g.addEdge(2, 3);

    const traversal = g.dfsRecursive(0);
    this.assertEqual(traversal.length, 5);
    this.assertEqual(traversal[0], 0);

    const visitedSet = new Set(traversal);
    this.assertEqual(visitedSet.size, 5);
});

runner.test('DFS iterative', function() {
    const g = new Graph(5, GraphType.UNDIRECTED);
    g.addEdge(0, 1);
    g.addEdge(0, 4);
    g.addEdge(1, 2);
    g.addEdge(1, 3);

    const traversal = g.dfsIterative(0);
    this.assertEqual(traversal.length, 5);
    this.assertEqual(traversal[0], 0);
});

runner.test('DFS on disconnected component', function() {
    const g = new Graph(6);
    g.addEdge(0, 1);
    g.addEdge(2, 3);

    const traversal = g.dfsRecursive(0);
    this.assertEqual(new Set(traversal).size, 2);
    this.assertTrue(traversal.includes(0));
    this.assertTrue(traversal.includes(1));
});

// ============================================================================
// BFS Tests
// ============================================================================

runner.test('BFS traversal', function() {
    const g = new Graph(5, GraphType.UNDIRECTED);
    g.addEdge(0, 1);
    g.addEdge(0, 4);
    g.addEdge(1, 2);
    g.addEdge(1, 3);

    const traversal = g.bfs(0);
    this.assertEqual(traversal.length, 5);
    this.assertEqual(traversal[0], 0);
});

// ============================================================================
// Topological Sort Tests
// ============================================================================

runner.test('Topological sort on DAG', function() {
    const g = new Graph(6, GraphType.DIRECTED);
    g.addEdge(5, 2);
    g.addEdge(5, 0);
    g.addEdge(4, 0);
    g.addEdge(4, 1);
    g.addEdge(2, 3);
    g.addEdge(3, 1);

    const topo = g.topologicalSort();
    this.assertTrue(topo !== null);
    this.assertEqual(topo.length, 6);

    // Verify topological ordering
    const position = {};
    topo.forEach((v, i) => position[v] = i);

    for (let u = 0; u < g.numVertices; u++) {
        for (const [v, _] of g.getNeighbors(u)) {
            this.assertTrue(position[u] < position[v],
                `Edge ${u}->${v} violates topological order`);
        }
    }
});

runner.test('Topological sort DFS', function() {
    const g = new Graph(4, GraphType.DIRECTED);
    g.addEdge(0, 1);
    g.addEdge(0, 2);
    g.addEdge(1, 2);
    g.addEdge(2, 3);

    const topo = g.topologicalSortDFS();
    this.assertTrue(topo !== null);
    this.assertEqual(topo.length, 4);
});

runner.test('Topological sort detects cycle', function() {
    const g = new Graph(3, GraphType.DIRECTED);
    g.addEdge(0, 1);
    g.addEdge(1, 2);
    g.addEdge(2, 0);

    const topo = g.topologicalSort();
    this.assertTrue(topo === null);
});

runner.test('Topological sort throws on undirected', function() {
    const g = new Graph(3, GraphType.UNDIRECTED);
    this.assertThrows(() => g.topologicalSort());
});

// ============================================================================
// Connected Components Tests
// ============================================================================

runner.test('Single connected component', function() {
    const g = new Graph(4);
    g.addEdge(0, 1);
    g.addEdge(1, 2);
    g.addEdge(2, 3);

    const components = g.findConnectedComponents();
    this.assertEqual(components.length, 1);
    this.assertEqual(components[0].length, 4);
});

runner.test('Multiple connected components', function() {
    const g = new Graph(7);
    g.addEdge(0, 1);
    g.addEdge(1, 2);
    g.addEdge(3, 4);
    g.addEdge(5, 6);

    const components = g.findConnectedComponents();
    this.assertEqual(components.length, 3);
});

runner.test('Is connected', function() {
    const g1 = new Graph(3);
    g1.addEdge(0, 1);
    g1.addEdge(1, 2);
    this.assertTrue(g1.isConnected());

    const g2 = new Graph(4);
    g2.addEdge(0, 1);
    g2.addEdge(2, 3);
    this.assertFalse(g2.isConnected());
});

// ============================================================================
// Cycle Detection Tests
// ============================================================================

runner.test('Undirected graph has cycle', function() {
    const g = new Graph(5, GraphType.UNDIRECTED);
    g.addEdge(0, 1);
    g.addEdge(1, 2);
    g.addEdge(2, 3);
    g.addEdge(3, 4);
    g.addEdge(4, 0);

    this.assertTrue(g.hasCycle());
});

runner.test('Undirected graph no cycle', function() {
    const g = new Graph(4, GraphType.UNDIRECTED);
    g.addEdge(0, 1);
    g.addEdge(1, 2);
    g.addEdge(2, 3);

    this.assertFalse(g.hasCycle());
});

runner.test('Directed graph has cycle', function() {
    const g = new Graph(3, GraphType.DIRECTED);
    g.addEdge(0, 1);
    g.addEdge(1, 2);
    g.addEdge(2, 0);

    this.assertTrue(g.hasCycle());
});

runner.test('Directed graph no cycle (DAG)', function() {
    const g = new Graph(4, GraphType.DIRECTED);
    g.addEdge(0, 1);
    g.addEdge(0, 2);
    g.addEdge(1, 3);
    g.addEdge(2, 3);

    this.assertFalse(g.hasCycle());
});

// ============================================================================
// Graph Coloring Tests
// ============================================================================

runner.test('Greedy coloring', function() {
    const g = new Graph(5, GraphType.UNDIRECTED);
    g.addEdge(0, 1);
    g.addEdge(0, 2);
    g.addEdge(1, 2);
    g.addEdge(1, 3);
    g.addEdge(2, 3);
    g.addEdge(3, 4);

    const coloring = g.greedyColoring();

    // Check all vertices are colored
    this.assertEqual(coloring.size, 5);

    // Check no adjacent vertices have same color
    for (let u = 0; u < g.numVertices; u++) {
        for (const [v, _] of g.getNeighbors(u)) {
            this.assertTrue(coloring.get(u) !== coloring.get(v),
                `Adjacent vertices ${u} and ${v} have same color`);
        }
    }
});

runner.test('Chromatic number complete graph', function() {
    const g = GraphGenerator.completeGraph(4);
    const chromatic = g.chromaticNumberUpperBound();

    this.assertEqual(chromatic, 4);
});

// ============================================================================
// Graph Generator Tests
// ============================================================================

runner.test('Complete graph generator', function() {
    const g = GraphGenerator.completeGraph(5);

    this.assertEqual(g.numVertices, 5);
    this.assertEqual(g.numEdges, 10);

    for (let v = 0; v < 5; v++) {
        const neighbors = g.getNeighbors(v);
        this.assertEqual(neighbors.length, 4);
    }
});

runner.test('Cycle graph generator', function() {
    const g = GraphGenerator.cycleGraph(6);

    this.assertEqual(g.numVertices, 6);
    this.assertEqual(g.numEdges, 6);

    for (let v = 0; v < 6; v++) {
        const neighbors = g.getNeighbors(v);
        this.assertEqual(neighbors.length, 2);
    }
});

runner.test('Random graph generator', function() {
    const g = GraphGenerator.randomGraph(10, 0.5, GraphType.UNDIRECTED);

    this.assertEqual(g.numVertices, 10);
    this.assertTrue(g.numEdges > 0);
});

runner.test('DAG generator', function() {
    const g = GraphGenerator.dag(10, 0.3);

    this.assertEqual(g.numVertices, 10);
    this.assertFalse(g.hasCycle());

    const topo = g.topologicalSort();
    this.assertTrue(topo !== null);
});

// ============================================================================
// Visualization Tests
// ============================================================================

runner.test('ASCII visualization', function() {
    const g = new Graph(3, GraphType.UNDIRECTED);
    g.addEdge(0, 1);
    g.addEdge(1, 2);

    const ascii = g.toASCII();

    this.assertTrue(typeof ascii === 'string');
    this.assertTrue(ascii.includes('Graph:'));
    this.assertTrue(ascii.includes('Vertices: 3'));
});

// ============================================================================
// Memory Usage Tests
// ============================================================================

runner.test('Memory usage analysis', function() {
    const g = new Graph(10, GraphType.UNDIRECTED);
    for (let i = 0; i < 9; i++) {
        g.addEdge(i, i + 1);
    }

    const stats = g.memoryUsage();

    this.assertTrue('representation' in stats);
    this.assertTrue('vertices' in stats);
    this.assertTrue('edges' in stats);
    this.assertTrue('bytes' in stats);
});

// ============================================================================
// Edge Cases Tests
// ============================================================================

runner.test('Empty graph operations', function() {
    const g = new Graph(0);

    this.assertEqual(g.findConnectedComponents().length, 0);
    this.assertTrue(g.isConnected());
});

runner.test('Single vertex graph', function() {
    const g = new Graph(1);

    const components = g.findConnectedComponents();
    this.assertEqual(components.length, 1);
    this.assertEqual(components[0][0], 0);
});

runner.test('Get neighbors of vertex with no edges', function() {
    const g = new Graph(3);
    const neighbors = g.getNeighbors(0);
    this.assertEqual(neighbors.length, 0);
});

// ============================================================================
// Run Tests
// ============================================================================

runner.run().then(success => {
    process.exit(success ? 0 : 1);
});
