"""
Comprehensive unit tests for graph.py

Run with:
    python -m pytest test_graph.py -v
    or
    python test_graph.py
"""

import unittest
import sys
from graph import (
    Graph, GraphType, RepresentationType, GraphGenerator
)


class TestGraphCreation(unittest.TestCase):
    """Test graph creation and basic operations"""

    def test_create_empty_graph(self):
        """Test creating an empty graph"""
        g = Graph(0)
        self.assertEqual(g.num_vertices, 0)
        self.assertEqual(g.num_edges, 0)

    def test_create_graph_with_vertices(self):
        """Test creating a graph with initial vertices"""
        g = Graph(5)
        self.assertEqual(g.num_vertices, 5)
        self.assertEqual(g.num_edges, 0)

    def test_add_vertex(self):
        """Test adding vertices dynamically"""
        g = Graph(2)
        vertex_id = g.add_vertex()
        self.assertEqual(vertex_id, 2)
        self.assertEqual(g.num_vertices, 3)

    def test_add_edge_undirected(self):
        """Test adding edges to undirected graph"""
        g = Graph(3, GraphType.UNDIRECTED)
        g.add_edge(0, 1, 5.0)
        self.assertEqual(g.num_edges, 1)

        neighbors = g.get_neighbors(0)
        self.assertEqual(len(neighbors), 1)
        self.assertEqual(neighbors[0][0], 1)
        self.assertEqual(neighbors[0][1], 5.0)

    def test_add_edge_directed(self):
        """Test adding edges to directed graph"""
        g = Graph(3, GraphType.DIRECTED)
        g.add_edge(0, 1)
        self.assertEqual(g.num_edges, 1)

        # Check only source has the edge
        self.assertEqual(len(g.get_neighbors(0)), 1)
        self.assertEqual(len(g.get_neighbors(1)), 0)

    def test_invalid_edge(self):
        """Test adding edge with invalid vertices"""
        g = Graph(3)
        with self.assertRaises(ValueError):
            g.add_edge(0, 5)


class TestAdjacencyList(unittest.TestCase):
    """Test adjacency list representation"""

    def setUp(self):
        """Create a test graph"""
        self.g = Graph(5, GraphType.UNDIRECTED, False,
                      RepresentationType.ADJACENCY_LIST)
        self.g.add_edge(0, 1)
        self.g.add_edge(0, 4)
        self.g.add_edge(1, 2)
        self.g.add_edge(1, 3)
        self.g.add_edge(1, 4)
        self.g.add_edge(2, 3)
        self.g.add_edge(3, 4)

    def test_neighbors(self):
        """Test getting neighbors"""
        neighbors = self.g.get_neighbors(1)
        neighbor_vertices = [n[0] for n in neighbors]
        self.assertIn(0, neighbor_vertices)
        self.assertIn(2, neighbor_vertices)
        self.assertIn(3, neighbor_vertices)
        self.assertIn(4, neighbor_vertices)

    def test_edge_count(self):
        """Test edge count"""
        self.assertEqual(self.g.num_edges, 7)


class TestAdjacencyMatrix(unittest.TestCase):
    """Test adjacency matrix representation"""

    def setUp(self):
        """Create a test graph"""
        self.g = Graph(4, GraphType.DIRECTED, True,
                      RepresentationType.ADJACENCY_MATRIX)
        self.g.add_edge(0, 1, 2.5)
        self.g.add_edge(0, 2, 1.0)
        self.g.add_edge(1, 2, 3.0)
        self.g.add_edge(2, 3, 1.5)

    def test_weighted_edges(self):
        """Test weighted edges"""
        neighbors = self.g.get_neighbors(0)
        self.assertEqual(len(neighbors), 2)

        weights = {n[0]: n[1] for n in neighbors}
        self.assertEqual(weights[1], 2.5)
        self.assertEqual(weights[2], 1.0)

    def test_directed_edges(self):
        """Test directed edges"""
        # Edge 0->1 exists
        self.assertTrue(any(n[0] == 1 for n in self.g.get_neighbors(0)))
        # Edge 1->0 does not exist
        self.assertFalse(any(n[0] == 0 for n in self.g.get_neighbors(1)))


