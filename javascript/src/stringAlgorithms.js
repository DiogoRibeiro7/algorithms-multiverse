/**
 * @module stringAlgorithms
 * @description String algorithms and pattern matching
 */

/**
 * KMP (Knuth-Morris-Pratt) Pattern Searching
 * Time: O(n + m), Space: O(m)
 * @param {string} text - Text to search in
 * @param {string} pattern - Pattern to search for
 * @returns {Array<number>} Array of starting indices where pattern is found
 */
export function kmpSearch(text, pattern) {
    if (!pattern || pattern.length === 0) return [];
    if (pattern.length > text.length) return [];

    const matches = [];
    const lps = computeLPSArray(pattern);
    let i = 0; // index for text
    let j = 0; // index for pattern

    while (i < text.length) {
        if (pattern[j] === text[i]) {
            i++;
            j++;
        }

        if (j === pattern.length) {
            matches.push(i - j);
            j = lps[j - 1];
        } else if (i < text.length && pattern[j] !== text[i]) {
            if (j !== 0) {
                j = lps[j - 1];
            } else {
                i++;
            }
        }
    }

    return matches;
}

/**
 * Compute Longest Proper Prefix which is also Suffix array
 * @private
 */
function computeLPSArray(pattern) {
    const lps = new Array(pattern.length).fill(0);
    let len = 0;
    let i = 1;

    while (i < pattern.length) {
        if (pattern[i] === pattern[len]) {
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len !== 0) {
                len = lps[len - 1];
            } else {
                lps[i] = 0;
                i++;
            }
        }
    }

    return lps;
}

/**
 * Rabin-Karp Pattern Searching
 * Time: O(nm) worst case, O(n+m) average
 * @param {string} text - Text to search in
 * @param {string} pattern - Pattern to search for
 * @param {number} [prime=101] - Prime number for hashing
 * @returns {Array<number>} Array of starting indices where pattern is found
 */
export function rabinKarpSearch(text, pattern, prime = 101) {
    if (!pattern || pattern.length === 0) return [];
    if (pattern.length > text.length) return [];

    const matches = [];
    const m = pattern.length;
    const n = text.length;
    const d = 256; // Number of characters in alphabet
    let patternHash = 0;
    let textHash = 0;
    let h = 1;

    // h = d^(m-1) % prime
    for (let i = 0; i < m - 1; i++) {
        h = (h * d) % prime;
    }

    // Calculate hash of pattern and first window of text
    for (let i = 0; i < m; i++) {
        patternHash = (d * patternHash + pattern.charCodeAt(i)) % prime;
        textHash = (d * textHash + text.charCodeAt(i)) % prime;
    }

    // Slide the pattern over text
    for (let i = 0; i <= n - m; i++) {
        // Check if hash values match
        if (patternHash === textHash) {
            // Check characters one by one
            let j;
            for (j = 0; j < m; j++) {
                if (text[i + j] !== pattern[j]) {
                    break;
                }
            }
            if (j === m) {
                matches.push(i);
            }
        }

        // Calculate hash for next window
        if (i < n - m) {
            textHash = (d * (textHash - text.charCodeAt(i) * h) + text.charCodeAt(i + m)) % prime;
            if (textHash < 0) {
                textHash = textHash + prime;
            }
        }
    }

    return matches;
}

/**
 * Boyer-Moore Pattern Searching
 * Time: O(nm) worst case, O(n/m) best case
 * @param {string} text - Text to search in
 * @param {string} pattern - Pattern to search for
 * @returns {Array<number>} Array of starting indices where pattern is found
 */
export function boyerMooreSearch(text, pattern) {
    if (!pattern || pattern.length === 0) return [];
    if (pattern.length > text.length) return [];

    const matches = [];
    const badCharTable = buildBadCharTable(pattern);
    const n = text.length;
    const m = pattern.length;
    let shift = 0;

    while (shift <= n - m) {
        let j = m - 1;

        while (j >= 0 && pattern[j] === text[shift + j]) {
            j--;
        }

        if (j < 0) {
            matches.push(shift);
            shift += (shift + m < n) ? m - badCharTable[text.charCodeAt(shift + m)] || m : 1;
        } else {
            const badChar = badCharTable[text.charCodeAt(shift + j)];
            shift += Math.max(1, j - (badChar || -1));
        }
    }

    return matches;
}

