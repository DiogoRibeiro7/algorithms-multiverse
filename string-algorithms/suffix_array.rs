/*
 * Suffix Array and LCP Array Construction in Rust
 * ===============================================
 *
 * Algorithms implemented:
 * 1. Prefix doubling O(n log² n) for suffix array construction
 * 2. Kasai's algorithm O(n) for LCP array computation
 *
 * Applications:
 * - Pattern matching in O(m log n) time
 * - Finding longest repeated substring
 * - Counting distinct substrings
 * - Longest common substring between two strings
 *
 * Compilation: rustc -O suffix_array.rs
 * Usage: ./suffix_array
 */

use std::time::Instant;

/// Suffix structure for sorting
#[derive(Debug, Clone, Copy)]
struct Suffix {
    index: usize,
    rank: [i32; 2],
}

/// Suffix Array with LCP array
pub struct SuffixArray {
    text: String,
    sa: Vec<usize>,
    lcp: Vec<usize>,
}

impl SuffixArray {
    /// Create a new suffix array from text
    pub fn new(text: &str) -> Self {
        let mut sa = SuffixArray {
            text: text.to_string(),
            sa: Vec::new(),
            lcp: Vec::new(),
        };
        sa.build();
        sa.build_lcp();
        sa
    }

    /// Build suffix array using prefix doubling algorithm
    /// Time: O(n log² n)
    /// Space: O(n)
    fn build(&mut self) {
        let n = self.text.len();
        if n == 0 {
            return;
        }

        let text_bytes = self.text.as_bytes();

        // Create suffix structures
        let mut suffixes: Vec<Suffix> = (0..n)
            .map(|i| Suffix {
                index: i,
                rank: [
                    text_bytes[i] as i32,
                    if i + 1 < n { text_bytes[i + 1] as i32 } else { -1 },
                ],
            })
            .collect();

        // Sort by first two characters
        suffixes.sort_by(|a, b| {
            if a.rank[0] != b.rank[0] {
                a.rank[0].cmp(&b.rank[0])
            } else {
                a.rank[1].cmp(&b.rank[1])
            }
        });

        // Build initial rank array
        let mut rank = vec![0; n];
        for (i, suffix) in suffixes.iter().enumerate() {
            rank[suffix.index] = i as i32;
        }

        // Prefix doubling
        let mut k = 4;
        while k < 2 * n {
            // Update ranks for sorting
            for i in 0..n {
                let curr = suffixes[i].index;
                suffixes[i].rank[0] = rank[curr];
                suffixes[i].rank[1] = if curr + k / 2 < n {
                    rank[curr + k / 2]
                } else {
                    -1
                };
            }

            // Sort suffixes
            suffixes.sort_by(|a, b| {
                if a.rank[0] != b.rank[0] {
                    a.rank[0].cmp(&b.rank[0])
                } else {
                    a.rank[1].cmp(&b.rank[1])
                }
            });

            // Update ranks
            let mut temp_rank = vec![0; n];
            temp_rank[suffixes[0].index] = 0;

            for i in 1..n {
                let prev = suffixes[i - 1];
                let curr = suffixes[i];

                // Same rank if both pairs are equal
                temp_rank[curr.index] = if curr.rank[0] == prev.rank[0]
                    && curr.rank[1] == prev.rank[1]
                {
                    temp_rank[prev.index]
                } else {
                    temp_rank[prev.index] + 1
                };
            }

            rank = temp_rank;
            k *= 2;
        }

        // Build suffix array from sorted suffixes
        self.sa = suffixes.iter().map(|s| s.index).collect();
    }

