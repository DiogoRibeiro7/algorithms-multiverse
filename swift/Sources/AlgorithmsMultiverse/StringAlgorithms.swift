// String Algorithms - Swift Implementation
// Advanced string processing and pattern matching algorithms

import Foundation

/// Namespace for string algorithms
public enum StringAlgorithms {

    // MARK: - Pattern Matching Algorithms

    /// KMP (Knuth-Morris-Pratt) pattern searching
    /// - Parameters:
    ///   - text: Text to search in
    ///   - pattern: Pattern to find
    /// - Returns: Array of starting indices where pattern is found
    /// - Complexity: O(n + m) time, O(m) space
    public static func kmpSearch(_ text: String, pattern: String) -> [Int] {
        let textArray = Array(text)
        let patternArray = Array(pattern)
        let n = textArray.count
        let m = patternArray.count

        guard m > 0 && m <= n else { return [] }

        // Build LPS (Longest Proper Prefix which is also Suffix) array
        let lps = computeLPSArray(patternArray)
        var matches: [Int] = []

        var i = 0  // Index for text
        var j = 0  // Index for pattern

        while i < n {
            if textArray[i] == patternArray[j] {
                i += 1
                j += 1
            }

            if j == m {
                matches.append(i - j)
                j = lps[j - 1]
            } else if i < n && textArray[i] != patternArray[j] {
                if j != 0 {
                    j = lps[j - 1]
                } else {
                    i += 1
                }
            }
        }

        return matches
    }