/**
 * Build bad character table for Boyer-Moore
 * @private
 */
function buildBadCharTable(pattern) {
    const table = {};
    for (let i = 0; i < pattern.length; i++) {
        table[pattern.charCodeAt(i)] = i;
    }
    return table;
}

/**
 * Z-Algorithm for pattern searching
 * Time: O(n + m), Space: O(n)
 * @param {string} text - Text to search in
 * @param {string} pattern - Pattern to search for
 * @returns {Array<number>} Array of starting indices where pattern is found
 */
export function zAlgorithmSearch(text, pattern) {
    if (!pattern || pattern.length === 0) return [];
    if (pattern.length > text.length) return [];

    const concat = pattern + '$' + text;
    const z = buildZArray(concat);
    const matches = [];

    for (let i = 0; i < z.length; i++) {
        if (z[i] === pattern.length) {
            matches.push(i - pattern.length - 1);
        }
    }

    return matches;
}

/**
 * Build Z array
 * @private
 */
function buildZArray(str) {
    const n = str.length;
    const z = new Array(n).fill(0);
    let l = 0, r = 0;

    for (let i = 1; i < n; i++) {
        if (i > r) {
            l = r = i;
            while (r < n && str[r - l] === str[r]) {
                r++;
            }
            z[i] = r - l;
            r--;
        } else {
            const k = i - l;
            if (z[k] < r - i + 1) {
                z[i] = z[k];
            } else {
                l = i;
                while (r < n && str[r - l] === str[r]) {
                    r++;
                }
                z[i] = r - l;
                r--;
            }
        }
    }

    return z;
}

/**
 * Naive pattern searching
 * Time: O(nm), Space: O(1)
 * @param {string} text - Text to search in
 * @param {string} pattern - Pattern to search for
 * @returns {Array<number>} Array of starting indices where pattern is found
 */
export function naiveSearch(text, pattern) {
    const matches = [];
    const n = text.length;
    const m = pattern.length;

    for (let i = 0; i <= n - m; i++) {
        let j;
        for (j = 0; j < m; j++) {
            if (text[i + j] !== pattern[j]) {
                break;
            }
        }
        if (j === m) {
            matches.push(i);
        }
    }

    return matches;
}

/**
 * Levenshtein Distance (Edit Distance)
 * Time: O(nm), Space: O(nm)
 * @param {string} str1 - First string
 * @param {string} str2 - Second string
 * @returns {number} Minimum edit distance
 */
export function levenshteinDistance(str1, str2) {
    const m = str1.length;
    const n = str2.length;
    const dp = Array(m + 1).fill().map(() => Array(n + 1).fill(0));

    // Initialize base cases
    for (let i = 0; i <= m; i++) {
        dp[i][0] = i;
    }
    for (let j = 0; j <= n; j++) {
        dp[0][j] = j;
    }

    // Fill the DP table
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (str1[i - 1] === str2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + Math.min(
                    dp[i - 1][j],     // delete
                    dp[i][j - 1],     // insert
                    dp[i - 1][j - 1]  // replace
                );
            }
        }
    }

    return dp[m][n];
}

/**
 * Hamming Distance
 * Time: O(n), Space: O(1)
 * @param {string} str1 - First string
 * @param {string} str2 - Second string
 * @returns {number} Hamming distance (-1 if different lengths)
 */
export function hammingDistance(str1, str2) {
    if (str1.length !== str2.length) {
        return -1;
    }

    let distance = 0;
    for (let i = 0; i < str1.length; i++) {
        if (str1[i] !== str2[i]) {
            distance++;
        }
    }

    return distance;
}