class TestEdgeList(unittest.TestCase):
    """Test edge list representation"""

    def setUp(self):
        """Create a test graph"""
        self.g = Graph(4, GraphType.UNDIRECTED, False,
                      RepresentationType.EDGE_LIST)
        self.g.add_edge(0, 1)
        self.g.add_edge(1, 2)
        self.g.add_edge(2, 3)

    def test_get_neighbors_from_edge_list(self):
        """Test getting neighbors from edge list"""
        neighbors_1 = self.g.get_neighbors(1)
        neighbor_vertices = [n[0] for n in neighbors_1]
        self.assertIn(0, neighbor_vertices)
        self.assertIn(2, neighbor_vertices)


class TestCSR(unittest.TestCase):
    """Test CSR representation"""

    def test_build_csr(self):
        """Test building CSR representation"""
        from graph import Edge

        g = Graph(4, GraphType.DIRECTED, False, RepresentationType.CSR)
        edges = [
            Edge(0, 1, 1.0),
            Edge(0, 2, 1.0),
            Edge(1, 2, 1.0),
            Edge(2, 3, 1.0)
        ]
        g.build_csr(edges)

        self.assertEqual(g.num_edges, 4)

        neighbors_0 = g.get_neighbors(0)
        self.assertEqual(len(neighbors_0), 2)


class TestDFS(unittest.TestCase):
    """Test Depth-First Search"""

    def setUp(self):
        """Create a test graph"""
        self.g = Graph(5, GraphType.UNDIRECTED)
        self.g.add_edge(0, 1)
        self.g.add_edge(0, 4)
        self.g.add_edge(1, 2)
        self.g.add_edge(1, 3)
        self.g.add_edge(1, 4)
        self.g.add_edge(2, 3)
        self.g.add_edge(3, 4)

    def test_dfs_recursive(self):
        """Test recursive DFS"""
        traversal = self.g.dfs_recursive(0)
        self.assertEqual(len(traversal), 5)
        self.assertEqual(traversal[0], 0)
        # All vertices should be visited
        self.assertEqual(set(traversal), {0, 1, 2, 3, 4})

    def test_dfs_iterative(self):
        """Test iterative DFS"""
        traversal = self.g.dfs_iterative(0)
        self.assertEqual(len(traversal), 5)
        self.assertEqual(traversal[0], 0)
        self.assertEqual(set(traversal), {0, 1, 2, 3, 4})

    def test_dfs_disconnected(self):
        """Test DFS on disconnected component"""
        g = Graph(6)
        g.add_edge(0, 1)
        g.add_edge(2, 3)

        traversal = g.dfs_recursive(0)
        self.assertEqual(set(traversal), {0, 1})


class TestBFS(unittest.TestCase):
    """Test Breadth-First Search"""

    def setUp(self):
        """Create a test graph"""
        self.g = Graph(5, GraphType.UNDIRECTED)
        self.g.add_edge(0, 1)
        self.g.add_edge(0, 4)
        self.g.add_edge(1, 2)
        self.g.add_edge(1, 3)
        self.g.add_edge(1, 4)
        self.g.add_edge(2, 3)
        self.g.add_edge(3, 4)

    def test_bfs(self):
        """Test BFS traversal"""
        traversal = self.g.bfs(0)
        self.assertEqual(len(traversal), 5)
        self.assertEqual(traversal[0], 0)

        # Check level-order property: vertices at distance 1 come before distance 2
        self.assertIn(1, traversal[:3])
        self.assertIn(4, traversal[:3])

    def test_bfs_shortest_path_property(self):
        """Test that BFS explores by levels"""
        traversal = self.g.bfs(0)
        # 0 is at position 0
        # 1 and 4 are neighbors of 0, should come early
        pos_0 = traversal.index(0)
        pos_1 = traversal.index(1)
        pos_4 = traversal.index(4)

        self.assertEqual(pos_0, 0)
        self.assertLess(pos_1, len(traversal))
        self.assertLess(pos_4, len(traversal))


