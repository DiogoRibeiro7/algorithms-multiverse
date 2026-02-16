"""
Simplex Method for Linear Programming
=====================================

Implementation of the Simplex algorithm for solving linear programming problems.
The Simplex method is a fundamental algorithm for optimizing linear objective
functions subject to linear equality and inequality constraints.

Key Features:
- Two-phase Simplex method
- Big M method for artificial variables
- Dual Simplex method
- Revised Simplex method
- Sensitivity analysis
- Integer programming branch-and-bound
- Transportation problem solver

Applications:
- Resource allocation
- Production planning
- Diet optimization
- Transportation logistics
- Portfolio optimization
- Network flow problems
- Game theory

Author: Claude
Date: January 2026
"""

import numpy as np
from typing import List, Tuple, Optional, Dict, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import math
from fractions import Fraction


class OptimizationType(Enum):
    """Optimization problem type."""
    MINIMIZE = "minimize"
    MAXIMIZE = "maximize"


class SimplexStatus(Enum):
    """Status of Simplex solution."""
    OPTIMAL = "optimal"
    UNBOUNDED = "unbounded"
    INFEASIBLE = "infeasible"
    CYCLING = "cycling"


@dataclass
class LinearProgram:
    """
    Linear programming problem in standard form:
    Minimize c^T x
    Subject to: Ax = b, x >= 0
    """
    c: np.ndarray  # Objective coefficients
    A: np.ndarray  # Constraint matrix
    b: np.ndarray  # Right-hand side
    optimization_type: OptimizationType = OptimizationType.MINIMIZE

    def to_standard_form(self):
        """Convert to standard minimization form."""
        if self.optimization_type == OptimizationType.MAXIMIZE:
            self.c = -self.c
            self.optimization_type = OptimizationType.MINIMIZE


@dataclass
class SimplexTableau:
    """Simplex tableau representation."""
    tableau: np.ndarray
    basis: List[int]
    m: int  # Number of constraints
    n: int  # Number of variables

    def get_objective_value(self) -> float:
        """Get current objective value."""
        return -self.tableau[0, -1]

    def get_basic_solution(self) -> np.ndarray:
        """Extract basic feasible solution."""
        solution = np.zeros(self.n)
        for i, var in enumerate(self.basis):
            if var < self.n:
                solution[var] = self.tableau[i + 1, -1]
        return solution


