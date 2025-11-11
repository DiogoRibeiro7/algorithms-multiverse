# String Pattern Matching Algorithms

A comprehensive, multi-language implementation of six major string pattern matching algorithms with detailed explanations, performance analysis, and benchmarking.

## 📚 Table of Contents

- [Algorithms Implemented](#algorithms-implemented)
- [Language Support](#language-support)
- [Features](#features)
- [Algorithm Details](#algorithm-details)
- [Usage Examples](#usage-examples)
- [Performance Comparison](#performance-comparison)
- [Benchmarking](#benchmarking)
- [Real-World Applications](#real-world-applications)
- [Build and Run](#build-and-run)

## 🎯 Algorithms Implemented

1. **Knuth-Morris-Pratt (KMP)** - Linear time pattern matching with failure function
2. **Boyer-Moore** - Sublinear best-case performance with two heuristics
3. **Rabin-Karp** - Rolling hash-based matching for multiple patterns
4. **Aho-Corasick** - Multiple pattern matching using trie with failure links
5. **Z-Algorithm** - Linear time pattern matching with Z-array
6. **Manacher's Algorithm** - Linear time palindrome detection

## 💻 Language Support

All algorithms are implemented in:
- **Python** (3.7+)
- **JavaScript** (ES6+, Node.js)
- **Java** (11+)
- **C++** (C++17)
- **Go** (1.16+)
- **Rust** (2021 edition)

## ✨ Features

- ✅ Complete implementation of all 6 algorithms in all 6 languages
- ✅ Detailed preprocessing step explanations
- ✅ Pattern matching with all occurrences
- ✅ Comprehensive performance analysis
- ✅ Edge case handling (empty strings, single characters)
- ✅ Unicode support (where applicable)
- ✅ Visualization of algorithm progress
- ✅ Cross-language benchmarking suite
- ✅ Real-world application examples
- ✅ Detailed documentation and comments

## 📖 Algorithm Details

### 1. Knuth-Morris-Pratt (KMP)

**Time Complexity**: O(n + m)
**Space Complexity**: O(m)

**Key Concept**: Uses a Longest Proper Prefix which is also Suffix (LPS) array to avoid re-examining text characters. When a mismatch occurs, the algorithm uses precomputed information to skip unnecessary comparisons.

**Best For**:
- Text editors (Find functionality)
- DNA sequence matching
- Network packet inspection
- Log file analysis

**Advantages**:
- Linear time guarantee
- Never moves backward in text
- Predictable performance

**Disadvantages**:
- Preprocessing overhead
- Not as fast as Boyer-Moore in practice for large alphabets

### 2. Boyer-Moore

**Time Complexity**: Best O(n/m), Average O(n), Worst O(n*m)
**Space Complexity**: O(|Σ|) where Σ is alphabet size

**Key Concepts**:
1. **Bad Character Rule**: Skip alignments based on mismatched character
2. **Good Suffix Rule**: Skip based on matched suffix
3. Searches from right to left in pattern

**Best For**:
- GNU grep utility
- Text editors with fast search
- Antivirus signature matching
- Large alphabet searches

**Advantages**:
- Sublinear time in best case
- Very fast for large patterns
- Efficient for large alphabets

**Disadvantages**:
- Complex preprocessing
- Can degrade to O(n*m) in worst case
- Higher space overhead

### 3. Rabin-Karp

**Time Complexity**: Average O(n + m), Worst O(n*m)
**Space Complexity**: O(1)

**Key Concept**: Uses rolling hash to quickly compute hash values of all substrings of length m. Compares hashes first, then verifies with character comparison to handle collisions.

**Hash Function**:
```
hash = (c₀ * base^(m-1) + c₁ * base^(m-2) + ... + c_{m-1}) mod prime
```

**Best For**:
- Plagiarism detection
- Multiple pattern matching
- DNA sequence analysis
- Document similarity

**Advantages**:
- Simple implementation
- Easy to extend to multiple patterns
- Good average case performance

**Disadvantages**:
- Hash collisions require verification
- Performance depends on hash quality
- Not as fast as KMP or Boyer-Moore

### 4. Aho-Corasick

**Time Complexity**: O(n + k) where k = number of matches
**Space Complexity**: O(sum of pattern lengths)

**Key Concept**: Builds a trie of patterns with failure links (similar to KMP). Can find all patterns in a single pass through the text, making it extremely efficient for multiple pattern matching.

**Components**:
1. **Trie**: Stores all patterns
2. **Failure Links**: Point to longest proper suffix that is also a prefix of some pattern
3. **Output Links**: Store pattern matches at each node

**Best For**:
- Antivirus scanning (multiple virus signatures)
- Network intrusion detection systems
- Content filtering
- Bioinformatics (multiple gene sequences)

**Advantages**:
- Finds all patterns in single pass
- Linear time regardless of pattern count
- Extremely efficient for multiple patterns

**Disadvantages**:
- High memory usage for many patterns
- Preprocessing overhead
- Overkill for single pattern matching

### 5. Z-Algorithm

**Time Complexity**: O(n + m)
**Space Complexity**: O(n + m)

**Key Concept**: Z[i] = length of longest substring starting at i that is also a prefix of the string. Creates concatenation: pattern + "$" + text, then Z-values equal to pattern length indicate matches.

**Z-Array Properties**:
- Z[0] = n (by definition)
- Z[i] represents match length at position i
- Uses previously computed values to avoid redundant comparisons

**Best For**:
- Pattern matching (alternative to KMP)
- String processing
- Compression algorithms
- Finding repeated substrings

**Advantages**:
- Simple and elegant
- Linear time guarantee
- Easy to understand and implement

**Disadvantages**:
- Requires concatenation of strings
- Higher space usage than KMP
- Not as fast as Boyer-Moore in practice

### 6. Manacher's Algorithm

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Key Concept**: Finds all palindromes in linear time using:
1. Transform string to handle even/odd length palindromes uniformly (insert '#' between characters)
2. Use previously computed palindrome information to avoid redundant checks

**Transformation**: `"aba"` → `"#a#b#a#"`

**Best For**:
- DNA sequence analysis
- Text compression
- Finding repeated structures
- Natural language processing
- Longest palindromic substring problems

**Advantages**:
- Linear time for all palindromes
- Handles both even and odd length palindromes
- Elegant algorithm

**Disadvantages**:
- Specific to palindrome detection
- String transformation overhead
- Not applicable to general pattern matching

## 🚀 Usage Examples

### Python

```python
from pattern_matching import KMP, BoyerMoore, RabinKarp, AhoCorasick, ZAlgorithm, Manacher

text = "ABABCABABABCABAB"
pattern = "ABAB"

# Single pattern matching
matches = KMP.search(text, pattern)
print(f"KMP matches: {matches}")  # [0, 5, 9, 12]

matches = BoyerMoore.search(text, pattern)
print(f"Boyer-Moore matches: {matches}")

matches = RabinKarp().search(text, pattern)
print(f"Rabin-Karp matches: {matches}")

matches = ZAlgorithm.search(text, pattern)
print(f"Z-Algorithm matches: {matches}")

# Multiple pattern matching
ac = AhoCorasick()
ac.add_pattern("ABAB", 0)
ac.add_pattern("ABC", 1)
ac.add_pattern("CAB", 2)
ac.build_failure_links()
results = ac.search(text)
print(f"Aho-Corasick results: {results}")

# Palindrome detection
text = "babad"
longest = Manacher.longest_palindrome(text)
print(f"Longest palindrome: {longest}")  # "bab" or "aba"

all_palindromes = Manacher.find_all_palindromes(text)
for start, end, palindrome in all_palindromes:
    print(f"[{start}:{end}] = '{palindrome}'")
```

### JavaScript

```javascript
const { KMP, BoyerMoore, RabinKarp, AhoCorasick, ZAlgorithm, Manacher } = require('./pattern_matching.js');

const text = "ABABCABABABCABAB";
const pattern = "ABAB";

// Single pattern matching
let matches = KMP.search(text, pattern);
console.log(`KMP matches: [${matches.join(', ')}]`);

matches = BoyerMoore.search(text, pattern);
console.log(`Boyer-Moore matches: [${matches.join(', ')}]`);

matches = new RabinKarp().search(text, pattern);
console.log(`Rabin-Karp matches: [${matches.join(', ')}]`);

// Multiple pattern matching
const ac = new AhoCorasick();
ac.addPattern("ABAB", 0);
ac.addPattern("ABC", 1);
ac.buildFailureLinks();
const results = ac.search(text);
console.log(`Aho-Corasick results:`, results);

// Palindrome detection
const palindromeText = "babad";
const longest = Manacher.longestPalindrome(palindromeText);
console.log(`Longest palindrome: '${longest}'`);
```

### Java

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        String text = "ABABCABABABCABAB";
        String pattern = "ABAB";

        // Single pattern matching
        List<Integer> matches = KMP.search(text, pattern);
        System.out.println("KMP matches: " + matches);

        matches = BoyerMoore.search(text, pattern);
        System.out.println("Boyer-Moore matches: " + matches);

        RabinKarp rk = new RabinKarp();
        matches = rk.search(text, pattern);
        System.out.println("Rabin-Karp matches: " + matches);

        // Multiple pattern matching
        AhoCorasick ac = new AhoCorasick();
        ac.addPattern("ABAB", 0);
        ac.addPattern("ABC", 1);
        ac.buildFailureLinks();
        Map<Integer, List<Integer>> results = ac.search(text);
        System.out.println("Aho-Corasick results: " + results);

        // Palindrome detection
        String palindromeText = "babad";
        String longest = Manacher.longestPalindrome(palindromeText);
        System.out.println("Longest palindrome: '" + longest + "'");
    }
}
```

### C++

```cpp
#include "pattern_matching.cpp"
#include <iostream>

int main() {
    std::string text = "ABABCABABABCABAB";
    std::string pattern = "ABAB";

    // Single pattern matching
    auto matches = KMP::search(text, pattern);
    std::cout << "KMP matches: ";
    for (int m : matches) std::cout << m << " ";
    std::cout << std::endl;

    matches = BoyerMoore::search(text, pattern);
    std::cout << "Boyer-Moore matches: ";
    for (int m : matches) std::cout << m << " ";
    std::cout << std::endl;

    // Multiple pattern matching
    AhoCorasick ac;
    ac.addPattern("ABAB", 0);
    ac.addPattern("ABC", 1);
    ac.buildFailureLinks();
    auto results = ac.search(text);

    // Palindrome detection
    std::string palindromeText = "babad";
    std::string longest = Manacher::longestPalindrome(palindromeText);
    std::cout << "Longest palindrome: '" << longest << "'" << std::endl;

    return 0;
}
```

### Go

```go
package main

import (
    "fmt"
)

func main() {
    text := "ABABCABABABCABAB"
    pattern := "ABAB"

    // Single pattern matching
    kmp := &KMP{}
    matches := kmp.Search(text, pattern, false)
    fmt.Printf("KMP matches: %v\n", matches)

    bm := &BoyerMoore{}
    matches = bm.Search(text, pattern, false)
    fmt.Printf("Boyer-Moore matches: %v\n", matches)

    // Multiple pattern matching
    ac := NewAhoCorasick()
    ac.AddPattern("ABAB")
    ac.AddPattern("ABC")
    ac.BuildFailureLinks()
    results := ac.Search(text, false)
    fmt.Printf("Aho-Corasick results: %v\n", results)

    // Palindrome detection
    palindromeText := "babad"
    manacher := &Manacher{}
    longest := manacher.LongestPalindrome(palindromeText)
    fmt.Printf("Longest palindrome: '%s'\n", longest)
}
```

### Rust

```rust
fn main() {
    let text = "ABABCABABABCABAB";
    let pattern = "ABAB";

    // Single pattern matching
    let matches = KMP::search(text, pattern, false);
    println!("KMP matches: {:?}", matches);

    let matches = BoyerMoore::search(text, pattern, false);
    println!("Boyer-Moore matches: {:?}", matches);

    // Multiple pattern matching
    let mut ac = AhoCorasick::new();
    ac.add_pattern("ABAB");
    ac.add_pattern("ABC");
    ac.build_failure_links();
    let results = ac.search(text, false);
    println!("Aho-Corasick results: {:?}", results);

    // Palindrome detection
    let palindrome_text = "babad";
    let longest = Manacher::longest_palindrome(palindrome_text);
    println!("Longest palindrome: '{}'", longest);
}
```

## 📊 Performance Comparison

### Time Complexity Comparison

| Algorithm | Preprocessing | Searching | Total | Best Case | Worst Case |
|-----------|---------------|-----------|-------|-----------|------------|
| KMP | O(m) | O(n) | O(n + m) | O(n) | O(n + m) |
| Boyer-Moore | O(m + \|Σ\|) | O(n/m) - O(n*m) | O(n + m + \|Σ\|) | O(n/m) | O(n*m) |
| Rabin-Karp | O(m) | O(n) | O(n + m) | O(n) | O(n*m) |
| Aho-Corasick | O(Σm) | O(n + k) | O(Σm + n + k) | O(n) | O(n + k) |
| Z-Algorithm | O(n + m) | O(n + m) | O(n + m) | O(n) | O(n + m) |
| Manacher | O(n) | O(n) | O(n) | O(n) | O(n) |

*Where: n = text length, m = pattern length, Σ = sum of pattern lengths, k = number of matches, |Σ| = alphabet size*

### Space Complexity Comparison

| Algorithm | Space Complexity | Notes |
|-----------|------------------|-------|
| KMP | O(m) | LPS array |
| Boyer-Moore | O(m + \|Σ\|) | Bad character + good suffix tables |
| Rabin-Karp | O(1) | Constant extra space |
| Aho-Corasick | O(Σm) | Trie with failure links |
| Z-Algorithm | O(n + m) | Z-array for concatenated string |
| Manacher | O(n) | Palindrome radius array |

### When to Use Each Algorithm

**Use KMP when**:
- You need guaranteed linear time
- Text is read sequentially (streaming)
- Pattern is relatively small
- You want predictable performance

**Use Boyer-Moore when**:
- Alphabet is large (e.g., ASCII, Unicode)
- Pattern is long
- You want best practical performance
- Text is in memory

**Use Rabin-Karp when**:
- Multiple patterns need to be searched
- Pattern matching with wildcards
- String similarity/distance needed
- Implementing plagiarism detection

**Use Aho-Corasick when**:
- Searching for multiple patterns simultaneously
- Implementing antivirus/IDS systems
- Content filtering
- Pattern count is large

**Use Z-Algorithm when**:
- You need a simple linear-time solution
- Finding all occurrences of pattern
- String processing tasks
- Alternative to KMP

**Use Manacher when**:
- Finding palindromes
- Longest palindromic substring
- DNA sequence analysis
- String compression

## 🧪 Benchmarking

### Running Benchmarks

Run the comprehensive cross-language benchmark suite:

```bash
# Python benchmarks
python string-algorithms/pattern_matching.py

# JavaScript benchmarks
node string-algorithms/pattern_matching.js

# Java benchmarks
cd string-algorithms
javac PatternMatching.java
java PatternMatching

# C++ benchmarks
cd string-algorithms
g++ -std=c++17 -O3 -o pattern_matching pattern_matching.cpp
./pattern_matching

# Go benchmarks
cd string-algorithms
go run pattern_matching.go

# Rust benchmarks
cd string-algorithms
rustc -O pattern_matching.rs
./pattern_matching

# Cross-language comparison
python string-algorithms/benchmark_suite.py
```

### Benchmark Results

Results are saved in:
- `benchmark_results.json` - Detailed JSON format
- `benchmark_results.csv` - CSV format for spreadsheet analysis

## 🌍 Real-World Applications

### Text Editors
- **Algorithms**: KMP, Boyer-Moore
- **Use Case**: Find and replace functionality
- **Why**: Fast substring search with guaranteed performance

### Antivirus Software
- **Algorithm**: Aho-Corasick
- **Use Case**: Scanning for multiple virus signatures
- **Why**: Efficient multiple pattern matching in single pass

### DNA Sequence Analysis
- **Algorithms**: KMP, Aho-Corasick, Manacher
- **Use Case**: Finding genes, motifs, palindromic sequences
- **Why**: Linear time, handles large genomic data

### Plagiarism Detection
- **Algorithm**: Rabin-Karp
- **Use Case**: Document similarity, copy detection
- **Why**: Rolling hash enables efficient substring comparison

### Network Intrusion Detection
- **Algorithm**: Aho-Corasick
- **Use Case**: Detecting malicious patterns in network traffic
- **Why**: Real-time multiple pattern matching

### Search Engines
- **Algorithms**: Boyer-Moore, Aho-Corasick
- **Use Case**: Web crawling, indexing, query matching
- **Why**: Fast pattern matching at scale

### Log File Analysis
- **Algorithms**: KMP, Boyer-Moore
- **Use Case**: Finding error patterns, monitoring
- **Why**: Efficient searching through large log files

### Compression Algorithms
- **Algorithms**: Z-Algorithm, Manacher
- **Use Case**: Finding repeated substrings
- **Why**: Identifying patterns for compression

## 🔧 Build and Run

### Prerequisites

- **Python**: 3.7 or higher
- **JavaScript**: Node.js 12 or higher
- **Java**: JDK 11 or higher
- **C++**: g++ with C++17 support
- **Go**: 1.16 or higher
- **Rust**: 1.50 or higher (2021 edition)

### Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd algorithms-multiverse/string-algorithms

# Run Python implementation
python pattern_matching.py

# Run JavaScript implementation
node pattern_matching.js

# Compile and run Java
javac PatternMatching.java
java PatternMatching

# Compile and run C++
g++ -std=c++17 -O3 -o pattern_matching pattern_matching.cpp
./pattern_matching

# Run Go
go run pattern_matching.go

# Compile and run Rust
rustc -O pattern_matching.rs
./pattern_matching
```

### Visualization Mode

All implementations support visualization mode to see algorithm progress:

```python
# Python
matches = KMP.search(text, pattern, visualize=True)
```

```javascript
// JavaScript
const matches = KMP.search(text, pattern, true);
```

```java
// Java
List<Integer> matches = KMP.search(text, pattern, true);
```

## 📝 Algorithm Visualizations

Each algorithm includes visualization mode that shows:
- Current comparison position
- Pattern shifts/movements
- Matches found
- Preprocessing information (LPS array, hash values, etc.)

Example KMP visualization:
```
KMP Algorithm Visualization:
Text:    ABABCABABABCABAB
Pattern: ABAB
LPS:     [0, 0, 1, 2]

Comparing at position 0: 'ABAB'
✓ Match found at index 0
Comparing at position 4: 'CABABABCABAB'
  Mismatch at position 4, using LPS to skip to j=0
Comparing at position 5: 'ABABABCABAB'
✓ Match found at index 5
...
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional optimizations
- More test cases
- Performance improvements
- Additional languages
- Bug fixes
- Documentation improvements

## 📄 License

This project is part of the algorithms-multiverse repository. See the main repository for license information.

## 📚 References

### Academic Papers
1. Knuth, D. E., Morris, J. H., & Pratt, V. R. (1977). "Fast pattern matching in strings"
2. Boyer, R. S., & Moore, J. S. (1977). "A fast string searching algorithm"
3. Karp, R. M., & Rabin, M. O. (1987). "Efficient randomized pattern-matching algorithms"
4. Aho, A. V., & Corasick, M. J. (1975). "Efficient string matching: An aid to bibliographic search"
5. Gusfield, D. (1997). "Algorithms on Strings, Trees, and Sequences"
6. Manacher, G. (1975). "A new linear-time on-line algorithm for finding the smallest initial palindrome"

### Books
- "Introduction to Algorithms" by Cormen, Leiserson, Rivest, and Stein (CLRS)
- "Algorithms" by Robert Sedgewick and Kevin Wayne
- "The Algorithm Design Manual" by Steven Skiena
- "Algorithms on Strings, Trees, and Sequences" by Dan Gusfield

### Online Resources
- [CP-Algorithms: String Algorithms](https://cp-algorithms.com/string/)
- [GeeksforGeeks: Pattern Searching](https://www.geeksforgeeks.org/algorithms-gq/pattern-searching/)
- [Wikipedia: String Searching Algorithms](https://en.wikipedia.org/wiki/String-searching_algorithm)

---

**Note**: All implementations are optimized for clarity and educational purposes while maintaining good performance. For production use, consider language-specific string matching libraries that may include additional optimizations.