class TestTopologicalSort(unittest.TestCase):
    """Test topological sorting"""

    def test_dag_topological_sort(self):
        """Test topological sort on DAG"""
        g = Graph(6, GraphType.DIRECTED)
        g.add_edge(5, 2)
        g.add_edge(5, 0)
        g.add_edge(4, 0)
        g.add_edge(4, 1)
        g.add_edge(2, 3)
        g.add_edge(3, 1)

        topo = g.topological_sort()
        self.assertIsNotNone(topo)
        self.assertEqual(len(topo), 6)

        # Check ordering property
        for i in range(len(topo)):
            for j in range(i + 1, len(topo)):
                u, v = topo[i], topo[j]
                # There should be no edge from v to u
                neighbors = g.get_neighbors(v)
                neighbor_vertices = [n[0] for n in neighbors]
                self.assertNotIn(u, neighbor_vertices)

    def test_topological_sort_dfs(self):
        """Test DFS-based topological sort"""
        g = Graph(4, GraphType.DIRECTED)
        g.add_edge(0, 1)
        g.add_edge(0, 2)
        g.add_edge(1, 2)
        g.add_edge(2, 3)

        topo = g.topological_sort_dfs()
        self.assertIsNotNone(topo)
        self.assertEqual(len(topo), 4)

    def test_cycle_detection_in_topological_sort(self):
        """Test that topological sort returns None for cyclic graphs"""
        g = Graph(3, GraphType.DIRECTED)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 0)  # Creates cycle

        topo = g.topological_sort()
        self.assertIsNone(topo)

    def test_undirected_graph_error(self):
        """Test that topological sort raises error for undirected graphs"""
        g = Graph(3, GraphType.UNDIRECTED)
        with self.assertRaises(ValueError):
            g.topological_sort()


class TestConnectedComponents(unittest.TestCase):
    """Test connected components detection"""

    def test_single_component(self):
        """Test graph with single component"""
        g = Graph(4)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 3)

        components = g.find_connected_components()
        self.assertEqual(len(components), 1)
        self.assertEqual(set(components[0]), {0, 1, 2, 3})

    def test_multiple_components(self):
        """Test graph with multiple components"""
        g = Graph(7)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(3, 4)
        g.add_edge(5, 6)

        components = g.find_connected_components()
        self.assertEqual(len(components), 3)

        component_sets = [set(c) for c in components]
        self.assertIn({0, 1, 2}, component_sets)
        self.assertIn({3, 4}, component_sets)
        self.assertIn({5, 6}, component_sets)

    def test_is_connected(self):
        """Test connectivity check"""
        g1 = Graph(3)
        g1.add_edge(0, 1)
        g1.add_edge(1, 2)
        self.assertTrue(g1.is_connected())

        g2 = Graph(4)
        g2.add_edge(0, 1)
        g2.add_edge(2, 3)
        self.assertFalse(g2.is_connected())

    def test_isolated_vertices(self):
        """Test components with isolated vertices"""
        g = Graph(5)
        g.add_edge(0, 1)

        components = g.find_connected_components()
        self.assertEqual(len(components), 4)  # {0,1}, {2}, {3}, {4}


class TestCycleDetection(unittest.TestCase):
    """Test cycle detection"""

    def test_undirected_cycle(self):
        """Test cycle detection in undirected graph"""
        g = Graph(5, GraphType.UNDIRECTED)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 4)
        g.add_edge(4, 0)  # Creates cycle

        self.assertTrue(g.has_cycle())

    def test_undirected_no_cycle(self):
        """Test no cycle in undirected tree"""
        g = Graph(4, GraphType.UNDIRECTED)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 3)

        self.assertFalse(g.has_cycle())

    def test_directed_cycle(self):
        """Test cycle detection in directed graph"""
        g = Graph(3, GraphType.DIRECTED)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 0)  # Creates cycle

        self.assertTrue(g.has_cycle())

    def test_directed_no_cycle(self):
        """Test DAG has no cycle"""
        g = Graph(4, GraphType.DIRECTED)
        g.add_edge(0, 1)
        g.add_edge(0, 2)
        g.add_edge(1, 3)
        g.add_edge(2, 3)

        self.assertFalse(g.has_cycle())

    def test_self_loop(self):
        """Test self-loop detection"""
        g = Graph(3, GraphType.DIRECTED)
        g.add_edge(0, 0)  # Self-loop

        self.assertTrue(g.has_cycle())