    /// Build LCP array using Kasai's algorithm
    /// Time: O(n)
    /// Space: O(n)
    ///
    /// LCP[i] = length of longest common prefix between
    ///          suffix[SA[i]] and suffix[SA[i-1]]
    fn build_lcp(&mut self) {
        let n = self.text.len();
        self.lcp = vec![0; n];

        if n == 0 {
            return;
        }

        let text_bytes = self.text.as_bytes();

        // Compute inverse suffix array (rank)
        let mut rank = vec![0; n];
        for (i, &sa_i) in self.sa.iter().enumerate() {
            rank[sa_i] = i;
        }

        let mut h = 0; // Height of LCP

        for i in 0..n {
            if rank[i] > 0 {
                let j = self.sa[rank[i] - 1];

                // Compute LCP
                while i + h < n && j + h < n && text_bytes[i + h] == text_bytes[j + h] {
                    h += 1;
                }

                self.lcp[rank[i]] = h;

                // Decrease h for next iteration
                if h > 0 {
                    h -= 1;
                }
            }
        }
    }

    /// Pattern search using binary search on suffix array
    /// Time: O(m log n)
    pub fn pattern_search(&self, pattern: &str) -> Vec<usize> {
        let n = self.text.len();
        let m = pattern.len();
        let mut matches = Vec::new();

        if m == 0 || n == 0 {
            return matches;
        }

        // Binary search for lower bound
        let lower = self.sa.partition_point(|&idx| {
            let suffix = &self.text[idx..];
            suffix < pattern
        });

        // Binary search for upper bound
        let upper = self.sa.partition_point(|&idx| {
            let suffix = &self.text[idx..];
            if suffix.len() < m {
                suffix <= &pattern[..suffix.len()]
            } else {
                &suffix[..m] <= pattern
            }
        });

        // Collect all matches
        for i in lower..upper {
            if self.text[self.sa[i]..].starts_with(pattern) {
                matches.push(self.sa[i]);
            }
        }

        matches
    }

    /// Find longest repeated substring
    /// Time: O(n)
    pub fn longest_repeated_substring(&self) -> &str {
        if self.lcp.is_empty() {
            return "";
        }

        let mut max_lcp = 0;
        let mut max_idx = 0;

        // Find maximum LCP value
        for (i, &lcp_val) in self.lcp.iter().enumerate().skip(1) {
            if lcp_val > max_lcp {
                max_lcp = lcp_val;
                max_idx = i;
            }
        }

        if max_lcp == 0 {
            return "";
        }

        &self.text[self.sa[max_idx]..self.sa[max_idx] + max_lcp]
    }

    /// Count distinct substrings
    /// Time: O(n)
    /// Formula: n*(n+1)/2 - sum(LCP)
    pub fn count_distinct_substrings(&self) -> usize {
        let n = self.text.len();
        let total = n * (n + 1) / 2;
        let duplicates: usize = self.lcp.iter().sum();
        total - duplicates
    }

    /// Visualize suffix array and LCP array
    pub fn visualize(&self) {
        println!("\nSuffix Array Visualization:");
        println!("Text: '{}'", self.text);
        println!("Length: {}\n", self.text.len());

        println!("{:<4} | {:<6} | {:<6} | Suffix", "i", "SA[i]", "LCP[i]");
        println!("{}", "-".repeat(70));

        for (i, &sa_i) in self.sa.iter().enumerate() {
            let suffix = &self.text[sa_i..];
            let suffix_display = if suffix.len() > 40 {
                format!("{}...", &suffix[..37])
            } else {
                suffix.to_string()
            };
            println!("{:<4} | {:<6} | {:<6} | {}", i, sa_i, self.lcp[i], suffix_display);
        }
        println!();
    }
}

/// Find longest common substring between two strings
/// Time: O(n + m)
pub fn longest_common_substring(text1: &str, text2: &str) -> String {
    // Concatenate with separator
    let separator = "#";
    let combined = format!("{}{}{}", text1, separator, text2);
    let len1 = text1.len();

    // Build suffix array
    let sa = SuffixArray::new(&combined);

    // Find max LCP where adjacent suffixes are from different strings
    let mut max_lcp = 0;
    let mut max_pos = 0;

    for i in 1..sa.sa.len() {
        let pos1 = sa.sa[i - 1];
        let pos2 = sa.sa[i];

        // One before separator, one after
        if (pos1 < len1) != (pos2 < len1) {
            if sa.lcp[i] > max_lcp {
                max_lcp = sa.lcp[i];
                max_pos = sa.sa[i];
            }
        }
    }

    if max_lcp == 0 {
        return String::new();
    }

    combined[max_pos..max_pos + max_lcp].to_string()
}

