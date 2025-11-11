/**
 * Edit Distance Algorithms - JavaScript Implementation
 * ====================================================
 *
 * String similarity and edit distance metrics.
 *
 * Algorithms:
 * - Hamming distance
 * - Levenshtein distance (standard & space-optimized)
 * - Damerau-Levenshtein distance
 * - Longest Common Subsequence (LCS)
 * - Jaro & Jaro-Winkler distances
 *
 * Run: node edit_distance.js
 */

/**
 * Edit Distance Algorithms
 */
class EditDistance {
    /**
     * Hamming Distance - Number of positions at which symbols differ
     * Time: O(n), Space: O(1)
     */
    static hamming(str1, str2) {
        if (str1.length !== str2.length) {
            throw new Error('Hamming distance requires equal length strings');
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
     * Levenshtein Distance - Minimum edits (insert, delete, substitute)
     * Time: O(nm), Space: O(nm)
     */
    static levenshtein(str1, str2, visualize = false) {
        const m = str1.length;
        const n = str2.length;

        // Create DP table
        const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

        // Initialize base cases
        for (let i = 0; i <= m; i++) {
            dp[i][0] = i;
        }
        for (let j = 0; j <= n; j++) {
            dp[0][j] = j;
        }

        // Fill DP table
        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                const cost = str1[i - 1] === str2[j - 1] ? 0 : 1;

                dp[i][j] = Math.min(
                    dp[i - 1][j] + 1,      // deletion
                    dp[i][j - 1] + 1,      // insertion
                    dp[i - 1][j - 1] + cost // substitution
                );
            }
        }

        if (visualize) {
            EditDistance._visualizeDPTable(str1, str2, dp);
        }

        return dp[m][n];
    }

    /**
     * Space-optimized Levenshtein distance
     * Time: O(nm), Space: O(min(n,m))
     */
    static levenshteinOptimized(str1, str2) {
        // Ensure str1 is shorter
        if (str1.length > str2.length) {
            [str1, str2] = [str2, str1];
        }

        const m = str1.length;
        const n = str2.length;

        // Use two rows
        let prevRow = Array(n + 1).fill(0).map((_, i) => i);
        let currRow = Array(n + 1).fill(0);

        for (let i = 1; i <= m; i++) {
            currRow[0] = i;

            for (let j = 1; j <= n; j++) {
                const cost = str1[i - 1] === str2[j - 1] ? 0 : 1;

                currRow[j] = Math.min(
                    prevRow[j] + 1,        // deletion
                    currRow[j - 1] + 1,    // insertion
                    prevRow[j - 1] + cost  // substitution
                );
            }

            [prevRow, currRow] = [currRow, prevRow];
        }

        return prevRow[n];
    }

    /**
     * Damerau-Levenshtein Distance - Adds transposition operation
     * Time: O(nm), Space: O(nm)
     */
    static damerauLevenshtein(str1, str2) {
        const m = str1.length;
        const n = str2.length;

        const maxDist = m + n;
        const H = {};

        // Initialize
        H[-1] = {};
        H[-1][-1] = maxDist;

        for (let i = 0; i <= m; i++) {
            H[i] = {};
            H[i][-1] = maxDist;
            H[i][0] = i;
        }

        for (let j = 0; j <= n; j++) {
            H[-1][j] = maxDist;
            H[0][j] = j;
        }

        for (let i = 1; i <= m; i++) {
            let DB = 0;

            for (let j = 1; j <= n; j++) {
                let k = DB;
                const l = str1[i - 1] === str2[j - 1] ? 0 : 1;

                if (str1[i - 1] === str2[j - 1]) {
                    DB = j;
                }

                H[i][j] = Math.min(
                    H[i - 1][j] + 1,           // deletion
                    H[i][j - 1] + 1,           // insertion
                    H[i - 1][j - 1] + l,       // substitution
                    H[k - 1][DB - 1] + (i - k - 1) + 1 + (j - DB - 1) // transposition
                );
            }
        }

        return H[m][n];
    }

