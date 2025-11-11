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
 * Compile: rustc -O pattern_matching.rs
 * Run: ./pattern_matching
 */

use std::collections::{HashMap, VecDeque};
use std::time::Instant;

// ============================================================================
// 1. KNUTH-MORRIS-PRATT (KMP) ALGORITHM
// ============================================================================

/// Knuth-Morris-Pratt (KMP) Pattern Matching Algorithm
/// Time: O(n + m), Space: O(m)
pub struct KMP;

impl KMP {
    /// Compute LPS (Longest Proper Prefix which is also Suffix) array
    /// Time: O(m)
    pub fn compute_lps(pattern: &str) -> Vec<usize> {
        let pattern_bytes = pattern.as_bytes();
        let m = pattern_bytes.len();
        let mut lps = vec![0; m];
        let mut length = 0;
        let mut i = 1;

        while i < m {
            if pattern_bytes[i] == pattern_bytes[length] {
                length += 1;
                lps[i] = length;
                i += 1;
            } else {
                if length != 0 {
                    length = lps[length - 1];
                } else {
                    lps[i] = 0;
                    i += 1;
                }
            }
        }

        lps
    }

    /// Find all occurrences of pattern in text
    /// Time: O(n + m)
    pub fn search(text: &str, pattern: &str, visualize: bool) -> Vec<usize> {
        if pattern.is_empty() || text.is_empty() {
            return Vec::new();
        }

        let text_bytes = text.as_bytes();
        let pattern_bytes = pattern.as_bytes();
        let n = text_bytes.len();
        let m = pattern_bytes.len();

        if m > n {
            return Vec::new();
        }

        let lps = Self::compute_lps(pattern);
        let mut matches = Vec::new();

        let mut i = 0; // Index for text
        let mut j = 0; // Index for pattern

        if visualize {
            println!("\nKMP Algorithm Visualization:");
            println!("Text:    {}", text);
            println!("Pattern: {}", pattern);
            println!("LPS:     {:?}\n", lps);
        }

        while i < n {
            if visualize && j == 0 {
                let end_idx = std::cmp::min(i + m, n);
                println!("Comparing at position {}: '{}'", i, &text[i..end_idx]);
            }

            if pattern_bytes[j] == text_bytes[i] {
                i += 1;
                j += 1;
            }

            if j == m {
                matches.push(i - j);
                if visualize {
                    println!("✓ Match found at index {}", i - j);
                }
                j = lps[j - 1];
            } else if i < n && pattern_bytes[j] != text_bytes[i] {
                if j != 0 {
                    if visualize {
                        println!("  Mismatch at position {}, using LPS to skip to j={}", i, lps[j - 1]);
                    }
                    j = lps[j - 1];
                } else {
                    i += 1;
                }
            }
        }

        matches
    }
}

// ============================================================================
// 2. BOYER-MOORE ALGORITHM
// ============================================================================

/// Boyer-Moore Pattern Matching Algorithm
/// Time: Best O(n/m), Average O(n), Worst O(n*m)
pub struct BoyerMoore;

impl BoyerMoore {
    /// Build bad character table
    /// Time: O(m + |Σ|)
    pub fn bad_character_table(pattern: &str) -> HashMap<u8, usize> {
        let pattern_bytes = pattern.as_bytes();
        let m = pattern_bytes.len();
        let mut table = HashMap::new();

        for i in 0..m {
            table.insert(pattern_bytes[i], i);
        }

        table
    }

    /// Build good suffix table
    /// Time: O(m)
    pub fn good_suffix_table(pattern: &str) -> Vec<usize> {
        let pattern_bytes = pattern.as_bytes();
        let m = pattern_bytes.len();
        let mut shift = vec![0; m + 1];
        let mut border = vec![0; m + 1];

        let mut i = m;
        let mut j = m + 1;
        border[i] = j;

        while i > 0 {
            while j <= m && pattern_bytes[i - 1] != pattern_bytes[j - 1] {
                if shift[j] == 0 {
                    shift[j] = j - i;
                }
                j = border[j];
            }

            i -= 1;
            j -= 1;
            border[i] = j;
        }

        j = border[0];
        for i in 0..=m {
            if shift[i] == 0 {
                shift[i] = j;
            }
            if i == j {
                j = border[j];
            }
        }

        shift
    }

