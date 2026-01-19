/**
 * @module numerical
 * @description Numerical algorithms and mathematical computations
 */

/**
 * Calculate Greatest Common Divisor using Euclidean algorithm
 * Time: O(log min(a,b)), Space: O(1)
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} GCD of a and b
 */
export function gcd(a, b) {
    a = Math.abs(a);
    b = Math.abs(b);

    while (b !== 0) {
        const temp = b;
        b = a % b;
        a = temp;
    }

    return a;
}

/**
 * Calculate GCD of multiple numbers
 * @param {...number} numbers - Numbers to find GCD
 * @returns {number} GCD of all numbers
 */
export function gcdMultiple(...numbers) {
    return numbers.reduce((acc, num) => gcd(acc, num));
}

/**
 * Calculate Least Common Multiple
 * Time: O(log min(a,b)), Space: O(1)
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} LCM of a and b
 */
export function lcm(a, b) {
    return Math.abs(a * b) / gcd(a, b);
}

/**
 * Calculate LCM of multiple numbers
 * @param {...number} numbers - Numbers to find LCM
 * @returns {number} LCM of all numbers
 */
export function lcmMultiple(...numbers) {
    return numbers.reduce((acc, num) => lcm(acc, num));
}

/**
 * Extended Euclidean Algorithm
 * Finds x, y such that ax + by = gcd(a, b)
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {Object} {gcd, x, y}
 */
export function extendedGCD(a, b) {
    if (b === 0) {
        return { gcd: a, x: 1, y: 0 };
    }

    const result = extendedGCD(b, a % b);
    const x = result.y;
    const y = result.x - Math.floor(a / b) * result.y;

    return { gcd: result.gcd, x, y };
}

/**
 * Check if a number is prime
 * Time: O(√n), Space: O(1)
 * @param {number} n - Number to check
 * @returns {boolean} True if prime
 */
export function isPrime(n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 === 0 || n % 3 === 0) return false;

    for (let i = 5; i * i <= n; i += 6) {
        if (n % i === 0 || n % (i + 2) === 0) {
            return false;
        }
    }

    return true;
}

/**
 * Miller-Rabin Primality Test
 * Probabilistic primality test
 * @param {number} n - Number to test
 * @param {number} [k=5] - Number of rounds
 * @returns {boolean} True if probably prime
 */
export function millerRabin(n, k = 5) {
    if (n < 2) return false;
    if (n === 2 || n === 3) return true;
    if (n % 2 === 0) return false;

    // Write n-1 as d * 2^r
    let r = 0;
    let d = n - 1;
    while (d % 2 === 0) {
        d /= 2;
        r++;
    }

    // Witness loop
    for (let i = 0; i < k; i++) {
        const a = 2 + Math.floor(Math.random() * (n - 4));
        let x = modPow(a, d, n);

        if (x === 1 || x === n - 1) continue;

        let continueWitnessLoop = false;
        for (let j = 0; j < r - 1; j++) {
            x = (x * x) % n;
            if (x === n - 1) {
                continueWitnessLoop = true;
                break;
            }
        }

        if (!continueWitnessLoop) return false;
    }

    return true;
}

/**
 * Generate prime numbers using Sieve of Eratosthenes
 * Time: O(n log log n), Space: O(n)
 * @param {number} n - Upper limit
 * @returns {Array<number>} Array of primes up to n
 */
export function sieveOfEratosthenes(n) {
    if (n < 2) return [];

    const sieve = new Array(n + 1).fill(true);
    sieve[0] = sieve[1] = false;

    for (let i = 2; i * i <= n; i++) {
        if (sieve[i]) {
            for (let j = i * i; j <= n; j += i) {
                sieve[j] = false;
            }
        }
    }

    const primes = [];
    for (let i = 2; i <= n; i++) {
        if (sieve[i]) {
            primes.push(i);
        }
    }

    return primes;
}

/**
 * Segmented Sieve for large ranges
 * @param {number} low - Lower bound
 * @param {number} high - Upper bound
 * @returns {Array<number>} Primes in range [low, high]
 */