/**
 * Jaro Distance
 * @param {string} s1 - First string
 * @param {string} s2 - Second string
 * @returns {number} Jaro distance (0 to 1)
 */
export function jaroDistance(s1, s2) {
    if (s1 === s2) return 1;

    const len1 = s1.length;
    const len2 = s2.length;

    if (len1 === 0 || len2 === 0) return 0;

    const matchWindow = Math.floor(Math.max(len1, len2) / 2) - 1;
    const s1Matches = new Array(len1).fill(false);
    const s2Matches = new Array(len2).fill(false);

    let matches = 0;
    let transpositions = 0;

    // Find matches
    for (let i = 0; i < len1; i++) {
        const start = Math.max(0, i - matchWindow);
        const end = Math.min(i + matchWindow + 1, len2);

        for (let j = start; j < end; j++) {
            if (s2Matches[j] || s1[i] !== s2[j]) continue;
            s1Matches[i] = true;
            s2Matches[j] = true;
            matches++;
            break;
        }
    }

    if (matches === 0) return 0;

    // Find transpositions
    let k = 0;
    for (let i = 0; i < len1; i++) {
        if (!s1Matches[i]) continue;
        while (!s2Matches[k]) k++;
        if (s1[i] !== s2[k]) transpositions++;
        k++;
    }

    return (matches / len1 + matches / len2 + (matches - transpositions / 2) / matches) / 3;
}

/**
 * Jaro-Winkler Distance
 * @param {string} s1 - First string
 * @param {string} s2 - Second string
 * @param {number} [p=0.1] - Scaling factor (max 0.25)
 * @returns {number} Jaro-Winkler distance (0 to 1)
 */
export function jaroWinklerDistance(s1, s2, p = 0.1) {
    const jaro = jaroDistance(s1, s2);

    if (jaro === 0) return 0;

    // Find common prefix up to 4 characters
    let prefix = 0;
    for (let i = 0; i < Math.min(s1.length, s2.length, 4); i++) {
        if (s1[i] === s2[i]) {
            prefix++;
        } else {
            break;
        }
    }

    return jaro + prefix * p * (1 - jaro);
}

/**
 * Longest Common Subsequence
 * Time: O(nm), Space: O(nm)
 * @param {string} str1 - First string
 * @param {string} str2 - Second string
 * @returns {string} Longest common subsequence
 */
export function longestCommonSubsequence(str1, str2) {
    const m = str1.length;
    const n = str2.length;
    const dp = Array(m + 1).fill().map(() => Array(n + 1).fill(0));

    // Fill the DP table
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (str1[i - 1] === str2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    // Backtrack to find the LCS
    let lcs = '';
    let i = m, j = n;

    while (i > 0 && j > 0) {
        if (str1[i - 1] === str2[j - 1]) {
            lcs = str1[i - 1] + lcs;
            i--;
            j--;
        } else if (dp[i - 1][j] > dp[i][j - 1]) {
            i--;
        } else {
            j--;
        }
    }

    return lcs;
}

/**
 * Longest Common Substring
 * Time: O(nm), Space: O(nm)
 * @param {string} str1 - First string
 * @param {string} str2 - Second string
 * @returns {string} Longest common substring
 */
export function longestCommonSubstring(str1, str2) {
    const m = str1.length;
    const n = str2.length;
    const dp = Array(m + 1).fill().map(() => Array(n + 1).fill(0));

    let maxLength = 0;
    let endPos = 0;

    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (str1[i - 1] === str2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
                if (dp[i][j] > maxLength) {
                    maxLength = dp[i][j];
                    endPos = i;
                }
            }
        }
    }

    return str1.substring(endPos - maxLength, endPos);
}

/**
 * Check if string is palindrome
 * Time: O(n), Space: O(1)
 * @param {string} str - String to check
 * @returns {boolean} True if palindrome
 */
export function isPalindrome(str) {
    let left = 0;
    let right = str.length - 1;

    while (left < right) {
        if (str[left] !== str[right]) {
            return false;
        }
        left++;
        right--;
    }

    return true;
}