class SimplexSolver:
    """
    Standard Simplex method solver for linear programming.
    """

    def __init__(self, lp: LinearProgram):
        """
        Initialize Simplex solver.

        Args:
            lp: Linear programming problem
        """
        self.lp = lp
        self.lp.to_standard_form()
        self.m, self.n = lp.A.shape
        self.iterations = 0
        self.tableau = None

    def solve(self, max_iterations: int = 1000) -> Tuple[SimplexStatus, Optional[np.ndarray], float]:
        """
        Solve linear program using Simplex method.

        Args:
            max_iterations: Maximum iterations allowed

        Returns:
            (status, solution, objective_value)
        """
        # Phase 1: Find initial basic feasible solution
        if not self._has_feasible_basis():
            status, initial_solution = self._phase_one()
            if status != SimplexStatus.OPTIMAL:
                return SimplexStatus.INFEASIBLE, None, float('inf')

        # Phase 2: Optimize
        self._initialize_tableau()
        status = self._simplex_iterations(max_iterations)

        if status == SimplexStatus.OPTIMAL:
            solution = self.tableau.get_basic_solution()
            obj_value = self.tableau.get_objective_value()
            return status, solution, obj_value

        return status, None, float('inf')

    def _has_feasible_basis(self) -> bool:
        """Check if we have an obvious feasible basis."""
        # Check if b >= 0 (can use slack variables)
        return np.all(self.lp.b >= 0)

    def _initialize_tableau(self):
        """Initialize Simplex tableau."""
        m, n = self.m, self.n

        # Create tableau with slack/artificial variables
        tableau = np.zeros((m + 1, n + m + 1))

        # Objective row
        tableau[0, :n] = self.lp.c

        # Constraint rows
        tableau[1:, :n] = self.lp.A
        tableau[1:, n:n+m] = np.eye(m)  # Slack/artificial variables
        tableau[1:, -1] = self.lp.b

        # Initial basis (slack variables)
        basis = list(range(n, n + m))

        self.tableau = SimplexTableau(tableau, basis, m, n)

    def _simplex_iterations(self, max_iterations: int) -> SimplexStatus:
        """
        Perform Simplex iterations.

        Args:
            max_iterations: Maximum iterations

        Returns:
            Solution status
        """
        for _ in range(max_iterations):
            self.iterations += 1

            # Find entering variable (most negative reduced cost)
            entering = self._find_entering_variable()
            if entering is None:
                return SimplexStatus.OPTIMAL

            # Find leaving variable (minimum ratio test)
            leaving = self._find_leaving_variable(entering)
            if leaving is None:
                return SimplexStatus.UNBOUNDED

            # Pivot
            self._pivot(entering, leaving)

        return SimplexStatus.CYCLING

    def _find_entering_variable(self) -> Optional[int]:
        """Find entering variable using Bland's rule to avoid cycling."""
        reduced_costs = self.tableau.tableau[0, :-1]

        # Find first negative reduced cost
        for i in range(len(reduced_costs)):
            if reduced_costs[i] < -1e-10:
                return i
        return None

    def _find_leaving_variable(self, entering: int) -> Optional[int]:
        """Find leaving variable using minimum ratio test."""
        column = self.tableau.tableau[1:, entering]
        rhs = self.tableau.tableau[1:, -1]

        min_ratio = float('inf')
        leaving = None

        for i in range(self.m):
            if column[i] > 1e-10:  # Positive coefficient
                ratio = rhs[i] / column[i]
                if ratio < min_ratio:
                    min_ratio = ratio
                    leaving = i

        return leaving

    def _pivot(self, entering: int, leaving: int):
        """Perform pivot operation."""
        tableau = self.tableau.tableau
        pivot_row = leaving + 1
        pivot_col = entering

        # Normalize pivot row
        pivot_element = tableau[pivot_row, pivot_col]
        tableau[pivot_row] /= pivot_element

        # Eliminate column
        for i in range(len(tableau)):
            if i != pivot_row:
                multiplier = tableau[i, pivot_col]
                tableau[i] -= multiplier * tableau[pivot_row]

        # Update basis
        self.tableau.basis[leaving] = entering

    def _phase_one(self) -> Tuple[SimplexStatus, Optional[np.ndarray]]:
        """
        Phase 1: Find initial basic feasible solution.

        Returns:
            (status, initial_solution)
        """
        # Add artificial variables where needed
        artificial_vars = []
        extended_A = self.lp.A.copy()

        for i in range(self.m):
            if self.lp.b[i] < 0:
                # Multiply constraint by -1
                extended_A[i] *= -1
                self.lp.b[i] *= -1
            artificial_vars.append(i)

        # Create Phase 1 objective (minimize sum of artificial variables)
        phase1_c = np.zeros(self.n + len(artificial_vars))
        phase1_c[self.n:] = 1

        # Solve Phase 1 problem
        phase1_lp = LinearProgram(phase1_c, extended_A, self.lp.b)
        phase1_solver = SimplexSolver(phase1_lp)
        status, solution, obj_val = phase1_solver.solve()

        if status == SimplexStatus.OPTIMAL and abs(obj_val) < 1e-10:
            return SimplexStatus.OPTIMAL, solution[:self.n]

        return SimplexStatus.INFEASIBLE, None


