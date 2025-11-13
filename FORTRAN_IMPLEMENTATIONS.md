# Fortran Algorithm Implementations

## 📘 Comprehensive Fortran Algorithm Collection

This document details all Fortran algorithm implementations in the Algorithms Multiverse repository. Fortran (Formula Translation) is one of the oldest programming languages, designed for numerical and scientific computing.

**Total Implementations**: 11 major algorithm files
**Lines of Code**: ~3,000+ lines of Modern Fortran (90/95/2003)
**Categories**: Sorting, Graph Theory, Dynamic Programming, String Processing, Numerical Methods

---

## 📊 Implementation Overview

| Category | Files | Lines | Algorithms | Status |
|----------|-------|-------|------------|--------|
| Sorting | 3 | ~600 | QuickSort, MergeSort, HeapSort | ✅ Complete |
| Graph Algorithms | 1 | ~260 | BFS, DFS, Dijkstra | ✅ Complete |
| Dynamic Programming | 1 | ~580 | 6 classic problems | ✅ Complete |
| String Algorithms | 1 | ~550 | 5 algorithms | ✅ Complete |
| Search Algorithms | 1 | ~500 | 6 search variants | ✅ Complete |
| Numerical Methods | 1 | ~500 | 5 numerical algorithms | ✅ Complete |
| Number Theory | 1 | ~300 | Existing | ✅ Complete |
| Computational Geometry | 1 | ~350 | Existing | ✅ Complete |

**Total**: 11 files, ~3,600 lines

---

## 🎯 Why Fortran?

### Historical Significance
- **First high-level language** (1957)
- **Dominated scientific computing** for decades
- **Still widely used** in physics, weather modeling, computational chemistry

### Modern Advantages
1. **Array Operations**: Native support for multi-dimensional arrays
2. **Performance**: Excellent compiler optimizations for mathematical code
3. **Numerical Stability**: IEEE 754 compliance, precise floating-point
4. **Legacy Code**: Massive libraries (LAPACK, BLAS, FFTW)
5. **Parallel Computing**: Built-in support for array operations

### Modern Fortran (90+)
- Free-form source code
- Modules and interfaces
- Dynamic memory allocation
- Recursion support
- Object-oriented features (F2003+)

---

## 📁 Detailed Implementation Guide

### 1. Sorting Algorithms

#### QuickSort (`sorting/quicksort.f90` - ~200 lines)

**Features:**
- Standard QuickSort with Lomuto partition
- Randomized pivot selection
- Performance benchmarking

**Compile & Run:**
```bash
gfortran -O2 -o quicksort sorting/quicksort.f90
./quicksort
```

**Key Fortran Features:**
- Recursive subroutines
- Array slicing
- Modern random number generation
- `cpu_time()` for performance measurement

**Example:**
```fortran
recursive subroutine quicksort_int(arr, left, right)
    integer, intent(inout) :: arr(:)
    integer, intent(in) :: left, right
    integer :: pivot_idx

    if (left < right) then
        pivot_idx = partition_int(arr, left, right)
        call quicksort_int(arr, left, pivot_idx - 1)
        call quicksort_int(arr, pivot_idx + 1, right)
    end if
end subroutine quicksort_int
```

#### MergeSort (`sorting/mergesort.f90` - ~180 lines)

**Features:**
- Top-down recursive implementation
- Stable sorting
- Array allocation/deallocation

**Key Fortran Features:**
- Allocatable arrays
- Array section assignments
- `allocate`/`deallocate`

#### HeapSort (`sorting/heapsort.f90` - ~220 lines)

**Features:**
- Max heap implementation
- Priority queue operations
- In-place sorting

**Key Fortran Features:**
- Module organization (can be extended)
- Complete binary heap in array
- Heapify operations

---

### 2. Graph Algorithms (`graph-algorithms/graph_algorithms.f90` - ~260 lines)

**Algorithms Implemented:**
1. **Breadth-First Search (BFS)**
   - Queue-based level-by-level traversal
   - Uses adjacency matrix

2. **Depth-First Search (DFS)**
   - Recursive depth-first exploration
   - Stack-based via recursion

3. **Dijkstra's Shortest Path**
   - Single-source shortest paths
   - Array-based priority queue
   - O(V²) implementation (simple, no heap)

**Graph Representation:**
- Adjacency matrix (better for Fortran)
- `INF` constant for no edges
- Dense representation

