/**
 * String Algorithms in TypeScript
 * ================================
 *
 * Advanced string manipulation and pattern matching algorithms:
 * - Pattern matching algorithms
 * - String transformation
 * - Text processing utilities
 *
 * @module stringAlgorithms
 * @author Algorithms Multiverse
 */

/**
 * String Algorithm Implementations
 */
export class StringAlgorithms {
    /**
     * Knuth-Morris-Pratt (KMP) Pattern Matching
     */
    static kmpSearch(text: string, pattern: string): number[] {
        if (pattern.length === 0) return [];

        const lps = this.computeLPSArray(pattern);
        const matches: number[] = [];
        let i = 0; // Index for text
        let j = 0; // Index for pattern

        while (i < text.length) {
            if (text[i] === pattern[j]) {
                i++;
                j++;
            }

            if (j === pattern.length) {
                matches.push(i - j);
                j = lps[j - 1];
            } else if (i < text.length && text[i] !== pattern[j]) {
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
     * Compute LPS (Longest Proper Prefix which is also Suffix) array
     */
    private static computeLPSArray(pattern: string): number[] {
        const lps: number[] = new Array(pattern.length).fill(0);
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
     * Rabin-Karp Algorithm (Rolling Hash)
     */
    static rabinKarpSearch(text: string, pattern: string): number[] {
        const matches: number[] = [];
        const d = 256; // Number of characters in input alphabet
        const q = 101; // A prime number
        const m = pattern.length;
        const n = text.length;
        let patternHash = 0;
        let textHash = 0;
        let h = 1;

        // Calculate h = d^(m-1) % q
        for (let i = 0; i < m - 1; i++) {
            h = (h * d) % q;
        }

        // Calculate initial hash values
        for (let i = 0; i < m; i++) {
            patternHash = (d * patternHash + pattern.charCodeAt(i)) % q;
            textHash = (d * textHash + text.charCodeAt(i)) % q;
        }

        // Slide the pattern over text
        for (let i = 0; i <= n - m; i++) {
            if (patternHash === textHash) {
                // Check characters one by one
                let match = true;
                for (let j = 0; j < m; j++) {
                    if (text[i + j] !== pattern[j]) {
                        match = false;
                        break;
                    }
                }
                if (match) {
                    matches.push(i);
                }
            }

            // Calculate hash for next window
            if (i < n - m) {
                textHash = (d * (textHash - text.charCodeAt(i) * h) + text.charCodeAt(i + m)) % q;
                if (textHash < 0) {
                    textHash += q;
                }
            }
        }

        return matches;
    }

    /**
     * Boyer-Moore Algorithm
     */
    static boyerMooreSearch(text: string, pattern: string): number[] {
        const matches: number[] = [];
        const badChar = this.buildBadCharTable(pattern);
        const m = pattern.length;
        const n = text.length;
        let shift = 0;

        while (shift <= n - m) {
            let j = m - 1;

            while (j >= 0 && pattern[j] === text[shift + j]) {
                j--;
            }

            if (j < 0) {
                matches.push(shift);
                shift += (shift + m < n) ? m - badChar[text.charCodeAt(shift + m)] : 1;
            } else {
                const charCode = text.charCodeAt(shift + j);
                shift += Math.max(1, j - badChar[charCode]);
            }
        }

        return matches;
    }

    /**
     * Build bad character table for Boyer-Moore
     */
    private static buildBadCharTable(pattern: string): number[] {
        const table: number[] = new Array(256).fill(-1);

        for (let i = 0; i < pattern.length; i++) {
            table[pattern.charCodeAt(i)] = i;
        }

        return table;
    }

    /**
     * Z-Algorithm for pattern matching
     */
    static zAlgorithm(text: string, pattern: string): number[] {
        const concat = pattern + "$" + text;
        const z = this.computeZArray(concat);
        const matches: number[] = [];

        for (let i = 0; i < z.length; i++) {
            if (z[i] === pattern.length) {
                matches.push(i - pattern.length - 1);
            }
        }

        return matches;
    }

    /**
     * Compute Z array
     */
    private static computeZArray(s: string): number[] {
        const n = s.length;
        const z: number[] = new Array(n).fill(0);
        let left = 0, right = 0;

        for (let i = 1; i < n; i++) {
            if (i > right) {
                left = right = i;
                while (right < n && s[right - left] === s[right]) {
                    right++;
                }
                z[i] = right - left;
                right--;
            } else {
                const k = i - left;
                if (z[k] < right - i + 1) {
                    z[i] = z[k];
                } else {
                    left = i;
                    while (right < n && s[right - left] === s[right]) {
                        right++;
                    }
                    z[i] = right - left;
                    right--;
                }
            }
        }

        return z;
    }

    /**
     * Manacher's Algorithm - Find all palindromes
     */
    static manacher(s: string): string {
        // Preprocess string
        let processed = "#";
        for (const char of s) {
            processed += char + "#";
        }

        const n = processed.length;
        const p: number[] = new Array(n).fill(0);
        let center = 0, right = 0;
        let maxLen = 0, maxCenter = 0;

        for (let i = 0; i < n; i++) {
            const mirror = 2 * center - i;

            if (i < right) {
                p[i] = Math.min(right - i, p[mirror]);
            }

            // Expand around center
            let a = i + p[i] + 1;
            let b = i - p[i] - 1;
            while (a < n && b >= 0 && processed[a] === processed[b]) {
                p[i]++;
                a++;
                b--;
            }

            // Update center and right
            if (i + p[i] > right) {
                center = i;
                right = i + p[i];
            }

            // Update longest palindrome
            if (p[i] > maxLen) {
                maxLen = p[i];
                maxCenter = i;
            }
        }

        // Extract palindrome
        const start = (maxCenter - maxLen) / 2;
        return s.substring(start, start + maxLen);
    }

    /**
     * Longest Common Prefix of array of strings
     */
    static longestCommonPrefix(strs: string[]): string {
        if (strs.length === 0) return "";
        if (strs.length === 1) return strs[0];

        let prefix = strs[0];

        for (let i = 1; i < strs.length; i++) {
            while (!strs[i].startsWith(prefix)) {
                prefix = prefix.substring(0, prefix.length - 1);
                if (prefix === "") return "";
            }
        }

        return prefix;
    }

    /**
     * Check if string is an anagram
     */
    static isAnagram(s1: string, s2: string): boolean {
        if (s1.length !== s2.length) return false;

        const charCount = new Map<string, number>();

        for (const char of s1) {
            charCount.set(char, (charCount.get(char) || 0) + 1);
        }

        for (const char of s2) {
            const count = charCount.get(char) || 0;
            if (count === 0) return false;
            charCount.set(char, count - 1);
        }

        return true;
    }

    /**
     * Generate all permutations of a string
     */
    static generatePermutations(s: string): string[] {
        const results: string[] = [];

        const permute = (chars: string[], start: number): void => {
            if (start === chars.length - 1) {
                results.push(chars.join(''));
                return;
            }

            for (let i = start; i < chars.length; i++) {
                [chars[start], chars[i]] = [chars[i], chars[start]];
                permute(chars, start + 1);
                [chars[start], chars[i]] = [chars[i], chars[start]]; // Backtrack
            }
        };

        permute(s.split(''), 0);
        return results;
    }

    /**
     * Check if string is a palindrome
     */
    static isPalindrome(s: string): boolean {
        let left = 0;
        let right = s.length - 1;

        while (left < right) {
            if (s[left] !== s[right]) return false;
            left++;
            right--;
        }

        return true;
    }

    /**
     * Reverse words in a string
     */
    static reverseWords(s: string): string {
        return s.split(' ').filter(word => word.length > 0).reverse().join(' ');
    }

    /**
     * Group anagrams together
     */
    static groupAnagrams(strs: string[]): string[][] {
        const groups = new Map<string, string[]>();

        for (const str of strs) {
            const key = str.split('').sort().join('');
            if (!groups.has(key)) {
                groups.set(key, []);
            }
            groups.get(key)!.push(str);
        }

        return Array.from(groups.values());
    }

    /**
     * Find the shortest palindrome by adding characters
     */
    static shortestPalindrome(s: string): string {
        const rev = s.split('').reverse().join('');
        const combined = s + "#" + rev;
        const lps = this.computeLPSArray(combined);

        const charactersToAdd = s.length - lps[lps.length - 1];
        const prefix = s.substring(s.length - charactersToAdd).split('').reverse().join('');

        return prefix + s;
    }

    /**
     * Minimum window substring containing all characters
     */
    static minWindow(s: string, t: string): string {
        if (s.length === 0 || t.length === 0) return "";

        const dictT = new Map<string, number>();
        for (const char of t) {
            dictT.set(char, (dictT.get(char) || 0) + 1);
        }

        const required = dictT.size;
        let left = 0, right = 0;
        let formed = 0;

        const windowCounts = new Map<string, number>();
        let ans: [number, number, number] = [-1, 0, 0]; // [window length, left, right]

        while (right < s.length) {
            const char = s[right];
            windowCounts.set(char, (windowCounts.get(char) || 0) + 1);

            if (dictT.has(char) && windowCounts.get(char) === dictT.get(char)) {
                formed++;
            }

            while (left <= right && formed === required) {
                const char = s[left];

                if (ans[0] === -1 || right - left + 1 < ans[0]) {
                    ans = [right - left + 1, left, right];
                }

                windowCounts.set(char, windowCounts.get(char)! - 1);
                if (dictT.has(char) && windowCounts.get(char)! < dictT.get(char)!) {
                    formed--;
                }

                left++;
            }

            right++;
        }

        return ans[0] === -1 ? "" : s.substring(ans[1], ans[2] + 1);
    }

    /**
     * Longest Repeating Character Replacement
     */
    static characterReplacement(s: string, k: number): number {
        const count = new Map<string, number>();
        let maxCount = 0;
        let maxLength = 0;
        let left = 0;

        for (let right = 0; right < s.length; right++) {
            const char = s[right];
            count.set(char, (count.get(char) || 0) + 1);
            maxCount = Math.max(maxCount, count.get(char)!);

            if (right - left + 1 - maxCount > k) {
                const leftChar = s[left];
                count.set(leftChar, count.get(leftChar)! - 1);
                left++;
            }

            maxLength = Math.max(maxLength, right - left + 1);
        }

        return maxLength;
    }
}

/**
 * String Utilities
 */
export class StringUtils {
    /**
     * Convert string to camelCase
     */
    static toCamelCase(str: string): string {
        return str
            .replace(/[-_\s]+(.)?/g, (_, char) => char ? char.toUpperCase() : '')
            .replace(/^[A-Z]/, char => char.toLowerCase());
    }

    /**
     * Convert string to snake_case
     */
    static toSnakeCase(str: string): string {
        return str
            .replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`)
            .replace(/^_/, '')
            .replace(/[-\s]+/g, '_');
    }

    /**
     * Convert string to kebab-case
     */
    static toKebabCase(str: string): string {
        return str
            .replace(/[A-Z]/g, letter => `-${letter.toLowerCase()}`)
            .replace(/^-/, '')
            .replace(/[\s_]+/g, '-');
    }

    /**
     * Truncate string with ellipsis
     */
    static truncate(str: string, maxLength: number, suffix = '...'): string {
        if (str.length <= maxLength) return str;
        return str.substring(0, maxLength - suffix.length) + suffix;
    }

    /**
     * Count occurrences of substring
     */
    static countOccurrences(str: string, substring: string): number {
        if (substring.length === 0) return 0;
        let count = 0;
        let pos = 0;

        while ((pos = str.indexOf(substring, pos)) !== -1) {
            count++;
            pos += substring.length;
        }

        return count;
    }

    /**
     * Capitalize first letter of each word
     */
    static capitalize(str: string): string {
        return str.replace(/\b\w/g, char => char.toUpperCase());
    }

    /**
     * Remove duplicate characters
     */
    static removeDuplicates(str: string): string {
        return [...new Set(str)].join('');
    }

    /**
     * Check if string is a valid email
     */
    static isValidEmail(email: string): boolean {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Levenshtein distance between two strings
     */
    static levenshteinDistance(s1: string, s2: string): number {
        const m = s1.length;
        const n = s2.length;
        const dp: number[][] = Array(m + 1).fill(0).map(() => Array(n + 1).fill(0));

        for (let i = 0; i <= m; i++) dp[i][0] = i;
        for (let j = 0; j <= n; j++) dp[0][j] = j;

        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                if (s1[i - 1] === s2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
                }
            }
        }

        return dp[m][n];
    }
}

// Example usage and tests
if (require.main === module) {
    console.log("TypeScript String Algorithms Demonstration");
    console.log("=" .repeat(50));

    const text = "ABABDABACDABABCABAB";
    const pattern = "ABABCABAB";

    console.log("\n1. Pattern Matching Algorithms:");
    console.log("Text:", text);
    console.log("Pattern:", pattern);
    console.log("KMP matches:", StringAlgorithms.kmpSearch(text, pattern));
    console.log("Rabin-Karp matches:", StringAlgorithms.rabinKarpSearch(text, pattern));
    console.log("Boyer-Moore matches:", StringAlgorithms.boyerMooreSearch(text, pattern));
    console.log("Z-Algorithm matches:", StringAlgorithms.zAlgorithm(text, pattern));

    console.log("\n2. Palindrome Algorithms:");
    const palindromeStr = "babad";
    console.log(`Longest palindrome in "${palindromeStr}":`, StringAlgorithms.manacher(palindromeStr));
    console.log(`Is "racecar" palindrome:`, StringAlgorithms.isPalindrome("racecar"));

    console.log("\n3. String Transformations:");
    const testStr = "hello world from typescript";
    console.log("Original:", testStr);
    console.log("CamelCase:", StringUtils.toCamelCase(testStr));
    console.log("snake_case:", StringUtils.toSnakeCase("HelloWorldFromTypescript"));
    console.log("kebab-case:", StringUtils.toKebabCase("HelloWorldFromTypescript"));
    console.log("Capitalized:", StringUtils.capitalize(testStr));
    console.log("Reversed words:", StringAlgorithms.reverseWords(testStr));

    console.log("\n4. Anagrams:");
    const strs = ["eat", "tea", "tan", "ate", "nat", "bat"];
    console.log("Strings:", strs);
    console.log("Grouped anagrams:", StringAlgorithms.groupAnagrams(strs));
    console.log("Is 'listen' anagram of 'silent':", StringAlgorithms.isAnagram("listen", "silent"));

    console.log("\n5. String Utilities:");
    console.log("Count 'AB' in text:", StringUtils.countOccurrences(text, "AB"));
    console.log("Remove duplicates from 'aabbccdd':", StringUtils.removeDuplicates("aabbccdd"));
    console.log("Levenshtein('kitten', 'sitting'):", StringUtils.levenshteinDistance("kitten", "sitting"));

    console.log("\n6. Permutations:");
    const permStr = "ABC";
    console.log(`Permutations of "${permStr}":`, StringAlgorithms.generatePermutations(permStr));

    console.log("\n7. Common Prefix:");
    const prefixStrs = ["flower", "flow", "flight"];
    console.log("Strings:", prefixStrs);
    console.log("Longest common prefix:", StringAlgorithms.longestCommonPrefix(prefixStrs));

    console.log("\n8. Window Problems:");
    const s = "ADOBECODEBANC";
    const t = "ABC";
    console.log(`Minimum window in "${s}" containing "${t}":`, StringAlgorithms.minWindow(s, t));
}