    /**
     * Longest Common Subsequence length
     * Time: O(nm), Space: O(nm)
     */
    static lcsLength(str1, str2) {
        const m = str1.length;
        const n = str2.length;

        const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                if (str1[i - 1] === str2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }

        return dp[m][n];
    }

    /**
     * Return the actual Longest Common Subsequence
     * Time: O(nm), Space: O(nm)
     */
    static lcsString(str1, str2) {
        const m = str1.length;
        const n = str2.length;

        const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                if (str1[i - 1] === str2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }

        // Backtrack to find LCS
        const lcs = [];
        let i = m, j = n;

        while (i > 0 && j > 0) {
            if (str1[i - 1] === str2[j - 1]) {
                lcs.unshift(str1[i - 1]);
                i--;
                j--;
            } else if (dp[i - 1][j] > dp[i][j - 1]) {
                i--;
            } else {
                j--;
            }
        }

        return lcs.join('');
    }

    /**
     * Get sequence of edit operations
     * Returns: Array of {operation, position, character}
     */
    static editSequence(str1, str2) {
        const m = str1.length;
        const n = str2.length;

        const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
        const ops = Array(m + 1).fill(null).map(() => Array(n + 1).fill(null));

        for (let i = 0; i <= m; i++) {
            dp[i][0] = i;
            if (i > 0) {
                ops[i][0] = {op: 'delete', pos: i - 1, char: str1[i - 1]};
            }
        }

        for (let j = 0; j <= n; j++) {
            dp[0][j] = j;
            if (j > 0) {
                ops[0][j] = {op: 'insert', pos: j - 1, char: str2[j - 1]};
            }
        }

        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                if (str1[i - 1] === str2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1];
                    ops[i][j] = {op: 'match', pos: i - 1, char: str1[i - 1]};
                } else {
                    const costs = [
                        {cost: dp[i - 1][j] + 1, op: 'delete', pos: i - 1, char: str1[i - 1]},
                        {cost: dp[i][j - 1] + 1, op: 'insert', pos: j - 1, char: str2[j - 1]},
                        {cost: dp[i - 1][j - 1] + 1, op: 'substitute', pos: i - 1, char: str2[j - 1]}
                    ];

                    const minCost = costs.reduce((min, curr) => curr.cost < min.cost ? curr : min);
                    dp[i][j] = minCost.cost;
                    ops[i][j] = {op: minCost.op, pos: minCost.pos, char: minCost.char};
                }
            }
        }

        // Backtrack to get sequence
        const sequence = [];
        let i = m, j = n;

        while (i > 0 || j > 0) {
            if (ops[i][j]) {
                sequence.unshift(ops[i][j]);

                const opType = ops[i][j].op;
                if (opType === 'match' || opType === 'substitute') {
                    i--;
                    j--;
                } else if (opType === 'delete') {
                    i--;
                } else if (opType === 'insert') {
                    j--;
                }
            } else {
                break;
            }
        }

        return sequence;
    }

    /**
     * Visualize DP table
     * @private
     */
    static _visualizeDPTable(str1, str2, dp) {
        console.log('\nDP Table:');
        console.log('='.repeat(70));

        // Header
        process.stdout.write('       ');
        for (const c of str2) {
            process.stdout.write(`${c.padStart(4)}`);
        }
        console.log();

        // Rows
        for (let i = 0; i < dp.length; i++) {
            if (i === 0) {
                process.stdout.write('  ');
            } else {
                process.stdout.write(`${str1[i - 1].padStart(2)}`);
            }

            for (const val of dp[i]) {
                process.stdout.write(`${val.toString().padStart(4)}`);
            }
            console.log();
        }
    }
}

/**
 * String Similarity Metrics
 */
class SimilarityMetrics {
    /**
     * Normalized Levenshtein distance (0 to 1)
     * 1.0 = identical, 0.0 = completely different
     */
    static normalizedLevenshtein(str1, str2) {
        if (!str1 && !str2) {
            return 1.0;
        }

        const distance = EditDistance.levenshtein(str1, str2);
        const maxLen = Math.max(str1.length, str2.length);

        return 1.0 - (distance / maxLen);
    }

