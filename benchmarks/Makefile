# Makefile for Dijkstra Benchmark

CC = gcc
CFLAGS = -O3 -Wall -Wextra -std=c11
LDFLAGS = -lm

TARGET = compare_dijkstra
SOURCE = compare_dijkstra.c

# Default target
all: $(TARGET)

# Compile the benchmark
$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) -o $(TARGET) $(SOURCE) $(LDFLAGS)
	@echo "Build complete: ./$(TARGET)"

# Run comprehensive benchmark
run: $(TARGET)
	./$(TARGET)

# Run with custom graph (usage: make run-custom V=1000 E=50000)
run-custom: $(TARGET)
	./$(TARGET) $(V) $(E)

# Quick test with small graphs
test: $(TARGET)
	./$(TARGET) 100 1000

# Generate visualizations (requires Python with pandas, matplotlib, seaborn)
visualize: dijkstra_results.csv
	python3 visualize_results.py

# Clean build artifacts
clean:
	rm -f $(TARGET) $(TARGET).exe

# Clean all outputs
clean-all: clean
	rm -f dijkstra_results.csv dijkstra_trials.csv
	rm -rf plots/

# Run and visualize in one command
benchmark: run visualize

# Help message
help:
	@echo "Dijkstra Benchmark Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  make              - Build the benchmark executable"
	@echo "  make run          - Build and run comprehensive benchmark"
	@echo "  make test         - Run quick test with small graph"
	@echo "  make run-custom   - Run with custom graph (e.g., make run-custom V=1000 E=50000)"
	@echo "  make visualize    - Generate plots from results (requires Python)"
	@echo "  make benchmark    - Run benchmark and generate visualizations"
	@echo "  make clean        - Remove executable"
	@echo "  make clean-all    - Remove all generated files"
	@echo "  make help         - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make run                      - Run full benchmark suite"
	@echo "  make run-custom V=500 E=10000 - Test 500-vertex graph with 10k edges"
	@echo "  make benchmark                - Run and visualize in one step"

.PHONY: all run run-custom test visualize clean clean-all benchmark help
