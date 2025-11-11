# Number Theory Algorithms

A comprehensive collection of fundamental number theory algorithms implemented in multiple programming languages with a focus on correctness, performance, and educational value.

## Overview

Number theory is a branch of pure mathematics devoted to the study of integers and integer-valued functions. These algorithms form the foundation of modern cryptography, hashing, and many computer science applications.

## Algorithms Implemented

### 1. Prime Number Generation
- **Sieve of Eratosthenes**: Ancient algorithm for finding all primes up to a limit
  - Time Complexity: O(n log log n)
  - Space Complexity: O(n)
  - Optimal for generating multiple primes

- **Sieve of Sundaram**: Alternative sieve algorithm
  - Time Complexity: O(n log n)
  - Generates odd primes efficiently

### 2. Prime Factorization
- Trial division with optimizations
- Applications: Cryptography, simplifying fractions
- Time Complexity: O(√n)

### 3. Greatest Common Divisor (GCD)
- **Euclidean Algorithm**: Classical recursive/iterative approach
  - Time Complexity: O(log min(a,b))
  - Foundation for Extended Euclidean Algorithm
- **Extended GCD**: Returns GCD and Bézout coefficients
  - Used in modular multiplicative inverse

### 4. Modular Arithmetic Operations
- Modular addition, subtraction, multiplication
- Modular multiplicative inverse
- Applications: Cryptographic protocols

### 5. Fast Exponentiation (Modular Exponentiation)
- **Binary Exponentiation**: Also known as exponentiation by squaring
  - Time Complexity: O(log n)
  - Space Complexity: O(1)
  - Critical for RSA encryption/decryption
  - Prevents integer overflow in modular operations

### 6. Chinese Remainder Theorem (CRT)
- Solves systems of congruences
- Applications: RSA optimization, calendar calculations
- Time Complexity: O(n log n)

### 7. Miller-Rabin Primality Test
- Probabilistic primality testing algorithm
- Time Complexity: O(k log³ n) for k rounds
- Accuracy: Error probability ≤ 4⁻ᵏ
- Used for large prime testing in cryptography

### 8. Pollard's Rho Algorithm
- Integer factorization algorithm
- Time Complexity: O(n^(1/4)) expected
- Efficient for finding small factors of large numbers
- Applications: Breaking weak RSA keys

## Language Implementations

### Python (`number_theory.py`, `advanced_number_theory.py`)
- Full implementation with all algorithms
- Uses arbitrary precision integers (native)
- Includes detailed docstrings and mathematical proofs
- Cryptographic random numbers for Miller-Rabin

### C (`number_theory.c`)
- High-performance implementation
- Uses `unsigned long long` for big integers
- Optimized with compiler hints
- Manual memory management for arrays

### Go (`number_theory.go`)
- Idiomatic Go implementation
- Uses `big.Int` for arbitrary precision
- Concurrent versions of some algorithms
- Clean error handling

### Rust (`number_theory.rs`)
- Memory-safe implementation
- Uses `num-bigint` crate for big integers
- Zero-cost abstractions
- Comprehensive unit tests

### Fortran (`number_theory.f90`)
- Modern Fortran 90+ implementation
- Optimized for numerical computing
- Array operations and intrinsic functions
- Scientific computing focus

### COBOL (`number_theory.cob`)
- Enterprise-grade implementation
- Fixed-point arithmetic
- Detailed procedure divisions
- Business computing applications

### R (`number_theory.R`)
- Statistical computing focus
- Vectorized operations where possible
- Integration with `gmp` package for big integers
- Data analysis applications

## Features

### Big Integer Support
- **Python**: Native arbitrary precision
- **Go**: `math/big` package
- **Rust**: `num-bigint` crate
- **R**: `gmp` package
- **C/Fortran/COBOL**: Limited to native types (64-bit)

### Cryptographic Applications
- RSA encryption/decryption building blocks
- Diffie-Hellman key exchange components
- Digital signature algorithms
- Hash function implementations

### Performance Optimizations
- Cache-friendly sieve implementations
- Early termination conditions
- Bit manipulation tricks
- Compiler optimizations

### Mathematical Proofs
Each implementation includes:
- Algorithm correctness proofs in comments
- Time and space complexity analysis
- Mathematical foundations
- Edge case handling explanations

## Usage Examples

