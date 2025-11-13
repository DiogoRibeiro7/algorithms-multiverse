#!/bin/bash
# Comprehensive Build and Test Script for Fortran Data Structures
#
# Compiles and runs all Fortran data structure implementations
#
# Author: Algorithms Multiverse

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
echo "        FORTRAN DATA STRUCTURES - BUILD AND TEST SUITE"
echo "================================================================================"
echo ""

# Check for gfortran
if ! command -v gfortran &> /dev/null; then
    echo -e "${RED}Error: gfortran not found!${NC}"
    echo "Please install gfortran to compile Fortran programs"
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
            echo "Output (first 30 lines):"
            echo "----------------------------------------"
            head -n 30 output.log
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
# EXISTING DATA STRUCTURES
# ================================================================================

echo "================================================================================"
echo "                     EXISTING DATA STRUCTURES"
echo "================================================================================"
echo ""

if [ -f "linkedlist.f90" ]; then
    compile_and_run "linkedlist.f90" "linkedlist_test" \
                    "Linked List - Singly and Doubly linked lists"
fi

if [ -f "hashtable.f90" ]; then
    compile_and_run "hashtable.f90" "hashtable_test" \
                    "Hash Table - Separate chaining hash table"
fi

# ================================================================================
# NEW DATA STRUCTURES
# ================================================================================

echo ""
echo "================================================================================"
echo "                      NEW DATA STRUCTURES"
echo "================================================================================"
echo ""

if [ -f "bst.f90" ]; then
    compile_and_run "bst.f90" "bst_test" \
                    "Binary Search Tree - Insert, Delete, Search, Traversals"
fi

if [ -f "stack.f90" ]; then
    compile_and_run "stack.f90" "stack_test" \
                    "Stack - Array-based and Linked-list with applications"
fi

if [ -f "queue.f90" ]; then
    compile_and_run "queue.f90" "queue_test" \
                    "Queue - Circular Queue, Linked Queue, Priority Queue, Deque"
fi

if [ -f "trie.f90" ]; then
    compile_and_run "trie.f90" "trie_test" \
                    "Trie (Prefix Tree) - Dictionary and auto-complete"
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
    echo "Data Structures Implemented:"
    echo "  1. Linked List (Singly & Doubly)"
    echo "  2. Hash Table (Separate Chaining)"
    echo "  3. Binary Search Tree (BST)"
    echo "  4. Stack (Array & Linked)"
    echo "  5. Queue (Array, Linked, Priority, Deque)"
    echo "  6. Trie (Prefix Tree)"
    echo ""
    exit 0
else
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════════════════════"
    echo "                 ⚠ SOME TESTS FAILED - CHECK OUTPUT ABOVE"
    echo "════════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    exit 1
fi
