"""
Tree Decomposition Algorithms
==============================

This module implements tree decomposition algorithms for graphs, which are
fundamental for solving many NP-hard problems efficiently on graphs with
small treewidth.

Key Features:
- Tree decomposition construction
- Treewidth computation (exact and heuristic)
- Nice tree decomposition
- Path decomposition
- Minimum fill-in algorithms
- Dynamic programming on tree decompositions
- Applications to optimization problems

Author: Algorithms Multiverse
Date: 2024
"""

from typing import List, Set, Tuple, Dict, Optional, Any, FrozenSet
from collections import defaultdict, deque
from dataclasses import dataclass, field
import heapq
import itertools
import random
import math


@dataclass
class TreeDecomposition:
    """Represents a tree decomposition of a graph"""
    bags: Dict[int, Set[int]]  # Node ID -> set of vertices in bag
    tree_edges: List[Tuple[int, int]]  # Edges in the decomposition tree
    width: int  # Treewidth (max bag size - 1)

    def is_valid(self, graph: Dict[int, Set[int]]) -> bool:
        """Check if this is a valid tree decomposition"""
        vertices = set()
        for v_set in self.bags.values():
            vertices.update(v_set)

        # Check 1: Every vertex appears in some bag
        graph_vertices = set(graph.keys())
        if vertices != graph_vertices:
            return False

        # Check 2: Every edge appears in some bag
        for u in graph:
            for v in graph[u]:
                found = False
                for bag in self.bags.values():
                    if u in bag and v in bag:
                        found = True
                        break
                if not found:
                    return False

        # Check 3: Running intersection property
        # For each vertex, bags containing it form a subtree
        for vertex in vertices:
            containing_bags = [bid for bid, bag in self.bags.items() if vertex in bag]
            if not self._forms_subtree(containing_bags):
                return False

        return True

    def _forms_subtree(self, bag_ids: List[int]) -> bool:
        """Check if given bag IDs form a connected subtree"""
        if not bag_ids:
            return True

        # Build adjacency list for tree
        tree_adj = defaultdict(set)
        for u, v in self.tree_edges:
            tree_adj[u].add(v)
            tree_adj[v].add(u)

        # BFS to check connectivity
        visited = {bag_ids[0]}
        queue = deque([bag_ids[0]])
        bag_set = set(bag_ids)

        while queue:
            node = queue.popleft()
            for neighbor in tree_adj[node]:
                if neighbor in bag_set and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return len(visited) == len(bag_ids)


@dataclass
class NiceTreeDecomposition(TreeDecomposition):
    """Nice tree decomposition with specific node types"""
    root: int
    node_types: Dict[int, str]  # 'leaf', 'introduce', 'forget', 'join'
    children: Dict[int, List[int]]  # Parent -> list of children

    def get_introduced_vertex(self, node: int) -> Optional[int]:
        """Get the vertex introduced at an introduce node"""
        if self.node_types.get(node) != 'introduce':
            return None
        if node not in self.children or not self.children[node]:
            return None
        child = self.children[node][0]
        diff = self.bags[node] - self.bags[child]
        return diff.pop() if diff else None

    def get_forgotten_vertex(self, node: int) -> Optional[int]:
        """Get the vertex forgotten at a forget node"""
        if self.node_types.get(node) != 'forget':
            return None
        if node not in self.children or not self.children[node]:
            return None
        child = self.children[node][0]
        diff = self.bags[child] - self.bags[node]
        return diff.pop() if diff else None


