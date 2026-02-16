# Makefile for Algorithms Multiverse - Fortran Implementation
# Supports gfortran, ifort, and other Fortran compilers

# Compiler selection
FC ?= gfortran

# Compiler-specific flags
ifeq ($(FC),gfortran)
    FFLAGS = -O3 -Wall -Wextra -std=f2018 -fcheck=all -fbacktrace
    FFLAGS_DEBUG = -g -O0 -Wall -Wextra -std=f2018 -fcheck=all -fbacktrace
    FFLAGS_RELEASE = -O3 -march=native -funroll-loops -std=f2018
    OPENMP_FLAG = -fopenmp
else ifeq ($(FC),ifort)
    FFLAGS = -O3 -warn all -std18 -check all -traceback
    FFLAGS_DEBUG = -g -O0 -warn all -std18 -check all -traceback
    FFLAGS_RELEASE = -O3 -xHost -ipo -std18
    OPENMP_FLAG = -qopenmp
else ifeq ($(FC),ifx)
    FFLAGS = -O3 -warn all -std18 -check all -traceback
    FFLAGS_DEBUG = -g -O0 -warn all -std18 -check all -traceback
    FFLAGS_RELEASE = -O3 -xHost -ipo -std18
    OPENMP_FLAG = -qopenmp
else
    FFLAGS = -O2
    FFLAGS_DEBUG = -g -O0
    FFLAGS_RELEASE = -O3
    OPENMP_FLAG = -fopenmp
endif

# Add OpenMP support
FFLAGS += $(OPENMP_FLAG)
FFLAGS_DEBUG += $(OPENMP_FLAG)
FFLAGS_RELEASE += $(OPENMP_FLAG)

# Directories
SRC_DIR = src
TEST_DIR = tests
BUILD_DIR = build
BIN_DIR = bin
LIB_DIR = lib
MOD_DIR = $(BUILD_DIR)/modules

# Source files
SOURCES = $(SRC_DIR)/sorting_module.f90 \
          $(SRC_DIR)/searching_module.f90 \
          $(SRC_DIR)/numerical_module.f90 \
          $(SRC_DIR)/matrix_module.f90 \
          $(SRC_DIR)/dynamic_programming_module.f90 \
          $(SRC_DIR)/graph_module.f90 \
          $(SRC_DIR)/string_module.f90 \
          $(SRC_DIR)/crypto_module.f90 \
          $(SRC_DIR)/geometry_module.f90 \
          $(SRC_DIR)/data_structures_module.f90 \
          $(SRC_DIR)/statistics_module.f90 \
          $(SRC_DIR)/optimization_module.f90 \
          $(SRC_DIR)/streaming_module.f90 \
          $(SRC_DIR)/algorithms_multiverse.f90

# Test files
TEST_SOURCES = $(TEST_DIR)/graph_module_test.f90 \
               $(TEST_DIR)/string_module_test.f90 \
               $(TEST_DIR)/crypto_module_test.f90 \
               $(TEST_DIR)/geometry_module_test.f90 \
               $(TEST_DIR)/data_structures_module_test.f90 \
               $(TEST_DIR)/statistics_module_test.f90 \
               $(TEST_DIR)/optimization_module_test.f90 \
               $(TEST_DIR)/streaming_module_test.f90 \
               $(TEST_DIR)/run_all_tests.f90

# Object files
OBJECTS = $(patsubst $(SRC_DIR)/%.f90,$(BUILD_DIR)/%.o,$(SOURCES))
TEST_OBJECTS = $(patsubst $(TEST_DIR)/%.f90,$(BUILD_DIR)/%.o,$(TEST_SOURCES))

# Module files
MODULES = $(patsubst $(SRC_DIR)/%.f90,$(MOD_DIR)/%.mod,$(SOURCES))

# Targets
LIBRARY = $(LIB_DIR)/libalgorithms_multiverse.a
SHARED_LIBRARY = $(LIB_DIR)/libalgorithms_multiverse.so
TEST_EXECUTABLE = $(BIN_DIR)/test_runner
EXAMPLE_EXECUTABLE = $(BIN_DIR)/example

# Build mode (debug/release)
BUILD_MODE ?= debug

ifeq ($(BUILD_MODE),release)
    FFLAGS := $(FFLAGS_RELEASE)
else
    FFLAGS := $(FFLAGS_DEBUG)
endif

# Default target
.PHONY: all
all: directories $(LIBRARY) $(SHARED_LIBRARY)

# Create necessary directories
.PHONY: directories
directories:
	@mkdir -p $(BUILD_DIR)
	@mkdir -p $(BIN_DIR)
	@mkdir -p $(LIB_DIR)
	@mkdir -p $(MOD_DIR)

# Static library
$(LIBRARY): $(OBJECTS)
	@echo "Creating static library: $@"
	ar rcs $@ $^

# Shared library
$(SHARED_LIBRARY): $(OBJECTS)
	@echo "Creating shared library: $@"
	$(FC) -shared -fPIC $(FFLAGS) -o $@ $^

# Compile source files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.f90 | directories
	@echo "Compiling: $<"
	$(FC) $(FFLAGS) -J$(MOD_DIR) -c $< -o $@