    private static func computeLPSArray(_ pattern: [Character]) -> [Int] {
        let m = pattern.count
        var lps = Array(repeating: 0, count: m)
        var length = 0
        var i = 1

        while i < m {
            if pattern[i] == pattern[length] {
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

    /// Rabin-Karp rolling hash pattern searching
    /// - Complexity: O(n + m) average, O(nm) worst case
    public static func rabinKarpSearch(_ text: String, pattern: String) -> [Int] {
        let textArray = Array(text)
        let patternArray = Array(pattern)
        let n = textArray.count
        let m = patternArray.count

        guard m > 0 && m <= n else { return [] }

        let prime = 101
        let base = 256
        var matches: [Int] = []

        // Calculate hash value of pattern and first window
        var patternHash = 0
        var windowHash = 0
        var h = 1

        // Calculate h = base^(m-1) % prime
        for _ in 0..<m - 1 {
            h = (h * base) % prime
        }

        // Calculate initial hash values
        for i in 0..<m {
            patternHash = (base * patternHash + Int(patternArray[i].asciiValue ?? 0)) % prime
            windowHash = (base * windowHash + Int(textArray[i].asciiValue ?? 0)) % prime
        }

        // Slide pattern over text
        for i in 0...(n - m) {
            if patternHash == windowHash {
                // Check characters one by one
                var match = true
                for j in 0..<m {
                    if textArray[i + j] != patternArray[j] {
                        match = false
                        break
                    }
                }
                if match {
                    matches.append(i)
                }
            }

            // Calculate hash for next window
            if i < n - m {
                windowHash = (base * (windowHash - Int(textArray[i].asciiValue ?? 0) * h) +
                             Int(textArray[i + m].asciiValue ?? 0)) % prime

                if windowHash < 0 {
                    windowHash += prime
                }
            }
        }

        return matches
    }

    /// Boyer-Moore pattern searching
    /// - Complexity: O(nm) worst case, O(n/m) best case
    public static func boyerMooreSearch(_ text: String, pattern: String) -> [Int] {
        let textArray = Array(text)
        let patternArray = Array(pattern)
        let n = textArray.count
        let m = patternArray.count

        guard m > 0 && m <= n else { return [] }

        var matches: [Int] = []

        // Build bad character table
        let badCharTable = buildBadCharTable(patternArray)

        var shift = 0
        while shift <= n - m {
            var j = m - 1

            while j >= 0 && patternArray[j] == textArray[shift + j] {
                j -= 1
            }

            if j < 0 {
                matches.append(shift)
                shift += (shift + m < n) ? m - (badCharTable[textArray[shift + m]] ?? m) : 1
            } else {
                let badChar = textArray[shift + j]
                shift += max(1, j - (badCharTable[badChar] ?? -1))
            }
        }

        return matches
    }

    private static func buildBadCharTable(_ pattern: [Character]) -> [Character: Int] {
        var table: [Character: Int] = [:]

        for (index, char) in pattern.enumerated() {
            table[char] = index
        }

        return table
    }

    /// Z-Algorithm for pattern matching
    /// - Complexity: O(n + m) time, O(n) space
    public static func zAlgorithm(_ str: String) -> [Int] {
        let s = Array(str)
        let n = s.count
        var z = Array(repeating: 0, count: n)

        var left = 0
        var right = 0

        for i in 1..<n {
            if i > right {
                left = i
                right = i

                while right < n && s[right - left] == s[right] {
                    right += 1
                }

                z[i] = right - left
                right -= 1
            } else {
                let k = i - left

                if z[k] < right - i + 1 {
                    z[i] = z[k]
                } else {
                    left = i

                    while right < n && s[right - left] == s[right] {
                        right += 1
                    }

                    z[i] = right - left
                    right -= 1
                }
            }
        }

        return z
    }

    // MARK: - String Manipulation

    /// Find longest common prefix among strings
    /// - Complexity: O(S) where S is sum of all string lengths
    public static func longestCommonPrefix(_ strings: [String]) -> String {
        guard !strings.isEmpty else { return "" }

        var prefix = strings[0]

        for str in strings.dropFirst() {
            while !str.hasPrefix(prefix) {
                prefix = String(prefix.dropLast())
                if prefix.isEmpty {
                    return ""
                }
            }
        }

        return prefix
    }

    /// Find longest common substring between two strings
    /// - Complexity: O(mn) time and space
    public static func longestCommonSubstring(_ s1: String, _ s2: String) -> String {
        let arr1 = Array(s1)
        let arr2 = Array(s2)
        let m = arr1.count
        let n = arr2.count

        var dp = Array(repeating: Array(repeating: 0, count: n + 1), count: m + 1)
        var maxLength = 0
        var endingPos = 0

        for i in 1...m {
            for j in 1...n {
                if arr1[i - 1] == arr2[j - 1] {
                    dp[i][j] = dp[i - 1][j - 1] + 1
                    if dp[i][j] > maxLength {
                        maxLength = dp[i][j]
                        endingPos = i
                    }
                }
            }
        }

        if maxLength == 0 {
            return ""
        }

        return String(arr1[(endingPos - maxLength)..<endingPos])
    }

    /// Check if string is palindrome
    /// - Complexity: O(n) time, O(1) space
    public static func isPalindrome(_ str: String) -> Bool {
        let chars = Array(str)
        var left = 0
        var right = chars.count - 1

        while left < right {
            if chars[left] != chars[right] {
                return false
            }
            left += 1
            right -= 1
        }

        return true
    }

    /// Find longest palindromic substring using Manacher's algorithm
    /// - Complexity: O(n) time and space
    public static func longestPalindrome(_ s: String) -> String {
        guard !s.isEmpty else { return "" }

        // Preprocess string to handle even-length palindromes
        var processed = "#"
        for char in s {
            processed += "\(char)#"
        }

        let chars = Array(processed)
        let n = chars.count
        var palindromeLengths = Array(repeating: 0, count: n)
        var center = 0
        var rightBoundary = 0

        for i in 0..<n {
            let mirror = 2 * center - i

            if i < rightBoundary {
                palindromeLengths[i] = min(rightBoundary - i, palindromeLengths[mirror])
            }

            // Try to expand palindrome centered at i
            var left = i - (1 + palindromeLengths[i])
            var right = i + (1 + palindromeLengths[i])

            while left >= 0 && right < n && chars[left] == chars[right] {
                palindromeLengths[i] += 1
                left -= 1
                right += 1
            }

            // Update center and right boundary if needed
            if i + palindromeLengths[i] > rightBoundary {
                center = i
                rightBoundary = i + palindromeLengths[i]
            }
        }

        // Find longest palindrome
        let maxLength = palindromeLengths.max() ?? 0
        let maxIndex = palindromeLengths.firstIndex(of: maxLength) ?? 0

        // Extract original palindrome
        let start = (maxIndex - maxLength) / 2
        return String(Array(s)[start..<(start + maxLength)])
    }

    /// Find all palindromic substrings
    /// - Complexity: O(n²) time, O(1) space per palindrome
    public static func allPalindromes(_ s: String) -> [String] {
        let chars = Array(s)
        var palindromes: Set<String> = []

        // Check odd-length palindromes
        for center in 0..<chars.count {
            expandAroundCenter(chars, center, center, &palindromes)
        }

        // Check even-length palindromes
        for center in 0..<chars.count - 1 {
            expandAroundCenter(chars, center, center + 1, &palindromes)
        }

        return Array(palindromes).sorted { $0.count > $1.count }
    }

    private static func expandAroundCenter(_ chars: [Character], _ left: Int, _ right: Int, _ palindromes: inout Set<String>) {
        var l = left
        var r = right

        while l >= 0 && r < chars.count && chars[l] == chars[r] {
            palindromes.insert(String(chars[l...r]))
            l -= 1
            r += 1
        }
    }

    // MARK: - String Distance Metrics

    /// Calculate Levenshtein (edit) distance between two strings
    /// - Complexity: O(mn) time and space
    public static func editDistance(_ s1: String, _ s2: String) -> Int {
        let m = s1.count
        let n = s2.count
        let arr1 = Array(s1)
        let arr2 = Array(s2)

        var dp = Array(repeating: Array(repeating: 0, count: n + 1), count: m + 1)

        // Initialize base cases
        for i in 0...m {
            dp[i][0] = i
        }
        for j in 0...n {
            dp[0][j] = j
        }

        // Fill DP table
        for i in 1...m {
            for j in 1...n {
                if arr1[i - 1] == arr2[j - 1] {
                    dp[i][j] = dp[i - 1][j - 1]
                } else {
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],     // Delete
                        dp[i][j - 1],     // Insert
                        dp[i - 1][j - 1]  // Replace
                    )
                }
            }
        }

        return dp[m][n]
    }

    /// Calculate Hamming distance (for equal-length strings)
    /// - Complexity: O(n) time, O(1) space
    public static func hammingDistance(_ s1: String, _ s2: String) -> Int? {
        guard s1.count == s2.count else { return nil }

        return zip(s1, s2).reduce(0) { count, pair in
            count + (pair.0 == pair.1 ? 0 : 1)
        }
    }

    // MARK: - String Transformations

    /// Run-length encoding compression
    /// - Complexity: O(n) time and space
    public static func runLengthEncode(_ str: String) -> String {
        guard !str.isEmpty else { return "" }

        var encoded = ""
        let chars = Array(str)
        var count = 1
        var currentChar = chars[0]

        for i in 1..<chars.count {
            if chars[i] == currentChar {
                count += 1
            } else {
                encoded += "\(currentChar)\(count > 1 ? "\(count)" : "")"
                currentChar = chars[i]
                count = 1
            }
        }

        encoded += "\(currentChar)\(count > 1 ? "\(count)" : "")"

        return encoded.count < str.count ? encoded : str
    }

    /// Run-length decoding
    /// - Complexity: O(n) time and space
    public static func runLengthDecode(_ str: String) -> String {
        var decoded = ""
        var i = 0
        let chars = Array(str)

        while i < chars.count {
            let char = chars[i]
            i += 1

            var countStr = ""
            while i < chars.count && chars[i].isNumber {
                countStr.append(chars[i])
                i += 1
            }

            let count = Int(countStr) ?? 1
            decoded += String(repeating: String(char), count: count)
        }

        return decoded
    }

    /// Check if two strings are anagrams
    /// - Complexity: O(n) time, O(k) space where k is alphabet size
    public static func areAnagrams(_ s1: String, _ s2: String) -> Bool {
        guard s1.count == s2.count else { return false }

        var charCount: [Character: Int] = [:]

        for char in s1 {
            charCount[char, default: 0] += 1
        }

        for char in s2 {
            guard let count = charCount[char], count > 0 else {
                return false
            }
            charCount[char] = count - 1
        }

        return charCount.values.allSatisfy { $0 == 0 }
    }

    /// Find all anagrams of pattern in text
    /// - Complexity: O(n) time, O(k) space
    public static func findAnagrams(_ text: String, pattern: String) -> [Int] {
        let textArray = Array(text)
        let patternArray = Array(pattern)
        let n = textArray.count
        let m = patternArray.count

        guard m <= n else { return [] }

        var result: [Int] = []
        var patternFreq: [Character: Int] = [:]
        var windowFreq: [Character: Int] = [:]

        // Count pattern characters
        for char in patternArray {
            patternFreq[char, default: 0] += 1
        }

        // Sliding window
        for i in 0..<n {
            // Add character to window
            windowFreq[textArray[i], default: 0] += 1

            // Remove leftmost character if window is too large
            if i >= m {
                let leftChar = textArray[i - m]
                if let count = windowFreq[leftChar] {
                    if count == 1 {
                        windowFreq[leftChar] = nil
                    } else {
                        windowFreq[leftChar] = count - 1
                    }
                }
            }

            // Check if anagram
            if i >= m - 1 && windowFreq == patternFreq {
                result.append(i - m + 1)
            }
        }

        return result
    }

    // MARK: - Advanced String Algorithms

    /// Suffix array construction using prefix doubling
    /// - Complexity: O(n log n) time, O(n) space
    public static func buildSuffixArray(_ str: String) -> [Int] {
        let s = Array(str)
        let n = s.count
        var suffixArray = Array(0..<n)
        var rank = s.map { Int($0.asciiValue ?? 0) }
        var tempRank = Array(repeating: 0, count: n)

        var k = 1
        while k < n {
            // Sort suffixes based on rank[i] and rank[i+k]
            suffixArray.sort { i, j in
                if rank[i] != rank[j] {
                    return rank[i] < rank[j]
                }
                let rankI = (i + k < n) ? rank[i + k] : -1
                let rankJ = (j + k < n) ? rank[j + k] : -1
                return rankI < rankJ
            }

            // Update ranks
            tempRank[suffixArray[0]] = 0
            for i in 1..<n {
                let prevRank1 = rank[suffixArray[i - 1]]
                let prevRank2 = (suffixArray[i - 1] + k < n) ? rank[suffixArray[i - 1] + k] : -1
                let currRank1 = rank[suffixArray[i]]
                let currRank2 = (suffixArray[i] + k < n) ? rank[suffixArray[i] + k] : -1

                if prevRank1 == currRank1 && prevRank2 == currRank2 {
                    tempRank[suffixArray[i]] = tempRank[suffixArray[i - 1]]
                } else {
                    tempRank[suffixArray[i]] = tempRank[suffixArray[i - 1]] + 1
                }
            }

            rank = tempRank
            k *= 2
        }

        return suffixArray
    }

    /// Find minimum window containing all characters of pattern
    /// - Complexity: O(n) time, O(k) space
    public static func minWindowSubstring(_ s: String, pattern: String) -> String {
        let sArray = Array(s)
        let n = sArray.count

        var patternFreq: [Character: Int] = [:]
        for char in pattern {
            patternFreq[char, default: 0] += 1
        }

        var windowFreq: [Character: Int] = [:]
        var left = 0
        var minLength = Int.max
        var minStart = 0
        var formed = 0
        let required = patternFreq.count

        for right in 0..<n {
            let char = sArray[right]
            windowFreq[char, default: 0] += 1

            if let patternCount = patternFreq[char],
               windowFreq[char] == patternCount {
                formed += 1
            }

            while formed == required && left <= right {
                if right - left + 1 < minLength {
                    minLength = right - left + 1
                    minStart = left
                }

                let leftChar = sArray[left]
                if let count = windowFreq[leftChar] {
                    windowFreq[leftChar] = count - 1
                    if let patternCount = patternFreq[leftChar],
                       count - 1 < patternCount {
                        formed -= 1
                    }
                }
                left += 1
            }
        }

        return minLength == Int.max ? "" : String(sArray[minStart..<(minStart + minLength)])
    }
}

// MARK: - String Extensions

public extension String {
    /// Convenience methods for string algorithms

    /// Find all occurrences of pattern using KMP
    func findPattern(_ pattern: String) -> [Int] {
        return StringAlgorithms.kmpSearch(self, pattern: pattern)
    }

    /// Check if palindrome
    var isPalindrome: Bool {
        return StringAlgorithms.isPalindrome(self)
    }

    /// Get longest palindromic substring
    var longestPalindrome: String {
        return StringAlgorithms.longestPalindrome(self)
    }

    /// Calculate edit distance to another string
    func editDistance(to other: String) -> Int {
        return StringAlgorithms.editDistance(self, other)
    }

    /// Compress using run-length encoding
    var runLengthEncoded: String {
        return StringAlgorithms.runLengthEncode(self)
    }

    /// Check if anagram of another string
    func isAnagram(of other: String) -> Bool {
        return StringAlgorithms.areAnagrams(self, other)
    }
}