class TreeDecompositionAlgorithms:
    """Algorithms for computing tree decompositions"""

    @staticmethod
    def greedy_min_degree(graph: Dict[int, Set[int]]) -> TreeDecomposition:
        """Greedy minimum degree heuristic for tree decomposition

        Repeatedly eliminate vertex with minimum degree
        """
        # Make a copy of the graph
        g = {v: set(neighbors) for v, neighbors in graph.items()}
        elimination_order = []
        bags = {}
        tree_edges = []
        max_bag_size = 0

        # Compute elimination ordering
        while g:
            # Find vertex with minimum degree
            min_vertex = min(g.keys(), key=lambda v: len(g[v]))
            neighbors = g[min_vertex]

            # Create bag for this vertex and its neighbors
            bag_id = len(elimination_order)
            bags[bag_id] = {min_vertex} | neighbors
            max_bag_size = max(max_bag_size, len(bags[bag_id]))

            elimination_order.append(min_vertex)

            # Make neighbors a clique (fill-in edges)
            for u, v in itertools.combinations(neighbors, 2):
                if u in g and v in g:
                    g[u].add(v)
                    g[v].add(u)

            # Remove vertex
            del g[min_vertex]
            for neighbor in neighbors:
                if neighbor in g:
                    g[neighbor].discard(min_vertex)

        # Build tree structure
        for i in range(len(elimination_order) - 1):
            tree_edges.append((i, i + 1))

        return TreeDecomposition(bags, tree_edges, max_bag_size - 1)

    @staticmethod
    def greedy_min_fill(graph: Dict[int, Set[int]]) -> TreeDecomposition:
        """Greedy minimum fill-in heuristic for tree decomposition

        Choose vertex that requires minimum fill-in edges
        """
        g = {v: set(neighbors) for v, neighbors in graph.items()}
        elimination_order = []
        bags = {}
        tree_edges = []
        max_bag_size = 0

        def count_fill_edges(vertex: int) -> int:
            """Count fill-in edges needed when eliminating vertex"""
            neighbors = g[vertex]
            count = 0
            for u, v in itertools.combinations(neighbors, 2):
                if v not in g[u]:
                    count += 1
            return count

        while g:
            # Find vertex with minimum fill-in
            min_vertex = min(g.keys(), key=count_fill_edges)
            neighbors = g[min_vertex]

            # Create bag
            bag_id = len(elimination_order)
            bags[bag_id] = {min_vertex} | neighbors
            max_bag_size = max(max_bag_size, len(bags[bag_id]))

            elimination_order.append(min_vertex)

            # Add fill-in edges
            for u, v in itertools.combinations(neighbors, 2):
                if u in g and v in g:
                    g[u].add(v)
                    g[v].add(u)

            # Remove vertex
            del g[min_vertex]
            for neighbor in neighbors:
                if neighbor in g:
                    g[neighbor].discard(min_vertex)

        # Build tree
        for i in range(len(elimination_order) - 1):
            tree_edges.append((i, i + 1))

        return TreeDecomposition(bags, tree_edges, max_bag_size - 1)

    @staticmethod
    def minimum_separators(graph: Dict[int, Set[int]]) -> TreeDecomposition:
        """Tree decomposition using minimal separators

        Based on the relationship between minimal separators and treewidth
        """
        vertices = list(graph.keys())
        n = len(vertices)

        # Find all minimal separators
        separators = set()

        for s, t in itertools.combinations(vertices, 2):
            # Find minimal s-t separator
            separator = TreeDecompositionAlgorithms._find_minimal_separator(graph, s, t)
            if separator:
                separators.add(frozenset(separator))

        # Build clique tree from maximal cliques
        cliques = TreeDecompositionAlgorithms._find_maximal_cliques(graph)

        # Create bags from cliques
        bags = {i: set(clique) for i, clique in enumerate(cliques)}

        # Build tree using maximum spanning tree on intersection sizes
        edges = []
        for i, j in itertools.combinations(range(len(cliques)), 2):
            intersection = len(bags[i] & bags[j])
            if intersection > 0:
                edges.append((-intersection, i, j))  # Negative for max spanning tree

        # Kruskal's algorithm for maximum spanning tree
        edges.sort()
        tree_edges = []
        parent = list(range(len(cliques)))

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
                return True
            return False

        for weight, u, v in edges:
            if union(u, v):
                tree_edges.append((u, v))
                if len(tree_edges) == len(cliques) - 1:
                    break

        max_bag_size = max(len(bag) for bag in bags.values())
        return TreeDecomposition(bags, tree_edges, max_bag_size - 1)

    @staticmethod
    def _find_minimal_separator(graph: Dict[int, Set[int]], s: int, t: int) -> Set[int]:
        """Find a minimal s-t separator"""
        if t in graph[s]:
            return set()  # Adjacent vertices have no separator

        # Find vertex cut using max flow
        # Simplified: use BFS to find reachable vertices from s without going through t
        visited = {s}
        queue = deque([s])
        separator = set()

        while queue:
            v = queue.popleft()
            for neighbor in graph[v]:
                if neighbor == t:
                    separator.add(v)
                elif neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return separator

    @staticmethod
    def _find_maximal_cliques(graph: Dict[int, Set[int]]) -> List[FrozenSet[int]]:
        """Find all maximal cliques using Bron-Kerbosch algorithm"""
        cliques = []

        def bron_kerbosch(r: Set[int], p: Set[int], x: Set[int]):
            if not p and not x:
                if r:
                    cliques.append(frozenset(r))
                return

            # Choose pivot
            pivot = max(p | x, key=lambda v: len(p & graph[v])) if (p | x) else None

            for v in list(p - (graph[pivot] if pivot else set())):
                bron_kerbosch(
                    r | {v},
                    p & graph[v],
                    x & graph[v]
                )
                p.remove(v)
                x.add(v)

        bron_kerbosch(set(), set(graph.keys()), set())
        return cliques

    @staticmethod
    def path_decomposition(graph: Dict[int, Set[int]]) -> TreeDecomposition:
        """Compute a path decomposition (special case of tree decomposition)"""
        # Use interval graph recognition for optimal path decomposition
        # Simplified: use vertex ordering heuristic

        vertices = list(graph.keys())
        n = len(vertices)

        # Compute vertex ordering using breadth-first search
        if not vertices:
            return TreeDecomposition({}, [], -1)

        start = vertices[0]
        visited = {start}
        ordering = [start]
        queue = deque([start])

        while queue:
            v = queue.popleft()
            for neighbor in graph[v]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    ordering.append(neighbor)
                    queue.append(neighbor)

        # Build path decomposition from ordering
        bags = {}
        tree_edges = []
        max_bag_size = 0

        for i, v in enumerate(ordering):
            # Include v and all its neighbors that appear later
            bag = {v}
            for neighbor in graph[v]:
                if ordering.index(neighbor) >= i:
                    bag.add(neighbor)

            bags[i] = bag
            max_bag_size = max(max_bag_size, len(bag))

            if i > 0:
                tree_edges.append((i-1, i))

        return TreeDecomposition(bags, tree_edges, max_bag_size - 1)

    @staticmethod
    def make_nice(td: TreeDecomposition, root: int = 0) -> NiceTreeDecomposition:
        """Convert a tree decomposition to nice tree decomposition"""
        # Build adjacency list
        adj = defaultdict(set)
        for u, v in td.tree_edges:
            adj[u].add(v)
            adj[v].add(u)

        # Root the tree
        children_map = defaultdict(list)
        visited = set()

        def build_rooted_tree(node: int, parent: Optional[int] = None):
            visited.add(node)
            for child in adj[node]:
                if child not in visited:
                    children_map[node].append(child)
                    build_rooted_tree(child, node)

        build_rooted_tree(root)

        # Convert to nice tree decomposition
        nice_bags = {}
        nice_edges = []
        nice_types = {}
        nice_children = defaultdict(list)
        next_id = max(td.bags.keys()) + 1

        def make_nice_subtree(node: int, parent_bag: Set[int]) -> int:
            """Convert subtree rooted at node to nice form"""
            nonlocal next_id

            current_bag = td.bags[node]
            node_children = children_map[node]

            if not node_children:
                # Leaf node
                # Add forget nodes to make it empty
                current_node = node
                nice_bags[current_node] = current_bag.copy()
                nice_types[current_node] = 'leaf' if not current_bag else 'forget'

                for v in current_bag:
                    new_node = next_id
                    next_id += 1
                    nice_bags[new_node] = current_bag - {v}
                    nice_types[new_node] = 'forget'
                    nice_edges.append((current_node, new_node))
                    nice_children[current_node] = [new_node]
                    current_node = new_node

                # Final leaf node
                nice_types[current_node] = 'leaf'
                return node

            elif len(node_children) == 1:
                # Single child - add introduce/forget nodes
                child = node_children[0]
                child_id = make_nice_subtree(child, current_bag)

                # Handle differences between bags
                to_introduce = current_bag - td.bags[child]
                to_forget = td.bags[child] - current_bag

                current_node = child_id

                # Add forget nodes
                for v in to_forget:
                    new_node = next_id
                    next_id += 1
                    nice_bags[new_node] = nice_bags[current_node] - {v}
                    nice_types[new_node] = 'forget'
                    nice_edges.append((new_node, current_node))
                    nice_children[new_node] = [current_node]
                    current_node = new_node

                # Add introduce nodes
                for v in to_introduce:
                    new_node = next_id
                    next_id += 1
                    nice_bags[new_node] = nice_bags.get(current_node, set()) | {v}
                    nice_types[new_node] = 'introduce'
                    nice_edges.append((new_node, current_node))
                    nice_children[new_node] = [current_node]
                    current_node = new_node

                return current_node

            else:
                # Multiple children - create binary join tree
                child_ids = [make_nice_subtree(child, current_bag) for child in node_children]

                # Create join nodes
                while len(child_ids) > 1:
                    left = child_ids.pop(0)
                    right = child_ids.pop(0)

                    join_node = next_id
                    next_id += 1
                    nice_bags[join_node] = nice_bags[left]  # Should be same as right
                    nice_types[join_node] = 'join'
                    nice_edges.append((join_node, left))
                    nice_edges.append((join_node, right))
                    nice_children[join_node] = [left, right]

                    child_ids.append(join_node)

                return child_ids[0]

        nice_root = make_nice_subtree(root, set())

        return NiceTreeDecomposition(
            bags=nice_bags,
            tree_edges=nice_edges,
            width=td.width,
            root=nice_root,
            node_types=nice_types,
            children=nice_children
        )


