/**
 * Comprehensive String Pattern Matching Algorithms
 * =================================================
 *
 * This module implements six major pattern matching algorithms with detailed
 * explanations, preprocessing steps, performance analysis, and benchmarking.
 *
 * Algorithms:
 * 1. Knuth-Morris-Pratt (KMP)
 * 2. Boyer-Moore
 * 3. Rabin-Karp
 * 4. Aho-Corasick (multiple pattern matching)
 * 5. Z-algorithm
 * 6. Manacher's algorithm (palindrome detection)
 *
 * Run: node pattern_matching.js
 */

// ============================================================================
// 1. KNUTH-MORRIS-PRATT (KMP) ALGORITHM
// ============================================================================

/**
 * Knuth-Morris-Pratt (KMP) Pattern Matching Algorithm
 * ===================================================
 *
 * Time: O(n + m), Space: O(m)
 *
 * Real-world applications:
 * - Text editors, DNA matching, network packet inspection
 */
class KMP {
    /**
     * Compute LPS (Longest Proper Prefix which is also Suffix) array
     * Time: O(m)
     */
    static computeLPS(pattern) {
        const m = pattern.length;
        const lps = Array(m).fill(0);
        let length = 0;
        let i = 1;

        while (i < m) {
            if (pattern[i] === pattern[length]) {
                length++;
                lps[i] = length;
                i++;
            } else {
                if (length !== 0) {
                    length = lps[length - 1];
                } else {
                    lps[i] = 0;
                    i++;
                }
            }
        }

        return lps;
    }

    /**
     * Find all occurrences of pattern in text
     * Time: O(n + m)
     */
    static search(text, pattern, visualize = false) {
        if (!pattern || !text) return [];

        const n = text.length;
        const m = pattern.length;

        if (m > n) return [];

        const lps = this.computeLPS(pattern);
        const matches = [];

        let i = 0; // Index for text
        let j = 0; // Index for pattern

        if (visualize) {
            console.log('\nKMP Algorithm Visualization:');
            console.log(`Text:    ${text}`);
            console.log(`Pattern: ${pattern}`);
            console.log(`LPS:     [${lps.join(', ')}]\n`);
        }

        while (i < n) {
            if (visualize && j === 0) {
                console.log(`Comparing at position ${i}: '${text.substring(i, i + m)}'`);
            }

            if (pattern[j] === text[i]) {
                i++;
                j++;
            }

            if (j === m) {
                matches.push(i - j);
                if (visualize) {
                    console.log(`✓ Match found at index ${i - j}`);
                }
                j = lps[j - 1];
            } else if (i < n && pattern[j] !== text[i]) {
                if (j !== 0) {
                    if (visualize) {
                        console.log(`  Mismatch at position ${i}, using LPS to skip to j=${lps[j - 1]}`);
                    }
                    j = lps[j - 1];
                } else {
                    i++;
                }
            }
        }

        return matches;
    }
}

// ============================================================================
// 2. BOYER-MOORE ALGORITHM
// ============================================================================

/**
 * Boyer-Moore Pattern Matching Algorithm
 * ======================================
 *
 * Time: Best O(n/m), Average O(n), Worst O(n*m)
 * Space: O(|Σ|)
 *
 * Real-world applications:
 * - GNU grep, text editors, antivirus scanning
 */
class BoyerMoore {
    /**
     * Build bad character table
     * Time: O(m + |Σ|)
     */
    static badCharacterTable(pattern) {
        const table = new Map();
        const m = pattern.length;

        for (let i = 0; i < m; i++) {
            table.set(pattern[i], i);
        }

        return table;
    }

    /**
     * Build good suffix table
     * Time: O(m)
     */
    static goodSuffixTable(pattern) {
        const m = pattern.length;
        const shift = Array(m + 1).fill(0);
        const border = Array(m + 1).fill(0);

        let i = m;
        let j = m + 1;
        border[i] = j;

        while (i > 0) {
            while (j <= m && pattern[i - 1] !== pattern[j - 1]) {
                if (shift[j] === 0) {
                    shift[j] = j - i;
                }
                j = border[j];
            }

            i--;
            j--;
            border[i] = j;
        }

        j = border[0];
        for (let i = 0; i <= m; i++) {
            if (shift[i] === 0) {
                shift[i] = j;
            }
            if (i === j) {
                j = border[j];
            }
        }

        return shift;
    }

