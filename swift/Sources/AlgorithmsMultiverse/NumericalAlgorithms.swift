// Numerical Algorithms - Swift Implementation
// Mathematical, number theory, and numerical computation algorithms

import Foundation
import Accelerate  // For optimized numerical operations on Apple platforms

/// Namespace for numerical and mathematical algorithms
public enum NumericalAlgorithms {

    // MARK: - Basic Number Theory

    /// Calculate Greatest Common Divisor using Euclidean algorithm
    /// - Complexity: O(log(min(a,b))) time, O(1) space
    public static func gcd(_ a: Int, _ b: Int) -> Int {
        var x = abs(a)
        var y = abs(b)

        while y != 0 {
            let temp = y
            y = x % y
            x = temp
        }

        return x
    }

    /// Extended Euclidean algorithm
    /// Returns (gcd, x, y) such that ax + by = gcd(a,b)
    public static func extendedGCD(_ a: Int, _ b: Int) -> (gcd: Int, x: Int, y: Int) {
        if b == 0 {
            return (a, 1, 0)
        }

        let result = extendedGCD(b, a % b)
        let x = result.y
        let y = result.x - (a / b) * result.y

        return (result.gcd, x, y)
    }

    /// Calculate Least Common Multiple
    /// - Complexity: O(log(min(a,b))) time, O(1) space
    public static func lcm(_ a: Int, _ b: Int) -> Int {
        return abs(a * b) / gcd(a, b)
    }

    /// Check if number is prime using trial division
    /// - Complexity: O(√n) time, O(1) space
    public static func isPrime(_ n: Int) -> Bool {
        guard n > 1 else { return false }
        guard n > 3 else { return true }
        guard n % 2 != 0 && n % 3 != 0 else { return false }

        var i = 5
        while i * i <= n {
            if n % i == 0 || n % (i + 2) == 0 {
                return false
            }
            i += 6
        }

        return true
    }

    /// Miller-Rabin primality test (probabilistic)
    /// - Parameters:
    ///   - n: Number to test
    ///   - k: Number of rounds (higher = more accurate)
    /// - Complexity: O(k log³ n) time
    public static func millerRabinTest(_ n: Int, rounds k: Int = 5) -> Bool {
        guard n > 1 else { return false }
        guard n != 2 && n != 3 else { return true }
        guard n % 2 != 0 else { return false }

        // Write n-1 as 2^r * d
        var d = n - 1
        var r = 0
        while d % 2 == 0 {
            d /= 2
            r += 1
        }

        // Witness loop
        for _ in 0..<k {
            let a = 2 + Int.random(in: 0..<(n - 4))
            var x = modPow(a, d, n)

            if x == 1 || x == n - 1 {
                continue
            }

            var continueWitnessLoop = false
            for _ in 0..<r - 1 {
                x = modPow(x, 2, n)
                if x == n - 1 {
                    continueWitnessLoop = true
                    break
                }
            }

            if !continueWitnessLoop {
                return false
            }
        }

        return true
    }

    /// Sieve of Eratosthenes to find all primes up to n
    /// - Complexity: O(n log log n) time, O(n) space
    public static func sieveOfEratosthenes(_ n: Int) -> [Int] {
        guard n >= 2 else { return [] }

        var isPrime = Array(repeating: true, count: n + 1)
        isPrime[0] = false
        isPrime[1] = false

        for i in 2...Int(sqrt(Double(n))) {
            if isPrime[i] {
                for j in stride(from: i * i, through: n, by: i) {
                    isPrime[j] = false
                }
            }
        }

        return isPrime.enumerated().compactMap { $1 ? $0 : nil }
    }

    /// Prime factorization
    /// - Complexity: O(√n) time, O(log n) space
    public static func primeFactorization(_ n: Int) -> [(prime: Int, power: Int)] {
        var num = n
        var factors: [(Int, Int)] = []

        // Check for 2
        var count = 0
        while num % 2 == 0 {
            count += 1
            num /= 2
        }
        if count > 0 {
            factors.append((2, count))
        }

        // Check odd factors
        var i = 3
        while i * i <= num {
            count = 0
            while num % i == 0 {
                count += 1
                num /= i
            }
            if count > 0 {
                factors.append((i, count))
            }
            i += 2
        }

        // If num is still > 1, it's a prime factor
        if num > 1 {
            factors.append((num, 1))
        }

        return factors
    }

