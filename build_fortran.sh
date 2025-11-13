#!/bin/bash
# Comprehensive Build and Test Script for Fortran Implementations
#
# Compiles and runs all Fortran programs in the repository

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TOTAL=0
PASSED=0
FAILED=0

echo "================================================================================"
echo "          FORTRAN ALGORITHMS - BUILD AND TEST SUITE"
echo "================================================================================"
echo ""

# Check for gfortran
if ! command -v gfortran &> /dev/null; then
    echo -e "${RED}Error: gfortran not found!${NC}"
    echo "Please install gfortran to compile Fortran programs"
    echo ""
    echo "Installation:"
    echo "  Ubuntu/Debian: sudo apt-get install gfortran"
    echo "  macOS:         brew install gcc"
    echo "  Windows:       Install MinGW-w64"
    exit 1
fi

echo -e "${GREEN}✓ Found gfortran:${NC} $(gfortran --version | head -n1)"
echo ""

# Function to compile and run
compile_and_run() {
    local source=$1
    local output=$2
    local description=$3

    TOTAL=$((TOTAL + 1))
    echo "--------------------------------------------------------------------------------"
    echo -e "${BLUE}[$TOTAL] $description${NC}"
    echo "Source: $source"
    echo ""

    # Compile
    echo -n "Compiling... "
    if gfortran -O2 -o "$output" "$source" 2>error.log; then
        echo -e "${GREEN}✓ Success${NC}"
        rm -f error.log

        # Run
        echo -n "Running...   "
        if timeout 10 ./"$output" > output.log 2>&1; then
            echo -e "${GREEN}✓ Success${NC}"
            echo ""
            echo "Output (first 20 lines):"
            echo "----------------------------------------"
            head -n 20 output.log
            echo "----------------------------------------"
            echo ""
            PASSED=$((PASSED + 1))
        else
            echo -e "${RED}✗ Execution failed${NC}"
            echo "Error output:"
            cat output.log
            echo ""
            FAILED=$((FAILED + 1))
        fi

        rm -f output.log "$output"
    else
        echo -e "${RED}✗ Compilation failed${NC}"
        echo "Error output:"
        cat error.log
        echo ""
        rm -f error.log
        FAILED=$((FAILED + 1))
    fi
}

# ================================================================================
# SORTING ALGORITHMS
# ================================================================================

echo "================================================================================"
echo "                          SORTING ALGORITHMS"
echo "================================================================================"
echo ""

if [ -f "sorting/quicksort.f90" ]; then
    compile_and_run "sorting/quicksort.f90" "sorting/quicksort_test" \
                    "QuickSort - O(n log n) average case sorting"
fi

if [ -f "sorting/mergesort.f90" ]; then
    compile_and_run "sorting/mergesort.f90" "sorting/mergesort_test" \
                    "MergeSort - O(n log n) stable sorting"
fi

if [ -f "sorting/heapsort.f90" ]; then
    compile_and_run "sorting/heapsort.f90" "sorting/heapsort_test" \
                    "HeapSort - O(n log n) in-place sorting with priority queue"
fi

# ================================================================================
# GRAPH ALGORITHMS
# ================================================================================

echo ""
echo "================================================================================"
echo "                          GRAPH ALGORITHMS"
echo "================================================================================"
echo ""

if [ -f "graph-algorithms/graph_algorithms.f90" ]; then
    compile_and_run "graph-algorithms/graph_algorithms.f90" "graph-algorithms/graph_test" \
                    "Graph Algorithms - BFS, DFS, Dijkstra's shortest path"
fi

# ================================================================================
# DYNAMIC PROGRAMMING
# ================================================================================

echo ""
echo "================================================================================"
echo "                       DYNAMIC PROGRAMMING"
echo "================================================================================"
echo ""

if [ -f "dynamic-programming/dp_algorithms.f90" ]; then
    compile_and_run "dynamic-programming/dp_algorithms.f90" "dynamic-programming/dp_test" \
                    "Dynamic Programming - Fibonacci, Knapsack, LCS, Coin Change, Edit Distance"
fi

# ================================================================================
# SEARCH ALGORITHMS
# ================================================================================

echo ""
echo "================================================================================"
echo "                          SEARCH ALGORITHMS"
echo "================================================================================"
echo ""

if [ -f "searching/advanced_search.f90" ]; then
    compile_and_run "searching/advanced_search.f90" "searching/search_test" \
                    "Advanced Search - Binary, Interpolation, Jump, Exponential, Ternary, Fibonacci"
fi

# ================================================================================
# STRING ALGORITHMS
# ================================================================================

echo ""
echo "================================================================================"
echo "                         STRING ALGORITHMS"
echo "================================================================================"
echo ""

if [ -f "string-algorithms/string_algorithms.f90" ]; then
    compile_and_run "string-algorithms/string_algorithms.f90" "string-algorithms/string_test" \
                    "String Algorithms - Pattern Matching, KMP, Rabin-Karp, Palindromes"
fi

# ================================================================================
# NUMERICAL ALGORITHMS
# ================================================================================

echo ""
echo "================================================================================"
echo "                        NUMERICAL ALGORITHMS"
echo "================================================================================"
echo ""

if [ -f "numerical/numerical_algorithms.f90" ]; then
    compile_and_run "numerical/numerical_algorithms.f90" "numerical/numerical_test" \
                    "Numerical Methods - Root Finding, Integration, Matrix Operations, Linear Systems"
fi

# ================================================================================
# EXISTING IMPLEMENTATIONS
# ================================================================================

echo ""
echo "================================================================================"
echo "                    EXISTING IMPLEMENTATIONS"
echo "================================================================================"
echo ""

# Number Theory
if [ -f "number-theory/number_theory.f90" ]; then
    compile_and_run "number-theory/number_theory.f90" "number-theory/nt_test" \
                    "Number Theory - Primes, GCD, Modular Arithmetic"
fi

# Computational Geometry
if [ -f "computational-geometry/geometry.f90" ]; then
    compile_and_run "computational-geometry/geometry.f90" "computational-geometry/geom_test" \
                    "Computational Geometry - Convex Hull, Line Intersection"
fi

# ================================================================================
# SUMMARY
# ================================================================================

echo ""
echo "================================================================================"
echo "                            TEST SUMMARY"
echo "================================================================================"
echo ""
echo "Total Programs:  $TOTAL"
echo -e "${GREEN}Passed:          $PASSED${NC}"
echo -e "${RED}Failed:          $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}════════════════════════════════════════════════════════════════════════════════"
    echo "                    ✓ ALL TESTS PASSED SUCCESSFULLY!"
    echo "════════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    exit 0
else
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════════════════════"
    echo "                 ⚠ SOME TESTS FAILED - CHECK OUTPUT ABOVE"
    echo "════════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    exit 1
fi