    /**
     * Find all occurrences using Boyer-Moore
     * Time: O(n) average
     */
    static search(text, pattern, visualize = false) {
        if (!pattern || !text) return [];

        const n = text.length;
        const m = pattern.length;

        if (m > n) return [];

        const badChar = this.badCharacterTable(pattern);
        const goodSuffix = this.goodSuffixTable(pattern);

        const matches = [];
        let s = 0;

        if (visualize) {
            console.log('\nBoyer-Moore Algorithm Visualization:');
            console.log(`Text:    ${text}`);
            console.log(`Pattern: ${pattern}\n`);
        }

        while (s <= n - m) {
            let j = m - 1;

            if (visualize) {
                console.log(`Checking at position ${s}: '${text.substring(s, s + m)}'`);
            }

            while (j >= 0 && pattern[j] === text[s + j]) {
                j--;
            }

            if (j < 0) {
                matches.push(s);
                if (visualize) {
                    console.log(`✓ Match found at index ${s}`);
                }
                s += goodSuffix[0];
            } else {
                const badCharShift = j - (badChar.get(text[s + j]) || -1);
                const goodSuffixShift = goodSuffix[j + 1];
                const shift = Math.max(badCharShift, goodSuffixShift);

                if (visualize) {
                    console.log(`  Mismatch at j=${j}, shifting by ${shift}`);
                }

                s += shift;
            }
        }

        return matches;
    }
}

// ============================================================================
// 3. RABIN-KARP ALGORITHM
// ============================================================================

/**
 * Rabin-Karp Rolling Hash Algorithm
 * ==================================
 *
 * Time: Average O(n + m), Worst O(n*m)
 * Space: O(1)
 *
 * Real-world applications:
 * - Plagiarism detection, DNA analysis, document similarity
 */
class RabinKarp {
    constructor(base = 256, prime = 101) {
        this.base = base;
        this.prime = prime;
    }

    /**
     * Compute hash value
     */
    hash(s, length) {
        let h = 0;
        for (let i = 0; i < length; i++) {
            h = (h * this.base + s.charCodeAt(i)) % this.prime;
        }
        return h;
    }

    /**
     * Find all occurrences using Rabin-Karp
     * Time: O(n + m) average
     */
    search(text, pattern, visualize = false) {
        if (!pattern || !text) return [];

        const n = text.length;
        const m = pattern.length;

        if (m > n) return [];

        const patternHash = this.hash(pattern, m);
        let textHash = this.hash(text, m);

        const h = Math.pow(this.base, m - 1) % this.prime;

        const matches = [];

        if (visualize) {
            console.log('\nRabin-Karp Algorithm Visualization:');
            console.log(`Text:    ${text}`);
            console.log(`Pattern: ${pattern}`);
            console.log(`Pattern hash: ${patternHash}\n`);
        }

        for (let i = 0; i <= n - m; i++) {
            if (visualize) {
                console.log(`Position ${i}: hash=${textHash}, substring='${text.substring(i, i + m)}'`);
            }

            if (patternHash === textHash) {
                if (text.substring(i, i + m) === pattern) {
                    matches.push(i);
                    if (visualize) {
                        console.log(`  ✓ Match found at index ${i}`);
                    }
                } else if (visualize) {
                    console.log(`  ✗ Hash collision, not a real match`);
                }
            }

            if (i < n - m) {
                textHash = (this.base * (textHash - text.charCodeAt(i) * h) + text.charCodeAt(i + m)) % this.prime;

                if (textHash < 0) {
                    textHash += this.prime;
                }
            }
        }

        return matches;
    }
}

// ============================================================================
// 4. AHO-CORASICK ALGORITHM (MULTIPLE PATTERN MATCHING)
// ============================================================================