/// Benchmark suffix array construction
fn benchmark_construction(text: &str) -> std::time::Duration {
    let start = Instant::now();
    SuffixArray::new(text);
    start.elapsed()
}

// =========================================================================
// EXAMPLES AND TESTING
// =========================================================================

fn example_basic_construction() {
    println!("{}", "=".repeat(70));
    println!("EXAMPLE 1: Basic Suffix Array Construction");
    println!("{}", "=".repeat(70));

    let text = "banana";
    let sa = SuffixArray::new(text);
    sa.visualize();
}

fn example_pattern_search() {
    println!("{}", "=".repeat(70));
    println!("EXAMPLE 2: Pattern Searching");
    println!("{}", "=".repeat(70));

    let text = "the quick brown fox jumps over the lazy dog";
    let pattern = "the";

    let sa = SuffixArray::new(text);
    let matches = sa.pattern_search(pattern);

    println!("Text: '{}'", text);
    println!("Pattern: '{}'", pattern);
    println!("Matches at positions: {:?}\n", matches);

    for &pos in &matches {
        println!(
            "  Position {}: '{}'",
            pos,
            &text[pos..pos + pattern.len()]
        );
    }
    println!();
}

fn example_longest_repeated_substring() {
    println!("{}", "=".repeat(70));
    println!("EXAMPLE 3: Longest Repeated Substring");
    println!("{}", "=".repeat(70));

    let text = "abracadabra";
    let sa = SuffixArray::new(text);
    let lrs = sa.longest_repeated_substring();

    println!("Text: '{}'", text);
    println!("Longest repeated substring: '{}'\n", lrs);
}

fn example_count_distinct() {
    println!("{}", "=".repeat(70));
    println!("EXAMPLE 4: Count Distinct Substrings");
    println!("{}", "=".repeat(70));

    let text = "abab";
    let sa = SuffixArray::new(text);
    let count = sa.count_distinct_substrings();

    println!("Text: '{}'", text);
    println!("Number of distinct substrings: {}\n", count);
}

fn example_longest_common_substring() {
    println!("{}", "=".repeat(70));
    println!("EXAMPLE 5: Longest Common Substring");
    println!("{}", "=".repeat(70));

    let text1 = "algorithms";
    let text2 = "altruistic";
    let lcs = longest_common_substring(text1, text2);

    println!("Text 1: '{}'", text1);
    println!("Text 2: '{}'", text2);
    println!("Longest common substring: '{}'\n", lcs);
}

fn example_benchmark() {
    println!("{}", "=".repeat(70));
    println!("EXAMPLE 6: Performance Benchmarking");
    println!("{}", "=".repeat(70));

    // Small text
    let small_text = "banana".repeat(10);
    let small_time = benchmark_construction(&small_text);
    println!(
        "Small text (length {}): {:?}",
        small_text.len(),
        small_time
    );

    // Medium text
    let medium_text = "abracadabra".repeat(100);
    let medium_time = benchmark_construction(&medium_text);
    println!(
        "Medium text (length {}): {:?}\n",
        medium_text.len(),
        medium_time
    );
}

fn main() {
    println!("{}", "=".repeat(70));
    println!("SUFFIX ARRAY AND LCP ARRAY IN RUST");
    println!("{}", "=".repeat(70));
    println!();

    example_basic_construction();
    example_pattern_search();
    example_longest_repeated_substring();
    example_count_distinct();
    example_longest_common_substring();
    example_benchmark();

    println!("{}", "=".repeat(70));
    println!("All examples completed successfully!");
    println!("{}", "=".repeat(70));
}
