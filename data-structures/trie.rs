/**
 * Comprehensive Trie Data Structure Implementations in Rust
 *
 * This module implements multiple trie variants and applications:
 * 1. Standard Trie
 * 2. Compressed Trie (Patricia Tree)
 * 3. Suffix Trie
 * 4. Applications: Spell checker, Auto-complete, Dictionary
 *
 * Time Complexity:
 * - Insert: O(m) where m is key length
 * - Search: O(m)
 * - Delete: O(m)
 * - Prefix Search: O(p + n) where p is prefix length, n is results
 * - Space: O(ALPHABET_SIZE * N * M) where N is number of keys
 *
 * Advantages over Hash Tables:
 * ✓ Prefix-based operations
 * ✓ Ordered traversal
 * ✓ No hash collisions
 * ✓ Memory efficient for common prefixes
 *
 * Use Cases:
 * - Auto-complete systems
 * - Spell checkers
 * - IP routing (longest prefix match)
 * - Dictionary implementations
 * - DNA sequence analysis
 * - Text prediction
 */

use std::collections::{HashMap, HashSet, VecDeque, BTreeMap};

// ============================================================================
// STANDARD TRIE
// ============================================================================

/// Node in a standard trie
#[derive(Default)]
struct TrieNode {
    children: HashMap<char, Box<TrieNode>>,
    is_end_of_word: bool,
    frequency: i32, // For ranking suggestions
}

impl TrieNode {
    fn new() -> Self {
        TrieNode {
            children: HashMap::new(),
            is_end_of_word: false,
            frequency: 0,
        }
    }
}

/// Standard Trie implementation
///
/// Features:
/// - Insert, search, delete operations
/// - Prefix search
/// - Auto-completion
/// - Word frequency tracking
pub struct Trie {
    root: Box<TrieNode>,
    word_count: usize,
}

impl Trie {
    /// Create a new trie
    pub fn new() -> Self {
        Trie {
            root: Box::new(TrieNode::new()),
            word_count: 0,
        }
    }

    /// Insert a word into the trie. O(m)
    pub fn insert(&mut self, word: &str, frequency: i32) {
        let mut node = &mut self.root;

        for ch in word.chars() {
            node = node.children.entry(ch).or_insert_with(|| Box::new(TrieNode::new()));
        }

        if !node.is_end_of_word {
            self.word_count += 1;
        }

        node.is_end_of_word = true;
        node.frequency = frequency;
    }

    /// Search for exact word. O(m)
    pub fn search(&self, word: &str) -> bool {
        if let Some(node) = self.find_node(word) {
            node.is_end_of_word
        } else {
            false
        }
    }

    /// Check if any word starts with prefix. O(p)
    pub fn starts_with(&self, prefix: &str) -> bool {
        self.find_node(prefix).is_some()
    }

    /// Helper to find node for given prefix
    fn find_node(&self, prefix: &str) -> Option<&TrieNode> {
        let mut node = &*self.root;

        for ch in prefix.chars() {
            match node.children.get(&ch) {
                Some(child) => node = child,
                None => return None,
            }
        }

        Some(node)
    }

    /// Delete a word from trie. O(m)
    pub fn delete(&mut self, word: &str) -> bool {
        self.delete_helper(&mut self.root, word, 0)
    }

    fn delete_helper(&mut self, node: &mut Box<TrieNode>, word: &str, index: usize) -> bool {
        let chars: Vec<char> = word.chars().collect();

        if index == chars.len() {
            if !node.is_end_of_word {
                return false;
            }

            node.is_end_of_word = false;
            self.word_count -= 1;
            return node.children.is_empty();
        }

        let ch = chars[index];

        let should_delete = if let Some(child) = node.children.get_mut(&ch) {
            self.delete_helper(child, word, index + 1)
        } else {
            return false;
        };

        if should_delete {
            node.children.remove(&ch);
            return !node.is_end_of_word && node.children.is_empty();
        }

        false
    }

    /// Suggestion for autocomplete
    #[derive(Debug, Clone)]
    pub struct Suggestion {
        pub word: String,
        pub frequency: i32,
    }

