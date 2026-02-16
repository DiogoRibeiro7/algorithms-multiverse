#!/usr/bin/env python3
"""
Hungarian Algorithm (Kuhn-Munkres Algorithm) Implementation

The Hungarian algorithm solves the assignment problem in polynomial time.
Given a cost matrix, it finds the assignment that minimizes total cost.

Applications:
- Job assignment to workers
- Task scheduling
- Resource allocation
- Bipartite matching with weights

Author: Algorithms Multiverse
License: MIT
"""

import numpy as np
from typing import List, Tuple, Optional, Set
import sys


class HungarianAlgorithm:
    """
    Hungarian Algorithm for solving the assignment problem.

    Finds minimum cost assignment in a bipartite graph.

    Time Complexity: O(n³) where n is the size of the matrix
    Space Complexity: O(n²)
    """

    def __init__(self, cost_matrix: List[List[float]], maximize: bool = False):
        """
        Initialize Hungarian algorithm.

        Args:
            cost_matrix: Cost matrix (square or rectangular)
            maximize: If True, finds maximum assignment instead of minimum
        """
        self.original_matrix = np.array(cost_matrix, dtype=float)
        self.maximize = maximize

        # Handle maximization by negating the matrix
        if maximize:
            self.cost_matrix = -self.original_matrix
        else:
            self.cost_matrix = self.original_matrix.copy()

        # Make matrix square if necessary
        self.n_rows, self.n_cols = self.cost_matrix.shape
        self.size = max(self.n_rows, self.n_cols)

        if self.n_rows != self.n_cols:
            self.cost_matrix = self._make_square(self.cost_matrix)

        # Initialize variables
        self.marked_rows = set()
        self.marked_cols = set()
        self.assignments = np.zeros((self.size, self.size), dtype=bool)

    def _make_square(self, matrix: np.ndarray) -> np.ndarray:
        """
        Make matrix square by padding with zeros.

        Args:
            matrix: Input matrix

        Returns:
            Square matrix
        """
        padded = np.zeros((self.size, self.size))
        padded[:self.n_rows, :self.n_cols] = matrix

        # Use large value for padding (not infinity to avoid numerical issues)
        max_val = np.max(np.abs(matrix)) * 10
        padded[self.n_rows:, :] = max_val
        padded[:, self.n_cols:] = max_val

        return padded

    def solve(self) -> Tuple[List[Tuple[int, int]], float]:
        """
        Solve the assignment problem.

        Returns:
            (assignments, total_cost) where assignments is list of (row, col) pairs
        """
        # Step 1: Subtract row minimums
        self._subtract_row_minimums()

        # Step 2: Subtract column minimums
        self._subtract_col_minimums()

        # Main loop
        iteration = 0
        max_iterations = self.size * 10  # Prevent infinite loops

        while iteration < max_iterations:
            # Step 3: Cover zeros with minimum lines
            self._find_zero_assignments()

            # Check if we have a complete assignment
            if self._is_complete_assignment():
                break

            # Step 4: Create additional zeros
            self._create_additional_zeros()

            iteration += 1

        if iteration >= max_iterations:
            raise RuntimeError("Hungarian algorithm did not converge")

        # Extract solution
        return self._extract_solution()

    def _subtract_row_minimums(self):
        """Subtract the minimum value from each row."""
        for i in range(self.size):
            min_val = np.min(self.cost_matrix[i, :])
            if min_val != float('inf'):
                self.cost_matrix[i, :] -= min_val

    def _subtract_col_minimums(self):
        """Subtract the minimum value from each column."""
        for j in range(self.size):
            min_val = np.min(self.cost_matrix[:, j])
            if min_val != float('inf'):
                self.cost_matrix[:, j] -= min_val

    def _find_zero_assignments(self):
        """Find optimal assignment of zeros."""
        self.assignments = np.zeros((self.size, self.size), dtype=bool)

        # Find zeros in the matrix
        zero_positions = np.argwhere(self.cost_matrix == 0)

        # Sort by number of zeros in row and column (ascending)
        # This helps find independent zeros more efficiently
        zero_counts = []
        for pos in zero_positions:
            row_zeros = np.sum(self.cost_matrix[pos[0], :] == 0)
            col_zeros = np.sum(self.cost_matrix[:, pos[1]] == 0)
            zero_counts.append((row_zeros + col_zeros, pos))

        zero_counts.sort(key=lambda x: x[0])

        assigned_rows = set()
        assigned_cols = set()

        # Assign zeros
        for _, pos in zero_counts:
            i, j = pos
            if i not in assigned_rows and j not in assigned_cols:
                self.assignments[i, j] = True
                assigned_rows.add(i)
                assigned_cols.add(j)

    def _is_complete_assignment(self) -> bool:
        """Check if we have a complete assignment."""
        return np.sum(self.assignments) == self.size

    def _cover_zeros(self) -> Tuple[Set[int], Set[int]]:
        """
        Find minimum number of lines to cover all zeros.

        Returns:
            (covered_rows, covered_cols) sets
        """
        # This uses König's theorem: minimum vertex cover in bipartite graph
        # equals maximum matching

        # Find unassigned zeros
        zero_positions = np.argwhere(self.cost_matrix == 0)

        # Build bipartite graph of zeros
        marked_rows = set()
        marked_cols = set()

        # Start with unassigned rows
        unassigned_rows = set(range(self.size))
        for i in range(self.size):
            for j in range(self.size):
                if self.assignments[i, j]:
                    unassigned_rows.discard(i)

        # Mark rows and columns using alternating paths
        changed = True
        while changed:
            changed = False

            # Mark columns with zeros in marked rows
            for i in marked_rows | unassigned_rows:
                for j in range(self.size):
                    if self.cost_matrix[i, j] == 0 and j not in marked_cols:
                        marked_cols.add(j)
                        changed = True

            # Mark rows with assignments in marked columns
            for j in marked_cols:
                for i in range(self.size):
                    if self.assignments[i, j] and i not in marked_rows:
                        marked_rows.add(i)
                        changed = True

        # Covered lines are unmarked rows and marked columns
        covered_rows = set(range(self.size)) - (marked_rows | unassigned_rows)
        covered_cols = marked_cols

        return covered_rows, covered_cols

    def _create_additional_zeros(self):
        """Create additional zeros by manipulating the matrix."""
        covered_rows, covered_cols = self._cover_zeros()

        # Find minimum uncovered value
        min_val = float('inf')
        for i in range(self.size):
            if i in covered_rows:
                continue
            for j in range(self.size):
                if j in covered_cols:
                    continue
                if self.cost_matrix[i, j] < min_val:
                    min_val = self.cost_matrix[i, j]

        if min_val == float('inf'):
            return

        # Subtract from uncovered, add to double-covered
        for i in range(self.size):
            for j in range(self.size):
                if i not in covered_rows and j not in covered_cols:
                    # Uncovered: subtract minimum
                    self.cost_matrix[i, j] -= min_val
                elif i in covered_rows and j in covered_cols:
                    # Double-covered: add minimum
                    self.cost_matrix[i, j] += min_val

    def _extract_solution(self) -> Tuple[List[Tuple[int, int]], float]:
        """Extract the final solution."""
        assignments = []
        total_cost = 0

        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.assignments[i, j]:
                    assignments.append((i, j))
                    if self.maximize:
                        total_cost += -self.original_matrix[i, j]
                    else:
                        total_cost += self.original_matrix[i, j]

        return assignments, total_cost