/**
 * Longest Palindromic Substring (Manacher's Algorithm)
 * Time: O(n), Space: O(n)
 * @param {string} s - Input string
 * @returns {string} Longest palindromic substring
 */
export function longestPalindromicSubstring(s) {
    if (!s || s.length < 2) return s;

    // Transform string to avoid even/odd length issues
    let str = '#';
    for (const char of s) {
        str += char + '#';
    }

    const n = str.length;
    const p = new Array(n).fill(0);
    let center = 0;
    let right = 0;
    let maxLen = 0;
    let centerIndex = 0;

    for (let i = 0; i < n; i++) {
        const mirror = 2 * center - i;

        if (i < right) {
            p[i] = Math.min(right - i, p[mirror]);
        }

        // Try to expand palindrome centered at i
        try {
            while (str[i + (1 + p[i])] === str[i - (1 + p[i])]) {
                p[i]++;
            }
        } catch (e) {
            // Out of bounds
        }

        // If palindrome centered at i extends past right
        if (i + p[i] > right) {
            center = i;
            right = i + p[i];
        }

        // Update longest palindrome
        if (p[i] > maxLen) {
            maxLen = p[i];
            centerIndex = i;
        }
    }

    // Extract the longest palindrome
    const start = Math.floor((centerIndex - maxLen) / 2);
    return s.substring(start, start + maxLen);
}

/**
 * Check if two strings are anagrams
 * Time: O(n), Space: O(n)
 * @param {string} str1 - First string
 * @param {string} str2 - Second string
 * @returns {boolean} True if anagrams
 */
export function areAnagrams(str1, str2) {
    if (str1.length !== str2.length) {
        return false;
    }

    const charCount = {};

    for (const char of str1) {
        charCount[char] = (charCount[char] || 0) + 1;
    }

    for (const char of str2) {
        if (!charCount[char]) {
            return false;
        }
        charCount[char]--;
    }

    return true;
}

/**
 * Find all anagrams in a string
 * Time: O(n), Space: O(k) where k is pattern length
 * @param {string} s - String to search in
 * @param {string} p - Pattern
 * @returns {Array<number>} Starting indices of anagrams
 */
export function findAnagrams(s, p) {
    const result = [];
    if (s.length < p.length) return result;

    const charCount = {};
    for (const char of p) {
        charCount[char] = (charCount[char] || 0) + 1;
    }

    let left = 0, right = 0, count = p.length;

    while (right < s.length) {
        if (charCount[s[right]] > 0) {
            count--;
        }
        charCount[s[right]] = (charCount[s[right]] || 0) - 1;
        right++;

        if (count === 0) {
            result.push(left);
        }

        if (right - left === p.length) {
            if (charCount[s[left]] >= 0) {
                count++;
            }
            charCount[s[left]]++;
            left++;
        }
    }

    return result;
}

/**
 * String compression (Run Length Encoding)
 * @param {string} str - String to compress
 * @returns {string} Compressed string
 */
export function compressString(str) {
    if (!str || str.length <= 2) return str;

    let compressed = '';
    let count = 1;

    for (let i = 0; i < str.length; i++) {
        if (i + 1 < str.length && str[i] === str[i + 1]) {
            count++;
        } else {
            compressed += str[i] + count;
            count = 1;
        }
    }

    return compressed.length < str.length ? compressed : str;
}

/**
 * String decompression (Run Length Decoding)
 * @param {string} str - Compressed string
 * @returns {string} Decompressed string
 */
export function decompressString(str) {
    let result = '';
    let i = 0;

    while (i < str.length) {
        const char = str[i];
        i++;

        let numStr = '';
        while (i < str.length && !isNaN(str[i])) {
            numStr += str[i];
            i++;
        }

        const count = parseInt(numStr) || 1;
        result += char.repeat(count);
    }

    return result;
}