**Compile & Run:**
```bash
gfortran -O2 -o graph graph-algorithms/graph_algorithms.f90
./graph
```

**Fortran-Specific:**
```fortran
! Adjacency matrix initialization
graph = INF
do i = 1, n_vertices
    graph(i, i) = 0  ! Distance to self
end do

! Add weighted edge
graph(u, v) = weight
graph(v, u) = weight  ! Undirected
```

---

### 3. Dynamic Programming (`dynamic-programming/dp_algorithms.f90` - ~580 lines)

**Problems Implemented:**

1. **Fibonacci Sequence**
   - Memoization (top-down)
   - Tabulation (bottom-up)
   - Space-optimized O(1) space

2. **0/1 Knapsack Problem**
   - Dynamic programming table
   - O(nW) time complexity

3. **Longest Common Subsequence (LCS)**
   - String matching
   - O(mn) time

4. **Coin Change Problem**
   - Minimum coins needed
   - Greedy + DP hybrid

5. **Edit Distance (Levenshtein)**
   - String transformation
   - Insert/Delete/Replace operations

6. **Matrix Chain Multiplication**
   - Optimal parenthesization
   - O(n³) time

**Compile & Run:**
```bash
gfortran -O2 -o dp dynamic-programming/dp_algorithms.f90
./dp
```

**Key Implementation:**
```fortran
function fib_memo(n, memo) result(fib)
    integer, intent(in) :: n
    integer(8), intent(inout) :: memo(0:)
    integer(8) :: fib

    if (memo(n) /= -1) then
        fib = memo(n)
        return
    end if

    if (n <= 1) then
        fib = n
    else
        fib = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    end if

    memo(n) = fib
end function fib_memo
```

---

### 4. String Algorithms (`string-algorithms/string_algorithms.f90` - ~550 lines)

**Algorithms Implemented:**

1. **Naive Pattern Matching**
   - O(nm) brute force
   - Simple baseline

2. **KMP (Knuth-Morris-Pratt)**
   - O(n + m) optimal
   - Failure function preprocessing
   - No redundant comparisons

3. **Rabin-Karp**
   - Rolling hash technique
   - O(n + m) average case
   - Good for multiple pattern search

4. **Longest Palindromic Substring**
   - Expand around center
   - O(n²) time

5. **String Hashing**
   - Polynomial rolling hash
   - Fast string comparison

**Compile & Run:**
```bash
gfortran -O2 -o string string-algorithms/string_algorithms.f90
./string
```

**Fortran String Handling:**
```fortran
! Character variables
character(len=100) :: text, pattern

! String comparison
if (text(i:i) == pattern(j:j)) then
    ! Characters match
end if

! String length
n = len_trim(text)  ! Trimmed length
```

---

### 5. Advanced Search (`searching/advanced_search.f90` - ~500 lines)

**Search Algorithms:**

1. **Binary Search**
   - Iterative and recursive
   - O(log n)

2. **Interpolation Search**
   - O(log log n) for uniform data
   - Better than binary for certain distributions

3. **Jump Search**
   - O(√n)
   - Jump by √n blocks

4. **Exponential Search**
   - O(log n)
   - Good for unbounded arrays

5. **Ternary Search**
   - O(log₃ n)
   - For unimodal functions

6. **Fibonacci Search**
   - O(log n)
   - Avoids division (good for some hardware)

**Compile & Run:**
```bash
gfortran -O2 -o search searching/advanced_search.f90
./search
```

**Performance Comparison:**
All algorithms include performance benchmarking showing:
- Time taken for 10,000 searches
- Relative speedup compared to binary search

---

### 6. Numerical Algorithms (`numerical/numerical_algorithms.f90` - ~500 lines)

**Showcasing Fortran's Strength in Numerical Computing**

**Algorithms:**

1. **Root Finding**
   - Bisection Method: Guaranteed convergence
   - Newton-Raphson: Quadratic convergence
   - Secant Method: Super-linear convergence

2. **Numerical Integration**
   - Trapezoidal Rule: O(h²) accuracy
   - Simpson's Rule: O(h⁴) accuracy
   - Composite methods

3. **Matrix Operations**
   - Determinant calculation
   - Matrix-vector operations
   - Fortran's column-major storage

4. **Linear Systems**
   - Gaussian Elimination
   - Forward elimination + back substitution
   - O(n³) complexity

5. **Polynomial Evaluation**
   - Horner's Method: O(n) efficient evaluation
   - Numerically stable