/**
 * Aho-Corasick Multiple Pattern Matching Algorithm
 * ================================================
 *
 * Time: O(n + k) where k = number of matches
 * Space: O(sum of pattern lengths)
 *
 * Real-world applications:
 * - Antivirus scanning, network intrusion detection, content filtering
 */
class AhoCorasick {
    constructor() {
        this.root = { children: {}, output: [], fail: null };
        this.patterns = [];
    }

    /**
     * Add pattern to trie
     * Time: O(m)
     */
    addPattern(pattern, patternId = null) {
        if (patternId === null) {
            patternId = this.patterns.length;
        }

        this.patterns.push(pattern);

        let node = this.root;
        for (const char of pattern) {
            if (!node.children[char]) {
                node.children[char] = { children: {}, output: [], fail: null };
            }
            node = node.children[char];
        }

        node.output.push(patternId);
    }

    /**
     * Build failure links using BFS
     * Time: O(total pattern length)
     */
    buildFailureLinks() {
        const queue = [];

        for (const child of Object.values(this.root.children)) {
            child.fail = this.root;
            queue.push(child);
        }

        while (queue.length > 0) {
            const current = queue.shift();

            for (const [char, child] of Object.entries(current.children)) {
                queue.push(child);

                let failNode = current.fail;
                while (failNode !== null && !failNode.children[char]) {
                    failNode = failNode.fail;
                }

                child.fail = failNode ? failNode.children[char] : this.root;
                child.output = [...child.output, ...child.fail.output];
            }
        }
    }

    /**
     * Find all occurrences of all patterns
     * Time: O(n + k)
     */
    search(text, visualize = false) {
        if (!text) return {};

        if (Object.keys(this.root.children).length > 0 &&
            Object.values(this.root.children)[0].fail === null) {
            this.buildFailureLinks();
        }

        const results = {};
        let current = this.root;

        if (visualize) {
            console.log('\nAho-Corasick Algorithm Visualization:');
            console.log(`Text: ${text}`);
            console.log(`Patterns: [${this.patterns.map(p => `'${p}'`).join(', ')}]\n`);
        }

        for (let i = 0; i < text.length; i++) {
            const char = text[i];

            while (current !== null && !current.children[char]) {
                current = current.fail;
            }

            if (current === null) {
                current = this.root;
                continue;
            }

            current = current.children[char];

            if (current.output.length > 0) {
                for (const patternId of current.output) {
                    const patternLen = this.patterns[patternId].length;
                    const startIdx = i - patternLen + 1;

                    if (!results[patternId]) {
                        results[patternId] = [];
                    }
                    results[patternId].push(startIdx);

                    if (visualize) {
                        console.log(`✓ Found pattern '${this.patterns[patternId]}' at index ${startIdx}`);
                    }
                }
            }
        }

        return results;
    }
}

// ============================================================================
// 5. Z-ALGORITHM
// ============================================================================

/**
 * Z-Algorithm for Pattern Matching
 * =================================
 *
 * Time: O(n + m), Space: O(n + m)
 *
 * Real-world applications:
 * - Pattern matching, string processing, compression
 */