export function segmentedSieve(low, high) {
    const limit = Math.floor(Math.sqrt(high)) + 1;
    const basePrimes = sieveOfEratosthenes(limit);
    const primes = [];

    if (low <= 2 && 2 <= high) primes.push(2);

    // Make low odd
    if (low % 2 === 0) low++;

    const isPrime = new Array(high - low + 1).fill(true);

    for (const p of basePrimes) {
        if (p === 2) continue;

        let start = Math.max(p * p, Math.ceil(low / p) * p);
        if (start % 2 === 0) start += p;

        for (let j = start; j <= high; j += 2 * p) {
            isPrime[j - low] = false;
        }
    }

    for (let i = Math.max(3, low); i <= high; i += 2) {
        if (isPrime[i - low]) {
            primes.push(i);
        }
    }

    return primes;
}

/**
 * Find next prime after n
 * @param {number} n - Starting number
 * @returns {number} Next prime
 */
export function nextPrime(n) {
    if (n < 2) return 2;

    let candidate = n + 1;
    while (!isPrime(candidate)) {
        candidate++;
    }

    return candidate;
}

/**
 * Prime factorization
 * Time: O(√n), Space: O(log n)
 * @param {number} n - Number to factorize
 * @returns {Array<Object>} Array of {prime, power} objects
 */
export function primeFactorization(n) {
    const factors = [];

    // Handle 2 separately
    let count = 0;
    while (n % 2 === 0) {
        count++;
        n /= 2;
    }
    if (count > 0) {
        factors.push({ prime: 2, power: count });
    }

    // Check odd divisors
    for (let i = 3; i * i <= n; i += 2) {
        count = 0;
        while (n % i === 0) {
            count++;
            n /= i;
        }
        if (count > 0) {
            factors.push({ prime: i, power: count });
        }
    }

    // If n is still greater than 1, it's a prime
    if (n > 1) {
        factors.push({ prime: n, power: 1 });
    }

    return factors;
}

/**
 * Get all divisors of a number
 * @param {number} n - Number
 * @returns {Array<number>} All divisors
 */
export function getDivisors(n) {
    const divisors = [];

    for (let i = 1; i * i <= n; i++) {
        if (n % i === 0) {
            divisors.push(i);
            if (i !== n / i) {
                divisors.push(n / i);
            }
        }
    }

    return divisors.sort((a, b) => a - b);
}

/**
 * Calculate Euler's totient function φ(n)
 * @param {number} n - Number
 * @returns {number} Count of numbers coprime to n
 */
export function eulerTotient(n) {
    let result = n;

    for (let p = 2; p * p <= n; p++) {
        if (n % p === 0) {
            while (n % p === 0) {
                n /= p;
            }
            result -= result / p;
        }
    }

    if (n > 1) {
        result -= result / n;
    }

    return result;
}

/**
 * Calculate factorial
 * @param {number} n - Number
 * @returns {number} n!
 */
export function factorial(n) {
    if (n < 0) return undefined;
    if (n === 0 || n === 1) return 1;

    let result = 1;
    for (let i = 2; i <= n; i++) {
        result *= i;
    }

    return result;
}

/**
 * Calculate factorial using BigInt for large numbers
 * @param {number} n - Number
 * @returns {bigint} n! as BigInt
 */
export function factorialBig(n) {
    if (n < 0) return undefined;
    if (n === 0 || n === 1) return 1n;

    let result = 1n;
    for (let i = 2n; i <= BigInt(n); i++) {
        result *= i;
    }

    return result;
}

/**
 * Calculate binomial coefficient (n choose k)
 * @param {number} n - Total items
 * @param {number} k - Items to choose
 * @returns {number} C(n, k)
 */
export function binomialCoefficient(n, k) {
    if (k < 0 || k > n) return 0;
    if (k === 0 || k === n) return 1;

    k = Math.min(k, n - k); // Optimization

    let result = 1;
    for (let i = 1; i <= k; i++) {
        result = result * (n - i + 1) / i;
    }

    return Math.round(result);
}

/**
 * Generate Pascal's Triangle
 * @param {number} n - Number of rows
 * @returns {Array<Array<number>>} Pascal's triangle
 */