    /// Find all occurrences using Boyer-Moore
    /// Time: O(n) average
    pub fn search(text: &str, pattern: &str, visualize: bool) -> Vec<usize> {
        if pattern.is_empty() || text.is_empty() {
            return Vec::new();
        }

        let text_bytes = text.as_bytes();
        let pattern_bytes = pattern.as_bytes();
        let n = text_bytes.len();
        let m = pattern_bytes.len();

        if m > n {
            return Vec::new();
        }

        let bad_char = Self::bad_character_table(pattern);
        let good_suffix = Self::good_suffix_table(pattern);

        let mut matches = Vec::new();
        let mut s = 0;

        if visualize {
            println!("\nBoyer-Moore Algorithm Visualization:");
            println!("Text:    {}", text);
            println!("Pattern: {}\n", pattern);
        }

        while s <= n - m {
            let mut j = m - 1;

            if visualize {
                println!("Checking at position {}: '{}'", s, &text[s..s + m]);
            }

            while j > 0 && pattern_bytes[j] == text_bytes[s + j] {
                if j == 0 {
                    break;
                }
                j -= 1;
            }

            if j == 0 && pattern_bytes[j] == text_bytes[s + j] {
                matches.push(s);
                if visualize {
                    println!("✓ Match found at index {}", s);
                }
                s += good_suffix[0];
            } else {
                let bad_char_shift = if let Some(&pos) = bad_char.get(&text_bytes[s + j]) {
                    if j > pos {
                        j - pos
                    } else {
                        1
                    }
                } else {
                    j + 1
                };
                let good_suffix_shift = good_suffix[j + 1];
                let shift = std::cmp::max(bad_char_shift, good_suffix_shift);

                if visualize {
                    println!("  Mismatch at j={}, shifting by {}", j, shift);
                }

                s += shift;
            }
        }

        matches
    }
}

// ============================================================================
// 3. RABIN-KARP ALGORITHM
// ============================================================================

/// Rabin-Karp Rolling Hash Algorithm
/// Time: Average O(n + m), Worst O(n*m)
pub struct RabinKarp {
    base: i64,
    prime: i64,
}

impl RabinKarp {
    pub fn new() -> Self {
        RabinKarp {
            base: 256,
            prime: 101,
        }
    }

    /// Compute hash value
    fn hash(&self, s: &str, length: usize) -> i64 {
        let s_bytes = s.as_bytes();
        let mut h: i64 = 0;
        for i in 0..length {
            h = (h * self.base + s_bytes[i] as i64) % self.prime;
        }
        h
    }

    /// Find all occurrences using Rabin-Karp
    /// Time: O(n + m) average
    pub fn search(&self, text: &str, pattern: &str, visualize: bool) -> Vec<usize> {
        if pattern.is_empty() || text.is_empty() {
            return Vec::new();
        }

        let text_bytes = text.as_bytes();
        let n = text_bytes.len();
        let m = pattern.len();

        if m > n {
            return Vec::new();
        }

        let pattern_hash = self.hash(pattern, m);
        let mut text_hash = self.hash(text, m);

        let mut h: i64 = 1;
        for _ in 0..m - 1 {
            h = (h * self.base) % self.prime;
        }

        let mut matches = Vec::new();

        if visualize {
            println!("\nRabin-Karp Algorithm Visualization:");
            println!("Text:    {}", text);
            println!("Pattern: {}", pattern);
            println!("Pattern hash: {}\n", pattern_hash);
        }

        for i in 0..=n - m {
            if visualize {
                println!("Position {}: hash={}, substring='{}'", i, text_hash, &text[i..i + m]);
            }

            if pattern_hash == text_hash {
                if &text[i..i + m] == pattern {
                    matches.push(i);
                    if visualize {
                        println!("  ✓ Match found at index {}", i);
                    }
                } else if visualize {
                    println!("  ✗ Hash collision, not a real match");
                }
            }

            if i < n - m {
                text_hash = (self.base * (text_hash - text_bytes[i] as i64 * h) + text_bytes[i + m] as i64) % self.prime;

                if text_hash < 0 {
                    text_hash += self.prime;
                }
            }
        }

        matches
    }
}

// ============================================================================
// 4. AHO-CORASICK ALGORITHM (MULTIPLE PATTERN MATCHING)
// ============================================================================

#[derive(Default)]
struct TrieNode {
    children: HashMap<u8, Box<TrieNode>>,
    output: Vec<usize>,
    fail: Option<*mut TrieNode>,
}

/// Aho-Corasick Multiple Pattern Matching Algorithm
/// Time: O(n + k) where k = number of matches
pub struct AhoCorasick {
    root: Box<TrieNode>,
    patterns: Vec<String>,
}

