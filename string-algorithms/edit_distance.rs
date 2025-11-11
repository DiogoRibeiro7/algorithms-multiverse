/**
 * Edit Distance Algorithms - Rust Implementation
 * ===============================================
 *
 * String similarity and edit distance metrics.
 *
 * Compile: rustc -O edit_distance.rs
 * Run: ./edit_distance
 */

use std::cmp;
use std::collections::HashMap;

// ============================================================================
// Edit Distance Algorithms
// ============================================================================

/// Hamming Distance - Number of positions at which symbols differ
/// Time: O(n), Space: O(1)
pub fn hamming_distance(str1: &str, str2: &str) -> Result<usize, &'static str> {
    if str1.len() != str2.len() {
        return Err("Hamming distance requires equal length strings");
    }

    let distance = str1
        .chars()
        .zip(str2.chars())
        .filter(|(c1, c2)| c1 != c2)
        .count();

    Ok(distance)
}

/// Levenshtein Distance - Minimum edits (insert, delete, substitute)
/// Time: O(nm), Space: O(nm)
pub fn levenshtein_distance(str1: &str, str2: &str, visualize: bool) -> usize {
    let m = str1.len();
    let n = str2.len();

    // Create DP table
    let mut dp = vec![vec![0; n + 1]; m + 1];

    // Initialize base cases
    for i in 0..=m {
        dp[i][0] = i;
    }
    for j in 0..=n {
        dp[0][j] = j;
    }

    // Convert to char vectors for indexing
    let chars1: Vec<char> = str1.chars().collect();
    let chars2: Vec<char> = str2.chars().collect();

    // Fill DP table
    for i in 1..=m {
        for j in 1..=n {
            let cost = if chars1[i - 1] == chars2[j - 1] { 0 } else { 1 };

            dp[i][j] = cmp::min(
                cmp::min(
                    dp[i - 1][j] + 1,      // deletion
                    dp[i][j - 1] + 1,      // insertion
                ),
                dp[i - 1][j - 1] + cost,   // substitution
            );
        }
    }

    if visualize {
        visualize_dp_table(str1, str2, &dp);
    }

    dp[m][n]
}

/// Space-optimized Levenshtein distance
/// Time: O(nm), Space: O(min(n,m))
pub fn levenshtein_optimized(str1: &str, str2: &str) -> usize {
    // Ensure str1 is shorter
    let (str1, str2) = if str1.len() > str2.len() {
        (str2, str1)
    } else {
        (str1, str2)
    };

    let m = str1.len();
    let n = str2.len();

    let chars1: Vec<char> = str1.chars().collect();
    let chars2: Vec<char> = str2.chars().collect();

    // Use two rows
    let mut prev_row: Vec<usize> = (0..=n).collect();
    let mut curr_row = vec![0; n + 1];

    for i in 1..=m {
        curr_row[0] = i;

        for j in 1..=n {
            let cost = if chars1[i - 1] == chars2[j - 1] { 0 } else { 1 };

            curr_row[j] = cmp::min(
                cmp::min(
                    prev_row[j] + 1,        // deletion
                    curr_row[j - 1] + 1,    // insertion
                ),
                prev_row[j - 1] + cost,     // substitution
            );
        }

        std::mem::swap(&mut prev_row, &mut curr_row);
    }

    prev_row[n]
}

/// Damerau-Levenshtein Distance - Adds transposition operation
/// Time: O(nm), Space: O(nm)
pub fn damerau_levenshtein_distance(str1: &str, str2: &str) -> usize {
    let m = str1.len();
    let n = str2.len();
    let max_dist = m + n;

    let chars1: Vec<char> = str1.chars().collect();
    let chars2: Vec<char> = str2.chars().collect();

    // Use HashMap for sparse matrix
    let mut h: HashMap<(isize, isize), usize> = HashMap::new();

    // Initialize
    h.insert((-1, -1), max_dist);

    for i in 0..=(m as isize) {
        h.insert((i, -1), max_dist);
        h.insert((i, 0), i as usize);
    }

    for j in 0..=(n as isize) {
        h.insert((-1, j), max_dist);
        h.insert((0, j), j as usize);
    }

    for i in 1..=m {
        let mut db = 0;

        for j in 1..=n {
            let k = db;
            let l = if chars1[i - 1] == chars2[j - 1] {
                db = j;
                0
            } else {
                1
            };

            let i_i = i as isize;
            let j_i = j as isize;
            let k_i = k as isize;
            let db_i = db as isize;

            h.insert(
                (i_i, j_i),
                cmp::min(
                    cmp::min(
                        cmp::min(
                            h[&(i_i - 1, j_i)] + 1,          // deletion
                            h[&(i_i, j_i - 1)] + 1,          // insertion
                        ),
                        h[&(i_i - 1, j_i - 1)] + l,          // substitution
                    ),
                    h[&(k_i - 1, db_i - 1)] + (i - k - 1) + 1 + (j - db - 1), // transposition
                ),
            );
        }
    }

    h[&(m as isize, n as isize)]
}