### Python
```python
from number_theory import *

# Generate primes up to 1000
primes = sieve_of_eratosthenes(1000)

# Find GCD
gcd_result = gcd(48, 18)  # Returns 6

# Modular exponentiation (for RSA)
result = mod_exp(base=3, exp=1000, mod=13)

# Miller-Rabin primality test
is_prime = miller_rabin(561, k=5)  # Tests if 561 is prime
```

### Go
```go
import "algorithms/number-theory"

// Generate primes
primes := SieveOfEratosthenes(1000)

// Fast exponentiation with big integers
base := big.NewInt(2)
exp := big.NewInt(1000)
mod := big.NewInt(1000000007)
result := ModExp(base, exp, mod)
```

### Rust
```rust
use number_theory::*;

// Sieve of Eratosthenes
let primes = sieve_of_eratosthenes(1000);

// Miller-Rabin test
let is_prime = miller_rabin(561, 5);
```

## Building and Running

### Python
```bash
python number_theory.py
python advanced_number_theory.py
```

### C
```bash
gcc -O3 -o number_theory number_theory.c -lm
./number_theory
```

### Go
```bash
go run number_theory.go
```

### Rust
```bash
rustc number_theory.rs
./number_theory
# Or with Cargo:
cargo run --release
```

### Fortran
```bash
gfortran -O3 -o number_theory number_theory.f90
./number_theory
```

### COBOL
```bash
cobc -x -free number_theory.cob
./number_theory
```

### R
```bash
Rscript number_theory.R
```

## Benchmarking

Each implementation includes benchmarking code that compares:
- Algorithm performance against built-in functions
- Scaling behavior with input size
- Memory usage patterns
- Accuracy validation

Run `benchmark.py` for comprehensive performance analysis across all implementations.

## Applications in Computer Science

### Cryptography
- **RSA**: Relies on modular exponentiation, prime generation, and GCD
- **Diffie-Hellman**: Uses modular exponentiation
- **Digital Signatures**: Built on number theory primitives

### Hashing
- Modular arithmetic in hash function design
- Prime numbers for hash table sizing
- Collision resolution strategies

### Algorithms
- Randomized algorithms use primality testing
- Graph algorithms use GCD for cycle detection
- Dynamic programming with modular arithmetic

### Computational Number Theory
- Testing conjectures (Goldbach, twin primes)
- Finding large primes (Mersenne primes)
- Integer factorization challenges

## Mathematical Foundations

### Euclidean Algorithm Proof
The algorithm is based on: gcd(a,b) = gcd(b, a mod b)
- **Base case**: gcd(a, 0) = a
- **Inductive step**: Any common divisor of a and b also divides a mod b
- **Termination**: Each step reduces the problem size

### Fermat's Little Theorem
If p is prime and a is not divisible by p, then: a^(p-1) ≡ 1 (mod p)
- Foundation for Miller-Rabin test
- Used in modular inverse calculation

### Chinese Remainder Theorem
Given pairwise coprime moduli m₁, m₂, ..., mₖ and remainders a₁, a₂, ..., aₖ,
there exists unique solution x (mod M) where M = m₁ × m₂ × ... × mₖ

## Performance Notes

### Sieve of Eratosthenes
- Best for finding all primes up to n
- Memory intensive for large n (>10⁹)
- Optimizations: Odd-only sieve, segmented sieve

### Miller-Rabin
- Deterministic for n < 2⁶⁴ with specific witness set
- Probabilistic for larger n (use k ≥ 20 for high confidence)
- Much faster than trial division for large numbers

### Pollard's Rho
- Expected O(n^(1/4)) but can fail
- Best for semi-primes with factors of similar size
- Use multiple starting values if first attempt fails

## Testing

Each implementation includes:
- Unit tests for correctness
- Edge case testing (0, 1, primes, composites)
- Large input testing
- Cross-language verification

## References

- *Introduction to Algorithms* (CLRS), Chapter 31: Number-Theoretic Algorithms
- *The Art of Computer Programming*, Volume 2: Seminumerical Algorithms (Knuth)
- *A Computational Introduction to Number Theory and Algebra* (Shoup)
- *Prime Numbers: A Computational Perspective* (Crandall & Pomerance)

## License

Part of the algorithms-multiverse repository. See root LICENSE file.

## Contributing

When adding new algorithms or optimizations:
1. Include mathematical proof or correctness argument
2. Add comprehensive test cases
3. Benchmark against existing implementations
4. Update this README with complexity analysis