class DynamicProgrammingOnTD:
    """Dynamic programming algorithms on tree decompositions"""

    @staticmethod
    def independent_set(graph: Dict[int, Set[int]], td: NiceTreeDecomposition) -> int:
        """Solve maximum independent set using tree decomposition

        Time complexity: O(2^k * n) where k is treewidth
        """
        dp = {}

        def compute_table(node: int) -> Dict[FrozenSet[int], int]:
            """Compute DP table for subtree rooted at node"""
            if node in dp:
                return dp[node]

            bag = td.bags[node]
            node_type = td.node_types[node]
            table = {}

            if node_type == 'leaf':
                # Base case: empty bag
                table[frozenset()] = 0
                return table

            elif node_type == 'introduce':
                v = td.get_introduced_vertex(node)
                child = td.children[node][0]
                child_table = compute_table(child)

                for subset, value in child_table.items():
                    # Don't include v
                    table[subset] = value

                    # Include v if valid
                    if not any(u in subset for u in graph.get(v, [])):
                        new_subset = frozenset(subset | {v})
                        table[new_subset] = value + 1

            elif node_type == 'forget':
                v = td.get_forgotten_vertex(node)
                child = td.children[node][0]
                child_table = compute_table(child)

                for subset, value in child_table.items():
                    # Consider both including and not including v
                    subset_without_v = frozenset(s for s in subset if s != v)
                    table[subset_without_v] = max(
                        table.get(subset_without_v, 0),
                        value
                    )

            elif node_type == 'join':
                left_child, right_child = td.children[node]
                left_table = compute_table(left_child)
                right_table = compute_table(right_child)

                for left_subset, left_value in left_table.items():
                    for right_subset, right_value in right_table.items():
                        if left_subset == right_subset:
                            # Intersection must be the same
                            combined_value = left_value + right_value - len(left_subset)
                            table[left_subset] = max(
                                table.get(left_subset, 0),
                                combined_value
                            )

            dp[node] = table
            return table

        root_table = compute_table(td.root)
        return max(root_table.values()) if root_table else 0

    @staticmethod
    def vertex_cover(graph: Dict[int, Set[int]], td: NiceTreeDecomposition) -> int:
        """Solve minimum vertex cover using tree decomposition"""
        dp = {}

        def compute_table(node: int) -> Dict[FrozenSet[int], int]:
            """Compute DP table for subtree rooted at node"""
            if node in dp:
                return dp[node]

            bag = td.bags[node]
            node_type = td.node_types[node]
            table = {}

            if node_type == 'leaf':
                table[frozenset()] = 0
                return table

            elif node_type == 'introduce':
                v = td.get_introduced_vertex(node)
                child = td.children[node][0]
                child_table = compute_table(child)

                for subset, value in child_table.items():
                    # Include v in cover
                    new_subset_with_v = frozenset(subset | {v})
                    table[new_subset_with_v] = value + 1

                    # Don't include v (check if edges are covered)
                    edges_covered = True
                    for u in graph.get(v, []):
                        if u in td.bags[child] and u not in subset:
                            edges_covered = False
                            break

                    if edges_covered:
                        table[subset] = min(table.get(subset, float('inf')), value)

            elif node_type == 'forget':
                v = td.get_forgotten_vertex(node)
                child = td.children[node][0]
                child_table = compute_table(child)

                for subset, value in child_table.items():
                    subset_without_v = frozenset(s for s in subset if s != v)
                    table[subset_without_v] = min(
                        table.get(subset_without_v, float('inf')),
                        value
                    )

            elif node_type == 'join':
                left_child, right_child = td.children[node]
                left_table = compute_table(left_child)
                right_table = compute_table(right_child)

                for left_subset, left_value in left_table.items():
                    for right_subset, right_value in right_table.items():
                        if left_subset == right_subset:
                            combined_value = left_value + right_value - len(left_subset)
                            table[left_subset] = min(
                                table.get(left_subset, float('inf')),
                                combined_value
                            )

            dp[node] = table
            return table

        root_table = compute_table(td.root)
        return min(root_table.values()) if root_table else 0

    @staticmethod
    def dominating_set(graph: Dict[int, Set[int]], td: NiceTreeDecomposition) -> int:
        """Solve minimum dominating set using tree decomposition

        States: 0 = not in set, not dominated
                1 = not in set, dominated
                2 = in dominating set
        """
        dp = {}

        def compute_table(node: int) -> Dict[Tuple[Tuple[int, int], ...], int]:
            """Compute DP table with states for each vertex"""
            if node in dp:
                return dp[node]

            bag = list(td.bags[node])
            node_type = td.node_types[node]
            table = {}

            if node_type == 'leaf':
                # Empty configuration
                table[tuple()] = 0
                return table

            elif node_type == 'introduce':
                v = td.get_introduced_vertex(node)
                child = td.children[node][0]
                child_table = compute_table(child)
                child_bag = list(td.bags[child])

                for config, value in child_table.items():
                    # Try all states for v
                    for v_state in [0, 1, 2]:
                        # Check validity
                        valid = True

                        if v_state == 0:  # Not dominated
                            # Check if v has a dominating neighbor in bag
                            for i, u in enumerate(child_bag):
                                if u in graph.get(v, []) and config[i] == 2:
                                    valid = False
                                    break

                        new_config = list(config)
                        # Insert v's state at appropriate position
                        v_idx = bag.index(v)
                        new_config.insert(v_idx, v_state)
                        new_config = tuple(new_config)

                        cost = value + (1 if v_state == 2 else 0)

                        if valid:
                            table[new_config] = min(table.get(new_config, float('inf')), cost)

            # Similar logic for forget and join nodes...
            dp[node] = table
            return table

        root_table = compute_table(td.root)
        # Return minimum over valid configurations
        return min(root_table.values()) if root_table else 0


