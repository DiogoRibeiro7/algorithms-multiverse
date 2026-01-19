# Makefile for Algorithms Multiverse - C Implementation
# Supports gcc, clang, and MSVC compilers

# Compiler selection
CC ?= gcc
AR = ar
RANLIB = ranlib

# Detect OS
UNAME_S := $(shell uname -s 2>/dev/null || echo Windows)
ifeq ($(UNAME_S),Linux)
    OS := Linux
else ifeq ($(UNAME_S),Darwin)
    OS := macOS
else
    OS := Windows
endif

# Compiler flags
CFLAGS_BASE = -Wall -Wextra -std=c11 -Iinclude
CFLAGS_DEBUG = -g -O0 -DDEBUG -fsanitize=address -fsanitize=undefined
CFLAGS_RELEASE = -O3 -DNDEBUG -march=native
CFLAGS_PROF = -O2 -pg -DPROFILE

# OpenMP support
ifeq ($(CC),gcc)
    OPENMP_FLAG = -fopenmp
else ifeq ($(CC),clang)
    OPENMP_FLAG = -fopenmp
else ifeq ($(CC),icc)
    OPENMP_FLAG = -qopenmp
else
    OPENMP_FLAG =
endif

# Math library
LDFLAGS = -lm
ifeq ($(OS),Linux)
    LDFLAGS += -lrt -lpthread
else ifeq ($(OS),macOS)
    LDFLAGS += -lpthread
endif

# Build mode (debug/release/profile)
BUILD_MODE ?= debug

ifeq ($(BUILD_MODE),release)
    CFLAGS = $(CFLAGS_BASE) $(CFLAGS_RELEASE) $(OPENMP_FLAG)
else ifeq ($(BUILD_MODE),profile)
    CFLAGS = $(CFLAGS_BASE) $(CFLAGS_PROF) $(OPENMP_FLAG)
else
    CFLAGS = $(CFLAGS_BASE) $(CFLAGS_DEBUG) $(OPENMP_FLAG)
endif

# Directories
SRC_DIR = src
INC_DIR = include
BUILD_DIR = build
LIB_DIR = lib
BIN_DIR = bin
TEST_DIR = tests
EXAMPLE_DIR = examples
DOC_DIR = docs

# Source files (grouped by module)
SORTING_SRCS = $(SRC_DIR)/sorting.c
SEARCHING_SRCS = $(SRC_DIR)/searching.c
DATA_STRUCTURES_SRCS = $(SRC_DIR)/stack.c \
                       $(SRC_DIR)/queue.c \
                       $(SRC_DIR)/linked_list.c
GRAPH_SRCS = $(SRC_DIR)/graph.c
STRING_SRCS = $(SRC_DIR)/string_algorithms.c
NUMERICAL_SRCS = $(SRC_DIR)/numerical.c
DP_SRCS = $(SRC_DIR)/dynamic_programming.c
MATRIX_SRCS = $(SRC_DIR)/matrix.c
UTILS_SRCS = $(SRC_DIR)/algorithms_multiverse.c

# All source files
SRCS = $(SORTING_SRCS) $(SEARCHING_SRCS) $(DATA_STRUCTURES_SRCS) \
       $(GRAPH_SRCS) $(STRING_SRCS) $(NUMERICAL_SRCS) $(DP_SRCS) \
       $(MATRIX_SRCS) $(UTILS_SRCS)

# Object files
OBJS = $(SRCS:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)