**Compile & Run:**
```bash
gfortran -O2 -o numerical numerical/numerical_algorithms.f90
./numerical
```

**Example - Newton-Raphson:**
```fortran
function newton_raphson(x0, tol, iter) result(root)
    real(8), intent(in) :: x0, tol
    integer, intent(out) :: iter
    real(8) :: root, x_old, x_new

    x_old = x0
    iter = 0

    do
        iter = iter + 1
        x_new = x_old - f(x_old) / f_prime(x_old)

        if (abs(x_new - x_old) < tol) exit

        x_old = x_new
        if (iter > 100) exit
    end do

    root = x_new
end function newton_raphson
```

---

## 🔧 Build and Test

### Comprehensive Build Script

**File**: `build_fortran.sh`

```bash
chmod +x build_fortran.sh
./build_fortran.sh
```

**Features:**
- Checks for gfortran compiler
- Compiles all Fortran programs
- Runs each program with timeout
- Captures and displays output
- Color-coded success/failure
- Detailed test summary

**Expected Output:**
```
================================================================================
          FORTRAN ALGORITHMS - BUILD AND TEST SUITE
================================================================================

✓ Found gfortran: GNU Fortran (GCC) 11.2.0

================================================================================
                          SORTING ALGORITHMS
================================================================================

[1] QuickSort - O(n log n) average case sorting
Compiling... ✓ Success
Running...   ✓ Success

Output (first 20 lines):
----------------------------------------
===========================================================================
                    QUICKSORT IN FORTRAN
===========================================================================
...
```

---

## 📈 Performance Characteristics

### Sorting Algorithms

| Algorithm | Time Complexity | Space | Stable | In-Place |
|-----------|----------------|-------|--------|----------|
| QuickSort | O(n log n) avg | O(log n) | No | Yes |
| MergeSort | O(n log n) all | O(n) | Yes | No |
| HeapSort | O(n log n) all | O(1) | No | Yes |

### Graph Algorithms

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| BFS | O(V + E) | O(V) | Shortest path (unweighted) |
| DFS | O(V + E) | O(V) | Connectivity, cycles |
| Dijkstra | O(V²) | O(V) | Shortest path (weighted) |

*Note*: Dijkstra is O(V²) with array implementation, can be O((V+E) log V) with heap

---

## 💡 Fortran Programming Best Practices

### 1. Modern Fortran Style

**Use Modern Features:**
```fortran
! Good: Free-form modern Fortran
program my_program
    implicit none
    integer :: i, n = 100
    real(8), allocatable :: array(:)

    allocate(array(n))
    ! ... code ...
    deallocate(array)
end program my_program
```

**Avoid:**
```fortran
! Bad: Fixed-form FORTRAN 77
      PROGRAM MYPROG
      INTEGER I, N
      PARAMETER (N=100)
      REAL*8 ARRAY(N)
      ! ... code ...
      END
```

### 2. Intent Declarations

```fortran
subroutine process(input, output, work)
    real(8), intent(in) :: input(:)     ! Read-only
    real(8), intent(out) :: output(:)   ! Write-only
    real(8), intent(inout) :: work(:)   ! Read-write
```

### 3. Array Operations

```fortran
! Fortran excels at array operations
real(8) :: A(100), B(100), C(100)

! Vectorized operations (very efficient!)
C = A + B           ! Element-wise addition
C = A * B           ! Element-wise multiplication
C = sin(A)          ! Element-wise function

! Array slicing
C(1:50) = A(51:100) ! Copy second half to first half
```

### 4. Precision Control

```fortran
! Use kind parameters for portability
use iso_fortran_env, only: real64, int32

real(real64) :: x    ! 64-bit float
integer(int32) :: n  ! 32-bit integer

! Or define custom kinds
integer, parameter :: dp = selected_real_kind(15, 307)
real(dp) :: precise_value
```

---

## 🎓 Educational Value

### Learning Outcomes

**Algorithm Design:**
- Understand classic algorithms in a high-performance context
- See how algorithms map to mathematical notation
- Appreciate numerical stability considerations

**Fortran Proficiency:**
- Modern Fortran syntax (90/95/2003)
- Array-oriented programming
- Numerical computing best practices
- Performance optimization

**Scientific Computing:**
- Root finding and optimization
- Numerical integration
- Linear algebra
- Matrix computations

---

## 🔬 Real-World Applications

### Where Fortran is Used Today