class ZAlgorithm {
    /**
     * Compute Z-array
     * Time: O(n)
     */
    static computeZArray(s) {
        const n = s.length;
        const z = Array(n).fill(0);
        z[0] = n;

        let l = 0, r = 0;

        for (let i = 1; i < n; i++) {
            if (i > r) {
                l = r = i;
                while (r < n && s[r - l] === s[r]) {
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
                    while (r < n && s[r - l] === s[r]) {
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
     * Find all occurrences using Z-algorithm
     * Time: O(n + m)
     */
    static search(text, pattern, visualize = false) {
        if (!pattern || !text) return [];

        const n = text.length;
        const m = pattern.length;

        if (m > n) return [];

        const concat = pattern + '$' + text;
        const z = this.computeZArray(concat);

        const matches = [];

        if (visualize) {
            console.log('\nZ-Algorithm Visualization:');
            console.log(`Text:    ${text}`);
            console.log(`Pattern: ${pattern}`);
            console.log(`Concatenation: ${concat}`);
            console.log(`Z-array: [${z.join(', ')}]\n`);
        }

        for (let i = m + 1; i < concat.length; i++) {
            if (z[i] === m) {
                const matchPos = i - m - 1;
                matches.push(matchPos);
                if (visualize) {
                    console.log(`✓ Match found at index ${matchPos} (Z[${i}] = ${m})`);
                }
            }
        }

        return matches;
    }
}

// ============================================================================
// 6. MANACHER'S ALGORITHM (PALINDROME DETECTION)
// ============================================================================

/**
 * Manacher's Algorithm for Finding Palindromes
 * ============================================
 *
 * Time: O(n), Space: O(n)
 *
 * Real-world applications:
 * - DNA analysis, text compression, NLP
 */
class Manacher {
    /**
     * Preprocess string to handle even/odd palindromes uniformly
     */
    static preprocess(s) {
        if (!s) return '#';

        let result = '#';
        for (const char of s) {
            result += char + '#';
        }
        return result;
    }

    /**
     * Find all palindromes
     * Time: O(n)
     */
    static findAllPalindromes(s, visualize = false) {
        if (!s) return [];

        const t = this.preprocess(s);
        const n = t.length;
        const p = Array(n).fill(0);

        let center = 0;
        let right = 0;

        if (visualize) {
            console.log('\nManacher\'s Algorithm Visualization:');
            console.log(`Original: ${s}`);
            console.log(`Transformed: ${t}\n`);
        }

        for (let i = 0; i < n; i++) {
            const mirror = 2 * center - i;

            if (i < right) {
                p[i] = Math.min(right - i, p[mirror]);
            }

            try {
                while (i + p[i] + 1 < n && i - p[i] - 1 >= 0 &&
                       t[i + p[i] + 1] === t[i - p[i] - 1]) {
                    p[i]++;
                }
            } catch (e) {}

            if (i + p[i] > right) {
                center = i;
                right = i + p[i];
            }
        }

        const palindromes = [];
        for (let i = 0; i < n; i++) {
            if (p[i] > 0) {
                const start = Math.floor((i - p[i]) / 2);
                const end = Math.floor((i + p[i]) / 2);
                if (start < end) {
                    const palindromeStr = s.substring(start, end);
                    palindromes.push({ start, end, palindrome: palindromeStr });
                }
            }
        }

        if (visualize) {
            console.log('Palindromes found:');
            for (const { start, end, palindrome } of palindromes) {
                console.log(`  [${start}:${end}] = '${palindrome}'`);
            }
        }

        return palindromes;
    }

    /**
     * Find longest palindromic substring
     * Time: O(n)
     */
    static longestPalindrome(s) {
        if (!s) return '';

        const t = this.preprocess(s);
        const n = t.length;
        const p = Array(n).fill(0);

        let center = 0;
        let right = 0;

        for (let i = 0; i < n; i++) {
            const mirror = 2 * center - i;

            if (i < right) {
                p[i] = Math.min(right - i, p[mirror]);
            }

            try {
                while (i + p[i] + 1 < n && i - p[i] - 1 >= 0 &&
                       t[i + p[i] + 1] === t[i - p[i] - 1]) {
                    p[i]++;
                }
            } catch (e) {}

            if (i + p[i] > right) {
                center = i;
                right = i + p[i];
            }
        }

        let maxLen = 0;
        let centerIndex = 0;
        for (let i = 0; i < n; i++) {
            if (p[i] > maxLen) {
                maxLen = p[i];
                centerIndex = i;
            }
        }

        const start = Math.floor((centerIndex - maxLen) / 2);
        return s.substring(start, start + maxLen);
    }
}

// ============================================================================
// PERFORMANCE BENCHMARKING
// ============================================================================

class PerformanceBenchmark {
    /**
     * Benchmark single-pattern algorithms
     */
    static benchmarkSinglePattern(text, pattern, iterations = 100) {
        console.log('\n' + '='.repeat(70));
        console.log('PERFORMANCE BENCHMARK');
        console.log('='.repeat(70));
        console.log(`Text length: ${text.length}`);
        console.log(`Pattern length: ${pattern.length}`);
        console.log(`Iterations: ${iterations}\n`);

        const algorithms = [
            ['KMP', () => KMP.search(text, pattern)],
            ['Boyer-Moore', () => BoyerMoore.search(text, pattern)],
            ['Rabin-Karp', () => new RabinKarp().search(text, pattern)],
            ['Z-Algorithm', () => ZAlgorithm.search(text, pattern)],
        ];

        const results = [];

        for (const [name, func] of algorithms) {
            const start = performance.now();
            let matches;
            for (let i = 0; i < iterations; i++) {
                matches = func();
            }
            const end = performance.now();

            const avgTime = (end - start) / iterations;
            results.push([name, avgTime, matches.length]);

            console.log(`${name.padEnd(15)} | ${avgTime.toFixed(4).padStart(8)} ms | ${matches.length} matches`);
        }

        const best = results.reduce((min, curr) => curr[1] < min[1] ? curr : min);
        console.log(`\n✓ Fastest: ${best[0]} (${best[1].toFixed(4)} ms)`);

        return results;
    }
}

// ============================================================================
// EXAMPLE USAGE AND TESTING
// ============================================================================

console.log('='.repeat(70));
console.log('STRING PATTERN MATCHING ALGORITHMS');
console.log('='.repeat(70));

const text = 'ABABCABABABCABAB';
const pattern = 'ABAB';

console.log(`\nTest Text: ${text}`);
console.log(`Pattern: ${pattern}\n`);

// 1. KMP Algorithm
console.log('\n' + '='.repeat(70));
console.log('1. KMP ALGORITHM');
console.log('='.repeat(70));
let matches = KMP.search(text, pattern, true);
console.log(`\nMatches found: [${matches.join(', ')}]`);

// 2. Boyer-Moore Algorithm
console.log('\n' + '='.repeat(70));
console.log('2. BOYER-MOORE ALGORITHM');
console.log('='.repeat(70));
matches = BoyerMoore.search(text, pattern, true);
console.log(`\nMatches found: [${matches.join(', ')}]`);

// 3. Rabin-Karp Algorithm
console.log('\n' + '='.repeat(70));
console.log('3. RABIN-KARP ALGORITHM');
console.log('='.repeat(70));
const rk = new RabinKarp();
matches = rk.search(text, pattern, true);
console.log(`\nMatches found: [${matches.join(', ')}]`);

// 4. Aho-Corasick Algorithm
console.log('\n' + '='.repeat(70));
console.log('4. AHO-CORASICK ALGORITHM (Multiple Patterns)');
console.log('='.repeat(70));
const ac = new AhoCorasick();
const patterns = ['ABAB', 'ABC', 'CAB'];
patterns.forEach((p, i) => ac.addPattern(p, i));
ac.buildFailureLinks();
const results = ac.search(text, true);
console.log(`\nAll matches: ${JSON.stringify(results)}`);

// 5. Z-Algorithm
console.log('\n' + '='.repeat(70));
console.log('5. Z-ALGORITHM');
console.log('='.repeat(70));
matches = ZAlgorithm.search(text, pattern, true);
console.log(`\nMatches found: [${matches.join(', ')}]`);

// 6. Manacher's Algorithm
console.log('\n' + '='.repeat(70));
console.log('6. MANACHER\'S ALGORITHM');
console.log('='.repeat(70));
const palindromeText = 'babad';
const longest = Manacher.longestPalindrome(palindromeText);
console.log(`Text: ${palindromeText}`);
console.log(`Longest palindrome: '${longest}'`);

const palindromes = Manacher.findAllPalindromes(palindromeText, true);

// Performance Benchmarking
console.log('\n' + '='.repeat(70));
console.log('PERFORMANCE BENCHMARKING');
console.log('='.repeat(70));

const benchmarkText = 'ABC'.repeat(1000);
const benchmarkPattern = 'ABCABC';

PerformanceBenchmark.benchmarkSinglePattern(benchmarkText, benchmarkPattern, 100);

console.log('\n' + '='.repeat(70));

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        KMP,
        BoyerMoore,
        RabinKarp,
        AhoCorasick,
        ZAlgorithm,
        Manacher,
        PerformanceBenchmark
    };
}