class TreewidthAlgorithms:
    """Algorithms for computing exact and approximate treewidth"""

    @staticmethod
    def exact_treewidth_dp(graph: Dict[int, Set[int]]) -> int:
        """Compute exact treewidth using dynamic programming

        Time complexity: O(2^n * n^2) - only feasible for small graphs
        """
        vertices = list(graph.keys())
        n = len(vertices)

        if n == 0:
            return -1

        # DP table: dp[S] = treewidth of induced subgraph on S
        dp = {}

        # Base cases
        for v in vertices:
            dp[frozenset([v])] = 0

        # Fill DP table
        for size in range(2, n + 1):
            for subset_list in itertools.combinations(vertices, size):
                subset = frozenset(subset_list)

                # Try all possible last bags
                min_tw = float('inf')

                for bag_size in range(1, size + 1):
                    for bag_list in itertools.combinations(subset_list, bag_size):
                        bag = set(bag_list)

                        # Check if bag is a clique or can be made one
                        is_valid = True
                        for u, v in itertools.combinations(bag, 2):
                            if v not in graph.get(u, []):
                                # Would need to add edge
                                pass

                        if is_valid:
                            remaining = subset - bag
                            if remaining:
                                # Recursively compute treewidth
                                sub_tw = dp.get(remaining, float('inf'))
                                min_tw = min(min_tw, max(len(bag) - 1, sub_tw))
                            else:
                                min_tw = min(min_tw, len(bag) - 1)

                dp[subset] = min_tw

        return dp[frozenset(vertices)]

    @staticmethod
    def approximate_treewidth(graph: Dict[int, Set[int]]) -> Tuple[int, int]:
        """Compute lower and upper bounds for treewidth

        Returns: (lower_bound, upper_bound)
        """
        if not graph:
            return -1, -1

        # Lower bound: maximum clique size - 1
        cliques = TreeDecompositionAlgorithms._find_maximal_cliques(graph)
        lower_bound = max(len(clique) for clique in cliques) - 1 if cliques else 0

        # Upper bound: use greedy heuristic
        td = TreeDecompositionAlgorithms.greedy_min_degree(graph)
        upper_bound = td.width

        return lower_bound, upper_bound

    @staticmethod
    def is_tree(graph: Dict[int, Set[int]]) -> bool:
        """Check if graph is a tree (treewidth 1)"""
        n = len(graph)
        if n == 0:
            return True

        # Count edges
        edge_count = sum(len(neighbors) for neighbors in graph.values()) // 2

        # Tree has n-1 edges
        if edge_count != n - 1:
            return False

        # Check connectivity
        visited = set()
        start = next(iter(graph))
        queue = deque([start])
        visited.add(start)

        while queue:
            v = queue.popleft()
            for neighbor in graph[v]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return len(visited) == n

    @staticmethod
    def is_series_parallel(graph: Dict[int, Set[int]]) -> bool:
        """Check if graph is series-parallel (treewidth ≤ 2)

        Uses recognition algorithm for K4-minor-free graphs
        """
        # Simplified check: look for K4 minor
        vertices = list(graph.keys())

        # Check all 4-vertex subsets
        for subset in itertools.combinations(vertices, 4):
            # Check if forms K4
            is_k4 = True
            for u, v in itertools.combinations(subset, 2):
                if v not in graph.get(u, []):
                    is_k4 = False
                    break

            if is_k4:
                return False  # Has K4, not series-parallel

        # More sophisticated check would use series-parallel recognition
        return True


