/*
 * ==============================================================================
 * String Algorithms in Swift
 *
 * Pattern matching and text processing algorithms leveraging Swift's
 * powerful String type and Unicode support.
 *
 * Implementations:
 * - Naive String Matching
 * - Knuth-Morris-Pratt (KMP) Algorithm
 * - Rabin-Karp Algorithm (rolling hash)
 * - Longest Palindromic Substring
 * - String Hashing
 *
 * Swift's String type handles Unicode correctly, making these algorithms
 * robust for international text.
 *
 * Compile: swiftc -O string_algorithms.swift
 * Run: ./string_algorithms
 *
 * @author Algorithms Multiverse
 * @version 1.0
 * ==============================================================================
 */

import Foundation

// ==============================================================================
// Naive String Matching
// ==============================================================================

/// Naive String Matching
///
/// Time Complexity: O((n-m+1) × m)
/// Space Complexity: O(1)
func naiveSearch(text: String, pattern: String) -> [Int] {
    let textArray = Array(text)
    let patternArray = Array(pattern)
    let n = textArray.count
    let m = patternArray.count

    var positions = [Int]()

    for i in 0...(n - m) {
        var match = true
        for j in 0..<m {
            if textArray[i + j] != patternArray[j] {
                match = false
                break
            }
        }
        if match {
            positions.append(i)
        }
    }

    return positions
}

// ==============================================================================
// Knuth-Morris-Pratt (KMP) Algorithm
// ==============================================================================

/// Compute KMP Failure Function
func computeLPS(pattern: String) -> [Int] {
    let patternArray = Array(pattern)
    let m = patternArray.count
    var lps = Array(repeating: 0, count: m)
    var length = 0
    var i = 1

    while i < m {
        if patternArray[i] == patternArray[length] {
            length += 1
            lps[i] = length
            i += 1
        } else {
            if length != 0 {
                length = lps[length - 1]
            } else {
                lps[i] = 0
                i += 1
            }
        }
    }

    return lps
}

/// KMP String Matching
///
/// Time Complexity: O(n + m)
/// Space Complexity: O(m)
///
/// Applications:
/// - Text editors (find/replace)
/// - Intrusion detection
/// - Biological sequence matching
func kmpSearch(text: String, pattern: String) -> [Int] {
    let textArray = Array(text)
    let patternArray = Array(pattern)
    let n = textArray.count
    let m = patternArray.count

    let lps = computeLPS(pattern: pattern)
    var positions = [Int]()

    var i = 0  // Index for text
    var j = 0  // Index for pattern

    while i < n {
        if patternArray[j] == textArray[i] {
            i += 1
            j += 1
        }

        if j == m {
            positions.append(i - m)
            j = lps[j - 1]
        } else if i < n && patternArray[j] != textArray[i] {
            if j != 0 {
                j = lps[j - 1]
            } else {
                i += 1
            }
        }
    }

    return positions
}

// ==============================================================================
// Rabin-Karp Algorithm (Rolling Hash)
// ==============================================================================

/// Rabin-Karp String Matching
///
/// Time Complexity: O(n + m) average, O(nm) worst case
/// Space Complexity: O(1)
///
/// Applications:
/// - Plagiarism detection
/// - Multiple pattern search
func rabinKarpSearch(text: String, pattern: String, d: Int = 256, q: Int = 101) -> [Int] {
    let textArray = Array(text)
    let patternArray = Array(pattern)
    let n = textArray.count
    let m = patternArray.count

    var positions = [Int]()

    // Calculate hash value for pattern and first window
    var h = 1
    for _ in 0..<(m - 1) {
        h = (h * d) % q
    }

    var p = 0  // Hash for pattern
    var t = 0  // Hash for text window

    for i in 0..<m {
        p = (d * p + Int(patternArray[i].asciiValue ?? 0)) % q
        t = (d * t + Int(textArray[i].asciiValue ?? 0)) % q
    }

    // Slide pattern over text
    for i in 0...(n - m) {
        if p == t {
            // Verify character by character
            var match = true
            for j in 0..<m {
                if textArray[i + j] != patternArray[j] {
                    match = false
                    break
                }
            }
            if match {
                positions.append(i)
            }
        }

        // Calculate hash for next window
        if i < n - m {
            t = (d * (t - Int(textArray[i].asciiValue ?? 0) * h) + Int(textArray[i + m].asciiValue ?? 0)) % q
            if t < 0 {
                t += q
            }
        }
    }

    return positions
}

