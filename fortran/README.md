# Algorithms Multiverse - Fortran Implementation

A comprehensive collection of algorithms implemented in modern Fortran (2008/2018), featuring high-performance implementations with OpenMP parallelization support.

## Features

- **Modern Fortran**: Uses Fortran 2008/2018 features for clean, maintainable code
- **Comprehensive Coverage**: 50+ algorithms across multiple domains
- **Performance Optimized**: Includes parallel implementations using OpenMP
- **Generic Interfaces**: Type-generic programming for flexibility
- **Well-Tested**: Comprehensive test suite for all algorithms
- **Multiple Build Systems**: Supports both Make and CMake

## Algorithm Categories

### Sorting Algorithms
- Quick Sort (with parallel variant)
- Merge Sort
- Heap Sort
- Insertion Sort
- Bubble Sort
- Shell Sort
- Radix Sort
- Counting Sort
- Bucket Sort
- Tim Sort
- Intro Sort
- Selection Sort

### Searching Algorithms
- Binary Search
- Linear Search
- Jump Search
- Interpolation Search
- Exponential Search
- Ternary Search
- Fibonacci Search
- K-th Element Selection
- Two-Pointer Search
- Sliding Window Search

### Numerical Algorithms
- GCD/LCM
- Prime Checking & Generation
- Sieve of Eratosthenes
- Prime Factorization
- Factorial & Binomial Coefficients
- Fast Power & Modular Exponentiation
- Newton-Raphson Method
- Bisection Method
- Numerical Integration (Trapezoidal, Simpson's)
- Fast Fourier Transform (FFT)

### Matrix Operations
- Matrix Multiplication (Strassen's Algorithm)
- Matrix Transpose
- Matrix Inverse
- LU Decomposition
- QR Decomposition
- Cholesky Decomposition
- Gaussian Elimination
- Jacobi Iteration
- Gauss-Seidel Method
- Eigenvalue Computation
- Sparse Matrix Operations (CSR format)

### Dynamic Programming
- Fibonacci (DP variant)
- 0/1 Knapsack
- Longest Common Subsequence
- Edit Distance (Levenshtein)
- Matrix Chain Multiplication
- Coin Change
- Longest Increasing Subsequence
- Maximum Subarray (Kadane's)
- Rod Cutting
- Subset Sum
- Palindrome Partitioning
- Optimal Binary Search Tree
- Word Break

## Requirements

- Fortran compiler with F2008/F2018 support:
  - GNU Fortran (gfortran) >= 7.0
  - Intel Fortran Compiler (ifort) >= 18.0
  - Intel Fortran Compiler (ifx) >= 2021.1
- OpenMP support (optional, for parallelization)
- Build tools:
  - Make (for Makefile build)
  - CMake >= 3.10 (for CMake build)

## Building

### Using Make

```bash
# Build libraries (debug mode)
make

# Build in release mode
make BUILD_MODE=release

# Run tests
make test

# Build with specific compiler
make FC=ifort

# Install to system
make install PREFIX=/usr/local

# Show all available targets
make help
```

### Using CMake

```bash
# Configure build
mkdir build && cd build
cmake ..

# Build
cmake --build .

# Run tests
ctest

# Install
cmake --install .

# Configure with options
cmake .. -DCMAKE_BUILD_TYPE=Release \
         -DBUILD_TESTS=ON \
         -DBUILD_BENCHMARKS=ON \
         -DCMAKE_INSTALL_PREFIX=/usr/local
```

## Usage

### Basic Example

```fortran
program example
    use algorithms_multiverse
    implicit none

    integer(int32), dimension(10) :: arr = [3, 7, 1, 4, 6, 2, 9, 8, 5, 10]
    integer(int32) :: index

    ! Sort array using quicksort
    call quick_sort(arr)
    print *, "Sorted array:", arr

    ! Search for element
    index = binary_search(arr, 7)
    print *, "Found 7 at index:", index

    ! Calculate GCD
    print *, "GCD(48, 18) =", gcd(48_int64, 18_int64)

end program example
```

### Matrix Operations Example

```fortran
program matrix_example
    use algorithms_multiverse
    implicit none

    type(matrix_type) :: A, B, C
    real(real64), dimension(3,3) :: data_a, data_b

    ! Initialize matrices
    data_a = reshape([1.0, 2.0, 3.0, &
                     4.0, 5.0, 6.0, &
                     7.0, 8.0, 9.0], [3, 3])

    data_b = reshape([9.0, 8.0, 7.0, &
                     6.0, 5.0, 4.0, &
                     3.0, 2.0, 1.0], [3, 3])

    call A%init(data_a)
    call B%init(data_b)

    ! Matrix multiplication
    C = matrix_multiply(A, B)

    ! LU decomposition
    call lu_decomposition(A)

end program matrix_example
```

### Dynamic Programming Example

```fortran
program dp_example
    use algorithms_multiverse
    implicit none

    type(item_type), dimension(4) :: items
    integer(int32) :: max_value
    character(len=20) :: str1 = "ALGORITHM"
    character(len=20) :: str2 = "ALTRUISTIC"

    ! Knapsack problem
    items = [item_type(10, 60), &
             item_type(20, 100), &
             item_type(30, 120), &
             item_type(40, 140)]

    max_value = knapsack(items, 50)
    print *, "Maximum knapsack value:", max_value

    ! Longest common subsequence
    print *, "LCS length:", longest_common_subsequence(str1, str2)

    ! Edit distance
    print *, "Edit distance:", edit_distance(str1, str2)

end program dp_example
```

## Testing

The library includes comprehensive test suites:

```bash
# Run all tests
make test

# Run specific test category
./bin/test_runner sorting
./bin/test_runner searching
./bin/test_runner numerical
./bin/test_runner matrix
./bin/test_runner dp

# Run with coverage analysis
make coverage
```

## Benchmarking

Performance benchmarks are available:

```bash
# Build and run benchmarks
make benchmark

# Or with CMake
cmake --build . --target run_benchmarks
```

## Documentation

API documentation can be generated using FORD:

```bash
# Install FORD
pip install ford

# Generate documentation
ford ford.md
```

## Performance Considerations

- **Parallelization**: Many algorithms include OpenMP parallel variants for improved performance on multi-core systems
- **Cache Optimization**: Algorithms are implemented with cache-friendly memory access patterns
- **Compiler Optimization**: Use release mode (`-O3`) for production code
- **SIMD**: Modern compilers can auto-vectorize many loops with appropriate flags

## Compiler-Specific Optimizations

### GNU Fortran
```bash
gfortran -O3 -march=native -funroll-loops -fopenmp
```

### Intel Fortran
```bash
ifort -O3 -xHost -ipo -qopenmp
```

### Intel OneAPI Fortran
```bash
ifx -O3 -xHost -ipo -qopenmp
```

## Module Structure

```
fortran/
├── src/                          # Source files
│   ├── algorithms_multiverse.f90 # Main module
│   ├── sorting_module.f90       # Sorting algorithms
│   ├── searching_module.f90     # Searching algorithms
│   ├── numerical_module.f90     # Numerical algorithms
│   ├── matrix_module.f90        # Matrix operations
│   └── dynamic_programming_module.f90  # DP algorithms
├── tests/                        # Test files
│   ├── test_runner.f90
│   ├── test_sorting.f90
│   ├── test_searching.f90
│   ├── test_numerical.f90
│   ├── test_matrix.f90
│   ├── test_dynamic_programming.f90
│   └── benchmark.f90
├── examples/                     # Example programs
├── cmake/                        # CMake configuration
├── CMakeLists.txt               # CMake build file
├── Makefile                     # Make build file
└── README.md                    # This file
```

## Contributing

Contributions are welcome! Please ensure:
1. Code follows modern Fortran standards (F2008/F2018)
2. All algorithms include comprehensive tests
3. Performance-critical code includes benchmarks
4. Documentation is updated for new features

## License

This project is part of the Algorithms Multiverse collection. See the main repository LICENSE file for details.

## Acknowledgments

- Fortran community for continuous language modernization
- OpenMP for parallel computing support
- Contributors to numerical algorithms literature