export function pascalTriangle(n) {
    const triangle = [];

    for (let i = 0; i < n; i++) {
        const row = new Array(i + 1);
        row[0] = row[i] = 1;

        for (let j = 1; j < i; j++) {
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j];
        }

        triangle.push(row);
    }

    return triangle;
}

/**
 * Calculate nth Fibonacci number
 * @param {number} n - Index
 * @returns {number} nth Fibonacci number
 */
export function fibonacci(n) {
    if (n <= 0) return 0;
    if (n === 1) return 1;

    let prev = 0, curr = 1;
    for (let i = 2; i <= n; i++) {
        [prev, curr] = [curr, prev + curr];
    }

    return curr;
}

/**
 * Calculate nth Fibonacci using matrix exponentiation
 * Time: O(log n)
 * @param {number} n - Index
 * @returns {number} nth Fibonacci number
 */
export function fibonacciMatrix(n) {
    if (n <= 0) return 0;
    if (n === 1) return 1;

    const multiply = (a, b) => [
        [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
        [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]
    ];

    const power = (mat, n) => {
        if (n === 1) return mat;

        if (n % 2 === 0) {
            const half = power(mat, n / 2);
            return multiply(half, half);
        }

        return multiply(mat, power(mat, n - 1));
    };

    const base = [[1, 1], [1, 0]];
    const result = power(base, n);

    return result[0][1];
}

/**
 * Generate Fibonacci sequence
 * @param {number} n - Number of terms
 * @returns {Array<number>} Fibonacci sequence
 */
export function fibonacciSequence(n) {
    if (n <= 0) return [];
    if (n === 1) return [0];

    const seq = [0, 1];
    for (let i = 2; i < n; i++) {
        seq.push(seq[i - 1] + seq[i - 2]);
    }

    return seq;
}

/**
 * Check if number is Fibonacci number
 * @param {number} n - Number to check
 * @returns {boolean} True if Fibonacci number
 */
export function isFibonacci(n) {
    const isPerfectSquare = (num) => {
        const sqrt = Math.sqrt(num);
        return sqrt === Math.floor(sqrt);
    };

    return isPerfectSquare(5 * n * n + 4) || isPerfectSquare(5 * n * n - 4);
}

/**
 * Calculate nth Catalan number
 * @param {number} n - Index
 * @returns {number} nth Catalan number
 */
export function catalanNumber(n) {
    if (n <= 1) return 1;

    const catalan = new Array(n + 1).fill(0);
    catalan[0] = catalan[1] = 1;

    for (let i = 2; i <= n; i++) {
        for (let j = 0; j < i; j++) {
            catalan[i] += catalan[j] * catalan[i - 1 - j];
        }
    }

    return catalan[n];
}

/**
 * Fast power calculation (Binary Exponentiation)
 * Time: O(log n)
 * @param {number} base - Base
 * @param {number} exp - Exponent
 * @returns {number} base^exp
 */
export function fastPower(base, exp) {
    if (exp < 0) return 1 / fastPower(base, -exp);

    let result = 1;
    while (exp > 0) {
        if (exp % 2 === 1) {
            result *= base;
        }
        base *= base;
        exp = Math.floor(exp / 2);
    }

    return result;
}

/**
 * Modular exponentiation
 * Calculate (base^exp) % mod
 * @param {number} base - Base
 * @param {number} exp - Exponent
 * @param {number} mod - Modulo
 * @returns {number} Result
 */
export function modPow(base, exp, mod) {
    if (mod === 1) return 0;

    let result = 1;
    base = base % mod;

    while (exp > 0) {
        if (exp % 2 === 1) {
            result = (result * base) % mod;
        }
        exp = Math.floor(exp / 2);
        base = (base * base) % mod;
    }

    return result;
}

/**
 * Modular multiplicative inverse
 * @param {number} a - Number
 * @param {number} m - Modulo
 * @returns {number} Multiplicative inverse or -1 if doesn't exist
 */
export function modInverse(a, m) {
    const { gcd: g, x } = extendedGCD(a, m);

    if (g !== 1) return -1; // Inverse doesn't exist

    return ((x % m) + m) % m;
}

/**
 * Chinese Remainder Theorem
 * @param {Array<number>} remainders - Remainders
 * @param {Array<number>} moduli - Moduli (must be pairwise coprime)
 * @returns {number} Solution
 */
export function chineseRemainderTheorem(remainders, moduli) {
    const prod = moduli.reduce((a, b) => a * b);
    let sum = 0;

    for (let i = 0; i < remainders.length; i++) {
        const p = prod / moduli[i];
        sum += remainders[i] * modInverse(p, moduli[i]) * p;
    }

    return sum % prod;
}

/**
 * Calculate square root using Newton's method
 * @param {number} n - Number
 * @param {number} [precision=1e-10] - Precision
 * @returns {number} Square root
 */
export function sqrt(n, precision = 1e-10) {
    if (n < 0) return NaN;
    if (n === 0) return 0;

    let x = n;
    let prev;

    do {
        prev = x;
        x = (x + n / x) / 2;
    } while (Math.abs(x - prev) > precision);

    return x;
}

/**
 * Calculate nth root
 * @param {number} n - Number
 * @param {number} root - Root degree
 * @param {number} [precision=1e-10] - Precision
 * @returns {number} nth root
 */
export function nthRoot(n, root, precision = 1e-10) {
    if (root === 0) return NaN;
    if (n === 0) return 0;

    let x = n;
    let prev;

    do {
        prev = x;
        x = ((root - 1) * x + n / Math.pow(x, root - 1)) / root;
    } while (Math.abs(x - prev) > precision);

    return x;
}

/**
 * Check if number is perfect square
 * @param {number} n - Number
 * @returns {boolean} True if perfect square
 */
export function isPerfectSquare(n) {
    if (n < 0) return false;
    const sqrt = Math.sqrt(n);
    return sqrt === Math.floor(sqrt);
}

/**
 * Check if number is perfect number
 * @param {number} n - Number
 * @returns {boolean} True if perfect number
 */
export function isPerfectNumber(n) {
    if (n <= 1) return false;

    const divisors = getDivisors(n);
    const sum = divisors.slice(0, -1).reduce((a, b) => a + b, 0);

    return sum === n;
}

/**
 * Check if number is Armstrong number
 * @param {number} n - Number
 * @returns {boolean} True if Armstrong number
 */
export function isArmstrong(n) {
    const str = n.toString();
    const power = str.length;
    const sum = str.split('').reduce((acc, digit) =>
        acc + Math.pow(parseInt(digit), power), 0);

    return sum === n;
}

/**
 * Generate Collatz sequence
 * @param {number} n - Starting number
 * @returns {Array<number>} Collatz sequence
 */
export function collatzSequence(n) {
    const sequence = [n];

    while (n !== 1) {
        if (n % 2 === 0) {
            n = n / 2;
        } else {
            n = 3 * n + 1;
        }
        sequence.push(n);
    }

    return sequence;
}

/**
 * Calculate sum of digits
 * @param {number} n - Number
 * @returns {number} Sum of digits
 */
export function sumOfDigits(n) {
    return Math.abs(n).toString().split('').reduce((sum, digit) =>
        sum + parseInt(digit), 0);
}

/**
 * Reverse a number
 * @param {number} n - Number
 * @returns {number} Reversed number
 */
export function reverseNumber(n) {
    const sign = Math.sign(n);
    const reversed = parseInt(Math.abs(n).toString().split('').reverse().join(''));
    return sign * reversed;
}

/**
 * Check if number is palindrome
 * @param {number} n - Number
 * @returns {boolean} True if palindrome
 */
export function isPalindromeNumber(n) {
    if (n < 0) return false;
    return n === reverseNumber(n);
}

/**
 * Linear interpolation
 * @param {number} x0 - First x coordinate
 * @param {number} y0 - First y coordinate
 * @param {number} x1 - Second x coordinate
 * @param {number} y1 - Second y coordinate
 * @param {number} x - Point to interpolate
 * @returns {number} Interpolated y value
 */
export function linearInterpolation(x0, y0, x1, y1, x) {
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0);
}