    /// Get word suggestions for prefix
    pub fn autocomplete(&self, prefix: &str, limit: usize) -> Vec<Suggestion> {
        let node = match self.find_node(prefix) {
            Some(n) => n,
            None => return Vec::new(),
        };

        let mut suggestions = Vec::new();
        self.dfs_collect_words(node, prefix.to_string(), &mut suggestions);

        // Sort by frequency (descending) and then alphabetically
        suggestions.sort_by(|a, b| {
            if a.frequency != b.frequency {
                b.frequency.cmp(&a.frequency)
            } else {
                a.word.cmp(&b.word)
            }
        });

        suggestions.truncate(limit);
        suggestions
    }

    fn dfs_collect_words(&self, node: &TrieNode, current: String, suggestions: &mut Vec<Suggestion>) {
        if node.is_end_of_word {
            suggestions.push(Suggestion {
                word: current.clone(),
                frequency: node.frequency,
            });
        }

        // Use BTreeMap for sorted iteration
        let sorted_children: BTreeMap<_, _> = node.children.iter().collect();
        for (ch, child) in sorted_children {
            let mut new_current = current.clone();
            new_current.push(*ch);
            self.dfs_collect_words(child, new_current, suggestions);
        }
    }

    /// Find longest common prefix of all words
    pub fn longest_common_prefix(&self) -> String {
        if self.root.children.is_empty() {
            return String::new();
        }

        let mut prefix = String::new();
        let mut node = &*self.root;

        while node.children.len() == 1 && !node.is_end_of_word {
            let (ch, child) = node.children.iter().next().unwrap();
            prefix.push(*ch);
            node = child;
        }

        prefix
    }

    /// Get all words in trie
    pub fn get_all_words(&self) -> Vec<String> {
        let mut words = Vec::new();
        self.dfs_collect_all_words(&self.root, String::new(), &mut words);
        words.sort();
        words
    }

    fn dfs_collect_all_words(&self, node: &TrieNode, current: String, words: &mut Vec<String>) {
        if node.is_end_of_word {
            words.push(current.clone());
        }

        for (ch, child) in &node.children {
            let mut new_current = current.clone();
            new_current.push(*ch);
            self.dfs_collect_all_words(child, new_current, words);
        }
    }

    /// Count how many words have given prefix
    pub fn count_words_with_prefix(&self, prefix: &str) -> usize {
        match self.find_node(prefix) {
            Some(node) => self.count_words_helper(node),
            None => 0,
        }
    }

    fn count_words_helper(&self, node: &TrieNode) -> usize {
        let mut count = if node.is_end_of_word { 1 } else { 0 };

        for child in node.children.values() {
            count += self.count_words_helper(child);
        }

        count
    }

    /// Get word count
    pub fn get_word_count(&self) -> usize {
        self.word_count
    }
}

// ============================================================================
// COMPRESSED TRIE (PATRICIA TREE)
// ============================================================================

/// Node in Patricia trie (compressed trie)
struct PatriciaNode {
    key: String, // Edge label (can be multiple characters)
    children: HashMap<char, Box<PatriciaNode>>,
    is_end_of_word: bool,
    value: String,
}

impl PatriciaNode {
    fn new(key: String) -> Self {
        PatriciaNode {
            key,
            children: HashMap::new(),
            is_end_of_word: false,
            value: String::new(),
        }
    }
}

/// Compressed Trie (Patricia Tree)
pub struct PatriciaTrie {
    root: Box<PatriciaNode>,
}

impl PatriciaTrie {
    /// Create a new Patricia trie
    pub fn new() -> Self {
        PatriciaTrie {
            root: Box::new(PatriciaNode::new(String::new())),
        }
    }

