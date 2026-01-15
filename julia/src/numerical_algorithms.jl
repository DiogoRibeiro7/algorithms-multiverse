"""
    NumericalAlgorithms

Module containing numerical and mathematical algorithms implemented in Julia.
"""
module NumericalAlgorithms

using LinearAlgebra

export gcd, lcm, sieve_of_eratosthenes, is_prime, prime_factors,
       power_mod, fibonacci_matrix, matrix_multiply, matrix_power,
       binary_exponentiation, newton_raphson, bisection_method,
       trapezoidal_integration, simpsons_rule, gaussian_elimination

"""
    gcd(a::Int, b::Int)

Calculate greatest common divisor using Euclidean algorithm.
Time: O(log(min(a,b)))
"""
function gcd(a::Int, b::Int)
    while b != 0
        a, b = b, a % b
    end
    return abs(a)
end

"""
    lcm(a::Int, b::Int)

Calculate least common multiple.
"""
function lcm(a::Int, b::Int)
    return abs(a * b) ÷ gcd(a, b)
end

"""
    sieve_of_eratosthenes(n::Int)

Generate all prime numbers up to n.
Time: O(n log log n), Space: O(n)
"""
function sieve_of_eratosthenes(n::Int)
    if n < 2
        return Int[]
    end

    is_prime = trues(n)
    is_prime[1] = false

    for i in 2:Int(floor(sqrt(n)))
        if is_prime[i]
            for j in i*i:i:n
                is_prime[j] = false
            end
        end
    end

    return findall(is_prime)
end

"""
    is_prime(n::Int)

Check if n is prime using trial division.
Time: O(√n)
"""
function is_prime(n::Int)
    if n < 2
        return false
    end
    if n == 2
        return true
    end
    if n % 2 == 0
        return false
    end

    for i in 3:2:Int(floor(sqrt(n)))
        if n % i == 0
            return false
        end
    end

    return true
end

"""
    prime_factors(n::Int)

Find prime factorization of n.
Time: O(√n)
"""
function prime_factors(n::Int)
    factors = Tuple{Int, Int}[]
    d = 2

    while d * d <= n
        count = 0
        while n % d == 0
            count += 1
            n ÷= d
        end
        if count > 0
            push!(factors, (d, count))
        end
        d += (d == 2) ? 1 : 2
    end

    if n > 1
        push!(factors, (n, 1))
    end

    return factors
end

"""
    power_mod(base::Int, exp::Int, mod::Int)

Calculate (base^exp) % mod efficiently.
Time: O(log exp)
"""
function power_mod(base::Int, exp::Int, mod::Int)
    result = 1
    base %= mod

    while exp > 0
        if exp & 1 == 1
            result = (result * base) % mod
        end
        base = (base * base) % mod
        exp >>= 1
    end

    return result
end

"""
    fibonacci_matrix(n::Int)

Calculate n-th Fibonacci number using matrix exponentiation.
Time: O(log n)
"""
function fibonacci_matrix(n::Int)
    if n <= 1
        return n
    end

    F = [1 1; 1 0]
    result = matrix_power(F, n - 1)

    return result[1, 1]
end

"""
    matrix_power(A::Matrix, n::Int)

Calculate matrix A raised to power n.
Time: O(m³ log n) where m is matrix dimension
"""
function matrix_power(A::Matrix, n::Int)
    m = size(A, 1)
    result = Matrix{eltype(A)}(I, m, m)

    while n > 0
        if n & 1 == 1
            result = result * A
        end
        A = A * A
        n >>= 1
    end

    return result
end

"""
    binary_exponentiation(base::T, exp::Int) where T

Calculate base^exp using binary exponentiation.
Time: O(log exp)
"""
function binary_exponentiation(base::T, exp::Int) where T
    result = one(T)

    while exp > 0
        if exp & 1 == 1
            result *= base
        end
        base *= base
        exp >>= 1
    end

    return result
end

"""
    newton_raphson(f::Function, df::Function, x0::Float64; tol::Float64=1e-10, max_iter::Int=100)

Find root using Newton-Raphson method.
"""
function newton_raphson(f::Function, df::Function, x0::Float64;
                        tol::Float64=1e-10, max_iter::Int=100)
    x = x0

    for _ in 1:max_iter
        fx = f(x)
        if abs(fx) < tol
            return x
        end

        dfx = df(x)
        if abs(dfx) < eps()
            error("Derivative too small")
        end

        x = x - fx / dfx
    end

    error("Maximum iterations exceeded")
end

"""
    bisection_method(f::Function, a::Float64, b::Float64; tol::Float64=1e-10)

Find root using bisection method.
"""
function bisection_method(f::Function, a::Float64, b::Float64;
                         tol::Float64=1e-10, max_iter::Int=100)
    if f(a) * f(b) > 0
        error("Function must have opposite signs at endpoints")
    end

    for _ in 1:max_iter
        c = (a + b) / 2
        fc = f(c)

        if abs(fc) < tol || (b - a) / 2 < tol
            return c
        end

        if sign(fc) == sign(f(a))
            a = c
        else
            b = c
        end
    end

    return (a + b) / 2
end

"""
    trapezoidal_integration(f::Function, a::Float64, b::Float64, n::Int=1000)

Numerical integration using trapezoidal rule.
"""
function trapezoidal_integration(f::Function, a::Float64, b::Float64, n::Int=1000)
    h = (b - a) / n
    sum = (f(a) + f(b)) / 2

    for i in 1:n-1
        x = a + i * h
        sum += f(x)
    end

    return h * sum
end

"""
    simpsons_rule(f::Function, a::Float64, b::Float64, n::Int=1000)

Numerical integration using Simpson's rule.
"""
function simpsons_rule(f::Function, a::Float64, b::Float64, n::Int=1000)
    if n % 2 != 0
        n += 1
    end

    h = (b - a) / n
    sum = f(a) + f(b)

    for i in 1:n-1
        x = a + i * h
        if i % 2 == 0
            sum += 2 * f(x)
        else
            sum += 4 * f(x)
        end
    end

    return h * sum / 3
end

"""
    gaussian_elimination(A::Matrix{Float64}, b::Vector{Float64})

Solve Ax = b using Gaussian elimination with partial pivoting.
"""
function gaussian_elimination(A::Matrix{Float64}, b::Vector{Float64})
    n = size(A, 1)
    aug = hcat(A, b)  # Augmented matrix

    # Forward elimination
    for i in 1:n-1
        # Partial pivoting
        max_row = argmax(abs.(aug[i:n, i])) + i - 1
        if max_row != i
            aug[[i, max_row], :] = aug[[max_row, i], :]
        end

        # Eliminate below
        for j in i+1:n
            if abs(aug[i, i]) < eps()
                error("Matrix is singular")
            end

            factor = aug[j, i] / aug[i, i]
            aug[j, :] -= factor * aug[i, :]
        end
    end

    # Back substitution
    x = zeros(n)
    for i in n:-1:1
        x[i] = aug[i, n+1]
        for j in i+1:n
            x[i] -= aug[i, j] * x[j]
        end
        x[i] /= aug[i, i]
    end

    return x
end

end # module NumericalAlgorithms