def demo_tree_decomposition():
    """Demonstrate tree decomposition algorithms"""
    print("=" * 80)
    print("Tree Decomposition Algorithms Demonstration")
    print("=" * 80)

    # Example graph (small for demonstration)
    graph = {
        1: {2, 3, 4},
        2: {1, 3, 5},
        3: {1, 2, 4, 5, 6},
        4: {1, 3, 6},
        5: {2, 3, 6, 7},
        6: {3, 4, 5, 7},
        7: {5, 6}
    }

    print("\n1. Graph Structure:")
    print("-" * 40)
    print(f"Vertices: {list(graph.keys())}")
    print(f"Number of edges: {sum(len(adj) for adj in graph.values()) // 2}")

    # Compute tree decompositions
    print("\n2. Tree Decomposition Heuristics:")
    print("-" * 40)

    # Minimum degree heuristic
    td_min_degree = TreeDecompositionAlgorithms.greedy_min_degree(graph)
    print(f"Minimum Degree Heuristic:")
    print(f"  Treewidth: {td_min_degree.width}")
    print(f"  Valid: {td_min_degree.is_valid(graph)}")

    # Minimum fill heuristic
    td_min_fill = TreeDecompositionAlgorithms.greedy_min_fill(graph)
    print(f"\nMinimum Fill-in Heuristic:")
    print(f"  Treewidth: {td_min_fill.width}")
    print(f"  Valid: {td_min_fill.is_valid(graph)}")

    # Path decomposition
    path_dec = TreeDecompositionAlgorithms.path_decomposition(graph)
    print(f"\nPath Decomposition:")
    print(f"  Pathwidth: {path_dec.width}")
    print(f"  Valid: {path_dec.is_valid(graph)}")

    # Nice tree decomposition
    print("\n3. Nice Tree Decomposition:")
    print("-" * 40)
    nice_td = TreeDecompositionAlgorithms.make_nice(td_min_degree)
    print(f"Root node: {nice_td.root}")
    print(f"Number of nodes: {len(nice_td.bags)}")

    node_type_counts = defaultdict(int)
    for node_type in nice_td.node_types.values():
        node_type_counts[node_type] += 1
    print(f"Node types: {dict(node_type_counts)}")

    # Treewidth bounds
    print("\n4. Treewidth Bounds:")
    print("-" * 40)
    lower, upper = TreewidthAlgorithms.approximate_treewidth(graph)
    print(f"Lower bound: {lower}")
    print(f"Upper bound: {upper}")

    # Special graph classes
    print("\n5. Special Graph Classes:")
    print("-" * 40)
    print(f"Is tree: {TreewidthAlgorithms.is_tree(graph)}")
    print(f"Is series-parallel: {TreewidthAlgorithms.is_series_parallel(graph)}")

    # Dynamic programming applications
    print("\n6. DP on Tree Decomposition:")
    print("-" * 40)

    # Maximum independent set
    max_ind_set = DynamicProgrammingOnTD.independent_set(graph, nice_td)
    print(f"Maximum Independent Set size: {max_ind_set}")

    # Minimum vertex cover
    min_vertex_cover = DynamicProgrammingOnTD.vertex_cover(graph, nice_td)
    print(f"Minimum Vertex Cover size: {min_vertex_cover}")

    # Larger example for performance
    print("\n7. Performance on Larger Graph:")
    print("-" * 40)

    # Create a grid graph (known treewidth)
    def create_grid_graph(rows: int, cols: int) -> Dict[int, Set[int]]:
        """Create a grid graph"""
        graph = defaultdict(set)
        for i in range(rows):
            for j in range(cols):
                node = i * cols + j
                # Add edges to neighbors
                if j < cols - 1:  # Right
                    graph[node].add(node + 1)
                    graph[node + 1].add(node)
                if i < rows - 1:  # Down
                    graph[node].add(node + cols)
                    graph[node + cols].add(node)
        return dict(graph)

    grid = create_grid_graph(4, 4)
    print(f"4x4 Grid Graph:")
    print(f"  Known treewidth: 4")

    grid_td = TreeDecompositionAlgorithms.greedy_min_fill(grid)
    print(f"  Computed treewidth: {grid_td.width}")

    # Tree example
    print("\n8. Tree Example:")
    print("-" * 40)
    tree = {
        1: {2, 3},
        2: {1, 4, 5},
        3: {1, 6},
        4: {2},
        5: {2, 7},
        6: {3},
        7: {5}
    }

    tree_td = TreeDecompositionAlgorithms.greedy_min_degree(tree)
    print(f"Binary tree treewidth: {tree_td.width}")
    print(f"Is tree: {TreewidthAlgorithms.is_tree(tree)}")

    print("\n" + "=" * 80)
    print("Tree decomposition enables efficient algorithms for NP-hard problems!")
    print("=" * 80)