    /// Insert word into Patricia trie
    pub fn insert(&mut self, word: &str, value: &str) {
        if word.is_empty() {
            return;
        }

        let mut node = &mut self.root;
        let mut remaining = word;

        while !remaining.is_empty() {
            let matched_char = remaining.chars().next().unwrap();

            if !node.children.contains_key(&matched_char) {
                // No matching child, create new node
                let mut new_node = Box::new(PatriciaNode::new(remaining.to_string()));
                new_node.is_end_of_word = true;
                new_node.value = if value.is_empty() {
                    word.to_string()
                } else {
                    value.to_string()
                };
                node.children.insert(matched_char, new_node);
                return;
            }

            let child = node.children.get_mut(&matched_char).unwrap();

            // Find common prefix between remaining and child.key
            let common_len = remaining
                .chars()
                .zip(child.key.chars())
                .take_while(|(a, b)| a == b)
                .count();

            if common_len == child.key.len() {
                // Child key is prefix of remaining
                remaining = &remaining[common_len..];
                node = child;
            } else {
                // Need to split the edge
                let common: String = child.key.chars().take(common_len).collect();
                let old_suffix: String = child.key.chars().skip(common_len).collect();

                // Create new intermediate node
                let mut new_node = Box::new(PatriciaNode::new(common.clone()));

                // Update child key
                let old_child_key = child.key.clone();
                child.key = old_suffix.clone();

                // Move old child
                let old_child = std::mem::replace(child, new_node);
                let suffix_char = old_suffix.chars().next().unwrap();
                child.children.insert(suffix_char, old_child);

                remaining = &remaining[common_len..];
                if !remaining.is_empty() {
                    let mut leaf = Box::new(PatriciaNode::new(remaining.to_string()));
                    leaf.is_end_of_word = true;
                    leaf.value = if value.is_empty() {
                        word.to_string()
                    } else {
                        value.to_string()
                    };
                    let rem_char = remaining.chars().next().unwrap();
                    child.children.insert(rem_char, leaf);
                } else {
                    child.is_end_of_word = true;
                    child.value = if value.is_empty() {
                        word.to_string()
                    } else {
                        value.to_string()
                    };
                }
                return;
            }
        }

        node.is_end_of_word = true;
        node.value = if value.is_empty() {
            word.to_string()
        } else {
            value.to_string()
        };
    }

    /// Search for exact word
    pub fn search(&self, word: &str) -> bool {
        if let Some(node) = self.find_node(word) {
            node.is_end_of_word
        } else {
            false
        }
    }

    /// Find node for given word
    fn find_node(&self, word: &str) -> Option<&PatriciaNode> {
        let mut node = &*self.root;
        let mut remaining = word;

        while !remaining.is_empty() {
            let matched_char = remaining.chars().next()?;
            let child = node.children.get(&matched_char)?;

            if !remaining.starts_with(&child.key) {
                return None;
            }

            remaining = &remaining[child.key.len()..];
            node = child;
        }

        if remaining.is_empty() {
            Some(node)
        } else {
            None
        }
    }

    /// Get value for word
    pub fn get_value(&self, word: &str) -> Option<String> {
        self.find_node(word)
            .filter(|node| node.is_end_of_word)
            .map(|node| node.value.clone())
    }
}

// ============================================================================
// SUFFIX TRIE
// ============================================================================

/// Suffix Trie for pattern matching
pub struct SuffixTrie {
    trie: Trie,
    text: String,
}

impl SuffixTrie {
    /// Create a new suffix trie
    pub fn new(text: &str) -> Self {
        let mut trie = Trie::new();

        // Insert all suffixes
        for i in 0..text.len() {
            trie.insert(&text[i..], 1);
        }

        SuffixTrie {
            trie,
            text: text.to_string(),
        }
    }

    /// Check if pattern exists as substring
    pub fn contains_substring(&self, pattern: &str) -> bool {
        self.trie.starts_with(pattern)
    }

    /// Find all starting positions of pattern in text
    pub fn find_all_occurrences(&self, pattern: &str) -> Vec<usize> {
        let mut positions = Vec::new();

        for i in 0..self.text.len() {
            if self.text[i..].starts_with(pattern) {
                positions.push(i);
            }
        }

        positions
    }
}

// ============================================================================
// APPLICATIONS
// ============================================================================

/// Spell checker using trie
pub struct SpellChecker {
    trie: Trie,
}

impl SpellChecker {
    /// Create a new spell checker
    pub fn new(dictionary: &[String]) -> Self {
        let mut trie = Trie::new();

        for word in dictionary {
            trie.insert(&word.to_lowercase(), 1);
        }

        SpellChecker { trie }
    }

    /// Check if word is spelled correctly
    pub fn is_correct(&self, word: &str) -> bool {
        self.trie.search(&word.to_lowercase())
    }

    /// Suggest corrections for misspelled word
    pub fn suggest(&self, word: &str, max_distance: usize) -> Vec<String> {
        let word = word.to_lowercase();

        if self.is_correct(&word) {
            return vec![word];
        }

        let candidates = self.generate_candidates(&word, max_distance);
        let mut suggestions = HashSet::new();

        for candidate in candidates {
            if self.trie.search(&candidate) {
                suggestions.insert(candidate);
            }
        }

        let mut result: Vec<_> = suggestions.into_iter().collect();
        result.sort();
        result.truncate(10);
        result
    }