/// Longest Common Subsequence length
/// Time: O(nm), Space: O(nm)
pub fn lcs_length(str1: &str, str2: &str) -> usize {
    let m = str1.len();
    let n = str2.len();

    let chars1: Vec<char> = str1.chars().collect();
    let chars2: Vec<char> = str2.chars().collect();

    let mut dp = vec![vec![0; n + 1]; m + 1];

    for i in 1..=m {
        for j in 1..=n {
            if chars1[i - 1] == chars2[j - 1] {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = cmp::max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    dp[m][n]
}

/// Return the actual Longest Common Subsequence
pub fn lcs_string(str1: &str, str2: &str) -> String {
    let m = str1.len();
    let n = str2.len();

    let chars1: Vec<char> = str1.chars().collect();
    let chars2: Vec<char> = str2.chars().collect();

    let mut dp = vec![vec![0; n + 1]; m + 1];

    for i in 1..=m {
        for j in 1..=n {
            if chars1[i - 1] == chars2[j - 1] {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = cmp::max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    // Backtrack to find LCS
    let mut lcs = Vec::new();
    let mut i = m;
    let mut j = n;

    while i > 0 && j > 0 {
        if chars1[i - 1] == chars2[j - 1] {
            lcs.push(chars1[i - 1]);
            i -= 1;
            j -= 1;
        } else if dp[i - 1][j] > dp[i][j - 1] {
            i -= 1;
        } else {
            j -= 1;
        }
    }

    lcs.reverse();
    lcs.iter().collect()
}

// ============================================================================
// Similarity Metrics
// ============================================================================

/// Normalized Levenshtein distance (0 to 1)
/// 1.0 = identical, 0.0 = completely different
pub fn normalized_levenshtein(str1: &str, str2: &str) -> f64 {
    if str1.is_empty() && str2.is_empty() {
        return 1.0;
    }

    let distance = levenshtein_distance(str1, str2, false);
    let max_len = cmp::max(str1.len(), str2.len());

    1.0 - (distance as f64 / max_len as f64)
}

/// Similarity ratio based on LCS
pub fn similarity_ratio(str1: &str, str2: &str) -> f64 {
    if str1.is_empty() && str2.is_empty() {
        return 1.0;
    }

    let lcs_len = lcs_length(str1, str2);
    let total_len = str1.len() + str2.len();

    if total_len == 0 {
        return 1.0;
    }

    2.0 * lcs_len as f64 / total_len as f64
}

/// Jaro distance - Good for short strings like names
/// Returns: 0.0 to 1.0 (1.0 = identical)
pub fn jaro_distance(str1: &str, str2: &str) -> f64 {
    if str1 == str2 {
        return 1.0;
    }

    let len1 = str1.len();
    let len2 = str2.len();

    if len1 == 0 || len2 == 0 {
        return 0.0;
    }

    let chars1: Vec<char> = str1.chars().collect();
    let chars2: Vec<char> = str2.chars().collect();

    // Maximum allowed distance
    let mut match_distance = cmp::max(len1, len2) / 2;
    if match_distance > 0 {
        match_distance -= 1;
    }
    if match_distance < 1 {
        match_distance = 1;
    }

    let mut str1_matches = vec![false; len1];
    let mut str2_matches = vec![false; len2];

    let mut matches = 0;

    // Find matches
    for i in 0..len1 {
        let start = if i >= match_distance { i - match_distance } else { 0 };
        let end = cmp::min(i + match_distance + 1, len2);

        for j in start..end {
            if str2_matches[j] || chars1[i] != chars2[j] {
                continue;
            }
            str1_matches[i] = true;
            str2_matches[j] = true;
            matches += 1;
            break;
        }
    }

    if matches == 0 {
        return 0.0;
    }

    // Find transpositions
    let mut transpositions = 0;
    let mut k = 0;

    for i in 0..len1 {
        if !str1_matches[i] {
            continue;
        }
        while !str2_matches[k] {
            k += 1;
        }
        if chars1[i] != chars2[k] {
            transpositions += 1;
        }
        k += 1;
    }

    (matches as f64 / len1 as f64
        + matches as f64 / len2 as f64
        + (matches as f64 - transpositions as f64 / 2.0) / matches as f64)
        / 3.0
}

/// Jaro-Winkler distance - Gives more weight to common prefix
pub fn jaro_winkler_distance(str1: &str, str2: &str, prefix_scale: f64) -> f64 {
    let jaro = jaro_distance(str1, str2);

    // Find common prefix length (max 4)
    let mut prefix = 0;
    let min_len = cmp::min(str1.len(), str2.len());
    let chars1: Vec<char> = str1.chars().collect();
    let chars2: Vec<char> = str2.chars().collect();

    for i in 0..cmp::min(min_len, 4) {
        if chars1[i] == chars2[i] {
            prefix += 1;
        } else {
            break;
        }
    }

    jaro + prefix as f64 * prefix_scale * (1.0 - jaro)
}

// ============================================================================
// Helper Functions
// ============================================================================

fn visualize_dp_table(str1: &str, str2: &str, dp: &[Vec<usize>]) {
    println!("\nDP Table:");
    println!("{}", "=".repeat(70));

    // Header
    print!("       ");
    for c in str2.chars() {
        print!("{:>4}", c);
    }
    println!();

    // Rows
    let chars1: Vec<char> = str1.chars().collect();
    for (i, row) in dp.iter().enumerate() {
        if i == 0 {
            print!("  ");
        } else {
            print!("{:>2}", chars1[i - 1]);
        }

        for val in row {
            print!("{:>4}", val);
        }
        println!();
    }
}

// ============================================================================
// Main Function - Examples
// ============================================================================

fn main() {
    println!("{}", "=".repeat(70));
    println!("EDIT DISTANCE ALGORITHMS - RUST");
    println!("{}", "=".repeat(70));

    // Example 1: Hamming distance
    println!("\n{}", "=".repeat(70));
    println!("EXAMPLE 1: Hamming Distance");
    println!("{}", "=".repeat(70));

    let str1 = "karolin";
    let str2 = "kathrin";

    match hamming_distance(str1, str2) {
        Ok(dist) => {
            println!("String 1: '{}'", str1);
            println!("String 2: '{}'", str2);
            println!("Hamming distance: {}", dist);
        }
        Err(e) => println!("Error: {}", e),
    }

    // Example 2: Levenshtein distance
    println!("\n{}", "=".repeat(70));
    println!("EXAMPLE 2: Levenshtein Distance");
    println!("{}", "=".repeat(70));

    let str3 = "kitten";
    let str4 = "sitting";
    let dist2 = levenshtein_distance(str3, str4, true);

    println!("\nString 1: '{}'", str3);
    println!("String 2: '{}'", str4);
    println!("Levenshtein distance: {}", dist2);

    // Example 3: Damerau-Levenshtein
    println!("\n{}", "=".repeat(70));
    println!("EXAMPLE 3: Damerau-Levenshtein Distance");
    println!("{}", "=".repeat(70));

    let test_cases = vec![
        ("kitten", "sitting"),
        ("teh", "the"),
        ("abcd", "acbd"),
    ];

    for (s1, s2) in test_cases {
        let lev_dist = levenshtein_distance(s1, s2, false);
        let dam_lev_dist = damerau_levenshtein_distance(s1, s2);

        println!("\nString 1: '{}'", s1);
        println!("String 2: '{}'", s2);
        println!("  Levenshtein:         {}", lev_dist);
        println!("  Damerau-Levenshtein: {}", dam_lev_dist);
    }

    // Example 4: LCS
    println!("\n{}", "=".repeat(70));
    println!("EXAMPLE 4: Longest Common Subsequence");
    println!("{}", "=".repeat(70));

    let str5 = "ABCDGH";
    let str6 = "AEDFHR";
    let lcs = lcs_string(str5, str6);

    println!("String 1: '{}'", str5);
    println!("String 2: '{}'", str6);
    println!("LCS: '{}' (length: {})", lcs, lcs.len());

    // Example 5: Similarity metrics
    println!("\n{}", "=".repeat(70));
    println!("EXAMPLE 5: Similarity Metrics");
    println!("{}", "=".repeat(70));

    let test_pairs = vec![
        ("kitten", "sitting"),
        ("saturday", "sunday"),
        ("martha", "marhta"),
        ("dixon", "dicksonx"),
    ];

    for (s1, s2) in test_pairs {
        let norm_lev = normalized_levenshtein(s1, s2);
        let sim_ratio = similarity_ratio(s1, s2);
        let jaro = jaro_distance(s1, s2);
        let jaro_winkler = jaro_winkler_distance(s1, s2, 0.1);

        println!("\n'{}' vs '{}':", s1, s2);
        println!("  Normalized Levenshtein: {:.4}", norm_lev);
        println!("  Similarity Ratio:       {:.4}", sim_ratio);
        println!("  Jaro:                   {:.4}", jaro);
        println!("  Jaro-Winkler:           {:.4}", jaro_winkler);
    }

    println!("\n{}", "=".repeat(70));
}