    /// Generate all divisors of n
    /// - Complexity: O(√n) time and space
    public static func divisors(_ n: Int) -> [Int] {
        var result: Set<Int> = []

        for i in 1...Int(sqrt(Double(n))) {
            if n % i == 0 {
                result.insert(i)
                result.insert(n / i)
            }
        }

        return result.sorted()
    }

    /// Euler's totient function φ(n)
    /// - Complexity: O(√n) time
    public static func eulerTotient(_ n: Int) -> Int {
        var result = n
        var num = n

        var p = 2
        while p * p <= num {
            if num % p == 0 {
                while num % p == 0 {
                    num /= p
                }
                result -= result / p
            }
            p += 1
        }

        if num > 1 {
            result -= result / num
        }

        return result
    }

    // MARK: - Modular Arithmetic

    /// Modular exponentiation: (base^exp) % mod
    /// - Complexity: O(log exp) time, O(1) space
    public static func modPow(_ base: Int, _ exp: Int, _ mod: Int) -> Int {
        var result = 1
        var base = base % mod
        var exp = exp

        while exp > 0 {
            if exp & 1 == 1 {
                result = (result * base) % mod
            }
            base = (base * base) % mod
            exp >>= 1
        }

        return result
    }

    /// Modular multiplicative inverse using Extended Euclidean
    /// - Returns: a^(-1) mod m, or nil if doesn't exist
    public static func modInverse(_ a: Int, _ m: Int) -> Int? {
        let (gcd, x, _) = extendedGCD(a, m)

        if gcd != 1 {
            return nil  // Inverse doesn't exist
        }

        return (x % m + m) % m
    }

    /// Chinese Remainder Theorem solver
    /// Finds x such that x ≡ a[i] (mod n[i]) for all i
    public static func chineseRemainderTheorem(remainders a: [Int], moduli n: [Int]) -> Int? {
        guard a.count == n.count else { return nil }

        let N = n.reduce(1, *)
        var x = 0

        for i in 0..<a.count {
            let Ni = N / n[i]
            guard let Mi = modInverse(Ni, n[i]) else { return nil }
            x += a[i] * Ni * Mi
        }

        return x % N
    }

    // MARK: - Combinatorics

    /// Calculate factorial
    /// - Complexity: O(n) time, O(1) space
    public static func factorial(_ n: Int) -> Int {
        guard n >= 0 else { return 0 }
        guard n <= 20 else { return Int.max }  // Overflow protection

        var result = 1
        for i in 2...n {
            result *= i
        }
        return result
    }

    /// Calculate nCr (n choose r) - binomial coefficient
    /// - Complexity: O(r) time, O(1) space
    public static func binomialCoefficient(_ n: Int, _ r: Int) -> Int {
        guard r >= 0 && r <= n else { return 0 }

        let r = min(r, n - r)  // Optimization
        var result = 1

        for i in 0..<r {
            result *= (n - i)
            result /= (i + 1)
        }

        return result
    }

    /// Generate Pascal's Triangle up to n rows
    /// - Complexity: O(n²) time and space
    public static func pascalsTriangle(_ n: Int) -> [[Int]] {
        guard n > 0 else { return [] }

        var triangle: [[Int]] = []

        for i in 0..<n {
            var row = Array(repeating: 1, count: i + 1)

            for j in 1..<i {
                row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
            }

            triangle.append(row)
        }

        return triangle
    }

    /// Calculate Catalan number
    /// - Complexity: O(n) time, O(1) space
    public static func catalanNumber(_ n: Int) -> Int {
        return binomialCoefficient(2 * n, n) / (n + 1)
    }

    // MARK: - Sequences

    /// Generate Fibonacci sequence up to n-th term
    /// - Complexity: O(n) time, O(1) space
    public static func fibonacci(_ n: Int) -> [Int] {
        guard n > 0 else { return [] }

        if n == 1 { return [0] }
        if n == 2 { return [0, 1] }

        var sequence = [0, 1]
        for _ in 2..<n {
            let next = sequence[sequence.count - 1] + sequence[sequence.count - 2]
            sequence.append(next)
        }

        return sequence
    }

    /// N-th Fibonacci number using matrix exponentiation
    /// - Complexity: O(log n) time
    public static func fibonacciMatrix(_ n: Int) -> Int {
        guard n > 0 else { return 0 }

        if n <= 2 {
            return n == 1 ? 0 : 1
        }

        let matrix = [[1, 1], [1, 0]]
        let result = matrixPower(matrix, n - 1)

        return result[0][0]
    }