1. **Weather Forecasting**
   - NOAA, ECMWF models
   - Atmospheric simulations

2. **Computational Chemistry**
   - Gaussian, GAMESS
   - Molecular dynamics

3. **Physics Simulations**
   - Particle physics (CERN)
   - Astrophysics

4. **Engineering**
   - Finite element analysis
   - Computational fluid dynamics

5. **High-Performance Computing**
   - Supercomputer applications
   - Large-scale simulations

---

## 📚 Fortran Language Features Demonstrated

### Core Features

- ✅ **Modules and Procedures**: Subroutines and functions
- ✅ **Recursive Procedures**: For divide-and-conquer algorithms
- ✅ **Dynamic Memory**: `allocate`/`deallocate`
- ✅ **Array Operations**: Native array syntax
- ✅ **Intent Specifications**: `in`, `out`, `inout`
- ✅ **Derived Types**: Can be extended for OOP

### Advanced Features

- ✅ **Precision Control**: `real(8)`, `integer(8)`
- ✅ **Array Slicing**: `arr(1:n:2)` for every other element
- ✅ **Intrinsic Functions**: `sqrt`, `sin`, `matmul`
- ✅ **Performance**: `cpu_time()` for benchmarking
- ✅ **String Handling**: Fixed and variable length

---

## 🚀 Quick Start

### Compile Single Program

```bash
gfortran -O2 -o program_name source_file.f90
./program_name
```

### Compile All Programs

```bash
chmod +x build_fortran.sh
./build_fortran.sh
```

### Optimization Flags

```bash
# Basic optimization
gfortran -O2 source.f90

# Aggressive optimization
gfortran -O3 -march=native source.f90

# With debugging
gfortran -g -Wall -Wextra -fbounds-check source.f90

# Profile-guided optimization
gfortran -O3 -fprofile-generate source.f90
./a.out
gfortran -O3 -fprofile-use source.f90
```

---

## 📊 Complexity Summary

### All Algorithms at a Glance

| Algorithm | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| **Sorting** |
| QuickSort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| MergeSort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| HeapSort | O(n log n) | O(n log n) | O(n log n) | O(1) |
| **Searching** |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) |
| Interpolation | O(1) | O(log log n) | O(n) | O(1) |
| Jump Search | O(1) | O(√n) | O(√n) | O(1) |
| **Graph** |
| BFS | O(V+E) | O(V+E) | O(V+E) | O(V) |
| DFS | O(V+E) | O(V+E) | O(V+E) | O(V) |
| Dijkstra | O(V²) | O(V²) | O(V²) | O(V) |
| **DP** |
| Fibonacci | O(n) | O(n) | O(n) | O(n) or O(1) |
| Knapsack | O(nW) | O(nW) | O(nW) | O(nW) |
| LCS | O(mn) | O(mn) | O(mn) | O(mn) |

---

## 🎯 Next Steps

### Extend These Implementations

1. **Add More Algorithms**
   - Red-Black Trees
   - AVL Trees
   - B-Trees in Fortran

2. **Parallel Computing**
   - OpenMP directives
   - Coarrays (Fortran 2008)
   - MPI integration

3. **Advanced Numerical Methods**
   - Runge-Kutta ODE solvers
   - Eigenvalue algorithms
   - Sparse matrix operations

4. **Interface with Libraries**
   - BLAS routines
   - LAPACK linear algebra
   - FFTW for FFT

---

## 📖 Resources

### Learning Fortran

- **Modern Fortran**: "Modern Fortran Explained" by Metcalf et al.
- **Numerical Recipes**: Classic numerical algorithms
- **Online**: fortran-lang.org

### Fortran Compilers

- **gfortran**: GNU Fortran (free, open-source)
- **ifort**: Intel Fortran (commercial, very fast)
- **flang**: LLVM-based (modern)

---

## ✅ Conclusion

This comprehensive Fortran implementation provides:

- **11 fully documented programs**
- **~3,600 lines of modern Fortran code**
- **40+ algorithms across 6 categories**
- **Complete with performance benchmarks**
- **Automated build and test infrastructure**
- **Educational comments and explanations**

**Perfect for:**
- Learning Modern Fortran
- Understanding algorithm implementation
- Scientific computing education
- Performance-critical applications
- Numerical methods study

---

**Status**: ✅ **COMPLETE**
**Last Updated**: November 2025
**Fortran Standard**: 90/95/2003
**Tested With**: gfortran 11.x