# Module dependencies
$(BUILD_DIR)/algorithms_multiverse.o: $(BUILD_DIR)/sorting_module.o \
                                      $(BUILD_DIR)/searching_module.o \
                                      $(BUILD_DIR)/numerical_module.o \
                                      $(BUILD_DIR)/matrix_module.o \
                                      $(BUILD_DIR)/dynamic_programming_module.o \
                                      $(BUILD_DIR)/graph_module.o \
                                      $(BUILD_DIR)/string_module.o \
                                      $(BUILD_DIR)/crypto_module.o \
                                      $(BUILD_DIR)/geometry_module.o \
                                      $(BUILD_DIR)/data_structures_module.o \
                                      $(BUILD_DIR)/statistics_module.o \
                                      $(BUILD_DIR)/optimization_module.o \
                                      $(BUILD_DIR)/streaming_module.o

# Test compilation
$(BUILD_DIR)/%.o: $(TEST_DIR)/%.f90 $(LIBRARY) | directories
	@echo "Compiling test: $<"
	$(FC) $(FFLAGS) -I$(MOD_DIR) -c $< -o $@

# Test executable
$(TEST_EXECUTABLE): $(TEST_OBJECTS) $(LIBRARY)
	@echo "Linking test executable: $@"
	$(FC) $(FFLAGS) -o $@ $(TEST_OBJECTS) -L$(LIB_DIR) -lalgorithms_multiverse

# Build tests
.PHONY: test
test: $(TEST_EXECUTABLE)
	@echo "Running tests..."
	@./$(TEST_EXECUTABLE)

# Build and run tests with coverage
.PHONY: coverage
coverage: FFLAGS += --coverage
coverage: clean test
	@echo "Generating coverage report..."
	@gcov $(SOURCES) -o $(BUILD_DIR)
	@lcov --capture --directory $(BUILD_DIR) --output-file coverage.info
	@genhtml coverage.info --output-directory coverage_report
	@echo "Coverage report generated in coverage_report/index.html"

# Benchmark
.PHONY: benchmark
benchmark: BUILD_MODE=release
benchmark: all
	@echo "Building benchmark executable..."
	$(FC) $(FFLAGS_RELEASE) -I$(MOD_DIR) $(TEST_DIR)/benchmark.f90 -o $(BIN_DIR)/benchmark \
	      -L$(LIB_DIR) -lalgorithms_multiverse
	@echo "Running benchmarks..."
	@./$(BIN_DIR)/benchmark

# Example program
.PHONY: example
example: all
	@echo "Building example program..."
	$(FC) $(FFLAGS) -I$(MOD_DIR) examples/example.f90 -o $(BIN_DIR)/example \
	      -L$(LIB_DIR) -lalgorithms_multiverse
	@echo "Running example..."
	@./$(BIN_DIR)/example

# Install
PREFIX ?= /usr/local
.PHONY: install
install: all
	@echo "Installing to $(PREFIX)..."
	@mkdir -p $(PREFIX)/lib
	@mkdir -p $(PREFIX)/include/algorithms_multiverse
	@cp $(LIBRARY) $(SHARED_LIBRARY) $(PREFIX)/lib/
	@cp $(MOD_DIR)/*.mod $(PREFIX)/include/algorithms_multiverse/
	@echo "Installation complete!"

# Uninstall
.PHONY: uninstall
uninstall:
	@echo "Uninstalling from $(PREFIX)..."
	@rm -f $(PREFIX)/lib/libalgorithms_multiverse.a
	@rm -f $(PREFIX)/lib/libalgorithms_multiverse.so
	@rm -rf $(PREFIX)/include/algorithms_multiverse
	@echo "Uninstallation complete!"

# Clean
.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf $(BUILD_DIR)
	@rm -rf $(BIN_DIR)
	@rm -rf $(LIB_DIR)
	@rm -f *.gcov *.gcda *.gcno
	@rm -rf coverage_report coverage.info
	@echo "Clean complete!"

# Help
.PHONY: help
help:
	@echo "Algorithms Multiverse - Fortran Implementation"
	@echo ""
	@echo "Available targets:"
	@echo "  all        - Build static and shared libraries (default)"
	@echo "  test       - Build and run tests"
	@echo "  benchmark  - Build and run benchmarks"
	@echo "  example    - Build and run example program"
	@echo "  coverage   - Run tests with coverage analysis"
	@echo "  install    - Install libraries and modules"
	@echo "  uninstall  - Remove installed files"
	@echo "  clean      - Remove all build artifacts"
	@echo "  help       - Show this help message"
	@echo ""
	@echo "Variables:"
	@echo "  FC         - Fortran compiler (default: gfortran)"
	@echo "  BUILD_MODE - Build mode: debug/release (default: debug)"
	@echo "  PREFIX     - Installation prefix (default: /usr/local)"
	@echo ""
	@echo "Examples:"
	@echo "  make                    - Build libraries in debug mode"
	@echo "  make BUILD_MODE=release - Build libraries in release mode"
	@echo "  make test              - Run tests"
	@echo "  make FC=ifort          - Build with Intel Fortran compiler"