    /// Matrix exponentiation
    private static func matrixPower(_ matrix: [[Int]], _ n: Int) -> [[Int]] {
        let size = matrix.count
        var result = Array(repeating: Array(repeating: 0, count: size), count: size)
        var base = matrix
        var exp = n

        // Initialize result as identity matrix
        for i in 0..<size {
            result[i][i] = 1
        }

        while exp > 0 {
            if exp & 1 == 1 {
                result = matrixMultiply(result, base)
            }
            base = matrixMultiply(base, base)
            exp >>= 1
        }

        return result
    }

    private static func matrixMultiply(_ a: [[Int]], _ b: [[Int]]) -> [[Int]] {
        let n = a.count
        var result = Array(repeating: Array(repeating: 0, count: n), count: n)

        for i in 0..<n {
            for j in 0..<n {
                for k in 0..<n {
                    result[i][j] += a[i][k] * b[k][j]
                }
            }
        }

        return result
    }

    // MARK: - Numerical Methods

    /// Find root using Newton-Raphson method
    /// - Parameters:
    ///   - f: Function to find root of
    ///   - df: Derivative of function
    ///   - x0: Initial guess
    ///   - tolerance: Convergence tolerance
    ///   - maxIterations: Maximum iterations
    /// - Complexity: O(iterations) time
    public static func newtonRaphson(
        f: (Double) -> Double,
        df: (Double) -> Double,
        initialGuess x0: Double,
        tolerance: Double = 1e-10,
        maxIterations: Int = 100
    ) -> Double? {
        var x = x0

        for _ in 0..<maxIterations {
            let fx = f(x)

            if abs(fx) < tolerance {
                return x
            }

            let dfx = df(x)
            if abs(dfx) < Double.ulpOfOne {
                return nil  // Derivative too small
            }

            x = x - fx / dfx
        }

        return nil  // Failed to converge
    }

    /// Find root using bisection method
    /// - Complexity: O(log((b-a)/tolerance)) time
    public static func bisectionMethod(
        f: (Double) -> Double,
        a: Double,
        b: Double,
        tolerance: Double = 1e-10,
        maxIterations: Int = 100
    ) -> Double? {
        var left = a
        var right = b

        // Check if root exists in interval
        if f(left) * f(right) > 0 {
            return nil
        }

        for _ in 0..<maxIterations {
            let mid = (left + right) / 2
            let fmid = f(mid)

            if abs(fmid) < tolerance || (right - left) / 2 < tolerance {
                return mid
            }

            if f(left) * fmid < 0 {
                right = mid
            } else {
                left = mid
            }
        }

        return (left + right) / 2
    }

    /// Numerical integration using Simpson's rule
    /// - Complexity: O(n) time
    public static func simpsonsRule(
        f: (Double) -> Double,
        a: Double,
        b: Double,
        n: Int = 1000
    ) -> Double {
        let n = n % 2 == 0 ? n : n + 1  // Ensure even number
        let h = (b - a) / Double(n)
        var sum = f(a) + f(b)

        for i in 1..<n {
            let x = a + Double(i) * h
            sum += (i % 2 == 0 ? 2 : 4) * f(x)
        }

        return h * sum / 3
    }

    /// Numerical integration using trapezoidal rule
    /// - Complexity: O(n) time
    public static func trapezoidalRule(
        f: (Double) -> Double,
        a: Double,
        b: Double,
        n: Int = 1000
    ) -> Double {
        let h = (b - a) / Double(n)
        var sum = (f(a) + f(b)) / 2

        for i in 1..<n {
            sum += f(a + Double(i) * h)
        }

        return h * sum
    }

    /// Find derivative numerically using central difference
    public static func numericalDerivative(
        f: (Double) -> Double,
        at x: Double,
        h: Double = 1e-5
    ) -> Double {
        return (f(x + h) - f(x - h)) / (2 * h)
    }

    // MARK: - Linear Algebra