/**
 * Reverse words in a string
 * Time: O(n), Space: O(n)
 * @param {string} str - String with words
 * @returns {string} String with reversed words
 */
export function reverseWords(str) {
    return str.split(' ').filter(word => word.length > 0).reverse().join(' ');
}

/**
 * Check if string is rotation of another
 * Time: O(n), Space: O(n)
 * @param {string} s1 - First string
 * @param {string} s2 - Second string
 * @returns {boolean} True if s2 is rotation of s1
 */
export function isRotation(s1, s2) {
    if (s1.length !== s2.length || s1.length === 0) {
        return false;
    }
    return (s1 + s1).includes(s2);
}

/**
 * Generate all permutations of a string
 * Time: O(n!), Space: O(n!)
 * @param {string} str - Input string
 * @returns {Array<string>} All permutations
 */
export function getPermutations(str) {
    if (str.length <= 1) return [str];

    const permutations = [];

    for (let i = 0; i < str.length; i++) {
        const char = str[i];
        const remaining = str.slice(0, i) + str.slice(i + 1);
        const subPermutations = getPermutations(remaining);

        for (const perm of subPermutations) {
            permutations.push(char + perm);
        }
    }

    return permutations;
}

/**
 * Find longest substring without repeating characters
 * Time: O(n), Space: O(min(n, m)) where m is charset size
 * @param {string} s - Input string
 * @returns {string} Longest substring without repeating chars
 */
export function longestSubstringWithoutRepeating(s) {
    const seen = new Map();
    let start = 0;
    let maxLen = 0;
    let maxStart = 0;

    for (let end = 0; end < s.length; end++) {
        if (seen.has(s[end]) && seen.get(s[end]) >= start) {
            start = seen.get(s[end]) + 1;
        }

        seen.set(s[end], end);

        if (end - start + 1 > maxLen) {
            maxLen = end - start + 1;
            maxStart = start;
        }
    }

    return s.substring(maxStart, maxStart + maxLen);
}

/**
 * String hashing using polynomial rolling hash
 * @param {string} str - String to hash
 * @param {number} [prime=31] - Prime base
 * @param {number} [mod=1e9+7] - Modulo value
 * @returns {number} Hash value
 */
export function polynomialHash(str, prime = 31, mod = 1e9 + 7) {
    let hash = 0;
    let pow = 1;

    for (let i = 0; i < str.length; i++) {
        hash = (hash + (str.charCodeAt(i) - 96) * pow) % mod;
        pow = (pow * prime) % mod;
    }

    return hash;
}

/**
 * Check if string matches pattern with wildcards
 * ? matches single character, * matches any sequence
 * @param {string} str - String to match
 * @param {string} pattern - Pattern with wildcards
 * @returns {boolean} True if matches
 */
export function wildcardMatch(str, pattern) {
    const m = str.length;
    const n = pattern.length;
    const dp = Array(m + 1).fill().map(() => Array(n + 1).fill(false));

    dp[0][0] = true;

    // Handle patterns with *
    for (let j = 1; j <= n; j++) {
        if (pattern[j - 1] === '*') {
            dp[0][j] = dp[0][j - 1];
        }
    }

    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (pattern[j - 1] === '*') {
                dp[i][j] = dp[i - 1][j] || dp[i][j - 1];
            } else if (pattern[j - 1] === '?' || str[i - 1] === pattern[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            }
        }
    }

    return dp[m][n];
}

// Export all string algorithms
export default {
    kmpSearch,
    rabinKarpSearch,
    boyerMooreSearch,
    zAlgorithmSearch,
    naiveSearch,
    levenshteinDistance,
    hammingDistance,
    jaroDistance,
    jaroWinklerDistance,
    longestCommonSubsequence,
    longestCommonSubstring,
    isPalindrome,
    longestPalindromicSubstring,
    areAnagrams,
    findAnagrams,
    compressString,
    decompressString,
    reverseWords,
    isRotation,
    getPermutations,
    longestSubstringWithoutRepeating,
    polynomialHash,
    wildcardMatch
};