    /**
     * Similarity ratio based on LCS
     * Returns: 2 * LCS / (len(str1) + len(str2))
     */
    static similarityRatio(str1, str2) {
        if (!str1 && !str2) {
            return 1.0;
        }

        const lcsLen = EditDistance.lcsLength(str1, str2);
        const totalLen = str1.length + str2.length;

        if (totalLen === 0) {
            return 1.0;
        }

        return 2.0 * lcsLen / totalLen;
    }

    /**
     * Jaro distance - Good for short strings like names
     * Time: O(nm)
     * Returns: 0.0 to 1.0 (1.0 = identical)
     */
    static jaroDistance(str1, str2) {
        if (str1 === str2) {
            return 1.0;
        }

        const len1 = str1.length;
        const len2 = str2.length;

        if (len1 === 0 || len2 === 0) {
            return 0.0;
        }

        // Maximum allowed distance
        let matchDistance = Math.floor(Math.max(len1, len2) / 2) - 1;
        if (matchDistance < 1) {
            matchDistance = 1;
        }

        const str1Matches = Array(len1).fill(false);
        const str2Matches = Array(len2).fill(false);

        let matches = 0;
        let transpositions = 0;

        // Find matches
        for (let i = 0; i < len1; i++) {
            const start = Math.max(0, i - matchDistance);
            const end = Math.min(i + matchDistance + 1, len2);

            for (let j = start; j < end; j++) {
                if (str2Matches[j] || str1[i] !== str2[j]) {
                    continue;
                }
                str1Matches[i] = true;
                str2Matches[j] = true;
                matches++;
                break;
            }
        }

        if (matches === 0) {
            return 0.0;
        }

        // Find transpositions
        let k = 0;
        for (let i = 0; i < len1; i++) {
            if (!str1Matches[i]) {
                continue;
            }
            while (!str2Matches[k]) {
                k++;
            }
            if (str1[i] !== str2[k]) {
                transpositions++;
            }
            k++;
        }

        return (matches / len1 + matches / len2 +
                (matches - transpositions / 2) / matches) / 3.0;
    }

    /**
     * Jaro-Winkler distance - Gives more weight to common prefix
     * Time: O(nm)
     * Returns: 0.0 to 1.0 (1.0 = identical)
     */
    static jaroWinklerDistance(str1, str2, prefixScale = 0.1) {
        const jaro = SimilarityMetrics.jaroDistance(str1, str2);

        // Find common prefix length (max 4)
        let prefix = 0;
        const minLen = Math.min(str1.length, str2.length, 4);

        for (let i = 0; i < minLen; i++) {
            if (str1[i] === str2[i]) {
                prefix++;
            } else {
                break;
            }
        }

        return jaro + prefix * prefixScale * (1 - jaro);
    }
}

// ============================================================================
// EXAMPLE USAGE AND TESTING
// ============================================================================