# Test files
TEST_SRCS = $(wildcard $(TEST_DIR)/*.c)
TEST_BINS = $(TEST_SRCS:$(TEST_DIR)/%.c=$(BIN_DIR)/test_%)

# Example files
EXAMPLE_SRCS = $(wildcard $(EXAMPLE_DIR)/*.c)
EXAMPLE_BINS = $(EXAMPLE_SRCS:$(EXAMPLE_DIR)/%.c=$(BIN_DIR)/example_%)

# Library targets
STATIC_LIB = $(LIB_DIR)/libalgorithms_multiverse.a
SHARED_LIB = $(LIB_DIR)/libalgorithms_multiverse.so
ifeq ($(OS),macOS)
    SHARED_LIB = $(LIB_DIR)/libalgorithms_multiverse.dylib
else ifeq ($(OS),Windows)
    SHARED_LIB = $(LIB_DIR)/algorithms_multiverse.dll
endif

# Default target
.PHONY: all
all: directories $(STATIC_LIB) $(SHARED_LIB)

# Create necessary directories
.PHONY: directories
directories:
	@mkdir -p $(BUILD_DIR)
	@mkdir -p $(LIB_DIR)
	@mkdir -p $(BIN_DIR)

# Compile source files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@echo "Compiling $<..."
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

# Build static library
$(STATIC_LIB): $(OBJS)
	@echo "Creating static library $@..."
	$(AR) rcs $@ $^
	$(RANLIB) $@

# Build shared library
$(SHARED_LIB): $(OBJS)
	@echo "Creating shared library $@..."
ifeq ($(OS),macOS)
	$(CC) -dynamiclib -o $@ $^ $(LDFLAGS)
else
	$(CC) -shared -o $@ $^ $(LDFLAGS)
endif

# Build tests
.PHONY: test
test: $(TEST_BINS)
	@echo "Running tests..."
	@for test in $(TEST_BINS); do \
		echo "Running $$test..."; \
		$$test || exit 1; \
	done
	@echo "All tests passed!"

$(BIN_DIR)/test_%: $(TEST_DIR)/%.c $(STATIC_LIB)
	@echo "Building test $@..."
	$(CC) $(CFLAGS) $< -o $@ -L$(LIB_DIR) -lalgorithms_multiverse $(LDFLAGS)

# Build examples
.PHONY: examples
examples: $(EXAMPLE_BINS)

$(BIN_DIR)/example_%: $(EXAMPLE_DIR)/%.c $(STATIC_LIB)
	@echo "Building example $@..."
	$(CC) $(CFLAGS) $< -o $@ -L$(LIB_DIR) -lalgorithms_multiverse $(LDFLAGS)

# Run specific test
.PHONY: test-%
test-%: $(BIN_DIR)/test_%
	@echo "Running test $<..."
	$<

# Run specific example
.PHONY: example-%
example-%: $(BIN_DIR)/example_%
	@echo "Running example $<..."
	$<

# Benchmark
.PHONY: benchmark
benchmark: BUILD_MODE=release
benchmark: $(BIN_DIR)/benchmark
	@echo "Running benchmarks..."
	$(BIN_DIR)/benchmark

$(BIN_DIR)/benchmark: $(TEST_DIR)/benchmark.c $(STATIC_LIB)
	@echo "Building benchmark..."
	$(CC) $(CFLAGS) $< -o $@ -L$(LIB_DIR) -lalgorithms_multiverse $(LDFLAGS)

# Code coverage
.PHONY: coverage
coverage: CFLAGS += --coverage
coverage: LDFLAGS += --coverage
coverage: clean test
	@echo "Generating coverage report..."
	@gcov $(SRCS) -o $(BUILD_DIR)
	@lcov --capture --directory $(BUILD_DIR) --output-file coverage.info
	@genhtml coverage.info --output-directory coverage_report
	@echo "Coverage report generated in coverage_report/index.html"

# Static analysis
.PHONY: analyze
analyze:
	@echo "Running static analysis..."
	@which cppcheck > /dev/null && cppcheck --enable=all --suppress=missingIncludeSystem $(SRC_DIR) $(INC_DIR) || echo "cppcheck not found"
	@which clang-tidy > /dev/null && clang-tidy $(SRCS) -- $(CFLAGS) || echo "clang-tidy not found"
	@which pvs-studio-analyzer > /dev/null && pvs-studio-analyzer analyze -o pvs.log && plog-converter -a GA:1,2 -t errorfile pvs.log || echo "PVS-Studio not found"

# Format code
.PHONY: format
format:
	@echo "Formatting code..."
	@which clang-format > /dev/null && clang-format -i $(SRCS) $(INC_DIR)/*.h || echo "clang-format not found"

# Generate documentation
.PHONY: docs
docs:
	@echo "Generating documentation..."
	@which doxygen > /dev/null && doxygen Doxyfile || echo "doxygen not found"

# Install
PREFIX ?= /usr/local
.PHONY: install
install: all
	@echo "Installing to $(PREFIX)..."
	@mkdir -p $(PREFIX)/lib
	@mkdir -p $(PREFIX)/include/algorithms_multiverse
	@cp $(STATIC_LIB) $(SHARED_LIB) $(PREFIX)/lib/
	@cp $(INC_DIR)/*.h $(PREFIX)/include/algorithms_multiverse/
	@echo "Installation complete!"

# Uninstall
.PHONY: uninstall
uninstall:
	@echo "Uninstalling from $(PREFIX)..."
	@rm -f $(PREFIX)/lib/libalgorithms_multiverse.*
	@rm -rf $(PREFIX)/include/algorithms_multiverse
	@echo "Uninstallation complete!"

# Clean
.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf $(BUILD_DIR)
	@rm -rf $(LIB_DIR)
	@rm -rf $(BIN_DIR)
	@rm -f *.gcov *.gcda *.gcno
	@rm -rf coverage_report coverage.info
	@rm -f pvs.log
	@echo "Clean complete!"

# Help
.PHONY: help
help:
	@echo "Algorithms Multiverse - C Implementation"
	@echo ""
	@echo "Available targets:"
	@echo "  all        - Build static and shared libraries (default)"
	@echo "  test       - Build and run all tests"
	@echo "  examples   - Build all examples"
	@echo "  benchmark  - Build and run benchmarks"
	@echo "  coverage   - Generate code coverage report"
	@echo "  analyze    - Run static analysis tools"
	@echo "  format     - Format source code"
	@echo "  docs       - Generate documentation"
	@echo "  install    - Install libraries and headers"
	@echo "  uninstall  - Remove installed files"
	@echo "  clean      - Remove all build artifacts"
	@echo "  help       - Show this help message"
	@echo ""
	@echo "Variables:"
	@echo "  CC         - C compiler (default: gcc)"
	@echo "  BUILD_MODE - Build mode: debug/release/profile (default: debug)"
	@echo "  PREFIX     - Installation prefix (default: /usr/local)"
	@echo ""
	@echo "Examples:"
	@echo "  make                    - Build libraries in debug mode"
	@echo "  make BUILD_MODE=release - Build libraries in release mode"
	@echo "  make test              - Run all tests"
	@echo "  make test-sorting      - Run sorting tests"
	@echo "  make example-graph     - Run graph example"

# Dependency generation
-include $(OBJS:.o=.d)

$(BUILD_DIR)/%.d: $(SRC_DIR)/%.c
	@mkdir -p $(dir $@)
	@$(CC) -MM $(CFLAGS) $< | sed 's,\($*\)\.o[ :]*,$(BUILD_DIR)/\1.o $@ : ,g' > $@