/**
 * Lagrange interpolation
 * @param {Array<number>} xPoints - X coordinates
 * @param {Array<number>} yPoints - Y coordinates
 * @param {number} x - Point to interpolate
 * @returns {number} Interpolated value
 */
export function lagrangeInterpolation(xPoints, yPoints, x) {
    let result = 0;
    const n = xPoints.length;

    for (let i = 0; i < n; i++) {
        let term = yPoints[i];
        for (let j = 0; j < n; j++) {
            if (i !== j) {
                term *= (x - xPoints[j]) / (xPoints[i] - xPoints[j]);
            }
        }
        result += term;
    }

    return result;
}

/**
 * Newton-Raphson method for finding roots
 * @param {Function} f - Function
 * @param {Function} df - Derivative of function
 * @param {number} x0 - Initial guess
 * @param {number} [tolerance=1e-10] - Tolerance
 * @param {number} [maxIter=100] - Maximum iterations
 * @returns {number|null} Root or null if not found
 */
export function newtonRaphson(f, df, x0, tolerance = 1e-10, maxIter = 100) {
    let x = x0;

    for (let i = 0; i < maxIter; i++) {
        const fx = f(x);
        if (Math.abs(fx) < tolerance) {
            return x;
        }

        const dfx = df(x);
        if (dfx === 0) {
            return null; // Derivative is zero, can't continue
        }

        x = x - fx / dfx;
    }

    return null; // Didn't converge
}