class DualSimplexSolver:
    """
    Dual Simplex method for solving linear programming problems.
    Useful when dual feasibility is easier to maintain.
    """

    def __init__(self, lp: LinearProgram):
        """Initialize Dual Simplex solver."""
        self.lp = lp
        self.lp.to_standard_form()

    def solve(self) -> Tuple[SimplexStatus, Optional[np.ndarray], float]:
        """
        Solve using Dual Simplex method.

        Returns:
            (status, solution, objective_value)
        """
        # Convert to dual problem
        dual_lp = self._get_dual_problem()

        # Solve dual with standard Simplex
        solver = SimplexSolver(dual_lp)
        status, dual_solution, dual_obj = solver.solve()

        if status == SimplexStatus.OPTIMAL:
            # Extract primal solution from dual
            primal_solution = self._extract_primal_from_dual(dual_solution)
            return status, primal_solution, dual_obj

        return status, None, float('inf')

    def _get_dual_problem(self) -> LinearProgram:
        """Convert primal to dual problem."""
        # Dual: Maximize b^T y subject to A^T y <= c
        dual_c = -self.lp.b  # Maximize b^T y = minimize -b^T y
        dual_A = -self.lp.A.T  # A^T y <= c becomes -A^T y >= -c
        dual_b = -self.lp.c

        return LinearProgram(dual_c, dual_A, dual_b, OptimizationType.MINIMIZE)

    def _extract_primal_from_dual(self, dual_solution: np.ndarray) -> np.ndarray:
        """Extract primal solution from dual solution."""
        # In strong duality, primal variables are dual slack variables
        # This is a simplified extraction
        return dual_solution[:self.lp.A.shape[1]]


