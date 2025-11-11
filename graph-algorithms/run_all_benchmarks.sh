#!/bin/bash

################################################################################
# Cross-Language Benchmark Runner
# Runs graph algorithm benchmarks across multiple languages and aggregates results
################################################################################

set -e  # Exit on error

echo "================================================================================"
echo "Cross-Language Graph Algorithms Benchmark Suite"
echo "================================================================================"
echo ""

# Clean up old results
echo "Cleaning up old results..."
rm -f results_*.json
rm -rf benchmark_results
echo ""

# Counter for successful runs
SUCCESSFUL_RUNS=0
TOTAL_LANGUAGES=6

################################################################################
# Python
################################################################################
echo "================================================================================"
echo "[1/6] Running Python benchmarks..."
echo "================================================================================"
if command -v python3 &> /dev/null; then
    if python3 benchmark_py.py; then
        echo "✓ Python benchmarks completed successfully"
        ((SUCCESSFUL_RUNS++))
    else
        echo "✗ Python benchmarks failed"
    fi
    echo ""
else
    echo "✗ Python 3 not found, skipping Python benchmarks"
    echo ""
fi

################################################################################
# JavaScript
################################################################################
echo "================================================================================"
echo "[2/6] Running JavaScript benchmarks..."
echo "================================================================================"
if command -v node &> /dev/null; then
    if node benchmark_js.js; then
        echo "✓ JavaScript benchmarks completed successfully"
        ((SUCCESSFUL_RUNS++))
    else
        echo "✗ JavaScript benchmarks failed"
    fi
    echo ""
else
    echo "✗ Node.js not found, skipping JavaScript benchmarks"
    echo ""
fi

################################################################################
# Java
################################################################################
echo "================================================================================"
echo "[3/6] Running Java benchmarks..."
echo "================================================================================"
if command -v javac &> /dev/null && command -v java &> /dev/null; then
    echo "Compiling Java benchmark runner..."
    if javac BenchmarkJava.java 2>/dev/null; then
        if java BenchmarkJava; then
            echo "✓ Java benchmarks completed successfully"
            ((SUCCESSFUL_RUNS++))
        else
            echo "✗ Java benchmarks failed"
        fi
    else
        echo "✗ Java compilation failed"
        echo "Note: Java benchmark requires proper JSON library setup"
    fi
    echo ""
else
    echo "✗ Java not found, skipping Java benchmarks"
    echo ""
fi

################################################################################
# Go
################################################################################
echo "================================================================================"
echo "[4/6] Running Go benchmarks..."
echo "================================================================================"
if command -v go &> /dev/null; then
    if go run benchmark_go.go graph.go; then
        echo "✓ Go benchmarks completed successfully"
        ((SUCCESSFUL_RUNS++))
    else
        echo "✗ Go benchmarks failed"
    fi
    echo ""
else
    echo "✗ Go not found, skipping Go benchmarks"
    echo ""
fi

################################################################################
# C++
################################################################################
echo "================================================================================"
echo "[5/6] Running C++ benchmarks..."
echo "================================================================================"
if command -v g++ &> /dev/null; then
    echo "Compiling C++ benchmark runner..."
    if g++ -std=c++17 -O3 -o benchmark_cpp benchmark_cpp.cpp 2>/dev/null; then
        if ./benchmark_cpp; then
            echo "✓ C++ benchmarks completed successfully"
            ((SUCCESSFUL_RUNS++))
        else
            echo "✗ C++ benchmarks failed"
        fi
        # Clean up binary
        rm -f benchmark_cpp benchmark_cpp.exe
    else
        echo "✗ C++ compilation failed"
    fi
    echo ""
else
    echo "✗ g++ not found, skipping C++ benchmarks"
    echo ""
fi

################################################################################
# Rust
################################################################################
echo "================================================================================"
echo "[6/6] Running Rust benchmarks..."
echo "================================================================================"
if command -v cargo &> /dev/null; then
    echo "Note: Rust benchmark runner not yet implemented"
    echo "✗ Skipping Rust benchmarks"
    echo ""
else
    echo "✗ Cargo not found, skipping Rust benchmarks"
    echo ""
fi

################################################################################
# Results Aggregation
################################################################################
echo "================================================================================"
echo "Aggregating Results..."
echo "================================================================================"

# Count result files
RESULT_FILES=$(ls results_*.json 2>/dev/null | wc -l)

if [ "$RESULT_FILES" -eq 0 ]; then
    echo "✗ No benchmark results found!"
    echo ""
    echo "Please ensure at least one language runtime is installed:"
    echo "  - Python 3: https://www.python.org/"
    echo "  - Node.js: https://nodejs.org/"
    echo "  - Java JDK: https://adoptium.net/"
    echo "  - Go: https://go.dev/"
    echo "  - g++: Part of GCC (https://gcc.gnu.org/)"
    echo "  - Rust: https://www.rust-lang.org/"
    exit 1
fi

echo "Found $RESULT_FILES result file(s)"
echo ""

# Check if Python 3 and required packages are available
if command -v python3 &> /dev/null; then
    echo "Checking Python visualization dependencies..."

    # Check if required packages are installed
    if python3 -c "import pandas, matplotlib, seaborn" 2>/dev/null; then
        echo "Running aggregation and visualization..."
        if python3 aggregate_results.py; then
            echo ""
            echo "✓ Results aggregated and visualizations created successfully!"
        else
            echo ""
            echo "✗ Aggregation failed"
        fi
    else
        echo ""
        echo "⚠ Required Python packages not found"
        echo "Install with: pip install pandas matplotlib seaborn"
        echo ""
        echo "Skipping visualization, but benchmark results are available in results_*.json files"
    fi
else
    echo "⚠ Python 3 not available for result aggregation"
    echo ""
    echo "Benchmark results are available in results_*.json files"
fi

echo ""
echo "================================================================================"
echo "Benchmark Suite Complete"
echo "================================================================================"
echo "Languages run successfully: $SUCCESSFUL_RUNS/$TOTAL_LANGUAGES"
echo ""
echo "Result files:"
ls -lh results_*.json 2>/dev/null || echo "  (none)"
echo ""
echo "Visualizations:"
if [ -d "benchmark_results" ]; then
    ls -lh benchmark_results/*.png 2>/dev/null | head -5 || echo "  (none)"
    COUNT=$(ls benchmark_results/*.png 2>/dev/null | wc -l)
    if [ "$COUNT" -gt 5 ]; then
        echo "  ... and $((COUNT - 5)) more files"
    fi
else
    echo "  (none - install Python dependencies to generate visualizations)"
fi
echo ""
echo "================================================================================"
