package com.algorithms.stringalgorithms;

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
 * Compile: javac PatternMatching.java
 * Run: java PatternMatching
 */

import java.util.*;

// ============================================================================
// 1. KNUTH-MORRIS-PRATT (KMP) ALGORITHM
// ============================================================================

/**
 * Knuth-Morris-Pratt (KMP) Pattern Matching Algorithm
 * ===================================================
 *
 * Time Complexity: O(n + m)
 * Space Complexity: O(m)
 *
 * Real-world applications:
 * - Text editors, DNA matching, network packet inspection
 */
class KMP {
    /**
     * Compute LPS (Longest Proper Prefix which is also Suffix) array
     * Time: O(m)
     */
    public static int[] computeLPS(String pattern) {
        int m = pattern.length();
        int[] lps = new int[m];
        int length = 0;
        int i = 1;

        while (i < m) {
            if (pattern.charAt(i) == pattern.charAt(length)) {
                length++;
                lps[i] = length;
                i++;
            } else {
                if (length != 0) {
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
    public static List<Integer> search(String text, String pattern, boolean visualize) {
        if (pattern == null || text == null || pattern.isEmpty() || text.isEmpty()) {
            return new ArrayList<>();
        }

        int n = text.length();
        int m = pattern.length();

        if (m > n) return new ArrayList<>();

        int[] lps = computeLPS(pattern);
        List<Integer> matches = new ArrayList<>();

        int i = 0; // Index for text
        int j = 0; // Index for pattern

        if (visualize) {
            System.out.println("\nKMP Algorithm Visualization:");
            System.out.println("Text:    " + text);
            System.out.println("Pattern: " + pattern);
            System.out.println("LPS:     " + Arrays.toString(lps) + "\n");
        }

        while (i < n) {
            if (visualize && j == 0) {
                int endIdx = Math.min(i + m, n);
                System.out.println("Comparing at position " + i + ": '" + text.substring(i, endIdx) + "'");
            }

            if (pattern.charAt(j) == text.charAt(i)) {
                i++;
                j++;
            }

            if (j == m) {
                matches.add(i - j);
                if (visualize) {
                    System.out.println("✓ Match found at index " + (i - j));
                }
                j = lps[j - 1];
            } else if (i < n && pattern.charAt(j) != text.charAt(i)) {
                if (j != 0) {
                    if (visualize) {
                        System.out.println("  Mismatch at position " + i + ", using LPS to skip to j=" + lps[j - 1]);
                    }
                    j = lps[j - 1];
                } else {
                    i++;
                }
            }
        }

        return matches;
    }

    public static List<Integer> search(String text, String pattern) {
        return search(text, pattern, false);
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
    public static Map<Character, Integer> badCharacterTable(String pattern) {
        Map<Character, Integer> table = new HashMap<>();
        int m = pattern.length();

        for (int i = 0; i < m; i++) {
            table.put(pattern.charAt(i), i);
        }

        return table;
    }

    /**
     * Build good suffix table
     * Time: O(m)
     */
    public static int[] goodSuffixTable(String pattern) {
        int m = pattern.length();
        int[] shift = new int[m + 1];
        int[] border = new int[m + 1];

        int i = m;
        int j = m + 1;
        border[i] = j;

        while (i > 0) {
            while (j <= m && pattern.charAt(i - 1) != pattern.charAt(j - 1)) {
                if (shift[j] == 0) {
                    shift[j] = j - i;
                }
                j = border[j];
            }

            i--;
            j--;
            border[i] = j;
        }

        j = border[0];
        for (i = 0; i <= m; i++) {
            if (shift[i] == 0) {
                shift[i] = j;
            }
            if (i == j) {
                j = border[j];
            }
        }

        return shift;
    }

    /**
     * Find all occurrences using Boyer-Moore
     * Time: O(n) average
     */
    public static List<Integer> search(String text, String pattern, boolean visualize) {
        if (pattern == null || text == null || pattern.isEmpty() || text.isEmpty()) {
            return new ArrayList<>();
        }

        int n = text.length();
        int m = pattern.length();

        if (m > n) return new ArrayList<>();

        Map<Character, Integer> badChar = badCharacterTable(pattern);
        int[] goodSuffix = goodSuffixTable(pattern);

        List<Integer> matches = new ArrayList<>();
        int s = 0;

        if (visualize) {
            System.out.println("\nBoyer-Moore Algorithm Visualization:");
            System.out.println("Text:    " + text);
            System.out.println("Pattern: " + pattern + "\n");
        }

        while (s <= n - m) {
            int j = m - 1;

            if (visualize) {
                System.out.println("Checking at position " + s + ": '" + text.substring(s, s + m) + "'");
            }

            while (j >= 0 && pattern.charAt(j) == text.charAt(s + j)) {
                j--;
            }

            if (j < 0) {
                matches.add(s);
                if (visualize) {
                    System.out.println("✓ Match found at index " + s);
                }
                s += goodSuffix[0];
            } else {
                int badCharShift = j - badChar.getOrDefault(text.charAt(s + j), -1);
                int goodSuffixShift = goodSuffix[j + 1];
                int shift = Math.max(badCharShift, goodSuffixShift);

                if (visualize) {
                    System.out.println("  Mismatch at j=" + j + ", shifting by " + shift);
                }

                s += shift;
            }
        }

        return matches;
    }

    public static List<Integer> search(String text, String pattern) {
        return search(text, pattern, false);
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
    private final int base;
    private final int prime;

    public RabinKarp() {
        this(256, 101);
    }

    public RabinKarp(int base, int prime) {
        this.base = base;
        this.prime = prime;
    }

    /**
     * Compute hash value
     */
    private long hash(String s, int length) {
        long h = 0;
        for (int i = 0; i < length; i++) {
            h = (h * base + s.charAt(i)) % prime;
        }
        return h;
    }

    /**
     * Find all occurrences using Rabin-Karp
     * Time: O(n + m) average
     */
    public List<Integer> search(String text, String pattern, boolean visualize) {
        if (pattern == null || text == null || pattern.isEmpty() || text.isEmpty()) {
            return new ArrayList<>();
        }

        int n = text.length();
        int m = pattern.length();

        if (m > n) return new ArrayList<>();

        long patternHash = hash(pattern, m);
        long textHash = hash(text, m);

        long h = 1;
        for (int i = 0; i < m - 1; i++) {
            h = (h * base) % prime;
        }

        List<Integer> matches = new ArrayList<>();

        if (visualize) {
            System.out.println("\nRabin-Karp Algorithm Visualization:");
            System.out.println("Text:    " + text);
            System.out.println("Pattern: " + pattern);
            System.out.println("Pattern hash: " + patternHash + "\n");
        }

        for (int i = 0; i <= n - m; i++) {
            if (visualize) {
                System.out.println("Position " + i + ": hash=" + textHash + ", substring='" + text.substring(i, i + m) + "'");
            }

            if (patternHash == textHash) {
                if (text.substring(i, i + m).equals(pattern)) {
                    matches.add(i);
                    if (visualize) {
                        System.out.println("  ✓ Match found at index " + i);
                    }
                } else if (visualize) {
                    System.out.println("  ✗ Hash collision, not a real match");
                }
            }

            if (i < n - m) {
                textHash = (base * (textHash - text.charAt(i) * h) + text.charAt(i + m)) % prime;

                if (textHash < 0) {
                    textHash += prime;
                }
            }
        }

        return matches;
    }

    public List<Integer> search(String text, String pattern) {
        return search(text, pattern, false);
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
    private static class TrieNode {
        Map<Character, TrieNode> children = new HashMap<>();
        List<Integer> output = new ArrayList<>();
        TrieNode fail = null;
    }

    private final TrieNode root;
    private final List<String> patterns;

    public AhoCorasick() {
        this.root = new TrieNode();
        this.patterns = new ArrayList<>();
    }

    /**
     * Add pattern to trie
     * Time: O(m)
     */
    public void addPattern(String pattern, Integer patternId) {
        if (patternId == null) {
            patternId = patterns.size();
        }

        patterns.add(pattern);

        TrieNode node = root;
        for (char c : pattern.toCharArray()) {
            node.children.putIfAbsent(c, new TrieNode());
            node = node.children.get(c);
        }

        node.output.add(patternId);
    }

    public void addPattern(String pattern) {
        addPattern(pattern, null);
    }

    /**
     * Build failure links using BFS
     * Time: O(total pattern length)
     */
    public void buildFailureLinks() {
        Queue<TrieNode> queue = new LinkedList<>();

        for (TrieNode child : root.children.values()) {
            child.fail = root;
            queue.offer(child);
        }

        while (!queue.isEmpty()) {
            TrieNode current = queue.poll();

            for (Map.Entry<Character, TrieNode> entry : current.children.entrySet()) {
                char c = entry.getKey();
                TrieNode child = entry.getValue();
                queue.offer(child);

                TrieNode failNode = current.fail;
                while (failNode != null && !failNode.children.containsKey(c)) {
                    failNode = failNode.fail;
                }

                child.fail = (failNode != null) ? failNode.children.get(c) : root;
                child.output.addAll(child.fail.output);
            }
        }
    }

    /**
     * Find all occurrences of all patterns
     * Time: O(n + k)
     */
    public Map<Integer, List<Integer>> search(String text, boolean visualize) {
        if (text == null || text.isEmpty()) {
            return new HashMap<>();
        }

        if (!root.children.isEmpty() && root.children.values().iterator().next().fail == null) {
            buildFailureLinks();
        }

        Map<Integer, List<Integer>> results = new HashMap<>();
        TrieNode current = root;

        if (visualize) {
            System.out.println("\nAho-Corasick Algorithm Visualization:");
            System.out.println("Text: " + text);
            System.out.println("Patterns: " + patterns + "\n");
        }

        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);

            while (current != null && !current.children.containsKey(c)) {
                current = current.fail;
            }

            if (current == null) {
                current = root;
                continue;
            }

            current = current.children.get(c);

            if (!current.output.isEmpty()) {
                for (int patternId : current.output) {
                    int patternLen = patterns.get(patternId).length();
                    int startIdx = i - patternLen + 1;

                    results.putIfAbsent(patternId, new ArrayList<>());
                    results.get(patternId).add(startIdx);

                    if (visualize) {
                        System.out.println("✓ Found pattern '" + patterns.get(patternId) + "' at index " + startIdx);
                    }
                }
            }
        }

        return results;
    }

    public Map<Integer, List<Integer>> search(String text) {
        return search(text, false);
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
    public static int[] computeZArray(String s) {
        int n = s.length();
        int[] z = new int[n];
        z[0] = n;

        int l = 0, r = 0;

        for (int i = 1; i < n; i++) {
            if (i > r) {
                l = r = i;
                while (r < n && s.charAt(r - l) == s.charAt(r)) {
                    r++;
                }
                z[i] = r - l;
                r--;
            } else {
                int k = i - l;
                if (z[k] < r - i + 1) {
                    z[i] = z[k];
                } else {
                    l = i;
                    while (r < n && s.charAt(r - l) == s.charAt(r)) {
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
    public static List<Integer> search(String text, String pattern, boolean visualize) {
        if (pattern == null || text == null || pattern.isEmpty() || text.isEmpty()) {
            return new ArrayList<>();
        }

        int n = text.length();
        int m = pattern.length();

        if (m > n) return new ArrayList<>();

        String concat = pattern + "$" + text;
        int[] z = computeZArray(concat);

        List<Integer> matches = new ArrayList<>();

        if (visualize) {
            System.out.println("\nZ-Algorithm Visualization:");
            System.out.println("Text:    " + text);
            System.out.println("Pattern: " + pattern);
            System.out.println("Concatenation: " + concat);
            System.out.println("Z-array: " + Arrays.toString(z) + "\n");
        }

        for (int i = m + 1; i < concat.length(); i++) {
            if (z[i] == m) {
                int matchPos = i - m - 1;
                matches.add(matchPos);
                if (visualize) {
                    System.out.println("✓ Match found at index " + matchPos + " (Z[" + i + "] = " + m + ")");
                }
            }
        }

        return matches;
    }

    public static List<Integer> search(String text, String pattern) {
        return search(text, pattern, false);
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
    public static class Palindrome {
        public final int start;
        public final int end;
        public final String text;

        public Palindrome(int start, int end, String text) {
            this.start = start;
            this.end = end;
            this.text = text;
        }

        @Override
        public String toString() {
            return "[" + start + ":" + end + "] = '" + text + "'";
        }
    }

    /**
     * Preprocess string to handle even/odd palindromes uniformly
     */
    public static String preprocess(String s) {
        if (s == null || s.isEmpty()) return "#";

        StringBuilder result = new StringBuilder("#");
        for (char c : s.toCharArray()) {
            result.append(c).append('#');
        }
        return result.toString();
    }

    /**
     * Find all palindromes
     * Time: O(n)
     */
    public static List<Palindrome> findAllPalindromes(String s, boolean visualize) {
        if (s == null || s.isEmpty()) {
            return new ArrayList<>();
        }

        String t = preprocess(s);
        int n = t.length();
        int[] p = new int[n];

        int center = 0;
        int right = 0;

        if (visualize) {
            System.out.println("\nManacher's Algorithm Visualization:");
            System.out.println("Original: " + s);
            System.out.println("Transformed: " + t + "\n");
        }

        for (int i = 0; i < n; i++) {
            int mirror = 2 * center - i;

            if (i < right) {
                p[i] = Math.min(right - i, p[mirror]);
            }

            try {
                while (i + p[i] + 1 < n && i - p[i] - 1 >= 0 &&
                       t.charAt(i + p[i] + 1) == t.charAt(i - p[i] - 1)) {
                    p[i]++;
                }
            } catch (Exception e) {}

            if (i + p[i] > right) {
                center = i;
                right = i + p[i];
            }
        }

        List<Palindrome> palindromes = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if (p[i] > 0) {
                int start = (i - p[i]) / 2;
                int end = (i + p[i]) / 2;
                if (start < end) {
                    String palindromeStr = s.substring(start, end);
                    palindromes.add(new Palindrome(start, end, palindromeStr));
                }
            }
        }

        if (visualize) {
            System.out.println("Palindromes found:");
            for (Palindrome pal : palindromes) {
                System.out.println("  " + pal);
            }
        }

        return palindromes;
    }

    public static List<Palindrome> findAllPalindromes(String s) {
        return findAllPalindromes(s, false);
    }

    /**
     * Find longest palindromic substring
     * Time: O(n)
     */
    public static String longestPalindrome(String s) {
        if (s == null || s.isEmpty()) return "";

        String t = preprocess(s);
        int n = t.length();
        int[] p = new int[n];

        int center = 0;
        int right = 0;

        for (int i = 0; i < n; i++) {
            int mirror = 2 * center - i;

            if (i < right) {
                p[i] = Math.min(right - i, p[mirror]);
            }

            try {
                while (i + p[i] + 1 < n && i - p[i] - 1 >= 0 &&
                       t.charAt(i + p[i] + 1) == t.charAt(i - p[i] - 1)) {
                    p[i]++;
                }
            } catch (Exception e) {}

            if (i + p[i] > right) {
                center = i;
                right = i + p[i];
            }
        }

        int maxLen = 0;
        int centerIndex = 0;
        for (int i = 0; i < n; i++) {
            if (p[i] > maxLen) {
                maxLen = p[i];
                centerIndex = i;
            }
        }

        int start = (centerIndex - maxLen) / 2;
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
    public static void benchmarkSinglePattern(String text, String pattern, int iterations) {
        System.out.println("\n" + "=".repeat(70));
        System.out.println("PERFORMANCE BENCHMARK");
        System.out.println("=".repeat(70));
        System.out.println("Text length: " + text.length());
        System.out.println("Pattern length: " + pattern.length());
        System.out.println("Iterations: " + iterations + "\n");

        List<Object[]> algorithms = Arrays.asList(
            new Object[]{"KMP", (Runnable) () -> KMP.search(text, pattern)},
            new Object[]{"Boyer-Moore", (Runnable) () -> BoyerMoore.search(text, pattern)},
            new Object[]{"Rabin-Karp", (Runnable) () -> new RabinKarp().search(text, pattern)},
            new Object[]{"Z-Algorithm", (Runnable) () -> ZAlgorithm.search(text, pattern)}
        );

        List<Object[]> results = new ArrayList<>();

        for (Object[] algo : algorithms) {
            String name = (String) algo[0];
            Runnable func = (Runnable) algo[1];

            long start = System.nanoTime();
            for (int i = 0; i < iterations; i++) {
                func.run();
            }
            long end = System.nanoTime();

            double avgTime = (end - start) / 1_000_000.0 / iterations;
            results.add(new Object[]{name, avgTime});

            System.out.printf("%-15s | %8.4f ms%n", name, avgTime);
        }

        Object[] best = results.stream().min(Comparator.comparingDouble(a -> (double) a[1])).get();
        System.out.printf("%n✓ Fastest: %s (%.4f ms)%n", best[0], (double) best[1]);
    }
}

// ============================================================================
// EXAMPLE USAGE AND TESTING
// ============================================================================

public class PatternMatching {
    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("STRING PATTERN MATCHING ALGORITHMS");
        System.out.println("=".repeat(70));

        String text = "ABABCABABABCABAB";
        String pattern = "ABAB";

        System.out.println("\nTest Text: " + text);
        System.out.println("Pattern: " + pattern + "\n");

        // 1. KMP Algorithm
        System.out.println("\n" + "=".repeat(70));
        System.out.println("1. KMP ALGORITHM");
        System.out.println("=".repeat(70));
        List<Integer> matches = KMP.search(text, pattern, true);
        System.out.println("\nMatches found: " + matches);

        // 2. Boyer-Moore Algorithm
        System.out.println("\n" + "=".repeat(70));
        System.out.println("2. BOYER-MOORE ALGORITHM");
        System.out.println("=".repeat(70));
        matches = BoyerMoore.search(text, pattern, true);
        System.out.println("\nMatches found: " + matches);

        // 3. Rabin-Karp Algorithm
        System.out.println("\n" + "=".repeat(70));
        System.out.println("3. RABIN-KARP ALGORITHM");
        System.out.println("=".repeat(70));
        RabinKarp rk = new RabinKarp();
        matches = rk.search(text, pattern, true);
        System.out.println("\nMatches found: " + matches);

        // 4. Aho-Corasick Algorithm
        System.out.println("\n" + "=".repeat(70));
        System.out.println("4. AHO-CORASICK ALGORITHM (Multiple Patterns)");
        System.out.println("=".repeat(70));
        AhoCorasick ac = new AhoCorasick();
        String[] patterns = {"ABAB", "ABC", "CAB"};
        for (int i = 0; i < patterns.length; i++) {
            ac.addPattern(patterns[i], i);
        }
        ac.buildFailureLinks();
        Map<Integer, List<Integer>> results = ac.search(text, true);
        System.out.println("\nAll matches: " + results);

        // 5. Z-Algorithm
        System.out.println("\n" + "=".repeat(70));
        System.out.println("5. Z-ALGORITHM");
        System.out.println("=".repeat(70));
        matches = ZAlgorithm.search(text, pattern, true);
        System.out.println("\nMatches found: " + matches);

        // 6. Manacher's Algorithm
        System.out.println("\n" + "=".repeat(70));
        System.out.println("6. MANACHER'S ALGORITHM");
        System.out.println("=".repeat(70));
        String palindromeText = "babad";
        String longest = Manacher.longestPalindrome(palindromeText);
        System.out.println("Text: " + palindromeText);
        System.out.println("Longest palindrome: '" + longest + "'");

        List<Manacher.Palindrome> palindromes = Manacher.findAllPalindromes(palindromeText, true);

        // Performance Benchmarking
        System.out.println("\n" + "=".repeat(70));
        System.out.println("PERFORMANCE BENCHMARKING");
        System.out.println("=".repeat(70));

        String benchmarkText = "ABC".repeat(1000);
        String benchmarkPattern = "ABCABC";

        PerformanceBenchmark.benchmarkSinglePattern(benchmarkText, benchmarkPattern, 100);

        System.out.println("\n" + "=".repeat(70));
    }
}