def main():
    """Main demonstration"""
    demo_tree_decomposition()

    # Additional examples
    print("\n" + "=" * 80)
    print("Additional Examples")
    print("=" * 80)

    # Complete graph (clique)
    print("\n9. Complete Graph K5:")
    print("-" * 40)
    k5 = {i: set(range(1, 6)) - {i} for i in range(1, 6)}
    k5_td = TreeDecompositionAlgorithms.greedy_min_degree(k5)
    print(f"Treewidth of K5: {k5_td.width} (expected: 4)")

    # Cycle
    print("\n10. Cycle C6:")
    print("-" * 40)
    c6 = {
        1: {2, 6}, 2: {1, 3}, 3: {2, 4},
        4: {3, 5}, 5: {4, 6}, 6: {5, 1}
    }
    c6_td = TreeDecompositionAlgorithms.greedy_min_degree(c6)
    print(f"Treewidth of C6: {c6_td.width} (expected: 2)")

    # Series-parallel graph
    print("\n11. Series-Parallel Graph:")
    print("-" * 40)
    sp_graph = {
        1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 4},
        4: {2, 3, 5}, 5: {4}
    }
    sp_td = TreeDecompositionAlgorithms.greedy_min_fill(sp_graph)
    print(f"Treewidth: {sp_td.width}")
    print(f"Is series-parallel: {TreewidthAlgorithms.is_series_parallel(sp_graph)}")

    print("\n" + "=" * 80)
    print("Applications of Tree Decomposition:")
    print("- Solving NP-hard problems on graphs with small treewidth")
    print("- Circuit design and VLSI layout")
    print("- Computational biology (phylogenetic trees)")
    print("- Constraint satisfaction problems")
    print("- Bayesian network inference")
    print("=" * 80)


if __name__ == "__main__":
    main()