    fn generate_candidates(&self, word: &str, max_distance: usize) -> HashSet<String> {
        if max_distance == 0 {
            return [word.to_string()].iter().cloned().collect();
        }

        let mut candidates = HashSet::new();
        candidates.insert(word.to_string());
        let alphabet = "abcdefghijklmnopqrstuvwxyz";
        let chars: Vec<char> = word.chars().collect();

        // Deletions
        for i in 0..chars.len() {
            let mut deleted = chars.clone();
            deleted.remove(i);
            candidates.insert(deleted.iter().collect());
        }

        // Transpositions
        for i in 0..chars.len().saturating_sub(1) {
            let mut transposed = chars.clone();
            transposed.swap(i, i + 1);
            candidates.insert(transposed.iter().collect());
        }

        // Replacements
        for i in 0..chars.len() {
            for c in alphabet.chars() {
                let mut replaced = chars.clone();
                replaced[i] = c;
                candidates.insert(replaced.iter().collect());
            }
        }

        // Insertions
        for i in 0..=chars.len() {
            for c in alphabet.chars() {
                let mut inserted = chars.clone();
                inserted.insert(i, c);
                candidates.insert(inserted.iter().collect());
            }
        }

        if max_distance > 1 {
            let mut new_candidates = HashSet::new();
            for candidate in &candidates {
                new_candidates.extend(self.generate_candidates(candidate, max_distance - 1));
            }
            candidates.extend(new_candidates);
        }

        candidates
    }
}

/// Auto-complete system using trie
pub struct AutoComplete {
    trie: Trie,
    recent_searches: VecDeque<String>,
    max_recent: usize,
}

impl AutoComplete {
    /// Create a new auto-complete system
    pub fn new() -> Self {
        AutoComplete {
            trie: Trie::new(),
            recent_searches: VecDeque::new(),
            max_recent: 100,
        }
    }

    /// Add word to auto-complete dictionary
    pub fn add_word(&mut self, word: &str, frequency: i32) {
        self.trie.insert(&word.to_lowercase(), frequency);
    }

    /// Get auto-complete suggestions
    pub fn search(&self, prefix: &str) -> Vec<String> {
        let prefix = prefix.to_lowercase();
        let suggestions = self.trie.autocomplete(&prefix, 10);

        // Boost recent searches
        let recent_set: HashSet<_> = self.recent_searches.iter().collect();
        let mut boosted: Vec<_> = suggestions
            .iter()
            .map(|s| {
                let freq = if recent_set.contains(&s.word) {
                    s.frequency * 2
                } else {
                    s.frequency
                };
                (s.word.clone(), freq)
            })
            .collect();

        boosted.sort_by(|a, b| {
            if a.1 != b.1 {
                b.1.cmp(&a.1)
            } else {
                a.0.cmp(&b.0)
            }
        });

        boosted.iter().map(|(word, _)| word.clone()).collect()
    }

    /// Record user search for boosting
    pub fn record_search(&mut self, query: &str) {
        self.recent_searches.push_back(query.to_lowercase());
        if self.recent_searches.len() > self.max_recent {
            self.recent_searches.pop_front();
        }
    }
}

/// Dictionary implementation using trie
pub struct Dictionary {
    trie: PatriciaTrie,
}

impl Dictionary {
    /// Create a new dictionary
    pub fn new() -> Self {
        Dictionary {
            trie: PatriciaTrie::new(),
        }
    }

    /// Add word with definition
    pub fn add(&mut self, word: &str, definition: &str) {
        self.trie.insert(&word.to_lowercase(), definition);
    }

    /// Get definition for word
    pub fn lookup(&self, word: &str) -> Option<String> {
        self.trie.get_value(&word.to_lowercase())
    }
}

// ============================================================================
// DEMONSTRATION
// ============================================================================