impl AhoCorasick {
    pub fn new() -> Self {
        AhoCorasick {
            root: Box::new(TrieNode::default()),
            patterns: Vec::new(),
        }
    }

    /// Add pattern to trie
    /// Time: O(m)
    pub fn add_pattern(&mut self, pattern: &str) {
        let pattern_id = self.patterns.len();
        self.patterns.push(pattern.to_string());

        let mut node = &mut *self.root;
        for &byte in pattern.as_bytes() {
            node = node.children.entry(byte).or_insert_with(|| Box::new(TrieNode::default()));
        }

        node.output.push(pattern_id);
    }

    /// Build failure links using BFS
    /// Time: O(total pattern length)
    pub fn build_failure_links(&mut self) {
        let mut queue = VecDeque::new();

        // Set failure links for depth 1 nodes
        let root_ptr = &mut *self.root as *mut TrieNode;
        for child in self.root.children.values_mut() {
            child.fail = Some(root_ptr);
            queue.push_back(&mut **child as *mut TrieNode);
        }

        // BFS to set failure links
        while let Some(current_ptr) = queue.pop_front() {
            let current = unsafe { &mut *current_ptr };

            for (&byte, child) in current.children.iter_mut() {
                queue.push_back(&mut **child as *mut TrieNode);

                let mut fail_node = current.fail;
                while let Some(fail_ptr) = fail_node {
                    let fail = unsafe { &*fail_ptr };
                    if fail.children.contains_key(&byte) {
                        break;
                    }
                    fail_node = fail.fail;
                }

                if let Some(fail_ptr) = fail_node {
                    let fail = unsafe { &*fail_ptr };
                    if let Some(fail_child) = fail.children.get(&byte) {
                        child.fail = Some(&**fail_child as *const TrieNode as *mut TrieNode);
                        let fail_child_output = unsafe { &(**child.fail.unwrap()).output };
                        child.output.extend_from_slice(fail_child_output);
                    } else {
                        child.fail = Some(root_ptr);
                    }
                } else {
                    child.fail = Some(root_ptr);
                }
            }
        }
    }

    /// Find all occurrences of all patterns
    /// Time: O(n + k)
    pub fn search(&self, text: &str, visualize: bool) -> HashMap<usize, Vec<usize>> {
        if text.is_empty() {
            return HashMap::new();
        }

        let mut results = HashMap::new();
        let mut current = &*self.root as *const TrieNode;

        if visualize {
            println!("\nAho-Corasick Algorithm Visualization:");
            println!("Text: {}", text);
            println!("Patterns: {:?}\n", self.patterns);
        }

        for (i, &byte) in text.as_bytes().iter().enumerate() {
            loop {
                let current_ref = unsafe { &*current };
                if current_ref.children.contains_key(&byte) {
                    break;
                }
                if let Some(fail_ptr) = current_ref.fail {
                    current = fail_ptr;
                } else {
                    current = &*self.root as *const TrieNode;
                    break;
                }
            }

            let current_ref = unsafe { &*current };
            if let Some(child) = current_ref.children.get(&byte) {
                current = &**child as *const TrieNode;
            } else {
                continue;
            }

            let current_ref = unsafe { &*current };
            if !current_ref.output.is_empty() {
                for &pattern_id in &current_ref.output {
                    let pattern_len = self.patterns[pattern_id].len();
                    let start_idx = i - pattern_len + 1;

                    results.entry(pattern_id).or_insert_with(Vec::new).push(start_idx);

                    if visualize {
                        println!("✓ Found pattern '{}' at index {}", self.patterns[pattern_id], start_idx);
                    }
                }
            }
        }

        results
    }
}

// ============================================================================
// 5. Z-ALGORITHM
// ============================================================================

/// Z-Algorithm for Pattern Matching
/// Time: O(n + m), Space: O(n + m)
pub struct ZAlgorithm;

impl ZAlgorithm {
    /// Compute Z-array
    /// Time: O(n)
    pub fn compute_z_array(s: &str) -> Vec<usize> {
        let s_bytes = s.as_bytes();
        let n = s_bytes.len();
        let mut z = vec![0; n];
        z[0] = n;

        let mut l = 0;
        let mut r = 0;

        for i in 1..n {
            if i > r {
                l = i;
                r = i;
                while r < n && s_bytes[r - l] == s_bytes[r] {
                    r += 1;
                }
                z[i] = r - l;
                r -= 1;
            } else {
                let k = i - l;
                if z[k] < r - i + 1 {
                    z[i] = z[k];
                } else {
                    l = i;
                    while r < n && s_bytes[r - l] == s_bytes[r] {
                        r += 1;
                    }
                    z[i] = r - l;
                    r -= 1;
                }
            }
        }

        z
    }