    /// Gaussian elimination for solving Ax = b
    /// - Complexity: O(n³) time, O(n²) space
    public static func gaussianElimination(_ A: [[Double]], _ b: [Double]) -> [Double]? {
        let n = A.count
        guard n == A[0].count && n == b.count else { return nil }

        // Create augmented matrix
        var aug = A
        for i in 0..<n {
            aug[i].append(b[i])
        }

        // Forward elimination
        for i in 0..<n-1 {
            // Partial pivoting
            var maxRow = i
            for k in i+1..<n {
                if abs(aug[k][i]) > abs(aug[maxRow][i]) {
                    maxRow = k
                }
            }
            aug.swapAt(i, maxRow)

            // Check for zero diagonal
            if abs(aug[i][i]) < Double.ulpOfOne {
                return nil  // Singular matrix
            }

            // Eliminate below
            for j in i+1..<n {
                let factor = aug[j][i] / aug[i][i]
                for k in i..<n+1 {
                    aug[j][k] -= factor * aug[i][k]
                }
            }
        }

        // Back substitution
        var x = Array(repeating: 0.0, count: n)
        for i in stride(from: n-1, through: 0, by: -1) {
            x[i] = aug[i][n]
            for j in i+1..<n {
                x[i] -= aug[i][j] * x[j]
            }
            x[i] /= aug[i][i]
        }

        return x
    }

    /// LU decomposition of a matrix
    /// Returns (L, U, P) where PA = LU
    public static func luDecomposition(_ A: [[Double]]) -> (L: [[Double]], U: [[Double]], P: [[Double]])? {
        let n = A.count
        guard n == A[0].count else { return nil }

        var L = Array(repeating: Array(repeating: 0.0, count: n), count: n)
        var U = A
        var P = Array(repeating: Array(repeating: 0.0, count: n), count: n)

        // Initialize P as identity matrix
        for i in 0..<n {
            P[i][i] = 1.0
        }

        for i in 0..<n {
            // Pivoting
            var maxRow = i
            for k in i..<n {
                if abs(U[k][i]) > abs(U[maxRow][i]) {
                    maxRow = k
                }
            }

            U.swapAt(i, maxRow)
            P.swapAt(i, maxRow)

            if i > 0 {
                for k in 0..<i {
                    swap(&L[i][k], &L[maxRow][k])
                }
            }

            // Compute L and U
            for j in i..<n {
                L[j][i] = U[j][i] / U[i][i]
            }

            for j in i+1..<n {
                for k in i..<n {
                    U[j][k] -= L[j][i] * U[i][k]
                }
            }
        }

        return (L, U, P)
    }

    // MARK: - Fast Fourier Transform (FFT)

    /// Cooley-Tukey FFT algorithm
    /// - Complexity: O(n log n) time
    public static func fft(_ x: [Complex]) -> [Complex] {
        let n = x.count

        // Base case
        if n <= 1 {
            return x
        }

        // Ensure n is power of 2
        guard n & (n - 1) == 0 else {
            return []  // Not a power of 2
        }

        // Divide
        var even: [Complex] = []
        var odd: [Complex] = []

        for i in 0..<n {
            if i % 2 == 0 {
                even.append(x[i])
            } else {
                odd.append(x[i])
            }
        }

        // Conquer
        let evenFFT = fft(even)
        let oddFFT = fft(odd)

        // Combine
        var result = Array(repeating: Complex(0, 0), count: n)
        let half = n / 2

        for k in 0..<half {
            let angle = -2.0 * Double.pi * Double(k) / Double(n)
            let w = Complex(cos(angle), sin(angle))
            let t = w * oddFFT[k]
            result[k] = evenFFT[k] + t
            result[k + half] = evenFFT[k] - t
        }

        return result
    }

    /// Complex number structure for FFT
    public struct Complex {
        public let real: Double
        public let imag: Double

        public init(_ real: Double, _ imag: Double) {
            self.real = real
            self.imag = imag
        }

        static func + (lhs: Complex, rhs: Complex) -> Complex {
            return Complex(lhs.real + rhs.real, lhs.imag + rhs.imag)
        }

        static func - (lhs: Complex, rhs: Complex) -> Complex {
            return Complex(lhs.real - rhs.real, lhs.imag - rhs.imag)
        }

        static func * (lhs: Complex, rhs: Complex) -> Complex {
            return Complex(
                lhs.real * rhs.real - lhs.imag * rhs.imag,
                lhs.real * rhs.imag + lhs.imag * rhs.real
            )
        }

        public var magnitude: Double {
            return sqrt(real * real + imag * imag)
        }

        public var phase: Double {
            return atan2(imag, real)
        }
    }
}