fn demonstrate() {
    println!("{}", "=".repeat(80));
    println!("COMPREHENSIVE TRIE DEMONSTRATIONS");
    println!("{}", "=".repeat(80));

    // Standard Trie
    println!("\n1. STANDARD TRIE");
    println!("{}", "-".repeat(80));
    let mut trie = Trie::new();

    let words = vec!["the", "a", "there", "answer", "any", "by", "bye", "their"];
    println!("Inserting words: {}", words.join(", "));
    for word in &words {
        trie.insert(word, 1);
    }

    println!("\nTotal words: {}", trie.get_word_count());
    println!("Search 'the': {}", trie.search("the"));
    println!("Search 'these': {}", trie.search("these"));
    println!("Starts with 'th': {}", trie.starts_with("th"));

    let autocomplete = trie.autocomplete("th", 10);
    let autocomplete_words: Vec<_> = autocomplete.iter().map(|s| s.word.as_str()).collect();
    println!("\nAuto-complete for 'th': {}", autocomplete_words.join(", "));
    println!("Longest common prefix: '{}'", trie.longest_common_prefix());
    println!("Words with prefix 'the': {}", trie.count_words_with_prefix("the"));

    // Patricia Trie
    println!("\n2. PATRICIA TRIE (Compressed)");
    println!("{}", "-".repeat(80));
    let mut ptrie = PatriciaTrie::new();

    let routes = vec![
        ("192.168.1.0", "Router A"),
        ("192.168.2.0", "Router B"),
        ("192.168.1.1", "Host 1"),
        ("10.0.0.0", "Network B"),
    ];

    for (ip, dest) in &routes {
        ptrie.insert(ip, dest);
        println!("  Added route: {} -> {}", ip, dest);
    }

    println!("\nSearch '192.168.1.0': {}", ptrie.search("192.168.1.0"));
    println!("Search '192.168.1.1': {}", ptrie.search("192.168.1.1"));

    // Suffix Trie
    println!("\n3. SUFFIX TRIE");
    println!("{}", "-".repeat(80));
    let text = "banana";
    let suffix_trie = SuffixTrie::new(text);

    println!("Text: '{}'", text);
    println!("Contains 'ana': {}", suffix_trie.contains_substring("ana"));
    println!("Contains 'nan': {}", suffix_trie.contains_substring("nan"));
    let occurrences = suffix_trie.find_all_occurrences("ana");
    println!("Occurrences of 'ana': {:?}", occurrences);

    // Spell Checker
    println!("\n4. SPELL CHECKER");
    println!("{}", "-".repeat(80));
    let dictionary = vec![
        "hello".to_string(),
        "world".to_string(),
        "python".to_string(),
        "programming".to_string(),
        "algorithm".to_string(),
    ];
    let checker = SpellChecker::new(&dictionary);

    let test_words = vec!["hello", "helo", "wrld", "python", "pyton"];
    for word in &test_words {
        let correct = checker.is_correct(word);
        let suggestions = if !correct {
            checker.suggest(word, 2)
        } else {
            Vec::new()
        };
        print!("  '{}': {}", word, if correct { "✓" } else { "✗" });
        if !suggestions.is_empty() {
            let limited: Vec<_> = suggestions.iter().take(3).collect();
            print!(" → Suggestions: {}", limited.iter().map(|s| s.as_str()).collect::<Vec<_>>().join(", "));
        }
        println!();
    }

    // Auto-Complete
    println!("\n5. AUTO-COMPLETE");
    println!("{}", "-".repeat(80));
    let mut auto_complete = AutoComplete::new();

    let searches = vec![
        ("python", 100),
        ("programming", 80),
        ("program", 60),
        ("javascript", 90),
        ("java", 95),
    ];

    for (word, freq) in &searches {
        auto_complete.add_word(word, *freq);
    }

    println!("Popular searches added");
    println!("\nSuggestions for 'pro': {}", auto_complete.search("pro").join(", "));
    println!("Suggestions for 'ja': {}", auto_complete.search("ja").join(", "));

    // Dictionary
    println!("\n6. DICTIONARY");
    println!("{}", "-".repeat(80));
    let mut dict = Dictionary::new();

    dict.add("algorithm", "A step-by-step procedure for solving a problem");
    dict.add("data structure", "A way of organizing data");
    dict.add("trie", "A tree-like data structure for storing strings");

    println!("Lookup 'trie': {}", dict.lookup("trie").unwrap_or_default());
    println!("Lookup 'algorithm': {}", dict.lookup("algorithm").unwrap_or_default());

    println!("\n{}", "=".repeat(80));
    println!("✨ All demonstrations complete!");
    println!("{}", "=".repeat(80));
}

fn main() {
    demonstrate();
}