    /// Find all occurrences using Z-algorithm
    /// Time: O(n + m)
    pub fn search(text: &str, pattern: &str, visualize: bool) -> Vec<usize> {
        if pattern.is_empty() || text.is_empty() {
            return Vec::new();
        }

        let n = text.len();
        let m = pattern.len();

        if m > n {
            return Vec::new();
        }

        let concat = format!("{}${}", pattern, text);
        let z = Self::compute_z_array(&concat);

        let mut matches = Vec::new();

        if visualize {
            println!("\nZ-Algorithm Visualization:");
            println!("Text:    {}", text);
            println!("Pattern: {}", pattern);
            println!("Concatenation: {}", concat);
            println!("Z-array: {:?}\n", z);
        }

        for i in m + 1..concat.len() {
            if z[i] == m {
                let match_pos = i - m - 1;
                matches.push(match_pos);
                if visualize {
                    println!("✓ Match found at index {} (Z[{}] = {})", match_pos, i, m);
                }
            }
        }

        matches
    }
}

// ============================================================================
// 6. MANACHER'S ALGORITHM (PALINDROME DETECTION)
// ============================================================================

#[derive(Debug, Clone)]
pub struct Palindrome {
    pub start: usize,
    pub end: usize,
    pub text: String,
}

/// Manacher's Algorithm for Finding Palindromes
/// Time: O(n), Space: O(n)
pub struct Manacher;

impl Manacher {
    /// Preprocess string to handle even/odd palindromes uniformly
    pub fn preprocess(s: &str) -> String {
        if s.is_empty() {
            return "#".to_string();
        }

        let mut result = String::from("#");
        for c in s.chars() {
            result.push(c);
            result.push('#');
        }
        result
    }

    /// Find all palindromes
    /// Time: O(n)
    pub fn find_all_palindromes(s: &str, visualize: bool) -> Vec<Palindrome> {
        if s.is_empty() {
            return Vec::new();
        }

        let t = Self::preprocess(s);
        let t_bytes = t.as_bytes();
        let n = t_bytes.len();
        let mut p = vec![0; n];

        let mut center = 0;
        let mut right = 0;

        if visualize {
            println!("\nManacher's Algorithm Visualization:");
            println!("Original: {}", s);
            println!("Transformed: {}\n", t);
        }

        for i in 0..n {
            let mirror = 2 * center - i;

            if i < right && mirror < n {
                p[i] = std::cmp::min(right - i, p[mirror]);
            }

            while i + p[i] + 1 < n && i >= p[i] + 1 && t_bytes[i + p[i] + 1] == t_bytes[i - p[i] - 1] {
                p[i] += 1;
            }

            if i + p[i] > right {
                center = i;
                right = i + p[i];
            }
        }

        let mut palindromes = Vec::new();
        for i in 0..n {
            if p[i] > 0 {
                let start = (i - p[i]) / 2;
                let end = (i + p[i]) / 2;
                if start < end {
                    palindromes.push(Palindrome {
                        start,
                        end,
                        text: s[start..end].to_string(),
                    });
                }
            }
        }

        if visualize {
            println!("Palindromes found:");
            for pal in &palindromes {
                println!("  [{}:{}] = '{}'", pal.start, pal.end, pal.text);
            }
        }

        palindromes
    }

    /// Find longest palindromic substring
    /// Time: O(n)
    pub fn longest_palindrome(s: &str) -> String {
        if s.is_empty() {
            return String::new();
        }

        let t = Self::preprocess(s);
        let t_bytes = t.as_bytes();
        let n = t_bytes.len();
        let mut p = vec![0; n];

        let mut center = 0;
        let mut right = 0;

        for i in 0..n {
            let mirror = 2 * center - i;

            if i < right && mirror < n {
                p[i] = std::cmp::min(right - i, p[mirror]);
            }

            while i + p[i] + 1 < n && i >= p[i] + 1 && t_bytes[i + p[i] + 1] == t_bytes[i - p[i] - 1] {
                p[i] += 1;
            }

            if i + p[i] > right {
                center = i;
                right = i + p[i];
            }
        }

        let mut max_len = 0;
        let mut center_index = 0;
        for i in 0..n {
            if p[i] > max_len {
                max_len = p[i];
                center_index = i;
            }
        }

        let start = (center_index - max_len) / 2;
        s[start..start + max_len].to_string()
    }
}