// ==============================================================================
// Longest Palindromic Substring
// ==============================================================================

/// Longest Palindromic Substring
///
/// Time Complexity: O(n²)
/// Space Complexity: O(n²)
///
/// Applications:
/// - Bioinformatics
/// - Text processing
func longestPalindrome(_ s: String) -> String {
    let chars = Array(s)
    let n = chars.count
    guard n > 0 else { return "" }

    var dp = Array(repeating: Array(repeating: false, count: n), count: n)
    var maxLength = 1
    var start = 0

    // All single characters are palindromes
    for i in 0..<n {
        dp[i][i] = true
    }

    // Check for length 2
    for i in 0..<(n - 1) {
        if chars[i] == chars[i + 1] {
            dp[i][i + 1] = true
            start = i
            maxLength = 2
        }
    }

    // Check for lengths > 2
    for length in 3...n {
        for i in 0..<(n - length + 1) {
            let j = i + length - 1

            if chars[i] == chars[j] && dp[i + 1][j - 1] {
                dp[i][j] = true
                start = i
                maxLength = length
            }
        }
    }

    let startIndex = s.index(s.startIndex, offsetBy: start)
    let endIndex = s.index(startIndex, offsetBy: maxLength)
    return String(s[startIndex..<endIndex])
}

// ==============================================================================
// String Hashing
// ==============================================================================

/// Polynomial Rolling Hash
///
/// Time Complexity: O(n)
/// Space Complexity: O(1)
func stringHash(_ s: String, p: Int = 31, m: Int = 1_000_000_009) -> Int {
    var hashValue = 0
    var pPow = 1

    for char in s {
        let charValue = Int(char.asciiValue ?? 0)
        hashValue = (hashValue + charValue * pPow) % m
        pPow = (pPow * p) % m
    }

    return hashValue
}

// ==============================================================================
// Main Program - Examples and Tests
// ==============================================================================

print("==============================================================================")
print("                STRING ALGORITHMS IN SWIFT")
print("           Pattern Matching & Text Processing")
print("==============================================================================\n")

// Example 1: KMP vs Naive Search
print("Example 1: Pattern Matching (KMP vs Naive)")
print(String(repeating: "=", count: 80))

let text = "ABABDABACDABABCABAB"
let pattern = "ABABCABAB"

let positionsNaive = naiveSearch(text: text, pattern: pattern)
let positionsKMP = kmpSearch(text: text, pattern: pattern)

print("Text:", text)
print("Pattern:", pattern)
print("Naive search found at:", positionsNaive.map { String($0) }.joined(separator: ", "))
print("KMP search found at:", positionsKMP.map { String($0) }.joined(separator: ", "))
print()

// Example 2: Rabin-Karp
print("Example 2: Rabin-Karp (Rolling Hash)")
print(String(repeating: "=", count: 80))

let text2 = "GEEKS FOR GEEKS"
let pattern2 = "GEEKS"

let positionsRK = rabinKarpSearch(text: text2, pattern: pattern2)
print("Text:", text2)
print("Pattern:", pattern2)
print("Found at positions:", positionsRK.map { String($0) }.joined(separator: ", "))
print()

// Example 3: Longest Palindrome
print("Example 3: Longest Palindromic Substring")
print(String(repeating: "=", count: 80))

let palindromeStr = "babad"
let longestPal = longestPalindrome(palindromeStr)

print("String:", palindromeStr)
print("Longest palindrome:", longestPal)
print()

// Example 4: String Hashing
print("Example 4: String Hashing")
print(String(repeating: "=", count: 80))

let strings = ["hello", "world", "hello", "testing"]
print("String hashes:")
for str in strings {
    let hash = stringHash(str)
    print(String(format: "  %-10s -> %d", str, hash))
}
print("\nNote: 'hello' has same hash (duplicate detected)")
print()

// Summary
print(String(repeating: "=", count: 80))
print("Summary: Swift String Algorithm Capabilities")
print(String(repeating: "=", count: 80))
print("✓ Naive Search: O(nm) - Simple baseline")
print("✓ KMP: O(n+m) - Optimal pattern matching")
print("✓ Rabin-Karp: O(n+m) average - Rolling hash")
print("✓ Longest Palindrome: O(n²) - DP approach")
print("✓ String Hashing: Fast comparison")
print("\nSwift Advantages:")
print("- Native Unicode support")
print("- Type-safe string handling")
print("- Efficient character iteration")
print(String(repeating: "=", count: 80))