class HungarianSolver:
    """
    Alternative implementation using the Munkres variant.
    More efficient for sparse matrices.
    """

    def __init__(self):
        """Initialize Hungarian solver."""
        pass

    def solve_assignment(self,
                        cost_matrix: List[List[float]],
                        maximize: bool = False) -> Tuple[List[Tuple[int, int]], float]:
        """
        Solve assignment problem using Hungarian method.

        Args:
            cost_matrix: Cost matrix
            maximize: Whether to maximize instead of minimize

        Returns:
            (assignments, total_cost) tuple
        """
        n = len(cost_matrix)
        m = len(cost_matrix[0]) if n > 0 else 0

        # Pad to square matrix
        size = max(n, m)
        matrix = [[float('inf')] * size for _ in range(size)]

        for i in range(n):
            for j in range(m):
                matrix[i][j] = cost_matrix[i][j]

        if maximize:
            # Convert to minimization problem
            max_val = -float('inf')
            for i in range(n):
                for j in range(m):
                    if matrix[i][j] != float('inf'):
                        max_val = max(max_val, matrix[i][j])

            for i in range(size):
                for j in range(size):
                    if matrix[i][j] != float('inf'):
                        matrix[i][j] = max_val - matrix[i][j]

        # Apply Hungarian algorithm
        row_covered = [False] * size
        col_covered = [False] * size
        assignments = [[-1] * size for _ in range(size)]

        # Step 1: Row reduction
        for i in range(size):
            min_val = min(matrix[i])
            if min_val != float('inf'):
                for j in range(size):
                    matrix[i][j] -= min_val

        # Step 2: Column reduction
        for j in range(size):
            min_val = min(matrix[i][j] for i in range(size))
            if min_val != float('inf'):
                for i in range(size):
                    matrix[i][j] -= min_val

        # Find optimal assignment
        matches = self._kuhn_munkres(matrix, size)

        # Calculate cost
        total_cost = 0
        result = []
        for i, j in matches:
            if i < n and j < m:
                result.append((i, j))
                total_cost += cost_matrix[i][j]

        return result, total_cost

    def _kuhn_munkres(self, matrix: List[List[float]], size: int) -> List[Tuple[int, int]]:
        """Apply Kuhn-Munkres algorithm."""
        # Simplified implementation
        row_match = [-1] * size
        col_match = [-1] * size

        for i in range(size):
            visited = [False] * size
            self._find_augmenting_path(matrix, i, visited, row_match, col_match)

        # Extract matching
        matches = []
        for i in range(size):
            if row_match[i] != -1:
                matches.append((i, row_match[i]))

        return matches

    def _find_augmenting_path(self,
                             matrix: List[List[float]],
                             row: int,
                             visited: List[bool],
                             row_match: List[int],
                             col_match: List[int]) -> bool:
        """Find augmenting path using DFS."""
        for col in range(len(matrix[0])):
            if matrix[row][col] == 0 and not visited[col]:
                visited[col] = True

                if col_match[col] == -1 or \
                   self._find_augmenting_path(matrix, col_match[col],
                                            visited, row_match, col_match):
                    row_match[row] = col
                    col_match[col] = row
                    return True

        return False


