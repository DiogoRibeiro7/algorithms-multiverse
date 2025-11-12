#!/bin/bash
# Build and Test Script for C, Fortran, and R Implementations
#
# This script compiles all C and Fortran programs and runs tests

set -e  # Exit on error

echo "================================================================================"
echo "     ALGORITHMS MULTIVERSE - BUILD AND TEST SCRIPT"
echo "================================================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to print section header
print_header() {
    echo ""
    echo "================================================================================"
    echo "  $1"
    echo "================================================================================"
    echo ""
}

# Function to compile and run C program
compile_and_run_c() {
    local source=$1
    local output=$2
    local description=$3

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "[$TOTAL_TESTS] $description... "

    if gcc -O2 -o "$output" "$source" -lm 2>/dev/null; then
        echo -e "${GREEN}✓ Compiled${NC}"
        if ./"$output" > /dev/null 2>&1; then
            echo -e "    ${GREEN}✓ Executed successfully${NC}"
            PASSED_TESTS=$((PASSED_TESTS + 1))
        else
            echo -e "    ${RED}✗ Execution failed${NC}"
            FAILED_TESTS=$((FAILED_TESTS + 1))
        fi
        rm -f "$output"
    else
        echo -e "${RED}✗ Compilation failed${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Function to compile and run Fortran program
compile_and_run_fortran() {
    local source=$1
    local output=$2
    local description=$3

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "[$TOTAL_TESTS] $description... "

    if gfortran -O2 -o "$output" "$source" 2>/dev/null; then
        echo -e "${GREEN}✓ Compiled${NC}"
        if ./"$output" > /dev/null 2>&1; then
            echo -e "    ${GREEN}✓ Executed successfully${NC}"
            PASSED_TESTS=$((PASSED_TESTS + 1))
        else
            echo -e "    ${RED}✗ Execution failed${NC}"
            FAILED_TESTS=$((FAILED_TESTS + 1))
        fi
        rm -f "$output"
    else
        echo -e "${RED}✗ Compilation failed${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Function to run R script
run_r_script() {
    local script=$1
    local description=$2

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "[$TOTAL_TESTS] $description... "

    if Rscript "$script" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Executed successfully${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ Execution failed${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Check for required compilers
print_header "Checking Required Tools"

echo -n "Checking for gcc... "
if command -v gcc &> /dev/null; then
    echo -e "${GREEN}✓ Found$(NC}: $(gcc --version | head -n1)"
else
    echo -e "${RED}✗ Not found${NC}"
    echo "Please install gcc to compile C programs"
fi

echo -n "Checking for gfortran... "
if command -v gfortran &> /dev/null; then
    echo -e "${GREEN}✓ Found${NC}: $(gfortran --version | head -n1)"
else
    echo -e "${YELLOW}⚠ Not found${NC}"
    echo "gfortran is optional but recommended for Fortran programs"
fi

echo -n "Checking for R... "
if command -v Rscript &> /dev/null; then
    echo -e "${GREEN}✓ Found${NC}: $(R --version | head -n1)"
else
    echo -e "${YELLOW}⚠ Not found${NC}"
    echo "R is optional but recommended for R programs"
fi

# ================================================================================
# SORTING ALGORITHMS
# ================================================================================

print_header "Building and Testing SORTING ALGORITHMS"

# C implementations
if command -v gcc &> /dev/null; then
    compile_and_run_c "sorting/quicksort.c" "sorting/quicksort_c" "QuickSort (C)"
    compile_and_run_c "sorting/mergesort.c" "sorting/mergesort_c" "MergeSort (C)"
fi

# Fortran implementations
if command -v gfortran &> /dev/null; then
    compile_and_run_fortran "sorting/quicksort.f90" "sorting/quicksort_f90" "QuickSort (Fortran)"
    compile_and_run_fortran "sorting/mergesort.f90" "sorting/mergesort_f90" "MergeSort (Fortran)"
fi

# R implementations
if command -v Rscript &> /dev/null; then
    run_r_script "sorting/quicksort.R" "QuickSort (R)"
    run_r_script "sorting/mergesort.R" "MergeSort (R)"
fi

# ================================================================================
# GRAPH ALGORITHMS
# ================================================================================

print_header "Building and Testing GRAPH ALGORITHMS"

# C implementation
if command -v gcc &> /dev/null; then
    compile_and_run_c "graph-algorithms/graph_algorithms.c" "graph-algorithms/graph_c" "Graph Algorithms (C)"
fi

# Fortran implementation
if command -v gfortran &> /dev/null; then
    compile_and_run_fortran "graph-algorithms/graph_algorithms.f90" "graph-algorithms/graph_f90" "Graph Algorithms (Fortran)"
fi

# R implementation
if command -v Rscript &> /dev/null; then
    run_r_script "graph-algorithms/graph_algorithms.R" "Graph Algorithms (R)"
fi

# ================================================================================
# DYNAMIC PROGRAMMING
# ================================================================================

print_header "Building and Testing DYNAMIC PROGRAMMING"

# C implementation
if command -v gcc &> /dev/null; then
    compile_and_run_c "dynamic-programming/dp_algorithms.c" "dynamic-programming/dp_c" "DP Algorithms (C)"
fi

# ================================================================================
# SUMMARY
# ================================================================================

print_header "TEST SUMMARY"

echo "Total tests:  $TOTAL_TESTS"
echo -e "Passed:       ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed:       ${RED}$FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    exit 0
else
    echo ""
    echo -e "${YELLOW}⚠ Some tests failed. Check the output above for details.${NC}"
    echo ""
    exit 1
fi