/**
 * Bisection method for finding roots
 * @param {Function} f - Function
 * @param {number} a - Lower bound
 * @param {number} b - Upper bound
 * @param {number} [tolerance=1e-10] - Tolerance
 * @returns {number|null} Root or null if not found
 */
export function bisectionMethod(f, a, b, tolerance = 1e-10) {
    if (f(a) * f(b) > 0) {
        return null; // No root in interval
    }

    while (b - a > tolerance) {
        const c = (a + b) / 2;

        if (Math.abs(f(c)) < tolerance) {
            return c;
        }

        if (f(a) * f(c) < 0) {
            b = c;
        } else {
            a = c;
        }
    }

    return (a + b) / 2;
}

/**
 * Trapezoidal rule for numerical integration
 * @param {Function} f - Function to integrate
 * @param {number} a - Lower bound
 * @param {number} b - Upper bound
 * @param {number} [n=1000] - Number of trapezoids
 * @returns {number} Approximate integral
 */
export function trapezoidalRule(f, a, b, n = 1000) {
    const h = (b - a) / n;
    let sum = (f(a) + f(b)) / 2;

    for (let i = 1; i < n; i++) {
        sum += f(a + i * h);
    }

    return sum * h;
}

/**
 * Simpson's rule for numerical integration
 * @param {Function} f - Function to integrate
 * @param {number} a - Lower bound
 * @param {number} b - Upper bound
 * @param {number} [n=1000] - Number of intervals (must be even)
 * @returns {number} Approximate integral
 */
export function simpsonsRule(f, a, b, n = 1000) {
    if (n % 2 !== 0) n++; // Make sure n is even

    const h = (b - a) / n;
    let sum = f(a) + f(b);

    for (let i = 1; i < n; i++) {
        const x = a + i * h;
        sum += (i % 2 === 0 ? 2 : 4) * f(x);
    }

    return sum * h / 3;
}

// Export all numerical algorithms
export default {
    gcd,
    gcdMultiple,
    lcm,
    lcmMultiple,
    extendedGCD,
    isPrime,
    millerRabin,
    sieveOfEratosthenes,
    segmentedSieve,
    nextPrime,
    primeFactorization,
    getDivisors,
    eulerTotient,
    factorial,
    factorialBig,
    binomialCoefficient,
    pascalTriangle,
    fibonacci,
    fibonacciMatrix,
    fibonacciSequence,
    isFibonacci,
    catalanNumber,
    fastPower,
    modPow,
    modInverse,
    chineseRemainderTheorem,
    sqrt,
    nthRoot,
    isPerfectSquare,
    isPerfectNumber,
    isArmstrong,
    collatzSequence,
    sumOfDigits,
    reverseNumber,
    isPalindromeNumber,
    linearInterpolation,
    lagrangeInterpolation,
    newtonRaphson,
    bisectionMethod,
    trapezoidalRule,
    simpsonsRule
};