def example_usage():
    """Demonstrate Hungarian algorithm."""
    print("=" * 60)
    print("Hungarian Algorithm Demonstration")
    print("=" * 60)

    # Example 1: Job Assignment Problem
    print("\n1. Job Assignment Problem")
    print("-" * 40)

    # Cost matrix: workers (rows) vs jobs (columns)
    # Each value is the cost for worker i to do job j
    cost_matrix = [
        [4, 2, 8, 5],
        [2, 3, 7, 6],
        [3, 4, 5, 7],
        [5, 8, 3, 4]
    ]

    print("Cost Matrix:")
    print("Worker\\Job", end="")
    for j in range(len(cost_matrix[0])):
        print(f"  J{j}", end="")
    print()

    for i, row in enumerate(cost_matrix):
        print(f"W{i}:       ", end="")
        for cost in row:
            print(f"  {cost:2}", end="")
        print()

    hungarian = HungarianAlgorithm(cost_matrix)
    assignments, total_cost = hungarian.solve()

    print("\nOptimal Assignment:")
    for worker, job in assignments:
        print(f"  Worker {worker} -> Job {job} (cost: {cost_matrix[worker][job]})")
    print(f"Total minimum cost: {total_cost}")

    # Example 2: Maximization Problem
    print("\n2. Profit Maximization Problem")
    print("-" * 40)

    # Profit matrix: maximize instead of minimize
    profit_matrix = [
        [10, 19, 8, 15],
        [10, 18, 7, 17],
        [13, 16, 9, 14],
        [12, 19, 8, 18]
    ]

    print("Profit Matrix:")
    for i, row in enumerate(profit_matrix):
        print(f"Agent {i}: {row}")

    hungarian_max = HungarianAlgorithm(profit_matrix, maximize=True)
    assignments, total_profit = hungarian_max.solve()

    print("\nOptimal Assignment for Maximum Profit:")
    for agent, task in assignments:
        print(f"  Agent {agent} -> Task {task} (profit: {profit_matrix[agent][task]})")
    print(f"Total maximum profit: {total_profit}")

    # Example 3: Unbalanced Assignment
    print("\n3. Unbalanced Assignment (More Workers than Jobs)")
    print("-" * 40)

    # 5 workers, 3 jobs
    unbalanced_cost = [
        [4, 5, 6],
        [2, 3, 4],
        [5, 6, 7],
        [3, 4, 5],
        [6, 7, 8]
    ]

    print("Cost Matrix (5 workers, 3 jobs):")
    for i, row in enumerate(unbalanced_cost):
        print(f"Worker {i}: {row}")

    hungarian_unbalanced = HungarianAlgorithm(unbalanced_cost)
    assignments, total_cost = hungarian_unbalanced.solve()

    print("\nOptimal Assignment:")
    assigned_workers = set()
    for worker, job in assignments:
        print(f"  Worker {worker} -> Job {job} (cost: {unbalanced_cost[worker][job]})")
        assigned_workers.add(worker)

    unassigned = set(range(5)) - assigned_workers
    if unassigned:
        print(f"Unassigned workers: {list(unassigned)}")
    print(f"Total minimum cost: {total_cost}")

    # Example 4: Large Scale Problem
    print("\n4. Large Scale Random Problem")
    print("-" * 40)

    # Generate random cost matrix
    np.random.seed(42)
    size = 10
    large_cost = np.random.randint(1, 100, (size, size)).tolist()

    print(f"Solving {size}x{size} assignment problem...")

    hungarian_large = HungarianAlgorithm(large_cost)
    assignments, total_cost = hungarian_large.solve()

    print(f"Total assignments: {len(assignments)}")
    print(f"Total minimum cost: {total_cost}")
    print(f"Average cost per assignment: {total_cost/len(assignments):.2f}")

    # Example 5: Solver Comparison
    print("\n5. Alternative Solver Comparison")
    print("-" * 40)

    solver = HungarianSolver()
    assignments2, total_cost2 = solver.solve_assignment(cost_matrix)

    print("Alternative solver results:")
    for worker, job in assignments2:
        print(f"  Worker {worker} -> Job {job}")
    print(f"Total cost: {total_cost2}")
    print(f"Results match: {total_cost == total_cost2}")

    # Example 6: Special Cases
    print("\n6. Special Cases")
    print("-" * 40)

    # All same cost
    same_cost = [[5] * 3 for _ in range(3)]
    print("All same cost matrix:")
    hungarian_same = HungarianAlgorithm(same_cost)
    assignments, total_cost = hungarian_same.solve()
    print(f"Total cost with identical values: {total_cost}")

    # Diagonal preference
    diagonal = [[10] * 4 for _ in range(4)]
    for i in range(4):
        diagonal[i][i] = 1

    print("\nDiagonal preference matrix:")
    hungarian_diagonal = HungarianAlgorithm(diagonal)
    assignments, total_cost = hungarian_diagonal.solve()
    print("Assignments (expecting diagonal):")
    for i, j in assignments:
        print(f"  {i} -> {j}")
    print(f"Total cost: {total_cost}")


if __name__ == "__main__":
    example_usage()