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
 * Compile: g++ -std=c++17 -O3 -o pattern_matching pattern_matching.cpp
 * Run: ./pattern_matching
 */

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <queue>
#include <algorithm>
#include <chrono>
#include <iomanip>
#include <functional>
#include <memory>

using namespace std;

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
public:
    /**
     * Compute LPS (Longest Proper Prefix which is also Suffix) array
     * Time: O(m)
     */
    static vector<int> computeLPS(const string& pattern) {
        int m = pattern.length();
        vector<int> lps(m, 0);
        int length = 0;
        int i = 1;

        while (i < m) {
            if (pattern[i] == pattern[length]) {
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
    static vector<int> search(const string& text, const string& pattern, bool visualize = false) {
        if (pattern.empty() || text.empty()) {
            return vector<int>();
        }

        int n = text.length();
        int m = pattern.length();

        if (m > n) return vector<int>();

        vector<int> lps = computeLPS(pattern);
        vector<int> matches;

        int i = 0; // Index for text
        int j = 0; // Index for pattern

        if (visualize) {
            cout << "\nKMP Algorithm Visualization:" << endl;
            cout << "Text:    " << text << endl;
            cout << "Pattern: " << pattern << endl;
            cout << "LPS:     [";
            for (size_t k = 0; k < lps.size(); k++) {
                cout << lps[k];
                if (k < lps.size() - 1) cout << ", ";
            }
            cout << "]\n" << endl;
        }

        while (i < n) {
            if (visualize && j == 0) {
                cout << "Comparing at position " << i << ": '"
                     << text.substr(i, min(m, n - i)) << "'" << endl;
            }

            if (pattern[j] == text[i]) {
                i++;
                j++;
            }

            if (j == m) {
                matches.push_back(i - j);
                if (visualize) {
                    cout << "✓ Match found at index " << (i - j) << endl;
                }
                j = lps[j - 1];
            } else if (i < n && pattern[j] != text[i]) {
                if (j != 0) {
                    if (visualize) {
                        cout << "  Mismatch at position " << i
                             << ", using LPS to skip to j=" << lps[j - 1] << endl;
                    }
                    j = lps[j - 1];
                } else {
                    i++;
                }
            }
        }

        return matches;
    }
};

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
public:
    /**
     * Build bad character table
     * Time: O(m + |Σ|)
     */
    static unordered_map<char, int> badCharacterTable(const string& pattern) {
        unordered_map<char, int> table;
        int m = pattern.length();

        for (int i = 0; i < m; i++) {
            table[pattern[i]] = i;
        }

        return table;
    }

    /**
     * Build good suffix table
     * Time: O(m)
     */
    static vector<int> goodSuffixTable(const string& pattern) {
        int m = pattern.length();
        vector<int> shift(m + 1, 0);
        vector<int> border(m + 1, 0);

        int i = m;
        int j = m + 1;
        border[i] = j;

        while (i > 0) {
            while (j <= m && pattern[i - 1] != pattern[j - 1]) {
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
    static vector<int> search(const string& text, const string& pattern, bool visualize = false) {
        if (pattern.empty() || text.empty()) {
            return vector<int>();
        }

        int n = text.length();
        int m = pattern.length();

        if (m > n) return vector<int>();

        auto badChar = badCharacterTable(pattern);
        auto goodSuffix = goodSuffixTable(pattern);

        vector<int> matches;
        int s = 0;

        if (visualize) {
            cout << "\nBoyer-Moore Algorithm Visualization:" << endl;
            cout << "Text:    " << text << endl;
            cout << "Pattern: " << pattern << "\n" << endl;
        }

        while (s <= n - m) {
            int j = m - 1;

            if (visualize) {
                cout << "Checking at position " << s << ": '"
                     << text.substr(s, m) << "'" << endl;
            }

            while (j >= 0 && pattern[j] == text[s + j]) {
                j--;
            }

            if (j < 0) {
                matches.push_back(s);
                if (visualize) {
                    cout << "✓ Match found at index " << s << endl;
                }
                s += goodSuffix[0];
            } else {
                int badCharShift = j - (badChar.count(text[s + j]) ? badChar[text[s + j]] : -1);
                int goodSuffixShift = goodSuffix[j + 1];
                int shift = max(badCharShift, goodSuffixShift);

                if (visualize) {
                    cout << "  Mismatch at j=" << j << ", shifting by " << shift << endl;
                }

                s += shift;
            }
        }

        return matches;
    }
};

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
private:
    int base;
    int prime;

public:
    RabinKarp(int base = 256, int prime = 101) : base(base), prime(prime) {}

    /**
     * Compute hash value
     */
    long long hash(const string& s, int length) const {
        long long h = 0;
        for (int i = 0; i < length; i++) {
            h = (h * base + s[i]) % prime;
        }
        return h;
    }

    /**
     * Find all occurrences using Rabin-Karp
     * Time: O(n + m) average
     */
    vector<int> search(const string& text, const string& pattern, bool visualize = false) const {
        if (pattern.empty() || text.empty()) {
            return vector<int>();
        }

        int n = text.length();
        int m = pattern.length();

        if (m > n) return vector<int>();

        long long patternHash = hash(pattern, m);
        long long textHash = hash(text, m);

        long long h = 1;
        for (int i = 0; i < m - 1; i++) {
            h = (h * base) % prime;
        }

        vector<int> matches;

        if (visualize) {
            cout << "\nRabin-Karp Algorithm Visualization:" << endl;
            cout << "Text:    " << text << endl;
            cout << "Pattern: " << pattern << endl;
            cout << "Pattern hash: " << patternHash << "\n" << endl;
        }

        for (int i = 0; i <= n - m; i++) {
            if (visualize) {
                cout << "Position " << i << ": hash=" << textHash
                     << ", substring='" << text.substr(i, m) << "'" << endl;
            }

            if (patternHash == textHash) {
                if (text.substr(i, m) == pattern) {
                    matches.push_back(i);
                    if (visualize) {
                        cout << "  ✓ Match found at index " << i << endl;
                    }
                } else if (visualize) {
                    cout << "  ✗ Hash collision, not a real match" << endl;
                }
            }

            if (i < n - m) {
                textHash = (base * (textHash - text[i] * h) + text[i + m]) % prime;

                if (textHash < 0) {
                    textHash += prime;
                }
            }
        }

        return matches;
    }
};

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
private:
    struct TrieNode {
        unordered_map<char, shared_ptr<TrieNode>> children;
        vector<int> output;
        shared_ptr<TrieNode> fail;

        TrieNode() : fail(nullptr) {}
    };

    shared_ptr<TrieNode> root;
    vector<string> patterns;

public:
    AhoCorasick() : root(make_shared<TrieNode>()) {}

    /**
     * Add pattern to trie
     * Time: O(m)
     */
    void addPattern(const string& pattern, int patternId = -1) {
        if (patternId == -1) {
            patternId = patterns.size();
        }

        patterns.push_back(pattern);

        auto node = root;
        for (char c : pattern) {
            if (node->children.find(c) == node->children.end()) {
                node->children[c] = make_shared<TrieNode>();
            }
            node = node->children[c];
        }

        node->output.push_back(patternId);
    }

    /**
     * Build failure links using BFS
     * Time: O(total pattern length)
     */
    void buildFailureLinks() {
        queue<shared_ptr<TrieNode>> q;

        for (auto& [c, child] : root->children) {
            child->fail = root;
            q.push(child);
        }

        while (!q.empty()) {
            auto current = q.front();
            q.pop();

            for (auto& [c, child] : current->children) {
                q.push(child);

                auto failNode = current->fail;
                while (failNode && failNode->children.find(c) == failNode->children.end()) {
                    failNode = failNode->fail;
                }

                child->fail = (failNode) ? failNode->children[c] : root;
                child->output.insert(child->output.end(),
                                    child->fail->output.begin(),
                                    child->fail->output.end());
            }
        }
    }

    /**
     * Find all occurrences of all patterns
     * Time: O(n + k)
     */
    unordered_map<int, vector<int>> search(const string& text, bool visualize = false) {
        if (text.empty()) {
            return unordered_map<int, vector<int>>();
        }

        if (!root->children.empty() && root->children.begin()->second->fail == nullptr) {
            buildFailureLinks();
        }

        unordered_map<int, vector<int>> results;
        auto current = root;

        if (visualize) {
            cout << "\nAho-Corasick Algorithm Visualization:" << endl;
            cout << "Text: " << text << endl;
            cout << "Patterns: [";
            for (size_t i = 0; i < patterns.size(); i++) {
                cout << "'" << patterns[i] << "'";
                if (i < patterns.size() - 1) cout << ", ";
            }
            cout << "]\n" << endl;
        }

        for (size_t i = 0; i < text.length(); i++) {
            char c = text[i];

            while (current && current->children.find(c) == current->children.end()) {
                current = current->fail;
            }

            if (!current) {
                current = root;
                continue;
            }

            current = current->children[c];

            if (!current->output.empty()) {
                for (int patternId : current->output) {
                    int patternLen = patterns[patternId].length();
                    int startIdx = i - patternLen + 1;

                    results[patternId].push_back(startIdx);

                    if (visualize) {
                        cout << "✓ Found pattern '" << patterns[patternId]
                             << "' at index " << startIdx << endl;
                    }
                }
            }
        }

        return results;
    }
};

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
public:
    /**
     * Compute Z-array
     * Time: O(n)
     */
    static vector<int> computeZArray(const string& s) {
        int n = s.length();
        vector<int> z(n, 0);
        z[0] = n;

        int l = 0, r = 0;

        for (int i = 1; i < n; i++) {
            if (i > r) {
                l = r = i;
                while (r < n && s[r - l] == s[r]) {
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
                    while (r < n && s[r - l] == s[r]) {
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
    static vector<int> search(const string& text, const string& pattern, bool visualize = false) {
        if (pattern.empty() || text.empty()) {
            return vector<int>();
        }

        int n = text.length();
        int m = pattern.length();

        if (m > n) return vector<int>();

        string concat = pattern + "$" + text;
        vector<int> z = computeZArray(concat);

        vector<int> matches;

        if (visualize) {
            cout << "\nZ-Algorithm Visualization:" << endl;
            cout << "Text:    " << text << endl;
            cout << "Pattern: " << pattern << endl;
            cout << "Concatenation: " << concat << endl;
            cout << "Z-array: [";
            for (size_t i = 0; i < z.size(); i++) {
                cout << z[i];
                if (i < z.size() - 1) cout << ", ";
            }
            cout << "]\n" << endl;
        }

        for (size_t i = m + 1; i < concat.length(); i++) {
            if (z[i] == m) {
                int matchPos = i - m - 1;
                matches.push_back(matchPos);
                if (visualize) {
                    cout << "✓ Match found at index " << matchPos
                         << " (Z[" << i << "] = " << m << ")" << endl;
                }
            }
        }

        return matches;
    }
};

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
public:
    struct Palindrome {
        int start;
        int end;
        string text;

        Palindrome(int s, int e, const string& t) : start(s), end(e), text(t) {}
    };

    /**
     * Preprocess string to handle even/odd palindromes uniformly
     */
    static string preprocess(const string& s) {
        if (s.empty()) return "#";

        string result = "#";
        for (char c : s) {
            result += c;
            result += '#';
        }
        return result;
    }

    /**
     * Find all palindromes
     * Time: O(n)
     */
    static vector<Palindrome> findAllPalindromes(const string& s, bool visualize = false) {
        if (s.empty()) {
            return vector<Palindrome>();
        }

        string t = preprocess(s);
        int n = t.length();
        vector<int> p(n, 0);

        int center = 0;
        int right = 0;

        if (visualize) {
            cout << "\nManacher's Algorithm Visualization:" << endl;
            cout << "Original: " << s << endl;
            cout << "Transformed: " << t << "\n" << endl;
        }

        for (int i = 0; i < n; i++) {
            int mirror = 2 * center - i;

            if (i < right) {
                p[i] = min(right - i, p[mirror]);
            }

            try {
                while (i + p[i] + 1 < n && i - p[i] - 1 >= 0 &&
                       t[i + p[i] + 1] == t[i - p[i] - 1]) {
                    p[i]++;
                }
            } catch (...) {}

            if (i + p[i] > right) {
                center = i;
                right = i + p[i];
            }
        }

        vector<Palindrome> palindromes;
        for (int i = 0; i < n; i++) {
            if (p[i] > 0) {
                int start = (i - p[i]) / 2;
                int end = (i + p[i]) / 2;
                if (start < end) {
                    string palindromeStr = s.substr(start, end - start);
                    palindromes.emplace_back(start, end, palindromeStr);
                }
            }
        }

        if (visualize) {
            cout << "Palindromes found:" << endl;
            for (const auto& pal : palindromes) {
                cout << "  [" << pal.start << ":" << pal.end
                     << "] = '" << pal.text << "'" << endl;
            }
        }

        return palindromes;
    }

    /**
     * Find longest palindromic substring
     * Time: O(n)
     */
    static string longestPalindrome(const string& s) {
        if (s.empty()) return "";

        string t = preprocess(s);
        int n = t.length();
        vector<int> p(n, 0);

        int center = 0;
        int right = 0;

        for (int i = 0; i < n; i++) {
            int mirror = 2 * center - i;

            if (i < right) {
                p[i] = min(right - i, p[mirror]);
            }

            try {
                while (i + p[i] + 1 < n && i - p[i] - 1 >= 0 &&
                       t[i + p[i] + 1] == t[i - p[i] - 1]) {
                    p[i]++;
                }
            } catch (...) {}

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
        return s.substr(start, maxLen);
    }
};

// ============================================================================
// PERFORMANCE BENCHMARKING
// ============================================================================

class PerformanceBenchmark {
public:
    /**
     * Benchmark single-pattern algorithms
     */
    static void benchmarkSinglePattern(const string& text, const string& pattern, int iterations) {
        cout << "\n" << string(70, '=') << endl;
        cout << "PERFORMANCE BENCHMARK" << endl;
        cout << string(70, '=') << endl;
        cout << "Text length: " << text.length() << endl;
        cout << "Pattern length: " << pattern.length() << endl;
        cout << "Iterations: " << iterations << "\n" << endl;

        vector<pair<string, function<void()>>> algorithms = {
            {"KMP", [&]() { KMP::search(text, pattern); }},
            {"Boyer-Moore", [&]() { BoyerMoore::search(text, pattern); }},
            {"Rabin-Karp", [&]() { RabinKarp().search(text, pattern); }},
            {"Z-Algorithm", [&]() { ZAlgorithm::search(text, pattern); }}
        };

        vector<pair<string, double>> results;

        for (const auto& [name, func] : algorithms) {
            auto start = chrono::high_resolution_clock::now();
            for (int i = 0; i < iterations; i++) {
                func();
            }
            auto end = chrono::high_resolution_clock::now();

            double avgTime = chrono::duration<double, milli>(end - start).count() / iterations;
            results.emplace_back(name, avgTime);

            cout << left << setw(15) << name << " | "
                 << fixed << setprecision(4) << setw(8) << avgTime << " ms" << endl;
        }

        auto best = *min_element(results.begin(), results.end(),
                                [](const auto& a, const auto& b) { return a.second < b.second; });
        cout << "\n✓ Fastest: " << best.first << " (" << fixed << setprecision(4) << best.second << " ms)" << endl;
    }
};

// ============================================================================
// EXAMPLE USAGE AND TESTING
// ============================================================================

int main() {
    cout << string(70, '=') << endl;
    cout << "STRING PATTERN MATCHING ALGORITHMS" << endl;
    cout << string(70, '=') << endl;

    string text = "ABABCABABABCABAB";
    string pattern = "ABAB";

    cout << "\nTest Text: " << text << endl;
    cout << "Pattern: " << pattern << "\n" << endl;

    // 1. KMP Algorithm
    cout << "\n" << string(70, '=') << endl;
    cout << "1. KMP ALGORITHM" << endl;
    cout << string(70, '=') << endl;
    auto matches = KMP::search(text, pattern, true);
    cout << "\nMatches found: [";
    for (size_t i = 0; i < matches.size(); i++) {
        cout << matches[i];
        if (i < matches.size() - 1) cout << ", ";
    }
    cout << "]" << endl;

    // 2. Boyer-Moore Algorithm
    cout << "\n" << string(70, '=') << endl;
    cout << "2. BOYER-MOORE ALGORITHM" << endl;
    cout << string(70, '=') << endl;
    matches = BoyerMoore::search(text, pattern, true);
    cout << "\nMatches found: [";
    for (size_t i = 0; i < matches.size(); i++) {
        cout << matches[i];
        if (i < matches.size() - 1) cout << ", ";
    }
    cout << "]" << endl;

    // 3. Rabin-Karp Algorithm
    cout << "\n" << string(70, '=') << endl;
    cout << "3. RABIN-KARP ALGORITHM" << endl;
    cout << string(70, '=') << endl;
    RabinKarp rk;
    matches = rk.search(text, pattern, true);
    cout << "\nMatches found: [";
    for (size_t i = 0; i < matches.size(); i++) {
        cout << matches[i];
        if (i < matches.size() - 1) cout << ", ";
    }
    cout << "]" << endl;

    // 4. Aho-Corasick Algorithm
    cout << "\n" << string(70, '=') << endl;
    cout << "4. AHO-CORASICK ALGORITHM (Multiple Patterns)" << endl;
    cout << string(70, '=') << endl;
    AhoCorasick ac;
    vector<string> patterns = {"ABAB", "ABC", "CAB"};
    for (size_t i = 0; i < patterns.size(); i++) {
        ac.addPattern(patterns[i], i);
    }
    ac.buildFailureLinks();
    auto results = ac.search(text, true);
    cout << "\nAll matches: {";
    bool first = true;
    for (const auto& [id, indices] : results) {
        if (!first) cout << ", ";
        cout << id << ": [";
        for (size_t i = 0; i < indices.size(); i++) {
            cout << indices[i];
            if (i < indices.size() - 1) cout << ", ";
        }
        cout << "]";
        first = false;
    }
    cout << "}" << endl;

    // 5. Z-Algorithm
    cout << "\n" << string(70, '=') << endl;
    cout << "5. Z-ALGORITHM" << endl;
    cout << string(70, '=') << endl;
    matches = ZAlgorithm::search(text, pattern, true);
    cout << "\nMatches found: [";
    for (size_t i = 0; i < matches.size(); i++) {
        cout << matches[i];
        if (i < matches.size() - 1) cout << ", ";
    }
    cout << "]" << endl;

    // 6. Manacher's Algorithm
    cout << "\n" << string(70, '=') << endl;
    cout << "6. MANACHER'S ALGORITHM" << endl;
    cout << string(70, '=') << endl;
    string palindromeText = "babad";
    string longest = Manacher::longestPalindrome(palindromeText);
    cout << "Text: " << palindromeText << endl;
    cout << "Longest palindrome: '" << longest << "'" << endl;

    auto palindromes = Manacher::findAllPalindromes(palindromeText, true);

    // Performance Benchmarking
    cout << "\n" << string(70, '=') << endl;
    cout << "PERFORMANCE BENCHMARKING" << endl;
    cout << string(70, '=') << endl;

    string benchmarkText;
    for (int i = 0; i < 1000; i++) {
        benchmarkText += "ABC";
    }
    string benchmarkPattern = "ABCABC";

    PerformanceBenchmark::benchmarkSinglePattern(benchmarkText, benchmarkPattern, 100);

    cout << "\n" << string(70, '=') << endl;

    return 0;
}