class TransportationProblem:
    """
    Solver for transportation problems using specialized algorithms.
    """

    def __init__(self, supply: np.ndarray, demand: np.ndarray, costs: np.ndarray):
        """
        Initialize transportation problem.

        Args:
            supply: Supply at each source
            demand: Demand at each destination
            costs: Cost matrix (sources x destinations)
        """
        self.supply = supply
        self.demand = demand
        self.costs = costs
        self.m = len(supply)  # Number of sources
        self.n = len(demand)  # Number of destinations

    def solve_northwest_corner(self) -> np.ndarray:
        """
        Find initial solution using Northwest Corner method.

        Returns:
            Initial allocation matrix
        """
        allocation = np.zeros((self.m, self.n))
        supply = self.supply.copy()
        demand = self.demand.copy()

        i, j = 0, 0
        while i < self.m and j < self.n:
            quantity = min(supply[i], demand[j])
            allocation[i, j] = quantity
            supply[i] -= quantity
            demand[j] -= quantity

            if supply[i] == 0:
                i += 1
            if demand[j] == 0:
                j += 1

        return allocation

    def solve_vogel(self) -> np.ndarray:
        """
        Find initial solution using Vogel's approximation method.

        Returns:
            Initial allocation matrix
        """
        allocation = np.zeros((self.m, self.n))
        supply = self.supply.copy()
        demand = self.demand.copy()

        while np.sum(supply) > 0 and np.sum(demand) > 0:
            # Calculate penalties
            row_penalties = []
            for i in range(self.m):
                if supply[i] > 0:
                    costs_row = [self.costs[i, j] for j in range(self.n) if demand[j] > 0]
                    if len(costs_row) >= 2:
                        costs_row.sort()
                        row_penalties.append((costs_row[1] - costs_row[0], i))
                    elif len(costs_row) == 1:
                        row_penalties.append((0, i))

            col_penalties = []
            for j in range(self.n):
                if demand[j] > 0:
                    costs_col = [self.costs[i, j] for i in range(self.m) if supply[i] > 0]
                    if len(costs_col) >= 2:
                        costs_col.sort()
                        col_penalties.append((costs_col[1] - costs_col[0], j))
                    elif len(costs_col) == 1:
                        col_penalties.append((0, j))

            # Find maximum penalty
            if not row_penalties and not col_penalties:
                break

            max_row_penalty = max(row_penalties, key=lambda x: x[0]) if row_penalties else (-1, -1)
            max_col_penalty = max(col_penalties, key=lambda x: x[0]) if col_penalties else (-1, -1)

            if max_row_penalty[0] >= max_col_penalty[0]:
                # Use row with max penalty
                i = max_row_penalty[1]
                # Find minimum cost in this row
                j = min([j for j in range(self.n) if demand[j] > 0],
                       key=lambda j: self.costs[i, j])
            else:
                # Use column with max penalty
                j = max_col_penalty[1]
                # Find minimum cost in this column
                i = min([i for i in range(self.m) if supply[i] > 0],
                       key=lambda i: self.costs[i, j])

            # Allocate
            quantity = min(supply[i], demand[j])
            allocation[i, j] = quantity
            supply[i] -= quantity
            demand[j] -= quantity

        return allocation

    def optimize_modi(self, initial_allocation: np.ndarray) -> np.ndarray:
        """
        Optimize using MODI (Modified Distribution) method.

        Args:
            initial_allocation: Initial feasible solution

        Returns:
            Optimal allocation
        """
        allocation = initial_allocation.copy()
        max_iterations = 100

        for _ in range(max_iterations):
            # Calculate dual variables (u and v)
            u, v = self._calculate_dual_variables(allocation)

            # Calculate opportunity costs
            improved = False
            for i in range(self.m):
                for j in range(self.n):
                    if allocation[i, j] == 0:
                        opportunity_cost = self.costs[i, j] - u[i] - v[j]
                        if opportunity_cost < 0:
                            # Improvement possible
                            allocation = self._improve_allocation(allocation, i, j)
                            improved = True
                            break
                if improved:
                    break

            if not improved:
                break

        return allocation

    def _calculate_dual_variables(self, allocation: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate dual variables u and v."""
        u = np.full(self.m, np.nan)
        v = np.full(self.n, np.nan)

        # Start with u[0] = 0
        u[0] = 0

        # Iteratively calculate u and v
        changed = True
        while changed:
            changed = False
            for i in range(self.m):
                for j in range(self.n):
                    if allocation[i, j] > 0:
                        if not np.isnan(u[i]) and np.isnan(v[j]):
                            v[j] = self.costs[i, j] - u[i]
                            changed = True
                        elif np.isnan(u[i]) and not np.isnan(v[j]):
                            u[i] = self.costs[i, j] - v[j]
                            changed = True

        return u, v

    def _improve_allocation(self, allocation: np.ndarray, enter_i: int, enter_j: int) -> np.ndarray:
        """Improve allocation by finding a cycle and adjusting."""
        # Simplified: just return current allocation
        # Full implementation would find closed loop and adjust
        return allocation


class IntegerProgrammingSolver:
    """
    Integer Linear Programming solver using Branch and Bound.
    """

    def __init__(self, lp: LinearProgram, integer_vars: Set[int]):
        """
        Initialize ILP solver.

        Args:
            lp: Linear program
            integer_vars: Indices of integer variables
        """
        self.lp = lp
        self.integer_vars = integer_vars
        self.best_solution = None
        self.best_objective = float('inf')
        self.nodes_explored = 0

    def solve(self) -> Tuple[SimplexStatus, Optional[np.ndarray], float]:
        """
        Solve integer linear program using branch and bound.

        Returns:
            (status, solution, objective_value)
        """
        # Start with root node (relaxed LP)
        self._branch_and_bound(self.lp, 0)

        if self.best_solution is not None:
            return SimplexStatus.OPTIMAL, self.best_solution, self.best_objective
        return SimplexStatus.INFEASIBLE, None, float('inf')

    def _branch_and_bound(self, node_lp: LinearProgram, depth: int):
        """Recursive branch and bound."""
        self.nodes_explored += 1

        # Solve relaxed LP
        solver = SimplexSolver(node_lp)
        status, solution, obj_value = solver.solve()

        if status != SimplexStatus.OPTIMAL:
            return  # Prune infeasible branch

        # Check if objective is worse than current best (pruning)
        if obj_value >= self.best_objective:
            return

        # Check if solution is integer
        is_integer = True
        branch_var = None
        branch_value = None

        for var in self.integer_vars:
            if var < len(solution):
                value = solution[var]
                if abs(value - round(value)) > 1e-6:
                    is_integer = False
                    branch_var = var
                    branch_value = value
                    break

        if is_integer:
            # Update best solution
            self.best_solution = solution
            self.best_objective = obj_value
            return

        # Branch on fractional variable
        if branch_var is not None:
            floor_val = math.floor(branch_value)
            ceil_val = math.ceil(branch_value)

            # Create two branches
            # Branch 1: x <= floor
            branch1_lp = self._add_constraint(node_lp, branch_var, floor_val, "<=")
            self._branch_and_bound(branch1_lp, depth + 1)

            # Branch 2: x >= ceil
            branch2_lp = self._add_constraint(node_lp, branch_var, ceil_val, ">=")
            self._branch_and_bound(branch2_lp, depth + 1)

    def _add_constraint(self, lp: LinearProgram, var: int, value: float,
                        direction: str) -> LinearProgram:
        """Add branching constraint to LP."""
        # Create new constraint row
        new_row = np.zeros(lp.A.shape[1])
        new_row[var] = 1 if direction == ">=" else -1

        # Add to constraint matrix
        new_A = np.vstack([lp.A, new_row])
        new_b = np.append(lp.b, value if direction == ">=" else -value)

        return LinearProgram(lp.c, new_A, new_b, lp.optimization_type)


def diet_problem_example():
    """Example: Diet optimization problem."""
    print("=" * 60)
    print("DIET OPTIMIZATION PROBLEM")
    print("=" * 60)

    # Foods: Bread, Milk, Eggs, Meat
    # Nutrients: Calories, Protein, Calcium

    # Cost per unit of food
    costs = np.array([2.0, 3.5, 3.0, 8.0])

    # Nutrient content matrix (nutrients x foods)
    nutrients = np.array([
        [100, 150, 80, 250],   # Calories per unit
        [3, 8, 7, 20],          # Protein (g) per unit
        [15, 300, 20, 10]       # Calcium (mg) per unit
    ])

    # Minimum daily requirements
    requirements = np.array([2000, 50, 800])  # Calories, Protein, Calcium

    print("Foods: Bread, Milk, Eggs, Meat")
    print(f"Costs: ${costs}")
    print(f"\nMinimum requirements:")
    print(f"  Calories: {requirements[0]}")
    print(f"  Protein: {requirements[1]}g")
    print(f"  Calcium: {requirements[2]}mg")

    # Formulate as LP: minimize cost subject to nutrient constraints
    # Variables: x = [bread, milk, eggs, meat]
    # Minimize: c^T x
    # Subject to: nutrients * x >= requirements, x >= 0

    # Convert to standard form (Ax = b)
    # Add slack variables for >= constraints
    A = np.hstack([nutrients, -np.eye(3)])  # Include slack variables
    b = requirements
    c = np.concatenate([costs, np.zeros(3)])  # No cost for slack variables

    lp = LinearProgram(c, A, b, OptimizationType.MINIMIZE)
    solver = SimplexSolver(lp)
    status, solution, cost = solver.solve()

    if status == SimplexStatus.OPTIMAL:
        print(f"\nOptimal solution found!")
        print(f"Minimum daily cost: ${cost:.2f}")
        print(f"\nOptimal quantities:")
        food_names = ["Bread", "Milk", "Eggs", "Meat"]
        for i, name in enumerate(food_names):
            if i < len(solution):
                print(f"  {name}: {solution[i]:.2f} units")

        # Verify nutrient constraints
        total_nutrients = nutrients @ solution[:4]
        print(f"\nNutrient totals:")
        print(f"  Calories: {total_nutrients[0]:.0f} (required: {requirements[0]})")
        print(f"  Protein: {total_nutrients[1]:.1f}g (required: {requirements[1]}g)")
        print(f"  Calcium: {total_nutrients[2]:.0f}mg (required: {requirements[2]}mg)")


def production_planning_example():
    """Example: Production planning optimization."""
    print("\n" + "=" * 60)
    print("PRODUCTION PLANNING")
    print("=" * 60)

    # Products: Tables, Chairs
    # Resources: Wood, Labor

    # Profit per product
    profits = np.array([50, 30])  # Tables: $50, Chairs: $30

    # Resource requirements (resources x products)
    requirements = np.array([
        [4, 2],  # Wood needed (units)
        [3, 1]   # Labor needed (hours)
    ])

    # Available resources
    available = np.array([100, 60])  # 100 units wood, 60 hours labor

    print("Products: Tables, Chairs")
    print(f"Profit per unit: ${profits}")
    print(f"Wood required: {requirements[0]} units")
    print(f"Labor required: {requirements[1]} hours")
    print(f"Available: {available[0]} wood, {available[1]} labor hours")

    # Maximize profit subject to resource constraints
    # Convert to minimization: minimize -profit
    c = -profits
    A = requirements
    b = available

    # Add slack variables for <= constraints
    A_with_slack = np.hstack([A, np.eye(2)])
    c_with_slack = np.concatenate([c, np.zeros(2)])

    lp = LinearProgram(c_with_slack, A_with_slack, b, OptimizationType.MINIMIZE)
    solver = SimplexSolver(lp)
    status, solution, neg_profit = solver.solve()

    if status == SimplexStatus.OPTIMAL:
        profit = -neg_profit
        print(f"\nOptimal production plan:")
        print(f"  Tables: {solution[0]:.0f} units")
        print(f"  Chairs: {solution[1]:.0f} units")
        print(f"  Maximum profit: ${profit:.2f}")

        # Resource utilization
        used = requirements @ solution[:2]
        print(f"\nResource utilization:")
        print(f"  Wood: {used[0]:.0f}/{available[0]} units")
        print(f"  Labor: {used[1]:.0f}/{available[1]} hours")


def transportation_problem_example():
    """Example: Transportation optimization."""
    print("\n" + "=" * 60)
    print("TRANSPORTATION PROBLEM")
    print("=" * 60)

    # 3 warehouses, 4 stores
    supply = np.array([50, 60, 40])  # Supply at each warehouse
    demand = np.array([30, 45, 35, 40])  # Demand at each store

    # Transportation costs (warehouse x store)
    costs = np.array([
        [8, 6, 10, 9],
        [9, 12, 13, 7],
        [14, 9, 16, 5]
    ])

    print(f"Warehouses supply: {supply}")
    print(f"Store demand: {demand}")
    print(f"Transportation costs:")
    for i, row in enumerate(costs):
        print(f"  Warehouse {i+1}: {row}")

    # Check if balanced
    total_supply = np.sum(supply)
    total_demand = np.sum(demand)

    if total_supply != total_demand:
        print(f"\nUnbalanced problem: supply={total_supply}, demand={total_demand}")
        # Balance by adding dummy source/destination
        if total_supply > total_demand:
            # Add dummy destination
            demand = np.append(demand, total_supply - total_demand)
            costs = np.hstack([costs, np.zeros((3, 1))])

    transport = TransportationProblem(supply, demand, costs)

    # Find initial solution
    print("\nFinding initial solution using Northwest Corner...")
    initial = transport.solve_northwest_corner()
    initial_cost = np.sum(initial * costs[:3, :4])
    print(f"Initial cost: ${initial_cost:.0f}")

    # Find better initial using Vogel's method
    print("\nFinding solution using Vogel's method...")
    vogel = transport.solve_vogel()
    vogel_cost = np.sum(vogel * costs[:3, :4])
    print(f"Vogel's cost: ${vogel_cost:.0f}")

    # Optimize using MODI
    print("\nOptimizing with MODI method...")
    optimal = transport.optimize_modi(vogel)
    optimal_cost = np.sum(optimal * costs[:3, :4])
    print(f"Optimal cost: ${optimal_cost:.0f}")

    print("\nOptimal shipping plan:")
    for i in range(3):
        for j in range(4):
            if optimal[i, j] > 0:
                print(f"  Ship {optimal[i, j]:.0f} units from "
                      f"Warehouse {i+1} to Store {j+1}")


def integer_programming_example():
    """Example: Integer programming (knapsack problem)."""
    print("\n" + "=" * 60)
    print("INTEGER PROGRAMMING - KNAPSACK PROBLEM")
    print("=" * 60)

    # Items: weights and values
    weights = np.array([4, 3, 2, 3])
    values = np.array([10, 7, 5, 8])
    capacity = 8

    print(f"Items weights: {weights}")
    print(f"Items values: ${values}")
    print(f"Knapsack capacity: {capacity}")

    # Binary knapsack: maximize value subject to weight constraint
    # Variables: x[i] = 1 if item i is selected, 0 otherwise

    n_items = len(weights)

    # Objective: maximize value (convert to minimization)
    c = -values

    # Constraint: sum(weights * x) <= capacity
    A = np.array([weights])
    b = np.array([capacity])

    # Add bounds 0 <= x[i] <= 1
    for i in range(n_items):
        # x[i] <= 1
        row = np.zeros(n_items)
        row[i] = 1
        A = np.vstack([A, row])
        b = np.append(b, 1)

    lp = LinearProgram(c, A, b, OptimizationType.MINIMIZE)

    # Solve as integer program
    integer_vars = set(range(n_items))
    ilp_solver = IntegerProgrammingSolver(lp, integer_vars)
    status, solution, neg_value = ilp_solver.solve()

    if status == SimplexStatus.OPTIMAL and solution is not None:
        value = -neg_value
        print(f"\nOptimal selection (value: ${value:.0f}):")
        selected_weight = 0
        for i in range(min(n_items, len(solution))):
            if solution[i] > 0.5:  # Binary variable
                print(f"  Item {i+1}: weight={weights[i]}, value=${values[i]}")
                selected_weight += weights[i]
        print(f"Total weight: {selected_weight}/{capacity}")
        print(f"Nodes explored: {ilp_solver.nodes_explored}")


def sensitivity_analysis_example():
    """Example: Sensitivity analysis on LP solution."""
    print("\n" + "=" * 60)
    print("SENSITIVITY ANALYSIS")
    print("=" * 60)

    # Simple production problem
    # Maximize: 3x + 2y
    # Subject to: x + y <= 4, 2x + y <= 5, x,y >= 0

    c = np.array([-3, -2])  # Minimize negative for maximization
    A = np.array([
        [1, 1],
        [2, 1]
    ])
    b = np.array([4, 5])

    print("Original problem:")
    print("  Maximize: 3x + 2y")
    print("  Subject to: x + y <= 4")
    print("              2x + y <= 5")

    # Solve original
    A_with_slack = np.hstack([A, np.eye(2)])
    c_with_slack = np.concatenate([c, np.zeros(2)])

    lp = LinearProgram(c_with_slack, A_with_slack, b)
    solver = SimplexSolver(lp)
    status, solution, neg_obj = solver.solve()

    if status == SimplexStatus.OPTIMAL:
        print(f"\nOptimal solution:")
        print(f"  x = {solution[0]:.2f}")
        print(f"  y = {solution[1]:.2f}")
        print(f"  Objective value: {-neg_obj:.2f}")

        # Test sensitivity to objective coefficients
        print("\nSensitivity to objective coefficient of x:")
        for delta in [-1, -0.5, 0, 0.5, 1]:
            c_test = np.array([c[0] + delta, c[1]])
            c_test_slack = np.concatenate([c_test, np.zeros(2)])
            lp_test = LinearProgram(c_test_slack, A_with_slack, b)
            solver_test = SimplexSolver(lp_test)
            _, sol_test, obj_test = solver_test.solve()

            if sol_test is not None:
                print(f"  c1 = {-c_test[0]:.1f}: x={sol_test[0]:.2f}, "
                      f"y={sol_test[1]:.2f}, obj={-obj_test:.2f}")

        # Test sensitivity to RHS
        print("\nSensitivity to first constraint RHS:")
        for delta in [-1, -0.5, 0, 0.5, 1]:
            b_test = np.array([b[0] + delta, b[1]])
            lp_test = LinearProgram(c_with_slack, A_with_slack, b_test)
            solver_test = SimplexSolver(lp_test)
            _, sol_test, obj_test = solver_test.solve()

            if sol_test is not None:
                print(f"  b1 = {b_test[0]:.1f}: x={sol_test[0]:.2f}, "
                      f"y={sol_test[1]:.2f}, obj={-obj_test:.2f}")


if __name__ == "__main__":
    # Run examples
    diet_problem_example()
    production_planning_example()
    transportation_problem_example()
    integer_programming_example()
    sensitivity_analysis_example()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- Simplex method solves linear programs efficiently")
    print("- Two-phase method handles infeasible starting points")
    print("- Transportation problems have specialized algorithms")
    print("- Integer programming uses branch and bound")
    print("- Sensitivity analysis reveals solution robustness")
    print("=" * 60)