if (require.main === module) {
    console.log('='.repeat(70));
    console.log('EDIT DISTANCE ALGORITHMS - JAVASCRIPT');
    console.log('='.repeat(70));

    // Example 1: Hamming distance
    console.log('\n' + '='.repeat(70));
    console.log('EXAMPLE 1: Hamming Distance');
    console.log('='.repeat(70));

    const str1 = 'karolin';
    const str2 = 'kathrin';
    const dist = EditDistance.hamming(str1, str2);

    console.log(`String 1: '${str1}'`);
    console.log(`String 2: '${str2}'`);
    console.log(`Hamming distance: ${dist}`);

    // Example 2: Levenshtein distance
    console.log('\n' + '='.repeat(70));
    console.log('EXAMPLE 2: Levenshtein Distance');
    console.log('='.repeat(70));

    const str3 = 'kitten';
    const str4 = 'sitting';
    const dist2 = EditDistance.levenshtein(str3, str4, true);

    console.log(`\nString 1: '${str3}'`);
    console.log(`String 2: '${str4}'`);
    console.log(`Levenshtein distance: ${dist2}`);

    // Example 3: Damerau-Levenshtein
    console.log('\n' + '='.repeat(70));
    console.log('EXAMPLE 3: Damerau-Levenshtein Distance');
    console.log('='.repeat(70));

    const testCases = [
        ['kitten', 'sitting'],
        ['teh', 'the'],
        ['abcd', 'acbd']
    ];

    for (const [s1, s2] of testCases) {
        const levDist = EditDistance.levenshtein(s1, s2);
        const damLevDist = EditDistance.damerauLevenshtein(s1, s2);

        console.log(`\nString 1: '${s1}'`);
        console.log(`String 2: '${s2}'`);
        console.log(`  Levenshtein:         ${levDist}`);
        console.log(`  Damerau-Levenshtein: ${damLevDist}`);
    }

    // Example 4: LCS
    console.log('\n' + '='.repeat(70));
    console.log('EXAMPLE 4: Longest Common Subsequence');
    console.log('='.repeat(70));

    const str5 = 'ABCDGH';
    const str6 = 'AEDFHR';
    const lcs = EditDistance.lcsString(str5, str6);

    console.log(`String 1: '${str5}'`);
    console.log(`String 2: '${str6}'`);
    console.log(`LCS: '${lcs}' (length: ${lcs.length})`);

    // Example 5: Edit sequence
    console.log('\n' + '='.repeat(70));
    console.log('EXAMPLE 5: Edit Sequence');
    console.log('='.repeat(70));

    const str7 = 'saturday';
    const str8 = 'sunday';
    const sequence = EditDistance.editSequence(str7, str8);

    console.log(`String 1: '${str7}'`);
    console.log(`String 2: '${str8}'`);
    console.log('\nEdit operations:');

    for (const {op, pos, char} of sequence) {
        if (op !== 'match') {
            console.log(`  ${op.padEnd(12)} at position ${pos}: '${char}'`);
        }
    }

    // Example 6: Similarity metrics
    console.log('\n' + '='.repeat(70));
    console.log('EXAMPLE 6: Similarity Metrics');
    console.log('='.repeat(70));

    const testPairs = [
        ['kitten', 'sitting'],
        ['saturday', 'sunday'],
        ['martha', 'marhta'],
        ['dixon', 'dicksonx']
    ];

    for (const [s1, s2] of testPairs) {
        const normLev = SimilarityMetrics.normalizedLevenshtein(s1, s2);
        const simRatio = SimilarityMetrics.similarityRatio(s1, s2);
        const jaro = SimilarityMetrics.jaroDistance(s1, s2);
        const jaroWinkler = SimilarityMetrics.jaroWinklerDistance(s1, s2);

        console.log(`\n'${s1}' vs '${s2}':`);
        console.log(`  Normalized Levenshtein: ${normLev.toFixed(4)}`);
        console.log(`  Similarity Ratio:       ${simRatio.toFixed(4)}`);
        console.log(`  Jaro:                   ${jaro.toFixed(4)}`);
        console.log(`  Jaro-Winkler:           ${jaroWinkler.toFixed(4)}`);
    }

    // Example 7: Spell checking simulation
    console.log('\n' + '='.repeat(70));
    console.log('EXAMPLE 7: Spell Checking Simulation');
    console.log('='.repeat(70));

    const dictionary = ['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'lazy', 'dog'];
    const misspelled = 'quikc';

    console.log(`Misspelled word: '${misspelled}'`);
    console.log(`Dictionary: ${JSON.stringify(dictionary)}\n`);

    const suggestions = [];
    for (const word of dictionary) {
        const distance = EditDistance.levenshtein(misspelled, word);
        suggestions.push({word, distance});
    }

    suggestions.sort((a, b) => a.distance - b.distance);

    console.log('Suggestions (sorted by edit distance):');
    for (const {word, distance} of suggestions.slice(0, 5)) {
        console.log(`  '${word}' (distance: ${distance})`);
    }

    console.log('\n' + '='.repeat(70));
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        EditDistance,
        SimilarityMetrics
    };
}