class TestGraphColoring(unittest.TestCase):
    """Test graph coloring algorithms"""

    def test_greedy_coloring(self):
        """Test greedy coloring"""
        g = Graph(5, GraphType.UNDIRECTED)
        g.add_edge(0, 1)
        g.add_edge(0, 2)
        g.add_edge(1, 2)
        g.add_edge(1, 3)
        g.add_edge(2, 3)
        g.add_edge(3, 4)

        coloring = g.greedy_coloring()

        # Check that all vertices are colored
        self.assertEqual(len(coloring), 5)

        # Check that no adjacent vertices have same color
        for u in range(g.num_vertices):
            for neighbor, _ in g.get_neighbors(u):
                self.assertNotEqual(coloring[u], coloring[neighbor])

    def test_chromatic_number_complete_graph(self):
        """Test chromatic number on complete graph"""
        g = GraphGenerator.complete_graph(4)
        chromatic = g.chromatic_number_upper_bound()

        # Complete graph K4 needs 4 colors
        self.assertEqual(chromatic, 4)

    def test_chromatic_number_bipartite(self):
        """Test chromatic number on bipartite graph"""
        g = Graph(4, GraphType.UNDIRECTED)
        g.add_edge(0, 2)
        g.add_edge(0, 3)
        g.add_edge(1, 2)
        g.add_edge(1, 3)

        chromatic = g.chromatic_number_upper_bound()

        # Bipartite graph needs at most 2 colors
        self.assertLessEqual(chromatic, 2)


class TestGraphGenerators(unittest.TestCase):
    """Test graph generators"""

    def test_complete_graph(self):
        """Test complete graph generator"""
        g = GraphGenerator.complete_graph(5)

        self.assertEqual(g.num_vertices, 5)
        # K5 has 10 edges (n*(n-1)/2 for undirected)
        self.assertEqual(g.num_edges, 10)

        # Every vertex should have degree 4
        for v in range(5):
            neighbors = g.get_neighbors(v)
            self.assertEqual(len(neighbors), 4)

    def test_cycle_graph(self):
        """Test cycle graph generator"""
        g = GraphGenerator.cycle_graph(6)

        self.assertEqual(g.num_vertices, 6)
        self.assertEqual(g.num_edges, 6)

        # Each vertex should have degree 2
        for v in range(6):
            neighbors = g.get_neighbors(v)
            self.assertEqual(len(neighbors), 2)

    def test_random_graph(self):
        """Test random graph generator"""
        g = GraphGenerator.random_graph(10, 0.5, GraphType.UNDIRECTED)

        self.assertEqual(g.num_vertices, 10)
        self.assertGreater(g.num_edges, 0)

    def test_dag_generator(self):
        """Test DAG generator"""
        g = GraphGenerator.dag(10, 0.3)

        self.assertEqual(g.num_vertices, 10)
        self.assertFalse(g.has_cycle())

        # Should be able to topologically sort
        topo = g.topological_sort()
        self.assertIsNotNone(topo)


class TestVisualization(unittest.TestCase):
    """Test ASCII visualization"""

    def test_to_ascii(self):
        """Test ASCII output generation"""
        g = Graph(3, GraphType.UNDIRECTED)
        g.add_edge(0, 1)
        g.add_edge(1, 2)

        ascii_output = g.to_ascii()

        self.assertIsInstance(ascii_output, str)
        self.assertIn("Graph:", ascii_output)
        self.assertIn("Vertices: 3", ascii_output)


class TestMemoryUsage(unittest.TestCase):
    """Test memory usage analysis"""

    def test_memory_usage(self):
        """Test memory usage calculation"""
        g = Graph(10, GraphType.UNDIRECTED)
        for i in range(9):
            g.add_edge(i, i + 1)

        stats = g.memory_usage()

        self.assertIn('representation', stats)
        self.assertIn('vertices', stats)
        self.assertIn('edges', stats)
        self.assertIn('bytes', stats)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""

    def test_empty_graph_operations(self):
        """Test operations on empty graph"""
        g = Graph(0)

        self.assertEqual(g.find_connected_components(), [])
        self.assertTrue(g.is_connected())

    def test_single_vertex(self):
        """Test graph with single vertex"""
        g = Graph(1)

        components = g.find_connected_components()
        self.assertEqual(len(components), 1)
        self.assertEqual(components[0], [0])

    def test_get_neighbors_invalid_vertex(self):
        """Test getting neighbors of non-existent vertex"""
        g = Graph(3)
        # Should return empty list for vertex with no edges
        neighbors = g.get_neighbors(0)
        self.assertEqual(len(neighbors), 0)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