// ============================================================================
// PERFORMANCE BENCHMARKING
// ============================================================================

pub fn benchmark_single_pattern(text: &str, pattern: &str, iterations: usize) {
    println!("\n{}", "=".repeat(70));
    println!("PERFORMANCE BENCHMARK");
    println!("{}", "=".repeat(70));
    println!("Text length: {}", text.len());
    println!("Pattern length: {}", pattern.len());
    println!("Iterations: {}\n", iterations);

    let algorithms: Vec<(&str, Box<dyn Fn()>)> = vec![
        ("KMP", Box::new(|| { KMP::search(text, pattern, false); })),
        ("Boyer-Moore", Box::new(|| { BoyerMoore::search(text, pattern, false); })),
        ("Rabin-Karp", Box::new(|| { RabinKarp::new().search(text, pattern, false); })),
        ("Z-Algorithm", Box::new(|| { ZAlgorithm::search(text, pattern, false); })),
    ];

    let mut results = Vec::new();

    for (name, func) in algorithms {
        let start = Instant::now();
        for _ in 0..iterations {
            func();
        }
        let elapsed = start.elapsed();

        let avg_time = elapsed.as_secs_f64() * 1000.0 / iterations as f64;
        results.push((name, avg_time));

        println!("{:<15} | {:>8.4} ms", name, avg_time);
    }

    let best = results.iter().min_by(|a, b| a.1.partial_cmp(&b.1).unwrap()).unwrap();
    println!("\n✓ Fastest: {} ({:.4} ms)", best.0, best.1);
}

// ============================================================================
// EXAMPLE USAGE AND TESTING
// ============================================================================

fn main() {
    println!("{}", "=".repeat(70));
    println!("STRING PATTERN MATCHING ALGORITHMS");
    println!("{}", "=".repeat(70));

    let text = "ABABCABABABCABAB";
    let pattern = "ABAB";

    println!("\nTest Text: {}", text);
    println!("Pattern: {}\n", pattern);

    // 1. KMP Algorithm
    println!("\n{}", "=".repeat(70));
    println!("1. KMP ALGORITHM");
    println!("{}", "=".repeat(70));
    let matches = KMP::search(text, pattern, true);
    println!("\nMatches found: {:?}", matches);

    // 2. Boyer-Moore Algorithm
    println!("\n{}", "=".repeat(70));
    println!("2. BOYER-MOORE ALGORITHM");
    println!("{}", "=".repeat(70));
    let matches = BoyerMoore::search(text, pattern, true);
    println!("\nMatches found: {:?}", matches);

    // 3. Rabin-Karp Algorithm
    println!("\n{}", "=".repeat(70));
    println!("3. RABIN-KARP ALGORITHM");
    println!("{}", "=".repeat(70));
    let rk = RabinKarp::new();
    let matches = rk.search(text, pattern, true);
    println!("\nMatches found: {:?}", matches);

    // 4. Aho-Corasick Algorithm
    println!("\n{}", "=".repeat(70));
    println!("4. AHO-CORASICK ALGORITHM (Multiple Patterns)");
    println!("{}", "=".repeat(70));
    let mut ac = AhoCorasick::new();
    let patterns = vec!["ABAB", "ABC", "CAB"];
    for pattern in patterns {
        ac.add_pattern(pattern);
    }
    ac.build_failure_links();
    let results = ac.search(text, true);
    println!("\nAll matches: {:?}", results);

    // 5. Z-Algorithm
    println!("\n{}", "=".repeat(70));
    println!("5. Z-ALGORITHM");
    println!("{}", "=".repeat(70));
    let matches = ZAlgorithm::search(text, pattern, true);
    println!("\nMatches found: {:?}", matches);

    // 6. Manacher's Algorithm
    println!("\n{}", "=".repeat(70));
    println!("6. MANACHER'S ALGORITHM");
    println!("{}", "=".repeat(70));
    let palindrome_text = "babad";
    let longest = Manacher::longest_palindrome(palindrome_text);
    println!("Text: {}", palindrome_text);
    println!("Longest palindrome: '{}'", longest);

    let _palindromes = Manacher::find_all_palindromes(palindrome_text, true);

    // Performance Benchmarking
    println!("\n{}", "=".repeat(70));
    println!("PERFORMANCE BENCHMARKING");
    println!("{}", "=".repeat(70));

    let benchmark_text = "ABC".repeat(1000);
    let benchmark_pattern = "ABCABC";

    benchmark_single_pattern(&benchmark_text, benchmark_pattern, 100);

    println!("\n{}", "=".repeat(70));
}
